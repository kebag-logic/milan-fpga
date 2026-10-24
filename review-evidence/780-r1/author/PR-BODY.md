[A670]

## Contents

- **[Status](#status)** -- REVIEW READY: the fifth parent pin adoption, processor `ed211803`, with every gate green; `780-pin5-ed211803` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, related issues and roles.
- **[Description](#description)** -- The gitlink, the re-recorded records, the grep, the measured resources and the parent-side probe.
- **[Authoritative references](#authoritative-references)** -- The clause, the processor change and the resource record.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout, submodules and tools.
- **[How to validate](#how-to-validate)** -- The gate commands and the expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this lane did not change, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

**REVIEW READY** at `25f05752f7e50e3cf7e27008e434ffde930b4b6f`; `780-pin5-ed211803` -> `dev` (from `a032c6d6`).

Every gate the issue names passes at this head:

- The full parent sweep, as four shards: 64 / 64 suites, 2,190,096 checks, 0 in-suite failures, 0 timed out.
- milan_dp: RESULT PASS 15, 0 failures.
- The firmware gate set: all eight commands exit 0.
- The rtl-fast replica: 11 / 11 jobs succeed, including `cd tests && behave --no-capture -f plain`.
- behave: 406 scenarios.
- Yosys: 60 / 60 tops.
- lint: 89 violations, at the ratchet of 89.
- The docs gates under GNU Make 4.3: every step passes (one builder leg needed a rerun; see Description).
- The resource gate: RESULT PASS at `route-1x1`, `ooc-1x1` and `ooc-8x8` against the eleventh record. The largest
  move is -77 LUT on the route, and no tolerance is approached.

## Linked Issue / roles

Closes #780
Relates to #773
Relates to #774
Relates to #775

Processor issue #200 / PR #201 is the donor change adopted here.

Executor: `[A670]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

| Commit | Change |
|---|---|
| `e4bd7f5b` | `protocol-processor` gitlink `93fb0b2d` -> `ed2118035e4cec76fb1b59cfbf8a053aeacc8af8` (processor `main`, the PR #201 merge). FPGA-gPTP stays at `55680bff` |
| `afdbd99b` | Pin-derived records, each through its generator: ROM ledger rows (`syn/yosys/rom_digests.tsv:72-73`), the boundary diagram and the pin table row |
| `25f05752` | The adoption section on the pin page (`docs/reference/SUBMODULES.md:260-274`) and the CHANGELOG section (`CHANGELOG.md:47-59`) |

**The parent-visible change.** A GET_AVB_INFO on a descriptor other than AVB_INTERFACE now answers NOT_SUPPORTED
(status 11), with the command echoed at its own length. Since processor #177 it had answered NOT_IMPLEMENTED
(status 1).

IEEE 1722.1-2021 Table 7-141 defines the two statuses:

- 1 means the entity does not support the command type.
- 11 means the command is implemented but its target is not supported.

GET_AVB_INFO is implemented (7.4.40), so 11 is the right status here. Two cases are unchanged: an absent
AVB_INTERFACE index still answers NO_SUCH_DESCRIPTOR, and a command under cdl 16 still answers BAD_ARGUMENTS. The
processor change is one dispatch constant. Both processor ROM digests equal the `93fb0b2d` rows, and no port,
parameter or register changes.

**The grep.** `git grep` over the parent, submodules excluded, found no test, model or document that expects status 1
for this case, so nothing needed updating:

- milan_dp sends GET_AVB_INFO only to AVB_INTERFACE 0.
- The behave model grades only an existing target.
- The hive compliance tool sends AVB_INTERFACE with a bad index.
- The firmware's own AECP already answers NOT_SUPPORTED.
- The compliance matrix and the testing guide name no status for this case.

The two remaining hits are history and are left as they are: the fourth adoption's CHANGELOG section and its pin-page
table row. The new sections state that #200 reverses them.

**A parent-side probe, not committed.** One extra GET_AVB_INFO(CLOCK_DOMAIN 0) was added to the `pp_shadow` base
leg, sent through `KL_pp_shadow`, and run in clean clones. At dev `a032c6d6` the parent receives status 1 at cdl 16.
At this head it receives status 11 at cdl 16. Both runs report 622 checks and 0 failures. So the wrapper passes the
processor's status through unchanged.

**Resources, against the eleventh record** (Vivado 2026.1, one run at a time):

| Endpoint | Figure | Record | Head | Delta | Tolerance |
|---|---|---:|---:|---:|---:|
| `route-1x1` | LUT / FF / SLICE | 51,259 / 53,208 / 15,835 | 51,182 / 53,208 / 15,825 | -77 / 0 / -10 | 500 / 600 / 80 |
| | WNS / WHS ns | 0.236 / 0.028 | 0.165 / 0.036 | -0.071 / +0.008 | 0.25 |
| `ooc-1x1` | LUT / FF | 23,828 / 20,000 | 23,845 / 20,002 | +17 / +2 | 250 / 250 |
| `ooc-8x8` | LUT / FF | 32,467 / 28,220 | 32,450 / 28,218 | -17 / -2 | 316 / 339 |

RAMB36, RAMB18 and DSP are unchanged at every endpoint. The route is complete, with 0 routing errors. Signoff:

- Slow corners: WNS +0.165 ns, WHS +0.102 ns.
- Fast corners: WNS +1.536 ns, WHS +0.036 ns.
- TNS and THS are 0.

The record is not re-recorded.

**The docs builder leg 1.** On the first docs pass, builder leg 1 failed in its NVM saved-state writer self-test
while the sweep was loading the host. That self-test then passed alone in the same clone. The leg then passed twice,
once on CPython 3.12.3 and once with the LiteX interpreter. This change does not touch that writer.

**The rtl-fast replica** runs the workflow's step bodies for an unpushed head. In its first run the six firmware
jobs stopped at the SDK install step, because the RV32 SDK in that run's home directory had been copied from
another directory and its provenance receipt did not match. The SDK was then installed with
`scripts/ci_rv32_sdk.py --archive` from the pinned archive, and `changes` and the six firmware jobs were rerun at
the same head. All six passed. Taking each job from its latest run, all 11 of the fast gate's `needs:` jobs succeed.

## Authoritative references

- IEEE 1722.1-2021 7.4.40 (GET_AVB_INFO) and Table 7-141 (AECP status codes 1 and 11).
- Processor issue #200 and PR #201, and its compliance review entry (processor `docs/architecture`, section 8 item 12).
- The fourth adoption, #771 / #772, for the method.
- `syn/ooc/pp_resource_baseline.json`, the eleventh record (`docs/design/AREA_BUDGET.md`).
- `docs/reference/SUBMODULES.md`, the pin page and its adoption tables.

## How to get into the same state

Set `REPO` to the candidate checkout. Point `VERILATOR`, `MAKE43_BIN`, `RV32_SDK`, `LITEX_PYTHON`, `GTEST_1_14`,
`CLANG_18_BIN` and `VIVADO_BIN` at the local dependencies. Before any command inside a submodule, check its own
top-level directory.

```sh
cd "$REPO"
git remote get-url origin
git rev-parse HEAD
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP
test "$(git -C protocol-processor rev-parse --show-toplevel)" = "$PWD/protocol-processor"
test "$(git -C gptp-processor rev-parse --show-toplevel)" = "$PWD/gptp-processor"
git submodule status protocol-processor gptp-processor
python3 scripts/ci_rv32_sdk.py --destination "$RV32_SDK"
python3 scripts/ci_rv32_sdk.py --destination "$RV32_SDK" --verify-only
export VERILATOR VERILATOR_JOBS=2 PYTHON_CPU_COUNT=4 PYTHONHASHSEED=0
export MILAN_RV32_CC="$RV32_SDK/bin/riscv32-linux-gcc"
export PKG_CONFIG_PATH="$GTEST_1_14/lib/pkgconfig" LD_LIBRARY_PATH="$GTEST_1_14/lib"
export PATH="$MAKE43_BIN:$CLANG_18_BIN:$VIVADO_BIN:$PATH"
make --version
"$VERILATOR" --version
```

The expected state:

- origin `https://github.com/kebag-logic/milan-fpga.git`
- head `25f05752f7e50e3cf7e27008e434ffde930b4b6f`
- processor `ed2118035e4cec76fb1b59cfbf8a053aeacc8af8`
- gPTP `55680bff3b287b9a7b0c759f51471fa617c17335`
- GNU Make 4.3
- Verilator 5.050

## How to validate

```sh
python3 syn/ooc/pp_resource_gate.py check-baseline
bash syn/yosys/ooc.sh --record-rom-digests
git diff --exit-code syn/yosys/rom_digests.tsv
python3 docs/diagrams/submodule_boundaries.gen.py --check
python3 docs/diagrams/timesync_chain.gen.py --check
python3 scripts/check_submodule_docs.py
python3 scripts/check_gptp_docs.py --with-submodule
python3 scripts/check_port_contracts.py
python3 scripts/measure_naming.py --check
python3 scripts/measure_test_evidence.py --check
python3 protocol-processor/scripts/check-integrator-params.py
python3 scripts/lint_rtl.py --check
suite_logs=$(mktemp -d)
scripts/run_all_suites.sh "$suite_logs" --wait
python3 scripts/suite_tally.py "$suite_logs" --quiet --expect-suite-root tb/verilator
syn/yosys/run.sh
(cd tests && behave --no-capture -f plain)
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
python3 sw/firmware/gtest/tally_selftest.py --mutants
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --lwsrp third_party/lwSRP --jobs 4
python3 sw/firmware/ctrl/test/test_ctrl_firmware_shards.py
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 4
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --lwsrp third_party/lwSRP --jobs 4
"$LITEX_PYTHON" sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest
```

Expected result: every command exits 0. In detail:

- The ROM ledger regenerates byte-identically.
- The sweep: 64 / 64 suites, 2,190,096 checks, 0 in-suite failures, 0 timed out.
- Yosys: 60 / 60 tops, with 0 unjustified tied inputs.
- behave: 14 features, 406 scenarios and 1,977 steps.
- lint: "LINT GATE: PASS (89 violation(s) <= ratchet 89; 19 waived, 0 justified lint_off)".
- `test_ctrl_firmware`: PASS.
- The saved-state gate: OK over 5 shapes, 435 tests and 109 / 109 planted defects.
- The coverage ratchet: PASS on 30 files. `ctrl_boundary`: PASS.
- `route-1x1`, `ooc-1x1` and `ooc-8x8`: run with the recipe's Vivado flows, then
  `python3 syn/ooc/pp_resource_gate.py check` gives RESULT: PASS at each, with the figures above.

## Known limitations / out of scope

- No parent test is added for the wrong-type status. No parent expectation existed for it, and the issue's Required
  list adds none. The processor's own suites grade the status, and the uncommitted probe above shows the parent
  receives it.
- The resource record is not re-recorded, because every figure is within tolerance.
- FPGA-gPTP is not moved.
- #773, #774 and #775, the other fixes for the next qualification image, are separate lanes.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests (the processor's own suites grade the status; no parent expectation existed)
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
