[R776] NEGATIVE - exact head 3d1ca52f8e9a3ec59076b423c0812982945c7a8b

# R776-3: external independent review of PR #842 (issue #840)

- Head `3d1ca52f8e9a3ec59076b423c0812982945c7a8b`, tree `4ff1978a7fc9ecb649394a1cab9e9b46750f9ba2`.
- Delta reviewed: `beb38447..3d1ca52f`: one merge of dev `87e9d03a` and three commits. Live dev and the source base are both `87e9d03aa2a4797957ac0124d0c7851a2eec234c`.
- Context was rebuilt from public state. My own verdict was fixed in `receipts/own-pass-verdict.md` before I wrote the prior-finding dispositions.

## Verdict

NEGATIVE. One MINOR is open, under Tests and Docs. There is no BLOCKER or MAJOR.

All four assigned items hold at their causes, and the firmware is correct. The problem is one new sentence.

To describe the N1 fix, the delta added a claim about every kept bit: "Two gigabit arms start each bit it keeps in opposite states, so forcing or dropping one fails." The firmware keeps more bits than the peer grades. Eighteen planted force and drop mutants of those other bits pass with rc 0.

This is the same defect as F5: the guide claims more than the peer can fail. Narrowing three comments and one guide line would close it, or the peer can grade the remaining bits.

## Results on the assigned focus

| Item | Result | Evidence |
|---|---|---|
| (1) Kept fields start in opposite states, and forcing and dropping fail by name | Holds for selector, pause and MASTER-SLAVE. Start values decode as stated: `0x4be1` and `0x47fe` give selector 00001 and 11110, pause 10 and 01; `0xf5ff` and `0xe9ff` give MASTER-SLAVE 101 and 010. All 23 kept-field force and drop mutants added this round fail by name. Does not hold for the wider claim: see F6 | `receipts/test_phy_firmware.log`, `receipts/phy_probe.txt` |
| (1) The opposite states are what catch them | Holds. With the prior start values, 13 of the 25 kept-field mutants escape, including all three R775-2 named mutants. With either arm given the other's values, 10 or 11 escape. So both arms are needed | `receipts/phy_probe.txt`, `prior-start-values:`, `arm1-as-arm2:`, `arm2-as-arm1:` lines |
| (1) Whole-field defects | Holds. A constant selector, swapped pause bits, a constant MASTER-SLAVE and an inverted MASTER-SLAVE all fail by name | `receipts/phy_probe.txt` |
| (2) Registers 4 and 0 have refusal arms, named assertions and mutants | Holds. `nak-reg4-not-checked` and `nak-reg0-not-checked` fail by name. So do guards I moved between the writes, which leave a partial write. The retry is proved by the later `expect_gigabit_only_advertisement(0, 1)`, which counts writes from 0 and exactly one restart. A guard returning 1 instead of 0 is caught too | `sw/firmware/nvm_hosttest/phy_host.c:158-176`, `receipts/phy_probe.txt`, `receipts/phy_probe_round2.txt` |
| (3) Three digests re-pinned, no new table mismatch | Holds. Each row equals its bytes at this head, the delta moves three `sha256` lines and nothing else, and the stale set is identical at dev and head: none added, none removed. The table equals the repository serializer's output byte for byte | `receipts/table_audit.txt`, `receipts/table_pr_rows.txt` |
| (4) The merge keeps both sides | Holds. A fresh merge of `beb38447` and `87e9d03a` conflicts only in `docs/DOCUMENTATION_AUDIT.md`. The committed merge differs from that automatic result in that page alone. The gitlinks equal dev's | Reproduced in the review clone; `receipts/source_integrity.txt` |
| (4) The docs inventory is what the generator writes | Holds. `--check` rc 0 and `--selftest` rc 0. `--write` on a scratch clone of this head changes nothing: tree stays `4ff1978a` | `receipts/docs_inventory_check.log`, `receipts/docs_inventory_selftest.log`, `receipts/docs_inventory_write.log` |

The table counts reconcile. The author's 37 mismatches cover 147 rows, leaving out the four submodule rows. My blob comparison counts those four as unreadable, which gives 41. A filesystem comparison gives 39, because two `gptp-processor` rows differ from their files. Those are dev's rows too: the gitlink is unchanged.

The author's two questions for a reviewer:

