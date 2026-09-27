[R372] NEGATIVE - exact head 3a0cb4cf4fed2d71436a43f4b96cb375f9178342

# R372-2: internal independent review of PR #605 for #395 items 1, 2 and 5

- **Head:** `3a0cb4cf4fed2d71436a43f4b96cb375f9178342`, tree `f6398593ff7a0449150cc18dd361e85cff6675d6`.
- **Delta under review:** `66001a30..3a0cb4cf`. This is two commits, `09de469c7` and `3a0cb4cf4`. Each has a one-line message with no trailers. I also read the full diff from `8bc97021f28fb7f729418d3a00851c84ea0b50fd`.
- **PR body:** "Relates to #395", with no closing keyword.
- **Context:** cleared. I rebuilt the task from public material only:
  - AGENTS.md and CONTRIBUTING.md;
  - the #395 body, the owner decision (5789765635), the margin decision (5860418611), the round-2 assignment (5860419679), and the [A390] TAKEN and REVIEW READY comments (5860428534, 5860663722);
  - #607;
  - BUILDING section 5, RUNNING_TESTS sections 4 and 5, and LITEX_SOC section 7;
  - the public evidence tree `42822357:review-evidence/395-r1`;
  - the exact-head hosted checks;
  - my own R372-1 packet.
- **Read order:** I wrote the verdict and ledger below before reading the other reviewer's round-1 report. That report is dealt with under "Prior public findings".

## Verdict summary

The round-2 content is correct, and I reproduced it independently:

- **Round-1 findings:** all three of mine (F1 to F3) are answered at this head.
- **Warning census:** the record's census of the rejected crossing constraints matches the shipping build log line for line.
- **Crossing measurements:** all sixteen intended-bound numbers in the record, across four directions and two models, reproduce exactly on the read-only checkpoint.
- **Planted faults:** each of my five former survivors now makes the builder-bank entry fail. A 30-plant campaign run through both test entries has no unexpected outcome.
- **Margin:** item 2 is graded against the recorded margin decision, and the record cites it.
- **PLL speed grade:** derived from the single declaration, with a changed-part control that goes through the real AX7101 constructor.

The verdict is NEGATIVE for one finding. The round-2 text of the record fails a required repository gate at this exact head: `scripts/check_baremetal_only.py --check`. The hosted required context `docs-check` is red for this reason. Every later docs-check step was skipped, including the hosted end-station builder gates. I reproduced the failure locally and in a disposable copy. Rewording one line clears it.

**Correction to my round-1 report.** R372-1 F1 said the shipping log has "15 CRITICAL WARNINGs". The correct count is **14 emitted diagnostics**: ten 12-4739, two 12-5201 and two 20-1307. The fifteenth substring match is at log line 6400. It is echoed source text from the IOB-pack hook, not a diagnostic (`receipts/r2-critical-warning-census.txt`). The record at `docs/findings/COMMERCIAL_TIMING_395.md:104-107` has this right.

## Findings

### R372-2-F1 - BLOCKER - Docs, Tests

**Location:** `docs/findings/COMMERCIAL_TIMING_395.md:115`, introduced in `09de469c7`. Hosted `docs-check` job 108727991180 (run 36357487267).

**Title:** The new record line fails the bare-metal scope gate, so the required `docs-check` context is red at the exact head.

**Authority and evidence:**

- CONTRIBUTING lists `docs-check` among the seven required status-check contexts. RUNNING_TESTS section 4 lists `python3 scripts/check_baremetal_only.py --check` as a static gate.
- At this head the gate reports: `docs/findings/COMMERCIAL_TIMING_395.md:115: [R] prohibited target runtime/service surface '/sys': 'Ethernet/sys crossings remain **unbounded false paths**, in both directions.'`, then `baremetal-only: FAIL`, exit 1.
- **Hosted:** step 23 "Bare-metal scope gate" failed. Steps 24 to 51 were skipped, including "End-station builder gates", the idiom gates, the contents gate and the doc cited-path gate (`receipts/r2-hosted-docs-check-failure.txt`, `receipts/r2-hosted-checks-3a0cb4cf.tsv`).
- **Local:** the failure reproduces in the clone (`receipts/r2-t7-baremetal-scope-gate.log`, rc 1; the `--selftest` passes with 700 arms).
- **Round-1 head:** at `66001a30` the record had no such line (`git show 66001a307:docs/findings/COMMERCIAL_TIMING_395.md | grep 'Ethernet/sys'` is empty).
- **Disposable copy:** changing only `Ethernet/sys crossings` to `Ethernet-to-system crossings` makes the gate return `OK (0 findings)`, rc 0 (same receipt).
- **Scope of the author's evidence:** the REVIEW READY validation list does not name this gate.

