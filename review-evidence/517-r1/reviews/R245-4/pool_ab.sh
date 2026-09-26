#!/usr/bin/env bash
# Pool-phase A/B at the head under review, with the eleven already-built legs:
#   head  - the recipe's runner line at the head (no --exclusive marks)
#   marks - the same line with round 4's five --exclusive marks restored
# Both run at the same time, each from its own mirror of the suite directory
# (a real directory whose entries are symlinks into the clone, with a private
# obj_legs/ and TMPDIR), so neither writes the clone and both see the same
# host load. The runner is the head's sim_pool.py in both. A 585 s guard sends
# SIGTERM, which the runner turns into a reaped, attributed cancellation.
#   usage: pool_ab.sh REPO SCRATCH OUTDIR
set -uo pipefail
REPO=$1; SCRATCH=$2; OUT=$3
SUITE=$REPO/tb/verilator/milan_dp
mkdir -p "$OUT"
LINE=$(make -s -n -C "$SUITE" run VERILATOR=/nonexistent | tr -d '\\' | tr '\n' ' ' \
       | grep -o 'exec python3 sim_pool.py.*obj_aclk/Vmilan_dp_aclk')
for v in head marks; do
  root=$SCRATCH/ab-$v
  rm -rf "$root"; mkdir -p "$root/tb/verilator/milan_dp" "$root/tmp"
  for e in "$REPO"/* ; do ln -s "$e" "$root/$(basename "$e")" 2>/dev/null || true; done
  rm -f "$root/tb"; mkdir -p "$root/tb/verilator/milan_dp"
  for e in "$SUITE"/* ; do
    case "$(basename "$e")" in obj_legs) ;; *) ln -s "$e" "$root/tb/verilator/milan_dp/$(basename "$e")";; esac
  done
  cmd=${LINE#exec }
  if [ $v = marks ]; then
    for leg in '$(NOTIFY_MDIR)/Vmilan_dp_notify' obj_notify/Vmilan_dp_notify obj_nxn/Vmilan_dp_nxn obj_nxndv/Vmilan_dp_nxndv obj_nxn8/Vmilan_dp_nxn8 obj_nxn4c/Vmilan_dp_nxn4c; do
      cmd=${cmd/ .\/$leg / --exclusive .\/$leg }
    done
  fi
  printf '%s\n' "$cmd" > "$OUT/$v.argv"
done
start_one() {
  local v=$1; local d=$SCRATCH/ab-$v/tb/verilator/milan_dp
  ( cd "$d" && env TMPDIR="$SCRATCH/ab-$v/tmp" /usr/bin/time -f "%e" -o "$OUT/$v.seconds" \
      timeout -s TERM 585 bash -c "$(cat "$OUT/$v.argv")" > "$OUT/$v.stdout" 2> "$OUT/$v.stderr";
    echo $? > "$OUT/$v.exit" )
}
start_one head & start_one marks & wait
for v in head marks; do
  cp "$SCRATCH/ab-$v/tb/verilator/milan_dp/obj_legs/replay.log" "$OUT/$v.replay.log" 2>/dev/null
  echo "$v exit=$(cat "$OUT/$v.exit") seconds=$(cat "$OUT/$v.seconds") exclusive_marks=$(grep -o -- '--exclusive' "$OUT/$v.argv" | wc -l) replay_sha256=$(sha256sum < "$OUT/$v.replay.log" | cut -c1-16)"
done
