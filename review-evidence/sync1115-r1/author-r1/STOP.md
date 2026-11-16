[A787] STOP

The sync of dev `6b66f66d` into dev-soft-core (ruling item 3) is merged and resolved locally at `d2da3159` (not pushed). One CPU service-budget row is over its bound at 8x8/1if after the merge.

**The row.** At 8x8/1if, `save-held` and `save-starved` each have one MRPDU row over its bound: `mrpdu.leaveall.if0` at 161.1 ms. A LeaveAll timer runs out at 14,091 ms under the held load, and its first frame or build comes 161 ms later. THE TRANSMIT's bound is 49 ms, and the row budget is 20 ms. Every other 8x8/1if row is as at the base: arm A's four parts, 95 groups, 0 refusals; the only other misses are `backlog-owed`'s 7 held-egress rows, which are ruled.

**The cause is the #840 identity, not the merge's code.** The split SRP adapter seeds lwSRP's LeaveAll draws from the interface MAC (`srp_mbx.c:347-348`). The MAC moved to 02:4B:4C:4B:4C:01, so in `save-held` the LeaveAll run-outs moved:

| Run of `save-held` at 8x8/1if | LeaveAll run-outs | MRP timers' run-outs | Misses |
|---|---|---|---|
| base `659d7687` | 10,461.9 and 14,621.9 ms | 39 released, 34 empty, 0 late | 0 |
| head code with the old MAC in the 8x8 config, an experiment only | 10,461.8 and 14,621.8 ms | 39 released, 34 empty, 0 late | 0 |
| head | 14,091.0 and 14,921.2 ms | 41 released, 30 empty, 1 late | 1 |

**The weakness itself predates the sync.** In all three runs THE TRANSMIT's build at 8x8/1if is over the stated 95,000-cycle tier-2 slice: 108,118 cycles at base, 108,246 with the old MAC, 109,286 at the head. 8x8/1if is still held to one interface's 1x1/1if costs (#914's scope). The new seed puts a LeaveAll where the slice holds its build past the bound.

**1x1/1if holds at the head, leg for leg as at the base** (#902's legs, whose firmware equals the base's):
- arm A, 96 groups: 0, 0, 0 and 7 misses by quarter, the 7 being the ruled held-egress rows. Probe instances and paths are equal to the base's.
- the answering-every-port arm and the answering-ports leg: rc 0.
- `flip_grade.py --check --point 1x1/1if`: PASS, every row held, txL 48.43 of 49 ms.
- `load_grade.py --check`: 0.516 and 0.512 against 0.70.

**Decision needed** (I recommend option 1):
1. Carry the row as a finding owed to #914, the 8x8/1if tier rows: the sync proceeds, and #914 must hold THE TRANSMIT's row at every LeaveAll phase, not only at the base's.
2. Or hold the sync until #914 lands.

A seed that does not depend on the MAC would be a behaviour change beyond the ruling, so I have not made one.

**State of the lane.** One `--no-ff` merge `62625941` (10 files, 13 hunks, both sides kept; pins: gptp-processor `1616fc8f` and protocol-processor `801ef228` from dev, tsn-c-stack `715589c1` kept). After it, one commit for each semantic conflict found:
- `a563a83d`: the split control lane now binds #839's gated handshake. At the merge the split build refused with `%Error-UNDRIVEN: 'pp_txs_tvalid_w'`.
- `dfcd8eed`: the split leg writes the station MAC before its frame leaves, with two gate plants. `split-mutants`: 28 of 28 caught.
- `b84d095a` and `d2da3159`: dev's area plan named #810 as unmerged, which is false on this line.
- `d8c8c4b7` and `1facd42e`: the two-placement stimulus and its rows take the #840 identity.
- `3c94c76c`: the owed rows #893 fixes are deleted. Twin: 0 findings, 14 of 14 plants refused.
- `3a5ba178`: section 5's images are restated: 24 to 40 B more rom, no tile moves.
- `f5750b3d`: the documentation audit is regenerated.

**What else stands:**
- clockAccuracy 0x22, the #843 engine fixes and the #840 identity reach the split images, through the fabric gPTP engine, the board config and the AEM image.
- The ledger for #847, #852 and #893: each has a split counterpart with its test.
- Not reaching the split: #840's 1000BASE-T-only advertisement. It is in the release firmware only, and the split has no MDIO path (#919 does not list it).
- Split 1x1/1if route: all three directives meet the floors. The best is AltSpreadLogic_high, +0.399 / +0.036 ns.
- The docs workflow passes, and rtl-fast passes so far: firmware suites, `fw_coverage --check` PASS on 39 files, publication census, lint, yosys elaboration and split CDC. The mutation campaigns, elaborate, the Yosys shards, the 8x8/1if and release routes and the 4-shard sweep are not finished.

Receipts and the handoff are in the lane's round-1 output.
