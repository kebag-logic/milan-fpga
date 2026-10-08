[R532] POSITIVE - exact head 154722e14781c7373f3229420b6e007f9bcf9835

Round R532-13 is the internal independent review of issue #665, lane F4, PR #690. It covers the delta `efea7485..154722e1`, tree `1928df9c4d94eadc68e864b219a68270227e9f41`, against source base and live dev `99e4eb6c14462aafa84bb1ac597fd241abc1a240`. The round-12 verdicts at `efea7485` are the baseline.

All five lenses (Conformance, RTL, Robustness, Tests, Docs) were applied at this head and are CLEAN. No BLOCKER, MAJOR, MINOR or RESIDUE is open. R532-12-F1 and R533-12-R1 are resolved. R532-12-S1 stays an optional SUGGESTION.

## 1. Reconstruction

- **Contract.**
  - AGENTS.md sections 3 to 8 and CONTRIBUTING.md.
  - Issue #665 body.
  - The F4 lane, 6030279477: Parts A to C, including the 100 % ratchet, a named plant per check, and IF=1/2.
  - Acceptance additions 6009661573 and 6030870481.
  - The round-13 assignment, 6051940062: items 1 to 3, tests only, with no production change unless a test proves one is needed.
  - REVIEW READY 6052380945 and the review start, 6052396702.
- **Authorities.**
  - Pinned lwSRP `9197193e`, fetched into scratch: `doc/integrator.md:321-323`, `src/include/shish_lan/mrp.h:284-290`.
  - `src/core/mrp_mad.c:622-681`. Under Milan v1.2 4.2.7.2.2 rapid leave, IN/rLv issues Lv and enters MT immediately. So Lv then New inside one PDU really is two registration transitions, as `srp/README.md:80,185` states.
- **Delta (`git diff efea7485..154722e1`, `receipts/scope.log`).** Three files change:
  - `sw/firmware/ctrl/test/srp_feedback.hpp`: +55 lines, three `TEST_F` cases at `:87`, `:104` and `:122`.
  - `sw/firmware/ctrl/test/srp_mutants.py`: +13 lines, three `Defect` entries at `:802-814`.
  - `docs/design/MAILBOX_SPLIT.md:295`: one hash changes, `19f5796b...` to `9197193e47a6bb1c45a56d90a18c1784123aba44`.
  - Nothing else changes. There is no firmware source, RTL, register, configuration or workflow change, and all five gitlinks are identical at `efea7485` and at the head.
- **Public evidence read.**
  - The author's round-13 packet at evidence commit `ef69cd57` (`author-r13/ROUND13-*.md|json`, `round13-helpers/*`).
  - The live PR body, section "Round 13".
  - The R532-12 (6051937140) and R533-12 (6051926602) reports, read after the independent pass.
  - The original R532-12 probe header, fetched from evidence commit `83b76bfd` (`reviews/R532-12/probe-tests/r12_failed_intrapdu.hpp`) into `inputs/`. It is byte-identical (sha256 `7fa2d66d…`) to the author's copy.

## 2. Independent pass over the delta

### The three standing cases

All three go through real mailbox ingress, `mbx_model_rx` on `acfg.sink_interface[k]`, and the composition poll `settle()`. Each runs for both sinks and at both interface counts.

- **Frame construction (`srp_binding.hpp:49-63`).**
  - Each case removes the 2-byte PDU EndMark and appends the next message from offset 15, after the Ethernet header and ProtocolVersion.
  - The event is the first 3-packed event (`event*36`): New=0, JoinIn=1, Lv=5.
  - The result is a valid multi-message MSRPDU. Each case asserts `srp_adapter.received` advanced by exactly 1, so it is one PDU and not several.
- **`FailedSinglePduWithdrawalThenRegistrationRetainsTheFirstEvent` (`:87`).**
  - Precondition: a settled Failed Talker (`ASSERT_TRUE tk_failed`).
  - PDU: Failed Lv, then Failed New.
  - Trace through `srp_mbx.c`: `left()` (`:114`) clears bit 0. The next filter call (`:166-171`) sees `desired` 1→0 and latches `withdrawn` in `capture()` (`:562-570`). New sets bit 0 again (`:106`), and the post-receive `snapshot()` (`:572-585`) cannot clear the latch.
  - Required observable: `reprobed()` (`:28-32`), meaning PRB_W_AVAIL, binding retired, and `impossible==0`.
- **`FailedReplacementWithdrawnInsideOnePduStillReprobes` (`:104`).**
  - Precondition: Advertise settled.
  - PDU: Failed JoinIn (an atomic replacement, continuous), Failed Lv, Advertise JoinIn.
  - The Failed Lv empties the copies before Advertise returns, so the withdrawal is latched.
  - Required observable: `reprobed()`.
