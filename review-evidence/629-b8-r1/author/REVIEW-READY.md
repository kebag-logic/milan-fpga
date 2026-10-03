[A521] REVIEW READY

Head: `4fb5125a2e43997384839deeb1fe4742a5b2dca8` on `629-b8-bench`, two commits on PR #644's head `40714c1b`: `c17997fb` (the first session's STOP) and `4fb5125a` (items 2 to 4 under the [ruling](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5970994127)). Local, not pushed. It completes the section "Dev bbf704ec, 2026-10-03: lane B8" in `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and updates its row in `docs/findings/README.md`; no other file changes. Refs #629.

**Changed:** the section now records items 2 to 4 with per-case tables (THD+N, SNR, frequency offset and discontinuities of the tone path; the servo, meter, slip and render words around every set, unbind and rebind; the GET_COUNTERS marks against the declared values), the tool controls, the identity gate before and after the power cycle, the bench as left, the #629 acceptance re-judged, limits and artifact hashes.

**Per-run tables:**

| Run | Window | Result |
|---|---|---|
| Identity gate, start, resume, after the power cycle | - | PASS each; verdict byte-equal to lane B7's |
| Tool controls | - | PASS, byte-equal to lanes B6 and B7 (run after the cases) |
| Tone proof (first session) | 10 s from 18:05:13 CEST | TONE ABSENT |
| 1. B0, B-CRF, B-AAF by THD+N and SNR | - | NOT RUN: the owner checks the tone's path |
| SW: INTERNAL to AAF (the case's first set) | set 18:32:31; LOCKED 6.64 to 7.14 s; 120 s hold | #645 repeated: `SLIP_LB` +2 at 2.0 to 3.0 s after LOCKED |
| 2. SW: AAF to CRF | set 18:34:38; LOCKED 2.62 to 3.12 s; 150 s hold | PASS |
| 2. SW: CRF to AAF | set 18:37:11; LOCKED 5.96 to 6.48 s; 150 s hold | PASS |
| SW tone path, both switches inside | 417.3 s from 18:32:51 | 0 listener discontinuities; counted ratio 0 (0 net steps in 20,030,400 frames); timed -0.02 +-0.57 ppm |
| B-CRF repeated | 420 s from 18:40:41 (401.3 s captured) | PASS: LOCKED at all 797 polls; counted ratio 0 |
| 3. CRF lock loss | unbind 18:47:42, held 11.04 s | As declared |
| 4. Saved selection across the power cycle | off 18:49:51, on 18:49:59 | PASS: GET_CLOCK_SOURCE 2 after the boot; LOCKED with no command |

| Switch counters | Before | INTERNAL to AAF | AAF to CRF | CRF to AAF | Declared |
|---|---|---|---|---|---|
| DUT AAF talker MEDIA_RESET | 0 | 1 | 2 | 3 | one per source change |
| Peer listener MEDIA_RESET | 0 | 1 | 2 | 3 | as above |
| DUT CLOCK_DOMAIN LOCKED / UNLOCKED | 6 / 5 | 7 / 6 | 8 / 7 | 9 / 8 | C1, one pair per switch |
| `SLIP_LB` dups | 414 | 422 | 422 | 422 | no slip on a stream-to-stream switch |
| `SLIP_TDM`, render rails | 0, 31 | static | static | static | static |

| CRF lock-loss counters | Before the unbind | Holdover | After LOCKED | Declared |
|---|---|---|---|---|
| DUT AAF talker MEDIA_RESET | 1 | 2 | 2 | one per disruption, none on the return |
| DUT CLOCK_DOMAIN LOCKED / UNLOCKED | 10 / 9 | 10 / 10 | 11 / 10 | C1 |
| DUT STREAM_INPUT 1 MEDIA_UNLOCKED | 0 | 1 | 0 (bank reset at the bind) | the Stream Input's |

**Validation:** at `4fb5125a`, every gate rc 0: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base 40714c1b`, `check_doc_paths.py` (pinned Markdown environment), `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test`, `git diff --check 40714c1b HEAD`.

**Acceptance criteria:** items 2, 3 and 4 run as assigned and met, with evidence in the section. Item 1 NOT RUN. #629 acceptance re-judged: lock loss met for both sources; the saved selection met at the bench; the switch met between the AAF and CRF streams but not from INTERNAL to AAF (#645); Direction B's THD+N NOT met. So "Refs #629".

**Open risks/questions:**
- #645: the INTERNAL-to-AAF ring slip after LOCKED repeated; its data is in the section "B8: the INTERNAL-to-AAF set and #645". Nothing was posted on #645 (this lane's posts are TAKEN, REVIEW READY and STOP on #629).
- The audio the DUT receives is not graded (no known signal on the peer's talker); the ring, junction and render words and the listener counters stand in. The #386 recentre count is not readable on silicon.
- Windows are shorter than lane B7's (each bench command ended within 10 minutes). The CRF window lost 19.0 s to three host capture stalls. The tool controls ran after the cases.
- Residuals: the DUT was power-cycled once, as authorised (counters reset, MAAP addresses re-allocated); NVM image seq 33; the SoC board's bridge legs under new process IDs. The bench lock is free and nothing is left running.
