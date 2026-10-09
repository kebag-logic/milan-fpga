# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Build wire observations against an unchanged, explicitly selected processor tree."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
REFERENCE = {
    1: ("2ad2f845dd583f8310075fa2380cb60a04fd091a", "289fcd1ac47f29b5926e6655954ec4ad1bfe660fe2d2af45fc0fe2eaaadef0fc"),
    2: ("c9f74b6866a63dd3c0e4534724bfc07a86ad142b", "6cd79f9f8be863cc27b2af684dbe3981c5502983a0ba9a10cd305e21f940cc7e"),
}


def run(command: list[str], directory: Path, log: Path) -> None:
    """Preserve every command's complete verdict without shell pipelines."""
    with log.open("w", encoding="utf-8") as sink:
        subprocess.run(command, cwd=directory, stdout=sink, stderr=subprocess.STDOUT,
                       check=True, timeout=540)


def replace_once(text: str, before: str, after: str) -> str:
    """Refuse a drifted reference instead of silently changing the wrong fixture."""
    if text.count(before) != 1:
        raise ValueError(f"reference marker has {text.count(before)} matches: {before}")
    return text.replace(before, after)


def physical_fixture(source: str) -> str:
    """Adapt only external observation ports to the generated verification shape."""
    start = source.index("  static uint64_t gsi_value(")
    brace = source.index("{", start)
    depth = 1
    end = brace + 1
    while depth:
        depth += (source[end] == "{") - (source[end] == "}")
        end += 1
    source = source[:start] + (
        "  static uint64_t gsi_value(uint8_t k,uint16_t t,uint16_t i,uint8_t s,uint8_t o) {\n"
        "    return scenario_word(k,t,i,s,o);\n  }") + source[end:]
    for before, after in (
        ("if (fmt == SFMT_MAIN_C || fmt == SFMT_ALT_C) v |= 1;",
         "if (scenario_format(ty,ix,fmt)) v |= 1;"),
        ("const unsigned chans = (fmt == SFMT_ALT_C) ? 2 : 8;",
         "const unsigned chans = (fmt >> 22) & 1023;"),
        ("uint16_t pages = ty == 0x000E ? 1 : 4;", "uint16_t pages = 1;"),
        ("if (co / 8 == page) rows.push_back(v);", "if (page == 0) rows.push_back(v);"),
    ):
        source = replace_once(source, before, after)
    return source


def prepare(reference: Path, output: Path, interfaces: int) -> Path:
    """Copy the reference bench and record the unchanged HDL's content digest."""
    bench = output / "reference/tb/pp_top"
    bench.mkdir(parents=True, exist_ok=True)
    records = {}
    for area in ("hdl", "tb/common", "tb/pp_top"):
        for path in sorted((reference / area).rglob("*")):
            rel = path.relative_to(reference)
            if (path.is_file() and path.suffix in (".sv", ".svh", ".cpp", ".hpp", ".py") and
                    not any(n.startswith(("obj_", "__pycache__")) for n in rel.parts)):
                records[str(path.relative_to(reference))] = hashlib.sha256(path.read_bytes()).hexdigest()
    digest = hashlib.sha256("".join(f"{p} {h}\n" for p, h in records.items()).encode()).hexdigest()
    if digest != REFERENCE[interfaces][1]:
        raise ValueError(f"reference content differs from {REFERENCE[interfaces][0]}")
    (output / "reference-sha256.json").write_text(json.dumps(records, indent=2) + "\n")
    for name in ("Makefile", "sim_main.cpp", "pp_top_wrap.sv"):
        shutil.copy2(reference / "tb/pp_top" / name, bench / name)
    for path in (reference / "tb/pp_top").glob("*.hpp"):
        shutil.copy2(path, bench / path.name)
    shutil.copytree(reference / "tb/common", bench.parent / "common", dirs_exist_ok=True)
    hdl = bench.parents[1] / "hdl"
    if not hdl.exists():
        hdl.symlink_to(reference / "hdl", target_is_directory=True)
    source = (bench / "sim_main.cpp").read_text()
    (bench / "reference.cpp").write_text(physical_fixture(source))
    make = (bench / "Makefile").read_text().replace("--build -j 0", "--build -j 8")
    (bench / "Makefile").write_text(make)
    return bench


