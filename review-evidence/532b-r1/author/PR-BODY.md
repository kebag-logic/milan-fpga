[A331]

Relates to #532

## Status

Ready for independent review. The live proof reruns after merge.

## Description

When `pasta` is a symlink to `passt`, resolving the executable path changes
its invoked name and selects the wrong mode. Slot uplink startup then fails.

Preserve the absolute `pasta` path found on `SAFE_PATH`. Every other host tool
keeps its resolved path. Document the rule and add seven offline regression
checks using a fake executable reached through a real symlink.

## How to reproduce

Use a multi-call executable named `passt` with a `pasta` symlink.
The previous lookup launches it as `passt`; the corrected uplink launches
it as `pasta`.

## How to validate

Run `python3 -I scripts/act_ci.py --selftest` and
`bash scripts/act_slot_proof.sh --selftest`, followed by the assigned CI,
documentation, style, and diff gates. All required offline gates passed.
The resolving-path mutant fails the full self-test on the regression checks.
Detailed evidence is recorded in the issue's REVIEW READY comment.

## DoD

- Assignment items 1-2 implemented and checked offline.
- Independent reviews pending.
- Item 3: manager reruns the live proof from the trusted merged runner.
- Issue #532 stays open until that live proof succeeds.
