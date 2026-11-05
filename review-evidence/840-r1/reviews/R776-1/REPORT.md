[R776] NEGATIVE - exact head dd764ed7c09e4764f4d7368f447e94af151a24de

External independent review R776-1 of kebag-logic/milan-fpga PR #842 (issue #840), exact head `dd764ed7c09e4764f4d7368f447e94af151a24de`, tree `7e0fae18322bfb45ada20f49493a9082c77702d9`, eleven commits on dev `604899c08ff1cd1830e1dd08b733109ef852400c`.

Context rebuilt from public material only: AGENTS.md, CONTRIBUTING.md (docs rules, section 6), docs/README.md, the #840 body (maintainer decisions 2026-11-05), the TAKEN and REVIEW READY comments, the PR body, FPGA-gPTP #100, the diff `604899c0..dd764ed7` and its history, the public evidence tree `review-evidence/840-r1` at `194f3733`, and the exact-head hosted check list. I wrote my verdict and ledger before reading any other reviewer's report. The only prior public review on this PR is the internal one at the same head (`#issuecomment-6669957820`). I read it afterwards and resolve each of its findings in the "Prior public findings" section.

Verdict: NEGATIVE. One MAJOR and two MINOR findings are open:

- F3 (MAJOR) under Tests, RTL and Docs. The prior review raised it first; I reproduced it independently and keep it.
- F1 (MINOR) under Tests.
- F2 (MINOR) under Docs.

Conformance and Robustness are covered clean at this head.

## What I checked against the scope

1. **Identity.** The AX7101 configs (`configs/endstation_ax7101_8x8.yaml:90`, `configs/endstation_ax7101_1x1_tdm8.yaml:67`) carry `02:4b:4c:00:00:01`. The three Arty configs carry `02:4b:4c:00:00:02`. I built all five configs into scratch: each overlay has `adp.entity_id` 0x024B4CFFFE000001 or 0x024B4CFFFE000002 and the matching `adp.mac_address` (receipt 25). The builder passes the same MAC as `--mac` to the gPTP microcode (`sw/builder/endstation_builder.py:5957-5961`). The AX `gptp_ucode.hex` digest `04c9adb122deec35...` equals the `gptp_ucode_sha256` in `tb/verilator/nvm_capture_cpu/measurements.json`. The ax1x1gptp leg I ran saw `GET_AVB_INFO names thisClock` and `GET_AS_PATH ends with thisClock` both equal to 0x024B4CFFFE000001 (receipt 31). The tracked `configs/generated/*/gen/adp_shape_defaults.svh` files are byte-identical to fresh builder output for all five configs (receipt 25). The company-ID octets 02, 4B, 4C are nonzero. The maintainer chose the station octets `00:00:01` and `00:00:02` themselves, so I read the issue's "no identity octet 0x00" rule as covering the CID octets, which is what the page states (`docs/reference/STRICTER_READINGS.md:42`).
2. **Builder warning.** `identity_warnings()` (`sw/builder/endstation_builder.py:5135-5156`) tests bit 41 (the U/L bit, IEEE 802-2014 8.2 and 8.4) and returns a warning but never raises. `main()` prints it to stderr only. Each of the five configs built with rc 0, one warning on stderr and none on stdout (receipt 24). Gate 28b passes (receipt 12).
3. **PHY init.** `phy_mdio_write()` (`sw/firmware/milan_baremetal/milan_baremetal.c:1017-1028`) frames ST 01, OP 01, PHYAD, REGAD, TA 10 and 16 data bits, with every bit driven by the station (IEEE 802.3 22.2.4.5). `phy_advertise_gigabit_only()` (`:1040-1067`) does the following:
   - writes only when the poll's own BMSR read shows bit 1.8 and register 15 shows bit 15.13;
   - writes register 9 with bits 12:10 kept, bit 9 set and the half duplex, test-mode and reserved bits cleared (Table 40-3);
   - writes register 4 with bits 9:5 and reserved bit 14 cleared (Table 28B-1, Table 28-2);
   - writes register 0 with AN enable and restart set, and reset and isolate cleared (22.2.4.1.7);
   - returns 0 on any unacknowledged read, so the next poll retries.

   The worst-case discovery poll is 16 transactions: ID, BMSR, registers 15/4/9/0, three writes, the BMSR re-read, and the six resolution reads. That matches the new charge `16 * max_transaction` (`tb/verilator/fw_service_budget/run.py:412`). `test_phy_firmware.py` reran green with all 16 PHY mutants and 5 boot-path mutants caught by name (receipt 10).
