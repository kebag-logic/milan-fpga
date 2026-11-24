STATUS: LOCAL VALIDATION COMPLETE

# [A837] REVIEW READY

PR: 966

Commit: `44c566399002db32bf8a6ad3ce719488d418bcb0`. Base of this repair: `165476c755e4728a044c12ea6bc33ce0a0a9d28f`.
Branch: `884-gptp-firmware`; PR base: `dev-soft-core-optimisation`.
Local commits only. No push, PR edit or review verdict is claimed.

The coverage repair adds two AECP face tests and two mailbox-driver tests, with one planted defect per test.
They cover software snapshot fields, path callback capacity/refusal, timestamp flags and both time words across
ring wrap, and publication ordering with one final generation commit. The ratchet restores the face and driver
to 100% lines and branches, removes the stale platform gate exclusion, and records both gPTP files. No recorded
figure is lowered. The cancelled-job replay exposed test-build integration omissions; the gPTP simulation now
honors STACK_DIR and its pin and is captured by the boundary gate. Both defect campaigns have explicit suite
classification. The two driver mutations live in a focused table; all 828 entries and their order are identical
to the inline version used when shard 1 started. No product C or RTL changed.

| File | Lines | Branches |
|---|---:|---:|
| aecp_face.c | 229/229 | 204/204 |
| mbx.c | 384/384 | 202/202 |
| ctrl_plat.c | 224/224 | 110/110 |
| gptp.h | 2/2 | 0/0 |
| gptp.c | 665/704 | 346/437 |

Coverage at 7ad1e7df is rc 0. The final commit corrects README prose only; all 21 parsed exclusions and all ratchet figures are identical (coverage-readme-identity.log). The commands below are the substantive local job steps, with the available
pinned tools. Hosted setup/cache/upload/cancellation actions are not represented as local tests. No hosted green
context or exact-remote-head act replica is claimed; the manager controls pushing and review. The candidate
runner's offline self-test ran only inside a disposable, unprivileged container with no credentials or Docker
socket, not as a host orchestrator.

## Validation

| Check | Exit code | Seconds | Receipt under receipts/966 |
|---|---:|---:|---|
| Coverage ratchet | 0 | 711.9 | `coverage-7ad1.log` |
| Firmware shard 0/4 with RV32 and planted defects | 0 | 1077.9 | `fw-shard-0-final.log` |
| Firmware shard 1/4 with RV32 and planted defects | 0 | 3867.4 | `fw-shard-1-final.log` |
| Firmware shard 2/4 with RV32 and planted defects | 0 | 2256.7 | `fw-shard-2-final.log` |
| Firmware shard 3/4 with RV32 and planted defects | 0 | 2547.8 | `fw-shard-3-final.log` |
| Boundary builders without Verilator | 0 | 2722.7 | `firmware-boundary-edd31.log` |
| Boundary builders with Verilator | 0 | 1540.1 | `firmware-verilator-edd31.log` |
| Documentation workflow aggregate (original result) | 1 | 2373.1 | `docs-final.log` |
| Python idiom corrected replay | 0 | 18.1 | `python-idiom-7ad1.log` |
| Final documentation, inventory and whitespace checks | 0 | 19.5 | `docs-44c5.log` |
| Yosys elaborate workflow, five steps | 0 | 976.2 | `yosys-elaboration.log` |
| Ratcheted lint and source-list derivation | 0 | 22.0 | `verilator-lint-retry.log` |
| Specification-facing tests | 0 | 3.7 | `bdd-conformance-retry.log` |
| Split crossing checks | 0 | 121.1 | `split-cdc.log` |
| Publication census and controls | 0 | 3138.4 | `publication-census.log` |
| Builder with elaboration and RV32 required | 0 | 2488.9 | `builder.log` |
| LiteX aggregate (original timeout retained) | 92 | 2270.7 | `litex.log` |
| LiteX timing-cut corrected timeout replay | 0 | 1269.1 | `litex-timing-final.log` |
| LiteX runner self-test | 0 | 4.0 | `litex-selftest.log` |
| NVM firmware gate | 0 | 166.5 | `firmware-nvm.log` |
| Coverage controls | 0 | 0.4 | `coverage-selftest.log` |
| Verdict tally controls | 0 | 4.3 | `tally-selftest.log` |
| RV32 gate controls | 0 | 8.5 | `rv32-selftest.log` |
| Runner offline controls inside disposable container | 0 | 147.4 | `act-offline-exec.log` |
| gPTP simulation baseline | 0 | 635.5 | `gptp-simulation.log` |
| gPTP simulation planted defects | 0 | 2541.5 | `gptp-simulation-mutants.log` |

