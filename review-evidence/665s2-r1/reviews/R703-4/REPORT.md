[R703] NEGATIVE - exact head a66148f6b7e59e3f42c939f464fe76e2b05404d7

# [R703] R703-4: internal cleared-context review of PR #792 (issue #665, lane S2, CPU budget), round 4 delta

Head `a66148f6b7e59e3f42c939f464fe76e2b05404d7`, tree `30799d272d92b00999d28bc475d29e7ea797b3c3`, base `dev-soft-core` `e76a755a`.
The delta under review is `f8876638..a66148f6`, one commit. It changes only `tb/verilator/ctrl_service_budget/`: README, `grade.py`, `run.py`, `scenario.py`, `selftest.py` and `selftest_mutants.py` (`receipts/delta_stat.txt`, `receipts/delta_f8876638_a66148f6.diff`).
It answers R703-3 and R704-3. The rows missing T_svc are the lane's result (the D4 measurement STOP), not a finding.

Scope comes from the S2 assignment on #665 (issuecomment-6409745905):

- measured cycles per mailbox access and per response path;
- the worst pass at the composed maximum;
- each backlog row of `MAILBOX_SPLIT.md:753-758`, at 1x1 with one interface and 8x8 with two;
- each figure compared with T_svc and the 3.4.1 ceiling;
- mutants and controls.

The owner's 2026-10-26 decision (issuecomment-6421463860) makes this head the no-cache baseline for S2c and S2b.

## Verdict

**NEGATIVE.** All four R703-3 findings are fixed at their cause, and the round-3 residue inside the lane is applied:

- the bare-metal gate passes;
- arm A's composed maximum is now taken over every backlog window and labelled a lower bound;
- every fan-out range contains every cell;
- G6 and G9 are caught by my round-3 script, run unmodified.

The new code computes the right figures. Every arm A number the README states can be read off the published regrade at this head.

Two MINOR findings remain open. Both are in the composed-maximum rule this round added:

- **R703-4-F1 (MINOR; Robustness, Tests, Docs).** The composed maximum is reported over whatever backlog windows a run happened to include, with no completeness check and no label. Arm B runs three of the four backlog rows, yet its figure is published as "the composed maximum over every backlog window".
- **R703-4-F2 (MINOR; Tests).** The new check does not pin its own rule ("a lower bound while one [window] left its load unreleased"), nor the published lower-bound label. Four plausible defects pass the self-test. One of them, a lower bound only when the longest window is the unreleased one, matches the transition S2c is likely to measure.

## What I verified

