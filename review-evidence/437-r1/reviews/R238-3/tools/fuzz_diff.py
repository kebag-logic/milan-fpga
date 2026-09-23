#!/usr/bin/env python3
"""Seeded differential sweep: base walk against head walk against GitHub.

Usage: fuzz_diff.py <head-scripts> <base-scripts> <out-dir> <seed> <count> <render-cap> [same-cap]

Generates <count> pages from a container/HTML/fence/comment vocabulary with
column-0 ATX headings `## H<n>` (never inside a container, so family two's
omissions cannot enter), runs both walks locally, and renders on GitHub
every distinct page where the two walks differ (up to <render-cap>), plus
up to [same-cap] pages where they agree. Only headings spelled `H<n>` are
compared on GitHub's side, so a setext heading a line pair happens to form
is not scored.
"""
import json
import os
import random
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gfm  # noqa: E402

OPENERS = ["- item", "* item", "1. item", "10. item", "2. item", "-", "-   ", "> quote",
           "[^1]: note", "- > q", "> - q", "- [a]: /u", "[a]: /u", "-  item", " - item",
           "1) item", "- - x", "-     code"]
INNER = ["  text", "   text", "    text", " text", "\ttext", "lazy", "  > quote", "  - nested",
         "  <span>", "   <span>", "  </span>", "  <div>", "  <pre>", "  </pre>", "  ```", "   ~~~",
         "  <!--", "  -->", "  [b]: /v", "  <? x", "  <!DOCTYPE x", "    <span>", "    <!--",
         "  <div title='", "  <!-->"]
TOP = ["<span>", "</span>", "<div>", "</div>", "<pre>", "</pre>", "```", "~~~", "<!--", "-->",
       "<!-- c -->", "<? x", "?>", "<!DOCTYPE x", ">", "text `<!--` more", "text \\<!-- more",
       "<div title='", "'>", "text", "para", "<!-->", "<select>", "</select>", "|a|", "|-|"]
HEAD_RE = re.compile(r"^H\d+$")


VOCAB = os.environ.get("FUZZ_VOCAB", "full")
if VOCAB == "markdown":             # no HTML and no comment delimiter at all
    OPENERS = ["- item", "* item", "1. item", "10. item", "2. item", "-", "-   ", "> quote",
               "[^1]: note", "- > q", "> - q", "- [a]: /u", "[a]: /u", "-  item", " - item",
               "1) item", "- - x", "-     code", "2) z", "3. z"]
    INNER = ["  text", "   text", "    text", " text", "\ttext", "lazy", "  > quote",
             "  - nested", "  ```", "   ~~~", "    ```", "  [b]: /v", "  |a|", "  |-|", "     x",
             "  ***", "  # in", "   ---"]
    TOP = ["```", "~~~", "text", "para", "|a|", "|-|", "| a | b |", "|---|---|", "    x", "***",
           "---", "===", ">", "> x", "\tx", "[b]: /v", "[^2]: n", "  x"]


def page(rng: random.Random) -> str:
    lines, h = [], 0
    for _ in range(rng.randint(3, 9)):
        r = rng.random()
        if r < 0.22:
            lines.append(rng.choice(OPENERS))
        elif r < 0.50:
            lines.append(rng.choice(INNER))
        elif r < 0.72:
            lines.append(rng.choice(TOP))
        elif r < 0.86:
            lines.append("")
        else:
            h += 1
            lines.append(f"## H{h}")
    h += 1
    lines += ["", f"## H{h}"]
    return "\n".join(lines) + "\n"


def walk(scripts: str, rows: list, out: Path) -> list:
    src = out.with_suffix(".in.json")
    src.write_text(json.dumps(rows))
    subprocess.run([sys.executable, str(Path(__file__).with_name("walk.py")), scripts,
                    str(src), str(out)], check=True)
    src.unlink()
    rows = json.loads(out.read_text())
    out.unlink()
    return rows


def main() -> int:
    head, base, outdir = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    seed, count, cap = int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
    same_cap = int(sys.argv[7]) if len(sys.argv) > 7 else 0
    outdir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)
    pages = sorted({page(rng) for _ in range(count)})
    rows = [{"name": f"s{seed}-{i}", "page": p} for i, p in enumerate(pages)]
    hw = walk(head, rows, outdir / "head.json")
    bw = walk(base, rows, outdir / "base.json")
    differ = [(r, h["walk"], b["walk"]) for r, h, b in zip(rows, hw, bw) if h["walk"] != b["walk"]]
    same = [(r, h["walk"], b["walk"]) for r, h, b in zip(rows, hw, bw) if h["walk"] == b["walk"]]
    pick = random.Random(seed + 1)
    pick.shuffle(differ)
    pick.shuffle(same)
    chosen = differ[:cap] + same[:same_cap]
    receipts = gfm.render_all([r["page"] for r, _, _ in chosen], jobs=1)
    results = []
    for (r, h, b), rc in zip(chosen, receipts):
        gh = [x for x in rc["headings"] if HEAD_RE.match(x[1])]
        results.append({"name": r["name"], "page": r["page"], "github": gh, "head": h, "base": b,
                        "walks_differ": h != b, "head_agrees": h == gh, "base_agrees": b == gh,
                        "request_sha256": rc["request_sha256"], "response_sha256": rc["response_sha256"]})
    (outdir / f"results-{seed}.json").write_text(json.dumps(results, indent=1))
    tally = {}
    for x in results:
        key = ("differ" if x["walks_differ"] else "same",
               "head=gh" if x["head_agrees"] else "head!=gh",
               "base=gh" if x["base_agrees"] else "base!=gh")
        tally[" ".join(key)] = tally.get(" ".join(key), 0) + 1
    summary = [f"seed {seed}: {len(pages)} distinct pages, {len(differ)} where the walks differ, "
               f"{len(same)} where they agree; rendered {len(results)}"]
    summary += [f"  {k}: {v}" for k, v in sorted(tally.items())]
    (outdir / f"SUMMARY-{seed}.txt").write_text("\n".join(summary) + "\n")
    print("\n".join(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
