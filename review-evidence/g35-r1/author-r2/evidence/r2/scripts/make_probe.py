"""Turn a copy of the parser bench into the per-position probe: one TSV row
per flagged byte (drops, events, writes before/on/after) for the four swept
types and an Announce, and nothing else. Usage: make_probe.py <sim_main.cpp>
(the copy must sit at tb/verilator/parser/ beside tb/common/ in a scratch tree)"""
import sys
from pathlib import Path
p = Path(sys.argv[1]); t = p.read_text()
def sub(a, b):
    global t
    assert t.count(a) == 1, a
    t = t.replace(a, b)
sub("  void check_a_refused_frame_leaves_no_stale_word();\n",
    "  void check_a_refused_frame_leaves_no_stale_word();\n  void probe_positions();\n")
sub("int RxParserHarness::report() {", '''void RxParserHarness::probe_positions() {
  std::vector<ErrArm> arms = rx_err_arms();
  arms.push_back({"ann", announce_frame(0x350B, AGM, 0, ASRC, {}), 3});
  printf("type\\tlen\\tbyte\\tdrops\\tevents\\tbefore\\ton\\tafter\\n");
  for (const ErrArm &a : arms) {
    for (size_t p = 0; p < a.f.b.size(); p++) {
      uint16_t d0 = dut->drop_cnt_o;
      feed_err(a.f.b, p, p);
      printf("%s\\t%zu\\t%zu\\t%d\\t%d\\t%d\\t%d\\t%d\\n", a.tag, a.f.b.size(), p,
             dut->drop_cnt_o - d0, ev_count, writes_before_err, writes_on_err,
             writes_after_err);
    }
  }
}

int RxParserHarness::report() {''')
sub("int RxParserHarness::run() {\n  reset_the_parser();\n",
    "int RxParserHarness::run() {\n  reset_the_parser();\n  probe_positions();\n  return 0;\n")
p.write_text(t)
