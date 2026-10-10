[R559] NEGATIVE - exact head d1b18b3fa0b476a9b534c88466b163e15f469004

# R559-6 external review: issue #696 / PR #706

- Head `d1b18b3fa0b476a9b534c88466b163e15f469004`, tree `32c6c80f62e026070ca11b8e3dba8178667b0e13`, detached clean clone.
- Source base `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`. The lane-net delta is measured against the merged dev parent `e8454e27` (17 files); round 6 is `6de3904e..d1b18b3f` (12 files).
- Scope comes from the issue body and the public assignment and rulings on #696: 6076750392, 6076940309, 6079087547, 6079463350, 6080332335, 6089712293, 6093171536 and the round-6 assignment 6097504752.
- **Verdict: NEGATIVE.** The RTL is correct. I proved the round-6 fold guarantees exhaustively, and RTL, Robustness and the area records are clean.
- Two MINOR findings are open. R559-6-F1 is under Tests and Conformance. R559-6-F2 is under Tests and Docs.
  - Both are about evidence for the new first-draw property, not about the logic.
  - One check is named for a property the head does not have.
  - The universal guarantees rest on one sample per carry run, so planted fold-constant regressions that break them pass all 177 checks.
- One RESIDUE (wording) and three optional suggestions are recorded below.

## 1. Reconstruction

**Frozen acceptance (issue body):**
1. Each of M1-M8 is either conformed, with a suite check and a planted defect, or justified by clause.
2. M4 is fixed in RTL first, with a datapath check that different MACs draw different intervals.
3. The OOC area and one shipping route stay within budget, and the records are re-recorded through the recipe.
4. Bench interop is assigned to a post-merge bench lane (assignment item 6).

**Rulings:**
- M8 counting is withdrawn (6076940309).
- The +60 LUT / +60 FF ceiling applies to `g_maap.maap_engine` (6079087547).
- The differential stimulus varies the MAC (6079463350).
- Documentation consistency fixes are authorized (6080332335).
- Merge dev and re-measure, with no floor exception (6089712293).

**Round-6 assignment (6097504752), option 1:**
- The first Begin! offset and the first probe interval depend on the full 32-bit seed through at least one generator step.
- A named check grades the first Begin! range across equally timed stations: "Different MACs (adjacent ones, and ones differing only in bits 16..31) must give non-identical, non-overlapping first blocks, and different clocks must give different first offsets".
- p7 joins the campaign.
- Re-measure and record only if every gate passes.
- Docs describe the first draw exactly.

**Round-6 RTL (`KL_maap.sv:146-178, 200-203, 334-339`):**
- `lfsr_step()` is factored out.
- `seed_next_w = lfsr_step(enable_seed_w)`.
- The first-Begin! offset is `rand_offset(offset_fold(seed_next_w), count_i)`, through 16 parity rows `OFFSET_FOLD_C`.
- Every probe interval is `518 + probe_fold(lfsr_next_w)`, through 6 parity rows `PROBE_FOLD_C`. At the first PROBE, on the cycle after enable, `lfsr_r` holds the seed, so this is the fold of the stepped seed.
- Later Begin! draws `lfsr_next_w[15:0]`, and Restart! / PortOperational! draw `lfsr_r[15:0]`, both unchanged.
- No register is added: the folds are functions of existing wires.

## 2. Findings

### R559-6-F1 - MINOR - Tests, Conformance - `tb/verilator/maap/sim_main.cpp:1073` (with `:1044-1046`, `mutants.py:71`); issue #696 assignment 6097504752 item 2 - the "bits 16..31" check is named for a property the head does not have, and the round-6 criterion it answers is unmet and needs a recorded narrowing

**Authority:**
- Assignment 6097504752 item 2: MACs "differing only in bits 16..31 must give non-identical, non-overlapping first blocks".
- AGENTS.md section 4: wrong or contradictory acceptance needs a public change request, not a private interpretation.
- AGENTS.md section 6 (Tests): each test can fail for the defect it claims to detect.

**Evidence at this head.** I ran my own first-claim harness (`scripts/first_offsets.cpp`) on the unmodified head RTL. Stations were reset and enabled on the same cycles at clock 0, count 8:

