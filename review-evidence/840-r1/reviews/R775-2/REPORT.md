[R775] NEGATIVE - exact head beb38447d07cceac5170ba0a35c7615f5714b7f7

# R775-2: internal cleared-context review of PR #842 (issue #840)

- Head: `beb38447d07cceac5170ba0a35c7615f5714b7f7`, tree `ba0183c2c52237818d6a08120b620d53e2e490c4`.
- Delta reviewed: `dd764ed7..beb38447`, which is rounds 2 and 3. Source base and live dev: `cc204c6fd2349b543d73f15c97162a2c4434c86e`.
- Reviewed in an isolated detached clone. No source edits, commits, pushes or GitHub writes were made.
- My verdict and ledger were fixed before I read any prior review (`receipts/own-verdict-before-prior-findings.md`). No other reviewer's round-2 report was read.

## Verdict

NEGATIVE. There are two MINOR findings, both under Tests, and no MAJOR or BLOCKER.

The firmware itself is right, and the round's main work holds:

- **F3 (MAJOR) is resolved at its cause.** No enforced plan reports a PHY finding, and the head's ROM image is byte-identical to the one the receipts measured.
- **F2 is resolved.** Every figure I checked equals the committed receipt.
- **The identity and the round-3 merge are correct.**
- **All sixteen named round-1 mutants now fail by name.**

Two test gaps stay open:

- **N1:** the kept fields are graded only from all-ones. A firmware that forces manual MASTER-SLAVE on passes every test. This is F1's cause, surviving in mirror image.
- **N2:** the guide says an unacknowledged read of registers 15, 4, 9 or 0 writes nothing. Only 15 and 9 are graded. The firmware behaves correctly on all four.

One small harness change closes both. `receipts/phy_fix_probe.txt` shows that a temporary copy of `phy_host.c` with changed start values and two NAK arms passes the committed firmware and fails all five mutants by name.

## Findings

### N1 - MINOR - Tests - kept fields are graded only from all-ones

- **Where:**
  - The start values: `sw/firmware/nvm_hosttest/phy_host.c:128`, `:130`, `:313`, `:315`.
  - The assertions: `phy_host.c:62`, `:66`.
  - The claim: `phy_host.c:119`, and `docs/integration/BAREMETAL_FIRMWARE.md:2177`, `:2179`, `:2194-2195`.
- **Authority:** AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect". Issue #840 round-2 assignment item 2: the peer exercises "every documented keep and clear".
- **Evidence.** A keep is an identity on the field, so it needs more than one start value. Both gigabit arms start register 4 at `0x4fe1` and register 9 at `0xfdff`, so pause and MASTER-SLAVE only ever start at ones. `pause_bits_kept` and `master_slave_kept` compare against those same ones. Three planted mutants escape with rc 0 (`receipts/phy_own_mutants.txt`):

  | Mutant | Planted defect |
  |---|---|
  | `force-manual-master` | register 9 always written with bits 12 to 10 set |
  | `force-manual-config-only` | register 9 always written with bit 12 set |
  | `force-pause-on` | register 4 always written with both pause bits set |

- **Impact.** The untested half is the ordinary state. The repository's own service peer models register 9 as `0x0300`, with MASTER-SLAVE at zero (`tb/verilator/fw_service_budget/phy.hpp:100`), and that peer does not grade writes. A regression that forces manual MASTER-SLAVE configuration would override automatic resolution on the board, and it would ship green. Round 1's fixture had the mirror gap: bits at zero, so a dropped field escaped.
- **Why Tests only.** The documented firmware behaviour is true at this head, and no doc figure or claim changes. The fix is to the test.
- **Required outcome.** At least one gigabit arm starts each kept field so that both forcing and dropping change it, for example a mixed pattern. The named assertions then grade it.
- **Verification.** The three mutants fail on `master_slave_kept` and `pause_bits_kept`, and `test_phy_firmware.py` stays green. `receipts/phy_fix_probe.txt` shows this works with `0x47e1` and `0xedff` in the auto-negotiation-disabled arm.

### N2 - MINOR - Tests - the documented retry is graded for two of four registers

- **Where:**
  - The claim: `docs/integration/BAREMETAL_FIRMWARE.md:2183`, "An unacknowledged read of registers 15, 4, 9 or 0 writes nothing; the next poll retries."
  - The arms: `sw/firmware/nvm_hosttest/phy_host.c:139`, `:146`, registers 15 and 9 only.
  - The product check: `sw/firmware/milan_baremetal/milan_baremetal.c`, `if (advertisement < 0 || gigabit < 0 || control < 0)`.
