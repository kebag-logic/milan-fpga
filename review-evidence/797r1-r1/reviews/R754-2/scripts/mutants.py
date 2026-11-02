#!/usr/bin/env python3
"""Plant one RTL or input change per scratch tree and run that tree's own --check.
Usage: mutants.py <clone> <scratch-dir> <python-with-wavedrom>. Prints one verdict row per mutant."""
import concurrent.futures as cf, json, os, re, shutil, subprocess, sys
from pathlib import Path
clone, scratch, py = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
RTL = "hdl/common/csr/milan_csr.sv"
PATHS = ["scripts", "hdl/common/csr", "hdl/common/ethernet_packet_pkg.sv", "hdl/milan/milan_datapath.sv",
         "configs/generated/endstation_ax7101_1x1_tdm8", "docs/reference/REGISTER_MAP.md",
         "docs/reference/milan_feature_status.json", "docs/diagrams/README.md", "docs/diagrams/regmap",
         "docs/design/CSR_REGISTER_NOTES.md", "hdl/common/KL_link_guard.sv", "hdl/ieee1722/crf/KL_mmcm_drp_servo.sv"]
def sub(pat, rep, count=1):
    def f(t):
        n, k = re.subn(pat, rep, t, count=count, flags=re.S)
        if not k: raise SystemExit(f"plant missed: {pat}")
        return n
    return f
def rep(a, b):
    def f(t):
        if a not in t: raise SystemExit(f"plant missed: {a}")
        return t.replace(a, b, 1)
    return f
