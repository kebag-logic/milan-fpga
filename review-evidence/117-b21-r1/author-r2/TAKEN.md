[A625] TAKEN

Bench lane B21, #117 acceptance box 4, the audio continuity row, under the [B21 assignment](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-6208207821).

Branch: `117-b21-bench` from dev `4a9b5a2a74fe793a637745fd3ccf51ad2eaf93b4` (findings docs only; local, not pushed). Image: dev `9ef71772` as installed on 2026-10-15; not flashed, not power-cycled, not reset.

Authoritative references: #117 acceptance box 4 and the B21 assignment; lane B5's page `docs/findings/117_AUDIO_CONTINUITY.md` and its analysis tools (`b5_attrib.py`, `b5_round3.py`); the first-light method and pattern (`docs/findings/451_TDM8_FIRST_LIGHT.md`); the #617 torn-frame definition (`docs/findings/617_DIN_FRAME_COHERENCE_BENCH.md`); `docs/design/TIME_SYNC.md` (talker capture handoff); `docs/reference/REGISTER_MAP.md` (`SLIP_LB`, `SLIP_TDM`, `RENDER_STAT`).

Interpreted scope:
1. Identity gate as lanes B18 and B19 ran it; STOP if any read differs.
2. Capture-path self-test with no DUT or peer in the signal path: the same reader and per-read timing record as lane B5, for 10 minutes. A loopback inside the external capture only if it can be set and restored purely in software; otherwise the deficit-only self-test. If a host stall source is found, its evidence is recorded and the lane STOPs before any host configuration change.
3. Direction A (DUT talker to the peer's listener, the peer's output to the external capture), the peer following the DUT's CRF as found: at least 10 minutes, with both taps decoded packet by packet (sequence, timestamps, pattern payload), the DUT's slip, talker and render CSRs polled read-only, and the peer's counters read over ATDECC. Each capture loss is placed against the taps and the CSRs.
4. Direction B (the peer's talker to the DUT's listener, the DUT's TDM output to the SoC board's capture), graded in the DUT's clock domain, with the same wire and CSR record, if a known signal reaches the peer's talker over the existing signal path; otherwise recorded with the reason.
5. Restore the state as found, with read-back. A dated section in `docs/findings/117_AUDIO_CONTINUITY.md`; no other doc edit.

Validation plan: per-run grades from the capture, both taps and the CSR polls; census and counters before and after; the nine assigned gates at the committed head.

Blockers: none known; identity gate pending.
