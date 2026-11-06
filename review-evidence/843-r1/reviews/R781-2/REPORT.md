[R781] POSITIVE - exact head 1105f54546b2f19d9577b7fad902c908e34f88ee

# [R781] Internal cleared-context review, round R781-2: PR #846 / issue #843

- Head: `1105f54546b2f19d9577b7fad902c908e34f88ee`, tree `94be1980e4b837611cb08bc30b0d5dee1b5ecc7f`. Base and live dev: `cc204c6fd2349b543d73f15c97162a2c4434c86e`.
- This is the same head R781-1 reviewed. Only the PR body changed, to answer R781-1 F1.
- Verdict: POSITIVE.
  - F1 is resolved at its cause: the body's Status head and its checkout now name this head, and the gate figures that were measured at this head are bound to it.
  - Two wording items remain. Both are RESIDUE (W1, W2), so neither leaves a lens unclean. W1 is the route table and the mutant count, which say "this head" but were measured at `8210abaa`. I checked that nothing they depend on changed between `8210abaa` and this head (see W1), so every figure and verdict still holds at this head. W2 is the stale reviewer roles.
  - S1 is retained as a SUGGESTION.
  - No tree change since R781-1, so every tree artifact keeps its R781-1 lens verdict.

## Scope of this round

- Delta since the previously reviewed head: none in the tree (same SHA, `git status` clean, gitlinks unchanged). The only delta is the PR #846 body, edited at 2026-11-06T09:15:20Z (`receipts/pr846_view.json`, `receipts/pr846_body.md`).
- Issue #843 acceptance and scope (`receipts/issue843_body.md`): re-read. The issue has no maintainer or manager comment since R781-1 (`receipts/issue843_comments.json`: the TAKEN and REVIEW READY comments only).
- I checked the body against the public evidence tree at `3b2b1ef2` (`review-evidence/843-r1/author/receipts/*`) and against `git diff` in this clone. `scripts/check_body_binding.sh` reproduces this check, with output in `receipts/body_binding.txt`.
- I read the prior finding (R781-1, `receipts/r781-1_comment.md`) only after my own pass over the body was done.

## Body figure binding (focus check)

| Body statement (line in `receipts/pr846_body.md`) | Receipt and the commit it was measured at | Bound correctly? |
|---|---|---|
| Status head `1105f545` (16); checkout `--detach 1105f545` (67) | `gh pr view` headRefOid `1105f54546b2...` | yes |
| Sweep, four shards: 0, 1, 3 exit 0; shard 2 exit 92 (capture_coherence timeout), re-run 17/17; 65 suites (18) | `sweep-1105f545/shard-*/complete.json` all `"head": "1105f545..."`. Shard 2 `results.json` exit 92, its 01.log shows `TIMEOUT capture_coherence`. The rerun shows `17 passed, 0 timed out`. 15+17+17+16 = 65 | yes |
| milan_dp gptp / gptp-lat 212/212, gptp_shadow 326/326, gptp_plane 31/31, fw_service_budget 55 + 14 (19) | Inside the `sweep-1105f545` shards. The milan_dp `run` target includes both leg images (`tb/verilator/milan_dp/Makefile:739`). The full shard-0 milan_dp.log is published by hash only. gptp_shadow is 326/326 in shard-1, gptp_plane 31/31 in the shard-2 rerun, and fw_service_budget 14 + 55 in the shard-2 rerun and in `final-gates-1105f545/fw_service_budget.log` (`# head 1105f545`). R781-1 also ran all five at this head | yes |
| Builder bank `ALL GATES PASS EXCEPT 2 NOT RUN` and the other final gates rc 0 (20, 92) | `final-gates-1105f545/*.rc`: all 0. `builder.log` line 1 reads `# head 1105f545`, lines 619-622 show the gate 1b MAKEFLAGS arm and gate 11 (`receipts/builder_not_run.txt`). behave: 14 features, 508 scenarios | yes |
| docs workflow 65 rc 0 / 31 not run / 0 bad (21) | `docs-yml-1105f545/verify.md:100`; `docs-check__tree-after.txt` reads `head 1105f545` | yes |
| Physical gPTP 151 + 6 + 20 + 14 + 14 (22) | `physical-gptp-4c4c5982/milan_dp_gptp.log` reads `# head 4c4c5982`. The body says "at the parent of this head", and `4c4c5982` is the parent. `git diff --name-only 4c4c5982 1105f545` lists only `tb/verilator/fw_service_budget/oracle.json`, which nothing under `tb/verilator/milan_dp_gptp` reads | yes (relative wording only; see W1 for naming the SHA) |
| Eight planted mutants, ten check runs (23, 52) | `mutants-8210abaa/mutants.json`: 8 rows, 10 checks, all `caught: true`. The body does not name a commit | **no**: see W1 |
| Route table column "this head", and "At this head the slow corners..." (104-114) | `route-head/bank.out` line 2 is `8210abaa...`. `route-dev/bank.out` is `cc204c6f` and matches the "dev" column. Every figure matches the receipts: LUT 52,695/51,994, FF 54,288/54,101, slices 15,846/15,841, DSP 15/13, WNS +0.018/+0.236, WHS +0.015/+0.036. The resource gate rows for LUT +683 > 500, DSP +2 > 0 and the WNS floor match too | **no**: measured at `8210abaa`, labelled "this head"; see W1 |

