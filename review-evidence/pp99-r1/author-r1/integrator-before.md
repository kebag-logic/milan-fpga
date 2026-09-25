<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# Integrator guide — dropping this processor into an SoC

You have a fabric with a MAC, a memory system and probably a soft CPU, and you want a
Milan control plane in it. This page is the contract:
[`hdl/top/protocol_processor_top.sv`](../../hdl/top/protocol_processor_top.sv) is the one
instantiation boundary, and everything below describes it.

**Read the picture first:**
**[`../diagrams/21-integration-faces.svg`](../diagrams/21-integration-faces.svg)** is the
whole contract on one page, including what happens when you do not connect something.
For what is inside the box, see
[`../diagrams/20-rtl-dataflow.svg`](../diagrams/20-rtl-dataflow.svg).

> The port names and defaults on this page are transcribed from the RTL. Where the
> architecture documents describe an older interface, the RTL is authoritative and the
> divergence is listed in the
> [HDL engineer guide](hdl-engineer.md#9-where-the-specification-and-the-tree-still-disagree).

---

## 1. Clocking and reset

There is exactly one clock and one reset.

| Port | Contract |
|---|---|
| `clk_i` | the single core clock. `CLK_HZ_P` tells the timer prescaler what it is. |
| `rst_n` | **synchronous**, active low. It needs a running clock to take effect. |

**No clock-domain crossing lives inside this processor.** Every crossing is yours:

- the MAC boundaries — put your asynchronous FIFOs outside, and present the byte streams
  below in the `clk_i` domain;
- `link_up_i` and `gm_change_i` — level and strobe inputs from other domains. Give them a
  two-flop synchroniser before they arrive;
- the class-D status outputs are combinational reads of `clk_i`-domain registers. A
  consumer in another domain owns its own synchroniser.

[`KL_pp_side_port`](../../hdl/packet_engine/KL_pp_side_port.sv) is documented as being
able to run from a bridged management clock; the top instantiates it on `clk_i`.

---

## 2. Parameters — the shape is fixed when you build the bitstream

Nothing here is writable at runtime, and that is deliberate.

| Parameter | Default | What it sets |
|---|---|---|
| `N_STREAM_IN_P` | 8 | Stream Inputs — sinks, listener machines, per-sink records |
| `N_STREAM_OUT_P` | 8 | Stream Outputs — sources, talker gates, SRP declarations |
| `RX_SLOTS_P` × `RX_SLOT_BYTES_P` | 4 × 576 | the RX payload pool |
| `TX_STD_SLOTS_P` | 4 | standard TX slots (a fifth oversize slot always exists) |
| `TX_OVERSIZE_BYTES_P` | 1600 | the oversize TX slot, for the responses Milan lets exceed the normal cap |
| `CLK_HZ_P` | 100 MHz | the timer prescaler base |
| `TIM_DIV_US_P` / `TIM_DIV_MS_P` | derived / 1000 | prescaler overrides. **Simulation only** — they exist so a testbench can compress time. |
| `TROM_HEX_P` | `ltn_rom.hex` | the ACMP listener transition-ROM image |
| `UCODE_HEX_P` | `ucode.hex` | the AECP µcode ROM image |
| `DESC_BASE_P` | 0x20000000 | where the descriptor image lives in **your** memory |
| `DESC_LINE_BYTES_P` | 576 | the on-chip line buffer for one located descriptor |
| `DESC_IDX_ENTRIES_P` | 32 | cached index-map entries |
| `DESC_NAME_ENTRIES_P` | 32 | name-table entries held on chip; set it from the generated image's `n_names`, up to 1024 |
| `DESC_MEM_TMO_CYC_P` | 4096 | no-progress watchdog on the descriptor memory face, in clocks |
| `RESP_BASE_P` | 0x20100000 | where the AECP response buffer lives in **your** memory |
| `SRP_DOM_DEF_VID_P` | 2 | the Class A Domain VID the SRP engine declares at start-up and on every link-up, and returns to on link-down (Milan §4.2.7.2.1). A bridge's differing Class A Domain is still adopted at run time. **Keep it at 2 in a product build**: Milan fixes the value, and any other one exists only to prove this binding in verification. |

Three traps worth stating plainly:

1. **The ROM parameters are file paths, and a relative name resolves against the tool's
   run directory** — not against the source file. That is the entire reason they are
   parameters. Hand over absolute paths.
2. **An over-large stream shape stops the build.** The top carries elaboration guards
   over the timer-slot map and the owner-tag space; exceeding either raises `$error`
   rather than silently aliasing a timer slot. A too-large shape is a build failure, not
   a field fault.
3. **A one-stream shape is supported.** Index widths are clamped so a shape of one does
   not declare a negative-width vector.

Parameter identities and ranges are owned by
[`01_overview.md` §7](../architecture/01_overview.md#7-parameter-master-table-f015).

---

## 3. The MAC faces

One frame stream in, one frame stream out, both **byte-wide**, both in the `clk_i`
domain. Byte 0 of each frame is the first destination-address octet.

| Direction | Ports | Backpressure |
|---|---|---|
| RX | `rx_valid_i`, `rx_data_i[7:0]`, `rx_last_i` | **none.** There is no `rx_ready`. The RX side cannot be stalled — feed it from a FIFO that can absorb a frame. |
| TX | `tx_valid_o`, `tx_sof_o`, `tx_data_o[7:0]`, `tx_eof_o`, `tx_ready_i` | `tx_ready_i` is real. A granted frame streams from `tx_sof_o` to `tx_eof_o` with no preemption, so holding `tx_ready_i` low stalls that frame in place; it never truncates. |

This is a control-plane trunk. It sees the frames a Milan control plane needs — the
ATDECC multicast and this station's own unicast, plus the two MRP group addresses — and
it emits control frames only. Streaming data never passes through here.

---

## 4. The two main-memory masters

The entity model and the AECP response buffer do **not** live on chip. This is the single
most important thing to plan for. On the reference part the generated entity model was
already tens of kilobytes and the die's block RAM was effectively fully spoken for, and
the response buffer as fabric state was the flop group the placer could not pack.

Both masters are **vendor-neutral by contract** — this repository does not know what is
behind them. You bridge them to whatever you have.

### 4.1 `desc_mem_*` — read only

| Port | |
|---|---|
| out | `desc_mem_req_valid_o`, `desc_mem_req_addr_o[31:0]`, `desc_mem_req_beats_o[8:0]`, `desc_mem_rsp_ready_o` |
| in | `desc_mem_req_ready_i`, `desc_mem_rsp_valid_i`, `desc_mem_rsp_data_i[63:0]`, `desc_mem_rsp_last_i`, `desc_mem_rsp_err_i` |

One outstanding request. Responses arrive **in order**; `rsp_last` marks the final beat.
Addresses are byte addresses, 8-byte aligned. A beat carries its lowest byte address in
bits [63:56] — IEEE 1722.1 wire order, so a descriptor byte can be handed to the µCPU
unswapped.

### 4.2 `resp_mem_*` — read and write

| Port | |
|---|---|
| out | `resp_mem_req_valid_o`, `resp_mem_req_addr_o[31:0]`, `resp_mem_req_beats_o[8:0]`, `resp_mem_rsp_ready_o`, `resp_mem_wr_valid_o`, `resp_mem_wr_addr_o[31:0]`, `resp_mem_wr_data_o[63:0]`, `resp_mem_wr_strb_o[7:0]` |
| in | `resp_mem_req_ready_i`, `resp_mem_rsp_valid_i`, `resp_mem_rsp_data_i[63:0]`, `resp_mem_rsp_last_i`, `resp_mem_rsp_err_i`, `resp_mem_wr_ready_i`, `resp_mem_wr_done_i`, `resp_mem_wr_err_i` |

Same read contract, with **one difference that matters**: here `resp_mem_rsp_ready_o` is
real backpressure. The buffer takes a beat only once the frame builder has consumed the
previous one, so your bridge shall hold a beat until it is taken.

The write channel is one outstanding single-beat write. `wr_data` is a 64-bit lane in the
same big-endian order as a read beat — byte `addr + n` is bits `[63-8n -: 8]`. `wr_strb`
bit *n* enables byte *n*, and a byte whose strobe is 0 **shall not be modified**.
`wr_done_i` is a one-cycle pulse when the write is committed; it may be the same cycle as
`wr_ready_i` for a posted bridge, or later for an acknowledged one. No further write is
issued until it arrives.

Ordering: a read request accepted after a write reported done shall observe that write.
Nothing else in this processor addresses the region, so no further rule is needed.

### 4.3 Why two masters and not one

Both are watchdog-bounded clients with one outstanding transaction each. Sharing a single
channel would mean an arbiter whose grant has to be released correctly on every watchdog
of both. Your memory system already arbitrates — let it.

---

## 5. What you must reserve in your memory map

| Region | Size | Who writes it |
|---|---|---|
| `DESC_BASE_P` | your descriptor image, sized by your entity model | **your software**, before `entity_enable_i`. The processor only reads it. |
| `RESP_BASE_P` | `16 + DESC_LINE_BYTES_P` bytes | **the processor.** Nothing else may write here. |

Both are 8-byte aligned, and `RESP_BASE_P` must not overlap `DESC_BASE_P`.

The image opens with a magic, a layout version and a checksum. Until all three agree,
the store reports zero configurations. `READ_DESCRIPTOR` validates the requested
configuration before it locates a descriptor, so every request against an invalid or
unloaded image answers `BAD_ARGUMENTS`, never a garbage descriptor on the wire.
Uninitialised memory is not a recognisable zero, which is exactly why the header check
exists. A **late** load heals it: the next locate re-arms the header probe, so software
that loads the image after reset does not need a reset to recover.

Layout of the image itself, and its generator, are in
[`07_memory_maps.md` §3](../architecture/07_memory_maps.md).

The whole path, with its failure modes, is
[`../diagrams/22-aecp-descriptor-fetch.svg`](../diagrams/22-aecp-descriptor-fetch.svg).

---

## 6. Configuration and identity inputs

The identity, capability, SRP and talker-source groups are quasi-static: set
them before `entity_enable_i` and leave them alone. The two dynamic rows are
updated at runtime under the event contracts below.

| Group | Ports |
|---|---|
| Identity and model | `entity_id_i[63:0]`, `entity_model_id_i[63:0]`, `own_mac_i[47:0]`, `current_cfg_i[15:0]`, `identify_index_i[15:0]` |
| Advertised capability | `talker_sources_i[15:0]`, `talker_caps_i[15:0]`, `listener_sinks_i[15:0]`, `listener_caps_i[15:0]` |
| Dynamic gPTP state | `gm_change_i`, `gm_id_i[63:0]`, `gptp_domain_i[7:0]` |
| Level controls | `entity_enable_i`, `link_up_i` |
| SRP | `p2p_i`, `cfg_rank_i`, `cfg_acc_lat_ns_i[31:0]`, `port_rate_bps_i[31:0]`, `cfg_tspec_max_frame_i[15:0]` |
| Talker sources | `cfg_src_en_i`, `cfg_src_iface_i`, `cfg_stream_id_i` |

The three per-source vectors are **flat packed bit vectors**: index *s* occupies
`[W*s +: W]`. The same convention is used by every per-index status output.

`entity_enable_i` is the boot gate of Milan §5.6.1. While it is low the advertise machine
is held in DOWN and the entity is silent — because an entity must already be able to
answer commands before it announces itself. Deasserting it later **is** the shutdown: it
emits ENTITY_DEPARTING and resets `available_index`. There is no separate shutdown port.

`gm_change_i` is a one-cycle **ADP / GET_AVB_INFO** event, not a
`GET_AS_PATH` event. Raise it after atomically publishing a changed `gm_id_i`
or `gptp_domain_i`; both fields are advertised and both are returned by
`GET_AVB_INFO`. The path has its own publication edge, `gsi_asp_chg_i`. Raise
that strobe after atomically publishing any changed PathTrace sequence,
including entry 0 when a new grandmaster identity changes it. Consequently a
GM identity update normally raises both strobes, a domain-only update raises
only `gm_change_i`, and a tail-only PathTrace update raises only
`gsi_asp_chg_i`. The processor keeps the two events separate so a domain
change cannot claim that the path changed.

---

## 7. The optional faces, and what a tie-off does

Every one of these is watchdog-bounded. Leaving one unconnected degrades that function to
an honest answer on the wire; **it never wedges the control plane.** That is a design
property, not an accident, and it is regression-tested. It covers the faces, not the boot
controls: `restore_go_i` is not part of the NVM tie-off, and a boot that never pulses it
leaves the ACMP listener held until the next reset
([05 §5.1](../architecture/05_acmp_engine.md#sec-05-boot-admission)).

| Face | Ports | Tie it off and… |
|---|---|---|
| MAAP allocation | `maap_req_valid_o`, `maap_req_release_o`, `maap_req_src_o`, `maap_conflict_ack_o` / `maap_req_ready_i`, `maap_rsp_valid_i`, `maap_rsp_ok_i`, `maap_rsp_da_i[47:0]`, `maap_conflict_valid_i`, `maap_conflict_src_i` | **no source ever declares.** `acmp_declaring_o` is structurally 0 and PROBE_TX answers `TALKER_DEST_MAC_FAILED`. Commands are still answered normally. |
| Descriptor memory | `desc_mem_*` | the failed header probe leaves zero configurations, so every `READ_DESCRIPTOR` answers `BAD_ARGUMENTS` after the watchdog. |
| Response memory | `resp_mem_*` | every built response becomes a well-formed 60-byte `ENTITY_MISBEHAVING`. |
| NVM device | `nvm_dev_*`, plus `restore_go_i`, `restore_busy_o`, `restore_done_o`, `restore_fail_o`, `restore_blank_o`, `nvm_alarm_o`, `nvm_unflushed_o` | bindings do not survive a power cycle. **`restore_go_i` is not part of the tie-off:** pulse it on every boot. The ACMP listener serves nothing until the walk has ended ([05 §5.1](../architecture/05_acmp_engine.md#sec-05-boot-admission)), and what the walk reports depends on how you tie the face off. Tie it off **as erased media**: grant each READ, deliver the bytes it asks for as `0xFF`, then `done`. The walk then ends with `restore_done_o`, no `restore_fail_o` and `restore_blank_o`, the same done-without-fail as a successful walk, so publish `restore_blank_o` beside them and report not-successful when you know there is no media. A face that answers with `err`, or with `done` before the eight header bytes, is a failing device: the walk fails whole (`restore_fail_o`, a device error). A face that never answers fails the walk at `NVM_RS_TMO_CYC_P` (`restore_fail_o`, the deadline) and leaves the port quarantined until reset ([07 §5.3](../architecture/07_memory_maps.md#fig-07-nvmflow)). Nothing else changes **in this plane**. |
| Management side port | `host_*` | you lose all diagnostics. The plane still runs. |
| SRP service | `svc_*` | nothing declares through the configuration plane. |
| AECP pop face | `aecp_txn_*`, `aecp_rxs_*` | **tie `aecp_txn_ready_i` low.** The internal AECP engine already drains this queue; this face is an *additional* observer. Driving it steals records from the engine. |

**MAAP is yours to place.** With `cfg_maap_internal_i` tied 0 (the default), the
processor disables its internal allocator and selects the external allocation seam.
Address allocation then stays in the integrating fabric, which must provide the
claim/defend/announce machine from IEEE 1722-2016 Annex B. Tie
`cfg_maap_internal_i` to 1 (quasi-static, set before `entity_enable_i`)
and the in-scope `KL_pp_maap` engine
([11](../architecture/11_maap_engine.md)) provides it instead: give it
`cfg_maap_count_i` (block size; `N_STREAM_OUT_P` covers one DA per source) and
optionally a persistence seed (`cfg_maap_seed_offset_i` + `cfg_maap_seed_valid_i`),
gate talker egress on `maap_addr_valid_o`, read source s's DA as `maap_addr_o + s`
(`maap_state_o`/`maap_conflicts_o`/`maap_defends_o` are the observability trio), leave
the whole external `maap_*` port group unconnected — it is quiesced — and retire your
allocator.

---

## 8. The class-D status wires — read them every clock

These are the reason the processor is worth integrating rather than polling. They are
combinational reads of `clk_i` registers, published continuously, so your datapath can
gate on them per cycle.

| Output | Use |
|---|---|
| `acmp_declaring_o` | **the talker egress gate.** AND it with your own stream enable. |
| `acmp_bound_o` | per-sink binding installed, **debounced** — safe to edge-detect. The raw internal register dips low and high again inside a single rebind transaction; this port does not. |
| `acmp_bound_eid_o`, `acmp_bound_sid_o`, `acmp_bound_dmac_o`, `acmp_bound_vlan_o` | the bound stream's identity on the wire: who the talker is, which stream, on what address and VLAN. Arm your RX filter and stream table from these — you cannot derive them from the entity id. |
| `srp_active_o` | **the AVTP transmit gate.** Declaring, not failed, a listener is ready, and admitted. Use this one. |
| `srp_sr_admitted_o` | the raw Σ-slope verdict. It **lags** `srp_active_o` by up to three admission rounds after a fresh declare, because admission is optimistic. Gating on this instead mutes a legal stream for those rounds. |
| `srp_granted_slope_bps_o`, `srp_sum_slope_bps_o` | per-source and summed granted idleSlope — the value your credit-based shaper's slope multiplexer needs. |
| `srp_over_limit_o` | at least one source was refused against the port ceiling. |
| `srp_class_a_prio_o`, `srp_class_a_vid_o`, `srp_domain_adopted_o`, `srp_domain_change_o` | the Class A identity in force. The two values are defaults until `srp_domain_adopted_o` says a bridge Domain was adopted. The VID default is `SRP_DOM_DEF_VID_P`, and a link-down restores both defaults. |
| `srp_tk_decl_state_o`, `srp_lstn_reg_state_o`, `srp_tk_reg_state_o`, `srp_lstn_decl_state_o` | the four declaration/registration state vectors, two bits per index. Read each one against its port comment, never against a listed order: `srp_lstn_reg_state_o` carries `srp_pkg::srp_decl_e` (1 Asking Failed, 2 Ready, 3 Ready Failed, [02 F02.10](../architecture/02_interfaces.md#fig-02-statusdict)), so "a Listener is registered" is any non-zero code and "Ready or Ready Failed" is bit 1 |
| `srp_acc_latency_o` | per-sink registered accumulated latency in nanoseconds, **raw** — add your own ingress delay |
| `srp_src_fail_code_o`, `srp_src_fail_bridge_o`, `srp_snk_fail_code_o` | failure codes, valid only while the matching state vector says FAILED |
| `adp_next_avail_index_o` | 32 bits, deliberately. Truncating it would make a controller see `available_index` step backwards, which is exactly the signal it uses to decide an entity restarted. |
| `nvm_unflushed_o` | per-sink binding state the manager has accepted and not yet committed. 1 from the accepted change until its record commits with `done`, or until the retries are exhausted and `nvm_alarm_o` rises on the same cycle. OR it with `aecp_dyn_dirty_o` for a "saved state pending" bit; without it a binding taken inside the commit debounce reads durable. |
| `aecp_nvm_stb_o`, `aecp_nvm_mark_o` | one cycle per committed command that marked a record group, and the group: 1 a dynamic-state field, 6 channel maps, 7 user names. Nothing in the processor writes a record for 6 or 7, so this strobe is the only notice that those live values moved. |
| `dbg_now_ms_o` | the free-running millisecond timebase |

The status dictionary these implement is catalogued in
[`02_interfaces.md` F02.10](../architecture/02_interfaces.md#fig-02-statusdict).

---

## 9. Bring-up order

1. Load the descriptor image into your memory at `DESC_BASE_P`.
2. Release `rst_n` with `clk_i` running.
3. Pulse `restore_go_i` to restore persisted bindings from NVM, **on every boot**; wait
   for `restore_done_o`, then read `restore_fail_o` **and** `restore_blank_o`.
   `restore_done_o` says the walk sequenced, not that anything came back: every
   per-record vendor default sets it. `restore_blank_o` is the pin that separates
   a restore from a walk over blank, unframed or absent media. The walk is not
   optional: from reset until `restore_done_o` the ACMP listener's work is held at
   its producers, so a boot that never starts the walk never answers an ACMP
   listener command. `restore_done_o` rises once the last restored binding has been
   written and its discovery armed, a few cycles after the walk's own terminal, with
   `restore_busy_o` high in between; gate the entity enable on it. The walk always
   reaches that terminal: `restore_fail_o` beside it says it failed whole (a torn
   read-back, a device error, or a device silent for `NVM_RS_TMO_CYC_P` clocks) and
   every binding starts at its vendor default. The saved records stay on the media:
   only a later BIND replaces one, so the next boot on a healthy device restores them
   ([07 §5.3](../architecture/07_memory_maps.md#fig-07-nvmflow)). Size `NVM_RS_TMO_CYC_P` (default
   20 ms of `CLK_HZ_P`) above the slowest single record read your device face can
   take.
4. Present identity, capability and configuration inputs.
5. Assert `entity_enable_i`. Only now may the entity advertise.

If it does not come up, hand the board to the [operator guide](operator.md) — its
[bring-up ladder](../diagrams/23-bringup-decision.svg) is written for exactly this moment.

---

## 10. Consuming this repository

The reference platform includes this repository as a **git submodule** and instantiates
the top from here. The HDL is authored here and only consumed there — never copied. The
pin is moved only to a commit where the documentation gates, the lint gate and the full
suite sweep are green. Interface stability at `hdl/top/` follows
[`02_interfaces.md`](../architecture/02_interfaces.md): a breaking port change is a
documented interface change *before* it is an RTL change.

Details of that contract are in [`../../hdl/README.md`](../../hdl/README.md).
