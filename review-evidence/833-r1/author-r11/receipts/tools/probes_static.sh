#!/usr/bin/env bash
# Round 10 reviewer probes that read a tree (no campaign), from manifest-checked copies, at the head; one log and rc each.
set -u
S=$VALIDATION_STORAGE/833-a726k; O=$MANAGEMENT/2026-09-23/833-a726k/receipts/final
H=$S/wt-head; PREV=$S/wt-prev; P3=$S/probes/833-r763-10/scripts; P4=$S/probes/833-r764-10/scripts
export TMPDIR=$S/tmp
grep SigIgn /proc/self/status > "$O/static.sigign"
run() { id=$1; shift; { echo "# $*"; "$@"; } > "$O/$id.log" 2>&1; rc=$?; echo $rc > "$O/$id.rc"; echo "$id rc=$rc: $(tail -n 1 "$O/$id.log" | cut -c1-150)"; }
echo '{}' > "$S/empty-manifest.json"
run r763-10-table-check python3 -I "$P3/table_check.py" "$H"
run r763-10-modcheck python3 -I "$P3/modcheck.py" "$PREV" "$H"
run r763-10-natcheck python3 -I "$P3/natcheck.py" "$H" "$S/probes/833-r763-9/natural.py"
run r763-10-probe-cells python3 -I "$P3/probe_cells.py" "$H"
run r764-10-byte-match-r9 python3 -I "$P4/byte_match_r9.py" "$S/probes/833-r763-9/natural.py" "$H" "$S/empty-manifest.json"
run r764-10-module-moves python3 -I "$P4/module_moves.py" "$PREV" "$H"
run a726k-byte-f1 python3 -I "$S/tools/byte_f1.py" "$H" "$P3/natural10.py"