| MAC pair (differ only in bits 16..31) | First offsets | 8-address blocks | Receipt |
|---|---|---|---|
| `02:00:00:00:12:34` / `02:00:90:00:12:34` | 0xa074 / 0xa075 | overlap | `receipts/xval.log` |
| `02:00:01:80:12:34` / `02:00:ed:6f:12:34` | 0x0074 / 0x0074 | **identical** | `receipts/identical_pair.log` |

- A model of the RTL first draw reproduces the head harness on 202 stations (`receipts/xval.log`). On that model:
  - 513 first offsets are shared by more than one high half (`receipts/identical_pair.log`).
  - 14 of 65,535 high halves overlap one fixed MAC (`receipts/high_half_overlap.log`).
- This cannot be fixed:
  - 65,536 high halves map onto at most 65,017 offsets, so no count-8 draw makes all such pairs non-identical, let alone non-overlapping.
  - The author's open risk and the PR body say so: "no 16-bit draw can separate every pair".
- The check at `:1073`, "M4 B.3.6.1 MACs differing in bits 16..31 claim disjoint first blocks", still asserts that property. It passes because it samples 136 power-of-two-apart pairs (i ≥ 16) and three fixed pairs (`:1044-1046`).
  - The PR body and the REVIEW READY cite it as "139 pairs differing only in bits 16..31".
  - No published decision narrows the round-6 criterion to the power-of-two pairs that the RTL actually guarantees. The REVIEW READY lists the limit as an open risk, not as a requested change.

**Impact:**
- The suite's named evidence states a separation guarantee that the head violates for concrete MAC pairs, including M4's own failure mode: an identical first block under identical timing.
- A cold reader of the check list would conclude that the round-6 criterion is met as written.

**Required outcome:**
- Each first-draw check is named for what it establishes. For example, "MACs 2^i apart (i ≥ 16) claim disjoint first blocks", with the fixed pairs named as fixed pairs. Mutant anchors follow the rename.
- The manager publicly records the narrowed round-6 criterion: disjoint for seeds a power of two apart, and different words for any bits-16..31 difference. The other option is a different achievable criterion.

**Verification:**
- `grep` of the check names in `sim_main.cpp` and `mutants.py`.
- Campaign rc 0 with the renamed anchors.
- A link to the manager's narrowing comment.

### R559-6-F2 - MINOR - Tests, Docs - `docs/design/MAAP_FABRIC.md:112-116`, `hdl/ieee1722/maap/doc/KL_maap/KL_maap.md:5`, `hdl/ieee1722/maap/KL_maap.sv:156-162`; checks `sim_main.cpp:1072-1074` - the documented universal first-draw guarantees have no check that can fail when they are lost

**Authority:**
- AGENTS.md section 6 Tests: "Each new test can fail for the defect it claims to detect".
- AGENTS.md section 6 Docs: "The PR and Issue contain enough evidence for another cold reviewer".

**Evidence:**
- The docs claim, for every seed:
  - two seeds a power of two apart, with any carry, claim disjoint first blocks of up to 8, "through the pool fold and the clip";
  - seed bits 16..31 map one-to-one onto the offset word.
- At the head both claims are true. My exhaustive check (`scripts/fold_proof.py`, `receipts/fold_proof.log`, rc 0) reads the constants from the RTL and confirms them:
  - all 528 carry runs × all 65,536 words × counts 1..8 are disjoint;
  - all 528 runs give different probe draws;
  - bits 16..31 are a bijection;
  - the 22 rows have rank 22.
- No artifact in the repository or the public evidence establishes these claims. The suite draws one random seed per carry run (`sim_main.cpp:1050-1063`, described at `MAAP_FABRIC.md:254-255`).
- Two planted fold-constant regressions show that the checks cannot fail when the claims are lost:
  - **q3** drops one bit of offset row 0 (`32'h0000_0081` to `32'h0000_0080`). The bijection breaks: 32,768 distinct words, with kernel `0x9000`. MACs `02:00:00:00:12:34` and `02:00:90:00:12:34` then claim the identical block 0xa074. The unit harness reports **177 checks, 0 failures** (`receipts/probes.log`, `receipts/q3_pair.log`, `receipts/xval.log`).
  - **q9** drops one bit of offset row 6 (`32'h8008_0040` to `32'h8000_0040`). Run 18..18 overlaps. MACs `02:00:17:a1:47:bb` and `02:00:17:a5:47:bb`, 2^18 apart, claim 0xfdf8 / 0xfdf3, overlapping blocks at the clip, where the head gives 0xfdf8 / 0xfdb3. The unit harness reports **177 checks, 0 failures** (`receipts/q9_pair.log`), although the check "M4 B.3.6.1 MACs 2^i apart claim disjoint first blocks" is named for exactly this.
  - A model search (`receipts/row_flip_search.log`) finds that 109 of the 512 single-bit row flips break a documented universal claim while every sampled suite pair still passes.

