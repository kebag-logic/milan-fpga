#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""nvm_format_32x32_tables.py - the page blocks of SAVED_STATE_FORMAT_32X32.md.

`scripts/nvm_format_32x32.py` computes the figures; this module formats them,
renders the page's generated tables, and holds the two inventories the page
cites: every layer carrying `record_id` (or the bound the format changes) and
the VERSION chain. Each anchor names a file and a token that must be on
exactly one of its lines. The page cites the file and the token, never a line
number, so a line moved by an unrelated edit keeps the citation true, and a
token that is gone or no longer unique reddens scripts/check_nvm_format_32x32.py.
Processor sources are named by stem and located through scripts/pp_srcs.py,
never spelled out here.
"""

from __future__ import annotations

import re
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))


@dataclass(frozen=True)
class Anchor:
    """One cited line: its file, the token only that line carries, what it holds, and the change."""

    layer: str
    where: str      # a tree path, or "pp:<stem>" for a processor source
    token: str
    today: str
    change: str


def resolve(where: str) -> Path:
    """A tree path, or a processor source found by stem through pp_srcs."""
    if not where.startswith("pp:"):
        return ROOT / where
    import pp_srcs
    stem = where[3:]
    hits = [s for s in pp_srcs.pp_sources() if Path(s).stem == stem]
    if len(hits) != 1:
        raise RuntimeError(f"{stem}: expected one processor source, found {len(hits)}")
    return ROOT / hits[0]


def shown(where: str) -> str:
    """The path as the page prints it."""
    return str(resolve(where).relative_to(ROOT))


#: What the all-fabric rows answer (#823): the format is the split placement's,
#: and the all-fabric placement keeps KLJ2 and today's limits.
KEEP = "unchanged: the all-fabric placement keeps KLJ2"

LAYERS = (
    # ---- the split placement: the one declaration and its two readers
    Anchor("Declaration", "sw/firmware/ctrl_nvm/nvm_layout3.h", "#define NVM3_CAP_NAME 907u",
           "NAME block, 907 ids", "the one declaration, every block's capacity"),
    Anchor("Declaration", "sw/firmware/ctrl_nvm/nvm_layout3.h", "#define NVM3_ID_SPACE (NVM3_ID_NAME",
           "1,129 ids", "bases chained from the capacities"),
    Anchor("F1 codec", "sw/firmware/ctrl_nvm/nvm_shape.h", "#define NVM_REC_HDR    NVM3_REC_HDR",
           "10-byte header", "layout 3"),
    Anchor("F1 codec", "sw/firmware/ctrl_nvm/nvm_shape.h", "_Static_assert(MILAN_NVM3_N_NAME <= NVM3_CAP_NAME",
           "the NAME block's refusal", "compile time, from the declaration"),
    Anchor("F1 codec", "sw/firmware/ctrl_nvm/nvm_shape.h",
           "#define NVM_JOURNAL_OFFSET MILAN_FLASH_JOURNAL_KLJ3_OFFSET", "journal_klj3", "the 640 KiB journal"),
    Anchor("F1 codec", "sw/firmware/ctrl_nvm/nvm_shape.h", "#define NVM_KLJ3_MAX       NVM_SLOT_BYTES",
           "container up to a slot", "KLJ3 rule 3"),
    Anchor("F1 codec", "sw/firmware/ctrl_nvm/nvm_klj2.c",
           "static const uint16_t nvm_mapout_entries[NVM_MAP_PORTS]", "32 ports, 16-bit counts", "done"),
    Anchor("F1 codec", "sw/firmware/ctrl_nvm/nvm_klj2.c", "if (nvm_rd32le(hdr) == NVM_KLJ2_MAGIC)",
           "KLJ2 refused `VD_VER`", "decision 2"),
    Anchor("F1 codec", "sw/firmware/ctrl_nvm/nvm_klj2.h", "uint16_t id;", "16-bit id", "done"),
    Anchor("F1 store", "sw/firmware/ctrl_nvm/nvm_store.c", "rec[4] == (uint8_t)(r.id >> 8)",
           "16-bit id at bytes 4 and 5", "done"),
    Anchor("F1 store", "sw/firmware/ctrl_nvm/nvm_store.c", "#define NVM_WORDS ((NVM_ID_SPACE + 31u) / 32u)",
           "open bits, 36 words", "decision 6"),
    Anchor("F1 store", "sw/firmware/ctrl_nvm/nvm_store.c", "v->count++;", "the open records' count",
           "decision 6"),
    Anchor("F1 store", "sw/firmware/ctrl_nvm/nvm_store.c", "nvm_legacy_check();",
           "today's journal read, never written", "decision 2"),
    Anchor("F1 store", "sw/firmware/ctrl_nvm/nvm_store.c", "(++nvm.block < NVM_ERASE_BLOCKS)",
           "every block the container spans", "the whole-image commit"),
    Anchor("F1 port", "sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c",
           "return addr >= NVM_JOURNAL_OFFSET &&", "writes only journal_klj3", "done"),
    Anchor("F1 link", "sw/litex/ctrl_memory.py", "def stage_bytes(shape: object)",
           "stage = KLJ3 container", "whole container until the append path"),
    Anchor("F1 link", "sw/litex/milan_soc.py", "split_constants(_nvm_split, _nvm_shape)",
           "the split SoC's constants", "from the builder's split output"),
    Anchor("F1 link", "sw/litex/milan_soc.py", '"journal_klj3": {"offset": 0xE4_0000',
           "640 KiB journal", "below today's"),
    Anchor("Builder", "sw/builder/endstation_builder.py", "def emit_nvm_split(",
           "nvm_split.json", "refused over a layout 3 block"),
    Anchor("Scripts", "scripts/nvm_klj3.py", 'hdr = struct.pack(">HBBHH"', "16-bit id frame",
           "the split's reference"),
    Anchor("Scripts", "scripts/nvm_layout3.py", "def read(", "the declaration's reader", "done"),
    # ---- the all-fabric placement: the processor's port and its managers
    Anchor("F07.8 framing", "pp:KL_pp_nvm_port", "HDR_LEN_C  = 16'd8", "8-byte header", KEEP),
    Anchor("F07.8 framing", "pp:KL_pp_nvm_port", "[7:0]  nvm_record_id_i", "8-bit record id in", KEEP),
    Anchor("F07.8 framing", "pp:KL_pp_nvm_port", "[7:0]  dev_region_o", "8-bit region out", KEEP),
    Anchor("F07.8 framing", "pp:KL_pp_nvm_port", "MAX_PAYLOAD_P = 1024", "1,024-byte payload cap", KEEP),
    Anchor("F07.8 framing", "pp:KL_acmp_nvm_shadow", "REC_ID_BASE_P = 8'h20", "BINDING base 32", KEEP),
    Anchor("F07.8 framing", "pp:KL_acmp_nvm_shadow", "LAYOUT_VER_P  = 8'h02", "layout 2", KEEP),
    Anchor("F07.8 framing", "pp:KL_acmp_nvm_shadow", "DEB_TICKS_P   = 500", "500 ms window", KEEP),
    Anchor("F07.8 framing", "pp:KL_aecp_nvm_writer", "function automatic logic [7:0] sel_base_f",
           "fixed bases 0, 2, 10, 48, 64, 80, 128", KEEP),
    Anchor("F07.8 framing", "pp:KL_aecp_nvm_writer", "DEB_MS_P       = 500", "500 ms window", KEEP),
    Anchor("F07.8 framing", "pp:KL_pp_nvm_mgr_arb", "[7:0]  m0_rid_i", "8-bit ids, both managers", KEEP),
    Anchor("F07.8 framing", "pp:protocol_processor_top", "[7:0]  nvm_dev_region_o",
           "8-bit region at the top", KEEP),
    # ---- the all-fabric placement: the parent's device face and the backend
    Anchor("`dev_region_i`", "hdl/milan/KL_nvm_backend.sv", "[7:0]  dev_region_i", "8-bit region in", KEEP),
    Anchor("`dev_region_i`", "hdl/milan/KL_pp_shadow.sv", "logic [7:0]  pp_dev_region_w",
           "8-bit wire to the backend", KEEP),
    Anchor("`dev_region_i`", "hdl/milan/KL_pp_shadow.sv", "[7:0]  mrec_region_i", "8-bit map-writer id", KEEP),
    Anchor("Backend decode", "hdl/milan/KL_nvm_backend.sv", "ID_NAME_C  = 'h80", "fixed id blocks", KEEP),
    Anchor("Backend decode", "hdl/milan/KL_nvm_backend.sv", "REC_HDR_C = 8", "8-byte header", KEEP),
    Anchor("Backend decode", "hdl/milan/KL_nvm_backend.sv", "logic [255:0]          open_r",
           "256 ownership bits", KEEP),
    Anchor("Backend refusals", "hdl/milan/KL_nvm_backend.sv", "N_NAME_MAX_C = 128", "128 names", KEEP),
    Anchor("Backend refusals", "hdl/milan/KL_nvm_backend.sv", "N_STREAM_IN_P > 16",
           "16 streams per direction", KEEP),
    Anchor("Map writer", "hdl/milan/milan_datapath.sv", "amr_rid_w  = 8'h60 + 8'(p)", "ids 96 + port", KEEP),
    Anchor("Map writer", "hdl/milan/milan_datapath.sv", "debounce (DR2a,", "500 ms window", KEEP),
    Anchor("Firmware, shipping writer", "sw/firmware/milan_baremetal/milan_baremetal.c",
           "NVM_ID_NAME  0x80u", "fixed id blocks", KEEP),
    Anchor("Firmware, shipping writer", "sw/firmware/milan_baremetal/milan_baremetal.c",
           "NVM_SLOT_BYTES (MILAN_FLASH_JOURNAL_SIZE / 2u)", "two 64 KiB slots", KEEP),
    Anchor("Builder", "sw/builder/endstation_builder.py", "if len(lst) > 16:",
           "16 streams per direction", "kept: a #859 census limit, not this format's"),
    Anchor("Builder", "sw/builder/endstation_builder.py", "if aem_name_entries > capacity:",
           "128 names, the all-fabric shape header", KEEP),
    Anchor("Builder", "sw/builder/endstation_builder.py", '"nvm_base": base +', "64 KiB sub-windows", KEEP),
    Anchor("Scripts", "scripts/nvm_contract.py", "ALLOC = {", "layout 2's fixed blocks", KEEP),
    Anchor("Scripts", "scripts/nvm_klj2.py", 'struct.pack(">HBBH"', "8-bit id frame", KEEP),
    Anchor("Mailbox contract", "sw/mailbox/mailbox.yaml", "bound_talkers: 16",
           "16 bound talkers, as the BINDING block", "a #859 decision, not this format"),
)

#: the page's other file:line citations, held the same way
CITED = (
    Anchor("name count", "sw/builder/endstation_builder.py", "def aem_name_count(", "", ""),
    Anchor("capacity reader", "sw/builder/endstation_builder.py", "def nvm_name_capacity(", "", ""),
    Anchor("key owner", "hdl/milan/milan_datapath.sv", "owner register only ever holds", "", ""),
    Anchor("datasheet", "scripts/nvm_contract.py", "Micron N25Q128 Table 32", "", ""),
    Anchor("flash map", "sw/litex/milan_soc.py", '"journal_klj3": {"offset": 0xE4_0000', "", ""),
    Anchor("SPI clock", "sw/litex/milan_soc.py", "clk_freq=int(12.5e6)", "", ""),
    Anchor("Arty flash part", "sw/litex/milan_soc.py", "S25FL128S(SpiCodes.READ_1_1_1)", "", ""),
)

VERSION_CHAIN = (
    Anchor("CSR", "hdl/common/csr/milan_csr.sv", "VERSION = 32'h0002_0060", "", ""),
    Anchor("CSR suite", "tb/verilator/csr/sim_main.cpp", "0x00020060", "", ""),
    Anchor("Datapath", "tb/verilator/milan_dp/sim_main.cpp", "0x00020060", "", ""),
    Anchor("Every stream shape", "tb/verilator/milan_dp/sim_nxn.cpp", "0x00020060", "", ""),
    Anchor("gPTP option", "tb/verilator/milan_dp/sim_gptp.cpp", "0x00020060", "", ""),
    Anchor("Pruning", "tb/verilator/milan_dp/sim_prune.cpp", "0x00020060", "", ""),
)


def tree_text(a: Anchor) -> str:
    """The text of the file an anchor cites, as the tree holds it."""
    return resolve(a.where).read_text()


def anchor_lines(a: Anchor, read: Callable[[Anchor], str] = tree_text) -> list[int]:
    """The lines, counted from 1, of the anchor's file that carry its token."""
    return [k for k, text in enumerate(read(a).splitlines(), 1) if a.token in text]


