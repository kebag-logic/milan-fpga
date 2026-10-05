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

Author validation complete at `42f654478c11bd8f2b070969d83140587190f276`, `661-pp-pin-ead80360` -> `dev`.
All 59 default parent suites pass. The two authorized failing campaigns reproduce the base exactly. Skipped arms are disclosed below; hosted checks and independent review remain pending.

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

Adopts processor `ead8036035affd53ef4b29979190f2f4f67084c0` from `631eeb342ca1e3fa80e734077a56a943aee76ff1` on dev `506d91db`.
This brings in wave 2, P1/P2, C10, #85, the three area lanes #232/#230/#639, and #81/#84.

| Change | Result |
|---|---|
| Four supplied adaptations | C8 waiver propagation, P1/P2 saved-state contracts, complete 42-top synthesis inventory and retired xvlog findings; one commit per concern |
| Required cleanup | Processor lint owns L6/L10; parent tests exercise it through both image emitters. REGISTER_MAP 0x644 says available_index resets after departing |
| Pin-derived records | ROM digest ledger, submodule inventory and boundary diagram, port budget and DUT-reader dispositions; naming generator produces no change |
| Resource baseline | Three measurements recorded through the generator, with policy unchanged and per-block deltas against C |

The route uses 50,318 LUT, 54,214 FF, 15,789 slices and 87.5 BRAM tiles.
It saves 449 LUT, 5,420 FF, 43 slices and five RAMB36s against C, leaving 61 slices free.
All 100,970 routable nets are fully routed, with zero routing errors; WNS/WHS is +0.108/+0.036 ns at 50 MHz.
Standalone 1x1 uses 23,178 LUT / 19,776 FF; 8x8 uses 29,853 / 27,370.
The authoritative baseline explains the notification, SRP and queue mappings alongside P1/P2 growth and cites the processor PRs' measured deltas.

