#!/usr/bin/env bash
# run_campaign.sh <repo> <packet>: every probe and mutant of this round, 16 at a time.
# Each job writes receipts/<name>.log and receipts/<name>.rc (rc, then wall seconds).
set -u
export PYTHONDONTWRITEBYTECODE=1
REPO="$1"; P="$2"; PY="$HOME/litex-milan/venv/bin/python3"; S="$P/scripts"; R="$P/receipts"
mkdir -p "$R" "$P/scratch/equiv"
jobs=()
jobs+=("head_test_soc_timing_cuts|cd $REPO/sw/litex && PYTHONHASHSEED=0 $PY test_soc_timing_cuts.py")
for p in 842 1001 10; do for s in staged plain undelayed; do
  jobs+=("equiv_${p}_${s}|$PY $S/probe_zqcs_equiv.py $REPO/sw/litex $p 12000 $s $P/scratch/equiv/${p}_${s}.json")
done; done
for m in zqcs_hold2 zqcs_rephase_extra zqcs_hold_both ref_last_comb_h ref_ready_registered_h ref_no_last_h ref_shipping_equivalent axi_valid_waits_ready axi_dup spi_tx_valid_waits_ready spi_rx_valid_waits_ready spi_rx_dup; do
  jobs+=("mut2_$m|$PY $S/mutate_r2.py $REPO/sw/litex $m")
done
for m in ref_zqcs_done_delayed axi_dropheld spi_tx_dropheld spi_rx_dropheld; do
  jobs+=("authmut_$m|$PY $S/author_mutants_round4.py $REPO/sw/litex $m")
done
for m in ref_ready_registered ref_no_last ref_last_comb axi_lossy_ready axi_pipevalid axi_ar_unstaged spi_tx_lossy_ready spi_rx_lossy_ready spi_cs_comb spi_tx_no_pipe_ready; do
  jobs+=("mut1_$m|$PY $S/mutate_timing_cuts.py $REPO/sw/litex $m")
done
printf '%s\n' "${jobs[@]}" | xargs -P 16 -d '\n' -I{} bash -c '
  j="{}"; n="${j%%|*}"; c="${j#*|}"; s=$(date +%s)
  bash -c "$c" > "'"$R"'/$n.log" 2>&1; rc=$?
  printf "%s %ss\n" "$rc" "$(( $(date +%s) - s ))" > "'"$R"'/$n.rc"'
echo CAMPAIGN DONE > "$R/campaign.done"
