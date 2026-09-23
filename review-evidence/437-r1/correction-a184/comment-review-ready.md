[A184] REVIEW READY

Commit: `4741498f3b2b4f67f431037d327c96cf65691278`
Tree: `ee70aaf8faadbced21dfdd0cf7719597e9fbe8eb`
Branch `437-container-paragraph-scopes`, clean tree and index, local only, not pushed. It descends from live dev `483a133ed08867ea0d300d2b4a027b5b48a4282f` (still the dev tip at 04:51 UTC) through merge `a09ff881`. The paths were disjoint: the intersection is empty and the issue patch is byte-identical before and after the merge (SHA-256 `1fed0345...211fe`). The four gitlinks and `.gitmodules` are unchanged. Both commits have one-line subjects with no trailers.

Changed:
- `scripts/gen_toc.py` (999 lines, ratchet 1000):
  - The rendered-comment rule from the [decision](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5789133990).
  - `<!-->` and `<!--->` are complete comments.
  - The docstring states the rule and its residues.
  - The arm floor rises from 909 to 1091.
- `scripts/gen_toc_family_one.json` (51 shapes) and `scripts/gen_toc_comment_shapes.json` (40 controls, including #516's twelve variants). Each shape carries GitHub's `gfm` rendering: exact request bytes, response bytes, both SHA-256 values and the rendered headings.
- `scripts/gen_toc_container_cases.py`: two selftest arms per shape (receipt integrity, then walk against rendering) and a real-Git em-dash row per shape.
- CONTRIBUTING 6.1: the rule and its two residue directions.

Validation at this head (all exit 0):
- TOC `--selftest` 1091/1091, `--check` 105 pages, `--verify-anchors` 144 links, `--sites` 27.
- Em-dash `--selftest` 345 arms. `--base 483a133e` gives 0 findings over 20 added lines; `--base 88e9276b` gives 0 over 32.
- `docs_check` and its selftest, doc style and its selftest, doc paths.
- Python idiom and its selftest: long module 10 <= 10, long function 9 <= 9.
- Hygiene; naming, fail-fast, test-evidence, control-flow and cohesion measures; TODO ownership, ci_events, feature status, solution, submodule and gPTP docs, archive.

That is 33 commands. No budget file changed.

Acceptance:
- **Restated AC1: met by author evidence.**
  - The fixture covers bullet, star, ordered and two-digit ordered items resumed at and past the content column. Each is followed by an inline and an unknown tag, outside and inside the item.
  - It also covers the two-digit marker below its wider column and the one-space, four-space, quote, footnote and tab boundaries.
  - Each of the nine R86-5 descriptions maps to a named shape (`r86_5` field).
  - All 91 shapes were re-rendered fresh at this head and are byte-identical to the fixture. The walk agrees with the recorded rendering for all 91.
  - The two-digit shapes at or past column 4 are decided by the flat four-column code reading. The wider column is held by the below-column boundary.
- **No regression vs `88e9276b`.** A replay covers 695 unique pages with recorded renderings: every public R237, R238, A168 and A172 receipt plus this author's. It finds 0 regressions (the starting head had 6, the #516 resumed variants). There are 255 fixes; 21 pages disagree identically at base and head, and 4 disagree differently.
  - Fresh re-renders of R238's 62 probes, R237's 45 controls and #516's twelve variants: 103 agree, 0 regress.
  - R238 C01-C08, D01-D07, P01 and P04, R237's F1 matrix and F3 marker controls, and all twelve #516 variants agree.
  - The 16 pre-existing items are family-two omissions and the #495 residues P02, P03 and F09.
  - All 707 base-era arm pages classify identically under the base, starting and new walks.
- **AC2** unchanged: the five family-two forms stay documented as omitted.
- **AC3**: 16 new named mutations are killed at named arms in the TOC and em-dash selftests. Two receipt-only mutations are read only by the TOC selftest. All 23 A172 mutants still fail at their required arms.
- **AC4**: zero classification differences across the three walks on the 163 pages of each of the base, dev and head trees. The base digest matches R238-r1's.
- **AC5** as above.

Open risks/questions: rendered-comment residues are documented with their direction.
- Withholding: `--!>`, or a non-comment inline tag carrying `-->`, closes the comment for the renderer only.
- Escape, already present at the base: a code-span comment, or an escaped `-->` after a prose `<!--`, closes it here only.

R238 F3 (#495) was not adopted. Finding identities, severities and lenses stay with R237 and R238. R237 F2 is for re-judgement against the restated criterion.

Remains for the manager:
- Push and PR #515 update; a proposed body is in the packet.
- Publication of the author packet (HANDOFF, PR-BODY, COMMANDS, receipts, reproducible scripts).
- Full native and builder banks, trusted act, hosted contexts, current-candidate validation, and dispositions of #516 and #495.

Remains for reviewers: R237 and R238 cleared-context re-review of the published head with reviewer-owned five-lens coverage. Then maintainer merge authorisation.

This author did no push, PR edit, merge, act/Docker, full bank run or delegation. Stopping at this head.
