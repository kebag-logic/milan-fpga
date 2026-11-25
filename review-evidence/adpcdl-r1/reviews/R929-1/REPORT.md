[R929] NEGATIVE - exact head e0b144904e57c96928f1dd3fca36a00df42f6ed3

Round R929-1, issue kebag-logic/tsn-c-stack#37, PR #38. Tree `2b5890f3cbb82b2415f7fa50151db3acc550e282`, base `69bac7cd52815d2ae223a5a3aa6d022a1f1d35de`.

The behaviour, the clause citations and the consumer patch are correct. One MINOR test defect is open (F1), so the verdict is NEGATIVE. This PR had no earlier public findings: no reviews, and no comment except the review start.

## What was checked

- **Scope.** `src/` changes by one comparison (`!=` to `<`) and one tracing comment. `include/` and `examples/` are unchanged. Transmit still writes 56 (`src/adp.c:107`) and the 82-octet check is unchanged (`src/adp.c:311`).
- **Clauses, read in the standards.**
  - IEEE 1722.1-2021 6.2.2.6: the field is the length in octets after entity_id, "set to 56".
  - IEEE 1722.1-2021 6.2.7.1.3: rcvdDiscover depends on message_type, with no length condition.
  - Milan v1.2 5.6.3.1: entity_id is the only discard reason. Table 5.50 defines RCV_ADP_DISCOVER by entity_id alone.
  - IEEE 1722-2016 4.4.5.4: the field is the control_data_payload length. It has no receive rule, unlike 4.4.3.4 for an unsupported version.
  - The two analogies in the PR body hold: Milan 5.5.2.2 and IEEE 1722.1-2021 7.4.37.1.
- **Accept/refuse rule, every receive state.** `scripts/differential.cpp` drives the old and new cores with the same frames, under address and undefined-behaviour sanitizers, in exact-size heap buffers: 5 states, 4 targets, 14 buffer lengths, 4 valid_time values. 5,344,320 frames: 0 differences, where a length above 56 must behave as the old core does at 56. 398,200 long discovers were accepted, none was discarded, and no length below 56 was accepted (`receipts/differential.txt`). No other ADP behaviour changed in this set.
- **Plants and tests.** The full child campaign caught 484 of 484, the six new ones included (`receipts/mutation-full.txt`). On the old core, exactly the five `AcceptsLongControlDataLength` instances fail and 39 tests pass (`receipts/red-run.txt`). Mask changes that widen the field into valid_time, and the bound plants, are caught. Narrowing it is not (F1).
- **Coverage, targets, generated tables.** ctest 10 of 10; `src/adp.c` 100 % lines and branches after the existing exclusions (`receipts/coverage-and-ctest.txt`). Bare-metal rc 0; its Release ELF hash equals the published one, and its Debug ELF hash differs (cause not investigated). The traceability and test-inventory checks pass, so TESTS and TRACEABILITY match their generators. Other child gates run here are rc 0 (`receipts/static-gates.txt`).
- **Consumer.** `parent-consumer.patch` applies to 5de21ff3, and its apply check passes on dev e275d795. With this core at 5de21ff3, the unmodified adp arm fails 1 of 63 checks. With the patch it passes 64 of 64, and the six `pin-adp-*` plants and `foreign-discover-answered` are caught (`receipts/consumer-adp-patched.txt`, `consumer-adp-unmodified.txt`). `KL_mbx_rx.sv` and `KL_ctrl_split.sv` contain no control_data_length use. The channel limit is 128 octets, so 102 is the largest length with its surplus present, as the parent text says.
- **Hosted, exact head.** Both runs concluded success: quality and bare-metal, executed jobs and not skipped contexts. The quality log I read shows all 28 steps at rc 0.
- **Comment, label and privacy scan.** The added lines carry no bench lane label, reviewer ID, round or test-plan reference. The commit message is one line with no trailer.

## Findings

### F1 - MINOR - Tests - the upper bits of the 11-bit field lost their test; defects the base suite caught now survive
- **Where.** `tests/test_adp.cpp:817-830` (`AcceptsLongControlDataLength`), lengths 57, 84 and 2047 only. `tests/mutations.json` has no plant that narrows the field.
- **Evidence.** With the head's tests, a core reading the length through mask 0x03FF, 0x01FF, 0x00FF or 0x007F, or from the low octet only, survives (`receipts/own-mutants-head.txt`). 57 and 84 fit in seven bits, and 2047 has every bit set. Such cores wrongly refuse conforming lengths: 256 under 0x00FF, 0x007F or the low octet, 512 under 0x01FF, 1024 under 0x03FF. The base tests caught all five (`receipts/own-mutants-base.txt`), because `RejectsWrongControlDataLength` swept 0 to 2047. At the consumer, with the patch, 0x00FF also survives.
- **Impact.** The documents state an 11-bit value of at least 56. A core that reads part of it refuses long discovers, the defect #37 removes, and the suite stays green. The lengths listed in the issue are met, but the scope rule "56 or more is processed" is sampled too thinly, and the PR loses sensitivity the base had.
- **Authority.** Issue #37 scope and acceptance 2 (one planted defect per rule); ADP-01; CONTRIBUTING ("a regression needs a failing assertion and a runnable planted defect").
- **Required outcome.** Test accepted lengths above 127 whose low bits are below 56, for example a sweep of 57 to 2047 with the surplus absent. Add a caught plant that narrows the mask, for example 0x00FF. Update the counts in `docs/VERIFICATION.md` and regenerate the tables.
- **Verification.** Run `scripts/own_mutants.py TREE WORK '<'` on the fixed tree: every entry except `control-unmutated` must be caught. A trial sweep does that (`receipts/own-mutants-full-sweep.txt`); all five accept instances took about 84 ms.

