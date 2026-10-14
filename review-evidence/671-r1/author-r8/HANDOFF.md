[A592]

# HANDOFF: lane for #671 (a boot read fault must leave saved-state authority unknown)

Status: Round 8 REVIEW READY at `d5cd863561ba1ee7bc6342fb1b00f57dd786bd97` (see Round 8 at the end). Earlier sections preserve historical evidence at their named heads.

- Branch `671-read-fault` from dev `e8454e27` (merge-base confirmed). Remote `https://github.com/kebag-logic/milan-fpga.git` (confirmed).
- Assignment: #671 comment 6098494890. TAKEN posted: 6098611315. REVIEW READY posted: 6100491164 (head `f54dbe3e393e2b1b027f1825c4acb736cf502cda`).
- Commits: `8d93a60d` (firmware, host read-fault model, checks 13 and 14, cosim statics), `5a9f523a` (docs), `7b714334` (host model idiom fix; the measured commit), `f54dbe3e` (capture receipt and section 18).

## Read-path evidence: the STOP condition does not hold

The shipping writer reads a slot through `nvm_slot()` (`sw/firmware/milan_baremetal/milan_baremetal.c:493`), a pointer into the memory-mapped QSPI window (`SPIFLASH_BASE`). That load always returns bytes, and nothing reports a failed read. The Mark II store reads the same window the same way: `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c:185-196`, where `ls_read` returns 0 for any in-range read. Its README says the port's read and refusal faults "do not reach memory-mapped LiteSPI reads" (`sw/firmware/ctrl_nvm/README.md:380`).

