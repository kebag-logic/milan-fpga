# [A385] Combined firmware lane handoff

Status: author implementation and assigned local validation complete; independent review pending.
Head: `792a57b092efaee8920f344faacb7675c8e163bd`. Branch: `590-592-599-firmware`.
Origin: `https://github.com/kebag-logic/milan-fpga.git`.
[Assignment](https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5859537529).
[Scope correction](https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5859930453).
Internal reviewer: [R368]. External reviewer: [R369].

The preserved draft became three per-issue commits: #590 `4befe3f0d`, #592 `a133358f9`, #599 `f420e1a73`.
Merge `42f7f4fe7` incorporated dev `20aa4eabf` without conflicts or resolution edits.
The processor is initialized at `16be6768f710e79450aace277abacd6c2c3336e5`.
Commit `999a03255` changes only the authorized builder selection count from 2 to 4.
Commit `0d6f697ac` adds target service/control evidence; `7eae38744` services the wipe boundary.
Later commits bind the peer sources and record documentation and measurement evidence.
All subjects are one line, without bodies or trailers.

Firmware SHA-256: `91d6ca57937530e429985e08e687b4e6949e074a7b75f38bfdf47c554430be7d`; size: 64668 bytes.
All six final captures use this firmware and the merged processor pin.
Earlier `870ff88a` captures and the pre-wipe-tick merged-pin runs are historical only.
No push, PR operation, hardware action, RTL edit, processor source/configuration edit or extra checkout occurred.
The earlier STOP is resolved by the public fixture correction.
A later host probe found delayed recovery after a brief latched loss; the corrected poll publishes the loss and resolves recovered state in the same call.
All earlier final2 captures and service runs are historical after that correction.
Neither assignment timing STOP condition was reached.

## Per-issue changes and acceptance

| Issue | Changes with file:line | Acceptance evidence |
| --- | --- | --- |
| #590 | `sw/firmware/milan_baremetal/milan_baremetal.c:473` CRC opportunity every 256 bytes; `:636` validation every 16 records; `:1635`, `:1737`, `:1770`, `:1781`, `:1802` command-entry service; `:1754` between wipe erases | Same 250 ms heartbeat rate limit; 133 queued bytes on both shapes; continuous backing in every plan; dispatch-removal control loses backing; findings page refreshed |
| #592 | `sw/firmware/milan_baremetal/milan_baremetal.c:447`, `:1170` aligned word interiors within each closed record, byte edges; capture `firmware.py` and `run.py` preserve poison/traffic controls and add byte-only timing control | Six final arms, 16 captures each, byte-identical copies with no open-record copy; optimized 8x8 fits 24.5 ms; byte-only restores 24.30636 ms |
| #599 | `sw/firmware/milan_baremetal/milan_baremetal.c:773` derived 125 ms trigger; `:790` bit-bang; `:826` negotiation; `:873` discovery/publication; `:921` service entry | Clause-22 link/speed/duplex publication; host modes/error/discovery checks; actual MAC_STATUS and fabric counter simulation; no-publish mutation caught; acceptance 4 remains a later physical lane |
| Tests | `sw/firmware/nvm_hosttest/phy_host.c:30`, `test_phy_firmware.py:11`; `tb/verilator/fw_service_budget/phy.py:1`, `phy.hpp:8`, `run.py:344`, `sim_main.cpp:36` | All-shape host suite including Arty, target scheduling and explicit controls |
| Documentation | `docs/findings/397_SERVICE_BUDGET.md:1`, `docs/integration/BAREMETAL_FIRMWARE.md:66`, `docs/reference/REGISTER_MAP.md` MAC_STATUS, compliance matrix item 7.4.42.2, both harness READMEs | One-hart contract, timing derivation, ownership, historical clock correction, reproduction and limits |

## Tick placement and measured stretches

The table gives maximum no-tick stretches across five final plans on each shape.
CRC and record-validation placements jointly bound status/commit work.
Command-entry opportunities also bound repeated short commands that suppress idle service.
Wipe's midpoint separates two approximately 74 ms verification walks at 8x8.

