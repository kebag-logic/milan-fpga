[A190] DECISION: a container-aware block walk replaces the flat paragraph and container classification

Targeted patches cannot close this family. At the base, several flat-walk errors cancel on the same page. Fixing one exposes the next: both root causes of R237-2 F1, and F2's flat-item trigger, are base errors that the base's other errors used to hide.

Choice (stdlib only):
- A container walk tracks block quotes, list items and GFM footnote definitions with CommonMark 0.31.2 5.1 and 5.2 continuation, including lazy paragraph continuation and the interruption rules. It runs the existing leaf machine on each line's content inside its containers.
- It decides three things:
  1. A lone type-7 tag opens raw HTML unless the deepest block the line matches is an open paragraph. This is the renderer's rule, and GitHub's recorded HTML in R237-2's receipts shows it.
  2. A fence, a raw HTML block or a comment opened inside a container ends when that container ends.
  3. Which lines GitHub emits verbatim as raw HTML, including types 3 to 5. The rendered comment is read from those lines by a model of HTML's tokenizer:
     - `<!--` opens only in data state: not inside a quoted attribute value, a bogus comment (CDATA outside foreign content, `<?`, `<!X`) or a tag GFM's tag filter leaves alone.
     - `-->`, `--!>`, `<!-->` and `<!--->` close.
     - In Markdown text, a closer counts only inside inline raw HTML (CommonMark 6.6, with GitHub's uppercase declarations), never in a code span or after an escape.
     - Footnote content is excluded, because GitHub moves it to the page end.
- A comment opened in prose ends at the first line that is not paragraph text.
- Line labels stay the base walk's column-0 labels. Tracked-page classification (AC4) and every existing arm are therefore kept, and family two stays omitted as documented.

Prototype evidence, rendered with GitHub `gfm`: 0 regressions against the base. The pages checked are all 1,367 public renderings, R237-2's 2,070-page corpus and about 17,000 new generated pages, with 2,300 fresh renders where the walks differ. Every page where the walk still disagrees with GitHub disagrees only on a family-two heading. The same mechanism also closes R238-r1 F3's P02, P03 and F09 and R237-2 S1.

Structure: `scripts/gen_toc.py` is at 999 of its 1,000-line ratchet. The walk becomes three modules, split by responsibility as CODE_QUALITY rule 1 allows:
- `gen_toc.py` keeps the leaf machine, every Markdown expression and character class, and the orchestration.
- `gen_toc_containers.py` holds the container layer.
- `gen_toc_html.py` holds the rendered-comment model.

The class guard enumerates the decision sites of all three. The owner guard still binds the four modules beside the walk. No ratchet widens.

This supersedes the current head's content-column rule and the rendered-comment rule of [5789133990](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5789133990). Finding identities, severities and lenses stay with their reviewers.
