[R520] POSITIVE - exact head fe8294978dd306706d659dc06468d0c07d43ce3e

# R520-3: internal cleared-context review of PR #692 (issue #682)

POSITIVE. All five lenses were applied at the exact head and are CLEAN. No BLOCKER, MAJOR or MINOR finding is open. One RESIDUE and one retained SUGGESTION are recorded; neither affects the verdict or coverage.

- Reviewed head: `fe8294978dd306706d659dc06468d0c07d43ce3e`, tree `1d9982e2943098fd1003e069dc7df8cc210d98ca`.
- Source base and live dev: `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`.
- Delta under review:
  - round 3, `5428b044..cb359db3`: the CHANGELOG `2ad2f845` section and the baseline F worker-cap recipe text;
  - the manager's commit `cb359db3..fe829497`, which applies the exact fix for R520-2-F1.
- Baseline: R520-1 and R520-2 findings, and R521-1 POSITIVE at `5428b044`. R521-2 is VOID.
- No settled engineering was re-opened.

## Reconstruction

The review was rebuilt from public state only, in this order:

1. AGENTS.md and CONTRIBUTING.md.
2. docs/README.
3. The issue #682 body and its decisions:
   - the assignment (6018127147);
   - the round-2 ruling on #657 (6028334443);
   - the round-3 assignment (6043632388);
   - REVIEW READY 6044322927;
   - the manager's VOID note (6044571736).
4. Processor PRs #156, #159, #160, #161, #162 and #164: bodies and merge diffs in the pinned submodule.
5. The diff `e21c1ca0..fe829497` and its history.
6. The public evidence tree at `8d4e0732` (`review-evidence/682-r1`).
7. The exact-head hosted check runs.

Prior public findings on this PR were read only after this round's own pass and its ledger conclusions were complete.

## What changed since the last reviewed heads

- `git diff --name-only 5428b044 fe829497` lists exactly three files: `CHANGELOG.md`, `docs/reference/SUBMODULES.md` and `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`.
- No source, record, generated file or gitlink changed since `5428b044` (`receipts/verify_claims.log`).
- `cb359db3..fe829497` changes exactly two lines: `CHANGELOG.md:54` and `SUBMODULES.md:163`. Each now matches R520-2-F1's prescribed text verbatim.
- Both commits have one-line subjects, no body and no trailers.

## Claim-by-claim check of `CHANGELOG.md:44-71` (and `SUBMODULES.md:158-185`)

