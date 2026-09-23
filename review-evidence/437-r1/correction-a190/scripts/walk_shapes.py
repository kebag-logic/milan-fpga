#!/usr/bin/env python3
"""The shapes of scripts/gen_toc_container_walk.json: (name, pins, page).

`pins` names the finding or rule a shape holds. Every page carries `## Old`
so the em-dash real-Git row can copy its label; `## Real` shows recovery.
"""
F = "```"
T = "\n## Old\n\n## Real\n"
ESC = "\ntext\n\n" + F + "\n## Old\n" + F + "\n\n## Real\n"
OPEN = "<div>\n<!--\n</div>\n\n## Hidden\n\n"


def shapes() -> list[tuple[str, str, str]]:
    """Every fixture shape, in order."""
    hold = "R237-2 F1: a tag under a nested block opens raw HTML in the item"
    life = "R237-2 F1: a block opened in an item ends with the item"
    empty = "R237-2 F3: an empty item's first line meets no paragraph"
    f2 = "R237-2 F2: a comment opener outside HTML's data state opens nothing"
    raw = "raw HTML the walk reads as the page's HTML parser does"
    close = "a closer in Markdown text counts only inside inline raw HTML"
    prose = "a comment opened in prose ends with its paragraph"
    rows = [
        ("nested quote, tag opens HTML", hold, f"- item\n  > quote\n  <span>\n  {F}\n" + T),
        ("nested quote, in-item fence would escape", hold, f"- item\n  > quote\n  <span>\n  {F}\n" + ESC),
        ("nested bullet, tag opens HTML", hold, f"- item\n  - nested\n  <span>\n  {F}\n" + T),
        ("nested bullet, in-item fence would escape", hold, f"- item\n  - nested\n  <span>\n  {F}\n" + ESC),
        ("nested ordered, pre inside the HTML block", hold, "- item\n  1. nested\n  <span>\n  <pre>\n" + T),
        ("nested footnote, tag opens HTML", hold, f"- item\n  [^1]: note\n  <span>\n  {F}\n" + T),
        ("table in item, tag opens HTML", hold, f"- item\n\n  | a |\n  | - |\n  <span>\n  {F}\n" + T),
        ("quote-first item, tag opens HTML", hold, f"- > quote\n  <span>\n  {F}\n" + T),
        ("lazy line after nested quote, tag opens HTML", hold, f"- item\n  > quote\nlazy\n  <span>\n  {F}\n" + T),
        ("thematic break in item, tag opens HTML", hold, f"- item\n  ***\n  <span>\n  {F}\n" + T),
        ("live bullet paragraph, in-item fence", life, f"- item\n  <span>\n  {F}\n" + T),
        ("live bullet paragraph, in-item fence would escape", life, f"- item\n  <span>\n  {F}\n" + ESC),
        ("live ordered paragraph, in-item pre", life, "1. item\n   <span>\n   <pre>\n" + T),
        ("task item, in-item fence would escape", life, f"- [ ] item\n  <span>\n  {F}\n" + ESC),
        ("resumed paragraph, in-item fence would escape", life, f"- item\n\n  text\n  <span>\n  {F}\n" + ESC),
        ("R238 P02 tag after a blank in the item, then fence", life,
         "- item\n\n  <span>\n" + F + "\n\n## Old\n" + F + "\n\n## Real\n"),
        ("R238 P03 div after a blank in the item, then fence", life,
         "- item\n\n  <div>\n" + F + "\n\n## Old\n" + F + "\n\n## Real\n"),
        ("R238 F09 tag after a blank in the item, heading after", life,
         "- item\n\n  text\n\n  <span>\n## Old\n  </span>\n\n## Real\n"),
        ("empty item, tag opens HTML", empty, f"-\n  <span>\n  {F}\n" + T),
        ("empty item, in-item fence would escape", empty, f"-\n  <span>\n  {F}\n" + ESC),
        ("empty item kept by a blank of its column", empty, "-\n  \n  text\n<span>\n## Old\n</span>\n\n## Real\n"),
        ("empty item ended by a shorter blank", empty, "-\n \n  text\n<span>\n## Old\n</span>\n\n## Real\n"),
        ("lazy indented line continues a nested quote", "lazy continuation",
         "- item\n  > quote\n      code\n  <span>\n## Old\n  </span>\n\n## Real\n"),
        ("lazy indented comment opener is prose", "lazy continuation", "> quote\n    <!-- x\n" + T),
        ("indented comment opener continues a paragraph", prose, "text\n    <!-- x\n" + T),
        ("a quote's optional space leaves a raw opener", raw, ">    <!--\n" + T),
        ("a continued quote's optional space leaves a raw opener", raw, "> quote\n>    <!--\n" + T),
        ("double-quoted attribute", f2, '<div title="<!--">\n' + T),
        ("inline tag attribute", f2, '<span title="<!--">\n' + T),
        ("a quoted value hides a greater-than", f2, '<div title="a > <!--">\n' + T),
        ("attribute inside a block", f2, '<div>\n<img alt="<!-- x">\n</div>\n' + T),
        ("CDATA is a bogus comment", f2, "<div>\n<![CDATA[<!--]]>\n</div>\n" + T),
        ("--!> closes on its line", f2, "<div>\n<!-- a --!>\n</div>\n" + T),
        ("--!> closes on a later line", f2, "<div>\n<!--\n--!>\n</div>\n" + T),
        ("inline tag closes after the block", f2, '<div>\n<!--\n</div>\n\ntext <a title="-->"> more\n' + T),
        ("item block ends before a code span", f2, "- item\n\n  <div>\ntext `<!--` more\n" + T),
        ("item block ends before an escape", f2, "- item\n\n  <div>\ntext \\<!-- more\n" + T),
        ("item block ends before an inline attribute", f2, '- item\n\n  <div>\ntext <a title="<!--"> more\n' + T),
        ("tag filter leaves the attribute as text", raw, '<div>\n<textarea title="<!--">\n</div>\n' + T),
        ("a greater-than ends the bogus comment", raw, "<div>\n<![CDATA[ a > <!-- ]]>\n</div>\n" + T),
        ("type-5 block", raw, "<![CDATA[ a > <!-- ]]>\n" + T),
        ("type-3 block", raw, "<? a > <!-- ?>\n" + T),
        ("type-4 block", raw, "<!X a > <!--\n" + T),
        ("lowercase declaration is no block", raw, "<!x a > <!--\n" + T),
        ("spaced dashes close nothing", raw, "<div>\n<!-- a -- >\n</div>\n" + T),
        ("a bang right after the opener closes nothing", raw, "<div>\n<!--!>\n</div>\n" + T),
        ("raw HTML in an item", raw, "- <div>\n  <!--\n" + T),
        ("raw HTML in a quote", raw, "> <div>\n> <!--\n" + T),
        ("R237-2 S1 opener four columns into an item", raw, "- item\n\n    <!--\n" + T),
        ("R237-2 S1 opener after a tag four columns in", raw, "- item\n\n    <div><!--\n" + T),
        ("single-quoted attribute closes", close, OPEN + "text <a title='-->'> more\n" + T),
        ("unquoted attribute closes", close, OPEN + "text <a title=--> more\n" + T),
        ("comment with dashes closes", close, OPEN + "text <!-- a -- b --> more\n" + T),
        ("processing instruction closes", close, OPEN + "text <?-->?>\n" + T),
        ("uppercase declaration closes", close, OPEN + "text <!X -->\n" + T),
        ("lowercase declaration is text", close, OPEN + "text <!x -->\n" + T),
        ("CDATA closes", close, OPEN + "text <![CDATA[-->]]>\n" + T),
        ("tag across lines closes", close, OPEN + 'text <a\ntitle="-->"> more\n' + T),
        ("code span hides the tag", close, OPEN + 'text `` <a title="-->"> `` more\n' + T),
        ("escape hides the tag", close, OPEN + 'text \\<a title="-->"> more\n' + T),
        ("prose bang closer is text", close, OPEN + "text --!> more\n" + T),
        ("attribute bang closer closes", close, OPEN + 'text <a title="--!>"> more\n' + T),
        ("footnote content is read at the page end", close, OPEN + "[^1]: n <!-- x -->\n" + T),
        ("table cell comment closes", close, OPEN + "| a <!-- x --> |\n| - |\n" + T),
        ("tag filter keeps the attribute's closer", close, OPEN + 'text <textarea title="-->"> more\n' + T),
        ("raw closer after a type-7 opener", close, "<span>\n<!--\n\n## Hidden\n\n<div>\n--!>\n</div>\n" + T),
        ("heading after a prose opener", prose, "text <!--\n## Old\n\n## Real\n"),
        ("heading after a code-span opener", prose, "text `<!--` more\n## Old\n\n## Real\n"),
        ("heading after a table-cell opener", prose, "| a <!-- |\n| - |\n## Old\n\n## Real\n"),
        ("list item after a prose opener", prose, "text <!--\n- item\n## Old\n\n## Real\n"),
        ("blank after an opener in an item", prose, "- item <!--\n\n## Old\n\n## Real\n"),
    ]
    return rows
