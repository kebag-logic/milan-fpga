[R298] POSITIVE - exact head f222f6b96328c8eb0f4d2c5c3470ebd365e51fdc

# R298-2 internal independent review: issue #112 / PR #114, round 2

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #114 (closes #112).
- Exact head `f222f6b96328c8eb0f4d2c5c3470ebd365e51fdc`, tree `60b6e1b11dfa57558a2d839a36d8a6769c0a4e72`.
- Source base `939c143333d11e2378a514f1c7b6abd4c3259bfd`. Processor main merged at this head: `7a47f5788ff504f099a47ad4407c340771bb6bdb` (#111).
- Reviewer role: internal independent reviewer. The review ran in a cleared context in an isolated detached clone. There were no GitHub writes, source edits, commits, pushes or author contact.
- Simulator: the pinned Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`), identity checked before use.

## Reconstruction order

1. Repository conventions. There is no AGENTS.md or CONTRIBUTING.md, so the conventions came from `README.md` and `docs/README.md`.
2. Issue #112: the body with the five frozen acceptance items, plus the manager and author comments:
   - 5816023315: A259 assignment.
   - 5816726610: A266, round 1b, test idiom.
   - 5816928229: A267, the manager's round-2 design decision.
   - 5818554274: A273, the merge round.
   - The three REVIEW READY receipts.
   - Parent decision context: kebag-logic/milan-fpga comment 5816014072.
3. PR #114: the body, and the review-start comment 5818801802.
4. Interface authorities:
   - 10 §6.3, including the anchors `sec-10-admission-freshness` and `sec-10-admission-cross-source`.
   - F02.10.
   - The integrator guide rows.
   - The port comments in `protocol_processor_top.sv` and `KL_srp_top.sv`.
   - The admission banner.
5. `git diff 939c1433..f222f6b9` (34 files) and the PR-own diff `7a47f578..f222f6b9` (16 files), with the history of `73a5478`, `90e1ce1`, `fbabb94`, `ae7f531` and `f222f6b`.
6. Public evidence at kebag-logic/milan-fpga@da848abf `review-evidence/pp112-r1`. Five merge-round receipts were hash-checked against its MANIFEST.json, and all match.
7. Hosted check runs at the exact head.
8. **Only after my own independent pass:** the prior public round-1 findings, R298-1 (comment 5816919660) and R299-1 (comment 5816799437). The concurrent R299-2 review was not read.

## Verdict

**POSITIVE.** The round-2 design of manager decision 5816928229 is implemented exactly:

- The pending source's own grant goes low when its declaration is accepted: `grant_r & ~invalid_w` (`hdl/srp/KL_srp_admission.sv:223`).
- A round that visits a requesting source without a valid current slope is discarded (`pend_w`/`pend_acc_r`, `:192`, `:233`). So every other grant, every granted slope, `sum_slope` and `over_limit` keep their last published values.
- Capacity is released only by a withdrawal (the live AND with `req`) or by an evaluated shrink.
- Only published rounds strobe `round_done_o`, so the optimistic window counts published rounds only (`KL_srp_top.sv:785-797`).

Evidence for the verdict:

- My round-1 probes, re-run at this head, report 0 FAIL at unit N=2 and N=8, in srp_top (including the wire) and at the processor top. The processor top shows 0 admitted cycles.
- An independent randomized oracle, written from 10 §6.3, runs about 120 M checks at N=1/2/3/5/8 with 0 FAIL. It also kills every reviewer and author mutant, and round 1's RTL.
- #111's GET_STREAM_INFO behaviour is unaffected. The full pp_top functional transcript at processor main and at this head is identical, and the 13 GSI mutants are all detected.
- No MINOR, MAJOR or BLOCKER finding is open at this head.
- Both prior MAJOR findings (R298-1 F1, R299-1 F1) and both MINOR findings (F2) are resolved.
- Two SUGGESTIONs are raised below. They do not affect the verdict.

## Findings at this head

### S1: the integrator's svc-face note omits the four-clock case at one source (SUGGESTION)

- **Severity:** SUGGESTION.
- **Lenses:** Docs.
- **Location:** `docs/guides/integrator.md:254` says "takes up to three rounds (`3*N_STREAM_OUT_P` clocks)".
- **Authority/evidence:** 10 §6.3 (`docs/architecture/10_srp_engine.md:314-316`) gives three rounds for M ≥ 2 and **four clocks for M = 1**. The same guide's `srp_sr_admitted_o` row (`:285`) and the top port comment (`hdl/top/protocol_processor_top.sv:523-524`) say so as well. The unit suite and my fuzz both measure 4 clocks at N=1 (fuzz `max_latency=4 bound=4`).
- **Impact:** at `N_STREAM_OUT_P = 1` the svc row understates the hold by one clock. The authoritative row next to it is correct.
- **Required outcome (optional):** add "(four clocks at one source)" to the svc row.
- **Verification:** reading. `make check` stays green.

### S2: the admission README keeps the pre-merge srp_top control tally (SUGGESTION)

- **Severity:** SUGGESTION.
- **Lenses:** Docs, Tests.
- **Location:** `tb/srp_admission/README.md:91-92` says "the controls pass (… 1527 in srp_top)".
- **Authority/evidence:** at this head the srp_top control runs **1531** checks. That figure appears in `tb/srp_top/README.md:14`, the campaign log `receipts/author_mutants/control-srp-top.log` and `receipts/head_srp_top.log`. The per-mutant failure counts in the same paragraph (105/205/90 in srp_top) reproduce exactly.
- **Impact:** a stale dated number only. Every verdict is unaffected.
- **Required outcome (optional):** refresh the number, or mark it as measured at `ae7f531`.
- **Verification:** re-run `tb/srp_admission/mutants.py`.

## Focus items judged

| Item | Result | Evidence |
|---|---|---|
| [A266] test idiom fixes, no behaviour change | Confirmed. Only `tb/srp_top/sim_main.cpp` and `tb/srp_admission/mutants.py` change. The srp_top and admission N=8 stdout at `73a5478` and at `90e1ce1` are byte-identical, apart from build lines (0 diff lines). The parent idiom gates were not run here (manager/author receipts). | `receipts/a266_*`, `receipts/r1_*`, `receipts/r1b_*` |
| [A267] RTL implements the manager design | Confirmed by reading and by probes. `pend_w = !invalid_w && !slope_valid_r` sets `pend_acc_r`. The round_w branch publishes, and strobes `round_done_o`, only when `!(pend_acc_r ‖ pend_w)`. Invalidation retires only the changed/non-requesting grants and restarts the partial round. Aggregates move only on publication. | `KL_srp_admission.sv:185-256`; fuzz C5/C6/C6b/C9 |
| Cross-source test at every phase | Covered.<br>• Unit: for every sampling phase p < N, at N ≥ 2, there are identical, shrink, grow and double re-declarations of source 0 with N-1 refused and watched on every clock (`tb/srp_admission/sim_main.cpp:181-194`), a freeing shrink and a withdrawal (`:197-213`), and a pending middle source at N ≥ 3 (`:216-228`).<br>• srp_top I: sources 1 and 7 × 3 frames × 8 phases = 48 runs, plus 40 join placements. In every one, `refused_levels = 0`, meaning no grant, no ACTIVE and no declared Advertise. The freeing control grants on the same clock as source 0 (`hi_first = lo_first`).<br>• srp_top J: 8 phases × 6 gaps, with 0 Failed. | `receipts/head_srp_admission_shapes.log`, `receipts/head_srp_top.log` (CROSS/WINDOW lines) |
| Σ-context oracle | Sound and strong. Every clock checks:<br>• the live Σ is at or below the ceiling;<br>• a publication equals the greedy walk over **all** current declarations (grants, slopes, sum, over);<br>• between publications, grants only retire with their own declaration, and slopes, sum and over hold (`tb/srp_admission/sim_main.cpp:87-115`).<br>srp_top I applies the same rule to recorded rounds against its own model (`tb/srp_top/sim_main.cpp:1337-1394`). My independent oracle adds three further checks: a publication at least 4 clocks after every change, a changed source low until the next publication, and the latency bound. It found no counter-example. | fuzz receipts |
| The 12 campaign verdicts | Reproduced 12/12. Controls pass: 12615, 991231 and 1531 checks. The failing counts are 402/5473/105 (stale-evaluation), 175/1067/205 (pending-absent) and 146/695/90 (discarded-round-strobes), each on its named check. | `receipts/author_mutants*` |
| Validity-term removal now equivalent | **Verified.** By argument: a pending visit sets `pend_acc_r`, or blocks publication at `round_w`. The working state (`wgrant`/`acc`/`over_acc`) is cleared at every round end and every restart, so it never reaches an output. By lockstep: head against a variant with both `&& slope_valid_r[aidx_r]` terms removed gives 0 output mismatches over about 120 M checks at N=1/2/3/5/8. Round-1 A5 (drop `!invalid_w` from `fit_w`) is also equivalent under the port contract (`req` changes only with an invalidation strobe), with 0 mismatches over 35 M checks. As a positive control, removing the request qualification as well is **not** equivalent, and the lockstep check catches it. | `receipts/fuzz_head_eq_N*.log`, `receipts/fuzz_equiv*` |
| Window-length change (round 1: 25 at every phase; head: 25/33/41 at 8 sources) | Measured at 25/33/41 clocks (shrink/identical H runs: 10/32/6). That is 17 clocks past the publishing round, as documented in 10 §6.3 (`10_srp_engine.md:334-351`) and in the srp_top README. The effect is a longer optimistic Advertise for a fresh declaration. At most 41 clocks is 410 ns at 100 MHz, orders of magnitude below T-MRP-JOIN. J shows the window never closes before a held verdict publishes, and the discarded-round-strobes mutant proves that check is live. | `receipts/head_srp_top.log` LATENCY/WINDOW |
| Area: +37 LUT / +17 FF against 939c1433 | Vivado is not available here, so the absolute numbers were not reproduced. The register attribution (validity 10, `pend_acc_r` 1, 5 `aidx_r` replicas, `wgrant_r[7]` kept) adds up, and it matches the engine and `u_admission` rows (862 → 879). An independent generic Yosys synthesis of `KL_srp_admission` (N=8) gives 913 → 924 FF bits (+11 = validity 10 + `pend_acc_r` 1), with round 1 at 923. That matches the tool-independent part of the attribution. RAM and DSP are unchanged per the author. | `receipts/yosys_admission_*.stat`; `syn/ooc/README.md:87-131` |
| #111 GET_STREAM_INFO unaffected by the hold | Confirmed:<br>• The admission outputs reach only the top ports and side-port snapshot words 3, 11, 12 and 30. The GSI input path reads the sink registrar and the listener record.<br>• The merge tree equals an automatic re-merge, except for the two README conflict resolutions.<br>• The full pp_top functional output is identical at main `7a47f578` and at this head. Both have 1948 checks and 0 FAIL; only build lines differ.<br>• `gsi_mutants.py` at head detects 13/13, and the golden and restored runs pass with 488 checks each.<br>• The processor-top ports are identical to main and to base. | `receipts/pp_top_main_vs_head.diff`, `receipts/gsi_mutants*`, `receipts/port_lists_compare.txt` |

## Issue acceptance mapping (at this head)

| # | Status |
|---|---|
| 1 | **Met**, including the cross-source case:<br>• The grant never rises from a round that evaluated a non-current slope, and the declaring source's grant is low from acceptance.<br>• My processor-top probe gives 0 admitted cycles over 48 runs; the pre-fix RTL through the same probe gives 596.<br>• The fuzz C2/C5/C5b/C9 checks give 0 FAIL at five shapes. |
| 2 | **Met.** Both directions, two or more sources, every phase, unit and engine. The refused case shows no pulse. The admitted latency is stated and measured: 4; 4/6; 6/9; 5/10/15; 8/16/24 clocks. The engine gives 8/16/24, and 16/24 beside a refused source. |
| 3 | **Met.** The stale-evaluation mutant (both protections removed) fails its named check in all three benches. My round-1 A1–A3, A4 (re-anchored), A6 and T1 are killed. Five further reviewer mutants are killed by both the author suites and my fuzz. |
| 4 | **Met.** No top-level port change. ACTIVE, the window, `sum_slope`, `granted_slope` and `over_limit` behave as the updated 10 §6.3, the integrator rows, the admission banner and the port comments state (fuzz C3/C4/C6b; srp_top H/I/J). |
| 5 | **Source side met.**<br>• Focused suites at head: srp_admission 1138/12615/41012/201073/991231, srp_top 1531 and pp_top 1948, all 0 FAIL.<br>• `lint_hdl.sh` and `make check`: rc 0.<br>• Hosted `suites`, `docs-gates` and `portability`: success in both the push and pull_request runs at the exact head. The Verilator build step was skipped on a cache hit; the test steps executed.<br>• The parent consumer gates rest on the author/manager receipts (371 checks). They were not run here. |

## Prior public review findings: resolution at this head

| Finding | Status | Evidence at this head |
|---|---|---|
| R298-1 F1 (MAJOR): a pending re-declaration releases capacity to a refused higher-index source | **RESOLVED** | My unchanged round-1 probes report:<br>• unit cross-source 792/792 at N=2 and 32832/32832 at N=8 (cases A/B/D at 0, shrink control C at 0);<br>• srp_top 192/192 over 32 runs, each with 0 refused grant, 0 ACTIVE, 0 Advertise and 0 wire Advertise;<br>• processor top 0 admitted cycles.<br>Against round 1's RTL/tree the same probes fail 36/240 and 80/192, so they are still sensitive. The required tests, the Σ-context oracle, the pending-absent mutant and the docs (10 §6.3 cross-source anchor, integrator rows, banner) are present. |
| R298-1 F2 (MINOR): parent idiom gates fail | **RESOLVED** (manager/author receipt) | A266 `90e1ce1` is kept, and the no-behaviour-change claim was verified here. The parent gates at the head (cpp/py idiom, source lists, pp_shadow 371) rest on the A267/A273 receipts; this review did not run them. |
| R298-1 S1: CI runs N=8 only | Resolved | `tb/srp_admission/Makefile`: `all: shapes` runs N=1/2/3/5/8. |
| R298-1 S2: service-rate assumption | Resolved | The integrator svc row (`:254`) and 10 §6.3 state that churn holds verdicts. |
| R298-1 S3: "same optimistic lag" comment | Resolved | `protocol_processor_top.sv:528`. |
| R298-1 S4: A5 equivalent; comment the defensive term | Resolved | `KL_srp_admission.sv:185-186`. A5 is equivalence-checked here. |
| R299-1 F1 (MAJOR): same defect, with wire and P1 | **RESOLVED** | Same evidence as R298-1 F1. The wire placement k = 1..40 is exercised by srp_top I, with 0 Advertise. P1 (the concurrent refused grow) is covered by my processor-top probe (0) and by unit case B (0). Every item of its required outcome is present: the Σ-context oracle, every-clock checks at every phase at unit and srp_top level, the pending-absent mutant, and the docs. R299-1's own probe scripts were not executed by this review; they belong to that reviewer. |
| R299-1 F2 (MINOR) | **RESOLVED** (manager/author receipt) | As R298-1 F2. |
| R299-1 S1: SRP-top and top port comments | Resolved | `KL_srp_top.sv:216-218`, `protocol_processor_top.sv:517-532`. |
| R299-1 S2: the area drop is unexplained | Resolved | `syn/ooc/README.md:111-127` gives the remap explanation and the bank-by-bank FF attribution. The FF part is consistent with the Yosys cross-check. |

## Reviewer probes and commands (all in the foreground, at most 8 parallel jobs)

- **Head suites:** `make shapes` (tb/srp_admission), `make` (tb/srp_top, tb/pp_top), `tb/srp_admission/mutants.py` and `tb/pp_top/gsi_mutants.py`, on a `git archive` extraction of the exact head.
- **Round-1 probes, unchanged:** `scripts/r298-1/*` are byte-identical to the published R298-1 scripts (`receipts/r298-1_scripts_identity.txt`).
  - The processor-top runner's text anchor `Suite(h).run();` no longer exists after the #111 merge, which wraps it in `if (!gsi_only)`. The unchanged runner stops with an assertion (`receipts/r1probes/probe_pp_top_head_unchanged_anchor_fail.log`).
  - An anchor-only adaptation (`scripts/r298-2-adapted/probe_pp_top_run.sh`, diff in `receipts/r1probes/probe_pp_top_adaptation.diff`) leaves the probe body unchanged. It gives 0 admitted cycles at head and 596 with the pre-fix main RTL.
  - Mutant A4's anchor no longer matches, because the restart branch now also clears `pend_acc_r`. A re-anchored A4 with the same intent is killed in all three benches (`scripts/r298-2-adapted/mutant_a4_adapted.py`).
- **New reviewer fuzz** (`scripts/fuzz/`): an independent oracle drives random declarations, re-declarations, withdrawals and occasional simultaneous two-source changes. It uses TSpecs near the ceiling, saturation, MaxIntervalFrames 0, 1 Gb/s and 100 Mb/s, and change rates of 1–40 %/clock with quiet stretches. It checks 11 properties every clock, and runs lockstep equivalence against a second RTL variant.
- **Mutants:** five reviewer-added mutants (no restart branch, no grant retire, stage-1/2/3 kill removed), the three author mutants and round 1's RTL are all killed by the fuzz. The five reviewer-added mutants are also killed by the author suites (`receipts/author_suites_reviewer_mutants*`).
- **Lint:** `KL_srp_admission` at N=1/2/3/5/8 with the repository lint flags, plus `scripts/lint_hdl.sh`: rc 0. `make check` and `gen_matrix.py --check`: rc 0.
- **Merge:** the merge commit was compared with `git merge-tree --write-tree ae7f531 7a47f57`. Only `syn/ooc/README.md` and `tb/srp_top/README.md` differ, and those are the resolved conflicts.
- **Clone integrity** (`receipts/clone_verify.txt`): HEAD, tree and index tree are exact, and 246 tracked entries match in blob bytes and modes. The worktree and index are clean. There are no untracked or ignored files and no gitlinks, because the repository has no submodules. An empty `abc.history` that my synthesis probe wrote into the clone was inspected, removed and re-verified. The helper was then amended to run in its output directory, and its output was re-checked identical.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #112 acceptance 1–5; manager decision 5816928229 and A266/A273 assignments; parent #551 decision 5816014072; 10 §6.3 (freshness, cross-source, window, accounting); F02.10; unchanged top ports; round-1 probes; fuzz C1–C9 | R298-2 | f222f6b96328c8eb0f4d2c5c3470ebd365e51fdc |
| RTL | CLEAN | all of `KL_srp_admission.sv` (validity pipeline, override loop, pend/discard, restart, publish, outputs); `KL_srp_top.sv` invalidation strobe, sole `adm_*` write site, window aging, `sr_adm_fsm`; top SRP wiring and snapshot readers; merge against re-merge; lint N=1/2/3/5/8 and `lint_hdl.sh`; lockstep equivalence; generic synthesis FF count | R298-2 | f222f6b96328c8eb0f4d2c5c3470ebd365e51fdc |
| Robustness | CLEAN (R298-1 S2 now documented) | all phases and shapes; simultaneous and rapid changes; withdrawal while another source is pending; saturation; MaxIntervalFrames 0; 100 Mb/s; latency bound tight at 3N (4 at N=1); held verdicts under churn (documented in 10 §6.3 and integrator `:254`); wire through two join periods | R298-2 | f222f6b96328c8eb0f4d2c5c3470ebd365e51fdc |
| Tests | CLEAN (S2 non-blocking) | `tb/srp_admission` (sim_main, wrap, Makefile, mutants.py, README); `tb/srp_top` H/I/J and wrap probes; campaign 12/12; 5 reviewer mutants against the author suites; A266 identity; GSI campaign 13/13 | R298-2 | f222f6b96328c8eb0f4d2c5c3470ebd365e51fdc |
| Docs | CLEAN (S1, S2 non-blocking) | 10 §6.3 (`10_srp_engine.md:257-366`); integrator rows `:254`, `:284-287`; top and SRP port comments; admission and SRP-top banners; tb READMEs; `syn/ooc/README.md` and `srp_ooc.tcl`; MODULE_MATRIX; `make check` | R298-2 | f222f6b96328c8eb0f4d2c5c3470ebd365e51fdc |

## Real limits

- Physical calibration was NOT RUN. No hardware was used. Field skips are not hardware proof.
- The absolute Vivado area (7603 LUT / 10502 FF) was not reproduced, because Vivado is not available here. Only the flip-flop attribution was cross-checked with generic synthesis of one module.
- Not run here, by instruction:
  - the full 33-suite bank;
  - the parent consumer gates;
  - the PP/gPTP/Yosys/builder/native banks;
  - act or Docker.
  Those rest on the author and manager receipts, five of which were hash-verified.
- The fuzz is randomized simulation, not formal proof: about 120 M checks over 1500 episodes of 4000 clocks. The equivalence argument for the validity-term removal is by construction; the lockstep run supports it.
- R299-1's own probe scripts were not executed. Their scenarios are covered by the author's srp_top I/J and by my probes.
- One round-1 A4 run was started detached by mistake. It was waited for in the foreground, completed normally, and no probe process remained afterwards.
- Receipt logs have local paths redacted to `<packet>`, `<pinned-tool-bin>`, `<pinned-verilator-root>`, `<review-clone>`, `<round-1-packet>`, `<home>` and `<tmp>`.

## Pending manager duties

- Build the merge-turn current-dev candidate: source base `939c143333d11e2378a514f1c7b6abd4c3259bfd`, live dev `573f0052a0e4412e81f0845438fcec2086ce5d55`. Run the full static, builder and native banks there.
- Run the parent consumer gates (cpp/py idiom, RTL source lists, pp_shadow) with this head as the processor gitlink at parent dev (acceptance 5).
- Own hosted and act acceptance. At capture, the hosted `suites`, `docs-gates` and `portability` jobs were all successful at the exact head, and the legacy commit-status API showed no statuses.
- Own physical calibration when it is scheduled.
- Reconcile this report with the independent R299-2 report after publication. Merge still needs two independent positive reviews.
- Optionally carry S1 and S2 to the author.

## Packet contents and reproduction

- `REPORT.md`, `MANIFEST.sha256`.
- `scripts/fuzz/`: `fz_wrap.sv`, `fz_main.cpp` and `run_fuzz.sh <tree> <A.sv> <out> <N> <EQ> <seed> <episodes> [<B.sv>]`.
- `scripts/author_suites_on_mutant.sh` and `scripts/yosys_admission_ff.sh`.
- `scripts/r298-1/`: the round-1 scripts, unchanged.
- `scripts/r298-2-adapted/`: the anchor-only pp_top runner, the mutant subset runner and the re-anchored A4.
- `receipts/`: raw logs, and `summary.txt` with every headline number.
- Trees are `git archive` extractions of the exact head, of base, of `73a5478`, of `90e1ce1` and of main `7a47f578`.
- Put the pinned Verilator 5.050 first on PATH, or set `VL_PINNED` for the round-1 scripts.

R298-2 FINISHED
