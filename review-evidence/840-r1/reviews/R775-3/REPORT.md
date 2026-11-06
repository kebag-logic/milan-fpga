[R775] NEGATIVE - exact head 3d1ca52f8e9a3ec59076b423c0812982945c7a8b

# R775-3: internal cleared-context review of PR #842 (issue #840)

- Head: `3d1ca52f8e9a3ec59076b423c0812982945c7a8b`, tree `4ff1978a7fc9ecb649394a1cab9e9b46750f9ba2`.
- Delta reviewed: `beb38447..3d1ca52f`, the round 4 assignment on #840 (issuecomment-6683958840).
- Source base and live dev: `87e9d03aa2a4797957ac0124d0c7851a2eec234c`. One merge base.
- Reviewed in an isolated detached clone. No source edits, commits, pushes or GitHub writes were made.

## Verdict

NEGATIVE. There is one MINOR finding, N3, under Tests and Docs. There is no MAJOR or BLOCKER.

All four assigned items hold at their cause:

- **N1 is resolved.** Each of the ten bits of the selector, pause and MASTER-SLAVE fields starts in opposite states across the two gigabit arms. Forcing or dropping any of them fails by name.
- **N2 = F5 is resolved.** Registers 4 and 0 have refusal arms with named assertions, and removing either arm lets its mutant escape.
- **F4 is resolved.** The three rows equal the head's bytes, and this PR adds no command-table mismatch.
- **The dev merge is correct.** Both sides are kept, and the inventory is what the generator writes.

The firmware is right and is unchanged by this delta.

N3 is what the delta says about its own test. It widens "the selector, pause and MASTER-SLAVE fields" to "each bit it keeps", and the firmware keeps more bits than that. Twenty-two probed force and drop mutants of other kept bits pass the test.

## Findings

### N3 - MINOR - Tests, Docs - the test is described as covering every kept bit, and it covers ten

- **Where:**
  - `docs/integration/BAREMETAL_FIRMWARE.md:2195`: "Two gigabit arms start each bit it keeps in opposite states, so forcing or dropping one fails."
  - `sw/firmware/nvm_hosttest/phy_host.c:122-126`: "start each kept bit in opposite states", "forcing or dropping any kept bit changes it in one arm".
  - `sw/firmware/nvm_hosttest/test_phy_firmware.py:80`: "each field the PHY init keeps". Also `:88`.
  - PR body lines 67 and 102 repeat the claim.
- **Authority:** AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect". Section 6, Docs: changed contracts are reflected in authoritative docs.
- **Evidence.** `milan_baremetal.c:1065-1069` writes register 4 and register 0 by clearing and setting named bits, so every other bit passes through as read. That keeps 4.15, 4.13 and 4.12, and every register 0 bit except 15, 12, 10 and 9. `KEPT_FIELDS` holds only the ten bits. Both arms start 4.15, 4.13 and 4.12 at zero, and no assertion grades them or the other register 0 bits.

  All 22 mutants below exit 0 (`receipts/phy_probe.tsv`, rows `x-force-*` and `x-drop-*`):

  | Register | Bits forced on and dropped | Mutants escaped |
  |---|---|---|
  | 4 | 15, 13, 12 | 6 of 6 |
  | 0 | 14, 13, 11, 8, 7, 6, 5, 0 | 16 of 16 |

  Bit 0.11 is power-down and bit 0.14 is loopback, so a firmware that forces either passes the gate. I did not probe register 0 bits 4 to 1. They take the same path.
