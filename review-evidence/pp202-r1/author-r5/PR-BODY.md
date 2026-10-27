[A676e]

Closes #202

After a MAAP conflict, a source whose Stream ID has been on the wire moves to a new, distinct Stream ID at the next `ALLOC_DA` grant, and a declaring source declares it at once, with no `T-SRP-LEAVEALL2` wait. The processor publishes each source's current Stream ID on one new top-level output, `src_stream_id_o[N_STREAM_OUT_P*64-1:0]` (the owner decision on #202, option A). `PROBE_TX`, GET_TX_STATE and the Talker Advertise carry it. Every other path that would declare an ID again with another FirstValue either moves it or waits two LeaveAllTime periods: a disable of a declared source moves it, and an SR-class PCP change keeps the ID and waits, also when the declaration was withdrawn before the change. No move takes an ID that any source declared within the last two LeaveAll periods, and a return granted inside one `T-MRP-JOIN` still sends the withdrawn ID's Leave before the new ID's first Talker Advertise.

This revision addresses the reviews of PR #204 at `a8aa626e` (R710-1, R709-1), at `ebb1f001` (R709-2, R710-2) and at `429c909c` (R710-3, R709-3). The RTL is that of `429c909c`; this revision changes tests, mutation records and documents only.

## Clauses

- IEEE 802.1Q-2018 35.2.2.8 (normative): "MSRP does not support changes in any of the FirstValue fields for an existing StreamID". A Talker that brings a new Stream up "with a different FirstValue, utilizing the same StreamID" must leave two LeaveAllTime periods (Table 10-7) after removing the old registration. The rule is about the StreamID, whichever source declared it before. The destination address and VID are in DataFrameParameters and the PCP in PriorityAndRank (35.2.2.8.5), all in FirstValue.
- IEEE 802.1Q-2018 10.7.7 and Table 10-3: one Applicant per attribute value. Lv! takes AA or QA to LA, whose next tx! sends the Lv; a Join! for another attribute value does not cancel it.
- Milan v1.2 Table 5.3 is in 5.3.7.5, "Plug-and-play SRP parameters (informative)". It leaves the two last bytes of the Stream ID to the PAAD "to distinguish between the different Streams it is sourcing from this AVB interface", and lets the PAAD use "the same Stream ID as before, or another Stream ID".
- Milan v1.2 5.5.4.1 step 3 and Table 5.42: `PROBE_TX` answers `TALKER_DEST_MAC_FAILED` while the source has no valid destination address; from the grant on it answers SUCCESS with the new ID and address.
- IEEE 1722.1-2021 7.4.16.2: GET_STREAM_INFO's stream_id is "the current id of the stream". IEEE 1722-2016 4.4.4.8: every stream data AVTPDU carries the StreamID.
- IEEE 802.1Q-2018 10.7.5.4/10.7.5.5 and 35.2.3.1.1: the re-declaration after a move is a Join!, not a New!, so the new ID's first message is sJ, a JoinMt (10.7.6.3); a new StreamID is a new attribute value, which a Registrar in MT registers on rJoinMt! as on rNew! (Table 10-4).

## The move rule (05 F05.12)

- After reset, a source's Stream ID is its `cfg_stream_id_i` slice.
- A move keeps the slice's upper 48 bits and replaces the 16-bit unique ID with the first value, counted up modulo 2^16 from a move cursor, for which {upper 48 bits, unique ID} is no source's current Stream ID, no source's configured Stream ID and no ID in a source's quarantine record. The cursor then moves past it. It starts at `P-N-STREAM-OUT`, the first unique ID past the default {MAC, s} assignment.
- The quarantine *Q* is the longest `T-SRP-LEAVEALL2`, two LeaveAll periods at their longest (F08.1), counted in epochs of *Q* with small saturating counts, so no compare wraps:
  - a move writes the ID it takes its source off into that source's record, unless the record is younger than two epochs; a record refuses its ID for two epochs, more than *Q*;
  - the cursor re-enters the half of the 16-bit unique IDs it is not in only four epochs after it left it, more than 3*Q*. A search that would re-enter sooner ends with no ID: the grant installs its DA, the source keeps its ID, and the declaration waits `T-SRP-LEAVEALL2` from the grant, which comes after the withdrawal, as after a PCP change.
