#!/usr/bin/env bash
# Planted probes of the cross-page rule on the real tree. Usage: probe_cross_page.sh LANE WORKDIR
# Each probe: a fresh `git clone --no-local` at HEAD (no submodules), one mutation, then the gate.
set -u
src=$1; work=$2
mkdir -p "$work"
head=$(git -C "$src" rev-parse HEAD)
G=scripts/docs_inventory.py
A=docs/DOCUMENTATION_AUDIT.md
fresh() { rm -rf "$work/c"; git clone -q --no-local "$src" "$work/c" && git -C "$work/c" checkout -q --detach "$head"; }
gate() { python3 -I $G "$@" 2>&1 | cut -c1-150 | head -3; echo "    ${1} rc=${PIPESTATUS[0]}"; }
echo "head $head"
echo "== p00 unchanged tree"; fresh; ( cd "$work/c"; gate --check )
echo "== p01 planted stale page: one added line on docs/guides/README.md"; fresh
( cd "$work/c"; echo "Added line." >> docs/guides/README.md; gate --check )
echo "== p02 the README statement copied, wrapped, onto docs/guides/SYSTEM_INTEGRATOR.md"; fresh
( cd "$work/c"; printf '\n- ADP, ACMP, AECP, MAAP and **SRP default\n  to** bare-metal firmware.\n' >> docs/guides/SYSTEM_INTEGRATOR.md
  gate --check; gate --write; gate --check
  grep -c 'D0-001 | \[docs/guides/SYSTEM_INTEGRATOR.md\]' $A; grep -F '[docs/guides/SYSTEM_INTEGRATOR.md](guides/SYSTEM_INTEGRATOR.md) |' $A | cut -d'|' -f7-8 | head -1 )
echo "== p03 the REQUIREMENTS.md copy row deleted by hand"; fresh
( cd "$work/c"; sed -i '/^| D0-001 | \[REQUIREMENTS.md\]/d' $A; gate --check )
echo "== p04 REQUIREMENTS.md marked current by hand"; fresh
( cd "$work/c"; python3 -I - <<'PY'
import re
p='docs/DOCUMENTATION_AUDIT.md'; s=open(p,encoding='utf-8').read()
n=re.sub(r'(\[REQUIREMENTS\.md\]\(\.\./REQUIREMENTS\.md\) \|[^\n]*?\| )stale \| 1 finding\(s\): D0-001 \|', r'\1current | no recorded contradiction |', s, count=1)
assert n!=s; open(p,'w',encoding='utf-8').write(n)
PY
  gate --check )
echo "== p05 the named mutant: cross-page search disabled"; fresh
( cd "$work/c"; python3 -I - <<'PY'
p='scripts/docs_inventory.py'; s=open(p,encoding='utf-8').read()
o='    for finding in findings + copies(findings, texts):'; assert s.count(o)==1
open(p,'w',encoding='utf-8').write(s.replace(o,'    for finding in findings:'))
PY
  gate --check; gate --write; gate --check; gate --selftest )
echo "== p06 the requirements statement reworded: the row leaves and the page recovers"; fresh
( cd "$work/c"; sed -i 's/The Mark II default places them on the bare-metal core\./The placement is open./' REQUIREMENTS.md; gate --check; gate --write; gate --check
  grep -c 'D0-001 | \[REQUIREMENTS.md\]' $A; grep -F '| [REQUIREMENTS.md](../REQUIREMENTS.md) |' $A | cut -d'|' -f7-8 | head -1 )
echo "== p07 a paraphrase with no recorded spelling is not found (the rule's stated limit)"; fresh
( cd "$work/c"; echo "Placement defaults to the bare-metal core." >> docs/guides/SYSTEM_INTEGRATOR.md; gate --write; grep -c 'D0-001 | \[docs/guides/SYSTEM_INTEGRATOR.md\]' $A )
rm -rf "$work/c"
