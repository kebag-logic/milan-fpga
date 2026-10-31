[R731] POSITIVE - exact head cbc7c6043ebf84d5bcd74652dc0a7131b7d54271

# R731-4: internal cleared-context delta review of PR #822 (#787)

- PR: kebag-logic/milan-fpga#822, `787-reboot-reset` -> `dev`. Issue #787.
- Head `cbc7c6043ebf84d5bcd74652dc0a7131b7d54271`, tree `43d185333ff4048986a2080996ed5e482af3f3bc`. Source base `1e80128f`; live dev `02ca829a`.
- Previously reviewed head: `f7d5fc3c` (R731-3 NEGATIVE, R732-3 NEGATIVE).
- Delta `f7d5fc3c..cbc7c604`: three commits.
  - `ddbf87e6` regenerates the CDC census.
  - `6ffadb07` merges PR #820's head `81f78a81` (#818).
  - `cbc7c604` states the round-5 route in `SUBMODULES.md` and `AREA_BUDGET.md`.
- PR #826's and PR #820's own changes are not re-reviewed. This review checks only that they compose here.

## Verdict

POSITIVE. Every prior MINOR (R731-3 F1, R732-3 F1 and F2) is fixed at this head, each against its stated verification. Every prior RESIDUE named for round 6 is fixed. The #820 merge is the automatic merge and drops nothing from either side. The docs gates pass. All five lenses are clean. This round found five RESIDUE items and two SUGGESTIONs. None of them opens a lens.

## Order of work

1. Contract: AGENTS.md and the #787 body.
2. Scope: the round-4/5/6 manager comments on #787 and #822 (issuecomment-6541732410, -6543406776, -6544849367, -6545964041). The round-5 handoff (issuecomment-6544827306).
3. The delta, commit by commit.
4. The author-r5 receipts in the public evidence tree `a16caad4`.
5. My own probes, then a provisional verdict and ledger, written to `receipts/verdict-before-prior-findings.txt` at 16:25:09Z.
6. Only after that: the findings of R731-3 and R732-3, resolved below.

## Probes and receipts (all run in the foreground at the exact head; the clone was restored and verified afterwards)

