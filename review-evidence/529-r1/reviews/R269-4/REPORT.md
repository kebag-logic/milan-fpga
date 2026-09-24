[R269] POSITIVE - exact head 87abaf33a439c1cef05092aadd3377a36552a4be

Round R269-4: independent composition review of issue #529 / PR #534, in a cleared context.

- **Candidate:** `87abaf33a439c1cef05092aadd3377a36552a4be`, tree `bc40b183a9c999cbd3369c29ad7f7e3ff0dd64af`.
- **Parents:** live dev `26d855a9176d63625e6635a029a0c44e3d57ce9a` and the PR source head `31e62ffead16e43d648993278b0ab9190d99b672`.
- **Scope:** composition acceptance only. The source head has two POSITIVE source reviews: R268-3 (PR comment 5805443584) and R269-3 (PR comment 5805466331). Both cover all five lenses clean at `31e62ffe`.

## Summary

- **Verdict: POSITIVE.** The composed tree introduces no defect beyond the reviewed sources.
- No BLOCKER, MAJOR, MINOR or new SUGGESTION.
- All five lenses are covered clean at this exact head for the composed delta.
- **One file overlaps.** `docs/reference/REGISTER_MAP.md` is the only path changed on both sides. A raw three-way merge reproduces the candidate blob byte for byte, and the nearest hunks are 925 base lines apart.
- **One semantic interaction exists.** The two RTL modules dev changed (`KL_media_grid_align`, `KL_chan_map_capture`) are instantiated inside `milan_datapath.sv`, which this PR changes.
  - On the candidate, every milan_dp leg the PR's tests live in produces a run log byte-identical to the source head's. That includes every `got=` value.
  - The candidate model provably contains dev's RTL.
- **Fault probes still fail on the composed tree.** A permuted binding, a removed dirty source, and a CRF row that never leaves pending each turn their named checks red.
- **The prior findings stay resolved.** Every earlier MINOR and MAJOR on this PR remains resolved here. The open SUGGESTIONs are retained unchanged, since their files are blob-identical to the source head.
- My verdict and ledger were written before I read any prior review report. `receipts/50_interim_verdict_and_ledger_before_prior_findings.md` is a time-preserving copy, written 2026-09-24 03:31:40 +0200.

## Reconstruction

1. AGENTS.md and CONTRIBUTING.md, then docs/README.md.
2. Issue #529: the body, the manager's assignments (A10, 14:17, 19:25, 23:27), the author's TAKEN and three REVIEW READY comments, and the PR body.
3. The frozen acceptance: REGISTER_MAP "Closure criteria for the CRF Stream Input counter gap", criteria 1-4.
4. The history and diffs, read with raw `git`:
   - `26d855a9..87abaf33`;
   - the source side `ede8d48e..31e62ffe`;
   - the dev side `ede8d48e..26d855a9`.
5. Executable evidence regenerated on the candidate, then hosted evidence read-only.
6. Only then, the prior public reports: R269-1/-2/-3 and R268-1/-2/-3.

I read no private author material, lane scratchpad, or management directory.

## The composition set

`receipts/01_topology.txt`:

- **Merge base.** The source head's merge base with dev is `ede8d48ecd7c7f589a14b957951f040d92c99c70`, the only merge base.
- **Dev-side delta.** Live dev is three first-parent merges ahead of it. Their net change is the composition's dev side:
  - PR #526: isolate gPTP mutations and stop suite execution on cancellation;
  - PR #521: hosted firmware gates with a pinned RV32 compiler;
  - PR #528: junction counters and the raced media-grid lock.
- **Queued predecessors.** None: the candidate has exactly the two parents.
- **The candidate is the clean merge.** It is the clean `merge-tree` of dev and source, identical to the candidate tree.
  - The 16 source-side paths carry the source blobs, except REGISTER_MAP.md.
  - The 33 dev-side paths carry the dev blobs, except REGISTER_MAP.md.
- **Paths changed on both sides:** `docs/reference/REGISTER_MAP.md` only.
- **Submodule gitlinks:** unchanged on both sides. They are protocol-processor `424c688f`, gptp-processor `c1b61743`, verilog-axis `48ff7a7e` and external `efeb541a`.

