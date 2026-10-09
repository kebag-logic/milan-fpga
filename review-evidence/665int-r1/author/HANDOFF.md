[A582]

# F-INT handoff, round 2 (PR 1 of 2: the publication block)

Status: REVIEW READY, posted on #665 as comment 6091286964. Every gate below
exits 0. Not pushed; no review object exists.
Branch: `665-int-split` -> `dev`. Base (dev): `7c1b52bee26b497080ee22b1c1986109f80a5ee7`.
Round-2 start head: `79efa393ccb92dd80f4ed219a932a1e5c3cae52d`.
Head: `25bbe4d956e79de979783d7e4706a5581c0742a7`.

Ruling applied: #665 comment 6088423771. PR 1 is the firmware-to-fabric
publication block in the mailbox window and its firmware writers; the build
switch is PR 2, after F5. Earlier rulings read for context: 6087214078,
6087462816, 6087654804. Round-1 STOP: 6088406545.

An earlier session on this round was stopped by the service memory cap after
`f8ea6936` and posted nothing. Its commits were kept. Re-running its gates
found three defects, each fixed by a new commit:

- The Vivado front-end gate (`scripts/xvlog_gate.py --check`) failed: the
  generated `KL_mbx.sv` read the publication storage before declaring it.
- The naming ratchet (`scripts/measure_naming.py --check`) failed: the new
  port `pub_idle_slope_o` documented bits per second without naming the unit.
- The full firmware campaign let one existing SRP plant escape,
  `cancelled-link-never-recovers`, which dev catches. Its test relies on a
  LINK record staying held while the level drops and returns. The reset's new
  publication writes made the host model post that record, and the UP record
  that followed restored the link for the plant.

## Commits on the base

| SHA | Subject |
|---|---|
| `780a199ca8a62d4ceebe39df952710cffcb1f828` | Compare SRP transmit opportunities canonically |
| `79efa393ccb92dd80f4ed219a932a1e5c3cae52d` | Plant a duplicated SRP declaration apart from an extra one |
| `21b6dd8c58061c26dfc67c35b693fadc5f366796` | Add the firmware-to-fabric publication block to the mailbox contract |
| `0a62616e08dd58928e73183ecdf16dbee330becd` | Export each sink's SID_VALID beside its stream_id instead of gating every bit |
| `5a50b2045427313527197eb22cd0f8276ef4b015` | Publish the firmware owner's class-D state before the responses that promise it |
| `49542c1651a96ac0e16e435cbd6786a53c0ebcfd` | Document the publication block, its writers and the bounds they add |
| `f685a5b2fa9015b49bbb7d414cc954d065b71393` | Hold each SRP slope and Domain publish past its first MSRP frame as a plant |
| `f8ea69362f23535924875c562338c02ca61424dc` | Record the publication block's measured area |
| `b4582fe0a280a336c0ddefeaa677c37f9de4856c` | Declare the publication registers before the read-back that names them |
| `9b73a8c66ea301819917dfacafe0da23b975245a` | Name the published idle slope's unit on its port |
| `25bbe4d956e79de979783d7e4706a5581c0742a7` | Hold the model's event poster so the cancelled LINK record stays held past the publication writes |

The first two are round 1's comparator commits, kept as infrastructure (the
ruling). VERSION is unchanged. 47 files change against dev. Outside the mailbox
contract and its generated outputs, the mailbox bench, the firmware and its
tests, and the docs, the only file changed is `sw/litex/milan_soc.py`, in the
`--ctrl-mailbox` instance only.

## Changes with source anchors

Line numbers are at the head.

### The contract and the generator

