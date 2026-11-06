# The three re-pinned command-table rows, read against their declarations

`docs/testing/CI_IMAGE.md` says a changed declared script refuses generation until reviewed again.
The checker cannot reach these three rows at this dev: it refuses first at `sw/builder/endstation_builder.py` (#838).
See `table-checker.log`. So this is the executor's reading of each diff against dev, not a walker result, and it is not a review verdict.

| Row | Declared class and reason, unchanged | Change against dev `87e9d03a` | New process, argument form or install |
|---|---|---|---|
| `tb/verilator/fw_service_budget/run.py` | reviewed non-installing: "Runs a built firmware service-budget simulation and records measured counters." | The poll charge's transaction count 9 becomes 16, with its comment, and one self-test boundary value 374.9982 becomes 374.9975 with its derivation | None |
| `tb/verilator/nvm_capture_cpu/run.py` | reviewed non-installing: "Capture harness; builds the probe with Verilator and runs the simulator it built; installs nothing." | One more constant, `station_mac`, in the generated `probe_config.hpp` | None; the `verilator` argument list is unchanged |
| `tb/verilator/nvm_capture_cpu/soc.py` | reviewed non-installing: "Capture SoC generator; drives the pinned LiteX builder, which compiles SoC software with the image compiler and emits simulation sources without starting a simulation; installs nothing." | One more key, `station_mac`, in the spec JSON, parsed from `platform.mac_address` | None |

Each row's `class` and `reason` text is unchanged, and only the `sha256` line moved.