Documentation has a passing result for each of its 42 substantive steps after the focused Python idiom replay.
The original aggregate rc 1 is retained; its only failure was the new inline mutation entries taking a module
past 1000 lines. Extracting them fixed it without changing any mutation. LiteX has eight passing checks after
the timing-cut replay: its first run exceeded the default 900 s wall-clock limit (unknown, rc 92); the replay
completed in 1269 s under a 7200 s limit without changing assertions.

The full builder returned rc 0 and explicitly reported two uncovered arms: the build-flags mutation is inert
with the available make, and the historical placed-resource calibration report is absent. Neither is counted
as a pass. Previous failed or superseded runs remain in the receipt index. Their passing replacements are
identified above; an interrupted run does not count as evidence.

`receipts/966/input-equivalence.json` records the tested-input relationship across local commits. The four
firmware shards started with the tests at 17bd60c6; subsequent C/C++ test inputs are identical, and the driver's
mutation serialization proves the refactor preserves all entries. Both boundary legs were restarted after the
registry change. Coverage and the Python idiom check ran at 7ad1e7df before the final README prose correction; the documentation checks were replayed after it. The changed Makefile was exercised
by the closed loop and its planted-copy campaign.

`receipts/INDEX.md` indexes bounded plain-text receipts and hashes. Reproduction wrappers and environment are
under `receipts/reproduce`; source logs and build products remain in the named scratch directory. This packet
provides author evidence for independent review, not an author's approval of the PR.

## Exact commands

### Coverage ratchet

Working directory: `/data-2/milan/lanes/opt-gptp-sw`.
Launch head: `7ad1e7df55d8516ce9f8080d3400320719e3f6d0`.

```sh
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep /data-2/milan/tmp/opt-a837/coverage-7ad1
```

### Firmware shard 0/4 with RV32 and planted defects

Working directory: `/data-2/milan/tmp/opt-a837/fw-cwd-0`.
Launch head: `17bd60c6989f9db53407dec06a245feba36656df`.

```sh
python3 /data-2/milan/lanes/opt-gptp-sw/sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4 --build-dir /data-2/milan/tmp/opt-a837/fw-shard-0
```

### Firmware shard 1/4 with RV32 and planted defects

Working directory: `/data-2/milan/tmp/opt-a837/fw-cwd-1`.
Launch head: `17bd60c6989f9db53407dec06a245feba36656df`.

```sh
python3 /data-2/milan/lanes/opt-gptp-sw/sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 1/4 --build-dir /data-2/milan/tmp/opt-a837/fw-shard-1
```

### Firmware shard 2/4 with RV32 and planted defects

Working directory: `/data-2/milan/tmp/opt-a837/fw-cwd-2`.
Launch head: `17bd60c6989f9db53407dec06a245feba36656df`.

```sh
python3 /data-2/milan/lanes/opt-gptp-sw/sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 2/4 --build-dir /data-2/milan/tmp/opt-a837/fw-shard-2
```

### Firmware shard 3/4 with RV32 and planted defects

Working directory: `/data-2/milan/tmp/opt-a837/fw-cwd-3`.
Launch head: `17bd60c6989f9db53407dec06a245feba36656df`.

```sh
python3 /data-2/milan/lanes/opt-gptp-sw/sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 3/4 --build-dir /data-2/milan/tmp/opt-a837/fw-shard-3
```

### Boundary builders without Verilator

Working directory: `/data-2/milan/lanes/opt-gptp-sw`.
Launch head: `edd31d4d349e147aa7a20cc1ad854ec901263d31`.

```sh
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator
```

### Boundary builders with Verilator

Working directory: `/data-2/milan/lanes/opt-gptp-sw`.
Launch head: `edd31d4d349e147aa7a20cc1ad854ec901263d31`.

```sh
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator
```

### Documentation workflow aggregate (original result)

Working directory: `/data-2/milan/lanes/opt-gptp-sw`.
Launch head: `17bd60c6989f9db53407dec06a245feba36656df`.

```sh
python3 /data-2/milan/tmp/opt-a837/workflow_steps.py docs
```

### Python idiom corrected replay

Working directory: `/data-2/milan/lanes/opt-gptp-sw`.
Launch head: `7ad1e7df55d8516ce9f8080d3400320719e3f6d0`.

```sh
python3 scripts/check_py_idiom.py
```

### Final documentation, inventory and whitespace checks

Working directory: `/data-2/milan/lanes/opt-gptp-sw`.
Launch head: `44c566399002db32bf8a6ad3ce719488d418bcb0`.

```sh
python3 /data-2/milan/tmp/opt-a837/docs_head.py
```

### Yosys elaborate workflow, five steps

Working directory: `/data-2/milan/lanes/opt-gptp-sw`.
Launch head: `not embedded in this early receipt; see input-equivalence.json`.

```sh
python3 /data-2/milan/tmp/opt-a837/workflow_steps.py yosys-elaboration
```

### Ratcheted lint and source-list derivation

