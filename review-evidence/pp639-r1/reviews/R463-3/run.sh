#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# R463-3 reproduction of the reviewer-owned runs for processor PR #155 (milan-fpga #639).
# Usage: sh run.sh CLONE OUT VERILATOR
#   CLONE      a clone of the processor repository holding c725be12d7ea6bf96f1b64e3a56416f0d4defd6c
#   OUT        an empty working directory (extracts, logs and campaign outputs go here)
#   VERILATOR  a Verilator 5.050 executable
# Each step writes its own log and rc file. The steps are independent apart from the extracts;
# the review ran them concurrently with at most four builds at a time.
set -u
CLONE=$1; OUT=$2; V=$3
HEAD=c725be12d7ea6bf96f1b64e3a56416f0d4defd6c
MAIN=b0a74196   # processor main merged into the head (PR #157)
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$OUT/head-src" "$OUT/head" "$OUT/main" "$OUT/logs" "$OUT/tmp"
git -C "$CLONE" archive "$HEAD" | tar -x -C "$OUT/head-src"
git -C "$CLONE" archive "$HEAD" | tar -x -C "$OUT/head"
git -C "$CLONE" archive "$MAIN" | tar -x -C "$OUT/main"
export TMPDIR="$OUT/tmp"
step() { name=$1; shift; ( "$@" > "$OUT/logs/$name.log" 2>&1; echo $? > "$OUT/logs/$name.rc" ); }
# 1. the two suites that read the changed blocks, at the head (six pp_top builds)
step head-pp_top make -C "$OUT/head/tb/pp_top" VERILATOR="$V"
step head-acmp_listener make -C "$OUT/head/tb/acmp_listener" VERILATOR="$V"
# 2. the committed ACMP campaign (33 arms, four goldens)
(cd "$OUT/head-src" && step acmp-campaign python3 tb/pp_top/acmp_mutants.py \
    --output "$OUT/acmp-camp" --jobs 3 --verilator "$V")
# 3. the committed notify campaign (47 arms) and the AECP campaign's TD control and arms
(cd "$OUT/head-src" && step notify-campaign python3 tb/pp_top/notify_mutants.py \
    --output "$OUT/notify-camp" --verilator "$V" --jobs 5)
(cd "$OUT/head-src" && PATH="$(dirname "$V"):$PATH" step aecp-td python3 tb/pp_top/aecp_mutants.py \
    --output "$OUT/aecp-td" --only td-lock-default-59s,td-tl-default-301s --jobs 3)
# 4. the reviewer's own probes (probes.py lists each edit and its expectation)
step probes python3 "$HERE/probes.py" --root "$OUT/head-src" --main "$OUT/main" \
    --output "$OUT/probes" --verilator "$V" --jobs 3
# 5. focused lint of the two changed modules, and the documentation gates
(cd "$OUT/head-src" && pkgs=$(find hdl -name '*_pkg.sv' | sort) && all=$(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort) \
  && for top in protocol_processor_top KL_pp_acmp_listener; do
       "$V" --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM \
            --Mdir "$OUT/tmp/lint-$top" --top-module "$top" $pkgs $all > "$OUT/logs/lint-$top.log" 2>&1
       echo $? > "$OUT/logs/lint-$top.rc"
     done)
cp -a "$OUT/head-src" "$OUT/docgate"
(cd "$OUT/docgate" && step make-check make check && step gen-matrix python3 scripts/gen_matrix.py --check)
python3 "$HERE/summarize.py" "$OUT"
