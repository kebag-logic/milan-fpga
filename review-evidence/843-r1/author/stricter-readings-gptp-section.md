## gPTP readings

[FPGA-gPTP #100](https://github.com/Mister-M-alt/FPGA-gPTP/issues/100) items 3 to 5 are deliberate stricter readings.

Its items 1 and 2 are defects, tracked there.

They merged in FPGA-gPTP main `1616fc8f`, PR #101.

[#843](https://github.com/kebag-logic/milan-fpga/issues/843) pins that commit.

| Reading | Clause | The clause allows | The board does | Why | At the pinned processor |
|---|---|---|---|---|---|
| Announce aging at the instant | Milan v1.2 4.2.6.2.3, Table 4.2; IEEE 802.1AS-2011 Figure 10-13, as Cor1 changes it | announceReceiptTimeout from 2.7 s to 4.5 s. Figure 10-13 guards CURRENT to AGED with `!rcvdMsg`, but does not order PortAnnounceReceive setting `rcvdMsg` against the expiry instant | An Announce arriving exactly at the expiry does not refresh the port; the timeout fires first. With a 1 s interval, Announces 3.0 s apart age the port | 3.0 s lies inside Table 4.2. Such a gap is outside Table 4.1's 1500 ms Announce maximum | Graded: an Announce in the deadline's millisecond ages the port first, and the port re-elects right after it |
| Late Pdelay responses | Milan v1.2 4.2.6.2.6; IEEE 802.1AS-2011 B.2.3, 11.2.15.1.10, Figure 11-8, 11.5.3 | A turnaround of at most 10 ms (B.2.3), relaxed by 50% to 15 ms. Later responses may or may not be processed, and "should not" clear asCapable | A Pdelay_Resp and Pdelay_Resp_Follow_Up pair later than 15 ms counts as a lost response. Above allowedLostResponses, which is 3, asCapable becomes FALSE | "Should not" is a recommendation, and the board takes the stricter path | A response whose t4 - t1 exceeds 15.006181 ms counts as lost (`PD_LATE_NS_C`); one at the bound is kept |
| clockAccuracy | IEEE 802.1AS-2011 8.6.2.3; IEEE 1588-2008 7.6.2.5, Table 6 | The value reflecting the LocalClock and ClockSource, or 0xFE when that is unknown | A build parameter, set per board. The AX7101 announces 0x22, accurate to within 250 ns. The Arty's oscillator is not characterised, so it announces 0xFE | The decision. 7.6.2.5 asks for an estimate behind any claimed value | The builder passes each config's `gptp.clock_accuracy` to `--clock-accuracy`. AX7101 0x22, Arty 0xFE |

- The 15 ms bound is 10 ms relaxed by 50%.
- A build claiming 0x22 owes that oscillator characterisation.
- The processor issue's harness rows are the executable evidence.
- The `milan_dp` legs grade 0x22 and 0xFE on the wire.
- Builder gate 26c grades each config's image.
