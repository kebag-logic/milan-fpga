# HANDOFF: #871 (#665 S11), AECP REBOOT on the core ([A761], round 1)

Status: REVIEW READY at head `b29f94d7aa1d73c4d1eef705a42d9a3a34fc4702` (six commits on dev-soft-core `1d6bf5556a`); every gate below passed at that head; nothing pushed. Acceptance items 2 to 5 are met; item 1 is met for six of the eight items and the binding, so the PR body does not close #871 (Open risks 1).

Commits: `79158b750c` the reset port and the census; `38b051833e` the firmware's REBOOT; `3be8410e24` two more host checks and the platform's redundant state check dropped (the coverage ratchet found it); `2dc41d2189` the CPU simulation and the docs; `bc939bc727` three mutant anchors my code had made ambiguous or removed, and the simulation's figures restated.

**Two earlier gate passes are not cited.** The first, at `2dc41d2189`, was stopped: its firmware campaigns refused: `identify-refusal-body-lost` and `unknown-body-lost` (AECP) found their anchors twice, because `reboot()` repeated their text, and `plat-loop-before-ready` found its anchor nowhere after `ctrl_plat_step` was restructured. I had planted only the new mutants before committing. A check of all 730 anchors (`anchors.py`) then found exactly those three, `bc939bc727` fixes them, and campaign shards 1 to 3 then passed on the lane tree (580 of 580 control mutants, every AECP defect), with the coverage ratchet. The REBOOT simulation was rerun at that tree, and its figures moved by a few cycles.

The second, at `bc939bc727`, was cut by a host restart and then run again whole. It passed everything but two steps. `rtl-fast` firmware-boundary `ci_step_9` refused `tb/verilator/ctrl_reboot/run.py`: it names the firmware's tree and was in none of the boundary gate's tables; `b29f94d7aa` lists it. `elaborate` elaborate-gates-1 `gate_19` ended UNKNOWN (exit 92) twice, `test_soc_timing_cuts` at the runner's 900 s wall clock with the other seven simulations passed, on a host whose shared CPUs were 100% busy; run alone with no wall clock it passed in 814 s, and my diff changes none of the SoC paths it builds. At `b29f94d7aa`, `gate_19` passed, eight of eight.

- TAKEN: issuecomment-6765258088 (2026-11-10). REVIEW READY: issuecomment-6780168002 (2026-11-10), at `b29f94d7aa1d73c4d1eef705a42d9a3a34fc4702`.
- Lane `$LANES/665-s11-aecp-reboot`, branch `665-s11-aecp-reboot`; scratch `/data-2/milan/tmp/665s11-a761`.
- #822 (#787's reset) is on dev-soft-core: merge `1f29f18927` is an ancestor of `1d6bf5556a`.
- The split ties the request to 0 (`hdl/milan/milan_datapath.sv:10143`, `assign pp_reboot_req_w = 1'b0;`), so the split had no CPU-driven reset port.
- `docs/spec-refs.md`, named by the assignment, does not exist in the tree. IEEE 1722.1-2021 7.4.43 was read from the local standard instead.

## Decisions

- **The carrier is the platform reset port, not a face-block field.** `docs/design/MAILBOX_SPLIT.md` left the carrier to this lane ("a face-block level being the expected end state, decided in that lane"). A face-block field adds a field to `sw/mailbox/mailbox.yaml`, a contract change the assignment excludes. The smallest port with no contract change is one LiteX CSR bit (`milan_soc.CtrlReboot`, `ctrl_reboot_req`, bank `n_locs - 3`), crossed by a `MultiReg` into `milan_cd` onto a new `milan_datapath` input `i_reboot_req`. The split branch drives `pp_reboot_req_w` from it. `reboot_req_o` stays class G with its all-fabric exclusion; the split census holds the net to that one port (`G_CARRIED`).
- **ENTITY_DEPARTING before the reset.** REBOOT_RESET.md section 1 states a REBOOT owes the network SUCCESS, the notification and ENTITY_DEPARTING (Milan v1.2 5.6.3.3), which #396's `power.reboot-reset` grades. The platform shuts ADP down once the REBOOT's frames have left, and fires the port once ADP's ring has drained.
- **Nothing is taken once the port fired.** A bind after the port would start a journal write during the 3.5 s PHY hold, whose erase can outlast it, and the reload would read a busy flash (REBOOT_RESET.md section 4 states a conformant writer starts none). From the port's write the platform services only the store and its F_NVM (`quiet`).
- **The sequence runs in the console's poll.** The loop's poll table is full (8 of 8 at the composition), and `sw/firmware/ctrl/loop` is S2b's.
- **REBOOT without a reset port stays NOT_IMPLEMENTED** (`aecp_config.reboot`), so every other composition and the twin are unchanged.

