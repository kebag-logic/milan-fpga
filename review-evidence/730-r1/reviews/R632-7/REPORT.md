[R632] POSITIVE - exact head b341e875d87c6aa2be355bad17f373782517f723

# R632-7: internal cleared-context review of PR #731 (issue #730)

- **Head under review:** `b341e875d87c6aa2be355bad17f373782517f723`, tree `82915e6c72b793bdf50a3b615afa5b03a6883c07`. GitHub reported this SHA as the PR head when the review was done.
- **Full diff:** source base `dc4d06cb`; `dc4d06cb..b341e875`, 13 commits. `scripts/act_ci.py` +2631/-171; `docs/testing/CI_WORKFLOWS.md` +167/-8.
- **Round 7 delta:** `73b8dcd6..b341e875`, `scripts/act_ci.py` +79/-0, test only. I diffed it: one new arm family (`scripts/act_ci.py:12466-12472`) and its helper `act_interrupt_signal_case` (`scripts/act_ci.py:12476-12545`). No runtime line changed.
- **Scope:** a FULL review of the PR at this head, applying all five lenses over the whole diff, plus the Round 2-7 obligations named in the assignment.
- **Order:**
  1. AGENTS.md and CONTRIBUTING.md.
  2. docs/README.md.
  3. Issue #730: its body, assignment 6131408752, ruling 6131815815 and the Round 2-7 manager comments.
  4. The full diff and history.
  5. Executable evidence.

  I wrote the verdict, findings and ledger below before reading any prior reviewer report. The section "Prior public findings" was added afterwards.

## Verdict

POSITIVE. No BLOCKER, MAJOR or MINOR finding is open under any lens at this head. There is one RESIDUE, which is PR-body wording only, and three SUGGESTIONs. None of them changes the verdict or leaves a lens unclean.

## Findings

### R632-7-R1 - RESIDUE - Docs - PR #731 body, section "Status"

- **Evidence.** The body says: "The two Round 6 commits are pushed; the PR head is `73b8dcd667aa5bf1254e828dd1dd7217c8a103ce`. The new Round 7 commit is local and unpushed." GitHub reports the PR head as `b341e875d87c6aa2be355bad17f373782517f723` (`gh pr view 731 --json headRefOid`, read during this review). So the Round 7 commit is published.
- **Impact.** Wording only. It changes no measurement, figure, verdict, test, code, generated artifact, conformance or clause claim, and it touches no privacy rule.
- **Exact fix.** Replace those two sentences with: "The Round 7 commit is pushed; the PR head is `b341e875d87c6aa2be355bad17f373782517f723`."
- **Verification.** Compare the Status section with `headRefOid`.

### R632-7-S1 - SUGGESTION - Tests - `scripts/act_ci.py:5921-5922`; `docs/testing/CI_WORKFLOWS.md:1784-1785` and `:2185-2186`

- **The code is right.** The runtime derives the ranges, and refuses when it must, before `replay_slot` is entered. The authoritative document says the same.
- **Probe D3 confirms it.** Each of the following refuses with event order `['refused']`, before the slot is entered, before submodules and before any plan line:
  - a `max-parallel` of 5;
  - an expression `max-parallel`;
  - a 39-CPU host for slot 1.
- **The gap.** No standing self-test arm pins this ordering. Mutant T01, which moves the derivation inside `replay_slot`, survives the self-test (rc 0). Probe D3 kills it.
- **Why only a suggestion.** Code and document agree, and the self-test list in `CI_WORKFLOWS.md` does not claim to pin this ordering.
- **Suggested outcome.** Add an arm through `run_validation` with a recording `replay_slot`. It should require a derivation or host Refusal before the slot is entered.

### R632-7-S2 - SUGGESTION - Tests - `scripts/act_ci.py:5921`

- **The code is right.** The runtime reads the workflows of the materialized PR checkout (`layout.checkout`). Probe D3 shows it: in a PR checkout where both shard jobs name `max-parallel: 2`, slot 3 plans exactly `64-67 68-71`.
- **The gap.** No arm pins it. Mutant T09 survives the self-test. It reads `ROOT` instead of `layout.checkout`, the same defect as R632-3's Q29. It survives because the self-test's checkout is a copy of the runner's own workflows. Probe D3 kills it.
- **Suggested outcome.** Add an arm whose checkout workflow differs from the runner's copy.

