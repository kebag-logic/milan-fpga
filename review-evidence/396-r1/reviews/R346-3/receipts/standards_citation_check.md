# R346-3 citation check (delta 24d32d54..8153576a)

Sources: text extracted with `pdftotext -layout` from the Milan v1.2 consolidated specification
(final approved 2023-11-30), IEEE 1722.1-2021 and IEEE 1722-2016 under `$STANDARDS_DIR`, plus the
repository file named. Quotations are the minimum needed to check each cited claim.

| Cited in the head | Claim | Source text | Result |
|---|---|---|---|
| REQUIREMENTS.md:289, :296; TESTING.md:959, :972; `power.adp-valid-time` (torture_campaign.py:3420-3427) | Milan 5.6.2 requires `valid_time=10`, i.e. 20 s | Milan v1.2 5.6.2 "ADPDUs" (p.101-102): "The valid_time field shall be set to 10 in ENTITY_AVAILABLE messages. Note: this results in the requirement that a PAAD-AE shall advertise itself every 5 seconds." | Correct |
| same | two-second units; 6.2.2.5 | IEEE 1722.1-2021 6.2.2.5 "valid_time field": "indicates how long the record will be valid for in two-second increments ... between 2 and 62 seconds, resulting in a valid_time field value of 1 to 31" | Correct. `valid_time=10` gives 20 s |
| same | 6.2.4/6.2.5 and Milan 5.6.3 are the advertiser | IEEE 1722.1-2021 6.2.4 "Advertising Entity State Machine", 6.2.5 "Advertising Interface State Machine"; Milan 5.6.3 "Advertise state machine" | Correct |
| REQUIREMENTS.md:267-270; TESTING.md:926-929; `soak.tu-within-holdover` (:3390-3397) | B.1.1 gives 0.25 s for `tu` on a GM change | Milan v1.2 Annex B.1.1 (p.134, informative annex "Recommended Practices"): "In case of a change of grandmaster, the tu bit shall be set to 1 for the duration of 0.25 seconds." | Clause is correct. The text says "for the duration of", which the head (and the decision) reads as a minimum. See S2 |
| same | B.1's 5 s is media-clock holdover, not a `tu` bound | Milan v1.2 Annex B.1: "This specification recommends a minimum value of 5 seconds holdover time" (media clock free-wheel during a GM change) | Correct |
| REQUIREMENTS.md:267; TESTING.md:926 | IEEE 1722-2016 4.4.4.7 `tu` | IEEE 1722-2016 4.4.4.7 "tu (timestamp uncertain) field": a Talker that detects a gPTP discontinuity should set `tu` | Correct |
| TESTING.md:928; decision 5855515133 item 2 | Clock validity implements 0.25-0.5 s | `hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv:119-122`: "discontinuity holdover in quarter-ticks. 2 => 0.25..0.5 s against the free-running prescaler, so Milan v1.2 Annex B.1.1's 0.25 s minimum holds whatever the phase of the event." with `HOLD_QTICK_P = 2` | Correct, lines as cited |
| REQUIREMENTS.md:285-286; TESTING.md:936; plan `power_off_hold_origin` | 8 s default follows `phys.dut-cycle.power-cycle` | `tb/tools/torture_campaign.py:3229-3241`: step `phys.dut-cycle.power-cycle`, `"off_s": 8`, "off for at least 8 s" | Correct |
