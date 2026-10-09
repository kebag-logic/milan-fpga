[A572]

## Contents

- **[Status](#status)** — Local evidence and remaining review work.
- **[Linked Issue / roles](#linked-issue--roles)** — Assignment and independent reviewers.
- **[Description](#description)** — Opt-in AECP ownership and corrected behavior.
- **[Round 2](#round-2)** — Changes answering both review packets.
- **[Authoritative references](#authoritative-references)** — Requirements and protocol clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Candidate and dependency setup.
- **[How to validate](#how-to-validate)** — Reproducible checks and expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — Integration obligations.
- **[Definition of Done](#definition-of-done)** — Remaining publication and review gates.

## Status

Local implementation head `0ded1f269a44d107498f177c8276665656e07d30`; `665-f5-aecp` -> `dev`.
REVIEW READY: all required local command families return 0. This local head is unpushed; PR #700 remains at the round 1 head. Independent re-review is required.

## Linked Issue / roles

Relates to #665.

Executor: `[A572]`
Internal cleared-context reviewer: `[R564]`
External reviewer: `[R565]`

## Description

Add the opt-in portable AECP owner, mailbox adapter and composed application bridge. Serve the generated descriptor model, mandatory AEM/MVU commands and notifications, saved maps/scalars, interface-specific registrations and response-before-notification ordering. Keep the default fabric ownership and shipping image unchanged.

## Round 2

Answer R565-1 and R564-1 against the protocol clauses:

- Ignore configuration_index for root descriptor reads and return zero.
- Return current SET_STREAM_INFO fields on success/refusal; accept no sub-command and ignore SAVED_STATE/STREAMING_WAIT.
- Retry unavailable snapshots without blocking eligible peers or spinning.
- Guard all 15 public inputs across real callbacks on another instance.
- Acknowledge HDCP commands with an empty NOT_IMPLEMENTED response and document every other message-type decision.
- Observe ENTITY available_index from the real ADP owner; verify N advertisements followed by a read of N.
- Re-link all four shape/interface combinations; maximum RAM span is 221728 bytes, below 224 KB.

## Authoritative references

- Issue #665 assignment comments 6081266905 and 6085423196; budget ruling 6081705916.
- Issues #678, #653 and #637; processor #69 and #73.
- REQUIREMENTS section 1; FR_NFR NFR-SCOUT-02/03/08; MAILBOX_SPLIT.
- IEEE 1722.1-2021 6.2.2.15, 7.2.1, 7.4, 7.5, 9.2.2.4, 9.4.4/.5, 9.5.4/.5, 9.6.4 and 9.7.4.
- Milan v1.2 5.4, especially 5.4.2.9 and 5.4.5.2/Table 5.22.

## How to get into the same state

After the candidate is published, use the recorded commit and initialized pins:

```sh
git fetch origin 665-f5-aecp
git checkout --detach 0ded1f269a44d107498f177c8276665656e07d30
git submodule update --init --recursive
```

Set `F5_SCRATCH` to disk-backed scratch and use the pinned simulation executable,
RV32 compiler and freestanding runtime archives recorded in the evidence packet.

## How to validate

```sh
export TMPDIR="$F5_SCRATCH" PYTHONDONTWRITEBYTECODE=1 VERILATOR_JOBS=2
timeout 560 python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --jobs 4 --build-dir "$F5_SCRATCH/firmware"
timeout 560 python3 -B sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep "$F5_SCRATCH/coverage" --lwsrp third_party/lwSRP
timeout 560 python3 -B sw/firmware/ctrl/test/aecp_mutants.py --shard "$PART" 2 --output "$F5_SCRATCH/mutants-$PART"
timeout 560 python3 -B sw/mailbox/gen_mailbox.py --check
```

Run both mutation partitions. `ROUND2-REPRODUCE.md` records the full wire,
mailbox, builder, docs, unchanged-probe, sanitizer and four-link commands.
Expected: every command returns zero; 1406 firmware checks, 12 unchanged review
probes, all 69 plants caught, 100% coverage in all eight AECP/application units,
and 69 tests per sanitizer arm. Wire grading covers 132/137/137 records and six
oracle controls per ingress. The handoff carries the full test-to-defect,
coverage, gate, clause-difference and size tables.

## Known limitations / out of scope

- Physical timing calibration, routed memory fit and complete stack bounds remain integration work.
- Processor #73's common command model remains owed.
- The linked composition is an opt-in size/ABI fixture; the shipping image is unchanged.
- Publication, hosted checks, independent re-review and candidate-merge validation remain owed.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
