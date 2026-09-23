#!/usr/bin/env python3
"""[A220] Author mutants of scripts/act_slot_proof.sh for guards no reviewer set mutated.

Each mutant is one exact substitution that must apply exactly once to a
scratch COPY of the proof script (the lane file is only read). The mutated
copy's own offline `--selftest` (stand-in runner and stand-in sudo) runs ONLY
inside a network-less, unprivileged bubblewrap sandbox, one mutant at a time.
KILLED means the self-test failed; SURVIVED means it passed.

Usage: proof-mutants-a220.py LANE_PROOF_SCRIPT SCRATCH_DIR
"""

import hashlib
import pathlib
import shutil
import subprocess
import sys

MUTANTS = [
    ("A00 control: comment only", "set -euo pipefail\n\nPROOF_LABEL",
     "set -euo pipefail\n# a220 control\n\nPROOF_LABEL"),
    ("A01 parallel comparison: completion not required",
     '  if ! complete "$1"; then\n    record FAIL "$1 did not complete its workflows: '
     '$(tr \'\\n\' \' \' <"$logs/$1.verdict")"\n  elif same_verdict',
     '  if false; then\n    record FAIL "$1 did not complete its workflows: '
     '$(tr \'\\n\' \' \' <"$logs/$1.verdict")"\n  elif same_verdict'),
    ("A02 collision holder: completion not required",
     '    && complete "collide-$slot-holder" && same_verdict', "    && same_verdict"),
    ("A03 interrupt gate: exit status ignored",
     '    --sudo --slot "$slot_a" --slot-root "$slot_root_a") >"$log" 2>&1 \\\n',
     '    --sudo --slot "$slot_a" --slot-root "$slot_root_a") >"$log" 2>&1; true \\\n'),
    ("A04 PROVED despite a FAIL record when ten checks passed",
     "  if grep -q '^FAIL' \"$logs/SUMMARY\" || [", "  if false || ["),
    ("A05 isolation target: a failed start goes unrecorded",
     '    --entrypoint python3 "$probe_image" -c "$LISTENER" >/dev/null || return 1\n',
     '    --entrypoint python3 "$probe_image" -c "$LISTENER" >/dev/null || true\n'),
    ("A06 isolation target: an unanswerable container query reads as absent",
     "    || containers=unknown\n", "    || containers=\"\"\n"),
    ("A07 slots: a non-number is accepted",
     "    case \"$number\" in ''|*[!0-9]*) echo \"slots are numbers: $number\" >&2; exit 2 ;; esac\n",
     "    true\n"),
    ("A08 interrupt gate: its slot line not required",
     "    && grep -q \"^interrupt-selftest: slot $slot_a: \" \"$log\"; then\n", "; then\n"),
    ("A09 isolation: slot-side refusal of the published port not required",
     '  if [ "$inside" = "container=refused published=refused internet=reached " ] \\\n',
     '  if [[ "$inside" == "container=refused published="*" internet=reached " ]] \\\n'),
    ("A10 isolation: slot-side refusal of the container not required",
     '  if [ "$inside" = "container=refused published=refused internet=reached " ] \\\n',
     '  if [[ "$inside" == "container="*" published=refused internet=reached " ]] \\\n'),
]

SANDBOX = [
    "bwrap", "--unshare-all", "--die-with-parent", "--new-session",
    "--ro-bind", "/usr", "/usr", "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib", "/lib64",
    "--symlink", "usr/bin", "/bin", "--symlink", "usr/bin", "/sbin", "--ro-bind", "/etc", "/etc",
    "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp", "--tmpfs", "/run", "--tmpfs", "/home",
    "--tmpfs", "/var", "--clearenv", "--setenv", "PATH", "/usr/bin:/bin", "--setenv", "HOME", "/tmp",
    "--setenv", "LANG", "C.UTF-8",
]


def main() -> int:
    """Apply each mutant to a scratch copy, run its sandboxed self-test, print one verdict line."""
    lane_script = pathlib.Path(sys.argv[1]).resolve()
    scratch = pathlib.Path(sys.argv[2]).resolve()
    original = lane_script.read_bytes()
    digest = hashlib.sha256(original).hexdigest()
    text = original.decode("utf-8")
    print(f"lane act_slot_proof.sh sha256={digest}", flush=True)
    for label, before, after in MUTANTS:
        count = text.count(before)
        if count != 1:
            print(f"{label}: NOT APPLIED (fragment occurs {count} times)", flush=True)
            continue
        work = scratch / "a220-mutant"
        shutil.rmtree(work, ignore_errors=True)
        work.mkdir(parents=True)
        (work / "act_slot_proof.sh").write_text(text.replace(before, after, 1), encoding="utf-8")
        command = SANDBOX + ["--ro-bind", str(work), "/work", "--chdir", "/work",
                             "bash", "act_slot_proof.sh", "--selftest"]
        result = subprocess.run(command, capture_output=True, text=True, timeout=600, check=False)
        failed = [line.strip() for line in result.stdout.splitlines() if line.startswith("  FAIL")]
        print(f"{label}: {'KILLED' if result.returncode else 'SURVIVED'} rc={result.returncode}", flush=True)
        for line in failed[:3]:
            print(f"    {line}", flush=True)
        shutil.rmtree(work, ignore_errors=True)
    after = hashlib.sha256(lane_script.read_bytes()).hexdigest()
    print(f"lane file after run sha256={after} {'EXACT' if after == digest else 'CHANGED'}")
    return 0 if after == digest else 2


if __name__ == "__main__":
    raise SystemExit(main())
