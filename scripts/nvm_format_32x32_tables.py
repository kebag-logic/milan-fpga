#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""nvm_format_32x32_tables.py - the page blocks of SAVED_STATE_FORMAT_32X32.md.

`scripts/nvm_format_32x32.py` computes the figures; this module formats them,
renders the page's generated tables, and holds the two inventories the page
cites by file:line: every layer carrying `record_id` (or the bound the format
changes) and the VERSION chain. Each anchor names a token its line must still
carry, so a moved line reddens scripts/check_nvm_format_32x32.py instead of
leaving a stale citation. Processor sources are named by stem and located
through scripts/pp_srcs.py, never spelled out here.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))


@dataclass(frozen=True)
class Anchor:
    """One cited line: where it is, what it must still read, and the change."""

    layer: str
    where: str      # a tree path, or "pp:<stem>" for a processor source
    line: int
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


LAYERS = (
    # ---- the KLJ2 / F07.8 framing: the processor's port and its managers
    Anchor("F07.8 framing", "pp:KL_pp_nvm_port", 182, "HDR_LEN_C  = 16'd8",
           "8-byte header", "10-byte header, layout 3"),
    Anchor("F07.8 framing", "pp:KL_pp_nvm_port", 135, "[7:0]  nvm_record_id_i",
           "8-bit record id in", "16-bit field, 11 bits decoded"),
    Anchor("F07.8 framing", "pp:KL_pp_nvm_port", 160, "[7:0]  dev_region_o",
           "8-bit region out", "widen with the id"),
    Anchor("F07.8 framing", "pp:KL_pp_nvm_port", 115, "MAX_PAYLOAD_P = 1024",
           "1,024-byte payload cap", "derived: the shape's largest payload"),
    Anchor("F07.8 framing", "pp:KL_acmp_nvm_shadow", 127, "REC_ID_BASE_P = 8'h20",
           "BINDING base 32", "derived BINDING base"),
    Anchor("F07.8 framing", "pp:KL_acmp_nvm_shadow", 137, "LAYOUT_VER_P  = 8'h02",
           "layout 2", "layout 3"),
    Anchor("F07.8 framing", "pp:KL_acmp_nvm_shadow", 139, "DEB_TICKS_P   = 500",
           "500 ms window", "the producer window of section 5"),
    Anchor("F07.8 framing", "pp:KL_aecp_nvm_writer", 397, "function automatic logic [7:0] sel_base_f",
           "fixed bases 0, 2, 10, 48, 64, 80, 128", "derived bases"),
    Anchor("F07.8 framing", "pp:KL_aecp_nvm_writer", 193, "DEB_MS_P       = 500",
           "500 ms window", "the producer window of section 5"),
    Anchor("F07.8 framing", "pp:KL_pp_nvm_mgr_arb", 79, "[7:0]  m0_rid_i",
           "8-bit ids, both managers", "widen with the id"),
    Anchor("F07.8 framing", "pp:protocol_processor_top", 598, "[7:0]  nvm_dev_region_o",
           "8-bit region at the top", "widen with the id"),
    # ---- the parent's device face and the backend
    Anchor("`dev_region_i`", "hdl/milan/KL_nvm_backend.sv", 156, "[7:0]  dev_region_i",
           "8-bit region in", "widen with the id"),
    Anchor("`dev_region_i`", "hdl/milan/KL_pp_shadow.sv", 1064, "logic [7:0]  pp_dev_region_w",
           "8-bit wire to the backend", "widen with the id"),
    Anchor("`dev_region_i`", "hdl/milan/KL_pp_shadow.sv", 417, "[7:0]  mrec_region_i",
           "8-bit map-writer id", "widen with the id"),
    Anchor("Backend decode", "hdl/milan/KL_nvm_backend.sv", 243, "ID_NAME_C  = 'h80",
           "fixed id blocks", "derived blocks of section 2"),
    Anchor("Backend decode", "hdl/milan/KL_nvm_backend.sv", 228, "REC_HDR_C = 8",
           "8-byte header", "10-byte header"),
    Anchor("Backend decode", "hdl/milan/KL_nvm_backend.sv", 311, "IDW_C = 9",
           "9-bit compare", "12-bit compare"),
    Anchor("Backend decode", "hdl/milan/KL_nvm_backend.sv", 194, "[5:0]  csr_addr_i",
           "16 map ports per table", "32 ports: one more index bit"),
    Anchor("Backend decode", "hdl/milan/KL_nvm_backend.sv", 531, "logic [255:0]          open_r",
           "256 ownership bits", "one bit per id, section 7"),
    Anchor("Backend decode", "hdl/milan/KL_nvm_backend.sv", 1124, "gi < 256",
           "256-id ownership loop", "the derived id count"),
    Anchor("Backend refusals", "hdl/milan/KL_nvm_backend.sv", 248, "N_NAME_MAX_C = 128",
           "128 names", "the derived NAME block"),
    Anchor("Backend refusals", "hdl/milan/KL_nvm_backend.sv", 285, "N_STREAM_IN_P > 16",
           "16 streams per direction", "the derived stream blocks"),
    Anchor("Backend refusals", "hdl/milan/KL_nvm_backend.sv", 288, "N_SPORT_IN_P > 16",
           "16 stream ports", "the derived map blocks"),
    Anchor("Map writer", "hdl/milan/milan_datapath.sv", 5252, "amr_rid_w  = 8'h60 + 8'(p)",
           "ids 96 + port", "derived MAPS_IN base"),
    Anchor("Map writer", "hdl/milan/milan_datapath.sv", 5262, "amr_rid_w  = 8'h70 + 8'(p)",
           "ids 112 + port", "derived MAPS_OUT base"),
    Anchor("Map writer", "hdl/milan/milan_datapath.sv", 5229, "(AMR_OK_C > 127)",
           "127-entry cursors", "cursors for 264 output keys"),
    Anchor("Map writer", "hdl/milan/milan_datapath.sv", 318, "debounce (DR2a,",
           "500 ms window", "the producer window of section 5"),
    # ---- firmware
    Anchor("Firmware, shipping writer", "sw/firmware/milan_baremetal/milan_baremetal.c", 258,
           "NVM_ID_NAME  0x80u", "fixed id blocks", "generated bases"),
    Anchor("Firmware, shipping writer", "sw/firmware/milan_baremetal/milan_baremetal.c", 373,
           "uint8_t base;", "8-bit block base and count", "16-bit"),
    Anchor("Firmware, shipping writer", "sw/firmware/milan_baremetal/milan_baremetal.c", 329,
           "NVM_SLOT_BYTES (MILAN_FLASH_JOURNAL_SIZE / 2u)", "two 64 KiB slots",
           "the slot and log of section 4"),
    Anchor("Firmware, F1 store", "sw/firmware/ctrl_nvm/nvm_shape.h", 132,
           "NVM_N_REC <= NVM_ID_SPACE", "256 ids", "the derived id count"),
    Anchor("Firmware, F1 store", "sw/firmware/ctrl_nvm/nvm_shape.h", 133,
           "MILAN_NVM_N_NAME <= 128u", "128 names", "the derived NAME block"),
    Anchor("Firmware, F1 store", "sw/firmware/ctrl_nvm/nvm_shape.h", 134,
           "NVM_IMG_LEN <= NVM_SLOT_BYTES", "image within one slot", "base within one slot"),
    Anchor("Firmware, F1 store", "sw/firmware/ctrl_nvm/nvm_shape.h", 136,
           "NVM_SLOT_BYTES == 65536u", "one erase block", "the derived slot"),
    Anchor("Firmware, F1 store", "sw/firmware/ctrl_nvm/nvm_shape.h", 33,
           "NVM_KLJ2_MAX     65536u", "64 KiB container", "format 3 bound"),
    Anchor("Firmware, F1 store", "sw/firmware/ctrl_nvm/nvm_klj2.c", 37,
           "static const uint8_t nvm_mapout_entries[16]", "16 ports, 8-bit counts",
           "32 ports, 16-bit counts"),
    Anchor("Firmware, F1 store", "sw/firmware/ctrl_nvm/nvm_klj2.h", 62, "uint8_t id;",
           "8-bit id", "16-bit"),
    Anchor("Firmware, F1 store", "sw/firmware/ctrl_nvm/nvm_store.c", 490, "rec[3] == r.id",
           "id at header byte 3", "16-bit id at bytes 4 and 5"),
    Anchor("Firmware, F1 store", "sw/firmware/ctrl_nvm/nvm_store.c", 54,
           "NVM_WORDS (NVM_ID_SPACE / 32u)", "8 ownership words", "the derived id count"),
    # ---- the F1 store's link and the SoC
    Anchor("F1 link", "sw/litex/ctrl_memory.py", 384, "def stage_bytes(", "stage = container",
           "stage = one page and one record"),
    Anchor("F1 link", "sw/litex/milan_soc.py", 4653, "MILAN_NVM_IMAGE_MAX", "64 KiB image",
           "the base bound"),
    Anchor("F1 link", "sw/litex/milan_soc.py", 3547, "_nvm_base = _resp_base - FLASH_ERASE_BLOCK",
           "64 KiB live window", "the derived sub-window"),
    Anchor("F1 link", "sw/litex/milan_soc.py", 173, '"journal": {"offset": 0xEE_0000',
           "128 KiB journal", "kept; a new journal below it"),
    # ---- the builder and the scripts
    Anchor("Builder", "sw/builder/endstation_builder.py", 1464, "if len(lst) > 16:",
           "16 streams per direction", "read from the record space"),
    Anchor("Builder", "sw/builder/endstation_builder.py", 2740, "if aem_name_entries > capacity:",
           "128 names", "the derived NAME block"),
    Anchor("Builder", "sw/builder/endstation_builder.py", 2353, '"nvm_base": base +',
           "64 KiB sub-windows", "the derived sub-windows"),
    Anchor("Scripts", "scripts/nvm_contract.py", 60, "self.ID_SPACE = 256", "256 ids",
           "the derived id count"),
    Anchor("Scripts", "scripts/nvm_contract.py", 152, "ALLOC = {", "fixed blocks",
           "derived blocks"),
    Anchor("Scripts", "scripts/nvm_contract.py", 34, "REC_HDR = 8", "8-byte header",
           "10-byte header"),
    Anchor("Scripts", "scripts/nvm_shape.py", 131, "FW_MAP_PORTS = 16", "16 map ports",
           "the shape's ports"),
    Anchor("Scripts", "scripts/nvm_klj2.py", 89, 'struct.pack(">HBBH"', "8-bit id frame",
           "16-bit id frame"),
    Anchor("Mailbox contract", "sw/mailbox/mailbox.yaml", 93, "bound_talkers: 16",
           "16 bound talkers, as the BINDING block", "a #859 decision, not this format"),
)

