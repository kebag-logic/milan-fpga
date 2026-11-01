#!/usr/bin/env python3
"""Plant copies of recorded statements in a disposable copy of the tree, and read the verdict of the generator under review.
Usage: python3 -I plant_probes.py COPY"""
import json, re, subprocess, sys
from pathlib import Path
copy = Path(sys.argv[1]); sys.path.insert(0, str(copy / "scripts"))
import docs_inventory as d
GEN = ["python3", "-I", "scripts/docs_inventory.py"]
def sh(*a):
    r = subprocess.run(a, cwd=copy, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr
def restore():
    sh("git", "reset", "-q", "--hard", "HEAD"); sh("git", "clean", "-qfd", "--", "docs", "scripts")
audit = lambda: (copy / d.OUTPUT).read_text(encoding="utf-8")
findings = json.loads((copy / d.DATA).read_text())["findings"]
# 1. every statement and spelling, wrapped and marked up, on one synthetic page: the generator's own search must find it.
objs = d.load_data(copy, [f["page"] for f in findings])[3]
bad = total = 0
for f in objs:
    for s in (f.quote, *f.also):
        words = s.split(); cut = max(1, len(words) // 2)
        for form in ("> " + " ".join(words[:cut]) + "\n> " + " ".join(words[cut:]) + "\n",
                     "- **" + " ".join(words[:cut]) + "**\n  " + " ".join(words[cut:]).upper() + "\n",
                     "| cell | " + " ".join(words) + " |\n"):
            total += 1
            got = d.copies([f], {f.page: "unrelated\n", "planted.md": "intro\n\n" + form})
            if not any(x.page == "planted.md" and x.ident == f.ident for x in got):
                bad += 1; print("  NOT FOUND", f.ident, repr(form)[:120])
print(f"every-statement plant: {total} planted forms over {len(objs)} findings, {bad} not found")
# 2. plants through the real gate, on a page the committed audit marks current.
line = next(l for l in audit().split("\n") if "| current |" in l and "docs/guides/" in l and "no recorded contradiction" in l)
target = re.search(r"\]\(([^)]+)\)", line).group(1); target = "docs/" + target
print("plant target:", target)
S = "The Mark II default places them on the bare-metal core."
Q = "ADP, ACMP, AECP, MAAP and SRP default to bare-metal firmware."
plants = [
 ("plain", S + "\n"), ("wrapped-blockquote", "> The Mark II default\n> places them on the bare-metal core.\n"),
 ("bold-and-code", "**The Mark II** default places `them` on the bare-metal core.\n"),
 ("table-cell", "| a | " + S + " | b |\n"), ("uppercase", S.upper() + "\n"),
 ("nbsp", S.replace(" ", " ") + "\n"), ("crlf-wrapped", "The Mark II default\r\nplaces them on the bare-metal core.\r\n"),
 ("list-wrapped", "- The Mark II default\n  places them on the bare-metal core.\n"),
 ("origin-quote-on-another-page", Q + "\n"),
 ("underscore-emphasis", "The __Mark II__ default places _them_ on the bare-metal core.\n"),
 ("link-in-statement", "The [Mark II](README.md) default places them on the bare-metal core.\n"),
 ("html-break", "The Mark II default<br>places them on the bare-metal core.\n"),
 ("html-bold", "The <b>Mark II</b> default places them on the bare-metal core.\n"),
 ("hard-break-backslash", "The Mark II default\\\nplaces them on the bare-metal core.\n"),
 ("paraphrase", "Mark II places these on the bare-metal core by default.\n"),
]
for name, text in plants:
    restore()
    path = copy / target
    path.write_text(path.read_text(encoding="utf-8") + "\n" + text, encoding="utf-8", newline="")
    rc, _ = sh(*GEN, "--check")
    sh(*GEN, "--write")
    rc2, _ = sh(*GEN, "--check")
    rows = [l for l in audit().split("\n") if l.startswith("| D0-") and f"]({target[5:]})" in l]
    state = next((re.findall(r"\| (current|stale) \|", l) for l in audit().split("\n") if l.startswith(f"| [{target}]")), [])
    print(f"{name}\tcheck rc={rc}\tafter --write rc={rc2}\trows={[r.split(' | ')[0][2:] for r in rows]}\tstatus={state}")
# 3. bad data: a spelling that normalises to nothing.
restore()
p = copy / d.DATA; j = json.loads(p.read_text()); j["findings"][0]["also"] = ["**"]; p.write_text(json.dumps(j))
rc, out = sh(*GEN, "--check"); print("also=['**']\tcheck rc", rc, out.strip().split("\n")[0][:120])
sh(*GEN, "--write"); print("   rows after --write:", sum(l.startswith("| D0-001 |") for l in audit().split("\n")), "D0-001 rows")
restore()
j = json.loads(p.read_text()); j["findings"][0]["also"] = ["the"]; p.write_text(json.dumps(j))
rc, out = sh(*GEN, "--write"); print("also=['the']\twrite rc", rc, "D0-001 rows", sum(l.startswith("| D0-001 |") for l in audit().split("\n")))
restore()
# 4. held-not-updated on the real tree.
print("restored:", sh("git", "status", "--short")[1].strip() or "clean")
