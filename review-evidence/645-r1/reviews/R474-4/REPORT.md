[R474] NEGATIVE - exact head 85db353400c6bf3965d279a9f5b5d47e08a0d1ed

Review R474-4: internal cleared-context review of PR #672 (issues #645 and #647), round 2e.

- Exact head: `85db353400c6bf3965d279a9f5b5d47e08a0d1ed`, tree `67922e03f4c2d5d8add9b41f6f4c169ea3c9a364`.
- Delta reviewed: `2525eae9..85db3534`. It holds the `--no-ff` merge `9a0d68e2` of dev `99e4eb6c` and the wording commit `85db3534`.
- Baseline: R474-3 and R475-3, both POSITIVE at `2525eae9`.

The merge composes cleanly, and the lane's RTL is byte-identical to `2525eae9`. Every functional campaign I re-ran at the head passes. One MAJOR finding is open, under Tests and Docs:

- The lane's two default suites no longer fit the 1,800 s per-suite wall clock on the hosted runner.
- At this exact head, hosted `Verilator shard 0/5` killed both `follow_ring` and `milan_dp_render` at 1,800 s, so `verilator-suites` is red.
- Dev's `milan_dp_render` took 1,112 s on a runner of the same speed.

One new wording RESIDUE and one carried wording RESIDUE do not affect the verdict.

## Scope and method

Context was read in this order:

1. AGENTS.md and CONTRIBUTING.md.
2. docs/README.md.
3. Issue #645's frozen acceptance and every manager ruling. These are 5982568394, 5985974804, 5987852678, 5990646410, 5994641859, 6009543884, 6009767440, 6009790232, 6010634115, 6032466525, 6041375798, the round-2e assignment 6050481968, and #691 ruling 6045752839.
4. The PR body and REVIEW READY 6056511818.
5. The diff and merge history.
6. The author packet `review-evidence/645-r1/author-r2e` at `00f489b1`.

Prior review reports were read only after my draft verdict and ledger were written (`receipts/DRAFT-VERDICT-PRE-PRIOR-READ.md`, 13:28:32Z). The MAJOR finding came later, from exact-head hosted evidence that finished after that draft.

Execution used the pinned simulator, version 5.050 rev v5.050. Its wrapper's SHA-256 is `905795b9...e92f`, and the binary's is `44898b22...bfdd`. No job used more than 16 parallel workers.

- `follow_ring` and `chmap_capture` ran in a `git archive` export of the head with its three submodules.
- The render and physical legs need git metadata (`scripts/pp_srcs.py`), so they ran inside this clone, which was then restored.
- Commands are in `scripts/run_focused.sh`.

## Findings

### R474-4-F1 MAJOR: the lane's default suites exceed the hosted per-suite wall clock; exact-head `verilator-suites` is red

- **Lenses:** Tests, Docs.
- **Where:**
  - `tb/verilator/follow_ring/Makefile:64-65`: `all: run mutants`. The default target is four legs plus twelve rebuilt controls.
  - `tb/verilator/milan_dp_render/sim_tdm8_render.cpp:110-115, 3762-3810`: the `[PULLIN]` standing phase, which the lane added to the default shipping leg.
  - `docs/testing/TESTING.md:288-290` and the `milan_dp_render/Makefile` header's budget paragraph. Both still state the pre-lane figure: "663.8 s cold ... about 1049 s, inside the 1800 s budget".
  - Hosted run `37773988913`, job `113300393423`.
