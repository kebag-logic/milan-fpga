[R714] NEGATIVE - exact head e0bb857a9f4b8e9d29736970a1135afde03260c5

Round R714-2, external independent review of issue #665 lane S2c, PR #796 (`665-s2c-icache` -> `dev-soft-core`). Tree `e183ba210eb7e9e8e408da9ad0268b307f98646c`. Source base `f58d049beb377c3f535628067022d4d5b51e8208`. This is a later round, so it judges the delta since R714-1's head `a611785f2afe5bbe587f74034d869e869a1c8d37` (7 commits, 9 files) and every prior finding, and re-covers all five lenses at this head.

**Verdict.** One MINOR is open, under Docs and Conformance: the authoritative requirement page still states the pre-amendment NFR-SCOUT-01 in its introduction. Everything else in the delta holds:
- Every finding from R713-1 and R714-1 is resolved at its cause.
- The owner's amendment text is applied exactly where the owner listed it.
- The new tests fail for the defects they claim to catch. Five of my own source mutants are all killed.
- The author's gate receipts reproduce at this head.

## Scope reconstructed from public state

- **S2c assignment** (#665 issuecomment-6421463860):
  - an L1 instruction cache on the split SoC's VexiiRiscv only, through the pinned generator's options, with the all-fabric CPU byte-identical;
  - measurement on S2's harness at both points, with a size sweep, block-RAM/LUT/FF cost and a hybrid-XIP arm;
  - the remaining T_svc gap stated;
  - firmware and the mailbox contract unchanged.
- **Round-2 items 1 to 6** (issuecomment-6433542516): R713-1-F1 to F4, R714-1-F1 and F2, and the residue. No new measurement.
- **Owner amendment of NFR-SCOUT-01** (issuecomment-6434741232), with its correction (issuecomment-6434744436), whose wording governs. It names four edits, leaves `docs/history/` alone, and requires the owner again for any change of geometry or a data cache.
- The PR stays "Relates to #665", because T_svc is not closed.

## Findings

### R714-2-F1: MINOR, Docs and Conformance: the requirement page's introduction still states the pre-amendment NFR-SCOUT-01

- **Where:**
  - `docs/reference/FR_NFR.md:5-6`: "The release uses one cacheless RV32I control hart and scales media capacity through fabric stream contexts, ...".
  - The PR body's Status line: "There is no open requirement conflict."
- **Authority and evidence** (`receipts/fr_nfr_intro_vs_row.txt`):
  - The amended row on the same page (`:321`) reads: "The release architecture MUST use one RV32I control hart: in the split placement it has a 4 KiB direct-mapped instruction cache ... in the all-fabric placement it stays cacheless."
  - NFR-SCOUT-02 (`:322`) says "Mark II defaults to firmware", which is the split placement. So the introduction's "the release uses one cacheless ... hart" restates the requirement the owner replaced.
  - The owner's amendment asked that repetitions of "cacheless" be replaced ("wherever it repeats 'cacheless': the same wording"). This page's introduction is such a repetition, on the requirement page itself.
  - The author published it as an open risk in REVIEW READY (issuecomment-6435396245), and the PR's checklist leaves "No undocumented requirement or interface change remains" unticked for it. Publishing a contradiction does not remove it from the tree.
  - The PR body's "There is no open requirement conflict" contradicts the PR body's own risk bullet.
- **Why MINOR, not RESIDUE:** the sentence is a claim about what the requirement is, so it is a clause claim, which the residue rule excludes.
- **Impact:** a cold reader of the authoritative FR/NFR page gets two answers to "does the control hart have a cache". The page that Docs and Conformance are read against does not reflect the changed contract.
- **Required outcome:** one of these two.
  - The introduction agrees with the amended row. A suggested text: "The release uses one RV32I control hart (in the split placement with a 4 KiB instruction cache and no data cache; in the all-fabric placement cacheless) and scales media capacity through ...". The PR body's Status then stays true.
  - Or the owner or manager publicly records that the introduction stays as written, and the PR body states that, not "no open requirement conflict".
- **Verification:** `sed -n 4,8p docs/reference/FR_NFR.md` agrees with `:321`. The docs gates (`docs_check`, `check_em_dash`, `gen_toc --check`) stay rc 0. The PR body's Status matches the page.

### R714-2-S1: SUGGESTION, Docs (a question for the owner, not for the executor): the area plan's control-hart row pairs the owner's cached text with cacheless figures

- **Where:** `docs/design/MARK_II_AREA_PLAN.md:383`.
  - The row now reads "the control hart (NFR-SCOUT-01: one RV32I hart, 4 KiB instruction cache, no data cache)".
  - Its 3,522 LUT and 4,736 FF are the pre-split inventory's hart, which is the all-fabric hart. The corrected amendment says that hart stays cacheless.
- **Why not a finding:** the text is exactly the owner's, reconfirmed by the correction ("The other edits are as listed"). The executor applied it and published the mismatch. The cache's own 1.5 tiles are debited separately (`:887`, `:896`).
- **Optional:** the manager asks the owner whether to add a qualifier, for example "(figures: the cacheless all-fabric hart as inventoried; the split's cache is debited in the ledger)".

### R714-2-S2: SUGGESTION, Tests: the portable self-test does not cover `split_soc.build`'s own `fetch_l1` record

- **Where:** `tb/verilator/ctrl_service_budget/selftest.py:795-810` stands a recorder in for `split_soc.build`. So a mutant of `split_soc.py:353` (`'fetch_l1': fetch_l1`) would not be seen by the self-test.
- **Mitigation:** the README states it as a Limit (`README.md:957`), and each real run's `build.json` attests the record. R713-1-F4's required change, that `build()`'s record is checked and the refusal is driven, is met for `build.build` (see the next section).
- **Optional:** a LiteX-free unit check of the record dict that `split_soc.build` returns.

### Prior suggestions retained (optional, unchanged at this head)

- R714-1-S1: the refill-wait accounting in `sim_main.cpp` has no self-test.
- R714-1-S2: `xip_offset()` is not covered.
- R713-1-S2: reuse compares the label, not the resolved geometry.
- R713-1-S3: `--xip --fetch-l1 none` is accepted.
- R713-1-S4: a first-beat refill mutant survives.

The author declined these this round, as is allowed. R713-1-S1 is answered by R714-1-F1's fix.

**RESIDUE:** no new instance in this delta. The comment-rule scan of every added source line since `f58d049b` finds only "decision D3", the decision ID that R714-1 RES1 prescribed (`receipts/comment_rule_scan.txt`).

## Prior findings, resolved or retained at this head

| Finding | State at `e0bb857a` | Evidence |
|---|---|---|
| R714-1-F1 (Tests): the option test accepted any geometry | **Resolved** | `test_soc_options.py:26` restates `--fetch-l1 --fetch-l1-sets=64 --fetch-l1-ways=1`, and `:234-235` require it exactly for `ctrl_cpu_args` and for the constructor. Three new killed controls (128 sets, 2 ways, 32 sets). My rerun: rc 0, 6 killed controls, byte-identical to the author's receipt. My own mutant of the call site `milan_soc.py:2903` to `ctrl_cpu_args((128, 1))` is killed (`receipts/probe-socopt-*`). |
| R714-1-F2 / R713-1-F2 (Docs): block-RAM rate | **Resolved** | README `:769`: "one tile for each 4 KiB of data and half a tile of tags for each way". All 8 rows of the Vivado table (`:757-764`) satisfy 4.5 + size/4 KiB + 0.5 x ways (4.5, 5.5, 6, 7, 7.5, 9, 9.5, 13). That agrees with `SPLIT_CONTROL_MEMORY.md:236` (6.0 tiles). |
| R713-1-F1 (Conformance, Docs): unbounded rows | **Resolved** | The six rows (`README.md:676, 681, 682, 708, 718, 719`) read "at least X, **never answered** / **never released**" in both ms columns and the cycles column. A note (`:664-666`) calls them lower bounds. Delta number audit: no table figure changed, only labels (`receipts/readme_delta_numbers.txt`). |
| R713-1-F3 (Docs, Tests): reproduction commands | **Resolved** | The Results block (`:187-192`), the controls (`:924-929`) and the fixture regeneration (`:915-918`) select `--fetch-l1 none`. The cache controls name `--fetch-l1 64x1` (`:796-797`). The author's rerun receipt `author-r2/a685c/receipts/reruns/C1-slow-none.log` shows `BUDGET control.discover.if0: 24.614 ms`, `CONTROL slow-adp-rx caught`, rc 0. The fixture regeneration was byte-identical at `619e84e6` (`fixture_identity.txt`). At this head `fixture.log`/`oracle.json` have the same blobs and sha256, and only `selftest.py` changed since (+1 docstring line). |
| R713-1-F4 (Tests): the reuse refusal was never exercised | **Resolved** | `selftest.py:825-857` drives `run.main()` through both the build and the `--reuse-build` refusal: eight cases, plus a record with neither key. My five source mutants on a disposable copy all fail the self-test, and the unmutated copy passes (`probe_mutants.sh`, `receipts/probe-selftest-*`): `built_as` ignoring `xip`; a missing `fetch_l1` read as `split`; `build.build` handing `split` whatever the selection; `selected()` dropping `xip`. The built-in mutants `reuse: a reused build is not compared with the selection` and `build: an XIP build records the block-RAM arm` are R713-1's two probes, and both are caught. |
| R714-1 RES1 / R713-1 RS1: lane names in comments | **Resolved** | `build.py:149` "(#665, decision D3)" and `:151` "the saved-state flash driver (nvm_flash_litespi.c)". The delta's `build.py` change is comment-only (0 non-comment lines, `receipts/scope_blobs.txt`). RS1's alternative text for `:149` is not applied. Either text satisfies the comment rule, so nothing remains. |
| R714-1 RES2: XIP conclusion | **Resolved** | README `:746` and the PR body's XIP bullet carry RES2's exact texts. |
| R713-1 RS2 to RS4 | **Resolved** | `MARK_II_AREA_PLAN.md:897-898` ("All four", "None of these numbers"; the four totals 114/115/115.5/116.5 check). The PR body's Status sentence is RS3's text. "a CPU of 13 tiles" is at README `:741`, `:745` and in the PR body. |
| Prior suggestions | Retained, optional | Listed above. |

## Lens results at the exact head

| Lens | Result | Artifact | What was checked, and against what |
|---|---|---|---|
| Conformance | **UNCLEAN (F1)** | `docs/reference/FR_NFR.md:321` against issuecomment-6434744436; `ARCHITECTURE_HW_SW_SPLIT.md:62`; `MARK_II_AREA_PLAN.md:383`; `SPLIT_CONTROL_MEMORY.md:243-247`; round-2 items 1-6; PR body | The row's first sentence is the corrected owner text character for character, and the rest of the row is unchanged. The architecture page has "uses" for "MUST", because that page carries no requirement keywords. The area plan has the owner's exact string. The design page records the decision, its correction, the old and new text and the re-decision rule. `docs/history/` is untouched. Items 1-6 are met (prior-findings table). The remaining "cacheless" mentions describe the shipping all-fabric product, history or patch names, and none restates NFR-SCOUT-01, except `FR_NFR.md:6` (F1). |
| RTL | CLEAN | `receipts/scope_blobs.txt`: `milan_soc.py` `9aaf5659`, `split_soc.py` `58658d60`, `sim_main.cpp` `643449b8`, `observe.vlt` `07275805`, patch 0005 `2841a0a8`, identical at `a611785f` and `e0bb857a` | The delta touches no RTL, SoC, netlist-generating or observer file. R714-1 covered these artifacts clean at `a611785f`, an ancestor that nothing in RTL scope has touched since, and the delta changes nothing they depend on. My rerun of `test_soc_options.py` (rc 0) confirms that the constructor hands the all-fabric CPU exactly `--xlen=32` and the split CPU exactly the 4 KiB, 64-set, 1-way fetch L1 with no LSU L1 at this head. |
| Robustness | CLEAN | `run.py:285-318` (`selected`, `built_as`, the reuse refusal), blob `d1104493` unchanged; `selftest.py:825-857` | The refusal paths were exercised at this head: 6 reuse cases across arm and cache mismatches, 2 legacy-record cases, and default-`split` against a `none` build. My mutants of the legacy default and of the `xip` comparison are killed. The build change is comment-only. The open robustness suggestions (R713-1-S2, S3) are optional. |
| Tests | CLEAN | `selftest.py` (93 PASS, 70 of 70 mutants, rc 0), `selftest_mutants.py:333-470`, `test_soc_options.py:22-257` (6 killed controls, rc 0), `sw/litex/test_ctrl_memory.py` (rc 0), `receipts/probe-*`, `receipts/mutant_table_check.txt` | Each new check fails for its defect: 3 new built-in mutants, 3 new soc controls, and 5 reviewer mutants, all killed. The README's 70-row mutant table matches the 70 caught lines and their named checks (0 mismatches). My self-test and option-test logs equal the author's published receipts byte for byte, apart from the receipt header and footer. |
| Docs | **UNCLEAN (F1)** | Harness README delta (`:47-49, :75-76, :185-193, :664-666, :676-719, :741-746, :769, :796-797, :826-832, :898-929, :957`); the four amended pages; PR body; `receipts/docs/*` | Labels, rates and commands agree with the figures beside them. Docs gates at the head, rc 0: `docs_check` (0 findings), `check_doc_paths`, `check_doc_style`, `DOC_MAP --check`, `gen_module_matrix --check`, `check_em_dash` (0 findings over 1009 added lines), `gen_toc --check` and `--verify-anchors` (552 reproduced), `git diff --check e76a755a HEAD`. Open: F1. S1 is the owner's question. |

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R714-2-F1 open) | Owner amendment and correction; `FR_NFR.md:5-6, :321-322`; `ARCHITECTURE_HW_SW_SPLIT.md:62`; `MARK_II_AREA_PLAN.md:383, :887-898`; `SPLIT_CONTROL_MEMORY.md` section 7; round-2 items 1-6; PR body | R714-2 | `e0bb857a9f4b8e9d29736970a1135afde03260c5` |
| RTL | CLEAN | Unchanged RTL-scope blobs (`receipts/scope_blobs.txt`), carried from R714-1 at ancestor `a611785f`; `test_soc_options.py` rerun at the head | R714-2 (scope carried from R714-1 at `a611785f`) | `e0bb857a9f4b8e9d29736970a1135afde03260c5` |
| Robustness | CLEAN | `run.py` reuse refusal (unchanged blob); `selftest.py:825-857` cases; reviewer mutants `bas_xip`, `bas_default`, `sel_xip` | R714-2 | `e0bb857a9f4b8e9d29736970a1135afde03260c5` |
| Tests | CLEAN | `selftest.py`, `selftest_mutants.py`, `test_soc_options.py`, `test_ctrl_memory.py` reruns; 5 reviewer source mutants killed; mutant-table cross-check | R714-2 | `e0bb857a9f4b8e9d29736970a1135afde03260c5` |
| Docs | UNCLEAN (R714-2-F1 open) | Harness README delta; four amended pages; PR body; docs gates at the head | R714-2 | `e0bb857a9f4b8e9d29736970a1135afde03260c5` |