- **Why this is new.** R775-2 S2 recorded this gap as a suggestion, because no document then claimed these bits. The delta's wording now makes the claim. That wording is new, while the test gap itself is not.
- **Impact.** A reader of the guide concludes that any change to a kept bit fails the gate, and a change to any of these bits would ship green. The shipped firmware is correct, so this is a false statement of test strength and not a live defect.
- **Why MINOR, not RESIDUE.** A wording fix alone would make every statement true. But these sentences state what a test proves, and execution falsifies them, so I cannot say the defect is only wording. The owner's rule makes that case MINOR. This is the deciding reason, and without it I would have called the wording RESIDUE. The test itself meets the frozen item, which names kept fields and, through N1, documented keeps.
- **Required outcome.** Either of these:
  1. Say what is graded. Exact text:
     - Guide `:2195`: `Two gigabit arms start the ten bits of the selector, pause and MASTER-SLAVE fields in opposite states, so forcing or dropping one fails.` Then a new line: `Register 4 bits 15, 13 and 12 and the other register 0 bits pass through as read and are not graded.`
     - `phy_host.c:124`: `start each bit of these three fields in opposite states`. `:126`: `or dropping any of those ten bits changes it in one arm`.
     - `test_phy_firmware.py:80`: `each field the PHY init is documented to keep`. `:88`: `Each bit of a documented field forced on and dropped`.
     - PR body lines 67 and 102: the same narrowing.
  2. Or grade those bits: start them in opposite states and add them to `KEPT_FIELDS`, with a named register 0 assertion.
- **Verification.** Under option 1, the sentences name only what the 47 mutants cover, `test_phy_firmware.py` stays green, and `docs_inventory.py --write` then `--check` run if the line count moves. Under option 2, the 22 mutants in `scripts/phy_probe.py` each fail by name.

## Assigned focus

### 1. Kept fields start in opposite states: resolved at its cause

- The start values decode as stated. Register 4 is `0x4be1` then `0x47fe`: selector `00001` then `11110`, pause `10` then `01`. Register 9 is `0xf5ff` then `0xe9ff`: MASTER-SLAVE `101` then `010`.
- `rediscover()` copies the second arm's values into `initial` before the init reads them, so the second arm grades against its own start.
- `test_phy_firmware.py` rc 0 at this head: 51 PHY and 5 boot-path mutants, each named. All 47 tabled mutants failed on their expected assertion in my separate build.
- My own field-shaped defects were all caught by name: constant selector, selector low bit only, swapped pause bits, constant MASTER-SLAVE both ways, inverted MASTER-SLAVE.
- **The start values are the cause, and the controls show it** (`receipts/phy_probe.tsv`):

  | Driver variant | Result |
  |---|---|
  | Both arms back at the previous `0x4fe1` and `0xfdff` | Each force of a pause or MASTER-SLAVE bit, and `force-pause-on` and both manual MASTER-SLAVE mutants, escape |
  | Second arm collapsed onto the first | 10 of the 20 per-bit mutants escape, and so does `force-manual-config-only` |

- R775-2's three escaped mutants now fail on `pause_bits_kept` and `master_slave_kept`.

### 2. Registers 4 and 0 refused: resolved at its cause

- `nak-reg4-not-checked` and `nak-reg0-not-checked` fail on their named assertions.
- With the matching arm deleted from the driver, each escapes, so each arm is what catches its mutant.
- Beyond the table:
  - Checking register 4 or register 0 only after writing register 9 fails on the same names.
  - Dropping register 9's term fails on `no_write_before_its_read`.
  - A guard that gives up instead of retrying fails on `no_10base_t_advertised`, so the retry is graded.
- The comment at `phy_host.c:158` is true. That poll publishes value 5 (`receipts/test_phy_firmware.log:10`), which is 1000BASE-T half duplex from the unwritten register 9, so the arm rightly avoids `expect_poll(now, 0)`.

### 3. Digests: resolved at its cause

- Hashing blobs independently of the repository's tools, the three rows equal the head's bytes (`receipts/table_digests.txt`).
- Added at head: none. Removed: none. Only these three rows differ from dev, and only by `sha256`.
- `ci_tool_inventory.serialized()` of the table reproduces the file byte for byte.
- The author's 37 reconciles with mine: 36 stale and 1 missing in the superproject (`receipts/table_count_reconcile.txt`). Two submodule rows are also stale in my clone, and those gitlinks equal dev's, so they are not this PR's.
- **Author's open question 1, the route.** I accept it. No repository command writes these pins, and the digest function and serializer are the table's own. Nothing suggests hand-typing, and the bytes match independently.
- **Author's open question 2, the row re-review.** I read the three diffs against dev and accept the reading. `class` and `reason` remain true for all three: a constant 9 to 16 with its comment and self-test value, one generated constant, and one JSON entry. None adds a process, an argument form or an install. This is the reviewer acceptance the author asked for.
- The checker did not run here, because the pinned parser is absent (`receipts/ci_tool_inventory_check.txt`). For the checker's own result I rely on the author's `table-checker.log`.

