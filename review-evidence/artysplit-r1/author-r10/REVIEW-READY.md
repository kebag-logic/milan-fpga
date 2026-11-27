[A829] REVIEW READY

Commit: `640699e6866602b2a5de5d404c43f3bd4df8037c` (local, branch `arty-int-1127`; nothing pushed or posted).

Changed:
- `7af5117f1`, `1903077be`: the Arty's bind-save bounds by #1009's rule, 400 ms in flight and 4 saves for the burst (PR #1004's ruling), and the bind self-test held to them.
- `033726520` to `640699e68`: THE 100 Mb/s EGRESS. At the Arty point the testbench drains the mailbox through the shipping transmit queue (`egress_queue.hpp`). `egress_mii.py` grades the row with 9 planted defects, and `egress_fixed.py` measures the fixed path on the converted MII chain. `grade.py` accepts the queue's lines.
- `6e49d1fad`: the census extractor refuses an overlong line, binds the copied qualification to the inventory, and gains `--selftest`.
- `fb4b456a4`: FR_NFR 3.4.1 (254 records; the 100 Mb/s row; AECP's admission burst as the structural maximum), the harness README and section 15.

Validation:
- The instant-egress census replayed through the queue changes the free-space outcome in 11 of 159 cases. So the census ran again at link rate: 159/159, no finding.
- Derivation: every cost and owner row unchanged, the installed row a fixed point. Load 0.5014, ACMP 29.84, txL 48.90, last notice 117.58 ms, longest pass 143,181 cycles.
- Qualification PASS, the egress row included. The no-disposition control finds no qualifying row (least last notice 237.0 ms).
- The 100 Mb/s row is 505.74 us of 1000 us: the 426.47 us largest wait, plus gPTP 54.88 us, times 1.05, plus 0.32 us fixed. The replay agrees with every testbench departure exactly.
- Packet and extract: 159/159 identical regrades, the control refused, and the extract passes the publication scrub unchanged.
- Gates at the head: 19/19. Harness self-test: 8/8 partitions.

Acceptance criteria: met for all four round-10 items.

Open risks/questions:
- The rings at capacity, 254 least records committed together, would leave their last octet 2.65 ms after commit. The control lane's 512-cycle gasket paces them, at 10.26 us a frame. That is above 1 ms, and above the AECP burst the ruling names as the structural maximum. No census case queues more than 19 records.
- The ruling's premise that the firmware reads TX_TAIL only for the free-space test does not hold: AECP's completions and REBOOT's drain read it too. The link-rate census covers all three.
- Round 9's open items stand: the +62-LUT routed delta, and #977 landing first needing one more integration.
