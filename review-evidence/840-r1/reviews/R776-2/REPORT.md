[R776] NEGATIVE - exact head beb38447d07cceac5170ba0a35c7615f5714b7f7

# R776-2: external independent review of PR #842 (issue #840)

- Head `beb38447d07cceac5170ba0a35c7615f5714b7f7`, tree `ba0183c2c52237818d6a08120b620d53e2e490c4`.
- Delta reviewed: `dd764ed7..beb38447`, rounds 2 and 3 together, plus the diff against dev `cc204c6fd2349b543d73f15c97162a2c4434c86e`.
- Live dev equals the source base, `cc204c6f`, and it is the one merge base.
- Context was rebuilt from public state only: AGENTS.md, CONTRIBUTING.md, docs/README.md, the #840 body and thread, the PR body, the diff, and the `840-review-evidence` tree at `f9114411`.
- I wrote my own verdict and ledger before opening any prior review text (`receipts/own-pass-verdict.md`).

## Verdict

NEGATIVE. Two MINOR findings are open, both under Tests. There is no BLOCKER or MAJOR.

The lane's real work holds up. F3, F1 and F2 are resolved at their causes, the identity is right everywhere it is generated, and the merge and inventory are sound. Conformance, RTL, Robustness and Docs are covered clean.

Two things keep it from POSITIVE:

- **F4.** This PR adds three stale script digests to the image command table. The assignment's exception for #838 applies only if the PR adds no mismatch, and it adds three.
- **F5.** The firmware guide says an unacknowledged read of registers 15, 4, 9 or 0 writes nothing. The peer exercises 15 and 9 only, so mutants that remove the guard for 4 or 0 pass. This is F1's cause again, on a claim F1 did not list. The firmware itself is correct.

Both fixes are small. F5 needs about sixteen lines in `phy_host.c`, and a working version is in this packet.

## Results on the assigned focus

| Item | Result | Evidence |
|---|---|---|
| (1) F3: enforced plans report no over-budget stretch | Holds. Eight receipts regraded and one plan re-executed at this head, byte-identical to its published log. See the F3 row of the prior-findings table and Real limits | `receipts/regrade_receipts.log`, `receipts/oracle_bind.log`, `receipts/svc-1x1-qs-result.txt` |
| (1) `phy_mdio_write()` is identical on the wire | Holds. 34,740 pin writes hash identically at head, `dd764ed7` and `c06150b4`, with equal `delay_cycles` 737280 | `receipts/phy_r776_2_mutants.log`, WIRE lines |
| (1) 397 states `P + 16*T` and the figures | Holds at `docs/findings/397_SERVICE_BUDGET.md:264`. I recomputed every charge, margin and reserve | below |
| (1) Worst bound under 250 ms | Holds, with a correction: 248.69 ms is the `dd764ed7` firmware's figure (248.68507). At this head the worst is 246.80864 ms, 8x8 `milan_nvm`, uart-paced. The tree states this correctly | `receipts/regrade_receipts.log`; `before-dd764ed7/run-8x8-queued-input.log:371` |
| (2) F1: peer start values and both mutant sets | Holds. R775-1 8 of 8 and R776-1 8 of 8 fail on a named assertion, rerun by me. See F5 for a neighbouring gap | `receipts/prior-R775-1-mutants.log`, `receipts/prior-R776-1-mutants.log` |
| (3) F2: design documents state the current receipt | Holds. Commit, tree, firmware digest, pins, six arm ranges, ratios, margins and the 67-of-96 repeat count all equal `measurements.json` | `receipts/capture_doc_check.log` |
| (4) Identity | Holds in all five configs, the head build and the gPTP ROM, with no zero EUI-64 octet | `receipts/generated_identity.log`, `receipts/gate28b.log` |
| (5) Merge keeps both sides | Holds. A fresh reconstruction gives tree `9265b407`, the merge's own tree | `receipts/merge-reconstruct.txt` |
| (5) Inventory through its generator | Holds. `--check` rc 0, `--selftest` 50 controls, and `af9a8a33` touches only `docs/DOCUMENTATION_AUDIT.md` | `receipts/inventory_and_interface.log` |
| (5) The local interface name gone | Holds. Zero hits in 1,473 tracked files, binary included. See S3 for the two new defaults | `receipts/inventory_and_interface.log` |

Round 3's receipts agree with its summary. All eleven `.rc` files are 0. The documentation table counts 65 rc 0 and 31 NOT RUN. Each NOT RUN row I read gave a reason, and those were hosted-only recording or installs already satisfied. The manifest's 524 `author-r2` and `author-r3` digests all match the published bytes.

The arithmetic I recomputed for 397:

