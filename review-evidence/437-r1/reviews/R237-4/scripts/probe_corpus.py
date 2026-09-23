#!/usr/bin/env python3
"""Generate this review's own probe pages for the #437 container walk.

Usage: probe_corpus.py > probes.json    (a JSON list of {"name", "page"})

Deterministic: no randomness. Families:
  L  items and quotes holding link reference definitions (CommonMark 4.7),
     one-line and other forms, followed by blocks at the item's column.
  E  a fence or raw HTML block opened inside a container, then the line
     that may or may not end that container.
  G  the lone type-7 tag gate after container paragraphs and nested blocks.
  N  footnote definitions: blank, whitespace-only and indented lines.
Every page ends with a visible `## Real` sentinel after a blank line so a
block left open is observable.
"""
import json
import sys

FOLLOW = {
    "fence2": "  ```\n## Old\n```\n",
    "div2": "  <div>\n## Old\n",
    "span0": "<span>\n## Old\n</span>\n",
    "span2": "  <span>\n## Old\n  </span>\n",
    "text-span0": "  text\n<span>\n## Old\n</span>\n",
    "pre2": "  <pre>\n## Old\n</pre>\n",
    "fence0": "```\n## Old\n```\n",
}


def link_family() -> list:
    defs = {
        "bare": "[a]: /u",
        "bare-title-dq": '[a]: /u "t"',
        "angle": "[a]: <u>",
        "title-sq": "[a]: /u 't'",
        "title-paren": "[a]: /u (t)",
        "multiline-dest": "[a]:\n  /u",
        "multiline-title": "[a]: /u\n  \"t\"",
        "two-defs": "[a]: /u\n  [b]: /v",
        "escaped-label": "[a\\]b]: /u",
        "not-a-def-empty-dest": "[a]:",
        "def-then-text": "[a]: /u\n  text",
        "footnote-like": "[^a]: /u",
        "angle-empty": "[a]: <>",
        "bare-parens": "[a]: /u(x)",
        "nested-parens": "[a]: /u((x))",
        "title-dq-escaped": '[a]: /u "t\\"x"',
    }
    rows = []
    for dname, d in defs.items():
        for marker in ("- ", "1. "):
            pad = " " * len(marker)
            body = d.replace("\n  ", "\n" + pad)
            for blanks in (1, 2):
                for fname, follow in FOLLOW.items():
                    f = follow.replace("  ", pad, 1) if follow.startswith("  ") else follow
                    page = f"{marker}{body}\n" + "\n" * blanks + f + "\n## Real\n"
                    rows.append({"name": f"L {dname} {marker.strip()} blanks={blanks} {fname}", "page": page})
        for blanks in (1, 2):
            for fname, follow in FOLLOW.items():
                q = "> " + d.replace("\n  ", "\n> ")
                page = q + "\n" + "\n" * blanks + follow + "\n## Real\n"
                rows.append({"name": f"L quote {dname} blanks={blanks} {fname}", "page": page})
    return rows


def end_family() -> list:
    containers = {
        "item": ("- a\n", "  "),
        "item-resumed": ("- a\n\n  b\n", "  "),
        "ordered": ("1. a\n", "   "),
        "two-digit": ("10. a\n", "    "),
        "nested": ("- a\n  - b\n", "    "),
        "quote": ("> a\n", "> "),
        "quote-item": ("> - a\n", ">   "),
        "item-quote": ("- > a\n", "  > "),
        "footnote": ("[^1]: a\n", "    "),
        "empty-item": ("-\n", "  "),
        "paren-ordered": ("1) a\n", "   "),
        "marker-indent": ("  - a\n", "    "),
        "tab-item": ("-\ta\n", "    "),
    }
    blocks = {
        "fence": ("```", "```"),
        "tilde": ("~~~", "~~~"),
        "div": ("<div>", "</div>"),
        "pre": ("<pre>", "</pre>"),
        "span": ("<span>", "</span>"),
        "type3": ("<?x", "?>"),
        "type4": ("<!X", ">"),
        "cdata": ("<![CDATA[", "]]>"),
    }
    enders = {
        "heading": "## Old\n",
        "text": "text\n## Old\n",
        "blank-heading": "\n## Old\n",
        "indented-text": " text\n## Old\n",
        "lazy-like": "lazy\n\n## Old\n",
        "closer0": "{close}\n## Old\n",
        "quote-line": "> q\n## Old\n",
        "item-line": "- x\n## Old\n",
    }
    rows = []
    for cname, (head, cont) in containers.items():
        for bname, (opener, closer) in blocks.items():
            for ename, ender in enders.items():
                e = ender.replace("{close}", closer)
                page = head + cont + opener + "\n" + e + closer + "\n\n## Real\n"
                rows.append({"name": f"E {cname} {bname} {ename}", "page": page})
                inner = head + cont + opener + "\n" + cont + "## Inside\n" + e + "\n## Real\n"
                rows.append({"name": f"E {cname} {bname} {ename} inner", "page": inner})
    return rows


