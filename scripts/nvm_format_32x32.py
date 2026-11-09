#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""nvm_format_32x32.py - every figure of docs/design/SAVED_STATE_FORMAT_32X32.md (#823).

The page proposes the saved-state format for shapes up to 32x32 streams. Each
number on it is recomputed here from what the tree defines, and
scripts/check_nvm_format_32x32.py fails when the page and this script disagree.

WHERE EACH INPUT COMES FROM
  * The shapes. The shipped configs are built by sw/builder as they are. The
    32x32 points are those configs with 32 listener and 32 talker rows, built
    by the same builder in a child process with three of its limits lifted in
    memory: the 16-stream cap, the 5-bit SRP row index and the NAME capacity it
    reads from KL_nvm_backend.sv. Each lift first checks that the limit still
    reads as the #859 census found it, so a moved limit refuses the run.
  * The per-stream name rule of each config family, from builds at every
    stream count the unlifted builder accepts.
  * The record inventory, from scripts/nvm_shape.py inventory(); payload
    widths, framing and the datasheet maxima, from scripts/nvm_contract.py.
  * The flash map, from sw/litex/milan_soc.py, read as literals (no LiteX).
  * The proposal's own constants, in PROPOSAL below, each named on the page.

usage:
    python3 scripts/nvm_format_32x32.py            # every figure, one per line
    python3 scripts/nvm_format_32x32.py --blocks   # every generated page block
"""

from __future__ import annotations

import argparse
import ast
import json
import math
import re
import struct
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import nvm_contract as contract  # noqa: E402
import nvm_layout3  # noqa: E402
from nvm_contract import Shape  # noqa: E402
from nvm_shape import binding_base, inventory, output_map_entries  # noqa: E402
import nvm_format_32x32_tables as tables  # noqa: E402

BUILDER = ROOT / "sw/builder/endstation_builder.py"
AEMI = ROOT / "avdecc/gen_aemi_image.py"
BACKEND = ROOT / "hdl/milan/KL_nvm_backend.sv"
SOC = ROOT / "sw/litex/milan_soc.py"
FASTCONNECT = ROOT / "docs/design/SAVED_STATE_FASTCONNECT.md"

FAMILY_CONFIG = {
    "tdm8": ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml",
    "census": ROOT / "configs/endstation_ax7101_8x8.yaml",
}
#: every stream count the unlifted builder accepts for each family, the
#: points the per-stream name rule is fitted and then checked on
RULE_STREAMS = {"tdm8": (1, 2, 3, 4), "census": (1, 2, 4, 8, 9)}
#: the first stream count each family's NAME capacity refuses
REFUSED_STREAMS = {"tdm8": 5, "census": 10}

#: the descriptor types carrying a writable name, as the builder's
#: `_adp_name_entries` counts them (ENTITY counts twice through its `1 +`)
NAMED_TYPES = ("ENTITY", "CONFIGURATION", "AUDIO_UNIT", "STREAM_INPUT",
               "STREAM_OUTPUT", "AVB_INTERFACE", "CLOCK_SOURCE",
               "CLOCK_DOMAIN", "CONTROL", "AUDIO_CLUSTER")


@dataclass(frozen=True)
class Point:
    """One shape the page sizes the format at."""

    label: str      # as the page names it
    key: str        # the figure-key prefix
    family: str     # which config family
    streams: int    # AAF streams per direction
    lifted: bool    # built with the three limits lifted


POINTS = (
    Point("1x1/1if", "p1", "tdm8", 1, False),
    Point("8x8/2if", "p8", "census", 8, False),
    Point("32x32/2if", "p32", "census", 32, True),
    Point("32x32/2if TDM8", "t32", "tdm8", 32, True),
)
#: the shape the record space and the slot are sized for
BOUND = "t32"

#: The proposal's constants. Each is a design choice the page states and asks
#: a ruling on; none is a measurement.
PROPOSAL = {
    # F07.8 layout 3: magic 2, layout_version 1, reserved 1, record_id 2,
    # payload_length 2, crc16 2
    "rec_hdr_bytes": 10,
    "rid_field_bits": 16,
    # every journal segment carries the KLJ2 container's header and trailer
    "seg_hdr_bytes": contract.KLJ2_HDR,
    "seg_trailer_bytes": contract.KLJ2_TRAILER,
    # the first-dirty windows replacing D3 DR2a's 500 ms and 1,000 ms
    "w_prod_ms": 100,
    "w_fw_ms": 150,
    "bound_ms": 500,
    "commit_timeout_ms": 500,
    # the log of a slot is at least one base image: write amplification <= 2
    "log_per_base": 1,
    # a compaction starts when half the log is used
    "reserve_fraction_den": 2,
    # A3's suspend latency, graded at its typical value (#823 issue comment
    # 6730985093 item 3): N25Q128 datasheet section 9.1.20 and
    # Table 17, "Suspend Latency, Erase", 15 us typical, no maximum given
    "susp_typ_us": 15,
    # the 3-byte-address command overheads of the writer's opcodes
    # (milan_baremetal.c NVM_CMD_*): WREN 1, PP 1 + 3, RDSR 1 + 1, READ 1 + 3
    "wren_bytes": 1, "pp_cmd_bytes": 4, "rdsr_bytes": 2, "read_cmd_bytes": 4,
}

#: ESTIMATES for section 7, each labelled on the page; none is measured (#823)
AREA_EST = {"lut_per_open_bit": 3, "ff_per_open_bit": 1, "mux_inputs_per_lut": 4,
            "ram_open_lut": 100, "width_lut": 40, "width_ff": 24}


@dataclass
class Built:
    """What one point's build produced."""

    dc: dict
    spi: list
    spo: list
    names: int
    names_aemi: int | None
    desc_bytes: int | None
    aemi_refusal: str | None
    lifts: dict = field(default_factory=dict)


