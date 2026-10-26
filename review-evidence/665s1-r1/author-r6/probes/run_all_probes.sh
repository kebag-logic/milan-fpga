#!/bin/bash
# Every reviewer probe of rounds 3 to 5, unchanged, at the checkout's head; receipts under $2.
#   $1 checkout   $2 receipts directory (empty)   $3 the management directory   $4 the review packets directory
set -u
C=$1 O=$2 P=$3 RP=$4
S=$O/scratch
mkdir -p "$S" "$O/r702-5-mutants"
git -C "$C" rev-parse HEAD > "$O/head.txt"
R=$P/665s1-a680g/probes/run_cpp_probe.sh
RA=$P/665s1-r702-5/scripts/run_arm.py
# round 5: R702-5's two C++ probes (its run_arm.py), R701-5's C++ probe, R702-5's four mutants, R701-5's count
for arm in core app; do
    for i in 1 2; do
        bash "$R" "$C" "$P/665s1-r702-5/scripts/probe_release_reads.cpp" "$S/release-reads-$arm-if$i" "$arm" "$i" \
            'Core.ReviewProbe*' "$RA" > "$O/r702-5-probe-release-reads-$arm-if$i.log" 2>&1
        echo "rc=$?" >> "$O/r702-5-probe-release-reads-$arm-if$i.log"
    done
done
for i in 1 2; do
    bash "$R" "$C" "$P/665s1-r702-5/scripts/probe_held_interface.cpp" "$S/held-interface-if$i" core "$i" \
        'Core.ReviewProbe*' "$RA" > "$O/r702-5-probe-held-interface-core-if$i.log" 2>&1
    echo "rc=$?" >> "$O/r702-5-probe-held-interface-core-if$i.log"
    bash "$R" "$C" "$P/665s1-r701-5/probes/probe_wait_refusals.cpp" "$S/wait-refusals-if$i" app "$i" \
        'Face.ReviewerProbe*' "$RA" > "$O/r701-5-probe-wait-refusals-app-if$i.log" 2>&1
    echo "rc=$?" >> "$O/r701-5-probe-wait-refusals-app-if$i.log"
done
for m in wait-bound-past-cadence owed-change-not-refused record-not-reset held-interface-not-restored; do
    (cd "$C" && python3 -B "$P/665s1-r702-5/scripts/review_mutants.py" "$C" "$S/r702-5-mutants" "$m" 2) \
        > "$O/r702-5-mutants/$m.out" 2>&1
    echo "rc=$?" >> "$O/r702-5-mutants/$m.out"
done
python3 -B "$P/665s1-r701-5/count_face_defects.py" "$C/sw/firmware/ctrl/test" > "$O/r701-5-count-face-defects.txt" 2>&1
# rounds 3 and 4: R701-3's and R701-4's test-editing probes through round 5's driver; R702-3's and R702-4's as published
python3 -I "$P/665s1-a680g/probes/run_probe.py" "$C" "$RP/665s1-r701-4-packet/scripts/response_probe.py" "$S/r701-3" \
    mailbox 'Face.ALateCommitIsOwedAndPublishedAgainWhole' > "$O/r701-3-response-probe.log" 2>&1
echo "rc=$?" >> "$O/r701-3-response-probe.log"
python3 -I "$P/665s1-a680g/probes/run_probe.py" "$C" "$RP/665s1-r701-4-packet/scripts/late_ack_notify_probe.py" \
    "$S/r701-4" app 'Face.ReviewerProbe*' > "$O/r701-4-late-ack-notify-probe.log" 2>&1
echo "rc=$?" >> "$O/r701-4-late-ack-notify-probe.log"
mkdir -p "$S/r702-3" "$S/r702-4/pk"
cp "$RP/665s1-r702-4-packet/probe_ack.py" "$S/r702-3/"
cp "$RP/665s1-r702-4-packet/delta_probes.py" "$S/r702-4/"
(cd "$S/r702-3" && python3 -I probe_ack.py "$C") > "$O/r702-3-probe-ack.out" 2>&1
echo "rc=$?" >> "$O/r702-3-probe-ack.out"
cp "$S/r702-3/ack-probe.log" "$O/r702-3-probe-ack.log"
(cd "$S/r702-4" && python3 -I delta_probes.py "$C" "$S/r702-4/pk") > "$O/r702-4-delta-probes.out" 2>&1
echo "rc=$?" >> "$O/r702-4-delta-probes.out"
for i in 1 2; do cp "$S/r702-4/pk/scratch/delta-probes/if$i.log" "$O/r702-4-delta-probes-if$i.log"; done
sha256sum "$S/r702-3/probe_ack.py" "$S/r702-4/delta_probes.py" "$RP/665s1-r701-4-packet/scripts/response_probe.py" \
    "$RP/665s1-r701-4-packet/scripts/late_ack_notify_probe.py" "$P/665s1-r702-5/scripts/probe_held_interface.cpp" \
    "$P/665s1-r702-5/scripts/probe_release_reads.cpp" "$P/665s1-r701-5/probes/probe_wait_refusals.cpp" \
    "$P/665s1-r702-5/scripts/run_arm.py" "$P/665s1-r702-5/scripts/review_mutants.py" "$P/665s1-r701-5/count_face_defects.py" \
    | sed "s#$O#<receipts>#;s#$RP#<reviews>#;s#$P#<management>#" > "$O/probe-hashes.txt"
