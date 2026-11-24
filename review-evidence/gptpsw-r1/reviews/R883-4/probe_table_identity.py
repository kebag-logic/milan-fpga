"""Reviewer probe: serialise the control campaign's MUTANTS table from an extracted tree.
usage: python3 -I probe_table_identity.py <extracted-root>  (prints count and sha256 of the ordered table)"""
import dataclasses, hashlib, json, sys
root = sys.argv[1]
sys.path[:0] = [root + "/sw/firmware/ctrl/test", root + "/sw/firmware/gtest", root + "/scripts"]
import ctrl_mutants
rows = [dataclasses.asdict(m) for m in ctrl_mutants.MUTANTS]
blob = json.dumps(rows, sort_keys=True).encode()
print(len(rows), hashlib.sha256(blob).hexdigest(), [r["name"] for r in rows].index("pub-gptp-generation-written-twice"))
