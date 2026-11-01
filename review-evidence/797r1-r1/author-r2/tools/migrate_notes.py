#!/usr/bin/env python3
"""One-off, run once on the round-1 descriptions: every carried note moves
verbatim to the static design record, in its written order, with the carried
statements the reviews found false corrected first. Tables and images stay on
the generated page. Usage: migrate_notes.py <repo> <round-1 json> <order json>"""
import json, re, sys
root, source, order_file = sys.argv[1:4]
sys.path.insert(0, root + "/scripts")
from register_page import anchor, relative, strip_md
RECORD = "docs/design/CSR_REGISTER_NOTES.md"
text = open(source, encoding="utf-8").read()
import os
LABELS = [
    ("silicon m001g", "silicon"), ("2026-07-23 mf51 silicon", "2026-07-23 silicon"), ("mf51 silicon", "silicon"),
    ("the lane-K engines", "the context engines"), ("#617 round 3", "#617"),
    ("match key `[31:0]` (dest MAC, MSB-first: byte0 in `[31:24]`? no - see note)", "match key `[31:0]` (destination MAC)"),
    ("WIRE, ProfiShark inline on the board link", "WIRE, an inline tap on the board link"),
    ("{02:00:00:00:00:02, uid", "{station MAC, uid"),
    ("a ProfiShark capture inline", "a capture inline"),
]
CARRIED = [
    ("Unused bits read 0; writes to `RO` fields are ignored;",
     "Reserved read-only bits read 0, and reserved R/W bits store what is written; writes to read-only fields are ignored;"),
    ("**Every one defaults to PRESENT**, so a shipping build's map is exactly what this page describes.",
     "**Every one defaults to PRESENT**, but a build may set them: the shipping AX7101 export sets `I2SPB_P` and `LPF_P` to 0."),
    ("`[8]`/`[3:0]` are ignored while set.", "it acts only while `[8]` is 0, and `[3:0]` still gates the window."),
    ("Only these bits are stored/read back.", "These bits are stored; a read returns `[8]` and `[3:0]` only."),
    (" -- the user's instruction was \\\"remove the old code AECP/ACMP/ADP the lwSRP shall be removed as well. Only use the uCPU code\\\" and \\\"do not leave the option, remove everything out of the code base that is legacy\\\"", ""),
]
groups = os.environ.get("FIX_GROUPS", "")
FIXES = (CARRIED if "carried" in groups else []) + (LABELS if "labels" in groups else [])
for old, new in FIXES:
    if old not in text and "silicon" not in old and "ProfiShark" not in old and "02:00" not in old:
        raise SystemExit(f"correction target is gone: {old}")
    text = text.replace(old, new)
d = json.loads(text)
ACCESS_LEGEND = "**Access:** `RO` read-only" if "carried" in groups else "\0"
order = json.load(open(order_file))


def rec_link(s):
    """Links in the record are relative to the design page; targets are spelled from the repository root."""
    def fix(m):
        t = m.group(1)
        return m.group(0) if t.startswith(("http", "#", "/")) else "](" + relative(t, RECORD) + ")"
    return re.sub(r"\]\(([^)\s]+)\)", fix, s)


def split(notes, lines, level):
    keep = []
    for item in notes:
        if isinstance(item, dict) and "heading" in item:
            sub = []
            kept = split(item.get("rows", []), sub, level + "#" if len(level) < 4 else level)
            intro = item.get("intro", [])
            lines += [f"{level} {rec_link(item['heading'])}", ""]
            for p in intro:
                lines += [rec_link(p), ""]
            lines += sub
            if kept:
                keep.append({"heading": item["heading"], "intro": [], "rows": kept})
        elif isinstance(item, dict):
            keep.append(item)
            lines += ["The table is on the [register reference](../reference/REGISTER_MAP.md).", ""]
        elif isinstance(item, list) and item and item[0] == "Code":
            lines += ["```text", item[1], "```", ""]
        elif isinstance(item, list):
            if item[0] != "Group summary":
                lines += [f"**{rec_link(item[0])}:** {rec_link(' '.join(item[1:]))}", ""]
        elif item.startswith("!["):
            keep.append(item)
        elif not item.startswith(ACCESS_LEGEND):
            lines += [rec_link(item), ""]
    return keep


seen = {}
final = []
lines = []
d["page"]["notes"] = split(d["page"].get("notes", []), lines, "###")
final.append("## Reading the register map\n\n" + "\n".join(lines).rstrip() + "\n")
d["page"]["record"] = anchor("Reading the register map", seen)
for h in re.findall(r"(?m)^#{3,6} (.+)$", final[-1]):
    anchor(h, seen)
by_mod = {}
for key, r in d["registers"].items():
    lines = []
    r["notes"] = split(r.get("notes", []), lines, "####")
    if lines:
        info = order[key]
        mod = next(m for m in d["modules"] if int(m["start"], 16) <= info["offset"] <= int(m["end"], 16))
        by_mod.setdefault(mod["key"], []).append((info["offset"], key, r, lines, info["acronym"]))
