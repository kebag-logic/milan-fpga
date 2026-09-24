#!/bin/sh
# Real-wiring probe of the CRF servo inside milan_datapath (the milan_dp aclk
# leg, gPTP plane off). A probe copy of sim_aclk.cpp reads A_MCSRV_STAT
# (0x8F8) before and after [RENDER-RC-CRF], whose two CSR PHC adjtimes of
# 65536 ns land while the servo runs under the CRF selection, and once more at
# the end of the CRF phases. Expected: [15:10] = 0 before (no false step on the
# real PHC), +2 across the two adjtimes (the real CSR adjtime is seen as a step),
# and nothing else. No product source is modified.
set -u
. "$(dirname "$0")/env.sh"
W="$PKT/scratch/aclk"
rm -rf "$W"; mkdir -p "$W"
git -C "$CLONE" archive "$HEAD_SHA" | tar -x -C "$W"
for s in protocol-processor gptp-processor third_party/verilog-axis; do
  mkdir -p "$W/$s"
  git -C "$CLONE/$s" archive "$(git -C "$CLONE" rev-parse "$HEAD_SHA:$s")" | tar -x -C "$W/$s"
  # the build derives source lists with git ls-files: give each export a
  # throwaway index of exactly the pinned bytes
  (cd "$W/$s" && git init -q && git add -A && git -c user.name=probe -c user.email=probe@invalid commit -qm pinned)
done
H="$W/tb/verilator/milan_dp/sim_aclk.cpp"
python3 - "$H" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
old = '    prove_the_recentre_is_one_shot("RENDER-RC-CRF");\n'
new = ('    { const uint32_t a = axi_read(0x8F8); printf("  R282-PROBE before RENDER-RC-CRF: MCSRV_STAT=0x%08X state=%u disc=%u\\n", a, a & 7u, (a >> 10) & 63u); }\n'
       '    prove_the_recentre_is_one_shot("RENDER-RC-CRF");\n'
       '    { const uint32_t a = axi_read(0x8F8); printf("  R282-PROBE after RENDER-RC-CRF: MCSRV_STAT=0x%08X state=%u disc=%u\\n", a, a & 7u, (a >> 10) & 63u); }\n')
assert s.count(old) == 1
s = s.replace(old, new)
old2 = '    move_the_running_feed_past_a_tick("RENDER-LIVE", false);\n    prove_the_mr_toggle_echoes_only_under_crf();\n'
new2 = ('    { const uint32_t a = axi_read(0x8F8); printf("  R282-PROBE after RING-CRF: MCSRV_STAT=0x%08X state=%u disc=%u\\n", a, a & 7u, (a >> 10) & 63u); }\n'
        + old2)
assert s.count(old2) == 1
s = s.replace(old2, new2)
open(p, "w").write(s)
print("probe applied")
PY
cd "$W/tb/verilator/milan_dp"
make VERILATOR="$VERILATOR" VERILATOR_JOBS=8 aclk-build > build_aclk.log 2>&1 || { echo "BUILD FAILED"; tail -30 build_aclk.log; exit 2; }
./obj_aclk/Vmilan_dp_aclk; echo "aclk probe exit=$?"
