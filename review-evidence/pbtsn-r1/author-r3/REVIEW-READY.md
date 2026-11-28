# Review ready: tsn-c-stack PR #43, round 3

Head `ebaac61` on `pocket-beagle`. Base `main` bf02d81, merged in at 70a437f. Issue #42 (AEM-01). Round 3 is two commits on round 2's head, 40c3111.

## Findings and their outcomes

| Review | Finding | Outcome | Where |
| --- | --- | --- | --- |
| internal 7238076326 F1, external 7238106277 F1 | Bits 53 to 55 of the AAF format word are refused by the code but tested by nothing. The plant claim "every format field" / "field by field" is overstated. | `Pbaem.AafFieldRefusals` refuses `0x0225022002006000` (bit 53), `0x0245022002006000` (bit 54) and `0x0285022002006000` (bit 55), each on every AAF input under its own message. Plants `pbaem-ignore-reserved-bit-53`, `-54` and `-55` each drop one bit from both sides of the comparison. Each is caught by its own assertion, "reserved bit 5x of the rate octet is refused". The fields that had an assertion but no plant now have plants: `pbaem-ignore-bit-depth` (caught by "24-bit depth is refused") and `pbaem-ignore-ut` (caught by "the family entry is not a stream format"). Counts updated: CHANGELOG (thirty-three, with the fields named), VERIFICATION (551 core plants), TESTS, PR body (33, 556). | 9a0de3c |
| both, RES-1 | The packet names a receipts directory that is published as `receipts-round2/` | `round2/HANDOFF-r2.md`: "Receipts are in `../receipts-round2/`". This file is rewritten and names no round directory; receipts are listed in `receipts/INDEX.md`. | packet |

The plant claim now matches the plants. Each field of the format word has at least one plant: subtype, its high bit, rate, the up-to bit, reserved bits 53, 54 and 55, format code, bit depth, channel count (zero and nine), samples per frame, and the low reserved field (bit 0 and bits 1 to 11).

## Suggestions taken

- Internal S1: reserved bit 11 is refused, plant `pbaem-ignore-reserved-bit-11` (bits 1 to 11 dropped), caught by "reserved bit 11 is refused".
- External S2: a loop flips each of the 54 bits outside the channel count of a valid format and expects a refusal.
- Internal S2 and external S1: POCKETBEAGLE.md gives the golden's full identity: clock identity equal to the entity ID, and empty serial number and group name.
- Internal S3: regenerating needs milan-fpga's `protocol-processor` submodule at `801ef228`. Checked against the public 58f7673b tree.
- External S4: `pb2-aecp-1` is the only public branch of the board support repository with an end-station configuration. Checked against every public branch's tree today.

## Gates at ebaac61

| Gate | Result |
| --- | --- |
| `validate.py` (CI replica: Ubuntu 24.04, Clang 18.1.3, GoogleTest 1.14.0) | 27/27 rc 0 |
| Mutation campaign | 556 caught, 0 escaped, 0 error (33 `pbaem-`, 6 new) |
| Coverage, `src/pbaem.c` | 224/224 lines, 103/103 branches |
| `baremetal.py` | Debug and Release rc 0, with the AEM golden |
| `render_graphs.py` (host) | 5 rendered |
| Privacy, after the commits | 109 commits, pass; self-test 17 controls pass |

The model, its golden CRC 0xd891cd2f and the model ID are unchanged.

Receipts: the round 3 section of `receipts/INDEX.md`.