- **Authority:**
  - `docs/testing/CI_WORKFLOWS.md:188-247` (per-suite wall clocks).
    - A budget is the measured hosted worst case plus a stated margin.
    - Default suites above 80% of their budget take a ruled increase (#673).
    - "The #545 decision keeps all clean checks under 1800 seconds", and long mutation campaigns move to explicit targets under #367's rule.
  - AGENTS.md section 7 requires exact-head `verilator-suites` evidence.
  - The stage-2 ruling (5982568394) requires that "all existing render-law campaigns ... stay green".
- **Evidence** (`receipts/hosted-shard0-suite-times.txt`, `receipts/hosted-*-shard0.log`). Times are in seconds.

  | Commit | Short shared suites (gptp_txts / ptp / rx_filter) | `follow_ring` | `milan_dp_render` | Shard result |
  |---|---|---|---|---|
  | dev `99e4eb6c` | 68 / 24 / 16 | (not in dev) | 1,112 PASS | 11/11 |
  | lane `2525eae9` | 50 / 17 / 12 | 1,366 PASS | 1,259 PASS | 12/12 |
  | head `85db3534` | 72 / 24 / 17 | **1,800 TIMEOUT** | **1,800 TIMEOUT** | exit 92, `verilator-suites` failure |

  - The head's runner ran the short shared suites at dev's speed, within about 5%. The `2525eae9` pass ran on a runner about 27% faster.
  - Scaled to a dev-class runner, `2525eae9` itself would be about 1,870 s for `follow_ring` and about 1,725 s for `milan_dp_render`. Those are 104% and 96% of the budget.
  - The author's own local receipts show the same growth. `render-default` took 1,408.9 s at the head against 777.0 s for `dev-render-default`, which is +81%. At TESTING.md's stated 1.58x hosted slowdown that is about 2,226 s.
  - No in-suite check failed: the shard reports 0 in-suite failures. The suites ran out of time.
  - My own local `follow_ring` `make all` took about 1,107 s on a shared 16-core host. No wall time or budget basis for `follow_ring` is recorded anywhere.
- **Impact:**
  - The protected `verilator-suites` aggregate cannot grade `follow_ring` or `milan_dp_render` at this head. Exit 92 is TIMEOUT/UNKNOWN, and the job is red.
  - After a merge, every dev sweep on a normal runner would carry the same two unknowns. CI would then stop grading T30, `[LAW]`, `[PULLIN]` and the twelve settle controls.
  - The documented render budget is now a false measurement claim.
  - Whether a hosted run passes depends on which runner class it lands on, as `2525eae9` shows.
- **Required outcome:** this needs a decision on the route.
  - **Either:** the default targets fit the 1,800 s guard with a stated hosted margin, for example by moving `follow_ring`'s mutation arm and/or the render `[PULLIN]` standing phase to explicit targets under #367's rule. Their coverage must be kept in a declared campaign that someone runs.
  - **Or:** a ruled budget increase in the #673 form. It needs the measured hosted worst case plus a margin. That figure goes into `scripts/run_all_suites.sh` `suite_timeout`, the `CI_WORKFLOWS.md` table and the `measure_test_evidence.py` pins, and the shard envelope must be re-checked.
  - **In both cases:** `TESTING.md:288-290` and the render Makefile header state the new measured figure, and `follow_ring` gains a stated wall time.
- **Verification:**
  - An exact-head hosted `verilator-suites` with `follow_ring` and `milan_dp_render` PASS, not TIMEOUT, on a dev-class runner.
  - The recorded measurement matches the receipts.
  - `measure_test_evidence.py --check` and its self-test pass.

### R474-4-R1 RESIDUE: TESTING.md's "test plan" link lands on a section without the controls column

- **Lenses:** Docs (wording only).
- **Where:** `docs/testing/TESTING.md:514`, second link: "the controls column of the [test plan](../design/MEDIA_CLOCK_FOLLOWING.md#settle-recentre)".
- **Evidence:**
  - `#settle-recentre` (`MEDIA_CLOCK_FOLLOWING.md:1060-1263`) contains no control list. Searching it for mutant, planted, twelve, controls or "test plan" finds nothing.
  - The twelve-control column is in `## Test plan` / `### Simulation` (`:1507-1545`).
  - TESTING.md's other test-plan links already use `#simulation` (`:493, :527, :528`).
  - The anchor came from R474-3-R2's own prescribed fix, which the author applied verbatim.
- **Why wording only:** it changes no check, figure, verdict, code or generated artifact. The anchor exists, so the anchors gate passes.
- **Exact fix:** in that second link on line 514 only, replace `MEDIA_CLOCK_FOLLOWING.md#settle-recentre` with `MEDIA_CLOCK_FOLLOWING.md#simulation`. The first link on the line, "[settle recentre]", stays as it is.
- **Verification:** follow the link; `gen_toc.py --verify-anchors` still passes.

### Carried: R475-2-R2 RESIDUE, retained unchanged

- `docs/design/MEDIA_CLOCK_FOLLOWING.md:1086` still locates the preserved #386 trigger as `g_settle_recentre`. That block is `g_src_recentre` (`milan_datapath.sv:6533`).
- The file is unchanged since `2525eae9`.
- Exact fix: replace that one parenthetical identifier with `g_src_recentre`.

## Prior public findings at this head

| Prior finding | Status at `85db3534` | Evidence |
|---|---|---|
| R474-3-R1 RESIDUE: the mutation-driver docstring under-counts its plants and its usage line lacks `--select` | **RESOLVED verbatim** | `tb/verilator/follow_ring/mutants.py:6, 11-13`; `MUTANTS` (`:81-127`) has 12 entries, four of them capture plants (`:77, :124`); 12/12 caught in my run |
| R474-3-R2 RESIDUE: TESTING.md names five of the twelve controls | **RESOLVED as prescribed**; its anchor is corrected by R474-4-R1 | `TESTING.md:514` |
| R475-2-R1 RESIDUE: the PR body's Status called the head local | **RESOLVED** (superseded) | The Status section now reads "REVIEW READY at `85db3534` ... Independent reviews and the protected publication/merge gates remain required"; "local until" no longer appears |
| R475-2-R2 RESIDUE: locator at `MEDIA_CLOCK_FOLLOWING.md:1086` | **RETAINED** (RESIDUE) | See above |
| R474-2-S1, R474-2-S2, R474-2-S3 / R474-1-S2 SUGGESTION | **RETAINED** (SUGGESTION) | `settle_control.py`, `quiet_distributions.py` and `sim_ax1x1gptp.cpp` are unchanged since `2525eae9`. The physical run had two decisions, so the NOT RUN branch at `:1101` was not taken |
| R474-2-F1 MINOR, R474-1 F1-F4, R475-1 F1-F3 | Remain **resolved** | The merge touches none of their artifacts. The lane HDL is byte-identical to `2525eae9`. chmap 785/0, the span checks and the HELD-DUP, STARVED-HELD-DUP and SINGLE-DROP controls are all caught |
| R475-3 | No findings of its own | Its carried items are listed above |

## Independent execution at this head

Every return code is preserved in `receipts/`. All runs below are mine.

- **Merge audit** (`scripts/merge_audit.sh`, `receipts/merge-audit.txt`):
  - 38 lane paths and 91 dev paths, with no path changed on both sides.
  - Every path of `9a0d68e2` equals one of its two parents, so the composition is exact.
  - The gitlinks at the head are processor `2ad2f845`, time processor `5dce647a` and AXIS `48ff7a7e`, the same as dev.
  - `85db3534` touches only `TESTING.md` and `mutants.py`.
- **`follow_ring` `make all`** at the head export: rc 0.
  - `[B8]`: 48 checks, 0 failures. `[PULLIN]`: 18 checks, 0 failures.
  - Small pulls 10/10. The settle controller passes at 6.25, 25, 50 and 100 MHz.
  - **12/12 controls caught**, each by its named check.
  - The follow_ring inputs are unchanged since `2525eae9` except the `mutants.py` docstring.
- **Arrival campaign replay:** two of the 128 runs. Both returned rc 0 and are **byte-identical** to the published logs.
  - `slow-none` p00, SHA-256 `4ea7c226...`.
  - `fast-uniform60` p05, SHA-256 `5b0d42ef...`. It shows margins 4.9997/3.1949 ticks and 0 slips.
- **`chmap_capture`:** **785 checks, 0 failures**, plus the netlist leg at **20/0**. The `[LRC]` held-walk case, the counter checks and the span counter checks pass.
- **Render pull-in** (`tdm8render-pullin`): rc 0. **18/18 phases, 18 x 31 = 558 checks, 0 failures**, every phase gradable, and loopback slips 0 during the pull and 0 after the settle. The settle came 1,246.8 ms after the hold.
- **LAW boundary:** rc 0. **81/81 over 564 windows.** The largest walk is 3 cycles against the stated 5.
- **#657 comparison** (`tdm8render-mutants` at the head; `scripts/compare_657.py`, `receipts/657-comparison.txt`):
  - The head scores 30/34, rc 2.
  - Its four FAIL lines are identical to dev `99e4eb6c`'s 28/32 transcript (the author's dev receipt). They are the epoch-only clean leg, the two arrival-skew clean controls and the surviving uncounted-repeat mutant.
  - The head adds two passes: the clean `--pullin` leg and the missing-settle mutant.
  - No dev outcome line changed. My head transcript's outcomes also equal the author's head transcript.
