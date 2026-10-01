[A482] Design media-clock following of one selected AAF or CRF source (#629, lane M1)

## Contents

- **[Status](#status)**: design only, one docs commit, `629-media-clock-follow` -> `dev`, awaiting the #629 decision.
- **[Linked Issue / roles](#linked-issue--roles)**: relates to #629; executor and reviewers.
- **[Description](#description)**: the design page, its index row, and the decisions it asks for.
- **[Authoritative references](#authoritative-references)**: the Milan, IEEE 1722.1 and IEEE 1722 clauses read.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: the branch and the pinned Markdown environment.
- **[How to validate](#how-to-validate)**: the gates, and the one area measurement the page quotes.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what the page does not establish.
- **[Definition of Done](#definition-of-done)**: the merge bar.

## Status

Design only, for decision. One commit, `78d4fef220c0ad4873a89b138828c0543c2bcad0`, on dev `d4dd742679b902b2bc5eedf89d525066d59aafbb`, `629-media-clock-follow` -> `dev`. Documentation only: no RTL, builder, generator, configuration or processor change. Every gate below rc 0 at `78d4fef2`.

## Linked Issue / roles

Relates to #629 (lane M1, the design item of its body; the implementation, simulation and bench items stay open). The lane's assignment is [#629 comment 5935051587](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5935051587).

Executor: `[A482]`
Internal cleared-context reviewer: to be assigned
External reviewer: to be assigned

## Description

| File | Change |
|---|---|
| `docs/design/MEDIA_CLOCK_FOLLOWING.md` (new) | The design for following one selected AAF or CRF talker's media clock |
| `docs/README.md` | Its row in the design index (the "Architecture and integration" table) |

The page holds:

- **Clause findings**, by question. (a) Milan v1.2 5.3.3.6 is a minimum set: it neither requires nor forbids an INPUT_STREAM source on an AAF input beside the CRF input's; no clause sets an order; IEEE 1722.1-2021 7.2.32 caps the list at 216. (b) On a lost stream the selection is kept (Milan v1.2 5.3.11.1, 5.4.2.15) and holdover is permitted (IEEE 1722-2016 4.4.4.3, 4.4.4.7 NOTE, 10.4.3). (c) The 4.4.4.3 disruption and echo shalls name CRF only; applying them to a followed AAF stream is permitted and recommended. (d) Seven places where the current reading is wrong, among them the exclusive reading of 5.3.3.6, BAD_ARGUMENTS attached to Milan 5.4.2.15/.16 instead of IEEE 1722.1-2021 7.2.32 and Table 7-141, Milan 7.2.2 and 7.2.3 cited for restrictions they do not make, and two stale RTL comments.
- **A map of the current state**, every fact at `path:line` on dev `d4dd7426` (processor paths at its pin `b2db3a97`).
- **The design**: an AAF clock meter that decimates the selected stream's presentation timestamps to the CRF 96-sample spacing and feeds the existing servo in its own units; one widened selection decode; the source switch; lock loss and holdover; `mr`; the CRF output and A2; the CLOCK_DOMAIN counters; area.
- **The change lists**: every parent-visible change, and a cross-repository plan for the protocol processor under its own issue (no processor RTL change is needed; its documentation and tests change).
- **The test plan**: simulation cases each with a failing mutant, and bench cases by B6's method (PR #630).

Decisions requested, each with the page's recommendation:

| ID | Question | Recommendation |
|---|---|---|
| D1 | Source order | L1: INTERNAL 0, CRF 1, AAF input k at 2 + k, so saved selections keep their meaning |
| D2 | AAF measurement | M1: one meter on the selected input; `KL_crf_rx` untouched |
| D3 | Switching between two followed sources | W2: hold over and re-acquire, no trim reset |
| D4 | A2 at INTERNAL | A2-a: engage the grid aligner at INTERNAL too; reverses the recorded INTERNAL free-run rule |
| D5 | CLOCK_DOMAIN LOCKED and UNLOCKED | C1: unlocked while the followed source is not LOCKED |
| D6 | Shipping configurations | All five, in one regeneration |
| D7 | Phase alignment (IEEE 1722-2016 10.8, 4.3.5) | A new issue: a pre-existing gap of the CRF path |

## Authoritative references

- Milan v1.2: 5.3.3.6, 5.3.8.7, 5.3.11.1, 5.3.11.2 (Tables 5.7, 5.15), 5.4.2.15, 5.4.2.16, Table 5.4, Table 5.6, 6.2, 7.1, 7.2.2, 7.2.3, 7.3.2, 7.4, 7.6.2.
- IEEE 1722.1-2021: 6.2.2.8, 7.2.6 (Table 7-8), 7.2.9, 7.2.9.2 (Table 7-17), 7.2.32 (Table 7-61), 7.4.23, 7.4.23.1, 7.4.24, Table 7-141.
- IEEE 1722-2016: 4.3.2, 4.3.5, 4.4.4.3, 4.4.4.7, 10.4.3, 10.8 (Equation 15), PICS Table F.7 (AAF-5, AAF-6).
- #629 (the decision in its body, and the lane M1 assignment), #389 (option (a), reversed for AAF), #74 (A2 and its ledger), PR #630 (bench lane B6, the baseline).
- `docs/design/TIME_SYNC.md`, `docs/reference/FR_NFR.md` (FR-CLK-03, FR-CLK-04), `docs/reference/MILAN_COMPLIANCE_MATRIX.md`, `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` (L6), `docs/design/AREA_BUDGET.md`; the protocol processor's `docs/architecture/07_memory_maps.md` (L6) and `docs/00_MILAN_COMPLIANCE_REVIEW.md` (REQ-AEM-013, REQ-MDL-005).

## How to get into the same state

```sh
git fetch origin
git checkout 629-media-clock-follow
git submodule update --init protocol-processor
python3 -m venv .md-venv
.md-venv/bin/python -m pip install --require-hashes -r tools/markdown/requirements.txt
```

## How to validate

```sh
.md-venv/bin/python scripts/docs_check.py
.md-venv/bin/python scripts/check_doc_style.py
.md-venv/bin/python scripts/gen_toc.py --check
.md-venv/bin/python scripts/gen_toc.py --verify-anchors
.md-venv/bin/python scripts/check_em_dash.py --base d4dd7426
.md-venv/bin/python scripts/check_doc_paths.py
python3 scripts/check_feature_status.py --self-test
git diff --check d4dd7426 HEAD
# the one measurement the page quotes (Yosys estimate, out of context):
OOC_SHAPE="$PWD/configs/generated/endstation_ax7101_1x1_tdm8" syn/yosys/ooc.sh KL_crf_rx
```

Expected result / pass criteria: every command exits 0. `docs_check` reports 0 findings; `check_em_dash` reports 0 findings over 578 added lines in 2 pages; the TOC gate and the anchor check pass. The area run prints `KL_crf_rx` at 433 LUT, 544 FF, 1 RAMB18 and 147 CARRY4, the figures in the page's "Area estimate".

Results at `78d4fef2`, each run unpiped with its output to a file: all rc 0. `docs_check`: 0 findings across 184 Markdown files and 955 scrubbed text files. `check_doc_style`: OK. `gen_toc --check`: OK. `gen_toc --verify-anchors`: 292 links reproduced. `check_em_dash --base d4dd7426`: 0 findings over 578 added lines. `check_doc_paths`: OK, 871 cited paths resolve. `check_feature_status --self-test`: rc 0. `git diff --check` and `git diff --check d4dd7426 HEAD`: clean.

## Known limitations / out of scope

- Design only: no simulation was run, and nothing in the page is implemented. The area figures are estimates scaled from one out-of-context run.
- The baseline findings page (B6) is cited through PR #630, which was open when this page was written.
- Out of scope, by the assignment: every RTL, builder, generator, configuration and processor change, and the requirement amendments themselves (FR-CLK-03, FR-CLK-04 and the #389 record). The page lists each of them as a change for the implementation lanes.
- IEEE 1722-2016 10.8 and 4.3.5 phase alignment is recorded as a pre-existing gap and proposed as a new issue (D7), not designed here.
- The RX monitor's unused external-clock media-lock rule stays #74's ledger item 3.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (this PR covers #629's design step only; it relates to #629 and does not close it)
- [ ] New or changed behavior has self-checking tests (no behavior changes; the test plan is in the page)
- [x] Required local verification bar passes (the Markdown gates above, rc 0)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains (none is made; the proposed ones are listed in the page)
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
