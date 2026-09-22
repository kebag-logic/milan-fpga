#!/usr/bin/env python3
"""[R238] acceptance 1 completeness: is any family-one-like shape still
invented by BOTH walks (so the change would not have reached it)?

Within the sweep's universe, take pages ending in the column-0 tag suffix
where the base and head walks AGREE and both list `Old`, and whose prefix
holds a list item, then a blank token, then an indented text token (the
family's precondition). A seeded sample is rendered (cached with the probes);
a row GitHub renders without `Old` would be an unfixed family-one member.
"""
import itertools
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_render as probes  # noqa: E402
from sweep import ITEMS, SUFFIXES, TOKENS  # noqa: E402

INDENTED = {" text", "  text", "   text", "    text"}
SAMPLE = 40


def candidates():
    suffix = SUFFIXES["S1 col-0 tag"]
    for n in (3, 4):
        for seq in itertools.product(range(len(TOKENS)), repeat=n):
            toks = [TOKENS[i] for i in seq]
            if toks[0] not in ITEMS:
                continue
            try:
                blank = toks.index("", 1)
            except ValueError:
                continue
            if not any(t in INDENTED for t in toks[blank + 1:]):
                continue
            text = "\n".join(toks) + "\n" + suffix
            b = [h[1] for h in probes.BASE.headings(text)]
            h = [h[1] for h in probes.HEAD.headings(text)]
            if b == h and "Old" in h:
                yield toks, text


def main() -> int:
    pool = list(candidates())
    pick = random.Random(437).sample(pool, min(SAMPLE, len(pool)))
    cache = probes.load_cache()
    hidden = []
    for toks, text in pick:
        shown = [s for _, s in probes.rendered_headings(probes.render(text, cache)["response"])]
        if "Old" not in shown:
            hidden.append((toks, shown))
    lines = [f"{len(pool)} candidate pages where both walks list Old after an item, a blank and "
             f"indented text; sampled {len(pick)}; GitHub hides Old in {len(hidden)}"]
    lines += [f"  UNFIXED {json.dumps(t)} GitHub {s}" for t, s in hidden]
    (probes.OUT / "receipts" / "unfixed-family-one.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
