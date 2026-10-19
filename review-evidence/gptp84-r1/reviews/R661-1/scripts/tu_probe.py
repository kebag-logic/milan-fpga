#!/usr/bin/env python3
"""Instrument a COPY of the parent gptp_shadow harness to measure the AVTP
tu bit (ts_uncertain_o, the parent's KL_ptp_clock_validity) on every cycle
whose committed publication carries the master bit.

Per mastership entry it records the tu=1 cycles inside the first 400 cycles
(the harness runs the parent holdover at 2 quarter-ticks of 64 cycles, so a
grandmaster change holds tu for 128..192 cycles) and every tu=1 cycle after
that window. Prints one INFO line before the suite's summary.

Usage: tu_probe.py PATH/TO/tb/verilator/gptp_shadow/sim_main.cpp
"""
import sys
from pathlib import Path

f = Path(sys.argv[1])
s = f.read_text(encoding="utf-8")

glob_anchor = "int main(int argc, char **argv) {"
tick_anchor = "    cyc++;\n  }\n\n  void run(uint64_t n) { while (n--) tick(); }"
sum_anchor = '    printf("%d checks: %d PASS, %d FAIL\\n", checks, checks - fails, fails);'
for a in (glob_anchor, tick_anchor, sum_anchor):
    assert s.count(a) == 1, a

decl = ("// reviewer tu probe state\n"
        "static uint64_t rv_mc, rv_mtu, rv_late, rv_trans, rv_early, rv_since;\n"
        "static uint64_t rv_early0, rv_prev_gm, rv_last_gm;\n"
        "static bool rv_pm;\n")
s = s.replace("class GptpShadowHarness", decl + "class GptpShadowHarness", 1)
probe = ("    {\n"
         "      const bool m = dut->rst_n && (dut->pub_flags_o & FL_AMGM);\n"
         "      if (rv_pm && rv_since == 400)\n"
         "        printf(\"INFO reviewer tu probe entry %llu at cycle %llu: \"\n"
         "               \"gm %016llx -> %016llx, tu=1 cycles in first 400: %llu\\n\",\n"
         "               (unsigned long long)rv_trans,\n"
         "               (unsigned long long)(cyc - 400),\n"
         "               (unsigned long long)rv_prev_gm,\n"
         "               (unsigned long long)dut->pub_gm_id_o,\n"
         "               (unsigned long long)(rv_early - rv_early0));\n"
         "      if (m && !rv_pm) { rv_trans++; rv_since = 0; rv_early0 = rv_early;\n"
         "                         rv_prev_gm = rv_last_gm; }\n"
         "      if (!m) rv_last_gm = dut->pub_gm_id_o;\n"
         "      if (m) {\n"
         "        rv_mc++; rv_since++;\n"
         "        if (dut->ts_uncertain_o) {\n"
         "          rv_mtu++;\n"
         "          if (rv_since > 400) {\n"
         "            if (rv_late < 5)\n"
         "              printf(\"INFO reviewer tu probe: tu=1 at master cycle %llu \"\n"
         "                     \"(cycle %llu, flags %x, pub_commit %d)\\n\",\n"
         "                     (unsigned long long)rv_since,\n"
         "                     (unsigned long long)cyc,\n"
         "                     (unsigned)dut->pub_flags_o, (int)dut->pub_commit_o);\n"
         "            rv_late++;\n"
         "          } else rv_early++;\n"
         "        }\n"
         "      }\n"
         "      rv_pm = m;\n"
         "    }\n")
s = s.replace(tick_anchor, probe + tick_anchor, 1)
report = ('    printf("INFO reviewer tu probe: mastership entries %llu, master cycles %llu, '
          'tu=1 master cycles %llu (within 400 cycles of entry %llu, later %llu)\\n", '
          '(unsigned long long)rv_trans, (unsigned long long)rv_mc, '
          '(unsigned long long)rv_mtu, (unsigned long long)rv_early, '
          '(unsigned long long)rv_late);\n')
s = s.replace(sum_anchor, report + sum_anchor, 1)
assert "class GptpShadowHarness" in s and s.count("reviewer tu probe state") == 1
f.write_text(s, encoding="utf-8")
print("instrumented", f)
