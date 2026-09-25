[R250] NEGATIVE - exact head e122f3302cf8a8e89de960233a8638b9dd1387dc

# R250-3: external independent review of PR #566 (issues #400 and #403), round 3

- Head `e122f3302cf8a8e89de960233a8638b9dd1387dc`, tree `59497ea361687e8d49e468bc884f220a418680b5`. This is two commits on `7463ab08`: `de36e514` and `e122f330`.
- This is a delta review. R250-2 covered `7463ab08` in full. This round judges `7463ab08..e122f330` (17 files) and rechecks every earlier public finding at this head.
- All five lenses were applied: Conformance, RTL, Robustness, Tests and Docs.
- Every round-2 finding answered by the round-3 assignment is **closed** at this head: R250 F1, F2 and F3, and R249 F1 through F4.
- The verdict is still NEGATIVE because of one new MINOR finding, under Docs. Two builder comments still describe gates this PR retired. The same stale text was already present at `7463ab08`, and both round-2 reviews missed it.

## Reconstruction

The review was rebuilt from public state only, in this order:

1. AGENTS.md, CONTRIBUTING.md and docs/README.md.
2. The #400 body and every comment on it: decisions 5729726367 and 5770922734, assignment 5781042070, owner decision 5789766951, resume order 5831927176, round-2 order 5832912970 and the round-3 assignment 5834690477 (the F2 durable-option decision). Also the author's REVIEW READY 5836209846.
3. `docs/testing/CI_WORKFLOWS.md` (suite budgets), `scripts/run_all_suites.sh`, `scripts/suite_shards.py`, `.github/workflows/rtl.yml` and `docs/reference/REGISTER_MAP.md` rows `0x654`, `0x680`, `0x684` and `0x6CC`.
4. The delta diff and both commits, then the public evidence tree `a94b8b81.../review-evidence/400-403-r1` (directory listing only) and the hosted runs at this head.

An independent verdict draft was written before any prior review text was read. Prior findings were read after that: R250-2 (5834684851) and R249-2 (5834667344). No other reviewer's round-3 text was read.

## Findings

### N1 - MINOR - Docs - `sw/builder/endstation_builder.py:361-364` and `:403-407`: builder comments still describe the two gates this PR retired

- **Authority and evidence:**
  - AGENTS.md section 6, Docs, requires changed contracts to be reflected in the docs. CONTRIBUTING section 5 asks that touched code be left at least as clear as it was.
  - The round-3 assignment (5834690477, item 3) corrected this same class of text in `milan_datapath.sv:274-275` and `:301-302`. The same stale text survives in the builder, directly beside the constants and gates this PR changed (receipts `41-rx-posture-residue.txt` and `44-retired-gate-comment-residue.txt`).
  - **`:361-364`** says `stream_dmac_base: maap` "is the only value that forbids `board.features.maap: false`". At base `864b36f5` that was true, because the gate at `:3165` keyed on `stream_dmac_alloc == SRP_DMAC_DYNAMIC`. This PR replaced that gate with an unconditional refusal (`:3208-3214`, "removes the allocator required by every declared talker"). So every configuration now forbids it.
  - **`:403-407`** says "`hardware` (the default, and what both boards ship) REQUIRES rx_mac_filter; the other two are the honest declarations that let it be pruned". This PR changed the constant under that comment from `("hardware", "promiscuous")` to `("promiscuous",)`. It now refuses `hardware` (`:3262-3267`), and presence is independent of the posture (`:3225`). The PLATFORM default is `promiscuous` (`:446`), there is only one value, and nothing reads `RX_ADDRESS_FILTERS` any more.
  - Both texts contradict ENDSTATION_BUILDER row 30, README-parameters line 71, AREA_BUDGET line 41 and the RTL banners this round corrected.
  - Both comments are unchanged since `7463ab08`, so R250-2 should have reported them. They are raised now rather than left in the tree.
