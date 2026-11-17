# Row-bound STOP

The standard harness regrade exits 1, with zero refusals, seven budget misses,
4 of 12 paths failing, and zero of 311 work passes over the 2 ms share.
This is a completed trace, not a partial simulation being mistaken for a failure.
CPU: 100 MHz on sys; bus: 100 MHz. Point: 1x1, one interface.

The trace was built from the clean clone at `428f125d`. The firmware C/header files
and service harness code are identical at final head `73e30fb2`; the intervening
changes are docs, twin bookkeeping and split memory ledger entries. This is not
claimed as a complete final-head gate. See `../candidate-state.txt`.

| Row | Measured ms | Approved bound ms |
|---|---:|---:|
| `backlog.owed.if0` | 63.03732 | 20 |
| `backlog.owed_behind0.if0` | 63.22358 | 20 |
| `backlog.owed_behind1.if0` | 63.40896 | 20 |
| `backlog.owed_behind2.if0` | 63.59426 | 20 |
| `backlog.owed_behind3.if0` | 63.77957 | 20 |
| `backlog-owed.service.acmp.last.if0` | 62.14233 | 20 |
| `backlog-owed.service.aecp.last.if0` | 61.88483 | 20 |

The primary row has seven owed responses ahead and measures RX commit to response
commit. Its start is sys cycle 272873024 and its end 279176756 (6,303,732 cycles).
From the separate `room` marker it takes 303,433 cycles, 3.03433 ms.

`tb/verilator/ctrl_service_budget/scenario.py:813` explains the full transmit ring
and the 60 ms egress hold. Line 844 implements `wait cycles 60 * MS` before
`mark room` and `txready 1`. `grade.py:586` measures from RX commit, and line 593
applies the budget to that complete interval; `also_from` is a separate figure.
The group records 17,298 retry rounds with zero notices, the heaviest 1,935 cycles.
The notification pacing therefore cannot remove the fixture's 60 ms egress hold.

The scenario and grading code are unchanged from `70f4056f`. No claim is made that
#936 introduced this failure. Changing the stimulus, measurement origin or approved
bound needs a public decision outside #936; none was changed here.

Reproduction of the completed trace using the repository's standard grader:

```sh
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 \
  --build-dir "$BUDGET_BUILD" --regrade --groups backlog-owed --out "$RECORDED_TRACE"
```

The build directory is the original recorded build; its input digests and model hash
are checked by `build.reused`. `backlog-owed.txt` is byte-checked against the scenario.
The full raw trace is 14,853,878 bytes, so only its hash, size and selected lines are
included in `trace-excerpt.txt`; the complete graded JSON and table are in this folder.
No record-budget option masks the regrade's exit status. The separate simulation
`RESULT: PASS` proves the stimulus completed; it is not the budget verdict.
