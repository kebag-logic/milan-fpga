#!/usr/bin/env python3
"""Show what --write publishes after a write arm the parser cannot read, in a scratch copy.
Usage: write_probe.py <repo-root> <scratch>"""
import re, sys, tempfile
from pathlib import Path
root, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.dont_write_bytecode = True
sys.path.insert(0, str(root / "scripts"))
from register_selftest import copy_inputs
from gen_register_reference import main
CASES = [("masked store on CHMAP_SEL", "A_CHMAP_SEL:  chmap_sel  <= s_axi_wdata;", "A_CHMAP_SEL:  chmap_sel  <= s_axi_wdata & 32'h1FF;", "CHMAP_SEL"),
         ("slice store on MCSRV_CTRL", "A_MCSRV_CTRL: mcsrv_ctrl <= s_axi_wdata;", "A_MCSRV_CTRL: mcsrv_ctrl[1:0] <= s_axi_wdata[1:0];", "MCSRV_CTRL")]
for name, old, new, reg in CASES:
    with tempfile.TemporaryDirectory(dir=scratch, prefix="wp-") as tmp:
        r = Path(tmp); copy_inputs(r)
        p = r / "hdl/common/csr/milan_csr.sv"; t = p.read_text(encoding="utf-8"); assert old in t
        p.write_text(t.replace(old, new), encoding="utf-8")
        rc = main(["--write"], root=r)
        page = (r / "docs/reference/REGISTER_MAP.md").read_text(encoding="utf-8")
        m = re.search(rf"^### {reg} register.*?(?=^### )", page, re.M | re.S)
        rows = re.findall(r"^\| \d+.*$", m.group(0), re.M)
        print(f"--- {name}: --write rc={rc}, page says the RTL write arm stores nothing:")
        for row in rows:
            print("   ", row[:90])
