[R488] NEGATIVE - exact head 9050c4bbd25556929a0f24fb98258bc98e3bcfbe

# R488-2 internal independent review: issue #134 / PR #160

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #160 (`pp134-lv-leave` into `main`).
- Exact head `9050c4bbd25556929a0f24fb98258bc98e3bcfbe`, tree `3bcc8532549ea69139323a863049022d10f799c1`. Source base `ead8036035affd53ef4b29979190f2f4f67084c0`. Merged main `21c6f7096ac80007f723de59c6f717f55bd34cfc`.
- Review start: PR #160 comment 6000474432. This is a cleared-context pass in a detached clone of its own. Every build and probe ran on a `git archive` extraction under the packet's `scratch/`. The clone was never built in or patched (see Integrity).
- Simulator: pinned Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`, wrapper sha256 `905795b9…e92f`, `receipts/tool-identity.txt`).

## Verdict summary

The RTL fix is correct and does what the round-2 ruling asks:
- Both registrar planes now consume the one-clock leavetimer! before a same-clock rLv, rLA, txLA, rIn or rMt.
- A same-clock New, JoinIn or JoinMt still finishes IN.
- No port, register or parameter changed.
- The restoration mutant is byte-identical to the pre-fix RTL.
- Every count, measured figure and planted-fault result that I re-ran matches its README or PR-body statement, with two exceptions.

My own integration probe lands a registering JoinIn on the expiry clock. That is a case the lane's integrated sweep does not drive, and the head passes it 6432/6432. A fault that lets the expiry beat the renewal fails exactly the 16 same-clock cases.

The verdict is NEGATIVE because of two MINOR record defects. Neither is in RTL behaviour:
- **F1 (MINOR).** The suite README's mutation record says that neither #134 arm fails any other check of the suite. At this head, `lv-never-ends` fails 3016 SC2 checks of the complete default suite.
- **F2 (MINOR).** The PR body's two suite-bank totals differ by 6,560. The per-suite tallies of the base the PR body names give 6,584.

Both prior public findings on this PR (R488-1 F1 MAJOR, R488-1 F2 MINOR) are **resolved** at this head.

## Reconstruction (order followed)

1. **Contributor guides.** This repository has no AGENTS.md or CONTRIBUTING.md (`git ls-files` finds neither), so I read the conventions from `README.md` and `docs/README.md`. Three of them apply here:
   - §2: the single-source rules, with timing values only in F08.1;
   - §4: the citation style;
   - §6: `make check` before commit.
2. **Issue #134, frozen acceptance.** It sets three conditions:
   1. the arm passes, both mutants turn red, and both are recorded in the suite README;
   2. 10_srp_engine.md states the LV-case behaviour with the clause;
   3. the donor gates and the parent consumer gates pass.

   The maintainer and manager comments add the following:
   - **Lane comment 5988316116:** run both an own and a peer LeaveAll; cite Table 10-4; record LeaveTime against Milan Table 4.3.
   - **Round-2 ruling 5990549074:** route (b), fix the RTL in both planes. An expiry is never lost to a same-clock received event. Every pair is recorded against Table 10-4. The arm sweeps k = 0..400 on both planes for own and peer LeaveAll. Add a restore-order mutant. Docs and the `sim_main.cpp` comment state the same-clock rule. F2 states the head's clock count. OOC area stays at or below 40 LUT / 40 FF.
   - **Round-3 ruling 5994864535:** fix the D3 format, check record equality, and `--no-ff` merge main 21c6f709.
   - **Round-3b ruling 5995957938:** add the fifth parent patch.
   - **REVIEW READY 6000454088:** posted at this head.
3. **Authorities.** All three are taken from the repository's quotations and the standard's tables. The specification PDFs are not distributed.
   - **802.1Q-2014 Table 10-4.** Row `rLv!/rLA!/txLA!/Re-declare!`: IN gives "Start leavetimer" and LV; LV and MT give `-x-`. Row `leavetimer!`: LV gives Lv and MT. Rows `rNew!`, `rJoinIn!` and `rJoinMt!` give IN from LV and from MT. rIn! and rMt! are not registrar events.
   - **Δ13 (Milan §4.2.7.2.2).** `01_overview.md:148` replaces only IN / rLv!.
   - **Milan Table 4.3 LeaveTime.** 5000 ms (4500–7500), held as REQ-SRP-001 (`00_MILAN_COMPLIANCE_REVIEW.md:498`) and F08.1 T-MRP-LEAVE (`08_timing.md:40`).
4. **Diff `ead8036..9050c4bb`.**
   - **Size.** 64 files, +1911/-228. Of that, 40 files and their hunks come from merged main 21c6f709 (PRs #156 and #159, already landed).
   - **Merge commit.** `git merge-tree --write-tree 9d26598 21c6f70` gives exactly the head tree `3bcc8532…`. The two sides touch no common file. So the merge is a clean automatic `--no-ff` merge, with no hand resolution.
   - **Lane-own change.** `git diff 21c6f70..HEAD` is 24 files, +646/-36:
     - two RTL files, a branch reorder only;
     - `10_srp_engine.md` §6.5;
     - the `tb/srp_top` and `tb/srp_stream_fsms` arms, READMEs and patches;
     - the `tb/pp_top/d3_phases.hpp` format fix.
5. **Public evidence.**
   - **What the evidence directory covers.** milan-fpga `7aecfd0b…/review-evidence/pp134-r1` holds `MANIFEST.json`, the author HANDOFF.md (sha256 `fb077d45…`, equal to the manifest's published hash), PR-BODY.md and four adoption patches. All of it is for the round-1 head `5ab43bd9`, not for this head.
   - **What covers this head.** The only public evidence at this head is the REVIEW READY comment (6000454088) and the PR body.
   - **Not re-run here.** I did not re-run the parent consumer set, the full processor bank, Yosys or the builder banks, or Vivado. The review rules exclude them, and they stay manager-owned.
6. **Prior public review findings.** I read them only after my own verdict and ledger were written (`receipts/verdict-ledger-before-prior-findings.md`). They are resolved or retained below. F2 came out of the bank arithmetic after that point, independently of any prior review.

## Executed evidence (reviewer runs; pinned Verilator 5.050)

| # | What | Result | Receipt |
|---|---|---|---|
| E1 | Complete default `tb/srp_top` at head | rc 0, `8656 checks: 8656 PASS, 0 FAIL`, `TOTAL_CLOCKS 210547557` (equal to `sim_main.cpp:368`). 6416 `LV_COLLISION … CLOSED` lines, 0 STUCK. The eight `LV_LEAVE` lines match README `:534-537`: own 14200 / 14216, 16700 / 19200 ms, peer 705 / 711, 3205 / 5705 ms, 5000 ms, one STREAM_STOP and no START each | `receipts/head-srp_top.log` |
| E2 | `tb/srp_stream_fsms` at head | rc 0, `1347 checks: 1347 PASS`, which is base 1219 + 128 SC1 | `receipts/head-srp_stream_fsms.log` |
| E3 | Full `tb/srp_top/mutants.py --jobs 6` at head | rc 0, 16 controls PASS. Every arm is KILLED, including `lv-second-lv-ends` 16 S1,S2; `lv-never-ends` 16 S2,S3; `lv-expiry-masked` 16 SC2 and 16 SC1; `lv-expiry-last` 48 SC1; `lv-expiry-dropped` 86 (80 SC1 + 6 older); `lv-sweep-misses-collision` 16 SC3. `assertion coverage: 86/86`, `137 checks: 137 PASS` | `receipts/srp-campaign.log`, `receipts/srp-campaign/` |
| E4 | Restoration mutant vs pre-fix RTL | `lv-expiry-masked` applied to head gives `hash-object` equal to the `21c6f70` blobs of both FSMs (talker `433d080f…`, listener `78014b42…`) | this report (command in Integrity) |
| E5 | Reviewer faults, one plane at a time (pre-fix order restored on one plane only) | listener-only: 8 SC1 + 8 SC2 failures, all on the listener plane. talker-only: 8 SC1 + 8 SC2, all on the talker plane. So each plane is guarded on its own | `receipts/fault-{listener,talker}-only-restore-{fsms,lvcoll}.log`, `.diff` |
| E6 | **Reviewer probe `r488join`** (`scripts/probe_join_collision.py`): the head's own calibration and snapshot replay, but a registering JoinIn decoded across the expiry clock, k = 0..400, both planes, own and peer LeaveAll, Ready and ReadyFailed, index 0 and 7. Required: every k ends IN. Before or on the expiry clock, no ACTIVE edge and no TK pulse. After it, one close then one re-registration. On the same clock, T-MRP-LEAVE + 200 ms more with no stale expiry | head: `6432 checks: 6432 PASS` (exactly one same-clock k per combination) | `receipts/probe-join-collision.log` |
| E7 | Reviewer fault `expiry-over-renewal` (expiry branch above the registering branch, both planes) | SC1 48 failures (every registering case). lvcoll green (Lv only). `r488join` **16 failures, all at rel = 0** (registration closed, STREAM_STOP 1). Both restore-only faults pass `r488join`, so the probe isolates the renewal path | `receipts/fault-expiry-over-renewal-*.log` |
| E8 | Checked-in arms through the complete head suite | `lv-second-lv-ends`: `8656 checks: 8640 PASS, 16 FAIL` (8 S1 + 8 S2). **`lv-never-ends`: `8656 checks: 5624 PASS, 3032 FAIL` (8 S2 + 8 S3 + 3016 SC2)** | `receipts/patch-lv-second-lv-ends-full.log`, `receipts/fault-lv-never-ends-full.log` |
| E9 | Older arms through `lvleave`, and dropped expiry through `lvcoll` | `talker-strict-lv` 16/24 S1,S2, closing at +14 ms. `talker-no-expiry` 16/24 S2,S3, never closing (README `:548-551` holds). `lv-expiry-dropped` fails all 6416 SC2 checks (PR body holds) | `receipts/patch-talker-*-lvleave.log`, `receipts/patch-lv-expiry-dropped-lvcoll.log` |
| E10 | Base tallies | `21c6f709` and `ead80360`: srp_top 2200, srp_stream_fsms 1219. `21c6f709` plus the head's D3 format fix vs head: pp_top `10444` at both, output identical after build-line normalisation; timer_map `1360` at both | `receipts/base-*.log`, `receipts/head-pp_top.log`, `receipts/head-timer_map.log` |
| E11 | Static gates at head | `make check` rc 0 (in a scratch clone, because it needs git): 41 mermaid + 18 wavedrom, 1174 links, 115 REQ, 94 rows / 0 untested, ids 91, figures OK. `lint_hdl.sh` rc 0. `gen_matrix.py --check` rc 0 | `receipts/head-make-check.log`, `head-lint.log`, `head-matrix.log` |
| E12 | Focused Yosys (sv2v + `synth -lut 6`) of the two FSMs, pre-fix vs head | elaborate at both. One instance: talker 595 → 610 LUT6, listener 509 → 511, FFs unchanged (523, 389). This is a different tool and flow from the shipping OOC measurement and is not a substitute for it | `receipts/yosys-fsm-focused.txt` |
| E13 | R489-1-S1 recheck (`scripts/probe_harness_no_lv.py`): both target Lvs removed from group S | still `24 checks: 24 PASS` at head | `receipts/probe-harness-no-lv.log` |
| E14 | D3 format fix | `d3_phases.hpp:2963` has 4 conversions and 4 arguments. `:2993` has 6 and 6. `git grep -F` finds neither old line in `tb/**/*.patch` or in the `d3_mutants.py` / `notify_mutants.py` tables | inspection |
| E15 | Hosted checks at the exact head (read-only, 2026-10-05T19:13Z) | `docs-gates` and `portability` succeeded in both runs (37355190245, 37355183501). **`suites` still in progress** in both | `receipts/hosted-check-runs.txt` |

The scripts are portable and resolve paths from the packet directory:
- `scripts/run_review.sh` (sequence);
- `launch.sh` and `wait.sh` (detached job plus polled rc);
- `probe_join_collision.py`, `reviewer_mutants.py` and `probe_harness_no_lv.py` (probes);
- `clone_integrity.sh`.

As first run, `launch.sh` dropped the rc file of a failing job because its subshell inherited `set -e`. It was fixed before any recorded fault result: those jobs were re-run, and every listed `.rc` is from the fixed script. In published receipts, host-specific simulator image paths are redacted to `<PINNED_VERILATOR_IMAGE>` / `<HOME>`.

## Findings

### R488-2-F1: MINOR. The suite README's mutation record is false at this head for `lv-never-ends`

- **Lenses:** Tests, Docs.
- **Where:** `tb/srp_top/README.md:539-541`: "Neither arm fails any other check of the suite: each was run through the complete default suite of the base (2200 checks) and passed it". The table at `:543-546` follows it.
- **Authority:** Issue #134 acceptance 1 requires that the mutants are recorded in the suite README. The round-2 ruling put the `lvcoll` sweep into the default run (README `:555`).
- **Evidence:** E8. Through the complete default suite at this head (8656 checks), `lv-never-ends` fails 3016 SC2 checks besides its 16 S2/S3 failures. `lv-second-lv-ends` fails only its 16. R488-1's E4 made the sentence true at `5ab43bd9` (2224 checks), and the later SC group made it false.
- **Impact:** The README's present-tense record of what the arm kills is wrong. A reader concludes that `lv-never-ends` is isolated to group S, when it also turns 3016 sweep checks red. Because the sentence records a mutation measurement, this is not RESIDUE.
- **Required outcome:** Restate the record at this head. `lv-second-lv-ends` fails only S1,S2 (16 of 8656). `lv-never-ends` fails S2,S3 (16) plus 3016 SC2 in `lvcoll`. Alternatively, scope the sentence explicitly as the 2026-10-05 measurement against the 2200-check base, and add the head result.
- **Verification:** Plant each arm in a scratch export and run `make -C tb/srp_top` (the complete default run). The README's statement must match both tallies. `make check` stays green.

### R488-2-F2: MINOR. The PR body's suite-bank totals do not add up to the per-suite deltas

- **Lenses:** Tests, Docs.
- **Where:** PR #160 body, validation list: "The suite banks pass 1,021,664 and 1,028,224 checks respectively", for the "corrected merged base and head" of the line above. The difference is 6,560.
- **Evidence:** E1, E2 and E10.
  - Between `21c6f709` (with the head's format fix) and the head, only four suites build a changed file. I checked the `tb/*/Makefile` source lists: no other suite references the two FSMs, `KL_srp_top` or `d3_phases.hpp`, and no suite reads the changed docs.
  - Their measured tallies are srp_top 2200 → 8656 (+6456), srp_stream_fsms 1219 → 1347 (+128), pp_top 10444 → 10444 and timer_map 1360 → 1360.
  - The bank delta must therefore be **6,584**. The stated 6,560 is short by 24, which is exactly the size of group S.
  - So either one total is wrong, or the "base" bank was measured on a tree other than the one the line names, for example one that already carried group S.
- **Impact:** The PR's headline validation figure does not reconcile with deterministic suite tallies, and a reader cannot tell which tree "corrected merged base" was. It is a measured figure, so this is not RESIDUE.
- **Required outcome:** Name the exact base tree for the bank totals. Then either correct the figure so that head − base equals the sum of per-suite deltas, or show which suite accounts for the 24.
- **Verification:** A per-suite tally table (from `scripts/run_suites.sh`) at both named trees, whose sum difference equals the stated totals' difference.

### Suggestions (non-blocking)

- **R488-2-S1 (Conformance, Docs).** For a same-clock renewal, the RTL publishes the composed final state. It emits no Lv/Join indication pair, which Table 10-4 applied literally (expiry, then rNew!/rJoinIn! at MT) would emit. 10 §6.5 `:571-572` and README `:591-596` state and justify this choice, and the ruling asks for "the result". Consider naming it in F01.4's terms (a deviation or an implementation note), so that a compliance reader finds it without reading §6.5.

## Prior public review findings at this head

| Finding | Prior severity | State at 9050c4bb | Evidence |
|---|---|---|---|
| R488-1-F1: a same-clock rLv masks leavetimer!, and the §6.5 statement is false at a reachable timing | MAJOR | **RESOLVED** (ruling route (b)). Both planes test the expiry before rLv (`KL_srp_talker_fsm.sv:732-734`, `KL_srp_listener_fsm.sv:769-772`). The listener's `ind_unreg_w` (`:449-454`) now agrees with `reg_r`. 10 §6.5 `:566-576`, README `:553-596` and `sim_main.cpp:778-789` state the same-clock rule | E1 (6416/6416 CLOSED), E3 (restore order 16 SC2), E4, E5 |
| R488-1-F2: stale run-length figure at `sim_main.cpp:364-365` | MINOR | **RESOLVED.** `:368` states 210,547,557, equal to the measured `TOTAL_CLOCKS` | E1 |
| R488-1-S-1 / R489-1-S3: T-MRP-LEAVE value restated in 10 §6.5 | SUGGESTION | Adopted. `:557-558` cites T-MRP-LEAVE, F08.1 and Table 4.3 without the value | inspection |
| R488-1-S-2: the peer `aged` term accepts any received LeaveAll lane | SUGGESTION | Retained, non-blocking (`sim_main.cpp:839`, `dbg_rx_la_o` at `:381`). `lv1_reg == 2` still pins LV entry | inspection |
| R489-1-S1: group S does not observe that its Lvs were decoded | SUGGESTION | Retained, non-blocking. The no-Lv stimulus still passes 24/24. `lvcoll`'s SC3 does observe its decoded Lv | E13 |
| R489-1-S2: "as the integrator's STREAM_START/STREAM_STOP counters do" wording | SUGGESTION | Retained, non-blocking (README `:521-523`, `sim_main.cpp:357-359`). 02 `:541` has the counters count `streaming[src]` edges | inspection |

## Lens ledger (reviewer-owned)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Table 10-4 LV / leavetimer! composed with every received event (rNew, rJoinIn, rIn, rJoinMt, rMt, rLv, rLA, own txLA) against both priority chains (`KL_srp_talker_fsm.sv:720-744`, `KL_srp_listener_fsm.sv:747-784`); the Δ13 scope (`01_overview.md:148`); LeaveTime 5000 ms vs F08.1 / REQ-SRP-001 and the measured close at +5000 ms (E1); SC1 128 cases (E2); integrated JoinIn collision (E6) | R488-2 | 9050c4bbd25556929a0f24fb98258bc98e3bcfbe |
| RTL | CLEAN | lane RTL diff (a reorder only, no port, register or parameter); `ind_unreg_w` / `ind_reg_w` consistency; pending-ARM guard; timer-service cancel of an already-fired slot (`KL_pp_timer_service.sv:195-206`, which only clears `armed_r`); restore mutant byte-identity (E4); lint (E11); focused Yosys elaboration (E12); clean `--no-ff` merge (merge-tree equality) | R488-2 | 9050c4bbd25556929a0f24fb98258bc98e3bcfbe |
| Robustness | CLEAN | 401-offset sweeps on both planes, own and peer, Ready and ReadyFailed, index 0 and 7, for Lv (E1) and for JoinIn with a T-MRP-LEAVE + 200 ms stale-expiry watch (E6); per-plane restore faults (E5); expiry-over-renewal fault (E7); cycle budget 300 M vs 210.5 M measured; snapshot file under TMPDIR and unlinked | R488-2 | 9050c4bbd25556929a0f24fb98258bc98e3bcfbe |
| Tests | UNCLEAN (F1, F2) | `check_withdrawal_meets_an_lv_registrar`, `check_leave_expiry_collisions` and `collision_setup` (`sim_main.cpp:778-990`); SC1 (`srp_stream_fsms/sim_main.cpp:1069-1106`); `mutants.py` rows and S/SC coverage; the full campaign (E3); the README mutation record (E8, F1); bank arithmetic (E10, F2); the D3 format fix (E14) | R488-2 | 9050c4bbd25556929a0f24fb98258bc98e3bcfbe |
| Docs | UNCLEAN (F1, F2) | 10 §6.5 `:548-576` (clause, Δ13 scope, same-clock rule, anchor); `tb/srp_top/README.md:14`, `:497-596`; `tb/srp_stream_fsms/README.md:8`, `:218-232`; `sim_main.cpp:357-368`, `:778-789`; every PR-body figure re-measured (E1-E3, E9), with the bank totals failing (F2); `make check` (E11) | R488-2 | 9050c4bbd25556929a0f24fb98258bc98e3bcfbe |

## Integrity

`scripts/clone_integrity.sh` was run after all probes (`receipts/clone-integrity.txt`). It confirms the following:
- HEAD is `9050c4bb…` and the tree is `3bcc8532…`;
- `git write-tree` equals the tree;
- `git status --porcelain --ignored --untracked-files=all` is empty;
- `hash-object` equals the tree blob for all 562 files, and the exec bits equal the tree modes: **INTEGRITY OK**;
- there are 0 gitlinks. This repository has no submodules, so no required gitlink applies.

E4 was checked in a separate `git archive hdl` extraction. The clone was only read.

## Real limits

- I did not read the specification PDFs. The Table 10-4 and Table 4.3 readings rest on the repository's quotations and the reviewer's reading of the tables.
- Not run, per the review rules:
  - the processor-wide `run_suites.sh` bank;
  - the Yosys gate `syn/yosys/run.sh`;
  - the parent consumer set of 17 with the five adoption patches;
  - the builder and static banks;
  - Vivado OOC;
  - the 446-entry patch and exact-edit audit;
  - the D3 / notify mutant record-equality re-measurement (this review checked only base vs head pp_top equality, E10).

  For these, the only public evidence at this head is the author's REVIEW READY comment and the PR body. The published evidence directory covers round-1 head `5ab43bd9`.
- The reported OOC delta (−16 LUT, −3 FF) was not reproduced. The focused Yosys numbers (E12) come from a different tool and scope.
- Hosted `suites` had not concluded at the snapshot (E15).
- Physical calibration was NOT RUN. Field skips are not hardware proof, and nothing here is hardware evidence.
- The final current-dev candidate (source base `ead8036…`, live dev `28f9666f…`) has not been built. It is distinct from this source validation.

## Pending manager duties

- Carry F1 and F2 to the executor: the README record and the PR-body bank totals.
- Decide on the retained SUGGESTIONs and on R488-2-S1.
- Own hosted/act acceptance, including the in-progress `suites` jobs at this head.
- Own the parent consumer gate with the five patches, the OOC area gate and the mf48 calibration NOT RUN record.
- Build the merge-turn current-dev candidate against live dev `28f9666f…`.
- Apply the merge bar of two independent positive reviews.

R488-2 FINISHED
