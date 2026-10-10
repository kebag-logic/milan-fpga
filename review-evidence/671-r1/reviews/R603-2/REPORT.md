[R603] NEGATIVE - exact head 9112a0df27acc1381091845e94d8eaa1407f1bbb

# R603-2: external review of PR #715 (issue #671), round 2

- **Head under review.** `9112a0df27acc1381091845e94d8eaa1407f1bbb`, tree `7589415dd1c3ab6957686a6d7f20c47a62c45ba2`. Source base `e8454e2751d05b02ee8e5a571857589ab358ab86`.
- **Diff examined.** 11 commits, 12 files, +1,335 / -336.
- **Scope.**
  - The #671 body: Required, and Acceptance 1 to 3.
  - The assignment, issuecomment-6098494890: the media-fault rule of `sw/firmware/ctrl_nvm/README.md` Boot items 3 and 9 applied to the shipping writer, with the A/B guarantee, record format, register map and boot budget unchanged.
  - The round-2 assignment, issuecomment-6100704879. Its item 1: "the read-fault check must be able to fail for every mechanism the fix depends on".
- **Lenses.** Conformance, RTL, Robustness, Tests and Docs were each applied independently at this head.
- **Order.** The verdict and the ledger were fixed before any prior-round review text was read. The prior findings were then resolved against this head (section "Prior public findings").

## Verdict

**NEGATIVE on one MAJOR (R603-2-F1: Conformance, Tests).**

What holds at this head:

- The firmware is correct on every path I drove, including the one F1 names.
- Acceptance 1 is met in the firmware host tests for the cold boot.
- Acceptance 3 holds.
- Every round-1 finding is resolved.

What fails is part of Acceptance 2, together with round-2 item 1:

- The PR adds the writer hold at two call sites, the cold boot and the writer restart without a fabric reset (re-attach).
- A plant that restores restart-at-zero on the re-attach path alone reddens no gate. Checks 1 to 14 stay green on three shapes, and nvm_cosim has no read-fault model.
- I drove that plant through a restart under a boot read fault. It reproduces #671's loss exactly.

## Findings

### R603-2-F1 MAJOR - Conformance, Tests - restart-at-zero can return on the writer-restart (re-attach) path and no gate fails

- **Where.**
  - `sw/firmware/milan_baremetal/milan_baremetal.c:1698`: the re-attach branch's `nvm_go_live()`. This is one of the two call sites this PR introduced; the other is `:1734`.
  - `sw/firmware/nvm_hosttest/read_fault_cases.py:21`: `restart_at_zero` plants inside `nvm_go_live()` itself, so it removes the hold on both paths at once and cannot tell them apart.
  - `sw/firmware/nvm_hosttest/test_nvm_firmware.py:727` (`grade_fault_case`) and `:168` (`RETIRE_CAUSES`) boot only the cold path and the four retire paths.
  - `sw/firmware/nvm_hosttest/nvm_host.c:847` (`--boot-backend contract|over|live`) has no "load pending 0, load accepted 1" state, and the host suite has no CPU-only restart.
  - `tb/verilator/nvm_cosim` models the restart (W1 to W4) but no read fault. With `nvm_unread` 0, `nvm_go_live()` is exactly `nvm_ready = 1`, so the suite cannot see this by construction.
- **Authority.**
  - #671 Acceptance 2: "A planted control that restores the restart-at-zero behaviour must fail."
  - Round-2 assignment item 1, quoted above. The PR body says it is met ("Check 13 can now fail for every mechanism the fix depends on").
  - `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:715-726`: a writer restart without a fabric reset "re-derives the authoritative slot and the sequence from the media". That is the second place the shipping path derives the generation.
  - AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect."
- **Evidence.**
  - **Full suite stays green.** Probe `p_reattach_goes_live` (`scripts/probe_mutants.py`) replaces that one `nvm_go_live();` with `nvm_ready = 1;`. With `--all-grades` (checks 1 to 14 in full) it SURVIVES on `endstation_arty_4x4`, `endstation_ax7101_1x1_tdm8` and `endstation_ax7101_8x8` (`receipts/probe_reattach_mutant_allgrades.log`, rc 0).
  - **The restart under a fault.** `scripts/probe_reattach.py` (`receipts/probe_reattach_1x1.log`, rc 0, "every expectation met") gives a scratch copy of the harness a restart hook. It reuses `run_cases.host_restart()` from the PR's own cosim: every writer static is reset, then `nvm_boot()` runs again with the fabric model kept. Nothing in the tree is modified. The scenario:
    - slot A blank, slot B valid at 0x5A5A5, and a clean cold boot;
    - slot B's magic byte faulted on the restart's three judgement reads, each with different bytes;
    - the restart, a real change, a 3 s idle, then a clean reboot.
  - Results at the 1x1 product shape:
    - **Head:** "slot B gave no standing verdict in 3 reads ... HELD until reset". The run ends with erases 0, programs 0, acks 0, dirty 1 and backed 0. Persistence was refused and reported, as #671 requires.
    - **Mutant:** "commit (dirty) seq 1 -> slot A ... acknowledged". The clean reboot reads "slot A VD_OK seq 1, slot B VD_OK seq 370085; offered B seq 370085", so the change was LOST. This is #671's defect, and nothing reddens.
    - **No-fault control:** both firmwares commit seq 0x5A5A6 to A and the change survives, so the scenario itself is sound.