- **Physical gPTP** (`milan_dp_gptp` `make all`): rc 0.
  - Main 143/0, abort 6/0, no-TX 20/0, no-Pdelay 14/0 and recentre controls 14/0, for **197/0**.
  - `RECENTRE WIRE` at output PDUs 9822 and 95985: declared step -5, observed step -5, dup and skip both 0. This is identical to the author's trace.
- **Source and documentation gates at the head:** 14/14 rc 0 (`receipts/gates/`). They are traceability (`gen_module_matrix --check`), test-evidence, source lists, doc paths, toc, anchors, doc style, docs_check, em dash against dev `99e4eb6c`, py-idiom, fail-fast, hygiene, `git diff --check 99e4eb6c..85db3534` and naming.

**Receipts checked, not re-run:**

- **Timing:** the kept image is AltSpreadLogic_high.
  - Setup +0.066 ns slow and hold +0.024 ns fast, with all four corner reports at TNS/THS 0. The values match the published report table rows.
  - ExtraPostPlacementOpt: +0.057 / +0.024 ns. ExtraTimingOpt: +0.011 / +0.036 ns, below +0.030, recorded and not kept. This conforms to ruling 6045752839.
- **IOB check:** every row shows 21 PASS, 1 INERT (`eth0_rx_er`, no net) and 0 FAIL. All nine GMII RX captures are FDRE cells in ILOGIC, with RX valid at `ILOGIC_X0Y119`. Route status shows 0 routing errors, and the critical-warning lists are empty.
- **Resource gate:**
  - The baseline SHA-256 `aa8f90e7...` equals `syn/ooc/pp_resource_baseline.json` at the head and at dev.
  - The `route-1x1` log reads `RESULT: PASS`.
  - The ooc endpoints (`KL_pp_shadow`, untouched by the lane) are identical to the baseline.