- **`BothKindsFailedLeaveInsideOnePduIsNotAWithdrawal` (`:122`).**
  - Precondition, asserted: both kinds registered (`registered_kinds==3`, `tk_failed`).
  - PDU: Failed Lv, then Advertise JoinIn. Bit 1 stays set throughout, so there is no withdrawal.
  - Required observables: SETTLED_RSV_OK, still bound, and `current_kind(k,false)` (`:6-24`). That last check reads the GET_RX_STATE response's REGISTERING_FAILED flag on the wire and requires `impossible==0` and no reentries.

### The three plants

Each plant is a single-site change at the exact sites R532-12-F1 named, and each names its test and behavioural needle:

- **`feedback-leave-clears-advertise-only`** (q04). Site `:114`. Test `:87`. Needle "retained withdrawal reprobes".
- **`feedback-failed-indication-as-advertise`** (q13). Site `:106`. Test `:104`. Needle "retained withdrawal reprobes".
- **`feedback-change-clears-both-kinds`** (q06). Site `:87`. Test `:122`. Needle "continuous Advertise is not withdrawn".

All three carry the `feedback-` prefix, so they are in the IF=1 selection at `test_ctrl_firmware.py:202` as well as the full IF=2 table.

### R532-12-S1 (judged only as a suggestion)

- The adapter's `enter()` busy guard (`srp_mbx.c:30-41`) is debug-asserted and release-counted. It is exercised by `srp_debug.cpp` (bind, receive and tick from an output), and that covers the externally reachable reentries.
- The production observation path makes no library entry from a callback. `interested_msrp` (`srp_mbx.c:159-190`) touches only adapter copies, and registrar visits run at `:52`, `:426`, `:432` and `:763`, outside callbacks.
- The missing internal-visit flag is therefore a hardening against a future code regression, not a present contract breach or a reachable defect.
- The tests-only assignment made it optional. Its absence is acceptable as a SUGGESTION.

## 3. Executed evidence (this round, exact head)

Runs used the pinned lwSRP clone at `9197193e` in scratch and the host compiler (GCC 16.2.1). The suite ran without `--require-rv32`. The ctrl RV32I freestanding arm ran with a host cross compiler and passed, but the SRP RV32 shape arms (`--require-rv32` with the pinned SDK) were not run. Every receipt below is listed in `MANIFEST.sha256`.

