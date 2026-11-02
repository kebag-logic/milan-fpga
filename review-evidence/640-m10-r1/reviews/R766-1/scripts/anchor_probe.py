"""Check every #fragment link in the given pages against the page's rendered heading ids (cmark-gfm)."""
import re, sys, cmarkgfm, html5lib, os
def ids(path):
    html = cmarkgfm.github_flavored_markdown_to_html(open(path).read())
    doc = html5lib.parse(html, namespaceHTMLElements=False)
    out=set()
    for el in doc.iter():
        if el.tag in ("h1","h2","h3","h4","h5","h6"):
            t="".join(el.itertext()).strip().lower()
            t=re.sub(r"[^\w\- ]","",t).replace(" ","-")
            out.add(t)
    return out
bad=0
for page in sys.argv[1:]:
    own=ids(page); txt=open(page).read()
    for m in re.finditer(r"\]\(([^)\s]*)#([^)\s]+)\)", txt):
        tgt, frag = m.group(1), m.group(2)
        p = page if not tgt else os.path.normpath(os.path.join(os.path.dirname(page), tgt))
        if tgt.startswith("http"): continue
        if not os.path.exists(p): print("MISSING FILE", page, tgt); bad+=1; continue
        if frag not in ids(p): print("BAD", page, tgt+"#"+frag); bad+=1
    print("checked", page)
print("bad", bad); sys.exit(1 if bad else 0)
