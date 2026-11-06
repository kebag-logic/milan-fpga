# HANDOFF: #840 round 4, [A732d]

Status: REVIEW READY for the manager. Nothing pushed; no PR edit.

- Assignment: #840 issuecomment-6683958840, with R775-2 (issuecomment-6683678472) and R776-2 (issuecomment-6683953603).
- Previous head: `beb38447d07cceac5170ba0a35c7615f5714b7f7`.
- Merged dev and sole merge base: `87e9d03aa2a4797957ac0124d0c7851a2eec234c`.
- Validated head: `3d1ca52f8e9a3ec59076b423c0812982945c7a8b`.
- Original lane base: `604899c08ff1cd1830e1dd08b733109ef852400c`.
- State: [repository-state.json](receipts/repository-state.json).

## Decision needed from the manager

1. **The re-pin route.** The assignment says "through the table's own tool", and no repository command writes these pins.
   `ci_tool_inventory.py --write` writes only `tool-inventory.json`, and it refuses before writing.
   I used `ci_command_table.sha256()` and `ci_tool_inventory.serialized()`, the table's own digest and serializer, through [repin_rows.py](scripts/repin_rows.py).
   No digest was typed by hand. Rerunning it on a clean clone reproduces the committed table: [table-repin.log](receipts/table-repin.log).
   If you meant another route, F4 needs it.
2. **The three rows' re-review is my reading, not the walker's.** The checker cannot reach them: see below.
   R776-2 said a reading is not the recorded review, so a reviewer must accept [table-rows-review.md](receipts/table-rows-review.md).
3. **#838 needs a note.** Allowing `exec` moves the refusal to `compile` at the same file, which #838 does not name.
   Posting that on #838 is outside what this lane may post.

## Commits this round

| Commit | Change |
|---|---|
| `2fbd07254d` | Merge dev 87e9d03a; the only conflict was the generated audit page, ours taken and then regenerated |
| `25902fe527` | PHY peer arms, mutant table, two doc lines |
| `87c9f81f5e` | Three command-table pins |
| `3d1ca52f8e` | Inventory through `docs_inventory.py --write` |

All are one-line subjects with no body and no trailer ([merge-verification.log](receipts/merge-verification.log)).
No firmware, RTL, LiteX or submodule file differs from `beb38447`. That is why no full sweep ran, as the assignment says.

## Changes and clauses

| File:line at head | Change | Clause or authority |
|---|---|---|
| `sw/firmware/nvm_hosttest/phy_host.c:131`, `:133` | First gigabit arm starts register 4 at `0x4be1`, register 9 at `0xf5ff` | N1. IEEE 802.3-2022 Table 40-3 (9.12:10), Table 28B-2 (pause), 28.2.1.2.1 (selector); AGENTS.md section 6 |
| `sw/firmware/nvm_hosttest/phy_host.c:336`, `:338` | Second gigabit arm starts them at `0x47fe`, `0xe9ff`, the complement in every kept bit | Same |
| `sw/firmware/nvm_hosttest/phy_host.c:158-176` | Registers 4 and 0 refused, each with a named no-write assertion | N2 = F5. IEEE 802.3-2022 22.2.4.5.7 (the PHY drives the turnaround zero on a read); `docs/integration/BAREMETAL_FIRMWARE.md:2183` |
| `sw/firmware/nvm_hosttest/phy_host.c:118-127` | The comment states clears and keeps separately, with the patterns | Same as N1 |
| `sw/firmware/nvm_hosttest/test_phy_firmware.py:75-101` | The guard and value anchors, `KEPT_FIELDS`, `kept_bit_mutants()` | N1, N2 |
| `sw/firmware/nvm_hosttest/test_phy_firmware.py:135`, `:138`, `:191-196` | Twenty-five new table rows | N1, N2 |
| `sw/firmware/nvm_hosttest/test_phy_firmware.py:319` | Each mutant's log line now names its assertion | Gate "by name" |
| `docs/integration/BAREMETAL_FIRMWARE.md:2194-2197` | Peer description, count forty-seven | Documentation must match the test |
| `docs/reference/STRICTER_READINGS.md:73` | Count forty-seven | Same |
| `ci/image/command-table.json:14076`, `:14171`, `:14176` | Three `sha256` lines | F4; `docs/testing/CI_IMAGE.md` |
| `docs/DOCUMENTATION_AUDIT.md` | Regenerated, 214 pages | Item 4 |

