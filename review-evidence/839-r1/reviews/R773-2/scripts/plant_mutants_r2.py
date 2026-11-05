#!/usr/bin/env python3
"""Write reviewer-planted mutants of hdl/milan/milan_datapath.sv into argv[2].
PM1-PM4 are the round-1 probes unchanged; PM5 is new in round 2.
Each edit must match exactly once. Usage: plant_mutants_r2.py <datapath.sv> <outdir>"""
import sys
from pathlib import Path
src = Path(sys.argv[1]).read_text(); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
G = "  assign maap_tx_tvalid    = maap_txs_tvalid_w & tx_sa_ok_w;\n  assign maap_txs_tready_w = maap_tx_tready    & tx_sa_ok_w;\n  assign aaf_tx_tvalid     = aaf_txs_tvalid_w  & tx_sa_ok_w;\n  assign aaf_txs_tready_w  = aaf_tx_tready     & tx_sa_ok_w;\n  assign crft_tx_tvalid    = crft_txs_tvalid_w & tx_sa_ok_w;\n  assign crft_txs_tready_w = crft_tx_tready    & tx_sa_ok_w;\n"
M = {
 # PM1: the hold removed from MAAP, AAF and CRF only (processor lane still held)
 "PM1_nohold_maap_aaf_crf": [(G, G.replace(" & tx_sa_ok_w", ""))],
 # PM2: the processor lane's tvalid held but its tready passed through
 "PM2_pp_tready_ungated": [("  assign pp_txs_tready_w   = pp_tx_tready_w    & tx_sa_ok_w;\n",
                           "  assign pp_txs_tready_w   = pp_tx_tready_w;\n")],
 # PM3: the stamp's beat position wraps instead of saturating (stamps payload octets)
 "PM3_stamp_wraps": [("      else if (ctl_sa_idx_r != TX_SA_IW_C'(TX_SA_BEATS_C)) ctl_sa_idx_r <= ctl_sa_idx_r + 1'b1;",
                     "      else                                                 ctl_sa_idx_r <= ctl_sa_idx_r + 1'b1;")],
 # PM4: a later write to an unrelated CSR (MAC_CTRL) re-closes the hold
 "PM4_reclose_on_mac_ctrl": [("      if (s_axi_awaddr == MAC_AHI_ADDR_C) mac_ahi_wr_r <= 1'b1;\n",
                             "      if (s_axi_awaddr == MAC_AHI_ADDR_C) mac_ahi_wr_r <= 1'b1;\n      if (s_axi_awaddr == 16'h0100) mac_ahi_wr_r <= 1'b0;\n")],
 # PM5 (new): the stamp flips bit 0 of control-lane frame octet 15 (beat 1, lane 7),
 # outside the source address, leaving EtherType, subtype and both addresses intact
 "PM5_octet15_bitflip": [("          ctlg2_tdata[8*ln +: 8] = cfg_mac_addr[8*(b * int'(TX_SA_BPB_C) + ln - 6) +: 8];\n  end : ctl_sa_stamp",
                          "          ctlg2_tdata[8*ln +: 8] = cfg_mac_addr[8*(b * int'(TX_SA_BPB_C) + ln - 6) +: 8];\n    if (ctl_sa_idx_r == TX_SA_IW_C'(1)) ctlg2_tdata[56] = ~ctlg_src_tdata_w[56];\n  end : ctl_sa_stamp")],
}
for name, edits in M.items():
    t = src
    for a, b in edits:
        n = t.count(a)
        if n != 1: sys.exit(f"{name}: pattern occurs {n} times")
        t = t.replace(a, b)
    (out / f"{name}.sv").write_text(t); print("planted", name)
