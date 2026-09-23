[R268] NEGATIVE - exact head 535701a06128d54c7f0f161e1c061fa02d4d1342

Round R268-2: the internal, cleared-context independent re-review of issue #529 / PR #534 after correction round 1.

## Scope

- **Head:** `535701a06128d54c7f0f161e1c061fa02d4d1342`, tree `8c62c1a118b6bdacc0cf9b39d2cbdc633717630f`.
- **Source base:** `ede8d48ecd7c7f589a14b957951f040d92c99c70`. Six one-line commits with no trailers, linear on the base. Correction round 1 is `a51d5164` (harness) and `535701a0` (docs) on the round-0 head `f8155775`.
- **RTL:** `git diff f8155775 HEAD -- hdl` is empty. The RTL under review is the round-0 RTL, re-covered at this head.
- **Gitlinks:** unchanged from base. protocol-processor `424c688f`, gptp-processor `c1b61743`, third_party/verilog-axis `48ff7a7e`.
- **Lenses:** all five applied at this head.
- **Verdict: NEGATIVE.** One MINOR finding (F1) is open under Tests and Docs. Conformance, RTL and Robustness are covered clean. Every prior-round finding (R268-1 F1-F3, R269-1 F1) is resolved at this head.

## Reconstruction order

1. AGENTS.md, CONTRIBUTING.md, docs/README.md.
2. Issue #529: the body, the A10 assignments (A204, then A216 for correction round 1), the A204 TAKEN and REVIEW READY, and the A216 REVIEW READY.
3. The frozen acceptance: `docs/reference/REGISTER_MAP.md` "Closure criteria for the CRF Stream Input counter gap", items 1-4, at base `ede8d48e`.
4. Authorities: Milan v1.2 5.3.8.10 (Table 5.6 and its reset-on-bind sentence), 5.4.2.25 (Table 5.16), 5.4.5 (Table 5.22); IEEE 1722.1-2021 Tables 7-156/7-157; the repository contract `tests/features/counters_contract_milan.feature:70-100` (Milan Stream Input mask `0xF3F`, IEEE block `0xFFF`).
5. Interfaces: `KL_crf_rx` ports and banner; the GET_COUNTERS gather face, the `crf_rx` instance and the Table 5.22 descriptor arbiter in `milan_datapath.sv`.
6. `git diff ede8d48e..535701a0`, the per-commit history, and `git diff f8155775..535701a0`.
7. Public evidence: the packet at `9f799fe0` `review-evidence/529-r1` (the A216 correction packet, `MUTATION-RESULTS.md`, mutant diffs), the manager's evidence comments, and the exact-head hosted check runs (read only).
8. Prior public review findings (R268-1, R269-1) were read only after this round's own pass over the diff, its own mutants and probes. No current-round report of another reviewer was read.

## Focus items

### Every one of the ten output-to-root bindings is discriminated

- The new event arm (`tb/verilator/milan_dp/sim_nxn.cpp:3578-3624`) seeds no tally. In a fresh era, real PDUs at the root and the engine's own silence timeout move each of the ten to a pairwise-distinct count (2, 1, 3, 4, 5, 6, 7, 8, 9, 21). The plan was traced against `hdl/ieee1722/crf/KL_crf_rx.sv:343-549` (settle, interval commit, sequence cursor, mr seeding, late/early limits, timeout reset); each count follows from the engine's own law, and the head run reads exactly those counts on every broad leg.
- **This round's own mutants:** all 45 pairwise exchanges of the ten `KL_crf_rx` tally bindings at the instance, generated independently by `scripts/gen_mutants.py`. They are byte-identical to the 45 published pairwise mutants (`receipts/swap_vs_published.txt`).
  - Head harness, nxn: 45/45 KILLED; in every one the event arm's "all ten" row fails on BOTH exchanged quadlets (`receipts/swap_summary_head_nxn.txt`).
  - Head harness, nxn8: 45/45 KILLED, both quadlets red in each (`receipts/swap_summary_head_nxn8.txt`).
  - Round-0 harness (`f8155775`, sha256 `3f948b1b...`), nxn: 22 of 45 SURVIVE (`receipts/swap_summary_f815harness_nxn.txt`), the same 22 the author published. The new arm, not an older check, is what kills them.
