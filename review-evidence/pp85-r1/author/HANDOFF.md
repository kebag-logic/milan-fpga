# [A524] HANDOFF: processor #85 (GAP-16, ADP MTXW walker)

Status: REVIEW READY at head `a866973`. Every item of the assignment is done; no STOP
condition arose (no cell's behaviour is wrong, no RTL change). One parent gate is red as
the assignment foresaw: gate 16's two T30 INTERNAL LAW checks, which go against
milan-fpga #643 and fail identically with the processor at `main` (section 9).

- Processor repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Branch: `pp85-adp-mtxw`, base processor `main` `5c71928ad2bf1a854a5538d69b77214dfdf1697f`
  (`origin` and HEAD checked at start).
- Head: `a8669732b30436c641d51829950c204defd57a30` (six commits on `5c71928a`).
- Assignment: #85 comment 5974306370. Requirement tickets #39, #40, #41.
- TAKEN: #85 comment 5974309854. REVIEW READY with the head: #85 comment 5975128280.
  Not pushed; no PR created. No RTL change: `hdl/` is
  untouched (`git diff 5c71928a..HEAD --stat -- hdl` is empty).

| Commit | Subject |
|---|---|
| `c291f89` | Cite IEEE 1722.1-2021 §6.2.2.15 for available_index in 04 §5 and the review, where §6.2.2.9 (entity_capabilities) stood |
| `502451d` | Cite every ADP walk cell to its Milan v1.2 clause and the IEEE 1722.1-2021 clause it replaces or follows, derived in 04 F04.7 and F04.8, and count the cells citing both |
| `c0d5860` | Plant one mutant per F04.3 arc in the ADP campaign, each required to fail its arc's own check: 38 of 38 arms killed |
| `f80fa44` | Adjudicate the available_index interop note against IEEE 1722.1-2021 §6.2.2.15 and the B6 to B8 enumerations, and restate the one case still open |
| `1d5b680` | Cite the discovery walk's cells to the same Milan §5.6.4.5 steps as 04 F04.8 |
| `a866973` | Cite IEEE §6.2.2.15 beside §6.2.6.4 on the fresh-index cells as F04.8 does, and correct the README's reading of the B8 rate (6.96 s) and of where the F04.2 table sits |

Files: `tb/adp_engine/sim_main.cpp`, `tb/adp_engine/mutants.py`, eight new
`tb/adp_engine/mutations/arc-*.patch`, `tb/adp_engine/README.md`,
`docs/architecture/04_adp_engine.md`, `docs/architecture/09_verification.md`,
`docs/00_MILAN_COMPLIANCE_REVIEW.md`.

## 1. Starting point and what this lane adds

At `5c71928a`, PR #136 (lane C3) had already landed a P13 MTXW walk in `tb/adp_engine`:
45 F04.2 cells (9 events x 5 columns: NOT STARTED, DOWN, WAITING, DELAY with the draw in
flight, DELAY with the timer armed), 33 F04.3 cells, `CHECK(adv_cells == 45)`,
`CHECK(disc_cells == 33)`, an eight-arc check, and 30 mutation arms under a driver with
`--jobs`. Base suite: 1328 checks PASS (pinned Verilator 5.050).

| #85 item | At base | At head |
|---|---|---|
| 1. walker from an independent table, each cell's next state, transmit and timer action cited to IEEE 1722.1-2021 §6.2.x and Milan v1.2 §5.x as 04 derives them, cell-count check | walker and counts present; one Milan reference per cell, no IEEE clause, no derivation in 04; seven cells cited the table where a clause rules them: §5.6.1 (NOT STARTED x TMR_ADVERTISE, TMR_DELAY, SHUTDOWN), §5.6.3.5.9 (TMR_DELAY x DELAY, draw phase), §5.6.3.1 (another entity's ENTITY_DISCOVER x DOWN and both DELAY phases) | every cell carries `milan` and `ieee` fields, printed in each of its failure messages; 04 F04.7 derives each advertise cell, F04.8 each discovery arc; two new checks count the cells citing both (45 of 45; 33 of 33, where a sink binding has no IEEE counterpart). Cell counts unchanged: 45 and 33 |
| 2. the five undriven cells | walked, both DELAY phases | unchanged, re-graded (section 2) |
| 3. every F04.3 arc in the same walk; mutants for DOWN answering DISCOVER, DELAY ignoring LINK_DOWN, and one per F04.3 arc; in the campaign with `--jobs` | the two named F04.2 arms present; no arm was required to fail an arc check; arcs 1, 3, 6 and 8 had no arm | eight `arc-*` arms, one per arc, each required to fail its own `P13 F04.3 arc ...` check; 38 of 38 arms KILLED |
| 4. available_index interop note | "still open, needs a live controller" | adjudicated against the standard and the B6/B7/B8 enumerations; the rule stands, the limit is restated and narrowed to the one case not on record (section 5) |