M = [
 # expected-to-fail plants named by the review brief
 ("new register: label, read arm, write arm", RTL, lambda t: rep("A_GPTP_LAT   = 'h7F0;", "A_GPTP_LAT   = 'h7F0;\n  localparam [ADDR_WIDTH-1:0] A_PLANTED = 'h7F8;")(
     rep("A_SCRATCH:   scratch  <= s_axi_wdata;", "A_SCRATCH:   scratch  <= s_axi_wdata;\n          A_PLANTED:   scratch  <= s_axi_wdata;")(t))),
 ("renamed field, described port (o_tone_att)", RTL, lambda t: t.replace("o_tone_att", "o_tone_attn")),
 ("renamed field, described port (o_tcam_wr_index)", RTL, lambda t: t.replace("o_tcam_wr_index", "o_tcam_wr_idx")),
 ("renamed field, undescribed port (o_mcsrv_ps_invert)", RTL, lambda t: t.replace("o_mcsrv_ps_invert", "o_mcsrv_ps_inv")),
 ("reset change: csr_default MAC_CTRL", RTL, rep("A_MAC_CTRL[10:0]:   csr_default = 32'h13;", "A_MAC_CTRL[10:0]:   csr_default = 32'h17;")),
 ("reset change: both ROM and flop MAC_IFG", RTL, lambda t: rep("mac_ifg <= 32'h0C;", "mac_ifg <= 32'h0D;")(rep("A_MAC_IFG[10:0]:    csr_default = 32'h0C;", "A_MAC_IFG[10:0]:    csr_default = 32'h0D;")(t))),
 ("reset change: live-read flop LINK_CTRL", RTL, rep("link_ctrl  <= 32'h0000_0001;", "link_ctrl  <= 32'h0000_0005;")),
 ("reset change: CBS table", RTL, rep("'{38, 76, 76, 228, 684}", "'{39, 76, 76, 228, 684}")),
 ("offset change: A_MC_LO", RTL, rep("A_MC_LO   = 'h114", "A_MC_LO   = 'h120")),
 ("write decode: W1C bit moved", RTL, rep("if (s_axi_wdata[2]) irq_status[2] <= 1'b0;", "if (s_axi_wdata[3]) irq_status[2] <= 1'b0;")),
 ("write decode: TCAM commit bit moved", RTL, rep("if (s_axi_wdata[16]) begin", "if (s_axi_wdata[17]) begin")),
 ("write decode: guard sense inverted on PHY_RST", RTL, rep("A_PHY_RST:   if (!eth_guard) phy_rst <= s_axi_wdata;", "A_PHY_RST:   if (eth_guard) phy_rst <= s_axi_wdata;")),
 ("write decode: guard mask moved to bit 2", RTL, rep("? {s_axi_wdata[31:2], 1'b0, s_axi_wdata[0]}\n                            : s_axi_wdata;", "? {s_axi_wdata[31:3], 1'b0, s_axi_wdata[1:0]}\n                            : s_axi_wdata;")),
 ("read decode: arm deleted (A_SLIP_TDM)", RTL, rep("A_SLIP_TDM:   live_mux = i_slip_tdm;", "")),
 ("read decode: concat bits swapped (MAC_STATUS)", RTL, rep("{ 28'h0, i_full_duplex, i_speed, i_link_up }", "{ 28'h0, i_speed, i_full_duplex, i_link_up }")),
 ("output assign moved (o_mac_tx_en to bit 7)", RTL, rep("assign o_mac_tx_en    = mac_ctrl[0];", "assign o_mac_tx_en    = mac_ctrl[7];")),
 ("plain-RW set: word removed (A_CLS_TCQ)", RTL, rep("A_CLS_REGEN, A_CLS_TCQ,", "A_CLS_REGEN,")),
 ("array end moved: A_LTAP_END", RTL, lambda t: rep("A_APRB_BASE = 'h8B4;", "A_APRB_BASE = 'h8B8;")(rep("A_LTAP_END  = 'h8B4;", "A_LTAP_END  = 'h8B8;")(t))),
 ("VERSION bump", RTL, rep("32'h0002_0060", "32'h0002_0061")),
 ("shape default LWSRP_VID via generated include", "hdl/common/csr/gen/lwsrp_csr_defaults.svh", lambda t: re.sub(r"LWSRP_VID_RST_C\s*=\s*32'h[0-9A-Fa-f_]+", "LWSRP_VID_RST_C = 32'h00000BAD", t, count=1)),
 # silent-drop hunts: the page must change or the generator must refuse
 ("HUNT reset block only: mac_ctrl flop, ROM unchanged", RTL, rep("mac_ctrl <= 32'h13;", "mac_ctrl <= 32'h17;")),
 ("HUNT reset block only: scratch flop, plain-RW", RTL, rep("scratch <= 32'h0;", "scratch <= 32'h5;")),
 ("HUNT literal-address read arm, no A_ label", RTL, rep("A_GPTP_LAT: begin", "16'h7F8: live_mux = i_txarb_diag;\n      A_GPTP_LAT: begin")),
 ("HUNT literal-address write arm, no A_ label", RTL, rep("A_SCRATCH:   scratch  <= s_axi_wdata;", "A_SCRATCH:   scratch  <= s_axi_wdata;\n          16'h7F8:     scratch  <= s_axi_wdata;")),
 ("HUNT 0x86C poison value changed", RTL, rep("else if (rd_addr_q == ADDR_WIDTH'('h86C))\n            strm_mux = 32'hDEAD_DEAD;", "else if (rd_addr_q == ADDR_WIDTH'('h86C))\n            strm_mux = 32'h0000_0000;")),
 ("HUNT carve-out removed: A_SLIP_TDM from rd_in_window", RTL, rep("(rd_addr_q == A_SLIP_TDM) ||", "")),
 ("HUNT carve-out removed: A_MCSRV_CTRL from rd_in_window", RTL, rep("(rd_addr_q == A_MCSRV_CTRL) ||", "")),
 ("HUNT new write block outside the two parsed blocks", RTL, rep("always_ff @(posedge aclk) begin : shadow_sweep", "always_ff @(posedge aclk) begin : extra_wr\n    if (wr_fire && wr_addr == A_CLKV_CTRL) scratch <= s_axi_wdata;\n  end\n  always_ff @(posedge aclk) begin : shadow_sweep")),
 ("HUNT unmatched write statement: self-increment arm", RTL, rep("A_CHMAP_CTRL: chmap_ctrl <= s_axi_wdata;", "A_CHMAP_CTRL: chmap_ctrl <= s_axi_wdata + 32'd1;")),
 ("HUNT unmatched write statement: masked stored word", RTL, rep("A_CHMAP_CTRL: chmap_ctrl <= s_axi_wdata;", "A_CHMAP_CTRL: chmap_ctrl <= s_axi_wdata & 32'h1;")),
 ("HUNT read masked with a non-_P constant", RTL, rep("A_CRF_DELTA:  live_mux = i_crf_delta;", "A_CRF_DELTA:  live_mux = i_crf_delta & 32'h0000_00FF;")),
 ("HUNT read side-effect: clear on read added", RTL, rep("always_ff @(posedge aclk) begin : shadow_sweep", "always_ff @(posedge aclk) begin : extra_rc\n    if (rd_fire && rd_addr == A_IRQ_RAW) irq_mask <= 32'h0;\n  end\n  always_ff @(posedge aclk) begin : shadow_sweep")),
 ("HUNT o_ assign drops a bit for a RESERVED-looking use", RTL, rep("assign o_lpf_enable       = lpf_ctrl[0];", "assign o_lpf_enable       = lpf_ctrl[0] & lpf_ctrl[1];")),
 ("HUNT stored bit consumed internally, not by an assign", RTL, rep("assign o_irq = |(irq_status & irq_mask);", "assign o_irq = |(irq_status & irq_mask) & ~mac_ctrl[9];")),
 ("HUNT window SRP alias removed", RTL, rep("? i_lwsrp_status  ", "? 32'd0  ")),
 ("HUNT new register whose label ends _END", RTL, lambda t: rep("A_GPTP_LAT: begin", "A_PLANT_END: live_mux = i_txarb_diag;\n      A_GPTP_LAT: begin")(rep("A_GPTP_LAT   = 'h7F0;", "A_GPTP_LAT   = 'h7F0;\n  localparam [ADDR_WIDTH-1:0] A_PLANT_END = 'h7F8;")(t))),
 ("HUNT new register whose label lacks the A_ prefix", RTL, lambda t: rep("A_GPTP_LAT: begin", "R_PLANT: live_mux = i_txarb_diag;\n      A_GPTP_LAT: begin")(rep("A_GPTP_LAT   = 'h7F0;", "A_GPTP_LAT   = 'h7F0;\n  localparam [ADDR_WIDTH-1:0] R_PLANT = 'h7F8;")(t))),
 ("HUNT CBS word offset moved in the plain-RW decode", RTL, rep("(a[4:0] == 5'h08) || (a[4:0] == 5'h0C);", "(a[4:0] == 5'h08) || (a[4:0] == 5'h10);")),
 ("CONTROL comment-only RTL edit must stay fresh", RTL, rep("//! ETHERNET GUARD (USER 2026-08-06", "//! ETHERNET  GUARD (USER 2026-08-06")),
]
base = scratch / "mut_base"
if base.exists(): shutil.rmtree(base)
base.mkdir(parents=True)
subprocess.run(f"git -C {clone} archive HEAD {' '.join(PATHS)} | tar -x -C {base}", shell=True, check=True)
def run(i_m):
    i, (name, rel, plant) = i_m
    if plant is None: return i, name, "n/a", "skipped"
    d = scratch / f"mut_{i:02d}"
    if d.exists(): shutil.rmtree(d)
    shutil.copytree(base, d, copy_function=os.link)
    p = d / rel
    t = p.read_text(encoding="utf-8")
    n = plant(t)
    if n == t: return i, name, "PLANT-NOP", ""
    p.unlink(); p.write_text(n, encoding="utf-8")
    r = subprocess.run([py, "-B", str(d / "scripts/gen_register_reference.py"), "--check"], capture_output=True, text=True, cwd=d)
    last = r.stdout.strip().split("\n")
    shutil.rmtree(d)
    return i, name, r.returncode, " / ".join(x for x in last if not x.startswith("STALE docs/diagrams"))[:230]
with cf.ThreadPoolExecutor(16) as ex:
    res = sorted(ex.map(run, enumerate(M)))
for i, name, rc, out in res:
    print(f"{i:02d}\trc={rc}\t{name}\t{out}")