- **Prior reviewers' mutants, re-applied from the public packet** (all 32 diffs apply cleanly and reproduce the published sha256, `receipts/prior_mutants_INDEX.tsv`):
  - R269 mx1-mx4: KILLED on nxn, nxndv, nxn8 (as the byte-identical exchanges) and nxn4c.
  - R268 p1-p5: KILLED on nxn, nxndv, nxn8 and nxn4c.
  - R268 a1-a8: KILLED on nxn; a5 also KILLED on notify.
  - R269 ma1-ma7: KILLED on nxn.
  - R268 r2, r4, r5, r7: KILLED on nxn. r3: green on nxn, KILLED on notify. r1: green (wire-equivalent: the processor refuses index N+1 before the gather face is consulted). r6: green (arbiter starvation, see S5). The marked control is green on nxn, nxn8 and notify.
- Mutation receipts in this packet: 230 (`receipts/MUTATION-SUMMARY.tsv`). The author's packet lists 197; their pairwise and prior-reviewer results agree with this round's wherever both exist.

### The `[NOTIFY-CRF]` timed check

- `sim_nxn.cpp:1346-1353` now requires, after the release, two more processor seconds with no further push to B or to A.
- A pending bit that never clears (this round's `pend_crf_stuck`, and R268 `r3`) is KILLED on `obj_notify`: 4 pushes against 2, to B and to A. The same mutant SURVIVES the round-0 harness (143/0, `receipts/mutants/f815harness_notify__pend_crf_stuck.txt`). A free-running dirty source (`dirty_free_running`) is also KILLED by the new checks. The head passes 145/0 with the release measured 997 ms after the first push.

### The harness shortcut (the silence timeout advanced to its last millisecond)

Judged acceptable. `sim_nxn.cpp:3607-3610` writes only `crf_rx.tout_r`, the engine's idle counter, to 1 ms short of its limit; no tally is written, and a port-map exchange cannot relabel that counter. Evidence (`receipts/harness_probes/`, `receipts/probe_harness_*.diff`):

- **Equivalence:** with the write removed and the whole 100 ms plus the same 0.1 ms margin run for real, nxn gives all 1705 check lines identical in name and value to the head run (`fullsilence_vs_head_checklines.txt`), at 38 s instead of 6 s.
- **The last millisecond is real:** the write followed by only 0.99 ms fails the two unlock checks (`shorttail.txt`); no write and 1.1 ms fails four (`nowrite.txt`).
- **Fail-closed coupling:** binding `KL_crf_rx` to half or twice the fabric clock at the root (`tout_half`, `tout_double`) is red on nxn.
- The constants are literals rather than derived from the elaborated clock (S1). Every leg that compiles `sim_nxn.cpp` elaborates the 100 MHz default, and a different clock fails red, never green.

### Docs claim only what the tests prove

- Resolved at this head: the signature arm is described as grading the gather mux only (`sim_nxn.cpp:3422-3428`, `REGISTER_MAP.md:876-887`, `README.md:508-510`); the binding claim rests on the event arm; the mutation claims say "at least one check red"; the frozen criteria are quoted verbatim (normalized text comparison against `ede8d48e`); the opening status (`REGISTER_MAP.md:31-35`) is current; the compliance-matrix row names the event arm.
- Not resolved: F1 below. The criterion-3 evidence and two companions claim the bind edge reaches the arbiter "as {STREAM_INPUT, N} and as nothing else", which the check does not prove.

## Findings

### F1 - MINOR - Tests, Docs - the "and as nothing else" arbiter claim is stronger than its check

```text
[R268] MINOR Tests, Docs - docs/reference/REGISTER_MAP.md:898-899, tb/verilator/milan_dp/README.md:513-514, tb/verilator/milan_dp/sim_nxn.cpp:3464-3472 - the bind edge is claimed to reach the arbiter as {STREAM_INPUT, N} "and as nothing else"; the check sees STREAM_INPUT rows only
```

- **Authority / evidence.**
  - AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect". Docs: the PR and docs carry evidence another cold reviewer can rely on. This round's charter: docs claim only what the tests prove.
  - The closure record for criterion 3 (`REGISTER_MAP.md:898-899`) says `[CTRS-CRF]` "sees the bind edge reach the descriptor arbiter as {STREAM_INPUT, `N_STREAMS`} and as nothing else". The README (`:513-514`) says "{STREAM_INPUT, `N_STREAMS`} alone". The harness comment (`sim_nxn.cpp:3464-3467`) states the same requirement.
  - The check (`sim_nxn.cpp:3469-3472`) clears and compares only `pp_ctr_evt_sin_seen`. The STREAM_OUTPUT, AVB_INTERFACE and CLOCK_DOMAIN observation bitmaps the harness already keeps (`sim_nxn.cpp:563-584`) are neither cleared nor checked.
  - Two mutants that deliver the CRF input's dirty pulse additionally to another descriptor type pass every committed check on nxn and on the timed leg (`receipts/extra_mutants/extra_nxn__*.txt`, `extra_notify__*.txt`; diffs in `receipts/extra_mutant_diffs/`):
    - `dirty_also_sout_n`: also raises STREAM_OUTPUT `N_STREAMS`, the CRF Media Clock Output's row at the same index;
    - `dirty_also_ckd`: also raises CLOCK_DOMAIN 0.
  - A three-check strengthening in a disposable harness copy (clear all four bitmaps before the edge; require no STREAM_OUTPUT, AVB_INTERFACE or CLOCK_DOMAIN tuple; `receipts/probe_harness_arbprobe.diff`) kills both mutants on nxn and is green on the unmutated head on nxn, nxndv, nxn8 and nxn4c (`receipts/extra_mutants/arbprobe_*`). So the head RTL has the claimed property; only the evidence is missing.
- **Impact.** A regression that also pushes GET_COUNTERS for the CRF Media Clock Output or the Clock Domain whenever the CRF input's counters change (a plausible confusion: the CRF input and output share index `N_STREAMS`) keeps every gate named as #529's evidence green, while the closure record says the test excludes it.
- **Lens attribution.** Tests and Docs. Not Conformance: the frozen criteria 1-4 are met by the checks as they stand, and the probe shows the head RTL delivers no other tuple. Not RTL or Robustness: the RTL is correct.
- **Required outcome.** Either the committed check proves exclusivity across all four tuple families, or the three texts are narrowed to what it proves (for example, "and no other STREAM_INPUT row").
- **Verification.** If strengthened: `dirty_also_sout_n` and `dirty_also_ckd` are red on nxn, and the head stays green on the four broad legs. If narrowed: the three texts read against `sim_nxn.cpp:3469-3472`, plus `docs_check.py` and `check_em_dash.py`.
- **Provenance.** The wording was already present at `f8155775` and was not raised by R268-1 or R269-1.

### Suggestions (do not affect coverage)

- **S1 - Tests - `sim_nxn.cpp:3607-3608`.** `kCrfSilenceCyc` and `kFabricMsCyc` are literals mirroring `CLK_FREQ_HZ_P / 10` and `MILAN_CLK_FREQ_HZ / 1000`. The Makefile's own discipline hands such numbers over as a `-D` from the variable behind the `-G`. Fail-closed today (`tout_half`, `tout_double` red).
- **S2 - Docs - `REGISTER_MAP.md:900-901`, `README.md:524-525`.** "reach both registered controllers, byte-identical from the body on to the solicited answer": only B's copy is compared (`sim_nxn.cpp:1315-1325`); A's copy is counted, not compared.
- **S3 - Tests - the tally wires are named through non-public model members.** Removing a wire's only reader or tying it off makes the harness fail to compile rather than fail a named check (`receipts/mutants/head_nxn__mux_row_removed.txt`, `head_nxn__unbind_*.txt`). Still fail-closed; marking the ten wires `public_flat_rw`, as the prior reviewers' mutants do, would turn those regressions into named red checks.
- **S4 - retained, R269-1 S2 - Tests.** `[NOTIFY-CRF]` grades `>= 990 ms` (`sim_nxn.cpp:1345`) while the timed-leg header says "RELEASED after >= 1000 ms" (`:1062`).
- **S5 - retained, R268-1 S1 - Tests.** R268 `r6_rr_sout_old` (round-robin resumes at the STREAM_OUTPUT just delivered) is still green on nxn; the no-starvation property has no discriminating check.
- **S6 - retained, R268-1 S2 / R269-1 S1 - Robustness, Tests.** No leg elaborates a `crf_sink: false` shape. This round's builder-emitted 4x4 no-CRF shape elaborates with warning kinds and counts identical to the CRF shape; the harness then fails to compile on the CRF wire the guard legitimately removes (`receipts/nocrf_shape/RESULT.txt`).
- **S7 - retained, R269-1 S3 - Docs.** `configs/endstation_arty_4x4.yaml:103`, `endstation_arty_8ch.yaml:139`, `endstation_ax7101_8x8.yaml:153` still point runtime gaps at "the current audit B3 and B4"; B4 is now recorded closed.

## Per-lens results at this head

```text
[R268] PASS Conformance - hdl/milan/milan_datapath.sv:3511-3552,5438-5501,7200-7301; tests/features/counters_contract_milan.feature:70-100; REGISTER_MAP.md:870-913 against the frozen criteria at ede8d48e; receipts/baseline/SUMMARY.txt - mask 0xF3F at the Table 7-157 offsets, Table 5.6 lock pair 0/0, 1/0, 1/1, 2/1, 32-bit wrap, reset on not-bound to bound, NO_SUCH_DESCRIPTOR at N+1, one push per descriptor per second and quiet after it; criteria 1-4 met at source level
[R268] PASS RTL - hdl/milan/milan_datapath.sv:1785-1796,3349-3352,3511-3552,4992-5003,5438-5501,7184-7301; hdl/ieee1722/crf/KL_crf_rx.sv (comment-only change); receipts/static_gates.txt, receipts/nocrf_shape/RESULT.txt - axis_clk only, no new crossing, all new state reset, 32-bit widths, CRF arm disjoint from the AAF arm, PP_CTR_SIN_N_C sizing and pick/clear/round-robin arithmetic for N = 1, 4, 8, both shape branches elaborate, lint 90 <= 90
[R268] PASS Robustness - milan_datapath.sv:3524-3526,7206-7274; receipts/nocrf_shape/RESULT.txt; receipts/harness_probes/; receipts/prior_mutants/prior_nxn__r268_r1_index_ge.txt - undeclared and large indices, reset and bind wipe, wrap, pending absorption and no re-push, no-CRF shape, shortcut equivalence and its fail-closed failure modes
[R268] MINOR Tests, Docs - REGISTER_MAP.md:898-899, README.md:513-514, sim_nxn.cpp:3464-3472 - arbiter "and as nothing else" claim not proven by its check (F1)
```

- **Tests: UNCLEAN (F1).** Everything else examined under this lens is clean: the event arm discriminates all 45 exchanges on two shapes; the NOTIFY-CRF release-then-quiet arm fails for a stuck or free-running row; the signature, wrap, isolation and from-reset arms kill every gather-face mutant; no existing check was removed or weakened (the only non-additive harness hunk is the `send_crf` refactor into `send_crf_pdu` at `sim_nxn.cpp:4631-4655`, the same PDU byte for byte); the four broad legs and the timed leg are green.
- **Docs: UNCLEAN (F1).** Everything else examined under this lens is accurate against the code and the executed evidence: REGISTER_MAP (opening status, `:138-142`, the `0x738` group, criteria 1, 2 and 4), REGISTER_MAP_CLASSES, the compliance-matrix rows 5.4.2.25 and 5.4.5.1/.2, audit B4 and item 7, FR_NFR, the roadmap, the builder page, the CHANGELOG, the milan_dp README outside `:513-514`, `port_docs.budget` (regenerates byte-identical), and the `KL_crf_rx`/`milan_datapath` comments. `docs_check` and `check_em_dash --base ede8d48e` are clean.

## Prior public findings

Read after this round's own pass. Each is checked again at this head.

| Prior item | Disposition at this head |
|---|---|
| R269-1 F1 MAJOR = R268-1 F1 MINOR (Conformance, Tests, Docs): permuted `KL_crf_rx` bindings invisible | **RESOLVED.** 45/45 exchanges KILLED on nxn and nxn8, both quadlets red; mx1-mx4 and p1-p5 KILLED on nxn, nxndv, nxn8, nxn4c; the round-0 harness lets 22 through. The binding docs now rest on the event arm. |
| R269-1 F1 docs overclaim (REGISTER_MAP 846-877, sim_nxn 3409-3411, README 507-521 at `f8155775`) | **RESOLVED** for the binding claims. The separate arbiter-exclusivity wording is this round's F1. |
| R268-1 F2 MINOR (Tests, Docs): `[NOTIFY-CRF]` cannot fail for a row that keeps pushing | **RESOLVED.** r3 and `pend_crf_stuck` KILLED on notify (4 pushes against 2); both SURVIVE the round-0 harness. |
| R268-1 F3 MINOR (Docs): opening status lists the CRF bank as a gap | **RESOLVED.** `REGISTER_MAP.md:31-35`. |
| R268-1 S3 / R269-1 S5: `Closes #529` before the silicon item | **RESOLVED.** The PR body now reads "Relates to #529", the issue closing after the manager's silicon check. |
| R269-1 S4: frozen criteria paraphrased | **RESOLVED.** All four are quoted verbatim. |
| R268-1 S1: arbiter starvation untested (r6) | **RETAINED** as S5. |
| R268-1 S2 / R269-1 S1: no `crf_sink: false` leg | **RETAINED** as S6. |
| R269-1 S2: 990 ms floor vs ">= 1000 ms" header | **RETAINED** as S4. |
| R269-1 S3: config comments point at B4 | **RETAINED** as S7. |

The pre-existing mismatch the author reported as out of scope (the `KL_crf_rx` banner and the `CRF_CTRL` row say a validation error unlocks the sink; the engine unlocks only on the 100 ms silence) is confirmed by reading `KL_crf_rx.sv:508-513` against `:480-489`. It predates this lane and is tracked by open issue #541; it is not a finding against this head.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Milan v1.2 5.3.8.10/Table 5.6, 5.4.2.25/Table 5.16, 5.4.5/Table 5.22; IEEE 1722.1-2021 Tables 7-156/7-157; `counters_contract_milan.feature:70-100`; `milan_datapath.sv:3511-3552,5438-5501,7200-7301`; frozen criteria 1-4 at `ede8d48e` vs `REGISTER_MAP.md:870-913`; five baseline legs | R268-2 | `535701a06128d54c7f0f161e1c061fa02d4d1342` |
| RTL | CLEAN | `milan_datapath.sv:1785-1796,3349-3352,3511-3552,4992-5003,5438-5501,7184-7301`; `KL_crf_rx.sv` diff (comments only); lint, port-contract gate and budget regeneration; no-CRF shape elaboration | R268-2 | `535701a06128d54c7f0f161e1c061fa02d4d1342` |
| Robustness | CLEAN | `milan_datapath.sv:3524-3526,7206-7274`; no-CRF shape; shortcut probes (full silence, no write, short tail); r1 equivalence; wrap and bind-wipe results | R268-2 | `535701a06128d54c7f0f161e1c061fa02d4d1342` |
| Tests | UNCLEAN (F1) | `sim_nxn.cpp:1062,1280-1356,3277-3624,4631-4655`; 230 mutant receipts; 3 shortcut probes; the arbiter probe; 5 baseline legs | R268-2 | `535701a06128d54c7f0f161e1c061fa02d4d1342` |
| Docs | UNCLEAN (F1) | REGISTER_MAP.md, REGISTER_MAP_CLASSES.md, MILAN_COMPLIANCE_MATRIX.md, FR_NFR.md, MILAN_V12_ROADMAP.md, ENDSTATION_BUILDER.md, MILAN_V12_AUDIT_2026-08-16.md, CHANGELOG.md, milan_dp README.md, port_docs.budget, `KL_crf_rx.sv` and `milan_datapath.sv` comments; `docs_check`, `check_em_dash` | R268-2 | `535701a06128d54c7f0f161e1c061fa02d4d1342` |

A fix for F1 that touches only `sim_nxn.cpp` or the docs un-covers Tests and Docs; Conformance, RTL and Robustness stay banked at this head as long as nothing in their scope changes.

## Reproduced evidence at this head

Pinned simulator 5.050 (`receipts/tool_identity.txt`), at most 8 C++ jobs in total, in a disposable clone of the exact head. Leg recipes are the `run` recipe's (`scripts/legs.mk`).

| Leg | Result | `[CTRS-CRF]` / `[NOTIFY-CRF]` checks |
|---|---|---|
| obj_nxn | 1705/0 | 72 |
| obj_nxndv | 1707/0 | 72 |
| obj_nxn8 | 3133/0 | 72 |
| obj_nxn4c | 1705/0 | 72 |
| obj_notify | 145/0 | 10 |

Static, focused: `lint_rtl.py --check` 90 <= 90; `check_port_contracts.py` OK, and `--write-budget` regenerates `port_docs.budget` byte-identical; `check_em_dash.py --base ede8d48e` 0 findings over 153 added lines; `docs_check.py` 0 findings; `git diff --check` clean (`receipts/static_gates.txt`).

## Receipts

Every published file is listed in `MANIFEST.sha256` (paths relative to the packet root).

- `scripts/`: `build_leg.sh`, `legs.mk`, `run_leg.sh`, `run_mutants.sh`, `gen_mutants.py`, `analyze_swaps.py`, `gen_harness_probes.py`, `gen_arbiter_probe.py`, `summarize_receipts.py`, `verify_clone.sh`.
- `receipts/baseline/`: the five head runs and `SUMMARY.txt`.
- `receipts/mutants/`, `receipts/mutant_diffs/`, `receipts/mutants_INDEX.tsv`, `receipts/swap_summary_*.txt`, `receipts/swap_vs_published.txt`: this round's 65 mutants.
- `receipts/prior_mutants/`, `receipts/prior_mutants_INDEX.tsv`: the prior reviewers' mutants, re-run.
- `receipts/extra_mutants/`, `receipts/extra_mutant_diffs/`, `receipts/probe_harness_arbprobe.diff`, `receipts/arbiter_probe_sha256.txt`: F1. In the `arbprobe_*` receipts the unmutated head is the green control, so its verdict reads SURVIVED.
- `receipts/harness_probes/`, `receipts/probe_harness_{fullsilence,nowrite,shorttail}.diff`, `receipts/harness_probes_sha256.txt`: the shortcut.
- `receipts/nocrf_shape/`: the no-CRF shape probe.
- `receipts/MUTATION-SUMMARY.tsv`: all 230 mutant receipts in one table.
- `receipts/hosted_check_runs.tsv`, `receipts/static_gates.txt`, `receipts/tool_identity.txt`, `receipts/clone_state_final.txt`.

Reproduce: clone the exact head with the three required submodules into a disposable tree, generate the hex images (`make ltn_rom.hex ucode.hex gptp_ucode.hex gen_divergent/gen/adp_shape_defaults.svh` in `tb/verilator/milan_dp`), then `VERILATOR=<pinned 5.050> bash scripts/run_mutants.sh <tree> <leg> <harness> <tag> <mutdir> <scratch> <outdir> <par> <ids...>`.

## Limits

- **Not run by this round:** the full suite sweep; the milan_dp legs that do not compile `sim_nxn.cpp` (obj_dir, nolpf, prune, ax1x1, aclk, gptp, gptplat) and the render mutants; pp_shadow, milan_dp_render, crf_rx, behave; `xvlog_gate`, `check_sv_idiom`, `check_cpp_idiom`, `gen_module_matrix`; Yosys, the builder bank, any synthesis or timing; act; hardware. Correction round 1 changes only `sim_nxn.cpp` and docs, and `hdl/` equals the round-0 head.
- **Shortcut equivalence** was run whole on nxn only; the other legs use the same code path and constants.
- **Synthesis:** the +1,134 generic-cell figure is the author's and was not reproduced. No physical timing exists for the added answer arm.
- **Hosted, exact head, read only:** 22 check runs; 21 success, 1 skipped ("Physical gPTP (nightly and manual)"). All seven required contexts (`rtl-fast`, `docs-check`, `wire-accountability`, `docs-check-no-git`, `elaborate`, `verilator-suites`, `yosys-portability`) concluded success; Verilator shards 0-4 and Yosys shards 0-3 executed. A skipped context is not evidence. Hosted and act acceptance belong to the manager.
- **Manager banks:** the source static/builder and native banks for this head were still running when this round started; this report makes no claim about them.
- **Physical calibration NOT RUN;** field skips are not hardware proof. No silicon or controller verdict exists for this head.
- **Object fetch:** the review clone fetched the public evidence commit `9f799fe0` read-only; no tracked byte, mode, index record or gitlink changed.

## Pending manager duties

- Publish the source static/builder and native bank results for this head.
- Accept the hosted and act evidence.
- Build and gate the final current-dev candidate at the merge turn (source base `ede8d48e`, live dev `26d855a9`).
- Route F1 to the author; re-review its fix at the new head (Tests and Docs must be re-covered there).
- Silicon: re-flash and the Milan-controller verdict (#117); #529 closes after it, per the PR's "Relates to".

## Clone restoration

No tracked file in the review clone was edited; every build, mutant and probe ran in a disposable clone under the packet's scratch directory. `scripts/verify_clone.sh` (`receipts/clone_state_final.txt`): HEAD and tree match; index records equal the HEAD tree records; 864 tracked blobs, 0 byte or mode mismatches; no untracked, ignored or modified residue; the three required gitlinks at mode 160000, at their pins, with clean worktrees.

R268-2 FINISHED
