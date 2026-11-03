#!/usr/bin/env python3
"""Mutation campaign over the LiteX leg split in a disposable clone.

usage: mutants.py <clone> <fixture-commit> <outdir>
Each mutant: reset the clone to the fixture (stub LiteX members), apply exact-text edits
(each old text must occur exactly once) and/or file plants, commit locally in the
disposable clone, then run concurrently: the end-to-end leg probe (e2e.sh), the runner
selftest, the LiteX legs selftest, the gate workflow selftest and the generator --check.
A mutant is KILLED when any detector is red; for mutants that change what runs, the
union and aggregate verifier must refuse with words."""
import json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
clone, fixture, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
H = Path(__file__).resolve().parent
RS, LG, GR, GW, WF = ("scripts/run_litex_sims.sh", "scripts/ci_litex_legs.py", "scripts/ci_gate_receipts.py",
                      "scripts/ci_gate_workflows.py", ".github/workflows/elaborate.yml")
TPL = ".github/ci-templates/elaborate.yml"
ROW = 'printf \'%s\\t%s\\t%s\\n\' "$t" "$verdict" "$((SECONDS - start))" >> "$out/verdicts.tsv"'
PASSER = 'import sys\nprint("RESULT: PASS")\nsys.exit(0)\n'
M = [
 ("R1 --only keeps only its first member", [(RS, 'SELECTED+=("$t"); unset', '[ "${#SELECTED[@]}" -eq 0 ] && SELECTED+=("$t"); unset')], {}),
 ("R2 --only ignored (whole inventory per leg)", [(RS, '  select_members "$ONLY" || exit 2', '  true')], {}),
 ("R3 reconciliation narrowed to the selection", [(RS, '  # Reconciliation, both directions, before anything runs.\n  for t in "${INVENTORY[@]}"; do', '  # Reconciliation, both directions, before anything runs.\n  for t in "${SELECTED[@]}"; do')], {}),
 ("R4 no verdict row for a PASS", [(RS, ROW, '[ "$verdict" = PASS ] || ' + ROW)], {}),
 ("R5 verdict row written twice", [(RS, ROW, ROW + '; ' + ROW)], {}),
 ("R6 FAIL recorded as PASS, with a failing member", [(RS, '*) verdict=FAIL ;;', '*) verdict=PASS ;;')], {"sw/litex/test_ctrl_memory.py": 'import sys\nprint("RESULT: FAIL")\nsys.exit(1)\n'}),
 ("R6b failing member, no code mutant", [], {"sw/litex/test_ctrl_memory.py": 'import sys\nprint("RESULT: FAIL")\nsys.exit(1)\n'}),
 ("R7 member file deleted", [], {"sw/litex/test_pp_mem_bridge.py": None}),
 ("R8 unlisted member file added", [], {"sw/litex/test_rogue.py": PASSER}),
 ("R9 member masks its verdict (exit 0, no RESULT: PASS)", [], {"sw/litex/test_gmii_rx_capture.py": 'print("ok")\n'}),
 ("R10 member declares a skip", [], {"sw/litex/test_pp_boot_bus_freeze.py": 'print("RESULT: SKIP no tool")\n'}),
 ("R11 member removed from INVENTORY, file kept", [(RS, '  test_pp_mem_bridge\n', '')], {}),
 ("L1 partition drops the last member", [(LG, '    return [[name for name in names if owner[name] == leg] for leg in range(legs)]', '    return [[name for name in names if owner[name] == leg and name != names[-1]] for leg in range(legs)]')], {}),
 ("L2 partition puts a member in two legs", [(LG, '    return [[name for name in names if owner[name] == leg] for leg in range(legs)]', '    out = [[name for name in names if owner[name] == leg] for leg in range(legs)]\n    out[1] = sorted(set(out[1]) | {out[0][0]}, key=names.index)\n    return out')], {}),
 ("L3 run() passes no --only", [(LG, '[*command, "--only", ",".join(legs[leg])]', '[*command]')], {}),
 ("L4 run() passes leg 0 selection to every leg", [(LG, '",".join(legs[leg])', '",".join(legs[0])')], {}),
 ("L5a union absent check removed", [(LG, '    if absent:\n', '    if False:\n')], {}),
 ("L5b union repeated check removed", [(LG, '    if repeated:\n', '    if False:\n')], {}),
 ("L6 union per-leg executed check removed", [(LG, '        if executed != legs[leg]:', '        if False:')], {}),
 ("L7 union verdict check removed", [(LG, '            if row["verdict"] != "PASS":', '            if False:')], {}),
 ("L8 union exit check removed", [(LG, '        if receipt["exit"] != 0:', '        if False:')], {}),
 ("L9 union selection check removed", [(LG, '        if receipt["selected"] != legs[leg]:', '        if False:')], {}),
 ("L10 measured seconds move a member (legitimate re-partition)", [(LG, '"test_gmii_rx_capture": 1,', '"test_gmii_rx_capture": 600,')], {}),
 ("L11 a leg over its budget", [(LG, '"test_soc_timing_cuts": 534,', '"test_soc_timing_cuts": 1300,')], {}),
 ("L12 a member unmeasured", [(LG, '    "test_pp_mem_bridge": 14,\n', '')], {}),
 ("G1 aggregate never requires the LiteX union", [(GR, '    if any(simulated):', '    if False:')], {}),
 ("G1b aggregate skips the union and its skipped-division guard", [(GR, '    if any(simulated):', '    if False:'), (GR, '    elif litex:\n        raise ValueError("LiteX leg receipts', '    elif False:\n        raise ValueError("LiteX leg receipts')], {}),
 ("G2 aggregate collects no LiteX receipts (glob typo)", [(GR, 'rglob("litex-leg-*.json")', 'rglob("litex-legs-*.json")')], {}),
 ("G3 skipped-division guard removed", [(GR, '    elif litex:\n        raise ValueError("LiteX leg receipts', '    elif False:\n        raise ValueError("LiteX leg receipts')], {}),
 ("G4 LiteX steps never counted as executed", [(GR, '                simulated.append(result == ("success", "success"))', '                simulated.append(False)')], {}),
 ("W1 generator puts two LiteX legs on one worker", [(GW, 'LITEX_WORKERS = {"elaborate": (2, 3, 4)}', 'LITEX_WORKERS = {"elaborate": (2, 3, 3)}')], {}),
 ("W2 generated workflow hand edit: worker 4 runs leg 1", [(WF, 'python3 scripts/ci_litex_legs.py run 2 ', 'python3 scripts/ci_litex_legs.py run 1 ')], {}),
 ("W3 generated workflow hand edit: worker 4 runs the whole aggregate", [(WF, 'python3 scripts/ci_litex_legs.py run 2 --receipt "$RUNNER_TEMP/gate-results/litex-leg-2.json" -- scripts/run_litex_sims.sh', 'scripts/run_litex_sims.sh')], {}),
 ("W4 template aggregate gains its own --only", [(TPL, '          scripts/run_litex_sims.sh "$RUNNER_TEMP/litex-sim-logs"\n', '          scripts/run_litex_sims.sh "$RUNNER_TEMP/litex-sim-logs" --only test_ctrl_memory\n')], {}),
 ("W5 template runs a second whole aggregate first", [(TPL, '          scripts/run_litex_sims.sh --selftest\n          scripts/run_litex_sims.sh "$RUNNER_TEMP/litex-sim-logs"\n', '          scripts/run_litex_sims.sh --selftest\n          scripts/run_litex_sims.sh "$RUNNER_TEMP/x"\n          scripts/run_litex_sims.sh "$RUNNER_TEMP/litex-sim-logs"\n')], {}),
]
def sh(cmd, cwd=clone, **kw): return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, **kw)
def tail(text): return (text.strip().splitlines() or [""])[-1][:220]
rows = []
only = set(sys.argv[4:])
for label, edits, plants in M:
    key = label.split()[0]
    if only and key not in only: continue
    sh(["git", "reset", "-q", "--hard", fixture]); sh(["git", "clean", "-qfdx", "-e", "protocol-processor", "-e", "gptp-processor", "-e", "third_party"])
    for path, old, new in edits:
        text = (clone / path).read_text()
        assert text.count(old) == 1, (label, path, text.count(old))
        (clone / path).write_text(text.replace(old, new))
    for path, body in plants.items():
        if body is None: (clone / path).unlink()
        else: (clone / path).write_text(body)
    sh(["git", "add", "-A", "sw/litex", "scripts", ".github"]); r = sh(["git", "commit", "-qm", "mutant " + key])
    d = out / key
    jobs = {"e2e": [str(H / "e2e.sh"), str(clone), str(d / "e2e")],
            "runner_selftest": ["bash", RS, "--selftest"],
            "legs_selftest": ["python3", "scripts/ci_litex_legs_selftest.py"],
            "gate_selftest": ["python3", "scripts/ci_gate_workflows_selftest.py"],
            "check": ["python3", GW, "--check"]}
    with ThreadPoolExecutor(5) as pool:
        res = dict(zip(jobs, pool.map(lambda c: sh(c, timeout=600), jobs.values())))
    d.mkdir(parents=True, exist_ok=True)
    for k, v in res.items(): (d / (k + ".log")).write_text(v.stdout + v.stderr)
    e = res["e2e"].stdout.strip()
    det = {k: res[k].returncode for k in jobs if k != "e2e"}
    row = {"mutant": label, "e2e": e, **{k: v for k, v in det.items()},
           "selftest_tails": {k: tail(res[k].stdout + res[k].stderr) for k in det if det[k] != 0}}
    rows.append(row); print(json.dumps(row), flush=True)
(out / "mutants.json").write_text(json.dumps(rows, indent=1) + "\n")
sh(["git", "reset", "-q", "--hard", fixture])
