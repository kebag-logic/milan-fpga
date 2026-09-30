#!/usr/bin/env python3
"""Scratch probe for acmp_mutants.py's per-run timeout (not part of the tree).

Arm 1 plants a real defect (the validator accepts ACMP only at cdl 44) and
makes the bench hang AFTER it has printed its tally and every failing check, so
the log alone would read as a kill. The per-run timeout must record it
SURVIVED/TIMEOUT and leave no process behind.

Arm 2 grades a golden copy under a timeout shorter than its build: BROKEN/TIMEOUT.

Usage: python3 timeout_probe.py --root TREE --output DIR [--timeout S]
"""

import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import time


def load(root: Path):
    """Import the driver from the tree under test."""
    spec = importlib.util.spec_from_file_location("acmp_mutants", root / "tb/pp_top/acmp_mutants.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def survivors(tag: str) -> list[str]:
    """Processes still alive whose working directory or command line is in a copy."""
    found = []
    for proc in Path("/proc").iterdir():
        if not proc.name.isdigit():
            continue
        try:
            cwd = str((proc / "cwd").resolve())
            cmd = (proc / "cmdline").read_bytes().replace(b"\0", b" ").decode(errors="replace")
        except OSError:
            continue
        if (tag in cwd or tag in cmd) and "timeout_probe" not in cmd:
            found.append(f"{proc.name} {cwd} {cmd}")
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=240.0)
    parser.add_argument("--golden-timeout", type=float, default=3.0)
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    am = load(args.root.resolve())
    tally = ('  printf("%d checks: %d PASS, %d FAIL\\n", checks, checks - fails, fails);\n'
             '  return fails ? 1 : 0;\n')
    hang = ('  printf("%d checks: %d PASS, %d FAIL\\n", checks, checks - fails, fails);\n'
            '  std::fflush(stdout);\n'
            '  for (;;) pause();   // PROBE: hang after the tally\n')
    main_sig = "int main(int argc, char** argv) {\n"
    edits = (
        (am.VALIDATOR, am.V1_END, am.CDL_44_ONLY),
        ("tb/rx_validator/sim_main.cpp", tally, hang),
        ("tb/rx_validator/sim_main.cpp", main_sig, "#include <unistd.h>\n" + main_sig),
    )
    checks = ("F29 BIND_RX cdl 84", "F29 PROBE_TX cdl 84")
    records = []
    t0 = time.monotonic()
    r1 = am.judge("probe-hang-after-tally@rx_validator", am.RX_VALIDATOR, edits, checks,
                  (args.root.resolve(), out, "verilator", args.timeout))
    r1["wall_s"] = round(time.monotonic() - t0, 1)
    r1["left_running"] = survivors("pp-acmp-mutant-")
    records.append(r1)
    t0 = time.monotonic()
    r2 = am.judge("probe-golden-short-timeout@pp_top", am.PP_TOP, (), (),
                  (args.root.resolve(), out, "verilator", args.golden_timeout))
    r2["wall_s"] = round(time.monotonic() - t0, 1)
    r2["left_running"] = survivors("pp-acmp-mutant-")
    records.append(r2)
    for r in records:
        print(json.dumps({k: r.get(k) for k in ("mutant", "verdict", "timeout", "completed",
                                                "missing", "build_rc", "run_rc", "wall_s",
                                                "left_running")}))
        print("   failing checks in the log:", len(r.get("failing_checks", [])))
    (out / "probe_results.json").write_text(json.dumps(records, indent=1) + "\n")
    ok = (r1["verdict"] == "SURVIVED/TIMEOUT" and r1["completed"] and not r1["missing"]
          and not r1["left_running"] and r2["verdict"] == "BROKEN/TIMEOUT"
          and not r2["left_running"])
    print("PROBE", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
