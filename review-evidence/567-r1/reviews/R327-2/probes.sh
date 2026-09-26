#!/usr/bin/env bash
# R327-2 disposable probes. Usage: probes.sh <checkout> <python> <scratch-dir>
# Every mutation happens in a git-archive copy under <scratch-dir>; the checkout is read only.
set -u
REPO=${1:?checkout}; PY=${2:?python}; S=${3:?scratch}
cd "$REPO" || exit 2
HEAD=$(git rev-parse HEAD)

echo "## P1: the assigned 11-word S1 sentence against the unchanged style gate"
C="$S/probe_style"; rm -rf "$C"; mkdir -p "$C"; git archive HEAD | tar -x -C "$C"
( cd "$C" && "$PY" -B scripts/check_doc_style.py >/dev/null 2>&1; echo "control (head bytes) rc=$?" )
"$PY" - "$C/docs/reference/SUBMODULES.md" <<'EOF'
import sys; p=sys.argv[1]; t=open(p).read()
old="OOC synthesis requires ledger rows for the pin of record.\nRows must match that exact pin.\n"
new="OOC synthesis requires ledger rows for the exact pin of record.\n"
assert t.count(old)==1, "anchor"; open(p,"w").write(t.replace(old,new))
EOF
( cd "$C" && "$PY" -B scripts/check_doc_style.py 2>&1 | tail -n 3; echo "mutant (assigned sentence) rc=${PIPESTATUS[0]}" )

echo "## P2: ledger lookup exactly as ooc.sh performs it, keyed by the superproject gitlink"
PIN=$(git rev-parse :protocol-processor); SUBHEAD=$(git -C protocol-processor rev-parse HEAD)
echo "gitlink=$PIN checkout=$SUBHEAD"
for img in ltn_rom.hex ucode.hex; do
  new=$(awk -v p="$PIN" -v i="$img" '$1 == p && $2 == i { print $3; exit }' syn/yosys/rom_digests.tsv)
  old=$(awk -v p=990f96526bb89356c963a260ebbdcf2a77e6623a -v i="$img" '$1 == p && $2 == i { print $3; exit }' syn/yosys/rom_digests.tsv)
  n=$(awk -v p="$PIN" -v i="$img" '$1 == p && $2 == i' syn/yosys/rom_digests.tsv | wc -l)
  echo "$img pin_rows=$n pin=$new prev=$old $([ -n "$new" ] && [ "$new" = "$old" ] && echo MATCH || echo DIFFER)"
done
echo "mutant: ledger without the pin-of-record rows"
grep -v "^$PIN" syn/yosys/rom_digests.tsv > "$S/ledger_mutant.tsv"
r=$(awk -v p="$PIN" -v i=ucode.hex '$1 == p && $2 == i { print $3; exit }' "$S/ledger_mutant.tsv")
echo "lookup='${r}' -> $([ -z "$r" ] && echo 'EMPTY: ooc.sh refusal branch (no recorded content digest) would fire' || echo present)"

echo "## P3: processor sources feeding the ROMs and HDL across the pin move"
git -C protocol-processor diff --stat 990f96526bb89356c963a260ebbdcf2a77e6623a "$PIN" -- hdl/ ; echo "hdl diff rc=$? (empty stat = unchanged)"
echo "hdl trees: $(git -C protocol-processor rev-parse 990f96526bb89356c963a260ebbdcf2a77e6623a:hdl) $(git -C protocol-processor rev-parse "$PIN":hdl)"

echo "## P4: pinned permalink targets at README:552 versus the pin of record"
for f in docs/architecture/06_aecp_engine.md docs/architecture/05_acmp_engine.md; do
  a=$(git -C protocol-processor rev-parse "990f96526bb89356c963a260ebbdcf2a77e6623a:$f" 2>/dev/null || echo absent)
  b=$(git -C protocol-processor rev-parse "$PIN:$f" 2>/dev/null || echo absent)
  echo "$f old=$a new=$b $([ "$a" = "$b" ] && echo SAME || echo DIFFERENT)"
done
