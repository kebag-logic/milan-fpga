2026-10-09T18:26:56Z
[A572]

## Contents

- **[Status](#status)** -- Local evidence and remaining review work.
- **[Linked Issue / roles](#linked-issue--roles)** -- Assignment and reviewers.
- **[Description](#description)** -- Opt-in AECP ownership.
- **[Round 3](#round-3)** -- No-subcommand latency evidence.
- **[Authoritative references](#authoritative-references)** -- Requirements and clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Candidate and dependencies.
- **[How to validate](#how-to-validate)** -- Commands and expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- Integration obligations.
- **[Definition of Done](#definition-of-done)** -- Publication and review gates.

## Status

Local implementation head `fb9c57d2ae3484804ff90f67feb57bf420c93dfa`; `665-f5-aecp` -> `dev`.
PR #700 is published at `0ded1f269a44d107498f177c8276665656e07d30`. The two Round 3 commits are unpushed. Required local gate families pass; independent re-review of the new head remains owed.

## Linked Issue / roles

Relates to #665.

Executor: `[A572]`
Internal cleared-context reviewer: `[R564]`
External reviewer: `[R565]`

## Description

Add the opt-in portable AECP owner, mailbox adapter and composed application bridge. Serve the generated descriptor model, mandatory AEM/MVU commands and notifications, saved maps/scalars, interface-specific registrations and response-before-notification ordering. The default fabric ownership and shipping image remain unchanged.

Round 2 corrected root descriptor configuration, current SET_STREAM_INFO fields, retry scheduling, cross-instance callback guards, non-AEM responses and real ADP available_index observations. R564-2 resolved all prior findings but identified one MINOR evidence gap, addressed below.

## Round 3

A SET_STREAM_INFO without MSRP_ACC_LAT_VALID returns current latency and changes no state. The previous test and differential sent the same latency already stored, allowing request-echo and unintended-store defects to escape.

- Send request 765432 against saved 123456 in the native flag loop; separately test observed 12345 and saved 123456, with flags 0/4/8/12.
- Check response latency, the complete store, saved override, callback silence and absence of peer notification.
- Grade the differential's request 765432 against current 67890. Echo requested latency only for a successful valid-latency subcommand.
- Kill both exact R564-2 plants with both named native tests. Add a notification plant and a wire request-echo control with a required diagnosis.
- Document the exception under IEEE 7.4.15.1 and Milan 5.4.2.9.

Production code is unchanged in Round 3. All four linked load images match Round 2 byte for byte; maximum RAM span remains 221728 bytes including the 8192-byte stack reservation.

## Authoritative references

- Issue #665 assignments 6081266905, 6085423196 and 6086491737; budget ruling 6081705916.
- PR #700 review R564-2, comment 6086483772, finding F1.
- Issues #678, #653 and #637; processor #69 and #73.
- REQUIREMENTS section 1; FR_NFR NFR-SCOUT-02/03/08; MAILBOX_SPLIT.
- IEEE 1722.1-2021 6.2.2.15, 7.2.1, 7.4, 7.4.15.1, 7.5, 9.2.2.4, 9.4.4/.5, 9.5.4/.5, 9.6.4 and 9.7.4.
- Milan v1.2 5.4, especially 5.4.2.9 and 5.4.5.2/Table 5.22.

## How to get into the same state

After the authorized owner publishes the candidate:

```sh
git fetch origin 665-f5-aecp
git checkout --detach fb9c57d2ae3484804ff90f67feb57bf420c93dfa
git submodule update --init --recursive
```

Use disk-backed `F5_SCRATCH`, the pinned simulation executable, RV32 compiler and freestanding runtime archives recorded in the evidence packet. `PACKET` names that packet.

## How to validate

```sh
export TMPDIR="$F5_SCRATCH" PYTHONDONTWRITEBYTECODE=1 VERILATOR_JOBS=2
timeout 560 python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --jobs 4 --build-dir "$F5_SCRATCH/firmware"
timeout 560 python3 -B sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep "$F5_SCRATCH/coverage" --lwsrp third_party/lwSRP
timeout 560 python3 -B sw/firmware/ctrl/test/aecp_mutants.py --shard "$PART" 2 --output "$F5_SCRATCH/mutants-$PART"
timeout 560 python3 -B sw/mailbox/gen_mailbox.py --check
```

Run mutation `PART=0,1`. `ROUND3-REPRODUCE.md` records the full wire, mailbox, builder, docs, unchanged-probe, sanitizer and four-link commands. `round3/commands.json` retains exact argument vectors and return codes.

Expected: all gate commands return zero; 1408 firmware checks, Q1-Q5 passing at both interface counts, all 72 source plants caught, 100% raw coverage in all eight AECP/application units, and 70 tests per sanitizer arm. Wire grading covers 132/137/137 records and seven oracle controls per ingress. Both review latency plants fail both `Core.SetStreamInfoReportsCurrentFieldsOnSuccessAndRefusal` and `Core.SetStreamInfoWithoutSubcommandPreservesState`. HANDOFF.md contains the test-to-defect, coverage, gate and size tables.

## Known limitations / out of scope

- Builder gate 11 resource calibration is explicitly unexecuted because its historical placed-utilization report is absent.
- Physical timing calibration, routed memory fit and complete stack bounds remain integration work. The 224000-byte budget passes; 32-bit tile packing still requires owner attention.
- Processor #73's common command model remains owed.
- The linked composition is an opt-in size/ABI fixture; the shipping image is unchanged.
- Assignment-required local gates pass. Publication, the full merge verification bar, hosted checks, independent re-review and candidate-merge validation remain owed.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

