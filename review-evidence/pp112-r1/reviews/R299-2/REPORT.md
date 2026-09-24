[R299] POSITIVE - exact head f222f6b96328c8eb0f4d2c5c3470ebd365e51fdc

# R299-2 external independent review: processor issue #112 / PR #114, round 2

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head `f222f6b96328c8eb0f4d2c5c3470ebd365e51fdc`, tree `60b6e1b11dfa57558a2d839a36d8a6769c0a4e72`.
- The head is a merge commit. Its parents are `ae7f531` (PR branch: `73a5478`, `90e1ce1` [A266], `fbabb94` and `ae7f531` [A267]) and `7a47f578` (main after PR #111).
- Source base `939c143333d11e2378a514f1c7b6abd4c3259bfd`. The live parent dev `573f0052a0e4412e81f0845438fcec2086ce5d55` and the merge-turn current-dev candidate belong to the manager and were not exercised here.
- Reviewer role: external independent reviewer, working in a cleared context in its own detached clone. It made no GitHub writes, no source edits, no commits, and had no author contact.
- Simulator: pinned Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`, wrapper sha256 `905795b9…e92f`), identity checked before use.

## Verdict

**POSITIVE.** The round-2 design (manager decision, issue #112 comment 5816928229) is implemented as specified:
- A pending source's own grant stays low.
- Any admission round that visits a requesting source without a valid current-declaration slope is discarded. Every other published grant, every granted slope, `sum_slope` and `over_limit` therefore hold their last published values (`hdl/srp/KL_srp_admission.sv:185-193,230-246`).
- Capacity is released only by a withdrawal (the live AND with `req_i`) or by an evaluated shrink.
- The optimistic window ages only on published rounds (`hdl/srp/KL_srp_top.sv:785-796`).

Evidence at the exact head:
- My round-1 probes, re-run unchanged, all give 0 FAIL: unit N=2 28/28 and N=8 112/112; `srp_top` 80/80; wire 0 of 40. P1 stays at 0/4 and 0/16 pulses, while the base still pulses 4/4 and 16/16.
- New round-2 probes are all clean:
  - an independent randomized Σ-context oracle, about 146 M per-clock checks over N = 1/2/3/5/8, 0 FAIL, with the worst latency exactly at the documented bound;
  - a processor-top cross-source probe through the real `svc_*` face, 144/144;
  - the #111 GET_STREAM_INFO phase under a sustained admission-hold storm, 488/488, the same as without the storm.
- Every non-equivalent mutant is killed. That includes three new discard-logic mutants, all killed by the author's own suites.

Both round-1 findings, R299-1 F1 (MAJOR) and F2 (MINOR), are resolved, as are the matching R298-1 findings. No finding at MINOR or above is open. There are three SUGGESTIONs, which do not affect the verdict.

## Reconstruction (order followed)

1. **Conventions.** The repository has no `AGENTS.md` and no `CONTRIBUTING.md`; its conventions come from `README.md` (build/check commands, submodule pin contract) and `docs/README.md` (single-source rules, F02.10 as the home of status names).
2. **Scope.** Issue #112: body with frozen acceptance 1–5, and all 8 comments:
   - the A259 assignment;
   - A266, the round-1b test-idiom fix;
   - **5816928229**, the manager DECISION for round 2 (design plus required items 1–7);
   - the A266, A267 and A273 REVIEW READY comments;
   - the A273 merge assignment.
   On PR #114: the review-start comment 5818807789 and the manager validation 5818943152 (donor bank 9/9; parent consumer gates 7/7 at parent dev `573f0052` with this head staged).
3. **Authorities:**
   - `docs/architecture/10_srp_engine.md` §6.3, including the new anchors `sec-10-admission-freshness` (:276) and `sec-10-admission-cross-source` (:292) and the optimistic-window paragraph (:334);
   - `02_interfaces.md` F02.10 rows `granted_slope_bps` / `sr_admitted` (:430-431);
   - the `docs/guides/integrator.md` svc row (:254) and port rows (:284-287);
   - the port comments in `hdl/top/protocol_processor_top.sv:516-532` and `hdl/srp/KL_srp_top.sv:213-218`.
4. **Diff and history.** `git diff 939c1433..f222f6b9`: 34 files, of which 16 are this PR and 18 come from main (#111).
   - `git diff 939c143 ae7f531` and `git diff 7a47f57 f222f6b` are line-identical apart from hunk offsets.
   - The only content differences are the two conflict resolutions (`syn/ooc/README.md` keeps both sections; `tb/srp_top/README.md` gives 1531 checks) and the adjacent `KL_srp_top` port-comment lines, where both sides are kept. The merge adds or loses nothing else.
5. **Public evidence.** kebag-logic/milan-fpga@da848abf `review-evidence/pp112-r1` (529 manifest entries):
   - I read the `author-merge` summaries for the exact head (`final-summary.json`, `merge-metadata.json`, admission/GSI/parent result JSON); see `receipts/evidence-check.txt`.
   - I did not open the `reviews/` subtree until my verdict and ledger were written.
   - Hosted checks at the exact head are listed under Tests below.

## Probes and runs (all in the foreground, at most 8 parallel jobs, on `git archive` exports of the exact head under the scratch area)

| Item | Result | Receipt |
|---|---|---|
| Round-1 unit probe, unchanged (byte-identical to the R299-1 manifest, 7/7 files) | head N=2 28/28, P1 0/4, P2 0/2+0/2; N=8 112/112, P1 0/16, P2 0/8+0/8, longest refused-source grant 0 clocks. Base: P1 4/4 and 16/16 (the original defect) | `unit-probe-{head,base}-N{2,8}.log`, `r1-probes-unchanged.txt` |
| Round-1 `srp_top` cross-source probe (identical and shrink, 8 phases, real service port and Listener Ready) | 80/80, 16 runs: 0 grant, 0 ACTIVE∧grant, 0 declared Advertise, 0 wire Advertise | `top-probe-head.log` |
| Round-1 wire probe (identical re-declaration k = 1..40 clocks before T-MRP-JOIN) | 80/80; 0 of 40 placements put a Talker Advertise for the refused stream on the wire | `top-wire-probe-head.log` |
| **New:** randomized Σ-context oracle (`probes/r2/sigma_random_probe.cpp`), 200 seeds × 400 random events per configuration. Events are declares, identical re-declares, shrinks, grows, saturation, withdrawals, bursts shorter than a round and quiet gaps; MULTI mode also changes several sources on one edge. Rules R1–R7 are checked on every clock | N=1/2/3/5/8 × single/multi: 0 FAIL in all 10 (2.59 M to 37.99 M checks each). Measured worst latency after the last change is 4/6/9/15/24, exactly the documented bound. R7 exercised 746 k–760 k refused-source hold clocks at N=8 | `sigma-head-N*-{single,multi}.log` |
| **New:** processor-top cross-source probe (`probes/r2/pp_top_cross_probe.inc`). It adds observe-only wrapper taps on `srp_sr_admitted_w`, `srp_active_w`, `srp_tk_decl_state_w`, `srp_sum_slope_w` and `srp_over_limit_w`. Source 0 ≈ 69.95 Mb/s is admitted and source 7 ≈ 15.49 Mb/s is refused, with real MSRP Listener Ready for both. Source 0 then re-declares identically, shrinks but still refuses 7, or shrinks and frees 7, at 8 phases, through `svc_*` | 144/144. Refused runs: 0 grant, 0 ACTIVE∧grant, 0 declared Advertise, 0 wire Advertise. The aggregate never moved during a hold (0/24). Source 0's hold is 16 or 24 clocks. The freed source 7 grants on the same clock as source 0's re-grant (8/8), then declares Advertise | `pp-top-cross-probe-head.log` |
| Same probe, pending-absent mutant | 48 FAIL: 16/16 refused runs licensed (grant, ACTIVE∧grant and Advertise), 24/24 with aggregate movement. The probe is sensitive | `pp-top-cross-probe-mutant-pending-absent.log` |
| **New:** #111 GET_STREAM_INFO under an admission hold (`run_pp_top_probe.sh … gsi-storm`). The unchanged `InternalStreamInfoPhase` runs while the harness re-declares SRP source 6 through `svc_*` every ~60 clocks, alternating an admitted and a refused TSpec | 488/488, 0 failures, the same as the storm-free control (488/488). 25,498 re-declarations were issued and answered; source 6 was not admitted for 1.50 M clocks | `pp-top-gsi-head.log`, `pp-top-gsi-storm-head.log` |
| Author suites at head | `srp_admission` shapes: 1138 / 12615 / 41012 / 201073 / 991231 checks at N = 1/2/3/5/8, 0 FAIL. `srp_top`: 1531 / 0 FAIL. `pp_top`: 1948 / 0 FAIL (both builds). `gsi_mutants.py`: 13/13 detected by named checks; golden and restored pass | `head-srp_admission-shapes.log`, `mutants-author/control-srp-top.log`, `head-pp_top.log`, `gsi-mutants-summary.txt` |
| Author admission mutant campaign (`tb/srp_admission/mutants.py`) | 12/12 verdicts. Failing-check counts match `tb/srp_admission/README.md` exactly: stale-evaluation 402/5473/105; pending-absent 175/1067/205, of which the named cross-source check fails 44 at N=2 and 368 at N=8, and srp_top's I check fails in 72 of 72 runs; discarded-round-strobes 146/695/90 | `mutants-author-summary.txt`, `mutants-author/` |
| Round-1 reviewer mutant campaign, re-run unchanged (`mutants_r299.py`) | M2–M6 are KILLED by all three benches. M7 (top strobe removed) is KILLED by srp_top, as expected: the unit bench has no top. **M1 (validity terms only) survives all benches: an equivalent mutant**, see below | `mutants-r1-summary.txt`, `mutants-r1/` |
| **New** mutants against my Σ probe (`mutants_r2.py`, N=3 multi and N=8 single, 50 seeds) | Nine mutants: A pending-absent, B stale-both, C discard-strobes, D last-visit-ignored, E pend-not-accumulated, F validity-terms-only, G no-retire, H no-restart, I aggregate-not-frozen. All except F are KILLED, by the named rules R1/R3/R4/R5. F survives with the same check count as the control | `mutants-r2-summary.txt`, `mutants-r2/` |
| **New** mutants D, E and I against the author's suites (`mutants_r2_suites.py`) | Each is killed by at least one author suite. D is killed by N=2 and N=8 (`round publishes the greedy walk …`). E is killed by N=8 and srp_top (the named cross-source and I checks). I is killed by N=2 and N=8 (`aggregate holds between publications`). The author bank as a whole kills all three | `mutants-r2-suites-summary.txt`, `mutants-r2-suites/` |
| [A266] "no behaviour change" (`73a5478` vs `90e1ce1`) | Filtered stdout is byte-identical for `srp_top` (735 checks) and all five `srp_admission` shapes | `a266-equivalence.txt` |
| Scoped lint (the flags of `scripts/lint_hdl.sh`, whole tree visible) | `KL_srp_admission`, `KL_srp_top`, `protocol_processor_top`, and `KL_srp_admission` at N_SOURCES_P = 1/2/3/5/8: rc 0, 0 warnings | `lint-scoped.log` |
| Port surface | `protocol_processor_top` port declarations (comments stripped) are identical at base 939c143, main 7a47f57 and head. `KL_srp_top` is identical from main to head; its one port delta against base (`evt_tk_fail_chg_o`) is #111's. `KL_srp_admission` gains the internal `invalidate_i` | `port-compare.txt` |
| Docs gates (`make links matrix modmatrix` on the head export) | 855 links OK; 115 REQ rows and 17 GAP findings OK; 92 module rows, 0 untested. The PR diff touches no mermaid or wavedrom block | `docs-gates-scoped.log` |

### M1 equivalence (the author's claim, verified)

In round 1, removing ` && slope_valid_r[aidx_r]` from `fit_w`/`refuse_w` was a killable mutant. At this head it is equivalent. Here is why:
- Every register that feeds a publication (`acc_r`, `over_acc_r`, `pend_acc_r`, `wgrant_r`, `wgslope_r`) is cleared at every round end and at every invalidation (`:224-229,241-246`), so a published verdict depends only on the visits of that round.
- A round publishes only if every visit had `pend_w = 0`, that is `invalid_w || slope_valid_r`.
- On such a visit, `!invalid_w && slope_valid_r` equals `!invalid_w`. So `fit_w` and `refuse_w` are identical with or without the term, on every visit of every published round.
- Nothing else reads `slope_valid_r`.

The empirical result agrees: F/M1 survives every bench, and its check counts are identical to the control's (9,544,389 at N=8 single; 991,231 in the author N=8 suite). The RTL comment at `:185-186` and `tb/srp_admission/README.md` both state this. The campaign replaced it with a both-protections mutant, which is killed.

## Lens assessments

- **Conformance, CLEAN.**
  - Issue #112 acceptance 1–4 are met:
    - no grant on a slope other than the current declaration's (R1, P1);
    - both directions tested at several sources, with latency measured and stated (8/16/24 at M=8; 4, 4/6, 6/9, 5/10/15 at M = 1/2/3/5, matching the 10 §6.3 table);
    - the stale-evaluation mutant fails;
    - no top-level port change, with ACTIVE, the window and the aggregates documented.
  - Acceptance 5, green suites and parent consumer gates: the processor side is re-run here, and the parent side is the manager's 7/7 receipt (5818943152).
  - Manager round-2 items 1–7:
    - (1) the design is implemented;
    - (2) the cross-source test runs at unit level (every phase, N ≥ 2: identical, shrink, grow, double and middle) and through `tb/srp_top` (sources 1 and 7, 8 phases, 40 join placements), checked every clock for no grant, no ACTIVE and no declared Advertise, plus the wire;
    - (3) all my probes give 0 FAIL, P1 0;
    - (4) the pending-absent mutant fails the new tests;
    - (5) the Σ-context oracle is present;
    - (6) 10 §6.3, the integrator row and the admission banner state the rule;
    - (7) the parent idiom gates are covered by the manager receipt.
  - The greedy index-order / 75 % ceiling rule is unchanged at every publication (R3 over ~1.27 M random publications).
- **RTL, CLEAN.**
  - `KL_srp_admission` was read in full. The slope pipeline invalidates at all three stages, with a same-edge override.
  - Pending is `!invalid && !slope_valid`, accumulated across the round, with the last visit included in the publish decision.
  - Invalidation retires only the changed sources and restarts the round.
  - A discarded round does not strobe `round_done_o`.
  - `KL_srp_top`: the invalidation strobe comes only from `gate_acc_w`, which only the talker DECLARE/WITHDRAW ops reach (`:811,820`); Listener ops go to `S_CTL`. The window counter ages on `adm_round_w` (published rounds only), and the talker FSM sees `opt_r | adm_admitted_w` (`:450`).
  - Non-power-of-two shapes and N = 1/2 aliasing are covered by the shapes, the random probe and lint.
  - Area (`syn/ooc/README.md`, not re-synthesized here) is internally consistent: +17 FF = 10 validity + 1 `pend_acc_r` + 5 `aidx_r` replicas + 1 `wgrant_r[7]`, which matches `u_admission` 862 → 879; +37 LUT on 7566. RAM and DSP are unchanged.
- **Robustness, CLEAN.**
  - All sampling phases were covered, including multi-source same-edge changes, concurrent pendings, withdrawal during a hold, bursts shorter than a round, saturating TSpecs and join-tick straddling.
  - Liveness: publication follows within 3N clocks (4 at N=1) of the last change in every random run.
  - The live Σ never exceeds the published Σ or the ceiling.
  - A starvation storm (changes less than a round apart) holds verdicts indefinitely, in the safe direction (no grant rises; a retired slope stays in Σ). This is documented at 10 §6.3 and in the integrator svc row. Base had the equivalent restart behaviour.
  - The window growth from 25 to up to 41 clocks is bounded and documented. It only extends an already-documented optimistic ACTIVE (parent #551 prescribes ACTIVE AND real grant).
  - #111 GSI is structurally disjoint: it reads only sink-side `tk_reg_state`, `snk_fail_*` and `evt_tk_*` from `u_listener`, never the admission nets. It is behaviourally unaffected under a hold storm.
- **Tests, CLEAN.**
  - The unit Σ-context oracle (`tb/srp_admission/sim_main.cpp:87-115`) checks, on every clock:
    - every publication equals the greedy walk over all current declarations;
    - between publications, grants only retire with their own change;
    - the aggregate holds.
  - It is independent of the DUT's pipeline, and my randomized oracle agrees.
  - The srp_top I and J sections judge every clock at all phases.
  - Coverage of the discard logic is strong: the author's campaign kills 3/3, and D/E/I are all killed by the author's suites.
  - `make` in `tb/srp_admission` now runs all shapes, so the bank covers N = 1/2/3/5/8.
  - Hosted checks at the exact head (`hosted-check-runs.txt`): six executed check runs, `suites`, `docs-gates` and `portability` in both the push and pull_request workflows, all `completed/success`, none skipped. The legacy combined-status API has 0 statuses. The manager owns hosted and act acceptance.
- **Docs, CLEAN, with three non-blocking suggestions.**
  - 10 §6.3's freshness, cross-source, latency, window and accounting text matches the measured behaviour:
    - latency sets and bound;
    - window 25/33/41 = verdict + 17 clocks;
    - the freed source grants on the same clock;
    - Σ ≥ live Σ;
    - the storm clause.
  - The integrator rows, top and `KL_srp_top` port comments, admission banner, srp_top banner, suite READMEs (1531 and 12615/991231 checks), MODULE_MATRIX and `syn/ooc` notes are accurate, apart from S1–S3.

## Findings

No finding at MINOR, MAJOR or BLOCKER is open.

### S1: a dated check count in the mutant section predates the merge (SUGGESTION)
- **Lenses:** Docs
- **Location:** `tb/srp_admission/README.md:91-92`, "the controls pass (12615 checks at two sources, 991231 at eight, 1527 in srp_top)".
- **Authority/evidence:** `tb/srp_top/README.md:14` states 1531, and the merged head measures 1531 (`mutants-author/control-srp-top.log`). The 1527 was measured at `ae7f531`, before #111 added four srp_top checks.
- **Impact:** reader confusion only. The failing-check counts per mutant are still exact.
- **Required outcome:** update to 1531, or name the head the figure was measured at.
- **Verification:** the README figure equals the control tally.

### S2: the integrator svc row omits the one-source exception to the 3N bound (SUGGESTION)
- **Lenses:** Docs
- **Location:** `docs/guides/integrator.md:254`: "up to three rounds (`3*N_STREAM_OUT_P` clocks)".
- **Authority/evidence:** at N = 1 the latency is 4 clocks, which is more than 3N. This is stated at 10 §6.3 (:316), in the `srp_sr_admitted_o` row (:285) and in `protocol_processor_top.sv:523-524`, and measured here (`sigma-head-N1-*.log`: max 4).
- **Impact:** only integrators running a one-source shape could mis-budget, by one clock.
- **Required outcome:** add "(four clocks for one source)" as the adjacent row does.
- **Verification:** reading.

### S3: the admission banner's over_limit gloss is older than its port comment (SUGGESTION)
- **Lenses:** Docs
- **Location:** `hdl/srp/KL_srp_admission.sv:38`: "over_limit view (some requested source stands refused)". Compare `:81`, "some evaluated source refused by the ceiling (latched by published rounds)".
- **Authority/evidence:** after a refused source withdraws, `over_limit_o` stays high until the next publication (by design; 10 §6.3 "snapshots latched by published rounds"). "Stands" reads as live.
- **Impact:** negligible; the port comment, the architecture page and the integrator guide are correct.
- **Required outcome:** align the banner wording with `:81`.
- **Verification:** reading.

## Prior public review findings at this head

I read these only after the verdict and ledger above were fixed: R299-1 (5816799437) and R298-1 (5816919660), both NEGATIVE at `73a5478`. No other review findings exist on PR #114.

| Prior finding | Status at f222f6b | Evidence |
|---|---|---|
| R299-1 F1 / R298-1 F1 (MAJOR): a pending re-declaration releases capacity and licenses a refused higher-index source | **RESOLVED** | The discard rule in the RTL. My round-1 verification commands, re-run unchanged, give unit 28/28 and 112/112, top 80/80 and wire 0/40, with P1 at 0. New processor-top probe: 0 licensed runs. The pending-absent mutant fails the new unit (44/368 named) and srp_top (72/72) tests. The Σ-context oracle is present. 10 §6.3 `sec-10-admission-cross-source`, the integrator row and the banner state the rule. R298-1's own probe scripts are that reviewer's; their required properties (no refused grant, Advertise or ACTIVE; shrink still admits) are covered by my probes and the author's I section |
| R299-1 F2 / R298-1 F2 (MINOR): parent consumer idiom gates fail | **RESOLVED** | [A266] `90e1ce1` is kept at head. The cited multi-declarators are gone, and every public function in `mutants.py` is annotated and documented (`prior-findings-recheck.txt`). The manager's receipt 5818943152 reports the parent consumer gates 7/7 PASS with this head staged. The change is output-identical (`a266-equivalence.txt`). I did not run the parent gates |
| R299-1 S1 / R298-1 S3: stale port-comment wording | RESOLVED | `protocol_processor_top.sv:528` "zero until the real grant, follows srp_sr_admitted_o"; `KL_srp_top.sv:216-218` latched / "pending is not refusal" |
| R299-1 S2: the area reduction is unexplained | RESOLVED | `syn/ooc/README.md` explains the round-1 remapping and accounts for the round-2 flip-flops bank by bank |
| R298-1 S1: CI ran only N=8 | RESOLVED | `tb/srp_admission/Makefile:6` `all: shapes`; `run_suites.sh:30` runs `make` |
| R298-1 S2: service-rate / storm assumption | RESOLVED | integrator svc row (:254) and 10 §6.3 storm clause |
| R298-1 S4: `!invalid_w` term in `fit_w` equivalent; comment it | RESOLVED | `KL_srp_admission.sv:185-186` comments the validity terms as defensive |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #112 acceptance 1–5; manager decision 5816928229 items 1–7; A266/A267/A273 comments; manager validation 5818943152; 10 §6.3 (:276, :292, :334); F02.10 (:430-431); greedy/ceiling rule; unit, srp_top, processor-top and wire probes; port-surface comparison | R299-2 | f222f6b96328c8eb0f4d2c5c3470ebd365e51fdc |
| RTL | CLEAN | `KL_srp_admission.sv` in full; `KL_srp_top.sv` invalidation (:759), window (:785-796, :870-878), FSM feed (:450), op routing (:805-845); `protocol_processor_top.sv` ports/SRP adapter and #111 overlap; merge diff equivalence; scoped lint at 5 shapes; syn/ooc area accounting; M1 equivalence proof | R299-2 | f222f6b96328c8eb0f4d2c5c3470ebd365e51fdc |
| Robustness | CLEAN | randomized multi-source/same-edge/burst/withdraw/saturation traffic at N = 1/2/3/5/8; liveness bound; live-Σ bound; join-tick placements; hold storm with GSI; starvation clause; window growth to 41 | R299-2 | f222f6b96328c8eb0f4d2c5c3470ebd365e51fdc |
| Tests | CLEAN | `tb/srp_admission` (sim_main oracle, wrap, Makefile, mutants.py, README); `tb/srp_top` H/I/J and wrap taps; `pp_top` + `gsi_mutants.py`; author 12-verdict campaign; round-1 7-mutant campaign; 9 new Σ-probe mutants; D/E/I against author suites; A266 equivalence; hosted check runs | R299-2 | f222f6b96328c8eb0f4d2c5c3470ebd365e51fdc |
| Docs | CLEAN (S1–S3 non-blocking) | 10 §6.3 text vs. measurements; integrator svc and port rows; top and `KL_srp_top` port comments; admission and srp_top banners; tb READMEs; MODULE_MATRIX; `syn/ooc/README.md` and `srp_ooc.tcl`; link/matrix/modmatrix gates | R299-2 | f222f6b96328c8eb0f4d2c5c3470ebd365e51fdc |

## Real limits

- The following were not run: the full 33-suite bank, `lint_hdl.sh` over all 40 tops, Yosys/portability, the builder and native banks, the gPTP bank, the parent consumer gates and vendor synthesis (not allowed or not available). The area figures (+37 LUT / +17 FF) were checked for internal consistency only. Parent gate status rests on manager receipt 5818943152.
- The randomized Σ probe uses a 1 Gb/s port and class-A slopes from ten frame sizes, with MaxIntervalFrames 1–4 and occasional saturation. Other port rates were not swept.
- The processor-top probes use the pp_top bench's 100 Mb/s port and its time compression (1 ms = 100 clocks). The storm probe drives one source; it shows that GSI is unaffected by holds, not every possible svc/listener interleaving.
- The probe wrappers add observe-only hierarchical taps in scratch copies; no RTL was modified.
- Physical calibration was NOT RUN. No hardware was used, and field skips are not hardware proof.
- The final current-dev candidate (source base 939c143, live dev 573f0052) is distinct from the source validated here.
- Clone integrity after all work (`clone-integrity.txt`):
  - HEAD and tree are exact, porcelain status (including ignored files) is empty, and the index and worktree are clean;
  - all 246 tracked entries match in blob bytes and modes;
  - there are 0 gitlinks and no `.gitmodules`, because the repository has no submodules, so there are no gitlinks to restore.

## Pending manager duties

- Build and validate the merge-turn current-dev candidate against live dev `573f0052`.
- Hosted and act acceptance.
- Parent consumer gates on the final candidate.
- Physical calibration when scheduled.
- Merge still requires two independent positive reviews and the full completion bar.
- The S1–S3 suggestions can be picked up at the author's discretion.

## Packet contents

- `REPORT.md`.
- `probes/r1/`: the round-1 probes, byte-identical to the R299-1 manifest.
- `probes/r2/`: `sigma_random_probe.cpp`, `run_sigma_probe.sh`, `mutants_r2.py`, `mutants_r2_suites.py`, `pp_top_cross_probe.inc`, `run_pp_top_probe.sh`.
- `receipts/`: raw logs. Local absolute paths are redacted to `<packet>`, `<scratch>`, `<clone>`, `<pinned-tool-bin>`, `<pinned-tool-root>` and `<home>`.

Every publishable file is listed in `MANIFEST.sha256`. `scratch/` is disposable and not published.

R299-2 FINISHED