Doc fix on the way: 04 §5 and 00 (GAP-16 text, REQ-ADP-011's clause column) cited IEEE
§6.2.2.9 for available_index. In IEEE 1722.1-2021 §6.2.2.9 is entity_capabilities and
available_index is §6.2.2.15 (§6.2.1.16 in the 2013 edition, so no edition makes it
§6.2.2.9). The RTL banner and the README already cited §6.2.2.15.

No cell's behaviour is wrong: every cell matches its clause at head, so there is no STOP.

## 2. F04.2 cell table with clause citations, and each cell's check

Dumped from `tb/adp_engine/sim_main.cpp` at head (the walk's own `ADV` table, compiled
and printed, not retyped). 04 F04.7 derives the same pairs per Milan state; the walk
splits DELAY into its two hardware phases. Next is the `dbg_adv_state` the cell must end
in (DELAY(draw) is the draw in flight); Draws counts T-ADP-DELAY draw requests; Arms the
arms of the shared advertise slot; Cancel whether a cancel must happen, may happen
(harmless: the slot is replaced or unarmed) or must not; Frame the committed frame.

| Event | State | Class | Next | Draws | Arms | Cancel | Frame | Milan v1.2 | IEEE 1722.1-2021 |
|---|---|---|---|---|---|---|---|---|---|
| RCV_ADP_DISCOVER(eid 0) | NOT STARTED(DOWN) | I | DOWN | 0 | 0 | none | none | 5.6.1 not started | 6.2.4.3 before BEGIN |
| RCV_ADP_DISCOVER(eid 0) | DOWN | I | DOWN | 0 | 0 | none | none | Table 5.51 - | 6.2.7.2 DISCOVER, no DOWN state |
| RCV_ADP_DISCOVER(eid 0) | WAITING | N | DELAY | 1 | 1 | must | none | 5.6.3.1; 5.6.3.5.4 | 6.2.7.2 DISCOVER; 6.2.4.3 |
| RCV_ADP_DISCOVER(eid 0) | DELAY(draw in flight) | I | DELAY | 0 | 1 | none | none | Table 5.51 - | 6.2.4.3 ADVERTISE clears needsAdvertise |
| RCV_ADP_DISCOVER(eid 0) | DELAY(timer armed) | I | DELAY | 0 | 0 | none | none | Table 5.51 - | 6.2.4.3 ADVERTISE clears needsAdvertise |
| RCV_ADP_DISCOVER(own eid) | NOT STARTED(DOWN) | I | DOWN | 0 | 0 | none | none | 5.6.1 not started | 6.2.4.3 before BEGIN |
| RCV_ADP_DISCOVER(own eid) | DOWN | I | DOWN | 0 | 0 | none | none | Table 5.51 - | 6.2.7.2 DISCOVER, no DOWN state |
| RCV_ADP_DISCOVER(own eid) | WAITING | N | DELAY | 1 | 1 | must | none | 5.6.3.1; 5.6.3.5.4 | 6.2.7.2 DISCOVER; 6.2.4.3 |
| RCV_ADP_DISCOVER(own eid) | DELAY(draw in flight) | I | DELAY | 0 | 1 | none | none | Table 5.51 - | 6.2.4.3 ADVERTISE clears needsAdvertise |
| RCV_ADP_DISCOVER(own eid) | DELAY(timer armed) | I | DELAY | 0 | 0 | none | none | Table 5.51 - | 6.2.4.3 ADVERTISE clears needsAdvertise |
| ENTITY_DISCOVER(foreign eid) | NOT STARTED(DOWN) | I | DOWN | 0 | 0 | none | none | 5.6.1 not started | 6.2.4.3 before BEGIN |
| ENTITY_DISCOVER(foreign eid) | DOWN | I | DOWN | 0 | 0 | none | none | 5.6.3.1 discard | 6.2.7.2 entity_id neither 0 nor own |
| ENTITY_DISCOVER(foreign eid) | WAITING | I | WAITING | 0 | 0 | none | none | 5.6.3.1 discard | 6.2.7.2 entity_id neither 0 nor own |
| ENTITY_DISCOVER(foreign eid) | DELAY(draw in flight) | I | DELAY | 0 | 1 | none | none | 5.6.3.1 discard | 6.2.7.2 entity_id neither 0 nor own |
| ENTITY_DISCOVER(foreign eid) | DELAY(timer armed) | I | DELAY | 0 | 0 | none | none | 5.6.3.1 discard | 6.2.7.2 entity_id neither 0 nor own |
| TMR_ADVERTISE | NOT STARTED(DOWN) | S | DOWN | 0 | 0 | none | none | 5.6.1 not started, no timer: a stray | 6.2.4.3 before BEGIN |
| TMR_ADVERTISE | DOWN | S | DOWN | 0 | 0 | none | none | Table 5.51 x, stray | 6.2.4.3 timers, no DOWN state |
| TMR_ADVERTISE | WAITING | N | DELAY | 1 | 1 | may | none | 5.6.3.5.5 | 6.2.4.3 reannounce; 6.2.4.2.2 |
| TMR_ADVERTISE | DELAY(draw in flight) | S | DELAY | 0 | 1 | none | none | Table 5.51 x, stray | 6.2.4.3 reannounce timer only in WAITING |
| TMR_ADVERTISE | DELAY(timer armed) | C | - | 0 | 0 | none | none | Table 5.51 x | 6.2.4.3 reannounce timer only in WAITING |
| TMR_DELAY | NOT STARTED(DOWN) | S | DOWN | 0 | 0 | none | none | 5.6.1 not started, no timer: a stray | 6.2.4.3 before BEGIN |
| TMR_DELAY | DOWN | S | DOWN | 0 | 0 | none | none | Table 5.51 x, stray | 6.2.4.3 timers, no DOWN state |
| TMR_DELAY | WAITING | C | - | 0 | 0 | none | none | Table 5.51 x | 6.2.4.3 delay timer only in DELAY |
| TMR_DELAY | DELAY(draw in flight) | S | DELAY | 0 | 1 | none | none | 5.6.3.5.9, not yet started: a stray | 6.2.4.3 delay timer not yet set |
| TMR_DELAY | DELAY(timer armed) | N | WAITING | 0 | 1 | none | ENTITY_AVAILABLE | 5.6.3.5.9; 5.6.2 | 6.2.4.3 ADVERTISE; 6.2.5.3; 6.2.2.15 |
| LINK_UP | NOT STARTED(DOWN) | I | DOWN | 0 | 0 | none | none | 5.6.1 not started | 6.2.4.3 before BEGIN |
| LINK_UP | DOWN | N | DELAY | 1 | 1 | may | none | 5.6.3.5.3 | 6.2.7.2 LINK STATE CHANGE; 6.2.4.3 |
| LINK_UP | WAITING | C | - | 0 | 0 | none | none | Table 5.51 x | 6.2.7.2 needs a link change |
| LINK_UP | DELAY(draw in flight) | C | - | 0 | 0 | none | none | Table 5.51 x | 6.2.7.2 needs a link change |
| LINK_UP | DELAY(timer armed) | C | - | 0 | 0 | none | none | Table 5.51 x | 6.2.7.2 needs a link change |
| LINK_DOWN | NOT STARTED(DOWN) | I | DOWN | 0 | 0 | none | none | 5.6.1 not started | 6.2.4.3 before BEGIN |
| LINK_DOWN | DOWN | C | - | 0 | 0 | none | none | Table 5.51 x | 6.2.7.2 needs a link change |
| LINK_DOWN | WAITING | N | DOWN | 0 | 0 | must | none | 5.6.3.5.6 | 6.2.7.2 LINK STATE CHANGE, no needsAdvertise |
| LINK_DOWN | DELAY(draw in flight) | N | DOWN | 0 | 0 | may | none | 5.6.3.5.10 | 6.2.7.2 LINK STATE CHANGE, no needsAdvertise |
| LINK_DOWN | DELAY(timer armed) | N | DOWN | 0 | 0 | must | none | 5.6.3.5.10 | 6.2.7.2 LINK STATE CHANGE, no needsAdvertise |
| GM_CHANGE | NOT STARTED(DOWN) | I | DOWN | 0 | 0 | none | none | 5.6.1 not started | 6.2.4.3 before BEGIN |
| GM_CHANGE | DOWN | I | DOWN | 0 | 0 | none | none | Table 5.51 - | 6.2.7.2 UPDATE GM, no DOWN state |
| GM_CHANGE | WAITING | N | DELAY | 1 | 1 | may | none | 5.6.3.5.7 | 6.2.7.2 UPDATE GM; 6.2.4.3 |
| GM_CHANGE | DELAY(draw in flight) | I | DELAY | 0 | 1 | none | none | Table 5.51 - | 6.2.4.3; 6.2.2.16 at the send |
| GM_CHANGE | DELAY(timer armed) | I | DELAY | 0 | 0 | none | none | Table 5.51 - | 6.2.4.3; 6.2.2.16 at the send |
| SHUTDOWN | NOT STARTED(DOWN) | C | - | 0 | 0 | none | none | 5.6.1 not started, enable already low | 6.2.4.1.3 doTerminate ends a running machine |
| SHUTDOWN | DOWN | I | DOWN | 0 | 0 | none | none | Table 5.51 - | 6.2.5.3 DEPARTING, no DOWN state |
| SHUTDOWN | WAITING | N | DOWN | 0 | 0 | must | ENTITY_DEPARTING | 5.6.3.5.8 | 6.2.5.3 DEPARTING; 6.2.2.15; 6.2.2.5 |
| SHUTDOWN | DELAY(draw in flight) | N | DOWN | 0 | 0 | may | ENTITY_DEPARTING | 5.6.3.5.11 | 6.2.5.3 DEPARTING; 6.2.2.15; 6.2.2.5 |
| SHUTDOWN | DELAY(timer armed) | N | DOWN | 0 | 0 | must | ENTITY_DEPARTING | 5.6.3.5.11 | 6.2.5.3 DEPARTING; 6.2.2.15; 6.2.2.5 |

Classes: 12 N, 20 I, 6 S, 7 C (the run prints `P13 MTXW: F04.2 45 cells (N 12, I 20, S 6,
C 7)`). The five cells #85 named are DOWN x {RCV_ADP_DISCOVER (both), GM_CHANGE,
SHUTDOWN}, all I with no draw, no arm, no cancel, no frame, and DELAY x LINK_DOWN (N:
DOWN, no frame, a cancel that must happen in the armed phase) and DELAY x SHUTDOWN (N:
DOWN, ENTITY_DEPARTING byte-exact with the pre-reset index, index 0), the last two in
both DELAY phases.

