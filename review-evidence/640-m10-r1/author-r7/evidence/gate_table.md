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