#: the page's other file:line citations, held the same way
CITED = (
    Anchor("name count", "sw/builder/endstation_builder.py", 2714, "def _adp_name_entries(", "", ""),
    Anchor("capacity reader", "sw/builder/endstation_builder.py", 2694, "def nvm_name_capacity(", "", ""),
    Anchor("key owner", "hdl/milan/milan_datapath.sv", 5211, "owner register only ever holds", "", ""),
    Anchor("datasheet", "scripts/nvm_contract.py", 112, "Micron N25Q128 Table 32", "", ""),
    Anchor("flash map", "sw/litex/milan_soc.py", 173, '"journal": {"offset": 0xEE_0000', "", ""),
    Anchor("SPI clock", "sw/litex/milan_soc.py", 3361, "clk_freq=int(12.5e6)", "", ""),
    Anchor("Arty flash part", "sw/litex/milan_soc.py", 3346, "S25FL128S(SpiCodes.READ_1_1_1)", "", ""),
)

VERSION_CHAIN = (
    Anchor("CSR", "hdl/common/csr/milan_csr.sv", 201, "VERSION = 32'h0002_0060", "", ""),
    Anchor("CSR suite", "tb/verilator/csr/sim_main.cpp", 355, "0x00020060", "", ""),
    Anchor("Datapath", "tb/verilator/milan_dp/sim_main.cpp", 291, "0x00020060", "", ""),
    Anchor("Every stream shape", "tb/verilator/milan_dp/sim_nxn.cpp", 3189, "0x00020060", "", ""),
    Anchor("gPTP option", "tb/verilator/milan_dp/sim_gptp.cpp", 860, "0x00020060", "", ""),
    Anchor("Pruning", "tb/verilator/milan_dp/sim_prune.cpp", 351, "0x00020060", "", ""),
)


