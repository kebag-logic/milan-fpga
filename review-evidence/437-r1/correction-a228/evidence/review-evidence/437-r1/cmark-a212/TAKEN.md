[A212] TAKEN

Branch: `437-cmark-gfm`, clean start at live dev `759da623072358afdb0e9d570a7b4b6a788492c9`. Sole author for #437 and #516 (they close together) per the [assignment](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5800600405). Manager A10; R237 and R238 review the head cold.

Authoritative references: the [owner decision](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5798044806) of 17:45; acceptance 1 as restated and amended in the #437 body; #516 body and its [17:45 decision](https://github.com/kebag-logic/milan-fpga/issues/516#issuecomment-5798045125); AGENTS.md 4, 6 and 7; CONTRIBUTING.md 6.1; REQ-VER-04; PR #515 reviews R237-1 to R237-4 and R238-1 to R238-3, read as a catalogue of shapes only.

Interpreted scope:
- The Contents walk stops classifying Markdown itself. `blocks()`, `line_kinds()` and `headings()` read the syntax tree of cmark-gfm, the renderer GitHub uses, through the `cmarkgfm` binding pinned to one version. This covers heading nodes with their source lines and level, container nesting, fenced and indented code, and raw HTML blocks.
- `check_em_dash.py` navigation provenance follows automatically, because it reads those functions.
- The emulation is deleted: the character-class table, every block expression, the paragraph, comment and closer state machines, and the decision-site guard module with its arms.
- Every existing case file stays, and each case is judged by the parser. An arm the old walk had wrong is converted only with a recorded GitHub rendering of its page.
- Unchanged: the TOC output contract (labels, anchors, separators, placement), the refusal policy, provenance, exemptions and budgets. No ratchet is widened.
- The docs install step goes into `.github/workflows/docs.yml`, cached by the hash-locked file, and its pin goes into `scripts/ci_events.py`.

Material decision, published before dependent edits:
1. **Tree access.** The binding's Python surface exposes only parse and render, but its extension exports the whole cmark-gfm C API (225 symbols). The walk declares the node calls it needs (children, type, source position, level, fenced flag, literal) and reads the tree through that same pinned library. It does not use `cmark_node_get_string_content`, which returns an unterminated buffer for an empty heading.
2. **HTML parse.** The #516 family is hidden during HTML parsing, not during Markdown block parsing. For the resumed #516 page, cmark-gfm emits `<span>\n<!--\n<h2 ...>Old</h2>\n</span>\n<h2 ...>Real</h2>`: both headings are block nodes, and the raw `<!--` hides them only once the HTML is parsed. So the walk parses cmark-gfm's own output, with source positions, using an HTML5 parser, `html5lib` 1.1 in the same lock. A heading is listed only when its element survives that parse. The standard library's `html.parser` is not used for two reasons: its comment handling changed in 2025 security releases, so its answer depends on the interpreter's patch level, and it has no tree construction, while GitHub hides a heading inside `<select>`, as R238-2 measured.
3. **Lock.** `tools/markdown/requirements.txt` pins `cmarkgfm==2025.10.22` (bundled cmark-gfm `0.29.0.gfm.13`), `cffi==2.1.1`, `pycparser==3.0`, `html5lib==1.1`, `six==1.17.0` and `webencodings==0.6.1`. It carries the sha256 of every wheel the hosted runner (CPython 3.12, x86_64) and this author's host (CPython 3.14, x86_64) need, and no sdist, so a source build is refused. A drifted release is refused by name.
4. **Heading text.** The parser decides that a line is a rendered heading and its level. For an ATX heading the label is read from its own source line with CommonMark 4.2's content rule, which keeps every existing label byte-identical. For a setext heading, which has no prior label contract, the label is the rendered text.

Validation plan:
- Commit the shape set: family one, the content-column cases, the twelve #516 variants, every shape R237 and R238 published, and the page of every converted arm. Record each shape's GitHub rendering (`POST /markdown`, mode gfm, through `gh api`) as request and response bytes with SHA-256 and date.
- Selftest arms check receipt integrity and parser headings against the recorded headings. A real-Git em-dash row per shape runs through the shipped gate.
- Compare the old and new walks over every tracked page on blocks, line kinds, headings with anchors, plan, provenance and refusals, and enumerate each difference.
- Run the full documentation gate set from `docs.yml`, `ci_events.py --check` and `--selftest`, and `check_py_idiom.py`.
- Record a named mutation per new property.
- Any disagreement between the parser and GitHub is reported as a finding, not pinned away.

Blockers: none.
