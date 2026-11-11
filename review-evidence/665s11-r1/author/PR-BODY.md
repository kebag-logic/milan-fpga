[A761]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

Green at `b29f94d7aa`: every local gate passed (88 workflow steps, 64 docs steps, 65 of 65 sweep suites, 0 bad); acceptance items 2 to 5 met, item 1 met for six of the eight items and the binding — `665-s11-aecp-reboot` -> `dev-soft-core`

## Linked Issue / roles

Relates to #871 (not closed: acceptance item 1 is met for six of its eight items, see below)
Relates to #665

Executor: `[A761]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

The split's AECP REBOOT (#665 S11): the firmware's AECP owner answers it, and the platform's reset port starts the reset #787 chose (PR #822, already on `dev-soft-core`).

| Piece | Change |
|---|---|
| The reset port | `dev-soft-core` tied the split's request to 0 (`milan_datapath.sv`, `assign pp_reboot_req_w = 1'b0;`). One CSR bit of the split SoC, `ctrl_reboot_req` (`milan_soc.CtrlReboot`, its bank pinned below the mailbox's), crossed by a `MultiReg` into the datapath's clock onto a new input `i_reboot_req`, which the split branch connects to `reboot_ctrl.reboot_req_i`. `KL_reboot_ctrl` is unchanged. No `mailbox.yaml` change. |
| The census | `reboot_req_o` stays class G with its all-fabric exclusion; the split census holds `pp_reboot_req_w` to `i_reboot_req` alone (`G_CARRIED`), with two plants. |
| The AECP owner | REBOOT (0x002A) in the processor's order: BAD_ARGUMENTS short of Figure 7-68, NOT_SUPPORTED for a type other than ENTITY (no MEMORY_OBJECT firmware image), NO_SUCH_DESCRIPTOR for another ENTITY index, ENTITY_LOCKED under another controller's lock, ENTITY_MISBEHAVING while a change waits for the platform; otherwise SUCCESS, notified to the other registered controllers. No command after it. `aecp_reboot_due` once every frame owed has completed. Without a reset port it stays NOT_IMPLEMENTED. |
| The platform | After the SUCCESS and its notifications have left the mailbox, ADP shuts down (ENTITY_DEPARTING, Milan v1.2 5.6.3.3); once ADP's ring has drained, it writes the port. From then it services the saved-state store and its F_NVM alone, so a journal write in progress completes and no frame is taken that could start another during the PHY hold. |
| The memory ledger | `sizeof(struct ctrl_plat)` re-measured at the four points (+32 B each; 21,272 B at the ledgered 8x8/2if point). |
| The tests | three AECP core tests and eleven planted defects; host platform tests B11 to B18 and ten planted defects; a new CPU simulation, `tb/verilator/ctrl_reboot`, with four planted images and five grader controls, listed in the TSN stack boundary gate's `OUTSIDE` table as the split boot simulation is. |

The carrier decision: `docs/design/MAILBOX_SPLIT.md` left it to this lane, a face-block level being its expected end. A face-block field is a `mailbox.yaml` change; the CSR bit is the smallest port that needs none. The design doc now records the choice.

