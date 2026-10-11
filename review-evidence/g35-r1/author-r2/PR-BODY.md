[A599]

Closes #35

`rx_err_i` raised with any byte of a frame now refuses that frame. The parser used to read the flag only in its end-of-frame branch, so a pulse on any earlier byte was ignored and the frame dispatched. Following the ruling on #35 (the safer default), the flag now latches into the parser's existing drop state on every valid byte, the first and the last included. The frame is consumed to its eof and counted exactly once, with no event and no bank write after the flagged byte's own edge, however many of its bytes carry the flag. Pulsing the flag on the corrupt byte and holding it to eof refuse alike. A flag raised between bytes, with `rx_valid_i` low, belongs to no byte and is ignored. The port comment, the module header and the integration guide state this contract, including the bank ruling on #35 (comment 6105869522): words written up to and including the flagged byte are undefined and named by no event, and the next accepted frame's event reads only that frame's data.

Frames without an error behave exactly as before. With `rx_err_i` tied low, the base and head parsers are formally equivalent: all 748 equivalence cells are proven. With the port left free exactly one cell, `bad_r`, stays unproven, so the proof is not vacuous. Round 2 changes no RTL code: with comments stripped the parser is identical to round 1's, and the parent's staged input is byte-identical.

## Change

- `hdl/wire/KL_gptp_rx_parser.sv:652`: one line, `if (rx_err_i) bad_r <= 1'b1;`, inside the valid-byte branch and below the sof arm. A flag on the first byte therefore outlasts that arm's clear. The eof byte's own flag still reaches `fin_ok_r` directly (`:632`), because `bad_r` settles on the same edge. Port documentation `:113-116`, DROP-arm list `:32`, contract paragraph `:52-66` and eof-gate comment.
- `tb/verilator/parser/sim_main.cpp`:
  - `feed_err` splits every bank write of a flagged frame at the flagged byte: before it, on its own edge, and after it.
  - `check_rx_err_on_any_byte_drops_the_frame()`: the flag at every byte of four types, held to eof, controls, and a flag in every gap (30 checks).
  - `check_rx_err_writes_before_on_and_after_the_flag()`: the first byte, byte 29 and the eof byte of four types plus an Announce. Each position must give one drop, no event and no write after the flag; before and on are printed (15 checks).
  - `check_a_refused_frame_leaves_no_stale_word()`: a frame refused at its eof is followed with no gap by a clean frame of the same type and of a different type. The clean frame's event must carry exactly its own fields (24 checks).
  - Parser suite 268 -> 337. The new checks run after the existing drop-count total, which is untouched.
