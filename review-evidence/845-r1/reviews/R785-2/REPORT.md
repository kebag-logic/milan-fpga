[R785] POSITIVE - exact head 853ca25ae00fe26b09e019fbfe70893666617fc1

Round R785-2, internal cleared-context review of issue #845 / PR #847. Tree `bf3105f580d47a197a1e0d0af49ff343d78a6b1b`, source base and live dev `87e9d03aa2a4797957ac0124d0c7851a2eec234c`. This round covers rounds 2 and 3, the delta from `b16f0175` to this head, against the rulings on #845 and the maintainer decision issuecomment-6689114981.

## Verdict

POSITIVE. All five lenses are clean at this head. No BLOCKER, MAJOR or MINOR is open.

- R785-1 F1 to F4 and R786-1 F1 to F4 are resolved at their cause.
- The thirteenth record agrees with the published Vivado reports in every figure and every sub-block count I could read.
- The decision, the figures, the three directives and the 15 free slices are stated truthfully on all three named pages.
- Three wording RESIDUE items and one new SUGGESTION are recorded below.

One limit applies to the gate result. I did not run `check` on the measurement directories: they are not published and no Vivado run was allowed here. "`check` exits 0" rests on the author's receipts plus my replay of the gate's `judge()` from the published reports. See [Real limits](#real-limits).

This verdict is one of two required. It is not merge authority.

## Focus items

| # | Item | Result | Evidence |
|---|---|---|---|
| 1 | Thirteenth record written through `pp_resource_gate.py`, not by hand | Holds, as far as bytes and reports can show | See [The record's provenance](#the-records-provenance) |
| 2 | `check` exits 0 on all three endpoints | Holds on receipts and replay | Author: `after-route-1x1.rc`, `after-ooc-1x1.rc`, `after-ooc-8x8.rc` all 0. My replay of `judge()` from the reports: exit 0 on all three against the thirteenth record, exit 1 on all three against the twelfth, refusing exactly the same LUT and FF rows as the author's `before-*.log` (`receipts/gate-replay.txt`) |
| 3 | `check-baseline` exits 0 | Holds, run here at head | `receipts/check-baseline.log`: "baseline PASS: 3 endpoints". Four planted edits to policy or the record each exit 2 (`receipts/gate-replay.txt`) |
| 4 | Decision, figures, three directives and 15 slices truthful on the three pages | Holds | `docs/design/AREA_BUDGET.md:162-187`, `docs/reference/SUBMODULES.md:587-633`, `CHANGELOG.md:92-97`, each compared with the decision text and the receipts. One wording residue, R785-2-R1 |
| 5 | No synthesis input changed since `b16f0175` and `bf6c5a67` | Holds | See [Synthesis inputs](#synthesis-inputs) |
| 6 | Definition of Done box honest about `519d9c2b` | Holds | See [The Definition of Done box](#the-definition-of-done-box) |

### The record's provenance

- `syn/ooc/pp_resource_baseline.json` equals `json.dumps(load, indent=1) + "\n"` byte for byte, which is the gate's writer at `syn/ooc/pp_resource_gate.py:969`, and it is pure ASCII.
- Between the twelfth and thirteenth records only `record` and the `measured` note change on each endpoint. Every tolerance, floor, ceiling, the schema and the description are unchanged (`receipts/json-diff-twelfth-to-thirteenth.txt`).
- The only identity change is `place_design -directive ExtraPostPlacementOpt` to `ExtraTimingOpt` on `route-1x1`. `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` says a route-set record does exactly this.
- The record's keys follow the gate's `RECORD` order. Its scopes follow hierarchy-report row order, 51, 52 and 52 of them, and its figure types match (`receipts/gate-replay.txt`).
- Every utilization figure, the tool, device, design and state fields, and every scope's LUT, FF, RAMB36, RAMB18 and DSP, recomputed from the published reports with the gate's own parsers, equal the record. `RESULT EQUAL` (`receipts/recompute-from-reports.txt`).
- CARRY4 (3,675, 1,636 and 2,317) equals each utilization report's primitive row. WNS and WHS equal the published timing tables.
- The author's `record.rc` reads rc 0 for all three. The hand-edited `measured` notes are permitted by `NOTES` in the gate and the PR says they were edited.

### Synthesis inputs

- `git diff --name-status b16f0175 HEAD` lists ten paths: nine documentation or record files plus `tb/verilator/pp_shadow/sim_main.cpp`, one comment. `bf6c5a67..HEAD` lists eight, none a synthesis input (`receipts/synthesis-input-paths.txt`).
- All six gitlinks are identical at `b16f0175`, `bf6c5a67` and the head.
- The builder's mentions of `docs/design/` are comments. It reads neither the CHANGELOG nor the baseline.
- The author's `digest-at-head.txt` supports this by re-export: 131 files against 131, generics and images equal, and only the generated top differs, inside its block comment. The non-reproducing `inputs_sha256` is not reported here, as instructed; it is open as #850.
- The recorded `ucode.hex` and `ltn_rom.hex` in all three image manifests equal the `92100657` rows of `syn/yosys/rom_digests.tsv`.
- `N_STREAM_IN_P` is 9 in the 8x8 parameters, which supports "nine Stream Inputs".

### The Definition of Done box

The box says the head carries the docs gates, `check` and `check-baseline`, and that the sweep, firmware self-test, builder and behave are at `519d9c2b`, pointing to Status. That is honest, for these reasons:

- Status says those four were not re-run at a later head.
- Known limitations adds the one point that matters: `b16f0175`'s dev merge changed the process owner the suites run under.
- `git diff --stat 519d9c2b b16f0175` confirms the six files the body lists.
- The `519d9c2b` receipts hold: all four shards' `complete.json` name `519d9c2b` with exit 0, the tallies sum to 65 suites and 2,192,435 checks with 0 failures, behave reports 14, 508 and 2,330, and the firmware, coverage and builder rc files are 0 (`receipts/sweep-receipt-spotcheck.txt`).

The box does not claim a full sweep at the head. No manager source bank is claimed or inferred.

## Prior findings

| Finding | State at this head | At the cause |
|---|---|---|
| R785-1 F1 and R786-F1, MAJOR: growth with no gate verdict, decision or record | **Resolved** | The decision is on #845 (issuecomment-6689114981). The gate ran in its own form on all three endpoints and exited 1 against the twelfth record. All three are re-recorded, policy untouched. `AREA_BUDGET.md`, the pin page and the CHANGELOG state this, and `AREA_BUDGET.md` no longer ends at `a9e84b66`. The growth itself is accepted and is not reported here |
| R785-1 F2 and R786-F2, MINOR: link-change text | **Resolved** | `SUBMODULES.md:542-543`, `CHANGELOG.md:75-84` and `INTEGRATION_GUIDE.md:78-86` now state leaving settled, the three flags clearing, active or passive by discovery, and probing and settling again, with a held value applying at that settle. This agrees with the processor's table, `EVT_TK_UNREGISTERED` through A8 then A12 or A17 (`05_acmp_engine.md:280`, `:298`, `:303`), and with R786-1's published probe table. Milan 5.5.3.5.48 is the clause `10_srp_engine.md:666` cites for that re-probe. The 0 to 1 s delay was read only against that probe's observed +400 to +930 ms |
| R785-1 F3 and R786-F3, MINOR: `sim_main.cpp` comment | **Resolved** | `tb/verilator/pp_shadow/sim_main.cpp:3738-3745` states what row U states, in the same words. `grep "ignores every attribute"` over `tb`, `docs` and the CHANGELOG finds nothing. `make -C tb/verilator/pp_shadow run` passes at this head with pinned Verilator 5.050: 719, 719, 759 and 317 checks, 0 failures |
| R785-1 F4 and R786-F4, MINOR: results at the wrong head | **Resolved** | Status and Description name a measured head for each result, and each named head has a receipt. A wording residue in that body is R785-2-R2 |
| R786-R1, RESIDUE: "Recipe" wording | Carried | The round 3 ruling sends it to #495, which is open |
| R785-1 S1, R786-S2: parent harness arm | Retained as SUGGESTION | The PR states the limitation |
| R785-1 S2: `tb/verilator/milan_dp/README.md` dated row | Retained as SUGGESTION | Unchanged |
| R786-S1: name `eff_link_w` once | Retained as SUGGESTION | Unchanged |

## Findings

No BLOCKER, MAJOR or MINOR.

### R785-2-R1 RESIDUE - Docs

**Artifact:** `docs/reference/SUBMODULES.md:615`.

**Evidence:** "Against that record, `check` exits 0 on every endpoint." directly follows a table whose column is "Exit, twelfth record" and reads 1 on every row. The nearest antecedent is therefore the twelfth record, while the sentence means the thirteenth, named above that table.

**Why RESIDUE, not MINOR:** the intended claim is true, and the fix moves no figure, verdict or test. A disposable copy with the fix still passes `docs_inventory.py --check`, so no generated artifact moves.

**Impact:** a reader meets an apparent contradiction with the table above and must resolve it from context.

**Exact fix:** "Against the thirteenth record, `check` exits 0 on every endpoint."

**Verification:** read the line; `docs_inventory.py --check`.

### R785-2-R2 RESIDUE - Docs

**Artifact:** PR #847 body, Round 2 table, row F1.

**Evidence:** the row has two cells where the table has three, and a sentence breaks off: "The gate ran in its own form Answered in [Round 3](#round-3): ...".

**Impact:** the row renders with its State cell empty, and the Change text ends mid-sentence.

**Exact fix:** end the Change cell with "The gate ran in its own form, and its exit is recorded below." and start a new cell with "Answered in [Round 3](#round-3): the maintainer decision accepts the growth, and the record is re-baselined".

**Verification:** read the rendered table.

### R785-2-R3 RESIDUE - Docs

**Artifact:** PR #847 body, Known limitations, the `inputs_sha256` item.

**Evidence:** it says "the fix belongs in a new Issue". That Issue exists and is open as #850.

**Exact fix:** "the fix is tracked by #850".

**Verification:** read the line.

### R785-2-S1 SUGGESTION - Docs, Tests

**Artifact:** `docs/findings/234_PP_SHADOW_AREA_BASELINE.md`, the thirteenth record, and the published route receipts.

**Evidence:** four statements have no published source: the worst setup path (15 levels, 9.170 ns, 3.100 ns plus 6.070 ns), the worst hold path, the 8,827 MB memory peak, and the `Synth 8-4445` and `Synth 8-6901` statements. The evidence holds only the timing tables and each log's tail, size and hash. The arithmetic is consistent, and the listed log sizes and hashes match `large.sha256`, but a cold reviewer cannot open these claims.

**Impact:** none on any gated figure.

**Suggested outcome:** publish each route's worst-path report section and a grep of those diagnostics with the next measurement.

## Lens results

```text
[R785] PASS Conformance - issue #845 acceptance and items 1 to 4, issuecomment-6689114981, the [A10] round 3 ruling, docs/design/AREA_BUDGET.md:162-187, docs/reference/SUBMODULES.md:587-633, CHANGELOG.md:92-97 - each ruling item done as written; decision scope, quote and citation match its text; link-change statements checked against processor 05_acmp_engine.md:280 and 10_srp_engine.md:666
[R785] PASS RTL - protocol-processor gitlink 92100657 at b16f0175, bf6c5a67 and head; route-selected/route-1x1-ETO-baseline_hierarchy.rpt; receipts/processor-history.txt - no RTL input moved in the delta; the resource effect is now judged by the gate; the listener is untouched between f65c8ff7 and a9e84b66, so its movement is #212's as the page states; wrapper 24,895, milan_datapath 43,906 and KL_maap 473 equal the report
[R785] PASS Robustness - receipts/gate-replay.txt, receipts/gate-mutants.log, syn/ooc/pp_resource_gate.py:495-499 - the ExtraTimingOpt record stays comparable with a route at another recipe directive (exit 0), a directive outside the recipe is refused (exit 2), four tampered baselines are refused (exit 2); the prior link-change and pre-settle probes keep their verdict, since the delta changes no RTL or harness behaviour
[R785] PASS Tests - receipts/pp_shadow-run.summary.txt, receipts/gate-selftest.log, receipts/gate-mutants.log - pp_shadow 719, 719, 759 and 317 checks, 0 failures at head after the comment change; gate self-test rc 0; 236 of 236 mutants fail and the control passes; check_cpp_idiom.py rc 0; no suite reads the record's figures
[R785] PASS Docs - docs/design/AREA_BUDGET.md, docs/reference/SUBMODULES.md, CHANGELOG.md, docs/findings/234_PP_SHADOW_AREA_BASELINE.md, docs/findings/README.md, docs/design/MARK_II_AREA_PLAN.md, docs/integration/INTEGRATION_GUIDE.md, PR #847 body - every figure, percentage, delta and sub-block row checked against the JSON and receipts; no stale current-record figure remains; docs_inventory.py --check, check_submodule_docs.py and git diff --check rc 0; author docs.yml receipts 72 steps rc 0 at this head; comment rule: the delta's one source comment names only processor #212
```

Other checks behind those lines:

- The published evidence manifest verifies for `author-r3`: 445 files, 0 bad, 0 unlisted, 11 path-redacted (`receipts/evidence-manifest-verify.txt`). No signature was found: commit `a3149b01` is unsigned, so "verified" here means hashes only.
- All three directives' figures equal their reports. Each route status shows 0 routing errors and the IOB checks read PASS.
- The run table's seconds, log hashes and byte counts match the receipts for all six runs.
- The commits since base are one-line with no trailers. A search of the changed pages and the JSON for local paths finds none.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #845 body, rulings and decision; `AREA_BUDGET.md`; pin page; CHANGELOG; contract; processor `05_acmp_engine.md`, `10_srp_engine.md` | R785-2 | `853ca25ae00fe26b09e019fbfe70893666617fc1` |
| RTL | CLEAN | Gitlinks at three heads; route, `ooc-1x1` and `ooc-8x8` reports; hierarchy reports; processor `hdl` history | R785-2 | `853ca25ae00fe26b09e019fbfe70893666617fc1` |
| Robustness | CLEAN | `pp_resource_gate.py` comparison and refusal paths through `receipts/gate-replay.txt`; mutants; prior probes retained because nothing they depend on moved | R785-2 | `853ca25ae00fe26b09e019fbfe70893666617fc1` |
| Tests | CLEAN | `sim_main.cpp` comment and pp_shadow run; gate self-test and mutants; `check-baseline`; replay of `judge()`; `519d9c2b` receipts spot-checked | R785-2 | `853ca25ae00fe26b09e019fbfe70893666617fc1` |
| Docs | CLEAN, with R785-2-R1 to R3 as RESIDUE | The eight changed pages; the audit; PR body; published receipts; docs gates | R785-2 | `853ca25ae00fe26b09e019fbfe70893666617fc1` |

## Real limits

- **`check` not run here.** The measurement directories are not published and no Vivado run was allowed. My replay feeds report-derived figures to `judge()` with the record's identity, so it does not exercise `measure()`, `inputs()` or `routing()` on real directories.
- **"Not by hand" is strong evidence, not proof.** A hand-typed record could in principle reproduce the same bytes. The `inputs_sha256` values were not recomputed, since they need the exports.
- **Not verified:** the items in R785-2-S1, and "All 18 memory-image entries were rehashed" beyond the ledger spot-check of two images and the count of 18.
- **Not run here:** the full sweep, firmware, builder, behave, the whole of `docs.yml` and any route. Those results are the author's receipts. I spot-checked them; I did not repeat them.
- **The sweep predates dev's PR #834 merge.** No full sweep exists after `519d9c2b`, as assigned.
- **Standards not opened.** Milan and 802.1Q clauses were compared through the processor's documents only. Conformance of the SRP RTL itself belongs to the processor repository.
- **Prior behavioural probes were not repeated.** Their verdicts stand because nothing they depend on moved.
- **Hardware:** physical calibration NOT RUN. Field skips are not hardware proof, and no hardware was touched.
- **Hosted, read once, not acceptance evidence:** 3 success (`docs-check-no-git`, `full-ci-gate`, `bdd-conformance`), 1 skipped (`Physical gPTP`, nightly and manual, not executed), 8 in progress, 26 queued (`receipts/hosted-check-runs.txt`).

Run incidents, for the record:

- While looking for a local copy of the Milan text I ran a filesystem-wide `find` by file name. That went beyond the review's directories and walked areas this review was told not to read. It matched file names only, opened nothing and printed no match before I stopped it. Nothing from it is used here.
- The evidence checkout also holds `HANDOFF.md` files. I did not read them.
- `make run` left ignored build outputs in the clone. They were previewed and removed, and the clone was re-verified: HEAD, tree and index exact, 0 tracked differences, 0 ignored files, the five populated gitlinks at their pins and clean, `external` unpopulated as received (`receipts/clone-integrity.txt`).

## Pending manager duties

- The second independent positive review, and merge authorization.
- Current-dev merge candidate build and native banks, with receipts linked on the PR.
- Hosted and act acceptance at the final head; most contexts are still queued or in progress.
- Carry R785-2-R1 to R3 to the residue checklist #495, with R786-R1 and the processor `integrator.md` sentence, and confirm the last two are recorded there.
- Route the integrated image with every lab fix before the release build, as the decision requires; #846 re-baselines on top of this PR.
- The Definition of Done boxes still unticked are the manager's and reviewers' to settle.

R785-2 FINISHED