| Figure | Check | Result |
|---|---|---|
| 8x8 charge | 1.31864 + 16 x 0.12457 | 3.31176 ms |
| 1x1 charge | 1.31480 + 16 x 0.12451 | 3.30696 ms |
| 8x8 worst duty + UART | 246.34096 - 125 - 2.84408 | 118.49688 ms |
| 8x8 reserve | 250 - 118.49688 - 3.31176 - 125 | 3.19136 ms |
| 1x1 reserve | 250 - 79.87187 - 3.30696 - 125 | 41.82117 ms |
| `dd764ed7` charge | 2.47411 + 16 x 0.16963 | 5.18819 ms |

The sixteen-transaction count also matches `phy_link_tick()`: ID, BMSR, four init reads, three writes, the BMSR re-read, and six resolution reads.

## Findings

### F4 - MINOR - Tests - `ci/image/command-table.json:14076`, `:14171`, `:14176` - this PR adds three stale script digests

- **Authority/evidence.**
  - `docs/testing/CI_IMAGE.md:44`: "Changed declared scripts refuse generation until reviewed again."
  - `scripts/ci_command_table.py:219-220` raises `changed declared script` on a digest mismatch.
  - The review assignment: the checker's failure "is not a finding unless this PR adds a mismatch".
  - I compared every digest the table records with the file at each revision (`cmdtable_digests.py`, `receipts/cmdtable_digests.log`). Dev has 33 mismatches and the head has 36. None is removed, and exactly three are added:

  | Script | Pinned digest, equal to dev's bytes | Head bytes |
  |---|---|---|
  | `tb/verilator/fw_service_budget/run.py` | `5c2a6477...` | `d9914cd7...` |
  | `tb/verilator/nvm_capture_cpu/run.py` | `c230cb3e...` | `4b8d85bd...` |
  | `tb/verilator/nvm_capture_cpu/soc.py` | `e782993b...` | `f1fe0da5...` |

  - Running the checker cannot show this. It stops at its first refusal, which #838 records as `endstation_builder.py`, so it reads the same at dev and head. Here it stops earlier still, because the pinned parser is absent (`receipts/cmdtable-head.log`, `receipts/cmdtable-dev.log`).
- **Impact.** The repair #838 tracks grows by three rows, and the three changed scripts have not had the re-review the table requires. My reading of the three diffs is that no new command appears: a constant from 9 to 16, one spec key and one dictionary entry. That reading is not the recorded review. No hosted gate fails today, because no workflow runs this checker, which is why the mismatch stayed invisible.
- **Required outcome.** The three rows equal their bytes at the merge candidate, re-pinned by the route #838's acceptance allows. Moving them to #838 without re-pinning does not clear this finding.
- **Verification.** `python3 -I cmdtable_digests.py <repo> <head> <dev>` prints `added by <head> []`.

### F5 - MINOR - Tests - `sw/firmware/nvm_hosttest/phy_host.c:139-154` - the unacknowledged-read claim for registers 4 and 0 cannot fail the peer

- **Authority/evidence.**
  - AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect", and negative behaviour is covered.
  - `docs/integration/BAREMETAL_FIRMWARE.md:2183`: "An unacknowledged read of registers 15, 4, 9 or 0 writes nothing; the next poll retries."
  - `sw/firmware/milan_baremetal/milan_baremetal.c:1043` and `:1061` state and implement it.
  - The peer refuses only registers 15 and 9 during the init (`phy_host.c:139`, `:146`). Register 5 at `:225` is a resolution arm, after the init is done.
  - Two of my mutants survive with rc 0 (`phy_r776_2_mutants.py`, `receipts/phy_r776_2_mutants.log`): `nak-reg4-unguarded` and `nak-reg0-unguarded`. The matching `nak-reg9-unguarded` is caught by `no_write_before_its_read`.
  - The existing `write-unread` mutant removes the whole guard, so it does not show each term is needed.
- **Impact.** A regression dropping either term ships green. With the register 4 term gone, a refused read writes `0xbc1f` to register 4, setting next page, remote fault and every selector bit. There is no live defect: the head passes a peer that also refuses registers 4 and 0 (`receipts/phy_nak_probe.log`, `NAKPROBE head: rc=0 PHY_OK`).
- **Required outcome.** The peer refuses registers 4 and 0 during the init, each graded by a named assertion that no write happened, and each mutant joins the table. Or the guide and comment claim only what is graded.
- **Verification.** With `phy_host_nak.c` in this packet, both mutants fail by name: `no_write_before_its_register_4_read` and `no_write_before_its_register_0_read`. A register 4 refusal still publishes 13, because the gigabit resolution does not read register 4, so an arm must not expect status 0 there. My first probe made that mistake.

