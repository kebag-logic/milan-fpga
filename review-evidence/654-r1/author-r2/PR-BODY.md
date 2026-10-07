[A566]

## Contents

- [Status](#status)
- [Linked Issue / roles](#linked-issue--roles)
- [Description](#description)
- [Authoritative references](#authoritative-references)
- [How to get into the same state](#how-to-get-into-the-same-state)
- [How to validate](#how-to-validate)
- [Known limitations / out of scope](#known-limitations--out-of-scope)
- [Definition of Done](#definition-of-done)
- [Round 2](#round-2)

## Status

Round 1: required local gates return 0 at `d6b6ca899ae4c248a1342867bb89060e24febcd5`.
The builder declares one unavailable historical Arty report calibration arm.
`654-soc-option-refusals` -> `dev`.
Current status is recorded in Round 2 below.

## Linked Issue / roles

Closes #654
Relates to #583

Executor: `[A566]`
Internal cleared-context reviewer: `[R550]`
External reviewer: `[R551]`

## Description

VexiiRiscv accepted constructor FPU and L2 requests without building the requested hardware. Shared CLI/constructor validation now rejects those requests before setup, with specific reasons. It also rejects explicit NaxRiscv L2 zero, which silently kept the upstream default, and invalid byte counts.

The existing NaxRiscv FPU and positive-L2 effects remain supported through the developer constructor. Tests cover both register widths, early refusals, generated RTL changes, and ten planted defects. The build guide documents each entry point.

Both AX7101 configurations retain byte-identical generated build artifacts: 32 files each. The comparison fixes timestamp and diagnostic hierarchy-order inputs equally before generation; it compares raw artifact bytes. Diagnostic logs are retained separately. Defaults and the product CLI profile remain unchanged.

## Authoritative references

- Issue #654 body, first comment, assignment 6045462105 and resume ruling 6045774790.
- [Requirements](REQUIREMENTS.md), REQ-VER-03 and REQ-VER-04.
- [Contribution rules](CONTRIBUTING.md).
- [Build guide](docs/integration/BUILDING.md).

## How to get into the same state

Use the pinned dependency environment from `sw/litex/litex_pins.txt`, its existing patch series, the required RV32 SDK, and the pinned lint version. The netlist mode additionally requires the NaxRiscv data package at `20da269306bb3bfabd09de08d4c1be1fbc202474`, NaxRiscv sources at `9f452d50560d02fb391bc8039f5453c54e0911af` and SpinalHDL at `c362657003fa178350d6955055867e9ab363c44a`.

```sh
git switch 654-soc-option-refusals
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
: "${SCRATCH:?Select a disk-backed scratch directory}"
: "${LITEX_PYTHON:?Select the pinned dependency interpreter}"
export TMPDIR="$SCRATCH"
export MILAN_LITEX_PYTHON="$LITEX_PYTHON"
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0
export VERILATOR_JOBS=2 MAKEFLAGS=-j8
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
```

## How to validate

```sh
"$LITEX_PYTHON" sw/builder/test_soc_options.py --netlists
"$LITEX_PYTHON" sw/builder/test_builder.py --require-elaboration --require-rv32
scripts/run_litex_sims.sh "$SCRATCH/litex-sim-logs"
python3 scripts/lint_rtl.py --check
python3 scripts/docs_check.py
python3 scripts/check_doc_style.py
python3 scripts/check_doc_paths.py
python3 scripts/check_py_idiom.py
python3 scripts/check_soc_sources.py
python3 scripts/check_sweep_shape.py --self-test
python3 scripts/check_deploy_shape.py --selftest
python3 scripts/check_entity_shape.py --self-test
python3 scripts/check_feature_status.py
python3 scripts/check_gptp_docs.py
python3 scripts/check_solution_docs.py
python3 scripts/check_submodule_docs.py
python3 scripts/check_port_contracts.py
python3 scripts/check_todo_ownership.py
python3 scripts/check_baremetal_only.py --check
python3 scripts/measure_fail_fast.py --check
python3 scripts/measure_naming.py --check
python3 scripts/measure_test_evidence.py --check
python3 scripts/check_hygiene.py --check
python3 scripts/check_em_dash.py --base e21c1ca024d37ea188ad15b5c8f9c2dae18628df
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/gen_toc.py --check
python3 docs/traceability/gen_module_matrix.py --check
```

Expected result: every command returns 0. The focused test reports 36 constructor cases, 11 CLI cases, six killed refusal controls, four real netlist effects and four killed forwarding controls. All four simulations pass without skips. Lint adds no violations.

The accompanying handoff contains raw CPU measurements, the complete artifact digest population, gate logs' hashes, and `export_compare.py`. Reproduce the raw AX7101 comparison from the repository root:

```sh
: "${EVIDENCE_DIR:?Select the accompanying evidence directory}"
export MEASURE_DIR="$SCRATCH/exports-654"
for shape in ax7101_8x8 ax7101_1x1_tdm8; do
  "$LITEX_PYTHON" "$EVIDENCE_DIR/export_compare.py" baseline-fixed "$shape"
  "$LITEX_PYTHON" "$EVIDENCE_DIR/export_compare.py" candidate-fixed "$shape"
done
```

Expected result: 32 raw artifacts match for each configuration, exit 0. The baseline recipe is read from the assigned Git blob. No generated artifact is normalized after generation.

## Known limitations / out of scope

- Arty configurations and their existing PLL refusal belong to #583, per the resume ruling. The builder also reports one historical Arty mf48 utilization-report calibration arm as NOT RUN because that report is absent; its return code is 0, and every required elaboration arm ran.
- NaxRiscv remains a developer constructor path; the product CLI still requires single-hart RV32 VexiiRiscv.
- Export equality covers generated gateware and software inputs. No new bitstream, timing or hardware claim is made.
- The builder includes the refusal bank. Real NaxRiscv effect tests are an explicit additional command and fail when their generator dependency is absent.
- Independent review, hosted checks, merge validation and containment remain pending. This assignment authorizes no push, PR operation or merge.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

## Round 2

Current head: `853a7357ba86d758a0e38f65db89a6187fb547bc`. Every required local command returns 0.
This section supersedes round 1 counts and review status above.
Assignment: issue #654 comment 6046709819.

CLI L2 parsing now preserves the decimal token through validation. Both
`1e-400` and `-1e-400` are refused with the whole-byte reason before setup.
Omission and genuine zero retain their behavior. The constructor also refuses
unknown CPU names, closing the fallback path identified by the internal review.
The build guide restores its section 2.1 reference and documents isolated data.

| Review item | Change | Verification |
|---|---|---|
| R551-1-F1 | Exact token parsing and whole-byte validation | Both underflow cases; two killed float-parser controls; unchanged review probe rc 0 |
| R550-1 RESIDUE | Explicit section 2.1 reference | Documentation gates rc 0 |
| R550-1 S2 | Unknown CPU refusal before setup | 16 cases across both widths; guard-removal control killed |
| R550-1 S1 | Cache side effects and `--nax-data-dir` documented | Documentation gates rc 0 |

The final focused bank passes 52 constructor cases, 18 CLI cases and nine
refusal controls. The effect bank retains four netlist effects and four
forwarding controls. Both AX7101 exports remain byte-identical to the original
base, 32 artifacts each. Lint and documentation gates return 0.
All four simulations pass without skips. The full builder bank and three shape
self-tests return 0. The builder retains its single NOT RUN historical Arty
utilization-report arm; every required elaboration and RV32 compiler arm ran.

Use the round 1 reproduction commands, with an isolated NaxRiscv data copy:

```sh
"$LITEX_PYTHON" sw/builder/test_soc_options.py --netlists --nax-data-dir "$NAX_DATA_DIR"
"$LITEX_PYTHON" "$REVIEW_PACKET/scripts/byte_count_underflow.py" "$PWD"
```

`REVIEW_PACKET` names the R551-1 packet from the public evidence branch.
The reviewer probe must return 0 with both underflow tokens refused.
The handoff includes fresh gate receipts and the artifact digest population.
Independent re-review is required; earlier verdicts cover the previous head.
Publication, hosted checks, final-candidate validation and containment remain pending.

The round 2 REVIEW READY evidence is posted on issue #654.
