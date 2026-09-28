# Round 3 handoff

Status: REVIEW READY at `93262f2512054166ae753eda24d76c99f2ea6714`. All native evidence is retained, and every required gate returns rc 0 at this committed head (see Gate table).
Role: author [A411]. Independent reviewers: [R368] (internal) and [R369] (external).
Scope: #590, #592 and #599; PR #609. Assignment: #590 comment 5865679172.
Starting head: `c64f8cd896a4462bd42c4b90b32861ac7fd35176`; remote `https://github.com/kebag-logic/milan-fpga.git`; branch `590-592-599-firmware`, clean at start.
Public TAKEN: https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5865703318.

## Commits (local, not pushed)

| Commit | Subject | Content |
| --- | --- | --- |
| `26a26e1f39feeebaebb0f450d7cbe2b63429c252` | Guard disabled firmware writers and require BIOS dispatch support | N1, S5, S6, S7, S8 code and tests; docs F5, S9 |
| `69d8337352d79ffd4a7c0895dc14f0ae0d58811e` | Refresh round-three capture and service evidence | capture receipt, snapshot-ownership §18/§20.6 (N2/F4), findings-page tables |
| `93262f2512054166ae753eda24d76c99f2ea6714` | Supply BIOS dispatch marker in fabric host fixture | builder gate-35 fixture forced by the S5 link marker |

Firmware and every native build input are unchanged after `26a26e1f`: `git diff 26a26e1f..93262f25` touches only the two documentation pages, the capture receipt and the builder fixture. The firmware SHA-256 at the final head is `89c0360e…`, the digest the receipt binds. The receipt's tree `1ced48e2…` equals `26a26e1f^{tree}`.

## Per-item ledger

### 1. R368-2 N1: no heartbeat from a rejected writer

Change:
- `sw/firmware/milan_baremetal/milan_baremetal.c:418-419` adds `nvm_started`: identity and shape must admit the writer before any service access.
- `:926-928`: `nvm_heartbeat_tick()` returns before reading time, polling the PHY or writing `PP_NVM_STAT` unless the writer was admitted. Every caller goes through it: the dispatch hook (`:943-946`), the Milan command handlers, the CRC and validation walk yields, and the idle service.
- `:1449`: `nvm_boot()` sets `nvm_started` only after `nvm_shape_consistent()` succeeds. The shape-mismatch return at `:1445-1447` leaves it clear.
- `milan_init()` returns at `:1636-1638` on a CSR identity mismatch, before `nvm_boot()`, so `nvm_started` stays clear.
- The retired-writer rule (`:929-932`) and the tag-mismatch path are unchanged.

Test:
- `sw/firmware/nvm_hosttest/test_disabled_writer.py:9-35` plants each rejected startup (the shape check returns 0; the identity check always fails). It drives each of nine console lines twice per run: empty, `unknown_command`, `milan_status`, `milan_nvm`, `milan_nvm commit`, `milan_nvm wipe`, `milan_gettime`, `milan_settime 1 0` and `milan_utc 1 0 37`. Each run is graded immediately and after 2500 ms of idle time.
- It requires the rejection message and `hb=0 backed=0 stale=0` in every case: 18 cases per state per shape, on all five shapes including Arty.
- `test_disabled_writer.py:38-48` is the negative control. Removing the admission guard must produce findings in both states. It is wired into `test_nvm_firmware.py:620-636` (grade on every shape, self-test on the first).
- `nvm_host.c:61-63,652-657` routes `milan_gettime`, `milan_settime` and `milan_utc` so that every Milan command reaches the firmware handler.

Reviewer evidence:
- R368-2's unchanged `disabled_writer_probe.py` (`logs/final-probe-disabled-writer-probe.log`) gives `hb=0 backed=0 stale=0` for the head in both planted states. The healthy arms keep `hb=1 backed=1`.
- Disclosed consequence: a rejected startup also performs no PHY poll or link-status publication. The identity path must not touch a foreign fabric. On the shape path the idle hook was never installed (`:1553`), so continuous PHY service was already absent in that state.

