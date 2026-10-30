#!/usr/bin/env bash
# Weaken scripts/check_docs.py in a disposable copy and confirm --selftest
# fails for each weakening. Usage: checker_mutants.sh <clone> <scratch-dir>
set -u
SRC=$1; WORK=$2; mkdir -p "$WORK"
fresh() { rm -rf "$WORK/t"; mkdir -p "$WORK/t"; git -C "$SRC" archive HEAD | tar -x -C "$WORK/t"; }
mut() { # name python-replace-old python-replace-new
  fresh
  python3 -I - "$WORK/t/scripts/check_docs.py" "$2" "$3" <<'PY'
import sys; p, old, new = sys.argv[1:]
s = open(p, encoding="utf-8").read()
assert s.count(old) == 1, ("anchor count", s.count(old), old)
open(p, "w", encoding="utf-8").write(s.replace(old, new))
PY
  [ $? -eq 0 ] || { echo "$1: ANCHOR MISSED"; return; }
  local out rc; out=$(cd "$WORK/t" && python3 scripts/check_docs.py --selftest 2>&1); rc=$?
  printf '%-32s selftest rc=%s | %s\n' "$1" "$rc" "$(printf '%s' "$out" | tail -1)"
}
fresh; out=$(cd "$WORK/t" && python3 scripts/check_docs.py --selftest 2>&1); echo "control_unmutated                selftest rc=$? | $out"
mut no_required_set '        if name not in seen
    )' '        if name not in seen and False
    )'
mut decimal_accepts_any '    if DECIMAL_RE.fullmatch(cell) is None:
        return None' '    if DECIMAL_RE.search(cell) is None:
        return None
    cell = DECIMAL_RE.search(cell).group(0)'
mut no_us_conversion '    if unit == "ns" and value % 1000 == 0:
        numbers.append' '    if False:
        numbers.append'
mut no_minutes_word '        patterns += [rf"\b{minutes}[\s-]min", rf"\b{word}[\s-]minutes?\b"]' '        pass'
mut home_never_exempt '            if fenced or home:' '            if fenced:'
mut no_rom_duplicate '        if image in seen:
            findings.append(f"{ROM_PAGE}: duplicate ROM budget row: {image}")' '        pass'
mut no_const_duplicate '            findings.append(f"{CONSTANTS_PAGE}: duplicate constant row: {name}")' '            pass'
mut no_lookbehind '        rf"(?<![\d.,]){re.escape(text)}[\s-]?{suffix}\b"' '        rf"{re.escape(text)}[\s-]?{suffix}\b"'
rm -rf "$WORK/t"
# The duplicate constants-row rule in the real tree, with the checker intact
# and with that rule removed: the intact gate must fail, and the weakened
# checker's selftest result shows whether any arm guards the rule.
fresh; sed -i 's/^| `SYNC_RTO_MS_C` | 375 |.*$/&\n&/' "$WORK/t/docs/INTEGRATION.md"
out=$(cd "$WORK/t" && python3 scripts/check_docs.py 2>&1); echo "dup_const_row_real_tree          gate rc=$? | $(printf '%s' "$out" | sed -n 2p)"
rm -rf "$WORK/t"
