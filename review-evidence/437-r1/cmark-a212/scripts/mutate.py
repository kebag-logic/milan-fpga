"""Named mutations of the new walk, each applied to a scratch copy and scored by both shipped selftests."""
import json, re, shutil, subprocess, sys, tempfile
from pathlib import Path
REPO = Path(sys.argv[1]); PY = sys.argv[2]; OUT = Path(sys.argv[3])
ETREE = """import types as _t
    def _conv(e):
        n = _t.SimpleNamespace(nodeType=1, ELEMENT_NODE=1, TEXT_NODE=3, tagName=e.tag if isinstance(e.tag, str) else "",
                               getAttribute=lambda k, e=e: e.get(k) or "", childNodes=[])
        if e.text:
            n.childNodes.append(_t.SimpleNamespace(nodeType=3, ELEMENT_NODE=1, TEXT_NODE=3, data=e.text, childNodes=[]))
        for c in e:
            n.childNodes.append(_conv(c))
            if c.tail:
                n.childNodes.append(_t.SimpleNamespace(nodeType=3, ELEMENT_NODE=1, TEXT_NODE=3, data=c.tail, childNodes=[]))
        return n
    tree = _conv(bound.html5lib.parseFragment(html, treebuilder="etree", namespaceHTMLElements=False))
    out, stack = [], list(reversed(tree.childNodes))"""
M = [  # (id, property, file, old, new)
 ("M01", "a raw HTML block covers the lines of its literal", "gen_toc.py",
  'if node.kind == "html_block" or (node.kind == "code_block"\n                                     and not node.fenced):',
  'if node.kind == "never" or (node.kind == "code_block"\n                                     and not node.fenced):'),
 ("M02", "an indented code block covers the lines of its literal", "gen_toc.py",
  'if node.kind == "html_block" or (node.kind == "code_block"\n                                     and not node.fenced):',
  'if node.kind == "html_block":'),
 ("M03", "a fenced code block is FENCE, an indented one CODE", "gen_toc.py",
  '{"code_block": FENCE if node.fenced else CODE,', '{"code_block": CODE,'),
 ("M04", "a raw HTML comment block is COMMENT", "gen_toc.py",
  '"html_block": COMMENT if node.literal.lstrip(" ").startswith(\n                     "<!--") else HTML}', '"html_block": HTML}'),
 ("M05", "a block the HTML parse swallows is COMMENT", "gen_toc.py",
  "        if node.element and node.position not in shown:", "        if False:"),
 ("M06", "a paragraph in a tight list renders bare", "gen_toc_renderer.py",
  'and not bare))', '))'),
 ("M07", "every child of a list is an item element", "gen_toc_renderer.py",
  "node = _node(bound, child, bool(holder) or bool(", "node = _node(bound, child, bool("),
 ("M08", "positions are unquoted before the HTML parse", "gen_toc_renderer.py",
  "for element in _elements(bound, unquoted(html))", "for element in _elements(bound, html)"),
 ("M09", "the dom builder keeps foster-parented nodes", "gen_toc_renderer.py",
  'tree = bound.html5lib.parseFragment(html, treebuilder="dom",\n                                        namespaceHTMLElements=False)\n    out, stack = [], list(reversed(tree.childNodes))',
  ETREE),
 ("M10", "the HTML parse decides visibility", "gen_toc.py",
  "    shown = {position for _, position, _ in rendered.shown if position}",
  "    shown = {node.position for node in rendered.nodes}"),
 ("M11", "a lone carriage return ends a renderer line", "gen_toc.py",
  'if char == "\\n" or (char == "\\r" and text[at + 1:at + 2] != "\\n"):', 'if char == "\\n":'),
 ("M12", "an ATX closing run needs a blank before it", "gen_toc.py",
  "if body != rest and (not body or body[-1] in BLANK):", "if body != rest:"),
 ("M13", "an ATX label is read off its own line", "gen_toc.py",
  "        if node.last == node.first:\n", "        if False:\n"),
 ("M14", "a setext label keeps its line break", "gen_toc.py",
  "        raw = rendered_text\n", '        raw = " ".join(rendered_text.split())\n'),
 ("M15", "a label reads a line break as a space", "gen_toc.py",
  '.replace("*", r"\\*").replace("\\n", " ")', '.replace("*", r"\\*")'),
 ("M16", "a page spelling the position attribute renders nothing", "gen_toc_renderer.py",
  "    if POSITION in text:\n        return Rendered((), ())\n", ""),
 ("M17", "headings are listed in rendered order", "gen_toc.py",
  "    return tuple(labels), tuple(kinds), tuple(found)", "    return tuple(labels), tuple(kinds), tuple(sorted(found, key=lambda h: h[2]))"),
 ("M18", "a raw HTML heading is not listed", "gen_toc.py",
  "        if node is None or tag != f\"h{node.level}\":\n            continue",
  "        if node is None:\n            if tag in ('h1','h2','h3','h4','h5','h6'):\n                found.append((int(tag[1]), rendered_text, 0, rendered_text))\n            continue\n        if tag != f\"h{node.level}\":\n            continue"),
 ("M19", "the tag filter extension is attached", "gen_toc_renderer.py",
  'EXTENSIONS = ("table", "strikethrough", "autolink", "tagfilter", "tasklist")',
  'EXTENSIONS = ("table", "strikethrough", "autolink", "tasklist")'),
 ("M20", "the table extension is attached", "gen_toc_renderer.py",
  'EXTENSIONS = ("table", "strikethrough", "autolink", "tagfilter", "tasklist")',
  'EXTENSIONS = ("strikethrough", "autolink", "tagfilter", "tasklist")'),
 ("M21", "footnotes are on", "gen_toc_renderer.py",
  "| lib.CMARK_OPT_FOOTNOTES", ""),
 ("M22", "raw HTML is kept", "gen_toc_renderer.py",
  "options = (lib.CMARK_OPT_SOURCEPOS | lib.CMARK_OPT_UNSAFE", "options = (lib.CMARK_OPT_SOURCEPOS"),
 ("M23", "the bundled cmark-gfm release is checked", "gen_toc_renderer.py",
  "    if core != CMARK_GFM:", "    if False:"),
 ("M24", "each rendering release is checked", "gen_toc_renderer.py",
  "           if versions.get(name) != want]", "           if False]"),
 ("M25", "a hash counts only after its requirement", "gen_toc_renderer.py",
  'elif word.startswith("--hash=sha256:") and name in pins:', 'elif word.startswith("--hash=") and name in pins:'),
 ("M26", "a table's lines are table rows", "gen_toc.py",
  'kind = {"heading": HEADING_LINE, "table": TABLE_ROW}.get(node.kind)', 'kind = {"heading": HEADING_LINE}.get(node.kind)'),
 ("M27", "a heading's lines are heading lines", "gen_toc.py",
  'kind = {"heading": HEADING_LINE, "table": TABLE_ROW}.get(node.kind)', 'kind = {"table": TABLE_ROW}.get(node.kind)'),
 ("M28", "the element flag counts only rendered positions", "gen_toc_renderer.py",
  "element=element or kind in _OWN_ELEMENT)", "element=True)"),
 ("M29", "a recorded response is the bytes its hash names", "gen_toc_shapes.json",
  '"response_bytes": "<ul dir=\\"auto\\">\\n<li>\\n<p dir=\\"auto\\">item</p>', '"response_bytes": "<ul dir=\\"auto\\">\\n<li>\\n<p dir=\\"auto\\">itex</p>'),
 ("M30", "a recorded request asks for exactly its page", "gen_toc_shapes.json",
  '"page": "- item\\n\\n  text\\n<span>\\n## Old\\n</span>\\n\\n## Real\\n"', '"page": "- item\\n\\n  text\\n<span>\\n## Old\\n</span>\\n\\n## Real\\n\\n"'),
]
def run(root, script):
    p = subprocess.run([PY, "-B", str(root / "scripts" / script), "--selftest"], capture_output=True, text=True, cwd=root)
    names = re.findall(r"FAIL \[([^\]]+)\]", p.stdout) + re.findall(r"^\s+- \[([^\]]+)\]", p.stderr, re.M) + re.findall(r"GUARD (.*)", p.stdout)
    return p.returncode, names, (p.stdout + p.stderr)[-400:]
