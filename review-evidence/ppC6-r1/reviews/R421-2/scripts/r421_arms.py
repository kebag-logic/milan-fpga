#!/usr/bin/env python3
"""Insert R421-2's probe arms into a scratch copy's tb/pp_top/notify_phases.hpp.

R421a/R421b: the MAC refuses the LAST byte (the eof beat) of identify frame 1
(then frame 2) for 400 ms, through the bench's own stall_tx_at_eof hook; the
next frame must still leave at least T-IDENT-BURST after that byte was taken.
R421c/R421d: a short press, then a second press (30 ms / 200 ms long) made in
WAITING 2 ms after the burst's third frame left. Figure 7-142 enters IDENTIFY
on the press; the documented gap (banner, 06 section 7) says the next burst
starts T-IDENT-BURST after that third frame, never at once.
Usage: r421_arms.py TREE [--without-c]
  --without-c  omit the R421c call, so a golden of the other arms can pass
"""
import sys
from pathlib import Path

ARMS = r'''
  // ---- R421 probe arms (reviewer-owned, never committed) ----
  void r421_stall_at_eof(size_t frame, const char* tag) {
    const size_t from = seen.size();
    press(true);
    if (frame > 0) wait_idents(from, frame);
    // arm the bench's eof-beat stall while the frame is part-way out
    for (long c = 0; c < 400L * MS_CYC && !mid_ident_frame(); ++c) tick();
    press(false);
    io.stall_tx_at_eof = true;
    for (long c = 0; c < 50L * MS_CYC && !io.tx_eof_stalled; ++c) tick();
    io.stall_tx_at_eof = false;
    const bool hit = io.tx_eof_stalled;
    run_ms(400);
    io.mac_tx_ready = true;
    io.tx_eof_stalled = false;
    run_ms(1500);
    const auto v = idents(from);
    CHECK(hit && v.size() == 3, "%s: premise: the eof beat of frame %zu was stalled (%d) "
          "and three frames left (%zu)", tag, frame + 1, int(hit), v.size());
    if (v.size() == 3) {
      printf("  [i] %s: eof-beat stall of frame %zu: gaps %ld and %ld clocks\n", tag,
             frame + 1, gap_of(v, 0), gap_of(v, 1));
      for (size_t k = 0; k < 2; ++k)
        CHECK(gap_of(v, k) >= BURST, "%s: gap %zu->%zu is %ld clocks, want at least "
              "T-IDENT-BURST %ld after the stalled last byte was taken", tag, k + 1,
              k + 2, gap_of(v, k), BURST);
    }
  }
  //! a second press of `hold_ms`, made 2 ms after a burst's third frame left
  void r421_repress_after_burst(long hold_ms, const char* tag) {
    const size_t from = seen.size();
    press(true);
    run_ms(30);
    press(false);
    wait_idents(from, 3);
    run_ms(2);
    press(true);
    run_ms(hold_ms);
    press(false);
    run_ms(1500);
    const auto v = idents(from);
    printf("  [i] %s: a %ld ms press 2 ms after frame 3: %zu frames\n", tag, hold_ms,
           v.size());
    CHECK(v.size() == 6, "%s: a %ld ms press made in WAITING 2 ms after the burst's "
          "third frame starts IDENTIFY (Figure 7-142), got %zu frames", tag, hold_ms,
          v.size());
    if (v.size() == 6) {
      printf("  [i] %s: next burst %ld clocks after frame 3\n", tag, gap_of(v, 2));
      CHECK(gap_of(v, 2) >= BURST, "%s: the next burst's first frame is %ld clocks "
            "after the third frame, want at least T-IDENT-BURST %ld (the documented gap)",
            tag, gap_of(v, 2), BURST);
    }
  }
  void r421_probes() {
    r421_stall_at_eof(0, "R421a");
    r421_stall_at_eof(1, "R421b");
    r421_repress_after_burst(200, "R421d");
    r421_repress_after_burst(30, "R421c");  // R421C_MARK
  }

  void run() {
    boot_to_idle(true);
'''

def main() -> int:
    path = Path(sys.argv[1]) / "tb/pp_top/notify_phases.hpp"
    text = path.read_text()
    old = "  void run() {\n    boot_to_idle(true);\n    one_press_sends_one_burst();\n"
    assert text.count(old) == 1, "anchor"
    text = text.replace(old, ARMS + "    one_press_sends_one_burst();\n", 1)
    old2 = "    a_tx_stall_mid_burst_never_bunches_it();\n  }\n"
    assert text.count(old2) == 1, "anchor2"
    text = text.replace(old2, "    a_tx_stall_mid_burst_never_bunches_it();\n    r421_probes();\n  }\n", 1)
    if "--without-c" in sys.argv[2:]:
        text = text.replace('    r421_repress_after_burst(30, "R421c");  // R421C_MARK\n', "", 1)
    path.write_text(text)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
