<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# ucpu — KL_aecp_ucpu skeleton suite

Proves the µCPU skeleton (`hdl/aecp/KL_aecp_ucpu.sv`) actually executes the
[06 §8](../../docs/architecture/06_aecp_engine.md) µISA before anyone quotes its
area: `make` = build + run, exit 0 = PASS, 342 checks.

The C++ harness is an independent model, never DUT logic: it implements the
state port (2-cycle read latency, locate mapping, forced miss), the gather port
(2-cycle latency, selector-keyed data), a reluctant TX (3 stall cycles before
`tx_ready`), and the lock context — then checks the exact response-buffer bytes,
length, status and send count each µprogram must produce.

The response-buffer face is **flow controlled** and the harness holds it off by
default (`rb_stall` = 2): the buffer lives in the integrator's main memory
(`KL_aecp_resp_buf`), where closing a lane costs a memory round trip, so every
check below already runs against a buffer that pushes back.

Covered per program (µcode from `hdl/aecp/ucode/gen_ucode.py`, shared with
synthesis): the GET_SAMPLING_RATE exemplar success + locate-miss fail path;
RAW interlock and branch flush (poison ops must never reach the buffer); masked
merge; 2-beat qword fields; the ITER_OPEN/APPEND/ITER_NEXT loop shape of
GET_DYNAMIC_INFO; CHECK_ARG → BAD_ARGUMENTS; CHECK_LOCK → LOCKED vs SUCCESS;
GATHER_EXT and the 4-beat READ_COUNTERS burst; re-dispatch readiness.

Covered by P8b through P8i: fixed-size GET_NAME and SET_NAME response bodies,
semantic name address lookup, ENTITY group-name index 1, a missing descriptor,
an invalid selector, changed and idempotent writes, GET after SET, and a locked
SET response carrying the old current name with no write or effects.

Covered additionally: the SET_SAMPLING_RATE exemplar with its full effect
chain (state write-back strobes, COMMIT, NVM_MARK, NOTIFY_ENQ — and their
suppression under a foreign lock), the name region select, COPY_BUFFER lanes,
MAP_VALIDATE both ways, the 524-byte cap with §7.4.76.1 skip-on-overflow (64
of 70 elements fit, the rest skip, iteration continues), Table 7-141 status
codes on the wire header, write-strobe formats B/W/Q, truncating moves, 64-bit
compares, the unknown-opcode NOT_IMPLEMENTED path, the ACQUIRE_ENTITY Milan Δ7
exemplar, and the §9.3.2.6 FAIL_SAFE arm preserving the best current status.

Covered by P17 — the **MVU GET_MILAN_INFO** body of Milan v1.2 Figure 5.4
(`E_MVUINFO`). The µprogram builds all 20 payload bytes from constants: the
tail of the 48-bit protocol_id, r + command_type, the reserved word §5.4.4.1
requires the sender to zero, then protocol_version, features_flags and
certification_version. Each is checked as a FIELD rather than as a length,
because a wrong protocol_version or an overclaimed Table 5.20 flag is a lie a
controller believes — see [06 §8.1](../../docs/architecture/06_aecp_engine.md)
for why this device reports 1 / 0 / 0.

Covered by P18 — **GET_COUNTERS lays out all of IEEE §7.4.42.2's block**: the
response is 148 bytes (12 header + descriptor_type + descriptor_index +
counters_valid + THIRTY-TWO quadlets), quadlet n comes from gather selector
`{n>>2, n&3}` and from nowhere else, the `counters_valid` word comes from
selector `0x80`, and nothing is written past the block. The selector mapping is
checked rather than the values, because that mapping is the reason the 32-quadlet
block needs no decoder in the datapath.

Covered by P16 — **the µCPU is invariant to how hard the buffer pushes back**.
Ten µprograms are run twice, at zero stall and at a 9-cycle stall per write,
and must produce identical bytes, length, status and send count; the number of
writes the buffer ACCEPTS must be identical too (a stalled write that is
duplicated or lost changes it); a REFUSED write must be re-presented
byte-for-byte identically while it is held; and the zero-stall run must be
held zero cycles, so the invariance is not vacuous.

Mutation-proven 2026-08-14 (P17): `MILAN_PROTOCOL_VERSION` 1 -> 2 in
`gen_ucode.py` fails 1 of 181; `MILAN_FEATURES_FLAGS` 0 -> 0x2 (claiming
TALKER_DYNAMIC_MAPPINGS_WHILE_RUNNING this build cannot serve) fails 1 of 181.
Both mutants are internally consistent frames of the right length, which is
exactly why the fields are checked one by one.

Mutation-proven 2026-08-13: advancing the E-stage beat counter while the buffer
refuses the write (the one thing `rb_ready` must gate) fails **58 of 164** —
the beat counter is what selects the write, so advancing it loses the byte the
buffer just declined.

Mutation-proven 2026-08-11: RAW interlock off fails 11 of 92; branch flush
removed fails 2; the 524 cap widened fails 4; the COMMIT strobe killed fails 1.
(One earlier candidate mutation — advance-gating on a never-stalling op — was
behavior-equivalent and was replaced: an equivalent mutant proves nothing.)
