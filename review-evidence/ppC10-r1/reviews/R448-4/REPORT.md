[R448] POSITIVE - exact head 39298e03aa53d5f82c7485b8d12d2b69a47b0d55

# R448-4: independent internal review of PR #149 (lane C10; issue #25), body-only re-review

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #149.
- Exact head: `39298e03aa53d5f82c7485b8d12d2b69a47b0d55`, tree `7f3b4639ee70ad34c567f4df4cc9fec4c8172780`. This is the same commit and tree as R448-3. The source is unchanged.
- Source base: `f4167536d358c996f4e1b70b875879c1651f85d3`.
- Review start: PR #149 comment 5973954162.
- Role: internal independent reviewer, cleared context, own detached clone. The clone is byte-exact before and after the probes (`receipts/clone_integrity_pre.txt`, `receipts/clone_integrity_post.txt`).
- Scope: the manager edited only the PR body, to address R448-3 F1. This round checks the edit against my R448-3 receipts and checks that no other byte changed. The code, the tests and the merge were found sound at this head by R448-3 and R449-3.

## Verdict

**POSITIVE. There is no open BLOCKER, MAJOR or MINOR, and no RESIDUE.**

- **The body edit.** It inserts one paragraph-opening sentence at body line 48 and nothing else. The diff against my round-3 snapshot (`author-r3/PR-BODY.md`, sha256 `55eef4af…`) is that sentence plus the trailing newline the CLI adds (`receipts/body_diff_r3_vs_live.diff`).
- **Each claim in the sentence holds:**
  - The "this head" column was measured at `b6f17f2`.
  - Every rc and every named module reproduce at `39298e03`.
  - The `module automatic` row gives `all.v:20859` at the merge.
  - The `all.v` syntax plant moves to a correspondingly later line (+110).
  - The shift comes from P1's sources, which precede these modules in `all.v`.
- **R448-3 F1 is RESOLVED**, through its second permitted outcome: the body states the revision the excerpts were measured at, and that `all.v` line numbers move with the merge.
- **R449-3 R1 (RESIDUE, the same defect) is RESOLVED** in substance, though not by its exact header wording. See §3.

## 1. Reconstruction

1. **Contributor rules.** The processor has no `AGENTS.md` or `CONTRIBUTING.md`. I re-applied the parent's AGENTS.md rules (reading order, five lenses, severities) as used in R448-3, together with the owner's RESIDUE rule of 2026-10-02. I also used the processor's `docs/README.md` conventions.
2. **Frozen scope.** Issue #25's acceptance is unchanged:
   - every declared module is a top;
   - the gate goes red on a broken new top;
   - a failure names its module;
   - the RAMB36E1 assertion is unchanged.

   Since R448-3, the only new public items are the R448-3 verdict (5973750262), the R449-3 verdict (5973952340), this round's start comment, and the issue's `REVIEW READY 39298e03` (5973148371). No scope decision changed.
3. **Diff and history.** The head is the R448-3 head. `git diff f4167536..39298e03` is the delta R448-3 reviewed in full. No commit was added, and the PR's head SHA is still `39298e03`.
4. **Public evidence.** `milan-fpga@2a54253e:review-evidence/ppC10-r1` holds `MANIFEST.json` and `author/` (the round-1 HANDOFF, PR-BODY and the c8, p2 and c10 adoption patches). It has no round-4 items, which is consistent with a body-only change. Since R448-3 there are no new manager evidence comments on #25 or #149.

## 2. Independent pass

### The body edit (Docs)

- `receipts/pr_body_r3_snapshot.md` is the round-3 body (sha256 `55eef4af4b05e1074d777f122a04f5cb4db5cdefb84585f0a1db880be2f8e9bf`). R448-3 found this equal to the then-live body, apart from one CLI trailing newline.
- `receipts/pr_body_live_39298e03.md` is the live body, fetched read-only.
- `diff` gives exactly two hunks:
  - **48c48:** the sentence is inserted after "**Red on a broken new top, naming it.**". The rest of line 48 ("Each case is a scratch copy. Unless stated") is unchanged.
  - **556a557:** one trailing newline.
