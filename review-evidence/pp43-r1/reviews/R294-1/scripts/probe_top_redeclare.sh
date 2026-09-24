#!/usr/bin/env bash
# R294 probe P2: at protocol_processor_top, count MSRP Listener (type 3)
# declarations for sink 0's stream transmitted after a CHANGED vs an
# UNCHANGED Talker Failed FailureInformation, in the GI phase.
# Usage: probe_top_redeclare.sh <extracted-head-tree> <log>
# Runs on a DISPOSABLE extracted tree (git archive), never on the clone.
set -euo pipefail
tree=$1; log=$2
here=$(cd "$(dirname "$0")" && pwd)
f=$tree/tb/pp_top/gsi_internal.hpp
python3 - "$f" <<'PY'
import sys
path = sys.argv[1]
src = open(path).read()
helper = r'''
  // ---- R294 probe P2 (disposable) ----
  void r294_scan(const char* tag) {
    int n = 0;
    for (const auto& fr : io.q_msrp) {
      for (size_t i = 14; i + 14 <= fr.size(); ++i) {
        if (fr[i] != 0x03 || fr[i + 1] != 0x08) continue;
        if (fv_u64(fr, int(i + 6), 8) != sid(0)) continue;
        const unsigned nvals = ((fr[i + 4] & 0x1F) << 8) | fr[i + 5];
        const unsigned tp = fr[i + 14], fp = fr[i + 15];
        printf("R294-P2 %s: listener decl sid0 nvals=%u event=%u fourpack=%u\n",
               tag, nvals, tp / 36, fp >> 6);
        ++n;
      }
    }
    printf("R294-P2 %s: %d listener declaration(s) for sink 0\n", tag, n);
  }
'''
anchor = "  void run() {"
assert src.count(anchor) == 1
src = src.replace(anchor, helper + anchor)
a1 = '''    attribute(0, 9, BRIDGE0 ^ 0xFFFF000000000000ull, true);
    pair("FAILED-REFRESH", 0, 3, 0, 9, BRIDGE0 ^ 0xFFFF000000000000ull);
'''
b1 = '''    io.run_ms(1500); io.q_msrp.clear();
    attribute(0, 9, BRIDGE0 ^ 0xFFFF000000000000ull, true);
    pair("FAILED-REFRESH", 0, 3, 0, 9, BRIDGE0 ^ 0xFFFF000000000000ull);
    io.run_ms(600); r294_scan("changed-failure");
    io.run_ms(1500); io.q_msrp.clear();
'''
a2 = '''    io.run_ms(100);
    CHECK(io.q_aecp.empty(), "GI unchanged Failed: no fabricated failure transition");
'''
b2 = '''    io.run_ms(1100);
    CHECK(io.q_aecp.empty(), "GI unchanged Failed: no fabricated failure transition");
    r294_scan("unchanged-failure");
'''
assert src.count(a1) == 1 and src.count(a2) == 1
src = src.replace(a1, b1).replace(a2, b2)
open(path, "w").write(src)
PY
cd "$tree/tb/pp_top"
rm -rf obj_dir
make gsi-build VERILATOR="$here/verilator8" > "$log.build" 2>&1
./obj_dir/Vpp_top_sim --gsi-internal-only > "$log" 2>&1 || true
grep -E 'R294-P2|checks, ' "$log"
