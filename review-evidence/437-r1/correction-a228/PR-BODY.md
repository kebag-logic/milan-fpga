[A228] Read Contents navigation from cmark-gfm, the renderer GitHub uses; correction round 1

Closes #437
Closes #516

This follows the owner decision of 2026-09-23 17:45 ([#437 comment 5798044806](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5798044806)). The Contents walk's hand-written block and container classification is replaced by the renderer GitHub itself uses, pinned and hash-locked in the docs gates.

- The first three commits are A212's: takeover and material decision at [5800875179](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5800875179).
- The fourth answers R237-5 ([5805567266](https://github.com/kebag-logic/milan-fpga/pull/538#issuecomment-5805567266)) and R238-4 ([5805762716](https://github.com/kebag-logic/milan-fpga/pull/538#issuecomment-5805762716)), under the assignment [5805766160](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5805766160).
- Head `26a0cc3042300d5213edf7b1c0037a3ae2612ecd`.
- Base dev `759da623072358afdb0e9d570a7b4b6a788492c9`.
- Four one-line commits with no trailers.

## What changes

- **`scripts/gen_toc.py` no longer parses Markdown.**
  - `blocks()`, `line_kinds()` and `headings()` read one page model, built from cmark-gfm's syntax tree and an HTML5 parse of cmark-gfm's own HTML.
  - A heading is listed only when GitHub would keep it. That is how the #516 family is hidden: a heading after a raw `<!--` the page leaves open, inside an open quoted value, or inside a `<select>`.
  - An ATX label is still read off its own line, so every existing label and anchor is unchanged.
- **`scripts/gen_toc_renderer.py` (new): the binding.**
  - `cmarkgfm` 2025.10.22, which carries cmark-gfm 0.29.0.gfm.13, and `html5lib` 1.1. Another release is refused by name.
  - It reads a page as rendering nothing, which withholds every heading, in two cases:
    - cmark-gfm's HTML rendered without positions (GitHub's own) spells the position attribute in any ASCII letter case. Raw HTML in any case, or text through a character reference or a backslash escape, could otherwise put a position on an element of its own.
    - The parse nests an element more than 200 deep. Where GitHub nests an element 256 deep, it loses that element's content and everything after it.
  - The syntax tree is walked with a stack, not recursion.
- **`scripts/gen_toc.py` `refusals()`** also names a page whose text spells the position attribute, in any letter case. The generator leaves it alone and the gate exempts nothing on it.
- **`tools/markdown/requirements.txt` (new).** Every distribution is pinned to one version, with the sha256 of the CPython 3.12 and 3.14 wheels and no sdist.
- **`.github/workflows/docs.yml`** caches pip downloads keyed by the lock and installs it with `--require-hashes` before the first consumer. `scripts/ci_events.py` pins both steps.
- **`scripts/check_em_dash.py`.** Navigation provenance follows automatically. Without the renderer it answers `cannot judge` (rc 2).
- **Deleted:** the class table, every block expression, the paragraph, comment and closer state machines, and `scripts/gen_toc_guards.py`. Every existing case is kept and judged by the renderer.
- **`scripts/gen_toc_shapes.json` (new).**
  - 362 pages with GitHub's `POST /markdown` gfm rendering, as exact request and response bytes with SHA-256, recorded on 2026-09-23 and 2026-09-24.
  - 11 `file_view` pages recorded in `markdown` mode, GitHub's file view, with each heading's anchor. On each, every heading `headings()` lists, label and anchor, must be one GitHub shows.
- **CONTRIBUTING.md 6.1, docs/DOC_GENERATION.md and docs/testing/RUNNING_TESTS.md** state the basis, the install and the four measured limits. Each limit withholds a heading and grants no exemption.

## Correction round 1 (R237-5, R238-4)

| Finding | Resolution | Arm that fails when it is removed |
|---|---|---|
| F1 MAJOR, both reviews: the guard is case-sensitive | The guard reads GitHub's own HTML in any ASCII case, which also closes a character-reference and a backslash-escape spelling found in this round. The page is refused by name when its text spells the attribute | Four forged pages list nothing; refusal arms; 11 file-view label and anchor arms; 5 real-Git em-dash rows. The reverse mutant is killed |
| R237-5 F2: recursion on deep pages | The walk uses a stack. Pages nested past 200 render nothing: GitHub loses what it nests 256 deep, and the reviewed head listed a heading GitHub dropped | Depths 200 (read), 201 and 1100 (withheld) |
| R237-5 F3: five own-element kinds unarmed | One arm per kind; `list` is armed on the blank line it alone holds | All six drops are killed |
| R238-4 F2: M17, M15, M11 | Heading-tag arms, `bind()` drift arms, and a strikethrough arm with its GitHub recording; the extensions are spelled (S3) | All three killed, plus M10 and M12 |

## Acceptance (#437; #516 closes with it)

| # | Result | Evidence |
|---|---|---|
| 1 | Met by construction | 362/362 shapes agree with their gfm rendering, 2 carrying GitHub's hidden footnote label (N1). All 11 file-view pages list only what GitHub shows. The #516 residual escape is closed in every spelling measured |
| 2 | Met: listed | The five family-two forms are listed, and their anchors equal GitHub's file-view ids |
| 3 | Met | 23 mutations of this round's properties are killed at named arms. The reviewers' campaigns at the head: R238-4 19 killed, R237-5 14 and 6/6 killed. Every mutant not applied maps to an equivalent that is killed |
| 4 | Met for navigation | 164 tracked pages give identical answers at the reviewed head and this head, and `--write` changes no page gen_toc owns |
| 5 | Met | 96 `docs.yml` command runs exit 0 at the head. TOC self-test 1501/1501 (floor 1501), em-dash 339 arms. The same gates pass under CPython 3.12.13. No ratchet widened |

## Findings (parser against GitHub), reported

- **N1.** GitHub's gfm output opens a referenced footnote's section with a visually hidden `Footnotes` h2, which the pinned cmark-gfm does not emit. It is withheld and held as `github_only`.
- **N2.** GitHub's file view parses some raw HTML differently from gfm mode: `<?`, `<select>` and `<xmp>`, on 8 of 1,052 pages measured on 2026-09-23. The manager ruled the file view the reference and this family a documented, directed limitation (CONTRIBUTING 6.1).
- **N3 (pre-existing).** The anchor rule reads raw Markdown, so inline raw HTML in a heading anchors differently.
- **Observed, not fixed.** When a comment closes inside a block quote or list whose element it swallowed, a later visible line is labelled commented. This affects labels only, withholds only and predates this PR, and is proposed as a new issue.

## Validation

- **Constraints.**
  - The gates run without submodules, without git metadata (`docs_check`, `check_feature_status`), and on CPython 3.12.
  - They refuse with rc 2 when the renderer is missing or drifted.
  - Both gates answer pages nested 1200 deep, where the reviewed head crashed.
- **Fuzz.** 700 seeded pages rendered through GitHub agree with the renderer in gfm mode.
- **GitHub renderings.** This round sent 40 requests of synthetic pages.
- **Receipts.** In the author packets: HANDOFF, COMMANDS and MANIFEST for A212, and the same for A228.
