"""The committed shape set for #437/#516, before rendering: (set, name, page, source, extra)."""
import json
from pathlib import Path

PR515 = Path("/tmp/a212/pr515")
SRC515 = "PR #515 fixture {} at 34f124f9 (page only; rendered afresh)"


def _from_515():
    out = []
    fam = json.loads((PR515 / "gen_toc_family_one.json").read_text())
    for s in fam["shapes"]:
        extra = {"kind": s["kind"]}
        if s.get("r86_5"):
            extra["r86_5"] = s["r86_5"]
        out.append(("family one", s["name"], s["page"], SRC515.format("gen_toc_family_one.json"), extra))
    com = json.loads((PR515 / "gen_toc_comment_shapes.json").read_text())
    for s in com["shapes"]:
        kind = "#516" if s["name"].startswith("#516") else "comment"
        out.append((kind, s["name"], s["page"], SRC515.format("gen_toc_comment_shapes.json"), {}))
    con = json.loads((PR515 / "gen_toc_container_walk.json").read_text())
    for s in con["shapes"]:
        out.append(("container", s["name"], s["page"], SRC515.format("gen_toc_container_walk.json"),
                    {"pins": s.get("pins", "")} if s.get("pins") else {}))
    return out


R237_1 = "R237-r1 (PR #515 comment 5777954062)"
R238_1 = "R238-r1 (PR #515 comment 5778167234)"
R237_2 = "R237-2 (PR #515 comment 5790354117)"
R237_3 = "R237-3 (PR #515 comment 5794524773)"
R238_2 = "R238-2 (PR #515 comment 5794587304)"
R237_4 = "R237-4 (PR #515 comment 5797159256)"
R238_3 = "R238-3 (PR #515 comment 5797915656)"
WRAP = "## Old\n</span>\n\n## Real\n"


