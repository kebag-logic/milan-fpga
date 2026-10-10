#!/usr/bin/env python3
"""Reproduce the M4 draft and its reset-time sampling defect.

Apply M4-DRAFT.patch to an initialized checkout of the stated base first.
Set VERILATOR to the pinned executable; builds use two compiler workers.
Usage: python3 reproduce_m4.py <checkout> <empty-disk-scratch>
"""
import json
import os
from pathlib import Path
import subprocess
import sys


def main():
    repo = Path(sys.argv[1]).resolve()
    work = Path(sys.argv[2]).resolve()
    work.mkdir(parents=True, exist_ok=False)
    environment = dict(os.environ, TMPDIR=str(work), VERILATOR_JOBS="2",
                       PYTHONDONTWRITEBYTECODE="1")
    source = repo / "hdl/ieee1722/maap/KL_maap.sv"
    text = source.read_text()
    anchor = "      lfsr_r       <= 16'hACE1;\n      rng_seeded_r <= 1'b0;"
    replacement = "      lfsr_r       <= enable_seed_w;\n      rng_seeded_r <= 1'b1;"
    assert text.count(anchor) == 1
    mutant = work / "reset-seed.sv"
    mutant.write_text(text.replace(anchor, replacement))
    results = []
    for name, rtl, expected in (("clean", source, 0), ("reset-seed", mutant, 1)):
        build = work / name
        with (work / f"{name}.build.log").open("w") as log:
            status = subprocess.run(
                ["make", "-j8", "-C", str(repo / "tb/verilator/maap"),
                 "integration-build", f"DP_MDIR={build}", f"MAAP_RTL={rtl}"],
                env=environment, stdout=log, stderr=subprocess.STDOUT,
                check=False).returncode
        assert status == 0, f"{name}: build failed; no defect verdict"
        with (work / f"{name}.run.log").open("w") as log:
            status = subprocess.run([str(build / "maap_integration")],
                                    cwd=build, env=environment, stdout=log,
                                    stderr=subprocess.STDOUT, check=False).returncode
        output = (work / f"{name}.run.log").read_text()
        marker = "ok" if expected == 0 else "FAIL"
        passed = status == expected and (
            f"[{marker}] M4 datapath: programmed MAC changes probe intervals" in output)
        results.append({"case": name, "build_rc": 0, "run_rc": status,
                        "expected_run_rc": expected, "passed": passed})
        print(name, "PASS" if passed else "FAIL", flush=True)
    (work / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    return 0 if all(row["passed"] for row in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
