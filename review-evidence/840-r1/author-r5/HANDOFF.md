# HANDOFF: #840 round 5, [A732e]

Status: REVIEW READY for the manager. Nothing pushed; no PR edit.

- Assignment: the latest [A10] comment on #840, with R775-3 N3 = R776-3 F6.
- Base: `3d1ca52f8e9a3ec59076b423c0812982945c7a8b`.
- Validated head: `27df6e08cf157b9c5e4b0fdb7da2fa28d8ab83fa`, one commit, one-line subject, no body or trailer.
- Dev and sole merge base: `87e9d03aa2a4797957ac0124d0c7851a2eec234c`. Dev has not moved, so there is no merge.
- Original lane base: `604899c08ff1cd1830e1dd08b733109ef852400c`, an ancestor of the head.
- State: [repository-state.txt](receipts/repository-state.txt).

## Changes and clauses

No firmware, RTL, LiteX, config or submodule file changed.

| File:line at head | Change | Clause or authority |
|---|---|---|
| `sw/firmware/nvm_hosttest/phy_host.c:74-75`, `:92-93` | `power_down_kept` and `loopback_kept`, graded against the arm's own start value | Ruling item 1; IEEE 802.3-2022 22.2.4.1.5 (bit 0.11), 22.2.4.1.2 (bit 0.14) |
| `sw/firmware/nvm_hosttest/phy_host.c:135` | First arm starts register 0 at `0x9c00`: power-down 1, loopback 0 | Same |
| `sw/firmware/nvm_hosttest/phy_host.c:343` | Second arm starts register 0 at `0x6100`: power-down 0, loopback 1 | Same |
| `sw/firmware/nvm_hosttest/phy_host.c:47-51`, `:336-337` | Comments state the two bits, and that the peer stores bit 0.14 and models no loopback | Same |
| `sw/firmware/nvm_hosttest/phy_host.c:127-133` | Names the twelve graded bits; the others are unmodified by construction and not graded | Ruling item 2 |
| `sw/firmware/nvm_hosttest/test_phy_firmware.py:81-83` | `REGISTER_0_VALUE`, the anchor for the register 0 mutants | Ruling item 1 |
| `sw/firmware/nvm_hosttest/test_phy_firmware.py:84-91` | `KEPT_FIELDS` gains both bits; its comment says "the peer grades" | Ruling items 1 and 2 |
| `sw/firmware/nvm_hosttest/test_phy_firmware.py:94-108` | `kept_bit_mutants()` covers register 0; docstring narrowed | Same |
| `docs/integration/BAREMETAL_FIRMWARE.md:2195-2197` | Names the graded bits, then the ungraded ones: 4.15, 4.13, 4.12, 0.13 and 0.8 to 0.0 | Ruling item 2; `milan_baremetal.c:1065-1069` |
| `docs/integration/BAREMETAL_FIRMWARE.md:2199`, `docs/reference/STRICTER_READINGS.md:73` | Count fifty-one | Documentation must match the test |
| `docs/DOCUMENTATION_AUDIT.md` | Regenerated through `docs_inventory.py --write`: the guide grew two lines | Docs rule |

`STRICTER_READINGS.md` was not named in the ruling. It stated forty-seven, which this round made false.

## New checks

The full table is [phy-mutation-map.md](receipts/phy-mutation-map.md).

| New check | Planted mutant | Failing words |
|---|---|---|
| `power_down_kept` | `force-bit-0.11`, `drop-bit-0.11` | `Assertion `power_down_kept' failed` |
| `loopback_kept` | `force-bit-0.14`, `drop-bit-0.14` | `Assertion `loopback_kept' failed` |

[arm_probe.log](receipts/gates/arm_probe.log) shows that the start values and assertions are what catch them:

- Putting either arm back lets that arm's drop mutant escape.
- Giving both arms the same state lets the force mutant escape.
- Removing an assertion lets both of its mutants escape.

## Gates

All on clean clones of `27df6e08`, rc 0, never piped. Each has a `.log` and `.rc` under [receipts/gates](receipts/gates).

