#!/usr/bin/env python3
"""Plant one RTL or input defect per scratch copy and run the workflow's --check on it.
Usage: plant_probes.py <repo-root> <scratch-dir> <jobs>. Reports rc per plant; rc 0 is a miss."""
import contextlib, io, json, re, shutil, sys, tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
root, scratch, jobs = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), int(sys.argv[3])
sys.dont_write_bytecode = True
sys.path.insert(0, str(root / "scripts"))
RTL = "hdl/common/csr/milan_csr.sv"
GEN = "hdl/common/csr/gen/lwsrp_csr_defaults.svh"
SHAPE = "configs/generated/endstation_ax7101_1x1_tdm8/gen/adp_shape_defaults.svh"
DP = "hdl/milan/milan_datapath.sv"
ADDR = "A_GPTP_LAT   = 'h7F0;"
def sub(old, new, count=1, rel=RTL):
    def f(r):
        p = r / rel; t = p.read_text(encoding="utf-8")
        if old not in t:
            raise AssertionError(f"plant text absent: {old!r}")
        p.write_text(t.replace(old, new, count), encoding="utf-8")
    return f
def resub(pat, new, rel=RTL):
    def f(r):
        p = r / rel; t = p.read_text(encoding="utf-8")
        t2, n = re.subn(pat, new, t)
        if not n:
            raise AssertionError(f"plant pattern absent: {pat!r}")
        p.write_text(t2, encoding="utf-8")
    return f
def chain(*fs):
    def f(r):
        for g in fs:
            g(r)
    return f
