[R776] POSITIVE - exact head 27df6e08cf157b9c5e4b0fdb7da2fa28d8ab83fa

# R776-4: external independent review of PR #842 (issue #840)

- Head `27df6e08cf157b9c5e4b0fdb7da2fa28d8ab83fa`, tree `25d62820b5a41a49368ef027aac7e9a531dd93b5`.
- Delta reviewed: `3d1ca52f..27df6e08`, one commit, five files, under the round 5 ruling (issue comment 6685367720).
- Base and live dev: `87e9d03aa2a4797957ac0124d0c7851a2eec234c`, one merge base.

## Verdict

POSITIVE. All three ruling items are met, and R775-3 N3 = R776-3 F6 is resolved at its cause. No BLOCKER, MAJOR or MINOR is open. Two new RESIDUE items and three retained ones go to the checklist.

This verdict covers source review at this head. It is not hosted acceptance, candidate-merge validation or hardware proof.

## Ruling items

### 1. Power-down and loopback start in opposite states, each with a mutant caught by name: met

| Bit | Arm 1 start `0x9c00` | Arm 2 start `0x6100` | Assertion | Mutants |
|---|---|---|---|---|
| 0.11 power-down | 1 | 0 | `power_down_kept`, `phy_host.c:74`, `:92` | `force-bit-0.11`, `drop-bit-0.11` |
| 0.14 loopback | 0 | 1 | `loopback_kept`, `phy_host.c:75`, `:93` | `force-bit-0.14`, `drop-bit-0.14` |

- **Run at this head:** `test_phy_firmware.py` exits 0, with 55 poll and advertisement mutants (51 advertisement, 4 poll) and 5 boot-path mutants caught, and `PHY_BOOT_OK`. All four new mutants fail their named assertion (`receipts/test_phy_firmware.head.log`).
- **Written values:** arm 1 writes `0x1a00` and arm 2 writes `0x7300`, so each arm keeps its own state of both bits.
- **The start values are the cause.** Undoing each one in turn lets exactly the mutant it exposes escape (`receipts/phy_keep_matrix.json`):

| Start value changed | Mutant that then escapes |
|---|---|
| Arm 1 to `0x9400` (power-down clear) | drop 0.11 |
| Arm 2 to `0x6900` (power-down set) | force 0.11 |
| Arm 1 to `0xdc00` (loopback set) | force 0.14 |
| Arm 2 to `0x2100` (loopback clear) | drop 0.14 |

- **The assertions are the only guard.** With `assert(power_down_kept)` or `assert(loopback_kept)` removed, that bit's force and drop mutants both escape, so nothing else catches them.
- **Other start bits still hold.** `0x9c00` keeps bits 15 and 10 set, so the guide's "starts every bit the PHY init clears at one" stays true. `0x6100` still reads as forced 100 Mb/s full duplex with auto-negotiation off, so the arm 2 comment stays true.

### 2. Every claim names the graded bits and says the others are not graded: met

I forced and dropped all 25 pass-through bits of registers 4, 9 and 0, giving 50 rows. The result matches the text exactly:

- **24 rows caught:** the twelve stated bits, forced and dropped, by the five named assertions.
- **26 rows escape:** 4.15, 4.13, 4.12, 0.13 and 0.8 to 0.0, which are exactly the bits the guide lists as not graded.
- **Disagreements with the stated bits:** 0.

The list is complete. `milan_baremetal.c:1063-1069` shows register 9 has no pass-through bit beyond MASTER-SLAVE, so "registers 4 and 0" is the right scope, and bits 4.14, 0.15, 0.12, 0.10 and 0.9 are all set or cleared by the init. Those line numbers include the ruling's `1065-1069`.

