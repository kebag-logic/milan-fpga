#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""check_nvm_format_32x32.py - SAVED_STATE_FORMAT_32X32.md agrees with its figures (#823).

The page's numbers are recomputed by scripts/nvm_format_32x32.py from the
tree's definitions. This gate fails when any of them drifts:

  1. every generated block on the page equals the block rendered now;
  2. every inline figure on the page reads the value recomputed now;
  3. every block and inline key on the page is one the script computes;
  4. every cited token is on exactly one line of its file, so a line that
     moves keeps its citation true;
  5. the page cites every one of its prose anchors (tables.CITED) by token
     and file, and no line by its number in any form: `path:N`, a range
     `path:N-M`, a list `path:N,M`, each quoted or not, "`path` line N", or a
     link to `path#LN`;
  6. the documentation index links the page.

A generated block sits between `<!-- nvm-format: begin NAME -->` and
`<!-- nvm-format: end NAME -->`; an inline figure is
`<!-- fig:KEY -->VALUE<!-- /fig -->`.

usage:
    python3 scripts/check_nvm_format_32x32.py              # the gate
    python3 scripts/check_nvm_format_32x32.py --self-test  # one plant per check
    python3 scripts/check_nvm_format_32x32.py --write      # regenerate the page
"""

from __future__ import annotations

import argparse
import copy
import re
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import nvm_contract as contract  # noqa: E402
import nvm_format_32x32 as fmt  # noqa: E402
import nvm_format_32x32_tables as tables  # noqa: E402

PAGE = ROOT / "docs/design/SAVED_STATE_FORMAT_32X32.md"
INDEX = ROOT / "docs/README.md"
INDEX_LINK = "(design/SAVED_STATE_FORMAT_32X32.md)"
BLOCK_RE = re.compile(r"<!-- nvm-format: begin (\w+) -->\n(.*?)<!-- nvm-format: end \1 -->", re.S)
INLINE_RE = re.compile(r"<!-- fig:(\w+) -->(.*?)<!-- /fig -->")
#: a file name with its extension, as a citation gives it
_CITED_FILE = r"[\w./-]+\.[A-Za-z]\w*"
#: line numbers: one, a range or a list
_LINES = r"\d+(?:\s*[-,]\s*\d+)*"
#: a file cited by line number, which the next edit above the line makes false: `path:12`, a range `path:12-34` or
#: a list `path:12,34`, each quoted or not; "`path` line 12" or "lines 12-34"; or a link to `path#L12`
LINE_CITE_RE = re.compile(rf"{_CITED_FILE}:{_LINES}"
                          rf"|`{_CITED_FILE}` lines? {_LINES}"
                          rf"|{_CITED_FILE}#L\d+(?:-L?\d+)?")
#: the self-test's plants: a line-number citation of each form as the page would write it, and the whole
#: citation its finding must name
LINE_CITE_PLANTS = (
    ("`sw/litex/milan_soc.py:179`", "sw/litex/milan_soc.py:179"),
    ("`sw/litex/milan_soc.py:179-181`", "sw/litex/milan_soc.py:179-181"),
    ("`scripts/nvm_klj3.py:408,465`", "scripts/nvm_klj3.py:408,465"),
    ("sw/litex/milan_soc.py:179", "sw/litex/milan_soc.py:179"),
    ("`sw/litex/milan_soc.py` line 179", "`sw/litex/milan_soc.py` line 179"),
    ("[the map](../../sw/litex/milan_soc.py#L179)", "../../sw/litex/milan_soc.py#L179"),
)


def rendered(r: dict) -> tuple[dict[str, str], dict[str, str]]:
    """The blocks and the inline figures, as the page must carry them."""
    return (tables.blocks(r, fmt.POINTS, fmt.PROPOSAL, fmt.AREA_EST),
            fmt.figure_map(r))


def findings(page: str, index: str, r: dict, anchors: tuple,
             read: Callable[[tables.Anchor], str] = tables.tree_text) -> list[str]:
    """Every disagreement between the page, the tree (as `read` gives each cited file) and the figures."""
    try:
        want_blocks, want_figs = rendered(r)
    except RuntimeError as err:
        return [f"FINDING: the figures cannot be recomputed: {err}"]
    bad = []
    have = {m.group(1): m.group(2) for m in BLOCK_RE.finditer(page)}
    for name, text in want_blocks.items():
        if name not in have:
            bad.append(f"FINDING: block {name} is missing from the page")
        elif have[name] != text + "\n":
            bad.append(f"FINDING: block {name} drifted from the figures; regenerate it")
    bad += [f"FINDING: block {name} is not one the script renders"
            for name in have if name not in want_blocks]
    for m in INLINE_RE.finditer(page):
        key, value = m.group(1), m.group(2)
        if key not in want_figs:
            bad.append(f"FINDING: inline figure {key} is not a figure the script computes")
        elif value != want_figs[key]:
            bad.append(f"FINDING: inline figure {key} reads {value}, recomputed {want_figs[key]}")
    bad += [f"FINDING: anchor {a}" for a in tables.anchor_findings(anchors, read)]
    bad += [f"FINDING: the page cites {m.group(0)} by line number; cite a token the gate checks instead"
            for m in LINE_CITE_RE.finditer(page)]
    bad += [f"FINDING: the page no longer cites {tables.cited(a)}"
            for a in tables.CITED if tables.cited(a) not in page]
    if [tuple(b) for b in r["declared"]] != [tuple(b) for b in r["space"]["blocks"]]:
        bad.append("FINDING: the layout 3 declaration (nvm_layout3.h) is not the bound shape's derived space")
    if INDEX_LINK not in index:
        bad.append("FINDING: the docs index does not link the page")
    return bad


def regenerate(page: str, r: dict) -> str:
    """The page with every block and inline figure written from the figures."""
    want_blocks, want_figs = rendered(r)

    def block(m: re.Match) -> str:
        """One block, re-rendered when the script knows it."""
        name = m.group(1)
        body = want_blocks[name] + "\n" if name in want_blocks else m.group(2)
        return f"<!-- nvm-format: begin {name} -->\n{body}<!-- nvm-format: end {name} -->"

    def inline(m: re.Match) -> str:
        """One inline figure, re-rendered when the script knows it."""
        return f"<!-- fig:{m.group(1)} -->{want_figs.get(m.group(1), m.group(2))}<!-- /fig -->"

    return INLINE_RE.sub(inline, BLOCK_RE.sub(block, page))


def compute() -> dict:
    """Recompute every figure in a scratch directory."""
    with tempfile.TemporaryDirectory(prefix="nvm-format-check-") as tmp:
        return fmt.compute(Path(tmp))


# --------------------------------------------------------------- the plants --

def _plant_inline(page: str) -> str:
    """Change the first inline figure's value."""
    m = INLINE_RE.search(page)
    return page[:m.start(2)] + m.group(2) + "1" + page[m.end(2):]


