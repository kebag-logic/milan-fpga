[A676b]

Closes #202

After a MAAP conflict, a source whose Stream ID has been on the wire now moves to a new, distinct Stream ID at the next `ALLOC_DA` grant, and a declaring source declares it at once. There is no `T-SRP-LEAVEALL2` wait on this path any more. The processor publishes each source's current Stream ID on one new top-level output, `src_stream_id_o[N_STREAM_OUT_P*64-1:0]` (the owner decision on #202, option A). `PROBE_TX`, GET_TX_STATE and the Talker Advertise carry it. The SR-class PCP-change path keeps its two-LeaveAllTime gap, because it keeps the Stream ID.

## Clauses

- IEEE 802.1Q-2018 35.2.2.8 (normative): "MSRP does not support changes in any of the FirstValue fields for an existing StreamID". A Talker that brings a new Stream up "with a different FirstValue, utilizing the same StreamID" must leave two LeaveAllTime periods (Table 10-7) after removing the old registration. This rule covers the same StreamID only. The new destination address is in FirstValue (DataFrameParameters), so a new Stream ID needs no wait.
- Milan v1.2 Table 5.3 is in 5.3.7.5, "Plug-and-play SRP parameters (informative)". It leaves the two last bytes of the Stream ID to the PAAD "to distinguish between the different Streams it is sourcing from this AVB interface", and lets the PAAD use "the same Stream ID as before, or another Stream ID".
- Milan v1.2 5.5.4.1 step 3 and Table 5.42: `PROBE_TX` answers `TALKER_DEST_MAC_FAILED` while the source has no valid destination address. From the grant on, it answers SUCCESS with the new ID and address.
- IEEE 1722.1-2021 7.4.16.2: GET_STREAM_INFO's stream_id is "the current id of the stream". IEEE 1722-2016 4.4.4.8: every stream data AVTPDU carries the StreamID.

## The move rule (05 F05.12)

- After reset, a source's Stream ID is its `cfg_stream_id_i` slice.
- A move keeps the slice's upper 48 bits and replaces the 16-bit unique ID. The new value is the first unique ID, counted up modulo 2^16 from a move cursor, for which {upper 48 bits, unique ID} is no source's current Stream ID and no source's configured Stream ID. The cursor then moves past it. It starts at `P-N-STREAM-OUT`, the first unique ID past the default {MAC, s} assignment.
- Distinctness: at most 2 × `P-N-STREAM-OUT` IDs are excluded, so one of the first 2 × `P-N-STREAM-OUT` + 1 candidates is free, and the search (one candidate per clock, inside the walk that consumes the grant) ends within that many clocks. The result is a whole 64-bit ID that equals no source's current ID, the withdrawn one included, whatever values the integrator provisions. An equal unique ID under other upper 48 bits is another ID and is not refused.
- No ID withdrawn moments before comes back with another address. The configured IDs stay excluded after their source has moved off them. The cursor revisits no moved ID within one lap of 2^16 candidates. The move is booked by any conflict once the current ID has been declared: after a withdrawal on a lapsed gate, inside a PCP backoff, or while the source is disabled. It is kept through a disable, and the moved ID stays until reset. A conflict on an ID that has never been declared moves nothing.

## Change

- `KL_acmp_talker`: a conflict on a declaring source withdraws, invalidates the DA and re-allocates at once (no draw, no backoff), and books the move. The grant runs the search (new walker state `S_EV_SID`), installs the new ID and declares it in the same walk if the gate is true. Per source, the move state is a booked bit, a declared bit and a 16-bit replacement unique ID, plus one 16-bit cursor, all in flops. `PROBE_TX`, GET_TX_STATE and `DECLARE_TALKER` read the current ID.
- `protocol_processor_top`: the one new output, `src_stream_id_o`, wired from the talker. No parameter or register map changes.
- Documents: F05.12 and the move rule with its proof (05), the `T-SRP-LEAVEALL2` row (08: same Stream ID only, IEEE 802.1Q-2018 35.2.2.8 normative, Table 5.3 informative), REQ-ACMP-010 in the compliance review, the F02.10 status dictionary and the `srp`/`maap`/`avtp` faces (02), the Talker FSM's per-open latch (10), the output stream_id owner note (06), the integrator guide, the integration diagram, and a 09 evidence map.

