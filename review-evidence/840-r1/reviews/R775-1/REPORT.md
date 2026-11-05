[R775] NEGATIVE - exact head dd764ed7c09e4764f4d7368f447e94af151a24de

# R775-1: internal cleared-context review of PR #842 (issue #840)

- Head: `dd764ed7c09e4764f4d7368f447e94af151a24de`, tree `7e0fae18322bfb45ada20f49493a9082c77702d9`.
- Source base and live dev: `604899c08ff1cd1830e1dd08b733109ef852400c`. Eleven commits, 31 files.
- Scope source: the #840 body (maintainer decisions 2026-11-05), the TAKEN and REVIEW READY comments, the PR body, and FPGA-gPTP #100.
- Reviewed in a separate clone. No source edits, commits, pushes or GitHub writes were made.
- After the probes, the clone was restored to the exact head. See `receipts/restore_check.txt`.

## Verdict

NEGATIVE. There is one MAJOR, two MINOR and no BLOCKER.

Most of the lane is right:
- The identity is correct. All five configs carry the decided address, the regenerated artifacts carry the new identity, and the builder warns without refusing.
- The firmware advertisement matches the decision.
- certification_version is untouched in its submodule.
- The stricter-readings page passes every docs gate.

Three problems keep it from merging:
- F3: raising the PHY poll charge from 9 to 16 transactions, with write transactions that measure about 1.9x a read, was never graded against the 250 ms publication bound on target data. The published 8x8 reserve was 4.46 ms. On the page's own arithmetic it now falls to between about +1.2 ms and -0.6 ms.
- F1: five firmware properties have no test that can fail. These are the keep and clear behaviours that the code comments and the firmware guide claim.
- F2: the capture design document still states the old receipt's figures.

## Prior public findings

None. At the time of this report, PR #842 had no reviews and no review comments. Its two issue comments are review-start notices. See `receipts/pr_prior_review_state.txt`.

## Findings

### F3 - MAJOR - Tests, RTL, Docs - the raised PHY poll charge was not graded on target data

- **Where:**
  - `tb/verilator/fw_service_budget/run.py:412`
  - `docs/findings/397_SERVICE_BUDGET.md:262-276`
  - `docs/integration/BAREMETAL_FIRMWARE.md:2201`

- **Evidence: the claim.**
  - The bound is "125 ms + no-tick stretch + TX allowance + scheduling charge <= 250 ms" (397, lines 250-251).
  - The firmware guide says "The service harness grades this derived publication bound against 250 ms".
  - `service_findings()` grades it only in `--enforce-service` runs: the queued-input, queued-short, queued-builtins and device-wait plans.
  - The suite (`run.py --self-test`) checks the formula only on planted numbers (`service_controls()`).

- **Evidence: what changed.** The head raises the charge to `P + 16*T`. The oracle the head commits shows both terms grew (`receipts/phy_charge_estimate.txt`):

  | Term | Base, cycles | Head, cycles | Ratio |
  |---|---|---|---|
  | T, 8x8 `all` (largest transaction) | 8793 | 16963 | 1.93x |
  | P, 8x8 `all` (largest complete poll) | 65294 | 247411 | 3.79x |

  The writes appear to be the slow transactions. A read and a write each clock 64 MDIO bits.

- **Evidence: what was run.** The author's service receipts at `d62417f1` (`service-budget-d62417f1/fw-*-service-*.json`) are `all` and `uart-paced` runs only. None carries `service_findings` or `phy` (`receipts/author_service_receipts_scope.txt`).

- **Estimate, not a measurement.** It uses 397's 8x8 row (worst duty plus UART of 118.58473 ms and a 125 ms trigger), so the charge must stay at or below 6.41527 ms.

  | Charge taken from | Head charge | Reserve |
  |---|---|---|
  | the head's `all`-plan P and T | 5.18819 ms | +1.22708 ms |
  | those P and T scaled as the page's plans exceeded the base `all` plan | 7.00426 ms | -0.58899 ms |

  The published reserve was 4.46039 ms.

- **Evidence: the page.** 397 still states `C = P + 9*T` and "Nine reads", and its charge and reserve tables are the base figures.

- **Impact.** The 250 ms PHY publication bound for the measured duties is unverified at the head. It may now be exceeded on 8x8, which is the failure that `service_findings()` exists to catch ("over-budget PHY service stretch"). The authoritative findings page states a formula the code no longer uses.

