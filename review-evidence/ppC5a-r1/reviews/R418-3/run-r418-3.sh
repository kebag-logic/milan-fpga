#!/bin/sh
# R418-3 reproduction of the executed evidence (PR #140 at ee0e2b72).
# Every build and simulation runs in a git-archive export under $SCRATCH;
# the reviewed clone is only read. Run each step in the foreground.
#   REPO     the reviewed clone at ee0e2b72ea10c83f983ec9e35878fb0193223ccb
#   PACKET   this packet directory (scripts and receipts/)
#   VERILATOR a Verilator 5.050 executable
set -eu
REPO=${REPO:?clone path}
PACKET=${PACKET:?packet path}
VERILATOR=${VERILATOR:?verilator 5.050}
SCRATCH=$PACKET/scratch
RC=$PACKET/receipts
HEAD=ee0e2b72ea10c83f983ec9e35878fb0193223ccb
mkdir -p "$SCRATCH/bin" "$SCRATCH/tmp" "$RC"
ln -sf "$VERILATOR" "$SCRATCH/bin/verilator"
export PATH="$SCRATCH/bin:$PATH" TMPDIR="$SCRATCH/tmp"
"$VERILATOR" --version > "$RC/verilator_identity.txt"

# 1. merge integrity (static, from the clone's objects)
python3 "$PACKET/both_sides_kept.py" "$REPO" 0451d83 44a6bb9 3f3ea56 97fe22f > "$RC/merge3_both_sides.txt"
python3 "$PACKET/both_sides_kept.py" "$REPO" 3f3ea56 d4ca85c 16ea10a "$HEAD" > "$RC/merge3b_both_sides.txt"
python3 "$PACKET/deleted_not_resurrected.py" "$REPO" 0451d83 44a6bb9 3f3ea56 97fe22f \
    $(git -C "$REPO" diff --name-only 0451d83 3f3ea56) > "$RC/merge3_deleted.txt"
python3 "$PACKET/deleted_not_resurrected.py" "$REPO" 3f3ea56 d4ca85c 16ea10a "$HEAD" \
    $( (git -C "$REPO" diff --name-only 3f3ea56 16ea10a; git -C "$REPO" diff --name-only 3f3ea56 d4ca85c) | sort -u) \
    > "$RC/merge3b_deleted.txt"

# 2. exports
rm -rf "$SCRATCH/head" "$SCRATCH/main16" "$SCRATCH/f5"
mkdir -p "$SCRATCH/head" "$SCRATCH/main16" "$SCRATCH/f5"
git -C "$REPO" archive "$HEAD" | tar -x -C "$SCRATCH/head"
git -C "$REPO" archive 16ea10a | tar -x -C "$SCRATCH/main16"
git -C "$REPO" archive "$HEAD" | tar -x -C "$SCRATCH/f5"

# 3. focused suites and gates at the head
( cd "$SCRATCH/head/tb/pp_top" && taskset -c 0-7 make run ) > "$RC/pp_top_make_run.log" 2>&1
( cd "$SCRATCH/head" && taskset -c 0-7 make -C tb/ucpu run ) > "$RC/ucpu_run.log" 2>&1
( cd "$SCRATCH/head" && taskset -c 0-7 ./scripts/lint_hdl.sh ) > "$RC/lint_hdl.log" 2>&1
( cd "$SCRATCH/head" && python3 scripts/gen_matrix.py --check ) > "$RC/gen_matrix.log" 2>&1
( cd "$SCRATCH/head" && python3 scripts/check_upc_map.py ) > "$RC/upc_map.log" 2>&1
( cd "$SCRATCH/head" && python3 scripts/check_m9_opcodes.py --selftest ) > "$RC/m9_selftest.log" 2>&1
( cd "$SCRATCH/head" && python3 scripts/check_m9_opcodes.py ) > "$RC/m9.log" 2>&1
( cd "$SCRATCH/head" && make check ) > "$RC/make_check.log" 2>&1

# 4. both AECP campaigns in full, in chunks (arm lists from the drivers)
cd "$SCRATCH/head/tb/pp_top"
i=0
for A in $(python3 -c "import re;s=open('aecp_mutants.py').read();a=[x for x,_ in re.findall(r'^\s*\(\"([a-z0-9-]+)\",\s*\"([a-z0-9-]+)\"',s,re.M)];print(' '.join(','.join(a[j:j+14]) for j in range(0,len(a),14)))"); do
  i=$((i+1)); taskset -c 0-7 python3 aecp_mutants.py --output "$SCRATCH/lane_c$i" --only "$A" > "$RC/lane_campaign_chunk$i.log" 2>&1
done
i=0
for A in $(python3 -c "import re;s=open('aecp_dispatch_mutants.py').read();a=[x for x,_ in re.findall(r'^\s*\(\"([a-z0-9-]+)\",\s*\"([a-z0-9-]+)\"',s,re.M)];print(' '.join(','.join(a[j:j+18]) for j in range(0,len(a),18)))"); do
  i=$((i+1)); taskset -c 0-7 python3 aecp_dispatch_mutants.py --verilator verilator --output "$SCRATCH/disp_c$i" --only "$A" > "$RC/dispatch_campaign_chunk$i.log" 2>&1
done
python3 "$PACKET/readme_counts_vs_run.py" README.md "$RC"/lane_campaign_chunk*.log "$RC"/dispatch_campaign_chunk*.log > "$RC/readme_counts_vs_run.txt"

# 5. the two re-cut C5b arms against main's original patches on main's tree
( cd "$SCRATCH/main16/tb/pp_top" && taskset -c 0-7 python3 aecp_dispatch_mutants.py --verilator verilator \
    --output "$SCRATCH/dispatch_main16" --only ov-oversize-never,ov-oversize-at-576 ) > "$RC/dispatch_main16_arms.log" 2>&1
for a in ov-oversize-never ov-oversize-at-576; do
  grep '^FAIL:' "$SCRATCH/dispatch_main16/$a.log" > "$RC/orig_main_$a.fails"
  grep '^FAIL:' "$SCRATCH/disp_c1/$a.log" > "$RC/recut_head_$a.fails"
  diff "$RC/orig_main_$a.fails" "$RC/recut_head_$a.fails" > "$RC/recut_vs_main_$a.diff" || true
done

# 6. the R419-2 F5 probe, unchanged, on a head export
python3 "$PACKET/probe_gdi_stream_info.py" "$SCRATCH/f5" verilator > "$RC/probe_gdi_stream_info_head.log" 2>&1
