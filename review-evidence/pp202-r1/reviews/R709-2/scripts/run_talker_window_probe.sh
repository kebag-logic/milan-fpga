#!/bin/sh
# usage: run_talker_window_probe.sh <exported-head-tree> <work-dir> <verilator>
# Copies the talker bench and, inside S10's block-allocator leg (src5 disabled
# and re-enabled, the allocator handing back the same DA), prints every gate
# strobe of src5 with its millisecond, so the close-to-reopen interval of a
# disable/return can be compared with T-MRP-JOIN (200 ms).
set -e
HEAD=$1; W=$2; V=$3
rm -rf "$W"; mkdir -p "$W/tb"; cp -r "$HEAD/hdl" "$W/"; cp -r "$HEAD/tb/acmp_talker" "$HEAD/tb/common" "$W/tb/" 2>/dev/null || cp -r "$HEAD/tb/acmp_talker" "$W/tb/"
cd "$W/tb/acmp_talker"
python3 -I - <<'PY'
import pathlib
p = pathlib.Path("sid_cases.hpp"); t = p.read_text()
anchor = '  probe(h, 5, ST_OK, da_pool(5), sid_of(5), "S10 src5 declares its configured ID");\n'
assert t.count(anchor) == 1
t = t.replace(anchor, anchor + '  h.gates.clear();\n', 1)
anchor2 = '        "S10 PROBE_TX after the same DA returns answers the new ID");\n'
assert t.count(anchor2) == 1
t = t.replace(anchor2, anchor2 +
  '  for (const auto& e : h.gates) if (e.src == 5)\n'
  '    printf("WINDOW src5 %s sid=%016llx da=%012llx ms=%u\\n", e.open ? "OPEN " : "CLOSE",\n'
  '           (unsigned long long)e.sid, (unsigned long long)e.da, e.ms);\n', 1)
p.write_text(t)
PY
make run VERILATOR="$V"
