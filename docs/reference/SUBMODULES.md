# Submodule integration map

Gitlinks define accepted revisions.

Detached submodule heads are normal.

Dirty submodules invalidate local evidence.

![Verified submodule boundaries](../diagrams/submodule_boundaries.svg)

## Contents

- **[Pinned dependencies](#pinned-dependencies)** -- Identify every imported repository.
- **[Initialize safely](#initialize-safely)** -- Populate exact recorded revisions.
- **[Respect ownership](#respect-ownership)** -- Separate donor and root responsibilities.
- **[Known documentation conflicts](#known-documentation-conflicts)** -- Avoid stale donor claims.

## Pinned dependencies

<!-- submodule-pins:start -->
| Path | Pin | Purpose | Root integration |
|---|---|---|---|
| `external` | `efeb541ae5fe1e078332d8462dca2fc2d9cb8db5` | Historical Ethernet MAC RTL | No active product consumer |
| `gptp-processor` | `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` | Fabric gPTP engine | `KL_gptp_shadow.sv` |
| `protocol-processor` | `ead8036035affd53ef4b29979190f2f4f67084c0` | ADP, ACMP, AECP, and SRP | `KL_pp_shadow.sv` |
| `third_party/lwSRP` | `9197193e47a6bb1c45a56d90a18c1784123aba44` | Bare-metal MRP, MSRP and MVRP | `sw/firmware/ctrl/srp/srp_mbx.c` |
| `third_party/verilog-axis` | `48ff7a7e2ef782cf778d47910cf85835c64b1bce` | AXI-Stream primitives | Multiple RTL consumers |
<!-- submodule-pins:end -->

Issue #508 adopted these processor changes.

| Processor issues | Merged PR | Adopted behavior |
|---|---|---|
| [92](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/92), [93](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/93) | [109](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/109) | Saved-binding restore, bounded walk, listener boot hold |
| [94](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/94) | [110](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/110) | Descriptor-memory guard; no external port change |
| [43](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/43), [49](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/49) | [111](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/111) | Processor-owned input probing, ACMP status and failure fields |
| [112](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/112) | [114](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/114) | Admission grants wait for the current declaration's evaluation |
| [116](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/116) | [117](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/117) | Parent-gate fixes; no behavior or external port change |
| [113](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/113) | [115](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/115) | Latency-only GET_STREAM_INFO notification; no external port change |

PR 117 merged as `265d6762`.

PR 115 then merged as `990f9652`.

Issue #567 adopted processor pin `0922e434`.

| Merged processor PR | Adopted change |
|---|---|
| [118](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/118) | October MVU waiver and unsupported-command response tests |
| [119](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/119) | Complete integration parameter inventory and its checker |

That adoption left processor HDL and ROM generators unchanged.

The repository tool recorded ROM digest rows for `0922e434`.

Their digests match the `990f9652` rows.

Issue #502 adopted processor pin `870ff88a`.

- PR 121 exports each accepted live name write.
- `KL_pp_shadow` connects that pulse to saved-state pending.
- The parent's actual-write enable supplies the map trigger.
- Later marks retain their command-completion meaning.

Issue #580 adopted processor pin `16be6768`.

- [Processor PR 124](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/124) rejects body/key type and index mismatches.
- [Processor PR 126](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/126) documents descriptor ownership.
- [Processor #122](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/122#issuecomment-5853884588) retains Milan 5.3.3.8's cluster minimum.
- The zero-cluster 8x8 input pools violate that minimum.
- Parent [#584](https://github.com/kebag-logic/milan-fpga/issues/584) owns the D8 product correction.
- All five configurations retain identical AEM images and builder outputs.

Issues #606 and #608 adopted processor pin `c951a9ff`.

- [Processor PR 129](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/129) retries refused destination allocation every 100 ms.
- Every enabled source acquires independently of its first probe.
- [Processor PR 130](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/130) defers own LeaveAll aging until transmit acceptance.
- Listener withdrawal before that action still clears IN.
- Existing LV withdrawal semantics remain unchanged.
- Parent regressions exercise MAAP acquisition and CRF STREAM_STOP.
- Bench re-measurement follows on the next image.

Issue #70 lane 2 adopted processor pin `b2db3a97`.

- [Processor PR 132](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/132) adds the scalar-record D3 writer (`d352bbaa`).
- It holds AECP until the D3 restore's terminal.
- `KL_pp_shadow` connects the combined restore status and the D3 pending.
- [Processor PR 133](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/133) restarts the leavealltimer on a received LeaveAll.
- Its talker licence waits for the stream VID's MVRP join.
- It changes no port or parameter of the processor top.
- The ROM generators' outputs match the `c951a9ff` rows.

Issue #635 adopts processor pin `631eeb34`.

| Processor lane | Merged PR | `main` after merge |
|---|---|---|
| C3, ADP | [136](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/136) | `0451d83d` |
| C2, MAAP | [135](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/135) | `d5f73bac` |
| C4, ACMP | [137](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/137) | `3f3ea56b` |
| C5b, AECP dispatch and responses | [138](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/138) | `16ea10ac` |
| C5a, AECP deadlines and hazards | [140](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/140) | `03c842a7` |
| C6, notifications and Identify | [139](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/139) | `2ebd4fe8` |
| P141, clock sources for #629 | [142](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/142) | `631eeb34` |

- `ltn_rom.hex` matches the `b2db3a97` row.
- The `ucode.hex` digest changes.

The parent can observe these processor changes.

| Processor change | Parent position |
|---|---|
| C6 adds input `identify_button_i` and parameter `EN_IDENTIFY_NOTIF_P`, default 0 | `KL_pp_shadow` ties both to 0 until a board button exists |
| C6 draws that input in processor diagram 21 | The parent keeps no copy of that diagram |
| C5a answers an AECP command still running 100 ms after reception | No top port or parameter; its kill ports stay inside the processor, and the three scoreboard kill tie-offs left the processor top |
| C5a answers a non-AEM command whose response memory fails NOT_IMPLEMENTED, with the command echoed ([processor PR 140](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/140); Milan v1.2 Section 5.4.3.3, Table 5.19) | No top port or parameter; GET_MILAN_INFO is such a command, and at `b2db3a97` the same fault answered ENTITY_MISBEHAVING |
| C5a serializes AECP and ACMP work by hazard class | No top port or parameter |
| C5b accepts `DESC_LINE_BYTES_P` from 576 to 1008, in steps of 8 | The parent binds 576, the floor |
| C3 carries a SET_CONFIGURATION index in the ADPDU | The parent image declares one configuration; the wire is unchanged while `ADP_IDX0` is 0 |
| C2 fixes the internal MAAP engine | The parent ties `cfg_maap_internal_i` to 0, so it stays inactive |
| P141 grades SET/GET_CLOCK_SOURCE over ten sources | [Media-clock following](../design/MEDIA_CLOCK_FOLLOWING.md#protocol-processor-changes) records it as landed |

Issue #661 adopts processor pin `ead80360`.

| Processor lane | Merged PR | `main` after merge |
|---|---|---|
| C8, descriptor model lint | [144](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/144) | `88969246` |
| #143, campaign jobs | [146](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/146) | `c74711d4` |
| P2, NVM port deadline | [145](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/145) | `ddb3119d` |
| C7, counters face | [147](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/147) | `f4167536` |
| P1, persistence beyond BINDING | [150](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/150) | `c4cb84ff` |
| C10, Yosys tops and declarations | [149](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/149) | `5c71928a` |
| #85, ADP matrix walk | [152](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/152) | `83999eba` |
| #232, notification registry RAM | [153](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/153) | `c050d971` |
| #230, SRP area | [154](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/154) | `07b1469d` |
| #81 and #84, scoreboard faces | [157](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/157) | `b0a74196` |
| #639, arm queues and listener records | [155](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/155) | `ead80360` |

- `ltn_rom.hex` and `ucode.hex` match the `631eeb34` rows.
- The top gains one parameter and no port.

The parent can observe these processor changes.

| Processor change | Parent position |
|---|---|
| P2 adds parameter `NVM_MEM_TMO_CYC_P`, default `CLK_HZ_P` (1,000 ms) | `KL_pp_shadow` keeps the default |
| P2 answers a silent NVM device at that deadline: err, cause DEADLINE | Three failed attempts raise `nvm_alarm`; the [D3 contract](../design/SAVED_STATE_MATERIALIZATION.md) is amended (W13, section 8.8, section 15 item 4) |
| P1 adds the name stage; the channel maps are the parent's ([processor #83 ruling](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/83#issuecomment-5967611704)) | The D3 contract is amended; the map writer, restore and roll-back are #637's |
| P1 keeps `pend_i`'s sticky live-name term | A parent lane transfers names to `d3_unflushed_o` |
| C8 lints the descriptor model inside `build()` by default | Both image emitters run it; the 8x8 configuration carries its #584 waiver; the parent's duplicate L6/L10 checker is retired |
| C10 names six modules as Yosys tops and declares before use | `processor_yosys_tops.budget` is empty and the xvlog ratchet banks the fix |
| #232 drops the `pd_ix_w` use-before-declaration | The xvlog ratchet banks it |
| #85 resets `available_index` to 0 after ENTITY_DEPARTING (IEEE 1722.1-2021 Section 6.2.2.15) | The [register map](REGISTER_MAP.md) `0x644` note says so |
| #157 serializes GET_DYNAMIC_INFO against an in-flight ACMP stream step | No top port or parameter |
| #230, #232 and #639 move storage into distributed RAM | No top port or parameter; the [resource gate](../design/AREA_BUDGET.md#the-resource-gate) is re-baselined |
| C7 documents the integrator-owned `ctr_*` counters face | `milan_datapath` already meets it |
| #143 adds `--jobs` to the processor's mutation campaigns | No parent change |

The ROM ledger records current and earlier pins.

The boundary diagram follows the current pin.

OOC synthesis requires ledger rows for the pin of record.
Rows must match that exact pin.

The parent wrapper's parameter bindings match the documented inventory.

Run the inventory checker from the parent checkout:

```sh
python3 protocol-processor/scripts/check-integrator-params.py
```

The [datapath suite](../../tb/verilator/milan_dp/README.md#the-508-get_stream_info-seam-the-gsi-section-of-obj_notify) records notification coverage.

`traffic_queues.sv` is one representative consumer.

Other consumers exist throughout root RTL.

The pin checker reads Git index entries.

It does not trust checked-out heads.

## Initialize safely

Firmware and root gates use these four submodules.

```sh
git submodule update --init \
  third_party/verilog-axis \
  protocol-processor \
  gptp-processor \
  third_party/lwSRP
```

lwSRP uses the HTTPS URL recorded in `.gitmodules`.
The repository is public; anonymous HTTPS fetch needs no credentials.

The pin is published on `main`.
It includes PR #12 and PR #15.

The [SRP adapter](../../sw/firmware/ctrl/srp/README.md) documents compilation and ownership.

lwSRP is licensed under Apache-2.0.
Its pinned `LICENSE` and `NOTICE` retain dependency terms.

The unused external import uses SSH.

Initialize it only when needed.

```sh
git submodule update --init external
```

Compare every populated checkout revision.

```sh
git submodule status --recursive
```

- A leading space confirms the recorded revision.
- A leading dash means uninitialized content.
- A leading plus means revision mismatch.
- A leading `U` means unresolved content.

Revision agreement does not prove cleanliness.

```sh
git submodule foreach --quiet --recursive 'git status --short'
```

The cleanliness command must print nothing.

## Respect ownership

- Change donor behavior inside its repository.
- Land donor tests before changing pins.
- Move pins only after donor evidence.
- Run root integration after every pin.
- Root tests never replace donor suites.
- Root wrappers own adaptation logic.
- Root documentation owns integration behavior.

| Repository | Donor gate | Root gate |
|---|---|---|
| `protocol-processor` | `protocol-processor/scripts/run_suites.sh` | `make -C tb/verilator/pp_shadow` |
| `gptp-processor` | `make -C gptp-processor` | `make -C tb/verilator/gptp_shadow` |
| `third_party/verilog-axis` | Upstream evidence | `make -C tb/verilator/queues` |
| `third_party/lwSRP` | cgreen and behave | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` |
| `external` | Upstream evidence | Not applicable; no active product consumer |

## Known documentation conflicts

The reviewed gPTP guides match root ownership.

The pinned engine exports `phc_slew_active_o` for policy correction.

The parent carries it to the CRF servo (#545).

Window overlap preserves lock until measured correction completes.

- [Manager guide](https://github.com/Mister-M-alt/FPGA-gPTP/blob/5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d/docs/MANAGER.md)
- [Integration guide](https://github.com/Mister-M-alt/FPGA-gPTP/blob/5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d/docs/INTEGRATION.md)
- [HDL guide](https://github.com/Mister-M-alt/FPGA-gPTP/blob/5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d/docs/HDL_DEVELOPER.md)
- [Test guide](https://github.com/Mister-M-alt/FPGA-gPTP/blob/5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d/docs/TEST_DEVELOPER.md)

Protocol donor prose retains these known contradictions.

Use root RTL for integration truth.

Imported prose never defines root runtime behavior.

| Conflict | Implementation evidence |
|---|---|
| Protocol interface guide shows word-wide RX | Landed processor receives bytes |
| Protocol interface guide shows RX backpressure | Landed processor has no RX ready |

Track donor repairs separately.

Historical audit exceptions remain open disclosures.
PR13/PR6 branch continuity is UNKNOWN.

PR13/PR9 retain the negative-merge baseline.
Parent integration does not clear these donor audit findings.
