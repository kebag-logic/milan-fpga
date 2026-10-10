[A589]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN -- every local gate exits 0 at `49b437f4`: 59 firmware arms, 784 of 784 planted defects, 61 Verilator suites, 58 Yosys tops, 81 documentation commands, route PASS -- `711-lwsrp-bump` -> `dev`

## Linked Issue / roles

Closes #711
Relates to #665

Executor: `[A589]`
Internal cleared-context reviewer: `[R596]`
External reviewer: `[R597]`

## Description

This adopts lwSRP `main` at `08ee86e8`, the merge of lwSRP PR #18. That PR groups every VectorAttribute of one AttributeType into a single Message per MRPDU. Decoded events are unchanged; only the byte layout of some MRPDUs changes.

| Change | Where | Clause |
|---|---|---|
| Gitlink `9197193e` to `08ee86e8`, the only lwSRP change | `third_party/lwSRP` | IEEE 802.1Q-2018 10.8.1.2 c, d |
| Pin check and its fetch comment | `sw/firmware/ctrl/test/ctrl_arms.py:359`, `:362` | none |
| The MVRP LeaveAll walk reads every VectorAttribute to the Message's EndMark; each walk must end on the MRPDU EndMark | `sw/firmware/ctrl/test/srp_latency.cpp:76-84` | 10.8.1.2 b, d; 10.8.2.8; 10.8.2.9; 10.8.2.10.1 |
| Ledger row and PR list | `docs/reference/SUBMODULES.md:26`, `:229` | none |
| Regenerated boundary diagram (`submodule_boundaries.gen.py`) | `docs/diagrams/submodule_boundaries.{svg,drawio,png}`, `docs/diagrams/PNG_MANIFEST.json` | none |
| Prose pins and contract permalinks (the cited text is unchanged at the new pin) | `sw/firmware/ctrl/README.md:340-342`, `sw/firmware/ctrl/srp/README.md:75-76`, `:293`, `:343-345`, `docs/design/MAILBOX_SPLIT.md:295` | 10.8.1.2 |

The only byte-level SRP expectation that changes is `srp_latency.cpp`'s MVRP walk. It assumed one VectorAttribute per MVRP Message and passed at the new pin only because its arm declares one VID. The new end-of-walk assertion makes the old walk fail at `08ee86e8` at one and two interfaces. The new walk passes at both pins.

## Authoritative references

- Issue #711 acceptance 1-5 and assignment comment 6098059753.
- kebag-logic/lwSRP#17 and PR #18. `08ee86e8` has the tree of the twice-reviewed head `a44eeedf`.
- IEEE 802.1Q-2018 10.8.1.2 (MRPDU structure), 10.8.2.4-10.8.2.10.2 (field encodings), 35.2.2.4-35.2.2.9 (MSRP), 11.2.3.1 (MVRP).
- The #621 capture ruling 6089776382 (the base-against-candidate log comparison model).
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` (shipping export and route recipe).

## How to get into the same state

```sh
git fetch origin 711-lwsrp-bump
git checkout 711-lwsrp-bump
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP
git submodule status
```

## How to validate

```sh
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
python3 docs/diagrams/submodule_boundaries.gen.py --check
python3 scripts/check_submodule_docs.py
python3 scripts/check_nvm_capture.py
python3 scripts/check_em_dash.py --base "$(git merge-base origin/dev HEAD)"
```

On a machine with Vivado 2026.1, `python3 scripts/xvlog_gate.py --check` also passes. The shipping route follows `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` ("Integrated measurements", then "Resource gate"), ending in `python3 syn/ooc/pp_resource_gate.py check "$WORK/ax7101/gateware" --endpoint route-1x1`.

Expected result / pass criteria: every command exits 0. `test_ctrl_firmware.py` ends `test_ctrl_firmware: PASS` with 59 arms `ok`, `mutants: 471 of 471 caught`, every AECP and SRP defect `[ok]`, and both lwSRP pin refusals `[ok]`. `fw_coverage.py --check` prints `firmware coverage: PASS (30 files)`.

Results (base `e8454e27` against this head `49b437f4`):

| Evidence | Base | Head |
|---|---|---|
| Firmware arms | 59 ok, 1,191 cases | 59 ok, 1,191 cases, identical verdict lines |
| Planted defects (control 471, AECP 74, SRP 169 + 68, pin 2) | 784 caught | 784 caught |
| Coverage, 30 files | 100 % | 100 %, identical table and denominators |
| Decoded SRP frames of every firmware arm (independent 802.1Q 10.8 decoder) | | 4,186 MRPDUs: 2,201 identical, 1,985 layout-only, **0 decoded differently**; every head MRPDU grouped |
| Saved-state capture, six arms and three controls, receipt recipe, Verilator 5.052 | | all nine `capture.log` files byte-identical to the base's |
| All-fabric shipping export (`ax7101` and `ax8x8`) | | firmware ROM identical (`a14e34e7…` 1x1, `cf2c371f…` 8x8); non-comment RTL and every image identical |
| Documentation gates (all of `docs.yml`, CPython 3.12.3) | 81 rc 0 | 81 rc 0 |
| Yosys `syn/yosys/run.sh` | | 58 of 58 tops, tap purity PASS |
| Verilator sweep `scripts/run_all_suites.sh` (Verilator 5.050) | | 61 suites passed, 0 failed, 0 timed out; 2,185,848 checks |
| `tsn_fuzz` with the CI-pinned field oracle | | AAF/AVTP 164 pass, gPTP 677 pass, 0 fail |
| SRP linked-size fixture `ctrl_srp_image.py`, 1x1 and 8x8 at IF=1 and IF=2 | 1x1 IF=1 `.text` 45,828 | `.text` +588 octets at every shape; `.rodata`, `.bss`, stack and every static object unchanged |
| Shipping route `route-1x1` (Vivado 2026.1), then `pp_resource_gate.py check` | LUT 50,267, FF 54,413, SLICE 15,779, RAMB36 74, RAMB18 27, DSP 14; WNS 0.299 ns, WHS 0.031 ns; fully routed; PASS | identical figures and PASS; the census, utilization, timing and route-status reports equal the base's apart from their `Date` line |
| `scripts/xvlog_gate.py --check` | | PASS, 0 findings |

## Known limitations / out of scope

- The capture receipt `tb/verilator/nvm_capture_cpu/measurements.json` is not re-recorded. This lane changes no capture input: lwSRP is not compiled into the capture firmware, and its digest (over `milan_baremetal.c`) does not move. The receipt's existing staleness against dev is #621's, re-recorded by open PR #707.
- The base's `byte-only` capture control exits 1 by design of this base's grader. Its correction is in open PR #707. The simulator output is identical at base and head.
- The control firmware grows by the grouped encoder's code only. The RV32 arm reports `core_mrp_mad.o` text 12,709 to 13,309 octets (+600) at every shape, as upstream measured. The linked size fixture shows +588 `.text` octets after section garbage collection. The tree records no size figure of the control firmware, so nothing there is re-recorded.
- The suggestions on lwSRP PR #18 (capacity assertion in its sweeps, a layout note, the trace buffer) belong to lwSRP and are not part of this pin bump.
- The issue expected the capture's firmware digest to move and the shipping ROM to match a documented digest. Neither premise holds as written. The capture firmware does not contain lwSRP. No tracked record documents the current shipping ROM digest. Measured at base, head and a second base export, the shipping ROM is identical: 1x1 `a14e34e7…`, 8x8 `cf2c371f…`.
- `act_ci.py --pr` needs a pushed head; it was not run. Its offline `--selftest` passes.
- No hardware, bench or flashing.

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
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
