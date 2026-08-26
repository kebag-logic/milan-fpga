[OBSOLETE + 2026-08-17]

# Milan v1.2 compliance matrix — counters + notifications first

> ## STATUS 2026-08-13 — **EVERY ROW ON THIS PAGE IS STILL NOT IMPLEMENTED — BUT NOT FOR THE REASON THIS BANNER USED TO GIVE.**
>
> An earlier revision of this page, written the same day, said this device
> answers **no** AECP/AEM command at all. **That premise was false and is
> corrected here.** The `protocol-processor` submodule landed its **AECP uCPU**:
> the device is reachable on AECP, it answers `READ_DESCRIPTOR` (0x0004), it
> answers `IDENTIFY_NOTIFICATION`-as-a-command with `BAD_ARGUMENTS`, and it
> answers **every other AECP command with a conformant `NOT_IMPLEMENTED` echo**
> — correct `message_type`+1, correct length, correct `controller_data_length`.
> Never silence, never malformed.
>
> **That changes none of the verdicts on this page, and the reason matters.**
> This page is a matrix of **GET_COUNTERS sets, counter update laws, Table 5.22
> unsolicited notifications and controller liveness**. Not one of those four
> functions exists. A controller now gets a well-formed `NOT_IMPLEMENTED` where
> it used to get nothing, and it still gets no counter, no push, no registry and
> no liveness probe. **An echo is not an implementation** — do not promote a row
> here because the entity answered.
>
> The repository's own AECP/AEM engine, ACMP talker/listener, ADP advertiser and
> lwSRP applicant are still DELETED (USER, explicit and repeated: *"remove the
> old code AECP/ACMP/ADP the lwSRP shall be removed as well. Only use the uCPU
> code"*). The replacement is the protocol processor —
> `hdl/milan/KL_pp_shadow.sv`, instantiated unconditionally by
> `hdl/milan/milan_datapath.sv` — and it owns **ADP, ACMP, SRP and AECP**.
>
> GET_COUNTERS serves the supported descriptor targets. There is still no
> Table 5.22 counter-change producer, no `CONTROLLER_AVAILABLE`
> probe and no `LOCK_ENTITY` to auto-unlock. The processor's **unsolicited** TX
> lane has no producer at all: the Table 5.22 push is genuinely absent, and the
> landed engine drives only the *solicited* lane. **The former `IMPLEMENTED` /
> `PARTIAL` / `VERIFIED` verdicts below are HISTORY.** They are kept, marked as
> such, for exactly one reason: they record which clause was read, what the law
> says and where the mechanism sat — which is the specification the
> function-landing round is built and graded against. Nothing here is a claim of
> coverage today.
>
> **What the landing DID make reachable, and it is not on this page:**
> descriptor-read enumeration — and only once a descriptor image is loaded into
> DRAM. The tracked builder deployment handoff now supplies it when
> explicitly requested; an inspection-only/custom flow that skips the handoff
> still answers `BAD_ARGUMENTS` (the microprogram checks
> `configuration_index` against `configurations_count` before it locates, and an
> invalid image reports a count of zero). `BAD_ARGUMENTS` to every read therefore
> reads as "no image"; `NO_SUCH_DESCRIPTOR` reads as "image loaded, that
> descriptor genuinely absent". The row-level detail is
> in [`PDU_GETTER_SETTER_VERIFICATION.md`](PDU_GETTER_SETTER_VERIFICATION.md).
> **Known gap, kept visible:** Milan Δ7 `ACQUIRE_ENTITY` (`NOT_SUPPORTED` with
> `owner_id` = 0) is **not** distinguished from the generic echo.
>
> **Two counter facts a reader needs before the tables.** The Milan Table 5.4
> **per-STREAM_OUTPUT** counters are live for solicited GET_COUNTERS reads.
> `KL_talker_diag_ctx` is instantiated per declared output. The Table 5.22
> unsolicited change producer remains open. The
> **STREAM_INPUT** counters at the `0x6B8` `A_STRMW_CNT` window are
> **UNAFFECTED and still live** — `KL_avtp_rx_monitor_ctx` still tallies them
> and software still reads them over CSR; what is gone is the AECP command that
> served them.

The clause-by-clause work list of the compliance-extension round (2026-08-05,
USER: "a lot is still not compliant, counter update etc"). Source of law: the
local `Milan_Specification_Consolidated_v1.2_Final_Approved 20231130.pdf` —
clause text was read, not remembered. Source of state as originally written: the
RTL at VERSION `0x0023` + the rv32-g campaign record; firmware VERSION major is
now **2** (`0x0002_0043`) and that RTL is deleted.

**Status vocabulary** — the point of this file is that these are DIFFERENT:

| status | meaning |
|---|---|
| **NOT IMPLEMENTED** | **the current verdict of every row here: the command draws a conformant `NOT_IMPLEMENTED` echo and no function, so the law cannot be exercised at all** |
| VERIFIED | a grader/TB check EXISTS and is green (evidence linked) |
| IMPLEMENTED | RTL present and plausible; NO grader has ever forced the law |
| PARTIAL | some of the clause's items covered, others not |
| MISSING | no RTL behind the law |
| UNKNOWN | not yet inventoried — the round must resolve it |

The four lower verdicts now appear only inside the **"was, before 2026-08-13"**
column. Do not promote one back into a live verdict without the *function* on
the other end of the wire. There **is** an engine on the other end of the wire
now, and it answers every row here `NOT_IMPLEMENTED`; that is a response, not a
counter, a push or a probe.

**How to review this file (human collaborator):** mark any row you know to
be wrong on silicon with `KNOWN-BAD:` + what you observed (controller,
frame, counter value). A row's status only moves to VERIFIED through a
grader, never through reading code — that discipline is what made rv32-g
self-triaging. Verdicts you contribute here become Phase-B grader specs.
Since 2026-08-13 there is a second discipline on top of it: a row cannot leave
NOT IMPLEMENTED until the entity **serves the command's function** on the wire —
answering it `NOT_IMPLEMENTED`, which it now does, is not that. A CSR read of
the underlying tally is real evidence about the tally and no evidence at all
about the clause, which is written about a command.

## Contents

- **[1. GET_COUNTERS sets (5.4.2.25, Tables 5.13–5.17)](#1-get_counters-sets-54225-tables-513517)** — the five sets, each split into two facts that must not be merged: whether the *tally* still exists in fabric, and whether anything can *serve* it. Only STREAM_INPUT keeps its data intact; STREAM_OUTPUT lost the counters themselves.
- **[2. Counter UPDATE LAWS (the "when does it move" half — the named pain)](#2-counter-update-laws-the-when-does-it-move-half--the-named-pain)** — per-counter movement laws, now with the tally's fate per row: STREAM_INPUT laws stay gradeable over CSR, every STREAM_OUTPUT law lost its counter, and the round's old RED row is retired by subtraction rather than fixed.
- **[3. Unsolicited notifications (5.4.5.2 Table 5.22 + 1722.1 7.5.2)](#3-unsolicited-notifications-5452-table-522--17221-752)** — the whole Table 5.22 duty as one open gap: the landed AECP uCPU drives only the solicited TX lane, so the unsolicited lane has no producer at all. The pre-deletion mechanism is kept as the specification the function-landing round rebuilds against.
- **[4. Controller liveness (5.4.5.3)](#4-controller-liveness-5453)** — the 30–60 s monitor timer, probe/retry and auto-deregister family: not implemented, and now with the clause's premise reachable — commands do arrive and are answered, and nothing records who sent them.
- **[5. Not yet inventoried (the "etc" — the round grows this section)](#5-not-yet-inventoried-the-etc--the-round-grows-this-section)** — the open backlog, with the one item on it that is still live today (ACMP timers) called out.
- **[Round protocol](#round-protocol)** — re-scoped: clause reading is unblocked and durable, graders split into CSR-readable and wire-only halves, and most fabric fixes still wait — on the missing functions now, not on a missing responder.

## 1. GET_COUNTERS sets (5.4.2.25, Tables 5.13–5.17)

**The command itself is NOT IMPLEMENTED.** 5.4.2.25 says an entity "shall
implement **and return**" its mandatory sets; this device returns a conformant
`NOT_IMPLEMENTED` and no set. The per-set rows below therefore record two
separate facts a reader must not merge: whether the *tally* still exists in
fabric, and whether anything can *serve* it. Only the first is ever green.

| clause | law | today | was (pre-2026-08-13) | evidence / gap |
|---|---|---|---|---|
| T5.13 AVB_IF mandatory | LINK_UP, LINK_DOWN, GPTP_GM_CHANGED served | **IMPLEMENTED through the processor GET_COUNTERS path** | IMPLEMENTED | `pp_top`, `milan_dp`; sources `cnt_linkup_r/linkdn_r/gmchg_r` |
| T5.14 AVB_IF optional | FRAMES_TX/RX, RX_CRC_ERROR | **NOT IMPLEMENTED** (was allowed-missing, and is now moot) | MISSING (allowed) | optional — RMON has the raw events if ever wanted |
| T5.15 CLOCK_DOMAIN | LOCKED, UNLOCKED served | **SERVED through GET_COUNTERS.** The domain can only select the INTERNAL source today, so CRF-sourced events remain unreachable | IMPLEMENTED | `pp_top`, `milan_dp` |
| T5.16 STREAM_INPUT | the mandatory ten, per sink | **SERVED through GET_COUNTERS.** The tallies also remain readable through the `0x6B8` CSR window | IMPLEMENTED+ | all-context mirror; CRF sink serves its own set |
| T5.17 STREAM_OUTPUT | START, STOP, MEDIA_RESET, TS_UNCERTAIN, FRAMES_TX; **interval semantics** | **IMPLEMENTED FOR EVERY DECLARED OUTPUT.** `KL_talker_diag_ctx` is instantiated per AAF output and CRF, with integrated GET_COUNTERS coverage. The Table 5.22 producer remains separate | IMPLEMENTED | `tkdiag`, `milan_dp`, pinned la_avdecc decoder |

### 1a. What the loss of SET_CLOCK_SOURCE does to §1 and §2

`SET_CLOCK_SOURCE` was the **only** writer of the live CLOCK_DOMAIN
`clock_source_index`. It is now pinned at 0 — the INTERNAL media clock — for the
life of the build, so **the CRF media clock can never be selected**.
`KL_mmcm_drp_servo` and the `KL_media_nco` packet-grid servo are therefore
**structurally off**, and `A_MCSRV_STAT` (`0x8F8`) reads its idle. The CRF Media
Clock Input engine (`KL_crf_rx`) still parses, counts and reports — it simply
cannot steer anything. Every CLOCK_DOMAIN counter law below that turns on "the
domain's current source" is consequently untestable in this build, and the
"source switch behaviour" clause has no reachable switch.

Two more losses belong at the top of this page rather than buried in a row:

* **presentation-time offset is pinned at the Milan 2 ms DEFAULT** for every
  Stream Output, because `SET_MAX_TRANSIT_TIME` (and `SET_STREAM_INFO`'s
  `MSRP_ACC_LAT` sub-command) are gone. That is a **DEFAULT, not a zero** — 0 ns
  would be a presentation time in the past and every listener would drop every
  frame as late;
* **saved-state persistence is gone.** `KL_persist_journal` is deleted and the
  processor's NVM face is a BLANK-FLASH responder (reads `0xFF`, writes accepted
  and discarded). Nothing restores a binding, a format, a mapping list, a name
  or a sampling rate across a power cycle.

## 2. Counter UPDATE LAWS (the "when does it move" half — the named pain)

Every row here needs a Phase-B grader that FORCES the event and reads the
delta, desk first (Verilator) then silicon. None has one today, **and a
GET_COUNTERS grader still cannot be written** — a grader reads the counter over
the wire, and the wire answers `NOT_IMPLEMENTED`. The uCPU landing did not
change this: there is a response path now, and no counter on it. What a grader
*can* still do, for the STREAM_INPUT family only, is force the event and read
the `0x6B8` `A_STRMW_CNT` window over CSR; that proves the tally law and leaves
the *serving* law unproven. Say which one a green result covers.

The `today` column below is the tally's fate. The *command* is NOT IMPLEMENTED
in every row without exception.

| counter | update law to grade | today (the tally) | was (pre-2026-08-13) |
|---|---|---|---|
| AVB_IF LINK_UP/DOWN | +1 per real link cycle; no false counts on JTAG reload / eth_rst | tally lives, CSR-readable; unservable over AECP | IMPLEMENTED, ungraded |
| AVB_IF GPTP_GM_CHANGED | +1 per BMCA GM change (incl our own deposition/recovery); NOT per announce | tally lives, CSR-readable; unservable over AECP | IMPLEMENTED, ungraded |
| CLK_DOM LOCKED/UNLOCKED | +1 per media-lock edge of the domain's current source; source switch behaviour | tally lives, but **the source can no longer switch** (§1a) — the second half of this law is unreachable, not merely ungraded | IMPLEMENTED, ungraded |
| SI MEDIA_LOCKED/UNLOCKED | per lock/unlock EVENT, and the 5.3.8.10 INVARIANT: at ANY time LOCKED==UNLOCKED (unsynced) or LOCKED==UNLOCKED+1 (synced) — a grader can assert it on every read | tally lives (`0x6B8`); assertable over CSR | IMPLEMENTED, ungraded |
| SI STREAM_INTERRUPTED | +1 per playback interruption **for any reason EXCEPT a Controller Unbind** (5.3.8.10: AVTPDU loss, wrong timestamps, over/underrun all count; unbind must NOT) | tally lives; assertable over CSR | law RESOLVED, ungraded |
| SI SEQ_NUM_MISMATCH | +1 per OBSERVATION INTERVAL (≤1 s, impl-chosen) containing ≥1 non-sequential sequence_num — NOT per event | tally lives; assertable over CSR | IMPLEMENTED, ungraded (verify interval semantics, not per-frame) |
| SI MEDIA_RESET | +1 per observation interval in which the **mr bit TOGGLED** in any received AVTPDU | tally lives; assertable over CSR | law RESOLVED, ungraded |
| SI TIMESTAMP_UNCERTAIN | +1 per observation interval with any tu=1 AVTPDU | tally lives; assertable over CSR | IMPLEMENTED, ungraded |
| SI **RESET LAW** | ALL Table 5.6 counters reset to ZERO on the not-bound→bound EDGE; explicitly NOT reset on unbind (5.3.8.10 final para) — prime suspect for the 08-05 KNOWN-BAD stream-input reports | tally + reset edge live; the bind edge now comes from the **protocol processor's** bind record, so the grader's force path changed even though the law did not | IMPLEMENTED (`KL_avtp_rx_monitor_ctx` header cites M-5.3.8.10, per-stream `bind_rise_i` pulses), ungraded — the grader must force bind→traffic→unbind (HOLD)→rebind (ZERO), incl the REBIND-while-bound path where the pulse could be missed. The fast-connect path it also named is unreachable now: nothing persists a binding |
| SI UNSUPPORTED_FORMAT | frames not matching the CURRENT format (proven live 07-27 at 8ch-vs-2ch) | tally lives — and it is now the **only** format feedback a bench has, since `SET_STREAM_FORMAT` is gone and a listener's format can no longer be changed | VERIFIED (campaign) |
| SI LATE/EARLY_TIMESTAMP | presentation-time window comparisons | tally lives; note the talker-side window it is judged against is pinned at the 2 ms default (§1a) | IMPLEMENTED, ungraded at law level (0.44% stress row pending taps build) |
| SI FRAMES_RX | **STANDARD (USER-corrected 08-05)**: ATDECC defines the quantity (frames, Table 7-157), Milan bounds the update cadence (≤1 s interval; the 'not in line' note covers only the OUTPUT table) — count frames, publish COALESCED at the interval close (~8000/s visible, batched 1/s) | tally lives in `KL_avtp_rx_monitor_ctx` (frx accumulator), TB-verified (incl the TV+TNV==FRX identity) | IMPLEMENTED |
| SO STREAM_START/STOP | +1 per licence open/close (ACMP bind + SRP settle; START_STREAMING refusal is 5.4.2.19-mandated and must NOT count) | **COUNTER GONE** — `KL_talker_diag_ctx` is not instantiated | IMPLEMENTED, ungraded |
| SO MEDIA_RESET / TS_UNCERTAIN | talker-side laws — clause read needed (5.3.9.x area) | **COUNTER GONE** | UNKNOWN |
| SPO mappings NV-restore | 5.3.9.1: output channel mappings SHALL persist in non-volatile memory across power cycles (input twin 5.3.10.1) | ADD/REMOVE/GET audio mappings and their atomic live projections are implemented. Persistence is not: the processor NVM face is still backed by a blank-flash responder in the root integration | MISSING (recorded deviation, issue #70) |
| GET_MILAN_INFO TALKER_DYNAMIC_MAPPINGS_WHILE_RUNNING | 5.3.9.1 + Table 5.20 (PDF p58, read 08-05): bit 30 value 0x00000002, SHALL be set by an entity accepting mapping edits while the Stream Output streams | GET_MILAN_INFO is served with this feature clear. Output ADD and REMOVE are accepted only while every referenced Stream Output is stopped; a running target returns BAD_ARGUMENTS without mutation | COHERENT: the advertised feature and command admission rule agree |
| SO FRAMES_TX | same coalesced-frames law (Table 5.4 wording + reset-on-start) | **COUNTER GONE** — the `facc` accumulator lived in `KL_talker_diag_ctx` | IMPLEMENTED, TB-green |

## 3. Unsolicited notifications (5.4.5.2 Table 5.22 + 1722.1 7.5.2)

**The whole duty is NOT IMPLEMENTED.** An unsolicited notification is an AECP
response with `u=1`. The AECP uCPU landed and drives the processor's
**solicited** TX lane; the **unsolicited** lane has no producer at all. There is
no registry to register into — `REGISTER_UNSOLICITED_NOTIFICATION` draws the
generic `NOT_IMPLEMENTED` echo, which registers nothing — no trigger path and no
transmitter. The `was` column is the specification the function-landing round
rebuilds against, including the residues that were still open when the plane was
deleted.

| trigger | law | today | was (pre-2026-08-13) |
|---|---|---|---|
| state-modifying command | successful response ⇒ IMMEDIATE unsol to all OTHER registered controllers (7.5.2 list) | **NOT IMPLEMENTED** — there are no state-modifying commands either | IMPLEMENTED (`unsol_pend4_r` SET-response replay); coverage of the FULL 7.5.2 command list was never verified |
| GET_STREAM_INFO push | on ANY of 13 items: stream ID, acc latency, dest MAC, MSRP talker reg state, failure code/bridge, listener reg state, talker decl state, VLAN, bound, probing, ACMP status, started/stopped | **NOT IMPLEMENTED**. Note several of the 13 items are still *changing* underneath — the bind, the talker declaration and the SRP state are the protocol processor's class-D face and move exactly as before; nothing publishes them to a controller, and `GET_STREAM_INFO` itself is not served either | IMPLEMENTED (0x0024): talker ta/lo edge, listener change-signature with a 16 ms settle dwell, sink 0 + the CRF sink. RESIDUE: sinks 1..N-1 had no per-sink signature |
| GET_AVB_INFO push | on GM, propagation delay, domain, asCapable, class-A priority, class-A VID | **NOT IMPLEMENTED** | IMPLEMENTED (0x0024) off {GM, domain, SR VID, asCapable, pdelay[31:8]}; pdelay quantized to 256 ns and 1 Hz-bounded as anti-churn policy, not as a Table 5.22 bound |
| GET_AS_PATH push | on gPTP path sequence change | **NOT IMPLEMENTED**; the `0x7DC` AS_PATH staging port accepts writes and discards them | IMPLEMENTED (0x0024) off {GM, parent bridge ckid} |
| GET_COUNTERS push | on counter update, ≤1/s per descriptor | **NOT IMPLEMENTED**, and for the STREAM_OUTPUT descriptor the counters themselves are gone (§1 T5.17) | PARTIAL: input 0 + talker per-descriptor + AVB_IF + CLOCK_DOMAIN. RESIDUE: input sinks ≥1 and the CRF input had no push |
| LOCK_ENTITY push | on the 1-minute AUTO-unlock, to registered controllers | Implemented. `ACQUIRE_ENTITY` returns `NOT_SUPPORTED`; `LOCK_ENTITY` owns and expires the live entity lock; the level reaches the root CSR and map writers; local map writes are refused while locked; auto-unlock drives the registered-controller notification path | processor lock and notification cases plus root `milan_dp` T66 |
| DEREGISTER push | when the entity auto-deregisters a controller (to it only) | **NOT IMPLEMENTED** | MISSING (suspected) |

## 4. Controller liveness (5.4.5.3)

**NOT IMPLEMENTED.** The whole clause is about tracking controllers that have
issued AECP commands and probing them with `CONTROLLER_AVAILABLE`. This device
now *receives* AECP commands and answers them, so the premise of the clause is
reachable — and none of the mechanism exists: no per-controller table, no
monitor timer, no `CONTROLLER_AVAILABLE` transmitter, and no
`DEREGISTER_UNSOLICITED_NOTIFICATION` to send (the unsolicited TX lane has no
producer). A `CONTROLLER_AVAILABLE` command arriving here draws the generic
`NOT_IMPLEMENTED` echo, which is a response and not liveness tracking.

| law | today | was (pre-2026-08-13) |
|---|---|---|
| per-controller monitor timer, RANDOM 30–60 s, reset on each valid AECP command from it | **NOT IMPLEMENTED** — valid AECP commands do arrive and are answered, and nothing records which controller sent them | MISSING (suspected — no timer found; we answered CONTROLLER_AVAILABLE, we never SENT one) |
| on expiry: CONTROLLER_AVAILABLE probe + 1722.1 9.3.6 retry; any-status reply re-arms | **NOT IMPLEMENTED** | MISSING (suspected) |
| no reply ⇒ deregister + DEREGISTER_UNSOLICITED_NOTIFICATION to that controller only | **NOT IMPLEMENTED** | MISSING (suspected) |

## 5. Not yet inventoried (the "etc" — the round grows this section)

5.4.5.4 identification notification (button — n/a, no panel; verify the
"should"; note `o_identify` is tied 0 in this build, so the IDENTIFY indicator
is **structurally dark** and there is no SET_CONTROL to light it. One narrow,
related behaviour **is** implemented and belongs on the record: an
`IDENTIFY_NOTIFICATION` (0x0026) arriving as a **command** is answered
`BAD_ARGUMENTS`, because IEEE 1722.1 §7.4.39.2's opcode-specific rule beats
§9.3.5.3.3. That is a refusal rule, not identification), 5.4.2.21
REGISTER_UNSOLICITED semantics vs the 4-slot bound (reference uses 16 —
behaviour at slot exhaustion?), the full 7.5.2 command list vs the pend4
replay, ACMP timer table 5.5.2.3 (**the one live item in this list** — ACMP is
the protocol processor's and its timers are exercisable today), redundancy
clauses (n/a on this bench — secondary uncabled), 5.4.4 SET_* family acceptance
laws beyond formats.

## Round protocol

**Re-scoped 2026-08-13.** Phases A–D below were written for a round that fixed
a live AECP engine. The AECP uCPU has since landed, and it changed nothing on
this page: three of the four phases are still blocked, now on the *functions*
(`GET_COUNTERS`, the Table 5.22 push, the liveness family) rather than on the
absence of a responder. The honest sequencing is:

* **Phase A (clause reading) is unblocked and is the durable half of this page.**
  Resolve every UNKNOWN by reading the clause, never by reading our code first.
  A clause verdict does not expire when an engine is deleted, and every verdict
  captured here is what the function-landing round is graded against.
* **Phase B graders split.** A grader that forces the event and reads the tally
  over CSR is writable today for the STREAM_INPUT family (`0x6B8`
  `A_STRMW_CNT`) and for the AVB_IF/link events. A grader that reads a counter
  or observes a push **over the wire** is still not writable — the wire answers
  `NOT_IMPLEMENTED`. The one wire-level grader the landing *did* unblock is the
  echo contract itself (`message_type`+1, length, `controller_data_length` on a
  `GET_COUNTERS` command), and it grades §9.3.5's duty to respond, not any row
  on this page. Do not stub one and call a row graded.
* **Phase C fabric fixes** are unblocked only where the mechanism survives:
  the RX-monitor tallies, the bind edge (now from the protocol processor), the
  SRP/ACMP/ADP behaviours. Everything else waits.
* **Phase D** (identical-plan re-run with every delta attributable) is unchanged
  in method, but its baseline moved: firmware VERSION major is now 2.
