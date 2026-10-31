[R732] POSITIVE - exact head cbc7c6043ebf84d5bcd74652dc0a7131b7d54271

# R732-4: external cleared-context delta review of PR #822 (#787)

Head `cbc7c6043ebf84d5bcd74652dc0a7131b7d54271`, tree `43d185333ff4048986a2080996ed5e482af3f3bc`. Delta from the reviewed head `f7d5fc3c`: `ddbf87e6` (CDC census regenerated), `6ffadb07` (merge of PR #820's head `81f78a81`), `cbc7c604` (route records).

## Verdict

POSITIVE. Both MINOR findings from round 3 are fixed at their cause, and so is every residue item:

- **R731-3 F1 = R732-3 F1 (census).** The tracked SVG and drawio are byte-identical to the generator's output at this head. The PNG is byte-identical to a fresh render made with the generator's own `rsvg-convert` line, and it shows `x3 call sites`.
- **R732-3 F2 (route record).** Both records now state the measured re-pin route: +0.365 ns, 52,021 LUTs, 63 slices left, and the #818 gate passes. Each figure matches the published receipt `head-set-check.log`, and that receipt matches its manifest hash. Nothing in the tree still says the route waits for #814, and no fall the #818 gate passes is refused in the present tense.
- **The #820 merge.** It is textually clean: a re-merge gives the recorded tree `755d7ec3`, and nothing is dropped from either side. Its gate bytes are the bytes the route was judged with.
- **Docs gates.** The docs gates covering the delta give rc 0.

Nothing open is MINOR or worse. Three RESIDUE items (pure wording) and three SUGGESTIONs are listed below for one pass.

## How the task was reconstructed

1. AGENTS.md (sections 3, 6, 7) and CONTRIBUTING.md (docs and merge rules).
2. Issue #787: body and frozen acceptance.
3. The manager's round-6 answer on PR #822.
4. `git log` and `git diff f7d5fc3c..cbc7c604`, read per commit.
5. The public evidence tree `a16caad4:review-evidence/787-r1/author-r5/receipts/route/`.
6. Probes of my own.

The round-3 findings (R731-3, R732-3) were read only after this pass was done.

## What was checked, with receipts

| Claim | Result | Receipt / script |
|---|---|---|
| The census equals its generator | `python3 -I docs/diagrams/cdc_census.gen.py <scratch>/cdc_census` gives 27 fabric crossings, 14 modules and 4 SoC rows. `cmp` shows the svg and drawio IDENTICAL to the tracked files (sha256 `393f45f8…`, `9f9c0981…`) | `receipts/census-regen.log` |
| The PNG is re-rendered and shows x3 | `rsvg-convert -w 1900` (2.63.4) on the tracked SVG gives a PNG byte-identical to the tracked one (`f2e5b337…`, 1900x1318). On inspection the MultiReg row reads `x3 call sites`. Before `ddbf87e6` it read `x2`. The three sites are `sw/litex/milan_soc.py:1986, 1987, 2131`; 2131 is this PR's PHY hold | `receipts/census-regen.log`, `receipts/gitlinks-and-blobs.log` |
| The #820 merge is textual-clean | `git merge-tree --write-tree ddbf87e6 81f78a81` gives rc 0 and tree `755d7ec3`, the recorded merge tree. Four files auto-merge: CHANGELOG, AREA_BUDGET, BUILDING, SUBMODULES. `81f78a81` is PR #820's live head (OPEN) | `receipts/merge-820-retree.log` |
| The merge drops nothing | Each of the 69 files only one side changed equals that side. In the 4 files both sides changed, every line either side added against the base `02ca829a` is present: ours 29/4/3/75 lines and theirs 2/18/14/5 lines, 0 missing | `scripts/merge_keeps_both.py`, `receipts/merge-820-keeps-both.log` |
| The route was judged with the gate this head carries | The blobs of `pp_resource_gate.py`, `_set_selftest.py` and `_mutants.py` are identical at `50e5d08d` (the gate the route used), `81f78a81` and HEAD | `receipts/gitlinks-and-blobs.log` |
| Route figures against the receipt | `head-set-check.log` gives rc 0 and `RESULT: PASS`. AltSpreadLogic_high is selected at 0.365 ns: Slow_0C/85C at 0.365, Fast at 1.633. LUT is 52,021 (+9 on 52,012). SLICE is 15,787, so 63 of 15,850 are left. This matches `AREA_BUDGET.md:149-150` and `SUBMODULES.md:511-517` | `receipts/evidence-manifest-check.log` |
| Receipt integrity | 9 fetched route receipts (including `head-set-check.log`/`.rc`, `head-figures.md`, `prep.log`, the signoff-grade files and the ASLH utilization) match `published_sha256` in the packet's `MANIFEST.json` (`805a0993…`): 0 mismatches | `receipts/evidence-manifest-check.log` |
| gPTP pin of the `1be824fc` route | The branch commit that has processor `1be824fc` (`a0905d4a`) has gptp-processor `f97c1803`. The head and `f7d5fc3c` both have `135afd04` and `a9e84b66`. `SUBMODULES.md:489` is correct | `receipts/gitlinks-and-blobs.log` |
| No present-tense refusal of a passing fall | A grep of all Markdown for refusal or deferral wording finds only historical forms ("Before #818 the gate refused" at `AREA_BUDGET.md:145`, `SUBMODULES.md:427, 499`) and unrelated gate prose. No "after #814 merges" or "routed again" remains | `receipts/present-tense-refusal-grep.log` |
| Docs gates | gate_7, 8, 9, 10, 12, 14, 36, 39, 43 and 45 give rc 0, and so does `git diff --check 02ca829a..HEAD`. gate_8 and gate_45 first exited rc 2 because the pinned Markdown renderer was missing on this host. They were re-run with it installed from `tools/markdown/requirements.txt` (`--require-hashes`) in a disposable venv, and both give rc 0. gate_8 is also rc 0 against base `1e80128f` | `scripts/docs_gates.sh`, `receipts/docs-gates/`, `receipts/docs-gates-venv/` |
| The gate composes at this head | `pp_resource_gate_selftest.py` passes 312 arms and 500 generated cases, rc 0, and imports the set arms. `pp_placement_selftest.py` gives rc 0 | `receipts/gate-selftests-summary.txt` |
| Commit shape | All three delta commits have a one-line message and no trailers. The PR's own non-merge delta touches only `docs/diagrams/cdc_census.{svg,drawio,png}`, `AREA_BUDGET.md` and `SUBMODULES.md`. The only code in the delta (`syn/ooc/*`) is #820's, byte-identical to its head | `receipts/delta-shape.log` |
| Clone restored | `porcelain-lines 0`. The worktree equals the index, which equals HEAD. The index tree is `43d18533`, and the index blob and mode list equals HEAD's. The gitlinks are `external efeb541a`, `gptp-processor 135afd04` and `protocol-processor a9e84b66` | `receipts/integrity-after.log` |

## Findings

### R1 - RESIDUE - Docs (PR body) - PR #822 body, "Status", "Route timing" and "Linked Issue / roles" - text predates the #820 merge

- **Issue.**
  - "Route timing" says the gate is "`syn/ooc/pp_resource_gate.py` as PR #820 has it at `50e5d08d`; that file is not part of this PR". Since `6ffadb07` this PR carries that file, at the same bytes, so the clause is now false.
  - "Status" says "Rounds 4 and 5 each merge into the branch. Neither changes the reset…", but round 6 also merges.
  - "Linked Issue / roles" says "Carries PR #826 (#814)" only.
- **Exact fix.**
  - Replace "; that file is not part of this PR" with "; this PR carries it through `6ffadb07` at `81f78a81`, byte-identical".
  - Replace "Rounds 4 and 5 each merge into the branch. Neither changes" with "Rounds 4, 5 and 6 each merge into the branch. None changes".
  - Add the line "Carries PR #820 (#818): this PR holds its commits through the merge of `818-wns-gate` at `81f78a81`, and merges after it."

### R2 - RESIDUE - Docs - `docs/reference/SUBMODULES.md:503` - "this change" has no referent

- **Issue.** "That path lies outside this change." In a standing reference page, "this change" has no referent. This is the same class as R731-3 RES2. It was not in the delta: it came in at `10767ad8`, within this PR.
- **Exact fix.** "That path lies outside #787's change."

### R3 - RESIDUE - Docs - `docs/design/AREA_BUDGET.md:149-150`, `docs/reference/SUBMODULES.md:511-517` - the re-pin route does not say where it is recorded

- **Issue.** R732-3 F2's required outcome asked for the measured route "citing the receipt", or saying where the route is recorded.
  - The substantive part is met: the verdict, WNS, LUTs and slices are stated and correct, and nothing waits for #814.
  - Neither passage points to where the route is recorded, so a cold reader on dev cannot find the receipt.
  - The neighbouring area-note lines cite no receipts either. This is a pointer only and changes no figure or verdict.
- **Exact fix.**
  - In AREA_BUDGET, append " ([recorded on PR #822](https://github.com/kebag-logic/milan-fpga/pull/822), Route timing)" to line 150, before the full stop.
  - In SUBMODULES, add after line 517: "PR #822 records the route set."

### S1 - SUGGESTION - Docs, Tests - `docs/diagrams/cdc_census.gen.py:122-123` (rendered in `cdc_census.svg`/`.png`, MultiReg row) - the MultiReg note is pre-existing and inaccurate

The generated row's note reads "single-bit status/IRQ levels (incl. the CSR IRQ to sys)". None of the three `MultiReg(` sites in `milan_soc.py` carries the CSR IRQ: they are `link_up`, `full_duplex` and the reboot PHY hold. The PHY hold is a control level, not status or IRQ.

The literal is unchanged since `4a5db279`, and the count that F1 required is correct, so this is outside the PR. Consider one separate Issue that covers both:

- deriving or correcting the note, for example "single-bit levels (link status, the REBOOT PHY hold)";
- R731-3 S2's missing `--check` arm.

### S2 - SUGGESTION - Docs - `docs/reference/SUBMODULES.md:499`

The #806 record (`:427-429`) gives both halves: "Before #818 the gate refused that fall. Under #818 the fall prints a WARNING and passes." The #787 record gives only the first. Consider adding "Under #818 the fall prints a WARNING and passes." for symmetry.

### S3 - SUGGESTION - Docs - `docs/design/AREA_BUDGET.md:151`

"The next growth on the shipping image therefore has no slice room" now follows the re-pin's 63-slice sentence. Its antecedent is the shipping route's 27 slices at line 143. Consider "With 27 slices left on the shipping route, the next growth needs its own owner decision…".

Comment rule: the PR's own delta changes no source comment, so there is no new instance. The `syn/ooc/*` code in the delta is #820's and is out of scope here.

## Prior public findings (read after the independent pass)

| Finding | Severity, lenses | Status at `cbc7c604` |
|---|---|---|
| R731-3 F1 = R732-3 F1: the CDC census is stale | MINOR; Docs | **Resolved.** The generator output equals the tracked svg and drawio. The PNG is re-rendered byte-identical and shows x3. The docs gates give rc 0 |
| R732-3 F2: the #787 route record waits for #814 | MINOR; Docs | **Resolved.** Both passages state the receipt's figures and the PASS verdict, and nothing waits for #814. The missing pointer is carried as R3 (RESIDUE) |
| R731-3 RES1: the route's gPTP provenance | RESIDUE; Docs | **Resolved.** `SUBMODULES.md:489` reads "…at `1be824fc` with FPGA-gPTP `f97c1803`." |
| R731-3 RES2 = R732-3 S1: "this change" in AREA_BUDGET | RESIDUE / SUGGESTION; Docs | **Resolved.** `AREA_BUDGET.md:146` reads "#806's route meets…" |
| R731-3 RES3: "pre-existing" in the PR body | RESIDUE; Docs | **Resolved.** The paragraph is gone, and there is no "pre-existing" in the body |
| R732-3 R1: stale push sentence | RESIDUE; Docs | **Resolved.** No "stays `4aa5666e`" sentence remains |
| R732-3 R2: reviewer placeholders | RESIDUE; Docs | **Resolved.** The body reads `[R731]` and `[R732]` |
| R731-3 S1: refused route left as the latest figure | SUGGESTION; Docs | **Addressed** by `cbc7c604` |
| R731-3 S2: census generator has no `--check` arm | SUGGESTION; Tests | Retained (optional, out of scope). See S1 |
| R731-3 S3: LiteX aggregate member limit | SUGGESTION; Tests | Retained (optional); #826's harness, not in the delta |
| R731-1 F1 = R732-1 R2: `tb/verilator/reboot_ctrl/mutants.py:113-114`, lane label and issue-comment ID in a comment | RESIDUE; Docs | **Retained.** Blob `2528a927` is unchanged, and line 113 still reads `# the [A10] arms of issuecomment-6518083444: …` |
| R732-1 R1: `tb/tools/torture_campaign.py:3135-3139`, link-down comment | RESIDUE; Docs | **Retained.** Blob `43b1fc40` is unchanged |
| R732-1 S1, R731-1 S2: `hdl/milan/KL_reboot_ctrl.sv` | SUGGESTION; RTL, Robustness, Tests | Retained (optional). Blob `d2c74f47` is unchanged |
| R732-1 S2: `mutants.py` saturation control | SUGGESTION; Tests | Retained (optional). Blob unchanged |
| R731-1 S1: `.mac_tx_beat_i` / `.mac_flush_i` wirings | SUGGESTION; Tests, Robustness | Retained (optional). `milan_datapath.sv` blob `443c2085` is unchanged |

## Lens results

```text
[R732] PASS Conformance - git diff f7d5fc3c..cbc7c604 --name-only; hdl/milan/KL_reboot_ctrl.sv d2c74f47, hdl/milan/milan_datapath.sv 443c2085 - the delta touches no HDL, SoC, firmware, test or gitlink, so the AECP REBOOT (IEEE 1722.1-2021 7.4.43) reset path and #787's acceptance evidence are unchanged; the area-record figures match head-set-check.log
[R732] PASS RTL - sw/litex/milan_soc.py:2131 against docs/diagrams/cdc_census.{svg,png}; syn/ooc/pp_resource_gate.py fa26f0f9 at 50e5d08d, 81f78a81 and HEAD - the PHY-hold crossing is drawn as an approved MultiReg; the route at f7d5fc3c binds this head (no RTL, constraint or gitlink change) and was judged by the bytes this head carries
[R732] PASS Robustness - 6ffadb07: merge-tree rc 0 = 755d7ec3, merge_keeps_both.py 0 lines missing on either side - the merge composes without loss; the docs gates' missing-renderer path exits rc 2 rather than passing silently
[R732] PASS Tests - receipts/census-regen.log (svg, drawio and png cmp IDENTICAL), receipts/docs-gates*/ (rc 0), receipts/gate-selftests-summary.txt (312 arms + 500 cases PASS) - F1's verification run as written
[R732] PASS Docs - docs/design/AREA_BUDGET.md:143-151, docs/reference/SUBMODULES.md:487-517, PR #822 body - checked against head-set-check.log, the gitlink history and the round-3 required outcomes; RESIDUE R1-R3 recorded
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | delta file list; reset-path blobs unchanged; route figures against the receipt | R732-4 | cbc7c6043ebf84d5bcd74652dc0a7131b7d54271 |
| RTL | CLEAN | census MultiReg row against the `milan_soc.py` call sites; gate blob identity; no HDL, constraint or gitlink delta | R732-4 | cbc7c6043ebf84d5bcd74652dc0a7131b7d54271 |
| Robustness | CLEAN | #820 merge re-tree and per-side line retention; gate failure path | R732-4 | cbc7c6043ebf84d5bcd74652dc0a7131b7d54271 |
| Tests | CLEAN | census regeneration and PNG render cmp; 10 docs gates and `diff --check`; #818 gate self-tests at head | R732-4 | cbc7c6043ebf84d5bcd74652dc0a7131b7d54271 |
| Docs | CLEAN (RESIDUE R1-R3, R731-1 F1 and R732-1 R1 carried) | AREA_BUDGET and SUBMODULES route passages; CDC census; PR body; the grep for refusal wording | R732-4 | cbc7c6043ebf84d5bcd74652dc0a7131b7d54271 |

Code the delta does not touch keeps the earlier rounds' verdicts. Under the owner's later-round rule, those verdicts carry to this head, because no blob they depend on changed (`receipts/gitlinks-and-blobs.log`).

## Real limits

- **Unsigned packet.** The evidence packet commit `a16caad4` is unsigned (commit verification: unsigned). I checked receipt integrity only against the packet's own `MANIFEST.json`, so the binding is no stronger than that commit.
- **Route measured at the previous head.** The route was measured at `f7d5fc3c`, not at this head. It carries to this head only because the delta changes no HDL, SoC source, constraint or gitlink, and because the gate bytes are identical.
- **Subset of the docs gates.** I ran only the docs-workflow gates that cover the delta's files. I did not run the builder legs (gate_25), the firmware, NVM or saved-state gates, or the act contract gates.
- **PNG renderer version.** The PNG is byte-identical with rsvg-convert 2.63.4 on this host. Another renderer version may differ; `check_diagram_pngs.py` (gate_14, rc 0) is the binding gate.
- **Hosted checks incomplete.** At 2026-10-31T16:35Z the hosted checks at this exact head showed 9 completed success: wire-accountability, verilator-lint, Prepare pinned Yosys, full-ci-gate, firmware-unit, docs-gates-1, docs-check-no-git, changes and bdd-conformance. Physical gPTP was skipped (nightly and manual only). 38 runs were queued or in progress, including the Verilator and Yosys shards (`receipts/hosted-checks-cbc7c604.txt`). I claim no hosted verdict.
- **No manager source bank at this head.** There is none, and none is inferred. Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Hosted and act acceptance at the exact head, including the exhaustive Verilator and Yosys shards still running at review time.
- The current-dev merge candidate (builder and native banks) at the merge turn, with receipts linked on the PR. Merge order: PR #826 (#814), then PR #820 (#818), then this PR. The candidate must keep the `AREA_BUDGET.md:143-151` composition checked here.
- Carry RESIDUE R1-R3, R731-1 F1 and R732-1 R1 to the residue checklist.
- If accepted, open the follow-up Issue for S1 together with R731-3 S2.
- The bench REBOOT run that closes #787.

R732-4 FINISHED