| Anchor | Change |
|---|---|
| `sw/mailbox/mailbox.yaml:63` | contract minor 2 (2.2): the publication block, additive |
| `sw/mailbox/mailbox.yaml:70` | `publication: {sources: 16, sinks: 16}` per interface |
| `sw/mailbox/mailbox.yaml:315` | `interface_publication_registers`: base `0x800`, stride `0x200`; `DA_GATE`, `LICENCE`, `IDLE_SLOPE`, `SR_DOMAIN`; sink entries at `+0x100 + 0x10*k`: `SID_LO`, `SID_HI`, `BINDING{BOUND, SID_VALID}` |
| `sw/mailbox/mailbox_model.py:408` | `_check_publication`: sizes 1..32, registers before the sink base, each entry inside its stride, the block inside `[0x400, window)`, no overlap with a ring |
| `sw/mailbox/mailbox_model.py:575`, `:660` | the generated constants (`PUB_BASE`, `N_PUB_SOURCES`, `N_PUB_SINKS` and the register offsets) |
| `sw/mailbox/mailbox_skeleton.py:52` | `PUB_OUTPUTS`: one `pub_*_o` port per field, `pub_idle_slope_bps_o` naming its unit |
| `sw/mailbox/mailbox_skeleton.py:186`, `:292`, `:329` | the ports, the decode (interface, sink, register; holes and absent interfaces decode to nothing), and the storage, write and output blocks |
| `sw/mailbox/mailbox_skeleton.py:552` | wiring checks: power-of-two strides, read-write only, the field set, OPEN/ACTIVE as wide as the sources, both SID words 32 bits |
| `sw/mailbox/mailbox_skeleton.py:694` | emit order: the publication block before the read-back that names its storage |
| `sw/mailbox/gen_mailbox.py:85`, `:257` to `:265`, `:312` to `:316` | the cross-check covers `PUB_REG` and `PUB_SINK_REG`; three output and the contract self-test arms |
| `sw/mailbox/mailbox_emit.py:274` | reference sections for both register sets |
| `hdl/milan/mailbox/KL_mbx.sv:62` to `:70` | nine new output ports (generated) |
| `hdl/milan/mailbox/KL_mbx.sv:157` | `pub_decode` |
| `hdl/milan/mailbox/KL_mbx.sv:259` to `:313` | storage, `pub_write` (reset to 0, field masks, only on a full-strobe write `wr_w`), `pub_out` |
| `hdl/milan/mailbox/KL_mbx.sv:343` | read-back of the seven registers, inside `reg_read` (`:316`) |
| `hdl/milan/mailbox/KL_mbx_pkg.sv:34`, `:300` | sizes, base and register constants (generated) |
| `sw/firmware/ctrl/mbx/mbx_contract.h`, `docs/reference/MAILBOX_CONTRACT.md` | generated |
| `sw/litex/milan_soc.py:2540`, `:2560` to `:2569` | the `--ctrl-mailbox` instance names the nine ports as unread signals; the default build carries no mailbox |

A partial strobe on a publication register is refused and counted in `BUS_ERR`
by the existing `refused_w` path (`KL_mbx.sv:90`), as on every other register.

### The bench, the host model and the driver

| Anchor | Change |
|---|---|
| `tb/verilator/mbx/tb_mbx_top.sv:82` to `:91` | the nine outputs on the bench top |
| `tb/verilator/mbx/frames.hpp:28`, `bench.hpp:178` | `PubView`: the datapath's view (the stream_id read as 0 while `SID_VALID` is clear) |
| `tb/verilator/mbx/suite.hpp:1668` | `check_publication`, checks P0 to P5, through both adapters, at two interfaces and on the host model |
| `tb/verilator/mbx/mutants.py:423` to `:469` | ten RTL plants, each through both adapters; `top-pub-sid-valid-held-high` in the quick set |
| `sw/firmware/ctrl/host/mbx_model.c:612` to `:686`, `:780`, `:891` | the model's twin: decode, masks, holes, view, read and write |
| `sw/firmware/ctrl/host/mbx_model.c:130`, `:286`; `mbx_model.h:117`, `:151` | `mbx_model_evt_pause`: the event poster held as a full ring holds the RTL's (test support, commit `25bbe4d9`) |
| `sw/firmware/ctrl/mbx/mbx.c:137` to `:205`; `mbx.h:89` | `mbx_pub_da_gate`, `mbx_pub_licence`, `mbx_pub_idle_slope`, `mbx_pub_domain`, `mbx_pub_sink` (`BINDING` with `SID_VALID` clear, `SID_LO`, `SID_HI`, then `BINDING` with it set when the stream_id is not 0) |

### The writers

