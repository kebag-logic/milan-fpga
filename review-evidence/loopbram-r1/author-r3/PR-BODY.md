Target: `pf-loopbram-1` into `dev-soft-core`. Closes #979.

Adds optional input-mapped loopback from received audio to transmitted audio. At 8x8,
63 independent mono destinations share the 64-key space with an independent physical
destination; port 0 has physical plus eight loopback destinations and port 7 has seven.
The 1x1 shape has eight physical and eight loopback destinations. The option defaults off.

Received samples are copied from the presentation queue into a separate synchronous
block RAM, adding one media frame. Eight sample pages retain a claimed frame throughout
the capture walk, with four availability records and the full saved page address.
Missing or invalidated data produces silence. Enabled leads above two refuse elaboration.
Timestamp matching includes clock quantisation, marker latency and a bounded rate offset.
Optional capture phases, held samples and writes exist only in the enabled structure.

The generated parent integration runs the production command core against the real map
store and writers. Both sizes pass ADD, REMOVE, replacement, rejected/no-op edits, both
GET pages, format clipping and an edit during copying. The 8x8 case grades all 63 mapped
destinations and eight output streams together. Silence and the first eligible frame are
checked. Four planted connection, retention and address defects fail sample assertions.
This covers command handling and parent transactions, without processor or mailbox execution.

Existing mutation anchors are repaired without removing arms. All seven loopback plants,
both wire sizes, the complete datapath and affected render/capture regressions pass.
The 114-entry builder union and 63-top portability bank pass; one existing calibration-report
row remains unrun because its external report is absent. Five defensive guards remain
explicitly untested in isolation: bind-only flush, one-shot claim, expiry, backlog and age.

Disabled builder artifacts, descriptors, firmware ROM and memory initialization bytes
remain identical to the base. The disabled capture leaf has equal FF and LUT counts.
The queue leaf has equal FF count and two fewer LUTs. Disabled 8x8 grows by 1041 LUTs, so the no-growth criterion remains open. Exact equality
also remains unmet; the full-image comparison is included below.

| Shape | LUT base / head (delta) | FF base / head (delta) | Block-memory tiles base / head (delta) | F7 / F8 mux delta |
|---|---:|---:|---:|---:|
| 1x1/1if | 33792 / 33692 (-100) | 42649 / 42642 (-7) | 80 / 80 (+0) | +62 / +3 |
| 8x8/1if | 45199 / 46240 (+1041) | 53086 / 53051 (-35) | 99 / 99 (+0) | -14 / +3 |

Both enabled routing sweeps selected results above the unchanged +0.030 ns setup and
0 ns hold floors at every required corner, with no failing endpoints or routing errors.
1x1: 33038 LUTs, 42642 FFs, 83 block-memory tiles, minimum setup/hold +0.228/+0.011 ns; 8x8: 48114 LUTs, 54677 FFs, 111 block-memory tiles, minimum setup/hold +0.295/+0.036 ns.

Enabled control-memory allocation is 47.0 tiles at 1x1 and 70.5 at 8x8. The 8x8 result
remains S14 debt, 11.5 tiles above its unchanged ledger and 14.5 above the default budget.
The ordinary product allocator still refuses that image; measurements use disposable
exports. Split builds now apply layout 3's NAME capacity instead of the absent all-fabric
backend's 128-record bound. Owner memory ledgers and service limits remain unchanged.