### 4. Dev merge and inventory: resolved

- `2fbd07254d` has parents `beb38447` and `87e9d03a`.
- All 5 dev-only files equal dev's blobs at the merge, and all 38 PR-only files equal `beb38447`'s blobs.
- `docs/DOCUMENTATION_AUDIT.md` is the only file both sides changed and the only conflict.
- `docs_inventory.py --check` rc 0 and `--selftest` rc 0 with 50 controls.
- `git diff --check` against dev is clean, and all six gitlinks equal dev's.
- `check_doc_style.py` and `check_doc_paths.py` rc 0 at this head.

## Prior public findings

| Finding | Severity, lenses | Disposition at this head |
|---|---|---|
| R775-2 N1 | MINOR; Tests | **Resolved.** See focus 1. |
| R775-2 N2 = R776-2 F5 | MINOR; Tests | **Resolved.** See focus 2. |
| R776-2 F4 | MINOR; Tests | **Resolved.** See focus 3. |
| R775-1 and R776-1 F1, F2, F3 | MAJOR and MINOR | **Resolved** at R775-2, and this delta touches nothing they depend on. The firmware, service figures and receipts are unchanged. |
| RES-1 = R776-2 R3, PR title | RESIDUE | **Retained.** The title still names `02:4B:4C:00:00:01`. |
| RES-2 = R776-2 R4, PR body inventory text | RESIDUE | **Resolved.** The body now reads `pass at 3d1ca52f`, and the open-item text is gone. |
| RES-3, roles line | RESIDUE | **Resolved.** `[A732c]` and `[A732d]` are listed. |
| RES-4, `STRICTER_READINGS.md:45` | RESIDUE | **Retained**, with the exact fix from R775-2. |
| RES-5, `397_SERVICE_BUDGET.md:290-291` | RESIDUE | **Retained**, with the exact fix from R775-2. |
| R775-2 S2 | SUGGESTION | **Superseded by N3**, because the delta's wording now makes the claim. |
| R775-2 S1, S3, S4, S5; R776-2 S3, S4, S5; R776-1 S2 | SUGGESTION | **Retained, not taken.** |

## Residue

No new residue. RES-1, RES-4 and RES-5 stay as above, with their exact fixes in R775-2.

## Suggestions

- **S6 - Tests - `ci/image/tool-inventory.json`.** This is a second digest set, outside the command table and outside item 3. Its `inputs` entries for `tb/verilator/nvm_capture_cpu/run.py` and `soc.py` were fresh at dev and are stale at this head, taking 95 stale inputs to 97 (`receipts/tool_inventory_inputs.txt`). The generator refuses, and hand-editing a generated file would be wrong, so I do not ask for a change in this PR. Naming it on #838 would keep it visible.
- **S7 - Tests - `phy_host.c:161-168`.** The register 4 arm's comment says a link is published, and nothing asserts it. `assert(status_word == 5u)` would pin the comment.
- **S8 - Tests - `phy_host.c:131`, `:336`.** The two arms also differ in auto-negotiation enable, so a defect conditional on that state can hide. `x-drop-pause10-when-an-on` escapes, because bit 4.10 is set only in the disabled arm. This mutant is artificial, so it is optional.

## Lens results

```text
[R775] PASS Conformance - assignment items 1 to 4 against phy_host.c, command-table.json, 2fbd07254d and DOCUMENTATION_AUDIT.md at 3d1ca52f - each item met; the PHY init, configs and identity are unchanged since R775-2; the maintainer points are settled on the PR
[R775] PASS RTL - git diff beb38447..3d1ca52f on hdl, syn, sw/litex, constraints, configs and sw/firmware/milan_baremetal is empty and all six gitlinks equal dev's - no RTL in scope
[R775] PASS Robustness - phy_host.c:143-186 refusal arms, phy_peer.h:98, receipts/phy_probe.tsv - each refused read of registers 15, 9, 4 and 0 writes nothing and the next poll retries; a give-up guard and late checks are caught; the firmware is unchanged
```

