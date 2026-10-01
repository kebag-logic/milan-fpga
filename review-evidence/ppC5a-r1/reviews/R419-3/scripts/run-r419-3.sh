#!/bin/sh
# R419-3 reproduction: every executed step of this review, in order.
# Usage: run-r419-3.sh CLONE PACKET VERILATOR
#   CLONE     a clone of protocol-processor-control-plane-avb-milan holding
#             ee0e2b72 and 16ea10ac (never built in; exports only)
#   PACKET    this packet's directory (receipts/ and scripts/ live there)
#   VERILATOR the pinned Verilator 5.050 executable
# Every heavy step runs under an eight-CPU mask, one at a time.
set -u
C=$1; P=$2; V=$3
HEAD=ee0e2b72ea10c83f983ec9e35878fb0193223ccb
MAIN=16ea10ace6c755c91bb9e864b2b855acb240b09b
S=$P/scratch; R=$P/receipts
mkdir -p "$S/bin" "$S/tmp" "$R"
printf '#!/bin/sh\nexec %s "$@"\n' "$V" > "$S/bin/verilator"; chmod +x "$S/bin/verilator"
export PATH="$S/bin:$PATH" TMPDIR="$S/tmp"
for d in head probe-gdi dispatch-arms lane-arms; do
  mkdir -p "$S/$d"; git -C "$C" archive "$HEAD" | tar -x -C "$S/$d"
done
mkdir -p "$S/main16"; git -C "$C" archive "$MAIN" | tar -x -C "$S/main16"

# 1. static merge checks (no build)
python3 "$P/scripts/merge_side_check.py" "$C" 3f3ea56b 16ea10ac d4ca85c ee0e2b7 > "$P/merge_main_side_ee0e2b7.txt"
python3 "$P/scripts/merge_side_check.py" "$C" 3f3ea56b d4ca85c 16ea10ac ee0e2b7 > "$P/merge_lane_side_ee0e2b7.txt"
python3 "$P/scripts/merge_side_check.py" "$C" 0451d83d 3f3ea56b 44a6bb9 97fe22f > "$P/merge_main_side_97fe22f.txt"
python3 "$P/scripts/merge_side_check.py" "$C" 0451d83d 44a6bb9 3f3ea56b 97fe22f > "$P/merge_lane_side_97fe22f.txt"

# 2. the whole tb/pp_top suite (four builds) and tb/ucpu at the head
(cd "$S/head" && taskset -c 0-7 make -C tb/pp_top run) > "$R/pp_top-run.log" 2>&1; echo "rc=$?" >> "$R/pp_top-run.log"
(cd "$S/head" && taskset -c 0-7 make -C tb/ucpu run) > "$R/ucpu-run.log" 2>&1; echo "rc=$?" >> "$R/ucpu-run.log"

# 3. the round-2 F5 probe, unchanged
taskset -c 0-7 python3 "$P/scripts/probe_gdi_stream_info.py" "$S/probe-gdi" "$S/bin/verilator" > "$R/probe-gdi-stream-info.log" 2>&1
echo "rc=$?" >> "$R/probe-gdi-stream-info.log"

# 4. C5b's two re-cut arms at the head, and main's originals at 16ea10ac
(cd "$S/dispatch-arms" && taskset -c 0-7 python3 tb/pp_top/aecp_dispatch_mutants.py --output "$S/out-dispatch-head" \
   --only ov-oversize-never,ov-oversize-at-576 --verilator "$S/bin/verilator") > "$R/dispatch-recut-arms-head.log" 2>&1
(cd "$S/main16" && taskset -c 0-7 python3 tb/pp_top/aecp_dispatch_mutants.py --output "$S/out-dispatch-main" \
   --only ov-oversize-never,ov-oversize-at-576 --verilator "$S/bin/verilator") > "$R/dispatch-orig-arms-main16ea10ac.log" 2>&1

# 5. the lane's whole AECP campaign at the head, then every count against the README
(cd "$S/lane-arms" && taskset -c 0-7 python3 tb/pp_top/aecp_mutants.py --output "$S/out-aecp-head") > "$R/aecp-mutants-head.log" 2>&1
python3 "$P/scripts/compare_campaign_counts.py" "$C/tb/pp_top/README.md" '### AECP deadline and hazard-class controls' \
  "$R/aecp-mutants-head.log" > "$R/aecp-mutants-vs-readme.txt"

# 6. light gates on the head copy
(cd "$S/head" && taskset -c 8-15 ./scripts/lint_hdl.sh) > "$R/lint_hdl.log" 2>&1
for t in links matrix modmatrix params; do (cd "$S/head" && make "$t") > "$R/docs-$t.log" 2>&1; done
(cd "$S/head" && python3 scripts/gen_matrix.py --check) > "$R/gen_matrix-check.log" 2>&1

# 7. the reviewed clone is still the published head
sh "$P/scripts/tree_integrity.sh" "$C" "$HEAD" 3eb7d8ec80192da62a2c2c3966628782c5d93854 > "$R/tree-integrity-final.txt"
