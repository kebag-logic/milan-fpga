#!/usr/bin/env bash
# Planted probes against scripts/docs_inventory.py --check at the reviewed head.
# Usage: probe_gate.sh SOURCE_CLONE WORKDIR
# Each probe runs in a fresh `git clone --no-local` of SOURCE_CLONE at HEAD (no
# submodules), applies one mutation, runs --check and records rc and output.
set -u
src=$1; work=$2
mkdir -p "$work"
head=$(git -C "$src" rev-parse HEAD)
fresh() {  # fresh clone at the reviewed head in $work/$1
  rm -rf "$work/$1"
  git clone -q --no-local "$src" "$work/$1" && git -C "$work/$1" checkout -q --detach "$head"
}
probe() {  # name, expected rc, mutation command (run inside the clone)
  local name=$1 want=$2; shift 2
  fresh "$name"
  ( cd "$work/$name" && eval "$*" )
  local out rc
  out=$(cd "$work/$name" && python3 -I scripts/docs_inventory.py --check 2>&1); rc=$?
  local verdict=OK; [ "$rc" = "$want" ] || verdict=UNEXPECTED
  printf '%s\t%s\twant=%s\trc=%s\n' "$verdict" "$name" "$want" "$rc"
  printf '%s\n' "$out" | sed 's/^/    /' | head -4
  rm -rf "${work:?}/$name"
}
probe p00-unchanged 0 'true'
probe p01-stale-page-append 1 'echo "planted line" >> docs/guides/README.md'
probe p02-stale-page-heading 1 'sed -i "1s/^# .*/# Planted heading/" docs/guides/README.md'
probe p03-edited-finding-quote 1 "python3 -I -c \"import json;p='scripts/docs_inventory.json';d=json.load(open(p));d['findings'][4]['quote']=d['findings'][4]['quote'].replace('steerability','steering');open(p,'w').write(json.dumps(d,indent=1,ensure_ascii=False)+'\n')\""
probe p04-edited-finding-source 1 "python3 -I -c \"import json;p='scripts/docs_inventory.json';d=json.load(open(p));d['findings'][0]['source']+=' planted';open(p,'w').write(json.dumps(d,indent=1,ensure_ascii=False)+'\n')\""
probe p05-fixed-statement-on-page 1 'sed -i "s/ADP, ACMP, AECP, MAAP and SRP default to bare-metal firmware./ADP, ACMP, AECP, MAAP and SRP move to bare-metal firmware under Mark II./" README.md'
probe p06-hand-edit-status-cell 1 'sed -i "0,/| current | no recorded contradiction |/s//| stale | no recorded contradiction |/" docs/DOCUMENTATION_AUDIT.md'
probe p07-hand-edit-quote-in-page 1 'sed -i "s/is \*\*steerability\*\*/is **steering**/" docs/DOCUMENTATION_AUDIT.md'
probe p08-untracked-md-ignored 0 'echo "# untracked" > docs/guides/UNTRACKED.md'
probe p09-new-tracked-md 1 'echo "# added" > docs/guides/ADDED.md && git add docs/guides/ADDED.md'
probe p10-tracked-md-deleted 1 'rm docs/guides/PROJECT_MANAGER.md'
probe p11-untracked-build-output-ignored 0 'mkdir -p sw/builder/out/x && echo "# build" > sw/builder/out/x/README.md'
probe p12-malformed-data 2 'printf "{" > scripts/docs_inventory.json'
probe p13-finding-on-untracked-page 2 "python3 -I -c \"import json;p='scripts/docs_inventory.json';d=json.load(open(p));d['findings'][0]['page']='docs/NOPE.md';open(p,'w').write(json.dumps(d,indent=1))\""
probe p14-same-length-body-edit 0 'sed -i "s/Use this path when embedding the datapath./Use this path when embedding the data path./" docs/guides/SYSTEM_INTEGRATOR.md'