- **Authority:** AGENTS.md section 5, "test negative, boundary, reset, ordering, and failure paths where relevant", and section 6, Tests.
- **Evidence.** Dropping either check escapes with rc 0: `nak-reg4-not-checked` and `nak-reg0-not-checked` (`receipts/phy_own_mutants.txt`). The existing `write-unread` mutant removes the whole condition, so register 9's arm catches it and hides this.
- **Impact.** With the register 0 check dropped, a single failed read would write `0x7bff`, which sets loopback and power-down. With the register 4 check dropped, it would write `0xbc1f`. Either passes the gate the guide cites. The shipped firmware does neither (see Robustness).
- **Why Tests only.** `receipts/phy_nak_probe.txt` runs the unmutated firmware with register 4 and then register 0 unacknowledged. Each poll writes nothing and the next poll advertises normally, so the guide's statement is true.
- **Required outcome.** Registers 4 and 0 each get a NAK arm with a named assertion, and both mutants join the table.
- **Verification.** Both mutants fail by name. `receipts/phy_fix_probe.txt` shows this with `no_write_before_register_4_read` and `no_write_before_register_0_read`. The register 4 arm must not use `expect_poll(now, 0)`: that poll publishes 5 from the pre-init advertisement, because the resolution path does not need register 4 there.

## Residue

Each item below is wording only. None changes a figure, verdict, test or claim.

| ID | Where | Defect | Exact fix |
|---|---|---|---|
| RES-1 | PR title | Names the round-1 address | `Prototype identity 02:4B:4C:4B:4C:01, 1000BASE-T-only advertisement on 1G PHYs, and the stricter-reading page (#840)` |
| RES-2 | PR body lines 19, 40, 49, 144, 156 | Still say the docs inventory cannot run or was not run, against the body's own round-3 note | Line 40: `` `scripts/docs_inventory.py --check` \| pass at beb38447 ``. Lines 19, 49, 144 and 156: drop the inventory exception. |
| RES-3 | PR body roles line | Omits the round-3 executor | Add `` `[A732c]` (round 3) `` to the Executor line |
| RES-4 | `docs/reference/STRICTER_READINGS.md:45` | "The builder gate" reads as the builder, which does not check this; gate 28b does, on tracked configs | `- Gate 28b refuses a zero octet in any tracked config.` |
| RES-5 | `docs/findings/397_SERVICE_BUDGET.md:290-291` | The colon sentence is split from its table by a parenthetical | Move line 291 below the table |

## Suggestions

- **S1:** `tb/tools/avdecc_ctl.py:312` and `tb/tools/crf_vs_phc.py:30` now default `--iface` to the placeholder, so an omitted flag fails at socket bind. `required=True` gives a clear error. No tracked caller relies on the default.
- **S2:** The firmware keeps register 4 bits 15, 13 and 12 and the other register 0 bits as read. The docs do not name these, and `clear-next-page`, `clear-remote-fault` and `reg0-from-constant` escape. Naming them, or grading them, would finish the contract.
- **S3:** No arm NAKs register 1 before the PHY init, so `init-on-failed-bmsr` escapes. The effect is small.
- **S4 (R775-1 S1, partly taken):** `tb/verilator/milan_dp/Makefile:565` still repeats the MAC literal beside `kStationMac`.
- **S5 (R775-1 S2, not taken):** `tb/verilator/nvm_capture_cpu/soc.py:187` still parses the MAC with `replace(':', '')`, so a dash-spelled config would crash the harness.

## Assigned focus

| Item | Result | Evidence |
|---|---|---|
| (1) F3 | Met, with two corrections to the brief below | `receipts/regrade_service.txt`, `receipts/live_1x1_vs_receipt.txt` |
| (2) F1 | Named mutants met; N1 and N2 open | `receipts/r775_1_mutants_at_head.txt`, `receipts/r776_1_mutants_at_head.txt` |
| (3) F2 | Met | `receipts/capture_compare.txt`, `receipts/capture_arms_vs_receipt.txt` |
| (4) Identity | Met | `receipts/identity_derivation.txt`, `receipts/oracle_vs_receipts.txt` |
| (5) Round 3 | Met | `receipts/merge_and_history.txt`, gate logs |

Two corrections to item (1) as briefed:

- **The fix is not a cheaper `phy_mdio_write()` loop.** That loop is unchanged. The whole firmware delta is `always_inline` on `phy_mdio_bit()` plus its comment. Frame bits are unchanged, and the bit period stays above the 400 ns MDC minimum at about 1.5 us.
- **The 248.69 ms figure is `dd764ed7`'s firmware.** At this head the worst publication bound is 246.80864 ms (8x8, `milan_nvm`, uart-paced). Both are under 250 ms.

### How F3 was proved

