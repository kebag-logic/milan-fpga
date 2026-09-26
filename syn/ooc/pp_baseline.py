#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Prepare measurement scripts from an exported AX7101 shipping build.

Run the integrated script first. Its synthesis log supplies every wrapper
parameter for the standalone script; no second parameter table is maintained.
All generated scripts, checkpoints and reports belong outside the repository.
"""

import argparse
import contextlib
import hashlib
import io
import json
from pathlib import Path
import re
import tempfile


ROM_ERROR = "set_msg_config -id {Synth 8-4445} -new_severity ERROR\n"
REPORTS = """
report_utilization -hierarchical -hierarchical_depth 10 -hierarchical_min_primitive_count 0 -file baseline_hierarchy.rpt
report_utilization -file baseline_utilization.rpt
report_timing_summary -max_paths 10 -file baseline_timing.rpt
set pf [open baseline_cells.tsv w]
puts $pf "cell\\tprimitive"
foreach c [get_cells -hier -filter {IS_PRIMITIVE == 1}] {
  puts $pf "$c\\t[get_property REF_NAME $c]"
}
close $pf
"""
PP_REPORTS = """
set pp [get_cells -hier -filter {ORIG_REF_NAME == KL_pp_shadow || REF_NAME == KL_pp_shadow}]
if {[llength $pp] != 1} { error "Expected exactly one protocol wrapper" }
report_utilization -cells $pp -file baseline_pp_utilization.rpt
report_timing -through [get_pins -of_objects $pp] -max_paths 10 -file baseline_pp_boundary_timing.rpt
"""
SCOPE_TIMING = """
set scope_root ""
set pp [get_cells -quiet -hier -filter {ORIG_REF_NAME == KL_pp_shadow || REF_NAME == KL_pp_shadow}]
if {[llength $pp] == 1} {
  set scope_root "$pp/"
} elseif {[llength $pp] == 0} {
  set core [get_cells -quiet u_pp]
  if {[llength $core] != 1 || [get_property ORIG_REF_NAME $core] ne "protocol_processor_top"} {
    error "Expected the standalone wrapper's processor instance"
  }
} else {
  error "Expected exactly one protocol wrapper"
}
set tf [open baseline_scope_timing.tsv w]
puts $tf "instance\\tsequential_cells\\tinternal_WNS_ns"
foreach relative {wrapper u_pp u_pp/u_aecp u_pp/u_srp u_pp/u_notify u_pp/u_listener u_pp/u_talker u_nvm} {
  set path "$scope_root$relative"
  if {$relative eq "wrapper"} {
    set path [string trimright $scope_root /]
  }
  if {$path eq ""} {
    set path KL_pp_shadow
    set regs [get_cells -hier -filter {IS_SEQUENTIAL == 1}]
  } else {
    set regs [get_cells -hier -filter [format {NAME =~ "%s/*" && IS_SEQUENTIAL == 1} $path]]
  }
  set worst [get_timing_paths -from $regs -to $regs -max_paths 1]
  if {[llength $worst] != 1} { error "No internal timing path for $path" }
  puts $tf "$path\\t[llength $regs]\\t[get_property SLACK $worst]"
  flush $tf
}
close $tf
"""


def split_once(text: str, marker: str) -> tuple[str, str]:
    """Refuse a changed template instead of silently selecting another stage."""
    if text.count(marker) != 1:
        raise ValueError(f"expected exactly one template marker: {marker}")
    return tuple(text.split(marker))


def parameters(log: str) -> dict[str, int | str]:
    """Read only the wrapper's elaborated parameter block."""
    marker = "synthesizing module 'KL_pp_shadow' "
    _, after = split_once(log, marker)
    block = after.split("\n", 1)[1].split("INFO:", 1)[0]
    values = {}
    for name, raw in re.findall(r"Parameter (\w+) bound to: ([^\n]+)", block):
        if name in values:
            raise ValueError(f"duplicate parameter: {name}")
        raw = raw.strip()
        binary = re.fullmatch(r"\d+'b([01]+)", raw)
        integer = re.fullmatch(r"(\d+) - type: integer", raw)
        if binary:
            values[name] = int(binary[1], 2)
        elif integer:
            values[name] = int(integer[1])
        elif raw.endswith(" - type: string"):
            values[name] = raw.removesuffix(" - type: string")
        else:
            raise ValueError(f"unsupported parameter value: {name}={raw}")
    if not values:
        raise ValueError("no wrapper parameters in synthesis log")
    return values


