#!/bin/sh
# R571-3 reproduction. Usage: run_review.sh <clone at 83239549> <packet dir> <verilator 5.050>
# Runs the exact-head campaign, builds the two harness probes, runs them against
# the campaign's clean and credit-on-step ROMs, and confirms plant identity.
set -eu
REPO=$1; P=$2; export VERILATOR=$3
S=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$P/receipts" "$P/scratch"
# 1. Exact-head campaign (clean, nocease-control, six planted defects).
(cd "$REPO/tb/verilator/gptp_plane" && VERILATOR_JOBS=12 python3 phc_step.py --mutants \
   --work "$P/scratch/campaign") > "$P/receipts/campaign_head.log" 2>&1
# 2. Harness probes (answered: crossing answered again; partial: Pdelay_Resp, no Follow_Up).
python3 -I "$S/make_harness_probes.py" "$REPO/tb/verilator/gptp_plane/sim_phc_step.cpp" "$P/scratch/probes/h"
for v in answered partial; do sh "$S/build_probe.sh" "$REPO" "$P/scratch/probes/h/$v" 16; done
for combo in answered:clean partial:clean partial:credit-on-step; do
  h=${combo%%:*}; rom=${combo##*:}; d=$P/scratch/probes/run/$h-$rom
  mkdir -p "$d"; cp "$P/scratch/campaign/$rom/gptp_ucode.hex" "$d/"
  (cd "$d" && "$P/scratch/probes/h/$h/obj/phc_step" > run.log 2>&1; echo $? > rc) || true
done
# 3. R571-2's published credit_on_step patch applied to the head donor must equal
#    the campaign's credit-on-step generator text.
cp "$REPO/gptp-processor/hdl/ucode/gen_gptp_ucode.py" "$P/scratch/gen.py"
patch -s "$P/scratch/gen.py" < "$P/receipts/r571-2_patch_credit_on_step.diff"
cmp "$P/scratch/gen.py" "$P/scratch/campaign/credit-on-step/generate.py"
# 4. Evidence-reader ratchet.
(cd "$REPO" && python3 scripts/measure_test_evidence.py --check) > "$P/receipts/measure_test_evidence_check.log" 2>&1
