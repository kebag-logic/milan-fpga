#!/usr/bin/env python3
"""Judge each base/head line-label difference against GitHub's rendering.

Usage: judge_ac4_lines.py <repo> <tree-rev> <ac4-compare.json> <out.json> [mode]
For every page with a line_kinds difference (headings-only pages included),
the page at <tree-rev> is rendered by GitHub (`gh api POST markdown`, mode
default `markdown`, the file view). For each differing non-blank line a
distinctive fragment of its text is located in the parsed rendering, and the
element chain around it is reported: pre/code -> code, table cells -> table
row, heading -> heading, otherwise prose. The request/response bytes and
SHA-256 are kept. Requires html5lib (the PR's lock) for the DOM.
"""
import hashlib, json, re, subprocess, sys
from pathlib import Path
import html5lib

repo, rev, cmp_path, out = sys.argv[1], sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
mode = sys.argv[5] if len(sys.argv) > 5 else "markdown"
MAP = {"indented code line": "code", "fenced line": "code", "table row": "table row",
       "heading": "heading", "prose line": "prose", "commented line": "hidden", "raw HTML line": "raw html"}

def render(text):
    req = json.dumps({"context": "kebag-logic/milan-fpga", "mode": mode, "text": text}, separators=(",", ":"))
    r = subprocess.run(["gh", "api", "--method", "POST", "markdown", "--input", "-"],
                       input=req.encode(), capture_output=True, check=True, timeout=120)
    return req, r.stdout.decode()

def fragment(line):
    t = re.sub(r"[`*_>|\\\[\]()#-]", " ", line)
    words = [w for w in t.split() if len(w) > 2]
    best = max((" ".join(words[i:i + 3]) for i in range(max(1, len(words) - 2))), key=len, default="")
    return best

def chains(doc, frag):
    found = []
    def walk(node, anc):
        for ch in node.childNodes:
            if ch.nodeType == ch.TEXT_NODE:
                if frag and frag in " ".join(ch.data.split()):
                    found.append(anc)
            elif ch.nodeType == ch.ELEMENT_NODE:
                walk(ch, anc + [ch.tagName])
    walk(doc, [])
    return found

def classify(chain):
    if "pre" in chain: return "code"
    if "td" in chain or "th" in chain: return "table row"
    if any(t in chain for t in ("h1","h2","h3","h4","h5","h6")): return "heading"
    return "prose"

cmp = json.loads(cmp_path.read_text())
results = []
for e in cmp["pages"]:
    if "lines" not in e and "headings" not in e["fields"]:
        continue
    text = subprocess.run(["git", "-C", repo, "show", f"{rev}:{e['page']}"], capture_output=True, check=True).stdout.decode()
    req, resp = render(text)
    doc = html5lib.parseFragment(resp, treebuilder="dom", namespaceHTMLElements=False)
    lines = []
    for n, base_k, head_k, _ in e.get("lines", []):
        src = text.split("\n")[n - 1]
        if not src.strip():
            lines.append({"line": n, "base": base_k, "head": head_k, "blank": True}); continue
        frag = fragment(src)
        cs = chains(doc, frag)
        kinds = sorted({classify(c) for c in cs})
        verdict = ("head matches" if kinds == [MAP[head_k]] else
                   "base matches" if kinds == [MAP[base_k]] else f"ambiguous {kinds}")
        lines.append({"line": n, "base": base_k, "head": head_k, "fragment": frag,
                      "github": kinds, "chains": [c[-4:] for c in cs][:3], "verdict": verdict})
    results.append({"page": e["page"], "request_sha256": hashlib.sha256(req.encode()).hexdigest(),
                    "response_sha256": hashlib.sha256(resp.encode()).hexdigest(), "response_bytes": resp,
                    "lines": lines})
    tally = {}
    for l in lines:
        v = "blank" if l.get("blank") else l["verdict"]
        tally[v] = tally.get(v, 0) + 1
    print(e["page"], tally)
    for l in lines:
        if not l.get("blank") and l["verdict"] != "head matches":
            print("   ", l["line"], l["base"], "->", l["head"], "| github:", l["github"], "|", l["fragment"], l["chains"])
out.write_text(json.dumps({"mode": mode, "rev": rev, "pages": results}, indent=1))
