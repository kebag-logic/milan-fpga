#!/usr/bin/env bash
# Planted probes against the status rule and freshness gate of scripts/docs_inventory.py.
# Usage: probe_gate2.sh SOURCE_CLONE WORKDIR
# Each probe: fresh `git clone --no-local` at HEAD (no submodules), one mutation, then --check.
set -u
src=$1; work=$2
mkdir -p "$work"
head=$(git -C "$src" rev-parse HEAD)
G=scripts/docs_inventory.py
fresh() { rm -rf "$work/$1"; git clone -q --no-local "$src" "$work/$1" && git -C "$work/$1" checkout -q --detach "$head"; }
# Plant one finding on a current page (SYSTEM_INTEGRATOR.md), quote taken from that page.
PLANT="python3 -I -c \"import json;p='scripts/docs_inventory.json';d=json.load(open(p));d['findings'].append(dict(id='D0-999',page='docs/guides/SYSTEM_INTEGRATOR.md',quote='Use this path when embedding the datapath.',source='planted probe',correction='planted probe'));open(p,'w').write(json.dumps(d,indent=1,ensure_ascii=False)+'\n')\""
# Remove the status rule from the generator (a later regression).
NORULE="python3 -I -c \"p='$G';s=open(p).read();o='    if page_findings and state == \\\"current\\\":';assert s.count(o)==1;open(p,'w').write(s.replace(o,'    if False:'))\""
probe() {  # name, expected rc, mutation, [extra command after check]
  local name=$1 want=$2 mut=$3
  fresh "$name"
  ( cd "$work/$name" && eval "$mut" ) >/dev/null 2>&1
  local out rc
  out=$(cd "$work/$name" && python3 -I $G --check 2>&1); rc=$?
  local verdict=OK; [ "$rc" = "$want" ] || verdict=UNEXPECTED
  printf '%s\t%s\twant=%s\trc=%s\n' "$verdict" "$name" "$want" "$rc"
  printf '%s\n' "$out" | sed 's/^/    /' | head -5
  if [ $# -ge 4 ]; then ( cd "$work/$name" && eval "$4" ) 2>&1 | sed 's/^/    + /'; fi
  rm -rf "${work:?}/$name"
}
probe q00-unchanged 0 'true'
probe q01-plant-finding-on-current-page-no-regen 1 "$PLANT"
probe q02-plant-finding-then-write 0 "$PLANT && python3 -I $G --write" "grep -n '^| \[docs/guides/SYSTEM_INTEGRATOR.md\]' docs/DOCUMENTATION_AUDIT.md | cut -c1-40,200- ; grep -c 'D0-999' docs/DOCUMENTATION_AUDIT.md"
probe q03-hand-edit-stale-row-to-current 1 "sed -i 's#^\(| \[docs/reference/EGRESS_QUEUE_MAP.md\](reference/EGRESS_QUEUE_MAP.md) |.*\)| stale | \([0-9]* finding(s): [^|]*\)|#\1| current | no recorded contradiction |#' docs/DOCUMENTATION_AUDIT.md && grep -c 'EGRESS_QUEUE_MAP.md) .*| current |' docs/DOCUMENTATION_AUDIT.md"
probe q04-rule-lost-generator-plant-and-write 1 "$NORULE && $PLANT && python3 -I $G --write"
probe q05-rule-lost-generator-unchanged-data-write 1 "$NORULE && python3 -I $G --write"
probe q06-hand-edit-remove-finding-row-and-current 1 "sed -i '/^| D0-028 |/d;/^| D0-029 |/d' docs/DOCUMENTATION_AUDIT.md"
probe q07-plant-finding-quote-absent 1 "${PLANT/Use this path when embedding the datapath./No such sentence anywhere.}"
probe q08-plant-finding-quote-absent-then-write 0 "${PLANT/Use this path when embedding the datapath./No such sentence anywhere.} && python3 -I $G --write" "grep -n '^| D0-999 ' docs/DOCUMENTATION_AUDIT.md | cut -c1-120; grep -n '^| \[docs/guides/SYSTEM_INTEGRATOR.md\]' docs/DOCUMENTATION_AUDIT.md | grep -o '| stale | [^|]*|'"
probe q09-fixed-statement-on-qspi-page 1 "python3 -I -c \"import json;d=json.load(open('scripts/docs_inventory.json'));f=[x for x in d['findings'] if x['id']=='D0-024'][0];p=f['page'];s=open(p).read();assert f['quote'] in s;open(p,'w').write(s.replace(f['quote'],'X'*0+f['quote'][:-1]+' (fixed)'))\""
probe q10-hook-env-selftest 0 "git init -q --bare $work/dummy.git; git -C $work/dummy.git rev-parse --git-dir" "GIT_DIR=$work/dummy.git GIT_WORK_TREE=$work/dummy-wt python3 -I $G --selftest; echo selftest-under-hook-env rc=\$?; git --git-dir=$work/dummy.git ls-files | wc -l | sed 's/^/dummy index entries: /'; ls $work/dummy-wt 2>&1 | head -2"
rm -rf "$work/dummy.git" "$work/dummy-wt"