- `tb/verilator/parser/mutants.py` (new) and `Makefile`: a mutation arm with eight mutants. `all: run mutants` is the default goal, so `make tb` runs it. Every check a mutant names must appear in a FAIL line; a red tally alone does not count.
- Docs:
  - `docs/INTEGRATION.md`: the receive table, and the contract lines with a link to the bank ruling.
  - `docs/SOURCE_EVIDENCE.md`: a new anchorless row, two parser anchors moved by the header lines (#L374 -> #L393, #L456 -> #L475), and #35 under closed work.
  - The #35 risk bullets are removed from `README.md` and `docs/MANAGER.md`.
  - `docs/TEST_DEVELOPER.md`, `docs/HDL_DEVELOPER.md` and the parser README describe the contract and the checks.

Nothing outside the parser, its tests and its documentation changes. No microcode, no engine RTL, no checker script.

## Per-position result

The flag is raised for one byte at every position of a Sync (58 bytes), a Follow_Up (90), a Pdelay_Req (68) and a Pdelay_Resp (68): 284 frames. Measured with the head bench against base and head RTL. Every bank write is counted and split at the flagged byte's own edge.

| type | flagged byte | base | head |
|---|---|---|---|
| Sync | 0-56 | drops +0, 1 event, 1-6 writes after | drops +1, 0 events, 0 writes after |
| Sync | 57 (eof) | drops +1, 0 events | drops +1, 0 events |
| Follow_Up | 0-88 | drops +0, 1 event, 0-7 writes after | drops +1, 0 events, 0 writes after |
| Follow_Up | 89 (eof) | drops +1, 0 events | drops +1, 0 events |
| Pdelay_Req | 0-66 | drops +0, 1 event, 0-4 writes after | drops +1, 0 events, 0 writes after |
| Pdelay_Req | 67 (eof) | drops +1, 0 events | drops +1, 0 events |
| Pdelay_Resp | 0-66 | drops +0, 1 event, 1-8 writes after | drops +1, 0 events, 0 writes after |
| Pdelay_Resp | 67 (eof) | drops +1, 0 events | drops +1, 0 events |

The base rows reproduce the issue's measurement: Sync byte 20 and 40 dispatch, byte 57 drops. At head every position is one drop and no event. At every position the writes before and on the flagged byte equal base's: the repair removes only the writes after it. A first-byte flag leaves no bank write at all. Held from byte 20 through eof: one drop and no event, at base and at head, for all four types. After each sweep, the same frame without the flag dispatches (codes 1, 2, 4, 5) with no drop, so a refusal does not outlive its frame. A Sync streamed with an idle cycle in every gap, each idle cycle carrying the flag, dispatches with no drop.

## Bank writes before, on and after the flag

The suite's record at head. Each row is one drop and no event.

| type | first byte | byte 29 | eof byte |
|---|---|---|---|
| Sync | 0 / 0 / 0 | 0 / 1 / 0 | 5 / 1 / 0 |
| Follow_Up | 0 / 0 / 0 | 0 / 1 / 0 | 7 / 0 / 0 |
| Pdelay_Req | 0 / 0 / 0 | 0 / 1 / 0 | 4 / 0 / 0 |
| Pdelay_Resp | 0 / 0 / 0 | 0 / 1 / 0 | 7 / 1 / 0 |
| Announce, no PathTrace | 0 / 0 / 0 | 0 / 1 / 0 | 6 / 1 / 0 |

Each cell is writes before / on / after. Byte 29 completes `w1` on its own edge, so the "on" boundary the ruling accepts is exercised. The Announce is included because its deferred hop-count word `w12` is the only write in the parser that lands after an eof. In the four ruled types no word completes after the eof, so their eof leg is zero by construction.

## No stale word reaches the next event

Each frame draws every field from its own salt, so no word of a refused frame equals the clean frame's. A frame flagged on its eof byte leaves every word it writes. It is followed with no idle cycle by a clean frame, and the bank is kept across both. The engine moves to its other bank only on an accepted event, so in the engine the two frames share one bank too.

| clean frame | after a refused | refused frame's words left | outside the clean type's words |
|---|---|---|---|
| Sync | Sync / Pdelay_Resp | 6 of 6 / 8 of 8 | 0 / 2 |
| Follow_Up | Follow_Up / Pdelay_Resp | 7 of 7 / 8 of 8 | 0 / 2 |
| Pdelay_Req | Pdelay_Req / Sync | 4 of 4 / 6 of 6 | 0 / 2 |
| Pdelay_Resp | Pdelay_Resp / Follow_Up | 8 of 8 / 7 of 7 | 0 / 1 |

In all eight pairs the pair counts one drop, and the clean frame raises exactly one event with its own code and sequence. As that event saw the bank, every word the clean type names held the clean frame's own field. The left-over words outside the clean type's layout are the undefined words the ruling allows; no event of the clean type names them.

## Planted controls

The arm's first mutant deletes the one latch line, restoring exactly the end-of-frame-only read the base shipped. It fails 27 checks by name, 310 of 337 pass. Among them:

```
FAIL sync rx_err at every byte: one drop got 0000000000000001 exp 000000000000003a
FAIL sync rx_err at every byte: no event got 0000000000000001 exp 000000000000003a
FAIL sync rx_err at every byte: no later write got 0000000000000001 exp 000000000000003a
FAIL pdreq rx_err at every byte: no later write got 0000000000000015 exp 0000000000000044
FAIL sync rx_err at first, middle, eof: no write after got 0000000000000001 exp 0000000000000003
FAIL ann rx_err at first, middle, eof: no write after got 0000000000000001 exp 0000000000000003
```

The defect the bank ruling asks for is the arm's last mutant. A refusal leaks into the next frame and skips its `w2` (source identity) write. It fails all eight stale-word checks by name, each showing the refused frame's own word:

```
  sync after a refused pdresp: w2 holds aabbccfffe000303, not aabbccfffe000404, the refused frame's word
FAIL sync after a refused pdresp: every word is this frame's got 0000000000000005 exp 0000000000000006
```

Every new check has a mutant that fails it by name:

| mutant | named checks it must fail |
|---|---|
| rx_err read only at eof (the planted control) | every-byte one drop, no event, no later write (four types); first/middle/eof one drop, no event, no write after (five types) |
| a first-byte flag lost to the sof clear | every-byte one drop; first/middle/eof one drop |
| the eof byte's own flag ignored | every-byte one drop, no event; first/middle/eof one drop, no event; Announce no write after |
| every flagged byte counts a drop | held from byte 20 to eof: one drop |
| rx_err ignored on every byte | held from byte 20 to eof: no event |
| the refusal outlives its frame | control after the errors: event, no drop; stale-word one drop, event (eight pairs) |
| rx_err sampled between bytes | rx_err in every gap between bytes: sync event, no drop |
| a refusal skips the next frame's w2 write | stale-word every word is this frame's (eight pairs) |

The arm reports 9 of 9: the clean control plus eight caught. It is itself not vacuous. With the base RTL in place it reports 2 PASS, 7 FAIL: the control fails, five patterns no longer apply, and the w2 mutant misses because base never latches a refusal for it to leak. With one stale-word check renamed in the bench it reports 8 PASS, 1 FAIL: that mutant "missed its named check".

## Parent identity

Measured in a scratch parent at dev `ac2c5e77`, never committed. Base is dev's own gitlink, `5dce647a`; head has the gitlink set to this branch's head. The parent ties the port low (`KL_gptp_shadow.sv:666` at `ac2c5e77`), and the engine forwards it only to the parser.

| measure | base | head |
|---|---|---|
| `syn/yosys/run.sh --mode elaborate --no-structural --top KL_gptp_shadow` | PASS, cells=3567 | PASS, cells=3568 |
| staged sv2v input, module by module | 9 modules | 8 byte-identical, only `KL_gptp_rx_parser` differs |
| same program then `flatten; opt; opt_clean` | 2432 cells | 2432 cells, `stat` identical for every cell type |
| that parser module, `rx_err_i` tied 0, against base | | equivalent, 748 of 748 cells proven |
| `gptp_ucode.hex`, `ucode.hex`, `ltn_rom.hex` sha256 | match the ledger rows for their pins | identical |
| ROM bundle digest | `018e9be9527f8c41ed605c2c4c5e2c8e134f2d84375758c81a022cbfb7646fd2` | identical |
| `syn/yosys/ooc.sh tcam`, ROM ledger keyed by pin | rc 0 | rc 0 once `--record-rom-digests` adds the new pin's one row, `gptp_ucode.hex c496ed8a...`, the same digest as base's row |

The parent's gate is hierarchical, so the parser module gains one `$mux` (529 -> 530 cells) and the rollup moves 3567 -> 3568. This was ruled acceptable on #35 (comment 6105366046). Once the tie-off is propagated, the netlist is unchanged and the ROM digests are unchanged.

## Acceptance

Item 2 is as amended by the bank ruling on #35 (comment 6105869522).

- [x] The contract is stated in the port documentation and the module header, and the code matches it.
- [x] A pulse at any byte refuses the frame with exactly one counted drop and no event. Tested at every byte, the first, mid-frame and the eof byte included, for four types. As the ruling amends it, there is no bank write after the flagged byte's own edge. This is measured by an oracle that counts every write before, on and after the flagged byte, at the first, a middle and the eof byte. Words written up to and including a later flagged byte stay in the write bank, undefined and named by no event, as for every other refusal arm. A first-byte flag leaves none at all. The next accepted frame's event reads only that frame's data: tested after a refused frame of the same type and of a different type, with a planted skipped write failing by name.
- [x] A planted mutation restoring mid-frame acceptance goes red, permanently, in `make tb`. No current README carries a parser count: the documentation rework moved those figures to the dated history record, which is left as is.
- [x] `feed_gap` drives `rx_err_i` explicitly. This was already true at base and is unchanged.

## Validation

At head, with Verilator 5.050:

```sh
make tb
make contract
make lint
make docs
```

| gate | base `5dce647a` | head |
|---|---|---|
| `make tb` | rc 0: ucpu 768; parser 268; engine 1613 x3 + mutants 34/34; gaskets 81 + 5/5; tsngen 288 + 4/4; bench tag PASS | rc 0: ucpu 768; parser 337 + parser mutants 9/9; engine 1613 x3 + mutants 34/34; gaskets 81 + 5/5; tsngen 288 + 4/4; bench tag PASS |
| `make contract` | rc 0 | rc 0 |
| `make lint` | rc 0 | rc 0 |
| `make docs` | rc 0, 20 exact anchors | rc 0, 20 exact anchors |

The bench gasket raises its error only with the last byte (`bench/arty/bench_mii_rx.sv:158`), so the bench path behaves as before. No parent adoption is part of this change; the next adoption records the new pin's ROM-ledger row.

## Round 2

Answers R616-1 (POSITIVE, one residue) and R617-1 (NEGATIVE on R617-F1) under the scope ruling on #35 (comment 6105869522). Three commits on round 1's head, no rebase or amend:

- `3acd2f5` Count every bank write before, on and after the flagged byte in the parser suite.
- `c5c6646` Prove no word a refused frame leaves reaches the next accepted frame's event.
- `a70e388` State the ruled rx_err_i bank contract in the parser header, port and integration guide.

What each finding received:

- R617-F1: the ruling accepts writes up to and including the flagged byte.
  - The oracle now counts every write, before, on and after, and asserts none after (ruling item 1).
  - The stale-word check, with its planted defect, covers the consumer risk (item 2).
  - The header, port documentation and integration guide state the ruled contract, and acceptance item 2 above cites the ruling (item 3).
- R616-1-RES1: the header sentence is applied verbatim. This body reads "after the flagged byte's own edge" and "up to and including a later flagged byte" (item 4).
- R616-1-S1: not taken. Anchoring the any-byte row needs a checker-script edit outside this change's scope.
- R616-1-S2: partly taken. The bank-write oracle adds an Announce, the one type with a write after its eof. Other shapes remain in the reviewers' probes.

Limits: parser-level evidence only. No engine bench drives `rx_err_i`, and the engine's Announce context is not exercised here. The stale-word check covers the four ruled types.