**Each cell's check** (`walk_advertise_cell`, one cell per call, 200 observed clocks):

- reached: `dbg_adv_state` equals the column's state; NOT STARTED with `entity_enable_i`
  low; DOWN with enable high and the link down; DELAY(draw) with the draw request on the
  PRNG port and not yet taken (so the event acts strictly inside the draw).
- C cells: the precondition that rules the event out, checked in the state reached:
  TMR_DELAY x WAITING, the slot holds T-ADP-ADV (armed at +5000 ms); TMR_ADVERTISE x
  DELAY(armed), the slot holds the drawn T-ADP-DELAY (<= 4000 ms); LINK_UP x WAITING
  and DELAY, the link is up; LINK_DOWN x DOWN, the link is down; SHUTDOWN x NOT STARTED,
  the enable is low.
- every other cell, after the event: the state; the draw requests (and a drawn value of
  kind 2, 0..4000 ms where one is drawn); no timer operation on any other slot; the arm
  count of the shared slot, the arm being the last operation with deadline `now` +
  5000 ms into WAITING or `now` + the draw into DELAY; a cancel where the clause says
  Stop, none where the slot is untouched; the committed frames and TX requests (0 or 1),
  byte-exact against the independent 82-byte model; available_index +1, 0 or unchanged;
  no discovery event; and the RX-slot free of each DISCOVER.
- I and S cells are those checks with zero draws, zero arms, no cancel and no frame
  (the draw phase keeps its one in-flight arm).
- two table checks: `P13 F04.2 cells citing Milan v1.2 5.x and IEEE 1722.1-2021 6.2.x:
  45 of 45` and the F04.3 equivalent, 33 of 33.

## 3. F04.3 arcs

The walk's `DISC` table at head (33 cells: 13 N, 15 I, 2 S, 3 C), then the arcs. Each
cell checks the sink's bound and discovered bits, the exact class-C event sequence (sink
and order), the sink's T-ADP-NOADP operations (one arm at +20000 ms, the received
valid_time 10; one cancel; or none; nothing on another slot), that nothing is
transmitted, and the RX-slot free; a C cell checks the binding precondition. Cells
rotate over all eight sinks.

