[R935] POSITIVE - exact head 17f44fe0df361d02a8d6ea4081b99c6942bdc4a7

# R935-6: composition review of the merge-train candidate for kebag-logic/milan-fpga PR #1015 (Relates to #970)

- **Head under review:** `17f44fe0df361d02a8d6ea4081b99c6942bdc4a7`, tree `2dc4b2ceb4b3eaae77f3b9e38e9d102e92acabed`. It is a merge commit with two parents:
  - `04a20c74d` (the p1win train candidate);
  - `35d29eb71` (the PR source head).
- **Train shape:** `dev-soft-core` `4df125b8` -> cicd4 (`8156dc7ae`, merging `6841c5e3b`) -> p1win (`04a20c74d`, merging `079c4fa15`, the `1009-bind-window` branch) -> this PR (`35d29eb71`). The PR's base is `dev-soft-core`, and its merge base with the train is `4df125b8`.
- **Previously reviewed head (this role):** `35d29eb71`, R935-5, POSITIVE. The source reviews named for lenses this composition does not change are R935-5 at `35d29eb71` and R936-3 at `701a980b`. R936-3 is the external one, and its delta to `35d29eb71` is two commits (`57f32b28`, `35d29eb71`), which R935-4 and R935-5 covered.
- **Verdict:** POSITIVE. The composed tree adds no defect beyond the reviewed sources.
  - The candidate tree is the clean three-way merge of its two parents.
  - Every hunk this PR brings into the candidate is byte-identical to the PR's diff on its own base.
  - The five files both sides change carry disjoint hunks.
  - Every shared registry, inventory, document table and gate I could identify passes on the composed tree.
- **Findings:** no BLOCKER, MAJOR or MINOR. Four RESIDUE items are retained from the source rounds and none is new. One new SUGGESTION (S6) is added and the earlier ones are carried.
- This verdict does not authorize a merge and does not close #970.

## 1. Reconstruction (public state only)

- **Contract:** I read `AGENTS.md` sections 3 and 6 to 8 and `CONTRIBUTING.md`'s review bar. Their rules: the five lenses; evidence for every clean lens; coverage banked per head; a finding moved to another Issue is not resolved; no agent merge without maintainer authorization. The owner rules in the brief also apply: RESIDUE, the comment rule and the token economy.
- **#970 frozen acceptance:** the issue body sets six requirements:
  - the first ENTITY_AVAILABLE within the declared discovery time, with Milan's 0 to 4 s and 0 to 2 s draws, uniform per IEEE 1722.1-2021 6.2.4.2.2;
  - those draws at 1x1/1if and 8x8/1if, with and without a grandmaster change;
  - the 6.0 s derived in FR_NFR;
  - the grandmaster change still announced;
  - a host test of both orders with a planted defect;
  - the bench re-run.
- **#970 rulings:** I read the public rulings of 2026-11-22 (no narrowing of the draw), 2026-11-25 (no link hold; the 6.0 s stands; a seeded draw) and 2026-11-26 (the lost first frames were the test path's).
- **PR #1015:** base `dev-soft-core`, head `35d29eb71`. The live body was last updated 2026-11-27T05:35:19Z.
- **Public executable evidence:**
  - Packet `review-evidence/adp970-r1` at `40ce56ee`: all 14 files re-hashed and all 14 match the manifest's `published_sha256` (`receipts/evidence_packet_verify.txt`). GitHub reports that commit as unsigned, so I relied on its hashes, not a signature. Its receipts cover `0ad0e518`, so I used them as history only.
  - Hosted checks at the source head `35d29eb71`: 99 runs, of which 98 succeeded and one, `Physical gPTP (nightly and manual)`, was skipped (`receipts/hosted_source_head_checks.tsv`). They include `firmware-boundary`, the four `firmware-control-mutants` legs, both `firmware-unit` legs and the five `docs-gates`.
  - Candidate `17f44fe0`: it is not on GitHub (the API answers "No commit found"), so it has no hosted run of its own.
  - Manager receipts: no manager evidence comment for this candidate is on the issue or the PR yet. No manager source bank is claimed or inferred.
