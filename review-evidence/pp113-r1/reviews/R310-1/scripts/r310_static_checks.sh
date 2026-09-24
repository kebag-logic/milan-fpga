#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer static checks for processor PR #115 (issue #113).
# Usage: r310_static_checks.sh <clone> <evidence-dir> <milan-v1.2-text> <out-dir>
#   <evidence-dir>: local copy of review-evidence/pp113-r1 (public packet)
#   <milan-v1.2-text>: pdftotext -layout output of the Milan v1.2 consolidated PDF
set -uo pipefail
REPO=$1; EV=$2; SPEC=$3; OUT=$4
BASE=a8f8ce810ddba1816cd129d0afcd71e6e02ade1b
HEAD=29840136bb2d21bc0fbe92c7c533368f40837ff6
mkdir -p "$OUT"
g() { git -C "$REPO" "$@"; }

{
  echo "## top-level port header (module ... through first ');')"
  hdr() { g show "$1:hdl/top/protocol_processor_top.sv" \
          | awk '/^module protocol_processor_top/{f=1} f{print} f&&/^\);/{exit}'; }
  a=$(hdr $BASE | sha256sum); b=$(hdr $HEAD | sha256sum)
  echo "base $a"; echo "head $b"
  [ "$a" = "$b" ] && echo "RESULT identical" || echo "RESULT DIFFERENT"

  echo "## every reference to the new strobe at head"
  g grep -n "evt_tk_latency_chg\|srp_evt_tk_latency_chg_w" $HEAD -- hdl tb
  echo "## event-router strobe map entries for SRP talker events (must not name latency)"
  g grep -n "evr_strobe_w\[.*srp_evt" $HEAD -- hdl/top/protocol_processor_top.sv

  echo "## changed files base..head"
  g diff --stat $BASE $HEAD
} > "$OUT/static-rtl.txt" 2>&1

{
  echo "## OOC figures from the published reports"
  for d in area-base area-head; do
    echo "== $d"
    grep -E "^\| (Slice LUTs|Slice Registers|  RAMB36/FIFO|  RAMB18|DSPs)" "$EV/author/$d/util.rpt"
    grep -E "Tool Version|Design  " "$EV/author/$d/util.rpt"
    grep -E "u_listener +\| +KL_srp_listener_fsm" "$EV/author/$d/util_hier.rpt"
    awk '/WNS\(ns\)/{getline; getline; print "WNS/TNS line:", $0}' "$EV/author/$d/timing.rpt"
  done
  echo "## provenance: every hdl sha256 against the exact head blob"
  python3 - "$REPO" "$EV/author/provenance.json" $HEAD <<'EOF'
import hashlib, json, subprocess, sys
repo, prov, head = sys.argv[1:]
d = json.load(open(prov))
bad = 0
for path, want in sorted(d["hdl_sha256"].items()):
    blob = subprocess.run(["git", "-C", repo, "show", f"{head}:{path}"],
                          capture_output=True).stdout
    if hashlib.sha256(blob).hexdigest() != want:
        bad += 1; print("MISMATCH", path)
tracked = [p for p in subprocess.run(["git", "-C", repo, "ls-tree", "-r", "--name-only",
           head, "hdl"], capture_output=True, text=True).stdout.split() if p.endswith(".sv")]
print(f"entries={len(d['hdl_sha256'])} mismatches={bad} head_sv={len(tracked)} "
      f"uncovered={[p for p in tracked if p not in d['hdl_sha256']]} "
      f"head={d.get('head')} tree={d.get('tree')} spec_sha256={d.get('spec_sha256')}")
EOF
  echo "## OOC recipe unchanged base..head"
  g diff --quiet $BASE $HEAD -- syn/ooc/protocol_processor_ooc.tcl && echo "protocol_processor_ooc.tcl unchanged"
} > "$OUT/static-area.txt" 2>&1

{
  echo "## Milan v1.2 consolidated, 5.4.5.2 / Table 5.22 (printed pp. 62-63), GET_STREAM_INFO row"
  n=$(grep -n "^5.4.5.2 List of unsolicited notifications" "$SPEC" | tail -1 | cut -d: -f1)
  sed -n "$((n+12)),$((n+14))p" "$SPEC"
  grep -n "Table 5.22: Unsolicited notifications" "$SPEC"
  grep -n -A1 "MSRP accumulated latency (Stream Input" "$SPEC"
  grep -n "GET_COUNTERS .*Sent when one of the counters" "$SPEC"
} > "$OUT/static-spec.txt" 2>&1
echo "static checks written to $OUT"
