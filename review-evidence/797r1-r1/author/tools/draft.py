#!/usr/bin/env python3
"""One-off drafting aid (not committed): carry every row, paragraph, list item
and table of the hand-written REGISTER_MAP.md into a draft descriptions file,
attached to the register (by offset), the module (by section) or the page."""
import json
import re
import sys
from pathlib import Path

LANE = Path(sys.argv[1])
OLD = Path(sys.argv[2])
OUT = Path(sys.argv[3])
sys.path.insert(0, str(LANE / "scripts"))
import gen_register_reference as g  # noqa: E402

model, facts = g.build_model.__wrapped__(LANE) if hasattr(g.build_model, "__wrapped__") else (None, None)
from register_fields import Deriver  # noqa: E402
from register_rtl import csr_parameters, load_rtl  # noqa: E402

soc = json.loads((LANE / "scripts/register_map_soc.json").read_text())
ov, _ = csr_parameters(LANE, soc)
facts = load_rtl(LANE, soc["shape"], ov)
regs = Deriver(facts).all_registers()
by_off = {}
for r in regs:
    for n in range(r.count):
        by_off.setdefault(r.offset + n * r.stride, r)

MODULES = [
    ("ident", "0x000  -  Identification / IRQ", 0x000, 0x0FF),
    ("mac", "0x100  -  MAC control / status  `(REQ-MAC-01..03)`", 0x100, 0x1FF),
    ("stats", "0x200  -  Statistics (RMON)  `(REQ-MAC-04)`", 0x200, 0x2FF),
    ("cls", "0x300  -  802.1Q classifier  `(REQ-CLS-01..04)`", 0x300, 0x3FF),
    ("cbs", "0x400  -  802.1Qav CBS (per queue)  `(REQ-CBS-01..03)`", 0x400, 0x4FF),
    ("ptp", "0x500  -  PTP hardware clock  `(REQ-PTP-01..04, 06)`", 0x500, 0x5FF),
    ("adp", "0x600  -  ADP advertiser  `(IEEE 1722.1-2021 / Milan v1.2, FR-DISC-01..04)`", 0x600, 0x647),
    ("aecp", "0x648  -  AECP/ACMP status + AAF talker  `(IEEE 1722.1 / Milan v1.2)`", 0x648, 0x67F),
    ("lwsrp", "0x680  -  lwSRP engine  `(802.1Q MSRP/MVRP, Milan v1.2 Section 5.6, FR-SRP-*)`", 0x680, 0x6A3),
    ("acmpl", "0x6A4  -  ACMP listener SM  `(Milan v1.2 Section 5.5 listener, FR-CONN-01)`", 0x6A4, 0x6FF),
    ("tcam", "0x700  -  RX destination-MAC TCAM filter  `(REQ-MAC-02)`", 0x700, 0x71B),
    ("link", "0x71C  -  Link guard / MAC recovery (VERSION minor ≥ 0x0006)", 0x71C, 0x723),
    ("overlay", "0x724  -  identity / playback / 802.1AS overlay", 0x724, 0x737),
    ("crf", "0x738  -  CRF media-clock sink  `(Milan v1.2 7.3, KL_crf_rx)`", 0x738, 0x74F),
    ("crft", "0x750  -  CRF media-clock talker  `(Milan v1.2 7.3.1, KL_crf_tx)`", 0x750, 0x767),
    ("bdbg", "0x768  -  AECP GET_DYNAMIC_INFO scan forensics (BDBG) -- 🔴 STRUCTURAL ZERO, and the link-guard status", 0x768, 0x777),
    ("clkv", "0x778  -  Clock validity: the AVTP `tu` verdict `(VERSION minor >= 0x0016)`, TX arbiter and SRP domain", 0x778, 0x79F),
    ("rest", "0x7A0  -  ACMP bind-restore  `(saved-state fast-connect E1, Milan 5.5.3.5.2)`", 0x7A0, 0x7B7),
    ("jnl", "0x7B8  -  Persistence-journal ingest  `(saved-state fast-connect E3)`", 0x7B8, 0x7C7),
    ("aemp", "0x7C8  -  AEM dynamic-state patch port  `(saved-state fast-connect E4)`", 0x7C8, 0x7D7),
    ("guard", "0x7D8  -  Ethernet guard", 0x7D8, 0x7DB),
    ("asp", "0x7DC  -  retired AS_PATH compatibility addresses", 0x7DC, 0x7E7),
    ("gptpd", "0x7E8  -  gPTP plane drop diagnostics", 0x7E8, 0x7EF),
    ("gptpl", "0x7F0  -  applied gPTP timestamp latency corrections", 0x7F0, 0x7FF),
    ("strm", "0x800  -  Indexed per-stream window", 0x800, 0x86F),
    ("ltap", "0x870  -  AAF per-stage latency taps  `(roadmap item-11, KL_aaf_latency_taps)`", 0x870, 0x8B3),
    ("aprb", "0x8B4  -  RX stream-parser probe  `(APRB, avtp_stream_parser + milan_datapath)`", 0x8B4, 0x8C7),
    ("gap", "0x8C8  -  reserved target-media compatibility words", 0x8C8, 0x8D3),
    ("slip", "0x8D4  -  media-boundary slip counters  `(SLIP, KL_chan_map_capture)`", 0x8D4, 0x8DB),
    ("render", "0x8DC  -  render presentation state", 0x8DC, 0x8DF),
    ("aafm", "0x8E0  -  AAF clock meter  `(#629, KL_aaf_clock_meter)`", 0x8E0, 0x8F7),
    ("mcsrv", "0x8F8  -  MMCM-DRP media-clock servo  `(Milan v1.2 7.3.4, KL_mmcm_drp_servo)`", 0x8F8, 0x8FF),
    ("chmap", "0x900  -  channel-map fabric  `([Section 6 of docs/CHANNEL_MAP_64.md](../CHANNEL_MAP_64.md#6-csr-window-0x900-0x97f-debug-and-override), KL_chan_map_render / KL_chan_map_capture)`", 0x900, 0x91F),
    ("pp", "0x920  -  protocol-processor control plane  `(KL_pp_shadow, VERSION major 2)`", 0x920, 0x93F),
]