## Residue

### R3 - RESIDUE - Docs - PR title - names the round-1 address

Exact fix: `Prototype identity 02:4B:4C:4B:4C:01, 1000BASE-T-only advertisement on 1G PHYs, and the stricter-reading page (#840)`.

### R4 - RESIDUE - Docs - PR body - the round-2 inventory text survives below the round-3 note

The opening note says the limitation is resolved, but these lines still state it as open. Exact fixes:

- **Status:** replace `GREEN, except the docs inventory, which cannot run on this base.` with `GREEN.`.
- **Gate table, `scripts/docs_inventory.py --check` row:** replace `not run: absent at the base and the head` with `pass at beb38447`.
- **Linked Issue section:** delete the sentences from `One acceptance point stays open` to `the next round's dev merge.`.
- **Known limitations:** delete the `Docs inventory (acceptance item 4, open)` bullet.
- **Definition of Done:** delete `(all but the docs inventory, which cannot run on this base)`.
- **Same state and validate sections:** replace `cadb63b4985c0ad4fb7dc036a23bf9fe93eb6276` with the head, and `604899c08ff1cd1830e1dd08b733109ef852400c` with `cc204c6fd2349b543d73f15c97162a2c4434c86e`.

## Suggestions

- **S3 - Robustness - `tb/tools/avdecc_ctl.py:312`, `tb/tools/crf_vs_phc.py:30`.** The default `<host-iface>` satisfies the CONTRIBUTING placeholder rule, but it is passed straight to `bind()`. Omitting `--iface` now ends in `OSError: [Errno 19] No such device` rather than a usage error (`receipts/iface_default_probe.log`). `required=True` would say what is missing. No tracked caller relies on the default.
- **S4 - Tests - `milan_baremetal.c:1144`, `phy_mdio_write()`.** Two more mutants survive, neither against a documented claim: `bmsr-unacked-still-inits` drops `bmsr >= 0`, and `write-frame-no-release` drops the final pin release. A refused register 1 arm would catch the first alongside F5.
- **S5 - Docs - `sw/builder/README-parameters.md:173`.** The spelling example still uses the retired `02:00:00:00:00:02`. It is valid as a parser example, so this is optional.
- **Retained, not taken:** R775-1 S2 (`nvm_capture_cpu/soc.py:187` parses only colon spellings) and R776-1 S2 (once per boot, the documented design). I have no new evidence on either.

The mutant `init-before-found` in my script also survives, but it is not evidence. It behaves like the head at the peer's odd address 7, so I do not count it.

Comment rule: 660 added source lines scanned, zero new lane labels, review rounds, reviewer IDs or comment IDs (`receipts/comment_scan.log`).

## Prior public findings

| Prior finding | Severity, lenses | Disposition at this head | Evidence |
|---|---|---|---|
| F3, both reviews | MAJOR, Tests/RTL/Docs | RESOLVED at cause. The doubled transaction came from `phy_mdio_bit()` losing its inlining, and that is reversed: T 9534 and P 131864 against 16963 and 247411. The oracle equals the published receipts, all 141 source inputs equal the head, and the head's grader finds nothing in the eight full receipts. I also ran the 1x1 `queued-short` plan with `--enforce-service` at this head: rc 0, no finding, and its output is byte-identical to the published log (266,679 bytes, SHA-256 `0843ea3d...`) | `receipts/oracle_bind.log`, `receipts/regrade_receipts.log`, `receipts/svc-1x1-qs-result.txt` |
| F1, both reviews | MINOR, Tests | RESOLVED as filed: every listed keep and clear now fails by name. F5 is a new instance of the same cause on a claim F1 did not list | `receipts/prior-R775-1-mutants.log`, `receipts/prior-R776-1-mutants.log` |
| F2, both reviews | MINOR, Docs | RESOLVED, including line 1687's "PHY poll only" and the `remeasurement_assignment` point | `receipts/capture_doc_check.log` |
| R775-1 S1 | SUGGESTION | MET: `sim_ax1x1gptp.cpp` derives the MAC words from `kStationMac` | source |
| R775-1 S2 | SUGGESTION | NOT TAKEN, retained as optional | `soc.py:187` |
| R775-1 S3, R776-1 R1 | SUGGESTION, RESIDUE | RESOLVED: all three usage texts carry the new identity | `tb/tools/hive_compliance.py:6-7`, `hive_compliance_clusters.py:7`, `check_tu_on_wire.sh:55` |
| R776-1 R2 | RESIDUE | RESOLVED | `STRICTER_READINGS.md:19-25` |
| R776-1 S1 | SUGGESTION | MET: gmstep derives MAC, ADP and AECP identity from `kStationMac` and `kEntityId` | `sim_gmstep.cpp:121-122` |
| R776-1 S2 | SUGGESTION | NOT TAKEN by assignment, retained as optional | #840 round-2 assignment |

