[R532] NEGATIVE - exact head 50d492c12789e1d80bf11f547e7fe53e02b4bdb9

# R532-1: internal cleared-context review of PR #690 (issue #665, lane F4)

- **Subject:** PR #690 "Mark II F4: bare-metal SRP on lwSRP over the mailbox". Head `50d492c12789e1d80bf11f547e7fe53e02b4bdb9`, tree `89b2d8707c3638521d6669f850ae4f8d6c1a666b`.
- **Parent delta:** `db9aa8c9b135b34ff3d070a979dee70440b37cc6..50d492c1` (two commits).
- **lwSRP gitlink:** `ef8a28b9f991ad2f6a466b377c25c2f7bcb310da`, 20 commits on lwSRP `19f5796` (`receipts/lwsrp_stack.txt`).
- **Role:** internal reviewer [R532]. Executor [A560]; external reviewer [R533].
- **Context reconstructed from:** AGENTS.md and CONTRIBUTING.md; the #665 body; owner directives 5992455815, 6008744385 and 6009661573; assignment 6030279477; acceptance addition 6030870481; the #608 rulings 5885808887 and 5886425487; IEEE 802.1Q-2018 clauses 10.7, 10.8 and 35.2; Milan v1.2 4.2.7, 4.3 and 5.5.2.7; `sw/mailbox/mailbox.yaml`; the diff; and the public evidence archive `fa19435a` at `review-evidence/665f4-r1`.

## Verdict

**NEGATIVE.** The firmware does not implement Milan v1.2 4.2.7.2.2.

- **The rule:** for MSRP, an IN registrar receiving rLv! moves to MT immediately, with no LeaveTime.
- **What the firmware does:** it waits the full 5 s LeaveTime instead. A talker keeps its licence, and keeps streaming, for 5000 ms after its last Listener explicitly withdraws.
- **Why it matters:** #608 was opened for exactly this symptom. Its public ruling sets the bar at "within one PDU period of a withdrawal that reaches an IN registrar".
- **How it is presented:** the PR documents and tests the behaviour as a normative difference with the processor (D1), citing only IEEE 802.1Q Table 10-4. The processor stimulus it reuses names the Milan rule.

The assigned #608 LV case itself is correct: a withdrawal meeting an LV registrar after a LeaveAll stops the talker at the original deadline. The rest of the F4 delivery is substantially sound, and it reproduces:

- the gate and the coverage ratchet;
- both mutation campaigns of the PR (43 of 43 and 97 of 97);
- RV32 freestanding builds at all ten shapes;
- lwSRP's own suites at the pin.

I also planted 25 defects of my own: 19 are caught and 6 survive. Five of the survivors are recorded under F2; A10 is an equivalent mutant.

## Findings

### F1 - BLOCKER - Conformance, RTL, Tests, Docs - Milan v1.2 4.2.7.2.2 (IN / rLv! -> Lv -> MT) is not implemented, and D1 presents the omission as 802.1Q-correct

**Where:**
- `third_party/lwSRP/src/core/mrp_mad.c:354-356`: the registrar rLv! row, IN column, is "start leavetimer, LV" for every application, MSRP included. lwSRP has no Milan override.
- `sw/firmware/ctrl/srp/srp_mbx.c:155-175` (`open_interface`, `mrp_port_configure` at :164): configures MSRP with LeaveTime 500 cs and nothing that selects the Milan transition.
- `sw/firmware/ctrl/srp/README.md:142,145`: D1 row and "IEEE 802.1Q is the oracle for both differences".
- `sw/firmware/ctrl/test/srp_walk.cpp:47-51`: asserts the Listener stays Ready 4990 ms after a Talker Lv from IN.
- The same D1 statement appears in the PR body ("delayed Lv deregistration under Table 10-4").