**Impact:**

- The PR cannot meet AGENTS section 7, which requires the local verification gates to pass, or CONTRIBUTING's required contexts.
- Because the hosted builder and static gates behind step 23 did not run at this head, there is no hosted exact-head evidence for them.

**Required outcome:**

- `scripts/check_baremetal_only.py --check` passes at the new head, and the hosted `docs-check` completes green with its later steps executed.
- The gate and its patterns are not weakened. The fix is wording in the record, and the record's meaning must not change.

**Verification:** rerun `python3 -B scripts/check_baremetal_only.py --check` and `--selftest` at the new head, and read the new head's hosted `docs-check` step list.

### Suggestions (no effect on coverage)

- **S1 (Docs, RTL): `COMMERCIAL_TIMING_395.md:115-117` and #607's acceptance 2.**
  - The record attributes the masking of the eth/sys bound to "the generic LiteX MultiReg false path" alone. My probe classifies every crossing endpoint (`receipts/r2-v1-crossings-r2-results.txt`, part A).
  - Sys to Ethernet has 16 endpoints: 12 are `mr_ff` D pins, and 4 are `ars_ff1/ars_ff2` PRE pins under the separate AsyncResetSynchronizer false path at shipping `xdc:568`. The worst sys-to-Ethernet endpoint, `FDPE_14/PRE`, is one of those four.
  - The fully exposed milan-to-Ethernet population has 14 endpoints: 8 are ARS PRE pins, including the record's worst, `FDPE_18/PRE`.
  - Every sentence in the record is true, but it is incomplete. Naming `xdc:568` alongside `xdc:566` would let #607 decide explicitly whether reset-assertion paths stay false-pathed. That is conventional, since assertion is asynchronous by design.
- **S2 (Tests): `sw/builder/test_timing_grade.py:186-189`.** The file's own `__main__` does not call `test_pll_grade`, so running the file standalone does not exercise the PLL control. The builder bank does (`test_builder.py:27556-27564`), and my `pll-literal-restored` plant shows the split: the focused entry survives, the builder entry kills (`receipts/r2-t3b-mutation-probes-r2.log`). No documentation cites the standalone entry.
- **S3 (Docs): the older gate wording is not aligned with the new rule.**
  - `sw/litex/milan_soc.py:206-207` still describes the AX7101 PLL as "speedgrade -2" in a comment.
  - The BUILDING gate table (`BUILDING.md:72`) still heads the row "WNS ≥ 0" with the +0.03 caveat.
  - `RUNNING_TESTS.md:155` still says "non-negative post-route WNS" above the new +0.03 ns rule at `:168-170`.
  - The margin decision says the sweep "already enforces" the rule. In fact `sweep.sh` launches three directives and the pick is manual. No hook refuses WNS below +0.03 ns or WHS below 0.
  - The PR's own text does not claim automatic enforcement. Aligning the older lines would remove the ambiguity.
- **S4 (Docs): `COMMERCIAL_TIMING_395.md:125`.** The record names the retained `crossings.tcl` and `crossings-results.txt` without a location. The only public evidence tree named for this round is the round-1 packet (`42822357:review-evidence/395-r1`, head `66001a30`), which does not contain them. I reproduced the numbers independently, so this is a traceability gap only. It is also listed under pending manager duties.
- **Retained from R372-1:**
  - S1: "UG835 documents that operating-condition temperature is not used for timing" at `:57`, unchanged.
  - S2: the pre-placement hook fixes power Tj at 85 C.
  - S3: reporter argument edges; `report_timing_grade.py` is unchanged.
  - S4: `docs/findings/README.md` does not list the record.

