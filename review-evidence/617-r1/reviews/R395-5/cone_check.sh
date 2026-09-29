#!/bin/sh
# Structural interaction check for the composed milan_datapath.sv:
# the #602 restart / re-base signals must not reach the ports of the media
# NCO, the grid aligner or the capture crossbar that this PR binds, and the
# PR's aligner binding must not reach the #602 restart engine.
# Usage: cone_check.sh <repo>   (exit 0 = no shared signal found)
set -u
F=$1/hdl/milan/milan_datapath.sv
rc=0
# Instance port blocks: from the instance header line to the closing ');'.
block() { awk -v pat="$1" 'index($0, pat) {on=1} on {print NR": "$0} on && /^[[:space:]]*[)];/ {exit}' "$F"; }
echo "== media_nco ports";         block ') media_nco (' > /tmp/cc_nco.$$
echo "== media_grid_align ports";  block ') media_grid_align (' > /tmp/cc_mga.$$
echo "== chan_map_capture ports";  block ') chan_map_capture (' > /tmp/cc_cmap.$$
echo "== media_clock_restart ports"; block 'KL_media_clock_restart #' > /tmp/cc_mcr.$$
for f in /tmp/cc_nco.$$ /tmp/cc_mga.$$ /tmp/cc_cmap.$$; do
  echo "-- $(basename "$f" | cut -d. -f1): $(wc -l < "$f") lines"
  [ -s "$f" ] || { echo "   EMPTY PORT BLOCK: pattern did not match"; rc=2; continue; }
  if grep -nE 'media_rebase_p_w|mcr_restart_p_w|mcr_mr_v_w|render_recentre_p_w|eff_ptp_adjust_w|cfg_ptp_cmd_load|aaf_mr_w|crft_mr_w' "$f"; then
    echo "   SHARED SIGNAL FOUND"; rc=1
  else
    echo "   no #602 restart/re-base signal"
  fi
done
echo "-- media_clock_restart: $(wc -l < /tmp/cc_mcr.$$) lines"
if grep -nE 'mnco_|mga_|media_tick_q_r|MGA_KEEPOFF|CMAP_TDM|aafcap_' /tmp/cc_mcr.$$; then
  echo "   PR SIGNAL FOUND IN RESTART ENGINE"; rc=1
else
  echo "   no PR aligner/NCO/capture signal"
fi
echo "== drivers of the aligner/NCO shared inputs"
grep -nE '^[[:space:]]*assign[[:space:]]+mnco_servo_en_w|crf_clk_selected_r[[:space:]]*<=' "$F"
echo "== every reader of the #602 signals"
grep -nE 'media_rebase_p_w|mcr_restart_p_w|mcr_mr_v_w|render_recentre_p_w' "$F"
rm -f /tmp/cc_nco.$$ /tmp/cc_mga.$$ /tmp/cc_cmap.$$ /tmp/cc_mcr.$$
echo "rc=$rc"
exit $rc
