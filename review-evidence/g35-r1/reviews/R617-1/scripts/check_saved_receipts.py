#!/usr/bin/env python3
"""Audit the resumed round's raw results; never equate a nonzero exit with a catch."""
from pathlib import Path
import re,sys
p=Path(sys.argv[1])
for g in ("tb","contract","lint","docs"):
 assert (p/f"receipts/gates_head/gate_{g}.rc").read_text().strip()=="0"
print("Four donor gate exit codes: PASS")
text=(p/"receipts/gates_head/gate_tb.log").read_text()
assert "298 checks: 298 PASS, 0 FAIL" in text
assert text.count("[PASS] mutant caught:")>=7
print("Parser: 298 checks PASS; all seven committed named controls PASS")
for tag in ("R1_latch_deleted","R2_latch_before_sof_clear","R3_eof_direct_term_dropped","R7_latch_outside_valid"):
 s=(p/f"receipts/reviewer_mutants/{tag}.bench.log").read_text()
 assert s.startswith("rc=1\n") and "FAIL " in s
 m=re.search(r"(\d+) checks: (\d+) PASS, (\d+) FAIL",s);assert m and int(m[3])>0
 if tag=="R7_latch_outside_valid": names=["rx_err in every gap between bytes: sync event","rx_err in every gap between bytes: no drop"]
 else:
  fields=["one drop","no event"]
  if tag in ("R1_latch_deleted","R2_latch_before_sof_clear"):fields+=["no later write"]
  names=[f"{t} rx_err at every byte: {field}" for t in ("sync","fu","pdreq","pdresp") for field in fields]
 for name in names: assert any(line.startswith("FAIL "+name+" ") for line in s.splitlines()),name
 print(tag+": caught by "+str(len(names))+" independently checked names; "+m[0])
s=(p/"receipts/probe/probe_head.tsv").read_text();assert "57 checks: 57 PASS, 0 FAIL" in s
print("Independent extended probe: 57 checks PASS (read tally, not exit code)")
s=(p/"receipts/equiv/equiv_tied.log").read_text();assert "749 are proven and 0 are unproven" in s
s=(p/"receipts/equiv/equiv_free.log").read_text();assert "748 are proven and 1 are unproven" in s and "bad_r_gold" in s
print("Independent parser equivalence: 749/749 tied; bad_r unproven when free")
s=(p/"receipts/bank_contract/result.csv").read_text();assert "24 checks: 12 PASS, 12 FAIL" in s
assert (p/"receipts/bank_contract/run.rc").read_text().strip()=="1"
print("Frozen no-write requirement: 12 directed failures; expected negative receipt rc=1")
print("Saved receipt audit: PASS")
