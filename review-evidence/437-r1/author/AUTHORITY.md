# Public authority read for #437

- Repository AGENTS.md; CONTRIBUTING.md, especially 5 and 6.1; docs/README.md; REQUIREMENTS.md; docs/development/CODE_QUALITY.md rule 12.
- Issue #437: https://github.com/kebag-logic/milan-fpga/issues/437
- Selected decision: https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5775771538
- Original R85-4/R86-5 public comments cached as R21.md and R22.md, with all PR #428 public comments in pr428-comments.json. Neither report attaches the locally named original fixture JSON/HTML.
- CommonMark 0.31.2 sections 4.2, 4.3, 4.4, 5.2, 5.3; 2.2 tab stops and 4.6 type-7 paragraph guard: https://spec.commonmark.org/0.31.2/ . Source https://raw.githubusercontent.com/commonmark/commonmark-spec/0.31.2/spec.txt cached as commonmark-0.31.2.txt.
- GitHub's footnote implementation evidence: https://github.com/github/cmark-gfm/blob/master/src/blocks.c . Public source cached as cmark-gfm-blocks.c; parse_footnote_definition_block_prefix requires four indentation columns for continuation, while blanks persist. This is source evidence, not an assertion that the hosted renderer runs that exact master revision. Direct synthetic GFM results are the footnote-boundary oracle here.
- Live GFM evidence: POST /markdown, mode gfm, context kebag-logic/milan-fpga. Only synthetic inputs; every request/response/UTC is in renderer-cache.json, also published in the issue's renderer receipt. Two requested GitHub Docs URLs were unavailable through the web tool; no claim depends on their absent content.

The CommonMark item rules use marker width plus 1-4 padding columns; over-four padding and empty items use one. A blank ends an empty item, but nonempty items can retain subsequent paragraphs. Item content and ordinal 1 are required to interrupt a paragraph. Fixtures hold those choices at positive and negative boundaries without changing existing column-zero block labels or the refusal policy.
