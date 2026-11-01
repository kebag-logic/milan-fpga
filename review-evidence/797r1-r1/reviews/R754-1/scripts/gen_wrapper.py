#!/usr/bin/env python3
"""Generate a flat-vector wrapper around milan_csr so a harness can drive any input and
sample any output by bit position. Independent of the generator under review."""
import json, re, sys
rtl, out_sv, out_map = sys.argv[1:4]
PARAMS = dict(NUM_QUEUES=5, ADDR_WIDTH=16, N_LISTENERS_P=1, N_TALKERS_P=1, SRP_LSN0_ROW_P=2,
              GPTP_PLANE_EN_P=1, MILAN_CLK_FREQ_HZ_P=50000000, CHMAP_RDBK_P=3, PPS_P=0, PPS_WIDTH_CYC_P=50000)
t = open(rtl).read()
t = re.sub(r"//[^\n]*", "", t)
t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)
hdr = t[t.index("module milan_csr"):]
hdr = hdr[hdr.index(")(")+2:hdr.index("\n);")]
ports = []
for m in re.finditer(r"\b(input|output)\s+wire\s*(\[[^\]]+\])?\s*(\w+)", hdr):
    ports.append((m.group(1), m.group(2) or "[0:0]", m.group(3)))
def w(r):
    hi, lo = r[1:-1].split(":")
    env = dict(PARAMS)
    return eval(hi.replace("/", "//"), {}, env) - eval(lo, {}, env) + 1
ins, outs, ipos, opos = [], [], 0, 0
imap, omap = {}, {}
for d, r, n in ports:
    if n in ("aclk", "aresetn") or n.startswith("s_axi"): continue
    W = w(r)
    if d == "input":
        ins.append((n, W, ipos)); imap[n] = [ipos, W]; ipos += W
    else:
        outs.append((n, W, opos)); omap[n] = [opos, W]; opos += W
s = ["`default_nettype none", "module tb_top(input wire aclk, input wire aresetn,",
     " input wire [15:0] awaddr, input wire awvalid, output wire awready, input wire [31:0] wdata, input wire wvalid,",
     " output wire wready, output wire bvalid, input wire bready, input wire [15:0] araddr, input wire arvalid,",
     " output wire arready, output wire [31:0] rdata, output wire rvalid, input wire rready,",
     f" input wire [{ipos-1}:0] all_in, output wire [{opos-1}:0] all_out);",
     " wire [1:0] bresp, rresp;",
     " milan_csr #(" + ",".join(f".{k}({v})" for k, v in PARAMS.items()) + ") dut(.aclk,.aresetn,",
     " .s_axi_awaddr(awaddr),.s_axi_awvalid(awvalid),.s_axi_awready(awready),.s_axi_wdata(wdata),.s_axi_wstrb(4'hF),",
     " .s_axi_wvalid(wvalid),.s_axi_wready(wready),.s_axi_bresp(bresp),.s_axi_bvalid(bvalid),.s_axi_bready(bready),",
     " .s_axi_araddr(araddr),.s_axi_arvalid(arvalid),.s_axi_arready(arready),.s_axi_rdata(rdata),.s_axi_rresp(rresp),",
     " .s_axi_rvalid(rvalid),.s_axi_rready(rready),"]
for n, W, p in ins: s.append(f" .{n}(all_in[{p}+:{W}]),")
for i, (n, W, p) in enumerate(outs):
    s.append(f" .{n}(all_out[{p}+:{W}])" + ("," if i < len(outs)-1 else ""))
s += [" );", " wire _u = &{1'b0, bresp, rresp};", "endmodule", "`default_nettype wire"]
open(out_sv, "w").write("\n".join(s) + "\n")
json.dump(dict(inputs=imap, outputs=omap, in_bits=ipos, out_bits=opos, params=PARAMS), open(out_map, "w"), indent=1)
print("inputs", len(ins), ipos, "outputs", len(outs), opos)