def image_record(path: Path, words: int | None, width: int | None) -> dict:
    """Hash the actual input, checking complete ROM geometry when supplied."""
    data = path.read_bytes()
    body = re.sub(r"/\*.*?\*/|//[^\n]*", "", data.decode(), flags=re.S)
    tokens = body.split()
    if not all(re.fullmatch(r"[0-9a-fA-F]+", word) for word in tokens):
        raise ValueError(f"unknown or non-hexadecimal image word: {path}")
    if words is not None and len(tokens) != words:
        raise ValueError(f"wrong image depth: {path}: {len(tokens)} != {words}")
    if width is not None and any(len(word) != (width + 3) // 4 for word in tokens):
        raise ValueError(f"wrong image width: {path}")
    return dict(path=str(path), bytes=len(data), words=len(tokens),
                digits=sorted({len(word) for word in tokens}),
                sha256=hashlib.sha256(data).hexdigest())


def wrapper_parameters(log: str, wrapper: str) -> dict[str, int | str]:
    """Include literal defaults omitted from Vivado's override-only log."""
    values = parameters(log)
    wrapper = re.sub(r"/\*.*?\*/|//[^\n]*", "", wrapper, flags=re.S)
    declarations = dict(re.findall(
        r"\bparameter\s+(?:int unsigned|logic\s*\[[^]]+\]|string)\s+"
        r"(\w+)\s*=\s*([^,\n]+)", wrapper))
    for name in set(declarations) - set(values):
        literal = declarations[name].strip().replace("_", "")
        if not re.fullmatch(r"\d+", literal):
            raise ValueError(f"unreported non-literal default: {name}")
        values[name] = int(literal)
    if set(values) != set(declarations):
        raise ValueError("log parameters differ from wrapper declaration")
    return values


def package_number(source: str, name: str) -> int:
    """Read one decimal geometry declaration from its source package."""
    source = re.sub(r"/\*.*?\*/|//[^\n]*", "", source, flags=re.S)
    hits = re.findall(r"\b(?:localparam|parameter)\b[^;=]*\b" + name
                      + r"\s*=\s*(\d+)\s*;", source)
    if len(hits) != 1:
        raise ValueError(f"expected one decimal declaration of {name}")
    return int(hits[0])


def inventory(gateware: Path, source: str) -> list[dict]:
    """Bind control ROMs and generated firmware/memory inputs to their bytes."""
    verilog = (gateware / "alinx_ax7101.v").read_text()
    inputs = []
    for name, words, width in re.findall(
            r"// Memory (\w+): (\d+)-words x (\d+)-bit", verilog):
        path = gateware / f"alinx_ax7101_{name}.init"
        if not path.exists():
            continue
        # LiteX intentionally emits an empty init for writable SRAM.
        # Its existence is mandatory; emptiness is not accepted for a ROM.
        if name == "sram":
            inputs.append(image_record(path, 0, None))
        else:
            inputs.append(image_record(path, int(words), int(width)))
    expected = set(re.findall(r'\$readmemh\("([^"\n]+)"', verilog))
    if expected != {Path(row["path"]).name for row in inputs}:
        raise ValueError("generated memory inventory differs from readmemh inputs")
    files = [Path(p) for p in re.findall(r"^read_verilog (?:-v )?\{([^}]+)\}",
                                       source, re.M)]
    for parameter, package, depth, width in (
            ("PP_TROM_HEX_P", "pp_acmp_pkg.sv", "TROM_DEPTH_C", "TROM_W_C"),
            ("PP_UCODE_HEX_P", "ucpu_pkg.sv", "UPC_W_C", "UCODE_W_C"),
            ("GPTP_UCODE_HEX_P", "gptp_ucpu_pkg.sv", "UPC_W_C", "UCODE_W_C")):
        matches = re.findall(r"\." + parameter + r'\s*\("([^"\n]+)"\)', verilog)
        packages = [path for path in files if path.name == package]
        if len(matches) != 1 or len(packages) != 1:
            raise ValueError(f"ambiguous image or geometry source: {parameter}")
        text = packages[0].read_text()
        count = package_number(text, depth)
        if depth == "UPC_W_C":
            count = 1 << count
        inputs.append(image_record(Path(matches[0]), count,
                                   package_number(text, width)))
    return inputs


def prepare(gateware: Path, output: Path, log: Path | None,
            synthesis_only: bool, attribution_only: bool = False) -> None:
    """Retain the exported build's sources, includes and synthesis directive."""
    source = (gateware / "alinx_ax7101.tcl").read_text()
    prefix, rest = split_once(source, "# Add constraints")
    prefix += ROM_ERROR
    if log is None and output != gateware:
        raise ValueError("integrated scripts must run in their gateware directory")
    if attribution_only:
        if log is not None:
            raise ValueError("attribution requires an integrated build")
        constraint = "set_property KEEP_HIERARCHY TRUE [get_cells milan_datapath/pp_shadow]\n"
        (gateware / "baseline_boundary.xdc").write_text(constraint)
        prefix += "read_xdc baseline_boundary.xdc\n"
    output.mkdir(parents=True, exist_ok=True)
    images = inventory(gateware, source)
    (output / "baseline_images.json").write_text(json.dumps(images, indent=2) + "\n")
    if log is None:
        marker = "# Add pre-optimize commands" if synthesis_only else "# Bitstream generation"
        endpoint, _ = split_once(rest, marker)
        script = prefix + "# Add constraints" + endpoint + REPORTS + PP_REPORTS
        target = output / "baseline_integrated.tcl"
    else:
        wrapper = next(Path(p) for p in re.findall(
            r"^read_verilog (?:-v )?\{([^}]+)\}", source, re.M)
                       if Path(p).name == "KL_pp_shadow.sv")
        values = wrapper_parameters(log.read_text(), wrapper.read_text())
        (output / "baseline_parameters.json").write_text(json.dumps(values, indent=2) + "\n")
        numeric = " ".join(f"{key}={value}" for key, value in values.items()
                           if isinstance(value, int))
        (output / "baseline_chparam.txt").write_text(numeric + "\n")
        generics = []
        for key, value in values.items():
            if isinstance(value, str):
                if any(char in value for char in '{}"\n'):
                    raise ValueError("unsupported character in image pathname")
                value = f'"{value}"'
            generics.append(f"-generic {{{key}={value}}}")
        commands = re.findall(r"^synth_design [^\n]+", source, re.M)
        if len(commands) != 1:
            raise ValueError("expected exactly one integrated synthesis command")
        command = commands[0].replace("-top alinx_ax7101", "-top KL_pp_shadow")
        if command == commands[0]:
            raise ValueError("unexpected integrated synthesis top")
        clock = "create_clock -period 10.000 -name clk [get_ports clk_i]\n"
        (output / "clock.xdc").write_text(clock)
        script = (prefix + "\nread_xdc clock.xdc\n" + command
                  + " -mode out_of_context " + " ".join(generics) + "\n"
                  + REPORTS + "\nwrite_checkpoint -force baseline_synth.dcp\n")
        target = output / "baseline_ooc.tcl"
    target.write_text(script + SCOPE_TIMING + "\nquit\n")
    print(target)


def selftest() -> None:
    """Reject wrong parameter blocks and missing or partial ROM images."""
    log = ("INFO: synthesizing module 'KL_pp_shadow' [wrapper.sv:1]\n"
           "\tParameter N_STREAM_IN_P bound to: 32'b10\n"
           "INFO: synthesizing module 'other' [other.sv:1]\n"
           "\tParameter N_STREAM_IN_P bound to: 32'b111\n")
    wrapper = ("parameter int unsigned N_STREAM_IN_P = 8,\n"
               "parameter int unsigned RX_FIFO_BYTES_P = 4096,\n")
    values = wrapper_parameters(log, wrapper)
    if values != {"N_STREAM_IN_P": 2, "RX_FIFO_BYTES_P": 4096}:
        raise AssertionError("wrong module or omitted default accepted")
    refused = 0
    with tempfile.TemporaryDirectory(prefix="pp-baseline-test-") as tmp:
        path = Path(tmp) / "rom.hex"
        path.write_text("12345678\nabcdef01\n")
        if image_record(path, 2, 32)["words"] != 2:
            raise AssertionError("complete image refused")
        for contents in ("", "12345678\n", "12345678\nabcdef0x\n",
                         "1234\n5678\n", "12345678\nabcdef01\n12345678\n"):
            path.write_text(contents)
            try:
                image_record(path, 2, 32)
            except ValueError:
                refused += 1
            else:
                raise AssertionError("incomplete or invalid image accepted")
        path.unlink()
        try:
            image_record(path, 2, 32)
        except FileNotFoundError:
            refused += 1
        else:
            raise AssertionError("missing image accepted")
    for changed in (log.replace("'KL_pp_shadow'", "'another_top'"), log + log):
        try:
            parameters(changed)
        except ValueError:
            refused += 1
        else:
            raise AssertionError("ambiguous wrapper accepted")
    try:
        wrapper_parameters(log, wrapper.replace("4096", "2 * 2048"))
    except ValueError:
        refused += 1
    else:
        raise AssertionError("unreported expression guessed")
    print(f"baseline selftest: complete image and exact block PASS; {refused} refusals PASS")
    export_selftest()


def export_selftest() -> None:
    """Exercise inventory, emitted enforcement, and the real CLI refusal."""
    with tempfile.TemporaryDirectory(prefix="pp-baseline-export-") as tmp:
        gateware = Path(tmp) / "gateware"
        gateware.mkdir()
        declarations = []
        reads = []
        for parameter, package, depth, width in (
                ("PP_TROM_HEX_P", "pp_acmp_pkg.sv", "TROM_DEPTH_C", "TROM_W_C"),
                ("PP_UCODE_HEX_P", "ucpu_pkg.sv", "UPC_W_C", "UCODE_W_C"),
                ("GPTP_UCODE_HEX_P", "gptp_ucpu_pkg.sv", "UPC_W_C", "UCODE_W_C")):
            path = gateware / package
            path.write_text(f"parameter {depth} = {'2' if depth == 'TROM_DEPTH_C' else '1'};\n"
                            f"parameter {width} = 32;\n")
            rom = gateware / f"{parameter}.hex"
            rom.write_text("12345678\nabcdef01\n")
            declarations.append(f'.{parameter}("{rom}")')
            reads.append(f"read_verilog {{{path}}}\n")
        wrapper = gateware / "KL_pp_shadow.sv"
        wrapper.write_text("parameter int unsigned N_STREAM_IN_P = 2,\n")
        reads.append(f"read_verilog {{{wrapper}}}\n")
        verilog = '\n'.join(declarations) + '\n'
        for name, words in (("rom", 2), ("sram", 4)):
            verilog += (f"// Memory {name}: {words}-words x 32-bit\n"
                        f'$readmemh("alinx_ax7101_{name}.init", mem);\n')
            (gateware / f"alinx_ax7101_{name}.init").write_text(
                "12345678\nabcdef01\n" if name == "rom" else "")
        generated = gateware / "alinx_ax7101.v"
        generated.write_text(verilog)
        source = ("".join(reads) + "# Add constraints\n"
                  "synth_design -top alinx_ax7101 -part xc7a100t-fgg484-2\n"
                  "# Add pre-optimize commands\n# Bitstream generation\n")
        (gateware / "alinx_ax7101.tcl").write_text(source)
        log = gateware / "synthesis.log"
        log.write_text("INFO: synthesizing module 'KL_pp_shadow' [wrapper.sv:1]\n"
                       "Parameter N_STREAM_IN_P bound to: 2 - type: integer\nINFO: end\n")
        if len(inventory(gateware, source)) != 5:
            raise AssertionError("complete export inventory refused")
        standalone = Path(tmp) / "ooc"
        for destination, evidence, synth_only, filename in (
                (gateware, None, False, "baseline_integrated.tcl"),
                (gateware, None, True, "baseline_integrated.tcl"),
                (standalone, log, False, "baseline_ooc.tcl")):
            prepare(gateware, destination, evidence, synth_only)
            script = (destination / filename).read_text()
            # This literal oracle must not disappear with ROM_ERROR itself.
            promotion = "set_msg_config -id {Synth 8-4445} -new_severity ERROR\n"
            if script.count(promotion) != 1 or script.index(promotion) > script.index("synth_design "):
                raise AssertionError(f"missing pre-synthesis ROM promotion: {filename}")
        prepare(gateware, gateware, None, True, attribution_only=True)
        script = (gateware / "baseline_integrated.tcl").read_text()
        constraint = (gateware / "baseline_boundary.xdc").read_text()
        expected = "set_property KEEP_HIERARCHY TRUE [get_cells milan_datapath/pp_shadow]\n"
        if constraint != expected or "read_xdc baseline_boundary.xdc\n" not in script:
            raise AssertionError("attribution boundary constraint is absent or changed")
        if script.index("read_xdc baseline_boundary.xdc") > script.index("synth_design "):
            raise AssertionError("attribution boundary constraint follows synthesis")
        mutations = [
            (gateware / "alinx_ax7101_rom.init", None),
            (gateware / "alinx_ax7101_sram.init", "12345678\n"),
            (generated, verilog.replace('alinx_ax7101_rom.init",', 'unlisted.init",')),
        ]
        for parameter in ("PP_TROM_HEX_P", "PP_UCODE_HEX_P", "GPTP_UCODE_HEX_P"):
            mutations.append((gateware / f"{parameter}.hex", "12345678\n"))
        for path, replacement in mutations:
            original = path.read_text()
            try:
                if replacement is None:
                    path.unlink()
                else:
                    path.write_text(replacement)
                try:
                    prepare(gateware, gateware, None, True)
                except (ValueError, FileNotFoundError):
                    pass
                else:
                    raise AssertionError(f"invalid export accepted: {path.name}")
            finally:
                path.write_text(original)
        # Use an existing directory: no test output can be left in the tree.
        # With the guard removed, prepare() reaches its directory mismatch;
        # that ValueError must not count as the expected argparse refusal.
        root = Path(__file__).resolve().parents[2]
        with contextlib.redirect_stderr(io.StringIO()):
            try:
                main([str(gateware), "--output", str(root)])
            except SystemExit as error:
                if error.code != 2:
                    raise AssertionError("wrong in-repository refusal") from error
            else:
                raise AssertionError("in-repository output accepted")
        print("baseline export selftest: 3 default scripts, attribution constraint, "
              "6 inventory refusals, CLI refusal PASS")


def main(argv: list[str] | None = None) -> None:
    """Prepare one explicit measurement endpoint without launching tools."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("gateware", type=Path, nargs="?")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--integrated-log", type=Path,
                        help="derive standalone parameters from this synthesis log")
    parser.add_argument("--synthesis-only", action="store_true")
    parser.add_argument("--attribution-only", action="store_true",
                        help="preserve the integrated protocol-wrapper boundary")
    args = parser.parse_args(argv)
    if args.selftest:
        selftest()
        return
    if args.gateware is None:
        parser.error("gateware directory is required")
    gateware = args.gateware.resolve()
    output = args.output.resolve() if args.output else gateware
    root = Path(__file__).resolve().parents[2]
    if output.is_relative_to(root):
        parser.error("measurement output must be outside the repository")
    if args.integrated_log and (args.synthesis_only or args.attribution_only):
        parser.error("--synthesis-only and --attribution-only require the integrated endpoint")
    prepare(gateware, output, args.integrated_log, args.synthesis_only,
            args.attribution_only)


if __name__ == "__main__":
    main()