results = []
ONLY = set(sys.argv[4].split(",")) if len(sys.argv) > 4 else None
for mid, prop, fname, old, new in M:
    if ONLY and mid not in ONLY:
        continue
    with tempfile.TemporaryDirectory(prefix="a212mut.") as tmp:
        root = Path(tmp)
        shutil.copytree(REPO / "scripts", root / "scripts")
        shutil.copytree(REPO / "tools" / "markdown", root / "tools" / "markdown")
        f = root / "scripts" / fname
        src = f.read_text()
        if src.count(old) != 1 and not (fname.endswith(".json") and src.count(old)):
            results.append({"id": mid, "property": prop, "error": f"anchor occurs {src.count(old)} times"}); print(mid, "ANCHOR", src.count(old)); continue
        f.write_text(src.replace(old, new, 1))
        rc1, n1, t1 = run(root, "gen_toc.py")
        rc2, n2, t2 = run(root, "check_em_dash.py")
        results.append({"id": mid, "property": prop, "file": fname, "gen_toc_rc": rc1, "gen_toc_failing": n1, "em_dash_rc": rc2, "em_dash_failing": n2,
                        "tail": t1 if not n1 else ""})
        print(mid, prop, "| gen_toc rc", rc1, len(n1), "arms", n1[:3], "| em_dash rc", rc2, len(n2), n2[:2])
OUT.write_text(json.dumps(results, indent=1, ensure_ascii=False))
