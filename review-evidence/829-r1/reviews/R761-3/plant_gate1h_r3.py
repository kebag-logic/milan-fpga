#!/usr/bin/env python3
"""Reviewer plants for gate 1h, written from the delta and not from the committed controls.

Usage: plant_gate1h_r3.py <clone root>   (the front end is whatever is first on PATH)

Each row is (expected, name, planted text). `refuse` means the gate must name a
finding; `accept` means an equal spelling the gate must pass; `limit` means the
row is a recorded measurement of a stated or found limit, and its result is
printed without judging it. Exit status 1 when a refuse row is accepted or an
accept row is refused.
"""
import contextlib
import io
import re
import shutil
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/builder"))
sys.argv = [sys.argv[0]]
with contextlib.redirect_stdout(io.StringIO()):
    import test_builder as tb  # noqa: E402

rtl = (root / "hdl/milan/milan_datapath.sv").read_text()
TICK = ".ETH_TICK_NS_P (GPTP_ETH_TICK_NS_P),"
OCTET = ".ETH_CYC_PER_OCTET_P(GPTP_ETH_CYC_PER_OCTET_P),"
DECL_T = "parameter int unsigned GPTP_ETH_TICK_NS_P = 8,"
DECL_O = "parameter int unsigned GPTP_ETH_CYC_PER_OCTET_P = 1,"
PLANE = "    KL_gptp_shadow #(\n"
END = "    ) u_gptp_shadow ("
for needle in (TICK, OCTET, DECL_T, DECL_O, PLANE, END):
    assert rtl.count(needle) == 1, needle


def sub(old, new):
    planted = rtl.replace(old, new)
    assert planted != rtl, old
    return planted