| Gate | Result | Receipt |
|---|---|---|
| `python3 sw/firmware/nvm_hosttest/test_phy_firmware.py` | 51 advertisement, 4 poll and 5 boot-path mutants caught by name; `PHY_BOOT_OK` | [log](receipts/gates/phy_firmware.log) |
| Every `run:` step of `docs.yml`, verifier rc 0, each job on a new empty HOME | 65 ran rc 0, 31 not run with a reason, 0 bad; `SDK fresh installation: verified` in all three | [table](receipts/docs-yml-table.md) |
| Documentation builder legs, inside `docs.yml` | `EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN` | [leg 0](receipts/docsyml/docs-gates-1__gate_25_0.log), [leg 1](receipts/docsyml/docs-gates-2__gate_25_1.log) |
| `python3 scripts/docs_inventory.py --check` | Fresh | [log](receipts/gates/inventory_check.log) |
| `python3 scripts/docs_inventory.py --selftest` | Pass | [log](receipts/gates/inventory_selftest.log) |
| Digests of this PR's files | 3 match, 2 stale at dev too, 0 made stale | [log](receipts/gates/pr_table_digests.log) |
| Digests of the whole table | 37 at head, 37 at dev, added `[]`, removed `[]` | [log](receipts/gates/cmdtable_digests.log) |
| `git diff --check` against the merge base | Clean | [log](receipts/gates/diffcheck.log) |
| `git merge-base --all HEAD origin/dev` | One, `87e9d03a` | [log](receipts/gates/merge_bases.log) |
| `push-privacy-check.py . origin/dev` | 0 private lines | [log](receipts/gates/privacy.log) |

No digest moved: neither `phy_host.c` nor `test_phy_firmware.py` has a table row, so nothing was re-pinned.

Reviewer scripts rerun as a cross-check, unchanged:

| Script | Result | Log |
|---|---|---|
| R775-1 and R776-1 | 8 of 8 each caught; R776-1's one `SURVIVED` line is its unmutated control | [R775-1](receipts/gates/r775_1_phy_mutants.log), [R776-1](receipts/gates/r776_1_phy_mutants.log) |
| R775-3 `phy_probe.py` | Of its 22 rows, 4 caught by name and 18 escape, as ruled | [log](receipts/gates/r775_3_probe.log) |
| R776-3 `phy_probe.py` | Of its 18 rows, 4 caught by name and 14 escape, as ruled | [log](receipts/gates/r776_3_probe.log) |

The four caught in each are 0.11 and 0.14, forced and dropped.
R775-3's 26 `NOT-NAMED` lines are all in its control variants, none on the head.

## Not done

- **Not run, by the assignment:** the full sweep, the service-budget plans, the capture arms and the standalone `test_builder.py --require-rv32`. The sweep record stays at `cadb63b4`. No hardware.
- **`ci_tool_inventory.py --check` not run:** this round's gate is the digest comparison. Its #838 refusal is recorded at `3d1ca52f`.
- **Not assigned, left alone:** RES-4, RES-5 (= R6, R7), R775-3 S6 to S8, R776-3 S6 and S7, and all retained suggestions.
- **Yours:** the PR title (RES-1 = R5), the #840 title and body pointer, and S6 for #838 if you want it named there.
- **No closing keyword** is in the body, so #840 needs closing by hand after the merge.

## Limit of the new arms

The peer is a register file. It stores bits 0.11 and 0.14 and models neither power-down nor loopback, so the arms grade the written value, not link behaviour.
The first arm therefore holds a link with power-down set, which a real PHY would not. `phy_host.c:336` says so for loopback, and `:131` gives the start states.

## PR-BODY.md

It is the live body with the round 5 line, plus these edits:

- First line `[A732e]`, the roles lines, the checkout head and the inventory row move to this round.
- The ruling's narrowing is applied to the Description row and to the Round 4 row.
- The Round 2 row said "every bit the init keeps" too, so it now states that round's start values without the claim.
- "Twenty-two planted advertisement mutants" was stale since round 4, and now reads fifty-one.

## Receipt handling

[INDEX.md](INDEX.md) is generated from the files present.
Logs and the copies under `scripts/` carry path placeholders, so those scripts do not run as they stand.
[raw-log-manifest.json](receipts/raw-log-manifest.json) records each original's size and SHA-256.
No file over 200 KB, toolchain, virtual environment or build tree is in the packet.