### 2. R368-2 N2 = R369-2 F4: design authority states the committed receipt

`docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md`:

- §18, `:1591-1630`, gives:
  - measured commit `26a26e1f`, tree `1ced48e2`, firmware `89c0360e…` and pin `16be6768`;
  - the six-row table (minimum to maximum and floor ratio), taken from `tb/verilator/nvm_capture_cpu/measurements.json`;
  - the worst 8x8 figure: 13.23352 ms, 3.7027x floor ratio, 11.26648 ms margin to 24.5 ms;
  - the historical pre-word-copy maximum of 24.30246 ms, labelled historical;
  - 11.06894 ms of margin gained.
- The traffic paragraph (`:1653-1654`) no longer asserts the superseded 100 MHz inversion.
- §20 item 6, `:1771-1785`, states the same maximum, ratio, margin and gain, with the 1x1 and 100 MHz maxima.
- `rg '24\.30246|0\.19754|6\.60642|19\.79024' docs/design` returns only `:1614`, the line labelled historical.
- The PR body's margin sentence now matches the receipt (see PR-BODY.md).
- R368-2 T3: the receipt's `bios_dispatch_patch_sha256` is stated as informational provenance (`:1599`).

### 3. R369-2 F5: long built-in lapse threshold

- `docs/integration/BAREMETAL_FIRMWARE.md:1912-1914` and `docs/findings/397_SERVICE_BUDGET.md:202-204` now read: "A built-in body can lapse backing after about 1,750 ms. The 2,000 ms deadline includes up to 250 ms beforehand. That phase can suppress the dispatch heartbeat write."
- This matches `nvm_heartbeat_tick()` (`milan_baremetal.c:933-937`, 250 ms rate limit) and T-NVM-WRITER-ALIVE (2,000 ms).

### 4. R369-2 F6: native evidence retained and regraded

- All F6 arms ran at the implementation head `26a26e1f`, whose firmware and harness inputs equal the final head.
- Raw logs, JSON receipts, specs and build logs are under `native-evidence/`. `native-artifacts.json` binds 135 artifacts by raw and stored SHA-256 and size. Files over 200 KB are gzip-compressed.
- `native-commands.json` records the 62 commands, their head, duration and rc.
- `run.py --regrade` passes at the final head on every kept service log (`final-target-gates.json`, 15 entries, rc 0; logs under `logs/final-regrade-*`).

| F6 arm | Result | Retained |
| --- | --- | --- |
| `queued-builtins` 1x1 | 1051/1051 lines, each with at least one tick; 269.21480 ms maximum gap; `unbacked_cycles=0`; 0 findings | `service-1x1-queued-builtins{.log,-raw.log,-receipt.json}.gz`, `-spec.json` |
| `queued-builtins` 8x8 | 1051/1051 lines, each with at least one tick; 258.41092 ms maximum gap; `unbacked_cycles=0`; 0 findings | `service-8x8-queued-builtins*` |
| `remove-dispatch` on `queued-builtins` | 1051 named per-line findings plus continuous backing lost; 8238.99253 ms gap; `unbacked_cycles=623935512`; prints `PASS: dispatch removal caught by continuous backing and per-line checks` | `service-remove-dispatch-queued-builtins*` |
| `remove-dispatch` on `queued-short` | 350 named per-line findings; 2770.22295 ms gap; same PASS line | `service-remove-dispatch-queued-short*` |
| target `late-sample` | the named finding `PHY initial gigabit negotiation was not published`; `PASS: late MDIO sampling caught by target negotiation check` | `service-late-sample-all*` |
| byte-only capture | 24.30310–24.30446 ms; minimum slowdown 1.83648x against the 1.5x bound; baseline SHA-256 bound | `capture-byte-only*` |

### 5. Suggestions taken

