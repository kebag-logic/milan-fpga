# Milan v1.2 compliance matrix — counters + notifications first

The clause-by-clause work list of the compliance-extension round (2026-08-05,
USER: "a lot is still not compliant, counter update etc"). Source of law: the
local `Milan_Specification_Consolidated_v1.2_Final_Approved 20231130.pdf` —
clause text was read, not remembered. Source of state: the RTL at VERSION
`0x0023` + the rv32-g campaign record.

**Status vocabulary** — the point of this file is that these are DIFFERENT:

| status | meaning |
|---|---|
| VERIFIED | a grader/TB check EXISTS and is green (evidence linked) |
| IMPLEMENTED | RTL present and plausible; NO grader has ever forced the law |
| PARTIAL | some of the clause's items covered, others not |
| MISSING | no RTL behind the law |
| UNKNOWN | not yet inventoried — the round must resolve it |

**How to review this file (human collaborator):** mark any row you know to
be wrong on silicon with `KNOWN-BAD:` + what you observed (controller,
frame, counter value). A row's status only moves to VERIFIED through a
grader, never through reading code — that discipline is what made rv32-g
self-triaging. Verdicts you contribute here become Phase-B grader specs.

## 1. GET_COUNTERS sets (5.4.2.25, Tables 5.13–5.17)

