#!/usr/bin/env bash
# [A213] Drive the stage's scripts/act_slot_proof.sh against the reviewers'
# and the original author's stand-in runners, ONLY inside a network-less
# unprivileged bubblewrap sandbox (no_new_privs: sudo can never elevate, and
# no Docker socket exists). Usage: proof-probes.sh STAGE EVIDENCE_DIR
set -euo pipefail
stage=$(cd "$1" && pwd) evidence=$(cd "$2" && pwd)
bwrap --unshare-all --die-with-parent --new-session \
  --ro-bind /usr /usr --symlink usr/lib /lib --symlink usr/lib /lib64 \
  --symlink usr/bin /bin --symlink usr/bin /sbin --ro-bind /etc /etc \
  --proc /proc --dev /dev --tmpfs /tmp --tmpfs /run --tmpfs /home --tmpfs /var \
  --ro-bind "$stage/scripts/act_slot_proof.sh" /proof/act_slot_proof.sh \
  --ro-bind "$evidence" /evidence --chdir /tmp --clearenv \
  --setenv PATH /usr/bin:/bin --setenv HOME /tmp --setenv LANG C.UTF-8 \
  bash -c '
    set -u
    run() {  # LABEL RUNNER [ENV...]
      local label=$1 source=$2; shift 2
      mkdir -p /tmp/$label/wt-a /tmp/$label/wt-b /tmp/$label/locks
      install -m 0555 "$source" /tmp/$label/runner.py
      sha=$(sha256sum /tmp/$label/runner.py | cut -d" " -f1)
      env "$@" FAKE_LOCKS=/tmp/$label/locks bash /proof/act_slot_proof.sh --runner /tmp/$label/runner.py \
        --sha256 "$sha" --act-bin /nonexistent/act --logs /tmp/$label/logs --pr-a 11 \
        --worktree-a /tmp/$label/wt-a --pr-b 22 --worktree-b /tmp/$label/wt-b \
        --slot-a 1 --slot-b 2 --poll-seconds 0.5 >/tmp/$label/out 2>&1
      echo "== $label: proof exit=$? PROVED-lines=$(grep -c "^PROVED" /tmp/$label/logs/SUMMARY)"
      sed "s/^/   /" /tmp/$label/logs/SUMMARY
    }
    rm -f /tmp/fake-slot-*.lock
    run r266-refuse-after-slot /evidence/reviews/R266-1/probes/fake_runner_refuse_after_slot.py
    run r267-refusing-runner /evidence/reviews/R267-1/proof-probe/fake_refusing_runner.py
    for mode in pass nolock parallel; do
      run a203-fake-$mode /evidence/author-a203/receipts/proof-script-dryrun/fake_runner.py FAKE_BREAK=$mode
    done'