## Tests

`tb/acmp_talker` (1,463 checks):

- E: src3's conflict withdraws with no draw and no arm, and re-allocates in the same millisecond. A probe before the grant answers `TALKER_DEST_MAC_FAILED`. The grant declares the new DA under `0xAB00000000000008`. After that, GET_TX_STATE, PROBE_TX and `src_stream_id_o` carry the new ID. F then shows the PCP path keeping that ID and the two-LeaveAll arm.
- S1: the whole path, timed. A 1,700 ms allocator walk, then the declaration at the grant: conflict to new declaration in 1,700 ms, under 2 s.
- S2 to S5 cover distinctness: a slot provisioned with the first candidate is skipped; another source's configured ID stays excluded after that source moved off it; an equal unique ID under another MAC is not a collision; and one full lap of the cursor (65,528 moves) never repeats a unique ID and skips every configured ID and another source's moved ID after the wrap.
- S6: the move is booked after a listener withdrawal and after a freshness lapse, and an ID not declared since its move is not moved again.
- R6, R12 and R16 follow the new conflict path. R6 also shows that the PCP backoff cannot be shortened when a conflict hits it.

`tb/pp_top` MP8, through the in-scope MAAP engine (IEEE 1722-2016 Annex B), the SRP engine and the MAC stream:

- MP8a: while the fresh walk probes, `PROBE_TX` answers `TALKER_DEST_MAC_FAILED` byte-exact.
- MP8: the declaration rises 1,737 ms after the conflicting ANNOUNCE (the walk plus one `T-ACMP-DA-RETRY` round). `src_stream_id_o` names `{OWN_MAC, 8}`. A Talker Advertise for it on the new base appears on the wire. `PROBE_TX` and GET_TX_STATE answer it byte-exact.

Planted mutants, group `STREAM_ID` in `tb/pp_top/acmp_mutants.py`, 20 of 20 killed by named checks. Failing checks in brackets; "MP8" counts are on the MP section alone:

- The old wait kept, `conflict_keeps_old_wait`: `E1 no backoff`, `S1 conflict to new declaration under 2 s`, `MP8: conflict to new declaration under 2 s` (108; MP8 5).
- The old ID reused without the gap, `conflict_reuses_old_id`: `S1 the declaration carries a new Stream ID`, `MP8: the Talker Advertise carries the new Stream ID` (28; MP8 4).
- The output not following the change, `output_ignores_move`: `S1 src_stream_id_o follows the move`, `MP8: src_stream_id_o names the new Stream ID` (11; MP8 1).
- A colliding new ID, `move_takes_colliding_id`: `S2 a provisioned collision with the first candidate is skipped` (4).
- Each search term dropped: configured IDs (2), moved IDs (2), upper 48 bits (1). A stuck cursor (2). A move lost on disable (1).
- The booking rule: booked only while declaring (6); the declared mark not set by the event path (8) or the command path (22); the mark kept after a move (4).
- Each answer and the declaration reading the configured ID: `PROBE_TX` (4), GET_TX_STATE (2), `DECLARE_TALKER` (12).
- The same-Stream-ID path: the PCP change re-declaring without the gap, `pcp_skips_the_gap` (22).

## Validation at processor main ed211803 and this head

