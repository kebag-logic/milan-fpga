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
> **Revision d** answers the round-three contract reviews of this page at
> `ab0fb23f` (R217 and R218, both NEGATIVE, each finding MAJOR under all
> five lenses). Both answers are prerequisites of stage 1 and of every
> shippable stage (section 10):
>
> - **S4**, the listener's boot-owned admission: from the hard reset to the
>   binding walk's drained terminal, the pinned ACMP listener is offered
>   nothing but the binding restore's preloads. A held talker event, a
>   transaction, a timer expiry or a START/STOP request no longer holds the
>   preload phase, and a read-only command no longer withdraws a restored
>   binding (sections 5.1 and 8.9). Its release is one of three separate
>   release points, each stated with what runs from it: the listener's live
>   ACMP work from S4's release, AECP from the D3 terminal, ADP advertising
>   from the combined enable (section 8.1).
> - **The descriptor store's roll-back reset belongs to stage 1**, not
>   stage 2: after a fetch's response timed out, the pinned store's next
>   fetch errs at once, and the roll-back's one LOCATE is that fetch unless
>   the store's reset re-arms the watchdog first (sections 8.6 and 10).
>
> The seams revision c added stay prerequisites as well:
>
> - **S1**, the port's terminal cause: a device error during a header read
>   is told from an erased or unframed record, so it aborts the restore
>   instead of defaulting that record (section 8.6).
> - **S2**, response isolation on the descriptor store's memory face: a
>   late beat of a burst the store abandoned never enters another burst,
>   nor the roll-back's re-walk. With it, a failed or late descriptor read
>   aborts the restore and is never a refused value (sections 8.6 and 8.8).
> - **S3**, a bounded binding read phase: a silent persistence device no
>   longer holds AECP for ever. Commands are served on defaults, and the
>   port stays quarantined, for ever if the device never answers (section
>   8.8).
>
> An image the restore cannot prove ends CLOSED. The passes agree record by
> record. The output-format evidence separates the SYNTHETIC judge from a
> SHIPPING-legal save and replay (sections 8.2 and 8.4). Revision c answered
> the round-two reviews at `40d14d92`, revision b the round-one reviews at
> `d0256846`. Section 16 maps every finding of the three rounds to its
> answer.

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
  `branch 500-design-evidence, commit c1ee27d81c4a1e98f9584e979b73a88acfe238b3, path design-evidence/500-materialization/COMMAND_RESULTS.md`;
- how to re-run it:
  `branch 500-design-evidence, commit c1ee27d81c4a1e98f9584e979b73a88acfe238b3, path design-evidence/500-materialization/proposal-evidence/README.md`;
- the run script:
  `branch 500-design-evidence, commit c1ee27d81c4a1e98f9584e979b73a88acfe238b3, path design-evidence/500-materialization/proposal-evidence/run.py`;
- its graded results:
  `branch 500-design-evidence, commit c1ee27d81c4a1e98f9584e979b73a88acfe238b3, path design-evidence/500-materialization/proposal-evidence/results.txt`
  and `results.json` beside it;
- the prototypes (the writer, the arbiter, the descriptor memory guard)
  and the amended prototypes of the pinned port and binding manager:
  `branch 500-design-evidence, commit c1ee27d81c4a1e98f9584e979b73a88acfe238b3, path design-evidence/500-materialization/proposal-evidence/prototype/`;
- the area rows and the two cost proxies:
  `branch 500-design-evidence, commit c1ee27d81c4a1e98f9584e979b73a88acfe238b3, path design-evidence/500-materialization/proposal-evidence/ooc/`;
- the ticket drafts of section 10:
  `branch 500-design-evidence, commit c1ee27d81c4a1e98f9584e979b73a88acfe238b3, path design-evidence/500-materialization/tickets/`;
- the round-two and round-three reviewers' own probes, rerun against this
  revision:
  `branch 500-design-evidence, commit c1ee27d81c4a1e98f9584e979b73a88acfe238b3, path design-evidence/500-materialization/reviewer-probes/`.

The evidence the round-three reviews examined is commit
`fc2e3a6211bdbca3c41718eb6e1b4b4c2a128293` on the same branch, the round-two
reviews commit `ca8cb5943f885c22aec397ff75059e2d4791f4fb` and the round-one
reviews commit `a21b165ac1c671d10cba7255beaf75cea0f81d18`. Their
counterexamples are kept as named cases and mutants of this revision
(section 16). The executable sources of this revision's run are commit
`a78c79afebab98d53b94c034c92f7191989e8806`; the commits after it add the
results, the command record and documentation, and change no executable
file.

A section number that is a link points into another page; a plain section
number is this page's.

## Contents

