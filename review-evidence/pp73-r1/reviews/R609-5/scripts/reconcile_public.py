#!/usr/bin/env python3
"""Extract prior public findings only after the independent verdict is recorded."""
import json
from pathlib import Path
import subprocess

packet = Path(__file__).resolve().parents[1]
assert (packet / "receipts/independent-verdict.md").read_text().startswith("[R609] POSITIVE")
cache = packet / "scratch/pr174-comments.json"
cache.parent.mkdir(exist_ok=True)
if not cache.exists():
    pages = json.loads(subprocess.check_output(["gh", "api", "--paginate", "--slurp",
                      "repos/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/174/comments"]))
    cache.write_text(json.dumps([c for page in pages for c in page]))
comments = json.loads(cache.read_text())
boundaries = {
    6104874774: ("## 2. Findings", "## 3. Focus"),
    6104929075: ("## Findings", "## What holds"),
    6107310880: ("**R609-2-F1", "**Prior public"),
    6107318258: ("## Findings", "## Reviewer ledger"),
    6112257211: ("## Findings", "## Reviewer ledger"),
    6112326328: ("**Retained observations**", "**Public execution evidence"),
    6114429001: ("Retained observations have no unclean lens:", "Public execution evidence comes"),
    6114436395: ("## Findings", "## Reviewer ledger"),
}
excerpts = []
for ident, (begin, end) in boundaries.items():
    comment = next(c for c in comments if c["id"] == ident)
    body = comment["body"]
    first = body.index(begin)
    last = body.index(end, first)
    excerpts.append(dict(id=ident, url=comment["html_url"], findings=body[first:last]))
(packet / "receipts/prior-public-findings.json").write_text(json.dumps(excerpts, indent=2)+"\n")
for path in (packet / "receipts").glob("prior-comment-*.md"):
    path.rename(packet / "scratch" / path.name)
print(f"Saved public findings excerpts from {len(excerpts)} prior comments after independent verdict.")
