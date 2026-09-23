#!/usr/bin/env python3
"""A190 probe corpora for the container-aware walk. Deterministic.

Usage: gen_probes.py NAME > corpus.json
NAME is one of: containers, comments, prose, fuzz, tabs, fuzz2
Every page is synthetic and ends with `## Real` so a later heading shows
whether the walk recovered.
"""
import json
import random
import sys

F = "```"

PREFIXES = {
    "bullet": "- item",
    "bullet resumed": "- item\n\n  text",
    "bullet resumed 3": "- item\n\n   text",
    "ordered": "1. item",
    "ordered resumed": "1. item\n\n   text",
    "two-digit": "10. item",
    "two-digit resumed": "10. item\n\n    text",
    "padded item": "-   item",
    "padded resumed": "-   item\n\n    text",
    "wide padding code": "-      code",
    "empty item": "-",
    "empty item gains": "-\n  text",
    "empty item blank": "-\n\n  text",
    "empty item spaces blank": "-\n   \n  text",
    "task": "- [ ] item",
    "nested quote": "- item\n  > quote",
    "nested quote resumed": "- item\n\n  > quote",
    "quote first": "- > quote",
    "quote nested list": "> - item",
    "quote nested list resumed": "> - item\n>\n>   text",
    "quote in quote": "> > deep",
    "nested bullet": "- item\n  - nested",
    "nested bullet resumed": "- item\n  - nested\n\n    text",
    "nested bullet blank outer": "- item\n  - nested\n\n  text",
    "nested ordered": "- item\n  1. nested",
    "nested two-digit": "- item\n  10. nested",
    "nested footnote": "- item\n  [^1]: note",
    "footnote": "[^1]: note",
    "footnote resumed four": "[^1]: note\n\n    text",
    "footnote nested list": "[^1]: note\n\n    - item",
    "table in item": "- item\n\n  | a |\n  | - |",
    "table rows in item": "- item\n\n  | a |\n  | - |\n  | b |",
    "thematic in item": "- item\n  ***",
    "setext in item": "- item\n\n  text\n  ---",
    "heading in item": "- item\n  ## Inner",
    "fence closed in item": "- item\n  ```\n  code\n  ```",
    "html closed in item": "- item\n  <div>\n  x\n\n  text",
    "lazy after nested quote": "- item\n  > quote\nlazy",
    "lazy item": "- item\nlazy",
    "lazy resumed": "- item\n\n  text\nlazy",
    "quote lazy": "> quote\nlazy",
    "sibling": "- item\n- next",
    "sibling ordered": "1. item\n2. next",
    "interrupt": "text\n- item",
    "quote then text": "> quote\n\n  text",
    "code then item": "    code\n- item",
    "item after heading": "## H\n- item",
    "item four-space nested blank": "- a\n\n    - b",
    "tab item": "-\titem",
    "tab resumed": "-\titem\n\n\ttext",
    "quote tab": ">\tquote",
}
TAGS = ["<span>", "</span>", "<div>", "<pre>"]
FOLLOWERS = {
    "heading": "## Old\n",
    "fence in item": "{ind}" + F + "\n\n## Old\n",
    "pre in item": "{ind}<pre>\n\n## Old\n",
    "comment in item": "{ind}<!--\n\n## Old\n",
    "fence then real fence": "{ind}" + F + "\n\ntext\n\n" + F + "\n## Old\n" + F + "\n",
    "blank heading": "\n## Old\n",
    "lazy then heading": "lazy\n## Old\n",
}


def containers() -> list:
    out = []
    for pname, prefix in PREFIXES.items():
        for col in range(0, 6):
            for tag in TAGS:
                for fname, follow in FOLLOWERS.items():
                    ind = " " * col
                    page = f"{prefix}\n{ind}{tag}\n" + follow.format(ind=ind) + "\n## Real\n"
                    out.append({"name": f"{pname} | {col} {tag} | {fname}", "page": page})
        for fname, follow in FOLLOWERS.items():
            for col in (0, 2, 3, 4):
                ind = " " * col
                page = f"{prefix}\n" + follow.format(ind=ind) + "\n## Real\n"
                out.append({"name": f"{pname} | no tag {col} | {fname}", "page": page})
    return out


