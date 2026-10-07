[R518] NEGATIVE - exact head c4539ff107a6a4c7d2e4a4844182b00a2bf33c82

Round R518-2 is a delta review of processor PR #166 (issue #163). Head `c4539ff107a6a4c7d2e4a4844182b00a2bf33c82`, tree `4378652558345d65dd87efd4f092f41f413226c8`, source base `86a7b0c57831c15e9cd8b42d64cc4a9843f4e726`. [Public review start](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/166#issuecomment-6032441833).

**Verdict.** One open MINOR finding (F1: Tests, Robustness, Docs) makes this round NEGATIVE. Both merges keep both sides. Every check, mutant arm and README count of #163, #42 and #69 is present. The re-anchored `cancel_one_clock_late` arm means what it meant before. The fix commit `c4539ff1` changes no observable bench output. The notify campaign (89 of 89) and the plant audit hold, and the timing receipts agree with the PR body. F1 was found by my own plants at this head, but it was not introduced by the merges: the RTL and section WD are unchanged since round 1. The registered withdraw mask that #163 adds can be removed from all three readers, or delayed by a second clock, and section WD and every section of the default build still pass. The only state in which the mask alone withdraws a frame is a cancellation parked behind another exchange's response. No test exercises that state.

## 1. Scope reconstruction

I read the sources in the assigned order.

