[A330]

Closes #567

## Status

Prepared for independent review at `c9484ac8e86cb33d1120471530f9e1762bd4af1f`. The assigned Round 2 local gates pass.

## Description

Advance the protocol processor from `990f9652` to `0922e434`. The adopted changes record the October MVU waiver and unsupported-command responses, including under lock, and complete the integration parameter inventory with its consistency checker.

Refresh the parent pin references, adoption notes, changelog, submodule diagram and image manifest. Processor HDL and parent RTL are unchanged.

## Round 2 ledger

The [public decision](https://github.com/kebag-logic/milan-fpga/issues/567#issuecomment-5845149786) requires exact-pin ledger rows even when the ROM bytes are unchanged.

The repository recorder adds two rows for `0922e434`. Both ROM digests exactly match `990f9652`; all 37 existing rows and the header are preserved. This round changes only the ledger.

The inherited statements at `CHANGELOG.md:44` and `docs/reference/SUBMODULES.md:53,57` still describe the earlier unresolved ledger decision. They remain for review because this round explicitly permits only the ledger change.

## How to reproduce

Use the candidate commit and initialize the three active imported dependencies at their recorded pins. Re-record the ledger with the repository recorder and compare the two processor-image digests with the previous pin.

## How to validate

Replay the commands in the Round 2 issue evidence and `HANDOFF.md`: the normal OOC processor-wrapper path, the hosted fast job's three integration-top elaboration command, documentation checks with and without metadata, the em-dash check against `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`, and whitespace checks.

## DoD

- [x] Generated exact-pin ledger rows match the previous ROM digests.
- [x] All assigned Round 2 gates return 0.
- [x] The round contains only two ledger insertions.
- [ ] Resolve the inherited documentation consistency gap during review.
- [ ] Complete independent review, hosted gates, merge validation and containment.
