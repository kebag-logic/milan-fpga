#!/usr/bin/env python3
"""Check every relative link on the given pages: the target path exists in
the repository and any fragment is a heading anchor of the target, using
the repository's own gen_toc anchor algorithm. Run with the pinned markdown
environment. Usage: link_probe.py <repo> <page>..."""
import sys, re, importlib.util
from pathlib import Path
repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "scripts"))
spec = importlib.util.spec_from_file_location("gen_toc", repo / "scripts/gen_toc.py")
gt = importlib.util.module_from_spec(spec); sys.modules["gen_toc"] = gt; spec.loader.exec_module(gt)
LINK = re.compile(r"\]\(([^)\s]+)\)")
bad = ok = ext = 0
for p in sys.argv[2:]:
    page = repo / p
    text = page.read_text(encoding="utf-8")
    fenced = False
    for n, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            fenced = not fenced; continue
        if fenced:
            continue
        for m in LINK.finditer(line):
            t = m.group(1)
            if t.startswith(("http://", "https://", "mailto:")):
                ext += 1; continue
            path, _, frag = t.partition("#")
            tgt = page if not path else (page.parent / path).resolve()
            if not tgt.exists():
                bad += 1; print(f"MISSING {p}:{n}: {t}"); continue
            if frag:
                if tgt.suffix != ".md":
                    bad += 1; print(f"FRAG-ON-NON-MD {p}:{n}: {t}"); continue
                anchors = {a for _, _, a in gt.headings(tgt.read_text(encoding='utf-8'))}
                if frag not in anchors:
                    bad += 1; print(f"BAD-ANCHOR {p}:{n}: {t}"); continue
            ok += 1
print(f"relative links ok={ok} bad={bad}; external links not fetched={ext}")
sys.exit(1 if bad else 0)
