# [A599] HANDOFF: lane for #35 (a mid-frame rx_err_i drops the frame)

Status: REVIEW READY at head `5b4ce3974f7627d57b31167bde50cde8f4bdcdf3` (all four donor gates rc 0 at head).

- Repository: Mister-M-alt/FPGA-gPTP, branch `g35-rx-err`, base main `5dce647a`
  (`5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`), remote confirmed
  `https://github.com/Mister-M-alt/FPGA-gPTP.git`.
- Head: `5b4ce3974f7627d57b31167bde50cde8f4bdcdf3` (four commits, local only; not pushed, no PR).
- Assignment: issue #35 comment 6104916029 ([A10]); ruling "the safer default": latch on any byte.
- TAKEN: issue #35 comment 6104922026.
- REVIEW READY: issue #35 comment 6105359326, at head `5b4ce397`, flagging the hierarchical-netlist point for a ruling.
- Roles: executor [A599]; reviewers [R616] (internal) and [R617] (external).

## Commits (one-line subjects, no body, no trailers)

| commit | subject |
|---|---|
| `a7c031f8` | Latch rx_err_i on any byte of a frame into the parser's drop state |
| `fd1d6c9` | Raise rx_err_i at every byte of four message types in the parser suite |
| `05cacb6` | Plant seven rx_err_i defects the parser suite must fail by name |
| `5b4ce39` | Document the any-byte rx_err_i contract and retire the #35 risk lines |

Each step was gated before its commit: step 1 parser suite 268/268 plus lint and docs rc 0;
step 2 parser 298/298 plus docs; step 3 parser 298/298 plus arm 8/8 plus docs; step 4 docs rc 0.

## Changes (file:line at head)

