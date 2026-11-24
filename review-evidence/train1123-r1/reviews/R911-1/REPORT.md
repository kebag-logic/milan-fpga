[R911] NEGATIVE - exact head 43076d0f8c87b5118f6f4317d000a7eebdefc967

# R911-1: internal cleared-context review of PR #988 (issue #665), the post-flip composition train

- Head `43076d0f8c87b5118f6f4317d000a7eebdefc967`, tree `c0a5e3cb0e0dfd9899e57053ad1a6f5b32f9c32e`.
- Base: live `dev-soft-core` `aa30d77f75cd97b3a29878ca0ed68010a7629266`.
- Round R911-1. All five lenses were applied independently.
- Verdict: **NEGATIVE**. One MINOR is open under `Conformance`, `Robustness` and `Tests` (F1). The rest of the composition is sound. The merges keep both sides, the combined figures are measured, the single statement raised follows the rule, and every owner bound holds.

## Scope and how it was reconstructed

Sources, in order:
1. AGENTS.md and CONTRIBUTING.md (sections 3, 5 and 6);
2. docs/README.md;
3. issue #665: the body, the owner decision of 2026-11-23 (issuecomment-7092968837), the ruling on the #958 sync's STOP (issuecomment-7093949712) and the 2026-11-20 rulings (issuecomment-7029526172, issuecomment-7044585511);
4. #969: the body, the ruling of 2026-11-22 (issuecomment-7083542634) and its amendment of 2026-11-23 (issuecomment-7116192252);
5. #818 (the route floor);
6. the diff and history `aa30d77f..43076d0f`;
7. the public packet `review-evidence/train1123-r1` at `1e47451c`: author round 1, the STOP, and author-r2, REVIEW READY;
8. the REVIEW READY on #665 (issuecomment-7117784930) and the PR body.

As instructed, the seven PRs' own content was not re-reviewed. Each was confirmed by ancestry and patch identity only.

## Findings

### F1: MINOR, lenses `Conformance`, `Robustness`, `Tests`

**What:** `kept_grade` owes every srp-bound tier-2 slice of THE TRANSMIT's build to #977. That includes a pass given whole to the build (both MRPDUs). The amendment owes the build of one only.

**Where:** `tb/verilator/ctrl_service_budget/kept_grade.py:72-75`, the `OWED_KINDS[srp-bound]` entry `"a tier-2 slice of THE TRANSMIT's build of "`. It is matched by line prefix in `Disposition.owes`, `kept_grade.py:224-227`.

**Authority and evidence:**
- #969's amendment, item 2, owes two things to #977: "the bound path's build-of-one pass and its pass over THE SHARE".
- `run.py` prints one STATED line, `"<group>: a tier-2 slice of THE TRANSMIT's build of N"`, for every build pass over `CTRL_LOOP_SLICE_US`. That covers builds of one and passes given whole alike (`slice_grade.slices`, kind `build`).
- `Disposition` owes that line by its prefix, so it never asks which kind of pass it is. kept_grade's own build check, `whole_grade.held`, holds a whole build only against `CTRL_LOOP_BUILD_PASS_US`.
- `CTRL_LOOP_BUILD_PASS_US` is above the slice at both points: 1,010 against 950 us at 1x1/1if, and 1,795 against 1,475 us at 8x8/1if (`ctrl_loop.h:362-373`).
- So a srp-bound pass that makes both MRPDUs is OWED and fails nothing, if its length falls between the slice and the whole-build cost.

**Probe** (`tools/probe_whole_slice.py`, receipt `receipts/harness/probe-whole-build-slice.txt`):
- It uses the harness's own Synthetic logs at 1x1/1if, with `slice_grade.held`, `run.stated_misses` and `Disposition`.
- Setup: a srp-bound pass of 98,000 CPU cycles with two SRP frames, against a 95,000-cycle slice and a 101,000-cycle build cost.
- In srp-bound, the line prints `OWED #977` and nothing fails.
- The same pass in srp-kept stays a failure.
- Before `ce8454cb`, the srp-bound line was a failure too.

**Impact:** At this head no figure changes. No srp-bound pass makes both MRPDUs: "BUILD srp-bound build: the heaviest pass 0" appears in all four re-grade receipts. But a regression would now pass the formal measurement as #977's registration debt instead of failing it, beyond what the ruling owes. The regression in question puts both of srp-bound's MRPDUs in one slice, against `CTRL_LOOP_BUILD_MOST` 1 and the slice design `ctrl_loop.h` states. The self-test has no case for this, so its 24 checks do not detect it.

