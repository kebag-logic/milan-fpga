#!/usr/bin/env python3
"""Dual-instance differential on the gptp_shadow suite's stimulus (R593-2).

Usage: python3 -I make_shadow_dual.py <exact-head tree copy> <out dir> <dev dir>

<dev dir> holds the `_dev`-suffixed dev-base copies made for make_dual.py.
Writes into <out dir>:
  gptp_shadow_wrap_head.sv  the exact-head slice wrapper, module renamed
  gptp_shadow_wrap.sv       a top with the wrapper's own ports that runs the
                            head slice (driving every output) and the dev-base
                            slice side by side on the same inputs, compares
                            every output each cycle outside reset, and prints
                            the result from a `final` block
  sim_main.cpp              the suite's harness, unchanged
The raw result-face debug outputs (dbg_eng_txts_{ns,seq,type,ok,gen}) are
compared only on an accepted beat (dbg_eng_txts_v_o), as the engine samples
them; their idle divergence is counted separately as information.
"""
import re
import sys
from pathlib import Path

tree, out, dev = (Path(a) for a in sys.argv[1:4])
suite = tree / "tb/verilator/gptp_shadow"
src = (suite / "gptp_shadow_wrap.sv").read_text()
out.mkdir(parents=True, exist_ok=True)
(out / "gptp_shadow_wrap_head.sv").write_text(
    re.sub(r"\bgptp_shadow_wrap\b", "gptp_shadow_wrap_head", src))
(out / "sim_main.cpp").write_text((suite / "sim_main.cpp").read_text())

start = src.index("module gptp_shadow_wrap #(")
end = src.index("\n);", start) + 3
header = src[start:end]
ports = []
for m in re.finditer(r"^\s*(input|output)\s+(wire|logic)\s*(signed\s*)?(\[[^\]]+\])?\s*(\w+)\s*,?",
                     header, re.M):
    ports.append((m.group(1), m.group(3) or "", m.group(4) or "", m.group(5)))
assert len(ports) > 40, len(ports)
params = re.findall(r"parameter\s+[\w\s]+?\s(\w+)\s*=", header)

raw = {"dbg_eng_txts_ns_o", "dbg_eng_txts_seq_o", "dbg_eng_txts_type_o",
       "dbg_eng_txts_ok_o", "dbg_eng_txts_gen_o"}
skip = {"clk_i", "rst_n"}
outs = [p for p in ports if p[0] == "output"]
ins = [p for p in ports if p[0] == "input"]

lines = [header.replace("module gptp_shadow_wrap #(", "module gptp_shadow_wrap #("), ""]
pmap = ", ".join(f".{p}({p})" for p in params)
lines.append(f"  gptp_shadow_wrap_head #({pmap}) u_bench (.*);")
for d, s, w, n in outs:
    lines.append(f"  wire {s}{w} d_{n};")
conns = [f".{n}({n})" for _, _, _, n in ins] + [f".{n}(d_{n})" for _, _, _, n in outs]
lines.append(f"  gptp_shadow_wrap_dev #({pmap}) u_dev (\n      " + ",\n      ".join(conns) + ");")
terms = []
for _, _, _, n in outs:
    if n in raw:
        terms.append((n, f"(dbg_eng_txts_v_o && ({n} != d_{n}))"))
    else:
        terms.append((n, f"({n} != d_{n})"))
lines.append(f"  logic [{len(terms)-1}:0] dd_w;")
for i, (n, t) in enumerate(terms):
    lines.append(f"  assign dd_w[{i}] = {t};")
rawexpr = " || ".join(f"({n} != d_{n})" for n in sorted(raw) if any(n == p[3] for p in outs))
lines.append(f"""
  logic [63:0] dd_cyc_r = 0, dd_cmp_r = 0, dd_mm_r = 0, dd_raw_r = 0, dd_txb_r = 0, dd_res_r = 0;
  logic [63:0] dd_first_r = '1;
  logic [{len(terms)-1}:0] dd_seen_r = '0;
  always_ff @(posedge clk_i) begin : dual_count
    dd_cyc_r <= dd_cyc_r + 1;
    if (rst_n) begin
      dd_cmp_r <= dd_cmp_r + 1;
      if (|dd_w) begin
        dd_mm_r <= dd_mm_r + 1;
        dd_seen_r <= dd_seen_r | dd_w;
        if (dd_first_r == '1) dd_first_r <= dd_cyc_r;
      end
      if (!dbg_eng_txts_v_o && ({rawexpr})) dd_raw_r <= dd_raw_r + 1;
      if (tx_tvalid_o && tx_tready_i) dd_txb_r <= dd_txb_r + 1;
      if (dbg_eng_txts_v_o) dd_res_r <= dd_res_r + 1;
    end
  end : dual_count
  final begin
    $display("SHADOW-DUAL: %0d cycles, %0d compared, %0d mismatching, first at %0d, %0d tx beats, %0d results accepted, %0d idle raw-face cycles differ",
             dd_cyc_r, dd_cmp_r, dd_mm_r, dd_first_r, dd_txb_r, dd_res_r, dd_raw_r);""")
for i, (n, _) in enumerate(terms):
    lines.append(f'    if (dd_seen_r[{i}]) $display("SHADOW-DUAL: output {n} differed");')
lines.append('    $display("SHADOW-DUAL: verdict %s", (dd_mm_r == 0) ? "IDENTICAL" : "DIFFERENT");')
lines.append("  end\nendmodule : gptp_shadow_wrap\n")
(out / "gptp_shadow_wrap.sv").write_text("`default_nettype none\n" + "\n".join(lines) + "`default_nettype wire\n")
print(f"{len(ins)} inputs, {len(outs)} outputs compared; params {params}")
