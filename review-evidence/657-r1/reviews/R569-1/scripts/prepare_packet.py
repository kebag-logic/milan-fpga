#!/usr/bin/env python3
"""Prepare public receipts, retaining unredacted originals only in scratch."""
import hashlib,json,pathlib,re
packet=pathlib.Path(__file__).resolve().parents[1]
originals=packet/"scratch/unpublished-originals";originals.mkdir(exist_ok=True)
changes=[]
for path in sorted((packet/"receipts").rglob("*")):
    if not path.is_file() or path.name=="redactions.json":continue
    data=path.read_bytes()
    try:text=data.decode()
    except UnicodeDecodeError:continue
    # Preserve paths only by installation/workspace role, never home identity.
    text=text.replace("<home-path>/work/milan-fpga/milan-fpga", "<hosted-workspace>")
    text=text.replace("<home-path>", "<hosted-runner-home>")
    text=re.sub(r"/home/[^/\s]+/[^\s\"']+", "<compiler-install-path>", text)
    text=text.replace(str(packet),"<review-packet>")
    text=text.replace("$REVIEWS/r569-1-657","<review-source>")
    text=text.replace("$VALIDATION_TOOLS/pinned-verilator-5.050/verilator","<pinned-compiler>")
    changed=text.encode()
    if changed!=data:
        rel=path.relative_to(packet)
        dest=originals/rel;dest.parent.mkdir(parents=True,exist_ok=True)
        if not dest.exists():dest.write_bytes(data)
        path.write_bytes(changed)
        changes.append({"file":str(rel),"raw_sha256":hashlib.sha256(data).hexdigest(),"published_sha256":hashlib.sha256(changed).hexdigest(),"change":"installation and review paths replaced by role placeholders; measurements and verdicts unchanged"})
(packet/"receipts/redactions.json").write_text(json.dumps(changes,indent=2)+"\n")
files=sorted(p for directory in (packet/"scripts",packet/"receipts") for p in directory.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
(packet/"MANIFEST.sha256").write_text("".join(hashlib.sha256(p.read_bytes()).hexdigest()+"  "+str(p.relative_to(packet))+"\n" for p in files))
print(f"Prepared {len(files)} publishable files; {len(changes)} path-redacted receipts")
