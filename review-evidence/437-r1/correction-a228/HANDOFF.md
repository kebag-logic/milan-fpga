# [A228] Handoff: PR #538 correction round 1 (issues #437 and #516)

Assignment: [#437 comment 5805766160](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5805766160).
It answers R237-5 ([5805567266](https://github.com/kebag-logic/milan-fpga/pull/538#issuecomment-5805567266)) and R238-4 ([5805762716](https://github.com/kebag-logic/milan-fpga/pull/538#issuecomment-5805762716)).

## Heads

| | |
|---|---|
| Reviewed head | `196cb7d99cb06631df514715979a5f82fbb1f7aa` |
| New head | `26a0cc3042300d5213edf7b1c0037a3ae2612ecd` (tree `dd03278237b213f237e911ce3c370e6471bc8be8`) |
| Source base | dev `759da623072358afdb0e9d570a7b4b6a788492c9` |
| Branch | `437-cmark-gfm`; the lane is clean and the gitlinks are unchanged |

- The round adds one commit on top of the reviewed head. Its subject is one line and it carries no trailers (checked on the raw commit object).
- The commit is local only. The assignment does not allow a push, so pushing it is the manager's step.
- Two earlier local heads of the same commit were superseded before handoff:
  - `6903f6f7`: `docs_check` refused a bare `CONTRIBUTING.md` reference.
  - `edbe7f31`: the tracked-depth figure read 7 and is really 8, and the depth-limit wording was imprecise.
- Their gate logs are kept in `gates-attempt-6903f6f7/` and `gates-attempt-edbe7f31/`.

Changed files (`196cb7d9..26a0cc30`): `CONTRIBUTING.md`, `docs/DOC_GENERATION.md`, `scripts/gen_toc.py`, `scripts/gen_toc_cases.py`, `scripts/gen_toc_renderer.py`, `scripts/gen_toc_renderer_cases.py`, `scripts/gen_toc_shape_cases.py`, `scripts/gen_toc_shapes.json`.
No budget or ratchet file changed. `check_em_dash.py` is untouched and still exactly 1000 lines.

## What changed, finding by finding

### F1 MAJOR (R237-5 F1 = R238-4 F1): the position guard

The guard is wider than letter case. A page can make the HTML parse read the renderer's position attribute on an element of its own in four ways:

- raw HTML in upper case;
- raw HTML in mixed case;
- a character reference in text (`&#100;ata-sourcepos=...`);
- a backslash escape in text (`data\-sourcepos=...`).

In the last two, a raw `<h2 title='` is left open and the paragraph closes the quote, so the parse reads the paragraph's text as attributes. cmark-gfm writes that text out decoded.

Measured at the reviewed head through the shipped gate on real commits (`receipts/emdash-e2e-spellings-at-196cb7d9.txt`):

- All four spellings list `Old <em dash> heading`.
- All four exempt the copied label: rc 0, 1 label exempt.

So a case-insensitive check on the page text would still leave two escapes. The candidate fix R238-4 probed (M22, `POSITION in text.lower()`) is my mutant A03, and it is killed.

The fix (`scripts/gen_toc_renderer.py`):

- **The renderer checks its own HTML.** `render()` also renders the page without positions, which is GitHub's own HTML. When that HTML spells the attribute in any ASCII letter case (`spells_position()`, `bytes.lower()`), the page renders nothing. `bytes.lower()` lowers the ASCII letters and nothing else, as the HTML parse does.
- **Positions are the only difference between the two renderings.** Identical once positions are removed on:
  - all 362 recorded shapes and 700 fuzz pages;
  - all 164 tracked pages (both in `receipts/position-only-difference-at-26a0cc30.txt`).
- **So every position the parse reads is one cmark-gfm wrote.** The heading-tag check (`tag == h{level}`) then handles a renderer position that an open raw tag absorbs.
- **The page is also refused by name** (`scripts/gen_toc.py` `refusals()`). A page whose text spells the attribute in any ASCII letter case is named with its line and column, as a page carrying one of the 26 refused characters is. The generator leaves it alone and the gate exempts nothing on it. This adopts R237-5 S2 and R238-4 S1.
  - It removes the destructive `--write` for such pages, which deleted their Contents block.
  - A spelling the text does not carry (a character reference or an escape) is not named. The renderer still reads that page as rendering nothing, which withholds.
- **The limitation text now matches** in CONTRIBUTING 6.1, `docs/DOC_GENERATION.md` and the module docstring. DOC_GENERATION.md also points at the file-view divergence in 6.1 (R237-5 S1).

Arms:

- **Renderer arms.** A forged page in each of the four spellings lists nothing, and the control page lists its four headings.
- **Refusal arms.** The attribute is refused in every case with its line and column. The note names it. A refused character and the attribute on one line are named in column order.
- **The lower-case arm still passes.**
- **The reverse mutant is killed.** A02 (guard back to the page text, case-sensitive) fails 8 TOC arms and 2 em-dash arms.

**R238-4's extra requirement: an arm that compares `headings()` labels and anchors with a recorded GitHub rendering.**

- `scripts/gen_toc_shapes.json` gains `file_view`: 11 pages recorded in the Markdown API's `markdown` mode, GitHub's file view, with each heading's anchor.
- For each page, `gen_toc_shape_cases.shown_in_file_view()` requires every heading `headings()` lists to be one the file view shows, in order: the same level, the same reader-visible text and the same anchor.
- The pages are the control, the four forged spellings, the two heading-tag pages, the strikethrough page, and pages nesting an element 201, 256 and 1101 deep.
- A self-check arm proves that the checker refuses a missing heading, a wrong text, a wrong anchor and a wrong level.
- The five file-view pages carrying `## Old <em dash> heading` are also real-Git em-dash rows. Whether GitHub rendered `Old` is decided by its anchor.
- At the reviewed head, 6 of the 11 fail this test; at the new head all 11 pass (`receipts/file-view-196cb7d9-vs-26a0cc30.txt`).

### R237-5 F2 MINOR: deep nesting, and a new depth finding

- `_nodes()` now walks the syntax tree with a stack, so a page nested past the interpreter's recursion limit is read.
- Measuring what GitHub does with such pages found a second escape (new, not in either review). Where GitHub nests an element 256 deep, that element's content and everything after it are lost. Measured on 2026-09-24:
  - 255 block quotes: all 255 are kept, the paragraph inside them (256 deep) is left empty, and the `## B` after them is gone.
  - 128 list levels (256 elements): the innermost item is empty and `## B` is gone.
  - 255 raw `<div>` tags: `B` lost, and an empty `<h2>` remains.
  - GitHub renders 254 block quotes, 199, 200, a heading in a 30-deep block quote, and a heading in a 12-deep or 30-deep list in full.
- The reviewed head listed `B` on the 256-deep page, a heading GitHub does not show. Past about 990 it crashed with a RecursionError: rc 1, the findings code, with a traceback.
- Fixed with `DEEPEST = 200`: a page whose parse nests an element deeper than 200 renders nothing.
- No tracked page nests an element deeper than 8 (`receipts/tracked-depth-and-write-at-26a0cc30.txt`).
- Arms:
  - an element 200 deep is read, and agrees with GitHub (gfm shape);
  - 201 deep lists nothing;
  - 1100 block quotes list nothing. That arm fails, not raises, when the recursive walk is restored.
- The file view records the 201, 256 and 1101 pages.
- Both shipped gates now answer the 1200-deep block-quote and list pages with rc 1 findings and 0 exempt, where the reviewed head crashed (`receipts/deep-pages-gates-196cb7d9-and-26a0cc30.txt`).

### R237-5 F3 MINOR: the own-element kinds

One arm each for `block_quote`, `code_block`, `thematic_break` and `table`: the lines of the block that an open raw comment swallows are commented.

`list` is observable, but only on a blank line that the list holds past an empty item. Fuzz page `s437212-0335` is the corpus instance. It is armed on the page `<span>\n<!--\n\n-\n\n- b\n`.

All six drops are killed:

- R237-5's own `mutate_own_element.py`: `receipts/r237-own-element-at-26a0cc30.txt`.
- My A11 to A16.

Observation (not fixed, proposed as a new issue):

- When a comment closes inside a container, the container's element is swallowed while a later line is not. `block_quote` and `list` then label that later, visible line `commented line`.
- Measured on two pages (`receipts/partial-swallow-containers-at-26a0cc30.txt`): the paragraph `> b` and the item `- c` render, yet are labelled commented.
- It affects labels only. Headings come from the shown elements, and a withheld label only withholds provenance.
- It predates this round.

### R238-4 F2 MINOR: three unarmed properties

- **M17**, the heading tag matched to its level: two arms, for `<div foo` and `<div title=` followed by `## Old`, `## Real`. Both pages are also gfm shapes, file-view pages and real-Git em-dash rows.
- **M15**, the drift refusal: `binding()` now calls `bind(installed)`. Three arms go through `bind()` itself:
  - the pinned releases bind;
  - cmarkgfm 2025.10.20 is refused by name;
  - a missing html5lib is refused by name.
- **M11**, strikethrough: the setext heading `a ~~b~~` lists `a b` / `a-b`, and GitHub's recording agrees in both modes.
- **R238-4 S3 adopted:** the attached extensions are spelled in an arm, so M10 (autolink) and M12 (task list) are killed too.

### Not adopted

- R237-5 S3 and R238-4 S4 (the "not installed (collections)" wording for an import-incompatible html5lib): message clarity only, outside the findings.
- R237-5 S4 (template, noscript and similar shapes): no rendering was asked for.
- R238-4 S2 (REGISTER_MAP.md:1866 anchor, byte-identical at base): outside #437. The manager decides whether it becomes an issue.

## Arm counts

- **TOC self-test: 1433 → 1501 (`MIN_ARMS` 1501).**
  - walk +5;
  - heading +11;
  - guard +4;
  - refusal +3;
  - shape +45: 10 new gfm shapes × 2, 11 file-view pages × 2, and 3 file-view coverage arms.
- **Em-dash self-test: 332 → 339.** The 7 new rows are the 2 heading-tag shapes and 5 file-view pages.
- **Fixture: 352 → 362 shapes, plus 11 file-view pages.**

## GitHub renderings sent

- 40 `POST /markdown` requests of synthetic pages. No repository page was sent and no repository state was written.
- Each request and response is kept byte for byte under `render-cache/<request sha256>.{req,resp,meta}`.
- 21 are in the fixture: 10 in gfm mode and 11 in the file view (`probes/pages-a228.json`, `probes/rendered-a228.json`).
- 19 are depth probes (`probes/pages-depth*.json`, `probes/rendered-depth*.json`).

## Validation at `26a0cc30` (all reproduced by `COMMANDS.md`)

- **Every `docs.yml` command, 96 runs, all rc 0.** The list is `gates/EXITS.txt`, with each command's output in `gates/logs/NNN.log`. The interpreter was a CPython 3.14.7 venv with the lock installed from its hashes plus `wavedrom==2.0.3.post3`, the HDL-reference lock and pyyaml, as `docs.yml` installs them. The runs cover:
  - the `docs-check` job: HDL reference, RV32 SDK installed and verified into a scratch HOME, compiler-absent audit, builder `ALL GATES PASS EXCEPT 11 NOT RUN` (litex absent), NVM, SoC, ratchets, idioms, `ci_events`, `act_ci --selftest`, archive, and the TOC gates;
  - the `wire-accountability` job;
  - the `docs-check-no-git` job, in a `git archive` export with no `.git`, which also passes the TOC and em-dash self-tests with no submodule content.
- **CPython 3.12.13**, in a venv holding only the lock, installed from its hashes:
  - `gen_toc.py --selftest` 1501/1501, `--verify-anchors` 147, `--check` 106 pages;
  - `check_em_dash.py --selftest` 339 and `--base 759da623`: 0 findings over 100 lines, 0 exempt.
- **`check_py_idiom`**: long module 10 ≤ 10, long function 9 ≤ 9. `git diff --check 759da623 HEAD` is clean.
- **Mutations, all at `26a0cc30`:**
  - my 23 (`receipts/mutations-a228-at-26a0cc30.txt`): 23 killed, each at an arm named for its property, with no traceback;
  - R238-4's `mutate.py`: 19 killed; M04, M06 and M22 do not apply because their lines were rewritten, and my A23, A01/A02 and A03 are their equivalents, all killed;
  - R237-5's `mutate.py`: 14 killed; M02, M03 and M16 map to A01, A23 and A03;
  - R237-5's `mutate_own_element.py`: 6 of 6 killed.
- **The reviewers' end-to-end probes, rerun at `26a0cc30`:**
  - R238-4 `emdash_spoof_e2e.sh`: the spoof variant is refused like the control, rc 1 with 0 exempt, and the attribute is named.
  - R237-5 `probe_emdash_gate.py`: neither forged page lists `Old`; 0 exempt.
  - My four-spelling probe: all rc 1, 0 exempt, where the reviewed head gave rc 0 with 1 exempt.
- **Tracked tree** (`receipts/tracked-pages-196cb7d9-vs-26a0cc30.txt`): 164 pages give identical refusals, blocks, line kinds, headings, plan, existing span, ownership, generated block and `apply()` under both heads. No tracked page is refused. `--write` would change no page gen_toc owns.

## Environment note

- The 3.14 venv was created with system site packages, as the assignment asked. pip therefore took the locked releases of `cffi` 2.1.1 and `pycparser` 3.0 from the system site, and `six` 1.17.0 from the user site.
- The 3.12 venv installed all six locked distributions from their hashes.
- The gates pass in both.
- R237-5's three scripts clear HOME, so the user site is invisible to them: `probe_emdash_gate.py`, `mutate.py` and `mutate_own_element.py`. Their first runs under the 3.14 venv were void because `six` could not be found, and were rerun with the 3.12 venv. Every receipt kept, including those in `receipts/superseded-edbe7f31/`, is from a valid run.

## Open risks and questions

1. **Some withheld pages are not named.** A page nested past 200, or one spelling the attribute only through a character reference or an escape, renders nothing but is not refused by name. So `--check` reports TOC drift and `--write` would drop its Contents block.
   - This is the S2 shape, and it only ever withholds.
   - Naming these pages would need the renderer inside `refusals()`.
2. **The partial-swallow container labels** (F3 observation above). Proposed as a new issue.
3. **The depth bound of 200 relies on a measurement.** It is a margin under GitHub's measured 256, taken on 2026-09-24. GitHub's pipeline can change.
4. **Local evidence only.** The author did not run the hosted CI, act, or a candidate merge with live dev.

## Acceptance (#437; #516 closes with it)

- 1: met on the committed set, 362 of 362 shapes. The #516 residual escape (F1) is closed in every spelling measured, and so is the depth escape.
- 2: unchanged and met.
- 3: every property both reviews listed now has an arm shown to fail when it is removed.
- 4: no tracked page changes.
- 5: every gate passes.

The completion ledger is the reviewers' to publish.