The two doc pages were not named in the assignment.
They stated "twenty-two" and "keeps or clears in the other state", which this round made false, so they had to change.

**Beyond the minimum, and why.** R775-2's probe kept the first arm at all-ones and mixed the second.
That still lets a forced single bit escape, for example bit 4.10, which is the same cause in a smaller form.
So the two arms are complements, and the selector gets a second start value, because `selector_kept` had only one.
`kept_bit_mutants()` then forces and drops each of the ten kept bits. Drop it if you want the smaller table: the arms stand alone.

## New checks

Every row fails on the named words in [phy_firmware.log](receipts/gates/phy_firmware.log); the full table is [phy-mutation-map.md](receipts/phy-mutation-map.md).

| New check | Planted mutant | Failing words |
|---|---|---|
| `no_write_before_its_register_4_read` | `nak-reg4-not-checked` | `no_write_before_its_register_4_read` |
| `no_write_before_its_register_0_read` | `nak-reg0-not-checked` | `no_write_before_its_register_0_read` |
| `pause_bits_kept`, new start values | `force-pause-on`, `force-bit-4.10`, `force-bit-4.11`, `drop-bit-4.10`, `drop-bit-4.11` | `pause_bits_kept` |
| `master_slave_kept`, new start values | `force-manual-master`, `force-manual-config-only`, `force-bit-9.10` to `9.12`, `drop-bit-9.10` to `9.12` | `master_slave_kept` |
| `selector_kept`, new start values | `force-bit-4.0` to `4.4`, `drop-bit-4.0` to `4.4` | `selector_kept` |

[arm_probe.log](receipts/gates/arm_probe.log) shows each new part is what catches them:

| Temporary change to `phy_host.c` | New mutants that then escape |
|---|---|
| None | 0 of 25 |
| First arm back at `beb38447` values | 2 |
| Second arm back | 9 |
| Both arms back | 13, including R775-2's three |
| Register 4 refusal removed | 1, `nak-reg4-not-checked` |
| Register 0 refusal removed | 1, `nak-reg0-not-checked` |

The committed firmware passes every variant.
The register 4 arm uses `phy_link_tick()`, not `expect_poll()`, because that poll publishes a link.
[phy_firmware.log](receipts/gates/phy_firmware.log) shows `PHY_PUBLISH value=5` there, as R775-2 says, not 13 as R776-2 says: register 9 is still unwritten.
The arm asserts only the absent write, so this does not affect the test.

## The table checker

Run with its parser, fetched by `ci/image/prepare_parser.py` and authenticated by size and SHA-256 ([table-checker.log](receipts/table-checker.log)):

| Tree | `ci_tool_inventory.py --check` |
|---|---|
| Head | rc 2, `changed declared script 'sw/builder/endstation_builder.py'` |
| Dev | rc 2, the same words |
| Throwaway clone, all 36 stale rows re-pinned | rc 2, `uncensused Python builtin 'exec'` |
| The same, `exec` also allowed | rc 2, `uncensused Python builtin 'compile'` |

So this is not a passing check, and it is not one of this round's gates. The gate is the digest comparison, which passes.
Two more files this PR changes have stale rows, `sw/builder/endstation_builder.py` and `sw/builder/test_builder.py`.
Both are stale at dev too, so they are #838's and I left them. `tool-inventory.json` is not regenerated, because `--write` refuses.

## Gates

All on clean clones of `3d1ca52f8e9a3ec59076b423c0812982945c7a8b`, rc 0, never piped. Each gate has a `.log` and `.rc` under [receipts/gates](receipts/gates).

