#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer lockstep matrix: base KL_srp_{talker_fsm,listener_fsm,admission}
# against the head's, at several shapes and seeds, then the same with planted
# head-side controls, each of which must show mismatches at a shape where its
# edited arm is elaborated.
# usage: matrix.sh <head-tree> <base-tree> <work> <cycles> <jobs>
# LS_CFLAGS passes through to build_run.sh.
set -u
LS_CFLAGS=${LS_CFLAGS:-}
HEAD=$1 BASE=$2 WORK=$3 CYC=$4 JOBS=$5
HERE=$(cd "$(dirname "$0")" && pwd)
SEEDS="11 22 33 44"
mkdir -p "$WORK"

# controls: label | module | sed edit on the head module
cat > "$WORK/controls.txt" <<'EOF'
c1-wtsp-write-ignores-ready|KL_srp_talker_fsm|s/assign gate_open_acc_w = rst_n \&\& gate_acc_w \&\& gate_open_i;/assign gate_open_acc_w = rst_n \&\& gate_valid_i \&\& gate_open_i;/
c2-wid-ram-read-neighbour|KL_srp_talker_fsm|s/assign wid_w = wid_r\[wsrc_r\];/assign wid_w = wid_r[wsrc_r - 1'b1];/
c3-wsid-write-ignores-ready|KL_srp_listener_fsm|s/if (rst_n \&\& ctl_acc_w \&\& ctl_settle_i) begin/if (rst_n \&\& ctl_valid_i \&\& ctl_settle_i) begin/
c4-slope-read-source-0|KL_srp_admission|s/{1'b0, slope_q_r\[aidx_r\]}/{1'b0, slope_q_r[0]}/
c5-wid-ram-only-ignores-ready|KL_srp_talker_fsm|/walk_id_write/,/end/s/if (gate_open_acc_w) begin/if (rst_n \&\& gate_valid_i \&\& gate_open_i) begin/
EOF

jobs_file="$WORK/jobs.txt"
: > "$jobs_file"
for n in 1 2 3 5 8 9; do
  echo "pos KL_srp_talker_fsm N_SOURCES_P $n" >> "$jobs_file"
  echo "pos KL_srp_listener_fsm N_SINKS_P $n" >> "$jobs_file"
done
for n in 1 2 3 5 8 9; do echo "pos KL_srp_admission N_SOURCES_P $n" >> "$jobs_file"; done
while IFS='|' read -r label mod edit; do
  np=N_SOURCES_P; [ "$mod" = KL_srp_listener_fsm ] && np=N_SINKS_P
  for n in 2 3 9; do echo "$label $mod $np $n" >> "$jobs_file"; done
done < "$WORK/controls.txt"

export HEAD BASE WORK CYC HERE SEEDS LS_CFLAGS
# each job runs in a fresh sh
while read -r kind mod np n; do
  printf '%s %s %s %s\n' "$kind" "$mod" "$np" "$n"
done < "$jobs_file" | xargs -P "$JOBS" -L 1 sh -c '
  kind=$0 mod=$1 np=$2 n=$3
  dir="$WORK/$kind-$mod-$n"
  hdl="$HEAD/hdl"
  if [ "$kind" != pos ]; then
    edit=$(grep "^$kind|" "$WORK/controls.txt" | cut -d"|" -f3)
    mkdir -p "$dir/hdl"
    cp -r "$HEAD/hdl/common" "$HEAD/hdl/srp" "$dir/hdl/"
    sed -i "$edit" "$dir/hdl/srp/$mod.sv"
    if cmp -s "$dir/hdl/srp/$mod.sv" "$HEAD/hdl/srp/$mod.sv"; then echo "$kind $mod N=$n: EDIT DID NOT APPLY"; exit 0; fi
    hdl="$dir/hdl"
  fi
  "$HERE/build_run.sh" "$hdl" "$BASE/hdl" "$mod" "$np" "$n" "$dir" "$CYC" $SEEDS > "$dir.out" 2>&1
  echo "[$kind $mod N=$n] rc=$? $(grep seed= "$dir.out" | sed "s/.*seed=/seed=/" | tr "\n" ";")"
' | sort
