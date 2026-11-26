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

The full service-budget run at both points, every group of the default run, run again from a clean checkout of this branch's head
(`079c4fa15`, no status entry before or after), its record, table, exit status and source identity (commit, tree,
submodules, command, the firmware's and the testbench's sha256) published with the review packet: 113 groups at each
point, no refusal, exit 0, with `--record-budget-findings` as the harness's README prescribes for `backlog-owed`. Its
seven rows are the scenario's 60 ms egress hold and miss at every point: 61.6 to 63.2 ms at 1x1/1if, within 0.05 ms of
the base's same group; 63.0 to 64.8 ms at 8x8/1if, every one under its `egress_ledger.py` figure, no new miss. Every
other row is within its 20 ms budget: the worst ACMP row 4.8 ms at 1x1/1if and 8.3 ms at 8x8/1if, the worst
notification 3.2 ms and 3.3 ms, the worst SRP row 9.2 ms and 11.5 ms. No work pass is over the 2.0 ms share at
1x1/1if, and one at 8x8/1if, `srp-bound`'s registrations, owed to #977 as on the base. #920's groups stay within their
5 s: `save-burst` 1,097.4 ms (1x1/1if) and 1,354.0 ms (8x8/1if), `save-flight` 147.1 ms and 651.0 ms. Every figure
equals round 1's run to the microsecond, and its verdict lines are identical to round 1's. The long-window load
(`load_grade.py --check`): 0.512 at 1x1/1if (ceiling 0.70) and 0.744 at 8x8/1if (the flip check's 0.75; ruling 3's
0.76). The longest pass that carries
the store's step is 1.158 ms, its step 0.793 ms, within the step's 1.0 ms.

The default run holds no notice row: the notice groups run only in the harness's notice arms. Each arm ran at both
points from the same clean checkout of `079c4fa15` (no status entry before or after), its record, table, exit status
and identity published with the review packet; every one exits 0 with no refusal and no notice miss:

| Arm (`run.py --variant`) | Rows | 1x1/1if, worst | 8x8/1if, worst | Bound |
|---|---|---:|---:|---:|
| `answering-later`: the retried notice, a BIND_RX of input 0 during a SET_NAME's save (8 phases) | `notice.retried` | 8.184 ms | 8.157 ms | 20 ms |
| `answering-every-port`: every notice the model holds pending at once and every port answering at the same attempt, 8 phases without and 8 with the composed burst 6 ms after the answer (16 groups) | `notice.queued`, the queue's last | 20.707 ms (192 rows) | 27.647 ms (640 rows) | 140 ms (`CTRL_LOOP_QUEUED_MS` 130, the harness's row bound) |
| the same | the queue's first | 6.847 ms | 2.633 ms | 20 ms |
| `talker-notices`: a declared and a withdrawn Talker (8 phases) | `notice.declared` / `notice.withdrawn` | 5.343 / 5.219 ms | 11.958 / 10.447 ms | 20 ms |

