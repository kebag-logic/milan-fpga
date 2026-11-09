# HANDOFF - [A720q] issue #640, PR #835 round 7 (sync with dev ac0a01e3, docs only)

Status: REVIEW READY (2026-11-09). Head e70ae2cb2dd0746060612493cb6724522b8701bc, one merge of dev ac0a01e3 on round 6's 72816d26. Every docs.yml step that can run locally is rc 0 on a clean clone (65 steps; 31 hosted-only steps not run, each with its reason; verifier rc 0). Every lane step is rc 0. Local only, nothing pushed.

- Lane: $LANES/640-mark2-charter, branch 640-charter-followup. Started at 72816d26a7e2a29db5bc198ff65056ee4c5790b4, round 6's head. Both round 6 reviews are POSITIVE there: R765-6 (PR #835 issuecomment-6719846258) and R766-6 (issuecomment-6719945800).
- Remote checked: https://github.com/kebag-logic/milan-fpga.git
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6731392443 (text: evidence/taken.md)
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6732066141 (text: evidence/review_ready.md)
- New head: e70ae2cb2dd0746060612493cb6724522b8701bc. One merge commit, "Merge dev ac0a01e3 into the #640 charter follow-up (#640)". Parents 72816d26 and origin/dev ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36. `git merge-base HEAD origin/dev` is ac0a01e3. Nothing pushed.
- How: `git fetch origin`, then `git merge --no-ff origin/dev`. No rebase, force or amend. No hooks configured.
- Dev since 0a75aa77: 1 first-parent merge (PR #852, issue #851, merged 2026-11-09T03:11:39Z), 11 commits, 20 files (796+, 248-).
- Head against dev: only the branch's four pages differ, 231+ / 53-. `diff` of the `-U0` +/- line sets against round 6's (0a75aa77..72816d26 vs ac0a01e3..HEAD) is empty. No RTL, firmware, generator, gate or configuration change.

## PRs dev brought (0a75aa77..ac0a01e3)

| Merge | PR | Issue | Subject |
|---|---|---|---|
| ac0a01e3 | #852 | #851 | Adopt the processor pin that sends one vector per value: processor gitlink 92100657 to 044cb25f, the fifteenth area record (route-1x1, ooc-1x1, ooc-8x8), AREA_BUDGET, the #234 page, SUBMODULES, INTEGRATION_GUIDE, CHANGELOG, milan_dp crflic leg |

## Conflicts and resolutions

Files both sides changed since 0a75aa77: docs/findings/README.md, docs/design/AREA_BUDGET.md, docs/design/MARK_II_AREA_PLAN.md.

| File | Git result | Resolution |
|---|---|---|
| docs/findings/README.md:25-26 | CONFLICT, two adjacent table rows | Dev changed the 234 row ("The gate's current record is #851's re-baseline of 2026-11-08, the first image with all four lab fixes"). The branch changed the 649 row ("a tenth of the gap to NFR-RES-01's former 60 % target"). Kept dev's 234 row and the branch's 649 row, each verbatim, by a scripted splice (evidence/splice_readme.py) that asserts each side changed exactly one row against 0a75aa77. `git diff origin/dev HEAD` on the file shows only the 649 row; `git diff 72816d26 HEAD` only the 234 row. |
| docs/design/AREA_BUDGET.md | auto-merged | Dev's lines: :13 (#851 image), :126-134 (#851 record paragraph), the record table :149-155 (53,428 LUT, 54,837 FF, 15,829 slices, 21 free, +0.210 / +0.036 ns), :216-241 (#851 paragraph and directive table), :253-257 (allocation 25,199 / 44,831 / 25,184), :663-667 (fifteenth record). Branch's lines: :140-141 (target sentences) and :260-262 (acceptance bar). Separate lines; merged sections read coherent. |
| docs/design/MARK_II_AREA_PLAN.md | auto-merged | Dev changed :61 (+0.242 to +0.210 ns warning row) and :1099-1100 (#843 line now past tense, new #851 anchor line: 53,428 LUTs, 15,829 slices, 74/27). Neither is near a branch hunk. |

## Figures checked against dev (task 1)

Corrected figures: **none**.

- Method: every `+` line of `git diff -U0 origin/dev HEAD -- docs` (231 lines, scratch `branch_added.txt`) grepped for resource figures and for every value #851 superseded: 53,221, 15,834, 16 free / 16 slices, +0.242, +0.012, 54,754, 83.94, 24,996, 44,631, 24,937, 39.4 %, 70.4 %, "fourteenth", #843 / #845 / #851, 92100657 / 044cb25f, record, anchor, WNS. No hit in a branch line (one false hit: "Event record" in MAILBOX_SPLIT).
- The branch's figures are 5,119, 3,249, 1,150, 27,224, 30,974, 34,223, 3,948, 47 and 18 RAMB36 (the 2026-10-31 basis build, 52,008 LUTs), 35.0 tiles (SPLIT_CONTROL_MEMORY.md, unchanged by dev), 20,000 and 60 % (NFR-RES-01, unchanged), 3,828 (the #649 page, unchanged). Dev's #851 changed none of their sources.
- The superseded #843 figures still on the merged pages (AREA_BUDGET :188, :198-210, :237; AP :1099) are dev's own history lines, current at ac0a01e3.
- Other reference pages the PR body lists: since 503bc97c dev changed only AREA_BUDGET.md, MARK_II_AREA_PLAN.md and sw/litex/milan_soc.py (the last before 0a75aa77). PR #810 still OPEN (checked 2026-11-09).

## Generated pages (task 2)

No generator output changes, so there is no regeneration commit. In the lane at the merge, before the gate run:

| Generator | Result |
|---|---|
| `scripts/docs_inventory.py --check` | documentation inventory: OK (547 lines, docs/DOCUMENTATION_AUDIT.md is fresh) |
| `scripts/gen_toc.py --check` | TOC gate: OK (152 page(s) ...) |
| `docs/traceability/gen_module_matrix.py --check` | traceability matrix up to date (80 modules ...) |
| `docs/DOC_MAP.gen.py --check` | documentation map: OK (4 roles, 24 valid paths, decoded PNG) |
| `docs/diagrams/timesync_chain.gen.py --check`, `submodule_boundaries.gen.py --check` | rc 0 |

Dev's own generated files (DOCUMENTATION_AUDIT.md, submodule_boundaries.*, PNG_MANIFEST.json, rom_digests.tsv, pp_resource_baseline.json) came in through the merge unchanged; the branch feeds none of them except the audit page, which is fresh.

## Gate table (task 4)

Every `run:` step of `.github/workflows/docs.yml` at the head, job by job, sequentially. Each job ran on its own fresh `--shared` clone of the lane at e70ae2cb, made by the 829-a725c runner (`run_docs_yml.py`, copied with this lane's LANE, VENV and HOME; evidence/tools/). docs.yml and the skip list are unchanged since round 6 (dev ac0a01e3 changes no workflow). Rows come from the 829-a725c verifier (`verify_docs_yml.py`): "65 steps ran, 31 not run with a reason, 0 bad", rc 0. Run 2026-11-09T04:19:33+01:00 to 05:12:18+01:00 (53 minutes).

Environment: venv and venv-behave (behave + PyYAML) copied from 640-a720p, shebangs repointed; scratch HOME copied from 640-a720p with its SDK removed, so ci_step_28 installed the pinned RV32 SDK fresh. Submodules came from their .gitmodules URLs through the workflow's own fetch steps (protocol-processor at dev's new pin 044cb25f). Every job's `tree-after` status is empty.

| Job | Step | Name | rc | Last line |
|---|---|---|---:|---|
| wire-accountability | ci_step_1 | Set CPU-derived job budgets | 0 | # clone $VALIDATION_STORAGE/640-a720q/gates/wire-accountability/wt |
| wire-accountability | ci_step_3 | Fetch the engine authority the builder derives from | 0 | Submodule path 'gptp-processor': checked out '1616fc8f062fbf58c35ad31674b5b233207bbdb8' |
| wire-accountability | ci_step_4 | Advertised-vs-emitted gate (green since 2026-07-28, item 00) | 0 | RESULT: PASS |
| wire-accountability | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs-check-no-git | ci_step_1 | Retain checkout identity before removing metadata | 0 | # clone $VALIDATION_STORAGE/640-a720q/gates/docs-check-no-git/wt |
| docs-check-no-git | ci_step_2 | Set CPU-derived job budgets | 0 | # clone $VALIDATION_STORAGE/640-a720q/gates/docs-check-no-git/wt |
| docs-check-no-git | ci_step_3 | Strip git metadata, then run the docs gate | 0 | feature_status: 0 finding(s) |
| docs-check-no-git | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs-gates-0 | ci_step_1 | Set CPU-derived job budgets | 0 | # clone $VALIDATION_STORAGE/640-a720q/gates/docs-gates-0/wt |
| docs-gates-0 | gate_1 | Build the validated HDL reference | 0 | Wrote: $VALIDATION_STORAGE/640-a720q/gates/docs-gates-0/runner_temp/milan-hdl-reference/index.html |
| docs-gates-0 | ci_step_5 | Install the python gate dependencies | 0 | [notice] To update, run: pip install --upgrade pip |
| docs-gates-0 | ci_step_7 | Install the pinned Markdown renderer | 0 | [notice] To update, run: pip install --upgrade pip |
| docs-gates-0 | ci_packages_6 | Resolve exact package downloads 6 | NOT RUN | apt package index for librsvg2-bin; this host has rsvg-convert installed and no apt |
| docs-gates-0 | ci_step_10 | Install diagram gate dependencies | NOT RUN | sudo apt-get for librsvg2-bin; rsvg-convert is installed here and the venv carries wavedrom==2.0.3.post3 |
| docs-gates-0 | gate_7 | Link health, wording, dead-reference and local-info gate | 0 | docs_check: 0 finding(s) across 214 md files + 1448 scrubbed text files, scrub self-test 23/23, routing arms 4/4 [git ls-files] |
| docs-gates-0 | gate_8 | Added-line em-dash gate | 0 | check_em_dash: 0 finding(s) over 231 added line(s) in 4 changed Markdown page(s), 0 mirrored label(s) exempt, arms 339/339 [ac0a01e3..HEAD] |
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
| docs-gates-1 | ci_step_1 | Set CPU-derived job budgets | 0 | # clone $VALIDATION_STORAGE/640-a720q/gates/docs-gates-1/wt |
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
| docs-gates-2 | ci_step_1 | Set CPU-derived job budgets | 0 | # clone $VALIDATION_STORAGE/640-a720q/gates/docs-gates-2/wt |
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
| style_merge_new | check_doc_style's `analyze()` on all 11 pages the merge touched, at the merge and both parents: findings neither parent has | 0 | merge style probe: 11 page(s), 0 new finding(s) [72816d26 + ac0a01e3 -> e70ae2cb] |
| style_merge_new_control | the same with a planted 12-word sentence; must report it (negated) | 0 | merge style probe: 11 page(s), 1 new finding(s) [72816d26 + ac0a01e3 -> e70ae2cb] |
| style_blocks_vs_dev | changed-block probe, the branch's 4 pages against dev ac0a01e3 | 0 | docs/findings/README.md: 0 finding(s) in changed blocks |
| behave | `cd tests && behave --no-capture -f plain` (behave + PyYAML) | 0 | Took 0min 2.500s |
| diffcheck_mergebase | `git diff --check ac0a01e3 HEAD` (merge base) | 0 | # head e70ae2cb2dd0746060612493cb6724522b8701bc lane step diffcheck_mergebase: git diff --check ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36 HEAD |
| diffcheck_oldbase | `git diff --check 0a75aa77 HEAD` (round 6 base) | 0 | # head e70ae2cb2dd0746060612493cb6724522b8701bc lane step diffcheck_oldbase: git diff --check 0a75aa774b89ac89351700f63dd8cbb89694af6c HEAD |
| em_dash_mergebase | `check_em_dash.py --base ac0a01e3` | 0 | check_em_dash: 0 finding(s) over 231 added line(s) in 4 changed Markdown page(s), 0 mirrored label(s) exempt, arms 339/339 [ac0a01e3..HEAD] |
| reader_check_baseline | AREA_BUDGET.md's reader: `pp_resource_gate.py check-baseline` | 0 | baseline PASS: 3 endpoints |
| reader_service_bounds | MAILBOX_SPLIT.md's reader: `ctrl_service_bounds.arm_service_bounds` | 0 | rc 0 |
| census_coverage | `census_coverage.py` at the merge, against dev's `sw/litex/milan_soc.py` | 0 | RESULT: PASS |
| census_coverage_control | `! census_coverage.py` against the round 1 page 3f8ed303 (must fail) | 0 | RESULT: FAIL |

Notes:
- **Lane steps** ran on a separate fresh clone of the head (scratch `gates/extra/wt`), submodules from docs-gates-0's clone, origins reset to their .gitmodules URLs (logs/extra__submodules.txt). Its `git status --porcelain` was empty after every step (logs/lane__tree-after.txt).
- **Style on every page the merge touched:** check_doc_style.py takes no page list; it judges its own 24 current documents, rc 0. `style_merge_new` applies its `analyze()` to all 11 Markdown pages the merge touched (evidence/touched_pages.txt) at the merge and both parents: 0 findings neither parent has. A planted 12-word sentence is reported (control). `style_blocks_vs_dev`: 0 findings in the changed blocks of each of the branch's four pages against ac0a01e3.
- Round 6's informational `style_blocks_vs_r5` probe is dropped; `style_merge_new` covers dev's pages. behave ran once, with PyYAML: 14 features, 508 scenarios, 2,330 steps passed.
- Builder leg 0 shows "1 NOT RUN" (the `MAKEFLAGS += -e` mutation has no effect on this host's make), leg 1 "16 NOT RUN" (migen, LiteX or an Arty report), as in round 6. Each leg's rc is 0.
- docs-check's "Require every gate exactly once", ci-manifest, ci-fail-fast and ci-cancel-tail are hosted orchestration; not run locally, listed with reasons. act was not used: it needs a pushed head, and this lane pushes nothing.
- Large logs (gate_41, behave) are kept as 20,000-byte tails, with sha256 and size in evidence/gates/LARGE_LOGS.txt.
- One slip, no effect: my first lane-side DOC_MAP check used a wrong path (`docs/diagrams/DOC_MAP.gen.py`, rc 2, file not found). The generator is `docs/DOC_MAP.gen.py`; rerun rc 0, and gate_10 runs it too.

## Round 6 review residues

- R765-6-R1 / R766-6-RESIDUE-1 (RESIDUE, Docs, PR body wording): taken in PR-BODY.md. The "Authoritative references" bullet now reads "at `ac0a01e3`, the merge base; since `503bc97c` only `AREA_BUDGET.md` and `MARK_II_AREA_PLAN.md` changed, by dev's #845, #843 and #851 records". Checked: `git diff --stat 503bc97c ac0a01e3` on every listed page names only those two (plus sw/litex/milan_soc.py, before 0a75aa77).
- R765-6-S1 / R766-6-S1 (SUGGESTION, evidence hash chain): evidence/SHA256SUMS is computed last, over the final bytes. It covers PR-BODY.md (not a published evidence file) and not HANDOFF.md, which gets the REVIEW READY URL afterwards. Redaction for publication is the publisher's step.
- R765-6-S2 (dev's AP:73 "52,008" sentence) and R765-6-S3 (start estimate basis): not taken, out of scope for a sync; listed below.

## Open list (as it now stands)

1. #640's body still shows 34.2k, 26.9k and 20.7k (640-a720j). Unchanged.
2. The merge head e70ae2cb is local. Pushing it updates PR #835. PR #835 is not a draft, so the push starts the hosted exact-head gates (AREA_BUDGET.md and MAILBOX_SPLIT.md are gate-read). R766-6 notes every hosted context at 72816d26 was cancelled (infrastructure 504s), so an executed exact-head rtl-fast and docs verdict, or the act replica, is still needed before merge.
3. Review coverage: R765-6 and R766-6 are POSITIVE at 72816d26. The merge brings dev's lines into three branch pages (README:25, AP:61 and :1099-1100, AREA_BUDGET's #851 lines). Under section 7, Docs and Conformance should be covered again at e70ae2cb; the branch's own lines are byte-identical to round 6.
4. Candidate-merge validation: done locally at e70ae2cb on dev ac0a01e3 (docs workflow, both builder legs, behave, census, both gate-read readers). rtl-fast's native and firmware banks beyond the service-bounds reader were not run here.
5. The console buffer still rests on S2b's 2.0 ms share; PR #810 is still OPEN (checked 2026-11-09). Unchanged.
6. D21's slot offset and budget wait for the stage 1 lane. Unchanged.
7. The census keeps today's `PSCLK` and PHY reset behaviour; changing either is a new decision. Unchanged.
8. For the stage 1 lane: the probe's AX7101 -3,758 LUT figure includes the failing route (R766-1-S3). Unchanged.
9. Not taken, optional: R765-3-S1; R765-2-S1 / R766-2-S1, R766-2-S2, R766-2-S3, R765-2-S4; R765-6-S2 (dev's AP:73 present-tense 52,008 sentence, a later docs lane); R765-6-S3 (the switch-over lane re-derives the start estimate; dev's gate record is now 53,428, 1,416 LUTs above the 52,012 of #799).
10. Observation, unchanged: the switch-over's Block RAM ledger credits no removal for the 8 processor crossing RAMB36; for the switch-over lane.
11. Observation for the manager, unchanged: `docs/diagrams/egress_queue_map.gen.py` and `nxn_window_map.gen.py` could not parse current RTL at dev 0a75aa77 (not re-run this round). A new issue may be wanted; this lane may post only on #640.
12. Maintainer authorization to merge, post-merge containment, and #640's close and move to Done remain.

## Evidence (./evidence)

| File | What |
|---|---|
| taken.md, taken_url.txt | TAKEN as posted, and its URL |
| review_ready.md, review_ready_url.txt | REVIEW READY as posted, and its URL |
| merge_vs_dev.diff | `git diff ac0a01e3 HEAD` (the branch's four pages) |
| merge_vs_r6_branch_pages.diff | `git diff 72816d26 HEAD` on the four branch pages (what dev brought into them) |
| touched_pages.txt | the 11 Markdown pages the merge touched |
| gate_table.md | the table above, built by tools/gate_table.py from the verifier's rows and each log |
| make_pr_body.py | builds PR-BODY.md from round 6's |
| tools/ | runner, verifier and skip list as run; run_all.sh, run_extra.sh; splice_readme.py (the conflict splice); style_touched.py, merge_style_probe.py, service_bounds_arm.py, gate_table.py |
| gates/ | verify.md and verify.rc, run_all.out, start and end times, every step's log and rc, LARGE_LOGS.txt |
| SHA256SUMS | digests of every file above and PR-BODY.md, computed last |

## Not done / not allowed

No push, PR creation or edit, rebase, amend, sub-agent, bench, flashing or Vivado. One merge only, the ordered merge of origin/dev. No existing comment edited. On #640, only TAKEN and REVIEW READY posted. No repo file changed beyond the merge and its conflict resolution.
