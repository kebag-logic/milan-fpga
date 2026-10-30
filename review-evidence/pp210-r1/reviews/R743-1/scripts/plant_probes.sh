#!/usr/bin/env bash
# Plant faults one at a time in a disposable clone of the head and record each
# gate's rc and diagnostic; every plant is reverted with git before the next.
# usage: plant_probes.sh <probe-clone> <outfile>
set -u
c=$1; out=$2; cd "$c" || exit 2
: >"$out"
inv() { python3 scripts/check-doc-inventory.py 2>&1 | grep -E 'FAIL|inventory:' | head -4; echo "  rc=${PIPESTATUS[0]}"; }
lnk() { python3 scripts/check-links.py 2>&1 | tail -3; echo "  rc=${PIPESTATUS[0]}"; }
reset() { git checkout -q -- . && git clean -qfd -e .venv-wavedrom; }
case_() { echo "### $1" >>"$out"; }
case_ "P0 clean head: inventory"; inv >>"$out"
case_ "P0 clean head: links"; lnk >>"$out"
case_ "P1 stale entry: a row for a page that does not exist"
sed -i 's#^| \[`tb/ucpu/README.md`\].*#&\n| [`tb/gone/README.md`](../tb/gone/README.md) | x | verification | x | current | run 1 check |#' docs/INVENTORY.md
inv >>"$out"; reset
case_ "P2 stale entry: a tracked page deleted, its row kept"
git rm -q tb/prng/README.md; inv >>"$out"; git reset -q --hard
case_ "P3 missing file: new untracked page with no row"
printf '# new\n' > docs/architecture/12_new.md; inv >>"$out"; reset
case_ "P4 missing file: new page staged (git add) with no row"
printf '# new\n' > tb/new_suite/README.md 2>/dev/null || { mkdir -p tb/new_suite; printf '# new\n' > tb/new_suite/README.md; }
git add tb/new_suite/README.md; inv >>"$out"; git reset -q --hard; reset
case_ "P5 superseded page marked current"
sed -i 's#^\(| \[`docs/10_RESOURCE_AND_EFFORT.md`\].*\)| superseded |#\1| current |#' docs/INVENTORY.md; inv >>"$out"; reset
case_ "P6 current page bannered superseded"
sed -i '2a > **Superseded** by nothing.' docs/guides/operator.md; inv >>"$out"; reset
case_ "P7 row without its link form (plain path cell)"
sed -i 's#^| \[`tb/prng/README.md`\](../tb/prng/README.md) |#| tb/prng/README.md |#' docs/INVENTORY.md; inv >>"$out"; reset
case_ "P8 status outside vocabulary"
sed -i 's#^\(| \[`tb/prng/README.md`\].*\)| current |#\1| fresh |#' docs/INVENTORY.md; inv >>"$out"; reset
case_ "P9 evidence emptied"
sed -i 's#^\(| \[`tb/prng/README.md`\].*| current |\).*#\1 |#' docs/INVENTORY.md; inv >>"$out"; reset
case_ "P10 duplicate row"
sed -i 's#^| \[`tb/prng/README.md`\].*#&\n&#' docs/INVENTORY.md; inv >>"$out"; reset
case_ "P11 (limit probe) row text names one file, its link points at another existing page"
sed -i 's#^| \[`tb/prng/README.md`\](../tb/prng/README.md)#| [`tb/prng/README.md`](../tb/ucpu/README.md)#' docs/INVENTORY.md; inv >>"$out"; lnk >>"$out"; reset
case_ "P12 (limit probe) a page with an upper-case .MD suffix"
printf '# x\n' > docs/NOTES.MD; inv >>"$out"; reset
case_ "L1 link checker: broken relative file link"
sed -i '$a See [gone](architecture/99_gone.md).' docs/README.md; lnk >>"$out"; reset
case_ "L2 link checker: broken anchor on an existing page"
sed -i '$a See [x](architecture/05_acmp_engine.md#no-such-heading).' docs/README.md; lnk >>"$out"; reset
case_ "L3 link checker: the old collapsed-anchor form re-planted"
sed -i '0,/#6bis-talker-side--stateless-responder/s//#6bis-talker-side-stateless-responder/' docs/guides/integrator.md; lnk >>"$out"; reset
case_ "L4 make check fails through the new inventory target"
printf '# new\n' > docs/architecture/12_new.md; make inventory >/dev/null 2>&1; echo "  make inventory rc=$?" >>"$out"; make check >/dev/null 2>&1; echo "  make check rc=$?" >>"$out"; reset
case_ "END state"; git status --porcelain >>"$out"; git rev-parse HEAD >>"$out"