def anchor_findings(anchors: tuple[Anchor, ...]) -> list[str]:
    """Every anchor whose line no longer carries its token."""
    bad = []
    for a in anchors:
        lines = resolve(a.where).read_text().splitlines()
        text = lines[a.line - 1] if 0 < a.line <= len(lines) else ""
        if a.token not in text:
            bad.append(f"{shown(a.where)}:{a.line} no longer reads `{a.token}`")
    return bad


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
    f["au_max"], f["cd_max"] = num(sp["au_max"]), num(sp["cd_max"])
    s = r["save"]
    for k in ("t_page_ms", "t_seg_ms", "fabric_ms", "split_ms", "susp_allow_ms", "no_suspend_ms",
              "big_ms", "one_name_ms", "commit_min_ms", "t_prog_ms", "t_read_ms"):
        f[k] = dec(s[k], 3 if k in ("t_prog_ms", "t_read_ms", "t_page_ms", "one_name_ms") else 2)
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
    """Section 6: every layer, by file:line, with its change."""
    rows = [[a.layer, f"`{shown(a.where)}:{a.line}`", a.today, a.change] for a in LAYERS]
    return table(["Layer", "Where", "Today", "Change"], rows, right=4)


def block_version() -> str:
    """Section 5: the VERSION chain."""
    rows = [[a.layer, f"`{shown(a.where)}:{a.line}`", f"`{a.token}`"] for a in VERSION_CHAIN]
    return table(["Assertion", "Where", "Reads today"], rows, right=3)


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