- **Repository instructions.** There is no tracked `AGENTS.md` or `CONTRIBUTING.md`. I read `docs/README.md` (conventions; §8 of 09 makes each suite README the evidence home) and `README.md`.
- **Issue #163.** The frozen acceptance is in the issue body. Item 2 reads: "register stage ... no path into the transmit arbiter exceeds about 20 levels. Keep cycle-level behaviour equivalent, or grade the extra cycle in tb/pp_top and tb/aecp_notify with planted mutants".
- **Assignments.**
  - [6015580618](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/163#issuecomment-6015580618): the lane assignment (no port, register-map or parameter change; STOP at 60 LUT / 120 FF).
  - Round 2, [6023618295](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/163#issuecomment-6023618295): merge #42 and keep DN with its nine controls.
  - Round 3, [6028791146](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/163#issuecomment-6028791146): merge #69 and keep both sides of the counter-notification cancel path. Any re-graded check must state its reason.
- **PR #166 body.** It says "Relates to #163". The parent three-directive sweep belongs to pin adoption, which is consistent with acceptance item 3.
- **Authorities.** 03 §8 (F03 arbiter table, Withdrawal row), 08 F08.1 (T-TX-AGING), 09 §8.4 and §8.9, Milan §5.3.4.2 (registry tuple and port) and §5.4.5.3 (any command supersedes the CONTROLLER_AVAILABLE probe). I also read the originator, tx_arbiter and KL_aecp_notify RTL, and the parent OOC recipe and resource gate at parent dev `28f9666f` (`syn/ooc/pp_baseline.py`, `syn/ooc/pp_resource_gate.py`).
- **Diff and history.** `git diff 86a7b0c5..c4539ff1` covers 47 files. The 12-file net PR is against new main `c9f74b68`. I replayed both merges with remerge diffs (`receipts/remerge-diff-*.txt`).
- **Public evidence.** The assigned link pins milan-fpga `fc004672`, which holds only round-1 files. The round-3 author packet `review-evidence/pp163-r1/author-r3/` is at archive commit `c4a23f5a47804a521c54ada84a175b3c11df86d5`. All 52 author-r3 files match their published SHA-256 in `MANIFEST.json` (`receipts/public/author-r3-manifest-validation.json`). No manager evidence comment or manager bank receipt for this head exists on #163, #166 or under `review-evidence/pp163-r1` (see §7).

## 2. What the delta is

| Commit | Content | Reviewer check |
|---|---|---|
| `ff581556` | `--no-ff` merge of main `2ad2f845` (#42, tests only: no `hdl/` change) | four pp_top conflicts; DN and its nine arms retained (plant audit; campaign records) |
| `5fe5ea57` | `--no-ff` merge of main `c9f74b68` (#69: `KL_aecp_notify.sv`, `protocol_processor_top.sv`, ADP and benches) | the five conflicts resolved as remerge diff shows; analysed below |
| `c4539ff1` | the tally block of `tb/pp_top/sim_main.cpp` `main()` moved verbatim into `report_build()` | output identical; scanner clean (§3.4) |

- **RTL delta.** The changed RTL lines vs new main (`git diff c9f74b6..HEAD -- hdl docs tb/tx_arbiter`) equal the round-1 changed lines line for line. These are `KL_pp_tx_arbiter.sv:161-196`, `protocol_processor_top.sv:4444-4458,4480,4500,4578` and the 03 row. `KL_aecp_notify.sv` at head is new main's blob `c8fbce30`, so #69's `ctr_last_r [0:N_CTR_DESC_C-1]` shape, `N_CTR_DESC_C = N_STREAM_IN_P + N_STREAM_OUT_P + 1 + N_IF_P`, `g_ca_turns` and `g_ca_own` are kept byte-exact.
- **Withdraw-mask readers.** `org_withdraw_slot_mask_w` still has exactly one reader, the stage at `protocol_processor_top.sv:4456-4459`. #69 added no new combinational reader into the arbiter.
- **Net bench diff.** `notify_phases.hpp`, `pp_top_wrap.sv` and `tb/aecp_notify/sim_main.cpp` change the same lines as round 2. The only differences are the conflict text and the follow-up helper.

## 3. Lenses

### 3.1 Conformance: CLEAN
- **Delta scope.** The merges add no protocol behaviour of their own. #69's Milan §5.3.4.2 port keying (rows `{index, port}`, per-interface depth, per-interface AVB_INTERFACE counter slots) is unchanged from new main.
- **Supersession.** #163's §5.4.5.3 behaviour is unchanged since round 1. A command supersedes the probe. A cancellation on the arbiter's acceptance clock now lets one complete probe leave, with its exchange gone (WD1). The 03 Withdrawal row documents that race.
- **Interfaces.** Ports, parameters and register maps are unchanged against new main. The withdraw stage is independent of `N_AVB_IF_P`. I ran section WD inside the two-interface top build: 9 of 9 pass, and the unregistered mask fails WD1 and WD2 there too (probes `ctl-if-top-with-wd`, `r-if-top-wd-unregistered`).
- **Round-1 coverage.** For the arbiter's ranking equivalence I cite round 1 (R518-1), because the RTL is unchanged.

### 3.2 RTL: CLEAN
- **Stage at head.** The stage resets to zero, and all three readers take `org_withdraw_mask_r`.
- **Interaction with #69's cancel path.**
  - At one interface (`g_ca_own`), `cx_ok_w` feeds only `ca_cancel_valid_o`.
  - At two interfaces (`g_ca_turns`), cancels leave one per clock and each becomes a mask bit one clock later. The CX_SETTLE_C settle covers originator reports (`ca_rsp`/`ca_fail`), which do not pass through the top's stage.
  - A late answer to a probe that was sent in the race cannot hit a newer probe of the same owner. The originator matches `{key, seq}` with a per-owner sequence counter (`KL_pp_originator.sv:225-235`).
- **Lint.** `scripts/lint_hdl.sh` with the pinned Verilator 5.050 returns rc 0 and 41 `LINT OK` (`receipts/docs/lint-hdl-head.*`).

### 3.3 Robustness: UNCLEAN (F1)
- **Simple path.** A cancellation taken at once, on the selection or the acceptance clock, is graded by WD at one and two interfaces.
- **Parked path (ungraded).** A cancellation parked behind another entry's response in the same clock is not graded at the top (F1). The originator probe (`scripts/originator_j2_mask_probe.sh`, test J2's own stimulus) records:

| Clock | Withdraw mask | Release |
|---|---|---|
| c | 0x18 (slots 3, 4) | none |
| c+1 | 0x10 | slot 3 |
| c+2 | 0x00 | slot 4 |

  The parked slot 4 is therefore covered at c+1 only by the registered mask. The arbiter's other abort term is the release, and it covers slot 4 only from c+2.

### 3.4 Tests: UNCLEAN (F1)
**Executed at head, with the pinned Verilator 5.050** (wrapper and binary hashes in `receipts/identity/toolchain.txt`):

| Run | Result |
|---|---|
| `tb/pp_top`, all seven builds | rc 0, **10,468** = 9,974 + 20 + 178 + 231 + 56 + 3 + 6: new main's 10,465 plus WD's 3 |
| `tb/aecp_notify` | **65** = 42 + 4 + 19, as the merged README states |
| `tb/tx_arbiter` | 66 |
| `tb/originator` | 107 |

**Notify campaign** (`notify_mutants.py --jobs 4`): rc 0, 11 goldens PASS, **89 of 89 KILLED**. Every arm's failing-check count equals its README row (123 rows compared, 0 differences; `receipts/notify-campaign-vs-readme.txt`). The WD/CX and CA/PD failures:

| Arm | Failing checks |
|---|---|
| `withdraw_unregistered` | WD1, WD2 |
| `withdraw_abort_ignored` | WD2, WD3 |
| `cancel_one_clock_late` | IX3, CX1 |
| `ix_new_identity_unset` | IX3, IX4, IX6b, CX1 |
| `settle_dropped` | CA4 |
| `owner_turns_dropped` | CA3, CA4 |
| `depth_shared` | PD1-PD3, CA1, CA2, CA1b |

**Nothing lost from either side** (`receipts/plant-audit/`):
- The notify arm set at head is exactly the union of round 2 (68) and new main (86), which gives 89.
- Every arm's named checks are unchanged. The edits are unchanged except `cancel_one_clock_late` (the stated re-anchor) and `dereg_lost_at_round_end` (identical to new main).
- No string literal (check label) of either parent or of `5fe5ea57` is missing from the head's bench sources.
- All 298 patches apply. 89 notify arms with 96 edits, 110 d3, 33 acmp and 20 gsi arms all plant exactly once.
- At round 2: 283 patches and 68/75. At new main: 298 and 86/89.

**Re-anchored `cancel_one_clock_late`.** In `g_ca_own`, `cx_ok_w` has no reader other than `ca_cancel_valid_o`. Moving the anchor from `ca_cancel_valid_o` to `assign cx_ok_w` is therefore the same mutant: command cancel one clock late, drain cancel immediate. Its failures are unchanged (IX3, CX1). The README states the reason (`tb/pp_top/README.md:2607-2611`). CA4 runs on the bare engine without the top stage, so it is correctly not re-graded (`tb/aecp_notify/README.md:31-35`).

**Fix commit `c4539ff1`.**
- `main()` length: 99 at round 2, 100 at new main, 102 at the merge, 89 at head. The parent's own scanner (`scripts/check_cpp_idiom.py` at parent `28f9666f`, functions only) reports 1 long function at `5fe5ea57` and 0 at head (`receipts/fix-commit/`).
- I ran the full seven-build pp_top suite at `5fe5ea57` and at head. The logs are identical after excluding paths and timings, except for the parallel `g++` order, and identical after sorting. Both give 10,468 with the same per-build tallies. No check is weakened.

**Reviewer-owned plants** (`scripts/reviewer_probes.py`, which builds and grades with the tree's own campaign harness; `receipts/probes/*/results.json`):

| Probe | Defect | Result |
|---|---|---|
| `r-wd-abort-only-comb` | only the arbiter abort reads the combinational mask | KILLED (WD) |
| `r-wd-lane-only-comb` | only the lane readers combinational | KILLED (WD) |
| `r-wd-sticky` | mask register holds its last non-zero value | KILLED (WD, 2) |
| `r-cx-repeated` | cancellation presented in the command's clock and again the next | KILLED (CX1) |
| `r-ca-settle-one` | `CX_SETTLE_C` 3 to 1 | KILLED (CA4) |
| `r-ca-drain-cancel-dropped` | two-interface drain cancel dropped | KILLED (CA) |
| `r-ca-owner-low-bits` | CA owner from the row's low bits | KILLED (CA, 4) |
| `r-pd-any-port-row` | REGISTER may claim any port's row | KILLED (PD, 6) |
| `r-ck-avb1-shares-avb0-window` | AVB_INTERFACE 1's throttle reads AVB_INTERFACE 0's stamp and sent bit | KILLED (CK, 3) |
| `r-if-top-wd-unregistered` | WD in the two-interface top, mask unregistered | KILLED (WD1, WD2) |
| `r-ca-turns-ignore-pending-cancel` | owner turns ignore `cx_pend_r` | survived: **equivalent** (see below) |
| `r-wd-two-clocks` | mask delayed two clocks | **survived** WD 3/3 (F1) |
| `r-wd-mask-dropped` | all three readers see no mask (release term only) | **survived** WD 3/3 (F1) |
| `r-full-two-clocks` | as above, whole default build | **survived** 9,974/9,974 (F1) |
| `r-full-mask-dropped` | as above, whole default build | **survived** 9,974/9,974 (F1) |
| controls | head unplanted: WD, aecp_notify run, interfaces, IF top, IF top with WD | PASS |

`r-ca-turns-ignore-pending-cancel` is equivalent, so it is not a gap. `cx_pend_r` becomes non-zero only on an edge where `cx_ok_w` sends a cancel, which also loads `cx_settle_r <= 3`. While anything is pending, `cx_work_w != 0`, so `cx_ok_w` reloads the settle every clock. Hence `cx_pend_r != 0` implies `cx_settle_r != 0`, and the `cx_pend_r` term of `ca_hold_w` is redundant (`KL_aecp_notify.sv:735-743,765-775`).

### 3.5 Docs: UNCLEAN (F1)
- **Round-3 READMEs.** The aecp_notify README's build table and 65-check sum, the pp_top README's campaign history (68 + 21 = 89) and its mutation table all match the executed results.
- **Gates.** `make check` (in a disposable clone at the exact head) returns rc 0 (`receipts/docs/make-check-head.*`).
- **PR body and timing receipts.** The round-3 section matches the receipts:

| Quantity | Value |
|---|---|
| WNS | +3.337 ns |
| TNS | 0 |
| Failing setup endpoints | 0 |
| WHS | +0.159 ns |
| Maximum arbiter depth | 16 levels |
| Pairs above 20 levels | 0 |
| Startpoints | 328 |
| `u_pp` | 22,478 LUT / 18,951 FF |
| Own logic | -110 LUT / +6 FF |
| Worst arbiter slack | +11.912 ns |
| Base | -3.562 ns, 146,535 pairs above 20, 51 levels |

  The final histogram sums to 17,990 pairs with no level above 20 (`receipts/timing-receipt-audit.json`).
- **Inaccurate timing statement.** The 03 row, the top's comment and the pp_top README WD text say the registered mask arrives "in the clock its registered release reaches the slot pool". That holds only for a cancellation taken at once (F1).

## 4. Findings

**F1 - MINOR - Tests, Robustness, Docs.** The registered withdraw mask is not graded in the only case where it alone withdraws a frame.

- **Locations.**
  - Stage: `hdl/top/protocol_processor_top.sv:4454-4459`, readers at :4480, :4500 and :4578.
  - Section WD: `tb/pp_top/notify_phases.hpp:1814-1838` and :1963-1995.
  - Docs: `tb/pp_top/README.md:2520-2555`, `docs/architecture/03_packet_engine.md:488`, the comment at `protocol_processor_top.sv:4444-4453`, and the PR body's "Graded with planted mutants".
- **Authority.**
  - Issue #163 acceptance item 2 and assignment 6015580618 item 2: "where a cycle is added, grade it ... with planted mutants".
  - Assignment 6028791146 asks the review to verify "#163's registered withdraw mask (+1 cycle, graded by the WD/CX checks)".
  - `KL_pp_originator.sv:314-318`: "Stored cancellations remain masked while a response for another entry consumes the single action lane".
- **Evidence.**
  - In WD's scenario the cancellation is taken at once. The originator's registered release (`txs_release_*`) reaches `arb_start_abort_w` and the lane-queue drop in the same clock as `org_withdraw_mask_r`, so section WD cannot see the mask itself.
  - Removing the mask from all three readers passes WD 3/3 and the whole default build 9,974/9,974 (`r-wd-mask-dropped`, `r-full-mask-dropped`). Delaying it two clocks also passes both (`r-wd-two-clocks`, `r-full-two-clocks`).
  - The mask differs from the release only for a cancellation parked behind another entry's response. The originator's own J2 stimulus shows this: mask 0x18 at c; release slot 3 at c+1, while the mask still has slot 4; release slot 4 at c+2 (`receipts/probes/originator-j2-mask-replay.log`).
  - So with #163 a selected, parked probe is withdrawn at c+1. With the mask dropped or delayed it is first covered at c+2, after the pool may have started it.
  - The parked case can occur at the top. The originator's `cancel_valid_i` comes straight from the notify block, so a timer-driven TIME_LIMITED drain cancel (`n_st_r == N_DRAIN`) can land in the same clock as an unrelated response commit.
  - The two existing WD arms grade only that the mask is not combinational (`withdraw_unregistered`) and that the abort port is wired (`withdraw_abort_ignored`).
- **Impact.**
  - The element #163 introduces could be removed or retimed without any failing check, campaign arm or README count.
  - That would widen the window in which a superseded or drained CONTROLLER_AVAILABLE probe, parked behind another exchange's response, is still sent.
  - The new +1 boundary for that case is ungraded. The docs describe only the immediate case, which hides why the stage is not redundant with the release.
- **Required outcome.**
  - Add a top-level check, for example WD4 in section WD. It should put a superseded or drained probe's cancellation in the same clock as another inflight exchange's matched response, with that probe selected by the arbiter in that clock. It should grade that the selection is withdrawn in the next clock, before the pool starts it, and that the probe never reaches the wire.
  - Add two arms to `notify_mutants.py`: the mask removed from the three readers (release term only) and the mask delayed two clocks. Both must fail the new check, and the README records must say so.
  - State the parked case in the 03 row, the top's comment and the WD README text: for a parked cancellation the registered mask leads the release by one clock.
  - Alternatively, the author shows, with evidence, that no parked cancellation can coincide with the arbiter selecting its slot at the top, and documents why the stage is still kept.
- **Verification.**
  - Rerun `python3 scripts/reviewer_probes.py TREE OUT VERILATOR 3 r-wd-mask-dropped r-wd-two-clocks r-full-mask-dropped r-full-two-clocks`. All four must be KILLED, and `ctl-withdraw` must PASS.
  - The notify campaign must stay all-KILLED with goldens PASS.
  - `make check` must return rc 0.
- **History.** F1 has been present since round 1 (`cd9825c9`, same RTL and section WD). It was found by this round's reviewer plants. The merges did not introduce it.

**S1 (retained) - SUGGESTION - Tests, Docs.** This is R518-1 S1 and R519-1-S1. The round-3 packet adds `cone-summary-m3*` and `source-cones-m3.json`, but still does not publish the cone traversal script, the cell/pin inventory or the raw pair tables. The m3 final summary equals round 1's head summary except for its first-line threshold (`above -1: 17990` vs `above 0: 17989`) and the zero-level FSM pair now counted. Required outcome if adopted: as stated in round 1.

**S2 - SUGGESTION - Tests, Docs.** The final OOC measurement's input digest is not published.
- The round-3 packet publishes `inputs_sha256` only for the fresh new-main reference (`a331e67f...`), which differs from the parent's stored reference for processor `ead80360` (`b68c6d35...`).
- `rtl-scope-m3final.json` binds the arbiter and notify blobs to head, but not `protocol_processor_top.sv` (head blob `bf522a6f`), which carries the stage.
- The fresh flow differs from the stored one only in `general.maxThreads` 2 vs 32.
- Required outcome if adopted: publish the final record's `inputs_sha256` (or its resource-gate record) and the top blob.
- Verification: the gate's `inputs()` digest at `c4539ff1` reproduces the published value.

**S3 - SUGGESTION - Docs.**
- 09 §8.4 (`docs/architecture/09_verification.md:297-321`) lists DN and the IX/TS/TW/DR notification sections. It does not list WD, CX or `--withdraw-only`, and its "five of the notification block's" is now six. 09 §8 makes the suite READMEs the evidence home, so this is not a contract breach.
- `tb/aecp_notify/README.md:15` is a 146-character prose line that the merge left unwrapped.

### Prior public findings at this head
I read them after my independent diff pass. There are no submitted reviews and no inline review comments on #166. Issue #163 carries no findings.

| Prior finding | Status at `c4539ff1` |
|---|---|
| R518-1 S1 (SUGGESTION) | RETAINED as S1: script and raw tables still unpublished |
| R519-1-S1 (SUGGESTION) | RETAINED as S1: same artifact gap |

## 5. Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #163 acceptance and three assignments; Milan §5.3.4.2 / §5.4.5.3 paths; 03 Withdrawal row; unchanged ports and parameters vs new main; WD at one and two interfaces; arbiter equivalence cited from R518-1 | R518-2 (arbiter equivalence: R518-1) | c4539ff107a6a4c7d2e4a4844182b00a2bf33c82 |
| RTL | CLEAN | net RTL diff identical to round 1; single reader of the combinational mask; `g_ca_own`/`g_ca_turns` cancel and report paths; originator `{key, seq}` match; lint 41/41 | R518-2 (unchanged arbiter/stage logic: R518-1) | c4539ff107a6a4c7d2e4a4844182b00a2bf33c82 |
| Robustness | UNCLEAN (F1) | immediate vs parked cancellation; originator J2 per-clock mask/release probe; settle invariant; two-interface WD | R518-2 | c4539ff107a6a4c7d2e4a4844182b00a2bf33c82 |
| Tests | UNCLEAN (F1) | pp_top 10,468 (head and merge), aecp_notify 65, tx_arbiter 66, originator 107; notify campaign 89/89 + 11 goldens; plant audits at three revisions; check-literal preservation; 20 reviewer plants; fix-commit scanner and log identity | R518-2 | c4539ff107a6a4c7d2e4a4844182b00a2bf33c82 |
| Docs | UNCLEAN (F1) | five conflict resolutions; both suite READMEs and counts; 03 row; 09 §8.4/§8.9; PR body round-3 section; timing receipts vs claims; `make check` rc 0 | R518-2 | c4539ff107a6a4c7d2e4a4844182b00a2bf33c82 |

## 6. Real limits

- **Not run by me.** The full 33-suite processor bank, the other 13 campaigns, Yosys, the parent consumer set of 17 and any Vivado/OOC run. The timing result rests on the author's published receipts, which I checked for consistency and blob identity (S2). The suite totals I did not run (1,028,290 bank, 17/17 consumers) are author claims.
- **No manager receipts.** No public manager receipt for the "full source static/builder and native banks" at this head was found on #163, #166 or in milan-fpga up to `c4a23f5a`, so none was examined.
- **Evidence link.** The assigned evidence link `fc004672` contains only round-1 files. The round-3 packet was read at `c4a23f5a`.
- **Hosted CI at the exact head.** Runs [37582394027](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/37582394027) (pull_request) and 37582388080 (push): `docs-gates` and `portability` completed with success. `suites` was still in progress at the last inspection (`receipts/hosted-*`), and its "Build Verilator v5.050" step was skipped. No credit is given for running or skipped contexts.
- **F1 reachability.** Reachability at the top is argued from the RTL (drain cancel vs response commit) and the originator's own J2 stimulus. No top-level bench reproduces it today; producing one is F1's required outcome.

## 7. Pending manager duties

- Hosted and local workflow acceptance at the exact head, including the pending `suites` job.
- The manager's full source static/builder and native banks: publish receipts. They are source validation, distinct from the final current-dev candidate.
- The final current-dev candidate at the merge turn (source base `86a7b0c57831c15e9cd8b42d64cc4a9843f4e726`, live dev `09f1841bd2c6a9dea8eb1994d887f7386ca4f62d`), with donor and consumer banks.
- The parent three-directive sweep on the merged pin at +0.03 ns or better in each directive (acceptance item 3), at pin adoption.
- Physical calibration is NOT RUN. Field skips and software passes are not hardware proof.

## 8. Replay and integrity

Run from this packet. Set `V` to the pinned Verilator 5.050 and `T` to an exported tree of the head (`git archive c4539ff1`).
- `python3 scripts/plant_audit.py T OUT.json`
- `python3 T/tb/pp_top/notify_mutants.py --output DIR --verilator V --jobs 4`
- `python3 scripts/reviewer_probes.py T OUT V 3 [NAME ...]`
- `sh scripts/originator_j2_mask_probe.sh T WORK V LOG`
- `python3 scripts/function_length.py T...` (uses the parent scanner copied beside it)
- `python3 scripts/timing_receipt_audit.py REPO EVIDENCE_DIR`
- `python3 scripts/verify_state.py REPO HEAD TREE OUT`
- `scripts/bg.sh` and `scripts/wait.sh` ran the long jobs with per-job log, rc and resource files (`receipts/runs/`).

Path prefixes under the home directory are shown as `$HOME` in the receipts.

**Integrity.**
- The reviewed checkout is byte-exact at the head: 581 tracked entries by raw blob bytes and modes, index tree = HEAD tree = `4378652558345d65dd87efd4f092f41f413226c8`, status empty (`receipts/checkout-state-final.json`).
- This repository has no submodule gitlinks.
- Every probe ran in disposable trees under `scratch/`.
- No source fix, commit, push, merge, GitHub write, author contact or other-checkout edit was made, and no hardware was used.
- Unit memory peak: 9,826,365,440 bytes under the 12 GiB cap.

R518-2 FINISHED
