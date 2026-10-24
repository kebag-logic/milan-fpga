# #780 [A670] handoff: fifth parent pin adoption (protocol-processor ed211803)

Status: REVIEW READY at `25f05752`; every acceptance item met. TAKEN posted (issuecomment-6386897420); REVIEW READY posted (issuecomment-6389598798). Branch `780-pin5-ed211803` from dev
`a032c6d6` (origin `https://github.com/kebag-logic/milan-fpga.git`; remote `dev` still `a032c6d6`). Head
`25f05752f7e50e3cf7e27008e434ffde930b4b6f`. Not pushed.

A host reset at 21:22 cut the previous session. The tree was clean with three commits. The reset cut two firmware
gates and the rtl-fast replica, and each was rerun at the same head (below).

## Commits

| Commit | Change |
|---|---|
| `e4bd7f5b` | `protocol-processor` gitlink `93fb0b2d` -> `ed2118035e4cec76fb1b59cfbf8a053aeacc8af8` (processor `main`, the PR #201 merge; resolved with `git rev-parse` inside the submodule after its toplevel and origin were checked) |
| `afdbd99b` | Pin-derived records through their generators: ROM ledger (`bash syn/yosys/ooc.sh --record-rom-digests`), boundary diagram (`python3 docs/diagrams/submodule_boundaries.gen.py`), pin table row (checked by `scripts/check_submodule_docs.py`) |
| `25f05752` | Pin page adoption section and CHANGELOG section |

FPGA-gPTP stays at `55680bff`. Before every git command inside `protocol-processor`, its toplevel was checked and
its origin was confirmed as `https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git`.

## Changes, each with file:line and its clause

| File:line | Change | Clause |
|---|---|---|
| `protocol-processor` (gitlink) | `93fb0b2d` -> `ed211803` | processor #200 / PR #201 |
| `syn/yosys/rom_digests.tsv:72-73` | Two rows for `ed2118035e4c...`: `ltn_rom.hex` `23cc67ee...`, `ucode.hex` `1f78804e...`, byte-equal to the `93fb0b2d` rows at `:48-49` (the ROMs are unchanged, as PR #201 states) | ROM ledger rule, `syn/yosys/ooc.sh` |
| `docs/diagrams/submodule_boundaries.{svg,drawio,png}`, `docs/diagrams/PNG_MANIFEST.json` | Generated; `svg:33` reads `pin ed2118035e4c` | -- |
| `docs/reference/SUBMODULES.md:25` | Pin table row | -- |
| `docs/reference/SUBMODULES.md:260-274` | Adoption section: the #200 row (the parent-visible list) and its notes | IEEE 1722.1-2021 Table 7-141 (1 NOT_IMPLEMENTED: "does not support the command type"; 11 NOT_SUPPORTED: "the command is implemented but the target of the command is not supported"), 7.4.40.1 |
| `CHANGELOG.md:11`, `:47-59` | Contents entry and section | same |

### The grep (assignment item 2)

`git grep` over the parent (submodules excluded) for NOT_IMPLEMENTED / NOTIMPL / "not implemented" / status 1 near
GET_AVB_INFO / AVB_INFO / 0x0027. Every file naming GET_AVB_INFO was also read by hand. The grep was re-run after the
reset and gave the same result:

- No parent test, model or document expects status 1 for a wrong-type GET_AVB_INFO, so item 2 changes nothing.
  - milan_dp (`tb/verilator/milan_dp/sim_nxn.cpp:1721`, `:1770`, `:10301`; `sim_gptp.cpp:1036`) sends GET_AVB_INFO
    only to AVB_INTERFACE 0 (`{0x00, 0x09, 0x00, 0x00}`).
  - The behave model (`tests/steps/aecp_engine_steps.py:246`) grades only an existing target (SUCCESS).
  - `tb/tools/hive_compliance.py:450` sends AVB_INTERFACE with a bad index (NO_SUCH_DESCRIPTOR, unchanged).
  - The firmware AECP (`sw/firmware/ctrl/aecp/aecp_commands.c:394-396`) is its own stack and already answers a
    non-AVB_INTERFACE type NOT_SUPPORTED.
  - The parent RTL only serves GET_AVB_INFO data (`hdl/milan/milan_datapath.sv:6281`, the gather face). The status
    comes from the processor.
  - The compliance matrix (`docs/reference/MILAN_COMPLIANCE_MATRIX.md:129`) and the testing guide name no status
    for this case.
- History, left as is:
  - `CHANGELOG.md:143` (the 93fb0b2d section, "answers NOT_IMPLEMENTED (#177)") and `docs/reference/SUBMODULES.md:228`
    (#771's table, the #177 row) record the fourth adoption. The new sections state that #200 reverses it.
  - `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:207` and `PDU_GETTER_SETTER_VERIFICATION.md:290` use "NOT
    IMPLEMENTED" as a v1 feature status, not a status code.
  - `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:188` is #182's measured area cost.

## New checks / planted mutants

No check is added or changed in the tree. No parent expectation existed for this case (above), and the assignment
adds none.

There is uncommitted parent-side evidence instead (`probe/pp_shadow-p780-probe.patch`, `receipts/probe/`). It adds
one GET_AVB_INFO(CLOCK_DOMAIN 0) to the `pp_shadow` base leg, sent through `KL_pp_shadow`. Each revision ran in a
clean clone:

| Revision | Processor pin | Status the parent receives | cdl | pp_shadow |
|---|---|---|---|---|
| dev `a032c6d6` | `93fb0b2d` | 1 (NOT_IMPLEMENTED) | 16 | 622 checks, 0 failures |
| head `25f05752` | `ed211803` | 11 (NOT_SUPPORTED) | 16 | 622 checks, 0 failures |

The probe acts as its own control. The same build prints status 1 at the old pin, so the parent wrapper passes the
processor's status through unchanged.

## Resources and route timing

Measured against the eleventh record (`syn/ooc/pp_resource_baseline.json`, which this lane does not change). Vivado
2026.1, one run at a time under the lock, using the recipe flows as recorded (`receipts/vivado/`):

| Endpoint | Figure | Record | Head | Delta | Tolerance | Verdict |
|---|---|---:|---:|---:|---:|---|
| `route-1x1` | LUT | 51,259 | 51,182 | -77 | 500 | ok |
| | FF | 53,208 | 53,208 | 0 | 600 | ok |
| | SLICE | 15,835 | 15,825 | -10 | 80 | ok |
| | RAMB36 / RAMB18 / DSP | 74 / 27 / 13 | 74 / 27 / 13 | 0 | 0 | ok |
| | WNS / WHS ns | 0.236 / 0.028 | 0.165 / 0.036 | -0.071 / +0.008 | 0.25 | ok |
| `ooc-1x1` | LUT / FF | 23,828 / 20,000 | 23,845 / 20,002 | +17 / +2 | 250 / 250 | ok |
| | RAMB36 / RAMB18 / DSP | 16 / 3 / 8 | 16 / 3 / 8 | 0 | 0 | ok |
| `ooc-8x8` | LUT / FF | 32,467 / 28,220 | 32,450 / 28,218 | -17 / -2 | 316 / 339 | ok |
| | RAMB36 / RAMB18 / DSP | 21 / 5 / 8 | 21 / 5 / 8 | 0 | 0 | ok |

The route is complete: all 101,515 routable nets are fully routed, with 0 routing errors. Signoff timing:

- Slow corners: WNS +0.165 ns, WHS +0.102 ns.
- Fast corners: WNS +1.536 ns, WHS +0.036 ns.
- TNS and THS are 0.

No tolerance is exceeded, so the resource STOP condition does not apply. The issue expected a delta of about 0, and
that is what was measured. The sub-block movements, which the gate does not grade, net to the wrapper totals above.

## Gate table

All gates ran at head `25f05752` in clean clones, with submodules taken from the lane's checkouts. Each is rc 0
unless stated.

| Gate | Command | Result | Receipt |
|---|---|---|---|
| Full sweep, 4 shard units | `bash scripts/run_all_suites.sh <logs> --wait --shard k/4`, k = 0..3, each in its own clone and unit | 64 / 64 suites (15 + 16 + 17 + 16), 2,190,096 checks, 0 in-suite failures, 0 timed out | `receipts/sweep/` |
| milan_dp | the milan_dp leg of shard 0 | RESULT: PASS 15, [FAIL] 0; every GET_AVB_INFO row targets AVB_INTERFACE 0 | `receipts/milan_dp/summary.txt` |
| Firmware gate set (`docs/testing/CI_WORKFLOWS.md`, the firmware block) | `fw_rv32_selftest.py --require-rv32`; `tally_selftest.py --mutants`; `test_ctrl_firmware_shards.py`; `fw_coverage.py --selftest`; `test_ctrl_firmware.py --require-rv32 --self-test --lwsrp third_party/lwSRP --jobs 8`; `test_ctrl_nvm.py --require-rv32 --self-test --jobs 8`; `fw_coverage.py --check --lwsrp third_party/lwSRP --jobs 8`; `ctrl_boundary.py --require-rv32 --selftest` | all 8 rc 0; `test_ctrl_firmware: PASS`; 435 NVM tests, 109 / 109 planted defects caught; coverage PASS (30 files); `ctrl_boundary: PASS` | `receipts/firmware/` |
| rtl-fast replica | the workflow's `run:` bodies, `scripts/rtl_fast_steps.py`; combined by `scripts/rtlfast_combine.py` | 11 / 11 `needs:` jobs success (`changes` rtl=true). verilator-lint, bdd-conformance (`behave --no-capture -f plain` in `tests/`: 406 scenarios), yosys-elaboration and publication-census come from run 1. `changes` and the six firmware jobs come from run 2 (see Environment notes). Clone clean, head unchanged | `receipts/rtl_fast/` |
| Pin-record checks | `pp_resource_gate.py check-baseline`; `ooc.sh --record-rom-digests` then `git diff --exit-code syn/yosys/rom_digests.tsv`; `submodule_boundaries.gen.py --check`; `timesync_chain.gen.py --check`; `check_submodule_docs.py`; `check_gptp_docs.py --with-submodule`; `check_port_contracts.py`; `measure_naming.py --check`; `measure_test_evidence.py --check`; `protocol-processor/scripts/check-integrator-params.py` | all 11 rc 0; the ROM ledger regenerates byte-identically; clone clean after | `receipts/pinchecks/` |
| behave | `cd tests && behave --no-capture -f plain` | 14 features, 406 scenarios, 1,977 steps passed, 0 failed | `receipts/bdd/` |
| Yosys | `syn/yosys` open-synthesis check via sv2v (Yosys 0.66, sv2v v0.0.12) | 60 / 60 tops; tied-input gate PASS; tap-purity PASS | `receipts/yosys/` |
| lint | `python3 scripts/lint_rtl.py --check` (Verilator 5.050) | "LINT GATE: PASS (89 violation(s) <= ratchet 89; 19 waived, 0 justified lint_off)" | `receipts/lint/` |
| Docs gates, GNU Make 4.3 | the docs workflow's step bodies (`scripts/docs_steps.py`) | 44 steps: 41 rc 0 and 2 skipped by rule. Builder leg 1 (`gate_25_1`) was rc 1 on the first pass (below) and rc 0 with the LiteX interpreter. The five markdown gates are rc 0 on CPython 3.12.3, and the no-git step's two gates are rc 0 | `receipts/docs_gates/` |
| route-1x1, ooc-1x1, ooc-8x8 | the recipe's Vivado flows, then `syn/ooc/pp_resource_gate.py check` | RESULT: PASS at all three (table above) | `receipts/vivado/` |

### Docs builder leg 1

On the first pass, `gate_25_1` failed in `test_nvm_firmware_shapes`, in its `test_nvm_firmware.py --self-test`
subprocess. The sweep was loading the host while that pass ran.

- The same self-test passes when run alone in the same clone with the same interpreter: rc 0, 166 s, "saved-state
  writer gate: OK across 5 shape(s), and every planted defect reddened".
- The leg passes (rc 0, 304 s) when run with the LiteX interpreter.
- The leg also passes on CPython 3.12.3 without LiteX, the configuration of the first pass, rerun on a quiet host
  (rc 0, 208 s; `receipts/docs_gates/leg1-ci312.*`).
- The test exercises the NVM saved-state writer, which neither this change nor processor #200 touches.

The failure is therefore transient and unrelated to the status change, and the STOP condition does not apply.

## Environment notes

- The rtl-fast replica's firmware jobs first failed at "Install and verify the pinned RV32 SDK" with "SDK
  provenance mismatch". The SDK in that HOME was a copy whose receipt names another directory.
  - The replica now uses its own HOME. `scripts/ci_rv32_sdk.py --archive` installed the SDK there from the pinned
    archive (sha256 `d42680e9...`, verified by the installer).
  - The six firmware jobs were then rerun at the same head.