| Gate | Result | Receipt |
|---|---|---|
| `python3 sw/firmware/nvm_hosttest/test_phy_firmware.py` | 51 PHY mutants and 5 boot-path mutants caught; `PHY_BOOT_OK` | [log](receipts/gates/phy_firmware.log) |
| `python3 sw/builder/test_builder.py --require-rv32` | `ALL GATES PASS EXCEPT 2 NOT RUN`: gate 1b's MAKEFLAGS mutation, gate 11's calibration report | [log](receipts/gates/builder.log) |
| Every `run:` step of `docs.yml`, verifier rc 0 | 65 ran rc 0, 31 not run with a reason, 0 bad | [table](receipts/docs-yml-table.md) |
| SDK step, each job on a new empty HOME | `SDK fresh installation: verified` in all three | [log](receipts/docsyml/docs-gates-0__ci_step_28.log) |
| Documentation builder legs | `EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN` | [leg 0](receipts/docsyml/docs-gates-1__gate_25_0.log), [leg 1](receipts/docsyml/docs-gates-2__gate_25_1.log) |
| `python3 scripts/docs_inventory.py --check` | Fresh | [log](receipts/gates/inventory_check.log) |
| `python3 scripts/docs_inventory.py --selftest` | 50 controls | [log](receipts/gates/inventory_selftest.log) |
| Command-table digests, R776-2's script | 37 at head, 37 at dev, added `[]`, removed `[]` | [log](receipts/gates/cmdtable_digests.log) |
| Digests of this PR's files | 3 match, 2 stale at dev too, 0 made stale | [log](receipts/gates/pr_table_digests.log) |
| `git diff --check` against the new merge base | Clean | [log](receipts/gates/diffcheck.log) |
| `git merge-base --all HEAD origin/dev` | One, `87e9d03a` | [log](receipts/gates/merge_bases.log) |
| `push-privacy-check.py . origin/dev` | 0 private lines | [log](receipts/gates/privacy.log) |

Reviewer scripts rerun unchanged, as a cross-check:

- R775-1 and R776-1: 8 of 8 each caught. The one `SURVIVED` line in R776-1's log is its unmutated control.
- R775-2's script: 5 escape, `init-on-failed-bmsr`, `clear-next-page`, `clear-remote-fault`, `reg0-from-constant`, `write-4-before-9`.
- R776-2's script: 3 survive, `bmsr-unacked-still-inits`, `write-frame-no-release`, `init-before-found`.

Those eight are the reviews' suggestions, or mutants they discount. They are unchanged and not assigned. The two reviewers' fix probes anchor on the old `phy_host.c`, so they were not rerun.

## Not done

- **Not run:** the full sweep, the service-budget plans and the capture arms, by the assignment. The sweep record stays at `cadb63b4`. No hardware.
- **Not assigned, left alone:** RES-4, RES-5, S1 to S5 of R775-2, S3 to S5 of R776-2.
- **Residue for you:** RES-1, the PR title still names the round-1 address.
- **PR-BODY.md goes past "the live body plus a section".**
  It also applies RES-2, RES-3 and R4 with this round's head and dev, because the live text is false at this head.
  It also drops the account prefix from the FPGA-gPTP reference, under the no-account-names rule, so that reference is no longer a link.
- **No closing keyword** is in the body, so #840 needs closing by hand after the merge.
- **The maintainer's two open points** from the reviews stand: the `gen_ucode.py:177` STOP clause and the 1000BASE-T ability gate.
- **The `docs/spec-refs.md` extract** named in the assignment does not exist in this tree. I read 802.3-2022 22.2.4.5.7, Table 40-3, Table 28B-1, Table 28B-2 and 28.2.1.2.1 in the standard itself.

## Receipt handling

[INDEX.md](INDEX.md) is generated from the files present.
Logs and the copies under `scripts/` carry path placeholders, so those scripts do not run as they stand.
[raw-log-manifest.json](receipts/raw-log-manifest.json) records each original's size and SHA-256.
No file over 200 KB, toolchain, virtual environment or build tree is in the packet.
