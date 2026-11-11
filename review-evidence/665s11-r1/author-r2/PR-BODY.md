[A761c]

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

Green at `d08d30c6ec`: every local gate passed (88 workflow steps, 64 docs steps, 65 of 65 sweep suites, 0 bad); acceptance items 2 to 5 met, item 1 met for six of the eight items and the binding — `665-s11-aecp-reboot` -> `dev-soft-core`

## Linked Issue / roles

Relates to #871 (not closed: acceptance item 1 is met for six of its eight items, see below)
Relates to #665

Executor: `[A761c]` (round 2; round 1 was `[A761]`)
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

The split's AECP REBOOT (#665 S11): the firmware's AECP owner answers it, and the platform's reset port starts the reset #787 chose (PR #822, already on `dev-soft-core`).
Round 2 answers R821-1 and R822-1 under the ruling on #871: from the SUCCESS to the reset port the split now behaves as the processor it replaces (REQ-FWX-001).

| Piece | Change |
|---|---|
| The reset port | `dev-soft-core` tied the split's request to 0. One CSR bit of the split SoC, `ctrl_reboot_req` (`milan_soc.CtrlReboot`, its bank pinned below the mailbox's), is crossed by a `MultiReg` into the datapath's clock onto a new input `i_reboot_req`. The split branch connects that input to `reboot_ctrl.reboot_req_i`. `KL_reboot_ctrl` is unchanged. No `mailbox.yaml` change. |
| The census | `reboot_req_o` stays class G with its all-fabric exclusion; the split census holds `pp_reboot_req_w` to `i_reboot_req` alone (`G_CARRIED`), with two plants. The CDC census row now names the REBOOT request level among the `MultiReg` crossings, regenerated through `cdc_census.gen.py`. |
| The AECP owner | REBOOT (0x002A) in the processor's order: BAD_ARGUMENTS short of Figure 7-68, NOT_SUPPORTED for a type other than ENTITY (no MEMORY_OBJECT firmware image), NO_SUCH_DESCRIPTOR for another ENTITY index (judged before the lock), ENTITY_LOCKED under another controller's lock, ENTITY_MISBEHAVING while a change waits for the platform; otherwise SUCCESS, notified to the other registered controllers. From the SUCCESS `aecp_reboot_accepted` is true and no command is taken; `aecp_reboot_due` turns true once every frame owed has completed. Without a reset port it stays NOT_IMPLEMENTED. |
| The platform, parity (round 2) | **No frame is taken from the SUCCESS:** every channel's take sits behind a gate on `aecp_reboot_accepted`, installed at boot through the loop's own `ctrl_loop_bind_rx` and `ctrl_loop_set_rx_ready` with each channel's binding behind it. A frame stays in its ring, and the mailbox drops whole one that then finds no room (`RX_DROP`), as the processor's top discards every frame. **No frame after ENTITY_DEPARTING:** once `aecp_reboot_due`, the loop is no longer serviced, so no channel starts another transmission. ADP shuts down only once every other channel's ring has drained, so ENTITY_DEPARTING is the last frame. The port is written once ADP's ring has drained too. From the loop's last pass `ctrl_plat_step` services the saved-state store, its F_NVM, and ADP's poll until the port fires. |
| The memory ledger | `sizeof(struct ctrl_plat)` re-measured at the four points: 18,528, 20,016, 19,184 and 21,328 B (the ledgered 8x8/2if point), the gate's saved bindings included. |
| The tests | AECP core tests with thirteen planted defects; host platform tests B11 to B21 with thirteen REBOOT defects; the CPU simulation `tb/verilator/ctrl_reboot` with five planted images and seven grader controls, each required to give its own finding's words. |

The carrier decision is unchanged: `docs/design/MAILBOX_SPLIT.md` left it to this lane, a face-block level being its expected end. A face-block field is a `mailbox.yaml` change; the CSR bit is the smallest port that needs none.

