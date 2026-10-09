#!/usr/bin/env python3
"""Round-2f cross-checks: policy equality, gate verdict replay, input-file binding.

Usage: python3 -I -B check_2f_policy_inputs.py <clone> <receipts-dir> <dev-sha> <merge-sha> <head-sha>
"""
import hashlib, importlib.util, json, subprocess, sys
from pathlib import Path

clone, rec, dev, merge, head = Path(sys.argv[1]), Path(sys.argv[2]), *sys.argv[3:6]
sys.path.insert(0, str(clone / "syn/ooc"))
spec = importlib.util.spec_from_file_location("gate", clone / "syn/ooc/pp_resource_gate.py")
gate = importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)
show = lambda rev, path: subprocess.run(["git", "-C", str(clone), "show", f"{rev}:{path}"],
                                        capture_output=True, check=True).stdout
base = json.loads(show(dev, "syn/ooc/pp_resource_baseline.json"))
mrg = json.loads(show(merge, "syn/ooc/pp_resource_baseline.json"))
cur = json.loads(show(head, "syn/ooc/pp_resource_baseline.json"))
fails = 0
def check(label, ok):
    global fails
    fails += not ok
    print(("OK   " if ok else "FAIL ") + label)

check("merge-result records == dev records (merge did not touch the JSON)", mrg == base)
check("endpoint set unchanged", set(base["endpoints"]) == set(cur["endpoints"]))
for name in base["endpoints"]:
    b, c = base["endpoints"][name], cur["endpoints"][name]
    pol = {k: v for k, v in b.items() if k not in ("record", "measured")}
    polc = {k: v for k, v in c.items() if k not in ("record", "measured")}
    check(f"{name}: every non-record field (tolerance/floor/ceiling/notes) unchanged: keys {sorted(pol)}", pol == polc)
    check(f"{name}: record identity unchanged vs dev", b["record"]["identity"] == c["record"]["identity"])
    published = json.loads((rec / "commands" / f"record-{name}.log").read_text())
    unrouted = [] if published["kind"] == "route" else None
    status, lines = gate.judge(b, published, unrouted)
    logged = (rec / "commands" / f"check-{name}.log").read_text().splitlines()[1:]
    check(f"{name}: judge(dev record, published record) replays check log exactly (status {status})",
          status == 0 and lines == logged)
top = {k: v for k, v in base.items() if k != "endpoints"}
topc = {k: v for k, v in cur.items() if k != "endpoints"}
check("top-level JSON fields unchanged", top == topc)

# Input binding: every repository file the measurement read hashes to the merge and head blobs.
for cfg in ("ax7101", "ax8x8", "ooc-1x1", "ooc-8x8"):
    data = json.loads((rec / f"{cfg}-inputs-before.json").read_text())
    files = data["files"]; n_repo = n_ok = 0; other = []
    for f in files:
        p = f["path"]
        if p.startswith("$LANES/645-ring-slip/"):
            rel = p.removeprefix("$LANES/645-ring-slip/")
            n_repo += 1
            try:
                blob_m = show(merge, rel); blob_h = show(head, rel)
            except subprocess.CalledProcessError:
                # submodule path: resolve through the gitlink
                parts = rel.split("/", 1)
                if parts[0] in ("protocol-processor", "third_party") or True:
                    sub = None
                    for cand in ("protocol-processor", "gptp-processor", "third_party/lwSRP", "third_party/verilog-axis"):
                        if rel.startswith(cand + "/"):
                            sub = cand
                    if sub is None:
                        other.append(rel); continue
                    gl = subprocess.run(["git", "-C", str(clone), "rev-parse", f"{merge}:{sub}"], capture_output=True, text=True).stdout.strip()
                    glh = subprocess.run(["git", "-C", str(clone), "rev-parse", f"{head}:{sub}"], capture_output=True, text=True).stdout.strip()
                    inner = rel.removeprefix(sub + "/")
                    r = subprocess.run(["git", "-C", str(clone / sub), "show", f"{gl}:{inner}"], capture_output=True)
                    if r.returncode or gl != glh:
                        other.append(rel); continue
                    blob_m = blob_h = r.stdout
            if hashlib.sha256(blob_m).hexdigest() == f["sha256"] == hashlib.sha256(blob_h).hexdigest():
                n_ok += 1
            else:
                other.append(rel)
        else:
            other.append(p)
    print(f"{cfg}: {n_ok}/{n_repo} repository inputs equal merge and head blobs; not bound by git: {len(other)}")
    for o in other:
        print(f"   unbound: {o}")
    check(f"{cfg}: every repository input matches", n_ok == n_repo and all(o.startswith("$") for o in other))
print("RESULT:", "PASS" if not fails else f"FAIL ({fails})")
sys.exit(1 if fails else 0)