| Anchor | Value | Written before |
|---|---|---|
| `sw/firmware/ctrl/acmp/acmp.h:324`, `:377` | the ACMP publish port; the pair the port holds per sink | |
| `sw/firmware/ctrl/acmp/acmp.c:197` | `publish()`: each sink whose (bound, settled stream_id) moved | |
| `sw/firmware/ctrl/acmp/acmp.c:285` | at the top of `transmit()` | any frame of the entry, so the BIND_RX and UNBIND_RX responses |
| `sw/firmware/ctrl/acmp/acmp.c:487` | first in `finish()` | the store and the notifier hear of the change |
| `sw/firmware/ctrl/acmp/acmp.c:510` to `:525` | `sink_reset` keeps what the port holds, so a reset sink is published unbound at the next open | |
| `sw/firmware/ctrl/acmp/acmp_mbx.c:15`, `:69`, `:91` | sinks fit the block; `port_publish` to `mbx_pub_sink` | |
| `sw/firmware/ctrl/maap/maap_mbx.c:62` | `DA_GATE`: bit s open while the range is valid | the allocation is reported (a PROBE_TX_RESPONSE then promises the address) |
| `sw/firmware/ctrl/maap/maap_mbx.c:70` | init refuses more sources than the block holds | |
| `sw/firmware/ctrl/srp/srp_mbx.c:23`, `:64` | sources fit `LICENCE`; `publish_licence`: bit s while source s holds its licence | |
| `sw/firmware/ctrl/srp/srp_mbx.c:804`, `:813` | `LICENCE` | each licence report in the poll |
| `sw/firmware/ctrl/srp/srp_mbx.c:713` to `:725` | `LICENCE` cleared | a reset's revocations |
| `sw/firmware/ctrl/srp/srp_mbx.c:333` | `LICENCE` cleared | destroy's revocations |
| `sw/firmware/ctrl/srp/srp_mbx.c:173` | `IDLE_SLOPE` (the admitted bandwidth, Ethernet overhead included) | the declarations it admits (participant creation, Domain adoption) |
| `sw/firmware/ctrl/srp/srp_mbx.c:243` | `SR_DOMAIN` default, not adopted | the Domain is declared |
| `sw/firmware/ctrl/srp/srp_mbx.c:634` | `SR_DOMAIN` adopted | the declarations that carry it |

ADP owns no value the split datapath consumes: its `available_index` reaches
only CSR status and the AEM face, which the core serves after F5. The ruling
lists ADP among the adapters; no ADP writer is added, and the reason is in
`docs/design/MAILBOX_SPLIT.md:826`. GET_STREAM_INFO needs no publication (the
ruling).

### Documentation

| Anchor | Change |
|---|---|
| `docs/ARCHITECTURE_HW_SW_SPLIT.md:88` to `:92`, `:187` | the publication block in the placement contract; its outputs unread until the switch |
| `docs/design/MAILBOX_SPLIT.md:802` to `:860` | the block: values, registers, writers, ordering, the processor output each stands for, the two-word stream_id, the choices, the bounds |
| `docs/design/MAILBOX_SPLIT.md:871`, `:879` | verification rows for the RTL and the writers |
| `docs/design/MAILBOX_SPLIT.md:1046` to `:1071` | the measured area |
| `sw/firmware/ctrl/README.md`, `sw/firmware/ctrl/srp/README.md`, `sw/firmware/ctrl/maap/README.md`, `tb/verilator/mbx/README.md` | the composed bounds and the tests |

### Bounds the writes add (access counts, host model)

| Macro | Before | After |
|---|---:|---:|
| `ACMP_MBX_LAT_BIND` | 76 | 77 |
| `ACMP_MBX_LAT_UNBIND` | 49 | 50 |
| `ACMP_MBX_LAT_PROBE_RESP` | 28 | 32 |
| `ACMP_MBX_LAT_TIMER_ARM` | 13 | 14 |
| `ACMP_MBX_SINK_WORK` | 23 | 24 |
| `ACMP_MBX_HANDLER_MAX` | 51 | 52 |
| `MAAP_MBX_EVENT_MAX` | 48 | 49 |
| `SRP_MBX_EVENT_MAX` | 1 | 4 (`1 + SRP_MBX_PUB_RESET`) |
| `SRP_MBX_POLL_MAX` | `IF * (4 + 2 * TX)` | `IF * (4 + SRP_MBX_PUB_POLL_MAX + 2 * TX)`, with `SRP_MBX_PUB_POLL_MAX` = 37 |
| `CTRL_APP_SRP_FEEDBACK_MAX` | 6 per sink | 7 per sink |

Each is measured through the real callbacks on the host model. The composed
figures in `sw/firmware/ctrl/README.md` and `docs/design/MAILBOX_SPLIT.md`
follow: the three-protocol pass 1,606 / 1,685, the SRP envelope 1,657 / 2,464,
the composed bound 3,327 / 4,213 accesses at one / two interfaces.

## Tests and the planted defect each catches

### RTL (`tb/verilator/mbx`)

