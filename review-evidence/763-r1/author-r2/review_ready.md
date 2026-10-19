[A653] REVIEW READY
Commit: `07c6c72fce79e705bcf28a70071497d0ce7040e4` (branch `763-map-persist`, two commits on dev `e9cbb676`; not pushed, as the assignment requires)
Changed (Round B, option B of the ruling):
- `sw/firmware/ctrl/test/test_aecp.cpp`: new `Nvm.EmptyAndNonDefaultMapsSurviveTheRealStorePowerCycle`, run once per direction. REMOVE_AUDIO_MAPPINGS (IEEE 1722.1-2021 7.4.46) empties port 0 and removes one row from the other direction's port 0. The test commits through the real store and checks that the empty set is a framed record (magic `0x1722`) whose entries are all UNUSED. After a power cycle of the flash model, the emptied list must come back empty and the non-default list must come back as saved (Milan v1.2 5.3.9.1, 5.3.10.1).
- `sw/firmware/ctrl/test/aecp_mutants.py`: two named mutants. `nvm-empty-map-keeps-defaults` plants "`count == 0` keeps the defaults" in `aecp_nvm.c`. `nvm-unused-payload-reads-erased` plants "an all-`0xFF` payload reads as erased" at `nvm_store.c:298`. The campaign now copies the store beside its firmware copy so that the second mutant can be planted.
- `sw/firmware/ctrl/test/aecp_arms.py`: the saved-state arm compiles the store from the tree's sibling `ctrl_nvm/`. That is the same directory for the checkout and the planted copy for the campaign.
- `sw/firmware/ctrl/aecp/README.md`: documents both changes.
- No firmware source, record format, saved-state layout or RTL changed.

Validation (CPython 3.12.3, pinned RV32 SDK, pinned Verilator 5.050), all rc 0:
- `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test`: `test_ctrl_firmware: PASS`, 939 planted controls caught, none escaped, both new mutants `[ok]`.
- `python3 sw/firmware/ctrl/test/test_ctrl_firmware_shards.py`
- `python3 sw/firmware/gtest/tally_selftest.py`
- `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32`
- `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4`: 435 tests over 5 shapes.
- `python3 sw/firmware/gtest/fw_coverage.py --selftest` and `--check --jobs 4`: the ratchet is unchanged.
- `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator` and `--only verilator`
- `python3 scripts/docs_check.py`, `check_feature_status.py`, `check_doc_style.py` (and `--selftest`), `gen_toc.py --selftest/--verify-anchors/--check`, and `check_em_dash.py --base e9cbb676`

Acceptance criteria (narrowed #763):
- Met: an empty list in both directions and a non-default list survive the store's power-cycle path, and the empty set is a framed record of UNUSED entries.
- Met: both plants are named mutants, and each fails the new test on its own diagnostic.
- Gap closed: with the new test excluded, the store plant passes all 73 other AECP app-arm tests and all six store suite binaries. No record-format change.
- Moved to #637 by the ruling: the on-board cold cycle.

Open risks/questions: `ci/image/tool-inventory.json` `--check` already exits 2 on dev `e9cbb676` (two unrelated script digests). This lane adds two more input digests to it (`aecp_arms.py`, `aecp_mutants.py`). That check runs in the CI image build, not in a pull-request workflow. I did not regenerate it, because that would fold unrelated drift into this lane. It is left to the inventory's owner.

Receipts, the handoff and the PR body are in the lane's output directory, with an index generated from the files present.
