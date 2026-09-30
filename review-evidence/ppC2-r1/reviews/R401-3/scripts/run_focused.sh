#!/usr/bin/env bash
# R401-3 focused reproduction for processor PR #135 at the exact head.
# Records the commands behind receipts/: every step ran in the foreground,
# one at a time, with Verilator builds capped at 8 jobs by scripts/bin/verilator.
#
#   CLONE=<exact-head clone> PACKET=<this packet dir> \
#   PINNED_VERILATOR=<pinned Verilator 5.050 wrapper> ./scripts/run_focused.sh
set -u
: "${CLONE:?}" "${PACKET:?}" "${PINNED_VERILATOR:?}"
HEAD_SHA=921fff59d6e1243284e477f7a368173018420d35
export PINNED_VERILATOR PATH="$PACKET/scripts/bin:$PATH" TMPDIR="$PACKET/scratch/tmp"
R="$PACKET/receipts"; S="$PACKET/scratch"
mkdir -p "$R/head" "$R/static" "$R/campaign" "$TMPDIR"

# a disposable copy of the exact head tree; the clone itself is never written
rm -rf "$S/head"; mkdir -p "$S/head"
git -C "$CLONE" archive "$HEAD_SHA" | tar -x -C "$S/head"
cd "$S/head" || exit 1

# suites: this lane's, and those main's #132 / #133 changed
for s in maap rx_validator; do make -C tb/$s run > "$R/head/$s-run.log" 2>&1; echo "$s rc=$?"; done
make -C tb/pp_top run > "$R/head/pp_top-run.log" 2>&1; echo "pp_top rc=$?"
for mode in --maap-internal-only --d3-only --dr3a --gsi-internal-only --name-writes-only; do
  tb/pp_top/obj_dir/Vpp_top_sim "$mode" > "$R/head/pp_top$mode.log" 2>&1; echo "pp_top $mode rc=$?"
done
for s in acmp_nvm desc_mem_guard dyn_state srp_encoder srp_stream_fsms srp_top; do
  make -C tb/$s > "$R/head/$s-run.log" 2>&1; echo "$s rc=$?"
done

# the MAAP campaign, and #132's rx_validator arm (the file the merge resolved)
python3 tb/maap/mutants.py --output "$R/campaign" > "$R/campaign.txt" 2>&1; echo "maap mutants rc=$?"
python3 tb/pp_top/d3_mutants.py --output "$R/d3-validator-arm" --verilator "$PACKET/scripts/bin/verilator" \
  --jobs 1 --only validator_admits_held_aecp > "$R/d3-validator-arm.txt" 2>&1; echo "d3 arm rc=$?"

# static gates
./scripts/lint_hdl.sh > "$R/static/lint_hdl.log" 2>&1; echo "lint rc=$?"
make check > "$R/static/make_check.log" 2>&1; echo "make check rc=$?"
python3 scripts/gen_matrix.py --check > "$R/static/gen_matrix.log" 2>&1; echo "gen_matrix rc=$?"
for b in c951a9ff 053f979b b2db3a97; do
  git -C "$CLONE" -c core.pager=cat diff --check "$b" "$HEAD_SHA" > "$R/static/diff_check_$b.log" 2>&1
  echo "diff --check $b rc=$?"
done

# ledger vs logs, reviewer probes and the round-1 RTL, patch identity
python3 "$PACKET/scripts/check_ledger.py" "$CLONE/tb/maap/README.md" "$R/campaign" > "$R/ledger-check.txt"; echo "ledger rc=$?"
python3 "$PACKET/scripts/own_probes.py" --clone "$CLONE" --out "$PACKET" > "$R/own-probes.txt" 2>&1; echo "probes rc=$?"
# R400-2 patch identity: fetch review-evidence/ppC2-r1/reviews/R400-2/receipts/r400-mutants/tx-set-omits-*.patch
# at milan-fpga 1afebd22 and compare sha256 with `git show HEAD:tb/maap/mutations/<same>.patch`.