# ---------------------------------------------------------------- building ----

def scaled_config(family: str, streams: int, out: Path) -> Path:
    """The family's config with `streams` listener and talker rows."""
    cfg = yaml.safe_load(FAMILY_CONFIG[family].read_text())
    rows = cfg["streams"]
    first_in, first_out = rows["listeners"][0], rows["talkers"][0]
    rows["listeners"] = [dict(first_in, name=f"Stream In {k}") for k in range(streams)]
    rows["talkers"] = [dict(first_out, name=f"Stream Out {k}") for k in range(streams)]
    for waiver in cfg.get("model_lint_waivers") or []:
        if waiver.get("type") == "STREAM_PORT_INPUT":
            waiver["last"] = streams - 1
    path = out / f"{FAMILY_CONFIG[family].stem}_n{streams}.yaml"
    path.write_text(yaml.safe_dump(cfg, sort_keys=False))
    return path


def run_builder(cfg: Path, out: Path, lifted: bool) -> dict:
    """Build `cfg`; a lifted build runs in a child that reports its lifts."""
    if lifted:
        cmd = [sys.executable, str(Path(__file__).resolve()),
               "--lifted-build", str(cfg), str(out)]
    else:
        cmd = [sys.executable, str(BUILDER), str(cfg), "-o", str(out)]
    res = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
    if res.returncode:
        raise RuntimeError(f"{cfg.name}: the builder refused: "
                           f"{(res.stderr or res.stdout).strip().splitlines()[-1]}")
    lifts = {}
    for line in res.stdout.splitlines():
        if line.startswith("LIFTS "):
            lifts = json.loads(line[len("LIFTS "):])
    return lifts


def builder_names(dc: dict) -> int:
    """The builder's writable-name count: `1 + sum` over the named types."""
    return 1 + sum(int(dc[t]) for t in NAMED_TYPES)