| Placement/duty | 1x1 no-tick ms | 8x8 no-tick ms |
| --- | --- | --- |
| Dispatch status | 15.12404 | 15.12396 |
| Dispatch gettime | 1.21557 | 1.21557 |
| Dispatch settime variants | 2.92286 | 3.10698 |
| Dispatch UTC variants | 3.80082 | 3.98534 |
| Status CRC/record walks | 24.74636 | 85.85876 |
| Commit CRC/record walks | 28.58932 | 95.82806 |
| Wipe midpoint | 20.61798 | 75.17266 |
| Existing erase wait | 20.14383 | 74.52111 |
| Existing restore | 0.66227 | 0.66235 |


The authoritative findings page includes every duty's elapsed time, tick gap, full UART allowance,
500 ms conditional heartbeat comparison and PHY comparison.
The ordinary-command duration comparison is not a UART protocol deadline.
Long commands are serviced internally; old duration findings remain visible in raw receipts.
Boot's initial unarmed prefix precedes the first heartbeat.

## MDIO poll-period derivation

One hart has 500 ms maximum heartbeat period minus the unchanged 250 ms rate-limit phase.
The stated publication period bound is 250 ms.
Allocate 125 ms to the PHY trigger, reserving 125 ms for
pending duty time, full TX serialization and a conservative poll scheduling charge.
The steady-state check is `125 + no-tick + UART allowance + scheduling charge <= 250 ms`.
Startup AEM/restore entries report isolated service-plus-poll costs; they are not whole startup publication bounds.
Actual publication-readback gaps independently check startup and runtime against 250 ms.
The poll envelope begins at retired heartbeat entry and includes clock acquisition,
all Clause-22 transactions, resolution and publication bookkeeping.
The scheduling charge is `C = P + 9*T`: the largest measured complete poll plus nine
maximum measured transactions. The nine-read ceiling covers discovery, two BMSR reads,
BMCR, extended status and both local/peer negotiation pairs.
This deliberately counts observed transaction time twice and covers the longer fallback
path without claiming that every fallback was target-measured.

| Shape | Transaction ms | Complete poll ms | Scheduling charge ms | Largest observed publication gap ms | 50 ms page-poll margin |
| --- | --- | --- | --- | --- | --- |
| 1x1 | 0.12616 | 0.65403 | 1.78947 | 146.05480 | 48.21053 |
| 8x8 | 0.12624 | 0.84389 | 1.98005 | 212.72466 | 48.01995 |

| Shape | Worst duty + UART + charge ms | Maximum permissible trigger ms | Selected trigger ms | Remaining reserve ms |
| --- | --- | --- | --- | --- |
| 1x1 | 59.08791 | 190.91209 | 125.00000 | 65.91209 |
| 8x8 | 120.56450 | 129.43550 | 125.00000 | 4.43550 |


The simulations read MAC_STATUS through a separate bus master and sample actual fabric counters.
Every queued/device-wait plan sees one down/up cycle and no repeated-publication counter increments.
1000-to-100 Mb/s negotiation is visible in MAC_STATUS after 2.4 s.
Short plans claim only their observed edges.
Physical switch-cycle acceptance remains #599 acceptance 4, after merge.

## Capture table

| Shape | CPU MHz | Traffic | Captures | Maximum ms | 24.5 ms margin | Result |
| --- | --- | --- | --- | --- | --- | --- |
| endstation_ax7101_1x1_tdm8 | 50 | on | 16 | 3.88702 | 20.61298 | rc 0 |
| endstation_ax7101_1x1_tdm8 | 50 | off | 16 | 3.84214 | 20.65786 | rc 0 |
| endstation_ax7101_8x8 | 50 | on | 16 | 13.23262 | 11.26738 | rc 0 |
| endstation_ax7101_8x8 | 50 | off | 16 | 13.07044 | 11.42956 | rc 0 |
| endstation_ax7101_8x8 | 100 | on | 16 | 9.94948 | 14.55052 | rc 0 |
| endstation_ax7101_8x8 | 100 | off | 16 | 9.94094 | 14.55906 | rc 0 |