def fixture(output: Path) -> None:
    """Generate a two-rate test image; no product configuration is modified."""
    config = yaml.safe_load((ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml").read_text())
    config["clocking"]["audio_unit_rates_hz"] = [48000, 96000]
    path = output / "wire-shape.yaml"
    path.write_text(yaml.safe_dump(config))
    run([sys.executable, "-B", str(ROOT / "sw/firmware/ctrl/aecp/aecp_entity.py"),
         str(path), "-o", str(output / "aecp_entity_gen.h")], ROOT, output / "image.log")


def build(args: argparse.Namespace, bench: Path) -> Path:
    """Build at most one hardware model, then freshly compile every core object."""
    output = args.output
    header = (output / "aecp_entity_gen.h").read_text()
    names = re.search(r"#define AECP_ENTITY_NAMES (\d+)u", header)
    if names is None:
        raise ValueError("generated name capacity is absent")
    wrapper = (bench / "pp_top_wrap.sv").read_text()
    wrapper = replace_once(wrapper, "protocol_processor_top #(",
                           f"protocol_processor_top #(\n      .DESC_NAME_ENTRIES_P ({names[1]}),")
    (bench / "pp_top_wrap.sv").write_text(wrapper)
    flags = ("--cc --exe --build -j 8 --top-module pp_top_wrap -Wall -Wno-fatal "
             '-Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC '
             '-CFLAGS "-std=c++17 -O2 -Wall -Wextra"')
    if args.interfaces == 2:
        flags += ' +define+PP_TOP_IF2 -CFLAGS "-DPP_TOP_IF2"'
    run(["make", "timer-defaults-build", f"VERILATOR={args.verilator}", f"VFLAGS={flags}"],
        bench, output / "fabric-build.log")
    model = bench / "obj_tdf"
    match = re.search(r"^VERILATOR_ROOT = (.+)$", (model / "Vpp_top_wrap.mk").read_text(), re.M)
    if match is None:
        raise ValueError("model include directory missing")
    inc = [f"-I{ROOT/'sw/firmware/ctrl/aecp'}", f"-I{ROOT/'sw/firmware/ctrl/wire'}", f"-I{output}"]
    objects = []
    for name in ("aecp", "aecp_commands", "aecp_maps", "aecp_image", "aecp_state"):
        obj = output / (name + ".o")
        run(["gcc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", *inc, "-c",
             str(ROOT / "sw/firmware/ctrl/aecp" / (name + ".c")), "-o", str(obj)],
            ROOT, output / (name + "-build.log"))
        objects.append(obj)
    objects += [model / n for n in ("Vpp_top_wrap__ALL.a", "verilated.o",
                                    "verilated_threads.o", "verilated_dpi.o")]
    executable = output / "wire"
    flags = [f"-DAECP_WIRE_INTERFACES={args.interfaces}", "-DPP_TOP_TIM_DEFAULTS"]
    if args.interfaces == 2:
        flags.append("-DPP_TOP_IF2")
    run(["c++", "-std=c++17", "-O2", "-pthread", "-Wall", "-Wextra", *inc, *flags,
         f"-I{bench}", f"-I{model}", f"-I{match[1]}/include", f"-I{match[1]}/include/vltstd",
         str(HERE / "aecp_wire.cpp"), *map(str, objects), "-o", str(executable)],
        ROOT, output / "wire-build.log")
    return executable


def main() -> int:
    """Require successful build and observations on every configured ingress."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--interfaces", type=int, choices=(1, 2), default=1)
    parser.add_argument("--verilator", required=True)
    args = parser.parse_args()
    args.output = args.output.resolve()
    args.reference = args.reference.resolve()
    args.output.mkdir(parents=True, exist_ok=True)
    fixture(args.output)
    bench = prepare(args.reference, args.output, args.interfaces)
    exe = build(args, bench)
    from aecp_wire_oracle import check
    reports = []
    for interface in range(args.interfaces):
        log = args.output / f"wire-if{interface}.log"
        run([str(exe), str(interface)], bench, log)
        reports.append(check(log, args.output / "aecp_entity_gen.h"))
    (args.output / "verdict.json").write_text(json.dumps(reports, indent=2) + "\n")
    print(f"wire comparison PASS: {args.interfaces} ingress paths, "
          f"{sum(r['observations'] for r in reports)} observations; six oracle controls per ingress")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