- **Required outcome:**
  - Run the `--enforce-service` plans on both shapes at a head carrying this firmware, with no PHY service finding.
  - If any plan fails, change the firmware or the trigger and re-measure. One option is a cheaper write loop: `phy_mdio_write()` takes a variable `frame >> (31u - i)` on every bit.
  - Refresh 397's formula, transaction and poll figures, charge, and reserve tables from those receipts.

- **Verification:**
  - `run.py --shape <s> --plan <p> --enforce-service` for each plan reports no `over-budget PHY service stretch`.
  - 397 states `16*T` and the measured figures.

### F1 - MINOR - Tests - five claimed PHY init properties cannot fail the pin-level peer

- **Where:**
  - The claim: `sw/firmware/nvm_hosttest/phy_host.c:83`, "so each bit the PHY init must clear or keep is graded".
  - The assertions: `phy_host.c:50-61`.
  - The properties: `sw/firmware/milan_baremetal/milan_baremetal.c:956`, `:960` and `:1065`.
  - The docs that state them: `docs/integration/BAREMETAL_FIRMWARE.md:2177-2178` and `docs/reference/STRICTER_READINGS.md:57`.

- **Evidence.** Eight disposable mutants were planted into a temporary copy of the firmware, through the test's own bench (`scripts/phy_extra_mutants.py`, `receipts/phy_extra_mutants.log`). Five escape with `phy_host` passing:

  | Mutant | Property it breaks |
  |---|---|
  | `drop-pause` | register 4 pause bits 10 and 11 cleared, though the guide says they are kept |
  | `keep-reserved-4.14` | bit 4.14 no longer forced to zero |
  | `drop-master-slave` | register 9 bits 12 to 10 dropped, though the guide and the page say they are kept |
  | `keep-test-mode` | register 9 test-mode bits 15 to 13 kept |
  | `restart-keeps-isolate` | ISOLATE not cleared on the restart |

  The fixture starts register 4 at `0x0fe1`, register 9 at `0x0300` and register 0 at `0x1000`. Each of these bits therefore already holds its post-init value. No assertion checks pause bits 10 and 11.

  The other three mutants are caught: `restart-sets-reset`, `gate-on-half-duplex` and `no-register-4-write`.

- **Impact.** The changed behaviour's keep and clear contract, which the comments and two docs state, has no test that can fail. A regression that drops pause or MASTER-SLAVE configuration, or leaves a strap-isolated PHY isolated, would ship green.

- **Required outcome.** The peer starts with these bits in the opposite state. That means bit 4.14 set, a nonzero MASTER-SLAVE field, test-mode bits set and ISOLATE set. Named assertions then grade each kept and cleared bit. The ones that matter are added to the mutant table, or the comment and docs claim only what is graded.

- **Verification.** Each of the five mutants above fails `test_phy_firmware.py` by its own assertion name.

### F2 - MINOR - Docs - the capture design document states the superseded receipt

- **Where:**
  - `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1633-1702`, section 18.
  - `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1859-1867`, section 20 item 6.

- **Evidence.** Commit `67e61edb` re-measured `tb/verilator/nvm_capture_cpu/measurements.json`. The document still describes the previous receipt:

  | Field | The document says | The committed receipt says |
  |---|---|---|
  | Measured | "MEASURED on 2026-10-30", commit `c71364bd` | re-measured at `d62417f1` |
  | Firmware SHA-256 | `60799c75...` | `1071b45e...` |
  | 8x8 contract maximum | 13.86052 ms, 3.5352x | 13.85922 ms |
  | 1x1 maximum | 3.96490 ms | 3.96810 ms |

  The receipt's firmware digest equals the head's `milan_baremetal.c` (`receipts/capture_input_hashes.txt`). The per-arm table is the old receipt's.

  Line 1687 says the firmware changed in "its PHY poll only", but it now also writes the PHY.

  Each earlier re-measurement refreshed this section in the same lane, for example `b6a1c189` after `14e956f0`.

- **Impact.** The authoritative design record of the 24.5 ms acceptance limit cites a receipt that is no longer the committed one. A cold reader cannot tie the figures to the tree. This is a figure and measurement claim, so it is not RESIDUE.

- **Required outcome.** Sections 18 and 20 item 6 state the committed receipt: commit, firmware digest, maxima, ratios, margins and the per-arm table. The superseded receipt is kept as history, as the section already does for earlier ones.

- **Verification.** Every figure in those sections equals `measurements.json` at the merge candidate.

## Suggestions (non-blocking)

