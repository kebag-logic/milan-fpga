Use the exact reviewed checkout and a separate packet directory.
Disposable outputs belong under the packet's `scratch/` directory.
The repository's pinned build prerequisites must already be available.
No installation, hardware access or remote write is required.

Set `CHECKOUT`, `PACKET`, and `PYTHON` to the checkout, packet and interpreter.
For native runs, put the pinned 5.050 executable and RV32 SDK on `PATH`.
Set `LITEX_ENV_CC_TRIPLE` to the SDK prefix, without `-gcc`.
Set `PYTHONHASHSEED=0`, `COURSIER_MODE=offline` and `SBT_OPTS=-Dsbt.offline=true`.
Run from `CHECKOUT` and keep every invocation in the foreground.

The native head runs were:

```sh
"$PYTHON" -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --variant answering-ports --groups aecp-largest-notice --record-budget-findings --jobs 4 --build-dir "$PACKET/scratch/native-head-ap"
"$PYTHON" -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --variant declaring-outputs --groups aecp-largest-notice --record-budget-findings --jobs 4 --build-dir "$PACKET/scratch/native-head-do"
"$PYTHON" -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --variant answering-ports --groups aecp-largest-notice --record-budget-findings --jobs 4 --build-dir "$PACKET/scratch/native-head-1x1"
```

Each build invokes `make -j16`. Schedule the builds separately.
Independent simulations and controls may overlap within 16 jobs and 12 GB.
All three native head invocations must return zero.

For each head directory, run:

```sh
"$PYTHON" -B "$PACKET/reproduce_base.py" "$CHECKOUT" "$PACKET" "$PACKET/scratch/native-head-ap"
"$PYTHON" -B "$PACKET/reproduce_base.py" "$CHECKOUT" "$PACKET" "$PACKET/scratch/native-head-do"
"$PYTHON" -B "$PACKET/reproduce_base.py" "$CHECKOUT" "$PACKET" "$PACKET/scratch/native-head-1x1"
"$PYTHON" -B "$PACKET/collect_native.py" "$PACKET"
```

The base reproduction replaces only `aecp_maps.c` in a disposable firmware copy with its exact base blob.
That is the sole production-source delta between the base and head.
It recompiles the firmware and verifies every function address and size, all module spans,
and all loaded bytes outside `aecp_map_command` before reusing the native model.
It verifies the original ROM initialization against the head ELF before substituting the base bytes.
Both 8x8 base runs must report two passes over the share; 1x1 must report none.
The driver returns zero when execution and probe grading are complete; `native-summary.json`
separately reports the strict share verdict, which is one for the two expected base failures.
This reuse method does not claim a second independent elaboration of identical RTL.

The focused host and harness checks were:

```sh
"$PYTHON" -B sw/firmware/ctrl/test/aecp_arms.py --core --interfaces 2 --output "$PACKET/scratch/core"
"$PYTHON" -B "$PACKET/probe.py" "$CHECKOUT" "$PACKET"
"$PYTHON" -B sw/firmware/ctrl/test/test_ctrl_firmware_shards.py --census "$PACKET/shard-census.json"
"$PYTHON" -B "$PACKET/harness_parallel.py" "$CHECKOUT" "$PACKET"
"$PYTHON" -B "$PACKET/verify_integrity.py" "$CHECKOUT"
```

The harness wrapper partitions all 295 existing controls across eight fresh processes.
Every process runs the unchanged complete baseline checks, then its disjoint mutation subset.
The earlier serial self-test was stopped for scheduling and is not counted as a pass.
Two preliminary base-driver setup attempts failed before execution; the final script fixes
symbol-table generation and handles every ROM bank. Only completed reruns are counted.

For the public evidence audit, extract only `review-evidence/963-r1` from
`e31126d8e3c975f09a9c539f1496d3bccf44e8f2` beneath `PACKET/scratch`.
Then run:

```sh
"$PYTHON" -B "$PACKET/audit_receipts.py" "$PACKET"
"$PYTHON" -B "$PACKET/group_census.py" "$CHECKOUT" "$PACKET"
```

The audit verifies 703 published hashes and 481 unique pairs.
It does not turn the author's complete campaign into a reviewer execution.
Native `.log.gz` files contain the complete raw simulation logs, with no field redaction.
Host diagnostics replace only absolute local path prefixes with role placeholders;
their pre-redaction hashes are recorded in `publication-paths.json`.