| Claim | Result | Evidence |
|---|---|---|
| Self-test at the head | `run.py --self-test`: 84 PASS lines, 57 of 57 mutants caught, rc 0 (4.2 s) | `receipts/selftest_head.log`, `.rc` |
| R703-3's `review_mutants3.py`, unmodified (sha256 `54f6855e…`, the published copy) | 21 run, 18 caught. **G6 and G9 are caught**. G2, G3 and H3 still escape, as recorded at R703-3 | `receipts/review_mutants3_head.log` |
| R703-2's `review_mutants2.py`, unmodified | 25 run, 23 caught (N11 and N12, as before) | `receipts/review_mutants2_head.log` |
| `scenario.py` delta is wording only | The AST with docstrings removed is identical to `f8876638`'s, so every generated group script is unchanged. In `grade.py` the only code change is `BACKLOG_ROWS`, with `COMPOSED_ROWS` keeping the same tuple value | `receipts/ast_delta.txt`, `scripts/ast_delta.py` |
| No new measurement is needed | No firmware, RTL, SoC, `sim_main.cpp` or build file is in the delta. The author's published regrade of round-3 logs at this head reports every group grade byte-identical to `f8876638`'s, with only `composed_maximum` added. I accepted those figures from the receipts and reproduced none by simulation | author-r4 `receipts/head-regrade/compare_base_f8876638_vs_head.txt` (evidence tree `74d66c7e`) |
| Composed maximum, arm A | The published tables give 1x1 = max(740,260; 1,565,803; 1,531,355; 582,677) = **1,565,803**, `backlog-adp`, lower bound. 8x8 = max(1,392,016; 2,208,710; 2,209,308; 1,111,766) = **2,209,308**, `backlog-adp-refill`, lower bound. Both equal README `:199`, `:201`, `:205`, `:437`, `:439` and the PR body | author-r4 `head-regrade/A1/table.md:89-100`, `A8/table.md:137-147` |
| Fan-out ranges (R703-3-F3) | Every cell is inside its stated range: all 58 fan-outs, A+B, are 11,786 to 22,030 cycles a recipient; arm A is 11,818 to 20,486. 1x1 runs 7.77 to 14.80 ms (A: 7.77 to 11.33). 8x8 runs 12.39 to 32.78 ms (A: 12.39 to 22.98). SET_NAME is 20,358 to 20,486, SET_STREAM_INFO 21,875 to 22,030, BIND_RX's notice 18,358 to 18,475, the rest 11,786 to 13,440 (A: 11,818 to 13,440). The README table `:291-305` agrees with these cells | author-r4 `receipts/f3/fanout_cells_and_ranges.txt`; `README.md:310-312`, `:454-456`, `:461` |
| Docs gates at the head | rc 0 for `check_baremetal_only.py --check` (0 findings, 1431 files), `check_doc_style.py`, `check_doc_paths.py` and `check_py_idiom.py`. Not run here: em dash, `gen_toc.py --check` and `--verify-anchors` need the pinned Markdown renderer, which this environment lacks (rc 2, cannot judge). The author's receipts show all three at rc 0 at this head | `receipts/gates/*` |
| Probes on the new code | 10 single-edit mutants against `run.py --self-test`, each restored by bytes; then a demonstration on synthetic window sets | `scripts/r703_4_probes.py`, `receipts/probes/probes.json` |
| Clone restored | No porcelain changes. Worktree equals index equals HEAD, with the same modes and blobs. 0 rehash mismatches in the harness. The six gitlinks match HEAD's tree | `receipts/clone_identity_final.txt` |

Probe results (`receipts/probes/probes.json`):

| Probe | Self-test |
|---|---|
| P1 `BACKLOG_ROWS` drops `backlog-adp-refill` | caught |
| P2 `BACKLOG_ROWS` drops `backlog-owed` | caught |
| P3 the table drops "at least" from a lower-bound composed maximum | **escaped** |
| P4 the table drops the ", a lower bound (load unreleased in …)" clause | **escaped** |
| P5 `results.json` omits `composed_maximum` | **escaped** |
| P6 fan-out recipients' commits not sorted before first and last | **escaped** |
| P7 `lower_bound` only when the longest window is the unreleased one | **escaped** |
| P8 the released-only figure taken over every window | caught |
| P9 a record released at exactly its successor's commit counted ahead | **escaped** |
| P10 every earlier record counted ahead | caught |
| D1 `composed_maximum` on arm B's three windows / on one window | `windows: 3` / `windows: 1`, `lower_bound: false` in both; table line "Composed maximum over the 1 backlog windows: 740,260 CPU cycles (14.805 ms), backlog." |

## Findings

### R703-4-F1 MINOR: Robustness, Tests, Docs. A composed maximum over an incomplete set of backlog rows is reported as the composed maximum, and arm B's is

- **Where.**
  - `run.py:73-81` (`composed_maximum`): the figure covers whichever `BACKLOG_ROWS` windows the run contains. Nothing checks that all four were run, and nothing says which were not. `run.py:136` prints "Composed maximum over the N backlog windows" with no qualifier.
  - `README.md:59`: arm B's command, which omits `backlog-adp-refill`.
  - `README.md:197`, `:200` and `:202`: the column "Composed maximum, every backlog window" for arm B.
  - `README.md:207`: "Every window of arm B released its load, so its two figures are the same".
  - `README.md:438`: "In arm B every window released its load, and the composed maximum is 14.81 and 27.84 ms".
  - The PR body row "Composed maximum over every backlog window, arm B (every window released)".
  - `selftest.py:395-401`: the check's second case asserts that a two-window set is a composed maximum with `lower_bound: False`.
- **Authority and evidence.**
  - The delta defines the figure as "the longest pass over every backlog row's window" (`README.md:154`, `run.py:68`, `grade.py:52-53`). Arm B's regrade says "Composed maximum over the **3** backlog windows" at both points (author-r4 `head-regrade/B1/table.md:60`, `B8/table.md:84`; `compare_base_f8876638_vs_head.txt`, `"windows": 3`).
  - `backlog-adp-refill` is a defined-load backlog row (`MAILBOX_SPLIT.md:753-758`; `scenario.py:764`). In arm A it is the 8x8 composed maximum, so it is not a row that cannot matter.
  - D1 shows the general case: a run whose `--groups` selects one backlog row reports "Composed maximum over the 1 backlog windows: 740,260 …" with no qualifier.
