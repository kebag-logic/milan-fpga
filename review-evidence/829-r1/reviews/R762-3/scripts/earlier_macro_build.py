#!/usr/bin/env python3
"""Convert the planted datapath the way syn/yosys/run.sh does and read the plane.

Usage: earlier_macro_build.py <clone root> <macro> <shipped|planted>. Prints the
macros earlier sources define at file scope, then the plane's parameter bindings
in the converted Verilog. Works on a temporary copy; the clone is not edited.
"""
import pathlib, re, subprocess, sys, tempfile, time
sys.dont_write_bytecode = True
root = pathlib.Path(sys.argv[1]).resolve(); macro = sys.argv[2]; mode = sys.argv[3]
sys.path.append(str(root / "syn/ooc"))
import dp_srcs
rec, _p, _s = dp_srcs.ask_authority("milan_datapath")
srcs = rec["src"]; dp = next(s for s in srcs if s.endswith("/milan_datapath.sv"))
rtl = pathlib.Path(dp).read_text()
line = "        .ETH_CYC_PER_OCTET_P(GPTP_ETH_CYC_PER_OCTET_P),"
text = rtl if mode == "shipped" else rtl.replace(line, f"`ifndef {macro}\n{line.strip()}\n`endif", 1)
names = sorted({m for s in srcs[:srcs.index(dp)] for m in re.findall(
    r"^\s*`define\s+(\w+)", pathlib.Path(s).read_text(errors="replace"), re.M)})
print(f"macros earlier sources define: {len(names)}; first ten: {names[:10]}")
with tempfile.TemporaryDirectory() as tmp:
    copy = pathlib.Path(tmp) / "milan_datapath.sv"; copy.write_text(text)
    cmd = ["sv2v", "--top=milan_datapath", *(f"-D{d}" for d in rec["define"]), "-I", str(root / "hdl/milan"),
           *(a for d in rec["incdir"] for a in ("-I", d)), *[str(copy) if s == dp else s for s in srcs]]
    t = time.time(); out = subprocess.run(cmd, capture_output=True, text=True, timeout=540)
print(f"{mode}: sv2v --top rc {out.returncode} in {time.time()-t:.0f}s; {out.stderr[:200]}")
m = re.search(r"^\s*KL_gptp_shadow\w*\s*#\((.*?)^\s*\)\s*\S*u_gptp_shadow", out.stdout, re.M | re.S)
print("plane bindings:", re.findall(r"\.(\w*(?:TICK_NS|CYC_PER_OCTET)\w*)\((.*?)\)", m.group(1)) if m else "plane statement not found")
