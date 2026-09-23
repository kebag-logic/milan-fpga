#!/usr/bin/env python3
"""Per-heading regression analysis of a compare.py / offline_compare.py result.

Usage: per_heading.py <result.json> <pages.json> <out.txt> [old=base] [new=head]
A heading line `## H<n>` is one unit. For each walk it is LISTED or not,
and GitHub RENDERS it or not. A NEW ESCAPE is a heading the new walk lists,
the old walk does not, and GitHub does not render: the exemption-granting
regression. A NEW WITHHOLD is one GitHub renders, the old walk lists and the
new walk does not. Each new escape is tagged with the constructs on the page
that can explain it (a tag is a hint for triage, not a proof).
"""
import collections
import json
import re
import sys

HINTS = [
    ("inline PI or CDATA carrying > then <!--",
     re.compile(r"^(?![ \t>]*(?:<\?|<!\[CDATA\[)).*\S.*(?:<\?p > <!--|CDATA\[ > <!--)", re.M)),
    ("raw HTML block of type 3 to 5",
     re.compile(r"^(?:[ \t>]|[-*+] |\d+[.)] )*(?:<\?|<!\[CDATA\[|<![A-Z])", re.M)),
    ("open quoted attribute value",
     re.compile(r"title=[\"']$|^[ \t>]*[\"']$|^[ \t>]*'>$", re.M)),
    ("link reference definition", re.compile(r"\[r\]: /u")),
]


def main() -> None:
    result = json.load(open(sys.argv[1]))
    pages = json.load(open(sys.argv[2]))
    out_path = sys.argv[3]
    old, new = (sys.argv[4:6] if len(sys.argv) > 5 else ("base", "head"))
    counts = collections.Counter()
    hint_counts = collections.Counter()
    lines = []
    for key, row in sorted(result.items()):
        text = pages[key]
        names = re.findall(r"^## (H\d+)$", text, re.M)
        rendered = {h[1] for h in row["rendered"]}
        listed_old = {h[1] for h in row[old]["listed"]}
        listed_new = {h[1] for h in row[new]["listed"]}
        for name in names:
            r, o, n = name in rendered, name in listed_old, name in listed_new
            if not r and n and not o:
                kind = "new escape"
            elif r and o and not n:
                kind = "new withhold"
            elif not r and o and not n:
                kind = "fixed escape"
            elif r and n and not o:
                kind = "fixed withhold"
            elif not r and o and n:
                kind = "shared escape"
            elif r and not o and not n:
                kind = "shared withhold"
            else:
                kind = "agree"
            counts[kind] += 1
            if kind in ("new escape", "new withhold"):
                hints = [h for h, rx in HINTS if rx.search(text)] or ["(none)"]
                if kind == "new escape":
                    hint_counts[" | ".join(hints)] += 1
                lines.append(f"{kind}: {key} {name} request {row['request_sha256']} hints {hints}")
    summary = [f"{k}: {v}" for k, v in sorted(counts.items())]
    summary += ["new-escape hint sets:"] + [f"  {v:4d}  {k}" for k, v in hint_counts.most_common()]
    open(out_path, "w").write("\n".join(summary + [""] + lines) + "\n")
    print("\n".join(summary))


if __name__ == "__main__":
    main()
