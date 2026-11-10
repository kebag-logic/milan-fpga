[A757] STOP

Head: `5fb6904ffe12effc4bde6bf5313faea7a3beebdc` on `665-s7-srp-tx` (local, not pushed), on `dev-soft-core` `1d6bf555`: ten commits, added only. No RTL, firmware, lwSRP, mailbox-contract, ring or shape change; no lwSRP donor patch is needed.

**Why STOP: item 5 cannot be met in the production composition at this base.**
- It needs a split talker that holds a licence. Every split source declares Talker Failed from boot: `sw/firmware/ctrl/plat/ctrl_plat.c:146-161` (`configure_sources`) never sets `allocated`, and `sw/firmware/ctrl/srp/srp_mbx.c:170` admits only an allocated source.
- #665 issuecomment-6505997821, item 3, defers the adapter entry that re-declares a source once MAAP allocates, until S2b's `srp_mbx.c` lands.
- The #608 check therefore runs under a test-only fixture, published in `tb/verilator/milan_dp/srptx.hpp`. It gives source 0 its allocation at SRP creation in the licence scenario alone.
- Under it, the peer's LeaveAll at 16,000 ms arms the Listener's Leave timer, and its withdrawal in LV at 18,000 ms re-arms nothing. The timer expires at 21,000 ms, LICENCE clears 12 us later, and the stream gate closes in that millisecond. An lwSRP mutant that restarts LeaveTime on that withdrawal is refused.
- **Decision needed:** accept item 5 under the fixture, or keep #867 open for the allocation entry. The PR body says "Relates to #867" and "Relates to #665"; it does not close #867.

**Done: items 1 to 4, 6 and 7, and the measurements.** `make srptx` runs the split half of the two-placement simulation, which carries lwSRP's MRPDU through the SRP transmit ring, `KL_mbx_tx`, the crossing and `ctl_tx_mux` to the MAC. The bench sees lwSRP's output and timers at its boundary through link-time wrappers, so the adapter is not edited.
- **Item 1.** Every MRPDU has its 10.8.1/10.8.2 form and EndMarks, at most 1,500 octets, one Message per AttributeType, no value twice, and a LeaveAll on every AttributeType. No finding in 1,449 + 169 + 69 MRPDUs.
- **Item 2.** The port's MAC from the first MRPDU after reset, at 1 ms.
- **Item 3.** Join and LeaveAll spacing at egress hold within IEEE 802.1Q-2018 10.7.4.1, 10.7.4.3 and Table 10-7 (Milan Table 4.3 values). Each bound is widened by min(T_svc 20, the MRP ceiling 18) = 18 ms, the owner's per-family rule.
- **Item 4.** With the MAC held, the SRP ring reached 507 of 512 words, and the adapter refused a 30-word MSRP record, kept it, and sent it first on release. All 169 MRPDUs left in the order accepted, byte for byte.
- **Item 6.** Each LICENCE bit reaches ACTIVE, admitted and the stream gate as itself, for every talker of the shape, and the CRF term reads the top bit. This is `[POL]` in the split leg, and `[LIC]` at every millisecond of the licence scenario.
- **Item 7.** 23 capture plants and 10 code mutants (plus 2 split-leg arms), each refused by its own words. The five the issue names are planted both in a capture and in lwSRP or the adapter.
- **Measurements, wire scenario, 600 s.**
  - Egress after a Join or periodic tick: 1.52 to 26.31 us.
  - JoinTime interval error: -1.01 to +0.02 ms over 104 intervals (the centisecond grid).
  - LeaveAll interval error: mean 0, extremes +/-50 ms (MSRP) and +/-70 ms (MVRP), over 39 and 40 draws. These are the opportunity's wait for the Join timer.
  - Frames per transmit opportunity: 1 (727 MSRP, 722 MVRP).

**Gates, all rc 0, on clean clones:**
- At `5fb6904f`:
  - Every `run:` step of docs, elaborate, rtl-fast and rtl for a ready pull request to `dev-soft-core`: 546 ran, all rc 0, firmware-boundary with the LiteX venv included. 86 cannot run here, each with its reason.
  - The full sweep as four shards: 65 suites, 2,192,910 checks, 0 failures.
  - `make srptx`, `srptx-plants` and `srptx-mutants`; `make twin` and `twin-plants` (the twin's split capture byte-identical to the base's); `make split`, `split-mutants` (26 of 26), `split-cdc` and `split_parallel.py --selftest`.
  - `git diff --check` against the merge base.
- At `bf1bba25`, whose only difference from the head is the firmware README's pin-control count, which neither reads: `test_builder.py --require-rv32` (all pass except 2 arms not run here) and the CPU budget harness at 1x1 and 8x8.
- An earlier cancellation-control failure (the #833 class) was re-run once, and both results are recorded. Its cause was this session's inherited signal state, not the change.

**Found, not fixed (for new issues):**
- The split's AAF frames carry stream_id 0: no firmware writes the publication block's `SRC_SID`. This is latent until a split talker streams.
- The two-placement simulation's own split half sends a frame that follows another about 11 modeled ms late. That is a bench artifact the new check's drain removes; the twin itself is not changed here.
