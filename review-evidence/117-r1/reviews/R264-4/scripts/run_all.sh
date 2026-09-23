#!/usr/bin/env bash
# Regenerate the R264-4 receipts.
# usage: run_all.sh CLONE EVID_GITDIR PIN_ROOT TOKENS SUPERSEDED OUT
#   CLONE        clean clone at dfe6a587c6dc8e01eaceded4eb8e96d79e68a5ba
#   EVID_GITDIR  git dir holding the 117-review-evidence branch (tip 7626fb2b...)
#   PIN_ROOT     extraction of review-evidence/117-r1 at db842315015dda3d68c9687973c4803bb25ceefb
#   TOKENS       private token table (class<TAB>ci|cs<TAB>hex), never published
#   SUPERSEDED   private list of superseded archive commit ids, never published
#   OUT          receipt directory
# Not regenerated here: redacted_capture_integrity.txt (needs the earlier
# archive's bytes, not republished), hosted_check_runs_dfe6a587.tsv (read-only
# check-runs API), state_before.txt and clone_restore_verify.txt (clone state).
set -u
clone=$1 evid=$2 pin=$3 tokens=$4 superseded=$5 out=$6
here=$(cd "$(dirname "$0")" && pwd)
base=ede8d48ecd7c7f589a14b957951f040d92c99c70
head=dfe6a587c6dc8e01eaceded4eb8e96d79e68a5ba
pinc=db842315015dda3d68c9687973c4803bb25ceefb
tip=7626fb2b850e1e9c707ea247cab211b1e6833e0e
mkdir -p "$out"
git -C "$clone" show "$head:docs/findings/117_GPTP_SILICON_EVIDENCE.md" > "$out/.page.md"
python3 "$here/verify_manifest.py" "$pin" "$out/.page.md" > "$out/verify_manifest.txt"
rm -f "$out/.page.md"
python3 "$here/identity_sweep.py" "$evid" "$tokens" "pin=$pinc:review-evidence" "history=RANGE@$base..$tip" > "$out/identity_sweep_archive.txt"
python3 "$here/identity_sweep.py" "$clone/.git" "$tokens" "prcommits=RANGE@$base..$head" > "$out/identity_sweep_pr_commits.txt"
python3 "$here/identity_sweep.py" "$clone/.git" "$tokens" "headtree=$head" > "$out/identity_sweep_head_tree.txt"
python3 "$here/shape_sweep.py" "$evid" "$base..$pinc" > "$out/shape_sweep_pin_history.txt"
python3 "$here/shape_sweep.py" "$evid" "$pinc..$tip" > "$out/shape_sweep_review_commits.txt"
python3 "$here/shape_sweep.py" "$clone/.git" "$base..$head" > "$out/shape_sweep_pr_commits.txt"
python3 "$here/superseded_mentions.py" "$superseded" "$clone/.git" "$base..$head" "$evid" "$base..$tip" > "$out/superseded_mentions.txt"
python3 "$here/pcap_census.py" "$pin" "$out/pcap_census_pin.txt" "$out/.pcap_private.txt"
rm -f "$out/.pcap_private.txt"
python3 "$here/check_b1_b3.py" "$pin" > "$out/check_b1_b3.txt"
python3 "$here/rederive_step3.py" "$pin/bench-a202" > "$out/rederive_step3.jsonl"
python3 "$here/rederive_step2.py" "$pin/bench-a200" > "$out/rederive_step2.txt"
python3 "$here/turnaround_int.py" "$pin/bench-a200" > "$out/turnaround_int.txt"
python3 "$here/rederive_stream.py" "$pin/bench-a202" > "$out/rederive_stream.txt"
python3 "$here/spot_checks.py" "$pin" > "$out/spot_checks.txt"
python3 "$here/phc_steps.py" "$pin/bench-a202" > "$out/phc_steps.txt"
python3 "$here/carrier_return.py" "$pin/bench-a202" > "$out/carrier_return.txt"
python3 "$here/linkg_brackets.py" "$pin/bench-a202" > "$out/linkg_brackets.txt"
python3 "$here/intra_anchors.py" "$clone" docs/findings/117_GPTP_SILICON_EVIDENCE.md docs/design/GM_LOSS_RECOVERY.md docs/findings/README.md > "$out/anchors_resolve.txt"
(
  cd "$clone" || exit 2
  for g in "docs_check:scripts/docs_check.py" "em_dash:scripts/check_em_dash.py --base $base" \
           "doc_style:scripts/check_doc_style.py" "gptp_docs:scripts/check_gptp_docs.py" \
           "gen_toc_check:scripts/gen_toc.py --check" "gen_toc_anchors:scripts/gen_toc.py --verify-anchors" \
           "baremetal_only:scripts/check_baremetal_only.py --check" "feature_status:scripts/check_feature_status.py" \
           "solution_docs:scripts/check_solution_docs.py" "module_matrix:docs/traceability/gen_module_matrix.py --check"; do
    name=${g%%:*} cmd=${g#*:}
    { echo "\$ python3 $cmd"; python3 $cmd; echo "exit=$?"; } > "$out/gate_$name.txt" 2>&1
  done
)
mkdir -p "$out/.probes"
bash "$here/mutation_probes.sh" "$clone" "$out/.probes" > "$out/mutation_probes.txt" 2>&1
rm -rf "$out/.probes" "$clone/scripts/__pycache__"
python3 "$here/verify_clone.py" "$clone" "$head" 9c80255cbc74dfa1a57eb5979fd4e150c964cc14 \
  external=efeb541ae5fe1e078332d8462dca2fc2d9cb8db5 gptp-processor=c1b617435824929a790739ea8585c3fe1a328cc0 \
  protocol-processor=424c688fa2205b934a7689a58f2aa766420f2326 third_party/verilog-axis=48ff7a7e2ef782cf778d47910cf85835c64b1bce \
  > "$out/clone_restore_verify.txt"
