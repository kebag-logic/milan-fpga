#!/usr/bin/env python3
"""Copy focused raw receipts with explicit, hashed path-only redactions.

Usage: publish_receipts.py REPO PACKET SIMULATOR
Does not modify source files or originals under scratch.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

repo, packet, simulator = map(lambda x:Path(x).resolve(),sys.argv[1:4])
scratch=packet/"scratch"
out=packet/"receipts"
wrapper=simulator.read_text()
root=re.search(r"VERILATOR_ROOT=(\S+)",wrapper)[1]
sim_command=re.search(r" (\S+/bin/verilator) ",wrapper)[1]
version=subprocess.check_output([str(simulator),"--version"],text=True).strip()
assert "Verilator 5.050" in version and "rev v5.050" in version
digest=lambda data:hashlib.sha256(data).hexdigest()
identity={"version":version,"wrapper_sha256":digest(simulator.read_bytes()),"program_sha256":digest(Path(sim_command).read_bytes())}
(out/"simulator-identity.json").write_text(json.dumps(identity,indent=2)+"\n")
replacements=sorted([(str(repo),"<repo>"),(str(packet),"<packet>"),(str(simulator),"<simulator>"),(str(simulator.parent),"<simulator-dir>"),(root,"<SIMULATOR_ROOT>"),(str(Path(sim_command).parent),"<SIMULATOR_BIN>")],key=lambda x:-len(x[0]))
records=[]
def copy(source,destination):
    raw=source.read_bytes()
    text=raw.decode()
    for old,new in replacements:
        text=text.replace(old,new)
    data=text.encode()
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_bytes(data)
    records.append({"original":source.relative_to(packet).as_posix(),"published":destination.relative_to(packet).as_posix(),"original_sha256":digest(raw),"published_sha256":digest(data),"path_redacted":raw!=data})
for source in scratch.glob("*.raw.log"):
    copy(source,out/(source.name.removesuffix(".raw.log")+".log"))
for group in ("fine-results","controller","mutants"):
    for source in sorted((scratch/group).rglob("*")):
        if not source.is_file():continue
        relative=source.relative_to(scratch/group)
        if any(p in {"obj_dir","obj_mut"} for p in relative.parts):continue
        if source.suffix not in {".log",".rc"} and not source.name.endswith(".command.json"):continue
        copy(source,out/group/relative)
(out/"publication-redactions.json").write_text(json.dumps(records,indent=2)+"\n")
print(f"Published {len(records)} execution receipts with path-only redactions; originals remain in scratch.")
