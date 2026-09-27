#!/bin/sh
# R328-4: re-check each prior public review finding on PR #579 at the candidate.
# Usage: prior_findings_check.sh <candidate-clone> <pp_shadow_default.log> <pending_mutant.log>
set -u
C=$1; PPS=$2; MUT=$3
cd "$C" || exit 2
H=f80525e695ce7937ba1a2c1caa01ec9cdde93904
S=90ab4a3da5b676f90b768b4f22b77ce7d0bd911d
show() { printf '\n== %s\n' "$1"; }
show "blob identity candidate vs source head for finding-bearing files"
for f in CHANGELOG.md docs/reference/SUBMODULES.md docs/design/SAVED_STATE_MATERIALIZATION.md \
         docs/design/SAVED_STATE_FASTCONNECT.md tb/verilator/pp_shadow/sim_main.cpp \
         tb/verilator/pp_shadow/README.md hdl/milan/KL_pp_shadow.sv hdl/milan/milan_datapath.sv \
         hdl/common/csr/milan_csr.sv docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md docs/testing/TESTING.md; do
  a=$(git rev-parse "$S:$f"); b=$(git rev-parse "$H:$f")
  [ "$a" = "$b" ] && echo "EQ   $f" || echo "DIFF $f (predecessor overlap)"
done
show "R328-1 F1 = R329-1 F2: refused-at-validation control (harness log)"
grep -E '^\s*\[(PASS|FAIL)\] K12 refused record' "$PPS" | sort | uniq -c
show "R328-1 F2: MATERIALIZATION section 1 current trigger"
sed -n 127,143p docs/design/SAVED_STATE_MATERIALIZATION.md
show "R328-1 F3: TESTING campaign row"
grep -n 'pp_shadow pending-mutant' docs/testing/TESTING.md
show "R328-1 S1 = R329-1 F3: map pulse requires an actual change"
sed -n 4269,4271p hdl/milan/milan_datapath.sv
grep -E '^\s*\[(PASS|FAIL)\] K12 duplicate' "$PPS" | sed -E 's/ +got=.*//' | sort | uniq -c
printf 'tree hits for "conservative duplicate": %s\n' "$(git grep -i -c 'conservative duplicate' $H -- . ':!protocol-processor' | wc -l)"
show "R328-1 S2: storage-anchored observer (harness unchanged vs source head: see blob identity)"
show "R329-1 F1: REMOVE controls and mutant kills"
grep -E '^\s*\[(PASS|FAIL)\] K12 remove' "$PPS" | sed -E 's/ +got=.*//' | sort | uniq -c | head -20
grep -E '^\s*\[FAIL\] K12 remove' "$MUT" | sed -E 's/ +got=.*//' | sort | uniq -c
show "R328-2 F1 = R329-2 F1: CHANGELOG and SUBMODULES trigger text"
sed -n 36,44p CHANGELOG.md
sed -n 57,62p docs/reference/SUBMODULES.md
printf 'tree hits for "every commit beat": %s\n' "$(git grep -i -c 'every commit beat' $H -- . ':!protocol-processor' | wc -l)"
show "R328-2 S1: partial-refusal controls"
grep -E '^\s*\[(PASS|FAIL)\] K12 partial refusal' "$PPS" | sed -E 's/ +got=.*//' | sort | uniq -c
show "R328-2 S2: SNAPSHOT section 11 map row wording"
grep -n 'from the first actual write' docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md
show "R329-3 F1 / S1: MATERIALIZATION UNRESOLVED item and history labels"
grep -n -E 'RESOLVED by #502|[Hh]istorical' docs/design/SAVED_STATE_MATERIALIZATION.md | head -12
show "R328-3 S1 / R329-4 S1: case-tagged refusal and exact-record diagnostics"
grep -E '^\s*\[(PASS|FAIL)\] K12 [a-z ]*(input|output) GET_AUDIO_MAP exact record' "$PPS" | sed -E 's/ +got=.*//' | sort | uniq -c
show "R329-4 F1: SNAPSHOT section 13 current parent use"
grep -n -E 'Current parent use|pend_i = aecp_dyn_dirty_o|Original parent use' docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md
git grep -n -E 'pend_i *=|D2 sticky|D2 bit' $H -- . ':!protocol-processor' | cut -c1-200
show "R329-4 S2: milan_csr.sv comment wrap"
sed -n 195,199p hdl/common/csr/milan_csr.sv
show "R329-5 S1-S4 (optional) at candidate"
sed -n 1697,1698p docs/design/SAVED_STATE_MATERIALIZATION.md | cut -c1-200
sed -n 1447p tb/verilator/pp_shadow/sim_main.cpp
sed -n 1378,1380p docs/design/SAVED_STATE_FASTCONNECT.md
grep -n 'are now REPORTED, because donor' docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md
