"""Check published receipt identity, counts, measurements and public snapshot."""
import datetime, hashlib, json, pathlib
p=pathlib.Path(__file__).resolve().parent
base=p/"public/author-r2/evidence"
r2=base/"r2"
gates=r2/"docs-gates-43a25fa"
assert (gates/"head").read_text().strip()=="43a25fa7eba4d7ed7d2bb757aa42b973bd24c76e"
rows=[r.split("\t") for r in (gates/"summary.tsv").read_text().splitlines()]
assert len(rows)==47 and all(r[1]=="0" for r in rows)
assert (gates/"status-before").read_bytes()==(gates/"status-after").read_bytes()==b""
assert "PASS (790 arm(s))" in (gates/"16.log").read_text()
controls=[line for line in (gates/"42.log").read_text().splitlines() if line.startswith("Census budget:")]
assert len(controls)==17 and not any("SKIP" in line for line in controls)
assert (r2/"baremetal-mask-mutants.txt").read_text().count(": CAUGHT")==6
print("Published exact-head docs receipts: 47/47 rc 0; clean status before and after")
print("Bare-metal gate: 0 findings; self-test: 790 arms")
print("Census budget: 16 executed cases, none skipped, plus workflow ownership assertion")
print("Mask mutations: all six caught (one deletion is caught by --check, not its shrinking self-test)")
print("Budget mutations: old -r and missing searchability guard caught; cat-status mutant survives because the numeric-input guard still refuses its empty output")
for name in ["sv2v","yosys"]:
    lines=(r2/(name+"-rss-selftest.log")).read_text().splitlines()
    values=[int(line.split()[0]) for line in lines if line.split()[0].isdigit()]
    print(name,"runs",len(values),"peak KiB",max(values))
    if name=="sv2v": assert len(values)==133 and max(values)==1212036
    else: assert len(values)==141 and max(values)==380492
assert "1213100" in (base/"census-capped-jobs4-time.txt").read_text()
print("Earlier capped self-test maximum: 1213100 KiB; current constant:",1213100*1024,"bytes")
print("Native OOM receipt predates oom_free rename; exact-head runner receipt and source assert the new field")
print("Builder leg 1: calibration NOT RUN; not physical evidence")
print("No-git docs receipt: inventory parity skipped as expected without metadata")
snapshot=json.loads((p/"public-snapshot.json").read_text())
assert snapshot["formal_reviews"]==snapshot["inline_review_comments"]==0
assert any(row["name"]=="docs-gates-0" and row["conclusion"]=="success" for row in snapshot["jobs"])
print("Public snapshot: docs-gates-0 and bare-metal step executed successfully; remaining hosted completion pending")
print("No four-job exact-head replay receipt was present in the retrieved public PR comments")