- **Impact.**
  - Arm B's "composed maximum" omits a window that carries the defined load. The README and the PR present it as covering every window.
  - The more serious risk is S2c's and S2b's before-and-after, which re-base on this function. A partial re-measure (`--groups` is documented at `README.md:44`) yields a composed maximum that looks complete and is not labelled a lower bound. That is the failure R703-3-F2 closed for unreleased windows, reopened for unrun ones.
  - Arm A, the formal measurement, runs all four rows, so no formal figure at this head is wrong.
- **Required outcome.**
  - `composed_maximum` names the `BACKLOG_ROWS` a run did not include. The table line and `results.json` then label the figure as not over every backlog window (for example, "over 3 of 4 backlog windows, `backlog-adp-refill` not run"), or the run refuses to call it the composed maximum.
  - A named check covers a set with a backlog row missing, and a mutant that drops the rule fails it.
  - The README (`:197-207`, `:438`) and the PR body state that arm B's figure covers `backlog`, `backlog-adp` and `backlog-owed`, without `backlog-adp-refill`. Alternatively, arm B's command adds the refill row and the arm is re-measured.
- **Verification.**
  - D1 in `scripts/r703_4_probes.py` reports the missing rows and the label.
  - A regrade of arm B's logs prints the qualified line.
  - The README and PR text name the three rows.

### R703-4-F2 MINOR: Tests. The new composed-maximum check does not pin its own lower-bound rule or the published label

- **Where.** `selftest.py:388-403`, the check "the composed maximum is the longest pass of every backlog window, a lower bound while one left its load unreleased". `run.py:79` and `run.py:132-140`. `selftest_mutants.py:105-114`, `:341-346`.
- **Authority and evidence.**
  - AGENTS.md, Tests lens: each new test can fail for the defect it claims to detect.
  - The `selftest.py` docstring says each rule is mutated and a named check must fail.
  - In the check's synthetic set the only unreleased window is also the longest. So P7 (`lower_bound=not top['serviced']`) passes, even though the rule the check is named for is "while one left its load unreleased".
  - The published form of the figure is `table.md`'s line, "at least … a lower bound (load unreleased in …)" (`README.md:168`). Neither the table line nor the `results.json` key is checked: P3, P4 and P5 pass. All four escapes run against an otherwise passing self-test (`receipts/probes/probes.json`).
- **Impact.**
  - The case P7 mishandles is the transitional one: the longest window releases its load while a shorter one still starves.
  - That is a plausible S2c outcome. A faster core could let `backlog-adp` finish while `backlog-adp-refill` does not. If the composed maximum's lower-bound label regressed then, the baseline comparison would present a lower bound as a measured maximum, with the self-test green.
  - At this head no published value changes under any of the four.
- **Required outcome.**
  - A named check in which the longest backlog window released its load and a shorter one did not, asserting `lower_bound: True`.
  - A check on the table line's lower-bound wording, or equivalently on the `results.json` `composed_maximum` record that the table renders.
  - Each comes with a mutant in `selftest_mutants.py` that the check kills.
- **Verification.** `scripts/r703_4_probes.py`, unmodified, reports P7, P3 and P4 caught (and P5, if the record is what is checked).

## RESIDUE (purely wording; exact fix given)

- **R703-4-R1: PR body, the row "A recipient's cost, every fan-out (arm A)".**
  - The cells are both arms' ranges with arm A's in brackets (1x1 11,818 to 21,875 (11,818 to 20,358); 8x8 11,786 to 22,030 (11,844 to 20,486)). The numbers are right.
  - The label reads as arm A only.
  - Fix: rename the row "A recipient's cost, every fan-out, both arms (arm A in brackets)".
- **R703-1 R-4 / R704-3-R1 (retained).**
  - `docs/testing/TESTING.md:518` still reads "The manual `nvm_capture_cpu` measurement is the Makefile exception."
  - This file is outside the lane, as disclosed.
  - Fix as R704-3-R1 states it.

