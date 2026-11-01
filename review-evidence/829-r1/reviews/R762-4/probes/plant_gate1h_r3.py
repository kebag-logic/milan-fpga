#!/usr/bin/env python3
"""Plant defects in milan_datapath.sv and ask gate 1h's own findings function.

Usage: plant_gate1h_r3.py <clone root> <jobs>. The front end is whatever sv2v is
first on PATH. Each row states what the gate must do with the plant:
  refuse  a defect, or a text the build would read differently; must be refused
  accept  the same code respelled; must be accepted
  limit   outside the gate's stated limit, recorded as it answers, and not judged
  probe   a shape outside the stated limit whose answer is reported for judgment
Exit 0 when every refuse row was refused and every accept row accepted.
"""
import concurrent.futures
import importlib.util
import pathlib
import shutil
import subprocess
import sys

root = pathlib.Path(sys.argv[1]).resolve()
jobs = int(sys.argv[2])
sys.argv = [sys.argv[0]]
sys.path.insert(0, str(root / "sw/builder"))
spec = importlib.util.spec_from_file_location("tb", root / "sw/builder/test_builder.py")
tb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tb)
rtl = (root / "hdl/milan/milan_datapath.sv").read_text()

TICK = "        .ETH_TICK_NS_P (GPTP_ETH_TICK_NS_P),"
OCT = "        .ETH_CYC_PER_OCTET_P(GPTP_ETH_CYC_PER_OCTET_P),"
TICK_D = "parameter int unsigned GPTP_ETH_TICK_NS_P = 8,"
OCT_D = "parameter int unsigned GPTP_ETH_CYC_PER_OCTET_P = 1,"
HEAD = "    KL_gptp_shadow #(\n"
assert all(s in rtl for s in (TICK, OCT, TICK_D, OCT_D, HEAD))
BIND = {"tick": (TICK, "ETH_TICK_NS_P", "GPTP_ETH_TICK_NS_P", "8"),
        "oct": (OCT, "ETH_CYC_PER_OCTET_P", "GPTP_ETH_CYC_PER_OCTET_P", "1")}
DECL = {"tick": (TICK_D, "GPTP_ETH_TICK_NS_P", "40"),
        "oct": (OCT_D, "GPTP_ETH_CYC_PER_OCTET_P", "2")}


def sub(old, new):
    assert old in rtl, old
    return rtl.replace(old, new, 1)


# the plane statement, from its head to its closing `);`
start = rtl.index(HEAD)
end = rtl.index("\n    );", start) + len("\n    );") + 1
PLANE = rtl[start:end]

rows = [("shipped text", "accept", rtl)]
for key, (line, port, param, dflt) in BIND.items():
    txt = line.strip()
    rows += [
        (f"{port} removed", "refuse", sub(line + "\n", "")),
        (f"{port} line comment", "refuse", sub(line, f"// {txt}")),
        (f"{port} block comment", "refuse", sub(line, f"/* {txt} */")),
        (f"{port} multi-line block comment", "refuse", sub(line, f"/*\n{txt}\n*/")),
        (f"{port} tied, binding in a trailing comment", "refuse",
         sub(line, f".{port} ({dflt}), // {txt}")),
        (f"{port} dead ifdef", "refuse", sub(line, f"`ifdef NO_SUCH\n{txt}\n`endif")),
        (f"{port} ifndef SYNTHESIS", "refuse", sub(line, f"`ifndef SYNTHESIS\n{txt}\n`endif")),
        (f"{port} tied under SYNTHESIS, bound in the else", "refuse",
         sub(line, f"`ifdef SYNTHESIS\n.{port} ({dflt}),\n`else\n{txt}\n`endif")),
        (f"{port} bound under `if 0 of a macro guard", "refuse",
         sub(line, f"`define KEEP_{key}\n`undef KEEP_{key}\n`ifdef KEEP_{key}\n{txt}\n`endif")),
        (f"{port} tied through a macro", "refuse",
         sub(line, f"`define M_{key} {dflt}\n.{port} (`M_{key}),")),
        (f"{port} swallowed by a macro that discards its argument", "refuse",
         sub(line, f"`define DROP_{key}(x)\n`DROP_{key}({txt.rstrip(',')})")),
        (f"{port} on the wrong parameter", "refuse", sub(line, f".{port} (GPTP_PHC_TICK_NS_P),")),
        (f"{port} no-op expression", "refuse", sub(line, f".{port} ({param} * 1),")),
        (f"{port} parenthesised expression of a literal", "refuse", sub(line, f".{port} (({dflt})),")),
        (f"{port} bound twice", "refuse", sub(line, f"{line}\n.{port} ({dflt}),")),
        # a macro hdl/common/ethernet_packet_pkg.sv defines, earlier in the build's list
        (f"{port} live only where an earlier source's macro is absent", "refuse",
         sub(line, f"`ifndef ETHERNET_PACKET_PKG_SV\n{txt}\n`endif")),
        (f"{port} comment beside it", "accept", sub(line, f"{line} // why")),
        (f"{port} odd whitespace", "accept", sub(line, f".{port}  (\n  {param}\n ),")),
        (f"{port} live ifdef", "accept", sub(line, f"`ifdef SYNTHESIS\n{txt}\n`endif")),
        (f"{port} through a macro naming the parameter", "accept",
         sub(line, f"`define N_{key} {param}\n.{port} (`N_{key}),")),
    ]