- **Impact:** a cold reader of the builder, the one source of these declarations, is told that a static-address config may prune MAAP, and that `hardware` is the shipped RX posture that requires the filter. Neither is true. This is the declaration drift #400 and #403 exist to remove, and it sits beside the code a future editor would change.
- **Required outcome:** both comments state the shipped contract, or are removed. That contract is:
  - MAAP is required for every supported configuration, and numeric `stream_dmac_base` is legacy scratch.
  - Only `promiscuous` is accepted, and `board.features.rx_mac_filter` independently selects hardware presence.

  Optionally, the now-unread `RX_ADDRESS_FILTERS` constant and `srp["stream_dmac_alloc"]` normalization (`:1983-1986`, no reader) can go at the same time. No behaviour change is needed.
- **Verification:**
  - Reread `:361-364` and `:403-407` at the new head.
  - `git grep -n "let it be pruned\|what both boards ship"` returns nothing.
  - No builder comment says a single `stream_dmac_base` value forbids `maap: false`.
  - `check_py_idiom` and the builder and declarations gates stay green.

### S1 (carried) - SUGGESTION - Tests, Conformance - `sw/builder/test_declarations.py:162-166`

This is the round-2 suggestion that the timer profile is read from `KL_srp_top` defaults only, not from the `u_srp` instance. The assignment moved it to #495, and it is not addressed at this head. As a SUGGESTION it does not affect coverage.

### S2 - SUGGESTION - Robustness - `tb/common/gen_declaration_fixture.py:45`

The emitter-VID guard is an `assert`, and `python3 -O` would strip it. The recipes do not use `-O`, so the guard works today. An explicit `raise` would keep it under any interpreter flags.

### S3 - SUGGESTION - Docs - `tb/verilator/csr/Makefile:4-35` and `tb/verilator/pp_shadow/Makefile:22`

The csr banner still says "Three executables" and "build and run all three". Before this round the default target already ran five binaries, and it now runs six. The pp_shadow banner says "the self-checking harness", but the default target now runs three builds. The new legs are documented next to their own rules (`csr/Makefile:136-137`, `pp_shadow/Makefile:140-142`), so this is optional.

## Disposition of earlier public findings at this head

| Finding | Status | Evidence at `e122f330` |
|---|---|---|
| R250-2 F1 BLOCKER (nvm_cosim `constants_header` caller) | **CLOSED** | `run_cases.py:110,132` now calls `ref.constants_header(shp, donor, ref.fabric_constants(overlay, lwsrp))`. The repository-wide census, submodules included, finds three `constants_header` references: the definition and two callers, both passing the shared derivation (`30-caller-census.txt`). `make quick`: 315/315 PASS, exit 0 (`31-nvm_cosim-quick.txt`). The full `make` target, both shapes: 465/465 PASS, 39/39 named mutants killed, exit 0 (`32-nvm_cosim-full.txt`). Hosted `Verilator shard 1/5` was still in progress when this report was written. |
| R250-2 F2 MINOR (fixture legs not committed) | **CLOSED** | The default targets run the committed recipes: `run-vid73`, `run-crf` and `reset-bits` (`10-pp_shadow-default-clean.txt`: three runs of 402 checks, 0 failures; `12-csr-default-clean.txt`: the reset leg reads `0x13` with both outputs at 1). Mutants were rerun against the **default** targets. R1-equivalent M1 (`milan_datapath.sv:7410`), M2 (`KL_pp_shadow.sv:1056`), M8 (`protocol_processor_top.sv:2226`) and R7b as M9 (`KL_srp_top.sv:341`) each fail with 3 VID checks, 2 against 73, exit 2. The reset mask M3 (`milan_csr.sv:1551`) fails both admission outputs, exit 2 (receipts 20-22, 27, 29). |
| R250-2 F3 MINOR items 1-5 | **CLOSED** | `milan_csr.sv:1542-1550` matches `AAF_CTRL_RST_C`/`MAAP_CTRL_RST_C = 0` (`:1207-1208`) and `LWSRP_VID_RST_C = 2`. `MAAP_FABRIC.md:83-84,151` matches REGISTER_MAP `0x6CC` and `boot_policy.py` `MILAN_MAAP_CTRL_BOOT = len(stream_outputs)<<8 \| 1`. `AREA_BUDGET.md:41`, the `milan_soc.py:3464-3468` help text and `milan_datapath.sv:274-275` match the builder's `:3210` refusal. `milan_datapath.sv:299-301` matches `:3225` and `:3262`. The milan_dp README `:683-684` and `sim_main.cpp:1330` name `ADP_STROUT_PRES_NS_C`, which is the fold at `milan_datapath.sv:3260-3266`. `git grep PRES_DFLT_C` returns nothing (receipts 40, 42). |
| R249-2 F1 BLOCKER | **CLOSED** | As for R250-2 F1. |
| R249-2 F2 MINOR (incl. the two misleading harness comments) | **CLOSED** | R249 receipts 41, 43 and 35 are my M2, M1 and M3, and all three are detected by the default targets (above). `pp_shadow/sim_main.cpp:625-626` and `csr/sim_main.cpp:103-104,750` now describe the committed recipes. |
| R249-2 F3 MINOR | **CLOSED** | `git grep "bypass=1\|rx_address_filter" -- hdl` returns nothing. The comments are as above. |
| R249-2 F4 MINOR | **CLOSED** | Row count: base said "66 rows" over 67 table rows (off by one). The head says "71 rows" over 71 rows, ids 0 through 44 with suffixes (`42-docs-f3f4-checks.txt`). The other items are as above. |
| R250-2 S1 / R249-2 S1 | Out of scope, moved to #495 | SUGGESTION, no coverage effect. |

