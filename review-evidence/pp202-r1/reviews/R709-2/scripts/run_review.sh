#!/bin/sh
# Reproduce this review's executions from an exact-head processor clone.
# usage: run_review.sh <processor-clone-at-ebb1f001> <packet-dir> <verilator-5.050>
set -e
SRC=$1; P=$2; V=$3; S=$P/scratch; R=$P/receipts; mkdir -p "$S" "$R" "$S/tmp"
cd "$SRC"
rm -rf "$S/head" "$S/prevrtl"; mkdir -p "$S/head" "$S/prevrtl"
git archive ebb1f0010bde76c38cc5270a6366ee9e3157ec54 | tar -x -C "$S/head"
cp -r "$S/head/hdl" "$S/head/tb" "$S/prevrtl/"
git show a8aa626e1cba30625ac764c70e1fb8fb02c69c40:hdl/acmp/KL_acmp_talker.sv > "$S/prevrtl/hdl/acmp/KL_acmp_talker.sv"
# 1. talker suite at head, and the head bench on the previous head's talker RTL
(cd "$S/head/tb/acmp_talker" && make run VERILATOR="$V" > "$R/talker-head.log" 2>&1; echo $? > "$R/talker-head.rc") &
(cd "$S/prevrtl/tb/acmp_talker" && make run VERILATOR="$V" > "$R/talker-head-bench-on-a8aa626-rtl.log" 2>&1; echo $? > "$R/talker-head-bench-on-a8aa626-rtl.rc") &
# 2. the STREAM_ID mutant group through the repository's own judge
(cd "$S/head" && TMPDIR="$S/tmp" python3 tb/pp_top/acmp_mutants.py --output "$S/mut-streamid" --verilator "$V" --jobs 8 \
  --only $(python3 -I -c "import ast,sys;t=open('tb/pp_top/acmp_mutants.py').read();i=t.index('STREAM_ID = (');print(' '.join(sorted(set(__import__('re').findall(r'Mutant\(\"([a-z0-9_]+)\"', t[i:t.index('MUTANTS =', i)])))))") \
  > "$R/streamid-mutants.log" 2>&1; echo $? > "$R/streamid-mutants.rc") &
wait
# 3. lint and the docs gate (the gate needs a git checkout)
(cd "$S/head/tb/acmp_talker" && make lint VERILATOR="$V" > "$R/talker-lint.log" 2>&1; echo $? > "$R/talker-lint.rc")
rm -rf "$S/headgit"; git clone -q --no-local "$SRC" "$S/headgit"
(cd "$S/headgit" && git checkout -q --detach ebb1f0010bde76c38cc5270a6366ee9e3157ec54 && make check > "$R/make-check.log" 2>&1; echo $? > "$R/make-check.rc")
# 4. reviewer probes
"$P/scripts/run_lv_probe.sh" "$S/head" "$S/lvprobe" "$V" > "$R/lv-probe.log" 2>&1; echo $? > "$R/lv-probe.rc"
"$P/scripts/run_talker_window_probe.sh" "$S/head" "$S/winprobe" "$V" > "$R/talker-window-probe.log" 2>&1; echo $? > "$R/talker-window-probe.rc"