| Place named by the ruling | Text at this head |
|---|---|
| `BAREMETAL_FIRMWARE.md:2195-2197` | Names the five fields, "those twelve bits", and the ungraded bits by number |
| `phy_host.c:127-133` | Twelve bits with each start pattern; the others "unmodified by construction and not graded" |
| `test_phy_firmware.py:84-86`, `:95` | "each kept field the peer grades"; "Each bit of a graded field" |
| PR body round 5 line and firmware test row | Names the twelve bits and the ungraded bits, and cites `milan_baremetal.c:1065-1069` |

A repository-wide search finds no "each kept bit", "every kept bit", "any kept bit" or "forty-seven". The live PR body keeps "forty-seven" and "47" only in its dated Round 4 section, which is a correct record of that round. "Fifty-one" is correct in both documents (27 named plus 24 kept-bit mutants).

Item 3 of the ruling is also respected: the test does not extend to the remaining bits. Those 26 escaping rows are RESIDUE by the ruling, and I raise no finding on them.

### 3. Digests: met, nothing needed re-pinning

- **Pins of the changed files.** I searched the head tree for the sha256 and git blob id of all five changed files, at both their old and new bytes. There are 0 pins (`receipts/final_checks.log`). None of the five is in `ci/image/command-table.json` or `ci/image/tool-inventory.json`.
- **`exec-audit-receipt.json`.** It names `test_phy_firmware.py` with a digest that matches neither side of this delta. It is a snapshot of commit `54fbcba6`, not a pin, and this delta did not move it.
- **Command table against dev.** The mismatch sets are identical, with none added and none removed.
- **This PR's rows.** There are 3 matching and 2 stale (`endstation_builder.py`, `test_builder.py`), and the same two rows are stale at dev.
- **The author's count of 37 reconciles:** 36 stale rows in the parent tree plus 1 absent file. Two further stale rows sit inside submodules and are the same at dev.
- **Generated inventory.** `docs_inventory.py --check` and `--selftest` pass. The audit's +2 lines match the guide's +4/-2 edit.

## Findings

No BLOCKER, MAJOR or MINOR.

### R8 - RESIDUE - Docs - `sw/firmware/nvm_hosttest/phy_host.c:130-134`

- **Lenses:** Docs.
- **Authority/evidence:** `phy_host.c:336-337` says the peer stores 0.14 and models no loopback. Arm 1 starts 0.11 set and then publishes a 1000 Mb/s link, with no matching sentence, although the author's REVIEW READY states it publicly. Separately, "That arm" at `:134` now sits two sentences from "the arm below" at `:128-129`.
- **Impact:** A reader of arm 1 may think the peer links while powered down. Nothing is measured or claimed differently.
- **Required outcome, exact fix:** After "changes it in one arm." add `The peer stores power-down and loopback and models neither.` Change the last sentence to `The arm below also grades the auto-negotiation enable bit.`
- **Verification:** Read the comment, and confirm `test_phy_firmware.py` stays rc 0.

### R9 - RESIDUE - Docs - PR body lines 15 and 113

- **Lenses:** Docs.
- **Authority/evidence:** The Contents entry for Round 4 says "with this head's gates", and the Round 4 section says "at this head and at dev". Those gates ran at `3d1ca52f`, and the head is now `27df6e08`.
- **Impact:** A cold reader could attach round 4 results to the wrong head. The Status section already separates the heads correctly.
- **Required outcome, exact fix:** Line 15: `with the gates at `3d1ca52f``. Line 113: `at `3d1ca52f` and at dev`.
- **Verification:** Read the PR body.

The comment rule has no new instance. A scan of the lines added under `sw`, `docs/integration` and `docs/reference` finds no bench lane label, review round, reviewer ID or comment ID. The commit is one line with no trailers.

## Suggestions

- **S9 - Tests - `phy_host.c:135`, `:343`.** This extends R775-3 S8 to the new bits. Each informative state of 0.11 and 0.14 sits in only one auto-negotiation state, so all four conditional mutants escape (`cond-drop-0.11-when-an-off`, `cond-force-0.11-when-an-on`, `cond-force-0.14-when-an-off`, `cond-drop-0.14-when-an-on`). They are artificial, and the guide's claim is about plain forcing and dropping, so this is optional.