4. **certification_version.** It is produced in the protocol-processor submodule (`protocol-processor/hdl/aecp/ucode/gen_ucode.py:177`, `MILAN_CERT_VERSION = 0x00000000`). The gitlink `a9e84b66` is the same at base and head. The value is asserted by `protocol-processor/tb/pp_top/sim_main.cpp:3088-3090` (check M2) and `tests/features/aecp_response_contract.feature:154`. Behave reran green: 508 scenarios (receipt 16).
5. **Stricter-readings page.** It has rows for identity, link speed, certification_version and FPGA-gPTP #100 items 3 to 5. Each row gives the clause, what it allows, what the board does and why. The page is linked from `docs/README.md:129` and registered with the style gate. The gPTP rows agree with the companion issue and with the repository's own authority (`docs/reference/MILAN_COMPLIANCE_MATRIX.md:88`: 15 ms). These gates reran green: `check_doc_style.py`, `docs_check.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base 604899c0`, and `git diff --check` (receipts 13, 14, 17-20).
6. **Docs inventory.** `scripts/docs_inventory.py` is absent at base and head. It lands with PR #815, so it stays a known open point for the dev-merge round, not a finding here.
7. **Comment rule.** I scanned the 609 added non-JSON lines for lane labels, bench lane labels, review rounds, reviewer IDs and comment IDs. Nothing was found (receipt 21; the one hit is the word "turnaround").

## Findings

### F1 - MINOR - Tests - `sw/firmware/nvm_hosttest/phy_host.c:81-89, 54, 57` - the pin-level peer never exercises the masks the PHY init documents as kept or cleared

