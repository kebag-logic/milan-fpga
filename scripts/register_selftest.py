#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted controls for the register reference freshness gate (#797).

Each control copies the generator's inputs and outputs into a temporary tree,
plants one defect and runs the same `--check` entry the docs workflow calls on
that tree. A fresh copy must pass; every planted defect must fail with the
expected exit status and message. The controls are the gate's own evidence: a
renamed field, a changed reset, a new register window, a behaviour change, a
write or read form the parser cannot read, a hand edit, a missing or extra
diagram, an edited SoC extract, and descriptions the RTL cannot back.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import itertools
import json
import shutil
import tempfile
from collections.abc import Callable
from pathlib import Path

from register_diagrams import LINK_GUARD, SERVO
from register_page import DESCRIPTIONS, DIAGRAM_DIR, PAGE, RECORD, SOC, read_rows
from register_rtl import CSR_INCLUDE_DIR, DATAPATH, ETH_PKG, ROOT, RTL, SHAPE_INCLUDE_DIR
from register_sv import flatten, parse_expression, unparse

LEDGER = "docs/reference/milan_feature_status.json"
FINGERPRINT = f"{DIAGRAM_DIR}/rtl_fingerprint.txt"
STALE_PAGE = f"STALE {PAGE}"
Entry = Callable[..., int]
#: Each plant is (file, text to find, replacement).
Plant = tuple[str, str, str]
REFUSED_ROM = "defaults ROM serves"
NOT_READ = "this generator does not read"
FORM = "a write form this generator cannot read"
NOT_REGISTER = "which is not an A_* register"
NEEDS_NAME = "needs a name and a purpose"
SCRATCH_ARM = "A_SCRATCH:   scratch  <= s_axi_wdata;"
GPTP_LAT = "A_GPTP_LAT   = 'h7F0;"
LATENCY_HEADER = "hdl/common/csr/gen/lwsrp_csr_defaults.svh"
#: name, plants, expected exit status, text the output must carry.
TEXT_CONTROLS: list[tuple[str, list[Plant], int, str]] = [
    ("reset change in the ROM alone",
     [(RTL, "A_MAC_IFG[10:0]:    csr_default = 32'h0C;", "A_MAC_IFG[10:0]:    csr_default = 32'h0D;")], 2, REFUSED_ROM),
    ("reset change in both the ROM and the flop",
     [(RTL, "A_MAC_IFG[10:0]:    csr_default = 32'h0C;", "A_MAC_IFG[10:0]:    csr_default = 32'h0D;"),
      (RTL, "mac_ifg <= 32'h0C;", "mac_ifg <= 32'h0D;")], 1, STALE_PAGE),
    ("reset change on the flop of a shadow-served word: mac_ifg",
     [(RTL, "mac_ifg <= 32'h0C;", "mac_ifg <= 32'h0D;")], 2, REFUSED_ROM),
    ("reset change on the flop of a shadow-served word: mac_ctrl",
     [(RTL, "mac_ctrl <= 32'h13;", "mac_ctrl <= 32'h12;")], 2, REFUSED_ROM),
    ("reset change on the flop of a shadow-served word: scratch",
     [(RTL, "scratch <= 32'h0;", "scratch <= 32'h5;")], 2, REFUSED_ROM),
    ("reset change on the flop of a shadow-served word: tcam_ctrl",
     [(RTL, "tcam_ctrl <= 32'h1;", "tcam_ctrl <= 32'h0;")], 2, REFUSED_ROM),
    ("reset change on a flop through its generated header",
     [(LATENCY_HEADER, "LWSRP_LATENCY_RST_C   = 32'h0000_0000", "LWSRP_LATENCY_RST_C   = 32'h0000_0009")], 2,
     REFUSED_ROM),
    ("reset change on a live-read flop",
     [(RTL, "ltap_en_r  <= 1'b1;", "ltap_en_r  <= 1'b0;")], 1, STALE_PAGE),
    ("reset change the ETH_GUARD diagram draws",
     [(RTL, "eth_guard <= 1'b1;", "eth_guard <= 1'b0;")], 2, "the ETH_GUARD diagram"),
    ("reset change behind a window read: the snapshot store",
     [(RTL, "for (int w = 0; w < 12; w++) snap_shadow_r[w] <= 32'h0;",
       "for (int w = 0; w < 12; w++) snap_shadow_r[w] <= 32'h5;")], 1, STALE_PAGE),
    ("poison constant behind CHMAP_LOOP",
     [(RTL, "CHMAP_LOOP_POISON_C = 32'hDEAD_DEAD;", "CHMAP_LOOP_POISON_C = 32'hDEAD_BEEF;")], 1, STALE_PAGE),
    ("CHMAP_LOOP subfield order swapped",
     [(RTL, "cmrd_data_r[14], cmrd_data_r[13],", "cmrd_data_r[13], cmrd_data_r[14],")], 2,
     "renames field CHMAP_LOOP"),
    ("PPS_WIDTH read expression changed",
     [(RTL, "live_mux = PPS_P ? 32'(PPS_WIDTH_CYC_P) : 32'h0;", "live_mux = PPS_P ? 32'(PPS_WIDTH_CYC_P) : 32'h1;")],
     1, STALE_PAGE),
    ("value of the 0x86C window hole changed",
     [(RTL, "else if (rd_addr_q == ADDR_WIDTH'('h86C))\n            strm_mux = 32'hDEAD_DEAD;",
       "else if (rd_addr_q == ADDR_WIDTH'('h86C))\n            strm_mux = 32'hDEAD_BEEF;")], 1, STALE_PAGE),
    ("STRMW_SRP's live alias removed",
     [(RTL, "? i_lwsrp_status", "? 32'd0")], 2, "describes field STRMW_SRP"),
    ("new range window with a live read term",
     [(RTL, GPTP_LAT, GPTP_LAT + "\n  localparam [ADDR_WIDTH-1:0] A_PLANTW_BASE = 'h7F4;\n"
                                 "  localparam [ADDR_WIDTH-1:0] A_PLANTW_END = 'h7F8;"),
      (RTL, "else if (strm_hit)\n", "else if (rd_addr_q >= A_PLANTW_BASE && rd_addr_q < A_PLANTW_END)\n"
                                    "          live_mux = i_txarb_diag;\n        else if (strm_hit)\n")],
     2, "does not document"),
    ("new register whose label ends in _END, with a live read arm",
     [(RTL, GPTP_LAT, GPTP_LAT + "\n  localparam [ADDR_WIDTH-1:0] A_PLANT_END = 'h7F8;"),
      (RTL, "A_TXARB_DIAG: live_mux = i_txarb_diag;",
       "A_TXARB_DIAG: live_mux = i_txarb_diag;\n      A_PLANT_END: live_mux = i_txarb_diag;")], 2, NEEDS_NAME),
    ("literal-address read arm",
     [(RTL, "A_TXARB_DIAG: live_mux = i_txarb_diag;",
       "A_TXARB_DIAG: live_mux = i_txarb_diag;\n      16'h7F8: live_mux = i_txarb_diag;")], 2, NOT_REGISTER),
    ("literal-address write arm",
     [(RTL, SCRATCH_ARM, SCRATCH_ARM + "\n          16'h7F8:     scratch  <= s_axi_wdata;")], 2, NOT_REGISTER),
    ("read arm whose label lacks the A_ prefix",
     [(RTL, GPTP_LAT, GPTP_LAT + "\n  localparam [ADDR_WIDTH-1:0] R_PLANT = 'h7F8;"),
      (RTL, "A_TXARB_DIAG: live_mux = i_txarb_diag;",
       "A_TXARB_DIAG: live_mux = i_txarb_diag;\n      R_PLANT: live_mux = i_txarb_diag;")], 2, NOT_REGISTER),
    ("literal-address test in a read decode",
     [(RTL, "else if (rd_addr_q == ADDR_WIDTH'('h86C))",
       "else if (rd_addr_q == ADDR_WIDTH'('h808))\n            strm_mux = 32'h1;\n"
       "          else if (rd_addr_q == ADDR_WIDTH'('h86C))")], 2, "literal address"),
    ("new address nothing decodes",
     [(RTL, GPTP_LAT, GPTP_LAT + "\n  localparam [ADDR_WIDTH-1:0] A_PLANTED = 'h7F4;")], 2, "nothing decodes"),
    ("new register with a read arm and no description",
     [(RTL, GPTP_LAT, GPTP_LAT + "\n  localparam [ADDR_WIDTH-1:0] A_PLANTED = 'h7F4;"),
      (RTL, "A_TXARB_DIAG: live_mux = i_txarb_diag;",
       "A_TXARB_DIAG: live_mux = i_txarb_diag;\n      A_PLANTED: live_mux = i_txarb_diag;")], 2, NEEDS_NAME),
    ("read arm removed from rd_in_window's reach",
     [(RTL, "(rd_addr_q == A_SLIP_TDM) ||", "")], 2, "rd_in_window makes it read 0"),
    ("write decoded in a new block outside the parsed ones",
     [(RTL, "always_ff @(posedge aclk) begin : shadow_sweep",
       "always_ff @(posedge aclk) begin : extra_wr\n    if (wr_fire && wr_addr == A_CLKV_CTRL) scratch <= 32'h1;\n"
       "  end\n  always_ff @(posedge aclk) begin : shadow_sweep")], 2, NOT_READ),
    ("clear on read added outside the parsed blocks",
     [(RTL, "always_ff @(posedge aclk) begin : shadow_sweep",
       "always_ff @(posedge aclk) begin : extra_rc\n    if (rd_fire && rd_addr == A_IRQ_RAW) irq_mask <= 32'h0;\n"
       "  end\n  always_ff @(posedge aclk) begin : shadow_sweep")], 2, NOT_READ),
    ("doorbell added to a write arm",
     [(RTL, SCRATCH_ARM, "A_SCRATCH: begin scratch <= s_axi_wdata; tcam_wr_p <= 1'b1; end")], 1, STALE_PAGE),
    ("write arm stores through a mask",
     [(RTL, "A_CHMAP_SEL:  chmap_sel  <= s_axi_wdata;", "A_CHMAP_SEL:  chmap_sel  <= s_axi_wdata & 32'h1FF;")], 2,
     FORM),
    ("write arm stores part of a register",
     [(RTL, "A_MCSRV_CTRL: mcsrv_ctrl <= s_axi_wdata;", "A_MCSRV_CTRL: mcsrv_ctrl[1:0] <= s_axi_wdata[1:0];")], 2,
     FORM),
    ("write arm increments the written value",
     [(RTL, "A_CHMAP_CTRL: chmap_ctrl <= s_axi_wdata;", "A_CHMAP_CTRL: chmap_ctrl <= s_axi_wdata + 32'd1;")], 2,
     FORM),
    ("read expression outside the grammar",
     [(RTL, "A_CRF_RATE:   live_mux = i_crf_rate;", "A_CRF_RATE:   live_mux = i_crf_rate ** 2;")], 2, "unexpected"),
    ("read masked by a constant",
     [(RTL, "A_CRF_DELTA:  live_mux = i_crf_delta;", "A_CRF_DELTA:  live_mux = i_crf_delta & 32'h0000_00FF;")], 1,
     STALE_PAGE),
    ("reserved stored bit consumed by logic",
     [(RTL, "assign o_irq = |(irq_status & irq_mask);", "assign o_irq = |(irq_status & irq_mask) & ~mac_ctrl[9];")],
     2, "cannot be called reserved"),
    ("CBS word moved in the shadow decode",
     [(RTL, "(a[4:0] == 5'h08)", "(a[4:0] == 5'h10)")], 2, "CBS window"),
    ("RTL field rename of a described field",
     [(RTL, "o_eth_guard", "o_eth_lock")], 2, "describes field ETH_GUARD.ETH_GUARD"),
    ("RTL field rename, with its description following",
     [(RTL, "o_ptp_offset", "o_ptp_off"), (DESCRIPTIONS, '"PTP_OFFSET"', '"PTP_OFF"')], 1, STALE_PAGE),
    ("unlock key change in the ETH_GUARD write decode",
     [(RTL, "(s_axi_wdata != 32'h554E_4C4B)", "(s_axi_wdata != 32'h554E_4C4C)")], 1, STALE_PAGE),
    ("code change no page text shows",
     [(RTL, "sweep_cnt", "sweep_count")], 1, f"STALE {FINGERPRINT}"),
    ("comment-only RTL edit stays fresh",
     [(RTL, "  //! CHMAP_LOOP 0x914 read view.", "  //! CHMAP_LOOP 0x914 read view, edited.")], 0, "fresh"),
    ("mechanism diagram's state gone from its source",
     [(SERVO, "HOLDOVER_S", "HOLD_OVER_S")], 2, "a mechanism diagram names HOLDOVER_S"),
    ("mechanism diagram's bit no longer a strobe",
     [(RTL, "wire snap_go_w  = wr_fire && (wr_addr == A_STRM_SNAP) && s_axi_wdata[0] &&",
       "wire snap_go_w  = wr_fire && (wr_addr == A_STRM_SNAP) && s_axi_wdata[1] &&")], 2, "a mechanism diagram uses"),
    ("hand edit of the page",
     [(PAGE, "[reset = 0x00000001]", "[reset = 0x00000000]")], 1, STALE_PAGE),
    ("edited WaveDrom source",
     [(f"{DIAGRAM_DIR}/guard.json", '"R/W-1h"', '"R/W-0"')], 1, f"STALE {DIAGRAM_DIR}/guard.json"),
    ("edited SoC extract",
     [(SOC, '"origin": 4026537984', '"origin": 4026540032')], 1, STALE_PAGE),
    ("design-note link to a heading that is gone",
     [(RECORD, "## Reading the register map", "## Reading the map")], 2,
     "which docs/design/CSR_REGISTER_NOTES.md lacks"),
]


