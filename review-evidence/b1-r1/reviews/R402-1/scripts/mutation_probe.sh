#!/usr/bin/env bash
# Plant one wrong cell per probe in a scratch copy of the two pages and require rederive.py to fail.
# usage: mutation_probe.sh <repo-root> <packet-root> <scratch-dir>
set -u
R=$1; PK=$2; S=$3
here=$(cd "$(dirname "$0")" && pwd)
probe() {
  local name=$1 page=$2 old=$3 new=$4
  rm -rf "$S/$name"; mkdir -p "$S/$name/docs/findings"
  cp "$R/docs/findings/599_394_E1_LINK_CYCLES.md" "$R/docs/findings/387_SOFTWARE_GM_STEP.md" "$S/$name/docs/findings/"
  python3 - "$S/$name/docs/findings/$page" "$old" "$new" <<'PY'
import sys
p, o, n = sys.argv[1:]
t = open(p).read(); assert t.count(o) >= 1, o
open(p, "w").write(t.replace(o, n, 1))
PY
  python3 -B "$here/rederive.py" "$PK" "$S/$name" > "$S/$name.out" 2>&1
  rc=$?
  echo "probe $name: rederive rc=$rc ($(grep -c '^FAIL' "$S/$name.out") FAIL lines: $(grep '^FAIL' "$S/$name.out" | head -1))"
  [ $rc -ne 0 ]
}
fails=0
probe mac_down 599_394_E1_LINK_CYCLES.md "| 3 | 20.88 | 2.31-2.56 |" "| 3 | 20.88 | 2.06-2.31 |" || fails=$((fails+1))
probe link_delta 599_394_E1_LINK_CYCLES.md "| 7 | 20.88 | 1.81-2.06 | 36.59-36.84 | +1 / +1 |" "| 7 | 20.88 | 1.81-2.06 | 36.59-36.84 | +2 / +1 |" || fails=$((fails+1))
probe recovery 599_394_E1_LINK_CYCLES.md "| 1.786 |" "| 5.786 |" || fails=$((fails+1))
probe step_ms 387_SOFTWARE_GM_STEP.md "| 3 | release | -10.004 ms |" "| 3 | release | -1.004 ms |" || fails=$((fails+1))
probe ascap 387_SOFTWARE_GM_STEP.md "| 4.78-6.78 |" "| 4.78-5.78 |" || fails=$((fails+1))
probe mr 387_SOFTWARE_GM_STEP.md "| 4.03-6.03 | 0 / 0 |" "| 4.03-6.03 | 1 / 0 |" || fails=$((fails+1))
echo "probes not killed: $fails"
exit $fails
