[A592] REVIEW READY
Commit: `f54dbe3e393e2b1b027f1825c4acb736cf502cda` on `671-read-fault` (local branch, not pushed under the lane rules; 4 commits on dev `e8454e27`)
Changed:
- `sw/firmware/milan_baremetal/milan_baremetal.c`: each slot is read once into the private stage and judged there, so the CRC, the records and the sequence come from the same bytes. Before, the sequence was re-read from flash after validation and the window was copied from flash a third time. OK stands on one read; any other verdict, blank included, stands only when two of at most three reads (`NVM_READ_TRIES`) return the same bytes (verdict, length, CRC-32 digest). A slot with no standing verdict is UNREAD: `VD_LEN`, no sequence. The picked slot is re-staged (at most three times) and accepted only under its picked sequence. No generation is taken from a refused slot. An UNREAD slot HOLDS the writer until reset: the accepted image is loaded and the walk runs, but nothing is captured, erased or written, `milan_nvm commit` is refused, and no liveness answer is given, so `nvm_backed` reads 0. The boot line adds `read faults=N unread=M`. No register-map, record-format or A/B change.
- `sw/firmware/nvm_hosttest/`: a host read-fault model (every mapped read counted, faulty views per window), check 13 (read faults) and check 14 (no generation from a refused slot), and four named plants.
- `tb/verilator/nvm_cosim/run_cases.py`: the two new statics join its restart model.
- Capture receipt re-measured. Docs: FASTCONNECT section 7, `BAREMETAL_FIRMWARE.md`, host-suite README, SNAPSHOT_OWNERSHIP section 18.
Where the sequence is derived: firmware only (`nvm_read_slot`, `nvm_judge_slot`, `nvm_restage`, `nvm_pick_slot`, `nvm_boot`, `nvm_commit`). `KL_nvm_backend.sv` stores and reads back the published word 2 (lines 424, 439, 490, 582). The processor's writer, port, arbiter and binding manager carry no generation, so there is no processor change and no adoption.
Read path: the shipping read is a memory-mapped load that always returns bytes, so a fault shows only as differing reads. That is the definition the Mark II store uses on the same LiteSPI mapping, so the STOP condition does not hold.
Validation (rc 0 each, at this head unless noted; CPython 3.12.3; pinned Verilator 5.050 for suites):
- `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test`: "OK across 5 shape(s), and every planted defect reddened".
- `make -C tb/verilator/nvm_cosim run`: 465/465, 39/39 mutants killed.
- `python3 sw/builder/test_builder.py --require-rv32` and `--require-elaboration --require-rv32`: each "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11, a local implementation tree).
- `python3 scripts/check_nvm_capture.py`: PASS; its four `--mutation` arms exit 1.
- `make -C tb/verilator/fw_service_budget`, and the record-space gate with `--self-test`.
- Local step replicas: docs.yml 81/81; rtl-fast firmware-unit 7/7, including `test_ctrl_nvm.py --require-rv32` with its power-cut sweep, 435 tests; lint/BDD 5/5 (the last two at `7b714334`, whose inputs are unchanged here).
- The act replica was not run: it needs an open PR.
Capture (all six arms, at `7b714334`, firmware sha256 `3b9468ee`): 8x8 contract maximum 13.86328 ms against the 24.5 ms limit, margin 10.63672 ms (3.5345x the floor; previously 13.86484). 1x1 maximum 3.96548 ms (12.3566x). Census unchanged.
Firmware size: text +1,680 B (15,476 to 17,156, product 1x1 headers), bss +8 B.
Acceptance criteria:
1. Met in the firmware host tests. 202 read-fault cases per shape: the valid slot in A and in B, at SEQ 1, 0x5A5A5, 0x80000000 and 0xFFFFFFFF, faults walked over every boot read. Each runs a change, its commit and a clean reboot; the change survives, or the writer held and persisted nothing. The base firmware reproduces the loss in the same model.
2. Met. `restart_at_zero` fails by name ("the change committed after the faulty boot was lost on the clean reboot"), as do `unbounded_retry` ("over the bound of 13"), `generation_from_refused_slot` and `verdict_only_agreement`.
3. Met. The A/B write path is unchanged, and the existing A/B checks, `nvm_cosim` and the Mark II power-cut suite pass.
Open risks/questions:
- A fault that returns the same wrong bytes twice (or reads all 0xFF twice) is indistinguishable from a refusal or a blank slot. This is the Mark II store's stated limit too, stated in both READMEs; hence "Relates to #671", not "Closes".
- A held writer reads as retired on the register face; the console names it.
- Boot time is estimated, not re-measured: three container reads nominal instead of about five passes, twelve at worst (about 2.5 s at 8x8 against #397's 20 s).
- dev moved to `f88df731` (docs only); the trial merge is clean.