## Prior findings, resolved or retained at this head

- **R781-1 F1 (MINOR, Docs): RESOLVED.**
  - The cause was a green verdict and a checkout bound to `4c4c5982`, where `fw_service_budget` fails.
  - Status and checkout now name `1105f545`. The body no longer contains `4c4c598273904f6c994b75c860e74ac742ae49d2` (`receipts/body_binding.txt`).
  - That head's published sweep (after the shard-2 rerun) and its `fw_service_budget` receipt exit 0.
  - The physical suite stays stated as run at the parent, with the reason.
  - F1's broader requirement that every figure be bound to its measured commit is met except for the route and mutant figures. Those stay true at this head, so they are carried as W1 RESIDUE, not as a reopened MINOR.
- **R781-1 S1 (SUGGESTION, Robustness): RETAINED unchanged.** `sw/builder/endstation_builder.py:3725` coerces `gptp.clock_accuracy` with `int()`. The code is unchanged, so the R781-1 evidence stands.

## Findings

### W1 - RESIDUE - Docs - PR #846 body, Status bullet "Eight planted mutants" (line 23), Description line 52, and the "Known limitations" route table and paragraph (lines 102-114) - route and mutant figures are stated as "this head" but were measured at `8210abaa`

- Evidence:
  - `route-head/bank.out` line 2 is `8210abaa1f5664bc6f755043b19a34a4eb38ede2`.
  - The mutant receipts sit in `mutants-8210abaa/`.
  - The body's table column header is "this head", and its Status line binds "head `1105f545`".
- Why RESIDUE and not MINOR: no figure or verdict changes at this head.
  - `git diff --stat 8210abaa 1105f545` touches only `CHANGELOG.md`, `docs/DOCUMENTATION_AUDIT.md`, `docs/design/AREA_BUDGET.md`, `docs/reference/SUBMODULES.md`, `sw/builder/test_clock_contract.py` and `tb/verilator/fw_service_budget/oracle.json`.
  - None of those files is a route input. All six gitlinks are equal: `route-head/bank.out` against `git ls-files -s`. The build reads only submodule pins from git, not the parent commit (`syn/yosys/ooc.sh:383-387`, `syn/yosys/ooc_harness.py:96-98`).
  - None of them is a mutated file or a mutant's catching check. The mutants plant changes in `endstation_builder.py` and in the milan_dp, gptp_shadow and gptp_plane Makefiles, and are caught by gates 1b/26b/26c and those three suites. All of these are unchanged.
  - So the measurements are valid at this head under AGENTS.md section 7: they come from an ancestor whose in-scope artifacts nothing has touched since. Only the stated provenance is imprecise.
- Impact: a cold reader believes the route and the mutants ran at `1105f545`. Re-running them at `1105f545` would give the same result.
- Exact fix:
  - Rename the table column "this head" to "this head (routed at `8210abaa`; nothing routed changed after it)".
  - Change "At this head the slow corners" to "At `8210abaa`, whose routed inputs equal this head's, the slow corners".
  - Change line 23 to "Eight planted mutants, each caught by name (at `8210abaa`; no mutated file or catching check changed after it)".
  - Optionally change "(at the parent of this head; ...)" on line 22 to "(at the parent `4c4c5982`; ...)".
- Verification: `gh pr view 846 --json body` shows `8210abaa` beside the route column and the mutant count.

### W2 - RESIDUE - Docs - PR #846 body, "Linked Issue / roles" (lines 33-34) - reviewers still "to be named"

- Evidence:
  - The PR's public review-start comments name the internal reviewer R781 (2026-11-06T08:41:19Z and 09:15:19Z) and the external reviewer R782 (08:41:48Z).
  - AGENTS.md section 3: every active Issue must publicly identify an independent reviewer.
- Impact: none on any figure or verdict. The roles are already public in the thread, and the body is stale wording.
- Exact fix: "Internal cleared-context reviewer: `[R781]`" and "External reviewer: `[R782]`".
- Verification: body text.

### S1 - SUGGESTION - Robustness - `sw/builder/endstation_builder.py:3725` - retained from R781-1 unchanged (see that round for evidence and the optional change).

