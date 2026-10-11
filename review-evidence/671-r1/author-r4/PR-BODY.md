[A592]

## Contents

- [Status](#status)
- [Linked Issue / roles](#linked-issue--roles)
- [Description](#description)
- [Round 4](#round-4)
- [Authoritative references](#authoritative-references)
- [How to get into the same state](#how-to-get-into-the-same-state)
- [How to validate](#how-to-validate)
- [Known limitations / out of scope](#known-limitations--out-of-scope)
- [Definition of Done](#definition-of-done)

## Status

Round 4 is ready for independent re-review at `7bc7ceca6ba1dd1a268d6fa1704613bb141487fe`. `671-read-fault` -> `dev`.

The full-bound writer gate passed five shapes and caught all 46 controls in 461.48 s at four jobs. Co-simulation passed 465/465 checks and killed 39/39 mutants. The firmware-unit bank and all required builder elaboration arms also passed. All six capture arms and the refreshed receipt/documentation checks passed. The new commits are local. Hosted and act evidence is required after the final head is published.

## Linked Issue / roles

Closes #671

Executor: `[A592]`
Internal cleared-context reviewer: `[R602]`
External reviewer: `[R603]`

## Description

A boot read fault could make the shipping writer discard a valid slot and restart the generation at zero. Its next verified commit could then disappear on a clean reboot, or overwrite the saved authoritative slot.

The firmware now judges each slot from one staged read. A validated container stands on one read; a refusal or blank verdict requires two matching reads within three attempts. The chosen container must read back under its validated sequence, again within three attempts. A slot that cannot be judged or re-staged leaves authority unknown and holds persistence until reset. The restore still offers the accepted slot. The hold applies both to a cold boot and to a writer restart without a fabric reset.

While held, the writer captures, erases, programs and acknowledges nothing, refuses the console commit, and stops heartbeating. The existing `nvm_backed` status therefore makes no durability claim. The console names each unread slot and its cause. A writer retired for another cause continues to name that cause. An explicit operator wipe still erases both slots.

Only the firmware derives the authoritative generation. The parent backend stores and reads back the published sequence; the processor writer and port operate on records and carry no generation. No processor change or adoption is needed. The register map, record format, A/B write sequence and power-loss guarantees are unchanged.

| Artifact | Result |
|---|---|
| `sw/firmware/milan_baremetal/milan_baremetal.c` | Staged validation, bounded judgement and re-stage, validated sequence selection, cold-boot and re-attach hold, and console cause |
| `sw/firmware/nvm_hosttest/` | Read-fault injection, generated windows, independent read-count expectations, persistent-state comparisons and named controls |
| `tb/verilator/nvm_cosim/run_cases.py` | Shares the complete writer-static restart model with the host suite |
| `sw/builder/test_builder.py` | The writer-gate timeout grows from 600 to 1,200 s; a hosted run already took 594 s before this round |
| Capture receipt and saved-state documentation | Firmware-bound measurements, the hold contract, detection limits and reproducible evidence |

## Round 4

This answers assignment #671 comment 6104799677 and PR #715 reviews R602-3 and R603-3. New commits start at `fc0c517c`; no history was rewritten.

- **Generated windows (R602-3-F1, R603-3-F1).** Each fault group crosses every manner of fault with every start position in the complete 13-read boot bound or 12-read restart bound and every length 1 through 4, plus the whole-boot window. It covers both orientations, one-valid/one-blank and both-valid layouts, cold boots and writer restarts. Starts a clean boot never reaches remain in the standing suite. No window is excluded to reduce runtime.
- **Sequence reduction, explicit.** The four one-valid sequences (1, 0x5A5A5, 0x80000000, 0xFFFFFFFF) and two both-valid sequences (0x5A5A5 and 0 across the wrap) rotate across windows instead of multiplying every window. No window is removed. This is the assignment's allowed sequence reduction for runtime. Of 2,244 generated cases, 86 lie outside the stated detection limit; 2,158 run per shape: 1,119 cold boots and 1,039 restarts. Every window retains every applicable byte-fault manner.
- **Exact expectations.** `read_fault_cases.expect()` models the judgement reads, the chosen slot's re-stage and the other slot's re-stage once, from the contract. Every case checks its exact read count and expected hold. Cases exercise all three attempts of judgements and re-stages. A clean reboot result is reused only for identical A/B slot bytes and hold state within that firmware and shape.
- **Controls.** All thirteen #671 controls fail by their named findings on `endstation_arty_4x4`, `endstation_ax7101_1x1_tdm8` and `endstation_ax7101_8x8`. The new unbounded re-stage control `p_restage_unbounded` produces 52 exact-count findings per shape; `r_restage_four_tries` produces 68; `r_judge_four_tries` produces 140. These are complete-case counts, distinct from the suite's early-stop counts. The reviewers' re-stage plants are also caught independently. A boot read storm ends at 1,001 reads and is graded as over-bound.
- **Correct base reproduction (R602-3-F2).** Base firmware `e8454e27`, sha256 `a73ecc25c77bfb7c4e1c2c711d72f0b560dd7e8d18cde92f40e67efcc84f0eb3`, produces 2,660 findings per product shape under this round's checks 13 and 14; 124 say the committed change was lost on the clean reboot. For this comparison only, the restart model retains the base's 15 writer statics, excluding the four absent names `nvm_unread`, `nvm_held`, `nvm_read_faults` and `nvm_unstaged`. The earlier 645 / 124 figures belonged to `9112a0df`.
- **Console cause (R603-3-S1).** A picked slot whose re-stage fails says "did not read back as it was judged in 3 reads". A judgement failure says "gave no standing verdict in 3 reads". The same helper supplies the boot hold and console refusal; the host gate checks the cause against the reference model.
- **Held re-attach publication (R602-3-S1).** Documented: word 2 describes the slot accepted in the new judgement, possibly older, or zero if none. The existing live window remains untouched. The word is diagnostic evidence; it cannot make the held writer persist.

**Firmware size.** With the pinned RV32 SDK and product 1x1 headers, text is 17,483 B: +186 B this round, +1,954 B over the base. Bss is 104 B: +4 B this round, +16 B over base. Data remains 104 B.

**Capture.** All six arms passed, 96 clean captures, bound to firmware sha256 `41000488944bea651733b9708fa0c3a72926ce2308034c51209f2dd95a27b2a2`. The 8x8 contract maximum is 13.86328 ms against 24.5 ms: 10.63672 ms margin and 3.5345x the 49 ms floor. The 1x1 maximum is 3.96548 ms. The 100 MHz comparison is non-contract, at 10.43406 ms. The receipt gate and its four mutation controls pass.

## Authoritative references

- #671 Required and Acceptance 1 to 3; assignment comments 6098494890 and 6104799677.
- `REQUIREMENTS.md`, product ownership and release verification.
- `docs/design/SAVED_STATE_FASTCONNECT.md`, sections 6.2 and 7.
- `docs/design/SAVED_STATE_MATERIALIZATION.md`, section 6.3.
- `sw/firmware/ctrl_nvm/README.md`, Boot items 3, 4 and 9.
- `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md`, writer restart and capture measurement.

## How to get into the same state

```sh
git switch 671-read-fault
git submodule update --init protocol-processor gptp-processor third_party/verilog-axis
```

Use the repository's pinned CPython dependencies, RV32 SDK and Verilator 5.050 for the suites. The capture recipe names its product build environment. Before any Git command within a submodule, verify its top-level directory.

## How to validate

```sh
python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test --jobs 4
make -C tb/verilator/nvm_cosim run JOBS=2 POOL=4
make -C tb/verilator/fw_service_budget
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
python3 sw/builder/test_builder.py --require-rv32 --require-elaboration
python3 scripts/check_nvm_capture.py
python3 scripts/check_nvm_record_space.py --self-test
python3 scripts/docs_check.py
python3 scripts/gen_toc.py --check
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
python3 scripts/check_hygiene.py --check
```

Use disk scratch through `TMPDIR`; limit campaign workers to four and simultaneous Verilator builds to two. The handoff records the resource-limited builder invocation and complete gate table. Expected writer result: five shapes pass and every planted defect reddens. Expected co-simulation result: 465/465 and 39/39 named mutants. Capture must bind the current firmware digest and satisfy the 24.5 ms contract limit.

## Known limitations / out of scope

- Memory-mapped flash always returns bytes. A differing read reveals a media fault; the same wrong bytes twice, two all-0xFF reads, or an address fault returning another valid container can be indistinguishable from stored contents. Both suites state that limit.
- The writer-restart model resets writer statics only. It assumes the retained fabric/window contract; it does not prove the boot code's memory initialization or physical reset behavior.
- A slot that never reads cleanly holds the writer on every boot. Only the operator's explicit wipe discards that saved state.
- Faulted boot time remains an estimate: ten worst-case 64 KiB refused reads plus two valid container reads give about 16.4 s at 1x1 and 17.1 s at 8x8, against the existing 20 s comparison. Capture timing is measured separately. A long restart can exceed the 2 s liveness deadline.
- Runtime capture prefill's fresh flash read remains tracked by #717.
- No hardware, flashing, processor change or merge. Hosted checks, act replication and current-dev merge-candidate validation remain later duties at the published head.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
