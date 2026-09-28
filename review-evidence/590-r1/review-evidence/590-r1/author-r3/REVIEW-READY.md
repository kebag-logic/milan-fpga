[A411] REVIEW READY

Commit: `93262f2512054166ae753eda24d76c99f2ea6714` (local branch `590-592-599-firmware`, not pushed; round-3 commits `26a26e1f3`, `69d833735` and `93262f251`). Processor pin unchanged at `16be6768f710e79450aace277abacd6c2c3336e5`.

Changed:

- **R368-2 N1.** `milan_baremetal.c` adds a startup admission flag, `nvm_started`. It is set in `nvm_boot()` only after the shape check passes, and it is never set on the CSR identity-mismatch return in `milan_init()`. `nvm_heartbeat_tick()`, the only heartbeat path (dispatch hook, Milan commands, walk yields, idle service), returns before reading time, polling the PHY or writing `PP_NVM_STAT` unless the writer was admitted. The retired-writer and tag-mismatch rules are unchanged.
  - New committed test `sw/firmware/nvm_hosttest/test_disabled_writer.py`. It plants each rejected state on all five shapes, Arty included. Nine console lines (empty, unknown and every Milan command) are each sent twice, and every case must show `hb=0 backed=0 stale=0` both immediately and after 2500 ms. Removing the guard fails both states.
  - Consequence: a rejected startup also does no PHY poll or link publication. The identity path must not touch a foreign fabric, and the shape path never installed the idle service.
- **N2 = F4.** `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` §18 and §20 item 6 now state the current receipt:
  - measured commit `26a26e1f`, tree `1ced48e2` and firmware `89c0360e…`;
  - the six maxima with their floor ratios;
  - the 8x8 margin of 11.26648 ms to 24.5 ms, and 11.06894 ms of margin gained.

  24.30246 ms remains only as the labelled historical value. The PR body's margin sentence matches the receipt.
- **F5.** BAREMETAL_FIRMWARE.md and the #397 page say that a built-in body can lapse backing after about 1,750 ms, net of the 250 ms rate-limit phase.
- **S5.** Patch 0006 defines a strong `bios_dispatch_hook_required()`, which the firmware calls at NVM startup. A BIOS without 0006 fails to link by name, in both the host test and a replay of the product RV32 BIOS link recipe.
- **S6.** The `apply.sh` header and the builder comment are corrected.
- **S7.** The `remove-dispatch` verdict requires the named per-line finding, with four new portable controls (47 grading checks).
- **S8.** A register-5 NAK after successful status and control reads kills a new `ack-ignored` mutant.
- **S9.** The findings page adds the phase-probe locator and explains its N/A rows. R368-2 T1-T4 are also addressed.
- **Builder edits:** the two S6 comments, plus the gate-35 host fixture's declaration and empty definition of the BIOS marker, which the S5 link dependency forces. No assertion or grading rule changed.

Capture re-measure (firmware changed; receipt binds `89c0360ed2eb63566d0413e9c721aee05aae4581f23d3897a1ae853b46a10070`). 96 captures, zero mismatches, zero open-record copies:

| Shape | CPU MHz | Traffic | Maximum ms | 49 ms floor ratio |
| --- | --- | --- | --- | --- |
| 1x1 | 50 | on | 3.88779 | 12.6036x |
| 1x1 | 50 | off | 3.84214 | 12.7533x |
| 8x8 | 50 | on | 13.23352 | 3.7027x |
| 8x8 | 50 | off | 13.06923 | 3.7493x |
| 8x8 | 100 comparison | on | 9.95464 | 4.9223x |
| 8x8 | 100 comparison | off | 9.94094 | 4.9291x |

#397 harness (native, `--enforce-service`):

- All twelve positive plans pass on both shapes, with zero unbacked cycles and no service findings. The largest heartbeat gap is 322.47884 ms.
- The largest MDIO transaction is 0.12457 ms and the largest complete poll 0.83375 ms.
- The worst 8x8 duty plus UART plus charge is 120.53971 ms, leaving 4.46029 ms under the 125 ms trigger.
- No capture or MDIO STOP condition occurred.

F6 evidence (the round-3 author packet, `native-evidence/`: 135 raw logs, JSON receipts, specs and build logs, each bound by raw and stored SHA-256 and size, gzip-compressed above 200 KB):

- `queued-builtins`, 1x1 and 8x8: 1051 of 1051 lines, each with a dispatch tick; zero unbacked cycles.
- `remove-dispatch` on `queued-builtins`: 1051 named per-line findings plus backing lost, 8238.99253 ms gap.
- `remove-dispatch` on `queued-short`: 350 named per-line findings.
- Target `late-sample`: the named finding "PHY initial gigabit negotiation was not published".
- Byte-only capture: 24.30310 to 24.30446 ms, 1.83648x against the 1.5x bound.
- Missing-copy, missing-traffic and missing-publication controls are caught.
- `run.py --regrade` passes on all 15 kept service logs at the head above.

Validation (rc 0 at the commit above, physical worktree, no pipelines; clean before and after):

- `sw/builder/test_builder.py --require-elaboration --require-rv32`: compiler present, ordered firmware census, gate-35 host link. `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11 calibration; report absent).
- The same bank with `--require-elaboration` and all three cross-compiler candidates hidden (`EXCEPT 2 NOT RUN`: the intentional compiled-census omission and gate 11).
- `sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test`: five shapes including Arty, five planted writer defects, the disabled-writer grade with its guard mutant, the link guard, and PHY mutants `no-publish`, `defer-recovery`, `late-sample` and `ack-ignored`.
- `scripts/check_nvm_capture.py`, plus a regrade of all 96 kept capture rows against the receipt.
- `tb/verilator/fw_service_budget/run.py --self-test` (47 grading, 14 flash) and 15 `--regrade` runs.
- `scripts/ci_scope.py --selftest`.
- Docs, paths, style, archive, TOC and `check_em_dash --base 20aa4eabf`.
- Feature, processor-source, baremetal-only, entity-shape, Python/C++ idiom, hygiene and test-evidence checks.
- `git diff --check 20aa4eabf`.
- Unchanged reviewer probes at this head: the R369 MDIO phase probe (`PHASE=1`: `0x796d`, `0x001c`, `link_status=13`); the R368 disabled-writer probe (head `hb=0 backed=0 stale=0` in both states); the R369 built-in oracle probe; R368 `edge-cross` (killed on all five shapes).

Acceptance criteria: round-3 required items 1-4 and taken suggestions S5-S9 are met with the evidence above. The capture is re-measured and the receipt binds the final firmware. #590 and #592 assigned criteria, and #599 criteria 1, 2, 3 and 5 in simulation scope, are met.

Open risks/questions:

- #599 acceptance 4 is the post-merge bench rerun, which also confirms the MDIO phase on silicon. The bench LiteX environment must carry the updated patch 0006, or the firmware now fails to link.
- Long single built-ins remain the documented residual.
- The physical-utilization calibration stays unrun because its report is absent.
- R369-1 S1, S3 and S4 were not in the taken list.
- The F6 native runs executed at `26a26e1f3`. Its firmware and native inputs are byte-identical to this head; the later commits touch only docs, the receipt and the builder fixture.
- No push, PR edit, merge, RTL, processor, configuration or hardware change was made. Independent review is pending.