def _plant_block(page: str) -> str:
    """Change one cell inside the record-space block."""
    m = BLOCK_RE.search(page, page.index("<!-- nvm-format: begin space -->"))
    body = m.group(2).replace("| NAME |", "| NAMES |", 1)
    return page[:m.start(2)] + body + page[m.end(2):]


def _plant_unknown(page: str) -> str:
    """Add an inline figure no script computes."""
    return page + "\n<!-- fig:no_such_figure -->1<!-- /fig -->\n"


def _plant_missing(page: str) -> str:
    """Delete the save-path block."""
    m = re.search(r"<!-- nvm-format: begin save -->.*?<!-- nvm-format: end save -->\n", page, re.S)
    return page[:m.start()] + page[m.end():]


PAGE_PLANTS = {
    "inline": (_plant_inline, "FINDING: inline figure"),
    "block": (_plant_block, "FINDING: block space drifted"),
    "unknown": (_plant_unknown, "FINDING: inline figure no_such_figure is not a figure"),
    "missing": (_plant_missing, "FINDING: block save is missing"),
}


def self_test() -> int:
    """Each plant must be caught with its finding; the clean tree must be clean."""
    page, index = PAGE.read_text(), INDEX.read_text()
    anchors = tables.LAYERS + tables.VERSION_CHAIN + tables.CITED
    r = compute()
    failed = 0

    def expect(name: str, got: list[str], want: str) -> None:
        """Record whether one plant produced its finding."""
        nonlocal failed
        hit = any(want in g for g in got)
        failed += not hit
        print(f"plant {name}: {'caught' if hit else 'NOT CAUGHT'} ({want})")

    clean = findings(page, index, r, anchors)
    failed += bool(clean)
    print(f"clean tree: {len(clean)} finding(s)")
    for line in clean:
        print("  " + line)
    for name, (plant, want) in PAGE_PLANTS.items():
        expect(name, findings(plant(page), index, r, anchors), want)
    gone = (tables.Anchor(**{**vars(anchors[0]), "token": anchors[0].token + " planted"}),) + anchors[1:]
    expect("anchor", findings(page, index, r, gone), "no longer carries")
    common = (tables.Anchor(**{**vars(anchors[0]), "token": "#define"}),) + anchors[1:]
    expect("anchor-unique", findings(page, index, r, common), "an anchor's token must be on one line")
    for written, named in LINE_CITE_PLANTS:
        expect(f"line-number {written}", findings(page + f"\nSee {written}.\n", index, r, anchors),
               f"cites {named} by line number")
    first = tables.cited(tables.CITED[0])
    expect("citation", findings(page.replace(first, "it"), index, r, anchors), "the page no longer cites")
    # the control: every cited file with 300 lines more above its first, as a merge may leave it
    shifted = findings(page, index, r, anchors, read=lambda a: "\n" * 300 + tables.tree_text(a))
    failed += bool(shifted)
    print(f"control moved-lines: {len(shifted)} finding(s)")
    expect("index", findings(page, index.replace(INDEX_LINK, "(design/X.md)"), r, anchors),
           "FINDING: the docs index does not link")
    moved_decl = copy.deepcopy(r)
    group, first, last, cap = moved_decl["declared"][-1]
    moved_decl["declared"][-1] = (group, first, last - 1, cap - 1)
    expect("declaration", findings(page, index, moved_decl, anchors), "FINDING: the layout 3 declaration")
    bent = copy.deepcopy(r)
    bent["rule"][("tdm8", 2)] += 1
    expect("rule", findings(page, index, bent, anchors), "is not one line in N")
    saved = contract.T_PP_MAX_MS
    contract.T_PP_MAX_MS = saved + 1
    try:
        moved_def = compute()
    finally:
        contract.T_PP_MAX_MS = saved
    expect("definition", findings(page, index, moved_def, anchors), "FINDING: block save drifted")
    print(f"self-test: {'PASS' if not failed else f'FAIL ({failed})'}")
    return int(bool(failed))


def main() -> int:
    """The gate, its self-test, or a regeneration of the page."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--self-test", action="store_true", help="run every plant")
    ap.add_argument("--write", action="store_true", help="regenerate the page's figures")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    r = compute()
    if args.write:
        PAGE.write_text(regenerate(PAGE.read_text(), r))
    bad = findings(PAGE.read_text(), INDEX.read_text(), r, tables.LAYERS + tables.VERSION_CHAIN + tables.CITED)
    for line in bad:
        print(line)
    print(f"{PAGE.relative_to(ROOT)}: {len(bad)} finding(s)")
    return int(bool(bad))


if __name__ == "__main__":
    raise SystemExit(main())