for key, (decl, param, mii) in DECL.items():
    live = f"parameter int unsigned {param} = {mii},"
    rows += [
        (f"{param} default moved", "refuse", sub(decl, live)),
        (f"{param} localparam", "refuse", sub(decl, decl.replace("parameter", "localparam"))),
        (f"{param} commented, live below", "refuse", sub(decl, f"// {decl}\n  {live}")),
        (f"{param} block comment, live below", "refuse", sub(decl, f"/* {decl} */\n  {live}")),
        (f"{param} dead ifdef, live else", "refuse",
         sub(decl, f"`ifdef NO_SUCH\n{decl}\n`else\n{live}\n`endif")),
        (f"{param} moved under an earlier source's macro, live else", "refuse",
         sub(decl, f"`ifndef ETHERNET_PACKET_PKG_SV\n{decl}\n`else\n{live}\n`endif")),
        (f"{param} moved under ifndef SYNTHESIS, live else", "refuse",
         sub(decl, f"`ifndef SYNTHESIS\n{decl}\n`else\n{live}\n`endif")),
        (f"{param} shadowed in the same scope", "refuse",
         sub(HEAD, f"    localparam int unsigned {param} = {mii};\n{HEAD}")),
        (f"{param} shadowed in a comma list", "refuse",
         sub(HEAD, f"    localparam int unsigned R3_X = 1, {param} = {mii};\n{HEAD}")),
        (f"{param} shadowed in a block around the plane", "refuse",
         sub(PLANE, f"    if (1) begin : g_r3\n    localparam int unsigned {param} = {mii};\n{PLANE}    end\n")),
        (f"{param} shadowed by a net in a block around the plane", "refuse",
         sub(PLANE, f"    if (1) begin : g_r3\n    wire [31:0] {param} = 32'd{mii};\n{PLANE}    end\n")),
        (f"{param} default a macro of the moved value", "refuse",
         sub(decl, f"parameter int unsigned {param} = `R3_D_{key},").replace(
             "module milan_datapath", f"`define R3_D_{key} {mii}\nmodule milan_datapath", 1)),
        (f"{param} comment inside the default", "accept",
         sub(decl, f"parameter int unsigned {param} = /* GMII */ {decl.split('= ')[1]}")),
        (f"{param} default respelled across lines", "accept",
         sub(decl, f"parameter int unsigned {param} =\n    {decl.split('= ')[1]}")),
        # stated limit is a defparam or a dead generate arm; this is neither:
        # a dims expression holding `=` hides a shadow from the declaration read
        (f"{param} shadowed by a genvar loop around the plane", "probe",
         sub(PLANE, f"    genvar {param};\n    for ({param} = {mii}; {param} < {mii} + 1; {param} = {param} + 1) begin : g_r3\n{PLANE}    end\n")),
        (f"{param} shadowed in a block, with == in its packed dims", "probe",
         sub(PLANE, f"    if (1) begin : g_r3\n    localparam logic [(1 == 1 ? 31 : 31):0] {param} = {mii};\n{PLANE}    end\n")),
    ]
