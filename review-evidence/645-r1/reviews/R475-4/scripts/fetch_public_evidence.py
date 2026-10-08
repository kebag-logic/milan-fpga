#!/usr/bin/env python3
"""Read the pinned public evidence; extract only the author-r2e packet.

Usage: fetch_public_evidence.py PACKET
Requires authenticated read access through gh. Writes only PACKET/scratch.
"""
import json
from pathlib import Path
import subprocess
import sys
import tarfile

scratch=Path(sys.argv[1]).resolve()/"scratch"
scratch.mkdir(parents=True,exist_ok=True)
commit="00f489b18c63d9cf7e617ddb9e0437902062d416"
endpoint="repos/kebag-logic/milan-fpga/"
tree=subprocess.check_output(["gh","api",endpoint+"git/trees/"+commit+"?recursive=1"])
assert not json.loads(tree).get("truncated")
(scratch/"evidence-tree.json").write_bytes(tree)
archive=scratch/"evidence.tar.gz"
with archive.open("wb") as out:
    subprocess.run(["gh","api",endpoint+"tarball/"+commit],stdout=out,check=True)
prefix="review-evidence/645-r1/author-r2e/"
count=0
with tarfile.open(archive) as tar:
    for member in tar:
        split=member.name.split("/",1)
        if len(split)!=2 or not split[1].startswith(prefix) or not member.isfile():
            continue
        relative=Path(split[1][len(prefix):])
        assert not relative.is_absolute() and ".." not in relative.parts
        target=scratch/"author-r2e"/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(tar.extractfile(member).read())
        count+=1
print(f"Extracted {count} public author-r2e files from {commit}")
