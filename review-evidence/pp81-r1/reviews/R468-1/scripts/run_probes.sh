#!/usr/bin/env bash
# R468-1 reviewer probes for PR #157 at exact head db2c4eb8.
# Usage: run_probes.sh <processor-clone> <scratch-dir>
#   VERILATOR (default: verilator on PATH) must be 5.050.
# Each probe gets its own exported tree (git archive of the head), so the
# clone is never written. rc files and logs land in <scratch-dir>.
set -u
CLONE=${1:?processor clone}
OUT=${2:?scratch dir}
HEAD=db2c4eb823c47b2607fb52234b58ac6b93ff548b
BASE=83999eba1ef4756e9e769e4fba164f5095761604
HERE=$(cd "$(dirname "$0")" && pwd)
V=${VERILATOR:-verilator}
mkdir -p "$OUT"

export_tree() {  # name commit
  mkdir -p "$OUT/$1"
  git -C "$CLONE" archive "$2" hdl tb | tar -x -C "$OUT/$1"
}

run() {  # name target
  ( cd "$OUT/$1" && make -C tb/pp_top "$2" VERILATOR="$V" > "$OUT/$1.log" 2>&1
    echo $? > "$OUT/$1.rc" ) &
}

# the unmodified head and base hazard sections (HZ count 189 vs 177)
export_tree p_headhz "$HEAD";  run p_headhz hazards
export_tree base_hz "$BASE";   run base_hz hazards

# TD window edges: the top's own defaults moved by a few ms
for p in td_lo_pass td_lo_kill td_hi_pass td_hi_kill; do
  export_tree "p_$p" "$HEAD"
  (cd "$OUT/p_$p" && patch -s -p1 < "$HERE/probe-$p.patch")
  run "p_$p" timer-defaults
done

# TD with only the sixth build's prescaler moved (1 ms = 50 and 200 clk):
# TD reads the DUT's own ms timebase, so it must still pass
for p in td_presc td_presc2; do
  export_tree "p_$p" "$HEAD"
  (cd "$OUT/p_$p" && patch -s -p1 < "$HERE/probe-$p.patch")
  run "p_$p" timer-defaults
done

# extra HZ checks at the head (GDI answer status, reads beside a held GDI,
# a talker step behind a held GDI), then two extra classifier mutants
for p in tbprobe tbprobe_streamcfg tbprobe_lockop; do
  export_tree "p_$p" "$HEAD"
  (cd "$OUT/p_$p" && patch -s -p1 < "$HERE/probe-hz-extra-checks.patch")
  if [ "$p" != tbprobe ]; then
    (cd "$OUT/p_$p" && patch -s -p1 < "$HERE/probe-$p.patch")
  fi
  run "p_$p" hazards
done
wait
for f in "$OUT"/*.rc; do echo "$(basename "$f" .rc): rc=$(cat "$f")"; done
# expected: p_headhz 0 (HZ 189/0), base_hz 0 (HZ 177/0), td_lo_pass 0,
# td_hi_pass 0, td_lo_kill 2, td_hi_kill 2, td_presc 0, td_presc2 0,
# tbprobe 0 (HZ 200/0),
# tbprobe_streamcfg 2 (9 failures), tbprobe_lockop 2 (1 failure: HZ1)