- **Impact.** One changed line can regress and bring #671's silent loss of a committed change back after any CPU-only reset that meets a boot read fault, while the shipping gate stays green. Acceptance 2 is demonstrated for the cold boot only.
- **Required outcome.**
  - The read-fault gate boots the re-attach path under a read fault that leaves a slot UNREAD.
  - That boot must hold: no erase, program or acknowledgement, and the change survives the clean reboot or persistence was refused.
  - A planted control that removes the hold on the re-attach path alone (the probe's text or an equivalent) reddens with a named finding on the first shape and both product shapes.
  - The PR body's "every mechanism" sentence is then true.
- **Verification.**
  - `python3 -I scripts/probe_mutants.py <root> --all-grades --only p_reattach_goes_live --shapes endstation_arty_4x4,endstation_ax7101_1x1_tdm8,endstation_ax7101_8x8` prints CAUGHT on each line.
  - `test_nvm_firmware.py --self-test` reports the new control "caught by N named finding(s)" on three shapes.
  - `scripts/probe_reattach.py` still shows the head holding.

### R603-2-R1 RESIDUE - Docs - the contract page's writer-restart bullet omits the hold

- `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:719-726` says the re-attaching writer "re-derives the authoritative slot and the sequence from the media, publishes them and resumes service."
- At this head, a re-derivation that leaves a slot UNREAD publishes and then HOLDS (`milan_baremetal.c:1696-1698`). The hold rule is already stated generally in FASTCONNECT section 7 (`SAVED_STATE_FASTCONNECT.md:781-800`) and in `BAREMETAL_FIRMWARE.md:2015-2051`. This is prose only: no figure, test, code, verdict or clause claim changes.
- **Exact fix:** replace "publishes them and resumes service." with "publishes them and resumes service, unless a slot gives no standing verdict in that re-derivation: the writer then publishes and HOLDS until reset, as on a cold boot ([#671](https://github.com/kebag-logic/milan-fpga/issues/671))."

### R603-2-S1 SUGGESTION - Tests - pin the per-slot read bound, not only the boot total

- `read_fault_cases.py:92` (`BOOT_READ_BOUND = 1 + 4 * READ_TRIES`) and `test_nvm_firmware.py:740` bound only the boot's total.
- Probe `p_judge_four_tries` (four judgement reads instead of `NVM_READ_TRIES` = 3) SURVIVES checks 13 and 14 on 1x1 (`receipts/probe_mutants_1x1_rest.log`). The fault model faults one slot, so no case comes near 13 reads.
- #671's "within a bound" still holds, but the documented "at most three reads" could drift silently.
- Suggestion: the `(0, 64)` whole-boot case with the other slot blank asserts its exact read count, 1 + 3 + 2.

### R603-2-S2 SUGGESTION - Robustness - console wording on a held re-attach

- `milan_baremetal.c:1698-1699`: a held re-attach prints the HELD line and then "writer restarted on a live backend; re-attached, the window is not reloaded." (`receipts/probe_reattach_1x1.log`, head/fault).
- Suggestion: print "re-attached and HELD", or drop "re-attached", when `nvm_held` is set. Console text only; the state is right.

### Out-of-scope observation (recommend a new Issue; not a finding against this head)

- **OBS-1.** `nvm_prefill_stage()` (`milan_baremetal.c:1245-1255`, unchanged by this PR) re-reads the authoritative slot from flash, one mapping read per byte, at every capture. A record the backend reports OPEN keeps those bytes.
- `scripts/probe_prefill_ff.py` (`receipts/probe_prefill_ff_1x1.log`): the prefill's 3,336 reads are answered with slot A as all `0xFF`, which is check 13's own fault mode. The open record is committed as an erased record, which the section 6.1 erased-record rule accepts. The clean reboot then "restored nothing (erased record)" for it, so its saved value is silently lost. The no-fault control keeps it.
- This is a runtime fault on a path #671 does not cover, it involves no generation, and the code predates the lane. It is recorded here only so it can become its own Issue.

## Prior public findings, resolved or retained at this head

| Finding (round 1, head f54dbe3e) | Status at 9112a0df | Evidence |
|---|---|---|
| R603-1-F1 MAJOR, Tests: no record-area faults, no both-valid layouts, three plants green | RESOLVED | `read_fault_cases.py:127-158` faults a record-area byte (`body`) and both-valid layouts in both orientations at 0x5A5A5 and across the wrap at 0. `r_digest_header_only`, `r_fill_from_flash` and `r_restage_fail_offers_none` are standing controls, each caught by its own words on three shapes (`receipts/hosttest_selftest_head.log`). The texts match the round-1 descriptions. |
| R603-1-F2 MINOR, Docs and RTL: worst case assumed container-length reads | RESOLVED | The PR body states ten slot-length reads plus two container reads, about 16.4 s (1x1) and 17.1 s (8x8), labelled an ESTIMATE, with the writer-restart note. This matches my read count from `nvm_judge_slot`/`nvm_restage` (`:781-825`). The per-byte cost is the author's measurement, not re-measured here. |
| R603-1-R1 RESIDUE: check numbering | RESOLVED | The README now numbers items 12 to 14 and says "fourteen checks", matching `test_nvm_firmware.py:45-63`. |
| R603-1-S1: wipe while held | RESOLVED | Documented at `milan_baremetal.c:1576-1578`, `BAREMETAL_FIRMWARE.md` Boot and the host README. Checked by `grade_hold_console` (`test_nvm_firmware.py:820-824`). |
| R603-1-S2: console names the slot on retire paths | RESOLVED | `nvm_held` (`:477`) is set only in `nvm_go_live()`. All four retire causes are checked (`test_nvm_firmware.py:825-830`). |
| R603-1-S3: re-stage sequence check unexercised | RESOLVED | `--read-other` plus control `r_restage_any_seq`, caught on three shapes. |
| R602-1-F1 MINOR, Docs and Robustness: worst case omits length-word faults | RESOLVED | Same evidence as R603-1-F2. |
| R602-1-R1 RESIDUE: FASTCONNECT loss mode per store | RESOLVED | `SAVED_STATE_FASTCONNECT.md:785-787` carries the exact text. |
| R602-1-R2 RESIDUE: numbering | RESOLVED | As R603-1-R1. |
| R602-1-R3 RESIDUE: SNAPSHOT_OWNERSHIP section 18 "boot path only" | RESOLVED | The exact text is at `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1651`. |
| R602-1-R4 RESIDUE: all-0xFF sentence | RESOLVED | The host README carries "A single all-`0xFF` read of the valid slot is walked over SKIP 0 to 5." |
| R602-1-S1: read-fault count | RESOLVED | Documented as a floor (`milan_baremetal.c:478-481`). |
| R602-1-S2: only the changed record graded; no both-valid layouts | RESOLVED | `reboot_findings` requires `lost == 0` for every other saved record (`test_nvm_firmware.py:705-711`), and both-valid layouts are present. |
| R602-1-S3: wipe in BAREMETAL | RESOLVED | `BAREMETAL_FIRMWARE.md`, Boot paragraph. |

No prior finding is retained. F1, R1, S1, S2 and OBS-1 are new at this head.

## Lens results

Each line names what was examined at this exact head.

- **Conformance: UNCLEAN** (F1). Also examined and clean:
  - `milan_baremetal.c:366,641-654,737-825,1480-1488,1536-1544,1564-1591,1647-1770,1980-1987` against #671 Required and the `ctrl_nvm/README.md` Boot items 3, 4 and 9. Refusal and blank stand only on two equal-byte reads within three. OK stands on one read, then a re-stage under its picked sequence. No sequence is taken from a refused or unread slot (the sequence is set only on `VD_OK`, `:757-758`). UNREAD holds. The wrap-safe pick and the tie are unchanged.
  - Acceptance 1, cold boot: met (head self-test: 446 cases per shape, both orientations, SEQ 1, 0x5A5A5, 0x80000000, 0xFFFFFFFF and the wrap).
  - Acceptance 3: met (the A/B write path, `nvm_commit()` `:1381-1446`, is unchanged; checks 1 to 12 green on 5 shapes; nvm_cosim 465/465).
  - The processor half of Acceptance 1 does not apply: `KL_nvm_backend.sv:424,439,482,490,582` only stores and reads back SEQ, and `KL_aecp_nvm_writer.sv`, `KL_pp_nvm_port.sv`, `KL_pp_nvm_mgr_arb.sv` and `KL_acmp_nvm_shadow.sv` at `2ad2f845` contain no sequence or generation identifier.
- **[R603] PASS RTL - `milan_baremetal.c:366,407-415,470-482,641-825,1536-1544,1581-1591,1619-1770`; `hdl/milan/KL_nvm_backend.sv:424-582` (no HDL diff).**
  - Stage writes are bounded by `NVM_SLOT_BYTES` under the static assert `NVM_SLOT_BYTES <= MILAN_NVM_IMAGE_MAX` (`:415`).
  - An accepted container is exactly `NVM_IMG_LEN`, so the window fill copies only re-staged bytes and no stale tail.
  - Each re-stage failure removes a slot, so the fallback loop ends within two passes.
  - The `uint32` sequence uses an `int32` wrap compare.
  - Every boot path's writer state was traced: live, held, retired and disabled.
  - There is no register-map or record-format change.
- **[R603] PASS Robustness - `receipts/hosttest_selftest_head.log` (446 fault cases per shape, 5 shapes); `receipts/probe_reattach_1x1.log` (head holds on a faulted re-attach); `receipts/probe_mutants_1x1_rest.log`.**
  - Faults are covered on the header, sequence word and record area, as all-0xFF reads, and as an other-slot address fault on the re-stage. They are walked over every boot read, including a fault for the whole boot.
  - One faulty read never holds; a whole-boot fault always holds. The bound is reached by the unbounded-retry control. The console cause is right on all four retire paths. Reset during activity was checked through my re-attach probe.
  - The stated detection limits (same wrong bytes twice, all-0xFF twice, an other-slot judgement read) were checked against the code and are disclosed in both READMEs and FASTCONNECT 7.
- **Tests: UNCLEAN** (F1). Also examined and clean:
  - The nine #671 controls, each caught by its own words on three shapes (head self-test).
  - Nine of my eleven 1x1 plants, plus `p_reattach_goes_live` on three shapes, were graded by checks 13 and 14:
    - caught: `p_cold_goes_live`, `p_no_second_agreement`, `p_restage_one_try`, `p_held_heartbeats`, `p_blank_on_one_read`, `p_refusal_on_one_read`, `p_hold_only_both`, `p_restage_skipped`, `p_judge_not_unread`;
    - survived: `p_judge_four_tries` (S1), `p_agree_ignores_count` (judged equivalent in effect), and `p_reattach_goes_live` (F1).
  - The base firmware graded by this head's checks 13 and 14 gives 645 findings, 124 of them "was lost on the clean reboot" (`receipts/probe_base_firmware_1x1.log`), matching the author's figure.
  - `run_cases.py:181-186` names the three new statics.
- **[R603] PASS Docs - `SAVED_STATE_FASTCONNECT.md:781-800`; `BAREMETAL_FIRMWARE.md:2015-2051,2154-2165`; `sw/firmware/nvm_hosttest/README.md:11-12,46-56,89-165,203-215`; `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1616-1666,1808-1820` against `tb/verilator/nvm_capture_cpu/measurements.json`.**
  - Every capture figure equals the receipt: 8x8 13.86328 ms, 3.5345x, margin 10.63672 ms; 1x1 3.96548 ms, 12.3566x; all six arms' minima and maxima.
  - The receipt binds the head firmware's SHA-256 `33eaa0c3...` and the head's capture gate PASSES.
  - The loss modes per store, the bound of twelve slot reads, the hold, the wipe exception and the retire causes all match the code. `docs_check.py` reports 0 findings, and no em-dash appears in added lines.
  - One RESIDUE (R1) is carried; it does not unclean the lens.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #671 body, assignment and round-2 assignment; `ctrl_nvm/README.md` Boot 3, 4 and 9; `milan_baremetal.c:366-825,1480-1770,1980-1987`; `KL_nvm_backend.sv:424-582`; processor NVM files at `2ad2f845`; head self-test; probe_reattach | R603-2 | 9112a0df27acc1381091845e94d8eaa1407f1bbb |
| RTL | CLEAN | `milan_baremetal.c:366,407-415,470-482,641-825,1536-1544,1581-1591,1619-1770`; `KL_nvm_backend.sv:424-582` | R603-2 | 9112a0df27acc1381091845e94d8eaa1407f1bbb |
| Robustness | CLEAN | `read_fault_cases.py:18-215`; `nvm_host.c:161-200,522-585,847-858`; hosttest_selftest_head.log; probe_reattach_1x1.log; probe_mutants_1x1_rest.log | R603-2 | 9112a0df27acc1381091845e94d8eaa1407f1bbb |
| Tests | UNCLEAN (F1) | `test_nvm_firmware.py:160-182,622-939`; `read_fault_cases.py`; `nvm_host.c`; `run_cases.py:181-186`; head self-test; nvm_cosim; probe_mutants (12 plants); probe_reattach; probe_base_firmware | R603-2 | 9112a0df27acc1381091845e94d8eaa1407f1bbb |
| Docs | CLEAN (RESIDUE R1 carried) | `SAVED_STATE_FASTCONNECT.md:781-800`; `BAREMETAL_FIRMWARE.md:2015-2051,2154-2165`; host README; `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:715-726,1616-1666,1808-1820`; measurements.json; check_nvm_capture; docs_check | R603-2 | 9112a0df27acc1381091845e94d8eaa1407f1bbb |

## Executed evidence (this round, at the exact head, in a scratch clone)

Every row below ran at `9112a0df` with submodules at their gitlinks. The rc files are beside each log.

| Command | Result |
|---|---|
| `python3 -B sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test --jobs 6` | rc 0, "OK across 5 shape(s), and every planted defect reddened"; nine #671 controls caught on three shapes; 3:20 wall time with nvm_cosim running beside it |
| `make -C tb/verilator/nvm_cosim run JOBS=6 POOL=6` (pinned Verilator 5.050) | rc 0, "465 checks: 465 PASS, 0 FAIL", "39 of 39 mutant(s) killed"; 7:14 wall time |
| `python3 -B scripts/check_nvm_capture.py` | rc 0, "PASS: capture census, clocks, both timing arms and receipt agree" |
| `python3 -B scripts/docs_check.py` | rc 0, 0 findings across 202 md files |
| `scripts/probe_mutants.py` (12 plants; `--all-grades` for F1's plant on 3 shapes) | as listed under Tests. `probe_mutants_1x1.log` (rc 1) is the first attempt, ended by a probe compile error in `p_no_second_agreement`; `probe_mutants_1x1_rest.log` re-ran it and the remaining plants |
| `scripts/probe_reattach.py` | rc 0; head holds, the mutant loses the change, both controls survive |
| `scripts/probe_base_firmware.py` (base `e8454e27`) | rc 0; 645 findings, 124 "was lost" |
| `scripts/probe_prefill_ff.py` | rc 0; OBS-1 |
| hosted checks at the head (`receipts/hosted_checks_head.tsv`, sampled 22:39Z) | 13 success, 1 skipped ("Physical gPTP (nightly and manual)", which is not executed evidence), 8 still in progress: docs-check, elaborate, firmware-unit, and Verilator shards 0, 1, 2 and 4. None is judged here. |

- **Clone integrity.** After all probes the review clone is unchanged (`receipts/clone_integrity.txt`): HEAD and tree are exact, the porcelain status is empty, and the index is byte-identical to the pre-review snapshot. All 1,271 tracked blobs match by hash and mode, and the five gitlinks and submodule states match.
- **Probe isolation.** Every probe planted into in-memory or scratch copies under `scratch/`. No tracked file was edited anywhere.

## Real limits

- The builder bank (`test_builder.py --require-rv32`, gate 11, the compiled store census of the new stage loop) and the record-space gate were not run: they are excluded from this round. The author's receipts stand for them.
- `fw_service_budget` was not run. The boot worst case (16.4 s and 17.1 s) and the 24.5 µs/B refused-read cost are the author's measurements and estimate, not reproduced here. The firmware size delta (+1,712 B text) was not rebuilt.
- The renderer-based docs gates (Contents walk, em-dash through the renderer) were not run, because their Python packages are not installed and no install was made. The plain-text `docs_check.py` ran.
- The host model counts one read per evaluation of the mapping's base. It does not model faults inside one read's span that change mid-read, physical QSPI behaviour, or interrupted-erase cells. Physical calibration was NOT RUN, and no hardware proof is claimed.
- The round-1 reviewer plant texts were compared with their published descriptions, not byte for byte with the round-1 scripts.
- The local Python is 3.14.7 and the author's is 3.12.3. The host build uses the system gcc 16.2.1.

## Pending manager duties

- Hosted and act acceptance of the exact head. Eight hosted contexts were still running at the last sample.
- The current-dev merge candidate (source base `e8454e27`, live dev `1fb0ed9a`) with its builder and native banks.
- RESIDUE R603-2-R1 goes to the residue checklist with its exact text.
- File OBS-1 (prefill read fault drops an open record's saved value) as a new Issue if the maintainer agrees.
- Re-review after F1 is answered. Coverage for Conformance and Tests must be re-banked at the new head, along with any lens whose artifacts the answer touches.

R603-2 FINISHED
