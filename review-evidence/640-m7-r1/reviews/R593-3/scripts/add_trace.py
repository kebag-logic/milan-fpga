#!/usr/bin/env python3
"""Insert a change trace of the gptp_shadow bench's plane-visible outputs.

Usage: add_trace.py <tree>
Edits <tree>/tb/verilator/gptp_shadow/gptp_shadow_wrap.sv (a disposable copy)
so every cycle on which the traced tuple changes writes one line, with the
cycle number, to review_trace.txt in the run directory. Accepted egress
results are traced only on their accepted beat, the only time the engine
samples them. Run at the base and at the head, the two files must be equal.
"""
import sys
from pathlib import Path

ANCHOR = "endmodule : gptp_shadow_wrap"
BLOCK = r"""
  // ---- reviewer differential trace (disposable copy only) ----
  integer rv_fd;
  longint unsigned rv_cyc;
  logic [1023:0] rv_now, rv_prev;
  initial begin
    rv_fd = $fopen("review_trace.txt", "w");
    rv_cyc = 0;
    rv_prev = '1;
  end
  always_comb begin
    rv_now = '0;
    rv_now = {tx_tdata_o, tx_tkeep_o, tx_tvalid_o, tx_tlast_o, tx_tready_i,
              pub_gm_id_o, pub_parent_id_o, pub_flags_o, pub_pdelay_ns_o,
              pub_offset_o, pub_annq_o, pub_path_count_o, pub_path_gen_o,
              pub_commit_o, pub_disc_o, ts_uncertain_o,
              dbg_tap_drop_o, dbg_rx_drop_o, dbg_tspush_v_o, dbg_tspop_v_o,
              dbg_prog_run_o, dbg_ev_drop_o, dbg_eng_txts_v_o,
              (dbg_eng_txts_v_o ? {dbg_eng_txts_ns_o, dbg_eng_txts_seq_o,
                                   dbg_eng_txts_type_o, dbg_eng_txts_ok_o,
                                   dbg_eng_txts_gen_o} : 89'd0),
              dbg_txts_lost_o, dbg_txts_disc_o, dbg_txts_barr_o,
              dbg_txts_stall_o, dbg_txts_phcl_o, dbg_txts_state_o,
              dbg_txts_torn_o, dbg_phc_adj_o, dbg_recov_req_cnt_o,
              dbg_epi_done_cnt_o, rst_n};
  end
  always @(posedge clk_i) begin
    rv_cyc <= rv_cyc + 1;
    if (rv_now != rv_prev) begin
      $fwrite(rv_fd, "%0d %h\n", rv_cyc, rv_now);
      rv_prev <= rv_now;
    end
  end
  final $fclose(rv_fd);

"""


def main() -> int:
    f = Path(sys.argv[1]) / "tb/verilator/gptp_shadow/gptp_shadow_wrap.sv"
    text = f.read_text(encoding="utf-8")
    if text.count(ANCHOR) != 1:
        print("anchor not found exactly once")
        return 2
    f.write_text(text.replace(ANCHOR, BLOCK + ANCHOR, 1), encoding="utf-8")
    print(f"trace added to {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