**Acceptance (#871).**

| # | Item | Evidence | Met |
|---|---|---|---|
| 1 | After the reset, the eight Milan state items restored, ADP inside its valid time, the binding restored (#396's power-area checks), in the CPU simulation | `tb/verilator/ctrl_reboot`: the #396 grader `check_release_state_restored` PASS over the stream format, presentation time offset, channel mappings, clock source, entity names, object name and the binding, each set away from its default before the REBOOT; the first ENTITY_AVAILABLE 500.667 ms after the reset, 4,590.218 ms after the REBOOT command of the 20,000 ms valid time; host test B15 | **Six of the eight items and the binding.** The configuration and the sampling rate cannot leave their defaults at the shipping shape (one configuration, one rate): read back unchanged and reported NOT RUN, as the #396 grader rules a pre-cycle value equal to its default |
| 2 | The response on the wire before the reset fires; a mutant firing the reset before the response leaves fails | ORDER: SUCCESS 2.166 ms, notification 2.309 ms, ENTITY_DEPARTING 3.799 ms, the port 4.457 ms after the command; plant `reset-before-the-response` (ORDER), `plat-reboot-before-the-response` (B12 no reset while the mailbox holds the response), `reboot-due-before-its-frames-complete` | yes |
| 3 | A mutant that ignores the request fails | plant `request-ignored` (ORDER: the reset port never fired), `plat-reboot-ignored` (B11, B15, B16), `reboot-never-accepted` | yes |
| 4 | A REBOOT during a journal write leaves a state the boot replay accepts, completed or abandoned, never half-applied; a planted mutant that tears the write fails | JOURNAL: the REBOOT arrives 62 bus cycles after the write's erase, 14 page programs follow, the drain ends durable and every item reads back after the reset (completed); the cut's replay reads the saved snapshot whole (abandoned); plant `write-torn` and `plat-reboot-stops-the-store` (the store stopped at the port: the write does not complete); host B16; tested against the current saved-state code, whose format #823 owns | yes |
| 5 | REBOOT of a descriptor other than the ENTITY answered as 7.4.43 states, with its test | REFUSE: STREAM_INPUT and MEMORY_OBJECT NOT_SUPPORTED, ENTITY 1 NO_SUCH_DESCRIPTOR, short BAD_ARGUMENTS, each at cdl 16, notifying no one, resetting nothing; `Core.RebootRefusalsLeaveTheEntityInService`, B13; plant `any-descriptor-type`, defects `reboot-any-descriptor-type`, `reboot-any-entity-index` | yes |

**Measurements.**

- **Request to reset:** 445,707 bus cycles, 222,853 CPU cycles (4.457 ms at 50 MHz) from the REBOOT command's last byte at the mailbox to the reset port, in the CPU simulation; then `KL_reboot_ctrl`'s stated bound to the IPROG word (`REBOOT_RESET.md` section 3), here a 582.094 ms drain for the write in progress and a quiet egress wait.
- **Linked size:** +868 B of ROM at every point (`.text` +744 at one interface and +740 at two, `.rodata` +120, `.data` +4), +48 B (1x1) or +32 B (8x8) of SRAM; `sizeof(struct ctrl_plat)` +32 B. No point's RAMB36 plan moves: 39.0, 42.0, 52.0 and the ledgered 59.0 at 8x8/2if, whose ROM holds 125,916 of 126,976 B.

## Authoritative references

- #871; plan S11 and decision D9 of #665.
- IEEE 1722.1-2021 7.4.43 (Figure 7-68, 7.4.43.1, 7.4.43.2), 7.5.2, Table 7-126 (REBOOT = 0x002A); 6.2.1 (ADPDU, valid_time).
- Milan v1.2 5.4.5.1, 5.4.5.2 (notifications), 5.6.2 (valid_time 10), 5.6.3.3 and Table 5.50 (SHUTDOWN, TMR_DELAY 0 to 4 s), 5.3.5.1, 5.3.7.1, 5.3.7.6, 5.3.8.1 to 5.3.8.3, 5.3.9.1, 5.3.10.1, 5.3.11.1, 5.3.13 (the saved items).
- `docs/design/REBOOT_RESET.md` (#787) sections 3 and 4, and the new section 8; `docs/design/MAILBOX_SPLIT.md`; protocol-processor `docs/architecture/06_aecp_engine.md` section 6.11 (the processor's routes and order).

## How to get into the same state

```sh
git clone https://github.com/kebag-logic/milan-fpga.git
cd milan-fpga
git fetch origin 665-s11-aecp-reboot
git checkout b29f94d7aa1d73c4d1eef705a42d9a3a34fc4702
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
```

The CPU simulation needs the product LiteX tree, the pinned RV32 SDK, Verilator and the offline CPU generator, as `tb/verilator/ctrl_service_budget/README.md` lists them.

## How to validate

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test
python3 sw/firmware/gtest/fw_coverage.py --check
python3 sw/mailbox/publication_census.py --check --selftest
python3 -B tb/verilator/ctrl_reboot/run.py --build-dir /tmp/reboot --self-test
```

Expected result / pass criteria: each exits 0. The firmware self-test reports every planted defect caught, the AECP and platform REBOOT ones included; the census reports the two REBOOT plants refused; the REBOOT simulation prints `ctrl_reboot: PASS (0 finding(s))` and `9 of 9 plants and controls caught`.

**Local gates at `b29f94d7aa1d73c4d1eef705a42d9a3a34fc4702`**, each on its own fresh clean clone:

| Gate | Result |
|---|---|
| `rtl-fast`, `elaborate`, `rtl`: every `run:` step of every job a pull_request to `dev-soft-core` triggers | 88 ran, rc 0; 167 not run, each with a stated reason (hosted-only installs, uploads and orchestration; `verilator-shards` replicated by the sweep); 0 bad |
| `docs.yml`: every `run:` step | 64 ran, rc 0; 31 not run, each with a stated reason; 0 bad |
| Full Verilator sweep, four native shards | 65 of 65 suites, 2,192,899 checks, 0 in-suite failures; suite-cancellation preflight PASS on each shard |
| `test_ctrl_firmware.py --require-rv32 --self-test` | PASS; control campaign 580 of 580 caught |
| `fw_coverage.py --check` | PASS (35 files) |
| Firmware mutant drivers | AECP 150 of 150; SRP PASS; saved-state store 109 of 109 planted defects reddened (5 shapes, 435 tests) |
| `ctrl_boundary.py` (firmware-boundary, firmware-verilator) | PASS |
| Publication census `--check --selftest` | 6 shapes, 246 checks, 0 failures; 0 of 164 arms failed; the REBOOT plants refused |
| S2's harness, 1x1/1if and 8x8/2if, and its self-test | rc 0, 0 refusals; T_svc misses recorded: 34 (13 of 81 paths) and 57 (29 of 129 paths) |
| `test_builder.py --require-rv32` | all gates pass except gate 11's calibration arm, not run: it needs a Vivado place report from a build this host does not have |
| `cd tests && behave` | 14 features, 508 scenarios passed |
| `git diff --check` against the merge base | clean |
| `tb/verilator/ctrl_reboot/run.py --self-test` | PASS (0 findings); 9 of 9 plants and controls caught |

Not run: the mailbox's full RTL mutant set (`make -C tb/verilator/mbx mutants`): the mailbox RTL is unchanged here, and the sweep's mbx suite ran its quick set, 7 of 7 caught. The hosted `rtl-fast`, `verilator-suites` and `yosys-portability` contexts remain mandatory.

## Known limitations / out of scope

- The CPU simulation builds no datapath: "on the wire" is the mailbox's transmit face. From there the fabric path to the MAC is cut-through, and `KL_reboot_ctrl`'s egress wait (#787, its own suites) holds the PHY until every frame given to the MAC has left. The bench's REBOOT cycles are S12's.
- The PHY hold is simulated for 50 of its 3,500 ms, and the IPROG word and the configuration load not at all; the ADP figure adds the RTL's hold and states the margin left for the load.
- The configuration and the sampling rate cannot be set away from their defaults at the shipping shape (one configuration, one rate), so they are read back, not graded.
- A datapath that never drains the mailbox's rings holds the reset back, as the processor's request waits for its last frame.
- S2's harness against the base (`1d6bf5556a`): at 1x1/1if the same 13 of 81 paths are over T_svc. At 8x8/2if 29 of 129 are over at the head and 31 at the base: three paths fall under it, and `acmp.probe_tx.if1` goes over it (5.416 ms at the base, 13.602 ms at the head). Every path moved by -15.343 to +8.186 ms, both ways, with the probes starting at other cycles. The misses are recorded, not graded, and the loop's budget is S2b's (#810).
- Out of scope, as #871 states: the bench's 50 soft resets (S12), the saved-state format (#823), the firmware loop (S2b, #810).
- Lane overlap: S8's `ctrl_wire_timing` builds its CPU SoC through `split_soc.add_devices`, which now adds the reset port, so its platform image's map resolves unchanged.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
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
