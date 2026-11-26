Give the binding class a 100 ms first-dirty window on the whole-commit save (#1009)

Relates to #1009 (step 1 of its scope ruling 3). Closes nothing until the board acceptance below is run.

Milan v1.2 5.5.3.5.3 saves the binding parameters before the BIND_RX_RESPONSE, and 5.3.8.3 counts a stream input's
started and stopped state with them. The split image's store started a 1,000 ms first-dirty window after any change, so a
binding was durable about 1.5 s after its response on the board. Binding-class changes now get a 100 ms window; every
other class keeps 1,000 ms. Each save stays a whole commit: KLJ3 minor 0, no format change, one 64 KiB erase per binding
change. Save before the response (Milan v1.2 Table 5.26 gives BIND_RX_COMMAND 200 ms) cannot be met by a whole commit and
stays open (#1012); the delta frames are step 2 (#1014).

## The change

`sw/firmware/ctrl_nvm`: the store keeps one deadline, the earliest end of the open windows, a window per class
(`NVM_BIND_DEBOUNCE_MS`, 100 ms, for the BINDING block's records: bind, unbind, started and stopped, one record a sink;
DR2a's 1,000 ms for every other record, DR2a amended for that class alone):

- a window starts at its class's first change and is not restarted; a later change brings the capture nearer, never
  later, so a binding change inside another record's window ends it 100 ms after itself, and the save captures
  everything dirty;
- a change the running capture takes joins it, as before; a binding change marked while a save is in flight opens the
  next 100 ms window, and any other change starts the next save at the first idle step, as #920 ruled.

## Measured (the CPU budget harness: the split CPU running the image's firmware, the part's busy times modelled)

`tb/verilator/ctrl_service_budget`, the bind groups with the part's erase of 120 ms and page program of 0.5 ms
(calibrated on the base image's whole save: 1,451.5 ms in the harness against the board's last-pending reading of
1.44 to 1.45 s and first-clear reading of 1.490 to 1.502 s). From each command's response to the verify of the first
save that holds its value:

| Group | 8x8/1if | 1x1/1if | Bound |
|---|---:|---:|---:|
| idle store: BIND_RX | 550.5 ms | 304.5 ms | 800 ms |
| idle store: STOP_STREAMING | 550.0 ms | 304.2 ms | 800 ms |
| idle store: START_STREAMING | 550.5 ms | 304.2 ms | 800 ms |
| idle store: UNBIND_RX | 550.4 ms | 304.5 ms | 800 ms |
| a BIND_RX during a SET_NAME's save, the worst of ten arrivals (just after its capture) | 891.2 ms | 395.0 ms | 950 / 450 ms |
| 64 binds and unbinds, 10 ms apart, each sink's last | 646.4 ms | 306.5 ms | 950 / 450 ms |
| the burst's saves (one erase each) | 2 | 4 | at most 3 / 4 |

A bind that arrives during another save is a stated bound, not the 800 ms gate: the rest of that save plus one save.
The other nine arrivals take 552.8 to 880.3 ms at 8x8/1if and 298.5 to 392.9 ms at 1x1/1if. The ten arrivals are just after the capture (the seal's first stretch), in the seal, at the erase and late in it, at the
blank check's start and late in it, at the first page and late in the program phase, at the verify's start and late in
it; each run is held to its phase and to two saves, the first of them without the bind. At a 1 s cut this case is not
safe; the frames and #1012 close it.

With an erase of 160 ms instead of 120 ms each save takes about 40 ms more, so a bind just after the capture at
8x8/1if would take about 970 ms; the board reading decides.

The store's host suite sweeps the cut on the whole path: from a binding change's response to 3 s after it, every
10 ms and inside each media effect, an erase of 150 ms modelled: every cut boots the old binding or the new one, never
neither, and the new one from 800 ms on; and for a binding change at nine phases of another record's save, the new one
from 450 ms on at the shapes of at most 16 pages (1x1, 14; the smallest Arty shape, 11) and from 950 ms at the larger ones
(8x8 and two Arty shapes).

The full service-budget run at both points, every group, run again from a clean checkout of this branch's head
(`079c4fa15`, no status entry before or after), its record, table, exit status and source identity (commit, tree,
submodules, command, the firmware's and the testbench's sha256) published with the review packet: 113 groups at each
point, no refusal, exit 0, with `--record-budget-findings` as the harness's README prescribes for `backlog-owed`. Its
seven rows are the scenario's 60 ms egress hold and miss at every point: 61.6 to 63.2 ms at 1x1/1if, within 0.05 ms of
the base's same group; 63.0 to 64.8 ms at 8x8/1if, every one under its `egress_ledger.py` figure, no new miss. Every
other row is within its 20 ms budget: the worst ACMP row 4.8 ms at 1x1/1if and 8.3 ms at 8x8/1if, the worst
notification 3.2 ms and 3.3 ms, the worst SRP row 9.2 ms and 11.5 ms. No work pass is over the 2.0 ms share at
1x1/1if, and one at 8x8/1if, `srp-bound`'s registrations, owed to #977 as on the base. #920's groups stay within their
5 s: `save-burst` 1,097.4 ms (1x1/1if) and 1,354.0 ms (8x8/1if), `save-flight` 147.1 ms and 651.0 ms. Every figure
equals round 1's run to the microsecond, and the firmware is byte-identical to it. The long-window load
(`load_grade.py --check`): 0.512 at 1x1/1if (ceiling 0.70) and 0.744 at 8x8/1if (0.76). The longest pass that carries
the store's step is 1.158 ms, its step 0.793 ms, within the step's 1.0 ms.

## Memory and fit, against `dev-soft-core` `c34e7d8b`

The platform ledger (`plat_ledger.py`): +72 B of `rom` at the 1x1 points and +64 B at the 8x8 points, no `sram`, and
the same RAMB36 at all four (45.5, 46.5, 59.5, 64.5). The size fixture's arms, each from its own plan: +64 to +72 B
of `rom`, no tile (57.0, 57.5, 57.0 with one interface; 61.5 with two). No ledger entry is raised.

Routed (one placement directive, `AltSpreadLogic_high`, chosen before the builds for head and base alike; Vivado's
four corners, WNS and WHS):

| Image | Slow WNS | Least WHS | LUTs | Registers | Block RAM tiles |
|---|---:|---:|---:|---:|---:|
| 8x8/1if, `c34e7d8b` | +0.146 ns | +0.036 ns | 45,814 | 53,381 | 98.5 |
| 8x8/1if, this change | +0.045 ns | +0.036 ns | 45,973 | 53,375 | 98.5 |
| 1x1/1if, `c34e7d8b` | +0.222 ns | +0.013 ns | 32,656 | 42,803 | 80.5 |
| 1x1/1if, this change | +0.126 ns | +0.036 ns | 32,647 | 42,803 | 80.5 |

Both images of this change meet +0.030 ns at every corner, route without errors and pass the identity gate; block RAM
is the base's at both. The base's own 1x1 image misses the floor by its fast-corner hold (+0.013 ns), and its 8x8
slow WNS is +0.146 ns against this change's +0.045 ns: one placement each, so the difference is not a trend.

**The LUT difference is placement, not design growth.** The two builds of each shape synthesize the same design: the
generated Verilog is identical apart from its date and the paths of three memory images whose contents are identical,
and the only netlist input that differs is the firmware ROM's contents, its banks' initial values. Every ROM bank of
block RAM keeps its cells (34 at 8x8/1if, 31 at 1x1/1if, base and head), and the last, partial bank of each shape is
mapped to logic, so its contents count in LUTs. After synthesis the head has 23 LUTs more at 8x8/1if (48,044 against
48,021, 0.05 %) and 19 more at 1x1/1if (34,495 against 34,476); registers are 2 fewer at 8x8/1if and the same at
1x1/1if. After
placement the difference is +159 at 8x8/1if and -9 at 1x1/1if, spread over about 45 instances at each shape, about half
up and half down, the largest 70 LUTs: the placer's physical optimization of one placement each, starting from
netlists that differ only in ROM contents. No HDL, SoC or gateware file changes.

KLJ3 stays minor 0: the 8x8/1if image of each boots the journal the other's wrote, with the binding and the entity's
name, and each tree's reference codec decodes both journals alike.

## Tests

Each from a clean checkout of `079c4fa15`, its log naming the commit, the tree and no status entry:

- `sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32`: PASS, five shapes, 128 tests each (76 checks, 52 on both
  ports); `--self-test`: PASS, all 170 planted defects caught (165 defects, 16 of them the window's, and five compile-time controls);
- coverage: `fw_coverage.py --check` PASS; `nvm_store.c` 513 of 513 lines and 317 of 326 branches, 100 % after its nine stated arcs;
- `tb/verilator/ctrl_service_budget/selftest.py`: PASS, 1,048 checks, all 321 mutants caught (26 of them the bind groups' and the verify's byte coverage);
- `tb/verilator/nvm_split_target/run.py --self-test` PASS (79 checks); the campaign, PASS at 1x1 and 8x8, every case and
  every control, ran at `85569e24` (the commit's erase 128.4 ms and 206.9 ms after its changes, at the binding records'
  window, not the rename's 1,000 ms): `079c4fa15` changes only a comment, the firmware's bytes are the same;
- `sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32`, `plat_ledger.py`, `test_ctrl_memory.py`,
  `load_grade.py --check`, the documentation checks: PASS.

## On the board

Run on both shapes, the readings off the console's `PP_STAT` (the store's dirty and pending bits), each change bracketed
by the last sample with the store busy and the first with both bits clear:

| From the response to durable | 8x8/1if | 1x1/1if | Gate |
|---|---:|---:|---:|
| BIND_RX, STOP_STREAMING, START_STREAMING, UNBIND_RX, every stream input, three passes | at most 600 ms (108) | at most 335 ms (24) | 800 ms |
| the binds of the power-cycle cases, in the hold before the cut | at most 603 ms (36) | at most 330 ms (8) | 800 ms |

No reading is over 800 ms. The brackets are 32 to 37 ms wide: the prepared reader read its first answer whole before
asking again, so its samples came about 30 ms apart and no change was bracketed within 10 ms (see the resolution note).

The power-cycle cases with the cut held 1.0 s after the bind (the outlet off 1.47 to 1.67 s after the response): at every
one of the 44 cuts (36 at 8x8/1if, 8 at 1x1/1if) the store was idle at the bind, its own save under way at the first
sample and no sample showing the bind behind another save, and the saved state was read as durable before the power
went off and at least 1.27 s before the DUT's last frame on the wire (the rule: 250 ms). Three of the four scenarios
passed at 8x8/1if and all four at 1x1/1if. The fourth at 8x8/1if (a Talker Failed declared at the DUT's first
ENTITY_AVAILABLE after power-on) passed on stream inputs 1 to 8 and was inconclusive on input 0. The board ran for up to
0.62 s after the outlet's command returned; the test withdrew the Talker in that time, and the DUT's re-probe, and then
each earlier boot's late probe, was taken as the attempt's settle, before the attempt's own declaration. That case is
prepared again with the test corrected (the withdraw waits for the board to go down, and only probes after the
attempt's own power-on count). This is a fault of the test, not of the store.

## Before it lands

- that one case, at 8x8/1if, stream input 0;
- the boot comparison: the boot's flash reads at the head identical to the base's, for a blank journal and journals
  written by each image;
- a decision on the board reading's resolution (below).

**Resolution note.** The console answers `milan_status` in about 300 bytes at 115,200 baud and runs a command only when
its transmit ring has room for the longest answer, so back-to-back readings are about 26 ms apart. A reader that sends
its second ask without waiting for the first answer gets samples about 9.5 ms apart in pairs; a reading is then 10 ms
or better only where the durable edge falls inside a pair. That corrected reader is prepared and not yet run. A
10 ms reading on every change needs a shorter read-only console query, a firmware change outside this step.
