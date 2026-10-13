#!/usr/bin/env python3
"""Check merge continuity and independently compare seven core token streams."""
import argparse
import json
from pathlib import Path
import re
import subprocess

p = argparse.ArgumentParser()
p.add_argument("root",type=Path)
p.add_argument("public",type=Path)
a = p.parse_args()
def git(*args):
    return subprocess.check_output(["git","-C",str(a.root),*args],text=True)
head=git("rev-parse","HEAD").strip()
dev="e81ce82f9aa3e4dcaffa5bcdf7e60f0c7cffd80c"
assert git("show","-s","--format=%P","a71b0e41").split() == ["97e713168470bfae2685521fa557dc462b782b32",dev]
for path in ("hdl","configs","scripts/suite_shards.py","tb/tools/torture_campaign.py","tests/features/counters_contract_milan.feature","tests/steps/counters_contract_steps.py"):
    assert not git("diff",dev,head,"--",path).strip(),path
    print("IDENTICAL TO DEV " + path)
for path in ("third_party/tsn-c-stack","third_party/lwSRP"):
    assert not git("diff","97e71316",head,"--",path).strip(),path
    print("UNCHANGED PIN " + path + " " + git("rev-parse",head+":"+path).strip())
pattern=re.compile(r'''//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|\s+|[A-Za-z_]\w*|[0-9]+(?:\.[0-9]+)?|[^\s]''',re.S)
def tokens(text):
    result=[];line=1
    for m in pattern.finditer(text):
        word=m.group()
        if not word.isspace() and not word.startswith(("//","/*")):
            result.append((word,line))
        line+=word.count("\n")
    return result
for module in ("adp","acmp","maap"):
    for ext,part in (("c","src"),("h","include")):
        old=f"sw/firmware/ctrl/{module}/{module}.{ext}"
        new=a.root/f"third_party/tsn-c-stack/{part}/{module}.{ext}"
        first=git("show",dev+":"+old);second=new.read_text()
        assert tokens(first)==tokens(second),old
        print("TOKEN AND LINE IDENTITY " + old + " -> " + str(new.relative_to(a.root)))
old="sw/firmware/ctrl/wire/wire.h"; new=a.root/"third_party/tsn-c-stack/include/wire.h"
assert tokens(git("show",dev+":"+old))==tokens(new.read_text())
print("TOKEN AND LINE IDENTITY " + old + " -> third_party/tsn-c-stack/include/wire.h")
equal=json.loads((a.public/"image-equality.json").read_text())
assert equal["images"]==len(equal["pairs"])==65 and equal["equal"]
assert all(x["head"]==x["dev"] for x in equal["pairs"])
assert len({x["head"]["path"] for x in equal["pairs"]})==65
head_images=json.loads((a.public/"images-head.json").read_text())
dev_images=json.loads((a.public/"images-dev.json").read_text())
assert head_images==dev_images
print("PUBLIC AUTHOR IMAGE RECEIPTS: 65 unique entries; paired paths, sizes and SHA-256 values identical")
coverage=json.loads((a.public/"coverage-comparison.json").read_text())
assert coverage["head"]==head and coverage["dev"]==dev and coverage["files"]==len(coverage["rows"])==30
assert all(row[-2:]==["100.00","100.00"] for row in coverage["rows"].values())
print("PUBLIC AUTHOR COVERAGE RECEIPTS: 30 normalized rows at exact head/dev; all 100% after exclusions")
print("PASS: source structure and published receipt consistency; no image rebuild claimed")