## What was measured

- **Clean default targets, from `make clean`:**
  - `make -C tb/verilator/pp_shadow`: exit 0 in 51.6 s. `run-base`, `run-vid73` and `run-crf` each report 402 checks with 0 failures (receipt 10).
  - `make -C tb/verilator/csr`: exit 0 in 35.6 s. Five existing binaries plus the reset leg: 391/391/110/44/391/391 (receipt 12).
  - Both are far inside the unchanged 1800 s budget (`CI_WORKFLOWS.md:158`, `run_all_suites.sh:243-249`). They agree with the author's 52.7 s and 35.1 s.
- **Header provenance:** Verilator `__ver.d` files show each leg compiled its own `obj_*/fixture/gen/*.svh`. The base leg compiled `configs/generated/endstation_arty_current` plus `hdl/common/csr/gen` (receipt 11).
  - VID73 fixture headers equal the tracked arty_current headers **except** `ADP_SRP_DOM_DEF_VID_C` and `LWSRP_VID_RST_C` (and the `Source:` comment).
  - The CRF fixture changes only the shape rows its override implies.
  - The reset fixture changes only `LWSRP_CTRL_RST_C` from `0x10` to `0x13`.
- **The generator and the VID injection:**
  - `gen_declaration_fixture.py` merges the committed overrides, then runs the real `endstation_builder.load_config()` (full validation) and the same `emit_adp_shape_svh`/`emit_csr_defaults_svh` that `_derive_artifacts` (`:5569-5572`) uses. Nothing is edited by hand.
  - The non-shipping VID is set on the **normalized** config after validation. Both emitters read `cfg["srp"]["vid"]` raw (`:2166`, `:2913`), and no validated field derives from it (`:1930-1935` only checks it).
  - So the injection bypasses exactly one thing: the shipping rule `vid == 2`. A defect there, or in config-to-normalized plumbing of `srp.vid`, is not this leg's claim. The builder's own gates cover it (`test_declarations.py` refusals and header mutants, all green per the manager's evidence).
  - The injection therefore cannot mask an emitter or binding defect. Dropping it (M5) turns the default target red with the three VID checks.
- **Fixture-input mutants:**
  - CRF output disabled in `crf_on.yaml` (M6): 3 failures.
  - `talker_declare_at_reset: false` in `reset_bits.yaml` (M7): 3 failures.
  - CRF source removed from `cfg_src_en_i` (M4b): 2 failures in `run-crf` only, while `run-base` and `run-vid73` pass. This shows the CRF leg adds detection that the one-output legs cannot provide.
  - M4 (`KL_pp_maap_shim.N_SRC_P` minus 1) survives. It is an equivalent mutant for the graded path: grants are bounded by `blk_count_i` (`KL_pp_maap_shim.sv:183`), the port width is 1 bit either way (`:148`), and `N_SRC_P` sizes only the conflict-pending vector (`:243`). No finding.
- **RTL delta:** a comment-stripping token comparison shows that `milan_csr.sv` and `milan_datapath.sv` are **comment-only** changes in `7463ab08..e122f330`. The same checker reports code changes over `864b36f5..e122f330`, which shows it can fail (receipt 43).
- **Focused static gates:**
  - `check_em_dash --base 864b36f5`: 0 findings over 57 added lines.
  - `check_doc_style`: OK.
  - `check_cpp_idiom`: every `-CFLAGS` group carries `-Wall -Wextra`, and "build without warnings" is 0 against a ratchet of 0.
  - `check_py_idiom`: all ratchets hold.
  - All exit 0 (receipt 50).
- **Hosted, at this head** (receipt 60). Every hosted job validates the merge ref `cbcfd172`, which is this head merged into dev `5c78ce2e`, not the source head alone.
  - Succeeded: `rtl-fast`, `docs-check`, `docs-check-no-git`, `elaborate`, `verilator-lint`, `yosys-elaboration`, Yosys shards 0-3, Verilator shards 0, 2 and 3, `bdd-conformance`, `wire-accountability` and `full-ci-gate`.
  - Shard 3 ran `csr` including the new reset leg (`0x13`, both outputs 1).
  - Verilator shard 1/5 (which owns `pp_shadow` and `nvm_cosim`) and shard 4/5 (`milan_dp`) were **in progress**. The `verilator-suites` aggregate had not reported.
  - `Physical gPTP` was skipped by schedule, which is not a result.
  - Hosted `csr` binaries report 400 checks against 391 locally. The 9 extra checks (`RENDER_STAT`, `0x8E0` and `0x8F4`) exist on dev (12 occurrences) and not at this head (0), so the difference is the merge ref, not a defect.

## Clean-lens evidence (same fields as a finding)

- `[R250] PASS Conformance` for `tb/verilator/pp_shadow/Makefile:134-153`, `fixtures/{vid73,crf_on}.yaml`, `tb/verilator/csr/Makefile:126-142`, `fixtures/reset_bits.yaml`, `tb/common/gen_declaration_fixture.py`, `run_cases.py:110,132` and `boot_policy.py:35-65`, checked against decision 5770922734 and assignment 5834690477.
  - Checked: the proof of each generated-VID hop, the live reset bits apart from the firmware boot policy, and the exact CRF-inclusive allocation. These now run as committed default-target recipes, with headers produced by the builder from committed fixture configs.
  - Checked: the saved-state co-simulation and host test share `fabric_constants()`.
  - Receipts 10-12, 20-32.
- `[R250] PASS RTL` for `hdl/common/csr/milan_csr.sv` and `hdl/milan/milan_datapath.sv` in `7463ab08..e122f330`.
  - Checked: the changes are comment-only (receipt 43). RTL-functional scope is therefore unchanged since R250-2's clean RTL coverage at `7463ab08`, an ancestor that nothing RTL-functional has touched since.
  - Checked: the parent, wrapper, donor-top and donor-child binding hops were mutated at this head and detected (M1, M2, M8, M9), and the reset flop mask was detected (M3).
- `[R250] PASS Robustness` for `gen_declaration_fixture.py` and the three new recipes.
  - Fail-closed: an unknown key or invalid config raises in `load_config`, a bad VID trips the guard, and any non-zero exit stops `make`.
  - The headers are regenerated on every run (phony targets). Each leg uses its own `--Mdir`. The build directories match `.gitignore:98`, and the default targets leave no tracked change (receipt 90).
  - Include-path precedence was proven per leg (receipt 11). Hosted runs invoke `make` serially (`run_all_suites.sh:390`), so the three pp_shadow legs cannot race.
  - Suggestion S2 only.
- `[R250] PASS Tests` for the default `pp_shadow`, `csr` and `nvm_cosim` targets at this head.
  - Nine source and fixture mutants were each detected by a default target (M1-M3, M4b, M5-M9). One equivalent mutant was explained (M4).
  - nvm_cosim: quick 315/315, full 465/465 with 39/39 mutants killed.
  - Hosted shard 3 ran the new csr leg.
  - Receipts 10, 12, 20-32 and 60.
- `[R250] UNCLEAN Docs` because of N1 (`endstation_builder.py:361-364,403-407`). All five round-2 Docs items are correct at this head (receipts 40 and 42). So are REGISTER_MAP `0x654/0x680/0x684/0x6CC`, the ENDSTATION_BUILDER count of 71 and the harness comments.

## Completion ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | new pp_shadow/csr recipes and fixtures; generator; run_cases.py/boot_policy.py; decisions 5770922734, 5834690477; receipts 10-12, 20-32 | R250-3 | e122f3302cf8a8e89de960233a8638b9dd1387dc |
| RTL | CLEAN | milan_csr.sv and milan_datapath.sv delta (comment-only, receipt 43); binding-hop and reset mutants M1-M3, M8, M9 at this head; functional RTL covered by R250-2 at ancestor 7463ab08, unchanged since | R250-3 | e122f3302cf8a8e89de960233a8638b9dd1387dc |
| Robustness | CLEAN | gen_declaration_fixture.py; recipe determinism and isolation; include precedence (receipt 11); .gitignore; serial hosted invocation | R250-3 | e122f3302cf8a8e89de960233a8638b9dd1387dc |
| Tests | CLEAN | default pp_shadow/csr/nvm_cosim targets; mutants M1-M9 incl. M4b; hosted shard 3 csr log | R250-3 | e122f3302cf8a8e89de960233a8638b9dd1387dc |
| Docs | UNCLEAN (N1 MINOR) | milan_csr/milan_datapath banners, MAAP_FABRIC, AREA_BUDGET, milan_soc help, milan_dp README/sim_main, ENDSTATION_BUILDER count, harness comments, endstation_builder.py comments | R250-3 | e122f3302cf8a8e89de960233a8638b9dd1387dc |

## Limits

- **Tool substitution:** the assigned `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist. I used this lane's manager wrapper `$VALIDATION_STORAGE/400-403-manager-r3/pinned-tool-bin/verilator` instead. It reports `Verilator 5.050 2026-07-01 rev v5.050`, and its wrapper and binary digests are recorded in receipt 00. g++ 16.2.1 and Python 3.14.7 were also used.
- **Job-cap deviation, disclosed:**
  - The recipes hard-code `--build -j 0`. Receipts 10, 12 and 20-28 ran as committed, so their C++ compiles used up to 16 jobs on this 16-core host, above the 8-job cap. Wall clocks were measured under the same condition as the author's.
  - nvm_cosim ran with `JOBS=8 POOL=8`, and its two builds may have overlapped.
  - Receipt 29 (M9) was capped at 8 with `scripts/verilator_cap8.sh`, self-tested in receipt 01.
  - No other deviation.
- **Not run, per the brief:** the full parent, PP, gPTP, Yosys and builder banks; `test_builder.py`, `test_declarations.py` and the firmware self-test; behave; the milan_dp recipe; the `run_all_suites.sh` sweep; the OOC area; act; host act_ci. For these I rely on the manager's reported source banks at this head. They are not independently verified here.
- The hosted Verilator shards 1/5 and 4/5 and the `verilator-suites` aggregate were still running at the final poll (2026-09-25T17:28Z).
- Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Clone integrity after all probes** (receipt 90):
  - HEAD and tree are exact, and the index equals the HEAD tree.
  - 896 tracked files match byte for byte and mode for mode.
  - Gitlinks match with clean worktrees: `gptp-processor e5dcea6e`, `protocol-processor 990f9652` and `verilog-axis 48ff7a7e`, with 103, 246 and 213 files byte-exact. `external` is not checked out.
  - Each mutant restore was sha256-verified (receipts 20-29).

## Pending manager duties

- Confirm hosted `Verilator shard 1/5` (pp_shadow and nvm_cosim), `4/5` (milan_dp), and the `verilator-suites` and `yosys-portability` aggregates at this head. Record that the hosted jobs validate the merge ref `cbcfd172`.
- Still owed: the final current-dev candidate (live dev `5c78ce2e`), trusted act, maintainer merge authorization and post-merge containment.
- After N1 is fixed, re-review the Docs lens at the new head, plus any lens whose scope the fix touches. A comment-only builder change touches Docs only.

R250-3 FINISHED
