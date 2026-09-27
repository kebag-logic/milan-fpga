# R346-2 standards citation check at 24d32d549fa7470318a93984403a92423a63fa25

Sources, extracted locally into an unpublished scratch area with `pdftotext -layout`:
Milan Specification Consolidated v1.2 (Final Approved 2023-11-30), IEEE 1722-2016,
IEEE 1722.1-2021. Only short identifying phrases are quoted here.

| Citation at head | Where cited | What the clause is (extracted) | Result |
|---|---|---|---|
| Milan 5.3.7.7 / Table 5.4 | REQ-VER-06 "Counter authority"; TESTING 6d soak table; soak/power counter-walk | "For each Stream Output ... counters in Table 5.4" (p.32-33) | correct |
| Milan 5.3.8.10 / Table 5.6 | same; soak.no-counter-errors | "For each Stream Input ... counters in Table 5.6"; Table 5.6 lists STREAM_INTERRUPTED and SEQ_NUM_MISMATCH (p.36-37) | correct |
| IEEE 1722-2016 4.4.4.6 | REQ-VER-06 "Sequence authority"; soak.no-counter-errors; TESTING table | "sequence_num field ... Listeners can use the sequence number to detect AVTPDUs lost" | correct (round-1 mis-attachment removed from the tu assertion) |
| IEEE 1722-2016 4.4.4.7 | REQ-VER-06 "Uncertainty authority"; soak.tu-within-holdover | "tu (timestamp uncertain) field" | correct |
| Milan Annex B.1 / B.1.1 | same | B.1 "recommends a minimum value of 5 seconds holdover time"; B.1.1 "tu bit shall be set to 1 for the duration of 0.25 seconds" (p.134) | correct, and the head now states both values distinctly |
| Milan 4.2.6.2.4 | REQ-VER-06 "asCapable authority"; soak.gptp-continuity; TESTING table | "asCapable (as defined in [802.1AS, Clause 10.2.4.1])" | correct (Table 4.1/4.2 citation removed) |
| Milan 5.3.8.2 / 5.3.8.3 | REQ-VER-06 "Binding authority"; power.state-restored | "current bound state shall be saved in a non-volatile memory"; binding parameters saved in non-volatile memory | correct; the enforced item is now anchored |
| Milan 5.3.5.1, 5.3.7.1, 5.3.7.6, 5.3.8.1, 5.3.8.7, 5.3.9.1, 5.3.10.1, 5.3.11.1, 5.3.13 | REQ-VER-06 "Remaining authority"; power.state-restored | each carries "saved in a non-volatile memory and restored after a power cycle" (sampling rate, output format, presentation time offset, input format, started/stopped, output/input channel maps, clock source, user names) | correct; together with 5.3.8.2/.3 this is every Milan 5.3 persistence clause found by a full-text search for "non-volatile" |
| IEEE 1722.1-2021 6.2.2.5 | REQ-VER-06 "ADP authority"; power.adp-valid-time; TESTING 6d | "how long the record will be valid for in two-second increments" (values 1..31, 2..62 s) | correct; the plan's `adp_valid_time_unit_s=2` matches |
| IEEE 1722.1-2021 6.2.4 / 6.2.5 | same | Advertising Entity / Advertising Interface state machines | correct |
| Milan 5.6.3 | same ("defines the profile's advertiser") | Advertise state machine | correct as phrased, and it is the clause the recorded decision names. The Milan value itself, "valid_time field shall be set to 10" (20 s; advertise every 5 s), is in 5.6.2 (p.101), which is not cited (Suggestion S1) |
| Milan 5.5.1.4 / 5.5.2.6 | REQ-VER-06 "Auto Connect authority"; power.automatic-restore-bound | listener re-establishes a bound stream after a power cycle without a controller (waits for ENTITY_AVAILABLE, then probes) | correct; now attached to the automatic-restoration bound |
| Milan 5.5.2.4 | REQ-VER-06 "Controller Bind authority"; power.rebind-bound | Controller Bind (BIND_RX_COMMAND, Milan's name for the controller connect) | correct; now attached to the controller reconnect check |
| Issue #75 | power.rebind-bound; REQ-VER-06 | CONNECT_RX response to first valid AVTP under one second | quoted correctly as the additional check the decision records |
