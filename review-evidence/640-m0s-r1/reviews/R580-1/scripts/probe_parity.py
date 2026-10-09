#!/usr/bin/env python3
"""Compare the base and head measurement tooling on the legacy (all-fabric and standalone) paths.

Usage: probe_parity.py <repo> <base-commit> <scratch>
1. Recipe: build one synthetic AX7101 export, run base and head pp_baseline.py with each
   legacy option set in the same directory, and require byte-identical outputs.
2. Gate: run base and head pp_resource_gate.py check-baseline on the real record, record on
   legacy fixtures, and --fuzz with a fixed seed; require identical output after replacing
   the private temporary directory names.
3. Gate self-test: require head's legacy self-test lines to equal base's, line for line.
Prints one row per comparison and exits 0 when the probe ran.
"""

import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

repo, base_commit, scratch = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
shutil.rmtree(scratch, ignore_errors=True)
trees = {"base": scratch / "base", "head": scratch / "head"}
for name, tree in trees.items():
    (tree / "syn/ooc").mkdir(parents=True)
    (tree / "docs/design").mkdir(parents=True)
    for path in sorted((repo / "syn/ooc").iterdir()):
        if path.suffix not in (".py", ".json"):
            continue
        if name == "head":
            shutil.copy2(path, tree / "syn/ooc" / path.name)
    if name == "base":
        listing = subprocess.run(["git", "-C", str(repo), "ls-tree", "--name-only", base_commit, "syn/ooc/"],
                                 check=True, capture_output=True, text=True).stdout.split()
        for entry in listing:
            if entry.endswith((".py", ".json")):
                data = subprocess.run(["git", "-C", str(repo), "show", f"{base_commit}:{entry}"],
                                      check=True, capture_output=True).stdout
                (tree / entry).write_bytes(data)
    for page in ("docs/design/AREA_BUDGET.md",):
        data = subprocess.run(["git", "-C", str(repo), "show", f"{'HEAD' if name == 'head' else base_commit}:{page}"],
                              check=True, capture_output=True).stdout
        (tree / page).write_bytes(data)
rows = []


def export(gateware: Path, clock: bool) -> tuple[Path, Path]:
    """The pp_baseline self-test's synthetic export, plus an optional bound CLK_HZ_P."""
    shutil.rmtree(gateware.parent, ignore_errors=True)
    gateware.mkdir(parents=True)
    declarations, reads = [], []
    for parameter, package, depth, width in (
            ("PP_TROM_HEX_P", "pp_acmp_pkg.sv", "TROM_DEPTH_C", "TROM_W_C"),
            ("PP_UCODE_HEX_P", "ucpu_pkg.sv", "UPC_W_C", "UCODE_W_C"),
            ("GPTP_UCODE_HEX_P", "gptp_ucpu_pkg.sv", "UPC_W_C", "UCODE_W_C")):
        path = gateware / package
        path.write_text(f"parameter {depth} = {'2' if depth == 'TROM_DEPTH_C' else '1'};\nparameter {width} = 32;\n")
        rom = gateware / f"{parameter}.hex"
        rom.write_text("12345678\nabcdef01\n")
        declarations.append(f'.{parameter}("{rom}")')
        reads.append(f"read_verilog {{{path}}}\n")
    wrapper = gateware / "KL_pp_shadow.sv"
    wrapper.write_text("parameter int unsigned N_STREAM_IN_P = 2,\n"
                       + ("parameter int unsigned CLK_HZ_P = 100_000_000,\n" if clock else ""))
    reads.append(f"read_verilog {{{wrapper}}}\n")
    verilog = "\n".join(declarations) + "\n"
    for name, words in (("rom", 2), ("sram", 4)):
        verilog += f'// Memory {name}: {words}-words x 32-bit\n$readmemh("alinx_ax7101_{name}.init", mem);\n'
        (gateware / f"alinx_ax7101_{name}.init").write_text("12345678\nabcdef01\n" if name == "rom" else "")
    (gateware / "alinx_ax7101.v").write_text(verilog)
    (gateware / "alinx_ax7101.tcl").write_text(
        "".join(reads) + "# Add constraints\nsynth_design -top alinx_ax7101 -part xc7a100t-fgg484-2\n"
        "# Add pre-optimize commands\nopt_design\n# Bitstream generation\nwrite_bitstream\n")
    log = gateware / "synthesis.log"
    log.write_text("INFO: synthesizing module 'KL_pp_shadow' [wrapper.sv:1]\n"
                   "Parameter N_STREAM_IN_P bound to: 2 - type: integer\n"
                   + ("Parameter CLK_HZ_P bound to: 32'b10111110101111000010000000\n" if clock else "")
                   + "INFO: end\n")
    return gateware, log


