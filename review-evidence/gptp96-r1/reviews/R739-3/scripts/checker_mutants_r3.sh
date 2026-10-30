#!/usr/bin/env bash
# Weaken scripts/check_docs.py in disposable copies and run --selftest on each.
# Two sets:
#  - silence_*: the findings.append/extend call that emits one finding of the
#    status, constants, copy or ROM rule is made a no-op;
#  - weak_*: the eight weakenings the PR body names.
# Usage: checker_mutants_r3.sh <clone> <scratch-dir> <out-file> [jobs]
set -u
SRC=$(cd "$1" && pwd); WORK=$2; OUT=$3; JOBS=${4:-16}
mkdir -p "$WORK"
SELF=$(readlink -f "$0")

if [ "${MUT:-}" != "" ]; then
  t="$WORK/m-$MUT"; rm -rf "$t"; mkdir -p "$t"; git -C "$SRC" archive HEAD | tar -x -C "$t"
  python3 -I - "$t/scripts/check_docs.py" "$MUT" <<'PY' || { printf '%-34s ANCHOR MISSED\n' "$MUT"; exit 0; }
import sys
path, name = sys.argv[1:]
s = open(path, encoding="utf-8").read()
silence = {
    "silence_status_duplicate": "{STATUS_PAGE}: duplicate status row",
    "silence_status_wrong": "status {status!r}, expected",
    "silence_status_missing_page": "status row names a missing page",
    "silence_status_no_rows": "no document status rows",
    "silence_status_no_history_row": "no status row for {HISTORY_ROW}",
    "silence_status_unlisted": "no status row for {relative}",
    "silence_const_duplicate": "{CONSTANTS_PAGE}: duplicate constant row",
    "silence_const_not_generator": "is not a generator constant",
    "silence_const_not_decimal": "is not a plain decimal",
    "silence_const_drift": "generator has {actual}",
    "silence_const_no_rows": "no protocol constant rows",
    "silence_const_missing_row": "no protocol constant row for {name}",
    "silence_copy": "link its constants row",
    "silence_rom_duplicate": "duplicate ROM budget row",
    "silence_rom_not_n_of_m": "is not plain 'N of M'",
    "silence_rom_counts_not_decimal": "counts are not plain decimals",
    "silence_rom_drift": "generator builds",
    "silence_rom_missing_row": "no ROM budget row for the",
}
weak = {
    "weak_no_const_duplicate": ('            findings.append(f"{CONSTANTS_PAGE}: duplicate constant row: {name}")',
                                '            pass'),
    "weak_no_required_set": ('        if name not in seen\n    )', '        if name not in seen and False\n    )'),
    "weak_decimal_accepts_any": ('    if DECIMAL_RE.fullmatch(cell) is None:\n        return None',
                                 '    if DECIMAL_RE.search(cell) is None:\n        return None\n    cell = DECIMAL_RE.search(cell).group(0)'),
    "weak_no_us_conversion": ('    if unit == "ns" and value % 1000 == 0:\n        numbers.append',
                              '    if False:\n        numbers.append'),
    "weak_no_minutes_word": ('        patterns += [rf"\\b{minutes}[\\s-]min", rf"\\b{word}[\\s-]minutes?\\b"]', '        pass'),
    "weak_home_never_exempt": ('            if fenced or home:', '            if fenced:'),
    "weak_no_rom_duplicate": ('        if image in seen:\n            findings.append(f"{ROM_PAGE}: duplicate ROM budget row: {image}")',
                              '        if image in seen:\n            pass'),
    "weak_no_lookbehind": ('        rf"(?<![\\d.,]){re.escape(text)}[\\s-]?{suffix}\\b"',
                           '        rf"{re.escape(text)}[\\s-]?{suffix}\\b"'),
}
if name in silence:
    anchor = silence[name]
    assert s.count(anchor) == 1, (name, s.count(anchor))
    at = s.index(anchor)
    call = max(s.rfind("findings.append(", 0, at), s.rfind("findings.extend(", 0, at))
    assert call >= 0 and at - call < 200, (name, at - call)
    s = s[:call] + "(lambda *_: None)(" + s[call + len("findings.append("):]
elif name in weak:
    old, new = weak[name]
    assert s.count(old) == 1, (name, s.count(old))
    s = s.replace(old, new)
elif name != "control":
    raise SystemExit(f"unknown mutant {name}")
open(path, "w", encoding="utf-8").write(s)
PY
  out=$(cd "$t" && python3 scripts/check_docs.py --selftest 2>&1); rc=$?
  gate=$(cd "$t" && python3 scripts/check_docs.py > /dev/null 2>&1; echo $?)
  printf '%-34s selftest rc=%s gate rc=%s | %s\n' "$MUT" "$rc" "$gate" "$(printf '%s' "$out" | tail -1)"
  rm -rf "$t"; exit 0
fi

{ echo control
  for m in status_duplicate status_wrong status_missing_page status_no_rows status_no_history_row \
           status_unlisted const_duplicate const_not_generator const_not_decimal const_drift \
           const_no_rows const_missing_row copy rom_duplicate rom_not_n_of_m \
           rom_counts_not_decimal rom_drift rom_missing_row; do echo "silence_$m"; done
  for m in no_const_duplicate no_required_set decimal_accepts_any no_us_conversion \
           no_minutes_word home_never_exempt no_rom_duplicate no_lookbehind; do echo "weak_$m"; done
} | xargs -P "$JOBS" -I{} env MUT={} bash "$SELF" "$SRC" "$WORK" /dev/null | sort > "$OUT"
cat "$OUT"
