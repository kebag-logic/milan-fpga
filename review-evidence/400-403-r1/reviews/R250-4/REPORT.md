[R250] POSITIVE - exact head c6c65e803f9eb270a11dfd65fda5814fb0b0ea55

# R250-4: external independent review of PR #566 (issues #400 and #403), round 4

- Head `c6c65e803f9eb270a11dfd65fda5814fb0b0ea55`, tree `12cccfa4014def96bb5d71563084c68cc6f137ef`. This is one commit on `e122f330` by the round-4 executor.
- This is a delta review. R250-3 covered `e122f330` in full. This round judges `e122f330..c6c65e80`: 6 files, +95/-84. It also rechecks every earlier public finding at this head.
- All five lenses were applied: Conformance, RTL, Robustness, Tests and Docs.
- **No BLOCKER, MAJOR or MINOR finding is open at this head.** R250-3 N1 (MINOR), R250-3 S2 and S3, and R249-3 S2 are closed. The two suggestions already moved to #495 are retained as SUGGESTION.
- **Merge caution. This does not affect the verdict, but it is new since R250-3.** The hosted `docs-check` job **fails** at this head. It fails on the merge ref `f7ecbc9f` (this head merged into live dev `1299b461`), not on the source tree.
  - The failing gate is `scripts/check_nvm_capture.py`. Dev added it in `31808e65`, after this PR's base, and it does not exist at this head.
  - It pins the product firmware digest. This PR changes that firmware.
  - The current-dev candidate therefore needs a re-measured capture receipt before merge. See pending manager duty 1.

## Reconstruction

The review was rebuilt from public state only, in this order:

1. AGENTS.md, CONTRIBUTING.md (sections 6.1 and the commit rule) and docs/README.md.
2. The #400 body, the round-4 assignment 5836794096, the executor's TAKEN 5836828595 and REVIEW READY 5837226204, and the review start 5837258946.
3. The authorities for the edited text:
   - `docs/ENDSTATION_BUILDER.md` rows 30 and 39.
   - `sw/builder/README-parameters.md:71`.
   - The builder's own gates at `sw/builder/endstation_builder.py:3196-3201` and `:3250-3255`.
   - The csr and pp_shadow Makefile recipes.
4. The delta diff and commit: one line, no trailers.
5. The executor's public round-4 packet in `f1baaf7a.../review-evidence/400-403-r1/author-r5`: REVIEW-READY, HANDOFF, `regenerate.py`, the builder logs and the fixture-guard log.
6. Hosted check runs at this head.

My own measurements and verdict draft were written first. The prior review texts, R250-3 (5836646270) and R249-3 (5836791822), were read after that, to settle their findings. No review directory in the evidence tree was opened.

## Findings

No BLOCKER, MAJOR or MINOR.

### S1 (carried) - SUGGESTION - Tests, Conformance - `sw/builder/test_declarations.py:162-166`

This is the round-2 timer-profile suggestion: the profile is read from `KL_srp_top` defaults, not from the `u_srp` instance. Assignment 5836794096 moved it to #495. It is retained as SUGGESTION and does not affect coverage.

### R249 S1 (carried) - SUGGESTION - Conformance - `boot_policy.py` literals

This was moved to #495 by the same assignment. It is retained as SUGGESTION and does not affect coverage.

## Disposition of earlier public findings at this head

