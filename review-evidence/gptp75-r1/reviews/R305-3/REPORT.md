[R305] POSITIVE - exact head 3face0914efd9d5e71f36da7e30108cfe09c837d

# R305-3 independent external review: FPGA-gPTP issue #75 / PR #76, round 3

- Repository Mister-M-alt/FPGA-gPTP, PR #76 (`75-slew-active` into `main`).
- Exact head `3face0914efd9d5e71f36da7e30108cfe09c837d`, tree `c1f98ddfb81a5e4d06dfa436cc5162023b590314`. Parent `4a897e44` (round-2 head). Source base `e5dcea6e351abff18a27a00f8e345f3251bdbd8f`.
- Round-3 assignment (A275, issue #75 comment 5819725333). R304-2 F3 is the same finding as R305-2 F1 (MINOR, Tests). Required:
  - an engine check in which, while `phc_slew_active_o` is low, asCapable is lost and recovered through wire inputs, the first consumed pairs after recovery are in-band, and the level stays low with no edge;
  - a named mutation control equivalent to X01, failing that check;
  - a refresh of the `docs/MANAGER.md` area snapshot (R304-2 S1 = R305-2 S1).
  - Nothing else changes.
- Verdict: **POSITIVE**. No MINOR, MAJOR or BLOCKER finding is open, and all five lenses are clean. Two SUGGESTIONs follow; they do not affect the verdict.
- The verdict and ledger were frozen in `receipts/verdict_ledger_before_prior_findings.md` (2026-09-24T19:25:56Z), before the round-2 review reports were opened. Reconciliation with prior findings did not change the verdict.

## 1. Reconstruction

1. **Repository guidance.** There is no AGENTS.md or CONTRIBUTING.md. I read `README.md` and `docs/README.md`. The truth order is RTL and generated microcode, then executable tests, then role guides, then history. I also read `docs/MANAGER.md`, `docs/INTEGRATION.md:295-345`, `docs/HDL_DEVELOPER.md:120-137`, `docs/TEST_DEVELOPER.md:95-115` and `tb/verilator/engine/mutants.py:1-44`.
2. **Issue #75 body (frozen acceptance):**
   - (1) a one-bit, registered, `clk_i`-synchronous level `phc_slew_active_o`;
   - (2) a timing contract, with defined behaviour on reset, asCapable loss, missing Sync, replacement step and return to grandmaster duty;
   - (3) tests, including "each defined edge case", and tied-low and early-clear mutants that fail;
   - (4) the port and contract documented in INTEGRATION.md;
   - (5) the parent consumer check, which runs with parent #545.
3. **Maintainer and manager scope decisions on #75:** the A265 assignment (base `e5dcea6`), the A272 round-2 assignment, and the A275 round-3 assignment quoted above. There are no other scope decisions.
4. **Diff and history.** I reviewed `git diff e5dcea6..3face09` (17 files) and the round-3 commit `3face09`, which changes three files (+45/−2): `docs/MANAGER.md`, `tb/verilator/engine/mutants.py` and `tb/verilator/engine/sim_main.cpp`. `hdl/`, `syn/`, `bench/`, `scripts/`, the Makefiles and all four ROM images are byte-identical to the round-2 head (`git diff --quiet 4a897e4 HEAD -- …`).
5. **Public executable evidence** at kebag-logic/milan-fpga `26975a0c702be697be3693529940b4c536484107/review-evidence/gptp75-r1`:
   - I downloaded 26 files. Each matches its `MANIFEST.json` published SHA-256.
   - `author-r3/commit.json` names this head and tree.
   - All 104 entries of `author-r3/candidate-sources.sha256` match the exact-head clone.
   - `author-r3/reviewer-scripts-after.sha256` lists my round-2 scripts at the same hashes as my copies (`receipts/evidence_crosscheck.txt`).
   - The issue and PR carry no separate manager evidence comments beyond the assignments and review-start notices. The evidence tree contains author and review packets, and I did not identify a separately labelled manager bank receipt in it. I therefore take the statement that the manager's static, builder and native banks passed as the manager's own, and did not verify it here.
6. **Disclosure.** While reconstructing, the PR comment listing exposed the round-1 R304-1 report and the opening of the round-1 R305-1 report before my own pass. Both are superseded by rounds 2 and 3. I opened the round-2 reports (R304-2, R305-2) only after the freeze noted in the header.
7. **Script names.** The brief names `make_gap_tree_r2.py` and `probe_mutants_r2.py`. The published hash list shows these are the other review lane's round-2 scripts. My own round-2 scripts are `make_probe_tree_r2.py` (probe C) and `probe_r2.py` (R21/R22), run through `probe_mutants.py`. I re-ran mine with unchanged bytes (hash-identical to the published R305-2 copies). My R21 is byte-identical to X01 as the finding describes it, and to the shipped control (`receipts/control_equivalence.txt`). I did not run the other lane's scripts.

## 2. Findings

No MINOR, MAJOR or BLOCKER finding is open.

### S1 - SUGGESTION - Docs - the test guide's inactive-direction bullets omit the new asCapable pin

- **Where:** `docs/TEST_DEVELOPER.md:105-107`.
- **What:** the bullets list inactive-direction checks for idle timeouts, GM changes and mastership returns, and the matching controls. The round-3 check (`sim_main.cpp:4766-4791`) and its control (`mutants.py:101-106`) are covered only by the generic "lost capability" bullet at `:103`.
- **Why it is only a suggestion:** the assignment says "Nothing else changes", and the list is a summary, not a claimed inventory.
- **Suggestion:** add "and asCapable loss and recovery" to `:105` the next time this guide is edited.

### S2 - SUGGESTION - Robustness - field behaviour is uncharacterised (carried)

- This is the same observation as R304-1 S3 and R304-2 S2.
- The ±100 ns band and the measured held intervals (6,138,826 and 3,833,378 cycles at 2 MHz, i.e. 3.069413 s and 1.916689 s) are simulation-derived. Parent #545 may want to count assertions and time spent high.

## 3. Lens results (artifact-specific evidence)

### Conformance: CLEAN

- **Acceptance (3), "each defined edge case", is now pinned in both directions for all five named edges:**
  - reset: `sim_main.cpp:4733-4734`, `:4873-4885`;
  - missing Sync: active at `:4810-4830`, inactive at `:4743-4754`;
  - GM change: active at `:4832-4837`, inactive at `:4756-4764`;
  - replacement and link-up step: `:4738`, `:4805-4806`, `:4882`;
  - mastership and return: `:4839-4857`;
  - asCapable loss: active at `:4858-4871`, and **inactive at `:4766-4791` (new)**.
- **What the new block does:**
  - it drives Pdelay `PD_FAR` on the wire until `pub_flags_o` asCapable falls (`:4773-4775`), and holds the port incapable for a further 100 ms (`:4776-4780`);
  - it restores `PD_NORMAL` until asCapable rises (`:4781-4783`) and re-announces the same GM (`:4784`);
  - it then consumes two in-band pairs: 0 ns as the link-up pair, then +100 ns at the inclusive band edge (`:4789-4790`).
- **What the new block checks:**
  - the level is low at every step;
  - there is no level edge (`slew_edges` count, `:4779`, `:4787`, `:4791`);
  - there is no rate write during the lapse or recovery (`:4780`, `:4788`);
  - each pair writes exactly one PI rate, and the addend matches the PI mirror (`slew_probe`, `:4704-4711`).
- This matches the A275 required outcome word for word, and uses public wire inputs only.
- **The contract is unchanged.** `docs/INTEGRATION.md:301` ("Tracking inside the band without an active correction | Stay inactive") and `:325` (asCapable loss) remain consistent with `KL_gptp_engine.sv:873-879`.
- **Duration.** The measured 1.9–3.1 s intervals, set against the parent decision's 0.5 s premise, are a manager and #545 matter, as in prior rounds. The issue sets no duration bound.

### RTL: CLEAN

- There is no RTL, generator or ROM change in round 3 (`git diff 4a897e4 HEAD` covers only the three files above).
- I re-read the lapse hook (`KL_gptp_engine.sv:873-879`) and the PHC words (`:918-943`). The invariant `phc_slew_left_r != 0 ⇒ phc_slew_active_o` holds:
  - word 2 sets active whenever it loads a nonzero value;
  - the hook runs only while active;
  - words 1 and 3 and reset zero the qualifier.
- The only microcode reader of the qualifier is the slew leg (`gen_gptp_ucode.py:844`; the other `RG_PHC` accesses are writes, at `:827`, `:854`, `:877`, `:1649`).
- All four tracked ROM images regenerate byte-exact (`receipts/rom_regen.txt`: 1,008/1,024 words).
- Engine and bench lint are clean with the pinned simulator (`receipts/static_gates.txt`).

### Robustness: CLEAN

- **The inactive asCapable path is correct and now observable.** Three reviewer mutants of that path:
  - **R31**: an asCapable rise arms qualification while inactive;
  - **R32**: an inactive asCapable loss raises the level directly;
  - **R33**: an inactive asCapable loss loads one pair.
- **Results:**
  - R31 and R32 are caught by the shipped harness (`receipts/r3_mutants_head_harness.txt`).
  - Both survive the round-2 harness (`receipts/r3_mutants_round2_harness.txt`). The new block is therefore load-bearing beyond X01: it pins the recovery edge as well as the loss edge.
  - R33 survives, as I predicted from code reading (`receipts/r3_mutant_r33_head_harness.txt`). With the level low, a qualifier of 1 is unobservable:
    - an in-band pair decrements it to 0 and publishes 0, so the level does not rise;
    - an outside-band pair reloads to 2 regardless;
    - step and mastership words clear it;
    - no other microcode reads it.
  - This also covers the one-pair-arming equivalence that the PR body attributes to the other lane's X03. I reached it with my own mutant.
- **R02** (the hook ignores asCapable) still survives, as recorded at `mutants.py:38-44`. The reachability argument is unchanged by round 3:
  - Syncs are not consumed while the port is incapable;
  - the 375 ms receipt watch clears sync-ok before a 1 s-cadence Pdelay recovery;
  - it is still a code-reading argument, not an executed proof.

### Tests: CLEAN

- **Engine suite:** 1,613/1,613 on each of the shipping, request-seeded and Sync-seeded images, rc 0 (`receipts/engine_run.log`).
  - Round 2 had 1,586. The +27 checks are exactly the new block: 13 direct `expect`s plus 2 × 7 `slew_probe` checks.
  - The change is additive (sim_main.cpp +27/−0).
- **PR mutation set:** 33/33 caught (`receipts/pr_mutants_00_17.txt`, `receipts/pr_mutants_17_33.txt`). All six `slew:` controls pass the named-check rule.
  - The new "slew idle asCapable loss arms qualification" fails first with `FAIL slew: in-band pair after asCapable recovery stays inactive got …1 exp …0`.
  - Its pattern occurs exactly once in the head engine.
  - Its pattern and replacement equal my R21 (plus the trailing newline).
  - Its named check occurs once and is not a substring of another check name (`receipts/control_equivalence.txt`).
- **Round-2 reviewer mutants** (unchanged `probe_r2.py`) on the shipped harness:
  - **R21 (≡ X01): CAUGHT** at `slew: in-band pair after asCapable recovery stays inactive`. It survived at the round-2 head.
  - R22: CAUGHT (`receipts/r2_mutants_head_harness.txt`).
- **Round-1 reviewer mutants R01–R20** (unchanged `probe_mutants.py`): 19/20 caught; R02 survives, as recorded (`receipts/reviewer_mutants_head_harness.txt`). This is identical to round 2.
- **Probe C** (unchanged `make_probe_tree_r2.py`):
  - At this head (HEAD rebound by `run_probe_c_at_head.py`, script bytes unchanged): the control passes 1,633/1,633, R21 and R22 are caught, and R01/R06 are caught with R02 surviving (`receipts/probe_c_at_head.txt`, `receipts/r305_probe_c_harness_at_head.diff`).
  - Fully unchanged, at its pinned round-2 head: it reproduces round 2 (1,606/1,606; R21 and R22 caught) (`receipts/probe_c_round2_head_repro.txt`).
- The shipped serial `make -C tb/verilator/engine mutants` was not run by me: it takes over 20 minutes, beyond my foreground limit. My driver calls the tree's own `stage`, `build`, `generate_image` and `run_harness` and `tb/mutation_verdict.py`, and applies the same named-check rule. The author's `author-r3/gates.json` records that gate at rc 0 (1,320 s).

### Docs: CLEAN

- **`docs/MANAGER.md:35-52`** matches the Vivado 2026.1 reports:
  - complete engine: 4,853 LUTs, 3,652 registers, 1.5 BRAM tiles, 4 DSPs, WNS +1.773 ns (`author-r3/engine_util.rpt`, `engine_timing.rpt`, dated 2026-09-24 20:53–20:54);
  - baseline: 4,773 LUTs, 3,646 registers, WNS +2.249 ns (`author/baseline-engine_*.rpt`); +80 LUTs and +6 registers are correct;
  - memory LUTs 466 in both;
  - standalone microCPU: 1,643 LUTs, 733 registers, WNS +1.941 ns, re-measured on 2026-09-24 20:52 (`author-r3/ucpu_*.rpt`). The new date line therefore truthfully covers both rows.
  - Part `xc7a100tfgg484-2` with a 10 ns clock (`syn/ooc/engine_ooc.tcl:18,20`).
  - The linked tree `4999d8d6…/gptp75-r1/author` exists and contains the baseline and candidate reports.
- **Gates:**
  - `make docs` passes: the docs checker and self-test, the diagram check and self-test, and source evidence "20 exact, 0 findings" with its 7-arm self-test.
  - My anchor review script shows all 20 anchors on their claimed constructs (`receipts/static_anchor_review.txt`).
  - My checker negative controls pass (`receipts/checker_controls.txt`).
- S1 is a suggestion only.

## 4. Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #75 body; A265/A272/A275 comments; INTEGRATION.md:295-345; KL_gptp_engine.sv:873-879, 918-943; sim_main.cpp:4730-4888 (new :4766-4791); engine suite ×3 | R305-3 | 3face0914efd9d5e71f36da7e30108cfe09c837d |
| RTL | CLEAN | hdl/ byte-identical to 4a897e44; lapse hook and PHC words re-read; qualifier readers in gen_gptp_ucode.py; 4 ROM images regenerated byte-exact; engine and bench lint | R305-3 | 3face0914efd9d5e71f36da7e30108cfe09c837d |
| Robustness | CLEAN | inactive asCapable loss/recovery path; R31/R32 (caught at head, survive round-2 harness); R33 predicted-equivalent survives; R02 note mutants.py:38-44 | R305-3 | 3face0914efd9d5e71f36da7e30108cfe09c837d |
| Tests | CLEAN | sim_main.cpp:4766-4791; mutants.py:101-106; 33/33 PR mutants with named-check rule; R01-R20; R21/R22 (R21 ≡ X01 caught); probe C at head and at round-2 head; control equivalence | R305-3 | 3face0914efd9d5e71f36da7e30108cfe09c837d |
| Docs | CLEAN (S1 SUGGESTION) | MANAGER.md:29-54 against published Vivado reports; TEST_DEVELOPER.md:95-115; HDL_DEVELOPER.md:120-137; `make docs`; 20 anchors; checker controls | R305-3 | 3face0914efd9d5e71f36da7e30108cfe09c837d |

## 5. Reconciliation with prior public review findings (read after the freeze)

| Finding | Status at this head | Basis |
|---|---|---|
| R305-2 F1 (MINOR; Tests, Conformance): inactive asCapable loss/recovery unpinned; R21 survives | **Resolved as specified** | `sim_main.cpp:4766-4791`; `mutants.py:101-106`, caught on its named check. R21 is caught by the unchanged `probe_r2.py` on the shipped harness. Probe C still passes at head, and R21 is caught there too. |
| R304-2 F3 (MINOR; Tests, Conformance): same as R305-2 F1; X01 survives | **Resolved as specified** | The shipped control equals X01 as the finding states it, byte-for-byte equal to R21, and is caught at the named check. I did not run the other lane's scripts. |
| R305-2 S1 / R304-2 S1 (SUGGESTION): MANAGER area snapshot | **Taken** | `docs/MANAGER.md:35-52`, verified against the reports (§3 Docs) |
| R304-2 S2 / R304-1 S3 (SUGGESTION): field characterisation | Agreed; carried | S2 above |
| R304-2 X03 (idle one-pair arming) equivalence | Agreed on my own evidence | R33 survives, and the code-reading argument is in §3 Robustness |
| R305-1 F1/F2, R304-1 F1/F2 (MINOR) | Remain resolved | They were resolved at round 2. Round 3 does not touch those checks, anchors or controls: 20 anchors exact, and the R01/R06 controls (≡ R304-1 R14/R07) are caught. |
| R305-1 S1/S2, R304-1 S1/S2 (SUGGESTION) | Remain taken | `docs/MANAGER.md:56-80`, `mutants.py:38-44` and `HDL_DEVELOPER.md:125-137` are unchanged |

There are no GitHub review objects or inline review comments on PR #76.

## 6. Executed evidence

All runs used `git archive` exports of the exact head (or probe copies) under `scratch/`. Nothing was built in the reviewed clone. The simulator is the pinned wrapper, whose identity matches round 2 (`receipts/tool_identity.txt`): wrapper `905795b9…`, Verilator 5.050, `verilator_bin` `44898b22…`. Builds used at most 8 compile jobs; mutation pools ran 4 workers × 2 build threads.

| Receipt | Content |
|---|---|
| `receipts/engine_run.log` | engine suite ×3 images, 1,613/1,613 each, rc 0, SLEW TRACE intervals |
| `receipts/pr_mutants_00_17.txt`, `receipts/pr_mutants_17_33.txt` | 33/33 PR mutants caught, including 6/6 slew named checks |
| `receipts/r2_mutants_head_harness.txt` | unchanged `probe_r2.py`: R21 (≡ X01) and R22 caught by the shipped harness |
| `receipts/reviewer_mutants_head_harness.txt` | unchanged `probe_mutants.py` R01–R20: 19/20 (R02 recorded) |
| `receipts/probe_c_at_head.txt`, `receipts/r305_probe_c_harness_at_head.diff` | probe C at head: control 1,633 PASS; R21, R22, R01 and R06 caught |
| `receipts/probe_c_round2_head_repro.txt` | fully unchanged probe C at its pinned round-2 head reproduces round 2 |
| `receipts/r3_mutants_head_harness.txt`, `receipts/r3_mutants_round2_harness.txt`, `receipts/r3_mutant_r33_head_harness.txt` | R31/R32 caught at head and surviving the round-2 harness; R33 survives (predicted equivalent) |
| `receipts/control_equivalence.txt` | shipped control ≡ R21; pattern uniqueness; named-check uniqueness |
| `receipts/static_gates.txt` | `make docs`, `make contract`, `make lint` (engine and bench), each rc 0 |
| `receipts/rom_regen.txt` | 4 ROM images byte-exact |
| `receipts/static_anchor_review.txt`, `receipts/checker_controls.txt` | anchor constructs; checker negative controls PASS |
| `receipts/evidence_crosscheck.txt` | public evidence hashes, head source hashes, script identity, area figures |
| `receipts/hosted_evidence.txt` | hosted state: 0 check runs, 0 statuses, 0 workflow runs, 0 workflows. No hosted job executed or was skipped; mergeable against `main` = `e5dcea6` |
| `receipts/clone_integrity.txt` | HEAD, tree and index exact; 104 blobs and modes exact; 0 untracked or ignored files; fsck clean; 0 gitlinks, and none required (no `.gitmodules`) |
| `receipts/verdict_ledger_before_prior_findings.md` | the verdict and ledger frozen before prior reports were read |

Scripts are in `scripts/`:
- round-2 bytes, unchanged: `probe_mutants.py`, `probe_r2.py`, `make_probe_tree_r2.py`, `run_probe_tree_at_head.py`, `static_checks.sh`, `checker_controls.py`;
- new this round: `run_probe_c_at_head.py`, `probe_r3.py`.

## 7. Real limits

- **Simulation only.**
  - Not rerun by me, because their sources and inputs are unchanged since round 2 and the round only touches engine test code and docs: the microCPU, parser, gasket, tsngen and bench-tag suites. The author's round-3 gates record them at rc 0.
  - Not run: the shipped serial engine mutation gate. My equivalent driver ran all 33.
  - Not run, per the brief: the full parent/PP/gPTP/Yosys/builder banks, Docker/act, and OOC synthesis. Area and WNS come from the published reports.
- **Physical calibration was NOT RUN.** Field skips are not hardware proof. The harness uses ideal timestamps at a 2 MHz model clock.
- **R02 and R33 equivalence** rests on code-reading reachability arguments, supported by survival under the harness. It is not a formal proof.
- **Parent consumer:** I did not examine the #545 `KL_gptp_shadow` connection or the CRF-servo consumer.
- **Manager banks:** I could not locate a separately labelled manager bank receipt in the published evidence tree, so the manager's bank result is taken as stated.
- **Candidate:** source validation at this head is distinct from the final current-dev candidate (source base `e5dcea6e`, live dev `573f0052a0e4412e81f0845438fcec2086ce5d55`), which the manager builds at the merge turn.

## 8. Pending manager duties

- Obtain the second independent exact-head review.
- Build and gate the merge-turn current-dev candidate, and own hosted/act acceptance. The repository has no workflows, so no hosted job exists for this head.
- Explicitly accept or override the author-chosen ±100 ns / two-pair completion tolerance.
- In #545, reconcile the 0.5 s slew premise with the measured 1.9–3.1 s intervals and the documented indefinite hold under asCapable loss or cease.
- In #545, connect `KL_gptp_shadow.u_engine.phc_slew_active_o` through to the CRF servo, validate the mastership-retire addend against the parent PHC, and run the parent consumer gates on that branch. Land the gitlink bump together with that connection.

R305-3 FINISHED
