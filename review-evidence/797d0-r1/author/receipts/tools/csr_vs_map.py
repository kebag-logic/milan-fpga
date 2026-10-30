"""List CSR address constants in milan_csr.sv and whether REGISTER_MAP.md has a table row for each."""
import re, sys
from pathlib import Path
root = Path(sys.argv[1])
rtl = (root / "hdl/common/csr/milan_csr.sv").read_text()
doc = (root / "docs/reference/REGISTER_MAP.md").read_text().split("\n")
consts = {}
for m in re.finditer(r"\b(A_[A-Z0-9_]+)\s*=\s*'h([0-9A-Fa-f]+)", rtl):
    consts.setdefault(m.group(1), int(m.group(2), 16))
rows = {}
for n, line in enumerate(doc, 1):
    if not line.startswith("|"):
        continue
    for m in re.finditer(r"0x([0-9A-Fa-f]{3,4})\b", line.split("|")[1] if line.count("|") > 2 else line):
        rows.setdefault(int(m.group(1), 16), n)
mentions = {}
for n, line in enumerate(doc, 1):
    for m in re.finditer(r"0x([0-9A-Fa-f]{3,4})\b", line):
        mentions.setdefault(int(m.group(1), 16), n)
for name, addr in sorted(consts.items(), key=lambda x: x[1]):
    first = rows.get(addr)
    print(f"0x{addr:03X} {name:22s} row={first if first else '-':>5} mention={mentions.get(addr, '-')}")
