[A781] STOP

Head: `db6bc954` (`894-8x8-1if`, PR #914), round 10: seven commits on round 9's `cd7d92ad`. Nothing is pushed.
- `d9335d1f`: item 1, the restatements as round 9's patch states them.
- `51e50436` and `705f6fa4`: item 2, the fix (#930).
- `11a9b4bf`: item 4, the tsn-c-stack#32 column.
- `1d4244a6` and `db6bc954`: the restatements on the fixed image.
- `46cf2a7d`: the design note.

**Exit: STOP, on one held-egress row.** The fix reaches every cost target at both points, and every row the CPU decides holds its bound. One of the seven rows the egress decides at 8x8/1if is over its ledger figure, which only a ruling moves:

| Row (8x8/1if, `backlog-owed`) | Measured, ms | Ledger, ms | Over by, ms | Round 8, composed image |
|---|---:|---:|---:|---:|
| `backlog-owed.service.aecp.last.if0` | 62.04905 | 61.94 | 0.10905 | 61.75319 |

The other six are within, each 0.22 to 0.37 ms under its figure. By the ledger's rule at this measurement the row's figure would be 62.16 ms.

**Why it moved: phase, not cost.**
- On both images the hold releases 6,005,361 cycles after the composed window opens. On the fixed image that window opens 29,006 cycles (290 us) earlier, because the settle before it is shorter: its SRP records are cheaper.
- So the release falls 237.5 us past a millisecond, instead of 527.5 us.
- On round 8's composed image an AECP frame was already queued at the release and left at +57 us. The first pass after the release (+170 us) was AECP's, and ACMP's owed frame left after all of AECP's frames, at +1,395 us.
- On the fixed image no AECP frame is queued at the release. The first pass after it (+51.9 us, 42,336 cycles) commits ACMP's owed frame, which leaves at +107 us. AECP's frames start at +352 us.
- AECP's last service therefore moves 0.296 ms later. ACMP's last service and the five owed frames each move 0.09 to 0.16 ms earlier.
- Both traces, read from the release on, are in the packet (`aecp-last-phase.txt`).

**The targets** (the ruling, item 3):

| Target | Measured | Bound |
|---|---|---|
| 1x1/1if: SRP's record by the rule | 23,503 cycles, 250 us (27,170 and 290 before); stated 280 | 280 |
| 1x1/1if: the last queued notice by every source | 136.65 ms at the statements | 140 |
| 8x8/1if: the load at the pin | 0.735 (0.694 in the second column) | 0.75 |
| Every row within its bound at both points, `srp-talker-held` included | all but the row above | each row's |

**The fix** (item 2; the split adapter only, lwSRP and tsn-c-stack unchanged):
- **What changed.** A Listener's indication copies its declaration, as before, and no longer marks the registrar walk owed. lwSRP's transition observer copies its presence.
- **Why a Registrar change no longer marks the walk.** Each change of what the walk copies comes with an indication: every Registrar change into or out of MT does (IEEE 802.1Q-2018 Table 10-4), and lwSRP indicates a value changed while it registers. A walk now follows only a Talker's indication, a binding, one of the adapter's own declarations or a participant's creation.
- **The licence.** It was already published only when it changes, and the record publishes and declares nothing.
- **What the dearest records measure now:**
  - 8x8/1if: a Listener Ready that licenses a declared Talker, 32,936 cycles (42,663 before);
  - 1x1/1if: 23,503 (27,170).
- **The differential** (`srp_listeners.cpp`) runs at 1x1/1if and 8x8/1if, two seeds of 3,000 random steps each.
  - Its reference run restores #665's walk schedule through two seams: `srp_mbx.c` is built with lwSRP's `msrp_app_create` and `mrp_set_observer` renamed.
  - Every mailbox write, every licence call and the state the loop, ACMP and THE TRANSMIT read must be identical after every step. The frames are compared from the model.
  - Each settled step must also hold what a walk of the registrar copies.
- **Planted defects** (`srp_listener_mutants.py`): five, one at each copy and mark site, each caught by name at 1x1/1if, 8x8/1if (a new one-interface campaign at the 8x8 entity) and 8x8/2if.
- **Coverage** stays 100 %: `fw_coverage --check` passes, `srp_mbx.c` 746 of 746 lines.
- **Two existing tests restated under #930's contract:**
  - `ARecordThatChangesNoRegistrationCostsNoWalk` now holds that a Listener record walks nothing and a Talker record walks once.
  - `AcmpMailbox.F3bListenerRegistrationControlsItsOwnGate` now binds a sink while Asking Failed registers, so a walk copies the Listener again.
  - `four-way-f3b-withdrawal-stale` plants where a withdrawal is now copied, with the same test and the same words.
- **Images.** All eight link. The 8x8/1if platform image is 56.0 RAMB36, within its 56. The 1x1/1if images differ from dev-soft-core `70f4056f`'s in `srp_mbx`'s `listener` and `moved` alone, by symbol size.

**Restated by the rule on the fixed image.** The SRP unit follows `record.srp` (the drain ruling).

| Point | Cost | Stated at `d9335d1f`, us | Measured, cycles | Stated now, us |
|---|---|---:|---:|---:|
| 1x1/1if | SRP's record and the SRP unit | 290 | 23,503 | 280 |
| 1x1/1if | The retained retry (a record's apply) | 285 | 23,144 | 280 |
| 8x8/1if | SRP's record and the SRP unit | 450 (its own) | 32,936 | 365 (8x8/2if's, `NEAREST`) |
| 8x8/1if | The retained retry | 450 | 32,618 | 345 |
| 8x8/1if | The reclaim | 35 | 3,446 | 40 |

The first four come down because the fix removed the work they measured. Each is the cut's own measurement by the rule, held at the figure its point stated before `srp-talker-held` existed (280, 365, 345). None is lower than that, so none goes down to fit a bound. Every other statement holds over every leg.

**The measurement** (on `46cf2a7d`'s image; `db6bc954` changes a grader only). 29 legs, every one rc 0 with no STATED line.
- **8x8/1if:** 117 groups and 1,762 instances.
  - The rows the CPU decides: AECP 5.144 (20), ACMP 7.555, ADP 7.000, an ENTITY_AVAILABLE 4.900 and MAAP 6.275 (30), SRP 10.869 (90), MRPDU 3.109 (49).
  - AECP's notices 3.146 (20); the queued notices first 2.650 (20) and last 25.625 (130); the largest legal command 3.404 (238 ms).
  - SRP's Talker declaration rows at most 189.638 ms (220).
  - Joins 186.895 to 191.012 ms. Slices within 147,500 (SRP's 124,869; the build 122,179).
  - THE RETRY's 2,403,014 rounds: none over. The transmit-aged control is caught in 8 of 8 groups.
- **1x1/1if:** 118 groups and 1,290 instances.
  - The rows the CPU decides: AECP 4.281 (20), ACMP 4.959, ADP 4.952, an ENTITY_AVAILABLE 4.450 and MAAP 4.990 (30), SRP 11.401 (90), MRPDU 2.968 (49).
  - AECP's notices 3.470 (20); the queued notices first 7.743 (20) and last 27.279 (140); the largest legal command 3.936 (238 ms).
  - The seven held-egress rows are each about 0.19 ms under the figures 1x1/1if's earlier measurement derives; no ruled ledger covers this point.
  - Joins 187.937 to 190.147 ms. Slices within 90,000.
- **Both points:** the AECP records by class pass. The survey holds every statement, once the reclaim above is restated.

**The tsn-c-stack#32 column** (item 4). The pin `715589c1` is the merge of tsn-c-stack PR #34, which closed #32. Its `src/` and `include/` are byte-identical to `9043b926`, the donor commit the second column was measured with, and #32's head `a530eca` is in the pin. So "at the pin" already includes it, and both columns state one image's costs:
- the pin's column also holds what images built before the pin moved measured for the five costs #32's walk moves (`WALK`), since a statement never goes down;
- the donor's column holds only measurements of images carrying #32.

`load_grade.py` says so. Every ceiling is read at the pin's column, as `flip_grade.py` reads it.

**Reported, owed to #872:** 8x8/1if's rows by every source, at the restated polls: R4 21.39 ms (20), R5 136.64 (90), the last queued notice 387.95 (130), txL 159.82 (49).

**Decision needed:** the ledger figure of `backlog-owed.service.aecp.last.if0` at 8x8/1if. The ledger allows a restatement only by ruling. This measurement gives 62.16 ms by the rule, against the 61.94 kept at round 9.

**Not run, by the STOP:** the final gates. Those are the firmware units and campaigns, the docs jobs, the lane gates and verilator shards 1, 3, 4, 6, 10 and 17. Their scripts are in the packet. Already passing:
- at `705f6fa4`, `test_ctrl_firmware`'s suites (82 arms) and `fw_coverage --check`;
- at `db6bc954`, the five new planted defects and the 29 existing ones nearest the change, each caught by name at one and two interfaces, and the five new ones at 8x8/1if: 73 plantings;
- quick checks on a clean clone of `db6bc954`: 20 of 20 pass, the shape table, the flip check (612 controls) and both points, rows_tiers (1,033), the load gate (28 and `--check`), the record classes (14), R843-3's mixed-point probe, the ledger's 14 mutants, docs_check, the idiom gates, the comment scans and R844-1's audit (0 lines), and the diff checks.
