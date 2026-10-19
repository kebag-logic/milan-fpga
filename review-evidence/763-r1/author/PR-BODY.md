[A653]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN locally at `07c6c72f`: every gate the change touches exits 0. That includes the full firmware bank with
`--self-test` (939 planted controls caught, none escaped), the store suites (435 tests over 5 shapes), the coverage
ratchet (unchanged), both TSN stack boundary halves, and the docs gates. `763-map-persist` -> `dev`, two commits, not
yet pushed.

## Linked Issue / roles

Closes #763
Relates to #637

Round B: #763 closes on its narrowed scope (option B of the ruling on #763). Its board acceptance, an empty list
and a non-default list surviving a cold cycle on the board, moved to #637. #637 owns the channel-map record writer
and restore.

Executor: `[A653]`
Internal cleared-context reviewer: to be assigned
External reviewer: to be assigned

## Description

#763 reported that an emptied dynamic mapping list comes back with its defaults after a power cycle. Round A of the
lane found two things:

- **On the board**, the cause is that nothing in the shipping build writes the channel-map records (#637).
- **In the firmware**, the AECP owner and the store already keep an empty list. But one of the two ways the store
  could lose it, reading a framed all-UNUSED payload as erased, failed no in-tree test. Neither the AECP suites nor
  the store's own suites caught it.

This PR closes that test gap. It changes no firmware source and no record format.

| Piece | Change |
|---|---|
| `sw/firmware/ctrl/test/test_aecp.cpp` | New `Nvm.EmptyAndNonDefaultMapsSurviveTheRealStorePowerCycle`, run once per direction. REMOVE_AUDIO_MAPPINGS empties port 0 in that direction and removes one row from port 0 in the other. The test commits through the real store and checks that the empty set is a framed record (magic `0x1722`) whose entries are all UNUSED. It then restores defaults, power-cycles the flash model and boots. The emptied list must come back empty, and the other list must come back with exactly its saved rows. |
| `sw/firmware/ctrl/test/aecp_mutants.py` | Two named defects. `nvm-empty-map-keeps-defaults` plants "`count == 0` keeps the defaults" in `aecp_nvm.c`. `nvm-unused-payload-reads-erased` plants "an all-`0xFF` payload reads as erased" in the record walk of `nvm_store.c`. Each must fail the new test on its own diagnostic, and the first must also fail `Nvm.WholeMapFramingAndEmptySetAreDistinct`. The campaign now copies the saved-state store beside its copy of the firmware tree, so that a store defect can be planted there. |
| `sw/firmware/ctrl/test/aecp_arms.py` | The saved-state arm compiles the store from the tree's sibling `ctrl_nvm/`. For the checkout that is the same directory as before. For the campaign it is the planted copy. |
| `sw/firmware/ctrl/aecp/README.md` | States the empty-map persistence rule and the campaign's store copy. |

Planted-defect evidence:

| Defect | Caught by | Without the new test |
|---|---|---|
| `nvm-empty-map-keeps-defaults` | the new test and `Nvm.WholeMapFramingAndEmptySetAreDistinct` | the second test still fails |
| `nvm-unused-payload-reads-erased` | the new test | escapes: the 73 other AECP app-arm tests pass, and so do all six store suite binaries |

## Authoritative references

- Milan v1.2 5.3.9.1 and 5.3.10.1: the output and input channel-mapping lists are saved in non-volatile memory and
  restored after a power cycle.
- IEEE 1722.1-2021 7.4.46 (REMOVE_AUDIO_MAPPINGS), the edit the test applies.
- docs/design/SAVED_STATE_FASTCONNECT.md section 6.1, the erased-record rule: an erased record is its whole span,
  header included, filled with `0xFF`.
- docs/design/SAVED_STATE_MATERIALIZATION.md section 8.3, case V3g: an empty set is a framed record of UNUSED entries.
- #70, #637, and the ruling on #763.

## How to get into the same state

```sh
git fetch origin
git switch 763-map-persist
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
python3 -m pip install pyyaml -r sw/litex/litex_pins.txt
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
```

Install GoogleTest, GoogleMock and the pinned RV32 SDK as the `firmware-unit` job does. Set `VERILATOR` to the
pinned Verilator for the `--only verilator` boundary run.

## How to validate

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test
python3 sw/firmware/ctrl/test/test_ctrl_firmware_shards.py
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator
python3 scripts/docs_check.py
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
```

Expected result / pass criteria: every command exits 0. The firmware gate prints
`[ok] nvm-empty-map-keeps-defaults` and `[ok] nvm-unused-payload-reads-erased`, and it ends with
`test_ctrl_firmware: PASS`. The coverage ratchet is unchanged.

## Known limitations / out of scope

- The board symptom is not fixed here. The parent channel-map record writer and restore belong to #637, and so does
  #763's cold-cycle board acceptance.
- No record format, firmware source or saved-state layout changed, so records written by the shipping image read
  exactly as before.
- `ci/image/tool-inventory.json` records the digests of `aecp_arms.py` and `aecp_mutants.py`. That file is already
  out of date on `dev` for two unrelated scripts. Its `--check` runs in the CI image build, not in a pull-request
  workflow. Regenerating it here would fold that unrelated drift into this PR, so this PR leaves it to the
  inventory's owner.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
