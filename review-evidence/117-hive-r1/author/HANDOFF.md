[A373] Bench handoff

Refs #117

Status: REVIEW READY. Commit `bcba79a50ecd2eca99db91c4f3802d888eaac7e4` on `117-la-avdecc-enum`, based on `2a2a7bb655e528edc3087c88033cd3a47546feb4`. The worktree is clean. No push or PR operation was performed.

Assignment: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5858063707
TAKEN: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5858076185
REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5858184304

Commit subject: `Record headless enumeration replacing the issue 117 Hive check`

Only `docs/findings/117_GPTP_SILICON_EVIDENCE.md` changed: the two Hive rows and B4. Every other original NOT RUN line is byte-identical. Product-image source is `9e9954e96bf55181edb9949ae94c9abd4ab6aaf5`; its diff to the lane base contains documentation/evidence only.

| Measurement | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| IEEE 1722.1 library compatibility | PASS | PASS | PASS |
| Milan library compatibility | PASS | PASS | PASS |
| Complaints / warnings / query errors | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| Descriptors / types | 41 / 14 | 41 / 14 | 41 / 14 |
| Enumeration time | 234 ms | 229 ms | 169 ms |
| Process return code | 0 | 0 | 0 |

Identity PASS: assigned bitstream SHA-256 `1696d1ea7568b2cf3cd536b1d34488e1ce7702e4a79e7cf3aca2c6ed6a54d2c7` and AEM SHA-256 `9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404`. UART, 17:26:15 to 17:26:38 UTC: VERSION 00020060, ROM CRC 9b6576a9, QSPI payload CRC 3c18c276, AEM CRC 93742dd2. AECP ENTITY and CONFIGURATION descriptors match the AEM templates byte-for-byte. Entity 020000fffe000001, model 001bc5c40236ba0e, firmware 2.96.0. This is CRC consistency readback, not configuration SHA-256 readback.

All three fresh 12 s runs have identical static descriptor trees and compatibility verdicts. Library `v4.3.1.1`, revision `6d61a92e7f264c69f23cdc38f50d31114e567aa0`; runtime 4.3.1-beta1. Probe source SHA-256 `ac552f67c8b769e0cfc46d0b80c4e9ece0c9da1811020d2c497e2f904749a623`. Full flags, binary hashes and sizes are in build-provenance.txt. All 41 descriptors and their indices are retained in the three entity dumps and inventory files.

Validation: all eight assigned gates returned 0 from `$LANES/117-la-avdecc-enum`. Exact commands/output are in gate-1.txt through gate-8.txt. The em-dash gate was rerun at the committed head, covering 116 added lines. The committed base-to-head diff also passes `git diff --check`. validation-head.txt ties the remaining gate results to unchanged committed bytes. Initial failures and fixes are disclosed in VALIDATION-NOTES.md.

Bench state: no lock held; availability check returned 0. No enumeration process remains, and temporary controller files were removed after size/SHA-256 checks. No binds, CSR writes, flash, power, wiring or instrument operations. Final UART SYNC=1, ASCAPABLE=1, TU=0. Link selection used carrier and route state, then successful DUT AECP replies. Raw-socket AECP joined 91:E0:F0:01:00:00.

Packet: README.md describes artifacts and reproduction. MANIFEST.sha256 covers every retained file except itself. No binary toolchains, dependency copies, environments or files above 200000 bytes are retained. The single interface-name substitution is documented by original and retained hashes in redaction.json. Enumeration logs and DUT entity JSON retain recorded bytes.

Next owner: coordinator publishes the local commit and packet and arranges independent review. PR-BODY.md is prepared and starts with Refs #117. This scoped evidence does not close acceptance box 4 or #117. No further bench action is pending.