def _reviews():
    out = []
    add = lambda s, n, p, src, rec=False: out.append((s, n, p, src + (", reconstructed from its description" if rec else ", exact page"), {"reconstructed": True} if rec else {}))
    # R237-r1 F1: the tag column matrix under a resumed item paragraph.
    for col in range(5):
        for what, tag in (("open", "<span>"), ("close", "</span>"), ("attribute", '<span class="x">')):
            add("R237", f"R237-r1 F1 resumed paragraph, tag column {col} {what}", f"- item\n\n  text\n{' ' * col}{tag}\n" + WRAP, R237_1, rec=True)
    # R237-r1 F3: block markers inside a fence, a comment and a raw HTML block, indented closer.
    for what, opener, closer in (("fenced", "```", "  ```"), ("commented", "<!--", "  -->"), ("HTML", "<div>", "  </div>")):
        add("R237", f"R237-r1 F3 {what} marker, indented closer", f"{opener}\n- fake item\n{closer}\n\n  text\n<span>\n" + WRAP, R237_1, rec=True)
    # R238-r1 C01-C08, D01-D07, P01, P04 (descriptions only).
    c01 = "- item\n\n  text\n  <span>\n"
    add("R238", "R238-r1 C01 tag at column 2 under a resumed paragraph", c01 + WRAP, R238_1, rec=True)
    add("R238", "R238-r1 C02 tag at column 3", "- item\n\n  text\n   <span>\n" + WRAP, R238_1, rec=True)
    add("R238", "R238-r1 C03 ordered item, tag at column 3", "1. item\n\n   text\n   <span>\n" + WRAP, R238_1, rec=True)
    add("R238", "R238-r1 C04 then a column-0 fence", c01 + "```\n\n## Old\n\n## Real\n", R238_1, rec=True)
    add("R238", "R238-r1 C05 then a column-0 comment", c01 + "<!--\n\n## Old\n\n## Real\n", R238_1, rec=True)
    add("R238", "R238-r1 C06 then a column-0 pre", c01 + "<pre>\n\n## Old\n\n## Real\n", R238_1, rec=True)
    add("R238", "R238-r1 C07 after a lazy line, then a fence", "- item\n\n  text\nlazy\n  <span>\n```\n\n## Old\n\n## Real\n", R238_1, rec=True)
    add("R238", "R238-r1 C08 column-3 item, then a fence", "1. item\n\n   text\n   <span>\n```\n\n## Old\n\n## Real\n", R238_1, rec=True)
    add("R238", "R238-r1 D01 dedented quote then resumed text", "- item\n> quote\n\n  text\n<span>\n" + WRAP, R238_1, rec=True)
    add("R238", "R238-r1 D02 dedented footnote then resumed text", "- item\n[^1]: note\n\n  text\n<span>\n" + WRAP, R238_1, rec=True)
    add("R238", "R238-r1 D03 dedented quote, fence after the tag", "- item\n> quote\n\n  text\n<span>\n```\n## Old\n```\n\n## Real\n", R238_1, rec=True)
    add("R238", "R238-r1 D04 dedented footnote, fence after the tag", "- item\n[^1]: note\n\n  text\n<span>\n```\n## Old\n```\n\n## Real\n", R238_1, rec=True)
    add("R238", "R238-r1 D05 quote after a blank line", "- item\n\n> quote\n\n  text\n<span>\n" + WRAP, R238_1, rec=True)
    add("R238", "R238-r1 D06 quote inside the item", "- item\n  > quote\n\n  text\n<span>\n" + WRAP, R238_1, rec=True)
    add("R238", "R238-r1 D07 dedented quote then four-column text", "- item\n> quote\n\n    text\n<span>\n" + WRAP, R238_1, rec=True)
    add("R238", "R238-r1 P01 first paragraph, tag then fence", "- item\n  <span>\n```\n\n## Old\n\n## Real\n", R238_1, rec=True)
    add("R238", "R238-r1 P04 first paragraph, tag", "- item\n  <span>\n" + WRAP, R238_1, rec=True)
    # R237-2: F1 (3), F2 (10), F3 (2), S1 (2).
    for i, p in enumerate(["- item\n  > quote\n  <span>\n  ```\n\ntext\n\n```\n## Old\n```\n\n## Real\n",
                           "- item\n  - nested\n  <span>\n  ```\n\n## Old\n\n## Real\n",
                           "- item\n  <span>\n  ```\n\ntext\n\n```\n## Old\n```\n\n## Real\n"], 1):
        add("R237", f"R237-2 F1 row {i}", p, R237_2)
    for i, p in enumerate(['<div title="<!--">\n\n## Old\n\n## Real\n', '<span title="<!--">\n\n## Old\n\n## Real\n',
                           '<div>\n<img alt="<!-- x">\n</div>\n\n## Old\n\n## Real\n', '<div>\n<![CDATA[<!--]]>\n</div>\n\n## Old\n\n## Real\n',
                           '<div>\n<!-- a --!>\n</div>\n\n## Old\n\n## Real\n', '<div>\n<!--\n--!>\n</div>\n\n## Old\n\n## Real\n',
                           '<div>\n<!--\n</div>\n\ntext <a title="-->"> more\n\n## Old\n\n## Real\n',
                           '- item\n\n  <div>\ntext `<!--` more\n\n## Old\n\n## Real\n', '- item\n\n  <div>\ntext \\<!-- more\n\n## Old\n\n## Real\n',
                           '- item\n\n  <div>\ntext <a title="<!--"> more\n\n## Old\n\n## Real\n'], 1):
        add("R237", f"R237-2 F2 row {i}", p, R237_2)
    add("R237", "R237-2 F3 empty item, tag", "-\n  <span>\n  ```\n\n## Old\n\n## Real\n", R237_2)
    add("R237", "R237-2 F3 empty item, tag then fence", "-\n  <span>\n  ```\n\ntext\n\n```\n## Old\n```\n\n## Real\n", R237_2)
    add("R237", "R237-2 S1 opener four columns in", "- item\n\n    <!--\n\n## Old\n\n## Real\n", R237_2)
    add("R237", "R237-2 S1 tag and opener four columns in", "- item\n\n    <div><!--\n\n## Old\n\n## Real\n", R237_2)
    # R237-3.
    for n, p, rec in (("E1", "Text <?p > <!-- ?> more.\n\n## Old\n", False), ("E1b", "Text <?p > <!-- ?> more.\n## Old\n", True),
                      ("E2", "Text <![CDATA[ > <!-- ]]> more.\n\n## Old\n", False), ("E2b", "- item <?p > <!-- ?>\n\n## Old\n", False),
                      ("E8", "## A <?p > <!-- ?>\n\n## Old\n", False), ("E9", "| a |\n|---|\n| <?p > <!-- ?> |\n\n## Old\n", True),
                      ("E5", "<![CDATA[\nx <!---> y\n\n## Old\n", False), ("E5b", "t <!--\n\n<?x\n\n## Old\n", False),
                      ("E6", "t <!--\n\n<div title='\n\n## Old\n", False), ("E6b", "`x <!--`\n\n<div title='\n\n## Old\n", True),
                      ("E7", "- [r]: /u\n\n\n    <!--\n\n## Old\n", False), ("E7b", "- [r]: /u\n\n    <!--\n\n## Old\n", True),
                      ("E7c", "- item\n\n\n    <!--\n\n## Old\n", True), ("E3", '<div>\n<!--\n\n![<b title="-->">](u)\n\n## Old\n', True),
                      ("E4", "<div>\n<!--\n\n[r]: /u '<b title=\"-->\">'\n\n## Old\n", False),
                      ("E10", 'Text <?p > <b title=" ?> more.\n\n## Old\n', False), ("E12", 'Text <!-- a --!> <b title="-->"> more.\n\n## Old\n', False),
                      ("Q1", "> ```\n\n> <!--\n\n## Old\n", False)):
        add("R237", f"R237-3 {n}", p, R237_3, rec)
    # R238-2.
    rows = [("F1a text PI", "text <? > <!-- ?>\n\n## X\n\n## Y\n"), ("F1a text CDATA", "text <![CDATA[ > <!-- ]]>\n\n## X\n\n## Y\n"),
            ("F1a item PI", "- text <? > <!-- ?>\n\n## X\n\n## Y\n"), ("F1a PI, no blank", "text <? > <!-- ?>\n## X\n\n## Y\n"),
            ("F1a control", "text <? <!-- ?>\n\n## X\n\n## Y\n"), ("F1b declaration across items", "- <!X y\n- <!--\n\n## X\n\n## Y\n"),
            ("F1b PI across items", "- <? x\n- <!--\n\n## X\n\n## Y\n"), ("F1b CDATA across containers", "- <![CDATA[ x\n> <!--\n\n## X\n\n## Y\n"),
            ("F1b control", "- <!X y>\n- <!--\n\n## X\n\n## Y\n"), ("F1c type-3 then item opener", "<? x\n- <!--\n## X\n\n## Y\n"),
            ("F1c type-3 then empty comment", "<? x\n<!-->\n## X\n\n## Y\n"), ("F1c CDATA then quote opener", "<![CDATA[\n> <!--\n## X\n\n## Y\n"),
            ("F1c control", "<? x\n## X\n\n## Y\n"), ("F1d tag in a type-4 block", "<!X y\n<b>\n## X\n\n## Y\n"),
            ("F1d tag in a type-3 block", "<? x\n<span>\n?>\n## X\n\n## Y\n"), ("F1d tag in a type-5 block", "<![CDATA[\n<span>\n]]>\n## X\n\n## Y\n"),
            ("F1d control", "<? x\ntext\n?>\n## X\n\n## Y\n"), ("F2 C17", "<? x\n?>\n<div>\n<!--\n\n## X\n\n## Y\n"),
            ("F2 H06", "<div>\n<? a <!-- ?>\n</div>\n\n## X\n\n## Y\n"), ("F2 H10 value across lines", '<div title="a\n<!--\nb">\n\n## X\n\n## Y\n'),
            ("F2 H10 tag across lines", '<div\ntitle="<!--">\n\n## X\n\n## Y\n'), ("F3 select", "<select>\n\n## X\n\n</select>\n\n\n## Y\n")]
    for n, p in rows:
        add("R238", f"R238-2 {n}", p, R238_2)
    add("R238", "R238-2 F3 link destination closer", "<div>\n<!--\n\n[x](<a-->)\n\n## X\n\n## Y\n", R238_2, rec=True)
    # R237-4.
    for n, p in (("F1 angle destination", "- [a]: <u>\n\n\n  ```\n## Old\n```\n\n## Real\n"), ("F1 single-quoted title", "- [a]: /u 't'\n\n\n  <div>\n## Old\n\n## Real\n"),
                 ("F1 destination on the next line", "1. [a]:\n   /u\n\n\n   <pre>\n## Old\n</pre>\n\n## Real\n"),
                 ("F1 parenthesised title", "- [a]: /u (t)\n\n\n  text\n<span>\n## Old\n</span>\n\n## Real\n"),
                 ("F1 control", "- [a]: /u\n\n\n  ```\n## Old\n```\n\n## Real\n"), ("F3 heading as lazy line", "- a\n## H\n  ```\n## Old\n```\n"),
                 ("F3 inline comment rule", "text <!-- c\nmore -->\n<span>\n## Old\n")):
        add("R237", f"R237-4 {n}", p, R237_4)
    # R238-3.
    for n, p, rec in (("T3", "| a | b |\n|---|---|\n    code\nTitle\n-\n  ```\n## Old\n```\n\n## Real\n", False),
                      ("T4", "text\n|-|\n    x\ny\n2. z\n   ```\n## Old\n```\n\n## Real\n", False),
                      ("T8", "## Top\n| a | b |\n|---|---|\n| c | d |\n    code\nTitle\n-\n  ```\n## Old\n```\n\n## Real\n", True),
                      ("T2", "text\n|-|\n    x\ny\n-\n   ~~~\n\n## H1\n", False), ("T5", "text\n|-|\ny\n-\n   ~~~\n\n## H1\n", True),
                      ("F2b single-quoted fence", "- [a]: /u 't'\n\n\n  ```\n## Old\n```\n\n## Real\n", True),
                      ("F2b parenthesised fence", "- [a]: /u (t)\n\n\n  ```\n## Old\n```\n\n## Real\n", True),
                      ("F2b angle tag", "- [a]: <u>\n\n\n  text\n<span>\n## Old\n</span>\n\n## Real\n", True),
                      ("F2b title on the next line", "- [a]: /u\n  't'\n\n\n  ```\n## Old\n```\n\n## Real\n", True),
                      ("F2b lazy definition fence", "- [a]: /u\n[b]: /v\n\n\n  ```\n## Old\n```\n\n## Real\n", True),
                      ("F2b lazy definition tag", "- [a]: /u\n[b]: /v\n\n\n  text\n<span>\n## Old\n</span>\n\n## Real\n", True),
                      ("F3 M21", "text \\<!-- more\n1) item\n  [b]: /v\n- - x\n-->\n\n    text\n  ```\n    text\n\n## H1\n", False),
                      ("S1 comment in a fence", "```\n<!--\n```\n\n## X\n", True)):
        add("R238", f"R238-3 {n}", p, R238_3, rec)
    return out


