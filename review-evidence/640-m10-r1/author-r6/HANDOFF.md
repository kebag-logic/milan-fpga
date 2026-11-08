# HANDOFF - [A720p] issue #640, PR #835 round 6 (sync with dev, docs only)

Status: REVIEW READY (2026-11-08). Head 72816d26a7e2a29db5bc198ff65056ee4c5790b4, one merge of dev 0a75aa77 on round 5's d85da329. Every docs.yml step that can run locally is rc 0 on a clean clone (65 steps; 31 hosted-only steps not run, each with its reason; verifier rc 0). Every lane step is rc 0. Local only, nothing pushed.

- Lane: $LANES/640-mark2-charter, branch 640-charter-followup. Started at d85da3297f0b664ac4f2b63eac3c5fd36ed4eb73, round 5's head. Both round 5 reviews are POSITIVE there: R765-5 (PR #835 issuecomment-6586963259) and R766-5 (issuecomment-6587152040).
- Remote checked: https://github.com/kebag-logic/milan-fpga.git
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6719142932 (text: evidence/taken.md)
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6719723402 (text: evidence/review_ready.md)
- New head: 72816d26a7e2a29db5bc198ff65056ee4c5790b4 (tree f9498ee5a4a88bf63453a3a2d162a1b225a7715e). One merge commit, "Merge dev 0a75aa77 into the #640 charter follow-up (#640)". Its parents are d85da329 and origin/dev 0a75aa774b89ac89351700f63dd8cbb89694af6c. `git merge-base HEAD origin/dev` is now 0a75aa77. Nothing pushed.
- How: `git fetch origin`, then `git merge --no-ff origin/dev`. No rebase, force or amend. No hooks are configured in the repo.
- Dev since 503bc97c: 9 first-parent merges, 231 commits, 130 files (14,839+, 2,572-). The order said "50 commits"; the counted figures are these.
- Head against dev: only the branch's four pages differ, 231+ / 53-, exactly the branch's delta against 503bc97c before the merge. No RTL, firmware, generator, gate or configuration change.

## Read this first

1. **One conflict, both sides kept.** docs/findings/README.md: dev's 234 row plus the branch's 649 row. The other two shared pages auto-merged cleanly and were read for meaning.
2. **No other change.** No regeneration commit: every generator is fresh at the merge. The branch's added and removed lines against dev 0a75aa77 are identical to its delta against 503bc97c before (`diff` of the two `-U0` line sets is empty).
3. **Census re-run on current dev, as R765-5 and R766-5 asked:** PASS at the merge, against dev's `sw/litex/milan_soc.py`; the round 1 control still fails.
4. **Two lane steps needed a second look**, both explained in the gate notes: behave's first attempt lacked PyYAML; the changed-block style probe against d85da329 reports dev's own prose.
5. The merge head must be pushed by whoever holds push rights; until then GitHub shows PR #835 as CONFLICTING (it reads d85da329).

## PRs dev brought (first-parent merges, 503bc97c..0a75aa77)

| Merge | PR | Issue | Subject |
|---|---|---|---|
| e61a4afa | #831 | #829 | Run the gPTP plane on the MII port at 100 Mb/s |
| 604899c0 | #836 | #737 | Split the hosted LiteX simulations into three measured elaborate legs |
| cc204c6f | #815 | #797 D0 | Generate the documentation audit from every tracked document and verify the release-facing pages |
| 87e9d03a | #834 | #833 | Bound and explain the owned-process cleanup under load |
| 3f6bef88 | #841 | #839 | Hold the CSR-addressed transmitters until the station MAC is written |
| 35448611 | #842 | #840 | Prototype identity, 1000BASE-T-only advertisement on 1G PHYs, the stricter-reading page |
| bfd4a215 | #849 | #848 | Drop line counts from the generated audit page |
| 1eb5289d | #847 | #845 | Adopt protocol-processor main 92100657 |
| 0a75aa77 | #846 | #843 | Adopt FPGA-gPTP main 1616fc8f |

## Conflicts and resolutions

Files both sides changed since 503bc97c: docs/findings/README.md, docs/design/AREA_BUDGET.md, docs/design/MARK_II_AREA_PLAN.md.

