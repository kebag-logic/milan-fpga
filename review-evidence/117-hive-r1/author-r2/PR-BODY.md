[A373] Refs #117

## Status

Round 2 documentation committed at `ecd36018a29f605efe790d33dd50382aec9c1201`; all eight assigned gates pass. Item 4's include-directory inventory is in the packet addendum. The round is under independent re-review.

## Description

The owner replaced the Hive desktop prerequisite with headless la_avdecc enumeration on 2026-09-27. Three fresh runs on the assigned image returned both IEEE 1722.1 and Milan compatibility, with identical static descriptor trees and no complaints or warnings. The findings page records those results and reconciles the superseded 2026-09-23 FAIL with the newer image's PASS. Every other NOT RUN line is unchanged.

| Measurement | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| IEEE 1722.1 library compatibility | PASS | PASS | PASS |
| Milan library compatibility | PASS | PASS | PASS |
| Complaints / warnings / query errors | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| Descriptors / types | 41 / 14 | 41 / 14 | 41 / 14 |
| Enumeration time | 234 ms | 229 ms | 169 ms |
| Process return code | 0 | 0 | 0 |

## How to reproduce

The [public round-1 packet](https://github.com/kebag-logic/milan-fpga/tree/557087b34479c9ba0f1fc1722b6e577a0ecc3998/review-evidence/117-hive-r1) contains the probe source, complete build flags, library revision, identity transcripts, three full entity dumps and logs, comparison script and SHA-256 manifest. Use `MANIFEST.json` to map recorded hashes to published bytes; the three entity dumps have masked serial fields. Use its README for bounded bench commands and `python3 tools/summarize.py` for the offline comparison. The [owner assignment](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5858063707) identifies the image.

## How to validate

Run the eight assigned documentation gates from the physical lane path. All eight returned rc 0 at `ecd36018a29f605efe790d33dd50382aec9c1201`; exact commands and output are in `gate-1.txt` through `gate-8.txt`. The em-dash gate checked 161 added lines against `2a2a7bb6`. `evidence-checks.txt` verifies the ten B4 table hashes and the unchanged NOT RUN rows.

## DoD

The round-1 identity matched on UART and AECP. Entity `020000fffe000001`, model `001bc5c40236ba0e`; VERSION `00020060`, ROM CRC `9b6576a9`, bitstream CRC `3c18c276`, AEM CRC `93742dd2`. Library `v4.3.1.1`, revision `6d61a92e7f264c69f23cdc38f50d31114e567aa0`. No binds or prohibited bench actions; temporary files removed and lock free. This records library compatibility only. Acceptance box 4 still has unmeasured rows. Round 2 publication and independent re-review remain with the coordinator.

## Round 2

The [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5858871629) takes four documentation and packet corrections:

1. Pin the public B4 packet and list the three serial-masked dump hashes with their `MANIFEST.json` mapping (R358-1 F1 / R359-1 F1).
2. Retain the 2026-09-23 `ede8d48e` Milan FAIL as a superseded dated record; box 4 now uses the `9e9954e9` PASS. #534 closed #529, and merge `50e78097` is in the newer image's ancestry, likely explaining the change. Behave hardware tier, latency (#64/#213), and audio continuity deferred to 2026-12-31 remain NOT RUN (R359-1 F2 / R358-1 S1, S2).
3. Name the full probe define and library option set at `6d61a92e`, and condition the no-warnings result on those defaults, including `IGNORE_INVALID_CONTROL_DATA_LENGTH` (R358-1 S3 / R359-1 S2).
4. Add the include-directory description separately as `PACKET-ADDENDUM.md`; its inventory is awaiting an existing receipt (R359-1 S3).

No new bench measurement was performed. The round-1 packet remains unchanged. The summary-script suggestion is outside this assignment.
