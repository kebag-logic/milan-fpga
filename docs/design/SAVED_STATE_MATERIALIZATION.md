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
>
> **Revision b** answers the round-one contract reviews of this page at
> `d0256846` (R217 and R218, both NEGATIVE). The restore is now a
> transaction: a transport failure in either pass leaves nothing partly
> applied, because pass 1 rolls every restorable owner back to its reset
> state (section 8.6). Every restore wait has a deadline, an abandoned read
> is drained, and the entity enable is released by the restore itself, never
> by a firmware timeout (section 8.8). An unused map entry is exactly eight
> 0xFF bytes (section 8.3). Every group's replay is graded with its value and
> its valid flag, a legal non-default sampling rate on a synthetic test
> configuration (section 8.2). Stage 3 is blocked on #501 and every stage
> waits for #502 before it is declared shippable (section 10). The live-write
> trigger stays a requested amendment, now with the exact wording it would
> replace (section 15 item 1). The evidence runner fails its exit status on
> any verdict failure, and seven process controls prove it (section 14).
> Section 16 maps every finding to its answer.

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
  `branch 500-design-evidence, commit ca8cb5943f885c22aec397ff75059e2d4791f4fb, path design-evidence/500-materialization/COMMAND_RESULTS.md`;
- how to re-run it:
  `branch 500-design-evidence, commit ca8cb5943f885c22aec397ff75059e2d4791f4fb, path design-evidence/500-materialization/proposal-evidence/README.md`;
- the run script:
  `branch 500-design-evidence, commit ca8cb5943f885c22aec397ff75059e2d4791f4fb, path design-evidence/500-materialization/proposal-evidence/run.py`;
- its graded results:
  `branch 500-design-evidence, commit ca8cb5943f885c22aec397ff75059e2d4791f4fb, path design-evidence/500-materialization/proposal-evidence/results.txt`
  and `results.json` beside it;
- the prototype writer and arbiter:
  `branch 500-design-evidence, commit ca8cb5943f885c22aec397ff75059e2d4791f4fb, path design-evidence/500-materialization/proposal-evidence/prototype/`;
- the area rows and the two cost proxies:
  `branch 500-design-evidence, commit ca8cb5943f885c22aec397ff75059e2d4791f4fb, path design-evidence/500-materialization/proposal-evidence/ooc/`;
- the ticket drafts of section 10:
  `branch 500-design-evidence, commit ca8cb5943f885c22aec397ff75059e2d4791f4fb, path design-evidence/500-materialization/tickets/`.

The evidence the round-one reviews examined is commit
`a21b165ac1c671d10cba7255beaf75cea0f81d18` on the same branch. Its
counterexamples are kept as named cases and mutants of this revision
(section 16).

A section number that is a link points into another page; a plain section
number is this page's.

## Contents

