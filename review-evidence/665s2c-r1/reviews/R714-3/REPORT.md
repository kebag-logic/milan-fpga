[R714] POSITIVE - exact head 5527a9c66716331fd06285f428ea1a653c526ada

Round R714-3. This is the external independent review of issue #665 lane S2c, PR #796 (`665-s2c-icache` -> `dev-soft-core`).

- Tree `3d2c50f0ef0f970efa9cff70f085bb25e0917774`.
- PR base `dev-soft-core` `1a635a4cf9dce5095be624f0265fc1002a60ec59`.
- Previously reviewed head: `e0bb857a9f4b8e9d29736970a1135afde03260c5` (R714-2 and R713-2, both NEGATIVE on one MINOR).

This is a later round, so it judges the delta `e0bb857a..5527a9c6` and every prior finding at its cause. Code the delta does not touch keeps its prior lens verdict, and the blob receipts below prove that it is untouched.

**Verdict basis:**
- No BLOCKER, MAJOR or MINOR is open.
- Both prior MINORs (R714-2-F1 and R713-2-F1, the same defect) are resolved at this head.
- One RESIDUE (README `:134`) and two optional suggestions are recorded below.
- All five lenses are covered clean at this exact head.

## Contents

- **[Task reconstructed from public state](#task-reconstructed-from-public-state)**: the scope and frozen acceptance this round is judged against.
- **[The delta under review](#the-delta-under-review)**: what changed since `e0bb857a`, and the proof that the merge is clean.
- **[Findings](#findings)**: RESIDUE and SUGGESTION items, with exact fixes.
- **[Prior public findings: resolved or retained at this head](#prior-public-findings-resolved-or-retained-at-this-head)**
- **[Lens results with evidence](#lens-results-with-evidence)**: one line per lens, with the artifacts examined.
- **[Reviewer-owned completion ledger](#reviewer-owned-completion-ledger)**
- **[Real limits](#real-limits)**
- **[Pending manager duties](#pending-manager-duties)**
- **[Receipts](#receipts)**

## Task reconstructed from public state

- **The S2c assignment** (#665 issuecomment-6421463860) is the frozen acceptance:
  - an L1 instruction cache on the split SoC's VexiiRiscv, through the pinned generator's own options;
  - the all-fabric CPU stays byte-identical, and the region decode stays exact (#791);
  - measurement on S2's harness at both points, with a size sweep, the block RAM and LUT/FF cost, and a hybrid-XIP arm;
  - the remaining T_svc gap at each point;
  - firmware behaviour, firmware tests and the mailbox contract stay unchanged.
- **The NFR-SCOUT-01 amendment:** the owner's decision (issuecomment-6434741232), in the corrected text of issuecomment-6434744436.
- **The round-3 assignment** (issuecomment-6461736980):
  1. Merge `origin/dev-soft-core` `1a635a4c` as a merge commit. S2's rules win on any conflict.
  2. R713-2-F1 / R714-2-F1: `FR_NFR.md:6` states the amended NFR-SCOUT-01 as `:321` does.
  3. Apply S2's round-6 file classification to the harness files this PR adds to.
  4. Run the gates and one real harness build at 1x1 with the cache, compared with the PR's figures.
- **Authorities read:** `AGENTS.md`, `CONTRIBUTING.md` (commit rule), `docs/reference/FR_NFR.md` (NFR-SCOUT-01 at `:321`, and 3.4.1 T_svc), and `sw/firmware/ctrl/test/ctrl_configs.py` (the boundary gate's `OUTSIDE` table).

## The delta under review

`git log e0bb857a..5527a9c6` contains three commits. Each commit message is one line with no trailers.

- **`10d8df98`** merges `1a635a4c`.
  - **It is a clean automatic merge.** `git merge-tree --write-tree e0bb857a 1a635a4c` gives `580e3504`, which is the merge's recorded tree. So the merge commit carries no manual edit (`receipts/scope_blobs.txt`, `receipts/verify_delta.txt`).
  - **The lane's own diff is unchanged by the merge.** `git diff f58d049b e0bb857a` and `git diff 1a635a4c 10d8df98` are identical apart from `index` lines and hunk offsets. The offsets move because S2's round 6 added a 12-line classification paragraph to the README.
  - The PR's diff against `1a635a4c` is 15 files, as REVIEW READY states.
- **`5e679594`** changes `docs/reference/FR_NFR.md:5-8`, the page summary. It now reads "The release uses one RV32I control hart: in the split placement it has a 4 KiB direct-mapped instruction cache (64-byte lines, one refill at a time) and no data cache; in the all-fabric placement it stays cacheless (NFR-SCOUT-01)."
  - That is `:321`'s clause word for word, with "uses" for "MUST use". It is also the owner's corrected text.
  - The paragraph keeps its four lines, so no line citation into the page moves.
- **`5527a9c6`** changes two things.
  - `ctrl_configs.py:181-191`, `build.py`'s `OUTSIDE` reason, now also names "the hybrid-XIP arm's relink of the image's objects to ctrl_srp_image.link, which compiles the split layout's reset entry from an unchanged copy and changes only the linker script".
  - README `:133` adds the same sentence.

**Checked against the code at this head:**
- `build.py:178-211` (`xip_image`) copies `plat/ctrl_split_start.S` unchanged. It writes only an edited `plat/ctrl_split.ld` (`xip_script`, `:169-175`) and links the already-built objects through `ctrl_srp_image.link`.
- `ctrl_srp_image.py:80-94` (`link`) compiles exactly that reset entry, generates `regions.ld` as the normal split link does, and links. So the new reason is true.
- The other two classified files the lane adds to still match their reasons:
  - `split_soc.py`'s delta adds `fetch_l1_geometry` and passes `ctrl_cpu_args`. It compiles no firmware.
  - `selftest.py`'s new `built()` (`:795-822`) replaces every toolchain step with a placeholder writer. It compiles nothing.

**Unchanged since `e0bb857a`** (identical blob IDs, `receipts/scope_blobs.txt`): `milan_soc.py`, `test_soc_options.py`, `build.py`, `run.py`, `selftest.py`, `selftest_mutants.py`, `split_soc.py`, `sim_main.cpp`, `observe.vlt`, patch 0005, `ARCHITECTURE_HW_SW_SPLIT.md`, `MARK_II_AREA_PLAN.md` and `SPLIT_CONTROL_MEMORY.md`.

Only `FR_NFR.md`, `ctrl_configs.py` and the harness README changed.

## Findings

### R714-3-RES1: RESIDUE, Docs: README `:134` "Its own compiles" now follows the `--xip` sentence

- **Where:** `tb/verilator/ctrl_service_budget/README.md:133-134`.
- **Evidence:**
  - At the base (`1a635a4c:README.md:113-114`), "Its own compiles build the Verilator model." follows "`build.py` hands its image to ...", so "Its" is `build.py`.
  - `5527a9c6` inserts the `--xip` sentence between them. "Its" now reads as the `--xip` arm.
  - The gate reads `ctrl_configs.py`, whose reason is correct ("... changes only the linker script; its own compiles build the test SoC's Verilator model"). So the defect is wording only: no figure, test, code, gate input or clause claim changes.
- **Exact fix:** in `README.md:134`, replace "Its own compiles build the Verilator model." with "`build.py`'s own compiles build the Verilator model."
- **Verification:** `sed -n 131,135p tb/verilator/ctrl_service_budget/README.md`. The docs gates stay rc 0.

### R714-3-S1: SUGGESTION, Docs: `FR_NFR.md:6-8` breaks the paragraph's wrap

- Lines 3 to 5 of the paragraph are 72 to 83 columns wide. Lines 6 to 8 are 106, 119 and 141.
- The author kept four lines on purpose, so that no line citation moves. That is a sound reason, and the style gate passes.
- **Optional:** rewrap the paragraph the next time the page is edited for another reason.

### R714-3-S2: SUGGESTION, Docs: the PR body's contents line says `branch` -> `dev`

- The PR body's Contents entry for Status says "`branch` -> `dev`". That is the CONTRIBUTING template's text.
- The Status section itself states `665-s2c-icache` -> `dev-soft-core` correctly.
- **Optional:** write "`665-s2c-icache` -> `dev-soft-core`" in the contents line, if the template allows it.

### Comment rule

- I scanned every added line of `5e679594` and `5527a9c6` for bench lane labels, lane names, review rounds, reviewer IDs and comment IDs: 0 hits (`receipts/comment_rule_scan.txt`).
- The only new source text is a string in `ctrl_configs.py`, and it cites no label.

## Prior public findings: resolved or retained at this head

I read these only after writing my own draft verdict and ledger. I did not read this round's other review.

| Finding | Status at `5527a9c6` | Evidence |
|---|---|---|
| R714-2-F1 (MINOR, Docs and Conformance): `FR_NFR.md:5-6` still stated a cacheless hart, and the PR body said "no open requirement conflict" | **Resolved** | `FR_NFR.md:5-7` states `:321`'s clause (above). The PR body's Status now says the summary "now states it as the row does. There is no open requirement conflict.", which is true at this head. The verification the finding named passes: `docs_check` 0 findings, `check_em_dash` 0 over 380 added lines, `gen_toc --check` OK, `--verify-anchors` 552 reproduced. |
| R713-2-F1 (MINOR, Docs and Conformance): the same defect | **Resolved** | As above. |
| R714-2-S1 (area plan `:383`'s figures are the cacheless hart's), R713-2-S3 (the same) | **Retained, optional** | `MARK_II_AREA_PLAN.md` blob unchanged. The owner's wording governs. This is still a question for the owner. |
| R714-2-S2 (`split_soc.build`'s own `fetch_l1` record is not self-tested) | **Retained, optional** | `split_soc.py` and `selftest.py` blobs unchanged. Each real run's `build.json` attests the record, and this round's 1x1 receipt shows `fetch_l1=split [64, 1]`. |
| R713-2-S1 (carrying R713-1-S2 to S4 and R714-1-S1, S2), R713-2-S2, S4, S5 | **Retained, optional** | None of their artifacts changed. The PR body lists them as not taken. |
| R714-1-F1, F2, RES1, RES2; R713-1-F1 to F4, RS1 to RS4 | **Still resolved** | Resolved at `e0bb857a` by R714-2 and R713-2. The merge leaves the lane diff identical, and no artifact those resolutions cite changed except README line offsets (+12). |

## Lens results with evidence

```text
[R714] PASS Conformance - docs/reference/FR_NFR.md:5-7 and :321 at 5527a9c6; #665 issuecomment-6434744436; round-3 items 1-4 (issuecomment-6461736980); merge 10d8df98 - the summary states the owner's corrected NFR-SCOUT-01 clause as the row does; the merge is the automatic merge (tree 580e3504 recomputed); S2's rules are unchanged by it (lane diff identical); item 3's reason matches build.py:178-211 and ctrl_srp_image.py:80-94; item 4's 1x1 build repeats the PR's 13 of 81 / 34 of 141 and 966,218-cycle composed maximum (receipts hash-verified, README :565, :623, :744, :789 agree)
[R714] PASS RTL - receipts/scope_blobs.txt: milan_soc.py 9aaf5659, split_soc.py 58658d60, sim_main.cpp 643449b8, observe.vlt 07275805, patch 0005 2841a0a8, test_soc_options.py 2962a280, identical at e0bb857a and 5527a9c6 - the delta touches no RTL, SoC, generator option or netlist input; test_soc_options.py rerun at this head with the pinned LiteX environment: 6 killed controls, RESULT: PASS (receipts/soc_options.log); the split control memory test: RESULT: PASS
[R714] PASS Robustness - run.py d1104493, build.py 96bfaacb, selftest.py df829f54 unchanged since e0bb857a; ctrl_configs.py:181-191 - the delta changes no runtime path, refusal or reuse rule; the only behavioural input it changes is the boundary gate's reason string, which the gate keys by path, and the hosted firmware-boundary job passed at the exact head (receipts/hosted_checks.tsv)
[R714] PASS Tests - harness self-test rerun at 5527a9c6: 93 PASS, 70 MUTANT caught, self-test: 0 failures, rc 0 (receipts/selftest.log); test_soc_options.py rc 0; test_ctrl_memory.py rc 0; behave 406/406; check_baremetal_only --check and --selftest rc 0 - the delta adds no test and changes no tested code; the author's real 1x1 run (comparison.txt, table.md sha256 8760d219, 18 of 18 per-group grades) matches the round-2 regrade, hash-verified against the packet manifest
[R714] PASS Docs - FR_NFR.md:5-8, README.md:120-137, ctrl_configs.py:181-191, PR body (live, equal to author-r3/PR-BODY.md except one trailing blank line) - the summary, README and reason agree with the code; docs_check, check_em_dash (0 of 380 added lines), check_doc_style, check_doc_paths, gen_toc --check and --verify-anchors, check_hygiene, check_py_idiom, check_feature_status and git diff --check all rc 0 at the head; one RESIDUE (R714-3-RES1, wording only) and two SUGGESTIONs
```

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `FR_NFR.md:5-7, :321` against the owner's corrected text; round-3 items 1-4; merge-tree recomputation; `build.py:178-211`, `ctrl_srp_image.py:80-94` against the new reason; author 1x1 receipts against README figures | R714-3 | `5527a9c66716331fd06285f428ea1a653c526ada` |
| RTL | CLEAN | RTL-, SoC- and generator-scope blobs identical to those R714-1 (`a611785f`) and R714-2 (`e0bb857a`) examined; `test_soc_options.py` and `test_ctrl_memory.py` rerun at the head | R714-3 (scope carried unchanged from R714-2 at `e0bb857a`) | `5527a9c66716331fd06285f428ea1a653c526ada` |
| Robustness | CLEAN | `run.py`, `build.py` and `selftest.py` blobs unchanged; the boundary reason edit; hosted `firmware-boundary` success at the head | R714-3 | `5527a9c66716331fd06285f428ea1a653c526ada` |
| Tests | CLEAN | Harness self-test (93 / 70 of 70), `test_soc_options.py`, `test_ctrl_memory.py`, `behave`, the bare-metal gate, all rerun at the head; author's packet receipts hash-verified | R714-3 | `5527a9c66716331fd06285f428ea1a653c526ada` |
| Docs | CLEAN (R714-3-RES1 carried as residue) | `FR_NFR.md`, harness README `:120-137`, `ctrl_configs.py` reason, live PR body; docs gates at the head | R714-3 | `5527a9c66716331fd06285f428ea1a653c526ada` |

## Real limits

- **I re-measured nothing.**
  - The 1x1 figures rest on the author's real build at this head. I verified it by manifest hash, and checked it against the README.
  - The 8x8 point, arm B, the sweep and the XIP arm rest on round 2's regrade. The delta cannot change them: no harness code, SoC or firmware blob changed.
- **`ctrl_boundary.py --require-rv32 --selftest --without verilator` did not complete locally.**
  - It ran past a 580 s foreground limit on a loaded host (rc 124, `receipts/boundary.log`, partial).
  - The exact-head hosted `firmware-boundary` job is `success`, and the author's receipt (`gates/firmware_boundary.log`, `ctrl_boundary: PASS`) is hash-verified.
- **Not run by me:**
  - `publication_census.py`: hosted `publication-census` is `success` at the head, and the author's receipt is hash-verified;
  - the builder bank, Yosys and Vivado out of context, and the four-shard sweep, because the delta changes none of their inputs.
- **Interpreters:** the first attempts of `test_soc_options.py`, `test_ctrl_memory.py` and the Markdown gates failed in the default interpreter (no `migen`, no `html5lib`). They were rerun with the pinned LiteX and Markdown interpreters, and those logs are the published ones.
- **The packet's integrity anchor is the manifest:**
  - The evidence commit `e98207b2` is unsigned on the host, so integrity rests on `MANIFEST.json`'s `published_sha256`.
  - 18 of the 135 round-3 files were downloaded and all 18 match.
  - The tree's file list equals the manifest's list.
- **Hosted checks at report time:** 31 completed successfully and 1 was skipped (physical gPTP, not run). 20 were still running or queued: the Verilator shards, the Yosys shards, `elaborate`, the `rtl-fast` aggregate and the CI manifest. Those are not evidence yet.
- **Hardware:** physical calibration was NOT RUN, and no hardware was used. Field skips are not hardware proof.
- **Source head only:** this is a source-head review. It is not the current-dev merge candidate.

## Pending manager duties

- Build and validate the current-dev merge candidate at the merge turn, with the builder and native banks. Source base: `1a635a4c`. Live dev: `97aab1d0`. Link the receipts on the PR.
- Accept the hosted and act evidence. That includes the exact-head Verilator, Yosys, `elaborate` and `rtl-fast` results still in progress.
- Carry R714-3-RES1 to the residue checklist.
- Put R714-2-S1 / R713-2-S3 (the area plan row's figures) to the owner as a question. Carry the other suggestions as optional.
- Obtain the maintainer's explicit merge authorization. No agent merges without it.

## Receipts

Every published receipt is listed in `MANIFEST.sha256`.

- `receipts/scope_blobs.txt`, `receipts/verify_delta.txt`: blob identity, the merge-tree recomputation and the lane-diff identity.
- `receipts/comment_rule_scan.txt`: the delta's added lines and the 0-hit scan.
- `receipts/packet_verify.txt`: the author packet's hash check.
- `receipts/hosted_checks.tsv`: the exact-head hosted check states at report time.
- `receipts/*.log` and `*.rc`: the gates run at the head.
- `receipts/tree_integrity.txt`: the head, the clean status, the index digest before and after, and the six submodule gitlinks unchanged.
- `scripts/verify_delta.sh <clone>` and `scripts/verify_packet.py <MANIFEST.json> <dir>` are portable reproductions.

R714-3 FINISHED
