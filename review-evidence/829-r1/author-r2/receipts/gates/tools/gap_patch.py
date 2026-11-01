"""Scratch probe, never committed: histogram of tx_en low runs on the pads, from the suite's own pad oracle edge."""
import sys
from pathlib import Path
p = Path(sys.argv[1]) / "tb/verilator/gptp_txts/sim_main.cpp"
t = p.read_text()
o = "void TxtsHarness::on_eth_edge() {\n"
n = o + """  {
    static uint64_t low_run = 0, last_rise_ns = 0, last_fall_ns = 0; static bool prev_en = false;
    const bool en = dut->gmii_tx_en_o != 0;
    if (en && !prev_en) {
      if (last_fall_ns != 0) { gap_hist_[low_run]++; gap_ns_hist_[now_ - last_fall_ns]++; }
      last_rise_ns = now_;
      low_run = 0;
    }
    if (!en && prev_en) { last_fall_ns = now_; low_run = 0; }
    if (!en) low_run++;
    prev_en = en;
    (void)last_rise_ns;
  }
"""
assert t.count(o) == 1
t = t.replace(o, n)
o = "  void prove_bring_up();\n"
n = o + "  std::map<uint64_t, uint64_t> gap_hist_;\n  std::map<uint64_t, uint64_t> gap_ns_hist_;\n"
assert t.count(o) == 1
t = t.replace(o, n)
t = t.replace("#include <cstring>\n", "#include <cstring>\n#include <map>\n", 1)
o = "  prove_full_run_laws();\n  return check.report();\n"
n = """  prove_full_run_laws();
  std::printf("GAP-PROBE tx_en low samples between frames (samples: count), smallest first:\\n");
  int shown = 0;
  for (const auto &kv : gap_hist_) { if (shown++ < 12) std::printf("GAP-PROBE   %llu samples: %llu\\n", (unsigned long long)kv.first, (unsigned long long)kv.second); }
  std::printf("GAP-PROBE distinct low-run lengths %zu\\n", gap_hist_.size());
  shown = 0;
  for (const auto &kv : gap_ns_hist_) { if (shown++ < 6) std::printf("GAP-PROBE   last tx_en high sample to next rise %llu ns: %llu\\n", (unsigned long long)kv.first, (unsigned long long)kv.second); }
  return check.report();
"""
assert t.count(o) == 1
t = t.replace(o, n)
p.write_text(t)
