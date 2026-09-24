#!/usr/bin/env python3
"""Reviewer mutation probe (R238-5) for PR #538 correction round 1.

Usage: python mutate.py <pristine-tree> <work-dir> <python> [ids...]

Each mutant is a copy of <pristine-tree> (an export of the head with its
index populated) with one exact textual replacement, asserted to match once.
It then runs `gen_toc.py --selftest` and `check_em_dash.py --selftest` and
records the exit codes and the arms that failed. A mutant is KILLED when
either self-test exits non-zero. Parallelism is left to the caller.
"""
import shutil
import subprocess
import sys
from pathlib import Path

R, C, T, S = ("scripts/gen_toc_renderer.py", "scripts/gen_toc.py",
              "scripts/gen_toc_shape_cases.py", "scripts/check_em_dash.py")

OLD_NODES = '''    api, ffi = bound.api, bound.node_ffi
    out = []
    stack = [(api.cmark_node_first_child(ffi.cast("cmark_node *", root)),
              "", False)]
    while stack:
        child, holder, bare = stack.pop()
        if child == ffi.NULL:
            continue
        stack.append((api.cmark_node_next(child), holder, bare))
        if api.cmark_node_get_type(child) & _CLASS != _BLOCK:
            continue
        node = _node(bound, child, bool(holder) or bool(
            ffi.string(api.cmark_node_get_type_string(child)) == b"paragraph"
            and not bare))
        out.append(node)
        if node.kind == "list":
            tight = api.cmark_node_get_list_tight(child)
            stack.append((api.cmark_node_first_child(child),
                          "tight" if tight else "loose", False))
        else:
            stack.append((api.cmark_node_first_child(child), "",
                          holder == "tight"))
    return out'''
RECURSIVE_NODES = '''    return _rec(bound, root)


def _rec(bound, parent, holder="", bare=False):
    api, ffi = bound.api, bound.node_ffi
    out = []
    child = api.cmark_node_first_child(ffi.cast("cmark_node *", parent))
    while child != ffi.NULL:
        if api.cmark_node_get_type(child) & _CLASS != _BLOCK:
            child = api.cmark_node_next(child)
            continue
        node = _node(bound, child, bool(holder) or bool(
            ffi.string(api.cmark_node_get_type_string(child)) == b"paragraph"
            and not bare))
        out.append(node)
        if node.kind == "list":
            tight = api.cmark_node_get_list_tight(child)
            out += _rec(bound, child, "tight" if tight else "loose")
        else:
            out += _rec(bound, child, bare=holder == "tight")
        child = api.cmark_node_next(child)
    return out'''

