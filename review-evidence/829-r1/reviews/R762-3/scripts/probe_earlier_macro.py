#!/usr/bin/env python3
"""Does gate 1h see a macro an earlier source of the build defines?

Usage: probe_earlier_macro.py <clone root>. Reads the build's source order from
run.sh --emit, picks a macro an earlier source defines outside any include, and
plants a binding live only where that macro is absent. Asks the whole-list front
end whether the binding survives and asks the gate what it answers.
"""
import importlib.util, pathlib, re, subprocess, sys, tempfile
root = pathlib.Path(sys.argv[1]).resolve()
sys.argv = [sys.argv[0]]
sys.path.insert(0, str(root / "sw/builder"))
spec = importlib.util.spec_from_file_location("tb", root / "sw/builder/test_builder.py")
tb = importlib.util.module_from_spec(spec); spec.loader.exec_module(tb)
rec, _p, _s = tb.dp_srcs.ask_authority("milan_datapath")
srcs = rec["src"]
at = next(i for i, s in enumerate(srcs) if s.endswith("/milan_datapath.sv"))
print(f"sources {len(srcs)}, datapath at index {at}, derived {len(rec['derived'])}")
macro = None
for src in srcs[:at]:
    m = re.search(r"^\s*`define\s+(\w+)", pathlib.Path(src).read_text(errors="replace"), re.M)
    if m:
        macro, origin = m.group(1), src
        break
print("macro", macro, "from", macro and origin.replace(str(root) + "/", ""))
if not macro:
    sys.exit(0)
rtl = (root / "hdl/milan/milan_datapath.sv").read_text()
line = "        .ETH_CYC_PER_OCTET_P(GPTP_ETH_CYC_PER_OCTET_P),"
assert line in rtl
planted = rtl.replace(line, f"`ifndef {macro}\n{line.strip()}\n`endif", 1)
print("gate answers:", tb._datapath_shape_findings(planted) or "ACCEPTED")
with tempfile.TemporaryDirectory() as tmp:
    copy = pathlib.Path(tmp) / "milan_datapath.sv"
    copy.write_text(planted)
    cmd = ["sv2v", "--pass-through", *(f"-D{d}" for d in rec["define"]),
           "-I", str(root / "hdl/milan"), *(a for d in rec["incdir"] for a in ("-I", d)),
           *srcs[:at], str(copy)]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    print("whole-list front end rc", out.returncode, out.stderr[:200])
    print("binding lines in the whole-list read:",
          re.findall(r"^\s*\.ETH_CYC_PER_OCTET_P\(.*$", out.stdout, re.M))
