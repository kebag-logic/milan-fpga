# #929 round 1 handoff ([A792])

Lane: `929-base-gates`, base dev-soft-core `70f4056f`. TAKEN posted (issuecomment-6929138088); REVIEW READY
posted (issuecomment-6932714309). PR body in `PR-BODY.md`; receipts in `receipts/` (index `receipts/INDEX.md`).
Head: `37255683` (5 commits on the base, not pushed; the manager pushes and opens the PR).

| Commit | What |
|---|---|
| `08ba6efa` | (a) the twin: `split-talker-failed` deleted, two plants' words restated, `talker-failed-back` added |
| `6b8e5042` | (b) `dynmap-mutants` makes each leg's generated inputs before its clean control |
| `becca95f` | (c) `srp_mbx.cpp`'s two startup tests hold every source of the compiled entity; 8x8 arms; three 8x8 plants |
| `a9a48546` | docs: the SRP README's 8x8 arms, milan_dp README's input step |
| `37255683` | `twin_compare.py:86` re-wrapped within 120 columns (docs-gates-0's Python idiom gate failed on it at `a9a48546`) |

Scratch clones (all clean clones from the lane's object store, submodules at the commit's pins):
`c-base`, `c-dyn`, `c-fw`, `c-rel-base`, `c-led-base` (base), `c-932` (#932's head `09a948d4`), `c-dynfix*`, `c-dynp1`,
`c-dynp2`, `c-rel-head` (`becca95f`), `c-F-*` (`a9a48546`), `c-G-*`, `c-rel-G`, `c-led-G` (the final head `37255683`).
Every workflow job ran on its own fresh clone (`run_wf.py`).

## Status

- [x] (a) twin: reproduced, cause, fix, plants; twin and twin-plants pass at `37255683`
- [x] (b) dynmap-mutants: reproduced on a fresh clone, cause confirmed, fix, plants; controls pass at `37255683`
- [x] (c) srp_mbx.cpp 8x8: reproduced, cause, fix, plants; `firmware-unit` at `37255683`
- [x] release image byte-identical at `37255683` (bios.bin, disassembly, debug-stripped ELF at both configs)
- [x] split images identical at `37255683` (plat_ledger PASS; every point's ELF, stripped and loadable)
- [x] every gate at `37255683` green: 88 replayed steps rc 0, 56 not run with a reason, 0 bad (gate table)
- [x] REVIEW READY posted once on #929 (issuecomment-6932714309), text in `comments/REVIEW-READY.md`

## Reproduction at 70f4056f (clean clones)

**(a) the twin.** `make -C tb/verilator/milan_dp -j16 twin` exits 2 (make's `Error 1` at `Makefile:949`):

```
[DIFF] owed row split-talker-failed does not hold: the fabric sent [MSRP Talker Advertise stream_id 0200000000010000: New x2, JoinMt x15, Lv x1, Mt x5] (the row: Talker Advertise for STREAM_OUTPUT 0's stream from the PROBE_TX until it withdraws), the split [MSRP Talker Advertise stream_id 0200000000010000: New x2, JoinMt x19, Lv x1] (the row: Talker Failed for both sources' streams from boot, never withdrawn)
twin: 1 finding(s); counts {... 'MSRP': 99 ... 'MSRP': 95 ...}
```

**(b) dynmap-mutants** (`make -C tb/verilator/milan_dp -j16 dynmap-mutants DYNMAP_MUTANT_JOBS=8`, a clone that never
built `milan_dp_render`):

```
[PASS] the unmutated gateware still passes the dynmap leg
[FAIL] the unmutated gateware does NOT pass the listener leg (caught) - its mutant results are meaningless
[PASS] the unmutated gateware still passes the talker leg
[PASS] the unmutated gateware still passes the maprec8 leg
[PASS] the unmutated gateware still passes the maprec4 leg
```

Stopped by me after 18 mutants caught, none surviving (the campaign's own verdict makes them meaningless). The
listener suite then held no `ltn_rom.hex`, `ucode.hex` or `tdm8r_aemi.bin`, and `capture_coherence` no `ltn_rom.hex`
or `ucode.hex` (its control passed without them).

**(c) `srp_mbx.cpp` at the 8x8 entity** (`srp_arms.arm_srp`, the arms' own recipe, `tools/srp8x8.py`): 1x1 if1 and
if2 74 of 74; 8x8 if1 fails `Srp.StartupDeclaresTalkersDomainAndVlan`; 8x8 if2 fails it and
`Srp.OneLoopOwnsTheGlobalCentisecondDispatch`:

```
srp_mbx.cpp:294: Failure  d.time_ms Which is: 0 / 10u*19u*count Which is: 190
srp_mbx.cpp:298: Failure  Value of: std::equal(d.value.begin(),d.value.begin()+8,identity(i,index).begin())  Actual: false
srp_mbx.cpp:293: Failure  Expected: (count) < (3u), actual: 3 vs 3
srp_mbx.cpp:704: Failure  Value of: srp_mbx_init(&second,&config)  Actual: false
```

## Causes

**(a)** The row owed the split's "Talker Failed for both sources' streams from boot, never withdrawn", caused by "no
SRP adapter entry takes MAAP's allocation", owed to "the SRP adapter entry that takes MAAP's allocation (#665)".
#895 landed that entry (`432c1e87`, `srp_mbx_allocation`, an ancestor of the base, whose plat README change removed
the "Not yet done" item the row cites) and declares a source only while its SRP parameters are valid. At the base the
split declares no Talker Failed in the twin's stimulus; it declares Talker Advertise for STREAM_OUTPUT 0's stream
from 5190 ms (the fabric 5200) until its Leave at 20190 ms (the fabric 20000). The owed difference has gone. The
counts the row printed differ only by each half's own timers (the split's LeaveAll at 14560 ms and its 190 ms join
grid; the fabric's LeaveAll at 10200 ms and Mt x5 from 21000 ms), which `twin_mrp` grades legal in both halves.

**#932 (#925) does not change this.** The twin at #932's head `09a948d4` exits 2 with the same finding, and its two
captures are byte-identical to the base's (`fabric.json` `fa6a5a12…`, `split.json` `7cc8a5d2…` at both). The twin's
split half receives no MSRPDU, and #932 changes how received Talker registrations decide the Listener. With the row
deleted, #932's captures grade 0 findings.

**(b)** `dynmap_mutants.py` builds a leg through its suite's recipe with `-o` for each generated input "its build
may not remake"; `make dynmap-mutants` makes only milan_dp's own legs first. On a fresh clone no other suite has made
its inputs, so `-o` leaves them absent and the clean listener leg runs with no ROM, microcode or entity image.

**(c)** Both tests were written for the 1x1 entity (2 sources, 2 sinks); the 8x8 entity compiles 9 and 9
(`srp_entity.py`). `StartupDeclaresTalkersDomainAndVlan` counted every Talker Failed as source 1's, so the 8x8
entity's eight unallocated sources fail its count, time and StreamID checks. The firmware does what its rule says
(`srp_mbx.c:252-305`: Advertise when allocated and admitted, else Failed, code 2 when unallocated, IEEE 802.1Q-2018
35.2.2.8.7, Table 35-6). `OneLoopOwnsTheGlobalCentisecondDispatch` gave two adapters one pool of 50 blocks of 512 B
sized for the 1x1 entity; at 8x8 with two interfaces the second `srp_mbx_init` is refused for memory before the test
reaches its subject. Test defects; no firmware change.

## Changes (file:line, reason)

(a) `08ba6efa`
- `tb/verilator/milan_dp/twin_compare.py`: the `split-talker-failed` Row, `FABRIC_TALKER`, `SPLIT_TALKERS` and the
  now unused `shown_msrp` deleted; its owed difference has gone (above), and the twin's rule is that the lane that
  fixed it deletes the row (#895's did not). The Talker attributes are now compared like every other MSRP attribute
  (`compare_declarations`, the Table 10-3 grade).
- `twin_compare.py:456-460`: `SRP_ADAPTER`/`SRP_ROUND` restated as `SRP_NOTICE`/`SRP_NOTICE_OWED` for the remaining
  `stream-output-0-notices` row: its old cause is false since #895 (the split's Talker declares and withdraws; it
  sends no GET_STREAM_INFO notice at either change). Its values and predicates are unchanged; the owing step is not
  named (see open questions).
- `twin_compare.py:70` `srp-plus-k` words: `MSRP Talker Failed stream_id 0200000000010001` ->
  `MSRP Talker Advertise stream_id 0200000000010001` (the plant bumps the first Talker vector's StreamID; the
  split's first Talker vector is now an Advertise). Refused by the split's Table 10-3 grade of the phantom attribute.
- `twin_compare.py:84-87` `leave-all-declaration` words: the same finding with the Talker's first boundary now in it
  (`{Talker Advertise ...; Domain ...} x1`), the plant's `{none} x3` kept.
- `twin_plants.py:231-263` new `talker-failed-back`: every Talker Advertise vector of the split re-encoded in place
  as a Talker Failed of the same StreamID and events (FailureInformation: the split's MAC, code 2), so the row's old
  behaviour is planted and must be refused. `Makefile` `TWIN_CAPTURE_PLANTS` adds it.
- `README.md`: the owed-row table, the row's deletion and why, the plants table (21 plants), "What it finds".

(b) `6b8e5042`
- `tb/verilator/milan_dp/dynmap_mutants.py:461-472` `prepare()`: makes each selected leg's LEGS inputs through its suite's own
  rules (`make -s -C <suite> <inputs>`), and returns why not when make fails or an input is still absent.
- `dynmap_mutants.py:644-649` `main()`: before each leg's clean control, a leg whose inputs are not made is a `[FAIL] the <leg> leg's inputs are
  not made: ...` and its control is not run. Docstring updated.

(c) `becca95f`
- `sw/firmware/ctrl/test/srp_mbx.cpp:281-329` `StartupDeclaresTalkersDomainAndVlan`: per interface, the Domain's
  three declarations; exactly three Talker declarations per source (`3u*CTRL_SRP_SOURCES`); each source by its own
  StreamID, type Advertise if allocated else Failed, New/New/JoinMt at 0/190/380 ms, VID 2, size 224, interval 1,
  priority 0x60, Failed's code 2. At 1x1 this is the old test (source 0 Advertise, source 1 Failed).
- `srp_mbx.cpp:712-730` `OneLoopOwnsTheGlobalCentisecondDispatch`: the shared pool is two of the shape's SRP pools
  (`srp_pool_classes` with counts doubled, `2u*SRP_POOL_ARENA_BYTES` static storage).
- `srp_arms.py:98-101` `mbx_entity_arms()`, `test_ctrl_firmware.py:196`: `srp_mbx.cpp` at the 8x8 entity at both interface
  counts in the suites phase (firmware-unit), the clean control of the plants below. Not added to `coverage()`.
- `srp_mutants.py:310-321`: three Defects with `entity='endstation_ax7101_8x8'` (the two-interface campaign).

## New / kept checks (plant, failing words)

| Plant | Where | Caught by | Run |
|---|---|---|---|
| `talker-failed-back` (new) | twin, capture plant | `MSRP declarations at the LeaveAll boundaries differ: the fabric's [{Talker Advertise stream_id 0200000000010000; Domain value 06030002} x1, {Domain value 06030002} x5], the split's [{Talker Failed stream_id 0200000000010000; Domain value 06030002} x1` | REFUSED both ways (base captures, dev) |
| `srp-plus-k` (kept, words restated) | twin, split run plant | `MSRP Talker Advertise stream_id 0200000000010001` | REFUSED both ways |
| `leave-all-declaration` (kept, words restated) | twin | the same finding with `{none} x3` | REFUSED both ways |
| prepare's make skipped (P1, one-off plant) | dynmap_mutants.py, fresh clone `becca95f` | `[FAIL] the listener leg's inputs are not made: its suite did not make ltn_rom.hex, ucode.hex, tdm8r_aemi.bin (make rc 0: ) - its mutant results are meaningless` | rc 1 |
| prepare call removed (P2, one-off plant) | same | `[FAIL] the unmutated gateware does NOT pass the listener leg (caught) - its mutant results are meaningless` | rc 1 |
| `startup-8x8-sources-past-two-undeclared` (new) | srp-mutants if2, 8x8 | `each source's three Talker declarations and no other` | ok; ESCAPED at 1x1 (inert there) |
| `startup-8x8-failure-code-past-two` (new) | srp-mutants if2, 8x8 | `source 2's failure code` | ok; ESCAPED at 1x1 (inert there) |
| `duplicate-tick-owner-8x8` (new) | srp-mutants if2, 8x8 | `srp_mbx_attach` | ok |
| `startup-vid`, `duplicate-tick-owner`, `transmit-first-link-up-owes-nothing` (kept) | srp-mutants if2, 1x1 | `d.value`, `srp_mbx_attach`, `adapter.transmitted` | ok |

## Images

- Release (all-fabric) firmware image, base `70f4056f` vs the head `37255683` (also `becca95f` and `a9a48546`):
  `bios.bin` identical at both configs (`860d4771…` 1x1, `d8851b6d…` 8x8), its disassembly identical, the
  debug-stripped ELF identical (`8cebfd66…`, `733c9938…`). Section by section, every loadable section of the ELFs is
  identical; only `.debug_line`, `.debug_line_str`, `.debug_info`, `.debug_str`, `.debug_macro` differ (the clone
  path). `receipts/images/`.
- Split images: none changes. `plat_ledger.py` PASS at all four points at base and head, with the base's figures
  (1x1/1if 117,488 B rom, 43 RAMB36; 1x1/2if 119,072, 44; 8x8/1if 130,200, 56; 8x8/2if 131,752, 60.5), and every
  point's `ctrl_app.elf`, debug-stripped ELF and loadable binary, and the split SoC's mapped and stand-in images, are
  byte-identical at base and head.
- milan_dp's make database (`make -pn`) differs between base and head only in `TWIN_CAPTURE_PLANTS`; `make -n all`
  and `ci-list` are identical, so the sweep's milan_dp suite runs the same recipes. No sweep suite invokes
  `twin_compare.py`, `twin_plants.py` or `dynmap_mutants.py`. The native sweep was not run.

## Gate table

All on clean clones (workflow jobs: each on its own fresh clone through `run_wf.py`, step by step).

| Gate | Command | Head | rc | Receipt |
|---|---|---|---|---|
| twin (reproduction) | `make -C tb/verilator/milan_dp -j16 twin` | 70f4056f | 2: `owed row split-talker-failed does not hold` | `twin/base-70f4056f-twin.txt` |
| twin at #932's head | same | 09a948d4 | 2, the same finding; both captures byte-identical to the base's | `twin/at-932-09a948d4-twin.txt`, `twin/captures-base-and-932.sha256` |
| twin | same | **37255683** | **0**, 0 findings | `twin/head-37255683-twin.txt` |
| twin-plants | `make ... twin-plants` | **37255683** | **0**, 42 REFUSED (21 plants x 2), 0 ESCAPED | `twin/head-37255683-twin-plants.txt` |
| dynmap-mutants (reproduction) | `make ... dynmap-mutants DYNMAP_MUTANT_JOBS=8`, fresh clone | 70f4056f | listener control `[FAIL]`; stopped at 18 caught, 0 survived | `dynmap/base-70f4056f-dynmap-mutants.txt` |
| dynmap-mutants | same, fresh clone | **37255683** | **0**, `71 checks: 71 PASS, 0 FAIL` (5 controls, 66 of 66 mutants) | `dynmap/head-37255683-dynmap-mutants.txt` |
| dynmap direct | `python3 dynmap_mutants.py 36`, fresh clone (no make prerequisites) | becca95f | 0, `2 checks: 2 PASS` | `dynmap/becca95f-dynfix2-36.log` |
| dynmap plants P1, P2 | same, planted (`*.plant.diff`) | becca95f | 1, 1: each caught by its words | `dynmap/becca95f-dynp1-36.log`, `-dynp2-36.log` |
| srp_mbx.cpp both entities (reproduction) | `tools/srp8x8.py` (`srp_arms.arm_srp`) | 70f4056f | 1: 8x8/1if 1 test, 8x8/2if 2 tests | `srp/base-70f4056f-*` |
| srp_mbx.cpp both entities | same | a9a48546 | 0, 74 of 74 x 4 | `srp/a9a48546-srp_mbx-both-entities.log` |
| SRP plants (dev) | `tools/srpplants.py` if2 / if1 | becca95f | if2 6 of 6 ok; if1 the two 8x8 plants ESCAPE (inert at 1x1) | `srp/becca95f-plants-*.log` |
| rtl-fast `changes`, `firmware-unit`, `firmware-srp-mutants`, `firmware-control-mutants`, `firmware-aecp-mutants`, `firmware-verilator`, `split-cdc` | `run_wf.py` | **37255683** | every step rc 0 or not run with a reason | `workflows/verify-37255683.md`, `workflows/logs/` |
| rtl-fast `firmware-boundary` | `run_wf.py`, `WF_VENV` the LiteX venv (the hosted job installs `sw/litex/litex_pins.txt`) | **37255683** | every step rc 0 (`failed 0`) | same |
| docs, all six jobs | `run_wf.py` | **37255683** | every step rc 0 or not run with a reason | same |
| release image | `tools/release_image.sh` | 70f4056f, 37255683 | 0, 0; identical | `images/release-*` |
| split images | `tools/ledger.sh` (`plat_ledger.py`) | 70f4056f, 37255683 | 0, 0; identical | `images/split-ledger-*` |

Within the replays: `test_ctrl_firmware: PASS` with `[ok] arm srp-srp_mbx-if1/if2-endstation_ax7101_1x1_tdm8` and
`..._8x8`; `firmware coverage: PASS (39 files)`; the SRP campaign 424 `[ok]`, 0 escaped (the base's inventory 421:
419 plants and 2 pin arms; the head 3 more).

Replay notes: `firmware-boundary` first ran with the gates venv, which has no `migen`, and refused at
`sw/litex/test_ctrl_memory.py` (`ModuleNotFoundError: No module named 'migen'`), at `a9a48546` and `37255683` alike;
those logs are kept in `receipts/workflows/logs-gates-venv/`. Other lanes' replays run this job with the LiteX venv.
`docs-check-no-git` removes `.git` by design, so the replay's post-run `git status` raised after its three steps
(all rc 0) and wrote no DONE marker. At `a9a48546` `docs-gates-0`'s Python idiom gate failed on one 121-column line
(`twin_compare.py:86`), fixed in `37255683`.

## Open risks / questions

- `stream-output-0-notices` still holds by its values; its cause is restated to what is true since #895, and its
  owing step is not named. No issue found for split GET_STREAM_INFO notices of a STREAM_OUTPUT on its Talker
  declaration change (Milan v1.2 5.4.5.2, Table 5.22). Needs an issue.
- The twin compares Talker declarations by type and StreamID only. The halves' TSpecs differ: MaxFrameSize 73 (fabric)
  vs 217 (split; Milan v1.2 4.3.3.2 Table 4.4 at 8 channels). The twin elaborates both datapaths at
  `TALKER_WIRE_CHANS_P` 2 (shipping AX: 8), and the fabric's source 0 declares its `LWSRP_TSPEC` word; which sets 73
  is not diagnosed. The deleted row pinned each half's value on its own; it never compared them. Needs an issue.
- `tb/verilator/milan_dp/README.md` srptx section ("At this base every split source declares Talker Failed ...", the
  licence scenario's fixture) predates #895; not changed here (srptx is not this issue's).
