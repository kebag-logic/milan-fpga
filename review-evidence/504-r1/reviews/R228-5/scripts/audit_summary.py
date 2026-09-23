#!/usr/bin/env python3
"""Summarise a gate 1b compiler audit (JSON lines written by the head's
sw/builder/test_firmware_compiler.py): records, executed/absent calls, whether
every executed call kept its argument tail, and the census assembly arches."""
import collections
import json
import sys

for path in sys.argv[1:]:
    recs = [json.loads(line) for line in open(path) if line.strip()]
    executed = [r for r in recs if r.get("actual_argv")]
    absent = [r for r in recs if r.get("result") == "deliberately absent"]
    tails_changed = sum(r["requested_argv"][1:] != r["actual_argv"][1:] for r in executed)
    mapped = sum(r["requested_argv"][0] != r["actual_argv"][0] for r in executed)
    compiles = sum("-std=gnu99" in r["actual_argv"] for r in executed)
    arches = collections.Counter(r.get("assembly_arch") for r in executed if "assembly_arch" in r)
    rc = collections.Counter(r.get("returncode") for r in executed)
    print(json.dumps({"audit": path.rsplit("/", 1)[-1], "records": len(recs),
                      "executed": len(executed), "deliberately_absent": len(absent),
                      "argv0_mapped": mapped, "argv_tails_changed": tails_changed,
                      "firmware_compiles": compiles, "census_arches": dict(arches),
                      "returncodes": {str(k): v for k, v in rc.items()}}))
