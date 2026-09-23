[A184] MATERIAL DECISION: rendered-comment rule for the six resumed #516 variants

The six resumed variants on #516 agreed at base `88e9276b` by accident. The flat walk read `  text` as a top-level paragraph, so the column-0 tag continued it and `<!--` opened a type-2 comment that never closed. The family-one fix now correctly opens a type-7 block at that tag. The `<!--` then sits inside raw HTML, and the walk lists `Old`/`Real` where GitHub renders neither. A three-way replay of all 597 unique pages in the public R237, R238, A168 and A172 renderer receipts shows these six are the only regressions at the starting head `b5e6c23e`.

Measured contract: 42 fresh synthetic `gfm` renders, with exact request/response bytes to be published in the packet. The renderer passes raw HTML block content through. A `<!--` left open there hides the rest of the page until a `-->` appears in raw HTML: a later HTML block line of type 1, 6 or 7, a type-2 comment block, or an inline comment. The same holds inside list items and quotes. A `-->` in paragraph, heading, code span, indented code or fence text is escaped and closes nothing. `<!-->` and `<!--->` are complete empty comments, as in CommonMark 0.31.2 section 6.6.

Bounded rule for `scripts/gen_toc.py`:
- `blocks()` keeps a rendered-comment flag. It reads the flag with the existing `_comment_after` on lines it labels raw HTML or commented, and on prose lines carrying `<!--`.
- While the flag is open, a prose line is labelled commented, so no heading is listed. Block classification and paragraph/item state are otherwise unchanged.
- `_comment_after` treats `<!-->` and `<!--->` as complete, so the new flag does not hide a heading the renderer shows.

Effect:
- The six resumed variants agree again. The six first-paragraph counterparts, which disagreed at the base, also agree.
- Without a raw-HTML comment, the flag mirrors the existing comment state, so the classification of such a page is unchanged.
- No tracked page carries an unclosed comment in an HTML block, or `<!-->` or `<!--->`.
- The rule only removes headings, so it cannot list a heading the starting head omits.

Residues are stated with their direction in the docstring and CONTRIBUTING 6.1:
- Withholding: `--!>`, and a non-comment inline tag carrying `-->`, close the rendered comment for the renderer only.
- Escape, also present at the base: a closed comment inside a code span, and an escaped `-->` after a comment the walk opened in prose, close it here only.

No exemption, provenance or ratchet change. #516's remaining disposition stays with the manager; this lane does not edit it.
