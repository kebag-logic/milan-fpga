[R444] POSITIVE - exact head 6ca4ade8c296540b78ca5bec0d13a342fd567d12

# R444-3 internal independent review: processor issue #83 / PR #150 (lane P1), round 3

- **Exact head:** `6ca4ade8c296540b78ca5bec0d13a342fd567d12`, tree `d0b0b5e9aac1b91e2fd749c4826ef8ff20741290`.
- **Round-2 head:** `5960d8fc7e4f6ef2d7551bb224154ef2c265d894`. **Lane base:** `ddb3119dbbce59f81bf7a536a1ad90a20546edb2`.
- **Scope:** a delta review of round 3 (`5960d8fc..6ca4ade8`, commits `6b8df47` and `6ca4ade`). Round 3 changes comments and docs only. It is judged against:
  - R444-2 (PR #150 comment 5970346414);
  - R445-2 (5970928548);
  - the round-3 assignment (#83 comment 5970930857).
- **Review start:** PR #150 comment 5971135735.

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR is open.

Round 3 does what the assignment asked:
- **R21 banner.** R444-2's N-F1 text is in place verbatim at `tb/pp_top/sim_main.cpp:4250-4254`. Each of its claims checks against the tree and the ruling. The comment-stripped source is identical to round 2's, and a one-token control is caught. R444-2's grep now finds nothing.
- **nvm_port README.** Both "not cut by this suite" passages carry R444-2's exact texts. The two citations now point at the right lines: `KL_aecp_nvm_writer.sv:549-552` (`frame_ok_w`) and `protocol_processor_top.sv:2730` (the `KL_acmp_nvm_shadow` instance).
- **PR body.** The "Seen, not fixed" note carries R444-2's exact figures, and every one of them checks against history.

Status of the round-2 items:
- every round-2 finding and residue item is **RESOLVED**;
- nothing is retained;
- nothing is worsened.

My own sweep found one further wording defect next to N-R1's passage. It is recorded as RESIDUE N3-R1 with its exact fix, and it does not affect the verdict.

## Reconstruction (public sources only)

1. **Repository guidance.** The tree has no `AGENTS.md` or `CONTRIBUTING.md`. I used `README.md` and `docs/README.md`: the conventions, the single-source rules and `make check`.
2. **Issue #83.** The body, with its frozen acceptance 1 to 4, then every comment in order:
   - lane assignment 5965788915;
   - STOP M1 5967588719 and ruling (b) 5967611704: the maps are the integrator's;
   - REVIEW READY 5968343520;
   - round 1b 5968352676, STOP 5969239148 and ruling (b) 5969246536: gate 16 goes to milan-fpga #643;
   - the round-2 assignment 5969765075, correction 5969802215 and REVIEW READY 5969914780;
   - the **round-3 assignment 5970930857**;
   - REVIEW READY (round 3) 5971127613.

   I checked that 5969239148, 5969802215, 5970930857 and 5971127613 each have `updated_at == created_at`, so none was edited.
3. **Authorities:**
   - 07 §5.1, "Persisted vs volatile" with its "channel maps are the integrator's" paragraph (`docs/architecture/07_memory_maps.md:552-602`);
   - 07 §5.2 and §5.3;
   - 02 §8 (`aecp_name_wr_o` at `02_interfaces.md:674`; "each is triggered by its accepted live write, never by a mark" at `:680-683`);
   - the writer banner (`KL_aecp_nvm_writer.sv:119-133`);
   - 09 F09.3, the NVM row (`09_verification.md:56`);
   - the D3N and D3KR sections in `tb/pp_top/README.md`.
4. **Diff and history.** `git diff 5960d8fc..6ca4ade8` (2 files, +15/−14; `receipts/round3_delta.diff`), within `ddb3119d..6ca4ade8` (34 commits).
5. **Public evidence:** `kebag-logic/milan-fpga@3a657083 review-evidence/ppP1-r1`. It is the round-1 author archive: MANIFEST, HANDOFF, PR-BODY and four parent patches. It holds no receipts from the manager's banks at this head (see Limits).
6. **Prior public reviews.** R444-2 and R445-2 were read only after my own pass over the round-3 diff was complete. That pass covered:
   - the banner claims against the RTL, 02 and 07;
   - the citations against the RTL at every relevant revision;
   - the comment-stripped comparison;
   - the PR body's figures.

## Executed evidence (at the exact head unless stated)

**Tool and build setup.**
- The simulator is the scoped pinned wrapper: `Verilator 5.050 2026-07-01 rev v5.050`, wrapper sha256 `905795b9…e92f` (`receipts/tool_identity.txt`).
- Builds ran from `git archive` extractions and from a local history-bearing clone, both under `scratch/`.
- Concurrent jobs went through a job-capping wrapper (`scripts/verilator-capj.sh`): 8 + 6 + 2, at most 16 parallel jobs.

| What | Result | Receipt |
|---|---|---|
| Round-3 delta | `tb/pp_top/sim_main.cpp` +4/−3 (one comment block); `tb/nvm_port/README.md` +11/−11 (three re-wrapped passages, so no line moves in that file). **No `hdl/` file, generator, ROM input, Makefile, script or patch changed** | `receipts/round3_delta.diff`, `round3_delta.diff.stat`, `round3_log.txt` |
| Comment-stripped token stream of `tb/pp_top/sim_main.cpp` (`g++ -fpreprocessed -E -P`, whitespace collapsed), `5960d8fc` vs head | **IDENTICAL** (sha256 `2d346ffd…44bc` for both, 417,502 bytes). Control: one token changed on the code line after the banner (`row(0, 3, 3)` → `row(0, 3, 4)`) is **CAUGHT** | `receipts/strip_compare.txt`, `scripts/strip_compare.sh` |
| Exact texts (whitespace and comment markers normalised): R444-2 N-F1, N-R1 ×2, N-R3 ×2 present, and every replaced text absent | **10 of 10 OK** | `receipts/exact_texts_head.txt`, `scripts/check_exact_texts.py` |
| R444-2's verification grep `git grep -nE -i "not implemented yet\|map stage\|later stage" -- hdl tb` | head: no hit (rc 1). `5960d8fc`: its one hit was `tb/pp_top/sim_main.cpp:4252` | `receipts/r444_2_grep.txt` |
| Banner claims vs the tree | `aecp_name_wr_o` is a top output (`protocol_processor_top.sv:769`, wired from the engine's `name_wr_o` at `:3847`). The writer takes a name's trigger from the accepted live name-lane write (`KL_aecp_nvm_writer.sv:130-133`), and the maps are the integrator's there (`:119-121`). D3N exists (`tb/pp_top/README.md:294`; `D3NamePhase` at `sim_main.cpp:10805`). 07 §5.1 says "The **channel maps are the integrator's**" (the ruling on #83). All hold | this report |
| Citations `frame_ok_w` and the shadow instance, at each revision | writer `482-485` (ddb3119d, f4167536), `546-549` (53e1474b, c066dd83), `549-552` (5960d8fc, head); shadow `2727` (ddb3119d), `2725` (f4167536), `2731`, `2729`, `2730` (5960d8fc, head). README `:100-101` and the PR body's "Seen, not fixed" figures match exactly | `receipts/citations_and_pr_body.txt` |
| PR #150 body at review (head `6ca4ade8`) | R444-2 N-R2's exact text present; no `:550-553` left; "What remains" no longer lists the citations. Round 3 section: line range `:4250-4254` correct, the "no line moves" claim correct (+11/−11 re-wrap), suggestions listed as open, "Neither round-2 review adds one" correct | `receipts/pr150_body_at_review.md` (sha256 `cd41674d…598a`) |
| Line shift in `sim_main.cpp` (+1 after `:4254`) | no line citation into `tb/pp_top/sim_main.cpp` anywhere in the tree; both tracked patches into that file have hunks at `:932` and `:1917`, above the shift; no driver or plant anchors on the replaced banner text | this report |
| Tracked mutation patches, `git apply --check` | **224 of 224 apply** | `receipts/patches_apply_head.txt`, `scripts/check_patches_apply.sh` |
| `make -C tb/pp_top run` (five builds) | rc 0, **10,390 checks: 10,390 PASS, 0 FAIL**; D3V 11, D3KR 1,000 | `receipts/logs/pp_top.log` |
| `tb/pp_top` `--cut-seed 0xD3C0FFEE` (the nvm_port README's "`--cut-seed S` reruns one") | rc 0, D3KR 39 checks, 0 failures, one seed across all 8 record types | `receipts/logs/cut_seed_probe.log` |
| `make -C tb/nvm_port run` | rc 0, 1,219 checks, 0 FAIL | `receipts/logs/nvm_port_run_and_figures_in_archive_extraction.log` |
| `make -C tb/nvm_port figures`, in a history-bearing local clone at the head | rc 0: "all measured figures agree with the tree" (154 rows `[ok ]`) | `receipts/logs/nvm_figures_git.log` |
| (same gate, first attempt in a `git archive` extraction) | rc 2. Every measured row was `[ok ]`, but the gate's git-form pins read `dc354be~1` and `62d96d6~1`, which an extraction without `.git` cannot provide. This was environmental, and the history-bearing re-run above is rc 0. A first in-clone attempt hit the foreground bound (rc 124) and was re-run detached | same log as `nvm_port run` |
| `./scripts/lint_hdl.sh`, `make check`, `scripts/gen_matrix.py --check` | rc 0: 41/41 LINT OK; 41 mermaid + 18 wavedrom; 1,114 links; 115 REQ / 17 GAP; 94 rows, 0 untested; parameters 28/28/28 | `receipts/logs/lint_docs.log` |
| Clone integrity after all probes | HEAD and tree exact; `status --porcelain --ignored` empty; index tree equals the HEAD tree; 501 entries, every blob re-hashes and every mode matches; **no gitlinks** (no `.gitmodules`) | `receipts/clone_integrity.txt`, `scripts/clone_integrity.sh` |

**Hosted CI at the exact head** (read-only). Workflow `hdl` has two runs: 37137368226 (push) and 37137370108 (pull_request). Last observed in `receipts/hosted_jobs_final.txt`:
- `docs-gates` and `portability` show success in both runs.
- `suites` is **in progress** in both runs:
  - step 5 (lint plus every suite) succeeded;
  - step 6 (SRP campaign) was running;
  - steps 7 to 12 were pending, the nvm_port figures step included.
- Step 4 (simulator build) was skipped on a cache hit. That is a cached context, not an executed build.

The hosted check is not yet complete, and the manager owns hosted acceptance.

## Round-2 items at this head

| Round-2 item | Status | Evidence |
|---|---|---|
| **R444-2 N-F1** (MINOR; Conformance, Tests, Docs): the R21 banner claimed that the "map and name stages (not implemented yet)" are pending | **RESOLVED** | `sim_main.cpp:4250-4254` is R444-2's text verbatim. Each claim holds against the RTL, 02 §8, 07 §5.1 and ruling 5967611704. The change is comment-only (stripped streams identical, control caught). The grep is clean, and `tb/pp_top` is 10,390/10,390 |
| **R444-2 N-R1** (RESIDUE): "still owed" lead words | **RESOLVED** | `tb/nvm_port/README.md:1064` and `:1347-1348` carry R444-2's exact texts, and the D3KR parenthetical is unchanged word for word. An adjacent "outstanding" is the new N3-R1 (RESIDUE) |
| **R444-2 N-R2** (RESIDUE): PR-body line figures | **RESOLVED** | PR body Round 2 "Seen, not fixed" carries R444-2's exact figures, each verified at its revision, and adds "Fixed in Round 3." |
| **R444-2 N-R3 = R445-2 R1** (RESIDUE): `tb/nvm_port/README.md:100-101` citations | **RESOLVED** | `:549-552` and `:2730`, both checked at the head; no `hdl/` line moved this round |
| **R445-2 R2** (RESIDUE): PR body "`:550-553` since the name stage" | **RESOLVED** | no `550-553` remains; the text now gives `:546-549` since the name stage and `:549-552` at the head (R444-2's superset text) |
| R444-1 S1, S2; R445-1 S1 to S3 (SUGGESTION) | open by assignment, not findings | listed in PR body Round 2 item 5 and Round 3 item 3 |

## Findings (this round)

No BLOCKER, MAJOR or MINOR.

### N3-R1 - RESIDUE - Docs, Tests - "outstanding" still precedes the reworded randomized-cut sentence

- **Where.** `tb/nvm_port/README.md:1061-1062`: "…names its gaps. The other outstanding item is the same: `09_verification.md:56` sets the bar as … so the randomized half is not cut by this suite (delivered at the top by `tb/pp_top` section D3KR, …)".
- **Authority / evidence.**
  - This is the residual of N-R1's class: a word calls the randomized cuts outstanding inside the sentence that says they are delivered at the top.
  - Round 3 replaced "still owed" exactly as prescribed, but this word sits one line above the prescribed span. It dates from `4448945`.
  - The coverage status itself is stated correctly in the same sentence: delivered by D3KR (1,000/1,000 at the head), with this suite's cuts fixed.
- **Impact.** Wording only:
  - no figure, measurement, test, code, generated artifact, conformance or clause claim changes;
  - the figures gate is rc 0 with the text as is;
  - no privacy rule is touched.
- **Required outcome (exact fix).** In `:1061-1062`, change "The other outstanding item is the same:" to "The other port-local gap is the same:".
- **Verification.** `grep -n 'outstanding item is the same' tb/nvm_port/README.md` finds nothing, and `make -C tb/nvm_port figures` stays rc 0.

## Lens evidence

- **Conformance: CLEAN.**
  - The banner now states the contract as amended by ruling 5967611704: the processor's name stage saves from `aecp_name_wr_o`'s accepted write (D3N), and the maps are the integrator's (07 §5.1).
  - It agrees with 02 §8's "triggered by its accepted live write, never by a mark" and with the writer banner `:119-133`.
  - No contract-status claim of a processor map stage remains (grep rc 1).
  - A comment- and docs-only round moves no acceptance line, so round 1's acceptance evidence carries.
- **RTL: CLEAN.**
  - No `hdl/` byte changed this round.
  - The two moved RTL citations point at the declared lines: `frame_ok_w` at `KL_aecp_nvm_writer.sv:549-552`, and `KL_acmp_nvm_shadow #(` at `protocol_processor_top.sv:2730`.
  - Lint is 41/41, and hosted portability succeeded at the head.
- **Robustness: CLEAN.**
  - No behaviour change is possible: the comment-stripped bench is identical, with the control caught, and no RTL or generator changed.
  - All 224 mutation patches apply despite the +1 shift in `sim_main.cpp`.
  - The `--cut-seed` rerun works as documented.
  - Clone bytes, modes and index were verified after the probes.
- **Tests: CLEAN.**
  - `tb/pp_top` 10,390/10,390 (D3KR 1,000, D3V 11); `tb/nvm_port` 1,219/0; the nvm_port figures gate is rc 0.
  - No test, driver or plant anchors on the changed text.
  - N3-R1 is RESIDUE.
- **Docs: CLEAN.**
  - Every prescribed text is verbatim (10/10).
  - `make check` is rc 0 (1,114 links) and `gen_matrix.py --check` is rc 0.
  - The PR body's Round 3 section is accurate: line range, re-wrap claim, figures, suggestions.
  - N3-R1 is RESIDUE and goes to the checklist.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ruling 5967611704; round-3 assignment 5970930857; 07 §5.1/§5.2/§5.3; 02 §8 (`:674`, `:680-683`); writer banner `:119-133`; `tb/pp_top/sim_main.cpp:4247-4257`; R444-2 grep | R444-3 | `6ca4ade8c296540b78ca5bec0d13a342fd567d12` |
| RTL | CLEAN | `git diff 5960d8fc..6ca4ade8 -- hdl` (empty); `KL_aecp_nvm_writer.sv:549-552`; `protocol_processor_top.sv:769, 2730, 3847`; `lint_hdl.sh` 41/41; hosted portability | R444-3 | `6ca4ade8c296540b78ca5bec0d13a342fd567d12` |
| Robustness | CLEAN | comment-stripped compare with control; 224/224 patch applies; `--cut-seed` rerun; clone integrity | R444-3 | `6ca4ade8c296540b78ca5bec0d13a342fd567d12` |
| Tests | CLEAN (N3-R1 RESIDUE) | `tb/pp_top` 10,390; `tb/nvm_port` 1,219; nvm_port figures gate rc 0; anchor and citation sweep into `sim_main.cpp` | R444-3 | `6ca4ade8c296540b78ca5bec0d13a342fd567d12` |
| Docs | CLEAN (N3-R1 RESIDUE) | `tb/nvm_port/README.md:97-103, 1056-1067, 1344-1351`; PR #150 body at review; exact-text check; `make check`; `gen_matrix.py --check` | R444-3 | `6ca4ade8c296540b78ca5bec0d13a342fd567d12` |

## Real limits

- **Banks not run here.** I did not run the full `run_suites.sh` bank, the mutation campaigns, the parent consumer set, the Yosys/builder banks or OOC area. They are not allowed in this review, and they are the manager's.
  - This round changes no logic, so those results carry from the prior heads.
  - The manager's statement that its source static/builder and native banks passed at this head was not checkable from the public evidence tree. `3a657083 review-evidence/ppP1-r1` is the round-1 author archive only, and I found no bank evidence comment for this head on #83 or PR #150.
- **Hosted `suites` was still in progress at both runs** when last observed. Steps 1 to 5 were green, step 6 was running, and steps 7 to 12 were pending. I did not see it complete.
- **The round-3 HANDOFF.md and the current parent patches are not public.** The author's statement that the four parent patches are unchanged rests on the absence of any patch or `hdl/` change in this delta, not on reading the patches.
- **The nvm_port figures gate needs git history.** It fails in a bare source extraction (its git-form pins), and it passes in a history-bearing clone at the head.
- **Hardware.** Physical calibration NOT RUN; no hardware; field skips are not hardware proof.

## Pending manager duties

- Carry RESIDUE N3-R1, with its exact fix, to the residue checklist.
- Accept hosted CI at the head: the `suites` jobs of runs 37137368226 and 37137370108, including the campaign and nvm_port figures steps.
- Publish the source static/builder and native bank receipts at this head, and the round-3 HANDOFF/PR-BODY archive.
- At the merge turn, build the final current-dev candidate: source base `ddb3119d`, live dev `bbf704ec`. Run the consumer bank with `parent-adoption-c8-bbf704ec.patch` and then the p2 successor, and record gate 16 against milan-fpga #643. This is distinct from the source validation above.
- The five open suggestions stay listed and are not part of this verdict. Merge still requires two independent positive reviews and the full completion bar.

R444-3 FINISHED
