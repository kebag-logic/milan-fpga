[R307] POSITIVE - exact head 9d66cfe0dc87ffe4a5f45691d5c86b041b050b38

# R307-3 external review: issue #508 / PR #560 (delta, round 4)

- Head `9d66cfe0dc87ffe4a5f45691d5c86b041b050b38`, tree `5424e3e661916f1fd38c8a198400dfc0ec6baded`. Both were verified in the review clone at the start and again after the probes (`receipts/clone_integrity_after.txt`).
- Prior reviewed head `224ec0e9a9fa129924bf8f0433cf70b4140f7bd2` (R307-2). Source base `573f0052a0e4412e81f0845438fcec2086ce5d55`. Processor gitlink `990f96526bb89356c963a260ebbdcf2a77e6623a`, unchanged.
- Role: external independent reviewer, cleared context. This is a delta round on the amended round-4 assignment (issue #508 comment 5826348330). All five lenses were applied at this head.
- **The verdict is POSITIVE. No BLOCKER, MAJOR or MINOR finding is open at this head.**
  - R307-2 F1 (MAJOR; Docs, Tests) is **RESOLVED**. The README links are now commit-pinned GitHub blob URLs at `990f9652` and keep their fragments. `docs_check.py` reports 0 findings in a `git archive` of the head that has no submodule content. The prior head fails the same run, which serves as the control.
  - R307-2 F2 (MINOR; Docs) is **RESOLVED**. All four locations now state eight arms, eight elaborations and nine runs. Both the driver source and an executed campaign at this head confirm those numbers.
  - The delta is exactly 5 files and 6 lines (6 insertions, 6 deletions). No HDL, testbench logic or gitlink changed.

## Reconstruction

Sources read, in this order:

1. `AGENTS.md` and the docs workflow contexts (`.github/workflows/docs.yml`: `docs-check`, `docs-check-no-git`, the em-dash, TOC and test-evidence steps).
2. Issue #508 comments:
   - 5826348330: the amended round-4 scope, which replaces 5826321018;
   - 5826412772: REVIEW READY from the executor;
   - PR #560 comment 5826440650: the review start.

   The PR is open, not draft, based on `dev`, with head `9d66cfe0` (read-only `gh pr view`).
3. The interface authority for F1: the processor's `docs/architecture/06_aecp_engine.md` and `05_acmp_engine.md` at the pinned `990f9652`.
4. `git diff 224ec0e9a..9d66cfe0` (one commit, one-line message, no body or trailers). The lane-wide diff `573f0052..9d66cfe0` differs from the round-3 head only in these five files.
5. Public evidence: `9bf2af2d/review-evidence/508-r1/author-r4` (path listing and the PR body statement "all eight mutants fail their named checks, with 9/9 campaign controls passing"), plus the hosted check runs at the exact head.

My own round-3 report (R307-2, PR comment 5826345263) supplied the prior findings F1, F2, S1 and S2. Their dispositions are below. I read no private author material and no lane scratchpad. I read the other reviewer's prior public R306-2 findings (PR comment 5826344643) only after I had written this verdict and ledger. I did not read any concurrent R306-3 report.

## Delta verified against the amended assignment

| Assignment item (5826348330) | Result | Evidence |
|---|---|---|
| 1. `tb/verilator/milan_dp/README.md:488`: commit-pinned GitHub blob URLs at `990f9652` (the repository convention, as at `:728`); keep `#fig-06-lineage` and `#fig-05-settled`; name F06.13 and F05.5 | **met** | See the F1 checks below this table. |
| 2. Campaign size as eight arms, eight elaborations and nine runs in `CHANGELOG.md:57`, `Makefile:451-452`, `measure_test_evidence.py:619-620` and `TESTING.md:267` | **met** | See the F2 checks below this table. |
| 3. Change nothing else, and the gates listed in the assignment | **met** | See the gate list below this table. |

**F1 checks (item 1):**
- `README.md:488` now reads `[F06.13, field lineage](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/990f96526bb89356c963a260ebbdcf2a77e6623a/docs/architecture/06_aecp_engine.md#fig-06-lineage)` and `[F05.5, settlement detail](.../blob/990f9652.../docs/architecture/05_acmp_engine.md#fig-05-settled)`.
- The repository is the one named for the `protocol-processor` submodule in `.gitmodules`.
- The pin equals the gitlink.
- At the pin, the targets carry `<a id="fig-06-lineage"></a>**F06.13 ...` (`06_aecp_engine.md:295`) and `<a id="fig-05-settled"></a>**F05.5 ...` (`05_acmp_engine.md:316`).
- The upstream contents API at that ref returns blob `77720a15...` and `56afbfdd...`, identical to the local pin. Both blob URLs return HTTP 200 (`receipts/link_targets_remote.txt`).
- `:728` uses the same URL form at another pin, so the convention matches.

**F2 checks (item 2):**
- All four locations now state eight arms, eight elaborations and nine runs. `TESTING.md:267` reads "the eight field and notification mutants": seven field mutants plus the G8 push-count mutant.
- `gsi_mutants.py` `MUTATIONS` has 8 entries. The clean executable is reused from the `notify` prerequisite, so the campaign adds 8 elaborations and 9 runs of the leg (the clean re-run plus 8).
- That is the same convention as `crflic-mutants`: 3 arms, and its comment says "three more elaborations and four runs" (`receipts/campaign_counts.txt`, `scripts/campaign_counts.py`).
- `grep -n -i seven` over the four files returns nothing. The only other tracked "seven" near this topic is `docs/MILAN_V12_ROADMAP.md:200` ("seven fields" of the dynamic store), which does not describe the campaign.
- Executed at this head: `make notify gsi-mutants` gives a clean leg of 380/0, all 8 mutants caught on their named checks, and "9 checks: 9 PASS, 0 FAIL" (`receipts/notify_gsi_mutants.log`).

**Item 3 gates and scope:**
- `git diff --numstat 224ec0e9..9d66cfe0` lists exactly `CHANGELOG.md`, `TESTING.md`, `measure_test_evidence.py`, the milan_dp `Makefile` (two comment lines) and `README.md`: 6/6 lines. The four gitlinks are identical at both heads. `git diff --check` returns rc 0 (`receipts/delta_scope_and_extra_gates.txt`).
- Gates, all rc 0:
  - `docs_check.py` in the clone: 0 findings;
  - `docs_check.py` in a `git archive` tree with no git metadata and no submodule content: 0 findings;
  - `gen_toc.py --verify-anchors`: 168 links reproduced;
  - `gen_toc.py --check` and `--selftest`: 1501/1501;
  - `check_doc_paths`: 842 paths;
  - `check_py_idiom`;
  - `check_em_dash --base` c266432d, 224ec0e9 and 573f0052: 0 findings;
  - `check_doc_style`;
  - `measure_test_evidence --check` and `--selftest`: 101/101.

## Findings

No BLOCKER, MAJOR or MINOR finding at this head.

### S1 - SUGGESTION - lenses: Tests (retained from R307-2)

**Location:** `tb/verilator/milan_dp/sim_nxn.cpp:2182-2199`.

G8 labels its two pushes by order, not by cause. The exact-count checks catch both single-cause removals, so this is optional. It is unchanged at this head.

### S2 - SUGGESTION - lenses: Docs (retained from R307-2)

**Location:** `tb/verilator/milan_dp/README.md:849`.

The `obj_notify` row still shows the dated round-1 measurement **345 / 0**, while the clean leg now reports 380/0 (`:499`). It is labelled as a dated measurement, so it is optional. It is unchanged at this head.

## Prior public findings: disposition at this head

| Finding | Disposition | Evidence |
|---|---|---|
| R307-2 F1 (MAJOR; Docs, Tests), README:488 links into the submodule | **RESOLVED** | Archive `docs_check` returns 0 findings, rc 0 (`receipts/docs_check_archive_9d66cfe0....txt`). The control archive of `224ec0e9` still reports the two broken links, rc 1 (`receipts/docs_check_archive_224ec0e9....txt`), so the gate can fail on exactly this defect. Hosted `docs-check` and `docs-check-no-git` are both **success** at this head (both were failure at `224ec0e9`), per the 04:10 UTC snapshot. |
| R307-2 F2 (MINOR; Docs), seven-arm campaign wording | **RESOLVED** | The four locations are corrected. The counts are derived from the drivers and confirmed by the executed campaign (9/9). |
| R307-2 S1, S2 (SUGGESTION) | **RETAINED** (optional) | Not touched this round. |
| R306-2 F1 (BLOCKER; Docs, Tests): the same defect as R307-2 F1 | **RESOLVED** | The evidence is the same as for R307-2 F1. The R306-2 verification is met: `git archive` `docs_check` returns 0, and both hosted contexts are green at this head. |
| R306-2 F2 (MINOR; Docs): the same defect as R307-2 F2 | **RESOLVED** | Its verification `grep -n "seven" CHANGELOG.md tb/verilator/milan_dp/Makefile scripts/measure_test_evidence.py` finds nothing. `measure_test_evidence --check` and `docs_check` are green. |
| R306-2 S1 (Robustness, Tests: no `seen == 2` assertion after the per-push loop) and S2 (Tests: parent coverage of the processor bridge gate) | **RETAINED** (SUGGESTION, optional) | `sim_nxn.cpp` and the processor pin are not in the delta. |
| R306-2 out-of-scope observation (pre-existing stale processor citations outside this PR) | **not a finding of this PR** | These lines predate the source base and are not in the delta. They are new work for a separate issue. |
| Earlier dispositions recorded in R307-2 (R307-1 F1/F2, R306-1 F1-F3 resolved; R307-1 S2 = R306-1 S1, R306-1 S2/S3 retained as SUGGESTION) | **unchanged** | None of the cited artifacts is in the delta. |

## Per-lens coverage lines

```text
[R307] PASS Conformance - issue #508 comment 5826348330 items 1-3 against README.md:488, CHANGELOG.md:57, TESTING.md:267, measure_test_evidence.py:620, Makefile:451-452 at 9d66cfe0; processor 06_aecp_engine.md:295 / 05_acmp_engine.md:316 at 990f9652 - pinned URL form, pin = gitlink, fragments and figure labels kept, counts 8/8/9 equal the driver; acceptance 1-6 behaviour untouched (5 files, 6 lines, no HDL/TB logic), R307-2 conformance ledger at 224ec0e9 stands
[R307] PASS RTL - receipts/delta_scope_and_extra_gates.txt (numstat 224ec0e9..9d66cfe0, gitlinks at both heads) - no *.sv/*.v/testbench source in the delta; Makefile change is two comment lines; four gitlinks identical; R307-2 RTL coverage at 224ec0e9 is an ancestor untouched in RTL scope
[R307] PASS Robustness - receipts/notify_gsi_mutants.log at 9d66cfe0 - G8 exact bounds, sink isolation and the delayed-duplicate arm still hold (380/0 clean, duplicate caught with 2 of 396); no input-handling, reset, timeout or backpressure artifact is in the delta
[R307] PASS Tests - receipts/docs_check_archive_{9d66cfe0,224ec0e9}.txt, notify_gsi_mutants.log, measure_test_evidence_{check,selftest}.txt, gen_toc_*.txt at 9d66cfe0 - the required docs regression is green without the submodule and demonstrably red on the prior head; campaign 9/9 with every arm on its named check; evidence ratchet check PASS, selftest 101/101; disposition string for gsi_mutants.py matches its 8 arms
[R307] PASS Docs - README.md:488, CHANGELOG.md:57, docs/testing/TESTING.md:267, scripts/measure_test_evidence.py:620, tb/verilator/milan_dp/Makefile:451-452 at 9d66cfe0 - links resolve on the hosted web view (HTTP 200, blob ids equal the pin), anchors exist, counts agree with the driver and with README:496-517, em-dash/doc-style/doc-paths/TOC gates rc 0; only S2 (optional) remains
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment 5826348330 items 1-3 against the 5-file delta; processor F06.13/F05.5 anchors at `990f9652`; acceptance 1-6 scope untouched by the delta, so the R307-2 coverage carries | R307-3 (delta), with R307-2 for untouched scope | `9d66cfe0dc87ffe4a5f45691d5c86b041b050b38` (R307-2 at ancestor `224ec0e9a9fa129924bf8f0433cf70b4140f7bd2`, untouched in scope since) |
| RTL | CLEAN | numstat and gitlinks at both heads (`receipts/delta_scope_and_extra_gates.txt`): no HDL or testbench logic in the delta | R307-3 (delta), with R307-2 for the RTL itself | `9d66cfe0dc87ffe4a5f45691d5c86b041b050b38` (R307-2 at ancestor `224ec0e9a9fa129924bf8f0433cf70b4140f7bd2`, untouched in scope since) |
| Robustness | CLEAN | Executed `notify` + `gsi-mutants` at head (G8 bounds, duplicate arm, sink isolation); delta has no robustness-relevant artifact | R307-3 | `9d66cfe0dc87ffe4a5f45691d5c86b041b050b38` |
| Tests | CLEAN | Archive `docs_check` at head (0) and prior head (control, 2); `notify` 380/0; `gsi-mutants` 9/9; `measure_test_evidence --check/--selftest`; `gen_toc --verify-anchors/--check/--selftest`; `check_em_dash`, `check_doc_paths`, `check_py_idiom`, `check_doc_style` | R307-3 | `9d66cfe0dc87ffe4a5f45691d5c86b041b050b38` |
| Docs | CLEAN (S2 optional) | `README.md:488` (pinned links, upstream blob ids, anchors), `CHANGELOG.md:57`, `TESTING.md:267`, `measure_test_evidence.py:620`, `Makefile:451-452`, README mutant table `:496-517`, `:728` convention | R307-3 | `9d66cfe0dc87ffe4a5f45691d5c86b041b050b38` |

## Commands run (foreground, at most 8 jobs)

- `git archive 9d66cfe0 | tar -x`, then `python3 scripts/docs_check.py` in the extracted tree. The tree has no `.git` and an empty `protocol-processor/`. Result: 0 findings, rc 0.
- The same run on `224ec0e9` as a control: 2 findings, rc 1.
- `python3 scripts/docs_check.py` in the clone: 0 findings, rc 0.
- The pinned Markdown renderer was installed with `--require-hashes` from `tools/markdown/requirements.txt` into a disposable virtual environment under the packet's scratch directory. With it, `gen_toc.py --verify-anchors`, `--check` and `--selftest`, `check_em_dash.py --base` (three bases), `check_doc_style.py`, `check_doc_paths.py` and `check_py_idiom.py` all returned rc 0.
- `measure_test_evidence.py --check` and `--selftest`: both rc 0.
- Simulator identity: the scoped wrapper (sha256 `905795b9...`) reports `Verilator 5.050 2026-07-01 rev v5.050`. `VERILATOR=<tool-bin>/verilator VERILATOR_JOBS=8 make -C tb/verilator/milan_dp notify gsi-mutants` returned rc 0 in 274 s.
- `scripts/campaign_counts.py <clone>`: gsi 8/8/9 and crflic 3/3/4, RESULT OK.
- Read-only `gh api` calls: the upstream contents at `990f9652`, the exact-head check runs, and the issue and PR comments.
- `scripts/reproduce.sh` re-creates every receipt.

## Real limits

- **Not run by this reviewer:** the full milan_dp default sweep, the parent, processor, gPTP, Yosys and builder banks, and Docker/act or host `act_ci`. Those rely on the manager's source banks at this head and on the R307-2 ledger, whose scopes the delta does not touch. The manager's native and static bank receipts at `9d66cfe0` were not found as a separate directory in the named evidence tree; I relied on the assignment statement for them.
- **Hosted snapshot at 2026-09-25T04:10Z** (`receipts/hosted_check_runs.tsv`):
  - Completed with success: `docs-check`, `docs-check-no-git`, `rtl-fast`, `elaborate`, `bdd-conformance`, `changes`, `full-ci-gate`, `verilator-lint`, `wire-accountability`, `yosys-elaboration`, Yosys shards 0-3/4 and Verilator shard 3/5.
  - Still in progress: Verilator shards 0, 1, 2 and 4/5.
  - "Physical gPTP (nightly and manual)": skipped. That context was not executed.
  - `verilator-suites` and `yosys-portability` were not yet reported as contexts.
- **Clause text.** Milan clause text was not re-read in this round. No normative behaviour changed.
- **Hardware.** Physical calibration was NOT RUN. The field skips are not hardware proof.
- **Clone state.** The build products I created were removed: `obj_notify/`, the two run-directory ROM images, and the `__pycache__` directories, including one in the processor submodule. The clone was then verified:
  - HEAD and index tree `5424e3e6`;
  - 885 tracked blobs matching in bytes and mode;
  - no status entries, including ignored ones;
  - four gitlinks at their pins;
  - the three initialised submodules clean.
- **Receipt hygiene.** Host path prefixes were replaced by `<clone>`, `<packet>`, `<tool-bin>`, `<tool-root>`, `<home>` and `<tmp>`. Only path strings changed.

## Pending manager duties

- Accept the hosted runs at the exact head: Verilator shards 0, 1, 2 and 4/5 (still running at the snapshot), and the exact-head `verilator-suites` and `yosys-portability` contexts. Own the act replica.
- Obtain the second independent positive at this head.
- Build and validate the final current-dev candidate at the merge turn (source base `573f0052`, live dev `c533b481`). Then run post-merge containment.
- Physical calibration remains NOT RUN.

R307-3 FINISHED
