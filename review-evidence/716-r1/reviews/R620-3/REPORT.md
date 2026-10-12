[R620] POSITIVE - exact head 194b7c4114c609fa3dc3b10f82292a45e7781b0e

# R620-3 composition review: issue #716 / PR #724 merge-train candidate

Reviewer: [R620], internal lane reviewer, cleared context. Round R620-3.
Head under review: `194b7c4114c609fa3dc3b10f82292a45e7781b0e`, tree
`093c496f7ff05a1d8f8d6723ed0705f50df913e7`. First parent dev
`c6bd08c6f52632c6d33d834ce842ac3cf63f29cc` (carries PR #722 / M5 and PR #707 / #621),
second parent PR #724 source head `941e15593ef3dbf561bd8ed75aaf680f5d146a41`
(merge base `09c7231eca343607c97c0d66abebb2553688712c`).
Scope: composition acceptance only. The source head carries its own reviews; this
round judges whether the composed tree introduces any defect beyond those sources.

Overall verdict: POSITIVE. The composition introduces no defect: no BLOCKER,
MAJOR or MINOR finding, and no new finding of any severity. Three prior RESIDUE
items and one SUGGESTION from the source rounds are retained unchanged at this
head (section "Prior reviews"). All five lenses CLEAN at the exact head (ledger
below).

## Reconstruction

Read in order: `AGENTS.md`, `CONTRIBUTING.md` (by reference), `docs/README.md` (by
the authority map), issue #716 body (acceptance items 1 to 3) and its public
comments: the manager's assignment (scope, STOP conditions, 70 % hosted / 60 %
prediction bounds, census and shard-coverage requirements), the round 2 merge-dev
assignment, the executor's TAKEN and both REVIEW READY posts; the manager's public
review-start comment for this round; then the diff `c6bd08c6..194b7c41` and
history; then the published author round 2 receipts (census only) at evidence
commit `879bafcc`. No private author material, lane scratch, or other review was
read before this verdict and ledger were written.

## Composition facts (receipt `receipts/composition_check.log`, rc 0)

1. The candidate is the mechanical clean merge: `git merge-tree --write-tree
   c6bd08c6 941e1559` yields `093c496f`, the candidate tree exactly. No hand
   resolution exists to review.
2. Since merge base `09c7231e`, dev changed 49 paths and the PR 5. The only path
   both sides changed is `docs/testing/CI_WORKFLOWS.md`; the manager's statement
   is confirmed.
3. The other four PR files are byte-identical to the PR head in the candidate:
   `.github/workflows/rtl-fast.yml` `902b92cd`, `scripts/ci_events.py` `ff8d7232`,
   `sw/firmware/ctrl/test/test_ctrl_firmware.py` `3f0bea6e`,
   `sw/firmware/ctrl/test/test_ctrl_firmware_shards.py` `07ec7a3e`. Dev changed
   neither `rtl-fast.yml` nor `ci_events.py` since `09c7231e` (dev blobs equal the
   merge-base blobs `0e53b3a6`, `52df0a83`).
4. All 48 dev-only paths, including the `gptp-processor` gitlink `7dda9c3b`, are
   identical (mode and object) to dev.
5. `CI_WORKFLOWS.md`: the dev hunk (20 changed lines, the #621 `milan_dp_gm_steps`
   paragraph in the Verilator budget history, candidate lines 343 to 365) and the
   PR hunks (60 changed lines: the rtl-fast list item at 44 to 46, the four-job
   paragraph and budget table at 64 to 102, the documentation-only skip sentence
   at 104 to 106, the local shard commands near 2369) are carried byte-identically.
   The hunks are disjoint by roughly 240 lines.
