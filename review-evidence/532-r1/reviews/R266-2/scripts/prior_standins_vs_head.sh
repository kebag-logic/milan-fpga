#!/usr/bin/env bash
# Review round R266-2: run the two refusing stand-in runners published by the
# previous round (R266-1 fake_runner_refuse_after_slot.py, R267-1
# fake_refusing_runner.py) against the reviewed head's act_slot_proof.sh.
# Offline: the head script's own stand-in `sudo` (extracted verbatim from its
# fake_sudo_source heredoc) is first on PATH, so no real sudo, Docker,
# namespace or network is ever reached. Expected: exit 1 and no PROVED line.
# Usage: prior_standins_vs_head.sh HEAD_PROOF_SCRIPT PRIOR_DIR SCRATCH
set -euo pipefail
proof=$1 prior=$2 scratch=$3
for name in r266-1_fake_runner_refuse_after_slot r267-1_fake_refusing_runner; do
  stage=$scratch/standin-$name
  rm -rf "$stage"; mkdir -p "$stage/bin" "$stage/state" "$stage/wt-a" "$stage/wt-b" "$stage/locks"
  awk '/^fake_sudo_source\(\) \{/{f=1;next} f&&/^  cat <<.EOF.$/{g=1;next} g&&/^EOF$/{exit} g' "$proof" >"$stage/bin/sudo"
  sed "s|/tmp/fake-slot-|$stage/locks/fake-slot-|" "$prior/$name.py" >"$stage/runner.py"
  chmod 0555 "$stage/bin/sudo" "$stage/runner.py"
  status=0
  FAKE_STATE=$stage/state PATH="$stage/bin:$PATH" bash "$proof" --runner "$stage/runner.py" \
    --sha256 "$(sha256sum "$stage/runner.py" | cut -d' ' -f1)" --act-bin /nonexistent/act \
    --logs "$stage/logs" --pr-a 21 --worktree-a "$stage/wt-a" --pr-b 23 --worktree-b "$stage/wt-b" \
    --slot-a 1 --slot-b 2 --poll-seconds 0.2 >"$stage/out" 2>&1 || status=$?
  proved=$(grep -c '^PROVED' "$stage/logs/SUMMARY" || true)
  echo "== $name: exit $status, PROVED lines $proved, $(grep -c '^PASS' "$stage/logs/SUMMARY" || true) PASS, $(grep -c '^FAIL' "$stage/logs/SUMMARY" || true) FAIL"
  sed 's/^/   | /' "$stage/logs/SUMMARY"
  if [ "$status" = 1 ] && [ "$proved" = 0 ]; then echo "   => refused to prove (expected)"; else echo "   => UNEXPECTED"; fi
done
