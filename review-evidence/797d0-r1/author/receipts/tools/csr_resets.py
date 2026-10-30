"""Compare REGISTER_MAP.md literal reset values with milan_csr.sv csr_default literals."""
import re, sys
from pathlib import Path
root = Path(sys.argv[1])
rtl = (root / "hdl/common/csr/milan_csr.sv").read_text()
consts = {}
for m in re.finditer(r"\b(A_[A-Z0-9_]+)\s*=\s*'h([0-9A-Fa-f]+)", rtl):
    consts.setdefault(m.group(1), int(m.group(2), 16))
body = rtl[rtl.index("function automatic [31:0] csr_default"):]
body = body[:body.index("endfunction")]
defaults = {}
for m in re.finditer(r"(A_[A-Z0-9_]+)\[10:0\]:\s*csr_default\s*=\s*([^;]+);", body):
    defaults[consts[m.group(1)]] = (m.group(1), m.group(2).strip())
doc = (root / "docs/reference/REGISTER_MAP.md").read_text().split("\n")
for n, line in enumerate(doc, 1):
    cells = [c.strip() for c in line.split("|")]
    if len(cells) < 6 or not re.fullmatch(r"`0x[0-9A-Fa-f]{3}`", cells[1] or ""):
        continue
    addr = int(cells[1].strip("`"), 16)
    reset = cells[4]
    rtl_def = defaults.get(addr)
    lit = re.fullmatch(r"`?0x([0-9A-Fa-f_]+)`?|`?(0)`?", reset)
    doc_val = int((lit.group(1) or lit.group(2)).replace("_", ""), 16) if lit else None
    if rtl_def:
        rv = rtl_def[1]
        m = re.fullmatch(r"32'h([0-9A-Fa-f_]+)|32'd(\d+)", rv)
        rtl_val = int(m.group(1).replace("_", ""), 16) if m and m.group(1) else (int(m.group(2)) if m else None)
        if rtl_val is not None and doc_val is not None and rtl_val != doc_val:
            print(f"MISMATCH line {n}: 0x{addr:03X} {cells[2]} doc={reset} rtl={rv}")
        elif rtl_val is None:
            print(f"DERIVED  line {n}: 0x{addr:03X} {cells[2]} doc={reset} rtl={rv}")
    elif doc_val not in (None, 0):
        print(f"NODEFAULT line {n}: 0x{addr:03X} {cells[2]} doc={reset} (no csr_default literal: live or flop)")
