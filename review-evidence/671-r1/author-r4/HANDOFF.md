[A592]

# HANDOFF: lane for #671 (a boot read fault must leave saved-state authority unknown)

Status: Round 4 is ready for independent re-review at `7bc7ceca6ba1dd1a268d6fa1704613bb141487fe`. All applicable local commands passed, and all six capture arms completed. The Round 4 section below is current; earlier sections preserve historical evidence at their named heads. The seven Round 4 commits are local and have not been pushed. Hosted/act evidence and independent re-review remain publication duties.

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
