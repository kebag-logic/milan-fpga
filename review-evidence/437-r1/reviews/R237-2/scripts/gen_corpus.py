#!/usr/bin/env python3
"""R237-2 combinatorial corpus: container prefix x tag line x follower x tail.

Writes every page as {"name", "page"} JSON to stdout. Deterministic.
"""
import json

F = "```"
PREFIXES = {
    "bullet": "- item",
    "bullet resumed": "- item\n\n  text",
    "ordered": "1. item",
    "ordered resumed": "1. item\n\n   text",
    "two-digit resumed": "10. item\n\n    text",
    "nested quote": "- item\n  > quote",
    "resumed nested quote": "- item\n\n  > quote",
    "quote-first item": "- > quote",
    "nested bullet": "- item\n  - nested",
    "nested ordered": "- item\n  1. nested",
    "nested bullet resumed": "- item\n  - nested\n\n    text",
    "nested footnote": "- item\n  [^1]: note",
    "table in item": "- item\n\n  | a |\n  | - |",
    "table rows in item": "- item\n\n  | a |\n  | - |\n  | b |",
    "thematic in item": "- item\n  ***",
    "setext in item": "- item\n\n  text\n  ===",
    "task item": "- [ ] item",
    "empty item gains": "-\n  text",
    "ordered nested quote": "1. item\n   > quote",
    "star nested quote": "* item\n  > quote",
    "lazy after nested quote": "- item\n  > quote\nlazy",
    "quote then text": "> quote\n\n  text",
    "footnote resumed": "[^1]: note\n\n  text",
}
TAGS = ["<span>", "</span>", "<custom-tag>"]
FOLLOWERS = {
    "heading": ("## Old\n", ""),
    "fence in item": (f"{{ind}}{F}\n\n## Old\n", ""),
    "pre in item": ("{ind}<pre>\n\n## Old\n", ""),
    "comment in item": ("{ind}<!--\n\n## Old\n", ""),
    "fence then real fence": (f"{{ind}}{F}\n\ntext\n\n{F}\n## Old\n{F}\n", ""),
}


def pages():
    for pname, prefix in PREFIXES.items():
        for col in range(0, 6):
            for tag in TAGS:
                for fname, (follow, _) in FOLLOWERS.items():
                    ind = " " * col
                    page = f"{prefix}\n{ind}{tag}\n" + follow.format(ind=ind) + "\n## Real\n"
                    yield {"name": f"{pname} | tag col {col} {tag} | {fname}", "page": page}


if __name__ == "__main__":
    print(json.dumps(list(pages()), indent=1))