- **[1. Context](#1-context)** -- Only the binding persists; where the seven other items live and how a change is seen.
- **[2. What reproduces at the current source](#2-what-reproduces-at-the-current-source)** -- Nothing is written, nothing comes back, and two changes read durable for a few cycles.
- **[3. Decision](#3-decision)** -- Ten rules: one processor-side writer, live triggers, the clear rule, a restore transaction, deadlines, the enable.
- **[4. Who writes: three candidates](#4-who-writes-three-candidates)** -- Per-group managers, one writer, the firmware: measured and judged.
- **[5. Interfaces](#5-interfaces)** -- What the processor, the parent and the firmware each change.
- **[6. State machines and next-state functions](#6-state-machines-and-next-state-functions)** -- The writer, the restore transaction, the port arbiter and its drain, priorities written out.
- **[7. The clear rule](#7-the-clear-rule)** -- When a pending source clears, and every risky ordering executed.
- **[8. Restore](#8-restore)** -- Order, cleared-first proof, value rules, coupling, names, the transaction, deadlines.
- **[9. What must not persist](#9-what-must-not-persist)** -- Lock, registry and Identify, as refusals with their clauses.
- **[10. Stages](#10-stages)** -- Three stages, their release conditions under #501 and #502, and the tickets.
- **[11. Alternatives rejected](#11-alternatives-rejected)** -- With their numbers.
- **[12. Cost](#12-cost)** -- Measured area, derived latency and time.
- **[13. Consequences](#13-consequences)** -- What the decision changes and costs.
- **[14. The executable model and its omissions](#14-the-executable-model-and-its-omissions)** -- What is real, what is a model, the process controls, the totals.
- **[15. UNRESOLVED](#15-unresolved)** -- What this contract does not settle, and the amendment it requests.
- **[16. Traceability](#16-traceability)** -- Milan clauses, the saved-state acceptance, issue #500's items, the review findings.

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
it releases `entity_enable`); issue #70's eight items and its vacuity trap;
processor issues 15, 61, 63 and 83; issues #501 and #502.

## 2. What reproduces at the current source

EXECUTED on the tracked glue: `d3_top.sv` built with `D3_TRACKED` is
`KL_pp_shadow.sv` at the current source, transcribed, with no D3 writer and
the enable as it ships. The run script requires the tracked build to fail
exactly these checks (`TRACKED_MUST_FAIL`), so they are shown not to be
vacuous; if one does not fail it exits 1 and names it:

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
and 6 model cycles here, a few instructions in the product (DERIVED). This
design triggers on the write instead (section 3, rule 3). The defect is
issue #502, and section 10 makes its correction a condition of every stage
declared shippable.

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
   records. This departs from accepted wording in two repository pages and
   the processor's F07.9; section 15 item 1 requests that amendment and
   quotes what it replaces.
4. **The clear rule** (section 7): a record's dirty bit is set by a change
   and cleared only by the done of the whole-record WRITE that carries a
   value latched after the last change, or when the record is given up after
   `RETRY_MAX_P` failed writes, which raises the sticky alarm that revokes
   `nvm_backed` (the same exception the binding manager makes). A change
   after the latch taints the write, and a tainted write clears nothing. A
   change on the done edge wins. Set and clear name the record by group AND
   index.
5. **One device-face initiator, two arbitrated producers.** The records
   reach the window only through `KL_pp_nvm_port`, so the backend still sees
   one device-face initiator. The port's manager face gains an explicit
   arbiter (section 6.4): the binding manager is manager 0, the writer
   manager 1, and a read the writer abandons is DRAINED there, never handed
   on. Obligation O1 is untouched: it constrains the one sequential
   CONTROL-face master (the strobe word, the image base and length, the
   channel-map tables), and neither the writer nor the drain writes a
   control-face register. Obligation O3, which orders device-face
   initiators after the restore walk, holds as well (section 8.1).
6. **The pending source.** `pend_i` becomes the binding manager's unflushed
   sinks OR the writer's unflushed records. The dynamic-state level and the
   parent's sticky class-6/7 bit LEAVE `pend_i`: a per-record bit replaces
   each of them, stage by stage (section 10).
7. **The restore is a transaction** (section 8.6), after the binding walk
   and before the entity is enabled. The writer owns the state bus FROM
   RESET, so no AECP program runs before or during the restore and the state
   it restores into is the reset state. It reads every record twice through
   the port: pass 0 only proves the records whole, pass 1 judges each value
   by the rule of the SET program that would set it and applies it with its
   valid flag, or leaves the image default. A transport failure in pass 0
   applies nothing. One in pass 1 ROLLS BACK: every restorable owner returns
   to its reset state, so no partial restore survives. A restore write is
   never a change. Restore done is both walks' terminal; blank is neither
   walk validating a record.
8. **Deadlines, and the enable** (section 8.8). Every restore wait is
   bounded (`RS_TMO_CYC_P` cycles without progress); its expiry is an abort
   like a torn read. The restore ends in one of three terminals: COMPLETE,
   DEFAULTS (rolled back) or CLOSED (a roll-back that cannot prove the image
   walked). The entity enable the firmware requests reaches the entity only
   at the restore's done, as the processor's F07.9 draws it ("release
   entity_enable"). A restore that never reaches done keeps the entity dark:
   fail-closed, never an early enable.
9. **An output map set its record cannot hold** is never written in part
   and never forgotten: it stays pending, and the flush skips it until its
   port changes again (section 7.2, K16). This is FAILURE CONTAINMENT, not
   persistence: Milan 5.3.10.1 requires the accepted set to persist, and
   stage 3 does not open until #501 decides a conforming allocation or
   limit (section 10).
10. **Three firmware changes** (section 5.3): the AEM image loads before
    `nvm_boot`; the restore walk starts on every boot path; the restore
    wait's timeout and the enable line report that the fabric holds the
    enable.

## 4. Who writes: three candidates

MEASURED out of context by the saved-state page's
[section 8.3](SAVED_STATE_FASTCONNECT.md#83-the-area-measured) recipe
(`synth_xilinx -family xc7 -flatten`, distributed RAM priced as LUTs),
reimplemented standalone because `syn/yosys/ooc.sh` only accepts its own
tops. The standalone recipe and `syn/yosys/ooc.sh` return the SAME row for
`KL_nvm_backend` at the 1x1 shape with 30 names: 1,030 LUT, 468 FF, 6 DSP,
114 CARRY4 (the command record, re-run for this revision). LUT is the
LUT-equivalent total, the worse of the DSP and no-DSP mappings.

| | (a) a manager per group | (b) one writer (DECIDED) | (c) the firmware writes |
|---|---|---|---|
| Where | seven managers in the processor, each in the image of `KL_acmp_nvm_shadow`, with a shadow each | one writer in the processor, no shadow | the parent's firmware reads values over CSRs and frames the records itself; the fabric only reports |
| Area, 1x1 | reference replication: 9,519 LUT, 8,789 FF, 1 RAMB36 | 2,311 LUT, 862 FF, 0 RAMB36, 0 DSP | fabric proxy: 530 LUT, 266 FF, 0 RAMB36; firmware not measured |
| Area, 8x8 | reference replication: 9,479 LUT, 8,725 FF, 3 RAMB36 | 2,876 LUT, 987 FF, 0 RAMB36, 0 DSP | fabric proxy: 1,631 LUT, 458 FF, 0 RAMB36 |
| O1, the one sequential control-face master | untouched: no manager writes the control face | untouched: neither the writer nor the drain writes a control-face register | still the firmware alone, but its control face GROWS: a per-record snapshot handshake and a state-bus bridge must be sequenced against ARM, ATTEST and ACK, a contract change to resolve explicitly |
| The device face, and O3 | eight producers behind the one port need an eight-way arbiter; each comes up after the restore walk | two producers behind the one port, with the arbiter and drain of section 6.4; the writer's first requests are its own restore walk | no D3 record crosses it, so the open vector, the attestation and the capture identity never see one: a second ownership mechanism must carry them |
| What a controller observes | pending from the write; durable after the manager debounce, the firmware debounce and a commit | the same | pending from the write; durable after the firmware debounce and a commit |
| Testability | seven managers to grade | the processor's own suites and the parent's co-simulation | the firmware on the host model plus a new CSR face |
| Repository | processor | processor, the parent glue and map-plane reset, and three firmware changes | both, and the processor's `07_memory_maps.md` section 5 must be amended to assign the groups to the integrator |

How each figure is made. (b) is the prototype writer at its worse mapping
plus the arbiter (2,263 + 48 LUT and 859 + 3 FF at 1x1; 2,828 + 48 LUT and
984 + 3 FF at 8x8). (a) estimates reference replication: seven copies of
`KL_acmp_nvm_shadow` at one sink (1,323 LUT and 1,223 FF each), plus a proxy
holding the shadows the seven groups need at the shape
(`d3a_shadow_proxy.sv`: 258 LUT, 228 FF and 1 RAMB36 at 1x1; 218 LUT, 164
FF and 3 RAMB36 at 8x8). Its eight-way port arbiter is not counted. (c)
measures a proxy of the fabric half (`d3c_fabric_proxy.sv`: per-record change
tracking with a snapshot handshake, a read window over the dynamic-state
rows, and a CSR bridge onto the state bus). Its firmware links into the BIOS,
in the fixed 128 KiB integrated ROM (`sw/litex/milan_soc.py` sets
`integrated_rom_size`), so it costs no new block RAM until that ROM
overflows. These proxies omit work needed for integration; they do not
bound every implementation of either alternative. Sharing or specializing
per-group managers can change (a)'s cost, and synthesis in context can
change every row. None of these figures is a bound on an integrated
implementation.

**Why (b).** In order of weight:

1. **The accepted contract applies unchanged.** In (b) and (a) a D3 record
   is a record the port writes, like a binding. The open vector, the
   capture, the attestation, the acknowledgement identity and the pending
   bit cover it with no new rule, and the control face does not change. In
   (c) no D3 record crosses the device face: a CSR-level snapshot handshake
   on a larger control face would have to carry the clear rule beside the
   contract, obligations O1 to O4 would have to be re-proved for it, and
   the firmware would become a writer of processor state.
2. **BRAM is the binding constraint.** (b) and (c) use none. (a) needs one to
   three RAMB36 for its shadows, on a device that measured 131 of its 135
   block-RAM tiles used on a recent build (the banner of the processor's
   `KL_aecp_desc_store`).
3. **LUT.** (b) measures about 3.65 percent of the XC7A100T's 63,400 LUT at
   1x1 and 4.54 percent at 8x8, out of context. Its integrated delta remains
   to be measured. The reference replication in (a) costs three to four
   times that. The measured fabric proxy in (c) is smaller by 1,781 LUT at
   1x1 and 1,245 at 8x8. That comparison excludes firmware and integration
   costs; it supports the choice alongside the ownership and interface
   arguments above.
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
| Ownership | `own` (writer to engine), `prog_busy` (engine to writer) | the engine dispatches no program while `own` is 1. `own` is 1 FROM RESET until the restore's terminal (section 8.6), and 1 for ever in the CLOSED terminal. In service the writer raises `own` only in a cycle `prog_busy` is 0; `prog_busy` is the µCPU's busy, which covers the program's commit marks |
| Change snoop | the µCPU's accepted write: `st_req AND st_we AND region 1 AND dyn_ready`, with `st_addr[15:3]` the selector and `desc_index`; a name write: `st_name AND st_we AND store_ready`, with `st_addr[15:6]` the name ordinal | the writer's trigger for the dynamic-state records and the names, tapped on the µCPU's side of the 2:1 selection so a restore write is never a change. Selector 7 and an out-of-range index set nothing |
| Map trigger | `amap_edit_req_o AND amap_edit_phase_o == 5`, with `amap_edit_desc_type_o` and `amap_edit_desc_index_o` | the commit-one-record beat, after phase 1's point of no return; it sets the port's record |
| Map read | the GET_AUDIO_MAP face (`amap_req_o` and its type, index, map index, selector and record ordinal; `amap_data_i`, `amap_wait_i`) | driven by the writer while `own` is 1 |
| Map restore | the edit face, phases 0, 4, 1, 5 and 2 or 3 | driven by the writer while `own` is 1, during the restore only |
| Format judge | the Milan-info gather face, kind 0 selector 15, with `gsi_prop_fmt_o` | the integrator's judgement of a proposed format: bit 0 supported, bit 1 no mapped channel orphaned |
| Port | `KL_pp_nvm_mgr_arb` in front of `KL_pp_nvm_port`; `m_abort` (writer to arbiter) | section 6.4. `m_abort` abandons the READ the port serves for the writer; the arbiter drains it |
| Roll-back | `rb_rst`, one strobe to every restorable owner | NEW soft-reset inputs: `KL_aecp_dyn_state` (T1), `KL_aecp_desc_store` (T2, its reset or a re-walk request: the store walks the image again and its names are the image's), and the parent's map plane (T4, stage 3). Each owner returns to its reset state |
| Entity enable | `entity_enable_i`, `restore_done_o` | the ADP engine's enable becomes `entity_enable_i AND restore_done_o`: the restore releases `entity_enable`, as F07.9 draws it |
| Exports | `nvm_unflushed_o` stays the binding manager's; new `d3_unflushed_o`, the OR of the writer's dirty bits; `nvm_alarm_o` becomes both managers' alarm; `restore_done_o`, `restore_fail_o` and `restore_blank_o` become both walks; new `restore_rb_o`, `restore_closed_o` and `rs_cause_o[2:0]` | section 8.7 |
| Parameters | the shape (`N_STREAM_IN_P` ... `N_NAME_P`, the per-port cluster counts), `LAYOUT_VER_P` shared with the binding manager, `DEB_TICKS_P` (T-NVM-DEBOUNCE), `RETRY_MAX_P`, `RS_TMO_CYC_P` (the restore deadline, section 8.8) | the record lengths follow section 4.2 of the saved-state page |

The processor's `07_memory_maps.md` section 5.3 draws the runtime commit as
"committed state change (COMMIT + NVM_MARK)" setting the record's dirty bit.
If the contract reviews accept the amendment of section 15 item 1, ticket T1
restates that figure as that item words it; if they do not, the same item
says what the mark trigger would need.

### 5.2 In the parent

`KL_pp_shadow.sv` changes three lines of glue and adds no CSR:

- `pend_i = (|nvm_unflushed_o) | d3_unflushed_o`. The `aecp_mark_pend_r` bit
  is deleted with the stage that retires its last class (section 10);
  `aecp_dyn_dirty_o` stays exported for diagnosis but leaves `pend_i`.
- `alarm_i` takes the processor's combined alarm.
- the restore outputs take the processor's combined verdicts; the blind-walk
  latch is unchanged.

With stage 3 the map plane (`milan_datapath.sv` and `KL_chan_map_capture.sv`)
takes the processor's roll-back strobe as a reset of the port sets to their
reset value, the EMPTY set.

[`REGISTER_MAP.md`](../reference/REGISTER_MAP.md) owes the PP_STAT rows for
the combined restore verdicts, and the PP_CTRL[0] and ADP_CTRL[0] rows (they
REQUEST the enable, which the restore releases), when the implementation
lands.

### 5.3 In the firmware

Three changes, not one; the evidence compiles the shipping firmware with the
first and the third (section 14).

1. `milan_init` becomes `configure_fabric`, `load_aem_image`, `nvm_boot`,
   `entity_advertise`: the AEM image moves ahead of the saved state. Two
   repository statements disagree today and this resolves them.
   `milan_init`'s comment says the saved state is restored "before the
   entity model is loaded"; `nvm_boot`'s own comment says it "Runs after
   the AEM image is in place and before the entity is advertised, the order
   Milan 5.5.3.5.2 requires" (`sw/firmware/milan_baremetal/milan_baremetal.c`
   lines 1448 and 1219). The code follows the first. D3 needs the second:
   the restore judges values against the image, and a name written back
   before the store walks the image is overwritten by it (section 8.5).
2. `nvm_boot` starts the restore walk on EVERY path. Today the path that
   finds the record set inconsistent with the generated shape returns before
   the walk. With AECP dispatch held from reset and the enable released by
   the restore, a boot that never starts the walk would leave the entity
   dark and deaf until reset. DERIVED: the model's shape always matches, so
   that path is never taken there; it is an acceptance item of T4.
3. The restore wait stays bounded, but it REPORTS and decides nothing: at
   its timeout the firmware prints that the restore has not reached its
   terminal and that the fabric holds the enable, and `entity_advertise`
   prints that it requested the enable. `entity_advertise` still writes
   PP_CTRL[0] and ADP_CTRL[0] after the wait; the restore releases them.

The ledger fact `firmware_boot_order` and the order block of
[`BAREMETAL_FIRMWARE.md`](../integration/BAREMETAL_FIRMWARE.md) move with
change 1; `scripts/check_feature_status.py` compares all three.

EXECUTED: F01_old_boot_order keeps the current order, and V1b then restores
nothing: "live (0, 0) want (1500000, 1)".

## 6. State machines and next-state functions

### 6.1 The writer in service

Service begins at the restore's COMPLETE or DEFAULTS terminal, with `own`
released; the CLOSED terminal never reaches it.

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

### 6.2 The writer at boot: the restore transaction

| State | Leaves when | To |
|---|---|---|
| reset | - | WAIT-GO, `own` 1: the state bus is the restore's from reset |
| WAIT-GO | the binding walk is done | IMAGE |
| IMAGE | the descriptor store holds a validated image, after a LOCATE of ENTITY 0 if it did not | NEXT, pass 0 |
| IMAGE | that LOCATE finds no validated image | NEXT, pass 0, with every framed record refused: nothing can be judged, so nothing applies |
| NEXT | the last record of pass 0 | NEXT, pass 1 from the first record |
| READ, STREAM | the port ends the read with the whole record | pass 0: counted whole, the next record. Pass 1: counted whole, the value rule (section 8.3), then APPLY or the next record |
| READ, STREAM | the port ends it with nothing forwarded | blank, the next record (an erased or unframed record) |
| READ, STREAM | the port ends it torn, or with err after bytes | ABORT |
| NEXT | the first name record of pass 1 | CHECK: every restored format is judged again against the final maps (section 8.4) |
| NEXT | the last record of pass 1 | FINISH when both passes counted the same records whole, else ABORT |
| a map record | the edit face refuses to give up the port's reset set, or to take it back | ABORT |
| any restore wait | `RS_TMO_CYC_P` cycles without progress | ABORT; a granted port read is abandoned to the arbiter's drain |
| ABORT | pass 0 | done and fail: nothing was applied, `own` 0 |
| ABORT | pass 1 | ROLL-BACK |
| ABORT | during the roll-back | CLOSED |
| ROLL-BACK | two cycles of `rb_rst` | RE-LOCATE |
| RE-LOCATE | the LOCATE of ENTITY 0 answers with a validated image | DEFAULTS: done, fail and rolled back, `own` 0 |
| RE-LOCATE | the LOCATE misses | CLOSED: fail, never done, `own` 1 |
| FINISH | - | COMPLETE: done, `own` 0 |

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
alarm'      = giveup ? 1 : alarm                      (sticky until reset)
d3_unflushed = OR over r of dirty[r]
pend_i      = (OR of the binding manager's unflushed sinks) OR d3_unflushed

restoring   = NOT done AND NOT closed AND the binding walk has started the restore
stall       = restoring AND the state waits AND its event did not come this cycle
wd'         = stall ? wd + 1 : 0
expire      = stall AND wd >= RS_TMO_CYC_P - 1
m_abort     = expire AND a granted port read is open
abort       = expire OR a torn or erring read OR a refused edit of a reset set
              OR (the end of pass 1 AND wholes1 != wholes0)
rolling'    = abort AND pass 1 AND NOT rolling ? 1 : rolling
rb_rst      = the two cycles after rolling rises
closed'     = (abort AND rolling) OR (RE-LOCATE misses) ? 1 : closed
done'       = FINISH OR (abort AND pass 0) OR (RE-LOCATE hits) ? 1 : done
fail'       = abort ? 1 : fail
own'        = reset ? 1 : done' ? (the service rule) : own
entity_en   = (PP_CTRL[0] OR ADP_CTRL[0]) AND restore_done
restore_done = binding walk done AND D3 done
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
drain'  = (done or err) ? 0 : (owner = writer AND m_abort) ? 1 : drain
rready  = owner = writer ? (drain OR writer rready) : owner = binding ? binding rready : 0
writer's bytes, done, err = owner = writer AND NOT drain AND the port's
```

A binding request therefore only ever meets an idle port and is issued at
once; nothing is held. A tie at an idle port goes to the binding manager.
The writer holds its request until granted. EXECUTED: K15 sweeps the
writer's release over 8 cycles against the binding manager's crc pass, and
at one of them (g3) the binding manager samples busy in the writer's grant
cycle; both records are committed at every release. A01_grant_cycle_not_busy
deletes the grant-cycle term, the binding request lands on a taken port and
is lost, and the binding never commits: "binding None, 0x50 0016e36f,
grant-cycle collisions 1".

**The drain.** The port answers untagged: its bytes and its done or err name
no operation. So an abandoned read stays OWNED by the arbiter until the port
ends it: the arbiter holds rready so every late byte can move, swallows the
bytes and the ending, and grants neither manager until then. A late response
can therefore only ever end the operation it belongs to. The drain never
ends on time: a device that never answers keeps the port drained for ever,
every later change reads pending and never durable, and bounding that is
processor issue 15 (section 15 item 4). EXECUTED in section 8.8;
D01_abandoned_read_not_drained withholds rready from the drained read, the
late response then wedges the port, and a later change never reaches a slot:
"latest 0076adf1, newest verified slot 0016e360".

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
| One change | K1 | converged@end, value_in_slot@end:0x50 | "backed 1 dirty 0 stale 0 pend 0" | M02_clear_at_latch ("durable at 533028: record 0x50 latest 0012d687 slot None"), G01_pend_misses_d3 |
| One name change | K10 | converged@end, value_in_slot@end:0x80 | the name in the newest verified slot | - |
| One map change | K12 | converged@end, value_in_slot@end:0x70 | the port's set in the newest verified slot | - |
| Every group changed, first and last index (V1a) | V1a | value_in_slot@cut for each changed record | 10 records at 1x1, 12 at 8x8, 11 at the synthetic 1x1r2 | TRG_cfg, TRG_rate (1x1r2), TRG_clks, TRG_fmti, TRG_fmto, TRG_ptof, TRG_mapi, TRG_mapo, TRG_name: each deletes one group's trigger, and its record is in no slot ("newest verified slot None") |
| A change during the record write | K2 | taint_rewrites:0x50, no_durable_claim_over_unsaved | "2 completed writes of 0x50; the last carries 0021e88e" | M01_taint_ignored ("durable at 1568748: record 0x50 latest 0021e88e slot 0010f447") |
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
| A SET waiting while the restore runs | K19 | value_in_slot@end:0x50, command_waits_for_the_restore@end | "the waiting SET was taken at [7605], the D3 terminal at 7605" | O01_own_taken_at_the_walk ("latest 001d48d7, newest verified slot 0016e360": the SET ran first and the restore overwrote it) |
| Power cut inside the processor debounce | K18a, K18b | pending_at_the_cut@cut, power_cut_loses_only_unsaved:0x50 | "pend 1, D3 unflushed 1"; "restored 1818001 ... the unsaved value 1818002" | - |
| Power cut during the record write | K17a, K17b | cut_inside_the_write@cut, power_cut_loses_only_unsaved:0x50 | "had taken 6 of 12 bytes at the cut"; "restored 1717001" | - |
| Power cut after the record, before the commit | K6a, K6b | power_cut_loses_only_unsaved:0x50 | "restored 1234567 ... the unsaved value 6000001" | - |
| Power cut after the acknowledgement | K7a, K7b | value_restored:0x50 | "restored 7000001 valid 1" | - |

Deleting a trigger reddens a case, for every group. Round one graded three
groups (the mutants M17, M18 and M19, now TRG_ptof, TRG_name and TRG_mapo);
this revision grades all nine, both format directions and both map
directions separately, each by V1a's value_in_slot check of that group's
record. This is the restatement section 15 item 1 proposes for the
saved-state page's mark acceptance.

A reset between a change and its record is a power cut here. A reset of
the fabric also resets the CPU (obligation O2), the firmware reloads the
window from the verified slot, and the processor's stores reset, so flash
is the only state carried across. The model's power cycle is exactly that:
a new process, fresh RTL and fresh firmware, with the flash array carried.

## 8. Restore

### 8.1 The order

1. `configure_fabric`. The writer has held the state bus since reset: no
   AECP program is dispatched until step 9.
2. `load_aem_image`: the AEM image in DDR, its CRC checked.
3. `nvm_boot`: both slots validated, the window loaded and the RELOAD
   accepted (the snapshot contract, unchanged), then the walk started through
   `PP_CTRL[1]`.
4. The binding manager's walk: read, validate, replay to the listener.
5. Its done starts the D3 walk.
6. If the descriptor store holds no validated image, a LOCATE of ENTITY 0
   makes it walk the one the firmware loaded.
7. Pass 0: every D3 record is read whole, or the walk aborts.
8. Pass 1: every record is read again, judged and applied or refused; the
   restored formats are judged again against the final maps; the names last.
   An abort rolls back (section 8.6).
9. Restore done, for both walks: the D3 terminal COMPLETE or DEFAULTS. The
   writer releases the state bus, and the enable bits the firmware writes
   (step 10) reach the entity. CLOSED never reaches this step.
10. `entity_advertise`: the firmware writes the enable bits. It does so after
    its bounded wait whether or not the restore is done; the fabric holds
    them until step 9.

Obligation O3 holds for the writer: it requests nothing on the device face
before the binding walk is done, its first requests are its own walk, and
its first flush follows that walk. The enable is now released by the
restore itself, so no entity enable precedes the restore of both walks
whatever the firmware's timing.

EXECUTED: V1b reads "enabled at 7613, D3 restore done at 7605, restore done
at 7605" at 1x1 and "enabled at 13895, D3 restore done at 13888" at 8x8.
G02_restore_done_without_d3 lets the processor report done after the binding
walk alone, and the entity is enabled first: "enabled at 188, D3 restore done
at 7605". G05_enable_not_released_by_restore removes the release, and the
firmware's enable after its timed-out wait reaches the entity 107,529 cycles
before the late restore ends (section 8.8, W14): "entity enabled at 3000074,
D3 terminal at 3107603".

ADP advertises nothing the restore is about to change. The ADPDU carries
the current configuration index from the dynamic state (the processor's
`04_adp_engine.md`), and no ADPDU leaves before the enable. `available_index`
is volatile, 0 at reset, and increments on every transmitted ADPDU
([`REGISTER_MAP.md`](../reference/REGISTER_MAP.md) `ADP_STATUS`), so the
first ADPDU after a power cycle already carries the restored index and no
index is spent on a value that changes. The writer holds the state bus from
reset to the restore's terminal, so no AECP program can read or write a
value before it.

### 8.2 What is proven cleared first

Issue #70's vacuity trap: "a restore that writes nothing and a store that
was never reset both pass a naive read-back". The checks close it for every
row the design restores, and read the defaults independently of the stores'
own answers.

- `rows_cleared_before_restore@boot` reads, through harness peeks and not
  through the bus the restore owns, EVERY row of selectors 0 to 5 at every
  index (value and valid flag) and every port's map set when the D3 walk
  starts, and EVERY name when its pass 1 starts, after the image walk. Each
  must be at its reset value, the model's reset set or the image's name:
  "0 rows, names or map sets not at their reset or image default before the
  restore", at every shape.
- `value_restored:<id>` for every record the slot holds, with the value AND
  the valid flag of a dynamic-state row, and the exact payload of a map set
  or a name, which must also differ from the image default;
  `unsaved_records_keep_defaults@restored` for every record it does not
  hold; and `restore_counts@boot` EXACT: "applied 10 refused 0 blank 39 of
  49; the slot holds 10" at 1x1, 12 of 145 at 8x8. Round one accepted any
  count up to the record total, so a missing application passed.
- `set_value_survives_power_cycle:0x50` compares the restored value with the
  value V1a SET, not with the slot.

V1a changes every group the shape can express, at its first and, where it
has more than one, its last index: the configuration index, the clock
source, both stream-format directions, the presentation offset, both map
directions (a narrowed stream takes the mappings that named its lost
channels with it) and the first and last names. The configuration index has
one legal value, 0, at every configuration the builder emits, so its replay
is graded by the valid flag: RPL_cfg deletes only that replay, and V1b reads
"live (0, 0) want (0, 1)". No shipped configuration lists two sampling rates,
so a legal non-default rate cannot be saved at either shipped shape; the
synthetic test configuration 1x1r2 (section 14) lists 48 kHz and 96 kHz, and
restores "live equals the slot" for 96,000 with its valid flag. Every group
has its replay-deletion mutant, killed by its own record's check:
RPL_cfg, RPL_rate (1x1r2), RPL_clks, RPL_fmti, RPL_fmto, RPL_ptof, RPL_mapi,
RPL_mapo and RPL_name.

The control, EXECUTED: V1b~stale borrows the state bus before the restore
and runs V1a's own programs with the writer's change snoop off, as stores
that were never reset would hold them. Under M13_restore_applies_nothing the
naive read-back of that store PASSES and the cleared-first check FAILS, as
the run script requires ("CONTROL stale store under M13: naive read-back
PASSES, cleared-first FAILS"). At 1x1 the check names "8 rows, names or map
sets not at their reset or image default before the restore". M13 itself is
killed by value_restored:0x50, "live (0, 0) want (1500000, 1)".

### 8.3 The value rule of each group

A record whose frame fails (magic, layout version, record id, length,
crc16) is refused and its image default stays; the walk goes on. A framed
record is applied only if its value passes the rule of the SET program that
would set it:

| Group | The SET program's rule | Refused | EXECUTED |
|---|---|---|---|
| configuration index | SET_CONFIGURATION: index below `configurations_count` (the store's region 0xD) | the image default stays | V4: "cfg row valid 0, refused 1" |
| sampling rate | SET_SAMPLING_RATE: the rate is on the AUDIO_UNIT's `sampling_rates` list, walked as the program walks it | the image default | V2: "rate row valid 0, refused 1"; M09_apply_blindly: "rate row valid 1, refused 0" |
| clock source | SET_CLOCK_SOURCE: index below `clock_sources_count` of the CLOCK_DOMAIN | the image default | V1b: value and valid flag restored |
| stream formats in and out | SET_STREAM_FORMAT: the integrator's judge, gather kind 0 selector 15 | the image default | V6b, V8, V9 (section 8.4) |
| presentation time offset | SET_STREAM_INFO: bit 31 of the latency is BAD_ARGUMENTS (`KL_aecp_engine.sv` line 3159) | the image default | V1b: first and last index restored |
| channel maps | the record's framing, then ADD_AUDIO_MAPPINGS: the integrator judges the staged set whole | the port's reset set is put back | V3 and V3a to V3g below |
| user names | SET_NAME: any 64 bytes; the empty name is a value | - | V7, V1b (section 8.5) |
| any group | the frame, the crc16 | the image default; the next record is still applied | V5: "ptof0 valid 0, refused 1" and "ptof1 1600000 valid 1" |

**The map record's framing.** A map record holds the port's set packed at
its head, then UNUSED entries up to the port's cluster count. An unused
entry is EXACTLY eight 0xFF bytes, which is what the flush writes; nothing
else is. The saved set is the entries before the first unused one, and
every one of them goes to the judge as a mapping, whatever its stream
index. An entry that is not unused, AFTER an unused one, makes the record
malformed: it is refused before the port's set is touched, and the reset set
stays. Round one called an entry unused when its FIRST byte was 0xFF, so a
mapping from stream 0xFF00 read as the end of the set and an empty set was
applied over the reset one ("refused 0, applied 1").

EXECUTED, each record for OUT port 0 beside a presentation-offset record
that must still apply, each graded on the live set and on exact counts:

| Case | The saved entries | Verdict |
|---|---|---|
| V3a | one mapping from stream 0xFF00, then unused entries | refused: "live OUT0 ... (want the default set); applied 1 refused 1 blank 47 of 49" |
| V3b | stream 0xFEFF | refused, the same counts |
| V3c | stream 0xFFFE | refused, the same counts |
| V3d | a valid mapping, unused entries, and a last entry of seven 0xFF bytes and a 0x00 | refused before the port is touched: "0 map sets staged for a malformed record" |
| V3e | an unused entry, then a valid mapping: a hole | refused before the port is touched |
| V3f | stream 2, one past the 1x1 shape's two output streams | refused, the same counts |
| V3g | every entry unused: the valid EMPTY set | applied: "live OUT0 empty (want the empty set); applied 2 refused 0" |
| V3 | a cluster past the port's clusters | refused: "live OUT0 equals the default True, refused 1" |

P01_padding_by_first_byte restores round one's rule and is killed by V3a:
"live OUT0 empty (want the default set); applied 2 refused 0".
P02_padding_holes_not_refused drops the hole rule; the judge still refuses
the record, after the port's set was removed and put back, and V3e kills it
by the staged edits: "3 map sets staged for a malformed record".

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
leaves "6 orphaned mappings". V9 refuses a map set, reverts the format paired
with it and keeps the other record the slot holds ("ptof0 1500000 valid 1,
rolled back 0"). M12_no_revert_before_readd puts the reset set back without
reverting the format first; the judge refuses the reset set, which now
ABORTS and rolls back (section 8.6) instead of leaving the port empty as it
did in round one, and V9 kills it by the refused record's neighbour, lost to
the roll-back: "ptof0 0 valid 0, rolled back 1".

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

### 8.6 The restore is a transaction

Round one read every record twice so that "a torn stream applies nothing".
That held only for a record torn AT REST, which pass 0 meets before
anything is applied. Pass 1 is another fallible read: a record pass 0 read
whole can tear, err or fall silent in pass 1, after earlier records are
applied. Both reviews showed it: a read failing in pass 1 left
"ptof0 valid 1, restore fail 1, D3 fail 1, applied 1", and the entity was
enabled over it.

This revision makes the whole D3 restore one transaction, with a roll-back
whose correctness is structural:

- **The state it restores into is the reset state.** The writer holds the
  state bus from reset until the restore's terminal, so no AECP program runs
  before or during the restore: no row, name or map is changed by anything
  but the restore. Round one's rule that "a live change made during the
  restore wins" had nothing left to act on and is removed.
- **So the roll-back is a reset.** An abort in pass 1 pulses `rb_rst`, which
  resets the dynamic-state store, the descriptor store and the parent's map
  plane (section 5.1). Each owner then holds exactly what it held before the
  restore: every row at its reset value with its valid flag clear, every
  name the image's (the descriptor store walks the image again), every
  port's reset set. Formats and maps return together, so they are
  consistent by construction. No journal of what the restore applied is
  needed, and none is kept.
- **The roll-back is proven before the entity is released.** The writer
  LOCATEs ENTITY 0, which waits out the descriptor store's walk. A
  validated image ends in DEFAULTS; a walk that cannot validate ends in
  CLOSED (section 8.8).
- **The passes must agree.** The port reports a device error during a
  header read exactly as an unframed record: err, nothing forwarded. So a
  pass-1 error on a record's header lane reads as an erased record, which
  alone would be skipped as blank. Each pass counts the records it read
  whole; a pass 1 that counts fewer (or more) than pass 0 aborts.
- **What it does not touch.** The saved state: nothing is written to the
  window or to flash by a failed restore, so the slot still holds what the
  controller last saved, and the next restore that succeeds brings it back.
  The live entity runs on defaults meanwhile, with restore fail set; the
  status can read durable over it, because every change a controller made is
  in a slot. The binding walk: the unit of atomicity for a transport
  failure is the walk, as it already is for the binding manager, which
  rejects its own walk whole. A D3 roll-back leaves a completed binding walk
  applied.

EXECUTED at 1x1 and 8x8, each on V1a's slots (every group non-default) with
one fault, then a controller's GET and SET:

| Case | The fault | What it read |
|---|---|---|
| V12 | a read error in PASS 0 on fmti0 (0x30), early | "applied 0, abort cause 2, roll-back at 0"; every record at its default |
| V13 | a read error in PASS 0 on the last name, late | the same: nothing was applied |
| V14 | a read error in PASS 1 on fmti0, after the configuration and the clock source applied | "2 records applied before the fault, roll-back at 3597"; "0 records off their defaults"; D3 done 1 fail 1 rolled back 1 |
| V15 | a read error in PASS 1 on the last name, after every scalar, format, map and the first name applied | "9 records applied before the fault"; "0 records off their defaults"; the slot kept: "11 saved records, 0 changed in the newest verified slot" |
| V16 | a read error in PASS 1 on the OUTPUT map, after the formats and the INPUT map applied | "7 records applied"; formats and maps at their defaults together |
| V18 | an error on 0x50's HEADER lane in PASS 1: the record reads as erased | "9 records applied before the fault, ... abort cause 5" (the passes disagree); every record at its default |
| V11b | the reviewers' counterexample: V11's slot, the name torn in PASS 1 after 0x50 applied | "ptof0 valid 0 after the pass-1 tear"; rolled back 1 |
| V11 | the name torn at rest: pass 0 meets it first | "applied 0, rolled back 0": nothing to roll back |

After each: the entity is enabled only at the terminal ("entity enabled at
7358, D3 terminal at 7340" in V15), no restore write follows the terminal,
the GET answers the default ("0 valid 0") and the SET persists.

The mutants: R01_no_rollback (a pass-1 abort ends without a roll-back, round
one's behaviour) is killed by V15, "9 records off their defaults ... rolled
back 0". R02, R03 and R04 each drop one owner from the roll-back: the
dynamic-state store (V15, "6 records off their defaults"), the descriptor
store (V15, "0x80 live 443320726573746f72656420 want 4d696c616e20465047412031"),
the map plane (V16). X01_passes_may_disagree drops the pass agreement and
V18 ends "D3 done 1 fail 0 rolled back 0" with 9 records applied and 0x50 at
its default: a partial restore reported as a success. M16_single_pass_restore
is killed by V11: "applied 1, rolled back 1", where pass 0 would have applied
nothing.

### 8.7 What the status says after a restore

- restore done: both walks' terminal (the D3 walk COMPLETE or DEFAULTS).
- restore fail: either walk torn or aborted (a D3 abort includes a port that
  refuses to give up or take back its reset set, and ends rolled back), or a
  blind walk (the latch `KL_pp_shadow` already keeps).
- restore blank: NEITHER walk validated a record. V7, a name back and no
  binding, reads "blank 0, done 1"; G04_blank_ignores_d3, the binding walk's
  blank alone, reads "blank 1". V10, a blank first boot, reads "blank 49 of
  49, applied 0 ... status blank 1" (145 of 145 at 8x8).
- new, on the processor's face (the PP_STAT rows are owed, section 5.2):
  rolled back (DEFAULTS), closed (CLOSED: fail, never done) and the first
  abort's cause (1 torn, 2 read error, 3 deadline, 4 edit refused, 5 the
  passes disagree).
- A restore write is not a change: "0 record writes after the restore,
  dirty 0, flash erases 0 -> 0". G03_restore_writes_are_changes taps the
  shared bus instead of the µCPU's side and commits one flash erase for
  nothing: "6 record writes after the restore, ... flash erases 0 -> 1".

### 8.8 Deadlines and containment

**The deadline.** Every wait of the restore (a port grant, a byte, a done or
err; a state-bus answer; the GET_AUDIO_MAP face; the edit face; the format
judge) is watched by one counter of consecutive cycles WITHOUT PROGRESS.
Progress is the awaited event itself, so a device that is slow but moving
never trips it. At `RS_TMO_CYC_P` the restore aborts. The model's value is
20,000 cycles, 20 ms at its 1 MHz clock; the integrator sizes it above the
descriptor store's whole walk and any single record read at the product's
clock (section 15 item 8). Only the restore is watched: in service the
writer holds the state bus only across on-chip faces (section 12's latch
windows), and a flush that waits on the port holds nothing but its record's
dirty bit.

**The abandoned read.** An abort while the port serves the writer's read
raises `m_abort`, and the arbiter DRAINS that read (section 6.4). The
writer never looks at it again: its bytes and its ending reach no manager,
and no new operation is granted until the device ends it. This is the
containment protocol for an untagged port; nothing here assumes the port can
be reused before the device answers, and a device that never answers keeps
it drained for ever (section 15 item 4).

**The terminals.**

| Terminal | Reached by | done | fail | `own` | The entity |
|---|---|---|---|---|---|
| COMPLETE | pass 1 ended, the passes agree | 1 | 0 | released | enabled at done |
| DEFAULTS | an abort in pass 0, or a pass-1 abort rolled back and the image walked | 1 | 1 | released | enabled at done, on defaults |
| CLOSED | a roll-back that cannot validate the image, or an abort during the roll-back | never | 1 | kept for ever | never enabled; no AECP program runs; only a reset leaves |

**The enable.** The restore releases it (section 8.1). The firmware's wait
decides nothing: when it times out, the firmware reports and writes the
enable, and the fabric holds that enable until done. So no restore write
can follow the enable: every restore write precedes the terminal, and the
enable follows it.

**The binding walk.** `KL_acmp_nvm_shadow` keeps no deadline of its own, and
this contract does not add one (processor issue 15). A device that never
answers during that walk keeps the restore short of done: the entity stays
dark and AECP stays held. That is fail-closed, never an early enable; a late
answer completes the walk and the D3 restore then runs as usual.

EXECUTED at 1x1, and the D3 cases at 8x8 as well, each on V1a's slots unless
named, each followed by a controller's GET and SET:

| Case | What was held | What it read |
|---|---|---|
| W1 | pass 0: the first memory read of fmti0, for ever | "held from 955, released 0, abort cause 3"; "stall began at 955, D3 terminal at 20955"; nothing applied; the later SET "pend 1, port busy 1": the drained read never ends |
| W2 | pass 0: released when the deadline was 40 cycles away | "the watchdog reached 19960 of 20000, abort cause 0"; the restore COMPLETE |
| W3 | pass 0: released 5 cycles after the deadline | "the writer aborted at 20954, the response came at 20959"; the drain took it, and the later SET persists |
| W4 | pass 1: fmti0, for ever | "stall began at 3544, D3 terminal at 24201"; rolled back to defaults |
| W5 | pass 1: released 40 cycles before the deadline | "the watchdog reached 19960 of 20000"; COMPLETE |
| W6 | pass 1: released 5 cycles after the deadline | "the writer aborted at 23543, the response came at 23548"; rolled back; the later SET persists |
| W7 | pass 1: the last name, for ever | "stall began at 6512, D3 terminal at 27154"; rolled back |
| W8, W9, W10 | pass 1: the GET_AUDIO_MAP face, the format judge, the edit face silent | each "abort cause 3", the terminal at most 20,666 cycles after the face fell silent, rolled back |
| W11 | R217's counterexample: V11's slot, the first D3 read 3,500,000 cycles late | "held from 781 to 3500781"; "D3 terminal at 20781", "entity enabled at 20798"; the late response drained; the later SET persists |
| W12 | R218's counterexample: a pass-1 read after records applied, 3,100,000 cycles late | "D3 terminal at 24201", "entity enabled at 24218"; rolled back; the response drained at 3103544 |
| W13 | the BINDING walk's first read, for ever | "restore done 0, entity enabled 0 (first 0), firmware asked at 3000074 and reported the timeout True, own 1, a GET answered None" |
| W14 | the binding walk's read, released at 3,100,000, after the firmware's 3,000 ms wait | "the firmware's wait timed out True, asked for the enable at 3000074, restore done at 3107603"; "entity enabled at 3107603"; the restore COMPLETE |
| W15 | the binding walk's read, released at 2,900,000, before the firmware's wait ends | "timed out False"; "entity enabled at 2907615"; COMPLETE |
| V17 | V15, and the descriptor memory fails from the roll-back on | CLOSED: "closed 1, restore done 0 fail 1, own 1, entity enabled 0 ... firmware asked at 3000074, a GET answered None" |

Every case above that reaches done also passes
entity_enabled_after_terminal@boot and no_restore_write_after_terminal. The
later SET persists wherever the port is free, and reads pending, never
durable, where a drained read never ends (W1, W4, W7); the GET after
recovery is graded wherever the restore ended on defaults.

W01_no_restore_watchdog is killed by W4: "D3 terminal at 0".
D01_abandoned_read_not_drained by W6 (section 6.4).
G05_enable_not_released_by_restore by W14 (section 8.1).
R05_closed_releases_the_entity lets CLOSED release the bus and report done,
and V17 kills it: "closed 0, restore done 1 ... entity enabled 1".
O01_own_taken_at_the_walk takes the bus at the walk instead of at reset, and
K19 kills it (section 7.2).

## 9. What must not persist

| State | Clause, as the repository quotes it | Where it lives | Why nothing here can persist it | Evidence |
|---|---|---|---|---|
| Lock state and the locking controller | Milan v1.2 5.3.4.1, volatile (the processor's `07_memory_maps.md` section 5.1) | `KL_aecp_notify` | not on the state bus, no trigger decodes it, and the allocation gives it no record id | DERIVED, structural; an acceptance item of the implementation |
| The registered-controller list | 5.3.4.2, volatile (same table) | `KL_aecp_notify` | the same | DERIVED, structural; the same acceptance item |
| The IDENTIFY value | 5.3.12: "0 = not identifying" is the reset default (`KL_aecp_dyn_state`'s banner) | `KL_aecp_dyn_state` selector 7 | the trigger decodes selectors 0 to 5; the store raises no dirty for it; SET_CONTROL carries no commit mark; a roll-back resets it to 0 with the rest of the store | EXECUTED K14; M06 killed |
| Started or stopped | persisted, but in the BINDING record (5.3.8.7) | the listener's binding record | selector 6 is retired | the binding manager's own suites |
| System unique id, media clock reference | allocated as design-affirmative items | nothing writes them | no trigger and no slot in the writer | they stay erased records |

The saved-state page's acceptance already names the check the
implementation owes: "The volatile set does NOT survive: after restore the
lock is clear, the controller registry is empty, IDENTIFY is 0"
([section 16](SAVED_STATE_FASTCONNECT.md#16-acceptance-for-the-implementation)).

## 10. Stages

Each stage is proved alone on silicon: set the values from a controller
host, read the status to durable, remove power at the outlet for 8 s (a cold
cycle, as the binding proof of 2026-09-21 did), and read every value back
with GET commands. Each also sets IDENTIFY and proves it comes back 0. The
ticket texts are drafted beside this page's evidence (the tickets path
above).

**Release conditions**, as recorded on #500 when this revision was taken.
They add gates, and change no allocation:

- **No stage is declared shippable before #502 is closed.** A shipped
  stage's proof reads the status durable, and until names and maps are
  materialized that reading can be false over them for a program's tail
  (section 2). The correction is #502's standalone one: the live-write
  trigger feeding the parent's pending bit from the first accepted write,
  for both classes. Filing #502 does not close it; the correction must land.
- **Stage 3 is BLOCKED on #501.** At 8x8 a legal accepted output set can
  outgrow its record, and the pending-and-skip rule of section 3 (rule 9)
  keeps the status honest about it without persisting it. Stage 3's
  implementation lane does not open until #501 records a conforming
  allocation or accepted-mapping limit with its protocol consequence. This
  page does not change the decided allocation and does not accept permanent
  pending as conformance.
- **Work that may proceed while those are open:** stages 1 and 2 may be
  implemented and merged, and released only after #502; #502's correction
  itself; design-level evidence for maps at 1x1, where every legal output
  set fits its record (16 stream channels, 17 entries). Not before #501: a
  stage-3 lane, a stage-3 release, or any claim of 8x8 map persistence.
- **Stated in every stage's release notes:** a silent device during the
  BINDING walk keeps the entity dark and deaf until processor issue 15 gives
  that walk a deadline (section 8.8). It is fail-closed, never an early
  enable, and no stage waits for issue 15.

| Stage | Records | What lands | Silicon proof | Tickets |
|---|---|---|---|---|
| 1. the dynamic-state selectors | configuration index, sampling rate, clock source, stream formats, presentation offset: 9 records at 1x1, 30 at 8x8 | the writer with the state-bus trigger, `own` from reset, the flush, the restore transaction with its deadline and the dynamic-state store's roll-back, the format rule on "supported"; the arbiter and its drain; the enable released by the restore; the exports; `pend_i` loses the dynamic-state level; the three firmware changes | SET_CLOCK_SOURCE 1, SET_STREAM_INFO, SET_STREAM_FORMAT on an unbound input; power cycle; GET_CLOCK_SOURCE, GET_STREAM_INFO, GET_STREAM_FORMAT, and the ADPDU's configuration index | T1 (processor), T4 (this repository); released after #502 |
| 2. names | 38 at 1x1, 99 at 8x8 | the name trigger, the eight-lane latch, the restore after the image walk, the descriptor store's roll-back; `pend_i` stops taking class 7 | SET_NAME on the entity name, the group name and a stream name, one of them to the EMPTY name; power cycle; GET_NAME | T2, T4; released after #502 |
| 3. channel maps | 2 at 1x1, 16 at 8x8 | BLOCKED on #501. Once unblocked: the edit-face trigger, the GET_AUDIO_MAP latch, the framing rule, the coupled restore, the map plane's roll-back, #501's capacity decision; the sticky class-6/7 bit is deleted | ADD and REMOVE on both ports; power cycle; GET_AUDIO_MAP | T3, T4, #501 |

Stage 1 restores formats while the maps still reset: the maps come back
empty, so nothing restored can be orphaned. Both shipped shapes list one
sampling rate, so the rate record can only be proved at its default on the
board; V2 covers its refusal and the synthetic 1x1r2 its replay. Until stage
3 the class-6 bit stays in `pend_i`, and until stage 2 the class-7 one,
unless #502's correction has already replaced them.

The area of each stage is a subset of section 12's row; each lane owes its
own post-place delta by the saved-state page's recipe, at both shipped
shapes.

Further tickets, not stages: T5 is #501; T6 is #502; T7, the saved-state
page's area table (recorded on #495); T8, an addendum to processor issue 15
naming what a port deadline must do for this contract.

## 11. Alternatives rejected

| Alternative | Rejected because | Evidence |
|---|---|---|
| (a) A manager per group, in the image of `KL_acmp_nvm_shadow` | the reference replication costs three to four times the LUT of (b) and one to three RAMB36 on a device whose binding constraint is block RAM; seven debounces, seven retries and seven restore walks to grade | reference replication estimate, section 4 |
| (c) The firmware materializes the records from CSR reads | D3 records would never cross the device face, so a second ownership mechanism, on a larger control face, must carry the clear rule beside the accepted contract; the firmware becomes a writer of processor state; the framing and the value rules move into firmware; the donor's F07.9 must be amended. Its measured fabric proxy is smaller by 1,781 LUT at 1x1 and 1,245 at 8x8, excluding firmware and integration costs | measured proxy, section 4 |
| Triggering on the commit marks, as the tracked glue does | the marks follow the live write by the program's tail, so the status reads durable over an applied name or map | EXECUTED on the tracked glue, section 2 |
| A shadow of every record inside (b) | 2,432 bytes of names at 1x1 and 6,336 at 8x8 alone; the live value is readable at flush, and latching it costs at most 179 cycles of dispatch hold-off | the (a) shadow rows, section 4; latch windows, section 12 |
| Staging every record before applying any, so a failed read applies nothing | the same shadow: one to three RAMB36 of names and maps held only for the restore. The roll-back gets the same outcome from resets the owners already have | section 8.6 |
| Rolling back by undoing each applied record | needs the pre-restore value of every record, which nobody keeps. Holding the state bus from reset makes that value the reset state, so a reset is the exact undo | section 8.6 |
| Latching without the dispatch hold-off | a SET in progress is latched half old, half new | EXECUTED: M05 is killed by K11 |
| Taking the state bus at the walk and letting a change made before it win (round one) | such a change survives the restore but not a roll-back: the reset would erase it while its record stayed dirty, and the writer would then save the default over it. Holding the bus from reset leaves no such change to protect | EXECUTED: O01 takes the bus at the walk without round one's rule, the waiting SET runs first and the restore overwrites it, and K19 kills it |
| A single restore pass | a record torn at rest is applied up to the tear and must be rolled back; pass 0 refuses it before anything is applied | EXECUTED: M16 is killed by V11 |
| Two passes without a roll-back (round one) | pass 1 is another fallible read | EXECUTED: R01 is killed by V15; the reviewers' V11b |
| A firmware deadline that enables the entity (round one) | a late restore then changes an enabled entity, and a silent one keeps the bus for ever | EXECUTED: G05 is killed by W14; W11, W12 |
| Aborting the port by releasing its owner at the deadline | the port answers untagged: a late byte or done would be taken by the next operation | the drain, section 6.4; D01 is killed by W6 |
| Keeping the entity enable in firmware and gating it there | the restore is the only party that knows when no restore write can follow; a firmware gate is one timeout away from round one's defect | section 8.8 |
| An alarm on an oversized map set (the evidence's first rule) | the alarm is sticky, so one oversized set would revoke `nvm_backed` for every record until reset | replaced by the pending-and-skip rule; K16 |
| Forgetting or truncating an oversized set | a durable reading over a set no slot holds | EXECUTED: M15 is killed by K16 |
| Restoring by replaying SET commands through the µCPU | it would reuse the programs' own rules, but needs a command path into the dispatch queue with its responses suppressed; not costed | UNRESOLVED 7 |
| The held-request path in the arbiter | unreachable under the rule of section 6.4, so no case can fail it | the evidence's first mutant A01 survived; the path is removed |
| Growing each output map record to the stream-channel key space | it changes the decided allocation, which is not this page's to change | #501 (section 10) |

The round-one table listed "Gating the entity enable on restore done in
hardware" as rejected, because the port has no timeout. The writer's own
deadline removes that reason for the D3 walk, and the binding walk's
remaining silence is exactly the case in which fail-closed is the honest
answer. It is section 3's rule 8 now.

## 12. Cost

MEASURED, out of context (section 4's recipe and calibration), re-run for
this revision. LUT is the LUT-equivalent total. These are estimates of the
prototypes, not bounds on an integrated implementation.

| Block | 1x1 LUT | 1x1 FF | 8x8 LUT | 8x8 FF | RAMB36 | DSP |
|---|---|---|---|---|---|---|
| the writer, with DSP mapping | 2,225 | 859 | 2,828 | 984 | 0 | 0 |
| the writer, without DSP | 2,263 | 859 | 2,785 | 984 | 0 | 0 |
| the arbiter, with its drain | 48 | 3 | 48 | 3 | 0 | 0 |
| **(b), worst column** | **2,311** | **862** | **2,876** | **987** | **0** | **0** |
| for scale: the binding manager | 1,040 | 1,081 | 1,119 | 1,123 | 0 | 0 |
| for scale: `KL_pp_nvm_port` | 197 | 116 | 197 | 116 | 0 | 0 |
| for scale: `KL_nvm_backend` | 1,051 | 476 | 1,476 | 515 | 0 | 6 |

Round one measured (b) at 2,312 LUT and 802 FF at 1x1 and 2,925 LUT and 927
FF at 8x8. The flops grow by 60: 59 in the writer (the 32-bit deadline
counter, the two 8-bit record counters and the transaction's flags) and the
drain's one in the arbiter. The LUT total moves by -1 and -49: removing
round one's unreachable "live change wins" branch removed a multiplexer over
every dirty bit, and differences of tens of LUT between mappings of one
design are usual here (the DSP and no-DSP rows differ by 38 and 43). The
honest reading is about the same LUT and 60 more flops.

DERIVED: the seams of section 5.1 (a 2:1 selection over the state bus and
the two map faces, about 250 signals) add a few hundred LUT at most; the
roll-back reset inputs and the enable gate are one gate each per owner. No
block RAM and no main memory is added; the records use the window the
saved-state page already sized.

The saved-state page's area table lists 772 LUT and 377 FF for
`KL_nvm_backend` at 1x1 with 30 names. That row predates the #484 contract:
both recipes return 1,030 LUT and 468 FF for the same parameters at the
current source. Ticket T7 records it.

Time, EXECUTED in model cycles of the processor clock: the dispatch hold-off
of a latch lasts 10 cycles for a scalar, 114 for a name, and at most 179 for
a port's map at 1x1 and 115 at 8x8. The whole boot restore, both walks,
ends by cycle 7,605 after reset at 1x1 and 13,888 at 8x8 (V1b, which now
restores every group), and the entity is enabled 8 and 7 cycles later. A
restore that meets a silent wait ends within the deadline plus its
roll-back: 20,657 cycles after the stall began in W4. The model's memory
answers in 2 or 3 cycles; the product's in about 1.4 µs, so every figure
grows on the board (UNRESOLVED 8).

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
- A D3 restore is all or nothing against a transport failure in either pass:
  complete, or every D3 group at its default with restore fail set. It is
  per record against a bad frame or a refused value.
- A failed restore never rewrites the saved state: the slot still holds what
  the controller last saved, and the next successful restore brings it back.
- The entity is enabled only when the restore of both walks is done. A
  restore that cannot finish keeps the entity dark (fail-closed): a D3
  roll-back that cannot prove the image walked, or a binding walk whose
  device never answers until processor issue 15 bounds it.
- No AECP program runs from reset until the restore's terminal. A command
  that arrives in that interval waits in the dispatch; before the entity is
  enabled no controller has been told the entity exists.
- An AECP command can wait for one latch window, at most 179 cycles in the
  model, before its program is dispatched.
- The port serves two managers. A binding request can wait for one D3 record
  operation, and the binding manager is otherwise unchanged. A read the D3
  writer abandons keeps the port until its device answers.
- The processor's restore verdicts mean both walks; the PP_STAT and PP_CTRL
  rows of [`REGISTER_MAP.md`](../reference/REGISTER_MAP.md) owe the update.
  A bench script that writes the enable without starting the restore walk
  now finds the entity dark.
- `milan_init`'s order changes, and with it the ledger fact
  `firmware_boot_order` and the order block of
  [`BAREMETAL_FIRMWARE.md`](../integration/BAREMETAL_FIRMWARE.md); `nvm_boot`
  starts the walk on every path.
- An output map set larger than its record stays pending until it shrinks,
  which is containment, not persistence; stage 3 waits for #501.
- The value rules exist twice, in the programs and in the writer
  (UNRESOLVED 7).
- The writer's alarm is sticky like the binding manager's, and joins its
  revocation of `nvm_backed`.
- Lock, registry and IDENTIFY stay volatile.
- Obligations O1 to O4 of the snapshot contract are unchanged. The writer
  is one more producer behind the one device-face initiator, arbitrated
  explicitly, and neither it nor the drain writes the control face. An
  implementation lane inherits all four.

## 14. The executable model and its omissions

- ONE process per build, one clock. REAL at the pinned processor: the
  dynamic-state store, the descriptor store walking a real AEMI image of the
  shape, the binding manager and the port. SHIPPING: `KL_nvm_backend.sv`,
  and the firmware `milan_baremetal.c` compiled for the host through its two
  CSR primitives, with firmware changes 1 and 3 of section 5.3 as counted
  substitutions. PROTOTYPE: the writer and the arbiter. TRANSCRIBED: the
  parent glue of `KL_pp_shadow.sv` with the enable the restore releases,
  and under `D3_TRACKED` the glue as it ships.
- MODELS, each stated where it is coded: the µCPU is a bus-functional model
  running programs as state-bus operations, with the dispatch hold-off and
  the commit marks after the write; the parent's map plane is C++, keyed as
  `milan_datapath.sv` keys it (an input mapping by cluster, an output
  mapping by stream channel owned by one port); the format judge's
  "supported" rule is a model of the integrator's; the edit face is one
  staged set, where the product has phases 0 to 5.
- THE ROLL-BACK'S OWNERS are modelled by their resets: the model drives the
  pinned stores' own `rst_n` from the writer's strobe, and the C++ map plane
  returns its ports to their reset sets. The product needs one soft-reset
  input per owner (section 5.1); a store-local re-walk request would serve
  the descriptor store equally.
- HARNESS-ONLY FACES, never product wiring: peeks that read every
  dynamic-state row and the name table through the hierarchy for the
  cleared-first and roll-back checks; a knob that lends the state bus to the
  stale-store control before the restore; the change-snoop knob; and the
  fault injection: memory reads that fail, are held back for a count or for
  ever, or are released relative to the writer's deadline; faces made
  silent; a descriptor memory made to fail.
- The model's reset map set is non-empty (the first clusters of each port on
  the first channels of one stream), where the shipping dynamic ports reset
  to empty. That exercises every step of section 8.4; it is not the
  product's default. It also has a limit: restoring port after port, a saved
  set that takes a stream channel a LATER port's reset set still owns is
  refused. The shipped empty reset sets cannot conflict that way; a
  non-empty one would need every reset set removed first (ticket T5, for
  #501).
- SHAPES: the two shipped configurations, and one SYNTHETIC test
  configuration, 1x1r2, derived at prep time from the 1x1 one with its
  AUDIO_UNIT listing 48 kHz and 96 kHz. The builder accepts it and marks the
  second rate planned. It runs V1a, V1b, V1b~stale, V2 and the two
  sampling-rate mutants; it is not a shipping fact.
- Time: the model clock is 1 MHz; the hold, the debounces, the deadlines and
  the heartbeat are counted in it. The CPU's instructions take no model
  time; DDR answers in 2 or 3 cycles; the flash is the host model. No
  hardware ran.
- Not modelled: the real microprograms' timing (the mark tail is DERIVED
  from `gen_ucode.py`), the product's GET_AUDIO_MAP hold of two cycles a
  beat, real flash, placement, and firmware change 2 (the model's shape
  always matches).
- THE RUNNER'S VERDICT IS ITS EXIT STATUS. `run.py run` exits 0 only with no
  verdict failure, 1 with each failure named, 2 when a build is missing or
  unknown; a planned case that did not run is a failure; a mutant counts as
  killed only by its named check in a run that COMPLETED. With no build
  named it is the FULL run and writes the results beside it; naming builds
  makes it a FOCUSED run, which says so and writes elsewhere. `run.py
  controls` proves it on doctored copies of the built binaries, through the
  real CLI, each against its exit status and diagnostic: a healthy binary in
  place of M01 ("MUTANT M01_taint_ignored: SURVIVED", exit 1); an executable
  that fails before its scenario in place of M06 ("NOT COMPLETED", exit 1,
  where round one counted it killed); a failed baseline, the 1x1r2 base
  running RPL_rate's binary ("UNEXPECTED base-1x1r2 V1b_restore_everything
  value_restored:0x02 FAIL", exit 1); the tracked build replaced by the
  prototype ("TRACKED K1_single_change_converges : converged@end DOES NOT
  FAIL", exit 1); the stale seeding removed under M13 ("CONTROL ... NOT AS
  REQUIRED", exit 1); an absent tracked build ("REFUSED: tracked-1x1 is not
  built", exit 2); an empty selection (exit 2). All seven as required.
- TOTALS: 55 builds (the two shipped shapes, the synthetic shape, the
  tracked glue and 51 mutants), 230 graded runs, 2,524 graded checks, 0
  verdict failures, exit 0, from an empty output tree. Every one of the 51
  mutants is killed by the one check the run script names for it, in a
  completed run; the vacuity control holds; the K15 premise is reached; the
  tracked glue fails its 7 named checks and passes its 4. The command record
  lists every command with its real exit status, and the sha256 of every
  file the evidence commit tracks and of the 14 repository files the model
  reads.

## 15. UNRESOLVED

1. **AMENDMENT REQUESTED: the trigger is the live write, not the commit
   mark.** Both reviews support it in principle; it is not adopted until
   the contract acceptance records it, and this page edits none of the
   wording below. Adopting it changes exactly:
   - [`SAVED_STATE_FASTCONNECT.md` section 16](SAVED_STATE_FASTCONNECT.md#16-acceptance-for-the-implementation),
     "The marks", first bullet, now "Each of the **eight** marks in section
     12.1 is graded end to end: deleting it alone must redden a save/restore
     test. Both stream-format placements count separately, and the mapping,
     presentation-offset and name marks are included." Proposed: "Each
     persisted group's live-write TRIGGER is graded end to end: deleting it
     alone must redden a save/restore test. The groups are the
     configuration index, the sampling rate, the clock source, the stream
     format in, the stream format out, the presentation time offset, the
     channel map in, the channel map out and the user names; both format
     directions and both map directions count separately."
   - The same list, second bullet, now "Deleting the mark's **absence** at
     `SET_CONTROL`, that is adding one, must also redden something".
     Proposed: "Adding IDENTIFY (selector 7) to the trigger must also redden
     something: 5.3.12 requires IDENTIFY to stay volatile."
   - The same page, "The status bits", the bullet "A power cut inside the
     debounce window loses exactly the marked changes, and `nvm_dirty` said
     so beforehand". Proposed: "... loses exactly the changes the pending
     bit (inside the writer's debounce) or `nvm_dirty` (inside the
     firmware's) reported beforehand."
   - The same page,
     [section 12.2](SAVED_STATE_FASTCONNECT.md#122-where-they-go-today),
     "mapping a class plus the program's descriptor index onto section 4's
     allocation is the missing manager's job". Proposed: the manager decodes
     the live write, and the marks stay for notification only.
   - [`SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 13](SAVED_STATE_SNAPSHOT_OWNERSHIP.md#13-donor-dependencies-each-its-own-scope),
     D2, "Parent use: a mark of class 6 or class 7 sets a sticky pend_i
     source until the record that materializes it is written". Proposed:
     retired stage by stage as section 10 retires each class.
   - The processor's `07_memory_maps.md` F07.9: the node "committed state
     change (COMMIT + NVM_MARK)" becomes "accepted live write of a persisted
     field (state-bus write, name-table write, map edit commit beat)"; "clear
     dirty" becomes "clear dirty on an untainted done"; and the boot restore
     gains the transaction of section 8.6 before "release entity_enable".
     Ticket T1 carries that edit once the amendment is recorded.

   What replaces the mark acceptance, EXECUTED: for each of the nine groups,
   deleting its trigger alone (TRG_*) fails V1a's value_in_slot check of
   that group's record, and deleting its replay alone (RPL_*) fails V1b's
   value_restored check of it (sections 7.2 and 8.2). The reasons for the
   amendment: a mark trigger reads durable over an applied change for the
   program's tail (EXECUTED on today's glue, section 2), and the class-1
   mark cannot name its record. If the reviews keep the mark, the mark must
   carry the opcode and the descriptor so it can name a record, and the tail
   window must be accepted and stated.
2. **An output map set can outgrow its record at 8x8** (#501, open). The
   allocation gives a map record 8 bytes a cluster; an output mapping is
   keyed by stream channel, so at 8x8 a port has 9 entries against 72
   stream channels. This design keeps such a set pending and never writes it
   in part (K16), which is containment only. Stage 3 is blocked on #501's
   decision (section 10).
3. **The mark-tail window of today's glue** (#502, open): the status reads
   durable over an applied name or map for a program's tail. Every stage
   declared shippable waits for its correction (section 10).
4. **The port has no deadline** (processor issue 15, open; ticket T8 names
   what this contract needs from it). The D3 restore is contained without
   it. Without it the binding walk is unbounded, so a silent device there
   keeps the entity dark; and a read the D3 writer abandoned keeps the port
   until its device answers, so a device that never does leaves every later
   change pending for ever.
5. **The port reports a device error during a header read as an unframed
   record.** Both end in one err with nothing forwarded. The pass agreement
   of section 8.6 catches a pass-1 occurrence; an error that recurs on the
   same header lane in both passes reads as an erased record, and that
   record restores its default without a failure verdict. Telling the two
   apart is part of T8.
6. **Two debounces.** The writer uses the binding manager's T-NVM-DEBOUNCE
   and the firmware adds its own 1,000 ms. The value of T-NVM-DEBOUNCE is
   still open
   ([section 14](SAVED_STATE_FASTCONNECT.md#14-what-this-page-does-not-decide)).
   A shorter writer debounce costs only port writes to main memory.
7. **The value rules exist twice**, in the programs and in the writer, and
   can diverge. Replaying the records as SET commands through the µCPU would
   remove the copy; it is not costed here.
8. **Time on the board.** The latch windows, the restore time and the
   deadline are model cycles; the product's memory latency and GET_AUDIO_MAP
   hold are not measured, and `RS_TMO_CYC_P` at the product clock is a
   proposal (20 ms), to be sized above the descriptor store's whole walk.
9. **Area in context.** The rows are out-of-context measurements and proxy
   estimates. Each stage owes its post-place delta at both shapes.
10. **System unique id and media clock reference** have allocated records
    and no source; nothing here writes them.
11. **An edit that changes nothing** still raises commit beats, so its port's
    record is written again for nothing; the program's FINISH knows, the
    trigger does not.
12. **The writer's alarm is sticky until reset**, as the binding manager's
    is; the snapshot page's UNRESOLVED 7 (forgiveness) covers it too.
13. **Commands before the restore's terminal wait.** Bounded by the D3
    deadline once the binding walk is done; unbounded while a silent binding
    walk holds (item 4).

## 16. Traceability

Milan v1.2 clauses, as the saved-state page lists them
([section 4.1](SAVED_STATE_FASTCONNECT.md#41-what-the-persisted-set-actually-needs)):

| Clause | Item | Records | Where | Executed by |
|---|---|---|---|---|
| 5.3.5.1 | sampling rate | `0x02`.. | 3, 8.3, 10 | V2, V1b at 1x1r2 (synthetic) |
| 5.3.7.1 | Stream Output format | `0x40`.. | 3, 8.3, 8.4, 10 | V1b, V6b, V8, V9 |
| 5.3.7.6 | presentation time offset | `0x50`.. | 3, 7, 8.3, 10 | K1 to K9, K17, K18, V1b, V5 |
| 5.3.8.1 | Stream Input format | `0x30`.. | 3, 8.3, 8.4, 10 | V1b |
| 5.3.8.2, 5.3.8.3, 5.3.8.7 | bound state, binding parameters, started or stopped | `0x20`.. | the binding manager, unchanged; 6.4 | K13, K15 |
| 5.3.9.1, 5.3.10.1 | channel mappings in and out | `0x60` to `0x7F` | 3, 7, 8.3, 8.4, 10 | K12, K16 (containment only; #501), V1b, V3 to V3g |
| 5.3.11.1 | clock source | `0x0A`.. | 3, 8.3, 10 | K4g, V1b |
| 5.3.13 | user names | `0x80`.. | 3, 8.5, 10 | K10, K11, V7, V1b |
| design-affirmative | configuration index | `0x00` | 3, 8.1, 8.3, 10 | V4, V1b (the valid flag) |
| 5.3.4.1, 5.3.4.2, 5.3.12 | lock, registry, IDENTIFY: must NOT persist | - | 9 | K14 |

The saved-state acceptance as the repository quotes it
([section 16](SAVED_STATE_FASTCONNECT.md#16-acceptance-for-the-implementation)),
the items this design answers:

| Item | Here | Stays with |
|---|---|---|
| "All eight Milan items plus the bound state, the binding parameters and started/stopped survive a reset that is proven to have cleared the rows first" | 8.2, 10 | each stage's silicon proof; maps at 8x8 after #501 |
| "The volatile set does NOT survive: after restore the lock is clear, the controller registry is empty, IDENTIFY is 0" | 9 | the implementation's suite |
| "A user name SET to the EMPTY string survives a power cycle as the empty string" | 8.3, 10 (stage 2) | stage 2 |
| "Each of the eight marks in section 12.1 is graded end to end: deleting it alone must redden a save/restore test" | 3 (rule 3), 7.2, 15 (item 1) | AMENDMENT REQUESTED. Under this design deleting a mark reddens nothing, because the trigger is the write; the item would be restated as deleting each group's TRIGGER, nine groups, each EXECUTED. The IDENTIFY half, adding a mark to SET_CONTROL, is kept in spirit: M06 adds IDENTIFY to the trigger and is killed |
| "The manager emits records at the section 4.2 ids, and a record whose id is outside its group's block is refused rather than written" | 3 (rule 1), 8.3 | the implementation's suite |
| "A power cut inside the debounce window loses exactly the marked changes, and `nvm_dirty` said so beforehand" | 7.2 (K18), 15 (item 1) | silicon. Inside the WRITER's debounce it is the pending bit that says so ("pend 1, D3 unflushed 1"); `nvm_dirty` says so inside the firmware's |

Issue #500's five items: who and where, section 4; the trigger and the clear
rule, sections 6 and 7; restore, section 8; what must not persist, section
9; stages, section 10.

The round-one review findings at `d0256846`, with the reviewers' own
severities and lenses. Answering a finding here is not clearing it: each
reviewer re-reviews the new heads and decides.

| Finding | Severity and lenses | Answer | Evidence |
|---|---|---|---|
| R217 F1, R218 F1: two passes do not make restore all-or-nothing | MAJOR; Conformance, RTL, Robustness, Tests, Docs (both) | the restore transaction: roll-back by reset, the pass agreement, `own` from reset (3 rule 7, 6.2, 6.3, 8.6) | V11b, V12 to V16, V18 at 1x1 and 8x8; R01 to R04, X01, M16 |
| R217 F2, R218 F2: the firmware timeout enables the entity without containing the restore | MAJOR; Conformance, RTL, Robustness, Tests, Docs (both) | the deadline, the drain, the three terminals, the enable released by the restore, the binding walk fail-closed, processor issue 15 named (3 rules 5 and 8, 5.1, 5.3, 6.4, 8.1, 8.8, 15 items 4 and 13) | W1 to W15, V17, K19; W01, D01, G05, R05, O01 |
| R217 F3: invalid map entries can bypass the value refusal | MAJOR; Conformance, RTL, Robustness, Tests, Docs | the exact unused entry and the hole rule (8.3) | V3a to V3g; P01, P02 |
| R217 F4, R218 F5: permanent pending is still an accepted Stage 3 outcome; the stage release conditions do not exclude the open defects | MAJOR; R217 Conformance, RTL, Robustness, Docs; R218 Conformance, Robustness, Tests, Docs | Stage 3 blocked on #501, every stage declared shippable after #502, pending-and-skip is containment only, the limited work named (3 rule 9, 10, 15 items 2 and 3; T3 to T6). #501 and #502 stay OPEN | K16 (containment only) |
| R217 F5: the evidence runner does not fail its process verdict | MINOR; Tests, Docs | exit statuses, completed-run kills, full and focused runs (14) | the seven process controls |
| R218 F3: the runner accepts surviving mutants and failed scenarios | MAJOR; Tests, Docs | the same | the same |
| R218 F4: configuration replay can be deleted without invalidating the evidence | MAJOR; Conformance, Tests, Docs | value AND valid flag for every group and first and last index, exact counts, cleared-first by peeks for every row, name and map, the synthetic two-rate shape (8.2, 14) | V1a, V1b at three shapes; TRG and RPL, nine groups each |
