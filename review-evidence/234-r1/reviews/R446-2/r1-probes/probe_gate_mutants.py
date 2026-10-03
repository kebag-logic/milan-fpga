#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe: enforcement removals NOT in pp_resource_gate_mutants.py.

Each mutant edits one enforcement point of syn/ooc/pp_resource_gate.py in a
disposable copy and runs that copy's --selftest (the 51-arm self-test the
hosted rtl-fast step runs). KILLED = the self-test fails (good); SURVIVED =
the self-test still passes with that check disabled.

Usage: probe_gate_mutants.py <checkout> [--jobs N]
"""

import concurrent.futures
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(sys.argv[1]).resolve() / "syn/ooc"
JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 8

MUTANTS = {
    "identity: design header dropped": ('"design": header(report, "Design"), ', ""),
    "identity: design state dropped": ('"state": header(report, "Design State"),', ""),
    "identity: FLOW drops synth_design": ("|synth_design|", "|"),
    "identity: FLOW drops opt_design": ("|opt_design|", "|"),
    "identity: FLOW drops route_design": ("|route_design", "|xroute_design"),
    "identity: FLOW drops phys_opt_design": ("|phys_opt_design|", "|"),
    "identity: FLOW drops create_project": ("^(create_project|", "^("),
    "identity: FLOW drops kl_timing_grade_configure": ("|kl_timing_grade_configure)", ")"),
    "header uniqueness": ("    if len(hits) != 1:\n", "    if not hits:\n"),
    "located(): one top and one wrapper": (
        "    if len(generated) != 1 or len(repository) != 1:\n", "    if not generated or not repository:\n"),
    "read source presence check": ("        if not path.is_file():\n", "        if False:\n"),
    "include directory presence check": ("            if not folder.is_dir():\n", "            if False:\n"),
    "timing floor boundary (< to <=)": ("        if after < floor:\n", "        if after <= floor:\n"),
    "timing fall boundary (> to >=)": ("        if before - after > tolerance:\n",
                                       "        if before - after >= tolerance:\n"),
    "GATED ooc drops RAMB36": ('"ooc": ("LUT", "FF", "RAMB36", "RAMB18", "DSP")', '"ooc": ("LUT", "FF", "RAMB18", "DSP")'),
    "GATED ooc drops DSP": ('"ooc": ("LUT", "FF", "RAMB36", "RAMB18", "DSP")', '"ooc": ("LUT", "FF", "RAMB36", "RAMB18")'),
    "GATED route drops WHS_ns": ('"DSP", "WNS_ns", "WHS_ns"),', '"DSP", "WNS_ns"),'),
    "count format accepts any decimal": ('r"\\d+(\\.5)?"', 'r"\\d+(\\.\\d+)?"'),
    "check_baseline: recorded figure below floor": (
        "                problems.append(f\"{name}: the recorded {figure} is below its floor\")\n",
        "                pass\n"),
    "identical-input refusal compares LUT only": (
        'candidate["figures"] != base["figures"]:\n', 'candidate["figures"]["LUT"] != base["figures"]["LUT"]:\n'),
    "generated-file root normalization dropped": ('                text = text.replace(root, f"$ROOT{index}")\n',
                                                 "                pass\n"),
    "generic path normalization dropped": ("re.sub(r'\"[^\"]*/([^/\"]+)\"', r'\"\\1\"', generic)", "generic"),
    "CARRY4 census attribution": ('            carry[""] += 1\n', "            pass\n"),
}


def run(name, change):
    source = (ROOT / "pp_resource_gate.py").read_text()
    with tempfile.TemporaryDirectory(prefix="r446-mut-") as tmp:
        folder = Path(tmp)
        for sibling in ("pp_baseline_rank.py", "pp_resource_gate_selftest.py"):
            shutil.copy2(ROOT / sibling, folder / sibling)
        if change is not None:
            old, new = change
            if source.count(old) != 1:
                return name, "NOT-APPLIED", f"pattern occurs {source.count(old)} times"
            source = source.replace(old, new)
        (folder / "pp_resource_gate.py").write_text(source)
        r = subprocess.run([sys.executable, "-B", str(folder / "pp_resource_gate.py"), "--selftest"],
                           capture_output=True, text=True, timeout=300)
        last = (r.stdout + r.stderr).strip().splitlines()
        reason = next((l for l in last if "AssertionError" in l or "Error" in l), last[-1] if last else "")
        return name, ("CONTROL-PASS" if change is None and r.returncode == 0 else
                      "CONTROL-FAIL" if change is None else
                      "KILLED" if r.returncode != 0 else "SURVIVED"), reason.strip()[:140]


def main():
    jobs = [("control", None), *MUTANTS.items()]
    with concurrent.futures.ThreadPoolExecutor(max_workers=JOBS) as pool:
        results = list(pool.map(lambda job: run(*job), jobs))
    for name, verdict, reason in results:
        print(f"{verdict:<12} {name:<48} | {reason}")
    survived = [n for n, v, _ in results if v == "SURVIVED"]
    print(f"probe_gate_mutants: {len(MUTANTS)} mutants, {len(survived)} survived, "
          f"{sum(v == 'KILLED' for _, v, _ in results)} killed, control "
          f"{results[0][1]}, not applied {sum(v == 'NOT-APPLIED' for _, v, _ in results)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
