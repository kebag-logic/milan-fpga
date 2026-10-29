[R737] POSITIVE - exact head ee1c0be0b99f0131eb10908a19f080299aa0cbb8

# R737-1: internal independent review of PR #812 (issue #665, S4)

- PR #812, `665-s4-f1-target` into `dev-soft-core`. Exact head `ee1c0be0b99f0131eb10908a19f080299aa0cbb8`, tree `48581b5296086a3ba87d35b76d6e986ad9a15dc3`. Source base `f4c9ad4f`.
- Whole PR, 7 commits. The packet holds both author rounds: round 1, which ended in the STOP, and round 2 under the owner's option (c).
- Reviewer role: internal, cleared context, own detached clone.
- Verdict: **POSITIVE**. No BLOCKER, MAJOR or MINOR is open. There is one RESIDUE (wording) and four SUGGESTIONs. All five lenses are covered clean at this head.

## 1. What the task is, rebuilt from public state

The authorities, read in this order:
1. AGENTS.md and CONTRIBUTING.md (sections 2, 3, 5 and 6).
2. docs/README.md.
3. The issue #665 body.
4. The S4 assignment (issuecomment-6493622258), with its scope, acceptance and shared-file note.
5. The STOP (issuecomment-6500265323).
6. The owner's option (c) of 2026-10-29 19:05 (issuecomment-6504551000), and its round-2 assignment.
7. The T_svc approval (issuecomment-6495692075): 20 ms, graded per family as `min(T_svc, ceiling)`.
8. FR_NFR.md 3.4.1 and NFR-SCOUT-03.
9. ARCHITECTURE_HW_SW_SPLIT.md sections 2, 5 and 6.
10. sw/firmware/ctrl_nvm/README.md ("The flash port", "Boot", "Write-back", "The service bound").
11. tb/verilator/nvm_capture_cpu/README.md and scripts/check_nvm_capture.py, which hold D5 on the current writer.

The frozen acceptance as option (c) restates it:
- F1 is not held to D5's 24.5 ms capture bound.
- Each F1 step is held to T_svc.
- The capture's CPU time and elapsed time are measured and recorded, with no bound of their own.
- D5's 24.5 ms stays on the current flash writer in `check_nvm_capture.py`.
- Planted defects: a step over T_svc must fail, and removing the current writer's 24.5 ms check must fail.
- Boot works with valid, absent, torn and wrong-version slots.
- `nvm_cosim` and `nvm_capture_cpu` pass.
- D3's apply order holds.
- The guard refuses every program or erase outside the journal.
- The port is generated from the split SoC's `csr.csv`.

Diff reviewed: `git diff f4c9ad4f..ee1c0be0`, 17 files, +2560/-132. Every hunk was read, plus the commit history.

## 2. What this review executed independently, at the exact head

The scoped Verilator 5.050 was checked for identity before use. Make parallelism was capped so at most 16 jobs ran at once.

