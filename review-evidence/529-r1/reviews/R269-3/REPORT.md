[R269] POSITIVE - exact head 31e62ffead16e43d648993278b0ab9190d99b672

Round R269-3, external independent review of issue #529 / PR #534, in a cleared context.

- Exact head `31e62ffead16e43d648993278b0ab9190d99b672`, tree `4d32ede1eba65adcee359d00751ddadf3314a36b`.
- Source base `ede8d48ecd7c7f589a14b957951f040d92c99c70`, which is an ancestor of the head.
- Nine commits on the base. This round is a delta review of the last three (`b65030e0`, `78cdff20`, `31e62ffe`, on `535701a0`), and it judges the full head on all five lenses.

## Summary

- **Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open at this head. All five lenses are covered clean in this round, at this head.
- **The focus, R268-2 F1 = R269-2 F1 (MINOR; Tests, Docs), is resolved.**
  - The bind-edge check now fails when the CRF pulse reaches the Table 5.22 arbiter as any tuple except {STREAM_INPUT, `N_STREAMS`}.
  - 11 reviewer mutants each turn a named check red on both nxn and nxn8. They cover:
    - another STREAM_INPUT row;
    - the CRF row delivered in place of another row;
    - STREAM_OUTPUT `N` and STREAM_OUTPUT 0;
    - AVB_INTERFACE 0 and CLOCK_DOMAIN 0;
    - a foreign type;
    - an undeclared index, a past-bitmap index, and {AVB_INTERFACE, 1}.
  - `[NOTIFY-CRF]` now compares A's copy as well. A corrupted A copy fails only that check.
  - REGISTER_MAP, the milan_dp README and the harness comments claim exactly this.
- **Every earlier MINOR and MAJOR on this PR stays resolved at this head.** They are R269-1 F1, R268-1 F1, F2 and F3, and R269-2 F1 = R268-2 F1. I re-ran their decisive mutants on this head, not on the round they were answered in.
- **Four new SUGGESTIONs (S1-S4) and four retained ones (S5-S8).** None affects lens coverage.
- I wrote my verdict and ledger before reading any earlier review report. That receipt is `receipts/50_independent_verdict_before_prior_findings.md`, timestamped 2026-09-24T00:45:10Z.

## Reconstruction

I read these in order:

1. AGENTS.md and CONTRIBUTING.md.
2. docs/README.md.
3. Issue #529: its body and the manager's assignment comments (A10 of 2026-09-23 14:17, 19:25 and 23:27).
4. The frozen acceptance, which is REGISTER_MAP "Closure criteria for the CRF Stream Input counter gap", criteria 1-4, as quoted at the base.
5. The authorities those criteria cite:
   - Milan v1.2 5.3.8.10 (Table 5.6), 5.4.2.25 (Table 5.16) and 5.4.5 (Table 5.22);
   - IEEE 1722.1-2021 Tables 7-156 and 7-157, through the repository's `tests/features/counters_contract_milan.feature` (the Stream Input mask `0xF3F`; the IEEE block `0xFFF` with TIMESTAMP_VALID at 24 and TIMESTAMP_NOT_VALID at 28).
6. The PR body.
7. `git diff ede8d48e..31e62ffe`, all 16 files, and the delta `535701a0..31e62ffe`, 6 files.
8. The author's REVIEW READY comments.
9. Executable evidence regenerated at this head.
10. Only then, the earlier public reports: R269-1, R269-2 and R268-2 (and R268-1 through their disposition tables).

I did not read any private author material, lane scratchpad or other reviewer's working files.

## Focus: criterion 3's arbiter evidence

The check and its observer:

- `tb/verilator/milan_dp/sim_nxn.cpp:575-593`: `step()` sorts each tuple the arbiter delivers into five records:
  - STREAM_INPUT bitmap (index < 64);
  - STREAM_OUTPUT bitmap (index < 64);
  - AVB_INTERFACE 0;
  - CLOCK_DOMAIN 0;
  - `pp_ctr_evt_other_n` for everything else (`:590-591`).

  Together the five are a complete partition of {type, index}.