- **S5 (link guard).** Patch 0006 (`sw/litex/patches/0006-bios-dispatch-hook.patch:9-16`) defines a strong `bios_dispatch_hook_required()`.
  - `milan_baremetal.c:356,1443-1444` calls it during NVM startup, so firmware linked against a BIOS without 0006 fails with an undefined reference.
  - The dependency is noted where the hook is introduced: `BAREMETAL_FIRMWARE.md:1897-1898`, `397_SERVICE_BUDGET.md:192-193` and `sw/litex/patches/README.md:18`.
  - Host test: `test_disabled_writer.py:51-61` strips the marker from the host BIOS stand-in, and the product object must fail to link by name.
  - Product-recipe control: `product_link_guard.py` replays the actual RV32 BIOS link command (`-Wl,--whole-archive`). The marker present links; the marker stripped from a scratch `main.o` fails with ``undefined reference to `bios_dispatch_hook_required'`` (`product-link-guard.json`, `logs/product-link-*.log`).
  - The installed LiteX `bios/main.c` at `a1e1c365` carries the updated patch (`:177-187,361`).
- **S6.** `sw/litex/patches/apply.sh:10` lists 0006 in the header. `sw/builder/test_builder.py:23296` says "four patches" (the SERIES count). `:23381` says "historical six". The README blank line before the 0006 bullet is removed (R368-2 T2).
- **S7.** `tb/verilator/fw_service_budget/run.py:553-555`: the `remove-dispatch` verdict requires a `console line lacks a dispatch opportunity:` finding in addition to continuous backing loss. `:353` applies the per-line oracle to both queued plans.
  - `:470-489` `dispatch_controls()` adds four portable checks: a serviced line is accepted; a zero-tick line is refused with the named finding while backing stays healthy; a verdict with backing loss but no per-line finding is refused; the complete verdict is accepted.
  - The portable self-test count rises from 43 to 47.
- **S8.** `sw/firmware/nvm_hosttest/phy_host.c:22,60,154-161`: the peer NAKs register 5 after BMSR and BMCR reads succeed. The firmware must publish 0 (a 0xffff read would falsely resolve 100/full), then 11 when the NAK clears.
  - `test_phy_firmware.py:24,32-36` adds the `ack-ignored` mutant, which this NAK kills.
- **S9.** `397_SERVICE_BUDGET.md:276` links the phase probe at `a1c4d79f`. `:173-175` explains N/A: no separate protocol deadline, including bounded memory reads, empty and unknown lines. The empty and unknown rows now show N/A consistently (R368-2 T4).
- **R368-2 T1 (prototype).** `milan_baremetal.c:356-357` declares both external hook symbols.

Not taken, as in round 2: R369-1 S1 (PHY discovery rate and error hold), S3 (builder literal 4), S4 (CHANGELOG), S10 (reviewer note, no change).

## MDIO phase proof

- Pinned reader, LiteX `a1e1c365` `litex/soc/software/libliteeth/mdio.c`:
  - `mdio_read` (`:80-95`) writes 32 preamble bits and the 14 start/opcode/address bits, then calls `raw_turnaround()` (`:55-65`, two clocks, nothing sampled).
  - `raw_read()` (`:37-53`) samples `MDIO_DI` with MDC low before each of the 16 rising edges.
- Firmware, `milan_baremetal.c:795-827`:
  - `phy_mdio_bit` drives the pins with MDC low, waits `cdelay(32)`, samples, then raises MDC. The sample for input clock k is therefore taken before rising edge k.
  - `phy_mdio_read` clocks bits 0-45 (preamble plus command) and discards clock 46 (released turnaround). It checks clock 47 as the zero acknowledgement and samples D15..D0 at clocks 48..63.
  - This is the same phase as the pinned reader, plus an acknowledgement check.
- IEEE 802.3 §22.3.4: the PHY launches each bit after a rising edge, so bit k+1 is valid before edge k+1. Both committed peers model this: `phy_host.c:55-60` and `tb/verilator/fw_service_budget/phy.hpp`.
- Evidence (re-run at the final head with byte-identical output):
  - R369's unchanged `probe_mdio_phase.py` (`logs/final-probe-phase-probe.log`) prints `PHASE=1 BMSR true=0x796d litex_reader=0x796d firmware_reader=0x796d`, `PHYID1 … 0x001c` and `published link_status=13`.
  - The host `late-sample` and `ack-ignored` mutants are killed (`test_phy_firmware.py`).
  - The target `late-sample` control fails its named negotiation check (F6 table).

## Dispatch hook design and service plan

- Design:
  - 0006 calls `command_dispatch_hook()` right after `readline()` in the only BIOS console loop (installed `main.c:360-361`), before the empty-line test and any parsing.
  - The BIOS links product libraries `--whole-archive`, so the firmware's strong definition (`milan_baremetal.c:943-946`) replaces the weak default.
  - The override calls only `nvm_heartbeat_tick()`, which is rate-limited at 250 ms, includes the PHY opportunity, and starts no idle commit.
  - Admission (item 1) gates it.
  - The required link marker (S5) makes a BIOS without 0006 a link failure instead of a silent regression.
- Service plan result: both shapes pass all six positive plans with zero unbacked cycles and zero service findings (#397 table below). Both queued plans show a dispatch tick for every line. Removing the hook fails with the named per-line finding.
- Residual (documented, unchanged decision): a single long built-in body has no internal service opportunity. It can exceed the 500 ms heartbeat and 250 ms PHY publication bounds, and it lapses backing after about 1,750 ms of body time.

## Edge guard

- The committed partial-ownership grade (`test_nvm_firmware.py`, `nvm_host.c --open-record`) is unchanged this round.
- R368-2's unchanged `host_mutant2.py edge-cross` (`next - i >= 1u`) fails on all five shapes, with both named findings per shape: "open record changed across unaligned predecessor edge" and "did not commit byte-identically". Raw rc 1, graded rc 0 (`edge-control.json`, `logs/edge-cross-all-shapes.log`).
- The ordinary host self-test passes.

## Capture table (re-measured; firmware digest bound)

All six arms, 16 captures each, 96 total, zero byte mismatches and zero open-record copies. Receipt: `tb/verilator/nvm_capture_cpu/measurements.json` (firmware `89c0360e…`, tree `1ced48e2…`, pin `16be6768`).

| Shape | CPU MHz | Traffic | Minimum to maximum ms | 49 ms floor ratio |
| --- | --- | --- | --- | --- |
| 1x1 | 50 | on | 3.87674 to 3.88779 | 12.6036x |
| 1x1 | 50 | off | 3.82856 to 3.84214 | 12.7533x |
| 8x8 | 50 | on | 13.21274 to 13.23352 | 3.7027x |
| 8x8 | 50 | off | 13.04976 to 13.06923 | 3.7493x |
| 8x8 | 100 (non-contract) | on | 9.94138 to 9.95464 | 4.9223x |
| 8x8 | 100 (non-contract) | off | 9.93764 to 9.94094 | 4.9291x |

The contract 8x8 maximum is 13.23352 ms, with 11.26648 ms margin to 24.5 ms, and gains 11.06894 ms over the historical 24.30246 ms byte-copy maximum. STOP (8x8 above 24.5 ms) did not occur. `verify_packet.py` replays all 96 rows from the retained raw logs against the committed receipt.

## #397 service harness table

Both shapes, native, `--enforce-service`. Every row has `unbacked_cycles=0`, zero service findings, and a regrade that passes at the final head.

| Shape | Plan | Largest heartbeat gap ms | Margin to 500 ms |
| --- | --- | --- | --- |
| 1x1 | all | 264.64718 | 235.35282 |
| 1x1 | uart-paced | 252.70784 | 247.29216 |
| 1x1 | queued-input | 269.07972 | 230.92028 |
| 1x1 | queued-short | 257.66458 | 242.33542 |
| 1x1 | queued-builtins | 269.21480 | 230.78520 |
| 1x1 | device-wait | 250.61836 | 249.38164 |
| 8x8 | all | 322.47884 | 177.52116 |
| 8x8 | uart-paced | 295.45834 | 204.54166 |
| 8x8 | queued-input | 322.47884 | 177.52116 |
| 8x8 | queued-short | 257.66520 | 242.33480 |
| 8x8 | queued-builtins | 258.41092 | 241.58908 |
| 8x8 | device-wait | 275.48170 | 224.51830 |

PHY: the largest MDIO transaction is 0.12451 ms (1x1) and 0.12457 ms (8x8). The largest complete poll is 0.64413 and 0.83375 ms, and the conservative charge 1.76472 and 1.95488 ms. The worst duty plus UART plus charge is 81.17743 and 120.53971 ms, leaving 43.82257 and 4.46029 ms of reserve inside the 125 ms trigger and the 250 ms publication bound. STOP (MDIO transaction plus bookkeeping over any budget term) did not occur.

## Mutant and control table

| Control | Where | Expected | Result |
| --- | --- | --- | --- |
| Admission guard removed | `test_disabled_writer.py:38-48` (committed) | findings in both rejected states | caught in both |
| Head, rejected startup, all Milan commands and empty lines | `test_disabled_writer.py` on 5 shapes | `hb=0 backed=0 stale=0` | 18 cases per state per shape pass |
| R368-2 disabled-writer probe (unchanged) | `logs/final-probe-disabled-writer-probe.log` | head `hb=0` in both states; healthy `hb=1` | as expected |
| BIOS marker removed (host) | `test_disabled_writer.py:51-61` | named link failure | refused |
| BIOS marker removed (product RV32 recipe) | `product-link-guard.json`, `logs/final-probe-product-link-guard.log` | named link failure; present links | as expected |
| R369-2 weak-link probe (unchanged) | `logs/weak-link-probe.log` | whole-archive owner 1, plain archive 0 | as expected |
| `ack-ignored` | `test_phy_firmware.py` + register-5 NAK | killed | killed |
| `late-sample`, `no-publish`, `defer-recovery` (host) | `test_phy_firmware.py` | killed | killed |
| Phase probe (unchanged R369) | `logs/final-probe-phase-probe.log` | `PHASE=1` true values, `link_status=13` | as expected |
| Target `late-sample` | native, 1x1 all | named negotiation finding | PASS line |
| Target `no-publish` | native, 1x1 all | missing publication | `PASS: missing publication caught by target simulation` |
| Target `remove-dispatch`, queued-builtins and queued-short | native | backing lost plus named per-line findings | PASS line; 1051 and 350 findings |
| Portable dispatch controls | `run.py:470-489` | 4 checks | pass within 47 grading checks |
| R369-2 builtin oracle probe (unchanged) | `logs/final-probe-dispatch-oracle-probe.log` | zero-tick row refused on both queued plans | as expected; its last line is a text-presence check, and the committed verdict also requires the per-line finding (`run.py:553-554`) |
| R368-2 `edge-cross` (unchanged) | `logs/final-probe-edge-cross.log`, `edge-control.json` | fails on 5 shapes | both named findings on all 5 |
| Byte-only capture | native, 8x8 50 MHz on | above 1.5x matched maximum | 1.83648x |
| Missing copy | native, 1x1 | destination-byte oracle | caught (3218 mismatches) |
| Missing traffic | native, 1x1 | traffic oracle | caught |

## Gate table

All at the committed head `93262f2512054166ae753eda24d76c99f2ea6714` and the physical `/data` path, never piped. Worktree clean before and after. Receipts: `final-builder-gates.json`, `final-gates.json`, `final-target-gates.json` and `final-probes.json`. `verify_final_gates.py` → `final-audit.json`: 42 records, every retained log re-hashed, no file over 200 KB, rc 0.

| Gate | Command | rc | Seconds | Notes |
| --- | --- | --- | --- | --- |
| Full builder bank, compiler present, with firmware census | `sw/builder/test_builder.py --require-elaboration --require-rv32` | 0 | 966 | `ALL GATES PASS EXCEPT 1 NOT RUN`: gate 11 calibration, report absent (as in earlier rounds). Gate 1b ordered census and gate 35 host link pass. |
| Full builder bank, compilers absent | `full-builder-absent.py` (all three candidates hidden) | 0 | 679 | `EXCEPT 2 NOT RUN`: the intentional gate-1b compiled census omission and gate 11 |
| Host firmware self-test | `sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | 57 | 5 shapes OK, Arty included. 5 planted writer defects caught. Disabled-writer: 10 state/shape lines pass, guard mutant caught in both states. Link guard refused on 5 shapes. PHY mutants `no-publish`, `defer-recovery`, `late-sample` and `ack-ignored` caught. |
| Capture receipt | `scripts/check_nvm_capture.py` | 0 | 0.7 | census, clocks, both arms, receipt and planted controls |
| Kept native capture oracles | `verify_packet.py` | 0 | 0.2 | 135 artifacts re-hashed; 96 captures regraded; byte-only control |
| #397 harness, portable | `tb/verilator/fw_service_budget/run.py --self-test` | 0 | 0.6 | 47 grading and 14 flash checks |
| #397 harness, kept logs | `run.py … --regrade` × 15 | 0 | 0.2-0.7 each | 12 positive plans and 3 target controls (`final-target-gates.json`) |
| CI scope | `scripts/ci_scope.py --selftest` | 0 | 2.5 | |
| Docs gates | `docs_check`, `check_doc_paths`, `check_doc_style`, `check_archive`, `gen_toc --check`, `check_em_dash --base 20aa4eabf` | 0 | ≤ 4.5 each | |
| Source checks | `check_feature_status --self-test`, `pp_srcs --check`, `check_baremetal_only --check`, `check_entity_shape --self-test`, `check_py_idiom`, `check_cpp_idiom`, `check_hygiene --check`, `measure_test_evidence --check` | 0 | ≤ 41 each | |
| Whitespace | `git diff --check 20aa4eabf` | 0 | 0.05 | |
| Reviewer probes, unchanged | phase, disabled writer, builtin oracle, `edge-cross` (expected raw rc 1), product link guard | 0 (graded) | ≤ 31 each | `final-probes.json`; logs `logs/final-probe-*.log` |