def anchor_findings(anchors: tuple[Anchor, ...], read: Callable[[Anchor], str] = tree_text) -> list[str]:
    """Every anchor whose token is gone from its file or is on more than one line."""
    bad = []
    for a in anchors:
        hits = anchor_lines(a, read)
        if not hits:
            bad.append(f"{shown(a.where)} no longer carries `{a.token}`")
        elif len(hits) > 1:
            bad.append(f"{shown(a.where)} carries `{a.token}` on lines {', '.join(map(str, hits))}; "
                       f"an anchor's token must be on one line")
    return bad


def cited(a: Anchor) -> str:
    """How the page cites an anchor: its token, then its file."""
    return f"`{a.token}` in `{shown(a.where)}`"


# ------------------------------------------------------------- formatting ----

def num(n: int | None) -> str:
    """An integer with thousands separators, or a dash when absent."""
    return "--" if n is None else f"{n:,}"


def dec(x: float, places: int = 2) -> str:
    """A decimal with thousands separators."""
    return f"{x:,.{places}f}"


def kib(n: int) -> str:
    """A byte count in whole KiB."""
    return f"{n // 1024:,}"


def table(head: list[str], rows: list[list[str]], right: int = 1) -> str:
    """A Markdown table, columns from `right` on right-aligned."""
    out = ["| " + " | ".join(head) + " |",
           "|" + "|".join("---" if k < right else "---:" for k in range(len(head))) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(out)


def figure_map(r: dict, points: tuple, prop: dict, est: dict) -> dict[str, str]:
    """Every scalar figure the page quotes inline, formatted as it prints."""
    f = {}
    for p in points:
        v = r["points"][p.key]
        for k in ("names", "records", "klj2_bytes", "base_bytes", "base_pages", "max_payload",
                  "descriptors", "raw_bytes", "names_bytes", "maps_out_bytes", "highest_id",
                  "f1_stage_now", "f1_stage_new", "open_ff", "open_lut", "own_words"):
            f[f"{p.key}_{k}"] = num(v[k])
        f[f"{p.key}_klj2_pct"] = f"{v['klj2_pct']:.0f}"
        f[f"{p.key}_names_pct"] = f"{v['names_pct']:.0f}"
        f[f"{p.key}_maps_out_pct"] = f"{v['maps_out_pct']:.0f}"
        f[f"{p.key}_compact_ms"] = dec(v["compact_ms"])
        f[f"{p.key}_commit_now_ms"] = dec(v["commit_now_ms"])
        f[f"{p.key}_desc_bytes"] = num(v["desc_bytes"])
    rule = r["rule"]
    for fam in ("tdm8", "census"):
        const, per = fit(rule, fam)
        f[f"{fam}_const"], f[f"{fam}_per_stream"] = num(const), num(per)
        f[f"{fam}_refused_names"] = num(rule[(fam, "refused")])
    sp = r["space"]
    f["ids_total"], f["id_bits"] = num(sp["total"]), num(sp["bits"])
    f["rid_field_bits"] = num(prop["rid_field_bits"])
    name = sp["blocks"][-1]
    f["name_first"], f["name_last"], f["name_past"] = num(name[1]), num(name[2]), num(name[2] + 1)
    f["name_cap_over"] = num(name[3] + 1)
    f["au_max"], f["cd_max"] = num(sp["au_max"]), num(sp["cd_max"])
    s = r["save"]
    for k in ("t_page_ms", "t_seg_ms", "fabric_ms", "split_ms", "susp_allow_ms", "no_suspend_ms",
              "big_ms", "one_name_ms", "commit_min_ms", "t_prog_ms", "t_read_ms"):
        f[k] = dec(s[k], 3 if k in ("t_prog_ms", "t_read_ms", "t_page_ms", "one_name_ms") else 2)
    f["split_typ_ms"], f["fabric_typ_ms"] = dec(s["split_typ_ms"]), dec(s["fabric_typ_ms"])
    f["susp_typ_us"], f["susp_margin"] = num(prop["susp_typ_us"]), num(s["susp_margin"])
    for k in ("p_cap", "cap_bytes", "names_per_save", "bigs_per_save", "big_rec", "big_pages",
              "commit_now_ms", "sectors", "log_pages", "reserve_pages", "boot_reads", "name_rec"):
        f[k] = num(s[k])
    for k in ("slot_bytes", "journal_bytes", "journal_start", "journal_end", "gap_bytes",
              "slot_now_bytes", "old_journal_bytes", "images_end"):
        f[k.replace("_bytes", "") + "_kib"] = kib(s[k])
    f["t_erase_s"] = dec(s["t_erase_ms"] / 1000, 0)
    f["rate_pages_s"] = dec(s["rate_pages_s"], 1)
    f["rate_bytes_s"] = num(round(s["rate_bytes_s"]))
    f["boot_pass_ms"] = dec(s["boot_pass_ms"])
    f["boot_all_ms"] = dec(s["boot_pass_ms"] * s["boot_reads"])
    for k in ("w_prod_ms", "w_fw_ms", "bound_ms", "commit_timeout_ms", "rec_hdr_bytes"):
        f[k] = num(prop[k])
    w = r["window"]
    for k in ("window_bytes", "sub_now", "sub_new", "resp_bytes"):
        f[k.replace("_bytes", "") + "_kib"] = kib(w[k])
    f["desc_room"] = num(w["desc_room"])
    f["p32_window_new"] = num(r["points"]["p32"]["window_new"])
    lifts = r["lifts"]["p32"]
    f["lift_name_capacity"] = num(lifts["name_capacity"])
    f["lift_srp_bits"] = num(lifts["srp_ctx_idx_bits"])
    f["lift_stream_cap"] = num(lifts["stream_cap"])
    if lifts != r["lifts"]["t32"]:
        raise RuntimeError("the two lifted builds read different limits")
    meas = r["area"]["measured"]
    f["meas_1x1_lut"], f["meas_1x1_ff"] = num(meas["1x1"][0]), num(meas["1x1"][1])
    f["meas_8x8_lut"], f["meas_8x8_ff"] = num(meas["8x8"][0]), num(meas["8x8"][1])
    for k in ("ram_open_lut", "lut_per_open_bit", "width_lut", "width_ff"):
        f[k] = num(est[k])
    f["id_space_words"] = num(r["area"]["id_space_words"])
    rom = re.search(r"AEM ROM (\d+) B \+ \d+ B MVU scratch exceeds the 16-bit store address space "
                    r"\((\d+) B\)", r["refusals"]["t32"] or "")
    if not rom:
        raise RuntimeError("the 32x32 TDM8 packer refusal moved")
    f["t32_rom_bytes"], f["rom_space_bytes"] = num(int(rom.group(1))), num(int(rom.group(2)))
    f["fw_window_now_ms"] = num(r["windows_now"]["firmware"])
    f["version_minor"] = num(r["version"] & 0xFFFF)
    f["max_payload_cap"] = num(r["max_payload_cap"])
    f["t_se_s"] = dec(r["datasheet"]["t_se_ms"] / 1000, 0)
    f["t_pp_ms"] = num(r["datasheet"]["t_pp_ms"])
    f["spi_mhz"] = dec(r["datasheet"]["spi_hz"] / 1e6, 1)
    f["per_stream_diff"] = num(fit(rule, "tdm8")[1] - fit(rule, "census")[1])
    for p in points:
        v = r["points"][p.key]
        f[f"{p.key}_in_cl"] = _sets(v["in_clusters"])
        f[f"{p.key}_out_cl"] = _sets(v["out_clusters"])
    f["prod_window_now_ms"] = num(r["windows_now"]["producer"])
    return f


def fit(rule: dict, family: str) -> tuple[int, int]:
    """The exact integer rule names = const + per * N, or a refusal."""
    pts = sorted((n, v) for (fam, n), v in rule.items() if fam == family and n != "refused")
    (n0, v0), (n1, v1) = pts[0], pts[1]
    per = (v1 - v0) // (n1 - n0)
    const = v0 - per * n0
    off = [n for n, v in pts if v != const + per * n]
    if off or (v1 - v0) % (n1 - n0):
        raise RuntimeError(f"{family}: the writable-name count is not one line in N at {off}")
    return const, per


# ------------------------------------------------------------------ blocks ----

def _per_point(r: dict, points: tuple, rows: list[tuple[str, object]]) -> str:
    """A table with one column per point; each row is (label, key or callable)."""
    out = []
    for label, key in rows:
        cells = []
        for p in points:
            v = r["points"][p.key]
            val = key(v) if callable(key) else v[key]
            cells.append(val if isinstance(val, str) else num(val))
        out.append([label] + cells)
    return table(["Quantity"] + [p.label for p in points], out)


def _sets(values: list[int]) -> str:
    """A per-port value; one figure when every port carries the same."""
    return " / ".join(num(v) for v in values)


def block_points(r: dict, points: tuple) -> str:
    """Section 1: what each point's build produced."""
    return _per_point(r, points, [
        ("AAF streams per direction", "streams"),
        ("STREAM_INPUT / STREAM_OUTPUT", lambda v: f"{num(v['si'])} / {num(v['so'])}"),
        ("STREAM_PORT_INPUT / OUTPUT", lambda v: f"{num(v['spi'])} / {num(v['spo'])}"),
        ("AUDIO_CLUSTER", "clusters"),
        ("CLOCK_SOURCE", "cs"),
        ("Clusters per input port", lambda v: _sets(v["in_clusters"])),
        ("Clusters per output port", lambda v: _sets(v["out_clusters"])),
        ("Map entries per output port", lambda v: _sets(v["out_entries"])),
        ("Descriptors", "descriptors"),
        ("Writable names, the builder's count", "names"),
        ("Writable names, the AEMI header", lambda v: num(v["names_aemi"]) if v["names_aemi"]
         else "refused"),
        ("Descriptor image bytes", lambda v: num(v["desc_bytes"]) if v["desc_bytes"] else "refused"),
    ])


def block_rule(r: dict) -> str:
    """Section 1: the per-stream name rule of each family, built point by point."""
    rows = []
    for fam, cfg in (("tdm8", "endstation_ax7101_1x1_tdm8"), ("census", "endstation_ax7101_8x8")):
        const, per = fit(r["rule"], fam)
        pts = sorted((n, v) for (f, n), v in r["rule"].items() if f == fam and n != "refused")
        built = ", ".join(f"{num(n)}: {num(v)}" for n, v in pts)
        rows.append([f"`{cfg}` rows", built, f"{num(const)} + {num(per)} x N",
                     num(r["rule"][(fam, "refused")])])
    return table(["Family", "N: names, as built", "Rule", "First refusal, names"], rows, right=3)


def block_space(r: dict) -> str:
    """Section 2: the derived record space."""
    rules = {"CFG_IDX": "1", "SUID": "1", "RATE": "AUDIO_UNIT", "CLKSRC": "CLOCK_DOMAIN",
             "MCR": "CLOCK_DOMAIN", "BINDING": "STREAM_INPUT", "FMT_IN": "STREAM_INPUT",
             "FMT_OUT": "STREAM_OUTPUT", "PT_OFS": "STREAM_OUTPUT",
             "MAPS_IN": "STREAM_PORT_INPUT", "MAPS_OUT": "STREAM_PORT_OUTPUT",
             "NAME": "writable names"}
    sized = {"RATE": "the backend's bound", "CLKSRC": "the backend's bound",
             "MCR": "the backend's bound", "CFG_IDX": "singleton", "SUID": "singleton"}
    rows = [[g, rules[g], sized.get(g, "the bound shape"), num(first), num(last), num(n)]
            for g, first, last, n in r["space"]["blocks"]]
    sp = r["space"]
    rows.append(["**all**", f"{num(sp['bits'])}-bit id", "", "0", num(sp["total"] - 1),
                 num(sp["total"])])
    return table(["Block", "Count rule", "Sized by", "First id", "Last id", "Ids"], rows, right=3)


def block_ids(r: dict, points: tuple) -> str:
    """Section 2: each point inside the derived space."""
    return _per_point(r, points, [
        ("Records", "records"),
        ("Highest id, derived space", "highest_id"),
        ("Records within today's 256 ids", lambda v: "yes" if v["records"] <= 256 else "no"),
        ("Inside the derived space", lambda v: "yes" if v["highest_id"] < r["space"]["total"]
         else "no"),
    ])


def block_image(r: dict, points: tuple) -> str:
    """Section 3: the byte arithmetic, today's framing and the proposal's."""
    return _per_point(r, points, [
        ("Fixed groups, framed", "fixed_bytes"),
        ("Input maps, framed", "maps_in_bytes"),
        ("Output maps, framed", "maps_out_bytes"),
        ("Names, framed", "names_bytes"),
        ("Record area, 8-byte headers", "raw_bytes"),
        ("KLJ2 image today", "klj2_bytes"),
        ("Share of one 64 KiB slot", lambda v: f"{v['klj2_pct']:.0f}%"),
        ("Largest payload (cap 1,024)", "max_payload"),
        ("Record area, 10-byte headers", "raw_new_bytes"),
        ("Base segment", "base_bytes"),
        ("Base segment, pages", "base_pages"),
    ])


def block_slot(r: dict, fmap: dict) -> str:
    """Section 3: the slot, the log and the journal."""
    rows = [
        ("Erase blocks per slot", fmap["sectors"], "smallest count holding twice the bound's base"),
        ("Slot", f"{fmap['slot_kib']} KiB", "today 64 KiB"),
        ("Log after the bound's base", f"{fmap['log_pages']} pages", "at least one base"),
        ("Compaction reserve", f"{fmap['reserve_pages']} pages", "half the log"),
        ("Journal, two slots", f"{fmap['journal_kib']} KiB", "today 128 KiB"),
        ("New journal", f"{fmap['journal_start_kib']} to {fmap['journal_end_kib']} KiB",
         "directly below today's"),
        ("Free flash below it", f"{fmap['gap_kib']} KiB", "after the AEM slot"),
    ]
    return table(["Item", "Value", "Rule"], [list(x) for x in rows], right=3)


def block_window(r: dict, points: tuple, fmap: dict) -> str:
    """Section 3: the ppmem window and the F1 stage."""
    w = r["window"]
    today = w["resp_bytes"] + 2 * w["sub_now"]
    return _per_point(r, points, [
        ("Descriptor image", lambda v: num(v["desc_bytes"]) if v["desc_bytes"] else "refused"),
        ("Base fits today's 64 KiB sub-window", lambda v: "yes" if v["base_bytes"] <= w["sub_now"]
         else "no"),
        ("Window use, proposal", lambda v: num(v["window_new"]) if v["window_new"] else "--"),
        ("F1 stage today", "f1_stage_now"),
        ("F1 stage, proposal", "f1_stage_new"),
    ]) + f"\n\nToday the window holds the image plus {num(today)} B; the proposal, plus " \
        f"{num(w['fixed_new'])} B, of {num(w['window_bytes'])} B."


def block_save(r: dict, fmap: dict) -> str:
    """Section 4: the save path's worst case against the bound."""
    s = r["save"]
    rows = [
        ("Producer first-dirty window", f"{fmap['w_prod_ms']} ms", f"today {fmap['prod_window_now_ms']} ms"),
        ("Firmware first-dirty window", f"{fmap['w_fw_ms']} ms", f"today {fmap['fw_window_now_ms']} ms"),
        ("One page programmed", f"{fmap['t_prog_ms']} ms", "tPP 5 ms, and 263 B on the 1x link"),
        ("One page read back", f"{fmap['t_read_ms']} ms", "260 B on the 1x link"),
        ("One page, both", f"{fmap['t_page_ms']} ms", ""),
        ("Segment cap", f"{fmap['p_cap']} pages", "a segment ends before the next window"),
        ("Records per segment", f"{fmap['cap_bytes']} B", "less the 44-byte frame"),
        ("Ahead of it: one compaction page", f"{fmap['t_page_ms']} ms", "compaction yields per page"),
        ("The segment itself", f"{fmap['t_seg_ms']} ms", ""),
        ("**Worst case, all-fabric**", f"**{fmap['fabric_ms']} ms** + suspend", "both windows"),
        ("**Worst case, split**", f"**{fmap['split_ms']} ms** + suspend", "firmware window only"),
        ("Room left for the suspend latency", f"{fmap['susp_allow_ms']} ms", "not in the tree"),
        ("Without erase suspend", f"{fmap['no_suspend_ms']} ms", "tSE 3,000 ms ahead"),
    ]
    del s
    return table(["Term", "Value", "Source"], [list(x) for x in rows], right=3)


def block_compaction(r: dict, points: tuple) -> str:
    """Section 4: compaction off the save path, against today's whole commit."""
    return _per_point(r, points, [
        ("Base segment, pages", "base_pages"),
        ("Compaction, ms", lambda v: dec(v["compact_ms"])),
        ("Today's whole-image commit, ms", lambda v: dec(v["commit_now_ms"])),
    ])


def block_layers() -> str:
    """Section 6: every layer, by file and token: what it holds and its state."""
    rows = [[a.layer, f"`{shown(a.where)}`", f"`{a.token}`", a.today, a.change] for a in LAYERS]
    return table(["Layer", "File", "Line carrying", "Holds", "Change"], rows, right=5)


def block_version() -> str:
    """Section 5: the VERSION chain."""
    rows = [[a.layer, f"`{shown(a.where)}`", f"`{a.token}`"] for a in VERSION_CHAIN]
    return table(["Assertion", "File", "Line carrying"], rows, right=3)


def block_area(r: dict, points: tuple, est: dict) -> str:
    """Section 7's ESTIMATE: the ownership vector at each point."""
    return _per_point(r, points, [
        ("Ownership bits, one per record", "open_ff"),
        ("Ownership read words", "own_words"),
        (f"ESTIMATE flop-held LUT, {est['lut_per_open_bit']} per bit and the read mux", "open_lut"),
        ("ESTIMATE OR-reduce depth, LUT6 levels", "or_levels"),
        ("ESTIMATE read-mux depth, levels", "mux_levels"),
    ])


def block_limits(fmap: dict) -> str:
    """Section 4: what one segment holds, and what the slot sustains."""
    rows = [
        ("One name alone", f"{fmap['one_name_ms']} ms", f"{fmap['name_rec']} B record, one page"),
        ("The largest record alone", f"{fmap['big_ms']} ms",
         f"{fmap['big_rec']} B output map, {fmap['big_pages']} pages"),
        ("Names in one segment", fmap["names_per_save"], f"{fmap['cap_bytes']} B"),
        ("Largest records in one segment", fmap["bigs_per_save"], f"{fmap['cap_bytes']} B"),
        ("Compaction at the bound", f"{fmap['t32_compact_ms']} ms", "off the save path"),
        ("Background erase of one slot", f"{fmap['t_erase_s']} s", f"{fmap['sectors']} x tSE 3 s"),
        ("Sustained save volume", f"{fmap['rate_pages_s']} pages/s",
         f"{fmap['rate_bytes_s']} B/s, assumption A2"),
        ("Boot read, both slots once", f"{fmap['boot_pass_ms']} ms", "1x link"),
        ("Boot read, three reads each", f"{fmap['boot_all_ms']} ms", "FASTCONNECT section 7, two of three reads"),
    ]
    return table(["Case", "Value", "Basis"], [[a, str(b), c] for a, b, c in rows], right=3)


#: The state column: done in the split's store, or built under #876, the
#: append-only save path (decisions 3, 4, 5 and 7) that section 4 designs.
DONE, APPEND = "done, split", "built under #876"

TESTS = (
    ("NAME first id {name_first}",
     "F1 `name_block_ends`; builder gate 39 pins it; the reference gate holds every id in its block",
     "`name_base_moved`; a block before NAME grown", DONE),
    ("NAME last id {name_last}",
     "F1 at {t32_names} names: `name_block_ends`; `capacity_round_trip` over two erase blocks; "
     "`capacity_commit_over_stale`, a commit over an older container, each erase at its block's address",
     "`name_last_dropped`; `first_block_only`; `erase_first_block_every_time`", DONE),
    ("NAME one past, {name_past}",
     "F1 `one_past_refused` and the parity table, `VD_REC`; {name_cap_over} names do not compile",
     "`id_space_unbounded`; the NAME assert removed", DONE),
    ("Every other block", "each block's first id read from the declaration; the reference gate's ledger at every shape",
     "the last name left out of the reference's inventory", DONE),
    ("Capacity", "builder gate 39: the 32x32 TDM8 overlay's {t32_names} names accepted, one more refused; "
     "the all-fabric header still refuses it", "capacity 906 and 908; the all-fabric bound read from the split's",
     DONE),
    ("Old journal on boot", "F1 `klj2_journal_refused`, `klj2_in_slot_refused`, `klj2_journal_unreadable`: "
     "blank, `VD_VER` recorded, today's journal unwritten; `legacy_other_format_not_recorded`, "
     "`own_refusal_kept_over_legacy`; `klj2_journal_at_its_flash_map_address`, today's slots from the flash map",
     "`klj2_not_recognised`, `klj2_reinterpreted`, `legacy_not_read`, `legacy_reason_dropped`, "
     "`legacy_any_nonblank_header`, `ver_overrides_own_refusal`, `legacy_b_wrong_place`", DONE),
    ("Append order", "a delta over the base: the last value wins", "segments applied in reverse", APPEND),
    ("Torn append", "a cut at every page restores the last closing segment",
     "a segment accepted without its CRC", APPEND),
    ("Torn compaction", "a cut at every page boots the old slot, losing nothing",
     "authority moved before the new trailer verifies", APPEND),
    ("Erase in progress", "a save during the background erase suspends it",
     "the save waits for the erase", APPEND),
    ("Save bound", "model time, change to verified, at most {bound_ms} ms at 32x32 TDM8",
     "a {fw_window_now_ms} ms firmware window", APPEND),
    ("Reserve exhausted", "the save waits, is published pending and is not lost", "the save dropped", APPEND),
    ("Commit deadline", "at least twice the worst append at every shape", "a 300 ms deadline", APPEND),
    ("Payload cap", "the F1 store sizes its payload buffer from the shape (`NVM_PAYLOAD_MAX`)",
     "none: the 1,024 B `MAX_PAYLOAD_P` is the processor's", "all-fabric unchanged"),
    ("Fit", "the container within one slot, asserted at compile time; base and log", "a two-block slot",
     APPEND),
    ("VERSION", "the format's chain: KLJ3 major 3, layout 3, KLJ2 `VD_VER` (`wrong_version_falls_back`, "
     "majors 2 and 4)", "`no_version_check`", "done, split; the gateware VERSION not moved, as ruled (#823)"),
    ("Map entry widths", "a count past the codec's table does not compile: 256 entries on an input port, "
     "65,536 on an output port", "either width assert removed", DONE),
)


def block_tests(fmap: dict) -> str:
    """Section 8: the test plan, one plant per rule, and its state."""
    rows = [[f"T{k}", rule.format(**fmap), test.format(**fmap), plant.format(**fmap), state]
            for k, (rule, test, plant, state) in enumerate(TESTS, 1)]
    return table(["#", "Rule", "Test", "Plant that must be caught", "State"], rows, right=5)


def blocks(r: dict, points: tuple, prop: dict, est: dict) -> dict[str, str]:
    """Every generated block of the page, by name."""
    fmap = figure_map(r, points, prop, est)
    return {
        "points": block_points(r, points), "rule": block_rule(r), "space": block_space(r),
        "ids": block_ids(r, points), "image": block_image(r, points),
        "slot": block_slot(r, fmap), "window": block_window(r, points, fmap),
        "save": block_save(r, fmap), "compaction": block_compaction(r, points),
        "version": block_version(), "layers": block_layers(),
        "area": block_area(r, points, est), "tests": block_tests(fmap),
        "limits": block_limits(fmap),
    }
