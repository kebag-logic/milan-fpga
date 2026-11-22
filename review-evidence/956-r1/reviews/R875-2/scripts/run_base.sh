#!/bin/sh
# run_base.sh <packet>: head's srp_talker.cpp/test_aecp.cpp plus the prior reviewers' probes on 0d80f0ed's firmware.
P=$1; B=$P/scratch/base-0d80f0ed; E=$P/scratch/ev/review-evidence/956-r1/reviews
F='Talker.RegistrationAfterLinkResetIsNoticed:Talker.ListenerRegistrationAfterAResetIsNoticed:Talker.ChangedDestination*:EveryPhase/*:ReviewerPhase.*'
for t in "1x1-if1 1 configs/endstation_ax7101_1x1_tdm8.yaml" "8x8-if1 1 configs/endstation_ax7101_8x8.yaml" "8x8-if2 2 configs/endstation_ax7101_8x8.yaml"; do set -- $t
  ( python3 -B $P/scripts/probe_arm.py $B $P/scratch/wb-srp-$1 srp $2 $3 srp_talker.cpp "$F" $E/R876-1/reset_probe.cpp $E/R875-1/scripts/probe_phase_956.cpp > $P/receipts/probes/base-0d80f0ed-srp-$1.log 2>&1; echo $? > $P/receipts/probes/base-0d80f0ed-srp-$1.rc ) &
done
for t in "1x1-if1 1 configs/endstation_ax7101_1x1_tdm8.yaml" "1x1-if2 2 configs/endstation_ax7101_1x1_tdm8.yaml" "8x8-if1 1 configs/endstation_ax7101_8x8.yaml"; do set -- $t
  ( python3 -B $P/scripts/probe_arm.py $B $P/scratch/wb-aecp-$1 aecp $2 $3 test_aecp.cpp 'AppOutputs.*' $E/R875-1/scripts/probe_link_reset_957.cpp > $P/receipts/probes/base-0d80f0ed-aecp-$1.log 2>&1; echo $? > $P/receipts/probes/base-0d80f0ed-aecp-$1.rc ) &
done
wait