The phase, disabled-writer and edge-cross probe logs at the final head are byte-identical to the implementation-head runs (same SHA-256).

## Evidence retention

- Raw F6 logs and receipts are under `native-evidence/`. Files larger than 200 KB are gzip-compressed and bound by raw and stored SHA-256 and size (`native-artifacts.json`).
- Build trees, tool prefixes, virtual environments and native executables stay outside this packet, under `$VALIDATION_STORAGE/590-a411/`.
- `ENVIRONMENT-NOTE.md` records the first wrapper attempt, which failed before simulation.
- `builder-fixture-failure-gates.json` retains the rc-1 builder logs at `69d83373` that exposed the gate-35 fixture gap.
- Long native runs and the full builder bank exceed the 10-minute single-command limit of this session. They ran as supervised jobs, one at a time, awaited by foreground polling. At the final head, two builder attempts overlapped by mistake. Both were stopped and discarded before any result was recorded, and the bank was rerun alone.

## Delivery

- No push, PR edit, merge, hardware, RTL, processor or configuration change.
- Builder edits (`sw/builder/test_builder.py`):
  - two S6 comment corrections (`:23296,23381`);
  - the gate-35 host fixture's declaration and empty definition of the BIOS marker (`:26644,26665`), forced by the S5 link dependency.
  - No assertion or grading rule changed; the lane's earlier authorized fixture (2 to 4) is unchanged.
- Public REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5869359958 (text in `REVIEW-READY.md`).
- Commits are local only; publishing the branch and the evidence packet is the manager's step.
