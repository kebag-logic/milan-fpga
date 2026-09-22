#!/usr/bin/env python3
"""[R238] bounded differential sweep: where do the base and head walks
disagree, and who does GitHub side with?

Pages are every sequence of 1 to 3 tokens below (and 4 tokens when the first
is a list item), followed by one of five probe suffixes. A page is DIVERGENT
when the base and head walks list different headings. A seeded, stratified
sample of divergent pages (by suffix) is rendered by GitHub (cached with the
probes) and each walk is scored against it; the feasibility-control walk from
candidate_repair.py is scored too, to test whether F1 and F2 account for
every head-only error in the sample.
"""
import importlib.util
import itertools
import json
import random
import subprocess
import sys
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_render as probes  # noqa: E402

TOKENS = ["- item", "1. item", "-", "- item\n  more", "text", " text", "  text",
          "   text", "    text", "lazy", "", "> quote", "[^1]: note", "---", "===",
          "  <span>", "   <span>", " <span>", "```\ncode\n```"]
ITEMS = TOKENS[:4]
SUFFIXES = {
    "S1 col-0 tag": "<span>\n## Old\n</span>\n\n## Real\n",
    "S2 col-2 tag": "  <span>\n## Old\n  </span>\n\n## Real\n",
    "S3 col-3 tag": "   <span>\n## Old\n   </span>\n\n## Real\n",
    "S4 col-2 tag, fence": "  <span>\n```\n\n## Old\n```\n\n## Real\n",
    "S5 col-0 tag, fence": "<span>\n```\n\n## Old\n```\n\n## Real\n",
}
PER_STRATUM = 18


def candidate_walk():
    """The feasibility-control walk, rebuilt from the head source in memory."""
    src = (probes.SCRATCH / "clone-head/scripts/gen_toc.py").read_text()
    edits = [
        ("            label, state, delim, tag = _opens(line, para, state)",
         "            held = (item_context and para == HELD\n"
         "                    and _indent_columns(line) >= item_context[0])\n"
         "            label, state, delim, tag = _opens(line, PARAGRAPH if held else para, state)"),
        ("    if para == HELD and after == HELD:\n        return after, context",
         "    if para == HELD and after == HELD and not (\n"
         "            BLOCK_QUOTE_RE.match(line) or FOOTNOTE_DEFINITION_RE.match(line)):\n"
         "        return after, context")]
    for old, new in edits:
        assert src.count(old) == 1
        src = src.replace(old, new, 1)
    path = probes.OUT / "scratch" / "gen_toc_candidate_inmemory.py"
    path.write_text(src)
    spec = importlib.util.spec_from_file_location("gen_toc_candidate_sweep", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def pages():
    for n in (1, 2, 3, 4):
        for seq in itertools.product(range(len(TOKENS)), repeat=n):
            if n == 4 and TOKENS[seq[0]] not in ITEMS:
                continue
            prefix = "\n".join(TOKENS[i] for i in seq)
            for key, suffix in SUFFIXES.items():
                yield key, seq, prefix + "\n" + suffix


def judge(item):
    key, seq, text = item
    b = [h[1] for h in probes.BASE.headings(text)]
    h = [h[1] for h in probes.HEAD.headings(text)]
    return (key, seq, text, b, h) if b != h else None


def main() -> int:
    with Pool(8) as pool:
        divergent = [r for r in pool.imap_unordered(judge, pages(), chunksize=2000) if r]
    total = sum(1 for _ in pages())
    by = {}
    for r in divergent:
        by.setdefault(r[0], []).append(r)
    rng = random.Random(238)
    cand = candidate_walk()
    cache = probes.load_cache()
    lines = [f"{total} pages walked, {len(divergent)} divergent (base != head)"]
    sample_rows = []
    for key in SUFFIXES:
        rows = sorted(by.get(key, []), key=lambda r: r[1])
        pick = rng.sample(rows, min(PER_STRATUM, len(rows)))
        score = {"head right": 0, "base right": 0, "neither": 0, "candidate right": 0}
        for _, seq, text, b, h in pick:
            shown = [s for _, s in probes.rendered_headings(probes.render(text, cache)["response"])]
            probe = [s for s in shown if s in ("Old", "Real")]
            hb = [x for x in b if x in ("Old", "Real")]
            hh = [x for x in h if x in ("Old", "Real")]
            hc = [x for x in (y[1] for y in cand.headings(text)) if x in ("Old", "Real")]
            who = "head right" if hh == probe else "base right" if hb == probe else "neither"
            score[who] += 1
            score["candidate right"] += hc == probe
            sample_rows.append({"stratum": key, "tokens": [TOKENS[i] for i in seq],
                                "page": text, "github": shown, "base": b, "head": h,
                                "candidate": [y[1] for y in cand.headings(text)], "who": who})
        lines.append(f"{key}: {len(rows)} divergent, sampled {len(pick)}: "
                     + ", ".join(f"{k} {v}" for k, v in score.items()))
    (probes.OUT / "receipts" / "sweep-sample.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in sample_rows) + "\n")
    (probes.OUT / "receipts" / "sweep.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