| Check (`suite.hpp:1668`) | Plants (`mutants.py`, each through both adapters) |
|---|---|
| P0 every register and output 0 after reset | (the reset plant below) |
| P1 each register keeps its fields only, at its own interface and sink | `top-pub-domain-unmasked`, `top-pub-sink-index-dropped` |
| P2 each field on its own output, one bit moving one bit | `top-pub-priority-from-vid` |
| P3 the stream_id only while `SID_VALID`, `BOUND` apart, never half written | `top-pub-sid-valid-held-high`, `top-pub-sid-halves-swapped`, `top-pub-bound-from-sid-valid` |
| P4 holes, an entry's fourth word and absent interfaces read 0 and take no write; a partial strobe refused | `top-pub-hole-aliases-a-register`, `top-pub-interface-unchecked` (two interfaces), `top-pub-partial-strobe-accepted` |
| P5 a reset clears the block | `top-pub-licence-kept-through-reset` |

The `mbx` campaign catches 167 of 167 plants after its four positive controls.

### Firmware (GoogleTest; plants in `ctrl_mutants.py` and `srp_mutants.py`)

For each writer the ruling's three plants exist: the publish moved after the
response, a wrong field, the publish skipped.

| Test | Plants it catches (anchor) |
|---|---|
| `DriverUnit.D14PublicationBlock` (`test_unit_driver.cpp:183`) | `pub-sid-valid-set-first`, `pub-sid-halves-swapped`, `pub-domain-priority-and-vid-swapped`, `pub-licence-in-the-da-gate`, `pub-sink-past-the-block` (`ctrl_mutants.py:484` to `:500`) |
| `Suite/MbxModelGroup.PassesOnTheModel/Publication` (the bench suite's P0 to P5 on the host model) | `model-pub-sid-not-gated`, `model-pub-hole-takes-a-write`, `model-pub-every-sink-reads-entry-0` (`:504` to `:511`) |
| `AcmpCore.A31TheBindingIsPublishedBeforeTheResponseThatPromisesIt` (`test_acmp.cpp:1924`) | moved: `pub-acmp-after-the-response` (`:516`); skipped: `pub-acmp-skipped-at-the-end-of-an-entry` (`:521`); wrong field: `pub-acmp-talker-for-the-stream` (`:526`) |
| `AcmpCore.A31LeavingSettlementTakesTheStreamOffTheDatapath` (`:1954`) | `pub-acmp-stream-held-past-settlement` (`:529`) |
| `AcmpCore.A31OnlyAMovedPairIsPublished` (`:1975`) | `pub-acmp-every-sink-every-entry` (`:533`) |
| `AcmpCore.A31RestoredBindingsArePublishedWhenTheTransportOpens` (`:1988`) | `pub-acmp-reset-forgets-the-port` (`:543`); second for `pub-acmp-skipped-at-the-end-of-an-entry` |
| `AcmpCore.A31ACallBackFromThePublishPortIsRefused` (`:2016`) | `pub-acmp-port-unguarded` (`:537`) |
| `AcmpMailbox.B10ThePublicationBlockFollowsEachBindingAheadOfItsResponse` (`test_acmp_mbx.cpp:610`) | `pub-acmp-adapter-drops-the-port` (`:548`); second for the moved and skipped ACMP plants: the writes precede the response's TX_HEAD commit on the model |
| `AcmpMailbox.B11RestoredBindingsArePublishedAtOpen` (`:670`) | second for `pub-acmp-adapter-drops-the-port` |
| `MaapHost.DaGateIsPublishedBeforeEachAllocationIsReported` (`test_maap_mbx.cpp:125`) | moved: `pub-maap-gate-after-the-report`; skipped: `pub-maap-gate-skipped`; `pub-maap-gate-open-while-invalid`, `pub-maap-sources-past-the-block` (`:556` to `:570`) |
| `MaapHost.CallbackWorkAndEveryOutputCount` (`:387`) | wrong field: `pub-maap-gate-one-source-short` (`:563`) |
| `Srp.PubLicenceIsSetAndClearedBeforeEachChangeIsReported` (`srp_mbx.cpp:92`) | moved: `pub-licence-after-the-report`, `pub-licence-after-the-revocations`; skipped: `pub-licence-skipped`, `pub-licence-kept-at-destroy`; wrong field: `pub-licence-wrong-bit` (`srp_mutants.py`) |
| `Srp.PubDomainPrecedesEveryDeclarationThatCarriesIt` (`srp_mbx.cpp:51`) | moved: `pub-domain-adoption-after-the-declarations`, `pub-domain-default-after-the-declarations`; skipped: `pub-domain-adoption-skipped`, `pub-domain-default-skipped`; wrong field: `pub-domain-priority-for-vid`, `pub-domain-default-marked-adopted` |
| `Srp.PubIdleSlopeIsPublishedBeforeTheDeclarationsItAdmits` (`srp_mbx.cpp:122`) | moved: `pub-slope-after-the-declarations`; skipped: `pub-slope-skipped`; wrong field: `pub-slope-halved` |
| `Srp.PollPublicationTermIsMeasuredThroughRealCallbacks` (`srp_app.cpp:214`) | `pub-term-poll-understated`, `pub-term-reset-understated` |
| `Srp.CancelledLinkRecordRecoversFromLevelAndFencesOldReceive` (`srp_mbx.cpp:841`) | the existing `cancelled-link-never-recovers` (`srp_mutants.py:503`), which escaped at `9b73a8c6` and is caught again; new: `cancelled-link-record-posted` (`:508`), a poster that ignores the hold, caught by the test's new precondition (`srp_mbx.cpp:859`, "the DOWN record stayed held") |

The SRP moved-after plants hold the publish back until `send_pdu` has
committed the interface's next MSRP frame, the latest a publish can move
(`held_back`, `srp_mutants.py:50`). The Domain test reads every frame from
before the link drops (`srp_mbx.cpp:60` to `:63`), so a default Domain
published after the restart's first declarations is caught.

At the head the firmware campaign catches 492 of 492 `ctrl_mutants.py` plants
and 186 of 186 `srp_mutants.py` plants (each reported caught by name), over 51
arms.

### Gate-level checks of this change, each with its plant

| Check | Defect it catches |
|---|---|
| `scripts/xvlog_gate.py --check` | the publication storage read before its declaration: red at `f8ea6936` (`VRFC 10-3380`, `pub_da_gate_r`), 0 findings at `9b73a8c6` |
| `scripts/measure_naming.py --check` | `pub_idle_slope_o` hiding bits per second: red at `b4582fe0`, PASS at `9b73a8c6` |
| `check_mbx_ports.py` (packet) on the `--ctrl-mailbox` export | the instance's ports against `KL_mbx`'s: 35 of 35 bound at the head; the pre-rename skeleton of `f8ea6936` against the head's export reports `pub_idle_slope_o` missing and `pub_idle_slope_bps_o` extra, rc 1 |

## Coverage table

`python3 sw/firmware/gtest/fw_coverage.py --check --jobs 2` at the head
(gcc and gcov 16.2.1, GoogleTest 1.18.0), rc 0, `firmware coverage: PASS (22 files)`.
Lines and branches are hit/total; the ratio is after the exclusions the
ratchet reads.

| File | Lines | Branches | Lines % | Branches % |
|---|---:|---:|---:|---:|
| `sw/firmware/ctrl/acmp/acmp.c` | 763/763 | 360/360 | 100.00 | 100.00 |
| `sw/firmware/ctrl/acmp/acmp_mbx.c` | 77/77 | 26/26 | 100.00 | 100.00 |
| `sw/firmware/ctrl/acmp/acmp_nvm.c` | 38/38 | 10/10 | 100.00 | 100.00 |
| `sw/firmware/ctrl/adp/adp.c` | 204/206 | 95/102 | 100.00 | 100.00 |
| `sw/firmware/ctrl/adp/adp_mbx.c` | 83/83 | 38/40 | 100.00 | 100.00 |
| `sw/firmware/ctrl/app/ctrl_app.c` | 42/43 | 40/44 | 100.00 | 100.00 |
| `sw/firmware/ctrl/app/ctrl_app_srp.c` | 82/82 | 62/62 | 100.00 | 100.00 |
| `sw/firmware/ctrl/loop/ctrl_loop.c` | 101/101 | 62/62 | 100.00 | 100.00 |
| `sw/firmware/ctrl/maap/maap.c` | 209/209 | 140/140 | 100.00 | 100.00 |
| `sw/firmware/ctrl/maap/maap_csr.c` | 39/39 | 18/18 | 100.00 | 100.00 |
| `sw/firmware/ctrl/maap/maap_mbx.c` | 99/99 | 64/64 | 100.00 | 100.00 |
| `sw/firmware/ctrl/mbx/mbx.c` | 228/228 | 92/92 | 100.00 | 100.00 |
| `sw/firmware/ctrl/mbx/mbx_wire.h` | 15/15 | 12/12 | 100.00 | 100.00 |
| `sw/firmware/ctrl/plat/mbx_plat_mmio.c` | 10/10 | 0/0 | 100.00 | 100.00 |
| `sw/firmware/ctrl/port/ctrl_debug.c` | 19/19 | 6/6 | 100.00 | 100.00 |
| `sw/firmware/ctrl/port/ctrl_pool.c` | 99/99 | 60/60 | 100.00 | 100.00 |
| `sw/firmware/ctrl/port/shlan_port.c` | 22/22 | 6/6 | 100.00 | 100.00 |
| `sw/firmware/ctrl/srp/srp_mbx.c` | 532/532 | 486/486 | 100.00 | 100.00 |
| `sw/firmware/ctrl/wire/wire.h` | 10/10 | 2/2 | 100.00 | 100.00 |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | 198/199 | 106/110 | 100.00 | 100.00 |
| `sw/firmware/ctrl_nvm/nvm_store.c` | 434/434 | 259/266 | 100.00 | 100.00 |
| `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c` | 100/100 | 63/64 | 100.00 | 100.00 |

Every file this lane's writers touch (`acmp.c`, `acmp_mbx.c`, `maap_mbx.c`,
`mbx.c`, `srp_mbx.c`) is at 100 % of its lines and branches with no exclusion.
The host model is not in the ratchet's population.