## SUGGESTION (optional)

- **S1 (P6).**
  - The fan-out check's three recipients commit in their registration order, so dropping `sorted` at `grade.py:524` passes.
  - Giving the synthetic recipients commits out of registration order would pin "first to last commit".
  - No evidence here shows a published value depending on it.
- **S2 (P9).** A boundary case for a service record's `ahead` would distinguish `r > commit` from `r >= commit`: an earlier record released on the same bus cycle as the commit. It is practically unreachable, so this is optional.
- **S3 (carried from R703-3).**
  - S1 (H3, a value-dependent pass filter) still escapes.
  - S2 (idle-range minimum only) and S3 (R703-2's S1-S3) are not applied, and remain optional.

## Prior public findings at this head

| Finding | Status at `a66148f6` | Evidence |
|---|---|---|
| R703-3-F1 MAJOR (bare-metal gate) | **Resolved.** `scenario.py:805` now reads "the ACMP transmit ring", the gate's term table is unchanged, `check_baremetal_only.py --check` gives rc 0 with 0 findings. Hosted `docs-gates-0` was still in progress at review time | `receipts/gates/baremetal_check.log`; `receipts/hosted_checks_head.tsv` |
| R703-3-F2 MINOR (arm A composed maximum) | **Resolved as required.** Over every backlog window, at least 31.32 / 44.19 ms, a lower bound, with the released-only figure beside it and labelled. README, PR body and S2b/S2c baseline note agree. The incomplete-set gap in the same function is the new F1, and the label's protection is F2 | head-regrade A1/A8; `README.md:197-212`, `:437-441` |
| R703-3-F3 MINOR (fan-out ranges) | **Resolved.** Every range contains every cell, with arm A's beside it | `f3/fanout_cells_and_ranges.txt`; `README.md:310-312`, `:454-456`, `:461` |
| R703-3-F4 MINOR (two rules unprotected) | **Resolved.** G6 and G9 are caught by the unmodified round-3 script. My P10 is caught too | `receipts/review_mutants3_head.log` |
| R703-3-R1 (SET_STREAM_FORMAT) | **Applied** as written | `README.md:622` |
| R704-3-R2 (`backlog_groups` docstring) | **Applied** | `scenario.py:845-852` |
| R704-3-R3 (owed row label) | **Applied** | `README.md:362` |
| R704-3-R4 (PR body sequencing) | **Applied** | PR body, Status paragraph |
| R703-1 R-4 / R704-3-R1 | **Retained** as residue | `docs/testing/TESTING.md:518` |
| R703-2 N11, N12 and R703-3 G2, G3, H3 escapes | Unchanged. None changes a published value, as recorded before | `receipts/review_mutants{2,3}_head.log` |

## Comment rule (delta)

- No added line in the delta's Python carries a bench lane label, lane name, review round, reviewer ID or issue-comment ID (`receipts/delta_f8876638_a66148f6.diff`).
- "A3" at `scenario.py:805` is `MAILBOX_SPLIT.md`'s assumption A3.
- The README's new baseline bullet (`README.md:439-441`) names S2b and S2c and links an issue comment. The README is a findings page, not a source comment, so this is not residue.

## Lens ledger (reviewer-owned)

| Lens | Result | Examined artifacts (at the head) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | **CLEAN** | `[R703] PASS Conformance — run.py:67-81, README.md:197-212, :437-441, :454-456, PR body table; author-r4 head-regrade A1/A8/B1/B8 table.md and compare_base_f8876638_vs_head.txt — the S2 acceptance (worst pass at the composed maximum; every backlog row at 1x1/1 interface and 8x8/2 interfaces; each against T_svc and the 3.4.1 ceiling) is met for the formal arm: all four rows are run, the composed maximum is the maximum over them (1,565,803 / 2,209,308 cycles) and is labelled a lower bound because SRP's load is never released; the fan-out figures are within their stated ranges` | R703-4 | `a66148f6b7e59e3f42c939f464fe76e2b05404d7` |
| RTL | **CLEAN** | `[R703] PASS RTL — receipts/delta_stat.txt (git diff --stat f8876638..a66148f6) and receipts/ast_delta.txt — no RTL, SoC (split_soc.py), sim_main.cpp, observe.vlt, build.py, firmware or CI file is in the delta and scenario.py's code is unchanged, so the R703-3 RTL result (mailbox RX_HEAD/RX_TAIL mod 2^16 accounting against mailbox.yaml:419-433, all RX_TAIL writes on record boundaries) still holds for what it depends on` | R703-4 (R703-3 at `f8876638`, an ancestor whose RTL-lens scope the delta does not touch) | `a66148f6b7e59e3f42c939f464fe76e2b05404d7` |
| Robustness | **UNCLEAN** (F1) | `run.py:67-81`, `:126-140` against configuration-dependent group selection (`--groups`, `README.md:44`, `:59`); D1 | R703-4 | `a66148f6b7e59e3f42c939f464fe76e2b05404d7` |
| Tests | **UNCLEAN** (F1, F2) | `selftest.py:325-403` (new checks); `selftest_mutants.py:76-114`, `:336-348`; `receipts/selftest_head.log`; `receipts/probes/probes.json` (P1-P10); `review_mutants{2,3}_head.log` | R703-4 | `a66148f6b7e59e3f42c939f464fe76e2b05404d7` |
| Docs | **UNCLEAN** (F1) | `README.md` delta by section (`:149-168`, `:193-212`, `:305-312`, `:362`, `:427-470`, `:505-530`, `:557-566`, `:619-622`); `grade.py:1-30`, `:49-57` docstrings; the PR body (live, matching the author-r4 packet apart from one trailing blank line); the docs gates in `receipts/gates/` | R703-4 | `a66148f6b7e59e3f42c939f464fe76e2b05404d7` |

My round-2 and round-3 ledger entries stand for code this delta does not touch: `sim_main.cpp`, `build.py`, `split_soc.py`, `frames.py`, `runtime_ssp.py`, `fixture_variant.py`, `observe.vlt`, `fixture.log` and `oracle.json` are unchanged.

## Real limits of this review

- **No manager source bank** runs at this exact head, and I claim none. Source-head execution evidence is the author's published receipts plus the runs listed here.
- **No simulation was re-run.**
  - The figures at this head are the author's regrade of round-3 logs. R703-3 reproduced those logs' figures to the cycle at `f8876638`.
  - The delta changes no script or measured input (`ast_delta.txt`), so I accepted the regrade receipts.
  - The fan-out per-recipient cells come from `results.json` files that are not published (their digests are), so I checked the ranges against the author's cell listing rather than raw logs.
- **Docs gates not run here:** em dash and the two TOC gates. The pinned Markdown renderer is absent and shared installs are out of scope. I accepted the author's rc 0 receipts.
- **Hosted evidence.** At review time, 8 of 46 exact-head check runs had succeeded and 1 was skipped. 37 were queued or in progress, including `docs-gates-0` (which carries the bare-metal gate) and the fail-fast guards. `docs-gates-1`, `docs-gates-2` and `docs-check-no-git` succeeded (`receipts/hosted_checks_head.tsv`). Hosted and act acceptance belong to the manager.
- **Physical calibration NOT RUN.** Every figure is a simulated cycle count on the test SoC. No hardware was used, and field skips are not hardware proof.

## Pending manager duties

- Validate the current-dev merge candidate (source base `e76a755a`, live dev `76de691e5625cc4ea2f9a19def9e07c1183a14ee`) with the builder and native banks. Own hosted and act acceptance at the exact head.
- Carry R703-4-R1 and R-4 / R704-3-R1 to the residue checklist.
- Tell S2c and S2b that the composed maximum must be compared over the same four backlog rows (F1). Until F1 is fixed, the figure does not show when a row was not run.
- Decide the carried question: whether the SRP starvation, the ACMP owed-capacity drop and the per-recipient fan-out cost become Issues or S2b scope.

## Receipts

`MANIFEST.sha256` lists every publishable file. All paths are relative to this packet.

- `scripts/r703_4_probes.py`: the probes P1-P10 and D1.
- `scripts/ast_delta.py`.
- `scripts/review_mutants2.py`, `scripts/review_mutants3.py` and `scripts/sandbox.sh`: R703-2's and R703-3's published scripts, byte-identical.
- `receipts/`: the self-test, the probes, both mutant reruns, the gates, hosted checks, the delta and its stat, the AST comparison, the environment and the clone's final identity.

R703-4 FINISHED
