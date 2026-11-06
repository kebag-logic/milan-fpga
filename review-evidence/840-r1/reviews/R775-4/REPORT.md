[R775] POSITIVE - exact head 27df6e08cf157b9c5e4b0fdb7da2fa28d8ab83fa

# R775-4: internal independent review of PR #842 (issue #840)

- Head `27df6e08cf157b9c5e4b0fdb7da2fa28d8ab83fa`, tree `25d62820b5a41a49368ef027aac7e9a531dd93b5`.
- Delta reviewed: `3d1ca52f..27df6e08`, one commit, under the round 5 ruling on #840 (issuecomment-6685367720).
- Source base and live dev: `87e9d03aa2a4797957ac0124d0c7851a2eec234c`, rechecked at review time. One merge base.
- Reviewed in an isolated detached clone. No source edits, commits, pushes or GitHub writes were made.

## Verdict

POSITIVE. There is no BLOCKER, MAJOR or MINOR open. All five lenses are clean at this head.

All three ruling items hold at their cause:

- **Item 1 holds.** Bits 0.11 and 0.14 start in opposite states across the two gigabit arms. Each is forced and dropped by a mutant caught by name, and the start values and assertions are what catch them.
- **Item 2 holds.** Every claim now names the twelve graded bits and states that the others are unmodified by construction and not graded. I derived the list from the firmware's macros and it matches. All 26 force and drop mutants of the named ungraded bits escape, so "not graded" is true as well.
- **Item 3 holds.** No digest needed moving. No tracked file names any of the five changed files at their old bytes, and the command table is unchanged.

R775-3 N3 = R776-3 F6 is resolved. Two new wording items are recorded as RESIDUE, and three earlier residues are retained. None affects the verdict.

## Assigned focus

### 1. Register 0's power-down and loopback: holds

The start values decode as the comments say.

| Arm | Start in `phy_host.c` | Bit 0.11 | Bit 0.14 | Value written |
|---|---|---|---|---|
| First, auto-negotiation enabled | `:135` `0x9c00` | 1 | 0 | `0x1a00` |
| Second, auto-negotiation disabled | `:343` `0x6100` | 0 | 1 | `0x7300` |

The written values come from `receipts/test_phy_firmware.head.log`. Both equal `(start | 0x1200) & ~0x8400`, so each bit is kept as read.

`test_phy_firmware.py` is rc 0 at this head in 42 s, against the 180 s bound at `test_nvm_firmware.py:989`. It reports 51 advertisement, 4 poll and 5 boot-path mutants caught, then `PHY_BOOT_OK`. The four new mutants fail on their named assertions, and each fails in the arm the design predicts (`receipts/opposite_state_probe.log`):

| Mutant | Assertion | Arms passed before the abort |
|---|---|---:|
| `force-bit-0.11` | `power_down_kept` | 1 |
| `drop-bit-0.11` | `power_down_kept` | 0 |
| `force-bit-0.14` | `loopback_kept` | 0 |
| `drop-bit-0.14` | `loopback_kept` | 1 |

The start values and the assertions are the cause. Each driver variant below ran unmutated at rc 0, and the mutants shown then escape:

| Driver variant | Escapes | Still caught |
|---|---|---|
| First arm at `0x9400` | `drop-bit-0.11` | `force-bit-0.11` |
| Second arm at `0x6900` | `force-bit-0.11` | `drop-bit-0.11` |
| First arm at `0xdc00` | `force-bit-0.14` | `drop-bit-0.14` |
| Second arm at `0x2100` | `drop-bit-0.14` | `force-bit-0.14` |
| `assert(power_down_kept)` removed | both 0.11 mutants | none |
| `assert(loopback_kept)` removed | both 0.14 mutants | none |

Three defects the table does not spell also fail by name: register 0 rebuilt from constants, both bits cleared together, and both forced together.

No test was weakened. The table goes from 47 to 51 entries: four added, none removed, none changed (`receipts/table_compare.log`). That includes the `kept_bit_mutants()` refactor, which leaves the twenty register 4 and 9 rows identical. The driver gains two assertions and loses none. Every earlier assertion still passes from the new start values, and `phy_resolved_status()` takes the same branches, because bit 0.12 is unchanged in each arm.

### 2. Claims name what is graded: holds

The firmware's own macros give this partition (`receipts/pass_through_probe.log`):

| Register | Pass-through bits | Graded | Other |
|---|---|---|---|
| 4 | 15, 13, 12, 11, 10, 4 to 0 | 11, 10, 4 to 0 | 15, 13, 12 |
| 0 | 14, 13, 11, 8 to 0 | 14, 11 | 13, 8 to 0 |
| 9 | 12 to 10 | 12 to 10 | none |