## Gate table

`WORK` is external scratch, `PACKET` this directory. The mailbox bench runs
from a mirror of the checkout in `WORK`, so no build writes the tree. Heads:
**H** = `25bbe4d9` (the head). **P** = `9b73a8c6`, the parent of the last
commit. The last commit changes only `sw/firmware/ctrl/host/mbx_model.c`,
`mbx_model.h`, `sw/firmware/ctrl/test/srp_mbx.cpp` and `srp_mutants.py`
(`git diff --name-only 9b73a8c6 25bbe4d9`), none of which a P-row gate reads:
no RTL, Yosys, Vivado, builder, LiteX or export input, and no firmware source.

| Gate | Head | Result |
|---|---|---|
| `python3 sw/mailbox/gen_mailbox.py --check`, `--crosscheck`, `--selftest` | H | rc 0, 0 findings; self-test 0 arms failed |
| `make run-wb run-axil run-cosim run-if2` in `tb/verilator/mbx` (pinned Verilator 5.050) | H | rc 0: 401, 446, 32 and 403 / 448 / 388 checks, 0 failures |
| `python3 -B mutants.py --quick --jobs 1` (the default `make`'s arm) | H | rc 0, 6 of 6 caught |
| `python3 -B mutants.py --jobs 1` (every RTL plant) | P | rc 0, 167 of 167 caught, 4 positive controls |
| `python3 scripts/lint_rtl.py --check --self-test` | H | rc 0, 90 <= 90 |
| `python3 scripts/xvlog_gate.py --check` (Vivado 2026.1 front end) | P | rc 0, 0 findings, 81 + 52 files |
| `syn/yosys/run.sh` (every top) | P | rc 0, 58 of 58 tops, tied-input and tap-purity gates PASS; `KL_mbx` 406,331 cells |
| `python3 syn/ooc/dp_srcs.py --selftest` and the other ten OOC instrument commands of `rtl-fast`'s `yosys-elaboration` job, with `python3 scripts/pp_srcs.py --check --selftest` | P | all rc 0 |
| `behave --no-capture -f plain` in `tests/` | H | rc 0, 14 features, 404 scenarios |
| `python3 sw/firmware/gtest/tally_selftest.py` | H | rc 0, 18 of 18 |
| `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | H | rc 0 |
| `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 2 --build-dir "$WORK/fw"` | H | rc 0, 51 arms; 492 of 492 and 186 of 186 plants |
| `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 2` | H | rc 0, 5 shapes, 435 tests |
| `python3 sw/firmware/gtest/fw_coverage.py --selftest` | H | rc 0, 28 of 28 |
| `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 2` | H | rc 0, 22 files, table above |
| the docs workflow's 76 checking commands (list in `PACKET/DOCS-GATES.txt`), including `docs_check.py`, `check_em_dash.py --base 7c1b52be`, `gen_toc.py --check`, `check_doc_paths.py`, `check_hygiene.py --check`, the idiom ratchets, `measure_naming.py --check` and every listed self-test | H | 76 of 76 rc 0 |
| `python3 scripts/gen_hdl_reference.py --selftest`, then `--output "$WORK/hdlref"` (pinned parser) | P | rc 0, 44 of 44 arms |
| `python3 scripts/ci_rv32_sdk_selftest.py`; `python3 sw/builder/test_firmware_compiler.py --selftest`, then `--absent --audit "$WORK/rv32-absent.jsonl"` | P | rc 0; GATE 1b PASS |
| `python3 sw/builder/test_builder.py --require-rv32` | P | rc 0 |
| `python3 sw/builder/test_builder.py --require-elaboration --require-rv32` (the pinned LiteX environment) | P | rc 0, ALL GATES PASS EXCEPT 1 NOT RUN: gate 11 needs an unrelated local build tree |
| `scripts/run_litex_sims.sh --selftest`, then `scripts/run_litex_sims.sh "$WORK/litex-sim-logs"` (three of the five import `milan_soc.py`) | H | rc 0; self-test 10 of 10; 5 of 5 simulations |
| `make -C tb/verilator/fw_service_budget` (imports `milan_soc.py`) | H | rc 0, 52 checks |
| default-build export proof (below) | P | rc 0 under the stated normalisations |
| `--ctrl-mailbox` export and `python3 -B -I PACKET/check_mbx_ports.py` | P | rc 0, 35 of 35 ports |
| firmware size (`sw/firmware/ctrl/test/ctrl_srp_image.py`, below) | P | rc 0 |
| mailbox area (Vivado, below) | P | rc 0, 7,449 of 7,449 nets routed |
| `git diff --check 7c1b52bee26b497080ee22b1c1986109f80a5ee7 HEAD`; `git status --short` | H | rc 0; clean |

The builder, LiteX and export gates ran in a scratch clone with the pinned
submodules checked out at their gitlinks; the other gates ran in the checkout.

Not run, and why:

- `scripts/run_all_suites.sh` (the 64-suite sweep). The only suite that reads
  the changed RTL or firmware is `mbx`, run in full above. The one suite that
  imports `milan_soc.py`, `fw_service_budget`, ran on its own (above).
- `scripts/act_ci.py --pr <n>`: there is no PR. Its `--selftest` ran in the
  docs list.

## Default build (all-fabric) unchanged

The ruling requires the all-fabric image to stay byte-identical to dev. The
proof exports both AX7101 shipping configs at their shipping arguments, from
one scratch tree path into one output path, at dev `7c1b52be` and at `9b73a8c6`
(`export/run.sh` pattern; no Vivado run):

| Config | Files | Byte-identical | Date lines only | Archives, members identical | Other |
|---|---:|---:|---:|---:|---|
| `endstation_ax7101_1x1_tdm8` | 3,876 | 3,856 | 5 | 13 | `alinx_ax7101.v`, `litex.log` (below) |
| `endstation_ax7101_8x8` | 3,876 | 3,856 | 5 | 13 | `alinx_ax7101.v` date lines, `litex.log` line order |

For the 1x1 config, the generated `alinx_ax7101.v` matches in all 30,946 lines
that are neither a date line nor a line of LiteX's comment-only hierarchy
tree, in order. The tree's 826 lines are the same multiset once the last-child
glyph is folded: two siblings (`OSERDESE2`, `OBUFDS`) swapped places
(`check_tree_order.py`). The log differs in the same two lines and in the line
order that parallel make gives it. A second export of dev's 1x1 config agrees
with the first, so this order is a property of the generator run, not of any
instantiated Verilog. `docs/design/MAILBOX_SPLIT.md:898` already records that
the tree's order varies between runs.

Vivado's inputs are therefore the same apart from comments: the TCL, XDC and
init files are byte-identical. All 63 checkout files and 56 pinned-submodule
files the TCL reads are unchanged between dev and the head
(`check_tcl_reads.py`: blobs equal, three gitlinks equal). The remaining four
paths are the LiteX installation's own files, named identically in both TCLs.
The flash layout and the AEM image (`aem_desc.bin`) are byte-identical. No
bitstream was built. Summary: `PACKET/DEFAULT-BUILD.json`.

## Firmware size against 224 KB

`python3 sw/firmware/ctrl/test/ctrl_srp_image.py` (the documented recipe,
`sw/firmware/ctrl/srp/README.md:241`), at dev and at `9b73a8c6`, with the same
runtime archives (sha256 in `PACKET/FIRMWARE-SIZE.json`). It links ADP, ACMP,
MAAP, SRP, the loop and the mailbox driver with the 8,192-byte stack
reservation; AECP is not linked (F5).

| Shape, interfaces | `.text` dev / head | `.bss` dev / head | RAM span dev / head | Of 229,376 B (224 KB) |
|---|---:|---:|---:|---:|
| `endstation_ax7101_1x1_tdm8`, 1 | 45,828 / 46,576 | 23,440 / 23,696 | 80,368 / 81,376 | 35.5 % (+1,008 B) |
| `endstation_ax7101_8x8`, 2 | 47,240 / 48,156 | 64,328 / 64,592 | 122,672 / 123,856 | 54.0 % (+1,184 B) |

`.rodata` is 2,898 B on all four. The head ELFs hash as the earlier session's
did on the same sources.

## Mailbox area

The ruling asks for the mailbox area delta "through the M0s recipe as a
measurement (no re-record)". Two readings apply:

- **The M0s recipe's all-fabric selection: zero.** That image carries no
  mailbox, and its export is unchanged (above). Nothing is re-recorded.
- **Its F0-F4 and full-split selections** (PR #702, open) measure the
  integrated route. That route does not exist before PR 2 (the #640 M0s STOP,
  comment 6087021702). They were not run.

So the block's own cost is measured with the mailbox's documented
out-of-context recipe (`docs/design/MAILBOX_SPLIT.md:1073`), Vivado 2026.1,
`xc7a100tfgg484-2`, at 10 ns. It was re-run at `9b73a8c6`, after the
declaration-order and port-name commits, and reproduced the committed
figures exactly (`docs/design/MAILBOX_SPLIT.md:1051` to `:1071`):

| Block | LUT dev | LUT head | FF dev | FF head |
|---|---:|---:|---:|---:|
| `KL_mbx_rx` | 1,481 | 1,520 | 1,155 | 1,155 |
| `KL_mbx` registers, decode, read mux | 294 | 647 | 532 | 1,668 |
| `KL_mbx_evt` | 702 | 669 | 978 | 978 |
| `KL_mbx_tx` | 488 | 493 | 280 | 280 |
| `KL_mbx_wb` | 122 | 203 | 1 | 1 |
| **Total** | **3,102** | **3,548** | **2,946** | **4,082** |

+446 LUT, +1,136 FF; block RAM unchanged, no DSP; WNS +0.329 ns (+0.402 ns
on dev); 7,449 of 7,449 nets routed. Summary and report digests:
`PACKET/MAILBOX-AREA.json`.

## Choices made public

- The published stream_id is the stream the sink listens to, from the
  PROBE_TX_RESPONSE that settles it until SRP stops, as the core's
  GET_RX_STATE reports it. The processor holds the last settled stream_id
  until the unbind. PR 2's comparison sees this difference.
- `LICENCE` is the firmware's licence, which already requires admission; it
  stands for the processor's `srp_active_o AND srp_sr_admitted_o`.
- `SR_DOMAIN.ADOPTED` follows the processor's F10.2 rule: set by the first
  received Domain that differs, cleared by a link restart.
- `pub_sid_o` is raw; the consumer takes it only while `pub_sid_valid_o` is
  set. Gating each bit inside the block would cost 1,024 AND gates.
- No ADP writer (above).
- The host model gained `mbx_model_evt_pause`, used by one test, so that test
  holds its LINK record the way a full RTL ring holds one, instead of relying
  on the firmware making no mailbox write in that window.

## Open questions

- The M0s whole-image delta for the split selections waits for PR 2's route
  (above). Confirm that the zero all-fabric delta and the out-of-context
  block figure answer the ruling for PR 1.
- The size fixture does not link AECP; F5 owns that figure against 224 KB.

## Independent review coverage

| Lens | Covering round | Head |
|---|---|---|
| Conformance | none | not covered |
| RTL | none | not covered |
| Robustness | none | not covered |
| Tests | none | not covered |
| Docs | none | not covered |

## Packet

Round-1 files (the comparator evidence, `ROUND1*`, `SRP-*`, `STOP-COMMENT.md`
and the `check_*.py` drivers they name) are unchanged. Round 2 adds:

| File | What |
|---|---|
| `DEFAULT-BUILD.json` | both configs' comparisons, the TCL read checks, the dev re-export, the generated Verilog digests |
| `FIRMWARE-SIZE.json` | the four size measurements and the runtime digests |
| `MAILBOX-AREA.json` | the hierarchical utilisation rows, WNS and report digests |
| `DOCS-GATES.txt` | the 76 docs-workflow commands run at the head |
| `compare_same.py`, `check_tree_order.py`, `check_tcl_reads.py` | the export comparison and its two follow-up checks |
| `check_mbx_ports.py` | the `--ctrl-mailbox` instance's port check |
| `REVIEW-READY-COMMENT.md` | the text of #665 comment 6091286964 |
| `PACKET-SHA256.json` | size and sha256 of every other file here |
