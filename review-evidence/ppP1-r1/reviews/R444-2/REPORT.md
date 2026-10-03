[R444] NEGATIVE - exact head 5960d8fc7e4f6ef2d7551bb224154ef2c265d894

# R444-2 internal independent review: processor issue #83 / PR #150 (lane P1), round 2

- Exact head `5960d8fc7e4f6ef2d7551bb224154ef2c265d894`, tree `99a6b049c9e2759799dd86daf26ba66ef466463e`. Round-1 head `c066dd83a2004f9b3640a933860c4d9e677d017e`. Lane base `ddb3119dbbce59f81bf7a536a1ad90a20546edb2`.
- Scope: a delta review of round 2 (`c066dd83..5960d8fc`: `219cd67`, `5960d8f`). Round 2 is documents and comments only. It is judged against R444-1 (5969549669), R445-1 (5969760336) and the round-2 assignment (#83 comment 5969765075).
- Review start: PR #150 comment 5969923302.

## Verdict

**NEGATIVE.** There is one open MINOR, N-F1.

Round 2 does what the assignment asked:
- The five prescribed map-contract replacements are applied verbatim.
- Every changed HDL line is a comment. The comment-stripped sources, the elaborated netlist and the ROMs are identical to the round-1 head.
- The randomized-cut text is appended at both `tb/nvm_port` passages, and it is accurate.
- The hunk count is corrected to 11 hunks in 7 files, and the correction comment is posted.
- The PR-body residue items are applied.

All six round-1 findings and all five round-1 residue items are resolved (table below).

N-F1 comes from my own sweep, which covered the whole tree and not only the round-1 grep scope. A fifth comment still states the claim that round 1 graded MINOR: "the saved-state contract's map and name stages (not implemented yet)", at `tb/pp_top/sim_main.cpp:4250-4253`. That claim is now false for names and contradicts the amended contract for maps.

Three further defects are wording only and are recorded as RESIDUE: N-R1 to N-R3.

## Reconstruction (public sources only)

1. The repository has no `AGENTS.md` or `CONTRIBUTING.md`. I used the conventions in `README.md` and `docs/README.md`: the single-source rules, and `make check` before every commit.
2. Issue #83's frozen acceptance (items 1 to 4), then the comments in order:
   - lane assignment 5965788915;
   - STOP M1 5967588719 and ruling (b) 5967611704: maps are the integrator's;
   - REVIEW READY 5968343520;
   - round 1b 5968352676, STOP 5969239148 and ruling (b) 5969246536: gate 16 goes to milan-fpga #643;
   - the round-2 assignment 5969765075;
   - correction 5969802215;
   - REVIEW READY (round 2) 5969914780.
3. Authorities:
   - 07 §5.1 "Who persists what" (`docs/architecture/07_memory_maps.md:552-589`);
   - 07 §5.2 rows `0x60`/`0x70` (`:629-630`);
   - 07 §5.3 (`:708-709`);
   - 09 F09.3 NVM row (`docs/architecture/09_verification.md:56`).
4. `git diff c066dd83..5960d8fc` (5 files, +25/−15) and `git log ddb3119d..5960d8fc` (28 commits).
5. Public evidence: `kebag-logic/milan-fpga@3a657083 review-evidence/ppP1-r1`. Its MANIFEST and the sha256 of each file match. It is the archive of round 1b, published at 12:39Z, before round 2.
6. The live PR #150 body at review time (`receipts/pr150_body_at_review.md`, sha256 `e12f58ac…75cf3`).
7. Round-1 reports R444-1 and R445-1: read only after my own pass over the round-2 diff and my own tree sweep were complete.

## Executed evidence (all at the exact head unless stated)

Simulator: the pinned 5.050 wrapper (`receipts/tool_identity.txt`, wrapper sha256 `905795b9…e92f`, `Verilator 5.050 2026-07-01 rev v5.050`). Builds ran from `git archive` extractions under `scratch/`, through a job-capping wrapper (`scripts/verilator-capj.sh`). Concurrent jobs were run from one foreground driver (`scripts/run_fg.sh`) and stayed at or below 16 parallel jobs.

| What | Result | Receipt |
|---|---|---|
| Changed HDL lines (`git diff -U0 c066dd83 5960d8fc -- hdl`) | 28 lines (engine 2+2, writer 10+7, top 4+3), all comment lines (`^[+-]\s*//`) | this report; `receipts/probe/pp_compare.txt` |
| Comment-stripped preprocess (`-E -P`), 3 files, base vs head | all three PP-EQUAL | `receipts/probe/pp_compare.txt` |
| Elaborated netlist of `protocol_processor_top` (whole `hdl/` tree, `--json-only`, source locations dropped), base vs head | 20 differing values, every one the text of a simulator-generated `unique case` assertion that embeds `<file>.sv:<line>` (shifted by the added comment lines); with that line number masked: identical (sha256 `edee2ca9…1a53` both) | `receipts/probe/netlist_hashes.txt`, `netlist_raw.diff` |
| ROMs regenerated from the generators, base vs head | `ltn_rom.hex` `23cc67ee…e956`, `ucode.hex` `518b900c…37f8`, both byte-identical; no generator or image input is in the diff | `receipts/probe/rom_hashes.txt` |
| Prescribed texts (R445-1 F2 ×5, F3 append ×2), whitespace/comment-marker normalized | all present verbatim, every old text gone | `receipts/exact_texts_head.txt`, `scripts/check_exact_texts.py` |
| Round-1 verification grep `map stage\|later stage\|not implemented` over `hdl/ tb/pp_top/README.md` | head: only `gen_ucode.py:1545` (sampling-rate MAY rule); base: 6 hits | `receipts/map_stage_grep_{head,base}.txt` |
| `tb/pp_top` (`make`, five builds) | rc 0, **10390 checks: 10390 PASS, 0 FAIL** (9918 + 20 + 178 + 218 + 56); D3KR 1000, D3V 11, HZ 177, ST 19 | `receipts/pp_top_head.log` |
| `tb/pp_top` `--cut-seed 0xD3C0FFEE` (README claim "`--cut-seed S` reruns one") | rc 0; D3KR 39 checks, one seed per each of the 8 types (cfg, rate, clks, fmti, fmto, ptof, name, bind) | `receipts/d3kr_cut_seed_probe.log` |
| `tb/nvm_port` (`make`) | rc 0, 1219 checks, 0 FAIL | `receipts/nvm_port_head.log` |
| `tb/timer_map` (`make`, also includes the top) | rc 0, 1360 checks, 0 FAIL | `receipts/timer_map_head.log` |
| `scripts/lint_hdl.sh` | rc 0, 41/41 LINT OK | `receipts/lint_hdl_head.log` |
| `make check` + `gen_matrix.py --check` | rc 0: 41 mermaid + 18 wavedrom, 1114 links, 115 REQ / 17 GAP, 94 rows 0 untested, 28 parameters | `receipts/docs_gates_head.log` |
| Tracked mutation patches, `git apply --check` | 224 of 224 apply (64 target a file round 2 changed) | `receipts/mutation_patches_apply_head.txt`, `scripts/check_patches_apply.sh` |
| c8 patches (published evidence) | both 11 `@@` hunks, 7 `diff --git` files, every `+`/`-` line identical; PR body says 11 at :293 and :331, no "13 hunks" left | `receipts/c8_hunk_count.txt` |
| Comments 5969239148, 5969246536, 5969765075, 5969802215, 5969914780 | `updated_at == created_at` for each (none edited) | API read only |
| `make -C tb/nvm_port figures` | **not completed locally**: rc 124 twice (560 s under load, 590 s alone), a serial ~150-build driver longer than one foreground call; see Limits | `receipts/nvm_figures_head.timeout-*.log` |
| Clone integrity after all probes | HEAD and tree as above; `git status --porcelain --ignored` empty; index (mode, blob, path) == HEAD tree for all 501 files; every on-disk blob hash and mode matches; no gitlinks (no `.gitmodules`) | `receipts/clone_integrity.txt` |

Hosted CI at the exact head: workflow `hdl`, runs 37128429648 (push) and 37128432590 (pull_request). Last observed at 14:58:38Z (`receipts/hosted_runs_final_observation.txt`):
- `docs-gates` success, both runs;
- `portability` (yosys + sv2v elaborate every top) success, both runs;
- `suites`: still **in progress** in both runs. Steps 1 to 6 succeeded: lint plus every suite, and the SRP LeaveAll campaign. Step 7 (MAAP campaign) was running; steps 8 to 12 were pending (ADP, AECP deadline/hazard, AECP dispatch campaigns, matrix, nvm_port figures). Step 4, "Build Verilator", was skipped on a cache hit; that is a cached context, not a failure.

The hosted check is therefore **not yet green**. `receipts/hosted_runs.txt` and `hosted_checkruns.tsv` hold an earlier snapshot. At prior heads this workflow took 75 to 125 min, so the manager owns the final state.

## Round-1 findings at this head

| Round-1 item | Status | Evidence |
|---|---|---|
| R444-1 F1 = R445-1 F2 (MINOR, stale processor map-stage claims) | **RESOLVED** at every enumerated place: `protocol_processor_top.sv:779-782`, `KL_aecp_engine.sv:469-470`, `KL_aecp_nvm_writer.sv:94-97` and `:119-121`, `tb/pp_top/README.md:665`. The new texts are R445-1's verbatim. They agree with 07 §5.1 (save from the accepted phase-5 commit beat, restore after `restore_done_o`, judged against the restored formats) and with §5.2 ("the processor never writes or reads it"). The writer has no `0x60`/`0x70` record path. No logic change: see the netlist, preprocessing and ROM rows. **The class is not fully closed**: one further instance, outside the round-1 grep scope, is N-F1. | `exact_texts_head.txt`, `probe/*`, `map_stage_grep_*.txt` |
| R444-1 F2 = R445-1 F3 (MINOR, randomized cuts recorded as owed) | **RESOLVED.** R445-1's text is appended at `tb/nvm_port/README.md:1064-1067` and `:1348-1351`, both passages. Every factual element checks against `tb/pp_top/README.md:381-400` and the bench: 8 record types (both producers, binding `0x20` included), 32 standing seeds each, a real `rst_n`, and `--cut-seed S` (executed). The lead words "still owed", left in place by the prescribed append, are N-R1 (RESIDUE). | `pp_top_head.log`, `d3kr_cut_seed_probe.log` |
| R444-1 F3 = R445-1 F1 (MINOR, hunk count) | **RESOLVED** in the PR body (:293, :331: 11 hunks, 7 files, every `+`/`-` line identical) and by correction comment 5969802215; 5969239148 is unedited. The round-2 HANDOFF is not public, and the published round-1b archive (`HANDOFF.md:745`) still reads 13 by construction (a pending manager duty, below). | `c8_hunk_count.txt` |
| R444-1 R1 / R445-1 R1 (RESIDUE, gate 16 pending) | **RESOLVED.** "What remains" carries R445-1's exact text, and the round-1b (a)/(b) list ends "Ruled (b) on #83 (5969246536)." | PR body :236-238, :312 |
| R444-1 R2 / R445-1 R2 (RESIDUE, area) | **RESOLVED.** Item 12 is R445-1's exact text plus R444-1's 8x8 sentence. The figures match the STOP comment 5969239148 and the published `HANDOFF.md:590-591`. | PR body :221-224 |
| R445-1 R3 (RESIDUE, `tb/pp_top` growth) | **RESOLVED.** "HZ 176 to 177 and ST 18 to 19" is appended. 169 + 12 + 11 + 1000 + 1 + 1 = 1,194 = 10,362 − 9,168; the head run shows HZ 177 and ST 19. | PR body :151-153 |
| R444-1 S1, S2; R445-1 S1 to S3 (SUGGESTION) | Open by assignment, and listed in the PR body (Round 2 item 5). Not findings. | PR body :366-375 |

## Findings (this round)

### N-F1 - MINOR - Conformance, Tests, Docs - a fifth stale "map and name stages (not implemented yet)" claim

- **Where.** `tb/pp_top/sim_main.cpp:4250-4253`, the R21 banner. It reads: "The mark is a completion notification, not a persistence trigger: the saved-state contract's map and name stages (not implemented yet) select their records from the accepted live writes, and section D3 grades the scalar records."
- **Provenance.** Commit `39789f98`, the same commit as the engine banner that R444-1 F1 included as "older but inside the ruling's amendment scope". It is present at the base `ddb3119d:4198`.
- **Authority.**
  - Ruling 5967611704: maps are the integrator's.
  - 07 §5.1 (`07_memory_maps.md:559-589`) and §5.2 (`:629-631`): the D3 writer persists the user names (records `0x80` + ordinal); the processor never writes or reads `0x60`/`0x70`.
  - This PR's own `a1f5cd5` implemented the name stage, which is graded by D3N in the same bench.
- **Evidence.**
  - My whole-tree sweep (`git grep` for "not implemented yet", "map/name stage", "later stage", "lands in P4" and related phrases at the head; `receipts/stale_claim_sweep_head.txt`, 24 hits, each read) finds no other stale instance. The other hits are current-contract citations, or unrelated (the dispatch ROM, the operator's `NOT_IMPLEMENTED` row).
  - The round-1 verification grep did not reach it, because it was limited to `hdl/` and `tb/pp_top/README.md`.
- **Impact.**
  - The comment states that the processor's name stage is not implemented, which is false at this head.
  - It states that a processor map stage is pending, which contradicts the amended contract.
  - This is the same contract-status claim that both round-1 reviews graded MINOR as "not wording alone". It sits in the bench that grades the name stage and the cuts.
- **Required outcome.** A comment-only rewording, for example: "…The mark is a completion notification, not a persistence trigger: the D3 writer's name stage selects its records from the accepted live name write (`aecp_name_wr_o`, section D3N), the channel maps are the integrator's to persist (07 §5.1, the ruling on #83), and section D3 grades the scalar records." No logic change.
- **Verification.**
  - `git grep -nE -i "not implemented yet|map stage|later stage" -- hdl tb` finds nothing. At this head its only hit is `tb/pp_top/sim_main.cpp:4252`.
  - `tb/pp_top` stays at 10,390/10,390.
  - `make check` and `lint_hdl.sh` stay rc 0.

### N-R1 - RESIDUE - Docs, Tests - "still owed" lead words left before the "delivered" parenthetical

- **Where.**
  - `tb/nvm_port/README.md:1064`: "…so the randomized half is still owed (delivered at the top by …)";
  - `:1347`: "**The RANDOMIZED cut points `09_verification.md:56` asks for are still owed** on both sides: … (delivered at the top by …)".
- **What.**
  - The prescribed append is correct and complete, but the sentence now calls the same half both owed and delivered.
  - The PR body says "No randomized cut stays owed port-locally".
  - The coverage status itself (delivered by D3KR, this suite's cuts fixed) is stated correctly in the same sentence, so only the wording is at issue.
- **Exact fix.**
  - `:1064`: "so the randomized half is still owed" → "so the randomized half is not cut by this suite".
  - `:1347`: "**… asks for are still owed** on both sides" → "**… asks for are not cut by this suite** on either side".

### N-R2 - RESIDUE - Docs (PR body) - wrong line figures in "Seen, not fixed in this round"

- **Where.** PR body lines 395-398.
- **What.**
  - `frame_ok_w` (declaration and assign) is at `:546-549` from the name stage (`a1f5cd5`) through `c066dd83`, and at `:549-552` at the head. No commit puts it at `:550-553`.
  - The binding shadow's instance is at `:2727` at the lane base `ddb3119d` and at `:2725` at `main` `f4167536`. The body's "`:2727` on `main`" matches neither the current `main` nor states which `main` it means.
  - Evidence: `receipts/nvm_port_readme_citations.txt`.
- **Exact fix.** "(`frame_ok_w`, right at `ddb3119d`, at `:546-549` since the name stage and `:549-552` at the head) and `protocol_processor_top.sv:2714` (the binding shadow's instance, at `:2727` at `ddb3119d`, `:2725` at `main` `f4167536`, `:2730` at the head)".

### N-R3 - RESIDUE - Docs - two stale line citations in `tb/nvm_port/README.md:100-101`

- **What.** The PR body records these as seen and not fixed.
  - `KL_aecp_nvm_writer.sv:482-485` was right at `ddb3119d`. This PR's name stage moved it to 546-549, and round 2's three added comment lines moved it to 549-552.
  - `protocol_processor_top.sv:2714` was already stale at the base; the instance is at 2730 at the head.
  - These are pointers in prose; no measurement, test or claim depends on them, and the figures gate does not check them.
- **Exact fix.** `:100` "`hdl/aecp/KL_aecp_nvm_writer.sv:482-485`" → "`hdl/aecp/KL_aecp_nvm_writer.sv:549-552`"; `:101` "`hdl/top/protocol_processor_top.sv:2714`" → "`hdl/top/protocol_processor_top.sv:2730`". If N-F1's fix lands in the same round and moves no line in those two files, these stay valid.

## Lens evidence

- **Conformance.**
  - The four HDL comment replacements and the README replacement state the amended D3 contract exactly as 07 §5.1/§5.2/§5.3 and ruling 5967611704 do.
  - The integrator remains the owner of `0x60`/`0x70`; the processor's roll-back still covers its two AECP stores only (`restore_rb_o` banner unchanged and consistent).
  - The closes lines and acceptance judgments of round 1 are untouched by a comment-only round.
  - **Unclean**: N-F1, a remaining contract-status claim against the ruling.
- **RTL.**
  - All 28 changed HDL lines are comments.
  - The comment-stripped preprocessing of all three files is identical.
  - The elaborated netlist of the top is identical once the simulator-generated assertion line numbers are masked; those strings are simulation-only text and not hardware.
  - The ROMs are byte-identical, lint is 41/41, and the hosted off-vendor elaboration (portability) is green at the head.
  - **Clean.**
- **Robustness.**
  - No behavioural change is possible from this delta (netlist and ROM equality).
  - All 224 mutation patches still apply despite the +1/+3 line shifts.
  - The single-seed rerun works as the README now documents.
  - Clone bytes, modes and index were restored and verified.
  - **Clean.**
- **Tests.**
  - `tb/pp_top` 10,390/10,390 across five builds, `tb/nvm_port` 1,219, `tb/timer_map` 1,360, with every count as recorded at `c066dd83`.
  - The appended README text matches the D3KR bench.
  - The nvm_port figures gate was not completed locally (see Limits). The new text adds no `N of M`/`PASS, FAIL` figure shape.
  - **Unclean**: N-F1 sits in the bench and misstates what it grades.
- **Docs.**
  - `make check` and the matrix check are rc 0, and all prescribed texts are verbatim.
  - The PR body carries the hunk-count correction and all five residue items, and the suggestions are listed as open.
  - N-R1 to N-R3 are RESIDUE.
  - **Unclean**: N-F1.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (N-F1) | ruling 5967611704; 07 §5.1/§5.2/§5.3; the five replaced comments; `restore_rb_o` banner; whole-tree stale-claim sweep; `tb/pp_top/sim_main.cpp:4250-4253` | R444-2 | `5960d8fc7e4f6ef2d7551bb224154ef2c265d894` |
| RTL | CLEAN | `git diff -U0 -- hdl` (28 comment lines); `-E -P` preprocess ×3; elaborated top netlist base vs head; ROM regeneration; `lint_hdl.sh` 41/41; hosted portability | R444-2 | `5960d8fc7e4f6ef2d7551bb224154ef2c265d894` |
| Robustness | CLEAN | netlist/ROM equality; 224/224 mutation patches; `--cut-seed` probe; clone integrity | R444-2 | `5960d8fc7e4f6ef2d7551bb224154ef2c265d894` |
| Tests | UNCLEAN (N-F1) | `tb/pp_top` 10,390; `tb/nvm_port` 1,219; `tb/timer_map` 1,360; D3KR text vs bench; `tb/pp_top/sim_main.cpp` R21 banner | R444-2 | `5960d8fc7e4f6ef2d7551bb224154ef2c265d894` |
| Docs | UNCLEAN (N-F1; N-R1 to N-R3 RESIDUE) | `make check`, `gen_matrix.py --check`; exact texts; both nvm_port passages; PR body at review; c8 patches; comments 5969802215 / 5969239148 | R444-2 | `5960d8fc7e4f6ef2d7551bb224154ef2c265d894` |

## Real limits

- **The `tb/nvm_port` figures gate was not completed here.** `measure_figures.py --check` is a serial driver of about 150 builds. Two attempts ended at the foreground bound (rc 124), one under shared load and one alone. Its hosted step (`suites` step 12) had not run when last observed. Round 2 adds no figure-shaped text to that README.
- **Hosted `suites` was still in progress at both runs** when last observed (14:58:38Z): steps 1 to 6 green, step 7 running, steps 8 to 12 pending. I did not see it complete.
- **I did not run** the full `run_suites.sh` bank, the mutation campaigns, the parent consumer set or any Yosys/builder bank. Those are the manager's banks; only the suites that include the changed modules were run, plus `nvm_port`.
- **The netlist comparison is the simulator's elaborated tree, not a synthesis netlist.** The hosted off-vendor elaboration is green at the head.
- **The round-2 HANDOFF.md is not public.** Only the PR body, the issue comments and the round-1b archive could be checked.
- Physical calibration NOT RUN; no hardware; field skips are not hardware proof.

## Pending manager duties

- Route N-F1 for a comment-only fix, and re-review that round.
- Carry N-R1, N-R2 and N-R3 with their exact fixes to the residue checklist.
- Accept the hosted `suites` jobs of runs 37128429648 and 37128432590 at the head, including the nvm_port figures step.
- Publish the round-2 HANDOFF/PR-BODY archive. The public archive's `HANDOFF.md:745` still reads 13 hunks, by construction.
- At the merge turn, build the final current-dev candidate (source base `ddb3119d`, live dev `bbf704ec`); it is distinct from this source validation.
- Track milan-fpga #643 (gate 16) before the second pin adoption.
- The open suggestions (R444-1 S1, S2; R445-1 S1 to S3) remain listed and are not part of this verdict.

R444-2 FINISHED