rows += [
    ("plane renamed", "refuse", sub(") u_gptp_shadow (", ") u_gptp_other (")),
    ("second plane beside the first", "refuse",
     sub(HEAD, "    KL_gptp_shadow #(.TDATA_WIDTH_P(8)) u_two ();\n" + HEAD)),
    ("second instance in the plane's own statement", "refuse",
     sub(PLANE, PLANE[:-len(");\n")] + "), u_gptp_two ();\n")),
    ("second plane in a live generate arm", "refuse",
     sub(HEAD, "    if (1) begin : g_r3 KL_gptp_shadow #(.TDATA_WIDTH_P(8)) u_two (); end\n" + HEAD)),
    ("plane in a comment, decoy-free", "refuse", sub(PLANE, f"/*\n{PLANE}*/\n")),
    ("plane in a dead ifdef", "refuse", sub(PLANE, f"`ifdef NO_SUCH\n{PLANE}`endif\n")),
    ("bindings crossed", "refuse", sub(TICK, ".ETH_TICK_NS_P (GPTP_ETH_CYC_PER_OCTET_P),").replace(
        OCT, ".ETH_CYC_PER_OCTET_P(GPTP_ETH_TICK_NS_P),", 1)),
    ("include of a file that does not exist", "refuse", sub(HEAD, f'`include "r3_no_such.svh"\n{HEAD}')),
    ("unterminated block comment at the plane", "refuse", sub(HEAD, f"/* never closed\n{HEAD}")),
    ("syntax error at the plane", "refuse", sub(HEAD, f"    wire ;\n{HEAD}")),
    ("parameters reordered, same bindings", "accept",
     sub(TICK + "\n" + OCT, OCT + "\n" + TICK)),
    ("the octet binding last with no comma", "accept",
     sub(OCT + "\n", "").replace(".EGRESS_LAT_NS_P (GPTP_EGRESS_LAT_NS_P)\n",
                                 ".EGRESS_LAT_NS_P (GPTP_EGRESS_LAT_NS_P),\n" + OCT.rstrip(",") + "\n", 1)),
    ("defparam moving the tick after the plane", "limit",
     sub(PLANE, f"{PLANE}    defparam u_gptp_shadow.ETH_TICK_NS_P = 8;\n")),
    ("defparam moving the octet after the plane", "limit",
     sub(PLANE, f"{PLANE}    defparam u_gptp_shadow.ETH_CYC_PER_OCTET_P = 1;\n")),
    ("plane only in an if (0) arm", "limit",
     sub(PLANE, f"    if (0) begin : g_r3\n{PLANE}    end\n")),
    ("plane only where the octet parameter is 1", "limit",
     sub(PLANE, f"    if (GPTP_ETH_CYC_PER_OCTET_P == 1) begin : g_r3\n{PLANE}    end\n")),
    ("plane in a never-instantiated module", "limit",
     rtl.replace(PLANE, "", 1) + "\nmodule r3_dead;\n" +
     "parameter int unsigned X = 1;\n" + PLANE + "endmodule\n"),
]
for name, want, text in rows:
    if want != "limit" and name != "shipped text":
        assert text != rtl, name


def ask(row):
    name, want, text = row
    bad = tb._datapath_shape_findings(text)
    return name, want, bad


print("front end:", shutil.which("sv2v"),
      subprocess.run(["sv2v", "--version"], capture_output=True, text=True).stdout.strip())
with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
    results = list(pool.map(ask, rows))
wrong = 0
for name, want, bad in results:
    answer = "refused" if bad else "accepted"
    ok = {"refuse": bool(bad), "accept": not bad}.get(want, True)
    wrong += not ok
    note = bad[0][:110].replace("\n", " ") if bad else ""
    print(f"{'ok ' if ok else 'BAD'} {want:6} {answer:8} {name}: {note}")
tally = {k: sum(1 for r in results if r[1] == k) for k in ("refuse", "accept", "limit", "probe")}
print(f"plants: {tally}; not as wanted: {wrong}")
sys.exit(1 if wrong else 0)
