# Running the tests

This is the execution guide for the current bare-metal product tree. Run the
cheap structural checks first, then the RTL suites, synthesis, and finally the
board acceptance lane.

## Contents

- **[1. LiteX and builder checks](#1-litex-and-builder-checks)** — Fast configuration, generated-artifact, source, and elaboration checks for the SoC.
- **[2. Verilator suites](#2-verilator-suites)** — Running one affected RTL harness or the complete discovered suite inventory.
- **[3. Protocol campaigns and behavior tests](#3-protocol-campaigns-and-behavior-tests)** — Processor-native and standards-facing campaigns for control, time, media, and robustness.
- **[4. Yosys portability and static gates](#4-yosys-portability-and-static-gates)** — Open synthesis plus documentation, source, contract, and hygiene checks.
- **[5. Place and route](#5-place-and-route)** — Candidate implementation, timing closure, and placed-resource evidence.
- **[6. Silicon acceptance](#6-silicon-acceptance)** — UART grading and external-wire measurements on the exact flashed artifacts.
- **[Debug loop](#debug-loop)** — The shortest evidence-preserving iteration sequence for a failing layer.

## 1. LiteX and builder checks

Start with an import and the builder's generated-artifact tests:

```sh
python3 -c "import sys; sys.path.insert(0, 'sw/litex'); import milan_soc"
python3 sw/builder/test_builder.py
python3 avdecc/gen_aem_store.py --self-test
python3 scripts/check_soc_sources.py
python3 scripts/check_sweep_shape.py --self-test
python3 scripts/check_deploy_shape.py --selftest
python3 sw/litex/iob_pack_selftest.py
```

For a full SoC elaboration without launching Vivado, invoke the intended
`sw/litex/build.sh` recipe with its build action disabled. Inspect the emitted
Verilog as well as the Python return status: Migen can represent an expression
that a downstream Verilog front end rejects.

The small `sw/litex/test_*.py` inventory now covers only integration helpers
that remain in the bare-metal SoC. The deleted memory-delivery engines and
their behavioral models are not a product contract. Treat `ls sw/litex/test_*.py`
as the inventory and run each tracked script directly with Python.

One local check sits outside that inventory, because it is not a `test_*.py`
file: [`sw/litex/iob_pack_selftest.py`](../../sw/litex/iob_pack_selftest.py)
drives [`sw/litex/iob_pack_check.tcl`](../../sw/litex/iob_pack_check.tcl)
(issue #475) in `tclsh` over stubbed netlists, which is the only gate that
check has outside a Vivado build. It is in the list above, and the
`docs-check` job runs it. It does not stand in for a live run: changing that
Tcl requires one on a placed checkpoint, in the four lines
[BUILDING](../integration/BUILDING.md) section 5 gives.

## 2. Verilator suites

Each directory below `tb/verilator/` that contains a `Makefile` is a
self-checking suite. Run one affected suite while iterating:

```sh
make -C tb/verilator/milan_dp
make -C tb/verilator/pp_shadow
make -C tb/verilator/csr
```

Run both selections for the complete inventory before release review:

```sh
suite_logs=$(mktemp -d)
scripts/run_all_suites.sh "$suite_logs"
physical_suite_logs=$(mktemp -d)
scripts/run_all_suites.sh "$physical_suite_logs" --physical-gptp
```

The runner needs Git 2.39.0 or newer: it gates the post-merge containment
self-test, which uses `git patch-id --verbatim`, and an older Git is refused
by name before any suite runs. That self-test exits 3 when every arm passed
but a temporary tree it built could not be removed; the runner prints a
`CLEANUP:` notice and carries on, because no verdict is in doubt, while any
other failure still aborts the sweep.
It preserves historical linear replay verdicts after later reversions.
It also tests the separate, optional `--current-retention` arm.
That arm measures bytes and entries, without inferring supersession intent.
See the [containment contract](../../CONTRIBUTING.md#21-the-issue-to-merge-lane)
for its supported histories and unresolved cases.
The runner discovers suites from the filesystem, serializes whole-tree sweeps,
enforces a per-suite wall clock, and refuses to quote a total when a suite's
check count cannot be read. The default selection contains 54 suites, each
with an 1800-second deadline except `milan_dp`, which has 3600 seconds
under [decision 5820240308](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5820240308).
The separate `milan_dp_gptp` selection uses
5400 seconds, including compilation, and preserves physical clock and timer
rates. CI shards the default selection; the physical job runs nightly and on
manual dispatch. Inspect both selections without compiling with:

```sh
scripts/run_all_suites.sh --shard 0/5 --list
scripts/run_all_suites.sh --physical-gptp --list
```

The `milan_dp` suite is the integration authority for MAC-facing wire traffic,
fabric AAF/TDM/I2S routing, protocol-processor merges, and the fabric gPTP
option. The direct option-OFF shape is verification-only: it must publish zero
GM, parent, path, and peer-delay state, remain unsynchronized and not
AS-capable, set time-uncertain, ignore legacy publication writes, and emit no
gPTP traffic.

## 3. Protocol campaigns and behavior tests

The pinned processor repositories own their native protocol suites. The
superproject additionally runs the generated AAF and gPTP wire campaigns from
`tb/verilator/tsn_fuzz` against the pinned `tsn-gen` revision. Set
`TSN_GEN_ROOT` to that checkout when running them locally.

Run the repository behavior layer with:

```sh
behave tests/features
```

These scenarios exercise cross-artifact contracts and external-tool evidence;
they complement, rather than replace, the cycle-accurate RTL harnesses.

## 4. Yosys portability and static gates

```sh
syn/yosys/run.sh
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_baremetal_only.py --selftest
python3 scripts/check_rtl_source_lists.py --selftest
python3 scripts/lint_rtl.py
python3 docs/traceability/gen_module_matrix.py --check
```

`syn/yosys/run.sh` elaborates the authoritative top inventory and maps it to a
generic cell library. The source-list gate independently walks the
`milan_datapath` module closure and asks every synthesis/simulation consumer
for its real source expansion.

Run the documentation and traceability checks after any path or architecture
change. `gen_toc.py` reads Markdown through the hash-locked renderer, so
install its lock once first:

```sh
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
python3 scripts/docs_check.py
python3 scripts/check_doc_paths.py
python3 scripts/gen_toc.py --check
python3 scripts/check_feature_status.py
```

## 5. Place and route

The canonical launcher is:

```sh
sw/litex/build.sh <config> [<config> ...] [--sweep]
```

Gate the final AX7101 candidate on WNS >= +0.03 ns and WHS >= 0
at every declared corner, and on the placed utilization report.
Run the configured placement-directive sweep and select its seed manually.
The timing thresholds are **not automatically enforced**, as the
[margin correction](https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5860783553) confirms.
An elaboration or out-of-context estimate is not a substitute for the placed design.

The AX7101 dev-board release claims **commercial grade, 0 to 85 C junction**.
The part and conditions come from
[`TIMING_GRADE`](../../sw/litex/platforms/ax7101_timing.py); the full builder
bank pins this declaration and exercises wrong-condition refusals.
Every candidate enables setup and hold at both Slow and Fast timing corners.
Artix-7 supplies fixed speed models, so the two temperature-endpoint reports
repeat each model rather than represent four independent PVT models.
Power-estimation junction temperature does not prorate timing delays.
The [margin decision](https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5860418611)
requires WNS >= +0.03 ns and WHS >= 0.
Apply both thresholds at every declared corner.

Use the saved-checkpoint command in
[BUILDING section 5](../integration/BUILDING.md#5-gates-before-a-build-is-good)
to retain WNS/TNS/WHS/THS per model and endpoint, clock interaction, CDC and
unconstrained-path evidence. Retain the implementation log's CRITICAL WARNING census too.
Record negative-slack paths without hiding them
behind the command's exit status. Positive WNS does not discharge CDC findings,
missing external I/O constraints, or #395's physical temperature and oscillator
measurements. The [candidate record](../findings/COMMERCIAL_TIMING_395.md)
contains the measured table and report limitations.

Issue #607's constraint tests run in the complete builder bank.
They elaborate both shipping AX7101 configurations with either GMII port.
The real build Tcl must carry the namespace-derived clock hook.
It must run between synthesis and optimization.
The generated XDC must omit the generic MultiReg false path.
These elaborations compile no firmware and run no vendor implementation.
Other controls check exception scope and conditional quasi-static constraints.
Log controls refuse `12-4739`, `20-1307` and `12-5201`.
Refused bitstreams must become `*.bit.rejected`, outside automatic discovery.
A live planted wrong clock name can also be checked against a
read-only routed checkpoint, using an interpreter with the build packages:

```sh
python3 sw/builder/test_clock_constraints.py \
  --vivado /path/to/vivado --checkpoint /path/to/routed.dcp
```

The live control uses at most 16 threads and never saves the checkpoint.
Set `TMPDIR` to the desired physical build storage before running it.
Retain each seed's clock-interaction report and bound slack, as specified in
[BUILDING section 5](../integration/BUILDING.md#5-gates-before-a-build-is-good).
For AX7101, the manual margin rule is WNS >= +0.03 ns and WHS >= 0 at every
corner; a completed implementation alone does not establish those margins.

## 6. Silicon acceptance

After flashing or JTAG-loading a candidate, run the UART grader from the build
box, which carries the AX7101 console and JTAG:

```sh
python3 scripts/baremetal_uart_smoke.py \
  --port /dev/serial/by-id/<adapter>
```

Require `ID=MILN`, `VERSION=0x0002_0060`, a loaded AEM image, enabled
PTP/ADP/protocol processing, nonzero GM and parent identities, a bounded
measured peer delay, a published path, `sync=1`, `asCapable=1`,
`time_uncertain=0`, and two increasing PHC reads.

Then generate and capture traffic from the bench hosts named in
[the build guide](../integration/BUILDING.md#41-bench-hosts-and-the-one-dut-acceptance-contract):
the controller and audio endpoint on `pw1`, the ProfiShark taps on the Ubuntu
server.
Preserve the exact bitstream identity, generated configuration, UART
transcript, packet capture, and any external CSR transcript with the result.
The UART intentionally exposes a small documented command set; it is not a
general register shell.

Physical acceptance for this change remains tracked in issue #117: one AX7101
DUT against the Milan-validated reference peer, with GM loss and return induced
through the peer or the bench AVB switch.

## Debug loop

1. Capture a reproducible wire/UART/CSR fingerprint on the candidate.
2. Reproduce the same packet and timing conditions in the narrowest RTL suite.
3. Add cycle-numbered observation at the first divergent fabric boundary.
4. Fix the owning layer, rerun its focused suite, then run the full gates before
   producing one new board candidate.
