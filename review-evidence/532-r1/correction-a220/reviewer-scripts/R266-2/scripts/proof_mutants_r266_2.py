#!/usr/bin/env python3
"""Independent mutants of scripts/act_slot_proof.sh's checks (review round R266-2).

Each mutant is one exact substitution that must apply exactly once to a
scratch COPY of the proof script; the copy's offline `--selftest` (stand-in
runner and stand-in sudo, no Docker, privilege or network) is run once per
mutant, sequentially. KILLED = the self-test failed; SURVIVED = it passed.
The reviewed file is never modified.

Usage: proof_mutants_r266_2.py REVIEWED_PROOF_SCRIPT SCRATCH_DIR
"""
import hashlib
import os
import pathlib
import shutil
import subprocess
import sys

MUTANTS = [
    ("control: comment only", "set -euo pipefail\n", "# r266-2 control\nset -euo pipefail\n"),
    ("M1 isolation: slot-side internet reachability not required",
     '  if [ "$inside" = "container=refused published=refused internet=reached " ] \\\n',
     '  if [[ "$inside" == "container=refused published=refused "* ]] \\\n'),
    ("M2 slot-0 collision: refusal reason unchecked",
     '  collide 0 "act-toolcache|already exist"\n', '  collide 0 "."\n'),
    ("M3 runner digest unchecked",
     '  if [ "$actual" != "$sha" ] || [ -n "$(find', '  if [ -n "$(find'),
    ("M4 runner write bits unchecked",
     ' || [ -n "$(find "$runner" -maxdepth 0 -perm /0222)" ] \\\n', ' \\\n'),
    ("M5 non-empty log directory accepted",
     '  if [ -n "$(ls -A "$logs")" ]; then\n', '  if false; then\n'),
    ("M6 ended ignores a refusal",
     "(PASS|FAILED)|REFUSED)' \"$logs/$1.log\"", "(PASS|FAILED))' \"$logs/$1.log\""),
    ("M7 collision: rival exit status unchecked",
     '[ "$rival_status" = 2 ] \\\n', 'true \\\n'),
    ("M8 isolated holder marker is the workflow start, not the slot",
     '  if [ "$slot" -ne 0 ]; then marker="act-ci: slot $slot: own daemon"; fi\n', ''),
    ("M9 PASS-count guard dropped",
     ' || [ "$(grep -c \'^PASS\' "$logs/SUMMARY")" -ne 10 ]; then\n', '; then\n'),
    ("M10 slot-A collision: refusal reason unchecked",
     '  collide "$slot_a" "is in use by another runner invocation"\n', '  collide "$slot_a" "."\n'),
    ("M11 isolation: host-side reach of the published port not required",
     '  && [ "$outside" = "container=reached published=reached " ]; then\n',
     '  && [[ "$outside" == "container=reached "* ]]; then\n'),
]


def main() -> int:
    reviewed = pathlib.Path(sys.argv[1]).resolve()
    scratch = pathlib.Path(sys.argv[2]).resolve()
    original = reviewed.read_bytes()
    digest = hashlib.sha256(original).hexdigest()
    print(f"reviewed act_slot_proof.sh sha256={digest}")
    text = original.decode("utf-8")
    for label, before, after in MUTANTS:
        if text.count(before) != 1:
            print(f"{label}: NOT-APPLICABLE count={text.count(before)}")
            continue
        work = scratch / "mutant"
        shutil.rmtree(work, ignore_errors=True)
        (work / "tmp").mkdir(parents=True)
        copy = work / "act_slot_proof.sh"
        copy.write_text(text.replace(before, after, 1), encoding="utf-8")
        env = {**os.environ, "TMPDIR": str(work / "tmp")}
        result = subprocess.run(
            ["bash", str(copy), "--selftest"], capture_output=True, text=True,
            env=env, timeout=900, check=False,
        )
        verdict = "SURVIVED" if result.returncode == 0 else "KILLED"
        print(f"{label}: {verdict} rc={result.returncode}")
        for line in result.stdout.splitlines():
            if line.startswith("  FAIL"):
                print(f"    {line.strip()}")
        shutil.rmtree(work, ignore_errors=True)
    after_digest = hashlib.sha256(reviewed.read_bytes()).hexdigest()
    print(f"reviewed file after run sha256={after_digest} {'EXACT' if after_digest == digest else 'CHANGED'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
