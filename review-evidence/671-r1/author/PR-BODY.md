[A592]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN locally at `f54dbe3e`: the saved-state writer gate (5 shapes, all planted defects caught), `nvm_cosim` 465/465 with 39/39 mutants killed, the builder bank with `--require-rv32` and with `--require-elaboration` (each "ALL GATES PASS EXCEPT 1 NOT RUN", gate 11), the capture gate at the new firmware digest, a docs.yml step replica (81/81) and rtl-fast firmware-unit (7/7) and lint/BDD (5/5) replicas. The act replica is not run (it needs an open PR). `671-read-fault` -> `dev`.

## Linked Issue / roles

Relates to #671

Executor: `[A592]`
Internal cleared-context reviewer: `[R602]`
External reviewer: `[R603]`

## Description

**The defect (#671).** Take slot A valid at sequence s > 1 and slot B blank, and a transient fault on A's read at boot. The shipping writer took A as refused and restarted the sequence at 0. Its next commit went to SEQ 1, and a clean boot then preferred the older container, so the commit was lost.

The host model reproduces this on the base firmware:

- B valid at 0x5A5A5 or 0x80000000 and faulted: the change goes to A at SEQ 1 and is lost on the clean reboot.
- A valid and faulted: the writer erases A itself, its commit fails, and both the saved state and the change are lost.

**Can the shipping path see a media read fault at all?** It reads a slot through the memory-mapped QSPI window, a load that always returns bytes. So a fault can only show as two reads of one slot that return different bytes. That is exactly the definition the Mark II store already applies over the same mapping (#665 round 4 item 1; `ctrl_nvm/plat/nvm_flash_litespi.c` `ls_read`). The assignment's STOP condition therefore does not hold, and the rule is applied.

**Where the authoritative sequence is derived.** Only in the firmware. `KL_nvm_backend` stores and reads back the published `PP_NVM_SEL` word 2. The processor's D3 writer, binding manager, arbiter and port work per record and carry no generation. No processor change and no parent adoption are needed.

| Piece | Change |
|---|---|
| `sw/firmware/milan_baremetal/milan_baremetal.c` | Each slot is read once into the private stage and judged there, so the CRC, the records and the sequence come from the same bytes. Before, the sequence word was re-read from flash after validation, and the window was copied a third time. OK stands on one read. Any other verdict, blank included, stands only when two of at most three reads (`NVM_READ_TRIES`) return the same bytes, by verdict, length and CRC-32 digest. A slot with no standing verdict is UNREAD: `VD_LEN`, no sequence. The picked slot is re-staged (at most three times) and accepted only under the sequence it was picked by; an unread pick offers the other slot. The window is filled from the stage. With no slot accepted the generation starts at 0: no sequence is ever taken from a refused slot. **An UNREAD slot holds the writer until reset.** The accepted image is still loaded and the restore walk runs, but nothing is captured, erased or written, `milan_nvm commit` is refused, and the writer answers no liveness deadline, so `nvm_backed` reads 0 (the existing retired-writer signal). The boot line gains `read faults=N unread=M`, and `milan_nvm` prints "writer HELD" |
| `sw/firmware/nvm_hosttest/` | The stub `SPIFLASH_BASE` is a host call, so every read the firmware opens is counted and can be answered from a view with one slot's bytes wrong (`--read-fault`, `--read-ff`). Checks 13 (read faults) and 14 (no generation from a refused slot), and four named #671 plants |
| `tb/verilator/nvm_cosim/run_cases.py` | The two new writer statics join the CPU-only restart model, which refuses a static it does not name |
| `tb/verilator/nvm_capture_cpu/measurements.json` | Re-measured at the new firmware digest, all six arms |
| Docs | FASTCONNECT section 7 (a slot that could not be read is not a slot that failed 6.2); `BAREMETAL_FIRMWARE.md` Boot; the host-suite README; SNAPSHOT_OWNERSHIP section 18 and section 20 item 6 figures |

Unchanged:

- the A/B write sequence and its power-loss guarantee;
- the KLJ2 record format;
- the register map;
- `nvm_capture()`;
- the console's live slot status.

**Capture, at firmware `3b9468ee`.** The worst 8x8 contract-clock capture is **13.86328 ms** against the 24.5 ms limit: 10.63672 ms of margin, 3.5345x the 49 ms floor (previously 13.86484 ms). The 1x1 maximum is 3.96548 ms (12.3566x). The census is unchanged.

**Firmware size.** Text grows by 1,680 B (15,476 to 17,156) against product 1x1 headers; bss grows by 8 B. The BIOS ROM is 128 KiB.

**Boot time.** With both slots valid, the boot reads three containers through the mapping instead of about five passes. The fault worst case is twelve, an estimated 2.5 s of flash at 8x8 against #397's 20 s comparison. This is an estimate from #397's measured read rate, not a measurement.

## Authoritative references

- #671 and its assignment, [comment 6098494890](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6098494890).
- [#665 decision 2](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-5997929153) and [round 4 item 1](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-5999350068).
- `docs/design/SAVED_STATE_FASTCONNECT.md` sections 6.2 and 7; `docs/design/SAVED_STATE_MATERIALIZATION.md` section 6.3.
- `sw/firmware/ctrl_nvm/README.md`, Boot items 3, 4 and 9 and "What this does not prove".
- `docs/findings/397_SERVICE_BUDGET.md` (the boot comparison).

## How to get into the same state

```sh
git fetch origin
git switch 671-read-fault
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP
python3 -m pip install pyyaml
```

## How to validate

```sh
python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
make -C tb/verilator/nvm_cosim run
python3 scripts/check_nvm_capture.py
python3 sw/builder/test_builder.py --require-rv32
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32
```

Expected result / pass criteria:

- the writer gate ends "saved-state writer gate: OK across 5 shape(s), and every planted defect reddened";
- every #671 plant is "caught by N named finding(s)": `restart_at_zero`, `unbounded_retry`, `generation_from_refused_slot`, `verdict_only_agreement`;
- `nvm_cosim`: "465 checks: 465 PASS, 0 FAIL", "39 of 39 mutant(s) killed by their named check";
- the capture gate: "PASS: capture census, clocks, both timing arms and receipt agree";
- the builder: "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11, which needs a local implementation build tree);
- the store suite: "saved-state store gate (#665 F1): OK across 5 shape(s)".

## Known limitations / out of scope

- **A fault that returns the same wrong bytes twice is indistinguishable from a refusal of those bytes.** The same holds for a slot read as all `0xFF` twice, which reads as blank. Either can still let the next commit restart the sequence below a surviving container. The memory-mapped path reports no read failure, so this is the limit of the rule in both stores, and it is stated in both suites' READMEs.
- The held state lasts until reset. A slot that never reads cleanly holds the writer on every boot, by design, as in the Mark II store.
- `nvm_backed` cannot distinguish a held writer from a retired one; the console names which. The register map is unchanged.
- The #397 service-budget receipt describes the previous firmware; boot timing is estimated here, not re-measured.
- No processor change and no bench run.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [ ] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
