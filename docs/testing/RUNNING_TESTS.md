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
python3 scripts/check_soc_sources.py
python3 scripts/check_sweep_shape.py --self-test
```

For a full SoC elaboration without launching Vivado, invoke the intended
`sw/litex/build.sh` recipe with its build action disabled. Inspect the emitted
Verilog as well as the Python return status: Migen can represent an expression
that a downstream Verilog front end rejects.

The small `sw/litex/test_*.py` inventory now covers only integration helpers
that remain in the bare-metal SoC. The deleted memory-delivery engines and
their behavioral models are not a product contract. Treat `ls sw/litex/test_*.py`
as the inventory and run each tracked script directly with Python.

## 2. Verilator suites

Each directory below `tb/verilator/` that contains a `Makefile` is a
self-checking suite. Run one affected suite while iterating:

```sh
make -C tb/verilator/milan_dp
make -C tb/verilator/pp_shadow
make -C tb/verilator/csr
```

Run the complete inventory before release review:

```sh
suite_logs=$(mktemp -d)
scripts/run_all_suites.sh "$suite_logs"
```

The runner discovers suites from the filesystem, serializes whole-tree sweeps,
enforces a per-suite wall clock, and refuses to quote a total when a suite's
check count cannot be read. CI uses the same inventory split into deterministic
shards. Inspect the assignment without compiling with:

```sh
scripts/run_all_suites.sh --shard 0/4 --list
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
change:

```sh
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

Gate the final candidate on non-negative post-route WNS and the placed
utilization report. For AX7101 release candidates, retain comfortable timing
margin and run the configured placement-directive sweep; an elaboration or
out-of-context estimate is not a substitute for the placed design.

## 6. Silicon acceptance

After flashing or JTAG-loading a candidate, run the UART grader from the bench
workstation:

```sh
python3 scripts/baremetal_uart_smoke.py \
  --port /dev/serial/by-id/<adapter>
```

Require `ID=MILN`, `VERSION=0x0002_0057`, a loaded AEM image, enabled
PTP/ADP/protocol processing, nonzero GM and parent identities, a bounded
measured peer delay, a published path, `sync=1`, `asCapable=1`,
`time_uncertain=0`, and two increasing PHC reads.

Then generate and capture traffic with an external workstation or instrument.
Preserve the exact bitstream identity, generated configuration, UART
transcript, packet capture, and any external CSR transcript with the result.
The UART intentionally exposes a small documented command set; it is not a
general register shell.

Physical and two-board acceptance for this change remains tracked in issue
#117.

## Debug loop

1. Capture a reproducible wire/UART/CSR fingerprint on the candidate.
2. Reproduce the same packet and timing conditions in the narrowest RTL suite.
3. Add cycle-numbered observation at the first divergent fabric boundary.
4. Fix the owning layer, rerun its focused suite, then run the full gates before
   producing one new board candidate.
