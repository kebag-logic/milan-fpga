import json, subprocess, sys
def load(c):
    return json.loads(subprocess.check_output(["git","show",f"{c}:scripts/docs_inventory.json"]))
a, b = load(sys.argv[1]), load(sys.argv[2])
def walk(o, path=""):
    # find list of dicts with 'id'
    if isinstance(o, dict):
        for k,v in o.items(): yield from walk(v, path+"/"+k)
    elif isinstance(o, list) and o and isinstance(o[0], dict) and "id" in o[0]:
        yield path, o
la = dict(walk(a)); lb = dict(walk(b))
print("lists:", list(la), list(lb))
for p in la:
    ia = [e["id"] for e in la[p]]; ib = [e["id"] for e in lb.get(p, [])]
    print(p, "before", len(ia), "after", len(ib))
    print(" removed:", sorted(set(ia)-set(ib)), "added:", sorted(set(ib)-set(ia)))
    rest_a = [e for e in la[p] if e["id"] in set(ib)]
    print(" surviving entries byte-identical:", rest_a == lb[p])
    for e in lb[p]:
        if e["id"] in ("D0-040","D0-057"): print(" ", json.dumps(e)[:400])
# other keys identical
def strip(o):
    o = json.loads(json.dumps(o))
    for p in la:
        cur=o
        for k in p.strip("/").split("/")[:-1]: cur=cur[k]
        cur[p.strip("/").split("/")[-1]] = None
    return o
print("non-entry content identical:", strip(a)==strip(b))