### R632-7-S3 - SUGGESTION - Tests - `scripts/act_ci.py:5871` and `:15934`

There are two self-test survivors. In both cases the code is correct at this head.

- **T06.** `report_job_cpu_ranges` reads the record after the monitor has joined its reader. Moving the report inside the `with` block survives, because no arm orders the report after `cpus-off`.
- **T02.** The live interrupt probe refuses unless its container was moved. Disabling that check survives, because the check runs only in the live `--interrupt-selftest`.
- **Suggested outcome (optional).** Add an assertion that orders the report after the monitor exits. Add an offline arm through `run_interrupt_probe`, with stand-ins whose record shows no move.

## Lens results (clean lenses carry their evidence)

```text
[R632] PASS Conformance - scripts/act_ci.py:2090-2139, :4671-4762, :5380-5543, :5900-5963; .github/workflows/rtl.yml:147-160, :449-462; act v0.2.89 pkg/model/workflow.go:236-250, pkg/runner/runner.go:171-214, pkg/common/executor.go:95-103, pkg/runner/job_executor.go:105-117 - acceptance 1-3 and the assignment items, checked against act's own source. Per stage, act runs CONCURRENT_JOB_LIMIT jobs, each min(max-parallel, legs) wide, default 4, floor 1. Probe D1/D2 oracle: 13 literal shapes and 72 selection x limit cases agree; 12 non-literal shapes are refused. --rm removes failed legs' containers. Every range is 4 CPUs wide (nproc 4), and the ranges are disjoint for slots 0-63 (D5: 320 ranges, 1280 CPUs). Slot N stays inside 20N..20N+19. The derivation reads the PR checkout (D3). An unreadable or too-wide max-parallel, or a short host, refuses before slot entry on every slot, slot 0 included (D3). D4 shows the dry-run lines of all four workflows in slots 0 and 3. The diff leaves the memory constants untouched. Acceptance 3's same-head verdict comparison, and acceptance 4 and 5, are post-merge under ruling 6131815815 and are not claimed here.
[R632] PASS RTL - scripts/act_ci.py:278-320, :353-440, :5313-5375, :5380-5543, :5574-5770, :15791-15810, :15926-15940 - the diff has no HDL: git diff --stat dc4d06cb..b341e875 shows two files, neither under hdl/. I applied the lens to the runner's state machine and concurrency architecture, which is what the RTL lens names. JobCpuRanges transitions: create/start/update/die/destroy, with default paths for unknown, foreign and malformed events. One assign per container; the reservation is made before the assign; a range is released only on destroy or when inspect shows the container gone. Signal-mask windows: the monitor's hold is set before the body's last yield; the act window is unblocked and then restored; delivered_after restores the incoming mask. The reader inherits the mask through start_cleanup_safe_thread. No unmasked runner thread exists during a normal replay: the threads at :5755 and :15637 both start through start_cleanup_safe_thread, and the serve_forever threads at :16194 belong only to a live self-test fixture. The ownership, lease and Refusal contracts are unchanged.
[R632] PASS Robustness - receipts/probe_r632_7_lifecycle-at-head.log; receipts/probe_r632_7_derivation-at-head.log; receipts/r633-4-probe_cleanup_entry-at-head.log; receipts/r633-5-probe_boundary_precedence-at-head.log; receipts/probe_r6_interrupt_diag-at-head.log; receipts/probe_shutdown-at-head.log - 1500 randomized lifecycles (5 modes x 300 seeds, about 401k events) with lagged, reordered, duplicated and lost-destroy events, and with moves that are applied then time out, lost then land late, refused, or unreadable. No two live containers ever share a range. No container sits on a job range it has not reserved. No late landing hits another container's range. With at most 4 containers alive, none is ever left on staging. Malformed and foreign events, a too-wide or unreadable max-parallel and a short host are each refused. The cleanup-entry, closing-restore, interrupt and shutdown probes pass unchanged.
[R632] PASS Tests - receipts/selftest-head.log (531 ok, 0 FAIL); receipts/mutants_r632_6-at-head.log; receipts/mutants_r2-at-head.log; receipts/mutants_r3-at-head.log; receipts/mutants_r632_7-at-head.log; scripts/act_ci.py:12466-12472, :12476-12545 - the six Round 7 arms are present, each named by signal and placement. Each asserts: exit 128+signal; exactly the conventional diagnostic, by string equality, so no closing line can pass; act started unmasked, or not at all; containment under the hold; trail ['contained', 'stream ended', 'outer teardown']; a closed pipe; a restored mask; nothing pending. S8 is KILLED with fails=6 by those named arms. The earlier campaigns keep their published outcomes: 36/36; 24/30 with Q24 KILLED; R632-6 8/10. My own set kills 10 of 14: T03, T04, T05, T07 and T08, plus 5 probe-validity controls that also fail my probes. The four survivors are recorded as SUGGESTIONs above.
[R632] PASS Docs - docs/testing/CI_WORKFLOWS.md:1551-1558, :1724-1729, :1742-1895, :2177-2192, :2397-2400; receipts/gates/*.log - each changed statement was checked against the code at this head: staging then move; a reservation held until destroy or until inspect shows the container gone; --rm; derivation and its refusals before slot entry; the slot block 20N..20N+19; on 128 CPUs, slots 1-5 fit any shipping workflow and slot 6 fits one-container workflows; the mask, delivery and first-failure precedence; both diagnostics verbatim; the mixed-runner warning. No other authoritative doc carries the old 4N layout (grep over *.md). The slot marker in act_slot_proof.sh matches only the unchanged 'own daemon' prefix. docs_check, doc_style, gen_toc --check and --verify-anchors, check_em_dash (0 findings over 167 added lines), check_doc_paths and ci_events --check (2016 items) all exit rc 0. The PR-body wording defect is RESIDUE R632-7-R1 and leaves the lens clean.
```

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | issue #730 acceptance 1-5, assignment 6131408752, ruling 6131815815; the derivation, layout, refusal order and dry-run path in `scripts/act_ci.py`; `.github/workflows/*.yml`; act v0.2.89 source (four files); probe D1-D5 | R632-7 | `b341e875d87c6aa2be355bad17f373782517f723` |
| RTL | CLEAN | no HDL in the diff; the runner's `JobCpuRanges` state machine, the monitor, the act boundary, `delivered_after`, the signal-mask windows, the thread inventory | R632-7 | `b341e875d87c6aa2be355bad17f373782517f723` |
| Robustness | CLEAN | lifecycle probe (5 modes x 300 seeds); derivation probe refusals; the R633-4, R633-5, R632-6 and R632-2 probes, unchanged | R632-7 | `b341e875d87c6aa2be355bad17f373782517f723` |
| Tests | CLEAN | self-test 531/0; the Round 7 arms; the R632-6, R632-2 and R632-3 campaigns, unchanged; my own 14-mutant campaign | R632-7 | `b341e875d87c6aa2be355bad17f373782517f723` |
| Docs | CLEAN | the `docs/testing/CI_WORKFLOWS.md` diff, the doc gates, consumer scripts, the PR body (RESIDUE R632-7-R1 only) | R632-7 | `b341e875d87c6aa2be355bad17f373782517f723` |