## Prior public findings

I read these only after recording my verdict and ledger.

| Prior finding | Severity, lenses | Disposition at this head | Evidence |
|---|---|---|---|
| R775-3 N3 = R776-3 F6 | MINOR; Tests, Docs | **RESOLVED** at its cause: two bits graded, every claim narrowed to what is graded | Ruling items 1 and 2 |
| R775-2 N1; R775-2 N2 = R776-2 F5; R776-2 F4 | MINOR; Tests | **RESOLVED.** The delta keeps them: the arms' other start values and the four refusal arms are unchanged | `test_phy_firmware.head.log` |
| R775-1 and R776-1 findings | MAJOR, MINOR | **RESOLVED** in earlier rounds. Nothing they depend on changed | Empty diff on firmware, RTL, LiteX, builder, configs, `tb` and submodules |
| R5 (= R775-2 RES-1, R776-2 R3), PR title | RESIDUE | **RETAINED.** The title still names `02:4B:4C:00:00:01`. Fix: `Prototype identity 02:4B:4C:4B:4C:01, 1000BASE-T-only advertisement on 1G PHYs, and the stricter-reading page (#840)` | Live PR title |
| R6 (= R775-2 RES-4), `STRICTER_READINGS.md:45` | RESIDUE | **RETAINED.** Fix: `- Gate 28b refuses a zero octet in any tracked config.` | File unchanged at that line |
| R7 (= R775-2 RES-5), `397_SERVICE_BUDGET.md:290-291` | RESIDUE | **RETAINED.** Fix: move line 291 below the table | File unchanged |
| R775-3 S6 = R776-3 S6, `tool-inventory.json` | SUGGESTION | **RETAINED**, for #838. This delta adds nothing to it | No changed file is named there |
| R775-3 S7, R776-3 S7 | SUGGESTION | **RETAINED**, optional | Code unchanged |
| R775-3 S8 | SUGGESTION | **RETAINED**, optional, and extended by S9 | `receipts/phy_keep_matrix.json` |
| Earlier suggestions (R775-1 S2, R776-1 S2, R775-2 S1, S3, S4, S5, R776-2 S3, S4, S5) | SUGGESTION | **RETAINED**, optional. The delta does not touch them | R776-3 table |

## Lens results

```text
[R776] PASS Conformance - git diff 3d1ca52f..27df6e08 against issue comment 6685367720, milan_baremetal.c:1063-1069, phy_host.c:49-50 - all three ruling items met; the firmware is unchanged, so the advertisement, identity and settled maintainer points keep the prior result; clause numbers 22.2.4.1.2 and 22.2.4.1.5 match the bit names
[R776] PASS RTL - git diff 3d1ca52f..27df6e08 on hdl, syn, sw/litex, sw/firmware/milan_baremetal, configs and all six gitlinks - empty, so no RTL, timing or firmware artifact is in scope and the prior result stands
[R776] PASS Robustness - phy_host.c:143-193, :331-358, phy_peer.h:54-60, receipts/phy_keep_matrix.json - the refused-read retries still end in one write set, advertised_once holds, initial[] is captured after each arm sets its registers, and the new start bits change no retry or resolution path
[R776] PASS Tests - phy_host.c:74-75, :92-93, :135, :343, test_phy_firmware.py:81-109, receipts/test_phy_firmware.head.log, receipts/phy_keep_matrix.json - the four new mutants fail by name, each start value and each assertion is load-bearing, 50 force and drop rows match the stated bits with 0 disagreements, and my mutant lines equal the author's published log
[R776] PASS Docs - BAREMETAL_FIRMWARE.md:2194-2199, STRICTER_READINGS.md:73, DOCUMENTATION_AUDIT.md, live PR body - every claim matches execution; docs_check, check_feature_status and docs_inventory --check and --selftest pass; only RESIDUE R5 to R9 remain
```

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling, delta, `milan_baremetal.c:1063-1069`, clause references | R776-4 | `27df6e08cf157b9c5e4b0fdb7da2fa28d8ab83fa` |
| RTL | CLEAN | Empty diff on RTL, firmware, LiteX, configs, gitlinks | R776-4 | `27df6e08cf157b9c5e4b0fdb7da2fa28d8ab83fa` |
| Robustness | CLEAN | Refusal and rediscovery arms, `phy_peer.h`, probe receipts | R776-4 | `27df6e08cf157b9c5e4b0fdb7da2fa28d8ab83fa` |
| Tests | CLEAN | `phy_host.c`, `test_phy_firmware.py`, head run, 50-row matrix, necessity controls | R776-4 | `27df6e08cf157b9c5e4b0fdb7da2fa28d8ab83fa` |
| Docs | CLEAN (RESIDUE R5 to R9 carried) | Guide, stricter-readings page, audit page, PR body, inventory gates | R776-4 | `27df6e08cf157b9c5e4b0fdb7da2fa28d8ab83fa` |