- **S1:** `tb/verilator/milan_dp/sim_ax1x1gptp.cpp:881` hard-codes `MAC_ADDR_LO = 0x004C4B02` beside `kStationMac`. The Makefile `--mac 0x024b4c000001` (line 565) repeats the config. Deriving both from one source avoids drift.
- **S2:** `tb/verilator/nvm_capture_cpu/soc.py` parses the MAC with `replace(':', '')`. A dash-spelled config, which the builder accepts, would crash the harness. The builder's parser would accept every spelling.
- **S3:** `tb/tools/hive_compliance.py:6-7`, `hive_compliance_clusters.py:7` and `check_tu_on_wire.sh:55` still show `02:00:00:00:00:01` / `020000FFFE000001` as usage examples. The lane updated the matching tool defaults.

No RESIDUE found. The added source comments carry no lane labels, review rounds, reviewer IDs or comment IDs (scan of every added non-Markdown line).

## Lens results

### Conformance - CLEAN

| Item | What was checked | Evidence |
|---|---|---|
| (1) Identity | All five configs build, and each warns once on stderr. `aem_overlay.json` carries `mac_address` and `entity_id` `0x024B4CFFFE000001` (AX7101) or `...0002` (Arty). `gptp_ucode.hex` carries `024b4c`. | `receipts/build_*.{out,err,rc}` |
| (1) Builder gate | Gate 28b passes. | `receipts/builder_gate28b.log` |
| (1) Company-ID octets | `02`, `4B` and `4C` are all nonzero. | the decided value |
| (1) Regenerated artifacts | The oracle has the exact `gen_oracle.py` shape, key order and digests, and its raw logs carry `024b4cfffe000001`. The capture receipt's config, firmware and harness hashes equal the head files. | `receipts/oracle_provenance.log`, `receipts/capture_input_hashes.txt` |
| (1) Fixture is load-bearing | The gPTP leg passes 210 of 210 checks. Its old-target revert mutant fails `GET_AVB_INFO`. | `receipts/milan_dp_exec_gptp.log`, `receipts/milan_dp_gptp_oldtarget_mutant.log` |
| (1) Harness-chosen identities | Fixtures with their own identities, such as gmstep and test_aecp, program their own CSRs and assert no config identity. | `sim_gmstep.cpp:874-875` |
| (2) Advertisement | `milan_baremetal.c:1012-1067` checked against IEEE 802.3-2022 22.2.4.5 (write frame), Table 28-2 and 28B-1 (register 4), Table 40-3 (register 9), 22.2.4.1.7 (restart) and 22.2.4.2.16 / 22.2.4.4.3 (the ability gate). The 10/100 PHY keeps its link. | `receipts/test_phy_firmware.log`: 16 PHY and 5 boot mutants caught, `PHY_BOOT_OK` |
| (3) certification_version | `protocol-processor/hdl/aecp/ucode/gen_ucode.py:177` reads `MILAN_CERT_VERSION = 0x00000000`. The gitlink `a9e84b66` is unchanged. pp_top M2 asserts 0. The behave scenario passes. | `receipts/behave_get_milan_info.log` |
| (4) Stricter-readings page | Items 1 to 3 are listed, plus FPGA-gPTP #100 items 3 to 5, each with its clause, allowance, behaviour and reason. The prototype MAC limitation is stated. | `docs/reference/STRICTER_READINGS.md` |

### RTL - UNCLEAN (F3)

- No HDL changed in the delta.
- The firmware and harness architecture was applied: the poll ordering, the latched-loss handling and the CDC publication order (`milan_baremetal.c:1118-1154`), and the scripted PHY's write path (`fw_service_budget/phy.hpp:12-31`).
- F3 is the timing effect of the change that was not measured.

### Robustness - CLEAN

| Path | Result |
|---|---|
| A NAK on register 15, then on register 9 | Writes nothing, and the next poll retries (`phy_host.c:94-112`). |
| A PHY without extended status, or without bit 15.13 | Never written, and links at 100FD (`phy_host.c:213-256`). |
| A 10/100-only partner | No link published, with and without extended status. |
| A repeated init | Caught (`advertise-every-poll`). |
| The ability gate taken from half duplex | Caught (`receipts/phy_extra_mutants.log`). |
| An identity-mismatch boot | Touches no MDIO pin (boot mutant `phy_unguarded`). |
| A PHY reset | Only on the AECP reboot path, which reconfigures the FPGA and reruns the init (`sw/litex/milan_soc.py:2132-2149`). |

