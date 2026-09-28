[R367] POSITIVE - exact head a3f95a4cea1faa3470b65b4ffc8a9bb3dc1b0c9c

# R367-4: composition review of PR #603 (issue #602) on the merge-train candidate

- **Candidate:** `a3f95a4cea1faa3470b65b4ffc8a9bb3dc1b0c9c`, tree `289ab42c1ba974b27ac35b6891f2a9d25b80be25`.
  - Parents: train parent `1a3c716f6e9fbc1c3227bce0a287ac943944fcbb` (after #595) and PR source head `d09c72ea2b0be1a2df3e18e77774f14f6df3242c`.
- **Focus:** composition acceptance only. The question is whether the composed tree introduces any defect beyond the reviewed source.
- **Reconstruction order:** AGENTS.md and CONTRIBUTING.md (sections 2.1 step 7, 3 and 6.1), then docs/README.md.
  - Issue #602: body, ruling 5859297355, assignment 5859299480, scope correction 5859621253, and the merge-dev round 5866438374 with dispositions 5866546855, 5866668156, 5868109315 and 5868627247.
  - The manager's R367-4 start comment 5868954976.
  - The linked authorities: `GM_LOSS_RECOVERY.md#media-re-base-on-a-phc-step`, `TIME_SYNC.md`, `REQUIREMENTS.md` section 8, and `TESTING.md` 6d.
  - Then the diff `1a3c716f..a3f95a4c` and its history, then executable evidence.
- **Independence:** my own pass over the composed diff, the gates and the stale-claim scan came first. Only after that did I read prior public review findings on PR #603. No private author material and no other reviewer's report was read before this verdict and ledger were settled.
  - I listed the public evidence manifest at `1dab2e7c:review-evidence/602-r1`. It is the round-1 source packet and not candidate evidence, so I did not rely on it.
- **Clone state:** probes and gates ran in the detached clone. Afterwards only ignored build products were removed. `receipts/verify_clone.txt` shows the following, with `VERIFY: PASS`:
  - HEAD, index tree and HEAD tree are exact.
  - All 950 superproject blobs were re-hashed from disk, with modes checked.
  - The three initialised gitlinks equal their checkouts, and each submodule's own blobs were re-hashed.
  - `external` is uninitialised with an empty directory.
  - No untracked or ignored residue remains.

## Verdict

**POSITIVE.** The composed tree introduces no defect beyond the reviewed sources.

- The merge is clean and patch-equivalent: the PR's delta onto the train is byte-identical to its reviewed source delta.
- The two shared files compose without overlap or semantic conflict.
- Every gate that reads them passes on this tree, including the full builder bank in both compiler modes, the pinned-environment Markdown gates and the full gmstep campaign.
- No `BLOCKER`, `MAJOR`, `MINOR` or `SUGGESTION` finding is raised. Every prior MINOR or MAJOR on this PR is verified resolved at this head.

## Composition facts (`receipts/composition_facts.txt`)

| Fact | Evidence |
|---|---|
| Candidate tree is the clean merge | `git merge-tree --write-tree 1a3c716f d09c72ea` gives `289ab42c`, which equals the candidate tree (rc 0, no conflict, no hand resolution) |
| Live dev is inside the train | Live dev `7a7582f0` tree `cd7ae956` equals the #70 train step `c08becbb` tree. After it come #606-608, #577, #395 and #595 |
| PR delta unchanged by composition | `diff(0eff6d2e..d09c72ea)` and `diff(1a3c716f..a3f95a4c)` are identical apart from `index` lines |
| Shared files (train and PR both change them since merge-base `0eff6d2e`) | exactly `docs/integration/BAREMETAL_FIRMWARE.md` and `sw/builder/test_builder.py` |
| Firmware doc hunks | Train (#70 PR #610): old lines 1905 and 1917. PR: old lines 1475 and 1477. They are disjoint |
| Builder hunks | Train (#577, #395, #595): 25546-25808, 27231, 27556-27638. PR: 10717-16654, all inside `test_baremetal_profile_contract`. They are disjoint |
| Gitlinks | protocol-processor is `c951a9ff` in the candidate (from the train) and `16be6768` at the PR source. gptp-processor, verilog-axis and external are equal. The train changes 0 files under `hdl/` |

## Semantic interactions checked

1. **`BAREMETAL_FIRMWARE.md` (#70 D3 text and #602 gate-contract rows).**
   - `:1475` states two `media_rebase_p_w` references with `render_recentre_p_w` as the sole reader. `:1477` states the CRF-only `mcr_restart_p_w` initializer. Both cite the #602 ruling.
   - These match the composed RTL: `hdl/milan/milan_datapath.sv:3132-3134` has the initializer, the reader is at `:6053-6054`, and the port is at `:3163`.
   - They also match the builder census at `sw/builder/test_builder.py:10719-10720,10775-10780`.
   - The #70 text is intact, and none of it concerns `mr`: the D3 DR2a debounce at `:1905-1906` and the DR2c retry/alarm paragraph at `:1919-1931`.
   - The file has no statement that a PHC-only step toggles `mr`. Every `mr`, re-base or `mcr_restart` token in the file is at `:1474-1477,1528-1530`.
   - Its D3 anchors (`SAVED_STATE_MATERIALIZATION.md#151-...`, `#182-...`, `SAVED_STATE_FASTCONNECT.md#92-...`) are among the 235 cross-page fragments `gen_toc.py --verify-anchors` reproduces.
   - Builder gate 1b reads this page (`test_builder.py:3046-3054`, `assert_boot_contract`) and passes in both modes.
   - As instructed, the later #70 correction of DR2c-carrier item 3 is not treated as a #602 concern.
2. **`test_builder.py` (gates from #577, #395 and #595, plus #602's gate-1b entries).**
   - There are no duplicate top-level definitions and no duplicate `gate` banners. Every `test_*` definition is called from `__main__` (`:27808-27830`).
   - The lanes' gate names and numbers are distinct:
     - `[timing grade]` `test_commercial_timing_grade` (`:27797`);
     - gate 36b (`:27234`, `:27325`);
     - `test_declaration_contracts` from `test_declarations.py`;
     - gate 1b `test_baremetal_profile_contract` (`:2980`).
   - All ran in both banks. `builder_rv32_elab.log` shows the `[timing grade]`, `[F1]` declaration, `[gate 36b]` and `[gate 1b]` output.
   - The only remaining `| media_rebase_p_w` spellings are intentional mutation anchors (`test_builder.py:12470`, `gmstep_mutants.py:132,144,197`).
3. **Processor pin change (`16be6768` to `c951a9ff`, from the train).**
   - The gmstep and option-off legs elaborate the full datapath with the train's pin. The full campaign passes 22/22 on it.
   - The builder's 53/53 RTL variants and `lint_rtl.py --check` also pass on it.
   - The `16be6768` citations in `CHANGELOG.md` and the D3 documents belong to other lanes and are historical. PR #603 cites no processor pin.
4. **Predecessor text that names #602.**
   - `SAVED_STATE_MATERIALIZATION.md:2262` (DR6) lists #602/PR #603 as a lane-2..5 input.
   - `:2641` says "Observe #602's final media-reset rule when grading timestamps".
   - Both remain consistent once #602 lands, because the rule they defer to is the one this PR states.
   - `75_RECONNECT_RESTART_MEASUREMENT.md:116` ("The mask leaves `mr`, `fs`, and `tu` unchecked") is unrelated.
5. **Tree-wide stale-claim scan** (`scripts/stale_claims.py` produces `receipts/stale_claims.txt`, 64 lines, `docs/history/**` excluded).
   - Every hit is one of four kinds:
     - a post-#602 statement;
     - a measurement contract explicitly labelled pre-#602 (`394_387_E1_SWITCH_CYCLES.md:165-177`, with the table row at `:239`);
     - a mutation inventory entry (`gmstep_mutants.py`, `milan_dp/README.md:697-712`);
     - a check name.
   - No line presents a PHC-only step as toggling `mr` or counting MEDIA_RESET. That includes the lines the predecessors added.
6. **Inventories, records and ratchets.**
   - `ci_events.py --check` passes: 1655 contract items across 4 workflows and `CI_WORKFLOWS.md`.
   - `measure_test_evidence.py --check` passes. It reports "can be lowered to 75", which is advisory for a downward-only ratchet and not a failure.
   - These also pass: `check_py_idiom`, `check_cpp_idiom`, `check_sh_idiom`, `check_sv_idiom`, `check_hygiene`, `measure_naming`, `measure_fail_fast`, `check_port_contracts`, `check_rtl_source_lists` and `pp_srcs.py --check`.
   - `TESTING.md:273` states fifteen gmstep plus five option-off controls, with five running by default. This equals the composed `gmstep_mutants.CONTROLS` inventory: 15 + 5 controls, 5 marked acceptance.

## Executed gates on the candidate (`receipts/summary.tsv`, 47 receipts, all rc 0)

| Gate | Result |
|---|---|
| `python3 sw/builder/test_builder.py --require-rv32 --require-elaboration` (pinned SDK installed by `scripts/ci_rv32_sdk.py` into scratch, verified archive `d42680e9...`, gcc 14.3.0; LiteX interpreter matching all seven `litex_pins.txt` revisions) | rc 0, 741 s. Gate 1b rejects 358/358 mutations; 53/53 RTL variants elaborate. `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11) |
| Compiler-absent bank: the same entry point with `--require-elaboration`, every `riscv*-gcc` hidden from PATH and no SDK under HOME | rc 0, 530 s. 256/256 mutations; 53/53 variants. `EXCEPT 2 NOT RUN` (gate 11, and the compiled census that needs RV32) |
| `sw/builder/test_firmware_compiler.py --selftest` / `--absent --audit` | rc 0 / rc 0 (`GATE 1b PASS; 1 NOT RUN; 0 actual firmware compiler invocations`) |
| `make -C tb/verilator/milan_dp gmstep-mutants` (Verilator 5.050, rev v5.050) | rc 0, 1004 s. The gmstep leg passes 103 checks with 0 failures. Campaign: `22 checks: 22 PASS, 0 FAIL`, which is both clean legs plus all 20 controls, including the delayed 16- and 256-cycle adjtime causes and coincident-step suppression |
| `check_em_dash.py --base 1a3c716f` / `--base 0eff6d2e` / `--selftest` | rc 0 (0 findings over 168 added lines in 13 pages, arms 339/339) |
| `docs_check.py`, `gen_toc.py --verify-anchors` / `--check` / `--selftest`, `check_doc_style` (+selftest), `check_doc_paths`, `check_gptp_docs`, `check_feature_status`, `DOC_MAP.gen.py --check`, `timesync_chain.gen.py --check`, `submodule_boundaries.gen.py --check`, `check_solution_docs`, `check_submodule_docs`, `check_diagram_pngs`, `check_archive` | all rc 0, using the pinned Markdown lock (`cmarkgfm==2025.10.22`, `html5lib==1.1`, hash-required install) |
| `check_baremetal_only --check` / `--selftest`, `check_nvm_record_space`, `check_soc_sources`, `ci_scope --selftest`, `ci_events --check` / `--selftest`, `lint_rtl --check`, `check_wire_accountability --self-test`, and the ratchets in item 6 | all rc 0 |
| `git diff --check 1a3c716f HEAD` | rc 0 |

The scripts that reproduce these results are in `scripts/`:

- `run_gate.sh` is the receipt wrapper.
- `static_gates.sh` runs the static gates.
- `long_banks.sh` runs the builder modes, the firmware compiler controls and gmstep.
- `composition_facts.sh`, `stale_claims.py` and `verify_clone.py` produce the facts, scan and clone receipts.

## Prior public findings on PR #603, dispositioned at this head

| Finding | Status at `a3f95a4c` | Evidence here |
|---|---|---|
| R367-1 F1 (MINOR, Docs); R366-1 F1 (MAJOR, Docs): current documents stated the superseded PHC-step `mr` / MEDIA_RESET rule | RESOLVED | Stale scan item 5; `REGISTER_MAP.md:128`, `FPGA_DESIGN.md:178`, `MILAN_COMPLIANCE_MATRIX.md:120,206`, `MILAN_V12_ROADMAP.md:360` |
| R367-1 F2, R366-1 F2 (MINOR, Docs and Tests): campaign routing and harness narrative | RESOLVED | `TESTING.md:273`, `milan_dp/README.md:79,658-728`, `KL_media_clock_restart.sv:63-64,105-109,171-172` |
| R366-1 F3 (MINOR, Tests): settime check measured absolute level | RESOLVED | The control "software settime is restored as an `mr` cause" is caught by "CLKV: the settime leaves mr unchanged (#602)" (`receipts/gmstep_campaign.log`) |
| R366-2 F1 (MINOR, Tests and Robustness): adjtime cause landing 16 or more cycles late | RESOLVED | The 16-cycle and 256-cycle controls are both caught (`receipts/gmstep_campaign.log`) |
| R367-2 F1 (MINOR, Docs and Conformance): `BAREMETAL_FIRMWARE.md` gate rows stated the PHC-inclusive initializer | RESOLVED, and it holds after composition with #70 | Item 1: `:1475,1477` |
| R366-4 F1 (MINOR, Conformance and Docs): `394_387_E1_SWITCH_CYCLES.md` stated the superseded contract | RESOLVED | `:165-177` is labelled pre-#602; `:353-355` states the post-#602 acceptance |
| All SUGGESTIONs (R367-1 F3/F4, R366-1 F4, R366-2 F2/F3, R367-2 F2/F3, R367-3 S1, R366-3 S1/S2) | optional; none reopens coverage | n/a |

## Findings

None. No `BLOCKER`, `MAJOR`, `MINOR` or `SUGGESTION` is raised by this round.

## Clean lenses

```text
[R367] PASS Conformance - docs/integration/BAREMETAL_FIRMWARE.md:1474-1477 vs hdl/milan/milan_datapath.sv:3132-3134,3163,6053-6054 and sw/builder/test_builder.py:10719-10720,10775-10780; composed-tree scan receipts/stale_claims.txt - the composed rows and every current statement match the #602 ruling 5859297355 (PHC-only re-base is not an mr cause; tu signals it); the D3 text at :1905-1906,1919-1931 is intact
[R367] PASS RTL - hdl/ delta 1a3c716f..a3f95a4c equals the reviewed source delta (receipts/composition_facts.txt); train changes 0 hdl files; processor pin c951a9ff elaborated in the gmstep/option-off legs (receipts/gmstep_campaign.log), 53/53 builder RTL variants (receipts/builder_rv32_elab.log) and lint_rtl --check (receipts/static/lint_rtl_check.log)
[R367] PASS Robustness - receipts/gmstep_campaign.log on the candidate's pin: delayed adjtime causes at 16/256 cycles, settime and both-cause restorations, coincident-step suppression, tu/holdover and licence controls all caught; clean legs pass; compiler-absent mode grades gate 1b with 0 compiler invocations (receipts/builder_absent_elab.log, receipts/fwcompiler_absent.log)
[R367] PASS Tests - sw/builder/test_builder.py composed gate inventory (__main__ :27808-27830; no duplicate defs or gate banners; every test_ def called), both builder modes rc 0 with each lane's gates executed; gmstep_mutants.CONTROLS 15+5 = TESTING.md:273; test-evidence/idiom/hygiene/naming/fail-fast ratchets rc 0 (receipts/summary.tsv)
[R367] PASS Docs - pinned-lock Markdown gates on the composed tree: check_em_dash vs 1a3c716f and 0eff6d2e, docs_check, gen_toc --check/--verify-anchors/--selftest, doc paths/style, ci_events --check (receipts/static/*); cross-lane anchors REQUIREMENTS.md#8-..., TESTING.md#6b-.../#6d-..., GM_LOSS_RECOVERY.md#media-re-base-on-a-phc-step resolve
```

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Does the composition touch its scope? | Covering round | Exact head |
|---|---|---|---|---|---|
| Conformance | CLEAN | `BAREMETAL_FIRMWARE.md:1474-1477,1905-1931`; `milan_datapath.sv:3132-3163,6053`; stale scan | Yes: the shared firmware document | R367-4 | `a3f95a4cea1faa3470b65b4ffc8a9bb3dc1b0c9c` |
| RTL | CLEAN | `hdl/` patch equivalence; processor gitlink `c951a9ff`; elaboration in the gmstep, option-off and 53 builder variants; lint ratchet | Only through the processor pin (0 `hdl/` files from the train) | R367-4 for the composed pin. The source RTL is covered by R366-5 at `d09c72ea` and R367-3 at ancestor `6b2ebd1c`, and `hdl/` is untouched since | `a3f95a4cea1faa3470b65b4ffc8a9bb3dc1b0c9c` |
| Robustness | CLEAN | Full gmstep campaign 22/22; compiler-absent bank | Only through the processor pin | R367-4. Source: R366-5, R367-3 | `a3f95a4cea1faa3470b65b4ffc8a9bb3dc1b0c9c` |
| Tests | CLEAN | `test_builder.py` composed inventory, both builder modes, `gmstep_mutants.py` inventory, test-evidence ratchet | Yes: the shared builder file | R367-4 | `a3f95a4cea1faa3470b65b4ffc8a9bb3dc1b0c9c` |
| Docs | CLEAN | Pinned Markdown gates; anchors; `TESTING.md:273`; D3 and #602 text coherence | Yes: the shared firmware document, and predecessor docs naming #602 | R367-4 | `a3f95a4cea1faa3470b65b4ffc8a9bb3dc1b0c9c` |

Source reviews I name for the source content, and do not re-litigate:

- R366-5 is POSITIVE at `d09c72ea2b0be1a2df3e18e77774f14f6df3242c` (PR comment 5868940566).
- R367-3 is POSITIVE at `6b2ebd1c435136966f84ffc16d28a80c7d6b9387` (PR comment 5862245933). That head is a pre-merge-dev ancestor, and later source commits were delta-reviewed by R366-4 and R366-5.

## Real limits

- **Gate 11 NOT RUN in both builder modes.** Its historical placed-calibration report is absent on this host, including under the real HOME. This matches the source evidence.
- **Compiler-absent mode also omits the compiled census by design.** The RV32 mode executes it.
- **Verilator path.** The named `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host. I used a scratch wrapper to the same container install that the other 5.050 wrappers here point to, and it reports `Verilator 5.050 2026-07-01 rev v5.050`. The system `verilator` is 5.052 and was not used.
- **LiteX.** The bench venv matches all seven pinned revisions. Its `litex` checkout carries the project's patch series as local modifications, and `test_toolchain_patches_are_applied` grades that series.
- **Not run: other suites and banks.**
  - The full `milan_dp` `run` sweep, `tkdiag`, Yosys/OOC and the parent, processor and gPTP banks were not run. They were not permitted in this round.
  - The composition changes no input of `tkdiag`: `KL_media_clock_restart.sv` and its harness are untouched by the train.
- **Not inspected: hosted and act evidence.** Hosted and act results for this candidate were not inspected.
- **Unpinned PyYAML.** PyYAML was installed unpinned, as the docs workflow does.
- **Redacted receipts.** Home-directory paths in `receipts/gmstep_campaign.log` were replaced with `$HOME`. The original hash is in `receipts/redaction.txt`.
- **No physical claim.** Physical calibration was NOT RUN. Field and simulation passes are not hardware proof.

## Pending manager duties

- Build and gate the final current-dev candidate at the merge turn. This round judged the train candidate `a3f95a4c` on top of live dev `7a7582f0`.
- Record hosted and act acceptance on the merge candidate.
- Carry the dev-parent artifact-identity baseline forward if dev moves.
- Check containment after the merge.
- Keep the `docs/findings/README.md` index entry for `394_387_E1_SWITCH_CYCLES.md` routed to the #495 checklist, per disposition 5868627247.

R367-4 FINISHED