Working directory: `/data-2/milan/lanes/opt-gptp-sw`.
Launch head: `1fe17e3c74ae1feac6961c9c16699fb107d8da97`.

```sh
python3 /data-2/milan/tmp/opt-a837/workflow_steps.py verilator-lint
```

### Specification-facing tests

Working directory: `/data-2/milan/lanes/opt-gptp-sw`.
Launch head: `1fe17e3c74ae1feac6961c9c16699fb107d8da97`.

```sh
python3 /data-2/milan/tmp/opt-a837/workflow_steps.py bdd-conformance
```

### Split crossing checks

Working directory: `/data-2/milan/lanes/opt-gptp-sw`.
Launch head: `not embedded in this early receipt; see input-equivalence.json`.

```sh
python3 /data-2/milan/tmp/opt-a837/workflow_steps.py split-cdc
```

### Publication census and controls

Working directory: `/data-2/milan/lanes/opt-gptp-sw`.
Launch head: `not embedded in this early receipt; see input-equivalence.json`.

```sh
python3 /data-2/milan/tmp/opt-a837/workflow_steps.py publication-census
```

### Builder with elaboration and RV32 required

Working directory: `/data-2/milan/lanes/opt-gptp-sw`.
Launch head: `not embedded in this early receipt; see input-equivalence.json`.

```sh
python3 sw/builder/test_builder.py --require-elaboration --require-rv32 --receipt /data-2/milan/tmp/opt-a837/builder-receipt.json
```

### LiteX aggregate (original timeout retained)

Working directory: `/data-2/milan/lanes/opt-gptp-sw`.
Launch head: `not embedded in this early receipt; see input-equivalence.json`.

```sh
scripts/run_litex_sims.sh /data-2/milan/tmp/opt-a837/litex-sim-logs
```

### LiteX timing-cut corrected timeout replay

Working directory: `/data-2/milan/lanes/opt-gptp-sw`.
Launch head: `e48ff320e17c22f2e577087e3c4b72a579fd02cd`.

```sh
scripts/run_litex_sims.sh /data-2/milan/tmp/opt-a837/litex-timing-logs --only test_soc_timing_cuts
```

### LiteX runner self-test

Working directory: `/data-2/milan/lanes/opt-gptp-sw`.
Launch head: `17bd60c6989f9db53407dec06a245feba36656df`.

```sh
scripts/run_litex_sims.sh --selftest
```

### NVM firmware gate

Working directory: `/data-2/milan/lanes/opt-gptp-sw`.
Launch head: `17bd60c6989f9db53407dec06a245feba36656df`.

```sh
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
```

### Coverage controls

Working directory: `/data-2/milan/lanes/opt-gptp-sw`.
Launch head: `17bd60c6989f9db53407dec06a245feba36656df`.

```sh
python3 sw/firmware/gtest/fw_coverage.py --selftest
```

### Verdict tally controls

Working directory: `/data-2/milan/lanes/opt-gptp-sw`.
Launch head: `17bd60c6989f9db53407dec06a245feba36656df`.

```sh
python3 sw/firmware/gtest/tally_selftest.py
```

### RV32 gate controls

Working directory: `/data-2/milan/lanes/opt-gptp-sw`.
Launch head: `17bd60c6989f9db53407dec06a245feba36656df`.

```sh
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
```

### Runner offline controls inside disposable container

Working directory: `/data-2/milan/lanes/opt-gptp-sw`.
Launch head: `17bd60c6989f9db53407dec06a245feba36656df`.

```sh
sudo -n docker run --rm --network none --cap-drop ALL --security-opt no-new-privileges --read-only --tmpfs /tmp:rw,exec,nosuid,nodev,size=1g --user 1000:1000 --env GITHUB_WORKSPACE=/work --mount type=bind,src=/data-2/milan/lanes/opt-gptp-sw,dst=/work,readonly --mount type=bind,src=/data-2/milan/tmp/opt-a837/act-offline-step.sh,dst=/step.sh,readonly --workdir /work ghcr.io/kebag-logic/milan-ci-tools:repo-link bash /step.sh
```

### gPTP simulation baseline

Working directory: `/data-2/milan/lanes/opt-gptp-sw`.
Launch head: `ee9b42b103a02f5ea55f3a3611c538d96273e3c8`.

```sh
make -C tb/verilator/gptp_sw all MDIR=/data-2/milan/tmp/opt-a837/gptp-simulation -j4
```

### gPTP simulation planted defects

Working directory: `/data-2/milan/lanes/opt-gptp-sw`.
Launch head: `e48ff320e17c22f2e577087e3c4b72a579fd02cd`.

```sh
python3 tb/verilator/gptp_sw/gptp_sw_mutants.py --jobs 2 --build-dir /data-2/milan/tmp/opt-a837/gptp-simulation-mutants
```
