#!/usr/bin/env python3
"""Reviewer probe (round R267-2, PR #533): candidate negative controls for the
proof guards that scripts/proof_mutants.py found uncontrolled.

On a private copy of scripts/act_slot_proof.sh it adds four stand-in faults
and four self-test cases:

  pass-then-refuse      every run prints a PASS for each workflow, then is
                        refused (exit 2), as a slot teardown, memory-cap or
                        moved-head refusal after the workflows would be;
  failed-refused        PR B's FAILED run exits 2 instead of 1;
  slot-dead             the probe from inside a slot reaches nothing, not
                        even the public name (a dead uplink);
  rival0-other-refusal  the slot-0 rival is refused for an unrelated reason.

It then runs the copy's --selftest four ways: with the head's checks (every
case, old and new, must pass), and with each of mutants P01, P02, P03 and
P04 applied on top (the matching new case must fail, killing the mutant).
Everything runs in a network-less user namespace; the tracked script is never
modified.

usage: proof_controls.py CLONE SCRATCH
"""
import pathlib
import shutil
import subprocess
import sys

ADDITIONS = [
    ("        print(f\"act-ci: {name}: PASS at {'a' * 40}\", flush=True)\nfinally:",
     "        print(f\"act-ci: {name}: PASS at {'a' * 40}\", flush=True)\n"
     "    if \"pass-then-refuse\" in faults:\n"
     "        print(\"act-ci: REFUSED: replay slot teardown failed\", file=sys.stderr)\n"
     "        sys.exit(2)\nfinally:"),
    ("            print(f\"act-ci: {name}: FAILED (1)\", file=sys.stderr, flush=True)\n"
     "            sys.exit(1)",
     "            print(f\"act-ci: {name}: FAILED (1)\", file=sys.stderr, flush=True)\n"
     "            sys.exit(2 if \"failed-refused\" in faults else 1)"),
    ("if pr == \"23\" and slot == \"1\" and \"rival-other-refusal\" in faults:",
     "if pr == \"23\" and slot == \"0\" and \"rival0-other-refusal\" in faults and run_number == 2:\n"
     "    print(\"act-ci: REFUSED: action clone failed\", file=sys.stderr)\n"
     "    sys.exit(2)\n"
     "if pr == \"23\" and slot == \"1\" and \"rival-other-refusal\" in faults:"),
    ("            reached = host == \"github.com\" and port == \"443\"",
     "            reached = host == \"github.com\" and port == \"443\" "
     "and not (inside and \"slot-dead\" in faults)"),
    ("the parallel runs never overlap|serialize|23|1|FAIL overlap\n",
     "the parallel runs never overlap|serialize|23|1|FAIL overlap\n"
     "a run passes every workflow and is then refused|pass-then-refuse|23|1|FAIL serial-a did not complete\n"
     "a run fails a workflow and is then refused|failed-refused|22|1|FAIL serial-b did not complete\n"
     "a slot whose uplink is dead|slot-dead|23|1|FAIL isolation slot 1\n"
     "the slot-0 rival is refused for another reason|rival0-other-refusal|23|1|FAIL collision slot 0\n"),
]

MUTANTS = {
    "P01": ('[ "$inside" = "container=refused published=refused internet=reached " ]',
            '[[ "$inside" == "container=refused published=refused "* ]]'),
    "P02": ('collide 0 "act-toolcache|already exist"', 'collide 0 "REFUSED"'),
    "P03": ('[ "$actual" = "exit 0$expected" ]', '[ "${actual#exit ?}" = "$expected" ]'),
    "P04": ('if [ "$actual" = "exit 1$expected"$\'\\n\'"$name FAILED" ]; then return 0; fi',
            'if [ "${actual#exit ?}" = "$expected"$\'\\n\'"$name FAILED" ]; then return 0; fi'),
}


def apply(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise SystemExit(f"anchor matches {text.count(old)} times: {old[:60]!r}")
    return text.replace(old, new, 1)


def run(label: str, text: str, scratch: pathlib.Path) -> None:
    workdir = scratch / "proof-controls" / label
    if workdir.exists():
        shutil.rmtree(workdir)
    (workdir / "tmp").mkdir(parents=True)
    script = workdir / "act_slot_proof.sh"
    script.write_text(text, encoding="utf-8")
    result = subprocess.run(
        ["unshare", "--user", "--map-current-user", "--net", "--", "bash", str(script), "--selftest"],
        env={"PATH": "/usr/bin:/bin", "TMPDIR": str(workdir / "tmp"), "LC_ALL": "C.UTF-8"},
        capture_output=True, text=True, timeout=900)
    print(f"== {label}: selftest rc {result.returncode}", flush=True)
    for line in result.stdout.splitlines():
        if line.startswith("  FAIL") or line.startswith("act_slot_proof selftest"):
            print(f"   {line.strip()}", flush=True)
        elif any(tag in line for tag in ("then refused", "uplink is dead", "slot-0 rival")):
            print(f"   {line.strip()}", flush=True)


def main() -> int:
    clone = pathlib.Path(sys.argv[1]).resolve()
    scratch = pathlib.Path(sys.argv[2]).resolve()
    text = (clone / "scripts" / "act_slot_proof.sh").read_text(encoding="utf-8")
    for old, new in ADDITIONS:
        text = apply(text, old, new)
    run("head-checks-with-new-controls", text, scratch)
    for name, (old, new) in MUTANTS.items():
        run(f"{name}-with-new-controls", apply(text, old, new), scratch)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
