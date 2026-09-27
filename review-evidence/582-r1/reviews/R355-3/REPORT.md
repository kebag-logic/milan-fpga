[R355] POSITIVE - exact head 1304205cfc9fa4c9e69a32130fb366895c5f883b

# R355-3: composition review of the #582 merge-train candidate (PR #596)

Round R355-3 is the external composition review of issue #582 / PR #596.

- **Candidate:** `1304205cfc9fa4c9e69a32130fb366895c5f883b`, tree `28c36c12cf459020de252185dbdb14ea508724d2`.
- **Parents:** train parent C_600 `b468a56d9e3ed9c10e4e41503c446dd6b242b9f8` and PR source head `aafcae59732c0a12333b73d82d5cdcbcbf90c47f`.
- **Source base:** `9e9954e96bf55181edb9949ae94c9abd4ab6aaf5`.

Scope is composition acceptance only. The PR source head already carries two independent POSITIVE source reviews: R354-3 at `aafcae59` and R355-2 at `77998f14`.

All five lenses were applied to the composed tree. No BLOCKER, MAJOR or MINOR finding is open. Two SUGGESTIONs follow; neither affects coverage. The composed tree introduces no defect beyond the reviewed sources.

## Scope reconstructed

I read the following, in order:

- AGENTS.md and CONTRIBUTING.md;
- docs/README.md;
- issue #582's body and frozen acceptance items 1-4;
- the [A10] scope comments (the scala_args message, the dated-history note for the tap page) and the round 1-3 assignments and decisions.

The recorded decisions are:

- one contract clock, `CPU_HZ` in `tb/verilator/nvm_capture_cpu/recipe.py`, imported by both entry points;
- no firmware, RTL, configuration or capture-receipt change;
- the five configurations stay byte-identical;
- sim-model mirrors and the listed suggestions go to #495 at merge.

Then I read the candidate diff `b468a56d..1304205c` and its history. Prior public review findings were read only after my own pass.

## Composition facts (`composition_overlap.sh`, `composition/overlap.txt`)

- **Clean merge.** `git merge-tree --write-tree b468a56d aafcae59` reproduces `28c36c12`, the candidate tree, so no hand resolution was involved.
- **Same patch.** The PR patch `9e9954e9..aafcae59` and the composed patch `b468a56d..1304205c` have the same stable patch-id, `32b34a81...`.
- **Unchanged PR files.** Eleven of the PR's 13 files are blob-identical at the candidate and at `aafcae59`.
- **Overlapping files.** Exactly two PR files were also changed by a train predecessor. In both, the changed-line sets are identical in the source and composed diffs.
  1. `docs/integration/BAREMETAL_FIRMWARE.md`, also changed by #397 (PR #588) in `ff75a7080`.
     - #582 edits the Contents list and the build contract (`:22-27`, `:38`, `:43-50`, `:56`, `:66`, `:68`).
     - #397 adds four service-budget lines at `:1899-1902`.
     - The hunks are about 1,830 lines apart.
  2. `sw/builder/endstation_builder.py`, also changed by #571 (PR #597) in `f8a52f919`.
     - #582 adds the recipe import at `:69-71` and the clock guard at `:4296-4299`, and edits the message at `:4303`.
     - #571 adds the `AEM_N_CONTROL_C` emission at `:2794`, with a comment. Its net line delta is 0.
- **Submodules.** The PR changes no gitlink. The candidate carries the #580 protocol-processor pin `16be6768`; gptp-processor and verilog-axis are unchanged.

## Semantic interactions examined

