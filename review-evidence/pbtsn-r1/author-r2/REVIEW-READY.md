# Review ready: tsn-c-stack PR #43, round 2

Head `40c3111` on `pocket-beagle`. Base `main` bf02d81, merged in at 70a437f. Issue #42 (AEM-01).

## Findings and their outcomes

| Review | Finding | Outcome | Where |
| --- | --- | --- | --- |
| internal F1, external F3 | AEM-01 traced to the import baseline | `ADDITIONAL_ORIGINS` and `requirements.json` give the origin "tsn-c-stack issue 42". REQUIREMENTS says "AEM-01 originates from issue #42". TRACEABILITY row 58 links issue 42. | ee3c173 |
| internal F2, external F4 | Untested refusals for the AAF format code, samples per frame, subtype and its high bit, reserved bits; the absent input's bound | `Pbaem.AafFieldRefusals` refuses `0x0205012002006000`, `0x020502200200c000`, `0x0305022002006000`, `0x8205022002006000` and `0x0205022002006001`. `Pbaem.AbsentInputRefusesEverything` checks input 5 refuses every AAF format and that a refused set leaves the model whole. Plants: `pbaem-ignore-format-code`, `-ignore-samples-per-frame`, `-ignore-subtype`, `-ignore-subtype-high-bit`, `-ignore-reserved`, `-absent-input-bound`, all caught. | 9e2a466 |
| external F5 | Identity only asserted for short strings and one model ID; held state | `PbaemIdentity.FullWidthStringsAndModel` uses four unterminated 64-octet strings and model ID `0x0123456789abcdef`. `Pbaem.InitResetsHeldState` re-initializes a model that held state. Plants: `pbaem-name-truncated`, `-firmware-truncated`, `-group-truncated`, `-serial-truncated`, `-model-id-constant`, `-init-keeps-state`, all caught. | 9e2a466 |
| internal F3, external RES-1 | RV32 gate says "three cores" | The source check says "all three cores and the AEM model". The smoke summary names the entity and PocketBeagle AEM image checks. | b03d499 |
| external F1 | Wrong Milan clause numbers | Corrected against the Milan v1.2 contents: 5.3.3.4 (streams), 5.3.3.5 (AVB_INTERFACE), 5.3.3.6 (CLOCK_SOURCE), 5.3.3.7 and 5.3.3.9 (stream ports), 5.3.3.10 and 5.3.12 (IDENTIFY), 5.3.3.11 (CLOCK_DOMAIN). `named` cites IEEE 1722.1-2021 7.3.7. | 9d06d80 |
| external F2, internal S7 | LOCALE `en-EN` invalid | `en-US`, set in the generator configuration and the model together. The regenerated image and the model are again identical, 84 of 84. Golden CRC 0xd891cd2f. The hash-derived model ID is unchanged. The board config change is handed to the BSP lane. | 9d06d80 |
| external F6 | #41 exemption undocumented | Taken from main's PR #44 by the merge: IMPORT.md:137 and VERIFICATION.md:43 name both merges, and the self-test checks each (closes S3/S4). | 70a437f |
| external F7 | The page cites a configuration and suites not at the named place | POCKETBEAGLE.md now says the 4x4 configuration and its suites are not yet published, and marks those clause rows "not yet published". The image evidence is milan-fpga 58f7673b and the facts on the page, with the golden's identity and CRC. | 40c3111 |
| external RES-2 | "Base format of 1 to 8 channels" | "Each 48 kHz PCM32 AAF format of 1 to 8 channels with six samples per PDU, which includes every 48 kHz Base format", in REQUIREMENTS, requirements.json, the page and the changelog. | ee3c173, 40c3111 |

## Suggestions taken

- Internal S1: the mapped-channel refusal is attributed to the firmware's AECP.
- Internal S2: the golden's provenance is stated.
- Internal S4 and external S1: a PORTING section states the model's contract and stack use.
- Internal S5: `<cstdio>` is included.
- Internal S6 and external S5: dumps are keyed by each descriptor's own header.
- External S2: DEV-01.

Not taken: external S3. It concerns the generator's defaults, which are milan-fpga's to change.

## Gates at 40c3111

| Gate | Result |
| --- | --- |
| `validate.py` (CI replica: Ubuntu 24.04, Clang 18.1.3, GoogleTest 1.14.0) | 27/27 rc 0 |
| Mutation campaign | 550 caught, 0 escaped, 0 error (27 `pbaem-`) |
| `baremetal.py` | Debug and Release rc 0, with the AEM golden |
| `render_graphs.py` (host) | 5 rendered |
| Privacy | 107 commits, pass |

Receipts: `receipts/round2/`.
