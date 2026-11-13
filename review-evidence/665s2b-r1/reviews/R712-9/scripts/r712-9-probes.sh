#!/bin/bash
# The reviewer's own probes of round R712-9 (#665, PR #810), at exact head 325514224bcc356a6b43843f1003c2323f09de25.
# usage: r712-9-probes.sh CLONE PACKET VERILATOR EVIDENCE
#   CLONE     a clean checkout at the head (left untouched: every build runs on a git-archive copy under PACKET/scratch)
#   PACKET    this packet's directory (receipts/ and scratch/ under it)
#   VERILATOR the pinned Verilator 5.050 launcher (verilator --version must print 5.050)
#   EVIDENCE  the author's packet directory review-evidence/665s2b-r1 of archive 8d591986
# Every step runs in the foreground; each writes its receipt under PACKET/receipts.
set -u
C=$1 P=$2 V=$3 E=$4
R=$P/receipts S=$P/scratch
mkdir -p "$R" "$S"
"$V" --version | grep -q 'Verilator 5.050' || { echo "not Verilator 5.050"; exit 2; }

# 1. The record mover's bench and its 24 plants, on a copy of the head's files.
rm -rf "$S/mini"; mkdir -p "$S/mini"
git -C "$C" archive HEAD hdl/milan/mailbox tb/verilator/mbx tb/common sw/firmware/ctrl/mbx | tar -x -C "$S/mini"
( cd "$S/mini/tb/verilator/mbx" && make -s run-dma VERILATOR="$V" VBUILD_JOBS=16 ) > "$R/run-dma-head.log" 2>&1
( cd "$S/mini/tb/verilator/mbx" && python3 -B dma_mutants.py --jobs 16 ) > "$R/dma-mutants-head.log" 2>&1

# 2. The head's bench against the mover as it was before the fix (the merge 187eeed8): must fail D11.
rm -rf "$S/old"; mkdir -p "$S/old"
git -C "$C" show 187eeed8:hdl/milan/mailbox/KL_mbx_dma.sv > "$S/old/KL_mbx_dma.sv"
( cd "$S/mini/tb/verilator/mbx" && mapfile -t FL < <(make -s print-dma-vflags VERILATOR="$V") &&
  "${FL[@]}" --Mdir "$S/old/obj" "$S/mini/hdl/milan/mailbox/KL_mbx_pkg.sv" "$S/old/KL_mbx_dma.sv" \
      "$PWD/dma_main.cpp" -o Vmbx_dma ) > "$S/old/build.log" 2>&1
timeout 300 "$S/old/obj/Vmbx_dma" > "$R/run-dma-old-rtl-new-bench.log" 2>&1

# 3. The load gate and its self-test (read-only; no bytecode written).
( cd "$C" && python3 -B -E -s tb/verilator/ctrl_service_budget/load_grade.py --check ) > "$R/load-check-head.log" 2>&1
echo "rc=$?" >> "$R/load-check-head.log"
( cd "$C" && python3 -B -E -s tb/verilator/ctrl_service_budget/load_grade.py --selftest ) > "$R/load-selftest-head.log" 2>&1
echo "rc=$?" >> "$R/load-selftest-head.log"

# 4. THE RETRY's search at the head, and on a copy with AECP_ROUND_COLD_US 186 at 8x8/2if (must fail),
#    and with CTRL_LOOP_BUILD_ONE_PASS_US 435 at 1x1/1if (headroom).
( cd "$C" && python3 -B -E -s sw/firmware/ctrl/test/ctrl_retry_search.py ) > "$R/retry-search-head.txt" 2>&1
rm -rf "$S/rs186"; mkdir -p "$S/rs186"; git -C "$C" archive HEAD sw/firmware | tar -x -C "$S/rs186"
sed -i 's/? 85u : 185u)/? 85u : 186u)/' "$S/rs186/sw/firmware/ctrl/aecp/aecp_mbx.h"
python3 -B -E -s "$S/rs186/sw/firmware/ctrl/test/ctrl_retry_search.py" > "$R/retry-search-probe-cold-186.txt" 2>&1
sed -i 's/? 85u : 186u)/? 85u : 185u)/' "$S/rs186/sw/firmware/ctrl/aecp/aecp_mbx.h"
sed -i 's/CTRL_LOOP_BUILD_ONE_PASS_US (MBX_N_IF == 1u ? 430u/CTRL_LOOP_BUILD_ONE_PASS_US (MBX_N_IF == 1u ? 435u/' \
    "$S/rs186/sw/firmware/ctrl/loop/ctrl_loop.h"
python3 -B -E -s "$S/rs186/sw/firmware/ctrl/test/ctrl_retry_search.py" > "$R/retry-search-probe-build-one-435.txt" 2>&1

# 5. The author's table derivation re-run against the head's tables, on a copy of the round's cost tallies:
#    every table must come out unchanged (the head's tables are its fixed point).
rm -rf "$S/costs-copy"; cp -r "$E/author-r30/receipts/ruling3/costs" "$S/costs-copy"
( cd /tmp && python3 -I -B "$E/author-r30/tools/tables30.py" "$C" "$S/costs-copy" ) > "$R/tables30-rerun-at-head.txt" 2>&1

# 6. The harness flash device's journal span, and a plant that restores the fixed KLJ2 span (must fail).
rm -rf "$S/flash"; mkdir -p "$S/flash"; git -C "$C" archive HEAD tb/verilator/fw_service_budget tb/common | tar -x -C "$S/flash"
F=$S/flash/tb/verilator/fw_service_budget
( cd "$F" && g++ -std=c++17 -O1 -Wall -Wextra -I. -I../../common flash_test.cpp -o "$S/flash/flash_test" ) > "$R/flash-test-build.log" 2>&1
"$S/flash/flash_test" > "$R/flash-test-head.log" 2>&1
sed -i 's/if (address_ < journal_lo_ || address_ >= journal_hi_)/if (address_ < 0xee0000 || address_ >= 0xf00000)/' "$F/flash.hpp"
( cd "$F" && g++ -std=c++17 -O1 -I. -I../../common flash_test.cpp -o "$S/flash/flash_test_plant" )
"$S/flash/flash_test_plant" > "$R/flash-test-plant-fixed-span.log" 2>&1

# 7. Both merges' conflict resolutions against an automatic re-merge.
git -C "$C" show --remerge-diff --format='%H' 187eeed8 > "$R/merge-187eeed8-remerge-diff.txt"
git -C "$C" show --remerge-diff --format='%H' 325514224b > "$R/merge-32551422-remerge-diff.txt"

# 8. The clone left at the head's bytes.
{ echo "HEAD $(git -C "$C" rev-parse HEAD) tree $(git -C "$C" rev-parse 'HEAD^{tree}')"
  echo "status-porcelain-lines $(git -C "$C" status --porcelain --untracked-files=all | wc -l)"
  git -C "$C" diff --quiet HEAD && echo "worktree==HEAD"; git -C "$C" diff --cached --quiet && echo "index==HEAD"
  git -C "$C" ls-tree -r HEAD | awk '$2=="commit"{print $3, $4}'; } > "$R/clone-integrity-after.txt"
