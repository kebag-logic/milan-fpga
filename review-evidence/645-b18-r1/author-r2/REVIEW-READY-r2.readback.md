[A622] REVIEW READY (round 2, PR #747)

Commit: `b3f7a696713a96b42265e08a8c3a04a430b7b5ed` on branch `645-b18-bench`, one commit on `480c5e91`. It is not pushed: origin's branch is still `480c5e91`.

Changed: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` only, +35 / -12 lines in the section "Dev 9ef71772, 2026-10-15: lane B18". The [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6200530754) asked for these four items:
- **R635-1-F1.** The image paragraph in "B18: identity and setup" links the manager's [provenance record](https://github.com/kebag-logic/milan-fpga/tree/bbc53aabb02a1654812ba2eaa1642f5e36e69ce0/review-evidence/645-b18-r1/manager-provenance) at `bbc53aab` and the [chain comment](https://github.com/kebag-logic/milan-fpga/pull/747#issuecomment-6200503436). It now states:
  - the source dev merge `9ef71772`, which carries PR #742;
  - bitstream SHA-256 `4b5a391af524cb3b490099381c0fd9e3275383fc51c163a75fb78cdb054ffcca` and the AEM descriptor SHA-256;
  - the verified flash-pair, `FLASH_RC=0`;
  - the cold power cycle, `POWERCYCLE_RC=0`, with no fallback;
  - the boot line;
  - that the identity reads ran from 18:50:11 UTC, after that boot, and no flash or power cycle came before the last cycle ended at 18:59:53 UTC.

  The statement that no device read distinguishes the two images is kept.
- **R634-1-S1.** One clause: in c01 and c10 the last poll fell 0.05 s short of B17's shortest, +31.75 s. That came from poll timing, and the counter is cumulative over the tail.
- **R634-1-S2.** "the design's earliest firing time" in the method, the bursts paragraph and the limits.
- **R634-1-S3.** The page names the published packet, `review-evidence/645-b18-r1/author` on branch `645-b18-review-evidence`, commit `2e913519`.

No figure, grade or table cell changed. There was no bench access.

Validation: run at `b3f7a696`, all rc 0, none piped:
- `docs_check.py`
- `check_doc_style.py`
- `gen_toc.py --check`
- `check_em_dash.py --base 9ef71772` (338 added lines, 0 findings)
- `check_doc_paths.py`
- `check_baremetal_only.py --check`
- `git diff --check 9ef71772 HEAD`

Acceptance criteria: met, unchanged from round 1. All ten binds held, with 0 #743 residuals and 0 class (c) slips. The image identity is now linked to public provenance.

| Cycle | Bind, UTC | Polls, s from the bind | `SLIP_LB` dups, skips | Grade | First peer PDU, ms | First burst over 20 us: s, peak | CLOCK_SOURCE DUT, peer |
|---|---|---|---|---|---|---|---|
| c01 | 18:50:56.251 | 80, -8.00 to +31.70 | 0, 0 to 0, 0 | Held | 135.267 | 4.74, 25.7 us | 0 to 0, 1 to 1 |
| c02 | 18:51:59.961 | 80, -8.00 to +31.84 | 0, 0 to 0, 0 | Held | 25.015 | 4.03, 25.1 us | 0 to 0, 1 to 1 |
| c03 | 18:52:51.821 | 80, -8.00 to +31.83 | 0, 0 to 0, 0 | Held | 165.076 | 0.38, 25.8 us | 0 to 0, 1 to 1 |
| c04 | 18:53:43.565 | 80, -8.00 to +31.78 | 0, 0 to 0, 0 | Held | 20.959 | 0.44, 26.2 us | 0 to 0, 1 to 1 |
| c05 | 18:54:46.633 | 80, -8.00 to +31.88 | 0, 0 to 0, 0 | Held | 153.259 | 2.38, 25.7 us | 0 to 0, 1 to 1 |
| c06 | 18:55:38.529 | 80, -8.00 to +31.85 | 0, 0 to 0, 0 | Held | 57.238 | 2.50, 29.0 us | 0 to 0, 1 to 1 |
| c07 | 18:56:30.394 | 80, -8.00 to +31.84 | 0, 0 to 0, 0 | Held | 192.267 | 2.64, 26.8 us | 0 to 0, 1 to 1 |
| c08 | 18:57:27.295 | 80, -8.00 to +31.77 | 0, 0 to 0, 0 | Held | 91.662 | 0.20, 27.6 us | 0 to 0, 1 to 1 |
| c09 | 18:58:19.017 | 80, -8.00 to +31.77 | 0, 0 to 0, 0 | Held | 170.932 | 0.25, 24.9 us | 0 to 0, 1 to 1 |
| c10 | 18:59:10.797 | 80, -8.00 to +31.70 | 0, 0 to 0, 0 | Held | 189.988 | 3.26, 25.3 us | 0 to 0, 1 to 1 |

The PR body's round-2 section lists the same items and keeps the manager's RS1 counter sentence.

Open risks/questions: none. These are operator observations, not a review verdict.