TESTS = (
    ("NAME first id {name_first}", "accepted by the builder, the backend decode, F1 and the codec",
     "NAME base off by one"),
    ("NAME last id {name_last}", "the 32x32 TDM8 overlay's {t32_names} names round trip",
     "block end taken as exclusive"),
    ("NAME one past, {name_past}", "backend `dev_err`, F1 refusal, builder `ConfigError`, RTL `$error`",
     "the refusal removed"),
    ("Every other block", "first, last and one-past id of each block in section 2",
     "one block sized by the wrong count"),
    ("Capacity", "{t32_names} names accepted, one more refused, in the builder and the RTL",
     "the builder reads a second copy of the bound"),
    ("Old journal on boot", "a KLJ2 journal boots blank with `VD_VER` recorded; its slots stay unwritten",
     "a reader that reinterprets major 2"),
    ("Append order", "a delta over the base: the last value wins", "segments applied in reverse"),
    ("Torn append", "a cut at every page restores the last closing segment",
     "a segment accepted without its CRC"),
    ("Torn compaction", "a cut at every page boots the old slot, losing nothing",
     "authority moved before the new trailer verifies"),
    ("Erase in progress", "a save during the background erase suspends it",
     "the save waits for the erase"),
    ("Save bound", "model time, change to verified, at most {bound_ms} ms at 32x32 TDM8",
     "a {fw_window_now_ms} ms firmware window"),
    ("Reserve exhausted", "the save waits, is published pending and is not lost", "the save dropped"),
    ("Commit deadline", "at least twice the worst append at every shape", "a 300 ms deadline"),
    ("Payload cap", "`MAX_PAYLOAD_P` covers {t32_max_payload} B", "the 1,024 B default"),
    ("Fit", "base, log and window fit at every shape", "a two-block slot"),
    ("VERSION", "the five assertions read the new VERSION", "one left at today's"),
)


def block_tests(fmap: dict) -> str:
    """Section 8: the test plan, one plant per rule."""
    rows = [[f"T{k}", rule.format(**fmap), test.format(**fmap), plant.format(**fmap)]
            for k, (rule, test, plant) in enumerate(TESTS, 1)]
    return table(["#", "Rule", "Test", "Plant that must be caught"], rows, right=4)


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
