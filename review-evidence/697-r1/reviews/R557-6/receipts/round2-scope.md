https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074721212

[A10] **Import round 2** for [A569] on [tsn-c-stack PR #1](https://github.com/kebag-logic/tsn-c-stack/pull/1). Both reviews are NEGATIVE: [R556-1](https://github.com/kebag-logic/tsn-c-stack/pull/1#issuecomment-6074692175) (3 MINOR) and [R557-1](https://github.com/kebag-logic/tsn-c-stack/pull/1#issuecomment-6074712341) (1 MAJOR, 3 MINOR). Export fidelity, provenance and privacy were judged clean.

1. **R557-1-F1 (MAJOR).** Every baseline and mutation execution must grade a freshly produced, complete report. Delete any old XML before each run, and refuse a missing or partial report. Add a reused-work-directory control: after a genuine catch, an early-`exit(1)` plant must ESCAPE. Fresh and repeated campaigns must still catch all 311 plants.
2. **R556-1-F1.** Give each of the 14 export-introduced killers its assertion's own words, and add a message where none exists (for example `advertise-period-wrong` with "A1 TMR_DELAY"). The inventory or the driver must refuse an empty or generic needle, with a planted table entry.
3. **R556-1-F2 = R557-1-F2.** Base the include boundary on the preprocessor: check each translation unit's dependency output (`-M`) under the real flags against `include/` and the allowed C headers. Base the no-heap check on the built objects' undefined symbols. Add compiling controls for `%:include`, `??=include` and a macro-hidden `malloc`, each refused, plus pass controls.
4. **R557-1-F3.** Reconcile the test inventory and traceability against the GoogleTest binary's own registration (`--gtest_list_tests`), not a column-zero regex. Add indented and multiline negative controls (an unknown requirement ID, and a test with no plant).
5. **R556-1-F3.** Give each cited standard in a clause cell its own link: split `clause` in `docs/requirements.json` per standard and regenerate TRACEABILITY.md.
6. **R557-1-F4: decision.** This import preserves behaviour. Document the inherited ADP input limits (AVTP version 1, a 26-byte frame and `control_data_length` 0 are not discarded) in REQUIREMENTS (ADP-01's wording), PORTING (caller obligations) and DEVIATIONS (clause and rationale), with tests that pin today's behaviour. Do not change the core here. The fix is tracked as [tsn-c-stack #3](https://github.com/kebag-logic/tsn-c-stack/issues/3).
7. **Wording.** Apply R556-1-R1 to R4 exactly. S1 (pin actions to SHAs), S2 (the commit map in `docs/IMPORT.md`) and S3 (regenerate the ratchet) are recommended. For S4, confirm Milan v1.2 5.5.2.3 and 4.3.5.1 against the standard text, or correct the citations.

Commit on `b9b9c20a`, with no rebase or amend. Run every gate, all rc 0. Then post REVIEW READY.