for m in d["modules"]:
    title = strip_md(m["heading"])
    lines = []
    m["notes"] = split(m.get("notes", []), lines, "###")
    subs = sorted(by_mod.get(m["key"], []), key=lambda x: x[0])
    if not lines and not subs:
        continue
    final.append(f"## {title}\n\n" + "\n".join(lines).rstrip() + "\n")
    m["record"] = anchor(title, seen)
    for h in re.findall(r"(?m)^#{3,6} (.+)$", "\n".join(lines)):
        anchor(h, seen)
    for off, key, r, reg_lines, acr in subs:
        head = f"{acr} (offset 0x{off:03X})"
        final.append(f"### {head}\n\n" + "\n".join(reg_lines).rstrip() + "\n")
        r["record"] = anchor(head, seen)
        for h in re.findall(r"(?m)^#{3,6} (.+)$", "\n".join(reg_lines)):
            anchor(h, seen)
lines = []
d["soc_notes"] = split(d.get("soc_notes", []), lines, "###")
if lines:
    final.append("## SoC CSR banks\n\n" + "\n".join(lines).rstrip() + "\n")
    d["soc_record"] = anchor("SoC CSR banks", seen)
HEADER = """# CSR register design notes

The [register reference](../reference/REGISTER_MAP.md) states what each register does today.

This page keeps the rationale, dated findings and version history behind it.

The prose comes from the hand-written register map, kept as written where it is still true.

The reference and the RTL win over this page.

This page is a record: it is not generated, and the concise-prose gate does not read it.

"""
open(root + "/" + RECORD, "w", encoding="utf-8").write(HEADER + "\n".join(final))
# structural keys the generator now reads
d["_comment"] = ("Prose for the generated register reference (#797), keyed by RTL register and field name. The generator "
                 "refuses a key the RTL lacks. Regenerate the page after any edit. Rationale and history live in "
                 "docs/design/CSR_REGISTER_NOTES.md; `record` keys are its anchors.")
d["literal_words"] = {"0x86C": "STRMW_RSVD_86C"}
d["condition_words"] = {
    "win_in_range_w": ["the selected stream exists", "the selected stream does not exist"],
    "acmp_fresh_r": ["the ACMP table answered since the last selection", "the ACMP table has not answered since the last selection"],
    "srp_fresh_r": ["the SRP table answered since the last selection", "the SRP table has not answered since the last selection"],
    "stg_hit_w": ["the staged identity belongs to the selected stream", "the staged identity belongs to another stream"],
    "srp_idx0_ls_w": ["`STRM_SEL[9]` selects the listener row at index 0", "`STRM_SEL[9]` does not select the listener row at index 0"],
    "snap_kind_r": "the kind the last snapshot recorded for this counter",
    "snap_busy_r": ["a snapshot is running", "no snapshot is running"],
    "strm_idx_r": "the stream index `STRM_SEL[3:0]`",
    "strm_dir_r": ["`STRM_SEL[8]` selects a talker", "`STRM_SEL[8]` selects a listener"],
    "cmrd_valid_r": ["a channel-map readback has completed", "no channel-map readback has completed"],
}
R = d["registers"]
R["STRMW_RSVD_86C"] = {"name": "Stream window hole", "purpose": "An undefined word of the stream window.", "fields": {}, "notes": []}
cap = R["CAP"]["fields"]
R["CAP"]["rename"] = {"BIT8": "CBS", "BIT9": "PTP", "BIT10": "STATS", "BIT11": "RX_FILTER", "BIT12": "ADP", "BIT13": "TCAM",
                      "BIT14": "LWSRP", "BIT15": "CAP_15", "BITS23_16": "TS_WIDTH"}
R["CAP"]["fields"] = {"NUM_QUEUES": cap["NUM_QUEUES"], "CBS": cap["BIT8"], "PTP": "PTP clock present.", "STATS": "Statistics block present.",
                      "RX_FILTER": "Receive filter present.", "ADP": "ADP present.", "TCAM": "Address filter TCAM present.",
                      "LWSRP": "lwSRP control registers present.", "CAP_15": "Reads 0.", "TS_WIDTH": "Timestamp width in bits."}
R["RENDER_STAT"]["fields"] = {"RENDER_STATUS": R["RENDER_STAT"]["fields"]["RENDER_STAT"]}
R["CHMAP_LOOP"]["rename"] = {"CMRD_SIDE_27": "MASK_VALID", "CHMAP_LOOP": "VALID", "BIT18": "LOOP_SUSPECT", "CMRD_DATA_17_16": "LOOP_FLAGS",
                             "CMRD_DATA_15_0": "RAW", "CMRD_SIDE_19": "SIDE"}
R["STRMW_BIND"]["fields"] = {"ACMP_FLAGS_Q": "**Structural zero.** Was the flags half of the ACMP bind context.",
                             "ACMP_TUID_Q": "**Structural zero.** Was the talker unique ID half of the ACMP bind context."}
R["STRMW_SRP"]["fields"] = {"STRMW_SRP": "Index 0, unless `STRM_SEL[9]` selects the listener row: the live `LWSRP_STATUS` word. "
                            "Other rows are the attribute-row port, which is never granted, so they read 0."}
R["I2SPB_STAT"]["rename"] = {"I2SPB_STAT_31_16": "UNDERRUN", "I2SPB_STAT_15_0": "OVERRUN"}
json.dump(d, open(root + "/scripts/register_descriptions.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
open(root + "/scripts/register_descriptions.json", "a", encoding="utf-8").write("\n")