- **Image identity.** I built both shapes at this head. On both, `sim_rom.init` and all but seven of 163 build hashes equal the receipts. The seven are `sim.v`, `Vsim`, `bios.elf` and four generated headers. `git.h` and `csr.h` carry a generation timestamp, and the others are consistent with that. The firmware digest `09c5d481...` is equal, and all measurement input hashes equal the head.
- **Live reproduction.** I ran 1x1 `all --enforce-service` at this head. Its log is byte-identical to the published receipt (sha256 `afe78757...`, 0 differing lines), with no service findings.
- **Regrade.** The head's own `service_findings()` over the eight published JSON receipts gives no findings. Each receipt's log digest binds, and all eight table rows match the page exactly.
- **Arithmetic.** `C = P + 16*T`, the charge, reserve and trigger tables, and the `dd764ed7` figures all recompute.
- **Measurement-mode findings.** 8x8 `all` and `uart-paced` show `budget findings: 2` (`over-budget duty: milan_nvm`). These are the measurement-only duration comparison, not service findings, and service grading of those runs is empty.

### How round 3 was checked

I checked its receipts and reran what was cheap, rather than trusting its summary.

- The merge tree reproduces exactly (`9265b407`), with no conflicts and one merge base.
- `ci/image/command-table.json` and `docs/README.md` are the only both-sides files. Each differs from dev only by this lane's lines.
- `docs_inventory.py --check` and `--selftest` pass at this head, and `af9a8a33` touches only the audit page.
- `<host-iface>` is in no tracked file and in no initialised submodule. The `<host-iface>` strings in `scripts/act_ci.py` are synthetic self-test fixtures from dev.
- Round 3's receipts: 65 rc files all 0, and the builder's final line is as stated.
- The command-table checker fails the same way on dev and at this head, with an `ImportError` (`receipts/cmdtable_dev.log`, `cmdtable_head.log`). It stops before comparing anything, so I checked the table by diff: it differs from dev by the one `--mac` line, which matches `tb/verilator/milan_dp/Makefile:565`.

## Prior public findings

| Finding | Severity, lenses | Disposition at this head |
|---|---|---|
| R775-1 F3, R776-1 F3 | MAJOR; Tests, RTL, Docs | **Resolved.** See above. |
| R775-1 F1, R776-1 F1 | MINOR; Tests | **Resolved for all sixteen named mutants** and every listed clear. **Retained at its cause for the keeps, as N1.** |
| R775-1 F2, R776-1 F2 | MINOR; Docs | **Resolved.** Sections 18 and 20 item 6 equal `measurements.json`, including the 67-of-96 repeat breakdown, and tree `5d2dfb00` equals `4ab1bca0`'s. `remeasurement_assignment` now names the assignment. |
| R776-1 R1 | RESIDUE | **Resolved** in all three places. |
| R776-1 R2 | RESIDUE | **Resolved** at `STRICTER_READINGS.md:23-25`. |
| R776-1 S1 | SUGGESTION | **Taken:** gmstep now carries the image's identity. In `tb/verilator/milan_dp/Makefile`, gmstep and ax1x1gptp are the legs that build the shipping image, and both agree with it. |
| R776-1 S2 | SUGGESTION | Not taken, by the assignment. Once per boot is the documented design. |
| R775-1 S1, S2 | SUGGESTION | Partly taken, and not taken. Carried as S4 and S5. |
| R775-1 S3 | SUGGESTION | **Resolved**, as R776-1 R1. |

## Lens results

```text
[R775] PASS Conformance - configs/endstation_*.yaml, milan_baremetal.c PHY init, aem_desc.bin, oracle.json - five configs derive the decided MAC and EUI-64 with no zero octet; the built 8x8 AEM carries the new entity_id twice and the old one never; firmware unchanged from the reviewed advertisement but for the inline attribute
[R775] PASS RTL - git diff cc204c6f..beb38447 on hdl, syn and sw/litex is empty and all gitlinks equal dev's - no RTL in scope; F3's timing effect graded on the measured image, T 0.12457 ms, P 1.31864 ms, charge 3.31176 ms, reserve 3.19136 ms
[R775] PASS Robustness - receipts/phy_nak_probe.txt, phy_host.c arms, 397 enforced plans - unacknowledged reads of registers 4 and 0 write nothing and retry; no-ability PHYs stay unwritten; the 16-transaction worst poll matches my own count of the code path
[R775] PASS Docs - 397_SERVICE_BUDGET.md, BAREMETAL_FIRMWARE.md, SAVED_STATE_SNAPSHOT_OWNERSHIP.md, STRICTER_READINGS.md, DOCUMENTATION_AUDIT.md - figures recomputed from receipts; docs_check, doc style, em-dash, doc paths, TOC, anchors, inventory, hygiene, baremetal-only all rc 0; residue only
```

