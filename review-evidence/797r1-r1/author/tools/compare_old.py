#!/usr/bin/env python3
"""Compare the old page's Acc and Reset columns with the RTL-derived values."""
import json
import re
import sys
from pathlib import Path

lane = Path(sys.argv[1])
sys.path.insert(0, str(lane / "scripts"))
import gen_register_reference as g  # noqa: E402

model, facts = g.build_model(lane)
old = json.loads(Path(sys.argv[2]).read_text())
regs = {r.label: r for r in model.registers}


def old_reset(text):
    t = text.strip("` ").replace("_", "")
    if re.fullmatch(r"0x[0-9A-Fa-f]+", t):
        return int(t, 16)
    if re.fullmatch(r"\d+", t):
        return int(t)
    return None


def gen_access(reg):
    acc = {f.access for f in reg.fields if f.name != "RESERVED"} or {"R"}
    return acc


rows = []
for label, items in old.items():
    reg = regs[label]
    for item in items:
        if item["line"] >= 2500:      # the memory-bridge table, not this block
            continue
        o_acc = item["acc"].strip()
        o_rst = old_reset(item["reset"]) if item["reset"] else None
        g_acc = gen_access(reg)
        verdict = []
        if o_rst is not None and "X" not in reg.reset and reg.count == 1:
            if o_rst != int(reg.reset, 16):
                verdict.append(f"reset {item['reset']} vs RTL {reg.reset}")
        a = o_acc.upper().replace(" ", "")
        if a.startswith("RO") and any("W" in x for x in g_acc):
            verdict.append(f"access {o_acc} vs RTL {sorted(g_acc)}")
        if a.startswith("RW") and not any("W" in x for x in g_acc):
            verdict.append(f"access {o_acc} vs RTL {sorted(g_acc)}")
        rows.append((item["offset"], item["name"], o_acc, item["reset"], reg.reset, sorted(g_acc), verdict,
                     item["line"]))
bad = [r for r in rows if r[6]]
print(f"compared {len(rows)} old rows; {len(bad)} disagree")
for r in bad:
    print(f"{r[0]} {r[1]} old line {r[7]}: {'; '.join(r[6])}")
