# [A830] REVIEW READY: milan-fpga #983, descriptor-only host profile

Commit: `677d605f37c3a80654df1dd2cde053b57242845b` (`pf-linuxprof-1`, on `dev-soft-core` `854bd723`). Local, not pushed.
PR description: [PR-BODY.md](PR-BODY.md). Evidence: [receipts/INDEX.md](receipts/INDEX.md).

Changed:

- `sw/builder/endstation_builder.py`: `board.target: host`, with its own board, gPTP and interface loaders and no SoC, fabric blocks or render lane. All other checks are the FPGA path's. `build()` refuses the profile. An FPGA target naming `board.gptp_owner` is refused.
- `configs/host/endstation_host_example.yaml`: the first user's inventory (AAF in, CRF in, AAF out; ADP 1/2).
- `sw/firmware/ctrl/loop/ctrl_loop.h`: a `(1, 1, 2)` row under `CTRL_HOST_PLATFORM` only. Its figures are 1x1/1if's, held as a stated host scheduling profile. FPGA rows untouched.
- `sw/builder/test_builder.py`: gates 41 (generators, image, shape row, section 6 key map) and 42 (28 planted defects).
- `docs/ENDSTATION_BUILDER.md`: section 6, row 5d, corrected section 3 counts.

Validation at the head:

| Check | Result |
|---|---|
| FPGA artifact identity, 5 configs x 2 placements, builder + image + 4 firmware generators + tracked generated files | 170/170 byte-identical; tracked tree clean |
| Builder suite (`test_builder.py --require-rv32`) in four subsets | 114/115 pass, each once; 1 NOT RUN row (gate 11 calibration report absent); gate 1b not completed (10-minute command bound) |
| Gates 32, 41, 42 | pass: 116 == 116 keys; host profile feeds 3 generators and the image; 28/28 defects refused |
| Docs and quality gates (24, incl. docs_check, em-dash vs base, bare-metal scope + self-test, py/C/sh idiom, ratchets, entity shape, wire accountability, NVM) | 24/24 pass |
| `ctrl_loop.h` preprocessed at base and head (no header, 1x1, 8x8, 3 Arty) | identical; Arty refused at both, `#error` line 397 -> 424 only |
| Firmware arms on the gate's tree: service bounds + every-shape SRP (RV32), AECP, platform | 21 + 18 + 8 pass |

Acceptance criteria (#983):

- Profile generates a descriptor image and ADP fields that pass the generators' AEM checks: met (gate 41).
- FPGA artifacts' identity gate passes: met (170/170).
- ENDSTATION_BUILDER describes the profile: met (section 6).

Open risks and questions:

- The host shape row's justification is a stated profile, not a host or board measurement.
- Gate 1b and the firmware mutation shards are owed to the hosted run.
- The bare-metal scope (#259) shaped the vocabulary. A reviewer should confirm that a host profile in the generators is within #259's intent; the issue's authorization says so.