- The word-level diff has no deletion. Every other byte of the body is identical, including all tables, figures and citations.

### Verification of each claim, against R448-3 receipts and re-runs at this head

| Claim in the new sentence | Evidence | Result |
|---|---|---|
| The column was measured at `b6f17f2`, before the merge of `c4cb84ff` | R448-3 `receipts/line_shift/r3-auto-split.log`: a `b6f17f2` tree gives `all.v:20749`, the body's figure. Round 3 changed only `syn/yosys/run.sh`, so `all.v` is the same at `cd08ca7` and `b6f17f2`, and the body's syntax figure `20318` belongs to that pre-merge layout | holds |
| Every rc and every named module reproduce at `39298e03` | I re-ran the 12 head census cases (`run_census_cases.sh`) and the 24 gate cases (`run_gate_cases.sh`), unchanged from R448-2/3, at this head (`receipts/census/`, `receipts/gate_probes/`). Every rc equals R448-3's (`census_vs_r3.txt`, `gate_probes_vs_r3.txt`). The verdict lines are byte-equal in 35 of 36 cases. The one DIFF is `h-malloc-emptyfile`, whose argument is a path that differs by construction (rc 2 in both). Each table row checked: `KL_srp_top` then `protocol_processor_top`; `KL_pp_dispatch`, `KL_pp_dispatch_fifo`, `protocol_processor_top`; two faults give four tops named and `parsed 4 time(s)`; the census messages for the dropped and bogus `tops` entries; the attributed module clean in `tops` gives rc 0 and 43 OK; `c-attr-own-top` names `KL_r448_attro`; `` `ifdef `` gives rc 0 and 42 OK | holds |
| At `39298e03` the `module automatic` row reports `all.v:20859` (not 20749) | `receipts/census/c-auto-split.log`: `YOSYS FAIL all.v in module KL_r448_auto: all.v:20859: ERROR: syntax error, unexpected TOK_AUTOMATIC, expecting TOK_ID`. This is identical to R448-3's `line_shift/h-auto-split.log` | holds |
| The `all.v` syntax plant reports a correspondingly later line | `receipts/gate_probes/h-allv-syntax.log` gives `all.v:20441` (R448-3: 20441 at this head, 20331 at `cd08ca7`). `receipts/allv_shift_attribution.txt`: lines 10393-21275 of `b6f17f2`'s `all.v` are byte-identical to lines 10503-21385 at the head. That region holds all of `KL_srp_top` (head 19356-20441) and the planted `hdl/top` module, so any plant inside them moves by exactly +110. The author's 20318 becomes 20428 | holds |
| Because P1's sources precede these modules in `all.v` | `receipts/allv_shift.txt` and `allv_shift_attribution.txt`: every merge hunk before `KL_srp_top` lies in head lines 4585-10502, in `KL_aecp_*` modules. Relative to `b6f17f2`, the merge's `hdl/` delta is only P1's `KL_aecp_desc_store.sv`, `KL_aecp_engine.sv` and `KL_aecp_nvm_writer.sv`, plus the top's port comments. The top's changed lines (head 21386-21401) come after the cited lines and do not move them | holds |
| "(R448-3 F1)" | the finding this answers | correct reference |

### Same-tree sanity at this head

- The clean Yosys gate, from a `git archive` of the head (`receipts/runs/gate-head.log`), is rc 0:
  - allocator `/usr/lib/libjemalloc.so.2`;
  - 42 `YOSYS OK`, and `YOSYS 42 tops, all.v parsed 1 time(s)`;
  - `YOSYS XILINX OK  KL_aecp_engine`;
  - 35.3 s, with a peak RSS of 0.8 GB.