## Changes (file:line, reason)

| File:line | Reason |
|---|---|
| `hdl/milan/milan_datapath.sv:619` `i_reboot_req` | the split's REBOOT request, in `axis_clk`, the input that stands for the processor's `reboot_req_o` |
| `hdl/milan/milan_datapath.sv:10149` | the split branch drives `pp_reboot_req_w`, and so `reboot_ctrl.reboot_req_i`, from that input (it was `1'b0`) |
| `sw/litex/milan_soc.py:3171` `CtrlReboot`, `:3189` `add_ctrl_reboot` | one CSR bit `ctrl_reboot_req`, its bank pinned at `n_locs - 3` (a new bank must not move an old one; measured at `0xf000e800` in the product split SoC and the test SoC) |
| `sw/litex/milan_soc.py:3214-3216` | `add_ctrl_mailbox` adds the port; with the split datapath a `MultiReg` crosses it into `milan_cd` |
| `sw/litex/milan_soc.py:1383` | the split's `milan_datapath` Instance binds `i_reboot_req`; the all-fabric one leaves it unread, as it leaves `i_ctl_*` |
| `tb/verilator/ctrl_service_budget/split_soc.py:383` | every CPU test SoC (S2's, S3's, S5's, S8's) carries the port, so the platform map's new row resolves on each |
| `sw/mailbox/census_split.py:66`, `:249` `G_CARRIED`, `:590` | the split census holds `pp_reboot_req_w` to `i_reboot_req` alone, never a constant |
| `sw/mailbox/census_plants.py:545`, `:599`, `:603` | the anchor follows the RTL; two plants: the request from another port, and tied off |
| `sw/mailbox/census_ports.py:59` | the exclusion's docstring: the carrier is the reset port, so `reboot_req_o` stays G in the all-fabric census |
| `scripts/check_solution_docs.py:181` and the two integrator tables | the new port's group and tie-off |
| `docs/litex/CLOCK_DOMAINS.md`, `docs/diagrams/cdc_census.*` | the crossing's row; the census regenerated through its generator (four `MultiReg` call sites) and `rsvg-convert` |
| `sw/firmware/ctrl/aecp/aecp.h:169` `aecp_config.reboot`, `:219`, `:240` `aecp_reboot_due` | REBOOT only where the platform resets; the acceptance state and the release |
| `sw/firmware/ctrl/aecp/aecp_commands.c:546` `reboot`, `:671` | 7.4.43's routes in the processor's order; NOT_IMPLEMENTED without a port |
| `sw/firmware/ctrl/aecp/aecp.c:197`, `:200`, `:400`, `:453`, `:630` | no command after the SUCCESS; accepted at it; completions tracked in order; due once every frame owed has completed; no probe or notification after it |
| `sw/firmware/ctrl/plat/ctrl_plat.c:171-215` | `adp_drained`, `reboot_step` (ADP SHUTDOWN, then the port once every DEPARTING has left), the console poll that runs it |
| `sw/firmware/ctrl/plat/ctrl_plat.c:271`, `:304` | AECP answers REBOOT only with a port; the console's slot runs the sequence (the poll table is full) |
| `sw/firmware/ctrl/plat/ctrl_plat.c:332` `quiet`, `:348` | once the port fired, only the store and its F_NVM, so the write in progress completes and nothing new starts during the PHY hold |
| `sw/firmware/ctrl/plat/ctrl_plat.h:26`, `:104`, `:123-124` | the sequence's contract; `env.reboot`; the platform's state |
| `sw/firmware/ctrl/plat/ctrl_plat_gen.py:54`, `ctrl_plat_main.c:25`, `test/ctrl_plat_csr.csv:12` | the port's address from the SoC's own `csr.csv` |
| `sw/litex/ctrl_memory.py:217`, `ctrl_memory_ledger.py:26`, `docs/design/SPLIT_CONTROL_MEMORY.md` | `sizeof(struct ctrl_plat)` re-measured at the four points (+32 B each; 21,272 B at the ledgered 8x8/2if point), as the ledger requires after a change to that struct |
| `sw/firmware/ctrl/test/test_aecp.cpp`, `aecp_wire_model.hpp`, `test_aecp_debug.cpp` | three `Core.Reboot*` tests; the new member in three brace initialisers |
| `sw/firmware/ctrl/test/test_plat_boot.cpp` | B11 to B18 on the mailbox model |
| `sw/firmware/ctrl/test/aecp_mutants.py`, `plat_mutants.py` | eleven and ten planted defects |
| `tb/verilator/ctrl_reboot/` | the CPU simulation (new) |
| `sw/firmware/ctrl/test/ctrl_configs.py:177` | the TSN stack boundary gate finds `tb/verilator/ctrl_reboot/run.py` by text (it names the firmware's tree); it is listed in `OUTSIDE` as the split boot simulation is, since it delegates every firmware compile to `ctrl_plat_image.py` and `runtime_ssp.py` and its own compiles build only its Verilator model |
| `docs/design/REBOOT_RESET.md` section 8, `MAILBOX_SPLIT.md`, the AECP and platform READMEs | the split's REBOOT, its carrier, and the evidence |

## New checks (planted mutant, failing words)

Each mutant is planted into a copy of the tree by its campaign; each named test must fail on the words shown (`[FAIL] <test>: <words>`).

**AECP core** (`aecp_mutants.py`, test file `test_aecp.cpp`), acceptance items 2, 3 and 5:

| Mutant | Edit | Test | Failing words |
|---|---|---|---|
| `reboot-without-a-reset-port` | REBOOT taken without `cfg.reboot` | `Core.RebootIsNotImplementedWithoutAResetPort` | REBOOT without a reset port is NOT_IMPLEMENTED |
| `reboot-short-not-bad-arguments` | a short command NOT_SUPPORTED | `Core.RebootRefusalsLeaveTheEntityInService` | BAD_ARGUMENTS short of Figure 7-68's four bytes |
| `reboot-any-descriptor-type` | the type check removed | same | NOT_SUPPORTED for a STREAM_INPUT; NOT_SUPPORTED for a MEMORY_OBJECT |
| `reboot-any-entity-index` | the index check removed | same | NO_SUCH_DESCRIPTOR for another ENTITY index |
| `reboot-ignores-the-lock` | the lock check removed | same | ENTITY_LOCKED under another controller's lock; ENTITY_MISBEHAVING while a change waits for the platform |
| `reboot-accepted-on-a-refusal` | accepted on any status | same | resetting nothing |
| `reboot-notifies-no-one` | no notification | `Core.RebootIsAnsweredNotifiedAndDueOnlyOnceItsFramesComplete` | the SUCCESS response, then one notification |
| `reboot-never-accepted` (item 3) | the acceptance removed | same | due once every frame of the REBOOT has completed; no command is taken after a REBOOT's SUCCESS |
| `reboot-due-before-its-frames-complete` (item 2) | the completion test removed | same | not due before the response has left |
| `reboot-serves-after-its-success` | commands taken after it | same | no command is taken after a REBOOT's SUCCESS |
| `reboot-probes-after-its-success` | probes and notifications started after it | same | no probe or notification is started after a REBOOT's SUCCESS |

**Platform** (`plat_mutants.py`, test file `test_plat_boot.cpp`, arm `platboot1`):

| Mutant | Edit | Test | Failing words |
|---|---|---|---|
| `plat-reboot-before-the-response` (item 2) | the port written at the acceptance | `Boot.B12TheResetWaitsForTheResponseToLeave` | B12 no reset while the mailbox holds the response |
| `plat-reboot-ignored` (item 3) | the port never written | B11, B15, B16 | B11 the reset port is written once; B15/B16 the REBOOT fires the reset port |
| `plat-reboot-without-departing` | no ADP SHUTDOWN | B11 | B11 every interface sends ENTITY_DEPARTING |
| `plat-reboot-departing-owed-ignored` | an owed DEPARTING not waited for | `Boot.B18ADepartingTheRingRefusedHoldsTheReset` | B18 ENTITY_DEPARTING leaves before the reset |
| `plat-reboot-before-departing-left` | ADP's ring not waited for | B12 | B12 no reset while the mailbox holds ENTITY_DEPARTING |
| `plat-reboot-without-a-port` (item 5) | REBOOT answered with no port | B14 | B14 without a reset port REBOOT is NOT_IMPLEMENTED |
| `plat-reboot-under-another-lock` (item 5) | the lock check removed | B13 | B13 ENTITY_LOCKED under another controller's lock |
| `plat-reboot-stops-the-store` (item 4, tears the write) | the store not serviced after the port | B16 | B16 the change made before the REBOOT is kept |
| `plat-reboot-hides-the-drain` (item 4) | F_NVM not published after the port | B16 | B16 the drain ends because the write completed, not at its deadline |
| `plat-reboot-takes-frames-after-the-port` | the loop serviced after the port | B17 | B17 a bind after the reset port fired is not taken |

**Split census** (`census_plants.py`, rule `split-tied`):

| Plant | Failing words |
|---|---|
| the REBOOT request from another port in the split | pp_reboot_req_w, the net of the wrapper's G output reboot_req_o, is driven by i_ctl_lock_held in the split, not by i_reboot_req |
| the REBOOT request tied off in the split | pp_reboot_req_w, the net of the wrapper's G output reboot_req_o, is driven by a constant in the split, not by i_reboot_req |

**CPU simulation** (`tb/verilator/ctrl_reboot/run.py --self-test`): four planted images, each built from a planted firmware tree and run, and five grader controls planted into a clean log; each must give a finding of its grade:

| Plant or control | Edit | Grade | Failing words |
|---|---|---|---|
| plant `reset-before-the-response` (item 2) | the port written at the acceptance | ORDER | ENTITY_DEPARTING did not leave between the notification and the reset port; a frame given after the reset port fired was taken |
| plant `request-ignored` (item 3) | the port never written | ORDER | the reset port never fired (NOREQ) |
| plant `write-torn` (item 4) | the store not serviced after the port | JOURNAL | the drain ended cap, not because the state was durable: the write in progress did not complete |
| plant `any-descriptor-type` (item 5) | a REBOOT of any type taken | REFUSE | refuse-input answered status 0 at cdl 16, not 11 at cdl 16 |
| control `response-after-the-port` | the port's rise one cycle after the REBOOT arrived | ORDER | the REBOOT's SUCCESS left the mailbox after the reset port fired |
| control `drain-at-its-cap` | the drain's end at the cap | JOURNAL | the drain ended cap |
| control `no-advertisement` | the boot's ADP frames deleted | ADP | no ENTITY_AVAILABLE after the reset |
| control `name-reverted` | the entity name read back changed | RESTORE | the #396 grader says FAIL ... differs ['entity_names'] |
| control `binding-lost` | the binding's talker zeroed | RESTORE | the #396 grader says FAIL ... differs ['stream_binding'] |

## Measurements

**The request-to-reset bound** (CPU simulation, 1x1/1if, the split CPU at 50 MHz): from the REBOOT command's last byte at the mailbox to the reset port, 445,707 bus cycles, 222,853 CPU cycles, 4.457 ms (SUCCESS at 2.166 ms, notification 2.309 ms, ENTITY_DEPARTING 3.799 ms). Then KL_reboot_ctrl: a write in progress kept the drain 582.094 ms (durable), the egress wait quiet; then the RTL's 3,500 ms hold, 3 ms and 8 clocks to the IPROG word (REBOOT_RESET.md section 3). REBOOT to the first ENTITY_AVAILABLE after the reset: 4,590.218 ms of 20,000 ms, 15,409.782 ms left for the configuration load, which is not modelled.

**The linked-size delta** (`ctrl_plat_image.py`, the base tree exported from `1d6bf5556a` against the same map and runtime; receipts `receipts/size/`):

| Point | Base rom / sram, B | Head rom / sram, B | Delta | RAMB36 |
|---|---:|---:|---:|---:|
| 1x1, one interface | 109,560 / 47,168 | 110,428 / 47,216 | +868 / +48 | 39.0, unchanged |
| 1x1, two interfaces | 111,200 / 58,592 | 112,068 / 58,640 | +868 / +48 | 42.0, unchanged |
| 8x8, one interface | 123,304 / 87,760 | 124,172 / 87,792 | +868 / +32 | 52.0, unchanged |
| 8x8, two interfaces | 125,048 / 113,936 | 125,916 / 113,968 | +868 / +32 | 59.0 (ledgered), unchanged; rom 125,916 of 126,976 |

Measured from a clean clone at `b29f94d7aa`. `.text` +744 at the one-interface points and +740 at the two-interface ones, `.rodata` +120, `.data` +4, `.bss` +32 at each. `sizeof(struct ctrl_plat)` +32 B at each point (18,464, 19,960, 19,120 and 21,272 B, the ledger's figures).

**S2's harness against the base** (the same harness, `--record-budget-findings`, run at `1d6bf5556a` and at the head; `receipts/s2-base/s2-compare.txt`, `gates/tools/s2_compare.py`): at 1x1/1if the same 13 of 81 paths are over T_svc at both, every path within -2.268 to +1.450 ms of the base. At 8x8/2if 29 of 129 paths are over at the head and 31 at the base: `acmp.disconnect_tx.if0`, `acmp.unbind_rx.if0` and `acmp.unbind_rx.if1` are no longer over, and `acmp.probe_tx.if1` is newly over, 5.416 ms at the base and 13.602 ms at the head. Every path moved within -15.343 to +8.186 ms, both ways, and the probes start at other cycles (that one at 123,293,598 at the base, 118,852,918 at the head): the stimulus timeline moved with the image, not one fixed cost.

## Gate table

All at `b29f94d7aa1d73c4d1eef705a42d9a3a34fc4702`, each on its own fresh clean clone; the receipts are under `receipts/` (index `receipts/INDEX.md`; host prefixes replaced by named placeholders; a file over 200 KB is listed in its directory's `LARGE.tsv` with its size and sha256, and `RAW.tsv` holds each source file's digest).

| Gate | Command | Result | Receipt |
|---|---|---|---|
| `rtl-fast`, `elaborate`, `rtl`: every `run:` step of every job a pull_request to dev-soft-core triggers | `gates/tools/wf/run_wf.py` per job, `verify_wf.py` over the workflows at the head | 88 steps ran, rc 0; 167 not run, each with its reason (`gates/tools/wf/not_run.json`); 0 bad. Among them `rtl-fast` (the verdict job), firmware-boundary (`ctrl_boundary: PASS`, 3,258 compiled sources), firmware-verilator (`ctrl_boundary: PASS`), elaborate-gates-1 `gate_19` (8 of 8 LiteX simulations), yosys-shards 0 to 3 of 4, publication-census (6 shapes, 246 checks, 0 failures; self-test 0 of 164 arms failed; 0 of 57 rules no arm proves; the three REBOOT plants refused) | `gates/wf-table.md`, `gates/wf/` |
| `docs.yml`: every `run:` step | the 829 docs runner and verifier | 64 ran, rc 0; 31 not run, each with its reason; 0 bad | `gates/docs-table.md`, `gates/docs/` |
| Full sweep (`rtl` verilator-shards' suites) | `native-shards.py`, 4 units, MemoryMax 10G, `MAKEFLAGS=-j4 --no-print-directory`, CPU ranges from `cpu_ranges.py pick`, the capture_coherence shard on 4 CPUs | 65 of 65 suites passed, 2,192,899 checks, 0 in-suite failures, 0 timed out; the suite-cancellation preflight PASS on each shard (no #833 re-run) | `sweep/` |
| Firmware self-test | `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` | `test_ctrl_firmware: PASS`; control campaign 580 of 580 caught (the ten platform REBOOT defects among them) | `gates/lane/fw_selftest.log` |
| Coverage ratchet | `fw_coverage.py --check --jobs 4` | `firmware coverage: PASS (35 files)` | `gates/lane/fw_coverage.log` |
| Firmware mutant drivers | the AECP driver `aecp_mutants.py`; the control, AECP and SRP campaigns in the four firmware jobs; the saved-state store's `test_ctrl_nvm.py --require-rv32 --self-test --jobs 8` | AECP 150 of 150 (the eleven REBOOT defects among them); control 580 of 580; SRP 280 `[ok]`, `PASS`; saved-state 5 shapes, 435 tests, all 109 planted defects reddened | `gates/lane/aecp_mutants.log`, `gates/wf/rtl-fast.firmware-*-mutants__ci_step_9.log`, `gates/lane/nvm_selftest.log` |
| S2's harness | `ctrl_service_budget/run.py --self-test`; `--point 1x1` and `--point 8x8`, `--record-budget-findings --jobs 8` | self-test 0 failures; 1x1/1if 18 groups graded, 0 refusals, 34 T_svc misses (13 of 81 paths); 8x8/2if 17 groups, 0 refusals, 57 misses (29 of 129 paths), recorded as the ruling says | `gates/lane/s2_*.log` |
| Builder | `sw/builder/test_builder.py --require-rv32` | `ALL GATES PASS EXCEPT 1 NOT RUN`: gate 11's calibration arm needs a real Vivado place report from a build tree this host does not have | `gates/lane/builder.log` |
| behave | `cd tests && behave` | 14 features, 508 scenarios, 2,330 steps passed | `gates/lane/behave.log` |
| Whitespace | `git diff --check 1d6bf5556a HEAD` | rc 0, no output | `gates/lane/diffcheck.log` |
| The REBOOT simulation | `tb/verilator/ctrl_reboot/run.py --self-test --jobs 3` | `ctrl_reboot: PASS (0 finding(s))`; 9 of 9 plants and controls caught; figures identical to the run at `bc939bc727` | `gates/lane/reboot.log` |
| The split boot simulation | `ctrl_split_boot/run.py`, and `--self-test` | rc 0; self-test 6 of 6 native controls, 2 of 2 plants, 8 of 8 placement controls | `gates/lane/boot_*.log` |
| The saved-state target | `nvm_split_target/run.py --self-test` | rc 0 | `gates/lane/nvm_target_selftest.log` |

Not run: the full mailbox RTL mutant set (`make -C tb/verilator/mbx mutants`). It plants RTL defects in the mailbox, which this branch does not change; the quick set ran in the sweep's mbx suite, 7 of 7 caught. The bench, flashing and Vivado routes are outside this lane.

## Open risks

1. **Acceptance item 1 is met for six of the eight items and the binding.** The configuration and the sampling rate cannot leave their defaults at the shipping shape (the builder ships one configuration; the shape advertises one AUDIO_UNIT rate, 48 kHz). The simulation reads both back unchanged and reports them NOT RUN, as #396's grader rules a pre-cycle value equal to its default. A shape with a second configuration or rate would grade them. The PR body therefore says Relates to #871, not Closes.
2. **One more T_svc miss at 8x8/2if, three fewer** (Measurements). The misses are recorded, not graded, under S2's ruling, and the loop's budget is S2b's (#810).
3. **The CPU simulation builds no datapath**: "on the wire" is the mailbox's transmit face, and the PHY hold is simulated for 50 of its 3,500 ms, with the IPROG word and the configuration load not modelled. The bench's REBOOT cycles are S12's.
4. **A datapath that never drains the mailbox's rings holds the reset back**: the platform writes the port only once ADP's ring has drained.
5. **Host load**: elaborate-gates-1 `gate_19` ran out its 900 s wall clock twice at `bc939bc727` on a host whose shared CPUs were 100% busy (history above); it passed at the head.
