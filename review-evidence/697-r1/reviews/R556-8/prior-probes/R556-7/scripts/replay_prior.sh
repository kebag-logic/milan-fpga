#!/bin/sh
# Replay earlier public reviewer probes byte-unchanged against a fresh clone of the reviewed head.
# Script bytes are copied from the published packets and their sha256 recorded (out/provenance.sha256).
# Adaptations (invocation only): plant_tree_probe.sh pins its checkout commit, so a copy with the
# reviewed head id substituted runs (diff in out/plant_tree_probe.adapt.diff); R557-5 scripts are
# placed so their fixed relative clang18 directory resolves to this packet's Ubuntu clang-18 extraction.
# usage: replay_prior.sh REVIEWS_DIR HEAD_CLONE HEAD_SHA REPLAY_DIR CAMPAIGN_DIR  (env.sh loaded)
set -u
D=$1; H=$2; SHA=$3; R=$4; C=$5
rm -rf "$R"; mkdir -p "$R/out" "$R/s"
O=$R/out; T=$R/tree
git clone -q --no-hardlinks "$H" "$T" && git -C "$T" checkout -q --detach "$SHA"
echo "tree head: $(git -C "$T" rev-parse HEAD)" > "$O/tree.txt"
cp_unchanged() { mkdir -p "$(dirname "$R/s/$2")"; cp "$D/$1" "$R/s/$2"; (cd "$R/s" && sha256sum "$2") >> "$O/provenance.sha256"; sha256sum "$D/$1" | sed "s#  .*#  published:$1#" >> "$O/provenance.sha256"; }
cp_unchanged 697-r556-3-packet/scripts/comment_probes.py R556-3/comment_probes.py
cp_unchanged 697-r556-3-packet/scripts/needle_probes.py R556-3/needle_probes.py
cp_unchanged 697-r556-4-packet/scripts/comment_bypass_probe.py R556-4/comment_bypass_probe.py
cp_unchanged 697-r556-4-packet/scripts/needle_default_fragments.py R556-4/needle_default_fragments.py
cp_unchanged 697-r556-4-packet/scripts/needle_specificity.py R556-4/needle_specificity.py
cp_unchanged 697-r557-4-packet/scripts/full_comment_bypass.py R557-4/full_comment_bypass.py
cp_unchanged 697-r556-5-packet/probes/hidden_text_probe.py R556-5/hidden_text_probe.py
cp_unchanged 697-r556-5-packet/probes/plant_tree_probe.sh R556-5/plant_tree_probe.sh
cp_unchanged 697-r557-5-packet/scripts/independent_probes.py R557-5/scripts/independent_probes.py
cp_unchanged 697-r557-5-packet/scripts/preservation_and_probe.py R557-5/scripts/preservation_and_probe.py
cp_unchanged 697-r556-6-packet/scripts/r556_6_probes.py R556-6/r556_6_probes.py
cp_unchanged 697-r557-6-packet/scripts/independent_probes.py R557-6/scripts/independent_probes.py
cp_unchanged 697-r557-6-packet/scripts/full_assertion_probe.py R557-6/scripts/full_assertion_probe.py
mkdir -p "$R/s/R557-5/scratch" "$R/s/R557-5/receipts" "$R/s/R557-6/receipts"; ln -s "$PACKET/scratch/debs/x" "$R/s/R557-5/scratch/clang18"
sed "s/60c911b92825a720044e78bed540752c7dd0368e/$SHA/" "$R/s/R556-5/plant_tree_probe.sh" > "$R/plant_tree_probe.head.sh"
diff -u "$R/s/R556-5/plant_tree_probe.sh" "$R/plant_tree_probe.head.sh" > "$O/plant_tree_probe.adapt.diff"
job() { name=$1; shift; ( "$@" > "$O/$name.log" 2>&1; echo $? > "$O/$name.rc" ) & }
job R556-3_comment_probes python3 -B "$R/s/R556-3/comment_probes.py" "$T"
job R556-3_needle_probes python3 -B "$R/s/R556-3/needle_probes.py" "$T"
job R556-4_comment_bypass_probe python3 -B "$R/s/R556-4/comment_bypass_probe.py" "$T" "$R/w-bypass"
job R556-4_needle_default_fragments python3 -B "$R/s/R556-4/needle_default_fragments.py" "$T"
job R556-4_needle_specificity python3 -B "$R/s/R556-4/needle_specificity.py" "$T" "$C"
job R557-4_full_comment_bypass python3 -B "$R/s/R557-4/full_comment_bypass.py" --repo "$T" --work "$R/w-full" --output "$O/R557-4_full_comment_bypass.json"
job R556-5_hidden_text_probe python3 -B "$R/s/R556-5/hidden_text_probe.py" "$T" "$R/w-hidden"
job R556-5_plant_tree_probe sh "$R/plant_tree_probe.head.sh" "$T" "$R/w-plant"
job R557-5_independent_probes python3 -B "$R/s/R557-5/scripts/independent_probes.py" "$T"
job R557-5_preservation_and_probe python3 -B "$R/s/R557-5/scripts/preservation_and_probe.py" "$T"
job R557-6_independent_probes python3 -B "$R/s/R557-6/scripts/independent_probes.py" "$T" "$R/w-r557-6"
job R557-6_full_assertion_probe python3 -B "$R/s/R557-6/scripts/full_assertion_probe.py" "$T" "$R/s/R557-6"
wait
job R556-6_r556_6_probes python3 -B "$R/s/R556-6/r556_6_probes.py" "$T" "$R/w-r556-6"
wait
for f in "$O"/*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f")"; done
