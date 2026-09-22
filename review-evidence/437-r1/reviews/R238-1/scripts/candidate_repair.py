#!/usr/bin/env python3
"""[R238] feasibility control only: is a repair of F1 and F2 reachable
without breaking a shipped arm or the tracked corpus?

This is NOT a proposed patch and prescribes no design. In a disposable
worktree of the scratch clone it applies two edits to scripts/gen_toc.py:
(F1) a line at or beyond a live item's content column while the item holds
its paragraph is read by `_opens` as paragraph continuation, so a lone tag
there opens no type-7 block; (F2) a dedented block quote or footnote
definition releases the item. It then runs both shipped self-tests, the
per-page corpus comparison against the base walk, and the renderer probes.
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_render as probes  # noqa: E402

OUT = probes.OUT
CLONE = OUT / "scratch" / "clone-head"
TREE = OUT / "scratch" / "candidate-repair"
EDITS = [
    ("            label, state, delim, tag = _opens(line, para, state)",
     "            held = (item_context and para == HELD\n"
     "                    and _indent_columns(line) >= item_context[0])\n"
     "            label, state, delim, tag = _opens(line, PARAGRAPH if held else para, state)"),
    ("    if para == HELD and after == HELD:\n        return after, context",
     "    if para == HELD and after == HELD and not (\n"
     "            BLOCK_QUOTE_RE.match(line) or FOOTNOTE_DEFINITION_RE.match(line)):\n"
     "        return after, context"),
]


def main() -> int:
    subprocess.run(["git", "-C", str(CLONE), "worktree", "remove", "--force", str(TREE)],
                   capture_output=True)
    subprocess.run(["git", "-C", str(CLONE), "worktree", "add", "-q", "--detach", str(TREE),
                    "65df1df50a80cd5f540a93d8f0cfabc97da3da75"], check=True)
    src = TREE / "scripts" / "gen_toc.py"
    text = src.read_text()
    for old, new in EDITS:
        assert text.count(old) == 1, old
        text = text.replace(old, new, 1)
    src.write_text(text)
    report = []
    for cmd in (["python3", "-B", "scripts/gen_toc.py", "--selftest"],
                ["python3", "-B", "scripts/check_em_dash.py", "--selftest"]):
        proc = subprocess.run(cmd, cwd=TREE, capture_output=True, text=True)
        tail = (proc.stdout + proc.stderr).strip().splitlines()
        fails = [l.strip() for l in tail if "FAIL [" in l or "GUARD" in l or l.startswith("  [")]
        report.append(f"{' '.join(cmd[2:])}: exit {proc.returncode}: {tail[-1]}")
        report += [f"    {f}" for f in fails[:20]]
    spec = importlib.util.spec_from_file_location("gen_toc_candidate_r238", src)
    cand = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cand)
    for tree in ("base", "head"):
        root = probes.SCRATCH / f"clone-{tree}"
        names = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "*.md"],
                               capture_output=True, text=True, check=True).stdout
        differ = []
        for rel in sorted(filter(None, names.split("\0"))):
            page = (root / rel).read_text()
            a = (probes.BASE.blocks(page), probes.BASE.headings(page))
            b = (cand.blocks(page), cand.headings(page))
            if a != b:
                differ.append(rel)
        report.append(f"corpus ({tree} tree): {len(differ)} page(s) classify differently "
                      f"from the base walk {differ[:5]}")
    rows = [json.loads(l) for l in (OUT / "receipts" / "probes.jsonl").read_text().splitlines()]
    tally = {}
    for row in rows:
        cand_heads = [h[1] for h in cand.headings(row["page"])]
        v = probes.verdict(cand_heads, row["github"])
        tally.setdefault(v.split(" ")[0], []).append(row["id"].split(" ")[0])
    for k, v in sorted(tally.items()):
        report.append(f"probes {k}: {len(v)} {' '.join(v)}")
    subprocess.run(["git", "-C", str(CLONE), "worktree", "remove", "--force", str(TREE)],
                   capture_output=True)
    (OUT / "receipts" / "candidate-repair.txt").write_text("\n".join(report) + "\n")
    print("\n".join(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