RTL, `hdl/wire/KL_gptp_rx_parser.sv`:
- `:645` the change itself: `if (rx_err_i) bad_r <= 1'b1;` inside `if (rx_valid_i)`, below the
  sof arm (`:640-644` comment). Non-blocking last-wins, so a flag on the first byte outlasts the
  sof arm's `bad_r <= 1'b0`. Every other `bad_r` assignment in the frame sets 1, so nothing clears it
  mid-frame. The existing `!rx_err_i` term in `fin_ok_r` (`:625`) stays: it is the eof byte's own read,
  because `bad_r` settles on the same edge.
- `:109` port comment: `abort: drop silently` -> `abort, with any byte: drop the frame`.
- `:32` DROP-arm list: `rx_err_i.` -> `rx_err_i (below).`
- `:52-62` new header paragraph stating the contract: sampled with every valid byte, sof and eof
  included; one counted drop and no event however many bytes carry it; pulse or hold refuse alike;
  a flag with `rx_valid_i` low is ignored; no bank write follows the flagged byte, and words written
  before it stay in the write bank like those of any refused frame.
- `:620-621` eof-gate comment names the eof byte's own `rx_err_i` read.

Tests:
- `tb/verilator/parser/sim_main.cpp:256-273` `feed_err(bytes, from, to)`: flag on bytes [from, to],
  counts bank writes after the first flagged byte's edge (`bank_writes` counter `:179-182`, `:205-208`).
- `:1210-1307` `check_rx_err_on_any_byte_drops_the_frame()`, run last (`:1334`), so the
  existing `drop count advanced` total (drops0 + 44) is untouched. 30 checks: per type (sync,
  fu, pdreq, pdresp) `rx_err at every byte: one drop | no event | no later write` (aggregated over
  all positions; a miss prints its byte), `rx_err held from byte 20 to eof: one drop | no event`,
  `control after the errors: event | no drop`; plus `rx_err in every gap between bytes: sync event | no drop`.
- `tb/verilator/parser/mutants.py` (new): seven mutants plus the clean control; every check a mutant
  names must appear in a FAIL line (stricter than a red tally).
- `tb/verilator/parser/Makefile:14-28`: `all: run mutants` is the default goal, so `make tb` runs the arm.
- `feed_gap` already drives `rx_err_i = 0` explicitly at base (`sim_main.cpp:244` at head, PR #34);
  acceptance item 4 was met before this lane and is unchanged.

Docs (every edit is about the parser's rx_err_i contract or its tests):
- `docs/INTEGRATION.md:47` row -> `Refuses the frame from any byte`; `:60-66` any byte, one drop,
  pulse and hold alike, between-byte flags ignored (replaces "Assert receive errors with the final byte.");
  `:70` "#35 records this any-byte contract".
- `docs/SOURCE_EVIDENCE.md:12` new anchorless row `Any-byte receive refusal`; `:13` and `:33`
  anchors moved #L374 -> #L386 and #L456 -> #L468 (header lines shifted them); `:42` #35 moved from
  "Open issues" to "Closed work" (the "Open issues" sentence had no other entry and is removed).
- `README.md` "Known risks" and `docs/MANAGER.md` "Open risks": the #35 bullet removed.
- `docs/TEST_DEVELOPER.md:35` entry `make -C tb/verilator/parser mutants`; `:94-95` parser-suite bullets.
- `docs/HDL_DEVELOPER.md:29` "A receive error on any byte refuses its frame."
- `tb/verilator/parser/README.md:16-18` the mutation arm.
- `scripts/` untouched: the new SOURCE_EVIDENCE row has no line anchor, so the checker's EXPECTED table
  needs no entry.

## Per-position drop table (every message type)

Scratch probe = the head bench with one printf per position, built against base RTL and head RTL.
"writes after" = bank writes after the flagged byte's own edge (later bytes plus the deferred
finalize). Full per-byte data: `evidence/mutation/per-position.tsv` (284 rows).

Sync (58 bytes)

| flagged byte | base drops | base events | base writes after | head drops | head events | head writes after |
|---|---|---|---|---|---|---|
| 0-28 | +0 | 1 | 6 | +1 | 0 | 0 |
| 29-40 | +0 | 1 | 5 | +1 | 0 | 0 |
| 41-42 | +0 | 1 | 4 | +1 | 0 | 0 |
| 43-46 | +0 | 1 | 3 | +1 | 0 | 0 |
| 47-52 | +0 | 1 | 2 | +1 | 0 | 0 |
| 53-56 | +0 | 1 | 1 | +1 | 0 | 0 |
| 57 (eof) | +1 | 0 | 0 | +1 | 0 | 0 |

Follow_Up (90 bytes)

| flagged byte | base drops | base events | base writes after | head drops | head events | head writes after |
|---|---|---|---|---|---|---|
| 0-28 | +0 | 1 | 7 | +1 | 0 | 0 |
| 29-40 | +0 | 1 | 6 | +1 | 0 | 0 |
| 41-42 | +0 | 1 | 5 | +1 | 0 | 0 |
| 43-46 | +0 | 1 | 4 | +1 | 0 | 0 |
| 47-52 | +0 | 1 | 3 | +1 | 0 | 0 |
| 53-56 | +0 | 1 | 2 | +1 | 0 | 0 |
| 57-72 | +0 | 1 | 1 | +1 | 0 | 0 |
| 73-88 | +0 | 1 | 0 | +1 | 0 | 0 |
| 89 (eof) | +1 | 0 | 0 | +1 | 0 | 0 |

Pdelay_Req (68 bytes)

| flagged byte | base drops | base events | base writes after | head drops | head events | head writes after |
|---|---|---|---|---|---|---|
| 0-28 | +0 | 1 | 4 | +1 | 0 | 0 |
| 29-40 | +0 | 1 | 3 | +1 | 0 | 0 |
| 41-42 | +0 | 1 | 2 | +1 | 0 | 0 |
| 43-46 | +0 | 1 | 1 | +1 | 0 | 0 |
| 47-66 | +0 | 1 | 0 | +1 | 0 | 0 |
| 67 (eof) | +1 | 0 | 0 | +1 | 0 | 0 |

Pdelay_Resp (68 bytes)

| flagged byte | base drops | base events | base writes after | head drops | head events | head writes after |
|---|---|---|---|---|---|---|
| 0-28 | +0 | 1 | 8 | +1 | 0 | 0 |
| 29-40 | +0 | 1 | 7 | +1 | 0 | 0 |
| 41-42 | +0 | 1 | 6 | +1 | 0 | 0 |
| 43-46 | +0 | 1 | 5 | +1 | 0 | 0 |
| 47-52 | +0 | 1 | 4 | +1 | 0 | 0 |
| 53-56 | +0 | 1 | 3 | +1 | 0 | 0 |
| 57-64 | +0 | 1 | 2 | +1 | 0 | 0 |
| 65-66 | +0 | 1 | 1 | +1 | 0 | 0 |
| 67 (eof) | +1 | 0 | 0 | +1 | 0 | 0 |

Held from byte 20 through eof: base +1 drop / 0 events, head +1 / 0, all four types.
The base rows reproduce the issue's measurement (Sync byte 20 and 40: +0 / 1; byte 57: +1 / 0).
A first-byte flag at head leaves no bank write at all for the frame.
Error-free controls after the sweeps dispatch with no drop, codes 1, 2, 4, 5.
A frame with a flagged idle cycle in every gap dispatches (code 1), no drop.

## Planted control and its failing words

The planted control deletes the one latch line (`:645`), restoring exactly the end-of-frame-only
read the base shipped. It is mutant 1 of the committed arm and was also built by hand
(`evidence/scripts/planted_control.sh`, log `evidence/mutation/planted-control.log`):
`298 checks: 286 PASS, 12 FAIL`, failing words:

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

(got = positions refused cleanly: only the eof byte; exp = frame length.)

Every new check has a mutant that fails it by name (committed arm, `make -C tb/verilator/parser mutants`):

| mutant | edit | named checks that must FAIL |
|---|---|---|
| rx_err read only at eof (the planted control) | latch deleted | 12: every-byte one drop / no event / no later write, x4 |
| a first-byte flag lost to the sof clear | latch moved above the sof arm | 4: every-byte one drop |
| the eof byte's own flag ignored | `!rx_err_i` removed from `fin_ok_r` | 8: every-byte one drop / no event |
| every flagged byte counts a drop | latch also increments `drop_cnt_r` | 4: held 20..eof one drop |
| rx_err ignored on every byte | latch deleted and `fin_ok_r` term removed | 4: held 20..eof no event |
| the refusal outlives its frame | sof arm's `bad_r <= 1'b0` deleted | 8: control after the errors event / no drop |
| rx_err sampled between bytes | latch moved outside `if (rx_valid_i)` | 2: gap event / no drop |