rows = [
    ("accept", "shipped text", rtl),
    # the three layers the round claims to close
    ("refuse", "tick binding in a line comment", sub(TICK, "// " + TICK)),
    ("refuse", "octet binding in a line comment", sub(OCTET, "// " + OCTET)),
    ("refuse", "tick binding in a block comment", sub(TICK, "/* " + TICK + " */")),
    ("refuse", "octet binding in a block comment", sub(OCTET, "/* " + OCTET + " */")),
    ("refuse", "tick binding in a dead ifdef", sub(TICK, "`ifdef NOPE\n" + TICK + "\n`endif")),
    ("refuse", "octet binding in a dead ifndef", sub(OCTET, "`ifndef SYNTHESIS\n" + OCTET + "\n`endif")),
    ("refuse", "tick binding under `if 0 of a macro",
     sub(TICK, "`define OFF\n`ifndef OFF\n" + TICK + "\n`endif")),
    ("refuse", "tick binding swallowed by a discard macro",
     sub(TICK, "`define DISCARD(x)\n`DISCARD(.ETH_TICK_NS_P (GPTP_ETH_TICK_NS_P))")),
    ("refuse", "tick default in a comment with a live 40 below",
     sub(DECL_T, "// " + DECL_T + "\n  parameter int unsigned GPTP_ETH_TICK_NS_P = 40,")),
    ("refuse", "octet default in a dead arm with a live 2 below",
     sub(DECL_O, "`ifdef NOPE\n" + DECL_O + "\n`else\nparameter int unsigned GPTP_ETH_CYC_PER_OCTET_P = 2,\n`endif")),
    ("refuse", "tick binding a macro expanding to the GMII value",
     sub(TICK, "`define V 8\n.ETH_TICK_NS_P (`V),")),
    ("refuse", "tick default a macro expanding to 40",
     sub(DECL_T, "`define V 40\nparameter int unsigned GPTP_ETH_TICK_NS_P = `V,")),
    # the bindings themselves
    ("refuse", "tick binding removed", sub(TICK + "\n", "\n")),
    ("refuse", "octet binding removed", sub(OCTET + "\n", "\n")),
    ("refuse", "tick tied to 8", sub(TICK, ".ETH_TICK_NS_P (8),")),
    ("refuse", "octet tied to 1", sub(OCTET, ".ETH_CYC_PER_OCTET_P(1),")),
    ("refuse", "tick on the PHC tick", sub(TICK, ".ETH_TICK_NS_P (GPTP_PHC_TICK_NS_P),")),
    ("refuse", "tick parenthesised expression", sub(TICK, ".ETH_TICK_NS_P ((GPTP_ETH_TICK_NS_P + 0)),")),
    ("refuse", "tick written with an implicit name", sub(TICK, ".ETH_TICK_NS_P,")),
    ("refuse", "tick left open", sub(TICK, ".ETH_TICK_NS_P (),")),
    ("refuse", "bindings crossed", sub(TICK, ".ETH_TICK_NS_P (GPTP_ETH_CYC_PER_OCTET_P),").replace(
        OCTET, ".ETH_CYC_PER_OCTET_P(GPTP_ETH_TICK_NS_P),")),
    ("refuse", "tick bound twice", sub(TICK, TICK + "\n.ETH_TICK_NS_P (8),")),
    # the defaults
    ("refuse", "tick default 40", sub(DECL_T, "parameter int unsigned GPTP_ETH_TICK_NS_P = 40,")),
    ("refuse", "octet default 2", sub(DECL_O, "parameter int unsigned GPTP_ETH_CYC_PER_OCTET_P = 2,")),
    ("refuse", "tick default removed", sub(DECL_T + "\n", "\n")),
    ("refuse", "tick a localparam", sub(DECL_T, DECL_T.replace("parameter", "localparam"))),
    ("refuse", "tick redeclared beside the plane",
     sub(PLANE, "    localparam int unsigned GPTP_ETH_TICK_NS_P = 40;\n" + PLANE)),
    ("refuse", "octet redeclared in a multi-declarator",
     sub(PLANE, "    localparam int unsigned OTHER_Q = 3, GPTP_ETH_CYC_PER_OCTET_P = 2;\n" + PLANE)),
    ("refuse", "tick redeclared with a packed range",
     sub(PLANE, "    localparam [31:0] GPTP_ETH_TICK_NS_P = 40;\n" + PLANE)),
    # the plane
    ("refuse", "plane instance renamed", sub(END, "    ) u_gptp_other (")),
    ("refuse", "plane module renamed", sub(PLANE, "    KL_gptp_shadow_x #(\n")),
    ("refuse", "second plane, no parameters",
     sub(PLANE, "    KL_gptp_shadow u_gptp_b (.clk_i(axis_clk));\n" + PLANE)),
    ("refuse", "second plane in a dead arm of a live generate",
     sub(PLANE, "    if (1'b0) begin : g_x KL_gptp_shadow #(.TDATA_WIDTH_P(8)) u_b (.clk_i(axis_clk)); end\n" + PLANE)),
    ("refuse", "plane without parameters", re.sub(
        r"KL_gptp_shadow #\(.*?\) u_gptp_shadow \(", "KL_gptp_shadow u_gptp_shadow (",
        rtl, flags=re.DOTALL)),
    ("refuse", "positional parameters", re.sub(
        r"KL_gptp_shadow #\(.*?\) u_gptp_shadow \(",
        "KL_gptp_shadow #(TDATA_WIDTH, MILAN_CLK_FREQ_HZ, GPTP_UCODE_HEX_P, GPTP_PHC_TICK_NS_P, "
        "GPTP_ETH_TICK_NS_P, GPTP_ETH_CYC_PER_OCTET_P, GPTP_INGRESS_LAT_NS_P, GPTP_EGRESS_LAT_NS_P) "
        "u_gptp_shadow (", rtl, flags=re.DOTALL)),
    ("refuse", "syntax error near the plane", sub(TICK, ".ETH_TICK_NS_P (GPTP_ETH_TICK_NS_P,")),
    # equal spellings
    ("accept", "tick with a comment beside it", sub(TICK, TICK + " // why")),
    ("accept", "tick spaced out", sub(TICK, ".ETH_TICK_NS_P\n  (\n GPTP_ETH_TICK_NS_P\n ),")),
    ("accept", "binding through a macro of the name",
     sub(TICK, "`define V GPTP_ETH_TICK_NS_P\n.ETH_TICK_NS_P (`V),")),
    ("accept", "plane on one line", re.sub(r"KL_gptp_shadow #\(\s*", "KL_gptp_shadow #(", rtl)),
    ("accept", "tick under a live ifdef", sub(TICK, "`ifdef SYNTHESIS\n" + TICK + "\n`endif")),
    # measurements of limits: printed, not judged
    ("limit", "defparam after a correct binding",
     sub(PLANE, "    defparam u_gptp_shadow.ETH_TICK_NS_P = 8;\n" + PLANE)),
    ("limit", "the only plane in an arm that never elaborates",
     sub(PLANE, "    if (1'b0) begin : g_dead\n" + PLANE)),
    ("limit", "an ifdef SYNTHESIS binding with a tied else",
     sub(TICK, "`ifdef SYNTHESIS\n" + TICK + "\n`else\n.ETH_TICK_NS_P (8),\n`endif")),
    ("limit", "the plane in a for-generate whose genvar shadows the name",
     sub(PLANE, "    for (genvar GPTP_ETH_TICK_NS_P = 40; GPTP_ETH_TICK_NS_P < 41; "
                "GPTP_ETH_TICK_NS_P = GPTP_ETH_TICK_NS_P + 1) begin : g_shadow\n" + PLANE)),
    ("limit", "a second plane behind an attribute",
     sub(PLANE, "    (* keep *) KL_gptp_shadow #(.TDATA_WIDTH_P(8)) u_b (.clk_i(axis_clk));\n" + PLANE)),
    ("limit", "a second plane under an escaped name",
     sub(PLANE, "    \\KL_gptp_shadow  #(.TDATA_WIDTH_P(8)) u_b (.clk_i(axis_clk));\n" + PLANE)),
]


def with_end_of_dead_arm(text):
    """The arm-opening rows need the matching `end` after the instance's `);`."""
    if "g_shadow" not in text and "g_dead" not in text:
        return text
    at = text.index("u_gptp_shadow (")
    close = text.index("\n    );", at)
    return text[:close] + "\n    );\n    end" + text[close + len("\n    );"):]


print("front end:", shutil.which("sv2v"),
      subprocess.run(["sv2v", "--version"], capture_output=True, text=True).stdout.strip())
wrong = 0
counts = {"refuse": 0, "accept": 0, "limit": 0}
for expected, name, text in rows:
    counts[expected] += 1
    text = with_end_of_dead_arm(text)
    bad = tb._datapath_shape_findings(text)
    mark = "refused" if bad else "accepted"
    ok = (expected == "limit") or (bool(bad) == (expected == "refuse"))
    wrong += not ok
    print(f"{'ok ' if ok else 'BAD'} {expected:6} {mark:8} {name}: {str(bad)[:170]}")
print("rows:", counts, "not as wanted:", wrong)
sys.exit(1 if wrong else 0)
