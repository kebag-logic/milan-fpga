Draft written 2026-10-12 ~21:58Z, before reading any prior review finding text.

Independent findings at 1add0cfb:
- RES-1 RESIDUE Docs: tb/verilator/milan_dp/README.md:4-21 - suite README does not say `run` now ends with `$(MAKE) counters` (four extra temporary elaborations; Makefile:636). Fix: one paragraph naming the target, its four legs, TMPDIR use, linking docs/testing/726_STREAM_COUNTERS.md.
- RES-2 RESIDUE Docs (PR body): Status/limitations say hosted shard 4/5 outstanding/unverified; update with the run result once published (pending hosted).
- S-1 SUGGESTION Tests: shipped plant set has RX interval-law plant only on CRF; add AAF interval-rate FRAMES_RX and per-engine guard restorations (own probes show standing checks catch them).
- S-2 SUGGESTION RTL/Robustness: KL_crf_rx.sv:644-689 bind-rise wipe drops a same-cycle accepted PDU (FRAMES_RX 0), unlike AAF ctx and talker diag which keep this cycle's event; stated, rare; optional alignment.
- S-3 SUGGESTION Tests: refresh bound uses service measured in the same run; a uniform service regression inflates its own bound; publish/cap absolute service.

Lens ledger (tentative, pending hosted shard 4/5):
Conformance CLEAN, RTL CLEAN, Robustness CLEAN, Tests CLEAN, Docs CLEAN (RESIDUE does not unclean).