| Finding | Status | Evidence at `c6c65e80` |
|---|---|---|
| R250-3 N1 MINOR (Docs): builder comments at `:361-364` and `:403-407` describe the retired gates | **CLOSED** | See the N1 detail below the table. |
| R250-3 S2 SUGGESTION (Robustness): `assert` in the fixture generator | **CLOSED** | `tb/common/gen_declaration_fixture.py:45-46` now raises `ValueError` under the same condition. The retired assert line is absent at head (`receipts/vid-guard-probe.json`). |
| R250-3 S3 SUGGESTION (Docs): csr and pp_shadow Makefile banners | **CLOSED** | `csr/Makefile:5-25` lists all six default builds, which matches the `run` and `reset-bits` recipes. `pp_shadow/Makefile:22-27` lists `run-base`, `run-vid73` and `run-crf`. No check counts appear. |
| R249-3 S2 SUGGESTION (Docs, Tests): suite READMEs | **CLOSED** | See the README detail below the table. |
| R250-3 S1 and R249-3 S1 SUGGESTION | Retained, routed to #495 | No coverage effect. |
| R250-2 F1-F3 and R249-2 F1-F4 (closed at `e122f330` by R250-3 and R249-3) | **Remain CLOSED** | None of their artifacts is in this delta: `run_cases.py`, `milan_csr.sv`, `milan_datapath.sv`, MAAP_FABRIC, AREA_BUDGET, `milan_soc.py`, the milan_dp README and both harness `sim_main.cpp` files. `git diff --stat e122f330 c6c65e80 -- hdl protocol-processor gptp-processor external third_party configs sw/firmware` is empty, and both suites' `make -n` output is identical at both commits (`receipts/make-n-compare.txt`). |

**R250-3 N1 detail.**

- `endstation_builder.py:361-363` now says:
  - MAAP allocates destinations in every supported config.
  - Every declared talker requires `board.features.maap: true`.
  - Numeric `stream_dmac_base` values are legacy table/ABI scratch.
- `:438-439` now says only `promiscuous` is accepted, and that `board.features.rx_mac_filter` independently selects hardware presence.
- Both texts match the gates at `:3196-3201` (unconditional `maap: false` refusal) and `:3250-3255` (`hardware` refused), and they match ENDSTATION_BUILDER rows 30 and 39.
- "Every supported configuration declares talkers" is true: a config with no talkers is refused at `:1370` (`receipts/zero-talker-probe.txt`).
- `RX_ADDRESS_FILTERS` and the `stream_dmac_alloc` writes are removed, and both names are absent from the tree.
- `git grep "let it be pruned\|what both boards ship"` returns nothing (`receipts/gate-stale_text.log`).

**R249-3 S2 detail.**

- csr README `:15-42`:
  - The six-row table matches the recipes. Each row names the config whose `adp_shape_defaults.svh` it compiles.
  - The CSR-defaults header is the tracked one for every leg except the reset leg. Its content is identical across all five configs apart from the source-path banner (`receipts/csr-defaults-per-config.txt`).
  - `sim_live` and the check counts are gone.
- pp_shadow README `:4-7` and `:22-46`: the three targets, executables, fixtures and `-D` expectations match `Makefile:140-157`, and "371 checks" is gone. At head each leg reports 402 checks, which confirms that the quoted count had gone stale.

## What was measured

All measurements are at this head, except the before and after comparisons, which also ran at `e122f330`.

- **Byte-identical generation**, reproducing the executor's 61-file proof.
  - Method: `regen_compare.py` exports both commits with `git archive`, links the submodules read-only, and calls the real `endstation_builder.build()` for all five `configs/endstation_*.yaml`.
  - Output directories: 55 files and 571,739 bytes per commit, 0 differences.
  - Tracked copies: the build rewrote 6 tracked copies (5 `configs/generated/*/gen/adp_shape_defaults.svh` and `hdl/common/csr/gen/lwsrp_csr_defaults.svh`). Each came out byte-identical to the committed file at both commits.
  - The only tree differences are the 6 edited files. 55 + 6 = 61 matches the executor's count (`receipts/regen-compare.json`, `receipts/regen-rewritten-tracked-copies.txt`).