- **Open question 1, the re-pin route: accepted.** No repository command writes these pins. `ci_command_table.sha256()` and `ci_tool_inventory.serialized()` are the table's own digest and serializer, and the published `table-repin.log` reproduces the committed bytes. #838's "never by hand" is met.
- **Open question 2, the three rows' re-review: accepted.** I read each diff against its declared reason:
  - `fw_service_budget/run.py` changes a constant from 9 to 16, a comment and a self-test boundary.
  - `nvm_capture_cpu/run.py` adds one more constant to a generated header.
  - `nvm_capture_cpu/soc.py` adds one dictionary entry.
  - None adds a process, an argument form or an install, so class `reviewed non-installing` and each reason still hold. This rests on reading, because the walker cannot reach these rows (see Real limits).

## Findings

### F6 - MINOR - Tests, Docs - `docs/integration/BAREMETAL_FIRMWARE.md:2195` - the guide says every kept bit fails when forced or dropped, and the peer grades ten of them

- **Where the claim is:**
  - `docs/integration/BAREMETAL_FIRMWARE.md:2195`: "Two gigabit arms start each bit it keeps in opposite states, so forcing or dropping one fails."
  - `sw/firmware/nvm_hosttest/phy_host.c:122-126`: "start each kept bit in opposite states ... so forcing or dropping any kept bit changes it in one arm."
  - `sw/firmware/nvm_hosttest/test_phy_firmware.py:80`: "each field the PHY init keeps", and `:88`.
  - All are new in this delta.
- **Authority:** AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect." The same section's Docs lens applies to changed contracts. R776-2 F5 was this same shape, filed MINOR, and its outcome allowed "the guide and comment claim only what is graded".
- **Evidence.**
  - `milan_baremetal.c:1065-1066` clears only `0x03e0` and `0x4000`, so register 4 bits 15, 13 and 12 are kept as read, as well as the selector and pause.
  - `milan_baremetal.c:1067-1069` keeps every register 0 bit except reset and isolate, with enable and restart set.
  - Register 4 bits 15, 13 and 12 are 0 in both arms, so they do not start in opposite states. No assertion reads them, and none reads register 0's kept bits.
  - All 18 mutants below pass with rc 0 (`receipts/phy_probe.txt`):

  | Register | Bits, each forced and dropped | Mutants |
  |---|---|---:|
  | 4 | 15, 13, 12 | 6 |
  | 0 | 14, 13, 11, 8, 7, 6 | 12 |

  - The author's own gate log at this head agrees: `gates/r775_2_phy_mutants.log` records `clear-next-page`, `clear-remote-fault` and `reg0-from-constant` as `ESCAPED`.
- **Why MINOR, when R775-2 S2 was a suggestion.** S2 was optional because "the docs do not name these": no claim covered them. This delta adds a claim that does. A reader of the guide now believes a forced power-down bit fails the gate.
- **Why not RESIDUE.** The sentence is a false statement about what a test proves, and one fix route changes the test. The owner's rule sends an unsure case to MINOR.
- **Impact.** There is no live defect: the firmware is correct at this head. A regression that forces bit 0.11 (power-down) or 0.14 (loopback), or forces next page or remote fault, ships green while the guide says it fails. Forcing 0.11 or 0.14 would keep the board's link down.
- **Required outcome, either one:**
  1. Grade them: start register 4 bits 15, 13 and 12 and register 0's kept bits in opposite states across the arms, assert each by name, and add the mutants to the table.
  2. Claim only what is graded:
     - Guide line 2195: `Two gigabit arms start the selector, pause and MASTER-SLAVE bits in opposite states, so forcing or dropping one fails.`
     - Add after it: `Register 4 bits 15, 13 and 12 and register 0's other bits are kept as read and are not graded.`
     - `phy_host.c:123-126`: say "each selector, pause and MASTER-SLAVE bit" and "any of those bits".
     - `test_phy_firmware.py:80`: say "each kept field the peer grades". At `:88`, say "Each graded kept bit".
- **Verification.** Route 1: `python3 -I scripts/phy_probe.py <clone> <work>` reports the 18 lines as CAUGHT by name, and `test_phy_firmware.py` stays rc 0. Route 2: no sentence in those places claims every kept bit, and the guide names the ungraded ones.

## Residue

| ID | Where | Defect | Exact fix |
|---|---|---|---|
| R5 (was R775-2 RES-1, R776-2 R3) | PR title | Still names the round-1 address | `Prototype identity 02:4B:4C:4B:4C:01, 1000BASE-T-only advertisement on 1G PHYs, and the stricter-reading page (#840)` |
| R6 (was R775-2 RES-4) | `docs/reference/STRICTER_READINGS.md:45` | "The builder gate" reads as the builder | `- Gate 28b refuses a zero octet in any tracked config.` |
| R7 (was R775-2 RES-5) | `docs/findings/397_SERVICE_BUDGET.md:290-291` | The colon sentence is split from its table by a parenthetical | Move line 291 below the table |

