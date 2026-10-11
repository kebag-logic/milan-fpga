#!/usr/bin/env python3
"""Usage: python3 -I check_md_anchors.py <tree-root>

Resolves every local Markdown link that carries a #fragment against the
GitHub-style heading slugs of its target file. Also reports any line that
starts with a merge-conflict marker. Prints one line per link and exits 1 on
any unresolved fragment or conflict marker.
"""
import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
MARKER_RE = re.compile(r"^(<<<<<<<|=======$|>>>>>>>)")


def slugs(path: Path) -> set[str]:
    out: set[str] = set()
    seen: dict[str, int] = {}
    fence = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("```"):
            fence = not fence
        if fence or not line.startswith("#"):
            continue
        text = line.lstrip("#").strip()
        s = re.sub(r"[^\w\- ]", "", text.lower()).replace(" ", "-")
        n = seen.get(s, 0)
        seen[s] = n + 1
        out.add(s if n == 0 else f"{s}-{n}")
    return out


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    bad = 0
    files = sorted(p for p in root.rglob("*.md") if ".git" not in p.parts)
    for path in files:
        rel = path.relative_to(root)
        for no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if MARKER_RE.match(line):
                print(f"CONFLICT-MARKER {rel}:{no}")
                bad += 1
            for _label, raw in LINK_RE.findall(line):
                if "://" in raw or "#" not in raw:
                    continue
                target, frag = raw.split("#", 1)
                tpath = (path.parent / target).resolve() if target else path
                if tpath.suffix != ".md":
                    continue
                if not tpath.exists():
                    print(f"MISSING-FILE {rel}:{no} {raw}")
                    bad += 1
                    continue
                ok = frag in slugs(tpath)
                print(f"{'OK' if ok else 'BROKEN'} {rel}:{no} {raw}")
                bad += 0 if ok else 1
    print(f"unresolved={bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
