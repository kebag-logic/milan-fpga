#!/usr/bin/env bash
# Composition spot check of the merge at an exact processor head: the suites that exercise
# main's #176 SET_STREAM_INFO change beside this PR's notify and router change.
# usage: probe_compose.sh <processor-git-dir> <head-sha> <out-dir>
# env: VERILATOR (default: verilator on PATH)
#   pp_top   tb/pp_top's first (default) build only (W24*/W25* SET_STREAM_INFO rows, NP/ST/RN)
#   cmds     tb/aecp_cmds `make run` (decode table, including SET_STREAM_INFO lengths)
#   router   tb/event_router `make run`
set -u
git_dir=$1; head=$2; out=$3
V=${VERILATOR:-verilator}
mkdir -p "$out"; t=$out/tree; rm -rf "$t"; mkdir -p "$t"
git -C "$git_dir" archive "$head" | tar -x -C "$t"
cat > "$out/default.mk" <<'MK'
r648-default: ltn_rom.hex ucode.hex
	@rm -f obj_dir/build_tally.txt
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vpp_top_sim
	./obj_dir/Vpp_top_sim
MK
one() { # <name> <dir> <make args...>
  local name=$1 dir=$2 rc=0; shift 2
  ( cd "$t/$dir" && make VERILATOR="$V" "$@" ) > "$out/$name.log" 2>&1 || rc=$?
  echo "$name rc=$rc" > "$out/$name.rc"
}
one pp_top tb/pp_top -f Makefile -f "$out/default.mk" r648-default &
one cmds tb/aecp_cmds run &
one router tb/event_router run &
wait
for n in pp_top cmds router; do
  printf '%s | %s | ' "$(cat "$out/$n.rc")" "$(grep -cE '^(FAIL|  FAIL)' "$out/$n.log")"
  grep -E 'checks|PASS|FAIL' "$out/$n.log" | tail -1
done > "$out/summary.txt"
grep -hoE '(PASS|FAIL)[: ]+W2[45][a-z0-9]*' "$out/pp_top.log" | sort | uniq -c > "$out/pp_top_ssi_rows.txt"
cat "$out/summary.txt"