RAW_OPENERS = [
    '<div title="<!--">', "<div title='<!--'>", "<div title=<!-->", '<span title="<!--">',
    '<div title="x" <!-- >', "<div\ntitle=\"<!--\">", '<img alt="<!-- x">', "<![CDATA[<!--]]>",
    "<![CDATA[ a > <!-- ]]>", "<?php <!-- ?>", "<? a > <!-- ?>", "<!DOCTYPE <!-- >",
    "<!X a > <!--", "</1 <!-- >", "</ <!--", "<textarea><!--</textarea>",
    '<textarea title="<!--">', "<style><!--</style>", "<script><!--</script>",
    "<title><!--</title>", "<xmp><!--</xmp>", "<iframe><!--</iframe>", "<noembed><!--",
    "<noframes><!--", "<plaintext><!--", "<textareax><!--", "<textarea/x><!--",
    "<!-- a --!>", "<!-- a -- >", "<!-- a --->", "<!--!>", "<!---!>", "<!----!>", "<!-->",
    "<!--->", "<!-- a -->", "<!-- a --> <!--", "<!--", "x <!--", "<!-- a\n-->", "<!--\n--!>",
    "<a href='x'><!--", "<b>text</b><!--", "<br/><!--", "<!--<!-- -->", "<!-- -- -->",
    "<svg><![CDATA[<!--]]></svg>", "<math><!--</math>",
]
RAW_WRAPPERS = {
    "div block": "<div>\n{raw}\n</div>\n",
    "span block": "<span>\n{raw}\n",
    "pre block": "<pre>\n{raw}\n</pre>\n",
    "bare line": "{raw}\n",
    "item div": "- item\n\n  <div>\n  {raw}\n",
    "quote div": "> <div>\n> {raw}\n",
}
CLOSERS = [
    "text <a title=\"-->\"> more", "text <a title='-->'> more", "text <a title=--> more",
    "text <!-- x --> more", "text <!-- a -- b --> more", "text <!---->", "text <!-->",
    "text <!--->", "text <?-->?>", "text <!X -->", "text <!x -->", "text <![CDATA[-->]]>",
    "text </a --> more", "text <a --> more", "text <a\ntitle=\"-->\"> more",
    "text `-->` more", "text `` <a title=\"-->\"> `` more", "text \\<a title=\"-->\"> more",
    "text --> more", "text --!> more", "text <a title=\"--!>\"> more", "## Hid <!-- x -->",
    "## Hid <a title=\"-->\">", "| a <!-- x --> |\n| - |", "- item <!-- x -->", "> q <!-- x -->",
    "[^1]: n <!-- x -->", "text <textarea title=\"-->\"> more", "<div>\n-->\n</div>",
    "<div>\n--!>\n</div>", "<pre>\n-->\n</pre>", "<!-- b -->", "    -->", F + "\n-->\n" + F,
    "text <http://a-->b> more", "text <a@b-->c> more", "[x](<-->) more", "text <!-- x --!> more",
    "text <a title=\"x\n-->\"> more",
]


def comments() -> list:
    out = []
    for raw in RAW_OPENERS:
        for wname, wrap in RAW_WRAPPERS.items():
            body = wrap.format(raw=raw.replace("\n", "\n  " if wname.startswith("item") else
                                                 ("\n> " if wname.startswith("quote") else "\n")))
            out.append({"name": f"open {wname} {raw!r}", "page": body + "\n## Old\n\n## Real\n"})
    for closer in CLOSERS:
        for opener in ("<div>\n<!--\n</div>\n", "<span>\n<!--\n"):
            out.append({"name": f"close {closer!r} after {opener!r}",
                        "page": opener + "\n## Hidden\n\n" + closer + "\n\n## Old\n\n## Real\n"})
        out.append({"name": f"closer alone {closer!r}", "page": closer + "\n\n## Old\n\n## Real\n"})
    return out