- **Authority/evidence.** AGENTS.md section 6, Tests lens: "Each new test can fail for the defect it claims to detect." `phy_host.c:83` claims "each bit the PHY init must clear or keep is graded". Three docs describe the masks as behaviour:
  - `docs/integration/BAREMETAL_FIRMWARE.md:2177-2178`: "keeps its MASTER-SLAVE bits", "keeping the selector and pause bits";
  - `docs/reference/STRICTER_READINGS.md:57`: "the MASTER-SLAVE bits are kept";
  - `milan_baremetal.c:952-961`.

  The peer starts from register 0 = 0x1000, register 4 = 0x0fe1 and register 9 = 0x0300. So the MASTER-SLAVE bits start at zero, reset and isolate start clear, and AN enable starts set. `selector_kept` (`:54`) masks 0x401f only, so the pause bits it starts with are never compared. I planted eight mutants into a scratch copy and ran them against the head's own peer (`scripts/phy_extra_mutants.py`, receipt 11). The `skip-register-4` sanity mutant was caught. Seven survived with rc 0:
  - `clear-pause-bits` (register 4 written 0x0001);
  - `drop-master-slave`;
  - `keep-test-mode`;
  - `keep-reserved-bit14`;
  - `keep-reset-isolate`;
  - `no-an-enable`;
  - `no-ability-retry-forever` (a 10/100 PHY's register 15 re-read on every poll).
- **Impact.** A regression could drop the pause advertisement or override a strapped MASTER-SLAVE configuration. It could also leave a strapped isolate set, or restart a PHY strapped with AN disabled without enabling AN. Any of these passes the gate that the docs cite as holding this behaviour.
- **Required outcome.** Either the peer's starting registers and assertions exercise every documented keep and clear, or the test comment and the docs stop claiming them. The keeps are pause bits 4.10-4.11 and MASTER-SLAVE bits 9.12-9.10. The clears are 4.14, 9.15-9.13, 0.15 and 0.10. AN enable must be forced, and a non-gigabit PHY must be read once only. At least the first four rows of the list above need a named assertion.
- **Verification.** Rerun `scripts/phy_extra_mutants.py <checkout> <work>`. Every listed mutant must exit nonzero on a named assertion, and `test_phy_firmware.py` must stay green.

### F2 - MINOR - Docs - `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1661-1665, 1678-1680, 1693-1703, 1856-1867` - section 18 and section 20 item 6 still state the superseded capture receipt as current

- **Authority/evidence.** AGENTS.md section 6, Docs lens: "Changed contracts are reflected in authoritative docs." Commit `67e61edb` replaced `tb/verilator/nvm_capture_cpu/measurements.json`. The new receipt has base `d62417f1`, tree `9ba1866d`, firmware `1071b45e...`, pins `a9e84b66`/`135afd04`, an 8x8 contract maximum of 13.85922 ms (3.5356x, so the margin is 10.64078 ms) and a 1x1 maximum of 3.96810 ms (12.3485x). The design doc was not touched. It still gives measured commit `c71364bd`, tree `69b8ed0f`, firmware `60799c75...` and pins `f65c8ff7`/`f97c1803`, plus "The worst 8x8 measurement is 13.86052 ms", 3.5352x, 10.63948 ms, 3.96490 ms and a six-arm table that matches no arm of the current receipt. Line 1856 calls this "the current receipt's identities and six maxima". Line 1687 still says the firmware changed in "its PHY poll only", but it now also writes the PHY. The harness README sends readers there (`tb/verilator/nvm_capture_cpu/README.md:137`). Dev keeps the doc in step with each re-measurement (`b6a1c189` "Refresh SAVED_STATE_SNAPSHOT_OWNERSHIP section 18 and section 20 item 6 from the re-measured capture receipt"). Separately, the new receipt's `remeasurement_assignment` points at `issues/840#issuecomment-6654606193`. That is the lane's own TAKEN comment, which does not ask for a re-measurement.
- **Impact.** The authoritative design page publishes figures and identities that no tracked receipt supports. A reader checking the hold margin against section 18 gets the superseded numbers.
- **Required outcome.** Section 18 and section 20 item 6 state the head receipt's identities, six arm ranges and maxima, and the receipt chain names the #840 re-measurement. The receipt's `remeasurement_assignment` names the public comment that required it, or the doc says the lane started it.
- **Verification.** Diff the doc's figures against `measurements.json` (`minimum_ms`/`maximum_ms`/`margin` per arm; `base`, `tree`, `product_firmware_sha256`, `processor_pins`), and rerun `check_doc_style.py`, `docs_check.py` and `gen_toc.py --check`.

### F3 - MAJOR - Tests, RTL, Docs - `tb/verilator/fw_service_budget/run.py:412`, `docs/findings/397_SERVICE_BUDGET.md:262-276`, `docs/integration/BAREMETAL_FIRMWARE.md:2201` - the raised PHY poll charge was never graded against the 250 ms publication bound at this head

The prior review raised this. I kept it after reproducing it independently; my own pass read the formula change but missed that the grading behind it was not rerun.

- **Authority/evidence.**
  - The contract is `125 ms + no-tick stretch + TX allowance + scheduling charge <= 250 ms` (`397_SERVICE_BUDGET.md:250-251`). The firmware guide says "The service harness grades this derived publication bound against 250 ms" (`BAREMETAL_FIRMWARE.md:2201`).
  - That grade, `service_findings()`, runs only in `--enforce-service` measurement runs (`run.py:765-766`). The suite (`run.py --self-test`) tests the formula only on planted numbers (`service_controls()`).
  - The head raises the charge to `P + 16*T`, and its own oracle shows both terms grew. For 8x8 `all`, T went from 8793 to 16963 cycles and P from 65294 to 247411 cycles (receipt 28, from the oracle `PHY_TIMING` lines).
  - The author's published service receipts at `d62417f1` are `all` and `uart-paced` runs only (`review-evidence/840-r1/author/receipts/service-budget-d62417f1`). No `--enforce-service` plan was run.
  - The findings page still states `C = P + 9*T` and "Nine reads" (`397_SERVICE_BUDGET.md:262-263`), and its charge and reserve tables are the base figures. The page's own base arithmetic reproduces exactly: charge 1.95488 ms, 8x8 reserve 4.46039 ms.
  - With the 397 page's 8x8 worst duty plus UART of 118.58473 ms, the head's 8x8 reserve is as follows. These are estimates, not measurements (receipt 28):

    | Charge model | Charge | Reserve |
    |---|---|---|
    | The head's `all`-plan P and T | 5.18819 ms | +1.22708 ms |
    | Base enforce-plan excess added | 5.95524 ms | +0.46003 ms |
    | Base enforce-plan excess scaled | 7.00426 ms | -0.58899 ms |

- **Impact.** The stated 250 ms PHY publication bound for the measured duties is unverified at the head and may be exceeded at 8x8. That is the case `service_findings()` exists to refuse ("over-budget PHY service stretch"). The authoritative findings page states a formula and figures the code no longer uses.
- **Required outcome.** Run the `--enforce-service` plans on both shapes at a head carrying this firmware, with no PHY service finding. If a plan fails, change the firmware or the trigger and re-measure. Then 397 states the 16-transaction formula and the measured transaction, poll, charge and reserve figures from those receipts.
- **Verification.** Run `run.py --shape <s> --plan <p> --enforce-service` for each shape and plan. Each must report no `over-budget PHY service stretch` and no `PHY publication interval exceeds 250 ms`. Then compare 397's figures against those receipts.

### R1 - RESIDUE - Docs - `tb/tools/hive_compliance.py:6-7`, `tb/tools/hive_compliance_clusters.py:7`, `tb/tools/check_tu_on_wire.sh:55` - bench usage text still names the retired AX7101 identity

The PR moved the bench tools' board defaults (`crf_vs_phc.py`, `torture_campaign.py`), but these usage examples still say `--target-eid 020000FFFE000001 --target-mac 02:00:00:00:00:01` and "e.g. 02:00:00:00:00:01". They are wording only: no default, test or fixture reads them.

Exact fix: in all three places, replace `020000FFFE000001` with `024B4CFFFE000001` and `02:00:00:00:00:01` with `02:4b:4c:00:00:01`.

### R2 - RESIDUE - Docs - `docs/reference/STRICTER_READINGS.md:19-23` - "How to read the rows" lists a Where column no table has, and omits two gPTP columns

Each section gives Where as a bullet, not a column. The gPTP table's "Reading" and "At the pinned processor" columns are not described.

Exact fix: replace line 23 with `- **Where**, a bullet under each table, names code and tests.`. Then add `- **Reading** names each gPTP row's behaviour.` and `- **At the pinned processor** states the current gitlink's behaviour.`. Each sentence is within the 10-word limit.

### S1 - SUGGESTION - Tests - `tb/verilator/milan_dp/sim_gmstep.cpp:229-232, 875` - mixed identity in a leg that loads the shipping image

The gmstep leg loads the AEM image built from `configs/endstation_ax7101_1x1_tdm8.yaml`, now entity 024B4CFFFE000001 (`tb/verilator/milan_dp/Makefile:486-487`). It still programs MAC and ADP CSRs of 02:00:00:00:00:01 / 020000FFFE000001 and addresses AECP to them. This PR moved its siblings `sim_gptp.cpp` and `sim_ax1x1gptp.cpp` to the image's identity. The identity is harness-chosen and the leg asserts no config identity, so this is optional. Aligning it would keep the served ENTITY descriptor and the ADP/AECP identity in agreement.

### S2 - SUGGESTION - Robustness - `sw/firmware/milan_baremetal/milan_baremetal.c:1140-1141` - the init runs once per boot

`phy_advertised` is never cleared. If the PHY loses its registers without a firmware reboot, it returns to its strap advertisement, and a 100 Mb/s link could form again. The docs say "once per boot", so this matches the documented design. One option is to re-arm when register 4 reads back with 10/100 bits set.

## Prior public findings

There is one prior review at this head: `[R775] NEGATIVE` at `https://github.com/kebag-logic/milan-fpga/pull/842#issuecomment-6669957820`. No commit has landed since it, so each of its findings is either kept or rejected. None can be resolved by a fix yet.

| Prior finding | Severity, lenses | Disposition at dd764ed7 | My evidence |
|---|---|---|---|
| R775 F3: PHY poll charge not graded on target data | MAJOR, Tests/RTL/Docs | KEPT as my F3 | Receipt 28 reproduces the base page's own 1.95488 ms and 4.46039 ms. The head reserve estimates are +1.22708, +0.46003 and -0.58899 ms. No `--enforce-service` receipt is in the evidence tree. `397_SERVICE_BUDGET.md:262` still reads `9*T` |
| R775 F1: five keep/clear PHY-init properties cannot fail the peer | MINOR, Tests | KEPT, the same as my F1. I found two more survivors (`no-an-enable`, `no-ability-retry-forever`) | Receipt 11 |
| R775 F2: the capture design doc states the superseded receipt | MINOR, Docs | KEPT, the same as my F2, including its line 1687 point | `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1661-1867` against `measurements.json` |
| R775 S1: `sim_ax1x1gptp.cpp:881` MAC words duplicate `kStationMac` | SUGGESTION | Agreed, optional | `sim_ax1x1gptp.cpp:881` |
| R775 S2: `nvm_capture_cpu/soc.py:187` parses only colon-spelled MACs | SUGGESTION | Agreed, optional. The builder accepts dash spellings, and a dash-spelled config would crash `int(...,16)` | `soc.py:187` |
| R775 S3: bench usage examples carry the old identity | SUGGESTION | KEPT as my R1, filed as RESIDUE because it is wording only | as R1 |

My independent ledger had RTL CLEAN. It is UNCLEAN below only because I kept F3, which the prior review files under RTL as a timing effect not understood. I agree with that filing, so the lens is not covered clean at this head.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `configs/endstation_*.yaml` platform rows; `sw/builder/endstation_builder.py:5135-5156, 5957-5961, 6106, 6156`; `sw/firmware/milan_baremetal/milan_baremetal.c:945-1067, 1139-1153` against IEEE 802.3-2022 22.2.4.1.7, 22.2.4.2.16, 22.2.4.4.3, 22.2.4.5, Table 28-2/28B-1 and Table 40-3; `protocol-processor/hdl/aecp/ucode/gen_ucode.py:177` and the unchanged gitlink; `docs/reference/STRICTER_READINGS.md` rows against #840 and FPGA-gPTP #100; receipts 12, 16, 24, 25, 31 | R776-1 | dd764ed7c09e4764f4d7368f447e94af151a24de |
| RTL | UNCLEAN (F3) | No `hdl/` file in the diff (`git diff --stat 604899c0..dd764ed7`). The PHY publication timing budget (F3: `run.py:375-436, 765-766`, oracle `PHY_TIMING` base against head, receipt 28). The firmware-to-fabric MDIO pin contract: `phy_mdio_write` frame widths and the OE/TA drive, checked against `tb/verilator/fw_service_budget/phy.hpp:16-39`, which enforces "MDIO write not driven" and "turnaround not 10". The CSR interface is unchanged (no new CSR). The poll's worst-case 16-transaction charge is in `run.py:405-415`. Receipts 10 and 15 | R776-1 | dd764ed7c09e4764f4d7368f447e94af151a24de |
| Robustness | CLEAN (S2 optional) | NAK retry paths (`milan_baremetal.c:1049-1058`; `phy_host.c` arms with `nak_register` 15 and 9); a PHY without extended status or without 15.13 (`phy_host.c:216-257`); once-only init (`advertise-every-poll` mutant); latched-loss preservation via the poll's own BMSR; the identity-mismatch path untouched (`phy_unguarded` boot mutant); a 10/100-only partner gets no link; the service budget at the boundary (`run.py:508-510`). Receipts 10, 11 and 15 | R776-1 | dd764ed7c09e4764f4d7368f447e94af151a24de |
| Tests | UNCLEAN (F1, F3) | `sw/firmware/nvm_hosttest/phy_host.c`, `phy_peer.h`, `test_phy_firmware.py` (16 + 5 mutants rerun) plus seven surviving reviewer mutants; `sw/builder/test_builder.py` gate 28b; `tb/verilator/fw_service_budget` self-test (55 oracle checks); the oracle against the author's simulation receipts (receipt 27); `scripts/check_nvm_capture.py` (receipt 23); the milan_dp `gptp` leg (210/210 PASS, receipt 30); the `ax1x1gptp` leg partial run (receipt 31); behave | R776-1 | dd764ed7c09e4764f4d7368f447e94af151a24de |
| Docs | UNCLEAN (F2, F3; R1 and R2 residue) | `docs/reference/STRICTER_READINGS.md`; `docs/findings/397_SERVICE_BUDGET.md:243-276`; `docs/integration/BAREMETAL_FIRMWARE.md:2174-2199`; `docs/README.md:129`; `docs/ENDSTATION_BUILDER.md` row 6a; `sw/builder/README-parameters.md:70`; `tb/verilator/fw_service_budget/README.md:105-110`; `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` sections 18 and 20; the docs gates (receipts 13, 14, 17-20); the comment-rule scan (receipt 21) | R776-1 | dd764ed7c09e4764f4d7368f447e94af151a24de |

## Real limits

- Physical calibration was NOT RUN and no hardware was used. The no-link result against a 10/100-only partner and the behaviour of a PHY that is never written are shown by the pin-level peer only. In that model a restart is instantaneous.
- I had no copy of the IEEE or Milan clause texts. I checked bit positions and clause numbers from working knowledge of IEEE 802.3 Clause 22/28/40 and against the repository's own authorities. I did not check them against the standards themselves.
- The `ax1x1gptp` leg built and ran to 4.75 simulated seconds with 0 FAIL, including the identity checks, but my session's time limit stopped it before it finished. Its full pass is the author's sweep receipt (`review-evidence/840-r1/author/receipts/sweep-dd764ed7`, four shards with exit 0), which I inspected but did not reproduce.
- I did not rerun the full sweep, `fw_coverage.py`, `test_nvm_firmware.py --self-test`, the RV32 legs, the capture arms or the service-budget simulations. No RV32 toolchain was on this host. Those receipts are the author's. I checked the oracle bytes against the author's three simulation receipts (identical) and against freshly built images (`run.py --self-test`).
- The oracle's `max_transaction_cycles` roughly doubled (8789 to 16957 at 1x1 "all"; 12451 to 22559 uart-paced) once the init added seven transactions. I did not find the cause. F3 depends on this. I could not run any `--enforce-service` plan myself because the product RV32 toolchain is not on this host, so F3's reserve figures are arithmetic estimates.
- At my check, hosted checks at the exact head were 57 success, 1 skipped and 3 in progress (receipt 26). The manager owns hosted and act acceptance.

## Pending manager and maintainer duties

- Maintainer acknowledgement of the STOP clause: certification_version is produced at `protocol-processor/hdl/aecp/ucode/gen_ucode.py:177` and left unchanged.
- Maintainer acknowledgement of the published material assumption that the init writes only a PHY reporting 1000BASE-T full duplex ability. This keeps the retired Arty 10/100 PHY linked.
- The docs-inventory acceptance item, once PR #815 lands on dev.
- Current-dev candidate validation (builder and native banks) at the merge turn, and hosted/act acceptance. No manager source bank at this head is claimed or inferred here.
- Carry R1 and R2 to the residue checklist.

R776-1 FINISHED