## Round obligations at this head

- **Round 7 (R632-6-F1).**
  - **What the arms do.** They send a first signal through the real `execute_act_boundary`, inside the real `job_cpu_range_monitor`. There are two cases: during act, and pending before act.
  - **What they require.** With no earlier failure, exit `128 + signal` and exactly `act-ci: interrupted by SIG<NAME> after cleanup\n`. The comparison is by string equality, so a closing line cannot pass (`scripts/act_ci.py:12539-12544`).
  - **R632-6 campaign.** The driver `mutants_r632_6.py` ran unchanged (sha256 `eb8d4ca1...e92385e58`). S8 is KILLED with rc 1 and fails=6. The first named FAIL arm is "first SIGINT during act, no earlier failure: conventional status and only the interrupt diagnostic, cleanup complete".
  - **R632-6 probe.** `probe_r6_interrupt_diag.py` ran unchanged: rc 0, all six cases.
  - **Runtime.** The delta changes no runtime line.
- **Round 6 (R633-5-F1).** The probe `probe_boundary_precedence.py` ran unchanged (sha256 `de624785...68e700`): rc 0, all nine cases. In each, the original Refusal and its status 2 are kept, and containment, reader completion and pipe close finish before outer teardown. The 18 closing-restore self-test arms pass.
- **Round 5 (R633-4-F1).** The probe `probe_cleanup_entry.py` ran unchanged (sha256 `2bcf4697...79b822`): rc 0, all six cases, with 130/143/129. The masked-step sweep arm passes. My mutants T05 (no hold over the body) and T08 (the mask never restored) are both KILLED.
- **Round 4 (R632-3-F1).** The driver `mutants_r3.py` ran unchanged: 30 mutants, 24 killed, Q24 KILLED. The survivors are Q06, Q11, Q13, Q15, Q28 and Q29, as published. There are no bad anchors.
- **Round 3 (R632-2-F1, R633-2-F1).** The driver `mutants_r2.py` ran unchanged: 36 of 36 killed, including K12, K13, K32 and K36. `probe_shutdown.py` passes S1-S4. The first-failure precedence arms pass.
- **Round 2 (R633-1-F1..F4, R632-1-F1..F2).**
  - **Self-test arms that pass:** the restart sequence; an update applied before the CLI times out; slot 0 refusing a short host; a reap failure with the reader joined.
  - **Independent re-proof:** my lifecycle probe (invariants I1-I4) and the L1-L4 controls prove the same properties again.
  - **Verdict independence:** the staging warning never changes a verdict (`selftest_cpu_range_warnings`).
