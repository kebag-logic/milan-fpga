# `tcam` — ternary CAM destination-MAC database (design doc)

**Module:** [`hdl/ieee8021q/filtering/tcam.sv`](../tcam.sv)
**Verification:** [`tb/verilator/tcam/`](../../../tb/verilator/tcam) — 19 self-checks, PASS
**Relates to:** `REQ-MAC-02` (RX MAC filtering), `MC_HASH_*` CSR, the AVDECC/gPTP
control-frame tap (`OPEN`/migration §B.1).

## 1. What it is

A small **register-based ternary CAM** that acts as a *destination-MAC database*:
a table of entries that software adds / removes / updates, and against which each
incoming frame's destination MAC is matched to produce an **action** (a tag/queue/
accept-drop code). "Ternary" = every entry has a per-bit **mask**, so one entry can
match an exact address *or* a range/prefix.

```
entry i = { valid, key[47:0], mask[47:0], action[A-1:0] }
hit[i]  = valid[i] && (((lookup_key ^ key[i]) & mask[i]) == 0)
match   = |hit ; match_index = lowest set hit (index 0 = highest priority)
```
`mask` bit **1** = "this key bit must match"; **0** = "don't care" (wildcard).

## 2. Why ternary (vs an exact-match CAM)

Forencich's [`verilog-cam`](https://github.com/alexforencich/verilog-cam) is a
**binary CAM (BCAM)** — exact match only (`cam.v`/`cam_bram.v`/`cam_srl.v`). It is
excellent for large *exact* MAC tables (e.g. thousands of learned unicast
addresses). But it cannot express a **range/prefix**, which MAC steering needs:

| Pattern | key | mask | matches |
|---------|-----|------|---------|
| exact gPTP pdelay | `01-80-C2-00-00-0E` | `FF-FF-FF-FF-FF-FF` | that one address |
| reserved multicast block | `01-80-C2-00-00-00` | `FF-FF-FF-FF-FF-F0` | `01-80-C2-00-00-0x` (16 addrs, one entry) |
| a vendor OUI | `91-E0-F0-00-00-00` | `FF-FF-FF-00-00-00` | any `91-E0-F0-xx-xx-xx` |

So this TCAM is the ternary piece Forencich doesn't ship. For a MAC filter the table
is small (tens of entries), so a **register-based parallel match** (every entry
compares in one cycle, priority-encoded) is the right, FPGA-independent choice —
no BRAM, Verilator-friendly. `verilog-cam`'s BCAM can be vendored alongside if a
large exact-match table is also wanted.

## 3. Interface

- **Write / configure (add · remove · update):** `wr_en_i`, `wr_index_i`,
  `wr_valid_i` (1 = add/update, **0 = remove**), `wr_key_i`, `wr_mask_i`,
  `wr_action_i`. One indexed entry per write — trivially CSR-mappable (an
  `TCAM_KEY/MASK/ACTION/CTRL[index]` register group).
- **Lookup (combinational):** `lookup_key_i` → `match_o`, `match_index_o`,
  `match_action_o`, plus `match_vec_o` (raw per-entry hits, for debug / multi-hit).

Params: `KEY_WIDTH` (48 = dest MAC), `NUM_ENTRIES` (16), `ACTION_WIDTH` (8).

## 4. How it fits the datapath

Feed `lookup_key_i` the destination MAC the classifier already extracts from the
Ethernet header; use `match_action_o` to steer/gate the frame. Suggested `action`
encoding (example): `[0]` accept, `[1]` drop, `[3:2]` target queue, `[4]` timestamp.

This gives **exact + ternary** RX filtering — a precise upgrade over the
approximate `MC_HASH` hash filter (`REQ-MAC-02`): the hash admits false positives
(different MACs share a bucket); the TCAM matches precisely and returns a
per-entry action. It is exactly what the **control-frame tap** needs — steer
gPTP `01-80-C2-00-00-0E`, AVDECC/ADP `91-E0-F0-01-00-00`, and MAAP-allocated stream
multicasts to the control/stream queues, everything else to best-effort or drop.

Typical power-on entries a driver would install:

| idx | key | mask | action |
|-----|-----|------|--------|
| 0 | `01-80-C2-00-00-0E` (gPTP) | exact | to control queue + timestamp |
| 1 | `91-E0-F0-01-00-00` (AVDECC) | exact | to control queue |
| 2 | `01-80-C2-00-00-00` | `..-F0` | reserved multicast → drop/control |
| 3 | station unicast | exact | accept |
| 4 | `FF-FF-FF-FF-FF-FF` | exact | accept (broadcast) |
| … | MAAP stream dests | exact | accept → stream queue |

## 5. Verification

[`tb/verilator/tcam/sim_main.cpp`](../../../tb/verilator/tcam/sim_main.cpp) programs
the table and checks: empty-table miss, **exact** match, **ternary/range** match,
**priority** when an address hits both an exact and a range entry (lowest index
wins), the **multi-hit vector**, clean **miss**, and **remove / update** of entries.
19 checks, `RESULT: PASS`.

## 6. Notes / extensions
- Combinational match; pipeline `match_*` with a register stage if timing needs it.
- Scale by raising `NUM_ENTRIES` (register cost grows linearly — fine to ~64). For
  hundreds/thousands of *exact* entries, front it with Forencich `verilog-cam`
  (BCAM) and keep the TCAM only for the handful of ranged/control patterns.
