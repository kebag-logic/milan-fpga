"""Compare CI_WORKFLOWS.md's verilator-shards k/17 rows with the selector self-test's head predictions.
usage: python3 -I doc_table.py <CI_WORKFLOWS.md> <selftest-output>"""
import re, sys
doc = dict((int(k), (int(a), int(b), int(c))) for k, a, b, c in re.findall(r"\| `verilator-shards (\d+)/17` \| (\d+) \| (\d+) \| (\d+) \|", open(sys.argv[1]).read()))
st = dict((int(k), (int(a), int(b))) for k, a, b in re.findall(r"head worker (\d+)/17 predicted (\d+) s \([\d.]+ min\), bound (\d+) s", open(sys.argv[2]).read()))
bad = [k for k in range(17) if k not in doc or k not in st or doc[k][:2] != st[k] or doc[k][2] != doc[k][1] - doc[k][0]]
for k in range(17): print(k, "doc", doc.get(k), "selftest", st.get(k))
print("rows", len(doc), "selftest", len(st), "mismatch", bad); print("DOC TABLE:", "PASS" if not bad and len(doc) == len(st) == 17 else "FAIL")
sys.exit(1 if bad else 0)
