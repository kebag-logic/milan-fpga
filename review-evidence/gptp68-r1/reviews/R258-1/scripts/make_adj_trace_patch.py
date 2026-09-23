#!/usr/bin/env python3
"""Instrument a copy of the parent gptp_shadow sim_main.cpp to print every
change of the PHC addend level and of the published flags with the cycle,
the published offset and the step pulse. Probe only: it adds prints and
changes no check. Usage: make_adj_trace_patch.py <sim_main.cpp>"""
import sys
from pathlib import Path


def main() -> None:
    """Rewrite the file in place."""
    path = Path(sys.argv[1])
    s = path.read_text()
    old = "    cyc++;\n  }\n\n  void run(uint64_t n) { while (n--) tick(); }"
    assert s.count(old) == 1
    new = """    {
      static int32_t probe_adj = 0;
      static uint32_t probe_flags = 0;
      const int32_t a = static_cast<int32_t>(dut->dbg_phc_adj_o);
      const uint32_t fl = dut->pub_flags_o;
      if (a != probe_adj || fl != probe_flags)
        fprintf(stderr, "ADJ cyc=%llu adj=%d flags=%u offset=%d phcl=%u\\n",
                (unsigned long long)cyc, a, fl,
                static_cast<int32_t>(dut->pub_offset_o),
                (unsigned)dut->dbg_txts_phcl_o);
      probe_adj = a;
      probe_flags = fl;
    }
    cyc++;
  }

  void run(uint64_t n) { while (n--) tick(); }"""
    path.write_text(s.replace(old, new))


if __name__ == "__main__":
    main()
