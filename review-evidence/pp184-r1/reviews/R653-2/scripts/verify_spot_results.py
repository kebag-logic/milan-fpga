#!/usr/bin/env python3
from pathlib import Path
p=Path(__file__).resolve().parents[1]
for label,needle,rc in [("golden","probe: 12 PASS, 0 FAIL",0),("refresh-while-waiting","FAIL: B1b",1),("enqueue-next-state","FAIL: B3b",1),("pop-without-ready","FAIL: B1b",1)]:
    text=(p/f"receipts/local-{label}.log").read_text()
    assert int((p/f"receipts/local-{label}.rc").read_text())==rc
    assert needle in text
    print(f"PASS {label}: rc {rc}; {needle}")
assert (p/"receipts/local-docs.rc").read_text().strip()=="0"
print("PASS documentation gate rc 0")