**Impact:**
- The central round-6 guarantee is protected only by sampling.
- A later edit of the fold constants, or of the pool mapping, can silently reintroduce first-claim collisions between equally timed stations.
- A cold reviewer cannot confirm the universal statements from public state without writing a proof.

**Required outcome:** one of the following.
- An executable check in the default MAAP target establishes the universal claims for the RTL's actual constants and fails for q3 and for q9. It may be exhaustive over carry runs and words through the pool fold and clip, plus the bits-16..31 bijection, at RTL or model level, provided the model is tied to the RTL.
- Or the universal statements at the three cited places are narrowed to what the suite establishes.

**Verification:**
- Apply q3 (anchor in `scripts/probes.py`) and q9 (the `32'h8008_0040` replacement above). Each must fail a named check.
- The default MAAP target stays rc 0.

### R559-6-R1 - RESIDUE - Docs - `docs/design/MAAP_FABRIC.md:116`; PR #706 body, "What the folds guarantee", third bullet - "always draw different words" omits that the pool fold can still give equal blocks

- **Evidence:** the head pair `02:00:01:80:12:34` / `02:00:ed:6f:12:34` draws different words but claims the identical block 0x0074 (`receipts/identical_pair.log`). The sentence is true but invites the stronger reading.
- **Exact fix:** append to both sentences: "; the pool fold can still map two such words onto one block, so their first blocks can coincide or overlap like any pair that is not a power of two apart."
- This is wording only. It changes no figure, check or claim.

### Suggestions (optional; no lens effect)

- **R559-6-S1 - Tests - `KL_maap.sv:202`.** Probe q1 replaces `probe_fold(lfsr_next_w)` with `probe_fold(lfsr_r)`, so the first probe interval comes from the unstepped seed. It escapes (177/0). The author disclosed this. A golden first-interval value for one seed would pin the generator step that the round-6 assignment asks for.
- **R559-6-S2 - Robustness, Tests - `KL_maap.sv:193-198, 337-339`.** Probe q8 replaces `count_i` in the Begin! draw with `8'd8` and escapes (177/0). No check drives a random draw into the pool-clip region with a count other than 8, and the M7 test (`sim_main.cpp:825-842`) reaches the clip only by chance. This gap predates #696, so it is a candidate for its own Issue.
- **R559-6-S3 - Tests.** Probe q5 makes every Begin! use the first-draw fold and escapes (177/0). The documented "later Begin! events draw the running generator's next low 16 bits" (`MAAP_FABRIC.md:110`) is not graded. Behaviour stays acceptable because the clock moves between enables.

## 3. Prior public findings, explicitly resolved or retained at this head

I read these only after my own pass.

| Finding | Status at `d1b18b3f` | Evidence |
|---|---|---|
| R558-6-F1 (MINOR; Conformance, RTL, Robustness, Tests): raw-seed first draw, p7 escapes | **Resolved** for its stated verification. The first offset and the first interval now come from `lfsr_step(seed)` folds. p7 is caught in unit and datapath (`m4_first_offset_ignores_seed`, `m4_datapath_first_offset_ignores_seed`, campaign 59/59). R558-6's four pairs are in the suite's fixed pairs and pass. The PR body's p7 copy fails the four named checks. The generalization to all bits-16..31 pairs cannot be met and is carried as **R559-6-F1** | `receipts/campaign.log`, `receipts/p7_repro.log`, `receipts/fold_proof.log` |
| R558-6-R1, R558-4-R1 (RESIDUE): stale PR-body head | **Resolved**. The body names `d1b18b3f` and lists round 6 | PR body as read |
| R558-5-R1 (RESIDUE): "records unchanged" lines | **Retained** at `AREA_BUDGET.md:362,379`, `MARK_II_AREA_PLAN.md:666`, on the residue checklist | file text at head |
| R558-2-R1 / R559-2-R1 (RESIDUE): baseline sentences | **Retained** at `MARK_II_AREA_PLAN.md:66-67`, `:317`, `:1007` | file text at head |
| R558-5-F1 (MINOR, Docs) | Still resolved. `AREA_BUDGET.md:371` names #696's 50,013-LUT route | file text |
| R558-3-F1 = R559-3-F1 (BLOCKER, `integration.mk`) | Still resolved locally. `integration.mk` is unchanged in round 6. The datapath build and run give 5/0, and the five datapath campaign rows are `[ok]`. The hosted Verilator shards at this head were still running when read | `receipts/integration.log`, `receipts/hosted_checks_summary.txt` |
| R558-1-F1, R559-1-F1/F2/F3 (MINOR) | Still resolved. The MAAP area lines give 441/445/490 with correct arithmetic. The Mark II inventory equals the record (66/66). The M5 loss check and its plant are in the campaign | `receipts/plan_vs_record.log`, `receipts/campaign.log` |
| R558-6-S1/S2, R559-5-S1, R558-3-S2, R558-4-S1/S2, R559-4-S1/S2, R559-1-S1..S4 (SUGGESTION) | Retained, optional | sources unchanged where cited |

