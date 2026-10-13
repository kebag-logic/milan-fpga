"""Parse-only check that two edits to one Python module compose without interaction.

Given the module at the common base, at each side, and in the composed tree,
it parses (never imports or runs) each file with `ast`, takes every
top-level statement's source keyed by the name it binds, and reports:

  * the names each side changed (added, removed or rewritten) against the base;
  * whether the two changed sets are disjoint;
  * whether every composed definition equals the side that changed it, or the
    base where neither did;
  * which changed names of one side are referenced (as a bare name) inside the
    definitions the other side changed.

usage: python3 -I compose_independence.py BASE SIDE_A SIDE_B COMPOSED
Exit 0 only if the sets are disjoint, the composed file is exactly the union,
and no cross reference exists.
"""
import ast
import sys


def defs(path: str) -> dict[str, str]:
    text = open(path, encoding="utf-8").read()
    tree = ast.parse(text)
    out: dict[str, str] = {}
    for index, node in enumerate(tree.body):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            key = node.name
        elif isinstance(node, ast.Assign) and all(isinstance(t, ast.Name) for t in node.targets):
            key = ",".join(t.id for t in node.targets)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            key = node.target.id
        else:
            key = f"<stmt:{ast.get_source_segment(text, node)[:60]!r}>"
        segment = ast.get_source_segment(text, node)
        decorators = "".join(
            "@" + ast.get_source_segment(text, d) + "\n" for d in getattr(node, "decorator_list", [])
        )
        out[key] = decorators + segment
    return out


def names_in(source: str) -> set[str]:
    return {n.id for n in ast.walk(ast.parse(source)) if isinstance(n, ast.Name)} | {
        n.attr for n in ast.walk(ast.parse(source)) if isinstance(n, ast.Attribute)
    }


def changed(base: dict[str, str], side: dict[str, str]) -> set[str]:
    return {k for k in base.keys() | side.keys() if base.get(k) != side.get(k)}


def main() -> int:
    base, a, b, comp = (defs(p) for p in sys.argv[1:5])
    ca, cb = changed(base, a), changed(base, b)
    print(f"side A changed {len(ca)} top-level names; side B changed {len(cb)}: {sorted(cb)}")
    overlap = ca & cb
    print(f"overlap: {sorted(overlap) or 'none'}")
    mismatch = []
    for key in base.keys() | a.keys() | b.keys() | comp.keys():
        expected = a.get(key) if key in ca else b.get(key) if key in cb else base.get(key)
        if comp.get(key) != expected:
            mismatch.append(key)
    print(f"composed definitions differing from the union: {sorted(mismatch) or 'none'}")
    a_refs_b = sorted(k for k in ca if k in a and names_in(a[k]) & cb)
    b_refs_a = sorted(k for k in cb if k in b and names_in(b[k]) & ca)
    print(f"side A definitions naming a side-B change: "
          f"{[(k, sorted(names_in(a[k]) & cb)) for k in a_refs_b] or 'none'}")
    print(f"side B definitions naming a side-A change: "
          f"{[(k, sorted(names_in(b[k]) & ca)) for k in b_refs_a] or 'none'}")
    return 0 if not overlap and not mismatch and not a_refs_b and not b_refs_a else 1


if __name__ == "__main__":
    sys.exit(main())