| Event | State | Class | Next | Events | T-ADP-NOADP | Milan v1.2 | IEEE 1722.1-2021 |
|---|---|---|---|---|---|---|---|
| AVAILABLE(match, index > last) | unbound | I | unbound | none | none | 5.6.4.1 bound sinks only | none: Milan per-sink binding |
| AVAILABLE(match, index > last) | TK_NOT_DISCOVERED | N | TK_DISCOVERED | DISCOVERED | arm | 5.6.4.5.1 steps 1-4 | 6.2.6.4 AVAILABLE |
| AVAILABLE(match, index > last) | TK_DISCOVERED | N | TK_DISCOVERED | none | arm | 5.6.4.5.2 steps 1 3 | 6.2.6.4 AVAILABLE; 6.2.2.15 |
| AVAILABLE(match, index <= last) | unbound | I | unbound | none | none | 5.6.4.1 bound sinks only | none: Milan per-sink binding |
| AVAILABLE(match, index <= last) | TK_NOT_DISCOVERED | N | TK_DISCOVERED | DISCOVERED | arm | 5.6.4.5.1 steps 1-4 | 6.2.6.4 AVAILABLE |
| AVAILABLE(match, index <= last) | TK_DISCOVERED | N | TK_DISCOVERED | DEPARTED, DISCOVERED | arm | 5.6.4.5.2 steps 2a 2c 3 | 6.2.2.15 a new cycle |
| AVAILABLE(GM mismatch, index > last) | unbound | I | unbound | none | none | 5.6.4.1 bound sinks only | none: Milan per-sink binding |
| AVAILABLE(GM mismatch, index > last) | TK_NOT_DISCOVERED | I | TK_NOT_DISCOVERED | none | none | 5.6.4.5.1 step 1 | 6.2.2.16; 6.2.2.17 |
| AVAILABLE(GM mismatch, index > last) | TK_DISCOVERED | N | TK_DISCOVERED | none | arm | 5.6.4.5.2 steps 1 3 | 6.2.6.4 AVAILABLE; 6.2.2.15 |
| AVAILABLE(GM mismatch, index <= last) | unbound | I | unbound | none | none | 5.6.4.1 bound sinks only | none: Milan per-sink binding |
| AVAILABLE(GM mismatch, index <= last) | TK_NOT_DISCOVERED | I | TK_NOT_DISCOVERED | none | none | 5.6.4.5.1 step 1 | 6.2.2.16; 6.2.2.17 |
| AVAILABLE(GM mismatch, index <= last) | TK_DISCOVERED | N | TK_NOT_DISCOVERED | DEPARTED | cancel | 5.6.4.5.2 steps 2a 2b | 6.2.2.15; 6.2.2.16; 6.2.2.17 |
| AVAILABLE(domain mismatch, index <= last) | unbound | I | unbound | none | none | 5.6.4.1 bound sinks only | none: Milan per-sink binding |
| AVAILABLE(domain mismatch, index <= last) | TK_NOT_DISCOVERED | I | TK_NOT_DISCOVERED | none | none | 5.6.4.5.1 step 1 | 6.2.2.16; 6.2.2.17 |
| AVAILABLE(domain mismatch, index <= last) | TK_DISCOVERED | N | TK_NOT_DISCOVERED | DEPARTED | cancel | 5.6.4.5.2 steps 2a 2b | 6.2.2.15; 6.2.2.16; 6.2.2.17 |
| AVAILABLE(interface_index differs) | unbound | I | unbound | none | none | 5.6.4.1 bound sinks only | none: Milan per-sink binding |
| AVAILABLE(interface_index differs) | TK_NOT_DISCOVERED | N | TK_DISCOVERED | DISCOVERED | arm | 5.6.4.5.1 steps 1-4 | 6.2.6.4 AVAILABLE |
| AVAILABLE(interface_index differs) | TK_DISCOVERED | I | TK_DISCOVERED | none | none | 5.6.4.5.2 step 1 | 6.2.2.20 |
| DEPARTING(interface_index matches) | unbound | I | unbound | none | none | 5.6.4.1 bound sinks only | none: Milan per-sink binding |
| DEPARTING(interface_index matches) | TK_NOT_DISCOVERED | I | TK_NOT_DISCOVERED | none | none | Table 5.54 - | 6.2.6.4 DEPARTING |
| DEPARTING(interface_index matches) | TK_DISCOVERED | N | TK_NOT_DISCOVERED | DEPARTED | cancel | 5.6.4.5.3 | 6.2.6.4 DEPARTING |
| DEPARTING(interface_index differs) | unbound | I | unbound | none | none | 5.6.4.1 bound sinks only | none: Milan per-sink binding |
| DEPARTING(interface_index differs) | TK_NOT_DISCOVERED | I | TK_NOT_DISCOVERED | none | none | Table 5.54 - | 6.2.6.4 DEPARTING |
| DEPARTING(interface_index differs) | TK_DISCOVERED | I | TK_DISCOVERED | none | none | 5.6.4.5.3 step 1 | 6.2.2.20 |
| TMR_NO_ADP | unbound | S | unbound | none | none | 5.6.4.1 stray | none: Milan per-sink binding |
| TMR_NO_ADP | TK_NOT_DISCOVERED | S | TK_NOT_DISCOVERED | none | none | Table 5.54 x, stray | 6.2.6.4 TIMEOUT |
| TMR_NO_ADP | TK_DISCOVERED | N | TK_NOT_DISCOVERED | DEPARTED | none | 5.6.4.5.4 | 6.2.6.4 TIMEOUT |
| UNBIND | unbound | C | - | none | none | 5.6.4.1 x: the binding is already so | none: Milan per-sink binding |
| UNBIND | TK_NOT_DISCOVERED | N | unbound | none | none | 5.6.4.1; 04 6.2 disarm | none: Milan per-sink binding |
| UNBIND | TK_DISCOVERED | N | unbound | none | cancel | 5.6.4.1; 04 6.2 disarm, timer stopped | none: Milan per-sink binding |
| BIND | unbound | N | TK_NOT_DISCOVERED | none | none | 5.6.4.4 sink connected; F04.3 entry | none: Milan per-sink binding |
| BIND | TK_NOT_DISCOVERED | C | - | none | none | 5.6.4.1 x: the binding is already so | none: Milan per-sink binding |
| BIND | TK_DISCOVERED | C | - | none | none | 5.6.4.1 x: the binding is already so | none: Milan per-sink binding |

| # | Arc (F04.3) | Walk cell | Milan v1.2 | IEEE 1722.1-2021 | Arc mutant | Its failures |
|---|---|---|---|---|---|---|
| 1 | [*] to TK_NOT_DISCOVERED (sink bound) | BIND x unbound | §5.6.4.4 (sink connected); F04.3 entry | none: Milan per-sink binding | `arc-bind-keeps-discovered` | 46 |
| 2 | TK_NOT_DISCOVERED to TK_DISCOVERED (grandmaster and domain match) | AVAILABLE(match, index > last) x TK_NOT_DISCOVERED | §5.6.4.5.1 steps 1-4 | §6.2.6.4 AVAILABLE | `arc-discover-no-noadp-arm` | 13 |
| 3 | TK_NOT_DISCOVERED to itself (grandmaster or domain mismatch) | AVAILABLE(GM mismatch, index <= last) x TK_NOT_DISCOVERED | §5.6.4.5.1 step 1 | §6.2.2.16; §6.2.2.17 | `arc-not-discovered-no-guard` | 14 |
| 4 | TK_DISCOVERED to itself (index > last) | AVAILABLE(match, index > last) x TK_DISCOVERED | §5.6.4.5.2 steps 1, 3 | §6.2.6.4 AVAILABLE | `arc-fresh-no-rearm` | 5 |
| 5 | TK_DISCOVERED to itself (index <= last, match: restart pair) | AVAILABLE(match, index <= last) x TK_DISCOVERED | §5.6.4.5.2 steps 2a, 2c, 3 | §6.2.2.15 | `arc-restart-detector-off-by-one` | 10 |
| 6 | TK_DISCOVERED to TK_NOT_DISCOVERED (index <= last, mismatch) | AVAILABLE(GM mismatch, index <= last) x TK_DISCOVERED | §5.6.4.5.2 steps 2a, 2b | §6.2.2.15; §6.2.2.16; §6.2.2.17 | `arc-restart-skips-guard` | 12 |
| 7 | TK_DISCOVERED to TK_NOT_DISCOVERED (DEPARTING, interface matches) | DEPARTING(interface_index matches) x TK_DISCOVERED | §5.6.4.5.3 | §6.2.6.4 DEPARTING | `arc-departing-silent` | 4 |
| 8 | TK_DISCOVERED to TK_NOT_DISCOVERED (T-ADP-NOADP expiry) | TMR_NO_ADP x TK_DISCOVERED | §5.6.4.5.4 | §6.2.6.4 TIMEOUT | `arc-noadp-expiry-silent` | 4 |

