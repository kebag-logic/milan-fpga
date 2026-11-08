#!/usr/bin/env python3
"""Compare the csr.csv-derived part of a committed SoC extract with a published export csr.csv.

Usage: check_extract_vs_csv.py <register_map_soc.json> <csr.csv> [<aem_desc.json>]
Re-derives csr_csv_sha256, memory regions, CSR banks, CSR registers and the milan_/spiflash_/config_
constants the way the extract's own reader does, and prints every key that differs. Exit 0 when equal.
The datapath parameters come from the export's top-level Verilog, which is not published, so they
are not compared here.
"""
import hashlib
import json
import re
import sys

soc = json.load(open(sys.argv[1], encoding="utf-8"))
lines = open(sys.argv[2], encoding="utf-8").read().splitlines()
body = [ln for ln in lines if ln and not ln.startswith("#")]
got = {"csr_csv_sha256": hashlib.sha256("\n".join(body).encode()).hexdigest(),
       "memory_regions": [], "csr_banks": [], "csr_registers": [], "constants": {}}
for ln in body:
    c = ln.split(",")
    if c[0] == "memory_region":
        got["memory_regions"].append({"name": c[1], "origin": int(c[2], 16), "size": int(c[3]), "type": c[4]})
    elif c[0] == "csr_base":
        got["csr_banks"].append({"name": c[1], "origin": int(c[2], 16)})
    elif c[0] == "csr_register":
        got["csr_registers"].append({"name": c[1], "address": int(c[2], 16), "words": int(c[3]), "mode": c[4]})
    elif c[0] == "constant" and (c[1].startswith(("milan_", "spiflash_"))
                                 or c[1] in ("config_clock_frequency", "config_platform_name")):
        got["constants"][c[1]] = int(c[2]) if re.fullmatch(r"-?\d+", c[2]) else c[2]
bad = 0
for k, v in got.items():
    if soc.get(k) != v:
        bad += 1
        print(f"DIFFERS {k}")
if len(sys.argv) > 3:
    desc = json.load(open(sys.argv[3], encoding="utf-8"))
    w = {k: desc[k] for k in ("desc_base", "resp_base", "nvm_base", "nvm_stage_base", "window_bytes")}
    if soc.get("pp_windows") != w:
        bad += 1
        print("DIFFERS pp_windows")
mac = soc["constants"]["milan_station_mac_lo"].to_bytes(4, "little") + \
    soc["constants"]["milan_station_mac_hi"].to_bytes(2, "little")
eid = (soc["constants"]["milan_entity_id_hi"] << 32) | soc["constants"]["milan_entity_id_lo"]
print("station MAC", ":".join(f"{b:02X}" for b in mac), "entity_id", f"0x{eid:016X}")
print("equal" if not bad else f"{bad} key(s) differ")
sys.exit(1 if bad else 0)
