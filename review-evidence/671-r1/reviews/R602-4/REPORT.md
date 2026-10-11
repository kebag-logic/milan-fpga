[R602] POSITIVE - exact head 7bc7ceca6ba1dd1a268d6fa1704613bb141487fe

Internal independent review R602-4 of issue #671 / PR #715. Head `7bc7ceca6ba1dd1a268d6fa1704613bb141487fe`, tree `70ee92ab909f37d435caa0b94daab84bff83d60d`. Diff from source base `e8454e2751d05b02ee8e5a571857589ab358ab86`: 23 commits, 15 files, no `hdl/` file, no gitlink change.

**Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR is open at this head. I record two SUGGESTIONs and no RESIDUE. All five lenses are covered CLEAN at this head.

- Acceptance 1 to 3 are met.
- Every prior public finding on this PR is resolved at this head, except the prefill read. The round-3 assignment placed that outside #671, and it is tracked as open issue #717.
- Round 4's required outcome now holds. Check 13 generates every fault window over the complete read bound. A reference model pins each case's exact read count and hold. The re-stage bound is pinned from both sides on the first shape and both product shapes.

I wrote my verdict and ledger before reading any prior review report on this PR. I then read R602-1 to R602-3 and R603-1 to R603-3 to resolve them, and I did not read the concurrent R603-4 round.

## Reconstruction

- **Order.** AGENTS.md, then CONTRIBUTING.md sections 3 and 6, then docs/README.md. Then the #671 body and the manager's assignments (6098494890, 6100704879, 6103025987, 6104799677). Then the executor's TAKEN and REVIEW READY comments 1 to 4 and the PR body. Then the diff and history, `sw/firmware/ctrl_nvm/README.md` Boot items 3, 4 and 9, FASTCONNECT section 7, and SNAPSHOT_OWNERSHIP sections 7, 17 and 18. Last, the public evidence tree `review-evidence/671-r1` at `25ad3f94`. That tree holds round-1 author evidence, so I re-ran the relevant gates at this head.
- **Frozen acceptance (issue body).**
  1. In the shipping path's tests: a transient refusal of A, then a real change, its commit and a clean reboot. The change survives, or persistence was refused. Run in both slot orientations and at the sequence boundaries.
  2. A planted restart-at-zero control fails.
  3. The A/B power-loss guarantees are unchanged.
- **Scope (assignment 6098494890 and rounds 2 to 4).** The media-fault rule of the Mark II store, applied wherever the shipping path derives the generation. Named controls must fail by name. Capture is re-measured.
  - Round 4 adds: check 13 generates its windows (every start in the boot and restart bound, lengths 1 to 4, and the whole boot); a reference model gives exact read counts; named controls for an unbounded re-stage, a four-try re-stage and a four-try judgement redden on three shapes; the base reproduction is attributed correctly; and the console names the re-stage cause.
- **Where the generation is derived.** Only in the firmware.
  - `hdl/milan/KL_nvm_backend.sv:424,439,482,490,582`: `seq_r` is a CSR word that is written and read back. Nothing decides on it.
  - In the processor at `2ad2f845`, `KL_pp_nvm_mgr_arb.sv` and `KL_acmp_nvm_shadow.sv` mention "sequence" only for restore sequencing, not a generation.
  - So the processor half of acceptance 1 does not apply, and no adoption is needed.

## Findings

### R602-4-S1 - SUGGESTION - Tests - the `read faults=` count on the boot line is reported but graded by no check

- **Where.** The counter is `milan_baremetal.c:481-485`. It is incremented at `:799-800` (judgement) and `:825` (re-stage), and printed at `:1773`.
- **Evidence.** I planted two defects into a copy of the firmware:
  - `q_judge_no_fault_count` drops the judgement increment;
  - `q_restage_no_fault_count` drops the re-stage increment.
- **Result.** Each gives **0 findings** under the head's full checks 13 and 14:
  - both on `endstation_arty_4x4`;
  - the re-stage one also on `endstation_ax7101_1x1_tdm8` and `endstation_ax7101_8x8`.
