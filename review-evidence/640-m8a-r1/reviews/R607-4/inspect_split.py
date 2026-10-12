#!/usr/bin/env python3
"""Check the current largest linked image's real SoC export and publication outputs."""
import json,pathlib,re,sys
out=pathlib.Path(sys.argv[1]);d=out/"scratch/export-head-split-8x8/export"
v=(d/"gateware/alinx_ax7101.v").read_text();plan=json.loads((out/"fit-8x8-if2.json").read_text())["split"]
memories=dict(re.findall(r"^reg \[31:0\] (\w+)\[0:(\d+)\];",v,re.M))
want={f"{region}_bank{n}":str(size//4-1) for region,key in [("rom","rom"),("sram","sram")] for n,size in enumerate(plan[key]["banks"])}
actual={k:val for k,val in memories.items() if "_bank" in k}
assert actual==want,(actual,want)
assert not {"rom","sram"}&set(memories)
for pin in ["da_gate","licence","idle_slope_bps","dom_vid","dom_prio","dom_adopted","talker_decl","bound","sid_valid","started","sid"]:
 assert f".pub_{pin}_o" in v,pin
print("PASS current largest image: actual export has",len(want),"image banks and no BIOS memory")
print("PASS all 11 publication output ports preserved")
print("RAM declarations",json.dumps(actual,sort_keys=True))
for line in (d/"csr.csv").read_text().splitlines():
 if line.startswith("memory_region,"):print(line)
print("RESULT: PASS")