def module_of(off):
    for key, _h, a, b in MODULES:
        if a <= off <= b:
            return key
    return None


def clean(text):
    text = text.replace("—", "--")
    return " ".join(text.split())


lines = OLD.read_text().splitlines()
page_notes = []          # groups
module_notes = {k: [] for k, *_ in MODULES}
reg_notes = {}
soc_notes = []
old_rows = {}            # label -> list of (name, acc, reset, desc, line)
skip_section = False
current = ("page", None)   # (scope, module key)
group = None               # current note group dict


def new_group(scope, key, heading):
    grp = {"heading": heading, "rows": []}
    if scope == "page":
        page_notes.append(grp)
    elif scope == "soc":
        soc_notes.append(grp)
    else:
        module_notes[key].append(grp)
    return grp


def target_rows():
    """Where a plain row goes: the current group, else the module/page list."""
    if group is not None:
        return group["rows"]
    scope, key = current
    if scope == "module":
        return module_notes[key]
    if scope == "soc":
        return soc_notes
    return page_notes


i = 0
para = []
in_fence = False
fence_buf = []
in_comment = False


def flush_para(lineno):
    global para
    if para:
        target_rows().append(clean(" ".join(para)))
        para = []


table = None
last_head = None
current_skip = None
group_rows = {}
while i < len(lines):
    ln = lines[i]
    lineno = i + 1
    s = ln.strip()
    if in_comment:
        if "-->" in s:
            in_comment = False
        i += 1
        continue
    if s.startswith("<!--"):
        flush_para(lineno)
        if "-->" not in s:
            in_comment = True
        i += 1
        continue
    if s.startswith("```"):
        flush_para(lineno)
        if in_fence:
            target_rows().append(["Code", "\n".join(fence_buf)])
            fence_buf = []
        in_fence = not in_fence
        i += 1
        continue
    if in_fence:
        fence_buf.append(ln)
        i += 1
        continue
    hm = re.match(r"^(#{1,6}) (.+)$", ln)
    if hm:
        flush_para(lineno)
        level, text = len(hm.group(1)), hm.group(2).strip()
        skip_section = text in ("Contents", "Register groups")
        current_skip = text
        last_head = None
        om = re.match(r"0x([0-9A-Fa-f]{3})\b", text)
        if level == 1:
            current, group = ("page", None), None
        elif text.startswith("Protocol-processor memory bridges"):
            current = ("soc", None)
            group = new_group("soc", None, text)
        elif level <= 3 and om:
            key = module_of(int(om.group(1), 16))
            current, group = ("module", key), None
        elif text.startswith("Link guard / MAC recovery"):
            current, group = ("module", "link"), None
        elif level == 2 or (level == 3 and current[0] == "page"):
            current = ("page", None)
            group = None if skip_section else new_group("page", None, text)
        else:
            scope, key = current
            group = new_group(scope, key, text)
        i += 1
        continue
    if skip_section:
        gm = re.match(r"^\|\s*`0x([0-9A-Fa-f]{3})`\s*\|\s*(.+?)\s*\|\s*$", ln)
        if gm and current_skip == "Register groups":
            key = module_of(int(gm.group(1), 16))
            group_rows.setdefault(key, []).append(clean(gm.group(2)))
        i += 1
        continue
    if s.startswith("|"):
        flush_para(lineno)
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", s.strip().strip("|"))]
        if re.fullmatch(r"[-: |]+", s):
            i += 1
            continue
        om = re.fullmatch(r"`(\+)?0x([0-9A-Fa-f]{2,3})`(?:\s*-\s*`0x[0-9A-Fa-f]{3}`)?", cells[0])
        if table is None:
            if om and last_head is not None:
                table = {"head": last_head, "rows": [], "line": lineno}
            else:
                table = {"head": cells, "rows": [], "line": lineno}
                if cells[0] == "Offset" and cells[1] in ("Name", "Register"):
                    last_head = cells
                i += 1
                continue
        head = table["head"]
        if om and head[0] == "Offset" and head[1] in ("Name", "Register"):
            off = int(om.group(2), 16) + (0x400 if om.group(1) else 0)
            reg = by_off.get(off)
            if reg is not None:
                col = {{"Access": "Acc", "Fields": "Description"}.get(h, h): k for k, h in enumerate(head)}
                acc = cells[col["Acc"]] if "Acc" in col and col["Acc"] < len(cells) else ""
                rst = cells[col["Reset"]] if "Reset" in col and col["Reset"] < len(cells) else ""
                d0 = col.get("Description", len(head) - 1)
                old_rows.setdefault(reg.label, []).append(
                    {"name": cells[1], "acc": acc, "reset": rst, "desc": clean(" | ".join(cells[d0:])),
                     "line": lineno, "offset": f"0x{off:03X}"})
                i += 1
                if i >= len(lines) or not lines[i].strip().startswith("|"):
                    if table["rows"]:
                        target_rows().append({"table": [table["head"]] + table["rows"], "line": table["line"]})
                    table = None
                continue
        table["rows"].append(cells)
        i += 1
        if i >= len(lines) or not lines[i].strip().startswith("|"):
            if table["rows"]:
                target_rows().append({"table": [table["head"]] + table["rows"], "line": table["line"]})
            table = None
        continue
    if table is not None:
        if table["rows"]:
            target_rows().append({"table": [table["head"]] + table["rows"], "line": table["line"]})
        table = None
    if not s:
        flush_para(lineno)
        i += 1
        continue
    if re.match(r"^\s*([-*+]|\d+\.)\s+", ln):
        flush_para(lineno)
        para = [re.sub(r"^\s*([-*+]|\d+\.)\s+", "", ln)]
        i += 1
        while i < len(lines) and lines[i].startswith("  ") and lines[i].strip() \
                and not re.match(r"^\s*([-*+]|\d+\.)\s+", lines[i]):
            para.append(lines[i].strip())
            i += 1
        flush_para(lineno)
        continue
    para.append(re.sub(r"^(?:>\s?)+", "", s))
    i += 1
