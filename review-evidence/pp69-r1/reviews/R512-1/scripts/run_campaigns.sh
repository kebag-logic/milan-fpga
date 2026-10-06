#!/bin/bash
# The #69 control arms of the two campaigns, at the head extraction, with the
# pinned Verilator first on PATH. Logs/rc under receipts/campaigns/.
P=$REVIEWS/pp69-r512-1-packet
export PATH=$P/scratch/bin:$PATH
mkdir -p $P/receipts/campaigns
cd $P/scratch/plant-head
case "$1" in
adp) s=$(date +%s); python3 tb/adp_engine/mutants.py --output $P/scratch/camp-adp --only "if-ingress-collapsed,if-egress-collapsed,if-pdu-index-collapsed,if-gm-sample-collapsed,if-top-count-collapsed,if-top-count-collapsed-lint,if-top-ingress-collapsed,if-top-ingress-live,if-top-range-unguarded,if-link-collapsed,if-gm-slice-reversed,if-link-fall-collapsed,if-aidx-reset-by-index,if-ingress-forced-one,if-top-range-floor-off-by-one,if-top-range-floor-dropped" --jobs 4 > $P/receipts/campaigns/adp-if.log 2>&1; echo "rc=$? seconds=$(($(date +%s)-s))" > $P/receipts/campaigns/adp-if.rc ;;
notify) s=$(date +%s); python3 tb/pp_top/notify_mutants.py --output $P/scratch/camp-notify --verilator $P/scripts/vl_j8.sh --jobs 4 --only port_not_compared port_not_latched port_not_stored avb_counter_row_dropped avb_counter_row_collapsed avb_counter_named_clock avb_counter_any_index avb_counter_name_overlaps_clock rgy_port_tied_zero > $P/receipts/campaigns/notify-69.log 2>&1; echo "rc=$? seconds=$(($(date +%s)-s))" > $P/receipts/campaigns/notify-69.rc; cp $P/scratch/camp-notify/results.json $P/receipts/campaigns/notify-69-results.json 2>/dev/null ;;
esac