- `scripts/lint_hdl.sh` with the pinned Verilator 5.050: rc 0, 41/41 `LINT OK` (`receipts/runs/lint_hdl.log`).
- Hosted at the exact head, read only (`receipts/hosted_checks_39298e03.txt`, `receipts/hosted_suites_steps.txt`):
  - **Push run 37151399092:** `docs-gates`, `portability` and `suites` all succeeded. `suites` executed every step: lint and every suite, the SRP, MAAP, ADP, AECP hazard and AECP dispatch campaigns, the matrix, and the nvm_port figures. Its only skipped step is "Build Verilator v5.050", a cache hit, which is not a test.
  - **PR run 37151403162:** `docs-gates` and `portability` succeeded. `suites` had passed every step through the matrix, and its "nvm_port README figures" step was still in progress when read (2026-10-03 22:09 UTC).

## 3. Prior public findings at this head (read after the independent pass)

| Finding | Severity | Status at `39298e03` | Evidence |
|---|---|---|---|
| R448-3 F1: the "this head" column quotes pre-merge `all.v` line numbers | MINOR | **RESOLVED** | Body line 48 states the revision (`b6f17f2`), that line numbers move with the merge, and the merge's figure for the `module automatic` row (20859). The syntax row is described as "correspondingly later", which is exact (+110, uniform shift). This is the second required outcome of F1. Verification as F1 specified: `c-auto-split` re-run gives `all.v:20859` |
| R449-3 R1: the same defect | RESIDUE | **RESOLVED** in substance | R1's exact fix was to relabel the header at body line 52. The header still reads "this head", but the sentence directly above it now gives the column's revision and the line-number caveat. No reader is left with an unexplained figure |
| R448-3 S1: the stale-entry message predates the scope change (`run.sh:184`) | SUGGESTION | open (optional), unchanged | the source is unchanged |
| R448-3 S2: a yosys that rejects the list command is reported as a parse failure (`run.sh:281-285`) | SUGGESTION | open (optional), unchanged | the source is unchanged |
| R449-3 S1 = R449-2 S1: the parent's census reads `.sv` text | SUGGESTION | open, out of scope (parent follow-up) | listed in the body under "Not done here" |
| R449-3 S2 = R449-2 S2: the `elab_bounds.sh` yosys leg never runs hosted | SUGGESTION | open | the workflow is unchanged |
| R448-2 F1, R449-2 F1, and the round-1 findings | | still **RESOLVED** | R448-3 established this at this exact head. The census, attributed-header and `automatic` cases re-run here give the same rc and verdict lines |

No finding is worsened, and no new finding arises.

### S3: SUGGESTION. Docs. Optionally relabel the column header too (PR body line 52)

If the author touches the body again, the header could carry the revision itself, so the table reads correctly when quoted alone. For example: `this PR (excerpts at b6f17f2; all.v lines move with each merge)`, as R449-3 R1 proposed. This is not required, since line 48 already states it.

## 4. Lenses

- **Conformance: CLEAN.**
  - The edit changes no acceptance claim.
  - #25 bullets 1-3 re-run at this head: 42 tops elaborated, every planted fault red and named, and the census rows reproduce.
  - #25 bullet 4: XILINX OK.
  - The #17 and #37 evidence is unchanged from R448-3 at the same tree.
- **RTL: CLEAN.**
  - The tree is identical to R448-3's.
  - Lint is 41/41, and the gate elaborates 42 tops and passes XILINX at this head.
  - The P1 `hdl/aecp` delta accounts for the whole `all.v` shift.
- **Robustness: CLEAN.**
  - All 36 census and gate fault cases (including the allocator cases) reproduce rc and verdict lines against R448-3.
  - S1 and S2 are optional.
- **Tests: CLEAN.**
  - No test changed.
  - R448-3's suite and campaign receipts (33 suites, 1,021,449 checks; dispatch 40/40; D3 P1 arms 23/23; notify 40/40) cover this tree.
  - Hosted push-run `suites` succeeded at the exact head.
- **Docs: CLEAN.**
  - The edit is the only change, and each of its claims is verified above.
  - R448-3 F1 and R449-3 R1 are resolved. S3 is optional.

