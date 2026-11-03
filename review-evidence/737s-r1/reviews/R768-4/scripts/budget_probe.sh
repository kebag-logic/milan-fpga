#!/usr/bin/env bash
# Budget boundary probe on a disposable copy of the head's scripts and LiteX tree.
# usage: budget_probe.sh <repo> <scratchdir>
set -u
repo=$1; work=$2
rm -rf "$work"; mkdir -p "$work"
git -C "$repo" archive HEAD scripts sw/litex | tar -x -C "$work"
f="$work/scripts/ci_litex_legs.py"
orig=$(sha256sum "$f" | cut -d' ' -f1)
try() { echo "== $1"; (cd "$work" && python3 scripts/ci_litex_legs.py legs); echo "rc=$?"; }
set_member() { sed -i -E "/^LARGEST = \{/,/^}/ s/(    \"$1\": )[0-9]+,/\1$2,/" "$f"; grep -n "    \"$1\":" "$f" | tail -1; }
python3 -I -c "import sys; sys.path.insert(0,'$work/scripts'); import ci_litex_legs as m; print('LEG_BUDGET', m.LEG_BUDGET, '=', m.JOB_LIMIT, '-', m.HEADROOM, '-', m.SETUP, '-', m.COLD_VERILATOR, '-', m.SELFTEST)"
git -C "$repo" show HEAD:scripts/ci_litex_legs.py > "$f.orig"
for v in 926 927; do cp "$f.orig" "$f"; set_member test_gptp_tx_timestamp $v; try "leg 0 gptp LARGEST=$v"; done
# leg 2 boundary: ctrl 284 + soc -> 926 / 927
for v in 642 643; do cp "$f.orig" "$f"; set_member test_soc_timing_cuts $v; try "leg 2 soc LARGEST=$v (leg 2 = $((284+v)))"; done
# ruling's 927 budget (self-test 3): gptp 927 then fits
cp "$f.orig" "$f"; sed -i -E 's/^SELFTEST = 4$/SELFTEST = 3/' "$f"; grep -n '^SELFTEST' "$f"; set_member test_gptp_tx_timestamp 927; try "SELFTEST=3, gptp LARGEST=927"
cp "$f.orig" "$f"; echo "restored $( [ "$(sha256sum "$f" | cut -d' ' -f1)" = "$orig" ] && echo equal || echo DIFFERENT)"; try restored
