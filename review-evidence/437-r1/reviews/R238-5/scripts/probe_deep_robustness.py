#!/usr/bin/env python3
"""Reviewer probe (R238-5): very deep pages are answered, not crashed on.

Usage: python probe_deep_robustness.py <repo-root>

Each page nests one construct far past DEEPEST and past CPython's default
recursion limit, with headings before and after. `headings()`,
`line_kinds()` and `refusals()` must each return (no exception), the
headings must be empty (the page renders nothing), and the time is printed.
"""
import sys
import time
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "scripts"))
from gen_toc import headings, line_kinds, refusals  # noqa: E402

PAGES = {
    "5000 block quotes": "## A\n\n" + ">" * 5000 + " x\n\n## B\n",
    "1000 list levels": "## A\n\n" + "".join("  " * i + "- a\n"
                                             for i in range(1000))
    + "\n## B\n",
    "3000 raw divs": "## A\n\n" + "<div>" * 3000 + "\n\n## B\n",
    "3000 nested emphasis": "## A\n\n" + "*a " * 3000 + "x" + " a*" * 3000
    + "\n\n## B\n",
    "2000 inline spans in one paragraph": "## A\n\n" + "<span>" * 2000
    + "x\n\n## B\n",
    # An ordered item may interrupt a paragraph only when it starts at 1,
    # so the markers are `1.`, each indented to its parent's content.
    "600 ordered-list levels": "## A\n\n" + "".join(
        "   " * i + "1. a\n" for i in range(600)) + "\n## B\n",
}


def main() -> int:
    bad = 0
    for name, page in PAGES.items():
        start = time.monotonic()
        try:
            listed = headings(page)
            kinds = line_kinds(page)
            refusals(page)
            ok = listed == []
            note = f"headings={listed} lines={len(kinds)}"
        except Exception as exc:  # the property under test is "no crash"
            ok, note = False, f"{type(exc).__name__}: {exc}"[:200]
        bad += not ok
        print(f"{'OK  ' if ok else 'FAIL'} {name}: {note} "
              f"({time.monotonic() - start:.1f}s)", flush=True)
    print(f"probe_deep_robustness: {len(PAGES) - bad}/{len(PAGES)} answered "
          f"with no heading")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
