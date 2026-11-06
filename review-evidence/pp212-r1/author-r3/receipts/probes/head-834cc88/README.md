# The reviewers' probes at `834cc88`

Each probe tree is `git archive 834cc88 hdl tb/common tb/srp_stream_fsms` from a clean
clone, with one block inserted into `tb/srp_stream_fsms/sim_main.cpp`. Each run is
`make -C <tree>/tb/srp_stream_fsms RUN_ARGS=suite` with the pinned Verilator 5.050.

| Run | Block (`in/`) | Inserted by | Result |
|---|---|---|---|
| `p769` | `r769_2_probe_block.cpp` (R769-2's packet, unchanged) | `insert.py`, before the tally (R769-2's own anchor) | 1,551 checks, 1 FAIL: P1 before the old Lv (below); P8 `tk 0 state 0 unreg 1` |
| `p770` | `r770_probes.inc` (R770-2's packet, unchanged) | `insert770.py`: R770-2's three insertions, anchored after PS24 instead of PS23 | 1,605 of 1,605; XP2 `reg 0 tk 0 state 0` |
| `pw` | `p1_words.cpp` (the author's): R769-2 P1's steps, printing what its `nothing_applied()` reads | `insert.py` | 1,512 of 1,512 (prints only) |

R769-2 P1's check is `nothing_applied()`. It requires no EVT_TK_REGISTERED, NONE, MT and
no timer op at the settle, and no push and no declaration at the next tx!.

Under the ruling's option (a), the link change withdraws the settled sink's declaration as a
leavetimer! does. So in the run before the old Lv, that Lv is still owed at the settle and
goes out at the next tx!. `pw` shows that this is the only thing P1's check sees:
- the settle reads `reg 0 tk 0 state 0 ops 0`;
- the next tx! carries one push, `5/2@0001` (code 5 Lv, FourPacked 2 Ready, the stream), and
  `decl 0`;
- in the run after the old Lv the push list is empty.

PS24 grades that sequence with the Lv expected.
