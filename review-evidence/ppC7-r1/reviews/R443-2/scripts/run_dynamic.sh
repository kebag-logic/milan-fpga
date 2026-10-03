#!/bin/bash
# R443-2 dynamic runs. Usage: run_dynamic.sh <clone> <packet dir> <verilator wrapper>
# Each run uses a git-archive copy of the exact head under <packet>/scratch; the
# two campaign runs and the suite start in the background with their own log and
# rc files; the caller waits on the rc files in the foreground.
set -u
C=${1:?clone}; P=${2:?packet}; V=${3:?verilator}
H=81edaaa74f688081ad34c1e2f392612f46eb558c; R1=e2c7d97d158a30e44289a06a33f8ff4c5e289b87
S=$P/scratch; R=$P/receipts; mkdir -p "$S" "$R"
for d in head-j8 head-j1 head-suite; do mkdir -p "$S/$d"; git -C "$C" archive "$H" | tar -x -C "$S/$d"; done
mkdir -p "$S/base-e2c7"; git -C "$C" archive "$R1" | tar -x -C "$S/base-e2c7"
camp() { # $1 jobs
  mkdir -p "$S/tmp-j$1" "$S/out-j$1"
  ( cd "$S/head-j$1" && export VERILATOR="$V" TMPDIR="$S/tmp-j$1"; s=$(date +%s)
    python3 tb/pp_top/ctr_mutants.py --jobs "$1" --output "$S/out-j$1" > "$R/ctr-campaign-jobs$1.log" 2>&1
    rc=$?; echo "rc=$rc wall_s=$(( $(date +%s) - s ))" > "$R/ctr-campaign-jobs$1.rc" ) </dev/null >/dev/null 2>&1 &
}
camp 8; wait   # the 8-way build peaks near the 12 GB unit cap: run it alone
camp 1
( cd "$S/head-suite" && s=$(date +%s); make -C tb/pp_top VERILATOR="$V" > "$R/pp_top-suite.log" 2>&1
  rc=$?; echo "rc=$rc wall_s=$(( $(date +%s) - s ))" > "$R/pp_top-suite.rc" ) </dev/null >/dev/null 2>&1 &
wait
cmp "$R/ctr-campaign-jobs1.log" "$R/ctr-campaign-jobs8.log" && echo BYTE-IDENTICAL
sha256sum "$R/ctr-campaign-jobs1.log" "$R/ctr-campaign-jobs8.log"
# preprocessed identity of the two RTL files the round touched
for f in hdl/acmp/KL_pp_acmp_listener.sv hdl/top/protocol_processor_top.sv; do
  for t in base-e2c7 head-suite; do "$V" -E -P -I"$S/$t/hdl/common" "$S/$t/$f" > "$S/pp-$t-$(basename $f).txt"; done
  cmp "$S/pp-base-e2c7-$(basename $f).txt" "$S/pp-head-suite-$(basename $f).txt" && echo "IDENTICAL $f"
done
# git diff --check against main, and the negative control with e2c7d97d's attributes
git -C "$C" diff --check c74711d45a8bbc0d6b38cb49211b26a4a6413e88 "$H"; echo "diff-check main..head rc=$?"
git clone -q --no-checkout "$C" "$S/negctl" && git -C "$S/negctl" checkout -q "$R1" &&
  { git -C "$S/negctl" diff --check c74711d45a8bbc0d6b38cb49211b26a4a6413e88 "$R1" >/dev/null; echo "negative control rc=$?"; }
git -C "$S/negctl" checkout -q "$H" && ( cd "$S/negctl" && make check; echo "make check rc=$?" )
