[A10] Raised out of a review of PR #428 (issue #413), which measured it and correctly declared it outside that lane.

## What is wrong

`scripts/gen_toc.py` decides where a fenced code block and a type-1 HTML block end by reading Python's notion of whitespace, which is wider than the one the renderer applies. Two decisions are affected, both present at the current dev tip and unchanged by #413:

- the closing fence, at the `not m.group(2).strip()` test: CommonMark 4.5 allows only spaces or tabs after a closing fence sequence, and `str.strip()` also removes 25 other characters (line tabulation, form feed, U+001C to U+001F, U+0085, U+00A0, U+1680, U+2000 to U+200A, U+2028, U+2029, U+202F, U+205F and U+3000).
- the type-1 end condition, at the `</%s\s*>` pattern: end condition 1 of CommonMark 4.6 names `</pre>`, `</script>`, `</style>` and `</textarea>`, with nothing but the tag inside, and `\s` again admits the same 25.

## What it costs

A heading placed after a closing fence that carries one of those characters, or after `</pre` plus one of them plus `>`, is listed in the generated contents while the renderer leaves it inside the block and shows no heading. The reviewer measured 25 rows for the fence and 27 for the type-1 case, plus one carriage-return row, all against the live renderer, and the behaviour is identical at the base of #428 and at its head.

That is the escape direction: a contents entry, an anchor and, through the em-dash gate's provenance exemption, a waiver for a label mirrored from a heading the page does not render.

## Why it is not urgent

No tracked page carries any of the 25 characters, and none carries the shapes at all, so nothing on the tree is affected today. There is also no gate that keeps those characters out of Markdown: the hygiene populations exclude Markdown and the documentation scrub has no such rule. So the escape is reachable by any future page.

## Acceptance

1. Each of the two decisions reads the class the renderer applies at that position, or the walk refuses input it cannot answer for, naming file, line and character.
2. Whichever is chosen is held by an arm that fails when the class is narrowed back, one arm per position.
3. The rows the review measured (the fence rows and the type-1 rows, including the carriage-return row) agree with the renderer or fall in a family declared in the source and in the documentation with its direction and its measured boundary.
4. The same sweep is run at the base to show the change moves only these rows.

## Notes

This sits next to #437 and next to the same family inside #413, which is closing its own positions in its own lane. Whoever takes this should read the round-9 review on PR #428 first: it names the exact lines, the character set and the row counts, and its sweep tool is the instrument to reuse.
