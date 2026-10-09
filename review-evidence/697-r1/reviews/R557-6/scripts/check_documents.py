#!/usr/bin/env python3
import json,pathlib,re,sys,urllib.parse
root=pathlib.Path(sys.argv[1]).resolve(); out=pathlib.Path(sys.argv[2]); rows=[]; errors=[]
for path in [*root.glob("*.md"),*(root/"docs").glob("*.md")]:
 for match in re.finditer(r"\[[^\]]*\]\(([^)]+)\)",path.read_text()):
  url=match[1]
  if re.match(r"\w+:",url):continue
  part,_,anchor=url.partition("#"); target=(path.parent/urllib.parse.unquote(part)).resolve() if part else path
  row={"file":str(path.relative_to(root)),"link":url,"exists":target.exists()}
  if not target.exists():errors.append(row)
  if anchor.startswith("L") and anchor[1:].isdigit() and target.is_file():
   row["line_valid"]=0<int(anchor[1:])<=len(target.read_text().splitlines())
   if not row["line_valid"]:errors.append(row)
  rows.append(row)
result={"relative_links":len(rows),"line_links":sum("line_valid" in r for r in rows),"errors":errors};out.write_text(json.dumps(result,indent=2)+"\n");print(json.dumps(result));assert not errors
