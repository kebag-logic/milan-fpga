[R746] POSITIVE - exact head b6a1c189fa83de85b470c77a2c7c1e5996138909

Whole-PR external review, round R746-1. Reviewed tree `74c696c64d1eb5b12fc7154a38cbc6d656954c50` against base `1e80128f0a467b58bf884b7d9bf62e013a2fb141`. Source paths below refer to [this exact head](https://github.com/kebag-logic/milan-fpga/tree/b6a1c189fa83de85b470c77a2c7c1e5996138909).

No BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION findings. All five lenses are CLEAN for the scoped source change. This verdict does not certify merge readiness or close issue #70.

The independent verdict and ledger were written to `independent-verdict.md` before reading issue/PR comments or prior findings. The public comments were reconciled afterwards. No private author material, other reviewer report, source fix, commit, push, GitHub write, hardware access or full bank was used. Supplemental mutation execution is now complete.

**Scope and public reconciliation.** The [2026-10-30 assignment](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-6515314113) narrows this PR to the two recorded firmware defects, volatile-state desk coverage, UART consumers and regenerated evidence. It explicitly excludes the full sweep and physical release campaign. The issue body remains the larger saved-state acceptance contract; this PR correctly says `Relates to #70`.

The post-checkpoint query found two review-start comments, zero submitted reviews and zero inline review comments on PR #816. There were no prior published PR #816 findings to resolve or retain. The [older #70 defect record](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5904331147) is reconciled as follows:

| Recorded item | Disposition at this head | Evidence |
|---|---|---|
| D3 5.3 change 3 / R413-1 F2: enabled claim after CLOSED | RESOLVED in this scope | Firmware lines 1552 and 1857 report the terminal wait and enable request; CLOSED and stalled cases pass; both old-message mutants fail their named checks. |
| R412-1 S2: persistence-disabled PHY never published | RESOLVED | Firmware lines 1099-1103 and 1671-1677 admit PHY service independently and install the idle hook; disabled boot publishes negotiated status; restoring the old writer guard is killed. |
| Volatile-set desk acceptance and IDENTIFY exclusion | MET for desk scope | Retained-window reset, nonblank restoration and three named reset-mutant failures; published processor `identify_is_a_change` control is killed. Physical observation remains separate. |

**Conformance and enable data flow.** D3 `SAVED_STATE_MATERIALIZATION.md` 5.3 change 3 requires reporting without making a restore decision. At `milan_baremetal.c:1533-1556`, terminal detection, bounded wait, restore-start bit and clearing of that bit are unchanged. At `:1851-1857`, `if (!verified)` still dominates the same two enable-setting writes, one per bit, to PP_CTRL[0] and ADP_CTRL[0]. `load_aem_image()` and `milan_init()` retain the same verifier-return, saved verdict, NVM call and choke-point invocation.

This conclusion uses the full delta and the published builder gate 1b resolved-address/CFG and linked-verdict census, not a count of matching source strings. That census ran at `c71364bd`; the complete firmware, builder, RTL and configuration inputs remain byte-identical at the reviewed head. `audit_evidence.py` checks that inheritance. The unchanged datapath at `hdl/milan/milan_datapath.sv:9547` gates the requested enable with the map-restore hold. The pinned processor at `hdl/top/protocol_processor_top.sv:1971,2865` further requires the combined restore-done verdict. CLOSED does not assert done. Neither new print can release the fabric.

**PHY and failure paths.** REQ-MAC-03 requires negotiated link state to reach the status path. `phy_live` is zero-initialized and set after identity/configuration admission, before the shape refusal. The no-writer branch polls and returns before writer heartbeat activity; `nvm_service()` retains its writer-readiness gate. The admitted-writer path still takes one time sample and uses the original heartbeat policy. The disabled path installs the idle hook. Identity mismatch returns before PHY admission.

The pin-level test exercises shipping, shape-disabled and identity-mismatch boots; the first two publish status 13 with eight idle publications in one second, while identity mismatch performs zero transfers/publications. Its five boot mutants are all killed by named findings. Existing pin-level controls also pass. The firmware self-test covers seven boot paths per shape, including CLOSED and indefinite stall, across five shapes; the stalled paths require the timeout report and the CLOSED paths must terminate without waiting out the timeout.

The three published service traces were independently regraded under the enforced service rule, all with zero findings. Maximum PHY publication bounds are 178.12012 ms (1x1 all), 184.78212 ms (1x1 paced) and 244.518031 ms (8x8), below 250 ms. Maximum heartbeat gaps are 266.01756, 257.63916 and 323.67890 ms, below 500 ms. The matched 1x1 base comparison records boot -0.01072 ms, commit growth below 0.09 ms and heartbeat-gap growth 0.08456 ms. The two 8x8 historical response-duration findings are unchanged from base; ordinary console response duration is distinct from the enforced service rule. Long BIOS built-in bodies remain outside these measured duties.

**Volatile reset and test sensitivity.** Milan v1.2 5.3.4.1, 5.3.4.2 and 5.3.12, D3 section 9 and the pinned processor memory-map section 5.1 define the volatile set. `tb/verilator/milan_dp/sim_nxn.cpp:5843-5975` proves registration by a notification to controller A, IDENTIFY by GET_CONTROL=255, and locking by the owner reply, status bit and refusal of controller B. It proves the retained window still equals the saved set before reset. `maprec_cut_the_power()` resets datapath and bus state while retaining window bytes; the subsequent restore reaches done with busy/fail/blank clear and recovers the saved name. IDENTIFY reads zero; the lock bit clears; B can change the name; that accepted change notifies nobody. An unsuccessful change cannot satisfy the registry check.

Reviewer execution on the pinned 5.050 simulator produced 711 checks, zero failures. The three processor-copy mutants compiled and completed normally with nonzero test verdicts: lock retention failed three of 711 checks, registry retention one, IDENTIFY retention one. Each failed its designated assertion. Full simulation logs and exit codes are retained. The separate positive control avoids interpreting a build error, crash or unrelated failure as a kill. Published processor evidence additionally kills `identify_is_a_change` through D3S7 and all three processor volatile-reset controls.

**Documentation and generated evidence.** All changed documentation, command-table hashes, firmware/test code, history and both generated records were examined. The executable old-UART reader search leaves only intentional old-line mutants; historical silicon quotations remain historical. `scripts/baremetal_uart_smoke.py` grades parsed CSR/AEM status and does not consume either old boot string. The BDD steps have no old-string dependency. The service grader, boot-walk checker, deployment guide and oracle move together. New source-comment lines contain behavior/specification references and no prohibited review or bench-lane labels.

`audit_evidence.py` verifies 373 published receipt/script hashes. All six sets of 16 capture rows match the published measurements and recompute correctly. The firmware digest is `60799c75d009ebbedbe0476ea0a8efe81f60d342141743956a8fd9a46229a625`; the recorded measured tree is `69b8ed0ff4b699434720bd96d8a0bcfabe5dc636` at `c71364bd`. The contract 8x8 maximum is 13.86052 ms against 24.5 ms, margin 10.63948 ms; the 1x1 maximum is 3.96490 ms. The 100 MHz 8x8 comparison remains non-contract. The service oracle exactly matches the published traces and graded fields; its digest matches the generator receipt, which records a byte-identical second generation. Snapshot-ownership sections 18 and 20 agree with these measurements.

**Execution evidence.** Reviewer commands, elapsed times and exits are in `logs/*.json`; corresponding `.log` files retain output. The reviewer reran:

| Check | Result |
|---|---|
| `test_nvm_firmware.py --self-test --jobs 4` | PASS, five shapes and all planted defects; 269.936 s |
| `test_phy_firmware.py` | PASS, pin-level checks and five boot mutants; 21.200 s |
| `make -j16 -C tb/verilator/milan_dp dynmap VERILATOR_JOBS=5` with pinned simulator | 711/0; 232.569 s |
| `run_volatile_mutants.py <disposable-repo> --jobs 3` | All three named kills; 262.483 s |
| `check_nvm_capture.py` | PASS |
| `fw_service_budget/run.py --self-test` | PASS, oracle and flash controls |
| `baremetal_uart_smoke.py --self-test` | PASS |
| `docs_check.py`, `check_feature_status.py` | PASS; documentation scan zero findings |
| Published-evidence audit and final raw snapshot checks | PASS |

The [author receipt packet](https://github.com/kebag-logic/milan-fpga/tree/999e04e9c417e080d988a0747359c60d2e9edb8a/review-evidence/70b-r1/author/receipts) supplies the prohibited-to-rerun banks and additional coverage:

| Receipt | Execution head and assessed result |
|---|---|
| `builder/builder-require-rv32-c71364bd.log` | `c71364bd`: builder and verdict/image pins pass; calibration gate 11 NOT RUN. Relevant inputs unchanged. |
| `firmware_unit/runner.out`, `01.log` through `07.log` | `dc7b1417`: seven commands rc 0, including firmware self-tests and coverage; 30-file coverage gate reports eligible lines/branches 100%. These control/NVM firmware inputs are unchanged. |
| `nvm_cosim/nvm_cosim-c71364bd.log` | `c71364bd`: 465/0; 39/39 mutants killed; inputs unchanged. |
| `milan_dp/legs-1767346a.log` | `1767346a`: dynmap 711/0, maprec8 219/0, maprec4 137/0; relevant inputs unchanged. |
| `processor/d3_mutants-*.log` | Unchanged pin `f65c8ff7`: IDENTIFY exclusion 1/1 killed and volatile resets 3/3 killed. |
| `gates-final/summary.md` and constituent logs | Exact reviewed head: 100 gates, zero nonzero exits; behave 495 scenarios/2288 steps passed, no skipped scenarios. |

These are author source-execution receipts. No manager source bank at this head is claimed or inferred.

**Reviewer-owned coverage ledger.** Each row records the applied lens, including clean results without findings.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | D3 5.3/9; REQ-MAC-03; firmware `:1533,:1668,:1851`; volatile readbacks `sim_nxn.cpp:5895`; `logs/nvm-selftest.log` | R746-1 | b6a1c189fa83de85b470c77a2c7c1e5996138909 |
| RTL | CLEAN | Whole diff without RTL/gitlink change; `milan_datapath.sv:9547`; processor top `:1971,:2865`; builder gate 1b receipt and unchanged-input audit | R746-1 | b6a1c189fa83de85b470c77a2c7c1e5996138909 |
| Robustness | CLEAN | `test_boot_walk.py:33,58,99`; `test_phy_firmware.py:75`; firmware disabled/identity guards; retained-window reset `sim_nxn.cpp:5083`; named mutant logs | R746-1 | b6a1c189fa83de85b470c77a2c7c1e5996138909 |
| Tests | CLEAN | `dynmap_mutants.py:440,532,548`; `logs/dynmap-clean.log`; three complete mutant logs; firmware/PHY self-tests; inherited firmware-unit, builder, co-simulation and behave receipts | R746-1 | b6a1c189fa83de85b470c77a2c7c1e5996138909 |
| Docs | CLEAN | Complete changed-doc/command-table delta; UART reader census; `measurements.json`, `oracle.json`; `logs/evidence-audit-final.log`; docs/feature checks; public scope reconciliation | R746-1 | b6a1c189fa83de85b470c77a2c7c1e5996138909 |

**Limits and pending manager duties.** Hosted status was sampled once after the independent checkpoint. Seventeen jobs showed successful completion, including firmware-unit, firmware AECP/control/SRP mutants, firmware-boundary, firmware-verilator and BDD. Thirty-one jobs were incomplete. Physical gPTP was skipped, not executed. `hosted-status.json` preserves that snapshot; it does not establish aggregate acceptance. The manager owns hosted/act acceptance, completion of the other independent review, and validation of the final current-dev merge candidate with builder/native banks and linked receipts. Merge and post-merge containment remain pending.

Physical calibration gate 11 was NOT RUN; the inventory check was NOT RUN locally because its pinned parser was absent. The PR reports 32 pre-existing command-table declarations stale at base; this change repins four changed declarations that were synchronized there. Neither those limits nor skipped field jobs are hardware proof. The supplied cold-boot observation of the new UART line is an owner-supplied observation on the pre-run image, not an independently reproduced physical acceptance result. No new capture simulation, full bank, physical timing, cold-cycle or release soak is claimed from this reviewer. Issue #70 and the #76 release obligations remain open.

Final integrity verification compares every tracked blob byte, executable/symlink mode and index entry against HEAD in both the review clone and disposable probe clone, recursively including initialized submodules. All pass. Required pins remain processor `f65c8ff7c673aaa8e2ea8da654f081ddb13588d8`, gPTP `f97c18035be6ef5345e5af27db2124c5697c1b40`, and the recorded third-party pins. The unused `external` module remains uninitialized; its index gitlink is verified. No tracked bytes needed restoration.

Portable scripts accept the repository path; the mutation runner also accepts `--verilator`. Builds and processor mutation copies reside only under `scratch/`. Published logs have path-only redactions, with original/published hashes in `RECEIPT_PROVENANCE.json`; unredacted originals stay in unpublished scratch. Only `MANIFEST.sha256` entries and this report are intended for publication.

R746-1 FINISHED
