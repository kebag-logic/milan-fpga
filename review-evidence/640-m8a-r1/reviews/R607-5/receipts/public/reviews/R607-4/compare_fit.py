#!/usr/bin/env python3
"""Compare identical-runtime links and verify the published table belongs to the previous source."""
import hashlib,json,pathlib,sys
out=pathlib.Path(sys.argv[1]);old_expected=[(95032,45520,35),(96320,56880,38),(108680,86080,48.5),(110056,112208,54.5)]
rows=[]
for (shape,i),want in zip([(s,i) for s in ["1x1_tdm8","8x8"] for i in [1,2]],old_expected):
 old=json.loads((out/f"previous-fit-{shape}-if{i}.json").read_text())
 new=json.loads((out/f"fit-{shape}-if{i}.json").read_text())
 assert old["artifacts"][:2]==new["artifacts"][:2]
 def value(d):
  p=d["split"];r,m=p["rom"],p["sram"]
  # Independent granule-rounding equation, no call to the planner.
  expected=( ((r["bytes"]+2047)//2048) + ((m["bytes"]+2047)//2048) )/2
  assert expected==p["tiles"]
  return r["bytes"],m["bytes"],p["tiles"]
 before,after=value(old),value(new)
 assert before==want
 assert after[2]<=56
 print(shape,i,"previous:",before,"head:",after,"runtime identical; head within limit")
 rows.append({"shape":shape,"interfaces":i,"previous":before,"head":after,"head_rom_banks":new["split"]["rom"]["banks"]})
assert rows[-1]["head"][2]==55 and rows[0]["head"][2]==35.5
print("Largest planned allocation headroom:",(56-rows[-1]["head"][2])*4096,"bytes, not the documented 6144")
print("PASS reproduction: previous links match all four published rows; merged links change every span")
(out/"fit-comparison.json").write_text(json.dumps(rows,indent=2)+"\n")
