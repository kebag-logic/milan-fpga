#!/bin/bash
# boundary_probes2.sh : stack-side include-path probes, judged like boundary_probes.sh (the reviewer's capture
# of the firmware steps, --without verilator, no --selftest); each plant removed and the tree verified after.
# A platform header named like a C library header the stack includes (<stdbool.h>) is placed in a directory
# the image builder (ctrl_image.py includes(): -I ctrl_nvm/plat) searches before the compiler's own headers.
P=$REVIEWS/697c-r585-6-packet; . $P/scripts/env.sh; R=$REVIEWS/r585-6-697c; cd $R
judge(){ local label=$1 tag=${1%% *}; local s=$(date +%s)
  python3 -B sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --capture $P/scratch/capture \
    --without verilator > $P/receipts/probe_$tag.log 2>&1; local rc=$?
  echo "== $label: rc=$rc ($(( $(date +%s)-s )) s)"
  grep -E '^\s+\[FAIL\]|^ctrl_boundary|REFUSED|exit [0-9]+ \(' $P/receipts/probe_$tag.log | grep -v 'exit 0 (' \
    | tail -n 4 | cut -c1-360; }
restore(){ "$@"
  if [ -z "$(git status --porcelain --untracked-files=all -- sw/firmware)" ]; then echo "   restored: clean"
  else echo "   NOT CLEAN"; git status --short; exit 1; fi; }
SHADOW='#pragma once\n#ifndef __cplusplus\n#define bool _Bool\n#define true 1\n#define false 0\n#define __bool_true_false_are_defined 1\n#endif\n'
# Q7 the shadow in sw/firmware/ctrl_nvm/plat (on the image builder's path, not on the gate's)
printf "$SHADOW" > sw/firmware/ctrl_nvm/plat/stdbool.h
judge "Q7 sw/firmware/ctrl_nvm/plat/stdbool.h shadows the C library's in the image build"
# what the image builder really compiles the stack's sources against, with the shadow in place
. $P/scripts/env.sh
python3 -B - <<'EOF' > $P/receipts/probe_Q7_image_deps.txt 2>&1
import subprocess, sys, os
from pathlib import Path
sys.path[:0] = ["sw/firmware/ctrl/test", "sw/firmware/gtest", "sw/firmware/ctrl_nvm/test"]
import ctrl_image, fw_rv32
cc = os.environ["MILAN_RV32_CC"]
fw = Path("sw/firmware").resolve()
inc = ctrl_image.includes(fw, Path("/nonexistent-gen"), Path("third_party/tsn-c-stack").resolve())
for src in ("third_party/tsn-c-stack/src/adp.c", "third_party/tsn-c-stack/src/maap.c"):
    argv = [cc, *ctrl_image.RV32_FLAGS, *ctrl_image.IMAGE_FLAGS, *fw_rv32.includes(cc), *inc, "-M", src]
    out = subprocess.run(argv, capture_output=True, text=True)
    deps = out.stdout.replace("\\\n", " ").split()
    print(src, "rc", out.returncode, "reads:", [d for d in deps if "ctrl_nvm" in d or "stdbool" in d])
EOF
cat $P/receipts/probe_Q7_image_deps.txt | cut -c1-300
restore rm -f sw/firmware/ctrl_nvm/plat/stdbool.h
# Q8 the same shadow in sw/firmware/ctrl_nvm (on the gate's fixed path), for comparison
printf "$SHADOW" > sw/firmware/ctrl_nvm/stdbool.h
judge "Q8 sw/firmware/ctrl_nvm/stdbool.h shadows the C library's (comparison)"
restore rm -f sw/firmware/ctrl_nvm/stdbool.h
judge "Q9 nothing planted after the probes (control)"