The previous 8x8 maximum was 24.30246 ms, leaving 0.19754 ms. The new capture gains 11.06984 ms of margin.


The four 50 MHz arms are contract evidence. The 100 MHz 8x8 pair is a labelled non-contract comparison.
All destination-byte/open-record checks pass; traffic-on arms also have concurrent requests, responses and reads.
The replaced receipt binds the final firmware digest, processor pin, generated CPU/BIOS/image identities and harness.

## #397 harness table

| Shape | Plan | Max heartbeat gap ms | Unbacked cycles | Down/up edges | Service verdict |
| --- | --- | --- | --- | --- | --- |
| 1x1 | all | 264.62414 | 0 | 0/0 | rc 0 |
| 1x1 | uart-paced | 252.67354 | 0 | 1/0 | rc 0 |
| 1x1 | queued-input | 269.07786 | 0 | 1/1 | rc 0 |
| 1x1 | queued-short | 257.67502 | 0 | 1/1 | rc 0 |
| 1x1 | device-wait | 250.41246 | 0 | 1/1 | rc 0 |
| 8x8 | all | 322.47112 | 0 | 1/1 | rc 0 |
| 8x8 | uart-paced | 295.46250 | 0 | 1/1 | rc 0 |
| 8x8 | queued-input | 322.47112 | 0 | 1/1 | rc 0 |
| 8x8 | queued-short | 257.67564 | 0 | 1/1 | rc 0 |
| 8x8 | device-wait | 275.41748 | 0 | 1/1 | rc 0 |


All plans use populated A/B media. Device-wait uses 3000000 us erase and 5000 us page WIP; other plans use zero WIP.
Both queued-input plans contain 133 bytes; both queued-short plans contain 350 status commands.
The historical 8x8 #397 generation declared gPTP/lwSRP at 100 MHz despite its 50 MHz CPU override.
Both current configurations and generated constants declare 50 MHz.

## Mutants and controls

| Control | Observed result |
| --- | --- |
| Dispatch removed, 350 queued status commands | Driver rc 0; heartbeat gap 2769.99749 ms; 77036756 unbacked system cycles; named backing refusal |
| Unmodified 350-command positive | Both shapes pass; zero unbacked cycles |
| Byte-only 8x8 capture | Two captures, driver rc 0, maximum 24.30636 ms versus the merged-pin historical 24.30246 ms; old copy cost restored |
| Missing-copy capture | Driver rc 0; destination poison/byte oracle rejects missing word and byte stores |
| Missing traffic | Driver rc 0; concurrent-traffic oracle rejects the traffic-on claim |
| Publisher removed, host | Named publication assertion rejects mutation |
| Latched recovery deferred, host | Current-state assertion rejects the old second-poll delay |
| Publisher removed, target | Driver rc 0; named missing-publication evidence check rejects mutation |
| Four existing NVM host mutants | Every planted defect caught across the all-shape self-test |
| Capture receipt controls | Seven planted receipt/grading errors refused by the final gate |
| Service portable controls | 42 grading controls and 14 flash controls, rc 0 |
| PHY reuse inventory | Both new peer files bound to compiled reuse; changed-file controls refuse stale builds |

## Gate table

Every command runs from the physical workspace path with a foreground timeout and no output pipeline.
The following final results name the same committed head shown above.
Large logs remain outside this output directory; each artifact has a recorded size and SHA-256.

