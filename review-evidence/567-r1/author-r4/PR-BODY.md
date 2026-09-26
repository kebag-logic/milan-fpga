[A335]

## Status

Ready for R327's Round 4 delta review of local head `9143e21a57e6315c7678430cfc45b4a2b7e10c09`.
Target: `567-pp-pin-0922e434` -> `dev`.

## Linked Issue / roles

Closes #567

Executor: [A335] for Round 4; [A332] for Round 3; [A325] and [A330] for Rounds 1 and 2.
Internal reviewer: [R326]. External reviewer: [R327].

## Description

Adopt protocol-processor `0922e43408f891fc0b84a84691df86b4fd0f1c0d` from `990f96526bb89356c963a260ebbdcf2a77e6623a`. This brings in the October MVU waiver, unsupported-command response tests, and the integration parameter inventory and checker.

The first three rounds deliver:

1. Update the processor gitlink, `docs/reference/SUBMODULES.md`, current pin text, generated submodule diagram and PNG manifest, and `CHANGELOG.md`.
2. Re-record `syn/yosys/rom_digests.tsv` through `syn/yosys/ooc.sh --record-rom-digests`. Both new rows have digests identical to the `990f9652` rows. Exact-pin ledger keys require the new rows even though ROM sources and bytes are unchanged.
3. Align the changelog and submodule reference with that recorded result, removing the superseded unchanged-ledger and pending-decision statements.

Processor HDL, parent RTL and VERSION are unchanged. Parent parameter bindings agree with the adopted inventory.

## Round 4

The restore procedure now names the pin of record. Its passing measurement remains explicitly attributed to `990f9652`. The submodule reference states that OOC ledger rows must match the exact recorded pin. That requirement uses two sentences to meet the ten-word style limit. The two superseded PR status statements are removed.

All assigned documentation gates returned 0 at this head, including both CI inventory modes. The remaining old-pin hits are historical records, measurements, retained ledger entries or fixed source permalinks.

This round changes only `tb/verilator/milan_dp/README.md` and `docs/reference/SUBMODULES.md`. R327 reviews the Docs and Conformance delta. Per the assignment, R326-1 remains the ancestor POSITIVE at `54b4c3bbbc8cdea5ced0be29c9226fdf82233b74`. S2 is tracked separately in #571.

## Authoritative references

- [Issue #567](https://github.com/kebag-logic/milan-fpga/issues/567)
- [Accepted ledger decision](https://github.com/kebag-logic/milan-fpga/issues/567#issuecomment-5845149786)
- [Text alignment assignment](https://github.com/kebag-logic/milan-fpga/issues/567#issuecomment-5845274184)
- [Round 4 assignment](https://github.com/kebag-logic/milan-fpga/issues/567#issuecomment-5845507642)
- [R327-1 findings](https://github.com/kebag-logic/milan-fpga/pull/569#issuecomment-5845505218)
- `CONTRIBUTING.md`, `REQUIREMENTS.md` Section 8, and `docs/reference/SUBMODULES.md`

## How to get into the same state

Use the issue branch and confirm the candidate head:

```sh
git switch 567-pp-pin-0922e434
git rev-parse HEAD
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
```

Expected head: `9143e21a57e6315c7678430cfc45b4a2b7e10c09`. Install the locked documentation dependencies in an isolated environment.

## How to validate

```sh
git grep -n 990f965
python3 -B scripts/docs_check.py
python3 -B scripts/check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a
python3 -B scripts/check_doc_style.py
python3 -B scripts/gen_toc.py --check
python3 -B scripts/gen_toc.py --verify-anchors
python3 -B scripts/check_doc_paths.py
git diff --check
git diff --check 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a HEAD
```

Also run `python3 -B scripts/docs_check.py` in a metadata-free archive export of this head, matching the filesystem CI mode. Expect every command to return 0; that mode explicitly skips Git inventory parity.

The [Round 1 evidence](https://github.com/kebag-logic/milan-fpga/issues/567#issuecomment-5845135353) records the processor-shadow, parameter inventory, builder, NVM, documentation and other assigned parent gates. The [Round 2 evidence](https://github.com/kebag-logic/milan-fpga/issues/567#issuecomment-5845257136) records digest equality, normal OOC synthesis and the assigned three-top fast elaboration gate.

## Known limitations / out of scope

- The previously reported builder calibration-report and absent-compiler skips remain explicit; skipped arms supply no passing evidence.
- R327's Round 4 delta review, exact-head hosted evidence, candidate-merge validation and post-merge containment remain pending.
- The change makes no new hardware measurement or full-compliance claim.

## Definition of Done

- [x] Adopt the requested pin and refresh its integration references and diagram.
- [x] Re-record exact-pin ledger rows with identical digest values under the public decision.
- [x] Align the two stale documentation passages with the result.
- [x] Correct the restore procedure and exact-pin ledger wording.
- [x] Record the assigned local gate evidence on the issue.
- [x] Preserve parent RTL and existing interfaces.
- [ ] Publish self-test evidence in a PR comment.
- [ ] Complete internal and external independent review with clean lens coverage.
- [ ] Satisfy required hosted contexts and the full merge bar.
- [ ] Validate the candidate merge result and post-merge containment.