The check that grades an arc is `P13 F04.3 arc <name>: walked and graded`: it fails when
any check of the arc's cell failed. Each arc arm is required to fail that check (the
driver's named-check prefix), and each does (section 4). The GM and domain guard is
planted at both of its sites (arc 3: TK_NOT_DISCOVERED; arc 6: the restart pair), the
restart detector at its boundary (arc 5: an index equal to the last one taken as fresh,
`>=` for `>`; it also turns arc 6 red, whose cell is walked at the same boundary).

## 4. Mutants and kills

`python3 tb/adp_engine/mutants.py --output <scratch> --jobs 4` at head `a866973`
(`make mutants` runs the same with the default `--jobs 4`): rc 0, `40 checks: 40 PASS,
0 FAIL`, 154 s. Both controls PASS. Two earlier runs of the same arms, on the tree that
became `c0d5860` (169 s) and at `1d5b680` (150 s), the commits after which changed
citation strings and the README only: rc 0, 40 of 40 each, and their verdict lines,
failure counts and named counts are identical to the head run's, line for line.

| Arm | Suite, target | Failures | Named | Verdict |
|---|---|---:|---:|---|
| `cfg-read-live` | adp_engine `run` | 1 | 1 | KILLED |
| `cfg-dependent-field` | adp_engine `run` | 14 | 3 | KILLED |
| `cfg-dependent-field-top` | pp_top `adp-config` | 9 | 1 | KILLED |
| `cfg-frozen-at-top` | pp_top `adp-config` | 4 | 2 | KILLED |
| `cfg-overlay-only` | pp_top `adp-config` | 6 | 2 | KILLED |
| `cfg-nonzero-for-valid` | pp_top `adp-config` | 3 | 2 | KILLED |
| `cfg-valid-not-sticky` | pp_top `adp-config` | 7 | 2 | KILLED |
| `cfg-valid-any-selector` | pp_top `adp-config` | 1 | 1 | KILLED |
| `cfg-valid-ucpu-bus` | pp_top `adp-config` | 3 | 2 | KILLED |
| `cfg-valid-hard-reset` | pp_top `adp-config` | 2 | 2 | KILLED |
| `cfg-valid-no-reset` | pp_top `adp-config` | 9 | 2 | KILLED |
| `gate-enable-dropped` | adp_engine `run` | 30 | 4 | KILLED |
| `gate-enable-dropped-top` | pp_top `adp-config` | 7 | 2 | KILLED |
| `walk-down-answers-discover` | adp_engine `run` | 16 | 4 | KILLED |
| `walk-delay-ignores-link-down` | adp_engine `run` | 4 | 4 | KILLED |
| `walk-down-answers-gm-change` | adp_engine `run` | 8 | 4 | KILLED |
| `walk-down-shutdown-departs` | adp_engine `run` | 1 | 1 | KILLED |
| `walk-delay-answers-discover` | adp_engine `run` | 9 | 4 | KILLED |
| `walk-delay-shutdown-silent` | adp_engine `run` | 4 | 4 | KILLED |
| `walk-stale-draw-arms` | adp_engine `run` | 4 | 2 | KILLED |
| `walk-departing-keeps-index` | adp_engine `run` | 6 | 1 | KILLED |
| `walk-foreign-discover-answered` | adp_engine `run` | 8 | 4 | KILLED |
| `walk-link-down-keeps-timer` | adp_engine `run` | 3 | 1 | KILLED |
| `disc-fresh-checks-gm` | adp_engine `run` | 3 | 3 | KILLED |
| `disc-not-discovered-checks-index` | adp_engine `run` | 14 | 3 | KILLED |
| `disc-not-discovered-checks-interface` | adp_engine `run` | 3 | 3 | KILLED |
| `disc-restart-not-rediscovered` | adp_engine `run` | 4 | 1 | KILLED |
| `disc-departing-ignores-interface` | adp_engine `run` | 3 | 3 | KILLED |
| `disc-stray-noadp-departs` | adp_engine `run` | 2 | 1 | KILLED |
| `disc-unbind-keeps-timer` | adp_engine `run` | 2 | 1 | KILLED |
| `arc-bind-keeps-discovered` | adp_engine `run` | 46 | 1 | KILLED |
| `arc-discover-no-noadp-arm` | adp_engine `run` | 13 | 1 | KILLED |
| `arc-not-discovered-no-guard` | adp_engine `run` | 14 | 1 | KILLED |
| `arc-fresh-no-rearm` | adp_engine `run` | 5 | 1 | KILLED |
| `arc-restart-detector-off-by-one` | adp_engine `run` | 10 | 1 | KILLED |
| `arc-restart-skips-guard` | adp_engine `run` | 12 | 1 | KILLED |
| `arc-departing-silent` | adp_engine `run` | 4 | 1 | KILLED |
| `arc-noadp-expiry-silent` | adp_engine `run` | 4 | 1 | KILLED |

Every one of the 30 earlier arms fails exactly the count its README row records. The
two mutations #85 names are `walk-down-answers-discover` (16, both DISCOVER rows x DOWN
and x NOT STARTED) and `walk-delay-ignores-link-down` (4, LINK_DOWN x both DELAY
phases). Patch sha256 (first 16) of the eight new arms:

- `arc-bind-keeps-discovered.patch` `fd778c3bb4ab4f48` (391 B)
- `arc-departing-silent.patch` `e11bf7c67ccd783b` (332 B)
- `arc-discover-no-noadp-arm.patch` `3a84cba7ecce5b95` (352 B)
- `arc-fresh-no-rearm.patch` `35e7117c8228d309` (456 B)
- `arc-noadp-expiry-silent.patch` `98106f38dbcaf3e9` (361 B)
- `arc-not-discovered-no-guard.patch` `672dcf7df2b3e145` (404 B)
- `arc-restart-detector-off-by-one.patch` `615a85d82612d599` (465 B)
- `arc-restart-skips-guard.patch` `21e3388bf584d2cd` (453 B)

## 5. available_index interop adjudication

