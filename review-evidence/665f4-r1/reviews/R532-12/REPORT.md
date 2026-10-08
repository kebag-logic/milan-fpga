[R532] NEGATIVE - exact head efea74858dffc482820d4f19c26c38796a57ff75

Round R532-12 is the internal independent review of issue #665, lane F4, PR #690. It covers the delta `b98eb2d5..efea7485`, tree `4e28d2409425b352c51d79526e4b48d6c93a38b7`. The delta has three parts:

- the `--no-ff` merge `d1fe17d1` of dev `99e4eb6c` (#682 processor pin `2ad2f845`, #691 GMII capture);
- the round-12 fix `959238f1` (SRP feedback observation without callback reentry);
- `7b47f333` (pinned contract citations) and `efea7485` (IF=1 plant selection).

**Inputs.** Assignment #665 comment 6050694779 (decision (a)), REVIEW READY 6051676441, and the author packet `review-evidence/665f4-r1/author-r12` at `30357b92`. Round-11 verdicts are the baseline.

**Lenses applied.** Conformance, RTL, Robustness, Tests and Docs.

## Summary

Both round-11 findings are resolved at this head.

- **R532-11-F1 is resolved.** The MSRP receive filter no longer enters its owning lwSRP application. It now derives the preceding event from copied Talker indication data. Registrar visits (`mrp_attr_visit`) run only outside library callbacks. The citations match the pinned `9197193e` contract text.
- **R532-11-F2 is resolved.** The three standing cases exist, and `p11-supersession-kind-stale`, `p11-reset-withdrawal-lost` and `p11-postwithdrawal-kind-overwrite` are caught by name at IF=1 and IF=2.

The other checks also hold:

- The dev merge equals the automatic merge, except for four documentation conflicts. Each was resolved by keeping both sides.
- Builder gate 23h and its five missing-patch controls pass.
- Coverage is 100 %.
- The plain and AddressSanitizer suites pass at IF=1/2.
- The four linked images reproduce the author's figures exactly.

One MINOR finding keeps the verdict NEGATIVE:

- **R532-12-F1 (MINOR; Tests).** The new copy logic handles each registration kind separately, and the Failed-kind half has no test that can fail. Three single-site plants on that logic each pass every standing suite at IF=1/2: Failed leave clearing the wrong bit, Failed indication setting the wrong bit, and clearing both kinds on any change. Two of them lose the intra-PDU withdrawal for a Failed Talker. Reviewer probe tests pass at the head and catch each plant at IF=1/2.

## 1. Reconstruction (public state only)

- **Workflow.** I read `AGENTS.md` sections 1 to 8, `CONTRIBUTING.md` (by reference from AGENTS for the review bar), and the issue #665 body: no RTL change; the default build and shipping image unchanged; portable C; a service-latency bound per path.
- **F4 contract and decisions on #665.**
  - 6030279477: the frozen F4 lane, Parts A to C.
  - 6048644347 and 6049530812: the round-10 and round-11 decisions, including kind-change option (a) and latched withdrawals.
  - 6050694779: the round-12 assignment, decision (a) for R532-11-F1 and the required F2 cases and plants.
  - 6051676441: REVIEW READY.
  - PR #690 6051700384: review start.
- **Authorities.** In the lwSRP pin `9197193e`, read from a scratch clone at the pin:
  - `doc/integrator.md:321-323`: "Transport callbacks, indications, observers, and filters must never synchronously reenter the owning application. Queue future work instead. The firmware adapter owns debug and release enforcement of this contract."
  - `src/include/shish_lan/mrp.h:288-290`: the filter "must not re-enter MRP".
  - `src/core/mrp_mad.c:617-689` (`reg_event`: indications per registrar transition, Milan rapid leave, refusal restores state).
  - `mrp_mad.c:990-1066` (`rx_on_attr`: the filter runs before each attribute; atomic replacement at `:1026-1050` is old rLv plus LeaveTimer, then the new Join).
  - `src/modules/msrp.c:45-97` (join and leave indication dispatch) and `msrp_attr_cmp` (StreamID identity, one attribute per type and StreamID).
- **Diff and history.** `git diff 99e4eb6c..efea7485` (59 lane files) and `d1fe17d1..efea7485` (8 files, +188/-16).
  - The four commits are one line each with no trailers.
  - Against dev `99e4eb6c`, the head changes no file under `hdl`, `sw/mailbox`, `syn`, `constraints`, `tb`, `sw/litex`, `sw/builder` or `configs`, and no gitlink (`receipts/merge-check.txt`).
- **Public evidence.** From the author packet at `30357b92` I read `ROUND12-GATES.md`, `ROUND12-REPRODUCE.md`, `ROUND12-COVERAGE.md`, `ROUND12-SIZE.md`, `BUILDER-RESULTS.json`, `ROUND12-REVIEW-INPUTS.json` and `ROUND12-REVIEW-RESULTS.json`, plus the live PR body. No private author material and no lane scratchpads were read.
- **Order of work.** Prior public findings were read only after my provisional verdict and ledger (`receipts/provisional-verdict.txt`; its time and sha256 are in `receipts/provisional-verdict.mtime.txt`).
  - My own R532-11 report was read after my independent pass over the diff.
  - R533-11 was read after the provisional verdict.

## 2. Delta review against the round-12 assignment

| Item (6050694779) | Result | Evidence at this head |
|---|---|---|
| R532-11-F1 (a): the filter makes no call into its owning application | **Met** | `srp_mbx.c:159-190`. `interested_msrp` reads only adapter state (`registered_kinds`, `desired`) and calls `capture()`. There is no lwSRP entry. `snapshot()`/`mrp_attr_visit` is called only from `tick` after `shlan_timer_tick` returns (`:43-56`), from `apply_receive` before and after `mrp_rx` (`:424-433`), and from `poll` (`:763`). None of these runs inside a library callback. The indication handlers `advertised`, `failed` and `left` (`:95-116`) only edit `registered_kinds` through `talker_changed` (`:81-93`). |
| Observe the preceding wire event from the data the filter is handed | **Met** | The copies come from the indications that `reg_event` issues on every registrar change between MT and registered. New/Join set a kind bit (with StreamID, destination and VID match, the same rule as `registrations()`, `:541-558`); Lv clears it. The filter recomputes `desired` with Failed precedence, as the visitor does. `srp_mbx.h:32` documents the bit meaning. |
| Intra-PDU Lv-then-New ordering kept; atomic kind replacement kept | **Met** (behavior) | Atomic replacement runs both halves inside one `rx_on_attr` (`mrp_mad.c:1026-1050`), so the next filter call sees a single continuous kind. `SinglePduKindReplacementsRemainContinuous` (`srp_feedback.hpp:85`, both directions, repeated) passes at IF=1/2. `SinglePduWithdrawalThenRegistrationRetainsTheFirstEvent` (`:74`) passes at IF=1/2. The Failed-kind variants also behave correctly: reviewer probe tests T1 and T3 pass at the head (section 4). Their test gap is F1. |
| Comment and `srp/README.md` cite `integrator.md:321-323` and `mrp.h:288-290` and state the compliance | **Met** | `srp_mbx.c:163-165`; `srp/README.md:71-82`. The links are pinned to `9197193e` and resolve to the quoted lines (checked at the pin). |
| `feedback-intrapdu-lost` (or its replacement) caught at IF=1/2; the two named cases pass | **Met** | The plant now removes `capture(s,previous)` from the filter (`srp_mutants.py:798`) and is caught by name at IF=1/2. `SinglePduWithdrawalThenRegistrationRetainsTheFirstEvent` passes in the full `test_acmp_mbx.cpp` run at IF=1/2. `R533WithdrawalBeforeReregistrationStillReprobes` belongs to the external reviewer's probe set; its standing equivalent is `WithdrawalThenRegistrationRetainsTheFirstEvent`, which passes and whose plant (`feedback-withdrawal-overwritten`) is caught by name. The author packet records the original probe passing (`ROUND12-REVIEW-RESULTS.json`); I did not re-execute that external probe. |
| R532-11-F2: standing cases through real mailbox input and the composition poll at IF=1/2 | **Met** | `IdenticalRebindAfterUndeliveredWithdrawalSettlesNoRsv` (`:184`), `LinkResetWithdrawsTheSettledRegistration` (`:204`, link down, and down/up with re-registration before delivery) and `LaterKindAfterWithdrawalIsNotReported` (`:226`) pass at IF=1/2. Each uses `mbx_model_rx` and BIND_RX ingress, the loop's delivery poll, and asserts the ACMP state. |
| p11 plants caught by name | **Met** | `srp_mutants.py:827-835` encodes my R532-11 plants at the same sites: the reseed in `ctrl_app_srp.c`, the reset `capture` in `reset_interface`, and `!s->withdrawn &&` in `capture`. All three are CAUGHT by name at IF=1 and IF=2 (`receipts/plants/`). `test_ctrl_firmware.py:199-207` adds `p11-` to the standing IF=1 selection. |
| README and PR-body claims | **Met** | `srp/README.md:258-266` and the PR body's "Round 12" section list exactly these cases. No guarantee is narrowed. |
| Merge dev `99e4eb6c --no-ff`, keeping both sides | **Met** | See section 3. |
| Builder gate 23h passes after the merge | **Met** | `receipts/gate23h.log`: the five patches, including `0007-liteeth-gmii-rx-capture`, reconstruct all four installed files byte for byte; 5/5 missing-patch fixtures are rejected. |
| Round-11 gates: coverage, ASan, images, bounds | **Met** (this reviewer's subset, section 5) | Coverage, ASan, images, bounds. |
| No mailbox, register-map or RTL change | **Met** | Protected-path diff against dev is empty; `gen_mailbox.py --check` rc 0. |

## 3. Merge result against both parents

Evidence: `receipts/merge-check.txt`.

- **Parents.** `d1fe17d1` has parents `b98eb2d5` (the lane) and `99e4eb6c` (dev).
- **Comparison with the automatic merge.** `git merge-tree` reports exactly four conflicted paths: `PNG_MANIFEST.json`, `submodule_boundaries.drawio`, `submodule_boundaries.png` and `SUBMODULES.md`. The recorded merge tree differs from the automatic merge in those four paths only.
- **The resolutions keep both sides:**
  - `SUBMODULES.md:25-26` carries dev's `protocol-processor` pin `2ad2f845` and the lane's `third_party/lwSRP` row.
  - The drawio holds dev's `pin 2ad2f845dd58` box and the lane's lwSRP box (page height 1100).
  - The PNG and its manifest are regenerated.
  - None of the three text files contains conflict markers.
- **Generator checks.** `submodule_boundaries.gen.py --check` reports "OK (5 exact gitlinks, decoded PNG)". `check_submodule_docs.py` reports "OK (5 exact gitlinks)".
- **F3 and F4 composition are intact by construction:**
  - `sw/firmware`, `sw/mailbox` and `hdl` are byte-identical between the lane parent and the merge.
  - Dev `d8b355fe..99e4eb6c` touches none of `sw/firmware`, `sw/mailbox` or `hdl/milan/mailbox`.
  - After the merge only the eight round-12 files change.
  - The four-module composition suite (49 tests, ADP, ACMP, MAAP and SRP) passes at IF=1/2.
- **Dev content is preserved.** Every protected path equals dev `99e4eb6c`, including `sw/litex` (#691 patch 0007, XDC and checks) and the processor gitlink `2ad2f845`.

## 4. Findings

### R532-12-F1 | MINOR | Tests | `sw/firmware/ctrl/srp/srp_mbx.c:87`, `:106`, `:114`; `sw/firmware/ctrl/test/srp_feedback.hpp:74-117`; `sw/firmware/ctrl/test/srp_mutants.py:798-835` | The Failed-kind half of the new copy observation has no discriminating test

- **Authority.**
  - AGENTS section 6 Tests lens: "Each new test can fail for the defect it claims to detect", and positive, negative and boundary behavior is covered.
  - Round-11 decision item 2 (6049530812): a withdrawal that happened is retained "even if a later receive in the same pass restores registration".
  - Round-12 item 1 (6050694779): the intra-PDU Lv-then-New ordering stays preserved.
  - `srp/README.md:80`: "Lv then New remains two transitions, even inside one PDU", stated for both kinds.
- **Evidence.**
  - Round 12 introduces per-kind bookkeeping:
    - `failed()` sets bit 0 (`srp_mbx.c:106`);
    - `left()` clears bit 0 for a Failed leave and bit 1 for an Advertise leave (`:114`);
    - `talker_changed` clears only the indicated kind before setting it (`:87`).
  - The standing intra-PDU and identity cases send Advertise frames only (`talker(k,false,…)` at `srp_feedback.hpp:74-117`). The two copy-loss plants (`feedback-advertise-copy-lost` and `feedback-failed-copy-lost`) disable the set path entirely. Nothing discriminates which bit a Failed indication or leave touches.
  - Single-site, compiling reviewer plants (`scripts/r12_probes.py`) were run through the whole `test_acmp_mbx.cpp` and `srp_mbx.cpp` suites at IF=1 and IF=2 (`receipts/probes/results.json`):

| Plant | Site | Standing suites, IF=1/2 | Reviewer probe test (`probe-tests/r12_failed_intrapdu.hpp`) | Failure mode the probe shows |
|---|---|---|---|---|
| q04 `leave-clears-advertise-only` | `:114`, Failed leave clears bit 1 | **survives** all four runs | T1 `R12FailedSinglePduWithdrawalThenRegistrationRetainsTheFirstEvent` and T3 `R12FailedReplacementWithdrawnInsideOnePduStillReprobes` pass at the head and **catch** it at IF=1/2 | A settled Failed Talker withdrawn and re-registered inside one PDU is never reprobed. The withdrawal is lost, which is the R533-10-F2 failure class for the Failed kind. |
| q13 `failed-indication-as-advertise` | `:106`, Failed join sets bit 1 | **survives** all four runs | T3 passes at the head and **catches** it at IF=1/2 | Advertise is replaced by Failed, then Failed leaves and Advertise returns, all inside one PDU. The withdrawal is lost and no reprobe follows. |
| q06 `change-clears-both-kinds` | `:87`, any change clears both bits | **survives** all four runs | T2 `R12BothKindsFailedLeaveInsideOnePduIsNotAWithdrawal` passes at the head and **catches** it at IF=1/2 | With both kinds registered, a Failed leave followed by an Advertise refresh in one PDU records a false withdrawal and reprobes a healthy listener. |

  - The head is correct: T1, T2 and T3 pass unmodified at IF=1/2 (`receipts/probe-tests/`). The plants are reproducible, and coverage is 100 % (`srp_mbx.c` 515/515 lines and 478/478 branches) because every line is executed. The kind values are simply asserted by nothing.
- **Impact.** The Failed half of the intra-PDU withdrawal guarantee, and the per-kind clear, can be removed or regressed with every gate, campaign and coverage check green. That is the guarantee that stops a listener from staying settled across a Failed Talker's withdrawal.
- **Required outcome.**
  - Standing cases through real mailbox ingress and the composition poll at IF=1/2 for:
    - Failed-kind Lv-then-New inside one PDU;
    - a replacement into Failed that is withdrawn inside the same PDU;
    - per-kind clearing while both kinds are registered.
  - A named plant equivalent to q04, q13 and q06, each caught by its named observable at IF=1/2.
  - No production change is required.
- **Verification.**
  - The three plants, or the author's equivalents, are caught by name at IF=1/2.
  - The reviewer probe tests still pass.
  - The coverage ratchet stays at 100 %.

### R532-12-S1 | SUGGESTION | RTL, Tests | `srp_mbx.c:30-41` (`enter`), `srp_mbx.c:572-585` (`snapshot`) | No enforcement detects a restored reentrant visit

`integrator.md:323` gives the firmware adapter "debug and release enforcement" of the no-reentry rule. Today the adapter's `enter()` guard protects only adapter entries.

Probe q10b (`scripts/r12_probe_q10.py`) restores `snapshot(i)` inside `interested_msrp`, which is the round-11 reentry. It passes the composition, adapter and debug-guard suites at IF=1/2 (`receipts/probe-q10/`).

A debug-only flag held across `mrp_rx`, `shlan_timer_tick` and `mrp_transmit`, and asserted in `snapshot()`, would turn that regression into a failing test. This is optional. The R532-11-F1 verification was by code reading, and that check is met.

### Observations (not findings)

- **q01, q11 and q12 are equivalent at this head.**
  - q01 (Advertise-first precedence in the filter): a withdrawal needs two events from a both-kinds state, so the filter that follows always sees a single kind, and the post-receive visit restores Failed precedence.
  - q11 and q12 (kinds not zeroed on reset or visit): lwSRP never drops a registration without a Lv indication, and destroy/bind zero the copies.
- **q02 (the pre-receive seed at `:424-427`) is defensive.** Removing it changes behavior only when a receive lands between an accepted bind and SRP's next poll. Both outcomes then end with the Talker registered. No finding.
- **q03, q05, q07, q08 and q09 are caught** by the composition suite at IF=1/2.
- **The first q10 encoding did not compile** (`-Werror=type-limits`). It is recorded as BUILD-REFUSED and replaced by q10b.

## 5. Executable evidence (this reviewer)

All runs used the pinned lwSRP `9197193e` from a separate scratch clone, which was verified clean at the pin. Host builds used GCC 16.2.1. The SDK was the CI-pinned RV32 SDK, installed offline after its digest check (`receipts/sdk-install.log`). At most 16 compile jobs ran at a time. The scoped HDL simulator was not needed: no HDL is in the delta.

| Work | Result | Receipt |
|---|---|---|
| SRP suites: adapter 53, receive recovery 17, `srp_app` 5, composition 49, latency 5, walk 5, debug guard 3 | PASS at IF=1 and IF=2 (14 arms) | `receipts/arms/` |
| The same under AddressSanitizer | PASS at IF=1 and IF=2 (14 arms) | `receipts/asan/` |
| Named `feedback-*`, `r10-*` and `p11-*` plants (25) | 25/25 caught by name at each count (50 catches) | `receipts/plants/results.json` |
| Reviewer probes q01 to q13 on the new copy code, whole suites | 5 caught (q03, q05, q07, q08, q09); q04, q06 and q13 survive (F1); q01, q02, q11 and q12 equivalent; q10 rewritten as q10b | `receipts/probes/` |
| Reviewer probe tests T1, T2 and T3 (head, then plants) | Pass at the head; catch q04 (T1, T3), q13 (T3) and q06 (T2) at IF=1/2 | `receipts/probe-tests/` |
| q10b, the reentrant visit restored | Survives the composition, adapter and debug suites at IF=1/2 (S1) | `receipts/probe-q10/` |
| `fw_coverage.py --check --jobs 4` | PASS; 22 files at 100 % after unchanged exclusions; `srp_mbx.c` 515/515, 478/478 | `receipts/coverage-check.log` |
| Bounds | Composition F6 prints bounds 3224 (IF=1) and 4073 (IF=2), equal to `MAILBOX_SPLIT.md` and the PR body | `receipts/arms/test_acmp_mbx-if{1,2}.log` |
| Linked images (`ctrl_srp_image.py`) | RAM span 80,368 / 93,024 (1x1, IF=1/2) and 95,168 / 122,672 (8x8), equal to the author's `ROUND12-SIZE.md`. F3 `ctrl_image`, `ctrl_image_selftest` and `fw_rv32_selftest` rc 0. | `receipts/images.log`, `receipts/images/` |
| Builder gate 23h and its control only (not the bank) | PASS: 5 patches, 4 files; 5/5 missing-patch fixtures rejected | `receipts/gate23h.log` |
| Docs and idiom gates: `docs_check`, `check_doc_style`, `check_doc_paths`, `check_em_dash --base 99e4eb6c`, `gen_toc --check`, `check_cpp_idiom`, `check_py_idiom`, `gen_mailbox --check`, `check_hygiene --check`, `check_baremetal_only --check`, `git diff --check` (both bases) | All rc 0 | `receipts/docs-checks.log` |
| Submodule diagram and docs after the merge | rc 0 | `receipts/docs-submodule-*.log` |
| Clone integrity after all probes | Worktree, index and HEAD tree identical (blob, mode, path); 0 status lines including ignored files; five gitlinks at their recorded pins; checked-out submodules clean | `receipts/clone-integrity.txt` |

The first image attempt refused because the candidate clone's `third_party/lwSRP` is not populated. It was rerun from a `git archive` export of the head with the pinned scratch clone linked in; that attempt is kept in scratch only. Earlier probe-test attempts refused for the same reason: an exported tree lacked the processor gitlink and the gPTP generator. Probe trees are disposable exports of the exact head.

## 6. Prior public findings at this head

| Finding | Status at `efea7485` |
|---|---|
| R532-11-F1 (MINOR; RTL, Docs): the filter re-enters lwSRP | **Resolved** (section 2, rows 1 to 5). |
| R532-11-F2 (MINOR; Tests, Docs): three guarantees without a discriminating check | **Resolved.** The three standing cases pass and the three p11 plants are caught by name at IF=1/2. |
| R532-11-S1 (SUGGESTION): name the per-event filter cost | **Taken.** `MAILBOX_SPLIT.md:735-738` names the per-AttributeEvent sink scan and the boundary registrar visits for target calibration. |
| R533-11 | POSITIVE with no finding or suggestion. Nothing to carry. |
| R532-8-F1, hosted half (carried) | **Still a manager duty.** The exact-head snapshot (`receipts/gh-check-runs-efea7485*.tsv`, `gh-workflow-runs-efea7485.tsv`) shows executed successes for `changes`, `elaborate`, `verilator-lint`, `wire-accountability`, `yosys-elaboration`, Yosys shards 0 to 3, Verilator shard 3/5, `bdd-conformance`, `docs-check-no-git` and `full-ci-gate`. Still in progress at the last query: `firmware-unit`, `docs-check`, and Verilator shards 0, 1, 2 and 4. `Physical gPTP` is skipped and is not counted. |
| Earlier rounds (R532-1 to R532-10, R533-1 to R533-10) | Retained as resolved per the round-11 baseline. This delta touches none of their sites, apart from the observation path re-reviewed above. |

## 7. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment 6050694779 items 1 to 3 against `srp_mbx.c:81-190,424-433,528-585,693-697`. `ctrl_app_srp.c:52-104`. Pinned lwSRP `integrator.md:321-323`, `mrp.h:288-290`, `mrp_mad.c:617-689,990-1066`, `msrp.c:45-97`. Named cases and p11 plants at IF=1/2 (`receipts/plants/`, `receipts/arms/`). Merge parents and conflict resolutions (`receipts/merge-check.txt`). | R532-12 | efea74858dffc482820d4f19c26c38796a57ff75 |
| RTL | CLEAN | Empty protected-path diff against dev `99e4eb6c` (`hdl`, `sw/mailbox`, `syn`, `constraints`, `tb`, `sw/litex`, `sw/builder`, `configs`, gitlinks). `gen_mailbox.py --check`. Interface contract: no lwSRP entry inside `interested_msrp` (`srp_mbx.c:159-190`); visitor call sites `:52,426,432,763`. Gate 23h. Linked RV32 images. S1 is optional. | R532-12 | efea74858dffc482820d4f19c26c38796a57ff75 |
| Robustness | CLEAN | Atomic replacement, Lv/New in one PDU, identity mismatch, link reset down and down/up, identical-identity rebind, retained receive retry (`srp_rx_retry` 17/17), AddressSanitizer at IF=1/2. Reviewer T1, T2 and T3 pass at the head. The q01, q02, q11 and q12 equivalence analysis is in section 4. | R532-12 | efea74858dffc482820d4f19c26c38796a57ff75 |
| Tests | **UNCLEAN** (R532-12-F1 open) | `srp_feedback.hpp:74-240`, `srp_mutants.py:786-848`, `test_ctrl_firmware.py:199-207`; 50 named catches; reviewer probes and probe tests (`receipts/probes/`, `receipts/probe-tests/`); coverage check | R532-12 | efea74858dffc482820d4f19c26c38796a57ff75 |
| Docs | CLEAN | `srp/README.md:71-82,258-266` (pinned links verified at `9197193e`), `srp_mbx.h:32-35`, `srp_mbx.c:79-80,163-165`, `MAILBOX_SPLIT.md:735-738`, merged `SUBMODULES.md:25-26` and diagram checks, live PR body "Round 12", docs and idiom gates rc 0 | R532-12 | efea74858dffc482820d4f19c26c38796a57ff75 |

## 8. Real limits

- **Delta review.** Earlier rounds' banks were not rerun. Out of scope: the full parent, processor, gPTP, Yosys and builder banks, the complete control-plant table (471 plants), saved-state campaigns, the compiler-absent audit, sanitizers with a second compiler family, act and Docker.
- **Builder.** Only gate 23h and its control ran. They used the shared LiteX environment, which was read only and mirrored into a temp directory.
- **Images.** The images are linked, not booted. Physical calibration was NOT RUN, and target CPU-cycle and whole-call-chain stack bounds remain unproved. A skipped field or physical context is not hardware proof.
- **Hosted contexts.** These are a snapshot of a run that was still in progress, recorded as evidence of state only.
- **Probe runs.** The q01 to q13 and q10b probes run whole suites and count any failure as a catch. The probe tests T1, T2 and T3 match their named observable.
- **External probe.** `R533WithdrawalBeforeReregistrationStillReprobes` (the external reviewer's probe) was not re-executed here. Its standing equivalent passes and its plant is caught.

## 9. Pending manager duties

- Carry R532-12-F1 to the executor. After the fix, re-review must cover Tests at the new head.
- Hosted acceptance at the exact head: `firmware-unit`, `docs-check`, and Verilator shards 0, 1, 2 and 4 were still in progress at the last query. Also the act local replica and the hosted half of R532-8-F1.
- Build and validate the final current-dev candidate at the merge turn: source base `99e4eb6c`, live dev `99e4eb6c` at assignment. Then post-merge containment.
- The full builder and compiler banks, including the compiler-absent instrument (the author records it as NOT RUN).
- Explicit maintainer merge authorization and the complete independent review bar.

R532-12 FINISHED