| Claim (line) | Result | Evidence |
|---|---|---|
| Pin carries processor PRs #156, #159-#162, #164 (`:47-48`) | TRUE | First-parent merges `ead80360..2ad2f845` are exactly 156, 159, 161, 160, 162, 164 |
| Counter spacing measured at grant (#148); later MAC stalls are a wire-gap limitation (`:49-50`) | TRUE | `KL_aecp_notify.sv` N_EMIT_WAIT refreshes `ctr_last_r[em_ctr_ix_r]` until the job retires. The PR #159 body says: "The stamp is taken at the frame's grant. A MAC that stalls a frame after its grant shortens the wire gap" |
| Harness finishes boundary-crossing frames, at most 2,048 cycles (`:51-52`) | TRUE | `tb/verilator/milan_dp/sim_nxn.cpp`: `c < cyc \|\| (!cur.empty() && c < cyc + 2048)` |
| C11 documents byte interfaces, TX backpressure and complete FCS-good RX frames (`:53-54`, `SUBMODULES.md:163`) | TRUE | The PR #156 diff of `02_interfaces.md` covers the byte faces, the `tx_ready_i` stall and the RX FIFO that passes only "complete, FCS-good frames" |
| No synchronous-reset credit to C11 (R520-2-F1) | TRUE | The PR #156 merge adds no reset-contract line. PR #157 (`b0a74196`, an ancestor of `ead80360`) adds "5. Reset: one input, `rst_n`, **synchronous and active low**". The PR #156 body says the same |
| SRP expiry precedes same-clock reception; Lv/LeaveAll finish MT; New/Join renew IN (`:55-56`) | TRUE | The PR #160 diff moves the expiry branch ahead of rLv/LeaveAll in both registrar FSMs; New/Join stays ahead (IN, timer cancelled) |
| Held DEREGISTER waits for the round boundary; later controllers keep notifications; contents unchanged, delivery later (`:57-59`) | TRUE | PR #161: `if (dh_v_r && !em_active_r)`. The body's "What remains" says the DEREGISTER reaches its controller later |
| Declarations precede use (#22); parent analysis budget has zero processor findings (`:60-61`) | TRUE | The PR #162 diff moves four declarations. `scripts/xvlog.budget` shows `section submodules: 0 finding(s)` with no `protocol-processor:` key |
| Domain/link-edge notification triggers gain tests (#42); parent owns mapping words (`:62-63`) | TRUE | PR #164 changes tests only (`tb/pp_top`, docs). Its body places msrp_mappings content outside the processor's scope |
| Processor top byte-identical to `ead80360`; no port/parameter/register adaptation (`:64-65`) | TRUE | `git diff --quiet ead80360 2ad2f845 -- hdl/top/protocol_processor_top.sv` returns 0. No parent register-map file is in the PR diff |
| Baseline F (`:66`) | TRUE | `syn/ooc/pp_resource_baseline.json` holds three endpoints. `AREA_BUDGET.md:102` and `234_PP_SHADOW_AREA_BASELINE.md:27-35` name combination F at processor `2ad2f845`. `pp_resource_gate.py check-baseline` passes all 3 endpoints |
| ROM ledger adds `2ad2f845` rows; both ROMs unchanged (`:67`) | TRUE | `syn/yosys/rom_digests.tsv:15-16` equal rows `:59-60` (`ead80360`). No `.hex`/ROM source changed between the pins |
| Capture census, receipt, product firmware unchanged; VERSION unchanged (`:68`, `:71`) | TRUE | The PR diff against `e21c1ca0` touches nothing under `sw/` or `configs/`, no capture checker, and not `VERSION` |
| Post-merge #608 cycles and #658 map are manager duties (`:69-70`) | TRUE | Issue acceptance 5. The soak is omitted (see the retained R520-2-S1) |

## Recipe against `identity.flow`

- All three baseline F endpoints (`route-1x1`, `ooc-1x1`, `ooc-8x8`) record `set_param synth.maxThreads 1` as flow line 1 and keep `set_param general.maxThreads 32` and their directives.
- `PP_SHADOW_BASELINE_RECIPE.md:105-113` and `:461` state exactly that.
- All five measurement-preparation commands (`:124`, `:125-126`, `:189-190`, `:191-192`, `:265-266`) carry `--single-thread-synthesis`.
- `pp_baseline.py:581-583` prepends the cap to the emitted script, which matches the recipe's "before synthesis" wording.
- `234_PP_SHADOW_AREA_BASELINE.md:33-35` is consistent with the recipe.
- The "exit 2 across flow identities" sentence (`:113`) is enforced. `receipts/probe_flow_identity.log` shows, for every endpoint:
  - the unchanged record judges 0;
  - dropping the cap line judges 2 (`NOT COMPARABLE: tool or recipe change in flow`);
  - changing the cap to 4 judges 2;
  - the gate's own `FLOW` extraction captures the prepended cap line.

## Gates run at the exact head (all rc 0; `receipts/gates/`)

| Gate | Result |
|---|---|
| `gen_toc.py --check` / `--selftest` / `--verify-anchors` | 139 pages OK; 1501/1501 arms; 393 links reproduced |
| `docs_check.py` | 0 findings, 199 md + 1140 scrubbed files |
| `check_doc_style.py` / `--selftest` | OK (22 current documents) / OK |
| `check_em_dash.py --base e21c1ca0` | 0 findings over 313 added lines in 6 pages; arms 339/339 |
| `syn/ooc/pp_baseline.py --selftest` | PASS (3 default and worker-capped scripts) |
| `syn/ooc/pp_resource_gate.py check-baseline` | PASS, 3 endpoints |
| `submodule_boundaries.gen.py --check` / `--selftest`; `check_submodule_docs.py` / `--selftest` | OK (4 exact gitlinks) |
| `DOC_MAP.gen.py --check`; `check_diagram_pngs.py` | OK |

The Markdown gates used an interpreter whose `cmarkgfm`, `html5lib`, `six`, `webencodings`, `cffi` and `pycparser` versions equal `tools/markdown/requirements.txt`.

## Mutation probes (`receipts/mutations/`, `NOTES.txt`)

| Probe | Gate | Result |
|---|---|---|
| M1: remove the new CHANGELOG contents entry | `gen_toc --check` | KILLED |
| M2: rename the new section heading | `gen_toc --check` | KILLED |
| M3c: committed U+2014 at `CHANGELOG.md:50` (scratch clone; control rc 0) | `check_em_dash --base e21c1ca0` | KILLED |
| M4: worker cap also alters `general.maxThreads` | `pp_baseline --selftest` | KILLED |
| M5: `--single-thread-synthesis` made a no-op | `pp_baseline --selftest` | KILLED |
| M6: over-long sentence in the new section | `check_doc_style` | KILLED |

M3, a worktree-only em-dash mutant, was an invalid probe design. The gate judges committed lines by construction, so it was superseded by M3c. It is not a gate weakness.

After probing, all 1,168 tracked entries match HEAD in bytes and mode. The index tree is `1d9982e2`, and the worktree and processor checkout are clean. The required gitlinks match: `protocol-processor` `2ad2f845`, `gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e`. See `receipts/restore_verification.txt`.

## Findings (this round)

### R520-3-R1 - RESIDUE - Docs - PR #692 body, "How to get into the same state", expected-values paragraph

- **Evidence:** the paragraph says "Expected ... parent head `cb359db3424c895010e89b4f9688347857008c85`". The PR head is now `fe8294978dd306706d659dc06468d0c07d43ce3e`. The Status section already names the correction.
- **Impact:** a reproducer who checks out the PR head sees a mismatch with the stated expected head. The defect is PR-body wording only: no measurement, verdict, code, test, generated artifact or clause claim changes.
- **Exact fix:** replace that value with `fe8294978dd306706d659dc06468d0c07d43ce3e`. Alternatively, write "parent head `fe8294978dd306706d659dc06468d0c07d43ce3e` (author validation at `cb359db3424c895010e89b4f9688347857008c85`; manager two-line documentation correction on top)".
- **Verification:** re-read the PR body.

No other finding was raised under any lens.

## Prior public findings on this PR

| Finding | State at `fe829497` | Evidence |
|---|---|---|
| R520-1-F1 (MINOR, Docs) | RESOLVED | The section is at `CHANGELOG.md:44-71` with its generated entry at `:11`. Every claim was checked true above |
| R520-1-F2 (MINOR, Docs) | RESOLVED | The recipe text, all five commands and `:461` were verified against the three flow identities. The exit-2 behaviour was probed |
| R520-1-S1 (SUGGESTION) | RESOLVED | The PR body quotes `(cd tb/verilator/milan_dp_render && make tdm8render-mutants)` |
| R520-2-F1 (MINOR, Docs) | RESOLVED | `cb359db3..fe829497` is exactly the prescribed two-line fix. The reset wording traces to PR #157 (`b0a74196`), an ancestor of `ead80360`. The PR #156 merge adds no reset-contract line (`receipts/verify_claims.log`) |
| R520-2-S1 (SUGGESTION, Docs) | RETAINED, optional | `CHANGELOG.md:69-70` and `SUBMODULES.md:181-183` still name only the #608 cycles and the #658 map, not acceptance 5's stream/counter soak |
| R521-1 (POSITIVE at `5428b044`, no findings) | Nothing to resolve | Only three Markdown files changed since then. No RTL, test or record artifact in its scope was touched |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `CHANGELOG.md:44-71` and `SUBMODULES.md:158-185`, checked claim by claim against processor merges `054d01c`, `21c6f70`, `e6a759d`, `7e5415e`, `86a7b0c`, `2ad2f84` and PR bodies #156/#159-#162/#164; issue #682 acceptance 1-5 and the round-2/round-3 rulings; `rom_digests.tsv`; `xvlog.budget`; `pp_resource_baseline.json` | R520-3 | `fe8294978dd306706d659dc06468d0c07d43ce3e` |
| RTL | CLEAN | Processor RTL deltas `KL_aecp_notify.sv` (#159 stamp in N_EMIT_WAIT, #161 `dh_v_r && !em_active_r`), `KL_srp_listener_fsm.sv` and `KL_srp_talker_fsm.sv` (#160 branch order), `KL_pp_originator.sv` and `KL_pp_rx_validator.sv` (#162); `hdl/top/protocol_processor_top.sv` byte-identical between pins; no parent RTL changed since `5428b044` | R520-3 | `fe8294978dd306706d659dc06468d0c07d43ce3e` |
| Robustness | CLEAN | `pp_resource_gate.py:310-326` judge refusal across flow identity (probe: dropped or changed cap gives 2 on all three endpoints; unchanged gives 0); `pp_baseline.py:575-583` argument refusals and cap placement; `sim_nxn.cpp` drain bound of 2,048 cycles | R520-3 | `fe8294978dd306706d659dc06468d0c07d43ce3e` |
| Tests | CLEAN | `pp_baseline.py:500-521` self-test arms (M4/M5 KILLED); contents, em-dash and style gates (M1/M2/M3c/M6 KILLED); no test file changed since `5428b044` (`receipts/verify_claims.log`) | R520-3 | `fe8294978dd306706d659dc06468d0c07d43ce3e` |
| Docs | CLEAN (RESIDUE R520-3-R1 carried) | `CHANGELOG.md:11,44-71`; `SUBMODULES.md:158-185`; `PP_SHADOW_BASELINE_RECIPE.md` (whole file); `234_PP_SHADOW_AREA_BASELINE.md:27-35`; `AREA_BUDGET.md:102`; PR #692 body; the 15 gate receipts in `receipts/gates/` | R520-3 | `fe8294978dd306706d659dc06468d0c07d43ce3e` |

## Real limits

- Full parent, PP, gPTP, Yosys and builder banks were not run, as this round's scope requires. Parent bank, image, timing, render-differential and capture results are the author's round-2 evidence at `5428b044` and its ancestors. They were accepted by R521-1. This round checked that nothing in their input scope changed since then; it did not re-execute them.
- The twelve builder documentation workflow steps were not re-run here. The author and manager receipts report them at `cb359db3` and `fe829497`.
- Hosted runs at this head were still running when inspected. The four workflows (rtl-fast, docs, elaborate, rtl-full) had 20 check runs between them: 10 succeeded, 9 in progress, and 1 skipped ("Physical gPTP (nightly and manual)"). A skipped context is not executed evidence.
- Physical calibration was NOT RUN, and field skips are not hardware proof.
- The processor PR claims were read from the PR bodies and the pinned history. The processor's suites were not re-run.

## Pending manager duties

- Hosted and local-replica acceptance at the exact head.
- Candidate-merge validation against the live dev tip at the merge turn.
- R521-3's independent verdict.
- Carry R520-3-R1 to the residue checklist. R520-2-S1 is optional.
- Explicit merge authorization.
- Post-merge containment.
- Acceptance 5 on hardware: the #608 withdrawal cycles, the #658 default map, and the stream and counter soak.

R520-3 FINISHED