**Round 2, item by item (the ruling on #871).**

| Ruling item | Done | Evidence |
|---|---|---|
| 1 Parity: from the SUCCESS no received frame of any channel is taken | yes | host B19 (an ENTITY_DISCOVER, a BIND_RX and an AEM command after the SUCCESS: no channel's `RX_TAIL` written, nothing applied or answered), defect `plat-reboot-takes-frames-after-the-success`; CPU simulation: a BIND_RX and an AEM command reach the mailbox between the SUCCESS and the port and neither is answered, plant `frames-taken-after-the-success` |
| 1 Parity: after ENTITY_DEPARTING no other channel starts a transmission until the port fires | yes | host B20 (a listener bound before the REBOOT; the mailbox holds the DEPARTING for 5 s: no other channel's `TX_HEAD` written; with the loop planted back on, SRP, MAAP and ACMP send 18 frames there), defect `plat-reboot-transmits-after-the-departing`; host B21 (the DEPARTING waits while another ring holds a frame), defect `plat-reboot-departs-before-the-rings-drain`; host B17 (nothing sent once the port fired), defect `plat-reboot-serves-the-loop-after-the-port`; CPU simulation grades every frame after the first DEPARTING and after the port, control `frame-after-the-departing` |
| 1 R821-1's `fw_probes.py ... behaviour-acmp-after-success` passes unchanged | yes | at `d08d30c6ec`: rc 0, no test failed, `acmp_frames_after_success=0 sink_bound=0 frames_after_departing=0`, and with the DEPARTING out before the port `acmp_frames_after_departing=0` |
| 1 R822-1's `run_probe_window.sh` reports `sink.bound` 0 and no ACMP frame | yes | at `d08d30c6ec`: `sink.bound` 0, `acmp_frames=0`; frames AECP, then ADP, then the port |
| 1 `REBOOT_RESET.md` section 8 corrected | yes | "Only the request's source differs" and "No command is taken after it" replaced by the window as the processor keeps it |
| 2 The early-reset plant fires the port before the SUCCESS leaves; each plant needs its own words | yes | `reset-before-the-response` writes the port in the take that accepts the REBOOT and is caught by "ORDER: the REBOOT's SUCCESS left the mailbox after the reset port fired"; `plant_point` and `control` match each one's own words |
| 3 `PYTHONHASHSEED` pinned for every export | yes | `run.py` sets 0 for its child exports; the documented command run twice with no seed in the environment: `run.py --self-test --jobs 3` and the plain `run.py`, each on the final head's clean clone with `PYTHONHASHSEED` unset, both `ctrl_reboot: PASS (0 finding(s))` |
| 4 The figure stated as a measurement; no firmware-stage bound while a ring is held | yes | `REBOOT_RESET.md` section 8 "The bound" and "One measurement", the simulation README's BOUND row, and this body |
| 5 R822-1 R1 | yes | `MAILBOX_SPLIT.md` "Default build", with the exact text |
| 6 Index before lock (R821 S1) | yes | `Core.RebootRefusalsLeaveTheEntityInService` asks ENTITY 1 under another controller's lock for NO_SUCH_DESCRIPTOR; defect `reboot-lock-before-the-index`, and the reviewer's `lock-before-the-index` probe now caught |
| 6 Mixed-replay grader control (R821 S3, R822 S1) | yes | control `replay-mixed`: "JOURNAL: the cut's replay reads ..., a write half applied" |
| 6 `i_reboot_req` tied 0 in the all-fabric instances, the exports still byte-identical (R821 S4) | **not taken: the two conditions conflict** | Measured: a 0 tie in `add_milan_datapath`'s Instance (it covers both all-fabric instances, `MilanMAC`'s ports override that dict) adds exactly one line to the generated all-fabric top `.v`, `.i_reboot_req (1'd0),`, at the 1x1 and 8x8 shipping configs. So no tie leaves the export byte-identical. Without it, the head's all-fabric exports match the base's byte for byte except LiteX's timestamps and its hierarchy comment's order, which also changes between two exports of one commit. The port is unread at `CTRL_SPLIT_P = 0`. A decision is needed if the tie is wanted at the cost of that one line. |
| 6 The base side of the S2 compare (R822 S2) | yes | the base runs' logs, tables and `results.json` digests, and the compare reproducing "31 at the base" and 5.416 ms |
| 6 The CDC census row names the request level (R822 S3) | yes | `cdc_census.gen.py`; the SVG and drawio regenerated by it, the PNG rendered from the SVG |
| 7 Item 1 partial; "Relates to #871" | unchanged | as below |

**Acceptance (#871).**

| # | Item | Evidence | Met |
|---|---|---|---|
| 1 | After the reset, the eight Milan state items restored, ADP inside its valid time, the binding restored (#396's power-area checks), in the CPU simulation | `tb/verilator/ctrl_reboot`: the #396 grader `check_release_state_restored` PASS over the stream format, presentation time offset, channel mappings, clock source, entity names, object name and the binding, each set away from its default before the REBOOT; the first ENTITY_AVAILABLE 502.312 ms after the reset, 4,590.679 ms after the REBOOT command, of the 20,000 ms valid time; host test B15 | **Six of the eight items and the binding.** The configuration and the sampling rate cannot leave their defaults at the shipping shape (one configuration, one rate): read back unchanged and reported NOT RUN, as the #396 grader rules a pre-cycle value equal to its default |
| 2 | The response on the wire before the reset fires; a mutant firing the reset before the response leaves fails | ORDER: SUCCESS 2.157 ms, notification 2.300 ms, ENTITY_DEPARTING 4.199 ms, the port 4.243 ms after the command; plant `reset-before-the-response` caught by "the REBOOT's SUCCESS left the mailbox after the reset port fired"; host defect `plat-reboot-before-the-response` (B12 no reset while the mailbox holds the response); AECP defect `reboot-due-before-its-frames-complete` | yes |
| 3 | A mutant that ignores the request fails | plant `request-ignored` (the reset port never fired), `plat-reboot-ignored` (B11, B15, B16), `reboot-never-accepted` | yes |
| 4 | A REBOOT during a journal write leaves a state the boot replay accepts, completed or abandoned, never half-applied; a planted mutant that tears the write fails | JOURNAL: the REBOOT arrives 62 bus cycles after the write's erase, 14 page programs follow, the drain ends durable and every item reads back after the reset (completed); the cut's replay reads the saved snapshot whole (abandoned), and control `replay-mixed` shows the grader refuses a mix; plant `write-torn` and `plat-reboot-stops-the-store`; host B16; tested against the current saved-state code, whose format #823 owns | yes |
| 5 | REBOOT of a descriptor other than the ENTITY answered as 7.4.43 states, with its test | REFUSE: STREAM_INPUT and MEMORY_OBJECT NOT_SUPPORTED, ENTITY 1 NO_SUCH_DESCRIPTOR, short BAD_ARGUMENTS, each at cdl 16, notifying no one, resetting nothing; `Core.RebootRefusalsLeaveTheEntityInService`, B13; plant `any-descriptor-type`, defects `reboot-any-descriptor-type`, `reboot-any-entity-index` | yes |

**Measurements.**

- **Request to reset, one scenario's measurement, not a bound:** in the CPU simulation's REBOOT scenario (shipping shape, no ring held), 424,271 bus cycles, 212,135 CPU cycles (4.243 ms at 50 MHz) from the REBOOT command's last byte at the mailbox to the reset port. Then `KL_reboot_ctrl`'s stated bound to the IPROG word (`REBOOT_RESET.md` section 3), here 581.124 ms to the PHY hold for the write in progress and a quiet egress wait.
- **The firmware stage has no bound while a mailbox ring is held:** it waits for the SUCCESS, its notifications and every ring to drain, so a datapath that never takes a frame holds the reset port back, as the processor documents for its MAC ("A MAC that never takes a frame holds the request back").
- **Linked size** against the base (`1d6bf5556a`, built by `ctrl_plat_image.py` with the same map, runtime and `csr.csv` at both; the base figures equal round 1's base receipts):

| Point | Base rom / sram, B | Head rom / sram, B | Delta | RAMB36 base / head | sizeof(struct ctrl_plat) base / head |
|---|---:|---:|---:|---:|---:|
| 1x1, one interface | 109,560 / 47,168 | 110,756 / 47,280 | +1,196 / +112 | 39.0 / 39.5 | 18,432 / 18,528 |
| 1x1, two interfaces | 111,200 / 58,592 | 112,404 / 58,688 | +1,204 / +96 | 42.0 / 42.0 | 19,928 / 20,016 |
| 8x8, one interface | 123,304 / 87,760 | 124,492 / 87,856 | +1,188 / +96 | 52.0 / 52.0 | 19,088 / 19,184 |
| 8x8, two interfaces | 125,048 / 113,936 | 126,252 / 114,032 | +1,204 / +96 | 59.0 / 59.0 | 21,240 / 21,328 |

  `.text` +1,064 to +1,080 B, `.rodata` +120, `.data` +4, `.bss` +88 to +96 at each point. One point's plan moves half a block (1x1, one interface, 39.0 to 39.5 RAMB36). The ledgered 8x8/2if point stays at 59.0, its ROM holding 126,252 of 126,976 B.

## Authoritative references

- #871 and the round 2 ruling on it; plan S11 and decision D9 of #665; R821-1 and R822-1 on this PR.
- REQ-FWX-001; protocol-processor `docs/architecture/06_aecp_engine.md` section 6.11 (the processor's routes, order, receive discard and transmit gate).
- IEEE 1722.1-2021 7.4.43 (Figure 7-68, 7.4.43.1, 7.4.43.2), 7.5.2, Table 7-126 (REBOOT = 0x002A); 6.2.1 (ADPDU, valid_time).
- Milan v1.2 5.4.5.1, 5.4.5.2 (notifications), 5.6.2 (valid_time 10), 5.6.3.3 and Table 5.50 (SHUTDOWN, TMR_DELAY 0 to 4 s), 5.3.5.1, 5.3.7.1, 5.3.7.6, 5.3.8.1 to 5.3.8.3, 5.3.9.1, 5.3.10.1, 5.3.11.1, 5.3.13 (the saved items).
- `docs/design/REBOOT_RESET.md` (#787) sections 3, 4 and 8; `docs/design/MAILBOX_SPLIT.md`.

## How to get into the same state

```sh
git clone https://github.com/kebag-logic/milan-fpga.git
cd milan-fpga
git fetch origin 665-s11-aecp-reboot
git checkout d08d30c6ecbac2e45867c3a509ef309ed081ab15
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
```

The CPU simulation needs the product LiteX tree, the pinned RV32 SDK, Verilator and the offline CPU generator, as `tb/verilator/ctrl_service_budget/README.md` lists them.

## How to validate

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test
python3 sw/firmware/gtest/fw_coverage.py --check
python3 sw/mailbox/publication_census.py --check --selftest
python3 -B tb/verilator/ctrl_reboot/run.py --build-dir /tmp/reboot-plants --self-test --jobs 3
```

Expected result / pass criteria: each exits 0. The firmware self-test reports every planted defect caught, the AECP and platform REBOOT ones included; the census reports the REBOOT plants refused; the REBOOT simulation prints `ctrl_reboot: PASS (0 finding(s))` and `12 of 12 plants and controls caught`, with no `PYTHONHASHSEED` needed in the environment.

**Local gates at `d08d30c6ecbac2e45867c3a509ef309ed081ab15`**, each on its own fresh clean clone:

| Gate | Result |
|---|---|
| `rtl-fast`, `elaborate`, `rtl`: every `run:` step of every job a pull_request to `dev-soft-core` triggers | 88 ran, rc 0; 167 not run, each with a stated reason (hosted-only installs, uploads and orchestration; `verilator-shards` replicated by the sweep); 0 bad. One step needed a second run: elaborate-gates-1's LiteX simulation aggregate first ended UNKNOWN (exit 92) when `test_soc_timing_cuts` reached the runner's 900 s wall clock on a loaded host. Rerun alone on the same clone it passed 8 of 8, and the test alone with no wall clock passed in 1,712 s. This round changes no SoC path that test builds. |
| Publication census `--check --selftest` | 6 shapes, 246 checks, 0 failures; 0 of 164 arms failed; the three REBOOT plants refused on their own words |
| `docs.yml`: every `run:` step | 64 ran, rc 0; 31 not run, each with a stated reason; 0 bad |
| Full Verilator sweep, four native shards | 65 of 65 suites, 2,192,899 checks, 0 in-suite failures, 0 timed out; suite-cancellation preflight PASS on each shard |
| `test_ctrl_firmware.py --require-rv32 --self-test` | PASS; control campaign 583 of 583 caught |
| `fw_coverage.py --check` | PASS (35 files) |
| Firmware mutant drivers | AECP 152 of 152; SRP 280, PASS; saved-state store 109 of 109 planted defects reddened (5 shapes, 435 tests) |
| `ctrl_boundary.py` (firmware-boundary, firmware-verilator) | PASS |
| S2's harness, 1x1/1if and 8x8/2if, and its self-test | rc 0, 0 refusals; T_svc misses recorded: 34 (13 of 81 paths) and 57 (29 of 129 paths); every path's worst figure equal to round 1's head |
| `test_builder.py --require-rv32` | all gates pass except two not run: gate 11's calibration arm needs a Vivado place report from a build this host does not have. Gate 1b's `MAKEFLAGS += -e` mutation cannot show on the make 4.3 that run had first on PATH; gate 1b alone with GNU Make 4.4.1 passes in full |
| `cd tests && behave` | 14 features, 508 scenarios, 2,330 steps passed |
| `git diff --check` against the merge base | clean |
| `tb/verilator/ctrl_reboot/run.py --self-test`, and plain, no seed in the environment | both PASS (0 findings); 12 of 12 plants and controls caught on their own words |
| `tb/verilator/ctrl_split_boot/run.py`, and `--self-test`, with `PYTHONHASHSEED=0` | PASS; 6 of 6 native controls, 2 of 2 plants, 0 placement controls wrong |
| All-fabric exports, base and head, 1x1 and 8x8 | every generated file equal, apart from LiteX's timestamps and its hierarchy comment's order, which differ between two exports of one commit too |

Not run: the mailbox's full RTL mutant set (`make -C tb/verilator/mbx mutants`): the mailbox RTL is unchanged here, and the sweep's mbx suite ran its quick set. The hosted `rtl-fast`, `verilator-suites` and `yosys-portability` contexts remain mandatory.

## Known limitations / out of scope

- The CPU simulation builds no datapath: "on the wire" is the mailbox's transmit face. From there the fabric path to the MAC is cut-through, and `KL_reboot_ctrl`'s egress wait (#787, its own suites) holds the PHY until every frame given to the MAC has left. The bench's REBOOT cycles are S12's.
- The PHY hold is simulated for 50 of its 3,500 ms, and the IPROG word and the configuration load not at all; the ADP figure adds the RTL's hold and states the margin left for the load.
- The configuration and the sampling rate cannot be set away from their defaults at the shipping shape (one configuration, one rate), so they are read back, not graded.
- The transmit gate has no CPU-simulation plant: in that scenario no producer sends between ENTITY_DEPARTING and the port, so a plant there would have nothing to show. Host B20 holds the DEPARTING for 5 s with producers running, and the simulation's grader control proves the check itself.
- The reviewer probe `quiet-without-the-face-poll` (R821 S2, not taken by the ruling) still escapes, as at round 1: the host model acknowledges a face commit at once.
- R821 S4 not taken, as the table above states.
- S2's harness: it builds the SRP fixture image, not the platform image, so this round's platform changes do not reach it, and every path's worst figure equals round 1's head. Against the base (`1d6bf5556a`), whose `results.json`, logs and tables are now published, the same 13 of 81 paths are over T_svc at 1x1/1if. At 8x8/2if 29 of 129 are over at the head and 31 at the base: three paths fall under it, and `acmp.probe_tx.if1` goes over it, 5.416 ms at the base and 13.602 ms at the head. The misses are recorded, not graded, and the loop's budget is S2b's (#810).
- The split boot simulation (`tb/verilator/ctrl_split_boot/run.py`, not this lane's) pins no hash seed. With none in the environment it refused twice at an intermediate head, on the same `csr.csv` comparison R822-F3 found in the REBOOT simulation; it ran with `PYTHONHASHSEED=0` here. Its owner should pin the seed as the REBOOT simulation now does.
- Out of scope, as #871 states: the bench's 50 soft resets (S12), the saved-state format (#823), the firmware loop (S2b, #810).

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