- **Own area:** the OOC inputs' SHA-256 values equal `KL_chan_map_capture.sv` at dev (`7f21dd43...`) and at the head (`2b07955b...`).
  - The utilization reports give settle 41/51 to 74/93 and capture 1,076/1,336 to 1,156/1,372.
  - That is **+113 LUT / +78 FF**, within ruling 1's 120/120.

## Lens results

```text
[R474] PASS Conformance - hdl/milan/milan_datapath.sv:6565-6666 and hdl/ieee1722/aaf/KL_chan_map_capture.sv (byte-identical to 2525eae9, receipts/merge-audit.txt); receipts/head_physical_gptp.log:515-517,686-688; receipts/follow_ring.log; receipts/arrival/ - the settle recentre, symmetric action and two-PDU declaration hold at the merge result: both wire recentres at the declared -5 step with unchanged counters, B8 and pull-in on the law, arrival replays byte-identical; timing kept build and IOB graded per ruling 6045752839; own area 113/78 within ruling 1's 120/120; bench items remain the manager's
[R474] PASS RTL - receipts/merge-audit.txt; hdl/milan/milan_datapath.sv (KL_mbx not instantiated; dev's mailbox delta adds no port to the lane's instances); hdl/ieee1722/aaf/KL_chan_map_capture.sv - lane RTL unchanged by the merge; the new processor pin and mailbox RTL elaborate with it (render, physical and mutant builds rc 0); widths, reset and recovery logic as reviewed at 2525eae9; IOB census and kept-image timing receipts checked
[R474] PASS Robustness - receipts/head_physical_gptp.log (reset reacquisition recentre at PDU 95985, abort, no-TX, no-Pdelay and recentre-control legs 197/0); receipts/head_render_lawb.log (81/81, 564 windows); receipts/render-pullin/ (18 phases); receipts/arrival/fast-uniform60_b8_j60_p05.log (0..60 us envelope, reversed sign) - no regression of the reset, envelope or ambiguity-band behaviour under the merged processor and mailbox content
```

