#!/usr/bin/env python3
"""Insert reviewer equivalence probes into a disposable copy of the tree.

Each probe is simulation-only SystemVerilog that compares a register cut by
PR #939 (issue #927) against the expression it replaced, every clock, and
stops the simulation ($fatal) on the first difference. Heartbeat lines show
that the compared state was exercised. Every anchor must occur exactly once.

usage: apply_probes.py <tree-root>
"""
import sys
from pathlib import Path

DMA_ANCHOR = "  end : transfer\n"
DMA_PROBE = DMA_ANCHOR + """
  // reviewer probe: ring_addr_r against the replaced base_r + (index_r & mask_r)
  logic [31:0] probe_mov_q = 32'd0;
  always_ff @(posedge clk_i) begin : probe_ring_addr
    if (rst_n) begin
      if (mover_w) begin
        probe_mov_q <= probe_mov_q + 32'd1;
        if ((probe_mov_q == 32'd0) || (probe_mov_q[13:0] == 14'd0))
          $display("PROBE-DMA mover-owned cycles=%0d", probe_mov_q + 32'd1);
      end
      if (ring_addr_r != (base_r + MBX_ADDR_W_C'(index_r & mask_r))) begin
        $display("PROBE-DMA MISMATCH ring_addr_r=%h formula=%h", ring_addr_r,
                 base_r + MBX_ADDR_W_C'(index_r & mask_r));
        $fatal(1, "PROBE-DMA");
      end
    end
  end : probe_ring_addr
"""

ENC_ANCHOR = "    assign amap_edit_out_enc_w = enc_r;\n"
ENC_PROBE = ENC_ANCHOR + """    // reviewer probe: in every cycle req is high the registered word equals
    // the combinational encode of the fields on the face this cycle
    logic [31:0] probe_req_q = 32'd0;
    always_ff @(posedge axis_clk) begin : probe_enc
      if (axis_resetn && pp_amap_edit_req_w) begin
        probe_req_q <= probe_req_q + 32'd1;
        $display("PROBE-ENC req-high cycle=%0d co=%0d idx=%0d enc_r=%h", probe_req_q + 32'd1,
                 amap_edit_co_w, pp_amap_edit_desc_index_w, enc_r);
        if (enc_r != amap_edit_out_encode(amap_edit_co_w, pp_amap_edit_desc_index_w)) begin
          $display("PROBE-ENC MISMATCH enc_r=%h comb=%h", enc_r,
                   amap_edit_out_encode(amap_edit_co_w, pp_amap_edit_desc_index_w));
          $fatal(1, "PROBE-ENC");
        end
      end
    end : probe_enc
"""

METER_ANCHOR = "  end : meter_engine\n"
METER_PROBE = METER_ANCHOR + """
  // reviewer probe: the replaced grp_ts0_r / 21-bit grp_off_r pair, updated
  // under the replaced conditions, against grp_ref_r and pc_ts0_r
  logic [31:0] probe_ts0_q, probe_pc_q, probe_n_q;
  logic [20:0] probe_off_q;
  always_ff @(posedge clk_i) begin : probe_old_ref
    if (!rst_n) begin
      probe_ts0_q <= '0; probe_off_q <= '0; probe_pc_q <= '0; probe_n_q <= '0;
    end else begin
      if (s2_v_r) begin
        if (s2_pos_w == 4'd0) begin
          probe_ts0_q <= s2_ts_r;
          probe_off_q <= 21'(PDU_NS_C);
        end else if (s2_gap_r || !grp_act_r || s2_tu_edge_w) begin
          probe_off_q <= probe_off_q;
        end else if (!s2_in_bound_w) begin
          probe_off_q <= probe_off_q;
        end else if (s2_pos_w == 4'd15) begin
          probe_pc_q <= probe_ts0_q;
        end else begin
          probe_off_q <= probe_off_q + 21'(PDU_NS_C);
        end
      end
      if (grp_ref_r != (probe_ts0_q + 32'(probe_off_q))) begin
        $display("PROBE-METER REF MISMATCH ref=%h old=%h", grp_ref_r, probe_ts0_q + 32'(probe_off_q));
        $fatal(1, "PROBE-METER");
      end
      if (pc_v_r) begin
        probe_n_q <= probe_n_q + 32'd1;
        if ((probe_n_q == 32'd0) || (probe_n_q[9:0] == 10'd0))
          $display("PROBE-METER group ends=%0d", probe_n_q + 32'd1);
        if (pc_ts0_r != probe_pc_q) begin
          $display("PROBE-METER PC MISMATCH new=%h old=%h", pc_ts0_r, probe_pc_q);
          $fatal(1, "PROBE-METER");
        end
      end
    end
  end : probe_old_ref
"""

EDITS = (
    ("hdl/milan/mailbox/KL_mbx_dma.sv", DMA_ANCHOR, DMA_PROBE),
    ("hdl/milan/milan_datapath.sv", ENC_ANCHOR, ENC_PROBE),
    ("hdl/ieee1722/crf/KL_aaf_clock_meter.sv", METER_ANCHOR, METER_PROBE),
)


def main() -> int:
    root = Path(sys.argv[1])
    for rel, anchor, new in EDITS:
        path = root / rel
        text = path.read_text()
        if text.count(anchor) != 1:
            print(f"FAIL {rel}: anchor found {text.count(anchor)} times")
            return 1
        path.write_text(text.replace(anchor, new))
        print(f"probed {rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
