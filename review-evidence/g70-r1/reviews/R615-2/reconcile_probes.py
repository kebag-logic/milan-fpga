#!/usr/bin/env python3
"""Confirm prior public finding dispositions after the independent verdict.

Usage: python3 reconcile_probes.py --repo CLONE --packet PACKET --jobs 4
Synthesis output is synthetic; this checks shell propagation, not hardware or timing.
"""
import argparse
import concurrent.futures
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
from review_probes import LOG, RPT


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--jobs", type=int, default=4)
    a = parser.parse_args()
    assert 1 <= a.jobs <= 16
    repo, packet = a.repo.resolve(), a.packet.resolve()
    root = packet / "scratch" / "reconcile"
    receipt = packet / "receipts" / "reconcile"
    root.mkdir(parents=True, exist_ok=True)
    receipt.mkdir(parents=True, exist_ok=True)
    source = repo / "syn/ooc/check_ooc_clock.py"
    emitter = root / "emit.py"
    emitter.write_text('''import os, sys
from pathlib import Path
args = sys.argv[1:]
script = Path(args[args.index("-source") + 1])
top = script.name.removesuffix("_ooc.tcl")
log = LOG.replace("@XDC@", str(script.parent / "ooc_clock.xdc")).replace("ucpu", top)
rpt = RPT
if os.environ.get("REVIEW_BAD_TOP") == top:
    log += "CRITICAL WARNING: [Vivado 12-4739] synthetic missing clock-port result\\n"
    log = log.replace("0 Critical Warnings", "2 Critical Warnings")
    rpt = "Synthetic unclocked report\\n1. checking no_clock (" + ("1003" if top == "ucpu" else "4412") + ")\\n"
Path(top + "_ooc.log").write_text(log)
Path(top + "_timing.rpt").write_text(rpt)
Path(top + "_util.rpt").write_text("Synthetic fixture: no measurement\\n| Slice LUTs | fixture |\\n")
Path(top + "_util_hier.rpt").write_text("Synthetic fixture: no measurement\\n")
print("SYNTHETIC_OUTPUT " + top)
'''.replace('args = sys.argv[1:]', 'LOG = ' + repr(LOG) + '\nRPT = ' + repr(RPT) + '\nargs = sys.argv[1:]'))
    settings = root / "settings.sh"
    settings.write_text('vivado() { python3 "$REVIEW_EMITTER" "$@"; }\n')
    env = dict(os.environ, TMPDIR=str(root), PYTHONDONTWRITEBYTECODE="1",
               VIVADO_SETTINGS=str(settings), REVIEW_EMITTER=str(emitter))

    def run_case(top):
        name = "integration_" + (top or "clean")
        tree = root / name
        shutil.copytree(packet / "scratch/probes/base", tree, dirs_exist_ok=True)
        arm_env = dict(env, REVIEW_BAD_TOP=top)
        result = subprocess.run(["make", "-j16", "ooc"], cwd=tree, env=arm_env,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=120)
        (receipt / (name + ".log")).write_text(result.stdout)
        (receipt / (name + ".rc")).write_text(str(result.returncode) + "\n")
        reports = sorted(p.name for p in (tree / "syn/ooc/work").glob("*.rpt"))
        ok = result.returncode == (2 if top else 0) and len(reports) == 6
        if top:
            ok &= all(x in result.stdout for x in (top + "_ooc.log", top + "_timing.rpt",
                      "CRITICAL WARNING", "session ends with 2 critical warnings",
                      "Clock Summary is []", "not bound to clk_i", "checking no_clock reports"))
        return {"name": name, "rc": result.returncode, "reports": reports, "pass_expected": bool(ok)}

    with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool:
        rows = list(pool.map(run_case, ("", "ucpu", "engine")))
    # The second prior suggestion's mutant: accept an echo anywhere in the log.
    text = source.read_text()
    old = "if first(lines, LOG_READ_RE, 0, command) is None:"
    assert text.count(old) == 1
    mutant = root / "echo_anywhere.py"
    mutant.write_text(text.replace(old, "if first(lines, LOG_READ_RE) is None:"))
    result = subprocess.run([sys.executable, str(mutant), "--selftest"], env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=120)
    (receipt / "echo_anywhere.log").write_text(result.stdout)
    (receipt / "echo_anywhere.rc").write_text(str(result.returncode) + "\n")
    rows.append({"name": "echo_anywhere", "rc": result.returncode,
                 "pass_expected": result.returncode == 1 and
                 "read_xdc echoed after synth_design escaped" in result.stdout and
                 "is not read before" in result.stdout and "Traceback" not in result.stdout})

    spec = importlib.util.spec_from_file_location("checker", source)
    check = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(check)
    clean = (repo / "syn/ooc/ooc_clock.xdc").read_text()
    observed = []
    for name, extra in (("generated_clock", "create_generated_clock -name extra -source [get_ports clk_i] -divide_by 2 [get_ports clk_i]"),
                        ("timing_exception", "set_false_path -from [get_ports rst_n]")):
        xdc = root / (name + ".xdc")
        xdc.write_text(clean + extra + "\n")
        found = check.xdc_findings(xdc)
        observed.append({"name": name, "static_findings": found})
        rows.append({"name": name, "pass_expected": found == []})
    xdc = root / "bad_period.xdc"
    xdc.write_text(clean.replace("10.000", "10.0.0"))
    try:
        found = check.xdc_findings(xdc)
        observed.append({"name": "bad_period", "static_findings": found})
        rows.append({"name": "bad_period", "pass_expected": False})
    except ValueError as exc:
        observed.append({"name": "bad_period", "exception": str(exc), "type": "ValueError"})
        rows.append({"name": "bad_period", "pass_expected": True})
    (receipt / "retained_suggestion.json").write_text(json.dumps(observed, indent=2) + "\n")
    (receipt / "results.json").write_text(json.dumps(rows, indent=2) + "\n")
    for row in rows:
        print(('PASS ' if row['pass_expected'] else 'FAIL ') + row['name'])
    print(f"TOTAL {sum(r['pass_expected'] for r in rows)}/{len(rows)} expected outcomes")
    return int(not all(r['pass_expected'] for r in rows))


if __name__ == "__main__":
    sys.exit(main())
