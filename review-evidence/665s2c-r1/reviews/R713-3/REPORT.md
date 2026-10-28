[R713] POSITIVE - exact head 5527a9c66716331fd06285f428ea1a653c526ada

# R713-3: internal cleared-context review of PR #796 (issue #665, lane S2c), round 3

- **Head:** `5527a9c66716331fd06285f428ea1a653c526ada`, tree `3d2c50f0ef0f970efa9cff70f085bb25e0917774` (the clone's HEAD, index tree and worktree all match; `receipts/clone_integrity.txt`).
- **Base:** `dev-soft-core` `1a635a4cf9dce5095be624f0265fc1002a60ec59`, still the live tip at review time. Live `dev` is `97aab1d0f28bd753a3e11df6278d5cac54f964dd` (`receipts/merge_and_scope.txt`).
- **Previously reviewed head:** `e0bb857a9f4b8e9d29736970a1135afde03260c5` (R713-2 and R714-2, both NEGATIVE on one MINOR).
- **Verdict:** POSITIVE. No BLOCKER, MAJOR or MINOR is open. One RESIDUE (wording only) and three optional suggestions are new. Every lens is covered clean at this head.

## Scope, reconstructed from public state

- **The assignment** is the owner decision of 2026-10-26 (issuecomment-6421463860):
  1. an instruction cache on the split SoC's VexiiRiscv, through the pinned generator's own options, with the all-fabric CPU byte-identical and the region decode exact (#791);
  2. measurement at both points against S2's tables, with a sweep of at least two sizes and the block RAM and LUT/FF cost;
  3. the hybrid-XIP effect;
  4. the residual T_svc gap;
  5. firmware behaviour, tests and the mailbox contract unchanged.
- **The NFR-SCOUT-01 amendment** is the owner's decision of 2026-10-27 (issuecomment-6434741232), with its correction (issuecomment-6434744436), whose text governs.
- **Round 3** (issuecomment-6461736980) asks for four things:
  1. merge `dev-soft-core` `1a635a4c` as a merge commit;
  2. fix R713-2-F1 / R714-2-F1, so that `FR_NFR.md:6` states the amended NFR-SCOUT-01 as `:321` does;
  3. classify any harness file S2 round 6 left unlisted;
  4. run the gates and one real 1x1 cache build, compared with the PR's figures.

## What changed since the previously reviewed head

`receipts/scope_blobs.txt` compares the blob of each of the PR's 15 files at `e0bb857a` and at the head.

- **Three files changed:**
  - `docs/reference/FR_NFR.md`: lines 6-8, the page summary;
  - `sw/firmware/ctrl/test/ctrl_configs.py`: `build.py`'s `OUTSIDE` reason, at `:181-191`;
  - `tb/verilator/ctrl_service_budget/README.md`: the file-classification paragraph, from the base, plus one line at `:133`.
- **Twelve files are blob-identical,** among them `milan_soc.py`, `split_soc.py`, `sim_main.cpp`, `observe.vlt`, `build.py`, `run.py`, `selftest.py`, `selftest_mutants.py`, `test_soc_options.py`, and the three other amended design pages.
- **The merge `10d8df98` resolved no conflict:** its remerge-diff is empty.
- **The base moved only CI tooling and READMEs.** Between S2's final head `f58d049b` (the merge base) and `1a635a4c` it changed only CI workflows and scripts, three READMEs, `docs/testing/*`, and the harness's `ctrl_configs.py` and README classification text. It changed no firmware, LiteX, patch or gitlink. So the PR's figures do not depend on anything the merge brought in.
- **This round's diff is all reachable from the head:** 16 commits on `1a635a4c` (15 non-merge), and no gitlink change against the base.

## Findings

### R713-3-RES1 RESIDUE - Docs - `tb/verilator/ctrl_service_budget/README.md:134` - "Its own compiles" now reads as the XIP arm's

- **Evidence:**
  - This round inserted `:133`, "The `--xip` arm relinks the image's objects through `ctrl_srp_image.link`, ...", between `:132` ("`build.py` hands its image ...") and `:134` ("Its own compiles build the Verilator model.").
  - The nearest antecedent of "Its" is now the `--xip` arm, but the sentence is about `build.py`. Its `OUTSIDE` reason at `ctrl_configs.py:181-191` says the same thing correctly ("its own compiles build the test SoC's Verilator model").
- **Why RESIDUE:** this is wording only. It changes no figure, test, gate input or classification, because the boundary gate reads `OUTSIDE`'s keys, not its reasons (`ctrl_configs.py:320`).
- **Exact fix:** in `README.md:134`, replace "Its own compiles build the Verilator model." with "`build.py`'s own compiles build the Verilator model."

### SUGGESTION (optional; affects no verdict or lens)

- **R713-3-S1 - Docs - `docs/reference/FR_NFR.md:6-8`: rewrap the summary to the paragraph's width.**
  - The paragraph's earlier lines wrap near 80 columns. The new lines run to 106, 119 and 141 columns.
  - The rendered page is unaffected and no gate requires a width. The four-line count that keeps line citations stable, and which the PR body states, can be kept.
- **R713-3-S2 - Docs: carried forward.** R713-2-S3 is the same point as R714-2-S1: the area plan's `:383` pairs the owner's cached text with the cacheless hart's figures. R713-2-S4 is the cacheless wording in `docs/litex/LITEX_SOC.md:11` and `sw/README.md:3`. Both are unchanged at this head and remain owner or manager questions, not executor work.
- **R713-3-S3 - Tests and Robustness: carried forward.**
  - R713-1-S2 to S4, R714-1-S1 and S2, and R713-2-S2 and S5: reuse identity by label, `--xip --fetch-l1 none` accepted, the refill-wait accounting not gated, `xip_offset()` not covered, and NFR-SCOUT-01 not cited in `test_soc_options.py:22-26`.
  - R714-2-S2: `split_soc.build`'s own `fetch_l1` record is not self-tested.
  - The code is blob-identical to `e0bb857a`, so each stays as stated.

### Comment rule

There is no new instance in this round's delta (`receipts/comment_rule_scan.txt`).

- The scan of added source lines from `e0bb857a` to the head finds nothing.
- Over the whole PR, from `1a635a4c` to the head, the only hits are `build.py:149` and `:153`, "decision D3". That is the owner decision ID that R714-1 RES1 prescribed and both round-2 reviews accepted.
- The new `ctrl_configs.py` reason text names no lane, round, reviewer or comment ID.

## Prior public findings: resolved or retained at this head

| Finding | Status at `5527a9c6` | Evidence |
|---|---|---|
| R713-2-F1 MINOR (Docs, Conformance): `FR_NFR.md:6` summary still said "cacheless" | **Resolved** | `FR_NFR.md:6-7` now reads: "The release uses one RV32I control hart: in the split placement it has a 4 KiB direct-mapped instruction cache (64-byte lines, one refill at a time) and no data cache; in the all-fabric placement it stays cacheless (NFR-SCOUT-01)." That is the corrected owner text of `:321`, with "MUST use" written as "uses" in a summary. `grep -n cacheless docs/reference/FR_NFR.md` finds only `:7` and `:321`, both the all-fabric placement. The manager publicly directed this edit (issuecomment-6461736980, item 2), and it restates the owner's own amended sentence and adds no new requirement content, so the routing condition in R713-2-F1 is met. The PR body's "There is no open requirement conflict" is now true. Lines 5-8 remain four lines, so no line citation into the page moves. The docs gates are rc 0 at the head (below). |
| R714-2-F1 MINOR (Docs, Conformance): the same line | **Resolved** | As above. |
| R713-1-F1 to F4, R714-1-F1 and F2, all prior RESIDUE | **Remain resolved** | They were resolved at `e0bb857a` by R713-2 and R714-2. Every file they touched is blob-identical at this head, except the README, whose only change is the classification paragraph `:127-137`, which none of them concerned. |
| R713-1/R714-1/R713-2/R714-2 SUGGESTIONs | Retained as optional | R713-3-S2 and R713-3-S3 above. |

## Lens results with evidence

Each lens below was applied at this head. The checks rerun here were chosen to match what the delta touched.

```text
[R713] PASS Conformance - docs/reference/FR_NFR.md:5-8,:321; ARCHITECTURE_HW_SW_SPLIT.md:62; MARK_II_AREA_PLAN.md:383; SPLIT_CONTROL_MEMORY.md:243-247; receipts/author_r3_verify.txt - the summary states the amended NFR-SCOUT-01 exactly as issuecomment-6434744436 and :321 do; the other three amended pages are blob-identical to e0bb857a, where they were checked against the owner text; the round-3 1x1 cache build at the head reproduces the PR's verdict line (18 groups, 0 refusals, 34 of 141 instances, 13 of 81 paths) and a table.md byte-identical (sha256 8760d219...) to round 2's regrade, carrying the PR's "at least 966,218 CPU cycles (19.324 ms)", so the acceptance tables (items 2-4) stand; the merge brought no firmware, LiteX, patch or gitlink change (receipts/merge_and_scope.txt).
[R713] PASS RTL - sw/litex/milan_soc.py blob 9aaf5659, split_soc.py 58658d60, sim_main.cpp 643449b8, observe.vlt 07275805 (receipts/scope_blobs.txt); base drift f58d049b..1a635a4c - every RTL-, SoC- and generator-scope file is blob-identical to e0bb857a, where R713-2 covered RTL clean, and the base drift is CI tooling and docs only, so nothing that lens depends on changed; author receipt soc_options.log at the head: 6 killed controls, RESULT: PASS.
[R713] PASS Robustness - tb/verilator/ctrl_service_budget/run.py blob d1104493 (reuse refusal), build.py 96bfaacb (xip_image :178-211), selftest.py df829f54 :764-857 - blob-identical to e0bb857a, where R713-2 killed 8 reviewer mutants of the refusal; the self-test reruns here at the head with both refusal checks PASS and the 4 cache-build mutants caught (receipts/gates/harness_selftest.log); ctrl_srp_image.link (sw/firmware/ctrl/test/ctrl_srp_image.py:80-95) read against the new boundary reason: it compiles plat/ctrl_split_start.S, copied unchanged by build.py:195, and links with the edited ctrl_split.ld.
[R713] PASS Tests - receipts/gates/harness_selftest.log (93 PASS, 70 MUTANT caught, 0 failures, rc 0, my rerun at the head); sw/firmware/ctrl/test/ctrl_configs.py:181-191 against ctrl_configs.py:320 - the changed reason is documentation: the gate reads OUTSIDE's keys, so the classification is unchanged; the author's firmware_boundary (ctrl_boundary: PASS, rc 0), publication_census (rc 0), ctrl_memory (RESULT: PASS), builder (ALL GATES PASS EXCEPT 1 NOT RUN, the calibration report needing a vendor build tree) and behave (406 scenarios passed) receipts at 5527a9c6 are hash-verified against the packet manifest (135 of 135); the six classified harness files match the six code files that name the firmware tree.
[R713] PASS Docs - FR_NFR.md:5-8; tb/verilator/ctrl_service_budget/README.md:127-137; ctrl_configs.py:181-191; PR #796 body - the summary, classification paragraph and boundary reason state what the code does (build.py:178-211, ctrl_srp_image.py:80-95); docs_check, check_doc_style, check_em_dash --base 1a635a4c (pinned renderer), gen_toc --check and --verify-anchors, check_hygiene, check_py_idiom, check_baremetal_only and check_feature_status all rc 0 at the head (receipts/gates/); the PR body's round-3 claims hold (16 commits, 15 files, merge without conflict, grep result, gate list); one wording RESIDUE (R713-3-RES1), which by rule leaves the lens clean.
```

## Evidence verified

- **The author's round-3 packet** is `review-evidence/665s2c-r1/author-r3` at `e98207b2`. All 135 files match `MANIFEST.json`'s `published_sha256`, and none is missing (`scripts/verify_author_r3.py`, `receipts/author_r3_verify.txt`).
  - The evidence commit carries no cryptographic signature (`%G?` = N). Integrity rests on the manifest hashes.
  - `gates/HEAD.txt` and `run-1x1-64x1/HEAD.txt` both name `5527a9c6`.
  - `gates/summary.md` reports "0 of 100 gates nonzero or left the tree dirty".
- **The 1x1 cache build at the head** was spot-checked.
  - `build.json` records `fetch_l1=split [64, 1]`, `xip False`, and the generator options `--fetch-l1 --fetch-l1-sets=64 --fetch-l1-ways=1`.
  - Its `table.md` hashes the same as round 2's `author/receipts/regrade/arms/P1-64x1/table.md`, which I recomputed.
  - The composed maximum it carries is the PR's "at least 966,218 CPU cycles (19.324 ms)".
- **My reruns at the head** (`receipts/gates/`):
  - the harness self-test;
  - `docs_check`, `check_em_dash`, `check_doc_style`, `gen_toc --check` and `--verify-anchors`, `check_hygiene`, `check_py_idiom`, `check_baremetal_only`, `check_feature_status`: all rc 0.
  - A first run of `em_dash` and the two TOC gates stopped with rc 2, because the pinned Markdown renderer was absent. Those were reruns with the renderer installed from `tools/markdown/requirements.txt` (hash-pinned) in a disposable environment. The `.log` files hold the final runs.
- **Hosted checks at the exact head** are only partly done: `receipts/hosted_checks_5527a9c6.txt` is a snapshot taken during this review.
  - Completed with success: `bdd-conformance`, `verilator-lint`, `wire-accountability`, `firmware-aecp-mutants`, `docs-check-no-git`, `changes` and `full-ci-gate`.
  - Skipped: `Physical gPTP`.
  - Still running or queued: `firmware-boundary`, `publication-census`, the docs gates, the elaborate gates, the Verilator shards and Yosys.
  - This review takes none of these as acceptance. The manager owns hosted and act acceptance.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Owner amendment and correction; `FR_NFR.md:5-8, :321`; three other amended pages (blob-identical); round-3 1x1 receipts (`table.md` identity, verdict line); merge and base-drift scope | R713-3 | `5527a9c66716331fd06285f428ea1a653c526ada` |
| RTL | CLEAN | `milan_soc.py`, `split_soc.py`, `sim_main.cpp`, `observe.vlt` blob-identical to `e0bb857a`; base drift free of RTL, SoC and generator files; `soc_options` receipt at the head | R713-3 (scope unchanged since R713-2 at `e0bb857a`) | `5527a9c66716331fd06285f428ea1a653c526ada` |
| Robustness | CLEAN | `run.py` reuse refusal, `build.py` `xip_image`, `selftest.py:764-857` (blob-identical); self-test rerun at the head; `ctrl_srp_image.link` against the new reason | R713-3 | `5527a9c66716331fd06285f428ea1a653c526ada` |
| Tests | CLEAN | Self-test rerun (93 / 70, rc 0); `ctrl_configs.py:181-191` against the gate's use at `:320`; hash-verified author receipts at the head (boundary, census, ctrl_memory, builder, behave) | R713-3 | `5527a9c66716331fd06285f428ea1a653c526ada` |
| Docs | CLEAN (RES1 is RESIDUE) | `FR_NFR.md:5-8`; harness README `:127-137`; boundary reason; PR body; docs gates rerun at the head | R713-3 | `5527a9c66716331fd06285f428ea1a653c526ada` |

## Real limits

- **No source build was run in this review.** The 1x1 and 8x8 harness builds, `test_soc_options.py` (which needs the LiteX environment), the firmware-boundary and publication-census steps, the builder bank and behave were not rerun here. Their execution evidence at this head is the author's published receipts, verified by hash, plus my reruns listed above.
- **The 8x8, sweep, XIP and control figures were not rebuilt at this head.** They rest on the earlier rounds' archives, together with the proof that nothing they depend on changed: the code blobs are identical to `e0bb857a`, and the base drift is CI and docs only.
- **No reviewer mutants were run this round.** The refusal and build-record code is blob-identical to `e0bb857a`, where R713-2's eight source mutants were killed. The self-test's own 70 mutants were rerun.
- **No manager source bank runs at this head, and none is claimed.** Physical calibration is NOT RUN. The builder's one NOT RUN, a calibration report that needs a vendor build tree, is not hardware proof.
- **The `FR_NFR.md:6` edit has no separate owner statement.** It rests on the manager's public direction, and it restates the owner's amended sentence word for word.
- **Hosted checks at the exact head were partly still running** when this report was written.

## Pending manager duties

- Validate the current-dev merge candidate (source base `1a635a4c`, live dev `97aab1d0`) with the builder and native banks, and link the receipts on the PR.
- Hosted and act acceptance at the exact head, including the exact-head `verilator-suites` and `yosys-portability` evidence for a ready PR.
- Carry R713-3-RES1 to the residue checklist.
- Route R713-3-S2 (area-plan row qualifier, cacheless wording in `LITEX_SOC.md` and `sw/README.md`) to the owner if wanted.
- The external review's verdict at this head.
- No merge without explicit maintainer authorization.

R713-3 FINISHED