The over-budget `milan_nvm` findings in 8x8 `all` and `uart-paced` (`regrade-at-cadb63b4.txt`) are not new. They are the same two findings the dev oracle records, and that grade is not the enforced PHY rule.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Five `configs/endstation_*.yaml` through `derive_entity_id()` and `identity_warnings()`; head build `aem_overlay.json` and `gptp_ucode.hex` (`04b59447...`, equal to `measurements.json`); gate 28b; `milan_baremetal.c:1044-1072`; #840 body and round-2 assignment; gitlinks `a9e84b66`, `135afd04` unchanged | R776-2 | beb38447d07cceac5170ba0a35c7615f5714b7f7 |
| RTL | CLEAN | No file under `hdl`, `syn`, `constraints` or the submodules in the diff; the MDIO pin stream, identical across three firmware revisions; poll timing in `run.py:405-426` and eight full receipts | R776-2 | beb38447d07cceac5170ba0a35c7615f5714b7f7 |
| Robustness | CLEAN (S3, S4 optional) | `phy_advertise_gigabit_only()` under refused registers 15, 9, 4 and 0, including a patched peer; ten caught mutants of my own covering write framing, ordering, masks and retry; the once-only arms | R776-2 | beb38447d07cceac5170ba0a35c7615f5714b7f7 |
| Tests | UNCLEAN (F4, F5) | `test_phy_firmware.py` (26 + 5 mutants, rc 0); both prior mutant sets; 15 mutants of mine; gate 28b; `run.py --self-test`; `check_nvm_capture.py`; `torture_campaign.py --self-test`; the command-table digests | R776-2 | beb38447d07cceac5170ba0a35c7615f5714b7f7 |
| Docs | CLEAN (R3, R4 residue; S5 optional) | `397_SERVICE_BUDGET.md:264-306`; `BAREMETAL_FIRMWARE.md:2174-2212`; `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1633-1705, 1871-1880`; `STRICTER_READINGS.md`; `check_doc_style.py`, `docs_check.py`, `docs_inventory.py --check` and `--selftest`, all rc 0; `git diff --check` rc 0 (`receipts/docs_gates.log`, `receipts/inventory_and_interface.log`) | R776-2 | beb38447d07cceac5170ba0a35c7615f5714b7f7 |

## Real limits

- Of the twelve service runs, I regraded eight from full published receipts and re-executed one. The other three (1x1 `queued-builtins`, 8x8 `queued-short`, 8x8 `queued-builtins`) are published as a digest and a tail only, so for them I rely on those tails, the author's table, and the exact reproduction of their sibling.
- The evidence commits are not signed (`verified=false`), so I checked integrity through the manifest digests. Ten published logs are path-redacted by design, so I checked their published bytes only.
- I could not run the command-table checker end to end: its pinned parser is absent here and downloads are not allowed. F4 rests on the direct digest comparison.
- No full sweep ran at this head. The last is at `cadb63b4`, four shards exit 0. Since then only docs, `tb/tools`, the docs workflow, `scripts/ci_events.py`, the inventory scripts and the command table changed.
- `check_em_dash.py` could not judge here: its pinned Markdown renderer is not installed (rc 2 in `receipts/inventory_and_interface.log`; the rc 2 in `receipts/docs_gates.log` is my omitted `--base`). That gate rests on round 3's published documentation table.
- I did not open IEEE 802.3. The delta's new citations (22.2.4.1.4, Figure 28-18) rest on my reading, not the text.
- The capture receipt records simulator 5.052, as its predecessor did. My service run used the pinned 5.050, and its output still matched the published log byte for byte.
- `tsn_fuzz/wire.py` and `avtp_wire_truth_frames.py` keep old-looking identities. I read both as harness-chosen, as round 1 did, and neither reads a config.
- No hardware was used. Physical calibration is NOT RUN, and field skips are not hardware proof.
- Hosted snapshot at review time: 16 success, 1 skipped, 35 in progress or queued (`receipts/hosted_snapshot.txt`). That is not a result.

## Pending manager duties

- Merge-candidate validation, builder and native banks, and hosted or act acceptance.
- The maintainer's answers on the two open public points: the certification_version STOP clause (`protocol-processor/hdl/aecp/ucode/gen_ucode.py:177`) and the 1000BASE-T ability gate, a material assumption beyond the issue's wording.
- The #840 title and body still state the round-1 identity. The round-2 assignment supersedes them, so a cold reader needs that pointer.
- R3 and R4 on the residue checklist.

R776-2 FINISHED