- **Receipts.** `receipts/probes_arty_B.json`, `probes_1x1.json`, `probes_8x8.json`.
- **Why this is only a SUGGESTION.**
  - The acceptance requires that the condition is reported. The `unread=` field, the HELD line, the console refusal and `nvm_backed` 0 report it, and all of them are graded.
  - The count is documented as a diagnostic floor (R602-1-S1, resolved).
  - No document claims the count is tested.
- **Optional outcome.** Either grade `read faults=` against a floor derived from `read_fault_cases.expect`, or say in the host README that the count is not graded.

### R602-4-S2 - SUGGESTION - Tests, Robustness - no generated case faults both slots in one boot

- **Where.** `read_fault_cases.py:144-158,199-225`. Each case plants exactly one fault, on one slot.
- **Evidence (`receipts/crosscheck_model.json`).** Across all 2,244 generated cases, the most reads any case opens is 8 on a cold boot and 7 on a restart. The stated bounds are 13 and 12.
- **What is still pinned.**
  - Each judgement's and each re-stage's three-read bound is pinned from both sides by the exact counts. My two-try and four-try plants and the lane's are all caught.
  - The total bound is reached only by the unbounded plants.
- **What is reached only by reading.** Two `nvm_boot()` paths are reached by reading only (`milan_baremetal.c:1660-1688`):
  - both slots UNREAD;
  - one slot UNREAD at its judgement while the other's re-stage fails, so no slot is offered, the blank image is staged and the writer holds.
- I read both paths, and they are correct.
- **Scope.** This is inside the round-4 assignment's defined class, which is single-fault windows.
- **Optional outcome.** Add one case per such path, faulting both slots, with its exact count and hold.

No RESIDUE is carried by this round.

## Prior public findings, resolved or retained at this head

| Prior finding | State at 7bc7ceca | Evidence at this head |
|---|---|---|
| R602-3-F1 / R603-3-F1 (MINOR; Tests, Robustness, Docs): the re-stage retry bound is reached by no check that can fail | RESOLVED | `read_fault_cases.py:188-196`: `windows()` covers every start 0 to 12 (cold) and 0 to 11 (restart), lengths 1 to 4, plus whole; my check confirms `windows_complete: true` (`receipts/crosscheck_model.json`). Exact counts come from `expect()` (`:243-286`) through `read_findings` (`:329-341`). My run catches each control on three shapes in its own words (`receipts/selftest_head.log`): `p_restage_unbounded`, `r_restage_four_tries`, `r_judge_four_tries`. My own two-try re-stage and two-try judgement plants are caught too: 193 and 311 findings (`receipts/probes_arty_B.json`). The coverage sentences the round-3 body made no longer appear in the body. |
| R602-3-F2 (MINOR, Docs): the base reproduction figure was the round-2 harness's | RESOLVED | The PR body gives 2,660 findings and 124 lost changes at this head, explains how the restart statics were matched, and attributes 645 / 124 to `9112a0df`. I reproduced 2,660 / 124 independently on `endstation_arty_4x4`, `endstation_ax7101_1x1_tdm8` and `endstation_ax7101_8x8` (label `base` in `receipts/probes_*.json`). |
| R602-3-S1: what a held re-attach publishes | RESOLVED | `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:725-733` and `BAREMETAL_FIRMWARE.md:2047-2052`. |
| R603-3-S1: the hold names the wrong cause for a re-stage | RESOLVED | `nvm_unstaged` (`milan_baremetal.c:476,1671`) and `nvm_print_unread` (`:1569-1580`). `hold_findings` grades the cause against the model (`read_fault_cases.py:344-362`). My plant `q_unstaged_wrong_slot`, which records the cause against the wrong slot, gives 86 "names another cause" findings. |
| R603-2-F1 / R602-2-F1: the re-attach hold is reached by no gate | RESOLVED | Of the 2,158 cases per shape, 1,039 are restarts. `r_reattach_goes_live` is caught on three shapes. My `q_hold_on_a_only` and `q_hold_on_unstaged_only` give 51 and 65 "re-attached live" findings. |
| R603-2-S1, R603-2-S2, R603-2-R1, R602-2-S1, R602-2-R1 | RESOLVED | Exact counts are pinned. The held re-attach prints "re-attached and HELD" (`:1713-1714`). `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:725-733` and `BAREMETAL_FIRMWARE.md:2053-2060` carry the texts. |
| R602-2-S2 / R603-2-OBS-1: the runtime prefill reads flash afresh | RETAINED, out of scope | `nvm_prefill_stage()` is unchanged (`:1248-1258`). Tracked as #717 (OPEN). |
| R603-1-F1, R603-1-F2, R603-1-R1, R603-1-S1 to S3, R602-1-F1, R602-1-R1 to R4, R602-1-S1 to S3 | RESOLVED | Record-area and both-valid faults are present (`GROUPS`, `:144-148`), and every saved record is graded (`test_nvm_firmware.py:675-716`). The worst-case boot estimate is in the PR body. The README numbers 14 checks. Wipe while held, the retire causes and `--read-other` are covered (`:812-839`). The FASTCONNECT text is at `:781-800`. R602-1-R4's sentence was superseded when the generated windows replaced the hand-picked ones. |

