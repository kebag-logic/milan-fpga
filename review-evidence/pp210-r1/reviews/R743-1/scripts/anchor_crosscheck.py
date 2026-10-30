#!/usr/bin/env python3
"""Cross-check every relative #anchor link of a checkout against an independent
approximation of GitHub's heading-id rule (rendered text: link text kept, code
ticks, emphasis markers and HTML dropped; lowercase; punctuation dropped; each
space one hyphen; duplicate headings get -1, -2 ...). Prints links that the
checkout's own checker accepts but the reference rejects, and the reverse.
usage: anchor_crosscheck.py <checkout>"""
import importlib.util, re, sys, unicodedata
from pathlib import Path
root = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("cl", root / "scripts/check-links.py")
cl = importlib.util.module_from_spec(spec); spec.loader.exec_module(cl)

def ref_slug(h):
    h = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", h)       # link -> its text
    h = re.sub(r"<[^>]+>", "", h)
    h = h.replace("`", "").replace("*", "")
    h = re.sub(r"(?<![\w])_([^_]+)_(?![\w])", r"\1", h)   # _emphasis_ only
    h = h.strip().lower()
    out = []
    for ch in h:
        cat = unicodedata.category(ch)
        if ch in "-_" or ch == " " or cat[0] in "LNM":
            out.append("-" if ch == " " else ch)
    return "".join(out)

def ref_anchors(p):
    body = p.read_text(encoding="utf-8")
    found = set(cl.EXPLICIT_ANCHOR.findall(body)); seen = {}
    for h in cl.HEADING.findall(cl.FENCED.sub("", body)):
        s = ref_slug(h); n = seen.get(s, 0); seen[s] = n + 1
        found.add(s if n == 0 else f"{s}-{n}")
    return found

new_only, ref_only, total = [], [], 0
for src in cl.md_files():
    body = cl.strip_code(src.read_text(encoding="utf-8"))
    for t in cl.LINK.findall(body):
        if t.startswith(("http://", "https://", "mailto:")) or "#" not in t: continue
        path, _, a = t.partition("#")
        tgt = src if not path else (src.parent / path).resolve()
        if not tgt.exists() or tgt.suffix != ".md": continue
        total += 1
        n = a in cl.anchors_of(tgt); r = a in ref_anchors(tgt)
        rel = src.relative_to(root)
        if n and not r: new_only.append(f"{rel} -> {t}")
        if r and not n: ref_only.append(f"{rel} -> {t}")
print(f"anchor links checked: {total}")
print(f"accepted by the checker, rejected by the reference: {len(new_only)}")
for x in new_only: print("  " + x)
print(f"accepted by the reference, rejected by the checker: {len(ref_only)}")
for x in ref_only: print("  " + x)
