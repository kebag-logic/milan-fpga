
The following evidence belongs to the previous head and is retained as history; it is not round-2 validation.

[A554]

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

BLOCKED at `1e99ad217f0747c33e03238f7d1c633c07ce572c`. Items 1-5 are complete. The full render mutation campaign returns rc 2: 28/32 checks, with the four failures tracked by #657. Fresh builds reproduce all four failed campaign cases after the shared generated header became stable: each clean case fails four of 127 assertions, and the mutant passes all 58 assertions. No exception to this gate is authorized in #682.
Branch `682-pp-pin-2ad2f845` targets `dev`.

## Linked Issue / roles

Closes #682
Relates to #608
Relates to #658
Closes Mister-M-alt/protocol-processor-control-plane-avb-milan#22

Executor: `[A554]`
Internal cleared-context reviewer: `[R520]`
External reviewer: `[R521]`

## Description

Adopts processor `2ad2f845dd583f8310075fa2380cb60a04fd091a` from `ead80360` on parent dev `bd884631`.
The processor top is byte-identical between pins, including its ports and parameters.
The parent harness completes a frame crossing its observation window, and the declaration-order budget drops its two fixed processor findings. The resource recipe gains an opt-in synthesis worker cap, covered by CLI controls and 34 mutation cases; default generated output is unchanged. The flow change requires the recorded resource re-baseline.
Pin-derived records are regenerated; the submodule reference records all six adopted processor PRs and C11's corrected interface documentation.

Both standalone syntheses completed with zero processor Synth 8-6901 warnings. The clean route and all three resource checks pass with unchanged policy. Capture provenance passes; the retained 8x8 maximum is 13.86484 ms. The best of three placement directives is ExtraTimingOpt: +0.334 ns WNS and +0.021 ns WHS across all corners. All 49 literal documentation workflow steps return zero under GNU Make 4.3. The initial open-synthesis sweep returns zero for 58/58 tops and both structural checks; the two tops that could overlap the builder’s temporary CSR-header edits also pass fresh repetitions, followed by passing three-top elaboration. The processor sweep passes 33 suites and 1,028,250 checks; BDD passes 404 scenarios and 1,968 steps. The host builder returns zero with two explicitly unrun arms. The direct notification target passes 421 checks. The parent sweep was cancelled after 10/60 suites passed once the render blocker was confirmed; its rc 143 is not a completed gate verdict. Remaining parent-bank commands and complete-image checks did not run.

## Authoritative references