## Real limits

- **Reading order.** While listing PR comments to find the round 3 findings, I saw the first 140 characters of R775-4's comment, which show its verdict line and title. I did not open it, and it was public before my verdict was recorded. I read no other part of it. I read the round 3 reports only after recording my verdict and ledger.
- **Evidence integrity.** The assigned link `194f3733` holds only the round 1 packet, for head `dd764ed7`. Its manifest matched on 4 of 4 sampled files. The round 5 packet is `author-r5` on `840-review-evidence` at `cca4a4ce`. I found no manifest at that packet's top level. These commits are unsigned, so I verified no signature. I did check that the one `tree-after` file I sampled names this head with a clean status, that it holds 65 step rc files, that nine gate rc files read 0, and that its PR body matches the live one.
- **Author gates read, not rerun:** the full `docs.yml` run, and `push-privacy-check.py`, which is not tracked in the repository. For privacy I read its rc and ran my own scan of the added lines.
- **`ci_tool_inventory.py --check`:** not run.
- **Sweep, service plans, builder:** not run at this head, by assignment. The sweep record stays at `cadb63b4`.
- **Peer model.** The peer stores 0.11 and 0.14 and models neither, so these arms grade the written value, not link behaviour.
- **Clause text.** I did not reopen the standards. The Clause 22 bit names and clause numbers are from my own knowledge of them.
- **Scoped Verilator:** not used. The probes are host compiles, so no RTL simulator was needed.
- **Probe rerun.** One rerun of my matrix failed at link time because my own scratch bench kept a generated header. I cleared it and reran; the published receipt is from the fresh run. The head was not involved.
- **Hardware.** Physical calibration NOT RUN. Everything here is at the pin-level peer, and field skips are not hardware proof.
- **Hosted.** At 13:52Z the head had 47 check runs: 10 completed success, 1 skipped, 19 in progress, 17 queued, and none failed. A later poll gave the same counts. `docs-gates-0` to `-2` were still in progress and `firmware-unit` was queued. I draw no acceptance from this.

## Pending manager duties

- Build and validate the current-dev merge candidate, builder and native banks, and link the receipts on the PR.
- Own hosted and local-replica acceptance at the exact head, including the jobs still running above.
- Carry R5 to R9 to the residue checklist. R8 edits a source comment, so taking it creates a new head; the ledger rule then applies to `Tests` and `Docs` scope.
- Confirm the second positive and the full completion bar. Merge needs explicit maintainer authorization.

## Clone state

No probe edited the clone. `HEAD` and tree match the assignment, `git status --porcelain` is empty, the index and `HEAD` have the same blob, mode and path digest (`3e9836b08403159c`), and all six gitlinks are unchanged (`receipts/final_checks.log`).

R776-4 FINISHED
