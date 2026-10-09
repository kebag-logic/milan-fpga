#!/usr/bin/env python3
"""Read source mutation tables as data; compare every portable substitution."""
import argparse
import ast
import importlib
import json
import hashlib
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
from collections import Counter

p = argparse.ArgumentParser()
p.add_argument("source", type=Path)
p.add_argument("repository", type=Path)
p.add_argument("results", type=Path)
a = p.parse_args()
directory = a.source / "sw/firmware/ctrl/test"
sys.path.insert(0, str(directory))
Mutant = importlib.import_module("ctrl_mutant").Mutant
acmp = importlib.import_module("acmp_mutants")
maap = importlib.import_module("maap_mutants").mutants
tree = ast.parse((directory/"ctrl_mutants.py").read_text())
# Only top-level table assignments execute. No runner or source bank is loaded.
nodes = [n for n in tree.body if isinstance(n, (ast.Assign, ast.AugAssign))]
namespace = {"acmp_mutants": acmp, "maap_mutants": maap, "Mutant": Mutant}
exec(compile(ast.Module(body=nodes, type_ignores=[]), "published-mutation-table", "exec"), namespace)
paths = {f"{m}/{m}.{e}": f"{d}/{m}.{e}" for m in ("adp", "acmp", "maap") for e,d in (("c","src"),("h","include"))}
paths["wire/wire.h"] = "include/wire.h"
original = {m.name: m for m in namespace["MUTANTS"] if m.path in paths}
current = {m["name"]: m for m in json.loads((a.repository/"tests/mutations.json").read_text())}
differences = []
for name in original.keys() & current.keys():
    before, after = original[name], current[name]
    if (paths[before.path], before.old, before.new) != (after["path"], after["old"], after["new"]):
        differences.append(name)
results = json.loads(a.results.read_text())
kills = sum(len(m["kills"]) for m in current.values())
checks = []
for r in results:
    m = current[r["name"]]
    default = "maap_debug" if any(k["test"].startswith("MaapDebug.") for k in m["kills"]) else Path(m["path"]).stem
    proofs = []
    for k in m["kills"]:
        arm = k.get("arm", default)
        path = a.results.parent/m["name"]/(arm+".xml")
        doc = ET.parse(path).getroot()
        failures = {case.get("classname")+"."+case.get("name"): "\n".join(f.get("message", "") for f in case.findall("failure")) for case in doc.iter("testcase") if case.findall("failure")}
        present = any(n.startswith(k["test"]) and k["needle"] in text for n,text in failures.items())
        proofs.append({"arm":arm,"test":k["test"],"needle":k["needle"],"assertion_present":present,"xml_sha256":hashlib.sha256(path.read_bytes()).hexdigest()})
    checks.append({"name": r["name"], "status": r["status"], "required_kills": len(m["kills"]), "all_named_assertions_present": all(p["assertion_present"] for p in proofs), "proofs": proofs})
print(json.dumps({"original_portable_plants":len(original), "imported_plants":len(current), "missing": sorted(original.keys()-current.keys()), "extra":sorted(current.keys()-original.keys()), "changed_substitutions":differences, "required_assertion_kills":kills, "results":dict(Counter(r["status"] for r in results)), "plants":checks}, indent=2))