MUTANTS = {
    # F1: the forged-position guard.
    "M01-guard-case-sensitive (reverse mutant)":
        (R, "return POSITION.encode() in html.lower()",
         "return POSITION.encode() in html"),
    "M02-guard-back-to-raw-text-check":
        (R, "forged = spells_position(ffi.string(plain_ptr))",
         "forged = POSITION in text"),
    "M03-guard-removed":
        (R, "forged = spells_position(ffi.string(plain_ptr))",
         "forged = False"),
    "M04-guard-reads-positioned-html":
        (R, "forged = spells_position(ffi.string(plain_ptr))",
         "forged = spells_position(ffi.string(html_ptr))"),
    "M05-guard-lowercases-only-the-first-letter":
        (R, "return POSITION.encode() in html.lower()",
         "return POSITION.encode() in html.replace(b'D', b'd')"),
    # F1 naming half: refusals().
    "M06-refusal-case-sensitive":
        (C, "folded = line.translate(_ASCII_LOWER)", "folded = line"),
    "M07-refusal-attribute-dropped":
        (C, "at = folded.find(POSITION)\n", "at = -1\n"),
    "M08-refusal-first-occurrence-only":
        (C, "at = folded.find(POSITION, at + 1)", "at = -1"),
    "M09-refusal-str-lower":
        (C, "folded = line.translate(_ASCII_LOWER)", "folded = line.lower()"),
    "M10-refusal-note-drops-column-wording":
        (C, 'f"{name}:{n}: `{what}` at column {col} spells',
         'f"{name}:{n}: `{what}` spells'),
    # F2: depth and the stack.
    "M11-depth-check-removed":
        (R, "if deepest > DEEPEST:", "if False:"),
    "M12-depth-off-by-one":
        (R, "if deepest > DEEPEST:", "if deepest >= DEEPEST:"),
    "M13-depth-counts-from-zero":
        (R, "stack = [(node, 1) for node in reversed(tree.childNodes)]",
         "stack = [(node, 0) for node in reversed(tree.childNodes)]"),
    "M14-deepest-256":
        (R, "DEEPEST = 200", "DEEPEST = 256"),
    "M15-nodes-recursive-again":
        (R, OLD_NODES, RECURSIVE_NODES),
    # F1 fix-probe: heading tag matched to its level.
    "M16-heading-tag-level-unchecked":
        (C, 'if node is None or tag != f"h{node.level}":',
         "if node is None:"),
    # File-view arm machinery.
    "M17-file-view-anchor-ignored":
        (T, 'return all((level, " ".join(strip_md(raw).split()), anchor) in rest',
         'return all((level, " ".join(strip_md(raw).split())) in '
         '(h[:2] for h in rest)'),
    "M18-file-view-anchor-reader-blank":
        ("scripts/gen_toc_renderer.py",
         'out[-1] = out[-1][:2] + (element.getAttribute("href")[1:],)',
         "pass"),
    # R238-4 F2 / R237-5 F3 arms.
    "M19-strikethrough-dropped":
        (R, 'EXTENSIONS = ("table", "strikethrough", "autolink", "tagfilter", '
            '"tasklist")',
         'EXTENSIONS = ("table", "autolink", "tagfilter", "tasklist")'),
    "M20-own-element-list-dropped":
        (R, '_OWN_ELEMENT = ("block_quote", "list", "heading",',
         '_OWN_ELEMENT = ("block_quote", "heading",'),
    "M21-own-element-thematic-break-dropped":
        (R, '"code_block",\n                "thematic_break", "table")',
         '"code_block",\n                "table")'),
    "M25-own-element-block-quote-dropped":
        (R, '_OWN_ELEMENT = ("block_quote", "list",', '_OWN_ELEMENT = ("list",'),
    "M26-own-element-code-block-dropped":
        (R, '"heading", "code_block",\n', '"heading",\n'),
    "M27-own-element-table-dropped":
        (R, '"thematic_break", "table")', '"thematic_break")'),
    "M28-prior-external-fix-probe-lowered-text-guard":
        (R, "forged = spells_position(ffi.string(plain_ptr))",
         "forged = POSITION in text.lower()"),
    "M22-bind-version-check-skipped":
        (R, "    bad = verify(versions, core)\n    if bad:",
         "    bad = verify(versions, core)\n    if False:"),
    "M23-unquoted-skipped":
        (R, "elements, deepest = _elements(bound, unquoted(html))",
         "elements, deepest = _elements(bound, html)"),
    "M24-em-dash-shape-rows-skipped":
        (S, "shape_problems, shape_rows = shape_arms(sys.modules[__name__])",
         "shape_problems, shape_rows = [], 0"),
}


def run(pristine: Path, work: Path, python: str, mid: str) -> str:
    path, old, new = MUTANTS[mid]
    tree = work / mid.split(" ")[0]
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(pristine, tree, symlinks=True)
    target = tree / path
    text = target.read_text(encoding="utf-8")
    if text.count(old) != 1:
        return f"{mid}: INVALID (pattern matches {text.count(old)} times)"
    target.write_text(text.replace(old, new), encoding="utf-8")
    lines = [f"== {mid}: {path}"]
    killed = False
    for gate in ("scripts/gen_toc.py", "scripts/check_em_dash.py"):
        proc = subprocess.run([python, gate, "--selftest"], cwd=tree,
                              capture_output=True, text=True, timeout=3000)
        out = (proc.stdout + proc.stderr).splitlines()
        fails = [l.strip() for l in out
                 if "FAIL" in l or l.strip().startswith(("-", "[", "Trace",
                                                          "Recursion"))]
        killed |= proc.returncode != 0
        lines.append(f"  {gate} --selftest rc={proc.returncode}; "
                     f"{len(fails)} failing line(s)")
        lines += [f"    {l[:220]}" for l in fails[:6]]
        lines.append(f"    last: {out[-1][:220] if out else ''}")
    lines.insert(1, f"  VERDICT: {'KILLED' if killed else 'SURVIVED'}")
    shutil.rmtree(tree)
    return "\n".join(lines)


def main() -> int:
    pristine, work, python = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    ids = sys.argv[4:] or list(MUTANTS)
    work.mkdir(parents=True, exist_ok=True)
    for prefix in ids:
        mid = next(m for m in MUTANTS if m.startswith(prefix))
        print(run(pristine, work, python, mid), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
