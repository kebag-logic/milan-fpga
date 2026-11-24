#!/bin/bash
# verify.sh <tree> <workflow> <receipts-root> <outfile>: the aggregate job's "Require every gate exactly once" step.
set -u
S=$(dirname "$(readlink -f "$0")")/../scratch
tree=$1; wf=$2; root=$3; out=$4
if [ "$wf" = docs ]; then legs="docs-gates-0 docs-gates-1 docs-gates-2"; else legs="elaborate-gates-0 elaborate-gates-1 elaborate-gates-2 elaborate-gates-3 elaborate-gates-4"; fi
needs=$(for l in $legs; do printf '"%s":{"result":"success","outputs":{}},' "$l"; done)
export CI_GATE_NEEDS="{${needs%,}}"
cd "$tree"
sha=$(git rev-parse HEAD)
echo "tree=$tree head=$sha workflow=$wf submodule-protocol-processor=$(ls protocol-processor | wc -l) python=$($S/shim/python3 -V)"
rm -f "$out"
PATH=$S/shim:/usr/bin:/bin bash --noprofile --norc -e -c "python3 scripts/ci_gate_receipts.py verify --workflow $wf --root '$root' --head '$sha' --output '$out'"
echo "exit=$?"