**Answer to the executor's open question 1:** Owing the tier-2 slice line of srp-bound's *build of one* is a sound reading of item 2. It is the same pass, and at 8x8/1if its slice is the build of one's stated cost. But the implementation owes more than that pass's slice.

**Required outcome:**
- Owe srp-bound's THE TRANSMIT slice line only where its pass is a build of one. Every other srp-bound build slice over the slice stays a failure. Alternatively, publish a ruling that extends item 2 to them, and cite it.
- Add a self-test check that a srp-bound pass given whole to THE TRANSMIT's build is still a failure, with the pass over the slice and within `CTRL_LOOP_BUILD_PASS_US`.

**Verification:**
- `kept_grade.py --selftest` passes with the new check.
- The probe above reports srp-bound's line as a failure.
- The four re-grades still pass with 0 findings, with 4, 4, 5 and 6 owed, and the 171,645-cycle build of one is still owed.

### R1: RESIDUE (wording in a source comment, lens `Docs`)

**Where:** `tb/verilator/ctrl_service_budget/poll_grade.py:136` (new in `f5a1585e`), which reads "(the manager's ruling on the #958 sync's STOP, item 2)".

**Problem:** The comment cites a workflow role and an item number the public ruling does not carry for this authority. #665 issuecomment-7093949712's "The ruling" lists three bullets:
- item 2 is the trial of the owner bounds;
- the authority for raising a further statement is the third.

**Exact fix:** "(#665's ruling of 2026-11-23 on the #958 sync's STOP: a further statement over is raised by the same rule while every owner bound holds)".

No figure, test or code changes.

### R2: RESIDUE (comment rule, issue-comment ID in source, lens `Docs`)

**Where:** `tb/verilator/ctrl_service_budget/kept_grade.py:67` (new in `ce8454cb`), `AMENDED = 'https://github.com/kebag-logic/milan-fpga/issues/969#issuecomment-7116192252'`.

**Problem:** The constant is read only by the docstring and comments at lines 11, 68, 71 and 76, and no output prints it. It is a citation carrying an issue-comment ID. The owner's comment rule of 2026-10-15 excludes issue-comment IDs from source, and this is a new instance in the reviewed delta.

**Exact fix:** Cite "#969's amendment of 2026-11-23" in place of the URL, for example `AMENDED = "#969's ruling of 2026-11-23"`, and keep the link in the README and the PR.

No output changes.

### R3: RESIDUE (PR body wording, lens `Docs`)

**Where:** PR #988 body, "Linked Issue / roles", which reads "The seven PRs are superseded by this one and close unmerged once it merges."

**Problem:** PR #961 is already merged, as `dev-soft-core` `aa30d77f`, and #950 and #954 are already closed.

**Exact fix:** "The six open PRs (#958, #959, #975, #971, #978, #974) are superseded by this one and close unmerged once it merges; #961 merged on dev-soft-core at aa30d77f, which closed #950 and #954."

### S1: SUGGESTION (lens `Docs`)

**Where:**
- the PR body's references;
- `docs/design/SPLIT_CONTROL_MEMORY.md:3310`;
- `poll_grade.py:135`;
- `kept_grade.py:68`.