## 5. Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #25 bullets 1-4 by re-run at this head (census 12, gate 24, clean gate); body claims vs acceptance; R448-3 receipts for #17 and #37 at the same tree | R448-4 (R448-3 for the unchanged #17/#37 runs) | 39298e03aa53d5f82c7485b8d12d2b69a47b0d55 |
| RTL | CLEAN | tree equals R448-3's; `lint_hdl.sh` 41/41; clean gate 42 OK + XILINX; `all.v` at `b6f17f2` vs head (shift attribution to P1's `hdl/aecp`) | R448-4 | 39298e03aa53d5f82c7485b8d12d2b69a47b0d55 |
| Robustness | CLEAN | 36 fault/census/allocator cases vs R448-3, rc and verdict lines | R448-4 | 39298e03aa53d5f82c7485b8d12d2b69a47b0d55 |
| Tests | CLEAN | R448-3 suite and campaign receipts at the same tree; hosted check runs and steps at the exact head (read only) | R448-3 + R448-4 | 39298e03aa53d5f82c7485b8d12d2b69a47b0d55 |
| Docs | CLEAN | full PR body diff vs the round-3 snapshot (one inserted sentence + trailing newline); each claim of the sentence vs receipts; red-proof table rows vs re-runs | R448-4 | 39298e03aa53d5f82c7485b8d12d2b69a47b0d55 |

## 6. Real limits

- This was a body-only round. I did not re-run the 33 suites, the campaigns, the parent consumer gates or the round-3 mechanism probes. They rest on R448-3 at this identical tree. Today's re-runs are the census, gate, clean-gate and lint runs above.
- I could not reproduce the author's exact `all.v` syntax plant (body `20318`). I verified that every line in its region moves by exactly +110, so the plant now sits at 20428. Mine is at 20441.
- The hosted PR run's `suites` job was still running its nvm_port figures step when read. The push run's `suites` had completed green.
- No Vivado or xvlog on this host. yosys 0.33 was not run locally; it is covered by the hosted `portability` jobs.
- Physical calibration NOT RUN. Field skips are not hardware proof. No hardware claim is made.

## 7. Pending manager duties

1. Confirm that the PR run's `suites` job (run 37151403162, job 111285888063) finishes green at the exact head. The manager owns hosted/act acceptance.
2. Build the final current-dev candidate at the merge turn (source base `f4167536`, live dev `5fabb46e`). This source-head review does not cover it.
3. At adoption, carry c8, then p2-p1 (`d3034e89`) in place of p2, then c10 (`55e62329`), and keep `check_rtl_source_lists.py --selftest` in the consumer set.
4. Close PR #26 at merge. Issue #151 keeps R449-1 S1, and R449-2/R449-3 S1 needs a parent follow-up.
5. Residue checklist: no RESIDUE from this review. R449-3 R1 is resolved by the line-48 sentence. S3 is optional.

## 8. Scripts and receipts

Every published file is listed in `MANIFEST.sha256`. The absolute packet path in one receipt is rewritten to `<packet>`.

- `scripts/`:
  - `r448-2/`: the round-2 probes, run unchanged. Their identity is in `receipts/probe_script_identity.txt`.
  - `compare_vs_r3.sh`: the rc and verdict-line comparison against round 3.
- `receipts/`:
  - `census/`, `gate_probes/`, and the round-3 comparisons `census_vs_r3.txt` and `gate_probes_vs_r3.txt`;
  - `runs/` (the clean gate and lint);
  - `allv_shift.txt`, `allv_shift_attribution.txt`;
  - `pr_body_r3_snapshot.md`, `pr_body_live_39298e03.md`, `body_diff_r3_vs_live.diff`;
  - `hosted_checks_39298e03.txt`, `hosted_suites_steps.txt`;
  - `clone_integrity_pre.txt`, `clone_integrity_post.txt`, `tool_identity.txt`, `probe_script_identity.txt`.

R448-4 FINISHED
