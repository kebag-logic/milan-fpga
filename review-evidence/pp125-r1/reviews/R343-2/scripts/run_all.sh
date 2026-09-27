#!/usr/bin/env bash
# R343-2 reproduction: docs gates, packer-claim probes and mutation discrimination.
# Usage: scripts/run_all.sh <processor checkout at e04234e1> <packet dir>
# The packet dir must contain scratch/r1pub/ with the round-1 public probe scripts
# (kebag-logic/milan-fpga@0b448a50 review-evidence/pp125-r1/reviews/{R342-1,R343-1}/scripts),
# whose sha256 values are checked against the round-1 manifests before use.
set -u
CK=$(realpath "$1"); P=$(realpath "$2"); S=$P/scratch; R=$P/receipts
export PYTHONDONTWRITEBYTECODE=1
mkdir -p "$R" "$S"
cd "$CK" || exit 2
test "$(git rev-parse HEAD)" = e04234e115cfdcaace393ae62ba68562d47834c6 || { echo "wrong head"; exit 2; }

echo "f5ca7619559c84096a12707f7cc83378c6efe77774b06899ca2bf68c8ce595d5  $S/r1pub/R342-1/scripts/probe_packer_claims.py
724a3ee89c63d194be7185b87d2448e063cb6252c549edd8ebfbd4f0e19853a6  $S/r1pub/R343-1/scripts/probe_packer.py
227391e3f0ded673c3c0b864ec88330271c46cba0fd2667f97da0f8ec9a672e5  $S/r1pub/R343-1/scripts/make_mutants.py" \
  | sha256sum -c - || exit 2

# 1. docs gates (the hdl.yml docs job, make lint, gen_matrix, whitespace)
: > "$R/docs-gates.log"
for c in "python3 scripts/check-links.py" "python3 scripts/check-matrix.py" \
         "python3 scripts/check-integrator-params.py" "python3 scripts/render-wavedrom.py --check" \
         "make stale" "python3 scripts/gen_matrix.py --check" "./scripts/lint-diagrams.sh" \
         "git diff --check 493e5e4bf58a6146bf9310194d71c72e18610704 e04234e115cfdcaace393ae62ba68562d47834c6" \
         "git diff --check 1d249e6e18a91c16a2620904483634548b0414a6 e04234e115cfdcaace393ae62ba68562d47834c6"; do
  echo "### $c" >> "$R/docs-gates.log"; bash -c "$c" >> "$R/docs-gates.log" 2>&1; echo "rc=$?" >> "$R/docs-gates.log"
done

# 2. R342's packer-claim probe at head and at a git-archive export of 493e5e4b
rm -rf "$S/base-493e5e4"; mkdir -p "$S/base-493e5e4"; git archive 493e5e4 | tar -x -C "$S/base-493e5e4"
{ python3 -B "$S/r1pub/R342-1/scripts/probe_packer_claims.py" "$CK" "$R/packer-claims-head.tsv"; echo "rc=$?"
  python3 -B "$S/r1pub/R342-1/scripts/probe_packer_claims.py" "$S/base-493e5e4" "$R/packer-claims-base.tsv"; echo "rc=$?"; } \
  > "$R/packer-claims-probe.log" 2>&1

# 3. round-1 probe bank at head, and both probes against scratch mutants
G=$CK/hdl/aecp/desc/gen_desc_image.py; J=$CK/hdl/aecp/desc/example_milan_8.json
python3 -B "$S/r1pub/R343-1/scripts/make_mutants.py" "$G" "$S/mutants"
{ python3 -B "$S/r1pub/R343-1/scripts/probe_packer.py" "$G" "$J"; echo "rc=$?"; } > "$R/probe_packer_head.log" 2>&1
for m in M1_no_body_key M2_l6_l10; do
  { python3 -B "$S/r1pub/R343-1/scripts/probe_packer.py" "$S/mutants/mutant_$m.py" "$J"; echo "rc=$?"; } \
    > "$R/probe_packer_mutant_$m.log" 2>&1
  rm -rf "$S/mutree-$m"; cp -a "$S/base-493e5e4" "$S/mutree-$m"
  cp "$S/mutants/mutant_$m.py" "$S/mutree-$m/hdl/aecp/desc/gen_desc_image.py"
  { python3 -B "$S/r1pub/R342-1/scripts/probe_packer_claims.py" "$S/mutree-$m" "$R/packer-claims-mutant-$m.tsv"; echo "rc=$?"; } \
    > "$R/packer-claims-mutant-$m.log" 2>&1
done

# 4. existing packer unit tests
{ python3 -B tb/desc_store/test_gen_desc_image.py -v; echo "rc=$?"; } > "$R/test_gen_desc_image.log" 2>&1

# the wavedrom gate bootstraps an ignored venv in the checkout; remove it
rm -rf "$CK/.venv-wavedrom"