| Interaction | Result | Evidence |
|---|---|---|
| Build contract vs #397 service-budget text in one page | Coherent. The #397 lines state no clock and link `docs/findings/397_SERVICE_BUDGET.md` and #590. Nothing cites the removed "not checked by either tool" / "tracked in #582" text; a repo-wide search finds no stale reference. | `BAREMETAL_FIRMWARE.md:1899-1902`; `gen_toc.py --verify-anchors` (195 links) and `--check` rc 0; `docs_check.py` rc 0 |
| Single-definition clock wording on the page | Holds. The only remaining `50 MHz` figures on the page, `:1995` and `:2021`, belong to the dated Vivado cell record for commit `1e80a106`. They predate both PRs (blame `38e27930`) and are already classified as dated records (R355-1 SG3). | `BAREMETAL_FIRMWARE.md:1990-2023` |
| Builder clock refusal vs #571 header emission | Independent and both live. Removing the guard is caught by the clock-contract test and not by the entity-shape gate. Removing the emission is caught by the entity-shape gate and not by the clock-contract test. | probes P3-P6 |
| Generated artifacts of the five configurations | Candidate equals train parent byte-for-byte: 59 files, including `gptp_ucode.hex`. The PR head equals its source base. Source base to candidate changes only `adp_shape_defaults.svh`, one line per configuration: `localparam int AEM_N_CONTROL_C = 1;`, from #571. #582 adds nothing. The candidate's regenerated `configs/generated/**` and `hdl/common/gen/adp_shape_defaults.svh` equal the tracked blobs. | `identity/identity-*.sha256`, `identity/adp_shape_diff_base_vs_candidate.txt`, `identity/candidate_generated_vs_tracked.txt` |
| #580 capture re-measure vs #582 clock import | Consistent. `check_nvm_capture.py` passes on the candidate, because the receipt hashes the unchanged `recipe.py` and `measured_for` records `configured_cpu_hz` 50 MHz. Moving `CPU_HZ` or the 8x8 declaration makes the gate refuse. | gate 23; probes C1, P2, P8 |
| #397 harness vs #582 SoC change | No behaviour interaction. The #397 build reuses the capture SoC through `milan_soc.MilanSoC` and never runs `main()`, where the new guard sits. `run.py --self-test` passes. The #397 external receipts inventory `sw/litex/milan_soc.py` (`run.py:153-160`), so they do not regrade on the merged tree. The #580 pin change in the same train had already changed their compiled inputs. They are dated external evidence, not tracked gates. | gate 40; `tb/verilator/nvm_capture_cpu/soc.py:62`, `:119-121` |
| Gate-read page registry and CI policy page | Consistent. The train changes neither `scripts/ci_scope.py` nor `docs/testing/CI_WORKFLOWS.md`. The four `GATE_READ_DOCS` pages match the "Four pages" prose, and the self-test derives the list from the composed tree. | gates 20-22 |
| Test-evidence and source registries touched by the train | Pass on the candidate: `measure_test_evidence.py --check/--selftest`, `pp_srcs.py --check`, `check_entity_shape.py` (166 checks, including `AEM_N_CONTROL_C == CONTROL census` per configuration) and its self-test (219). | gates 24-30, 39 |

## Gates run on the candidate (`run_gates.sh`, `run_md_gates.sh`)

`gates/gates-summary.tsv` and `gates/md-gates-summary.tsv` record every gate, all in the foreground at `1304205c`.

**Git and docs checks.**

- `git diff --check b468a56d..HEAD`: rc 0.
- `docs_check.py`: rc 0 (172 md files); `--selftest`: rc 0.
- The renderer-dependent gates used the pinned renderer environment, cmarkgfm 2025.10.22 and html5lib 1.1, all rc 0:
  - `check_em_dash.py --base b468a56d` (54 added lines, 5 pages, 339/339 arms);
  - `check_em_dash.py --base 9e9954e9` (1,866 lines, 20 pages);
  - `check_em_dash.py --selftest`;
  - `gen_toc.py --selftest` (1501/1501);
  - `gen_toc.py --verify-anchors`;
  - `gen_toc.py --check` (114 pages).
- Gates 05-10 in the first summary are rc 2 only because that interpreter lacked the pinned renderer, and they refused to judge. They are superseded by md02-md07.
- `check_doc_style.py`, `DOC_MAP.gen.py --check/--selftest`, `check_doc_paths.py`, `check_solution_docs.py` and its self-test: all rc 0.

**CI, capture and entity-shape checks**, all rc 0:

- `check_baremetal_only.py --check/--selftest`;
- `ci_scope.py --selftest`;
- `ci_events.py --check` (1655 items) and `--selftest`;
- `check_nvm_capture.py`;
- `check_nvm_record_space.py`;
- `check_entity_shape.py` and `--self-test`;
- `check_sweep_shape.py --self-test`;
- `check_deploy_shape.py --self-test`;
- `measure_test_evidence.py --check/--selftest`.

**Idiom and hygiene checks**, all rc 0: `check_py_idiom.py`, `check_sh_idiom.py`, `check_hygiene.py --check`, `check_todo_ownership.py` and `check_feature_status.py`.

**Tests**, all rc 0:

- `sw/builder/test_clock_contract.py`: 5 positives, 50 named refusals, 5 ROMs, extra sweep, 5 tap rows.
- `sw/builder/test_declarations.py`.
- `pp_srcs.py --check`.
- `tb/verilator/fw_service_budget/run.py --self-test`: 30 checks.

## Probes (`probes.sh`, `probes/probes-summary.tsv`)

The probes ran on a disposable export of the candidate, with the submodules exported at their pins. Each planted file was restored and its SHA-256 verified.