def build_point(cfg: Path, out: Path, lifted: bool) -> Built:
    """Build one shape, then its descriptor image where the packer accepts it."""
    lifts = run_builder(cfg, out, lifted)
    overlay = json.loads((out / cfg.stem / "aem_overlay.json").read_text())
    dc = overlay["descriptor_counts"]
    img = out / f"{cfg.stem}.img.bin"
    res = subprocess.run([sys.executable, str(AEMI), "--overlay",
                          str(out / cfg.stem / "aem_overlay.json"), "-o", str(img),
                          "--line-bytes", "576"],
                         cwd=ROOT, capture_output=True, text=True, check=False)
    names_aemi = desc = refusal = None
    if res.returncode == 0:
        blob = img.read_bytes()
        names_aemi = struct.unpack_from(">HH", blob, 8)[1]
        desc = len(blob)
    else:
        refusal = res.stderr.strip().splitlines()[-1]
    ports = overlay["stream_ports"]
    return Built(dc, ports["input"], ports["output"], builder_names(dc),
                 names_aemi, desc, refusal, lifts)


def build_all(out: Path) -> tuple[dict, dict]:
    """Every page point, and every point the name rules are checked on."""
    built = {}
    for p in POINTS:
        cfg = (scaled_config(p.family, p.streams, out) if p.lifted
               else FAMILY_CONFIG[p.family])
        built[p.key] = build_point(cfg, out, p.lifted)
    rule = {}
    for family, counts in RULE_STREAMS.items():
        for n in counts:
            cfg = scaled_config(family, n, out)
            run_builder(cfg, out, False)
            overlay = json.loads((out / cfg.stem / "aem_overlay.json").read_text())
            rule[(family, n)] = builder_names(overlay["descriptor_counts"])
        cfg = scaled_config(family, REFUSED_STREAMS[family], out)
        res = subprocess.run([sys.executable, str(BUILDER), str(cfg), "-o", str(out)],
                             cwd=ROOT, capture_output=True, text=True, check=False)
        refused = re.search(r"has (\d+) writable names", res.stdout + res.stderr)
        rule[(family, "refused")] = int(refused.group(1)) if res.returncode and refused else None
    return built, rule


# ------------------------------------------------------- the lifted child ----

def lifted_build(cfg: Path, out: Path) -> None:
    """Run the builder with its three 32x32 limits lifted (the #859 method).

    Each limit is read first and reported, so the parent can refuse a run
    whose limit moved; the lifts touch this process's module object only.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location("endstation_builder", BUILDER)
    builder = importlib.util.module_from_spec(spec)
    sys.argv = [str(BUILDER), str(cfg), "-o", str(out)]
    spec.loader.exec_module(builder)
    capacity, where = builder.nvm_name_capacity()
    try:
        builder._streams([{"name": "probe", "channels": 8}] * 64, "probe", "listener")
        cap_text = ""
    except builder.ConfigError as err:
        cap_text = str(err)
    cap = re.search(r"max (\d+) per direction", cap_text)
    lifts = {"name_capacity": capacity, "name_capacity_at": where,
             "srp_ctx_idx_bits": builder.SRP_CTX_IDX_BITS,
             "stream_cap": int(cap.group(1)) if cap else None}
    print("LIFTS " + json.dumps(lifts), flush=True)
    if lifts["stream_cap"] is None:
        sys.exit("the builder's stream cap moved: this lift must be re-pointed")
    original = builder._streams
    chunk = lifts["stream_cap"]

    def streams_in_chunks(lst: list, ctx: str, direction: str, rate_hz: int = 48000) -> list:
        """The builder's own row parser, fed at most `chunk` rows at a time."""
        rows = []
        for k in range(0, len(lst), chunk):
            rows += original(lst[k:k + chunk], ctx, direction, rate_hz)
        return rows

    builder._streams = streams_in_chunks
    builder.SRP_CTX_IDX_BITS = 8
    builder.nvm_name_capacity = lambda: (1 << 16, "lifted in memory")
    builder.main()


# ---------------------------------------------------------- reading the tree --

def soc_literals() -> dict:
    """The flash map's literals out of milan_soc.py, read without LiteX."""
    tree = ast.parse(SOC.read_text())
    want = {"FLASH_SIZE", "FLASH_ERASE_BLOCK", "FLASHBOOT_LAYOUT", "FLASHBOOT_RESERVED"}
    found = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            name = getattr(node.targets[0], "id", None)
            if name in want:
                found[name] = ast.literal_eval(node.value)
    missing = want - set(found)
    if missing:
        raise RuntimeError(f"milan_soc.py no longer states {sorted(missing)}")
    return found


