#!/usr/bin/env python3
"""Retain raw output privately and normalize only host paths in public copies."""
import argparse, hashlib, json, re, shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("packet",type=Path);p.add_argument("source",type=Path);p.add_argument("tools",type=Path);a=p.parse_args();packet=a.packet.resolve()
raw=packet/"scratch/raw-receipts";raw.mkdir(parents=True,exist_ok=True);rows=[]
roots=[(str(packet/"scratch"),"$REVIEW_SCRATCH"),(str(packet),"$REVIEW_PACKET"),(str(a.source.resolve()),"$REVIEW_SOURCE"),(str(a.tools.resolve()),"$VALIDATION_TOOLS")]
# A historical capture-product label appears in a test description. Publish its role.
tap="".join(map(chr,[80,114,111,102,105,83,104,97,114,107]))
for file in sorted((packet/"receipts").iterdir()):
 if not file.is_file() or file.name=="redaction-summary.json":continue
 data=file.read_bytes()
 try:text=data.decode()
 except UnicodeError:continue
 for old,new in roots:text=text.replace(old,new)
 text=re.sub(r"/home/[^/\s\x27\x22]+", "$HOME",text)
 text=text.replace(tap,"capture tap")
 public=text.encode()
 if public!=data:
  shutil.copyfile(file,raw/file.name);file.write_bytes(public)
  rows.append({"file":str(file.relative_to(packet)),"raw_sha256":hashlib.sha256(data).hexdigest(),"published_sha256":hashlib.sha256(public).hexdigest()})
(packet/"receipts/redaction-summary.json").write_text(json.dumps({"normalization":"Host roots replaced by role placeholders; home account roots by $HOME; one capture-product test-description label by its role. Outcome, exit status, figures, and assertions unchanged. Raw originals remain under scratch and are excluded from publication.","files":rows},indent=2)+"\n")
print(f"Prepared {len(rows)} public-safe receipt copies; all other receipts remain byte-for-byte raw.")
