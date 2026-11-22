#!/bin/sh
# run_probes.sh <checkout> <packet>: the reviewer's probe arms and shipped focused suites at head, concurrently.
R=$1; P=$2; E=$P/scratch/ev/review-evidence/956-r1/reviews
F='Talker.RegistrationAfterLinkResetIsNoticed:ReviewerPhase.*:Talker.R875*:R875/R875P4.*'
S1=configs/endstation_ax7101_1x1_tdm8.yaml; S8=configs/endstation_ax7101_8x8.yaml
PR="$E/R876-1/reset_probe.cpp $E/R875-1/scripts/probe_phase_956.cpp $P/scripts/probe_r875_2.cpp"
L="$E/R875-1/scripts/probe_link_reset_957.cpp"
cat > $P/scratch/jobs.txt <<J
srp-probes-8x8-if1 srp 1 $S8 srp_talker.cpp $F $PR
srp-probes-8x8-if2 srp 2 $S8 srp_talker.cpp $F $PR
suite-srp_talker-1x1-if1 srp 1 $S1 srp_talker.cpp *
suite-srp_talker-8x8-if1 srp 1 $S8 srp_talker.cpp *
suite-srp_talker-8x8-if2 srp 2 $S8 srp_talker.cpp *
suite-srp_mbx-8x8-if1 srp 1 $S8 srp_mbx.cpp Srp.ABuild*:Srp.*Transmit*:Srp.*Join*
suite-srp_mbx-8x8-if2 srp 2 $S8 srp_mbx.cpp Srp.ABuild*:Srp.*Transmit*:Srp.*Join*
aecp-probe-1x1-if1 aecp 1 $S1 test_aecp.cpp AppOutputs.* $L
aecp-probe-1x1-if2 aecp 2 $S1 test_aecp.cpp AppOutputs.* $L
aecp-probe-8x8-if1 aecp 1 $S8 test_aecp.cpp AppOutputs.* $L
J
while read -r tag kind n cfg test filt probes; do
  ( python3 -B $P/scripts/probe_arm.py $R $P/scratch/w-$tag $kind $n $cfg $test "$filt" $probes > $P/receipts/probes/$tag.log 2>&1
    echo $? > $P/receipts/probes/$tag.rc ) &
done < $P/scratch/jobs.txt
wait
for f in $P/receipts/probes/*.rc; do echo "$(basename $f .rc) rc=$(cat $f)"; done
