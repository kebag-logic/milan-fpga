# HANDOFF r10: [A825] #977 (part of #665), round 10

Status: **STOP at step 0** (09:30 CET 2026-11-27), as the instruction orders before any code. The registration cost restated by the rule over every registering group fails the 8x8/1if load ceiling, with or without the granted fourth hot-list window. That is an owner question. No commit this round: milan `pf-977-1` stays `a35b092f`, the stack `0f72ca69`. Nothing is pushed or posted.
ETA: none until the owner's answer. Steps 1-4 are not started; my estimate for them after the answer is about 15 h (step 1 ~4 h, step 2 ~2 h, step 3 ~8 h, step 4 ~1 h).

Inputs read in full: the RULING on round 9's STOP, #977 comment 7212897415; the manager's round 10 instruction.

Order: (0) restate the registration cost over every registering group by the rule from round 9's logs and compute the load at both points; STOP if it fails; (1) the delivery bound (one loss completion outside THE SETTLE and one binding change a delivery poll, the rest pending in turn within 2 x CTRL_SRP_SINKS ordinary passes, THE TRANSMIT never waits), its tests and plants, and the wire consequence in grader and test expectations; (2) the fourth hot-list window (srp-register-swap), S14's 8x8/1if expectation, the three groups, and the JoinIn-of-both-kinds record against 2 ms; (3) re-measure everything; (4) the lwSRP pin 73007b48 -> e27b34c9 with every product ELF byte-identical.


## STOP (step 0): the restated registration cost breaks the 8x8/1if load at 0.76

Measured over every registering group, the none and answering-ports arms, both one-interface points. The cost is a Talker's share of its record's apply past the SRP unit, plus its share of THE SETTLE's run after it (`load_grade.REGISTRATION_US`'s recorded definition), restated by the rule (plus 5 %, rounded up to 5 us). The tool is `regcost3.py`, which is regcost2's method. It divides each record by the Talkers its group's record registers: the sinks, or V for `srp-register-population`.

| Group | 1x1/1if at `07c4575e` | 8x8/1if at `07c4575e` | 8x8/1if with the fourth window |
|---|---:|---:|---:|
| `srp-register` | 5,118 cycles, 55 us | 8,513, 90 us | 8,454, 90 us |
| `srp-register-burst` | 10,850, 115 us | 12,387, 135 us | 12,309, 130 us |
| `srp-register-population` | 8,233, 90 us | 7,008, 75 us | 6,878, 75 us |
| `srp-register-leaveall` | 9,714, 105 us | 12,862, 140 us | 12,807, 135 us |
| `srp-register-swap` | 14,592, 155 us | **15,939, 170 us** (apply 140,070, settle 40,880, over 9) | **15,842, 170 us** (apply 140,530, settle 39,548, over 9) |
| `srp-register-messages` | **16,986, 180 us** (apply 54,557 with 8 Listener Messages, settle 7,916, over 2) | 11,641, 125 us | 11,585, 125 us |

Stated: 120 us at 1x1/1if, 135 us at 8x8/1if.

| `REGISTRATION_US` (1x1/1if, 8x8/1if) | 1x1/1if load (ceiling 0.70) | 8x8/1if load (flip ceiling 0.76) | `flip_grade.py --check --point 8x8/1if` |
|---|---:|---:|---|
| stated: 120, 135 | 0.521 | 0.757 | PASS |
| restated by the rule: 180, 170 | 0.523 | **0.761** | **FAIL** (over the flip ceiling 0.76) |
| 180, 165 | 0.523 | 0.760 | FAIL |
| 180, 160 | 0.523 | 0.760 | PASS |

- At 1x1/1if the restated 180 us passes with room: load 0.523, and `flip_grade --point 1x1/1if` passes.
- At 8x8/1if the dearest record is the swap: every input's Lv of the registered Talker kind with New of the other in one MRPDU (35.2.6), the case the ruling of 2026-11-27 item 5 added. To state 160 us it would need at most 15,238 cycles a Talker all in, about 4 % under the measured 15,842.
- **The fourth window does not close it.** It is learned by the recorded procedure on the 1x1/1if default arm's `srp-register-swap` from 300,000 bus cycles before the swap record, 900,000 PCs, its 19 new sections appended: 289 entries, all 72 maps clean, in a scratch clone only. It moves the swap by 97 cycles a Talker (0.6 %). The hot list orders text inside `rom`, so it buys fetch locality, not a faster memory.
- **Step 1's delivery bound does not reach this figure.** The swap's cost is lwSRP's apply (`srp_mbx:apply_receive`) and THE SETTLE's completions after it. The ruling bounds completions outside THE SETTLE and binding changes, which land in later passes' delivery polls. Those are outside the registration term's definition.

