#!/usr/bin/env python3
"""Path-only public receipt redaction and manifest; originals stay unpublished."""
import argparse,hashlib,json,pathlib,re,shutil
p=argparse.ArgumentParser();p.add_argument("--packet",type=pathlib.Path,required=True);p.add_argument("--source",type=pathlib.Path,default=pathlib.Path.cwd());a=p.parse_args();out=a.packet.resolve();raw=out/"scratch/raw-receipts";raw.mkdir(exist_ok=True);redactions=[]
for f in sorted((out/"receipts").glob("*.log")):
    original=f.read_bytes();s=original.decode()
    # This is the installed compiler support prefix, not a job/container run.
    s=re.sub(r"/home/[^/\s]+/\.local/share/containers/storage/overlay/[^/\s]+/diff/usr/share/verilator", "<SIMULATOR_SUPPORT>",s)
    s=s.replace(str(out),"<PACKET>").replace(str(a.source.resolve()),"<SOURCE>")
    s=re.sub(r"/home/[^/\s]+", "<HOME>",s)
    data=s.encode()
    if data!=original:
        (raw/f.name).write_bytes(original);f.write_bytes(data)
        redactions.append(dict(file=str(f.relative_to(out)),original_sha256=hashlib.sha256(original).hexdigest(),published_sha256=hashlib.sha256(data).hexdigest(),change="path-only substitutions; all diagnostics and numbers retained"))
(out/"receipts/redactions.json").write_text(json.dumps(redactions,indent=2)+"\n")
files=sorted([out/"REPORT.md",*[f for d in ("receipts","scripts") for f in (out/d).iterdir() if f.is_file()]])
assert "SKELETON" not in (out/"REPORT.md").read_text()
assert (out/"REPORT.md").read_text().splitlines()[-1]=="R523-2 FINISHED"
with (out/"MANIFEST.sha256").open("w") as manifest:
    for f in files:manifest.write(hashlib.sha256(f.read_bytes()).hexdigest()+"  "+str(f.relative_to(out))+"\n")
print(f"Published population: {len(files)} files, including REPORT.md; scratch excluded")