| clause | law | status | evidence / gap |
|---|---|---|---|
| T5.13 AVB_IF mandatory | LINK_UP, LINK_DOWN, GPTP_GM_CHANGED served | IMPLEMENTED | response_builder `DESC_AVB_INTERFACE` arm, mask 0x23; sources `cnt_linkup_r/linkdn_r/gmchg_r` |
| T5.14 AVB_IF optional | FRAMES_TX/RX, RX_CRC_ERROR | MISSING (allowed) | optional — RMON has the raw events if ever wanted |
| T5.15 CLOCK_DOMAIN | LOCKED, UNLOCKED served | IMPLEMENTED | mask 0x03 from `in0_cnt_locked/unlocked` (RX monitor media-lock) — talker-only operation honestly reads 0 |
| T5.16 STREAM_INPUT | the mandatory ten, per sink | IMPLEMENTED+ | all-context mirror since 0x0019; per-index verified at desk; CRF sink serves its own (la_avdecc 0xF3F check passes). Extras TIMESTAMP_VALID/NOT_VALID are 1722.1-legal — graders must NOT flag them |
| T5.17 STREAM_OUTPUT | START, STOP, MEDIA_RESET, TS_UNCERTAIN, FRAMES_TX; **interval semantics** (the spec's own "not in line with ATDECC" note) | IMPLEMENTED | `KL_talker_diag_ctx` per index incl CRF; interval FRAMES_TX since 0x001B-era fix |

## 2. Counter UPDATE LAWS (the "when does it move" half — the named pain)

Every row here needs a Phase-B grader that FORCES the event and reads the
delta, desk first (Verilator) then silicon. None has one today.

| counter | update law to grade | status |
|---|---|---|
| AVB_IF LINK_UP/DOWN | +1 per real link cycle; no false counts on JTAG reload / eth_rst | IMPLEMENTED, ungraded |
| AVB_IF GPTP_GM_CHANGED | +1 per BMCA GM change (incl our own deposition/recovery); NOT per announce | IMPLEMENTED, ungraded |
| CLK_DOM LOCKED/UNLOCKED | +1 per media-lock edge of the domain's current source; source switch behaviour | IMPLEMENTED, ungraded |
| SI MEDIA_LOCKED/UNLOCKED | per lock/unlock EVENT, and the 5.3.8.10 INVARIANT: at ANY time LOCKED==UNLOCKED (unsynced) or LOCKED==UNLOCKED+1 (synced) — a grader can assert it on every read | IMPLEMENTED, ungraded |
| SI STREAM_INTERRUPTED | +1 per playback interruption **for any reason EXCEPT a Controller Unbind** (5.3.8.10: AVTPDU loss, wrong timestamps, over/underrun all count; unbind must NOT) | law RESOLVED, ungraded |
| SI SEQ_NUM_MISMATCH | +1 per OBSERVATION INTERVAL (≤1 s, impl-chosen) containing ≥1 non-sequential sequence_num — NOT per event | IMPLEMENTED, ungraded (verify interval semantics, not per-frame) |
| SI MEDIA_RESET | +1 per observation interval in which the **mr bit TOGGLED** in any received AVTPDU | law RESOLVED, ungraded |
| SI TIMESTAMP_UNCERTAIN | +1 per observation interval with any tu=1 AVTPDU | IMPLEMENTED, ungraded |
| SI **RESET LAW** | ALL Table 5.6 counters reset to ZERO on the not-bound→bound EDGE; explicitly NOT reset on unbind (5.3.8.10 final para) — prime suspect for the 08-05 KNOWN-BAD stream-input reports | IMPLEMENTED (`KL_avtp_rx_monitor_ctx` header cites M-5.3.8.10, per-stream `bind_rise_i` pulses), ungraded — the grader must force bind→traffic→unbind (HOLD)→rebind (ZERO), incl the fast-connect and REBIND-while-bound paths where the pulse could be missed |
| SI UNSUPPORTED_FORMAT | frames not matching the CURRENT format (proven live 07-27 at 8ch-vs-2ch) | VERIFIED (campaign) |
| SI LATE/EARLY_TIMESTAMP | presentation-time window comparisons | IMPLEMENTED, ungraded at law level (0.44% stress row pending taps build) |
| SI FRAMES_RX | interval count at class rate (~8000/s @ 48k/A) | VERIFIED (campaign, H1-fixed graders) |
| SO STREAM_START/STOP | +1 per licence open/close (ACMP bind + SRP settle; START_STREAMING refusal is 5.4.2.19-mandated and must NOT count) | IMPLEMENTED, ungraded |
| SO MEDIA_RESET / TS_UNCERTAIN | talker-side laws — clause read needed (5.3.9.x area) | UNKNOWN |
| SPO mappings NV-restore | 5.3.9.1: output channel mappings SHALL persist in non-volatile memory across power cycles (input twin 5.3.10.1) — recorded deviation since 0x001C (no NV plane); journal decision (#7) is the enabler | MISSING (recorded deviation) |
| GET_MILAN_INFO TALKER_DYNAMIC_MAPPINGS_WHILE_RUNNING | 5.3.9.1/5.4.4.1: if we accept mapping edits while streaming (we do — the walk has no streaming refusal), the bit SHALL be set | UNKNOWN — check the features word |
| SO FRAMES_TX | interval count | VERIFIED (campaign) |

## 3. Unsolicited notifications (5.4.5.2 Table 5.22 + 1722.1 7.5.2)

| trigger | law | status | evidence / gap |
|---|---|---|---|
| state-modifying command | successful response ⇒ IMMEDIATE unsol to all OTHER registered controllers (7.5.2 list) | IMPLEMENTED | `unsol_pend4_r` SET-response replay — coverage of the FULL 7.5.2 command list unverified |
| GET_STREAM_INFO push | on ANY of 13 items: stream ID, acc latency, dest MAC, MSRP talker reg state, failure code/bridge, listener reg state, talker decl state, VLAN, bound, probing, ACMP status, started/stopped | PARTIAL | ta/lo state-edge push exists (`unsol_pend_r`); the other items (sid/dmac/VLAN changes, bound, probing, ACMP status, started/stopped) not inventoried |
| GET_AVB_INFO push | on GM, propagation delay, domain, asCapable, class-A priority, class-A VID | PARTIAL | `unsol_pend3_r` fires on link/GM edge; pdelay/asCapable/priority/VID changes not inventoried (pdelay churns — rate policy needed) |
| GET_AS_PATH push | on gPTP path sequence change | MISSING (suspected) | AS_PATH CSRs exist (0x730/4); no push wiring found |
| GET_COUNTERS push | on counter update, ≤1/s per descriptor | PARTIAL | input (`pend2`) + talker (`pend5`, per-descriptor limiter) + AVB_IF (via `pend3`); CLOCK_DOMAIN counter push not found |
| LOCK_ENTITY push | on the 1-minute AUTO-unlock, to registered controllers | UNKNOWN | lock exists (e41a8a9b hardened); auto-unlock timer + push not inventoried |
| DEREGISTER push | when the entity auto-deregisters a controller (to it only) | MISSING (suspected) | requires §5.4.5.3 below |

## 4. Controller liveness (5.4.5.3)

| law | status |
|---|---|
| per-controller monitor timer, RANDOM 30–60 s, reset on each valid AECP command from it | MISSING (suspected — no timer found; we answer CONTROLLER_AVAILABLE, we never SEND one) |
| on expiry: CONTROLLER_AVAILABLE probe + 1722.1 9.3.6 retry; any-status reply re-arms | MISSING (suspected) |
| no reply ⇒ deregister + DEREGISTER_UNSOLICITED_NOTIFICATION to that controller only | MISSING (suspected) |

## 5. Not yet inventoried (the "etc" — the round grows this section)

5.4.5.4 identification notification (button — n/a, no panel; verify the
"should"), 5.4.2.21 REGISTER_UNSOLICITED semantics vs the 4-slot bound
(reference uses 16 — behaviour at slot exhaustion?), the full 7.5.2
command list vs our `pend4` replay, ACMP timer table 5.5.2.3, redundancy
clauses (n/a on this bench — secondary uncabled), 5.4.4 SET_* family
acceptance laws beyond formats.

## Round protocol

Phase A: resolve every UNKNOWN by reading the clause (never by reading our
code first). Phase B: one grader per row BEFORE any fix — TB event-forcing
at desk, harness rows live (subscribe a second controller for the
push-to-others laws). Phase C: fabric fixes. Phase D: identical-plan
rv32-h re-run; every delta attributable.
