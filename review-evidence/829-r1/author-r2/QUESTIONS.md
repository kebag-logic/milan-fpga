# Two questions for the manager, from PR #831 round 2

Findings only. Neither is fixed in this PR. Receipts are under `receipts/` here.

## (a) R761 S1: does the MII inter-frame gap on the pads fall short of IEEE 802.3?

**Yes. Queued MII frames leave the pads 480 ns apart, and 802.3 asks for 960 ns. The bring-up's stream could not have been affected: the Arty received that stream and sent none of it.**

**The clause.** IEEE 802.3-2022 4.4.2, Table 4-2: `interPacketGap` is 96 bits for MAC data rates up to and including 100 Mb/s, and the table's values "shall be used". At 100 Mb/s that is 960 ns. 22.2.3.1 says the parameter is measured on the MII from CRS deasserting to CRS asserting. The notes to 4.4.2 allow shrinkage as seen at a receiver at 10 Mb/s and 1 Gb/s. None of them lets a transmitter send less.

**The simulation.** A scratch probe in the closed loop's pad oracle (`receipts/gap/probe-mii.log`, `probe-gmii.log`) histograms `tx_en` low runs between frames, at this head:

| Shape | Between frames queued back to back | Standard |
|---|---|---|
| MII, 100 Mb/s, at 80 MHz and at 100 MHz system clock | 12 low samples, 480 ns, in 57 gaps of each run (481 ns in a few, from the bench's 200 ppm wire offset) | 960 ns |
| GMII, 1 Gb/s | 12 low samples, 96 ns, in 75 gaps (97 ns in one) | 96 ns |

Every other gap in those runs is far longer, because those frames were not queued.

**Why.** `LiteEthMACGap` counts 12 clocks of the transmit domain. `cycles` is `ceil(12 / (dw // 8))`, and `dw` is 8 on both PHYs (`liteeth/mac/gap.py`). On GMII that is 12 octet times. On MII a clock is half an octet, so it is 6 octet times, 48 bit times. Core LiteEth offers a per-PHY override, `tx_gap_cycles` (`liteeth/mac/core.py:146`), and only `ecp5rgmii` sets it. Nothing in this tree sets it on the MII PHY. This PR neither causes nor changes it: it comes from LiteEth and predates the delta.

**The bring-up's stream.** It was not affected, for two reasons.

1. The connection ran with the reference peer as talker and the Arty as listener. This gap is on the Arty's transmit path. Of 462,416 frames on `stream-2`'s capture, 447 are the Arty's, and none is a stream frame: they are gPTP (`88f7`), MSRP (`22ea`), MVRP (`88f5`), and AVDECC and MAAP (`22f0` subtypes `0xfa`, `0xfb`, `0xfc`, `0xfe`). The 460,354 stream frames, VLAN tagged, all come from other sources (`receipts/gap/stream-2-arty-frames.txt`).
2. The Arty never queued frames back to back on those captures. The smallest gap between two consecutive Arty frames on the wire is about 4.8 us in `f-07`, `f-10`, `f-11` and `stream-2` (`receipts/gap/capture-gaps.txt`), so 480 ns did not occur there at all.

**Who it can reach.** It needs two Arty frames queued in the MAC. An Arty talker, not run so far, could queue a stream frame right behind a control frame, and that pair would be 480 ns apart. Whether a given switch accepts that is not measured. At 10 Mb/s the same 12 clocks give 4.8 us against 9.6 us, by arithmetic only.

**If you want it fixed:** a new Issue. The likely change is one statement setting `tx_gap_cycles` on the MII shape, and it re-generates the MII chain. I did not try it.

## (b) R761 S2: the `gptp_shadow` process-cleanup lifecycle test

**Cause not established. It is the fixed 4 s cleanup deadline in `scripts/owned_process.py` expiring, at three call sites, and yes, it reaches `dev`.**

**Which assertion.** All of it ends in one raise, `scripts/owned_process.py:201`, `CLEANUP FAILED: owned descendants remain`, after `GRACE_SECONDS` 2.0 and `REAP_SECONDS` 2.0. The failing step differs each time:

| Run | Head | Host load in the record | Where it surfaced in `tb/verilator/gptp_shadow/test_mutant_lifecycle.py` | Descendants left |
|---|---|---|---|---|
| First sweep of this branch, 2026-11-01 13:53 | `3cc89f5f` | not recorded | `:419`, the `with OwnedProcesses()` around `interrupted(SIGKILL)`: an uncaught `RuntimeError` from `__exit__`, straight after the `isolated-SIGKILL` line | one: pid 2542233, that case's own handshake child, whose parent was the test's outer owner |
| Final sweep of round 1, 16:14 | `4cda0aa0` | near 100, the author's note | `:384`, in `outer_cancellation`: `assert status == 128 + signum and "\nsuites:" not in output`. The status differs because the nested sweep printed `REFUSED: process ownership: CLEANUP FAILED` | two: 3445385 and its child 3445514 |
| The external review's probe | head and `dev` | 105 to 112 | `:234`, in `interrupted`, on the `REFUSED: CLEANUP FAILED` text for SIGTERM | one |

In every suite log, the RTL checks and all nine controls in that suite pass, and the failure is in this test alone.

**Can it be reached on `dev`?** Yes, both by reading and by a run.

- `git diff 1f29f189 HEAD` is empty for `scripts/owned_process.py`, `test_mutant_lifecycle.py`, `private_inputs.py`, the suite's `Makefile` and `mutants.py`, and `scripts/run_all_suites.sh`.
- R762's `receipts/flake/dev2-1.log` has `dev` failing on the same raise at the same `:234`, in the first pass at load 105 to 112. In that pass `dev` failed 1 of 6 and head 4 of 6, which R762 notes does not separate them (p = 0.24).

So my predecessor's "not reproduced on `dev`" no longer holds.

**What the logs cannot say.** They do not say why a descendant outlived its deadline. The message prints pid, parent and start time and no process state, so a process stuck in uninterruptible sleep, one not yet reaped, and one merely slow to be scheduled look the same. Every case reached the hard deadline, so a descendant was still listed up to 2 s after SIGKILL began, which is what I would look at first. "Load" remains a correlation: all the failures I can date came at high load, but the first sweep's load is not recorded, and R761's 24 runs at load 43 to 53 all passed.

**This round's runs at this head:** the test passed in the sweep's `gptp_shadow`, and again in a separate clean-clone run. The host's load average read 82 about three minutes before that second run's log ended (`receipts/gates/load-and-memory.txt`). So that is one more pass at high load, which does not contradict a failure that comes and goes.

**If you want it settled:** a new Issue, per R762 S4. Print each descendant's `/proc/<pid>/stat` state in the message first, because that names the cause. The deadline can then be judged on evidence.