The comment rule has no new instance. A scan of the lines this delta adds under `sw/firmware/nvm_hosttest` and `ci` finds no bench lane label, review round, reviewer ID or comment ID. The delta's commits are one line with no trailers.

## Suggestions

- **S6 - Tests - `ci/image/tool-inventory.json`, `inputs`.** This PR leaves two more stale input digests there: `tb/verilator/nvm_capture_cpu/run.py` and `soc.py`, taking the count from 95 to 97 (`receipts/table_audit.txt`). Round 4 item 3 and F4 cover the command table, so neither is breached. The file is generated whole and `--write` refuses at dev, so there is no honest route to fix them here, and #838's acceptance regenerates them. A line in the PR text would save #838 from finding them.
- **S7 - Tests - `milan_baremetal.c:1063-1066`.** `write-4-before-9` escapes (`gates/r775_2_phy_mutants.log`). No document claims that order, and the restart comes after both, so this is optional.

## Prior public findings

| Prior finding | Severity, lenses | Disposition at this head | Evidence |
|---|---|---|---|
| R775-2 N1 | MINOR, Tests | RESOLVED at its cause for the fields it named. Its wider wording is F6 | Focus item (1) |
| R775-2 N2 = R776-2 F5 | MINOR, Tests | RESOLVED. The guide's sentence on registers 15, 4, 9 and 0 is now graded for all four | Focus item (2); `receipts/phy_probe_round2.txt` |
| R776-2 F4 | MINOR, Tests | RESOLVED. Added by head: none | Focus item (3) |
| R775-2 S2 | SUGGESTION | PROMOTED to F6, because this delta added a claim that covers those bits | F6 |
| R775-2 RES-1, R776-2 R3 | RESIDUE | RETAINED as R5 | Live PR title |
| R775-2 RES-2, R776-2 R4 | RESIDUE | RESOLVED for the inventory text: the phrases are gone and the gate row reads pass at `3d1ca52f` | Live PR body |
| R775-2 RES-3 | RESIDUE | RESOLVED: the Executor line names all four sessions | Live PR body |
| R775-2 RES-4, RES-5 | RESIDUE | RETAINED as R6, R7 | Files unchanged |
| R775-2 S1, R776-2 S3 | SUGGESTION | RETAINED, optional | `tb/tools/avdecc_ctl.py:312` |
| R775-2 S3, R776-2 S4 | SUGGESTION | RETAINED, optional. `bmsr-unacked-still-inits` and `write-frame-no-release` still escape; neither is against a documented claim | `receipts/phy_probe_round2.txt` |
| R775-2 S4 | SUGGESTION | RETAINED, optional | `tb/verilator/milan_dp/Makefile:565` |
| R776-2 S5 | SUGGESTION | RETAINED, optional | `sw/builder/README-parameters.md:173` |
| R775-1 S2, R776-1 S2 | SUGGESTION | RETAINED, optional; the delta does not touch them | No new evidence |

**Correction to my own R776-2.** I wrote that a register 4 refusal still publishes 13. It publishes 5. The peer's unwritten register 9 has bit 9 clear and bit 8 set, so the resolution finds half duplex. R775-2 had this right, and `receipts/test_phy_firmware.log` shows it. The head's comment at `phy_host.c:158-160` says only "publishes a link", so nothing needs changing.

## Lens results

```text
[R776] PASS Conformance - sw/firmware/milan_baremetal/milan_baremetal.c:1044-1071, git diff beb38447..3d1ca52f on sw/firmware/milan_baremetal, configs and the submodules - that diff is empty, so the advertisement, identity and settled maintainer points keep R776-2's result; round 4 items 1 to 4 checked against the assignment
[R776] PASS RTL - git diff beb38447..3d1ca52f on hdl, syn, constraints, sw/litex and the gitlinks - empty, so no RTL or timing artifact is in scope and R776-2's result stands
[R776] PASS Robustness - phy_host.c:143-186 with phy_advertise_gigabit_only() - refused reads of registers 15, 9, 4 and 0 write nothing and the next poll advertises once; partial-write and no-retry mutants of mine are caught
```

