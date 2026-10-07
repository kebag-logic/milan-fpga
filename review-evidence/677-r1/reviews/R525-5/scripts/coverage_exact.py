#!/usr/bin/env python3
"""Compare exact measured denominators as well as the standard ratio gate."""
import pathlib,sys,subprocess,json,dataclasses
root=pathlib.Path.cwd();packet=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/"sw/firmware/gtest"))
import fw_coverage as c
rows=c.exclusions(c.README.read_text())
key=lambda x:(x.file,x.function,x.statement,x.uncovered)
for rev in ("64e62816ad21791f6df3657fadb935aec5555881","708e5634f28e6e5a19236a9b0a9a543c3622e52d"):
 prior=c.exclusions(subprocess.check_output(["git","show",rev+":sw/firmware/gtest/README.md"],text=True))
 assert [key(x) for x in rows]==[key(x) for x in prior]
assert len(rows)==14
merged=c.collect([packet/"scratch/coverage"])
kept,findings=c.apply_exclusions(merged,rows)
assert not findings,findings
measurement=c.render_ratchet(c.tally(kept))
(packet/"receipts/measured.ratchet").write_text(measurement)
assert measurement==c.RATCHET.read_text()
print(measurement)
print("PASS: exact measured line/branch numerators and denominators equal all 14 recorded rows")
print("PASS: 14 exclusion identities and their arc/line counts match both parents")
