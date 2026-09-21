<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# Saved-state materialization: who writes the non-binding records, and how they come back

> **Status: PROPOSED.** This page is the design phase of issue #500, under
> issue #70. It decides scope D3 of the
> [snapshot-ownership page](SAVED_STATE_SNAPSHOT_OWNERSHIP.md), its
> UNRESOLVED 1: who materializes the configuration index, the sampling rate,
> the clock source, the stream formats in and out, the presentation time
> offset, the channel maps and the user names into NVM records, and how they
> come back at boot. Nothing on this page is implemented. Two independent
> contract reviews accept or reject it; an implementation lane opens only on
> an accepted page, with the tickets of section 10.

Source examined: dev `07294a76` (protocol-processor `424c688f`,
gptp-processor `c1b61743`, third_party/verilog-axis `48ff7a7e`), which is
VERSION `0x0002_0060`. Where this page says the current source, it means that
commit. A claim marked EXECUTED comes from the run script at that source,
graded in its results files; a claim marked DERIVED does not. Case and check
names are the ones the run script grades.

The executable evidence is kept out of this tree, on a branch that is never
merged. Every evidence citation on this page names the branch, the commit and
a path in it:

- the command record, with every command, exit code and digest:
  `branch 500-design-evidence, commit a21b165ac1c671d10cba7255beaf75cea0f81d18, path design-evidence/500-materialization/COMMAND_RESULTS.md`;
- how to re-run it:
  `branch 500-design-evidence, commit a21b165ac1c671d10cba7255beaf75cea0f81d18, path design-evidence/500-materialization/proposal-evidence/README.md`;
- the run script:
  `branch 500-design-evidence, commit a21b165ac1c671d10cba7255beaf75cea0f81d18, path design-evidence/500-materialization/proposal-evidence/run.py`;
- its graded results:
  `branch 500-design-evidence, commit a21b165ac1c671d10cba7255beaf75cea0f81d18, path design-evidence/500-materialization/proposal-evidence/results.txt`
  and `results.json` beside it;
- the prototype writer and arbiter:
  `branch 500-design-evidence, commit a21b165ac1c671d10cba7255beaf75cea0f81d18, path design-evidence/500-materialization/proposal-evidence/prototype/`;
- the area rows and the two cost proxies:
  `branch 500-design-evidence, commit a21b165ac1c671d10cba7255beaf75cea0f81d18, path design-evidence/500-materialization/proposal-evidence/ooc/`.

A section number that is a link points into another page; a plain section
number is this page's.

## Contents

