[A298] REVIEW READY
Commit: c9bbb03cc3d4da9c6ee28996b91addbb081efa7e
Branch: 443-render-csr; base 0755923d983218ca6ca9db6891a558cbe6425b8d. Clean local worktree; no push or PR operations, as assigned.

Changed: RENDER_STAT at 0x8DC exposes the STRM_SEL-selected listener's fill [7:0], prefill [8], convergence [9], reserved zero [15:10], and global saturating rails [31:16]. Talker/out-of-range selections and absent-stage integrations read zero. The register-map row/class and all four #443 pointers are current. No STREAM_INTERRUPTED wiring.

Validation (final commands all rc 0):
- `make -C tb/verilator/milan_dp VERILATOR_JOBS=8`: complete default sweep, with 37 separately recorded build/run chunks, all rc 0. True-clock-ratio leg: 188 checks, zero failures. Existing render controls: 6/6; grandmaster-step controls: 4/4.
- `make -C tb/verilator/milan_dp render-csr-controls VERILATOR_JOBS=8`: clean 62/62; absent-stage control 31/31 despite accepted media ingress. The wrong-fill mutant exits 1 at `RENDER-CSR: filling mirrors taps` (got 0x100, expected 0x106); campaign exits 0.
- `make -C tb/verilator/milan_dp_render VERILATOR_JOBS=8`: shipping 150/150, two-listener 64/64, existing controls 5/5. The two-listener case checks unequal selected states.
- `syn/yosys/run.sh --top milan_csr --top milan_datapath --no-structural --results <output>` at base and head: milan_csr 70,355 -> 70,466 (+111); milan_datapath 1,633,435 -> 1,631,783 (-1,652). Generic cell counts, default parameters; no physical area/timing claim.
- `python3 sw/builder/test_builder.py`: rc 0; gate 11 NOT RUN because its calibration placement report is absent. No calibration evidence claimed.
- `docs_check.py` in git and filesystem-walk modes; `check_em_dash.py --base 0755923d983218ca6ca9db6891a558cbe6425b8d`; doc style, TOC, doc paths, module matrix, front-end analysis, RTL source lists, SV/C++/Python idioms, RTL lint, port contracts, naming, test evidence and diff checks: all rc 0. Existing lint/front-end findings stay within their recorded budgets.

Acceptance: items 1, 2, 3 and 5 met locally; item 4 follows the recorded manager decision. HANDOFF.md and PR-BODY.md are complete in the assigned output directory, with layout, source locations, control/mutant evidence, cell counts and gate exits. Independent review remains with [R320] and [R321].
Open implementation questions: none. Validation limit: the builder's report-dependent gate 11 remains NOT RUN.
