# [A849] ADP control_data_length above 56 (tsn-c-stack)

**Status: DONE, committed, not pushed.** Head `e0b144904e57c96928f1dd3fca36a00df42f6ed3` (tree `2b5890f3`), branch `adp-long-discover`, base `69bac7c`. ETA: none left in this lane.

## Change
- `src/adp.c:314`: `!= ADP_CONTROL_DATA_LENGTH` became `<`; `:309` one tracing comment. The 82-octet frame check (`:311`) and transmit (56) are untouched.
- ADP-01 in `docs/requirements.json` and `docs/REQUIREMENTS.md`, `docs/PORTING.md` (ADP input validation), `docs/VERIFICATION.md` (475 -> 480 core plants), `CHANGELOG.md`; `docs/TRACEABILITY.md` and `docs/TESTS.md` by their generators.
- `tests/test_adp.cpp`: the split test plus the `accepted_discovery` helper, taken from `ValidDiscovery` with its assertions unchanged. `tests/mutations.json`: 1 plant removed, 6 added.
- Beyond the brief: the short test sweeps 0..55 and the long one adds 2047 (the old test swept the whole field); both also set valid_time 31, because without the 0x07FF mask `<` would accept a short discover.

## Consumer (milan-fpga worktree at 5de21ff3, left clean at its own pin)
- The index gitlink was staged at the new head for the runs, then restored; nothing committed there.
- Unmodified parent tests: 1 of the `adp` arm's tests fails, `AdpAdapter.PinRejectsWrongDiscoveryControlLength` (it expects 57 and 2047 refused). This is the change itself.
- `receipts/parent-consumer.patch` adapts it and the two plants. With it: adp, port, walk, acmp, acmpif2, unit, reentry_debug, reentry_release, portable, rv32, hot, entity and service_bounds pass; C++ and Python idiom checks pass; with the full table no test is unnamed.
- consumer-plants.log ends rc 1 with "141 test(s) named by no defect": an artefact of planting only 11 of the 846 entries. All 11 are caught.
- Filters: `KL_mbx_rx.sv` and `KL_ctrl_split.sv` never read octets 16-17 and are unedited.

## For the manager
1. **128-octet bound.** The mailbox's `adp` channel has `max_frame_bytes: 128`: a discover whose frame is above 128 octets (control_data_length above 102 with its surplus present) is still dropped before the core. 57 and 84 pass. Left as is.
2. **All-fabric builds are unaffected and differ.** `KL_pp_rx_validator.sv` (protocol-processor, not used by the split build) does read the field: it drops a frame holding fewer than control_data_length + 12 payload octets. So it refuses a long discover with the surplus absent, which this core accepts as briefed.
3. **No tracked issue.** CONTRIBUTING asks for one; tsn-c-stack has no open issue for this. The PR body has no "Closes" line.
4. **Conflicts with `970-first-advertise`** (A847's lane): CHANGELOG.md, docs/TESTS.md, docs/TRACEABILITY.md, docs/VERIFICATION.md; regenerate the tables and recount the plants. `src/adp.c` and the tests merge cleanly.
5. `docs/VERIFICATION.md`'s `PORTING.md:310-353` anchors were already stale on main (the section is at 376 there); not touched.
6. tsn-c-stack's Clang sanitizer build used the host Clang 23.1.5 (the pinned Clang 18 cannot parse the host's libstdc++); the lexer gates used 18.1.3, as earlier lanes did.

## Left on disk
`/data-2/milan/tmp/adpcdl-a849`: the clone, the milan-fpga worktree (registered in `$LANES/train-0923`) and `scratch/` (2.0 GB, builds and logs; can go once the PR merges).
CPU: unbooked, 8 jobs at most. No bench.