- **[1. Context](#1-context)** -- Only the binding persists; where the seven other items live and how a change is seen.
- **[2. What reproduces at the current source](#2-what-reproduces-at-the-current-source)** -- Nothing is written, nothing comes back, and two changes read durable for a few cycles.
- **[3. Decision](#3-decision)** -- Eleven rules: one processor-side writer, live triggers, the clear rule, a restore transaction, deadlines, the enable, four prerequisite seams.
- **[4. Who writes: three candidates](#4-who-writes-three-candidates)** -- Per-group managers, one writer, the firmware: measured and judged.
- **[5. Interfaces](#5-interfaces)** -- What the processor, the parent and the firmware each change.
- **[6. State machines and next-state functions](#6-state-machines-and-next-state-functions)** -- The writer, the restore transaction, the port arbiter and its drain, priorities written out.
- **[7. The clear rule](#7-the-clear-rule)** -- When a pending source clears, and every risky ordering executed.
- **[8. Restore](#8-restore)** -- Order, cleared-first proof, value rules, coupling, names, the transaction, deadlines, the listener's admission.
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
it releases `entity_enable`); the saved-state page's
[section 9.3](SAVED_STATE_FASTCONNECT.md#93-reading-the-three-bits-together)
(the entity keeps answering AECP when persistence wedges); issue #70's
eight items and its vacuity trap; processor issues 15, 20, 61, 63 and 83;
issues #501 and #502.

## 2. What reproduces at the current source

EXECUTED on the tracked glue: `d3_top.sv` built with `D3_TRACKED` is
`KL_pp_shadow.sv` at the current source, transcribed, with no D3 writer, the
enable as it ships, the PINNED port and binding manager, and the PINNED
listener straight on its producers, with no admission gate. The run script
requires the tracked build to fail exactly these checks
(`TRACKED_MUST_FAIL`), so they are shown not to be vacuous; if one does not
fail it exits 1 and names it:

| Case : check | Tracked 1x1 | This design, both shapes |
|---|---|---|
| K1 : converged@end | FAILS "backed 1 dirty 0 stale 0 pend 1" | passes |
| K1 : value_in_slot@end:0x50 | FAILS "newest verified slot None" | passes |
| K10 : value_in_slot@end:0x80 | FAILS | passes |
| K12 : value_in_slot@end:0x70 | FAILS | passes |
| V1b : set_value_survives_power_cycle:0x50 | FAILS "restored 0 valid 0, set 1500000" | passes |
| K10 : no_durable_claim_over_unsaved | FAILS "change of 0x80 at 30182 inside a durable interval ending 30189" | passes |
| K12 : no_durable_claim_over_unsaved | FAILS "change of 0x70 at 30155 inside a durable interval ending 30161" | passes |
| L01 : listener_walk_bounded@terminal | FAILS "preload offers from 235: the longest untaken 3229969 cycles, 2 withdrawn" | passes |
| L05 : restored_binding_survives_a_read_only_command@recovered | FAILS "answered [(0, '0000000000000000')]; sink 0 in the newest verified slot 000000000000000000000000" | passes |

The run script also requires the tracked glue to PASS the durability check
on K1, V1a and V1b (`TRACKED_MUST_PASS`). A dynamic-state change is reported
from its own write by the store's level, so today's status never reads
durable over one.

The two L rows are the listener as it ships, and section 8.9 reads them.
L01 is round-three review R217's counterexample: a talker event held as a
level keeps the listener's `pre_ready_o` low, so the binding walk's preload
phase waits, with every AECP command behind it, until something else ends
it; in this case the case's own later GET_RX_STATE walks touched both
waiting sinks, the manager withdrew both preloads and flushed the unbound
records over the saved bindings. L05 is a hazard the same wiring exposes: a
read-only GET_RX_STATE served between a sink's stored record and its
preload writes the reset record back, the manager takes it as a live
change, and the saved binding is flushed away.

The K10 and K12 durability rows are a finding about today's glue, not only
the gap. It takes the class-6 and class-7 COMMIT MARKS, and the programs
raise them only after the live write: in
`protocol-processor/hdl/aecp/ucode/gen_ucode.py`, SET_NAME's `NVM_MARK` (line 2092) follows its last `NAME_WR` by COMPARE,
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
   manager 1, and a read either of them abandons is DRAINED there, never
   handed on. Obligation O1 is untouched: it constrains the one sequential
   CONTROL-face master (the strobe word, the image base and length, the
   channel-map tables), and neither the writer nor the drain writes a
   control-face register. Obligation O3, which orders device-face
   initiators after the restore walk, holds as well (section 8.1).
6. **The pending source.** `pend_i` becomes the binding manager's unflushed
   sinks OR the writer's unflushed records. The dynamic-state level and the
   parent's sticky class-6/7 bit LEAVE `pend_i`: a per-record bit replaces
   each of them, stage by stage (section 10).
7. **The restore is a transaction** (section 8.6), after the binding
   walk's drained terminal (seam S4) and before the entity is enabled. The
   writer owns the state bus FROM RESET, so no AECP program runs before or
   during the restore and the state it restores into is the reset state. It
   first proves the image the values are judged against; an image it
   cannot prove ends CLOSED. It
   reads every record twice through the port: pass 0 only proves the records
   whole, pass 1 judges each value by the rule of the SET program that would
   set it and applies it with its valid flag, or leaves the image default.
   A TRANSPORT FAILURE is a device error (the port's cause, seam S1), a torn
   read, a record whole in one pass and not the other, a descriptor read
   that the rule or an image default needs and that fails, or an expired
   deadline. One in pass 0 applies nothing. One in pass 1 ROLLS BACK: every
   restorable owner returns to its reset state, so no partial restore
   survives. A restore write is never a change. Restore done is both walks'
   terminal; blank is a restore that did not fail and in which neither walk
   validated a record.
8. **Deadlines, and the enable** (section 8.8). Every restore wait of both
   walks is bounded: the D3 walk's by `RS_TMO_CYC_P` cycles without
   progress, the binding walk's read phase by the same deadline (seam S3)
   and its preload phase by construction (seam S4: the listener is offered
   nothing else, so it takes each preload in the cycle it is presented). A
   deadline's expiry is an abort like a torn read. The D3
   restore ends in one of three terminals: COMPLETE, DEFAULTS (rolled back)
   or CLOSED (an image it cannot prove). The entity enable the firmware
   requests reaches the entity only at the restore's done, as the
   processor's F07.9 draws it ("release entity_enable"): ADP may then
   advertise it. The enable gates ADP advertising, not traffic: the
   listener's work faces and AECP dispatch have their own releases, S4's
   and the D3 terminal (section 8.1). A restore that never reaches done
   keeps the entity dark, never advertised and its AECP held: fail-closed,
   never an early enable. A silent persistence device ends both walks at their deadlines
   instead: commands are served on defaults, and the port stays quarantined
   until the device ends the operation it abandoned.
9. **An output map set its record cannot hold** is never written in part
   and never forgotten: it stays pending, and the flush skips it until its
   port changes again (section 7.2, K16). This is FAILURE CONTAINMENT, not
   persistence: Milan 5.3.10.1 requires the accepted set to persist, and
   stage 3 does not open until #501 decides a conforming allocation or
   limit (section 10).
10. **Three firmware changes** (section 5.3): the AEM image loads before
    `nvm_boot` (without it the restore cannot prove its image and ends
    CLOSED); the restore walk starts on every boot path; the restore wait's
    timeout and the enable line report that the fabric holds the enable.
11. **Four prerequisite seams** (sections 5.1 and 10), none of them a
    pinned feature today, each prototyped in the evidence:
    - **S1**: `KL_pp_nvm_port` reports why an operation failed: DEVICE (a
      device error, or a header read the device ended short) or UNFRAMED (a
      header the device delivered whole that is not a record). Both
      managers default a record only on UNFRAMED.
    - **S2**: a guard on the descriptor store's memory face holds the
      store's next request while an accepted burst still owes its last beat,
      and the roll-back holds the owners in reset while that debt lasts.
    - **S3**: the binding manager bounds its restore walk's read phase and
      fails the walk whole at the deadline, abandoning its read to the
      arbiter's drain.
    - **S4**: a gate in front of the pinned listener's work faces owns them
      from the hard reset to the binding walk's drained terminal. It holds
      a transaction and a talker event at their producers (valid and ready
      both masked), presents no START/STOP request (its valid masked; the
      listener's completion passes, and cannot fire while the gate owns the
      faces) and admits no timer expiry, so nothing but the preload reaches
      the listener. Its release starts the listener's live ACMP work and the
      D3 walk, and is part of the restore done that releases the enable
      (sections 8.1 and 8.9).

    They are prerequisites of stage 1's implementation lane and of every
    stage declared shippable (tickets T8 and T9). So is the descriptor
    store's roll-back reset, which stage 1 owns (section 10).

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
| Area, 1x1 | reference replication: 9,519 LUT, 8,789 FF, 1 RAMB36 | 2,377 LUT, 888 FF, 0 RAMB36, 0 DSP | fabric proxy: 530 LUT, 266 FF, 0 RAMB36; firmware not measured |
| Area, 8x8 | reference replication: 9,479 LUT, 8,725 FF, 3 RAMB36 | 3,116 LUT, 1,109 FF, 0 RAMB36, 0 DSP | fabric proxy: 1,631 LUT, 458 FF, 0 RAMB36 |
| O1, the one sequential control-face master | untouched: no manager writes the control face | untouched: neither the writer nor the drain writes a control-face register | still the firmware alone, but its control face GROWS: a per-record snapshot handshake and a state-bus bridge must be sequenced against ARM, ATTEST and ACK, a contract change to resolve explicitly |
| The device face, and O3 | eight producers behind the one port need an eight-way arbiter; each comes up after the restore walk | two producers behind the one port, with the arbiter and drain of section 6.4; the writer's first requests are its own restore walk | no D3 record crosses it, so the open vector, the attestation and the capture identity never see one: a second ownership mechanism must carry them |
| What a controller observes | pending from the write; durable after the manager debounce, the firmware debounce and a commit | the same | pending from the write; durable after the firmware debounce and a commit |
| Testability | seven managers to grade | the processor's own suites and the parent's co-simulation | the firmware on the host model plus a new CSR face |
| Repository | processor | processor, the parent glue and map-plane reset, and three firmware changes | both, and the processor's `07_memory_maps.md` section 5 must be amended to assign the groups to the integrator |

How each figure is made. (b) is the prototype writer at its worse mapping
plus the arbiter (2,325 + 52 LUT and 885 + 3 FF at 1x1; 3,064 + 52 LUT and
1,106 + 3 FF at 8x8). The four prerequisite seams S1 to S4 are costed
apart (section 12: 129 LUT and 54 FF at 1x1, 126 and 54 at 8x8), because
they amend the port and the binding manager, guard the descriptor store's
memory path and gate the listener's faces, which any candidate that
restores through the port and the listener and judges by descriptor rules
would need. (a) estimates reference replication: seven copies of
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
3. **LUT.** (b) measures about 3.75 percent of the XC7A100T's 63,400 LUT at
   1x1 and 4.91 percent at 8x8, out of context; with the seams S1 to S4,
   about 3.95 and 5.11 percent. Its integrated delta remains to be
   measured. The reference replication in (a) costs three to four times the
   writer and arbiter. The measured fabric proxy in (c) is smaller by 1,847
   LUT at 1x1 and 1,485 at 8x8. That comparison excludes firmware and
   integration costs; it supports the choice alongside the ownership and
   interface arguments above.
4. **The donor's own contract.** The processor's F07.9 puts the commit and
   the restore in the processor, and its issues 61 and 83 ask for exactly
   (b). (c) needs that contract amended first.
5. **Latency is a wash.** (b) adds the processor debounce before the firmware
   debounce (section 12); (c) does not. Both report pending from the write.

## 5. Interfaces

### 5.1 In the processor

All of this is the processor repository's (tickets T1 to T3, and the
prerequisites T8 and T9; S4 sits in `protocol_processor_top`, beside the
listener). The seams are where the prototype needed them;
the implementation places the writer inside `KL_aecp_engine` or beside it
with these ports. Rows marked AMENDED change a pinned module; rows marked
NEW add one. Neither is an existing product feature, and the evidence's
amended prototypes are the pinned files with declared amendments only,
renamed so they cannot pass for the pinned RTL.

| Face | Signals | Contract |
|---|---|---|
| State-bus client | `sb_req`, `sb_we`, `sb_name`, `sb_addr[19:0]`, `sb_wdata[63:0]`, `sb_wstrb`, `sb_didx[15:0]`; `sb_ready`, `sb_rvalid`, `sb_rdata`, `sb_err` | the engine's state port, with the µCPU's own contract: the request is held until the answer. A 2:1 selection in front of the two stores, `own` choosing the writer |
| Ownership | `own` (writer to engine), `prog_busy` (engine to writer) | the engine dispatches no program while `own` is 1. `own` is 1 FROM RESET until the restore's terminal (section 8.6), and 1 for ever in the CLOSED terminal. In service the writer raises `own` only in a cycle `prog_busy` is 0; `prog_busy` is the µCPU's busy, which covers the program's commit marks |
| Change snoop | the µCPU's accepted write: `st_req AND st_we AND region 1 AND dyn_ready`, with `st_addr[15:3]` the selector and `desc_index`; a name write: `st_name AND st_we AND store_ready`, with `st_addr[15:6]` the name ordinal | the writer's trigger for the dynamic-state records and the names, tapped on the µCPU's side of the 2:1 selection so a restore write is never a change. Selector 7 and an out-of-range index set nothing |
| Map trigger | `amap_edit_req_o AND amap_edit_phase_o == 5`, with `amap_edit_desc_type_o` and `amap_edit_desc_index_o` | the commit-one-record beat, after phase 1's point of no return; it sets the port's record |
| Map read | the GET_AUDIO_MAP face (`amap_req_o` and its type, index, map index, selector and record ordinal; `amap_data_i`, `amap_wait_i`) | driven by the writer while `own` is 1 |
| Map restore | the edit face, phases 0, 4, 1, 5 and 2 or 3 | driven by the writer while `own` is 1, during the restore only |
| Format judge | the Milan-info gather face, kind 0 selector 15, with `gsi_prop_fmt_o` | the integrator's judgement of a proposed format: bit 0 supported, bit 1 no mapped channel orphaned |
| Port | `KL_pp_nvm_mgr_arb` in front of `KL_pp_nvm_port`; `m_abort` (writer to arbiter) and `m0_abort` (binding manager to arbiter); `m_err_cause[1:0]` (arbiter to the owning manager, with its err) | section 6.4. Either abort abandons the READ the port serves for that manager, and the arbiter drains it. The cause is the port's (S1) |
| Port cause (S1) | `nvm_err_cause_o[1:0]` on `KL_pp_nvm_port`, valid with its err: 1 DEVICE, 2 UNFRAMED, 3 reserved | AMENDED (T8). DEVICE: the device reported an error in any state, or ended the 8-byte header read short. UNFRAMED: the device delivered the header whole and it failed the port's magic or length gate. Both managers keep a record's default only on UNFRAMED |
| Binding walk (S1, S3) | `KL_acmp_nvm_shadow`: `nvm_err_cause_i`, `nvm_abort_o`, `restore_cause_o[1:0]`, `RS_TMO_CYC_P` | AMENDED (T8). A zero-byte DEVICE err fails the walk whole. The read phase is bounded by the deadline; expiry fails the walk and abandons an issued read to the drain. Causes: 1 torn, 2 a device error with nothing forwarded, 3 the deadline. The preload phase is bounded by S4 |
| Listener admission (S4) | `KL_pp_acmp_lsn_admit` in front of `KL_pp_acmp_listener`'s transaction, talker-event, START/STOP and expiry faces; `walk_done` (the binding manager's `restore_done_o`), `pre_valid`, `lsn_busy` (`dbg_busy_o`), `lsn_arm` (`act_disc_arm_o`); `own`, `released` | NEW (T8); the listener is unchanged. Owned from the HARD reset; released once, when the binding walk is at its terminal, no preload is presented, the listener is idle and its last A4 strobe has left. While owned, a transaction and a talker event are held at their producers (valid AND ready masked: their ready is an acceptance); a START/STOP request's valid is masked and the listener's completion (`strm_set_ready_o`, `strm_set_error_o`) passes unmasked, because it fires only for a request the listener captured and its holder stays empty from the hard reset to the release; the expiry bus is not admitted (each listener-owner expiry counted). The gate and the listener take the same hard reset, never `rb_rst`. `released` is the binding walk's end for the D3 walk and for `restore_done_o`, and the start of the listener's live work (sections 8.1 and 8.9) |
| Descriptor memory (S2) | `KL_aecp_desc_mem_guard` between `KL_aecp_desc_store`'s memory master and the memory; `desc_debt` (guard to writer) | NEW (T9). An accepted burst owes its terminal beat (last or err). While it does, the store's next request is held and `desc_debt` is 1. The guard takes the hard reset only, never the roll-back strobe |
| Image status | `desc_img_valid`, the store's validated-image level | AMENDED (T1): today the debug tap `dbg_img_valid_o`; the restore's image proof reads it |
| Roll-back | `rb_rst`, one strobe to every restorable owner, held at least two cycles and while `desc_debt` is 1 | NEW soft-reset inputs: `KL_aecp_dyn_state` and `KL_aecp_desc_store`, BOTH stage 1's (T1; for the store, its reset or a re-walk request that also returns its fetch watchdog to zero: the store walks the image again, its watchdog re-armed and its names the image's), and the parent's map plane (T4, stage 3). Each owner returns to its reset state. The guard (S2) takes the hard reset only |
| Entity enable | `entity_enable_i`, `restore_done_o` | the ADP engine's enable becomes `entity_enable_i AND restore_done_o`, `restore_done_o` being the binding walk's drained terminal (S4's release) AND the D3 walk's done: the restore releases `entity_enable`, as F07.9 draws it. It gates ADP advertising only: the side port's image-window lock keeps the top's `entity_enable_i`, as it ships, and ACMP and AECP traffic have their own releases (section 8.1) |
| Exports | `nvm_unflushed_o` stays the binding manager's; new `d3_unflushed_o`, the OR of the writer's dirty bits; `nvm_alarm_o` becomes both managers' alarm; `restore_done_o`, `restore_fail_o` and `restore_blank_o` become both walks; new `restore_rb_o`, `restore_closed_o`, `rs_cause_o[2:0]` and the binding walk's `restore_cause_o[1:0]` | section 8.7 |
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
  latch is unchanged; restore blank reads 1 only for a restore that did not
  fail, so a device error that loses the one saved record never reads as a
  clean first boot (H8).

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
   Without this change the image is not in main memory when the walk
   starts, the restore cannot prove it and ends CLOSED.
2. `nvm_boot` starts the restore walk on EVERY path. Today the path that
   finds the record set inconsistent with the generated shape returns before
   the walk. With AECP dispatch held from reset, the listener's faces owned
   from reset (S4) and the enable released by the restore, a boot that
   never starts the walk would leave the entity dark and deaf, ACMP
   listener included, until reset. DERIVED: the model's shape always matches, so
   that path is never taken there; it is an acceptance item of T4.
3. The restore wait stays bounded, but it REPORTS and decides nothing: at
   its timeout the firmware prints that the restore has not reached its
   terminal and that the fabric holds the enable, and `entity_advertise`
   prints that it requested the enable. `entity_advertise` still writes
   PP_CTRL[0] and ADP_CTRL[0] after the wait; the restore releases them.

The ledger fact `firmware_boot_order` and the order block of
[`BAREMETAL_FIRMWARE.md`](../integration/BAREMETAL_FIRMWARE.md) move with
change 1; `scripts/check_feature_status.py` compares all three.

EXECUTED: F01_old_boot_order keeps the current order. The restore then ends
CLOSED, nothing V1a sets is saved, and V1b's end-to-end check reads
"restored None valid None, set 1500000".

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
| WAIT-GO | the binding walk's drained terminal, S4's release: the walk done or failed, the listener idle, the last preload written and armed | IMAGE |
| IMAGE | the descriptor store holds a validated image, after a LOCATE of ENTITY 0 if it did not | NEXT, pass 0 |
| IMAGE | that LOCATE errs or finds no validated image | CLOSED, cause 7: no value can be judged and the names are unproven |
| NEXT | the last record of pass 0 | NEXT, pass 1 from the first record |
| READ, STREAM | the port ends the read with the whole record | pass 0: marked whole, the next record. Pass 1: ABORT (cause 5) if pass 0 did not read it whole; else the value rule (section 8.3), then APPLY or the next record |
| READ, STREAM | the port ends it with nothing forwarded and the cause UNFRAMED | an erased or unframed record: blank, the next record. In pass 1, ABORT (cause 5) if pass 0 read it whole |
| READ, STREAM | the port ends it with a DEVICE err, with or without bytes, or torn | ABORT (cause 2, or 1 torn) |
| a value rule | a descriptor read the rule needs ends in err: the store's fetch error, or its own watchdog's answer | ABORT (cause 6), never a refused value |
| NEXT | the first name record of pass 1 | CHECK: every restored format is judged again against the final maps (section 8.4); a revert whose image-default read errs ABORTs (cause 6) |
| NEXT | the last record of pass 1 | FINISH: every record agreed with pass 0 as it was read |
| a map record | the edit face refuses to give up the port's reset set, or to take it back | ABORT (cause 4) |
| any restore wait | `RS_TMO_CYC_P` cycles without progress | ABORT (cause 3); a granted port read is abandoned to the arbiter's drain |
| ABORT | before the image was proven | CLOSED |
| ABORT | pass 0 | done and fail: nothing was applied, `own` 0 |
| ABORT | pass 1 | ROLL-BACK |
| ABORT | during the roll-back | CLOSED |
| ROLL-BACK | `rb_rst` held for two cycles and until `desc_debt` is 0; the deadline bounds that wait | RE-LOCATE |
| RE-LOCATE | the LOCATE of ENTITY 0 answers with a validated image | DEFAULTS: done, fail and rolled back, `own` 0 |
| RE-LOCATE | the LOCATE misses or errs | CLOSED: fail, never done, `own` 1 |
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
              (in ROLL-BACK the event is desc_debt falling)
wd'         = stall ? wd + 1 : 0
expire      = stall AND wd >= RS_TMO_CYC_P - 1
m_abort     = expire AND a granted port read is open
unframed    = port err AND nothing forwarded AND cause = UNFRAMED
whole0[r]'  = pass 0 AND record r read whole ? 1 : whole0[r]
disagree    = pass 1 AND (record r read whole) != whole0[r]
abort       = expire OR (port err AND NOT unframed) OR a torn read OR disagree
              OR a descriptor read a rule or a revert needs errs
              OR a refused edit of a reset set
rolling'    = abort AND pass 1 AND image proven AND NOT rolling ? 1 : rolling
rb_rst      = from rolling's rise, at least two cycles and while desc_debt
closed'     = (abort AND (rolling OR NOT image proven)) OR (IMAGE or RE-LOCATE
              finds no validated image) ? 1 : closed
done'       = FINISH OR (abort AND pass 0 AND image proven) OR (RE-LOCATE hits) ? 1 : done
fail'       = abort OR closed' ? 1 : fail
blank       = done AND NOT fail AND no record validated
own'        = reset ? 1 : done' ? (the service rule) : own
entity_en   = (PP_CTRL[0] OR ADP_CTRL[0]) AND restore_done
restore_done = bind_end AND D3 done

the binding manager's walk (seams S1 and S3):
bstall      = read phase AND (H_RS_REQ AND the port not idle
              OR H_RS_STREAM AND no byte, done or err this cycle)
bwd'        = bstall ? bwd + 1 : 0
bexpire     = bstall AND bwd >= RS_TMO_CYC_P - 1
bfail       = bexpire OR a torn read OR (port err AND nothing forwarded AND cause != UNFRAMED)
bfail       => done, fail, no preload, every uncaptured sink at its default
m0_abort    = bexpire AND in H_RS_STREAM (the read was issued)

the listener's admission (seam S4):
drained     = walk_done AND NOT pre_valid AND listener idle AND NOT A4 strobe
own_lsn'    = reset ? 1 : drained ? 0 : own_lsn         (one-way until reset)
txn, talker event to the listener = the producer's valid AND NOT own_lsn
their ready to the producer       = the listener's ready AND NOT own_lsn
START/STOP to the listener        = the engine's valid AND NOT own_lsn
START/STOP completion to the engine = the listener's ready and error,
                                    unmasked (0 while own_lsn: no holder)
expiry to the listener            = the expiry AND NOT own_lsn
bind_end    = NOT own_lsn   (live ACMP work; the D3 walk's go; restore_done)
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
drain'  = (done or err) ? 0
        : (owner = writer AND m_abort) OR (owner = binding AND m0_abort) ? 1 : drain
rready  = owner = writer ? (drain OR writer rready)
        : owner = binding ? (drain OR binding rready) : 0
owner's bytes, done, err, cause = owner's AND NOT drain AND the port's
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

**The drain.** The port answers untagged: its bytes and its done or err
name no operation. So a read either manager abandons stays OWNED by the
arbiter until the port ends it: the arbiter holds rready so every late byte
can move, swallows the bytes and the ending, and grants neither manager
until then. A late response can therefore only ever end the operation it
belongs to. The drain never ends on time. A device that ends the read late
ends the drain, and the port serves the next operation. A device that never
answers keeps the port QUARANTINED for ever: every later change reads
pending, never durable, until a reset. Nothing in this contract makes that
port reusable; that needs a real cancellation or device-reset
acknowledgement (processor issue 15's open recovery contract, section 15
item 4). EXECUTED in section 8.8; D01_abandoned_read_not_drained withholds
rready from the writer's drained read, the late response then wedges the
port, and a later change never reaches a slot: "latest 0076adf1, newest
verified slot 0016e360". B03_binding_abort_not_drained does the same to the
binding manager's abandoned read, and W13c kills it with the same reading.

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
| A change during the record write | K2 | taint_rewrites:0x50, no_durable_claim_over_unsaved | "2 completed writes of 0x50; the last carries 0021e88e" | M01_taint_ignored ("durable at 1568763: record 0x50 latest 0021e88e slot 0010f447") |
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
| A SET waiting while the restore runs | K19 | value_in_slot@end:0x50, command_waits_for_the_restore@end | "the waiting SET was taken at [7606], the D3 terminal at 7606" | O01_own_taken_at_the_walk ("latest 001d48d7, newest verified slot 0016e360": the SET ran first and the restore overwrote it) |
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
   AECP program is dispatched until step 9. The admission gate (S4) has
   owned the listener's work faces since reset: no ACMP listener command,
   talker event, START/STOP request or timer expiry reaches the listener
   until step 5.
2. `load_aem_image`: the AEM image in DDR, its CRC checked.
3. `nvm_boot`: both slots validated, the window loaded and the RELOAD
   accepted (the snapshot contract, unchanged), then the walk started through
   `PP_CTRL[1]`.
4. The binding manager's walk: read, validate, replay to the listener. Its
   read phase is bounded by its own deadline (seam S3): a silent device, a
   DEVICE error on a header or a torn read fails the walk whole, with
   nothing preloaded. Its preload phase meets a listener offered nothing
   else (S4), which takes each preload in the cycle it is presented.
5. Its DRAINED terminal, the gate's release (the walk done or failed, the
   listener idle, the last preload's record written and its discovery
   armed), starts the D3 walk. From here the listener does live ACMP
   work while the D3 walk runs, what waited first, after the restored
   image.
6. If the descriptor store holds no validated image, a LOCATE of ENTITY 0
   makes it walk the one the firmware loaded. An image it still cannot
   validate ends the restore CLOSED: nothing can be judged against it.
7. Pass 0: every D3 record is read whole, or the walk aborts.
8. Pass 1: every record is read again, judged and applied or refused; the
   restored formats are judged again against the final maps; the names last.
   An abort rolls back (section 8.6).
9. Restore done, for both walks: the D3 terminal COMPLETE or DEFAULTS. The
   writer releases the state bus: AECP programs run, the ones held since
   reset first. The enable bits the firmware writes (step 10) reach the ADP
   engine. CLOSED never reaches this step.
10. `entity_advertise`: the firmware writes the enable bits. It does so after
    its bounded wait whether or not the restore is done; the fabric holds
    them until step 9.

Obligation O3 holds for the writer: it requests nothing on the device face
before the binding walk is done, its first requests are its own walk, and
its first flush follows that walk. The enable is now released by the
restore itself, so no entity enable precedes the restore of both walks, nor
the last preload's record write and discovery arm, whatever the firmware's
timing.

**Three release points, each its own.** The restore releases three things
at three points, and none of them stands for another (the integration
clarification on this contract, [PR comment 5762146376](https://github.com/kebag-logic/milan-fpga/pull/503#issuecomment-5762146376)):

| Point | What it releases | What runs from it |
|---|---|---|
| S4's release, the binding walk's drained terminal (step 5) | the listener's four work faces | LIVE ACMP work: the ACMP commands the dispatch held and later ones, ADP's talker events, the AECP engine's START/STOP requests once AECP runs, and the expiries of the timers the listener's live walks arm |
| the D3 terminal, COMPLETE or DEFAULTS (step 9) | the state bus, and with it AECP dispatch | AECP programs, the ones held since reset first |
| the entity enable, `(PP_CTRL[0] OR ADP_CTRL[0]) AND restore_done`, `restore_done` being S4's release AND the D3 walk's done (step 10) | the ADP engine's enable | ADP advertising: F07.9's "ADP may start" (Milan 5.6.1) |

Live ACMP work after S4's release is not a late restore action. The binding
manager's preload phase is over and never runs again before a reset: no
preload is presented after the release, and every preload's record write
and discovery arm precede it (graded in every L case). What the listener
does from the release, a record write-back the binding manager persists as
a live change, a discovery arm, an ACMP PDU, is live service on the
restored image: a live change follows the restore and wins by coming later
(L06, L09), and a read-only command answers the restored bindings (L04,
L05).

The entity enable is not a traffic freeze. In the pinned `KL_adp_engine.sv`
it holds the advertise state machines in DOWN, where an ENTITY_DISCOVER is
ignored, and nothing else: the talker-discovery state machines, which feed
the listener's talker events, evaluate remote ENTITY_AVAILABLE on a
separate path. Its other consumer in `protocol_processor_top.sv`, the side
port's image-window write lock, keeps the top's `entity_enable_i`, as it
ships. ACMP listener work waits for S4's release only, and AECP for the D3
terminal only, whatever the enable says; a controller that already knows
the entity's id can reach both before the entity is advertised. A CLOSED
terminal holds AECP and the enable until a reset, and does not take the
listener's faces back. EXECUTED, L04 at 1x1: a controller polls
GET_RX_STATE from reset, "first taken at [243] (1745 in all), the release at
243"; the D3 terminal follows at 3879, and "entity enabled at 3893".

EXECUTED: V1b reads "enabled at 7613, D3 restore done at 7606, restore done
at 7606" at 1x1 and "enabled at 13895, D3 restore done at 13889" at 8x8.
G02_restore_done_without_d3 lets the processor report done after the binding
walk alone, and the entity is enabled first: "enabled at 188, D3 restore done
at 7606". G05_enable_not_released_by_restore removes the release, and an
enable a bench script requests from reset reaches the entity before the
restore (section 8.8, W14): "entity enabled at 9, D3 terminal at 7606". The
listener's order (section 8.9): in every L case the D3 walk starts the cycle
after the release, and the release follows the last preload's record write
and discovery arm, "preload record writes [236, 240], their discovery arms
[237, 241], the release at 243, the D3 walk from 244" at 1x1.

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

V1a changes every group at its first and, where it has more than one, its
last index: the configuration index, the clock source, both stream-format
directions, the presentation offset, both map directions (a narrowed stream
takes the mappings that named its lost channels with it) and the first and
last names. Its values are those the model's SYNTHETIC format judge admits
(section 14), and one of them is not product-legal: V1a narrows output 0
from eight channels to four, and the product admits an output's declared
format alone (section 8.4). Its input narrowing is product-legal. So the
output format's SHIPPING-legal persistence is graded apart, under the
product's own verdict: V1s_a SETs output 0 to a narrower format, refused,
and to its declared format, accepted; V1s_b restores that record WITH its
valid flag ("GET output 0 format 0x205022002006000 valid 1"); V1s_c refuses
a narrower saved output on replay ("output 0 format valid 0 (value 0),
refused 1, D3 fail 0"). The declared value equals the generated default, so
only the valid flag tells a replay from none, and it does.

The configuration index has one legal value, 0, at every configuration the
builder emits, so its replay is graded by the valid flag as well: RPL_cfg
deletes only that replay, and V1b reads "live (0, 0) want (0, 1)". No
shipped configuration lists two sampling rates, so a legal non-default rate
cannot be saved at either shipped shape; the synthetic test configuration
1x1r2 (section 14) lists 48 kHz and 96 kHz, and restores "live equals the
slot" for 96,000 with its valid flag. Every group has its replay-deletion
mutant, killed by its own record's check: RPL_cfg, RPL_rate (1x1r2),
RPL_clks, RPL_fmti, RPL_fmto, RPL_ptof, RPL_mapi, RPL_mapo and RPL_name.
RPL_fmti and RPL_fmto must fail V1s_b's check as well as V1b's, and
TRG_fmti and TRG_fmto V1s_a's as well as V1a's: a mutant counts as killed
only when every check the run script names for it fails.

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
| clock source | SET_CLOCK_SOURCE: index below `clock_sources_count` of the CLOCK_DOMAIN | the image default | V1b: value and valid flag restored; V2b: an index past the count, "clock source row valid 0, refused 1", no failure |
| stream formats in and out | SET_STREAM_FORMAT: the integrator's judge, gather kind 0 selector 15; the product admits an output's declared format alone, an input the 1/2/4/6/8 family | the image default | V6b, V8, V9 (section 8.4); V1s_c under the product's judge |
| presentation time offset | SET_STREAM_INFO: bit 31 of the latency is BAD_ARGUMENTS (`KL_aecp_engine.sv` line 3159) | the image default | V1b: first and last index restored |
| channel maps | the record's framing, then ADD_AUDIO_MAPPINGS: the integrator judges the staged set whole | the port's reset set is put back | V3 and V3a to V3g below |
| user names | SET_NAME: any 64 bytes; the empty name is a value | - | V7, V1b (section 8.5) |
| any group | the frame, the crc16 | the image default; the next record is still applied | V5: "ptof0 valid 0, refused 1" and "ptof1 1600000 valid 1" |

A refusal needs the rule. A descriptor read the rule needs that ends in
error, the store's fetch error or its own watchdog's answer, is not a
refused value: nothing was judged, and the restore aborts (section 8.6).

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

**Which judge.** The product's verdict (`hdl/milan/milan_datapath.sv`,
`sfv_supported_w`) admits an OUTPUT format only when it equals the
output's declared format, base and channel count, because the framer emits
the declared wire shape; it admits an INPUT format of the 1/2/4/6/8 family
on the declared base. The model's SYNTHETIC judge admits narrower OUTPUT
formats as well. V6a, V6b, V8, V9, V20c and V20d narrow an output, so the
output-format ordering they show rests on the synthetic judge: it exercises
the ordering, and it is not product-legal SET evidence. At the shipped
shapes an output format can be SET only to its declared value (V1s, under
the product's judge), and the input direction's coupling is product-legal.

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

This design makes the whole D3 restore one transaction, with a roll-back
whose correctness is structural:

- **The state it restores into is the reset state.** The writer holds the
  state bus from reset until the restore's terminal, so no AECP program runs
  before or during the restore: no row, name or map is changed by anything
  but the restore. Round one's rule that "a live change made during the
  restore wins" had nothing left to act on and is removed.
- **So the roll-back is a reset.** An abort in pass 1 pulses `rb_rst`, which
  resets the dynamic-state store, the descriptor store and the parent's map
  plane (section 5.1); the two stores are stage 1's owners, the map plane
  stage 3's. Each owner then holds exactly what it held before the
  restore: every row at its reset value with its valid flag clear, every
  name the image's (the descriptor store walks the image again), every
  port's reset set. Formats and maps return together, so they are
  consistent by construction. No journal of what the restore applied is
  needed, and none is kept.
- **The roll-back is proven before the entity is released.** The owners
  stay in reset for at least two cycles and while the descriptor memory
  still owes an accepted burst its last beat (seam S2), so no late beat
  enters the re-walk. The writer then LOCATEs ENTITY 0, which waits out the
  descriptor store's walk. A validated image ends in DEFAULTS; a walk that
  cannot validate, or a memory debt that outlasts the deadline, ends in
  CLOSED (section 8.8).
- **What is a transport failure.** At the pinned port a device error during
  a header read, a header the device ended short and a header it delivered
  whole that is not a record all end in one err with nothing forwarded. So
  a device error that recurred on a header in both passes read as an erased
  record and defaulted it with no failure verdict (both round-two reviews).
  The port's terminal cause (seam S1) separates them: UNFRAMED keeps the
  record's default, DEVICE aborts, with or without bytes forwarded. Equal
  counts of whole records did not prove the passes agreed, since two
  differences balance, so the passes now agree RECORD BY RECORD: a record
  whole in one pass and not in the other aborts at that record (cause 5).
  With the cause, a device error already aborts; the agreement catches
  content that differs between the passes with no device error at all,
  which no count and no list of record identities could (a record lost in
  both passes looks the same in both). A descriptor read that a value rule
  or a revert needs and that ends in error is a transport failure too
  (cause 6), never a refused value: the store's fetch error and its own
  4,096-cycle watchdog answer the same error, and neither judged anything.
  An image the restore cannot prove before pass 0 ends it CLOSED
  (cause 7).
- **What it does not touch.** The saved state: nothing is written to the
  window or to flash by a failed restore, so the slot still holds what the
  controller last saved, and the next restore that succeeds brings it back.
  The live entity runs on defaults meanwhile, with restore fail set; the
  status can read durable over it, because every change a controller made is
  in a slot. The binding walk: the unit of atomicity for a transport
  failure is the walk, as it already is for the binding manager, which
  rejects its own walk whole. A D3 roll-back leaves a completed binding walk
  applied: its owners are the two stores and the map plane, never the
  listener or the binding manager. EXECUTED, L13 at 1x1 and 8x8: a pass-1
  read error on 0x50 after both bindings were restored reads, at 1x1, "the
  D3 roll-back at 2612 (cause 2), after the binding walk's release at 243"
  (at 8x8, 6634 after 484), and the listener then answers both restored
  bindings and the slot still holds them.

EXECUTED at 1x1 and 8x8, each on V1a's slots (every group non-default) with
one fault, then a controller's GET and SET:

| Case | The fault | What it read |
|---|---|---|
| V12 | a read error in PASS 0 on fmti0 (0x30), early | "applied 0, abort cause 2, roll-back at 0"; every record at its default |
| V13 | a read error in PASS 0 on the last name, late | the same: nothing was applied |
| V14 | a read error in PASS 1 on fmti0, after the configuration and the clock source applied | "2 records applied before the fault, roll-back at 3598"; "0 records off their defaults"; D3 done 1 fail 1 rolled back 1 |
| V15 | a read error in PASS 1 on the last name, after every scalar, format, map and the first name applied | "9 records applied before the fault"; "0 records off their defaults"; the slot kept: "10 saved records besides 0x50, 0 changed in the newest verified slot" |
| V16 | a read error in PASS 1 on the OUTPUT map, after the formats and the INPUT map applied | "7 records applied"; formats and maps at their defaults together |
| V18 | a DEVICE error on 0x50's HEADER lane in PASS 1 only (R218's pass1) | "4 records applied before the fault, roll-back at 3761, abort cause 2"; every record at its default |
| V11b | the reviewers' counterexample: V11's slot, the name torn in PASS 1 after 0x50 applied | "ptof0 valid 0 after the pass-1 tear"; rolled back 1 |
| V11 | the name torn at rest: pass 0 meets it first | "applied 0, rolled back 0": nothing to roll back |

After each: the entity is enabled only at the terminal ("entity enabled at
7358, D3 terminal at 7341" in V15), no restore write follows the terminal,
the GET answers the default ("0 valid 0") and the SET persists.

Header transport faults, EXECUTED at 1x1 and 8x8 on V1a's slots unless
named. H1, H2, H2b and H3 are the round-two reviewers' own stimuli; the
reviewers' probe scripts, rerun unchanged but for their paths
(`reviewer-probes/`), agree with them:

| Case | The fault | What it read |
|---|---|---|
| H1 | a DEVICE error on 0x50's header lane in both passes (R217 header-repeat, R218 repeat) | pass 0 aborts at 0x50: "applied 0, abort cause 2 (a device error)"; every record at its default; "restore fail 1, D3 fail 1, blank 0" |
| H2 | 0x30's header in pass 0 and 0x50's in pass 1, so the counts would balance (R217 header-balanced) | pass 0 aborts at 0x30, the same readings |
| H2b | 0x51's header in pass 0 and 0x50's in pass 1 (R218 swap) | the same, at 0x51 |
| H3 | 0x50's header in pass 0 only (both reviewers' pass0) | the same |
| H4, H5, H6 | both passes, at the first record (0x00), a map record (0x70), the last name | the same, at that record |
| H8 | both passes, on a slot that holds 0x50 alone | "restore fail 1, D3 fail 1, blank 0": the one saved record, lost to a device error, never reads as a clean first boot |
| H7 | the last name's header in pass 1 only, after every other record applied | "9 records applied before the fault, roll-back at 6506, abort cause 2" |
| V18b | no device error: 0x50's header changes at rest after pass 0 read it whole | "4 records applied before the fault, roll-back at 3779, abort cause 5" |
| V18c | no device error: 0x30 unframed in pass 0 only, 0x50 in pass 1 only | "2 records applied before the fault, roll-back at 3574, abort cause 5": one unframed record in each pass, the counts equal |
| V10 | the control: every binding and D3 record erased | "restore fail 0 (D3 0, binding 0), causes D3 0 binding 0, done 1", blank 1 |

Descriptor faults, EXECUTED at 1x1 and 8x8. V20, V21 and V22 are R217's
own stimuli:

| Case | The fault | What it read |
|---|---|---|
| V20b | one error beat on the first descriptor fetch after an application: the clock source's rule | "the descriptor memory answered an error beat at 3390, the writer aborted at 3394"; "1 records applied before the fault, roll-back at 3395, abort cause 6"; refused 0; rolled back |
| V20c | V9's slot: the refused OUT map's revert fetches the image-default format, and that fetch errs once | "2 records applied before the fault, roll-back at 3741, abort cause 6"; rolled back |
| V20d | V8's slot: the final re-judge's revert fetch errs once | "1 records applied before the fault, roll-back at 2660, abort cause 6"; rolled back |
| V21 | the first descriptor request after an application answers 5,000 cycles late (R217 descriptor-timeout) | "request accepted at 3387, the store's error answer aborted the restore at 7487 (4100 cycles), the late burst came at 8388, the owners left reset at 8399"; rolled back to defaults, every name the image's |
| V21b | the same, 16,000 cycles late | "the late burst came at 19388, the owners left reset at 19399"; rolled back |
| V21c | the same, 30,000 cycles late, past the deadline | "aborted at 7487, CLOSED at 27489 (20002 cycles), the late burst came at 33388" |
| V21d | the same, 4,000 cycles late, inside the store's own watchdog | "its first beat at 7388 (4001 cycles ...), abort cause 0"; COMPLETE |
| V20 | the descriptor memory fails from the first application on (R217 descriptor-error) | abort cause 6; the re-walk cannot validate: CLOSED, "entity enabled 0 ... a GET answered None" |
| V22 | the descriptor memory fails from before boot (R217 descriptor-initial-error) | "abort cause 7, applied 0, refused 0, image validated 0, closed 1" |
| V22b | the same, on a slot holding an offset and a name, records no rule fetch touches | the same: CLOSED |
| V2b | the control: a clock-source index past the count, its rule fetched | "clock source row valid 0, refused 1"; "D3 fail 0, rolled back 0, cause 0" |
| V23 | in service: a locate answered by the store's own watchdog, a second at once, a third presented while the late burst is owed | "second locate err 1 ...; third locate err 0 type 0x5": never the late burst's bytes; afterwards "a locate answered err 0, descriptor_type 0x5" |

At 8x8 the same cases read the same verdicts at later cycles, for example
V21's "the late burst came at 11893, the owners left reset at 11904".

The mutants: R01_no_rollback (a pass-1 abort ends without a roll-back, round
one's behaviour) is killed by V15, "9 records off their defaults ... rolled
back 0". R02, R03 and R04 each drop one owner from the roll-back: the
dynamic-state store (V15, "6 records off their defaults"), the descriptor
store (V15, "0x80 live 443320726573746f72656420 want 4d696c616e20465047412031"),
the map plane (V16). X01_passes_may_disagree drops the per-record agreement,
and V18b ends "D3 done 1 fail 0 rolled back 0" with "9 records off their
defaults": a partial restore reported as a success. X02_passes_compared_by_count
restores round two's count comparison, and V18c ends the same way.
M16_single_pass_restore is killed by V11: "applied 0, rolled back 1". The
single pass applied a record before the tear and had to roll it back, where
pass 0 meets the tear first and has nothing to roll back.

The classification's mutants. C01_device_error_reads_as_blank (round two's
rule) is killed by H8: "D3 done 1 fail 0 ... cause 0", the lost record read
as nothing to restore. C02_port_cause_collapsed makes the port report
UNFRAMED for every err, the pinned port's information, and H1 ends "9
records off their defaults ... D3 done 1 fail 0". C03_unframed_reads_as_device_error
fails the blank first boot: V10 reads "restore fail 1 (D3 1, binding 0)".
DF01_desc_error_is_a_refusal (round two's rule) is killed by V20b: "9
records off their defaults ... fail 0". DF03 drops the check on the final
revert's fetch, and V20d ends "0x40 live (0, 1) ... fail 0". DF02 drops the
check on a map revert's fetch; its garbage default is then refused by the
re-add judge, so V20c still rolls back, under cause 4, and the truthful
cause is its killer. IMG01_unproven_image_continues walks an image it could
not prove, and V22b ends "abort cause 0, applied 2 ... closed 0".
DG01_guard_admits_a_request_while_owed is killed by V23: "third locate err
0 type 0x6", another descriptor's bytes served. DG02_rollback_ignores_mem_debt
releases the owners without the debt, and V21b ends "D3 done 0 fail 1 ...
closed 1": the re-walk times out on the owed burst.

**The descriptor store's reset belongs to stage 1** (round-three review
R218 R3-F1). After a fetch's RESPONSE timed out, the pinned store answers
without clearing its watchdog count (`KL_aecp_desc_store.sv` line 980), so
its next fetch errs in its first cycle (line 938). That error answer clears
the count, so in ordinary service the fetch after it succeeds (V23), but
the roll-back proves the image by one LOCATE, and that LOCATE is the next
fetch. Draining the memory's debt does not change that; only the store's
reset does, or a re-walk request that also returns the count to zero. Revision c's stages gave stage 1 the dynamic-state store's reset
alone and the descriptor store's to stage 2, for its names, so a stage-1
implementation would end CLOSED where a finite late burst must end in
proven defaults. Stage 1 now owns both resets (section 10, ticket T1), and
stage 2's names come back on the same reset.

EXECUTED on R218's selector-only slot (configuration `0x00` = 0000, clock
source `0x0A` = 0001, presentation offset `0x50` = 1500000, every other
record erased), on the stage-1 build (`D3_STAGE1`: the two stores roll
back, the map plane does not) and on both full builds alike; the readings
are the stage-1 build's:

| Case | The fault | What it read |
|---|---|---|
| S1a | none | "0 records not as saved [], D3 done 1 fail 0"; "configuration (0, 1), clock source (1, 1), ptof0 (1500000, 1)" |
| S1b | the first rule fetch after an application answers 4,000 cycles late | "request accepted at 2443, its first beat at 6444 (4001 cycles, the store's own watchdog 4096), abort cause 0"; COMPLETE |
| S1c | the same, 5,000 cycles late | "the store's error answer aborted the restore at 6543 (4100 cycles), the late burst came at 7444, the owners left reset at 7455"; DEFAULTS; the GET "answered 0 valid 0"; the later SET persists |
| S1d | the same, 16,000 cycles late | "the late burst came at 18444, the owners left reset at 18455"; DEFAULTS; the GET and the SET as S1c |
| S1e | the same, 30,000 cycles late, past the deadline | "aborted at 6543, CLOSED at 26545 (20002 cycles), the late burst came at 32444" |
| S1f | one error beat, then a healthy memory | "1 records applied before the fault, roll-back at 2451, abort cause 6"; DEFAULTS |
| S1g | the descriptor memory fails from before boot | "abort cause 7, applied 0, refused 0, image validated 0, closed 1" |
| S1h | a read error on 0x50's payload in pass 1 | "2 records applied before the fault, roll-back at 2744, abort cause 2"; DEFAULTS |

ST1_stage1_rollback_skips_desc_store is the stage-1 build with revision
c's stage-1 scope, the descriptor store left out of the roll-back, and S1c
and S1d both kill it: "D3 done 0 fail 1 rolled back 0 (want 1) closed 1 own
1 cause 6". R218's own six-case reproduction, rerun in an adapted copy that
adds the stage-1 build and ST1 (`reviewer-probes/`, 12 runs as demanded),
reads the same: with the store's reset V21 and V21b end in DEFAULTS
("terminal 8110, enable 8123"; "terminal 19110, enable 19118"), without it
in CLOSED, and the one-error control V20b recovers either way. In every
recovered case the guard's debt outlives the roll-back's own reset: the
owners leave reset only after the late burst.

### 8.7 What the status says after a restore

- restore done: both walks' terminal (the binding walk's drained terminal,
  S4's release, and the D3 walk COMPLETE or DEFAULTS).
- restore fail: either walk failed, or a blind walk (the latch
  `KL_pp_shadow` already keeps). The D3 walk fails on a device error, a
  torn read, a difference between the passes, a descriptor fault, an
  unproven image, a deadline, or a port that refuses to give up or take
  back its reset set. The binding walk fails on a torn read, a device error
  with nothing forwarded, or its deadline.
- restore blank: the restore did NOT fail, and NEITHER walk validated a
  record. V7, a name back and no binding, reads "blank 0, done 1";
  G04_blank_ignores_d3, the binding walk's blank alone, reads "blank 1".
  V10, a blank first boot, reads "blank 49 of 49, applied 0 ... status blank
  1" (145 of 145 at 8x8). H8, a device error losing the only saved record,
  reads "restore fail 1, D3 fail 1, blank 0".
- new, on the processor's face (the PP_STAT rows are owed, section 5.2):
  rolled back (DEFAULTS), closed (CLOSED: fail, never done), the D3 walk's
  first abort cause (1 torn, 2 device error, 3 deadline, 4 edit refused, 5
  the passes disagree, 6 descriptor fault, 7 image not proven) and the
  binding walk's (1 torn, 2 a device error with nothing forwarded, 3 its
  deadline).
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
clock (section 15 item 8). A subordinate's own, shorter timeout never
counts as progress: the descriptor store's 4,096-cycle watchdog answers an
error, and the writer aborts on it (cause 6, V21). Sized so, the writer's
deadline does not fire during a store fetch that is moving; if it did, the
roll-back would still hold the owners in reset while the memory owes a
burst. Only the restore is watched: in service the
writer holds the state bus only across on-chip faces (section 12's latch
windows), and a flush that waits on the port holds nothing but its record's
dirty bit.

**The abandoned read.** An abort while the port serves the writer's read
raises `m_abort`, and the binding manager's deadline raises `m0_abort`; the
arbiter DRAINS that read (section 6.4). Its bytes and its ending reach no
manager, and no new operation is granted until the device ends it. This is
the containment protocol for an untagged port; nothing here assumes the
port can be reused before the device answers, and a device that never
answers keeps it QUARANTINED for ever (section 15 item 4).

**The terminals.**

| Terminal | Reached by | done | fail | `own` | The entity |
|---|---|---|---|---|---|
| COMPLETE | pass 1 ended, the passes agree | 1 | 0 | released | enabled at done |
| DEFAULTS | an abort in pass 0, or a pass-1 abort rolled back and the image walked | 1 | 1 | released | enabled at done, on defaults |
| CLOSED | an image not proven at the start; a roll-back that cannot validate the image, or whose memory debt outlasts the deadline; an abort during the roll-back | never | 1 | kept for ever | never enabled; no AECP program runs; only a reset leaves |

**The enable.** The restore releases it (section 8.1). The firmware's wait
decides nothing: when it times out, the firmware reports and writes the
enable, and the fabric holds that enable until done. So no restore write
can follow the enable: every restore write precedes the terminal, and the
enable follows it.

**The binding walk (seams S3 and S4).** The pinned `KL_acmp_nvm_shadow`
keeps no deadline; this contract makes one a prerequisite (ticket T8),
prototyped as an amendment of that module. Its read phase is bounded by
`RS_TMO_CYC_P` without progress. Silence fails the walk whole: done, fail,
cause 3, nothing preloaded, every uncaptured sink at its default, and the
read it issued is abandoned to the drain. Its preload phase is bounded by
the listener's admission (S4, section 8.9): the listener is offered nothing
but the preloads from reset, so it takes each one in the cycle it is
presented, and the phase ends within four cycles a sink. The D3 walk then
starts at the drained terminal, meets a port the drain may still hold, and
ends at its own deadline in DEFAULTS. A silent device therefore keeps the
entity dark for at most the two deadlines plus the walks, never for ever,
whatever the listener's producers do, and commands are then served on
defaults with restore fail set, as the saved-state page's section 9.3
requires when persistence wedges.

**Command availability and persistence availability are two things.**
Commands come back when both walks end. The persistence device comes back
only when the device ends the read the drain holds: a late answer ends the
drain and the next change persists (W13c, W15); a device that never
answers keeps the port QUARANTINED until reset, and every later change reads
pending, never durable (W13). Nothing releases the port on time, and nothing
here claims the port reusable before the device ends that read; a real
cancellation or device-reset acknowledgement is processor issue 15's open
recovery contract, which this page neither delivers nor amends.

EXECUTED at 1x1, and the D3 cases at 8x8 as well, each on V1a's slots unless
named, each followed by a controller's GET and SET:

| Case | What was held | What it read |
|---|---|---|
| W1 | pass 0: the first memory read of fmti0, for ever | "held from 956, released 0, abort cause 3"; "stall began at 956, D3 terminal at 20956"; nothing applied; the later SET "pend 1, port busy 1": the drained read never ends |
| W2 | pass 0: released when the deadline was 40 cycles away | "the watchdog reached 19960 of 20000, abort cause 0"; the restore COMPLETE |
| W3 | pass 0: released 5 cycles after the deadline | "the writer aborted at 20955, the response came at 20960"; the drain took it, and the later SET persists |
| W4 | pass 1: fmti0, for ever | "stall began at 3545, D3 terminal at 24202"; rolled back to defaults |
| W5 | pass 1: released 40 cycles before the deadline | "the watchdog reached 19960 of 20000"; COMPLETE |
| W6 | pass 1: released 5 cycles after the deadline | "the writer aborted at 23544, the response came at 23549"; rolled back; the later SET persists |
| W7 | pass 1: the last name, for ever | "stall began at 6513, D3 terminal at 27155"; rolled back |
| W8, W9, W10 | pass 1: the GET_AUDIO_MAP face, the format judge, the edit face silent | each "abort cause 3", the terminal at most 20,666 cycles after the face fell silent at 1x1 and 21,158 at 8x8, rolled back |
| W11 | R217's counterexample: V11's slot, the first D3 read 3,500,000 cycles late | "held from 782 to 3500782"; "D3 terminal at 20782", "entity enabled at 20798"; the late response drained; the later SET persists |
| W12 | R218's counterexample: a pass-1 read after records applied, 3,100,000 cycles late | "D3 terminal at 24202", "entity enabled at 24218"; rolled back; the response drained at 3103545 |
| W13 | the BINDING walk's first read, for ever | "silence from 64, the binding walk's terminal at 20062"; "binding fail 1 cause 3, preloads []"; "D3 terminal at 40722", "entity enabled at 40733"; the GET "answered 0 valid 0"; the later SET "pend 1, port busy 1": quarantined |
| W13b | the binding read, released when the binding deadline was 40 cycles away | "the binding deadline count reached 19960 of 20000, binding cause 0"; "preloads [(20130, 0)]"; both walks COMPLETE |
| W13c | the binding read, released 5 cycles after the binding manager abandoned it | "abandoned at 20061, the response came at 20066"; "binding fail 1 cause 3"; "preloads []"; the D3 walk COMPLETE; the later SET persists |
| W15 | the binding read, released at 2,900,000, after the entity was enabled | "the entity enabled at 40733, the response came at 2900064"; "preloads []": no binding reaches the listener after enable; the D3 walk ended on defaults; the later SET persists once the drain ends |
| W16 | a DEVICE error on the binding record's header | "binding fail 1 cause 2 (a device error on the header), preloads [], restore fail 1, blank 0"; the D3 walk COMPLETE |
| W14 | an enable a bench script requests from reset | "the enable requested at 9, restore done at 7606"; the entity enabled after the terminal |
| V17 | V15, and the descriptor memory fails from the roll-back on | CLOSED: "closed 1, restore done 0 fail 1, own 1, entity enabled 0 ... firmware asked at 3000074, a GET answered None" |

Every case above that reaches done also passes
entity_enabled_after_terminal@boot and no_restore_write_after_terminal. The
later SET persists wherever the port is free, and reads pending, never
durable, where a drained read never ends (W1, W4, W7, W13); the GET after
recovery is graded wherever the restore ended on defaults.

W01_no_restore_watchdog is killed by W4: "D3 terminal at 0".
D01_abandoned_read_not_drained by W6 (section 6.4).
G05_enable_not_released_by_restore by W14 (section 8.1).
R05_closed_releases_the_entity lets CLOSED release the bus and report done,
and V17 kills it: "closed 0, restore done 1 ... entity enabled 1".
O01_own_taken_at_the_walk takes the bus at the walk instead of at reset, and
K19 kills it (section 7.2). B01_binding_walk_no_deadline is killed by W13:
"the binding walk's terminal at 0". B02_binding_device_error_reads_as_empty,
processor issue 20's defect, by W16: "binding fail 0 cause 0".
B03_binding_abort_not_drained by W13c: "latest 0076adf1, newest verified
slot 0016e360". B04_binding_unframed_reads_as_device_error by the blank
first boot V10: "restore fail 1 (D3 0, binding 1)".

**Every dependency of the restore, audited once.** Each row is a wait or an
answer the restore depends on, how it can fail at the pinned modules and the
seams, and what the transaction does about it.

| Dependency | How it can fail | The restore's answer | Evidence |
|---|---|---|---|
| Reset and admission | a request reaching the listener before or during the binding walk; a hard reset inside the walk | the gate owns the listener's faces from the hard reset (S4); a reset is a power cut, and the preload writes nothing, so the next boot restores the same slot | L04, L06, L09 (requests from reset), L08a, L08b; LG01 to LG05 |
| The image walk, a LOCATE of ENTITY 0 | a miss or an error: no validated image | CLOSED, cause 7, before any record is read | V22, V22b, S1g; IMG01 |
| The binding walk's read phase | a DEVICE err, a torn read, silence | the walk fails whole, nothing is preloaded, its read is drained (S1, S3); the D3 walk then runs | W13, W13b, W13c, W15, W16, L11, L12; B01 to B04 |
| The binding walk's preload phase | a transaction, a talker event, a START/STOP request or a timer expiry keeps the listener's `pre_ready_o` low for as long as it keeps coming; a live walk's write-back touches a waiting sink and withdraws its restored binding | nothing but the preload reaches the listener until the walk's drained terminal (S4): each preload is taken in the cycle it is presented, the phase ends within four cycles a sink | L00 to L13 at 1x1 and 8x8; LG01 to LG05; tracked L01, L05; R217's round-three probe (section 8.9) |
| The walk's end, the D3 walk and the enable | the D3 walk or the enable before the last preload's record write and discovery arm | the D3 walk starts on the gate's release, and restore done takes it | release_after_the_final_preload_action in every L case |
| A D3 read, pass 0 or pass 1 | a DEVICE err, a torn read, a record whole in one pass only, silence | abort (causes 2, 1, 5, 3): pass 0 applies nothing, pass 1 rolls back | H1 to H8, V11, V11b, V12 to V18c, W1 to W7, W11, W12 |
| A descriptor read a value rule or a revert needs | an error beat; the store's own 4,096-cycle watchdog | abort, cause 6, never a refused value | V20b, V20c, V20d, V21; DF01 to DF03 |
| A state-bus write, the apply | DERIVED from the pinned RTL: `KL_aecp_dyn_state` has no error output and takes a write in the cycle it is presented; the descriptor store's one writable region, the names, answers no error | a stall only, which the deadline watches (cause 3) | no case: the pinned stores offer no write error to inject |
| The edit face, a map apply | the port refuses to give up or take back its reset set; silence | abort, cause 4; cause 3 | cause 4 under DF02 (V20c: "abort cause 4"); W10 |
| The format judge, the GET_AUDIO_MAP face | silence | abort, cause 3 | W9, W8 |
| The roll-back and the re-walk | a burst still owed; the re-LOCATE misses or errs; either outlasting the deadline; the descriptor store's fetch watchdog left at its limit by a response timeout | the owners held in reset while a burst is owed; the store's own reset, stage 1's, re-arms its watchdog; then DEFAULTS, or CLOSED | V21, V21b, V21c, V20, V17, S1c to S1f; DG02, R05, ST1 |
| Late answers and late effects | an NVM read after its manager abandoned it; a descriptor burst after the store gave up on it; a preload, a discovery arm or a held request landing after the terminal | drained by the arbiter until the device ends it; held off by the guard, never served to a later request; no preload after the release, and each held request taken once, after it | W3, W6, W11, W12, W13c, W15; V21, V21b, V23; L03b, L09, L10; D01, B03, DG01, LG02, LG03 |
| The firmware | its wait times out; an enable is requested early | decides nothing: the restore releases the enable | W14, V17; G05 |
| Live service | a command held through the restore | AECP after the D3 terminal; the ACMP listener after the release, what waited first, in its own priorities; a D3 roll-back leaves the restored bindings | the GET and SET after every case; the listener's GET_RX_STATE after every L case; L06, L09, L13 |

The model's omissions that bear on this table: the edit face's phases 0 to
5, the product memory paths' own timing (their CDC FIFOs,
`pp_desc_bridge`'s watchdog and poison), the product's producers of the
listener's faces (the dispatch, the event router, ADP discovery and the
START/STOP µprogram, modelled by their handshakes), real flash and firmware
change 2 (section 14).

### 8.9 The listener's admission (seam S4)

**What round three found.** The binding walk's preload phase hands each
restored binding to the pinned `KL_pp_acmp_listener` on its preload face and
waits for its `pre_ready_o`. The listener serves one work item at a time,
and its X_IDLE ranks a START/STOP holder, a dispatch transaction, a pending
timer expiry and a talker event above the preload: `pre_ready_o` is low
while any of them is present (`KL_pp_acmp_listener.sv` line 484). Any of
them, kept coming, keeps the walk in `H_RP_DRIVE`, with every AECP command
held behind the restore and an idle persistence port (round-three review
R217 R3-F1; revision c's evidence had tied `pre_ready` high). A timeout
alone cannot mend that: when it fires, earlier sinks are preloaded and their
discovery armed, and nothing takes the listener's records back. A second
hazard sits in the same wiring. Every listener walk ends in a record
write-back (X_WB) that the binding manager captures as a live change, so a
walk served between a sink's stored record and its preload withdraws that
sink's restored binding and flushes the reset record over the saved one. A
read-only GET_RX_STATE is enough, and ACMP dispatch does not wait for the
entity enable.

**The mechanism.** A gate in front of the listener's four work faces,
`KL_pp_acmp_lsn_admit` (section 5.1, ticket T8), OWNS them from the hard
reset to the binding walk's drained terminal. The listener is unchanged.

- A dispatch transaction and a talker event are HELD at their producers:
  the valid towards the listener and the ready towards the producer are
  both masked, so the ACMP head stays in its dispatch queue, the event
  router's sticky latch stays set, and nothing is consumed that the
  listener did not see.
- A START/STOP request's VALID is masked, and the listener's completion
  passes to the AECP engine unmasked. That face is not an acceptance
  handshake: the engine holds its request until `strm_set_ready_o`, which
  the listener raises once the record commit or the no-op check is done
  (with `strm_set_error_o` when its bounded wait expires), and the listener
  captures a presented request into its holder in any state. The holder
  and its done and fail flags reset to 0 and fill only from a presented
  request; the gate and the listener take the same hard reset, and neither
  takes the roll-back. So from reset to the release the holder stays empty
  and no completion can fire: masking the completion as well would change
  nothing while the gate owns the faces, and a passed completion never
  answers a request the listener did not capture. Paired masking of valid
  and ready is for the transaction and the talker event, whose ready is an
  acceptance. In the product the engine presents no START/STOP request
  before the D3 terminal anyway, since the writer holds AECP dispatch from
  reset; the evidence's producer holds one from reset (L06, L06b), and
  every L case grades that no START/STOP request is captured while the gate
  owns the faces and that captures and completions agree in number.
- The timer expiry bus does not reach the listener, and every expiry of a
  listener owner that arrives is counted, never queued. The listener arms
  its timers only in the walks the gate holds off, and the timer service's
  armed bits reset to 0, so none can be legitimate while the gate owns the
  faces.
- The gate RELEASES the faces once: when the binding manager's walk is at
  its terminal (done, failed or not), no preload is presented, the listener
  is idle and its last A4 discovery strobe has left. The manager never walks
  again before a reset, so the gate never owns the faces again before one.
  The release is the binding walk's END: the D3 walk starts on it, and the
  restore done that releases the entity enable takes it.

**Why it bounds the walk.** With nothing else admitted, the listener's
reachable states from reset to the release are X_INIT, X_IDLE and
X_PRELOAD. No walk runs, so no timer is armed, no holder is captured and no
expiry is pending, and `pre_ready_o` is 1 in every X_IDLE cycle. X_INIT ends
N+1 cycles after reset, long before a walk can reach its preloads, and
X_PRELOAD lasts one cycle. So a preload is taken in the cycle it is
presented, the preload phase ends within four cycles a sink plus four, and
the release follows the manager's terminal within four cycles (two after a
preload, one without, in the evidence). The bound is by construction, not a
fairness claim, and nothing is released on time: no physical operation is
abandoned and no partial binding image is left, because the preload phase
has no failure exit to reach. At the pinned timing the manager's registered
done already follows the last preload's record write and discovery arm, so
the gate's two drain terms (listener idle, strobe gone) are not separately
observable here; they keep the release independent of the two modules'
pipeline depths, and every case grades the property itself.

**The exact boundary.** A request presented at any cycle before the release
is not accepted by the listener; its producer keeps it. The first released
cycle takes what the listener finds: a request presented in the last owned
cycle, or in the first released one, is taken in that first released cycle,
and one presented a cycle later is taken a cycle later (L10). A request held
from reset is taken exactly once, at the release, in the listener's own
priority (L04). No listener service is promised before the release, and
what a producer does with arrivals behind a held head is its own queue
policy, unchanged. A boot that never starts the binding walk leaves the
listener owned until reset, as it leaves AECP dispatch held; firmware
change 2 starts the walk on every path.

**What it changes for a live change.** A BIND, UNBIND, START or STOP that
arrives before the release now follows the restored image instead of
withdrawing it: it is served after the release, so it still wins, by coming
later, and the binding manager persists it as it persists any live change.
A read-only command no longer changes the saved state. A D3 roll-back
leaves the restored bindings, which are no D3 owner (L13). What the
listener does from the release is live service, not a late restore action,
and it does not wait for the D3 terminal or the enable (section 8.1's three
release points).

EXECUTED at 1x1 and 8x8, each on a slot holding the bindings of the first
and the last sink and a presentation offset. Each is graded on what the
LISTENER took and did (its own valid AND ready, its record writes, its A4
arms, the PDUs it sent), then on the listener's own GET_RX_STATE of both
sinks and a controller's AECP GET and SET:

| Case | The listener's faces | What it read at 1x1 |
|---|---|---|
| L00 | nothing held | "preload offers from 235: the longest untaken 0 cycles, 0 withdrawn, 0 left open; the walk's terminal at 241 (6 cycles after the first offer, bound 12), the listener released at 243" |
| L01 | R217's lever: a droppable talker event (sink `0xffff`) held as a level from reset, for ever | the same bound; "the droppable talker event level held from reset: first taken at [243], 1820364 taken" |
| L02 | the same level, dropped at cycle 100000 | the same bound; "99758 taken, the last at 100000, released at 243" |
| L03 | the level raised the cycle after the first sink's preload | "the later preload taken at [(239, 1)], the level first taken at [243]" |
| L03b | an EVT_TK_DISCOVERED of the first sink, raised after its preload (the discovery its A4 armed) | "popped [243], taken [243], released at 243, the listener's next record write of sink 0 at [270]" |
| L04 | a controller polling GET_RX_STATE from reset | "first taken at [243] (1745 in all), the release at 243" |
| L05 | ONE GET_RX_STATE, presented once the first sink's record was stored and before its preload | "taken at [243] (released 243), answered [(1, '00a1a1a1a1a10001')]; sink 0 in the newest verified slot 03000a0100a1a1a1a1a10001" |
| L06 | a STOP of the first sink, held by the AECP engine from reset | "STOP of sink 0 completed at [248] (errors []), after its preload [(235, 0)] and the release 243; the record written stopped at [247]"; the stopped binding persisted |
| L06b | START and STOP back to back from reset | "24960 completed, the first at [248], released 243" |
| L07 | an expiry of the first sink's owner every cycle | "234 expiries of sink 0's owner while owned, 234 not admitted, 0 reached the listener while owned, 149757 from [243]" |
| L08a, L08b | the power cut in the cycle the last sink's preload is taken, then the next boot | "the first sink's preload taken at 235, written at [236], armed at [237]; the last sink's taken at 239"; "3 of the 3 crafted unchanged; 0 device-face writes before it"; the next boot restores both |
| L09 | a BIND_RX of the first sink to another talker, from reset | "BIND_RX of sink 0 taken at [243], after its preload [(235, 0)] and the release 243; answered status [0]; the restored talker written back after it []"; the new binding persisted |
| L10 | ONE GET_RX_STATE in the last owned cycle (m1), the first released one (0) or the next (p1) | "popped at [243] and taken at [243] (want 243)" for m1 and 0; "popped at [244] and taken at [244] (want 244)" for p1 |
| L11 | the held level, and the binding read released 40 cycles short of its deadline | "the binding deadline count reached 19960 of 20000"; "the walk's terminal at 20197 (6 cycles after the first offer, bound 12), the listener released at 20199" |
| L12 | the held level, and the binding read silent for ever | "binding fail 1 cause 3, preloads [], done 20062, released 20063"; the D3 walk ends on defaults, the port stays quarantined |
| L13 | a pass-1 read error on 0x50 | "the D3 roll-back at 2612 (cause 2), after the binding walk's release at 243"; both bindings kept |

In every case the listener lives only in X_INIT, X_IDLE and X_PRELOAD while
the gate owns its faces ("states while owned ['X_INIT', 'X_IDLE',
'X_PRELOAD'], side effects 0, takes at its faces 0"). Each held request is
popped by its producer in the cycle the listener takes it, none while
owned. The release follows the last preload's record write and discovery
arm, and the D3 walk starts the cycle after ("preload record writes [236,
240], their discovery arms [237, 241], the release at 243, the D3 walk from
244"). After the release the listener's own GET_RX_STATE answers the
restored bindings, and the slot still holds them at the end, or holds the
live change where the case made one. At 8x8, with sinks 0 and 8 of nine
bound: "the walk's terminal at 482 (12 cycles after the first offer, bound
40), the listener released at 484".

The mutants, each killed in completed runs by every check named for it:

- LG01_admission_deleted deletes the gate's masks: the pinned wiring. L01
  kills it by its bound, "preload offers from 235: the longest untaken
  3229969 cycles, 2 withdrawn": the held level starved the preload until
  the case's own later GET_RX_STATE write-backs touched both waiting sinks,
  the manager withdrew both preloads, and the unbound records were flushed
  over the saved bindings. L05 kills it by the binding it erases:
  "answered [(0, '0000000000000000')]".
- LG02_valid_admitted_ready_masked admits the valid and masks the ready:
  the listener consumes what its producer is told was not taken. L05 kills
  it as it kills LG01, and L04 by "txn_pop 0 / txn_take 114747, 114747
  while owned".
- LG03_ready_passed_valid_masked masks the valid and passes the ready: the
  producer pops what the listener never saw. L10 m1 reads "popped at [242]
  and taken at [233935] (want 243)" and L03b "tk_pop 1 / tk_take 0, 1 while
  owned".
- LG04_expiries_admitted: L07 reads "149991 reached the listener while
  owned".
- LG05_start_stop_admitted: L06 reads "STOP of sink 0 completed at [14]
  (errors []), after its preload [(235, 0)] and the release 243; the record
  written stopped at []": the STOP reached the holder during the read
  phase, completed as a no-op on the still unbound sink, and the preload
  then restored the started binding over it.

The tracked glue fails L01 and L05 (section 2). R217's own round-three
probe, adapted only in its lever (the harness's own talker-event producer,
held as the same level, where the original patched a port) and run on the
gate and on LG01, holds as demanded (20 runs, `reviewer-probes/`). With the
gate, the held and the finite level leave the binding walk's end, the D3
terminal and the enable where the ready control leaves them: "binding walk
ends at 178 (control 178), D3 terminal 7606 (control 7606), enable 7613, GET
(1500000, 1)". With the gate deleted the counterexample comes back. The
reviewer's own checker exits 1 on the gate's results, its two
counterexample assertions false; on LG01's its held assertion holds again,
the GET unanswered after 2,000,068 cycles.

Cost (section 12): the gate alone measures 13 LUT and 17 FF at 1x1, 16 of
the flops its diagnostic count of refused expiries. In front of the pinned
listener it adds 13 LUT and 17 FF at 1x1 and 8 and 17 at 8x8 to the
listener's existing 2,174 LUT and 1,530 FF, and 2,268 and 1,557.

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

**Release conditions**, as recorded on #500 when revision b was taken, the
prerequisite seams revisions c and d add, and stage 1's ownership of the
descriptor store's roll-back. They add gates, and change no allocation:

- **The seams S1 to S4 are prerequisites of stage 1's implementation lane
  and of every stage declared shippable** (tickets T8 and T9, processor
  repository). S1 and S3 amend the pinned `KL_pp_nvm_port` and
  `KL_acmp_nvm_shadow`; S2 adds a guard on the descriptor store's memory
  face; S4 adds a gate in front of the pinned `KL_pp_acmp_listener`'s work
  faces and leaves the listener unchanged. Stage 1's restore consumes the
  port's cause and reads the descriptor store, and its dispatch hold from
  reset is acceptable only with a binding walk that ends, its preload phase
  included. A stage-1 lane may start on T8's and T9's reviewed interfaces;
  it does not merge before they land in the same pin or an earlier one. The
  evidence's prototypes and amended prototypes are design evidence, not the
  pinned RTL, and no product change is authorized by this page.
- **The descriptor store's roll-back reset is stage 1's** (ticket T1), with
  the dynamic-state store's: after a fetch's response timed out the pinned
  store's next fetch errs at once, and only its reset, or a re-walk request
  that also returns its watchdog to zero, lets the roll-back prove the image
  (section 8.6). The guard's debt (S2) survives that reset; it takes the
  hard reset only. Stage 2 adds no owner: its names come back on the same
  reset.

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
- **Stated in every stage's release notes:** a persistence device that
  never ends an operation the restore abandoned keeps the port QUARANTINED
  until reset (section 8.8). Commands are served and the entity is enabled
  on defaults with restore fail set; every later change reads pending, never
  durable. No reuse of that port is claimed: processor issue 15's recovery
  contract is open, and no stage waits for it.

| Stage | Records | What lands | Silicon proof | Tickets |
|---|---|---|---|---|
| 1. the dynamic-state selectors | configuration index, sampling rate, clock source, stream formats, presentation offset: 9 records at 1x1, 30 at 8x8 | on the seams S1 to S4: the writer with the state-bus trigger, `own` from reset, the flush, the restore transaction from the binding walk's drained terminal with its deadline, its cause classification, its descriptor-fault aborts and the roll-back of BOTH stores (the dynamic-state store, and the descriptor store, whose reset re-arms its fetch watchdog and re-walks the image), held while the descriptor memory owes a burst (S2); the format rule on "supported"; the arbiter and its drain of either manager; the enable released by the restore; the exports; `pend_i` loses the dynamic-state level; the three firmware changes | SET_CLOCK_SOURCE 1, SET_STREAM_INFO, SET_STREAM_FORMAT on an unbound input; power cycle; GET_CLOCK_SOURCE, GET_STREAM_INFO, GET_STREAM_FORMAT, and the ADPDU's configuration index | T8, T9 (processor, prerequisites), T1 (processor), T4 (this repository); released after #502 |
| 2. names | 38 at 1x1, 99 at 8x8 | the name trigger, the eight-lane latch, the restore after the image walk; the names' roll-back rides stage 1's descriptor-store reset; `pend_i` stops taking class 7 | SET_NAME on the entity name, the group name and a stream name, one of them to the EMPTY name; power cycle; GET_NAME | T2, T4; released after #502 |
| 3. channel maps | 2 at 1x1, 16 at 8x8 | BLOCKED on #501. Once unblocked: the edit-face trigger, the GET_AUDIO_MAP latch, the framing rule, the coupled restore, the map plane's roll-back, #501's capacity decision; the sticky class-6/7 bit is deleted | ADD and REMOVE on both ports; power cycle; GET_AUDIO_MAP | T3, T4, #501 |

Stage 1's descriptor recovery is shown alone: section 8.6's S1 cases run
on the stage-1 build, which rolls back the two stores and not the map
plane, on a slot holding stage-1 records only, and ST1 deletes the store's
reset from it. Stage 1 restores formats while the maps still reset: the
maps come back empty, so nothing restored can be orphaned. Both shipped
shapes list one sampling rate, so the rate record can only be proved at its default on the
board; V2 covers its refusal and the synthetic 1x1r2 its replay. Until stage
3 the class-6 bit stays in `pend_i`, and until stage 2 the class-7 one,
unless #502's correction has already replaced them.

The area of each stage is a subset of section 12's row; each lane owes its
own post-place delta by the saved-state page's recipe, at both shipped
shapes.

Further tickets, not stages: T5 is #501; T6 is #502; T7, the saved-state
page's area table (recorded on #495). T8 and T9 are the prerequisites
above: T8, a new processor issue referencing issues 15 and 20, carries S1,
S3 and S4 and closes and amends neither issue; T9, a new processor issue,
carries S2 and also closes a pre-existing exposure of ordinary AECP service
to a burst the descriptor store abandoned (section 8.6, V23).

## 11. Alternatives rejected

| Alternative | Rejected because | Evidence |
|---|---|---|
| (a) A manager per group, in the image of `KL_acmp_nvm_shadow` | the reference replication costs three to four times the LUT of (b) and one to three RAMB36 on a device whose binding constraint is block RAM; seven debounces, seven retries and seven restore walks to grade | reference replication estimate, section 4 |
| (c) The firmware materializes the records from CSR reads | D3 records would never cross the device face, so a second ownership mechanism, on a larger control face, must carry the clear rule beside the accepted contract; the firmware becomes a writer of processor state; the framing and the value rules move into firmware; the donor's F07.9 must be amended. Its measured fabric proxy is smaller by 1,847 LUT at 1x1 and 1,485 at 8x8, excluding firmware and integration costs | measured proxy, section 4 |
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
| Counting the records each pass read whole and comparing the counts (round two) | two differences balance: one record lost in each pass leaves equal counts over a partial restore | EXECUTED: X02 is killed by V18c |
| Comparing the record identities the two passes read | a record lost to the same device error in both passes is missing from both lists alike, so the lists agree over it | the port's cause (S1): H1, H8 |
| Telling an erased record from a device error in the manager alone, by the bytes or by err against done | the pinned port folds both into one err with nothing forwarded, and eight 0xFF bytes do not prove an erased span; processor issue 20's manager-only split would fail every first boot | the port's cause (S1); V10, C03 |
| A failed rule fetch counted as a refused value (round two) | the value was never judged: a transient descriptor fault, or the store's own watchdog, silently defaults a record the rule would accept | EXECUTED: DF01 is killed by V20b |
| Restoring over an image that cannot be proven, refusing every record (round two) | a restore reported complete over an unwalked image whose names are not proven | EXECUTED: IMG01 is killed by V22b; V22 |
| Re-walking the descriptor store at once after its reset | a burst it abandoned can hand its late beats to the re-walk, whose index and names are not checksummed | EXECUTED: DG02 is killed by V21b; the guard's own mutant DG01 by V23 |
| Holding AECP dispatch through an unbounded binding walk (revision b) | a silent device held every command for ever, against the saved-state page's section 9.3 | the bounded binding walk (S3), W13; B01 is killed by W13 |
| Releasing the port after a deadline, or calling it reusable, while its device may still answer | the port answers untagged; only the device ending the operation, or a real cancellation acknowledgement, makes reuse safe | section 8.8; processor issue 15's open recovery contract |
| Waiting on the listener's `pre_ready_o` as it ships (revision c) | a held transaction, talker event, START/STOP request or expiry holds the preload phase, and with it every AECP command, for as long as it lasts | R217 R3-F1; tracked L01; LG01 is killed by L01 |
| A preload deadline that ends the binding walk, or releases the listener, on time | when it fires, earlier sinks are preloaded and their discovery armed, and nothing takes the listener's records back: the D3 walk and the enable would follow a partial binding image | section 8.9 |
| Ranking the preload above the listener's other sources, in an amended listener | a transaction or a talker event served in the read phase still writes a record back and withdraws a restored binding; and it amends a pinned module the admission gate leaves unchanged | tracked L05; LG01 is killed by L05 |
| Rolling the preload phase back on a failure | once nothing else is admitted the phase has no failure exit to reach; the listener has no soft reset, and a roll-back would have to undo discovery arms already issued | section 8.9 |
| Masking only the listener's ready, or only its valid | the producer's pop and the listener's take disagree: a request is consumed unseen, or popped and never served | LG02 and LG03, each killed |
| Leaving the descriptor store's roll-back reset to stage 2 (revision c) | after a response timeout the pinned store's fetch watchdog stays at its limit, so draining the debt alone leaves the roll-back's LOCATE failing, and a stage-1 restore ends CLOSED where a finite late burst must end in proven defaults | ST1 is killed by S1c and S1d; R218's reproduction, adapted |

The round-one table listed "Gating the entity enable on restore done in
hardware" as rejected, because the port has no timeout. The writer's own
deadline removed that reason for the D3 walk in revision b, and the binding
walk's deadline (S3) removes it for the binding walk. It is section 3's
rule 8 now.

## 12. Cost

MEASURED, out of context (section 4's recipe and calibration), re-run for
this revision. LUT is the LUT-equivalent total. These are estimates of the
prototypes, not bounds on an integrated implementation.

| Block | 1x1 LUT | 1x1 FF | 8x8 LUT | 8x8 FF | RAMB36 | DSP |
|---|---|---|---|---|---|---|
| the writer, with DSP mapping | 2,258 | 885 | 3,064 | 1,106 | 0 | 0 |
| the writer, without DSP | 2,325 | 885 | 2,964 | 1,106 | 0 | 0 |
| the arbiter, with the drain of either manager | 52 | 3 | 52 | 3 | 0 | 0 |
| **(b), the writer and arbiter, worst column** | **2,377** | **888** | **3,116** | **1,109** | **0** | **0** |
| S2, the descriptor memory guard (NEW) | 5 | 1 | 5 | 1 | 0 | 0 |
| S1, the port's cause: the amended port, 201 LUT and 118 FF, against the pinned one | +4 | +2 | +4 | +2 | 0 | 0 |
| S1 and S3, the binding manager: amended, 1,147/1,115 at 1x1 and 1,222/1,157 at 8x8, against pinned | +107 | +34 | +103 | +34 | 0 | 0 |
| S4, the listener's admission gate (NEW) | 13 | 17 | 14 | 17 | 0 | 0 |
| S4 in place: the pinned listener with the gate in front, 2,187/1,547 at 1x1 and 2,276/1,574 at 8x8, against the listener alone | +13 | +17 | +8 | +17 | 0 | 0 |
| **(b) with the seams S1 to S4** | **2,506** | **942** | **3,242** | **1,163** | **0** | **0** |
| for scale, existing: the binding manager, pinned | 1,040 | 1,081 | 1,119 | 1,123 | 0 | 0 |
| for scale, existing: `KL_pp_acmp_listener`, pinned | 2,174 | 1,530 | 2,268 | 1,557 | 0 | 0 |
| for scale, existing: `KL_pp_nvm_port`, pinned | 197 | 116 | 197 | 116 | 0 | 0 |
| for scale, existing: `KL_nvm_backend` | 1,051 | 476 | 1,476 | 515 | 0 | 6 |

What each row covers. The writer and arbiter rows are the prototypes
alone. The guard row and the S4 gate row are the new modules alone; 16 of
the gate's 17 flops are its diagnostic count of refused expiries, which a
product could narrow to a sticky bit. The rows marked + are INCREMENTS: the
difference between an amended module and the pinned one, or between the
pinned listener with the gate in front and the listener alone, each
synthesized out of context the same way, so they are estimates within the
usual tens-of-LUT noise, not bounds. The S4 total takes the gate alone,
the larger figure at 8x8. The rows marked existing are hardware the product
already has, listed for scale and not added by this contract.

Round two measured (b) at 2,311 LUT and 862 FF at 1x1 and 2,876 LUT and 987
FF at 8x8. The writer grows by 26 FF at 1x1 and 122 at 8x8: the per-record
pass-0 vector (49 bits at 1x1, 145 at 8x8) replaces round two's two 8-bit
counts, a net 33 and 129 bits, and 7 flops fewer elsewhere at both shapes
are not attributed further. Its worst-column LUT grows by 62 and 236: the
classification, the descriptor-fault aborts, the debt wait and the vector's
selection. The arbiter's second drain adds 4 LUT.

DERIVED: the integration seams of section 5.1 not prototyped here (a 2:1
selection over the state bus and the two map faces, about 250 signals) add a
few hundred LUT at most; the roll-back reset inputs and the enable gate are
one gate each per owner. No block RAM and no main memory is added; the
records use the window the saved-state page already sized.

The saved-state page's area table lists 772 LUT and 377 FF for
`KL_nvm_backend` at 1x1 with 30 names. That row predates the #484 contract:
both recipes return 1,030 LUT and 468 FF for the same parameters at the
current source. Ticket T7 records it.

Time, EXECUTED in model cycles of the processor clock: the dispatch hold-off
of a latch lasts 10 cycles for a scalar, 114 for a name, and at most 179 for
a port's map at 1x1 and 115 at 8x8. The whole boot restore, both walks,
ends by cycle 7,606 after reset at 1x1 and 13,889 at 8x8 (V1b, which now
restores every group), and the entity is enabled 7 and 6 cycles later. The
binding walk's preload phase, the listener admitted to nothing else, lasts
6 cycles from the first offer to the walk's terminal at 1x1 (both sinks
bound) and 12 at 8x8 (sinks 0 and 8 of nine), and the release follows 2
cycles later (L00). A restore that meets a silent wait ends within the
deadline plus its roll-back: 20,657 cycles after the stall began in W4. A
silent BINDING walk ends 19,998 cycles after its silence began, and the D3
walk 20,660 cycles after that, meeting the drained port (W13: "silence from
64, the binding walk's terminal at 20062", "D3 terminal at 40722", "entity
enabled at 40733"). The model's memory answers in 2 or 3 cycles; the
product's in about 1.4 µs, so every figure grows on the board (UNRESOLVED 8).

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
- A D3 restore is all or nothing against a transport failure in either pass
  (a device error the port reports, a torn read, a difference between the
  passes, a descriptor fault, a deadline): complete, or every D3 group at its
  default with restore fail set, or CLOSED when its image cannot be proven.
  It is per record against a bad frame or a value that fails a rule the
  restore fetched.
- A failed restore never rewrites the saved state: the slot still holds what
  the controller last saved, and the next successful restore brings it back.
- The entity is enabled only when the restore of both walks is done. A
  restore that cannot prove its image keeps the entity dark (CLOSED,
  fail-closed). A silent persistence device no longer does: both walks end
  at their deadlines, and commands are served on defaults with restore fail
  set.
- No AECP program runs from reset until the restore's terminal. A command
  that arrives in that interval waits in the dispatch, at most the two
  deadlines plus the walks, whatever the listener's producers do; before
  the entity is enabled no controller has been told the entity exists.
- No ACMP listener command, talker event, START/STOP request or timer
  expiry reaches the listener from reset until the binding walk's drained
  terminal (S4). What arrives waits at its producer and is served after the
  release, in the listener's own priorities, after the restored image: a
  live change still wins, and a read-only command no longer erases a saved
  binding. A talker-directed ACMP command queued behind a held listener one
  waits with it. From the release the listener serves live work while the
  D3 walk runs and before the entity is enabled: the entity enable gates
  ADP advertising, not traffic (section 8.1).
- An AECP command can wait for one latch window, at most 179 cycles in the
  model, before its program is dispatched.
- The port serves two managers. A binding request can wait for one D3 record
  operation. The binding manager fails its walk on a device error or its
  deadline instead of defaulting a record or waiting for ever (seams S1 and
  S3). A read either manager abandons keeps the port QUARANTINED until its
  device answers, for ever if it never does: persistence then stays
  unavailable until reset, commands do not.
- The port reports a terminal cause and the descriptor store's memory face
  gains a guard (seams S1 and S2): processor changes, prerequisites of
  stage 1 with S3 and S4 (tickets T8 and T9). Stage 1's roll-back resets
  the descriptor store as well as the dynamic-state store.
- The processor's restore verdicts mean both walks; the PP_STAT and PP_CTRL
  rows of [`REGISTER_MAP.md`](../reference/REGISTER_MAP.md) owe the update.
  A bench script that writes the enable without starting the restore walk
  now finds the entity dark.
- `milan_init`'s order changes, and with it the ledger fact
  `firmware_boot_order` and the order block of
  [`BAREMETAL_FIRMWARE.md`](../integration/BAREMETAL_FIRMWARE.md); `nvm_boot`
  starts the walk on every path. The new order is mandatory: under the old
  one the restore cannot prove its image and ends CLOSED.
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
  dynamic-state store and the descriptor store walking a real AEMI image of
  the shape; since revision d the ACMP listener, unchanged and compiled from
  its pinned path with its ROM from the pinned generator, and the timer
  service on its arm and expiry faces. SHIPPING: `KL_nvm_backend.sv`, and
  the firmware `milan_baremetal.c` compiled for the host through its two CSR primitives,
  with firmware changes 1 and 3 of section 5.3 as counted substitutions.
  AMENDED PROTOTYPES of two pinned modules: the port with its terminal cause
  (S1) and the binding manager with the cause and its deadline (S1, S3).
  Each is the pinned file with declared amendments only, renamed so it
  cannot pass for the pinned RTL, and the run script refuses any other
  difference. PROTOTYPE: the writer, the arbiter, the descriptor memory
  guard (S2) and the listener's admission gate (S4). TRANSCRIBED: the
  parent glue of `KL_pp_shadow.sv` with the enable the restore releases,
  and under `D3_TRACKED` the glue as it ships, with the PINNED port and
  binding manager, no guard and no admission gate.
- MODELS, each stated where it is coded: the µCPU is a bus-functional model
  running programs as state-bus operations, with the dispatch hold-off and
  the commit marks after the write; the parent's map plane is C++, keyed as
  `milan_datapath.sv` keys it (an input mapping by cluster, an output
  mapping by stream channel owned by one port); the descriptor memory is an
  in-order FIFO that accepts a request while earlier bursts are owed, as the
  parent's asynchronous CDC FIFO does, and ends a burst at an error beat, as
  `pp_desc_bridge` does, with no watchdog of its own, so the store's is the
  only one; the edit face is one staged set, where the product has phases 0
  to 5; the producers of the listener's work faces (the dispatch head, the
  event router's sticky presentation, the AECP engine's START/STOP request,
  injected expiries) hold a presented request until its handshake, and the
  listener's RX slot read, TX slot pool and PRNG answer on its faces'
  timing.
- THE FORMAT JUDGE has two modes. SYNTHETIC, in every case but the V1s ones:
  the stream's default, or a narrower Milan Base AAF format of 1, 2, 4, 6 or
  8 channels in either direction, which admits narrower OUTPUT formats the
  product refuses. SHIPPING, in the V1s cases: `milan_datapath.sv`'s
  `sfv_supported_w` transcribed, an output's declared format alone and an
  input's 1/2/4/6/8 family. The results label every case whose stimulus
  narrows an output, including every case booting from V1a's slots.
- THE ROLL-BACK'S OWNERS are modelled by their resets: the model drives the
  pinned stores' own `rst_n` from the writer's strobe, and the C++ map plane
  returns its ports to their reset sets. The product needs one soft-reset
  input per owner (section 5.1); a store-local re-walk request that also
  returns its fetch watchdog to zero would serve the descriptor store
  equally. The guard and the admission gate take the hard reset only. The
  STAGE-1 build (`D3_STAGE1`) rolls back the two stores and not the map
  plane, stage 1's scope; it runs the S1 cases.
- HARNESS-ONLY FACES, never product wiring: peeks that read every
  dynamic-state row and the name table through the hierarchy for the
  cleared-first and roll-back checks; a knob that lends the state bus to the
  stale-store control before the restore; the change-snoop knob; and the
  fault injection: memory reads that fail, are held back for a count or for
  ever, or are released relative to the writer's or the binding manager's
  deadline; faces made silent; a descriptor memory made to fail, delayed
  or answering one error beat; window bytes changed between the passes
  (V18b, V18c); a knob that requests the enable from reset (W14); expiries
  injected on the timer bus in a cycle the timer service is quiet (L07);
  and peeks at the listener's state, holder and pending expiries.
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
  beat, real flash, placement, firmware change 2 (the model's shape always
  matches), the product's producers of the listener's faces themselves (the
  dispatch queue and its overflow, the event router's coalescing, ADP
  discovery, the START/STOP µprogram), which the model reduces to their
  handshakes, the edit face's phases, and the product memory paths' own
  timing, their CDC FIFOs and `pp_desc_bridge`'s watchdog and poison.
- THE LISTENER'S EVENTS ARE COUNTED. For each kind of acceptance, at the
  listener's faces and at the producers, a run prints how many, how many
  while the gate owned the faces, the first 16 cycles and the last one, and
  per face the cycles a producer's pop and the listener's take disagreed;
  record writes are runs of identical writes. A held level costs a counter,
  not a line a cycle, and every graded property reads those counts.
- THE RUNNER'S VERDICT IS ITS EXIT STATUS. `run.py run` exits 0 only with no
  verdict failure, 1 with each failure named, 2 when a build is missing or
  unknown; a planned case that did not run is a failure; a mutant counts as
  killed only when every check the run script names for it fails, each in a
  run that COMPLETED, and the verdict line shows each check's own state.
  With no build named it is the FULL run and writes the results beside it;
  naming builds makes it a FOCUSED run, which says so and writes elsewhere.
  `run.py controls` proves it on doctored copies of the built binaries,
  through the real CLI, each against its exit status and diagnostic: a
  healthy binary in place of M01 ("MUTANT M01_taint_ignored: SURVIVED",
  exit 1); an executable
  that fails before its scenario in place of M06 ("NOT COMPLETED", exit 1,
  where round one counted it killed); a failed baseline, the 1x1r2 base
  running RPL_rate's binary ("UNEXPECTED base-1x1r2 V1b_restore_everything
  value_restored:0x02 FAIL", exit 1); the tracked build replaced by the
  prototype ("TRACKED K1_single_change_converges : converged@end DOES NOT
  FAIL", exit 1); the stale seeding removed under M13 ("CONTROL ... NOT AS
  REQUIRED", exit 1); an absent tracked build ("REFUSED: tracked-1x1 is not
  built", exit 2); a healthy binary in place of TRG_fmto with V1s_a's
  declared-format SET dropped, so one of its two named checks kills and the
  other does not ("MUTANT TRG_fmto: SURVIVED by ... [SURVIVED] AND ...
  [KILLED]", exit 1); an empty selection (exit 2). All eight as required.
- TOTALS: 76 builds (the two shipped shapes, the synthetic shape, the
  stage-1 build, the tracked glue and 71 mutants), 386 graded runs, 4,560
  graded checks, 0 verdict failures, exit 0, from an empty output tree.
  Every one of the 71 mutants is killed by every check the run script names
  for it, in completed runs; the vacuity control holds; the K15 premise is
  reached; the tracked glue fails its 9 named checks and passes its 4. The
  reviewers' own probe scripts, rerun in copies adapted only in their paths
  and the one seam each that moved, hold as each reviewer demanded: 9 runs
  of R217's and 6 of R218's round-two probes, 20 of R217's and 12 of R218's
  round-three ones. R217's own round-two and round-three counterexample
  checkers both exit 1 at their counterexample assertions, as they must,
  and the round-three one finds its held counterexample again on LG01. The
  command record lists every command with its real exit status, and the
  sha256 of the 50 other files the evidence commit tracks and of the 19
  repository files the model reads or transcribes, all 69 checked against
  the immutable Git blobs.

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
4. **The port has no deadline and no cancellation** (processor issue 15,
   open: its criterion 2, that the port serves the next request, is
   undelivered, and its proposed amendment is unaccepted). This contract no
   longer depends on it for availability: the writer bounds its own waits,
   and S3 and S4, prerequisites (T8), bound the binding walk's read and
   preload phases. S4 touches no port operation. What stays open is
   PERSISTENCE recovery: a read either manager abandoned keeps the port
   quarantined until its device answers, so a device that never does leaves
   every later change pending until reset. This page claims no reuse of
   that port, and neither closes nor amends issue 15.
5. **The port's cause (S1) is a prerequisite, not an existing feature.** At
   the pinned port a device error during a header read and an unframed
   header are the same pulse. The transaction relies on the cause T8 adds,
   and the evidence runs an amended copy of the pinned port. Until T8 lands,
   no stage is implemented and merged (section 10). Processor issue 20's
   defect in the binding manager is closed by the same cause, in T8.
6. **Two debounces.** The writer uses the binding manager's T-NVM-DEBOUNCE
   and the firmware adds its own 1,000 ms. The value of T-NVM-DEBOUNCE is
   still open
   ([section 14](SAVED_STATE_FASTCONNECT.md#14-what-this-page-does-not-decide)).
   A shorter writer debounce costs only port writes to main memory.
7. **The value rules exist twice**, in the programs and in the writer, and
   can diverge. Replaying the records as SET commands through the µCPU would
   remove the copy; it is not costed here.
8. **Time on the board.** The latch windows, the restore time, the
   deadlines of both walks and the descriptor memory's debt wait are model
   cycles; the product's memory latency and GET_AUDIO_MAP hold are not
   measured, and `RS_TMO_CYC_P` at the product clock is a proposal (20 ms),
   to be sized above the descriptor store's whole walk.
9. **Area in context.** The rows are out-of-context measurements and proxy
   estimates. Each stage owes its post-place delta at both shapes.
10. **System unique id and media clock reference** have allocated records
    and no source; nothing here writes them.
11. **An edit that changes nothing** still raises commit beats, so its port's
    record is written again for nothing; the program's FINISH knows, the
    trigger does not.
12. **The writer's alarm is sticky until reset**, as the binding manager's
    is; the snapshot page's UNRESOLVED 7 (forgiveness) covers it too.
13. **Commands before the restore's terminal wait.** Bounded by the binding
    walk's deadline and its preload phase (S4), then the D3 walk's
    deadline, each per awaited event; with a device that never answers,
    about two deadlines plus the walks (W13, L12). ACMP listener commands
    wait for the binding walk's drained terminal only (section 8.9).
14. **The descriptor store does not re-arm its watchdog after a fetch's
    response timed out**, so its next fetch answers an error at once (V23).
    The failure is honest, an error and never stale data, and the store is
    not changed here (T9 records it); the fetch after it succeeds. Inside
    the D3 roll-back, whose one LOCATE is that next fetch, it would end a
    finite late burst in CLOSED; the store's roll-back reset, stage 1's
    (section 10), re-arms the watchdog before that LOCATE.
15. **What the model leaves to the implementation lanes.** The listener
    and its timer service are real, but the product's producers of its
    faces are reduced to their handshakes: the dispatch queue's overflow
    policy, the event router's coalescing and ADP discovery are the
    processor's own and stay as they are. The product's edit face has
    phases 0 to 5 where the model stages one set, so an abort inside each
    phase is stage 3's to test. The memory paths' own timing is not
    modelled: the guard's property, no request presented while a burst is
    owed, is what the evidence shows, and the product's path provides it by
    the guard or by a direct-wired bridge (T9).
16. **No listener service during the binding walk.** S4 holds ACMP listener
    work from reset to the binding walk's drained terminal: a request is
    held, never consumed and dropped, but a producer's own queue may refuse
    arrivals behind a held head, and a talker-directed ACMP command queued
    behind a listener one waits with it. A boot that never starts the
    binding walk leaves the listener owned until reset (firmware change 2
    starts the walk on every path).

## 16. Traceability

Milan v1.2 clauses, as the saved-state page lists them
([section 4.1](SAVED_STATE_FASTCONNECT.md#41-what-the-persisted-set-actually-needs)):

| Clause | Item | Records | Where | Executed by |
|---|---|---|---|---|
| 5.3.5.1 | sampling rate | `0x02`.. | 3, 8.3, 10 | V2, V1b at 1x1r2 (synthetic) |
| 5.3.7.1 | Stream Output format | `0x40`.. | 3, 8.2, 8.3, 8.4, 10 | V1s_a, V1s_b, V1s_c under the product's judge; V1b, V6b, V8, V9 under the synthetic one |
| 5.3.7.6 | presentation time offset | `0x50`.. | 3, 7, 8.3, 10 | K1 to K9, K17, K18, V1b, V5 |
| 5.3.8.1 | Stream Input format | `0x30`.. | 3, 8.3, 8.4, 10 | V1b, V1s_b |
| 5.3.8.2, 5.3.8.3, 5.3.8.7 | bound state, binding parameters, started or stopped | `0x20`.. | the binding manager, amended by S1 and S3, and the listener's admission S4 (T8); 6.4, 8.8, 8.9 | K13, K15, W13 to W16, L00 to L13 |
| 5.3.9.1, 5.3.10.1 | channel mappings in and out | `0x60` to `0x7F` | 3, 7, 8.3, 8.4, 10 | K12, K16 (containment only; #501), V1b, V3 to V3g |
| 5.3.11.1 | clock source | `0x0A`.. | 3, 8.3, 10 | K4g, V1b, V2b |
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

The round-three review findings at `ab0fb23f`, with the reviewers' own
severities and lenses. Answering a finding here is not clearing it: each
reviewer re-reviews the new heads and decides.

| Finding | Severity and lenses | Answer | Evidence |
|---|---|---|---|
| R217 R3-F1: unbounded listener preload still defeats the promised command-recovery bound | MAJOR; Conformance, RTL, Robustness, Tests, Docs | the listener's boot-owned admission S4, a prerequisite of stage 1 and of every shippable stage (T8): nothing but the preload reaches the pinned listener from the hard reset to the binding walk's drained terminal; transactions and talker events held at their producers (valid and ready masked), START/STOP admission masked with its completion passed (none can fire while owned), expiries not admitted; the release starts live ACMP work and the D3 walk, and gates the enable; the listener is real and unchanged in the evidence (2, 3 rules 7, 8 and 11, 4, 5.1, 5.3, 6.2, 6.3, 8.1, 8.6, 8.8, 8.9, 10, 11, 12, 13, 14, 15 items 13, 15 and 16) | L00 to L13, L03b, L06b, L10 m1, 0 and p1 at 1x1 and 8x8; LG01 to LG05; tracked L01 and L05; R217's round-three probe, adapted (20 runs), and its own checker |
| R218 R3-F1: stage 1 defers descriptor recovery needed for its finite-timeout acceptance | MAJOR; Conformance, RTL, Robustness, Tests, Docs | the descriptor store's roll-back reset (or a re-walk that also returns its watchdog to zero) is stage 1's, with the dynamic-state store's (T1); the guard's debt survives it, on the hard reset only (T9); stage 2 adds no owner (T2); evidence run on a stage-1 build and a stage-1 slot (3 rule 11, 5.1, 8.6, 8.8, 10, 11, 13, 14, 15 item 14) | S1a to S1h on the stage-1 build and both full builds; ST1, killed by S1c and S1d; R218's reproduction, adapted (12 runs); DG01, DG02 |

The integration clarification on this contract, [PR comment 5762146376](https://github.com/kebag-logic/milan-fpga/pull/503#issuecomment-5762146376),
is not a finding: it asks that S4's release, the D3 terminal's release of
AECP and the combined ADP enable be stated as separate points, with the
live ACMP work after S4 kept apart from a late restore action. Section 8.1
states them, and T1, T4 and T8 say the same.

The round-two review findings at `40d14d92`, with the reviewers' own
severities and lenses, as revision c answered them; the evidence names
below are this revision's, which keeps every round-two control.

| Finding | Severity and lenses | Answer | Evidence |
|---|---|---|---|
| R217 R2-F1, R218 F1: header errors still produce a successful partial restore; equal counts do not prove pass agreement | MAJOR; Conformance, RTL, Robustness, Tests, Docs (both) | the port's terminal cause S1, a prerequisite of stage 1 and of every shippable stage (T8), consumed by the writer and the binding manager; the passes agree record by record; a failed restore is never blank (3 rules 7 and 11, 5.1, 5.2, 6.2, 6.3, 8.6, 8.7, 10, 15 item 5) | H1 to H8, V18, V18b, V18c and the erased control V10 at 1x1 and 8x8, W16 at 1x1; C01, C02, C03, X01, X02, B02, B04; both reviewers' probes, rerun |
| R217 R2-F2: descriptor-memory errors and timeouts bypass the restore transaction | MAJOR; Conformance, RTL, Robustness, Tests, Docs | a rule or revert fetch that fails aborts (cause 6), never a refusal; an unproven image ends CLOSED (cause 7); response isolation S2, a prerequisite (T9), and a roll-back held while the memory owes a burst; a subordinate's timeout is a fault, never progress (3 rules 7 and 11, 5.1, 6.2, 6.3, 8.3, 8.6, 8.8, 10, 15 item 14). Its stage-1 remainder is R218 R3-F1, above | V20, V20b, V20c, V20d, V21, V21b, V21c, V21d, V22, V22b, V23, V17 and the refusal control V2b; DF01, DF02, DF03, IMG01, DG01, DG02; R217's probes, rerun |
| R217 R2-F3: the stages still permit an unbounded binding-walk hold, and T8 promises incompatible recovery | MAJOR; Conformance, RTL, Robustness, Tests, Docs | the bounded binding walk S3, a prerequisite (T8); commands served on defaults; persistence quarantined until the device answers, no reuse claimed; T8 rewritten (3 rules 8 and 11, 5.1, 6.3, 6.4, 8.1, 8.8, 10, 13, 15 items 4 and 13). Its preload-phase remainder is R217 R3-F1, above | W13, W13b, W13c, W15, W16, W14; B01, B03, G05 |
| R218 F6: the output-format oracle admits synthetic behavior without identifying that boundary | MINOR; Tests, Docs | the product's judge transcribed as the SHIPPING mode; every synthetic-judge case labelled; a shipping-legal save and replay graded by value and valid flag; which ordering claims rest on the synthetic judge (8.2, 8.4, 14) | V1s_a, V1s_b, V1s_c; TRG_fmto, RPL_fmto, TRG_fmti and RPL_fmti each killed by a V1s check as well as V1a's or V1b's; the partial-kill control |
| R218 F7: permanent-silence recovery contradicts mandatory quarantine | MINOR; Docs | T8 rewritten: a device that never ends the abandoned read keeps the port quarantined for ever, and no reuse is claimed without a cancellation or device-reset acknowledgement; finite late completion and permanent silence separated (6.4, 8.8, 15 item 4) | W13 (quarantined for ever), W13c and W15 (finite late completion) |

The round-one review findings at `d0256846`, with the reviewers' own
severities and lenses, as revision b answered them; the evidence names
below are this revision's cases, which keep every round-one control.

| Finding | Severity and lenses | Answer | Evidence |
|---|---|---|---|
| R217 F1, R218 F1: two passes do not make restore all-or-nothing | MAJOR; Conformance, RTL, Robustness, Tests, Docs (both) | the restore transaction: roll-back by reset, the pass agreement, `own` from reset (3 rule 7, 6.2, 6.3, 8.6) | V11b, V12 to V16, V18 at 1x1 and 8x8; R01 to R04, X01, M16 |
| R217 F2, R218 F2: the firmware timeout enables the entity without containing the restore | MAJOR; Conformance, RTL, Robustness, Tests, Docs (both) | the deadline, the drain, the three terminals, the enable released by the restore (revision b); the binding walk bounded by S3 (revision c) (3 rules 5 and 8, 5.1, 5.3, 6.4, 8.1, 8.8, 15 items 4 and 13) | W1 to W16, V17, K19; W01, D01, G05, R05, O01, B01, B03 |
| R217 F3: invalid map entries can bypass the value refusal | MAJOR; Conformance, RTL, Robustness, Tests, Docs | the exact unused entry and the hole rule (8.3) | V3a to V3g; P01, P02 |
| R217 F4, R218 F5: permanent pending is still an accepted Stage 3 outcome; the stage release conditions do not exclude the open defects | MAJOR; R217 Conformance, RTL, Robustness, Docs; R218 Conformance, Robustness, Tests, Docs | Stage 3 blocked on #501, every stage declared shippable after #502, pending-and-skip is containment only, the limited work named (3 rule 9, 10, 15 items 2 and 3; T3 to T6). #501 and #502 stay OPEN | K16 (containment only) |
| R217 F5: the evidence runner does not fail its process verdict | MINOR; Tests, Docs | exit statuses, completed-run kills, full and focused runs (14) | the process controls: seven in revision b, eight now with the partial-kill control |
| R218 F3: the runner accepts surviving mutants and failed scenarios | MAJOR; Tests, Docs | the same | the same |
| R218 F4: configuration replay can be deleted without invalidating the evidence | MAJOR; Conformance, Tests, Docs | value AND valid flag for every group and first and last index, exact counts, cleared-first by peeks for every row, name and map, the synthetic two-rate shape (8.2, 14) | V1a, V1b at three shapes; TRG and RPL, nine groups each |