- **No live replay.** None ran in this review. Self-test, probes and campaigns ran in a disposable boundary with no network, no Docker socket and a read-only system.

## Executed evidence (this review, at this head)

**Environment.** Every candidate execution ran inside `scripts/sandbox.sh`: no network, no Docker socket, a read-only system and a private `/tmp`. The interpreter was CPython 3.14.7 with PyYAML 6.0.3. The tree is a `git archive` of the head; its `scripts/act_ci.py` blob is `15257b8a`, identical to the head's.

**Support scripts.** `scripts/sandbox.sh` and `scripts/probe_r2.py` are byte-identical copies of the public R632-6 and R632-2 scripts (sha256 in `MANIFEST.sha256`). They sit where the unchanged drivers expect them. The drivers and probes I re-ran are under `public-inputs/`, fetched from evidence commit `16c2f70e`. Their sha256 values match the values cited in the public record: `mutants_r632_6.py` eb8d4ca1..., `mutants_r2.py` c78da783..., `mutants_r3.py` 2ef94964..., `probe_boundary_precedence.py` de624785..., `probe_cleanup_entry.py` 2bcf4697....

**Self-test.** `act_ci.py --selftest`: rc 0, 531 ok, 0 FAIL, 26 s.

**Repository gates (all rc 0):**

- `ci_events.py --check` (2016 items) and `--selftest` (2828 arms).
- `act_slot_proof.sh --selftest` (44 cases).
- `check_py_idiom.py`, with unchanged ratchets, and `--selftest` (54).
- `check_baremetal_only.py --check` and `--selftest` (700).
- `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base dc4d06cb` and `check_doc_paths.py`. These used the pinned renderer (cmarkgfm/html5lib).
- `git diff --check dc4d06cb b341e875`.

**Mutation campaigns (each driver rc 0):**

| Campaign | Mutants | Killed | Survivors |
| --- | --- | --- | --- |
| R632-6 | 10 | 8 | S5, S6, as published |
| R632-2 | 36 | 36 | none |
| R632-3 | 30 | 24 | as published |
| R632-7 (mine) | 14 | 10 | T01, T02, T06, T09 |

**Probes (all rc 0):**

- `probe_r632_7_lifecycle.py`, 300 seeds per mode.
- `probe_r632_7_derivation.py`.
- Unchanged: `probe_r6_interrupt_diag.py`, `probe_cleanup_entry.py`, `probe_boundary_precedence.py`, `probe_shutdown.py`.

**Probe validity.** My probes can fail:

| Mutant | What it breaks | Probe that fails |
| --- | --- | --- |
| L1 | a `die` frees the range | lifecycle |
| L2 | an unreadable inspect frees the range | lifecycle |
| L3 | an off-target move releases the range | lifecycle |
| L4 | a timed-out move releases the range | lifecycle |
| T07 | destroy events are not read | lifecycle (I5) |
| L5 | `max-parallel` is ignored | derivation |
| T01 | the derivation runs inside the slot | derivation |
| T09 | the runner's own workflows are read | derivation |

**Clone integrity after all probes.**

- The worktree is clean.
- The index digest and the gitlinks are identical to before: `external` efeb541a, `gptp-processor` 7dda9c3b, `protocol-processor` 2ad2f845, `third_party/lwSRP` 08ee86e8, `third_party/verilog-axis` 48ff7a7e.
- Blobs: `scripts/act_ci.py` is `15257b8a` (mode 100755); `docs/testing/CI_WORKFLOWS.md` is `a9ded0c0` (mode 100644).
- No probe wrote to the clone.

