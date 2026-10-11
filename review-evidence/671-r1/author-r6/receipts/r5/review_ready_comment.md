[A592] REVIEW READY (round 5)
Commit: 0c276b621d638c9a83e82f71fbf07bc153517bf7 on `671-read-fault`: five new commits on `7bc7ceca`. No push, rebase or amend.

Answers [the round-5 assignment](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6107082416), R603-4 (F1) and R602-4:

- **F1 is fixed.** Refused reads are now compared by verdict, byte count, a CRC-32 over all but the last four bytes, and those four bytes whole. Over a container whose CRC closes, the old whole-read CRC was always the residue `0x2144df1c`. The new comparison equals for two such containers only on a genuine prefix CRC collision, and it also catches a trailer-only difference. The three-read bound, validated-only generation, fallback and hold are unchanged.
- **The class is in the standing suite.** A new `--read-sealed` harness fault flips the entity byte or a record-area byte and recloses the CRC, so every faulty read is a different refused container (`VD_ENT` or `VD_REC`). It runs over every generated window. The generator also adds R603-4's exact pattern at every sequence boundary, both orientations and both entry paths: two sealed refusals opening a judgement, then a clean read. All 24 combinations are covered. That makes 3,422 cases per shape (1,775 cold, 1,647 restart).
- **New control `r_digest_with_trailer`** restores round 4's digest and agreement. It fails by name ("on reads that returned different bytes") on arty 4x4, 1x1 and 8x8, with 180 named findings each in full count. All 14 #671 controls fail by name on all three shapes.
- **R603-4's probe.** Unmodified, it now fails its own defect assertion. A copy that records all four cases reports DEFECT GONE on every case (change kept, 0 records lost). With the control planted, the same copy reproduces R603-4's 53 / 163 records lost.
- **Found and fixed: the hosted `docs-check` at `7bc7ceca` failed.** Its builder step killed the writer gate at 1,200 s (run 38120473372). The host model's `settle()` now skips its 1,024-word CSR walk after one `memcmp` when nothing was stored. 10,581 twin runs over three shapes show no difference in any transcript or dumped file. Locally the gate takes 267.29 s with 3,422 cases (round 4: 461.48 s with 2,158). The builder limit is still 1,200 s; the hosted result at the new head needs checking.
- **Item 2: `sw/firmware/ctrl_nvm` has the same collapse, and it is wider.** `nvm_store.c:142-149,165-173,208-216` chains the digest over the separate 40-byte header read and the whole-container read. For any CRC-clean container, only the header read and the length count. Driven on its host model with two sealed reads of slot A, the unchanged store keeps the refusal (`read_faults=0`, not held) and commits seq 1 to B; the clean reboot prefers A, so the acknowledged commit is lost, on 1x1 and 8x8. Its README overstates the digest's detection limit. Not changed here; it is reported for filing.
- **Docs:** `BAREMETAL_FIRMWARE.md` and FASTCONNECT section 7 state the comparison exactly, why the trailer is excluded, and its detection limit. The host README covers the sealed faults, the class, the counts and the control.

**Validation:** all executed gates return zero, except the unmodified reviewer probe, which exits 1 by failing its own defect assertion, as intended.

- Writer gate: five shapes, 49 controls, at the final source head.
- Full-count controls on three shapes, and the class coverage check.
- All 101 builder functions with every elaboration arm (part 6 rerun at the final source head).
- Co-simulation 465/465 with 39/39 mutants, and the service budget.
- Firmware-unit 7/7 (Mark II store 435 tests), lint/BDD 5/5, and the 78 runnable docs-check positions.
- Feature-status, record-space, idiom, hygiene, em-dash and diff checks.

**Capture re-measured:** six arms, 96 clean captures, firmware sha256 `497845e6243b919638285ce4de18e6687beff6a509d72c8e2e2f2d45ba7b1bed`. The 8x8 contract maximum is 13.86328 ms against 24.5 ms (10.63672 ms margin, 3.5345x floor), unchanged. 1x1 is 3.96548 ms; the non-contract 100 MHz figure is 10.42973 ms. The receipt gate passes, and its four mutation controls reject.

**Firmware size** with the pinned RV32 SDK: text 17,579 B (+96 this round, +2,050 over base), bss 104 B (unchanged, +16 over base), data 104 B.

Acceptance items 1–3 are met in the recorded tests. There is no RTL, register-map, record-format, gitlink or A/B write-path change. The processor stays at its pin. R602-4-S1 and S2 (optional) are not taken up. Prefill remains #717.

HANDOFF.md and PR-BODY.md have Round 5 sections. The working tree is clean. No STOP condition arose. The head is local: exact-head hosted and act evidence, independent re-review and merge-candidate validation remain. No merge is authorized or performed.