6. Semantic interaction search: every one of the 49 dev-side paths was searched
   for, by exact path, in `sw/firmware`, `rtl-fast.yml`, `ci_events.py`,
   `ci_scope.py` and `ci_rv32_sdk.py`. Hits are comments (`milan_baremetal.c`,
   `nvm_host.c`), unrelated `ci_scope.py` fixtures, pinned command lines for
   `suite_shards.py --selftest` and `check_nvm_capture.py` (both re-run green
   here), the `CI_WORKFLOWS.md` policy pin itself, and `gptp-processor` submodule
   initialisation. No firmware driver or suite reads any dev-changed file: the
   firmware jobs' inputs (`tb/verilator/mbx`, `tb/common`,
   `tb/verilator/nvm_backend`, `hdl/ieee1722/maap/KL_maap.sv`,
   `protocol-processor`, `third_party/lwSRP`) are all untouched by the dev delta;
   `milan_csr.sv` (PR #722) appears in `ctrl_arms.py:242` only as a comment, and
   `gptp-processor` is fetched but read by no firmware file. So the shard
   discovery set, census and timing basis of the source head carry over unchanged.

## Gates run on the candidate (receipts `receipts/gates/*.log|.rc`, all rc 0)

Script `gates.sh`, 30 gates concurrently, 23 s wall:

| Gate | Result |
|---|---|
| `docs_check.py` / `--selftest` | 0 findings over 204 md + 1272 text files; 23 + 4 arms PASS |
| `gen_toc.py --check` / `--verify-anchors` / `--selftest` | OK 144 pages; 480 cross-page fragments reproduced (incl. `sw/firmware/gtest/README.md:399` to `CI_WORKFLOWS.md#fast-feedback`); 1501/1501 arms |
| `check_em_dash.py --base c6bd08c6` (dev parent) | 0 findings over 58 added lines in 1 page, 339/339 arms |
| `check_em_dash.py --base 09c7231e` (PR merge base) | 0 findings over 404 added lines in 19 pages |
| `check_em_dash.py --selftest` | 339 arms PASS |
| `check_doc_style.py` / `--selftest`, `check_doc_paths.py`, `DOC_MAP.gen.py --check`, `check_solution_docs.py`, `check_submodule_docs.py` (5 exact gitlinks), `check_gptp_docs.py` | OK |
| `ci_events.py --check` | OK, 2016 contract items across 4 workflows and `CI_WORKFLOWS.md` |
| `ci_events.py --selftest` | PASS, 2016 items, 2828 arms |
| `ci_events.py --firmware-census` | rc 0; byte-identical (sha256 `0a1880a0...`) to the census regenerated at PR head `941e1559` and to the published `ROUND2-GENERATED-CENSUS.json` |
| `ci_scope.py --selftest`, `suite_shards.py --selftest` | PASS |
| `test_ctrl_firmware_shards.py` | PASS (missing/duplicate dispatch, future suite, nine invalid combinations) |
| `check_py_idiom.py` / `--selftest`, `check_hygiene.py --check`, `measure_test_evidence.py --check`, `measure_naming.py --check`, `measure_fail_fast.py --check`, `check_todo_ownership.py`, `check_nvm_capture.py` | PASS |
| `git diff --check c6bd08c6 HEAD` | clean |

Cross-tree comparison (`receipts/compare/`): `ci_events.py --check` gives 2016
items at both the PR head and the candidate (1821 at dev `c6bd08c6`, which lacks
this PR's pins); `--firmware-census` output is byte-identical between PR head and
candidate (at dev the option does not exist, rc 2, as expected).

## Disposable probes on a copy of the candidate (`probes.sh`, `receipts/probes/`)

Each probe edits a scratch copy and runs `ci_events.py --check`:

| Probe | Edit | Expected | Got |
|---|---|---|---|
| P0 | none | pass | rc 0 |
| P1 | delete the `firmware-aecp-mutants` budget row from the composed `CI_WORKFLOWS.md` | fail | rc 1, "firmware budget row must state ..." |
| P2 | `firmware-srp-mutants` row 45 min to 60 min | fail | rc 1, same pin |
| P3 | delete the dev-side #621 paragraph | pass (not pinned by this gate) | rc 0 |
| P4 | drop `firmware-srp-mutants` from the `rtl-fast` aggregate `needs` | fail | rc 1, three aggregate pins |

P1 and P2 show that the PR's acceptance item 3 pins read the composed page; P3
shows the dev paragraph sits outside those pins, so its presence can neither mask
nor trip them. No probe touched the clone; scratch copies were deleted.

## Combined-text judgement for `docs/testing/CI_WORKFLOWS.md`

- PR side (candidate lines 44 to 106, 2369 to 2382): four firmware jobs, each
  `needs: changes`, 45-minute timeouts, the aggregate requiring all of them plus
  `publication-census`, SDK-only cache, `--shard INDEX/4` phases, unsplit
  coverage, census and pins. Each statement checked against the candidate
  `rtl-fast.yml` lines 317 to 505 (byte-identical to the PR head): true.
- Dev side (candidate lines 343 to 365): `milan_dp_gm_steps` moved to Verilator
  worker 3/5, 1800 s budget, `suite_shards.py` landmark. Checked against
  `scripts/suite_shards.py` (landmark `"milan_dp_gm_steps": 3`, selftest PASS)
  and the dev-side `TESTING.md` and `tb/verilator/README.md` rows: true, and it
  concerns the `verilator-suites` workflow, which this PR does not touch.
- Neither side states a job count, inventory or ordering that the other side
  changes; the only enumerations of rtl-fast jobs are the PR's own and match the
  candidate workflow. No statement became false in combination. TOC and anchors
  regenerate unchanged.

## Findings

No new finding of any severity from this round's composition pass. Prior
residues and one suggestion are retained unchanged at this head (see "Prior
reviews"); none is BLOCKER, MAJOR or MINOR, and none was caused or altered by
the composition.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #716 acceptance 1 to 3 and assignment bounds; candidate `rtl-fast.yml:317-505` (four 45-minute jobs, aggregate needs) and `CI_WORKFLOWS.md:64-102` budget table; `ci_events.py --check` 2016 items rc 0; probes P1, P2, P4. Composition touches acceptance item 3's documented budget page; it holds. Items 1 and 2 (measurement, ten hosted runs) are source and hosted evidence, unchanged by composition (firmware inputs disjoint from the dev delta, fact 6). | R620-3 | `194b7c4114c609fa3dc3b10f82292a45e7781b0e` |
| RTL | CLEAN | No HDL in the PR; composition intersects no HDL the firmware jobs read (fact 6: `milan_csr.sv` comment-only in `ctrl_arms.py:242`; `KL_maap.sv`, `protocol-processor` untouched). CI architecture artifact `rtl-fast.yml` blob `902b92cd` identical to source head; job graph and timeouts verified by `ci_events.py --check` and P4. Composition does not touch this lens's scope; source coverage carries over from R620-2 (6117675328) and R621-2 (6117553751), both POSITIVE at `941e1559`. | R620-3 | `194b7c4114c609fa3dc3b10f82292a45e7781b0e` |
| Robustness | CLEAN | Shard discovery on the composed suite set: `test_ctrl_firmware_shards.py` PASS (missing, duplicate, future suite, nine invalid combinations); census byte-identical to source head; dev delta adds no firmware suite (fact 6). Pin robustness on the composed page: probes P1 to P4. Composition changes no failure path. | R620-3 | `194b7c4114c609fa3dc3b10f82292a45e7781b0e` |
| Tests | CLEAN | `test_ctrl_firmware.py` `3f0bea6e` and `test_ctrl_firmware_shards.py` `07ec7a3e` identical to source head; `ci_events.py --selftest` 2828 arms; shard self-test; probes show the item 3 pins fail when the composed page is mutated. Firmware suites themselves were not re-executed here (inputs unchanged by composition; see limits). Retained SUGGESTION R620-3-S1 does not affect coverage. | R620-3 | `194b7c4114c609fa3dc3b10f82292a45e7781b0e` |
| Docs | CLEAN | `docs/testing/CI_WORKFLOWS.md` lines 44-106, 343-365, 2369-2382 read against `rtl-fast.yml` and `suite_shards.py`; `docs_check.py`, `gen_toc.py --check/--verify-anchors/--selftest`, `check_em_dash.py --base c6bd08c6` and `--base 09c7231e`, `check_doc_style.py`, `check_doc_paths.py`, `DOC_MAP.gen.py --check`, `check_submodule_docs.py`, all rc 0. This is the one lens the composition touches directly. Retained wording residues R620-3-RES1 to RES3 are carried, not caused by composition. | R620-3 | `194b7c4114c609fa3dc3b10f82292a45e7781b0e` |

## Real limits

- The candidate commit `194b7c41` is not on the hosted service (the check-runs
  query returns "No commit found"); there is no exact-head hosted evidence.
  Hosted evidence was inspected only at source head `941e1559`: all four
  firmware jobs executed and succeeded (about 705, 916, 250 and 486 s from
  check-run timestamps, against 1890 s ceilings), `rtl-fast` success;
  `Physical gPTP` is a skipped context, not an execution. The manager's
  ten-run table at `941e1559` (PR comment 6117443205, run 38180290290 attempts
  1 to 10) reports the slowest job at 916 s, 33.9 % of 2700 s; the attempt
  visible in the check-runs matches its attempt 10. That table is for the
  source head, not for this candidate.
- No firmware suite, coverage ratchet, Verilator, Yosys or builder bank was run
  on the candidate. That their results carry over from the source head rests on
  the input disjointness of fact 6, not on an execution.
- Gates ran under local CPython 3.14.7 with the Markdown renderer versions
  that `tools/markdown/requirements.txt` pins; the hosted runner uses CPython 3.12.
- `act_ci.py` and its self-test were not run (outside this round's authority).
- Physical calibration NOT RUN; skipped field contexts are not hardware proof.

## Pending manager duties

- Build and validate the current-dev merge candidate at the merge turn (builder
  and native banks) and publish those receipts; this round claims no manager bank.
- Hosted and act acceptance of the exact merged head, including the ten
  consecutive hosted firmware runs that acceptance item 2 requires, and their table.
- Carry R620-3-RES1 and R620-3-RES2 (the R620-1 residues) to #495 at merge, per
  the round 2 assignment, and R620-3-RES3 to the residue checklist or a PR-body
  edit. Line numbers in RES1 are at this candidate head.
- Merge only with maintainer authorization and the full completion bar.

## Clone integrity

After all runs: HEAD `194b7c41`, HEAD tree and index tree `093c496f`, no tracked
modification, `git diff-index` rc 0; gitlinks `external efeb541a`,
`gptp-processor 7dda9c3b`, `protocol-processor 2ad2f845`, `third_party/lwSRP
08ee86e8`, `third_party/verilog-axis 48ff7a7e` match the tree. Bytecode caches
the gates created under ignored paths were removed; the pre-existing ignored
`scripts/__pycache__/` remains (`receipts/clone_integrity.log`).

## Prior reviews

Read only after the verdict and ledger above were written. PR #724 carries
R620-1 (6113853338) and R621-1 (6113677958), both POSITIVE at `f41e4f2d`, and
the source reviews at `941e1559`: R621-2 (6117553751) and R620-2 (6117675328),
both POSITIVE. These two are the source reviews this ledger relies on where the
composition does not touch a lens's scope. Structured reviews: none. Every prior
finding is re-checked at this head:

| Prior finding | Severity, lens | Disposition at `194b7c41` |
|---|---|---|
| R620-1-RES1 / R620-2-RES1, stale CI prose in PR files | RESIDUE, Docs | Retained as R620-3-RES1 below. All four locations are present unchanged; one moved by the dev insertion. |
| R620-1-RES2 / R620-2-RES2, single-job wording in two READMEs | RESIDUE, Docs | Retained as R620-3-RES2 below. Composition touched neither README. |
| R620-2-RES3 and R621-2-RES1, PR body status lines | RESIDUE, Docs | Retained as R620-3-RES3 below. The live PR body (head `941e1559`) still says "the merge head remains unpushed" and "Item 2 passed at f41e4f2d; the manager rechecks hosted runs at this new head", although its own Linked Issue line cites the `941e1559` table. |
| R620-1-S1 / R620-2-S1, shard inventory observes invocations, not verdict participation | SUGGESTION, Tests | Retained as R620-3-S1. `test_ctrl_firmware_shards.py` blob `07ec7a3e` is identical to the source head. |
| R621-1, R621-2 other content | none | Nothing further to resolve. |

### R620-3-RES1 (retains R620-2-RES1): stale CI prose in files this PR touches

- Severity: RESIDUE. Lenses: Docs.
- Locations at this head, with exact fixes:
  - `.github/workflows/rtl-fast.yml:312-313`, "plus the control mutation
    campaign". Fix: replace it with "while the three mutation jobs below run
    the campaigns (#716)".
  - `docs/testing/CI_WORKFLOWS.md:2372-2374` (was 2354 at the source head; moved
    by the dev #621 insertion), "run locally as `firmware-unit` runs them ...
    the required RV32 control build and its `--self-test` mutation campaign".
    Fix: replace "as `firmware-unit` runs them" with "as the four firmware jobs
    run them together".
  - `docs/testing/CI_WORKFLOWS.md:91`, "Issue #716 records measurements and the
    hosted acceptance table." Fix: "Issue #716 records measurements; PR #724
    records the hosted acceptance table."
  - `docs/testing/CI_WORKFLOWS.md:88`, "below 60%". Fix: "at most 60%".
- Authority: the candidate `rtl-fast.yml:317-505` assigns the campaigns to three
  separate jobs; issue #716's assignment states the prediction bound as "at
  most 60 %"; the hosted tables are PR #724 comments.
- Impact: wording only. No pin, measurement, gate or verdict changes; P1 and P2
  show the pinned budget rows are separate from these sentences.
- Required outcome: the manager carries it to #495 at merge, per assignment
  6113977586, or the wording is fixed.
- Verification: re-read the lines; rerun `ci_events.py --check`,
  `docs_check.py`, `check_doc_style.py`.

### R620-3-RES2 (retains R620-2-RES2): single-job CI wording outside the lane's permitted files

- Severity: RESIDUE. Lenses: Docs.
- Locations: `sw/firmware/gtest/README.md:398-411` (names only `firmware-unit`,
  "the ctrl gate", "`scripts/ci_events.py` pins the job's steps", "The control
  gate includes lwSRP, SRP and its mutation campaign");
  `sw/firmware/ctrl/README.md:349` ("The CI firmware step also requires the
  control mutation campaign.").
- Exact fixes: in the harness page name the four firmware jobs, say that
  `firmware-unit` runs the tally cases, the normal ctrl suites (`--shard 0/4`),
  the saved-state gate and coverage while `firmware-control-mutants`,
  `firmware-aecp-mutants` and `firmware-srp-mutants` run the campaigns, and say
  "`scripts/ci_events.py` pins all four firmware jobs"; in the ctrl README write
  "The `firmware-control-mutants` job runs the control mutation campaign (#716)."
- Impact: wording only. Required outcome: carried to #495, or a follow-up
  authorized. Verification: re-read; rerun `docs_check.py`.

### R620-3-RES3 (retains R620-2-RES3 and R621-2-RES1): PR body status lines

- Severity: RESIDUE. Lenses: Docs.
- Location: PR #724 body, "Status" lines 2 to 3 and "Known limitations".
- Exact fixes: Status: "`716-fw-unit-split` -> `dev`; head `941e1559` is
  published. Item 2 passed at `941e1559` (manager comment 6117443205: slowest
  916 s, 33.9 %); the `f41e4f2d` table below is superseded." Known limitations:
  "Re-review at the new head is complete; the merge-train candidate is
  validated by the manager at the merge turn."
- Impact: wording in a PR body only. Required outcome: the body is edited or the
  item is carried on the residue checklist. Verification: re-read the PR body.

### R620-3-S1 (retains R620-2-S1): shard inventory observes invocations

- Severity: SUGGESTION. Lenses: Tests.
- Artifact: `sw/firmware/ctrl/test/test_ctrl_firmware_shards.py:47-99`,
  unchanged. Optional: plant a failing stand-in per phase inside the in-tree
  check, and use explicit raises in place of `assert`. Verification: a planted
  discard of one shard's result fails the in-tree check. It does not affect
  coverage.

These retentions do not change the verdict: RESIDUE and SUGGESTION do not leave
a lens unclean (owner rule 2026-10-02), and none of them is a composition effect.

R620-3 FINISHED
