#!/bin/sh
# R506-2: the store's whole gate (5 shapes) against a copy whose loaded-prefix guard is off by one.
# Usage: guard_ge_probe.sh <review checkout at the head> <work dir>
# A shared local clone (read-only use of the checkout's objects), its two submodules at their
# gitlinks, the one-character edit, then the unchanged gate. rc 0 means no test failed: the
# mutant survives.
set -u
S=$1; W=$2/probe_ge
git clone -q --shared --no-checkout "$S" "$W" && cd "$W" && git checkout -q --detach "$(git -C "$S" rev-parse HEAD)" || exit 2
for s in gptp-processor protocol-processor; do
  sha=$(git -C "$S" ls-tree HEAD $s | awk '{print $3}'); rmdir $s 2>/dev/null
  git clone -q --shared --no-checkout "$S/$s" $s && git -C $s checkout -q --detach "$sha" || exit 2
done
sed -i 's/if (pos + NVM_REC_HDR > loaded)/if (pos + NVM_REC_HDR >= loaded)/' sw/firmware/ctrl_nvm/nvm_klj2.c
git diff --stat
python3 -u sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --jobs 8
