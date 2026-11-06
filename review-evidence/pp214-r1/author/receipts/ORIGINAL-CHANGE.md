## 1. Reproduction at the base

A testbench at the base RTL (base `hdl/` + the head's `tb/`) shows the doubled vector in both
shapes the issue reports. Receipts: `receipts/repro-base/`.

- `tb/srp_top` group `onevec`, OV1 (the capture's shape, MSRP Domain): the peer's LeaveAll
  MRPDU (every type flagged, its Domain {6, 3, 2} re-declared in the flagged vector) every
  1030 ms, sliding across periodic! and the T-MRP-JOIN tx!. 7 of 63 frames carrying the
  Domain carry it twice, `JoinIn JoinIn`, in exactly the windows that held a periodic!.
- OV2 / OV5 (MVRP VID 2): VID 2 twice after a received MVRP LeaveAll with periodic!, and up
  to eight times in one MVRP MRPDU when several LeaveAll re-join walks fall in one window;
  one own MVRP LeaveAll MRPDU carries VID 2 in its LeaveAll vector and again in further
  vectors (8 of 10 LeaveAll MRPDUs carry it once).
- OV4 (own MSRP LeaveAll), OV6 (LINK_UP: `New JoinMt`), OV7 (adoption: New {6, 5, 5} then
  JoinIn {6, 5, 5}) fail the same way; OV0 counts every MRPDU of the default run: 69 of
  17,643 carry a value twice. The default run reads `8681 checks: 8673 PASS, 8 FAIL` (OV0 to
  OV7); every existing check passes. Measured with the testbench of `44557b2`, whose suite sources
  equal the final head's (`receipts/repro-base/TREE.txt`, `srp_top_full.verdict.txt`).
- `tb/srp_encoder` PV1-PV12 at the base: `692 checks: 644 PASS, 48 FAIL` (every PV row except
  PV8, plus O8 as restated). The base appends every push: 7 more octets per doubled Domain
  vector, 5 per VID.
- Talker and Listener values are never doubled at the base (OV3, OV8, OV9, OV10 pass): the
  stream applicants transmit only at tx! walks, and each walk is drained before the next.

## 2. Cause

`KL_srp_encoder`'s pending tables were append-only event logs. Every producer hand-over took
a new entry, and each entry became its own VectorAttribute (a value is not the +1 successor
of itself, so runs never fold it). Two hand-overs of one value in one transmission window
therefore put the value in two VectorAttributes of one MRPDU. The producers hand a value over
again whenever a second reason to send it falls in the window:

- `KL_srp_domain`: periodic! re-joins at once, a received LeaveAll re-joins at the next tx!,
  the own LeaveAll at its tx!; LINK_UP and adoptions queue New (and Lv of the old value).
- `KL_srp_vlan`: periodic!, received and own LeaveAll each run a re-join walk over every
  held VID; a new VID's New precedes them.

802.1Q-2022 10.7.7 keeps one Applicant per attribute value; a VectorAttribute carries an event
for every value of its range (10.7.5.13 c), 10.8.2.10.1), so a value in two VectorAttributes
is two events for one state machine (the peer's MRP logged two rJoinIn).

The fix is at the queueing point: the table now holds one entry per value, so a second
hand-over cannot queue the value a second time. That also covers paths the reproduction did
not reach (several adoptions in one window, a deferred drain behind TX backpressure) for all
four participants, without touching `KL_srp_listener_fsm.sv`.

## 3. Changes (file:line at the head, clause)

| # | File:line | Change | Clause |
|---|---|---|---|
| 1 | `hdl/srp/KL_srp_encoder.sv:27` (banner), `:78` (Decision), `:101` (`ev_ready_o` note) | one entry per value; the search's cost | 802.1Q-2022 10.7.7, Table 10-3, 10.7.5.13 c), 10.8.2.10.1 |
| 2 | `hdl/srp/KL_srp_encoder.sv:190` (event codes), `:205` (`key_f`) | a value's identity: application, AttributeType, first eight octets of FirstValue (StreamID; Domain value; VID) | 10.8.1.2; 35.2.2.8.1, 35.2.2.8.2, 35.2.2.8, 35.2.2.9.1, 11.2.3.1.7 |
| 3 | `hdl/srp/KL_srp_encoder.sv:212` (comment), `:222` (`merge_ev_f`), `:234` (`merge_fp_f`) | the one message a merged entry carries | 10.7.7; Table 10-3 (New!, Lv!; VN under Join!, periodic!, rLA!; LA + Join! = AA); 10.7.6.3, 10.7.6.5, 10.7.6.12; 35.2.2.7.2 |
| 4 | `hdl/srp/KL_srp_encoder.sv:421` (search signals, `ev_ready_o` `:457`, read/write address muxes), `:467` (`value_search`), `:481` (`pend_write` merged write), `:496` (`pend_read` at the shared address) | search the target table through its own read port, one entry per clock; a hit rewrites in place, a miss appends; the search starts again when the offer changes | 10.7.7 |
| 5 | `hdl/srp/KL_srp_encoder.sv:679` (`cnt_*` increment) | a merge takes no new entry | — |
| 6 | `tb/srp_encoder/sim_main.cpp:1430` (O8) | restated: VID 3 is taken on the clock after the join clock (one search clock), still before any MVRP drain | — |
| 7 | `tb/srp_top/sim_main.cpp:1281` (N9) | stimulus re-cut: twelve adoptions fill the table (each adoption's Lv now takes the entry of the New before it) | — |
| 8 | `tb/srp_top/mutations/` 8 patches | cut again as the same edit (their context held the rewritten `ev_ready_o` line); verified edit-identical | — |
| 9 | `tb/srp_encoder/sim_main.cpp:1507` to `:1730` (PV1-PV12); `tb/srp_top/sim_main.cpp:331` (`doubled_values()`), `:502` (every frame of the run), `:728` (OV0), `:3408` (`check_one_vector_per_value`, OV1-OV10); `tb/srp_top/srp_top_wrap.sv:135`, `:179` (two read-only probes) | new checks | acceptance 1, 2 |
| 10 | `tb/srp_top/mutants.py:281` and 8 new patches; `:215`, `:245` (two issue #193 arms re-pointed) | new campaign arms | acceptance 2 |
| 11 | `docs/architecture/10_srp_engine.md:113` (§3 `sec-10-one-vector`), `:263` (§5.1), `:361` (§6.1), `:415` (§6.2), `:882` (§6.5); `docs/architecture/09_verification.md:823` (§8.14); both suite READMEs | documentation | — |

(line numbers at `44557b2`; the later commits touch only `tb/srp_top/mutants.py`, one patch, the
`tb/srp_top` README and the two architecture documents.)

## 4. New checks (planted arm, failing words)

Counts below are the round 1 recorded results. The round 2 campaign will confirm the merged results.

| Check (failing words) | What it requires | Planted arm | Failing |
|---|---|---|---:|
| `OV1:` ... `OV7:`, `OV0:` (`tb/srp_top` onevec) | see §1 and the README table | `second-queueing`: `sr_hit_w` tied 0, so every push appends (the base's second queueing) | 8 (OV0-OV7) |
| `PV1 two re-joins of one Domain value` (`tb/srp_encoder`) | the capture's shape at unit level: one JoinIn | `second-queueing` | 46 (every PV row but PV8) |
| `OV6:` (LINK_UP: New first) | a later join keeps a pending New | `join-displaces-new` | 2 (OV6, OV7) |
| `PV2 New then a re-join` | same, unit | `join-displaces-new` | 5 (PV2, PV6, PV9, PV12 x2) |
| `PV4 a re-join then Lv` | a later Lv replaces | `leave-does-not-replace` | 2 |
| `PV5 JoinIn then Mt` | an s replaces only an s | `s-displaces-declaration` | 3 (PV5 x2, PV6) |
| `PV6 Listener Ready then AskingFailed` | the newer declaration type | `listener-type-oldest` | 2 |
| `PV8 three types of one StreamID` | AttributeType in the identity | `merge-ignores-type` | 2 |
| `PV10 a value offered after another` | the search starts again when the offer changes | `search-no-restart` | 3 |
| `SW1:` (`tb/srp_top` share) | one Listener vector per shared stream, now held by two layers | `listener-shares-nothing-encoder-appends` (issue #193's settle compare dropped and `second-queueing`) | 6 (SW1-SW3, OV0) |

Rows with no killer by construction: OV8, OV9, OV10 pass at the base too (stream applicants
transmit only at tx!), so no arm of this change fails them; they are property rows for
acceptance item 1.