def gate_family() -> list:
    prefixes = {
        "item": "- a",
        "item-blank": "- a\n",
        "resumed": "- a\n\n  b",
        "nested-resumed": "- a\n  - b\n\n    c",
        "nested-outer": "- a\n  - b\n\n  c",
        "quote": "> a",
        "quote-blank": "> a\n",
        "item-in-quote": "> - a\n>\n>   b",
        "quote-in-item": "- > a",
        "footnote": "[^1]: a",
        "footnote-resumed": "[^1]: a\n\n    b",
        "table-in-item": "- | a |\n  | - |",
        "heading-in-item": "- # h",
        "hr-in-item": "- ***",
        "code-in-item": "-     code",
        "fenced-in-item": "- ```\n  x\n  ```",
        "lazy": "- a\nlazy",
        "lazy-quote": "> a\nlazy",
        "setext-in-item": "- a\n  ===",
        "empty-then-text": "-\n  a",
        "html-in-item": "- <div>\n  x",
        "comment-in-item": "- <!-- c -->",
        "def-in-item": "- [a]: /u",
        "def-in-item-text": "- [a]: /u\n  b",
        "ordered-2": "2. a",
        "ordered-10": "10. a\n\n    b",
    }
    tags = ("<span>", "</span>", '<span title="x">', "<custom-tag>", "<b/>")
    rows = []
    for pname, prefix in prefixes.items():
        for tag in tags:
            for col in range(6):
                page = f"{prefix}\n{' ' * col}{tag}\n## Old\n\n## Real\n"
                rows.append({"name": f"G {pname} {tag} col{col}", "page": page})
    return rows


def footnote_family() -> list:
    rows = []
    mids = {
        "empty": "\n",
        "ws1": " \n",
        "ws3": "   \n",
        "ws4": "    \n",
        "tab": "\t\n",
        "two-empty": "\n\n",
    }
    tails = {
        "code4": "    ```\n## Old\n```\n",
        "text4": "    b\n<span>\n## Old\n</span>\n",
        "text2": "  b\n<span>\n## Old\n</span>\n",
        "div4": "    <div>\n## Old\n",
        "fence0": "```\n## Old\n```\n",
    }
    for mname, mid in mids.items():
        for tname, tail in tails.items():
            for head in ("[^1]: a\n", "- [^1]: a\n", "> [^1]: a\n"):
                t = tail
                m = mid
                if head.startswith("- "):
                    t = "\n".join(("  " + l if l else l) for l in tail.split("\n"))
                    m = mid if mid.strip() == "" and mid.startswith("\n") else "  " + mid
                if head.startswith("> "):
                    t = "\n".join(("> " + l if l else l) for l in tail.split("\n"))
                    m = ">" + mid if mid != "\n\n" else ">\n>\n"
                page = head + m + t + "\n## Real\n"
                rows.append({"name": f"N {head.strip()[:6]} {mname} {tname}", "page": page})
    return rows


def main() -> int:
    rows = link_family() + end_family() + gate_family() + footnote_family()
    seen, out = set(), []
    for r in rows:
        if r["page"] not in seen:
            seen.add(r["page"])
            out.append(r)
    json.dump(out, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
