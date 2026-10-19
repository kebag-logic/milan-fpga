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

BLOCKED on a decision (Round 2 STOP, below). `763-map-persist` -> `dev`, two commits at published head `07c6c72f`.

Locally at `07c6c72f`, every firmware and docs gate exits 0. That covers the full firmware bank with `--self-test`
(`test_ctrl_firmware: PASS`: 876 source-mutant executions caught and 2 pin-refusal controls passed; 61 normal arm
outcomes passed; 939 top-level `[ok]` lines), plus the store suites (435 tests over 5 shapes), the coverage ratchet
(unchanged), both TSN stack boundary halves, and the docs gates. The CI tool-inventory refresh (R658-1-F1,
R657-1-F1) is generated and verified but not committed. Committing it makes the image-lock recipe check refuse,
which needs a decision.

## Linked Issue / roles

Relates to #763
Relates to #637

Round B: #763 is to close on its narrowed scope (option B of the ruling on #763). Until the Round 2 decision
lands, its "every touched gate rc 0" item is not met, so this PR only relates to #763 for now. Its board acceptance, an empty list
and a non-default list surviving a cold cycle on the board, moved to #637. #637 owns the channel-map record writer
and restore.

Executor: `[A653]`
Internal cleared-context reviewer: `[R657]` (review R657-1, started in PR #766 comment 6258585761)
External reviewer: `[R658]` (review R658-1, started in PR #766 comment 6258590845)

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
- `ci/image/tool-inventory.json` still records the base digests of `aecp_arms.py` and `aecp_mutants.py`, and of
  two scripts that went stale on `dev` before this lane. The refresh is ready but is held for the Round 2 decision.
- `ci/image/exec-audit-receipt.json` records the base digests of the same two AECP scripts. It is a committed
  observation of one traced run inside the image, and this PR does not re-run that audit.

## Round 2

Answers R658-1 (PR #766 comment 6258733493) and R657-1 (PR #766 comment 6259255660), as assigned in PR #766
comment 6259259419. No new commit: the head is still `07c6c72f`.

| Finding | Outcome |
|---|---|
| R658-1-F1, R657-1-F1 (inventory digests) | STOP for a decision. `python3 scripts/ci_tool_inventory.py --write` with the pinned parser changes four `inputs` rows and nothing else (same `tools`, `residue` and schema). Two rows are this lane's: `aecp_arms.py` and `aecp_mutants.py`. Two are inherited: `scripts/check_doc_style.py` (stale since PR #753) and `scripts/measure_test_evidence_readers.py` (stale since PR #754). The generator rewrites all four in one refresh. Afterwards `--check` exits 0 (2 at the head), and the eight inventory and image self-tests exit 0. But `tool-inventory.json` is a recipe input of the CI image. The recipe digest moves from `712f7b38` to `1e5e36f7`, so `python3 ci/image/build.py --work <dir> --check-lock` goes from 0 to 2 ("image lock does not describe the current recipe"). On `dev`, each earlier inventory regeneration was followed by a lock re-record from two cold image builds (for example `f1c041bc` and then `54fbcba6`). |
| R658-1-F2 (count) | Corrected. Classified from the gate log against the AECP and SRP tables at the head: 520 control-source, 78 AECP and 278 SRP source-mutant executions (876 caught), 2 dependency-pin refusal controls, and 61 normal arm outcomes, for 939 top-level `[ok]` lines. The earlier "939 planted controls caught" overstated the planted controls. |
| R658-1-F3, R657-1-R1 (status and roles) | Applied above. |

To reproduce the F1 measurement, set `IMAGE_WORK` to an empty directory outside the checkout, then run:

```sh
python3 ci/image/prepare_parser.py --output "$IMAGE_WORK/shfmt"
export CI_IMAGE_SHFMT="$IMAGE_WORK/shfmt"
python3 scripts/ci_tool_inventory.py --check
python3 ci/image/build.py --work "$IMAGE_WORK" --check-lock
python3 scripts/ci_tool_inventory.py --write
git diff --stat
python3 scripts/ci_tool_inventory.py --check
python3 ci/image/build.py --work "$IMAGE_WORK" --check-lock
git checkout -- ci/image/tool-inventory.json
```

The first pair exits 2 and 0. After `--write`, the diff is `ci/image/tool-inventory.json`, 4 insertions and
4 deletions, and the second pair exits 0 and 2.

Decision needed on F1, one of:

- **(a) Recommended.** Commit the refresh here as one generator-output commit. The image owner then re-records
  `ci/image/image.lock.json` through the documented build (`build.py --no-cache --defer-lock`, then
  `--record-lock`) on or before the merge candidate. The last re-record changed only `recipe_digest`.
- **(b)** Commit the refresh, and re-record the lock in this lane. That means two cold builds of every image
  layer on this host, far beyond this PR's four-file delta.
- **(c)** Leave the refresh out of this PR. A public decision assigns all four rows to the inventory's owner,
  with a tracking issue.

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