Tests is UNCLEAN under N1 and N2. What passes there: `test_phy_firmware.py` (26 PHY and 5 boot mutants), both reviewers' scripts (16 of 16), `run.py --self-test`, `check_nvm_capture.py`, behave (508 scenarios, 2330 steps), and `torture_campaign.py --self-test`.

The comment rule has no new instance: my scan of added non-Markdown source lines found no bench lane label, review round, reviewer ID or comment ID. Commits are one line with no trailers.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | five configs; `endstation_builder.py` derivation; `milan_baremetal.c` PHY init; built AEM and overlay; `oracle.json`; `STRICTER_READINGS.md` against #840 and the round-2 assignment | R775-2 | beb38447d07cceac5170ba0a35c7615f5714b7f7 |
| RTL | CLEAN | empty hdl, syn and sw/litex diff; gitlinks; PHY poll path; `sim_rom.init` identity; T, P and charge from receipts | R775-2 | beb38447d07cceac5170ba0a35c7615f5714b7f7 |
| Robustness | CLEAN | `phy_nak_probe`; `phy_host.c` failure arms; `phy_peer.h`; enforced plan receipts; worst-poll count | R775-2 | beb38447d07cceac5170ba0a35c7615f5714b7f7 |
| Tests | UNCLEAN (N1, N2) | `phy_host.c`, `phy_peer.h`, `test_phy_firmware.py`; own, R775-1 and R776-1 mutants; `run.py --self-test`; `check_nvm_capture.py`; behave; `phy_fix_probe` | R775-2 | beb38447d07cceac5170ba0a35c7615f5714b7f7 |
| Docs | CLEAN (RES-4, RES-5 carried) | 397, firmware guide, SAVED_STATE sections 18 and 20, stricter readings, audit page; the docs gates listed above | R775-2 | beb38447d07cceac5170ba0a35c7615f5714b7f7 |

## Real limits

- **Live runs.** Only 1x1 `all` was run to completion. I stopped the 8x8 `all` run after about 14 minutes, because the published run took over two hours. Its rc 1 and "native simulation failed" in `receipts/svc-run-8x8-all.log` come from my signal, not a simulation fault, and no conclusion rests on it. The 8x8 result rests on the published receipts, the identical ROM and the 1x1 run's determinism.
- **Queued-short and queued-builtins.** Their JSON receipts and full logs are published by digest only. For these four of twelve table rows I saw only the `budget findings: 0` tails, so I could not recompute their figures. The 1x1 reserve depends on one of them (207.70251 ms), and it recomputes from that row. None of the four is near the bound.
- **Simulator.** My service builds used the product environment's Verilator 5.052, the same version the capture receipt names. The scoped 5.050 was not used.
- **Evidence integrity.** The packet is hash-manifested, and 524 of 524 author round-2 and round-3 files match. Its commits carry no signature (`%G?` is `N`), so I cannot call it signed.
- **Sweep.** No full sweep ran at this head, and I did not run one. The last is at `cadb63b4`, and I read its shard result files only in outline. The head differs from it by the dev merge, the inventory and six strings.
- **Not rerun by me:** the full builder bank (so gate 28b was not rerun directly), `.github/workflows/docs.yml` as a whole, and the capture arms.
- **Clause text.** I did not reopen the standards this round. Clause numbers were read against my knowledge of them and round 1's check, not re-verified against the documents.
- **Hardware.** Physical calibration NOT RUN. No real PHY was used, so MASTER-SLAVE and no-link behaviour are shown at the pin-level peer only. Field skips are not hardware proof.
- **Hosted.** At 12:19 local on 2026-11-06: 54 contexts, 23 passed, 30 pending, 1 skipped (`Physical gPTP`), 0 failed. The long gates had not finished, so this is not hosted acceptance.

## Pending manager duties

- Merge-candidate builder and native banks, and hosted and act acceptance.
- Carry RES-1 to RES-5 to the residue checklist.
- Maintainer acknowledgements the author still requests: the 1000BASE-T ability gate assumption, and the STOP clause naming `gen_ucode.py:177`.
- The issue title and body still state the first identity. The round-2 assignment changed it publicly; a cold reader would benefit from a note there.
- The PR carries no closing keyword, so #840 needs closing by hand after the merge.

## Clone state

Restored and verified (`receipts/restore_check.txt`): 1473 index entries equal the tree, 1467 blobs hash equal, 0 mode mismatches, and an empty status including ignored files. All five initialised gitlinks match. `external` is uninitialised, as it was at the start. I removed four ignored build outputs my runs had created.

R775-2 FINISHED
