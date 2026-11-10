[A757] TAKEN

Round 3 on PR #874. I add commits on `2131eff48066da1e3bbeb6b417ea0655fa7c7741` only, with no merge, rebase, force or amend. Branch `665-s7-srp-tx`, base `dev-soft-core` `1d6bf555`.

Authoritative references:
- the round 3 ruling (PR #874 issuecomment-6766550989), items 1 to 4;
- R813-2 (PR #874 issuecomment-6766539856): F-1, R-1 and R-2, with its `scripts/request_probe.py` and `receipts/request-probe.txt` on `665s7-review-evidence`;
- R814-2 (PR #874 issuecomment-6766441473): R-1 to R-3;
- this issue's acceptance item 3;
- IEEE 802.1Q-2018 10.7.4.1, 10.7.11 and Table 10-7;
- `docs/reference/FR_NFR.md` 3.4.1 (Milan v1.2 4.2.7.1.1 and Table 4.3: JoinTime 200 ms, 180 to 240; a point-to-point requested transmit opportunity occurs within JoinTime);
- lwSRP `mrp_mad.c:854`, `:1421`, `:1539-1540` at the pinned gitlink.

Interpreted scope:
- **Item 1.** The bench (`srptx.hpp`) records what lwSRP did at its link-time boundary, at each transmit poll:
  - whether this poll was the first since the participant's Join timer expired. A Join expiry only clears `join_wait` (`:854`). So that poll sends the transmit the Join timer held, or it finds nothing to send (`:1421`);
  - otherwise, the last poll at which lwSRP had nothing to send while its Join timer was stopped.

  `srptx_grade.py` grades the Join interval only for frames sent at the first poll after a Join expiry, with no time window. A requested opportunity after an idle expiry is graded instead by the requested-opportunity rule of `FR_NFR.md` 3.4.1: within JoinTime, widened by T_svc, of the last time lwSRP had nothing to send. `measure_time`'s JoinTime figures use the same attribution. That rule gets its own plant and a control 1 ms inside.
- **Item 2.** `join-early-past-t-svc`, `join-interval-late`, and the 10 cs and 15 cs arms are still refused by their own words.
- **Item 3.** R813-2's off-grid case becomes a committed control in `make srptx`: the licence scenario with the peer's LeaveAll at ms 16280 and at ms 16240, both graded clean. I also run R813-2's `request_probe.py` unchanged at offsets 280 and 240, which must give 0 findings.
- **Item 4.**
  - R813-2's R-1 and R-2: the PR body's status, and `ATTRIBUTE_MS`'s comment.
  - R814-2's R-1 to R-3: the PR body, the grade's garbled prose, and the README's rate window named with its T_svc term.
- **Unchanged.** Item 5 stays owed, and the fixture is not touched. The edits stay within `tb/verilator/milan_dp` and its README, with no lwSRP, adapter, RTL, loop, shape or ring change. Every existing shape's generated output stays byte-identical.

Validation plan, all rc 0, on a clean clone of the final head:
- `make srptx`, `srptx-plants` and `srptx-mutants`, and `request_probe.py` at 280 and 240;
- every `run:` step of the workflow jobs a pull request to `dev-soft-core` triggers, with a reason for each step that cannot run;
- the docs workflow;
- the full sweep, in 4 shards;
- the firmware self-test, `fw_coverage.py --check` and every firmware mutant driver;
- S2's harness at 1x1/1if and 8x8/2if;
- `test_builder.py --require-rv32` and `cd tests && behave`;
- `git diff --check` against the merge base.

Blockers: none. The exit does not apply. lwSRP's boundary state tells a Join-gated transmit (sent at the first poll after the Join expiry) from a requested one (sent after a poll that found nothing to send), with no edit to lwSRP or the adapter.
