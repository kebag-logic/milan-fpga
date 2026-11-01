#!/usr/bin/env python3
"""Write each design-notes Contents description from the module purposes."""
import json, re, sys
root = sys.argv[1]
sys.path.insert(0, root + "/scripts")
from register_page import strip_md
d = json.load(open(root + "/scripts/register_descriptions.json"))
pur = {strip_md(m["heading"]): m["purpose"] for m in d["modules"]}
pur["Reading the register map"] = "How the control plane was replaced, and how to read the map."
pur["SoC CSR banks"] = "The LiteX banks beside the Milan block."
p = root + "/docs/design/CSR_REGISTER_NOTES.md"
out = []
for line in open(p, encoding="utf-8"):
    m = re.match(r"- \*\*\[(.*)\]\(#[^)]*\)\*\* -- TODO describe this section", line)
    if m:
        key = m.group(1).replace("\\*", "*")
        line = line.replace("TODO describe this section", pur[key])
    out.append(line)
open(p, "w", encoding="utf-8").writelines(out)
