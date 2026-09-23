#!/usr/bin/env python3
"""Generate random synthetic pages for the container / rendered-comment walk.

Usage: gen_pages.py <seed> <count> <out.json> [core]
With `core`, the processing-instruction, CDATA, declaration, open-quote,
link-reference and image fragments are left out, so only the container,
tag, comment, fence and table machinery is exercised.
Headings are `## H<n>` at column 0 with unique numbers, so a rendered
heading element is matched to its line exactly; other lines are drawn from
container openers, lazy text, lone tags, comments, types 3 to 5, fences,
tables, link reference definitions and inline HTML, each with a random
indentation and an optional container prefix.
"""
import json
import random
import sys

OPENERS = ["- a", "* a", "+ a", "1. a", "10. a", "2. a", "1) a", "-", "1.",
           "> a", ">", "[^1]: n", "- > a", "> - a", "-   a", "-\ta", "-     a",
           "- [ ] a", "> > a", "- - a", "> [^2]: n", "* * *", "- - -"]
TEXT = ["text", "lazy", "t <!--", "t -->", "t <span>", "`x <!--`", "\\<!--",
        "a <!-- b", "a --> b", "t `-->`", "t \\-->", "x <b title='-->'>",
        "x <?p > <!-- ?>", "x <![CDATA[ > <!-- ]]>", "![<b title='-->'>](u)",
        "[r]: /u '<b title=\"-->\">'", "[r]: /u", "<a href='x'>t</a>",
        "===", "---", "-", "| a | b |", "|---|---|", "x <!-- y --> z",
        "x <!---> y", "x <!--> y", "*emph <!--*"]
TAGS = ["<span>", "</span>", "<custom-x>", "<div>", "</div>", "<pre>", "</pre>",
        "<span title=\"x\">", "<span title=\"", "<b>", "<div title='", "\"",
        "'>", "<span\n", "<noscript>", "<svg>", "<template>", "<details>",
        "<textarea>", "<style>", "<p>", "</p>", "<table>", "<!-- <span>",
        "<span title='<!--'>", "<div><!--", "<div> -->"]
COMMENTS = ["<!--", "-->", "<!-- x -->", "<!-->", "--!>", "<!--->",
            "<!-- a", "b -->", "<!-- -- -->", "<!--x-->y<!--"]
RAW35 = ["<?x", "?>", "<!DOCTYPE x", "<![CDATA[", "]]>", "<?x > <!-- ?>",
         "<!X >", "<![CDATA[ x > <!-- ]]>", "<!x"]
FENCES = ["```", "~~~", "````", "``` x", "~~~~"]
KINDS = [(OPENERS, 5), (TEXT, 5), (TAGS, 5), (COMMENTS, 4), (RAW35, 2),
         (FENCES, 2), ([""], 5)]
INDENTS = ["", "", "", " ", "  ", "   ", "    ", "\t", "  ", "     "]
PREFIXES = ["", "", "", "", "> ", "- ", "  ", "1. ", ">", "> > "]


def line(rng: random.Random) -> str:
    pool = rng.choices([k for k, _ in KINDS], [w for _, w in KINDS])[0]
    body = rng.choice(pool)
    if not body:
        return ""
    return rng.choice(PREFIXES) + rng.choice(INDENTS) + body


def page(rng: random.Random) -> str:
    out, n = [], 1
    for _ in range(rng.randint(3, 9)):
        if rng.random() < 0.3:
            out.append(f"## H{n}")
            n += 1
        else:
            out.append(line(rng))
    out.append(f"## H{n}")
    return "\n".join(out) + "\n"


def main() -> None:
    seed, count, out_path = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    if sys.argv[4:] == ["core"]:
        exotic = ("<?", "CDATA", "<!D", "<!X", "<!x", "[r]", "![", "title=\"\n",
                  "?>", "]]>")
        for pool, _ in KINDS:
            pool[:] = [f for f in pool if not any(e in f for e in exotic)
                       and f not in ("<span title=\"", "<div title='", "\"", "'>")] or [""]
    rng = random.Random(seed)
    pages = {}
    while len(pages) < count:
        text = page(rng)
        pages.setdefault(f"s{seed}-{len(pages):06d}", text)
    json.dump(pages, open(out_path, "w"), indent=0)


if __name__ == "__main__":
    main()
