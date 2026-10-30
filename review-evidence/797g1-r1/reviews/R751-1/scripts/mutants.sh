#!/usr/bin/env bash
# Reviewer mutation probes for the two #797 generators. Each mutant edits one
# tracked file in place, runs one --check, and restores the file from HEAD.
# Usage: mutants.sh <repo-root> <python>   (prints one line per mutant)
set -u
REPO=$1
PY=$2
cd "$REPO" || exit 9

run() {  # id file sed-expr gate expect-description
    local id=$1 file=$2 expr=$3 gate=$4 want=$5
    cp "$file" "$file.orig-r751"
    sed -i -e "$expr" "$file"
    if cmp -s "$file" "$file.orig-r751"; then
        echo "$id: MUTATION DID NOT APPLY ($file)"
        mv "$file.orig-r751" "$file"
        return
    fi
    "$PY" $gate > "/tmp/r751-mutant-$id.log" 2>&1
    local rc=$?
    mv "$file.orig-r751" "$file"
    git checkout -q -- "$file"
    echo "$id: rc=$rc want $want :: $gate :: $(tail -1 /tmp/r751-mutant-$id.log | cut -c1-200)"
    rm -f "/tmp/r751-mutant-$id.log"
}

KR="sw/builder/gen_key_reference.py --check"
ED="docs/diagrams/endstation_definition.gen.py --check"
run K1 sw/builder/README-parameters.md 's/| optional | `115200` |/| optional | `9600` |/' "$KR" "1 (stale cell)"
run K2 sw/builder/endstation_builder.py 's/c.get("uart_baudrate", 115200)/c.get("uart_baudrate", 9600)/' "$KR" "non-zero (default moved)"
run K3 sw/builder/endstation_builder.py '1469s/1 <= ch <= 32/1 <= ch <= 16/' "$KR" "2 (range probe)"
run K4 sw/builder/endstation_builder.py '3742s/> 63/> 62/' "$KR" "2 (length probe)"
run K5 avdecc/aem_descriptors.py '156s/"Clock Reference Format"/"CRF Domain"/' "$KR" "non-zero (names default moved)"
run D1 docs/guides/DEFINING_THE_END_STATION.md 's/AUDIO_CLUSTER 17 to 24/AUDIO_CLUSTER 17 to 23/' "$ED" "1 (stale tree)"
run D2 sw/litex/sweep.sh 's/sweep_opts_/sweepopts_/g' "$ED" "2 (consumer label)"
run D3 avdecc/aem_descriptors.py '156s/"Clock Reference Format"/"CRF Domain"/' "$ED" "1 (tree label from overlay)"
run D4 hdl/milan/KL_nvm_backend.sv '248s/N_NAME_MAX_C = 128/N_NAME_MAX_C = 512/' "$ED" "2 (widest-probe claim)"
run D5 docs/guides/DEFINING_THE_END_STATION.md 's/| `endstation_ax7101_1x1_tdm8.yaml` | 1x1 | 25 | LUT 79.4 % | TIGHT |/| `endstation_ax7101_1x1_tdm8.yaml` | 1x1 | 25 | LUT 79.4 % | OK |/' "$ED" "1 (stale resources)"
run D6 docs/guides/DEFINING_THE_END_STATION.md 's/^| `entity_model_id` | `0x001BC5C1935893E1`/| `entity_model_id` | `0x001BC5C1935893E2`/' "$ED" "1 (stale moves)"
