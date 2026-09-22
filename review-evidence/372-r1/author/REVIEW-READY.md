[A170] REVIEW READY
Commit: `5bbf2953ea747403217aeeda020df6a6e5ff27f9` (tree `fee8638e957b1a4076da67cb7c1f368336f1a46c`). It is one one-line commit on dev `88e9276b2a220c716f64a843f7e1eb8f9265e896`, not pushed by the author.

Changed:
- `tb/common/sva/` holds three new files. `axis_stream_source_sva.sv` is a reusable AXI4-Stream source-obligation checker (IHI0051A 2.2): TVALID held, and TDATA, TKEEP and TLAST stable, until the handshake. `axis_mux_rr_2in_1out_sva.sv` has instances `u_s0_stimulus`, `u_s1_stimulus` and `u_m_dut`, plus the mux's grant, ownership, state, reset and forwarding laws. `axis_mux_rr_2in_1out_bind.sv` binds by module name. Product RTL is unchanged.
- `tb/verilator/ptp_ts/mux_sva_main.cpp` drives the unmodified mux at TDATA_WIDTH 8 and 64. It has compliant sources, a sink, a scoreboard independent of the checker, and a DPI witness ledger. Its 8 scenarios cover single and multi-beat packets, valid gaps, simultaneous offers, mid-packet and TLAST backpressure, reset while stalled with resumed traffic, and seeded random traffic.
- `tb/verilator/ptp_ts/sva_campaign.py` is the 62-row detection campaign. The Makefile default is now the original `run`, then `mux-sva`, then `sva-campaign`. The `run` recipe and `sim_main.cpp` are byte-identical to the base.
- `scripts/measure_test_evidence.py` gains one reader disposition classifying the campaign as a mutation campaign; the unexplained-reader budget stays 0.
- `docs/testing/ASSERTIONS.md` is the new guide, linked from `docs/README.md`, `docs/testing/TESTING.md`, `tb/verilator/README.md` and `docs/guides/VERIFICATION_DEVELOPER.md`.

Validation used pinned Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`) with explicit `--assert` and `-j 8`. The tool is the Arch `verilator-5.050-1` package present locally outside PATH; all 123 installed non-manual files hash-match its package mtree, and no container was started. The host PATH Verilator is 5.052 and was not used for evidence.
- `make -C tb/verilator/ptp_ts VERILATOR=<5.050>` exited 0 (111 s). `python3 scripts/suite_tally.py --verdict <log>` exited 0.
- The tally over that log is 495 checks, 0 failures, 4 tallies: `ptp_ts: 92 checks` (original, same as base), `mux sva w8: 170`, `mux sva w64: 171`, `sva campaign: 62`. No assertion evaluation or pass action is counted as a check.
- All 21 (instance, property) pairs report non-vacuous passes. For 15 the count equals the harness's own port count (for example w64 `u_m_dut` 228/228 and `u_s0_stimulus` 625/625). Two meet a port-count floor, and the 4 immediate laws are above zero.
- Every property fails, by its own name, on a planted defect:
  - 2 clean rows pass with no property failing.
  - 16 stimulus faults cover 4 source rules, 2 ports and 2 widths.
  - 14 DUT mutants are scratch copies with exactly-once patterns. Each is named at the first failing edge, including a replay of the defect the mux's own comment records (TVALID waiting for TREADY).
  - 1 scoreboard row inverts round-robin order: the scoreboard fails and no property fires.
  - 1 elaboration row builds width 12, which the checker's own guard message refuses.
- 4 lost-coverage controls: `--no-assert`, a mistyped bind target (5.050 builds it with no diagnostic, even under `-Wall`), an s0/s1-mirrored bind (every law still holds, so only the witness counts catch it) and an unused path. The harness refuses each positive run, and all 24 injected faults on them fail the detection check.
- Expected failures stay in per-row raw logs; the suite log carries no `[FAIL]` line.
- These gates exited 0 with no budget widened:
  - documentation: `docs_check`, `check_em_dash --base` (0 findings over 292 added lines), doc style, paths and gPTP docs, `gen_toc --check` and `--verify-anchors`, feature status, solution and submodule docs, diagram PNGs, `DOC_MAP`, `gen_module_matrix --check` (69 modules, unchanged), bare-metal-only, archive;
  - source lists and ratchets: `pp_srcs`, RTL source lists, naming, port contracts, fail-fast, TODO ownership, `measure_test_evidence --check` and `--selftest`, hygiene;
  - idiom and self-tests: SV, C++, Python and shell idiom, `suite_tally` and `suite_shards` self-tests;
  - lint: `lint_rtl --check` on 5.050 (90 <= 90).

Acceptance criteria:
- Met: at least one representative module has bound SVA checks passing in simulation. `axis_mux_rr_2in_1out` passes at both widths, with the witnesses above.
- Met: assertions fire on intentionally injected bugs. 14 mutants and 16 stimulus faults are each caught by the named property, and the lost-coverage controls make the detection check fail.
- Met: guidelines for adding assertions. `docs/testing/ASSERTIONS.md` covers files and naming, binding, enabling, reset and past state, witnesses, proving failure, and reproduction. It states the two-state/X, CDC, formal, timing and coverage limits.

Open risks/questions:
- The `scripts/test_evidence.budget` mutation ratchet reads 77 (75 at the base, 74 now). I left it unchanged to avoid editing a shared budget file; lowering it is the manager's call.
- `ptp_ts` suite time grows from about 5 s to about 110 s on an 8-core host (18 extra Verilator builds).
- The mux instance inside `ptp_ts_top` is not bound, because the original leg is unchanged. The guide records this as a limit.
- No defect was found in the unmodified mux.
