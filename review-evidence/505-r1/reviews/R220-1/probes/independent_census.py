"""R220 independent census: carrier run bodies vs CARRIER_STEP_LISTS records.

Reads the workflow YAML directly and re-implements the whitespace
normalization independently (LF split, backslash-newline joined, blank runs
collapsed, blank lines dropped) to cross-check the recorded constants.
"""
import sys, re, pathlib, importlib.util, yaml, json
root = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("ci_events", root / "scripts/ci_events.py")
ce = importlib.util.module_from_spec(spec); spec.loader.exec_module(ce)

def my_norm(text):
    text = text.replace("\\\n", "")
    out = []
    for raw in text.split("\n"):
        line = " ".join(w for w in re.split(r"[ \t]+", raw) if w)
        if line:
            out.append(line)
    return tuple(out)

carriers = {".github/workflows/docs.yml": ["docs-check", "wire-accountability", "docs-check-no-git"],
            ".github/workflows/elaborate.yml": ["elaborate"]}
total = 0; per = {}; problems = []; rows = []
for path, jids in carriers.items():
    wf = yaml.safe_load((root / path).read_text())
    for jid in jids:
        ss = wf["jobs"][jid]["steps"]
        recs = ce.CARRIER_STEP_LISTS[(path, jid)]
        if len(recs) != len(ss):
            problems.append(f"{jid}: {len(ss)} steps vs {len(recs)} records")
        n_run = 0
        for i, (s, r) in enumerate(zip(ss, recs), 1):
            if "run" in s:
                n_run += 1
                live = my_norm(s["run"])
                rec = r.get("run")
                ok = rec == live
                nflags = sum(bool(re.search(r" --(?:self-test|selftest|check)(?= |$)", l)) for l in live)
                rows.append((jid, i, s["name"], len(live), nflags, ok))
                if not ok:
                    problems.append(f"{jid} step {i} {s['name']}: record {rec!r} != live {live!r}")
                if s.get("name") != r.get("name"):
                    problems.append(f"{jid} step {i}: name mismatch")
            else:
                if "run" in r:
                    problems.append(f"{jid} step {i}: uses step but record has run")
        per[jid] = n_run; total += n_run
for row in rows:
    print("%-20s %2d %-70s lines=%d flaglines=%d match=%s" % row)
print("per carrier run bodies:", per, "total", total)
print("multi-command bodies:", sum(1 for r in rows if r[3] > 1),
      "bodies with a proof/check flag:", sum(1 for r in rows if r[4] > 0))
print("problems:", problems or "none")