**To clear:** a commit that resolves F1, or a published owner or manager decision that keeps `FR_NFR.md:6` with the PR body corrected. A Docs and Conformance re-check at that head. A docs-only fix changes nothing in RTL, Robustness or Tests scope, so those lenses stay covered at `e0bb857a` as their ancestor.

## Evidence verified

- **The published packet** `review-evidence/665s2c-r1` at `50e47e55a7cc8b0cb07d30628e493b6fcee6c8cf`, fetched read-only:
  - `MANIFEST.json` sha256 `a36783d1a379c5519f49641270d9076c10bbe06a06c2afe543e8e84e9fca9794`.
  - Every file under `author-r2/a685d` (109) and `author-r2/a685c` (137) matches its `published_sha256`, with none unlisted and none missing (`receipts/evidence_manifest_check.txt`).
  - The packet commit carries no cryptographic signature (the hosting service reports `unsigned`). Integrity rests on the manifest hashes and on the commit id the manager named.
- **The author's gate summary** (`a685d/receipts/gates/summary.md`, `HEAD.txt` = `e0bb857a`): 0 of 97 gates nonzero or dirty. These were spot-checked by my reruns:
  - the self-test and the option test, byte-identical;
  - `check_baremetal_only --check`: OK, 0 findings over 1431 files;
  - `test_ctrl_memory`: PASS;
  - the docs gates listed above, all rc 0.