Result at head: `8 checks: 8 PASS, 0 FAIL` (clean control plus seven caught). The arm itself is
not vacuous: with the base RTL in place it reports `8 checks: 2 PASS, 6 FAIL` (control fails, five
patterns stale), and with one named check renamed in the bench it reports `7 PASS, 1 FAIL`
(`missed its named check(s): rx_err in every gap between bytes: sync event`). Logs in
`evidence/mutation/`.

## Parent netlist / ROM identity at base and head

Scratch parent: clone at dev `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5` under the lane's scratch
directory, submodules `third_party/verilog-axis`, `protocol-processor` (`2ad2f845`) and
`gptp-processor` initialised. Base = dev's own gitlink `5dce647a`. Head = gitlink set to `5b4ce397`
in the index only (fetched from the lane into the scratch submodule); never committed or pushed.
Tools: Yosys 0.66 (CI pin), sv2v v0.0.13 (CI pins v0.0.12; the staged inputs below are compared
like for like on one host).

The tie-off: `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:666` (at `ac2c5e77`; the issue's `:447`
predates later parent edits) drives `.rx_err_i (1'b0)`; in the staged input the engine forwards it
only to the parser.

| measure | base `5dce647a` | head `5b4ce397` |
|---|---|---|
| parent gate `syn/yosys/run.sh --mode elaborate --no-structural --top KL_gptp_shadow` | PASS, cells=3567 | PASS, cells=3568 |
| per-module elaborated cells (hierarchical) | parser 529, all others as listed | parser 530 (+1 `$mux`), all other modules identical |
| staged sv2v input, module by module | 9 modules | 8 byte-identical; only `KL_gptp_rx_parser` differs; text outside modules identical |
| same program + `flatten; opt; opt_clean` (tie-off propagated) | 2432 cells | 2432 cells, `stat` byte-identical (every cell type) |
| equivalence of the staged parser module, `rx_err_i` tied 0 | | 748/748 `$equiv` proven (`equiv_make; equiv_simple -seq 2; equiv_induct -seq 2; equiv_status -assert` rc 0) |
| control: same, `rx_err_i` free | | 747/748, unproven `u.bad_r` only, rc 1 |
| `gptp_ucode.hex` sha256 | `c496ed8a...0371` (= rom_digests.tsv row for `5dce647a`) | identical |
| `ucode.hex` / `ltn_rom.hex` sha256 | `518b900c...` / `23cc67ee...` (= rows for PP pin `2ad2f845`) | identical |
| ROM bundle digest (`result_cache.py rom-digest`) | `018e9be9527f8c41ed605c2c4c5e2c8e134f2d84375758c81a022cbfb7646fd2` | identical |
| parent ROM-digest check `syn/yosys/ooc.sh tcam` (ledger keyed by pin) | rc 0 | rc 2 before the pin is recorded (`no recorded content digest ... pin 5b4ce397`, the parent's normal pin-bump refusal) |
| parent pin-bump record `syn/yosys/ooc.sh --record-rom-digests` (scratch only, reverted) | | rc 0; adds exactly one row, `5b4ce397 gptp_ucode.hex c496ed8a...0371`, the same digest as the `5dce647a` row; no protocol-processor row moves |
| `syn/yosys/ooc.sh tcam` after that record | | rc 0 |

Point for the reviewers: the parent's verbatim gate is hierarchical (`proc; opt_clean`, no flatten),
so it elaborates the parser module on its own with `rx_err_i` as a free input. In that view the one new
line is one `$mux`, and the rollup moves 3567 -> 3568. No implementation of the ruling can avoid that,
because the ruling adds behaviour to the parser module itself. With the tie-off propagated, the netlist
is unchanged: identical flattened `stat`, every other module's input byte-identical, and the one
differing module proven equivalent under the tie. The RTLIL bytes are not a usable instrument: even
after stripping `src` and enumerating private names they differ in ordering, so they are not claimed.
Evidence: `evidence/parent/` (incl. `romcheck/`), `evidence/equiv/`. The scratch ledger was restored
with `git checkout`, and the scratch parent is left with the gitlink at the head in its index only.

## Donor gate table

All runs: pinned Verilator 5.050 first on PATH, `make -j16 tb`, never piped, logs in `evidence/gates-*`.

| gate | base `5dce647a` | head `5b4ce397` |
|---|---|---|
| `make tb` | rc 0: ucpu 768; parser 268; engine 1613 x3 (shipping, request seed, Sync seed) + mutants 34/34; gaskets 81 + mutants 5/5; tsngen 288 + mutants 4/4; bench tag PASS | rc 0: ucpu 768; parser **298** + **parser mutants 8/8**; engine 1613 x3 + mutants 34/34; gaskets 81 + mutants 5/5; tsngen 288 + mutants 4/4; bench tag PASS |
| `make contract` | rc 0 | rc 0 |
| `make lint` | rc 0 | rc 0 |
| `make docs` | rc 0 (20 exact anchors) | rc 0 (20 exact anchors) |

## Acceptance (issue #35)

1. Contract in the port documentation and the module header; code matches: met (`:109`, `:32`, `:52-62`, `:645`).
2. A pulse at any byte refuses the frame with exactly one drop, no event and no bank write, tested at
   the first byte, mid-frame and the eof byte: met at EVERY byte of four types. "No bank write" is read
   as none after the flagged byte; a first-byte flag leaves none at all. Words written before a later
   flag cannot be retracted without buffering. They stay in the write bank, which no event names, as for
   every other refusal arm the header documents.
3. A planted mutation restoring mid-frame acceptance goes red: met, permanently in `make tb`.
   "README counts updated": no current README carries a parser count. Commit `46ba3eb` (docs rework)
   moved them to `docs/history/v1/testing/PARSER_TEST_RECORD.md`, a dated historical page left as
   is. The parser README now describes the arm.
4. `feed_gap` drives `rx_err_i` explicitly: met at base (PR #34), unchanged.

## Notes

- Error-free behaviour is unchanged: formal equivalence with `rx_err_i` tied low; all pre-existing
  parser checks pass unchanged (268 at step 1); engine and tsngen drive `rx_err_i = 0`.
- The bench gasket raises its error only with the last byte (`bench/arty/bench_mii_rx.sv:158`,
  `b_err_o <= !crc_ok_w` at eof), so the bench path behaves as before.
- Process note: a WIP RTL edit overlapped the first base `make tb` for about 20 s, while engine mutants
  could have staged the RTL. That run was killed and discarded, build outputs removed, and base
  `make tb` rerun from a clean tree with no edits until it finished. All later work was staged in
  scratch until the base run completed.
- Scratch (not in the tree, not in this directory): `$VALIDATION_STORAGE/g35-a599/` (parent clone,
  probes, equivalence work, logs).
- Not done, by rule: no push, no PR, no parent commit or adoption, no hardware.
