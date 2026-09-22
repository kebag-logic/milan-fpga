#!/usr/bin/env python3
"""[R238] every prior arm input classified by the base walk and the head walk.

Loads the BASE revision's case tables (gen_toc_cases, gen_toc_closer_cases)
bound to the base walk, takes every arm's page text, and compares `blocks()`,
`line_kinds()`, `headings()`, `plan()` and `refusals()` under both walks.
Also reports the byte identity of the base->head case modules.
"""
import hashlib
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_render import BASE, HEAD, OUT, SCRATCH  # noqa: E402

base_scripts = SCRATCH / "clone-base" / "scripts"
sys.modules["gen_toc"] = BASE
sys.path.insert(0, str(base_scripts))
cases = importlib.import_module("gen_toc_cases")
closers = importlib.import_module("gen_toc_closer_cases")


def answers(walk, text: str) -> tuple:
    return (walk.blocks(text), walk.line_kinds(text), walk.headings(text),
            walk.plan(text), walk.refusals(text))


def main() -> int:
    families = {"walk": cases.walk_arms(), "tag": cases.tag_arms(),
                "guard": cases.guard_arms(), "heading": cases.heading_arms(),
                "predecessor": cases.predecessor_arms(),
                "provenance": cases.provenance_arms(),
                "refusal": cases.refusal_arms(), "I440": closers.closer_arms()}
    total = sum(len(v) for v in families.values())
    differ, pages = [], 0
    for fam, arms in families.items():
        for name, page, _ in arms:
            if not isinstance(page, str):
                continue
            pages += 1
            if answers(BASE, page) != answers(HEAD, page):
                differ.append(f"{fam}: {name}")
    same = {}
    for mod in ("gen_toc_cases.py", "gen_toc_closer_cases.py", "gen_toc_guards.py"):
        b = (SCRATCH / "clone-base/scripts" / mod).read_bytes()
        h = (SCRATCH / "clone-head/scripts" / mod).read_bytes()
        same[mod] = (hashlib.sha256(b).hexdigest()[:16], hashlib.sha256(h).hexdigest()[:16], b == h)
    lines = [f"prior arms: {total} in the base tables, {pages} arm page texts compared, "
             f"{len(differ)} classify differently under the head walk"]
    lines += [f"  DIFFER {d}" for d in differ]
    lines += [f"  {m}: base {s[0]} head {s[1]} identical={s[2]}" for m, s in same.items()]
    (OUT / "receipts" / "prior-arms.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