def backend_unit_bounds() -> tuple[int, int]:
    """KL_nvm_backend's RATE and CLOCK_SOURCE capacities (g_refuse_units)."""
    m = re.search(r"N_AUDIO_UNIT_P > (\d+) \|\| N_CLK_DOM_P < 1 \|\| N_CLK_DOM_P > (\d+)",
                  BACKEND.read_text())
    if not m:
        raise RuntimeError("KL_nvm_backend.sv: g_refuse_units moved")
    return int(m.group(1)), int(m.group(2))


def builder_window() -> tuple[int, int, int]:
    """The ppmem window, its response buffer and its NVM sub-window."""
    text = BUILDER.read_text()
    window = re.search(r"^PP_MEM_BYTES = (0x[0-9A-Fa-f_]+)", text, re.M)
    sub = re.search(r'"nvm_base": base \+ int\(cfg\["platform"\]\["pp_mem_bytes"\]\) '
                    r"- (0x[0-9A-Fa-f]+) - (0x[0-9A-Fa-f]+),", text)
    if not (window and sub):
        raise RuntimeError("endstation_builder.py: the ppmem window moved")
    return int(window.group(1), 16), int(sub.group(1), 16), int(sub.group(2), 16)


def measured_backend() -> dict:
    """The LUT-only rows of FASTCONNECT section 8.3, read, never restated."""
    rows = {}
    for line in FASTCONNECT.read_text().splitlines():
        m = re.match(r"\| `KL_nvm_backend`, `-nodsp` \| (\w+) \| [\d,]+ \| [\d,]+ \| "
                     r"\*\*([\d,]+)\*\* \| ([\d,]+) \|", line)
        if m:
            rows[m.group(1)] = (int(m.group(2).replace(",", "")),
                                int(m.group(3).replace(",", "")))
    if set(rows) != {"1x1", "8x8"}:
        raise RuntimeError("FASTCONNECT section 8.3: the -nodsp rows moved")
    return rows


# -------------------------------------------------------------- arithmetic ----

def align4(n: int) -> int:
    """KLJ2 pads the record area to a word."""
    return n + (-n) % contract.ALIGN


def point_figures(p: Point, b: Built, base: int) -> dict:
    """The record set and the bytes of one point, both framings."""
    shape = Shape(cfg=Path(p.label), names=b.names, dc=b.dc, spi=b.spi, spo=b.spo)
    recs = inventory(shape, base)
    plen = {"fixed": 0, "maps_in": 0, "maps_out": 0, "names": 0}
    cls = {"MAPS_IN": "maps_in", "MAPS_OUT": "maps_out", "NAME": "names"}
    for group, _i, _rid, pl, _blk in recs:
        plen[cls.get(group, "fixed")] += contract.REC_HDR + pl
    raw = sum(plen.values())
    n_rec = len(recs)
    raw_new = raw + n_rec * (PROPOSAL["rec_hdr_bytes"] - contract.REC_HDR)
    base_new = PROPOSAL["seg_hdr_bytes"] + align4(raw_new) + PROPOSAL["seg_trailer_bytes"]
    dc = b.dc
    f = {
        "streams": p.streams, "si": dc["STREAM_INPUT"], "so": dc["STREAM_OUTPUT"],
        "spi": dc["STREAM_PORT_INPUT"], "spo": dc["STREAM_PORT_OUTPUT"],
        "au": dc["AUDIO_UNIT"], "cd": dc["CLOCK_DOMAIN"], "clusters": dc["AUDIO_CLUSTER"],
        "cs": dc["CLOCK_SOURCE"], "descriptors": sum(int(v) for v in dc.values()),
        "names": b.names, "names_aemi": b.names_aemi, "desc_bytes": b.desc_bytes,
        "in_clusters": sorted({q["clusters"] for q in b.spi}),
        "out_clusters": sorted({q["clusters"] for q in b.spo}),
        "out_entries": sorted({output_map_entries(shape, q) for q in b.spo}),
        "records": n_rec, "fixed_bytes": plen["fixed"], "maps_in_bytes": plen["maps_in"],
        "maps_out_bytes": plen["maps_out"], "names_bytes": plen["names"], "raw_bytes": raw,
        "klj2_bytes": contract.KLJ2_HDR + align4(raw) + contract.KLJ2_TRAILER,
        "max_payload": max(r[3] for r in recs),
        "raw_new_bytes": raw_new, "base_bytes": base_new,
        "base_pages": math.ceil(base_new / contract.FLASH_PAGE),
    }
    f["klj2_pct"] = f["klj2_bytes"] * 100 / contract.FIXED.ERASE_BLOCK
    f["names_pct"] = plen["names"] * 100 / raw
    f["maps_out_pct"] = plen["maps_out"] * 100 / raw
    f["f1_stage_now"] = f["klj2_bytes"] + contract.REC_HDR
    f["f1_stage_new"] = contract.FLASH_PAGE + PROPOSAL["rec_hdr_bytes"] + f["max_payload"]
    f["commit_now_ms"] = whole_commit_ms(f["klj2_bytes"])
    return f