**Owner question** (facts for it, not a choice):

- Either the 8x8/1if flip ceiling or `REGISTRATION_US`'s definition moves for this record, or the swap record's cost falls by about 4 % or more.
- On the last, round 4 measured a one-entry completion prototype for THE SETTLE at 2,302 cycles a sink against 4,136 (not in tsn-c-stack PR #41: a new public entry). Applied to this swap's 39,548-cycle settle at that ratio it would make about 22,000. That would bring the record to roughly 13,890 cycles a Talker, 150 us by the rule. It is an estimate from round 4's ratio, not a measurement.

Receipts:

- `receipts/step0/regcost-table.md`;
- the per-record lists `regcost-{1x1,8x8-1if}-nowindow.txt` and `regcost-8x8-1if-window.txt`;
- `load-flip-restated-a35b092f.txt`;
- `regcost3.py.txt`;
- the window's learn report, `receipts/step0/window-learn.txt`.

**Round 9 carried over:** firmware-gate shard 3 at `a35b092f` (the re-anchored plant) PASSED (`test_ctrl_firmware: PASS`). Round 9's every-arm pool was stopped at 16 of 562 groups (08:53): round 10's ruling changes firmware source, so its results would not stand.

## Scratch state (nothing in the lane)
- `r10/win`: a clone at `a35b092f` with the four-window hot list written (uncommitted; it is step 2's window, learned as ruled, to be relearned at step 3's head).
- `r10/b/8x8-1if/{none,answering-ports}`: its builds. `r10/w`: their 12 registering groups.
- `r9/arms3`: srp-register and srp-register-burst at `07c4575e` (pool9c).
- `tools/poolx.py` (a parameterised pool), `tools/hot_cut4.py` (the fourth window's anchor: the first RXC after `srp.register_swap.if0`), `tools/regcost3.py`.

## Log
- 08:53 round 9's every-arm pool (pool9-a, 16 of 562 groups done) stopped: round 10 changes firmware source, so its results would not stand. pool9c started (CPUs 0-7): srp-register and srp-register-burst at both points, none and answering-ports, on the `07c4575e` builds, for step 0.
- 09:01 step 0, pre-window: dearest a Talker all in over the new groups at 07c4575e: 8x8/1if 15,939 cycles (answering-ports srp-register-swap: apply 140,070, settle 40,880, over 9), 170 us by the rule; 1x1/1if 16,986 (none srp-register-messages: apply 54,557, settle 7,916, over 2), 180 us. With them the 8x8/1if load is 0.761 (flip_grade FAILs from 165 us; 160 passes), 1x1/1if 0.523 (passes). The fourth window (srp-register-swap, 1x1/1if default arm, 900,000 PCs, 19 new sections appended; 289 entries, 72 maps clean) is learned into a scratch clone to measure step 0 with the window, as the instruction asks, before any STOP.
- 09:02 the fourth window learned and applied in the scratch clone r10/win; 8x8/1if none and answering-ports built (b10w), their 12 registering groups run (pool10w, CPUs 16-27); pool9c done (8 groups).
- 09:25 every group in: the 8x8/1if swap restates to 170 us with and without the window; the 8x8/1if load at 170 us is 0.761, flip_grade FAILs. STOP per the instruction's step 0. Round 9's shard 3 rerun at a35b092f PASSED (08:39).

STOP: step 0, the registration cost restated by the rule over every registering group is 170 us at 8x8/1if (srp-register-swap, 15,842 cycles a Talker all in, with the fourth window; 15,939 without), and the 8x8/1if load is then 0.761, over the 0.76 flip ceiling (flip_grade FAILs from 165 us); 1x1/1if restates to 180 us and passes at 0.523
