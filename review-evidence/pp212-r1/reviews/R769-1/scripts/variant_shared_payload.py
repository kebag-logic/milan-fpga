#!/usr/bin/env python3
"""Area probe (disposable): route the settle's seeded payload through one shared
payload bus (the decoder value, or on a settle clock, which carries none, the
port registrar's payload) into the sink registrars, instead of a second
per-sink write path. Usage: variant_shared_payload.py <tree>"""
import sys, pathlib
f = pathlib.Path(sys.argv[1]) / "hdl/srp/KL_srp_listener_fsm.sv"
t = f.read_text()
def sub(old, new):
    global t
    assert t.count(old) == 1, old
    t = t.replace(old, new)
sub("""  always_ff @(posedge clk_i) begin : reg_plane
""", """  // area probe: one payload bus for both sink write paths
  logic [31:0] pl_lat_w;
  logic [7:0]  pl_fc_w;
  logic [63:0] pl_fs_w;
  assign pl_lat_w = evt_valid_i ? evt_acc_latency_i       : seed_lat_w;
  assign pl_fc_w  = evt_valid_i ? evt_failure_code_i      : seed_fcode_w;
  assign pl_fs_w  = evt_valid_i ? evt_failure_system_id_i : seed_fsys_w;
  always_ff @(posedge clk_i) begin : reg_plane
""")
sub("""          lat_r[s]   <= evt_acc_latency_i;   // refresh re-latches (10 §6.4)""",
    """          lat_r[s]   <= pl_lat_w;   // refresh re-latches (10 §6.4)""")
sub("""          if (rx_is_failed_w) begin
            fcode_r[s]  <= evt_failure_code_i;
            fsysid_r[s] <= evt_failure_system_id_i;
          end
          if (ind_reg_w[s])""", """          if (rx_is_failed_w) begin
            fcode_r[s]  <= pl_fc_w;
            fsysid_r[s] <= pl_fs_w;
          end
          if (ind_reg_w[s])""")
sub("""          lat_r[s]    <= 32'd0;
          fcode_r[s]  <= 8'd0;
          fsysid_r[s] <= 64'd0;""", """          lat_r[s]    <= seed_v_w ? pl_lat_w : 32'd0;
          fcode_r[s]  <= seed_v_w ? pl_fc_w  : 8'd0;
          fsysid_r[s] <= seed_v_w ? pl_fs_w  : 64'd0;""")
sub("""            lat_r[s]    <= seed_lat_w;
            fcode_r[s]  <= seed_fcode_w;
            fsysid_r[s] <= seed_fsys_w;
""", "")
f.write_text(t)
print("patched", f)