- **Order kept:** I made my own pass over the composition and its gates (sections 2 and 3) before reading the prior public findings. The prior reports read afterwards were R935-5 and R936-3.

## 2. Composition analysis

### 2.1 Textual composition

`scripts/composition.sh` and `receipts/composition.txt` establish four facts:
- `git merge-tree --write-tree 04a20c74d 35d29eb71` gives `2dc4b2ce...`, which is the candidate's tree. So the merge is clean, with no conflict and no hand edit.
- The PR changes 27 paths against `4df125b8`, and the two predecessors change 46.
- For all 27 PR paths, the stable patch-id of `4df125b8..35d29eb71` equals that of `04a20c74d..17f44fe0`, file by file.
- The candidate's delta on its train parent touches no path outside those 27.

### 2.2 Files changed by both sides

| File | Predecessor change | This PR's change | Interaction |
|---|---|---|---|
| `sw/firmware/ctrl/test/ctrl_configs.py` | cicd4: `OUTSIDE` entry `scripts/ci_fast_legs_selftest.py` (line 171) | `OUTSIDE` entry `tb/verilator/ctrl_service_budget/model_counts.py` (line 315) | Same registry, separate keys. The static half of `ctrl_configs.held()` passes on the composed tree: 93 builders found by text, no unlisted program, no stale key (`receipts/registry_probe.txt`). |
| `tb/verilator/ctrl_service_budget/run.py` | p1win: `bind_save` wiring in `run_group`, `burst_misses`, `print_bursts` and `table` | `--self-test` runs `model_counts.main()` before `selftest.main([])` (line 902) | Same self-test entry. The composed self-test passes with p1win's bind checks and mutants (section 3). |
| `tb/verilator/ctrl_service_budget/README.md` | p1win: the bind section and a line on the SET_NAME save | One bullet on `model_counts.py` in "Controls and self-test" (line 1347) | Disjoint sections. The bullet's "build-free group sets" claim still holds: p1win's `bind_save.groups` are reached only through `save_window.groups(p, build)`, which `model_counts.py`'s docstring already names as build-dependent. None of their probes publishes an ADP `accesses` count. |
| `docs/design/SPLIT_CONTROL_MEMORY.md` | p1win: line 166, the binding window's `rom` (+72 B at 1x1, +64 B at 8x8, measured against `c34e7d8b`), and two sentences elsewhere | Line 756, the seeded draw's `rom` (+264/+272/+264/+256 B, measured against `c34e7d8b`) | Both are measurements scoped to `c34e7d8b`, so neither falsifies the other. The composed sum is in 2.3. |
| `docs/DOCUMENTATION_AUDIT.md` | p1win: the `ctrl_nvm/README.md` row | The `tb/verilator/mbx/README.md` row | Different rows. `docs_inventory.py --check` gives fresh (541 lines). |

### 2.3 Semantic interactions beyond shared files

