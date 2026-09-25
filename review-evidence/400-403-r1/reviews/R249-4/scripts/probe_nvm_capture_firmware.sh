#!/usr/bin/env bash
# Probe: with only milan_baremetal.c replaced by the train parent's bytes, does
# check_nvm_capture.py pass? Restores the candidate bytes afterwards.
set -u
F=sw/firmware/milan_baremetal/milan_baremetal.c
TRAIN=551e4b5dfa8ac7ec68a3161c95d4000eb6337396
saved=$(mktemp); cp -p "$F" "$saved"
git show "$TRAIN:$F" > "$F"
echo "probe firmware sha256: $(sha256sum "$F" | cut -d' ' -f1)"
python3 scripts/check_nvm_capture.py; rc=$?
cp -p "$saved" "$F"; rm -f "$saved"
echo "probe check_nvm_capture exit=$rc"
echo "restored sha256: $(sha256sum "$F" | cut -d' ' -f1) blob-match: $( [ "$(git hash-object "$F")" = "$(git rev-parse HEAD:$F)" ] && echo yes || echo NO)"
exit $rc
