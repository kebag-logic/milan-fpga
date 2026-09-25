[A301] REVIEW READY
Commit: 5beebb7c7edd908d08be34e52286c9eee441f5b3
Branch: 443-render-csr. Local commit only; no push or PR edits.

Round 2 items 1-5 are implemented under the assignment: driven RENDER_STAT reads with neighbour checks, graded STRM_SEL[9], campaign ownership in TESTING.md, the Unreleased VERSION deferral, and the 0x8DC register-groups row. VERSION remains 0x0002_0060. The shared-selector caveats and full-width CSR rail checks are included; all RTL is unchanged from c9bbb03cc3d4da9c6ee28996b91addbb081efa7e.

Validation, final commands all rc 0:
- `make -C tb/verilator/csr`: 380/380, 380/380, 115/115, 38/38 and 380/380. The missing-decode probe exits 1 at `RENDER_STAT selected listener preserves all fields`; its campaign exits 0.
- `make -C tb/verilator/milan_dp aclk`: 189/189.
- `make -C tb/verilator/milan_dp render-csr-controls`: clean 63/63; absent-stage 32/32. Wrong-fill exits 1 at `RENDER-CSR: filling mirrors taps`. The formerly surviving selector mutant exits 1 at `RENDER-CSR: bit 9 preserves talker rejection` (got 65550, expected 0). Campaign 4/4.
- `make -C tb/verilator/milan_dp_render`: shipping 150/150, two-listener 64/64, existing controls 5/5.
- `python3 scripts/docs_check.py` in both git and filesystem-walk modes; `check_em_dash.py --base 0755923d983218ca6ca9db6891a558cbe6425b8d`; doc style; `gen_toc.py --check` and `--verify-anchors`; doc paths; `xvlog_gate.py --check`; SV/C++/Python idioms; `measure_test_evidence.py --check`; `git diff --check`: all rc 0. The evidence self-test passes 101/101 and source-list checks pass. The front-end ran with the existing four processor findings exactly at its unchanged ratchet.

HANDOFF.md and the full updated PR-BODY.md are complete in the assigned output directory. The committed delta matches the tested working-tree diff, recorded in validation-head.json. The fetched public review evidence was inspected and its temporary repository deleted.

Acceptance: all five Round 2 items met locally. Independent delta reviews remain with [R320] and [R321]. Prior synthesis counts are retained because RTL did not change; their datapath decrease is unattributed and makes no physical claim. Round 1's full default sweep remains prior evidence; its report-dependent builder gate 11 remains NOT RUN. No hardware was used. Open implementation questions: none.