def snapshot(root: Path) -> dict[str, bytes]:
    return {str(path.relative_to(root)): path.read_bytes() for path in sorted(root.rglob("*")) if path.is_file()}


variants = [("integrated route", [], False), ("synthesis-only", ["--synthesis-only"], False),
            ("attribution-only", ["--attribution-only"], False),
            ("single-thread", ["--single-thread-synthesis"], False),
            ("standalone", ["@ooc", "@log"], False),
            ("standalone single-thread", ["@ooc", "@log", "--single-thread-synthesis"], False),
            ("standalone integrated clock", ["@ooc", "@log", "--integrated-clock"], True)]
work = scratch / "export"
for label, options, clock in variants:
    results = {}
    for name in ("base", "head"):
        for explicit in ((False, True) if name == "head" else (False,)):
            gateware, log = export(work / "gateware", clock)
            args = [str(gateware)]
            for option in options:
                args += {"@ooc": ["--output", str(work / "ooc")], "@log": ["--integrated-log", str(log)]}.get(
                    option, [option])
            if explicit:
                args += ["--placement", "all-fabric"]
            result = subprocess.run([sys.executable, "-I", "-B", str(trees[name] / "syn/ooc/pp_baseline.py"), *args],
                                    capture_output=True, text=True, timeout=60)
            results[(name, explicit)] = (result.returncode, result.stdout, snapshot(work))
    base = results[("base", False)]
    for key in (("head", False), ("head", True)):
        same = results[key] == base
        rows.append(f"recipe\t{label}{' --placement all-fabric' if key[1] else ''}\trc {base[0]}/{results[key][0]}"
                    f"\t{len(base[2])} files\t{'IDENTICAL' if same else 'DIFFERENT'}")


def gate(name: str, *args: str) -> tuple[int, str]:
    result = subprocess.run([sys.executable, "-E", "-s", "-B", str(trees[name] / "syn/ooc/pp_resource_gate.py"), *args],
                            capture_output=True, text=True, timeout=600, cwd=scratch)
    text = re.sub(r"/[^\s'\"]*?/(pp-[a-z-]+?)[a-z0-9_]{6,}", r"<TMP>/\1", result.stdout + result.stderr)
    return result.returncode, text


baseline = repo / "syn/ooc/pp_resource_baseline.json"
budget = repo / "docs/design/AREA_BUDGET.md"
sys.path.insert(0, str(trees["base"] / "syn/ooc"))
from pp_resource_gate_selftest import fixture  # noqa: E402  (base copy, unchanged file)
fixtures = {kind: fixture(scratch / f"fixture-{kind}", kind) for kind in ("route", "ooc")}
comparisons = [("check-baseline real record", ["check-baseline", "--baseline", str(baseline), "--budget", str(budget)]),
               ("record legacy route fixture", ["record", str(fixtures["route"]), "--endpoint", "route-1x1"]),
               ("record legacy ooc fixture", ["record", str(fixtures["ooc"]), "--endpoint", "ooc-1x1"]),
               ("check legacy route fixture vs real record",
                ["check", str(fixtures["route"]), "--endpoint", "route-1x1", "--baseline", str(baseline)]),
               ("fuzz 3000 seed 234", ["--fuzz", "3000", "--seed", "234"])]
for label, args in comparisons:
    base_result, head_result = gate("base", *args), gate("head", *args)
    rows.append(f"gate\t{label}\trc {base_result[0]}/{head_result[0]}\t{len(base_result[1])} bytes"
                f"\t{'IDENTICAL' if base_result == head_result else 'DIFFERENT'}")
base_lines = gate("base", "--selftest")
head_lines = gate("head", "--selftest")
legacy = base_lines[1].splitlines()
head = head_lines[1].splitlines()
prefix = head[:len(legacy)] == legacy
extra = head[len(legacy):]
rows.append(f"gate\tlegacy self-test lines\trc {base_lines[0]}/{head_lines[0]}\t{len(legacy)} base lines, "
            f"{len(extra)} head-only lines\t{'IDENTICAL PREFIX' if prefix else 'DIFFERENT'}")
(scratch / "selftest_head_only.txt").write_text("\n".join(extra) + "\n")
print("area\tcomparison\trc base/head\tsize\tresult")
for row in rows:
    print(row)
