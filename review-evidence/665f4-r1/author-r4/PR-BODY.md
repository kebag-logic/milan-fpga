[A560]

## Contents

- **[Status](#status)** -- Candidate and validation state.
- **[Linked Issue / roles](#linked-issue--roles)** -- Scope and independent reviewers.
- **[Description](#description)** -- Bare-metal SRP behavior.
- **[Round 3](#round-3)** -- Previous findings and evidence.
- **[Round 4](#round-4)** -- Shared inheritance and Domain-VID regressions.
- **[Authoritative references](#authoritative-references)** -- Applicable contracts.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Dependencies and environment.
- **[How to validate](#how-to-validate)** -- Commands and pass criteria.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- Integration and review obligations.
- **[Definition of Done](#definition-of-done)** -- Remaining merge bar.

## Status

REVIEW READY: assigned round-4 local gates pass. `665-f4-srp` -> `dev`.
Head: `6f7deea15a9160761b30aaa93fe152f20d416695`.
Round 3 was REVIEW READY under ruling 6036016117. The compiler-absent docs entry passed in the manager's run (PR comment 6036186046); the builder bank remains with the candidate bank. Both checks remain with the manager under round-4 assignment 6036454509. This round makes no push or PR edit.

## Linked Issue / roles

Relates to #665.

Executor: `[A560]`.
Internal cleared-context reviewer: `[R532]`.
External reviewer: `[R533]`.
R533-3 was positive and R532-3 was negative at the preceding head. Independent re-review owns closure of the corrected findings.

## Description

Provide per-interface MSRP and MVRP through the bare-metal mailbox, using pinned lwSRP and entity-sized static pools. Startup declares every output, Class A Domain and its VLAN. Bound sinks reconcile Listener declarations; licences follow admission, registration and committed membership. Refused TX retains bytes and interface until commit. The firmware uses neither an OS nor a heap.

## Round 3

Attach learns each current mailbox link level. Polling recovers after a held level-change record is cancelled. Shared binding replacement preserves Applicant state until reconciliation; loss of the final eligible request withdraws Ready. The final binding releases a non-Domain VID regardless of its prior eligibility.

The dependency inventory, licence, fetch guidance and generated diagram are current. The round-3 documentation set passed 76 commands in the lane; the compiler-absent entry passed in the manager's run (6036186046). The dependency's published `f4-applicant-notes` follow-up tests Applicant notes 4/5. Its production sources equal the unchanged parent pin `23d9a8173b07503a0ee6e8528f922fceab4e67f0`.

## Round 4

R532-3-F1 now has two wire regressions: an ineligible binding joins an already-Ready StreamID in the other slot, then outlives the eligible binding; and a still-registered StreamID is rebound beside another Ready StreamID. They require withdrawal without stale renewal and a separate Ready declaration respectively. Both slot orders run on every interface.

R532-3-F2 now verifies final unbind preserves and renews the current Domain VLAN while withdrawing the Listener. It covers startup VID 2, peer-selected VID 7, both slots and every interface. The README states the Domain-VID exception.

Three matching plants reproduce RP3, RP10 and RP5. The adapter positives pass 53 cases at IF=1 and IF=2. The complete firmware command passes all 100 control plants, all 70 SRP plants and both dependency-refusal controls; all 19 final recorded gate commands return 0. Coverage remains 100% in all 15 measured files after unchanged exclusions, including 441/441 lines and 410/410 branches in `srp_mbx.c`. This commit changes only tests and the README; production sources, pins, generated files and ratchet are unchanged.

## Authoritative references

- Issue #665 assignments 6030279477, 6033558691, 6035166787 and 6036454509; rulings 6036016117 and 6036186046.
- R532-3 under `review-evidence/665f4-r1/reviews/R532-3/` on `665f4-review-evidence`; PR comment 6036450620.
- `REQUIREMENTS.md` section 1; `docs/design/MAILBOX_SPLIT.md`; `docs/reference/FR_NFR.md` NFR-SCOUT-02/03/08.
- Milan v1.2 4.2.7.2.2, 4.3.2, 5.5.2.7 and Table 4.3; IEEE 802.1Q-2018 Tables 10-3/10-4, 10.7.11, 35.1.2.2, 35.2.2.7.2 and 35.2.6.
- #608, #678, #679 and processor #134.

## How to get into the same state

After the integration role publishes this head:

```sh
git switch 665-f4-srp
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP
export TMPDIR="$SCRATCH"
export PYTHONDONTWRITEBYTECODE=1
export MILAN_RV32_CC="$SDK/bin/riscv32-linux-gcc"
export VERILATOR="$PINNED_VERILATOR"
export VERILATOR_JOBS=2
```

Use the CI-pinned ilp32d SDK distribution with the gate's RV32I/ILP32 freestanding flags and HDL compiler release 5.050. The dependency checkout needs repository read access. Keep build products in disk scratch and cap campaigns at four workers.

## How to validate

```sh
python3 scripts/ci_rv32_sdk_selftest.py
python3 scripts/ci_rv32_sdk.py --destination "$SDK"
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir "$SCRATCH/firmware"
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep "$SCRATCH/coverage"
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
python3 sw/firmware/gtest/tally_selftest.py --mutants
python3 sw/mailbox/gen_mailbox.py --check
python3 scripts/docs_check.py
python3 scripts/docs_check.py --selftest
python3 scripts/check_doc_paths.py
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/check_em_dash.py --base c1049de1970e93d2c36ace62891ee9d947cd3191
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
python3 scripts/check_hygiene.py --check
git diff --check c1049de1970e93d2c36ace62891ee9d947cd3191 HEAD
```

Expected result: each command exits 0; positives pass, every named defect is caught, and all coverage rows remain at 100%. The control gate includes the complete SRP campaign. HANDOFF.md records changes with file locations, test-to-defect mappings, coverage and gate tables. The round-4 packet retains small receipts and hashes larger artifacts.

## Known limitations / out of scope

- ACMP application composition, live MAAP/stream inputs and the connected fabric licence output remain integration work; F3 is absent from the assigned base.
- Service latency is a conditional host envelope with one shared 10 ms budget. Target scheduling and wire timing require separate release evidence.
- Retained round-3 linked spans are 53,968 / 65,216 bytes for 1x1 at IF=1/2 and 68,656 / 94,656 for 8x8. They include pools, alignment and an 8192-byte stack reservation, which is not a whole-call-chain bound. These are size fixtures, not booted images or routed measurements; round 4 changes no production code.
- No RTL, default all-fabric build, register map or shipping-image change is included.
- The manager owns the builder bank, compiler-absent check, publication, hosted checks, trusted local replication, upstream follow-up and later pin move, candidate validation and containment. No hardware validation is claimed.

## Definition of Done

- [ ] Linked Issue acceptance criteria are fully satisfied
- [x] New or changed behavior has self-checking tests
- [x] Assigned round-4 local verification passes
- [ ] Complete candidate and hosted verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive at the corrected head
- [ ] External review is positive at the corrected head
- [ ] Findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
