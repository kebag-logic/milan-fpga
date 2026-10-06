[R522] POSITIVE - exact head 021b9c1fb966e9a1a4acef6b5233edd3518f32a0

# R522-1: internal independent review of PR #685 (Relates to #665, lane FC: the full-tuple mailbox ingress filter)

- **Round:** R522-1, the first review of PR #685. Internal cleared-context reviewer.
- **Exact head:** `021b9c1fb966e9a1a4acef6b5233edd3518f32a0`, tree `b7c103aaffff9a48f7c05436372875c5d94331c7`. The detached clone was verified at both before review.
- **Source base:** `6714181d0c8a16e2983f85b724f4d688f5111835`. The diff has six one-line commits with no trailers, and 35 files: 2,043 lines added and 338 removed.
- **Reconstructed from, in order:**
  - `AGENTS.md` and `CONTRIBUTING.md`;
  - the #665 issue body, then the lane FC assignment (6021509373), the executor's TAKEN post (6021668206) and REVIEW READY post (6026344516);
  - the owner decision on #664 (6014311316) and its approval (6015500032);
  - `REQUIREMENTS.md` section 1, "Mailbox ingress acceptance";
  - `docs/reference/FR_NFR.md` NFR-SCOUT-02 and NFR-SCOUT-08 (lines 322 and 328) and the hooks H-ADP, H-ACMP, H-AECP, H-MAAP and H-SRP (lines 403-410);
  - `docs/design/MAILBOX_SPLIT.md`;
  - the full diff and its history;
  - the PR body, the public evidence tree `review-evidence/665fc-r1` at `8faa1b7a` (the manifest and the author's handoff), and the exact-head hosted check runs.
- **Prior public review findings on PR #685:** there are none. The PR's only comments are the two review-start notices (6026373298, 6026374045), so nothing needs to be resolved or retained.
- **Independence:** no other reviewer's report was read.

## Verdict

**POSITIVE.** All five lenses were applied, and each is CLEAN at the exact head: no BLOCKER, MAJOR, MINOR or RESIDUE is open. Two SUGGESTIONs are recorded. They are optional test hardening, and the reviewer's probes show the behaviour they concern is already correct at this head.

Every acceptance item of assignment 6021509373 is met, checked independently below.

The strongest independent evidence is a reviewer-written randomized differential:
- 40,000 frames went through the RTL and the host model, on the shipped one-interface contract and on the two-interface variant.
- Each frame was graded against a reference typed in from the requirement table, not from the generated contract tables.
- Result: 0 disagreements.
- Directed checks also confirmed FILTER_MISMATCH saturation, the per-frame clearing of the mismatch flag, and a reset in the middle of a frame.

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE.

### S1: SUGGESTION. Three guards in the new filter RTL that no suite check reaches

- **Lenses:** Tests, Robustness.
- **Location:**
  - `hdl/milan/mailbox/KL_mbx_rx.sv:396`: the FILTER_MISMATCH saturation guard `mismatch_r != 16'hFFFF`;
  - `hdl/milan/mailbox/KL_mbx_rx.sv:359`: `mis_r <= 1'b0` in the new-frame clear;
  - `hdl/milan/mailbox/KL_mbx_rx.sv:159`: `own_if_w` in the `own` tuple.
- **Evidence:** `probes/extra_plants.py` planted each guard's removal into a copy of the head. In each case the PR's suite still passed, at 285 of 285 through Wishbone (`receipts/probe_extra_plants_suite_rerun.txt`). The reviewer's probe caught all three (`receipts/probe_extra_plants.log`):
  - with saturation removed, the RTL reads `0x4` after 65,540 mismatches while the model reads `0xffff`;
  - with the flag left uncleared, a frame shorter than 15 bytes that follows a mismatch counts once more;
  - with `own_if_w` removed, an all-zero destination on an interface index that has no interface classifies as `own`.

  At the head itself, the same probe passes all three directed checks on the RTL and the model, on both contracts (`receipts/probe_diff_if1.log`, `receipts/probe_diff_if2.log`). The behaviour is correct; only the PR's own regression suite does not cover it. The executor declared the saturation item (open risk 3).
- **Impact:** none at this head. A later edit could regress any of the three guards without a suite check reddening. The flag and `own_if_w` cases are hard to reach in the field, because a compliant MAC delivers no frame under 60 bytes and no real frame is addressed to `00:00:00:00:00:00`.
- **Suggested outcome (optional):** one suite check per guard:
  - FILTER_MISMATCH driven past `0xFFFF`;
  - a frame under 15 bytes sent straight after a counted mismatch;
  - an all-zero destination on an index with no interface while OWN_MAC is still at its reset value.
- **Verification:** each of the three plants above reddens the named check.

### S2: SUGGESTION. The generator self-test plants two of the three TPIDs

- **Lens:** Tests.
- **Location:** `sw/mailbox/gen_mailbox.py`, the contract arms "a tuple names the C-VLAN TPID" and "a tuple names the S-VLAN TPID". The contract's TPID list is at `sw/mailbox/mailbox.yaml:439`, and the refusal is at `sw/mailbox/mailbox_model.py:336`.
- **Evidence:** `receipts/gen_selftest.log` lists arms for `0x8100` and `0x88A8` only. The refusal reads the whole `tpids` list, so `0x88E7` is refused by the same line, but nothing plants it.
- **Impact:** none at this head.
- **Suggested outcome (optional):** a third arm naming `0x88E7`.
- **Verification:** the arm reports "refused".

## Clean lens results

These are reported in the findings format, each with evidence examined at the exact head.

```text
[R522] PASS Conformance — sw/mailbox/mailbox.yaml:193-251,415-540; hdl/milan/mailbox/KL_mbx_rx.sv:130-168,184-210,252-259,396; sw/firmware/ctrl/host/mbx_model.c:286-322,382-412 — every row of the owner table (#664 6014311316; REQUIREMENTS.md section 1; NFR-SCOUT-02/-08) checked against the YAML and both implementations: ADP 91:E0:F0:01:00:00/0x22F0/0xFA; ACMP same address plus own unicast as the owner's tolerance, 0xFC; AECP own unicast only, 0xFB, with (even message_type AND target_entity_id@18 = own) OR (odd AND controller_entity_id@26 = own), matching the Table 9-1 parity and the AECPDU layout; MAAP 91:E0:F0:00:FF:00/0xFE; MSRP 01:80:C2:00:00:0E/0x22EA and MVRP 01:80:C2:00:00:21/0x88F5 with no subtype; tagged frames excluded because no tuple may name a TPID (mailbox_model.py:336) and classification reads bytes 12-13; own unicast is OWN_MAC of the arrival interface only; FILTER_MISMATCH counts an untagged control-EtherType (0x22F0/0x22EA/0x88F5) tuple failure once and never a valid, tagged, identity-refused, closed-channel or short frame; token buckets unchanged. Independent reference vs RTL vs model, 2 x 20,000 frames: 0 disagreements (receipts/probe_diff_if1.log, probe_diff_if2.log). The major version goes to 2 with the YAML change rule stating why (mailbox.yaml:29-43), and mbx.c:62 refuses another major.
[R522] PASS RTL — hdl/milan/mailbox/KL_mbx_rx.sv (whole file, 424 lines), KL_mbx.sv:106,123-124,153-154,185-188,212-217,464,481,499 (generated, --check clean) — single clock, synchronous reset of every new register (dst_r, mis_r, mismatch_r, own_mac_*_r); no CDC added; the 48-bit destination is shifted big-endian over bytes 0-5 and compared at byte 14 with rx_data_i as the subtype; tuple scan first-hit with channel = j / MAX_TUPLES; the generator forbids cross-channel tuple overlap (mailbox_model.py:305-343); mis_r is set only when no tuple holds and is cleared per frame, so mis_w pulses once at FIN (accept_w is 0 whenever mis_r is 1); the counter saturates at 0xFFFF (probe: 65,540 -> 0xffff); ERR gets the pulse; an IF index past MBX_N_IF has no own MAC; KL_mbx ports unchanged; the buckets are unchanged in the diff. Verilator 5.050 -Wall build: 0 warnings (receipts/mbx_make_all.log). Default-off placement unchanged by construction: sw/litex/milan_soc.py is not in the diff; its mailbox sources and instance are added only under --ctrl-mailbox (milan_soc.py:2555-2569, 2590, 3295-3296; default False). No other path into the default build reads the changed files (the builder, configs and constraints do not).
[R522] PASS Robustness — receipts/probe_diff_if1.log, probe_diff_if2.log, probe_extra_plants.log; suite.hpp:988-1164 — malformed and boundary input (lengths 1-89 around bytes 14, 15, 26, 34, 42 and 50; frames ending before the subtype byte; reserved subtype 0xFD; broadcast, zero and one-bit-off MACs; S-tag and C-tag with mixed TPID bytes; interface indices with no interface) agree with the reference on the RTL and the model; a reset in the middle of a mismatching frame leaves FILTER_MISMATCH 0; counter saturation is correct on both; a short frame after a mismatch is not counted; repeated mismatches count one each (suite Q9: five give five); refusals take no token (suite Q10; the PR's arm rx-refusal-takes-a-token caught); closed channels never count (Q9). The three guards no suite check reaches are recorded as S1 (SUGGESTION).
[R522] PASS Tests — tb/verilator/mbx/suite.hpp:960-1164, mutants.py (21 new arms), sw/firmware/ctrl/test/ctrl_mutants.py (17 new arms), test_unit_driver.cpp D11, test_port_loop.cpp D12 and L1, test_unit_seams.cpp U4, sw/firmware/gtest/coverage.ratchet — reviewer reruns at the head: make (Wishbone 285/0, AXI4-Lite 330/0, cosim 13/0, two interfaces 285/0 and 330/0, model 285/0, quick 5 of 5); make mutants with --jobs 6: both controls green, 67 of 67, each caught by its named check; test_ctrl_firmware.py --require-rv32 --self-test: every arm green (model 21, port 31, unit 23+2, adp 26, walk 41, entity 5x9, rv32), mutants 93 of 93; fw_coverage.py --check PASS with 14 files at 100 % lines and branches after exclusions; the README exclusion table and coverage.ratchet raised, no exclusion row added; --selftest 28 of 28; tally_selftest 18 of 18. Q0 has a positive control per row; Q1-Q5 change tag, destination, EtherType, subtype and identity one at a time; Q6 untagged AAF/CRF are never delivered; Q7 the CONTROLLER_AVAILABLE response passes both ways and one for another controller is dropped; Q8 per-interface own MAC on 1 and 2 interfaces; Q9/Q10. Re-pointed arms: rx-subtype-ignored (same defect, C0 caught first), rx-second-ethertype-ignored (the second tuple is MVRP's EtherType and address; C3 caught first), app-binds-pool-after-the-mailbox (same APP_BRING->APP_BRING_LATE defect, U1 "unsatisfied and active"). The tests can fail: the reviewer's plants of the AECP response offset (26->18) and the PR's own any-unicast defect redden the suite. Gaps are recorded as S1 and S2 (SUGGESTION).
[R522] PASS Docs — docs/design/MAILBOX_SPLIT.md (the ingress filter section, verification table, measured area), docs/reference/MAILBOX_CONTRACT.md (generated; gen_mailbox.py --check --crosscheck 0 findings), tb/verilator/mbx/README.md, sw/firmware/ctrl/README.md, sw/firmware/gtest/README.md, file banners of KL_mbx_rx.sv and mbx_model.c — the described behaviour matches the RTL and the model as probed; counts match the reruns (285/330/45, 14 and 12 self-test arms, 5 quick arms, 67/93 defects, 21/31/25 tests); area rows sum consistently (LUT rows 2,710 + 20 cross-hierarchy = 2,730, the same 20 as the base's 2,621 vs 2,641; FF rows 2,852); no obsolete requirement restored; the REQUIREMENTS.md 93-94 and FR_NFR.md 427/599 status text is the manager's merge-time duty (out of this PR, per the assignment). The PR body and issue post carry enough evidence for a cold reviewer.
```

## Acceptance criteria (assignment 6021509373), checked independently

| Item | Result | Reviewer evidence |
|---|---|---|
| 1. Contract | Met | `mailbox.yaml` carries:<ul><li>the tuple table, at most two tuples per channel;</li><li>`OWN_MAC_LO/HI` at `0x080 + 8*i`;</li><li>`FILTER_MISMATCH` at `0x074`.</li></ul>`gen_mailbox.py --check --crosscheck` gives 0 findings (rc 0). `--selftest` refuses all 14 output arms and 12 contract arms, writes a clean two-interface variant and refuses a four-interface one (rc 0). The generated `KL_mbx.sv`, `KL_mbx_pkg.sv`, `mbx_contract.h` and `MAILBOX_CONTRACT.md` byte-match the generator. |
| 2. RTL | Met | Tagged frames reach no ring and no counter: 4,686 tagged frames in the differential, and Q1/Q6.<br>Each channel matches its exact tuple, then its identity term.<br>Own unicast is the arrival interface's MAC only (Q8, on 1 and 2 interfaces).<br>AECP is two-sided (Q7; the differential covers every message_type).<br>FILTER_MISMATCH counts once and never otherwise (Q9 and the differential).<br>Buckets are unchanged (Q10; the diff leaves the bucket logic untouched).<br>The default-off placement is unchanged by construction (RTL lens). |
| 3. Firmware | Met | `mbx_filter_set_own_mac` and `mbx_filter_mismatch` go through `mbx_hal_*` (`mbx.c:101-117`). `ctrl_loop_open` writes every OWN_MAC before `mbx_filter_open` (`ctrl_loop.c:69-77`; L1). Coverage is 100 % lines and branches, with no new exclusion. |
| 4. Tests | Met | The suite gives:<ul><li>a positive control per row;</li><li>separate rejections;</li><li>untagged AAF/CRF never delivered;</li><li>the CONTROLLER_AVAILABLE response both ways;</li><li>the own MAC per interface.</li></ul>A planted defect per rule is caught by its named check: RTL 21 (67 of 67 overall) and model/firmware 17 (93 of 93 overall). Both adapters and the model run the same 285 checks. The reviewer's differential independently confirms that the RTL and the model agree. |
| 5. Fixture audit | Met at the head | No tracked `*.patch` file in the root or any submodule names the mailbox (`receipts/patch_fixture_audit.txt`). Every exact-text arm plants at the head: 67 RTL, 93 firmware/model and 26 generator arms. The base-side audit is the executor's; the reviewer re-checked the three re-pointed arms (Tests lens). |

## Reviewer commands and receipts

All commands ran on the pinned Verilator 5.050, whose identity was verified as `Verilator 5.050 2026-07-01 rev v5.050`. Builds ran from an extracted copy of the head tree, with submodules copied from the clone at their pinned gitlinks. The firmware gates ran in the clone with temporary files in scratch, because they need git metadata.

| Command | rc | Result | Receipt |
|---|---:|---|---|
| `gen_mailbox.py --check --crosscheck` | 0 | 0 findings | `receipts/gen_check.*` |
| `gen_mailbox.py --selftest` | 0 | 14 + 12 arms; variant 2 clean, variant 4 refused | `receipts/gen_selftest.*` |
| `make -C tb/verilator/mbx all` | 0 | 285/0, 330/0, cosim 13/0; if2: 285/0, 330/0, model 285/0; quick 5 of 5 | `receipts/mbx_make_all.*` |
| `mutants.py --jobs 6` | 0 | controls green; 67 of 67 | `receipts/mbx_mutants.*` |
| `test_ctrl_firmware.py --require-rv32 --self-test` | 0 | every arm PASS; mutants 93 of 93 | `receipts/fw_ctrl_selftest.*` |
| `fw_coverage.py --check --jobs 4` | 0 | PASS (14 files) | `receipts/fw_cov_check.*` |
| `fw_coverage.py --selftest` | 0 | 28 of 28 | `receipts/fw_cov_selftest.*` |
| `tally_selftest.py` | 0 | 18 of 18 | `receipts/fw_tally.*` |
| `probes/run_diff_probe.sh` (1 interface, N=20000, seed 522) | 0 | 0 disagreements; 3 directed checks ok | `receipts/probe_diff_if1.*` |
| `probes/run_diff_probe.sh` (2 interfaces, N=20000, seed 6651) | 0 | 0 disagreements; 3 directed checks ok | `receipts/probe_diff_if2.*` |
| `probes/extra_plants.py` | 0 | 3 survivors of the suite (S1), all caught by the probe; probe control caught | `receipts/probe_extra_plants.*`, `receipts/*.suite.log` |
| fixture audit | — | no `*.patch` names the mailbox | `receipts/patch_fixture_audit.txt` |
| clone restore check | — | identical to the head; gitlinks unchanged | `receipts/clone_restore_check.txt` |
| hosted check runs at the exact head (read only) | — | snapshot | `receipts/hosted_checks_snapshot.txt` |

`run_diff_probe.sh` exits 1 when anything fails. `extra_plants.py` reports per arm and exits 0. In its log, "suite rc 2, 0 failing check(s)" means the suite reddened: `make` failed on a non-zero bench exit, and the failing check lines go to stderr. `receipts/probe_extra_plants_suite_rerun.txt` names them.

Local absolute paths in the receipts are replaced by `<HOME>`, `<PACKET>`, `<CLONE>`, `<PINNED_VERILATOR>` and `<VERILATOR_PREFIX>`. Nothing else was edited.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `mailbox.yaml`; `KL_mbx_rx.sv`; `mbx_model.c`; `mbx.c`; REQUIREMENTS.md section 1; FR_NFR.md NFR-SCOUT-02/-08 and H-hooks; the owner decision 6014311316; the differential probe | R522-1 | `021b9c1fb966e9a1a4acef6b5233edd3518f32a0` |
| RTL | CLEAN | `KL_mbx_rx.sv`; `KL_mbx.sv`; `KL_mbx_pkg.sv` (generated); `milan_soc.py` switch path; Verilator 5.050 -Wall build | R522-1 | `021b9c1fb966e9a1a4acef6b5233edd3518f32a0` |
| Robustness | CLEAN (S1 SUGGESTION open, which does not affect coverage) | the differential and directed probes; extra plants; suite Q1-Q10 | R522-1 | `021b9c1fb966e9a1a4acef6b5233edd3518f32a0` |
| Tests | CLEAN (S1 and S2 SUGGESTION open) | `suite.hpp`; `mutants.py`; `ctrl_mutants.py`; D11, D12, L1, U4; coverage ratchet; reruns of every gate above | R522-1 | `021b9c1fb966e9a1a4acef6b5233edd3518f32a0` |
| Docs | CLEAN | `MAILBOX_SPLIT.md`; `MAILBOX_CONTRACT.md` (generated); the mbx, ctrl and gtest READMEs; file banners; PR body; REVIEW READY post | R522-1 | `021b9c1fb966e9a1a4acef6b5233edd3518f32a0` |

## Real limits of this round

- The OOC area and timing figures (+89 LUT, +115 FF, WNS +0.271 ns) were not re-measured. No Vivado run was made in this round. They are checked for internal arithmetic only.
- The default-build identity was established by construction (no default-path file changed, and the mailbox is added only under `--ctrl-mailbox`). The reviewer ran no gateware export. The export comparison is the executor's evidence.
- The following were not rerun by the reviewer and are the executor's or manager's evidence:
  - Yosys on the mailbox tops;
  - `lint_rtl.py`;
  - `xvlog_gate.py`;
  - `test_ctrl_nvm.py`;
  - the builder bank;
  - the docs gates;
  - the lwSRP pin arm.
- The differential probe drives the Wishbone adapter only. The AXI4-Lite adapter is covered by the PR's own 330-check run, which the reviewer reran.
- The protocol clauses and addresses were checked against the requirement text and the owner decision as stated. Standard documents beyond what the repository quotes were not consulted.
- Physical calibration was NOT RUN. Field skips are not hardware proof. No hardware was used.
- Hosted runs at the exact head were in progress at the snapshot (2026-10-06T22:32:17Z). These had passed: `rtl-fast`, `firmware-unit`, `verilator-lint`, `bdd-conformance`, `yosys-elaboration`, Yosys shards 0-3/4, Verilator shard 3/5, `docs-check-no-git` and `wire-accountability`. These were still running: Verilator shards 0, 1, 2 and 4/5, `docs-check` and `elaborate`. `Physical gPTP` was skipped, which is not an executed result. The manager owns hosted and local-replica acceptance.
- The firmware gate rewrites six tracked generated headers in the clone (under `configs/generated/*/gen/` and `hdl/common/csr/gen/`). Their bytes are identical to the head blobs (`receipts/clone_restore_check.txt`: 1,141 of 1,141 tracked regular files match).

## Pending manager duties

- Update the status text in REQUIREMENTS.md lines 93-94 and FR_NFR.md lines 427 and 599 ("awaits the contract lane after FT") at merge, as the assignment states.
- Build and validate the current-dev candidate (live dev `6a05347d4e2ec1dcb37d4e5806c7767537de3ce0`) at the merge turn. This round reviewed the source head only.
- Accept the exact-head hosted gates once complete, and the local-replica run.
- Run the parts of the full bank this round did not rerun (see the limits above).
- Obtain the external review.
- Carry S1 and S2 as optional follow-ups at the executor's or owner's discretion.

R522-1 FINISHED
