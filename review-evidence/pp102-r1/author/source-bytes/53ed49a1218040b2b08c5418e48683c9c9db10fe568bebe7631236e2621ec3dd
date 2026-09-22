<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# acmp_nvm — KL_acmp_nvm_shadow persistence suite

Proves the ACMP binding NVM shadow (`hdl/acmp/KL_acmp_nvm_shadow.sv`,
[05 §5](../../docs/architecture/05_acmp_engine.md) ≈20 B/sink shadow +
[07 §5](../../docs/architecture/07_memory_maps.md) F07.8/F07.9 +
[02 §8](../../docs/architecture/02_interfaces.md) F02.8): `make` = build + run,
exit 0 = PASS, 86 checks. `-GDEB_TICKS_P=50` pins the debounce window the C++
timing mirrors (tick_i is held high, so window = 50 cycles).

The wrap compiles the shadow together with the REAL `KL_pp_nvm_port` (class-F
manager face) and the REAL `KL_pp_acmp_listener` (capture from its record write
port, boot replay into its `pre_*` preload face) — face compatibility is
proven by elaboration, not transcription. The harness plays the physical NVM
behind the port's device face (region store, grant/completion delays,
per-byte stalls, targeted error injection) and independently re-implements
the record contract: crc16 CCITT-FALSE, big-endian 16-bit header fields, and
the 20-byte BINDING payload `{flags[valid,started,sw], rsv, talker_uid,
talker_eid, ctlr_eid}` transcribed from the docs, never from the RTL.
Injected F07.6 record images (volatile fields loaded with junk) stand in for
executor write-backs: settle, unbind, started-change, and volatile-only
churn.

Covered: write-through on CHANGE only (volatile-field write-backs — probe
bookkeeping, GET_RX-style — cost zero NVM traffic); T-NVM-DEBOUNCE
coalescing (three changes in one window → one ERASE+WRITE burst of two
records, byte-exact against the model, then quiescence); unbind rewrites the
record with a valid=0 payload; bounded commit retry (recovered error never
alarms) then the sticky side-port alarm with the engine still serviceable;
`restore_blank_o` separating a walk that validated records from one that
read blank or unframed media (`restore_done_o` is set on BOTH, which is
why the pin exists) and following the image rather than the history when
a tear discards records already taken;
boot replay driving `pre_*` for exactly the valid sinks in ascending order —
fields checked at the accept AND against the PRB_W_AVAIL record the listener
then writes (started/sw/eids exact, discovery armed per A4, replay
write-backs compare-equal so nothing re-dirties); per-record vendor defaults
that never abort (empty region, bad crc, wrong layout_version, wrong
payload_length); a TORN mid-record read-back (device error after 5 payload
bytes) aborting the WHOLE restore — `restore_fail_o`, not one preload
driven, the image discarded, the walk stopped, live captures still commit
after; change-during-restore ordering both ways (capture before AND after
its sink's record was walked: the capture wins, its sink is never preloaded,
the live value is flushed back); change-during-flush (the taint path: a
capture landing mid-serialization keeps dirty and the burst re-serializes —
NVM converges to the newest value); and group X, the contract
`protocol_processor_top` exports as `nvm_unflushed_o` (issue #90) — the bit
rises on the ACCEPTED change and on that sink only, holds through the
debounce and the burst, falls on the commit's manager-face `done` (graded on
the cycle, which is why the wrap publishes `dbg_port_done_o`: the device
face's own done is two cycles earlier), and on retry exhaustion falls on the
SAME cycle `alarm_o` rises, never silently.

Known limits (honest): the BINDING record id allocation (`REC_ID_BASE_P` =
0x20) and the exact payload byte layout are design decisions of the shadow's
banner — 07 §5.2 names the BINDING[i] record but pins neither; the suite's
model transcribes the banner contract. Captures arriving between reset and
`restore_go_i` (other than the all-zero init sweeps) are a boot-sequencing
violation (07 §5.3 restores before entity_enable) and are not defended
beyond the restore span. crc polynomial (CCITT-FALSE) matches the
`tb/nvm_port` manager BFM so both suites pin one on-media format.

Mutation-proven 2026-08-11 (backup → sed → run → restore → green):
- **M1** debounce window collapsed to one tick (`deb_cnt_r <= 32'd1`):
  fails 2 of 73 (B4 one-burst coalescing, B5 op-pair shape).
- **M2** torn read-back no longer sets the abort flag (`fail_r <= 1'b0`):
  fails 1 of 73 (G2 restore_fail).
- **M3** serializer streams ctlr EID in the talker EID byte lanes:
  fails 8 of 73 (every byte-exact store check, B6/B7/E2/E7/G7/H9/H10/I2).
- **M4** change detection dropped (`c1_wr_w = c1_v_r`): fails 4 of 73
  (C2 volatile churn, D3 op count, F16/F17 replay must not re-dirty).
- **M5** atomic reject keeps the restored valid bits: fails 1 of 73 (G4).

Mutation-proven 2026-08-13 for the blank arm:
- **M6** `restore_blank_o` hard-wired to `1'b0`: fails 2 of 76 (A2b empty
  NVM, G4b atomic reject), and 1 more in the consumer suite
  (milan-fpga `tb/verilator/pp_shadow`, `PP_STAT[7]`).

Mutation-proven 2026-09-20 for the unflushed export:
- **M7** `dbg_dirty_o` hard-wired to `'0` — the pin issue #90 exports:
  fails 12 of 86, X1, X1b, X2, X3, X3b, X4 and X5b by name (B2 and the
  four byte-exact store checks go with them, because the suite waits on the
  same pin to know a burst drained).
