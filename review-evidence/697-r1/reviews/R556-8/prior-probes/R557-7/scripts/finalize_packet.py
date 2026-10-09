#!/usr/bin/env python3
import hashlib,pathlib,re,sys
p=pathlib.Path(sys.argv[1]).resolve()
report=(p/"REPORT.md").read_text()
assert report.splitlines()[0]=="[R557] NEGATIVE - exact head 68070cb5723682586c07a6de80a49886732b5dc2"
assert report.splitlines()[-1]=="R557-7 FINISHED" and "SKELETON" not in report
for link in re.findall(r"\]\(([^)]+)\)",report):
 if not re.match(r"[a-z]+:",link):assert (p/link.split("#",1)[0]).exists(),link
paths=sorted([f for d in ["scripts","receipts"] for f in (p/d).rglob("*") if f.is_file()])
for f in paths:
 data=f.read_text()
 assert str(p) not in data and str(pathlib.Path.home()) not in data,str(f)
lines=[hashlib.sha256(f.read_bytes()).hexdigest()+"  "+f.relative_to(p).as_posix() for f in paths]
(p/"MANIFEST.sha256").write_text("\n".join(lines)+"\n")
print(len(paths),"publishable files; report links and public-text checks pass")
