#!/bin/sh
# Disposable probe: remove the PR's erased-payload loaded bound from nvm_klj2.c,
# rerun the ctrl_nvm suite with RV32 required, then restore the exact head bytes.
# usage: probe_drop_erased_check.sh <clone> <log>   (MILAN_RV32_CC must be set)
set -u
cd "$1"
python3 - <<'PY'
from pathlib import Path
p = Path("sw/firmware/ctrl_nvm/nvm_klj2.c"); s = p.read_text()
old = ("\t\t/* The caller may hold only a prefix of the CRC-closed container. */\n"
       "\t\tif (pos + NVM_REC_HDR + r.plen > loaded)\n\t\t\treturn NVM_VD_REC;\n")
assert s.count(old) == 1; p.write_text(s.replace(old, ""))
PY
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 8 > "$2" 2>&1
echo "probe suite rc=$?" >> "$2"
git checkout -- sw/firmware/ctrl_nvm/nvm_klj2.c
git diff --quiet && echo "restored: clean" >> "$2"