| Interaction | Finding | Evidence |
|---|---|---|
| The firmware-builder text cross-check (cicd4 adds `ci_fast_legs.py`, `ci_fast_legs_selftest.py` and `census_legs.py`; p1win adds `bind_save.py`, `selftest_bind.py` and `selftest_mutants_bind.py`; the PR adds `model_counts.py`) | Every program that names the firmware tree is listed. The five non-program builders are pre-existing files, and none is added by any side. | `receipts/registry_probe.txt` |
| The cicd4 shard dispatch of the control mutant table, which now includes the PR's 26 `adp_first_mutants` | "2026 live invocations in exactly one shard". The planted duplicate is refused, and the nine invalid combinations are refused. | `receipts/fw_shards.log` |
| The cicd4 fast-leg contract and workflow/event pins | `ci_events.py --check` passes: 2,409 contract items across 4 workflows and `CI_WORKFLOWS.md`. Its `--selftest` passes 6,174 arms. `ci_fast_legs_selftest.py`, `ci_gate_workflows.py --check` and its self-test all pass. | `receipts/ci_events_*.log`, `fast_legs_selftest.log`, `docsgates/gate_workflows_*.log` |
| p1win's store change (`nvm_store.c`, the binding window) linked under the PR's platform-boot tests (B25 to B27 link `ctrl_plat` with the store) | The ADP slice gives 84 checks and 0 failures (H9 and H10 included). `plat` passes. `platboot` passes at if1 (59 checks) and at if2 (60 checks), with B25 and B27 compiled into both binaries. `acmpnvm` passes (7). | `receipts/focused_arms.log` |
| The PR's planted defects on the composed tree (`adp_first_mutants`, 26 mutants, through `ctrl_mutants.campaign`'s own runner and arms) | 26 of 26 are caught by name, in 4 legs (7 + 7 + 6 + 6), and none escapes. | `receipts/adp_mutants_leg{0..3}.log` |
| The CPU budget harness self-test, now holding the PR's `model_counts` together with p1win's bind graders and mutants | `model_counts` rc 0; 1,048 checks, all PASS; 321 mutants, all caught (12 of them bind mutants); "self-test: 0 failures". | `receipts/budget_selftest_parallel.log` |
| The `rom` ledger: both sides add to the same images | The composed sum stays inside each platform point's current granule, so no tile moves at those points. The size fixture's one-interface answering-ports arm has only 144 B of granule margin after p1win. That is not measured here (S6, section 5). | Arithmetic below; `plat_ledger.py` could not run (section 8) |
| The stack gitlink `c3bff8f3`, which only the PR moves | `check_submodule_docs.py` passes (6 exact gitlinks), and so do the submodule diagram's `--check` and `--selftest`. `ci/image` holds the stack's path, not a pin. | `receipts/check_submodule_docs.log`, `docsgates/submodule_boundaries_*.log` |
| The `ci/image/tool-inventory.json` file pins, two of which name `ctrl_configs.py` and `ctrl_mutants.py` | These are not a composition defect. 163 of 376 pins were already stale at the base `4df125b8`, and the two pins match no train commit's blob. The file is an image-build snapshot, not a per-commit gate. | Recorded in this report (a direct hash comparison) |

The `rom` arithmetic uses the composed sum of both `c34e7d8b`-scoped measurements, with granules of 2,048 B (`sw/litex/ctrl_memory.py:52`) and tiles counted as the sum of the granule banks (`ctrl_memory.py:205`):

| Point | Base `c34e7d8b` | + binding window (p1win) | + seeded draw (PR) | Composed sum | Granule ceiling | Margin |
|---|---:|---:|---:|---:|---:|---:|
| 1x1, one interface | 127,568 | +72 | +264 | 127,904 | 129,024 | 1,120 B |
| 1x1, two interfaces | 129,352 | +72 | +272 | 129,696 | 131,072 | 1,376 B |
| 8x8, one interface | 141,680 | +64 | +264 | 142,008 | 143,360 | 1,352 B |
| 8x8, two interfaces | 143,432 | +64 | +256 | 143,752 | 145,408 | 1,656 B |

The base already sits in the same granule at each point, so the sum moves no platform tile.

## 3. Gates run on this candidate

All were run from the candidate checkout. Markdown gates used the hash-pinned renderer (`tools/markdown/requirements.txt`) in a private environment outside the checkout (`receipts/renderer_identity.txt`).