### F2 - RESIDUE - Docs - the change is not linked to issue #37
- **Where.** `CHANGELOG.md:5`; the last line of "ADP input validation" in `docs/REQUIREMENTS.md`.
- **Evidence.** The section credits only issue 3, whose assignment asked to refuse any length other than the 6.2 value. Issue #37 replaces that part.
- **Exact fix.** Append to the section: "[Issue 37](https://github.com/kebag-logic/tsn-c-stack/issues/37) replaced the exact-length rule of issue 3: a value above 56 is read by its first 56 octets." Add the same issue link to the change log entry. No behaviour or clause claim changes.

### F3 - SUGGESTION - Tests, Docs - RV32 smoke has no long-length control
`examples/rv32/smoke.c:147-182` covers lengths 0 and 56 only. `docs/REQUIREMENTS.md` says the hosted controls and the RV32 smoke checks "cover these rules", which is true of the two together only. A further control with a long length would cover it on RV32.

### F4 - SUGGESTION - Tests - consumer patch
`PinAcceptsLongDiscoveryThroughMailbox` uses 57, 84 and 102. A frame of 82 octets with length 2047 also reaches the core, and the old test held 2047. Adding 256 and 2047 with the surplus absent would close F1 at the consumer too. Carry it with the pin bump.

### F5 - SUGGESTION - Docs - published evidence packet
`HANDOFF.md`, `REVIEW-READY.md` and `red-run-old-core.log` still contain a host scratch path, though the manifest marks `HANDOFF.md` as path-redacted. Outside the PR's diff; for the manager to judge.

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | cited clauses in IEEE 1722.1-2021, Milan v1.2 and IEEE 1722-2016; ADP-01; `src/adp.c`; differential probe | R929-1 | e0b144904e57c96928f1dd3fca36a00df42f6ed3 |
| RTL | CLEAN | no RTL in the delta; `KL_mbx_rx.sv` and `KL_ctrl_split.sv` at 5de21ff3, read by text search, not simulated | R929-1 | e0b144904e57c96928f1dd3fca36a00df42f6ed3 |
| Robustness | CLEAN | differential probe under sanitizers, exact-size buffers from 0 to 2073 octets, RV32 bare-metal build and smoke | R929-1 | e0b144904e57c96928f1dd3fca36a00df42f6ed3 |
| Tests | UNCLEAN (F1) | split tests, six plants, 484-plant campaign, coverage, red run, own mutants on head and base, consumer arm and plants | R929-1 | e0b144904e57c96928f1dd3fca36a00df42f6ed3 |
| Docs | CLEAN (F2 is RESIDUE) | REQUIREMENTS, requirements.json, PORTING, VERIFICATION, CHANGELOG; TESTS and TRACEABILITY against their generators; PR body, issue, author packet | R929-1 | e0b144904e57c96928f1dd3fca36a00df42f6ed3 |

## Limits

- No manager source bank ran at this head, and none is claimed. Source-head execution evidence is the author's published gate receipts; the runs here are focused reproductions.
- Not repeated here: the sanitizer build of the suite, static-analysis, assertion-templates, dependencies, acmp-cache, mutation-controls, entity gates and graphs. The hosted job ran them at this head.
- The differential probe covers every length 0 to 2047 only for octet-15 values 0x02 and 0x82, and the 12 buffer lengths other than 82 and 128 only for 0x02. Other octet-15 values use a step of 31, at buffer lengths 82 and 128.
- Not run: the complete parent firmware gate, the other consumer arms, the parent stack boundary gate, RTL simulation. The author's statement about `KL_pp_rx_validator.sv` was not checked. Physical calibration NOT RUN; field skips are not hardware proof.
- The refusal of lengths below 56 is the issue's decision. The cited clauses neither require nor forbid it.
- The consumer runs used a disposable clone with its partial-clone settings removed, because the gitlink proof refuses them.
- At the end the review clone is unmodified: head and tree as above, empty status. The repository has no submodule gitlinks. Probes ran only in disposable copies.

## Pending manager duties

1. Route F1 to the author. F2 goes to the residue checklist.
2. Build and validate the current-dev merge candidate at the merge turn.
3. Apply the consumer patch with the pin bump and its gates; consider F4.
4. Judge F5.

R929-1 FINISHED
