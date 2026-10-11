[A592] REVIEW READY (round 2)
Commit: `9112a0df27acc1381091845e94d8eaa1407f1bbb` on `671-read-fault` (local branch, not pushed under the lane rules). The round started at `f54dbe3e`, and seven new commits answer [R602-1](https://github.com/kebag-logic/milan-fpga/pull/715#issuecomment-6100699429) and [R603-1](https://github.com/kebag-logic/milan-fpga/pull/715#issuecomment-6100671345) per [the round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6100704879). No rebase or amend.
Changed:
- Item 1, R603-1-F1 and R602-1-S2: check 13 can now fail for every mechanism the fix depends on (`sw/firmware/nvm_hosttest/`, 446 cases per shape).
  - What it faults:
    - a record-area byte of the valid slot (refused only by the CRC over every byte read), besides its magic byte and sequence word;
    - both slots valid in both orientations, the newer at 0x5A5A5 or at 0 across the wrap, faulted over every window;
    - the older slot faulted for the whole boot;
    - the newer slot's re-stage answered with the older slot's container (`--read-other`).
  - What it grades:
    - the boot line, the offer, and the window byte for byte;
    - every saved record surviving the reboot, not only the changed one.
  - Named `--self-test` controls: `r_digest_header_only`, `r_fill_from_flash`, `r_restage_fail_offers_none`, `restage_fail_not_unread`, plus `r_restage_any_seq` (R603-1-S3).
  - With the first four, nine #671 controls, each planted on `endstation_arty_4x4`, `endstation_ax7101_1x1_tdm8` and `endstation_ax7101_8x8`. Each is caught on every shape by a finding carrying its own words.
  - The five reviewer plants are byte-identical to the probes' texts.
- Item 2, R602-1-F1 and R603-1-F2: the boot worst case, with per-read costs MEASURED on the product CPU (service-budget harness, unchanged firmware).
  - A refused read costs 24.5 µs per byte: 1,611.6 ms for a header claiming the whole 64 KiB slot, measured, and linear across two and four reads.
  - A judgement stands on the first OK read, so a slot can spend two refused reads first. The worst boot is therefore ten slot-length reads and two container reads, not six.
  - ESTIMATE (a sum of measured costs): about 16.4 s (1x1) and 17.1 s (8x8) from reset to entity enabled, inside #397's 20 s comparison.
  - The 2.5 s of round 1, and the reviewers' 6.5 to 7.4 s, used a 15.5 µs/B rate that does not price the digest pass.
  - The optional cap is not taken: a read stopped at the container length cannot compute section 6.2's verdict, so the published verdict and the 6.2 order would change (a record-format change).
  - The writer-restart note is updated: a CPU-only restart under such faults outlasts T-NVM-WRITER-ALIVE, so the fabric revokes `nvm_backed`, an honest loss report.
  - Round 1's claim that the nominal boot "gets shorter" was never measured and is withdrawn. Both slots valid at 8x8: 1,247.27 ms to entity enabled.
- Item 3, R603-1-S2: `milan_baremetal.c` gains `nvm_held`, set only where the writer would have gone live with a slot unread.
  - `milan_nvm` and the commit refusal name the hold only then; a retired writer reports its own cause.
  - This is checked for all four causes (`--boot-backend contract|over|live`, four refused loads).
- Item 4, R603-1-S1 and R602-1-S3: the explicit `milan_nvm wipe` still erases both slots while held, as for a retired writer. Documented in the firmware, `BAREMETAL_FIRMWARE.md` and the host README, and checked.
- Item 5, residue: R602-1 R1 (FASTCONNECT 7, exact text), R3 (SNAPSHOT_OWNERSHIP section 18, exact text), R4 (host README) and the check renumbering (R602-1 R2 = R603-1 R1).
- Item 6, optional: the read-fault count is documented as a floor (R602-1-S1); the other-slot view is a fault mode with its control (R603-1-S3).
- Capture re-measured at the round-2 firmware (`33eaa0c3`), all six arms: identical maxima. 8x8 contract 13.86328 ms against 24.5 ms (margin 10.63672 ms, 3.5345x); 1x1 3.96548 ms (12.3566x).
- Firmware size, corrected: with the pinned SDK (`riscv32-linux` GCC 14.3.0), text +1,712 B (15,529 to 17,241) and bss +12 B. Round 1's +1,680 B was built with the local tree's `riscv64-elf` GCC 16.2.0 and mislabelled.
Validation (rc 0 each; CPython 3.12.3; pinned Verilator 5.050 for suites; `49d28e5a` is the last commit any of these rows reads except the docs replica and capture gate, run at `9112a0df`):
- `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test`: "OK across 5 shape(s), and every planted defect reddened", 34 controls; 237 s here, 358 s with `--jobs 4`.
- `make -C tb/verilator/nvm_cosim run`: 465/465, 39/39 mutants killed.
- `python3 sw/builder/test_builder.py --require-elaboration --require-rv32`: "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11).
- `python3 scripts/check_nvm_capture.py`: PASS; its four `--mutation` arms exit 1.
- Step replicas: docs.yml 81/81 (includes `test_builder.py --require-rv32`); rtl-fast firmware-unit 7/7 (the store suite "OK across 5 shape(s), 435 tests"); lint/BDD 5/5.
- `make -C tb/verilator/fw_service_budget`; the record-space gate with `--self-test`.
- Base firmware graded by this head's checks: 645 findings per product shape, 124 "was lost on the clean reboot".
- The act replica was not run: it needs an open PR.
Acceptance criteria:
1. Met in the firmware host tests, with both orientations and the sequence boundaries.
   - Faults on the header, the sequence and the record area.
   - Both slots valid across the wrap.
   - Every case runs a change, its commit and a clean reboot. Every saved record and the change survive, or the writer held and persisted nothing.
   - The processor writer carries no generation, so its half does not apply (confirmed by both reviews).
2. Met. `restart_at_zero` fails by name, as do the eight other controls, on three shapes.
3. Met. The A/B write path is unchanged; `nvm_cosim` and the Mark II power-cut suite pass.

Both first-round reviews judged 1 to 3 met with the identical-fault limit stated, so the PR body now says "Closes #671".
Open risks/questions:
- The detection limit is unchanged and stated: same wrong bytes twice, all `0xFF` twice, an address fault returning the other slot's container on a judgement read.
- The worst-case boot (about 17.1 s at 8x8) is an estimate summed from measured costs, about 2.9 s inside the 20 s comparison. A stored header claiming the whole slot costs 3.2 s per slot with no fault at all.
- `--self-test` takes 358 s at four jobs against the builder bank's 600 s timeout; the hosted time at this head is unknown until it runs.
- Observation outside #671: on the contract-mismatch path the disabled writer still heartbeats, as at base. Candidate follow-up.
- dev moved to `1fb0ed9a` (findings pages only); the trial merge is clean.
