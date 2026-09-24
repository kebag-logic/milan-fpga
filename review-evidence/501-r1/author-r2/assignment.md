[A10] Round 2 assignment for PR #557, covering R312-1 (F1-F3) and R313-1 (F1-F4). Executor [A288].

1. **Writer framing: R312-1 F1 = R313-1 F1 (MAJOR).** In `SAVED_STATE_MATERIALIZATION.md`, the map-record framing rule (about :940-941) and the writer parameter row (about :444) state an output record's capacity as the section 4.2 per-port entry count, or refer to section 4.2. Input records keep their cluster count. Remove the stale "stage 3 BLOCKED on #501" status (about :1641-1654). No saved-state page may size an output map record by cluster count.
2. **Stale figures: R312-1 F3 = R313-1 F2.** Every current-state 8x8 figure the reviewers list must carry the value the head's gate derives, or cite the section 4.2 derivation: image bytes and slot share, DRAM window, BRAM36 count, the 9.4 deadline row and margin, the stage container in SNAPSHOT_OWNERSHIP, and `BAREMETAL_FIRMWARE.md:1375` wording for the entry constants. Correct the pre-existing stale 1x1 figures in the same sentences. Historical rows that say they are historical stay.
3. **Capture hold: R312-1 F2 = R313-1 F3. Manager decision: option (b), no RTL change in this PR.**
   - Re-derive the section 18 copy budget at the grown 8x8 area with the page's own model, and publish nominal and 2x figures and margins (1.57x and 0.78x).
   - State the 8x8 exposure: safety holds through void and retry, and liveness under sustained producer activity is at risk.
   - Record that the shipping 1x1 shape is unchanged.
   - Make hold sizing a measured acceptance obligation of the donor writer adoption (processor #61/#83), because maps are not materialized yet (only BINDING is), so no map copy exists to overrun today. UNRESOLVED 6 carries the head figures and this obligation.
   - The manager records the obligation on the donor issue.
4. **Self-test: R313-1 F4.** Every control must produce its named finding or refusal line, and a control that crashes must fail `--self-test`. Show the reviewer's crash probe making `--self-test` fail.
5. **Suggestions:** take R313-1 S1 (name `nvm_cosim` as the instrument that kills a wrong firmware output-length table, or add a host-test check) and S2 (remove the unreachable guard) if cheap.

Gates: as in round 1. Review: delta reviews at the new head by [R312] and [R313].

