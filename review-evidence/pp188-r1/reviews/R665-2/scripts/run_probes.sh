#!/usr/bin/env bash
# Exact-head probes for the round-2 review of PR #195 (issues #188, #189).
# Usage: run_probes.sh PACKET_DIR JOB
#   PACKET_DIR holds scratch/<copy>/ trees extracted with
#   `git archive 7f56fc4d7f5102cac6dacb9c00f372d20d3b379e | tar -x`, and
#   scratch/bin/verilator, a link to the pinned Verilator 5.050 wrapper.
#   JOB is one of: pptop fsms acmpl srpmut acmpmut
# Each job writes receipts/<job>.log and receipts/<job>.rc (its exit code).
set -u
P=$1
JOB=$2
S=$P/scratch
V=$S/bin/verilator
export PATH=$S/bin:$PATH TMPDIR=$S/tmp
R=$P/receipts
mkdir -p "$R" "$TMPDIR"
case $JOB in
  pptop)  cd "$S/t-pptop/tb/pp_top" && make run VERILATOR="$V" ;;
  fsms)   cd "$S/t-fsms/tb/srp_stream_fsms" && make VERILATOR="$V" ;;
  acmpl)  cd "$S/t-acmpl/tb/acmp_listener" && make run VERILATOR="$V" ;;
  srpmut) cd "$S/t-srpmut" && python3 tb/srp_top/mutants.py --output "$S/srpmut-out" --jobs 6 \
            --only listener-csid-ram-ignores-park,listener-csid-flops-ignores-park,listener-rebind-back-keeps-park,listener-lo-not-owed,listener-park-retires-on-txla,listener-parked-applies-rx,listener-unrecorded-applicant-owes,listener-rebind-abandons-leave,listener-park-never-retires,listener-aa-tx-stays-aa,listener-reprobe-abandons-leave,listener-reprobe-parks-own-stream,listener-declaration-not-held ;;
  acmpmut) cd "$S/t-acmpmut" && python3 tb/pp_top/acmp_mutants.py --output "$S/acmpmut-out" --verilator "$V" --jobs 2 \
            --only tk_failed_first_payload tk_failed_or_payload tk_failed_and_payload router_coalesce_unflagged tk_type_unlatched ;;
  *) echo "unknown job $JOB"; exit 2 ;;
esac > "$R/$JOB.log" 2>&1
echo $? > "$R/$JOB.rc"