- Graded total: 12. That is the "twelve" at `BAREMETAL_FIRMWARE.md:2196` and `phy_host.c:129`.
- The "other" column equals the guide's list at `:2197` exactly.
- All 26 force and drop mutants of those 13 bits exit rc 0, so the words "not graded" are true and not merely cautious.
- `milan_baremetal.c:1065-1069` applies only named masks, so "unmodified by construction" is correct.

Each place the ruling named was changed:

| Ruling location | At this head |
|---|---|
| `BAREMETAL_FIRMWARE.md:2195` | `:2195-2197` names the five fields, the count and the ungraded bits |
| `phy_host.c:122-126` | `:127-133` says "twelve bits", then the disclaimer |
| `test_phy_firmware.py:80` | `:84-86` says "each kept field the peer grades", with the disclaimer (see RES-B) |
| `test_phy_firmware.py:88` | `:95` says "Each bit of a graded field" |
| PR body | `:69` names the bits and cites `milan_baremetal.c:1065-1069`; `:104` is the round 4 record and says "the ten bits of the selector, pause and MASTER-SLAVE fields", which is exact |

No "each kept", "every kept" or "any kept" claim remains in the tree or the PR body. "forty-seven" survives only at PR body `:109`, in the dated round 4 record. The count "fifty-one" is exact at both `BAREMETAL_FIRMWARE.md:2199` and `STRICTER_READINGS.md:73`.

### 3. Digests: holds, and nothing needed moving

- `ci/image/command-table.json` and `ci/image/tool-inventory.json` do not mention any of the five changed files, and the command table's blob is unchanged since `3d1ca52f`.
- A search of the five old sha256 values and blob ids across every tracked file at head finds nothing (`receipts/old_digest_search.log`).
- `ci/image/exec-audit-receipt.json` records `test_phy_firmware.py` at `c394cbfa`. That equals neither base, head nor dev (`a35eda0b`), so it is a past traced population and this delta did not stale it. No file under `scripts`, `.github` or `ci` names that receipt as an input.
- The script rows report 41 mismatches at dev, `3d1ca52f` and head, with none added or removed (`receipts/command_table_scripts.log`).
- My 41 reconciles with the author's 37. Both include 36 true byte mismatches and 1 absent file. My count adds the 4 submodule rows, which are not superproject blobs.
- `docs_inventory.py --check` is rc 0. The audit page moves only by the generator's line counts: `BAREMETAL_FIRMWARE.md` 2361 to 2363, total 92,393 to 92,395, D0-062 2312 to 2314.

## Findings

No BLOCKER, MAJOR or MINOR.

### RES-A - RESIDUE - Tests, Docs - `sw/firmware/nvm_hosttest/phy_host.c:123-134`

- **Authority/evidence:** `phy_host.c:336-337` says the second arm's bit 0.14 is set only to grade its keep and that the peer models no loopback. The first arm's comment has no matching sentence for bit 0.11, although it opens "Standard 1000BASE-T full-duplex negotiation" and that arm publishes a link with power-down set. `phy_peer.h:57` stores the bit and models nothing. The author's open risk 2 says this publicly.
- **Impact:** A reader could take the first arm as a model of a powered-down PHY that links. No claim is false and nothing measured changes.
- **Required outcome:** After `That arm also grades the auto-negotiation enable bit.`, add: `Bit 0.11 starts set only to grade its keep: the peer stores it and models no power-down.`
- **Verification:** The comment is present, and `test_phy_firmware.py` stays rc 0.

### RES-B - RESIDUE - Tests, Docs - `sw/firmware/nvm_hosttest/test_phy_firmware.py:84`

- **Authority/evidence:** The comment says "each kept field the peer grades". The assertions are in the host driver, and the guide says so at `BAREMETAL_FIRMWARE.md:2199`: "The host driver grades each property by name". The peer only stores what it is written. The wording came from a suggested fix in R776-3 F6.
- **Impact:** A small inconsistency about who grades. Nothing measured changes.
- **Required outcome:** `#: #840: each kept field the host driver grades: its register, its bits and the`
- **Verification:** The comment reads so, and `test_phy_firmware.py` stays rc 0.

### Retained residue

| ID | Where | Defect | Exact fix |
|---|---|---|---|
| RES-1 = R776-3 R5 | PR title | Still names `02:4B:4C:00:00:01` (rechecked live) | `Prototype identity 02:4B:4C:4B:4C:01, 1000BASE-T-only advertisement on 1G PHYs, and the stricter-reading page (#840)` |
| RES-4 = R776-3 R6 | `docs/reference/STRICTER_READINGS.md:45` | "The builder gate" reads as the builder | `- Gate 28b refuses a zero octet in any tracked config.` |
| RES-5 = R776-3 R7 | `docs/findings/397_SERVICE_BUDGET.md:290-291` | The colon sentence is split from its table by a parenthetical | Move line 291 below the table |