**Authority:**
- **Milan v1.2 4.2.7.2.2 ("Instantaneous transition from IN to MT"):** "For the MSRP application, the following transition of the MRP Registrar state machine [802.1Q, Table 10-4]: IN / rLv! -> (Start leavetimer) -> LV shall be changed by the following one: IN / rLv! -> (Lv) -> MT". Its note gives the reason: a 5 s LeaveTime can be used "without requiring 5 seconds to detect that a Stream has been explicitly withdrawn".
- **This repository's records:**
  - `docs/reference/MILAN_COMPLIANCE_MATRIX.md:97` records 4.2.7.2.2 as implemented by the SRP engine.
  - #608 ruling 5885808887 (corrected by 5886425487) sets acceptance as "within one PDU period of a withdrawal that reaches an IN registrar". 99 of 99 such withdrawals met it on the fabric.
  - The processor bench `protocol-processor/tb/srp_stream_fsms/sim_main.cpp:7,559-563,716-719`, the stimulus the differential reuses, labels the immediate MT "Milan Δ13".
- **Why 802.1Q is not the right oracle here:** it is the right oracle only where Milan is silent. Here Milan, the product's requirement, replaces that table cell.

**Evidence (my probe):**
- `probes/probe_r532.cpp` runs on the PR's own `Srp` fixture, driven by `probes/probe_run.py`.
- Listener Ready rJoinIn, then rLv! from IN with no LeaveAll: the talker licence is revoked **5000 ms** later.
- Talker Advertise rJoinIn on a bound sink, then rLv! from IN: the Listener declaration is withdrawn **5000 ms** later.
- Both results hold at one and at two interfaces: `receipts/probe_milan_4.2.7.2.2_if1.log`, `receipts/probe_milan_4.2.7.2.2_if2.log`.

**Impact:**
- **Every ordinary disconnect regresses to the #608 symptom.** A talker whose last Listener explicitly withdraws keeps transmitting for 5 s, holding bandwidth on the link, instead of stopping within one PDU period. A Listener keeps declaring Ready for 5 s after its Talker withdraws.
- **Milan conformance:** it fails, and the shipped Milan compliance claim would no longer hold once SRP is placed on the core.
- **Misleading evidence:** the selected differential labels a Milan-required behaviour as a processor defect. A later reader would "fix" the fabric in the wrong direction.

**Required outcome:**
- For the MSRP application only, IN / rLv! issues the Lv indication and moves to MT with no leavetimer. This can be an upstream lwSRP application option enabled by the adapter, or an equivalent.
- MVRP keeps Table 10-4.
- LV / rLv! keeps the 802.1Q behaviour, so the #608 LV case still stops at the original deadline.
- D1 is removed or rewritten to cite Milan 4.2.7.2.2. `srp_walk.cpp` asserts immediate deregistration for the section E stimulus.
- Tests cover both sides, Talker licence stop and Listener withdrawal, at one and two interfaces. The stop bound follows the #608 ruling, one PDU period, or at minimum T_svc on the host model.
- A planted defect restoring the leavetimer path is caught by name.
- The README and PR body cite the Milan clause.

