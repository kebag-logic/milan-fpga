#!/usr/bin/env python3
"""[A213] Mutation run for scripts/act_slot_proof.sh: each check of the live proof, removed.

Each mutant is one exact substitution that must apply exactly once to the
stage clone's proof script. The mutated script's own `--selftest` runs ONLY
inside a network-less, unprivileged bubblewrap sandbox. KILLED means the
self-test failed; SURVIVED means it passed. The stage bytes are restored after
every mutant and verified by SHA-256 at the end.

Usage: proof-mutants.py STAGE
"""

import hashlib
import pathlib
import subprocess
import sys

MUTANTS = [
    ("control comment", "set -euo pipefail\n\nPROOF_LABEL", "set -euo pipefail\n# a213 control\n\nPROOF_LABEL"),
    ("F3 a run that never completed counts", 'complete() {\n  local actual expected="" name\n',
     'complete() {\n  return 0\n  local actual expected="" name\n'),
    ("F3 interrupt gate graded on its exit status and PASS line only",
     "    && grep -q '^interrupt-selftest: PASS ' \"$log\" \\\n"
     "    && grep -q \"^interrupt-selftest: slot $slot_a: \" \"$log\"; then\n",
     "    && grep -q '^interrupt-selftest: PASS ' \"$log\"; then\n"),
    ("F3 no-isolation collision (slot 0) dropped", '  collide 0 "act-toolcache|already exist"\n', ""),
    ("F3 serial reference check dropped", "  reference serial-a\n", ""),
    ("F3 parallel verdict equality dropped", '  elif same_verdict "$1" "$2"; then\n', "  elif true; then\n"),
    ("F3 overlap not required",
     '    && ! ended parallel-a && ! ended parallel-b; then\n', "; then\n"),
    ("F3 a run that already ended still counts as holding its slot",
     "ended() {\n  grep -q -E", "ended() {\n  return 1\n  grep -q -E"),
    ("F3 rival may be refused after the holder left",
     '  if [ "$rival_early" -eq 1 ] && [ "$rival_status" = 2 ]', '  if [ "$rival_status" = 2 ]'),
    ("F3 rival refusal reason unchecked",
     '    && grep -q -E "$refusal" "$logs/collide-$slot-rival.log" \\\n', ""),
    ("F3 collision holder verdict unchecked",
     '    && complete "collide-$slot-holder" && same_verdict "collide-$slot-holder" serial-a; then\n',
     "; then\n"),
    ("F1 slot-side refusal not required",
     '  if [ "$inside" = "container=refused published=refused internet=reached " ] \\\n', "  if true \\\n"),
    ("F1 host-side differential dropped",
     '    && [ "$outside" = "container=reached published=reached " ]; then\n', "; then\n"),
    ("F1 published port not probed",
     '  local -a targets=("container,$target_ip,8080" "published,$target_gateway,$target_port")\n',
     '  local -a targets=("container,$target_ip,8080")\n'),
    ("F1 target absence not proved",
     '  if [ -n "$containers$networks" ]; then\n', "  if false; then\n"),
]


def main() -> int:
    """Apply, run and restore every mutant; print one verdict line each."""
    stage = pathlib.Path(sys.argv[1]).resolve()
    script = stage / "scripts/act_slot_proof.sh"
    original = script.read_bytes()
    digest = hashlib.sha256(original).hexdigest()
    text = original.decode("utf-8")
    print(f"stage act_slot_proof.sh sha256={digest}", flush=True)
    sandbox = [
        "bwrap", "--unshare-all", "--die-with-parent", "--new-session",
        "--ro-bind", "/usr", "/usr", "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib", "/lib64",
        "--symlink", "usr/bin", "/bin", "--symlink", "usr/bin", "/sbin", "--ro-bind", "/etc", "/etc",
        "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp", "--tmpfs", "/run", "--tmpfs", "/home",
        "--tmpfs", "/var", "--bind", str(stage), "/work", "--chdir", "/work", "--clearenv",
        "--setenv", "PATH", "/usr/bin:/bin", "--setenv", "HOME", "/tmp", "--setenv", "LANG", "C.UTF-8",
        "bash", "scripts/act_slot_proof.sh", "--selftest",
    ]
    try:
        for label, before, after in MUTANTS:
            count = text.count(before)
            if count != 1:
                print(f"{label}: NOT APPLIED (fragment occurs {count} times)", flush=True)
                continue
            script.write_text(text.replace(before, after, 1), encoding="utf-8")
            result = subprocess.run(sandbox, capture_output=True, text=True, timeout=600, check=False)
            failed = [line.strip() for line in result.stdout.splitlines() if line.startswith("  FAIL")]
            print(f"{label}: {'KILLED' if result.returncode else 'SURVIVED'} rc={result.returncode}", flush=True)
            for line in failed[:3]:
                print(f"    {line}", flush=True)
            script.write_bytes(original)
    finally:
        script.write_bytes(original)
    restored = hashlib.sha256(script.read_bytes()).hexdigest()
    print(f"restored sha256={restored} {'EXACT' if restored == digest else 'MISMATCH'}")
    return 0 if restored == digest else 2


if __name__ == "__main__":
    raise SystemExit(main())
