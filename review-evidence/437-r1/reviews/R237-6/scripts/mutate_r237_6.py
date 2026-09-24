#!/usr/bin/env python3
"""Reviewer mutation probe for the correction commit (PR #538, 26a0cc30).

Each mutant is one exact text replacement in a copy of the head's
`scripts/` + `tools/markdown/` tree (it must match exactly once). Both
self-tests run on the copy: `gen_toc.py --selftest` and
`check_em_dash.py --selftest`. A mutant is KILLED when either exits non-zero.
The named arms that failed are recorded.

Usage: mutate_r237_6.py PYTHON HEAD_TREE WORK_DIR OUT_JSON
"""
import concurrent.futures
import json
import shutil
import subprocess
import sys
from pathlib import Path

R, G, C, S, RC = ("scripts/gen_toc_renderer.py", "scripts/gen_toc.py",
                  "scripts/gen_toc_cases.py", "scripts/gen_toc_shape_cases.py",
                  "scripts/gen_toc_renderer_cases.py")

_KINDS = ("block_quote", "list", "heading", "code_block", "thematic_break",
          "table")
_OWN = ('_OWN_ELEMENT = ("block_quote", "list", "heading", "code_block",\n'
        '                "thematic_break", "table")\n')

MUTANTS = {
    # --- the forged-position guard (F1) ---
    "reverse: plain-HTML check case-sensitive":
        (R, "return POSITION.encode() in html.lower()",
         "return POSITION.encode() in html"),
    "plain-HTML check removed (never forged)":
        (R, "forged = spells_position(ffi.string(plain_ptr))",
         "forged = False"),
    "plain-HTML check reads the RAW TEXT again, case-sensitive (old guard)":
        (R, "forged = spells_position(ffi.string(plain_ptr))",
         "forged = POSITION in text"),
    "plain-HTML check reads the raw text, any case (no decoding)":
        (R, "forged = spells_position(ffi.string(plain_ptr))",
         "forged = spells_position(raw)"),
    "forged page keeps its nodes (only shown emptied)":
        (R, "    if forged:\n        return Rendered((), ())",
         "    if forged:\n        return Rendered(nodes, ())"),
    "refusals() case-sensitive":
        (G, "folded = line.translate(_ASCII_LOWER)", "folded = line"),
    "refusals() names no attribute":
        (G, "        at = folded.find(POSITION)\n",
         "        at = -1\n"),
    "refusals() names only the first spelling on a line":
        (G, "            at = folded.find(POSITION, at + 1)",
         "            at = -1"),
    "refusals() folds with str.lower()":
        (G, "folded = line.translate(_ASCII_LOWER)", "folded = line.lower()"),
    "refusal note for the attribute uses the character wording":
        (G, "if len(what) == 1 else", "if True else"),
    "both guards case-sensitive (plain-HTML check and refusals())":
        [(R, "return POSITION.encode() in html.lower()",
          "return POSITION.encode() in html"),
         (G, "folded = line.translate(_ASCII_LOWER)", "folded = line")],
    "tight-list paragraphs given an element (prior M03/M04 equivalent)":
        (R, '            stack.append((api.cmark_node_first_child(child), "",\n'
            '                          holder == "tight"))',
         '            stack.append((api.cmark_node_first_child(child), "",\n'
            '                          False))'),
    # --- depth (F2) ---
    "depth bound removed":
        (R, "    if deepest > DEEPEST:\n        return Rendered((), ())",
         "    if False:\n        return Rendered((), ())"),
    "depth bound off by one (>=)":
        (R, "if deepest > DEEPEST:", "if deepest >= DEEPEST:"),
    "depth bound raised to 255":
        (R, "DEEPEST = 200", "DEEPEST = 255"),
    "depth counts from 0":
        (R, "stack = [(node, 1) for node in reversed(tree.childNodes)]",
         "stack = [(node, 0) for node in reversed(tree.childNodes)]"),
    "syntax-tree walk recursive again":
        (R, "def _nodes(bound: SimpleNamespace, root: object) -> list[Node]:",
         "def _nodes(bound: SimpleNamespace, root: object) -> list[Node]:\n"
         "    import sys as _s\n"
         "    def _rec(n):\n"
         "        c = bound.api.cmark_node_first_child(n)\n"
         "        while c != bound.node_ffi.NULL:\n"
         "            _rec(c)\n"
         "            c = bound.api.cmark_node_next(c)\n"
         "    _rec(bound.node_ffi.cast('cmark_node *', root))"),
    "stack walk loses sibling order (children before next sibling swapped)":
        (R, "        stack.append((api.cmark_node_next(child), holder, bare))\n",
         ""),
    # --- own-element kinds (F3), one per kind ---
    **{f"own element drops {kind}":
       (R, _OWN, "_OWN_ELEMENT = " + repr(tuple(
           k for k in _KINDS if k != kind)) + "\n")
       for kind in _KINDS},
    # --- heading tag matched to level (R238-4 M17) ---
    "heading tag not matched to its level":
        (G, 'if node is None or tag != f"h{node.level}":',
         "if node is None:"),
    "heading tag matched to any heading tag":
        (G, 'if node is None or tag != f"h{node.level}":',
         'if node is None or tag not in ("h1","h2","h3","h4","h5","h6"):'),
    # --- bind() drift (R238-4 M15) ---
    "bind() ignores the release it is handed":
        (R, "            versions[name] = installed(name)",
         "            versions[name] = importlib.metadata.version(name)"),
    "verify() ignores cmarkgfm":
        (R, 'PINNED = {"cmarkgfm": "2025.10.22", "html5lib": "1.1"}',
         'PINNED = {"html5lib": "1.1"}'),
    # --- extensions (R238-4 M11, S3) ---
    "strikethrough extension dropped":
        (R, 'EXTENSIONS = ("table", "strikethrough", "autolink", "tagfilter", "tasklist")',
         'EXTENSIONS = ("table", "autolink", "tagfilter", "tasklist")'),
    "autolink extension dropped":
        (R, 'EXTENSIONS = ("table", "strikethrough", "autolink", "tagfilter", "tasklist")',
         'EXTENSIONS = ("table", "strikethrough", "tagfilter", "tasklist")'),
    "tasklist extension dropped":
        (R, 'EXTENSIONS = ("table", "strikethrough", "autolink", "tagfilter", "tasklist")',
         'EXTENSIONS = ("table", "strikethrough", "autolink", "tagfilter")'),
    # --- positions unquoted ---
    "positions left quoted":
        (R, "elements, deepest = _elements(bound, unquoted(html))",
         "elements, deepest = _elements(bound, html)"),
    # --- file-view anchor check (R238-4 F1 anchor requirement) ---
    "file-view check ignores anchors":
        (S, "return all((level, \" \".join(strip_md(raw).split()), anchor) in rest",
         "rest = iter((h[0], h[1], '') for h in rest)\n"
         "        return all((level, \" \".join(strip_md(raw).split()), '') in rest"),
    "file-view check allows any heading":
        (S, "return all((level, \" \".join(strip_md(raw).split()), anchor) in rest\n"
            "                   for level, raw, anchor in headings(text))",
         "return True"),
    "file-view permalink not read (anchors empty)":
        (R, "            out[-1] = out[-1][:2] + (element.getAttribute(\"href\")[1:],)",
         "            pass"),
}