**The note at base** (tb/adp_engine/README.md, and the engine banner
`hdl/adp/KL_adp_engine.sv:33-42`, `:703-707`): the engine implements the doc rule
(0 at power-up, +1 after each ENTITY_AVAILABLE, 0 after ENTITY_DEPARTING) and "diverges
from the reference platform's every-ADPDU increment; adjudication against live
controllers (Hive / la_avdecc) is required before cutover".

**The standard's text.**
- IEEE 1722.1-2021 §6.2.2.15: "The available_index value is incremented after
  transmitting an ENTITY_AVAILABLE message and is reset to zero (0) when transmitting an
  ENTITY_DEPARTING or after a power cycle." Figure 6-2 (§6.2.4.3): INITIALIZE sets it to
  0; ADVERTISE calls sendAvailable(); WAITING adds 1.
- §6.2.5.2.2 txEntityDeparting(): "All other fields are set per the entityInfo variable",
  so the ENTITY_DEPARTING carries the value the index holds; the reset follows. The
  engine does exactly that (walk cells SHUTDOWN x WAITING and both DELAY phases: the
  DEPARTING is byte-exact with the pre-reset index, then the index is 0).
- Milan v1.2 §5.6.2: ADPDUs are formed "as described in [ATDECC, Clause 6]" with
  clarifications that do not touch available_index. Milan §5.6.4.5.2 step 2 reads an
  index at or below the last as a talker restart (DEPARTED then DISCOVERED).
- The "every-ADPDU, no reset" rule therefore departs from §6.2.2.15 at ENTITY_DEPARTING,
  and only there: the only other ADPDU a PAAD sends is ENTITY_AVAILABLE, after which both
  rules increment. The parent's register map (`docs/reference/REGISTER_MAP.md`, the
  `0x644` note at dev `5fabb46e`) records the failure the every-ADPDU rule was adopted
  against: a bump-on-change-only index that repeated across adverts. §6.2.2.15 cannot
  repeat an index within an availability cycle either.
- No receiver reads the index of an ENTITY_DEPARTING: IEEE §6.2.6.4 DEPARTING removes the
  entity; Milan §5.6.4.5.3 has no index step; and TK_NOT_DISCOVERED takes any index
  (§5.6.4.5.1). The difference shows only to a receiver that lost the DEPARTING: under
  §6.2.2.15 the next cycle starts at 0, which §5.6.4.5.2 reads as the restart it is;
  under every-ADPDU it would continue from the last index + 1, read as the same cycle.

**The reference behaviour on record.** The parent's bench lanes B6, B7 and B8 (parent
issue #629) each ran an identity gate that ends with an ADP enumeration from the
controller host: `avdecc_ro.py discover <iface> 4` sends one ENTITY_DISCOVER with
entity_id 0 and logs every ENTITY_AVAILABLE for 4 s. Read with `git show` from the scratch
parent's remote branches only (nothing checked out, no bench access):

| Lane, run | Branch (tip) | File (blob, sha256 first 16) | UTC | This processor: available_index | Reference peer: available_index | Identity gate |
|---|---|---|---|---:|---:|---|
| B6 | `b6-review-evidence` (`36c1ea1f`) | `review-evidence/b6-r1/author/identity/adp-discover.jsonl` (`bd95c05c`, `6c1f6447...`) | 2026-10-01 11:07:48 | 13215 | 12817 | UART smoke PASS 10/10; AECP identity PASS |
| B7 | `629-b7-review-evidence` (`897788f4`) | `review-evidence/629-b7-r1/author/identity/adp-discover.jsonl` (`9b0993f8`, `bfa52d19...`) | 2026-10-03 12:30:19 | 85 | 42441 | IDENTITY GATE: PASS |
| B8 | `629-b8-review-evidence` (`9c4de5ad`) | `.../629-b8-r1/author/identity/adp-discover.jsonl` (`fc13336e`, `65e09021...`) | 2026-10-03 15:57:38 | 1865 | 44513 | IDENTITY GATE: PASS |
| B8 resume | same | `.../identity-resume/adp-discover.jsonl` (`fdb226d5`, `93ad7d6c...`) | 2026-10-03 16:31:25 | 2156 | 44851 | IDENTITY GATE: PASS |
| B8 after power cycle | same | `.../identity-postboot/adp-discover.jsonl` (`9fbc2f96`, `b3d098fb...`) | 2026-10-03 16:52:20 | 19 | 45061 | IDENTITY GATE: PASS |

This processor is the entity with entity_capabilities `0x0000C588` (the F04.6 value),
talker 2 and listener 2; the peer is the bench's reference Milan entity (its identity is
masked in the published evidence and is not repeated here). Rates from the records'
own timestamps:

| Interval | Peer: increments, seconds, s per increment | This processor |
|---|---|---|
| B6 to B7 | 29,624 in 177,749 s: 6.000 | restarted (13215 to 85): a reload between the lanes (the model id moved, `001bc5c40236ba0e` to `001bc5c1935893e1`) |
| B7 to B8 | 2,072 in 12,440 s: 6.004 | 1,780 in 12,439 s: 6.988 |
| B8 to resume | 338 in 2,025 s: 5.992 | 291 in 2,027 s: 6.965 |
| resume to after the power cycle | 210 in 1,257 s: 5.983 | restarted (2156 to 19) |

