#!/usr/bin/env python3
"""Compare every exported artifact except logs; normalize only output roots, Date lines and hierarchy comments."""
import hashlib,json,pathlib,re,sys
out=pathlib.Path(sys.argv[1]);rows=[]
for shape in ["1x1_tdm8","8x8"]:
 a=out/"scratch"/f"export-base-{shape}"/"export";b=out/"scratch"/f"export-head-{shape}"/"export"
 files=lambda d:{p.relative_to(d) for p in d.rglob("*") if p.is_file() and p.name!="litex.log"}
 assert files(a)==files(b)
 for rel in sorted(files(a)):
  def normalize(root):
   data=(root/rel).read_bytes()
   if b"\0" in data:return data
   data=data.replace(str(root).encode(),b"$EXPORT")
   data=re.sub(rb"(?m)^// Date\s*:.*$",b"// Date: $STAMP",data)
   # The one generated hierarchy comment before the Signals section.
   if rel.suffix==".v":
    removed=[]
    def comment(match):
     if b"[BB:" in match[0]:
      removed.append(1);return b"/* hierarchy omitted */"
     return match[0]
    data=re.sub(rb"/\*.*?\*/",comment,data,flags=re.S)
    assert len(removed)==1,(rel,len(removed))
   return data
  aa,bb=normalize(a),normalize(b)
  assert aa==bb,(shape,str(rel))
  rows.append({"shape":shape,"path":str(rel),"sha256":hashlib.sha256(aa).hexdigest()})
 print("PASS",shape,len(files(a)),"artifacts equal; generated hierarchy/Date/output root normalized")
(out/"export-digests.json").write_text(json.dumps(rows,indent=2)+"\n")
