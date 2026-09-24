[R304] NEGATIVE - exact head 49d23b20fcad15a3c03554476d8b8c9116b3b375

# R304-1 independent review: FPGA-gPTP issue #75 / PR #76

- Repository: Mister-M-alt/FPGA-gPTP. PR #76 is branch `75-slew-active` into `main`.
- Exact head `49d23b20fcad15a3c03554476d8b8c9116b3b375`, tree `804cd0dae42b46a2a85656f6e49781687ba671e6`. Source base `e5dcea6e351abff18a27a00f8e345f3251bdbd8f`.
- Reviewer: internal independent reviewer (R304), cleared context, isolated detached clone.
- Verdict: **NEGATIVE**. There are two open MINOR findings: F1 (Tests, Conformance) and F2 (Docs). The RTL and the microcode behave correctly on every probe I ran, including the new negative lifecycle probes. The findings concern missing test pins and stale documentation, not wrong hardware behaviour.

## 1. Reconstructed scope and authorities

1. The repository has no AGENTS.md or CONTRIBUTING.md. I read README.md, docs/README.md (truth order: RTL/microcode, then executable tests, then guides, then history), MANAGER.md, HDL_DEVELOPER.md, TEST_DEVELOPER.md, SOURCE_EVIDENCE.md and INTEGRATION.md.
2. Issue #75 body, the frozen acceptance:
   - (1) a documented one-bit, registered, `clk_i`-synchronous level named `phc_slew_active_o`;
   - (2) its timing contract: asserts on the policy slew decision, held for the whole affected interval including between pairs, clears when the policy correction completes while ordinary tracking continues, and defined behaviour on reset, asCapable loss, missing Sync, replacement step and return to grandmaster duty;
   - (3) tests: start and end on the policy's own decision, a step and ordinary tracking that do not assert it, **each defined edge case**, and tied-low and early-clear mutants that fail;
   - (4) INTEGRATION.md documents the port and contract;
   - (5) the parent consumer check runs on the parent #545 branch.
3. Issue comments: the executor assignment (base `e5dcea6`) and the review-ready note. No other maintainer scope decision is recorded on #75.
4. Linked authorities:
   - kebag-logic/milan-fpga #387 comment 5816509317: the CRF servo discards windows that overlap a slew and stays LOCKED. It states the premise "a slew lasts at most 0.5 s".
   - Parent #545: the consumer.
   - #387 comment 5794731090: the owner's step policy.
   - FPGA-gPTP #68 ruling 5798089412: the definition of link-up.
5. The full diff `e5dcea6..49d23b2` (13 files, +884/−481) and the single commit on top of the #74 merge.
6. Public evidence at kebag-logic/milan-fpga@941a6c7 `review-evidence/gptp75-r1`. All 36 manifest entries are under `author/`. Every file I downloaded matches its published SHA-256, and the source and ROM hashes in the packet match the head export (receipt `receipts/evidence_crosscheck.txt`). I found no manager bank receipt under that path, so I rely only on what I executed myself.

## 2. Findings

### F1 — MINOR — lenses: Tests, Conformance

- **Where:**
  - `tb/verilator/engine/sim_main.cpp:4730-4846` (`exercise_the_slew_level_contract`), especially `:4740` and `:4804`;
  - the unprotected RTL: `hdl/top/KL_gptp_engine.sv:876` (the `phc_slew_active_o &&` guard on the lapse hook) and `:940` (`phc_slew_left_r <= 2'd0` on PHC word 3).
- **Authority:** issue #75 acceptance 3 ("ordinary tracking that does not assert it, and each defined edge case"). The PR's own contract table in `docs/INTEGRATION.md:325-331` defines rows for missing Sync, asCapable loss and "Returning to slave duty — next consumed pair makes the policy decision".
- **Evidence:** the suite only exercises the lifecycle edges while the level is already active, or with an out-of-band first pair (`:4804` returns from mastership at +50 µs, which re-arms the qualifier regardless). The inactive direction is never pinned: an idle lapse or a return from mastership, followed by in-band ordinary tracking. Two reviewer mutants survive the shipped 1,532-check suite:
  - **R07** stops PHC word 3 from clearing the completion qualifier.
  - **R14** removes the `phc_slew_active_o &&` guard, so an idle flags lapse arms the qualifier.
- **These mutants are not equivalent.** A reviewer harness that adds only two negative cases passes on the unmodified head (1,555/1,555), and each mutant fails a named probe check:
  - probe A: idle Sync receipt timeout, then in-band pairs;
  - probe B: in-band first pair after mastership.
  - Receipts: `receipts/mutants/reviewer_06.json`, `reviewer_13.json`, `receipts/gapprobe/*`, `receipts/gapprobe_harness.diff`, `receipts/mutants_summary.txt`.