The comment rule has no new instance. A scan of the lines this delta adds under `sw` and `docs` finds no bench lane label, review round, reviewer ID or comment ID. The commit is one line with no body or trailer.

### Suggestions

- **S9 - Tests - `phy_host.c:135`, `:343`.** R775-3 S8 now reaches the two new bits. Bit 0.11 is set only in the auto-negotiation-enabled arm and bit 0.14 only in the disabled arm, so a defect conditional on that state could hide. This comes from reading the start values and I did not probe it. Such a mutant is artificial, so this is optional.

## Prior public findings

| Finding | Severity, lenses | Disposition at this head | Evidence |
|---|---|---|---|
| R775-3 N3 = R776-3 F6 | MINOR; Tests, Docs | **RESOLVED** at its cause: two bits graded, every claim narrowed, the remainder named | Focus 1 and 2 |
| R775-2 N1, N2 = R776-2 F5, R776-2 F4 | MINOR; Tests | **Resolved** by R775-3. The delta leaves those arms and rows intact | All 47 earlier mutants unchanged and caught; table blob unchanged |
| R775-1 and R776-1 F1, F2, F3 | MAJOR and MINOR | **Resolved** earlier. The delta touches nothing they depend on | Empty firmware and service diff |
| RES-1, RES-4, RES-5 (R5, R6, R7) | RESIDUE | **Retained**, exact fixes above | Live title; files unchanged |
| R775-2 RES-2, RES-3 | RESIDUE | **Resolved** by R775-3 | Delta does not touch them |
| R775-3 S6 = R776-3 S6 | SUGGESTION | **Retained, not taken.** Still for #838 | Delta does not touch it |
| R775-3 S7 | SUGGESTION | **Retained.** The comment is now at `phy_host.c:165-167` | Unchanged |
| R775-3 S8 | SUGGESTION | **Retained**, widened as S9 | Above |
| R776-3 S7 | SUGGESTION | **Retained, not taken** | Firmware unchanged |
| R775-2 S1, S3, S4, S5; R776-2 S3, S4, S5; R775-1 S2; R776-1 S2 | SUGGESTION | **Retained, not taken** | Delta does not touch them |

Ruling item 3 makes any request for the remaining pass-through bits residue, so I raise none.

## Lens results

```text
[R775] PASS Conformance - issuecomment-6685367720 items 1 to 3 against phy_host.c:74-75,92-93,135,343, test_phy_firmware.py:84-91, BAREMETAL_FIRMWARE.md:2195-2199, PR body:69, ci/image/command-table.json - each ruling item met; firmware and identity diff empty, so the issue's acceptance keeps its earlier result
[R775] PASS RTL - git diff 3d1ca52f..27df6e08 on hdl, syn, constraints, sw/litex, configs, sw/firmware/milan_baremetal and the gitlinks - empty, and milan_baremetal.c blob 780b5c56 is identical at both heads, so no RTL or firmware artifact is in scope
[R775] PASS Robustness - phy_host.c:135,343 start values through the refusal arms :150-183, the 10/100 arms and phy_peer.h:42-62; receipts/test_phy_firmware.head.log - the new bits change no refused-read, retry, reset, restart or resolution path; all earlier mutants still fail by name
[R775] PASS Tests - test_phy_firmware.py KEPT_FIELDS, phy_host.c:74-75,92-93; receipts/opposite_state_probe.log, pass_through_probe.log, table_compare.log - each new test fails for its defect, six driver variants prove the cause, 26 named ungraded mutants escape as stated, and no earlier mutant changed
[R775] PASS Docs - BAREMETAL_FIRMWARE.md:2195-2199, STRICTER_READINGS.md:73, DOCUMENTATION_AUDIT.md, PR body:3,69 against the derived bit partition; receipts/docs_gates.log - claims match execution; inventory, style and git diff --check rc 0; RES-A, RES-B and three retained residues are wording only
```

## Published evidence

