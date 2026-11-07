#!/bin/bash
# probes848d.sh <disposable clone> <head> <scratch>: the D0 class on the real tree, with and without Git history.
C=$1; H=$2; S=$3; cd "$C" || exit 2
export PYTHONDONTWRITEBYTECODE=1
reset() { git reset -q --hard "$H"; git clean -qfdx; }
A=docs/DOCUMENTATION_AUDIT.md
d0rows() { grep -cE '^\| \[.*\| D0 \| [^|]+ \|$' "$1/$A"; }
echo "# head $(git rev-parse HEAD)"
reset
python3 - <<'PY'
import json, re, subprocess
data = json.load(open("scripts/docs_inventory.json"))
listed = data["verified_pages"]
page = open("docs/DOCUMENTATION_AUDIT.md").read().split("\n")
rows = sorted(re.match(r"\| \[([^\]]+)\]", l).group(1) for l in page if l.startswith("| [") and re.search(r"\| D0 \| [^|]+ \|$", l))
base = set(subprocess.run(["git", "ls-tree", "-r", "--name-only", data["verified_at"]], capture_output=True, text=True, check=True).stdout.split("\n"))
print("listed", len(listed), "sorted", listed == sorted(listed), "unique", len(set(listed)) == len(listed))
print("D0 rows", len(rows), "equal to the list", rows == sorted(listed))
print("listed pages absent at the baseline", [p for p in listed if p not in base])
print("STRICTER_READINGS row:", [" | ".join(l.split(" | ")[-3:]) for l in page if l.startswith("| [docs/reference/STRICTER_READINGS.md]")])
print("lane figures:", [l for l in page if l.startswith(("| overview and guides |", "| reference |"))])
PY
for new in docs/reference/NEW_PAGE.md docs/guides/NEW_PAGE.md docs/integration/NEW_PAGE.md; do
  reset; printf '# New page\n' > "$new"; git add "$new"
  python3 scripts/docs_inventory.py --check >/dev/null; c1=$?
  python3 scripts/docs_inventory.py --write >/dev/null
  python3 scripts/docs_inventory.py --check >/dev/null; c2=$?
  echo "added $new: check rc=$c1, after --write rc=$c2, D0 rows $(d0rows .), row ends: $(grep -F "[$new]" $A | awk -F' \\| ' '{print $(NF-1)" | "$NF}')"
done
reset; git rm -q docs/reference/SUBMODULES.md; python3 scripts/docs_inventory.py --check | cut -c1-130; echo "listed page removed: check rc=${PIPESTATUS[0]}"
reset; git mv docs/reference/SUBMODULES.md docs/reference/SUBMODULES2.md; python3 scripts/docs_inventory.py --write | cut -c1-130; echo "listed page renamed: write rc=${PIPESTATUS[0]}"
reset
rm -rf "$S/archive"; mkdir -p "$S/archive"; git archive "$H" | tar -x -C "$S/archive"
(cd "$S/archive" && python3 scripts/docs_inventory.py --check; echo "archive tree, no Git metadata: check rc=$?, D0 rows $(grep -cE '^\| \[.*\| D0 \| [^|]+ \|$' $A)")
rm -rf "$S/shallow"; git clone -q --depth 1 "file://$C" "$S/shallow" 2>/dev/null
(cd "$S/shallow" && echo "shallow clone commits: $(git rev-list --count HEAD), baseline present: $(git cat-file -e 1e80128f 2>/dev/null && echo yes || echo no)"; python3 scripts/docs_inventory.py --check; echo "shallow clone: check rc=$?")
reset; echo "dirty after: $(git status --short | wc -l)"