- Every processor suite passes: 1,030,399 checks at main, 1,030,494 here, 0 failing. Only two suite lines move: `acmp_talker` 1,376 → 1,463 and `pp_top` 10,741 → 10,749.
- The requirement-tag execution check passes at both ends (231 → 237 tags; the six new ones in section S, the rest line offsets).
- Lint, `make check`, the portability elaboration (`syn/yosys/run.sh`, 42 tops) and the elaboration guards (93 of 93) pass. `make check` differs from main only by the new header file in its ID scan.
- Every campaign that builds a changed file passes here:
  - ACMP: 85 of 85 (65 existing arms and the 20 above). At main, 65 of 65. The 65 shared arms keep their verdicts and their named checks; three of them fail a different set of collateral checks, in the rewritten section E or the new MP8.
  - Talker retry: 62 killed, 7 equivalence and 1 performance control, assertion coverage 59 of 59, at both ends. Its README table is re-measured.
  - MAAP: 29 of 29. The pp_top arms fail 4 and 11 of 42 (README updated).
  - AECP deadline and hazard-class: 67. Dispatch: 74. Counters: 18. Milan-info face: 23. Name write: killed.
  - Notifications: 137. D3: 110.
  - Elaboration-guard mutants: 160. Name state: 16.

## Parent consumer gate

A scratch clone of milan-fpga dev e76a755a with this head as the protocol-processor gitlink and the integrator wiring applied, never pushed. At dev's own pin (this PR's base) and with this head:

- `pp_shadow`, `milan_dp` (every leg), `maap`, `capture_coherence` and `milan_dp_render` pass at both, 38,089 checks and 0 failures at both. `milan_dp`'s sorted check lines are identical; `capture_coherence` differs only in a planted build break's line number.
- The ROM-digest record check records the same ucode and latency-ROM digests for this head as the ledger holds for ed211803, and the out-of-context run validates them.
- The parent's static gates, behave scenarios, the elaboration of `milan_datapath`, `KL_pp_shadow` and `KL_gptp_shadow`, and the vendor parser gate pass at both.
- Area (`syn/yosys/ooc.sh KL_pp_shadow`, module defaults): LUT 58,185 → 59,535 (+1,350, +2.3 %), FF 26,948 → 27,133 (+185), CARRY4 +13, LUTRAM, BRAM and DSP unchanged. The FF delta is exactly the new state.

## Parent integration

A source's Stream ID is no longer fixed, so an integrator must stamp `src_stream_id_o` on the source's stream frames and answer a STREAM_OUTPUT's GET_STREAM_INFO stream_id (selector 2) with it, never with `cfg_stream_id_i`. Otherwise a listener bound through `PROBE_TX` registers for an ID no frame carries. The milan-fpga wiring for this is handed over for the pin adoption PR: the AAF framer gains a per-talker stream_id input (zero default, so its own benches are untouched), the CRF Media Clock Output's stamp and GET_STREAM_INFO selector 2 read `src_stream_id_o`, and `KL_pp_shadow` passes the port out. No parent suite drives a MAAP conflict on a declaring source, so the parent-side agreement after a conflict rests on that wiring and on MP8 here.

## Notes for review

- The PCP-change path is unchanged. The PCP is in PriorityAndRank (35.2.2.8.5) and the path keeps the Stream ID, so its gap is the normative one.
- Between DEFEND and the grant, an allocator that refuses while it probes leaves up to one `T-ACMP-DA-RETRY` round (100 ms) in which MAAP already holds the address but the source has none yet. `PROBE_TX` answers `TALKER_DEST_MAC_FAILED` until the grant, as the decision states it. The bound is the walk (at most three probe intervals of 600 ms, IEEE 1722-2016 Table B.8) plus that round.
- At the grant the gate predicate is unchanged: a fresh probe or a registered Listener. The SRP engine restarts the Listener registrar on every DA-gate open, so a registration of the withdrawn ID never counts for the new one.
- The booking rule reaches past a conflict on a declaring source on purpose. A source that declared, withdrew on a lapsed gate and then took a conflict used to re-declare its old ID with the new address at the next probe, with no gap. Now every conflict books the move once the current ID has been declared; a never-declared ID is not moved.
- The moved ID lasts until reset, through a disable, so a declared ID never comes back with another address.
- Ports, parameters and register maps: only `src_stream_id_o` is added.