Each `answering-later` group also carries its timer-driven MRPDU under its load, as the harness requires.

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
synthesized netlists whose only differing input is the ROM contents (after synthesis 9 instances differ at 8x8/1if,
the largest `KL_mbx` +40 and `KL_mbx_cdc` -25, and 2 at 1x1/1if, in the CPU's hierarchy, +19). No HDL, SoC or gateware file changes.

KLJ3 stays minor 0: the 8x8/1if image of each boots the journal the other's wrote, with the binding and the entity's
name, and each tree's reference codec decodes both journals alike.

## Tests

Each from a clean checkout of `079c4fa15`, its log naming the commit, the tree and no status entry:

- `sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32`: PASS, 656 tests: five shapes, 128 each (76 checks, 52 on
  both ports), and 16 more: the recorded vectors (2 at 1x1, 2 at 8x8), a build whose record walk and sizes disagree (1), a
  shape with no name record (1), layout 3's NAME capacity (6), the LiteSPI port with its command master and timer
  mocked (3) and the erased prefixes under the address sanitizer (1); `--self-test`: PASS, all 170 planted defects caught (165 defects, 16 of them the window's, and five compile-time controls);
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

The power-cycle cases with the cut held 1.0 s after the bind: 47 cuts ran, 38 at 8x8/1if and 9 at 1x1/1if, and 44
are graded, 36 and 8: one per bind. At every one of the 44 (the outlet off 1.47 to 1.67 s after the response) the
store was idle at the bind, its own save under way at the first sample and no sample showing the bind behind another
save, and the saved state was read as durable before the power went off and at least 1.27 s before the DUT's last
frame on the wire (the rule: 250 ms). The other three are retry attempts, which power-cycle again with no new bind, so
the test takes no hold reading at them (it reads in the hold after a bind):

| Cut | Scenario | Stream input | Bind since the previous cut | Off after the last bind | That bind read durable |
|---|---|---:|---|---:|---:|
| 8x8/1if, 29 of 38 | a Talker Failed declared at the DUT's first ENTITY_AVAILABLE after power-on, attempt 2 | 0 | no | 23.13 s | 0.579 s, before cut 28 |
| 8x8/1if, 30 of 38 | the same, attempt 3 | 0 | no | 44.84 s | the same |
| 1x1/1if, 5 of 9 | a Talker Failed declared 10 s after power-on, attempt 2 (it passed) | 1 | no | 21.45 s | 0.327 s, before cut 4 |

No cut followed a bind without a durable reading. Each cut's line, with the bind before it from the test's report, is
published with the review packet.

Three of the four scenarios passed at 8x8/1if and all four at 1x1/1if. The fourth at 8x8/1if (a Talker Failed
declared at the DUT's first ENTITY_AVAILABLE after power-on) passed on stream inputs 1 to 8 and was inconclusive on
input 0. The board does not go down when the test's power-off command returns. Over the 36 graded cuts at 8x8/1if
the DUT's last frame came 0.39 to 0.62 s after the relay's power-off instant, and the command returned 0.38 to
0.60 s after that instant. At each of the three attempts on input 0 the test withdrew the Talker within 1 ms of that
return. At attempts 1 and 2 the DUT, still up, answered a probe within 39 ms of the withdraw, as its last frame. At
attempt 3 the probe came from the boot that attempt 2 powered on, before that attempt's cut. Each attempt took that
probe as its settle, 20.6 to 21.6 s before its own post-power-on declaration, so none exercised the pre-settle
registration: RETRY, three times. The bind itself was durable 0.579 s after its response, 1.328 s before the DUT's
last frame. Each attempt's times, from the run's log, the relay's lines and the capture, are published with the
review packet (`board/fail-8x8-input0.txt`).

The test was corrected: after the cut it waits 1.0 s before the withdraw, and an attempt that power-cycles counts
only a probe answered after its own power-on. The cut hold (1.0 s after the bind's response), the verdicts and the
restore check are unchanged. The manager read the correction and accepted it and the rerun
([ruling](https://github.com/kebag-logic/milan-fpga/pull/1017#issuecomment-7191672753)). The test revision is frozen
as a private replica commit, `27734fa0`. Under it that case ran again on 8x8/1if, stream input 0, and passed at its
first attempt:

- **The image:** the head's, bitstream sha256 `aaf4a60a…`. Its control firmware is byte-identical to the
  firmware rebuilt at `079c4fa15`.
- **The store at the bind:** idle (first sample 0.079 s after the response); the saved state durable by 0.586 s
  (bracket 48.8 ms).
- **The cut:** the outlet off 1.551 s after the response, with the saved state durable 1.196 s before the DUT's last
  frame.
- **The restore:** the binding restored after power-on. The Talker Failed was declared 4.74 s after the test's
  power-on reference, at the DUT's first ENTITY_AVAILABLE (4.73 s). The DUT then declared Listener Asking Failed, New,
  0.2 ms after T's PROBE_TX_RESPONSE, and reported REGISTERING_FAILED 1.9 ms after it, within the 1.0 s window.

The rerun's identity (head, image, test revision, environment, start and end, rc 0) and its report as numbers are
published with the review packet (`board/si0-identity.txt`, `board/si0-report.txt`).

## Before it lands

- the boot comparison: the boot's flash reads at the head identical to the base's, for a blank journal and journals
  written by each image;
- a decision on the board reading's resolution (below).

**Resolution note.** The console answers `milan_status` in about 300 bytes at 115,200 baud and runs a command only when
its transmit ring has room for the longest answer, so back-to-back readings are about 26 ms apart. A reader that sends
its second ask without waiting for the first answer gets samples about 9.5 ms apart in pairs; a reading is then 10 ms
or better only where the durable edge falls inside a pair. That corrected reader read the input-0 case above: its pairs formed (the
second sample 9.2 to 9.4 ms after the first, pairs about 56 ms apart), and the edge fell between two pairs, so that
reading's bracket is 48.8 ms. A
10 ms reading on every change needs a shorter read-only console query, a firmware change outside this step.