## Where the two sides meet, and what was checked

| Interaction | Evidence | Result |
|---|---|---|
| **REGISTER_MAP.md** (both sides) | `receipts/13` (raw `git merge-file`), `receipts/16` | 0 conflicts, and the candidate blob is reproduced exactly. The source hunks sit at base lines 33-861 and the dev hunks (SLIP_TDM) at 1780-1829. Candidate lines 1-1837 equal the source's, so every source-side `REGISTER_MAP.md:N` citation still names the same text. The last 1362 lines equal dev's. |
| **Merged prose meaning** | REGISTER_MAP.md:31-35, :136-142, :182, :870-919 against the dev text at :1838 and :1871-1908 | No contradiction. The dev text (the grid clamp under a CRF selection, the junction-counter semantics) and the PR text (the CRF input bank served and pushed) describe disjoint mechanisms. |
| **Cross-citations** | `receipts/13` | Neither side adds a `path:line` citation into a file the other side changed. The one cross-mention is the audit doc's link `REGISTER_MAP.md#closure-criteria-for-the-crf-stream-input-counter-gap`, whose heading exists at candidate line 870. |
| **RTL hierarchy.** `milan_datapath.sv` (source) instantiates `KL_media_grid_align` and `KL_chan_map_capture` (dev) | `receipts/14` | Both instance blocks are byte-identical between dev and the candidate. The PR's `milan_datapath.sv` hunks do not touch them. The PR only connects previously open `KL_crf_rx` outputs and widens the Table 5.22 STREAM_INPUT pending vector. `locked_o`, `crf_clk_selected_r`, `aafcap_*` and `media_tick_p` are unchanged. |
| **The composed model contains both sides** | `receipts/11` | The obj_nxn generated code differs from the source head's only in logic naming `chan_map_capture` and `media_grid_align`, plus scheduling reorderings. So dev's RTL is really elaborated in the candidate runs. |
| **Behaviour of the PR's checks in the composed RTL** | `receipts/legs_*`, `receipts/10`, `receipts/12` | See the next section. |
| **Dev's rewritten gates reading the PR's files.** `measure_test_evidence.py`, `check_baremetal_only.py`, `ci_events.py` and `run_all_suites.sh` changed on dev | `receipts/gates/` | All pass on the candidate. `run_all_suites.sh` changed cancellation only, and the milan_dp deadline stays 2700 s. |
| **Dev's `test_builder.py` against the PR's configs and datapath** | `receipts/13` and a read of the dev diff | Dev's added builder lines name no PR-changed file. The PR's three config edits are YAML comments. `test_builder.py` itself was not run (builder bank). |
| **The behave suite reads the merged REGISTER_MAP.md, `KL_crf_rx.sv`, `milan_datapath.sv` and dev's `KL_chan_map_capture.sv`** | `receipts/23` | 14 features, 316 scenarios and 1515 steps pass on the candidate. |

## Executable evidence on the candidate

Pinned simulator 5.050 (wrapper sha256 `905795b9...`, `receipts/02`). Every leg was built from the suite's own `make -n run` recipe line, in a disposable clone of the exact head whose three required submodules were checked out at their gitlinks. At most 8 parallel jobs.

**milan_dp**, all 12 legs of the `run` recipe (`receipts/legs_cand/LEGS.txt`):

| Leg | Candidate | Source head | Dev tip | Candidate vs source log |
|---|---|---|---|---|
| obj_nxn | 1708/0 (75 `[CTRS-CRF]`) | 1708/0 | 1633/0 | identical |
| obj_nxndv | 1710/0 | 1710/0 | 1635/0 | identical |
| obj_nxn8 | 3136/0 | 3136/0 | 3061/0 | identical |
| obj_nxn4c | 1708/0 | 1708/0 | 1633/0 | identical |
| obj_notify | 146/0 (11 `[NOTIFY-CRF]`) | 146/0 | 135/0 | identical |
| obj_dir | 230/0, 1 guarded | same | same | identical |
| obj_nolpf | 230/0, 1 guarded | same | same | identical |
| obj_prune | 33/0 | same | same | identical |
| obj_ax1x1 | 227/0, 5 guarded | same | same | identical |
| obj_gptp | 181/0 | same | same | identical |
| obj_gptplat | 181/0 | same | same | identical |
| obj_aclk | 139/0 | not rerun | not rerun | - |