- Distinctness: at most 3 × `P-N-STREAM-OUT` IDs are refused, so one of the first 3 × `P-N-STREAM-OUT` + 1 candidates is free unless the guard ends the search, and the search (one candidate per clock, in the walk that consumes the grant) ends within that many clocks. The result is a whole 64-bit ID that equals no source's current ID, the withdrawn one included, whatever values the integrator provisions. The proof takes `cfg_stream_id_i` as stable since reset (02 §2 rule 4).
- No move takes an ID declared within *Q*: such an ID was taken by a move that passed the cursor over it and left by a later one inside *Q*. If it was taken within 3*Q*, the cursor guard keeps the cursor from reaching it; if earlier, its source's record holds it, because a record younger than two epochs at the leave would have been written after the ID was taken, inside 3*Q*. 05 states the proof. Moves at a conflict's pace never meet the guard: crossing a half takes at least 32,768 − 3 × `P-N-STREAM-OUT` moves, each after a MAAP claim of at least three probe intervals.
- The move is booked by any conflict once the current ID has been declared and by a disable of such a source. It is kept through a disable, and the moved ID stays until reset. An ID that has never been declared is not moved.

## The same-Stream-ID paths, and the owed Leave

After an ID has been declared and withdrawn:

- withdrawn on a lapsed gate (`DA_OK`): the DA is kept. A PCP change enters the same `BACKOFF` as one while declaring, with nothing to withdraw, and arms `T-SRP-LEAVEALL2` from the change. While a PCP change is pending for such a source, no same-ID declaration opens. Without a PCP change the next declaration carries the FirstValue it was withdrawn with;
- withdrawn by a PCP change: the existing gap;
- withdrawn by a conflict or a disable: a move is booked, so the next declaration uses a different ID, or, when the quarantine leaves no ID free, the same ID after `T-SRP-LEAVEALL2`.