- **The removed `maap` branch.**
  - All five shipping configs carry a numeric `stream_dmac_base`, so the proof above never takes the branch that set `stream_dmac_alloc = "maap"`.
  - `probe_dmac_variants.py` built arty_current variants at both commits.
  - `maap`, `  MaAp `, numeric and `rx_mac_filter: false` produce byte-identical artifacts at both commits (14 files each). The normalized cfg differs only by the removed `srp.stream_dmac_alloc` key. The base value was `static` or `maap`, and no reader exists.
  - The `rx_mac_filter: false` variant really changes the build: `--no-rx-mac-filter` and `RXFILT_P=0` appear, with a promiscuous policy.
  - `maap: false` (numeric and dynamic), `rx_address_filter: hardware` (with and without the filter) and a unicast DMAC are refused at both commits with the same `ConfigError` (`receipts/dmac-variants-probe.json`, `receipts/dmac-variants-rxfilter-effect.txt`).
- **Fixture guard** (`probe_vid_guard.py`).
  - The old assert predicate and the new raise predicate were compared over 5,014 values, integers -5..5000 plus non-integers. They accept exactly the same set, with 0 mismatches.
  - Executed at head under normal and `-O` Python: VIDs 1, 73 and 4094 succeed, with headers byte-identical to the base script's apart from the per-run `Source :` banner line.
  - 2, 0, 4095, -1, `True`, `73.0`, `"73"` and `null` all exit with `ValueError` in both modes.
  - At base under `-O`, 5 of those (-1, 0, 2, 4095, `True`) were silently accepted. That is the robustness gain S2 asked for (`receipts/vid-guard-probe.json`).
- **Suites run cold** from a fresh export, with the 5.050 simulator (see Limits):
  - `make -C tb/verilator/csr`: exit 0 in 35 s. Six executables ran: 391/391/110/44/391/391 checks, 0 failures. The reset leg printed `declaration fixture: reset_bits.yaml` (`receipts/csr-cold-head.log`).
  - `make -C tb/verilator/pp_shadow`: exit 0 in 61 s. `run-base`, `run-vid73` and `run-crf` each reported 402 checks, 0 failures and no simulator warning. The startup VID word read `0x00030002`, `0x00030049` and `0x00030002` respectively (`receipts/pp-shadow-cold-head.log`).
- **Focused gates** (`run_gates.sh`, `receipts/gates-summary.txt`):
  - All exit 0: `test_declarations.py` (gate 40: 5 configs, 9 binding/reset mutants, 26 refusals), `check_py_idiom`, `docs_check` in git mode (clone) and no-git mode (plain export), `check_doc_style` and `check_doc_paths`.
  - Also exit 0: `measure_test_evidence --check`, `git diff --check e122f330 c6c65e80`, and the stale-text grep.
  - With the pinned renderer, also exit 0: `gen_toc --check` (107 pages), `gen_toc --verify-anchors` (171 links) and `check_em_dash --base 864b36f5` (0 findings over 121 added Markdown lines). The one em dash on an added line is the Contents label that mirrors the unchanged heading `## Time compression — and why ...`. CONTRIBUTING 6.1 exempts exactly that, and its separator was changed to `--`.
- **Executor's builder receipts at this head** (public packet `author-r5`, not re-run here):
  - `test_builder.py` in SDK mode: exit 0. One arm did not run: gate 11, because the calibration report is absent.
  - Compiler-absent mode: exit 0. Two arms did not run: gate 1b's RV32 census, and gate 11.
- **Hosted, at this head** (`receipts/hosted-check-runs.txt`, polled 2026-09-25T18:30Z). All jobs validate the merge ref `f7ecbc9f` = `c6c65e80` into `1299b461` (`receipts/hosted-merge-ref.txt`).
  - Succeeded: `rtl-fast`, `changes`, `docs-check-no-git`, `elaborate`, `verilator-lint`, `yosys-elaboration`, Yosys shards 0-3, Verilator shards 0, 2 and 3, `bdd-conformance`, `wire-accountability` and `full-ci-gate`.
  - `Physical gPTP` was skipped by schedule, which is not a result.
  - Verilator shards 1/5 and 4/5 were in progress.
  - **`docs-check` failed** at step 29, "Capture measurement census and clock gate": `FAIL: product firmware changed; remeasure the copy` (`receipts/hosted-docs-check-108193046684.log`). Steps 30-51 were skipped, so the hosted Python-idiom, doc-path, contents and shape gates did not run on the candidate.
  - Cause (`receipts/merge-ref-firmware-pin.txt`): dev's `tb/verilator/nvm_capture_cpu/measurements.json` pins `milan_baremetal.c` at `7cdc5e68…`, which is the digest at this PR's base `864b36f5`. This PR's firmware is `0bf43cd4…`. The gate was introduced on dev by `31808e65` and is absent at this head. This delta does not touch the firmware. So the conflict is between the PR as a whole and dev's newer gate, not a defect in `e122f330..c6c65e80`.

