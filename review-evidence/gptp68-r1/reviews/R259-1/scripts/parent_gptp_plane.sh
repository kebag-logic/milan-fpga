#!/bin/bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Parent tb/verilator/gptp_plane `run` target (parent dev 574c29fa) against
# the donor hdl at head and at base, in disposable replicas under <WORK>
# (reuses the parent/, gptp-head/, gptp-base/ checkouts parent_probes.sh made).
# Verilator build jobs capped at 8. Usage: parent_gptp_plane.sh <WORK> <out dir>
set -euo pipefail
. "$(dirname "$0")/env.sh"
WORK="$1"; OUT="$2"; mkdir -p "$OUT"; cd "$WORK"
test "$(git -C parent rev-parse HEAD)" = "$PARENT_DEV"
test "$(git -C gptp-head rev-parse HEAD)" = "$HEAD_SHA"
test "$(git -C gptp-base rev-parse HEAD)" = "$BASE_SHA"
db="$(cd parent/tb/verilator/gptp_plane && make -pn run 2>/dev/null || true)"
VF="$(printf '%s\n' "$db" | sed -n 's/^VFLAGS = //p' | sed -n '1{s/-j 0/-j 8/;p}')"
for d in head base; do
  r="E-$d"; rm -rf "$r"; mkdir -p "$r/tb/verilator" "$r/gptp-processor"
  cp -r parent/hdl "$r/"; cp -r parent/tb/common "$r/tb/"
  cp -r parent/tb/verilator/gptp_plane "$r/tb/verilator/"
  cp -r "gptp-$d/hdl" "$r/gptp-processor/"
  rm -rf "$r/tb/verilator/gptp_plane/obj_dir" "$r/tb/verilator/gptp_plane/gptp_ucode.hex"
  rc=0
  (cd "$r/tb/verilator/gptp_plane" && timeout 1500 make run VFLAGS="$VF" > "$OUT/$r.raw" 2>&1) || rc=$?
  grep -E 'gptp_ucode.hex:|^FAIL|checks:|^TX flags' "$OUT/$r.raw" > "$OUT/$r.stdout.log" || true
  rm -f "$OUT/$r.raw"; echo "$rc" > "$OUT/$r.exit"
  echo "$r: exit $rc; $(grep 'checks:' "$OUT/$r.stdout.log" || echo 'no summary')"
done
