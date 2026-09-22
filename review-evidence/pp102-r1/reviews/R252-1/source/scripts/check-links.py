#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Check every relative markdown link and #anchor across the documentation."""
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"\]\(([^)\s]+)\)")
EXPLICIT_ANCHOR = re.compile(r'<a\s+id="([^"]+)"')
HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*$", re.M)
FENCED = re.compile(r"^```.*?^```", re.M | re.S)
INLINE_CODE = re.compile(r"`[^`\n]*`")


def strip_code(body: str) -> str:
    """Drop fenced blocks and inline code: links there are examples, not references."""
    return INLINE_CODE.sub("", FENCED.sub("", body))


def slug(text: str) -> str:
    """GitHub-style heading slug."""
    text = re.sub(r"`|\*|_", "", text.strip().lower())
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"\s+", "-", text).strip("-")


def anchors_of(path: Path) -> set:
    """Every `#fragment` one markdown file offers: explicit ids and heading slugs."""
    body = path.read_text(encoding="utf-8")
    found = set(EXPLICIT_ANCHOR.findall(body))
    for head in HEADING.findall(body):
        found.add(slug(head))
    return found


SKIP_DIRS = {".git", ".venv-wavedrom", "node_modules", "__pycache__"}


def md_files() -> list:
    """Every markdown file in the repository — docs/, the root, hdl/, tb/, syn/.

    The navigation is only coherent if the links OUT of the code trees are checked
    too: hdl/README.md and the tb/ suite notes point into docs/, and the guides
    point back at individual .sv modules.

    Sorted on the string form, not on `Path`: `Path` orders by path component,
    which puts `a/b.md` before `a-x/c.md`, and the failure list is read in the
    order a `find | sort` would produce it.
    """
    out = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith("obj_")]
        out += [Path(base) / f for f in files if f.endswith(".md")]
    return sorted(out, key=str)


def main() -> int:
    """Name every relative link with no target and every `#anchor` with no heading.

    A missing anchor is reported as loudly as a missing file because it fails
    the same way for a reader: the link resolves, the page opens, and it lands
    somewhere other than what the sentence promised.
    """
    cache, problems, checked = {}, [], 0
    for src in md_files():
        body = strip_code(src.read_text(encoding="utf-8"))
        for target in LINK.findall(body):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            checked += 1
            path, _, anchor = target.partition("#")
            resolved = src if not path else (src.parent / path).resolve()
            rel_src = src.relative_to(ROOT)
            if not resolved.exists():
                problems.append(f"{rel_src}: missing target -> {target}")
                continue
            if anchor and resolved.suffix == ".md":
                if resolved not in cache:
                    cache[resolved] = anchors_of(resolved)
                if anchor not in cache[resolved]:
                    problems.append(f"{rel_src}: missing anchor -> {target}")

    for line in problems:
        print(f"LINK FAIL: {line}")
    print(f"links: {checked} checked, "
          f"{'OK' if not problems else str(len(problems)) + ' FAILURES'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