PLANTS = [
 ("control: no plant", lambda r: None, "pass"),
 # --- new register
 ("REG plain new localparam in a module", sub(ADDR, ADDR + "\n  localparam [ADDR_WIDTH-1:0] A_PLANTED = 'h7F4;"), "fail"),
 ("REG new live read arm with its own label", chain(sub(ADDR, ADDR + "\n  localparam [ADDR_WIDTH-1:0] A_PLANTED = 'h7F4;"),
     sub("A_GPTP_LAT: begin", "A_PLANTED: live_mux = 32'h1234;\n      A_GPTP_LAT: begin")), "fail"),
 ("REG new range window named _BASE/_END with a read term", chain(
     sub(ADDR, ADDR + "\n  localparam [ADDR_WIDTH-1:0] A_PLANTW_BASE = 'h7F4;\n  localparam [ADDR_WIDTH-1:0] A_PLANTW_END = 'h7FC;"),
     sub("        else if (rd_addr_q >= A_RSVD_GAP_BASE", "        else if (rd_addr_q >= A_PLANTW_BASE && rd_addr_q < A_PLANTW_END)\n          live_mux = 32'h1234;\n        else if (rd_addr_q >= A_RSVD_GAP_BASE")), "fail"),
 ("REG literal-addressed read arm (no A_ label)", sub("A_GPTP_LAT: begin", "16'h7F8: live_mux = 32'h1234;\n      A_GPTP_LAT: begin"), "fail"),
 ("REG literal-addressed read inside strm mux (0x86C hole value)", sub("strm_mux = 32'hDEAD_DEAD;    //! window hole", "strm_mux = 32'h1234_5678;    //! window hole"), "fail"),
 ("REG offset moved", sub("A_MC_HI   = 'h118", "A_MC_HI   = 'h120"), "fail"),
 ("REG STAT count NS 9 to 10", sub("localparam int NS = 9;", "localparam int NS = 10;"), "fail"),
 ("REG read arm deleted", sub("      A_AAF_FRAMES: live_mux = i_aaf_frames;\n", ""), "fail"),
 # --- renamed field
 ("FIELD rename output port (undescribed)", resub(r"\bo_tcam_wr_action\b", "o_tcam_act_renamed"), "fail"),
 ("FIELD rename output port (described)", resub(r"\bo_eth_guard\b", "o_eth_lock"), "fail"),
 ("FIELD rename input read as a whole word", resub(r"\bi_aaf_frames\b", "i_aaf_frm_renamed"), "fail"),
 ("FIELD rename setter input", resub(r"\bi_evt_link_change\b", "i_evt_link_flip"), "fail"),
 ("FIELD rename a term of a ternary read (CHMAP_LOOP subfield order)", sub("cmrd_data_r[14], cmrd_data_r[13],                      // [17] fed, [16] mapped", "cmrd_data_r[13], cmrd_data_r[14],                      // swapped"), "fail"),
 ("FIELD move inside a packed input read", sub("A_ADP_DIAG:   live_mux = {14'd0, i_adp_depart_src, i_adp_rearm_cnt, i_adp_depart_cnt};", "A_ADP_DIAG:   live_mux = {14'd0, i_adp_depart_src, i_adp_depart_cnt, i_adp_rearm_cnt};"), "fail"),
 ("FIELD new consumer of a reserved stored bit", sub("  assign o_tone_enable      = tone_ctrl[0];", "  assign o_tone_enable      = tone_ctrl[0];\n  assign o_mac_new = mac_ctrl[7];"), "fail"),
 # --- changed reset
 ("RESET csr_default of a shadow word", sub("A_MAC_IFG[10:0]:    csr_default = 32'h0C;", "A_MAC_IFG[10:0]:    csr_default = 32'h0D;"), "fail"),
 ("RESET flop of a shadow word (mac_ifg) only", sub("mac_ifg <= 32'h0C;", "mac_ifg <= 32'h0D;"), "fail"),
 ("RESET flop of a shadow word (mac_ctrl) only", sub("mac_ctrl <= 32'h13;", "mac_ctrl <= 32'h12;"), "fail"),
 ("RESET flop of a shadow word (tcam_ctrl) only", sub("tcam_ctrl <= 32'h1;", "tcam_ctrl <= 32'h0;"), "fail"),
 ("RESET flop of a live word (ltap_en_r)", sub("ltap_en_r  <= 1'b1;", "ltap_en_r  <= 1'b0;"), "fail"),
 ("RESET eth_guard flop", sub("eth_guard <= 1'b1;", "eth_guard <= 1'b0;"), "fail"),
 ("RESET generated LWSRP_VID header", sub("LWSRP_VID_RST_C       = 32'h0000_0002", "LWSRP_VID_RST_C       = 32'h0000_0003", rel=GEN), "fail"),
 ("RESET generated LWSRP_LATENCY header (flop only)", sub("LWSRP_LATENCY_RST_C   = 32'h0000_0000", "LWSRP_LATENCY_RST_C   = 32'h0000_0009", rel=GEN), "fail"),
 ("RESET CBS table", sub("'{38, 76, 76, 228, 684}", "'{38, 76, 76, 228, 685}"), "fail"),
 ("RESET CHMAP poison constant", sub("CHMAP_LOOP_POISON_C = 32'hDEAD_DEAD", "CHMAP_LOOP_POISON_C = 32'hBEEF_BEEF"), "fail"),
 ("RESET PPS width expression", sub("A_PPS_WIDTH:  live_mux = PPS_P ? 32'(PPS_WIDTH_CYC_P) : 32'h0;", "A_PPS_WIDTH:  live_mux = PPS_P ? 32'(PPS_WIDTH_CYC_P) : 32'h7;"), "fail"),
 ("RESET snapshot shadow reset value", sub("for (int w = 0; w < 12; w++) snap_shadow_r[w] <= 32'h0;", "for (int w = 0; w < 12; w++) snap_shadow_r[w] <= 32'h5;"), "fail"),
 ("RESET version parameter", sub("VERSION = 32'h0002_0060", "VERSION = 32'h0002_0061"), "fail"),
 ("RESET shape ADP talker source count", resub(r"ADP_TALKER_SRC_C\s*=\s*(\d+)", "ADP_TALKER_SRC_C = 7", rel=SHAPE), "fail"),
 ("RESET datapath parameter expression", sub(".MILAN_CLK_FREQ_HZ_P(MILAN_CLK_FREQ_HZ)", ".MILAN_CLK_FREQ_HZ_P(MILAN_CLK_FREQ_HZ * 2)", rel=DP), "fail"),
 # --- write behaviour
 ("WRITE guard dropped from PHY_RST", sub("A_PHY_RST:   if (!eth_guard) phy_rst <= s_axi_wdata;", "A_PHY_RST:   phy_rst <= s_axi_wdata;"), "fail"),
 ("WRITE LINK_CTRL mask moved", sub("? {s_axi_wdata[31:2], 1'b0, s_axi_wdata[0]}\n", "? {s_axi_wdata[31:3], 1'b0, s_axi_wdata[1:0]}\n"), "fail"),
 ("WRITE new doorbell in a write arm", sub("A_SCRATCH:   scratch  <= s_axi_wdata;", "A_SCRATCH: begin scratch <= s_axi_wdata; pps_arm_p <= 1'b1; end"), "fail"),
 ("WRITE arm uses a masked store (unparsed form)", sub("A_CHMAP_SEL:  chmap_sel  <= s_axi_wdata;", "A_CHMAP_SEL:  chmap_sel  <= s_axi_wdata & 32'h1FF;"), "fail"),
 ("WRITE arm removed from a shadow word's flop", sub("A_MAC_IFG:   mac_ifg  <= s_axi_wdata;\n", ""), "fail"),
 ("WRITE plain_rw membership dropped", sub("A_SCRATCH, A_IRQ_MASK,", "A_IRQ_MASK,"), "fail"),
 ("WRITE read clears a status (RC behaviour outside the case)", sub("      if (i_evt_link_change)   irq_status[1] <= 1'b1;", "      if (rd_fire && rd_addr == A_IRQ_STATUS) irq_status[1] <= 1'b0;\n      if (i_evt_link_change)   irq_status[1] <= 1'b1;"), "fail"),
 ("WRITE doorbell decoded outside the case", sub("  wire sel_wr_w   = wr_fire && (wr_addr == A_STRM_SEL);", "  wire sel_wr_w   = wr_fire && (wr_addr == A_STRM_SEL);\n  wire plant_w = wr_fire && (wr_addr == A_SCRATCH);"), "n/a"),
 ("WRITE guard key changed", sub("(s_axi_wdata != 32'h554E_4C4B)", "(s_axi_wdata != 32'h554E_4C4C)"), "fail"),
 # --- SoC
 ("SOC bank origin edited", sub('"origin": 4026537984', '"origin": 4026540032', rel="scripts/register_map_soc.json"), "fail"),
 ("SOC bank register moved, not on the page table", sub('"address": 4026531840', '"address": 4026531844', rel="scripts/register_map_soc.json"), "n/a"),
 ("SOC csr_csv hash edited", resub(r'"csr_csv_sha256": "[0-9a-f]+"', '"csr_csv_sha256": "00"', rel="scripts/register_map_soc.json"), "n/a"),
 ("SOC unused constant edited", resub(r'"milan_sr_vid": 2', '"milan_sr_vid": 3', rel="scripts/register_map_soc.json"), "n/a"),
 # --- docs
 ("DESC unknown register key", sub('"registers": {', '"registers": {"PLANTED": {},', rel="scripts/register_descriptions.json"), "fail"),
]
def one(index):
    name, plant, want = PLANTS[index]
    from register_selftest import copy_inputs
    from gen_register_reference import main
    with tempfile.TemporaryDirectory(dir=scratch, prefix="plant-") as tmp:
        r = Path(tmp)
        copy_inputs(r)
        (r / "docs/diagrams").mkdir(parents=True, exist_ok=True)
        (r / "docs/diagrams/memory_map.svg").write_bytes((root / "docs/diagrams/memory_map.svg").read_bytes())
        try:
            plant(r)
        except AssertionError as exc:
            return name, -1, want, str(exc)
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                rc = main(["--check"], root=r)
        except Exception as exc:
            rc = f"crash:{type(exc).__name__}"
            buf.write(str(exc))
        page = r / "docs/reference/REGISTER_MAP.md"
        before = page.read_text(encoding="utf-8") if page.exists() else ""
        buf2 = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf2):
                wrc = main(["--write"], root=r)
        except Exception as exc:
            wrc = f"crash:{type(exc).__name__}"
        after = page.read_text(encoding="utf-8") if page.exists() else ""
        a, b = set(before.splitlines()), set(after.splitlines())
        delta = sorted(b - a)[:3]
        return name, rc, want, " ".join(buf.getvalue().split())[:170] + f" || --write rc={wrc} page lines changed={len(b-a)} sample={[d[:110] for d in delta]}"
if __name__ == "__main__":
    with ProcessPoolExecutor(jobs, mp_context=__import__('multiprocessing').get_context('fork')) as ex:
        res = list(ex.map(one, range(len(PLANTS))))
    miss = 0
    for name, rc, want, out in res:
        tag = "ok" if (want == "fail" and rc not in (0, -1)) or (want == "pass" and rc == 0) else ("MISS" if want == "fail" and rc == 0 else ("info" if want == "n/a" else "ERROR"))
        miss += tag == "MISS"
        print(f"{tag:5} rc={rc} [{name}] {out}")
    print("plants:", len(res), "misses:", miss)
