[R268] POSITIVE - exact head 31e62ffead16e43d648993278b0ab9190d99b672

Round R268-3: the internal, cleared-context independent re-review of issue #529 / PR #534 after correction round 2.

## Scope

- **Head:** `31e62ffead16e43d648993278b0ab9190d99b672`, tree `4d32ede1eba65adcee359d00751ddadf3314a36b`. The PR is ready (not draft), base `dev`. GitHub records no closing reference: the body says "Relates to #529".
- **Source base:** `ede8d48ecd7c7f589a14b957951f040d92c99c70`. Nine one-line commits, linear on the base. Correction round 2 is three commits on `535701a0`:
  - `b65030e0` (harness);
  - `78cdff20` (docs);
  - `31e62ffe` (three config comments).
- **RTL:** `git diff 535701a0 HEAD -- hdl` is empty. The datapath sha256 is `2b729369...`, the same as the previous round. The whole RTL diff from base was re-read at this head.
- **Gitlinks:** unchanged from base.
  - protocol-processor `424c688f`;
  - gptp-processor `c1b61743`;
  - third_party/verilog-axis `48ff7a7e`.
- **Lenses:** all five applied at this head.
- **Verdict: POSITIVE.**
  - No BLOCKER, MAJOR or MINOR is open.
  - One new SUGGESTION (S1) and four retained SUGGESTIONs, none of which affects coverage.
  - The focus finding (R268-2 F1 = R269-2 F1, MINOR, Tests and Docs) is resolved at this head. So is every other prior finding.

## Reconstruction order

1. AGENTS.md, CONTRIBUTING.md, docs/README.md.
2. Issue #529:
   - the body;
   - the A10 assignments for A204, A216 and A222;
   - A204 TAKEN and REVIEW READY;
   - A216 REVIEW READY and A222 REVIEW READY.
3. The frozen acceptance: `docs/reference/REGISTER_MAP.md` "Closure criteria for the CRF Stream Input counter gap", items 1-4, read at base `ede8d48e` (`:853-861` there).
4. Authorities:
   - Milan v1.2 5.3.8.10 (Table 5.6, the reset-on-bind sentence, the 32-bit wrap);
   - Milan v1.2 5.4.2.25 (Table 5.16) and 5.4.5 (Table 5.22, at most one GET_COUNTERS push per descriptor per second);
   - IEEE 1722.1-2021 Table 7-157, the Stream Input offsets and valid bits.
5. Interfaces:
   - the `KL_crf_rx` ports and banner;
   - in `milan_datapath.sv`: the GET_COUNTERS gather face, the `crf_rx` instance, and the Table 5.22 descriptor arbiter in front of `KL_pp_shadow`.
6. `git diff ede8d48e..31e62ffe`, the per-commit history, and the delta `git diff 535701a0..31e62ffe`.
7. Public evidence, read only:
   - the A222 correction packet at `83b3a839` `review-evidence/529-r1/correction-a222`, read through the API, with no fetch into the review clone;
   - the manager's issue and PR comments;
   - the exact-head hosted check runs.
8. Prior public review findings (R268-1, R269-1, R268-2, R269-2) were read only after this round's own pass over the diff and its own mutants and probes. That pass's provisional verdict was recorded before they were opened. No current-round report of another reviewer was read.

## Focus: criterion 3's evidence (R268-2 F1 = R269-2 F1)

### What the check now is

- **Observer.** The arbiter observer in `step()` (`tb/verilator/milan_dp/sim_nxn.cpp:562-594`) classifies every cycle's delivery into exactly one of five records:
  - the STREAM_INPUT bitmap (index < 64);
  - the STREAM_OUTPUT bitmap (index < 64);
  - AVB_INTERFACE 0;
  - CLOCK_DOMAIN 0;
  - `pp_ctr_evt_other_n`, for every other type, or an index those records keep no bit for.

  The chain is exhaustive, so no {type, index} the arbiter can hand over escapes all five.
- **Arm.** The bind-edge arm (`sim_nxn.cpp:3474-3500`) clears all five, raises the lever, then requires:
  - STREAM_INPUT exactly `1 << N`;
  - no STREAM_OUTPUT row;
  - neither AVB_INTERFACE 0 nor CLOCK_DOMAIN 0;
  - `other` equal to 0.
