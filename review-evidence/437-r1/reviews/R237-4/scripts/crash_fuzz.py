#!/usr/bin/env python3
"""Crash fuzz: run the head walk (blocks, headings, plan, generated_block)
over seeded random pages built from Markdown-significant fragments and
report any exception. Also reports the slowest page time.

Usage: crash_fuzz.py <head-scripts> <count> <seed>
"""
import random
import sys
import time
import traceback

sys.path.insert(0, sys.argv[1])
import gen_toc  # noqa: E402

FRAGMENTS = ["- ", "* ", "+ ", "1. ", "10) ", "> ", "[^1]: ", "[a]: /u", "[a]: <u>", "  ", "    ", "\t",
             "```", "~~~", "<div>", "</div>", "<span>", "</span>", "<pre>", "</pre>", "<!--", "-->",
             "<!-->", "<?x", "?>", "<!X", ">", "<![CDATA[", "]]>", "## Old", "# H", "text", "***", "---",
             "===", "|", "| a |", "\\", "`", "\"", "'", "(", ")", "[", "]", "<", "x", ""]


def page(rng: random.Random) -> str:
    lines = []
    for _ in range(rng.randint(1, 14)):
        lines.append("".join(rng.choice(FRAGMENTS) for _ in range(rng.randint(0, 4))))
    return "\n".join(lines) + "\n"


def main() -> int:
    count, seed = int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    worst, bad = 0.0, 0
    for i in range(count):
        p = page(rng)
        t = time.perf_counter()
        try:
            b = gen_toc.blocks(p)
            assert len(b) == len(p.split("\n")), "one label per line"
            gen_toc.headings(p)
            gen_toc.plan(p + "\n## A\n\n## B\n\n## C\n")
            gen_toc.generated_block(p, "x.md")
        except Exception:  # noqa: BLE001 - the fuzz reports every failure
            bad += 1
            if bad <= 5:
                print("EXCEPTION on", repr(p))
                traceback.print_exc()
        worst = max(worst, time.perf_counter() - t)
    print(f"pages {count} seed {seed}: exceptions {bad}, slowest page {worst * 1000:.1f} ms")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
