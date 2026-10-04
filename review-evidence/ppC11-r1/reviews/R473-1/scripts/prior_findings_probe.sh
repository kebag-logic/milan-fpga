#!/usr/bin/env bash
# Independent reproduction of the prior public findings F1 and F2 at exact head.
set -u
REPO=$1; S=$2; HEAD_SHA=91cef52b3c56cc69f66966b004782a69d2940a46
rm -rf "$S"; mkdir -p "$S"
ids_plant() { # tag, text appended to 08_timing.md
  local d="$S/$1"; git clone -q --no-checkout "$REPO" "$d"; git -C "$d" checkout -q --detach $HEAD_SHA
  printf '%s\n' "$2" >> "$d/docs/architecture/08_timing.md"
  python3 "$d/scripts/check-ids.py" --root "$d" | tail -2; echo "F1 plant $1 [$2]: rc=${PIPESTATUS[0]}"
}
ids_plant hyph-brace   'T-NVM-{RS-DEADLINE, RS-TYPO}'
ids_plant plain-brace  'T-MRP-{JOIN, TYPO}'
ids_plant lower-suffix 'the P-TX-shaped pool'
ids_plant lower-suffix-T 'a T-NOPE-ish timer'
# F2: figure self-test against three more mutants (dropped foreignObject check,
# root tag unchecked, empty inventory accepted)
src="$REPO/scripts/check-figures.py"
mut() { # tag, old, new
  local f="$S/fig-$1.py"
  python3 - "$src" "$f" "$2" "$3" <<'PY'
import sys
s = open(sys.argv[1]).read(); old, new = sys.argv[3], sys.argv[4]
assert s.count(old) == 1, old
open(sys.argv[2], "w").write(s.replace(old, new))
PY
  python3 "$f" --selftest > "$S/fig-$1.out" 2>&1; local rc=$?
  echo "F2 mutant $1: selftest rc=$rc ($( [ $rc = 0 ] && echo SURVIVED || echo KILLED))"
}
mut foreignobject-unchecked 'for tag in ("image", "foreignObject"):' 'for tag in ("image",):'
mut root-unchecked 'if svg.tag != f"{SVG_NS}svg":' 'if False:'
mut empty-inventory-ok 'if not names:
        raise ValueError(f"{INVENTORY}: the hand-authored inventory lists no SVG")' 'if False:
        raise ValueError(f"{INVENTORY}: the hand-authored inventory lists no SVG")'
# the production gate on the real tree for the same three faults
fig_plant() { local d="$S/g-$1"; git clone -q --no-checkout "$REPO" "$d"; git -C "$d" checkout -q --detach $HEAD_SHA; (cd "$d" && bash -c "$2"); python3 "$d/scripts/check-figures.py" --root "$d" | tail -1; echo "F2 tree plant $1: rc=${PIPESTATUS[0]}"; }
fig_plant foreignobject 'sed -i "0,/<rect/s//<foreignObject width=\"1\" height=\"1\"\/><rect/" docs/diagrams/23-bringup-decision.svg'
fig_plant wrong-root    'sed -i "0,/<svg /s//<svgx /; s#</svg>#</svgx>#" docs/diagrams/20-rtl-dataflow.svg'
fig_plant empty-inventory 'sed -i "/^| \`2[0-4]-.*\.svg\`/d" docs/diagrams/README.md'