| Gate | Exact command | rc | Log artifact |
| --- | --- | --- | --- |
| host | `rtk proxy timeout 1800 $VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 -B sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | a385-final-gate-host.log |
| capture-receipt | `rtk proxy timeout 1800 $VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 -B scripts/check_nvm_capture.py` | 0 | a385-final-gate-capture-receipt.log |
| service-selftest | `rtk proxy timeout 1800 $VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 -B tb/verilator/fw_service_budget/run.py --self-test` | 0 | a385-final-gate-service-selftest.log |
| phy-reuse | `rtk proxy timeout 1800 $VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 -B $MANAGEMENT/2026-09-23/590-a385/check_phy_reuse.py` | 0 | a385-final-gate-phy-reuse.log |
| ci-scope | `rtk proxy timeout 1800 $VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 -B scripts/ci_scope.py --selftest` | 0 | a385-final-gate-ci-scope.log |
| docs | `rtk proxy timeout 1800 $VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 -B scripts/docs_check.py` | 0 | a385-final-gate-docs.log |
| doc-paths | `rtk proxy timeout 1800 $VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 -B scripts/check_doc_paths.py` | 0 | a385-final-gate-doc-paths.log |
| doc-style | `rtk proxy timeout 1800 $VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 -B scripts/check_doc_style.py` | 0 | a385-final-gate-doc-style.log |
| archive | `rtk proxy timeout 1800 $VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 -B scripts/check_archive.py` | 0 | a385-final-gate-archive.log |
| toc | `rtk proxy timeout 1800 $VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 -B scripts/gen_toc.py --check` | 0 | a385-final-gate-toc.log |
| em-dash | `rtk proxy timeout 1800 $VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 -B scripts/check_em_dash.py --base 20aa4eabf` | 0 | a385-final-gate-em-dash.log |
| features | `rtk proxy timeout 1800 $VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 -B scripts/check_feature_status.py --self-test` | 0 | a385-final-gate-features.log |
| pp-sources | `rtk proxy timeout 1800 $VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 -B scripts/pp_srcs.py --check` | 0 | a385-final-gate-pp-sources.log |
| baremetal-only | `rtk proxy timeout 1800 $VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 -B scripts/check_baremetal_only.py --check` | 0 | a385-final-gate-baremetal-only.log |
| entity-shape | `rtk proxy timeout 1800 $VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 -B scripts/check_entity_shape.py --self-test` | 0 | a385-final-gate-entity-shape.log |
| python-idiom | `rtk proxy timeout 1800 $VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 -B scripts/check_py_idiom.py` | 0 | a385-final-gate-python-idiom.log |
| cpp-idiom | `rtk proxy timeout 1800 $VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 -B scripts/check_cpp_idiom.py` | 0 | a385-final-gate-cpp-idiom.log |
| hygiene | `rtk proxy timeout 1800 $VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 -B scripts/check_hygiene.py --check` | 0 | a385-final-gate-hygiene.log |
| test-evidence | `rtk proxy timeout 1800 $VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 -B scripts/measure_test_evidence.py --check` | 0 | a385-final-gate-test-evidence.log |
| diff-whitespace | `rtk proxy timeout 60 git diff --check 20aa4eabf` | 0 | a385-final-gate-diff-whitespace.log |
| builder-present-with-firmware-census | `rtk proxy timeout 14400 env PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 $WORKSPACE_HOME/litex-milan/venv/bin/python -B sw/builder/test_builder.py --require-elaboration --require-rv32` | 0 | a385-final-builder-present-with-firmware-census.log |
| builder-absent | `rtk proxy timeout 14400 env PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 $WORKSPACE_HOME/litex-milan/venv/bin/python -B $MANAGEMENT/2026-09-23/590-a385/full-builder-absent.py` | 0 | a385-final-builder-absent.log |
| bound-service-1x1-all | `rtk proxy timeout 28800 unshare -Urn env PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true LITEX_ENV_CC_TRIPLE=$WORKSPACE_HOME/br-milan-rv32/host/bin/riscv32-linux PATH=$WORKSPACE_HOME/litex-milan/venv/bin:/usr/bin:/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin $WORKSPACE_HOME/litex-milan/venv/bin/python -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_1x1_tdm8 --build-dir /tmp/a385-final3-service-1x1 --reuse-build --plan all --populated --enforce-service --regrade` | 0 | a385-final-regrade-service-1x1-all.log |
| bound-service-1x1-uart-paced | `rtk proxy timeout 28800 unshare -Urn env PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true LITEX_ENV_CC_TRIPLE=$WORKSPACE_HOME/br-milan-rv32/host/bin/riscv32-linux PATH=$WORKSPACE_HOME/litex-milan/venv/bin:/usr/bin:/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin $WORKSPACE_HOME/litex-milan/venv/bin/python -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_1x1_tdm8 --build-dir /tmp/a385-final3-service-1x1-uart-paced --reuse-build --plan uart-paced --populated --enforce-service --regrade` | 0 | a385-final-regrade-service-1x1-uart-paced.log |
| bound-service-1x1-queued-input | `rtk proxy timeout 28800 unshare -Urn env PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true LITEX_ENV_CC_TRIPLE=$WORKSPACE_HOME/br-milan-rv32/host/bin/riscv32-linux PATH=$WORKSPACE_HOME/litex-milan/venv/bin:/usr/bin:/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin $WORKSPACE_HOME/litex-milan/venv/bin/python -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_1x1_tdm8 --build-dir /tmp/a385-final3-service-1x1-queued-input --reuse-build --plan queued-input --populated --enforce-service --regrade` | 0 | a385-final-regrade-service-1x1-queued-input.log |
| bound-service-1x1-queued-short | `rtk proxy timeout 28800 unshare -Urn env PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true LITEX_ENV_CC_TRIPLE=$WORKSPACE_HOME/br-milan-rv32/host/bin/riscv32-linux PATH=$WORKSPACE_HOME/litex-milan/venv/bin:/usr/bin:/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin $WORKSPACE_HOME/litex-milan/venv/bin/python -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_1x1_tdm8 --build-dir /tmp/a385-final3-service-1x1-queued-short --reuse-build --plan queued-short --populated --enforce-service --regrade` | 0 | a385-final-regrade-service-1x1-queued-short.log |
| bound-service-1x1-device-wait | `rtk proxy timeout 28800 unshare -Urn env PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true LITEX_ENV_CC_TRIPLE=$WORKSPACE_HOME/br-milan-rv32/host/bin/riscv32-linux PATH=$WORKSPACE_HOME/litex-milan/venv/bin:/usr/bin:/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin $WORKSPACE_HOME/litex-milan/venv/bin/python -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_1x1_tdm8 --build-dir /tmp/a385-final3-service-1x1-device-wait --reuse-build --plan device-wait --populated --enforce-service --device-wait-us 3000000 --program-wait-us 5000 --regrade` | 0 | a385-final-regrade-service-1x1-device-wait.log |
| bound-service-8x8-all | `rtk proxy timeout 28800 unshare -Urn env PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true LITEX_ENV_CC_TRIPLE=$WORKSPACE_HOME/br-milan-rv32/host/bin/riscv32-linux PATH=$WORKSPACE_HOME/litex-milan/venv/bin:/usr/bin:/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin $WORKSPACE_HOME/litex-milan/venv/bin/python -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_8x8 --build-dir /tmp/a385-final3-service-8x8 --reuse-build --plan all --populated --enforce-service --regrade` | 0 | a385-final-regrade-service-8x8-all.log |
| bound-service-8x8-uart-paced | `rtk proxy timeout 28800 unshare -Urn env PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true LITEX_ENV_CC_TRIPLE=$WORKSPACE_HOME/br-milan-rv32/host/bin/riscv32-linux PATH=$WORKSPACE_HOME/litex-milan/venv/bin:/usr/bin:/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin $WORKSPACE_HOME/litex-milan/venv/bin/python -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_8x8 --build-dir /tmp/a385-final3-service-8x8-uart-paced --reuse-build --plan uart-paced --populated --enforce-service --regrade` | 0 | a385-final-regrade-service-8x8-uart-paced.log |
| bound-service-8x8-queued-input | `rtk proxy timeout 28800 unshare -Urn env PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true LITEX_ENV_CC_TRIPLE=$WORKSPACE_HOME/br-milan-rv32/host/bin/riscv32-linux PATH=$WORKSPACE_HOME/litex-milan/venv/bin:/usr/bin:/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin $WORKSPACE_HOME/litex-milan/venv/bin/python -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_8x8 --build-dir /tmp/a385-final3-service-8x8-queued-input --reuse-build --plan queued-input --populated --enforce-service --regrade` | 0 | a385-final-regrade-service-8x8-queued-input.log |
| bound-service-8x8-queued-short | `rtk proxy timeout 28800 unshare -Urn env PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true LITEX_ENV_CC_TRIPLE=$WORKSPACE_HOME/br-milan-rv32/host/bin/riscv32-linux PATH=$WORKSPACE_HOME/litex-milan/venv/bin:/usr/bin:/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin $WORKSPACE_HOME/litex-milan/venv/bin/python -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_8x8 --build-dir /tmp/a385-final3-service-8x8-queued-short --reuse-build --plan queued-short --populated --enforce-service --regrade` | 0 | a385-final-regrade-service-8x8-queued-short.log |
| bound-service-8x8-device-wait | `rtk proxy timeout 28800 unshare -Urn env PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true LITEX_ENV_CC_TRIPLE=$WORKSPACE_HOME/br-milan-rv32/host/bin/riscv32-linux PATH=$WORKSPACE_HOME/litex-milan/venv/bin:/usr/bin:/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin $WORKSPACE_HOME/litex-milan/venv/bin/python -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_8x8 --build-dir /tmp/a385-final3-service-8x8-device-wait --reuse-build --plan device-wait --populated --enforce-service --device-wait-us 3000000 --program-wait-us 5000 --regrade` | 0 | a385-final-regrade-service-8x8-device-wait.log |
| bound-remove-dispatch | `rtk proxy timeout 28800 unshare -Urn env PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true LITEX_ENV_CC_TRIPLE=$WORKSPACE_HOME/br-milan-rv32/host/bin/riscv32-linux PATH=$WORKSPACE_HOME/litex-milan/venv/bin:/usr/bin:/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin $WORKSPACE_HOME/litex-milan/venv/bin/python -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_1x1_tdm8 --build-dir /tmp/a385-final3-service-remove-dispatch --plan queued-short --mutation remove-dispatch --populated --enforce-service --regrade` | 0 | a385-final-regrade-remove-dispatch.log |


The compiler-present full bank retains one NOT RUN arm: its existing physical utilization-report calibration.
The report is absent and hardware is outside this lane.
The absent bank additionally registers the compiler-dependent instrument group as NOT RUN.
All elaboration arms execute; those explicit omissions are not presented as passes.
The absent wrapper hides all three cross-compiler candidates while retaining real host probes and the entire builder bank.

## Reproduction and artifact limits

`capture-artifacts-final.json` and `service-artifacts-final.json` record large artifact hashes and sizes.
`final-gates.json`, `final-builder-gates.json` and `final-target-gates.json` bind command results to the final head.
`control-artifacts-final.json` records the corresponding control receipts and logs.
`replace_capture_receipt.py` checks all six capture oracles and byte-binds instrumented firmware before replacement.
`refresh_service_findings.py` requires all ten successful service plans before generating the tables.
All target commands use the existing offline product environment, explicit physical workspace and external build directories.
Capture timeout is 14400 seconds; service timeout is 28800 seconds.
Use the retained per-run command inventory and repository recipes to reproduce each arm.

No output-directory file exceeds 200 KB; toolchains, packages, generated trees and executables remain outside it.
The SPI boundary remains optimistic (historical 67/65 cycles for 8 bits and 259/257 for 32 bits).
DDR is simulated and only one deterministic clock phase is measured.
No physical boot, twofold physical commit margin or field torture acceptance is claimed.
Future update, fault-log and temperature duties remain unmeasured under #397.

The branch is local and ready for the assigned independent reviewers.
Hosted gates and the deferred physical #599 rerun remain subsequent workflow steps.
No author validation in this packet is a review verdict.