def copy_inputs(dst: Path) -> None:
    """The files the generator reads and writes, copied under `dst`."""
    shape = json.loads((ROOT / SOC).read_text(encoding="utf-8"))["shape"]
    files = [RTL, DATAPATH, ETH_PKG, DESCRIPTIONS, SOC, LEDGER, PAGE, RECORD, LINK_GUARD, SERVO,
             "docs/diagrams/README.md"]
    for include_dir in (CSR_INCLUDE_DIR, SHAPE_INCLUDE_DIR.format(shape=shape)):
        files += [p.relative_to(ROOT).as_posix() for p in (ROOT / include_dir / "gen").glob("*.svh")]
    files += [p.relative_to(ROOT).as_posix() for p in (ROOT / DIAGRAM_DIR).rglob("*") if p.is_file()]
    for rel in files:
        (dst / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / rel, dst / rel)


def edit(root: Path, rel: str, old: str, new: str) -> None:
    """Replace every occurrence in a copied file; a plant that finds nothing fails."""
    path = root / rel
    before = path.read_text(encoding="utf-8")
    if old not in before:
        raise AssertionError(f"planted text is not in {rel}: {old[:60]}")
    path.write_text(before.replace(old, new), encoding="utf-8")


def edit_descriptions(root: Path, change: Callable[[dict], None]) -> None:
    """Apply one change to the copied descriptions file."""
    path = root / DESCRIPTIONS
    desc = json.loads(path.read_text(encoding="utf-8"))
    change(desc)
    path.write_text(json.dumps(desc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _drop_purpose(desc: dict) -> None:
    desc["registers"]["MAC_IFG"]["purpose"] = ""


def _unknown_register(desc: dict) -> None:
    desc["registers"]["PLANTED"] = {"name": "x", "purpose": "x"}


def _unknown_field(desc: dict) -> None:
    desc["registers"]["ETH_GUARD"]["fields"]["PLANTED_FIELD"] = "no such field"


def _long_note(desc: dict) -> None:
    desc["registers"]["ETH_GUARD"]["notes"] = ["word " * 25 + "end."]


def _long_cell(desc: dict) -> None:
    desc["registers"]["ETH_GUARD"]["fields"]["ETH_GUARD"] = "word " * 205 + "end."


def _one_column(desc: dict) -> None:
    desc["registers"]["ETH_GUARD"]["notes"] = [{"table": [["Note"], ["word " * 25 + "end."]]}]


def _unworded_condition(desc: dict) -> None:
    del desc["condition_words"]["win_in_range_w"]


def _bad_literal(desc: dict) -> None:
    desc["literal_words"]["0x808"] = "STRMW_PLANT"


def _unknown_rename(desc: dict) -> None:
    desc["registers"]["CAP"]["rename"]["BIT99"] = "NOTHING"


def controls() -> list[tuple[str, Callable[[Path], None], int, str]]:
    """(name, plant, expected exit status, text the output must carry)."""
    out: list[tuple[str, Callable[[Path], None], int, str]] = [("fresh copy", lambda r: None, 0, "fresh")]
    for name, plants, status, text in TEXT_CONTROLS:
        def plant(root: Path, edits: list[Plant] = plants) -> None:
            """Apply this control's text edits."""
            for rel, old, new in edits:
                edit(root, rel, old, new)
        out.append((name, plant, status, text))
    for name, change, status, text in (
            ("register without a purpose", _drop_purpose, 2, NEEDS_NAME),
            ("description of a register the RTL lacks", _unknown_register, 2, "describes register PLANTED"),
            ("description of a field the RTL lacks", _unknown_field, 2, "describes field ETH_GUARD.PLANTED_FIELD"),
            ("note breaking the prose rules", _long_note, 2, "breaks the documentation rules"),
            ("prose wrapped in a one-column table", _one_column, 2, "one-column table"),
            ("prose wrapped in a field's table cell", _long_cell, 2, "a table cell has"),
            ("condition without wording", _unworded_condition, 2, "has no wording"),
            ("literal word the RTL does not test", _bad_literal, 2, "does not test"),
            ("rename of a field the RTL lacks", _unknown_rename, 2, "renames field CAP.BIT99")):
        def plant(root: Path, chosen: Callable[[dict], None] = change) -> None:
            """Apply this control's change to the descriptions file."""
            edit_descriptions(root, chosen)
        out.append((name, plant, status, text))
    out += [("deleted register diagram", lambda r: next((r / DIAGRAM_DIR).rglob("*.svg")).unlink(), 1,
             "STALE docs/diagrams/regmap/"),
            ("extra stale diagram",
             lambda r: (r / DIAGRAM_DIR / "planted.svg").write_text("<svg/>\n", encoding="utf-8"),
             1, "planted.svg (not generated)")]
    return out


def memory_map_control() -> bool:
    """The memory-map label check refuses a label that overprints its address,
    or carries markup, and passes the labels the tree renders."""
    spec = importlib.util.spec_from_file_location("memory_map_gen", ROOT / "docs/diagrams/memory_map.gen.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    palette = ("#FFFFFF", "#000000")
    long_label = [("x" * 80, 0, 1, palette, 0)]
    marked = [("`code`", 0, 1, palette, 0)]
    return (bool(module.check_labels(long_label, [])) and bool(module.check_labels([], marked))
            and not module.check_labels([("short", 0, 1, palette, 0)], []))


#: A read decode and the rows it must print: value -> each row's terms. The first
#: is the shape of STRMW_CTRL, the second one signal compared with two values.
READ_SHAPES: list[tuple[str, dict[str, list[set[str]]]]] = [
    ("(a && !s && (!d || i != 4'd0)) ? (d ? t : l) : (a ? ((d && i == 4'd0) ? k : 32'd0) : 32'd0)",
     {"t": [{"a", "!s", "d", "!i == 4'd0"}], "l": [{"a", "!s", "!d"}], "k": [{"a", "d", "i == 4'd0"}],
      "32'd0": [{"!a"}, {"s", "!d"}, {"s", "!i == 4'd0"}]}),
    ("k == 2'd1 ? x : (k == 2'd2 ? y : 32'd0)",
     {"x": [{"k == 2'd1"}], "y": [{"k == 2'd2"}], "32'd0": [{"!k == 2'd1", "!k == 2'd2"}]}),
]


def read_table_control(entry: Entry) -> bool:
    """Read-table rows carry no grouping, so each must be one conjunction true
    as printed (#797): the shapes above give exactly their rows, and every When
    cell a regenerated page prints has no `or`, repeated term or contradiction."""
    for expression, want in READ_SHAPES:
        rows = read_rows(flatten(parse_expression(expression)), unparse)
        got = {value: [{("" if polarity else "!") + unparse(node) for node, polarity in term} for term in terms]
               for value, terms in rows.items()}
        if {v: sorted(map(sorted, t)) for v, t in got.items()} != {v: sorted(map(sorted, t)) for v, t in want.items()}:
            return False
    with tempfile.TemporaryDirectory(prefix="regref-selftest-") as tmp:
        root = Path(tmp)
        copy_inputs(root)
        with contextlib.redirect_stdout(io.StringIO()):
            if entry(["--write"], root=root) != 0:
                return False
        lines = (root / PAGE).read_text(encoding="utf-8").splitlines()
    words = json.loads((ROOT / DESCRIPTIONS).read_text(encoding="utf-8"))["condition_words"]
    opposites = [pair for pair in words.values() if isinstance(pair, list)]
    cells = []
    for at, line in enumerate(lines):
        if line == "| When | A read returns |":
            rows = itertools.takewhile(lambda text: text.startswith("|"), lines[at + 2:])
            cells += [row.split(" | ")[0].removeprefix("| ") for row in rows]
    for when in cells:
        terms = when.split(" and ")
        if " or " in when or len(set(terms)) < len(terms):
            return False
        if any(term.replace(" is not ", " is ") in terms for term in terms if " is not " in term):
            return False
        if any(yes in terms and no in terms for yes, no in opposites):
            return False
    return bool(cells)


def run(entry: Entry, root: Path) -> tuple[int, str]:
    """The workflow's `--check` on `root`: exit status and output."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = entry(["--check"], root=root)
    return rc, buf.getvalue()


def selftest(entry: Entry) -> int:
    """Run every control; 0 when each verdict is the expected one."""
    failures = 0
    names = controls()
    for name, plant, want_rc, want_text in names:
        with tempfile.TemporaryDirectory(prefix="regref-selftest-") as tmp:
            root = Path(tmp)
            copy_inputs(root)
            try:
                plant(root)
            except (AssertionError, StopIteration) as exc:
                rc, out = -1, f"the plant itself failed: {exc}"
            else:
                rc, out = run(entry, root)
        ok = rc == want_rc and want_text in out
        failures += not ok
        print(f"  {'ok  ' if ok else 'FAIL'} {name}: rc {rc} (want {want_rc})"
              + ("" if ok else f"\n       output: {' '.join(out.split())[:300]}"))
    labels_ok = memory_map_control()
    failures += not labels_ok
    print(f"  {'ok  ' if labels_ok else 'FAIL'} memory-map label check")
    rows_ok = read_table_control(entry)
    failures += not rows_ok
    print(f"  {'ok  ' if rows_ok else 'FAIL'} read-table rows are single conjunctions")
    print(f"register reference selftest: {'OK' if not failures else 'FAIL'} "
          f"({len(names) + 2 - failures}/{len(names) + 2} controls)")
    return 1 if failures else 0
