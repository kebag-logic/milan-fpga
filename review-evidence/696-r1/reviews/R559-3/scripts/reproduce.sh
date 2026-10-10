#!/bin/sh
# Reproduce this round's executed evidence. Needs: GNU make, python3, git, and
# a Verilator 5.050 at $VERILATOR_BIN. Each argument is a DISPOSABLE full copy
# of the repository at b9b389611304850ea435b2056887568afe5e6bf4 (with its
# protocol-processor and gptp-processor submodules checked out), because the
# suites write build directories in-tree.
#   reproduce.sh <copy-w> <copy-plain> <copy-control> <scratch>
set -u
w=$1; plain=$2; ctl=$3; s=$4; vb=${VERILATOR_BIN:?}; vd=$(dirname "$vb")
mkdir -p "$s/tmp_w" "$s/tmp_plain"
# 1. Hosted condition: an inherited print-directory flag. TMPDIR is private so
#    a host-wide /tmp cleaner cannot remove the campaign's work directory.
(cd "$w" && env TMPDIR="$s/tmp_w" PATH="$vd:$PATH" VERILATOR="$vb" MAKEFLAGS=w \
   make -C tb/verilator/maap VERILATOR="$vb" > "$s/w2.log" 2>&1; echo $? > "$s/w2.rc") &
# 2. Plain invocation.
(cd "$plain" && env TMPDIR="$s/tmp_plain" PATH="$vd:$PATH" VERILATOR="$vb" \
   make -C tb/verilator/maap VERILATOR="$vb" > "$s/plain2.log" 2>&1; echo $? > "$s/plain2.rc") &
wait
# 3. Negative control: the f909d6c4 integration.mk under MAKEFLAGS=w must fail
#    to elaborate with make chatter as Verilator sources; head must build/run.
cp -a "$ctl" "$s/f909ctl"
git -C "$s/f909ctl" show f909d6c460344527f102f24b8e7a77f09959e755:tb/verilator/maap/integration.mk \
  > "$s/f909ctl/tb/verilator/maap/integration.mk"
(cd "$s/f909ctl" && env PATH="$vd:$PATH" MAKEFLAGS=w make -C tb/verilator/maap integration-build \
   VERILATOR="$vb" DP_MDIR="$s/obj_f909_w" > "$s/f909ctl.log" 2>&1; echo $? > "$s/f909ctl.rc") &
(cd "$ctl" && env PATH="$vd:$PATH" MAKEFLAGS=w make -C tb/verilator/maap integration-build \
   VERILATOR="$vb" DP_MDIR="$s/obj_head_w" > "$s/headctl.log" 2>&1; echo $? > "$s/headctl.rc"
 cd "$s/obj_head_w" && ./maap_integration > "$s/headctl_run.log" 2>&1; echo $? > "$s/headctl_run.rc") &
wait
# 4. Parse-time guard probes (no build).
sh "$(dirname "$0")/guard_probes.sh" "$ctl" > "$s/guard_probes.txt" 2>&1