## Per-lens results

```text
[R602] PASS Conformance - sw/firmware/milan_baremetal/milan_baremetal.c:366,740-828,1592-1603,1632-1785,1957,1992-2003; hdl/milan/KL_nvm_backend.sv:424,439,482,490,582; protocol-processor@2ad2f845 KL_pp_nvm_mgr_arb.sv, KL_acmp_nvm_shadow.sv; receipts/selftest_head.log; receipts/probes_*.json (label base) - checked against #671 Required and Acceptance 1-3, assignments 6098494890/6104799677 and ctrl_nvm README Boot 3/4/9. No sequence is taken from bytes that failed validation (rd.seq is set on VD_OK only, :760-761; nvm_seq is 0 with nothing offered, :1686). OK stands on one read; any other verdict needs two of at most three reads with the same bytes (verdict, count, CRC-32 over every byte read, :768-771,784-809). The pick is re-staged under its sequence within three reads (:816-828); one that never reads back is UNREAD and the other slot is offered (:1669-1681). Any UNREAD slot holds the cold boot and the re-attach (:1592-1603,1712,1749). Acceptance 1: 2,158 cases per shape, both orientations, sequences 1/0x5A5A5/0x80000000/0xFFFFFFFF and the wrap, each followed by change, commit and clean reboot. Every orientation and manner meets every sequence of its group (crosscheck_model.json seq_coverage). Base e8454e27 loses the change 124 times per shape under these checks. Acceptance 2: restart_at_zero is caught by "was lost on the clean reboot" on three shapes. Acceptance 3: the commit/erase/program/verify functions are outside the diff; checks 1-12 and nvm_cosim 465/465 pass; ctrl_nvm sources are untouched.
[R602] PASS RTL - git diff e8454e27..7bc7ceca --stat (no hdl/ file, no gitlink); milan_baremetal.c:415 (static assert: 64 KiB slot fits the stage) against sw/litex/milan_soc.py:3025-3032,4094-4097 (the stage is the 64 KiB erase block below the live window, private to the firmware); :740-766 (the copy is bounded by the rule-3 length <= NVM_SLOT_BYTES; unsigned indices; the digest spans exactly rd.bytes); :1539-1547 (the window is filled from the judged stage; a VD_OK container is exactly NVM_IMG_LEN by :720-723); :1669-1681 (the re-pick loop ends: each pass removes a slot); KL_nvm_backend.sv seq_r store/read-back; receipts/nvm_cosim_head.log with pinned Verilator 5.050 (wrapper sha256 905795b9...) against the shipping backend and donor: 465/465 PASS, 39/39 mutants killed. Checked against the snapshot-ownership contract (section 7 re-attach, section 17 stage) and the 2,000 ms T-NVM-WRITER-ALIVE.
[R602] PASS Robustness - read_fault_cases.py:188-286; test_nvm_firmware.py:675-880; nvm_host.c:162-200,538-570; receipts/probes_arty_A.json, probes_arty_B.json, probes_1x1.json, probes_8x8.json; receipts/crosscheck_model.json - malformed input (header, sequence and record-area bytes, a different wrong byte on every read), blank and all-0xFF reads, address faults, minimum and maximum sequences and the wrap, invalid ordering (a fault on the pick's re-stage), reset during activity (1,039 restarts with the fabric kept), a held writer's liveness (q_go_live_not_retired caught: 226 "persisted something" on each of three shapes), the four retire causes, an explicit wipe while held, and the read-storm bound (1,000 reads per boot). The 86 dropped cases are 24 all-0xFF and 62 address faults, none of them byte faults; my independent model agrees with expect() on all 2,244 cases (0 mismatches), so they are exactly the stated detection limit. Both-slot faults: R602-4-S2.
[R602] PASS Tests - sw/firmware/nvm_hosttest/{read_fault_cases.py,test_nvm_firmware.py,nvm_host.c,writer_restart.py,stubs/}; tb/verilator/nvm_cosim/run_cases.py:72; receipts/selftest_head.log (rc 0; "OK across 5 shape(s), and every planted defect reddened"; 46 "self-test OK" lines; all 13 #671 controls on three shapes); my 13 plants in scripts/probe_mutants.py, graded by the full checks 13 and 14 - 10 behavioural plants caught (11 to 2,456 findings each), q_digest_ignores_bytes equivalent (0), and the two read-fault-counter plants uncaught (R602-4-S1, a SUGGESTION). The reference model was cross-checked against my own model on all generated cases (crosscheck_model.json, rc 0). Case counts match the documented ones: 2,244 generated, 2,158 run, 1,119 cold, 1,039 restart.
[R602] PASS Docs - docs/design/SAVED_STATE_FASTCONNECT.md:128,781-800; docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:719-733,1626-1676,1818-1829; docs/integration/BAREMETAL_FIRMWARE.md:2014-2066,2168-2182; sw/firmware/nvm_hosttest/README.md:43-75,98-259; tb/verilator/nvm_cosim/README.md:69-78; test_nvm_firmware.py docstring; PR #715 body - checked against the code and receipts. Every section-18 figure matches tb/verilator/nvm_capture_cpu/measurements.json (six arms recomputed); the harness sha256 values match the tree; the measured tree ff75487c is cb30a99a's, and milan_baremetal.c is unchanged from cb30a99a to the head. The base 2,660/124 figure, the 46 controls and the 2,158/86 split were reproduced. Gates: receipts/capture_gate.log (PASS; four mutation arms rc 1); receipts/docs_gates.log (docs_check, check_doc_paths, check_doc_style, py/cpp idiom and hygiene rc 0; gen_toc --selftest/--verify-anchors/--check rc 0 in the pinned Markdown environment). No em dash in any added line.
```

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #671 body and assignments; `milan_baremetal.c:366,740-828,1592-1603,1632-1785,1992-2003`; `KL_nvm_backend.sv:424-582`; processor files at `2ad2f845`; `ctrl_nvm/README.md` Boot 3/4/9; `selftest_head.log`; base reproduction in `probes_*.json` | R602-4 | `7bc7ceca6ba1dd1a268d6fa1704613bb141487fe` |
| RTL | CLEAN | diff stat (no `hdl/` file); `milan_baremetal.c:415,740-766,1539-1547,1669-1681`; `milan_soc.py:3025-3032,4094-4097`; `nvm_cosim_head.log` (465/465, 39/39) | R602-4 | `7bc7ceca6ba1dd1a268d6fa1704613bb141487fe` |
| Robustness | CLEAN (S2 is a SUGGESTION) | `read_fault_cases.py`; `nvm_host.c` fault model; restart, retire, wipe, liveness and storm paths; `probes_*.json`; `crosscheck_model.json` | R602-4 | `7bc7ceca6ba1dd1a268d6fa1704613bb141487fe` |
| Tests | CLEAN (S1 and S2 are SUGGESTIONs) | host suite sources; `selftest_head.log`; 13 reviewer plants; model cross-check; `nvm_cosim_head.log` | R602-4 | `7bc7ceca6ba1dd1a268d6fa1704613bb141487fe` |
| Docs | CLEAN | FASTCONNECT 7; SNAPSHOT_OWNERSHIP 7 and 18; BAREMETAL_FIRMWARE Boot and host suite; host README; cosim README; PR body; `measurements.json`; `capture_gate.log`; `docs_gates.log` | R602-4 | `7bc7ceca6ba1dd1a268d6fa1704613bb141487fe` |

