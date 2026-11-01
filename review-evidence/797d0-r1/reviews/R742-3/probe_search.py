#!/usr/bin/env python3
"""Probe the inventory's cross-page search: an independent wider search of the real tree, and planted spellings.

Usage: python3 -I probe_search.py REPO
Reads the reviewed generator and its data; writes nothing to REPO.
"""
import importlib.util, json, re, subprocess, sys, unicodedata
from pathlib import Path
sys.dont_write_bytecode = True
repo = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("inv", repo / "scripts/docs_inventory.py")
inv = importlib.util.module_from_spec(spec); sys.modules["inv"] = inv; spec.loader.exec_module(inv)
tree = inv.listing(repo)
paths = inv.population(tree)
data = json.loads((repo / inv.DATA).read_text(encoding="utf-8"))
_, _, _, findings = inv.load_data(repo, paths)
texts = {p: "\n".join(inv.OWN_HEAD) if p == inv.OUTPUT else (repo / p).read_text(encoding="utf-8", errors="replace") for p in paths}
listed = set(subprocess.run(["git", "-C", str(repo), "ls-files"], capture_output=True, text=True).stdout.split("\n"))
own_pop = sorted({p for p in listed if p and (p.endswith(".md") or Path(p).name.upper().startswith("README")) and (repo / p).is_file()} | {inv.OUTPUT})
print("population independent==generator:", own_pop == paths, len(paths))
rows = {(f.ident, f.page) for f in findings} | {(f.ident, f.page) for f in inv.copies(findings, texts)}
print("recorded", len(findings), "rows", len(rows))

def wide(text):
    """A wider normal form than the generator's, for hunting misses only."""
    t = unicodedata.normalize("NFKC", text)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("–", "-").replace("—", "-").replace("‑", "-").replace("\\|", "|")
    t = re.sub(r"<[^>\n]+>", " ", t)
    out = []
    for line in t.split("\n"):
        line = re.sub(r"^[\s>]*(?:(?:[-*+]|\d+[.)])\s+)?[\s>]*", "", line)
        out.append(line)
    t = "\n".join(out)
    t = re.sub(r"[`*_~]", "", t)
    t = re.sub(r"\n\s*\n", " \x00 ", t)
    return " ".join(t.split()).casefold()
flats = {p: wide(t) for p, t in texts.items()}
print("\n# wider search: a statement the wider form finds on a page with no row of that finding")
miss = 0
for f in findings:
    for s in (f.quote, *f.also):
        n = wide(s)
        for p, flat in flats.items():
            if (f.ident, p) in rows or n not in flat:
                continue
            if not re.search(r"(?<!\w)" + re.escape(n) + r"(?!\w)", flat):
                continue
            held = [g.ident for g in findings if g.page == p]
            print(f"MISS? {f.ident} on {p}: {s[:70]!r} (page already holds {held[:4]})")
            miss += 1
print("wider-only hits:", miss)

print("\n# fragment search: the longest 6-word runs of each recorded statement on pages with no row")
frag = 0
for f in findings:
    words = wide(f.quote).split()
    if len(words) < 6: continue
    pages = set()
    for i in range(len(words) - 5):
        run = " ".join(words[i:i+6])
        for p, flat in flats.items():
            if (f.ident, p) not in rows and run in flat and not p.startswith("docs/history/"):
                pages.add(p)
    for p in sorted(pages):
        print(f"FRAG {f.ident} on {p}: {f.quote[:70]!r}"); frag += 1
print("fragment pages:", frag)

print("\n# planted spellings of a recorded statement, one page each, through the generator's own copies()")
st = "All five default to firmware."
base = inv.Finding("D0-X", "A.md", st, "src", "fix")
cases = {
 "exact": st, "upper": st.upper(), "wrapped": "All five\ndefault to firmware.",
 "quote wrapped": "> All five\n> default to firmware.", "list wrapped": "- All five\n  default to firmware.",
 "ordered list": "1. All five default\n   to firmware.", "bold": "**All five** default to firmware.",
 "code": "All five `default` to firmware.", "underscore emphasis whole": "_All five default to firmware._",
 "underscore emphasis word": "All five _default_ to firmware.", "link word": "All five [default](x.md) to firmware.",
 "list inside quote": "> - All five\n>   default to firmware.", "quote inside list": "- > All five\n  > default to firmware.",
 "nbsp": "All five default to firmware.", "table cell": "| a | All five default to firmware. | b |",
 "heading": "## All five default to firmware.", "inside fence": "```\nAll five default to firmware.\n```",
 "hard break": "All five  \ndefault to firmware.", "tilde strike": "~~All five default to firmware.~~",
 "html bold": "<b>All five</b> default to firmware.", "paren list": "1) All five\n2) default to firmware.",
 "control blank": "All five\n\ndefault to firmware.", "control longer word": "All five default to firmwares.",
}
for name, body in cases.items():
    got = inv.copies([base], {"A.md": st, "P.md": "# P\n\n" + body + "\n"})
    print(f"{name:28s} {'row' if got else 'NO ROW'}" + (f" line {inv.carried_line(inv.flatten('# P\n\n' + body + '\n'), st)}" if got else ""))
apost = inv.Finding("D0-Y", "A.md", "the page's own rule", "s", "c")
for name, body in {"straight": "the page's own rule", "curly apostrophe": "the page’s own rule"}.items():
    print(f"{name:28s} {'row' if inv.copies([apost], {'A.md': apost.quote, 'P.md': body}) else 'NO ROW'}")
