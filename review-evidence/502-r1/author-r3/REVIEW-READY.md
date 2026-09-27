[A345] REVIEW READY

Commit: `5d4cf33e3709c35d4f5bc90d3c5a2334ef3bfd8e` (local candidate; no push).

Changed: retained round-2 option (a), storage-based observer and separate durable-baseline controls. The resume restores the original phase-5 input-change / output-change priority, names each existing comparison once, and exports their qualified OR to the unchanged shadow input. Committed tests are unchanged from `220c9d56`; matching documentation wording is updated.

Area, same default OOC recipe, both rc 0: datapath LUT total 98016 at `220c9d56`, 96166 at this head, saving 1850. Shadow LUT total stays 66982. FF, LUTRAM, RAM and DSP counts are unchanged; datapath CARRY4 is 3629 versus 3628. Relative to the earlier `104c8a54` baseline, datapath LUT total is lower by 1126. No timing claim.

Priority: RTL clears both key-valid flags and asserts them only in mutually exclusive descriptor branches. A read-only dynamic probe observed 25444 input-valid cycles, 37673 output-valid cycles and zero overlap. Expanding the named conditions reproduces the base phase-5 block, including its priority, exactly apart from whitespace.

Validation, all gate commands rc 0:

- Default RTL sweep at this head, all 55 suites and all default chunks: 55 passed, 0 failed, 0 timed out. Exact tally: suites: 55   passed: 55   failed: 0   timed out: 0; checks: 2125319   in-suite failures: 0.
- The sweep explicitly skips the unavailable AAF/AVTP and gPTP/802.1AS field campaigns and their two freshness checks (four declared skips, zero contribution to the tally).
- pp_shadow default: 575 + 575 + 575 + 263 checks, zero failures. The late-mark mutant is killed by named K10/K12 checks, including REMOVE.
- Both reviewers' scripts run unchanged; old textual anchors are explicitly refused. The recorded author adapter preserves their replacement expressions, and all remaining variants are killed. M5/phase4 fails refused-record checks; M6 fails named REMOVE checks in both legs. R329's unchanged probe passes 295 checks; P3 reports SUCCESS, unchanged map, pending 0 and durable 1.
- R328 oracle: 138 total checks in the static leg, 193 total checks in the dynamic leg, zero failures in either. These are two totals, not a passed/total fraction. All 10 static and 14 dynamic explicit live-change-without-pending assertions pass.
- Full builder rerun in both compiler modes with elaboration required; present mode also requires RV32. The unavailable historical placement-calibration fixture is explicitly NOT RUN in both modes; absent mode additionally omits its deliberately hidden compiler-dependent instruments.
- Lint, ports, naming, test-evidence, docs in both modes, em-dash, style, contents, anchors, paths, capture, language idioms, wire accountability and diff checks pass.

Acceptance: all seven round-2 assignment items and all resume items are addressed. Firmware, CSR/configuration inputs and submodule pins remain unchanged. HANDOFF.md, REVIEW-READY.md and PR-BODY.md carry this head; exact commands, bounded receipts, source verification and large-artifact hashes are in the assigned handoff packet. Independent re-review remains required; no review verdict is claimed.