| Run | Result | Receipt |
|---|---|---|
| `gen_flash_port.py --self-test` | rc 0, 33 checks, 0 failures | `receipts/gen_flash_port_selftest.log` |
| `nvm_split_target/run.py --self-test` | rc 0, 41 checks, 12 mutants caught | `receipts/nvm_target_selftest.log` |
| `ctrl_service_budget/run.py --self-test` | rc 0, 0 failures | `receipts/budget_selftest.log` |
| `nvm_split_target/run.py --point 1x1`, fresh build | rc 0. Every case passes and every control is caught. `table.md` and `results.json` are **byte-identical** to the author's published receipts (sha256 `a6d21e1f...`). | `receipts/target-1x1/` |
| `nvm_split_target/run.py --point 8x8`, fresh build | rc 0. Every case passes and every control is caught. `table.md` and `results.json` are **byte-identical** to the author's. | `receipts/target-8x8/` |
| Probe: `split_soc.map_deviations` on the reviewer's 1x1 test-SoC `csr.csv` | Empty as built. All 30 plants refused: each of the 9 port registers moved one word, and each removed; the window moved, resized, mapped twice and absent. | `scripts/probe_map_deviations.py`, `receipts/probe_map_deviations_1x1.log` |
| Probe: the guard off by one at the journal's end (`... <= SIZE - len + 1u`), guard-probe arm, `guard` case | **Caught**: `testbench: FAIL: flash write escaped the journal`, and the loop never ran | `scripts/probe_guard_mutant.py`, `receipts/probe-guard/` |
| Probe: the store skips the binding walk; the store skips the D3 walk (`valid` case) | Both **caught**. Binding walk: `apply order: entry 0 is aecp_map_restore ...` and `sink 0's talker is 0`. D3 walk: `apply order: entry 2 is absent ...` and the entity_name answered is the default. | `scripts/probe_restore_mutants.py`, `receipts/probe-restore/` |
| Probe: `check_nvm_capture.py`, unplanted, then with its 24.5 ms check deleted from `nvm_capture_cpu/run.py` `grade_rows` (disposable export of the head) | Unplanted rc 0. Planted rc 1, `FAIL: OFF timing limit was ignored`. The file was restored with its digest checked. | `scripts/probe_d5_removed.sh`, `receipts/d5_*` |
| Disassembly of the reviewer's linked 1x1 image | The port reaches the master at `lui 0xf0003` with offset -2024, which is `0xf0002818` (rxtx). It reaches timer0 at `0xf0003000` and the window at `0x0100_0000`. Those are the generated map's addresses, not the stand-ins' (`0xf000_3000`, `0xf000_3800`, `0x2000_0000`). | `receipts/elf_flash_port_addresses_1x1.txt` |
| `docs_check.py`, `gen_toc.py --check`, `check_em_dash.py --base f4c9ad4f`, `check_py_idiom.py`, `check_cpp_idiom.py` | All rc 0 | `receipts/*.log` |
| `git merge-tree` of this head with S2b's head `f884c7e9` | Textual conflicts in 3 files (section 3, item 6) | `receipts/merge_tree_s4_s2b.txt` |

## 3. Focus checks

**(1) The port compiles against the split SoC's own map, and the harness refuses any other placement. Holds.**
- How the map is made:
  - `build.flash_map` (build.py:242) exports `milan_soc.py --ctrl-mailbox --ctrl-firmware` for the shape's config.
  - `gen_flash_port.py` writes `generated/csr.h` and `generated/mem.h` from that export's `csr.csv`. It takes field offsets from LiteX's `csr.h` and cross-checks every address.
  - Its 8 rules are each planted in its self-test, and each plant is refused by its own rule and by no other.
- `ctrl_srp_image.py:55` puts the map ahead of the RV32 stand-ins. It refuses a map whose clock differs from the shape's.
- The ELF disassembly proves the image uses the generated addresses.
- The image-independence check (build.py:252) confirms the second export yields the same map.
- `split_soc.py:477` refuses a test SoC whose `csr.csv` places any port register or the window elsewhere. The probe shows that refusal firing on 30/30 plants.
- The 1x1 and 8x8 maps are equal (`receipts/flash_port_*.json`). The journal is `0xee0000`+`0x20000`. timer0's clock is 100 MHz.

**(2) Boot with valid, absent, torn and wrong-version slots, answered from the real owners, in D3's order. Holds at both points.**
- `held_to` (target_grade.py:294) reads the ENTITY descriptor's `entity_name` at frame bytes 90..154. It reads GET_RX_STATE_RESPONSE's talker at byte 34 and its sequence_id at byte 62.
- These offsets were checked against the IEEE 1722.1-2021 7.2.1 descriptor layout and the 8.2.1 ACMPDU layout.
- The torn and version journals come from the target's own commit through the reference codec. The self-test checks their verdicts: torn slot B is refused beside a valid slot A, and the version slot is refused with `VD_VER`.
- Both planted reorders (`reorder-settle`, `reorder-bindings`) are caught. So are the reviewer's two skipped-walk plants.
- One caveat on the version case: on the target it grades behaviour only (nothing applied, defaults answered), not the firmware's verdict code. The host suite owns the verdicts.

**(3) The guard refuses every program or erase outside the journal on the target, and the model catches an escape. Holds.**
- The `guard` case's probe (target_cases.py:60) makes 4 erases and 3 programs outside the journal and 1 erase inside it.
- The device sees only the inside erase.
- With `guard-removed`, the flash model (fw_service_budget/flash.hpp:75, a fixed window independent of firmware) throws `flash write escaped the journal`.
- The reviewer's end-boundary off-by-one is caught too.
- `ls_program` enforces page alignment and `ls_erase` enforces block alignment (nvm_flash_litespi.c:200-228), so a call straddling a 64 KiB journal boundary cannot occur. The probe's set is therefore complete for the boundaries.

