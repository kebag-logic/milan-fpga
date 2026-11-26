#!/usr/bin/env python3
"""Disposable fault probes against a probe copy of the head; each probe edits one file, regenerates the
workflows, runs the guarding gates, and restores the exact bytes. Usage: probes.py <probe-checkout> <out-dir>"""
import subprocess
import sys
from pathlib import Path

probe, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)

PROBES = [
    ("P1-campaign-count-exceeds-matrix", "scripts/ci_fast_legs.py",
     "' --campaign-shard \"${{ matrix.leg }}\" ' + str(count) + \"\\n\"",
     "' --campaign-shard \"${{ matrix.leg }}\" ' + str(count + 1) + \"\\n\""),
    ("P2-unit-phase-on-absent-leg", "scripts/ci_fast_legs.py",
     '"Hold the firmware coverage ratchet": 2,', '"Hold the firmware coverage ratchet": 3,'),
    ("P3-census-selection-drops-groups", "sw/mailbox/census_legs.py",
     "every[leg - 1::LEGS - 1]", "every[leg - 1::LEGS]"),
    ("P4-census-union-skips-rule-judge", "sw/mailbox/census_legs.py",
     "return int(bool(checks.mutations(judged,", "return 0 and int(bool(checks.mutations(judged,"),
    ("P5-aggregate-drops-legs-result", "scripts/ci_fast_legs.py",
     "    require_child(workflow, \"publication-census\", child)\n", "    pass\n"),
    ("P6-main-skips-campaign-mapping", "sw/firmware/ctrl/test/test_ctrl_firmware.py",
     "        args.mutation_shard = args.campaign_shard\n", "        pass\n"),
    ("P7-srp-8x8-table-unsliced", "sw/firmware/ctrl/test/test_ctrl_firmware.py",
     "srp_early_mutants.PREFIX, srp_link_mutants.PREFIX)))[share]",
     "srp_early_mutants.PREFIX, srp_link_mutants.PREFIX)))"),
    ("P8-census-legs-cache-may-miss", "scripts/ci_gate_workflows.py",
     "        shared[\"steps\"][where:where + 2] = [copy.deepcopy(restore)]\n",
     "        shared[\"steps\"][where:where + 2] = [{**copy.deepcopy(restore), \"with\": {k: v for k, v in "
     "restore[\"with\"].items() if k != \"fail-on-cache-miss\"}}]\n"),
]
GATES = [
    ("gate_workflows_check", ["python3", "scripts/ci_gate_workflows.py", "--check"]),
    ("events_check", ["python3", "scripts/ci_events.py", "--check"]),
    ("gate_workflows_selftest", ["python3", "scripts/ci_gate_workflows_selftest.py"]),
    ("ctrl_firmware_shards", ["python3", "sw/firmware/ctrl/test/test_ctrl_firmware_shards.py"]),
]
WORKFLOWS = [probe / ".github/workflows" / n for n in ("rtl-fast.yml", "docs.yml")]
summary = []
for name, rel, old, new in PROBES:
    path = probe / rel
    original = path.read_bytes()
    saved = {w: w.read_bytes() for w in WORKFLOWS}
    text = original.decode()
    assert text.count(old) == 1, (name, text.count(old))
    try:
        path.write_text(text.replace(old, new))
        regen = subprocess.run(["python3", "scripts/ci_gate_workflows.py"], cwd=probe, capture_output=True, text=True)
        log = [f"# probe {name}: {rel}\n# regenerate rc={regen.returncode}\n{regen.stdout}{regen.stderr}"]
        caught = []
        for gate, cmd in GATES:
            r = subprocess.run(cmd, cwd=probe, capture_output=True, text=True)
            log.append(f"## {gate} rc={r.returncode}\n{r.stdout[-4000:]}{r.stderr[-4000:]}")
            if r.returncode != 0:
                caught.append(gate)
        (out / (name + ".log")).write_text("\n".join(log))
        summary.append(f"{name}: regen rc={regen.returncode}; failing gates: {', '.join(caught) or 'NONE (escaped)'}")
    finally:
        path.write_bytes(original)
        for w, b in saved.items():
            w.write_bytes(b)
(out / "summary").write_text("\n".join(summary) + "\n")
print("\n".join(summary))