## 4. Per-lens results

```text
[R559] PASS RTL - hdl/ieee1722/maap/KL_maap.sv:141-178,193-203,330-339,380-386 at d1b18b3f - the generator step, the 16- and 6-bit folds (widths, row slicing, rank 22), the first-Begin! selection on rng_seeded_r, the first-PROBE timing (lfsr_r = seed on the cycle after enable, so probe_fold(lfsr_next_w) folds the stepped seed), unchanged Restart!/later-Begin! paths and no added register; a model built from these lines equals the RTL on 202 stations; single-module synthesis rc 0; lint 90 <= 90
```
```text
[R559] PASS Robustness - KL_maap.sv:150-151,337-339,383-386,451-459; probes q4/q6 CAUGHT, q5/q8 (S2, S3) - zero-sum fallback, re-seed per Begin!, provisioning-seed precedence at first enable, count 1..8 through the clip (fold_proof), link-return and restart draws unchanged; pre-existing count>8 clip gap recorded as S2
```
```text
[R559] UNCLEAN Conformance - issue #696 assignment 6097504752 item 2; sim_main.cpp:1073 - R559-6-F1 (criterion unmet as written, no recorded narrowing). Otherwise applied and clean: KL_maap.sv first draw against B.3.4 NOTE / B.3.6.1 and the option-1 text (full 32-bit seed, one generator step, both first draws), M1-M8 unchanged since R559-5; datapath first offsets 0x7029 / 0x9821 (adjacent MACs) and 0xf229 / 0xf1cd (two clocks)
```
```text
[R559] UNCLEAN Tests - sim_main.cpp:1031-1076, sim_integration.cpp, mutants.py, maap_differential.py:76-80 - R559-6-F1, R559-6-F2. Executed: unit 177/0, datapath 5/0, campaign 59/59 (57 caught, 2 controls), coverage 225/225, differential 12/12 and 17/17 (MAC-ignoring parent fails the lowest-draws check); reviewer probes q2/q4/q6/q7 caught, q1/q3/q5/q8/q9 escape
```
```text
[R559] UNCLEAN Docs - MAAP_FABRIC.md:112-116, KL_maap.md:5, KL_maap.sv:156-162 - R559-6-F2 (universal claims without executable evidence); RESIDUE R559-6-R1. Otherwise applied and clean: MAAP_FABRIC.md:96-118,150-168,253-260; AREA_BUDGET.md record table and arithmetic (78.88 %, 97 free, 11,020 / 11,973 / 52 %); 234_PP_SHADOW_AREA_BASELINE.md:34-106 against the record file; MARK_II inventory 66/66 equal; findings index; docs_check rc 0; no added em dash; check-baseline PASS
```

