Status: REVIEW READY, 2026-11-28 11:55. tsn-c-stack `pocket-beagle` head ebaac61. Round 3 closes the shared MINOR finding of both round-2 re-reviews (internal 7238076326 F1, external 7238106277 F1) and applies both RES-1 fixes.
ETA: none outstanding for this round. Nothing pushed or posted.

## What changed since 40c3111

| Commit | Content |
| --- | --- |
| 9a0de3c | `Pbaem.AafFieldRefusals` refuses each of bits 53, 54 and 55 set alone (`0x0225022002006000`, `0x0245022002006000`, `0x0285022002006000`), reserved bit 11 (`0x0205022002006800`), and every one-bit change outside the channel count (54 bits, one loop). Six new plants, each caught by its own named assertion: `pbaem-ignore-reserved-bit-53`, `-54`, `-55`, `pbaem-ignore-reserved-bit-11`, `pbaem-ignore-bit-depth` ("24-bit depth is refused") and `pbaem-ignore-ut` ("the family entry is not a stream format"). CHANGELOG now names the fields the 33 plants cover. VERIFICATION says 551 core plants. TESTS and TRACEABILITY regenerated. |
| ebaac61 | POCKETBEAGLE.md: the golden's full identity (clock identity equal to the entity ID, empty serial number and group name). The generator needs its `protocol-processor` submodule at `801ef228`. Only `pb2-aecp-1` of the board support repository's public branches holds an end-station configuration, and it has the one-input shape. I checked this against the public branch trees today. |

## The plant claim, corrected

With these plants, every field of the AAF format word has at least one plant: subtype, its high bit, rate, the up-to bit, reserved bits 53, 54 and 55 one by one, format code, bit depth, channel count, samples per frame, and the low reserved field at bit 0 and at bits 1 to 11. The CHANGELOG and the PR body list those fields instead of saying "field by field". The internal review's alternative (narrowing the claim) was not needed, because steps 1 to 3 of its required outcome were all taken.

## Residues and suggestions

- RES-1 (both reviews): `round2/HANDOFF-r2.md` now says "Receipts are in `../receipts-round2/`". REVIEW-READY.md is rewritten for this round. It no longer names a round-2 directory, and it points to `receipts/INDEX.md` for receipts.
- Taken: internal S1 (bit 11), external S2 (the one-bit loop), external S3 and internal step 2 (bit-depth and up-to plants), internal S2 / external S1 (golden identity), internal S3 (submodule), external S4 (branch name).

## Gates at ebaac61's tree, run in the CI replica (Ubuntu 24.04, Clang 18.1.3, GoogleTest 1.14.0)

- `validate.py`: 27 of 27 gates rc 0.
- Mutation campaign: 556 caught, 0 escaped, 0 errors. All 33 `pbaem-` plants are caught, including the six new ones.
- Coverage: `src/pbaem.c` 224/224 lines, 103/103 branches.
- `baremetal.py`: Debug and Release rc 0, with the AEM golden.
- Privacy gate, re-run after the commits: 109 commits, pass. Self-test: 17 controls pass.
- Graphs: 5 rendered, on the host.
- I ran the kit on the working tree just before committing it. The two commits hold exactly that tree, and the tree is clean.
- Receipts: see the round 3 section of `../receipts/INDEX.md`.

## Board-facing

No entity or model change this round: the descriptors, the golden CRC 0xd891cd2f and the model ID are unchanged. Nothing new goes to the BSP lane.

## Open (manager)

- External review pending duties: link the evidence commit where the packet is cited, and confirm the round-1 packet files' "Private" lines and the handoff's line 2 are meant to be public.
- Publish the round-3 PR body (PR-BODY.md) when posting is authorized.

No board or bench device was touched by this lane.
