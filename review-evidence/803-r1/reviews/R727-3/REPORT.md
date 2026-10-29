[R727] POSITIVE - exact head e06ade312a80eb578579365134ab797cda90622b

# R727-3: internal cleared-context delta review of PR #805 (issue #803, gPTP pin f97c1803), dev merge round

- Head `e06ade312a80eb578579365134ab797cda90622b`, tree `ecf83515ce35c5edfa4ed79239775aefa0ada4ec`. It is the merge `6fc0c214` (parents `2b1565fd`, `e78472ff`) plus `e06ade31`, which changes three documents.
- Scope: the delta over `2b1565fd`, where R727-2 and R728-2 were POSITIVE, judged against the [A10] round 3 ruling (issue #803, issuecomment-6486755432) and the owner's slice acceptance (issuecomment-6488027886).
- Verdict POSITIVE. No BLOCKER, MAJOR or MINOR is open. One RESIDUE is in the PR body, plus one new SUGGESTION and five retained prior SUGGESTIONs. All five lenses are clean at this head.

## Reconstruction

- Read: AGENTS.md; the ruling and the owner decision on #803; the [A693c] TAKEN and REVIEW READY comments; the PR #805 body at this head; `git diff 5fcec84b..e06ade31` and its history.
- Author evidence: `review-evidence/803-r1/author-r3` at `5936d7d0`. All 222 files match the published hashes in the tree's `MANIFEST.json`. The 18 files that differ from `INDEX.md` are the manifest's path-redacted rows, and for each one INDEX holds the original hash (`receipts/evidence-manifest-verify.txt`).
- I read the prior public findings (R727-2, R728-2) only after my own pass.

## Ruling items, checked

1. **Conflicted records keep both adoptions' content.**
   - My own re-merge, `git merge-tree 2b1565fd e78472ff`, conflicts in exactly the eight paths the ruling names (`receipts/remerge-conflicts.txt`).
   - The committed merge differs from git's automatic result only in those eight paths (`receipts/remerge-vs-merge-stat.txt`). No auto-merged file was edited by hand.
   - Section-level multiset compare (`receipts/scope/section-compare.txt`):
     - The CHANGELOG #799 section and the SUBMODULES #799 section and shared tail are line-identical to dev.
     - The #803 sections differ from `2b1565fd` only in the intended figure lines and in "The processor stays at `f65c8ff7`".
     - Nothing is lost and nothing is duplicated. Both Contents rows are present, newest first (`CHANGELOG.md:11-12`).
   - `RUNNING_TESTS.md:88-89` keeps 6900 s and nineteen workers.
   - AREA_BUDGET.md keeps dev's table and dev's #632/#771/#708 history. The PR side's old "13 logic levels … 9.471 ns" lines were base text that the PR never edited and dev rewrote, so dev's version is the correct resolution.
2. **Generated files come from their generators.**
   - I re-ran `bash syn/yosys/ooc.sh --record-rom-digests` (sv2v v0.0.12) and `python3 docs/diagrams/submodule_boundaries.gen.py` in the clone.
   - `rom_digests.tsv`, the `.drawio`, `.svg` and `.png`, and `PNG_MANIFEST.json` are byte-identical to the head (`receipts/generators/regen-compare.log`, rc 0). `--check` and `--selftest` are OK.
   - The ledger's 71 rows are exactly the union of both parents' rows, under an identical header (`receipts/generators/ledger-union.txt`).
3. **Area on the combined tree.** Measured at `6fc0c214`; `e06ade31` changes no synthesis input. Receipts are in `author-r3/receipts/vivado`.
   - route-1x1 gate rc 0:
     - LUT 52,012 → 51,801 (−211, tolerance 500).
     - FF 53,707 → 53,760 (+53).
     - Slices 15,780 → 15,834 (+54, tolerance 80): 16 of 15,850 free, matching the place report (`Slice | 15834 | 15850`).
     - WNS +0.303 ns and WHS +0.028 ns, the four-corner minimum.
     - 102,413 of 102,413 nets routed, 0 errors. RAMB and DSP unchanged.
   - ooc-1x1 and ooc-8x8 gates rc 0, equal to the record.
   - `check-baseline` is rc 0 in my run. `pp_resource_baseline.json` at the head equals `e78472ff`.
   - The "record = dev's own route" claim holds: `8b76de69..e78472ff` differs outside docs and tests only in comment lines of `mailbox.yaml`, `gen_mailbox.py` and a mutant script. The author's `8b76de69` re-route matches the record in every figure.
   - `AREA_BUDGET.md:143` states 15,834 placed and 16 free, and `:144` keeps the owner-decision sentence verbatim. No STOP condition is met.
4. **Shard planner.**
   - `suite_shards.py --selftest` PASS in my run.
   - The ownership step body for all 19 workers (indices 0..18) passes at the head and at dev `e78472ff`: 81 lines, no duplicate owner, worker 1 owns `tsn_fuzz`, worker 3 owns `chmap_capture`. Both listings are byte-identical (`receipts/shards/compare.txt`).
   - `tb/verilator/milan_dp/Makefile` is identical to dev, and the author's six piece-suite inventories are identical, with milan_dp at 24 cases. No leg re-deals (#804).
5. **Physical leg.**
   - The head runs 899,637,137 cycles, which equals the README figure, so the projection stays 5,347 to 5,484 s: 77.5 to 79.5 % of 6,900 s.
   - The author's run took 5,450 s (79.0 %) with 205 checks and 0 failures.
   - The relative sim-rate receipt is 0.981× of `2b1565fd`.
6. **Gates.**
   - My own runs, all rc 0: `ci_gate_workflows.py --check`, `ci_events.py --check`, `check_submodule_docs`, `check_gptp_docs` (plain and `--with-submodule`), `check_doc_style`, `docs_check`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash --base e78472ff` (pinned renderer requirements, see limits), the timesync diagram `--check`, and `cd tests && behave` (14 features, 495 scenarios, 2,288 steps, matching the author).
   - Author receipts, all rc 0:
     - sweep: 4 units, 64 suites, 2,191,694 checks, 0 failures.
     - rtl-fast replica: 12/12 jobs, base `e78472ff`.
     - docs workflow: 44 steps, 0 failed, 2 skipped by rule.
     - static bank: lint 89 ≤ 89, fail-fast ratchet; the builder bank has 2 arms NOT RUN, the same two as in rounds 1 and 2.
     - Yosys: rc 0, TAP-PURITY PASS.
7. **Scope.**
   - Of every path changed on either side (`receipts/scope/classification.tsv`): 46 dev-only paths equal dev, 35 PR-only paths equal `2b1565fd`, and 15 paths changed on both sides. No stray dev revert.
   - The 15 both-changed paths are the eight conflicts plus seven clean auto-merges: svg, REGISTER_MAP, CI_WORKFLOWS, TESTING, rtl.yml, milan_datapath.sv and milan_dp/README.
   - In `milan_datapath.sv` the PR's hunks (the gPTP path head, about `:1627-1635` and `:2278-2310`) and dev's hunks (processor #202 stream-ID wiring, #206 comment) are disjoint. They share no signal.
   - The PR body is at this head, says "Relates to #803", and `closingIssuesReferences` is empty, so it does not close #803.

## Findings

### RES-1 - RESIDUE - Docs - PR #805 body: "Status" last line, "Known limitations" first bullet, "Definition of Done" first item

- **Evidence:** the body says "One owner decision is open, on slice headroom", lists "Slice headroom: an owner decision" as a limitation, and leaves "the owner's slice acceptance" as remaining. The owner accepted this adoption's slice growth on 2026-10-29 (issue #803, issuecomment-6488027886), before REVIEW READY.
  - The [A693c] REVIEW READY comment's open risk 1 has the same staleness.
- **Impact:** wording only. No figure, gate or verdict changes, and the repository record (`AREA_BUDGET.md:143-144`) is unaffected.
- **Exact fix:**
  - Replace the Status line with "The owner accepted this adoption's slice growth on 2026-10-29 (#803, issuecomment-6488027886); 16 of 15,850 slices are free."
  - Retitle the limitation "Slice headroom", and say that the next growth needs its own owner decision.
  - Drop "the owner's slice acceptance" from the first Definition of Done item.
- **Verification:** read the PR body.

### SUG-1 - SUGGESTION - Docs - `docs/design/AREA_BUDGET.md:143`, `CHANGELOG.md:82-85`, `docs/reference/SUBMODULES.md:371-381`

- The #799 records cite their owner decision. The #803 records do not cite the 2026-10-29 acceptance of this adoption's +54 slices.
- The ruling asked only that `:144` keep its sentence, and the route is within every tolerance, so this is optional.
- A link at `:143` would let a cold reader find the decision. Separately, `:146-147` now reads as the record's critical path, which is accurate; the combined route's path is not stated, as was also the case at `2b1565fd`.

### Prior findings at this head

| Prior finding | Lenses | Status at e06ade31 | Evidence |
|---|---|---|---|
| R727-2 S-1, SUGGESTION (s1b level and per-cycle `evq_rp_r`) | Tests, Robustness | RETAINED, optional | `sim_gptp.cpp` unchanged since `2b1565fd`; `:1689` |
| R727-2 S-2, SUGGESTION (entries 2..7 count-gated) | Tests | RETAINED, optional | unchanged |
| R727-2 S-3 / R728-2 N2, SUGGESTION ("count beat held" wording) | Tests | RETAINED, optional | `sim_gptp.cpp:1492` |
| R728-2 N1, SUGGESTION (past-tense 5400 s lines) | Docs | RETAINED, optional | now `milan_dp/README.md:424-425`, shifted by dev's added rows |
| R727-2 N-1, informational (control construction) | - | no action | unchanged |
| R727-1 R1, RESIDUE ("keeps" WNS) | Docs | still RESOLVED | `SUBMODULES.md:381` "meets timing at +0.303 ns WNS" |

No BLOCKER, MAJOR or MINOR was open at `2b1565fd`, and none is introduced by the delta.

Comment rule: the delta adds no source comment of this PR (`e06ade31` is documents only, and the merge resolution touched only the eight records), so there is no new residue.

## Lens results

```text
[R727] PASS Conformance - receipts/remerge-conflicts.txt; receipts/scope/{classification.tsv,section-compare.txt}; AREA_BUDGET.md:143-145; RUNNING_TESTS.md:88-89; author-r3/receipts/vivado/*check-against-twelfth-record.log - ruling items 1-7 each met at e06ade31: both adoptions kept, generators reproduce, combined route within tolerance with 16 of 15,850 free, :144 sentence kept, no STOP condition
[R727] PASS RTL - hdl/milan/milan_datapath.sv at e06ade31 (PR hunks ~:1627-1635, :2278-2310 vs dev hunks :1457-1548, :2492-2567, :6002-6190, :7501, :9650); author-r3/receipts/vivado/route-1x1-alinx_ax7101_{route_status,utilization_place}.rpt, route-1x1-signoff-corners.txt - disjoint auto-merge with no shared signal; combined route places and routes 102,413/102,413 nets at +0.303/+0.028 ns; e06ade31 changes no RTL; record commit 8b76de69 differs from e78472ff only in comments
[R727] PASS Robustness - author-r3/receipts/physical/{projection.txt,tally.out,milan_dp_gptp.log:779}; AREA_BUDGET.md:143-144 - physical leg 205/0 within 6,900 s (79.0 % measured, 79.5 % projected worst case), scenario cycles unchanged by the merge; slice margin 16 stated and owner-accepted; the next-growth guard sentence is kept
[R727] PASS Tests - receipts/gates/behave.log (495/495); receipts/gates/suite_shards_selftest.log; receipts/shards/{head,dev,compare.txt}; author-r3/receipts/sweep/{shard-summaries.txt,suite-tally-quiet.out} - planner and 19-worker ownership identical to dev, milan_dp Makefile unchanged so no re-deal, sweep 64/64 with 0 failures at the head, sim_gptp.cpp unchanged and no test file differs from either parent
[R727] PASS Docs - receipts/generators/{regen-compare.log,ledger-union.txt,boundaries_check_head.log}; receipts/gates/{check_doc_style,docs_check,gen_toc_check,gen_toc_anchors,check_em_dash,check_submodule_docs,check_gptp_docs,check_gptp_docs_sub}.log; CHANGELOG.md:11-12,49-87; SUBMODULES.md #799/#803 sections - generated files byte-identical through their generators, records hold both adoptions with correct combined figures; RES-1 is PR-body wording only
```

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ruling items 1-7; re-merge; section compare; area gate logs | R727-3 | e06ade312a80eb578579365134ab797cda90622b |
| RTL | CLEAN | `milan_datapath.sv` auto-merge; route and place reports; 8b76de69 vs e78472ff inputs | R727-3 | e06ade312a80eb578579365134ab797cda90622b |
| Robustness | CLEAN | physical leg receipts and projection; slice margin statement | R727-3 | e06ade312a80eb578579365134ab797cda90622b |
| Tests | CLEAN | own behave, planner selftest and 19-worker ownership (head and dev); author sweep | R727-3 | e06ade312a80eb578579365134ab797cda90622b |
| Docs | CLEAN (RES-1 residue) | generator regeneration; docs gates; CHANGELOG, SUBMODULES, AREA_BUDGET, RUNNING_TESTS | R727-3 | e06ade312a80eb578579365134ab797cda90622b |

## Real limits

- I ran no Vivado route, no full sweep and no physical leg. Those figures rest on the author's published receipts, which I verified by hash and read by section.
- I attempted one targeted Verilator probe of the `milan_dp` `gptp` and `sidmove` legs on the combined tree:
  - In a git-less archive copy it refused at `pp_srcs.py`, which needs git metadata.
  - Creating a local shared clone for it was not permitted in this session.
  - So no own simulation evidence exists for the auto-merged datapath. It rests on the author's sweep (64/64) and on the disjointness of the hunks.
- The Markdown gates ran under the pinned renderer requirements (`tools/markdown/requirements.txt`, html5lib 1.1) but on CPython 3.14.8, not the CI's 3.12.3.
- The PNG was reproduced with the local `rsvg-convert` 2.63.4, which produced identical bytes.
- Exact-head hosted checks were still running when I fetched them: 16 success, 1 skipped, 29 queued or in progress (`receipts/hosted-check-runs-e06ade31.tsv`). They are not evidence here.
- Physical calibration NOT RUN; nothing here is hardware proof. No standard text was opened; the delta changes no clause interpretation.
- After the probes, the clone is at exact head bytes: index tree = HEAD tree, no tracked change, no untracked file, all five initialised submodules at their gitlinks and clean (`receipts/clone-integrity-after.txt`).

## Pending manager duties

- Validate the current-dev merge candidate (builder and native banks) at the merge turn and link its receipts.
- Hosted and local-replica acceptance at the exact head, including verilator-suites and yosys-portability once complete.
- Carry RES-1 to the residue checklist.
- Pair this ledger with the external round on the same head.
- The merge needs explicit maintainer authorization. FPGA-gPTP 87-91 close only after the bench re-run.

R727-3 FINISHED
