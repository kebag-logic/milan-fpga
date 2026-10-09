#!/usr/bin/env python3
"""R580-3 probe P11: plants on the round-3 self-test arms and the printed-record guard, per interpreter.

Usage: python3 -I -B probe_order_plants.py <repo> <scratch> <python> <jobs>
Each variant copies the five gate siblings of <repo>/syn/ooc into its own folder, applies
exact-once replacements (file, old, new), runs "<python> -B pp_resource_gate.py --selftest"
there, and prints: variant, wanted (pass|fail|either), observed rc, verdict, last diagnostic line.
"either" marks an interpreter-dependent plant whose rc is reported, not judged; "pass-shows-arm-needed"
removes a self-test arm together with the gate defect it targets and reports whether anything else detects it.
Exit 0 when every judged variant matched, 1 otherwise.
"""
import concurrent.futures
import shutil
import subprocess
import sys
from pathlib import Path

repo, scratch, python, jobs = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], int(sys.argv[4])
SIBLINGS = ("pp_resource_gate.py", "pp_baseline_rank.py", "pp_resource_gate_selftest.py",
            "pp_placement.py", "pp_placement_selftest.py")
S, G = "pp_placement_selftest.py", "pp_resource_gate.py"
OLD_ORDER_A = (S, "result = cli(command, *arguments, *options)", "result = cli(command, *options, *arguments)")
OLD_ORDER_B = (S, "cli(command, *arguments, *options), 2,", "cli(command, *options, *arguments), 2,")
JUDGED_PRINT = (G, "wrong = [] if printing else misplaced(", "wrong = misplaced(")
NO_PRINT_ARM = (S, '                expect_case(label + " printed record", cli("record", *arguments), 0, \'"kind": "route"\')\n',
                "                pass\n")
VARIANTS = {
    "control": ("pass", []),
    "old order, per-plant arm (round-2 shape)": ("either", [OLD_ORDER_A]),
    "old order, split-census arm only": ("either", [OLD_ORDER_B]),
    "old order, both arms": ("either", [OLD_ORDER_A, OLD_ORDER_B]),
    "record arm without --write": ("fail", [(S, 'judged = (("check",), ("record", "--write"))',
                                             'judged = (("check",), ("record",))')]),
    "check arm only, gate ignores record --write": ("pass-shows-arm-needed", [
        (S, 'judged = (("check",), ("record", "--write"))', 'judged = (("check",),)'),
        (G, '            if wrong:\n                raise Refusal', '            if False:\n                raise Refusal')]),
    "gate ignores record --write": ("fail", [
        (G, '            if wrong:\n                raise Refusal', '            if False:\n                raise Refusal')]),
    "gate judges a printed record": ("fail", [JUDGED_PRINT]),
    "printed-record arm removed, gate judges a printed record": ("pass-shows-arm-needed",
                                                                 [NO_PRINT_ARM, JUDGED_PRINT]),
    "printed-record arm also on wrapper absent": ("fail", [
        (S, 'if label != "wrapper absent":', "if True:")]),
    "split-census arm skips record --write": ("pass-shows-arm-needed", [
        (S, "        for command, *options in judged:\n            expect_case(\"all-fabric with a split census",
         "        for command, *options in judged[:1]:\n            expect_case(\"all-fabric with a split census"),
        (G, '            if wrong:\n                raise Refusal', '            if False:\n                raise Refusal')]),
}


def run(name: str, wanted: str, changes: list) -> tuple[str, bool]:
    folder = scratch / name.replace(" ", "_").replace(",", "").replace("(", "").replace(")", "").replace("-", "_")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    for sibling in SIBLINGS:
        shutil.copy2(repo / "syn/ooc" / sibling, folder / sibling)
    for target, old, new in changes:
        text = (folder / target).read_text()
        if text.count(old) != 1:
            return f"{name}\t{wanted}\t-\tPLANT-NOT-UNIQUE ({text.count(old)})\t{old[:60]!r}", False
        (folder / target).write_text(text.replace(old, new))
    result = subprocess.run([python, "-B", str(folder / G), "--selftest"], cwd=folder,
                            capture_output=True, text=True, timeout=900)
    tail = (result.stdout + result.stderr).strip().splitlines()
    last = next((line for line in reversed(tail) if "Error" in line or "exited through" in line), tail[-1] if tail else "")
    passed = result.returncode == 0
    if wanted == "pass":
        ok = passed
    elif wanted == "fail":
        ok = not passed
    else:
        ok = True  # informational: "either" is interpreter-dependent; "pass-shows-arm-needed" reports
        # whether the gate defect survives once the arm is removed (rc 0 = the arm is its only detector)
    verdict = ("as-expected" if ok else "UNEXPECTED") if wanted in ("pass", "fail") else \
        ("survives-without-arm" if passed else "detected-elsewhere") if wanted.startswith("pass-") else "reported"
    return f"{name}\t{wanted}\trc={result.returncode}\t{verdict}\t{last[:240]}", ok


with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
    results = list(pool.map(lambda item: run(item[0], *item[1]), VARIANTS.items()))
print("variant\twanted\tobserved\tverdict\tdiagnostic")
for line, _ in results:
    print(line)
bad = sum(not ok for _, ok in results)
print(f"interpreter {subprocess.run([python, '-V'], capture_output=True, text=True).stdout.strip()}: "
      f"{len(results)} variants, {bad} unexpected")
sys.exit(1 if bad else 0)