| Claim checked | Method | Result | Receipt |
|---|---|---|---|
| Census equals its generator (R731-3 F1 / R732-3 F1) | `python3 -I docs/diagrams/cdc_census.gen.py <scratch>/cdc_census`, then `rsvg-convert -w 1900` (the generator's usage line, rsvg-convert 2.63.4), then `cmp` against the tracked files | svg, drawio **and png** byte-equal. `x3 call sites`. `milan_soc.py` has 3 `MultiReg(` sites (lines 1986, 1987, 2131) | `receipts/census-check.log`, `check_census.sh` |
| The PNG shows x3 | Opened `docs/diagrams/cdc_census.png` at the head | The "MultiReg 2-FF" row reads `x3 call sites` | (visual; the PNG is byte-equal to the scratch render) |
| #820 merge is textual-clean and drops nothing | `git merge-tree --write-tree ddbf87e6 81f78a81` vs the recorded tree. Per-file `patch-id --stable` for each side | merge-tree rc 0. Tree `755d7ec3` equals the recorded tree (no manual resolution, so nothing dropped). Merge base `02ca829a` (live dev). 11 #820 files: merge-vs-p1 equals the #820 side, and merge-vs-p2 equals the 787 side, for every file. `AREA_BUDGET.md` matches at `-U0` (`1fc78c67` / `23a26f64`). With `-U3` it differs only because the two sides' adjacent hunks share context | `receipts/merge820-check.txt` |
| #820 gate files here equal #820's reviewed head | `git rev-parse 81f78a81:syn/ooc` vs `cbc7c604:syn/ooc`. `pp_resource_gate.py` at `50e5d08d` vs head | tree `d49dee33` both. Blob `fa26f0f9` both | `receipts/delta-dependency-check.txt` |
| Docs gates | 16 docs-workflow gates, run in parallel, with the pinned Markdown renderer installed from `tools/markdown/requirements.txt --require-hashes` into a scratch venv: docs_check, em-dash `--base 02ca829a`, doc_style (+selftest), gptp_docs, DOC_MAP `--check`, timesync `--check`, solution_docs, submodule_boundaries `--check`, submodule_docs (+selftest), diagram_pngs (+selftest), feature_status, traceability `--check`, pp_resource_gate_selftest | all 16 rc 0. Em dash: 0 findings over 702 added lines in 27 pages, arms 339/339 | `receipts/docs-gates/`, `run_docs_gates.sh` |
| Gates whose inputs round 6 changed | `test_builder.py --gates` with the four gates that read `AREA_BUDGET.md` and the builder docs (23d tier-1 table, 32 key map, and neighbours). rtl-fast's `syn/ooc` steps (`pp_resource_gate.py --selftest`, `_mutants.py`, `check-baseline`, `_set_selftest.py`, `pp_placement_selftest.py`) | builder subset `ALL GATES PASS` (4 of 105, rc 0). Each `syn/ooc` step rc 0 | `receipts/focused/` |
| Whitespace | `git diff --check` against `02ca829a` and against `1e80128f` | rc 0 both | `receipts/diff-check.txt` |
| Round-5 route figures in the docs | Fetched the author-r5 receipts from evidence tree `a16caad4`. Recomputed the git blob ids and checked the sha256 against `MANIFEST.json` | All match. `head-set-check.rc` = 0. ASLH selected at 0.365 ns. Slow_0C/85C +0.365. LUT 52,021. Slice 15,787 of 15,850 (63 free). Fall 0.075 ns, `RESULT: PASS` | `receipts/evidence-verification.txt`, `receipts/head-set-check.copy.log` |
| Delta touches no HDL, SoC, test or gitlink | `git diff --name-only f7d5fc3c cbc7c604` | 14 paths: CHANGELOG, 6 docs pages, 3 census files, 5 `syn/ooc` gate files (#820). Gitlinks `efeb541a` / `135afd04` / `a9e84b66` are unchanged | `receipts/delta-dependency-check.txt` |
| Clone restored | `git status --porcelain --untracked-files=all`, `git write-tree`, ls-files vs ls-tree hashes, gitlinks | Clean. Index tree `43d18533`. Modes and blobs equal HEAD. Gitlinks as above. Only ignored `__pycache__/` and `sw/builder/out/` remain | `receipts/restore-check.txt` |

## Prior findings at this head

| Prior finding | Severity; lens | Status at `cbc7c604` | Evidence |
|---|---|---|---|
| R731-3 F1 = R732-3 F1: the CDC census is stale against its generator | MINOR; Docs | **Resolved** | Generator output equals the tracked svg/drawio. The PNG re-render is byte-equal. `x3`. Docs gates rc 0 (each verification step as written) |
| R732-3 F2: the #787 route record still waits for #814 | MINOR; Docs | **Resolved** | `SUBMODULES.md:511-517` and `AREA_BUDGET.md:149-150` state the re-pin route: #814 cuts, three directives, #818 gate PASS, +0.365 ns, 52,021 LUTs, 63 slices. They match `head-set-check.log`. Neither page presents the route as waiting for #814. `check_submodule_docs.py` and the docs gates pass. The finding also asked for a receipt citation, and none was added; that is carried as RES-E (wording) |
| R731-3 RES1: the `1be824fc` route's gPTP provenance | RESIDUE; Docs | **Resolved** | `SUBMODULES.md:488` "measured at `1be824fc` with FPGA-gPTP `f97c1803`". Confirmed: `667b9bbc` and `1e80128f` pin gPTP `f97c1803` |
| R731-3 RES2 = R732-3 S1: "this change" | RESIDUE / SUGGESTION; Docs | **Resolved** | `AREA_BUDGET.md:146` "#806's route meets ..." |
| R731-3 RES3: PR body "pre-existing" | RESIDUE; Docs | **Resolved** | The paragraph is gone. `receipts/pr822-body.md` has no "pre-existing" |
| R732-3 R1: stale push sentence | RESIDUE; Docs | **Resolved** | No "pushed head stays" or "until the manager pushes" in the body |
| R732-3 R2: reviewer placeholders | RESIDUE; Docs | **Resolved** | Body lines 71-72 name `[R731]` and `[R732]` |
| R731-3 S1: the refused `1be824fc` route is the latest figure | SUGGESTION; Docs | **Addressed** | The re-pin route is stated, and the `1be824fc` fall is in the past tense ("Before #818 the gate refused", `SUBMODULES.md:499`; "was", `AREA_BUDGET.md:148`) |
| R731-3 S2: the census generator has no `--check` arm | SUGGESTION; Tests | **Retained** (optional) | `cdc_census.gen.py` still has no `--check`. A follow-up Issue would stop recurrence |
| R731-1 F1 = R732-1 R2: `tb/verilator/reboot_ctrl/mutants.py:113-114` shows a lane label and an issue-comment ID | RESIDUE; Docs | **Retained** | Blob `2528a927` unchanged (tracked by #746). Fix as given in R731-1 |
| R732-1 R1: `tb/tools/torture_campaign.py:3135-3139`, the link-down comment omits the egress wait | RESIDUE; Docs | **Retained** | Blob `43b1fc40` unchanged |

Required check "no present-tense refusal of a fall the #818 gate passes": I grepped every tracked `*.md` for refusals and for 0.333 / 0.408. The only refusals of these falls are "Before #818 the gate refused" at `CHANGELOG.md:104`, `AREA_BUDGET.md:145` and `SUBMODULES.md:499`. The other "refuses" hits are unrelated gates. **Met.**

## New findings this round

### RES-A - RESIDUE - Docs (PR body) - PR #822 body, "Route timing", "that file is not part of this PR"
- **Evidence:** Since `6ffadb07` this PR carries `syn/ooc/pp_resource_gate.py` through PR #820's head. The file is byte-equal to `50e5d08d` (blob `fa26f0f9`).
- **Exact fix:** replace "(`syn/ooc/pp_resource_gate.py` as PR #820 has it at `50e5d08d`; that file is not part of this PR)" with "(`syn/ooc/pp_resource_gate.py` as PR #820 has it at `50e5d08d`, which this PR now carries unchanged through the merge of `81f78a81`)".

### RES-B - RESIDUE - Docs (PR body) - PR #822 body, "Status", "**Gates at the head pass.**"
- **Evidence:** The head line is now `cbc7c604`. Most results in that list were measured at `f7d5fc3c` (author-r5) or `3e67de9c`. The substance carries to `cbc7c604`:
  - The round-6 paths are read only by the docs gates, builder gates 23d/32 and rtl-fast's `syn/ooc` steps. I re-ran each at this head, rc 0.
  - The route inputs are unchanged.
- So only the attribution is stale.
- **Exact fix:** "**Gates at `f7d5fc3c` pass, and carry to `cbc7c604`.** Round 6 changes only documentation, the census records and PR #820's gate files. The docs gates pass at `cbc7c604`."

### RES-C - RESIDUE - Docs (PR body) - Contents line 5, "Linked Issue / roles" line 68, "Status" line 17
- **Evidence:** Line 5 says "carrying PR #826's commits", and line 68 says "Carries PR #826 (#814): ... merges after it". Both omit PR #820, which line 17 names. "Rounds 4 and 5 each merge into the branch. Neither changes ..." omits round 6's merge of #820.
- **Exact fix:**
  - Line 5: "carrying PR #826's and PR #820's commits".
  - Line 68: "Carries PR #826 (#814) and PR #820 (#818): this PR holds their commits, through the merges of `4ee2aa96` and `81f78a81`, and merges after both."
  - Line 17: "Rounds 4, 5 and 6 each merge into the branch. None changes ...".

### RES-D - RESIDUE - Docs - `docs/design/AREA_BUDGET.md:150`, `:147`, `:149`; `docs/reference/SUBMODULES.md:511`
- **Evidence, line 150:** "has WNS +0.365 ns at every slow corner, 52,021 LUTs and 63 of 15,850 slices left" can be read as 52,021 LUTs left. The figures are correct (`utilization.rpt`: 52,021 used, 15,787 of 15,850 slices).
- **Evidence, gPTP pins:** The two #787 routes ran on different gPTP pins: `f97c1803` at `1be824fc`, `135afd04` at `f7d5fc3c`. `AREA_BUDGET.md` names neither, so the 57 -> 63 slice change reads as the processor's alone.
- **Exact fix:**
  - Line 150: "Its best directive, AltSpreadLogic_high, has WNS +0.365 ns at every slow corner, uses 52,021 LUTs and leaves 63 of 15,850 slices."
  - Line 147: add "and FPGA-gPTP `f97c1803`" after "with the REBOOT reset".
  - Line 149: "The re-pin to processor `a9e84b66` at FPGA-gPTP `135afd04`, routed with ...".
  - `SUBMODULES.md:511`: "The re-pin route, at FPGA-gPTP `135afd04`, carries the #814 cuts."

### RES-E - RESIDUE - Docs - `docs/design/AREA_BUDGET.md:149`, `docs/reference/SUBMODULES.md:517`
- **Evidence:** R732-3 F2's required outcome asked the record to cite the receipt. Both pages state the verdict and figures correctly but cite no source.
- **Exact fix:** link "passes the [#818] gate" in `AREA_BUDGET.md:149` to the manager's round-5 acceptance on #787 (issuecomment-6544849367), which names the author-r5 receipts. Or add "(receipt: PR #822 evidence `author-r5/receipts/route/results/head-set-check.log`)". Make the same edit at `SUBMODULES.md:517`.

### SUG-1 - SUGGESTION - Docs, Tests - `docs/diagrams/cdc_census.gen.py:122-123` (rendered at `cdc_census.svg:114`)
- **Evidence:** The MultiReg row's fixed descriptor reads "single-bit status/IRQ levels (incl. the CSR IRQ to sys)". None of the three call sites carries an IRQ. Two are link-status levels (`milan_soc.py:1986-1987`). One is this PR's PHY-hold control level (`:2131`).
- **Why a suggestion:** The descriptor is pre-existing, since no MultiReg at `1e80128f` carried an IRQ either. The generator is outside this PR's diff. The count, which is what this PR changed, is correct.
- **Suggestion:** Open an Issue to make the descriptor generated or neutral (for example "single-bit levels"). It can share that Issue with R731-3 S2's `--check` arm.

### SUG-2 - SUGGESTION - Docs - `docs/reference/SUBMODULES.md:492-503`
The superseded `1be824fc` route is described in the present tense ("57 of 15,850 slices remain", "WNS is +0.107 ns", "The worst path is"). `AREA_BUDGET.md:148` now uses the past tense ("was"). Aligning the tense would make the superseded figures read as history.

Comment rule: the reviewed delta adds no source comment of this lane. `ddbf87e6` changes generated text only, and `cbc7c604` changes Markdown only. `6ffadb07` brings in #820's sources, which are not re-reviewed here. No new RESIDUE under that rule.

## Lens results

```text
[R731] PASS Conformance - receipts/census-check.log; receipts/evidence-verification.txt (head-set-check.log blob 9e79c034, utilization.rpt blob 91238860); docs/reference/SUBMODULES.md:488-517; docs/design/AREA_BUDGET.md:143-150 - each prior finding's required outcome is met as written: generator output equals the tracked census, the PNG re-render is byte-equal and shows x3 against 3 MultiReg( sites; the #787 records state the re-pin route's verdict, WNS, LUT and slices exactly as head-set-check.log and utilization.rpt give them; no present-tense refusal of a fall the #818 gate passes; #787's frozen acceptance is untouched by a docs/records-only delta
[R731] PASS RTL - receipts/delta-dependency-check.txt (git diff --name-only f7d5fc3c cbc7c604; gitlinks efeb541a/135afd04/a9e84b66) - the delta changes no HDL, no SoC Python and no gitlink; the census count now matches milan_soc.py:2131's PHY-hold MultiReg into sys; R731-3's RTL verdict at f7d5fc3c carries, since nothing it depends on changed
[R731] PASS Robustness - receipts/merge820-check.txt; receipts/delta-dependency-check.txt (syn/ooc tree d49dee33 at 81f78a81 and at cbc7c604) - the #820 merge is the automatic merge (tree 755d7ec3 = merge-tree), every file carries both sides' patches, and the merged gate files are byte-equal to #820's reviewed head, so no reset, timeout, fault or ordering path of this lane changes and #820's gate behaviour is unchanged by composition
[R731] PASS Tests - receipts/focused/builder-leg.log (gates 23d/32 subset ALL GATES PASS), receipts/focused/rtlfast-ooc-steps.log (5 resource-gate steps rc 0), receipts/docs-gates/SUMMARY.txt (16/16 rc 0) - every gate whose inputs round 6 changed re-passes at this head; no test of this lane changed and none is weakened; the census regeneration is reproduced from the generator, not taken from the commit
[R731] PASS Docs - docs/diagrams/cdc_census.{svg,drawio,png}; docs/design/AREA_BUDGET.md:143-150; docs/reference/SUBMODULES.md:486-517; CHANGELOG.md:53-104; receipts/pr822-body.md; receipts/docs-gates/ - the census, area note and adoption record are current against the generator and the round-5 receipts, and the docs gates pass; RES-A..RES-E are wording-only residue and SUG-1/SUG-2 are optional, so neither opens this lens
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Prior findings' required outcomes; the census regeneration; the #787 route record against `head-set-check.log` / `utilization.rpt`; #787 acceptance | R731-4 | `cbc7c6043ebf84d5bcd74652dc0a7131b7d54271` |
| RTL | CLEAN | The delta's path list and gitlinks (no HDL/SoC change); census count vs `milan_soc.py:2131`; R731-3's RTL coverage at `f7d5fc3c` carries | R731-4 | `cbc7c6043ebf84d5bcd74652dc0a7131b7d54271` |
| Robustness | CLEAN | #820 merge composition (merge-tree, per-file patch-ids); `syn/ooc` tree equality with `81f78a81` | R731-4 | `cbc7c6043ebf84d5bcd74652dc0a7131b7d54271` |
| Tests | CLEAN | 16 docs gates; builder gates 23d/32 subset; rtl-fast `syn/ooc` steps; census reproduced | R731-4 | `cbc7c6043ebf84d5bcd74652dc0a7131b7d54271` |
| Docs | CLEAN (RES-A..E and the two prior retained RESIDUE go to the residue checklist; SUG-1, SUG-2 and R731-3 S2 optional) | Census svg/drawio/png; `AREA_BUDGET.md`; `SUBMODULES.md`; `CHANGELOG.md`; PR body | R731-4 | `cbc7c6043ebf84d5bcd74652dc0a7131b7d54271` |

## Real limits

- **No manager source bank at this head.** This review claims none. Source-head execution evidence is the author's receipts, at `f7d5fc3c` and earlier. My re-runs are only the docs gates, the builder 23d/32 subset and rtl-fast's `syn/ooc` steps. I ran no LiteX, Verilator, milan_dp, builder-full, Yosys or route bank.
- **The route was not re-run.** It was measured at `f7d5fc3c` with #820's gate at `50e5d08d`. I verified the receipts by git blob id and by `MANIFEST.json` sha256. The evidence commit `a16caad4` itself is unsigned (`verification: unsigned`). Integrity rests on those hashes, not on a signature.
- **Hosted checks at `cbc7c604` were still running** when I inspected them (wire-accountability, verilator-lint and full-ci-gate succeeded; Verilator/Yosys shards, firmware and docs jobs queued or in progress). The physical gPTP job was skipped. I make no hosted claim.
- **Physical calibration was NOT RUN**, and field skips are not hardware proof. #787 stays open for the bench REBOOT run.
- **The PNG was compared byte-for-byte with one local renderer** (rsvg-convert 2.63.4). Equality on another renderer version is not shown.

## Pending manager duties

- Validate the current-dev merge candidate (builder and native banks) at the merge turn, and link the receipts. Merge order: PR #826, PR #820, then this PR.
- Own hosted and act acceptance for `cbc7c604`. The Verilator/Yosys shards were in flight at inspection.
- Carry RES-A..RES-E, R731-1 F1 (`mutants.py:113-114`) and R732-1 R1 (`torture_campaign.py:3135-3139`) to the residue checklist.
- Consider one follow-up Issue for SUG-1 together with R731-3 S2 (a census `--check` arm).
- Bench REBOOT run for #787's end-to-end claim.

R731-4 FINISHED