| Run | Result | Receipt |
|---|---|---|
| Complete ctrl suite, `test_ctrl_firmware.py --lwsrp <pin>` (all ctrl arms, SRP arms at IF=1/2, debug arms, every entity shape) | rc 0. `test_acmp_mbx` passes 52/52 at each count, including the three new cases. | `receipts/suite.log`, `receipts/arms/suite-test_acmp_mbx-if{1,2}.log` |
| Coverage ratchet, `fw_coverage.py --check --lwsrp <pin>` | rc 0, 22 files at 100 % lines and branches. `srp_mbx.c` is 515/515 and 478/478; `ctrl_app_srp.c` is 82/82 and 62/62. | `receipts/coverage.log` |
| AddressSanitizer: seven SRP and composition suites, IF=1/2 (`scripts/asan.py`) | rc 0, 140 tests per count. The binaries link the sanitizer runtime (`__asan_init` present). | `receipts/asan.log`, `receipts/asan/` |
| The three named plants through the standing campaign driver, IF=1 and IF=2 (`scripts/named_plants.py`) | 6/6 caught by name and needle, at `srp_feedback.hpp:30-31` and `:134-135` | `receipts/named-plants-if{1,2}.log`, `receipts/plants/named-*` |
| Full standing SRP campaign as `--self-test` selects it (`scripts/srp_campaign.py`) | IF=2 169/169 caught; IF=1 68/68 caught; rc 0 | `receipts/srp-campaign-if{1,2}.log` |
| The 22-plant SrpFeedback family (`scripts/feedback_family.py`) | 22/22 at IF=1 and 22/22 at IF=2 | `receipts/feedback-family-if{1,2}.log` |
| Static plant-table check (`scripts/plant_sites.py`) | 169 plants, each with one planting site, no duplicate names. 68 in the IF=1 selection, including all three new ones. | `receipts/plant-sites.log` |
| Original R532-12 probe header appended to a disposable copy, `SrpFeedback.*` (`scripts/r12_probe_tests.py`) | rc 0, 22/22 per count (19 standing plus `R12*` T1, T2 and T3) | `receipts/r12-probe-tests/` |
| Reviewer-owned extra probes on the new cases, IF=1/2 (`scripts/extra_probes.py`) | 10/10 caught by name. x1: Failed Lv ignored, on `:87` and `:104`. x2: a leave clears both kinds, on `:122`. x3: filter capture removed, on `:87`. x4: q04 observed by `:104`. | `receipts/extra-probes-if{1,2}.log`, `receipts/plants/extra-*` |
| Docs gates: `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, `check_submodule_docs.py` | rc 0 for all four (0 findings across 200 md files; 941 paths; 5 exact gitlinks) | `receipts/docs-*.log` |
| Scope, gitlinks and stale pin (`git grep 19f5796b` → none) | Only the three files change. Gitlinks are unchanged. | `receipts/scope.log` |
| Clone restoration | HEAD, tree and index tree are `1928df9c…`. 1215 tracked blobs and modes match, with 0 mismatches. Worktree equals the index, which equals HEAD. Submodule gitlinks are as recorded. No untracked or ignored residue remains: the bytecode caches created by this round were removed. | `receipts/restore-verify.log` |
| Exact-head hosted check runs (snapshot only) | See section 8 | `receipts/hosted-checks.tsv` |

The author's published claims in the PR body ("Round 13") and in `ROUND13-*` match these independent results: 52 composition cases per count, 140 sanitizer tests per count, 169 and 68 SRP plants, 22 coverage files at 100 %, and three R12 probe cases per count.

## 4. Lens results

```text
[R532] PASS Conformance — srp_feedback.hpp:87,104,122; srp_mbx.c:81-115,159-171,562-585; lwSRP 9197193e mrp_mad.c:622-681 — Assignment 6051940062 items 1 and 3 met. Each case asserts the behaviour the round-11/12 decisions require: an Lv withdrawal is retained across a same-PDU New (Milan v1.2 4.2.7.2.2 rapid leave), an atomic replacement stays continuous, and a per-kind leave with the other kind registered is a kind change (Milan Table 5.23 REGISTERING_FAILED on the wire) and not a withdrawal. Item 2 was optional and was not taken.
[R532] PASS RTL — receipts/scope.log (efea7485..154722e1 name-status and gitlinks); srp_mbx.c:30-41,159-190 — No RTL, mailbox contract, register, configuration or gitlink change in the delta. Interface contract re-read: the filter makes no lwSRP entry. S1 retained as a SUGGESTION only.
[R532] PASS Robustness — srp_feedback.hpp:87-138; receipts/asan/; receipts/extra-probes-if{1,2}.log — Multi-message single PDUs for each kind ordering (Lv→New, JoinIn→Lv→JoinIn, Lv with the other kind refreshed), both sinks, IF=1/2, one-PDU assertion, AddressSanitizer clean at 140 tests per count, and four further single-site faults on the same logic caught by name.
[R532] PASS Tests — srp_mutants.py:802-814; test_ctrl_firmware.py:199-207; receipts/named-plants-if{1,2}.log, srp-campaign-if{1,2}.log, r12-probe-tests/, coverage.log — Each new case fails for the defect it claims (q04, q13 and q06 equivalents caught by named observable at IF=1 and IF=2, inside the standing 169 and 68 campaigns). The original R532-12 probe tests pass unmodified. Coverage is unchanged at 100 % with no new exclusion.
[R532] PASS Docs — docs/design/MAILBOX_SPLIT.md:294-297; docs/reference/SUBMODULES.md:26; sw/firmware/ctrl/test/ctrl_arms.py:362; sw/firmware/ctrl/srp/README.md:80,258-266; live PR body "Round 13"; receipts/docs-*.log — The pin citation now equals the gitlink and LWSRP_REV, and no stale 19f5796b reference remains. The README's existing claims now carry Failed-kind tests. The PR body's round-13 figures match the reviewer's re-execution. Four docs gates rc 0.
```

## 5. Findings at this head

No new finding.

**R532-12-S1 | SUGGESTION | RTL, Tests | `srp_mbx.c:30-41` (`enter`), `srp_mbx.c:572-585` (`snapshot`) | Debug-only reentrancy flag for internal registrar visits (carried, unchanged).**

- **Authority:** lwSRP `integrator.md:323`, under which the adapter owns debug and release enforcement.
- **Evidence:** the existing busy guard covers adapter entries but not a `snapshot()` reintroduced inside a library callback.
- **Impact:** a future regression of the round-11 reentry would not fail a test. No present defect exists.
- **Optional outcome:** a debug-only flag held across `mrp_rx`, `shlan_timer_tick` and `mrp_transmit`, asserted in `snapshot()`, plus a test that restores the reentrant visit and fails.
- **Effect here:** it does not affect the verdict or any lens.

## 6. Prior public findings at this head

| Finding | Status at `154722e1` |
|---|---|
| R532-12-F1 (MINOR; Tests): Failed-kind half of the copy observation had no discriminating test | **Resolved.** The three required standing cases exist (`srp_feedback.hpp:87,104,122`), run through real mailbox ingress and the composition poll at IF=1/2, and pass. Plants equivalent to q04, q13 and q06 are caught by their named observables at IF=1 and IF=2, both in isolation and in the standing campaigns (169 and 68). The original probe tests T1, T2 and T3 pass unmodified. Coverage remains at 100 %. No production change was made or needed. |
| R532-12-S1 (SUGGESTION; RTL, Tests) | **Not taken; acceptable.** Carried as an optional SUGGESTION (section 5). |
| R533-12-R1 (RESIDUE; Docs): stale lwSRP pin at `MAILBOX_SPLIT.md:294-297` | **Resolved.** Line 295 cites `9197193e47a6bb1c45a56d90a18c1784123aba44`, equal to the gitlink. |
| R532-8-F1, hosted half (carried) | **Still a manager duty.** See section 8. |
| Earlier rounds (R532-1 to R532-11, R533-1 to R533-11) | Retained as resolved per the round-12 baseline. This delta touches none of their sites. |

## 7. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment 6051940062 items 1 to 3, against `srp_feedback.hpp:6-32,87-138`, `srp_binding.hpp:49-68`, `srp_mbx.c:81-115,159-171,562-585`. Pinned lwSRP `mrp_mad.c:622-681`, `integrator.md:321-323`. Named cases and plants at IF=1/2. | R532-13 | 154722e14781c7373f3229420b6e007f9bcf9835 |
| RTL | CLEAN | `receipts/scope.log`: the delta name-status contains no RTL, `sw/mailbox`, register, configuration or workflow path, and gitlinks are identical at `efea7485` and the head. Adapter reentry guard `srp_mbx.c:30-41` and filter `:159-190` re-read. S1 is optional. | R532-13 | 154722e14781c7373f3229420b6e007f9bcf9835 |
| Robustness | CLEAN | New multi-message PDU cases for both kinds and both sinks at IF=1/2. AddressSanitizer, 140 tests per count. Extra probes x1 to x4 caught. Full ctrl suite rc 0. | R532-13 | 154722e14781c7373f3229420b6e007f9bcf9835 |
| Tests | CLEAN | `srp_mutants.py:802-814`, `test_ctrl_firmware.py:199-207`, `receipts/named-plants-*`, `srp-campaign-if{1,2}.log` (169/169, 68/68), `feedback-family-*` (22/22 ×2), `plant-sites.log`, `r12-probe-tests/`, `coverage.log` (22 files at 100 %) | R532-13 | 154722e14781c7373f3229420b6e007f9bcf9835 |
| Docs | CLEAN | `MAILBOX_SPLIT.md:294-297`, `SUBMODULES.md:26`, `ctrl_arms.py:362`, `srp/README.md:71-82,258-266`, live PR body "Round 13", and four docs gates rc 0 | R532-13 | 154722e14781c7373f3229420b6e007f9bcf9835 |

## 8. Real limits

- **Delta review.** This round re-ran the complete ctrl suite, the full SRP campaign, coverage, the sanitizer suites and the docs gates. It did not re-run:
  - the 471-plant control campaign, or the pin-refusal controls;
  - the SRP RV32 arms with the pinned SDK (`--require-rv32`);
  - linked images and the builder bank;
  - the parent, processor, gPTP and Yosys banks;
  - act or Docker.
  The delta changes none of their inputs.
- **No manager source bank.** No manager source bank ran at this exact head. The source-head execution evidence is the author's published receipts plus this round's reviewer runs. Neither is the current-dev merge candidate.
- **Hardware.** Physical calibration was NOT RUN. Skipped field and physical contexts are not hardware proof.
- **Hosted contexts.** The snapshot at 2026-10-08T05:01:04Z (`receipts/hosted-checks.tsv`) shows executed successes for:
  - `changes`, `verilator-lint`, `wire-accountability` and `yosys-elaboration`;
  - Yosys shards 0 to 3 and Verilator shard 3/5;
  - `bdd-conformance`, `docs-check-no-git` and `full-ci-gate`.

  Still in progress: `docs-check`, `elaborate`, `firmware-unit`, and Verilator shards 0, 1, 2 and 4. `Physical gPTP` was skipped and is not counted. This snapshot records state only.
- **Probe scope.** The probes plant single sites in a disposable copy. Equivalent or unreachable mutants beyond those recorded were not enumerated.

## 9. Pending manager duties

- **Hosted acceptance at the exact head:** `docs-check`, `elaborate`, `firmware-unit`, and Verilator shards 0, 1, 2 and 4, plus the act local replica. Also the hosted half of R532-8-F1.
- **Merge turn:** build and validate the current-dev merge candidate (builder and native banks, source base and live dev `99e4eb6c`) and link its receipts. This verdict does not authorize a merge.
- **R532-12-S1:** optional. File it as a separate hardening Issue if the owner wants it.
- **Second positive:** obtain the external review's verdict at this head.

R532-13 FINISHED