def whole_commit_ms(image: int) -> float:
    """Today's whole-image commit, FASTCONNECT section 9.4's formula."""
    pages = math.ceil(image / contract.FLASH_PAGE)
    return contract.T_SE_MAX_MS + pages * contract.T_PP_MAX_MS + image * 8 * 1000.0 / contract.SPI_HZ


def record_space(bound: dict, units: tuple[int, int]) -> dict:
    """The derived allocation: each block sized by the bound shape's count."""
    au_max, cd_max = units
    sizes = (("CFG_IDX", 1), ("SUID", 1), ("RATE", au_max), ("CLKSRC", cd_max),
             ("MCR", cd_max), ("BINDING", bound["si"]), ("FMT_IN", bound["si"]),
             ("FMT_OUT", bound["so"]), ("PT_OFS", bound["so"]), ("MAPS_IN", bound["spi"]),
             ("MAPS_OUT", bound["spo"]), ("NAME", bound["names"]))
    blocks, first = [], 0
    for group, size in sizes:
        blocks.append((group, first, first + size - 1, size))
        first += size
    return {"blocks": blocks, "total": first, "bits": (first - 1).bit_length(),
            "au_max": au_max, "cd_max": cd_max}


def save_path(figs: dict, flash: dict) -> dict:
    """Section 5: the append, the compaction, the erase and their bounds."""
    t_byte = 8 * 1000.0 / contract.SPI_HZ
    page = contract.FLASH_PAGE
    t_prog = contract.T_PP_MAX_MS + (PROPOSAL["wren_bytes"] + PROPOSAL["pp_cmd_bytes"] + page
                                     + PROPOSAL["rdsr_bytes"]) * t_byte
    t_read = (PROPOSAL["read_cmd_bytes"] + page) * t_byte
    t_page = t_prog + t_read
    seg_over = PROPOSAL["seg_hdr_bytes"] + PROPOSAL["seg_trailer_bytes"]
    p_cap = math.floor(PROPOSAL["w_fw_ms"] / t_page)
    cap_bytes = (p_cap * page - seg_over) // contract.ALIGN * contract.ALIGN
    t_seg = p_cap * t_page
    s = {"t_byte_ms": t_byte, "t_prog_ms": t_prog, "t_read_ms": t_read, "t_page_ms": t_page,
         "p_cap": p_cap, "cap_bytes": cap_bytes, "t_seg_ms": t_seg}
    s["fabric_ms"] = PROPOSAL["w_prod_ms"] + PROPOSAL["w_fw_ms"] + t_page + t_seg
    s["split_ms"] = PROPOSAL["w_fw_ms"] + t_page + t_seg
    s["susp_allow_ms"] = PROPOSAL["bound_ms"] - s["fabric_ms"]
    s["susp_typ_ms"] = PROPOSAL["susp_typ_us"] / 1000.0
    s["susp_margin"] = math.floor(s["susp_allow_ms"] / s["susp_typ_ms"])
    s["split_typ_ms"] = s["split_ms"] + s["susp_typ_ms"]
    s["fabric_typ_ms"] = s["fabric_ms"] + s["susp_typ_ms"]
    s["no_suspend_ms"] = PROPOSAL["w_prod_ms"] + PROPOSAL["w_fw_ms"] + contract.T_SE_MAX_MS + t_seg
    name_rec = PROPOSAL["rec_hdr_bytes"] + contract.NAME_BYTES
    s["name_rec"] = name_rec
    s["names_per_save"] = cap_bytes // name_rec
    s["one_name_pages"] = math.ceil((seg_over + align4(name_rec)) / page)
    s["one_name_ms"] = s["one_name_pages"] * t_page
    big = PROPOSAL["rec_hdr_bytes"] + figs[BOUND]["max_payload"]
    s["big_rec"] = big
    s["big_pages"] = math.ceil((seg_over + align4(big)) / page)
    s["big_ms"] = s["big_pages"] * t_page
    s["bigs_per_save"] = cap_bytes // big
    s["commit_min_ms"] = 2 * (t_page + t_seg)
    s["commit_now_ms"] = contract.FIXED.T_NVM_COMMIT_TIMEOUT_MS
    for key, f in figs.items():
        f["compact_ms"] = f["base_pages"] * t_page
    s.update(slot_layout(figs, flash, t_page, t_byte))
    return s


