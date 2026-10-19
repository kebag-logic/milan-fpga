https://github.com/Mister-M-alt/FPGA-gPTP/issues/85

Found by the in-house qualification run of 2026-10-18 on the AX7101 (dev e9cbb676).

**Behaviour.**
- With another station as grandmaster, the DUT's GET_AS_PATH path_sequence is the received path without the DUT itself. With the grandmaster directly attached it is [grandmaster], where it should be [grandmaster, DUT].
- With a 4-hop path upstream, the DUT's own entry is missing at the end.
- A reference end station on the same bench ends its path with its own clockIdentity.

**Required.**
- IEEE 802.1AS-2020 10.3.9.23: a PTP Instance's pathTrace is the received pathSequence with thisClock appended (see also 10.3.13.2.4).
- IEEE 1722.1-2021 7.4.41 and Milan v1.2 5.4.2.24 serve GET_AS_PATH from it.

**Source.** `hdl/ucode/gen_gptp_ucode.py:1580-1588` stages the taken Announce's PathTrace into the publish bank as received, and thisClock is never appended. (`prog_become` publishes the one-entry grandmaster path, which is right.)

**Done when:**
- when a slave port takes an Announce, the published path is the received path plus thisClock (count + 1);
- the path stays consistent with the grandmaster at every transition, which #82 also covers;
- simulation cases for a direct and a multi-hop grandmaster, each with a planted mutant;
- the parent's consumer gates pass.