## Round-1 findings (mine), at this head

| Round-1 finding | Status | Evidence |
|---|---|---|
| F1 (MAJOR): record misses the rejected crossing constraints | **Resolved** | See the checklist below |
| F2 (MINOR): five surviving planted faults | **Resolved** | See the checklist below |
| F3 (MINOR): margin decision not recorded | **Resolved** | See the checklist below |

**F1 checklist:**

- **Census:** the record `:78-110` names the rejected exceptions at `xdc:583-591` (12-4739, and 12-5201 at :591) and `:595` (20-1307), with the build log's line numbers. It gives the source `milan_soc.py:1520-1534` and `:1550-1556` at `66001a30`, and the missing `milansoc_` prefix as the cause. The source lines are identical at this head (`receipts/r2-milan_soc-1497-1558.txt`).
- **Census re-derived from the shipping log:** 1705/4118 (583), 4123 (585), 1710/4128 (587), 4133 (589), 1719/1721/1723 and 4142/4144/4146 (591), 1724/4147 (595). The log is 832920 bytes with sha256 `4519c33a...60a6`, as recorded (`receipts/r2-critical-warning-census.txt`, `receipts/r2-shipping-xdc-579-597.txt`).
- **Cause of the unsafe pairs** (`:112-114`): confirmed. With the shipping constraints, eth to milan is 50 timed endpoints at a 4.000 ns requirement, and the reverse pair is 6 timed plus 8 false-pathed out of 14. The clock-interaction classifications are `Timed (unsafe)` and `Partial False Path (unsafe)` (`receipts/r2-v1-A-shipping-clock-interaction.rpt`).
- **Unbounded eth/sys false paths** (`:115`): confirmed in both directions, 13 and 16 endpoints, all `False Path`. See S1 for the attribution.
- **Measured slack against the intended 8 ns bound** (`:121-149`): my `reset_timing` probe reproduces every table value. The distinction the second commit draws is right:
  - Slow: eth to sys 2.179/5.746, sys to eth 3.395/4.313, eth to milan 5.373/2.560, milan to eth 3.652/4.056.
  - Fast: 1.240/6.717, 1.979/5.895, 3.092/4.823 and 1.996/5.878.
  - Milan to eth has 14 endpoints, and the worst is `FDPE_18/PRE`.
  - My round-1 six-endpoint milan-to-eth figure (+7.066/+7.538 ns) was taken with the generic false paths still loaded (`scripts/vivado_probe.tcl` P3 in the R372-1 packet had no `reset_timing`), exactly as `:142-144` states.
- **#607** is linked at `:118` and owns the fix and the build refusal.
- **Retention list:** BUILDING section 5 names the CRITICAL WARNING census (`BUILDING.md:554-557`), as do RUNNING_TESTS `:175` and LITEX_SOC `:157`.

**F2 checklist:**

- **The five former survivors:** my unchanged R372-1 script at this head gives 22 plants and `unexpected=0` (`receipts/r2-t3-mutation-probes-r1-script.log`). All five are now killed, each by the assertion naming the fault:
  - `reports-no-leading-check` fails as `('part', 'kl_timing_grade_reports ...'`;
  - `reports-corner-setup-only` and `reports-corner-no-unconstrained` fail on the per-corner SUMMARY line;
  - `reports-all-no-check-verbose` fails on the combined SUMMARY line;
  - `reports-clock-interaction-setup-only` fails on the `report_clock_interaction` row.
- **Extended campaign:** 30 plants, each run through the file's own entry and through `test_builder.test_commercial_timing_grade()` (the first function the full builder bank calls; an exception ends the bank non-zero). Result: `unexpected=0` over 60 runs, and the unmodified control passes both with no skip (`receipts/r2-t3b-mutation-probes-r2.log`). The eight added plants are:
  - the PLL literal restored;
  - combined summary setup-only and without unconstrained paths;
  - `report_cdc` without `-details`;
  - `check_timing` without `-verbose`;
  - negative report setup-only and without the slack filter;
  - a report written before the leading refusal.
