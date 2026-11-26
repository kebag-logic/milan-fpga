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

The full service-budget run at both points, every group: 113 groups graded at each, no refusal, with `--record-budget-findings` as
the harness's README prescribes for `backlog-owed`: its seven rows are the scenario's 60 ms egress hold and miss at every
point (61.6 to 63.2 ms at 1x1/1if, within 0.05 ms of the base's; at 8x8/1if 63.0 to 64.8 ms, every one under its
`egress_ledger.py` figure, no new miss). Every other row is within its budget, the notices and ACMP's among them. No work
pass is over the 2.0 ms share at 1x1/1if, and one at 8x8/1if, `srp-bound`'s registrations, owed to #977 as on the base.
#920's groups stay within their 5 s: `save-burst` 1,097.4 ms (1x1/1if) and 1,354.0 ms (8x8/1if), `save-flight`
147.1 ms and 651.0 ms. The long-window load (`load_grade.py --check`): 0.512 at 1x1/1if (ceiling 0.70) and 0.744 at
8x8/1if (0.76). The longest pass that carries the store's step is 1.158 ms, its step 0.793 ms, within the step's
1.0 ms.

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

KLJ3 stays minor 0: the 8x8/1if image of each boots the journal the other's wrote, with the binding and the entity's
name, and each tree's reference codec decodes both journals alike.

## Tests

- `sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32`: PASS, five shapes, 128 tests each (76 checks, 52 on both
  ports); `--self-test`: PASS, all 170 planted defects caught (165 defects, 16 of them the window's, and five compile-time controls);
- coverage: `fw_coverage.py --check` PASS; `nvm_store.c` 513 of 513 lines and 317 of 326 branches, 100 % after its nine stated arcs;
- `tb/verilator/ctrl_service_budget/selftest.py`: PASS, 1,048 checks, all 321 mutants caught (26 of them the bind groups' and the verify's byte coverage);
- `tb/verilator/nvm_split_target/run.py`: PASS at 1x1 and 8x8, every case and every control; the commit's erase comes 128.4 ms and 206.9 ms
  after its changes, at the binding records' window, not the rename's 1,000 ms; `--self-test` PASS (79 checks);
- `sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32`, `plat_ledger.py`, `test_ctrl_memory.py`, the documentation
  checks: PASS.

## Before it lands (the board items of the acceptance)

Prepared, not run; the bench waits for the go:

- on-board response to durable for BIND_RX, STOP_STREAMING, START_STREAMING and UNBIND_RX at 8x8/1if and 1x1/1if, each
  change's reading bracketed by the console's samples and its width reported (see the resolution note);
- the power-cycle cases with the cut about 1 s after the response: per cut, the store idle at the bind and the saved
  state read as durable before the power is lost, at least 250 ms before the DUT's last frame;
- the boot comparison: the boot's flash reads at the head identical to the base's, for a blank journal and journals
  written by each image.

**Resolution note.** The console answers `milan_status` in about 300 bytes at 115,200 baud and runs a command only when
its transmit ring has room for the longest answer, so back-to-back readings are about 26 ms apart. The prepared reader
asks in pairs whose two samples are about 9.5 ms apart and reports each change's bracket; a reading is 10 ms or better
only where the durable edge falls inside a pair, so the run repeats each change three times. A finer reading on every
change needs a decision (a shorter read-only console query is a firmware change outside this step).
