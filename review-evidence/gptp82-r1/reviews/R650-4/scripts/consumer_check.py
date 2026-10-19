"""Check the author's parent consumer results against the manager's template.

usage: python3 -I consumer_check.py <pgates dir>
For each template command (ignoring the PATH/TMPDIR environment), require one
head result with the same argument tail, exit 0, and an existing log; print
the manager's 334e9fe6 exit codes beside them.
"""
import glob, json, sys
from pathlib import Path
d = Path(sys.argv[1])
tail = lambda c: [a for a in c if not a.startswith(("PATH=", "TMPDIR=", "VERILATOR_ROOT=")) and a != "env"]
tmpl = json.loads((d / "manager-334e9fe6/parent-consumer.json").read_text())
man = json.loads((d / "manager-334e9fe6/results.json").read_text())["results"]
head = []
for f in sorted(glob.glob(str(d / "head-acfef36b/consumer-head-*-results.json"))):
    j = json.loads(Path(f).read_text())
    assert j["gptp_processor"] == "acfef36b39283c3102ba5f6948fe1f8c8c494853", f
    head += [(j["parent_head"], r, Path(f).name.split("-results")[0]) for r in j["results"]]
print("template base", tmpl["base"], "commands", len(tmpl["commands"]))
ok = len(head) == len(tmpl["commands"])
for i, cmd in enumerate(tmpl["commands"], 1):
    hits = [(p, r, g) for p, r, g in head if tail(r["command"]) == tail(cmd)]
    mrc = [r.get("exit_code") for r in man if tail(r["command"]) == tail(cmd)]
    good = len(hits) == 1 and hits[0][1]["exit_code"] == 0 and (d / "head-acfef36b" / f"{hits[0][2]}-{hits[0][1]['log']}").is_file()
    ok &= good
    print(f"{i:2} {' '.join(tail(cmd)):45} head rc {[h[1]['exit_code'] for h in hits]} parent {[h[0][:8] for h in hits]} manager@334e9fe6 rc {mrc} {'OK' if good else 'BAD'}")
print("ALL 11 MATCH AND PASS" if ok else "MISMATCH")
