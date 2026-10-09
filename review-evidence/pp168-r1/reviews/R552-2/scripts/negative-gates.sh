#!/usr/bin/env bash
# Negative controls for the docs gates that read the changed pages: each plant
# must make its gate fail (rc != 0), so a pass at the head is meaningful.
#   N1 stale F07.6 render: restore fig-07-sinkrec.svg from the round base while
#      the WaveDrom source keeps the 16-bit layout -> wavedrom-check must fail
#   N2 dangling anchor: delete the new sec-02-avtp anchor that 05/07/integrator
#      link to -> links must fail
#   N3 stale 12-bit layout: restore the 12-bit + rsv WaveDrom source while the
#      SVG is the 16-bit render -> wavedrom-check must fail
# usage: negative-gates.sh SOURCE_REPO SCRATCH LOGDIR BASE_REV HEAD_REV
set -uo pipefail
src=$1; scratch=$2; out=$3; base=$4; head=$5
here=$(cd "$(dirname "$0")" && pwd)
export PATH="${WAVEDROM_VENV_BIN:?}:$PATH"
mkdir -p "$out"
run() { # name gate-target plant-cmd
  local name=$1 target=$2 plant=$3 t="$scratch/neg-$1"
  "$here/mkclone.sh" "$src" "$t" "$head" > "$out/neg-$name.log" 2>&1
  ( cd "$t" && eval "$plant" ) >> "$out/neg-$name.log" 2>&1
  git -C "$t" status --short >> "$out/neg-$name.log"
  ( cd "$t" && make "$target" ) >> "$out/neg-$name.log" 2>&1
  local rc=$?
  echo "$rc" > "$out/neg-$name.rc"
  if [ "$rc" -ne 0 ]; then echo "neg-$name: gate FAILED as required (rc $rc)"; else echo "neg-$name: gate PASSED - control not killed"; fi
}
run N1-stale-sinkrec-svg wavedrom-check \
  "git show $base:docs/diagrams/wavedrom/fig-07-sinkrec.svg > docs/diagrams/wavedrom/fig-07-sinkrec.svg"
run N2-dangling-avtp-anchor links \
  "sed -i '/<a id=\"sec-02-avtp\"><\/a>/d' docs/architecture/02_interfaces.md"
run N3-stale-12bit-source wavedrom-check \
  "python3 - <<'EOF'
from pathlib import Path
p = Path('docs/architecture/07_memory_maps.md')
s = p.read_text()
new = '  {\"bits\": 16, \"name\": \"settled vlan_id\"},\n'
old = '  {\"bits\": 12, \"name\": \"settled vlan_id\"},\n  {\"bits\": 4,  \"name\": \"rsv\"},\n'
assert s.count(new) == 1
p.write_text(s.replace(new, old))
EOF"