- `sim_nxn.cpp:3481-3499` clears all five, raises the lever and then requires:
  - STREAM_INPUT exactly `1 << N`;
  - STREAM_OUTPUT none;
  - neither AVB_INTERFACE 0 nor CLOCK_DOMAIN 0;
  - no other tuple.

How the RTL side works, and why the window is complete:

- The arbiter at `hdl/milan/milan_datapath.sv:7206-7301` has no ready handshake. It presents one tuple per cycle, combinationally from registered pending bits, and the tuple is cleared at the next edge.
- So sampling once after each rising edge sees every delivery exactly once.
- `crf_lever()` (`sim_nxn.cpp:3376-3384`) advances time only through `axi_write()` and `step()`. So every edge in the window is recorded.
- Instrumentation probe H2 shows the window is 70 cycles. The CRF tuple arrives at step 7, as {0x0005, 4} on nxn and {0x0005, 8} on nxn8.
- The worst-case drain for any extra tuple raised by the same pulse is at most 20 cycles on 8x8. The window has 63 cycles of margin after the CRF tuple.

Reviewer mutants, all generated with exact-once anchors (`scripts/gen_mutants.py`), built through the suite's own recipe lines (`scripts/probe.mk`) with the pinned simulator 5.050:

| Mutant | Edit | nxn | nxn8 | Red check |
|---|---|---|---|---|
| X01 | the CRF pulse also raises AAF STREAM_INPUT 0 | 1708/1 | 3136/1 | "...as STREAM_INPUT N only" (got 0x11 / 0x101) |
| X02 | ...also raises AAF STREAM_INPUT N-1 | 1708/1 | 3136/1 | same (0x18 / 0x180) |
| X03 | the pulse delivered at N-1 **instead of** N | 1708/1 | 3136/1 | same (0x8 / 0x80) |
| X04 | ...also raises STREAM_OUTPUT N (the CRF output) | 1708/1 | 3136/1 | "...and as no STREAM_OUTPUT row" |
| X05 | ...also raises STREAM_OUTPUT 0 | 1708/1 | 3136/1 | same |
| X06 | ...also raises AVB_INTERFACE 0 | 1708/1 | 3136/1 | "...nor AVB_INTERFACE 0 or CLOCK_DOMAIN 0" |
| X07 | ...also raises CLOCK_DOMAIN 0 | 1708/1 | 3136/1 | same |
| X08 | ...also raises AVB, handed out as {AVB_INTERFACE, 1} | 1708/1 | 3136/1 | "...nor any tuple of another type or index" |
| X09 | the CRF row handed out as type 0x000E | 1708/3 | 3136/3 | "N only" and "another type or index" |
| X10 | the CRF row handed out as STREAM_INPUT N+1 (undeclared) | 1708/2 | 3136/2 | "N only" (0x20 / 0x200) |
| X11 | the CRF row handed out at index N+64 | 1708/2 | 3136/2 | "N only" and "another type or index" |
| X13 | the CRF dirty source tied off | 1708/1 | - | "N only"; on notify all 11 `[NOTIFY-CRF]` red, A's copy included |
| X14 | the pending-clear loop stops below the CRF row | - | - | notify 146/2: both quiet checks (4 pushes against 2) |
| X12 | ...also raises STREAM_OUTPUT N, but 200 cycles late | 1708/0 | - | characterisation: green by design, outside the 70-cycle window (see S2) |

Harness probes:

| Probe | Result | Shows |
|---|---|---|
| H1: the fifth record removed, run against X08 | nxn 1708/0 (green) | The new `pp_ctr_evt_other_n` record is what catches a tuple the four named records cannot hold. |
| H3: one counters-block bit of A's logged push flipped | notify 146/1; only "...and so is A's copy" is red | The new check reads A's copy and compares it byte for byte from offset 38. |
| H2: instrumentation only | nxn 1708/0, nxn8 3136/0, notify 146/0 | The window length and delivery step above, and the `uns_log` state behind S1. |