**(4) Option (c). Holds.**
- Every service step, in every phase and every case, is graded against `scenario.T_SVC_MS` (target_grade.py:149). That is 10 ms at this base, under every `min(20 ms, ceiling)` family bound; the smallest is SRP's 18 ms.
- `slow-step` (a real 30 ms first step) is caught at both points, as 30.2216 ms and 30.2139 ms.
- `step-over-t-svc` is caught in all 7 phases at 500,000 cycles.
- The capture is recorded with no bound:
  - 1x1: 27.223 ms CPU, 534.905 ms elapsed.
  - 8x8: 103.227 ms CPU, 1,638.061 ms elapsed.
  - These match the owner's 0.53 s and 1.64 s.
- `check_nvm_capture.py` and `nvm_capture_cpu`'s `.py`, `.cpp` and `measurements.json` are unchanged. The removal plant fails the hosted gate (reviewer probe), and also the self-test mutant.
- No report presents 24.5 ms as F1's bound:
  - the run's table is checked for it in the self-test (`report_checks`);
  - every doc mention of 24.5 ms in the diff assigns it to the current writer;
  - the plan restatement receipt agrees.

**(5) Clocks. Holds, with one wording residue.**
- `build.json` at both points records `cpu_hz` 50,000,000 and `sys_hz` 100,000,000 (`receipts/build_clocks.txt`).
- `slow-step` cross-checks the two clocks: 30 ms of timer0 time at 100 MHz measures 30.22 ms of CPU cycles at 50 MHz.
- The nvm_split_target README (line 5) and ctrl_nvm/README.md:343 state 50 MHz.
- ARCHITECTURE_HW_SW_SPLIT.md:223 does not (R737-1-R1).
- The generated table and results.json carry no clock (R737-1-S1).

**(6) Files shared with S2b. Holds at this head; merge-turn work is pending.**
- S4 keeps S2b's contract where both touch:
  - the image's placeholder mailbox stays the fixture's;
  - `ctrl_srp_image.py` adds `--nvm-source` and `--flash-map` without changing the flags;
  - the S2 grader ignores the new SPAN and CALL lines (grade.py:158).
- S2b's change to `nvm_flash_litespi.c` (the clock conversion) touches neither the guard lines nor `nvm_store.c`, so S4's plant anchors survive it.
- `git merge-tree` shows textual conflicts in `ctrl_srp_image.py`, `split_soc.py` and the S2 README:
  - In `ctrl_srp_image.py`: S2b's `layout_flags` against S4's `nvm` include.
  - In `split_soc.py`: S2b's record mover `mbx_dma` and stand-in master against S4's generated map and `spiflash` bank.
- These need a semantic resolution at the merge candidate (section 8).

## 4. Findings

**R737-1-R1: RESIDUE. Lens: Docs.**
- Where: `docs/ARCHITECTURE_HW_SW_SPLIT.md:223`. A capture figure is given without its CPU clock.
- Evidence: focus item (5). The same figures state 50 MHz everywhere else (ctrl_nvm/README.md:343, nvm_split_target/README.md:5).
- Impact: wording only. No figure changes. A reader of this page alone cannot tell the clock.
- Exact fix: replace `At 8x8 it takes 103.2 ms of CPU time over 1.64 s elapsed.` with `At 8x8, on the split CPU at 50 MHz, it takes 103.2 ms of CPU time over 1.64 s elapsed.`
- Verification: docs gates rc 0.

**R737-1-S1: SUGGESTION. Lenses: Tests, Docs.**
- Where: `tb/verilator/nvm_split_target/run.py:118-142` (`table`) and `results.json`. The generated receipts do not state the clocks their milliseconds were computed at.
- Evidence: `ms()` uses `spec['cpu_hz']`. Only `build.json`, in the build directory, records the clocks, and it is not among the receipts.
- Impact: none on a verdict. A receipt read alone does not carry its CPU clock.
- Suggested: write `cpu_hz` and `sys_hz` into `results.json`, and the CPU clock into the table's T_svc line.
- Verification: the self-test's `report_checks` asserts the clock appears.

