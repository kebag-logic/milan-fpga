# HANDOFF — lane 895 ([A775]), round 11

**Status (2026-11-16): REVIEW READY at `16ba667d` (local, not pushed), posted once on #895 as
issuecomment-6902951918 (REVIEW-READY-COMMENT.md; the posted body checked).** One markdown-only commit on the PR's `1215bd82`.

Assignment: the manager's round-11 relay. R835-5 NEGATIVE (PR #901 issuecomment-6901818182; report at
`review-evidence/895-r1/reviews/R835-5/REPORT.md`, archive `b2f93194`, read in full, round11/reviews/) with one MINOR
(F1), RS1 and RS2; R836-5 POSITIVE (issuecomment-6901691558) with RS1.

## Answers

| Finding | Answer | Where |
|---|---|---|
| R835-5-F1 | the seven statements restated as this head's or bound by short commit; the sweep's three more (`:2595`, `:2604`, `:2618`) and FR_NFR 383's 7B-composition pace clause too | SPLIT_CONTROL_MEMORY.md, FR_NFR.md, plat/README.md |
| R835-5-RS1 | "held 124,876 B" | SPLIT_CONTROL_MEMORY.md:515 |
| R835-5-RS2 | "its bound at 1x1/1if was, on #894's head," | SPLIT_CONTROL_MEMORY.md:2529 |
| R836-5-RS1 | the roles: starts and verdicts linked, no "(next)"; R835-6 the one delta reviewer | PR-BODY.md |
| R835-5-S2 | the phrase sweep (round11/scripts/phrase_sweep.py) run, every hit fixed | receipts/docs/superseded-inventory.md |
| R835-5-S1, R835-4-S3 | retained (non-markdown) | |

Verification: the review's f1_sites.py 0 of 7 present (receipts/docs/f1-sites.txt); the inventory (inventory.py) 201
figure hits, 0 unclassed, none a superseded figure as this head's; the phrase sweep, README lines before `cec88385`
listed as dev-soft-core's.

## Paths after `1215bd82`

docs/design/SPLIT_CONTROL_MEMORY.md, docs/reference/FR_NFR.md, sw/firmware/ctrl/plat/README.md: markdown only. The merge
candidate of `1215bd82` carries its native bank.

## Gates at `16ba667d` (fresh clean clones)

- docs.yml, every job: failed 0; verify_wf.py docs.yml: 61 ran, 34 reasoned, 0 bad (gates/verify-docs.md).
- firmware-unit: failed 0, 6 steps rc 0, fw_coverage PASS.
- lane gates (diffcheck_base, diffcheck_merged, py_idiom, cpp_idiom, docs_check): rc 0.
- worktree: check_doc_style, check_doc_paths, check_gptp_docs, check_em_dash rc 0.

## Run history

- 22:42 relay read; R835-5 report and R836-5 comment fetched; HEAD 1215bd82 clean, no units.
- 22:4x the seven fixes and both residues; phrase sweep; three more fixed; FR_NFR 383's composition clause; f1_sites 0
  of 7; inventory rebuilt; doc checks rc 0; `16ba667d`.
- 22:48-00:0x gate units (pool and pick8): all green.

## For the manager

- Push `895-talker-redeclare` at `16ba667d`; replace PR #901's body with round11/PR-BODY.md.
- R835-6 reviews the markdown delta `1215bd82..16ba667d`.
