#!/bin/bash
# SPDX-License-Identifier: MIT
# Replay earlier reviewers' probes, byte-unchanged (blob ids in out/prior_probe_blobs.txt),
# against a clean clone of the reviewed head. The only adaptation: R556-5's
# plant_tree_probe.sh pins the commit it checks out, so a copy with the reviewed head's
# id substituted is run (diff recorded in REPORT.md). R557-5 scripts are placed so their
# fixed relative clang18 location resolves to the same Clang 18 package extraction.
# usage: replay_prior.sh PRIOR_DIR REPLAY_DIR CAMPAIGN_DIR   (load env.sh first)
D=$1; R=$2; C=$3
T=$R/tree; O=$R/out; mkdir -p "$O"
job() { name=$1; shift; ( "$@" > "$O/$name.log" 2>&1; echo $? > "$O/$name.rc" ) & }
job R556-3_comment_probes python3 -B "$D/R556-3/scripts/comment_probes.py" "$T"
job R556-3_needle_probes python3 -B "$D/R556-3/scripts/needle_probes.py" "$T"
job R556-4_comment_bypass_probe python3 -B "$D/R556-4/scripts/comment_bypass_probe.py" "$T" "$R/w-bypass"
job R556-4_needle_default_fragments python3 -B "$D/R556-4/scripts/needle_default_fragments.py" "$T"
job R556-4_needle_specificity python3 -B "$D/R556-4/scripts/needle_specificity.py" "$T" "$C"
job R557-4_full_comment_bypass python3 -B "$D/R557-4/scripts/full_comment_bypass.py" --repo "$T" --work "$R/w-full" --output "$O/R557-4_full_comment_bypass.json"
job R556-5_hidden_text_probe python3 -B "$D/R556-5/probes/hidden_text_probe.py" "$T" "$R/w-hidden"
job R556-5_plant_tree_probe sh "$R/plant_tree_probe.head.sh" "$T" "$R/w-plant"
job R557-5_independent_probes python3 -B "$R/R557-5/scripts/independent_probes.py" "$T"
job R557-5_preservation_and_probe python3 -B "$R/R557-5/scripts/preservation_and_probe.py" "$T"
wait
