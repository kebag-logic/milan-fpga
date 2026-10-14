#!/usr/bin/env bash
# Usage: probes.sh <disposable-clone> <receipt-dir>
# Each probe gets its own worktree of the disposable clone, applies one edit,
# and runs one gate. Expected rc is recorded beside the observed rc.
set -u
C=$1; OUT=$2; mkdir -p "$OUT"; cd "$C" || exit 2
HEAD=4c5d70b50230fbd5da347852d39daf7f23b3df0b; BASE=412e3f6c8c402bce63e94c291d2782b5579aaa1d
mk() { git worktree add -q --detach "wt-$1" "$2" >/dev/null 2>&1 || exit 3; echo "$C/wt-$1"; }
probe() { # name rev expect gate edit-command
  local n=$1 rev=$2 exp=$3 gate=$4 edit=$5 d
  d=$(mk "$n" "$rev")
  ( cd "$d" && bash -c "$edit" ) >"$OUT/$n.edit.log" 2>&1
  ( cd "$d" && git diff --stat && git diff ) >"$OUT/$n.diff" 2>&1
  ( cd "$d" && eval "$gate" ) >"$OUT/$n.log" 2>&1; local rc=$?
  echo "$n expect=$exp rc=$rc" >"$OUT/$n.rc"
}
SS='python3 scripts/suite_shards.py --selftest'
CK='python3 scripts/ci_events.py --check'
ST='python3 scripts/ci_events.py --selftest'
probe N1_base_selftest $BASE nonzero "$SS" 'true' &
probe N2_base_plus_step1_only $BASE nonzero "$SS" "sed -i 's/^    \"gptp_txts\": 72,/    \"gptp_tables\": 1800,\n    \"gptp_txts\": 72,/; s/^PROVISIONAL_SUITES: frozenset\[str\] = frozenset()/PROVISIONAL_SUITES: frozenset[str] = frozenset({\"gptp_tables\"})/' scripts/suite_shards.py" &
probe M1_drop_duration $HEAD nonzero "$SS" "sed -i '/^    \"gptp_tables\": 1800,/d' scripts/suite_shards.py" &
probe M2_figure_1799 $HEAD nonzero "$SS" "sed -i 's/^    \"gptp_tables\": 1800,/    \"gptp_tables\": 1799,/' scripts/suite_shards.py" &
probe M3_overhead_five $HEAD nonzero "$SS" "sed -i 's/^WORKER_OVERHEAD_SECONDS = (83, 115, 80, 93, 115, 80)/WORKER_OVERHEAD_SECONDS = (83, 115, 80, 93, 80)/' scripts/suite_shards.py" &
probe M4_matrix_five $HEAD nonzero "$CK" "sed -i 's/^        shard: \[0, 1, 2, 3, 4, 5\]/        shard: [0, 1, 2, 3, 4]/; s/^        total: \[6\]/        total: [5]/' .github/workflows/rtl.yml" &
probe M5_owner_arm_4 $HEAD nonzero "$CK" "sed -i 's/^            5) test \"\$(cat/            4) test \"\$(cat/' .github/workflows/rtl.yml" &
probe M7_expect_5 $HEAD nonzero "$CK" "sed -i 's/--require-target-sha --expect 6 /--require-target-sha --expect 5 /' .github/workflows/rtl.yml" &
probe M6_old_stale_fixture $HEAD nonzero "$ST" "sed -i 's/    assert shard == \[0, 1, 2, 3, 4, 5\], \"fixture drift: verilator-shards matrix\"\n    _restate_shards/X/' scripts/ci_events.py; python3 - <<'PY'
import re,pathlib
p=pathlib.Path('scripts/ci_events.py'); s=p.read_text()
old='''    assert shard == [0, 1, 2, 3, 4, 5], \"fixture drift: verilator-shards matrix\"
    _restate_shards(w, \"verilator-shards\", \"6\")
    shard.append(6)'''
new='''    assert shard == [0, 1, 2, 3, 4], \"fixture drift: verilator-shards matrix\"
    _restate_shards(w, \"verilator-shards\", \"5\")
    shard.append(5)'''
assert s.count(old)==1; p.write_text(s.replace(old,new))
PY" &
probe M8_stale_fixture_weakened $HEAD nonzero "$ST" "python3 - <<'PY'
import pathlib
p=pathlib.Path('scripts/ci_events.py'); s=p.read_text()
old='''    _restate_shards(w, \"verilator-shards\", \"6\")
    shard.append(6)'''
new='''    _restate_shards(w, \"verilator-shards\", \"6\")'''
assert s.count(old)==1; p.write_text(s.replace(old,new))
PY" &
probe M9_not_provisional $HEAD info "$SS" "sed -i 's/^PROVISIONAL_SUITES: frozenset\[str\] = frozenset({\"gptp_tables\"})/PROVISIONAL_SUITES: frozenset[str] = frozenset()/' scripts/suite_shards.py" &
probe P0_head_control $HEAD zero "$SS && $CK" 'true' &
wait
cat "$OUT"/*.rc