def _family_two():
    src = "#437 family two, A168's receipt (issue #437 comment 5775985191), exact page"
    return [("family two", n, p, src, {}) for n, p in (
        ("setext equals", "Alpha\n===\n"), ("setext dashes", "text\n---\n"), ("setext one dash", "text\n-\n"),
        ("heading in a block quote", "> ## Q\n"), ("heading in a list item", "- item\n\n  ## Inner\n"))]


def _corpus():
    src = "synthetic reproduction of a tracked-page difference between the old walk and the renderer ({})"
    rows = [("fence in a nested list item", "1. item\n\n   - **nested** text\n     more\n\n     ```bash\n     code\n     ```\n\n     after\n\n## Real\n", "CONTRIBUTING.md:320-328"),
            ("fence in a block quote", "> intro\n>\n> ```sh\n> git clone x\n> ```\n>\n\n## Real\n", "QUICKSTART.md:24-28"),
            ("paragraph four columns into a nested item", "- item\n  - **S4**: a gate\n    more\n\n    Later paragraph.\n\n## Real\n", "docs/design/SAVED_STATE_MATERIALIZATION.md:336-339, docs/testing/CI_WORKFLOWS.md:509-"),
            ("blank line after indented code", "text\n\n    code\n        more\n\nafter\n\n## Real\n", "docs/history/v1/design/TIME_SYNC.md:477, tb/verilator/gptp_txts/README.md:80,87"),
            ("heading three in a block quote", "> ### Title\n>\n> text\n\n## Real\n", "docs/testing/TESTING.md:15"),
            ("heading two in a block quote", "> ## STATUS 2026-08-13 - text\n>\n> more\n\n## Real\n", "docs/history/v1 status banners"),
            ("table in a block quote", "> What changed:\n>\n> | a | b |\n> |---|---|\n> | c | d |\n\n## Real\n", "docs/design/SAVED_STATE_FASTCONNECT.md:15-, docs/limitations/TROUBLESHOOTING.md:567-"),
            ("pipe row after a blank line is no table row", "| a | b |\n|---|---|\n| c | d |\n\n| e | f |\n| g | h |\n\n## Real\n", "docs/reference/REGISTER_MAP.md:355-359"),
            ("pipe row after a comment line is no table row", "| a | b |\n|---|---|\n| c | d |\n<!-- end -->\n<!-- start -->\n| e | f |\n<!-- end -->\n\n## Real\n", "docs/MILAN_V12_ROADMAP.md:135"),
            ("pipe-led line inside a paragraph", "text\n|ppm| < 0.5 with more\n\n## Real\n", "docs/history/v1/design/TIME_SYNC.md:495, docs/testing/TESTING.md:605")]
    return [("corpus", n, p, src.format(where), {}) for n, p, where in rows]


