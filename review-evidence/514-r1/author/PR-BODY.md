[A246] Separate historical linear inclusion from optional current retention

Closes #514

## Status

Implementation ready for independent review at `20b7bdaa307eba722ec6cc89d2683ba1636a0cb6`. Local commits only; publication and the remaining merge workflow are pending.

## Description

An exact linear replay followed by a revert still returns `contained/0`, preserving the decided historical-inclusion policy. Add `--current-retention` to request a separate `retained` or `UNKNOWN` result using #423's unchanged raw-entry and no-op three-way merge criterion. Diagnostics and the containment documentation identify the claim each result makes.

The optional arm requires a nonempty source-only linear range and distinct exact replays. Ancestry-only, squash-only and merge-shaped histories remain unsupported by this arm. Unmeasurable or unproved retention returns `UNKNOWN/1`; declared supersession intent does not supply proof.

## How to reproduce

Run the unchanged fixture 30 and `linear-patch-fallback`: both remain `contained/0`. Adding `--current-retention` reports `UNKNOWN/1`, naming `mod.txt` and `linear` respectively. The public baseline receipts are reproduced in the author handoff.

## How to validate

Run `python3 scripts/check_merge_containment.py --selftest`. It includes the original controls and the new executable retention examples, guard mutations, mode/kind boundaries, unsupported histories and measurement failures. Run the assigned docs gates in both discovery modes, em-dash against `3d2f3e3131c9db5898e1db9dd3e2a35149843109`, Python idiom and diff checks. Publish raw self-test and gate results as a separate evidence comment.

## DoD

- Historical verdicts and existing expectations preserved.
- Optional retention proof, explanatory diagnostics and authoritative wording implemented.
- Required positive/negative examples and mutation sensitivity included.
- Assigned local gates pass; independent review and the remaining hosted, candidate and merge workflow are still required.