## Prior public findings

(Added after the verdict, findings and ledger above were written.)

Source: the PR #731 conversation comments; the PR has no submitted reviews. Each disposition below is judged at this head, against the code and receipts above. Each finding keeps its original lenses.

| Finding(s) | Severity / lenses | Disposition at `b341e875` | Evidence here |
| --- | --- | --- | --- |
| R633-1-F1 (`die` freed a restartable container's range) | MAJOR, all five | RESOLVED | `observe` releases only on `destroy` (`:5525-5541`). Restart arm in `selftest_job_cpu_record`; lifecycle I1/I2 over 1500 runs; L1 and K01 KILLED |
| R633-1-F2 (an uncertain update freed its target) | MAJOR, all five | RESOLVED | `place` reserves before the assign and keeps the reservation on failure (`:5487-5518`). Move-failure arms; lifecycle I3; L4, K02, K03 KILLED |
| R633-1-F3 (slot-0 silent fallback) | MAJOR, all five | RESOLVED | `job_cpu_ranges` refuses on every slot (`:4719-4740`). Probe D3 (39 CPUs, slot 1); slot-0 boundary arm; K15 KILLED |
| R633-1-F4; R632-1-F1 (reap failure skipped the join; no arm failed without the join) | MAJOR, all five; MINOR, Tests and Docs | RESOLVED | `stop_job_cpu_range_monitor` runs every step (`:5610-5672`). Busy-reader arms; K09, K10, K11 KILLED |
| R632-1-F2 (verdict invariance not pinned at run level) | MINOR, Tests | RESOLVED | `selftest_cpu_range_warnings` (`:6589`); K23 KILLED |
| R632-1-R1, R632-1-R2 | RESIDUE, Docs | APPLIED / SUPERSEDED | Mixed-runner warning at `CI_WORKFLOWS.md:2188-2190`; the slot-0 fallback is gone and the PR table states the refusal |
| R632-1-S1..S4 | SUGGESTION | ADDRESSED | S1-S3 by the F1/F2/F4 fixes above. S4: the summary distinguishes "removed before that" |
| R633-2-F1 (first failure must win) | MINOR, all five | RESOLVED | `primary` passed to stop; `delivered_after` keeps it. Precedence arms; Q01-Q04 KILLED |
| R632-2-F1 (K12/K13/K32/K36 survived) | MINOR, Tests | RESOLVED | All four KILLED by named arms (`receipts/mutants_r2-at-head.log`) |
| R632-2-S1 | SUGGESTION, Tests | ADDRESSED | K29 and K31 KILLED |
| R632-2-S2 / R632-3-S2 / R632-4-S2 (signal at cleanup entry) | SUGGESTION, later MAJOR as R633-4-F1 | RESOLVED | See R633-4-F1 |
| R633-4-F1 (first signal at cleanup entry skips containment) | MAJOR, all five | RESOLVED | Mask held from before the yield to final restore (`:5736-5770`). Unchanged cleanup-entry probe passes; masked-step sweep arm; T05 and T08 KILLED |
| R632-3-F1 (derivation not graded in every order) | MINOR, Tests | RESOLVED | Q24 KILLED; probe D2 covers 24 selections x 3 limits |
| R633-5-F1 (closing-restore signal replaced the active failure) | MINOR, all five | RESOLVED | `execute_act_boundary` (`:5313-5375`). Unchanged nine-case probe passes; 18 closing arms; S1, S2, S3, S7, S10 KILLED |
| R632-5-R1, R632-5-R2 | RESIDUE, Docs | APPLIED | Exact wording at `CI_WORKFLOWS.md:1833-1834` and `:1838` |
| R632-5-S2 (per-step count depends on the interpreter) | SUGGESTION, Tests and Docs | ADDRESSED | The PR body says the count depends on the interpreter. This run records 185 steps on CPython 3.14.7 (`receipts/selftest-head.log:123`) |
| R632-6-F1 (no arm pins the conventional interrupt diagnostic) | MINOR, Tests | RESOLVED | Six named arms (`:12466-12472`, `:12476-12545`); S8 KILLED with fails=6; unchanged diagnostic probe 6/6 |
| R632-6-R1, R633-6-R1 (Round 6 PR-body status) | RESIDUE, Docs | Round 6 wording corrected; the same staleness recurs for Round 7 | Carried as R632-7-R1 above. It matches R633-7-R1, the same defect from the external reviewer at this head |
| R632-5-S1 / R632-6-S1 (S9 killed only by rc 129, with no named arm) | SUGGESTION, Tests | RETAINED, optional | `receipts/mutants_r632_6-at-head.log`: S9 KILLED rc=129 fails=0 |
| R632-3-S1 / R632-4-S1 / R632-5-S3 / R632-6-S2 (Q06/Q11/Q13/Q28/Q29 survive; Q15 equivalent) | SUGGESTION, Tests | RETAINED, optional | Same survivors at this head. Q29 is restated with fresh evidence as R632-7-S2 (T09; probe D3 kills it) |
| R632-2-S3 / R632-3-S3 / R632-4-S3 / R632-5-S4 / R632-6-S3 (a join that raises at once is reported as "survived its bounded shutdown") | SUGGESTION, Robustness | RETAINED, optional | Code unchanged at `:5584-5596`; the hold itself is accurate |
| R632-6 S5/S6 (campaign survivors) | not findings (equivalent) | Unchanged | Both survive at this head, as published |

No prior BLOCKER, MAJOR or MINOR finding was downgraded or moved to another issue to clear a lens. Every prior finding at those severities is resolved in the code at this head.

The external round at this head, R633-7 (POSITIVE, published while this review was running), was read only after the sections above were written. Its one RESIDUE is the same PR-body staleness recorded here as R632-7-R1. Its retained suggestions match the RETAINED rows above. Nothing in it changes this verdict.

## Real limits

- **No live Docker.** Under the ruling and the assignment, no `docker events`, `docker container update` or `docker container inspect` ran against a live daemon in this review.
  - The record's behaviour is proven against two independent model daemons: the self-test's and mine.
  - Two Docker behaviours are assumed from Docker's documented behaviour, not observed here: event ordering, and the label attributes on `update`, `die` and `destroy` events.
- **`nproc` 4 is inferred, not run.** It follows from every range being 4 CPUs wide and from kernel cpuset semantics. No container was started.
- **The live interrupt probe's move requirement (T02)** is pinned only by the live gate, which was not run.
- **One interpreter.** The candidate ran on CPython 3.14.7 only, because the local CPython 3.12 has no PyYAML and shared installs were not allowed. The hosted docs workflow exercises 3.12.
- **act's source, not its binary.** act's behaviour was read from the upstream v0.2.89 source on GitHub. The local act 0.2.89 binary was not disassembled.
- **A CPython window that cannot be closed.** A signal can arrive in the bytecode window between entering an `except` clause and its `primary = exc` assignment, both in `execute_act_boundary` and in the monitor.
  - CPython cannot close that window without masking.
  - If it happens, the signal's conventional status wins over the failure. Containment is unaffected.
  - I do not raise it as a finding. It is inherent to the platform, and far narrower than the delivery points the rounds were asked to close.
- **Hosted evidence is a snapshot.** `receipts/hosted-checks-snapshot*.txt` holds snapshots of the exact-head hosted checks, taken while some jobs were still in progress. I make no acceptance claim; the manager owns hosted and act acceptance.
- **No manager source bank** ran at this head, and none is claimed or inferred.
- **Physical calibration was NOT RUN.** Skipped field contexts are not hardware proof.

## Pending manager duties

- **Publication.** Publish this packet, and carry RESIDUE R632-7-R1 (the exact PR-body fix above) to the residue checklist.
- **Hosted and act acceptance at this head:** rtl-fast, verilator-suites, yosys-portability and docs-check, plus act acceptance.
- **Merge-candidate validation** against current dev: source base `dc4d06cb`, live dev `49da9fd974e8805d56c90e29dcfcb67994c2c430`, builder and native banks, with the receipts linked on the PR.
- **Post-merge, under ruling 6131815815.** The issue stays open for these (`Relates to #730`):
  - acceptance 3: the same-head verdict comparison and the `nproc` check;
  - acceptance 4: the before/after measurement, covering per-job wall clock, the slot memory peak, and a CPU-range summary with `m == n`, `k == 4` and no CPU-range warning;
  - optional acceptance 5.
- **Disk ruling.** Any slot data-root those measurements create is recorded and removed, as the issue's disk note requires.

R632-7 FINISHED
