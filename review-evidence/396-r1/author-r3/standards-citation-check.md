[A361] Round 3 source checks

The following source pages were independently extracted into temporary scratch
and read. Page numbers below are PDF page numbers. Source hashes are recorded
in `standards-source-hashes.json`; extracted text is not part of this packet.

| Source | Pages | Clauses and checked facts |
| --- | --- | --- |
| Milan v1.2 consolidated, approved 2023-11-30 | 23-24 | 4.2.6.2.2 and Table 4.1 govern message intervals; 4.2.6.2.3 and Table 4.2 govern timeout tolerances; 4.2.6.2.4 governs asCapable |
| Milan v1.2 | 35-39 | 5.3.5.1 sampling-rate persistence; 5.3.7.1 output-format persistence |
| Milan v1.2 | 40-44 | 5.3.7.7 and Table 5.4 output counters; 5.3.8.2/5.3.8.3 binding state; 5.3.8.7 started/stopped state; 5.3.8.10 and Table 5.6 input counters |
| Milan v1.2 | 45-47 | 5.3.9.1/5.3.10.1 channel maps; 5.3.11.1 clock-source persistence; 5.3.13 user-name persistence |
| Milan v1.2 | 72-76 | 5.5.1.4 and 5.5.2.6 Auto Connect; 5.5.2.4 Controller Bind; these are separate restoration and controller-request mechanisms |
| Milan v1.2 | 108-112 | 5.6.2 fixes ENTITY_AVAILABLE valid_time at 10 and the normal advertisement cadence at five seconds; 5.6.3 specifies the advertiser state machine |
| Milan v1.2 | 141 | Annex B.1 media-clock holdover uses five seconds; B.1.1 separately specifies GM-change uncertainty at 0.25 seconds |
| IEEE 1722-2016 | 37 | 4.4.4.6 sequence field and 4.4.4.7 timestamp-uncertainty field are distinct |
| IEEE 1722.1-2021 | 49, 55-58 | 6.2.2.5 expresses valid_time in two-second units; 6.2.4/6.2.5 are advertiser state machines |

Repository and decision interpretation

`hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv:119` implements the
documented 0.25-0.5-second uncertainty hold. `docs/design/GM_LOSS_RECOVERY.md`
states the implementation's minimum reading. The recorded round-3 decision
sets the release rule to the implemented upper bound plus recorded observation
resolution, requires a recorded discontinuity, and keeps media-clock holdover
separate. No RTL was edited.

The standards supply the ADP field value and its units. Measuring a complete
twenty-second post-cut window from T0, without charging off time or pre-cut
advertisement age, is the corrected project release decision. It is not
presented as a separate standards-mandated cold-boot deadline.

The seven-day duration, 200-cut phase mix, thirty-second provisional restoration
ceiling, eight-second default off hold and additional one-second reconnect
check are project policy. #397/#75 supply the future ratification measurements;
this desk work establishes no physical boot or restoration measurement.