## Executed at this head

All runs were local in this clone or a scratch export. Environment: CPython 3.14.7, host gcc 16.2.1, and the pinned Verilator 5.050 wrapper (sha256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`, reports "5.050 2026-07-01 rev v5.050").

| command | result | receipt |
|---|---|---|
| `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test --jobs 11` | rc 0, 336 s; "saved-state writer gate: OK across 5 shape(s), and every planted defect reddened"; 46 controls | `receipts/selftest_head.{log,rc}` |
| `make -C tb/verilator/nvm_cosim run JOBS=4 POOL=4` (pinned Verilator) | rc 0, 583 s; "465 checks: 465 PASS, 0 FAIL", "39 of 39 mutant(s) killed", "RESULT: PASS" | `receipts/nvm_cosim_head.{log,rc}` |
| `scripts/probe_mutants.py` (13 reviewer plants plus base, first shape; 3 plants plus base on each product shape) | as in the findings and ledger; base 2,660 / 124 on all three shapes | `receipts/probes_*.{json,log}` |
| `scripts/crosscheck_model.py` | rc 0; 2,244 / 2,158 / 86; 0 model mismatches; no byte fault dropped; windows complete | `receipts/crosscheck_model.json` |
| `python3 scripts/check_nvm_capture.py` and its four `--mutation` arms | rc 0; then rc 1 on each arm | `receipts/capture_gate.log` |
| docs, TOC, idiom and hygiene gates | rc 0 each | `receipts/docs_gates.log` |
| `scripts/verify_restore.sh` | head and tree match; index equals the HEAD tree; 0 status lines including ignored; 0 re-hash mismatches; three gitlinks at their pins and clean | `receipts/restore_verification.txt` |

**Hosted, read only** (`receipts/hosted_checks_exact_head.txt`, fetched 07:46Z):

- 12 contexts had completed `success`.
- 7 were `in_progress`: `docs-check`, `elaborate`, `firmware-unit`, and Verilator shards 0, 1, 2 and 4 of 5.
- "Physical gPTP (nightly and manual)" was `skipped`. A skipped context is not evidence.
- I claim no hosted or act acceptance.

**Restore.** I removed the build outputs and caches my runs created: `tb/verilator/nvm_cosim/{build,runs}`, two `__pycache__` directories in this clone, and one under `protocol-processor/hdl/aecp/desc`. All were created after this session began. The index and the submodule status equal the snapshot I took at the start. `external` and `third_party/lwSRP` were left uninitialised, as they were found.

## Real limits

- Physical calibration was NOT RUN: no hardware, bench, flashing or field run. Field skips are not hardware proof.
- No manager source bank ran at this head, and I claim and infer none.
- I did not re-run the following, and rely on the executor's published receipts and statements:
  - the builder bank (`test_builder.py --require-rv32` / `--require-elaboration`);
  - the Mark II store suite (`test_ctrl_nvm.py`; its sources are outside the diff);
  - `fw_service_budget` and the record-space gate;
  - the six-arm capture re-measurement (I checked receipt consistency, harness hashes, the figures and the gate);
  - the firmware digest and size with the pinned RV32 SDK;
  - the measured per-read boot costs. The faulted worst-case boot of about 16.4 s / 17.1 s stays an estimate.
- The host model counts one read per evaluation of `SPIFLASH_BASE` and faults whole reads of one slot. Three faults remain undetectable by design, as stated in both suites:
  - the same wrong bytes twice;
  - two all-0xFF reads;
  - an address fault answering with the other slot's valid container.
- The restart model resets the writer's statics only, so obligation O4 is assumed. D3 DR3b couples CPU and fabric resets in the product.
- The builder gate's 1,200 s writer timeout was not exercised on hosted hardware at this head when fetched.

## Pending manager duties

- Hosted and act acceptance at this exact head. In particular, the 7 contexts in progress at fetch time. Two of them run the writer gate: `docs-check` (`docs.yml:205,233`) and `elaborate` (`elaborate.yml:260`, through the builder under its 1,200 s timeout).
- Validate the current-dev merge candidate (source base `e8454e27`, live dev `ac2c5e77`) with the builder and native banks, and link the receipts.
- Keep #717 (prefill read) tracked.
- Optional: carry R602-4-S1 and R602-4-S2.

R602-4 FINISHED
