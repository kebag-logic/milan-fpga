[A592]

## Contents

- [Status](#status)
- [Linked Issue / roles](#linked-issue--roles)
- [Description](#description)
- [Round 5](#round-5)
- [Round 4](#round-4)
- [Authoritative references](#authoritative-references)
- [How to get into the same state](#how-to-get-into-the-same-state)
- [How to validate](#how-to-validate)
- [Known limitations / out of scope](#known-limitations--out-of-scope)
- [Definition of Done](#definition-of-done)

## Status

Round 5 is ready for independent re-review at `0c276b621d638c9a83e82f71fbf07bc153517bf7`. `671-read-fault` -> `dev`.

The writer gate passed five shapes at 3,422 cases each and caught all 49 controls, including the new `r_digest_with_trailer` on the first shape and both product shapes, in 267.29 s at four jobs. Co-simulation passed 465/465 checks and killed 39/39 mutants. The service-budget, firmware-unit (including the Mark II store's 435 tests) and rtl-fast replicas passed. All 101 builder functions passed with every elaboration arm. The 78 runnable docs-check positions passed. All six capture arms and the receipt gate with its four controls passed. The new commits are local. Hosted and act evidence is required at the published head; the hosted writer gate under the builder's 1,200 s limit is the first thing to read.

## Linked Issue / roles

Closes #671

Executor: `[A592]`
Internal cleared-context reviewer: `[R602]`
External reviewer: `[R603]`

## Description

A boot read fault could make the shipping writer discard a valid slot and restart the generation at zero. Its next verified commit could then disappear on a clean reboot, or overwrite the saved authoritative slot.

The firmware now judges each slot from one staged read. A validated container stands on one read; a refusal or blank verdict requires two matching reads within three attempts. Two refused reads match when their verdicts and byte counts, a CRC-32 over all but their last four bytes, and those four bytes are equal. The chosen container must read back under its validated sequence, again within three attempts. A slot that cannot be judged or re-staged leaves authority unknown and holds persistence until reset. The restore still offers the accepted slot. The hold applies both to a cold boot and to a writer restart without a fabric reset.

While held, the writer captures, erases, programs and acknowledges nothing, refuses the console commit, and stops heartbeating. The existing `nvm_backed` status therefore makes no durability claim. The console names each unread slot and its cause. A writer retired for another cause continues to name that cause. An explicit operator wipe still erases both slots.

Only the firmware derives the authoritative generation. The parent backend stores and reads back the published sequence; the processor writer and port operate on records and carry no generation. No processor change or adoption is needed. The register map, record format, A/B write sequence and power-loss guarantees are unchanged.

| Artifact | Result |
|---|---|
| `sw/firmware/milan_baremetal/milan_baremetal.c` | Staged validation, bounded judgement and re-stage, validated sequence selection, cold-boot and re-attach hold, and console cause |
| `sw/firmware/nvm_hosttest/` | Read-fault injection, generated windows, independent read-count expectations, persistent-state comparisons and named controls |
| `tb/verilator/nvm_cosim/run_cases.py` | Shares the complete writer-static restart model with the host suite |
| `sw/builder/test_builder.py` | The writer-gate timeout grows from 600 to 1,200 s; a hosted run already took 594 s before round 4 |
| `sw/firmware/nvm_hosttest/nvm_host.c` `settle()` | One `memcmp` replaces the CSR word walk when nothing was stored, so the larger campaign runs about 3.7 times faster per harness run |
| Capture receipt and saved-state documentation | Firmware-bound measurements, the hold contract, detection limits and reproducible evidence |

## Round 5

This answers assignment #671 comment 6107082416 and PR #715 reviews R603-4 (NEGATIVE, one MAJOR) and R602-4 (POSITIVE). New commits start at `7bc7ceca`; no history was rewritten.

- **Refused-read agreement distinguishes the bytes (R603-4-F1).** Round 4 compared refused reads by one CRC-32 over every byte read, trailer included. Over any container whose CRC closes, that is the constant residue `0x2144df1c`, so two different refused containers agreed. Two refused reads now match only when their verdicts and byte counts, a CRC-32 over all but their last four bytes, and those last four bytes are all equal. For two containers whose CRCs close, they match only on a genuine CRC-32 collision of their prefixes. Any two reads that differ in one or two bits, or within one 32-bit burst, are always told apart. A trailer-only difference is also told apart, which a prefix-only digest would miss. A second full copy for byte comparison is not available: the private stage holds one slot. The three-read bound, validated-only generation, fallback and hold are unchanged.
- **The class is in the standing generated suite.** A new harness fault, `--read-sealed`, flips the entity ID's low byte or a record-area byte and rewrites the trailer over the faulty bytes. Every faulty read is then a different container whose CRC closes and that is refused, `VD_ENT` or `VD_REC`. Both manners join every group with a container to seal. They cross every generated window, both orientations, both layouts, cold boots and writer restarts. The rotated sequences alone left R603-4's exact class short of the boundaries: in 20 of its 24 combinations a sequence was missing. So the generator also adds that class at every sequence of its group, both orientations and both entry paths, for each sealed manner. The class is two sealed refusals opening a judgement and then a clean read, and the reference model finds its window. Each shape now runs 3,422 of 3,508 generated cases: 1,775 cold boots and 1,647 restarts. The 86 excluded cases are the same documented limit as before.
- **Named control.** `r_digest_with_trailer` restores round 4's digest and agreement. It fails by name ("on reads that returned different bytes") on `endstation_arty_4x4`, `endstation_ax7101_1x1_tdm8` and `endstation_ax7101_8x8`: 180 named findings on each (82 restart / 98 cold) in a full-count run. All fourteen #671 controls fail by name on all three shapes.
- **R603-4's probe.** Unmodified, it now fails its own defect assertion on its first case. The faulty boot accepts A after a third, clean read, commits to B at the next sequence, and the clean reboot keeps every record. A copy that records all four cases instead of asserting the defect reports all four DEFECT GONE (1x1 and 8x8, slots A and B: acknowledged, not held, change kept, 0 records lost). With the control planted, the same copy reproduces R603-4's figures exactly (53 and 163 records lost; the change lost from slot B).
- **The hosted writer-gate timeout, found and fixed.** At `7bc7ceca` the hosted `docs-check` failed. The builder step killed `test_nvm_firmware.py --self-test` at its 1,200 s limit (run 38120473372) before it finished the #671 controls. Almost all of the gate's time is the host model's `settle()`, which walked 1,024 CSR words on every CSR access. It now returns after one `memcmp` when nothing was stored; otherwise the walk is unchanged. Every harness run of checks 1-14, the disabled-writer and the boot-walk graders on three shapes was run on both forms: 10,581 twin runs, with no difference in any transcript or dumped file. Locally at four jobs, the suite passed in 217.84 s with 3,382 cases and nothing else heavy running, and in 267.29 s at the final 3,422 cases alongside a builder run. Round 4's 2,158-case suite took 461.48 s. The builder limit stays 1,200 s. The hosted exact-head result is pending.
- **The Mark II store has the same class (item 2), unchanged here.** `sw/firmware/ctrl_nvm/nvm_store.c:142-149,165-173,208-216` chains a refusal's digest over the 40-byte header read and then a separate read of the whole container. For any container whose CRC closes, the container's own bytes cancel, so only the header read and the length are distinguished. Driven on its host flash model with two sealed reads of slot A (entity or record-area byte), the unchanged store keeps the refusal with `read_faults=0`, is not held, and commits sequence 1 to B. The clean reboot prefers A, so the acknowledged commit is lost, on 1x1 and 8x8. Its README's detection-limit sentence (Boot item 3 and the limits list) overstates the digest. This is reported for a separate Issue.
- **Documentation.** `BAREMETAL_FIRMWARE.md` and FASTCONNECT section 7 state the comparison exactly, why the trailer is excluded and the detection limit. The host-suite README adds the sealed faults, the case counts and the control.
- **Not taken up:** R602-4-S1 (the boot line's `read faults=` count is not graded) and R602-4-S2 (no generated case faults both slots). Both are optional SUGGESTIONs.

**Firmware size.** With the pinned RV32 SDK and product 1x1 headers, text is 17,579 B: +96 B this round and +2,050 B over the base. Bss is 104 B, unchanged this round and +16 B over the base. Data remains 104 B.

**Capture.** All six arms passed, 96 clean captures, bound to firmware sha256 `497845e6243b919638285ce4de18e6687beff6a509d72c8e2e2f2d45ba7b1bed`. The 8x8 contract maximum is 13.86328 ms against 24.5 ms: 10.63672 ms of margin and 3.5345x the 49 ms floor, unchanged from round 4. The 1x1 maximum is 3.96548 ms. The non-contract 100 MHz comparison is 10.42973 ms. The receipt gate and its four mutation controls pass.

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

- #671 Required and Acceptance 1 to 3; assignment comments 6098494890, 6104799677 and 6107082416.
- #665 decision 2 and the byte-agreement decision (comments 5997929153 and 5999350068).
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

Use disk scratch through `TMPDIR`; limit campaign workers to four and simultaneous Verilator builds to two. The handoff records the resource-limited builder invocation and complete gate table. Expected writer result: five shapes pass at 3,382 cases each and all 49 planted defects redden. Expected co-simulation result: 465/465 and 39/39 named mutants. Capture must bind the current firmware digest and satisfy the 24.5 ms contract limit.

## Known limitations / out of scope

- Memory-mapped flash always returns bytes. A differing read reveals a media fault; the same wrong bytes twice, two all-0xFF reads, or an address fault returning another valid container can be indistinguishable from stored contents. Both suites state that limit.
- Two refused reads are compared by a 32-bit CRC over all but their last four bytes plus those four bytes. Reads that differ in one or two bits, or within one 32-bit burst, are always told apart; other differences collide with a probability of about 2^-32.
- The Mark II store (`sw/firmware/ctrl_nvm`) has the same class of collapse in its refusal comparison and is unchanged here. The reproduction and file:line evidence are in the handoff for a separate Issue.
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