### Not findings

- The body names the executor `[A737]`. PR text may name lanes, and the comment rule covers source comments. The tree delta is empty, so no new source-comment residue exists.
- Shard 2's `complete.json` records `exit_code: 1`, while the body says "exited 92". 92 is the suite runner's own exit (`shard-2/results.json`), and 1 is the wrapper's verdict over it. The body's figure is the runner's and is correct.
- DoD "Self-test evidence is posted in a PR comment" is unchecked: the evidence comment is on issue #843. That is an honest status box, not a misstatement.

## Lens results

```text
[R781] PASS Conformance - receipts/issue843_body.md acceptance bullets and PR #846 body Description/Known limitations (lines 38-52, 115-118) against the unchanged tree; R781-1's builder consume/refuse, five configs, sim_gptp [CA], gates 26b/26c evidence stands at this head (no tree delta) - the edited body still states item 4 as not met and "Relates to #843", consistent with the issue
[R781] PASS RTL - route-head/bank.out (8210abaa, gitlinks equal to git ls-files -s at 1105f545), route-1x1-check-shipping.log and timing-summary.txt for head and dev; git diff --stat 8210abaa..1105f545 (no RTL, builder, config or gitlink change) - the body's route figures match the receipts and still hold at this head
[R781] PASS Robustness - no tree delta (same SHA, clean status); R781-1's _gptp_clock_accuracy_key / gate 26c refusal evidence stands; only S1 (suggestion) retained
[R781] PASS Tests - sweep-1105f545 shard complete/results/01.log (65 suites, shard-2 timeout then rerun 17/17), final-gates-1105f545 rc files, mutants-8210abaa/mutants.json (8 mutants, 10 runs, all caught; mutated files and catching checks unchanged since 8210abaa), physical-gptp-4c4c5982 log (only oracle.json differs, not read by milan_dp_gptp) - every test figure in the body matches a receipt
[R781] PASS Docs - receipts/pr846_body.md against receipts/body_binding.txt: F1 resolved (Status and checkout name 1105f545; no 4c4c5982 full SHA remains); W1 and W2 RESIDUE only; tree docs unchanged since R781-1 and keep that round's check
```

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #843 acceptance; PR body Description and limitations; R781-1 tree evidence (no tree delta) | R781-2 (tree: R781-1) | `1105f54546b2f19d9577b7fad902c908e34f88ee` |
| RTL | CLEAN | route-head and route-dev receipts; `git diff 8210abaa..1105f545`; gitlinks | R781-2 (tree: R781-1) | `1105f54546b2f19d9577b7fad902c908e34f88ee` |
| Robustness | CLEAN (S1 suggestion only) | unchanged builder key path; R781-1 probe | R781-1, carried | `1105f54546b2f19d9577b7fad902c908e34f88ee` |
| Tests | CLEAN | sweep-1105f545, final-gates-1105f545, mutants-8210abaa, physical-gptp-4c4c5982 | R781-2 (tree: R781-1) | `1105f54546b2f19d9577b7fad902c908e34f88ee` |
| Docs | CLEAN (W1, W2 RESIDUE) | PR #846 body at 2026-11-06T09:15:20Z; tree docs per R781-1 | R781-2 | `1105f54546b2f19d9577b7fad902c908e34f88ee` |

## Real limits

- No suite, build or route was run in this round. The tree is identical to R781-1's head, where R781-1 ran the gptp legs, harnesses, builder subset and fw_service_budget. This round's evidence is the published author receipts and `git diff`.
- The shard-0 milan_dp.log and other large logs are published by hash with tails only. The 212/212 leg figures at this head rest on the author's full log (by hash) and on R781-1's own runs at this head.
- The route ran at `8210abaa` on one directive only. #818 judges WNS on the best of three, and the other two were not routed. Area and timing are an open owner decision.
- Hosted checks at this head (`receipts/pr846_checks.txt`): 35 pass, 21 pending, 1 skipping. That is not hosted acceptance, which the manager owns.
- No manager source bank exists at this head. The current-dev merge candidate is not yet built.
- Physical calibration was NOT RUN. Field skips are not hardware proof, and nothing here measures the AX7101 oscillator (0x22 is the maintainer's decision).

## Pending manager duties

- Carry W1 and W2 to the residue checklist.
- Owner decisions:
  - Area and timing: LUT/DSP/WNS-floor refusals on the shipping route.
  - Issue item 4: depends on #842 landing order.
- Build and validate the current-dev merge candidate (builder and native banks) and link its receipts.
- Accept hosted and act contexts at the exact head.
- Obtain the external review (R782) verdict. Merge needs explicit maintainer authorization.

R781-2 FINISHED