- **Hosted, exact head** (`receipts/hosted_check_runs.tsv`, snapshot 2026-10-27 about 07:50 CET): 4 completed success (`changes`, `docs-gates-1`, `full-ci-gate`, `wire-accountability`), 1 skipped (`Physical gPTP (nightly and manual)`), 5 in progress, 32 queued. It is not complete. The manager owns hosted and act acceptance.

## Real limits

- **Not rerun:**
  - `cd tests && behave` and `test_builder.py --require-rv32`, on the author's receipts. `behave` reads none of the delta's files, and the builder bank passed at `de91db59` and reads none of the four pages.
  - The full harness arms, the controls, Vivado and Yosys. No measured figure changed in the delta, and R714-1 covered them at `a611785f`.
- No manager source bank runs at this head, and none is claimed or inferred. Source-head execution evidence is the author's published receipts plus my focused reruns.
- **Environment:**
  - The LiteX-dependent tests ran with the host's existing LiteX environment, read-only.
  - The renderer-dependent docs gates ran with the existing pinned Markdown environment.
  - Probe copies used read-only links to this clone's submodule trees.
- Physical calibration is NOT RUN. Field skips are not hardware proof.
- **Clone restored:**
  - HEAD `e0bb857a`, tree `e183ba21`, index and worktree identical to HEAD.
  - No untracked or ignored files remain (I removed the caches and outputs my runs created, including one cache in `protocol-processor`).
  - All six submodule gitlinks match their checkouts (`receipts/restore_check.txt`).

## Pending manager duties

- Resolve F1 with the executor, or put it to the owner. Carry S1 to the owner as a question.
- Hosted exact-head contexts are still in progress. The current-dev merge-candidate build (builder and native banks) against live dev `97aab1d0f28bd753a3e11df6278d5cac54f964dd` runs at the merge turn.
- Merge order: after PR #792. A merge needs the maintainer's explicit authorization and two independent POSITIVE reviews at the merge head.

R714-2 FINISHED
