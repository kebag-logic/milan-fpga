#!/bin/sh
# [R312] probe, as run: plant the old 9-entry output length into the
# firmware's backend table write ONLY, run the published D3 replay driver
# (scripts/replay_d3.published.py, sha256 d937a166...), then restore the exact
# head bytes. Run from the repository root with the pinned Verilator first on
# PATH and TMPDIR under a disposable directory. Expected: the replay fails
# (no 0x70 record reaches the journal) while test_nvm_firmware.py stays green.
set -u
F=sw/firmware/milan_baremetal/milan_baremetal.c
python3 - "$F" <<'PY'
import sys; p=sys.argv[1]; s=open(p).read()
o="unsigned int flen = REC_HDR + NVM_MAP_ENTRY * entries;"; assert s.count(o)==1
open(p,"w").write(s.replace(o,"unsigned int flen = REC_HDR + NVM_MAP_ENTRY * (dir ? 9u : entries);"))
PY
python3 "${DRIVER:?path to a copy of replay_d3.published.py}"; echo "mutant rc=$?"
git show HEAD:$F > $F && git diff --quiet -- $F && echo restored
