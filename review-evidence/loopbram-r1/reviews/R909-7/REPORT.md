[R909] POSITIVE - exact head 09201d35d7ea720b3ba205da185ba35c159ec24a

# R909-7: internal independent narrow re-review of PR #987 (issue #979)

- **Head.** `09201d35d7ea720b3ba205da185ba35c159ec24a`, tree `a3b3dca8a55b738e714ada4662a309a50118a481`. It is the PR's live head; the PR is open, not a draft, and mergeable.
- **Delta judged.** `1516b2ff..09201d35`: merge `7049c524` of dev-soft-core `5de21ff3` (PRs #1001, #1003, #995, #992), then `12382bc8`, `e9f95da4` and `09201d35`.
- **Same head as R909-6 and R910-4**, which were both NEGATIVE. No source byte has changed since. What is new is public evidence: the round-8 packet with routes at this head, a corrected attribution, and completed hosted runs. Both open findings asked for evidence or a text correction, so both can close without a commit.
- **Verdict reason.** No BLOCKER, MAJOR or MINOR is open under any lens. Four RESIDUE items (two new, two carried) and five SUGGESTIONs are listed below.
- **Order of reading.** The draft verdict and lens results were written before any prior report was opened (`receipts/draft-verdict-time.log`). The author's round-8 handoff, read earlier as evidence, names R910-4-F1, R910-4-F2 and R909-6-N1 in its headings, so I knew those IDs and titles before drafting. A path filter also copied a few prior reviewers' receipts into scratch; they were not opened.

## The four items

### 1. `e9f95da4`: firmware builder registration - verified

| Check | Result | Receipt |
|---|---|---|
| Category | `run.py:52-62` compiles five AECP sources with `cc` into the library its model links, and no other builder runs it. It is a `BUILDERS` entry, not `OUTSIDE`, `PART_OF` or `SUITES` | `ctrl_configs.py:140-143` |
| Argv | `--shape 1` and `--shape 8`, each `--work {work}/input-loopback-S --build-only`. Both commands ran under the gate's own recorder here: rc 0 in 12 s and 15 s, 59 invocations, 57 naming the AECP sources | `receipts/cap-*.rc`, `receipts/registry-probe.log` |
| Simulator selection | The entry takes it from `VERILATOR` (`run.py:72`), which `ctrl_runs.py:178` sets. The differential builder already does the same | source |
| Entry present, `--without verilator` scope | 0 reasons name the harness | `receipts/registry-probe.log` |
| **Planted removal** | exactly 1 reason: the hosted refusal text for `tb/verilator/input_loopback_dp/run.py` | same |
| **Its own capture missing**, `--only verilator` scope | refused, naming the harness | same |
| The leaf suite needs no entry | Of the seven loopback candidates, only `input_loopback_dp/run.py` is found by text | same |
| The legs | The harness is in neither leg of `ctrl_runs.LEGS` | same |
| **Hosted, both capture legs and the judge** | legs 0/2 and 1/2 succeeded (1888 and 1716 invocations). `firmware-boundary` judged both: `ctrl_boundary: PASS`, 308 ok lines, 0 escapes, harness named as left out | `receipts/hosted-excerpts.log` |
| **Hosted `firmware-verilator`** | `ctrl_boundary: PASS`, 202 ok lines, 0 escapes; the harness was held, and its two builds took 16 s and 18 s | same |

The removal and missing-capture probes call the gate's own `held()` on a real capture of the two registered commands. They are not a full judge run. The author's published judge runs and the hosted judge cover that.

### 2. `12382bc8`: 27 workers - verified

- My recomputation with the planner's own `balance()`: at 26 workers, four regular workers are over 1276 s (10, 20, 21 and 24 at 1304, 1278, 1290 and 1306). At 27, the largest is 1275 and none is over. The exception worker is 1530, alone. `input_loopback_dp` is on worker 14 and `input_loopback` on 15. All 27 rows of the `CI_WORKFLOWS.md` table match (`receipts/planner-projection.log`).
- A structural diff of `rtl.yml` against dev has six changed values: the two job-name lists, the shard list, the total, the exception's index, and `--expect 27`. No permission, trigger, token, fail-fast or context line changed. `verilator-suites` and `yosys-portability` keep their names.
- Generator checks, planner self-test and pieces self-test (67 parents, 96 units) pass. The fail-fast self-test passes, including its fork zero-write control (`receipts/failfast-selftest.log`).
- Hosted: all 27 shards, the eight unions and `verilator-suites` succeeded.

### 3. `09201d35`: leaf harness verdicts - verified

- **Protocol.** The depacketizer takes an enqueue pulse for the frame past its eighth beat, then a done pulse with the accepting mask (`KL_aaf_rx_depacketizer.sv:104-113`). The wrapper drives both from `|accept_w`, with `accept_w` as the mask. The monitors have distinct stream IDs, so the mask is one-hot. Entry allocation and done in one cycle are safe: retirement also waits for the frame's fate (`retire_w`). It is dev's own flat-monitor usage, at N inputs.
- **Results.** 79587 and 76017 checks, 468 and 447 packets, equal to the earlier rounds (`receipts/suite-leaf.log`).
- **My seven plants on the new wiring**, control clean: no enqueue, no done, zero mask, stream 0 only, all streams, top stream dropped, mask reversed. All seven fail the unchanged scoreboard with 1664 to 5589 sample failures (`receipts/verdict-plants.log`). The wiring is graded per stream.
- **Campaigns.** Leaf: control and 7 plants. Bounds: pass. Parent: 2 controls and 15 plants. Parent suite: 16173 and 122549 checks.

### 4. Merge, identity, egress - verified

- **Merge.** There was no textual conflict. `git merge-tree` of the two parents gives the merge commit's own tree, so it holds no hand edit. 38 of the PR's 46 files carry the same net lane lines before and after, including all three HDL sources. The other eight are the files this round's commits edit (`receipts/lane-patch.log`).
- **Generated files.** Both workflow generators report fresh. The hosted docs, elaboration and fast gates are green.
- **Identity, rebuilt here from three trees** (`receipts/identity.log`): 11 builder files per shape. Head equals dev at both shapes. Head against `1516b2ff` differs only in `gptp_ucode.hex`, which is dev's pin move. The published comparison adds the descriptor image, the twelve firmware images and the generated headers; I verified it by hash and did not rebuild it.
- **Egress ledger.** `--selftest` passes with 18 mutants caught. `tb/verilator/ctrl_service_budget`, `third_party` and `syn` have no difference from dev. The published 8x8/1if harness build equals dev's in every compared item. `--point 8x8-1if` was not run by anyone at this head (see limits).

## Enabled routes (prior findings R910-4-F1 and R909-6-N1)

`tools/route_check.py` over the published round-8 receipts gives (`receipts/route-check.log`):

- Source binding equals git at this head, start and end: head, tree, seven subtrees (`hdl` = `244c59e0`), all gitlinks, nothing dirty.
- All 138 tracked input files per shape hash equal to this clone's bytes.
- Every corner of all six routes, read from the full timing reports, and every routing status.

| Shape, selected | Setup / hold, worst corner | Failing endpoints (setup, hold, pulse width) | Routable = routed, errors | LUT / FF / BRAM / slices / DSP |
|---|---|---|---|---|
| 1x1 AltSpreadLogic_high | +0.147 / +0.036 ns | 0, 0, 0 | 73564, 0 | 32669 / 42821 / 82.5 / 14225 / 13 |
| 8x8 AltSpreadLogic_high | +0.309 / +0.036 ns | 0, 0, 0 | 97416, 0 | 48485 / 54965 / 110.5 / 15792 / 13 |

Both meet #818's floor. The three 8x8 route scripts equal round 5's apart from paths, and the routed 8x8 configuration is the shipped one plus the option. The worst selected path at each shape is in the mailbox. One 1x1 directive (+0.020) misses the floor; best-of-three is the prescribed rule. The ordinary 8x8 refusal (70.5 against 56) is retained as S14 debt.

## Findings

### R909-7-R1 - RESIDUE - Docs - `docs/testing/CI_WORKFLOWS.md:127-132`; comment at `.github/ci-templates/rtl-fast.yml:667-669`

- **Text.** Both list `firmware-verilator`'s builders as the mailbox bench, the MAAP differential and the AECP wire comparison. There are now four. The firmware README and the `BUILDERS` comment were updated; these two were not.
- **Wording only.** Both name `ctrl_configs.BUILDERS` as the authority. No check, figure or verdict reads either list. I edited the template comment in a scratch copy, and both generator checks stayed fresh (`receipts/template-comment.log`).
- **Exact fix.** Page: after "the AECP wire comparison at each processor reference it pins (... submodule's own objects)", add ", and the enabled parent loopback harness's build at both shapes (`--build-only`, #979)". Template: "the AECP wire comparison at each reference it pins and the enabled parent loopback harness at both shapes (#979), each run by its own".
- **Verification.** Read both; the generator checks and docs gates stay green.

### R909-7-R2 - RESIDUE - Docs - PR body

- **Text.** "Their hosted windows replace both figures after the first hosted run that completes them; none has yet." and the closing "Not run at this head ... Hosted acceptance at this head is required."
- **Problem.** Hosted runs at this head have since completed both suites and the other hosted items in that list.
- **Exact fix.** "The first hosted run that completed them, 45657606190 at this head, measured 11 s and 54 s; the figures are replaced in a later change." In the closing paragraph, say that hosted runs 45657606171, 45657606201, 45657606423 and 45657606190 covered the capture legs and judge, docs, elaboration, fast jobs, shards and portability, and keep only the egress ledger point as not run.
- **Verification.** Read the body against the check runs.

### Carried RESIDUE, both still unapplied

- **R909-6-R1** - Docs - `docs/testing/TESTING.md:478`, "as its N1 decision provides". Fix: "as the selector's new-suite steps provide when a provisional figure leaves a worker over its budget."
- **R909-5-R1** - Docs - `docs/testing/CI_WORKFLOWS.md:681-682`. Fix: "The measured hosted worst case plus a stated margin sets each named entry, except a provisional one, which keeps its own arm until its hosted window is measured:"

### Suggestions

- **R909-7-S1** - SUGGESTION - Tests, Docs - `scripts/suite_shards.py:113-114,152`, `TESTING.md:474-479`. The hosted windows exist: `input_loopback` about 10.3 s, `input_loopback_dp` about 53.4 s, from consecutive PASS lines of shards 15 and 14. At 11 and 54 s, 26 workers fit with a largest regular worker of 1275 s (`receipts/hosted-window-replan.log`). Replacing them in a later change drops the 27th worker and dates the "neither window exists yet" sentence. The figures cannot be replaced at the head that measures them.
- **R909-7-S2** - SUGGESTION - Docs, Tests - `docs/testing/TESTING.md:172`. "Every mutation driver therefore stages through `mutant_stage.py`" does not describe the two loopback drivers. `input_loopback/mutants.py` is the only tracked driver matched here by name that uses `tempfile` without the helper. Both are explicit campaigns outside the sweep and CI, so the cost is only compiler-cache misses. Several dev drivers also stage in-tree, so the sentence was already looser than the tree. Adopt the helper, or limit the sentence to sweep-run drivers.
- **R909-6-S1** (`suite_shards.py:150-151`, unnumbered steps) and **R909-6-S2** (a parent case that binds one stream to two inputs) are carried, optional.
- **R909-7-S3** - SUGGESTION - Docs - `CI_WORKFLOWS.md:3437-3463`. In the hosted run, shards 1, 2, 8 and 9 took 1702, 1501, 1461 and 1430 s of job time against projections of 1249, 1267, 1176 and 1176. All are inside 1800 s (at most 1.36 times the projection, against the stated 1.41). None owns a loopback suite. Worth recording when #998's figures are next refreshed.

**Comment-rule scan.** Lines added by this round's own commits hold no bench lane label, lane name, round, reviewer ID or comment ID. The N1 label is prose, carried as R909-6-R1.

## Prior public findings at this head

| Finding | Status | Evidence |
|---|---|---|
| R910-4-F1 MAJOR, R909-6-N1 MINOR (enabled routes) | **RESOLVED** (in my view; the external reviewer clears their own) | Routes section; required outcome met item by item |
| R910-4-F2 MINOR (verdict attribution) | **RESOLVED** | The PR body and round-8 handoff now give R909-5 at `1516b2ff` and R910-3 at `9acb9b82`, matching both public verdict lines |
| R909-6-R1, R909-5-R1 RESIDUE | **Retained** | Above |
| R909-2-N1, R909-3-N1, R909-4-N1 (planner, provisional, budget table) | Resolution holds | Item 2 |
| R909-1-F2 (disabled netlist identity) | Resolution retained by construction, not re-measured | The three HDL sources' lane lines are unchanged; builder identity |
| R910-2-F2, R909-2-N2 (8x8 route) | Closed again at this head's sources | Routes section |
| R909-1-F1, F3 to F7; R909-2-N3; R910-1-F1; R910-2-F1; earlier RESIDUE | Resolutions retained | Their artifacts are untouched except the leaf wrapper, re-verified; both campaigns pass |
| Earlier optional suggestions | Optional, unchanged | Untouched artifacts |

## Lens results

```text
[R909] PASS Conformance - receipts/route-check.log (hdl 244c59e0, both shapes, all corners), receipts/identity.log, receipts/suite-parent.log - #979 routing, area, end-to-end and disabled-identity criteria against this head
[R909] PASS RTL - tb/verilator/input_loopback/loopback_wrap.sv:64-69 vs KL_aaf_rx_depacketizer.sv:104-113 and its verdict queue; receipts/lane-patch.log - verdict protocol, and no shipped RTL byte of the PR altered by the merge
[R909] PASS Robustness - receipts/verdict-plants.log (7/7), receipts/parent-mutants.log, receipts/bounds.log, receipts/registry-probe.log, receipts/failfast-selftest.log - missing verdicts, wrong masks, missing capture, removal and fork zero-write
[R909] PASS Tests - receipts/suite-leaf.log, suite-parent.log, leaf-mutants.log, planner-projection.log, hosted-jobs-exact-head.tsv - unchanged counts, every plant caught, and hosted execution of both suites
[R909] PASS Docs - docs/testing/{CI_WORKFLOWS,RUNNING_TESTS,TESTING}.md and sw/firmware/ctrl/README.md:158-160 against the planner and the registry - figures and counts match; wording RESIDUE only
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #979 acceptance; option-B ruling; round-8 routes; identity rebuild; both suites; PR body | R909-7 | `09201d35d7ea720b3ba205da185ba35c159ec24a` |
| RTL | CLEAN | `loopback_wrap.sv`; depacketizer verdict queue; merge tree; lane patch comparison | R909-7 | `09201d35d7ea720b3ba205da185ba35c159ec24a` |
| Robustness | CLEAN | seven verdict plants; both campaigns; bounds; registry probes; fork control | R909-7 | `09201d35d7ea720b3ba205da185ba35c159ec24a` |
| Tests | CLEAN | both suites; campaigns; planner and pieces self-tests; hosted shards 14 and 15 | R909-7 | `09201d35d7ea720b3ba205da185ba35c159ec24a` |
| Docs | CLEAN (four RESIDUE) | three testing pages; firmware README; template comment; PR body | R909-7 | `09201d35d7ea720b3ba205da185ba35c159ec24a` |

Code the delta does not touch keeps its earlier lens verdict; the covering round above judged the delta and what it depends on.

## Hosted evidence at this head (read, not inferred)

Runs 45657606171 (docs), 45657606201 (elaboration), 45657606423 (fast) and 45657606190 (full) all concluded success, attempt 1. Of 85 check runs, 84 succeeded and one was skipped: Physical gPTP, nightly and manual. Job list for the fast and full runs: `receipts/hosted-jobs-exact-head.tsv`. Hosted and local-replica acceptance stays with the manager.

## Real limits

- No full parent, processor, portability or builder bank ran here, and no route or synthesis: route figures are the published reports, read and bound by hash. I did not read the round-8 synthesis logs or the disabled netlists.
- **Not run by anyone at this head:** `egress_ledger.py --point 8x8-1if`. The case for it is identity: the harness build equals dev's. The disabled release-top netlist comparison was not repeated.
- Not rebuilt here: firmware images and the CPU budget harness. I verified them by hash against the packet.
- Packet integrity: 114 of 114 round-7 files and 371 of 371 round-8 files match `MANIFEST.json`. The evidence commit itself is **unsigned**, so integrity rests on content hashes.
- The first registry-probe run stopped on an error in my own script after its main results; I fixed it and reran it clean. Compiler lines are filtered from the published suite and capture logs, and paths in the receipts are normalised.
- No manager source bank exists at this head and none is claimed. Physical calibration NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Hosted and local-replica acceptance, and the external reviewer's own clearance of R910-4-F1 and R910-4-F2.
- The merge-turn candidate with builder and native banks. dev-soft-core was still `5de21ff3` when read; if it moves, the PR body's own rule re-routes both shapes.
- Confirm the 27th worker, and schedule the figure replacement (R909-7-S1).
- Residue checklist: R909-7-R1, R909-7-R2, R909-6-R1, R909-5-R1.

**Restore.** All probes ran in copies under the packet's scratch. The clone's HEAD, index tree, every tracked blob and mode, and the five checked-out gitlinks equal the exact head; `external` is uninitialised, as provided.

R909-7 FINISHED
