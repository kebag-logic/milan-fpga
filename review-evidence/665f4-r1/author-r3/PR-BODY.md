[A560]

## Contents

- **[Status](#status)** -- Candidate and validation state.
- **[Linked Issue / roles](#linked-issue--roles)** -- Scope and independent reviewers.
- **[Description](#description)** -- Bare-metal SRP behavior.
- **[Round 3](#round-3)** -- Accepted findings and current evidence.
- **[Authoritative references](#authoritative-references)** -- Applicable contracts.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Dependencies and environment.
- **[How to validate](#how-to-validate)** -- Commands and pass criteria.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- Integration and review obligations.
- **[Definition of Done](#definition-of-done)** -- Remaining merge bar.

## Status

STOP: round-3 validation incomplete. `665-f4-srp` -> `dev`.
Head: `c1049de1970e93d2c36ace62891ee9d947cd3191`. The compiler-absent docs entry timed out twice at 540 seconds, including an isolated retry. The remaining final gate rows pass. The builder bank belongs to the manager's candidate bank under assignment 6035166787; that delegation is not used to claim this separate docs entry passed. This round made no push or PR edit.

## Linked Issue / roles

Relates to #665.

Executor: `[A560]`.
Internal cleared-context reviewer: `[R532]`.
External reviewer: `[R533]`.
Both round-2 verdicts were negative. Fresh independent verdicts are required on this head.

## Description

Provide per-interface MSRP and MVRP through the bare-metal mailbox, using the pinned lwSRP library and entity-sized static pools. Startup declares every output, Class A Domain and its VLAN. Bound sinks reconcile Listener declarations; licences follow admission, registration and committed membership. Refused TX retains bytes and interface until commit. No OS or firmware heap is introduced.

## Round 3

Attach now learns each mailbox link level, and polling recovers after a held level-change record is cancelled. Shared binding replacement preserves Applicant state until all bindings are reconciled; loss of the final eligible request withdraws Ready. The last binding releases its VID even if it never requested membership itself.

Nine new cases cover reattach, cancelled-record recovery, replacement combinations, consecutive rebinds, final VID withdrawal, the three lifecycle/shared-VLAN test gaps, and generic MVRP timing. There are 50 adapter cases per interface count. All 67 SRP plants, all 100 control plants and both dependency controls are caught. The selected processor walk/differential, target builds and all 15-file coverage checks pass at 100%, with no new exclusions.

The lwSRP inventory, Apache-2.0 licence boundary, fetch guidance and generated submodule diagram are current. All four previously failing submodule commands pass on this committed head. Of the 77 docs-check commands selected from the workflow, 76 pass and the compiler-absent entry remains incomplete. The additional offline runner self-test passed inside a disposable job boundary. Full local or hosted docs-context success is not claimed.

The published `f4-applicant-notes` topic `495520f5e02dd077fc9b1451942b25ec95afa1b8` follows dependency PR #12. Its `applicant_receive_conditions_follow_link_mode` and `pending_applicant_joinin_obeys_note_four` tests discriminate both link modes; `point-to-point-condition`, `pending-point-to-point-condition` and `shared-in-condition` each fail their named tests. Both positive profiles and all 40 upstream reversals pass. The parent pin stays `23d9a8173b07503a0ee6e8528f922fceab4e67f0` and the topic's production sources are identical to it.

Linked composition spans are 53,968 / 65,216 bytes for 1x1 at IF=1/2 and 68,656 / 94,656 for 8x8. Static storage is unchanged from round 2. Spans include pools, alignment and an explicit 8192-byte stack reservation; the corresponding dev-base spans are 19,200 / 19,696. These are linked size fixtures, not booted images or routed resource measurements.

## Authoritative references

- Issue #665 assignments 6030279477, 6033558691 and 6035166787; acceptance addition 6030870481 and ruling 6034653240.
- R532-2 and R533-2 under `review-evidence/665f4-r1/reviews/` on `665f4-review-evidence`.
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

Use the CI-pinned ilp32d SDK distribution with the gate's RV32I/ILP32 freestanding flags, and HDL compiler release 5.050. The dependency checkout needs repository read access. Keep build products in disk scratch and cap campaigns at four workers.

## How to validate

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir "$SCRATCH/firmware"
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep "$SCRATCH/coverage"
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
python3 sw/firmware/gtest/tally_selftest.py --mutants
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
make -C "$SCRATCH/mailbox/tb/verilator/mbx" -j2 VERILATOR="$PINNED_J8_WRAPPER"
python3 sw/mailbox/gen_mailbox.py --check
python3 scripts/lint_rtl.py
```

Run the full docs-check command set from `.github/workflows/docs.yml`, including the four verified-submodule commands, with the builder bank delegated as assigned. Run `act_ci.py --selftest` only inside a disposable job boundary. HANDOFF.md and ROUND3-GATES.md record exact commands and exits, the incomplete compiler-absent entry, coverage table, 67 test-to-defect mappings and receipt hashes. Rebuild the four linked size rows with `ctrl_image.py` and the recorded runtime archives.

Supplemental reviewer-probe evidence is reported separately: the unchanged shared-rebind wire probe passes at IF=1/2. R532 P3's old false-cache setup assertion conflicts with deliberately inherited shared-VID state; the lane's assigned equivalent preserves the never-requested setup, checks both wire unbind orders and catches the old defect. The full supplemental log includes those two setup failures and is not claimed wholly green.

## Known limitations / out of scope

- ACMP application composition, live MAAP/stream inputs and the connected fabric licence output remain integration work; F3 is absent from the assigned base.
- Service latency remains a conditional host envelope with one shared 10 ms budget. Target scheduling and wire timing require separate release evidence.
- The stack reservation is not a whole-call-chain bound. No RTL, default all-fabric build, non-mailbox register map or shipping-image change is included.
- The manager owns the builder/candidate bank, hosted checks, trusted local replication after publication, upstream follow-up, merge-candidate validation and post-merge containment. No physical validation is claimed.
- The recorded service memory peak was 10,242,949,120 bytes, exceeding the requested 9 GB working target; final current use was about 1.2 GB.

## Definition of Done

- [ ] Linked Issue acceptance criteria are fully satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Assigned local round-3 verification passes, with the builder bank delegated
- [ ] Complete candidate and hosted verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
