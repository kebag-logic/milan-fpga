# R346-1 standards citation check (clause headings and page locations only)

Sources: Milan Specification Consolidated v1.2 (Final Approved 2023-11-30),
IEEE 1722-2016, IEEE 1722.1-2021. Only the cited pages were extracted, into an
unpublished scratch area. Printed page numbers are given; no normative text is
reproduced beyond short identifying phrases.

| Citation at head b7b74b8b | Where cited | What the clause is | Result |
|---|---|---|---|
| Milan 5.3.8.10 + Table 5.6 | soak.counter-walk, soak.no-counter-errors, power.counter-walk | Stream Input diagnostic counters (SEQ_NUM_MISMATCH, STREAM_INTERRUPTED, MEDIA_UNLOCKED, lock invariant), pp.36-37 | correct |
| Milan Table 5.4 (5.3.7.7) | soak.counter-walk, power.counter-walk | Stream Output diagnostic counters, pp.32-33 | correct |
| Milan 4.2.6.2.2 / 4.2.6.2.3, Tables 4.1 / 4.2 | soak.gptp-continuity ("prove no asCapable loss") | gPTP message interval tolerances and timeout tolerances, p.16 | mismatched: asCapable is 4.2.6.2.4 (802.1AS 10.2.4.1); no assertion measures the Table 4.1/4.2 tolerances |
| Milan Annex B.1.1 | soak.tu-within-holdover; TESTING.md 6d table | tu set for 0.25 s on a GM change (B.1: 5 s recommended holdover), p.134 | correct (repository precedent names the B.1.1 window "holdover") |
| IEEE 1722-2016 4.4.4.6 / 4.4.4.7 | soak.tu-within-holdover | 4.4.4.6 is the sequence_num field; 4.4.4.7 is the tu field (PDF p.37) | 4.4.4.6 mis-attached: it belongs to the SEQ_NUM_MISMATCH assertion |
| Milan 5.3.5.1, 5.3.7.1, 5.3.8.7, 5.3.11.1, 5.3.13 | power.state-restored | sampling rate, output format, started/stopped, clock source (each "saved in a non-volatile memory and restored after a power cycle"), user names | correct for the future eight-item inventory, but the only item persisted today (stream binding) is 5.3.8.2 (bound state) / 5.3.8.3 (binding parameters), p.34, which is not cited |
| IEEE 1722.1-2021 6.2.6 | power.adp-valid-time | Discovery State Machine (observer side) | imprecise: valid_time is 6.2.2.5 (two-second units, 2..62 s); the advertiser obligation is 6.2.4 / 6.2.5 (Advertising Entity / Interface state machines). Repository precedent also cites 6.2.6 for ADP liveness |
| Milan 5.5.1.4 / 5.5.2.6 (Auto Connect) | power.rebind-bound | Listener re-establishes a bound stream after a power cycle without a controller: waits for the talker's ENTITY_AVAILABLE, then PROBE_TX_COMMAND (pp.65-66, 69) | the cited mechanism does not use CONNECT_RX; the assertion's measured interval (CONNECT_RX success to first valid AVTP) is the controller-bind path (5.5.2.4). See finding F1 |
| Issue #75 bound | power.rebind-bound; REQ-VER-06 | "time from the CONNECT_RX response to the first valid AVTP PDU under one second" (controller reconnect) | quoted correctly; its mapping onto a post-power-cycle automatic rebind is F1 |
| REQUIREMENTS.md REQ-VER-06 row | REQUIREMENTS.md:250-275 | n/a | carries no standards clause citation at all |