## 5. Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R559-6-F1) | issue body, rulings, round-6 assignment; `KL_maap.sv` first draw; datapath first offsets; fold proof; head collision pairs | R559-6 | `d1b18b3fa0b476a9b534c88466b163e15f469004` |
| RTL | CLEAN | `KL_maap.sv:141-203,330-339,380-386`; `milan_datapath.sv:7168-7176`; model==RTL cross-check; single-module synthesis; lint | R559-6 | `d1b18b3fa0b476a9b534c88466b163e15f469004` |
| Robustness | CLEAN | zero fallback, re-seed, provisioning precedence, clip counts 1..8, restart/link paths; probes q4/q5/q6/q8 | R559-6 | `d1b18b3fa0b476a9b534c88466b163e15f469004` |
| Tests | UNCLEAN (R559-6-F1, R559-6-F2) | `sim_main.cpp` section [12], `sim_integration.cpp`, `mutants.py`, `maap_differential.py`; executed unit, datapath, campaign, coverage, differential; 9 reviewer probes; row-flip search | R559-6 | `d1b18b3fa0b476a9b534c88466b163e15f469004` |
| Docs | UNCLEAN (R559-6-F2; RESIDUE R559-6-R1) | `MAAP_FABRIC.md`, `KL_maap.md`, `AREA_BUDGET.md`, `MARK_II_AREA_PLAN.md`, `234_PP_SHADOW_AREA_BASELINE.md`, `docs/findings/README.md`, `pp_resource_baseline.json`, PR body | R559-6 | `d1b18b3fa0b476a9b534c88466b163e15f469004` |

## 6. Executed evidence

Every command ran on a scratch checkout of the exact head with the pinned simulator, identity `5.050 2026-07-01 rev v5.050`. Every rc is recorded in `receipts/`.

| Run | Result |
|---|---|
| unit `make run` | 177 checks, 0 failures (`unit_run_treecopy.log`; byte copy of the head tree) |
| coverage | `KL_maap.sv` 225/225, gate PASS |
| datapath `integration-build` + run | 5 checks, 0 failures |
| campaign `mutants.py` | 59 checks, 0 failures |
| differential `--self-test` | clean 12/12; 17/17 caught (excerpt; full-log digest recorded) |
| `docs_check.py`; `lint_rtl.py --check`; `pp_resource_gate.py check-baseline` | rc 0; 90 <= 90; 3 endpoints PASS |
| single-module synthesis of `KL_maap` | rc 0 |
| fold proof / row-flip search / pair finders | see F1, F2 |
| reviewer probes (9) | q2, q4, q6, q7 caught; q1, q3, q5, q8, q9 escape |
| clone integrity | HEAD, tree, index and work tree equal the published head; gitlinks unchanged; 0 untracked or ignored entries (`clone_integrity.log`) |

## 7. Real limits

- I did not run the parent suite sweep, the processor, gPTP and Yosys banks, the builder, `tsn_fuzz`, behaviour or `xvlog`. The author reports them, some at `30242308`.
- I did not run Vivado. The round-6 OOC MAAP figure (490 / 340), the route and the three re-recorded endpoints are the author's measurements at `bee1b0d7`. I checked them only for consistency between the record file, `AREA_BUDGET.md`, the #234 finding, the Mark II inventory and `MAAP_FABRIC.md`. No round-6 measurement receipt is in the public evidence tree, which holds round-1 material. The claim "inputs differ only in `KL_maap.sv`" is unverified here.
- No manager source bank exists at this head, and I claim none.
- Hosted contexts were read, not owned. At reading time Yosys shards 0-3, yosys-elaboration, verilator-lint, wire-accountability, bdd-conformance and docs-check-no-git had succeeded; Verilator shards 0, 1, 2 and 4, docs-check, elaborate and firmware-unit were in progress; "Physical gPTP" was SKIPPED. A skip is not an execution.
- Physical calibration was NOT RUN, and field skips are not hardware proof. Acceptance 4 (bench) belongs to the post-merge lane.
- The fold proof and the pair finders use a model of the RTL first draw. That model equals the head RTL on 202 stations, and every collision cited above was confirmed on RTL.

## 8. Pending manager duties

- Rule on R559-6-F1's criterion: record the narrowed round-6 separation guarantee or set another one.
- Route R559-6-F1 and R559-6-F2 to the author.
- Carry RESIDUE R559-6-R1, R558-5-R1 and R558-2-R1 / R559-2-R1 to the residue checklist.
- Own hosted and local-replica acceptance at the exact head once the in-progress shards finish.
- Build and validate the current-dev merge candidate (source base `6aa25dec`, live dev `1fb0ed9a`) with builder and native banks, re-measuring the endpoints if the candidate's inputs differ from the record.
- Confirm the round-6 Vivado receipts (input manifests, gate output) for the re-recorded endpoints.

R559-6 FINISHED
