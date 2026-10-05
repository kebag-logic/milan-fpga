#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# builder_fragment_identity.sh - reviewer probe for PR #668 (#665 F0).
# The end-station builder reads sw/litex/milan_soc.py; run it for every shipped
# config with the BASE milan_soc.py in place and then with the HEAD one, in one
# disposable tree, and compare every generated file byte for byte (the path of
# the output root is the only normalisation). Also records git status after
# each run, so a tracked generated fragment that moved would show.
# usage: builder_fragment_identity.sh <tree> <base-sha> <outdir> <python>
set -u
T=$(cd "$1" && pwd); B=$2; O=$3; PY=$4
CFGS="endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8 endstation_arty_4x4 endstation_arty_8ch endstation_arty_current"
mkdir -p "$O"
cp "$T/sw/litex/milan_soc.py" "$O/milan_soc.head.py"
git -C "$T" show "$B:sw/litex/milan_soc.py" > "$O/milan_soc.base.py"
for side in base head; do
    cp "$O/milan_soc.$side.py" "$T/sw/litex/milan_soc.py"
    for cfg in $CFGS; do
        (cd "$T" && "$PY" sw/builder/endstation_builder.py "configs/$cfg.yaml" -o "$O/$side") > "$O/$side.$cfg.log" 2>&1
        echo "$side $cfg rc=$?"
    done
    git -C "$T" status --porcelain -- . ':!sw/litex/milan_soc.py' > "$O/$side.status"
done
cp "$O/milan_soc.head.py" "$T/sw/litex/milan_soc.py"
git -C "$T" diff --quiet -- sw/litex/milan_soc.py && echo "head milan_soc.py restored"
echo "status after base run: $(wc -l < "$O/base.status") entries; after head run: $(wc -l < "$O/head.status") entries"
n=0; d=0
while IFS= read -r f; do
    n=$((n+1))
    if ! cmp -s <(sed "s#$O/base#OUT#g" "$O/base/$f") <(sed "s#$O/head#OUT#g" "$O/head/$f"); then d=$((d+1)); echo "DIFFERS: $f"; fi
done < <(cd "$O/base" && find . -type f | sort)
m=$(cd "$O/head" && find . -type f | wc -l)
echo "builder outputs: $n files at base, $m at head, $d differ"