### Tests - UNCLEAN (F1, F3)

- These pass:
  - `test_phy_firmware.py` (rc 0)
  - `fw_service_budget run.py --self-test` (rc 0, 55 checks)
  - `check_nvm_capture.py` (rc 0, controls detected)
  - builder gate 28b (rc 0)
  - `ci_differential.py --check` (rc 0, 224 fixtures)
  - the gPTP leg and its revert mutant
- The 12 named advertisement mutants are each caught.
- F1 and F3 are open.

### Docs - UNCLEAN (F2, F3)

- These pass at the head:
  - `check_doc_style.py` and `--selftest`
  - `check_em_dash.py --base 604899c0`
  - `docs_check.py`
  - `check_doc_paths.py`
  - `gen_toc.py --check` and `--verify-anchors`
  - `check_gptp_docs.py`
  - `check_feature_status.py`
  - `check_hygiene.py --check`
  - `check_todo_ownership.py`
  - `check_py_idiom.py`
  - `check_cpp_idiom.py`
  - `check_baremetal_only.py --check` and `--selftest`

  Run log: `receipts/docs_gates_summary.txt`. The first `check_baremetal_only` run lacked pyyaml in the scratch environment. Its rerun on the system interpreter is rc 0.
- The stricter-readings page is registered with the style gate, linked from `docs/README.md`, and its contents block verifies.
- The docs inventory (`scripts/docs_inventory.py`) is absent at dev and lands with PR #815. As instructed, it is a known open point for a later dev-merge round, not a finding.
- F2 and F3 are open.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | configs/*.yaml; five builder outputs; `endstation_builder.py:5135-5157`, `:6106`, `:6156`; `milan_baremetal.c:946-1153`; gen_ucode.py:177 and gitlink; behave GET_MILAN_INFO; STRICTER_READINGS.md against #840 and FPGA-gPTP #100 | R775-1 | dd764ed7c09e4764f4d7368f447e94af151a24de |
| RTL | UNCLEAN (F3) | `milan_baremetal.c` PHY poll and init; `fw_service_budget/phy.hpp`, `run.py:400-436`; oracle PHY_TIMING base against head | R775-1 | dd764ed7c09e4764f4d7368f447e94af151a24de |
| Robustness | CLEAN | `phy_host.c` NAK, no-ability and no-partner arms; `phy_peer.h` write path; boot-path arms; mutant probes | R775-1 | dd764ed7c09e4764f4d7368f447e94af151a24de |
| Tests | UNCLEAN (F1, F3) | `test_phy_firmware.py`, `phy_host.c`, gate 28b, the fw_service_budget self-test, check_nvm_capture, the milan_dp gptp leg and its revert mutant, ci_differential | R775-1 | dd764ed7c09e4764f4d7368f447e94af151a24de |
| Docs | UNCLEAN (F2, F3) | STRICTER_READINGS.md, BAREMETAL_FIRMWARE.md:2171-2203, README-parameters.md, ENDSTATION_BUILDER.md row 6a, fw_service_budget/README.md, 397_SERVICE_BUDGET.md, SAVED_STATE_SNAPSHOT_OWNERSHIP.md sections 18 and 20; the docs gates | R775-1 | dd764ed7c09e4764f4d7368f447e94af151a24de |

## Real limits

- Not run at this head:
  - the full sweep
  - the firmware self-test `test_nvm_firmware.py --self-test`
  - `fw_coverage.py`
  - the full builder bank
  - full behave
  - the physical gPTP suite
  - any `--enforce-service` plan
- Those gates' results are the author's receipts, which were spot-checked rather than re-run. The four sweep shards record this head and exit 0.
- F3's reserve figures are estimates from committed oracle timings and the findings page's own arithmetic, not measurements.
- No hardware was used. The no-link behaviour with a 10/100-only partner is shown only by the pin-level peer.
- The docs gates ran in a scratch environment with the hash-pinned markdown lock.

## Pending manager duties

- The hosted contexts were still in progress or queued when last read, with "Physical gPTP" skipped. Hosted and local-replica acceptance at the exact head is the manager's.
- The current-dev merge candidate (builder and native banks) is the manager's at the merge turn. This report claims no manager source bank.
- These maintainer acknowledgements are requested in the PR and are still open:
  - the certification_version STOP clause (the file is named, nothing is edited)
  - the material assumption of the 1000BASE-T ability gate
- The docs inventory check belongs to a dev-merge round after PR #815 lands.

R775-1 FINISHED