So the shipping path observes a media read fault only one way: two reads of one slot that return different bytes. That is exactly the definition the Mark II rule uses (#665 round 4 item 1, comment 5999350068; `ctrl_nvm/README.md` Boot item 3). Under that definition the path can observe a fault, so I proceeded rather than STOP. The limit is stated, not hidden: a fault that returns the same wrong bytes on two reads is indistinguishable from a refusal of those bytes, in both stores (`ctrl_nvm/README.md` "What this does not prove"; `sw/firmware/nvm_hosttest/README.md` "What this suite does NOT prove").

## Where the shipping path derives the authoritative sequence (at head)

Firmware, `sw/firmware/milan_baremetal/milan_baremetal.c`:

| line | what |
|---|---|
| 459 | `nvm_seq`, the authoritative sequence (RAM) |
| 719 | `nvm_seq_of()`: the sequence word of a container |
| 731-756 | `nvm_read_slot()`: one read into the stage; line 752 takes the sequence from the staged bytes only after `VD_OK` |
| 775-800 | `nvm_judge_slot()`: the standing verdict and its sequence, at most `NVM_READ_TRIES` reads; UNREAD gives `VD_LEN` and sequence 0 |
| 807-820 | `nvm_restage()`: the picked slot again, accepted only under the sequence it was picked by |
| 1474-1482 | `nvm_pick_slot()`: the wrap-safe compare, A on a tie |
| 1643-1667 | `nvm_boot()`: sequences from the judged reads, the pick, the re-stage loop, `nvm_seq` = the picked slot's or 0, `nvm_auth_slot` |
| 909-913 | `nvm_publish()`: publishes `nvm_seq` to `PP_NVM_SEL` word 2 |
| 1377, 1423-1425 | `nvm_commit()`: `next = nvm_seq + 1`; only a verified, byte-matched commit moves `nvm_seq` and `nvm_auth_slot` |
| 1920-1925 | `nvm_print_status()`: re-validates both slots from flash for the console only; never feeds `nvm_seq` (display, unchanged) |

Before this lane, `nvm_boot()` validated each slot straight from flash, then re-read the sequence word with a second, unvalidated read (`nvm_seq_of(nvm_slot(X))`). It then copied the chosen slot a third time into the window (`nvm_fill_window()` read flash). The sequence and the loaded bytes were therefore not the bytes that were validated.

Parent backend, `hdl/milan/KL_nvm_backend.sv`: `seq_r` (439) is written only from the CSR (`R_SEQ_C`, 424 and 490) and read back (582). It stores the firmware's published value and derives nothing.

Processor, as the parent instantiates it (`protocol-processor` at `2ad2f845`). The chain:

- `hdl/milan/KL_pp_shadow.sv:997` instantiates `KL_nvm_backend`, and `:1079` instantiates `protocol_processor_top`.
- `protocol_processor_top.sv` instantiates the binding manager `KL_acmp_nvm_shadow` (`:2741`), `KL_pp_nvm_mgr_arb` (`:2851`), `KL_pp_nvm_port` (`:2899`) and `KL_aecp_engine` (`:3733`).
- `KL_aecp_engine.sv:2001` instantiates the D3 writer `KL_aecp_nvm_writer`.

What each of them carries:

- `hdl/aecp/KL_aecp_nvm_writer.sv` and `hdl/packet_engine/KL_pp_nvm_port.sv` work per record (WRITE/ERASE/READ of one F07.8 frame). They carry no generation counter: no `seq` identifier exists in either file, nor in `KL_pp_nvm_mgr_arb.sv` or `KL_acmp_nvm_shadow.sv`.
- The `seq` ports in `hdl/top/protocol_processor_top.sv` are AECP/ACMP sequence ids.

So no processor change is needed, and there is no parent adoption.

## Changes

Firmware, `sw/firmware/milan_baremetal/milan_baremetal.c` (73,500 B, sha256 `3b9468ee...`; base `a73ecc25...`):

| file:line | change |
|---|---|
| 366 | `NVM_READ_TRIES` = 3: the read bound, the Mark II store's |
| 407-415 | `struct nvm_read`: verdict, sequence (0 unless VD_OK), CRC-32 digest and byte count of one read. A compile-time check that the 64 KiB stage holds the longest container rule 3 admits |
| 473, 476 | `nvm_unread` (bit per slot) and `nvm_read_faults` |
| 635-649, 657-669 | `nvm_validate_head()` (rules 1 to 3 on the 40 header bytes) factored out of `nvm_validate()`; the order and the verdicts are unchanged |
| 731-756 | `nvm_read_slot()`: one read into the private stage, the header first, the rest only when the header does not decide; judged there; digest for a refusal; sequence for VD_OK |
| 759-762 | `nvm_reads_agree()`: verdict, digest and length |
| 775-800 | `nvm_judge_slot()`: OK stands on one read; any other verdict, BLANK included, only on two reads with the same bytes; three reads, then UNREAD (`VD_LEN`, no sequence, bit set) |
| 807-820 | `nvm_restage()`: the picked slot again, VD_OK under the picked sequence, three tries |
| 1530-1537 | `nvm_fill_window()`: the window is filled from the stage, never from a fresh flash read |
| 1558-1584 | `nvm_unread_name()`, `nvm_go_live()`: the writer goes live, or is HELD (`nvm_retired`: no capture, erase, write or heartbeat) with a console line |
| 1638-1667 | `nvm_boot()`: judged reads, the pick, the re-stage loop (an unread pick offers the other) |
| 1690, 1726 | the two arming sites call `nvm_go_live()` |
| 1750-1760 | the boot line gains `; read faults=N unread=M` at its end |
| 1934-1935, 1969-1976 | `milan_nvm` prints "writer HELD"; `milan_nvm commit` is refused while held |

Unchanged on purpose: the A/B write sequence (`nvm_commit()`), the record format, the register map (no new CSR word or bit), `nvm_capture()` and the console's `nvm_print_status()` re-validation (display only).

Host model, `sw/firmware/nvm_hosttest/`:

- `stubs/generated/mem.h:9`: `SPIFLASH_BASE` is `nvm_host_flash_base()`, so every read the firmware opens through the mapping is a host call.
- `stubs/nvm_host.h:23`: its declaration.
- `nvm_host.c:161-189` (`struct read_fault`, the 16 MiB view, counters, `READ_STORM`), `512-536` (`nvm_host_flash_base()`), `540-571` (`arm_read_fault()`: `--read-fault SLOT:OFF:SKIP:COUNT[:BASE]`, `--read-ff SLOT:SKIP:COUNT`), `788` (`boot_reads`), and the summary fields `reads=`, `boot_reads=` and `faulty_reads=`.

Checks, `sw/firmware/nvm_hosttest/test_nvm_firmware.py`: `READ_FAULT_MUTATIONS` (149), `FAULT_SEQS`, `FAULT_WINDOWS` and `BOOT_READ_BOUND` (177-182), `fault_cases()` (627), `grade_read_faults()` (650, check 13), `grade_refused_generation()` (743, check 14), `WRITER_GRADES` and `READ_FAULT_GRADES` (777-782), and the self-test of the four plants (811-826).

Co-simulation restart model, `tb/verilator/nvm_cosim/run_cases.py:186`: the two new statics join `WRITER_STATICS`. Its guard refuses a writer static that the CPU-only reset model does not name.

Docs:

- `docs/design/SAVED_STATE_FASTCONNECT.md` section 7: "A slot that could not be read is not a slot that failed section 6.2".
- `docs/integration/BAREMETAL_FIRMWARE.md`: the Boot paragraph and "What is proved".
- `sw/firmware/nvm_hosttest/README.md`: the model, checks 12 and 13, the nine controls, the limit.
- `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 18 and section 20 item 6, refreshed from the new capture receipt `tb/verilator/nvm_capture_cpu/measurements.json` (`f54dbe3e`).

## Tests and the planted defects they catch

All tests below are in `sw/firmware/nvm_hosttest/test_nvm_firmware.py`, and run per shipped shape (5).

Check 13, `grade_read_faults()` (#671 acceptance 1). One slot is valid and the other blank, both orientations, at SEQ 1, 0x5A5A5 (far above 1), 0x80000000 and 0xFFFFFFFF (the wrap value). Three fault families are each walked over windows SKIP 0-5 × COUNT 1-3, plus one whole-boot window: one byte of the valid slot's header or sequence word XORed differently on every faulty read; the blank slot's first byte; an all-0xFF read of the valid slot. That is 202 cases per shape. Each case:

1. faulty boot, a real change (the last name record), a 1,500 ms idle so the debounce commits, slots dumped;
2. clean reboot.

The change must survive, or the faulty boot must have HELD: no erase, program, START or ACK, no heartbeat, `backed=0`, `dirty=1`, the unread slot named on the boot line, and the clean reboot restoring the saved value. A held case then runs on through a second change, its commit and a third boot, which must restore that change. Further assertions:

- COUNT 1 never holds;
- the whole-boot fault on the valid slot always holds;
- `boot_reads` ≤ 13;
- a held writer refuses `milan_nvm commit` and prints "writer HELD".

Check 14, `grade_refused_generation()` (no generation from unvalidated bytes). A cleanly refused slot (foreign entity, or bad CRC) at header SEQ 0x5A5A5, in A or in B, with the other blank:

- the boot line reports seq 0 for it;
- the first commit is at SEQ 1.

Planted controls (#671 acceptance 2), each in `READ_FAULT_MUTATIONS` and required to be caught by a finding carrying its own words:

| plant | defect | caught by (first finding, 1x1 and arty_4x4 runs) |
|---|---|---|
| `restart_at_zero` | `if (!nvm_unread)` -> `if (1)`: an unread slot no longer holds; the sequence restarts at 0 | "slot A valid at seq 0x1, --read-fault a:0:0:64:8: the change committed after the faulty boot was lost on the clean reboot" (10 named findings) |
| `unbounded_retry` | the judge loop's bound removed | "the boot read the flash 68 times, over the bound of 13" (10) |
| `generation_from_refused_slot` | the sequence kept for refused reads, and `nvm_seq = max(seq_a, seq_b)` when none is accepted | "slot A refused (foreign entity): a generation was taken from a refused slot: the boot line reports ... seq 370085" (8) |
| `verdict_only_agreement` | two reads agree by verdict only (R501-3's probe on #665) | "... was lost on the clean reboot" (12) |

The five earlier plants (`edge_cross`, `no_ascending_check`, `no_heartbeat_in_wait`, `verify_skipped`, `erased_header_only`) are still caught by checks 1-11. The boot-walk and disabled-writer plants are unchanged and still caught.

Reproduction on the base firmware (`e8454e27`) with the same host model, from a scratch probe in this lane's scratch area, 1x1 shape:

- B valid at 0x5A5A5 or 0x80000000 with a whole-boot fault on B: the base commits the change to A at SEQ 1, and the clean reboot offers B, so the change is lost.
- A valid with a whole-boot fault on A: the base erases A, its commit then fails, and both slots boot blank, so the saved state and the change are both lost.

On this head the same cases hold the writer, erase nothing, and the clean reboot restores the saved state. The defect is real in the shipping writer, as #671 says.

## Boot-time budget (estimate, not re-measured)

The boot budget the repository grades is "boot to entity enabled" against the 20,000 ms ADP comparison of #397 (`docs/findings/397_SERVICE_BUDGET.md`). It measured 378 ms at 1x1 and 1,111 ms at 8x8 with both slots populated, at the old firmware `a73ecc25`.

The memory-mapped flash read costs about 15.5 µs per byte. That comes from the same page's 1x1 `milan_nvm` duty: 238.97 ms, of which about 35 ms is UART output, for about 13,100 byte reads (two slots, each walked twice).

- One container read is therefore about 52 ms at 1x1 (3,336 B) and about 205 ms at 8x8 (13,256 B).
- Old boot, both slots valid: about five container passes through the mapping (each slot walked twice, plus the window copy).
- New boot, both slots valid: three reads (A, B, re-stage), with validation done in DRAM. Fewer flash bytes are read, so the nominal boot gets shorter.
- New worst case, every read of a valid-length container faulty: 12 container reads, about 2.5 s of flash at 8x8, plus DRAM-side validation. That still leaves the 20 s comparison with wide margin.
- A pathological header claiming 65,536 B costs up to six 64 KiB reads (two slots × three), about 6 s. Verdict parity needs every byte for the CRC, as in the Mark II store.

The 20 s budget itself is unchanged. The #397 service receipt is bound to the old firmware digest and was not re-measured here; it is outside this assignment. See Open risks.

## Capture re-measure and firmware size delta

Re-measured with the harness's own recipe (`tb/verilator/nvm_capture_cpu/README.md` "Run"): `unshare -Urn "$PRODUCT_PYTHON" -B tb/verilator/nvm_capture_cpu/run.py --shape S --cpu-hz F --captures 16 --traffic on|off --build-dir <scratch>`.

- Environment: PYTHONHASHSEED=0, offline, LITEX_ENV_CC_TRIPLE=riscv32-linux, Verilator 5.052 as the receipt records.
- Measured commit `7b714334` (tree `a90192e8`), firmware sha256 `3b9468ee...`, protocol-processor pin `2ad2f845`.
- All six arms, at most two builds at once. The census is unchanged (`measured_for` identical); the CPU netlist and gPTP microcode digests are unchanged; the BIOS digests changed with the firmware. The 8x8 config digest differs from the old receipt because `configs/endstation_ax7101_8x8.yaml` changed on dev since `a2f17342`; its census did not.
- Receipt assembled by a scratch script that takes each arm's `measurement.json` verbatim and recomputes `measured_for`, the harness hashes and the maxima through `scripts/check_nvm_capture.py`'s own functions. It ends with that gate's `check_receipt`.
- `tb/verilator/nvm_capture_cpu/measurements.json`: 36,763 B, sha256 `0e9cd2fa868bad11018448ba3fc67784199d26c3a641760c6b5ba04cee1f8541`.

| shape | CPU MHz | traffic | min ms | max ms | 49 ms / max | previous receipt (max) |
|---|---|---|---|---|---|---|
| 1x1 | 50 (contract) | ON | 3.96020 | 3.96548 | 12.3566x | 3.96728 |
| 1x1 | 50 (contract) | OFF | 3.90676 | 3.92034 | 12.4989x | 3.91182 |
| 8x8 | 50 (contract) | ON | 13.84828 | **13.86328** | 3.5345x | 13.86484 |
| 8x8 | 50 (contract) | OFF | 13.67538 | 13.68956 | 3.5794x | 13.69390 |
| 8x8 | 100 (non-contract) | ON | 10.41950 | 10.43406 | 4.6962x | 10.42973 |
| 8x8 | 100 (non-contract) | OFF | 10.41246 | 10.41566 | 4.7045x | 10.41566 |

- **8x8 contract maximum: 13.86328 ms against the 24.5 ms limit (half the 49 ms hold floor). Margin 10.63672 ms, 3.5345x the floor.**
- 1x1 maximum: 3.96548 ms, margin 20.53452 ms, 12.3566x.
- `nvm_capture()` is unchanged, and the figures move by under 0.01 ms. That is consistent with code layout only.
- The capture SoC also ran the new boot path on the product CPU netlist: every arm's `capture.log` has the boot line ending `read faults=0 unread=0`, with two blank slots.
- `python3 scripts/check_nvm_capture.py`: rc 0, "PASS: capture census, clocks, both timing arms and receipt agree". Its `--mutation bytes|records|clock|ignore-off-timing` each exit 1.
- Section 18 and section 20 item 6 of `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` were refreshed from the receipt by a scratch script. Each old sentence was matched exactly once against the receipt at HEAD.

Firmware size delta, product compiler (`riscv32-linux-gcc` 14.3.0, Buildroot 2026.05). The object was compiled by LiteX's own `$(compile)` rule from `sw/firmware/milan_baremetal/Makefile`, base `a73ecc25` against head `3b9468ee`, in scratch, with each build's generated headers:

| headers | text | data | bss |
|---|---|---|---|
| product 1x1 build tree (PHY path compiled in) | 15,476 -> 17,156 (**+1,680**) | 104 -> 104 | 88 -> 96 (+8) |
| capture 1x1 build (PHY path compiled out) | 14,473 -> 16,169 (+1,696) | 104 -> 104 | 68 -> 76 (+8) |

The BIOS ROM is 0x20000 (131,072 B). The product 1x1 `bios.bin` at a recent dev build is 52,988 B, so +1.7 KB leaves about 76 KB free. Stack: `nvm_judge_slot()` holds three 16-byte `struct nvm_read` values.

## Gate table

Every command was run in the foreground or as a tracked background job, never piped. rc is the command's own exit status. Python is CPython 3.12.3 in a scratch venv carrying the workflows' pinned pip requirements, unless a row says otherwise. Verilator suites use the pinned 5.050.

Heads:

- `f54dbe3e` is the receipt commit.
- `7b714334` is the measured commit. Between the two, only `measurements.json` and SNAPSHOT_OWNERSHIP section 18 changed; no row run at `7b714334` reads either.

| Gate | Command | Head | rc | Result |
|---|---|---|---|---|
| Saved-state writer gate (host), all shapes and plants | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | f54dbe3e (replica step 39); also 8d93a60d | 0 | "saved-state writer gate: OK across 5 shape(s), and every planted defect reddened"; 9 writer plants plus 2 boot-walk plants and the disabled-writer plant caught; the 4 #671 plants by their named findings |
| Builder bank, RV32 required | `python3 sw/builder/test_builder.py --require-rv32` | f54dbe3e (replica step 35) | 0 | "ALL GATES PASS EXCEPT 1 NOT RUN"; gate 11 needs a local mf48 implementation tree, the same skip as the dev baseline. Gate 1b's compiled census and resolver ran on the new firmware |
| Builder bank, elaboration (elaborate.yml) | `python3 sw/builder/test_builder.py --require-elaboration --require-rv32` under the product LiteX venv | f54dbe3e | 0 | "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11, as above) and "--require-elaboration: an interpreter carrying the patch series was found and no elaboration arm was skipped for a toolchain reason"; 26 min 42 s |
| Service-budget self-test | `make -C tb/verilator/fw_service_budget` (pinned Verilator 5.050 on PATH) | `1d517428` | 0 | flash 14/0, oracle 55/0, "PASS: over-budget duty, marker integrity and product dispatch census" |
| Co-simulation of the shipping writer and backend | `make -C tb/verilator/nvm_cosim run JOBS=2 POOL=4` (pinned Verilator 5.050) | `1d517428` (its inputs equal `fc0c517c`'s) | 0 | "nvm_cosim: 465 checks: 465 PASS, 0 FAIL (0 not expressible)", "39 of 39 mutant(s) killed by their named check"; 701 s. W1 to W4 build with `writer_restart.host_restart`, the moved model |
| rtl-fast changes, lint, BDD replica | `scripts/r3/rtl_fast_other_replica.sh` (round 2's): `ci_scope.py --selftest`, pinned Verilator `--version`, `lint_rtl.py --check --self-test`, `pp_srcs.py --check --selftest`, `behave` | `fc0c517c` | 0 | 5/5 |
| Record-space gate | `python3 scripts/check_nvm_record_space.py` and `--self-test` | `fc0c517c` | 0, 0 | 0 findings across 5 configs |
| docs.yml replica (includes the builder bank `--require-rv32`, the capture gate, the writer gate `--self-test`, the idiom, hygiene, test-evidence and TODO ratchets) | `scripts/r3/docs_check_replica.sh` (round 2's; em-dash base `e8454e27`) | `fc0c517c` | 0 | 81/81 steps rc 0, 2,198 s (`receipts/r3/docs_replica.log`). The builder bank: "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11). The writer gate: "OK across 5 shape(s), and every planted defect reddened". The capture gate: PASS |
| Capture re-measure, six arms | `tb/verilator/nvm_capture_cpu/run.py` via `scripts/r3/capture_driver.sh` | `4886f231` | 0 x 6 | the table in "Capture re-measure (round 3)" |
| Capture gate | `python3 scripts/check_nvm_capture.py` and its four `--mutation` controls | `fc0c517c` | 0; 1 x 4 | "PASS: capture census, clocks, both timing arms and receipt agree"; every control detected |
| Docs gates after the receipt | `scripts/docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, `check_em_dash.py --base e8454e27` | `fc0c517c` | 0 x 4 | em-dash 0 over 234 added lines |
| Co-simulation of the shipping writer and backend | `make -C tb/verilator/nvm_cosim run` (JOBS=2) | f54dbe3e | 0 | "nvm_cosim: 465 checks: 465 PASS, 0 FAIL", "39 of 39 mutant(s) killed by their named check" |
| Service-budget suite self-test | `make -C tb/verilator/fw_service_budget` | f54dbe3e | 0 | flash 14/0, oracle 55/0, dispatch census PASS |
| Capture census and receipt | `python3 scripts/check_nvm_capture.py`; `--mutation bytes`, `records`, `clock`, `ignore-off-timing` | f54dbe3e | 0; 1 ×4 | "PASS: capture census, clocks, both timing arms and receipt agree"; every mutation refused |
| Capture re-measure, six arms | `tb/verilator/nvm_capture_cpu/run.py` (product venv, Verilator 5.052) | 7b714334 | graded | the table above |
| NVM record-space gate | `python3 scripts/check_nvm_record_space.py` and `--self-test` | f54dbe3e | 0, 0 | 0 findings across 5 configs |
| docs.yml replica (docs-check, wire-accountability, docs-check-no-git) | `docs_check_replica.sh` (scratch) | f54dbe3e | 0 | 81/81 steps rc 0, 40 min; em-dash base `e8454e27` = merge-base with live dev `f88df731` |
| rtl-fast firmware-unit replica | `firmware_unit_replica.sh` (scratch): tally self-test, SDK self-test, RV32 self-test, `test_ctrl_firmware.py --require-rv32 --self-test`, `test_ctrl_nvm.py --require-rv32`, coverage self-test and check | 7b714334 | 0 | 7/7. The A/B power-loss suite: "saved-state store gate (#665 F1): OK across 5 shape(s), 435 tests", power cut included. Coverage PASS |
| Builder bank, elaboration (elaborate.yml) | `python3 sw/builder/test_builder.py --require-elaboration --require-rv32`, product LiteX venv, offline (`scripts/r2/product_env.sh`) | `4886f231` | 0 | "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11, needs the local mf48 tree); "no elaboration arm was skipped for a toolchain reason"; the writer gate `--self-test` inside it: "OK across 5 shape(s), and every planted defect reddened"; 1,417 s |
| rtl-fast changes, verilator-lint and bdd replica | `ci_scope.py --selftest`; `lint_rtl.py --check --self-test` (Verilator 5.050); `pp_srcs.py --check --selftest`; `behave` in `tests/` | 7b714334 | 0 | 5/5 |
| Idiom and hygiene ratchets | `check_cpp_idiom.py`, `check_py_idiom.py`, `check_sh_idiom.py`, `check_hygiene.py --check`, `measure_test_evidence.py --check`, `check_todo_ownership.py` | f54dbe3e (in the replica) | 0 | C idiom: one multi-declarator line my first draft added was fixed in 7b714334 |

Not run, with the reason:

- `scripts/act_ci.py --pr N` (the act replica): it needs an open pull request, and this lane may not create one. The local step replicas above stand in for the four workflows' touched jobs. The hosted and act runs remain owed once a PR exists.
- `act_ci.py --selftest` (a docs-check step): the candidate's runner may self-test only inside the disposable CI job. The file is byte-identical to dev.
- `make -C gptp-processor docs` (a docs-check step): it writes into the submodule checkout, and nothing under `gptp-processor` changed.
- `scripts/ci_rv32_sdk.py --destination` (install step): the pinned SDK is already installed, and its self-test ran.
- rtl-fast `yosys-elaboration`, and rtl.yml's exhaustive `verilator-suites` and `yosys-portability`: no file under `hdl/`, `syn/` or any submodule changed. The only Verilator suites that read a changed file are `nvm_cosim`, `fw_service_budget` and `nvm_capture_cpu`, all run above. `tb/verilator/milan_dp/sim_nxn.cpp` names the firmware in a comment only.
- elaborate.yml `scripts/run_litex_sims.sh`: its five LiteX simulations read no changed file.

Environment differences from hosted CI: sv2v v0.0.13 locally against the pinned v0.0.12; system GoogleTest 1.18; the product venv (CPython 3.14.7) for the capture and the elaboration builder, as in the earlier re-measures.

## Open risks

1. **The detection limit.** A read fault that returns the same wrong bytes on two reads is a refusal of those bytes; a slot read as all `0xFF` twice reads blank. Either can still let the next commit restart the sequence below a surviving container. This is inherent to a read path that cannot report a failure, and it is the Mark II store's stated limit too. Check 12 grades faults that differ from read to read, and single all-0xFF reads. Reviewers decide whether #671 accepts it, which is why the PR says "Relates to".
2. **A held writer reads as retired** on the register face (`nvm_backed` 0, never stale on a cold boot). Only the console names the hold. The register map was frozen for this lane.
3. **Boot time is estimated, not measured** (see above). The #397 service receipt still describes firmware `a73ecc25`.
4. **The writer-restart path.** A CPU-only restart on a live backend also re-judges the slots without heartbeating. Under heavy read faults at 8x8 this could take about 2.5-3 s, longer than T-NVM-WRITER-ALIVE (2 s). The fabric would then revoke `nvm_backed` and set `nvm_stale` until the next commit: an honest loss report, not a false claim. Before this lane that boot read about 1 s of flash.
5. **An observation outside the sequence path, not changed.** `nvm_prefill_stage()` re-reads the authoritative slot from flash at every capture, so a transient fault there lands in an open record's prefilled bytes. Each record's crc16 makes `nvm_validate(NVM_STG)` defer such a commit, but the alignment pad bytes are not judged. A candidate follow-up issue.
6. **dev has moved** to `f88df731` (#709, one new findings page). The trial merge with `git merge-tree` is clean and touches nothing of this lane. Not merged here, since merging was not asked for.

## Round 2

Status: REVIEW READY at `9112a0df27acc1381091845e94d8eaa1407f1bbb` on `671-read-fault`, seven new commits on `f54dbe3e` (no rebase or amend; not pushed). An external usage-limit stop at 21:06 cut the first session of this round. Its commits `ebe13029`, `a58f7af9`, `d9443b8f`, `c94c9776` and `822d25de` were kept. Every gate whose result it had not recorded was re-run here.

- REVIEW READY (round 2) posted: #671 comment 6102799749 (text in `receipts/r2/review_ready_comment.md`).
- Assignment: #671 comment 6100704879. Reviews answered: PR #715 comments 6100699429 (R602-1, NEGATIVE on one MINOR) and 6100671345 (R603-1, NEGATIVE on one MAJOR).
- The reviewers' probes were read as data, never executed, from `origin/671-review-evidence` at `9b1d6b7b` (`review-evidence/671-r1/reviews/R602-1/` and `R603-1/`).

### Commits of this round

| commit | what |
|---|---|
| `ebe13029` | firmware: `nvm_held`, set only where the writer would have gone live with a slot unread; the console's status and its commit refusal name the hold only then; the read-fault counter is documented as a floor (R602-1-S1); `run_cases.py` names the new static |
| `a58f7af9` | firmware comments: the operator's wipe while held; what the unread and held flags mean on a retire path |
| `d9443b8f` | check 13 rebuilt (record-area faults, both slots valid across the wrap, the other slot's container on a re-stage, every saved record kept, boot line, offer and window graded), five new named controls on three shapes, `--read-other`, `--jobs` |
| `c94c9776` | check 13 grades a faulty boot whose line carries no unread tally, instead of stopping at it |
| `822d25de` | docs: R1 residue (FASTCONNECT 7), the wipe while held, a retire's own cause, the slot-read lengths behind the boot bound |
| `49d28e5a` | check 13's console check covers every retire cause the reviewer named (`--boot-backend contract|over|live`), not only refused loads |
| `9112a0df` | capture receipt re-measured at the round-2 firmware; SNAPSHOT_OWNERSHIP section 18 and section 20 item 6 refreshed, with the R3 residue |

### The items and where each is answered

| Item | Source | Answer |
|---|---|---|
| 1. check 13 can fail for every mechanism the fix depends on | R603-1-F1, R602-1-S2 | done: see "Check 13 now" and the control table |
| 2. boot worst case with length-word faults, labelled an estimate; writer-restart note | R602-1-F1, R603-1-F2 | done, with per-read costs MEASURED on the product CPU; see "Boot worst case" |
| 3. the console names the real cause on the retire paths | R603-1-S2 | done: `milan_baremetal.c:477`, `:1588`, `:1942`, `:1980`; checked for all four causes |
| 4. the docs say `milan_nvm wipe` still erases both slots while held | R603-1-S1, R602-1-S3 | done: `docs/integration/BAREMETAL_FIRMWARE.md:2038-2041`, `milan_baremetal.c:1576-1577`, `sw/firmware/nvm_hosttest/README.md:119-120`; the wipe is checked (`test_nvm_firmware.py:804`) |
| 5. residue R1, R3, R4, renumbering | R602-1 R1-R4, R603-1 R1 | R1 `SAVED_STATE_FASTCONNECT.md:785-787` (exact text); R4 `nvm_hosttest/README.md:94-100`; renumbering `nvm_hosttest/README.md:11, 90, 92, 123, 143-144, 208`; R3 `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1651` (exact text, `9112a0df`) |
| 6. optional | R602-1-S1, R603-1-S3 | both taken: the counter is documented as a floor, as in `ctrl_nvm` (`milan_baremetal.c:478-481`); the other slot's container answers re-stage reads (`--read-other`) and `r_restage_any_seq` is a control |

### Changes (file:line at `49d28e5a`)

Firmware, `sw/firmware/milan_baremetal/milan_baremetal.c` (sha256 `33eaa0c3...`):

| file:line | change |
|---|---|
| 470-482 | `nvm_unread` restated; `nvm_held` added; `nvm_read_faults` documented as a floor |
| 1573-1580, 1588 | `nvm_go_live()`: the operator's wipe stated; `nvm_held = 1` where the writer is held |
| 1942 | `milan_nvm` prints "writer HELD" only when held, otherwise "writer retired" or "writer disabled" |
| 1980 | `milan_nvm commit` names the unread slot only when held; a retired writer gets the existing refusal |

Unchanged: `nvm_commit()`, `nvm_capture()`, the read, judge, re-stage and fill paths of round 1, the record format, the register map.

Host model, `sw/firmware/nvm_hosttest/nvm_host.c`:

- 161-186: a third fault mode, the slot read as the other slot's bytes (an address fault).
- 191-195, 481: `PP_NVM_STAT[31:24]` comes from `stat_tag`.
- 544-545: the faulty view in that mode.
- 551-578: `arm_read_fault()` takes the mode.
- 838-839: `--read-other SLOT:SKIP:COUNT`.
- 847-858: `--boot-backend contract|over|live`, which selects the retire paths a cold boot of the model never takes: an older contract tag, the boot load ended with none accepted, the restore walk already sequenced.

`sw/firmware/nvm_hosttest/read_fault_cases.py` (new):

- 19-77: `READ_FAULT_MUTATIONS`, the nine #671 controls.
- 81-92: the sequences, both-valid sequences, re-stage windows and the read bound.
- 99: `FaultCase`.
- 127: `fault_cases()`.
- 161: `judged()`, the boot line's verdicts against what each slot's bytes say.
- 184: `offer()`, the offer the line's accepted slots make.

`sw/firmware/nvm_hosttest/test_nvm_firmware.py`:

- 165: `PRODUCT_SHAPES`; 168: `RETIRE_CAUSES`.
- 623-655: `FaultRun` and `fault_run()`. The older container differs from the newer in its last two names.
- 657: `restored()` counts every other saved record.
- 667: `boot_findings()`: the line, the offer, and the window byte for byte.
- 691: `reboot_findings()`, which requires every other saved record to survive (709, 713, 723).
- 727: `grade_fault_case()`; 765: `grade_read_faults()`, on `--jobs` threads, stopping at a named finding for a control.
- 804: `grade_hold_console()`: the held commit refusal, the wipe while held, and each retire cause.
- 905: `replant()`; 913: `self_test_read_faults()`.
- 949: `--jobs`; 974: the controls are planted on the first shape and both product shapes.

`tb/verilator/nvm_cosim/run_cases.py:186`: `nvm_held` joins the restart model's statics.

Docs:

- `docs/design/SAVED_STATE_FASTCONNECT.md:785-787`: R1.
- `docs/integration/BAREMETAL_FIRMWARE.md:2038-2051`: the wipe while held, a retire's own cause, the read lengths behind the twelve-read bound. `:2158-2164`: the host suite.
- `sw/firmware/nvm_hosttest/README.md`: the model, items 12-14, the control table, the limit.

### Check 13 now

There are 446 cases per shape, 2,230 across the five:

- One slot valid, the other blank, both orientations, at 1, 0x5A5A5, 0x80000000 and 0xFFFFFFFF. A header or sequence byte and a record-area byte of the valid slot (the middle of the area, refused only by the CRC over every byte read) are each walked over 19 windows. That makes 304 cases, plus 38 on the blank slot and 12 single all-0xFF reads.
- Both slots valid, both orientations. The newer is at 0x5A5A5, or at 0 with the older at 0xFFFFFFFF (the wrap), and the two differ in two names:
  - the newer slot faulted by its magic byte or a record-area byte over the 19 windows (76 cases);
  - the older faulted for the whole boot (4);
  - the newer's re-stage reads answered with the older's container, COUNT 1 to 3 (12).

Each case grades:

- the boot line: each slot as its bytes read, or UNREAD;
- the offer the line's own accepted slots make;
- the window, byte for byte that slot's container, or the blank image;
- after the faulty boot's change, commit and a clean reboot: every saved record plus the change, or a hold that persisted nothing and a reboot that restores every saved record.

Then a held case's recovery, the read bound, and the console checks (held commit refused, wipe while held, four retire causes).

### Controls and the defects they catch

All nine are planted on `endstation_arty_4x4`, `endstation_ax7101_1x1_tdm8` and `endstation_ax7101_8x8`. Each is caught on every shape by a finding carrying its own words.

The counts are from a full run (no early stop) at `49d28e5a` (`scripts/r2/plants_full.py`). They are the same on all three shapes.

| control | defect | named findings | first named finding (8x8) |
|---|---|---|---|
| `restart_at_zero` | an unread slot no longer holds | 20 | "slot A valid at seq 0x1, --read-fault a:0:0:64:8: the change committed after the faulty boot was lost on the clean reboot" |
| `unbounded_retry` | the judge loop unbounded | 26 | "the boot read the flash 68 times, over the bound of 13" |
| `generation_from_refused_slot` | a refused slot's sequence continues the generation | 8 | "a generation was taken from a refused slot: the boot line reports ... seq 370085" |
| `verdict_only_agreement` | two reads agree by verdict only | 24 | "... was lost on the clean reboot" |
| `r_digest_header_only` | the refusal digest covers the 40 header bytes | 46 | "--read-fault a:6646:0:3:128: slot A was taken as VD_CRC on reads that returned different bytes" |
| `r_fill_from_flash` | the window filled by a fresh read, as before #671 | 62 | "--read-fault a:0:5:1:8: the window the boot loaded is not the container it judged: it reads VD_MAGIC" |
| `r_restage_fail_offers_none` | an unread pick offers nothing | 8 | "slot A newer at seq 0x5a5a5, the other older, --read-fault a:6646:3:3: ... the offer is B seq 0x5a5a4, yet the boot offered - seq 0x0" |
| `restage_fail_not_unread` | an unread pick is not marked UNREAD | 24 | "--read-fault a:11:4:3:128: slot A did not read back as it was judged, yet the boot line does not name it unread". The A-valid orientation R602-1-S2 found blind now catches it, with "163 other saved record(s) did not survive" alongside |
| `r_restage_any_seq` | the re-stage takes any VD_OK read | 12 | "--read-other a:3:1: the window holds another valid container than the one the boot offered (A), at seq 0x5a5a4" |

The five `r_` and `restage_` plants are byte-identical to the reviewers' (`scripts/r2/compare_plants.py`, which parses their probe files and never executes them). So the shipped `--self-test` re-applies R603-1's three plants, as its verification asked.

Two scratch plants show the console check reddening (`scripts/r2/console_plants.py`, 1x1, at `49d28e5a`):

- round 1's console logic: 4 findings, one per retire cause;
- a wipe refused while held: 1 finding.

The base firmware (`a73ecc25`), graded by this head's checks 13 and 14 (`scripts/r2/base_repro.py`), gives 645 findings on each product shape. 124 of them are "was lost on the clean reboot" and 109 are "other saved record(s) did not survive".

### Boot worst case (item 2)

**Reads.** A boot opens at most 13 reads: the AEM image, and three judgements and three re-stages per slot.

A judgement stands on the first OK read, so a slot can spend two refused reads before its third read stands OK. A read whose header passes tests 1 to 3 copies as many bytes as its length word names, up to the 64 KiB slot (`milan_baremetal.c:745-754`). A read fault on the length word therefore makes a refused read up to a slot long.

The most expensive boot is:

1. two refused slot-length reads, then an OK read, for each slot;
2. three refused slot-length re-stages of the newer slot;
3. three of the older.

That is **ten slot-length reads and two container reads**. Both reviewers counted six slot-length reads; they left out the two refused judgement reads that can come before each slot's standing OK.

**Cost per read, MEASURED on the product CPU.**

- Harness: the unchanged firmware runs in the `fw_service_budget` native simulator (`scripts/r2/boot_read_probe.py`): the cacheless RV32I CPU at 50 MHz, the product LiteSPI master, and the harness's 12.5 MHz single-lane flash model. Built at `49d28e5a`.
- Span: the first AEM flash read to the restore walk's start. It holds the AEM copy (the same in every fixture) and all of `nvm_boot()`.
- Fixtures: a slot either blank, valid (the harness's own container), or that container with its length word set to N. With length N, tests 1 to 3 pass, the read copies N bytes, and the CRC refuses it, twice, so the verdict stands on two reads.

| shape | fixture (A / B) | aem to walk, ms | boot to entity enabled, ms |
|---|---|---|---|
| 1x1 | blank / blank | 98.56765 | 132.09935 |
| 1x1 | length 8,192 / blank | 500.31299 | 533.80185 |
| 1x1 | length 8,192 / length 8,192 | 902.05767 | 935.52525 |
| 1x1 | length 65,536 / blank | 3,321.68297 | 3,355.29859 |
| 1x1 | valid / blank | 238.89793 | 273.33671 |
| 1x1 | valid / valid | 324.94139 | 359.36731 |
| 8x8 | blank / blank | 299.48014 | 334.20865 |
| 8x8 | valid / valid | 1,210.07570 | 1,247.27325 |

What the table gives:

- **A refused read costs 24.5 us per byte:**
  - 8,192 B: 200.873 ms from two reads, 200.873 ms from four (linear);
  - 65,536 B: 1,611.558 ms, measured directly.

  It copies each byte through the mapping, then runs two CRC-32 passes over the stage: one to judge, one for the digest.
- **An OK container read:**
  - 1x1: 86.04 ms per 3,336 B (valid/valid minus valid/blank);
  - 8x8: three OK reads plus the window fill come to 910.60 ms (about 303.5 ms per read).
- **The 15.5 us/B rate round 1 used does not apply.** It came from a loop doing one flash load and one CRC step per byte.

**The worst case, an ESTIMATE.** It is the sum of the measured per-read costs. A boot that faults ten reads in that pattern was not itself driven on the product CPU.

| shape | slot reads | boot to entity enabled | against #397's 20 s comparison |
|---|---|---|---|
| 1x1 | 10 x 1,611.6 + 2 x 86.0 = 16,288 ms | about 16.4 s (blank boot 132 ms plus the reads) | about 3.6 s margin |
| 8x8 | 10 x 1,611.6 + 2 x 303.5 = 16,723 ms | about 17.1 s (blank boot 334 ms plus the reads) | about 2.9 s margin |

The reviewers' 6.5 to 7.4 s is low for two reasons: the count above, and the measured cost of a refused read. The same rates price two other cases:

- **A stored header claiming the whole slot, with no fault at all**, costs two agreeing refused reads: 3.2 s per slot, measured. Before this lane it cost one validation pass.
- **The nominal boot with both slots valid:** three container reads, 0.26 s at 1x1 and 0.91 s at 8x8. Boot to entity enabled at 8x8 is 1,247.27 ms at this head with immediate UART. #397's receipt has 1,111.33 ms at the base firmware, with paced UART and older pins, which is not a controlled comparison. Round 1's statement that the nominal boot "gets shorter" was never measured and is withdrawn.

**The optional cap was not taken.**

- Capping a refused read at the shape's container length would bound the worst case near 12 x 13,256 B.
- But section 6.2's verdict for a header that passes tests 1 to 3 is decided by the CRC over the length the header names, then the entity, the shape and the records (`nvm_validate()`, `scripts/nvm_klj2.py` `klj2_decode`).
- A read stopped at the container length cannot compute that CRC. So a stored container whose length differs (another shape's, for instance) would be published with another verdict than the decoder's. That breaks the verdict parity the writer gate checks and changes the 6.2 order.
- That is a record-format change, which this lane may not make. The bound is restated above instead.

**Writer restart.**

- A CPU-only restart on a live backend runs the same boot path. It does not heartbeat until the writer goes live: `nvm_crc32()` and `nvm_validate()` tick only once `nvm_ready` is set.
- With both slots valid, its slot reads take about 0.26 s (1x1) and 0.91 s (8x8).
- Under the worst faults they take about 16.3 to 16.7 s, far past T-NVM-WRITER-ALIVE (2 s). One stored or faulted slot-length refusal alone costs 1.6 s.
- In that case the fabric revokes `nvm_backed` and sets `nvm_stale` if backing was ever claimed. That is an honest loss report, not a false claim. A held writer then claims nothing until reset.
- Round 1 put this at 2.5 to 3 s; the measured rates replace that.

### Firmware size delta, corrected

Round 1's size row was mislabelled. Its objects were built with the TRIPLE of the local product build tree's `variables.mak`, `riscv64-elf` (GCC 16.2.0), not with the pinned SDK's `riscv32-linux` (GCC 14.3.0) that HANDOFF and the PR named.

Both compilers, LiteX's own `$(compile)` rule, product 1x1 build-tree headers (`scripts/r2/fw_size.sh`, receipt `receipts/r2/fw_size.txt`):

| compiler | base `a73ecc25` text / bss | round 1 `3b9468ee` | round 2 `33eaa0c3` | delta, base to round 2 |
|---|---|---|---|---|
| `riscv32-linux` GCC 14.3.0 (pinned SDK, as the capture receipt builds) | 15,529 / 88 | 17,225 / 96 | 17,241 / 100 | text +1,712, bss +12 |
| `riscv64-elf` GCC 16.2.0 (round 1's actual compiler) | 15,476 / 88 | 17,156 / 96 | 17,172 / 100 | text +1,696, bss +12 |

Data is 104 B in every build. The BIOS ROM is 128 KiB, and the product 1x1 `bios.bin` at a recent dev build is 52,988 B.

### Capture re-measure (round 2)

All six arms were re-measured with the harness's own recipe (`scripts/capture_driver.sh`: `unshare -Urn "$PRODUCT_PYTHON" -B tb/verilator/nvm_capture_cpu/run.py --shape S --cpu-hz F --captures 16 --traffic on|off --build-dir <scratch>`), two at a time, 21:46 to 23:44, each rc 0.

- Measured commit `49d28e5a` (tree `891f5d32`), firmware sha256 `33eaa0c3...`, protocol-processor pin `2ad2f845`.
- Environment as round 1: PYTHONHASHSEED=0, offline, LITEX_ENV_CC_TRIPLE=riscv32-linux, Verilator 5.052 as the receipt records.
- The CPU netlist (`c208df0b`) and gPTP microcode digests are unchanged. The instrumented firmware and BIOS digests changed with the firmware, and the census (`measured_for`) is unchanged.
- The receipt was assembled by `scripts/r2/assemble_receipt.py`. It takes each arm's `measurement.json` verbatim and recomputes `measured_for`, the harness hashes and the maxima through `scripts/check_nvm_capture.py`'s own functions. It ends with that gate's `check_receipt`.
- `tb/verilator/nvm_capture_cpu/measurements.json`: 36,832 B, sha256 `6a16d669c4df2f0ab3e96bbc69c164f0be30aef02c2e86664be20f8529c43760` (commit `9112a0df`).

| shape | CPU MHz | traffic | min ms | max ms | 49 ms / max | round 1 (max) |
|---|---|---|---|---|---|---|
| 1x1 | 50 (contract) | ON | 3.96020 | 3.96548 | 12.3566x | 3.96548 |
| 1x1 | 50 (contract) | OFF | 3.90676 | 3.92034 | 12.4989x | 3.92034 |
| 8x8 | 50 (contract) | ON | 13.84828 | **13.86328** | 3.5345x | 13.86328 |
| 8x8 | 50 (contract) | OFF | 13.67538 | 13.68956 | 3.5794x | 13.68956 |
| 8x8 | 100 (non-contract) | ON | 10.41950 | 10.43406 | 4.6962x | 10.43406 |
| 8x8 | 100 (non-contract) | OFF | 10.41246 | 10.41566 | 4.7045x | 10.41566 |

- **8x8 contract maximum: 13.86328 ms against the 24.5 ms limit, margin 10.63672 ms, 3.5345x the floor.** Every arm's minimum and maximum equal round 1's. Individual captures moved by a few hundred system cycles, and traffic counts by one or two requests. `nvm_capture()` is unchanged.
- `python3 scripts/check_nvm_capture.py`: rc 0, "PASS: capture census, clocks, both timing arms and receipt agree"; `--mutation bytes|records|clock|ignore-off-timing` each exit 1.
- Section 18 and section 20 item 6 were refreshed by `scripts/r2/refresh_section18.py` (19 edits, each matched exactly once). It also applied R3's exact text.

### Where the shipping path derives the authoritative sequence (at `49d28e5a`)

Firmware, `sw/firmware/milan_baremetal/milan_baremetal.c`:

| line | what |
|---|---|
| 459 | `nvm_seq`, the authoritative sequence (RAM) |
| 725 | `nvm_seq_of()`: the sequence word of a container |
| 737-762 | `nvm_read_slot()`: one read into the stage; 758 takes the sequence from the staged bytes only after `VD_OK` |
| 781-805 | `nvm_judge_slot()`: the standing verdict and its sequence; UNREAD gives `VD_LEN` and sequence 0 |
| 813-825 | `nvm_restage()`: the picked slot again, accepted only under the sequence it was picked by |
| 1480 | `nvm_pick_slot()`: the wrap-safe compare, A on a tie |
| 1647-1675 | `nvm_boot()`: sequences from the judged reads, the pick, the re-stage loop, `nvm_seq` = the picked slot's or 0 (1669, 1672), `nvm_auth_slot` (1675) |
| 917 | `nvm_publish()`: publishes `nvm_seq` to `PP_NVM_SEL` word 2 |
| 1383, 1429-1430 | `nvm_commit()`: `next = nvm_seq + 1`; only a verified, byte-matched commit moves `nvm_seq` and `nvm_auth_slot` |
| 1930-1932 | `nvm_print_status()`: re-validates both slots from flash for the console only; never feeds `nvm_seq` |

The backend (`hdl/milan/KL_nvm_backend.sv:424, 439, 482, 490, 582`) stores and reads back word 2. The processor at `2ad2f845` carries no generation. Neither changed, and neither reviewer disputed it.

### Gate table (round 2)

Every command ran in the foreground or as a tracked background job, never piped; rc is the command's own. Python is CPython 3.12.3 in the scratch venv with the workflows' pinned requirements unless a row says otherwise; Verilator suites use the pinned 5.050.

`49d28e5a` is the last commit that changes anything a row below reads, except the rows marked final: the receipt commit changes only `measurements.json` and SNAPSHOT_OWNERSHIP section 18, and only the capture gate and the docs replica read those.

| Gate | Command | Head | rc | Result |
|---|---|---|---|---|
| Saved-state writer gate, all shapes and controls | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 49d28e5a | 0 | "OK across 5 shape(s), and every planted defect reddened"; 34 controls caught (5 writer, 9 #671 x 3 shapes, 2 boot-walk), and the disabled-writer mutant; 237 s |
| Same, four threads (hosted-runner CPU count) | `... --self-test --jobs 4` | 49d28e5a | 0 | same verdict; 358 s |
| Co-simulation | `make -C tb/verilator/nvm_cosim run` (JOBS=2, POOL=4) | 49d28e5a | 0 | "465 checks: 465 PASS, 0 FAIL", "39 of 39 mutant(s) killed by their named check"; 733 s |
| Builder bank, elaboration (elaborate.yml) | `python3 sw/builder/test_builder.py --require-elaboration --require-rv32`, product LiteX venv | 49d28e5a | 0 | "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11, needs the local mf48 tree); "no elaboration arm was skipped for a toolchain reason"; 1,445 s |
| rtl-fast firmware-unit replica | `firmware_unit_replica.sh`: tally, SDK and RV32 self-tests, `test_ctrl_firmware.py --require-rv32 --self-test`, `test_ctrl_nvm.py --require-rv32`, coverage self-test and check | 49d28e5a | 0 | 7/7; "saved-state store gate (#665 F1): OK across 5 shape(s), 435 tests"; coverage PASS (30 files); 2,822 s |
| rtl-fast changes, lint, BDD replica | `rtl_fast_other_replica.sh` | 49d28e5a | 0 | 5/5 |
| Service-budget self-test | `make -C tb/verilator/fw_service_budget` | 49d28e5a | 0 | flash, oracle 55/0, dispatch census PASS |
| Record-space gate | `python3 scripts/check_nvm_record_space.py` and `--self-test` | 49d28e5a | 0, 0 | 0 findings across 5 configs |
| C and Python idiom ratchets | `scripts/check_cpp_idiom.py`, `scripts/check_py_idiom.py` | 49d28e5a (worktree before commit) | 0, 0 | within every ratchet |
| Plant comparison | `python3 -I scripts/r2/compare_plants.py` against the reviewers' probe files | 49d28e5a | 0 | five plants byte-identical |
| Full-count controls, three shapes | `scripts/r2/plants_full.py` | 49d28e5a | 0 x 3 | all nine caught by name on each shape (table above) |
| Base reproduction | `scripts/r2/base_repro.py` with the base firmware | 49d28e5a checks | 0 x 2 | 645 findings per product shape, 124 "was lost on the clean reboot" |
| Boot-read probe | `scripts/r2/boot_read_probe.py`, service harness built by `run.py --build-only` | 49d28e5a | 0 x 8 | the table in "Boot worst case" |
| Firmware size | `scripts/r2/fw_size.sh`, both compilers | sources by digest | 0 | the table in "Firmware size delta" |
| Capture re-measure, six arms | `tb/verilator/nvm_capture_cpu/run.py` via `capture_driver.sh` | 49d28e5a | 0 x 6 | the table in "Capture re-measure" |
| Capture gate | `python3 scripts/check_nvm_capture.py` and its four `--mutation` controls | 9112a0df (worktree, then committed unchanged) | 0; 1 x 4 | "PASS: capture census, clocks, both timing arms and receipt agree"; every control detected |
| docs.yml replica (includes the builder bank `--require-rv32`, the capture gate, the writer gate and the idiom and hygiene ratchets) | `docs_check_replica.sh` (em-dash base `e8454e27`) | 9112a0df | 0 | 81/81 steps rc 0; the builder bank "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11); 2,101 s |

Not run, with the reason (unchanged from round 1): the act replica needs an open pull request; `act_ci.py --selftest` may run only inside the disposable CI job; `make -C gptp-processor docs` writes into the submodule; the SDK install step; rtl.yml's exhaustive Verilator and Yosys gates and rtl-fast `yosys-elaboration` (no file under `hdl/`, `syn/` or any submodule changed).

### Open risks (round 2)

1. **The detection limit**, unchanged: a fault that returns the same wrong bytes twice is a refusal of those bytes, and a slot read as all `0xFF` twice is blank. A judgement read answered with the other slot's valid container (an address fault) is invisible to any rule over the bytes; the re-stage's sequence check refuses it for the picked slot only. Stated in the host README and FASTCONNECT 7.
2. **The fault worst-case boot is about 17.1 s at 8x8**, inside #397's 20 s comparison by about 2.9 s (estimate from measured per-read costs). The #397 receipt itself was not re-measured.
3. **The writer restart** under heavy faults revokes `nvm_backed` (see above). This is honest, not a false claim.
4. **Hosted runtime of the writer gate.**
   - The builder bank runs `--self-test` with a 600 s timeout (`sw/builder/test_builder.py:28747-28751`), and `--jobs` defaults to the CPU count.
   - Here it takes 237 s (16 CPUs) and 358 s with `--jobs 4`.
   - At `f54dbe3e` the hosted step took 281 s for a suite R602 timed at 349 s.
   - The hosted time at this head is unverified until it runs.
5. **Observation outside #671, unchanged:** on the contract-mismatch path the disabled writer still heartbeats (`nvm_started` is set before the contract check, as at base), so `backed` reads 1 there. Not touched here; a candidate follow-up.
6. Round 1's risk 5 (`nvm_prefill_stage()` re-reads flash) still stands.
7. dev has moved to `1fb0ed9a` (#709 and #712, findings pages and the findings README only). `git merge-tree --write-tree origin/dev HEAD` is clean, rc 0, and touches nothing of this lane. Not merged, since merging was not asked for.

## Round 3

Status: REVIEW READY at `fc0c517cd55111d81a9fc2aeaa2edd3a82c9ee08` (tree `5df4098e`) on `671-read-fault`: five new commits on `9112a0df27acc1381091845e94d8eaa1407f1bbb`, with no rebase or amend, not pushed. Every gate the change touches ran with rc 0 (gate table below).

- Assignment: #671 comment 6103025987. Reviews answered: PR #715 comments 6103023016 (R602-2, NEGATIVE on one MINOR, F1) and 6102963708 (R603-2, NEGATIVE on one MAJOR, F1).
- REVIEW READY (round 3) posted: #671 comment 6104389214 (text in `receipts/r3/review_ready_comment.md`).
- The reviewers' round-2 probes were read as data, never executed, from `origin/671-review-evidence` at `660e67c2` (`review-evidence/671-r1/reviews/R602-2/` and `R603-2/`). `scripts/r3/compare_plants.py` parses them with `ast` (receipt below).
- The runtime capture prefill's fresh flash read (R603-2 OBS-1, R602-2-S2) is out of scope (issue #717) and untouched.

### Commits of this round

| commit | what |
|---|---|
| `1f484c66` | firmware: a held writer restart prints "re-attached and HELD" (R603-2-S2); the re-attach comment states the hold |
| `4c382cbb` | check 13 boots a writer restart without a fabric reset under a read fault; the restart model moves to `writer_restart.py`, shared with the co-simulation; the whole-boot read count is pinned; two new named controls on three shapes |
| `4886f231` | docs: the re-attach hold and the every-boot hold with the wipe as the only recovery on the firmware page (R602-2-S1); the two residue texts (R603-2-R1, R602-2-R1) |
| `1d517428` | the host suite README: two paragraphs `4c382cbb` left unwrapped, rewrapped (text unchanged) |
| `fc0c517c` | capture receipt re-measured at the round-3 firmware; section 18's provenance refreshed |

### The items and where each is answered

| Item | Source | Answer |
|---|---|---|
| 1. re-attach under a read fault | R603-2-F1, R602-2-F1 | done: `--restart` in the harness, 26 restart cases per shape in check 13, control `r_reattach_goes_live` caught by name on the three shapes. See "Check 13 on the writer restart" |
| 2a. exact read count of the whole-boot case with the other slot blank | R603-2-S1 | done, for every whole-boot case: exactly 6 reads on a cold boot and 5 on a restart (`read_fault_cases.py:256-269`); control `r_judge_four_tries` |
| 2b. a held re-attach prints that it is held | R603-2-S2 | done: `milan_baremetal.c:1699-1701`; graded (`read_fault_cases.py:299-300`) |
| 2c. the firmware page states the every-boot hold and the wipe as the only recovery | R602-2-S1 | done: `docs/integration/BAREMETAL_FIRMWARE.md:2044-2054` |
| 3. residue | R603-2-R1, R602-2-R1 | exact texts: `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:725-729` and `:1654` |

### Changes (file:line at `fc0c517c`)

Firmware, `sw/firmware/milan_baremetal/milan_baremetal.c` (sha256 `5f174859...`):

| file:line | change |
|---|---|
| 1611-1612 | the re-attach branch's comment: a slot UNREAD in that re-derivation HOLDS the writer, as on a cold boot |
| 1699-1701 | after `nvm_go_live()`, the re-attach line reads "re-attached and HELD" when `nvm_held` is set, otherwise "re-attached" as before. The text a reviewer plant anchors on (`nvm_go_live();` followed by `printf("Milan NVM: writer restarted on a live backend`) is kept |

Nothing else in the firmware changed: not the judge, re-stage, pick, fill or hold, not `nvm_commit()`, `nvm_capture()`, the record format or the register map.

Host model, `sw/firmware/nvm_hosttest/nvm_host.c`:

- 68-71: `nvm_host_writer_restart()` declared, the writer's CPU-only reset that `writer_restart.py` appends to the host build.
- 165-179: a read fault counts its SKIP from the read it is armed at, power-on for one given before `--boot`.
- 207, 801-803: `restart_reads=` in the summary.
- 594-599, 849-853: `arm_from_here()`, which the three fault options call. `arm_read_fault()` itself is unchanged.
- 900-911: `--restart`: prints "HOST restarting" and the summary the restart meets, runs the restart, settles, counts the reads it opened, prints "HOST restarted".

`sw/firmware/nvm_hosttest/writer_restart.py` (new): `WRITER_STATICS` and `host_restart()`, moved verbatim from `tb/verilator/nvm_cosim/run_cases.py` (only the generated C comment names its new file). `run_cases.py:72` imports it, so `run_cases.host_restart` is the same function. `scratch: restart model check` below shows the generated C is identical outside its comment and the statics list is identical.

`sw/firmware/nvm_hosttest/read_fault_cases.py`:

- 79-90: controls `r_reattach_goes_live` (R603-2's `p_reattach_goes_live` text) and `r_judge_four_tries` (R603-2's `p_judge_four_tries` text).
- 95-109: `PRODUCT_SHAPES` and `RETIRE_CAUSES`, moved here from `test_nvm_firmware.py` so that file stays inside the 1,000-line module ratchet.
- 113, 125-126, 133: `WHOLE`, `RESTART_WINDOWS`, `RESTART_RESTAGE`, `REATTACH_HELD`.
- 148, 160: `FaultCase.restart`; a restart case's name ends "on a writer restart".
- 168-184: `restart_cases()`; 187-197: `fault_cases()` puts them first, so a control the restart cases catch stops early.
- 245-253: `line_findings()`, the boot-line rule (judged slots and the offer) both paths share, moved out of `boot_findings()`.
- 256-269: `read_findings()`: the bound (13 on a cold boot, 12 on a restart) and the exact count for a whole-boot fault (6, or 5 on a restart).
- 272-302: `restart_findings()`: the restart's line; a slot left unread or a whole-restart fault must hold; a held restart moves no heartbeat, erase, program, START or ACK count, ends `backed=0 stale=1 dirty=1`, and prints "re-attached and HELD"; otherwise the change commits.

`sw/firmware/nvm_hosttest/test_nvm_firmware.py`:

- 46-61, 63-76: the docstring's check 13 and the sixteen controls.
- 124, 237-243: `compile_bench()` appends `host_restart()` to every host build.
- 286-293: `host_state()`, the summary parser `run()` and the restart grader share.
- 661-679: `boot_findings()` uses `line_findings()`.
- 718-731: `grade_restart_case()`: a clean cold boot, a 100 ms idle, the window dumped, the fault armed, `--restart`, the window dumped again (the restart must not reload it), the change and a 3,000 ms idle (past T-NVM-WRITER-ALIVE, so a held writer's claim lapses), then the same clean-reboot grading as a cold case.
- 742-749: `grade_fault_case()` dispatches restart cases; the read count comes from `read_findings()` (no early return, so a control's findings are all counted).
- 758: on the cold boot too, a slot left unread must hold, not only a whole-boot fault.

Docs:

- `sw/firmware/nvm_hosttest/README.md:46-56, 63-71, 117-143, 168-190` (at `1d517428`, which rewraps two paragraphs of `4c382cbb`): the model's restart and fault origin, check 13's restart cases and read counts, the two controls.
- `tb/verilator/nvm_cosim/README.md:71-76`: the restart model's new home.
- `docs/integration/BAREMETAL_FIRMWARE.md:2044-2054` (R602-2-S1, the re-attach hold) and `:2169-2174` (what the host suite proves).
- `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:725-729` (R603-2-R1, exact) and `:1654` (R602-2-R1, exact).

### Check 13 on the writer restart

26 restart cases per shape (13 per orientation), each after a clean cold boot and a 100 ms idle. The fault is armed after the boot, so its SKIP counts the restart's own reads. The fault then meets a CPU-only restart: every writer static reset, `nvm_boot()` again, the backend kept at load pending 0, load accepted 1, the window live.

- Other slot blank, valid slot faulted for the whole restart: its magic byte at sequences 1, 0x5A5A5, 0x80000000 and 0xFFFFFFFF, and a record-area byte at 0x5A5A5. The slot is UNREAD, and the writer must hold.
- Other slot blank, one faulty read of the sequence word at each of the restart's first four reads, at 0x5A5A5. This reaches the judgement and the re-stage. It must not hold, and the change must commit and survive.
- Both slots valid (newer at 0x5A5A5, or at 0 across the wrap): the newer faulted for the whole restart, or on its three re-stage reads (restart reads 2 to 4). The newer is UNREAD, the older is offered, and the writer must hold.

At the head on 1x1 (`scratch: restart_cases_head_1x1.log`), all 18 fault-lasting cases held with `restart_reads=5` (6 for the re-stage window), `acks=0 backed=0 stale=1 dirty=1`. The 8 single-read cases committed (`acks=1 backed=1`). There were 0 findings.

What the re-attach control does to the same cases (`scratch: reattach_mutant_detail_1x1.log`):

- **slot B valid at 0x5A5A5, B faulted for the restart:** the planted writer goes live with `nvm_seq` 0 and commits the change to A at sequence 1. The clean reboot offers B, so the change "was lost on the clean reboot". This is R603-2's probe scenario, and #671's loss.
- **slot A valid at 0x5A5A5, A faulted for the restart:** the planted writer erases A, the saved container, to commit at sequence 1. The faulted read-back fails, so the change is "neither committed nor refused", the clean reboot finds both slots blank, and "53 other saved record(s) did not survive".

### Controls and the defects they catch (round 3)

All eleven #671 controls run on `endstation_arty_4x4`, `endstation_ax7101_1x1_tdm8` and `endstation_ax7101_8x8`. Each is caught on every shape by a finding carrying its own words. The full counts below come from a run with no early stop (`scripts/r3/plants_full.py`) and are the same on the three shapes. They are split into restart and cold-boot cases:

| control | defect | named (restart / cold) | total | first named finding |
|---|---|---|---|---|
| `restart_at_zero` | an unread slot no longer holds | 28 (8 / 20) | 210 | "... was lost on the clean reboot" |
| `unbounded_retry` | the judge loop unbounded | 40 (14 / 26) | 85 | "... over the bound" |
| `generation_from_refused_slot` | a refused slot's sequence continues the generation | 8 (0 / 8) | 426 | "a generation was taken from a refused slot" |
| `verdict_only_agreement` | two reads agree by verdict only | 32 (8 / 24) | 322 | "... was lost on the clean reboot" |
| `r_digest_header_only` | the refusal digest covers the header | 48 (2 / 46) | 143 | "... on reads that returned different bytes" |
| `r_fill_from_flash` | the window filled by a fresh read | 62 (0 / 62) | 130 | "... is not the container it judged" |
| `r_restage_fail_offers_none` | an unread pick offers nothing | 12 (4 / 8) | 12 | "... yet the boot offered" |
| `restage_fail_not_unread` | an unread pick is not marked UNREAD | 28 (4 / 24) | 52 | "... yet the boot line does not name it unread" |
| `r_restage_any_seq` | the re-stage takes any VD_OK read | 12 (0 / 12) | 24 | "... another valid container than the one the boot offered" |
| **`r_reattach_goes_live`** | **the re-attach path goes live with a slot unread; the cold boot still holds** | **18 (18 / 0)** | **41** | "slot A valid at seq 0x1, --read-fault a:0:0:64 on a writer restart: the restart left a slot unread, yet the writer re-attached live" |
| **`r_judge_four_tries`** | **a judgement takes four reads** | **40 (14 / 26)** | **40** | restart: "... read the flash 6 times, want exactly 5"; cold: "slot A valid at seq 0x1, --read-fault a:0:0:64:8: with one slot faulted on every read the boot read the flash 7 times, want exactly 6" |

- `r_reattach_goes_live` is caught by restart cases only, as it must be: the cold boot is unchanged. Its other 23 findings name the consequences, at 8x8: 8 "was lost on the clean reboot", 5 "neither committed nor refused", 5 "the clean reboot did not offer a slot", and 5 "163 other saved record(s) did not survive".
- `r_judge_four_tries` is caught by the 26 cold whole-boot cases on their own (R603-2-S1 as asked), and by the 14 whole-restart cases too.
- Graded by checks 1 to 14 (the gate's own `grade`, the reviewers' `--all-grades`), `r_reattach_goes_live` gives 41 findings on each of the three shapes (`scratch: all_grades_reattach.log`). R602-2's `run_probe.sh` runs that same gate, so its rc is 1 on this plant.
- `scripts/r3/compare_plants.py` parses the reviewers' files without executing them:
  - the two shipped controls are byte-identical to R603-2's `p_reattach_goes_live` and `p_judge_four_tries`;
  - R602-2's `p1_reattach_no_hold` old text contains the shipped one and occurs once;
  - all 12 R603-2 plant texts and all 7 R602-2 plant texts occur exactly once at the head;
  - `probe_reattach.py`'s harness anchors (`--erase-ms` branch, `main`) and its firmware anchor occur exactly once. Its `--read-fault-now` adds `reads` to an `arm_read_fault()` it calls directly, which is unchanged, so it aims where it did.

### Firmware size delta (round 3)

Both compilers, LiteX's own `$(compile)` rule, product 1x1 build-tree headers (`scripts/r3/fw_size.sh`, receipt `receipts/r3/fw_size.txt`):

| compiler | base `a73ecc25` text / bss | round 2 `33eaa0c3` | round 3 `5f174859` | round 2 to 3 | base to round 3 |
|---|---|---|---|---|---|
| `riscv32-linux` GCC 14.3.0 (pinned SDK) | 15,529 / 88 | 17,241 / 100 | 17,297 / 100 | text +56 | text +1,768, bss +12 |
| `riscv64-elf` GCC 16.2.0 | 15,476 / 88 | 17,172 / 100 | 17,228 / 100 | text +56 | text +1,752, bss +12 |

Data is 104 B in every build.

### Where the shipping path derives the authoritative sequence (at `fc0c517c`; the firmware is unchanged since `1f484c66`)

Unchanged from round 2 at the same lines. Both boot paths, cold and re-attach, run the same `nvm_boot()` derivation. This round's firmware change is a console line after `nvm_go_live()`.

| line | what |
|---|---|
| 459 | `nvm_seq`, the authoritative sequence (RAM) |
| 725 | `nvm_seq_of()`: the sequence word of a container |
| 737-762 | `nvm_read_slot()`: one read into the stage; 758 takes the sequence from the staged bytes only after `VD_OK` |
| 781-805 | `nvm_judge_slot()`: the standing verdict and its sequence; UNREAD gives `VD_LEN` and sequence 0 |
| 813-825 | `nvm_restage()`: the picked slot again, accepted only under the sequence it was picked by |
| 1480 | `nvm_pick_slot()`: the wrap-safe compare, A on a tie |
| 1648-1676 | `nvm_boot()`: sequences from the judged reads, the pick, the re-stage loop, `nvm_seq` = the picked slot's or 0 (1670, 1673), `nvm_auth_slot` (1676), for the cold boot and the re-attach alike |
| 1699, 1736 | the two `nvm_go_live()` call sites, re-attach and cold boot; each holds the writer when a slot is UNREAD |
| 915 | `nvm_publish()`: publishes `nvm_seq` to `PP_NVM_SEL` word 2 |
| 1383, 1429-1430 | `nvm_commit()`: `next = nvm_seq + 1`; only a verified, byte-matched commit moves `nvm_seq` and `nvm_auth_slot` |
| 1930 | `nvm_print_status()`: re-validates both slots from flash for the console only; never feeds `nvm_seq` |

The backend (`hdl/milan/KL_nvm_backend.sv:424, 439, 482, 490, 582`) stores and reads back word 2. The processor at `2ad2f845` carries no generation. Neither changed.

### Capture re-measure (round 3)

The firmware changed (`1f484c66`), so all six arms were re-measured. They used the harness's own recipe (`scripts/r3/capture_driver.sh`, round 2's: `unshare -Urn "$PRODUCT_PYTHON" -B tb/verilator/nvm_capture_cpu/run.py --shape S --cpu-hz F --captures 16 --traffic on|off --build-dir <scratch>`), ran two at a time from 01:12 to 03:15, and each ended rc 0 (`receipts/r3/capture_driver-a.log`, `-b.log`).

- Measured commit `4886f231` (tree `4f92a4db`), firmware sha256 `5f174859...`, protocol-processor pin `2ad2f845`. The later commits change no captured input: the README rewrap `1d517428`, and the receipt commit itself.
- Environment as round 2: PYTHONHASHSEED=0, offline, LITEX_ENV_CC_TRIPLE=riscv32-linux, Verilator 5.052 as the receipt records.
- The CPU netlist, gPTP microcode and config digests are unchanged. The instrumented firmware and BIOS digests changed with the firmware. The census (`measured_for`) and the harness hashes are unchanged.
- **Every one of the 96 captures has the same `sys_cycles` as in round 2 (16 of 16 per arm).** The capture SoC's boot line ends `read faults=0 unread=0`.
- `scripts/r3/assemble_receipt.py` (round 2's, with the round-3 provenance sentence) assembled the receipt and ended with the gate's `check_receipt`.
- `tb/verilator/nvm_capture_cpu/measurements.json`: 36,871 B, sha256 `7891b82d62207fb08ecf992787387d375f8833561bebb31fa123be5cc5e96ae5` (commit `fc0c517c`).

| shape | CPU MHz | traffic | min ms | max ms | 49 ms / max | round 2 (max) |
|---|---|---|---|---|---|---|
| 1x1 | 50 (contract) | ON | 3.96020 | 3.96548 | 12.3566x | 3.96548 |
| 1x1 | 50 (contract) | OFF | 3.90676 | 3.92034 | 12.4989x | 3.92034 |
| 8x8 | 50 (contract) | ON | 13.84828 | **13.86328** | 3.5345x | 13.86328 |
| 8x8 | 50 (contract) | OFF | 13.67538 | 13.68956 | 3.5794x | 13.68956 |
| 8x8 | 100 (non-contract) | ON | 10.41950 | 10.43406 | 4.6962x | 10.43406 |
| 8x8 | 100 (non-contract) | OFF | 10.41246 | 10.41566 | 4.7045x | 10.41566 |

- **8x8 contract maximum: 13.86328 ms against the 24.5 ms limit, a margin of 10.63672 ms and 3.5345x the floor.** It is unchanged.
- `python3 scripts/check_nvm_capture.py` gives rc 0, "PASS: capture census, clocks, both timing arms and receipt agree". `--mutation bytes|records|clock|ignore-off-timing` each exit 1 (`receipts/r3/check_nvm_capture.log`).
- `scripts/r3/refresh_section18.py` refreshed section 18: 18 edits, each matched exactly once. Only the provenance lines moved (date, assignment chain, measured commit, tree, firmware digest), because every figure is equal. Section 20 item 6 is unchanged for the same reason.

### Gate table (round 3)

Every command ran in the foreground or as a tracked background job, never piped; rc is the command's own. Python is CPython 3.12.3 in the scratch venv with the workflows' pinned requirements unless a row says otherwise; Verilator suites use the pinned 5.050. `fc0c517c` is the head. Since `4c382cbb` nothing a row reads has changed, except the rows' own targets: the docs, the README rewrap and the receipt.

| Gate | Command | Head | rc | Result |
|---|---|---|---|---|
| Saved-state writer gate, firmware change alone | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --jobs 8` | `1f484c66` (other files stashed) | 0 | "OK across 5 shape(s)" |
| Saved-state writer gate, all shapes and controls | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | `4c382cbb` worktree, unchanged at commit | 0 | "OK across 5 shape(s), and every planted defect reddened"; 40 controls caught (5 writer, 11 #671 x 3 shapes, 2 boot-walk), the disabled-writer mutant and the PHY checks; 202 s at 16 jobs |
| C idiom, Python idiom, hygiene ratchets | `scripts/check_cpp_idiom.py`, `scripts/check_py_idiom.py`, `scripts/check_hygiene.py --check` | worktree before `4c382cbb` | 0, 0, 0 | within every ratchet; `long module 10 <= 10` (`test_nvm_firmware.py` is 998 lines) |
| Docs gates | `scripts/docs_check.py`; `scripts/check_em_dash.py --base e8454e27`; `scripts/check_doc_style.py`; `scripts/check_doc_paths.py` | `4886f231` | 0 x 4 | 0 findings across 202 md files; em-dash 0 over 230 added lines; style OK; 957 cited paths resolve |
| Restart model check | scratch: old `run_cases.host_restart` against `writer_restart.host_restart` | `4c382cbb` | 0 | statics identical; generated C identical outside its comment; `run_cases.host_restart is writer_restart.host_restart` |
| Restart cases, head and three plants | `scripts/r3/restart_cases.py` | `4c382cbb` | 0 x 4 | head: 26 cases, 0 findings; `r_reattach_goes_live` 41, `r_judge_four_tries` 14, `restart_at_zero` findings on the restart cases |
| Full-count controls, three shapes | `scripts/r3/plants_full.py` | `4c382cbb` | 0 x 3 | the table above |
| Checks 1 to 14 on the re-attach plant | `scripts/r3/all_grades.py ... r_reattach_goes_live` | `4886f231` | 0 | CAUGHT, 41 findings on each of three shapes |
| Plant comparison | `python3 -I scripts/r3/compare_plants.py` | `4886f231` | 0 | see above |
| Firmware size | `scripts/r3/fw_size.sh`, both compilers | sources by digest | 0, 0 | the table above |
| Saved-state writer gate, four threads (hosted-runner CPU count) | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test --jobs 4` | `4886f231` | 0 | same verdict, 40 controls; 235 s with the load average near 25 (two capture arms running beside it); round 2's 358 s was under heavier load |
| rtl-fast firmware-unit replica | `scripts/r3/firmware_unit_replica.sh` (round 2's): tally, SDK and RV32 self-tests, `test_ctrl_firmware.py --require-rv32 --self-test`, `test_ctrl_nvm.py --require-rv32`, coverage self-test and check | `4886f231` | 0 | 7/7; the A/B power-loss suite "saved-state store gate (#665 F1): OK across 5 shape(s), 435 tests"; coverage PASS (30 files) |

Not run, with the reason:

- `scripts/act_ci.py --pr 715` (the act replica). This round's commits are not pushed, and this lane may not push. The runner records and checks out the remote PR head (`9112a0df`), so it would validate round 2, not this head. The hosted contexts are likewise owed at the pushed head.
- `act_ci.py --selftest`, `make -C gptp-processor docs` and the SDK install step: the same reasons as rounds 1 and 2.
- rtl.yml's exhaustive Verilator and Yosys gates and rtl-fast `yosys-elaboration`: no file under `hdl/`, `syn/` or any submodule changed. The Verilator suites that read a changed file were all run above: `nvm_cosim` (the firmware, `run_cases.py`, `writer_restart.py`), `nvm_capture_cpu` (the firmware) and `fw_service_budget` (the firmware).
- elaborate.yml `scripts/run_litex_sims.sh`: its five LiteX simulations read no changed file.
- The reviewers' probes (`probe_reattach.py`, `probe_mutants.py`, `run_probe.sh`) were not executed, as in round 2. The shipped controls carry their texts, and `compare_plants.py` checks every anchor they plant or patch.

### Open risks (round 3)

1. **The detection limit** is unchanged: the same wrong bytes twice, all-`0xFF` twice, and a judgement read answered with the other slot's container.
2. **The restart model is the co-simulation's, and it has the same limits.** It returns the writer's statics to their initial values and runs `nvm_boot()` again. It does not model the boot code's memory initialisation, the memory holding the live window, or the bus fabric (obligation O4 of the contract page, as for W1 to W4).
3. **The fault worst-case boot is an estimate, about 17.1 s at 8x8**, unchanged. A restart opens at most twelve slot reads (it reads no AEM image), so the same bound prices it. Under heavy faults a restart outlasts T-NVM-WRITER-ALIVE. The fabric then revokes `nvm_backed`, and a held restart is now graded to end `backed=0 stale=1`.
4. **Hosted runtime of the writer gate.** It takes 235 s here at `--jobs 4` and 202 s at 16 jobs, against the builder bank's 600 s timeout. The hosted time at this head is unknown until it runs.
5. **Unchanged observations outside #671:**
   - the disabled writer still heartbeats on the contract-mismatch path;
   - the runtime prefill reads the slot freshly from flash (#717).
6. **dev has moved to `ac2c5e77`** (#709, #712 and #710). #710 changes `sw/litex/milan_soc.py` (the MAC's retained crossings and its CSR FIFOs).
   - `git merge-tree --write-tree origin/dev HEAD` is clean, rc 0, and no file overlaps this lane.
   - The capture receipt binds the firmware, the census and the harness, not the SoC source. So the capture gate passes on a merge candidate without measuring there.
   - Whether #710 moves the capture time was not measured here.
   - Not merged, since merging was not asked for.


## Round 4

Status: REVIEW READY at `7bc7ceca6ba1dd1a268d6fa1704613bb141487fe` on `671-read-fault`, from `fc0c517cd55111d81a9fc2aeaa2edd3a82c9ee08` (new commits only, no rebase or amend, not pushed).

- Assignment: #671 comment 6104799677. Reviews answered: PR #715 comments 6104687947 (R602-3, NEGATIVE on two MINOR, F1 and F2) and 6104797818 (R603-3, NEGATIVE on one MINOR, F1; S1).
- The reviewers' round-3 probes were read as data from `origin/671-review-evidence` at `7b97b127` (`review-evidence/671-r1/reviews/R602-3/scripts/` and `R603-3/scripts/`).

### Resume checkpoint

The interrupted session left a clean worktree at `cb30a99aafbcc53e2cbef8da4dac5c70da096941`, five new commits on `fc0c517c`. Origin and ancestry were rechecked. Its sound implementation was retained. The resumed work completed the full 13/12-read window enumeration, reconciled the base reproduction, and collected the successful exits of the captures, documentation bank, firmware unit bank and co-simulation. No STOP condition arose.

### Committed changes and line references

These line references describe the final source at `10c6a6471`; the capture-only follow-up does not move them. The firmware has not changed since `079956ce9`.

| Commit | Change and file:line |
|---|---|
| `079956ce9` | `sw/firmware/milan_baremetal/milan_baremetal.c:476` adds the diagnostic `nvm_unstaged` bits; `:1569` prints each unread slot's real cause; `:1601` uses that helper for the boot hold; `:1671` records a failed re-stage; `:1997` uses the same cause for the console refusal. `sw/firmware/nvm_hosttest/writer_restart.py:23` resets the new static in both suites. |
| `d427c79a4` | `sw/firmware/nvm_hosttest/nvm_host.c:198` bounds a host boot/restart read storm separately from the run-wide counter; `:541` reports the count at the stop; `:827` and `:920` bracket boot and restart. The stop is after 1,000 reads, far above the contract's 13/12, so an unbounded plant terminates with a named finding. |
| `d49117ecb` | `sw/builder/test_builder.py:28753` gives the saved-state host gate 1,200 s. A hosted run took 594 s under the old 600 s limit; this is runtime allowance, not a changed correctness oracle. |
| `1eb460f7e` | `sw/firmware/nvm_hosttest/read_fault_cases.py:87` pins the judgement bound, `:95` adds the unbounded re-stage control, `:102` adds the four-try re-stage. `:188` generates windows; `:199` crosses them with fault manners and rotates sequences; `:243` models reads once; `:329` grades exact counts; `:344` grades the hold and cause. `sw/firmware/nvm_hosttest/test_nvm_firmware.py:675` caches clean reboot results by identical flash bytes and hold state; `:719` grades restarts; `:735` drives every faulty case; `:773` grades the generated campaign; `:812` checks console/refusal/wipe and retire causes. |
| `cb30a99aa` | `sw/firmware/nvm_hosttest/README.md:108` and the gate docstring describe generated windows, exact counts, the detection limit and controls. `docs/integration/BAREMETAL_FIRMWARE.md:2015` describes the judgement/re-stage causes, hold and publication. `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:725` records a held re-attach's diagnostic publication; `docs/design/SAVED_STATE_FASTCONNECT.md:797` states the read-back rule. |

**Final expansion, `10c6a6471`:** `sw/firmware/nvm_hosttest/read_fault_cases.py:188,216` enumerates the complete 13/12-read bound, including unreachable starts. `sw/firmware/nvm_hosttest/test_nvm_firmware.py:773` and `sw/firmware/nvm_hosttest/README.md:133` record the full generated campaign and its 2,158 cases. `sw/builder/test_builder.py:28749` no longer quotes the intermediate runtime ratio.

**Final capture commit, `7bc7ceca6`:** `tb/verilator/nvm_capture_cpu/measurements.json:3` and `:19` bind the new measured tree and firmware, with new rows and build identities throughout the six-arm receipt. `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1629` records the Round 4 assignment and measurement provenance.

### Generated campaign and runtime

R602-3-F1 and R603-3-F1 are answered by the generator and reference model, rather than adding another selected window.

- Every start position in the complete boot/restart bound meets lengths 1, 2, 3 and 4, plus the whole-boot window `(0, 64)`: 53 windows for a cold boot and 49 for a restart. Starts after a clean boot would end are included in the standing suite. This final expansion makes the assignment literal; no window is removed for runtime.
- Every applicable manner in each group is crossed with those windows: differing magic, sequence or record-area bytes; all-0xFF; another slot's valid container. Both orientations and both layouts run on cold boots and writer restarts.
- The sequence dimension is reduced as the assignment permits. The four one-valid values and two both-valid values rotate through the windows; they are not multiplied across every window. None of the windows or byte-fault manners is removed. The earlier complete-cross working version took 531.5 s at four jobs (not a passing receipt: it still had a stale plant anchor). The old head took 217.73 s; the intermediate 670-case suite took 243.84 s, including all 46 controls. The final 2,158-case suite passed in 461.48 s at four jobs while the builder, two captures and three full-control campaigns ran concurrently. The hosted old-head run's 594 s made keeping the full multiplication impractical under its 600 s ceiling. The builder allowance is now 1,200 s.
- There are 2,244 generated cases per shape. The reference model identifies 86 outside the documented detection limit: repeat identical wrong bytes, or another valid container accepted as the slot's contents. They are not graded as detectable faults. The remaining **2,158 cases per shape** are **1,119 cold boots and 1,039 writer restarts**. Every window retains each group's byte-fault manners.
- The model predicts 226 held cases, 86 involving a failed re-stage. It computes exact reads from the contract: AEM read on cold boot; A then B judgement; newest accepted slot re-staged; the remaining accepted slot re-staged after failure. It does not type an expected count into individual cases or read the firmware's control flow.
- `scripts/r4/complement_windows.py` also ran 1,488 windows beginning after the clean schedule. The reference model departed from the clean schedule in none, and the shipping head gave zero findings. Those positions are now also part of the standing generated campaign.
- Reboot caching is local to one firmware/shape campaign and keyed by both complete slot byte strings and held state. The changed record and expected records are constant in that campaign. A different slot result is always rebooted and graded. This retains the persistence oracle while avoiding identical deterministic reboots.

### Tests and planted defects

The standalone suite command is:

```sh
python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test --jobs 4
```

It passes five shapes and catches 46 controls: five pre-existing writer controls, thirteen #671 controls on three shapes, and two boot-walk controls. Disabled-writer and PHY checks also pass. The five older controls prove ascending IDs, erase-loop heartbeat, read-back verification, full erased-record validation and open-neighbour isolation. The boot-walk controls remove the shape-failure walk or wait only for DONE and must fail their own checks.

The following full-count table belongs to the intermediate 670-case campaign (`cb30a99a`), on each of the three required shapes. It records the defects and their named oracles. The final full-bound gate rechecks all controls; its three required bound-control counts are recorded separately below.

| Control | Planted defect | Named findings (restart / cold) | Oracle words |
|---|---|---|---|
| `restart_at_zero` | unread slot no longer holds | 31 (14 / 17) | was lost on the clean reboot |
| `unbounded_retry` | judgement retry unbounded | 32 (16 / 16) | over the bound |
| `generation_from_refused_slot` | generation from refused bytes | 8 (0 / 8) | generation was taken from a refused slot |
| `verdict_only_agreement` | verdict equality replaces byte agreement | 28 (14 / 14) | was lost on the clean reboot |
| `r_digest_header_only` | digest omits record bytes | 70 (31 / 39) | on reads that returned different bytes |
| `r_fill_from_flash` | extra unjudged read fills the window | 331 (0 / 331) | want exactly |
| `r_restage_fail_offers_none` | failed newest re-stage skips the other slot | 46 (21 / 25) | yet the boot offered |
| `restage_fail_not_unread` | failed re-stage is not marked unread | 86 (41 / 45) | yet the boot line does not name it unread |
| `r_restage_any_seq` | accepts a different valid sequence | 11 (0 / 11) | another valid container than the one the boot offered |
| `r_reattach_goes_live` | re-attach hold alone is removed | 106 (106 / 0) | yet the writer re-attached live |
| `r_judge_four_tries` | judgement takes four reads | 140 (65 / 75) | want exactly |
| `p_restage_unbounded` | re-stage loses its bound | 52 (26 / 26) | want exactly |
| `r_restage_four_tries` | re-stage takes four reads | 68 (32 / 36) | want exactly |

The unbounded re-stage also has sixteen over-bound findings, including a one-read address fault that leaves the picked slot permanently unable to read back. The host stops that plant at 1,001 reads; the head holds after seven and runs its restore walk. A four-try plant opens eight reads and fails the exact-count oracle. `scripts/r4/restage_hang.py` records this on 8x8.

The reviewer plants were parsed from the public evidence branch and applied by `scripts/r4/reviewer_plants.py`, with their old-text occurrence checked. The head gives zero findings. Both reviewers' re-stage plants and their other correctness plants are caught on the first and product shapes. R602-3's old console anchor no longer exists after the helper extraction; its equivalent head-form console omission is caught. `p_reattach_held_no_publish` still gives zero findings: this optional item is a documented diagnostic, not a persistence requirement. The original `R602-3_scripts_probe_restage_bound.py` was also run unmodified on arty, 1x1 and 8x8: all four head cases have zero findings; all four four-try cases fail exact counts; all four unbounded cases fail the total bound.

The final full-bound campaign at `10c6a6471` catches all 46 controls. Full-count repeats of the three required bound controls give the same named counts on each required shape: `p_restage_unbounded` 52 (26 restart / 26 cold), `r_restage_four_tries` 68 (32 / 36), and `r_judge_four_tries` 140 (65 / 75). The unbounded control additionally produces sixteen over-bound findings; its total is 160 on each shape in these runs. The independently run full-control receipts are `final_plants_<shape>.log`.

The following reproduces the complete-case bound counts and base comparison from the repository root. `HANDOFF` names this output directory and `SCRATCH` names an external disk directory. Use the pinned Python environment and export `TMPDIR` to disk scratch.

```sh
for shape in endstation_arty_4x4 endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
    python3 "$HANDOFF/scripts/r4/plants_full.py" "$PWD" "$SCRATCH/final-plants-$shape" 4 "$shape" p_restage_unbounded r_restage_four_tries r_judge_four_tries
done
python3 "$HANDOFF/scripts/r4/base_reproduction.py" "$PWD" "$SCRATCH/base-fullbound" 4 e8454e27 endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8
```

The builder bank's six foreground parts use the same required-elaboration verdict and all 101 functions in their original order:

```sh
for part in 0 1 2 3 4 5; do
    python3 "$HANDOFF/scripts/r4/builder_parts.py" "$PWD" "$part" 6 --require-elaboration --require-rv32
done
```

The measured builder run used a scratch `sitecustomize.py` that replaces `os.cpu_count()` with `min(4, original_cpu_count() or 4)` to cap default worker choices. It changes no test function or expected value. `VERILATOR_JOBS=2` and the pinned GNU make 4.3 were on that invocation's environment. The writer command itself used four jobs explicitly.

### Base reproduction, R602-3-F2

`base_reproduction.py` extracts `e8454e27`'s firmware and matches the restart model to its declared statics: 15 retained, with `nvm_unread`, `nvm_held`, `nvm_read_faults` and `nvm_unstaged` absent. No production code is rewritten for this probe. Its firmware digest is `a73ecc25c77bfb7c4e1c2c711d72f0b560dd7e8d18cde92f40e67efcc84f0eb3`.

At the final full-bound Round 4 harness (`base_fullbound.log`) it gives **2,660 findings per product shape, 124 "was lost on the clean reboot"**. The two product shapes agree. The intermediate 670-case result was 1,466 / 110, and is superseded here. PR-BODY now gives those figures and the model adaptation. The previous 645 / 124 belongs to `9112a0df`; the round-3 743 / 135 belongs to the reviewers' narrowed restart model at `fc0c517c`. They are not current-head claims.

### Authoritative sequence, every shipping-path location

The firmware is `sw/firmware/milan_baremetal/milan_baremetal.c`, digest `41000488944bea651733b9708fa0c3a72926ce2308034c51209f2dd95a27b2a2`:

| File:line | Role |
|---|---|
| firmware:459 | RAM authority, `nvm_seq` |
| firmware:728 | `nvm_seq_of`, reads the sequence word |
| firmware:740 and :761 | `nvm_read_slot`, copies one flash read into the stage and obtains a sequence only after VD_OK |
| firmware:784 and :806 | `nvm_judge_slot`, accepted read's sequence; an unread result has sequence zero |
| firmware:816 and :823 | bounded re-stage requires VD_OK and the selected sequence |
| firmware:1483 | wrap-safe slot selection; A wins ties |
| firmware:1660, :1664, :1666, :1680, :1683, :1686, :1689 | both boot paths derive authority from judged reads, re-pick on failed re-stage, assign the accepted sequence or zero, and set the authoritative slot |
| firmware:1712 and :1749 | re-attach and cold-boot persistence hold |
| firmware:918 and :920 | publishes RAM authority through word 2; does not derive it |
| firmware:1386, :1418 and :1432 | next generation is accepted generation plus one; the target’s verified sequence must match it; promotion follows successful verify and byte match |
| firmware:1943, :1947 and :1948 | console-only re-validation and sequence reads of current flash; does not feed RAM authority |
| `hdl/milan/KL_nvm_backend.sv:424,439,482,490,582` | word 2 definition, storage, reset, write and readback; no choice or arithmetic on it |
| `hdl/milan/KL_pp_shadow.sv:997` | parent instantiates this backend on the processor device face |
| `protocol-processor/hdl/top/protocol_processor_top.sv:2899` | instantiated record port |
| `protocol-processor/hdl/aecp/KL_aecp_engine.sv:2001` | instantiated D3 record writer |
| `protocol-processor/hdl/aecp/KL_aecp_nvm_writer.sv:16` and `hdl/packet_engine/KL_pp_nvm_port.sv:14` within that submodule | per-record framing and CRC-16, no slot-generation metadata or selection |

The processor remains clean at `2ad2f845dd583f8310075fa2380cb60a04fd091a`. No submodule commit or adoption is needed. Before submodule Git checks, each `rev-parse --show-toplevel` was verified to name its own directory. Origin is the required repository and the lane's merge-base with `e8454e27` is exactly `e8454e2751d05b02ee8e5a571857589ab358ab86`.

### Firmware size

`receipts/r4/fw_size.txt`, produced with `scripts/r4/fw_size.sh` and the product 1x1 generated headers:

| Compiler | Base text / bss | Round 3 | Round 4 | Round 4 delta | Total delta |
|---|---|---|---|---|---|
| pinned RV32 SDK, GCC 14.3.0 | 15,529 / 88 | 17,297 / 100 | 17,483 / 104 | text +186, bss +4 | text +1,954, bss +16 |
| local RV32-capable compiler, GCC 16.2.0 | 15,476 / 88 | 17,228 / 100 | 17,454 / 104 | text +226, bss +4 | text +1,978, bss +16 |

Data is 104 B throughout. Firmware size is an object-size comparison using the firmware Makefile's compile rule, not a complete ROM headroom claim.

### Capture re-measure

All six arms passed, 16 captures each, for firmware `41000488944bea651733b9708fa0c3a72926ce2308034c51209f2dd95a27b2a2`. The measured firmware and capture inputs are those of `cb30a99a`; the later generated-window change does not alter them. The source-bound receipt was regenerated only through `scripts/r4/assemble_receipt.py`; `refresh_section18.py` refreshed its documentation. The receipt gate passes, and all four mutation controls (`bytes`, `records`, `clock`, `ignore-off-timing`) return the required rejection (rc 1).

| Shape | CPU MHz | Traffic | Measured min–max, ms | Floor ratio |
|---|---:|---|---:|---:|
| 1x1 | 50 | on | 3.96020–3.96548 | 12.3566x |
| 1x1 | 50 | off | 3.90676–3.92034 | 12.4989x |
| 8x8 | 50 | on | 13.84828–13.86328 | 3.5345x |
| 8x8 | 50 | off | 13.67538–13.68956 | 3.5794x |
| 8x8 | 100 | on | 10.41950–10.43406 | 4.6962x |
| 8x8 | 100 | off | 10.41246–10.41566 | 4.7045x |

The 8x8 contract maximum is **13.86328 ms**, leaving **10.63672 ms** to the 24.5 ms limit, with a **3.5345x** ratio to the 49 ms floor. The 1x1 maximum is **3.96548 ms**, leaving **20.53452 ms**, with a **12.3566x** floor ratio. The 100 MHz 8x8 comparison is non-contract: **10.43406 ms** maximum. These maxima are unchanged from Round 3; individual cycle/request observations are not all identical, and the receipt retains the actual new rows.

The product capture recipe uses its recorded Verilator 5.052 environment; the suite runs use pinned 5.050. At most two builds ran concurrently. Later, the independent 1x1 simulations overlapped the two active 8x8 simulations. All six arms returned zero; the two inherited launchers' completed child exit statuses were collected before releasing them. No capture or gate remains running.

Retained evidence is indexed by [the receipt manifest](receipts/r4/MANIFEST.md). It maps scratch-relative names to small normalized copies and records original sizes and SHA-256 hashes. [Capture artifact identities](receipts/r4/CAPTURE-ARTIFACTS.md) cover the simulator, firmware object, BIOS and CPU netlist without copying build products into this directory. The final collection includes all six arms.

### Gate table

Final-source results at `7bc7ceca6`. Tests run at an earlier named head read inputs unchanged at this head; the refreshed receipt and documentation have their own final checks. The earlier 670-case writer run and the separate full-count table above remain intermediate evidence at `cb30a99a`; the standing full-bound campaign is the 2,158-case run below.

| Command / receipt | rc | Result / planted defect |
|---|---|---|
| `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test --jobs 4` / `full_bound_selftest.log` | 0 | Five shapes, 2,158 cases each, 46 controls; 461.48 s at `10c6a6471` |
| `scripts/r4/plants_full.py` / `final_plants_<shape>.log` | 0 each | Complete-case counts for the three required bound controls on all three shapes: 52 / 68 / 140 named findings |
| `scripts/r4/reviewer_plants.py` | 0 | Publicly supplied plant texts are caught; the clean firmware stays clean. The optional held-publication plant remains diagnostic-only |
| Original reviewer `probe_restage_bound.py` / `bound-final-<shape>.log` | 0 each | All three shapes: four clean cases pass, four raised-bound cases fail exact counts, four unbounded cases fail the total bound |
| `scripts/r4/restage_hang.py` | 0 | Address-fault hang plant reaches 1,001 reads; the head holds after seven and completes its walk |
| `scripts/r4/base_reproduction.py` / `base_fullbound.log` | 0 | Base failure reproduced under the current grader: 2,660 findings, 124 lost changes, per product shape |
| `python3 sw/builder/test_builder.py --require-elaboration --require-rv32`, through `scripts/r4/builder_parts.py` | 0 all six parts | All 101 test functions, unchanged and in order; all required elaboration arms run. Parts take 915.59, 25.76, 6.16, 53.94, 4.86 and 474.15 s. Gate 11 lacks its historical physical report; gate 1b’s make mutation has no effect under GNU make 4.3 |
| `make -C tb/verilator/nvm_cosim run JOBS=2 POOL=4` | 0 | 465/465 checks, 39/39 named mutants killed; unchanged A/B guarantees and restart wiring exercised |
| `make -C tb/verilator/fw_service_budget` | 0 | 14 firmware checks and 55 oracle checks; removing dispatch service fails its control |
| `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | 0 | Five shapes, 435 tests, including A/B power-cut sweeps |
| Other firmware-unit steps / `fwunit/replica.log`, `fwunit/tail.log` | 0 each | Tally controls, RV32 SDK and firmware self-tests, controller mutation bank, coverage self-test and coverage check; 7/7 with the store row |
| Selected documentation step replica | 0 all 81 positions | Initial positions 1–36 and resumed 37, 40–81: 79 positions, including record-space controls and builder bank. Position 39 is the final writer row above; position 38 is the new capture receipt gate |
| rtl-fast lint/BDD replica | 0 | 5/5 steps: workflow scope controls, RTL lint, processor source-list controls and BDD |
| C/Python idiom, hygiene, documentation style/path checks, `docs_check.py`, diff check after the full-bound change | 0 each | No increased ratchet, stale links, whitespace failures or documentation findings |
| Six capture arms and refreshed receipt/documentation gates | 0 | 96 clean captures; firmware-bound receipt passes. Four capture controls reject with expected rc 1. Final documentation, TOC, path/style, idiom, hygiene and diff checks pass |

The 81-position documentation replica is a selected command list, not a claim that every hosted workflow step ran locally. It omits dependency/SDK installation because those prerequisites are present, unchanged `gptp-processor` documentation generation because that would write into the submodule, and the candidate `scripts/act_ci.py --selftest` because AGENTS.md confines that command to the disposable CI job. The latter was not run on the host. Its protected job remains a publication duty.

A resumed batch inherited a host gate without a worker cap and disk TMPDIR. MemoryCurrent briefly reached about 11.6 GB. That inherited documentation batch was stopped, and remaining commands use disk scratch and a four-CPU resource policy. Memory dropped to about 6 GB. This interruption is a resource correction, not a gate pass or a firmware finding. The completed builder rc 0 and preceding gate receipts were preserved. The capture launchers were paused between arms to keep at most two builds in flight; their active measurements continued.

Not run by this lane: act against an unpublished head, hosted contexts for the new commits, a current-dev merge-candidate bank, physical hardware/bench work, flash writes, or unrelated exhaustive RTL/Yosys sweeps. There is no RTL, generator, register-map or gitlink change. The changed-file consumers are the host writer, builder, capture, co-simulation and service-budget suites, plus documentation and hygiene gates. The manager must publish the head and obtain exact-head hosted and act evidence, independent re-review and candidate validation. The exact final publication text is in `REVIEW-READY.md`; the public URL is recorded by the publication step.

The inherited firmware-unit launcher was stopped between steps after its controller child finished. That child's exit status was verified as zero. Steps 5 through 7 ran separately with disk scratch; `fwunit/tail.log` records each result.

The builder bank was divided into six consecutive parts by its own function list, with no test function changed or omitted. `scripts/r4/builder_parts.py` records each part and applies the bank’s required-elaboration verdict. The final part passed on `10c6a6471`. The two 1x1 capture arms were started independently while the 8x8 simulations continued; the old launchers were paused before those arms to prevent duplicate builds. Their completed child statuses were collected as rc 0, and the launchers were released. At most two builds ran at once.

Final cleanup: known ignored test outputs and Python caches, including the processor descriptor cache, were moved to disk scratch. No generated or scratch file remains in the worktree; tracked files and submodule checkouts are clean. No Makefile changed in this round.

Public Round 4 handoff: [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6106272193).

## Round 5

Status: REVIEW READY at `0c276b621d638c9a83e82f71fbf07bc153517bf7` on `671-read-fault`, from `7bc7ceca6ba1dd1a268d6fa1704613bb141487fe` (new commits only, no rebase or amend, not pushed).

- Assignment: #671 comment 6107082416. Reviews answered: PR #715 comments 6107062972 (R603-4, NEGATIVE on one MAJOR, F1) and 6107063548 (R602-4, POSITIVE; S1 and S2 are optional SUGGESTIONs and are not taken up here).
- R603-4's `probe_refusal_digest.py` was read as data from `origin/671-review-evidence` at `e71b0368` (`review-evidence/671-r1/reviews/R603-4/`). Its sha256 `87a45da255d7c3896a0a358c894dc9fbdbb14e99549ebe13fe79fd3d6ec4e685` matches that packet's manifest.
- **Found at the start, and fixed here:** the hosted `docs-check` at `7bc7ceca` FAILED. Its builder step (`test_builder.py --require-rv32`) timed out `test_nvm_firmware.py --self-test` at its 1,200 s limit (run 38120473372, job 114413970181). It had reached the fifth of thirteen #671 controls. Round 4's 2,158-case campaign caused it. `elaborate` passed the same builder gate at that head. No review mentioned the failure.

### Commits of this round

| Commit | Change |
|---|---|
| `68f8a0364` | host model: `settle()` skips its word walk when one `memcmp` finds no CSR store since the last settle |
| `af2165cb9` | firmware: refused reads compared by count, CRC-32 over all but the last four bytes, and those four; check 13 gains sealed faults; control `r_digest_with_trailer` |
| `bd42818d3` | docs: the comparison, its reason, its detection limit, the sealed faults and the control |
| `de90ca768` | cases: R603-4's class (two sealed refusals opening a judgement, then a clean read) at every sequence of its group, from the reference model's judgement reads |
| `0c276b621` | capture: six-arm re-measure at the new firmware; receipt and section 18 |

### Item 1: the refused-read comparison (R603-4-F1)

**The defect.** At `7bc7ceca`, `milan_baremetal.c:763` took a refusal's digest as one CRC-32 over every byte read, the trailer included. For any container whose CRC closes, that value is the CRC-32 residue `0x2144df1c`. So two refused reads of different containers whose CRCs both close compared equal. R603-4 showed the second refusal standing and the acknowledged change lost, on both product shapes and both orientations.

**The comparison now** (`sw/firmware/milan_baremetal/milan_baremetal.c` at `af2165cb9`):

- `:408-414` `struct nvm_read` gains `tail`; the comment says what a refusal records.
- `:744` and `:795` are the two initialisers.
- `:762-770` for a refusal: `digest` is the CRC-32 over `rd.bytes - KLJ2_TRAILER` bytes, and `tail` is the last four bytes, read whole.
- `:774-780` `nvm_reads_agree` requires equal verdict, byte count, digest and tail.

**Why this function.** For two containers whose CRCs close, the pair (digest, tail) is (CRC(M), CRC(M)), where M is all bytes but the trailer. They compare equal only when their prefix CRCs collide, never by construction. CRC-32 has Hamming distance 3 at the 64 KiB slot length. So any two reads that differ in one or two bits, or only within one 32-bit burst, are always told apart; any other two except with a probability of about 2^-32. For a refusal whose CRC does not close, the trailer is compared bit for bit. So two views that differ only in their trailer also disagree. A digest over the prefix alone would have missed that case. A header-only refusal (40 bytes) is the CRC over 36 bytes plus the last header word.

A full byte comparison would need a second 64 KiB copy of the first read. The stage holds exactly one slot, and the stage is the only private RAM the writer has for this.

**Unchanged:** the three-read judgement bound (`NVM_READ_TRIES`, `:800`), validated-only generation (`:762-763`, `:815`), the re-stage (`:825-837`), the fallback (`:1675-1690`) and the hold (`:1601-1603`, `:1721`, `:1758`). The CRC length is four bytes shorter, so boot time does not change.

**Harness** (`sw/firmware/nvm_hosttest/nvm_host.c` at `af2165cb9`):

- `:182` adds `RF_SEAL`.
- `:543-556` `seal_slot()` rewrites the trailer, at the place the slot's length word names, over the faulty bytes. A length no container can have is left alone.
- `:587-588` applies it after the XOR.
- `:593-601` and `:886-887` add `--read-sealed SLOT:OFF:SKIP:COUNT[:BASE]`.

Every faulty read is a different container whose CRC closes.

**Cases** (`sw/firmware/nvm_hosttest/read_fault_cases.py` at `af2165cb9`):

- `:148-169` add the manners `sealed-entity` (byte 20, the entity ID's low byte, refused `VD_ENT`) and `sealed-body` (the record-area middle byte, refused `VD_REC` by the record's CRC-16). They join three groups: one valid slot faulted, both valid with the newer faulted, and both valid with the older faulted. A blank slot has no CRC to close.
- `:248` maps the manners to the option.
- `:286` gives the reference model's faulty read for a sealed manner: bytes no other read returns, like `--read-fault`.

They are crossed with every generated window, both orientations, the cold boot and the writer restart, with the group's sequences rotating through them as for every other manner.

The rotation alone left R603-4's exact class short of the sequence boundaries. That class is two sealed faulty reads that open one slot's judgement and then a clean read. A replay of the reference model's schedule (`scripts/r5/sealed_class_coverage.py`) found 20 of the 24 combinations missing a sequence (entry path × layout × orientation × faulted slot × manner). `de90ca768` closes that:

- `read_fault_cases.py:285`: `Expect.judgement` records each slot's judgement reads, "c" when a read returned the slot's bytes and "f" when not, filled at `:316-321`.
- `:249-265`: `faulted_slot()`, and `sealed_class()`, which adds, for every sealed manner and every sequence of the group, the two-read window that the model finds reads `ffc` in the faulted slot's judgement.
- `:241-245`: the generator adds those cases to the group's list where they are not already in it.

The replay now reports all 24 combinations at every sequence of their group (rc 0, `receipts/r5/logs__sealed_class_coverage.log`). Examples: on a cold boot with A valid and B blank, the class window is (1, 2); with B valid behind a blank A it is (3, 2); on a restart the windows are (0, 2) and (2, 2).

**Campaign:** 3,508 generated cases per shape. The model drops the same 86 as in round 4 (all-0xFF twice, accepted address faults). That leaves **3,422 per shape: 1,775 cold boots and 1,647 restarts**. Of those, 1,264 are sealed: 1,224 from the windows and 40 more from the class. No sealed case is outside the detection limit.

**Controls** (`read_fault_cases.py:21-122`):

- `r_digest_with_trailer` (`:50-59`) restores the round-4 digest line and the round-4 agreement. Restoring only the digest line would not be the defect, because the tail comparison alone separates sealed reads.
- The anchors of `generation_from_refused_slot` (`:33-37`), `verdict_only_agreement` (`:38-43`) and `r_digest_header_only` (`:44-49`) follow the new text. Their planted defects are unchanged.
- `test_nvm_firmware.py:46-71` counts nineteen controls, fourteen of them #671.

### Item 1 evidence: tests and the defects they catch

`python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test --jobs 4`, final, at `de90ca768`: rc 0 in 267.29 s, run alongside builder part 6. It covers five shapes at 3,422 cases each. All 49 controls are caught: five writer, 14 #671 × 3 shapes, and two boot-walk (`receipts/r5/logs__selftest_final.log`). The earlier run at `af2165cb9`, 3,382 cases with nothing else heavy running, before the captures started, took 217.84 s (`logs__selftest_wip1.log`). `r_digest_with_trailer` is caught by name on `endstation_arty_4x4`, `endstation_ax7101_1x1_tdm8` and `endstation_ax7101_8x8`. First finding: "slot A newer at seq 0x5a5a5, the other older, --read-sealed a:20:0:64:8 on a writer restart: slot A was taken as VD_ENT on reads that returned different bytes".

Full-count runs at `de90ca768` (`scripts/r5/plants_full.py`, no early stop, checks 13 and 14, `receipts/r5/logs__plants_final_<shape>.log`). The counts are identical on all three required shapes:

| Control | Planted defect | Named (restart / cold) | Oracle words |
|---|---|---|---|
| `restart_at_zero` | unread slot no longer holds | 48 (22 / 26) | was lost on the clean reboot |
| `unbounded_retry` | judgement retry unbounded | 56 (28 / 28) | over the bound |
| `generation_from_refused_slot` | generation from refused bytes | 8 (0 / 8) | generation was taken from a refused slot |
| `verdict_only_agreement` | verdict equality replaces byte agreement | 51 (25 / 26) | was lost on the clean reboot |
| `r_digest_header_only` | digest omits record bytes | 70 (31 / 39) | on reads that returned different bytes |
| **`r_digest_with_trailer`** | **round-4 trailer-inclusive digest** | **180 (82 / 98)** | **on reads that returned different bytes** |
| `r_fill_from_flash` | extra unjudged read fills the window | 1,705 (0 / 1,705) | want exactly |
| `r_restage_fail_offers_none` | failed newest re-stage skips the other slot | 66 (31 / 35) | yet the boot offered |
| `restage_fail_not_unread` | failed re-stage is not marked unread | 126 (61 / 65) | yet the boot line does not name it unread |
| `r_restage_any_seq` | accepts a different valid sequence | 11 (0 / 11) | another valid container than the one the boot offered |
| `r_reattach_goes_live` | re-attach hold alone is removed | 168 (168 / 0) | yet the writer re-attached live |
| `r_judge_four_tries` | judgement takes four reads | 230 (107 / 123) | want exactly |
| `p_restage_unbounded` | re-stage loses its bound | 80 (40 / 40) | want exactly |
| `r_restage_four_tries` | re-stage takes four reads | 96 (46 / 50) | want exactly |

At `af2165cb9`, before the class cases, the same runs gave 140 (62 / 78) for `r_digest_with_trailer`, with every other count as above except `verdict_only_agreement` 44 and `r_fill_from_flash` 1,685. The 40 class cases each catch the control.

**R603-4's probe, at the fix.**

- The unmodified `probe_refusal_digest.py` now fails its own defect assertion on its first case. 1x1, slot A: two sealed `VD_ENT` reads, then a clean third. The boot line reads `slot A VD_OK seq 370085 ... read faults=1 unread=0`. The commit goes to B at 370086; the clean reboot offers B at 370086 and loses no record. The probe stops at `assert lost > 0` (rc 1, `receipts/r5/logs__probe_original_final.log`).
- `scripts/r5/probe_all_cases.py` runs a copy whose two defect assertions are replaced, as text, by a record of each case. All four cases (1x1 and 8x8, slots A and B) read DEFECT GONE: acknowledged, not held, the change survives, 0 records lost. rc 0 (`logs__probe_all_final.log`).
- The same copy with `r_digest_with_trailer` planted reproduces R603-4's figures exactly: 53 and 163 records lost on slot A, and the change lost on slot B. rc 0, which here means all four defective (`logs__probe_all_plant_final.log`).

**Host-model speed (the hosted timeout).** All of check 13's time is spent inside the harness binary, and almost all of that in `settle()`: 282,043 calls in one 8x8 commit run, each walking 1,024 CSR words. `nvm_host.c:515-524` now returns from that walk after one `memcmp` when no word changed. When one did, the walk is unchanged, so `on_store` sees exactly the same stores in the same order.

- An 8x8 boot, change and commit run fell from 97.3 ms to 26.2 ms (median of 15).
- Equivalence (`scripts/r5/settle_equivalence.py`): every harness run of checks 1-14 and the disabled-writer and boot-walk graders, on 1x1, 8x8 and arty_4x4, ran on both the word-walk and the memcmp harness. Result: 10,581 twin runs, 0 differences in transcript (host addresses normalised) or in any dumped slot, window or stage file, and 0 findings.
- Local runtime fell from 461.48 s (round 4, 2,158 cases) to 217.84 s (3,382 cases, nothing else heavy running). At the final 3,422 cases it is 267.29 s, measured alongside a builder run.
- Hosted estimate: about 600 to 940 s, assuming hosted runs 2.7 to 3.5 times slower than local, as the old head's 594 s against 217 s and round 4's timeout imply. That is inside the builder's 1,200 s, so `test_builder.py` is unchanged. This is an estimate; the hosted exact-head result belongs to the manager.

### Item 2: the Mark II store's comparison (no change in this lane)

**Yes, `sw/firmware/ctrl_nvm` has the same residue collapse, and it reaches further than the shipping writer's did.**

- `sw/firmware/ctrl_nvm/nvm_store.c:165-166` start a read's digest at `0xffffffff`, count 0.
- `:142-149` `nvm_take` folds every port read into the digest without a final complement.
- `:167` takes the 40-byte header read; `:173` takes a second, separate read of the whole `img_len` container from the slot base.
- `:208-216` `nvm_agrees` compares verdict, digest and count; `:240` lets the second agreeing refusal stand.

After the header read the register depends only on those 40 bytes, say R. CRC is linear, so continuing from R over a container M‖C with C = CRC(M) leaves a value that depends only on R and the length. The container's own bytes cancel, wherever they differ: the entity, the record area, or anywhere else whose CRC closes. Only the separate header read and the length are distinguished.

`sw/firmware/ctrl_nvm/README.md:152-158` (Boot item 3) describes this digest, and `:496-499` claims it always tells apart reads that differ in one or two bits. Both are wrong for containers whose CRCs close.

Executed against the unchanged store (`scripts/r5/ctrl_nvm_seal.c` and `.py`, log `receipts/r5/logs__ctrl_nvm_seal.log`). The driver wraps the host flash model's read port and seals slot A's first two whole-container reads (byte ^ 1, then ^ 2). Slot A is valid at 0x5A5A5 and B is blank. On both 1x1 and 8x8:

| Case | Faulty boot | Commit | Clean reboot |
|---|---|---|---|
| clean control | A `VD_OK` 0x5A5A5, auth A | B at 0x5A5A6 | B 0x5A5A6 wins |
| entity byte, two sealed reads | A `VD_ENT` (5), `read_faults=0`, `unread=0`, phase IDLE, auth none | B at seq 1, acknowledged | A 0x5A5A5 wins; the commit is lost |
| record-area byte, two sealed reads | A `VD_REC` (7), `read_faults=0`, `unread=0`, phase IDLE, auth none | B at seq 1, acknowledged | A 0x5A5A5 wins; the commit is lost |

This is #671's loss on the Mark II store. It is reported for the manager to file, and nothing in `sw/firmware/ctrl_nvm` is changed here. FASTCONNECT section 7's normative sentence ("stands only when two of at most three reads return the same bytes") is the rule; the store's implementation does not meet it for these reads.

### Item 3: documentation

- `docs/integration/BAREMETAL_FIRMWARE.md:2023-2034` states the comparison exactly, why the last four bytes stay out of the CRC, and the detection limit. `:2182-2191` give the sealed faults and the control counts.
- `docs/design/SAVED_STATE_FASTCONNECT.md:796-799` (section 7) gives the shipping writer's comparison and why a whole-container digest fails. `:128` counts nineteen controls.
- `sw/firmware/nvm_hosttest/README.md:47-55` adds `--read-sealed`. `:112-129` adds the sealed manners to check 13's groups. `:144-146` gives 3,382 of 3,468 cases (1,627 / 1,755). `:193` counts fourteen #671 controls, and `:211` adds the `r_digest_with_trailer` row. `:259-264` gives the detection limit.

### Authoritative sequence, every shipping-path location (at `af2165cb9`; the firmware is unchanged after it)

The firmware is `sw/firmware/milan_baremetal/milan_baremetal.c`, sha256 `497845e6243b919638285ce4de18e6687beff6a509d72c8e2e2f2d45ba7b1bed`.

| File:line | Role |
|---|---|
| firmware:461 | RAM authority, `nvm_seq` |
| firmware:730 | `nvm_seq_of`, reads the sequence word |
| firmware:742 and :763 | `nvm_read_slot` copies one flash read into the stage and takes a sequence only after VD_OK; a refusal takes none (:764-770 records its count, digest and tail) |
| firmware:793, :804 and :815 | `nvm_judge_slot` returns the accepted read's sequence; an unread result has sequence zero |
| firmware:825 and :832 | the bounded re-stage requires VD_OK and the selected sequence |
| firmware:1492 | wrap-safe slot selection; A wins ties |
| firmware:1669-1675, :1679-1689, :1692, :1695, :1698 | both boot paths take each slot's verdict and sequence from judged reads, re-pick after a failed re-stage, assign the accepted sequence or zero, and set the authoritative slot |
| firmware:1601-1603, :1721 and :1758 | the hold, and its re-attach and cold-boot call sites |
| firmware:927-929 | publishes RAM authority through word 2; does not derive it |
| firmware:1395, :1426-1427 and :1441-1442 | the next generation is the accepted generation plus one; the target's verified sequence must match it; promotion follows verify and byte match |
| firmware:1954-1957 | console-only re-validation and sequence reads of current flash; does not feed RAM authority |
| `hdl/milan/KL_nvm_backend.sv:424,439,482,490,582` | word 2: definition, storage, reset, write and readback; no choice or arithmetic on it |
| `hdl/milan/KL_pp_shadow.sv:997` | the parent instantiates this backend on the processor's device face |
| `protocol-processor/hdl/top/protocol_processor_top.sv:2899` | instantiated record port |
| `protocol-processor/hdl/aecp/KL_aecp_engine.sv:2001` | instantiated D3 record writer |
| `protocol-processor/hdl/aecp/KL_aecp_nvm_writer.sv:16` and `hdl/packet_engine/KL_pp_nvm_port.sv:14` within that submodule | per-record framing and CRC-16; no slot-generation metadata or selection |

No `hdl/` file or gitlink changed in this round (`git diff --stat 7bc7ceca HEAD -- hdl protocol-processor` is empty). The processor is clean at `2ad2f845dd583f8310075fa2380cb60a04fd091a`; `git -C protocol-processor rev-parse --show-toplevel` named its own directory first. No submodule commit or adoption is needed.

### Firmware size

`receipts/r5/fw_size.txt`, produced by `scripts/r5/fw_size.sh` (round 4's, unchanged) with the product 1x1 generated headers:

| Compiler | Base text / bss | Round 4 | Round 5 | Round 5 delta | Total delta |
|---|---|---|---|---|---|
| pinned RV32 SDK, GCC 14.3.0 | 15,529 / 88 | 17,483 / 104 | 17,579 / 104 | text +96, bss 0 | text +2,050, bss +16 |
| local RV32-capable compiler, GCC 16.2.0 | 15,476 / 88 | 17,454 / 104 | 17,582 / 104 | text +128, bss 0 | text +2,106, bss +16 |

Data is 104 B throughout. The +96 B comes from the five-word read record passed by value and the tail load. This is an object-size comparison by the firmware Makefile's compile rule, not a ROM headroom claim.

### Capture re-measure

All six arms passed, with 16 captures each, for firmware sha256 `497845e6243b919638285ce4de18e6687beff6a509d72c8e2e2f2d45ba7b1bed`. They measured commit `bd42818d3` (tree `39e2b51c`); the firmware and capture inputs there are those of the final head. `scripts/r5/capture_driver.sh` (round 4's, unchanged) ran in two drivers of three arms, so at most two builds ran at once. Driver A ran 8x8-50-on, 8x8-50-off and 1x1-50-on; driver B ran 8x8-100-on, 8x8-100-off and 1x1-50-off. Between 10:47 and 12:49, every arm returned rc 0.

The receipt was regenerated only through `scripts/r5/assemble_receipt.py`, which runs the gate's `check_receipt` before writing. `scripts/r5/refresh_section18.py` then made 18 exact-once edits to `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 18. The receipt gate passes, and all four mutation controls (`bytes`, `records`, `clock`, `ignore-off-timing`) reject with the required rc 1.

| Shape | CPU MHz | Traffic | Measured min–max, ms | Floor ratio |
|---|---:|---|---:|---:|
| 1x1 | 50 | on | 3.96020–3.96548 | 12.3566x |
| 1x1 | 50 | off | 3.90676–3.92034 | 12.4989x |
| 8x8 | 50 | on | 13.84828–13.86328 | 3.5345x |
| 8x8 | 50 | off | 13.67538–13.68956 | 3.5794x |
| 8x8 | 100 | on | 10.41235–10.42973 | 4.6981x |
| 8x8 | 100 | off | 10.41246–10.41566 | 4.7045x |

- The 8x8 contract maximum is **13.86328 ms**, leaving **10.63672 ms** to the 24.5 ms limit, at a **3.5345x** ratio to the 49 ms floor.
- The 1x1 maximum is **3.96548 ms**, leaving **20.53452 ms**, at a **12.3566x** floor ratio.
- The non-contract 100 MHz 8x8 comparison maximum is **10.42973 ms**, against 10.43406 ms in round 4.
- The contract maxima are unchanged from round 4, as expected: the change is confined to the boot path, and `nvm_capture()` and the census are untouched.

Retained evidence is indexed by [the receipt manifest](receipts/r5/MANIFEST.md). [Capture artifact identities](receipts/r5/CAPTURE-ARTIFACTS.md) cover each arm's simulator, BIOS, firmware object and CPU netlist without copying build products here.

### Gate table

The final source head is `de90ca768`. The capture commit `0c276b621` follows it and changes only the receipt and the section 18 text. The firmware has been unchanged since `af2165cb9`, and the harness since `af2165cb9`. Receipts are in `receipts/r5/`, indexed by [the manifest](receipts/r5/MANIFEST.md).

| Command / receipt | Head | rc | Result / planted defect |
|---|---|---|---|
| `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test --jobs 4` / `logs__selftest_final.log` | `de90ca768` | 0 | Five shapes, 3,422 cases each, 49 controls; 267.29 s alongside builder part 6 |
| the same / `logs__selftest_wip1.log` | `af2165cb9` | 0 | 3,382 cases, 49 controls; 217.84 s |
| the same / `logs__selftest_wip2.log` | the uncommitted class change, before the parameter refactor | 0 | 3,422 cases, 49 controls; 279.12 s; the refactor leaves the case list identical |
| `scripts/r5/plants_full.py` / `logs__plants_final_<shape>.log` | `de90ca768` | 0 each | All 14 #671 controls named on arty_4x4, 1x1 and 8x8 with identical counts (table above) |
| the same / `logs__plants_full_<shape>.log` | `af2165cb9` | 0 each | Same, before the class cases |
| `scripts/r5/sealed_class_coverage.py` / `logs__sealed_class_coverage.log` | `de90ca768` | 0 | 24 combinations of the R603-4 class, each at every sequence of its group |
| `scripts/r5/settle_equivalence.py` / `logs__equiv-*.log` | `af2165cb9` content | 0 | 10,581 twin runs (1x1, 8x8, arty_4x4), 0 differences, 0 findings |
| R603-4 `probe_refusal_digest.py`, unmodified / `logs__probe_original_final.log` | `de90ca768` | 1 | Its own defect assertion fails on its first case: the defect is gone |
| `scripts/r5/probe_all_cases.py` / `logs__probe_all_final.log` | `de90ca768` | 0 | 4 of 4 cases DEFECT GONE |
| `scripts/r5/probe_all_cases.py ... r_digest_with_trailer` / `logs__probe_all_plant_final.log` | `de90ca768` | 0 | 4 of 4 DEFECT PRESENT with the control planted; R603-4's 53 / 163 records lost |
| `scripts/r5/ctrl_nvm_seal.py` / `logs__ctrl_nvm_seal.log` | unchanged `ctrl_nvm` | 0 | The Mark II store's collapse reproduced on 1x1 and 8x8; report only |
| `sw/builder/test_builder.py --require-elaboration --require-rv32` in six parts (`scripts/r5/builder_bank.sh`) / `builder__part1..6.log` | parts 1-5 `bd42818d3`; part 6 rerun `de90ca768` (`builder__part6_final.log`) | 0 all | All 101 functions in their order, every elaboration arm ran. Parts 1-5 never read the host suite; part 6 holds the writer gate |
| `make -C tb/verilator/nvm_cosim run JOBS=2 POOL=4` (Verilator 5.050, GNU make 4.3) / `vsuites__nvm_cosim.log` | `bd42818d3` | 0 | 465/465 checks, 39/39 named mutants killed |
| `make -C tb/verilator/fw_service_budget` / `vsuites__fw_service_budget.log` | `bd42818d3` | 0 | 14 flash and 55 oracle checks; dispatch removal caught |
| firmware-unit replica, 7 steps (`scripts/r5/firmware_unit_replica.sh`) / `fwunit__replica.log` | `bd42818d3` to `de90ca768` | 0 all | Tally, SDK and RV32 self-tests, controller bank, `test_ctrl_nvm.py --require-rv32` (435 tests, five shapes), coverage self-test and check |
| rtl-fast lint/BDD replica, 5 steps / `rtlfast__replica.log` | `de90ca768` | 0 all | Scope controls, Verilator 5.050 lint with self-test, source lists, BDD |
| docs-check replica, 81 positions (`scripts/r5/docs_replica.sh`) / `docsrep__replica.log` | `de90ca768` | 0 all run | 78 run; 35 (builder), 38 (capture gate) and 39 (writer gate) have the separate receipts above and below |
| `scripts/check_feature_status.py` and `--self-test`; `scripts/check_nvm_record_space.py` and `--self-test` | `bd42818d3` | 0 each | The feature status reads the firmware |
| C and Python idiom, hygiene, `docs_check.py`, `gen_toc.py --check`, doc style and paths, `git diff --check` | each commit | 0 each | The Python ratchet first refused the seven-parameter `sealed_class`; it now takes the group, and the ratchet holds at 7 |
| Six capture arms (`capture__driver-a.log`, `capture__driver-b.log`), `assemble_receipt.py`, `refresh_section18.py`, `scripts/r5/final_gates.py` (`final_gates__final_gates.log`) | measured `bd42818d3`; gates at `0c276b621` content | 0; the four mutation arms 1 as required | 96 clean captures; the receipt binds the final firmware; capture, idiom, hygiene, docs, TOC, style, paths and diff checks pass; `check_em_dash.py --base e8454e27` rc 0 at `0c276b621` |

Not run by this lane: act against an unpublished head; hosted contexts for the new commits; a current-dev merge-candidate bank; physical hardware, bench or flash writes; unrelated exhaustive RTL or Yosys sweeps. There is no RTL, generator, register-map, record-format or gitlink change, and no Makefile changed. The changed-file consumers are the host writer gate, the builder, the Mark II store suite (it imports the host suite), the feature-status gate, capture, co-simulation, the service budget, and the documentation and hygiene gates. `scripts/act_ci.py --selftest` is not run on the host, as AGENTS.md requires. The manager must publish the head and obtain exact-head hosted and act evidence, independent re-review, and candidate validation. The hosted writer gate under the builder's 1,200 s is the first thing to read at the new head.

### Open risks (round 5)

- The hosted writer-gate runtime is estimated, not measured: 3,422 cases in 267.29 s locally, alongside a builder run. If hosted runs more than about 4.4 times slower than local, the builder's 1,200 s would still be exceeded. The harness change is equivalence-checked, so raising the limit would then be the remaining lever.
- The comparison is a 32-bit digest plus four exact bytes. Two refused reads differing in three or more scattered bits can collide, with a probability of about 2^-32. The suites document this beside the repeated-identical-bytes and accepted-address limits.
- The Mark II store's collapse (item 2) is open and reproduced; this lane does not change it.
- R602-4-S1 (the `read faults=` count is not graded) and S2 (no case faults both slots) remain optional SUGGESTIONs.
- Runtime prefill's fresh flash read remains #717.

Public Round 5 handoff: [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6108259934).

## Round 6

Status: REVIEW READY at `c7d0ad63510cf1aaee41ef440675d110ad2730d7` on `671-read-fault`, from `0c276b621d638c9a83e82f71fbf07bc153517bf7` (new commits only, no rebase or amend, not pushed). No STOP condition arose: the production comparison did not have to change.

- Assignment: #671 comment 6112358549. Reviews answered: PR #715 comments 6112353068 (R602-5, NEGATIVE, F1) and 6112253974 (R603-5, NEGATIVE, F1). Both report one MAJOR: no standing fault differs only in the trailer, so the trailer comparison can be removed with every grader green.
- The probes were read as data from `origin/671-review-evidence` at `d40737c1`. `probe_comparison.py` (sha256 `73c7970b...`) and `probe_r602_5.py` (`7cb5544f...`) match both packets' `MANIFEST.sha256`.
- Hosted checks at `0c276b62`: all 22 executed contexts succeeded, and `Physical gPTP` was skipped. The standalone hosted `test_nvm_firmware.py --self-test` step in `docs-check` took 356 s (11:27:09 to 11:33:05). The builder step that also runs it passed inside its 1,200 s limit.

### Commits of this round

| Commit | Change |
|---|---|
| `793641131` | host suite: the comparison's four terms listed once; per term, a check-13 class of two reads differing in that term alone and a control removing it; the comparison check; the harness's `--read-length`, `--read-verdict` and end-relative byte offsets |
| `c7d0ad635` | docs: the host-suite README, FASTCONNECT section 7 and the firmware page |

The firmware is unchanged. `git diff 0c276b62 HEAD -- sw/firmware/milan_baremetal` is empty, and its sha256 is still `497845e6243b919638285ce4de18e6687beff6a509d72c8e2e2f2d45ba7b1bed`. No `hdl/`, gitlink, `syn/`, `constraints/`, `configs/`, Makefile or workflow file changed.

### The finding

The writer compares two refused reads by `a.vd == b.vd && a.bytes == b.bytes && a.digest == b.digest && a.tail == b.tail` (`sw/firmware/milan_baremetal/milan_baremetal.c:778-779`). At `0c276b62` every generated byte fault changed bytes before the trailer, and every sealed fault changed the prefix and the trailer together. No case's two faulty reads differed in the trailer alone, so R603-5's plant (`a.tail == b.tail;` replaced by `1;`) and R602-5's `no_tail` and `digest_short` plants left checks 13 and 14 at 0 findings. That plant brings back #671's lost commit for a fault confined to the trailer.

### Item 1: the terms, listed once

`sw/firmware/nvm_hosttest/read_fault_cases.py` at `c7d0ad635`:

- `:18-29` `COMPARISON` lists the four terms: the name, the firmware's spelling, and the manner of fault whose faulty reads differ in that term alone. `AGREE_RE` finds `nvm_reads_agree`'s return expression in the firmware.
- `:32-39` `control_of(term)` names a term's control (`r_omit_<term>`), and `alone_in(term)` gives the words its findings carry ("which differ only in their <term>").
- The classes (`term_class`), the controls (`READ_FAULT_MUTATIONS`), the diagnostic (`judged`) and the check (`comparison_findings`) all iterate `COMPARISON`. None of them names a term on its own.

### Item 2: one fault class per term

Each term's manner (`read_fault_cases.py:24-27`, offsets `:191-196`) and the harness view behind it (`sw/firmware/nvm_hosttest/nvm_host.c` at `c7d0ad635`):

| Term | Manner | The faulty reads (`nvm_host.c`) |
|---|---|---|
| verdict | `--read-verdict SLOT:SKIP:COUNT` | `:594-598`, `:628-631`: the n-th faulty read XORs the low byte of the entity, model or record-layout word (offsets 20, 28 and 36, in turn). The four bytes before the trailer are then forged so the CRC-32 closes on the slot's own trailer value. Same byte count, same prefix CRC, same trailer, and the verdicts `VD_ENT`, `VD_SHAPE` and `VD_REC` in turn. |
| byte count | `--read-length SLOT:SKIP:COUNT` | `:623-627`: the length word grows by four on every faulty read, and the slot's trailer value moves to the end that length names. The prefix CRC is forged to that value's complement. Every read is `VD_CRC` with the same prefix CRC and trailer and another byte count. |
| prefix CRC | `--read-fault SLOT:-5:SKIP:COUNT:8` | `:632-635`: the last byte before the trailer XORed with another value on every read. `VD_CRC`, same count, same trailer, another prefix CRC. |
| trailer | `--read-fault SLOT:-1:SKIP:COUNT:8` | the same, on the trailer's last byte. `VD_CRC`, same count, same prefix CRC, another trailer. These are the trailer-only XOR views the assignment names. |

Harness changes:

- **Negative offsets.** A `--read-fault` or `--read-sealed` offset below zero counts back from the end of the container the slot's length word names (`nvm_host.c:181-183`, `:633`). It is resolved at each faulty read, as the firmware places its own trailer.
- **The forge.** `forge_crc` (`:580-592`) sets four bytes so that the CRC-32 over everything before them and them is a chosen value. It runs the register back 32 shifts and XORs the register in front of them. It was checked against `zlib.crc32` on 2,000 random prefixes before it was written in C.
- **Refusing misuse.** A fault placed by the container's end, or a length or verdict fault, on a slot whose length word names no container exits 2 (`:609-615`). It does not read out of the slot.
- **Arguments.** `arm_read_fault` (`:665-698`) parses signed values and refuses a negative SKIP or COUNT.
- **Refactor.** The view code moved into `fault_slot` (`:600-637`), which `nvm_host_flash_base` calls (`:660`). The old modes' bytes are unchanged; see the equivalence below.

**Placement.** `term_class` (`read_fault_cases.py:299-311`) adds, for each term and each sequence of every group whose faulted slot holds a container, the two-read window that the reference model finds opens that slot's judgement as faulty, faulty, clean (`ffc`). It does so both ways round and on both entry paths:

- one slot valid and the other blank, faulted valid: sequences 1, 0x5A5A5, 0x80000000 and 0xFFFFFFFF, 16 cases per term;
- both valid, faulted newer, and both valid, faulted older: 0x5A5A5 and 0 (the wrap, the older at 0xFFFFFFFF), 8 cases each.

That is 32 cases per term per shape and 128 in all. `fault_cases` (`:276`) gives each (entry path, group, orientation) its term list beside its group list. The lists are interleaved, so the four terms first appear at case indexes 1, 29, 57 and 85 of 3,550. The order does not depend on the shape, whose record-area byte only moves the body offset (`scripts/r6/term_census.py`, `receipts/r6/term_census.log`).

**Assertions.** Every class case goes through `grade_fault_case`, so it keeps the exact read count (`read_findings`), the hold (`hold_findings`), the boot line and the window (`boot_findings`), and the changed record and the other records on the clean reboot (`reboot_findings`). The reference model maps both new options to a refused read that no other read returns (`read_fault_cases.py:417-419`). A judgement's reads are consecutive, so any two of `--read-verdict`'s three words in turn differ.

**Diagnostic.** `judged` (`:463-469`) adds ", which differ only in their <term>" to "was taken as <verdict> on reads that returned different bytes" on the faulted slot of a term-class case. `term_of` (`:314-320`) derives the term from the case's fault, not from a label.

**What the classes hand the writer** (`scripts/r6/term_views.py`, log `receipts/r6/term_views.log`). A probe copy of the firmware, never the tree's, prints each read's slot and four terms. On `endstation_arty_4x4`, `endstation_ax7101_1x1_tdm8` and `endstation_ax7101_8x8`, all 32 cases of each term, 384 in all, give the faulted slot's judgement two refusals that differ in their own term and in no other, then `VD_OK`. 1x1 examples:

| Term | First refusal (vd, bytes, digest, tail) | Second | Third |
|---|---|---|---|
| verdict | 5, 3336, e27cfdc8, e27cfdc8 | 6, 3336, e27cfdc8, e27cfdc8 | VD_OK |
| byte count | 4, 3340, 1d830237, e27cfdc8 | 4, 3344, 1d830237, e27cfdc8 | VD_OK |
| prefix CRC | 4, 3336, eca775fa, e27cfdc8 | 4, 3336, 9ba0456c, e27cfdc8 | VD_OK |
| trailer | 4, 3336, e27cfdc8, ea7cfdc8 | 4, 3336, e27cfdc8, eb7cfdc8 | VD_OK |

The verdict and byte-count classes are constructed CRC-32 collisions. Outside the harness, two reads that agree in count, prefix CRC and trailer but not in verdict would need such a collision. They exist so that each term is pinned by a test that can fail for it. They do not claim that such faults are common.

**Campaign.** 3,636 generated cases per shape. The model drops the same 86 as before (all `0xFF` twice, accepted address faults). That leaves **3,550 per shape: 1,839 cold boots and 1,711 restarts**, 128 of them term-class cases. All 3,550 are distinct.

### Item 3: one control per term

`READ_FAULT_MUTATIONS` (`read_fault_cases.py:143-145`) generates four controls from `COMPARISON`. Each replaces one term's spelling in a copy of the firmware with `1`, the identity of `&&`, and keeps the other three. Each must be caught by its own words. Each spelling occurs exactly once in the firmware, and the plant refuses an anchor that does not.

| Control | Planted defect | Words | Named, full count (restart / cold), each of the three shapes |
|---|---|---|---|
| `r_omit_verdict` | `a.vd == b.vd` removed | "which differ only in their verdict" | 32 (16 / 16) of 78 findings |
| `r_omit_byte_count` | `a.bytes == b.bytes` removed | "which differ only in their byte count" | 32 (16 / 16) of 78 |
| `r_omit_prefix_crc` | `a.digest == b.digest` removed | "which differ only in their prefix CRC" | 32 (16 / 16) of 706 |
| `r_omit_trailer` | `a.tail == b.tail` removed | "which differ only in their trailer" | 32 (16 / 16) of 78 |

`r_omit_prefix_crc` also reddens the ordinary byte faults (706 findings in all), because a magic, sequence or record-area byte fault also differs in the prefix alone. Only its own class names the term.

**The cross matrix** (`scripts/r6/term_matrix.py`, `receipts/r6/term_matrix.log`, three shapes). Every term class is clean at the head. Each control is named by all 32 cases of its own class, and by none of the other three classes. The diagonal is complete, the other 36 cells have 0 failing cases, and 14 of each class's 32 cases also lose saved state on the clean reboot.

The self-test catches each new control on the first shape and both product shapes, within 1 or 2 named findings before its early stop:

- `r_omit_verdict`: "slot A valid at seq 0x1, --read-verdict a:0:2 on a writer restart: slot A was taken as VD_SHAPE on reads that returned different bytes, which differ only in their verdict";
- `r_omit_trailer`: "slot B valid at seq 0x1, --read-fault b:-1:2:2:8 on a writer restart: slot B was taken as VD_CRC on reads that returned different bytes, which differ only in their trailer".

All eighteen #671 controls, full count, no early stop (`scripts/r6/plants_full.py`, `receipts/r6/plants_b{1,2,3}_<shape>.log`). The counts are identical on all three required shapes:

| Control | Named (restart / cold) | Change from round 5 |
|---|---|---|
| `restart_at_zero` | 48 (22 / 26) | same |
| `unbounded_retry` | 56 (28 / 28) | same |
| `generation_from_refused_slot` | 8 (0 / 8) | same |
| `verdict_only_agreement` | 63 (31 / 32) | 51 before; the byte count, prefix CRC and trailer classes now also lose state under it |
| `r_digest_header_only` | 102 (47 / 55) | 70 before; the prefix CRC class adds 32 |
| `r_digest_with_trailer` | 180 (82 / 98) | same |
| `r_fill_from_flash` | 1,769 (0 / 1,769) | 1,705 before; 64 more cold boots |
| `r_restage_fail_offers_none` | 66 (31 / 35) | same |
| `restage_fail_not_unread` | 126 (61 / 65) | same |
| `r_restage_any_seq` | 11 (0 / 11) | same |
| `r_reattach_goes_live` | 168 (168 / 0) | same |
| `r_judge_four_tries` | 230 (107 / 123) | same |
| `p_restage_unbounded` | 80 (40 / 40) | same |
| `r_restage_four_tries` | 96 (46 / 50) | same |
| `r_omit_verdict` | 32 (16 / 16) | new |
| `r_omit_byte_count` | 32 (16 / 16) | new |
| `r_omit_prefix_crc` | 32 (16 / 16) | new |
| `r_omit_trailer` | 32 (16 / 16) | new |

### Item 4: a check fails when a term has no class or no control

`comparison_findings` (`read_fault_cases.py:323-347`) runs in `main()` for every shape against the firmware as shipped (`test_nvm_firmware.py:972-973`). It fails in three situations:

- the firmware's `nvm_reads_agree` compares by other terms than `COMPARISON` lists (a term added to or removed from the firmware);
- a listed term has no class case at one of the places item 2 names, by group, orientation, sequence and entry path;
- a listed term has no control, or its control does not remove exactly that term with that term's words.

It does not run inside the behavioural graders, so a planted copy is caught by behaviour, not by this text check. That keeps the reviewers' probe counts behavioural.

`comparison_self_test` (`:350-370`, called at `test_nvm_firmware.py:985`) requires the check to fail by its own words in nine situations:

- each term with its class taken out of the campaign: "the comparison's trailer has no fault class at 32 place(s)";
- each term with its control taken out: "... has no control that removes it alone";
- a firmware comparing by a fifth term (`&& a.seq == b.seq`): "the firmware compares two refused reads by ... && a.seq == b.seq, but the terms listed are ...".

All nine print "self-test OK".

### Item 5: the production comparison

Unchanged, so no STOP. The firmware file is byte-identical to `0c276b62`.

### Item 6: the reviewers' probes, re-run at `793641131` (the source of `c7d0ad635`)

Both probes ran with `python -I` under CPython 3.12.3, the tree passed as an argument, and the work under scratch.

- **R603-5 `probe_comparison.py ROOT --jobs 4`** (`receipts/r6/r603_5_probe_comparison.log`): rc 0 in 125 s. Its own assertions hold: 0 failing head cases, all 16 trailer-only cases failing under `omit_tail`, and all 32 sealed cases failing under `inclusive_crc`. The standing suite now gives **78 findings under `omit_tail` on each of the three shapes** (0 at `0c276b62`). Its `comparison.json` (sha256 `6c401273...`, 181,701 B, kept in scratch) breaks these down (`receipts/r6/r603_5_standing_summary.log`): 32 carry "which differ only in their trailer", 4 lose the change and 10 lose other records on the clean reboot.
- **R602-5 `probe_r602_5.py TREE WORK --mutants no_tail,digest_short --sets none --standing`**, its own verification line (`receipts/r6/r602_5_probe_standing.log`): rc 0. **`no_tail`: 78 findings on each shape. `digest_short`: 78 on each shape**, named "which differ only in their prefix CRC" (the class's byte is the last before the trailer). Both were 0 at `0c276b62`.
- **R602-5's trailer set** (`--sets trailer`, in two runs, `r602_5_probe_trailer_{a,b}.log`): 2,400 cases per shape. Head: 0 findings. `no_tail`: 500 (24 lost). `digest_short`: 250 (12 lost). `trailer_in`: 0, which R602-5 expected (equivalent). These match R602-5's figures at the old head, as they must with the firmware unchanged. This set is the probe's own, not the standing suite.

### Harness equivalence

`scripts/r6/harness_equivalence.py` ran every harness run of checks 1-14, the disabled-writer and the boot-walk graders on 1x1, arty_4x4 and 8x8 twice: on the round-6 harness and on `0c276b62`'s.

- **Result:** 10,641 twin runs with 0 differences in transcript (host addresses normalised) or in any dumped slot, window or stage file, and 0 findings (`receipts/r6/equiv_1x1_arty.log`, `equiv_8x8.log`).
- **Not compared:** 384 runs use `--read-length`, `--read-verdict` or an end-relative offset, which the old harness cannot take. They ran on the new harness only and are counted apart.

### Authoritative sequence, every shipping-path location

The firmware is byte-identical to `0c276b62` and `af2165cb9`, so round 5's table holds line for line at this head:

- firmware `:461`, `:730`, `:742`/`:763`, `:793`/`:804`/`:815`, `:825`/`:832`, `:1492`, `:1669-1698`, `:1601-1603`/`:1721`/`:1758`, `:927-929`, `:1395`/`:1426-1427`/`:1441-1442` and `:1954-1957`;
- `hdl/milan/KL_nvm_backend.sv:424,439,482,490,582`;
- `hdl/milan/KL_pp_shadow.sv:997`;
- `protocol-processor/hdl/top/protocol_processor_top.sv:2899`, `hdl/aecp/KL_aecp_engine.sv:2001`, `hdl/aecp/KL_aecp_nvm_writer.sv:16` and `hdl/packet_engine/KL_pp_nvm_port.sv:14`.

The lines were spot-read at `c7d0ad635`. No processor change is needed. `git -C protocol-processor rev-parse --show-toplevel` names its own directory, and the gitlink is `2ad2f845dd583f8310075fa2380cb60a04fd091a` as before.

### Firmware size and capture

- **Size:** no change this round. The firmware source is byte-identical, so round 5's figures stand: pinned RV32 SDK text 17,579 B and bss 104 B, +2,050 B and +16 B over the base.
- **Capture:** not re-measured. Nothing the capture measures changed. The receipt still binds firmware sha256 `497845e6...`, and its gate runs in the sweep below.

### Hosted writer-gate time (estimate)

At `0c276b62` the standalone hosted writer-gate step took 356 s for 3,422 cases. Locally that suite took 217.84 s alone and 267.29 s beside a builder run, so hosted ran about 1.3 to 1.6 times local. This round's suite (3,550 cases, 61 planted firmware defects and nine comparison-check arms) took 275.27 s locally at four jobs, beside the firmware-unit replica, on a shared host at load 57 to 72. That gives an estimated hosted 370 to 450 s, inside the builder's 1,200 s. Inside the builder (part 6) it passed in a 357.34 s part. This is an estimate; the hosted exact-head result belongs to the manager.

### Gate table

Final head `c7d0ad63510cf1aaee41ef440675d110ad2730d7`. Python is CPython 3.12.3 (the scratch venv with the workflow's pinned requirements), Verilator is 5.050 and GNU make is 4.3. Receipts are in `receipts/r6/`, indexed by [the manifest](receipts/r6/MANIFEST.md), with local paths normalized.

| Command / receipt | Head | rc | Result / planted defect |
|---|---|---|---|
| `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test --jobs 4` / `selftest_final.log` | `c7d0ad635` | 0 | 5 shapes at 3,550 cases; 61 planted firmware defects reddened (5 writer, 18 #671 × 3 shapes, 2 boot-walk) and 9 comparison-check arms failed by name; 275.27 s |
| the same / `selftest_wip1.log` | `793641131` content | 0 | the same; 259.47 s |
| `scripts/r6/plants_full.py` / `plants_b{1,2,3}_<shape>.log` | `c7d0ad635` | 0 each | All 18 #671 controls named on arty_4x4, 1x1 and 8x8 with identical counts (table above) |
| `scripts/r6/term_matrix.py` / `term_matrix.log` | `c7d0ad635` | 0 | Head clean; each `r_omit_` control named by its own class's 32 cases and by no other class, three shapes |
| `scripts/r6/term_views.py` / `term_views.log` | `c7d0ad635` | 0 | 384 of 384 class cases hand the judgement two refusals differing in their own term alone, then VD_OK |
| `scripts/r6/term_census.py` / `term_census.log` | `c7d0ad635` | 0 | 3,550 distinct cases, 128 in the classes, every term at every required place, comparison check clean |
| `scripts/r6/harness_equivalence.py` / `equiv_1x1_arty.log`, `equiv_8x8.log` | `793641131` content against `0c276b62` | 0 | 10,641 twin runs, 0 differences, 0 findings; 384 new-harness-only runs |
| R603-5 `probe_comparison.py` / `r603_5_probe_comparison.log`, `r603_5_standing_summary.log` | `793641131` | 0 | Own assertions hold; `omit_tail` standing 78 findings per shape (was 0), 32 naming the trailer class |
| R602-5 `probe_r602_5.py --mutants no_tail,digest_short --sets none --standing` / `r602_5_probe_standing.log` | `793641131` | 0 | `no_tail` 78, `digest_short` 78 findings per shape (both were 0) |
| R602-5 `probe_r602_5.py --sets trailer` / `r602_5_probe_trailer_{a,b}.log` | `793641131` | 0 | head 0; `no_tail` 500 (24 lost); `digest_short` 250 (12 lost); `trailer_in` 0 (equivalent) |
| `sw/builder/test_builder.py --require-elaboration --require-rv32` in six parts (`scripts/r6/builder_bank.sh`) / `builder__part1..6.log` | `c7d0ad635` | 0 all | All 101 functions; part 6 holds the writer gate (357.34 s). The two NOT RUN entries are round 5's: a MAKEFLAGS mutation this make cannot observe, and a calibration report not on disk |
| `make -C tb/verilator/nvm_cosim run JOBS=2 POOL=4` / `vsuites__nvm_cosim.log` | `c7d0ad635` | 0 | 465/465 checks, 39/39 named mutants killed |
| `make -C tb/verilator/fw_service_budget` / `vsuites__fw_service_budget.log` | `c7d0ad635` | 0 | 55 oracle checks; dispatch census |
| firmware-unit replica, 7 steps (`scripts/r6/firmware_unit_replica.sh`) / `fwunit__*.log` | `c7d0ad635` | 0 all | Tally, SDK and RV32 self-tests, the controller bank with its self-test, `test_ctrl_nvm.py --require-rv32` (the Mark II store, which imports the host gate: 435 tests, five shapes), coverage self-test and check |
| rtl-fast lint/BDD replica, 5 steps / `rtlfast__replica.log` | `c7d0ad635` | 0 all | Scope self-test, Verilator 5.050 lint with self-test, source lists, BDD |
| docs-check replica, 81 positions (`scripts/r6/docs_replica.sh`) / `docsrep__replica.log` | `c7d0ad635` | 0 all run | 78 run; 35 (builder), 38 (capture gate) and 39 (writer gate) have the separate receipts above and below |
| `scripts/r6/final_gates.py` / `final_gates__*.log` | `c7d0ad635` | 0; the four capture mutation arms 1 as required | Capture receipt gate, C and Python idiom, hygiene, docs, TOC, doc style and paths, `git diff --check` and against `e8454e27` |
| `scripts/check_em_dash.py --base e8454e27` | `c7d0ad635` | 0 | 0 findings over 349 added lines in 5 pages |
| `scripts/check_feature_status.py` and `--self-test`, `scripts/measure_test_evidence.py --check` | the working tree of `c7d0ad635` | 0 each | |

Not run by this lane:

- act against an unpublished head, and the hosted contexts for the new commits;
- a current-dev merge-candidate bank;
- physical hardware, bench or flash writes;
- the exhaustive RTL and Yosys sweeps, which this change does not reach;
- capture, because the firmware is byte-identical.

There is no RTL, generator, register-map, record-format, gitlink, Makefile or workflow change. `scripts/act_ci.py --selftest` is not run on the host, as AGENTS.md requires. The manager must publish the head and obtain exact-head hosted and act evidence, independent re-review and candidate validation.

### Open risks (round 6)

- The verdict and byte-count classes are constructed CRC-32 collisions in the host model. They make each term's removal fail a test. Their frequency on hardware is not claimed.
- The hosted writer-gate time is estimated (370 to 450 s), not measured at the new head.
- Each term class runs at the judgement's first two reads (`ffc`), as assigned, not over every window. Ordinary byte faults over every window also exercise the prefix CRC term, but not by it alone.
- Unchanged from round 5: the 2^-32 collision limit; the Mark II store's collapse (reported, not filed by this lane); R602-4-S1 and S2 remain optional; runtime prefill remains #717.


Public Round 6 handoff: [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6113473756).

## Round 7

Status: REVIEW READY at `9b32002cc0c3aafae9e864af7b4f08c1089a188a` on `671-read-fault`, two new commits on `c7d0ad63`: the merge commit `44416838` (parents `c7d0ad63` and dev `c6bd08c6`) and the capture re-measure `9b32002c`. No push, rebase or amend. No STOP condition arose: the conflicts touched only the two named files, and the merged capture meets its bound (13.86328 ms against 24.5 ms).

- Assignment: #671 comment 6125761347: merge dev `c6bd08c6` with a merge commit, resolve the snapshot-ownership design so both sides' statements stand, re-measure the capture through `tb/verilator/nvm_capture_cpu/run.py` instead of merging `measurements.json` by hand, change nothing else, and re-run round 6's bar at the merge head.
- `git fetch origin dev` gave `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`. The merge base is still `e8454e27`.

### Commits of this round

| Commit | Change |
|---|---|
| `44416838b90c40536a2104ab1f2bd4ff02268bec` | Merge commit of dev `c6bd08c6` into `c7d0ad63`. The design document is resolved so that both sides' statements stand, and the branch's capture receipt is kept unchanged until the re-measure. |
| `9b32002cc0c3aafae9e864af7b4f08c1089a188a` | The capture receipt, re-measured at `44416838` through `run.py`, and the section 18 figures and identities that state it. Only those two files change. |

There is no rebase or amend, and nothing is pushed. These checks were run at `9b32002c`:

- The files that differ from dev (`git diff --name-only c6bd08c6 HEAD`) are exactly the branch's own 15 files (`git diff --name-only e8454e27 c7d0ad63`).
- Of those 15, three differ from `c7d0ad63`: the two above and `sw/builder/test_builder.py`. Both sides changed that file and it merged without conflict. Its hunks against dev are exactly the branch's (`git diff -U0`, added and removed lines compared), and its hunks against `c7d0ad63` are exactly dev's.
- The other 12 files, the firmware included (sha256 `497845e6...`), are byte-identical to `c7d0ad63`.
- No `hdl/`, gitlink, register-map, record-format, Makefile or workflow change is this branch's. The gitlink and RTL differences against `c7d0ad63` are all dev's.

### The merge

`git merge --no-ff --no-commit c6bd08c6` reported conflicts in exactly the two files the assignment names, `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` and `tb/verilator/nvm_capture_cpu/measurements.json`. No STOP condition arose. Dev and the branch also both change `sw/builder/test_builder.py`, which merged without conflict. Dev moves two gitlinks: `gptp-processor` from `5dce647a` to `7dda9c3b`, and `third_party/lwSRP` from `9197193e` to `08ee86e8`. `protocol-processor` stays `2ad2f845`. After the commit, `git submodule update --init gptp-processor third_party/lwSRP` checked both out. `git -C <dir> rev-parse --show-toplevel` names each submodule's own directory.

**`measurements.json`.** Not merged by hand. Neither side's receipt fits the merged tree:

- the branch's binds firmware `497845e6...` but `run.py` `1bddc676...`, and dev's #621 change replaced `run.py` (now `c230cb3e...`);
- dev's binds `run.py` `c230cb3e...` but firmware `a73ecc25...`, the firmware before #671.

The merge commit keeps the branch's receipt unchanged (`git checkout --ours`), so at that commit alone `check_nvm_capture` fails on the harness hash. The next commit replaces the receipt with the re-measure at the merge commit. That re-measure is the only receipt that binds the merged tree.

**The design document.** Four conflicts, all in section 18 (capture timing) and UNRESOLVED 6. The resolution keeps every statement of both sides:

- **Timing provenance.** The branch's #671 chain stands (rounds 5, 4, 3, 2 and the assignment). Dev's #621 statements stand, attributed to dev's receipt: the #621 final ruling and its measured commit, tree, firmware, protocol-processor pin and gPTP-processor pin; the #621 base `5603c353` writing byte-identical logs; and the capture-SoC RTL drift attribution. The shared #629 and #70 lines appear once. The current-receipt identity lines describe the receipt the commit keeps, so the branch's round-5 receipt gets a `gPTP-processor pin: 5dce647a...` line, the pin it was measured at.
- **The worst 8x8 figure.** The branch's 13.86328 ms stands as current. Dev's 13.86318 ms (3.5345x, 10.63682 ms margin) is recorded as the #621 receipt's. "The previous census measured 13.23352 ms" (dev) and "The census before #629 measured 13.23352 ms" (the branch) state one fact, kept once in the branch's wording.
- **The six-row table.** The branch's table stands as current. Dev's six rows follow under "The #621 receipt on dev, at the same census and clocks".
- **UNRESOLVED 6.** The branch's figures stand as current. Dev's maximum and margin are added as the #621 receipt's.

Dev's non-conflicting additions merged as they were: the receipt-opt-out sentence in section 18's gate paragraph, the `check_nvm_capture.py` opt-out control and `run.py`'s production-only bound. The capture commit then updates only the current-receipt figures and identities (see below). Both earlier receipts stay as history.

### Capture re-measure

The recipe is `tb/verilator/nvm_capture_cpu/run.py`, run as its README states: `--captures 16`, `--cpu-hz 50000000` for both shapes and `100000000` for the 8x8 comparison, both traffic arms, in a network namespace, offline, with `PYTHONHASHSEED=0` and the product environment.

- **Drivers.** `scripts/r7/capture_driver.sh` (round 5's, unchanged) ran in two drivers of three arms at the clean merge commit `44416838`, so at most two builds ran at once.
  - Driver A: 8x8-50-on 16:02:49 to 16:49:11, 8x8-50-off to 17:33:38, 1x1-50-on to 17:42:31.
  - Driver B: 8x8-100-on 16:02:59 to 17:01:34, 8x8-100-off to 17:50:34, 1x1-50-off to 17:59:55.

  Every arm returned rc 0, with 16 graded captures. The run logs name Verilator 5.052, the simulator the receipt records.
- **Assembly.** The receipt was written only by `scripts/r7/assemble_receipt.py`, which is round 5's with this round's provenance. It refuses unless HEAD is the measured commit and the tree is clean. It takes each arm's `measurement.json` verbatim, hashes the per-arm identities from the build products, and recomputes the census, harness hashes and maxima through `scripts/check_nvm_capture.py`'s own functions. It then runs that gate's `check_receipt` before writing.
- **Section 18.** `scripts/r7/refresh_section18.py` then made 17 exact-once edits to section 18 and UNRESOLVED 6. A dry run against a synthetic receipt in a scratch clone checked every anchor first.

| Shape | CPU MHz | Traffic | Measured min to max, ms | Floor ratio |
|---|---:|---|---:|---:|
| 1x1 | 50 | on | 3.96020 to 3.96548 | 12.3566x |
| 1x1 | 50 | off | 3.90676 to 3.92034 | 12.4989x |
| 8x8 | 50 | on | 13.84828 to 13.86328 | 3.5345x |
| 8x8 | 50 | off | 13.67538 to 13.68956 | 3.5794x |
| 8x8 | 100 | on | 10.41235 to 10.42973 | 4.6981x |
| 8x8 | 100 | off | 10.41246 to 10.41566 | 4.7045x |

- **The bound holds.** The 8x8 contract maximum is **13.86328 ms**, which leaves **10.63672 ms** to the 24.5 ms limit, a **3.5345x** ratio to the 49 ms floor. The 1x1 maximum is 3.96548 ms (12.3566x), and the non-contract 100 MHz 8x8 maximum is 10.42973 ms.
- **The figures repeat round 5 exactly.** All 96 captures have the system-cycle counts of the #671 round-5 receipt (`bd42818d`), capture for capture. The assembler computes and states this. They differ from dev's #621 receipt in 91 of 96 captures: all 16 of every arm except 8x8-100-off, where 5 of 16 coincide.
- **Why they repeat round 5.** Per arm, the new receipt shares the CPU netlist and configuration hashes with both earlier receipts. It shares the instrumented firmware and BIOS hashes with the #671 receipt only, and the gPTP microcode hash with the #621 receipt only. The measured interval runs the firmware, and the merge carries the #671 firmware. Dev's gPTP pin changes the microcode but not the capture's cycle counts.
- **What the receipt changes.** `date`, `base` (`44416838...`), `tree` (`6bdf8b0d...`), `harness_sha256` (`run.py` now dev's `c230cb3e...`), `remeasurement_assignment`, `processor_pins` (gPTP `7dda9c3b...`), `provenance` and each arm's `gptp_ucode_sha256`. `measured_for` (the census and clocks) and `product_firmware_sha256` are unchanged.
- **The gate.** At `9b32002c`, `python3 scripts/check_nvm_capture.py` passes with the merged firmware digest. Its five mutation arms (`bytes`, `records`, `clock`, `ignore-off-timing`, and dev's new `receipt-opt-out`) each exit 1 by their own message. At the merge commit alone it fails with "measurement harness changed; refresh measured evidence", as expected (`receipts/r7/capture_gate_at_merge.log`).

**Firmware size.** The source is byte-identical to round 5's, so round 5's product-header figures stand: pinned RV32 SDK text 17,579 B (+2,050 B over the base) and bss 104 B (+16 B). The capture's BIOS links the instrumented copy of the firmware (`nvm_capture` is in `bios.elf`). That BIOS is byte-identical to round 5's in every arm, and it was built from the merged tree's generated headers. As a cross-check, `scripts/r7/fw_size.sh` (round 5's) compiled the base and head sources against the merged tree's capture 1x1 headers, where the PHY path is compiled out. Base text is 14,473 B and bss 68 B; head text is 16,523 B and bss 84 B. That is the same +2,050 B text and +16 B bss delta (`receipts/r7/size__fw_size.txt`).

### Where the shipping path derives the authoritative sequence (at `9b32002c`)

The firmware, `hdl/milan/KL_nvm_backend.sv` and the `protocol-processor` gitlink (`2ad2f845`) are unchanged from `c7d0ad63`. Dev's only change to `hdl/milan/KL_pp_shadow.sv` is one comment word at `:333`, which keeps its line count. So round 5's and round 6's table holds line for line:

- firmware `:461`, `:730`, `:742`/`:763`, `:793`/`:804`/`:815`, `:825`/`:832`, `:1492`, `:1669-1698`, `:1601-1603`/`:1721`/`:1758`, `:927-929`, `:1395`/`:1426-1427`/`:1441-1442` and `:1954-1957`;
- `hdl/milan/KL_nvm_backend.sv:424,439,482,490,582`;
- `hdl/milan/KL_pp_shadow.sv:997` (the backend instance, re-read at this head);
- `protocol-processor/hdl/top/protocol_processor_top.sv:2899`, `hdl/aecp/KL_aecp_engine.sv:2001`, `hdl/aecp/KL_aecp_nvm_writer.sv:16` and `hdl/packet_engine/KL_pp_nvm_port.sv:14`.

No processor change is needed.

### Gate table

The final head is `9b32002cc0c3aafae9e864af7b4f08c1089a188a`. Python is CPython 3.12.3 (the scratch venv with the workflow's pinned requirements), Verilator is 5.050 for the suites and 5.052 for the capture recipe, and GNU make is 4.3. Receipts are in `receipts/r7/`, indexed by [the manifest](receipts/r7/MANIFEST.md), with local paths normalized.

Some rows ran at the merge commit `44416838`. `9b32002c` differs from it in two files only, the capture receipt and the design document. Of the commands in those rows, only `check_nvm_capture.py` reads either file, and only comments name them elsewhere (`grep` over `scripts/`, `sw/`, `tb/` and the workflows). The writer gate, the builder bank, the co-simulation and the service budget also ran again at `9b32002c`.

| Command / receipt | Head | rc | Result / planted defect |
|---|---|---|---|
| `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test --jobs 4` / `selftest_final.log` | `9b32002c` | 0 | 5 shapes at 3,550 cases. 61 planted firmware defects reddened (5 writer, 18 #671 × 3 shapes, 2 boot-walk), and the comparison check failed by name in its 9 arms. 304.70 s. |
| the same / `selftest.log` | `44416838` | 0 | The same, 403.11 s beside two capture builds. The output equals round 6's except for early-stop finding counts. |
| `scripts/r6/term_census.py` / `controls__term_census.log` | `44416838` | 0 | 3,550 distinct cases, 128 in the classes, every term at every required place, comparison check clean. Identical to round 6. |
| `scripts/r6/term_matrix.py --jobs 4` / `controls__term_matrix.log` | `44416838` | 0 | The head is clean. Each `r_omit_` control is named by all 32 of its own class's cases and by no other class, on three shapes. Identical to round 6. |
| `scripts/r6/term_views.py` / `controls__term_views.log` | `44416838` | 0 | 384 of 384 class cases hand the judgement two refusals differing in their own term alone, then VD_OK |
| `scripts/r6/plants_full.py`, 9 runs via `scripts/r7/host_controls.sh` / `controls__plants_b{1,2,3}_<shape>.log` | `44416838` | 0 each | All 18 #671 controls are named on arty_4x4, 1x1 and 8x8. Named counts, totals and finding kinds are identical to round 6's table. |
| `make -C tb/verilator/nvm_cosim run JOBS=2 POOL=4` / `vsuites__nvm_cosim.log` | `44416838` | 0 | 465/465 checks, 39/39 named mutants killed |
| the same / `vsuites_final__nvm_cosim.log` | `9b32002c` | 0 | 465/465 checks, 39/39 named mutants killed |
| `make -C tb/verilator/fw_service_budget` / `vsuites_final__fw_service_budget.log` | `9b32002c` | 0 | 55 oracle checks; dispatch census |
| `make -C tb/verilator/fw_service_budget` / `vsuites__fw_service_budget.log` | `44416838` | 0 | 55 oracle checks; dispatch census |
| `sw/builder/test_builder.py --require-elaboration --require-rv32` in six parts (`scripts/r7/builder_bank.sh`) / `builder__part1..6.log` | `44416838` | 0 all | All 103 functions (dev added two). Part 6 holds the writer gate (342.61 s). The two NOT RUN entries are round 5's: a MAKEFLAGS mutation this make cannot observe, and a calibration report not on disk. |
| the same / `builder_final__part1..6.log` | `9b32002c` | 0 all | All 103 functions. Part 6 (writer gate) 308.28 s. The same two NOT RUN entries. |
| firmware-unit replica, 7 steps (`scripts/r7/firmware_unit_replica.sh`) / `fwunit__*.log` | `44416838` | 0 all | Tally, SDK and RV32 self-tests; the controller bank with its self-test, including the lwSRP pin at dev's `08ee86e8`; `test_ctrl_nvm.py --require-rv32` (the Mark II store, which imports the host gate: 435 tests, five shapes); coverage self-test and check |
| rtl-fast lint/BDD replica, 5 steps / `rtlfast__replica.log` | `44416838` | 0 all | Scope self-test; Verilator 5.050 lint with self-test (90 at ratchet 90); source lists; BDD 404 scenarios |
| capture recipe, six arms / `capture__driver-{a,b}.log`, `capture__<arm>__measurement.json` | `44416838` | 0 each | 96 captures; 8x8 contract maximum 13.86328 ms against 24.5 ms |
| `scripts/r7/assemble_receipt.py` / `assemble.log`; `scripts/r7/refresh_section18.py` / `refresh.log` | `44416838` | 0 | The receipt passes `check_receipt` before it is written; 17 exact-once doc edits |
| `python3 scripts/check_nvm_capture.py` / `capture_gate_at_merge.log` | `44416838` | 1, as expected | "measurement harness changed": the branch's receipt does not bind dev's `run.py` |
| `scripts/r7/final_gates.py` / `final__*.log` | `9b32002c` | 0; the five capture mutation arms 1 as required | Capture gate with the merged firmware digest; `bytes`, `records`, `clock`, `ignore-off-timing` and `receipt-opt-out` arms; C and Python idiom; hygiene; docs; TOC; doc style and paths; `git diff --check` against the tree, `e8454e27` and `c6bd08c6` |
| docs-check replica, 81 positions (`scripts/r7/docs_replica.sh`, base `c6bd08c6`) / `docsrep__replica.log` | `9b32002c` | 0 all run | 78 run. Positions 35 (builder), 38 (capture gate) and 39 (writer gate) have the separate receipts above. `check_em_dash`: 0 findings over 362 added lines in 5 pages against `c6bd08c6`. `check_feature_status` and `measure_test_evidence --check` pass. |
| `scripts/r7/fw_size.sh` / `size__fw_size.txt` | `9b32002c` source, merged capture headers | 0 | base 14,473 / 68, head 16,523 / 84 (text / bss); +2,050 / +16 |

Not run by this lane:

- act against an unpublished head, and the hosted contexts for the new commits;
- dev's new `publication-census` rtl-fast job, which needs sv2v and the pinned Yosys. The merge brings it but touches none of its inputs beyond dev's own;
- physical hardware, bench or flash writes;
- the exhaustive RTL and Yosys sweeps.

`scripts/act_ci.py --selftest` is not run on the host, as AGENTS.md requires. The manager must publish the head and obtain exact-head hosted and act evidence, independent re-review and candidate validation.

**Hosted writer-gate time (estimate).** At `c7d0ad63`, the hosted standalone writer-gate step took 407 s (21:09:03 to 21:15:50). The same suite took 275.27 s locally then, so hosted ran 1.48x local. The suite is unchanged by the merge, so about 400 s is expected again, inside the builder's 1,200 s.

### Open risks (round 7)

- The merge commit `44416838` alone fails `check_nvm_capture` (harness hash). This is by design, since the receipt is not merged by hand. The next commit, `9b32002c`, passes, and both commits go out together.
- The verdict and byte-count classes are constructed CRC-32 collisions in the host model. The 2^-32 collision limit is unchanged.
- Carried from earlier rounds: the Mark II store's collapse (reported, not filed by this lane); R602-4-S1 and S2 remain optional; runtime prefill remains #717.


Public Round 7 handoff: [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6128539329).

## Round 8

Status: REVIEW READY at `d5cd863561ba1ee7bc6342fb1b00f57dd786bd97` on `671-read-fault`. That is two commits on `9b32002c`: the merge commit `f3bb2014` (parents `9b32002c` and dev `fa820988`) and the capture re-measure `d5cd8635`. No push, rebase or amend. No STOP condition arose. The merge was clean, and the re-measured capture meets its bound (13.86328 ms against 24.5 ms).

- Assignment: [#671 comment 6161596895](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6161596895). It has four items: merge `origin/dev` (`fa820988`) with a merge commit; re-run every gate this lane's files touch, plus `scripts/ci_scope.py --selftest`, `scripts/act_ci.py --selftest` and `scripts/ci_events.py --check`; re-measure only what dev's changes could affect, by the round-7 rule, and say why each remaining measurement still holds; change nothing else.
- Origin is `https://github.com/kebag-logic/milan-fpga.git`, and the original base `e8454e27` is an ancestor. `git fetch origin dev` gave `fa8209889411e8ca95757174c981f720dbcd95a2`. The merge base with `9b32002c` is `c6bd08c6`, the dev head round 7 merged.
- Both commits use the repository-local identity. No configuration or author was changed.

### Commits of this round

| Commit | Change |
|---|---|
| `f3bb2014d065141930ae1a473c966b419d1040aa` | Merge commit of dev `fa820988` into `9b32002c`. Git merged it automatically, with no conflict and no hand resolution. |
| `d5cd863561ba1ee7bc6342fb1b00f57dd786bd97` | The capture receipt, re-measured at `f3bb2014` through `run.py`, and the section 18 lines that state its figures and identities. Only those two files change. |

These checks were run at `d5cd8635`:

- The paths that differ from dev (`git diff --name-only fa820988 HEAD`) are exactly the branch's own 15 (`git diff --name-only e8454e27 c7d0ad63`).
- At `f3bb2014` all 15 are byte-identical to `9b32002c`. At `d5cd8635` the 13 outside the two re-measure files still are. The firmware (`497845e6...`, 75,087 B) is among them.
- `git diff --name-only 9b32002c f3bb2014` is exactly dev's 160 changed paths since `c6bd08c6`, and their contents are dev's.
- The one gitlink change is dev's new `third_party/tsn-c-stack` at `70936b77`. `protocol-processor` stays `2ad2f845`, `gptp-processor` `7dda9c3b` and `third_party/lwSRP` `08ee86e8`. `git -C <dir> rev-parse --show-toplevel` named each submodule's own directory before any git command in it. No submodule commit was needed.
- No `hdl/`, gitlink, register-map, record-format, Makefile or workflow change is this branch's. No A/B power-loss guarantee changed. No processor change was made.

### Changes (file:line at `d5cd8635`)

- `tb/verilator/nvm_capture_cpu/measurements.json`: the receipt, written only by `scripts/r8/assemble_receipt.py`. Against `f3bb2014` it changes `date` (`:2`), `base` (`:3`), `remeasurement_assignment` (`:1360`), `tree` (`:1366`) and `provenance` (`:1377`). Nothing else changes: every arm's summary, rows and identity hashes, `harness_sha256`, `processor_pins`, `measured_for`, `simulator` (`:16`, Verilator 5.052) and `product_firmware_sha256` are as at `f3bb2014`.
- `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md`, section 18, written only by `scripts/r8/refresh_section18.py` in 19 exact-once edits:
  - `:1626`: the measurement date;
  - `:1629-1633`: the round-8 assignment and the merge it measures. These lines say what dev brings into the capture SoC and what is unchanged. The round-7 line becomes "required the previous one", in the past tense.
  - `:1635`: the round-5 line now reads "the one before that", since a newer link precedes it.
  - `:1650-1651`: the measured commit and tree.
  - The figures in section 18 and UNRESOLVED 6 are regenerated from the receipt. Every figure repeats round 7's, so 14 of the 19 edits rewrite a figure with its own value and leave the text unchanged. "All 96 captures repeat the previous #671 receipt's system-cycle counts" (`:1671`) is now a statement about the round-7 receipt, and it holds.

### The re-measure question (item 3)

Each measurement this lane relies on, the dev input that could reach it, and the decision:

| Measurement | Could dev's change affect it? | Decision |
|---|---|---|
| Capture hold timing (`measurements.json`, section 18) | Yes. Seven dev-changed RTL files are in the capture simulation's own source list (`sources.json` of every arm): `hdl/ieee1722/maap/KL_maap.sv` (#696), `hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv`, `KL_avtp_rx_monitor_ctx.sv`, `KL_talker_diag_ctx.sv`, `hdl/ieee1722/crf/KL_crf_rx.sv`, `hdl/ieee1722/aaf/KL_aaf_packetizer.sv` (#726 frame counters) and `hdl/milan/milan_datapath.sv`. They share the SoC with the measured CPU and traffic. The receipt gate's own input census (firmware, harness, census, clocks) is unchanged, so `check_nvm_capture` alone would not have asked for this. | **Re-measured**, all six arms at `f3bb2014` (below). |
| Firmware size (`+2,050 B` text, `+16 B` bss; product figure 17,579 B text, 104 B bss) | Only through the generated headers. The firmware source is byte-identical. The SoC generator's change (#640 M8a, `sw/litex/milan_soc.py`) adds an opt-in `--ctrl-mailbox` placement that neither the product build path used here nor the capture harness enables (`tb/verilator/nvm_capture_cpu/soc.py` passes no `ctrl_mailbox`). | **Recompiled, not re-derived.** Against the merged tree's 1x1 capture headers, the delta is again +2,050 B text and +16 B bss. Every generated header of all six arms equals round 7's apart from LiteX's timestamp line and the arm's own build directory. So the product-header figure stands. |
| Boot read cost and worst case (round 2, the `fw_service_budget` simulator on the capture SoC) | Not through any measured path. The firmware, CPU netlist, BIOS, LiteSPI controller and flash model are unchanged, and the generator change is opt-in and unused. The changed datapath shares the SoC, but the six capture arms repeat every one of round 7's 96 cycle counts. Those arms run the same CPU, DRAM controller and bridges under traffic. | **Holds; not re-measured.** It remains an estimate built from measured per-read costs, as round 2 stated. |
| Section 18's area rows (`KL_nvm_backend` alone, out of context) | No. `hdl/milan/KL_nvm_backend.sv` and the shape parameters are unchanged. | **Hold.** They are not whole-datapath figures, and no such claim is made. |
| Hosted writer-gate time (estimate) | No. The suite and its inputs are the lane's own and unchanged. | **Holds.** Locally it took 271.15 s at `f3bb2014` (275 to 308 s in round 7), so about 400 s hosted is expected again, inside the builder's 1,200 s. |

### Capture re-measure

**Simulator and environment.** The receipt records `"simulator": "Verilator 5.052"`, and `tb/verilator/nvm_capture_cpu/README.md:158` says the recorded measurements use Verilator 5.052. The receipt's environment puts the product environment first on `PATH`. An interrupted first attempt in this round had put the pinned 5.050 suite simulator first on `PATH`; it ran five arms and killed the sixth mid-simulation. Recording those would have changed the `simulator` field and made the README untrue, which is more than this round may change. So all six arms were run again with round 7's unchanged driver (`scripts/r8/capture_driver.sh`, byte-identical to `scripts/r7/capture_driver.sh`, sha256 `c3e82cf2...`): system Verilator 5.052, the documented `PATH`, in a network namespace, offline, `PYTHONHASHSEED=0`, `--captures 16`. Every run log names Verilator 5.052, and the assembler refuses a log that does not name the receipt's simulator. The five 5.050 arms are supplementary only. Their 80 cycle counts also equal round 7's.

- Driver A: 8x8-50-on 08:54:17 to 09:44:25, 8x8-50-off 09:44:25 to 10:28:41, 1x1-50-on 10:28:41 to 10:37:34.
- Driver B: 8x8-100-on 08:54:22 to 09:54:02, 8x8-100-off 09:54:02 to 10:51:24, 1x1-50-off 10:51:24 to 11:00:02.

Every arm returned rc 0 with 16 graded captures. At most two builds ran at once.

| Shape | CPU MHz | Traffic | Measured min to max, ms | Floor ratio |
|---|---:|---|---:|---:|
| 1x1 | 50 | on | 3.96020 to 3.96548 | 12.3566x |
| 1x1 | 50 | off | 3.90676 to 3.92034 | 12.4989x |
| 8x8 | 50 | on | 13.84828 to 13.86328 | 3.5345x |
| 8x8 | 50 | off | 13.67538 to 13.68956 | 3.5794x |
| 8x8 | 100 | on | 10.41235 to 10.42973 | 4.6981x |
| 8x8 | 100 | off | 10.41246 to 10.41566 | 4.7045x |

- **The bound holds.** The 8x8 contract maximum is **13.86328 ms**, which leaves **10.63672 ms** to the 24.5 ms limit, a **3.5345x** ratio to the 49 ms floor. The 1x1 maximum is 3.96548 ms, and the non-contract 100 MHz 8x8 maximum is 10.42973 ms.
- **The figures repeat round 7.** All 96 captures have the system-cycle counts of the round-7 receipt (`44416838`) capture for capture, and so those of round 5 (`bd42818d`). The assembler computes and states this.
- **The products repeat round 7** (`scripts/r8/compare_products.py`, `receipts/r8/capture52-products.json`). In every arm, these equal round 7's: the CPU netlist, instrumented firmware, BIOS and gPTP microcode hashes, and every generated header apart from its timestamp line and the arm's own build directory, which `variables.mak` names. The receipt's configuration hashes are unchanged as well.
- **What the receipt changes.** `date`, `base` (`f3bb2014...`), `tree`, `remeasurement_assignment` and `provenance`. Nothing else changes. The receipt is byte-identical to the one the dry run assembled from round 7's own arm products.
- **The gate.** At `d5cd8635`, `python3 scripts/check_nvm_capture.py` passes. Each of its five mutation arms (`bytes`, `records`, `clock`, `ignore-off-timing`, `receipt-opt-out`) exits 1 by its own message.

**Firmware size.** The source is byte-identical to round 7's, so the product-header figures stand: pinned RV32 SDK text 17,579 B (+2,050 B over the base) and bss 104 B (+16 B). At `d5cd8635`, `scripts/r8/fw_size.py` recompiled both sources against the merged tree's 1x1 capture headers with make 4.3 and `MAKEFLAGS=w`. Base: text 14,473 B, data 104 B, bss 68 B. Head: text 16,523 B, data 104 B, bss 84 B. The delta is +2,050 B text, +0 B data and +16 B bss, as in round 7 (`receipts/r8/firmware-size-final.log`). The capture's BIOS links the instrumented copy, and its hash is unchanged in every arm.

### Where the shipping path derives the authoritative sequence (at `d5cd8635`)

The firmware, `hdl/milan/KL_nvm_backend.sv`, `hdl/milan/KL_pp_shadow.sv` and the `protocol-processor` gitlink (`2ad2f845`) are byte-identical to `9b32002c`. Every line below was re-read at this head:

| Location | What it does with the sequence |
|---|---|
| `sw/firmware/milan_baremetal/milan_baremetal.c:461` | `nvm_seq`, the bookkeeping generation, starts at zero, which proves nothing |
| `milan_baremetal.c:730` | `nvm_seq_of()` decodes the sequence bytes; only the guarded callers below make it authoritative |
| `milan_baremetal.c:742`, `:763` | A staged read is judged; a sequence is taken only from a `VD_OK` read, never from a refused one |
| `milan_baremetal.c:776` | Two refused reads agree only on verdict, byte count, the CRC-32 over all but the last four bytes and those four bytes |
| `milan_baremetal.c:793`, `:804`, `:815` | At most three reads judge a slot; disagreement at the bound is UNREAD with a non-authoritative zero sequence |
| `milan_baremetal.c:825`, `:832` | The re-stage accepts only a valid container carrying the already-judged sequence, within its own three-read bound |
| `milan_baremetal.c:1492` | `nvm_pick_slot()` chooses from validated verdict and sequence pairs, wrap-aware |
| `milan_baremetal.c:1669`, `:1692`, `:1695` | Boot judges A and B, re-stages the chosen slot, falls back to the other valid slot on a failed re-stage, and assigns the chosen validated sequence or the bookkeeping zero |
| `milan_baremetal.c:1601`, `:1721`, `:1758` | Any unread authority holds the writer, at writer re-attach and at cold admission |
| `milan_baremetal.c:927` | `nvm_publish()` writes the bookkeeping sequence and the validity and hold status; it derives no generation |
| `milan_baremetal.c:1395`, `:1426`, `:1427`, `:1441` | A live commit derives `next = nvm_seq + 1`, verifies the written slot and its sequence, then promotes it |
| `milan_baremetal.c:1954` | The status command decodes sequences only for valid slots and changes nothing |
| `hdl/milan/KL_nvm_backend.sv:424`, `:439`, `:482`, `:490`, `:582` | The sequence CSR is storage: declared, reset, written by firmware and read back; it derives no generation |
| `hdl/milan/KL_pp_shadow.sv:997`, `:1079` | The parent instantiates this backend and the processor |
| `protocol-processor/hdl/top/protocol_processor_top.sv:2899`, `hdl/aecp/KL_aecp_engine.sv:2001`, `hdl/aecp/KL_aecp_nvm_writer.sv:16`, `hdl/packet_engine/KL_pp_nvm_port.sv:14` | The processor's port and writer, as the parent instantiates them, operate on records and carry no generation |

No processor change is needed.

### Gate table

The final head is `d5cd863561ba1ee7bc6342fb1b00f57dd786bd97`. Python is CPython 3.12.3 (the scratch environment with the workflow's pinned requirements); the suites use the pinned Verilator 5.050 and the capture recipe Verilator 5.052; GNU make is 4.3. Receipts are in `receipts/r8/`: [GATES.json](receipts/r8/GATES.json) has every command, return code, head and log identity, including failed and interrupted attempts, and [GATE-TABLE-R8.md](receipts/r8/GATE-TABLE-R8.md) has the commands. Local paths are normalized.

`d5cd8635` differs from `f3bb2014` in the receipt and the design document only. Only `scripts/check_nvm_capture.py` reads the receipt; the design document is read only by the documentation gates. Elsewhere, comments name the two files, but no code reads them. So the code and fixture rows ran at `f3bb2014`, and every consumer of either file ran again at `d5cd8635`, with the three requested CI checks.

| Gate | Head | rc | Seconds | What it catches |
|---|---|---|---:|---|
| Capture recipe, six arms, Verilator 5.052 | `f3bb2014` | 0 | 13,737.00 | 96 captures. Each checks attestation, closed ownership, every destination byte and the traffic arm's counters; the contract arms are graded against 24.5 ms. |
| Capture products against round 7 | `f3bb2014` | 0 | 0.11 | Any difference in an arm's CPU netlist, instrumented firmware, BIOS, gPTP microcode or generated headers (timestamp line and build directory aside). |
| Receipt assembly, section 18 refresh | `f3bb2014` | 0 | 0.88 | The assembler refuses a dirty tree, a HEAD other than the measured commit, a run log naming another simulator, or a receipt that fails `check_receipt`. The refresher refuses a changed census, firmware digest or processor pin, and any edit that does not match exactly once. |
| Shipping writer gate | `f3bb2014` | 0 | 271.15 | 5 shapes at 3,550 cases. 61 planted firmware defects (5 writer, 18 #671 on 3 shapes, 2 boot-walk) redden, and the comparison check fails by name in its 9 arms. |
| Term census | `f3bb2014` | 0 | 0.21 | A missing class, sequence, layout or restart combination, a duplicate case, or a comparison term without a class or control. |
| Term omission matrix | `f3bb2014` | 0 | 31.14 | Each `r_omit_` control must fail all 32 of its own class's cases per shape, and no other class. |
| Instrumented term views | `f3bb2014` | 0 | 10.75 | A class case that does not hand the judgement two refusals differing in its own term alone, then `VD_OK`. |
| Full read-fault campaigns | `f3bb2014` | 0 | 1,900.43 | Each of the 18 #671 controls is run over the full standing cases on 3 shapes and must be named by its own finding. |
| Campaign comparison with round 7 | `f3bb2014` | 0 | 0.06 | Any change in the named, restart, cold or total finding counts of the 54 shape and control pairs. |
| NVM co-simulation | `f3bb2014` | 0 | 968.31 | 465 checks; 39 named mutants (stale identity, lost pending work, reload and admission ordering, unbounded hold, writer restart) killed by their named checks. |
| Service budget | `f3bb2014` | 0 | 1.67 | 55 oracle checks; product dispatch removal, duty overrun and lost backing markers. |
| Builder, 103 functions | `f3bb2014` | 0 | 1,370.23 | Product profile, RV32, shape, dispatch, descriptor, clock and capacity plants; the writer gate in part 6. Every elaboration arm ran; two arms are NOT RUN for recorded reasons and not counted. |
| Firmware tally | `f3bb2014` | 0 | 3.63 | 18 planted false-success and empty-run tally cases. |
| SDK and RV32 self-tests | `f3bb2014` | 0 | 9.71 | Wrong SDK identity, ISA or ABI, disallowed symbols, images that do not link freestanding. |
| Control firmware, four phases | `f3bb2014` | 0 | 2,748.91 | Normal suites and the ADP, ACMP, MAAP, AECP and SRP mutation phases with RV32 builds, including the lwSRP pin controls. |
| Control shard proof, CI firmware census | `f3bb2014` | 0 | 0.49 | A dropped, duplicated or unassigned suite; invalid shard options; a CI census losing a phase. |
| Saved-state store | `f3bb2014` | 0 | 3,615.41 | 5 shapes, 435 tests and 109 planted store defects, which import this lane's host gate. |
| Coverage | `f3bb2014` | 0 | 279.50 | 29 planted ratchet and exclusion cases; the live coverage check over 30 files. |
| Firmware boundary | `f3bb2014` | 0 | 874.96 | Public-header boundary, source ownership and pins over 2,854 compiled sources; missing builders or compiler inputs refused. The control-memory image builds. |
| RTL lint and source lists | `f3bb2014` | 0 | 17.84 | Lint ratchet (90 at 90) and waiver plants; forged or missing submodule inputs; source-list drift. |
| BDD | `f3bb2014` | 0 | 1.72 | 406 scenarios, 1,977 steps. |
| Docs-check replica at the merge | `f3bb2014` | 0 | 753.75 | 81 positions, base `fa820988`. The builder, capture-gate and writer-gate positions have the separate rows above. |
| CI checks at the merge | `f3bb2014` | 0 | 125.45 | `ci_scope.py --selftest` (scope history and merge-base plants), `ci_events.py --check` (2,174 contract items), and `act_ci.py --selftest` in a disposable container, checked-in and flat layouts. |
| Final capture and document gates | `d5cd8635` | 0 | 9.74 | `check_nvm_capture` passes, and its `bytes`, `records`, `clock`, `ignore-off-timing` and `receipt-opt-out` arms each exit 1 by name. C and Python idiom, hygiene, docs, TOC and anchors, doc style, paths and map, em dash against `fa820988`, feature status, `git diff --check` against the tree, `e8454e27` and `fa820988`. |
| Docs-check replica at the final head | `d5cd8635` | 0 | 655.92 | The same 81 positions, at the head that changes the design document. |
| CI checks at the final head | `d5cd8635` | 0 | 117.61 | The three requested checks again, the firmware census, and both runner self-test layouts in a disposable container. |
| Firmware size | `d5cd8635` | 0 | 0.72 | Base and head sources against the merged tree's 1x1 capture headers, make 4.3 with `MAKEFLAGS=w`. A measurement, not a mutation test. |

Seconds is the sum of each row's records. The capture arms ran two at a time, so their wall time was 08:54 to 11:00.

Not run by this lane:

- act against an unpublished head, and the hosted contexts for the new commits;
- the exhaustive RTL and Yosys sweeps and rtl-fast's `publication-census` job (sv2v and the pinned Yosys);
- physical hardware, bench or flash writes.

`scripts/act_ci.py --selftest` ran only inside a disposable container (read-only checkout, no network, no capabilities, no credentials), in both the checked-in layout and a flat copy, never as a host-side orchestrator. The manager must publish the head and obtain exact-head hosted and act evidence, independent re-review and candidate validation.

### Execution notes

None of these changed a repository file or weakened a check, and no failed or interrupted attempt is counted as evidence. All are listed in `GATES.json`.

- The previous session ended on an engine capacity error after committing the merge `f3bb2014`. This session resumed from this file and the scratch records, and posted no second TAKEN.
- Its first wrapper had a 570 s limit, which expired for builder part 1, co-simulation and the saved-state store gate (rc 124). Their complete reruns pass: `builder-1-retry`, `nvm-cosim-retry` and `ctrl-nvm-retry`.
- Control phases 1 to 3 were stopped (rc -15) to relieve memory pressure. They were re-run at `--jobs 2` and pass.
- One capture launch found the SDK's `meson` ahead of the product environment on `PATH` and stopped at setup (rc 1).
- The first container self-test had no writable temporary directory (rc 1). With the container user and scratch mount corrected, both layouts pass.
- One term-census call lacked its repository argument (rc 1). It was corrected.
- The firmware boundary gate first refused because pinned Migen was missing from the scratch Python environment (rc 2). The Migen and LiteX revisions of `sw/litex/litex_pins.txt` were installed there, and the full gate was re-run.
- The 5.050 capture attempt (five arms rc 0, one killed) is superseded, as described above. Its records carry that note.
- The first product comparison returned rc 1 on `variables.mak`, which names each arm's own build directory. The comparison now writes that directory as `$BUILD` and passes.
- The gates left 19 ignored generated paths in the checkout: Python caches, builder and co-simulation outputs, and `configs/generated/*.hex`. These were moved to scratch (`tree-outputs/MOVED.txt`). The checkout, its submodules included, has no tracked change and no ignored file.
- The earlier session noted the service unit's `memory.high` as `max`. The only unit now running this lane reads `max`, so nothing remained to restore. No Vivado run was made.
- The two capture drivers and the final docs-check replica ran detached and were polled from foreground commands; every other command ran in the foreground.

### Open risks (round 8)

- The previous verdicts are at `9b32002c`; the new head needs the assigned reviews and exact-head CI.
- Two builder arms stay NOT RUN for recorded reasons, as in round 7: the `MAKEFLAGS += -e` plant, which make 4.3 cannot observe, and the hardware calibration report, which is not on disk.
- The boot read cost remains an estimate from measured per-read costs; it was not re-measured (see the table above).
- Carried from earlier rounds: identical wrong flash bytes stay indistinguishable from a deterministic refusal (the media-fault rule); the verdict and byte-count classes are constructed CRC-32 collisions in the host model; the Mark II store's collapse is reported, not filed by this lane; R602-4-S1 and S2 remain optional; runtime prefill remains #717.


Public Round 8 handoff: [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6165001131).
