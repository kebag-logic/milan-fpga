#!/bin/sh
# Run the prior reviewers' probe scripts, unchanged, at a tree with the Git PATH names; one receipt per script.
# usage: run_prior_probes.sh PRIOR_DIR TREE WORK RECEIPT_DIR LABEL
PR=$1; T=$2; W=$3; R=$4; L=$5
mkdir -p "$R" "$W"
for s in r585_14_superproject_sparse_gitlink_serve r585_14_superproject_sparse_gitlink r585_14_superproject r585_14_superproject_sparse; do
  { git --version; bash "$PR/$s.sh" "$T" "$W/$s"; echo "rc=$?"; } > "$R/$s.$L.txt" 2>&1
done
{ git --version; python3 -I "$PR/forge_probe.py" "$T" "$W/forge"; echo "rc=$?"; } > "$R/forge_probe.$L.txt" 2>&1
{ git --version; python3 -I "$PR/store_probe.py" "$T/sw/firmware/ctrl/test" "$T/third_party/tsn-c-stack" "$W/store"; echo "rc=$?"; } > "$R/store_probe.$L.txt" 2>&1
