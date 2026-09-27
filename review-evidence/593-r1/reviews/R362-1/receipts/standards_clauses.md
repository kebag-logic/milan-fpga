# R362-1 standards check (short quotations, extracted locally from the licensed PDFs)

| Clause | What it says (short quote or summary) | Used by the head for |
|---|---|---|
| IEEE 1722-2016 4.4.4.3 | mr "is toggled by the Talker each time a media clock restart is needed"; "Once this bit toggles, it shall remain in its new state for a minimum of eight (8) AVTPDUs for a given continuous stream."; streams "deriving timestamps from the CRF stream shall toggle the mr bit if a disruption of the CRF stream occurs or if the mr bit in the CRF stream has been toggled." | allowed cause kinds; per-stream 8-PDU hold; CRF causes scoped to deriving streams |
| IEEE 1722-2016 4.4.4.7 | discontinuities "can be caused by events such as changes in the identity of the gPTP grandmaster clock, changes in the timing source of the grandmaster clock, or other events"; tu "should" be set on a detected discontinuity and reset once gPTP returns to normal | tu discontinuity kinds (GM identity, GM time source, other) |
| Milan v1.2 5.3.7.7 Table 5.4 (Stream Output) | MEDIA_RESET "Incremented at the end of every observation interval during which the 'mr' bit has been toggled"; interval "shall be less than or equal to 1 second"; "Reset to 0 each time the Talker starts streaming." | interval semantics; one-second update lag; (restart reset: see S3) |
| Milan v1.2 Table 5.6 (Stream Input) | MEDIA_RESET incremented per observation interval (at most 1 s) during which mr "was toggled in any of the received Stream Data AVTPDUs" | input counter graded against received toggles |
| Milan v1.2 Annex B.1.1 (informative annex) | "In case of a change of grandmaster, the tu bit shall be set to 1 for the duration of 0.25 seconds." | 0.25 s GM minimum (project reads it as a minimum per the #396 correction) |
| Milan v1.2 Annex B.1.2 | a grandmaster change "shall not result in media clock unlock" when the recovery stream was stable for more than 60 s and all devices agree on the new grandmaster within 5 s | GM change alone never excuses an mr toggle (owner rule is stricter: unconditional) |

Result: every clause the head cites exists and says what the head uses it for. The head restates only what the checks need (REQUIREMENTS.md:262-292; TESTING.md:915-1020).
