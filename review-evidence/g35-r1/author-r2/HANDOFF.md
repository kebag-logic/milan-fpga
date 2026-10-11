# [A599] HANDOFF: lane for #35 (a mid-frame rx_err_i drops the frame)

Status: ROUND 2 REVIEW READY at head `a70e38804cb16435c089d024c58e8c3fb4d39ff6` (PR #80; three new
commits on `5b4ce397`, local, not pushed; all four donor gates rc 0). See "Round 2" at the end.

Round 1 status (kept as written): REVIEW READY at head `5b4ce3974f7627d57b31167bde50cde8f4bdcdf3` (all four donor gates rc 0 at head).
Every section before "Round 2" describes round 1; its file:line references are at `5b4ce397`.

- Repository: Mister-M-alt/FPGA-gPTP, branch `g35-rx-err`, base main `5dce647a`
  (`5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`), remote confirmed
  `https://github.com/Mister-M-alt/FPGA-gPTP.git`.
- Head: `5b4ce3974f7627d57b31167bde50cde8f4bdcdf3` (four commits, local only; not pushed, no PR).
- Assignment: issue #35 comment 6104916029 ([A10]); ruling "the safer default": latch on any byte.
- TAKEN: issue #35 comment 6104922026.
- REVIEW READY: issue #35 comment 6105359326, at head `5b4ce397`, flagging the hierarchical-netlist point for a ruling
  (ruled accepted, 6105366046). The branch was later pushed as PR #80 by the manager.
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

## Round 2

Status: REVIEW READY at head `a70e38804cb16435c089d024c58e8c3fb4d39ff6`; all four donor gates rc 0.
Posted: issue #35 comment 6106250782 (REVIEW READY, round 2). TAKEN was not posted again.

- Assignment and scope ruling: issue #35 comment 6105869522 ([A10]). Reviews answered: PR #80
  comments 6105577480 (R616-1, POSITIVE, one RESIDUE) and 6105855128 (R617-1, NEGATIVE on R617-F1).
