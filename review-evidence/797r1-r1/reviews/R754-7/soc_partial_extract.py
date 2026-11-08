#!/usr/bin/env python3
"""Compare a committed register_map_soc.json with the csr.csv / aem_desc.json parts
of a builder export (the gateware-parameter part needs the export's gateware/,
which is not published, so it is reported as not compared).
Usage: python3 -I soc_partial_extract.py <tree> <export-dir-with-csr.csv-and-aem_desc.json>"""
import json, sys, types, importlib.util, tempfile, shutil
from pathlib import Path
tree, export = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree / "scripts"))
import register_rtl as rr
with tempfile.TemporaryDirectory() as tmp:
    d = Path(tmp)
    for f in ("csr.csv", "aem_desc.json"):
        shutil.copy(export / f, d / f)
    (d / "gateware").mkdir()
    try:
        got = rr.extract_soc(d)
    except rr.Refusal as exc:
        got = None
        print("extract refused without gateware (expected):", exc)
committed = json.loads((tree / "scripts/register_map_soc.json").read_text())
# Re-run the csv/aem half by hand, mirroring extract_soc up to the gateware block.
import hashlib, re
lines = (export / "csr.csv").read_text(encoding="utf-8").splitlines()
body = [ln for ln in lines if ln and not ln.startswith("#")]
consts, regs, banks, mems = {}, [], [], []
for ln in body:
    c = ln.split(",")
    if c[0] == "constant" and (c[1].startswith(("milan_", "spiflash_")) or c[1] in ("config_clock_frequency", "config_platform_name")):
        consts[c[1]] = int(c[2]) if re.fullmatch(r"-?\d+", c[2]) else c[2]
    elif c[0] == "csr_register":
        regs.append({"name": c[1], "address": int(c[2], 16), "words": int(c[3]), "mode": c[4]})
    elif c[0] == "csr_base":
        banks.append({"name": c[1], "origin": int(c[2], 16)})
    elif c[0] == "memory_region":
        mems.append({"name": c[1], "origin": int(c[2], 16), "size": int(c[3]), "type": c[4]})
desc = json.loads((export / "aem_desc.json").read_text())
checks = {
    "csr_csv_sha256": committed["csr_csv_sha256"] == hashlib.sha256("\n".join(body).encode()).hexdigest(),
    "constants": committed["constants"] == consts,
    "csr_registers": committed["csr_registers"] == regs,
    "csr_banks": committed["csr_banks"] == banks,
    "memory_regions": committed["memory_regions"] == mems,
    "pp_windows": committed["pp_windows"] == {k: desc[k] for k in ("desc_base", "resp_base", "nvm_base", "nvm_stage_base", "window_bytes")},
}
for k, v in checks.items():
    print(f"{'ok  ' if v else 'DIFF'} {k}")
if not checks["constants"]:
    for k in sorted(set(consts) | set(committed["constants"])):
        if consts.get(k) != committed["constants"].get(k):
            print("   ", k, committed["constants"].get(k), "->", consts.get(k))
print("not compared: datapath parameters (need the export's gateware/)")
sys.exit(0 if all(checks.values()) else 1)
