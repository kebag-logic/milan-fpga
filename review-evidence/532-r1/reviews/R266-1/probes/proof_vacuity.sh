#!/usr/bin/env bash
# R266-1: drive the candidate scripts/act_slot_proof.sh against a fake runner
# whose every PR run refuses after taking its slot. Runs inside a disposable
# network-less rootless container as uid 1000.
set -euo pipefail
tree=$(realpath "$1") probes=$(realpath "$2")
timeout -k 10 300 podman run --rm --network none --user 1000:1000 \
  -v "$tree/scripts/act_slot_proof.sh:/proof/act_slot_proof.sh:ro" \
  -v "$probes/fake_runner_refuse_after_slot.py:/proof/runner.py:ro" \
  -v /usr/bin/cmp:/usr/local/bin/cmp:ro \
  localhost/milan-fpga-dev:latest bash -c '
    set -u; mkdir -p /tmp/wt-a /tmp/wt-b
    sha=$(sha256sum /proof/runner.py | cut -d" " -f1)
    bash /proof/act_slot_proof.sh --runner /proof/runner.py --sha256 "$sha" \
      --act-bin /usr/bin/true --logs /tmp/logs --pr-a 11 --worktree-a /tmp/wt-a \
      --pr-b 22 --worktree-b /tmp/wt-b --slot-a 1 --slot-b 2
    echo "proof exit=$?"
    for f in /tmp/logs/*.verdict; do printf "%s: %s\n" "${f##*/}" "$(tr "\n" " " <"$f")"; done'