| Gate | Result | Receipt |
|---|---|---|
| `docs_check.py` | 0 findings across 226 md and 1,967 text files | `docs_check.log`, `docs_check_v.log` |
| `gen_toc.py --selftest` / `--verify-anchors` / `--check` | 1,501 of 1,501 arms / 759 fragment links reproduced / OK, 161 pages | `toc_*.log` |
| `check_em_dash.py --base 04a20c74d` (the candidate's train parent) | 0 findings over 45 added lines in 9 pages | `em_dash.log` |
| `check_em_dash.py --base 4df125b8` (the whole train) | 0 findings over 198 added lines in 14 pages | `em_dash_dev.log` |
| `ci_events.py --check` / `--selftest` | OK, 2,409 items / PASS, 6,174 arms | `ci_events_*.log` |
| `check_py_idiom.py`, `check_cpp_idiom.py`, `check_sh_idiom.py` | All within their ratchets | `py_idiom.log`, `cpp_idiom.log`, `docsgates/sh_idiom.log` |
| `check_diagram_pngs.py` | OK, 6 rasters | `diagram_pngs.log` |
| `check_doc_style.py`, `check_submodule_docs.py` | OK | `check_doc_style.log`, `check_submodule_docs.log` |
| `DOC_MAP.gen.py --check`, `docs_inventory.py --check`, `check_doc_paths.py`, `memory_map.gen.py --check`, `gen_module_matrix.py --check`, `check_hygiene.py --check`, `check_todo_ownership.py`, `measure_naming.py --check`, `measure_test_evidence.py --check`, `measure_fail_fast.py --check`, `check_feature_status.py`, `check_baremetal_only.py --check`, `check_port_contracts.py`, `check_gptp_docs.py`, `check_solution_docs.py`, `generate_ci_evidence_pins.py --check`, `ci_gate_workflows.py --check` and its self-test, `submodule_boundaries.gen.py --check` / `--selftest` | All rc 0 | `docsgates/*.log` |
| `test_ctrl_firmware_shards.py`, `ci_fast_legs_selftest.py` | PASS | `fw_shards.log`, `fast_legs_selftest.log` |
| `model_counts.py` | 0 stale counts; each path planted one short is found at every instance (1 interface 6/2/1/2/5/1/2, 2 interfaces 11/3/2/3/10/2/3) | `model_counts.log` |
| CPU budget self-test (`run.py --self-test`'s work, parallel) | 0 failures, 1,048 checks, 321 of 321 mutants caught | `budget_selftest_parallel.log` |
| Firmware suites ADP, plat, platboot if1/if2, acmpnvm | PASS | `focused_arms.log` |
| `adp_first_mutants` campaign | 26 of 26 caught | `adp_mutants_leg*.log` |
| Static half of the firmware-boundary cross-check | CLEAN | `registry_probe.txt` |

Two harness notes:
- **Budget self-test driver.** `scripts/budget_selftest_parallel.py` runs the same work as `run.py --self-test`, which is `model_counts.main()`, then `selftest.checks()` unmutated, then every `selftest_mutants.MUTANTS` entry under `selftest.mutated()`. It applies the same verdict rule, with the same exception set counted as a refusal. It forks one process per mutant, where `selftest.main` uses one process. A serial run was stopped at the session's per-call limit before it finished and is not counted as evidence.
- **Focused suites.** Two attempts at the full default firmware suite (`test_ctrl_firmware.py --require-rv32 --jobs 4`) hit the same limit (rc 124, no verdict) and are not counted. `scripts/focused_arms.py` runs the suites the composition reaches, through the driver's own `Tree`, arms and report.

## 4. Prior findings, resolved or retained

| Prior ID | Disposition at this head | Evidence |
|---|---|---|
| R935-1 F1 to F4, R935-1 R1, R936-1-F1, R936-2-F1, R936-2-R1/R2, R935-3 F1, R935-3 RES-A, R935-3 S1 | Remain **RESOLVED** | The composition carries the PR's hunks unchanged (2.1). The suites and mutants that closed them pass on the composed tree (section 3). |
| R935-3 RES-B / R935-4 RES-B, RESIDUE (the PR body does not state the harness's 12 or the count check) | **RETAINED** | The live body's `sw/firmware/ctrl/adp/` bullet still reads only "its LINK_UP row stays at 11", and the body does not name `model_counts.py`. |
| R935-4 RES-C, RESIDUE (the body's "Status" list stops at `f4833e16`) | **RETAINED** | The list still has five items. |
| R935-2 RES2 / R935-4 RES-D, RESIDUE (`SPLIT_CONTROL_MEMORY.md`, "this change's own base `c34e7d8b`") | **RETAINED** | Now at line 756 of the composed tree. |
| R935-2 RES4 / R935-4 RES-E, RESIDUE (the body's CPU-leg base is described inexactly) | **RETAINED** | The two "CPU budget legs against the base" rows are unchanged. |
| R935-5 S5, R935-3 S2, R935-3 S3 / R936-2-S1, R935-2 S1 to S3, R935-1-S4, R935-4 S4, all SUGGESTION | Carried, optional | Unchanged at this head. |

## 5. Findings at this head

No BLOCKER, MAJOR or MINOR.

### RES-B (retained) - RESIDUE - Docs - live PR body, the `sw/firmware/ctrl/adp/` and "Harness waits" bullets
- **Evidence:** The body states 12 accesses where no clock is wired, and 11 for the platform. It does not say that the budget harness publishes 12, and it does not mention `model_counts.py`.
- **Impact:** PR text only.
- **Exact fix:** append to "Harness waits": "The budget harness's image wires no clock, so it publishes LINK_UP's model count as 12 (the platform's LINK_UP is 11). `model_counts.py`, run first by `run.py --self-test`, holds the published counts of all seven ADP paths to `adp_mbx.h` and must find each path planted one short at every instance."

### RES-C (retained) - RESIDUE - Docs - live PR body, the "Status" list
- **Evidence:** "Since the reviewed head `0ad0e518`" lists five items, ending at the `c3bff8f3` pin.
- **Exact fix:** add three items:
  - "6. `701a980b`: the budget harness publishes LINK_UP's model count as 12 (no clock wired), and `model_counts.py` holds the published ADP counts to `adp_mbx.h`."
  - "7. `57f32b28`: that check holds all seven ADP paths, LINK_DOWN and SHUTDOWN included, at every instance."
  - "8. `35d29eb7`: `ctrl_configs.OUTSIDE` lists `model_counts.py`, which reads `adp_mbx.h` as text and compiles nothing."

### RES-D (retained) - RESIDUE - Docs - `docs/design/SPLIT_CONTROL_MEMORY.md:756`
- **Evidence:** "against this change's own base `c34e7d8b`". The PR sits on `4df125b8`. In the composed tree, the binding window's line 166 cites the same base as "`dev-soft-core` `c34e7d8b`'s".
- **Exact fix:** "against `dev-soft-core` `c34e7d8b` (127,568 / 129,352 / 141,680 / 143,432 B of `rom`)". This matches line 166's wording and drops "this change's own base".

### RES-E (retained) - RESIDUE - Docs - live PR body, the two "CPU budget legs against the base" rows
- **Exact fix (as R935-2):** name the base commit the legs were paired against, in both rows.

### Suggestions (optional, no lens effect)

- **New S6 (RTL, Docs): state the composed `rom` at the merge turn.**
  - Each `SPLIT_CONTROL_MEMORY.md` figure is scoped to `c34e7d8b`: line 166 for the binding window and line 756 for the seeded draw. No figure gives the composed image.
  - The platform points keep more than 1,100 B of granule margin, so no tile moves there (2.3).
  - The size fixture's one-interface answering-ports arm is at 132,976 B after p1win (line 166), 144 B under the 133,120 B granule ceiling. The PR's line states no fixture figures, so whether the seeded draw pushes that arm to 57.5 is unmeasured.
  - That arm's entry is 57.5 and it is refused only at 58.0 (`ctrl_memory.py`, `8x8-one-interface`), so a crossing would not refuse a build. It would make "the other arms and plants 57.0" stale as a description of the composed head. Each existing statement names its own measurement train, so none is false today.
  - **Suggestion:** have the merge-turn ledger (`plat_ledger.py`, and the CPU budget harness's fixture plans) record the composed figures, then either add one line under section 5 or confirm that no arm moves.
- **Carried:**
  - **R935-5 S5:** add `ctrl_boundary.py --require-rv32 --selftest` to "How to validate".
  - **R935-3 S2:** note the 12-versus-11 model bound under the README's ADP table.
  - **R935-3 S3:** keep one `[A847]` opening and fill the three roles.
  - **R935-2 S1:** raise H10's distinct-delay floor nearer the 915 observed.
  - **R935-2 S2:** reflow `adp_mbx.h:23-25`.
  - **R935-2 S3:** investigate the 16-bit quantization of `draw_ms`, separately.
  - **R935-1-S4:** remove the generator-order dependence (`PYTHONHASHSEED=0`), separately.
  - **R935-4 S4:** filter `model_counts.py:102`'s plant count to the planted path.

### Comment rule

I scanned the source lines this PR adds to the candidate (`*.c`, `*.h`, `*.cpp`, `*.py`, `*.json`) for lane labels, review rounds, reviewer IDs and comment IDs.
- The only label-like tokens are `B25`, `B26` and `B27` in `test_plat_boot.cpp` and `adp_first_mutants.py`.
- These are test-case IDs. They continue the file's existing `TEST_F(Boot, B1...)` to `B24` sequence at the base, and they are not bench lane labels.
- No new RESIDUE under the rule.

## 6. Per-lens results

```text
[R935] PASS Conformance - sw/firmware/ctrl/adp/adp_mbx.c, adp_mbx.h, sw/firmware/ctrl/plat/ctrl_plat.c, third_party/tsn-c-stack@c3bff8f3 as composed at 17f44fe0 - the PR's ADP draw hunks are byte-identical to the reviewed source (patch-id, receipts/composition.txt); no predecessor touches an ADP, platform-wiring or stack file; the draw's tests (H9, H10, B25 to B27) and its 26 planted defects pass on the composed tree against Milan v1.2 5.6.3.5.2/5.6.3.5.3 and IEEE 1722.1-2021 6.2.4.2.2 as the source tests encode them
[R935] PASS RTL - sw/litex/ctrl_memory.py:52,205 with docs/design/SPLIT_CONTROL_MEMORY.md:166,756; ctrl_plat.c and nvm_store.c composed in test_plat_boot_if1/if2 - no HDL changes on either side; the adapter and platform contracts the PR changes are untouched by the predecessors; the composed rom sums keep every platform point within its current granule (2.3); the store change and the draw's wiring link and pass together (platboot 59/60 checks)
[R935] PASS Robustness - receipts/focused_arms.log (platboot if1/if2, acmpnvm), receipts/adp_mutants_leg*.log - the composed boot paths with the new store window (the reset, reboot and journal cases B11 to B23 in the same binaries) pass beside the seeded draw; the duplicate and disabled LINK_UP cases (H9) and the clock-wired-late, millisecond and 1,024 us granule defects (B25 mutants) are caught on the composed tree
[R935] PASS Tests - sw/firmware/ctrl/test/ctrl_configs.py:171,315; test_ctrl_firmware_shards.py; tb/verilator/ctrl_service_budget/run.py:902, model_counts.py, selftest*.py - shared registries compose (registry probe CLEAN); shard dispatch keeps 2,026 invocations exactly once with the PR's mutants; the composed budget self-test is 1,048 checks PASS and 321 of 321 mutants caught, p1win's bind mutants included; model_counts finds every planted stale count
[R935] PASS Docs - CHANGELOG.md, docs/DOCUMENTATION_AUDIT.md, docs/design/{MAILBOX_SPLIT,SPLIT_CONTROL_MEMORY}.md, docs/reference/{FR_NFR,SUBMODULES}.md, docs/diagrams/submodule_boundaries.*, tb/verilator/{ctrl_service_budget,ctrl_reboot,mbx}/README.md at 17f44fe0 - docs_check, gen_toc (selftest, anchors, check), check_em_dash against the train parent and the whole train, doc style, doc paths, DOC_MAP, docs inventory, submodule docs and diagram, and PNG gates all pass on the composed tree; RES-B to RES-E are wording only and carried
```

## 7. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ADP adapter, platform wiring and stack-pin hunks (identity with the source), focused ADP/platboot suites, `adp_first_mutants` 26/26 | R935-6 (composition). Source: R935-5 (`35d29eb71`), R936-3 (`701a980b`) | `17f44fe0df361d02a8d6ea4081b99c6942bdc4a7` |
| RTL | CLEAN | No HDL on either side. `ctrl_memory.py` granule rule against both ledger lines; the store and platform link together | R935-6 (composition). Source: R935-5, R936-3 | `17f44fe0df361d02a8d6ea4081b99c6942bdc4a7` |
| Robustness | CLEAN | platboot if1/if2 (boot, reset, reboot and journal cases) with p1win's store; the H9 and B25/B27 negative cases and their mutants | R935-6 (composition). Source: R935-5, R936-3 | `17f44fe0df361d02a8d6ea4081b99c6942bdc4a7` |
| Tests | CLEAN | `ctrl_configs` registries, shard dispatch, fast-leg contract, the budget self-test with model counts and bind mutants, focused suites, ADP mutants | R935-6 (composition) | `17f44fe0df361d02a8d6ea4081b99c6942bdc4a7` |
| Docs | CLEAN (RESIDUE RES-B to RES-E carried) | Every shared or PR-touched document and its gates (section 3) | R935-6 (composition) | `17f44fe0df361d02a8d6ea4081b99c6942bdc4a7` |

The composition touches every lens's scope, through the shared test registries, the shared harness, the shared memory ledger and the shared documents. So each lens was applied here at the candidate head. It was not merely inherited from the source rounds. Code that only the PR changes keeps its source verdicts from R935-5 and R936-3, because the composition carries it byte-identically.

## 8. Real limits

- **`plat_ledger.py` did not run.** The host has no LiteX (`receipts/plat_ledger.log`: `ModuleNotFoundError: litex`). The composed `rom` figures in 2.3 are arithmetic on two published measurements, not a measurement. That includes the size fixture's arms (S6).
- **The full default firmware suite did not complete.** It needs longer than one call allows, and its `--jobs` is capped at 4. I ran the suites the composition reaches instead (ADP, plat, platboot if1/if2, acmpnvm), not all of them. Hosted `firmware-unit` passed at the source head only.
- **The full `ctrl_boundary.py` capture gate did not run.** Only its static cross-check by text was probed. Hosted `firmware-boundary` passed at the source head `35d29eb71`, not at this candidate.
- **No hosted run exists at `17f44fe0`,** because the candidate is local. Hosted evidence is from the source head only, and it was paired against `dev-soft-core` without cicd4 or p1win.
- **The budget self-test used a parallel driver** of the same functions (section 3), not the serial command line.
- **Physical calibration was NOT RUN.** Field skips are not hardware proof, and #970's bench re-run item is not proven by this round.
- **The evidence packet's commit is unsigned on GitHub.** Integrity rests on its manifest hashes, all 14 of which match, and it covers `0ad0e518` only.
- **The brief names live `dev` as `e275d7950`,** which is not an ancestor of this candidate. The PR's base is `dev-soft-core`, and the candidate is built on it (`4df125b8`). `e275d7950` carries three process commits (`490d54ee2`, `ee5c6f922`, `eade77c95`) that this tree does not contain.

## 9. Pending manager duties

- Build and validate the final current-dev merge candidate at the merge turn, with the builder and native banks, and link their receipts on the PR. Confirm which branch it targets (`dev-soft-core`, the PR's base, against the brief's live `dev` `e275d7950`).
- Run `plat_ledger.py` and the CPU budget harness's fixture plans on the composed candidate, and resolve S6.
- Obtain exact-head hosted or act evidence for the merge head: `rtl-fast` including `firmware-boundary` and `firmware-unit`, `docs`, and, if applicable, `verilator-suites` and `yosys-portability`.
- Carry RES-B to RES-E to the residue checklist.
- Get explicit maintainer authorization for the merge. #970 stays open for its bench re-run item until that is evidenced.

## 10. Checkout integrity after probes

`receipts/checkout_integrity.txt` records the final state:
- HEAD `17f44fe0`, tree, and index tree `2dc4b2ce...`;
- 0 worktree differences against HEAD (modes included), 0 untracked files and 0 ignored files;
- the 1,998 index entries hashed;
- all 6 gitlinks at their recorded commits (`external` uninitialised as at the start), and every initialised submodule clean, ignored files included.

The probes wrote only bytecode caches and two untracked `dispatch-build/keys/*.yaml` files, all of them during this session. I removed them.

R935-6 FINISHED