Tests and Docs are UNCLEAN under R474-4-F1; their applied checks are recorded in the ledger below.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #645 acceptance and rulings listed above; merge audit; physical recentre wire trace; follow_ring B8 and pull-in; arrival replays; timing, IOB and own-area receipts against rulings 6045752839 and 1 | R474-4 | 85db353400c6bf3965d279a9f5b5d47e08a0d1ed |
| RTL | CLEAN | `milan_datapath.sv:1215-1222, 1308-1313, 6015-6025, 6562-6666`; `KL_chan_map_capture.sv` lane diff; merge audit (no HDL change from the merge on lane files, no shared path); mailbox port delta; elaboration of render, physical and 34 mutant builds; IOB census | R474-4 | 85db353400c6bf3965d279a9f5b5d47e08a0d1ed |
| Robustness | CLEAN | physical reset reacquisition and accounting legs; LAW boundary 564 windows; 18 pull-in phases; 0..60 us reversed-sign arrival replay; the #657 clean controls unchanged against dev | R474-4 | 85db353400c6bf3965d279a9f5b5d47e08a0d1ed |
| Tests | **UNCLEAN** (R474-4-F1 MAJOR) | follow_ring 12/12 controls, chmap 785+20, #657 comparison, render pull-in and boundary, physical 197/0; hosted shard-0 suite times at dev, `2525eae9` and the head; `CI_WORKFLOWS.md:188-247` | R474-4 | 85db353400c6bf3965d279a9f5b5d47e08a0d1ed |
| Docs | **UNCLEAN** (R474-4-F1 MAJOR, on `TESTING.md:288-290` and the render Makefile budget text; RESIDUE R474-4-R1 and R475-2-R2 carried) | `TESTING.md:288-290, 514`; `MEDIA_CLOCK_FOLLOWING.md:1060-1263, 1507-1545, 1086`; `mutants.py:1-50`; PR body; REVIEW READY 6056511818; 14 source and documentation gates | R474-4 | 85db353400c6bf3965d279a9f5b5d47e08a0d1ed |

## Real limits

- **No vendor implementation ran here.** Timing, IOB, resource gate and own area are author receipts.
  - I checked the corner tables, IOB reports, route status, empty critical-warning lists, the baseline hash and the own-area input hashes against the sources.
  - The published packet lacks the full reports, so I could not re-grade the resource check: `pp_resource_gate.py check` returned NOT COMPARABLE on it.
- **Banks and campaigns not re-run:**
  - The full 61-suite sweep and the builder, firmware, portability and vendor-parser banks were not run; they are outside this review's allowance.
  - I replayed only 2 of the 128 arrival runs and none of the 32 standalone INTERNAL pull-ins. Their inputs are byte-identical to `2525eae9` except a docstring.
- **The #657 dev side** is the author's dev transcript, not my own run. An isolated git-backed dev tree could not be created in this session.
- **Hosted evidence:** the hosted state snapshot (`receipts/hosted-checks-snapshot.tsv`, 14:48Z) shows every context complete. `verilator-suites` and `Verilator shard 0/5` are failure; `Physical gPTP (nightly and manual)` is skipped; every other context is success. A skipped context is not evidence.
- **Not hardware proof:** physical calibration was not run, and field skips do not stand in for hardware results.

## Pending manager duties

- Rule on R474-4-F1's route: explicit targets, or a #673-form budget increase. Then rerun the exact-head hosted `verilator-suites` and the act replica. Hosted and act acceptance are the manager's.
- Validate the current-dev merge candidate, with live dev `17f62ef6` (#654, #686 and its resource re-record), in the builder and native banks.
- Carry R474-4-R1 and R475-2-R2 to the residue checklist.
- Run the B-lane bench repeat of the INTERNAL→AAF and AAF→CRF switches after the merge.
- Run post-merge containment.

## Restoration

`receipts/restoration.txt`:

- HEAD is `85db3534`, tree `67922e03`.
- No untracked or ignored entry remains. The index equals HEAD, and the worktree equals the index in bytes and modes.
- The three submodules are clean at `2ad2f845`, `5dce647a` and `48ff7a7e`.
- Build products from the in-clone runs were removed with `git clean -X`; the clone had none before.

R474-4 FINISHED