- **[1. Context](#1-context)** -- Only the binding persists; where the seven other items live and how a change is seen.
- **[2. What reproduces at the current source](#2-what-reproduces-at-the-current-source)** -- Nothing is written, nothing comes back, and two changes read durable for a few cycles.
- **[3. Decision](#3-decision)** -- Nine rules: one processor-side writer, live triggers, the clear rule, a two-pass restore.
- **[4. Who writes: three candidates](#4-who-writes-three-candidates)** -- Per-group managers, one writer, the firmware: measured and judged.
- **[5. Interfaces](#5-interfaces)** -- What the processor, the parent and the firmware each change.
- **[6. State machines and next-state functions](#6-state-machines-and-next-state-functions)** -- The writer, the port arbiter, priorities written out.
- **[7. The clear rule](#7-the-clear-rule)** -- When a pending source clears, and every risky ordering executed.
- **[8. Restore](#8-restore)** -- Order, cleared-first proof, value rules, coupling, names, torn streams.
- **[9. What must not persist](#9-what-must-not-persist)** -- Lock, registry and Identify, as refusals with their clauses.
- **[10. Stages](#10-stages)** -- Three independently shippable stages, each with its silicon proof and tickets.
- **[11. Alternatives rejected](#11-alternatives-rejected)** -- With their numbers.
- **[12. Cost](#12-cost)** -- Measured area, derived latency and time.
- **[13. Consequences](#13-consequences)** -- What the decision changes and costs.
- **[14. The executable model and its omissions](#14-the-executable-model-and-its-omissions)** -- What is real, what is a model, the totals.
- **[15. UNRESOLVED](#15-unresolved)** -- What this contract does not settle.
- **[16. Traceability](#16-traceability)** -- Milan clauses, the saved-state acceptance, issue #500's items.

## 1. Context

The binding survives a cold power cycle on silicon since 2026-09-21
(issue #70). Its records, ids `0x20` to `0x2F`, are written by
`KL_acmp_nvm_shadow` through `KL_pp_nvm_port`. Nothing else is written.

The seven other Milan items have no record writer. The
[snapshot-ownership page section 11](SAVED_STATE_SNAPSHOT_OWNERSHIP.md#11-persistent-field-materialization)
reads NONE for each, and the contract reports them honestly instead: the
parent's `pend_i` is the dynamic-state store's sticky level OR the binding
manager's unflushed sinks OR a sticky bit a class-6 or class-7 commit mark
sets (`hdl/milan/KL_pp_shadow.sv` lines 935 to 946). After any such change
the pending bit reads 1 until reset, and no slot ever holds the change.

Where each live value is held, read at the current source:

| Ids | Group | Live value | How a change is seen today |
|---|---|---|---|
| `0x00` | configuration index | `KL_aecp_dyn_state` selector 0, flops with a valid flag | the store's `dirty_o`, sticky until reset |
| `0x02`.. | sampling rate | selector 1 | the same level |
| `0x0A`.. | clock source | selector 2 | the same level |
| `0x30`.. and `0x40`.. | stream formats in and out | selectors 3 and 4 | the same level |
| `0x50`.. | presentation time offset | selector 5 | the same level |
| `0x60` to `0x7F` | channel maps in and out | the PARENT: `hdl/milan/milan_datapath.sv` holds the input store and the output owner and cluster registers, and `hdl/ieee1722/aaf/KL_chan_map_capture.sv` the output map RAM. The processor reaches them only through the GET_AUDIO_MAP read face and the ADD/REMOVE edit face. Their reset value is the EMPTY set (`KL_chan_map_capture.sv` line 427, `milan_datapath.sv` lines 4193 to 4196) | the class-6 commit mark |
| `0x80`.. | user names | the writable name table of `KL_aecp_desc_store`, on chip, initialized from the image by the store's walk | the class-7 commit mark |

`0x01` (system unique id) and `0x12` to `0x19` (media clock reference) are
allocated, but no AECP program writes them, so they have nothing to
materialize and stay erased records.

This page decides the five items of issue #500: who writes each group and
where the writer lives; how a change becomes a record and how the sticky
sources clear; how the values come back; what must not persist; and the
stages.

Authority: [`REQUIREMENTS.md`](../../REQUIREMENTS.md) section 1 ("Required
Milan state must survive power loss"); the saved-state page's
[allocation](SAVED_STATE_FASTCONNECT.md#42-the-allocation----decided-the-donors-f078-rule-unchanged),
[KLJ2 container](SAVED_STATE_FASTCONNECT.md#61-the-container),
[status bits](SAVED_STATE_FASTCONNECT.md#91-the-bits) and
[acceptance](SAVED_STATE_FASTCONNECT.md#16-acceptance-for-the-implementation);
the accepted snapshot-ownership contract, its
[rules](SAVED_STATE_SNAPSHOT_OWNERSHIP.md#3-decision) and its
[obligations O1 to O4](SAVED_STATE_SNAPSHOT_OWNERSHIP.md#7-the-writer-sequence);
the processor's `07_memory_maps.md` section 5 (F07.8 framing, and F07.9: a
committed change sets a record's dirty bit, and the boot restore runs before
`entity_enable`); issue #70's eight items and its vacuity trap; processor
issues 61, 63 and 83.

## 2. What reproduces at the current source

EXECUTED on the tracked glue: `d3_top.sv` built with `D3_TRACKED` is
`KL_pp_shadow.sv` at the current source, transcribed, with no D3 writer.
The run script refuses to report success unless the tracked build fails
exactly these checks (`TRACKED_MUST_FAIL`), so they are shown not to be
vacuous:

| Case : check | Tracked 1x1 | This design, both shapes |
|---|---|---|
| K1 : converged@end | FAILS "backed 1 dirty 0 stale 0 pend 1" | passes |
| K1 : value_in_slot@end:0x50 | FAILS "newest verified slot None" | passes |
| K10 : value_in_slot@end:0x80 | FAILS | passes |
| K12 : value_in_slot@end:0x70 | FAILS | passes |
| V1b : set_value_survives_power_cycle:0x50 | FAILS "restored 0 valid 0, set 1500000" | passes |
| K10 : no_durable_claim_over_unsaved | FAILS "change of 0x80 at 30182 inside a durable interval ending 30189" | passes |
| K12 : no_durable_claim_over_unsaved | FAILS "change of 0x70 at 30155 inside a durable interval ending 30161" | passes |

The run script also requires the tracked glue to PASS the durability check
on K1, V1a and V1b (`TRACKED_MUST_PASS`). A dynamic-state change is reported
from its own write by the store's level, so today's status never reads
durable over one.

The last two rows are a finding about today's glue, not only the gap. It
takes the class-6 and class-7 COMMIT MARKS, and the programs raise them only
after the live write: in `protocol-processor/hdl/aecp/ucode/gen_ucode.py`,
SET_NAME's `NVM_MARK` (line 2092) follows its last `NAME_WR` by COMPARE,
BR_STATUS and COMMIT, and ADD/REMOVE_AUDIO_MAPPINGS's (line 1792) follows
the commit loop by FINISH, COMMIT, SET_STATUS, COMPARE and BR_STATUS.
Between the two, the status reads durable over an applied name or map: 7
and 6 model cycles here, a few instructions in the product (DERIVED). This design triggers on
the write instead (section 3, rule 3). Stages 2 and 3 remove the window;
until they land it stays, and ticket T6 of section 10 records it.

## 3. Decision

**One processor-side record writer materializes every non-binding group.
It shares `KL_pp_nvm_port` with the binding manager, so the records reach
the window through the same device face as the binding records, and the
accepted snapshot contract applies to them unchanged.** This is candidate
(b) of section 4. The rules:

1. **One writer**, `KL_aecp_nvm_writer`, in the processor, beside the
   stores it reads: the AECP engine's state bus, its dispatch and its two
   map faces are all there. It owns 49 records at 1x1 and 145 at 8x8 (every
   allocated id but `0x01`, `0x12` to `0x19` and the bindings).
2. **No shadow.** One dirty bit per record. At flush the writer LATCHES the
   live value from its owner, in ONE window in which no AECP program runs
   and none is dispatched: the dynamic-state store or the name table over
   the state bus, a port's map over the GET_AUDIO_MAP read face. A latched
   value is therefore always a value some completed command left.
3. **Triggers are the live writes, never the commit marks**: the µCPU's
   accepted state-bus write to a persisted dynamic-state row (selectors 0
   to 5) or to a name-table entry, and the edit face's commit-one-record
   beat (`amap_edit_phase_o` 5) for a map. Selector 7, IDENTIFY, is never a
   trigger. The marks follow the write by a program tail (section 2), and
   the class-1 mark cannot name its record: SET_STREAM_FORMAT and
   SET_STREAM_INFO both raise class 1 on a Stream Output, for two different
   records. This departs from two repository statements, and the departure
   is a DECISION REQUESTED of the contract reviews (section 15, item 1).
4. **The clear rule** (section 7): a record's dirty bit is set by a change
   and cleared only by the done of the whole-record WRITE that carries a
   value latched after the last change. A change after the latch taints the
   write, and a tainted write clears nothing. A change on the done edge
   wins. Set and clear name the record by group AND index.
5. **One device-face initiator.** The records reach the window only through
   `KL_pp_nvm_port`, behind a two-manager arbiter (section 6.4): the
   binding manager is manager 0, the writer manager 1. The backend sees
   nothing new, so obligation O1 holds as written.
6. **The pending source.** `pend_i` becomes the binding manager's unflushed
   sinks OR the writer's unflushed records. The dynamic-state level and the
   parent's sticky class-6/7 bit LEAVE `pend_i`: a per-record bit replaces
   each of them, stage by stage (section 10).
7. **Restore** (section 8), after the binding walk and before the entity is
   enabled: the writer walks every record twice through the port. The first
   pass only proves that no stream is torn; the second judges each value by
   the rule of the SET program that would set it, and applies it with its
   valid flag, or leaves the image default. A restore write is never a
   change. Restore done is both walks; blank is neither walk validating a
   record.
8. **An output map set its record cannot hold** is never written in part
   and never forgotten: it stays pending, and the flush skips it until its
   port changes again (section 7.2, K16).
9. **The firmware loads the AEM image before `nvm_boot`**, one reorder of
   `milan_init` (section 5.3), so the restore can judge values against the
   image and write names after the store has walked it.

## 4. Who writes: three candidates

MEASURED out of context by the saved-state page's
[section 8.3](SAVED_STATE_FASTCONNECT.md#83-the-area-measured) recipe
(`synth_xilinx -family xc7 -flatten`, distributed RAM priced as LUTs),
reimplemented standalone because `syn/yosys/ooc.sh` only accepts its own
tops. The standalone recipe and `syn/yosys/ooc.sh` return the SAME row for
`KL_nvm_backend` at the 1x1 shape with 30 names: 1,030 LUT, 468 FF, 6 DSP,
114 CARRY4 (the command record). LUT is the LUT-equivalent total, the worse
of the DSP and no-DSP mappings.

| | (a) a manager per group | (b) one writer (DECIDED) | (c) the firmware writes |
|---|---|---|---|
| Where | seven managers in the processor, each in the image of `KL_acmp_nvm_shadow`, with a shadow each | one writer in the processor, no shadow | the parent's firmware reads values over CSRs and frames the records itself; the fabric only reports |
| Area, 1x1 | at least 9,519 LUT, 8,789 FF, 1 RAMB36 | 2,312 LUT, 802 FF, 0 RAMB36, 0 DSP | fabric at least 530 LUT, 266 FF, 0 RAMB36; firmware not measured |
| Area, 8x8 | at least 9,479 LUT, 8,725 FF, 3 RAMB36 | 2,925 LUT, 927 FF, 0 RAMB36, 0 DSP | fabric at least 1,631 LUT, 458 FF, 0 RAMB36 |
| O1, one sequential writer on the device face | kept: eight managers behind the one port | kept: two managers behind the one port | the device face carries no D3 record at all, so the open vector, the attestation and the capture identity never see one: a second ownership mechanism must carry them |
| What a controller observes | pending from the write; durable after the manager debounce, the firmware debounce and a commit | the same | pending from the write; durable after the firmware debounce and a commit |
| Testability | seven managers to grade | the processor's own suites and the parent's co-simulation | the firmware on the host model plus a new CSR face |
| Repository | processor | processor, a small parent glue change and one firmware reorder | both, and the processor's `07_memory_maps.md` section 5 must be amended to assign the groups to the integrator |

How each figure is made. (b) is the prototype writer plus the arbiter
(2,266 + 46 LUT and 800 + 2 FF at 1x1; 2,879 + 46 LUT and 925 + 2 FF at
8x8). (a) is a FLOOR: seven copies of `KL_acmp_nvm_shadow` at one sink
(1,323 LUT and 1,223 FF each), plus a proxy holding the shadows the seven
groups need at the shape (`d3a_shadow_proxy.sv`: 258 LUT, 228 FF and 1
RAMB36 at 1x1; 218 LUT, 164 FF and 3 RAMB36 at 8x8). Its eight-way port
arbiter is not counted. (c) is a FLOOR too: a proxy of the fabric half
(`d3c_fabric_proxy.sv`: per-record change tracking with a snapshot
handshake, a read window over the dynamic-state rows, and a CSR bridge onto
the state bus). Its firmware links into the BIOS, in the fixed 128 KiB
integrated ROM (`sw/litex/milan_soc.py` sets `integrated_rom_size`), so it
costs no new block RAM until that ROM overflows.

**Why (b).** In order of weight:

1. **The accepted contract applies unchanged.** In (b) and (a) a D3 record
   is a record the port writes, like a binding. The open vector, the
   capture, the attestation, the acknowledgement identity and the pending
   bit cover it with no new rule. In (c) no D3 record crosses the device
   face: a CSR-level snapshot handshake would have to carry the clear rule
   beside the contract, obligations O1 to O4 would have to be re-proved for
   it, and the firmware would become a writer of processor state.
2. **BRAM is the binding constraint.** (b) and (c) use none. (a) needs one to
   three RAMB36 for its shadows, on a device that measured 131 of its 135
   block-RAM tiles used on a recent build (the banner of the processor's
   `KL_aecp_desc_store`).
3. **LUT.** (b) is at most 3.6 percent of the XC7A100T's 63,400 LUT at 1x1
   and 4.6 percent at 8x8, out of context; the in-context delta is smaller.
   (a) is three to four times that. (c)'s fabric half is smaller by 1,782
   LUT at 1x1 and 1,294 at 8x8; that is the price of keeping one ownership
   mechanism and of not moving the record framing and the value rules into
   firmware.
4. **The donor's own contract.** The processor's F07.9 puts the commit and
   the restore in the processor, and its issues 61 and 83 ask for exactly
   (b). (c) needs that contract amended first.
5. **Latency is a wash.** (b) adds the processor debounce before the firmware
   debounce (section 12); (c) does not. Both report pending from the write.

## 5. Interfaces

### 5.1 In the processor

All of this is the processor repository's (tickets T1 to T3). The seams are
where the prototype needed them; the implementation places the writer
inside `KL_aecp_engine` or beside it with these ports.

| Face | Signals | Contract |
|---|---|---|
| State-bus client | `sb_req`, `sb_we`, `sb_name`, `sb_addr[19:0]`, `sb_wdata[63:0]`, `sb_wstrb`, `sb_didx[15:0]`; `sb_ready`, `sb_rvalid`, `sb_rdata`, `sb_err` | the engine's state port, with the µCPU's own contract: the request is held until the answer. A 2:1 selection in front of the two stores, `own` choosing the writer |
| Ownership | `own` (writer to engine), `prog_busy` (engine to writer) | the engine dispatches no program while `own` is 1; the writer raises `own` only in a cycle `prog_busy` is 0. `prog_busy` is the µCPU's busy, which covers the program's commit marks |
| Change snoop | the µCPU's accepted write: `st_req AND st_we AND region 1 AND dyn_ready`, with `st_addr[15:3]` the selector and `desc_index`; a name write: `st_name AND st_we AND store_ready`, with `st_addr[15:6]` the name ordinal | the writer's trigger for the dynamic-state records and the names. Selector 7 and an out-of-range index set nothing |
| Map trigger | `amap_edit_req_o AND amap_edit_phase_o == 5`, with `amap_edit_desc_type_o` and `amap_edit_desc_index_o` | the commit-one-record beat, after phase 1's point of no return; it sets the port's record |
| Map read | the GET_AUDIO_MAP face (`amap_req_o` and its type, index, map index, selector and record ordinal; `amap_data_i`, `amap_wait_i`) | driven by the writer while `own` is 1 |
| Map restore | the edit face, phases 0, 4, 1, 5 and 2 or 3 | driven by the writer while `own` is 1, during the restore only |
| Format judge | the Milan-info gather face, kind 0 selector 15, with `gsi_prop_fmt_o` | the integrator's judgement of a proposed format: bit 0 supported, bit 1 no mapped channel orphaned |
| Port | `KL_pp_nvm_mgr_arb` in front of `KL_pp_nvm_port` | section 6.4 |
| Exports | `nvm_unflushed_o` stays the binding manager's; new `d3_unflushed_o`, the OR of the writer's dirty bits; `nvm_alarm_o` becomes both managers' alarm; `restore_done_o`, `restore_fail_o` and `restore_blank_o` become both walks | section 8.7 |
| Parameters | the shape (`N_STREAM_IN_P` ... `N_NAME_P`, the per-port cluster counts), `LAYOUT_VER_P` shared with the binding manager, `DEB_TICKS_P` (T-NVM-DEBOUNCE), `RETRY_MAX_P` | the record lengths follow section 4.2 of the saved-state page |

The processor's `07_memory_maps.md` section 5.3 draws the runtime commit as
"committed state change (COMMIT + NVM_MARK)" setting the record's dirty bit.
If the contract reviews accept rule 3, ticket T1 updates that figure to the
live write; if they do not, section 15 item 1 says what the mark trigger
would need.

### 5.2 In the parent

`KL_pp_shadow.sv` changes three lines of glue and adds no CSR:

- `pend_i = (|nvm_unflushed_o) | d3_unflushed_o`. The `aecp_mark_pend_r` bit
  is deleted with the stage that retires its last class (section 10);
  `aecp_dyn_dirty_o` stays exported for diagnosis but leaves `pend_i`.
- `alarm_i` takes the processor's combined alarm.
- the restore outputs take the processor's combined verdicts; the blind-walk
  latch is unchanged.

[`REGISTER_MAP.md`](../reference/REGISTER_MAP.md) owes the PP_STAT rows for
the combined restore verdicts when the implementation lands.

### 5.3 In the firmware

`milan_init` becomes `configure_fabric`, `load_aem_image`, `nvm_boot`,
`entity_advertise`: the AEM image moves ahead of the saved state. Two
repository statements disagree today and this resolves them. `milan_init`'s
comment says the saved state is restored "before the entity model is
loaded"; `nvm_boot`'s own comment says it "Runs after the AEM image is in
place and before the entity is advertised, the order Milan 5.5.3.5.2
requires" (`sw/firmware/milan_baremetal/milan_baremetal.c` lines 1448 and
1219). The code follows the first. D3 needs the second: the restore judges
values against the image, and a name written back before the store walks
the image is overwritten by it (section 8.5).

The ledger fact `firmware_boot_order` and the order block of
[`BAREMETAL_FIRMWARE.md`](../integration/BAREMETAL_FIRMWARE.md) move with
the code; `scripts/check_feature_status.py` compares all three. Nothing else
in the firmware changes: the walk it starts through `PP_CTRL[1]` now
includes the D3 walk, and its wait for PP_STAT restore done waits for both.

EXECUTED: the co-simulation compiles the shipping firmware with that one
reorder. F01_old_boot_order keeps the current order, and V1b then restores
nothing: "restored 0 valid 0, slot 0016e360".

## 6. State machines and next-state functions

### 6.1 The writer in service

| State | Leaves when | To |
|---|---|---|
| RUN | the debounce armed and a record is dirty and not skipped | ACQUIRE, the first such record in round-robin order |
| ACQUIRE | `prog_busy` is 0 | LATCH (scalar), LATCH-NAME (eight lanes) or LATCH-MAP (the port's live set); `own` 1, taint 0 |
| LATCH-MAP | the set has more mappings than the record has entries | RUN, `own` 0, the record skipped and still dirty |
| any latch | the value is in the payload buffer | RELEASE |
| RELEASE | one cycle | CRC, `own` 0: programs may run again |
| CRC | the header without its crc field and the payload are summed | REQUEST |
| REQUEST | the arbiter grants manager 1 | STREAM |
| STREAM | the 8 header bytes and the payload are taken | WAIT |
| STREAM or WAIT | the port pulses err | ACQUIRE again (a fresh latch), or RUN with the alarm after `RETRY_MAX_P` retries |
| WAIT | the port pulses done | RUN |

### 6.2 The writer at boot

| State | Leaves when | To |
|---|---|---|
| WAIT-GO | the binding walk is done | ACQUIRE, `own` 1 for the whole walk |
| IMAGE | the descriptor store holds a validated image, after a LOCATE of ENTITY 0 if it did not | NEXT, pass 0 |
| NEXT | the last record of pass 0 | NEXT, pass 1 from the first record |
| READ, STREAM | the port ends the read | pass 0: the next record, or FINISH on a torn stream. Pass 1: the value rule (section 8.3), then APPLY or the next record |
| NEXT | the first name record of pass 1 | CHECK: every restored format is judged again against the final maps (section 8.4) |
| NEXT | the last record of pass 1 | FINISH: done, `own` 0 |

### 6.3 Next-state functions

Priorities are written out, as the snapshot-ownership page does:

```
set[r]      = the live write of section 3 rule 3 that names record r
done_ok     = WAIT AND port done AND NOT taint
giveup      = port err AND retries = RETRY_MAX_P
clr[r]      = (done_ok OR giveup) AND r is the record in hand (group AND index)
dirty[r]'   = set[r] ? 1 : clr[r] ? 0 : dirty[r]
taint'      = (ACQUIRE AND NOT prog_busy) ? 0
            : (set[record in hand] AND the latch has begun) ? 1 : taint
skip[m]'    = set[m] ? 0 : (m in hand AND its set overflows the record) ? 1 : skip[m]
                                                     (map records only)
eligible[r] = dirty[r] AND NOT skip[r]
armed'      = the debounce window closed ? 1 : (RUN AND no record eligible) ? 0 : armed
own'        = (ACQUIRE AND NOT prog_busy) ? 1 : RELEASE ? 0 : own
alarm'      = giveup ? 1 : alarm                      (sticky until reset)
d3_unflushed = OR over r of dirty[r]
pend_i      = (OR of the binding manager's unflushed sinks) OR d3_unflushed
```

The debounce is the binding manager's: the first change opens a window of
`DEB_TICKS_P` ticks, and its close arms one burst that drains every eligible
record.

### 6.4 Two managers, one port

The binding manager raises a one-cycle REGISTERED request after it reads the
port idle (`KL_acmp_nvm_shadow.sv` lines 757 to 765), so its request lands
one cycle after the sample. The busy it reads must therefore cover every
cycle in which a request landing next cycle could not be issued: while the
writer owns the port AND in the cycle the writer is granted.

```
idle    = no owner AND port not busy AND no done or err pulse
issue0  = idle AND binding request
issue1  = idle AND NOT binding request AND writer request
m0_busy = port busy OR (owner = writer) OR issue1
owner'  = issue0 ? binding : issue1 ? writer : (done or err) ? none : owner
```

A binding request therefore only ever meets an idle port and is issued at
once; nothing is held. A tie at an idle port goes to the binding manager.
The writer holds its request until granted. EXECUTED: K15 sweeps the
writer's release over 8 cycles against the binding manager's crc pass, and
at one of them (g3) the binding manager samples busy in the writer's grant
cycle ("grant-cycle collisions 1"); both records are committed at every
release. A01_grant_cycle_not_busy deletes the grant-cycle term, the binding
request lands on a taken port and is lost, and the binding never commits:
"binding None, 0x50 0016e36f, grant-cycle collisions 1".

The evidence's first arbiter also held a binding request that met a taken
port. That path was unreachable under the rule above, so its mutant could
not be killed; it is removed, not kept as dead logic.

## 7. The clear rule

### 7.1 What clears, and when

Issue #500 asks that the sticky sources clear "when, and only when, the
record that materializes the change is durable, without ever reading
durable over a change made during the write". This design meets it with a
relay from one bit to the next, not with a new clear input on the old
sources:

1. A change sets its record's dirty bit in the cycle after the accepted
   write; `d3_unflushed` and the pending bit read 1.
2. The writer latches, frames and writes the record. A change after the
   latch taints the write, so its done clears nothing and the record is
   written again from a fresh latch.
3. The untainted WRITE completes with done. The backend closes the record
   at the device face's done and sets `dirty_live` on that same completion;
   the writer's dirty bit clears at the port's done, one cycle later. From
   then on `nvm_dirty` reports the change, and no cycle reports neither.
4. The firmware captures, commits and acknowledges under the accepted
   contract. The durable reading returns only when a verified slot holds
   the record.

So each pending source clears when its record is in the window, and the
status reads durable only when the record is in a slot. The old sources
cannot do this: `aecp_dyn_dirty_o` and the class-6/7 bit are one bit for
many records, so no single record write can clear them. They leave `pend_i`
and the per-record bits replace them (rule 6).

The global check is the definition. `no_durable_claim_over_unsaved` runs on
every case of every build: whenever the status reads durable (backed 1,
dirty 0, stale 0, pend 0), every record's latest accepted value must be the
value the newest verified slot holds, and a change inside a durable
interval must end it within 3 cycles.

### 7.2 The orderings that carry the risk

EXECUTED at 1x1 and at 8x8 unless marked. Values are the check's own
detail.

| Ordering | Case | Named checks | What it read | Mutant killed |
|---|---|---|---|---|
| One change | K1 | converged@end, value_in_slot@end:0x50 | "backed 1 dirty 0 stale 0 pend 0" | M02_clear_at_latch ("durable at 532028: record 0x50 latest 0012d687 slot None"), G01_pend_misses_d3, M17_trigger_misses_ptof |
| One name change | K10 | converged@end, value_in_slot@end:0x80 | the name in the newest verified slot | M18_trigger_misses_names |
| One map change | K12 | converged@end, value_in_slot@end:0x70 | the port's set in the newest verified slot | M19_trigger_misses_out_maps |
| A change during the record write | K2 | taint_rewrites:0x50, no_durable_claim_over_unsaved | "2 completed writes of 0x50; the last carries 0021e88e" | M01_taint_ignored ("durable at 1567725: record 0x50 latest 0021e88e slot 0010f447") |
| Two changes to one field in one debounce window | K3 | coalesced:0x50, value_in_slot@end:0x50 | "1 writes of 0x50 for two changes in one window" | - |
| A second record of the same group in flight | K4 | value_in_slot@end:0x51 | "latest 003d0902, newest verified slot 003d0902" | M04_clear_by_group ("newest verified slot None") |
| A second GROUP in flight: clock source 0x0A while 0x50 streams | K4g | value_in_slot@end:0x0a | "latest 0001, newest verified slot 0001" | M14_clear_by_index ("latest 0001, newest verified slot None") |
| A change on the WRITE's done edge | K5 | same_edge_change_survives@end:0x50 | "latest 004c4b42, newest verified slot 004c4b42" | M03_clear_wins_same_edge ("newest verified slot 004c4b41") |
| A slow SET_NAME across the debounce close | K11 | written_value_was_set:0x80 | every written name is a value a command left | M05_latch_ignores_program (a name latched between two lanes: "BBBB...AAAA") |
| A record write that fails once | K8 | retry_converges:0x50 | "1 failed operations on 0x50, then committed" | - |
| A record write that always fails | K9 | giveup_revokes:0x50 | "alarm 1 backed 0 slot None" | - |
| The binding and D3 records share the port | K13 | both_records_committed | both in the newest verified slot | - |
| The binding request on the writer's grant cycle (1x1) | K15, 8 releases | both_records_committed; the premise | collision reached at g3, 1 of 8 | A01_grant_cycle_not_busy |
| IDENTIFY set | K14 | identify_never_persisted | "0 record writes, dirty 0, pend 0, flash programs 0 -> 0" | M06_identify_is_a_change ("1 record writes ... flash programs 0 -> 13") |
| An output set larger than its record (8x8) | K16 | oversized_set_stays_pending@over, value_in_slot@end:0x70 | "10 mappings on a 9-entry record; pend 1, D3 alarm 0, backed 1, WRITEs of 0x70 0", then written once it fits | M15_overflow_forgets_the_change (the durable reading returns over the unsaved set) |
| Power cut inside the processor debounce | K18a, K18b | pending_at_the_cut@cut, power_cut_loses_only_unsaved:0x50 | "pend 1, D3 unflushed 1"; "restored 1818001 ... the unsaved value 1818002" | - |
| Power cut during the record write | K17a, K17b | cut_inside_the_write@cut, power_cut_loses_only_unsaved:0x50 | "had taken 6 of 12 bytes at the cut"; "restored 1717001" | - |
| Power cut after the record, before the commit | K6a, K6b | power_cut_loses_only_unsaved:0x50 | "restored 1234567 ... the unsaved value 6000001" | - |
| Power cut after the acknowledgement | K7a, K7b | value_restored:0x50 | "restored 7000001 valid 1" | - |

Deleting a trigger reddens a case. M17, M18 and M19 each delete one
group's trigger (the presentation offset, the names, the output maps), and
each is killed by the durability check of the case that changes that group:
"a change inside a durable interval" that never ends. This is the
restatement section 16 proposes for the saved-state page's mark acceptance.

A reset between a change and its record is a power cut here. A reset of
the fabric also resets the CPU (obligation O2), the firmware reloads the
window from the verified slot, and the processor's stores reset, so flash
is the only state carried across. The model's power cycle is exactly that:
a new process, fresh RTL and fresh firmware, with the flash array carried.

## 8. Restore

### 8.1 The order

1. `configure_fabric`.
2. `load_aem_image`: the AEM image in DDR, its CRC checked.
3. `nvm_boot`: both slots validated, the window loaded and the RELOAD
   accepted (the snapshot contract, unchanged), then the walk started through
   `PP_CTRL[1]`.
4. The binding manager's walk: read, validate, replay to the listener.
5. Its done starts the D3 walk. The writer takes the state bus for the whole
   walk; no program runs.
6. If the descriptor store holds no validated image, a LOCATE of ENTITY 0
   makes it walk the one the firmware loaded.
7. Pass 0: every D3 record is read; a torn stream ends the walk.
8. Pass 1: every record is read again, judged and applied or refused; the
   restored formats are judged again against the final maps; the names last.
9. Restore done, for both walks. The firmware stops waiting.
10. `entity_advertise`: the enable bits.

Obligation O3 holds for the writer: it requests nothing before the binding
walk is done, its first requests are its own walk, and its first flush
follows that walk.

EXECUTED: V1b reads "enabled at 5004, D3 restore done at 4992, restore done
at 4992" at 1x1 and "enabled at 8046, D3 restore done at 8031" at 8x8.
G02_restore_done_without_d3 lets the processor report done after the binding
walk alone, and the entity is enabled first: "enabled at 219, D3 restore
done at 4992".

ADP advertises nothing the restore is about to change. The ADPDU carries
the current configuration index from the dynamic state (the processor's
`04_adp_engine.md`), and no ADPDU leaves before the enable. `available_index`
is volatile, 0 at reset, and increments on every transmitted ADPDU
([`REGISTER_MAP.md`](../reference/REGISTER_MAP.md) `ADP_STATUS`), so the
first ADPDU after a power cycle already carries the restored index and no
index is spent on a value that changes. The restore also holds the state bus
for its whole walk, so no AECP program can read a value from before it.

### 8.2 What is proven cleared first

Issue #70's vacuity trap: "a restore that writes nothing and a store that
was never reset both pass a naive read-back". Two checks close it.

- `rows_cleared_before_restore@boot` reads every restorable row BEFORE the
  restore and requires the valid flag clear: "valid flags before the
  restore {cfg 0, rate 0, clks 0, fmti0 0, ptof0 0}". The dynamic-state
  store resets every valid flag; names come from the image walk; the maps
  reset to the empty set. A restored name must also differ from the image
  default.
- `set_value_survives_power_cycle:0x50` compares the restored value with the
  value V1a SET, not with the slot.

The control, EXECUTED: V1b~stale seeds the rows as a store that was never
reset would hold them. Under M13_restore_applies_nothing the naive read-back
of that store PASSES and the cleared-first check FAILS, as the run script
requires ("CONTROL stale store under M13: naive read-back PASSES,
cleared-first FAILS"). M13 itself is killed by value_restored:0x50,
"restored 0 valid 0, slot 0016e360".

### 8.3 The value rule of each group

A record whose frame fails (magic, layout version, record id, length,
crc16) is refused and its image default stays; the walk goes on. A framed
record is applied only if its value passes the rule of the SET program that
would set it:

| Group | The SET program's rule | Refused | EXECUTED |
|---|---|---|---|
| configuration index | SET_CONFIGURATION: index below `configurations_count` (the store's region 0xD) | the image default stays | V4: "cfg row valid 0, refused 1" |
| sampling rate | SET_SAMPLING_RATE: the rate is on the AUDIO_UNIT's `sampling_rates` list, walked as the program walks it | the image default | V2: "rate row valid 0, refused 1"; M09_apply_blindly: "rate row valid 1, refused 0" |
| clock source | SET_CLOCK_SOURCE: index below `clock_sources_count` of the CLOCK_DOMAIN | the image default | V1b: "restored 1 valid 1, slot 0001" |
| stream formats in and out | SET_STREAM_FORMAT: the integrator's judge, gather kind 0 selector 15 | the image default | V6b, V8, V9 (section 8.4) |
| presentation time offset | SET_STREAM_INFO: bit 31 of the latency is BAD_ARGUMENTS (`KL_aecp_engine.sv` line 3159) | the image default | V1b: "restored 1500000 valid 1" |
| channel maps | ADD_AUDIO_MAPPINGS: the integrator judges the staged set whole | the port's reset set is put back | V3: "live OUT0 equals the default True, refused 1" |
| user names | SET_NAME: any 64 bytes; the empty name is a value | - | V7, V1b (section 8.5) |
| any group | the frame, the crc16 | the image default; the next record is still applied | V5: "ptof0 valid 0, refused 1" and "ptof1 1600000 valid 1" |

When can a framed value fail its rule? The container is refused whole
unless its `entity_model_id` matches (KLJ2 rule 7), and
`sw/builder/endstation_builder.py` hashes that id from the model shape:
the rate lists, the formats, the clusters and the clock sources. So within
one id the image's lists cannot move. The rate, clock-source and
configuration rules are defence in depth, for a configuration that pins its
id; no shipped configuration does. The format and map rules are not
optional: they depend on the integrator's judgement and on each other.

### 8.4 Formats and maps are one decision

A format decides which stream channels exist, and a mapping names stream
channels. Restoring either alone can orphan the other, so the order is:

1. Formats are judged on "supported" alone, because the maps they will be
   checked against are not back yet.
2. Each port's saved set replaces its reset set as one staged ADD, judged
   against the restored formats.
3. A refused set puts the reset set back, and first reverts any restored
   format the reset set would orphan.
4. After every map, each restored format is judged again ("no mapped
   channel orphaned") and reverted to the image default if it fails.

EXECUTED: V6b restores a consistent narrower pair ("OUT0 set matches the
slot True"); M10_fmt_full_judge judges the format against the maps before
they are back and refuses it ("fmto0 0 valid 0"). V8 reverts a saved format
that would orphan the reset maps ("0 orphaned mappings"); M11_no_orphan_check
leaves "6 orphaned mappings". V9 refuses a map set and reverts the format
paired with it; M12_no_revert_before_readd fails it ("live OUT0 equals the
default False").

The shipping shapes' dynamic ports reset to the EMPTY set, so step 3 has
nothing to orphan there. The model uses a non-empty reset set so that every
step runs (section 14).

### 8.5 Names wait for the image walk

The store's name table is initialized from the image by the store's walk.
That walk runs at reset, before the firmware has loaded the image, and
again at the first LOCATE of an invalid image (its heal walk). A name
written back before the heal walk is overwritten by the image default at the
first command. The writer therefore makes the store walk first (section 8.1,
step 6).

EXECUTED: V7 restores a name and nothing else, and after the first command
reads "V7 names only restore". M08_restore_skips_image_check reads "Milan
FPGA 1x1 TDM8", the image default.

### 8.6 A torn stream applies nothing

The binding manager rejects its whole walk on a stream torn mid-record. The
writer keeps no copy to stage into, so it reads every record twice instead:
pass 0 proves that no stream is torn, and only pass 1 applies. A frame or
value refusal is still per record.

EXECUTED: V11 fails the backend's memory read inside the payload of 0x80,
after 0x50 was read whole: "ptof0 valid 0 (its record was read whole before
the torn one), restore fail 1, D3 fail 1, applied 0". M16_single_pass_restore
applies 0x50 before it meets the torn one: "ptof0 valid 1 ... applied 1".

### 8.7 What the status says after a restore

- restore done: both walks sequenced.
- restore fail: either walk torn, the image defaults refused, or a blind walk
  (the latch `KL_pp_shadow` already keeps).
- restore blank: NEITHER walk validated a record. V7, a name back and no
  binding, reads "blank 0, done 1"; G04_blank_ignores_d3, the binding walk's
  blank alone, reads "blank 1". V10, a blank first boot, reads "blank 49 of
  49, applied 0 ... status blank 1" (145 of 145 at 8x8).
- A restore write is not a change: "0 record writes after the restore,
  dirty 0, flash erases 0 -> 0". G03_restore_writes_are_changes lets the
  writer's own writes reach its trigger and commits one flash erase for
  nothing: "1 record writes after the restore ... flash erases 0 -> 1".

## 9. What must not persist

| State | Clause, as the repository quotes it | Where it lives | Why nothing here can persist it | Evidence |
|---|---|---|---|---|
| Lock state and the locking controller | Milan v1.2 5.3.4.1, volatile (the processor's `07_memory_maps.md` section 5.1) | `KL_aecp_notify` | not on the state bus, no trigger decodes it, and the allocation gives it no record id | DERIVED, structural; an acceptance item of the implementation |
| The registered-controller list | 5.3.4.2, volatile (same table) | `KL_aecp_notify` | the same | DERIVED, structural; the same acceptance item |
| The IDENTIFY value | 5.3.12: "0 = not identifying" is the reset default (`KL_aecp_dyn_state`'s banner) | `KL_aecp_dyn_state` selector 7 | the trigger decodes selectors 0 to 5; the store raises no dirty for it; SET_CONTROL carries no commit mark | EXECUTED K14; M06 killed |
| Started or stopped | persisted, but in the BINDING record (5.3.8.7) | the listener's binding record | selector 6 is retired | the binding manager's own suites |
| System unique id, media clock reference | allocated as design-affirmative items | nothing writes them | no trigger and no slot in the writer | they stay erased records |

The saved-state page's acceptance already names the check the
implementation owes: "The volatile set does NOT survive: after restore the
lock is clear, the controller registry is empty, IDENTIFY is 0"
([section 16](SAVED_STATE_FASTCONNECT.md#16-acceptance-for-the-implementation)).

## 10. Stages

Each stage ships alone and is proved alone on silicon: set the values from a
controller host, read the status to durable, remove power at the outlet for
8 s (a cold cycle, as the binding proof of 2026-09-21 did), and read every
value back with GET commands. Each also sets IDENTIFY and proves it comes
back 0. The ticket texts are drafted beside this page's evidence.

| Stage | Records | What lands | Silicon proof | Tickets |
|---|---|---|---|---|
| 1. the dynamic-state selectors | configuration index, sampling rate, clock source, stream formats, presentation offset: 9 records at 1x1, 30 at 8x8 | the writer with the state-bus trigger, the flush, the scalar restore and the format rule on "supported"; the arbiter; the exports; `pend_i` loses the dynamic-state level; the firmware reorder | SET_CLOCK_SOURCE 1, SET_STREAM_INFO, SET_STREAM_FORMAT on an unbound input; power cycle; GET_CLOCK_SOURCE, GET_STREAM_INFO, GET_STREAM_FORMAT, and the ADPDU's configuration index | T1 (processor), T4 (this repository) |
| 2. names | 38 at 1x1, 99 at 8x8 | the name trigger, the eight-lane latch, the restore after the image walk; `pend_i` stops taking class 7 | SET_NAME on the entity name, the group name and a stream name, one of them to the EMPTY name; power cycle; GET_NAME | T2, T4 |
| 3. channel maps | 2 at 1x1, 16 at 8x8 | the edit-face trigger, the GET_AUDIO_MAP latch, the coupled restore, the oversized-set rule; the sticky class-6/7 bit is deleted | ADD and REMOVE on both ports; power cycle; GET_AUDIO_MAP | T3, T4 |

Stage 1 restores formats while the maps still reset: the maps come back
empty, so nothing restored can be orphaned. Both shipped shapes list one
sampling rate, so the rate record can only be proved at its default on the
board; V2 covers its refusal. Until stage 3 the class-6 bit stays in
`pend_i`, and until stage 2 the class-7 one, so the pending bit keeps
reporting what no stage writes yet.

The area of each stage is a subset of section 12's row; each lane owes its
own post-place delta by the saved-state page's recipe, at both shipped
shapes.

Further tickets, not stages: T5, the record size of an output map at 8x8
(UNRESOLVED 2); T6, the mark-tail window of today's glue (section 2); T7,
the saved-state page's area table, whose shipping rows predate the #484
contract (section 12).

## 11. Alternatives rejected

| Alternative | Rejected because | Evidence |
|---|---|---|
| (a) A manager per group, in the image of `KL_acmp_nvm_shadow` | three to four times the LUT of (b) and one to three RAMB36 on a device whose binding constraint is block RAM; seven debounces, seven retries and seven restore walks to grade | MEASURED floor, section 4 |
| (c) The firmware materializes the records from CSR reads | D3 records would never cross the device face, so a second ownership mechanism must carry the clear rule beside the accepted contract; the firmware becomes a writer of processor state; the framing and the value rules move into firmware; the donor's F07.9 must be amended. Its fabric half is smaller by 1,782 LUT at 1x1 and 1,294 at 8x8 | MEASURED floor, section 4 |
| Triggering on the commit marks, as the tracked glue does | the marks follow the live write by the program's tail, so the status reads durable over an applied name or map | EXECUTED on the tracked glue, section 2 |
| A shadow of every record inside (b) | 2,432 bytes of names at 1x1 and 6,336 at 8x8 alone; the live value is readable at flush, and latching it costs at most 179 cycles of dispatch hold-off | the (a) shadow rows, section 4; latch windows, section 12 |
| Latching without the dispatch hold-off | a SET in progress is latched half old, half new | EXECUTED: M05 is killed by K11 |
| A single restore pass | a torn stream leaves the records before it applied | EXECUTED: M16 is killed by V11 |
| An alarm on an oversized map set (the evidence's first rule) | the alarm is sticky, so one oversized set would revoke `nvm_backed` for every record until reset | replaced by the pending-and-skip rule; K16 |
| Forgetting or truncating an oversized set | a durable reading over a set no slot holds | EXECUTED: M15 is killed by K16 |
| Restoring by replaying SET commands through the µCPU | it would reuse the programs' own rules, but needs a command path into the dispatch queue with its responses suppressed; not costed | UNRESOLVED 4 |
| Gating the entity enable on restore done in hardware | a device face with no timeout (processor issue 15) would keep the entity dark for ever; the firmware's bounded wait keeps it available, and the order is proved | EXECUTED: G02 is killed by V1b |
| The held-request path in the arbiter | unreachable under the rule of section 6.4, so no case can fail it | the evidence's first mutant A01 survived; the path is removed |
| Growing each output map record to the stream-channel key space | it changes the decided allocation, which is not this page's to change | UNRESOLVED 2 |

## 12. Cost

MEASURED, out of context (section 4's recipe and calibration). LUT is the
LUT-equivalent total.

| Block | 1x1 LUT | 1x1 FF | 8x8 LUT | 8x8 FF | RAMB36 | DSP |
|---|---|---|---|---|---|---|
| the writer, with DSP mapping | 2,266 | 800 | 2,735 | 925 | 0 | 0 |
| the writer, without DSP | 2,228 | 800 | 2,879 | 925 | 0 | 0 |
| the arbiter | 46 | 2 | 46 | 2 | 0 | 0 |
| **(b), worst column** | **2,312** | **802** | **2,925** | **927** | **0** | **0** |
| for scale: the binding manager | 1,040 | 1,081 | 1,119 | 1,123 | 0 | 0 |
| for scale: `KL_pp_nvm_port` | 197 | 116 | 197 | 116 | 0 | 0 |
| for scale: `KL_nvm_backend` | 1,051 | 476 | 1,476 | 515 | 0 | 6 |

DERIVED: the seams of section 5.1 (a 2:1 selection over the state bus and
the two map faces, about 250 signals) add a few hundred LUT at most. The
firmware reorder moves two calls. No block RAM and no main memory is added;
the records use the window the saved-state page already sized.

The saved-state page's area table lists 772 LUT and 377 FF for
`KL_nvm_backend` at 1x1 with 30 names. That row predates the #484 contract:
both recipes return 1,030 LUT and 468 FF for the same parameters at the
current source. Ticket T7 records it.

Time, EXECUTED in model cycles of the processor clock: the dispatch hold-off
lasts 10 cycles for a scalar, 114 for a name, and at most 179 for a port's
map at 1x1 and 120 at 8x8. The whole boot restore, both walks, ends by cycle
4,992 after reset at 1x1 and 8,031 at 8x8. The model's memory answers in 2
or 3 cycles; the product's in about 1.4 µs, so both figures grow on the
board (UNRESOLVED 5).

Latency, DERIVED: the pending bit rises the cycle after the accepted write.
The record reaches the window within `DEB_TICKS_P` (500 ms at the binding
manager's value) plus the latch and the write. The firmware commits after
its provisional 1,000 ms debounce, and a commit takes at most 3.06 s at 1x1
and 3.18 s at 8x8 by the datasheet
([section 9.4](SAVED_STATE_FASTCONNECT.md#94-the-deadlines)). A SET is
therefore durable at most about 4.6 s after it at 1x1 and 4.7 s at 8x8.
The board's own figure is a measurement each stage owes.

## 13. Consequences

- A controller change to any of the seven items becomes durable, and the
  pending bit clears once it is; today it reads 1 until reset.
- An AECP command can wait for one latch window, at most 179 cycles in the
  model, before its program is dispatched.
- The port serves two managers. A binding request can wait for one D3 record
  operation, and the binding manager is otherwise unchanged.
- The processor's restore verdicts mean both walks; the PP_STAT rows of
  [`REGISTER_MAP.md`](../reference/REGISTER_MAP.md) owe the update.
- `milan_init`'s order changes, and with it the ledger fact
  `firmware_boot_order` and the order block of
  [`BAREMETAL_FIRMWARE.md`](../integration/BAREMETAL_FIRMWARE.md).
- A D3 restore is all or nothing against a torn stream, and per record
  against a bad frame or a refused value.
- An output map set larger than its record stays pending until it shrinks;
  at 1x1 that cannot happen (section 15, item 2).
- The value rules exist twice, in the programs and in the writer
  (UNRESOLVED 4).
- The writer's alarm is sticky like the binding manager's, and joins its
  revocation of `nvm_backed`.
- Lock, registry and IDENTIFY stay volatile.
- Obligations O1 to O4 of the snapshot contract are unchanged; the writer
  is one more manager behind the one initiator, and an implementation lane
  inherits all four.

## 14. The executable model and its omissions

- ONE process per build, one clock. REAL at the pinned processor: the
  dynamic-state store, the descriptor store walking a real AEMI image of the
  shape, the binding manager and the port. SHIPPING: `KL_nvm_backend.sv`,
  and the firmware `milan_baremetal.c` compiled for the host through its two
  CSR primitives, with the one reorder of section 5.3. PROTOTYPE: the writer
  and the arbiter. TRANSCRIBED: the parent glue of `KL_pp_shadow.sv`, and
  under `D3_TRACKED` the glue as it ships.
- MODELS, each stated where it is coded: the µCPU is a bus-functional model
  running programs as state-bus operations, with the dispatch hold-off and
  the commit marks after the write; the parent's map plane is C++, keyed as
  `milan_datapath.sv` keys it (an input mapping by cluster, an output
  mapping by stream channel owned by one port); the format judge's
  "supported" rule is a model of the integrator's; the edit face is one
  staged set, where the product has phases 0 to 5.
- The model's reset map set is non-empty (the first clusters of each port on
  the first channels of one stream), where the shipping dynamic ports reset
  to empty. That exercises every step of section 8.4; it is not the
  product's default.
- Time: the model clock is 1 MHz; the hold, the debounces, the deadlines and
  the heartbeat are counted in it. The CPU's instructions take no model
  time; DDR answers in 2 or 3 cycles; the flash is the host model. No
  hardware ran.
- Not modelled: the real microprograms' timing (the mark tail is DERIVED
  from `gen_ucode.py`), the product's GET_AUDIO_MAP hold of two cycles a
  beat, real flash, placement.
- TOTALS: 27 builds (2 shapes, the tracked glue, 24 mutants), 121 graded
  runs, 778 graded checks, 0 verdict failures. Every one of the 24 mutants
  is killed by the one check the run script names for it; the vacuity
  control holds; the K15 premise is reached; the tracked glue fails its 7
  named checks and passes its 4. The command record lists every command and
  the sha256 of every evidence file and of the 13 repository files the model
  reads.

## 15. UNRESOLVED

1. **DECISION REQUESTED: the trigger is the live write, not the commit
   mark.** Two repository statements name the mark: the saved-state page's
   acceptance ("deleting it alone must redden a save/restore test") and the
   processor's F07.9 ("committed state change (COMMIT + NVM_MARK)"). Rule 3
   departs from both, for two reasons: the mark follows the live write by a
   program tail, so a mark trigger reads durable over an applied change
   (EXECUTED on today's glue, section 2), and the class-1 mark cannot name its
   record (SET_STREAM_FORMAT and SET_STREAM_INFO both raise class 1 on a
   Stream Output). This page proposes restating the acceptance as "deleting
   each group's TRIGGER alone must redden a save/restore test" (M17 to M19
   show the shape) and updating F07.9 in ticket T1. If the reviews keep the
   mark, the mark must carry the opcode and the descriptor so it can name a
   record, and the tail window must be accepted and stated.
2. **An output map set can outgrow its record at 8x8.** The allocation gives
   a map record 8 bytes a cluster. An output mapping is keyed by stream
   channel, so one cluster may feed several: at 8x8 a port has 9 entries
   against 72 stream channels. This design keeps such a set pending and
   never writes it in part (K16). Growing the record is an allocation
   change, ticket T5. At 1x1 it cannot happen: 16 stream channels against
   17 entries.
3. **Two debounces.** The writer uses the binding manager's T-NVM-DEBOUNCE
   and the firmware adds its own 1,000 ms. The value of T-NVM-DEBOUNCE is
   still open
   ([section 14](SAVED_STATE_FASTCONNECT.md#14-what-this-page-does-not-decide)).
   A shorter writer debounce costs only port writes to main memory.
4. **The value rules exist twice**, in the programs and in the writer, and
   can diverge. Replaying the records as SET commands through the µCPU would
   remove the copy; it is not costed here.
5. **Time on the board.** The latch windows and the restore time are model
   cycles; the product's memory latency and GET_AUDIO_MAP hold are not
   measured.
6. **Area in context.** The rows are out-of-context upper bounds; each stage
   owes its post-place delta at both shapes.
7. **Today's mark-tail window** (section 2) stays until stages 2 and 3 land.
8. **System unique id and media clock reference** have allocated records and
   no source; nothing here writes them.
9. **An edit that changes nothing** still raises commit beats, so its port's
   record is written again for nothing; the program's FINISH knows, the
   trigger does not.
10. **The writer's alarm is sticky until reset**, as the binding manager's
    is; the snapshot page's UNRESOLVED 7 (forgiveness) covers it too.

## 16. Traceability

Milan v1.2 clauses, as the saved-state page lists them
([section 4.1](SAVED_STATE_FASTCONNECT.md#41-what-the-persisted-set-actually-needs)):

| Clause | Item | Records | Where | Executed by |
|---|---|---|---|---|
| 5.3.5.1 | sampling rate | `0x02`.. | 3, 8.3, 10 | V2, V1b |
| 5.3.7.1 | Stream Output format | `0x40`.. | 3, 8.3, 8.4, 10 | V6b, V8, V9 |
| 5.3.7.6 | presentation time offset | `0x50`.. | 3, 7, 8.3, 10 | K1 to K9, K17, K18, V1b, V5 |
| 5.3.8.1 | Stream Input format | `0x30`.. | 3, 8.3, 8.4, 10 | V1b |
| 5.3.8.2, 5.3.8.3, 5.3.8.7 | bound state, binding parameters, started or stopped | `0x20`.. | the binding manager, unchanged; 6.4 | K13, K15 |
| 5.3.9.1, 5.3.10.1 | channel mappings in and out | `0x60` to `0x7F` | 3, 7, 8.3, 8.4, 10 | K12, K16, V3, V1b |
| 5.3.11.1 | clock source | `0x0A`.. | 3, 8.3, 10 | K4g, V1b |
| 5.3.13 | user names | `0x80`.. | 3, 8.5, 10 | K10, K11, V7, V1b |
| design-affirmative | configuration index | `0x00` | 3, 8.1, 8.3, 10 | V4, V1b |
| 5.3.4.1, 5.3.4.2, 5.3.12 | lock, registry, IDENTIFY: must NOT persist | - | 9 | K14 |

The saved-state acceptance as the repository quotes it
([section 16](SAVED_STATE_FASTCONNECT.md#16-acceptance-for-the-implementation)),
the items this design answers:

| Item | Here | Stays with |
|---|---|---|
| "All eight Milan items plus the bound state, the binding parameters and started/stopped survive a reset that is proven to have cleared the rows first" | 8.2, 10 | each stage's silicon proof |
| "The volatile set does NOT survive: after restore the lock is clear, the controller registry is empty, IDENTIFY is 0" | 9 | the implementation's suite |
| "A user name SET to the EMPTY string survives a power cycle as the empty string" | 8.3, 10 (stage 2) | stage 2 |
| "Each of the eight marks in section 12.1 is graded end to end: deleting it alone must redden a save/restore test" | 3 (rule 3), 7.2, 15 (item 1) | DECISION REQUESTED. Under this design deleting a mark reddens nothing, because the trigger is the write; the item would be restated as deleting each group's TRIGGER (M17 to M19). The IDENTIFY half, adding a mark to SET_CONTROL, is unchanged in spirit: M06 adds IDENTIFY to the trigger and is killed |
| "The manager emits records at the section 4.2 ids, and a record whose id is outside its group's block is refused rather than written" | 3 (rule 1), 8.3 | the implementation's suite |
| "A power cut inside the debounce window loses exactly the marked changes, and `nvm_dirty` said so beforehand" | 7.2 (K18) | silicon. Inside the WRITER's debounce it is the pending bit that says so ("pend 1, D3 unflushed 1"); `nvm_dirty` says so inside the firmware's |

Issue #500's five items: who and where, section 4; the trigger and the clear
rule, sections 6 and 7; restore, section 8; what must not persist, section
9; stages, section 10.