- **Window.** Everything inside `crf_lever(true)` (three AXI writes and 64 idle steps) runs through `step()`. This round's harness probe (`receipts/hprobe/`, diff `receipts/hprobe.diff`) prints the window's deliveries:
  - The window is 70 observed steps.
  - The CRF row is handed over at step 6, as {0x0005, 4} on nxn and {0x0005, 8} on nxn8.
  - A tuple raised with the pulse drains within `PP_CTR_EVT_N_C` cycles (12 on nxn, 20 on nxn8), well inside the window.

### This round's own mutants: the check fails for any other descriptor row or index

- **The mutant.** A disposable RTL mutant (`scripts/mk_ghost.py`, diff `receipts/ghost-mutant.diff`) leaves the arbiter's pick, pending and round-robin logic intact. It adds one extra delivery {TY, IX} per CRF dirty pulse at the lowest priority, chosen at run time by plusarg. A replace mode also drops the pulse from the STREAM_INPUT row.
- **The runs.** One build per shape, 28 cases each (`scripts/ghost_matrix.sh`). The tables are `receipts/ghost-matrix-nxn.md` and `receipts/ghost-matrix-nxn8.md`, and the raw logs are in `receipts/ghost/`.

| Case | Extra or replacing tuple | nxn (N = 4) | nxn8 (N = 8) | Check that turns red |
|---|---|---|---|---|
| c0 control | none (ghost off) | 1708/0 | 3136/0 | - |
| c1 control | the CRF row delivered only through the ghost path, {5, N} | 1708/0 | 3136/0 | - |
| c2 | the CRF pulse dropped (dirty source removed) | 1708/1 | 3136/1 | STREAM_INPUT N only |
| c3 | extra duplicate {5, N} | 1708/0 | 3136/0 | - (multiplicity is not claimed) |
| extra STREAM_INPUT | {5, 0}, {5, N-1}, {5, N+1}, {5, 63} | red | red | STREAM_INPUT N only |
| extra STREAM_INPUT, index >= 64 | {5, 64}, {5, 64+N}, {5, 0xFFFF} | red | red | another type or index |
| extra STREAM_OUTPUT | {6, 0}, {6, N} (the CRF output), {6, N+1}, {6, 63} | red | red | no STREAM_OUTPUT row |
| extra STREAM_OUTPUT, index >= 64 | {6, 64} | red | red | another type or index |
| extra AVB / CLOCK_DOMAIN index 0 | {9, 0}, {0x24, 0} | red | red | AVB_INTERFACE 0 or CLOCK_DOMAIN 0 |
| extra AVB / CLOCK_DOMAIN index 1 | {9, 1}, {0x24, 1} | red | red | another type or index |
| extra other types | {0, 0} ENTITY, {1, 0} CONFIGURATION, {0xFFFF, 0xFFFF} | red | red | another type or index |
| replace | {5, N-1}, {5, N+1} | red | red | STREAM_INPUT N only |
| replace | {5, 64+N}, {0x24, N} | red | red | STREAM_INPUT N only, and another type or index |
| replace | {6, N} | red | red | STREAM_INPUT N only, and no STREAM_OUTPUT row |