| ID | Plant | Gate | Result |
|---|---|---|---|
| C0/C1/C2 | none | clock contract / capture receipt / entity shape | PASS (controls) |
| P1 | `recipe.py` `CPU_HZ` to 100 MHz | builder on 8x8 | KILLED: `baremetal clock: milan_clk_hz must be 100000000 Hz` |
| P2 | same | `check_nvm_capture.py` | KILLED |
| P3 | builder guard disabled | clock contract | KILLED: `accepted invalid input: baremetal clock ...` |
| P4 | same | entity shape | PASS (independent of #571) |
| P5 | #571 `AEM_N_CONTROL_C` emission removed | entity shape | KILLED: tracked ADP shape differs |
| P6 | same | clock contract | PASS (independent of #582) |
| P7 | 8x8 declares 100 MHz | builder | KILLED: `must be 50000000 Hz` |
| P8 | same | capture receipt | KILLED |
| P9/P10 | tap table presence / clock row altered | clock contract | KILLED: `tap clock table differs from the configurations` |

## Findings

No BLOCKER, MAJOR or MINOR finding is open at this head.

### S1 - SUGGESTION - Conformance, Docs - `tb/verilator/fw_service_budget/run.py:19`, `:440`, `:452`; `tb/verilator/fw_service_budget/README.md:5` - a train predecessor restates the contract clock outside the #495 list

- **Authority and evidence.**
  - The #582 decision gives the clock one source, and the composed `BAREMETAL_FIRMWARE.md:43` says it has a single definition.
  - #397, composed ahead of #582, drives its product-CPU clock from its own literal `CPU_HZ = 50_000_000` (`run.py:19`, assigned to `args.cpu_hz` at `:440`). That literal overrides the configured clock in the reused capture SoC (`soc.py:121`).
  - The check at `:452` compares the build spec against the same literal, so it is not a cross-check against `recipe.CPU_HZ`.
- **Why a suggestion.** Today both values are 50 MHz, so the measured behaviour is correct.
  - The maintainer decision already routes the same class of sim-model mirror to #495 (`tb/verilator/milan_dp/Makefile:413`, `sim_ax1x1gptp.cpp:57`).
  - The #397 page labels its results as measurements at 50 MHz.
  - This literal could not be named in that decision, because #397 was not in #582's base.
- **Suggested outcome.** Add `run.py:19` (and the README line) to the #495 list at merge, so the harness derives its CPU clock from `recipe.CPU_HZ`.
- **Verification.** Planting another `recipe.CPU_HZ` either changes the harness's `args.cpu_hz` or fails a gate.

### S2 - SUGGESTION - Docs - `docs/findings/397_SERVICE_BUDGET.md:25-26` - stale premise after #565 and #582

- **Evidence.** The page says "The 8x8 configuration's Milan-clock declaration is overridden by the existing capture recipe to satisfy this assignment's explicit 50 MHz contract."
  - That sentence was written against a base where the 8x8 declared 100 MHz: `7f997b60d:configs/endstation_ax7101_8x8.yaml:56` is `100000000`.
  - In the composed tree the 8x8 declares the contract clock (#565), and the builder refuses any other value (#582, probe P7). The "override" is now the identity.
- **Why a suggestion.** The staleness comes from the #397 x #565 composition already in C_600, not from #582. The measured numbers are unaffected.
- **Suggested outcome.** Reword the sentence with #495, or with the #397 follow-up (#590).
- **Verification.** A reader of the page does not infer that the 8x8 declares a clock other than the contract clock.

## Prior public review findings on this PR (read after my own pass)

Eleven of the 13 PR files are blob-identical to `aafcae59`. The other two differ only by the predecessor hunks analysed above. Every finding therefore keeps the status R354-3 recorded at `aafcae59`.

| Prior item | Status at 1304205c | Evidence |
|---|---|---|
| R354-1 F1 = R355-1 F1 BLOCKER; manager bank r1 gate 6 | RESOLVED; still holds | gate 20 `ci_scope.py --selftest` rc 0 on the composed tree |
| R354-1 F2 = R355-1 F3 MINOR (configured clock to gPTP ROM) | RESOLVED; still holds | gate 36: 5 ROMs match configured clocks; `gptp_ucode.hex` identical parent vs candidate |
| R355-1 F2 MINOR (refusal coverage) | RESOLVED at source; SoC cases not re-run here (no LiteX) | builder refusals: gate 36 (50 refusals), probe P3; `test_clock_contract.py`, `milan_soc.py` blob-identical to `aafcae59` |
| R355-1 F4, F5 MINOR; R354-1 S1, S2 | RESOLVED; files blob-identical to `aafcae59` | `identity/pr_files_blob_vs_source_head.txt` |
| R354-2 F1 MINOR = R355-2 SG5 | RESOLVED; `CI_WORKFLOWS.md` and `ci_scope.py` blob-identical, and the train touches neither | gates 20-22 |
| R354-2 SG1; R355-2 SG6, SG7 | RESOLVED (R354-3); unchanged files | as above |
| R354-3 S1, S2 | RETAINED as suggestions | unchanged files |
| R355-1/-2 SG1-SG4, R355-2 SG8, R354-1 S3 groups 4-5 | RETAINED as suggestions; routed to #495 at merge per assignment | unchanged files |

## Reviewer-owned ledger

| Lens | Status | Examined artifacts (at the candidate) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Composition touches it: acceptance item 4 re-proved on the composed tree (`identity/*`); item 1 guard live with #571 (P1, P3-P7); `BAREMETAL_FIRMWARE.md:38-50` vs `:1899-1902` coherent; S1 recorded | R355-3 | `1304205cfc9fa4c9e69a32130fb366895c5f883b` |
| RTL | CLEAN | Composition does not touch RTL scope: the composed diff has no `.sv`/`.svh`/gitlink change, and the generated SV headers and ROM are byte-identical parent vs candidate (`identity/identity-b468a56d...` = `identity-1304205c...`). RTL scope otherwise covered by the source reviews | R355-3; source reviews R354-3 and R355-2 | `1304205cfc9fa4c9e69a32130fb366895c5f883b` (source: `aafcae59`, `77998f14`) |
| Robustness | CLEAN | Composition touches it: builder refusal next to #571 emission; divergent recipe and configuration clocks refused by the builder and the capture receipt (P1, P2, P7, P8); no-output-on-refusal (gate 36) | R355-3 | `1304205cfc9fa4c9e69a32130fb366895c5f883b` |
| Tests | CLEAN | Composition touches it: `test_clock_contract.py`, `test_declarations.py`, `check_entity_shape.py` (#571 unit counts), `check_nvm_capture.py` (#580), `fw_service_budget --self-test` (#397), `measure_test_evidence.py` pass; mutual-independence probes P3-P6 and table probes P9/P10 kill | R355-3 | `1304205cfc9fa4c9e69a32130fb366895c5f883b` |
| Docs | CLEAN | Composition touches it: `BAREMETAL_FIRMWARE.md` merged page, TOC/anchors/em-dash/docs/DOC_MAP/ci_events/ci_scope gates (gates 03-22, md02-md08); S1 and S2 recorded | R355-3 | `1304205cfc9fa4c9e69a32130fb366895c5f883b` |

## Real limits

- **No SoC tests.** LiteX is not installed in this session, so neither `test_clock_contract.py --soc` nor `sw/litex/test_pp_mem_bridge.py` was run. `milan_soc.py`, `test_pp_mem_bridge.py` and `test_clock_contract.py` are blob-identical to the source head, where the source reviews and the manager's bank ran them. The train changes no file they import directly, but #580's pin and #571's HDL are inputs to the native bank.
- **No builder or native bank.** Per assignment I did not run the full builder bank (`test_builder.py`), which imports `test_clock_contract`, or the native, PP, gPTP or Yosys banks.
- **No Verilator.** The scoped Verilator path named in the assignment does not exist on this host. No Verilator run was needed, because the composition touches no RTL.
- **No candidate bank receipt.** None of the manager's bank receipts for `1304205c` had been posted on the issue or PR when this review was written. The public evidence at `e0c591ff/review-evidence/582-r1` is source-round evidence.
- **Hosted evidence covers the source head only.** `1304205c` is not on the hosting service, so it has no hosted runs. The PR source head `aafcae59` shows 19 of 20 check runs complete: success, plus "Physical gPTP" skipped, which is not hardware proof. "Verilator shard 1/5" was still in progress when read.
- **Live dev has moved.** Dev is now `8bc97021`: #588 merged over `6d5ebd73`. Its commits `7f997b60d` and `ff75a7080` are already ancestors of the candidate. The final current-dev candidate still has to be built and validated.
- **Environment artefact.** My gate runs created the ignored `sw/builder/out/` inside the clone (`gates/logs/38.log`). It was removed, and the final integrity check passes: exact head and tree, `write-tree`, index, per-blob bytes and modes, and the three submodule gitlinks clean at their pins (`integrity/verify-final.log`).
- **No hardware.** No physical calibration or hardware validation was done.

## Pending manager duties

- Build and validate the final current-dev candidate against live dev (now `8bc97021`).
- Run the builder bank (both compiler modes) and the native/SoC banks on it, including `test_clock_contract.py --soc` and `test_pp_mem_bridge.py`.
- Own the hosted and local-replica acceptance, including the in-progress Verilator shard at `aafcae59`.
- At merge, route S1 and S2 with the existing #495 items. S2 could instead go to the #397 follow-up.
- Publish this packet: `REPORT.md` and the files listed in `MANIFEST.sha256`.

R355-3 FINISHED