def run_one(py: str, head: Path, work: Path, name: str, spec) -> dict:
    edits = spec if isinstance(spec, list) else [spec]
    d = work / f"m{abs(hash(name)) % 10**10}"
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(head, d)
    for path, old, new in edits:
        target = d / path
        src = target.read_text(encoding="utf-8")
        count = src.count(old)
        if count != 1:
            shutil.rmtree(d)
            return {"name": name, "applied": False, "matches": count}
        target.write_text(src.replace(old, new, 1), encoding="utf-8")
    out = {"name": name, "applied": True,
           "file": ", ".join(path for path, _, _ in edits)}
    for gate, argv in (("toc", ["scripts/gen_toc.py", "--selftest"]),
                       ("em_dash", ["scripts/check_em_dash.py", "--selftest"])):
        try:
            r = subprocess.run([py, *argv], cwd=d, capture_output=True,
                               text=True, timeout=900)
            text = r.stdout + r.stderr
            out[gate] = {"rc": r.returncode,
                         "fails": [l.strip() for l in text.splitlines()
                                   if "FAIL" in l or "GUARD" in l
                                   or l.strip().startswith("- ")][:12],
                         "tail": (text.strip().splitlines() or [""])[-1][:300]}
        except subprocess.TimeoutExpired:
            out[gate] = {"rc": "timeout"}
    out["killed"] = any(out[g]["rc"] != 0 for g in ("toc", "em_dash"))
    shutil.rmtree(d)
    return out


def main() -> int:
    py, head, work, dest = sys.argv[1:]
    work = Path(work)
    work.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        futures = [pool.submit(run_one, py, Path(head), work, n, s)
                   for n, s in MUTANTS.items()]
        results = [f.result() for f in futures]
    Path(dest).write_text(json.dumps(results, indent=1))
    for r in results:
        if not r["applied"]:
            print(f"NOT APPLIED ({r['matches']} matches): {r['name']}")
            continue
        state = "KILLED  " if r["killed"] else "SURVIVED"
        first = (r["toc"]["fails"] or r["em_dash"]["fails"] or [""])[0]
        print(f"{state} toc rc={r['toc']['rc']} em rc={r['em_dash']['rc']} "
              f"| {r['name']} | {first[:150]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