| File | Git result | Resolution |
|---|---|---|
| docs/findings/README.md:25-26 | CONFLICT, two adjacent table rows | Dev changed the 234 row (route record now #843's of 2026-11-07, standalone records #845's of 2026-11-06). The branch changed the 649 row ("a tenth of the gap to NFR-RES-01's former 60 % target"). Kept dev's 234 row and the branch's 649 row, each verbatim. Done by a scripted splice that asserts each side holds exactly those two rows (no hand edit of text). `git diff origin/dev HEAD` on the file now shows only the 649 row; `git diff d85da329 HEAD` only the 234 row. |
| docs/design/AREA_BUDGET.md | auto-merged | Dev's #845 / #843 record lines and "The [#799] route was 13,972 over it" (:130) sit beside the branch's headroom sentences (:127-128) and acceptance bar (:179-181). Read the merged section :115-200: coherent, no duplicate or contradicting line. |
| docs/design/MARK_II_AREA_PLAN.md | auto-merged | Dev changed :61 (+0.440 to +0.242 ns record) and :1097-1099 (#845 and #843 records). No branch line cites a gate record, the +0.440 ns figure or #799's anchor (grep of the branch's added lines for record, anchor, slices, WNS and pins). |

## Generated pages

No generator output changes, so there is no regeneration commit.

| Generator | Result at the merge (lane, before the gate run) |
|---|---|
| `scripts/docs_inventory.py --check` | documentation inventory: OK (547 lines, docs/DOCUMENTATION_AUDIT.md is fresh) |
| `scripts/gen_toc.py --check` | TOC gate: OK (152 pages) |
| `docs/traceability/gen_module_matrix.py --check` | up to date (80 modules) |
| `docs/DOC_MAP.gen.py`, `timesync_chain.gen.py`, `submodule_boundaries.gen.py` `--check` | rc 0 (and again in gate_10 / gate_12 below) |

The audit page's rows for the branch's four pages read "current, no recorded contradiction". `scripts/docs_inventory.json` names none of them.


## Gate table

Every `run:` step of `.github/workflows/docs.yml` at the head, job by job, sequentially. Each job ran on its own fresh `--shared` clone of the lane at 72816d26, made by the 829-a725c runner (`run_docs_yml.py`, copied with this lane's LANE, VENV and HOME; evidence/tools/). Rows come from the 829-a725c verifier at the head (`verify_docs_yml.py`): "65 steps ran, 31 not run with a reason, 0 bad", rc 0. Run 2026-11-08T09:18:17+01:00 to 10:14:26+01:00.

Environment: venv copied from 640-a720o (scratch); scratch HOME copied from 640-a720o with its SDK removed, so ci_step_28 installed the pinned RV32 SDK fresh (the shared SDK was not touched). Submodules came from their .gitmodules URLs through the workflow's own fetch steps. Every job's `tree-after` status is empty.

| Job | Step | Name | rc | Last line |
|---|---|---|---:|---|
| wire-accountability | ci_step_1 | Set CPU-derived job budgets | 0 | # clone $VALIDATION_STORAGE/640-a720p/gates/wire-accountability/wt |
| wire-accountability | ci_step_3 | Fetch the engine authority the builder derives from | 0 | Submodule path 'gptp-processor': checked out '1616fc8f062fbf58c35ad31674b5b233207bbdb8' |
| wire-accountability | ci_step_4 | Advertised-vs-emitted gate (green since 2026-07-28, item 00) | 0 | RESULT: PASS |
| wire-accountability | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs-check-no-git | ci_step_1 | Retain checkout identity before removing metadata | 0 | # clone $VALIDATION_STORAGE/640-a720p/gates/docs-check-no-git/wt |
| docs-check-no-git | ci_step_2 | Set CPU-derived job budgets | 0 | # clone $VALIDATION_STORAGE/640-a720p/gates/docs-check-no-git/wt |
| docs-check-no-git | ci_step_3 | Strip git metadata, then run the docs gate | 0 | feature_status: 0 finding(s) |
| docs-check-no-git | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs-gates-0 | ci_step_1 | Set CPU-derived job budgets | 0 | # clone $VALIDATION_STORAGE/640-a720p/gates/docs-gates-0/wt |
| docs-gates-0 | gate_1 | Build the validated HDL reference | 0 | Wrote: $VALIDATION_STORAGE/640-a720p/gates/docs-gates-0/runner_temp/milan-hdl-reference/index.html |
| docs-gates-0 | ci_step_5 | Install the python gate dependencies | 0 | [notice] To update, run: pip install --upgrade pip |
| docs-gates-0 | ci_step_7 | Install the pinned Markdown renderer | 0 | [notice] To update, run: pip install --upgrade pip |
| docs-gates-0 | ci_packages_6 | Resolve exact package downloads 6 | NOT RUN | apt package index for librsvg2-bin; this host has rsvg-convert installed and no apt |
| docs-gates-0 | ci_step_10 | Install diagram gate dependencies | NOT RUN | sudo apt-get for librsvg2-bin; rsvg-convert is installed here and the venv carries wavedrom==2.0.3.post3 |
| docs-gates-0 | gate_7 | Link health, wording, dead-reference and local-info gate | 0 | docs_check: 0 finding(s) across 214 md files + 1448 scrubbed text files, scrub self-test 23/23, routing arms 4/4 [git ls-files] |
| docs-gates-0 | gate_8 | Added-line em-dash gate | 0 | check_em_dash: 0 finding(s) over 231 added line(s) in 4 changed Markdown page(s), 0 mirrored label(s) exempt, arms 339/339 [0a75aa77..HEAD] |
| docs-gates-0 | gate_9 | Concise audience documentation gate | 0 | gPTP documentation selftest: OK (30 controls) |
| docs-gates-0 | gate_10 | Audience diagram no-drift gate | 0 | time-sync diagram selftest: OK (source, status, XML, raster) |
| docs-gates-0 | gate_11 | Product solution source-fact gate | 0 | solution documentation selftest: OK (45 mutation controls) |
| docs-gates-0 | gate_12 | Verified submodule documentation gate | 0 | submodule documentation selftest: OK (table and diagram controls) |
| docs-gates-0 | gate_13 | HDL timing diagram no-drift gate | 0 | WaveDrom current: docs/diagrams/wd_gptp_pdelay.json |
| docs-gates-0 | gate_14 | Published diagram PNG gate | 0 | diagram PNG selftest: OK (6 rasters, 28 mutation controls) |
| docs-gates-0 | gate_15 | Milan feature-status consistency gate | 0 | feature_status: 0 finding(s) |
| docs-gates-0 | gate_16 | Traceability matrix no-drift gate | 0 | traceability matrix up to date (80 modules, 0 untested <= ratchet 0, 0 archived) |
| docs-gates-0 | ci_step_21 | Fetch the builder source dependencies | 0 | Submodule path 'third_party/verilog-axis': checked out '48ff7a7e2ef782cf778d47910cf85835c64b1bce' |
| docs-gates-0 | gate_18 | Imported gPTP documentation gate | 0 | source evidence selftest: PASS (7 arms) |
| docs-gates-0 | gate_19 | Code-quality measurement self-tests | 0 | 18 checks: 18 PASS, 0 FAIL |
| docs-gates-0 | ci_step_25 | Install the pinned sv2v release | NOT RUN | sudo install into /usr/local/bin through /tmp; /usr/local/bin/sv2v is already the pinned v0.0.12 |
| docs-gates-0 | gate_21 | Bare-metal scope gate | 0 | baremetal-only selftest: PASS (867 arm(s)) |
| docs-gates-0 | ci_step_28 | Install and verify the pinned RV32 SDK | 0 | SDK fresh installation: verified |
| docs-gates-0 | gate_24 | Compiler-absent firmware controls | 0 | GATE 1b PASS; 2 NOT RUN; 0 actual firmware compiler invocations |
| docs-gates-0 | gate_26 | NVM record-space gate | 0 | 0 finding(s) across 5 config(s): the inventory's (group, index) key set is exactly the set the shape requires with no key claimed twice, every persist |
| docs-gates-0 | gate_27 | Capture measurement census and clock gate | 0 | PASS: capture census, clocks, both timing arms and receipt agree |
| docs-gates-0 | gate_28 | Saved-state writer gate | 0 | saved-state writer gate: OK across 5 shape(s), and every planted defect reddened |
| docs-gates-0 | gate_29 | SoC source-list gate (Vivado would fail 40 min in without this) | 0 | iob_pack_selftest: 22 arms, 21 mutants, 0 failure(s) |
| docs-gates-0 | gate_30 | RTL source-list drift gate | 0 | 50 checks: 50 PASS, 0 FAIL |
| docs-gates-0 | gate_31 | Boundary-unit naming ratchet | 0 | 66 checks: 66 PASS, 0 FAIL |
| docs-gates-0 | gate_32 | Port contract gate | 0 | 82 checks: 82 PASS, 0 FAIL |
| docs-gates-0 | gate_33 | Fail-fast ratchet | 0 | 106 checks: 106 PASS, 0 FAIL |
| docs-gates-0 | gate_34 | TODO ownership gate | 0 | 45 checks: 45 PASS, 0 FAIL |
| docs-gates-0 | gate_35 | Test-evidence ratchet | 0 | 105 checks: 105 PASS, 0 FAIL |
| docs-gates-0 | gate_36 | Mechanical hygiene ratchet | 0 | 35 checks: 35 PASS, 0 FAIL |
| docs-gates-0 | gate_37 | SystemVerilog idiom gate | 0 | 55 checks: 55 PASS, 0 FAIL |
| docs-gates-0 | gate_38 | C and C++ idiom gate | 0 | 75 checks: 75 PASS, 0 FAIL |
| docs-gates-0 | gate_39 | Python idiom gate | 0 | 54 checks: 54 PASS, 0 FAIL |
| docs-gates-0 | gate_40 | Shell idiom gate | 0 | 48 checks: 48 PASS, 0 FAIL |
| docs-gates-0 | gate_43 | Doc cited-path gate | 0 | doc path gate: OK (1638 cited paths all resolve, 2 allowlisted; 10 line anchor(s) within their file) |
| docs-gates-0 | gate_44 | Archive integrity gate | 0 | archive selftest: OK (24 controls) |
| docs-gates-0 | gate_45 | Per-page contents gate | 0 | TOC gate: OK (152 page(s) carry an annotated contents list, 18 below the 3-section threshold) |
| docs-gates-0 | gate_46 | Documentation inventory freshness gate | 0 | documentation inventory selftest: OK (60 controls) |
| docs-gates-0 | gate_47 | AEM store generator self-test | 0 | gen_aem_store self-test: PASS |
| docs-gates-0 | gate_48 | Sweep/build shape gate | 0 |   [self-test] OK: 1 drift(s) reported |
| docs-gates-0 | gate_49 | Deploy shape gate | 0 |   [selftest] OK: 1 drift(s) reported |
| docs-gates-0 | gate_50 | Entity shape gate | 0 | RESULT: PASS |
| docs-gates-0 | ci_step_53 | Fetch inventory dependencies | 0 | Submodule path 'third_party/tsn-c-stack': checked out '70936b77dc41981e192438388cd0aced69954f18' |
| docs-gates-0 | gate_51 | CI scheduling and evidence controls | 0 | manifest comparison controls: PASS |
| docs-gates-0 | ci_step_55 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context |
| docs-gates-0 | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs-gates-1 | ci_step_1 | Set CPU-derived job budgets | 0 | # clone $VALIDATION_STORAGE/640-a720p/gates/docs-gates-1/wt |
| docs-gates-1 | ci_step_3 | Install the python gate dependencies | 0 | [notice] To update, run: pip install --upgrade pip |
| docs-gates-1 | ci_step_5 | Install the pinned Markdown renderer | 0 | [notice] To update, run: pip install --upgrade pip |
| docs-gates-1 | ci_packages_4 | Resolve exact package downloads 4 | NOT RUN | apt package index for librsvg2-bin; this host has rsvg-convert installed and no apt |
| docs-gates-1 | ci_step_8 | Install diagram gate dependencies | NOT RUN | sudo apt-get for librsvg2-bin; rsvg-convert is installed here and the venv carries wavedrom==2.0.3.post3 |
| docs-gates-1 | ci_step_9 | Fetch the builder source dependencies | 0 | Submodule path 'third_party/verilog-axis': checked out '48ff7a7e2ef782cf778d47910cf85835c64b1bce' |
| docs-gates-1 | ci_step_11 | Install the pinned sv2v release | NOT RUN | sudo install into /usr/local/bin through /tmp; /usr/local/bin/sv2v is already the pinned v0.0.12 |
| docs-gates-1 | ci_step_13 | Install and verify the pinned RV32 SDK | 0 | SDK cache hit: verified |
| docs-gates-1 | gate_25_0 | End-station builder gates, leg 0 of 2 | 0 | ALL GATES PASS EXCEPT 1 NOT RUN |
| docs-gates-1 | ci_step_15 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context |
| docs-gates-1 | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs-gates-2 | ci_step_1 | Set CPU-derived job budgets | 0 | # clone $VALIDATION_STORAGE/640-a720p/gates/docs-gates-2/wt |
| docs-gates-2 | ci_step_3 | Install the python gate dependencies | 0 | [notice] To update, run: pip install --upgrade pip |
| docs-gates-2 | ci_step_5 | Install the pinned Markdown renderer | 0 | [notice] To update, run: pip install --upgrade pip |
| docs-gates-2 | ci_packages_4 | Resolve exact package downloads 4 | NOT RUN | apt package index for librsvg2-bin; this host has rsvg-convert installed and no apt |
| docs-gates-2 | ci_step_8 | Install diagram gate dependencies | NOT RUN | sudo apt-get for librsvg2-bin; rsvg-convert is installed here and the venv carries wavedrom==2.0.3.post3 |
| docs-gates-2 | ci_step_9 | Fetch the builder source dependencies | 0 | Submodule path 'third_party/verilog-axis': checked out '48ff7a7e2ef782cf778d47910cf85835c64b1bce' |
| docs-gates-2 | ci_step_11 | Install the pinned sv2v release | NOT RUN | sudo install into /usr/local/bin through /tmp; /usr/local/bin/sv2v is already the pinned v0.0.12 |
| docs-gates-2 | ci_step_13 | Install and verify the pinned RV32 SDK | 0 | SDK cache hit: verified |
| docs-gates-2 | gate_25_1 | End-station builder gates, leg 1 of 2 | 0 | ALL GATES PASS EXCEPT 16 NOT RUN |
| docs-gates-2 | gate_41 | CI event and SHA contract gate | 0 | selftest: PASS (2207 contract items, 5501 arms) |
| docs-gates-2 | gate_42 | Local act runner contract gate | 0 | selftest: PASS |
| docs-gates-2 | ci_step_17 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context |
| docs-gates-2 | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs-check | ci_step_1 | Set CPU-derived job budgets | NOT RUN | this job has no local gate |
| docs-check | ci_step_4 | Install the pinned evidence reader | NOT RUN | installs the reader only docs-check's hosted verify uses |
| docs-check | ci_step_6 | Require every gate exactly once | NOT RUN | verifies uploaded hosted receipts; this job's gates ran above |
| docs-check | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| ci-manifest | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration, no local gate |
| ci-manifest | step2 | Fetch inventory dependencies | NOT RUN | CI orchestration, no local gate |
| ci-manifest | step4 | Install the pinned evidence reader | NOT RUN | CI orchestration, no local gate |
| ci-manifest | ci_collect | Collect actual runtime evidence | NOT RUN | reads a hosted run's artifacts |
| ci-fail-fast | ci_step_1 | Set CPU-derived job budgets | NOT RUN | CI orchestration, no local gate |
| ci-fail-fast | ci_observe | Observe the first failed job | NOT RUN | watches a hosted run |
| ci-fail-fast | ci_step_3 | Cancel this run and sibling workflows | NOT RUN | cancels a hosted run |
| ci-fail-fast | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| ci-cancel-tail | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration, no local gate |
| ci-cancel-tail | step2 | Cancel confirmed terminal failures | NOT RUN | cancels a hosted run |

| Lane step | Command | rc | Last line |
|---|---|---:|---|
| inventory_check | `docs_inventory.py --check` | 0 | documentation inventory: OK (547 lines, docs/DOCUMENTATION_AUDIT.md is fresh) |
| doc_style | `check_doc_style.py` (its 24 current documents) | 0 | documentation style: OK (24 current documents) |
| style_merge_new | check_doc_style's `analyze()` on all 33 pages the merge touched, at the merge and both parents: findings neither parent has | 0 | merge style probe: 33 page(s), 0 new finding(s) [d85da329 + 0a75aa77 -> 72816d26] |
| style_merge_new_control | the same with a planted 12-word sentence; must report it (negated) | 0 | merge style probe: 33 page(s), 1 new finding(s) [d85da329 + 0a75aa77 -> 72816d26] |
| style_blocks_vs_dev | changed-block probe, the branch's 4 pages against dev 0a75aa77 | 0 | docs/findings/README.md: 0 finding(s) in changed blocks |
| style_blocks_vs_r5 | changed-block probe, the 32 pages dev changed, against d85da329 (dev's own prose; every finding is also on a parent, per style_merge_new; informational) | 1 | tb/verilator/pp_shadow/README.md: 0 finding(s) in changed blocks |
| behave | `cd tests && behave --no-capture -f plain` (behave + PyYAML) | 0 | Took 0min 2.460s |
| behave_attempt1_noyaml | first behave attempt, venv without PyYAML (superseded by the row above) | 1 | endstation_builder: PyYAML required (python3 -m pip install pyyaml) |
| diffcheck_mergebase | `git diff --check 0a75aa77 HEAD` (merge base) | 0 | # head 72816d26a7e2a29db5bc198ff65056ee4c5790b4 lane step diffcheck_mergebase: git diff --check 0a75aa774b89ac89351700f63dd8cbb89694af6c HEAD |
| diffcheck_oldbase | `git diff --check 503bc97c HEAD` | 0 | # head 72816d26a7e2a29db5bc198ff65056ee4c5790b4 lane step diffcheck_oldbase: git diff --check 503bc97cd4f24ad07596c17e7188f2024617972d HEAD |
| em_dash_mergebase | `check_em_dash.py --base 0a75aa77` | 0 | check_em_dash: 0 finding(s) over 231 added line(s) in 4 changed Markdown page(s), 0 mirrored label(s) exempt, arms 339/339 [0a75aa77..HEAD] |
| reader_check_baseline | AREA_BUDGET.md's reader: `pp_resource_gate.py check-baseline` | 0 | baseline PASS: 3 endpoints |
| reader_service_bounds | MAILBOX_SPLIT.md's reader: `ctrl_service_bounds.arm_service_bounds` | 0 | rc 0 |
| census_coverage | `census_coverage.py` at the merge, against dev's `sw/litex/milan_soc.py` | 0 | RESULT: PASS |
| census_coverage_control | `! census_coverage.py` against the round 1 page 3f8ed303 (must fail) | 0 | RESULT: FAIL |

Notes:
- **Skip list re-keyed.** Dev's #815 inserts gate_46 (inventory freshness) and renumbers docs-gates-0's later steps. The hosted-only "Record executed gate outcomes" step moved from `ci_step_54` to `ci_step_55`. My copy of `not_run.json` keys it as `docs-gates-0/ci_step_55`, same reason; nothing else changed (evidence/tools/not_run.json).
- **Lane steps** ran on a separate fresh clone of the head (scratch `gates/extra/wt`), submodules taken from docs-gates-0's clone, origins reset to their .gitmodules URLs (logs/extra__submodules.txt). Its `git status --porcelain` was empty after every step.
- **behave:** rtl-fast installs only behave on a runner whose system Python already carries PyYAML. My first venv had behave alone and stopped on "PyYAML required" (kept as `lane__behave_attempt1_noyaml`). With PyYAML added: 14 features, 508 scenarios, 2,330 steps passed, rc 0.
- **Style on every page the merge touched:** check_doc_style.py takes no page list; it judges its own 24 current documents, rc 0. None of the branch's four pages is in that set. So `style_merge_new` applies its `analyze()` to all 33 touched pages at the merge and both parents: 0 findings that neither parent has. A planted 12-word sentence is reported (control).
- `style_blocks_vs_dev` (round 5's changed-block probe, the branch's four pages against 0a75aa77): 0 findings. `style_blocks_vs_r5` (the same probe on the 32 pages dev changed, against d85da329) is rc 1, and every finding it lists is dev's own prose, present on dev too (style_merge_new). It is informational, not a gate.
- Builder leg 0 shows "1 NOT RUN": the `MAKEFLAGS += -e` mutation has no effect on this host's make. The 829-a725c run shows the same line. Leg 1's 16 NOT RUN arms need migen, LiteX or an Arty report, as before. Each leg's rc is 0.
- docs-check's "Require every gate exactly once" reads uploaded hosted receipts; ci-manifest, ci-fail-fast and ci-cancel-tail are CI orchestration. Not run locally; listed with reasons in the table. act was not used: it needs a pushed head, and this lane pushes nothing.
- Large logs (gate_41, behave) are kept as 20,000-byte tails, with sha256 and size in evidence/gates/LARGE_LOGS.txt.
- Diagram generators: only DOC_MAP, timesync_chain and submodule_boundaries take `--check` (gate_10, gate_12, rc 0). In my first pass in the lane, `flash_layout.gen.py --check` took `--check` as an output name and wrote `--check.drawio` and `--check.svg` into the lane root. I deleted those two files, confirmed the tree clean, and made no commit with them. `egress_queue_map.gen.py` and `nxn_window_map.gen.py` stop parsing current RTL ("the RTL shape changed"). No workflow runs either, and the branch changes no RTL, so the failure is the same on dev.

## Open list (as it now stands)

1. #640's body still shows 34.2k, 26.9k and 20.7k (640-a720j). Unchanged.
2. The merge head is local. Pushing it updates PR #835 and clears GitHub's CONFLICTING state. PR #835 is not a draft, so the push starts the hosted exact-head gates (AREA_BUDGET.md and MAILBOX_SPLIT.md are gate-read).
3. Review coverage: R765-5 and R766-5 are POSITIVE at d85da329. The merge brings dev's lines into three branch pages (README:25, AP:61 and :1097-1099, AREA_BUDGET's record lines). Under section 7, Docs and Conformance should be covered again at 72816d26; RTL, Robustness and Tests artifacts of the branch are untouched.
4. Candidate-merge validation (R765-5 / R766-5 next steps): done locally at 72816d26 on dev 0a75aa77 (docs workflow, both builder legs, behave, census, both gate-read readers). rtl-fast's native and firmware banks beyond the service-bounds reader were not run here; they run hosted on the push.
5. The console buffer still rests on S2b's 2.0 ms share; PR #810 is still OPEN (checked 2026-11-08). Unchanged.
6. D21's slot offset and budget wait for the stage 1 lane. Unchanged.
7. The census keeps today's `PSCLK` and PHY reset behaviour; changing either is a new decision. Unchanged.
8. For the stage 1 lane: the probe's AX7101 -3,758 LUT figure includes the failing route (R766-1-S3). Unchanged.
9. Not taken, optional: R765-3-S1; R765-2-S1 / R766-2-S1, R766-2-S2, R766-2-S3, R765-2-S4. Unchanged.
10. Observation, unchanged: the switch-over's Block RAM ledger (AP:1297-1305 at d85da329) credits no removal for the 8 processor crossing RAMB36; for the switch-over lane.
11. Observation for the manager, not this lane: `docs/diagrams/egress_queue_map.gen.py` and `nxn_window_map.gen.py` cannot parse current RTL at dev 0a75aa77. A new issue may be wanted; this lane may post only on #640.
12. Maintainer authorization to merge, post-merge containment, and #640's close and move to Done remain, as R766-5 lists.

## Evidence (./evidence)

| File | What |
|---|---|
| taken.md, taken_url.txt | TAKEN as posted, and its URL |
| review_ready.md, review_ready_url.txt | REVIEW READY as posted, and its URL |
| merge_vs_dev.diff | `git diff 0a75aa77 HEAD` (the branch's four pages) |
| merge_vs_r5_branch_pages.diff | `git diff d85da329 HEAD` on the four branch pages (what dev brought into them) |
| gate_table.py, gate_table.md | The table above, built from the verifier's rows and each log |
| make_pr_body.py | Builds PR-BODY.md from round 5's |
| tools/ | The runner, verifier and skip list as run; run_all.sh, run_extra.sh; style_touched.py, merge_style_probe.py, service_bounds_arm.py, body_style_snippet.py |
| gates/ | verify.md and verify.rc, run_all.out, start and end times, every step's log and rc, LARGE_LOGS.txt |
| SHA256SUMS | Digests of every file above |

## Not done / not allowed

No push, PR creation or edit, rebase, amend, sub-agent, bench, flashing or Vivado. One merge only, the ordered merge of origin/dev. No existing comment edited. On #640, only TAKEN and REVIEW READY posted.
