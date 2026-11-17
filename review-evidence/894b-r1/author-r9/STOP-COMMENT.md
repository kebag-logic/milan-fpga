[A781] STOP

Head: `cd7d92ad` (`894-8x8-1if`, PR #914), round 9: three commits on round 8's `acfa5601`, namely `24753b96` (item 1), `edbd04fe` (item 3's group) and `cd7d92ad` (its README). Nothing is pushed.

**Exit: STOP, on the gate item 3 asked for.** The new group declares every Talker beside a Listener Ready, with a LeaveAll under its held load. It measures five costs over their statements at 8x8/1if and two at 1x1/1if. Restated by the rule, as the ruling directs, they break a ceiling at each point:
- **8x8/1if:** the load at the pin is 0.783, over 0.75 (`flip_grade.py --check --point 8x8/1if` FAIL). With tsn-c-stack#32 it is 0.742.
- **1x1/1if:** the last queued notice by every source is 157.09 ms, over 140 (`flip_grade.py --check --point 1x1/1if` FAIL; past the amendment's 140, the owner's).

Statements only rise by the rule, so measuring a new image again cannot lower either figure. I have not committed the restatements; the patch, with the load gate's, the flip check's and the rows' output at it, is in the packet for the ruling.

| Point | Cost | Measured, cycles | By the rule, us | Stated, us |
|---|---|---:|---:|---:|
| 8x8/1if | SRP's record (`record.srp`) | 42,663 | 450 | 365, 8x8/2if's (NEAREST) |
| 8x8/1if | An SRP record's apply (the retained retry) | 42,449 | 450 | 345 |
| 8x8/1if | The registrar walk | 11,179 | 120 | 55 |
| 8x8/1if | The polls' base | 26,255 | 280 | 250 |
| 8x8/1if | The reclaim | 3,292 | 35 | 30 |
| 1x1/1if | SRP's record | 27,170 | 290 | 280 |
| 1x1/1if | An SRP record's apply | 26,925 | 285 | 280 |

**What follows from those statements:**
- **The SRP unit changes, and with it the images.** By #894's drain ruling the SRP unit follows each point's `record.srp`: 450 us at 8x8/1if and 290 at 1x1/1if (`CTRL_LOOP_SRP_UNIT_US`, THE SHAPES). That changes both points' images, and 1x1/1if's has so far been byte-identical to dev-soft-core `70f4056f`'s.
- **8x8/1if's load rises past its ceiling.** SRP's term goes from 0.217 to 0.270, and the load is 0.783 at the pin. Over 0.75 is #872's second-hart trigger, by round 6's item 1.
- **1x1/1if's load holds, but its last queued notice does not.** The load is 0.522 and 0.519, within 0.70. SRP's record at 290 alone moves the last queued notice from 136.65 to 157.09 ms, 71 passes to 97; the other rows hold.

**Where the cost comes from:** a Listener Ready that licenses a declared Talker. Each such SRP record publishes its source's licence and updates the declarations: LICENCE reaches `0x1ff` at 8x8/1if and `0x3` at 1x1/1if. The registrar walk then visits every registered Listener, nine at 8x8/1if and two at 1x1/1if. No group reached this before item 3: since #901 the fixture's sources declare only in the valid-destinations arm, and its two earlier groups had no Listener.

**The group itself holds at its rows** (`srp-talker-held`, the valid-destinations arm):
- **At 8x8/1if:** 26 instances, 0 budget misses and 0 refusals. The worst rows are:
  - SRP's held record 10.799 ms (20);
  - MRPDU rows 3.241 ms, with a LeaveAll under the held load at 1.177 (49);
  - the Talker declarations 189.426 ms (220);
  - the Listener Ready rows 0.715 ms.

  THE TRANSMIT's build is at most 121,848 cycles against 8x8/1if's own 147,500, so the builds and the slice hold and none is restated. Joins are 186.613 to 190.173 ms.
- **At 1x1/1if:** rc 0, 0 budget misses, both sources licensed, the build at most 45,323 cycles (90,000), and joins 188.102 to 190.147 ms. No LeaveAll ran out under its held load at this MAC's phase; the ruling asked for one at 8x8/1if.
- **The full 8x8/1if gate** (round 8's legs and this group, at `edbd04fe`) holds every row within its bound and the moved ledger. Only the group's STATED lines, the costs above, fail it.

**The ruling's items:**
1. **The ledger:** done (`24753b96`). `egress_ledger.py` states both measurements and derives each figure from the larger, naming the ruling: 63.86, 64.10, 64.36, 64.61, 64.86 and 62.62 ms, and `service.aecp.last` at 61.94. The tool's own output is section 13's table, and a 14th mutant is caught. Round 8's legs pass at it.
2. **R4 by every source at 8x8/1if,** 20.96 ms against 20, is owed to #872 and reported here.
3. **The group:** added (`edbd04fe`) and measured at both points; this STOP is its outcome.
4. **The `CTRL_LOOP_TX_MS` keying** stands: the hold-off is 2,026 cs at 8x8/1if.

**Decision needed:** both consequences are past what a lane can rule.
- **8x8/1if's load over 0.75 at the pin.** That is #872's second-hart trigger. Or the ceiling could be read in the tsn-c-stack#32 column, 0.742.
- **1x1/1if's last queued notice over the 140 ms cap,** the owner's.

The restatements themselves are measured costs, and I recommend taking them as the patch states them. The firmware is unchanged by this round, so this STOP does not ask for a code fix.

**Not run, by the STOP:** the final gates. Those are the firmware units and campaigns, `fw_coverage --check`, the docs jobs, the lane gates, and verilator shards 1, 3, 4, 6, 10 and 17 of 19. Their scripts are in the packet: `mkqueueR9.sh`, `lane_gates_r9.sh` and `vshard.sh`, which runs the shard step directly. Quick checks on a clean clone of the head pass, 18 of 18:
- the shape table, and the flip check's 612 of 612 controls and both points;
- rows_tiers 1,033 of 1,033;
- the load gate, 28 of 28 and `--check`;
- record classes 14 of 14, and R843-3's probe;
- the ledger's 14 mutants;
- docs_check and the idiom gates;
- both comment scans and R844-1's audit, 0 lines;
- the diff checks.