- **Result.** All 24 foreign-tuple cases and c2 are red on both shapes.
- **Isolation.** In every red run, the only `[FAIL]` lines are the named bind-edge checks, and nothing else in the 1708 or 3136 checks moves. The c0 and c1 controls are green, so the probe alone perturbs nothing and the ghost path delivers faithfully. c1 is also green on `obj_notify` (146/0).
- **Second mutation form.** The pending-bit form is the one the docs name: the pulse also raises another row's pending bit (`scripts/mk_pend.py`, diffs `receipts/pf-*.diff`, logs `receipts/pf/`).
  - `sout-n`, `aaf-all`, `avb` and `ckd` are each red on nxn, with exactly one `[FAIL]` (1708/1).
  - `stuck` (the CRF row's pending bit never cleared) is green on nxn, as the docs assign it to the timed leg. On `obj_notify` it is red on "...no further push to B in the next two seconds" and "...nor to A" (4 pushes against 2).
- **Author receipts.** The A222 receipts agree (`correction-a222/logs/mutants/SUMMARY.tsv`): the four extra-tuple mutants survive the `535701a0` harness (1705/0) and are killed by the head harness on nxn and nxn8.

### The notification half (R269-2 F1, second part = R268-2 S2)

- `sim_nxn.cpp:1333-1334` compares A's copy against the same solicited answer as B's.
- **Probe.** This round's probe (`scripts/mk_acopy.py`, `receipts/acopy-probe.diff`, `receipts/probe/acopy-notify.log`) flips one bit of A's logged push inside the FRAMES_RX quadlet. It fails only "...and so is A's copy" (146 checks, 1 failure).
- The dropped CRF pulse on `obj_notify` turns all 11 `[NOTIFY-CRF]` checks red (`receipts/ghost/c2-replace-by-nothing-notify.log`).

### The docs claim what the check proves

- **Criterion 3.** `REGISTER_MAP.md:897-907` reads "as {STREAM_INPUT, `N_STREAMS`} and as nothing else", followed by:
  - the enumerated exclusions, ending "no tuple of any other type or index may appear";
  - "each copy byte-identical".

  Each sentence is true of `sim_nxn.cpp:3474-3500` and `:1314-1364` as shown above.
- **README.** `tb/verilator/milan_dp/README.md:502-537` says the same. Its mutation list names the extra-tuple mutants. Each named class is red in this round's matrix: the AAF inputs (`aaf-all`), STREAM_OUTPUT `N_STREAMS`, AVB_INTERFACE 0, CLOCK_DOMAIN 0, and a tuple at an undeclared index.
- **Harness comment.** The comment at `sim_nxn.cpp:3474-3480` states the five-record exhaustiveness, which holds.
- **Scope of the claim.** Two properties are outside it, and the docs do not claim them:
  - The multiplicity of {STREAM_INPUT, N} inside the window: c3 is green. A row that keeps re-delivering is caught by `[NOTIFY-CRF]` (`stuck` red on notify).
  - A foreign tuple handed over after the 70-step window: the claim is scoped "in that window".

## Full head: per-lens results

```text
[R268] PASS Conformance - hdl/milan/milan_datapath.sv:3511-3552,5438-5501,7184-7301; docs/reference/REGISTER_MAP.md:870-919 against the frozen criteria at ede8d48e REGISTER_MAP.md:853-861; receipts/baseline/head-{nxn,nxndv,nxn8,nxn4c,notify}.log - counters_valid 0xF3F with the ten at their IEEE 1722.1-2021 Table 7-157 quadlets (0,1,2,3,4,5,8,9,10,11) and the two tv tallies unclaimed; 32-bit wrap of both update laws; not-bound to bound wipe (Milan 5.3.8.10); NO_SUCH_DESCRIPTOR with the empty body at N+1; the dirty source delivered as {STREAM_INPUT, N} alone and pushed to both registered controllers at most once a second, then quiet (Table 5.22); criteria 1-4 met at source level
[R268] PASS RTL - hdl/milan/milan_datapath.sv:1787-1799,3326-3352,3511-3552,5438-5501 (crf_rx on axis_clk/axis_resetn),7184-7301; hdl/ieee1722/crf/KL_crf_rx.sv (comment-only diff); receipts/port-contracts-{head,base}.txt - same clock domain as the gather server and the arbiter (no new crossing); 32-bit widths; the CRF arm type-disjoint from the STREAM_OUTPUT/AVB/CKD arms and index-disjoint from ctr_sin_w (< N_STREAMS); the ACMP_SINKS_C > N_STREAMS guard covers CRF_SNK_IDX_C's fallback to 0; PP_CTR_SIN_N_C sizing, pick, clear and round-robin arithmetic stay within PP_CTR_EVT_N_C for both generate branches; port-contract gate OK at head
[R268] PASS Robustness - milan_datapath.sv:3524-3526,7206-7217,7255-7274; receipts/ghost-matrix-{nxn,nxn8}.md; receipts/pf/pf-stuck-notify.log; receipts/baseline/*.log - undeclared index N+1 refused with an empty body; wrap from 0xFFFFFFFF to 0; the era wipe on the bind edge; re-pulses while pending absorbed and a stuck row caught; a shape without the CRF sink drops the pulse by construction (g_ctr_no_crf_dirty); out-of-range tuples ({5,0xFFFF}, {0xFFFF,0xFFFF}) handed to the processor cause no collateral failure anywhere in either leg
[R268] PASS Tests - tb/verilator/milan_dp/sim_nxn.cpp:562-594,1314-1364,3290-3314,3474-3500,3531-3646; receipts/ghost-matrix-*.md, receipts/pf/, receipts/swap-summary-nxn.md (45/45), receipts/swap-summary-nxn8.md (9/9), receipts/probe/acopy-notify.log, receipts/hprobe/, receipts/baseline/ - every new check has a failing arm; the bind-edge exclusivity is red for every tuple class on two shapes with isolated failures; each of the 45 KL_crf_rx output-binding exchanges reddens both of its quadlets on nxn; the NOTIFY-CRF release-then-quiet and A-copy checks fail for their defects; no existing check was removed or weakened; five sim_nxn legs green; check_cpp_idiom 0 <= 0
[R268] PASS Docs - docs/reference/REGISTER_MAP.md:31-35,136-142,182,819-919; tb/verilator/milan_dp/README.md:502-537; docs/reference/MILAN_COMPLIANCE_MATRIX.md:126,143; docs/testing/MILAN_V12_AUDIT_2026-08-16.md:210-231,384; docs/reference/FR_NFR.md:141; docs/reference/REGISTER_MAP_CLASSES.md:61-68,92,96; docs/MILAN_V12_ROADMAP.md:437-439; docs/ENDSTATION_BUILDER.md:1071; CHANGELOG.md:11,28-43; configs/endstation_{arty_4x4,arty_8ch,ax7101_8x8}.yaml:103/139/153; scripts/port_docs.budget; receipts/static-focused.txt - every claim matches the code and the executed evidence at this head; docs_check 0 findings; check_em_dash --base ede8d48e 0 findings over 164 added lines
```

Notes behind the PASS lines:

- **Leg coverage.** "Every `[CTRS-CRF]` check named here runs on the 4x4, divergent 4x4, 8x8 and shipping Arty 4x4 legs" (`REGISTER_MAP.md:873-874`) holds: the four broad legs each carry 75 `[CTRS-CRF]` lines and `obj_notify` carries 11 `[NOTIFY-CRF]` lines.
- **Budget file.** Besides the three `crf_rx` rows, `port_docs.budget` drops three `chan_tdm_render` rows and restates the hdl port count (1839 to 1902). That is base drift, not a change of this lane.
  - At base the gate already reports "the ratchet can be lowered ... 3 recorded connection(s) gained a rationale or left".
  - `--write-budget` at base produces exactly that diff (`receipts/port-budget-base-regenerated.diff`).

  So it is a monotone tightening that the regeneration folded in.
- **Timed-leg ordering.** `[NOTIFY-CRF]` is inserted before the departing-controller monitor on the timed leg (`sim_nxn.cpp:1196-1198`). The monitor re-bases on B's own command (`:1480-1486`), and A's silence before its first poll stays under 30 s. The monitor's window is therefore not biased, and the leg is 146/0.

## Findings

No BLOCKER, MAJOR or MINOR is open at this head.

### S1 - SUGGESTION - Tests - new

```text
[R268] SUGGESTION Tests - tb/verilator/milan_dp/sim_nxn.cpp:1322,1330-1332 - [NOTIFY-CRF] holds a pointer into the unsolicited log across a call that can append to it
```

- **Evidence.**
  - `n1` is taken from `notify_last(...)` at `:1322`, then `aecp_xact_from()` at `:1330` runs `await_aecp()`, which `push_back`s any unsolicited frame into `uns_log`. `n1` is then read at `:1331-1332`.
  - This round's probe (`receipts/hprobe/hprobe-notify.log`) shows `uns_log` exactly full at that point (size 2, capacity 2), and its storage UNMOVED across the exchange at this head. So the check reads live data today.
  - This code was added by this PR. The author disclosed the pattern publicly (A222 REVIEW READY), together with the base-era `[NOTIFY]` instance at `:1190-1195`.
- **Impact.**
  - None at this head.
  - Any unsolicited frame arriving during that exchange would reallocate the log, and `n1` would dangle. That is undefined behaviour, which under the usual allocator reads as a false red or a crash rather than a false green.
- **Suggested outcome.** Fetch B's pointer after the exchange, as the new A-copy check at `:1333-1334` already does.
- **Verification.** The timed leg stays 146/0. Rerun the A-copy probe for B's copy.

### Retained SUGGESTIONs (unchanged at this head; none affects coverage)

- **S2 - Tests. The silence constants are literals.**
  - Retained: R268-2 S1 = R269-2 S5.
  - `kCrfSilenceCyc` and `kFabricMsCyc` (`sim_nxn.cpp:3629-3630`) mirror `CLK_FREQ_HZ_P / 10` and `MILAN_CLK_FREQ_HZ / 1000` instead of coming from the recipe.
  - A different clock fails closed.
- **S3 - Tests. The ten tally wires are named through the model's internals.**
  - Retained: R268-2 S3.
  - `milan_datapath.sv:1792-1793` carries no public pragma, so a wire whose only reader is removed breaks the harness build rather than a named check.
  - Still fail-closed.
- **S4 - Tests. Arbiter no-starvation is ungraded.**
  - Retained: R268-2 S5 = R269-2 S4 = R268-1 S1.
  - No check discriminates the round-robin resume offset. `hdl/` and the arbiter tests are unchanged since those rounds.
- **S5 - Robustness, Tests. No leg elaborates a `crf_sink: false` shape.**
  - Retained: R268-2 S6 = R269-2 S1 = R268-1 S2 = R269-1 S1.
  - No tracked config disables the sink, so `g_ctr_no_crf_dirty` and the constant-false `ctr_crf_w` never run.

## Prior public findings

Each item was read after this round's own pass and is checked again at this head.

| Prior item | Disposition at this head | Evidence |
|---|---|---|
| R268-2 F1 = R269-2 F1, MINOR (Tests, Docs): the "and as nothing else" arbiter claim is stronger than its check | **RESOLVED** | The check strengthened (`sim_nxn.cpp:571,591,3482-3494`). 24 foreign-tuple cases and the dropped pulse are red on nxn and nxn8, with isolated failures. The pending-form `sout-n`/`aaf-all`/`avb`/`ckd` mutants are red. Docs `REGISTER_MAP.md:897-907` and `README.md:513-518` match the check. |
| R269-2 F1, second part (= R268-2 S2): A's push copy counted, not compared | **RESOLVED** | `sim_nxn.cpp:1333-1334`; the A-copy probe fails only that check. |
| R268-2 S4 = R269-2 S2: 990 ms floor against a ">= 1000 ms" header | **RESOLVED** | The header now reads "RELEASED about 1000 ms later" (`sim_nxn.cpp:1069`). The 990 ms floor is justified in place (`:1349-1354`). |
| R268-2 S7 = R269-2 S3: config comments point at audit B4 | **RESOLVED** | All three yaml lines now cite B3 only. No generated config carries a copy. |
| R269-2 S6: the PR body contradicts itself about closing #529 | **RESOLVED** | The PR body says #529 stays open until the silicon check; `closingIssuesReferences` is empty (`receipts/pr-534-body.txt`). |
| R268-2 S1 = R269-2 S5; R268-2 S3; R268-2 S5 = R269-2 S4; R268-2 S6 = R269-2 S1 | **RETAINED** as SUGGESTIONs S2, S3, S4, S5 | See above. |
| R269-1 F1 MAJOR = R268-1 F1 MINOR: permuted `KL_crf_rx` bindings invisible | **Still RESOLVED** | 45/45 exchanges are red on both quadlets on nxn, and a 9-exchange cover of all ten ports is red on both quadlets on nxn8 (`receipts/swap-summary-*.md`). |
| R268-1 F2 MINOR: `[NOTIFY-CRF]` cannot fail for a row that keeps pushing | **Still RESOLVED** | `stuck` is red on notify, 4 pushes against 2. |
| R268-1 F3 MINOR: the REGISTER_MAP opening status lists the CRF bank as a gap | **Still RESOLVED** | `REGISTER_MAP.md:31-35`. |
| R269-1 S4 (criteria paraphrased), R269-1 S5 / R268-1 S3 (`Closes #529`) | **Still RESOLVED** | Criteria 1-4 are quoted verbatim at `REGISTER_MAP.md:876-919`. The PR body says "Relates to". |

- **Out of scope, pre-existing.** The `KL_crf_rx` banner and the `CRF_CTRL` row say a validation error unlocks the sink, but the engine unlocks only on the 100 ms silence. This is tracked by open issue #541 and is not a finding against this head.
- **Disclosed by the author.** The pointer pattern in the base-era `[NOTIFY]` bar is outside this PR. The PR's own instance is S1.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Milan v1.2 5.3.8.10/Table 5.6, 5.4.2.25/Table 5.16, 5.4.5/Table 5.22; IEEE 1722.1-2021 Table 7-157; `milan_datapath.sv:3511-3552,5438-5501,7184-7301`; frozen criteria 1-4 at `ede8d48e` against `REGISTER_MAP.md:870-919`; five baseline legs | R268-3 | `31e62ffead16e43d648993278b0ab9190d99b672` |
| RTL | CLEAN | `milan_datapath.sv:1787-1799,3326-3352,3511-3552,5438-5501,7184-7301`; `KL_crf_rx.sv` diff (comments only); port-contract gate at head and base | R268-3 | `31e62ffead16e43d648993278b0ab9190d99b672` |
| Robustness | CLEAN | `milan_datapath.sv:3524-3526,7206-7217,7255-7274`; ghost matrix out-of-range tuples; `stuck` on notify; wrap, wipe and N+1 refusal in the baseline legs | R268-3 | `31e62ffead16e43d648993278b0ab9190d99b672` |
| Tests | CLEAN | `sim_nxn.cpp:562-594,1314-1364,3290-3314,3474-3500,3531-3646`; ghost matrix 28 cases x 2 shapes; 5 pending-form mutants; 45 + 9 binding exchanges; A-copy and window probes; five baseline legs; `check_cpp_idiom` | R268-3 | `31e62ffead16e43d648993278b0ab9190d99b672` |
| Docs | CLEAN | REGISTER_MAP.md, README.md (milan_dp), MILAN_COMPLIANCE_MATRIX.md, MILAN_V12_AUDIT_2026-08-16.md, FR_NFR.md, REGISTER_MAP_CLASSES.md, MILAN_V12_ROADMAP.md, ENDSTATION_BUILDER.md, CHANGELOG.md, three config comments, `port_docs.budget`, `KL_crf_rx.sv`/`milan_datapath.sv` comments; `docs_check`, `check_em_dash` | R268-3 | `31e62ffead16e43d648993278b0ab9190d99b672` |

Every lens was applied at this exact head and none has an open BLOCKER, MAJOR or MINOR. A later commit that touches a lens's scope un-covers that lens.

## Reproduced evidence at this head

Pinned simulator 5.050 (`receipts/tool-identity.txt`). At most 8 jobs ran at a time, in a disposable clone of the exact head. Each leg was built from its own `make -n run` recipe line (`scripts/leg.py`).

| Leg | Result | `[CTRS-CRF]` / `[NOTIFY-CRF]` lines |
|---|---|---|
| obj_nxn | 1708/0 | 75 |
| obj_nxndv | 1710/0 | 75 |
| obj_nxn8 | 3136/0 | 75 |
| obj_nxn4c | 1708/0 | 75 |
| obj_notify | 146/0 | 11 |

Static checks, focused on what this delta touches (`receipts/static-focused.txt`, `receipts/port-contracts-*.txt`):

- `docs_check.py`: 0 findings;
- `check_em_dash.py --base ede8d48e`: 0 over 164 added lines;
- `check_cpp_idiom.py`: every ratchet 0 <= 0;
- `git diff --check ede8d48e..HEAD`: clean;
- `check_port_contracts.py`: OK at head.

## Hosted evidence (exact head, read only)

- `receipts/hosted-check-runs.tsv` lists 22 check runs: 21 success and 1 skipped ("Physical gPTP (nightly and manual)").
- These completed with success: `rtl-fast`, `docs-check`, `docs-check-no-git`, `wire-accountability`, `elaborate`, `verilator-suites`, `yosys-portability`, `full-ci-gate`, `verilator-lint`, `yosys-elaboration` and `bdd-conformance`.
- Verilator shards 0-4 and Yosys shards 0-3 executed.
- A skipped context is not evidence. Hosted and act acceptance belong to the manager.

## Receipts

Every published file is listed in `MANIFEST.sha256`, with paths relative to the packet root.

- **`scripts/`:**
  - `leg.py`: build or run one leg from its recipe line;
  - `mk_ghost.py`, `ghost_matrix.sh`: the tuple matrix;
  - `mk_pend.py`: the pending-form mutants;
  - `mk_swap.py`, `swap_matrix.sh`, `analyze_swaps.py`: the binding exchanges;
  - `mk_hprobe.py`: the window and log-storage probe;
  - `mk_acopy.py`: the A-copy probe;
  - `summarize.py`;
  - `verify_clone.py`.
- **`receipts/baseline/`:** the five head runs and their build logs.
- **`receipts/ghost/`, `receipts/ghost-matrix-{nxn,nxn8}.md`, `receipts/ghost-mutant.diff`:** the tuple matrix and its notify controls.
- **`receipts/pf/`, `receipts/pf-*.diff`:** the pending-form mutants.
- **`receipts/swap/`, `receipts/swap-summary-{nxn,nxn8}.md`, `receipts/swap-*-console.txt`:** the binding exchanges, one diff each.
- **`receipts/hprobe/`, `receipts/hprobe.diff`, `receipts/probe/`, `receipts/acopy-probe.diff`:** the harness probes.
- **Other receipts:**
  - `receipts/port-contracts-{head,base}.txt` and `receipts/port-budget-base-regenerated.diff`;
  - `receipts/static-focused.txt` and `receipts/hosted-check-runs.tsv`;
  - `receipts/pr-534-body.txt` and `receipts/tool-identity.txt`;
  - `receipts/00-clone-state-before.txt` and `receipts/clone-state-final.txt`.
- **Path redaction.** The home-directory prefix in build logs is written as `$HOME`.

**Reproduce:**

1. Clone the exact head, with the three required submodules checked out at their gitlinks and registered, into a disposable tree.
2. In `tb/verilator/milan_dp`, run `make ltn_rom.hex ucode.hex gptp_ucode.hex` and `python3 gen_divergent_shape.py`.
3. Then:
   - `python3 scripts/leg.py <tree> <leg> both --jobs 8`;
   - for the matrices, `python3 scripts/mk_ghost.py <tree-copy>` followed by `sh scripts/ghost_matrix.sh <packet> <tree-copy> <leg> <N>`;
   - `sh scripts/swap_matrix.sh <packet> <leg> [portA:portB ...]`.

## Limits

- **Not run by this round:**
  - the full suite sweep;
  - the milan_dp legs that do not compile `sim_nxn.cpp` (obj_dir, nolpf, prune, ax1x1, aclk, gptp, gptplat) and the render mutants;
  - pp_shadow, milan_dp_render, crf_rx and behave;
  - `xvlog_gate`, `lint_rtl`, `check_sv_idiom`, `check_rtl_source_lists` and `gen_module_matrix`;
  - Yosys, the builder bank, synthesis and timing;
  - act;
  - hardware.

  `hdl/` is byte-identical to the previous round's head, and this delta changes only `sim_nxn.cpp`, docs and three config comments.
- **Binding exchanges.** All 45 were run on nxn. On nxn8 this round ran a 9-exchange cover of all ten ports, not all 45. nxndv and nxn4c were not mutated.
- **Pending-form mutants** ran on nxn, and `stuck` also on notify. They were not run on nxn8.
- **Synthesis.** The +1,134 generic-cell figure is the author's and was not reproduced. No physical timing exists for the added answer arm.
- **Manager banks.** The source static/builder and native banks for this head were still running when this round started. This report makes no claim about them and infers nothing from them.
- **Hardware.** Physical calibration NOT RUN, and field skips are not hardware proof. No silicon or Milan-controller verdict exists for this head. The issue's acceptance item "la_avdecc reports the entity Milan-compatible on silicon" is open by design.

## Pending manager duties

- Publish the source static/builder and native bank results for this head.
- Accept the hosted and act evidence.
- Build and gate the final current-dev candidate at the merge turn: source base `ede8d48e`, live dev `26d855a9`.
- Obtain the maintainer's explicit merge authorization and run post-merge containment.
- Re-flash the silicon and obtain the la_avdecc Milan-compatible verdict (#117). #529 closes only after that, per the PR's "Relates to".
- Optionally route S1 to the author.

## Clone restoration

No tracked file in the review clone was edited. Every build, mutant and probe ran in disposable clones under the packet's scratch directory, and those clones have been deleted. `scripts/verify_clone.py` (`receipts/clone-state-final.txt`) shows:

- HEAD `31e62ffe` and tree `4d32ede1` match;
- the index records equal the HEAD tree records, and the index sha256 equals the pre-review value;
- 864 tracked blobs, with 0 byte or mode mismatches;
- no untracked, ignored or modified residue;
- gptp-processor, protocol-processor and third_party/verilog-axis are gitlinks (mode 160000) at their pins, with clean worktrees;
- `external` is uninitialized, as at the start.

R268-3 FINISHED