## Clean-lens evidence (same fields as a finding)

- `[R250] PASS Conformance` — `sw/builder/endstation_builder.py:361-363,438-440,1969-1976` against ENDSTATION_BUILDER rows 30 and 39, README-parameters:71 and the gates at `:3196-3201` and `:3250-3255`.
  - The comments state the shipped contract.
  - The dead-code removal changes no generated artifact for any shipping config, and none for the `maap` spelling that shipping configs do not exercise.
  - Every refusal is unchanged.
  - Receipts: regen-compare, dmac-variants-probe, zero-talker-probe.
- `[R250] PASS RTL` — the delta against `hdl/`, the gitlinks, `configs/` and every generated RTL input.
  - No RTL, submodule or config byte changed (empty `git diff --stat`, identical gitlinks).
  - All 6 generated headers that RTL includes are byte-identical at both commits.
  - The csr and pp_shadow RTL suites pass cold at head.
  - Functional RTL scope is therefore exactly what R250-3 covered clean at the ancestor `e122f330`. Nothing in RTL scope has touched it since.
- `[R250] PASS Robustness` — `tb/common/gen_declaration_fixture.py:45-46` and the builder refusal paths.
  - The guard now fails closed under `-O`, where the old assert was stripped.
  - The accepted set is identical, and a bad VID gives a non-zero exit.
  - Refusals for `maap: false`, `hardware` and unicast DMACs are unchanged at both commits.
  - Receipts: vid-guard-probe, dmac-variants-probe.
- `[R250] PASS Tests` — the `tb/verilator/csr/Makefile` and `tb/verilator/pp_shadow/Makefile` recipes, the default targets, `test_declarations.py` and the fixture generator.
  - Recipe output is identical at both commits (`make -n`), so the delta weakens no test.
  - Default targets were green cold at head: 6 csr legs and 3 pp_shadow legs.
  - `test_declarations` is green.
  - The fixture legs still discriminate: the VID 73 leg reads `0x00030049` while the base leg reads `0x00030002`.
- `[R250] PASS Docs` — the csr README `:15-42,79-81`, the pp_shadow README `:4-46`, both Makefile banners, and the builder comments, checked against the recipes, `make -n` and ENDSTATION_BUILDER rows 30 and 39.
  - No check counts appear, and no stale harness is named.
  - The doc gates pass, and the em dash is used only in the exempt mirrored label.
  - The commit is one line with no trailers.

## Completion ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | builder comments and `_srp_dmac` against ENDSTATION_BUILDER rows 30/39, README-parameters:71, gates `:3196-3201`, `:3250-3255`; 61-file regeneration; 9 variant builds | R250-4 | c6c65e803f9eb270a11dfd65fda5814fb0b0ea55 |
| RTL | CLEAN | empty RTL, submodule and config diff; 6 byte-identical generated RTL headers; csr and pp_shadow cold runs; functional RTL covered by R250-3 at ancestor e122f330, untouched since | R250-4 | c6c65e803f9eb270a11dfd65fda5814fb0b0ea55 |
| Robustness | CLEAN | `gen_declaration_fixture.py:45-46` (5,014-value predicate equivalence, 44 normal and `-O` executions); builder refusal variants | R250-4 | c6c65e803f9eb270a11dfd65fda5814fb0b0ea55 |
| Tests | CLEAN | `make -n` equivalence of both suites; cold default targets (6 + 3 legs); `test_declarations.py`; the executor's builder receipts at head | R250-4 | c6c65e803f9eb270a11dfd65fda5814fb0b0ea55 |
| Docs | CLEAN | csr and pp_shadow READMEs and banners against the recipes; builder comments; doc, TOC, anchor, em-dash and path gates | R250-4 | c6c65e803f9eb270a11dfd65fda5814fb0b0ea55 |

