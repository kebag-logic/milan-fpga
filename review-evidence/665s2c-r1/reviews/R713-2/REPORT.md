[R713] NEGATIVE - exact head e0bb857a9f4b8e9d29736970a1135afde03260c5

# R713-2: internal cleared-context review of PR #796 (issue #665, lane S2c), round 2

- **Head:** `e0bb857a9f4b8e9d29736970a1135afde03260c5`, tree `e183ba210eb7e9e8e408da9ad0268b307f98646c`.
- **Source base:** `f58d049beb377c3f535628067022d4d5b51e8208` (S2's final head, PR #792).
- **Previously reviewed head:** `a611785f2afe5bbe587f74034d869e869a1c8d37` (R713-1, R714-1).
- **This round's delta:** `a611785f..e0bb857a`, seven commits, 9 files, +219 / -57.
- **Verdict basis:** one open MINOR (R713-2-F1, `Docs` and `Conformance`). Every prior finding (R713-1-F1 to F4, R714-1-F1 and F2) is resolved at this head, and so is every prior residue item. `RTL`, `Robustness` and `Tests` are covered clean at this head.

## What the task is, reconstructed from public state

- **S2c assignment** (issue #665, issuecomment-6421463860), items 1 to 5:
  - give the split SoC's VexiiRiscv an L1 instruction cache through the pinned generator's own options, with the all-fabric CPU byte-identical and #791's decode respected;
  - measure it on S2's harness at both points, sweeping at least two sizes, and price it in Yosys and out of context against the tile ledger;
  - measure a hybrid-XIP arm;
  - state the remaining T_svc gap;
  - leave firmware behaviour, firmware tests and the mailbox contract unchanged.
- **Round-2 assignment** (issuecomment-6433542516) answers R713-1 and R714-1:
  - F1: lower-bound labels on the unbounded rows;
  - F2: the block-RAM rate;
  - F3: S2's commands select the cacheless core;
  - F4: the reuse refusal is exercised and mutated;
  - R714-1-F1: the geometry is pinned exactly;
  - the residue items.
  - No new measurement is allowed.
- **Owner decision, 2026-10-27** (issuecomment-6434741232, corrected by issuecomment-6434744436): amend NFR-SCOUT-01 to "The release architecture MUST use one RV32I control hart: in the split placement it has a 4 KiB direct-mapped instruction cache (64-byte lines, one refill at a time) and no data cache; in the all-fabric placement it stays cacheless". It also lists edits to `ARCHITECTURE_HW_SW_SPLIT.md` "wherever it repeats 'cacheless'", to `MARK_II_AREA_PLAN.md:383` and to `SPLIT_CONTROL_MEMORY.md:243`. `docs/history/` is not edited.
- **Authorities read:**
  - AGENTS.md;
  - `docs/reference/FR_NFR.md` (NFR-SCOUT-01, 3.4.1);
  - `docs/ARCHITECTURE_HW_SW_SPLIT.md`;
  - `docs/design/SPLIT_CONTROL_MEMORY.md` section 7;
  - the `MARK_II_AREA_PLAN.md` ledger;
  - the harness README.
- **Public evidence:**
  - the author's round-2 handoffs and receipts under `review-evidence/665s2c-r1` at `50e47e55` (`author-r2/a685c`, `author-r2/a685d`);
  - the archived regrade tables (`author/receipts/regrade/arms/*`).
  - Every file used here was fetched and its sha256 matched the published `MANIFEST.json` (`receipts/evidence_fetch.txt`, all OK).

My own pass over the diff came first. I read the prior public review reports (R713-1, R714-1) only after it, to resolve or retain their findings.

## Findings

### R713-2-F1 MINOR - Docs, Conformance - `docs/reference/FR_NFR.md:6` (and the PR body's Status) - the requirements page's summary still states a cacheless control hart, contradicting the amended NFR-SCOUT-01 row on the same page

- **Requirement/evidence:**
  - `FR_NFR.md:321`, as amended at this head, says that in the split placement the hart has a 4 KiB direct-mapped instruction cache and no data cache, and that in the all-fabric placement it stays cacheless.
  - The page's own introduction, `FR_NFR.md:5-8`, still reads "The release uses one cacheless RV32I control hart and scales media capacity through fabric stream contexts ...". That sentence summarises NFR-SCOUT-01: its second clause restates NFR-SCOUT-01's second sentence.
  - The PR body's Status says "There is no open requirement conflict".
  - The executor raised this line publicly as an open risk (issuecomment-6435396245). The owner's amendment did not list it, so the executor correctly did not edit it. A published open question does not resolve the inconsistency, though: the tree still states two different hart requirements on the one authoritative page.
  - AGENTS.md section 6, `Docs` lens: "Changed contracts are reflected in authoritative docs".
  - This is a requirement claim, not wording only, so it is not RESIDUE.
- **Impact:** a reader of the requirements page gets "cacheless" from the summary and "4 KiB instruction cache" from the normative row. The PR states there is no open conflict while one remains in the tree.
- **Required outcome:**
  - `FR_NFR.md:6` agrees with the amended NFR-SCOUT-01, or the owner records publicly that it stays as written. Example text: "The release uses one RV32I control hart (NFR-SCOUT-01: cacheless in the all-fabric placement, with a 4 KiB instruction cache in the split placement) and scales media capacity ...".
  - Because the owner's listed edits omit this line, the manager obtains the owner's assent first.
  - The PR body's "no open requirement conflict" matches the outcome.
- **Verification:**
  - `grep -n cacheless docs/reference/FR_NFR.md` shows no statement that contradicts row NFR-SCOUT-01;
  - the docs gates and `sw/litex/test_ctrl_memory.py` stay rc 0.

### RESIDUE

None new in this delta.

- The comment-rule scan of every source line added since `f58d049b` (`*.py`, `*.cpp`, `*.vlt`, `*.c`, `*.h`, `*.sv`, `*.ld`) finds no lane label, review round, reviewer ID or comment ID.
- The only hits are `build.py:149` and `:151`. They cite "decision D3", an owner decision ID, which R714-1 RES1's exact text requested.

### SUGGESTION (optional; does not affect the verdict or any lens)

- **R713-2-S1 - Robustness, Tests: open suggestions carried forward.**
  - **R713-1-S2:** reuse compares the label `split`, not the geometry it resolved to.
  - **R713-1-S3:** `--xip --fetch-l1 none` is accepted.
  - **R713-1-S4 and R714-1-S1:** the refill-wait accounting in `sim_main.cpp` is not gated.
  - **R714-1-S2:** `xip_offset()` is not covered.
  - The author's replay (`author-r2/a685c/receipts/probes/r713_harness_probes.txt`) confirms that the five related probes still survive.
  - R713-1-S1 is answered by R714-1-F1's fix.
- **R713-2-S2 - Tests: `split` and `64x1` count as different builds.**
  - The new reuse check pins the refusal of a `64x1 --xip` build under `--xip` (`selftest.py:825-857`, `cache_build_checks`). Those two labels build the same CPU.
  - The refusal is conservative and correct today.
  - If R713-1-S2 is taken and identity becomes the resolved geometry, this case's expectation must change with it.
- **R713-2-S3 - Docs: `MARK_II_AREA_PLAN.md:383` labels figures from the cacheless hart.**
  - The row now carries the owner's text "NFR-SCOUT-01: one RV32I hart, 4 KiB instruction cache, no data cache".
  - Its figures (3,522 LUT / 4,736 FF) come from the pre-split inventory of the cacheless hart, which the all-fabric placement keeps. The executor noted this.
  - The owner's wording governs. A placement qualifier ("split: 4 KiB instruction cache") would stop the row from implying that the measured core has the cache. That change needs the owner.
- **R713-2-S4 - Docs: cacheless wording outside the amendment's list.**
  - `docs/litex/LITEX_SOC.md:11` ("`milan_soc.py` builds the supported target: a cacheless RV32 VexiiRiscv") and `sw/README.md:3` ("The product is one cacheless RV32I VexiiRiscv hart") are true of the shipping all-fabric build.
  - `milan_soc.py --ctrl-mailbox` now builds a cached hart.
  - A short qualifier, "(all-fabric; the split placement's hart has a 4 KiB instruction cache, NFR-SCOUT-01)", would keep these pages aligned.
- **R713-2-S5 - Tests: cite the clause in the restated options.**
  - `sw/builder/test_soc_options.py:22-26` restates the split options "on purpose", citing #665, the design doc and the ledger.
  - It could now also cite NFR-SCOUT-01, which since this head makes that geometry normative.

## Prior public findings: resolved or retained at this head

| Finding | Status at `e0bb857a` | Evidence |
|---|---|---|
| R713-1-F1 (Conformance, Docs): unbounded rows shown as measured ceiling misses | **Resolved** | `scripts/check_miss_rows.py` compares all 47 rows of the README's two miss tables with the archived P1/P8 none and 64x1 regrade `table.md` files: 0 problems (`receipts/miss_rows_check.txt`). Every value matches within 0.006 ms. The six unbounded rows carry "at least X, never answered/never released" in both ms columns and in their cycles cell. No bounded row is mislabelled. |
| R713-1-F2 / R714-1-F2 (Docs): block-RAM rate | **Resolved** | `README.md:769` gives "one tile for each 4 KiB of data and half a tile of tags for each way". All 8 rows of the table at `:757-764` satisfy 4.5 + size/4 KiB + 0.5 per way (5.5, 6, 7, 7.5, 9, 9.5, 13). |
| R713-1-F3 (Docs, Tests): S2's commands do not reproduce their figures | **Resolved** | The Results block (`:188-191`), the controls (`:924-930`) and the fixture regeneration (`:915-918`) select `--fetch-l1 none`. The cache controls name `--fetch-l1 64x1` (`:797`). Hash-verified author reruns: `C1-slow-none.log` shows `vexii_args='--xlen=32'` and `BUDGET control.discover.if0: 24.614 ms`, caught. `fixture_identity.txt` regenerates both committed files with an empty `git status`, at `619e84e6`. Since `619e84e6` only four docs and one `selftest.py` docstring line have changed, and the fixture blobs at the head (`d3b45a3b`, `0d8d1d64`) equal those recorded. |
| R713-1-F4 (Tests): reuse refusal never exercised | **Resolved** | `selftest.py:764-857` (`main_verdict`, `built`, `cache_build_checks`) drives `run.main()` on temporary builds. Eight disposable source mutants of my own (`scripts/probe_reuse_build.sh`, `receipts/mutants/*.verdict`) are **all killed**: refusal removed, `built_as` defaulting to `split`, `built_as` or `selected` dropping `xip`, `selected` dropping the fetch L1, `run.main` building without `xip`, `build.build` handing `split` to the SoC, and `build.json` recording `xip = False`. Both of R713-1's original mutants are among them. |
| R714-1-F1 (Tests): geometry not pinned | **Resolved** | `test_soc_options.py:26` restates `SPLIT_FETCH_L1`, and `:234-235` require it literally for both the constructor's options and `ctrl_cpu_args`. My run at the head (LiteX environment): `RESULT: PASS` with 6 killed controls, including 128 sets, 2 ways and 32 sets (`receipts/soc_options_head.log`). |
| R714-1 RES1 / R713-1-RS1 | **Resolved** | `build.py:149-151`: "(#665, decision D3)" and "the saved-state flash driver (nvm_flash_litespi.c)". RES1's text was chosen over RS1's. Both remove the lane names, so I accept it. |
| R714-1 RES2 | **Resolved** | `README.md:746` and the PR body's XIP bullet carry RES2's exact text. |
| R713-1-RS2 to RS4 | **Resolved** | `MARK_II_AREA_PLAN.md:897-898` ("All four", "None of these numbers"); PR body Status ("cuts ... by a third to a half"); `README.md:741`, `:745` and PR body ("a CPU of 13 tiles"). |
| R713-1-S1 to S4, R714-1-S1, S2 | S1 answered by R714-1-F1; the others are retained as suggestions (R713-2-S1) | Optional by definition. |

## Lens results with evidence

- `[R713] PASS RTL` - `sw/litex/milan_soc.py` (byte-identical to `a611785f`, `receipts/scope_unchanged.txt`), `sw/builder/test_soc_options.py:26,234-235`, `docs/reference/FR_NFR.md:321` - what was checked:
  - The amended NFR-SCOUT-01 now states the RTL R713-1 verified at `a611785f`: FetchL1Plugin with 64 sets and 1 way, the generator's 64-byte line, one refill slot, no prefetch, no LSU L1, and patch 0005's non-coherent fabric kept.
  - Since that head, nothing in `sw/litex`, `hdl`, `configs`, `sw/firmware`, `sw/mailbox`, `split_soc.py`, `sim_main.cpp`, `observe.vlt`, `run.py`, `scenario.py` or `grade.py` has changed.
  - The option test at the head pins the split's literal options and the all-fabric `--xlen=32`, which together make up the amended clause's split and all-fabric halves. No STOP condition applies: no generator change and no all-fabric change.
- `[R713] PASS Robustness` - `tb/verilator/ctrl_service_budget/run.py:285-321`, `build.py:496-520` (AST-identical to `a611785f`), `selftest.py:764-857`; `receipts/mutants/` - what was checked:
  - The delta changes no runtime path; `build.py` differs only in comments.
  - The new checks exercise the reuse refusal on the invalid-state inputs: a mismatched fetch L1, a mismatched arm, a legacy build that records neither key, and the default `split` against a cacheless build. Every refusal exits 2 with the named message, and the matching selection reuses.
  - All eight of my mutants of these paths are killed.
  - The self-test's patches of `sys.argv`, `os.environ`, `sys.modules`, `sys.path` and `build.*` are scoped by context managers. The tree is clean after the run.
- `[R713] PASS Tests` - `receipts/selftest_head.log`, `receipts/soc_options_head.log`, `receipts/mutants/*`, `receipts/mutant_table_xcheck.txt` - what was checked:
  - **Self-test at the head:** rc 0, 93 `PASS`, 70 `MUTANT caught`, `self-test: 0 failures`. Sorted line-by-line, it is identical to the author's hash-verified `author-r2/a685d/receipts/gates/harness_selftest.log` at the same head.
  - **Mutant coverage:** each of the 70 caught mutants matches a README mutant-table row and its named check. The one paraphrased row is S2's `composition` row, identical at the base `f58d049b`.
  - **Counts since the base:** 6 cache checks and 8 new mutants, as the PR body states.
  - Each new check fails for the defect it names (my eight killed mutants). The option test kills its six controls.
  - **Bare-metal scope gate:** `scripts/check_baremetal_only.py --check` rc 0.
- **Conformance - UNCLEAN (R713-2-F1).** What was checked:
  - **The NFR-SCOUT-01 edits:**
    - `FR_NFR.md:321` equals the owner's corrected text verbatim, and the rest of its row is unchanged;
    - `ARCHITECTURE_HW_SW_SPLIT.md:62` uses the same wording with "uses", and it is the page's only "cacheless";
    - `MARK_II_AREA_PLAN.md:383` carries the owner's text verbatim;
    - `SPLIT_CONTROL_MEMORY.md:243-247` records the amendment, its correction and the re-decision condition;
    - `docs/history/` is untouched.
  - **Round-2 items 1 to 6:** met (table above). No measured cycle count changed in the delta: the README hunks change labels and commands only, and every value equals the archive.
  - **Open:** `FR_NFR.md:6`.
- **Docs - UNCLEAN (R713-2-F1).** What was checked:
  - **Gates at the head, rc 0 each:**
    - `docs_check.py` (0 findings);
    - `check_em_dash.py --base f58d049b` with the pinned renderer (0 findings over 376 added lines);
    - `check_doc_style.py`;
    - `sw/litex/test_ctrl_memory.py`, which reads the amended design doc (`RESULT: PASS`);
    - `git diff --check f58d049b HEAD`.
  - **README:**
    - the new prose agrees with the arm labels (A, B, S at `:585-590`) and the self-test's checks list;
    - the tile rate agrees with its table;
    - the XIP conclusion is RES2's text.
  - **PR body:** its counts are correct (93 checks, 70 mutants, 6 controls, 6 cache checks, 8 mutants). The exception is the "no open requirement conflict" sentence (F1).

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R713-2-F1 open) | issue #665 S2c and round-2 assignments; owner amendment and correction; `FR_NFR.md:6,321`; `ARCHITECTURE_HW_SW_SPLIT.md:62`; `MARK_II_AREA_PLAN.md:383`; `SPLIT_CONTROL_MEMORY.md:243-247`; README miss tables against archived regrades | R713-2 | `e0bb857a9f4b8e9d29736970a1135afde03260c5` |
| RTL | CLEAN | `milan_soc.py` (unchanged since `a611785f`, where R713-1 verified generator options, netlists and out-of-context timing); `test_soc_options.py` at the head; amended NFR-SCOUT-01 | R713-2 (re-applied over R713-1's depth) | `e0bb857a9f4b8e9d29736970a1135afde03260c5` |
| Robustness | CLEAN | `run.py:285-321`, `build.py` (AST-identical), `selftest.py:764-857`; 8 killed reviewer mutants | R713-2 | `e0bb857a9f4b8e9d29736970a1135afde03260c5` |
| Tests | CLEAN | self-test (93 / 70); `test_soc_options.py` (6 controls); 8 reviewer mutants; mutant-table cross-check; author receipts hash-verified | R713-2 | `e0bb857a9f4b8e9d29736970a1135afde03260c5` |
| Docs | UNCLEAN (R713-2-F1 open) | harness README delta; four amended pages; PR body; docs gates at the head | R713-2 | `e0bb857a9f4b8e9d29736970a1135afde03260c5` |

## Real limits

- **No harness point, sweep, control or XIP arm was re-executed by this round.** No measured figure changed in the delta. Figures were checked against the hash-verified archived regrades and the author's hash-verified reruns (`C1-slow-none`, fixture identity). R713-1's independent reruns at `a611785f` (1x1 none and 64x1, two controls) cover runtime code that is unchanged since.
- **Not run by this round:**
  - Vivado, Yosys and the all-fabric export digest;
  - `test_builder.py --require-rv32` (the author ran it at `de91db59`, and none of its inputs changed after that);
  - behave and the four-shard sweep;
  - any hardware or bench work.
  - Physical calibration was NOT RUN, and field skips are not hardware proof.
- **No manager source bank ran at this head, and none is claimed.**
- **Hosted contexts at the exact head** (read-only snapshot, `receipts/hosted_check_runs.tsv`): 13 queued and 1 in progress, none concluded. No hosted result is claimed.
- **Two tests needed outside environments.** `sw/builder/test_soc_options.py` and `sw/litex/test_ctrl_memory.py` need LiteX (`migen`), so they ran in the existing LiteX Python environment, read-only. Under the plain system interpreter they fail at import. `check_em_dash.py` ran in the pinned Markdown renderer's environment.
- **Clone state:** HEAD, its tree, the index `write-tree` and all six gitlinks equal the head, and the status is clean (`receipts/clone_integrity.txt`). Probes ran only on `git archive` copies under the packet's scratch directory.

## Pending manager duties

- Route R713-2-F1 to the owner (`FR_NFR.md:6`, outside the amendment's listed edits), then have it applied or the owner's ruling recorded. The PR body's "no open requirement conflict" follows the outcome.
- Build and validate the current-dev merge candidate (source base `f58d049b`; live dev `97aab1d0f28bd753a3e11df6278d5cac54f964dd`) with its builder and native banks at the merge turn, and link the receipts.
- Accept or diagnose the exact-head hosted contexts, which were still queued at this snapshot.
- PR #792 merges first. The integrated route for the cache's 1.5 tiles is M8a-2's.
- Carry the suggestions R713-2-S1 to S5 as optional.

R713-2 FINISHED
