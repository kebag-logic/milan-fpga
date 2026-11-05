[A733b] Follow_Up information TLV values, announce receipt timeout from the received interval, and the three stricter readings (#100)

Closes #100

Base: main `3e3a4e7`, merged with main `5184fb3` in round 2. Head: `84fd227`.

The sections from "What changes" to "Merge note" are round 1's, at head `3e3f041`. "Round 2" at the end merges main and fixes three wordings. It changes no behaviour.

## What changes

**1. Follow_Up information TLV of this plane's mastership** (IEEE 802.1AS-2011 10.2.8.2.1 j) to l), 10.2.9 Figure 10-6, 11.4.4.3.7 to 11.4.4.3.9)

- The engine holds the three values in a new read-only region 6 of the microCPU's state address map. The Follow_Up leg (`prog_leg_syncfu`) sends them in place of the zeros it used to send.
- gmTimeBaseIndicator counts BECOME's PHC word-3 write, the plane's one entry into mastership. Like the clockIdentity mirror, it has no warm-reset assignment.
- lastGmPhaseChange is clockSourcePhaseOffset: this plane's time minus the grandmaster's at the last Sync it consumed as a slave, as ScaledNs. It reads zero after a reset.
- scaledLastGmFreqChange is the trim the PHC keeps less the rate estimate the slave held, scaled by 2^41 and floored. It is zero when an active slew makes BECOME write the estimate itself, and zero when no rate has been written since reset.
- cumulativeScaledRateOffset stays zero (a grandmaster's rateRatio is 1.0, 10.2.8.2.1 i)).

**2. Announce receipt timeout from the received interval** (10.3.9.1, 10.6.3.2, Figure 10-13)

- An Announce handler's receipt-watch arm becomes 3000 ms × 2^logMessageInterval of that Announce, counted from its last octet. Every other arm of timer slot 2 keeps its own delta.
- Intervals from 2^-11 s to 2^19 s are covered. A shorter interval gives 1 ms, a longer one the 2^19 s value, and negative exponents round down to whole milliseconds.
- logMessageInterval 0 gives 3000 ms, 1 gives 6000 ms and -1 gives 1500 ms. The deadline counts whole engine milliseconds from the last octet, so the port ages within 1 ms short of the interval: the harness measured 5999.74 ms and 1499.74 ms.

**3. Aging at the instant** (maintainer decision, 2026-11-05)

- An Announce whose last octet arrives in the deadline's millisecond or later is dispatched after the expiry. With a 1 s interval, Announces 3.0 s apart age the port; Announces 2.999 s apart never do.
- An expiry whose watch has since been re-armed, stopped or taken is dropped at the queue head. So an Announce received before the deadline still refreshes the watch, however late its handler runs.
- Inside the clauses:
  - In Figure 10-13, rcvdMsg comes from another state machine (Figure 10-12). Annex D leaves the order between state blocks of different machines undefined, so expiry first is an order the notation permits.
  - The Announce is still processed after AGED and re-elects its grandmaster.
  - Milan v1.2 4.2.6.2.3 Table 4.2 allows 2.7 to 4.5 s, and the watch fires at 2.999 to 3.000 s.

**4. Late Pdelay responses are lost responses** (maintainer decision, 2026-11-05)

- PDPAIR first compares t4 − t1 with `PD_LATE_NS_C`. A later pair moves nothing: no ratio window, no delay, no verdict. `S_PDGOT` stays clear, so the next beat counts the loss (Figure 11-8 RESET, 11.2.15.3). After allowedLostResponses (3, 11.5.3), the fifth consecutive loss clears asCapable.
- The bound is **15.006181 ms**, derived term by term:

  | Term | Value | Source |
  |---|---:|---|
  | Maximum Pdelay turnaround, at the TAI frequency | 15 ms | Milan v1.2 4.2.6.2.6 (802.1AS-2011 B.2.3's 10 ms relaxed by 50 %) |
  | Round trip of a link that can stay asCapable | 2 × 800 ns | Milan v1.2 4.2.6.1.1 (`NPD_HI_C`) |
  | The most this clock reads that 15.0016 ms span long, rounded up | × 1.0003 | B.1.1 100 ppm + `RATE_PPM_C` 200 ppm |
  | One stamp granule each for t1 and t4 | + 2 × 40 ns | B.1.2 |
  | ⌈15,001,600 ns × 1.0003⌉ + 80 ns | 15,006,181 ns | `PD_LATE_NS_C` |

- Inside the clause: 4.2.6.2.6's "shall" is the 15 ms turnaround, and no response within it is ever counted lost. Later responses "may or may not be processed". The clause's "should not" result in asCapable FALSE is a recommendation that the board deliberately does not take.

**5. clockAccuracy 0x22 by default** (8.6.2.3; IEEE 1588-2008 7.6.2.5 Table 6: "within 250 ns")

- `CQ_C` is now `0xF822436A`. `--clock-accuracy` sets the octet per image, so a build without a characterised oscillator states `0xFE`, as 8.6.2.3 b) requires.
- This is a generator option. No top-level port, parameter or host register map changes.

**ROM words.** `e_hdr` writes adjacent zero header fields as one wider zero field, so the octets on the wire are unchanged. That pays for the two new tests: the shipping image uses 1,015 of 1,024 words (was 1,022).

## Checks

The engine harness adds phases 52 to 56 in their own `#100` section. Each acceptance row has checks named `#100 ...` and planted mutants (`tb/verilator/engine/p100_mutants.py`, 24 controls). Each mutant must fail every check it names:

| Acceptance row | Checks | Mutants caught by name |
|---|---|---|
| Slave at a known rate ratio, then grandmaster loss | `#100 TLV settled: ...` and `#100 TLV slewing: ...`: gmTimeBaseIndicator increments, lastGmPhaseChange is the last offset, scaledLastGmFreqChange is the kept trim less the estimate (after a lock on a master 100 ppm fast) | TLV sent zero; indicator does not count; phase zero, not ScaledNs, or high word dropped; frequency zero, the estimate, the trim while slewing, or an unknown rate taken as zero |
| A peer logAnnounceInterval of 1 ages the port at 6 s | `#100 logAnnounceInterval 1: still slave 5998 ms after the Announce` and `... master within 6002 ms of the Announce`; -1 at 1.5 s | the watch ignores the received interval; a negative interval lengthens the watch; the watch counts from the handler |
| Announces exactly 3.0 s apart age the port | `#100 3.0 s apart, ...: the port is aged` at three tick phases; `#100 2.999 s apart: the port is not aged`; a handler stalled past the deadline still refreshes for an Announce received before it | a late Announce runs before the expiry; an Announce at the instant refreshes the port; lateness judged at dispatch; a stale expiry dispatches; a dispatched expiry leaves its watch armed |
| Responses past the bound clear asCapable after allowedLostResponses; inside it they do not | `#100 responses at the bound: six keep asCapable` and `... the delay is published`; `#100 late responses: four keep asCapable`, `... the fifth clears asCapable` and `... none moves the delay` | a late response completes its exchange; the bound one nanosecond short; the bound without the clock tolerance, the link or the timestamp granules |
| The default clockAccuracy is 0x22 | `#100 the default image announces clockAccuracy 0x22`; the fourth pass's `--clock-accuracy 0xFE` image: `p1 255 #100 a --clock-accuracy 0xFE image announces 0xFE` | the default clockAccuracy is unknown; `--clock-accuracy` is ignored |

Existing checks:

- Each shipping pass of the engine suite counts 2,048 checks at the base and 2,098 at the head. The fourth pass counts 60 and 61.
- Peers in the harness announce the image's clockQuality, so BMCA ties stay as they were.
- D2c's lost t1 carries a time the late bound would admit, so its control still shows.

## Gates (head 3e3f041)

All at head 3e3f041, every command rc 0, none piped:

| Gate | Result |
|---|---|
| `make contract` | PHC interface contract: PASS |
| `make -C tb/verilator/ucpu` | 768 checks, 0 FAIL |
| `make -C tb/verilator/parser` | 378 checks, 0 FAIL; mutation arm 16, 0 FAIL |
| `make -C tb/verilator/engine run` | 2,098 checks in each of the three shipping passes, 61 in the fourth, 0 FAIL |
| engine mutation arm (`make -C tb/verilator/engine mutants`, run 8 jobs at a time) | 160 checks: the unmutated control and 159 mutants, the 24 #100 controls among them, all caught |
| `make -C tb/verilator/gaskets` | 81 checks; mutation arm 5; 0 FAIL |
| `make -C tb/tsngen` | 288 checks; mutation arm 4; 0 FAIL |
| `make -C bench/arty test` | PASS |
| `make lint` | rc 0 |
| `make docs` | docs check, docs selftest (127 arms), source evidence (20 exact, 0 findings) and selftest, diagrams: PASS |
| `make diagrams-check` | PASS |
| `make ooc` | clock-order selftest (30 arms) and both synthesis checks PASS; figures below |
| `git diff --exit-code`, `git status --porcelain` | regenerated ROM images match the committed ones; tree clean |

Before the final head, the full mutation arm caught two harness defects of this branch:

- "a late response completes its exchange" did not fail `#100 late responses: none moves the delay`, because a completed late pair computed the same 600 ns delay. Late pairs now carry the residence of a 650 ns delay.
- The older #84 control "mastership never publishes the master bit" missed its check because phase 52 read an empty frame after a timed-out wait and crashed the pass. The #100 phases now refuse short frames and missing commits.

Both controls now fail by name.

## Area and timing (`make ooc`: Vivado out-of-context synthesis, xc7a100tfgg484-2, clk 10 ns)

| Top | Run | LUTs (logic + LUTRAM) | FFs | BRAM tiles | DSPs | WNS | Failing endpoints |
|---|---|---:|---:|---:|---:|---:|---:|
| `KL_gptp_ucpu` | base 3e3a4e7 | 1,643 (1,511 + 132) | 733 | 1.5 | 4 | +1.941 ns | 0 of 3,165 |
| `KL_gptp_ucpu` | head 3e3f041 | 1,643 (1,511 + 132) | 733 | 1.5 | 4 | +1.941 ns | 0 of 3,165 |
| `KL_gptp_engine` | base 3e3a4e7 | 4,926 (4,436 + 490) | 3,459 | 1.5 | 4 | +2.249 ns | 0 of 12,006 |
| `KL_gptp_engine` | head 3e3f041 | 5,425 (4,935 + 490) | 3,618 | 1.5 | 6 | +2.043 ns | 0 of 12,372 |

The engine adds 499 LUTs, 159 FFs and two DSPs, the TLV frequency multiply. Timing still closes at 10 ns with +2.043 ns of slack.

## Parent consumer gates

The parent was run at milan-fpga dev `604899c0` with this head as the `gptp-processor` gitlink, committed locally, never pushed. It needs a companion change when it moves the gitlink (milan-fpga #840 records the readings):

- `configs/endstation_ax7101_8x8.yaml` and `configs/endstation_ax7101_1x1_tdm8.yaml`: `gptp.clock_accuracy: 0x22`. The builder refuses a value that diverges from the engine's.
- `avdecc/aem_specs.py`: the built-in gptp `clock_accuracy=0x22`.
- `sw/builder/test_builder.py`: the model-shape pins move, because AVB_INTERFACE clock_accuracy is descriptor content (IEEE 1722.1 6.2.2.8). arty_current's hash becomes `0x001BC5B812EC1859` and its served pin `0x001BC50AC1000006` stays, as in the parent's earlier clock-field move. arty_4x4's hash-derived id becomes `0x001BC5ECED81D3F3`.

With that change, every gPTP consumer gate passes, rc 0:

| Gate | Result |
|---|---|
| `make -C tb/verilator/gptp_shadow -j8` | 325 checks, 0 FAIL |
| `make -C tb/verilator/milan_dp gptp` | 210 checks, 0 FAIL |
| `make -C tb/verilator/milan_dp gptp-lat` | 210 checks, 0 FAIL |
| `make -C tb/verilator/milan_dp_gptp` (scheduled physical suite) | physical 151 checks; setup abort 6, no-TX 20, no-Pdelay 14, recentre 14; 0 failures |
| `make -C tb/verilator/milan_dp_gm_steps` | gmstep 196 checks, 0 failures |
| `make -C tb/verilator/gptp_plane`, `gptp_txts`, `gptp_tables` | PASS (phc_step 62, txts 95, tables 36 checks, 0 failures) |
| `make -C tb/verilator/tsn_fuzz ptp` | the gPTP slice builds; its field campaign skipped here because its packet generator is not installed, so this is not a pass of that campaign |
| `scripts/check_cpp_idiom.py`, `check_py_idiom.py`, `xvlog_gate.py --check`, `check_rtl_source_lists.py`, `check_port_contracts.py`, `measure_naming.py --check`, `measure_test_evidence.py --check`, `docs_check.py`, `lint_rtl.py --check` | rc 0 |
| `sw/builder/test_builder.py` | ALL GATES PASS EXCEPT 1 NOT RUN: gate 11 needs a LiteX place report from a full build, not gPTP |
| `git status --porcelain` | clean |

## Merge note (round 1; the merge is done in round 2)

PR #99 merged into main (5184fb3) after this branch was cut from 3e3a4e7. The two `scripts/check_docs*.py` files here are byte-identical to main's. A trial merge conflicts only in `docs/SOURCE_EVIDENCE.md`: keep this branch's file and take main's two parser anchors (`KL_gptp_rx_parser.sv#L439` and `#L521`). Then run:

```sh
python3 scripts/check_source_evidence.py
```

On that merge, the repository gates pass, rc 0: contract, ucpu, parser 482 + 35, engine 2,098 × 3 + 61, gaskets, tsngen, bench, lint, docs and diagrams, with a clean tree.

## Round 2

Head `84fd227`, four commits on `3e3f041`. Both round-1 reviews were positive. This round makes the branch mergeable and changes no behaviour.

**Merge of main `5184fb3` (PR #99).** One `--no-ff` merge, with no rebase and no force. The only conflict was `docs/SOURCE_EVIDENCE.md`, in one hunk of five rows:

| Row | This branch | Main | Kept |
|---|---|---|---|
| Deferred receive event | `KL_gptp_rx_parser.sv#L392` | `#L439` | main's (the parser is main's) |
| Four-entry event queue, Parser arbitration priority, Priority timestamp return, Accepted-beat result face | `KL_gptp_engine.sv#L559`, `#L586`, `#L407`, `#L413` | `#L467`, `#L494`, `#L405`, `#L411` | this branch's (the engine is this branch's) |

"Ignored receive flag bits" merged without a conflict to main's `KL_gptp_rx_parser.sv#L521`. The source-evidence checker reports 20 exact anchors and 0 findings:

```sh
python3 scripts/check_source_evidence.py
```

The merge leaves the engine RTL, the generator and the engine mutants byte-identical to `3e3f041`.

**Wording only:**

| Item | Where | Now |
|---|---|---|
| R777-1 R1 | `docs/HDL_DEVELOPER.md:328`, `:330` | "Region 6 serves gmTimeBaseIndicator, lastGmPhaseChange as ScaledNs." and "It also serves scaledLastGmFreqChange, scaled by 2^41." |
| R778-1 S3 | `docs/INTEGRATION.md:857-865` | lastGmPhaseChange is defined by 11.4.4.3.8: a ScaledNs, the current grandmaster's time minus the previous one's, taken when the current grandmaster became grandmaster. This plane sends the offset it last measured as a slave, not extrapolated to the handover. The RTL does not change. |
| R778-1 S4 | `hdl/ucode/gen_gptp_ucode.py:2612` | The `--clock-accuracy` help, where the 0xFE alternative is chosen, reads `CLOCK_ACCURACY_UNKNOWN_C`. It prints the same text. |

The review's exact R1 sentence is 13 words, and the docs gate refuses more than 10 per sentence ("docs/HDL_DEVELOPER.md:328: 13 words"). So the same words, in the same order, are split into two sentences at "and".

**To the residue checklist, unchanged here:**

- R778-1 S1: grade scaledLastGmFreqChange exactly, and plant the truncation probe.
- R778-1 S2: a Sync between an Announce's last octet and its handler.
- R778-1 S5: the parent's `OUR_CQ` peer constants.
- R778-1 S6: an elaboration bound on `CLK_HZ_P` for the TLV multiply.
- R777-1 S3: the BTCA arm literal against `ANN_RTO_MS_C`.
- R777-1 R2 and S5 belong to the parent re-pin PR.

**Gates at `84fd227`.** Clean clones of the head; every command rc 0, none piped:

| Gate | Result |
|---|---|
| `make contract` | PASS |
| `make -C tb/verilator/ucpu` | 768 checks, 0 FAIL |
| `make -C tb/verilator/parser` | 482 checks, 0 FAIL; mutation arm in full, 35 checks (control and 34 mutants), 0 FAIL |
| `make -C tb/verilator/engine run` | 2,098 checks in each of the three shipping passes, 61 in the fourth, 0 FAIL |
| engine mutation arm, in full (run 8 jobs at a time) | 160 checks, 0 FAIL: the control and 159 mutants, all 24 #100 controls caught by name |
| `make -C tb/verilator/gaskets` | 81 checks; mutation arm 5; 0 FAIL |
| `make -C tb/tsngen` | 288 checks; mutation arm 4; 0 FAIL |
| `make -C bench/arty test` | PASS |
| `make lint` | rc 0 |
| `make docs` | docs check, docs selftest (127 arms), source evidence (20 exact, 0 findings) and its selftest, diagrams: PASS |
| `make diagrams-check` | PASS |
| `make ooc` | PASS; figures below |
| `git diff --exit-code`, `git status --porcelain` | regenerated ROM images match the committed ones; tree clean |
| `git diff --check 5184fb3 84fd227` | rc 0 |

**Area and timing at `84fd227`** (`make ooc`, xc7a100tfgg484-2, clk 10 ns):

| Top | Run | LUTs (logic + LUTRAM) | FFs | BRAM tiles | DSPs | WNS | Failing endpoints |
|---|---|---:|---:|---:|---:|---:|---:|
| `KL_gptp_ucpu` | main 5184fb3 | 1,643 (1,511 + 132) | 733 | 1.5 | 4 | +1.941 ns | 0 of 3,165 |
| `KL_gptp_ucpu` | head 84fd227 | 1,643 (1,511 + 132) | 733 | 1.5 | 4 | +1.941 ns | 0 of 3,165 |
| `KL_gptp_engine` | main 5184fb3 | 4,920 (4,430 + 490) | 3,461 | 1.5 | 4 | +2.249 ns | 0 of 12,004 |
| `KL_gptp_engine` | head 84fd227 | 5,395 (4,905 + 490) | 3,620 | 1.5 | 6 | +2.043 ns | 0 of 12,372 |

Against main, the engine adds 475 LUTs, 159 FFs and two DSPs, and timing closes with +2.043 ns.

**Parent consumer gates at `84fd227`.** milan-fpga dev `604899c0`, with round 1's companion change and this head as the gitlink, committed locally, never pushed. Every command rc 0:

| Gate | Result |
|---|---|
| `make -C tb/verilator/gptp_shadow -j8` | 325 checks, 0 FAIL |
| `make -C tb/verilator/milan_dp gptp` | 210 checks, 0 FAIL |
| `make -C tb/verilator/milan_dp gptp-lat` | 210 checks, 0 FAIL |
| `make -C tb/verilator/milan_dp_gptp` (scheduled physical suite) | physical 151 checks; setup abort 6, no-TX 20, no-Pdelay 14, recentre 14; 0 failures |
| `make -C tb/verilator/milan_dp_gm_steps` | gmstep 196 checks, 0 failures |
| `make -C tb/verilator/gptp_plane`, `gptp_txts`, `gptp_tables` | PASS (phc_step 62, txts 95, tables 36 checks, 0 failures) |
| `make -C tb/verilator/tsn_fuzz ptp` | the gPTP slice builds; its field campaign skipped here because its packet generator is not installed, so this is not a pass of that campaign |
| `scripts/check_cpp_idiom.py`, `check_py_idiom.py`, `xvlog_gate.py --check`, `check_rtl_source_lists.py`, `check_port_contracts.py`, `measure_naming.py --check`, `measure_test_evidence.py --check`, `docs_check.py`, `lint_rtl.py --check` | rc 0 |
| `sw/builder/test_builder.py` | ALL GATES PASS EXCEPT 1 NOT RUN: gate 11 needs a LiteX place report from a full build, not gPTP |
| `git status --porcelain` | clean |
