import json,sys
from datetime import datetime as D
f=lambda s:D.fromisoformat(s.replace("Z","+00:00")) if s else None
d=json.load(open(sys.argv[1]))
want=sys.argv[2:]
for j in d["jobs"]:
    if want and j["name"] not in want: continue
    js,jc=f(j["started_at"]),f(j["completed_at"])
    print("==",j["name"],(jc-js).total_seconds())
    gate=0;ver=0
    for s in j["steps"]:
        a,b=f(s.get("started_at")),f(s.get("completed_at"))
        t=(b-a).total_seconds() if a and b else None
        n=s["name"]
        if t is not None and (n.startswith("Elaboration gates") or n.startswith("LiteX simulations") or "leg" in n.lower()): gate+=t
        if n.startswith("Build Verilator from source") and t: ver+=t
        print(f"  {s['number']:>3} {s['conclusion'] or '':<9} {t!s:>7} {n}")
    print(f"  gate-ish={gate} verilator={ver} setup={(jc-js).total_seconds()-gate-ver}")
