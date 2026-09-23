#!/usr/bin/env python3
"""Second probe corpus: comment reading, raw HTML types 3 to 5, and one
shape per limitation sentence of CONTRIBUTING 6.1 / the blocks() docstring.

Usage: probe_corpus2.py > probes2.json    (JSON list of {"name", "page", "claim"})

`claim` names the documented direction a shape should show (escape,
withhold, agree) or null for the combinatorial rows.
"""
import json
import sys


def claims() -> list:
    """One shape per documented sentence, with the direction it states."""
    return [
        ("6.1 opener GitHub prints as text withholds (code span)", "text `<!--` more\n\n## Old\n\n## Real\n", "withhold"),
        ("6.1 opener GitHub prints as text withholds (escape)", "text \\<!-- more\n\n## Old\n\n## Real\n", "withhold"),
        ("6.1 opener GitHub prints as text withholds (no closer in paragraph)", "text <!-- more\n\n## Old\n\n## Real\n", "withhold"),
        ("6.1 empty comment <!--> withholds", "<!-->\n\n## Old\n\n## Real\n", "withhold"),
        ("6.1 empty comment <!---> withholds", "<!--->\n\n## Old\n\n## Real\n", "withhold"),
        ("6.1 --!> withholds", "<!-- a --!>\n\n## Old\n\n## Real\n", "withhold"),
        ("6.1 comment over a fence lists after --> in fence", "<!-->\n```\n-->\n## Old\n```\n\n## Real\n", "escape"),
        ("6.1 #516 opener in raw HTML block", "<div>\n<!--\n</div>\n\n## Old\n\n## Real\n", "escape"),
        ("6.1 #516 opener four columns into an item", "- item\n\n    <!--\n\n## Old\n\n## Real\n", "escape"),
        ("6.1 #516 closer GitHub prints as text", "<div>\n<!--\n</div>\n\n`-->`\n\n## Old\n\n## Real\n", "escape"),
        ("6.1 comment closed in its own raw HTML block agrees", "<div>\n<!-- a -->\n</div>\n\n## Old\n\n## Real\n", "agree"),
        ("6.1 raw HTML ends inside unclosed tag hides next heading", "<div\n\n## Old\n\n## Real\n", "escape"),
        ("6.1 raw HTML ends inside bogus comment hides next heading", "<div>\n<?x\n\n## Old\n\n## Real\n", "escape"),
        ("6.1 raw HTML ends inside open quoted value hides every later", "<div title=\"\n\n## Old\n\n## Real\n", "escape"),
        ("6.1 select hides the headings inside it", "<select>\n\n## Old\n\n</select>\n\n## Real\n", "escape"),
        ("6.1 type 3 to 5 block labelled prose lists heading", "<?php\n## Old\n?>\n\n## Real\n", "escape"),
        ("6.1 type 4 block labelled prose lists heading", "<!DOCTYPE x\n## Old\n>\n\n## Real\n", "escape"),
        ("6.1 CDATA block labelled prose lists heading", "<![CDATA[\n## Old\n]]>\n\n## Real\n", "escape"),
        ("6.1 lone tag continues a paragraph its line reaches", "- a\n\n  b\n  <span>\n## Old\n  </span>\n\n## Real\n", "agree"),
        ("6.1 lone tag otherwise opens raw HTML inside an item", "- a\n  - b\n  <span>\n  ```\n\n## Old\n\n## Real\n", "agree"),
        ("6.1 fence ends with the container it opened in", "- a\n  ```\n## Old\n```\n\n## Real\n", "agree"),
        ("6.1 raw HTML block ends with its container", "> <div>\n## Old\n\n## Real\n", "agree"),
        ("6.1 definition-only item empty once it closes", "- [a]: /u\n\n\n  ```\n## Old\n```\n\n## Real\n", "agree"),
        ("6.1 other definition keeps the item open", "- [a]: <u>\n\n\n  ```\n## Old\n```\n\n## Real\n", "escape"),
    ]


def combos() -> list:
    """Top-level comment and raw-HTML openers, a tag line, then a heading."""
    openers = {
        "none": "",
        "inline-closed": "text <!-- c --> more\n",
        "inline-open-closed-later": "text <!-- c\nmore -->\n",
        "inline-open-blank-closed": "text <!-- c\n\nmore -->\n",
        "block-comment": "<!-- c\n-->\n",
        "indented4-in-para": "text\n    <!-- c\n-->\n",
        "type3": "<?x ?>\n",
        "type3-multi": "<?x\ny ?>\n",
        "type4": "<!X y>\n",
        "cdata": "<![CDATA[ x ]]>\n",
        "para-then-type3": "text\n<?x ?>\n",
        "para-then-cdata-multi": "text\n<![CDATA[\nx ]]>\n",
    }
    tags = {"span": "<span>", "close": "</span>", "custom": "<custom-tag>", "div": "<div>"}
    rows = []
    for oname, opener in openers.items():
        for tname, tag in tags.items():
            for gap in ("", "\n"):
                page = opener + gap + tag + "\n## Old\n\n## Real\n"
                rows.append((f"C {oname} gap={bool(gap)} {tname}", page, None))
                page = opener + gap + "text\n" + tag + "\n## Old\n\n## Real\n"
                rows.append((f"C {oname} gap={bool(gap)} text {tname}", page, None))
                for container in ("- a\n\n  ", "> "):
                    inner = container + opener.replace("\n", "\n" + container.strip("\n").split("\n")[-1] if container.startswith(">") else "\n  ")
                    page = inner.rstrip(" >") + "\n" + tag + "\n## Old\n\n## Real\n"
                    rows.append((f"C {container.strip()[:1]} {oname} gap={bool(gap)} {tname}", page, None))
    return rows


def main() -> int:
    rows = claims() + combos()
    seen, out = set(), []
    for name, page, claim in rows:
        if page not in seen:
            seen.add(page)
            out.append({"name": name, "page": page, "claim": claim})
    json.dump(out, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