- **Hook probe:** at this head the hook refuses all four wrong conditions, rc 1. The leading-check mutant still accepts three of them, and the test now kills that mutant (`receipts/r2-t4-hook-refusal-probe.log`).

**F3 checklist:**

- The margin decision (5860418611) is cited and applied at record `:61-67`: WNS 0.123 ≥ +0.03, a surplus of 0.093 ns, and WHS 0.036 ≥ 0 at every row.
- It is also cited at BUILDING `:536-539`, RUNNING_TESTS `:168-170` and LITEX_SOC `:158-160`.
- The REVIEW READY comment grades item 2 against it.

## Answers to the assigned checks

1. **Record contents.** Everything the assignment lists is present and correct (see the F1 checklist). The one defect is that line 115's wording fails the scope gate (R372-2-F1).
2. **Planted faults.** All five now fail the builder bank (see the F2 checklist).
3. **Item 2 margin.** Graded against the recorded decision, and the decision is cited (see the F3 checklist).
4. **PLL speed grade.** `sw/litex/milan_soc.py:215` now reads `S7PLL(speedgrade=-int(platform.device.rsplit("-", 1)[1]))`.
   - `platform.device` is `TIMING_GRADE["part"]` (`alinx_ax7101.py:297`), so the declared part yields -2, the same value as the removed literal, and the generated PLL is unchanged.
   - `test_pll_grade` patches the declaration to -1 and asserts that the real AX7101 `_CRG` passes -1. My `pll-literal-restored` plant is killed by `AssertionError: call(speedgrade=-2)`.
   - Edge probe: -1, -2 and -3 derive correctly. `-2L`, `-1LI` and a part with no grade suffix fail loudly at elaboration (ValueError or IndexError), so they fail closed (`receipts/r2-t5-pll-edge-probe.log`).
   - The only other speed-grade literal is the Arty branch's `-1`, which is outside the AX7101 declaration.
5. **Items 3 and 4 stay open, and no timing or constraint fix is made.** The PR body says "Relates to #395". In this delta, the only source change outside tests and docs is `milan_soc.py:215`. The XDC-generating lines 1499-1556 are byte-identical to `66001a30` (`receipts/r2-milan_soc-1497-1558.txt`).

**Other gates at this head:**

- `docs_check.py`, `check_doc_paths.py` and `git diff --check` pass, both from the base and from `66001a30` (`receipts/r2-t6-docs-gates.log`).
- The static gates skipped behind the hosted failure pass locally: Python idiom, hygiene, fail-fast, test-evidence, TODO ownership, archive, feature-status and naming.
- The contents gate could not run here because the pinned Markdown renderer is not installed (`receipts/r2-t8-skipped-docs-check-static-gates.log`).

## Reviewer-owned ledger

