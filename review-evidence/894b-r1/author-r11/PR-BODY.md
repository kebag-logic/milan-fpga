[A781]

## Contents

- [Status](#status)
- [Linked Issue / roles](#linked-issue--roles)
- [Description](#description)
- [Authoritative references](#authoritative-references)
- [How to get into the same state](#how-to-get-into-the-same-state)
- [How to validate](#how-to-validate)
- [Known limitations / out of scope](#known-limitations--out-of-scope)
- [Definition of Done](#definition-of-done)

## Status

**STOP at `05a7ea82fa0625e077959cd1b4eed28a7a05b064`, round 11.** The numerical targets of #930 are met, and the ruled ledger change is committed. The final gates fail: two SRP mutations escape, and the twin comparison and its planted controls fail. This head is not review ready. Nothing has been pushed; the manager owns publication and the base synchronization for PR #914 (`894-8x8-1if` -> `894-tiers`).

The final-head step inventory, individual results and reasons for steps not run are in `receipts/gates/workflow-steps.md`, `receipts/gates/workflow-steps.json` and `receipts/gates/not_run.json`. Launcher exit codes are not acceptance evidence: the earlier wrappers returned zero despite recording failed commands.

## Linked Issue / roles

Closes #930
Relates to #894
Relates to #872

Executor: `[A781]`
Internal cleared-context reviewer: `[R843]`, latest R843-3 at `af2c4d7a`, NEGATIVE; re-review remains due.
External reviewer: `[R844]`, latest R844-3 at `af2c4d7a`, POSITIVE; that verdict does not cover this head.

## Description

The lane gives 8x8/1if its own shape, scheduling costs and acceptance evidence. #930's subsequent fix copies Listener changes where the split SRP adapter receives them, removing the registrar walk from each Listener record while preserving callback order, arguments and published state. No donor implementation changes.

### #930 targets and measured figures

Measured on `46cf2a7d`'s image; all eight images rebuilt at this head have identical ELF and loadable-byte hashes. The round-10 measurements therefore carry to this head. This identity does not clear failing source-level tests or an incomplete sweep.

| Target | Before the fix | Fixed measurement | Required |
|---|---:|---:|---:|
| 1x1/1if SRP record | 27,170 CPU cycles, 290 us by the rule | 23,503 cycles, 250 us by the rule; stated 280 us | At most 280 us / 26,660 cycles |
| 1x1/1if last queued notice, by every source | 157.09 ms after restating costs | 136.65 ms | At most 140 ms |
| 8x8/1if load at the pin | 0.783 after restating costs | 0.735 | At most 0.75 |
| Measured CPU-decided rows at both points, including `srp-talker-held` | New group exposed the understated SRP cost | Each within its own bound | Each row's bound |

At 8x8/1if the SRP record falls from 42,663 to 32,936 cycles (350 us by the rule; stated 365). The retained retry is stated at 345 us from 32,618 cycles. At 1x1/1if the retained retry is stated at 280 us from 23,144 cycles. These figures return to each point's earlier statements, never below them. The 8x8/1if reclaim is stated at 40 us from 3,446 cycles. The ruling accepts these restatements.

R4 by every source at 8x8/1if is **21.39 ms against 20 ms**, owed to #872. Other reported every-source rows there remain owed too: R5 136.64 ms, the last queued notice 387.95 ms, and txL 159.82 ms. Measured acceptance does not turn those derived misses into passes.

Evidence: `receipts/round10/model/`, `receipts/round10/harness/legs-46cf2a7d/`, `receipts/images/qimg-05a7ea82.txt`, and `receipts/images/identity-46cf2a7d-05a7ea82.txt`.

### Round 11's ruling and implementation

| Item | Result | Change / evidence |
|---|---|---|
| Move the one held-egress figure by ruling | `backlog-owed.service.aecp.last.if0` at 8x8/1if is 62.16 ms. The composed image measured 61.75319 ms; the Listener-copy image measures 62.04905 ms. The earlier merged image measured 61.84625 ms. The ledger retains all three and derives each entry from the largest measurement using the existing rule. The other six entries do not move. | `7ee9342d`; `tb/verilator/ctrl_service_budget/egress_ledger.py`; section 13 |
| Explain the changed measurement | The cheaper records open the composed window 290 us earlier. ACMP's owed frame then precedes AECP's after the hold releases. The growth is phase, as the ruling records. | `receipts/round10/harness/aecp-last-phase.txt`; ruling linked below |
| Keep authoritative figures current | Section 13 and FR_NFR 3.4.1 describe the Listener-copy image at both points and its measured record. | `9203d89d` |
| Include the new campaign in shard accounting | The SRP campaign stand-in accepts its entity argument and includes it in the invocation identity. The inventory sees 1,537 invocations, each assigned exactly once. This fixes the first attempt's argument mismatch before the final pass. | `05a7ea82`; `sw/firmware/ctrl/test/test_ctrl_firmware_shards.py:70` |
| Regrade existing measurements | Fourteen positive legs per point pass the final ledger, with no new measurement. The separate `transmit-aged` control is caught in all eight groups. An audit that included that negative control in positive acceptance correctly failed; its diagnostic is retained. | `receipts/harness/gate-1x1-05a7ea82.txt`, `gate-8x8-1if-05a7ea82.txt`, `control-included-refusal.txt`; round-10 `M8-CTA/leg.log` |
| Final gates | **Failed**, as below. No acceptance change or source repair is made after discovering the failures. | `receipts/gates/` |

The ledger's self-test passes with 15 caught mutants, including the new mutation that derives this entry from the smaller composed measurement. The unchanged-ledger control and each row's one-cycle and large increases remain tested. The held-egress rows remain recorded budget misses; a larger miss fails acceptance.

### Gate failures at the final head

| Gate | Result | Exact failure and source evidence |
|---|---|---|
| `rtl-fast.yml / firmware-srp-mutants / ci_step_9` | rc 1 | `[ESCAPED] asking-is-ready` and `[ESCAPED] readyfailed-ignored`. Both mutated tests return success. `srp_mutants.py:94` and `:224` still mutate `v[8] == 2 || v[8] == 3` in the registrar walk (`srp_mbx.c:861`); the new Listener callback copies readiness at `srp_mbx.c:185`. The receive path no longer owes that walk, so these plants no longer alter the behavior their selected tests exercise. |
| `make -C tb/verilator/milan_dp twin` | rc 2 | `[DIFF] owed row split-talker-failed does not hold`. The split trace declares Talker Advertise for stream `0200000000010000`, while the row expects Talker Failed for both sources from boot, never withdrawn. This is an observed expectation mismatch; this pass does not establish when it originated. |
| `make -C tb/verilator/milan_dp twin-plants` | rc 2 | `plant srp-plus-k: ESCAPED by "MSRP Talker Failed stream_id 0200000000010001"`. The planted run emits protocol diagnostics for Talker Advertise, while `twin_compare.py:70` expects Talker Failed. The required diagnostic was not found. |

Full or explicitly excerpted logs, original byte counts and SHA-256 hashes are retained under `receipts/gates/workflow/`, `receipts/gates/lane/` and `receipts/gates/raw-manifest.json`. No failed command is relabeled as a pass.

### Other final-head gate results

| Gate family | Result |
|---|---|
| Workflow commands | 83 executed: 82 rc 0, one rc 1 (SRP campaign). Each unexecuted `run:` step has a reason. These are local commands, not hosted jobs. |
| Firmware suites and coverage | All six unit-job steps rc 0; coverage ratchet PASS across 39 files, including `srp_mbx.c` 746/746 lines. |
| Control and AECP campaigns | All steps rc 0; 716 and 302 `[ok]` lines respectively, no escapes. |
| Boundary and firmware simulation jobs | Every executed step rc 0. |
| Documentation jobs | Every executed step of all six selected docs jobs rc 0. The no-git job intentionally removes Git metadata; its driver's later status query fails, separate from its three successful job steps. |
| Lane checks | 72 commands: 66 rc 0; four explicitly named report/control commands return their expected rc 1; `twin` and `twin_plants` fail at rc 2. |
| Quick checks | 21 rc 0, including ledger, shape costs, flip checks, comment scans and diff checks. |
| Selected exhaustive shards 1, 3, 4, 6, 10, 17 | No complete pass. The first attempts refused the local donor origin before affected suites ran. Fresh-clone retries of 1, 3, 4 and 6 were stopped on discovery of the firmware failure; 10 and 17 were not retried. No partial total is claimed. |
| `docs_inventory --check` | NOT RUN: no tracked executable with that name exists at this head. This is not substituted by a docs-job pass. |
| Image identity | All eight final images match `46cf2a7d` by ELF and loadable-byte SHA-256; the 8x8/1if platform remains 56.0 RAMB36. |

### Finding-by-finding dispositions

These are author dispositions. Independent reviewers must re-review the corrected head and own the completion ledger.

| Review item | Disposition |
|---|---|
| R844-1-F1, MAJOR: arbitrary growth of a held row passes | Fixed in round 4 by tracked `egress_ledger.py`, beside the graders. It checks every measured instance, fails new or enlarged misses, and owns its self-test. Each of seven names has one-cycle and large-increase controls; every published round-3 leg regraded successfully. See `receipts/round4/gates/gate-r4-controls.txt` and `receipts/round4/regrade/`. |
| R844-1-R1 and R843-1-R1: source-comment residue | Fixed. Added comments, docstrings and check descriptions carry behavior, issue and requirement references. Final-head scans of `7398ec0a..HEAD` and the newer deltas find zero prohibited lines. Round 4's before/after images are identical; receipts are in `receipts/round4/images/`. Later #930 firmware changes have their own measured image and are not claimed identical to round 3. |
| R843-1-S1: explicit compile-time contract | Taken. The guarded error names THE SHAPES when the attempt cost is used without its table; the host arms compiling `test_aecp.cpp` assert the interface contract. Both failing controls are in `receipts/round4/firmware/item3-guard-and-assert-checks.txt`. The debug and wire-only arms retain their documented contract. |
| R843-2-RES1 and R844-2-R1: ledger wording and include-order wording | Fixed in `a15345f7`; the header explains that most units include it before the table and charge nothing. |
| R843-2-RES2: assertion scope overstated | Corrected: the assertion applies to the arms compiling `test_aecp.cpp`. |
| R843-2-RES3 and R844-2-R2: stale carry receipt/range | Corrected to round 4's final `98c0b62b` evidence and `716a8ae7..98c0b62b`; current image evidence is separately named above. |
| R843-2-S1: refused groups invisible to directory grading | Taken in `25c782a4`; a results directory needs `results.json`, and its refusals fail. Controls and a mutant enforce it. |
| R843-2-S2 and R843-3-S2: extra debug/wire shapes | Not taken: these arms do not measure retry costs; the debug test configures one interface. |
| R843-2-S3: generated packet index | Taken; INDEX.md is regenerated from the files present after the final edits. |
| R843-3-F1: superseded figures presented as current | Fixed in `d0fea5f0` and `d539f162`, then updated again for #930 by `9203d89d`. Section 13 and FR_NFR describe the current image; this body states the current figures and failing gates. |
| R843-3-F2: mixed-point completeness skipped | Fixed in `d2fd8975`. Every exercised point in `COMPLETE` is checked. The mixed-point probe and all 14 record-class controls pass at the final head. |
| R843-3-R1 and R844-3-R2: slice keyed by interface count in documentation | Fixed in `d0fea5f0`; documentation keys the slice by THE SHAPES. |
| R843-3-R2: unlinked ledger ruling | Fixed; section 13 and FR_NFR link the ruling. |
| R844-3-R1: record classes described as merely reported | Fixed in `d2fd8975`; the 8x8/1if classes are held at their stated costs. |
| R844-3-R3: old figures beside current ones | Historical measurements are labeled. Current figures and identity proofs appear above. |
| R844-3-R4: reversed survey relation | The survey holds each measurement within its statement by the rule. |
| R843-3-S1: retained retry tied to measured record | No separate policy change: the apply check remains stricter; #930's measured apply now supports the stated 345 us at 8x8/1if. |

The original R843-1 and R844-1 reports are retained in `receipts/reviews/`. The new failed gates remain open regardless of earlier positive reviews.

## Authoritative references

- [#894 round-11 ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6934688411): the 62.16 ms ledger move, accepted #930 targets, final gates and #872's R4 debt.
- [#930](https://github.com/kebag-logic/milan-fpga/issues/930) and [the preceding ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6918853411): fix the SRP cost inside the split adapter; bounds do not move.
- [Held-egress ruling, item (a)](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6871343905) and [ledger ruling, items 2 and 3](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6892938049).
- [Shape ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867393730), [retry-cost ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6878014227), and [egress bounds](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867990126).
- IEEE 802.1Q-2018 Table 10-4; FR_NFR 3.4.1; SPLIT_CONTROL_MEMORY sections 11 and 13; the SRP adapter contract.
- #818: timing floor +0.030 ns setup, 0 ns hold, best of three directives.

## How to get into the same state

The manager must publish the local commits before these commands can retrieve them.

```sh
git fetch origin 894-8x8-1if
git switch --detach 05a7ea82fa0625e077959cd1b4eed28a7a05b064
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP
```

## How to validate

On a clean clone with the pinned prerequisites:

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 8 --shard 3/4
make -C tb/verilator/milan_dp -j16 twin
make -C tb/verilator/milan_dp -j16 twin-plants
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 8
python3 -I tb/verilator/ctrl_service_budget/egress_ledger.py --selftest
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 8x8/1if
git diff --check
```

At this head the first three commands reproduce the failures above; the remaining recorded gates pass. Acceptance requires correcting and rerunning the failures, finishing the selected shards, and completing independent review. Existing harness outputs can be regraded without a new measurement using `scripts/gate_r10.py` in this packet; its command contract and final receipts name the input populations.

## Known limitations / out of scope

- Every-source R4 at 8x8/1if remains owed to #872, as ruled. The held-egress rows remain recorded misses, limited by their ledger.
- The timing floor is **#818's +0.030 ns setup and 0 ns hold, best of three directives**. This round performs no route and claims no new timing result.
- `Mailbox.ARoundFillsWhatItsPassHasLeft` at 8x8/1if is the previously disclosed test outside the selected arm; its historical reproduction is in both reviews.
- No hardware, bench, flashing, donor edit, merge or base synchronization occurred in this round. No hosted or merge-candidate pass is claimed.

## Definition of Done

- [ ] Linked Issue acceptance criteria and verification are fully satisfied
- [x] Changed behavior has self-checking tests; the escaped existing mutations remain open
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] Requirement and interface changes are documented
- [ ] Internal cleared-context review is positive at the candidate
- [ ] External review is positive at the candidate
- [ ] Blocking findings and gate failures are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated
- [x] Authoritative documentation includes the ruled ledger update
- [ ] Post-merge containment is clean before the Issue moves to Done