The unmutated head passes every broad leg and the timed leg:

| Leg | Result | `[CTRS-CRF]` ok | `[NOTIFY-CRF]` ok |
|---|---|---|---|
| nxn | 1708/0 | 75 | - |
| nxndv | 1710/0 | 75 | - |
| nxn8 | 3136/0 | 75 | - |
| nxn4c | 1708/0 | 75 | - |
| notify | 146/0 | - | 11 |

On notify the CRF row's two pushes are 997 ms apart.

Claims checked against these results:

- REGISTER_MAP.md:897-907 (criterion 3) and :908-919 (criterion 4's mutation list), README.md:513-518 and :527-539, and the comments at sim_nxn.cpp:567-571 and :3473-3480.
- Each sentence is true of the checks that run. Every mutation class the docs name is among X01-X14 or the exchanges.

The binding exchanges, re-run because `sim_nxn.cpp` changed after the round that banked them:

- **nxn:** all 45 pairwise exchanges of the ten `KL_crf_rx` tally bindings turn **both** exchanged quadlets red in the event arm (45/45, `receipts/30_swaps_nxn_graded.txt`).
- **nxn8:** a sample of 6 of the 45, spread across all ten quadlets, gives 6/6.

## Findings

No BLOCKER, MAJOR or MINOR finding is open.

The SUGGESTIONs below are optional and do not affect coverage.

### S1 - SUGGESTION - Tests, Robustness (new)

```text
[R269] SUGGESTION Tests, Robustness - tb/verilator/milan_dp/sim_nxn.cpp:1322,1330-1332 - n1 points into uns_log across a solicited exchange that may append to it
```

- **Authority/evidence:**
  - `n1 = notify_last(...)` (`:1322`) returns a pointer into `uns_log`, which is a `std::vector<std::vector<uint8_t>>`.
  - `aecp_xact_from` (`:1330`) reaches `await_aecp`, which does `uns_log.push_back` for any unsolicited frame it meets (`:837`).
  - `n1` is used after that (`:1332`).
  - H2 measures size 2 and capacity 2 at that point. So one appended frame would reallocate the vector and leave `n1` dangling.
  - At head no frame arrives (2 -> 2), so the result is deterministic today. The author disclosed the pattern in the PR body. It dates from this PR's round 0, and the base-era `[NOTIFY]` has the same shape.
- **Impact:** undefined behaviour in a check if a later change makes any descriptor push during that exchange. The most likely effect is a spurious red or a crash, not a false green.
- **Suggested outcome:** take `n1` after the exchange, or copy the frame, here and in the base-era `[NOTIFY]` content bar. That is the separate Issue the author proposes.
- **Verification:** H2 again shows the pointer is taken after any append. The legs stay green.

### S2 - SUGGESTION - Tests, Docs (new)

```text
[R269] SUGGESTION Tests, Docs - tb/verilator/milan_dp/sim_nxn.cpp:559-571 - the five delivery records cover step()-driven cycles only
```

- **Authority/evidence:**
  - Only `step()` records deliveries. `inject()` (`:744`), `await_aecp()` (`:823`) and `drain_tx()` (`:853`) advance the clock through `lo()`/`hi()` and record nothing.
  - The bind-edge window is entirely `step()`-driven, 70 cycles, with the CRF tuple at step 7. So criterion 3's claim, which is scoped "in that window", holds.
  - A tuple raised later, such as X12 at 200 cycles, is outside the window and stays green.
- **Impact:** a future window that includes a GET_COUNTERS exchange or a PDU injection would under-record. The comment "the five account for every tuple" would then mislead.
- **Suggested outcome:** say in the observer comment that the records see only `step()`-driven cycles. Optionally state the window length.
- **Verification:** re-read the comment against `step()`, `inject()`, `await_aecp()` and `drain_tx()`.

### S3 - SUGGESTION - Robustness, Tests (retained: R269-2 S1 = R268-2 S6)

```text
[R269] SUGGESTION Robustness, Tests - hdl/milan/milan_datapath.sv:3524-3526,7206-7216 - no leg elaborates a crf_sink: false shape
```

- **Evidence:**
  - I generated a 4x4 shape with `clocking.crf_sink: false` in scratch with the builder (4 sinks, 5 sources).
  - It passes the simulator's elaboration stage with no error-class, UNDRIVEN or USERERROR diagnostic.
  - `sim_nxn.cpp` then fails to compile, because it names `crf_intrcnt_w`, which the guard legitimately leaves unread (`receipts/22_nocrf_shape_probe.txt`).
- **Impact:** "A shape that declares no CRF sink serves no such row" (REGISTER_MAP.md:867-868) is evident from the code but not executed.
- **Suggested outcome:** a no-CRF leg, or harness guards on the shape.

### S4 - SUGGESTION - Docs (new)

```text
[R269] SUGGESTION Docs - scripts/port_docs.budget:21-22 (and the six entries removed after :37) - the regenerated budget also drops stale pre-existing entries
```

- **Evidence:**
  - The regeneration removes `chan_tdm_render.frames_o`, `.overruns_o` and `.underruns_o`, which were already connected at base `ede8d48e` (milan_datapath.sv:6410-6439 there).
  - It also moves the hdl port total by 63 and the processor total by 3, more than this change alone.
  - `check_port_contracts.py` passes at head (`receipts/10_check_port_contracts.txt`). The file is tool output, and the ratchet only moves down.
- **Impact:** none on the product. A cold reviewer cannot see from the PR body why unrelated budget lines moved.
- **Suggested outcome:** one line in the PR body saying so.

### Retained SUGGESTIONs (unchanged at this head)

| ID | Lenses | Artifact | State at this head |
|---|---|---|---|
| S5 (R269-2 S2 = R268-2 S4) | Tests | sim_nxn.cpp:1354 | The release floor is still `990L * kMsCycTb` under the label "no earlier than one second". The header at `:1069` now says "about 1000 ms", which resolves the header half. Measured 997 ms. |
| S6 (R269-2 S4 = R268-2 S5) | Tests | milan_datapath.sv:7288-7299 | The round-robin no-starvation property still has no discriminating check. I did not re-probe it: neither the arbiter RTL nor any check of it changed since that round. |
| S7 (R269-2 S5 = R268-2 S1) | Tests, Docs | sim_nxn.cpp:3629-3630 | `kCrfSilenceCyc` and `kFabricMsCyc` are still literals. They fail closed at another clock. |
| S8 (R268-2 S3) | Tests | sim_nxn.cpp:3337-3351 | The tally wires are still reached through non-public model members, so removing a reader is a compile failure rather than a named red check. It fails closed. |

## Clean-lens evidence

```text
[R269] PASS Conformance - hdl/milan/milan_datapath.sv:3511-3552,5441-5501,7184-7301; tests/features/counters_contract_milan.feature:69-103; docs/reference/REGISTER_MAP.md:876-919 (criteria 1-4 verbatim vs base ede8d48e); receipts/23,20 - mask 0xF3F at the Table 7-157 offsets with quadlets 6/7 unclaimed; 32-bit served words and wrap; era wipe on not-bound -> bound; NO_SUCH_DESCRIPTOR at N+1; Table 5.22 push as {STREAM_INPUT, N} only (X01-X11 red), to both controllers, at most once per second (997 ms), then quiet (X14 red)
[R269] PASS RTL - hdl/milan/milan_datapath.sv:1790-1796,3327-3371,3511-3552,5441-5501,7184-7301; hdl/ieee1722/crf/KL_crf_rx.sv (comment-only diff); receipts/22 - one clock (crf_rx on axis_clk, no crossing), reset of the new pending width, generate guard for both shape branches (no-CRF branch elaborates), round-robin arithmetic (pick < 2*EVT_N, rr < EVT_N), 16-bit type/index, mux exclusivity (ctr_sin_w guards index < N_STREAMS), word convention matching the AAF block
[R269] PASS Robustness - tb/verilator/milan_dp/sim_nxn.cpp:3481-3499,3600-3650,1314-1360; hdl/milan/milan_datapath.sv:3524-3526,7255-7274; receipts/20,21,22 - malformed PDUs (type-2 rejects), min/max (0xFFFFFFFF -> 0), invalid ordering (sequence gaps), reset during activity (era wipe), repeated pulses absorbed while pending, wrong index/type deliveries (X03,X09-X11), feature-disabled shape (S3), the 100 ms silence path (real last millisecond)
[R269] PASS Tests - tb/verilator/milan_dp/sim_nxn.cpp:563-593,1314-1360,3305-3650; receipts/20,21,23,30,31,32 - every new check can fail for its defect (X01-X14, H1, H3), 45/45 exchanges red at both quadlets on nxn and 6/6 sampled on nxn8, all broad legs and notify green at head, H1 shows the fifth record is load-bearing
[R269] PASS Docs - docs/reference/REGISTER_MAP.md:31-35,136-142,841-919; tb/verilator/milan_dp/README.md:502-539; CHANGELOG.md; docs/reference/{MILAN_COMPLIANCE_MATRIX,FR_NFR,REGISTER_MAP_CLASSES}.md; docs/testing/MILAN_V12_AUDIT_2026-08-16.md B4; docs/MILAN_V12_ROADMAP.md; docs/ENDSTATION_BUILDER.md; configs/*.yaml:103/139/153; receipts/11 - every claim matches what runs; docs_check, check_em_dash --base ede8d48e, check_doc_style, gen_module_matrix --check exit 0; open S2/S4 are optional
```

## Prior public findings

| Prior item | Disposition at this head | Evidence (this round) |
|---|---|---|
| R269-2 F1 MINOR = R268-2 F1 MINOR (Tests, Docs): "and as nothing else" and "byte-identical" claimed beyond the checks | **RESOLVED** | The check is strengthened (sim_nxn.cpp:3481-3499, observer `:567-591`). The earlier surviving mutants `ve-also-ckd`/`dirty_also_ckd` and `ve-also-sout`/`dirty_also_sout_n` are my X07 and X04, now red on nxn and nxn8, as are X01-X03, X05, X06 and X08-X11. The A copy is compared (`:1333-1334`; H3 red, X13 red). REGISTER_MAP.md:897-919, README.md:513-539 and the harness comments now describe exactly this. |
| R269-1 F1 MAJOR = R268-1 F1 MINOR (Conformance, Tests, Docs): permuted `KL_crf_rx` bindings undetectable | **RESOLVED** (re-proved at this head) | 45/45 exchanges red at both quadlets on nxn and 6/6 sampled on nxn8 (receipts 30-32). |
| R268-1 F2 MINOR: `[NOTIFY-CRF]` cannot fail for a row that keeps pushing | **RESOLVED** | X14 (the pending-clear loop stops below the CRF row) is red on notify, with 4 pushes against 2, to B and to A. |
| R268-1 F3 MINOR: REGISTER_MAP opening status lists the CRF bank as a gap | **RESOLVED** | REGISTER_MAP.md:31-35 and :136-142. |
| R269-2 S3 = R268-2 S7: config comments point at closed B4 | **RESOLVED** | configs/endstation_arty_4x4.yaml:103, endstation_arty_8ch.yaml:139 and endstation_ax7101_8x8.yaml:153 now read "audit B3". |
| R268-2 S2: A's copy counted, not compared | **RESOLVED** | Same as the F1 row. |
| R269-2 S6: PR body contradicts itself about closing #529 | **RESOLVED** | The body now says "Relates to #529 (it stays open...)" in both places. GitHub records no closing reference (read-only query: `[]`). |
| R269-2 S1 = R268-2 S6: no `crf_sink: false` leg | RETAINED as S3 | receipts/22 |
| R269-2 S2 = R268-2 S4: 990 ms floor | RETAINED as S5 (the header half resolved) | sim_nxn.cpp:1354, :1069 |
| R269-2 S4 = R268-2 S5: round-robin no-starvation | RETAINED as S6 | unchanged RTL and checks |
| R269-2 S5 = R268-2 S1: silence literals | RETAINED as S7 | sim_nxn.cpp:3629-3630 |
| R268-2 S3: non-public tally wires | RETAINED as S8 | sim_nxn.cpp:3337-3351 |
| Earlier items the R269-2 and R268-2 tables already record as resolved (R269-1 S4 frozen criteria quoted, R269-1 S5 = R268-1 S3 `Closes #529`) | still resolved | REGISTER_MAP.md:876-919 quotes are verbatim against the base; the PR body has no closing keyword. |

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | milan_datapath.sv gather row, CRF instance and arbiter; counters contract feature; frozen criteria 1-4; X01-X14 and head legs | R269-3 | `31e62ffead16e43d648993278b0ab9190d99b672` |
| RTL | CLEAN | milan_datapath.sv:1790-1796, 3327-3371, 3511-3552, 5441-5501, 7184-7301; KL_crf_rx.sv diff; no-CRF shape elaboration | R269-3 | `31e62ffead16e43d648993278b0ab9190d99b672` |
| Robustness | CLEAN | event, wrap and era arms; wrong-row, wrong-type and wrong-index mutants; the no-CRF shape; the 100 ms silence path | R269-3 | `31e62ffead16e43d648993278b0ab9190d99b672` |
| Tests | CLEAN | sim_nxn.cpp observer, bind edge, `[NOTIFY-CRF]` and event arm; 14 RTL mutants, 3 harness probes, 45+6 exchanges; five head legs | R269-3 | `31e62ffead16e43d648993278b0ab9190d99b672` |
| Docs | CLEAN | REGISTER_MAP, milan_dp README, CHANGELOG, compliance matrix, FR_NFR, REGISTER_MAP_CLASSES, audit B4, roadmap, builder page, three configs; docs gates | R269-3 | `31e62ffead16e43d648993278b0ab9190d99b672` |

## Probes and receipts

- Everything was built in a disposable tree extracted from the exact head. The processor copy's 222 blob IDs are identical to the pinned gitlink `424c688f`.
- Pinned simulator: 5.050, wrapper sha256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f` (`receipts/01`).
- At most 8 parallel jobs: 4 builds of 2 jobs each.

| Receipt | Content |
|---|---|
| `receipts/00_baseline_state.txt`, `90_restoration_check.txt` | Clone state before the probes and after them |
| `receipts/10_check_port_contracts.txt`, `11_focused_gates.txt` | 12 read-only gates at head, all exit 0 (port contracts, docs_check, check_em_dash --base ede8d48e, check_doc_style, check_cpp_idiom, check_sv_idiom, measure_naming --check, measure_test_evidence --check, check_hygiene --check, check_rtl_source_lists, lint_rtl --check, gen_module_matrix --check), with the clone clean afterwards |
| `receipts/20_mutants_and_probes.tsv`, `logs/*.run.log.gz` | Every mutant and probe run, its tally and every FAIL line, plus the full logs |
| `receipts/21_window_and_log_instrumentation.txt` | H2 output |
| `receipts/22_nocrf_shape_probe.txt`, `mutants/endstation_arty_4x4_nocrf.yaml` | The no-CRF shape probe |
| `receipts/23_head_legs.tsv`, `logs/head_*.run.log.gz` | Head legs |
| `receipts/30_*`, `31_*`, `32_*`, `mutants/exchanges_all45.diff`, `mutants/SWAPS.tsv` | Exchanges |
| `receipts/40_hosted_contexts_observed.txt` | A read-only snapshot of the exact-head hosted contexts. Every executed job concluded SUCCESS; "Physical gPTP (nightly and manual)" was SKIPPED. Observed only; the manager owns acceptance. |
| `receipts/50_independent_verdict_before_prior_findings.md` | The verdict and ledger written before any earlier report was read |
| `mutants/*.diff`, `mutants/MUTANTS.tsv` | Each mutant as a unified diff against the head |
| `scripts/` | `gen_mutants.py`, `gen_swaps.py`, `grade_swaps.py`, `probe.mk`, `run_leg.sh`, `focused_gates.sh`, `collect_receipts.sh` |

## Real limits

- **No hardware.**
  - Physical calibration: NOT RUN.
  - Milan-controller confirmation on silicon (#117, and #529's closing condition): not done.
  - Skipped field or physical contexts are not hardware proof.
- **Not run here:**
  - the full parent, processor, gPTP, Yosys and builder banks;
  - `act` and the host `act_ci` self-test;
  - the vendor front-end parse (`xvlog_gate`);
  - timing and area;
  - the milan_dp legs that do not compile `sim_nxn.cpp` (obj_dir, nolpf, prune, ax1x1, aclk, gptp, gptplat, render mutants);
  - the pp_shadow, milan_dp_render and crf_rx suites, and behave.

  `hdl/` is byte-identical from `f8155775` to this head. I do not claim or infer the manager's source banks for this head.
- **Exchange coverage:** all 45 exchanges on nxn, 6 of 45 on nxn8, none on nxndv or nxn4c.
- **Exclusivity is proven for the bind-edge window only:** 70 `step()`-driven cycles (S2, X12).
- **H3 is a harness-level corruption,** not an RTL fault in the processor's fan-out.
- **Out of scope, pre-existing, not a finding against this PR:** REGISTER_MAP.md:828-829 still calls the CRF sink "ACMP listener sink 1". On N x N shapes it is sink `N_STREAMS` (`milan_datapath.sv:5000-5003` selects `CRF_SNK_IDX_C`). This is candidate new work for the manager. #541 already tracks the validation-error unlock wording.

## Pending manager duties

- Publish this report.
- Publish the running source static, builder and native banks for this head. They are separate from this review.
- Accept the hosted and `act` evidence on the exact head.
- At the merge turn, build and validate the candidate from live dev `26d855a9176d63625e6635a029a0c44e3d57ce9a` and this head (source base `ede8d48e`) with the full local bar.
- Obtain the second positive review and the completion-ledger acceptance.
- Obtain the maintainer's merge authorization.
- Run post-merge containment.
- After the merge: silicon re-flash and a Milan-controller confirmation before #529 closes.
- Optionally file S1 as its own Issue, as the author proposed.

## Clone restoration

- No probe edited the review clone. The mutants and builds lived only in the scratch tree.
- The gates created an ignored `scripts/__pycache__/`, which I removed.
- At the end:
  - HEAD `31e62ffe`, tree `4d32ede1`;
  - the index digest equals the baseline;
  - the worktree and index equal HEAD;
  - no tracked file hashes differently from its index blob;
  - no assume-unchanged or skip-worktree flags;
  - no untracked or ignored files;
  - gitlinks unchanged: `external efeb541a` (uninitialised, as at start), `gptp-processor c1b61743`, `protocol-processor 424c688f` and `third_party/verilog-axis 48ff7a7e`, each clean.

  See `receipts/90_restoration_check.txt`.

## Reproduce

```sh
# a disposable tree from the exact head, with the three pinned submodules extracted
# into it and a local index in protocol-processor/ (pp_srcs.py reads git ls-files)
python3 scripts/gen_mutants.py <tree> <out>      # X01-X14, H1-H3
python3 scripts/gen_swaps.py <tree> <out>        # the 45 exchanges
cp scripts/probe.mk <tree>/tb/verilator/milan_dp/
VERILATOR=<pinned 5.050> VERILATOR_JOBS=2 \
  scripts/run_leg.sh <tree> nxn obj_X04 <log>/X04 <out>/X04_also_sout_n/milan_datapath.sv
python3 scripts/grade_swaps.py <out>/SWAPS.tsv <logdir> nxn
```

R269-3 FINISHED