def _renderer():
    src = "the page of a gen_toc_cases I437 arm, exact page"
    rows = [("comment block closed by its end condition", "<!--\nx\n-->\n## Real\n"),
            ("indented code ends at its last code line", "    code\n\n    more\n\ntext\n"),
            ("fence in a list item", "- item\n\n  ```\n  ## Old\n  ```\n\n## Real\n"),
            ("fence in a block quote", "> ```\n> ## Old\n> ```\n\n## Real\n"),
            ("text indented into a nested item", "- item\n  - nested\n\n    text\n"),
            ("raw comment left open swallows a heading", "<span>\n<!--\n\n## Old\n</span>\n\n## Real\n"),
            ("open double-quoted value swallows the rest", '<div title="\n\n## Old\n\ntext\n'),
            ("open double-quoted value, then a heading and a paragraph", '<div title="\n\n## Old\n\ntext\n\n## Real\n'),
            ("open single-quoted value swallows the rest", "<div title='\n\n## Old\n\n## Real\n"),
            ("open double-quoted value in a list item", '- <span title="\n\n## Old\n\n## Real\n'),
            ("open double-quoted value closed by a later quote", '<div title="\n\n## Old\n\n<b title="x">\n\n## Real\n'),
            ("select swallows a heading", "<select>\n\n## X\n\n</select>\n\n\n## Y\n"),
            ("swallowed list", "<!-- a --> <!-- b\n- one\n- two\n"),
            ("tight list", "- a\n- b\n\n## Real\n"),
            ("task list", "- [ ] a\n- [x] b\n"),
            ("lone carriage return ends a line", "```\r```\n## Probe\n"),
            ("setext heading", "Alpha\n===\n"),
            ("two-line setext heading", "Alpha\nbeta\n---\n"),
            ("indented ATX heading", "   # H\n"),
            ("empty ATX heading", "##\n"),
            ("heading in a block quote with a closing run", "> ## Q ##\n"),
            ("heading in a list item with a closing run", "- item\n\n  ## Inner `x` ##\n"),
            ("heading in a referenced footnote", "[^1]: note\n\n    ## Same\n\n## Same\n\nref[^1]\n"),
            ("heading in an unreferenced footnote", "[^1]: note\n\n    ## FN\n\n## Top\n"),
            ("rendered heading text", "## a `b` *c*\n"),
            ("table in a block quote, bare", "> | a |\n> |---|\n> | b |\n"),
            ("pipe-led line", "text\n|a| b\n"),
            ("headings the parse moves out of an open table", "<table>\n***\n\n   ## H1\n\n## H2\n"),
            ("a heading after an open table and a stray closer", "## H1\n\n<table>\n-\n</pre>\n\n- [r]: /u\n## H2\n"),
            ("an item the parse swallows while its list renders", '- <div title="\n- two\n\n## Old\n'),
            ("a footnote heading follows the page's own", "[^1]: note\n\n    ## Same\n\n## Top\n\n## Same\n\nref[^1]\n")]
    return [("renderer", f"I437 arm page: {n}", p, src, {}) for n, p in rows]


def shapes(arm_fails=None):
    out = _from_515() + _reviews() + _family_two() + _corpus() + _renderer()
    for f in arm_fails or []:
        out.append(("arm", f"arm: {f['name']}", f["page"], "a gen_toc case-table arm the renderer answers differently from the old walk, exact page", {}))
    seen, uniq = set(), []
    for s in out:
        if s[2] in seen:
            continue
        seen.add(s[2])
        uniq.append(s)
    return uniq