Reading: within a boot this processor's index rises one per 6.96 to 6.99 s, the Milan
cadence of one ENTITY_AVAILABLE per T-ADP-ADV (5 s) plus the T-ADP-DELAY draw (uniform
0..4 s, mean 2 s): one increment per ENTITY_AVAILABLE. After each restart it starts low
again (§6.2.2.15's power cycle). The peer's index rises strictly, one per 6.0 s, with
no repeat and no restart across 2.2 days of record. The controller host enumerated both
entities in all five runs, and every identity gate passed. No ENTITY_DEPARTING appears in
any record, and `avdecc_ro.py` is a stateless read-only probe (one process per run), not
a controller that tracks entities: the one case where the two rules differ is not on
record, and nothing on record contradicts §6.2.2.15.

**Verdict.** The engine's rule is the standard's and stands; the divergence the note
recorded was the former reference-platform rule's from the standard, not the engine's.
The README limit is restated, not closed: open is only how a live controller that tracks
entities (Hive, la_avdecc) handles an ENTITY_DEPARTING and the availability cycle that
follows it from index 0. Only a live controller across an entity disable and re-enable
can show it (assignment item 4: stated, limit restated, no STOP). The engine banner keeps
its earlier wording, because this lane changes no RTL; `docs/10_RESOURCE_AND_EFFORT.md`
item 10 (a planning record of the same divergence) is left as it is.

**Branch note.** The assignment names `629-review-evidence` for B6. That branch carries
lane M1's packet (`review-evidence/629-r1`, a media-clock design lane) and no
enumeration. B6's packet is on `b6-review-evidence`; its `adp-discover.jsonl` blob
`bd95c05c` is the same at `422dcf91` and `b23b7dd9`, the two B6 commits B7's reviewer
privacy-scanned (`review-evidence/629-b7-r1/reviews/R451-3/receipts/privacy_scan_b6_evidence_*.txt`).
I read it there, read-only.

**A tool detail, for whoever reuses the record.** `avdecc_ro.py`'s `parse_adp` reads
`cfg` from ADPDU octets 52..53 (identify_control_index) and `interface_index` from
56..57 (association_id); IEEE Figure 6-1 puts current_configuration_index at 50 and
interface_index at 54. The `available_index` it logs (octets 36..39) is right. Not used
above beyond available_index, model id and capabilities.

## 6. Processor suites

`./scripts/run_suites.sh` at head, pinned Verilator 5.050 first on `PATH`:

| Suite | Checks | Verdict |
|---|---:|---|
| `acmp_listener` | 2,988 | PASS |
| `acmp_nvm` | 388 | PASS |
| `acmp_talker` | 1,342 | PASS |
| `adp_engine` | 1,330 | PASS |
| `aecp_notify` | 14 | PASS |
| `ca_originator` | 16 | PASS |
| `desc_mem_guard` | 78 | PASS |
| `desc_store` | 586 | PASS |
| `dispatch` | 211 | PASS |
| `dyn_state` | 118 | PASS |
| `event_router` | 81 | PASS |
| `lsn_admit` | 18 | PASS |
| `maap` | 196 | PASS |
| `nvm_port` | 1,219 | PASS |
| `originator` | 107 | PASS |
| `pp_top` | 10,416 | PASS |
| `prng` | 76 | PASS |
| `release_merge` | 18 | PASS |
| `resp_buf` | 64 | PASS |
| `rx_slots` | 130 | PASS |
| `rx_validator` | 555 | PASS |
| `scoreboard` | 3,705 | PASS |
| `side_port` | 368 | PASS |
| `srp_admission` | 991,231 | PASS |
| `srp_decoder` | 190 | PASS |
| `srp_encoder` | 581 | PASS |
| `srp_stream_fsms` | 1,219 | PASS |
| `srp_top` | 2,200 | PASS |
| `timer_map` | 1,360 | PASS |
| `timer_service` | 48 | PASS |
| `tx_arbiter` | 66 | PASS |
| `tx_slots` | 95 | PASS |
| `ucpu` | 437 | PASS |

rc 0, 33 suites, `suites: 1021451 checks total, 0 failing`, 722 s. Its pre-gates: `UPC MAP GATE: PASS (61 engine constants, 89 entry points, all agree)`; `M9 OPCODE GATE SELFTEST: 9 of 9 PASS`; `M9 OPCODE GATE: PASS (30 engine opcodes, all swept by M9)`. The `1d5b680` sweep gave the same per-suite tallies (857 s).

Also at head: `./scripts/lint_hdl.sh` rc 0 (41 LINT OK). `tb/adp_engine` alone at head:
1330 checks, 1330 PASS (base 1328; the two new checks are the citation counts).

## 7. Campaigns

| Campaign | Touched | Result at head |
|---|---|---|
| `tb/adp_engine` `mutants.py --jobs 4` (`make mutants`) | yes: eight arms added | rc 0, 2 controls PASS, 38 of 38 arms KILLED, 40 of 40, 154 s |
| `tb/srp_top`, `tb/maap`, `tb/pp_top` (aecp, aecp-dispatch, d3, ctr, gsi, notify), `tb/acmp_listener` and the other drivers | no: no file they read changed (this lane changes only `tb/adp_engine`, docs and the review) | not run |

## 8. Gates

| Gate | rc | Result |
|---|---:|---|
| Yosys: `./syn/yosys/run.sh` (sv2v 0.0.13, Yosys 0.66) | 0 | `YOSYS 42 tops, all.v parsed 1 time(s)`, `YOSYS XILINX OK KL_aecp_engine`; 45 s |
| `make check` | 0 | lint 41 mermaid + 18 wavedrom, wavedrom 18, links 1120 checked (base 1114), matrix 115 REQ rows, 17 GAP, 94 rows 0 untested, parameters 28/28/28 |
| `python3 scripts/gen_matrix.py --check` | 0 | `matrix: OK (94 rows, 0 untested)` |
| `./scripts/lint_hdl.sh` | 0 | 41 modules LINT OK |

## 9. Parent consumer set

Scratch parent `$VALIDATION_STORAGE/pp85-a524/parent` (never committed or pushed): a fresh
clone of `https://github.com/kebag-logic/milan-fpga.git`, detached at dev
`5fabb46e767c9308ab2580916237f43577698c6e`; submodules `external` `efeb541a`,
`gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e`; `protocol-processor`
fetched from this lane's branch and detached at `a866973`, the gitlink set in the index
only (`git update-index --cacheinfo 160000,a8669732...,protocol-processor`;
`git submodule status` shows ` a8669732...`). The three patches of this directory, each
`git apply --check` clean then `git apply`, in order: `parent-adoption-c8-bbf704ec.patch`
(sha256 `3340d2e8...b38a4c`), `parent-adoption-p2-p1-1269cdaf.patch`
(`d3034e89...613d84`), `parent-adoption-c10-1269cdaf.patch` (`55e62329...ea34b9`). All
three apply to `5fabb46e`. Ignored build products were cleaned (`git clean -ffdX`, parent
and processor) before the head run. Pinned Verilator 5.050 first on `PATH`, host GNU Make
4.4.1. Every command wrote its own log and rc file; none was piped.

| # | Command | rc | Result at dev `5fabb46e` + c8 + p2-p1 + c10, processor `a866973` |
|---:|---|---:|---|
| 1 | `scripts/check_cpp_idiom.py` | 0 | every count 0 <= 0 (c-style cast, file-scope mutable, macro constant, unnamed enum, multi-declarator, long function, build without warnings) |
| 2 | `scripts/check_py_idiom.py` | 0 | every ratchet held |
| 3 | `scripts/check_rtl_source_lists.py` | 0 | 108 files in the `milan_datapath` closure, 4 of 4 consumer lists; protocol-processor 42/42 tops, 0 recorded |
| 3s | `scripts/check_rtl_source_lists.py --selftest` | 0 | 50 checks, 50 PASS |
| 4 | `scripts/pp_srcs.py --check --selftest` | 0 | 46 tracked sources derived, self-test passed |
| 5 | `scripts/check_port_contracts.py` | 0 | protocol-processor 1,759 ports, 111 <= 111 undocumented |
| 6 | `scripts/measure_naming.py --check` | 0 | 95 candidates, all recorded |
| 7 | `scripts/measure_test_evidence.py --check` | 0 | 72 <= 77, 10 <= 10, 0 <= 0, 3 <= 3 |
| 8 | `scripts/docs_check.py` | 0 | 0 findings across 186 md + 970 files |
| 9 | `scripts/xvlog_gate.py --check` (Vivado 2026.1 `xvlog` on `PATH`, alone, last) | 0 | `PASS (3 finding(s) == ratchet; 0 hdl/, 3 pinned processors)`; 145 s |
| 9s | `scripts/xvlog_gate.py --selftest` (alone) | 0 | PASS; 21 s |
| 10 | `sw/builder/test_builder.py` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN (its gate 11 needs a local board build tree, as in the C10 and P1 records); 1,157 s |
| 11 | `scripts/lint_rtl.py --check` | 0 | 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j16` | 0 | 606, 606, 646, 311 checks, 0 failures; 224 s |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | lint pass |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315 checks, 315 PASS, `RESULT: PASS`; 30 s |
| 15 | `make -C tb/verilator/milan_dp -j16 VERILATOR_JOBS=3` | 0 | 9 `RESULT: PASS`, 0 FAIL; render and gmstep control campaigns 6 of 6 each; 1,578 s |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | **2** | two-stream leg 65 checks, 0 failures; shipping leg 155 checks, **2 failures, both T30 INTERNAL LAW** (`the fill at accept is the 8-event setpoint for every PDU got=227 exp=292`; `every PDU's first event is inside the law band got=285 exp=292`; first-event delay 18396..18821 cycles = 8.830..9.034 media ticks); 135 s. Per the assignment these go against milan-fpga #643 (open: "milan_dp_render T30 INTERNAL law depends on the feed's phase against the grid"); see the base control below |
| 16b | `python3 tdm8_render_mutants.py --leg-defects` (in `tb/verilator/milan_dp_render`, the part of gate 16's `run` recipe that make skipped after the failing leg) | 0 | 2 clean controls PASS (`ship --crf-only`, `ship --serial-only`), 3 of 3 leg defects caught; 5 of 5; 413 s |
| 17 | `scripts/check_sh_idiom.py` | 0 | every count held (no strict mode 5 <= 5, ...) |

**Base control for gate 16.** The same parent, with the processor submodule and gitlink
moved to `main` `5c71928a` and the render directory's build products removed, then
`make -C tb/verilator/milan_dp_render tdm8render -j16`: rc 2, the shipping leg's 155
checks with the same 2 failures, the same lines and the same numbers (18396..18821
cycles, got=227, got=285; T30 CRF LAW 17051..17055 cycles in both). `git diff
5c71928a a866973 -- hdl scripts syn` is empty: the render bench reads the same RTL and
generators at both. The failure is the parent's #643 at this dev revision, not this
lane's. It ran once, between gates 15 and 9 of the `1d5b680` round (section 11), after
which the submodule and gitlink were restored and the render build products removed;
`hdl`, `scripts` and `syn` are identical at `5c71928a`, `1d5b680` and `a866973`. (Other records saw T30 pass: C10 at dev `1269cdaf`
with its processor, the issue #232 lane at dev `bbf704ec` with processor `3ab2e4da`; #643
records why: the law depends on the feed's phase against the grid, which the dev
revision and the processor's boot length both move.)

## 10. Parent-visible list

- No RTL, port, parameter, register or behaviour change: `hdl/` is untouched, so the
  parent sees the processor of `5c71928a` (port contract 1,759 ports, 111 <= 111
  undocumented, unchanged).
- No parent patch is needed beyond the three adoption patches already in this
  directory; they apply to dev `5fabb46e` unchanged.
- One parent doc sentence no longer describes the processor: `docs/reference/REGISTER_MAP.md`
  (dev `5fabb46e`), the `0x644` ADP_STATUS note, says available_index "increments on
  EVERY transmitted ADPDU — periodic re-advertise, discover response and departing
  alike". The processor increments after each ENTITY_AVAILABLE (periodic and discover
  responses alike) and resets to 0 after an ENTITY_DEPARTING (IEEE §6.2.2.15). A parent
  lane may want to correct it; this lane does not touch the parent.

## 11. Run record

Logs and rc files are in the scratch directory `$VALIDATION_STORAGE/pp85-a524/` (`logs/`,
`pg/` for the head round, `pg-h2/` for the `1d5b680` round, `mut-h3/` and `mut-h2/`),
never in this directory.

- Base `5c71928a`: `tb/adp_engine` 1328 checks PASS; `make check` rc 0 (links 1114).
- Round 1, the tree that became `c0d5860` / `f80fa44`: the eight arc arms alone (`--only`,
  `--jobs 9`) rc 0, 9 of 9; the full campaign rc 0, 40 of 40, 169 s; at `f80fa44` lint,
  `make check`, gen_matrix and Yosys rc 0. I stopped its processor sweep and the parent's
  gates 10 and 12 partway, to align four discovery-cell citations with F04.8.
- Round 2, `1d5b680`: sweep rc 0 (857 s), campaign rc 0 (150 s), lint, gen_matrix,
  `make check`, Yosys rc 0; every parent command 1 to 17 with 3s, 9s and 16b, the same
  verdicts as the head round, and the gate 16 base control at `5c71928a`. A review of the
  diff then found a rounding error in the README (6.97 for 6.96 s) and two fresh-index
  cells citing one clause fewer than F04.8, fixed in `a866973`.
- Round 3, head `a866973`, everything again: the sweep and the ADP campaign concurrently;
  lint, gen_matrix, `make check`, Yosys; the parent's light gates; gates 10 and 12, 16,
  16b concurrently (beside the end of the sweep); 15 beside the end of 10; gate 9 and 9s
  alone, last. Every verdict and count equals round 2's. Memory peak of this session's
  unit: 9.7 GB of its 12 GB cap. Every command wrote its own log and rc file; none was
  piped.
- Standards read for the citations: IEEE 1722.1-2021 (and the 2013 edition for the
  clause-number check) and Milan v1.2 (Consolidated, Final 2023-11-30), from the host's
  licensed copies; extracted text kept in scratch only.