The large payload flop banks identified by #234 criterion 2 now map to RAM.
The [manager's remaining-criteria record](https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5974629836) leaves only that criterion, so this adoption closes #234 as well as #639's remaining re-baseline obligation.
The 60 percent LUT target remains assigned to #640; this image is still 12,278 LUT above it.

The processor top gains only `NVM_MEM_TMO_CYC_P = CLK_HZ_P`; its 213 ports are unchanged and the parent keeps the default.
P2 reports bounded errors while retaining device debt until the terminal or reset.
P1 persists names inside the processor; the parent's existing sticky name pending transfer and map persistence remain separately owned work under #637.
`docs/reference/SUBMODULES.md` contains the complete parent-visible list.

Saved-state census, firmware digest and clocks equal the retained receipt.
`check_nvm_capture.py` passes; the 8x8 maximum remains 13.86484 ms, below 24.5 ms, so no capture re-measurement was required.

## Authoritative references

- [#661 assignment](https://github.com/kebag-logic/milan-fpga/issues/661#issuecomment-5986065259) and processor PRs #143 through #157, including their parent-visible sections.
- `CONTRIBUTING.md`, `docs/development/CODE_QUALITY.md`, `docs/reference/SUBMODULES.md` and `syn/yosys/README.md`.
- `docs/design/SAVED_STATE_MATERIALIZATION.md`, `docs/design/SAVED_STATE_FASTCONNECT.md` and `docs/reference/REGISTER_MAP.md`.
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, `docs/findings/234_PP_SHADOW_AREA_BASELINE.md` and `docs/design/AREA_BUDGET.md` (#638's method and unchanged policy).
- NFR-RES-01 and the owner's #640 redesign decision; #635's adoption method in PR #636.

## How to get into the same state

The implementation branch is local and has not been pushed by this lane.
From the supplied repository:

```sh
git switch 661-pp-pin-ead80360
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
git rev-parse HEAD
git submodule status
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export PATH=$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin:$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_STORAGE/661-a537/sv2v012/bin:$PATH
export DOCS_MAKE_BIN=$VALIDATION_STORAGE/661-a537/make43/bin
"$DOCS_MAKE_BIN/make" --version
```

Expected processor pin: `ead8036035affd53ef4b29979190f2f4f67084c0`, clean.
Use the pinned Markdown Python environment and GNU Make 4.3 for the docs workflow.
The recorded local make prefix was built from the GNU 4.3 release; the version line must read `GNU Make 4.3`.
Synthesis requires Yosys 0.66 with its bundled ABC revision `5d51a5e420f5de493d07bf61109a977248c86ffb` and sv2v 0.0.12, as specified in `syn/yosys/README.md`.
The local canonical run selects that ABC binary in a private mount namespace; the system package has a different revision. The replay below uses the retained selector script, which exports the pinned environment and runs the full synthesis and fresh cache controls from this worktree. Its digest is recorded in `tool-versions.json`. With a distribution that already bundles the required ABC, use `syn/yosys/run.sh` directly.
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
flock /tmp/milan-vivado.lock python3 scripts/xvlog_gate.py --check
PATH="$DOCS_MAKE_BIN:$PATH" python3 sw/builder/test_builder.py --require-rv32
python3 scripts/lint_rtl.py --check --self-test
make -C tb/verilator/pp_shadow -j16 VERILATOR_JOBS=2
make -C tb/verilator/nvm_cosim -j16 lint
make -C tb/verilator/nvm_cosim -j16 quick
make -C tb/verilator/milan_dp -j16 VERILATOR_JOBS=2
make -C tb/verilator/milan_dp_render -j16 VERILATOR_JOBS=2
python3 scripts/check_sh_idiom.py
python3 scripts/check_nvm_capture.py
scripts/run_all_suites.sh $VALIDATION_STORAGE/661-review-suites
sudo -n unshare --mount --propagation private bash -c \
  'set -e; mount --bind $VALIDATION_STORAGE/661-a537/abc-pinned/abc /usr/bin/abc; exec sudo -n -u alex bash $VALIDATION_STORAGE/661-a537/pinned_synthesis.sh'
make -C gptp-processor -j16 contract tb lint
PATH=$VALIDATION_STORAGE/661-a537/sv2v013/bin:$PATH bash protocol-processor/scripts/run_suites.sh
python3 syn/ooc/pp_resource_gate.py check-baseline
```

Also run every shell step of `.github/workflows/docs.yml` with `PATH="$DOCS_MAKE_BIN:$PATH"`, under GNU Make 4.3.
The handoff records each step's make version, command, result and evidence.
The following separate campaigns have the authorized base failures and must reproduce the same verdict list on the assigned base and head:

```sh
make -C tb/verilator/milan_dp_gptp -j16 VERILATOR_JOBS=2
python3 tb/verilator/milan_dp_gptp/verify_abort.py
make -C tb/verilator/milan_dp_render -j16 VERILATOR_JOBS=2 tdm8render-mutants
```

The physical and full render commands return rc 2 for #656 and #657; the separate abort verifier must return rc 0. The handoff compares both exact verdict lists.
| Validation | Result | rc |
|---|---|---:|
| Default parent sweep | 59/59 suites; 2,149,002 checks, zero failures/timeouts; four declared skips | 0 |
| Processor sweep | 33/33 suites; 1,021,627 checks, zero failures | 0 |
| gPTP contract, complete tests and lint | All default tests and mutation controls pass | 0 |
| `pp_shadow` | Four configurations, 2,169 checks, zero failures | 0 |
| Full `nvm_cosim` | 465 checks; all 39 mutants killed; separate lint/quick also pass | 0 |
| Hosted docs shell steps | 49/49; every step uses GNU Make 4.3 | 0 |
| Whole builder with required RV32 compiler | Pass; two explicit NOT RUN arms | 0 |
| Yosys portability and controls | 55/55 tops, both structural checks, exact tally and fresh cache controls; required ABC revision | 0 |
| Lint, source/contract/measurement gates and vendor syntax | All 17 consumer commands pass; real vendor analysis covers 125 files and matches its two existing budgeted processor findings | 0 |
| BDD and LiteX | 404 scenarios / 1,968 steps; 4/4 simulations plus driver controls | 0 |
| Resource endpoints and instruments | Route plus both standalone endpoints pass; policy unchanged; all 174 resource mutants killed | 0 |
| Capture receipt | Census and firmware unchanged; 8x8 maximum 13.86484 ms | 0 |
| Physical campaign, base and head (#656) | Identical 139 checks / 3 failures; separate abort accounting passes at both | 2 / 2 |
| Full render campaign, base and head (#657) | Identical 28 PASS / 4 FAIL across all 32 controls | 2 / 2 |

`HANDOFF.md`, `gate-results.json`, `docs-results.json`, and `exception-comparison.json` retain the commands, exact heads, raw results and log hashes. The parent sweep's four skipped arms and the builder's two NOT RUN arms are excluded from coverage claims.

Expected result: rc 0, with only the specifically authorized dev exceptions under #656 and #657 demonstrated identically at base and head.

## Known limitations / out of scope

- The default parent sweep declares four `tsn_fuzz` skips because the optional generator is absent: two field campaigns and their freshness checks, contributing zero to its check total. The whole builder declares two NOT RUN arms: the ineffective `MAKEFLAGS += -e` mutation under GNU Make 4.3, and an unavailable historical calibration report.
- #656's physical gPTP failures and #657's render mutation survivors are unchanged dev work; their exact base/head results are recorded in the gate table.
- The resource comparison includes #653's CRF unbind change between C and the assigned dev base. It does not claim to isolate that predecessor's outside-wrapper resource movement.
- No parent RTL, processor source, firmware or SoC interface change. The SoC image emitter only drops the duplicate L6/L10 checker after the processor packer takes ownership. The only processor change is the gitlink.
- No hardware, bench access, flashing or soak. The manager performs those after merge.
- No push, PR operation or merge in this lane. Hosted contexts, independent reviews and candidate-merge validation remain pending.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied within the assigned author scope
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes with the assigned #656/#657 exceptions and disclosed skipped arms
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