| Lens | Result | Artifacts examined | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #395 body, owner decision, margin decision and round-2 assignment against: record `:61-149`; `milan_soc.py:215`; `alinx_ax7101.py:297`; the shipping build log census (`r2-critical-warning-census.txt`); shipping `xdc:579-597`; the Vivado crossing probe (`r2-v1-*`); #607; PR body (no closing keyword) | R372-2 | 3a0cb4cf4fed2d71436a43f4b96cb375f9178342 |
| RTL | CLEAN | No HDL in the diff. Examined: `milan_soc.py:195-216` PLL derivation (generated PLL unchanged at -2); the clock and CDC claims in record `:72-149` against the read-only checkpoint (endpoint classes by `mr_ff`/`ars_ff` tag, 4 ns relationship, clock-interaction classes, intended-bound slack; `r2-v1-crossings-r2-results.txt`, `r2-v1-A-shipping-clock-interaction.rpt`); only S1 open | R372-2 | 3a0cb4cf4fed2d71436a43f4b96cb375f9178342 |
| Robustness | CLEAN | `milan_soc.py:215` derivation under -1/-2/-3/-2L/-1LI/no-suffix parts (`r2-t5-pll-edge-probe.log`); the hook under four wrong conditions (`r2-t4`); the no-write-before-refusal assertion (`reports-write-before-check` killed); `timing_grade.tcl` and `report_timing_grade.py` unchanged since the R372-1 coverage at `66001a30` (`git diff 66001a307 3a0cb4cf4` on both is empty); only the retained R372-1 S3 is open | R372-2 | 3a0cb4cf4fed2d71436a43f4b96cb375f9178342 |
| Tests | UNCLEAN (R372-2-F1) | `sw/builder/test_timing_grade.py:73-189`; `test_builder.py:27556-27564`; focused and builder-entry runs, rc 0 (`r2-t1`); R372-1 22-plant rerun (`r2-t3`); 30-plant, two-entry campaign (`r2-t3b`); hook probe (`r2-t4`); trailing-check plant (`r2-t11`, read after the ledger was written); the bare-metal scope gate, red (`r2-t7`); hosted `docs-check` failure (`r2-hosted-docs-check-failure.txt`) | R372-2 | 3a0cb4cf4fed2d71436a43f4b96cb375f9178342 |
| Docs | UNCLEAN (R372-2-F1) | `COMMERCIAL_TIMING_395.md` (all 175 lines); BUILDING section 5 (`:515-562`) and `:72`; RUNNING_TESTS sections 4 and 5 (`:119-128`, `:155-180`); LITEX_SOC section 7 (`:145-164`); `docs/findings/README.md`; docs and static gates (`r2-t6`, `r2-t7`, `r2-t8`) | R372-2 | 3a0cb4cf4fed2d71436a43f4b96cb375f9178342 |

## Real limits

- **Timing work:** read-only static analysis of the saved routed checkpoint with the installed Vivado 2026.1 (build 6511674), at 8 threads. I did no synthesis, placement, routing or bitstream generation.
  - The intended-bound measurement uses in-memory `reset_timing`, the two primary clocks and the 8 ns datapath-only bound. It measures datapath delay against that bound. It does not prove CDC correctness, and it does not cover future seeds.
  - The shipping inputs and log were hashed before and after the probe, and are unchanged (`receipts/shipping-inputs-before.txt`, `receipts/r2-t10-shipping-inputs-recheck.txt`).
- **Tcl stubs:** the mutation campaigns drive the Tcl hook through the PR's own tclsh stubs, not live Vivado. Live-tool refusal of the unchanged `timing_grade.tcl` was shown in R372-1 (P2). The builder-entry arm links scratch git copies of the three pinned populated submodules into each extraction, because `git archive` omits them and `milan_soc` lists their files.
- **Pre-existing constraint defect:** the defect at `milan_soc.py:1520-1534` and `:1550-1556` is still in the tree. This PR does not touch it, it is on dev, it is outside this lane's scope by the manager's decision, and #607 owns it. My round-1 F1 asked for it to be disclosed, not fixed. The RTL lens here covers the diff and the record's clock and CDC claims. It does not certify the shipping constraint set.
- **Scoped Verilator:** not used. There is no HDL in the diff.
- **Gates I did not run:** the full builder, parent, PP, gPTP and Yosys banks, and the act runner, none of which is permitted. The contents gate (`gen_toc.py`) could not run locally. The manager's banks stand as published. The public tree named for them is the round-1 packet at `66001a30`, and I found no public round-2 bank evidence.
- **Hardware:** physical calibration NOT RUN. No hardware or temperature measurement was made. Items 3 and 4 remain unmeasured.
- **Hosted status**, read at review time:
  - Failed: `docs-check` (R372-2-F1, with steps 24 to 51 skipped).
  - Succeeded: `rtl-fast`, `bdd-conformance`, `changes`, `docs-check-no-git`, `full-ci-gate`, `verilator-lint`, `wire-accountability`, `yosys-elaboration`, Yosys shards 0 to 3, and Verilator shard 3.
  - Still in progress: `elaborate` and Verilator shards 0, 1, 2 and 4.
  - Skipped: "Physical gPTP", which is not hardware proof.
