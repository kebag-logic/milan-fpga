[A599]

Closes #35

`rx_err_i` raised with any byte of a frame now refuses that frame. The parser used to read the flag only in its end-of-frame branch, so a pulse on any earlier byte was ignored and the frame dispatched. Following the ruling on #35 (the safer default), the flag now latches into the parser's existing drop state on every valid byte, the first and the last included. The frame is consumed to its eof and counted exactly once, with no event and no bank write after the flagged byte, however many of its bytes carry the flag. Pulsing the flag on the corrupt byte and holding it to eof refuse alike. A flag raised between bytes, with `rx_valid_i` low, belongs to no byte and is ignored. The port comment, the module header and the integration guide state this contract.

Frames without an error behave exactly as before. With `rx_err_i` tied low, the base and head parsers are formally equivalent: all 748 equivalence cells are proven. With the port left free exactly one cell, `bad_r`, stays unproven, so the proof is not vacuous.

## Change

- `hdl/wire/KL_gptp_rx_parser.sv:645`: one line, `if (rx_err_i) bad_r <= 1'b1;`, inside the valid-byte branch and below the sof arm. A flag on the first byte therefore outlasts that arm's clear. The eof byte's own flag still reaches `fin_ok_r` directly (`:625`), because `bad_r` settles on the same edge. Port comment `:109`, DROP-arm list `:32`, contract paragraph `:52-62` and eof-gate comment `:620-621`.
- `tb/verilator/parser/sim_main.cpp`: a `feed_err(bytes, from, to)` feeder that also counts bank writes after the first flagged byte, and `check_rx_err_on_any_byte_drops_the_frame()`, 30 new checks (parser suite 268 -> 298). It runs last, so the existing drop-count total is untouched.
- `tb/verilator/parser/mutants.py` (new) and `Makefile`: a mutation arm with seven mutants. `all: run mutants` is now the default goal, so `make tb` runs it. Every check a mutant names must appear in a FAIL line; a red tally alone does not count.
- Docs: `docs/INTEGRATION.md` receive table and contract lines; `docs/SOURCE_EVIDENCE.md` gets a new anchorless row, two parser anchors moved by the header lines (#L374 -> #L386, #L456 -> #L468), and #35 under closed work; the #35 risk bullets removed from `README.md` and `docs/MANAGER.md`; `docs/TEST_DEVELOPER.md`, `docs/HDL_DEVELOPER.md` and the parser README describe the contract and the arm.

Nothing outside the parser, its tests and its documentation changes. No microcode, no engine RTL, no checker script.

## Per-position result

The flag is raised for one byte at every position of a Sync (58 bytes), a Follow_Up (90), a Pdelay_Req (68) and a Pdelay_Resp (68): 284 frames. Measured with the head bench against base and head RTL; "writes after" counts bank writes after the flagged byte's own edge.

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

The base rows reproduce the issue's measurement: Sync byte 20 and 40 dispatch, byte 57 drops. At head every position is one drop and no event. A first-byte flag leaves no bank write at all. Held from byte 20 through eof: one drop and no event, at base and at head, for all four types. After each sweep, the same frame without the flag dispatches (codes 1, 2, 4, 5) with no drop, so a refusal does not outlive its frame. A Sync streamed with an idle cycle in every gap, each idle cycle carrying the flag, dispatches with no drop.

## Planted control

The arm's first mutant deletes the one latch line, restoring exactly the end-of-frame-only read the base shipped. It fails 12 checks by name, 286 of 298 pass:

```
FAIL sync rx_err at every byte: one drop got 0000000000000001 exp 000000000000003a
FAIL sync rx_err at every byte: no event got 0000000000000001 exp 000000000000003a
FAIL sync rx_err at every byte: no later write got 0000000000000001 exp 000000000000003a
FAIL fu rx_err at every byte: one drop got 0000000000000001 exp 000000000000005a
FAIL fu rx_err at every byte: no event got 0000000000000001 exp 000000000000005a
FAIL fu rx_err at every byte: no later write got 0000000000000011 exp 000000000000005a
FAIL pdreq rx_err at every byte: one drop got 0000000000000001 exp 0000000000000044
FAIL pdreq rx_err at every byte: no event got 0000000000000001 exp 0000000000000044
FAIL pdreq rx_err at every byte: no later write got 0000000000000015 exp 0000000000000044
FAIL pdresp rx_err at every byte: one drop got 0000000000000001 exp 0000000000000044
FAIL pdresp rx_err at every byte: no event got 0000000000000001 exp 0000000000000044
FAIL pdresp rx_err at every byte: no later write got 0000000000000001 exp 0000000000000044
```

Every new check has a mutant that fails it by name:

| mutant | named checks it must fail |
|---|---|
| rx_err read only at eof (the planted control) | every-byte one drop, no event, no later write; four types |
| a first-byte flag lost to the sof clear | every-byte one drop; four types |
| the eof byte's own flag ignored | every-byte one drop, no event; four types |
| every flagged byte counts a drop | held from byte 20 to eof: one drop; four types |
| rx_err ignored on every byte | held from byte 20 to eof: no event; four types |
| the refusal outlives its frame | control after the errors: event, no drop; four types |
| rx_err sampled between bytes | rx_err in every gap between bytes: sync event, no drop |

The arm reports 8 of 8: the clean control plus seven caught. It is itself not vacuous. With the base RTL in place it reports 2 PASS, 6 FAIL: the control fails and five patterns no longer apply. With one named check renamed in the bench it reports 7 PASS, 1 FAIL: that mutant "missed its named check".

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

One point needs a ruling. The parent's gate is hierarchical (`proc; opt_clean`, no flatten), so it elaborates the parser module on its own with `rx_err_i` as a free input. In that view the new line is one `$mux` inside the parser (529 -> 530 cells), and the rollup moves 3567 -> 3568. No implementation of the ruling can avoid that, because the ruling adds behaviour to the parser module itself. Once the tie-off is propagated, the netlist is unchanged: the flattened `stat` is identical, every other module is byte-identical, and the one differing module is proven equivalent under the tie. The ROM digests are unchanged.

## Acceptance

- [x] The contract is stated in the port documentation and the module header, and the code matches it.
- [x] A pulse at any byte refuses the frame with exactly one counted drop, no event and no bank write after the flag. Tested at every byte, the first, mid-frame and the eof byte included, for four types. A first-byte flag leaves no bank write at all. Words written before a later flag stay in the write bank, which no event names, as for every other refusal arm.
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
| `make tb` | rc 0: ucpu 768; parser 268; engine 1613 x3 + mutants 34/34; gaskets 81 + 5/5; tsngen 288 + 4/4; bench tag PASS | rc 0: ucpu 768; parser 298 + parser mutants 8/8; engine 1613 x3 + mutants 34/34; gaskets 81 + 5/5; tsngen 288 + 4/4; bench tag PASS |
| `make contract` | rc 0 | rc 0 |
| `make lint` | rc 0 | rc 0 |
| `make docs` | rc 0, 20 exact anchors | rc 0, 20 exact anchors |

The bench gasket raises its error only with the last byte (`bench/arty/bench_mii_rx.sv:158`), so the bench path behaves as before. No parent adoption is part of this change.