**Problem:** These cite the stated-cost rule as "#665's ruling item 4 of 2026-11-20". The public item 4 of 2026-11-20 (issuecomment-7029526172) is the narrow 1x1/1if margin-recovery exception. The rule itself is "the usual rule", `record_classes.rule`. The governing rulings cite it the same way (issuecomment-7093949712, and #969's amendment), so this is not this lane's defect.

**Suggestion:** Cite `record_classes.rule` and the 2026-11-23 ruling.

### S2: SUGGESTION (lens `Docs`)

**Where:** `tb/verilator/ctrl_service_budget/kept_window.py:33`, which reads "each of srp-kept's builds within its stated cost".

**Problem:** It omits that srp-bound's whole builds are still held, which `kept_grade.py`'s docstring and the README do state.

### R4: RESIDUE (PR body wording, lens `Docs`; retains R912-1's D1)

**Where:** PR #988 body, "What this PR does not touch", which reads "It makes no RTL, mailbox-contract, lwSRP or owner-bound change".

**Problem:** The diff `aa30d77f..43076d0f` carries the approved PRs' own RTL: `hdl/milan/milan_datapath.sv`, `hdl/ieee1722/aaf/*` and `hdl/ieee1722/avtp/*`, 705 insertions in all, from #959, #975 and #974. Only the composition's own commits make none.

**Exact fix:** "Its own commits after the merges make no RTL, mailbox-contract, lwSRP or owner-bound change; the RTL in the diff is the approved PRs' own (#959, #975, #974), merged unchanged."

## Prior public findings on this PR

- No review was posted on an earlier head of #988.
- The only other review is the parallel external round R912-1, POSITIVE at this same head (PR comment 7118232105, posted 00:35:45Z). It was read only after this report's verdict and ledger were written.
- **D1 (RESIDUE):** retained, as R4 above.
- **T1 (SUGGESTION):** retained as optional. It adds a self-test control where kept × 100 equals bound × 105 exactly. Here `allowed` is the floor of bound × 1.05 (`kept_grade.py:318`), so the at/past pair tests the integer boundary, but not the exact-equality case unless bound × 105 is a multiple of 100.
- R912-1 does not raise F1. This round's finding stands on its own probe and receipt, so this round leaves `Conformance`, `Robustness` and `Tests` UNCLEAN.

## What was checked, by focus item

### 1. Merges and conflict resolution

**Ancestry:**
- All seven PR heads equal GitHub's head, read today: #958 `1825ba4e`, #961 `287ca1ee` (merged), #959 `8aeb2f0b`, #975 `3cda030c`, #971 `c113018d`, #978 `87b2fc0f`, #974 `77a74b2f`.
- Each is the exact second parent of its merge commit: `c812b438`, `ee58b499` (with `64117b77`), `93c5ad84` (with `8aeb2f0b`), `8fac1fd2`, `23ee9529`, `b04610c2` and `d6c398c8`.
- `e3de632b` merges `854bd723`, and `4df6751e` merges `aa30d77f`.
- `93c5ad84` and `4df6751e` each have tree `db8dd481`, which is `f5a1585e`'s tree.
- `64117b77..8aeb2f0b` is the README's 185 -> 192 alone. It equals `b6b2e603`'s change.

**Conflict resolution:**
- `git show --remerge-diff` for all nine merges is in `receipts/merge/remerge-*.diff`.
- Every conflict hunk keeps both sides: the imports, the AECP plant tables, the Streams and Early sink fixtures (with #969's constants renamed `EARLY_S13`/`EARLY_S14` and its plant row updated), both SRP prefixes, and the CHANGELOG entries.
- The ledger hunks took the newer side and were re-derived afterwards.
- The plat README bullet "ACMP's asking-failed source flag reads false" is correctly not restored, because #954 implemented the flag.

**Executable union check** (`tools/plant_names.py` and `tools/union_check.py`, receipt `receipts/merge/plant-union-check.txt`):
- At every merge, each conflicted table holds exactly (p1 ∪ p2) less what one side removed from the merge base. The tables are `aecp_mutants.DEFECTS`, `srp_mutants.DEFECTS` and `sink_mutants.mutants`.
- Head counts: 398 AECP, 407 SRP and 36 sink rows. The 36 is the README's "36 defects", and `platsinks` runs 17 tests (12 + 3 + 2).
- The SRP campaign filters at head are the union of the two sides: #969's early prefix and #973's link prefix at 8x8/1if, and #973's prefix at 1x1 with one interface, as on #973's branch.

**Composed figures, re-derived from measurement:**
- `c2b2ba1a`'s ledger gives `ctrl_plat` 18,048, 19,840, 19,136 and 21,888 B, and 8x8 entries of 64.5, 59.5 and 57.5.
- These equal `plat_ledger`'s measured lines at head (author-r2 `ledger/plat-ledger-43076d0f.txt`: PASS, 0 findings, 24 of 24 image hashes identical to `f5a1585e`'s).
- They also equal the builder's own refusal at `d6c398c8`: 57.5 RAMB36, 133,128 B of rom (author `ledger/fixture-sizes-d6c398c8.txt`).
- The S14 debts of 3.5, 8.5 and 1.5 are arithmetic on the entries, not on the PRs' figures.

**The two gate findings and their fixes:**
- `0ad0bf2d` classifies `sw/litex/mac_link_status.py` OUTSIDE. The file imports no LiteX and compiles nothing. It is byte-identical at #974's head, where `ctrl_configs.py` lacks the entry.
- `b6b2e603` sets the README's pin count to 192, the figure the self-test measures.
- The author's `ctrl_boundary` receipt at head (author-r2 `gates/ctrl-boundary-43076d0f.txt`) shows PASS, with 0 findings and 117 boundary, 192 pin and 4 figure controls. It was not re-run here (see Limits).

### 2. Statement changes

- `poll_grade.EIGHT_ONE['aecp_long']` goes from 320 to 325 us. `record_classes.rule(30,948, 100 MHz)` = 325 (309.48 us × 1.05 = 324.95, rounded up to 5).
- Authority: the third bullet of the #958-sync ruling, which raises a further statement only while every owner bound holds.
- In the 8x8/1if survey of the formal measurement (author `budget/cpu-8x8-1if-formal-c2b2ba1a.md`), every other statement is within. The only other row over is `record.srp` from `srp-kept.log`, which #969 owes to #977.
- 1x1/1if has 0 statements exceeded.
- `edit_rows.PACED` holds at 305 of 315 us, and `rows_tiers.LONG_RECORD_US` at 900 of 1,720 us.
- In the delta, the only statement-file change outside the PRs' own commits is `f5a1585e`'s. `c812b438` brings exactly #961's statement edits, byte for byte.
- `ctrl_loop.h`'s constants and every owner bound are untouched by the composition commits.

### 3. #969's amendment in `kept_grade.py` (`ce8454cb`)

What holds:
- `kept_within` is `kept*100 <= bound*105`, which is exact integer arithmetic.
- Allowance check: 142,137 × 1.05 gives 149,243, and the margin is 6,661.
- srp-bound's build of one is owed through `BOUND_OWED_BUILDS` and `OWED_KINDS`, and srp-bound's SHARE passes are owed through `shares`.
- srp-kept's builds and SHARE passes are still findings, and so are idle runs and whole builds over `CTRL_LOOP_BUILD_PASS_US`.
- No constant or bound is restated.

Run here:
- `--selftest`: PASS, 24 checks, including the 4 % and 6 % checks and bound + 5 % against one cycle more (`receipts/harness/kept-selftest.txt`).

What does not hold: F1, above.

### 4. The formal CPU budget, every arm and group (490 groups)

Author receipts:
- 245 groups at each point, in 12 legs a point; each leg's image is one ELF hash.
- 0 refusals.
- The only budget misses are the 7 held-egress `backlog-owed` rows.
- Passes over THE SHARE: 0 at 1x1/1if, and 2 of 737,682 at 8x8/1if, both srp-bound's (216,785 and 203,961 cycles), owed.
- The arm A legs' images (`df247549…` at 1x1, `0e263f65…` at 8x8) are the head's split-soc mapped images in the plat_ledger receipt.

Reproduced here at head (`receipts/harness/`):
- `load_grade --check`: 0.512 of 0.70 and 0.744 of 0.75.
- `flip_grade --check 1x1/1if`: last queued notice 127.43 of 130 ms, ACMP 29.15 of 30, txL 47.98 of 49.
- `flip_grade --check 8x8/1if`: THE TRANSMIT 76.86 of 77 ms.
- `shape_costs --check`: PASS.
- The record_classes, flip, load and shape `--selftest`s each PASS (26, 616, 28 and 25 planted controls).
- `run.py --self-test`: all 295 mutants caught. 143 were caught in the full run, whose base checks had 0 FAIL, before it was stopped by this session's time limit. The other 152 were caught in 12 slices through the same `selftest.mutated`/`checks` loop (`tools/selftest_slice.py`), with 0 escaped. Round 2's "295" is the right figure.
- The re-grades (author-r2 `budget/kept-grade-*-r2.txt`, `run-regrade-*-r2.txt`) give 0 findings with 4, 4, 5 and 6 owed. They match the PR body.

### 5. Gates

Run here at head (`receipts/docs/`):
- `docs_check.py`: 0 findings over 223 pages.
- `check_em_dash.py --base aa30d77f`: 0 findings over 762 added lines, the author's figure.
- `check_doc_style.py`: OK.
- The SV, C/C++, Python and Shell idiom gates: rc 0 each.

Taken from author receipts (not runnable here, see Limits):
- the four firmware shards at `f5a1585e`;
- `fw_coverage`, the builder union, the twin, the Verilator suites, split boot and `nvm_split_target` at `c2b2ba1a`;
- `ctrl_boundary` and `plat_ledger` at head.

Inputs since those heads:
- `git diff f5a1585e..HEAD` touches only `kept_grade.py`, `kept_window.py`, the harness README and the design page. Nothing under `sw/` reads them.
- After `c2b2ba1a`, the changes are text in `ctrl_memory.py`'s notes, the `test_ctrl_memory.py` and `sink_mutants.py` docstrings, and `ctrl_configs.OUTSIDE`.

Routes (author `route/*/signoff.txt`, c2b2ba1a images):
- 8x8/1if ExtraPostPlacementOpt: Slow +0.105/+0.102 ns, 46,621 LUT.
- 1x1/1if ExtraTimingOpt: +0.384/+0.102 ns, 32,680 LUT. Its ExtraPostPlacementOpt route, at +0.019 ns, was not selected.
- Both meet #818's floor on the best directive.
- The RTL and firmware inputs are unchanged at head.

### 6. PR body against the packet

- The PR body is byte-identical to author-r2 `PR-BODY.md`.
- Its figures match the receipts and the code: entries, `ctrl_plat`, the 133,128 B fixture, 325 us, 192, the margins, and 86,018 and 81,655 cycles.
- The `Closes` lines are the seven PRs' own.
- Two wording defects: R3 and R4.

### Concurrency, privacy, comment rule

- The formal legs run every group at the full 8x8 and 1x1 shapes on the composed image. That is the harness's every-stream load. This review ran no simulation of its own.
- No host, device, tool or model name appears in the delta's source.
- The only new comment-rule instances in the composition's own commits are R1 and R2. The PRs' own pre-existing instances are tracked by #746.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | `kept_grade.py:67-77,129-196,206-236` against #969 issuecomment-7116192252 items 1-3; `poll_grade.py:133-138` against the rule and #665 issuecomment-7093949712; `ctrl_memory.py`/`ctrl_memory_ledger.py` entries against plat_ledger's measured lines; the formal receipts' survey | R911-1 | `43076d0f8c87b5118f6f4317d000a7eebdefc967` |
| RTL | CLEAN | `git log aa30d77f..HEAD -- hdl sw/litex/milan_soc.py sw/litex/mac_link_status.py`: every commit is in #959 `64117b77`, #975 `3cda030c` or #974 `77a74b2f`. Each merge's `hdl/` diff equals its PR side's. No composition commit touches gateware. Gitlinks are unchanged from `aa30d77f` (tsn-c-stack `715589c1`). The route signoffs at `c2b2ba1a` meet #818's floor, with inputs identical at head | R911-1 | `43076d0f8c87b5118f6f4317d000a7eebdefc967` |
| Robustness | UNCLEAN (F1) | `Disposition` and `held` breach paths: graded alone, a condition broken, a whole build over its cost, idle runs, the at/past boundary of the 5 %; `kept_within` integer bounds; probe `receipts/harness/probe-whole-build-slice.txt` | R911-1 | `43076d0f8c87b5118f6f4317d000a7eebdefc967` |
| Tests | UNCLEAN (F1) | `kept_grade.py --selftest` (24 checks, run); the five grader `--selftest`s and three `--check`s (run); `run.py --self-test`, 295 of 295 mutants caught (run); `receipts/merge/plant-union-check.txt` (run); author shard, boundary and ledger receipts | R911-1 | `43076d0f8c87b5118f6f4317d000a7eebdefc967` |
| Docs | CLEAN (R1-R4 RESIDUE, S1-S2 SUGGESTION) | `docs_check`, em-dash, doc-style and idiom gates (run); `SPLIT_CONTROL_MEMORY.md` sections 3, 5 and 13; `tb/verilator/ctrl_service_budget/README.md:779-796`; `sw/firmware/ctrl/plat/README.md:161-163` (36 and 17 against the tables); `sw/firmware/ctrl/README.md:255` (192); the PR body against the packet | R911-1 | `43076d0f8c87b5118f6f4317d000a7eebdefc967` |

## Real limits

- **Not runnable on this host:** `plat_ledger`, `ctrl_boundary --require-rv32`, the firmware gate's four shards, `fw_coverage`, the builder union, the twin, the Verilator suites, split boot and `nvm_split_target`. No RV32 toolchain or LiteX environment is installed. `sw/litex/test_ctrl_memory.py` stops at `import migen` (`receipts/harness/test-ctrl-memory.txt`, rc 1, environment). For these gates this review relies on the author's published receipts and on the input-identity checks above.
- **Not re-run:** no CPU-budget leg was simulated here. The formal figures are the author's logs, re-graded by the author. This review reproduced the grader checks at head and the kept_grade logic on synthetic logs.
- **No route was run.**
- **Not hardware proof:** physical calibration was NOT RUN, and the bench and in-house qualification for #969, #972 and #973 is not covered. Field skips are not hardware proof.
- **#977 is owed:** THE SHARE and the build slice must clear on the composed head before the post-flip in-house qualification closes.
- **No manager source bank** exists at this head, and none is claimed or inferred.

## Pending manager duties

- Rule on F1, or take its fix through a round. The fix needs a re-review of `kept_grade.py` at the new head.
- Carry R1-R4 to the residue checklist.
- Validate the current-dev merge candidate. The source base is `aa30d77f`; live dev is `e275d795`. This means the builder and native banks, with hosted and act acceptance.
- File the output-map Issue (author-r2 `ISSUE-output-map.md`).
- Track #977 before the qualification closes.

R911-1 FINISHED
