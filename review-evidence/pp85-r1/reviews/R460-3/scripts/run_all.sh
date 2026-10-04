#!/bin/sh
# Reviewer receipt driver (round R460-3): reproduce every run in this packet.
# usage: run_all.sh CLONE PACKET VERILATOR
#   CLONE     a checkout of the exact head (read only; never written)
#   PACKET    the output packet directory (receipts/ and scratch/ go under it)
#   VERILATOR the pinned Verilator 5.050 executable
# Each campaign starts in the background with its own log and rc file; the
# caller waits on the rc files in the foreground.
set -eu
C=$1 P=$2 V=$3
S=$P/scratch R=$P/receipts H=4811c21d8fe29faa1e9e713a6622bb206189e74b
mkdir -p "$S/head" "$S/tmp" "$S/bin" "$R"
git -C "$C" archive "$H" | tar -x -C "$S/head"
ln -sf "$V" "$S/bin/verilator"
export VERILATOR="$V" TMPDIR="$S/tmp"
# 1. the suite at the head (foreground)
(cd "$S/head/tb/adp_engine" && make run VERILATOR="$V") > "$R/suite-adp_engine.log" 2>&1
echo $? > "$R/suite-adp_engine.rc"
# 2. the checked-in mutant campaign
(cd "$S/head/tb/adp_engine" && python3 mutants.py --output "$S/campaign-out" --jobs 12 \
  > "$R/campaign.log" 2>&1; echo $? > "$R/campaign.rc") &
wait
# 3. probes, concurrently (5 + 5 + 3 jobs)
(cd "$P/scripts" && python3 probes3.py --root "$S/head" --scratch "$S/p3" --out "$R/probes3" \
  --jobs 5 > "$R/probes3.txt" 2>&1; echo $? > "$R/probes3.rc") &
(cd "$P/scripts/prior" && python3 r460-1-probes.py --root "$S/head" --scratch "$S/p1" \
  --out "$R/r460-1-probes" --jobs 5 > "$R/r460-1-probes.txt" 2>&1; echo $? > "$R/r460-1-probes.rc") &
(cd "$P/scripts/prior" && export PATH="$S/bin:$PATH" &&
  python3 r461_probes.py --tree "$S/head" --work "$S/q" --out "$R/r461-probes" --jobs 3 \
    > "$R/r461-probes.txt" 2>&1; echo $? > "$R/r461-probes.rc"
  for v in A B; do
    python3 r461_fixcheck.py --variant $v --tree "$S/head" --work "$S/f$v" --out "$R/r461-fixcheck" \
      --jobs 3 > "$R/r461-fixcheck-$v.txt" 2>&1; echo $? > "$R/r461-fixcheck-$v.rc"
  done) &
wait
# 4. the pp_top run under q2 (unchanged prior script), docs gates, comparisons
sh "$P/scripts/prior/pptop_q2.sh" "$P"
(cd "$S/head" && make check > "$R/make-check.log" 2>&1; echo $? > "$R/make-check.rc")
(cd "$S/head" && python3 scripts/gen_matrix.py --check > "$R/gen-matrix-check.log" 2>&1; \
  echo $? > "$R/gen-matrix-check.rc")
python3 "$P/scripts/compare_counts.py" "$C/tb/adp_engine/README.md" "$R/campaign.log" \
  > "$R/campaign-vs-readme.txt" || true
sh "$P/scripts/verify_clone.sh" "$C" "$H" 320166a09c124757e9f217dbb91f822690f87c34 \
  > "$R/clone-integrity.txt" 2>&1
