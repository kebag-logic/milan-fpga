#!/usr/bin/env python3
"""R273-8: the round-six delta (991d5965 -> 062e89ad) of PR #535.

1. EXECUTABLE SCOPE. Parse sw/builder/test_builder.py at the parent and at
   the head, delete from the head's lexer_corpus the one tuple whose label
   starts "a /*/ opener", and compare the two syntax trees (comments are not
   in the tree; docstrings and string constants are). Equal trees mean the
   only executable change is that row.
2. THE NEW ROW ON THE PINNED GCC. Its text is preprocessed by the pinned
   compiler (-E -P -std=gnu99, one file) and the kept declarations listed;
   they must equal the row's recorded answer ("a", "z").
3. DETECTION. The gate's own lexer corpus check and closure-table check are
   loaded unmodified (as new_cells_probe.py does, RV32 re-measure stubbed
   off) from the parent and from the head, intact and under two in-memory
   mutations of the block-comment closer search (written to disposable
   copies under <work>; the lane is never edited):
     closer-from-i+1  `raw.find(... "*/", i + 2)` -> `i + 1` (the author's
                      control): `/*/` closes itself
     closer-from-i+3  -> `i + 3`: a `*/` right after the opener is missed
   The question is whether the head catches what the parent did not.
usage: delta_probe.py <parent-repo-copy> <head-repo> <gcc> <work> <out.json>"""
import ast, json, re, subprocess, sys, tempfile, traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "round5"))
import lexer_extract_head as base  # noqa: E402
import r6_extract  # noqa: E402

EXTRA = {"assert_character_closure", "assert_lexer_matches_compiler",
         "assert_lexer_reads", "lexer_measured", "LEXER_PIN",
         "SUBSET_CHARACTER_PIN", "assert_directive_set_is_closed",
         "line_marker_re", "lexer_names", "c_identifier_re"}
SITE = '            stop = raw.find("\\n" if raw[i + 1] == "/" else "*/", i + 2)\n'
MUTATIONS = {
    "closer-from-i+1": [(SITE, SITE.replace("i + 2)", "i + 1)"))],
    "closer-from-i+3": [(SITE, SITE.replace("i + 2)", "i + 3)"))],
}
NEW_LABEL = "a /*/ opener does not close its own block comment"


def strip(tree):
    return ast.dump(tree, annotate_fields=True, include_attributes=False)


def scope(parent, head):
    p = ast.parse((parent / "sw/builder/test_builder.py").read_text("utf-8"))
    h = ast.parse((head / "sw/builder/test_builder.py").read_text("utf-8"))
    removed = []
    for node in ast.walk(h):
        if isinstance(node, ast.Tuple):
            keep = []
            for elt in node.elts:
                if isinstance(elt, ast.Tuple) and elt.elts and \
                        isinstance(elt.elts[0], ast.Constant) and \
                        elt.elts[0].value == NEW_LABEL:
                    removed.append(ast.literal_eval(elt))
                    continue
                keep.append(elt)
            node.elts = keep
    return {"removed_rows": removed, "trees_equal_without_row": strip(p) == strip(h)}


def gcc_keeps(gcc, text):
    with tempfile.TemporaryDirectory(prefix="r273-8-") as tmp:
        src = Path(tmp) / "t.c"
        src.write_text(text, encoding="utf-8")
        run = subprocess.run([gcc, "-E", "-P", "-std=gnu99", str(src)],
                             capture_output=True, text=True)
    kept = tuple(re.findall(r"\bint\s+(\w+)\s*;", run.stdout))
    return {"rc": run.returncode, "kept": kept,
            "stderr": run.stderr.replace(tmp, "<tmp>")[:300]}


def load(root):
    saved = set(base.NESTED)
    base.NESTED |= EXTRA
    try:
        ns, missing = r6_extract.load(root)
    finally:
        base.NESTED.clear(); base.NESTED |= saved
    ns["census_compiler"] = lambda: None
    ns["census_used"] = {}
    return ns


def run(fn):
    try:
        return {"ok": True, "said": str(fn())[:300]}
    except AssertionError as exc:
        return {"ok": False, "said": str(exc)[:500]}
    except Exception:
        return {"ok": False, "said": "ERROR " + traceback.format_exc()[-600:]}


def main():
    parent, head, gcc, work, out = (Path(a) for a in sys.argv[1:6])
    result = {"scope": scope(parent, head)}
    row = result["scope"]["removed_rows"][0]
    result["new_row_gcc"] = gcc_keeps(str(gcc), row[1])
    result["new_row_gcc"]["recorded"] = row[2]
    result["new_row_gcc"]["agrees"] = tuple(row[2]) == result["new_row_gcc"]["kept"]
    result["detection"] = {}
    for tag, root in (("parent", parent), ("head", head)):
        source = (root / "sw/builder/test_builder.py").read_text("utf-8")
        for name, patches in [("intact", [])] + list(MUTATIONS.items()):
            text = source
            for old, new in patches:
                assert text.count(old) == 1, (tag, name, text.count(old))
                text = text.replace(old, new)
            copy = work / f"{tag}-{name}"
            (copy / "sw/builder").mkdir(parents=True, exist_ok=True)
            (copy / "sw/builder/test_builder.py").write_text(text, "utf-8")
            ns = load(copy)
            reads = ns["lexer_readers"]["keeps"](row[1])
            cell = {"corpora": run(ns["assert_lexer_matches_compiler"]),
                    "closure": run(ns["assert_character_closure"]),
                    "readers_on_new_row": list(reads) if reads else reads}
            result["detection"][f"{tag}/{name}"] = cell
            print(f"{tag:6} {name:16} corpora={'PASS' if cell['corpora']['ok'] else 'FAIL'} "
                  f"closure={'PASS' if cell['closure']['ok'] else 'FAIL'} "
                  f"readers on the /*/ text keep {cell['readers_on_new_row']}")
            for key in ("corpora", "closure"):
                if not cell[key]["ok"]:
                    print(f"    {key}: {cell[key]['said'][:240]}")
    print("scope:", {k: v for k, v in result["scope"].items()})
    print("new row on the pinned GCC:", result["new_row_gcc"])
    out.write_text(json.dumps(result, indent=1, ensure_ascii=False, default=list))
    ok = result["scope"]["trees_equal_without_row"] and \
        len(result["scope"]["removed_rows"]) == 1 and result["new_row_gcc"]["agrees"]
    return 0 if ok else 1


sys.exit(main())
