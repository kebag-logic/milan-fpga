"""Meta-mutants: each breaks one rule in memory; the self-test must fail on every one."""
import contextlib, io, sys
sys.path.insert(0, sys.argv[1])
import docs_inventory as d

orig = {name: getattr(d, name) for name in ("line_count", "locate", "cell", "status", "archive_evidence", "load_data", "audience_of", "describes_of")}
def broken_load(root, paths):
    v, j, f = orig["load_data"](root, paths)
    return v, j, f  # no validation beyond parsing: skip refusals
mutants = {
    "line count frozen": ("line_count", lambda text: 7),
    "locate always line 1": ("locate", lambda text, quote: 1),
    "em dash kept": ("cell", lambda text: " ".join(text.replace("|", "\\|").split())),
    "status always current": ("status", lambda text, path, judged, pf: ("current", "no recorded contradiction")),
    "archive successor dropped": ("archive_evidence", lambda text, path: "versioned archive under `docs/history/`"),
    "audience override ignored": ("audience_of", lambda text, path: d.first_match(d.AUDIENCES, path)),
    "describes empty": ("describes_of", lambda root, text, path: "--"),
}
bad = 0
for label, (name, repl) in mutants.items():
    setattr(d, name, repl)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        rc = d.selftest()
    setattr(d, name, orig[name])
    print(f"{label}: selftest rc={rc} {'KILLED' if rc != 0 else 'SURVIVED'}")
    bad += rc == 0
# refusal mutant: load_data that never refuses (wrap json parse only)
import json
def lax(root, paths):
    src = root / d.DATA
    try:
        data = json.loads(src.read_text())
    except ValueError:
        data = {}
    fs = [d.Finding(e.get("id",""), e.get("page",""), e.get("quote","") or "x", e.get("source",""), e.get("correction","")) for e in data.get("findings", [])]
    fs = [f for f in fs if f.page in set(paths)]
    return "x", {}, fs
d.load_data = lax
out = io.StringIO()
with contextlib.redirect_stdout(out):
    rc = d.selftest()
print(f"data refusals removed: selftest rc={rc} {'KILLED' if rc != 0 else 'SURVIVED'}")
bad += rc == 0
print("survivors:", bad)
sys.exit(1 if bad else 0)
