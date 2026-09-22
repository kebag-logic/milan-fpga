<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# `timer_map` — the F08.4 slot map and the 02 §5 event-router map

`make` → `0` = PASS; tally `1187 checks: 1187 PASS, 0 FAIL`. Two gates run in
order; either failing fails the suite.

## What defect this exists for

`protocol_processor_top` allocated its timer slots as **literals**:

```
TMR_ADP_ADV_BASE_C = 0    TMR_LSTN_BASE_C    = 9     TMR_SRP_TK_BASE_C = 73
TMR_ADP_NOADP_BASE_C = 1  TMR_TKR_BASE_C     = 17    TMR_SRP_LS_BASE_C = 81
                          TMR_SRP_CAD_BASE_C = 66
```

Every group assumed exactly 8 streams. The reference platform's generated
shape header for its 8×8 build asks for **9** (`ADP_TALKER_SRC_C = 9`,
`ADP_LISTENER_SINK_C = 9` — the CRF Media Clock Output is itself a source and
a sink), and at 9 the map aliases:

| collision | what happens | why it is silent |
|---|---|---|
| listener sink 8 → slot 9+8 = 17 = the talker base | the loser's deadline is **lost** | the ACMP listener and talker filter expiries **by owner tag**, and their tags differ — so each simply never sees the other's expiry |
| SRP talker 8 → slot 73+8 = 81 = the SRP listener base | SRP listener 0 acts on SRP talker 8's expiry — a **misdelivered** timer | ADP and SRP filter **by slot**, with no owner discrimination |
| event `TK_ATTR_UNREGISTERED{8}` → source 8+8 = 16 = ADP `EVT_TK_DISCOVERED` | the ACMP listener is handed a DISCOVERED it decodes as an UNREGISTERED | `KL_pp_event_router` carries no owner tag at all; the kind decode is a pure range compare on the source index |

None of the three raises an error or moves a counter. On silicon they read
as an intermittent ACMP timeout, a reservation that leaves at the wrong
moment, and a talker that goes away without saying so.

Both maps are now **derived** in `pp_pkg` (`pp_timer_map`, `pp_evr_map`); the
08 §5 / 02 §5 **order** is still the contract, only the **spacing** follows
the shape.

## Gate 1 — `shape_elab.sh`: the real top, at real shapes

Elaborates the actual `protocol_processor_top` (whole `hdl/` tree, zero
tolerance `-Wall`) at ten shapes: `1×1` (what the board ships), `8×8` (the
F01.5 default), `9×9` (the shape that aliased), `16×16`, and asymmetric
shapes — `1×8`, `8×1`, `9×2`, `3×12` — because a map derived from the wrong
count still looks right whenever SI == SO.

It then asserts the **negative**: `17×17`, `16×17` and `33×8` must be
**refused** at elaboration by the guard in the top, with the owner-overlap
message. The owner-tag allocation is a fixed carve-up of the 8-bit expiry bus
(`pp_pkg PP_OWN_*`), so a shape past it has no correct map — refusing to
build is the only honest answer, and a guard nobody proves fires is not a
guard.

This is a full elaboration of the real top, not a stand-in. It is the only
thing that can prove index widths track the shape; a simulation of `8×8` sees
nothing, because `8×8` is the one shape a literal map is right at.

## Gate 2 — `sim_main.cpp`: the map arithmetic, graded

`timer_map_wrap.sv` elaborates both maps at the ten shapes and publishes
every base as a port. The C++ model **re-derives F08.4 from the document**
(the 08 §5 table and the 02 §5 source catalog) and never reads a base back
from the RTL to build its own expectation. Per shape it grades:

1. every base against the independent running sum;
2. **pairwise disjointness** of all ten slot groups and all eight event
   groups — real interval overlap over every pair, which is the property the
   literal map lost, not a spot check of the two indices we happen to know
   about;
3. the map fits `P-TIMER-SLOTS`, and the derived index width can address it;
4. `8×8` still reproduces the historical literal map **exactly**
   (`0/1/9/17/25/57/61/66/73/81`, 89 slots; event sources
   `0/8/16/17/18/19/27/28`, 29 total) — the shipping shape must not move;
5. the `9×9` regression, with the old literal collisions stated as premises
   and then shown gone;
6. owner-tag disjointness, and *where* the space runs out (16 sources, 31
   sinks) — the boundary gate 1 proves is enforced.

## Honesty notes

- The DUT here is **elaboration arithmetic**, not a datapath: no clock, no
  state. That is the level the defect lived at.
- Gate 2 proves the map is disjoint. Gate 1 proves the real top *accepts*
  the 9×9 shape and *refuses* an over-large one. Neither runs 9-stream
  traffic through the processor — the behavioural suites still exercise the
  8×8 shape only, so a 9-stream *functional* bug outside the maps would not
  be caught here.
- The shape table is fixed, not swept: `SI` and `SO` are elaboration-time
  values, so each shape costs one elaboration of the whole tree.

## Files

| file | what it is |
|---|---|
| `shape_elab.sh` | gate 1: real-top elaboration sweep + the guard's negative test |
| `timer_map_wrap.sv` | gate 2 DUT: both maps at ten shapes, bases on ports |
| `sim_main.cpp` | gate 2 model: F08.4 re-derived from the document |
