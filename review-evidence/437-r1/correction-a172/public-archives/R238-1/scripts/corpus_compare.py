#!/usr/bin/env python3
"""[R238] acceptance 4: per-page classification, base walk vs head walk.

For every tracked `*.md` of a tree (the base tree and the head tree, each a
scratch checkout), dump under BOTH walks: `blocks()`, `line_kinds()`,
`headings()` with anchors, `plan()`, `generated_block()` for the page's
path, and `refusals()`. Print the page count, the digest of each dump and
every page that differs. Nothing is written outside receipts/.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_render import BASE, HEAD, OUT, SCRATCH  # noqa: E402


def dump(walk, rel: str, text: str) -> dict:
    return {"blocks": walk.blocks(text), "line_kinds": walk.line_kinds(text),
            "headings": walk.headings(text), "plan": walk.plan(text),
            "generated_block": walk.generated_block(text, rel),
            "owns": walk.owns(rel, text), "refusals": walk.refusals(text)}


def main() -> int:
    report = []
    for tree in ("base", "head"):
        root = SCRATCH / f"clone-{tree}"
        names = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "*.md"],
                               capture_output=True, text=True, check=True).stdout
        pages = sorted(filter(None, names.split("\0")))
        dumps = {"base": {}, "head": {}}
        for rel in pages:
            path = root / rel
            if not path.is_file():
                continue
            text = path.read_text()
            dumps["base"][rel] = dump(BASE, rel, text)
            dumps["head"][rel] = dump(HEAD, rel, text)
        digests = {w: hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest()
                   for w, d in dumps.items()}
        differ = [rel for rel in dumps["base"] if dumps["base"][rel] != dumps["head"][rel]]
        lines = sum(len(d["blocks"]) for d in dumps["base"].values())
        report.append(f"{tree} tree: {len(dumps['base'])} tracked Markdown pages, "
                      f"{lines} lines; base-walk dump sha256 {digests['base']}; "
                      f"head-walk dump sha256 {digests['head']}; pages differing: {len(differ)}")
        report += [f"  DIFFER {rel}" for rel in differ]
        (OUT / "receipts" / f"corpus-{tree}-tree.json").write_text(
            json.dumps({"digests": digests, "differ": differ,
                        "pages": sorted(dumps["base"])}, indent=1))
    (OUT / "receipts" / "corpus-compare.txt").write_text("\n".join(report) + "\n")
    print("\n".join(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