**R737-1-S2: SUGGESTION. Lenses: Tests, Robustness.**
- Where: `tb/verilator/ctrl_service_budget/split_soc.py:96` (`map_deviations`) and `sw/firmware/ctrl/test/ctrl_srp_image.py:55` (the flash map's clock refusal). Neither refusal has a committed negative control.
- Evidence: the S2 harness's self-test exercises neither. The reviewer probe shows `map_deviations` refuses all 30 planted placements.
- Impact: none today. A later edit could weaken either refusal unseen. The existing `ack_deviations` has the same gap.
- Suggested: add self-test checks with a moved register, a moved window and a mismatched map clock.
- Verification: a mutant that returns `[]` must fail the self-test.

**R737-1-S3: SUGGESTION. Lens: Robustness.**
- Where: `sw/firmware/ctrl_nvm/plat/gen_flash_port.py:246`. A zero-size `spiflash` memory region raises `ZeroDivisionError` instead of a named refusal.
- Evidence: `receipts/probe_gen_zero_window.log`. The run ends in a traceback with exit 1, and nothing is written.
- Impact: no unsafe outcome. The refusal is unnamed, and LiteX never emits a zero-size region.
- Suggested: `if size and base % size`, or refuse a zero size by name, with a plant.
- Verification: the self-test plant is refused by the rule `flash window`.

**R737-1-S4: SUGGESTION. Lens: Tests.**
- Where: `.github/workflows/`. The new `nvm_split_target` self-test and `gen_flash_port.py --self-test` run in no hosted workflow.
- Evidence: the author disclosed this. The S2 harness's self-test has the same placement. The hosted guard on D5, `check_nvm_capture.py` (docs.yml:334), is unchanged, and the reviewer probe shows it fails on the removal.
- Impact: these portable self-tests can rot between lane runs.
- Suggested: a follow-up Issue to run the portable harness self-tests in the docs workflow, with `ci_events` updated.
- Verification: a hosted step that runs both.

**Prior public review findings on PR #812:** none. The PR thread holds only the two review-start notices, and there are no review objects or review comments. Nothing needed resolving or retaining.

## 5. Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | <ul><li>Issue #665 S4 acceptance (6493622258) and option (c) (6504551000), against `target_grade.py:149-197,294-379`, `target_cases.py:131-142`, `run.py:85-152`</li><li>The reviewer's fresh 1x1 and 8x8 runs, byte-identical to the receipts</li><li>D5 probe on `check_nvm_capture.py`</li><li>`held_to` offsets against IEEE 1722.1-2021 7.2.1 and 8.2.1</li><li>FR_NFR 3.4.1 and the T_svc approval (6495692075) against `scenario.T_SVC_MS`, `CEILING_MS`</li></ul> | R737-1 | `ee1c0be0b99f0131eb10908a19f080299aa0cbb8` |
| RTL | CLEAN | <ul><li>Diff name list: no `.sv`/`.v`/`hdl/`/`sw/litex/` file and no gitlink changed</li><li>Test-SoC glue `split_soc.py:96-109,331-376` (LiteSPI `with_master=True` in one `spiflash` bank, PHY CSRs, bank alignment)</li><li>Clocks in `build.json` (CPU 50 MHz, bus 100 MHz) and `flash_port.json` (timer0 at 100 MHz)</li><li>`gen_flash_port.py:174-303` width, field and overlap rules</li><li>`sim_main.cpp:326` return detection on an RV32I image (`-march=rv32i`, every call 4 bytes)</li><li>`flash.hpp:75` journal window</li><li>ELF disassembly of the port's addresses</li></ul> | R737-1 | `ee1c0be0b99f0131eb10908a19f080299aa0cbb8` |
| Robustness | CLEAN | <ul><li>Malformed inputs: `gen_flash_port.py` reader and rules, with the zero-window probe (S3 only)</li><li>Torn, wrong-version, absent and valid journals (`target_cases.py:218-237`)</li><li>Guard boundaries (`nvm_flash_litespi.c:178-228`) with the end off-by-one probe</li><li>`map_deviations` 30-plant probe</li><li>Skipped-walk plants</li><li>T_svc at and one cycle past it, per phase</li><li>The reference codec's slot verdicts</li></ul> | R737-1 | `ee1c0be0b99f0131eb10908a19f080299aa0cbb8` |
| Tests | CLEAN | <ul><li>`target_selftest.py`, 41 checks and 12 mutants, re-run rc 0</li><li>`gen_flash_port.py` self-test, 33 checks, re-run rc 0</li><li>The S2 self-test re-run rc 0</li><li>Each control's ability to fail, shown by the reviewer's own plants (guard end, two skipped walks, D5 removal) on real builds</li><li>Determinism: a fresh build reproduced every cycle count</li></ul> | R737-1 | `ee1c0be0b99f0131eb10908a19f080299aa0cbb8` |
| Docs | CLEAN (R1 is RESIDUE) | <ul><li>`ctrl_nvm/README.md:7-16,63-67,318-360,517-544`</li><li>`ARCHITECTURE_HW_SW_SPLIT.md:163-176,217-224,260-264`</li><li>`nvm_split_target/README.md` (whole page; its figures checked against the reviewer's runs)</li><li>`ctrl_service_budget/README.md` hunks, `nvm_capture_cpu/README.md:9-10`</li><li>Docs, TOC, em-dash and idiom gates rc 0</li><li>Comment rule: no lane label, round, reviewer ID or comment ID in an added source comment. F1, D3, D5 and DR2a are design identifiers, as at the base.</li></ul> | R737-1 | `ee1c0be0b99f0131eb10908a19f080299aa0cbb8` |

## 6. Real limits

- **Simulation only.** Every target figure comes from the Verilator test SoC. The flash model's erase and program waits are zero, so the elapsed time is the store's step pacing. Physical calibration was NOT RUN. No hardware or field result is claimed.
- **Composed product image.** The image is the split size fixture, not S3's composed `main`. The mailbox address is still the fixture's placeholder.
- **T_svc value.** The cases grade at the base's 10 ms. The approved 20 ms per family arrives with S2b, and is looser for every family.
- **Not re-run by this review.** I did not re-run the author's long banks: builder, store gate, firmware campaigns, coverage, `nvm_cosim`, census, `firmware-boundary`, `test_ctrl_nvm.py`, `test_ctrl_firmware.py` or behave. Nor did I re-run `nvm_capture_cpu`'s 8x8 simulation. For those I rely on the author's published receipts at this head (`review-evidence/665s4-r1/author/receipts/gates-long`, `gates-short`, HEAD `ee1c0be0`). `check_nvm_capture.py`, which regrades that receipt, I did re-run.
- **Hosted CI and other banks.** No manager source bank runs at this head, and none is claimed. Hosted contexts at the exact head, snapshot 2026-10-29T23:46Z: 47 success, 1 skipped (the physical gPTP job, nightly and manual) and 8 still in progress (`receipts/hosted_checks_snapshot.txt`). Acceptance of those is the manager's.

## 7. Comment-rule check (owner 2026-10-15)

I scanned every added line in `.py`, `.c`, `.h`, `.cpp` and `.hpp` files for bench lane labels, lane names, review rounds, reviewer IDs and issue-comment IDs. None was found in a source comment. Issue references are `#665`, and the decision and design identifiers (F1, D3, D5, DR2a) follow the base's usage. Comment IDs appear only in Markdown links, which the rule allows.

## 8. Pending manager duties

- **Merge with S2b.** At the current-dev merge candidate (live dev `1e80128f`), resolve the three conflicts with S2b (PR #810) semantically. Keep S2b's `layout_flags` and record mover (`mbx_dma`, CSR bank `n_locs - 3`) and S4's generated flash map and `spiflash` bank. Then rebuild and re-run both `nvm_split_target` points and the S2 harness.
- **After S2b, by whichever lane merges second.** Update the docs that quote 10 ms. Update the figures that S2b's 32-bit clock conversion moves: the idle step's cost and "mostly the port's 64-bit clock conversion" (`ctrl_nvm/README.md:354-355`, `nvm_split_target/README.md:169`).
- **Hosted contexts.** Exact-head hosted and act acceptance, including the 8 contexts still running.
- **Residue.** Carry R737-1-R1 to the residue checklist.
- **Follow-up Issue.** Consider one for S4: hosted wiring of the portable harness self-tests.

## 9. Receipts

Every published file is listed in `MANIFEST.sha256`. Host paths in the two probe logs are replaced by `$PACKET`, `$CLONE`, `$HOME` and `$TOOLS`; each log's raw digest is beside it as `.raw-sha256`. Clone integrity after every probe (`receipts/clone_integrity.txt`):
- HEAD is `ee1c0be0`, tree `48581b52`.
- The worktree and index match HEAD.
- The index's (mode, blob, path) list equals the HEAD tree's.
- The submodule gitlinks are unchanged.
- No new CPU netlist appeared in the shared LiteX tree.

R737-1 FINISHED
