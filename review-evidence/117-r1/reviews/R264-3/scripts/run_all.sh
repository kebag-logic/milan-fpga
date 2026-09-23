#!/usr/bin/env bash
# Reproduce every R264-3 receipt.
#
# usage: run_all.sh CLONE EVID_GITDIR TOKENS SUPERSEDED OUT
#   CLONE        worktree of kebag-logic/milan-fpga at 8016f7ac843b0ae6764dc4ec0140cda5ac7d6cc1
#   EVID_GITDIR  bare repository holding refs/remotes/origin/117-review-evidence
#                (tip 4165beb89afe217931bc52a8aaf800303e7bee1b) and, for the positive
#                controls, the two superseded archive commits named in the manager's
#                2026-09-23 note, fetched by full SHA
#   TOKENS       private token file (label, class, ci|cs, bytes literal); never published
#   SUPERSEDED   private file of 'LABEL SHA' lines for superseded archive commits; the
#                second and fourth lines are the original and first-pass archives
#   OUT          output directory for receipts
set -euo pipefail
# keep the gates from leaving bytecode caches in the reviewed clone
export PYTHONDONTWRITEBYTECODE=1

clone=$1 evid=$2 tokens=$3 superseded=$4 out=$5
here=$(cd "$(dirname "$0")" && pwd)
pin=74ac94e8eb331202f39d66cc006bc2640481e6da
tip=4165beb89afe217931bc52a8aaf800303e7bee1b
head=8016f7ac843b0ae6764dc4ec0140cda5ac7d6cc1
base=ede8d48ecd7c7f589a14b957951f040d92c99c70
branch="5ff947b48a4a497d8940a0f8198e5c0ab8ba70aa,6af416d195094bbbe3bbb0efd25d18c63589736e,c615dbba3dbcd6811081f05ca34d992487c481a2,$pin,7205edb34f4074e569f7e59ee163070e30d080d6,0f8ac34a6bdb148c932df1154fb042e8915e51f8,ea4a884c7c5289c7879752883d0c2de66ba917b8,$tip"
pr="c3eb95fa9ac86a3f20b45f94057d6c011127db08,0abf147f726721f4a323ee6a32095a02363fe2dc,$head"
mkdir -p "$out"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

test "$(git -C "$clone" rev-parse HEAD)" = "$head"
git --git-dir "$evid" archive "$pin" review-evidence/117-r1 | tar -x -C "$work"
root="$work/review-evidence/117-r1"

orig=$(sed -n 2p "$superseded" | cut -d' ' -f2)
first=$(sed -n 4p "$superseded" | cut -d' ' -f2)
python3 "$here/identity_sweep.py" --repo "$evid" --tokens "$tokens" --prefix review-evidence --hide-revs \
  --scope "control-superseded-original-archive:$orig" \
  --scope "control-superseded-firstpass-archive:$first" > "$out/sweep-controls.txt"
python3 "$here/identity_sweep.py" --repo "$evid" --tokens "$tokens" \
  --scope "pin-74ac94e8-full-tree:$pin" --scope "branch-8-commits-full-trees:$branch" \
  --scope "base-ede8d48e-full-tree:$base" > "$out/sweep-evidence-branch.txt"
python3 "$here/identity_sweep.py" --repo "$clone/.git" --tokens "$tokens" \
  --scope "pr-531-three-commits-full-trees:$pr" > "$out/sweep-pr531.txt"
python3 "$here/identity_sweep.py" --repo "$clone/.git" --tokens "$tokens" --prefix docs \
  --scope "pr-531-docs-subtree-three-commits:$pr" >> "$out/sweep-pr531.txt"
(cd "$clone" && python3 "$here/binary_hit_container.py" docs/DOC_MAP.png \
  docs/history/v1/diagrams/timesync_chain.png docs/diagrams/egress_queue_map.png aem-and-aecp.pdf) >> "$out/sweep-pr531.txt"
python3 "$here/per_commit_token_files.py" "$evid" "$tokens" L3 ${branch//,/ } > "$out/usb-serial-per-commit.txt"
python3 "$here/superseded_link_sweep.py" "$clone/.git" "$superseded" "pr531-commits:$pr" > "$out/superseded-link-sweep.txt"
python3 "$here/superseded_link_sweep.py" "$evid" "$superseded" "evidence-branch-8-commits:$branch" \
  "pin-74ac94e8:$pin" >> "$out/superseded-link-sweep.txt"
python3 "$here/verify_page_vs_archive.py" "$clone/docs/findings/117_GPTP_SILICON_EVIDENCE.md" "$root" > "$out/page-vs-archive.txt"
python3 "$here/pcap_envelope_census.py" "$root" > "$out/pcap-envelope-census.txt"
python3 "$here/census_and_daemons.py" "$root" "$clone" "$base" > "$out/census-and-daemons.txt"
python3 "$here/console_command_census.py" "$root" > "$out/console-command-census.txt"
python3 "$here/step3_recheck.py" "$root" > "$out/step3-recheck.txt"
python3 "$here/step3_acmp_crf.py" "$root" > "$out/step3-acmp-crf.txt"
python3 "$here/superseded_original_checks.py" "$evid" "$orig" "$root" \
  33f0e7f9e86fe4829a2de6f6d04d1edf1463b7d6653c2865ad985f183b0ddfbc > "$out/superseded-original-checks.txt"
git -C "$clone" show "$base:scripts/baremetal_uart_smoke.py" | sha256sum | sed 's/-$/scripts\/baremetal_uart_smoke.py at ede8d48e/' > "$out/external-hash-sources.txt"
for h in f0725eef7a361bd7dc6d692c369868f25e5d4f49f6b7267562a0b5f949ada33d \
         aaece32fc6c84f790273878350f674c142407a6b9ff2097862870784921da5fb \
         9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404 \
         69322600bc9dc40a698ed30d125d29d2723f51cc1b26c0f1c3abc96acb39deab \
         4db0e6da9c9c910a5ee00e56c25908c190c380799e44c846bcfb4ffc7dc045a7 \
         71e798fc401ed3fbaac4cd43a299f23498beafa466aaa17d6773590a62fa93e2 \
         e84e579c3f48e7cd37443f64d28f6a5fbaaf7a5752938ce6bc005d00ac1b0083; do
  n=$(cd "$root" && { grep -rl "$h" . || true; } | sort | tr '\n' ' ')
  echo "IMAGE-HASH ${h:0:16} files_in_pin: ${n:-none}"
done >> "$out/external-hash-sources.txt"
python3 "$here/fw_digest_enumeration.py" 33f0e7f9e86fe4829a2de6f6d04d1edf1463b7d6653c2865ad985f183b0ddfbc > "$out/fw-digest-enumeration.txt"
(
  cd "$clone"
  for cmd in "python3 scripts/docs_check.py" "python3 scripts/check_em_dash.py --base $base" \
             "python3 scripts/check_doc_style.py" "python3 scripts/check_gptp_docs.py" \
             "python3 scripts/check_baremetal_only.py --check" "python3 scripts/check_doc_paths.py" \
             "python3 scripts/gen_toc.py --verify-anchors" "python3 scripts/gen_toc.py --check" \
             "python3 scripts/check_feature_status.py" "python3 scripts/check_hygiene.py --check"; do
    echo "=== \$ $cmd"
    rc=0; $cmd || rc=$?
    echo "=== rc=$rc :: $cmd"
  done
) > "$out/docs-gates.txt" 2>&1
echo "run_all: receipts written"