def slot_layout(figs: dict, flash: dict, t_page: float, t_byte: float) -> dict:
    """The slot, the log, the reserve and where the new journal goes."""
    block = flash["FLASH_ERASE_BLOCK"]
    page = contract.FLASH_PAGE
    base_pages = figs[BOUND]["base_pages"]
    sectors = math.ceil((1 + PROPOSAL["log_per_base"]) * base_pages * page / block)
    slot = sectors * block
    log_pages = slot // page - base_pages
    reserve = log_pages // PROPOSAL["reserve_fraction_den"]
    journal = 2 * slot
    old = flash["FLASHBOOT_RESERVED"]["journal"]
    start = old["offset"] - journal
    images_end = max(e["offset"] + e["size"] for e in flash["FLASHBOOT_LAYOUT"].values())
    t_erase = sectors * contract.T_SE_MAX_MS
    t_compact = figs[BOUND]["compact_ms"]
    rate = min(reserve / (t_compact / 1000.0), (log_pages - reserve) / (t_erase / 1000.0))
    return {"sectors": sectors, "slot_bytes": slot, "log_pages": log_pages, "reserve_pages": reserve,
            "journal_bytes": journal, "journal_start": start, "journal_end": old["offset"],
            "old_journal_bytes": old["size"], "images_end": images_end,
            "gap_bytes": start - images_end, "t_erase_ms": t_erase,
            "rate_pages_s": rate, "rate_bytes_s": rate * page,
            "boot_pass_ms": 2 * slot * t_byte, "boot_reads": 3,
            "slot_now_bytes": old["size"] // 2}


def window(figs: dict, flash: dict) -> dict:
    """The ppmem window at each point, today's sub-windows and the proposal's."""
    total, resp, sub_now = builder_window()
    block = flash["FLASH_ERASE_BLOCK"]
    sub_new = math.ceil(figs[BOUND]["base_bytes"] / block) * block
    w = {"window_bytes": total, "resp_bytes": resp, "sub_now": sub_now, "sub_new": sub_new,
         "fixed_new": resp + 2 * sub_new}
    w["desc_room"] = total - w["fixed_new"]
    for f in figs.values():
        f["window_new"] = None if f["desc_bytes"] is None else f["desc_bytes"] + w["fixed_new"]
    return w


def area(figs: dict, space: dict) -> dict:
    """Section 7's ESTIMATE: the ownership vector, its read mux and its depth."""
    est = AREA_EST
    a = {"measured": measured_backend()}
    for f in figs.values():
        bits = f["records"]
        words = math.ceil(bits / 32)
        f["open_ff"] = bits * est["ff_per_open_bit"]
        f["own_words"] = words
        f["open_lut"] = (bits * est["lut_per_open_bit"]
                         + 32 * math.ceil(words / est["mux_inputs_per_lut"]))
        f["or_levels"] = math.ceil(math.log(bits, 6))
        f["mux_levels"] = max(1, math.ceil(math.log(words, est["mux_inputs_per_lut"])))
    a["ram_open_lut"] = est["ram_open_lut"]
    a["id_space_words"] = math.ceil(space["total"] / 32)
    return a


def compute(out: Path) -> dict:
    """Every figure, keyed as the page's inline markers and blocks read them."""
    built, rule = build_all(out)
    base = binding_base()
    flash = soc_literals()
    figs = {p.key: point_figures(p, built[p.key], base) for p in POINTS}
    space = record_space(figs[BOUND], backend_unit_bounds())
    for f in figs.values():
        name_first = space["blocks"][-1][1]
        f["highest_id"] = name_first + f["names"] - 1
    save = save_path(figs, flash)
    win = window(figs, flash)
    est = area(figs, space)
    lifts = {p.key: built[p.key].lifts for p in POINTS if p.lifted}
    refusals = {p.key: built[p.key].aemi_refusal for p in POINTS}
    declared = [(b.group, b.base, b.last, b.cap) for b in nvm_layout3.read().blocks]
    return {"points": figs, "rule": rule, "space": space, "declared": declared, "save": save, "window": win,
            "area": est, "lifts": lifts, "refusals": refusals, "flash": flash,
            "base": base, "windows_now": windows_now(), "version": csr_version(),
            "max_payload_cap": contract.MAX_PAYLOAD,
            "datasheet": {"t_se_ms": contract.T_SE_MAX_MS, "t_pp_ms": contract.T_PP_MAX_MS,
                          "spi_hz": contract.SPI_HZ}}


def csr_version() -> int:
    """The gateware VERSION parameter the five simulations assert."""
    m = re.search(r"parameter logic \[31:0\] VERSION = 32'h([0-9A-Fa-f_]+)",
                  (ROOT / "hdl/common/csr/milan_csr.sv").read_text())
    if not m:
        raise RuntimeError("milan_csr.sv: the VERSION parameter moved")
    return int(m.group(1).replace("_", ""), 16)


def windows_now() -> dict:
    """D3 DR2a's first-dirty windows as the tree ships them."""
    from nvm_shape import WRITER_TIMING_MS
    found = set()
    for stem, pattern in (("KL_acmp_nvm_shadow", r"DEB_TICKS_P\s*=\s*(\d+)"),
                          ("KL_aecp_nvm_writer", r"DEB_MS_P\s*=\s*(\d+)")):
        m = re.search(pattern, tables.resolve("pp:" + stem).read_text())
        if not m:
            raise RuntimeError(f"{stem}: its first-dirty window moved")
        found.add(int(m.group(1)))
    if len(found) != 1:
        raise RuntimeError(f"the two producers' windows differ: {sorted(found)}")
    return {"producer": found.pop(), "firmware": WRITER_TIMING_MS["MILAN_NVM_DEBOUNCE_MS"]}


def figure_map(r: dict) -> dict[str, str]:
    """Every scalar figure, formatted as the page prints it."""
    return tables.figure_map(r, POINTS, PROPOSAL, AREA_EST)


def main() -> int:
    """Print every figure, or every block, or run one lifted build."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--blocks", action="store_true", help="print every generated block")
    ap.add_argument("--lifted-build", nargs=2, metavar=("CFG", "OUT"), help=argparse.SUPPRESS)
    args = ap.parse_args()
    if args.lifted_build:
        lifted_build(Path(args.lifted_build[0]), Path(args.lifted_build[1]))
        return 0
    with tempfile.TemporaryDirectory(prefix="nvm-format-") as tmp:
        r = compute(Path(tmp))
    if args.blocks:
        for name, text in tables.blocks(r, POINTS, PROPOSAL, AREA_EST).items():
            print(f"=== {name}\n{text}")
        return 0
    for key, value in figure_map(r).items():
        print(f"{key} = {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
