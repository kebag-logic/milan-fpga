[A287]

Commands and complete receipts for processor `4f6185ce97e31f3bdacc090ec1ab7ede32456d2e`
and local parent `399cb14f75ad1c73995bca4a0adebfab607dd640`.
`$PROCESSOR` and `$PARENT` name their respective checkouts, `$OUTPUT` this receipt
directory, and `$SCRATCH` a temporary directory outside it. `$VERILATOR` is the
CI-pinned 5.050 executable. The gate runner puts its directory first on PATH and
caps inherited CPU affinity at eight CPUs. Each command runs in the foreground,
without piping its output, with a 14,400-second command timeout; logs preserve
the command's own exit status. Individual probe subprocess timeouts are those of
the original runners.

The workflow's documentation commands are all included in `make check`:
`python3 scripts/check-links.py`, `python3 scripts/check-matrix.py`,
`python3 scripts/render-wavedrom.py --check`, and `make stale`. It also runs
diagram lint and `python3 scripts/gen_matrix.py --check`, covering the separate
workflow traceability step. Provisioning steps are satisfied by installed tools;
their versions are recorded in [tool-versions.json](tool-versions.json).
The workflow's required historical ref was fetched successfully with
`git fetch --no-tags origin refs/pull/13/head` before the NVM figures gate.

| Gate | Working directory | Command | rc | Seconds | Receipts |
|---|---|---|---:|---:|---|
| focused-live-peers | `$PROCESSOR` | `make -C tb/pp_top gsi-internal` | 0 | 29.54 | [status](focused-live-peers.json), [log](focused-live-peers.log) |
| docs-final | `$PROCESSOR` | `make check` | 0 | 34.7 | [status](docs-final.json), [log](docs-final.log) |
| lint | `$PROCESSOR` | `./scripts/lint_hdl.sh` | 0 | 8.19 | [status](lint.json), [log](lint.log) |
| suites | `$PROCESSOR` | `./scripts/run_suites.sh` | 0 | 260.08 | [status](suites.json), [log](suites.log) |
| nvm-figures | `$PROCESSOR` | `make -C tb/nvm_port figures` | 0 | 278.61 | [status](nvm-figures.json), [log](nvm-figures.log) |
| yosys | `$PROCESSOR` | `./syn/yosys/run.sh` | 0 | 73.84 | [status](yosys.json), [log](yosys.log) |
| mutants | `$PROCESSOR` | `python3 tb/pp_top/gsi_mutants.py --output $OUTPUT/mutants --verilator $VERILATOR` | 0 | 790.89 | [status](mutants.json), [log](mutants.log) |
| reviewer-r310 | `$PROCESSOR` | `python3 $SCRATCH/r310_probes.py --repo $PROCESSOR --commit 4f6185ce97e31f3bdacc090ec1ab7ede32456d2e --work $SCRATCH/r310-work --out $OUTPUT/reviewer-r310 --verilator $VERILATOR --cpus 32-39 golden cmp-low3 cmp-high2 cmp-no-bit31 cmp-low16` | 0 | 193.29 | [status](reviewer-r310.json), [log](reviewer-r310.log) |
| reviewer-r311 | `$PROCESSOR` | `python3 $SCRATCH/r311_probes.py --repo $PROCESSOR --rev 4f6185ce97e31f3bdacc090ec1ab7ede32456d2e --scratch $SCRATCH/r311-work --out $OUTPUT/reviewer-r311 --verilator $VERILATOR --workers 1 --jobs 8 --only golden,r-cmp-low8,r-cmp-low16,r-cmp-high16,r-cmp-no-bit31` | 0 | 180.29 | [status](reviewer-r311.json), [log](reviewer-r311.log) |
| parent-cpp | `$PARENT` | `python3 scripts/check_cpp_idiom.py` | 0 | 2.42 | [status](parent-cpp.json), [log](parent-cpp.log) |
| parent-python | `$PARENT` | `python3 scripts/check_py_idiom.py` | 0 | 3.57 | [status](parent-python.json), [log](parent-python.log) |
| parent-xvlog | `$PARENT` | `python3 scripts/xvlog_gate.py --check` | 0 | 145.28 | [status](parent-xvlog.json), [log](parent-xvlog.log) |
| parent-source-lists | `$PARENT` | `python3 scripts/check_rtl_source_lists.py` | 0 | 1.42 | [status](parent-source-lists.json), [log](parent-source-lists.log) |
| parent-pp-srcs | `$PARENT` | `python3 scripts/pp_srcs.py --check --selftest` | 0 | 0.26 | [status](parent-pp-srcs.json), [log](parent-pp-srcs.log) |
| parent-builder | `$PARENT` | `python3 sw/builder/test_builder.py` | 0 | 389.68 | [status](parent-builder.json), [log](parent-builder.log) |
| parent-consumer | `$PARENT` | `make -C tb/verilator/pp_shadow -j8` | 0 | 6.78 | [status](parent-consumer.json), [log](parent-consumer.log) |

Probe script identities and published archive paths are in
[review-probe-provenance.json](review-probe-provenance.json). Download them into
scratch at those exact commits to reproduce the reviewer commands; they were
not modified. The full retained mutation runner remains in the processor tree.
The audit [verify_results.py](verify_results.py) checks the original bank counts,
all final rc values, completed simulations and named failures in both polarities
and both directions. Failed pre-commit development output is isolated under
`iterations/`; it is not evidence for the committed head.

Parent limits: the front-end gate retains four existing findings, the source-list
gate reports 35 of 41 native tops with six recorded omissions, and the builder's
historical resource-calibration arm is unrun because its reference placement
report is absent. The requested commands themselves all return rc 0.
