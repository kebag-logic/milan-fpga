[R445] POSITIVE - exact head 6ca4ade8c296540b78ca5bec0d13a342fd567d12

# R445-3 external independent review: processor issue #83 / PR #150 (lane P1), round 3

- **Head.** Exact head `6ca4ade8c296540b78ca5bec0d13a342fd567d12`, tree `d0b0b5e9aac1b91e2fd749c4826ef8ff20741290`.
- **Base and previous heads.** Source base `ddb3119dbbce59f81bf7a536a1ad90a20546edb2`. The round-2 reviewed head was `5960d8fc7e4f6ef2d7551bb224154ef2c265d894`.
- **Review start.** PR #150 comment 5971136107.
- **Scope.** This is a delta review of round 3 (`5960d8fc..6ca4ade8`). The round has two commits:
  - `6b8df47`, the R21 banner;
  - `6ca4ade8`, the nvm_port README residue.

  It is judged against R444-2 (PR #150 comment 5970346414), R445-2 (5970928548) and the round-3 assignment (#83 comment 5970930857).
- **What the delta touches.** 2 files and 3 hunks, +15/-14:
  - `tb/pp_top/sim_main.cpp`, comment lines only;
  - `tb/nvm_port/README.md`.

  No other path changed (`git diff --raw 5960d8fc 6ca4ade8`).

## Verdict

**POSITIVE.** No BLOCKER, MAJOR, MINOR or RESIDUE is open at this head.

Every round-2 item is **resolved**, and none is retained or worsened:
- R444-2's one MINOR, N-F1;
- the three RESIDUE items N-R1 to N-R3;
- R445-2's R1 and R2.

The round-1 findings stay resolved, because nothing else changed. The five earlier suggestions stay open by assignment and are listed in the PR body. One new SUGGESTION (S1, wording) is optional.

## 1. Reconstruction (public sources only, in the order required)

1. **Repository guidance.** The tree has no `AGENTS.md` or `CONTRIBUTING.md` (`git ls-files`). I used `README.md` and `docs/README.md` instead: the single-source rules, the figure and citation conventions, and `make check`.
2. **Issue #83.** I read the body (frozen acceptance 1 to 4) and every comment in order:
   - lane assignment 5965788915;
   - STOP 5967588719 and ruling (b) 5967611704: the channel maps are the integrator's;
   - REVIEW READY 5968343520;
   - round 1b 5968352676, STOP 5969239148 and ruling (b) 5969246536: gate 16 goes to milan-fpga #643;
   - round-2 assignment 5969765075 and correction 5969802215;
   - REVIEW READY 5969914780;
   - **round-3 assignment 5970930857**;
   - REVIEW READY (round 3) 5971127613.
3. **Authorities.**
   - 07 §5.1 "Who persists what" (`docs/architecture/07_memory_maps.md:558-568`): the D3 writer persists user names, and the channel maps are the integrator's under the ruling on #83;
   - the writer's trigger rule (`hdl/aecp/KL_aecp_nvm_writer.sv:123-132`): a live write is the trigger, never a mark, and a name's trigger is `nchg_i`, the engine's `name_wr_o`;
   - the top port `aecp_name_wr_o` (`hdl/top/protocol_processor_top.sv:769`);
   - section D3N (`tb/pp_top/README.md:294`, `sim_main.cpp:10805`);
   - 09 `:56`, the randomized cuts.
4. **Diff and history.**
   - `git diff 5960d8fc..6ca4ade8` hunk by hunk;
   - `git log ddb3119d..6ca4ade8` (30 commits);
   - the cited line positions at `ddb3119d`, `53e1474b`, `f4167536`, `c066dd83`, `5960d8fc` and the head.
5. **Public evidence.** milan-fpga `3a657083`, `review-evidence/ppP1-r1`. Every file's sha256 equals its MANIFEST `published_sha256` (`receipts/public_evidence_3a657083.txt`). It is the round-1 author packet and holds no bank receipts for this head (see Limits). No manager evidence comment for this head exists on #83 or PR #150.
6. **Prior public reviews.** I read R444-1, R445-1, R444-2 and R445-2 only after my independent verdict and ledger were written down (`receipts/independent_verdict_before_prior_reviews.md`). That verdict is unchanged by reading them.

## 2. Executed evidence (all at the exact head unless stated)

**Simulator.** The scoped wrapper `$VALIDATION_TOOLS/pinned-verilator-5.050/verilator`:
- wrapper sha256 `905795b9…e92f`;
- version `Verilator 5.050 2026-07-01 rev v5.050`;
- record in `receipts/tool_identity.txt`.

The PATH simulator is 5.052. It was not used for any gate: lint was rerun with the pinned wrapper first on PATH.

**Where the builds ran.** All builds ran in a disposable clone under `scratch/`. The review clone was only read.

| # | Probe | Result | Receipt |
|---:|---|---|---|
| 1 | Paths changed in round 3 | `M tb/nvm_port/README.md`, `M tb/pp_top/sim_main.cpp`, modes 100644 unchanged; no `hdl/`, generator, image, Makefile or patch path | this report |
| 2 | Comment-stripped token stream of `tb/pp_top/sim_main.cpp`, `5960d8fc` vs head (`g++ -fpreprocessed -E -P`, whitespace collapsed) | **IDENTICAL** (sha256 `2d346ffd…44bc` both) | `receipts/strip_compare.txt`, `scripts/strip_compare.sh` |
| 3 | Control: one token (`+ 0`) planted on a code line of the head copy | **CAUGHT** | same |
| 4 | Line-shift exposure. The banner adds one line, which shifts everything after `:4254`. I looked for line-number citations into `sim_main.cpp`, for `__LINE__` in `tb/pp_top`, and for drivers or plants anchoring on the old banner text | none; none; none. The two tracked patches that touch `sim_main.cpp` (`ctr_mutations/store-*`) still apply | `receipts/citations_and_greps.txt` |
| 5 | Tracked mutation patches, `git apply --check` | **224 of 224 apply** | `receipts/patch_apply_check.txt`, `scripts/check_patches_apply.sh` |
| 6 | Assignment grep `git grep -nE -i "not implemented yet\|map stage\|later stage" -- hdl tb` | head: **no hit (rc 1)**; `5960d8fc`: one hit, `tb/pp_top/sim_main.cpp:4252` (the old banner) | `receipts/citations_and_greps.txt` |
| 7 | Facts the new banner states | port `aecp_name_wr_o` exists (`top:769`, `:3847`); the writer's name trigger is `nchg_i` = `name_wr_o` (`writer:130-131`), and a mark is never a trigger (`:123`); D3N exists and runs (`sim_main.cpp:10805`, README `:294`); 07 §5.1 assigns the maps to the integrator (`:562-565`) | same |
| 8 | Citations at `tb/nvm_port/README.md:100-101`, positions at each revision | `frame_ok_w`: 482-485 at `ddb3119d` and `f4167536`, 546-549 at `53e1474b` and `c066dd83`, **549-552 at the head**. Shadow instance: 2727 at `ddb3119d`, 2725 at `f4167536`, 2731 at `53e1474b`, 2729 at `c066dd83`, **2730 at the head**. Both README citations now point at the cited symbol | same, `scripts/check_citations.sh` |
| 9 | `make -C tb/pp_top run` (five builds) | rc 0, **10,390 checks: 10,390 PASS, 0 FAIL** (default 9,918 + 20 + 178 + 218 + 56; D3 319, D3V 11, D3KR 1,000) | `receipts/pp_top_head.log` |
| 10 | `scripts/lint_hdl.sh`, pinned 5.050 first on PATH | rc 0, 41 of 41 LINT OK | `receipts/lint_hdl_head_pinned.log` |
| 11 | `make check`; `scripts/gen_matrix.py --check` | rc 0 (1,114 links; 115 REQ rows, 17 GAP findings; parameters 28/28/28; 94 rows, 0 untested); rc 0 | `receipts/docs_gates_head.log` |
| 12 | `make -C tb/nvm_port figures`, the gate over the README this round edits | rc 0: 160 builds, baseline 393 of 393 PASS, "all measured figures agree with the tree" | `receipts/nvm_port_figures_head.log` |
| 13 | PR body as live at review (`receipts/pr150_body_at_review.md`, sha256 `4eada4fc…a0ca`) | The Round 3 section is present. The quoted banner text and R444-2 N-R2's exact text are present verbatim (whitespace-flattened match). Every line figure checks against probe 8, and the PR body's gate table matches probes 9 to 12 | this report |
| 14 | Hosted CI at the exact head (read-only API; observation time in the receipt) | Workflow `hdl`, run 37137368226 (push, exact head) and run 37137370108 (pull_request): `docs-gates` and `portability` **success** in both. `suites` was still **in progress** in both: step 5 (lint + every suite) was running and steps 6 to 12 were pending. Step 4 (`Build Verilator`) was skipped on a cache hit, which is a cached context and not an executed failure | `receipts/hosted_ci_observation.txt` |
| 15 | Review-clone integrity after all probes | HEAD and tree exact, index tree equals the HEAD tree, porcelain output (ignored files included) is empty, all 501 index entries match their on-disk blob and mode, 0 mismatches. **No gitlinks** (no `.gitmodules`), so there are no submodule gitlinks to verify | `receipts/clone_integrity.txt`, `scripts/clone_integrity.sh` |

## 3. Round-2 items at this head

| Round-2 item | Status | Evidence |
|---|---|---|
| **R444-2 N-F1** (MINOR; Conformance, Tests, Docs): the R21 banner claimed "map and name stages (not implemented yet)" | **RESOLVED** | `tb/pp_top/sim_main.cpp:4250-4254` now carries R444-2's required text verbatim: "…not a persistence trigger: the D3 writer's name stage selects its records from the accepted live name write (`aecp_name_wr_o`, section D3N), the channel maps are the integrator's to persist (07 §5.1, the ruling on #83), and section D3 grades the scalar records." Every fact holds (probe 7). Comment only (probes 2 and 3). The verification grep finds nothing (probe 6). `tb/pp_top` is 10,390/10,390, and `make check` and lint are rc 0 (probes 9 to 11) |
| **R444-2 N-R1** (RESIDUE): "still owed" lead words | **RESOLVED** | `tb/nvm_port/README.md:1064` reads "so the randomized half is not cut by this suite". `:1347` reads "**… asks for are not cut by this suite** on either side". These are R444-2's exact texts. The D3KR parenthetical is word-for-word unchanged, and each hunk is re-wrapped in place (11 lines out, 11 in). The figures gate passes (probe 12). Of the other "still owed" hits in the file (`:273`, `:540`, `:561`, `:601`, `:937`), none concerns randomized cuts: they describe a device still owing a completion |
| **R444-2 N-R2 = R445-2 R2** (RESIDUE): PR-body line figures in "Seen, not fixed in this round" | **RESOLVED** | The PR body (`:394-398`) carries R444-2's exact fix: "`:546-549` since the name stage and `:549-552` at the head … `:2727` at `ddb3119d`, `:2725` at `main` `f4167536`, `:2730` at the head". This also satisfies R445-2 R2's fix ("`:546-549` since the name stage, `:549-552` at this head"). All figures were verified per revision (probe 8) |
| **R444-2 N-R3 = R445-2 R1** (RESIDUE): stale citations `tb/nvm_port/README.md:100-101` | **RESOLVED** | They now cite `hdl/aecp/KL_aecp_nvm_writer.sv:549-552` (the `frame_ok_w` declaration and assign, exactly) and `hdl/top/protocol_processor_top.sv:2730` (`KL_acmp_nvm_shadow #(`). Round 3 changes neither HDL file, so the citations stay valid (probe 8) |
| Round-1 findings (R444-1 F1 to F3 = R445-1 F1 to F3) and round-1 residue | **remain RESOLVED** | Both round-2 reviews closed them. Round 3 touches none of their artefacts except the one further instance N-F1, now resolved |
| Suggestions R444-1 S1, S2; R445-1 S1 to S3 | open by assignment, not findings | Listed in the PR body (Round 2 item 5, Round 3 item 3, "What remains" `:234`) |

## 4. Findings at this head

No BLOCKER, MAJOR, MINOR or RESIDUE.

### S1 - SUGGESTION - Docs

- **Location.** `tb/nvm_port/README.md:1347-1348`.
- **The wording.** "The RANDOMIZED cut points `09_verification.md:56` asks for are not cut by this suite" says that cut *points* are "not cut".
- **Why it is only a suggestion.**
  - The meaning is unambiguous: this suite does not exercise them, and D3KR does.
  - It is R444-2's prescribed text.
  - It changes no claim.
- **Optional rewording, if the file is touched again.** "… asks for are not exercised by this suite** on either side". Not required. It does not affect the verdict.

## 5. Lens evidence

- **Conformance: CLEAN.** The R21 banner now states the amended D3 contract as ruling 5967611704 and 07 §5.1 do: the maps are the integrator's, and the D3 writer's name stage is triggered by the accepted live name write and never by a mark (writer `:123-132`). No requirement, clause or acceptance claim changed in round 3. The nvm_port README's coverage statement points at D3KR for #83 acceptance 3 and 09 `:56`.
- **RTL: CLEAN.** Round 3 changes no `hdl/` byte, generator or image input (probe 1), so the ROMs and netlist are untouched by construction. Lint at the head is 41/41 on the pinned simulator (probe 10). Hosted off-vendor elaboration (`portability`) succeeded at the head (probe 14).
- **Robustness: CLEAN.** The bench's comment-free token stream is identical, and the control is caught (probes 2 and 3). The added line shifts no citation, `__LINE__`-dependent output or text anchor. All 224 mutation patches apply, including the two that edit `sim_main.cpp` (probes 4 and 5). The review clone was verified byte- and mode-exact (probe 15).
- **Tests: CLEAN.** `tb/pp_top` is 10,390/10,390 across five builds, with D3 319, D3V 11 and D3KR 1,000 (probe 9). The banner now describes what D3N and D3 grade. The nvm_port figures gate re-measures the edited README, 393/393 baseline, and agrees (probe 12).
- **Docs: CLEAN.** The prescribed texts are verbatim (section 3). Both README citations and every PR-body line figure are verified against the tree per revision (probe 8). `make check` and the matrix check are rc 0 (probe 11). The PR body's Round 3 section matches the executed gates. S1 is a suggestion only.

## 6. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ruling 5967611704; 07 §5.1 `:558-568`; writer trigger rule `KL_aecp_nvm_writer.sv:123-132`; top `aecp_name_wr_o` `:769`; R21 banner `sim_main.cpp:4247-4256`; nvm_port README `:1064`, `:1347` vs 09 `:56` | R445-3 | 6ca4ade8c296540b78ca5bec0d13a342fd567d12 |
| RTL | CLEAN | `git diff --raw 5960d8fc 6ca4ade8` (no `hdl/` path); `lint_hdl.sh` 41/41 at pinned 5.050; hosted portability success | R445-3 | 6ca4ade8c296540b78ca5bec0d13a342fd567d12 |
| Robustness | CLEAN | comment-stripped token identity plus caught control; line-shift exposure scan; 224/224 patch applies; clone integrity | R445-3 | 6ca4ade8c296540b78ca5bec0d13a342fd567d12 |
| Tests | CLEAN | `tb/pp_top` five-build run 10,390/0; `tb/nvm_port` figures gate 160 builds rc 0; banner vs D3N/D3 sections; hosted suites job (in progress, not counted) | R445-3 | 6ca4ade8c296540b78ca5bec0d13a342fd567d12 |
| Docs | CLEAN | round-3 delta; `tb/nvm_port/README.md:97-101`, `:1060-1067`, `:1347-1351`; PR #150 body (live) Round 2/Round 3 sections; `make check`, `gen_matrix.py --check`; REVIEW READY 5971127613 | R445-3 | 6ca4ade8c296540b78ca5bec0d13a342fd567d12 |

## 7. Real limits

- **Banks not run here, by mandate.** I did not run the full `run_suites.sh` bank (33 suites), the mutation campaigns, the parent consumer set or any Yosys, builder or OOC bank. I ran `tb/pp_top`, which is the suite of the changed file, and the nvm_port figures gate, which covers the changed README. Round 3 has no logic change (probes 1 to 3), so the earlier campaign results carry over. The head-level bank figures are the author's and the manager's.
- **Manager bank receipts not in the public evidence.** The assignment states that the manager's source static/builder and native banks passed at this head. The cited public tree (`3a657083`, `review-evidence/ppP1-r1`) holds only the round-1 author packet, and no manager evidence comment for this head is on #83 or PR #150. I did not inspect those receipts.
- **Hosted `suites` was still in progress at both runs when observed.** `docs-gates` and `portability` had succeeded. I did not see `suites` complete. The pull_request run tests the merge ref, and the push run is the exact-head run.
- **Round-2 and round-3 HANDOFF.md are not public.** Only the PR body and the issue comments were checkable.
- **Stripping tool.** The token comparison used the C++ preprocessor (`-fpreprocessed`, no macro expansion) on the testbench source, not a compiled-object comparison. The control shows that it detects a one-token change.
- **Hardware.** Physical calibration NOT RUN. No hardware was used, and field skips are not hardware proof.

## 8. Pending manager duties

- Hosted/act acceptance at this head, including the `suites` jobs of runs 37137368226 and 37137370108 (lint and every suite, the SRP, MAAP, ADP and AECP campaigns, matrix no-drift and nvm_port figures).
- Publish the source static/builder and native bank receipts at this head, and the round-2/round-3 HANDOFF and PR-BODY archive.
- Build the final current-dev candidate at the merge turn (source base `ddb3119d`, live dev `bbf704ec`). It is distinct from this source validation. Run the consumer bank with `parent-adoption-c8-bbf704ec.patch` then `parent-adoption-p2-p1-1269cdaf.patch`, with gate 16 recorded against milan-fpga #643.
- Track milan-fpga #643 before the second pin adoption.
- The open suggestions (R444-1 S1, S2; R445-1 S1 to S3; and this review's S1) are not part of the verdict. Merge requires two independent positive reviews and the full completion bar.

R445-3 FINISHED
