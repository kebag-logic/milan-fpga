[R416] POSITIVE - exact head 441d64630aa0143fa43f1049a6860cd9ed60e71e

# R416-3: internal independent review of PR #138 (issue #76, lane C5b, AECP dispatch), round 3

- **Repository:** Mister-M-alt/protocol-processor-control-plane-avb-milan, issue #76 / PR #138.
- **Head:** exact head `441d64630aa0143fa43f1049a6860cd9ed60e71e`, tree `452670bf352d425c5eb8eda9eaf8cac88a9219fa`, verified in a detached clone.
- **Assignment and start:** round-3 assignment #76 comment 5927100611; review start PR #138 comment 5932646295.
- **Scope:** the five commits on the round-2 head `2acd4025`:
  - the merge `a8fe574` of main `3f3ea56b` (#137, lane C4);
  - `0de4234` (R417-2 F1);
  - `d6b2a23` (R417-2 S3);
  - `d2b3326` (R417-2 S1);
  - `441d646` (R417-2 S2).
- **Also re-read:** the whole lane diff against the source base, `git diff 3f3ea56b..441d6463` (60 files).

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR is open at this head, and all five lenses are CLEAN. This round raises no finding of its own, not even a SUGGESTION.

- **The merge `a8fe574`.** It is a true two-parent merge. I re-derived it with `git merge-file`:
  - only `tb/pp_top/README.md` (1 region) and `tb/pp_top/sim_main.cpp` (3 regions) conflict;
  - the other three files both sides touched equal the automatic merge byte for byte;
  - every line of both sides of every conflict region is in the merge, in order;
  - the one exception is `one_section`, whose two side-lines are replaced by their union, which ORs all seven section flags;
  - `run_acmp` is identical to main's, and `run_aecp_dispatch_focus` and `run_aecp_response` are identical to the lane's.
- **Nothing of #137 is lost:**
  - the 7 main-only files equal `3f3ea56b`;
  - the 54 lane-only files equal `2acd4025`;
  - section AC runs in the default build (43 checks, 0 failing);
  - #137's ACMP campaign is **19 of 19 KILLED**, with its three goldens PASS, at the head.
- **Campaign patches.** All 163 campaign patches pass `git apply --check` at the head: 35 AECP dispatch, 28 ADP, 27 MAAP and 73 SRP.
- **R417-2 F1 is resolved.** I re-ran the AECP dispatch campaign at the head with the CI-pinned simulator: **35 of 35 KILLED**, and all three controls PASS.
  - `lk-prefix-zero-body` fails 7 checks: the five non-zero LK1/LK3 bodies, LK3b and LK3c.
  - My table check finds all 35 README cells equal to the measured counts, and 0 rows off their header.
- **S3 (`d6b2a23`).** The step matches the SRP, MAAP and ADP steps (pinned Verilator on `PATH`, then the make target). The campaign took 8 min 45 s here, capped at 8 jobs. The hosted run at this exact head has not reached the step yet (see Real limits).
- **S1 (`d2b3326`).** My 14-form probe of the opcode gate gives 0 unexpected results at the head. Against the round-2 gate the same probe gives 3 unexpected results, all `parameter` forms. The ninth selftest fixture fails if the old pattern is used, so it is load-bearing.
- **S2 (`441d646`).** The sentences only moved: the word multiset of 07 is unchanged, and "That worst case" again follows its antecedent.
- **`hdl/`.** It is byte-identical to `2acd4025`.

## Reconstruction (order followed)

1. **Contributor guides.** The repository has no `AGENTS.md` or `CONTRIBUTING.md`. I read `README.md` (building and checking; the consumption contract) and `docs/README.md` (single-source rules, citation, figure and table conventions).
2. **Scope decisions.**
   - The issue #76 body: GAP-01 acceptance 1 to 4.
   - Every maintainer and manager comment on #76: the lane assignment 5906184962, round 2 5921225908, and round 3 5927100611 (merge-commit rule, both sides kept, F1, S1 to S3, the STOP rule, gates).
   - The acceptance lists of #50, #53, #74 and #82.
   - The PR body at the head.
3. **Authorities.**
   - IEEE 1722.1-2021 7.4.21.1, 7.4.23.1 and 7.4.25.1 ("the old value if it fails"), 7.4.76.1 and 9.3.5.3.3.
   - Milan v1.2 5.4.1, 5.4.2.13, .15, .17 and .26.
   - All of the above as quoted in-tree; the specification PDFs are not distributed.
   - The integrator contract for `DESC_LINE_BYTES_P` and `RESP_BASE_P`: F01.5, 07 §3.3.1 and §3.3.2, the top's banners, and the integrator guide.
4. **Diff and history.**
   - `git diff 3f3ea56b..441d6463`, then each round-3 commit.
   - The merge re-derived from base `d5f73bac`.
   - The RTL diff against main: `KL_aecp_engine.sv`, `KL_aecp_ucpu.sv`, `ucpu_pkg.sv`, `gen_ucode.py` and the top's comments.
5. **Public evidence.**
   - The milan-fpga tree at `28314916` (`review-evidence/ppC5b-r1`) is the round-2 archive. It carries no `author-r3` directory.
   - The round-3 author packet (`author-r3`: HANDOFF, PR-BODY, `parent-c4-disposition.patch`, receipts) is on the `ppC5b-review-evidence` branch at `1caf41611220bcfd2c05032c46d9d49fea5842e7`, and I read it there.
   - The manager's evidence comments on #76 and #138. The last bank comment is for round 2's `2acd4025`.
6. **Prior public findings.** I read them only after my verdict and ledger draft were written to this file. Each is resolved or retained below.

## Findings of this round

None at any severity.

## Prior public findings: disposition at this head

| Prior item | Disposition at 441d6463 | Evidence (this round) |
|---|---|---|
| R417-2 F1 (MINOR, Docs): the `lk-prefix-zero-body` row lost its count to a stray `\|` | **Resolved** (`0de4234`) | `receipts/readme_counts_check.txt`: 35 rows, 35 measured, 0 off header, 0 problems; `receipts/md_tables_gfm_added.txt`: 0 rows the PR adds are off their header |
| R417-2 S1 (Tests): the gate drops a `parameter`-keyword `OP_*_C` | **Taken** (`d2b3326`) | `receipts/m9_gate_probe_head.txt` (14 forms, 0 unexpected; selftest 9/9; gate PASS, 30 opcodes); `receipts/m9_gate_probe_round2_gate.txt` (round-2 gate: 3 unexpected); `receipts/m9_gate_old_pattern_selftest.txt` (8/9 with the old pattern) |
| R417-2 S2 (Docs): 07 §3.3.1 "That worst case" lost its antecedent | **Taken** (`441d646`) | `receipts/s2_word_multiset.txt`: move only; 07:286-296 read in place |
| R417-2 S3 (Tests): no CI step for the AECP dispatch campaign | **Taken** (`d6b2a23`) | `.github/workflows/hdl.yml:67-70`; the step's command ran here 35/35 (`receipts/aecp_dispatch_mutants_chunk{1,2}.txt`); hosted execution pending |
| R416-2 S-R2 (Tests, Robustness): AUDIO_UNIT and CLOCK_DOMAIN short-lane guards ungraded | **Retained** (SUGGESTION) | Recorded in the PR body's "What remains (round 3)" with the reachability reason. No code comment at `gen_ucode.py:1138/1165`. No impact. |
| R416-1 F1 / R417-1 F2 (MINOR): SET_CONTROL out-of-range body | **Resolved** (round 2), still holds | `sctrl-badarg-zero-body` KILLED (2); LK3b/LK3c pass in `receipts/pp_top_make_run.log` |
| R416-1 F2 (MINOR): undocumented 1008 ceiling | **Resolved** (round 2), still holds | `line guards: 6 cases, 0 failing`; `line-ceiling-dropped` KILLED; 1008 simulated (Robustness) |
| R417-1 F1 (MINOR): a line below 576 wrote past the reservation | **Resolved** (round 2), still holds | `line-floor-rounded`, `line-buffer-fixed-592` and `rb-rounded-buffer-no-page-cap` KILLED; RB passes at 584 and 1008 |
| R416-1 F3 (MINOR): `git diff --check` rc 2 | **Resolved** (round 2), still holds | `.gitattributes:5`; `git diff --check 0451d83d HEAD` and `3f3ea56b HEAD` rc 0 (`receipts/light_gates.txt`) |
| R416-1 S1/S2 and R417-1 S1/S2 | **Taken** in round 2 (S1 for STREAM only; the rest retained as S-R2) | unchanged at this head |

## Five lenses, with artifact-specific evidence

### Conformance — CLEAN

- **No behaviour change this round.** `hdl/` is identical to `2acd4025` (`git diff --quiet 2acd402 441d646 -- hdl`). The controller-visible behaviour judged in round 2 therefore stands:
  - the locked refusals and the out-of-range refusal carry the value in force (7.4.21.1, 7.4.23.1, 7.4.25.1);
  - responses above cdl 524 for the Milan 5.4.1 set;
  - GET_DYNAMIC_INFO capped at 524 (7.4.76.1);
  - pages above 71 records answer NO_RESOURCES with count 0.
  - At the head these are graded by AX LK, LK3b/LK3c, OV, PG and RD: `receipts/pp_top_make_run.log`, AX 218/0 in both the default and line builds.
- **Closes lines.** #50, #53, #74, #76 and #82 are each met in full against their own acceptance lists:
  - #76: M9 sweeps the 30 `OP_*_C` and the gate holds the set; the seven guard arms are KILLED and recorded; 03 §7 states that no response-size ROM ships; the suites are green;
  - #74: A5b's six opcodes; the REBOOT arm is KILLED;
  - #53: LK1 to LK6; 06 §6.8; six CHECK_LOCK NOP arms KILLED;
  - #50: OV1/OV2/OV5 above cdl 524 through slot 4; `ov-oversize-never` KILLED; PG; 06 §3 per command;
  - #82: RD0 to RD4; OV; 00 §6.6 and 07 §3 hand the model rules to the consumer; 07 §3.3 and 03 §7 state the Δ8 ceiling.
  - The requirement tickets listed under #76 and #82 (#38, #51 and #60) are not closed, and the PR body says so.
- **The STOP rule holds.** Round 3 changes no port, parameter or parent-visible behaviour. The parent-visible additions are the merged #137 (its `acmp_mutants.py` disposition line for the parent's `measure_test_evidence.py`) and a CI-only step.

### RTL — CLEAN

- **No RTL in round 3.** `hdl/` is byte-identical to the round-2 head, and every tracked file re-hashes to its index blob (`receipts/clone_integrity.txt`).
- **I re-read the lane's RTL against main:**
  - the response buffer exactly `16 + LINE_BYTES_P`;
  - three elaboration guards naming `DESC_LINE_BYTES_P`;
  - `LINE_MIN_BYTES_C = 24 + 8·71 - 16 = 576` and `LINE_MAX_BYTES_C = 1008`;
  - the uCPU's D8 APPEND cap, gated off inside a batch, with its own `$error` range;
  - the TAIL COPY_BUFFER count `rf[ra] - imm`, reachable only behind the too-short guards;
  - the configuration-0 READ_DESCRIPTOR re-dispatch, gated by protocol, message type 0, opcode, cdl ≥ 20 and `cfg_ix_r == 0`.
- **Pinned-simulator results.** `scripts/lint_hdl.sh` under the pinned 5.050 is OK for all 41 modules, and `check_upc_map.py` passes (58 constants, 86 entry points) (`receipts/light_gates.txt`).

### Robustness — CLEAN

- **The merge keeps both sides.** `receipts/merge_sides.txt` comes from `scripts/reconstruct_merge.sh` and `scripts/check_merge_sides.py` on a `git merge-file` reconstruction:
  - every lane-side and main-side line of the four conflict regions is in the merge, in order;
  - all 1,308 and 11,704 context lines are in order;
  - the only replaced lines are the two `one_section` variants, superseded by their union.
  - The resolution adds only one blank line in the README, plus, in `sim_main.cpp`, the separators and the first lines of `run_acmp`, which the three-way alignment had taken as context shared with `run_aecp_dispatch_focus`.
  - `scripts/compare_functions.py` confirms that, at the head:
    - `run_acmp` is identical to main's;
    - `run_aecp_dispatch_focus` and `run_aecp_response` are identical to the lane's.
- **The merged `main()`** (`sim_main.cpp:11689-11717`) keeps `--acmp-only`, `--maap-internal-only` and `--aecp-dispatch-only`, and AC runs after D3 in the default build. The fixture and line builds are unchanged.
- **The top of the legal line range runs end to end.** The suite lints 1008 but simulates only 576 and 584. A disposable scratch build at `LINE_FIXTURE=1008` ran section AX: **218 checks, 0 failing** (`receipts/probe_line1008_aecp_line.log`). That includes OV1's whole-line 1008-byte read at cdl 1024 and frame 1050, and RB (no write past `RESP_BASE_P + 1024`).
- **The opcode gate fails closed.** A `parameter`, untyped, typeless-width, `int`, decimal, comma-list or `#()`-port declaration, a duplicate opcode, and an upper-case radix are all refused. A comment, a GDI constant and a right-hand-side reference all pass, as they should (`receipts/m9_gate_probe_head.txt`).
- **The CI step on the hosted runner:**
  - the campaign runs serially in a temporary tree with the workflow's pinned Verilator, and writes nothing in the checkout;
  - the build parallelism follows the runner's cores (`-j 0`);
  - here it took 2 min 55 s plus 5 min 51 s at 8 jobs;
  - the round-2 hosted `suites` job took 75 min, so this step stays far inside the 360-minute default job limit, even at a several-fold slower runner.

### Tests — CLEAN

All runs used the CI-pinned Verilator 5.050 (identity `Verilator 5.050 2026-07-01 rev v5.050`, wrapper sha256 `905795b9…`), capped at 8 build jobs by `scripts/verilator_j8.sh`, all in the foreground:

| Run | Result | Receipt |
|---|---|---|
| `aecp_dispatch_mutants.py`, all 35 arms in 2 chunks | 35/35 KILLED by named check; controls `aecp-dispatch`, `aecp-line`, `line-guards` PASS | `receipts/aecp_dispatch_mutants_chunk{1,2}.txt`, `receipts/aecp_dispatch_results_chunk{1,2}.json` |
| README table against measured counts | 35/35 equal; 0 rows off header | `receipts/readme_counts_check.txt` |
| `tb/pp_top/acmp_mutants.py` (#137), 19 rows in 2 chunks | 19/19 KILLED; goldens acmp_listener, pp_top, rx_validator PASS | `receipts/acmp_mutants_chunk{1,2}.txt`, `receipts/acmp_results_chunk{1,2}.json` |
| `make run` in `tb/pp_top` (scratch copy) | rc 0; fixture guards 4, line guards 6; 8,367 + 20 + 218 = **8,605 checks, 0 failing**; D3 133, ACMP 43, AD 55, AX 218 | `receipts/pp_top_make_run.log` |
| `tb/ucpu` (scratch copy) | rc 0; 398/0 | `receipts/ucpu_make.log` |
| `check_m9_opcodes.py --selftest` and plain | 9/9; PASS, 30 opcodes | `receipts/m9_gate_probe_head.txt` |
| 163 campaign patches `git apply --check` | 0 refused | `receipts/patch_apply_check.txt` |
| `gen_matrix.py --check`, `git diff --check` (×2) | rc 0 | `receipts/light_gates.txt` |

These agree with the author's round-3 receipts (33 suites, 1,018,518 checks, run on a different simulator build), and with the PR body's counts.

### Docs — CLEAN

- **README.** `tb/pp_top/README.md` carries the F1 cell and the CI sentence. Its tail keeps section AC, the ACMP controls table, then section AX, every line of both sides in order.
- **07 §3.3.1.** The move is exact (`receipts/s2_word_multiset.txt`).
- **Tables.** No markdown table row the PR adds is off its header under GFM splitting (`receipts/md_tables_gfm_added.txt`). Two rows older than the lane do split on a `||` inside a code span (`docs/guides/integrator.md:365`, `tb/pp_top/README.md:672`). They are outside the lane's lines, and the PR body records them.
- **Docs gates.** `make check` passes: 41 mermaid and 18 WaveDrom blocks, 994 links, the matrices, and 26 parameters in top, guide and diagram (`receipts/light_gates.txt`).
- **PR body.** Its round-3 sections match the tree: merge facts, counts, the CI step, nine selftest fixtures, and the parent-visible list.

## Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #76 acceptance 1-4; #50/#53/#74/#82 acceptance; PR body Closes and parent-visible list; AX LK/OV/PG/RD/RB at the head | R416-3 | 441d64630aa0143fa43f1049a6860cd9ed60e71e |
| RTL | CLEAN | `hdl/` identity to 2acd4025; lane RTL diff against 3f3ea56b (engine, uCPU, package, top); pinned lint; UPC map gate | R416-3 | 441d64630aa0143fa43f1049a6860cd9ed60e71e |
| Robustness | CLEAN | merge re-derivation and side-union check; merged `main()`; scratch line-1008 AX run; 14-form gate probe; CI step budget | R416-3 | 441d64630aa0143fa43f1049a6860cd9ed60e71e |
| Tests | CLEAN | AECP dispatch campaign 35/35; ACMP campaign 19/19; pp_top 8,605/0; ucpu 398/0; M9 selftest 9/9; 163 patches apply | R416-3 | 441d64630aa0143fa43f1049a6860cd9ed60e71e |
| Docs | CLEAN | `tb/pp_top/README.md` mutation table and merged tail; 07 §3.3.1; GFM table check; `make check`; PR body round-3 sections | R416-3 | 441d64630aa0143fa43f1049a6860cd9ed60e71e |

## Real limits

- **Hosted runs.** Both hosted runs at this exact head (push 36870299862, pull_request 36870303632) were **in progress** at 14:15 UTC:
  - `docs-gates` and `portability`: success;
  - `suites`: lint and every suite succeeded, the SRP campaign was running, and the MAAP, ADP and **AECP dispatch** campaign steps were still pending.
  - So the new CI step has **not yet executed on a hosted runner**. My timing judgment is an estimate from my local run and the round-2 hosted job (`receipts/hosted_runs_exact_head.txt`).
- **No full banks.** I did not run `./scripts/run_suites.sh` over all 33 suites, the D3, GSI, name-write, SRP, MAAP or ADP campaigns, Yosys, or any parent or builder bank. Only `tb/pp_top`, `tb/ucpu`, the goldens of `tb/acmp_listener` and `tb/rx_validator`, and the two campaigns above ran here. For the rest I rely on the author's round-3 receipts and the manager's banks.
- **Evidence pointer.** The evidence link given for this round (milan-fpga `28314916`) is the round-2 archive. The round-3 author packet is at `1caf4161` on `ppC5b-review-evidence`. No public manager bank receipt or comment for `441d6463` was visible to me. I took the statement that the manager's source static/builder and native banks passed at this head as given, and did not verify it.
- **Simulator build.** All simulation used Verilator 5.050 (the CI pin). The author used 5.052; the two agree on every count I compared.
- **Hardware.** Physical calibration was NOT RUN; field skips are not hardware proof. No hardware was used.

## Pending manager duties

- Accept the exact-head hosted runs once complete, in particular the first hosted execution of "AECP dispatch mutation campaign", and its duration within the `suites` job.
- Publish or point to the manager's source static/builder and native bank receipts for `441d6463`.
- Run the donor bank and the parent consumer set at milan-fpga dev `ea3fb388`, with the processor gitlink at this head and #137's `acmp_mutants.py` `DUT_READER_DISPOSITIONS` line (`parent-c4-disposition.patch`).
- Build the final current-dev candidate at the merge turn (source base `3f3ea56b`, live dev `ea3fb388`), and own the hosted/act acceptance.
- At the merge, check that each of #50, #53, #74, #76 and #82 closes, and that #38, #51 and #60 stay open.

## Clone restoration

- Probes ran only in scratch copies under the packet's `scratch/`, or in temporary trees the drivers create there.
- The clone's own run artifacts (`.venv-wavedrom/`, two `__pycache__/` directories, all ignored and all created this session) were removed.
- Final state:
  - HEAD `441d6463`, index tree `452670bf…` (equal to HEAD's tree);
  - `git status --porcelain --ignored` empty;
  - every tracked blob re-hashes to its index entry, with no mode mismatch;
  - the repository has no submodule gitlinks (0 entries of mode 160000).

R416-3 FINISHED
