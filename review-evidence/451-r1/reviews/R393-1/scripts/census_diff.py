#!/usr/bin/env python3
"""Compare two AVDECC census JSONL files by (role, what), ignoring per-exchange
fields (seq, rtt_ms, t). Prints entries whose status or payload differ.
Usage: census_diff.py <before.jsonl> <after.jsonl>"""
import json, sys
def load(p):
    out = {}
    for line in open(p):
        r = json.loads(line)
        if "response" not in r: continue
        key = (r.get("role"), r.get("what"))
        resp = {k: v for k, v in r["response"].items() if k not in ("seq", "rtt_ms")}
        out.setdefault(key, []).append(resp)
    return out
a, b = load(sys.argv[1]), load(sys.argv[2])
keys = sorted(set(a) | set(b), key=str)
diff = [k for k in keys if a.get(k) != b.get(k)]
print(json.dumps({"entries_before": len(a), "entries_after": len(b), "differing": len(diff),
                  "details": [{"key": list(k), "before": a.get(k), "after": b.get(k)} for k in diff]}, indent=1))
