#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Insert the disposable R259 probe phase into a COPY of the engine harness.

The probe grades the plane against the owner decision's own text
(issue 68 comment 5794731372): one link-up, "the first synchronization after
asCapable"; once locked, "including after a grandmaster change", a pair up
to 100 us slews. A Sync gap longer than the 375 ms receipt timeout while
asCapable holds is not an asCapable rise, so the probe expects the next pair
to be locked. It runs only when R259_PROBE is set, straight after phase 18c,
and ends the run there."""
import sys
from pathlib import Path

path = Path(sys.argv[1])
s = path.read_text()
hook = "    stay_locked_across_a_grandmaster_change();\n"
assert s.count(hook) == 1
s = s.replace(hook, hook +
"""    if (std::getenv("R259_PROBE")) {
      probe_the_owner_text_after_a_sync_gap();
      printf("%d checks: %d PASS, %d FAIL\\n", checks, checks - fails, fails);
      return fails ? 1 : 0;
    }
""")
anchor = "  // ---- 19: the parent degrades below us -> immediate takeover -----------\n"
assert s.count(anchor) == 1
s = s.replace(anchor, """  // ---- R259 probe: the owner text after a Sync gap (disposable) -------
  void probe_the_owner_text_after_a_sync_gap() {
    const uint64_t SRC5 = 0x00F1F1FFFE000009ull;
    const uint64_t GM_C = 0x00C0C0FFFE00000Cull;
    const uint64_t GM_D = 0x00D0D0FFFE00000Dull;
    const uint64_t TP = 70000000000ull;
    expect_policy_pair("probe: locked pair before the gap", 0x0800, TP, 3000,
                       false, false, SRC5);
    struct Case { const char *tag; uint64_t gm; int64_t off; };
    const Case cases[] = {
      {"probe: same GM after a Sync gap, +50 us", GM_C, 50000},
      {"probe: GM failover after a Sync gap, -50 us", GM_D, -50000},
      {"probe: same GM after a Sync gap, +90 us", GM_D, 90000},
    };
    uint16_t seq = 0x0801;
    uint16_t aseq = 60;
    for (const Case &c : cases) {
      char n[128];
      const bool gap = wait_flags(FL_SYNCOK, 0, 900000ull);
      snprintf(n, sizeof n, "%s: receipt timeout, asCapable held", c.tag);
      expect(n, gap && (dut->pub_flags_o & FL_ASCAP) ? 1 : 0, 1);
      announce(aseq++, 100, c.gm, 1, SRC5);
      snprintf(n, sizeof n, "%s: grandmaster elected", c.tag);
      expect(n, dut->pub_gm_id_o, c.gm);
      const size_t s0 = steps_seen.size();
      expect_policy_pair(c.tag, seq,
                         TP + static_cast<uint64_t>(seq - 0x0800) * 1000000000ull,
                         c.off, false, false, SRC5, 0);
      printf("PROBE %s: step pulses %zu (owner text: 0)\\n", c.tag,
             steps_seen.size() - s0);
      seq++;
    }
  }

""" + anchor)
if "#include <cstdlib>" not in s:
    s = "#include <cstdlib>\n" + s
path.write_text(s)