- **Clone integrity after the probes:**
  - HEAD, the index write-tree and the head tree are equal, and the worktree is clean.
  - All 945 tracked blobs match by hash and mode.
  - The four gitlinks match the tree. `external` is unpopulated, as it was at checkout (`receipts/r2-t9-clone-integrity.txt`).
  - The public evidence commit was fetched into a scratch bare repository, not the clone.

## Pending manager duties

- Publish this verdict, and relay R372-2-F1 to the executor lane.
- Publish the round-2 author evidence, including `crossings.tcl`, `crossings-results.txt` and the census, at a public location the record can cite (S4).
- Relay S1 to #607: the ARS PRE false path at `xdc:568` masks the reset endpoints alongside the MultiReg path.
- File or assign the follow-ups that remain unowned since round 1: GMII RX/TX I/O delay constraints, and triage of the ten Critical CDC diagnostics. I found no open issue for either.
- Own hosted acceptance. `docs-check` must be green at the next head, with its builder and static steps executed. `elaborate` and four Verilator shards were still running at this head. The local-replica run and the current-dev candidate build belong to the merge turn (source base `8bc97021`, live dev `20aa4eab`).
- Re-review is needed at the next head. R372-2-F1 is a Docs change, and it un-covers Docs and needs Tests re-covered through the gate rerun. Conformance, RTL and Robustness stay covered at this head only if the next head changes nothing in their scope beyond the record wording.

## Prior public findings

I read these only after the verdict and ledger above were written. That reading changes neither.

**R372-1 (mine), comment 5860399025:**

- F1, F2 and F3 are resolved at this head, as shown in the table and checklists above.
- The count correction for F1 is also stated above.
- My R372-1 suggestions S1 to S4 are retained as suggestions.

**R373-1, comment 5860415369:**

| Item | Status at this head | Evidence |
|---|---|---|
| F1 (MINOR): record omits the cause of the unsafe pairs | **Resolved** | See below |
| S1: margin not recorded | **Resolved** | The decision is recorded (5860418611) and applied at record `:61-67` |
| S2: PLL literal | **Resolved** | `milan_soc.py:215` derives from the declared part, and `test_pll_grade` kills the restored literal |
| S3: three report-argument mutants survive | **Two resolved, one retained** | See below |
| S4: shared LiteX skip text at `test_builder.py:27561` | **Retained** | The call is unchanged, and it is a suggestion |
| S5: power Tj pinned at 85 C | **Retained** | Same as my retained R372-1 S2 |
| S6: reporter creates the directory before refusing a brace path | **Retained** | Same as my retained R372-1 S3; `report_timing_grade.py` is unchanged |
| NEW-1: crossing constraints never apply | **Owned by #607** | Linked from the record |
| NEW-2: GMII I/O delays | **No owner found** | Search of open issues on 2026-09-28 |
| NEW-3: CDC Critical triage | **No owner found** | Search of open issues on 2026-09-28 |

**R373-1 F1 in detail:**

- The record names the dropped exceptions with their log lines and codes, the source lines and the clock-name-prefix cause. It states the 4 ns relationship and the intended-bound slack, and it separates the reviewer's 7.066 ns figure from the fully exposed 4.056 ns. It links #607.
- BUILDING section 5 retains the census.
- R373-1's own verification also asked for the docs gates at rc 0. `docs_check.py` and `check_doc_paths.py` pass. The bare-metal scope gate fails on the new text, which I carry as R372-2-F1.

**R373-1 S3 in detail:**

- Combined summary without `-report_unconstrained`: now killed (`reports-all-no-unconstrained`).
- `report_cdc` without `-details`: now killed (`reports-cdc-no-details`).
- Dropping the trailing post-restore `kl_timing_grade_check` at `timing_grade.tcl:73`: still survives (`receipts/r2-t11-trailing-check-plant.log`). This is second-order. The test already proves the `finally` restore through the `SUMMARY 85 Slow min_max Fast min_max` assertion, so this check only matters if the restore also breaks. It was not among the five faults the assignment required, and it stays a suggestion.

**NEW-2 and NEW-3:** these are new work outside this lane, not findings against it. They are listed under pending manager duties.

R372-2 FINISHED
