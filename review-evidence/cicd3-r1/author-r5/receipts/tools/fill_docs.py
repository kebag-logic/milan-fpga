#!/usr/bin/env python3
"""fill_docs.py LANE_ROOT W: set the worker count W in suite_shards.py and the docs' placeholders, and regenerate
CI_WORKFLOWS.md's Verilator rows and the sentences under them from the live dealer at W workers."""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
W = int(sys.argv[2])
ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen " \
       "seventeen eighteen nineteen".split()


def word(n):
    if n < 20:
        return ONES[n]
    tens = {2: "twenty", 3: "thirty"}[n // 10]
    return tens + ("-" + ONES[n % 10] if n % 10 else "")


def ordinal(n):
    w = word(n)
    head, _, last = w.rpartition("-")
    last = {"one": "first", "two": "second", "three": "third", "five": "fifth", "eight": "eighth",
            "nine": "ninth", "twelve": "twelfth"}.get(last, last + "th")
    if last.endswith("yth"):
        last = last[:-3] + "ieth"
    return (head + "-" if head else "") + last


shards = root / "scripts" / "suite_shards.py"
text = shards.read_text()
text = re.sub(r"WORKER_OVERHEAD_SECONDS = \(122,\) \* \d+", f"WORKER_OVERHEAD_SECONDS = (122,) * {W}", text)
text = text.replace("@ADDED@", f"adds {word(W - 19)} more").replace("@N@", str(W))
shards.write_text(text)

sys.path.insert(0, str(root / "scripts"))
import suite_shards as s  # noqa: E402

suites = s.expand_suites(s.sweep_suites(root / "tb" / "verilator"))
owners, load = s.balance(suites, W)
regular = load[:-1]
heavy = max(range(W - 1), key=lambda i: regular[i])
values = {"@WORD@": word(W), "@N@": str(W), "@LAST@": str(W - 1), "@REGWORD@": word(W - 1).capitalize(),
          "@MAXREG@": str(max(regular)), "@NTH@": ordinal(W)}
for name in ("docs/testing/CI_WORKFLOWS.md", "docs/testing/TESTING.md", "docs/testing/RUNNING_TESTS.md"):
    path = root / name
    doc = path.read_text()
    for key, value in values.items():
        doc = doc.replace(key, value)
    if name.endswith("CI_WORKFLOWS.md"):
        rows = [f"| `verilator-shards {i}/{W}` | {v} | {s.CI_BUDGET_SECONDS if i < W - 1 else 2160} | "
                f"{(s.CI_BUDGET_SECONDS if i < W - 1 else 2160) - v} |" for i, v in enumerate(load)]
        doc = re.sub(r"(\| `verilator-shards \d+/\d+` \| \d+ \| \d+ \| -?\d+ \|\n)+", "\n".join(rows) + "\n", doc)
        start = doc.index("Verilator figures already include their 122-second overhead allowance.")
        end = doc.index("Docs now projects at", start)
        mine = ", ".join(x for x in suites if owners[x] == heavy)
        doc = doc[:start] + (
            "Verilator figures already include their 122-second overhead allowance.\n"
            f"A regular worker's bound is #998's {s.CI_BUDGET_SECONDS}-second budget, below 60% of its\n"
            "45-minute limit; leg A's row is its own 60% bound.\n"
            f"The heaviest regular worker, {heavy}, carries {mine} at {regular[heavy]} seconds:\n"
            f"{s.CI_BUDGET_SECONDS - regular[heavy]} inside the budget and {1800 - regular[heavy]} inside 30 minutes, "
            "before downstream collection.\n"
            "The continuous media-clock exception remains explicit at 1530 seconds (#998).\n") + doc[end:]
    path.write_text(doc)
left = [str(p) for p in (root / "docs" / "testing").glob("*.md") if "@" in re.sub(r"`[^`]*`", "", p.read_text())
        and re.search(r"@[A-Z]+@", p.read_text())]
print(f"W={W}: max regular {max(regular)} on worker {heavy}; leg A {load[-1]}; placeholders left: {left or 'none'}")