flush_para(len(lines))

registers = {}
for reg in regs:
    rows = old_rows.get(reg.label, [])
    entry = {"acronym": rows[0]["name"].strip("`") if rows else reg.label, "name": "", "purpose": "",
             "fields": {}, "notes": []}
    for r in rows:
        entry["notes"].append(r["desc"])
    registers[reg.label] = entry
for key, texts in group_rows.items():
    module_notes[key][:0] = [["Group summary", t] for t in texts]
draft = {
    "page": {"intro": [], "notes": page_notes},
    "modules": [{"key": k, "heading": h, "start": f"0x{a:03X}", "end": f"0x{b:03X}", "purpose": "",
                 "notes": module_notes[k]} for k, h, a, b in MODULES],
    "registers": registers,
    "soc_notes": soc_notes,
}
OUT.write_text(json.dumps(draft, indent=2, ensure_ascii=False) + "\n")
json.dump(old_rows, open(str(OUT) + ".oldrows.json", "w"), indent=2, ensure_ascii=False)
print("registers with old rows:", sum(1 for r in regs if r.label in old_rows), "of", len(regs))
print("missing old rows:", [r.label for r in regs if r.label not in old_rows])
print("page groups", len(page_notes), "soc groups", len(soc_notes))


# ---- second pass: split each old row's `[h:l]` segments onto the generated fields
SEG = re.compile(r"`\[(\d+)(?::(\d+))?\]`")
data = json.loads(OUT.read_text())
moved = kept = 0
for reg in regs:
    entry = data["registers"][reg.label]
    new_notes = []
    for note in entry["notes"]:
        marks = list(SEG.finditer(note))
        if not marks:
            if len(reg.fields) == 1 and not entry["fields"]:
                entry["fields"][reg.fields[0].name] = note
                moved += 1
            else:
                new_notes.append(note)
                kept += 1
            continue
        clean_split = not note[:marks[0].start()].strip()
        plan = {}
        for k, m in enumerate(marks):
            hi = int(m.group(1))
            lo = int(m.group(2)) if m.group(2) else hi
            end = marks[k + 1].start() if k + 1 < len(marks) else len(note)
            text = note[m.end():end].strip().strip(",;").strip()
            hit = [f for f in reg.fields if (f.hi, f.lo) == (max(hi, lo), min(hi, lo))]
            if not hit or hit[0].name == "RESERVED" or hit[0].name in plan or hit[0].name in entry["fields"] or not text \
                    or SEG.search(text) or "`[" in text:
                clean_split = False
                break
            plan[hit[0].name] = text
        if clean_split:
            entry["fields"].update(plan)
            moved += len(plan)
        else:
            new_notes.append(note)
            kept += 1
    entry["notes"] = new_notes
OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
print("segments moved to fields:", moved, "notes kept:", kept)
