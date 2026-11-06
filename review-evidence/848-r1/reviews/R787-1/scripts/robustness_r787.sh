#!/usr/bin/env bash
# usage: robustness_r787.sh <disposable clone at head> <base sha> <head sha>
# Edge probes of --check and --findings-dir, then the two-branch merge the issue exists for, at base and at head.
set -u
cd "$1"; BASE=$2; HEAD=$3; A=docs/DOCUMENTATION_AUDIT.md
chk(){ python3 -I scripts/docs_inventory.py --check 2>&1 | head -1 | cut -c1-110; echo "  $1: rc=${PIPESTATUS[0]}"; }
reset(){ git checkout -q -- . ; git clean -fdq docs scripts; }
chk "baseline"
rm "$A"; chk "audit page deleted"; reset
: > "$A"; chk "audit page emptied"; reset
git show "$BASE:$A" > "$A"; chk "old-format page under the new generator"; reset
sed -i '0,/| on page |/s//| 7 |/' "$A"; chk "a line number hand-written back into Located"; reset
sed -i '0,/| re-verify: quote not found |/s//| on page |/' "$A"; chk "a lost statement hand-marked on page"; reset
python3 -I - <<'PY'
import json,re
p='scripts/docs_inventory.json'; d=json.load(open(p)); d['findings'].pop(); json.dump(d,open(p,'w'))
PY
chk "a finding removed from the data file"; reset
python3 -I - <<'PY'
import json
p='scripts/docs_inventory.json'; d=json.load(open(p))
d['findings'].append({"id":"D0-999","page":"README.md","quote":"Milan","source":"probe","correction":"probe"}); json.dump(d,open(p,'w'))
PY
chk "a finding added to the data file"; reset
printf 'x\n' >> README.md; printf '# Probe | with a pipe\n\nAudience: a | b\n' > docs/ZZ_PROBE.md; git add docs/ZZ_PROBE.md
python3 -I scripts/docs_inventory.py --write >/dev/null; chk "a page whose title and audience carry a pipe, regenerated"
grep -n 'ZZ_PROBE' "$A" | cut -c1-140
python3 -I - <<'PY'
import importlib.util,sys
s=importlib.util.spec_from_file_location("inv","scripts/docs_inventory.py"); m=importlib.util.module_from_spec(s); sys.modules["inv"]=m; s.loader.exec_module(m)
row=[r for r in open("docs/DOCUMENTATION_AUDIT.md") if "ZZ_PROBE" in r and r.startswith("| [")][0]
print("  piped row cells:",len(m.cells(row.rstrip("\n"))),"status cell:",m.cells(row.rstrip("\n"))[4])
PY
git reset -q --hard; git clean -fdq docs scripts
d=$(mktemp -d -p "$PWD/.." r787fd.XXXX); python3 -I scripts/docs_inventory.py --findings-dir "$d/nested/lanes" | wc -l; echo "  findings-dir into a new nested directory: rc=$?"; rm -rf "$d"
python3 -I - <<'PY'
import json
p='scripts/docs_inventory.json'; d=json.load(open(p)); d['findings']=[]; json.dump(d,open(p,'w'))
PY
d=$(mktemp -d -p "$PWD/.." r787fd.XXXX); python3 -I scripts/docs_inventory.py --findings-dir "$d/l"; echo "  findings-dir with no findings: rc=$? files=$(ls "$d/l" | wc -l)"; rm -rf "$d"; reset
for side in base head; do
  sha=$BASE; [ "$side" = head ] && sha=$HEAD
  git checkout -q --detach "$sha"; git branch -qf p1 "$sha"; git branch -qf p2 "$sha"
  git checkout -q p1; printf '\nAdded by the first change.\n' >> QUICKSTART.md; python3 -I scripts/docs_inventory.py --write >/dev/null; git add -A; git -c user.name=p -c user.email=p@example.invalid commit -qm one
  git checkout -q p2; printf '\nAdded by the second change.\n' >> THIRD_PARTY.md; python3 -I scripts/docs_inventory.py --write >/dev/null; git add -A; git -c user.name=p -c user.email=p@example.invalid commit -qm two
  git -c user.name=p -c user.email=p@example.invalid merge -q --no-edit p1 >/dev/null 2>&1; m=$?
  echo "$side: audit page touched by the two changes: $(git diff --name-only "$sha" p1 p2 2>/dev/null | grep -c DOCUMENTATION_AUDIT); merge rc=$m; conflicted: $(git diff --name-only --diff-filter=U | tr '\n' ' ')"
  if [ "$m" = 0 ]; then python3 -I scripts/docs_inventory.py --check | head -1 | cut -c1-100; fi
  git merge --abort 2>/dev/null; git reset -q --hard; git checkout -q --detach "$HEAD"; git branch -qD p1 p2
done
git status --short | wc -l
