#!/usr/bin/env python3
"""Compare every REGISTER_MAP row's address, name, access and reset with milan_csr.sv.

Usage: python3 -I regmap_access.py <tree>

From the RTL: `A_NAME = 'hADDR` constants; the names decoded by the two write
case statements (`register_write`, `pp_regs`) are the writable set; the
`csr_default` literals are the reset words. From the map: every table row
`| 0xADDR | NAME | ACCESS | RESET | ...`. A row is flagged when its address is
not the constant's, when ACCESS says read-only (no W in it) but the name is
write-decoded, when ACCESS says writable but the name is never write-decoded,
or when its reset literal differs from a csr_default literal. A flag is a
candidate for the manual pass.
"""
import re
import sys
from pathlib import Path

tree = Path(sys.argv[1])
rtl = (tree / "hdl/common/csr/milan_csr.sv").read_text().split("\n")
addr = {}
for line in rtl:
    for m in re.finditer(r"\bA_([A-Z0-9_]+)\s*=\s*'h([0-9A-Fa-f_]+)", line):
        addr.setdefault(m.group(1), int(m.group(2).replace("_", ""), 16))
text = "\n".join(rtl)


def case_names(start_pat: str) -> set[str]:
    """Names in the `unique case (wr_addr)` after the named block's opening line, to its endcase."""
    names = set()
    for i, line in enumerate(rtl):
        if re.search(start_pat, line):
            depth = 0
            for j in range(i, len(rtl)):
                if "unique case (wr_addr)" in rtl[j]:
                    depth = 1
                    continue
                if depth and re.match(r"^\s*endcase\b", rtl[j]) and rtl[j].startswith(" " * 8) and depth == 1:
                    if re.match(r"^\s{8}endcase|^\s{10}endcase", rtl[j]):
                        return names
                if depth:
                    m = re.match(r"^\s*((?:A_[A-Z0-9_]+(?:\[[^\]]*\])?\s*,\s*)*A_[A-Z0-9_]+(?:\[[^\]]*\])?)\s*:", rtl[j])
                    if m:
                        names |= set(re.findall(r"A_([A-Z0-9_]+)", m.group(1)))
    return names


writable = case_names(r"begin : register_write") | case_names(r"begin : pp_regs")
# Plain-RW registers are written through the shadow: the names `is_plain_rw` lists (comments excluded).
start = next(i for i, l in enumerate(rtl) if "function automatic logic is_plain_rw" in l)
for line in rtl[start:start + 60]:
    if "endfunction" in line:
        break
    writable |= set(re.findall(r"A_([A-Z0-9_]+)", line.split("//")[0]))
# Indexed windows: an address inside [X_BASE, X_END), or STAT0..8 at stride 4 from A_STATS_BASE.
windows = [(addr[k], addr[k[:-5] + "_END"]) for k in addr if k.endswith("_BASE") and k[:-5] + "_END" in addr]
windows.append((addr.get("STATS_BASE", 0x210), addr.get("STATS_BASE", 0x210) + 9 * 4))
resets = {m.group(1): int(m.group(2).replace("_", ""), 16)
          for m in re.finditer(r"\bA_([A-Z0-9_]+)\[10:0\]:\s*csr_default\s*=\s*32'h([0-9A-Fa-f_]+)", text)}
rows = flags = 0
for n, line in enumerate((tree / "docs/reference/REGISTER_MAP.md").read_text().split("\n"), 1):
    m = re.match(r"^\|\s*`0x([0-9A-Fa-f]{3})`[^|]*\|\s*`([A-Z][A-Z0-9_]*)`\s*\|\s*([^|]*)\|\s*([^|]*)\|", line)
    if not m:
        continue
    a, name, access, reset = int(m.group(1), 16), m.group(2), m.group(3).strip(), m.group(4).strip()
    rows += 1
    notes = []
    at = sorted(k for k, v in addr.items() if v == a)
    if name in addr and addr[name] != a:
        notes.append(f"address 0x{a:03X} but RTL A_{name} = 0x{addr[name]:03X}")
    if not at and not any(lo <= a < hi for lo, hi in windows):
        notes.append("no RTL constant or window at this address")
    says_w = bool(re.search(r"\bW|RW|W1|wo\b", access))
    if at:
        if not says_w and any(k in writable for k in at):
            notes.append(f"access '{access}' but {at} is write-decoded")
        if says_w and not any(k in writable for k in at) and not re.search(r"inert|ignored|scratch|RO", access):
            notes.append(f"access '{access}' but {at} is never write-decoded")
    lit = re.search(r"0x([0-9A-Fa-f_]+)", reset)
    for k in at:
        if lit and k in resets and int(lit.group(1).replace("_", ""), 16) != resets[k]:
            notes.append(f"reset {reset} but csr_default of A_{k} 0x{resets[k]:08X}")
    if notes:
        flags += 1
        print(f"{n}\t0x{a:03X}\t{name}\t{access}\t" + "; ".join(notes))
print(f"{rows} rows, {flags} flagged; {len(writable)} write-decoded names, {len(resets)} reset literals")
