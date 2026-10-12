#!/usr/bin/env python3
import argparse,json,pathlib,re
p=argparse.ArgumentParser();p.add_argument("source",type=pathlib.Path);p.add_argument("packet",type=pathlib.Path);a=p.parse_args()
mutants={m["name"]:m for m in json.loads((a.source/"tests/mutations.json").read_text())};rows=[];plants={}
for line in (a.source/"docs/VERIFICATION.md").read_text().splitlines():
 if not re.match(r"\| (?:P|R)\d\d \|",line):continue
 cells=[x.strip() for x in line.strip("|").split("|")];rid,scope,killers,names=cells
 ns=re.findall(r"`([^`]+)`",names)
 assert ns or names=="None"
 for n in ns:
  m=mutants[n];assert len(m["kills"])==1
  k=m["kills"][0];assert k["test"] in killers
  plants[n]={**{key:m[key] for key in ("name","path","old","new")},"killer":k["test"],"needle":k["needle"],"modes":["full","removed"]}
 rows.append({"row":rid,"scope":scope,"killers":killers,"plants":ns})
assert len(rows)==31 and len(plants)==42
(a.packet/"receipts/contract-rows.json").write_text(json.dumps(rows,indent=2)+"\n")
(a.packet/"scripts/plants-contract.json").write_text(json.dumps(list(plants.values()),indent=2)+"\n")
print("contract:",len(rows),"rows",len(plants),"distinct plants")
