# HANDOFF: [A592] lane for #671 (a boot read fault must leave saved-state authority unknown)

Status: REVIEW READY at `f54dbe3e` (see the gate table). Relates to #671.

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
| Co-simulation of the shipping writer and backend | `make -C tb/verilator/nvm_cosim run` (JOBS=2) | f54dbe3e | 0 | "nvm_cosim: 465 checks: 465 PASS, 0 FAIL", "39 of 39 mutant(s) killed by their named check" |
| Service-budget suite self-test | `make -C tb/verilator/fw_service_budget` | f54dbe3e | 0 | flash 14/0, oracle 55/0, dispatch census PASS |
| Capture census and receipt | `python3 scripts/check_nvm_capture.py`; `--mutation bytes`, `records`, `clock`, `ignore-off-timing` | f54dbe3e | 0; 1 ×4 | "PASS: capture census, clocks, both timing arms and receipt agree"; every mutation refused |
| Capture re-measure, six arms | `tb/verilator/nvm_capture_cpu/run.py` (product venv, Verilator 5.052) | 7b714334 | graded | the table above |
| NVM record-space gate | `python3 scripts/check_nvm_record_space.py` and `--self-test` | f54dbe3e | 0, 0 | 0 findings across 5 configs |
| docs.yml replica (docs-check, wire-accountability, docs-check-no-git) | `docs_check_replica.sh` (scratch) | f54dbe3e | 0 | 81/81 steps rc 0, 40 min; em-dash base `e8454e27` = merge-base with live dev `f88df731` |
| rtl-fast firmware-unit replica | `firmware_unit_replica.sh` (scratch): tally self-test, SDK self-test, RV32 self-test, `test_ctrl_firmware.py --require-rv32 --self-test`, `test_ctrl_nvm.py --require-rv32`, coverage self-test and check | 7b714334 | 0 | 7/7. The A/B power-loss suite: "saved-state store gate (#665 F1): OK across 5 shape(s), 435 tests", power cut included. Coverage PASS |
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