Tests and Docs are UNCLEAN under F6. What passes in them:

- **Tests:** `test_phy_firmware.py` rc 0 with 51 PHY and 5 boot-path mutants, and 7 whole-field and refusal probes of mine plus the 3 round 2 refusal probes caught by name. The other 18 of my 25 probes are F6, and the 2 other round 2 probes are the retained S4 escapes.
- **Docs:** `docs_check.py` rc 0, `check_doc_style.py` rc 0, `docs_inventory.py --check` and `--selftest` rc 0, and `git diff --check 87e9d03a 3d1ca52f` clean. "Forty-seven" is correct: I counted the table.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `milan_baremetal.c:1044-1071`; empty firmware, config and gitlink diff; round 4 assignment; the settled maintainer points on the PR | R776-3 | 3d1ca52f8e9a3ec59076b423c0812982945c7a8b |
| RTL | CLEAN | Empty diff on `hdl`, `syn`, `constraints`, `sw/litex` and the gitlinks | R776-3 | 3d1ca52f8e9a3ec59076b423c0812982945c7a8b |
| Robustness | CLEAN (S4 retained, optional) | `phy_host.c:143-186`; refusal, partial-write and no-retry probes in `receipts/phy_probe.txt` and `receipts/phy_probe_round2.txt` | R776-3 | 3d1ca52f8e9a3ec59076b423c0812982945c7a8b |
| Tests | UNCLEAN (F6) | `phy_host.c`; `test_phy_firmware.py`; my probes in `receipts/phy_probe.txt`; `receipts/table_audit.txt`; author round 4 gates | R776-3 | 3d1ca52f8e9a3ec59076b423c0812982945c7a8b |
| Docs | UNCLEAN (F6; R5 to R7 residue) | `BAREMETAL_FIRMWARE.md:2168-2204`; `STRICTER_READINGS.md:52-74`; `DOCUMENTATION_AUDIT.md`; docs gates in `receipts/` | R776-3 | 3d1ca52f8e9a3ec59076b423c0812982945c7a8b |

## Real limits

- **Disclosure.** While listing recent PR comments to find the settled maintainer points, my listing printed the first line of the R775-3 report at this head, including its verdict word. I did not open that report's body, and its archive on the evidence branch was not read. The F6 probe receipt was already written by then, but my severity decision and `receipts/own-pass-verdict.md` came after it. I also read R775-2 and R776-2 after my independent pass and probes, as assigned, and before writing that file. A reader should weigh my NEGATIVE with that in mind.
- **The evidence packet is not signed.** The assignment calls it signed, but commit `447243f675`, which holds `author-r4`, is unsigned, as the rest of that branch is. I checked integrity through its manifest: 190 of 190 digests match (`receipts/author_r4_manifest_check.txt`).
- **The command-table checker did not reach the three rows.** Here it stops first at `REFUSED: CI_IMAGE_SHFMT must name the checksum-pinned Bash parser`, rc 2, because the pinned parser is absent. The author's run stops at `endstation_builder.py` (#838). The three rows rest on digests and on reading the diffs.
- **I did not run the builder or the `docs.yml` steps.** Those rest on the author's published receipts: `ALL GATES PASS EXCEPT 2 NOT RUN` (gate 1b's MAKEFLAGS mutation, gate 11's calibration report), and 65 steps rc 0, 31 not run with a reason, 0 bad.
- **`push-privacy-check.py` was not run by me.** The published log reports 0 private lines.
- **No full sweep ran at this head.** The last record is `cadb63b4`. The merged dev change touches `scripts/owned_process.py`, its tests and `docs/testing/TESTING.md`, which I checked only as kept-both-sides merge content.
- **I did not open IEEE 802.3.** The bit meanings rest on the source comments and my reading.
- **Hosted state is not a result.** At review time the exact head showed 2 checks successful and 13 without a conclusion.
- **No hardware was used.** Physical calibration is NOT RUN, and field skips are not hardware proof. No manager source bank ran at this head, and I infer none.

## Pending manager duties

- The current-dev merge-candidate build, with builder and native banks, and hosted and act acceptance.
- R5 to R7 on the residue checklist.
- The #840 title and body still state the round-1 identity. The round-2 assignment supersedes them, so a cold reader needs that pointer.
- S6, if the two inventory inputs should be named for #838.

The review clone is restored: head, tree, index and gitlinks equal the exact head, and `git status` with ignored files is empty (`receipts/source_integrity.txt`).

R776-3 FINISHED