- **Impact:** a regression that raises the level during ordinary tracking after an idle Sync timeout, a grandmaster change or a return from mastership would pass the gate. The consumer would then discard CRF windows and hold its integrator with no slew in progress. The shipped behaviour is correct today, but the acceptance "each defined edge case" is only half pinned.
- **Required outcome:** add engine checks that, while the level is inactive:
  - (a) a Sync receipt timeout (and/or a grandmaster change) followed by in-band pairs leaves `phc_slew_active_o` low;
  - (b) a return from grandmaster duty whose first consumed pair is in-band leaves it low.
  - Add named mutation controls equivalent to R07 and R14 to `tb/verilator/engine/mutants.py`, each failing its named check.
- **Verification:** the engine suite passes on all three images, and `make -C tb/verilator/engine mutants` reports both new controls caught on their named checks. Reproduce with `scripts/make_gap_tree.py` and `scripts/probe_mutants.py` (see §5).

### F2 — MINOR — lens: Docs

- **Where:** `docs/SOURCE_EVIDENCE.md:10-24`. These are the ten `KL_gptp_engine.sv#L57/L99/L120/L156/L236/L339/L345/L381/L401/L428` anchors. SOURCE_EVIDENCE.md is unchanged by the PR.
- **Authority:** `docs/SOURCE_EVIDENCE.md:6` ("Line numbers describe the current branch layout.") and docs/README.md ("Source evidence binds claims to implementation"). The previous engine change (#31, `5c483d3`) refreshed these anchors, and all 11 engine anchors are exact at base `e5dcea6`.
- **Evidence:** the PR inserts engine lines at `:29-30`, `:107-109`, `:697-700`, `:758` and `:795-796`. As a result, 10 of 11 anchors now land on unrelated lines. Examples:
  - "Accepted-beat result face" `#L345` now points at `logic [3:0] txts_pend_type_r;` instead of `assign txts_ready_o ...` (now `:349`);
  - "Single clock domain" `#L57` points at a blank line (the module is now `:58`).
  - The full table is in `receipts/static_checks.txt`. `make docs` passes because it does not validate line anchors.
- **Impact:** the claim-to-source ledger that reviewers and integrators follow now sends them to the wrong code at this head.
- **Required outcome:** refresh the ten anchors to 58/100/124/160/240/343/349/385/405/432, or wherever the final layout places them. Optionally add a ledger row for the new slew-level claim.
- **Verification:** rerun `scripts/static_checks.sh` and see every anchor reported `EXACT`.

### Suggestions (do not affect the verdict)

- **S1 (RTL, Docs): ROM headroom is nearly gone.**
  - The shipping image is now 1,008/1,024 words (98.4%, up from 994 at base).
  - The generator now packs shared legs into the formerly reserved µPC 0..15 prefix (`hdl/ucode/gen_gptp_ucode.py:2059-2063`; `SERVO@0`, `FUTO@13`).
  - I verified this is safe: dispatch entries are ≥16 (`KL_gptp_engine.sv:524-541`), and reset parks the sequencer in `S_IDLE` without fetching (`KL_gptp_ucpu.sv:468-470`).
  - However, the PR body does not mention the prefix policy change or that 16 free words remain. `docs/MANAGER.md:42` ("931 words") was already stale at base.
  - Suggest recording the headroom and the prefix policy where the next microcode change will see them.
- **S2 (Docs): the lapse hook is undocumented for HDL contributors.** `docs/HDL_DEVELOPER.md` describes PHC words 2 and 3, but not the RTL-owned rule that restarts qualification when the publish flags word is written (`KL_gptp_engine.sv:873-878`). That rule couples state region 3 to the PHC qualifier.
- **S3 (Robustness): field behaviour is uncharacterised.** The ±100 ns completion band and the measured held intervals (3.069413 s and 1.916689 s for ±90 µs) come from simulation only. Parent #545 may want to count level assertions and time spent high, so field noise that keeps offsets outside ±100 ns becomes visible.

### Prior public review findings

After my own pass I read PR #76 and issue #75. They contain no review findings and no review objects. The only review-related items are two review-start notices. Nothing needs to be resolved or retained at this head.

## 3. Lens results

**Conformance (UNCLEAN, due to F1).**
- The port exists (`KL_gptp_engine.sv:107-109`). It is a registered output driven only by the synchronous `always_ff` (`:795`, `:921`, `:932`, `:941`). The harness checks that it never changes outside a rising edge.
- The decision is published through PHC word 2 before the affected addend (`gen_gptp_ucode.py:844-854` precede the SVRATE write at `:877`). The test "decision asserts before its affected rate" holds, and reviewer mutant R12 (level rises only with the rate) is caught.
- The level is held between pairs (the 250,000-cycle hold check).
- Completion needs two consecutive in-band consumed pairs and clears on the replacement addend edge. Mutants R13 and R18 are caught.
- A step never asserts the level, and a replacement step clears on its rate tail. Mutants R08 and R09 are caught.
- Ordinary tracking in [−100, +100] ns does not assert the level. Mutants R11, R15, R16 and R17 are caught.
- Reset clears it (R10 caught). Missing Sync and GM change restart qualification (R01, R03 and R04 caught). Mastership retires the correction with −integral (R05, R19 and R20 caught).
- INTEGRATION.md documents the port and every contract row, and matches the code. For example, the Follow_Up timeout leg writes no flags (`gen_gptp_ucode.py` `prog_leg_futo`), which matches the "retain level and rate" row.
- The duration differs from the parent decision's premise: 1.9–3.1 s measured versus "at most 0.5 s". Issue #75 sets no duration bound, and the PR documents that there is no watchdog (`INTEGRATION.md:337-339`). This goes to the manager (§7), not to this PR.
- Acceptance 3 is incomplete in the inactive direction (F1).

**RTL (CLEAN).**
- The state is two new registers, `phc_slew_active_o` and `phc_slew_left_r[1:0]`, both reset synchronously.
- Invariant: `left≠0 ⇒ active`. Word 2 sets active when nonzero; the hook only runs while active; words 1 and 3 and reset zero `left`.
- The `unique case (st_addr_w[1:0])` covers all four PHC words.
- Words 2 and 3 previously aliased to rate and step, but no base microcode wrote them (base generator uses only `RG_PHC|0` and `|1`).
- Region-4 read now returns `left`.
- Hook writes (region 3) and PHC writes (region 4) cannot share a cycle.
- The bench wrapper leaves the output open (`bench/arty/bench_arty_top.sv:297`); lint passes with `-Wno-PINCONNECTEMPTY`.
- Area comes from the published Vivado 2026.1 OOC reports, whose source hashes equal this head: 4,773→4,853 LUTs (+80), 3,646→3,652 FF (+6), LUTRAM 466, BRAM 1.5 and DSP 4 unchanged.
- WNS moved 2.249→1.773 ns, still met. The new worst path is inside the unchanged `u_timer` (`sweep_r`→`armed_r`), which points to implementation variance rather than new logic. The PR body omits this WNS delta; I note it without raising a finding.
- All four tracked ROM images regenerate byte-exact from the head generator.

**Robustness (CLEAN).**
- I walked through the full lifecycle, including concurrent edges (step while active, lapse while settling, mastership while active, warm reset with retained scratch). The head behaves correctly under all 22 reviewer probes plus the two gap probes.
- R02 (hook ignores asCapable) survives both harnesses, but I consider it reachable-equivalent:
  - Syncs are not consumed while the port is incapable (`prog_rx_sync` gate).
  - The 375 ms Sync receipt watch stays armed through asCapable loss (`_tmr_slot_dispatch` slot 4 is ungated, and only `prog_become` disarms it). It therefore clears sync-ok and restarts qualification before any recovery, which needs a later Pdelay exchange at 1 s cadence.
  - The asCapable term is defensive redundancy, not an untested contract.
- A documented indefinite hold under asCapable loss or cease is truthful, because the P+I rate is still applied.
- Limits on noise and duration are listed in §6.

**Tests (UNCLEAN, due to F1).**
- The engine suite passes: 1,532/1,532 on each of the three images.
- The ucpu suite passes: 768/768. Contract, lint (engine and bench), docs and diagram checks all pass.
- All 30 author mutants are caught. The three #75 controls fail their named checks.
- 19 of 22 reviewer mutants are caught. R02 is equivalent; R07 and R14 are real gaps (F1).
- The new checks are additive (sim_main.cpp +196/−0). The #75 mutation arms require their named FAIL line (`mutants.py:382-392`, the named-check gate for `slew:` arms).

**Docs (UNCLEAN, due to F2).**
- INTEGRATION.md, HDL_DEVELOPER.md and TEST_DEVELOPER.md are updated and consistent with the code.
- SOURCE_EVIDENCE anchors are stale (F2). S1 and S2 are suggestions.

## 4. Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | issue #75 body and comments; #387 c5816509317, c5794731090; #68 r5798089412; #545; PR body; INTEGRATION.md:150-357; engine/generator diff; engine suite run | R304-1 | 49d23b20fcad15a3c03554476d8b8c9116b3b375 |
| RTL | CLEAN | KL_gptp_engine.sv:29-30,107-109,697-700,758,795-796,869-948; KL_gptp_ucpu.sv:468-540; gen_gptp_ucode.py:404-410,806-885,1639-1670,2030-2082; 4 ROM images regenerated; published OOC util/timing reports; lint | R304-1 | 49d23b20fcad15a3c03554476d8b8c9116b3b375 |
| Robustness | CLEAN | lifecycle walk (step, lapse, GM change, mastership, asCapable, cease, warm reset); prog_rx_sync, prog_leg_srto/futo, prog_becgate, _tmr_slot_dispatch; 22 reviewer probes + 2 gap probes | R304-1 | 49d23b20fcad15a3c03554476d8b8c9116b3b375 |
| Tests | UNCLEAN (F1) | sim_main.cpp diff and slew harness; mutants.py; 30 author + 22 reviewer mutants; gap-probe harness; engine ×3 and ucpu suites; `make contract`, `make lint` | R304-1 | 49d23b20fcad15a3c03554476d8b8c9116b3b375 |
| Docs | UNCLEAN (F2) | INTEGRATION.md, HDL_DEVELOPER.md, TEST_DEVELOPER.md, SOURCE_EVIDENCE.md, MANAGER.md, README.md, drawio labels; `make docs` | R304-1 | 49d23b20fcad15a3c03554476d8b8c9116b3b375 |

## 5. Executed evidence (all at the exact head; receipts listed in MANIFEST.sha256)

The tool is the pinned simulator wrapper, reporting 5.050 (`receipts/tool_identity.txt`). All runs used a `git archive` export under `scratch/`; the reviewed clone was never built in.

- `receipts/engine_run.raw.txt`: `make -C tb/verilator/engine run`. 1,532/1,532 on the shipping, request-seeded and Sync-seeded images. The SLEW TRACE shows 6,138,826 and 3,833,378 cycles at 2 MHz (3.069413 s and 1.916689 s).
- `receipts/ucpu_run.raw.txt`: 768/768.
- `receipts/static_gates.raw.txt`: `make contract`, `make lint`, `make docs` (diagram check and self-tests), each with rc 0.
- `receipts/static_checks.txt` (`scripts/static_checks.sh`): four ROM images MATCH; SOURCE_EVIDENCE anchor table.
- `receipts/mutants_*`, `receipts/mutants/*.json` (`scripts/probe_mutants.py`): 30/30 author mutants caught, 19/22 reviewer mutants caught, plus the control.
- `receipts/gapprobe*` (`scripts/make_gap_tree.py` + `probe_mutants.py`): head 1,555/1,555; R07 and R14 caught by the probes; R02 not caught.
- `receipts/evidence_crosscheck.txt`: public evidence hashes and head source/ROM hashes.
- `receipts/clone_integrity.txt`: clone HEAD, tree and index tree equal the exact head. The worktree and index are clean, there are zero untracked or ignored files, index modes and blobs equal the HEAD tree, all 103 worktree blobs hash-equal HEAD, and the repository has no gitlinks.
- Hosted CI: the commit has 0 check runs, 0 statuses and 0 workflow runs (the repository has no workflows), so there was nothing to execute or skip. Hosted and act acceptance stay with the manager.

## 6. Real limits

- **Process deviation:** my first engine-suite invocation used the Makefile's `--build -j 0`, which permits up to the host's 16 compile jobs for one build. That exceeded the 8-job cap during that single build. Every later build was capped at 8 or fewer (the mutation pool had 8 workers with single-threaded builds; ucpu used `-j 8`).
- **Not run:**
  - the full `make` bank (parser, gaskets, tsngen, bench tag test), per the round's rules;
  - Vivado OOC (area and WNS come from the published reports, whose sources hash-equal this head);
  - any parent, PP or builder bank;
  - Docker or act.
- Physical calibration was NOT RUN, and nothing here is hardware proof. The ±100 ns band and the second-scale held intervals are simulation-derived at a 2 MHz model clock with clock-scaled gains.
- The R02 equivalence rests on code reading (1 s Pdelay cadence against the 375 ms Sync watch). It is not proven by an executed scenario.
- I did not examine the parent #545 branch. Consumer behaviour is out of this round.

## 7. Pending manager duties

- Close F1 and F2 on a new head, then run an exact-head re-review.
- At the merge turn, build the final current-dev candidate. Source validation here covered base `e5dcea6` only; live dev is `57456af96b3127b9d309a995bbbd35a6113ce52d`.
- Parent dev `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv` (sha256 `72e3d867…4bd4db`) instantiates `u_engine` by name and does not connect `.phc_slew_active_o`. The gitlink bump must land together with the #545 connection, and the parent's lint and consumer gates must run on that branch.
- Reconcile the #387 c5816509317 premise ("a slew lasts at most 0.5 s") with the measured 1.9–3.1 s level intervals before accepting #545. The CRF servo will hold its integrator for that long.
- Hosted and act acceptance, and the second independent review, stay with the manager.

R304-1 FINISHED