- Start: `5b4ce3974f7627d57b31167bde50cde8f4bdcdf3` (PR #80's head, confirmed with `git rev-parse`).
  Three new commits on it, no rebase, no amend, nothing pushed.
- Ruled contract (the ruling's words): one drop and no event for a refused frame; no bank write after
  the flagged byte; the bank words a refused frame wrote are undefined and never referenced by an event;
  the next accepted frame's event reads only that frame's data. Acceptance item 2 is amended by the ruling.

### Round 2 commits (one-line subjects, no body, no trailers)

| commit | subject | gate before commit |
|---|---|---|
| `3acd2f5` | Count every bank write before, on and after the flagged byte in the parser suite | parser 313/313, arm 8/8 |
| `c5c6646` | Prove no word a refused frame leaves reaches the next accepted frame's event | parser 337/337, arm 9/9 |
| `a70e388` | State the ruled rx_err_i bank contract in the parser header, port and integration guide | docs rc 0, lint rc 0, arm 9/9 |

### Round 2 changes (file:line at `a70e388`)

Required item 1, the oracle counts every write (`tb/verilator/parser/sim_main.cpp`):
- `:189-195` counters `writes_before_err`, `writes_on_err`, `writes_after_err`.
- `:267-292` `feed_err` now splits every write of the feed at the first flagged byte: edges of earlier
  bytes (before), its own edge (on), later bytes plus the deferred end-of-frame (after). The old oracle
  took its baseline after the flagged byte's tick, which is what R617-F1 pointed at.
- `:1266-1289` `rx_err_arms()`: the four swept frames, shared by both rx_err checks (refactor, same frames).
- `:1405-1441` `check_rx_err_writes_before_on_and_after_the_flag()`: first byte, byte 29 (its edge
  completes `w1`, so "on" is exercised) and the eof byte, for Sync, Follow_Up, Pdelay_Req, Pdelay_Resp
  and an Announce. Asserts per type, aggregated over the three positions: one drop, no event, no write
  after. Prints one `INFO` line per position with drops, events, before, on and after (the record).
  The Announce is added because its deferred hop-count word `w12` is the only write in the parser that
  lands after an eof, so it is the only type in which the eof leg of "no write after" can fail. In the
  four ruled types no word completes after the eof, so their eof leg is zero by construction.

Required item 2, no stale data reaches a consumer (`sim_main.cpp`):
- `:185-188`, `:228` the bank as each event sees it (`ev_bank`), and as the refused frame left it.
- `:294-315` `feed_refused_then`: a frame flagged on its eof byte (so it leaves every word it writes),
  then a clean frame with no idle cycle, the bank kept across both. The engine moves to its other bank
  only on an accepted event (`bank_sel_r`, `hdl/top/KL_gptp_engine.sv:313-314`), so in the engine the two
  frames share one bank as they do here.
- `:1291-1335` `salted()`: each frame's fields drawn from its own salt, with the words its event names
  packed from those fields alone (independent of the RTL), so no word of the refused frame or of any
  earlier frame equals the clean frame's.
- `:1443-1502` `check_a_refused_frame_leaves_no_stale_word()`: pairs {clean, refused} = Sync/Sync,
  Sync/Pdelay_Resp, Follow_Up/Follow_Up, Follow_Up/Pdelay_Resp, Pdelay_Req/Pdelay_Req, Pdelay_Req/Sync,
  Pdelay_Resp/Pdelay_Resp, Pdelay_Resp/Follow_Up (the different type is the one whose words cover most
  of the clean type's). 24 checks: per pair `one drop`, `event` (code and sequence, exactly one event)
  and `every word is this frame's` (every word the clean type names, as its event saw the bank). A miss
  prints the word and whether it is the refused frame's.
- `:1530-1531` run order: the stale-word check runs before the oracle, so its first refused frame follows
  an accepted one (under the planted defect every pair then shows the refused frame's own word).
- `tb/verilator/parser/mutants.py:121-135` the planted defect: a `was_bad_r` register latched at sof gates
  the clean frame's `w2` (sourcePortIdentity.clockIdentity) write. `:57-80` `ORACLE_TYPES`, `PAIRS` and
  the named-check helpers; `:26-28` docstring. `tb/verilator/parser/Makefile:22` "Eight defects".

Required item 3, docs:
- `hdl/wire/KL_gptp_rx_parser.sv:52-66` module header: the existing contract plus R616-1-RES1's exact
  sentence (`:60-63`) and "Their contents are undefined: the next accepted frame writes every word its
  event names before raising it, so that event reads only that frame's data (FPGA-gPTP #35, the bank
  ruling)" (`:63-66`).
- `:113-116` port documentation, now a `//!` block above the port (the engine's multi-line style): one
  counted drop, no event, no bank write after that byte's own edge, words up to and including it
  undefined and named by no event.
- `docs/INTEGRATION.md:62-82`: refused frame raises no event; no bank write after the flagged byte's own
  edge; words up to that edge are undefined; no event references them; the next accepted event reads only
  its own frame; a link to the ruling comment (`:82`).
- `docs/SOURCE_EVIDENCE.md:13,33` anchors `#L386 -> #L393`, `#L468 -> #L475` (header and port grew by 7
  lines); `make docs` reports them EXACT.
- `docs/TEST_DEVELOPER.md:95-96`, `tb/verilator/parser/README.md:16` the two new test behaviours.
- PR body item 2 cites the ruling (PR-BODY.md, Round 2).
- The RTL diff since round 1 is comments only: with comments stripped, `a70e388` and `5b4ce397` are
  identical, and the parent's staged sv2v input is byte-identical between them (below).

Required item 4, R616-1-RES1: its exact header sentence is at `:60-63`; the PR body takes "after the
flagged byte's own edge" and "up to and including a later flagged byte" (PR-BODY.md, opening and item 2).

### First / middle / eof oracle record (head `a70e388`, from the suite's INFO lines)

| type (bytes) | flagged byte | drops | events | writes before | on | after |
|---|---|---|---|---|---|---|
| Sync (58) | 0 | +1 | 0 | 0 | 0 | 0 |
| Sync | 29 | +1 | 0 | 0 | 1 | 0 |
| Sync | 57 eof | +1 | 0 | 5 | 1 | 0 |
| Follow_Up (90) | 0 | +1 | 0 | 0 | 0 | 0 |
| Follow_Up | 29 | +1 | 0 | 0 | 1 | 0 |
| Follow_Up | 89 eof | +1 | 0 | 7 | 0 | 0 |
| Pdelay_Req (68) | 0 | +1 | 0 | 0 | 0 | 0 |
| Pdelay_Req | 29 | +1 | 0 | 0 | 1 | 0 |
| Pdelay_Req | 67 eof | +1 | 0 | 4 | 0 | 0 |
| Pdelay_Resp (68) | 0 | +1 | 0 | 0 | 0 | 0 |
| Pdelay_Resp | 29 | +1 | 0 | 0 | 1 | 0 |
| Pdelay_Resp | 67 eof | +1 | 0 | 7 | 1 | 0 |
| Announce, no PathTrace (78) | 0 | +1 | 0 | 0 | 0 | 0 |
| Announce | 29 | +1 | 0 | 0 | 1 | 0 |
| Announce | 77 eof | +1 | 0 | 6 | 1 | 0 |

The rows R617-1 measured independently (Sync 0/29/40/57, Follow_Up, Pdelay_Req and Pdelay_Resp eof)
match exactly.

### Per-position drop table, every message type (round 2: before / on / after)

Scratch probe = the head bench with one TSV row per flagged byte (`evidence/r2/scripts/make_probe.py`),
built against base `5dce647a` RTL and head `a70e388` RTL. Cell = drops / events / writes before-on-after.
Raw rows: `evidence/r2/position/per-position-{base,head}.tsv` (362 rows each). At head every one of the
362 positions is +1 / 0 / x-y-0, and before and on equal base's at every position: the repair removes
only the writes after the flag.
Sync (58 bytes)

| flagged byte | base drops / events / writes before-on-after | head drops / events / writes before-on-after |
|---|---|---|
| 0-28 | +0 / 1 / 0-0-6 | +1 / 0 / 0-0-0 |
| 29 | +0 / 1 / 0-1-5 | +1 / 0 / 0-1-0 |
| 30-40 | +0 / 1 / 1-0-5 | +1 / 0 / 1-0-0 |
| 41 | +0 / 1 / 1-1-4 | +1 / 0 / 1-1-0 |
| 42 | +0 / 1 / 2-0-4 | +1 / 0 / 2-0-0 |
| 43 | +0 / 1 / 2-1-3 | +1 / 0 / 2-1-0 |
| 44-46 | +0 / 1 / 3-0-3 | +1 / 0 / 3-0-0 |
| 47 | +0 / 1 / 3-1-2 | +1 / 0 / 3-1-0 |
| 48-52 | +0 / 1 / 4-0-2 | +1 / 0 / 4-0-0 |
| 53 | +0 / 1 / 4-1-1 | +1 / 0 / 4-1-0 |
| 54-56 | +0 / 1 / 5-0-1 | +1 / 0 / 5-0-0 |
| 57 (eof) | +1 / 0 / 5-1-0 | +1 / 0 / 5-1-0 |

Follow_Up (90 bytes)

| flagged byte | base drops / events / writes before-on-after | head drops / events / writes before-on-after |
|---|---|---|
| 0-28 | +0 / 1 / 0-0-7 | +1 / 0 / 0-0-0 |
| 29 | +0 / 1 / 0-1-6 | +1 / 0 / 0-1-0 |
| 30-40 | +0 / 1 / 1-0-6 | +1 / 0 / 1-0-0 |
| 41 | +0 / 1 / 1-1-5 | +1 / 0 / 1-1-0 |
| 42 | +0 / 1 / 2-0-5 | +1 / 0 / 2-0-0 |
| 43 | +0 / 1 / 2-1-4 | +1 / 0 / 2-1-0 |
| 44-46 | +0 / 1 / 3-0-4 | +1 / 0 / 3-0-0 |
| 47 | +0 / 1 / 3-1-3 | +1 / 0 / 3-1-0 |
| 48-52 | +0 / 1 / 4-0-3 | +1 / 0 / 4-0-0 |
| 53 | +0 / 1 / 4-1-2 | +1 / 0 / 4-1-0 |
| 54-56 | +0 / 1 / 5-0-2 | +1 / 0 / 5-0-0 |
| 57 | +0 / 1 / 5-1-1 | +1 / 0 / 5-1-0 |
| 58-72 | +0 / 1 / 6-0-1 | +1 / 0 / 6-0-0 |
| 73 | +0 / 1 / 6-1-0 | +1 / 0 / 6-1-0 |
| 74-88 | +0 / 1 / 7-0-0 | +1 / 0 / 7-0-0 |
| 89 (eof) | +1 / 0 / 7-0-0 | +1 / 0 / 7-0-0 |

Pdelay_Req (68 bytes)

| flagged byte | base drops / events / writes before-on-after | head drops / events / writes before-on-after |
|---|---|---|
| 0-28 | +0 / 1 / 0-0-4 | +1 / 0 / 0-0-0 |
| 29 | +0 / 1 / 0-1-3 | +1 / 0 / 0-1-0 |
| 30-40 | +0 / 1 / 1-0-3 | +1 / 0 / 1-0-0 |
| 41 | +0 / 1 / 1-1-2 | +1 / 0 / 1-1-0 |
| 42 | +0 / 1 / 2-0-2 | +1 / 0 / 2-0-0 |
| 43 | +0 / 1 / 2-1-1 | +1 / 0 / 2-1-0 |
| 44-46 | +0 / 1 / 3-0-1 | +1 / 0 / 3-0-0 |
| 47 | +0 / 1 / 3-1-0 | +1 / 0 / 3-1-0 |
| 48-66 | +0 / 1 / 4-0-0 | +1 / 0 / 4-0-0 |
| 67 (eof) | +1 / 0 / 4-0-0 | +1 / 0 / 4-0-0 |

Pdelay_Resp (68 bytes)

| flagged byte | base drops / events / writes before-on-after | head drops / events / writes before-on-after |
|---|---|---|
| 0-28 | +0 / 1 / 0-0-8 | +1 / 0 / 0-0-0 |
| 29 | +0 / 1 / 0-1-7 | +1 / 0 / 0-1-0 |
| 30-40 | +0 / 1 / 1-0-7 | +1 / 0 / 1-0-0 |
| 41 | +0 / 1 / 1-1-6 | +1 / 0 / 1-1-0 |
| 42 | +0 / 1 / 2-0-6 | +1 / 0 / 2-0-0 |
| 43 | +0 / 1 / 2-1-5 | +1 / 0 / 2-1-0 |
| 44-46 | +0 / 1 / 3-0-5 | +1 / 0 / 3-0-0 |
| 47 | +0 / 1 / 3-1-4 | +1 / 0 / 3-1-0 |
| 48-52 | +0 / 1 / 4-0-4 | +1 / 0 / 4-0-0 |
| 53 | +0 / 1 / 4-1-3 | +1 / 0 / 4-1-0 |
| 54-56 | +0 / 1 / 5-0-3 | +1 / 0 / 5-0-0 |
| 57 | +0 / 1 / 5-1-2 | +1 / 0 / 5-1-0 |
| 58-64 | +0 / 1 / 6-0-2 | +1 / 0 / 6-0-0 |
| 65 | +0 / 1 / 6-1-1 | +1 / 0 / 6-1-0 |
| 66 | +0 / 1 / 7-0-1 | +1 / 0 / 7-0-0 |
| 67 (eof) | +1 / 0 / 7-1-0 | +1 / 0 / 7-1-0 |

Announce (no PathTrace) (78 bytes)

| flagged byte | base drops / events / writes before-on-after | head drops / events / writes before-on-after |
|---|---|---|
| 0-28 | +0 / 1 / 0-0-8 | +1 / 0 / 0-0-0 |
| 29 | +0 / 1 / 0-1-7 | +1 / 0 / 0-1-0 |
| 30-40 | +0 / 1 / 1-0-7 | +1 / 0 / 1-0-0 |
| 41 | +0 / 1 / 1-1-6 | +1 / 0 / 1-1-0 |
| 42 | +0 / 1 / 2-0-6 | +1 / 0 / 2-0-0 |
| 43 | +0 / 1 / 2-1-5 | +1 / 0 / 2-1-0 |
| 44-46 | +0 / 1 / 3-0-5 | +1 / 0 / 3-0-0 |
| 47 | +0 / 1 / 3-1-4 | +1 / 0 / 3-1-0 |
| 48-65 | +0 / 1 / 4-0-4 | +1 / 0 / 4-0-0 |
| 66 | +0 / 1 / 4-1-3 | +1 / 0 / 4-1-0 |
| 67-73 | +0 / 1 / 5-0-3 | +1 / 0 / 5-0-0 |
| 74 | +0 / 1 / 5-1-2 | +1 / 0 / 5-1-0 |
| 75-76 | +0 / 1 / 6-0-2 | +1 / 0 / 6-0-0 |
| 77 (eof) | +1 / 0 / 6-1-0 | +1 / 0 / 6-1-0 |

### Stale-word check result (head)

All 24 checks pass. Record (`INFO` lines): the refused frame left every word it writes in each pair
(Sync 6/6, Follow_Up 7/7, Pdelay_Req 4/4, Pdelay_Resp 8/8). Words left outside the clean type's
layout: Sync after Pdelay_Resp 2 (`w6`, `w7`), Follow_Up after Pdelay_Resp 2, Pdelay_Req after Sync 2
(`w4`, `w5`), Pdelay_Resp after Follow_Up 1 (`w11`); those are the undefined words the ruling allows,
named by no event of the clean type. Every word the clean type names held the clean frame's field.

### Planted controls and failing words (round 2)

The planted control (latch deleted, mutant 1, by hand at `a70e388`, `evidence/r2/mutation/planted-*`):
`337 checks: 310 PASS, 27 FAIL`. The 12 round-1 lines are unchanged; the 15 new ones:

```
FAIL sync rx_err at first, middle, eof: one drop got 0000000000000001 exp 0000000000000003
FAIL sync rx_err at first, middle, eof: no event got 0000000000000001 exp 0000000000000003
FAIL sync rx_err at first, middle, eof: no write after got 0000000000000001 exp 0000000000000003
FAIL fu rx_err at first, middle, eof: one drop got 0000000000000001 exp 0000000000000003
FAIL fu rx_err at first, middle, eof: no event got 0000000000000001 exp 0000000000000003
FAIL fu rx_err at first, middle, eof: no write after got 0000000000000001 exp 0000000000000003
FAIL pdreq rx_err at first, middle, eof: one drop got 0000000000000001 exp 0000000000000003
FAIL pdreq rx_err at first, middle, eof: no event got 0000000000000001 exp 0000000000000003
FAIL pdreq rx_err at first, middle, eof: no write after got 0000000000000001 exp 0000000000000003
FAIL pdresp rx_err at first, middle, eof: one drop got 0000000000000001 exp 0000000000000003
FAIL pdresp rx_err at first, middle, eof: no event got 0000000000000001 exp 0000000000000003
FAIL pdresp rx_err at first, middle, eof: no write after got 0000000000000001 exp 0000000000000003
FAIL ann rx_err at first, middle, eof: one drop got 0000000000000001 exp 0000000000000003
FAIL ann rx_err at first, middle, eof: no event got 0000000000000001 exp 0000000000000003
FAIL ann rx_err at first, middle, eof: no write after got 0000000000000001 exp 0000000000000003
```

(got = positions of the three refused cleanly: only the eof.) The stale-word checks pass under it, as
they must: their refused frame is flagged on its eof byte, which the eof term still refuses.

The ruling's planted defect ("a refusal skips the next frame's w2 write", by hand at `a70e388`,
`evidence/r2/mutation/stale-mutant.diff` and `stale-mutant-suite.log`): `337 checks: 327 PASS, 10 FAIL`.

```
  sync after a refused sync: w2 holds aabbccfffe000101, not aabbccfffe000202, the refused frame's word
FAIL sync after a refused sync: every word is this frame's got 0000000000000005 exp 0000000000000006
  sync after a refused pdresp: w2 holds aabbccfffe000303, not aabbccfffe000404, the refused frame's word
FAIL sync after a refused pdresp: every word is this frame's got 0000000000000005 exp 0000000000000006
  fu after a refused fu: w2 holds aabbccfffe000505, not aabbccfffe000606, the refused frame's word
FAIL fu after a refused fu: every word is this frame's got 0000000000000006 exp 0000000000000007
  fu after a refused pdresp: w2 holds aabbccfffe000707, not aabbccfffe000808, the refused frame's word
FAIL fu after a refused pdresp: every word is this frame's got 0000000000000006 exp 0000000000000007
  pdreq after a refused pdreq: w2 holds aabbccfffe000909, not aabbccfffe000a0a, the refused frame's word
FAIL pdreq after a refused pdreq: every word is this frame's got 0000000000000003 exp 0000000000000004
  pdreq after a refused sync: w2 holds aabbccfffe000b0b, not aabbccfffe000c0c, the refused frame's word
FAIL pdreq after a refused sync: every word is this frame's got 0000000000000003 exp 0000000000000004
  pdresp after a refused pdresp: w2 holds aabbccfffe000d0d, not aabbccfffe000e0e, the refused frame's word
FAIL pdresp after a refused pdresp: every word is this frame's got 0000000000000007 exp 0000000000000008
  pdresp after a refused fu: w2 holds aabbccfffe000f0f, not aabbccfffe001010, the refused frame's word
FAIL pdresp after a refused fu: every word is this frame's got 0000000000000007 exp 0000000000000008
```

The other two FAIL lines are pre-existing checks of a Pdelay_Req that follows a refused frame
(`pdreq w2 srcid`, `complete pdreq after the arms: w2 srcid`). The first draft ran the stale check after
the oracle; then the first pair's refused frame itself followed a refused Announce, lost its own `w2` to
the same defect, and the leaked word was an older one (still a FAIL by name). The committed order shows
the refused frame's own word in every pair.

The eof-term mutant by hand (`evidence/r2/mutation/eofterm-suite.log`) shows the eof leg of the oracle
is load-bearing where a post-eof write exists: `INFO ann rx_err at byte 77 of 78: drops +0, events 1,
writes before 6, on 1, after 1` and `FAIL ann rx_err at first, middle, eof: no write after`. It also
fails all 16 stale-word `one drop` / `event` checks (the eof-flagged frame dispatches), beyond those it names.

Every new check has a mutant that fails it by name (committed arm, `make -C tb/verilator/parser mutants`):

| mutant | new round-2 checks it names |
|---|---|
| rx_err read only at eof (the planted control) | oracle one drop / no event / no write after, five types (15) |
| a first-byte flag lost to the sof clear | oracle one drop, five types (5) |
| the eof byte's own flag ignored | oracle one drop / no event, five types; ann oracle no write after (11) |
| the refusal outlives its frame | stale-word one drop / event, eight pairs (16) |
| a refusal skips the next frame's w2 write (new) | stale-word every word is this frame's, eight pairs (8) |

Arm at head: `9 checks: 9 PASS, 0 FAIL` (clean control plus eight caught), named-check totals 27, 9,
19, 4, 4, 24, 2 and 8.

### Parent netlist / ROM identity, round 2

Same scratch parent (dev `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`), same tools. Gitlink set in the
index only, never committed or pushed: base `5dce647a`, then head `a70e388`; left at head.
Evidence: `evidence/r2/parent/`.

| measure | base `5dce647a` | head `a70e388` |
|---|---|---|
| `syn/yosys/run.sh --mode elaborate --no-structural --top KL_gptp_shadow` | PASS, cells=3567 | PASS, cells=3568 (the ruled +1 `$mux`) |
| staged sv2v input, module by module | 9 modules | 8 byte-identical; only `KL_gptp_rx_parser` differs; outside text identical |
| staged sv2v input against round 1's head `5b4ce397` | | byte-identical (sv2v drops comments; the RTL change is comments only) |
| hierarchical `stat` | | identical to round 1's head |
| same program + `flatten; opt; opt_clean` | 2432 cells | 2432 cells, `stat` byte-identical to base |
| tied equivalence of the staged parser module | | the same bytes round 1 proved 748/748 under the tie |
| `gptp_ucode.hex` / `ucode.hex` / `ltn_rom.hex` sha256 | `c496ed8a...0371` / `518b900c...` / `23cc67ee...` | identical |
| ROM bundle digest | `018e9be9527f8c41ed605c2c4c5e2c8e134f2d84375758c81a022cbfb7646fd2` | identical |
| `syn/yosys/ooc.sh tcam` (ledger keyed by pin) | rc 0 | rc 2 before the pin is recorded (`no recorded content digest ... pin a70e3880...`) |
| `syn/yosys/ooc.sh --record-rom-digests` (scratch, reverted) | rc 0, adds no row | rc 0, adds one row: `a70e3880... gptp_ucode.hex c496ed8a...0371`, the base pin's digest |
| `syn/yosys/ooc.sh tcam` after that record | rc 0 | rc 0 |

### Donor gate table, round 2

All runs: pinned Verilator 5.050 first on PATH, `make -j16 tb`, never piped, from a clean tree with
no edits during the run. Logs in `evidence/r2/gates-head/`. Base column is round 1's (unchanged base).

| gate | base `5dce647a` | head `a70e388` |
|---|---|---|
| `make tb` | rc 0: ucpu 768; parser 268; engine 1613 x3 + mutants 34/34; gaskets 81 + 5/5; tsngen 288 + 4/4; bench tag PASS | rc 0: ucpu 768; parser **337** + parser mutants **9/9**; engine 1613 x3 + mutants 34/34; gaskets 81 + 5/5; tsngen 288 + 4/4; bench tag PASS |
| `make contract` | rc 0 | rc 0 |
| `make lint` | rc 0 | rc 0 |
| `make docs` | rc 0 (20 exact anchors) | rc 0 (20 exact anchors, incl. `#L393`, `#L475`) |

Arm non-vacuity at round 2 (scratch copies of the tree, `evidence/r2/mutation/meta-*.log`): with the
base RTL in place the arm reports `9 checks: 2 PASS, 7 FAIL` (clean control fails; five patterns
stale; the w2 mutant misses because base never latches a refusal into `bad_r`, so the leak it plants
has nothing to carry); with one stale-word check renamed in the bench, `8 PASS, 1 FAIL` (`missed its
named check(s): sync after a refused sync: every word is this frame's`, and the other seven).

### Findings answered

- R617-F1 (MAJOR): resolved by the ruling. The oracle counts every write, before, on and after, at
  first / middle / eof of the four types (plus Announce), and asserts zero after; the stale-word check
  covers the real risk the ruling names, with its planted defect failing by name; header, port doc and
  integration guide state the ruled contract; PR body item 2 cites the ruling.
- R616-1-RES1 (RESIDUE): applied verbatim (header `:60-63`, PR body).
- R616-1-S1 (SUGGESTION, anchor the any-byte row): not taken. It needs a `scripts/` checker edit, outside
  this lane's scope; the row stays anchorless as before.
- R616-1-S2 (SUGGESTION, broader types): partly taken. The oracle adds an Announce, for the reason above.
  Pdelay_Resp_Follow_Up, Signaling, padded frames, runts and zero-gap neighbours stay in the reviewers' probes.

### Acceptance (issue #35, item 2 as amended by the ruling)

1. Contract in port documentation and module header, code matches: met (`:52-66`, `:113-116`, `:652`, `:632`).
2. As amended: one drop and no event at any byte, including first, mid and eof, at every byte of four types;
   no bank write after the flagged byte's own edge, by the oracle that counts every write; words up to
   and including that edge recorded and undefined; the next accepted frame's event reads only its own
   data (stale-word check, same and different type, planted defect red by name): met.
3. Planted mutation restoring mid-frame acceptance goes red, permanently in `make tb`: met (27 named FAILs).
4. `feed_gap` drives `rx_err_i` explicitly: met at base, unchanged.

### Limits and notes (round 2)

- Parser-level evidence. No engine bench drives `rx_err_i` (engine and tsngen tie it low) and engine
  files are out of scope; the stale-word check models the engine bank by keeping one bank across the
  two frames, which is what `bank_sel_r` does for a refused frame. The engine's Announce context is
  engine-owned and not exercised here; the stale-word check covers the four ruled types.
- The issue body's checkbox text is the manager's to amend; this lane cannot edit issues.
- Error-free behaviour unchanged: the RTL code is identical to round 1's (comments only), whose base
  equivalence under the tie is 748/748; the 268 base parser checks still pass inside the 337.
- Process: no edit to the tree while `make tb` ran; all round-2 probes and mutants built in scratch
  (`$VALIDATION_STORAGE/g35-a599/r2/`); one `py_compile` cache file written into the tree was removed at once.
- Not done, by rule: no push, no PR edit, no parent commit, no hardware.