- Round 5 receipts are on `840-review-evidence` at `cca4a4ceb2d9f8f6202ac765d16aa688a603799d`. The assignment's `194f3733` holds only the round 1 packet.
- That commit is **unsigned**, so the packet is hash-manifested and not signed.
- 14 fetched files match `MANIFEST.json` with no mismatch (`receipts/evidence_check.log`). This is a spot-check of the 182 listed round 5 files.
- The `PHY_*` lines of the author's `phy_firmware.log` equal my own run, apart from the `delay_cycles` field, which my comparison strips.
- The author's `arm_probe.log` agrees with my independent variants.
- `repository-state.txt` agrees with the clone, and the published `PR-BODY.md` equals the live body apart from a trailing newline.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling items 1 to 3; `phy_host.c`; `test_phy_firmware.py`; guide; PR body; command table | R775-4 | 27df6e08cf157b9c5e4b0fdb7da2fa28d8ab83fa |
| RTL | CLEAN | Empty diff on `hdl`, `syn`, `constraints`, `sw/litex`, `configs`, firmware and gitlinks; blob identity of `milan_baremetal.c` | R775-4 | 27df6e08cf157b9c5e4b0fdb7da2fa28d8ab83fa |
| Robustness | CLEAN | `phy_host.c` arms; `phy_peer.h`; head test log | R775-4 | 27df6e08cf157b9c5e4b0fdb7da2fa28d8ab83fa |
| Tests | CLEAN (RES-A, RES-B wording only) | `phy_host.c`, `test_phy_firmware.py`; head run; 6 driver variants; 3 extra defects; 26 ungraded-bit mutants; table comparison | R775-4 | 27df6e08cf157b9c5e4b0fdb7da2fa28d8ab83fa |
| Docs | CLEAN (five residues, wording only) | `BAREMETAL_FIRMWARE.md`, `STRICTER_READINGS.md`, `DOCUMENTATION_AUDIT.md`, PR body; inventory, style and diff checks | R775-4 | 27df6e08cf157b9c5e4b0fdb7da2fa28d8ab83fa |

Under the owner's later-round rule, code this delta does not touch keeps the verdict of its earlier covering rounds, and the empty diffs above carry that verdict to this head.

## Real limits

- **Reading order.** The ruling and the author's REVIEW READY comment name N3 = F6, and I read both first, as the assignment's order requires. I read the R775-3 and R776-3 reports after my pass over the diff and after the opposite-state probes. `pass_through_probe.py` ran after that reading, to test N3's disposition. My verdict and ledger were written last. I did not open the `reviews` directory on the evidence branch or any fourth-round report.
- **My own probe error.** The first run of `opposite_state_probe.py` flagged one row as unexpected. My expected name for forcing both bits was wrong: the first arm starts with power-down set, so `loopback_kept` fires first. The mutant was caught either way. I corrected the expectation and reran, and the published log is the rerun. A rough digest walker that also counted a directory row was superseded by `receipts/command_table_scripts.log` and is not published.
- **The peer models neither bit.** These arms grade the written value and not link behaviour. That forcing 0.11 or 0.14 would break the link is the ruling's reasoning, not something this test shows.
- **Clause text.** I did not open IEEE 802.3. The citations 22.2.4.1.2 and 22.2.4.1.5 and the bit names rest on my knowledge of Clause 22. A text search of `ti_eth.pdf` in the repository found no Clause 22 control register description.
- **Author gates read from receipts, not rerun:** `docs.yml` (table: 65 rc 0, 31 not run with a reason, 0 bad), `docs_inventory.py --selftest`, and the privacy check (0 private lines). I ran `docs_inventory.py --check`, `check_doc_style.py`, `git diff --check` and `test_phy_firmware.py` myself.
- **`ci_tool_inventory.py --check`** was not run by me or, this round, by the author. Its #838 refusal is recorded at `3d1ca52f`. The digest conclusions rest on the direct comparisons above.
- **Not run at this head:** full sweep, service plans, capture arms, standalone builder. The sweep record stays at `cadb63b4`. No manager source bank ran at this head and I infer none.
- **Scoped Verilator.** Not used: the probes are host compiles, so I did not verify its identity.
- **Hardware.** Physical calibration NOT RUN, and field skips are not hardware proof.
- **Hosted.** At 2026-11-06T13:42:14Z the head had 6 runs successful, 1 skipped, 17 in progress and 23 queued (`receipts/hosted_snapshot.log`). That is not hosted acceptance, and I draw nothing from it.

## Pending manager duties

- The current-dev merge-candidate build, with builder and native banks, and hosted and act acceptance.
- RES-A, RES-B, RES-1, RES-4 and RES-5 on the residue checklist.
- Decide whether S6 goes onto #838.
- The #840 title and body still state the round-1 identity, so a cold reader needs a pointer to the later decision.
- The PR carries no closing keyword, so #840 needs closing by hand after the merge.
- The second independent positive review, which this report does not supply.

## Clone state

`receipts/clone_state.txt`: head, tree and index tree exact; `git status` with ignored files empty; 1467 tracked blobs with no byte or mode mismatch; six gitlinks recorded, none changed by this delta. The bytecode caches my runs created were removed before that check.

## Reproduce

Each script is in this packet. `<clone>` is a checkout of the exact head with submodules, and `<work>` is a scratch directory.

```sh
python3 -B opposite_state_probe.py <clone> <work>
python3 -B pass_through_probe.py <clone> <work>
python3 -B table_compare.py <clone> <base copy of test_phy_firmware.py>
cd <clone> && python3 -I <packet>/digest_probe.py 3d1ca52f 27df6e08
```

R775-4 FINISHED
