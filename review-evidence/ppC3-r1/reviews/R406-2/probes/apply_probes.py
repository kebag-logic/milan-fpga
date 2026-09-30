#!/usr/bin/env python3
"""Reviewer probes for PR #136 round 2 (disposable; applied to an exported tree copy only).

--split : an every-clock comparator in tb/pp_top/pp_top_wrap.sv between the
          published configuration-valid flag (dbg_adp_cfg_v_o) and the store's own
          (dbg_dyn_cfg_v_o), printing PROBE-SPLIT on a difference and PROBE-RISE /
          PROBE-FALL on each edge of the store's flag, over every model the run builds.
--refused : two refused-SET_CONFIGURATION arms appended to section AD
          (PR1: on the unset row; PR2: on a written row), each grading the echo,
          GET_CONFIGURATION, both flags and the next ENTITY_AVAILABLE's index.
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1])
modes = set(sys.argv[2:])

if "--split" in modes:
    w = tree / "tb/pp_top/pp_top_wrap.sv"
    s = w.read_text()
    probe = '''
  // ---- reviewer probe (disposable) ----
  logic probe_prev_v_r = 1'b0;
  always @(posedge clk_i) begin
    if (dbg_adp_cfg_v_o !== dbg_dyn_cfg_v_o)
      $display("PROBE-SPLIT %m adp=%0d store=%0d", dbg_adp_cfg_v_o, dbg_dyn_cfg_v_o);
    if (dbg_dyn_cfg_v_o && !probe_prev_v_r) $display("PROBE-RISE");
    if (!dbg_dyn_cfg_v_o && probe_prev_v_r) $display("PROBE-FALL");
    probe_prev_v_r <= dbg_dyn_cfg_v_o;
  end
endmodule : pp_top_wrap'''
    assert s.count("endmodule : pp_top_wrap") == 1
    w.write_text(s.replace("endmodule : pp_top_wrap", probe.lstrip("\n")))

if "--refused" in modes:
    c = tree / "tb/pp_top/sim_main.cpp"
    s = c.read_text()
    anchor = "    a_reset_returns_to_the_image_default();\n  }\n};"
    assert s.count(anchor) == 1
    arms = '''    a_reset_returns_to_the_image_default();
    // ---- reviewer probe PR1: a refused SET on the unset row (IEEE 7.4.7.1) ----
    {
      io.flush_all();
      const auto r = set_configuration(5);     // the image declares 2
      CHECK(status(r) == AECP_BAD_ARGUMENTS && word40(r) == IMAGE_CFG,
            "PR1: SET_CONFIGURATION(5) refused BAD_ARGUMENTS echoing %u (status %d, echo %u)",
            IMAGE_CFG, status(r), word40(r));
      CHECK(!io.d->dbg_dyn_cfg_v_o && !io.d->dbg_adp_cfg_v_o,
            "PR1: both flags stay clear after the refusal");
      CHECK(word40(ask(AEM_GET_CONFIGURATION, {})) == IMAGE_CFG,
            "PR1: GET_CONFIGURATION still reads the image default");
      io.q_adp.clear();
      const auto f = io.wait_any(io.q_adp, 9800);
      CHECK(f.size() == 82 && ((unsigned(f[64]) << 8 | f[65]) == IMAGE_CFG),
            "PR1: the next ENTITY_AVAILABLE still carries the image default");
    }
    // ---- reviewer probe PR2: a refused SET on a written row ----
    {
      io.flush_all();
      CHECK(status(set_configuration(0)) == AECP_SUCCESS, "PR2: SET_CONFIGURATION(0) SUCCESS (premise)");
      const auto r = set_configuration(9);
      CHECK(status(r) == AECP_BAD_ARGUMENTS && word40(r) == 0,
            "PR2: SET_CONFIGURATION(9) refused BAD_ARGUMENTS echoing 0 (status %d, echo %u)",
            status(r), word40(r));
      CHECK(io.d->dbg_dyn_cfg_v_o && io.d->dbg_adp_cfg_v_o && io.d->dbg_dyn_cfg_o == 0,
            "PR2: both flags stay set, the row still 0");
      CHECK(word40(ask(AEM_GET_CONFIGURATION, {})) == 0, "PR2: GET_CONFIGURATION still reads 0");
      io.q_adp.clear();
      const auto f = io.wait_any(io.q_adp, 9800);
      CHECK(f.size() == 82 && ((unsigned(f[64]) << 8 | f[65]) == 0),
            "PR2: the next ENTITY_AVAILABLE still carries 0");
    }
  }
};'''
    c.write_text(s.replace(anchor, arms))
print("probes applied:", sorted(modes))