## Limits

- **Tool substitution.** The designated `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist. I used this lane's manager wrapper `$VALIDATION_STORAGE/400-403-manager-r4/pinned-tool-bin/verilator` instead.
  - It reports `Verilator 5.050 2026-07-01 rev v5.050`.
  - The wrapper and wrapped-binary digests are in `receipts/tool-identity.txt`.
  - The system 5.052 simulator was not used.
- **Job cap.** The recipes hard-code `--build -j 0`. Both suite runs were confined to 8 CPUs with `taskset -c 0-7`. The simulator's internal compile job count was not logged, so on this 16-CPU host more than 8 compile processes may have shared those 8 CPUs.
- **Doc renderer.** The system interpreter lacks the pinned renderer. `gen_toc` and `check_em_dash` were rerun with an existing interpreter whose `cmarkgfm`, `html5lib`, `six` and `webencodings` versions equal `tools/markdown/requirements.txt` (`receipts/md-venv-freeze.txt`). Package hashes were not re-verified.
- **Not run here**, per the brief:
  - `test_builder.py` in either mode; for these I rely on the executor's public at-head receipts (`author-r5/builder-sdk.log`, `builder-absent.log`).
  - The firmware self-test, behave, milan_dp, nvm_cosim, the full parent, PP, gPTP, Yosys and builder banks, act and host act_ci.
- **Manager bank evidence.** I found no manager-authored bank receipt for this head in the named evidence tree, only the executor's `author-r5` packet. The manager's reported banks are not independently verified here.
- **Hosted.** Shards 1/5 and 4/5, `verilator-suites` and `yosys-portability` had not completed at the last poll. `docs-check` failed on the merge ref, as described above.
- Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Clone integrity after all probes** (`receipts/clone-integrity.txt`):
  - HEAD and tree are exact, the index equals HEAD, and status is clean, including untracked files.
  - 896 tracked blobs match byte for byte and mode for mode.
  - Gitlinks `gptp-processor e5dcea6e`, `protocol-processor 990f9652` and `verilog-axis 48ff7a7e` are checked out at their recorded commits with clean worktrees. `external` is not checked out.
  - All builds and probes ran in `git archive` exports under the packet's scratch directory.

## Pending manager duties

1. **Merge-blocking, candidate only:** the current-dev candidate fails hosted `docs-check` at `scripts/check_nvm_capture.py`.
   - The PR's `milan_baremetal.c` no longer matches `product_firmware_sha256` in dev's `tb/verilator/nvm_capture_cpu/measurements.json`.
   - Before merge, the candidate must carry a capture re-measurement for the new firmware, as the gate demands, with a public decision on which lane owns it.
   - Then `docs-check`, including its skipped steps 30-51, must be green on the candidate.
   - This gate was not on dev `5c78ce2e`, which R250-3's hosted runs used.
2. Confirm hosted Verilator shards 1/5 (pp_shadow, nvm_cosim) and 4/5 (milan_dp), and the `verilator-suites` and `yosys-portability` aggregates, on the exact candidate.
3. Still owed: the final current-dev candidate validation (base `864b36f5`, live dev `1299b461`), trusted act, maintainer merge authorization and post-merge containment.
4. #495 keeps R250 S1 (timer instance) and R249 S1 (`boot_policy` literals).

R250-4 FINISHED
