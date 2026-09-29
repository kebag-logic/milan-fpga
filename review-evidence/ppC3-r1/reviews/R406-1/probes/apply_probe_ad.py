#!/usr/bin/env python3
"""Reviewer probe: insert RP1-RP3 into a SCRATCH copy of tb/pp_top/sim_main.cpp.

RP1: a rejected SET_CONFIGURATION on a written row moves neither GET nor the ADPDU.
RP2: after SET(0) and a processor reset, GET and the ADPDU both return to the image default.
RP3: a rejected SET_CONFIGURATION on the unset row does not mark it written.
usage: apply_probe_ad.py <scratch tree root>
"""
import sys
from pathlib import Path

ANCHOR = ('    CHECK(e == avail(aidx_of(c) + 1, IMAGE_CFG),\n'
          '          "AD4: the set configuration outranks a moved current_cfg_i");\n'
          '    io.d->current_cfg_i = IMAGE_CFG;\n'
          '  }\n')
PROBE = r'''    CHECK(e == avail(aidx_of(c) + 1, IMAGE_CFG),
          "AD4: the set configuration outranks a moved current_cfg_i");
    io.d->current_cfg_i = IMAGE_CFG;
    probe_rejected_set_on_written_row(e);
    probe_reset_then_rejected_set_on_unset_row();
  }

  std::vector<uint8_t> enable_and_first_advert() {
    io.d->link_up_i = 1;
    io.d->entity_enable_i = 1;
    return io.wait_any(io.q_adp, 9800);
  }

  void probe_rejected_set_on_written_row(const std::vector<uint8_t>& before) {
    io.flush_all();
    const auto s = set_configuration(7);        // configurations_count is 2
    CHECK(status(s) == AECP_BAD_ARGUMENTS && word40(s) == IMAGE_CFG,
          "RP1: SET_CONFIGURATION(7) BAD_ARGUMENTS echoing %u, got %d / %u",
          IMAGE_CFG, status(s), word40(s));
    CHECK(word40(ask(AEM_GET_CONFIGURATION, {})) == IMAGE_CFG,
          "RP1: GET_CONFIGURATION still reads %u", IMAGE_CFG);
    const auto f = io.wait_any(io.q_adp, 9800);
    only_the_index_moved(before, f, IMAGE_CFG, "RP1");
  }

  void probe_reset_then_rejected_set_on_unset_row() {
    io.flush_all();
    const auto s0 = set_configuration(0);
    CHECK(status(s0) == AECP_SUCCESS && word40(s0) == 0,
          "RP2: SET_CONFIGURATION(0) SUCCESS before the reset");
    const auto z = io.wait_any(io.q_adp, 9800);
    CHECK(z.size() == 82 && ((unsigned(z[64]) << 8) | z[65]) == 0,
          "RP2: the advert before the reset carries 0");
    boot();                                     // rst_n pulse, image default 1
    const auto a = enable_and_first_advert();
    CHECK(a == avail(0, IMAGE_CFG),
          "RP2: after reset the first ENTITY_AVAILABLE carries the image default");
    CHECK(word40(ask(AEM_GET_CONFIGURATION, {})) == IMAGE_CFG,
          "RP2: after reset GET_CONFIGURATION reads the image default");
    io.flush_all();
    const auto s = set_configuration(2);        // == configurations_count
    CHECK(status(s) == AECP_BAD_ARGUMENTS && word40(s) == IMAGE_CFG,
          "RP3: SET_CONFIGURATION(2) on the unset row BAD_ARGUMENTS echoing %u, "
          "got %d / %u", IMAGE_CFG, status(s), word40(s));
    CHECK(word40(ask(AEM_GET_CONFIGURATION, {})) == IMAGE_CFG,
          "RP3: GET_CONFIGURATION still reads the image default");
    const auto f = io.wait_any(io.q_adp, 9800);
    only_the_index_moved(a, f, IMAGE_CFG, "RP3");
    printf("RP: reviewer probe arms ran\n");
  }
'''

src = Path(sys.argv[1]) / "tb" / "pp_top" / "sim_main.cpp"
text = src.read_text()
assert text.count(ANCHOR) == 1, "anchor not unique"
src.write_text(text.replace(ANCHOR, PROBE))
print("probe inserted")