How to read the table:

- **Candidate against source** (`receipts/10`): all 11 compared run logs are byte-identical, including every `got=` value.
- **Dev against candidate** (`receipts/12`): the differences are only:
  - the PR's `[CTRS-CRF]` lines (75 per broad leg) and `[NOTIFY-CRF]` lines (11 on notify);
  - the tally lines;
  - two informational `[i]` timing lines, which move because the PR's arms consume simulated time. These lines are identical between source and candidate.

**The other suites that elaborate the composed datapath:**

| Suite | Candidate | Source head |
|---|---|---|
| pp_shadow (`receipts/20`, `receipts/21`) | 371/0 | 371/0, run output identical |
| milan_dp_render (`receipts/22`) | tdm8render 150/0, tdm8render-multi 59/0 | - |
| behave (`receipts/23`) | 316 scenarios pass | - |

**Composition fault probes on the candidate** (`receipts/probes/`, each a one-line diff of the candidate's `milan_datapath.sv`, built through `DP_SRC`):

| Probe | Leg | Result | Red checks | Prior finding it exercises |
|---|---|---|---|---|
| P1: the MEDIA_RESET and TIMESTAMP_UNCERTAIN tally bindings exchanged at `KL_crf_rx` | nxn | 1708/2 | `[CTRS-CRF] events, all ten: @16 MEDIA_RESET got=0x6 exp=0x5` and `@20 TIMESTAMP_UNCERTAIN got=0x5 exp=0x6` | R269-1 F1 = R268-1 F1 |
| P2: `dirty_p_o` left open | nxn | 1708/1 | "the bind edge reached the arbiter as STREAM_INPUT N only" | R269-2 F1 = R268-2 F1 (criterion 3) |
| P2: `dirty_p_o` left open | notify | 146/11 | all 11 `[NOTIFY-CRF]`, A's copy included | - |
| P3: the STREAM_INPUT pending-clear loop stops below the CRF row | notify | 146/2 | "...no further push to B in the next two seconds" and "...nor to A" (4 against 2) | R268-1 F2 |
| P3 | nxn | 1708/0 | none, by design: multiplicity is not claimed there | - |

**Gates on the candidate:** 50 commands, all exit 0 (`receipts/gates/SUMMARY.txt`, one log each). They include:

- `docs_check.py`;
- `check_em_dash.py --base 26d855a9...` (the first parent, which is the push judgement after the merge): 0 findings over 164 added lines in 9 pages;
- `check_em_dash.py --base ede8d48e...` (the merge base): 0 findings over 515 lines in 18 pages;
- `check_em_dash.py --selftest`;
- `gen_toc.py --selftest`, `--verify-anchors` (148 cross-page links) and `--check` (106 pages);
- `check_feature_status.py` and `--self-test`;
- `gen_module_matrix.py --check` (69 modules, up to date);
- `check_port_contracts.py` (hdl 217 <= 217 against the PR-regenerated `port_docs.budget`) and `--selftest`;
- `lint_rtl.py --check` (90 <= 90);
- `xvlog_gate.py --check`, which ran against a local vendor front-end: `hdl/` 0 findings, and 4 pinned-processor findings equal to the ratchet;
- `check_rtl_source_lists.py`, `pp_srcs.py --check` and `check_soc_sources.py`;
- `ci_events.py --check` and `--selftest`, and `ci_scope.py --selftest`;
- `measure_test_evidence.py --check` and `--selftest`, and `check_baremetal_only.py --check` and `--selftest`;
- the sv, cpp, py and sh idiom gates, `check_hygiene`, `measure_naming`, `measure_fail_fast` and `check_todo_ownership`;
- `check_doc_style`, `check_gptp_docs` (also `--with-submodule`), the DOC_MAP, timesync and submodule diagram `--check` gates, `check_solution_docs`, `check_submodule_docs`, `check_diagram_pngs`, `check_doc_paths` and `check_archive`;
- `gen_aem_store --self-test`;
- the sweep, deploy, entity and wire-accountability shape gates;
- `check_nvm_record_space`.

**Hosted evidence, read only** (`receipts/15`):

- GitHub's pull-request test merge `6d22951890a2b8b906fefe0e80c6a047df9313fa` has parents dev `26d855a9` and `31e62ffe`, and its tree is `bc40b183`, the candidate's tree.
- The PR head's jobs checked out `6d22951`. In those jobs:
  - Verilator shards 0-4 executed with every suite PASS, including milan_dp, pp_shadow, milan_dp_render, crf_rx, media_grid_align and chmap_capture;
  - docs-check, elaborate, yosys-elaboration, the Yosys shards, verilator-suites, yosys-portability and bdd-conformance concluded success;
  - "Physical gPTP (nightly and manual)" was SKIPPED, which is not evidence.
- This is observed only. Hosted and `act` acceptance belong to the manager.

## Findings

None. No BLOCKER, MAJOR, MINOR or SUGGESTION is raised by this round.

## Prior public findings, at this head

The source-side files are blob-identical to `31e62ffe` in the candidate (`receipts/01`), except REGISTER_MAP.md, whose source-side lines are unchanged in position and text (`receipts/16`).

| Prior item | State at 87abaf33 | Evidence this round |
|---|---|---|
| R269-1 F1 MAJOR = R268-1 F1 MINOR (Conformance, Tests, Docs): a permuted `KL_crf_rx` binding goes undetected | RESOLVED | P1 is red on both exchanged quadlets. The event arm runs green at 75 `[CTRS-CRF]` on all four broad legs. |
| R268-1 F2 MINOR (Tests, Docs): `[NOTIFY-CRF]` cannot fail for a row that keeps pushing | RESOLVED | P3 is red on notify, 4 pushes against 2, to B and to A. |
| R268-1 F3 MINOR (Docs): the REGISTER_MAP opening status lists the CRF bank as a gap | RESOLVED | REGISTER_MAP.md:31-35 and :136-142 in the candidate are unchanged from the source. |
| R269-2 F1 = R268-2 F1 MINOR (Tests, Docs): the "and as nothing else" and "each copy" claims | RESOLVED | The check is present, and the candidate log is identical to the source's. P2 reddens the bind-edge check and all 11 `[NOTIFY-CRF]`, A's copy included. REGISTER_MAP.md:897-919 is unchanged. |
| R269-3 S1 = R268-3 S1 (SUGGESTION; Tests, Robustness): `n1` points into `uns_log` across an appending exchange (sim_nxn.cpp:1322,1330-1332) | RETAINED | sim_nxn.cpp blob-identical |
| R269-3 S2 (SUGGESTION; Tests, Docs): the delivery records see only `step()`-driven cycles | RETAINED | same |
| R269-3 S3 = R268-3 S5 (SUGGESTION; Robustness, Tests): no `crf_sink: false` leg | RETAINED | no leg added on either side |
| R269-3 S4 (SUGGESTION; Docs): `port_docs.budget` regeneration folded in unrelated tightening | RETAINED | At the candidate, `check_port_contracts` is exact at 217 <= 217, so dev's RTL moved no count. |
| R269-3 S5 (SUGGESTION; Tests): the 990 ms release floor | RETAINED | sim_nxn.cpp:1354 unchanged |
| R269-3 S6 = R268-3 S4 (SUGGESTION; Tests): round-robin no-starvation ungraded | RETAINED | arbiter RTL blob-identical to the source |
| R269-3 S7 = R268-3 S2 (SUGGESTION; Tests, Docs): silence constants are literals | RETAINED | sim_nxn.cpp:3629-3630 unchanged |
| R269-3 S8 = R268-3 S3 (SUGGESTION; Tests): non-public tally wires | RETAINED | unchanged |
| Earlier suggestions the source rounds recorded as resolved: frozen criteria quoted, B4 config comments, the `Closes #529` wording, the timed-leg header | still RESOLVED | The files are blob-identical. The PR body says "Relates to #529". |

Pre-existing and out of scope, as the source rounds recorded:

- REGISTER_MAP.md:828-829 "ACMP listener sink 1" (same text at the candidate);
- the `KL_crf_rx` unlock wording, tracked by #541.

## Reviewer-owned ledger

Each lens is judged per lens, and each touches the composition's scope as described.

- **Coverage of the source content** is R268-3 and R269-3 at `31e62ffead16e43d648993278b0ab9190d99b672`, an ancestor of the candidate.
- **Dev's own content** was reviewed in PRs #526, #521 and #528.
- **This round** covers the composed delta at the candidate.

| Lens | CLEAN/UNCLEAN | Composition touches scope? | Examined artifacts (at 87abaf33) | Covering round | Exact head |
|---|---|---|---|---|---|
| Conformance | CLEAN | Yes: the acceptance document is the both-sides file, and the served GET_COUNTERS and Table 5.22 behaviour now runs beside dev's RTL | REGISTER_MAP.md three-way merge and :870-919 criteria 1-4 text; `[CTRS-CRF]` 75 and `[NOTIFY-CRF]` 11 on the candidate, with logs identical to the source (0xF3F mask, 32-bit words, era wipe, N+1 refusal, {STREAM_INPUT, N}-only push, one per second then quiet); gptp and gptplat identical | R269-4 (source content: R268-3, R269-3) | 87abaf33a439c1cef05092aadd3377a36552a4be |
| RTL | CLEAN | Yes: dev's `KL_media_grid_align` and `KL_chan_map_capture` elaborate inside the PR's `milan_datapath.sv` | `milan_datapath.sv` instance blocks, identical dev vs candidate (`receipts/14`); the generated model contains both sides (`receipts/11`); lint 90 <= 90; `xvlog_gate` hdl 0; port contracts; `check_rtl_source_lists`; `check_sv_idiom`; 12 legs build clean | R269-4 (source content: R268-3, R269-3) | 87abaf33a439c1cef05092aadd3377a36552a4be |
| Robustness | CLEAN | Yes, through the shared hierarchy only: no signal is shared between the two changes | the reset, era-wipe, 100 ms silence-unlock, wrap and wrong-row arms rerun identically on the candidate (`receipts/10`); P3 (a stuck pending row) caught; no collateral change in the 1708, 3136, 146, 230, 227, 181 or 371-check legs | R269-4 (source content: R268-3, R269-3) | 87abaf33a439c1cef05092aadd3377a36552a4be |
| Tests | CLEAN | Yes: dev changed the test-evidence ratchet and the suite runner, and the PR's tests now run on composed RTL | 12 milan_dp legs, pp_shadow, the two milan_dp_render legs and behave on the candidate; P1, P2 and P3 red for their defects; `measure_test_evidence --check/--selftest`; `check_cpp_idiom`; suite deadlines unchanged | R269-4 (source content: R268-3, R269-3) | 87abaf33a439c1cef05092aadd3377a36552a4be |
| Docs | CLEAN | Yes: REGISTER_MAP.md changed on both sides | the merge-file reproduction and hunk distance; merged prose read at :31-35, :136-142, :182, :870-919, :1838 and :1871-1908; line stability (`receipts/16`); `docs_check`; `check_em_dash` against both the first parent and the merge base; `gen_toc` `--check` and `--verify-anchors`; `check_feature_status`; `gen_module_matrix --check`; `check_doc_style`; `check_doc_paths` | R269-4 (source content: R268-3, R269-3) | 87abaf33a439c1cef05092aadd3377a36552a4be |

## Real limits

- **Not run by this round:**
  - the full parent, processor, gPTP, Yosys and builder banks (`run_all_suites.sh`, `syn/yosys/run.sh`, `test_builder.py`, the RV32 SDK and firmware gates);
  - `act` and the host `act_ci` self-test;
  - `gen_hdl_reference` and `gen_wavedrom` (a missing module);
  - milan_dp_gptp (5400 s budget);
  - the milan_dp render mutation campaign and milan_dp_render `--leg-defects`;
  - timing and area.
- **Suites whose inputs are one-sided in the candidate were not rerun locally.** They are crf_rx (source only), and media_grid_align and chmap_capture (dev only). Their inputs are blob-identical to the parent that owns them. The hosted shards ran them on the identical tree, as observed only.
- **Source-head comparison runs** cover 11 of the 12 milan_dp legs. `obj_aclk` ran on the candidate only.
- **The probes are three focused composition probes,** not a repeat of the source rounds' mutation matrices. Those ran at `31e62ffe` on blob-identical RTL and harness.
- **The manager's banks.** The manager's source static, builder and native banks for this head are still running. This report neither claims nor infers them.
- **No hardware.** Physical calibration NOT RUN. Skipped field and physical contexts are not hardware proof. No silicon or Milan-controller verdict exists for this head, and #529's silicon acceptance item is open by design.

## Pending manager duties

- Publish this report. Publish the source static, builder and native bank results for this head.
- Accept the hosted and `act` evidence. The observed PR test merge `6d229518` has this candidate's tree.
- At the merge turn, build and gate the final current-dev candidate: source base `ede8d48e`, live dev `26d855a9` at this review, with the full local bar. If dev moves, this composition review no longer covers the new tree.
- Accept the completion ledger, obtain the maintainer's explicit merge authorization, and run post-merge containment.
- Re-flash the silicon and obtain the Milan-controller confirmation (#117) before #529 closes.
- Optionally route the retained suggestion S1 to its own Issue, as the author proposed.

## Clone restoration

- **No probe edited the review clone.** Builds, probes and comparison trees ran in disposable clones under the packet's `scratch/`, which is not published.
- **Gate residue.** The gates run in the review clone created ignored `__pycache__/` directories (four in the superproject and one in `protocol-processor/`) and `sw/builder/out/`. All were born after the clone and during the gate run, and were removed.
- **At the end** (`receipts/04_integrity_after.txt` against `receipts/03_integrity_before.txt`):
  - HEAD `87abaf33` and tree `bc40b183` match;
  - the index entries equal the HEAD tree entries (sha256 `d2ba0127...` for both). The raw index file hash moved only by the stat-cache refresh;
  - 872 tracked blobs, with 0 byte or mode differences;
  - no untracked, ignored, assume-unchanged or skip-worktree entries;
  - gitlinks at their pins: gptp-processor `c1b61743`, protocol-processor `424c688f` and third_party/verilog-axis `48ff7a7e`, each with 0 status lines. `external` is uninitialised, as at the start.

## Reproduce

Scripts are in `scripts/`. Paths in receipts are redacted to `<packet>`, `<review-clone>`, `<pinned-bin>`, `<data-root>` and `$HOME`.

```sh
bash scripts/topology.sh <clone> 87abaf33a439c1cef05092aadd3377a36552a4be 26d855a9176d63625e6635a029a0c44e3d57ce9a 31e62ffead16e43d648993278b0ab9190d99b672
python3 scripts/composition_checks.py <clone> 87abaf33... 26d855a9... 31e62ffe...
bash scripts/run_gates.sh <clone> <out> <pinned-bin> 26d855a9... ede8d48e...
# disposable clone per tree, the three submodules initialised at their gitlinks
PATH=<pinned-bin>:$PATH python3 scripts/run_milan_dp_legs.py --suite <tree>/tb/verilator/milan_dp --out <dir> --par 4 --vjobs 2
python3 scripts/compare_legs.py <dir-src> <dir-cand>
python3 scripts/make_probes.py <tree>/hdl/milan/milan_datapath.sv <probe-dir>
PATH=<pinned-bin>:$PATH python3 scripts/run_milan_dp_legs.py --suite <tree>/tb/verilator/milan_dp --out <dir> --legs obj_nxn,obj_notify --dp-src <probe-dir>/P2-dirty-open.sv
bash scripts/run_recipe.sh <tree>/tb/verilator/pp_shadow run 8 <pinned-bin> <log> "DP_SRCS=$(make -s -C <tree>/tb/verilator/milan_dp print-srcs)"
bash scripts/hosted_evidence.sh kebag-logic/milan-fpga 31e62ffe... 6d229518... <job-ids>
bash scripts/integrity.sh <clone> 87abaf33a439c1cef05092aadd3377a36552a4be
```

R269-4 FINISHED