**Verification:**
- `probes/probe_r532.cpp` (or the author's equivalent) passes at one and two interfaces.
- `Srp.LeaveAfterLeaveAllStopsAtOriginalFiveSecondDeadline`, `SrpWalk.RunBLeaveAllLanesPreserveTheRedeclaredListener` and `SrpLatency.OriginalLeaveDeadlineSurvivesCoalescedBacklog` still pass.
- The new planted defect is caught.
- lwSRP's own suites pass with the option tested upstream.

### F2 - MINOR - Tests - Three claimed behaviours survive planted defects in every suite

All three were run through the PR's own `arm_srp` at two interfaces against `srp_mbx.cpp`, `srp_latency.cpp` and `srp_walk.cpp`, and through lwSRP's cgreen suite where applicable (`receipts/r532_mutants.log`, `receipts/lwsrp_unit_*.log`).

1. **The admission boundary is untested.** `sw/firmware/ctrl/srp/README.md:66` claims "Admission charges Ethernet overhead and a 75% link-rate ceiling". `srp_mbx.c:93-99` implements it. Three defects survive:
   - A01: the tag-inclusive overhead `+ 22u` becomes `+ 18u`.
   - A11: the ceiling `* 3u / 4u` becomes `* 9u / 10u`.
   - A12: the preamble and IFG `(size + 20u)` becomes `(size + 0u)`.

   The only admission test, `sw/firmware/ctrl/test/srp_mbx.cpp:314` `AdmissionUsesBandwidthAndEthernetMinimum`, refuses a 5.6 Mb/s stream on a 1 Mb/s link, more than seven times over the ceiling. Nothing tests the admitted side next to the boundary, or the refused side just past it.
2. **The ReadyFailed callback path is untested** (A09).
   - **The defect:** removing `MSRP_LISTENER_DECL_READY_FAILED` from the `listener()` callback (`srp_mbx.c:58-59`) survives.
   - **What it would break:** under that defect, a Ready to ReadyFailed change on an active output owes a stop and gives a licence false/true blip. The README says a same-pass registration "cannot erase the owed stop notification", so this transition must not owe one.
   - **The gap:** no test drives Ready to ReadyFailed while the output is active.
3. **lwSRP's Table 10-3 note 4/5 handling is untested** (L11).
   - **The code:** stack commit `3365195` added it at `third_party/lwSRP/src/core/mrp_mad.c:493-497`: ignore rJoinIn! in VO/VP when point-to-point, and rIn! when not.
   - **The defect:** disabling it survives lwSRP's 1914 cgreen assertions and every parent suite.

**Equivalent mutant (not a finding):** A10 (`link &&` dropped from the licence predicate) also survives. Link loss recreates the participants, so `registered` already clears; it is recorded only for completeness.

**Impact:** a regression in the admission arithmetic or the ceiling would ship unnoticed. The bridge would then see Talker Advertise declarations the end station cannot honour, or Failed declarations it could. The other two gaps leave a licence glitch and a clause-cited applicant rule unguarded.

**Required outcome:**
- Boundary tests on both sides of the 75 % ceiling that discriminate each overhead term.
- An active Ready to ReadyFailed transition test with a strict licence mock.
- An upstream lwSRP test for note 4 (and note 5) that fails when the guard is removed.

**Verification:** re-run `probes/r532_mutants.py` (A01, A09, A11, A12) and `probes/r532_lwsrp_unit.sh` for L11. Each must be caught by a named test.

### Suggestions (non-blocking)

- **S1:** the LeaveAll-scope fix (`9a231ff`, `mrp_mad.c:914-922`) has no upstream regression test. Widening the received LeaveAll to all types survives lwSRP's suites. Only the parent `SrpWalk.RunBLeaveAllLanesPreserveTheRedeclaredListener` catches it (`receipts/lwsrp_unit_L05-leaveall-all-types.log`, `receipts/r532_mutants_L05_rerun.log`). Add the cgreen case upstream with the fix.
- **S2:** lwSRP's base table (`mrp_mad.c:346`, present since its first commit, not in this stack) issues a Join indication on LV / rJoinIn!. 802.1Q Table 10-4 lists only "Stop leavetimer, IN". The adapter is unaffected: `domain()` compares values, and the Listener state is recomputed every poll. An upstream issue is worth filing for bridge use.
- **S3:** `poll()` calls `mrp_reclaim`/`mrp_transmit` on `i->msrp`/`i->mvrp` without a null check (`srp_mbx.c:539-542`). A failed recreate at link reset (`srp_mbx.c:504`) would crash instead of being refused and counted. I judge it unreachable under the documented single-pool contract, since the released blocks dominate the startup demand. A defensive guard would make the failure mode a refusal.

### Residue (wording only)

- **R1:** `sw/firmware/ctrl/srp/README.md:45` reads "The fabric's millisecond events feed the loop's accumulated centiseconds". The fabric posts TICK events that carry centisecond counts (`sw/mailbox/mailbox.yaml:54,106-116,403-412`). Exact fix: "The fabric's TICK events carry the elapsed centiseconds into the loop's accumulated count;".
- **R2:** the PR body's "Known limitations" omits acceptance addition 6030870481, the linked RV32 `ctrl_app` image report. Exact fix: add "The linked composed `ctrl_app` image report (6030870481) is owed with the F3 composition; this head reports SRP object totals (at most 33,253 text, 140 data, 178 BSS bytes) and the entity-sized arena (at most 48,064 bytes at `ax7101_8x8`, two interfaces)."

## Prior public review findings

When this review started, PR #690 had no review, no review comment and no finding. Its only comments were the two start notices (6032180690, 6032181336). I found nothing to resolve or retain. The concurrent external round R533-1 was not read.

## What was checked, by lens

### Conformance (IEEE 802.1Q-2018 and Milan v1.2, judged directly)

**Applicant and Registrar tables.** I compared `mrp_mad.c:150-397` cell by cell with Table 10-3 and Table 10-4. All cells match, including:
- note 8: AN, tx! goes to QA only when the Registrar is IN (`mrp_mad.c:499`);
- notes 4 and 5 (`:493-497`).

The exceptions are F1 (the Milan override) and S2.

**LeaveAll.**
- The LeaveAll machine is per application; the received rLA! is scoped per attribute type (`mrp_mad.c:914-922`, 10.7.5.20 b).
- sLA raises rLA! locally only on commit (`:1275`, 10.7.6.6).
- The transmitted LeaveAll covers every MSRP type 1 to 4 (`:1189`, the 10.7.5.20 NOTE).
- A received LeaveAll restarts the timer (Table 10-5, the #608 correction).
- The draw is strictly between 1000 and 1500 cs (`:652`, 10.7.4.3; Milan Table 4.3).

**MSRP wire.**
- DA `01-80-C2-00-00-0E` and EtherType `0x22EA` (`msrp.c:403`, 35.2.2.1/2). Planted L02 is caught by 12 tests.
- Attribute lengths 25, 34, 8 and 4 (Table 35-2).
- FourPacked values (Table 35-3), with Ignore skipped on receive (35.2.2.7.2 a). Planted L07 is caught upstream.
- Talker increments of UniqueID and DA (35.2.2.8). Planted L03 is caught upstream.
- Domain increments SRclassID and SRclassPriority (35.2.2.9). It starts as `{6,3,2}` and is adopted from a class-A peer and reset on MAC_Operational, per 35.2.2.9.3/4 and Milan 4.2.7.2.1.
- EndMark `0x0000` on transmit (Milan 4.2.7.1.3). Planted L12 is caught.
- Whole-PDU discard of malformed input is permitted by Milan 4.2.7.1.2.

**MVRP.** VID 2 is declared at startup, with DA `01-80-C2-00-00-21` and `0x88F5`. A licence is granted only after the MVRP Join is committed (Milan 4.3.2).

**Talker and Listener declarations.**
- Talkers declare Advertise or Failed from startup (Milan 5.5.2.7). Bandwidth gives Failed code 1; an unallocated output gives code 2.
- Listener Ready or AskingFailed follows a matching registered Talker.
- Timers are JoinTime 20 cs, LeaveTime 500 cs and periodic 100 cs (Milan Table 4.3).

**The #608 LV case:** correct. The stop comes at the original 5000 ms deadline, and an rLv! in LV does not restart it (`Srp.LeaveAfterLeaveAllStopsAtOriginalFiveSecondDeadline`). Planted L06 is caught by three suites.

### RTL and architecture

**No RTL, register-map, config or testbench change.** `receipts/rtl_regmap_config_paths_touched.txt` lists 0 such paths, and `receipts/diff_name_status.txt` lists the full delta. The default all-fabric build and the shipping image are untouched.

**Loop contract.** `ctrl_loop.c:28-33,125-127` adds an optional per-channel `ready` gate. Existing users are zero-initialised and unaffected, and `srp_mbx_destroy` clears it.
- **No deadlock:** IRQ_STATUS.EVT is a level (`mailbox.yaml:75-85`).
- **Frame size:** 1514 equals the channel's `max_frame_bytes` and fits the 512-word TX ring.
- **Rebuild safety:** `fw_gtest` recompiles C on every build and keys C++ objects by content, so the shared work directory in `ctrl_mutants.py:440` cannot reuse a stale object.

**Ordering.** One owed frame is global across interfaces. RX and new declarations wait behind it, registrar clocks keep running, and link loss cancels only that interface's frame. `Srp.RefusedMailboxRetainsOwedFrameAndDefersInput` and `LinkLossCancelsItsOwedFrameOnly` cover this, and planted P01 and L10 are caught.

**RV32.** Freestanding RV32I/ILP32 objects build at all five shapes and both interface counts (`receipts/ctrl_gate.log`). The largest totals are 33,253 text, 140 data and 178 BSS bytes, plus at most 48,064 bytes of arena.

The lens is UNCLEAN only through F1's missing registrar transition, a broken architecture contract against `MILAN_COMPLIANCE_MATRIX.md:97`.

### Robustness

| Area | Evidence |
|---|---|
| Malformed and truncated input | The whole PDU is validated before any event (`mrp_pdu.c:105-215`). Planted L01 (ThreePacked 216 accepted) is caught by 2 tests. |
| Address and EtherType | Planted A04 (MSRP DA unchecked) is caught. |
| VID boundaries | 4095 in the domain filter and in binding: A05 and A06 are caught. |
| Reset during activity | Link reset recreates per interface (`InterfaceStateDoesNotCross`, `ExhaustedPoolStillReusesOwnedBlocksOnLinkReset`). |
| Exhaustion | Counted and refused at every startup stage, on domain change, and for sink Listener and VLAN declarations (5 tests). |
| Reentry | Refused and counted; asserted in debug builds (3 debug-arm tests). |
| Backpressure | The owed frame survives 11 ms and fails the budget predicate as designed. |
| Duplicates and idempotence | Duplicate and invalid bindings and duplicate Domain declarations are covered. |
| Reclaim | Planted L09 (an LV registration reclaimed) is caught by 5 tests. |

No defect found.

### Tests

- **Gate:** `test_ctrl_firmware.py --require-rv32 --jobs 4` returns 0: 36 arms, 0 skipped (`receipts/ctrl_gate.log`).
- **Coverage:** `fw_coverage.py --check --jobs 4` returns 0. `srp_mbx.c` is at 359/359 lines and 342/342 branches. The ratchet diff only adds `srp_mbx.c` and raises `ctrl_loop.c`, and `sw/firmware/gtest/README.md` (the exclusion list) is unchanged, so no exclusion is new (`receipts/coverage_check.log`).
- **The PR's campaigns, replicated in parallel with the PR's own plant and `caught()`:**
  - SRP: 43 of 43 caught (`receipts/pr_srp_campaign.log`).
  - Control: 97 of 97 caught (`receipts/pr_ctrl_campaign.log`).
  - RV32 self-test: 17 of 17 (`receipts/rv32_selftest.log`).
- **lwSRP at the pin:** cgreen gives 1914 passes and 0 failures (`receipts/lwsrp_unit_CONTROL.log`); behave passes 3 scenarios and 10 steps (`receipts/lwsrp_behave_CONTROL.log`).
- **My own planted defects:** 25 across the adapter, the loop and the lwSRP fixes (`probes/r532_mutants.py`, `probes/r532_lwsrp_unit.sh`).
  - Caught: 19 of 25. 17 fall to the parent suites: A02-A08, P01, L01, L02, L04, L05, L06, L08, L09, L10 and L12. L05 is the corrected plant, see `receipts/r532_mutants_L05_rerun.log`. The other 2, L03 and L07, fall only to lwSRP's own suite.
  - Survived: 6. A01, A09, A11, A12 and L11 are recorded in F2. A10 is the equivalent mutant.
- **Differential:** `srp_reuse.py` checks the processor blobs against the gitlink. It is not honest about D1 (F1): the stimulus's own source names Milan Δ13. D2 is correct under 35.2.2.7.2 a.

The lens is UNCLEAN through F1 and F2.

### Docs

- **Gates:** `docs_check`, `check_doc_paths`, `gen_toc --check` (pinned Markdown venv), `ci_events --check` and `--selftest`, `check_cpp_idiom`, `check_py_idiom`, `check_hygiene --check`, `lint_rtl --check` and `gen_mailbox --check` all return 0 (`receipts/*.rc`).
- **Readmes and CI page:** the SRP README, the ctrl README and the `CI_WORKFLOWS.md` change describe the shipped contract. The exceptions are F1 (the D1 row and its oracle sentence; the PR-body D1) and residues R1/R2.
- **Upstream licensing:** every source, header, build and test file in lwSRP carries Apache-2.0 SPDX, and LICENSE, NOTICE and a README section are present. That is lwSRP Part A, reviewed upstream.

The lens is UNCLEAN through F1.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | `third_party/lwSRP/src/core/mrp_mad.c` (Tables 10-3/10-4/10-5, transmit, receive), `mrp_pdu.c`, `msrp.c`, `mvrp.c`; `sw/firmware/ctrl/srp/srp_mbx.c`; 802.1Q-2018 10.7, 10.8, 35.2; Milan v1.2 4.2.7, 4.3, 5.5.2.7; `probes/probe_r532.cpp` | R532-1 | `50d492c12789e1d80bf11f547e7fe53e02b4bdb9` |
| RTL | UNCLEAN (F1) | `receipts/diff_name_status.txt`; `ctrl_loop.c/.h`; `srp_mbx.c` FSM and owed path; `mailbox.yaml` IRQ, TICK and srp channel; RV32 arms in `receipts/ctrl_gate.log`; `MILAN_COMPLIANCE_MATRIX.md:97` | R532-1 | `50d492c12789e1d80bf11f547e7fe53e02b4bdb9` |
| Robustness | CLEAN | `srp_mbx.c` receive, bind, poll and destroy; `mrp_pdu.c:105-215`; `srp_mbx.cpp` malformed, exhaustion, reset and reentry tests; planted A04-A06, L01, L09, L10, P01 in `receipts/r532_mutants.log` | R532-1 | `50d492c12789e1d80bf11f547e7fe53e02b4bdb9` |
| Tests | UNCLEAN (F1, F2) | `srp_mbx.cpp`, `srp_latency.cpp`, `srp_walk.cpp`, `srp_debug.cpp`, `srp_shape.cpp`, `srp_mutants.py`, `ctrl_mutants.py`, `coverage.ratchet`; `receipts/ctrl_gate.log`, `coverage_check.log`, `pr_srp_campaign.log`, `pr_ctrl_campaign.log`, `r532_mutants.log`, `lwsrp_unit_*.log`, `lwsrp_behave_CONTROL.log` | R532-1 | `50d492c12789e1d80bf11f547e7fe53e02b4bdb9` |
| Docs | UNCLEAN (F1) | `sw/firmware/ctrl/srp/README.md`, `sw/firmware/ctrl/README.md`, `docs/testing/CI_WORKFLOWS.md`, PR #690 body, lwSRP LICENSE/NOTICE/SPDX; docs-gate receipts | R532-1 | `50d492c12789e1d80bf11f547e7fe53e02b4bdb9` |

Robustness is banked clean at this head. Any later commit touching `srp_mbx.c`, `ctrl_loop.c` or the lwSRP pin un-covers it.

## Real limits

**No hosted evidence exists at this head.** No check run or status is recorded for `50d492c1`; the PR conflicts with dev, so there is no merge ref. Only my local runs stand behind the results.

**Not run by me:**
- the builder bank;
- `make -C tb/verilator/mbx`. The diff touches no RTL, and the manager's banks cover both.
- `test_ctrl_nvm.py`;
- the lwSRP pin-refusal arms of `ctrl_mutants.lwsrp_pin_arms`, which would plant into the submodule checkout;
- per-branch lwSRP topic heads. Only the final pin ran.

**lwSRP cgreen** was built against a private cgreen build (upstream HEAD `a249b395`) in disposable scratch. The packet supplies no cgreen pin.

**The latency evidence is the PR's desk envelope.** It assumes 100 ns per access and a 1 ms CPU allowance. It is not a target measurement; physical calibration was not run.

**My planted defects are a sample.** The A, P and L sets are not an exhaustive mutation.

**The clone was restored to the exact head after the probes.** HEAD and tree match, the worktree and index are clean, and no ignored files remain (the build caches the gates created were removed). The gitlinks are `third_party/lwSRP` `ef8a28b9`, `protocol-processor` `ead80360` and `gptp-processor` `5dce647a`, each with a clean checkout.

## Pending manager duties

1. Carry F1 and F2 to the executor. F1 needs an upstream lwSRP change, so the pin moves.
2. Carry R1 and R2 to the residue checklist.
3. At the merge turn: the dev merge, candidate-merge validation, hosted `rtl-fast` and long gates at the exact head, and lwSRP publication and fetchability.
4. The linked `ctrl_app` image report (6030870481), with the F3 composition.
5. The `ctrl_app` binding wiring to F3.
6. Re-run #608 bench cycles if the firmware placement is ever exercised on hardware.

R532-1 FINISHED
