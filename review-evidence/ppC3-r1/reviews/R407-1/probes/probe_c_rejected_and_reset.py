#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probe (disposable): extend tb/pp_top section AD in a scratch copy.

After AD4 it checks that the ADPDU's current_configuration_index equals what
GET_CONFIGURATION and ENTITY.current_configuration answer (a) after a refused
SET_CONFIGURATION (BAD_ARGUMENTS) on a set row, (b) across a reset with the
NVM model kept (after a SUCCESS SET to 0), (c) after a refused SET on the
row as the reboot left it, and (d) after an ENTITY_LOCKED refusal.
Usage: probe_c_rejected_and_reset.py <clone> <scratch-dir>; then
make -C <scratch-dir>/tb/pp_top adp-config
"""
import shutil
import sys
from pathlib import Path

clone, scratch = Path(sys.argv[1]), Path(sys.argv[2])
if scratch.exists():
    shutil.rmtree(scratch)
for sub in ("hdl", "tb/common", "tb/pp_top"):
    shutil.copytree(clone / sub, scratch / sub,
                    ignore=shutil.ignore_patterns("obj_*", "__pycache__"))
src = scratch / "tb/pp_top/sim_main.cpp"
text = src.read_text()
anchor = ('          "AD4: the set configuration outranks a moved current_cfg_i");\n'
          '    io.d->current_cfg_i = IMAGE_CFG;\n')
assert text.count(anchor) == 1, "anchor drifted"
probe = r'''
    probe_rejected_and_reset(e);
'''
helper = r'''
  static unsigned idx_of(const std::vector<uint8_t>& f) {
    return f.size() == 82 ? ((unsigned(f[64]) << 8) | f[65]) : 999u;
  }
  //! all three views of the current configuration, compared
  void agree(const std::vector<uint8_t>& adv, unsigned want, const char* tag) {
    const unsigned g = word40(ask(AEM_GET_CONFIGURATION, {}));
    const unsigned en = entity_current_configuration();
    printf("PROBE %s: ADPDU %u GET %u ENTITY %u (want %u)\n", tag, idx_of(adv), g,
           en, want);
    CHECK(idx_of(adv) == g && g == en, "PROBE %s: ADPDU %u == GET %u == ENTITY %u",
          tag, idx_of(adv), g, en);
    CHECK(g == want, "PROBE %s: current configuration %u, got %u", tag, want, g);
  }
  void probe_rejected_and_reset(const std::vector<uint8_t>& last) {
    (void)last;
    // (a) refused on a set row (1)
    io.flush_all();
    auto s = set_configuration(5);
    CHECK(status(s) == AECP_BAD_ARGUMENTS && word40(s) == IMAGE_CFG,
          "PROBE a: SET(5) BAD_ARGUMENTS echoing %u, got %d %u", IMAGE_CFG,
          status(s), word40(s));
    agree(io.wait_any(io.q_adp, 9800), IMAGE_CFG, "a refused SET on a set row");
    // SUCCESS to 0, then a reset with the NVM model kept
    io.flush_all();
    s = set_configuration(0);
    CHECK(status(s) == AECP_SUCCESS, "PROBE b: SET(0) SUCCESS, got %d", status(s));
    agree(io.wait_any(io.q_adp, 9800), 0, "b before reset");
    io.run_ms(200);                            // let any NVM commit land
    io.reset();
    io.d->current_cfg_i = IMAGE_CFG;
    io.d->restore_go_i = 1;
    io.idle(5);
    io.d->restore_go_i = 0;
    unsigned budget = 400000;
    while (!io.d->restore_done_o && budget-- != 0) io.step();
    CHECK(io.d->restore_done_o && !io.d->restore_fail_o, "PROBE b: restore done");
    io.flush_all();
    io.d->link_up_i = 1;
    io.idle(50);
    io.d->entity_enable_i = 1;
    const auto r = io.wait_any(io.q_adp, 5000);
    const unsigned after = word40(ask(AEM_GET_CONFIGURATION, {}));
    agree(r, after, "b after reset (the value GET serves)");
    // (c) refused on the row as the reboot left it
    io.flush_all();
    s = set_configuration(9);
    CHECK(status(s) == AECP_BAD_ARGUMENTS && word40(s) == after,
          "PROBE c: SET(9) BAD_ARGUMENTS echoing %u, got %d %u", after, status(s),
          word40(s));
    agree(io.wait_any(io.q_adp, 9800), after, "c refused SET after reboot");
    // (d) another controller locks; this controller's SET is refused
    std::vector<uint8_t> lock(16, 0);
    io.q_aecp.clear();
    io.feed(aecp_frame(OWN_MAC, 0x0202C2C2C2C2ull, 0, 0, EID, CTLR2_EID, 0xC051,
                       0x0001, lock));
    const auto lk = io.wait_any(io.q_aecp, 600);
    CHECK(status(lk) == AECP_SUCCESS, "PROBE d: controller 2 locks, got %d",
          status(lk));
    io.flush_all();
    s = set_configuration(after == 0 ? 1 : 0);
    CHECK(status(s) == AECP_ENTITY_LOCKED && word40(s) == after,
          "PROBE d: SET refused ENTITY_LOCKED echoing %u, got %d %u", after,
          status(s), word40(s));
    agree(io.wait_any(io.q_adp, 9800), after, "d ENTITY_LOCKED refusal");
  }
'''
text = text.replace(anchor, anchor + probe)
run_anchor = "  void run() {\n    boot();\n    boot_gate_holds_over_the_delay_span();"
assert text.count(run_anchor) == 1, "run anchor drifted"
text = text.replace(run_anchor, helper + run_anchor)
src.write_text(text)
print("probe planted in", src)
