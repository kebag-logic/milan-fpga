# avtp_parser — the listener ACCEPT VERDICT, at every shipping shape

Deep self-checking Verilator suite for `hdl/ieee1722/avtp/avtp_stream_parser.sv`
and its pairing with `hdl/ieee1722/avtp/KL_stream_table.sv` — the compare that
decides whether an inbound AVTP frame is *ours*.

[`avtp_stream/`](../avtp_stream) owns the module's first increment (21 checks,
one shape, accept-biased). This suite owns the **verdict** and, above all, its
**reject leg**: every negative here is asserted against the counter/latch
signature the `0x8B4` **APRB** probe group publishes to software
([`REGISTER_MAP.md` §0x8B4](../../../docs/reference/REGISTER_MAP.md)), so a
silicon read of those five words maps back to a named case in `sim_parser.cpp`
/ `sim_tbl.cpp`.

Born 2026-07-26 against the open blocker in
[`KNOWN_ISSUES_AND_LIMITATIONS.md`](../../../docs/limitations/KNOWN_ISSUES_AND_LIMITATIONS.md):
the fabric listener accepts nothing on the flashed 8×8 gateware while ACMP
reports a clean bind and both ends agree on the `stream_id`. Nothing owned the
N=8 compare that issues that verdict.

## Shapes

`make` builds five binaries from two sources and runs them all (a red shape
never hides another; the aggregate exit code stays honest):

| binary | parameters | why |
|---|---|---|
| `obj_n1/Vparser_n1` | `N_STREAMS=1` | the legacy / Arty-small shape |
| `obj_n4/Vparser_n4` | `N_STREAMS=4` | the Arty 4×4 shape |
| `obj_n8/Vparser_n8` | `N_STREAMS=8` | **`cfg_ax8x8`, the shipping shape** |
| `obj_be/Vparser_be` | `N_STREAMS=8, BIG_ENDIAN=1` | the beat-order knob, otherwise uncovered |
| `obj_tbl/Vparser_tbl8` | `parser_tbl_wrap`, `N_LISTENERS_P=8` | table + parser as `milan_datapath` wires them |

The index port width is a function of `N_STREAMS`, so entries 4..7 of the
shipping table are only expressible at N=8 — the width *is* the coverage.

## What each source covers

`sim_parser.cpp` (≈2 600 checks per shape):

* **A** — `stream_id` byte order as lifted off the wire: `SID_HI` is the *first*
  four wire bytes and `SID_LO` the last four (the exact claim `0x8BC`/`0x8C0`
  make), and it is neither the byte-reversed nor the half-transposed value;
  all-ones, `1` and `0` stream_ids.
* **B** — VLAN-tagged vs untagged header offset, with both mis-offset negatives
  (a tagged frame must not be read at offset 14, an untagged one not at 18) plus
  honest rejects for an 802.1ad S-tag (`0x88A8`) and Q-in-Q.
* **C** — the subtype gate swept `0x00`..`0x08`, the control subtypes that share
  the wire (ADP/AECP/ACMP/MAAP — none may parse, so none can overwrite the APRB
  media evidence), `sv=0`, and four non-AVTP EtherTypes.
* **D** — every table entry reachable at this N, index correct, top entry alone,
  and a sid armed nowhere.
* **E** — the **reject leg**, one case per way software and the wire can
  disagree while both believe they agree: byte-reversed arm, transposed
  `SID_LO`/`SID_HI`, one-bit-off (bit 0 and bit 63), correct sid but the entry
  disarmed — each asserted as *PARSED climbs, MATCHED does not, the latch shows
  the wire value* — then a positive control on the same frame, a live disarm,
  and an N-way hole test that a compare collapsed to entry 0 would fail.
* **F** — frame-stream integrity: exactly one verdict per frame at 64…1518
  bytes, the header-length floor (≤56 bytes never parses, 57 does), back-to-back
  frames with **no idle gap**, mid-frame backpressure at three ready patterns,
  and a runt ARP immediately before an AVTP frame.
* **G** — 600 randomised frames per shape diffed against an independent C++
  model of the documented byte layout, with random backpressure, plus the
  free-running `avtp_frames_o`/`matched_frames_o` counters reconciled against it.
* **H** — reset clears the probe counters and the parser resumes.

`sim_tbl.cpp` (69 checks) drives `parser_tbl_wrap.sv`:

* **T1** — the entry-0 ACMP alias: bound is the only gate, armed-entry count
  (what `0x8C4[23:16]` reports) tracked either way.
* **T2** — the **open blocker's shape**: the sid the listener SM binds vs the sid
  the parser lifts, disagreeing only in byte order / half order / one bit, with
  a positive control proving the chain is not merely wedged.
* **T3** — entries 1..7 through the CSR-window port; entries 4..7 reach nowhere
  else in the suite tree.
* **T4** — evict / neighbour-untouched / re-arm / duplicate-sid resolution /
  out-of-range write index, with the armed count tracked at each step.
* **T5** — `bind_rise` pulses exactly once per not-bound→bound edge.
* **T6** — **TRAP-1**, characterised not endorsed: *any* override write to
  entry 0 — an evict included — latches `ovr_armed_r[0]` and detaches the ACMP
  alias permanently; re-binding the listener does not revive it, only an
  explicit override write or a reset does. See the section comment for how
  `milan_datapath`'s window-commit glue can reach that state.

## Notes

* The build prints an `ASCRANGE` warning at `avtp_stream_parser.sv:77` — the
  `match_index_o` port is declared `[$clog2(N_STREAMS)-1:0]`, which degenerates
  to the malformed `[-1:0]` at `N_STREAMS=1` instead of using the module's own
  `IDXW` localparam. Left visible on purpose; harmless today (the index is
  always 0 at N=1) but it is a real wart.
* The harness models the APRB probe words in C++ from the parser's own ports —
  it deliberately does **not** replicate `milan_datapath`'s latch in RTL, so a
  defect there can never be masked by a mirror of itself. The latch and its CSR
  readback are covered in [`milan_dp/`](../milan_dp) and [`csr/`](../csr).

```
cd tb/verilator/avtp_parser && make
```
