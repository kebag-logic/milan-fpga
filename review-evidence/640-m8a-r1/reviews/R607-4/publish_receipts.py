#!/usr/bin/env python3
"""Copy selected raw command receipts with only local path substitutions; never publish scratch trees."""
import json,pathlib,re,sys
out=pathlib.Path(sys.argv[1]).resolve();repo=pathlib.Path(sys.argv[2]).resolve()
def scrub(text):
 text=text.replace(str(out),"$PACKET").replace(str(repo),"$REVIEW_CLONE")
 text=re.sub(r"/home/[^/\s]+",lambda m:"$HOME",text)
 text=text.replace("$VALIDATION_TOOLS/","$TOOLS/")
 return text
for path in (out/"scratch").glob("*.raw.log"):
 (out/path.name.replace(".raw.log",".log")).write_text(scrub(path.read_text(errors="replace")))
for tag in ["fit","previous-fit"]:
 for shape in ["1x1_tdm8","8x8"]:
  for i in [1,2]:
   stem=f"{tag}-{shape}-if{i}"
   for name in ["size.txt","symbols.txt"]:
    source=out/"scratch"/stem/name
    if source.exists():(out/(stem+"-"+name)).write_text(scrub(source.read_text()))
provenance=out/"scratch/runtime/provenance.json"
(out/"runtime-provenance.json").write_text(scrub(provenance.read_text()))
for path in out.iterdir():
 if path.is_file() and path.suffix in {".log",".json"} and path.name!="MANIFEST.sha256":
  path.write_text(scrub(path.read_text()))
print("PASS public receipts copied with path substitutions only; originals remain under scratch")
