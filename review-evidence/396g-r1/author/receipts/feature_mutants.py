"""Plant planner defects in a scratch copy of tests/ and tb/tools/ and require
the plan feature to fail. Usage: feature_mutants.py <scratch-root>"""
import re, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1])
src = root / "tb/tools/torture_campaign.py"
pristine = src.read_text()
MUTANTS = [
    ("soak returns to seven days", "RELEASE_SOAK_DURATION_S = 24 * 60 * 60\n", "RELEASE_SOAK_DURATION_S = 7 * 24 * 60 * 60\n"),
    ("soft resets planned as cold", 'cold = phase != "soft_reset"', "cold = True"),
    ("reset phase dropped", '                         ("soft_reset", settings.reset_cycles)):', "                         ):"),
    ("cycle mix not audited", 'if len(totals) != 1 or sum(s.args.get("cycles", 0) for s in repeats) not in totals:', "if False:"),
    ("assertion audit removed", "        if owed:\n", "        if False:\n"),
    ("LATE_TIMESTAMP may grow", 'RELEASE_ZERO_GROWTH_COUNTERS = ("SEQ_NUM_MISMATCH", "STREAM_INTERRUPTED",\n                                "LATE_TIMESTAMP", "EARLY_TIMESTAMP")',
     'RELEASE_ZERO_GROWTH_COUNTERS = ("SEQ_NUM_MISMATCH", "STREAM_INTERRUPTED",\n                                "EARLY_TIMESTAMP")'),
    ("MEDIA_UNLOCKED needs no planted event", "if delta > len(matches):", "if False:"),
    ("first-boot fixture healthy", 'desk_fixture={"boot_passes": 2, "restarts": 1, "capture_complete": True},', 'desk_fixture={"boot_passes": 1, "restarts": 0, "capture_complete": True},'),
    ("persistence fixture restored", '"post": {item: "default" for item in items},', '"post": {item: "set" for item in items},'),
    ("audio drop removed", '"dut_event": {"kind": "drop", "index": 3 * AUDIO_COUNTER_MODULUS + 7, "n": n},', '"dut_event": {"kind": "drop", "index": 3 * AUDIO_COUNTER_MODULUS + 7, "n": 0},'),
    ("swap read as corruption", "if partner is not None and partner != channel:", "if False:"),
    ("missed arm accepted", 'return "NOT RUN", dict(detail, why="void: a planted arm was missed")', 'return "PASS", dict(detail, why="void: a planted arm was missed")'),
    ("capture loss counted against DUT", '            event["attribution"] = "capture"', "            pass"),
    ("inventory loses clock source", '    "clock_source": "Milan v1.2 5.3.11.1: every CLOCK_DOMAIN",\n', ""),
    ("audio integrity loses CRF sink targets", '    args = _release_args(dut, peer)\n    args["evidence"] += ["audio_captures"', '    args = _release_args(dut, peer)\n    args["counter_targets"] = [t for t in args["counter_targets"] if not t["crf"]]\n    args["evidence"] += ["audio_captures"'),
]
rc = 0
for name, old, new in MUTANTS:
    if pristine.count(old) != 1:
        print(f"ANCHOR {name}: {pristine.count(old)}"); rc = 1; continue
    src.write_text(pristine.replace(old, new))
    r = subprocess.run(["behave", "--no-capture", "-f", "plain", "features/torture_campaign_plan.feature"],
                       cwd=root / "tests", capture_output=True, text=True, timeout=600)
    summary = [l for l in r.stdout.splitlines() if "scenarios passed" in l]
    fails = re.findall(r"Failing scenarios:\n((?:  .*\n)+)", r.stdout)
    first = fails[0].strip().splitlines()[0].strip() if fails else ""
    print(f"{'KILLED' if r.returncode else 'SURVIVED'}: {name}: {summary[-1].strip() if summary else ''} | first: {first}")
    rc |= r.returncode == 0
src.write_text(pristine)
sys.exit(rc)