Tests is UNCLEAN under N3. What passes there: `test_phy_firmware.py` rc 0 in 47.6 s under load, against the 180 s bound at `test_nvm_firmware.py:989`; all 47 tabled mutants fail by name; and the arm controls above.

Docs is UNCLEAN under N3. What passes there: the count "forty-seven" is exact, the other sentences at guide `:2194-2196` hold, and inventory, style and path gates are rc 0.

Comment rule: the added lines in `phy_host.c` and `test_phy_firmware.py` carry no bench lane label, review round, reviewer ID or comment ID. Commits are one line with no trailers.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment items 1 to 4; `phy_host.c`; `command-table.json`; merge `2fbd07254d`; audit page | R775-3 | 3d1ca52f8e9a3ec59076b423c0812982945c7a8b |
| RTL | CLEAN | Empty hdl, syn, `sw/litex`, constraints, configs and firmware diff; six gitlinks | R775-3 | 3d1ca52f8e9a3ec59076b423c0812982945c7a8b |
| Robustness | CLEAN | `phy_host.c` refusal arms; `phy_peer.h`; `receipts/phy_probe.tsv` | R775-3 | 3d1ca52f8e9a3ec59076b423c0812982945c7a8b |
| Tests | UNCLEAN (N3) | `phy_host.c`, `test_phy_firmware.py`, `phy_peer.h`; 47 tabled and 36 own mutants; 5 driver variants; digests | R775-3 | 3d1ca52f8e9a3ec59076b423c0812982945c7a8b |
| Docs | UNCLEAN (N3) | `BAREMETAL_FIRMWARE.md`, `STRICTER_READINGS.md`, `DOCUMENTATION_AUDIT.md`; inventory, style and path gates | R775-3 | 3d1ca52f8e9a3ec59076b423c0812982945c7a8b |

## Real limits

- **Reading order.** The assignment asks that no other reviewer's report be read before my verdict and ledger are written. I read R775-2 and R776-2 after my independent pass and all my probes, but before writing this verdict and ledger. N3's probe results predate that reading, while its severity was set afterwards, with S2 in view. I read no third-round report from another reviewer.
- **Evidence integrity.** The assignment's link, `194f3733`, holds only the round 1 packet. The round 4 receipts are on `840-review-evidence` at `447243f675`. That commit is unsigned, so the packet is hash-manifested and not signed. 17 fetched files match their manifest hashes, and the mutant lines in `gates/phy_firmware.log` equal my own run.
- **Author gates read from receipts, not rerun:** the builder (rc 0) and `docs.yml` (table: 65 rc 0, 31 NOT RUN), plus `push-privacy-check.py` (rc 0). I read those rc values, not the builder or `docs.yml` logs.
- **Checker.** `ci_tool_inventory.py --check` stopped here on the missing pinned parser, and I did not prepare one.
- **Scoped Verilator.** Not used: the probes are host compiles of the firmware, so no RTL simulator was needed.
- **Sweep and service plans.** Not run at this head, by assignment. The sweep record stays at `cadb63b4`.
- **Clause text.** I did not reopen the standards. Register 4 and 0 bit names are from my knowledge of Clause 22 and Clause 28.
- **Hardware.** Physical calibration NOT RUN. Everything here is at the pin-level peer, and field skips are not hardware proof.
- **Hosted.** At 12:42Z the head had 15 check runs, 3 in progress and 12 queued, none finished. This is not hosted acceptance, and I draw nothing from it.

## Pending manager duties

- Carry N3 to the author, and RES-1, RES-4 and RES-5 to the residue checklist.
- Merge-candidate builder and native banks, and hosted and act acceptance.
- Decide whether S6 goes onto #838.
- The issue title and body still state the first identity. A cold reader would benefit from a note.
- The PR carries no closing keyword, so #840 needs closing by hand after the merge.

## Clone state

`receipts/clone_state.txt`: head and tree exact, index tree equal, no status lines, 1473 tracked entries with no mode or blob mismatch, six gitlinks recorded. A `git fetch` of `dev` updated only remote-tracking state in this clone.

R775-3 FINISHED
