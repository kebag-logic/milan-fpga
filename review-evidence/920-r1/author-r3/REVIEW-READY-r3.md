[A786] REVIEW READY
Round 3 commit: `81c9a1a0`, tests only over `bd252db1`.

- **F-1:** `first_change_after_flight` catches `next_now_not_reset`; `retry_after_rewind` catches `rewound_not_reset`, including restoration after a power cut. Both plants are registered in the store suite's self-test. Case 4's claim now describes only its record ahead of the rewound cursor, as the review permits.
- **F-2:** the prepared PR body applies [the manager's ruling](https://github.com/kebag-logic/milan-fpga/issues/920#issuecomment-6935243271). 1x1/1if is **0.517 of 0.70**. The 8x8/1if load is graded by **#914's gate at the composition**, with **0.735 of 0.75 at #914's head**. The 8x8/2if figure, **0.798**, is the base's and owed to **#890**. This PR changes no load term.

**Validation on clean clones of this head, all rc 0:**
- Store: `test_ctrl_nvm.py --require-rv32 --self-test --jobs 8`: **566 tests at five shapes; all 154 plants caught**, including both new reset plants; power-cut tests green.
- `fw_coverage.py --check --jobs 8`: **PASS, 39 files**; store and AECP persistence remain at 100% measured lines and branches under the existing exclusions.
- Docs: **five local jobs, zero failed steps**; verifier: **61 executed steps, 34 declared setup/hosted-only NOT RUN reasons, zero bad**.
- All **eight ELFs and eight loadable binaries**, rebuilt at both heads with identical inputs, are **byte-identical to `bd252db1`**. Firmware and gateware are unchanged; the harness, routes and sweep carry. The routes remain misses at the base, owed to #927.

**Amended acceptance:** “the load within 0.70 at 1x1/1if, and within 0.75 at 8x8/1if by #914's gate at the composition; 8x8/2if's load is owed to #890”. Round 3's requested delta is ready for re-review; composition grading, the #919 sync, bench qualification and hosted acceptance remain outstanding.

Packet: `round3/HANDOFF-r3.md`, `PR-BODY.md`, `REVIEW-READY-r3.md`, and sanitized receipts with `INDEX.md`. Own gate units are closed. Nothing pushed; the manager owns publication of the commit and PR body.
