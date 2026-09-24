"""Seeded random pages over a vocabulary of containers, raw HTML, comments and headings."""
import json, random, sys
VOCAB = [
    "- item", "1. item", "10. item", "> quote", "[^1]: note", "- [ ] task", "-", "  - nested", "  text", "   text",
    "    text", "\ttext", "text", "lazy", "```", "~~~", "  ```", "> ```", "***", "Title\n===", "text\n---", "text\n-",
    "| a | b |\n|---|---|\n| c | d |", "> | a |\n> |---|", "[r]: /u", "- [r]: /u", "[x](<a-->)", "`<!--`", "\\<!--",
    "text <!-- c", "more -->", "text <? > <!-- ?>", "text <![CDATA[ > <!-- ]]>", "ref[^1]",
    "<span>", "</span>", "  <span>", "<div>", "</div>", "<pre>", "</pre>", '<div title="', "<div title='", '<b title="x">',
    "<!--", "-->", "<!-- c -->", "<!-->", "<!--->", "--!>", "<!-- a --!>", "<? x", "?>", "<![CDATA[", "]]>", "<!X y",
    "<select>", "</select>", "<textarea>", "</textarea>", "<noscript>", "</noscript>", "<template>", "</template>",
    "<table>", "</table>", "<svg>", "</svg>", "<details>", "<summary>s</summary>", "</details>", "<a href='", "<img alt=\"x",
    "<style>", "</style>", "<script>", "</script>", "<plaintext>", "<xmp>", "<iframe>",
]
def page(rng, n):
    parts, h = [], 0
    for _ in range(rng.randint(3, 8)):
        if rng.random() < 0.4:
            h += 1
            parts.append(rng.choice(["## H{}", "## H{}", "  ## H{}", "> ## H{}", "   ## H{}", "H{}\n---"]).format(h))
        else:
            parts.append(rng.choice(VOCAB))
    h += 1
    parts.append(f"## H{h}")
    out = parts[0]
    for part in parts[1:]:
        out += rng.choice(["\n", "\n", "\n\n"]) + part
    return out + "\n"
if __name__ == "__main__":
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    pages, seen = [], set()
    while len(pages) < count:
        p = page(rng, len(pages))
        if p not in seen and "data-sourcepos" not in p:
            seen.add(p); pages.append({"set": "fuzz", "name": f"s{seed}-{len(pages):04d}", "page": p})
    json.dump(pages, open(sys.argv[3], "w"), indent=1)
    print(len(pages))