PROSE = [
    "text <!--", "text `<!--` more", "text \\<!-- more", "text <a title=\"<!--\"> more",
    "## Head <!--", "- item <!--", "> q <!--", "| a <!-- |\n| - |", "text <!-- a", "    <!--",
    "text\n    <!--", "- item\n\n  text <!--", "- item\n  text <!--", "text <!-- x --> <!--",
]
AFTER = ["\n## Old\n", "## Old\n", "more\n## Old\n", "more -->\n## Old\n", "\n-->\n## Old\n",
         "- item\n## Old\n", "lazy\n\n## Old\n", "  more\n## Old\n"]


def prose() -> list:
    out = []
    for p in PROSE:
        for a in AFTER:
            out.append({"name": f"prose {p!r} then {a!r}", "page": p + "\n" + a + "\n## Real\n"})
            out.append({"name": f"prose in item {p!r} then {a!r}",
                        "page": "- item\n  " + p.replace("\n", "\n  ") + "\n" + a + "\n## Real\n"})
    return out


LINES = [
    "- item", "  - nested", "1. item", "10. item", "-", "  text", "   text", "    text", "text",
    "", "", "> quote", "  > quote", "> - item", ">", "[^1]: note", "    more", "<span>", "  <span>",
    "   <span>", "</span>", "<div>", "  <div>", "</div>", "<pre>", "  <pre>", "</pre>", F, "  " + F,
    "   " + F, "    " + F, "<!--", "  <!--", "-->", "  -->", "## Old", "## Mid", "text <!--",
    "| a |", "| - |", "  | a |", "  | - |", "***", "---", "===", "\t- tab", "-\ttab", "lazy",
    "<!-- a -->", '<div title="<!--">', "text <a title=\"-->\">", "~~~", "  ~~~", "<textarea>",
]


def fuzz(n: int = 6000, seed: int = 437) -> list:
    rng = random.Random(seed)
    out = []
    for i in range(n):
        lines = [rng.choice(LINES) for _ in range(rng.randint(2, 7))]
        out.append({"name": f"fuzz {i}", "page": "\n".join(lines) + "\n## Old\n\n## Real\n"})
    return out


def tabs() -> list:
    out = []
    pre = ["-\titem", "- \titem", "-  \titem", "1.\titem", ">\tquote", "> \tquote", ">\t- item",
           "-\t- item", "\t- item", " \t- item", "-\t\titem"]
    body = ["\ttext", "  text", "   text", "    text", "\t\ttext", " \ttext", "  \ttext"]
    for p in pre:
        for b in body:
            for tag in ("<span>", "</span>"):
                for col in ("", " ", "  ", "   ", "\t"):
                    out.append({"name": f"tabs {p!r} {b!r} {col!r}{tag}",
                                "page": f"{p}\n\n{b}\n{col}{tag}\n## Old\n" + F + "\n\n## Mid\n\n## Real\n"})
    return out




LINES2 = LINES + [
    "  > quote", ">  - item", "- > quote", "  1. item", "     text", "      code", "- [ ] task",
    "[^2]: note", "    [^1]: x", "  <!-- a -->", "<div title=\"a > <!--\">", "<![CDATA[ a > <!-- ]]>",
    "<? x ?>", "<!X a > <!--", "<!x a > <!--", "text `<!--` more", "text <!-- x --> more",
    "text <a title='-->'> more", "--!>", "<!-- a --!>", "<textarea title=\"<!--\">", "  </div>",
    "  <!-- x", "    <!-- x", "> <!--", ">    <!--", "| a <!-- |", "***", "  ***", "## Mid <!--",
    "\t<span>", " \t<span>", ">\t<span>", "-\t<span>", "  </span>", "   </span>", "text\t<!--",
]


def fuzz2(n: int = 8000, seed: int = 516) -> list:
    rng = random.Random(seed)
    out = []
    for i in range(n):
        lines = [rng.choice(LINES2) for _ in range(rng.randint(2, 8))]
        out.append({"name": f"fuzz2 {i}", "page": "\n".join(lines) + "\n## Old\n\n## Real\n"})
    return out


if __name__ == "__main__":
    print(json.dumps({"containers": containers, "comments": comments, "prose": prose,
                      "fuzz": fuzz, "tabs": tabs, "fuzz2": fuzz2}[sys.argv[1]](), indent=0))
