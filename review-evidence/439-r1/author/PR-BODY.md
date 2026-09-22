[A181]

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

Source ready for independent review and manager integration; unpublished at `f01f237d4b48c7b1ed59c80aca51430901791624`, tree `ff1c54c52cbb196db754ce6999c661730a3d0e94`, based on `483a133ed08867ea0d300d2b4a027b5b48a4282f`. Target: `439-rtl-script-content-pins` -> `dev`. Full local/hosted and current-dev candidate evidence remain manager-owned.

## Linked Issue / roles

Closes #439
Relates to #407
Relates to #504

Executor: `[A181]`
Internal cleared-context reviewer: `[R254]` reserved
External reviewer: `[R255]` Opus reserved, availability pending

## Description

Recognized RTL scripts could change while sequence checks stayed green. The sibling SHA-pin step also accepted deletion of its checkout mismatch assertion. Canonical records now hold all 38 scoped run bodies, with refusals naming the job, step and first differing normalized line.

The default self-test adds per-line and record controls, retaining all prior populations. Matching script/record maintenance is tested. CI_WORKFLOWS states the resulting coverage and maintenance contract. Workflows, specialized pins, normalization and budgets are unchanged.

## Authoritative references

REQ-VER-01/02/04; CONTRIBUTING.md; CI_WORKFLOWS items 4, 7, 11, 12 and One authoritative SHA; the [settled scope decision](https://github.com/kebag-logic/milan-fpga/issues/439#issuecomment-5772547851) and [source/integration assignment](https://github.com/kebag-logic/milan-fpga/issues/439#issuecomment-5782501927).

## How to get into the same state

This is an unpublished source draft. The manager supplies/publishes the source and records the later integrated candidate separately. Verify the source at the exact head above before reproducing these source gates. Use the repository's existing Python and required pinned dependencies; no installation change is part of this PR.

## How to validate

```sh
rtk proxy python3 scripts/ci_events.py --check
rtk proxy python3 scripts/ci_events.py --selftest
rtk proxy python3 scripts/docs_check.py
rtk proxy python3 scripts/check_em_dash.py --base 483a133ed08867ea0d300d2b4a027b5b48a4282f
rtk proxy python3 scripts/gen_toc.py --check
rtk proxy python3 scripts/gen_toc.py --verify-anchors
rtk proxy python3 scripts/check_py_idiom.py
rtk proxy python3 scripts/measure_test_evidence.py --check
rtk proxy python3 scripts/measure_fail_fast.py --check
rtk proxy python3 scripts/check_todo_ownership.py
```

Expected: no new findings; ci_events reports 1589 contract items and 2135 self-test arms. The author evidence comment supplies raw baseline/corrected counts, gate self-tests, wiring mutations and integrity. After integration, the manager records the actual candidate counts and complete local/hosted bar.

## Known limitations / out of scope

The source starts from dev483. #504/PR521 edits distinct non-RTL carrier SDK policy in the same files; its later composition requires current-dev validation and fresh applicable review. Product RTL/firmware, processor pins, hardware, workflow scheduling, carrier provisioning and budgets remain outside #439.

## Definition of Done

- [x] Source acceptance criteria have executable controls
- [x] Changed behavior has self-checking tests
- [x] Authoritative coverage and maintenance documentation updated
- [ ] Complete required local verification bar passes on the candidate
- [ ] Self-test evidence posted in a PR comment
- [ ] Internal cleared-context review positive
- [ ] External review positive
- [ ] All findings resolved and applicable lenses covered at the candidate
- [ ] No review round remains in flight
- [ ] Current-dev candidate merge result validated
- [ ] Required hosted contexts successful
- [ ] Authorized merge and post-merge containment complete