- [Issue #682 assignment](https://github.com/kebag-logic/milan-fpga/issues/682#issuecomment-6018127147).
- Processor PRs [156](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/156), [159](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/159), [160](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/160), [161](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/161), [162](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/162) and [164](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/164).
- `CONTRIBUTING.md`, `docs/development/CODE_QUALITY.md` and `docs/reference/SUBMODULES.md`.
- `docs/findings/234_PP_SHADOW_AREA_BASELINE.md`, `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` and the area-budget re-baseline rule.
- `docs/integration/BUILDING.md` section 5 and `scripts/check_nvm_capture.py`.
- Milan Table 5.22 counter-notification spacing and IEEE 802.1Q-2014 Table 10-4 registrar behavior, as cited by the processor changes.

## How to get into the same state

The local branch is not pushed. The commands below use the handed-off lane at its committed head. Dependency versions and hashes, every executed gate command, its working directory, return code and log digest are in the accompanying evidence packet.

```sh
cd $LANES/682-pp-pin3
test "$(git remote get-url origin)" = https://github.com/kebag-logic/milan-fpga.git
test "$(git rev-parse HEAD)" = 1e99ad217f0747c33e03238f7d1c633c07ce572c
test "$(git -C protocol-processor rev-parse --show-toplevel)" = "$PWD/protocol-processor"
test "$(git -C protocol-processor rev-parse HEAD)" = 2ad2f845dd583f8310075fa2380cb60a04fd091a
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export VERILATOR_JOBS=2
export MAKEFLAGS=-j8
export LAW_BOUNDARY_JOBS=4
export SDK=$VALIDATION_STORAGE/661-a537/sdk
export LITEX_PYTHON="$HOME/litex-milan/venv/bin/python3"
export MILAN_LITEX_PYTHON="$LITEX_PYTHON"
export LITEX_ENV_CC_TRIPLE=riscv32-linux
export PATH="$VALIDATION_STORAGE/661-a537/make43/bin:$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin:$HOME/litex-milan/venv/bin:$SDK/bin:$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_STORAGE/661-a537/sv2v012/bin:$PATH"
make --version
"$VERILATOR" --version
```

Expected versions are GNU Make 4.3 and the pinned simulator 5.050. Run builder rollback controls before source-reading builds: they temporarily rewrite a shared generated CSR header. Limit simultaneous simulator builds to two. Resource runs require the recorded runtime links and run alone under the vendor lock.

## How to validate

The current blocker is reproduced by the full repository campaign, without excluding any arm:

```sh
cd $LANES/682-pp-pin3/tb/verilator/milan_dp_render
make -j8 VERILATOR_JOBS=2 tdm8render-mutants
```

Required result: rc 0 and 32/32 checks. Observed: rc 2 and 28/32. The clean epoch mode and both level-arrival-skew controls fail; the uncounted-repeat mutant survives. The complete exact-command ledger is `GATE-COMMANDS.md`, with the structured receipts in `gate-receipts.json` and per-step Make versions in `HANDOFF.md`. It includes the 49 literal documentation workflow shell steps, not a replacement approximation.

The remaining acceptance commands include:

```sh
cd $LANES/682-pp-pin3
python3 scripts/check_nvm_capture.py
python3 syn/ooc/pp_resource_gate.py check-baseline
bash scripts/run_all_suites.sh $VALIDATION_STORAGE/682-a554/parent-suite-logs
python3 scripts/suite_tally.py $VALIDATION_STORAGE/682-a554/parent-suite-logs --quiet --expect-suite-root tb/verilator
bash syn/yosys/run.sh --results $VALIDATION_STORAGE/682-a554/yosys-results
make -C tb/verilator/milan_dp_gptp -j8 VERILATOR_JOBS=2
make -C tb/verilator/nvm_cosim -j8 lint
make -C tb/verilator/nvm_cosim -j8 quick JOBS=2 POOL=2
bash scripts/run_litex_sims.sh --selftest
bash scripts/run_litex_sims.sh $VALIDATION_STORAGE/682-a554/litex-sim-logs
```

Expected result: every assigned gate returns zero; capture stays at or below 24.5 ms at 8x8; the best complete image meets WNS at least +0.03 ns and WHS at least zero at every corner. The routed results are +0.101/+0.031 ns for ExtraPostPlacementOpt, -0.857/+0.008 ns for AltSpreadLogic_high, and +0.334/+0.021 ns for ExtraTimingOpt. Routed checkpoints alone do not satisfy the complete-image criterion: bitstreams and their generated bound flash manifests remain outstanding.

## Known limitations / out of scope

- #657 blocks the required all-green acceptance; no waiver or test weakening is applied.
- Documentation workflow builder controls report 16 unrun arms in their intentionally limited environment. The separate installed-environment builder covers elaboration and RV32 arms, but still reports two unrun arms: an ineffective MAKEFLAGS mutation under Make 4.3 and a missing historical calibration report.
- Current remote dev is `79b086d44eb62d007d38e18f5618b98e8e2a33e6`, 32 commits beyond this lane’s base. There are no overlapping changed paths, but integration and affected-gate revalidation remain required. This execution request forbids merge and rebase.
- Routed timing reports disclose CDC findings and unconstrained external I/O; positive slack does not discharge them. Resource baseline E is the prescribed default directive, distinct from the best timing directive.
- Hardware flashing, withdrawal cycles, default-map readback and soak are the manager's post-merge work.
- Counter spacing is stamped at frame grant; downstream MAC stalls remain the processor's disclosed wire-gap limitation.
- The held DEREGISTER retains its contents but can be delivered later.
- No processor source, parent RTL, firmware or interface edit beyond the supplied patches.
- No push, PR operation, rebase or merge in this session. Independent review, hosted checks and merge validation remain pending.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
