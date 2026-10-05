[A537]

## Contents

- [Status](#status)
- [Linked Issue / roles](#linked-issue--roles)
- [Description](#description)
- [Authoritative references](#authoritative-references)
- [How to get into the same state](#how-to-get-into-the-same-state)
- [How to validate](#how-to-validate)
- [Known limitations / out of scope](#known-limitations--out-of-scope)
- [Definition of Done](#definition-of-done)

## Status

Round 2 author validation complete at `3880c1eb6e2f927a07f98150d5b05a228f8f4efd`, `661-pp-pin-ead80360` -> `dev`.
Round 2 answers R486-1 and R487-1. It fixes R487-1 F1 (the `available_index` rule after the pin) and merges dev `fa450d30` (#652 and #656) with `--no-ff`. R486-1 F1, F2 and R1 were already fixed in this body at round 1's head.
With #656's pacing fix merged, the physical gPTP leg now passes, and its exception is retired. The #657 render campaign remains the one authorized dev exception. Skipped arms are disclosed below; hosted checks and independent review remain pending.

## Linked Issue / roles

Closes #661
Closes #639
Closes #234
Relates to #629
Relates to #229

Executor: `[A537]`
Internal cleared-context reviewer: `[R486]`
External reviewer: `[R487]`

## Description

Adopts processor `ead8036035affd53ef4b29979190f2f4f67084c0` from `631eeb342ca1e3fa80e734077a56a943aee76ff1` on dev `506d91db`, merged with dev `fa450d30`.
This brings in wave 2, P1/P2, C10, #85, the three area lanes #232/#230/#639, and #81/#84.

| Change | Result |
|---|---|
| Four supplied adaptations | C8 waiver propagation, P1/P2 saved-state contracts, complete 42-top synthesis inventory and retired xvlog findings; one commit per concern |
| Required cleanup | Processor lint owns L6/L10; parent tests exercise it through both image emitters. REGISTER_MAP 0x644 says available_index resets after departing |
| Pin-derived records | ROM digest ledger, submodule inventory and boundary diagram, port budget and DUT-reader dispositions; naming generator produces no change |
| Resource baseline | Three measurements recorded through the generator, with policy unchanged and per-block deltas against C |
| Round 2: `available_index` (R487-1 F1) | The adopted rule (IEEE 1722.1-2021 Section 6.2.2.15) is now stated in the saved-state page, the compliance matrix and the image packer and builder comments. `wt.adp.available-index-advances` accepts the reset to 0 after an ENTITY_DEPARTING and still refuses any other repeat, with self-test arms for each case |
| Round 2: dev merge | `--no-ff` merge of dev `fa450d30`. Its only RTL is an elaboration-time guard constant in `KL_nvm_backend.sv`. Source lists, builder outputs and the resource gate's other inputs are unchanged, so there was no re-route |

The route uses 50,318 LUT, 54,214 FF, 15,789 slices and 87.5 BRAM tiles.
It saves 449 LUT, 5,420 FF, 43 slices and five RAMB36s against C, leaving 61 slices free.
All 100,970 routable nets are fully routed, with zero routing errors; WNS/WHS is +0.108/+0.036 ns at 50 MHz.
Standalone 1x1 uses 23,178 LUT / 19,776 FF; 8x8 uses 29,853 / 27,370.
The authoritative baseline explains the notification, SRP and queue mappings alongside P1/P2 growth and cites the processor PRs' measured deltas.

The large payload flop banks identified by #234 criterion 2 now map to RAM.
The [manager's remaining-criteria record](https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5974629836) leaves only that criterion, so this adoption closes #234 as well as #639's remaining re-baseline obligation.
The 60 percent LUT target remains assigned to #640; this image is still 12,278 LUT above it.

The processor top gains only `NVM_MEM_TMO_CYC_P = CLK_HZ_P`; its 212 ports are unchanged and the parent keeps the default.
P2 reports bounded errors while retaining device debt until the terminal or reset.
P1 persists names inside the processor; the parent's existing sticky name pending transfer and map persistence remain separately owned work under #637.
`docs/reference/SUBMODULES.md` contains the complete parent-visible list.

Saved-state census, firmware digest and clocks equal the retained receipt.
`check_nvm_capture.py` passes; the 8x8 maximum remains 13.86484 ms, below 24.5 ms, so no capture re-measurement was required.

**`available_index` (R487-1 F1).** The adopted processor increments `available_index` after each ENTITY_AVAILABLE and resets it to 0 after an ENTITY_DEPARTING, which carries the pre-reset value. The saved-state page, the compliance matrix, the `UNBAKED_SPANS` comment in `avdecc/gen_aemi_image.py` and the matching builder test comment now say so, citing Section 6.2.2.15. The builder test comment is a fifth stale statement of the same rule, found by R487-1's verification grep. The matrix drops its "divergence stays recorded" sentence, because processor PR #152 removed the divergence.
The wire-truth check now exempts exactly one repeat: an index of 0 on the ADPDU after an ENTITY_DEPARTING. R487-1's probe (DEP 0, AVAIL 0, 1) passes. A repeat between two ENTITY_AVAILABLEs fails, including straight after a reset.
Four self-test arms cover the change. Three planted defects in the exemption are each caught by the new test.

**Dev merge.** The merge commit's tree equals `git merge-tree --write-tree` of its two parents. The only RTL change replaces the literal 128 in `KL_nvm_backend.sv`'s elaboration-time `g_refuse_names` guard with `N_NAME_MAX_C`.
Per recorded endpoint, the resource gate's own input digest at the merge head differs from the recorded one only through that file. Restoring it to its measured bytes reproduces all three recorded `inputs_sha256` values exactly.
Every builder output and packed image is byte-identical for all five configurations at round 1's head, before the merge and at the merge head. `sw/litex/milan_soc.py` and the submodule pins are unchanged.

## Authoritative references

- [#661 assignment](https://github.com/kebag-logic/milan-fpga/issues/661#issuecomment-5986065259), the [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/661#issuecomment-5991877761), and processor PRs #143 through #157, including their parent-visible sections.
- R486-1 ([5991604022](https://github.com/kebag-logic/milan-fpga/pull/663#issuecomment-5991604022)) and R487-1 ([5991869908](https://github.com/kebag-logic/milan-fpga/pull/663#issuecomment-5991869908)).
- `CONTRIBUTING.md`, `docs/development/CODE_QUALITY.md`, `docs/reference/SUBMODULES.md` and `syn/yosys/README.md`.
- `docs/design/SAVED_STATE_MATERIALIZATION.md`, `docs/design/SAVED_STATE_FASTCONNECT.md`, `docs/reference/REGISTER_MAP.md` and `docs/reference/MILAN_COMPLIANCE_MATRIX.md`.
- IEEE 1722.1-2021 Section 6.2.2.15, as the processor states it in `hdl/adp/KL_adp_engine.sv` and `tb/adp_engine/README.md` at `ead80360`.
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, `docs/findings/234_PP_SHADOW_AREA_BASELINE.md` and `docs/design/AREA_BUDGET.md` (#638's method and unchanged policy).
- NFR-RES-01 and the owner's #640 redesign decision; #635's adoption method in PR #636.

## How to get into the same state

The branch is published as `661-pp-pin-ead80360`. From a clone of this repository:

```sh
git fetch origin 661-pp-pin-ead80360 && git switch --detach FETCH_HEAD
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
git rev-parse HEAD
git submodule status
export VERILATOR=$VALIDATION_TOOLS/verilator-5.050/verilator
export PATH=$VALIDATION_TOOLS/md-venv/bin:$VALIDATION_TOOLS/verilator-5.050:$VALIDATION_TOOLS/sv2v-0.0.12/bin:$PATH
export DOCS_MAKE_BIN=$VALIDATION_TOOLS/make-4.3/bin
"$DOCS_MAKE_BIN/make" --version
```

Expected head: `3880c1eb6e2f927a07f98150d5b05a228f8f4efd`. Expected processor pin: `ead8036035affd53ef4b29979190f2f4f67084c0`, clean.
Use the pinned Markdown Python environment and GNU Make 4.3 for the docs workflow.
The recorded local make prefix was built from the GNU 4.3 release; the version line must read `GNU Make 4.3`.
Synthesis requires Yosys 0.66 with its bundled ABC revision `5d51a5e420f5de493d07bf61109a977248c86ffb` and sv2v 0.0.12, as specified in `syn/yosys/README.md`.
The local canonical run selected that ABC revision as the `abc` binary seen by Yosys (the system package has a different revision) and ran the full synthesis and fresh cache controls from this worktree; the selector's digest is recorded in `tool-versions.json`. With a distribution that already bundles the required ABC, use `syn/yosys/run.sh` directly.
The image and standalone measurements reproduce with the repository baseline recipe under the Vivado lock.

## How to validate

```sh
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
python3 scripts/check_rtl_source_lists.py
python3 scripts/check_rtl_source_lists.py --selftest
python3 scripts/pp_srcs.py --check --selftest
python3 scripts/check_port_contracts.py
python3 scripts/measure_naming.py --check
python3 scripts/measure_test_evidence.py --check
python3 scripts/docs_check.py
flock "$VIVADO_LOCK" python3 scripts/xvlog_gate.py --check
PATH="$DOCS_MAKE_BIN:$PATH" python3 sw/builder/test_builder.py --require-rv32
python3 scripts/lint_rtl.py --check --self-test
(cd tb/tools && python3 avtp_wire_truth.py --self-test)
(cd tests && behave --no-capture -f plain)
make -C tb/verilator/pp_shadow -j16 VERILATOR_JOBS=2
make -C tb/verilator/nvm_cosim -j16 lint
make -C tb/verilator/nvm_cosim -j16 quick
make -C tb/verilator/milan_dp -j16 VERILATOR_JOBS=2
make -C tb/verilator/milan_dp_render -j16 VERILATOR_JOBS=2
make -C tb/verilator/milan_dp_gptp -j16 VERILATOR_JOBS=2
python3 scripts/check_sh_idiom.py
python3 scripts/check_nvm_capture.py
scripts/run_all_suites.sh "$VALIDATION_STORAGE/suite-logs"
# with the ABC revision syn/yosys/README.md requires selected as the abc binary:
syn/yosys/run.sh --results "$VALIDATION_STORAGE/yosys-results"
make -C gptp-processor -j16 contract tb lint
PATH=$VALIDATION_TOOLS/sv2v-0.0.13/bin:$PATH bash protocol-processor/scripts/run_suites.sh
python3 syn/ooc/pp_resource_gate.py check-baseline
```

`make -C tb/verilator/milan_dp_gptp` runs the physical gPTP leg and then `verify_abort.py`; both must pass.
Also run every shell step of `.github/workflows/docs.yml` with `PATH="$DOCS_MAKE_BIN:$PATH"`, under GNU Make 4.3.
The handoff records each step's make version, command, result and evidence.
The remaining authorized base failure is #657's full render campaign. It must reproduce the same verdict list as the assigned base:

```sh
make -C tb/verilator/milan_dp_render -j16 VERILATOR_JOBS=2 tdm8render-mutants
```

It returns rc 2 for #657. The handoff compares its exact verdict list.

| Validation | Result | Head | rc |
|---|---|---|---:|
| Physical gPTP leg (#656 fix merged) | Physical 139 checks / 0 failures, simulation exit 0; `verify_abort.py` 6/0, 20/0 and 14/0 (40/0) | `3880c1eb` | 0 |
| Hosted docs shell steps | 49/49; every step uses GNU Make 4.3 | `3880c1eb` | 0 |
| Whole builder with required RV32 compiler (builder bank) | Pass, including the merged NAME-capacity gate; the same two explicit NOT RUN arms | `3880c1eb` | 0 |
| Wire-truth self-test and planted defects | 25 tests pass; the new test catches all three planted exemption defects | `3880c1eb` | 0 |
| BDD | 404 scenarios / 1,968 steps | `3880c1eb` | 0 |
| `milan_dp` and `milan_dp_render` (image packer consumers) | Fresh builds; every leg passes, with verdict and check counts identical to round 1 | `3880c1eb` | 0 / 0 |
| Full render campaign (#657) | Identical 28 PASS / 4 FAIL across all 32 controls to the round-1 base and head lists | `3880c1eb` | 2 |
| Source lists and resource gate | `pp_srcs`, source-list gate and self-test; `check-baseline` and `check` of all three recorded endpoints; input digests differ only through `KL_nvm_backend.sv` | `3880c1eb` | 0 |
| Builder outputs and packed images | 55 files over five configurations byte-identical at `42f65447`, `ba57a3bc` and `3880c1eb` | `3880c1eb` | 0 |
| Default parent sweep | 59/59 suites; 2,149,002 checks, zero failures/timeouts; four declared skips | `42f65447` | 0 |
| Processor sweep | 33/33 suites; 1,021,627 checks, zero failures | `42f65447` | 0 |
| gPTP contract, complete tests and lint | All default tests and mutation controls pass | `42f65447` | 0 |
| `pp_shadow` | Four configurations, 2,169 checks, zero failures | `42f65447` | 0 |
| Full `nvm_cosim` | 465 checks; all 39 mutants killed; separate lint/quick also pass | `42f65447` | 0 |
| Yosys portability and controls | 55/55 tops, both structural checks, exact tally and fresh cache controls; required ABC revision | `42f65447` | 0 |
| Lint, contract/measurement gates and vendor syntax | All 17 consumer commands pass; real vendor analysis covers 125 files and matches its two existing budgeted processor findings | `42f65447` | 0 |
| LiteX | 4/4 simulations plus driver controls | `42f65447` | 0 |
| Resource endpoints and instruments | Route plus both standalone endpoints recorded; policy unchanged; all 174 resource mutants killed | `42f65447` | 0 |
| Capture receipt | Census and firmware unchanged; 8x8 maximum 13.86484 ms | `42f65447` | 0 |

`HANDOFF.md`, `gate-results.json`, `docs-results.json`, and `exception-comparison.json` retain the commands, exact heads, raw results and log hashes. The parent sweep's four skipped arms and the builder's two NOT RUN arms are excluded from coverage claims.

Expected result: rc 0, with only the specifically authorized #657 dev exception demonstrated identically at base and head.

## Known limitations / out of scope

- Round 2 re-measured what the merged files feed (the builder bank, the docs gates and the physical gPTP leg), and every command its own changes feed. As the round-2 assignment directs, the other rows keep their round-1 evidence at `42f65447`. The merge's one RTL change is an elaboration-time guard constant, and the merge was not re-routed.
- The default parent sweep declares four `tsn_fuzz` skips because the optional generator is absent: two field campaigns and their freshness checks, contributing zero to its check total. The whole builder declares two NOT RUN arms: the ineffective `MAKEFLAGS += -e` mutation under GNU Make 4.3, and an unavailable historical calibration report.
- #657's render mutation survivors are unchanged dev work; their exact base and head results are recorded in the handoff.
- The resource comparison includes #653's CRF unbind change between C and the assigned dev base. It does not claim to isolate that predecessor's outside-wrapper resource movement.
- No parent RTL, processor source, firmware or SoC interface change beyond what dev brings. The SoC image emitter only drops the duplicate L6/L10 checker after the processor packer takes ownership. The only processor change is the gitlink.
- No hardware, bench access, flashing or soak. The manager performs those after merge.
- No push, PR operation or merge in this lane. Hosted contexts, independent reviews and candidate-merge validation remain pending.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied within the assigned author scope
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes with the assigned #657 exception and disclosed skipped arms
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