A disable and return answered at once re-declares before the withdrawal's Leave has gone out. The SRP talker keeps that Leave (10 §6.3): a gate re-open under another stream_id while the applicant is LA or LO arms the matcher and the records on the new value at once, but leaves the applicant on the old value, in a leave copy, until its next tx! sends the Lv (or the Empty of LO) with the FirstValue it was declared with; the re-open's Join! waits for that tx!, so the new value's first Talker Advertise goes out one `T-MRP-JOIN` later. A re-open on the stream_id the applicant holds keeps the existing LA + Join! = AA. This mirrors the listener's rule for an owed Listener Leave (#188). Nothing back-pressures the gate face.

## Change

- `KL_acmp_talker`: the conflict path (withdraw, invalidate the DA, re-allocate at once, book the move; the grant searches, installs and declares the new ID in the same walk); `EVC_OFF` books the move for a declared ID; `EVC_PCP` from `DA_OK` with a declared ID enters `BACKOFF`; `pcp_hold_w` holds same-ID opens while a PCP change is pending; the quarantine: per source a 16-bit record with a 2-bit epoch count, one half bit and a 3-bit epoch count for the cursor guard, and a grant that finds no ID keeping the ID behind `T-SRP-LEAVEALL2`. `PROBE_TX`, GET_TX_STATE and `DECLARE_TALKER` read the current ID.
- `KL_srp_talker_fsm`: the parked Leave: per source a parked bit and a waiting-Join! bit, the parked {stream_id, DA, VLAN} in flip-flops at a 128-bit stride with the stream_id at bit 0 (so both of its variable-index reads are multiplexers, not barrel shifters), and its TSpec part in distributed RAM.
- `protocol_processor_top`: the one new output, `src_stream_id_o`. No parameter or register map changes.
- Documents: F05.12, the move rule, the quarantine and both proofs, and the same-ID paths (05); the `T-SRP-LEAVEALL2` row (08); REQ-ACMP-010 and GAP-04 (00); the status dictionary and the `maap` face (02); the talker FSM's owed Leave, its storage row and the Join! statement (10, F10.4); the output stream_id owner note (06); the integrator guide; the 09 evidence map; the test READMEs.
- This revision: 02, 05 and 09 name the quarantine by the longest `T-SRP-LEAVEALL2` (F08.1) instead of copying its value; the 09 row states that a record is kept through a move in its first epoch and, past an epoch boundary, in its second; the processor-top README names the SRP talker FSM without the leave copy by its commit (`ebb1f001`).

## Tests

`tb/acmp_talker` (1,545 checks; 1,376 at main):

- E and S1: the conflict path, timed: conflict to new declaration in 1,700 ms, `TALKER_DEST_MAC_FAILED` only before the grant.
- S2 to S4: distinctness (a provisioned collision, another source's configured ID a minute after it moved off it, past its quarantine record, an equal unique ID under another MAC; every slot's whole published ID).
- S5: one full lap of the cursor at a conflict's pace (65,520 moves, 5 ms apart): no unique ID repeats; every declaration is checked against the last withdrawal of its ID, whichever source made it, and none comes inside two LeaveAllTime periods with another DA. The quarantine epochs end every 30 s from reset, since the timebase steps 5 ms or 1 ms at a time. Near the end one source moves twice inside one epoch (its record kept through a move at age 0), and another moves 10 s before an epoch ends and again 1 ms after it, its record then one epoch old. After the wrap the move skips every configured ID, the ID a third source left moments before, both records' IDs and a fourth source's current ID; the new check grades the second record: `S5 a record one epoch old is kept when its source moves again, so the ID it holds is not taken inside the quarantine`, 10,056 ms after that ID's withdrawal (REQ-ACMP-010).
- S6 to S10: the move booked after a withdrawal; the PCP gap after a withdrawal on the configured and a moved ID; the pending-PCP hold; the disable move.
- S11: a declared source disabled and returned 65,528 times inside one millisecond, each return granted at once with a fresh DA: every return moves until the cursor ends the upper half; the next return, whose search would re-enter the lower half, keeps its ID and waits `T-SRP-LEAVEALL2` from the grant (`PROBE_TX` answers SUCCESS with the kept ID and new DA meanwhile); three epochs on a return still keeps its ID, four epochs on it moves again. No ID is declared again with another DA inside two LeaveAllTime periods.

`tb/srp_stream_fsms` (1,435 checks): TP1 to TP9, the owed Talker Leave (the re-open under another stream_id sends the old Lv with its declared FirstValue, then the new JoinMt; the same stream_id; back to the parked one; an LO applicant; no record since reset; a close, a txLA! walk, a received value and the Listener tracker while parked). WK13 grades the leave copy at the four walk shapes (1, 2, 3 and 9 sources).

`tb/pp_top` (10,753 checks): MP8 through the in-scope MAAP engine, the SRP engine and the MAC stream (conflict to new declaration 1,737 ms, the new ID's first Talker Advertise a JoinMt, `PROBE_TX` and GET_TX_STATE byte-exact); MP9: a disable and return the in-scope engine grants at once puts the withdrawn ID's Lv on the wire before the new ID's first Talker Advertise.

On the RTL of `ebb1f001` the round-4 benches fail: the talker suite 8 checks (both history oracles among them: an ID declared again with another DA 65 ms and 0 ms after its withdrawal), the stream-FSM suite 9 (TP1, TP4, TP6 to TP9) and its walk arms 19 (WK13 at all four shapes), and MP9 1 (no Lv for the withdrawn ID).

The record rule a review found ungraded past its first epoch: with the plant that lets a one-epoch-old record be replaced, the talker suite passed all 1,540 checks at `429c909c`. Now it fails 3 of 1,545, the new check among them, and S5's history check shows the breach of 35.2.2.8 it allows: `ab0000000000000b` declared again with another DA 10,056 ms after its withdrawal.

Planted mutants:

- Group `STREAM_ID` of `tb/pp_top/acmp_mutants.py`, 33 of 33 arm runs killed by named checks (30 names). New this revision: a move replacing a record once it is one epoch old (`record_overwritten_after_one_epoch`, 3 failing checks, both of its named checks among them). Earlier this PR: the records refusing nothing (`move_ignores_left_ids`, 2), lapsing after one epoch (`record_lapses_in_one_epoch`, 1) or replaced while young (`record_overwritten_while_young`, 1); the cursor guard removed (`cursor_reenters_early`, 6) or releasing after three epochs (`cursor_guard_three_epochs`, 2); a blocked search declaring the kept ID's new DA at once (`blocked_move_declares_at_once`, 6); and in `KL_srp_talker_fsm` the park removed (`moved_open_skips_leave`: `MP9: a disable and return granted at once still sends the withdrawn ID's Lv`, 1). The other arms keep their named checks; for example the old wait kept fails 128 checks and 9 in the MP section.
- `tb/srp_top/mutants.py`, 15 patches (17 arm runs): every SRP park rule (TP1 to TP9) and the leave copy at every shape (WK13), each killed by its named check.

## Validation at processor main ed211803 and this head

- Every processor suite passes: 1,030,399 checks at main (inherited record), 1,030,593 here (swept at `b2b2bfdb`, whose suite inputs equal this head's; the head adds documents and README records only), 0 failing. Against the previous head only `acmp_talker` moves (1,540 → 1,545).
- The requirement-tag execution check passes on that run (246 tags, 246 evidence lines, 14 suites).
- At this head: lint, the documentation checks (`make check`), the talker suite (1,545) and the processor-top suite (10,753) pass.
- Every campaign that builds a changed file passes: ACMP 98 of 98 with eight goldens; talker retry 62 killed, 7 equivalence and 1 performance control (four with more failing assertions than before, the README re-measured). The RTL is unchanged since the previous head, so the other campaigns' results there stand: SRP 207 arm runs, 18 controls, assertion coverage 142 of 142; MAAP 29 of 29 (pp_top arms 4 and 15 of 46); AECP deadline and hazard-class 67 of 67; dispatch 74 of 74; counters 18 of 18; GET_STREAM_INFO 23 detected; name write killed; notifications 137 of 137; D3 110 of 110; elaboration-guard mutants 160 of 160; name-state 16 of 16; every golden passing; the portability elaboration (42 tops) and the elaboration guards (93 of 93).
- Area: out of context, the parent's `KL_pp_shadow` is 61,219 LUT and 28,334 FF with this head (59,862 and 27,133 before the quarantine and the leave copy). `KL_acmp_talker` alone at 8 sources grows by about 800 LUT (the quarantine) and `KL_srp_talker_fsm` by about 1,600 LUT and 1,000 FF (the leave copy).

## Parent integration and consumer gate

A source's Stream ID is no longer fixed, so an integrator stamps `src_stream_id_o` on the source's stream frames and answers a STREAM_OUTPUT's GET_STREAM_INFO stream_id (selector 2) with it, never with `cfg_stream_id_i`. The milan-fpga wiring is handed over for the pin adoption PR, unchanged from the previous revision. In it the AAF framer stamps the processor's current ID for every talker through an explicit `SID_PP_P` parameter that the datapath sets, so a TCTX unique ID can no longer name another ID than the one the processor declares; the CRF Media Clock Output's stamp and GET_STREAM_INFO selector 2 read `src_stream_id_o`; `KL_pp_shadow` passes the port out; and a specification-facing scenario step pins the precedence. The patch applies cleanly to milan-fpga dev e76a755a and gives the scratch parent's wiring tree exactly.

Two parent legs prove the agreement through a real MAAP conflict, at compressed time: the shipping AX 1x1 shape (AAF talker 0 and the CRF output) and the 8x8 shape (AAF talkers 0 and 1, talker 1's TCTX unique ID named explicitly). The sources bind and stream; a peer ANNOUNCEs the claimed block from a lower MAC; every declaring source withdraws and declares a new ID in under 2 s: 1,735 ms on AX 1x1 and 1,816 ms on 8x8, at this head's pin (50 and 52 checks, no failure). Before and after the move, the AVTP stream_id of every PDU on the wire, the PROBE_TX answer, GET_STREAM_INFO selector 2, the Talker Advertise and `src_stream_id_o` name the same ID, and no PDU carries the withdrawn ID 50 ms after its Leave.

Consumer gate on a scratch clone of milan-fpga dev e76a755a with the wiring applied (never pushed). With the processor pinned at the final RTL (`ffc76f17`, whose consumed inputs `hdl`, `scripts`, `syn` and `Makefile` equal this head's): `pp_shadow` 2,187 checks, `maap` 251, `milan_dp_render` 347, and all `milan_dp` legs 13,685, with zero failures and rc 0 for every command and aggregate verdict; the capture gate covers 43 cases exactly once with verified observations, its four shards and their union returning 0; the static, specification, elaboration and parser gates pass. The final local parent commit pins this head and records its ROM digests (the ROM contents are unchanged); `pp_shadow` (2,187 checks), both recovery legs, their aggregate verdicts and the out-of-context check pass at that pin.

Found earlier and outside this issue, kept for the pin adoption: on parent shapes whose AAF stream count is a power of two above one (8x8, 4x4), the datapath's maap-face source index is one bit narrower than the processor's, so the CRF output's allocation and conflict arrive as source 0's. The CRF output is graded on the AX 1x1 shape, which is unaffected.

## Notes for review

- The quarantine costs a fallback only when disables come so fast that the cursor would re-enter a half of the unique IDs within four epochs of leaving it; then the returning source keeps its ID and declares after `T-SRP-LEAVEALL2`, which §35.2.2.8 allows for the same ID. Conflict-paced moves never reach it.
- The owed Leave costs one `T-MRP-JOIN` of latency only where a Leave is owed. A conflict's re-open never meets the withdrawal's Lv, because the new claim takes three probe intervals; it meets the park only when a LeaveAll or a Leave received in the last `T-MRP-JOIN` has left the idle applicant in LO, and then its first Talker Advertise waits one more `T-MRP-JOIN` (latency only).
- The PCP gap after a withdrawal is counted from the PCP change, conservatively.
- Two reviews gave different exact texts for the same processor-top README line; it carries both: the commit (`ebb1f001`) and "before the leave copy".
- Ports, parameters and register maps: only `src_stream_id_o` is added.
