"""Verify published hashes, counts, named kills and README campaign table."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
root = Path(sys.argv[1]).resolve()
p = Path(__file__).resolve().parent
manifest = {x["file"]: x for x in json.loads((p / "published/MANIFEST.json").read_text())}
count = 0
for f in (p / "published").rglob("*"):
    if not f.is_file() or f.name == "MANIFEST.json":
        continue
    name = f.relative_to(p / "published").as_posix()
    assert hashlib.sha256(f.read_bytes()).hexdigest() == manifest[name]["published_sha256"], name
    count += 1
print(f"PASS manifest: {count} retained files")
a = p / "published/author-r3/receipts"
s = (a / "round3/campaign/campaign-600565b4.verdicts.txt").read_text()
kills = [l for l in s.splitlines() if l.startswith("[PASS] mutant caught:")]
clean = [l for l in s.splitlines() if l.startswith("[PASS] the unmutated")]
assert len(kills) == 63 and len(clean) == 5
assert "68 checks: 68 PASS, 0 FAIL" in s and "CAMPAIGN rc=0" in s
spec = importlib.util.spec_from_file_location("reviewed_campaign", root / "tb/verilator/milan_dp/dynmap_mutants.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
assert len(m.MUTATIONS) == 63
for n, (row, kill) in enumerate(zip(m.MUTATIONS, kills), 1):
    assert row[1] in kill, n
    names = (row[3],) if isinstance(row[3], str) else row[3]
    assert all(name in kill for name in names), n
    if n >= 61:
        rtl = (root / "hdl/milan/milan_datapath.sv").read_text()
        for before, after in row[2]:
            assert rtl.count(before) == 1
            assert before != after
        print(f"PASS row {n}: unique predicate anchor; every named blank check caught")
readme = (root / "tb/verilator/milan_dp/README.md").read_text()
rows = re.findall(r"^\| (\d+) \| .*?\| (\d+) of (\d+) \|$", readme, re.M)
assert len(rows) == 63
for (n, failures, total), kill in zip(rows, kills):
    match = re.search(r"(\d+) failure\(s\) across (\d+) checks", kill)
    assert match and match.groups() == (failures, total), n
print("PASS all 63 README failure tallies match campaign receipts; five clean legs")
for leg, expected in [("dynmap", 649), ("maprec8", 219), ("maprec4", 137)]:
    text = (a / f"round3/legs/leg-{leg}.log").read_text()
    assert re.search(rf"checks:\s*{expected}\s+failures:\s*0", text)
    assert "RESULT: PASS" in text
    print(f"PASS published {leg}: {expected}/0")
rc = (a / "round3/docs/rc.tsv").read_text().splitlines()
assert len(rc) == 95 and all(l.split("\t")[1] == "0" for l in rc)
rc = (a / "round3/builder/rc.tsv").read_text().splitlines()
assert len(rc) == 2 and all(l.split("\t")[1] == "0" for l in rc)
print("PASS docs receipts: 95 rc 0; builder receipts: two rc 0; calibration remains NOT RUN")
old = (a / "round2/campaign/campaign-af5eefc6.log.excerpt").read_text()
rerun = (a / "round2/campaign/campaign-row36-af5eefc6.log").read_text()
assert "65 checks: 63 PASS, 2 FAIL" in old and "CAMPAIGN rc=2" in old
assert "2 checks: 2 PASS, 0 FAIL" in rerun and "ROW36 rc=0" in rerun
print("PASS round-2 account: full rc 2 63/65; listener rc 0 2/2; distinct executions")
