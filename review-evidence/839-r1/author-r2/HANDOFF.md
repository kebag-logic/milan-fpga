# A731b HANDOFF: issue #839 round 2 (PR #841)

PRIVATE. Nothing pushed (the manager pushes). Receipts under `receipts/`, indexed in `receipts/INDEX.md` (generated from the files present).

## Status

DONE at `ba56827b`: every assigned gate rc 0 on clean clones of the head, REVIEW READY posted 2026-11-05 23:47 CET. Nothing pushed; the manager pushes `ba56827b` to `839-boot-source-address` (four commits on the pushed `992c3d7b`) and replaces the PR #841 body with `PR-BODY.md`.

| Item | State |
|---|---|
| Base | `604899c08ff1cd1830e1dd08b733109ef852400c` (dev; the live `dev` tip at 17:37 and again at 20:28 on 2026-11-05: unchanged; the merge base) |
| Round-1 head | `992c3d7bb37f4ade0b151c17d718baed0e119753` (pushed, PR #841) |
| Round-2 head | `ba56827bbfe4acadb84ca220616a76ad74611e7d`, four commits on top of `992c3d7b` (`97e9cfd8` leg, `267d669f` campaign, `274070e8` docs, `ba56827b` doc-style fix), no rebase, no force |
| Superseded gate run | the full set first ran at `274070e8`. The sweep there was green (65 of 65), but docs.yml `docs-gates-0` `gate_9` failed: `CHANGELOG.md:73` and `:75` were 11-word sentences against the 10-word limit (`receipts/diagnostic/docsyml-274070e8/docs-gates-0__gate_9.log`). `ba56827b` fixes those two lines and a README wording slip (`MAAP, and its MAAP and CRF talker` -> `MAAP, and MAAP and the CRF talker`), and every gate re-ran at `ba56827b`. The `274070e8` receipts are in `receipts/diagnostic/` |
| Remote | `origin` = `https://github.com/kebag-logic/milan-fpga.git` (verified) |
| TAKEN on #839 | posted, issuecomment-6663523296 (text: `taken.md`) |
| REVIEW READY on #839 | posted, issuecomment-6671536177 (text: `review-ready.md`), naming head `ba56827b` |
| Submodules | none edited, none entered with git |
| `hdl/` | unchanged: `git diff --stat 992c3d7b ba56827b -- hdl syn configs protocol-processor gptp-processor third_party` is empty (`receipts/area/synthesis-inputs-unchanged.txt`). No new check showed an RTL defect, so there was no STOP |
| CPU booking | `cpu_ranges.py pick` found no free range at either launch (`busy 128 cpus; free16 [] free12 []`), so the four shard units run on this unit's own range, 112-115, 116-119, 120-123, 124-127, four CPUs each, as round 1's diagnostic sweeps did. MemAvailable 42 GB and 50 GB at the two launches, so in parallel. The lane gates ran on CPUs a finished shard had freed |

## The assignment (issuecomment-6655612150), item by item

| # | Item | Done | Where |
|---|---|---|---|
| 1 | R773-1 F1 = R774-1 F1: a boot arm that enables MAAP, AAF (enable plus bypass) and CRF at reset release, before the station-MAC write, and grades their frames; a planted control removing those three holds fails it by name; the AAF talker offers inside the held window, or the README says why not with the RTL lines | Done. Two early-enable boots. With MAAP on, MAAP and the CRF talker offer inside the window. The AAF talker structurally cannot, and the README gives the RTL lines. With MAAP off, the AAF talker offers inside the window. The three-hold control fails both boots by name, and one control per source fails that source's own check | `sim_boot_sa.cpp:549-618`, README `:1159-1181`, `bootsa_mutants.py:116-127` |
| 2 | R773-1 F2, option (a): the leg compares every control-lane octet outside 6 to 11 with what entered the stamp; a beat-position-wrap control fails it by name; README and TESTING match what the leg checks | Done | `sim_boot_sa.cpp:429-452`, `:621-629`; `bootsa_mutants.py:128-130`; README `:1183-1202`; `TESTING.md:277` |
| 3a | S1: CRF required where the config declares it; MVRP driven or excluded with the reason | CRF required when `kCrfOutputDeclared` (generated from `boot_policy.crf_output_declared()`). MVRP driven: a listener's PROBE_TX_COMMAND once MAAP holds its claim (Milan v1.2 4.3.3.1, 4.3.2), and MVRP is in the required list | `sim_boot_sa.cpp:731-757`, `:817-825`; `gen_boot_fw.py:150-156` |
| 3b | S2: link the decision record in the PR body | Done | `PR-BODY.md`, Linked Issue |
| 4a | RES-1 = R2: the area paragraph says the head synthesis ran at `8d2dfb65` | Done, with R773-1's exact text in the PR body's area paragraph and R774-1's exact text in REVIEW READY | `PR-BODY.md`, `review-ready.md` |
| 4b | R774-1 R1: both "pending a maintainer" phrases replaced by the exact text | Done | `PR-BODY.md` (Known limitations, Definition of Done) |

## Design of the round-2 checks, and why

- **Why two early-enable boots.** The assignment's arm enables MAAP, AAF and CRF at reset release. With MAAP enabled, the AAF talker cannot offer a frame while held, however long the window is:
  - `aaf_gate` needs `maap_addr_valid` while `cfg_maap_enable` is set (`hdl/milan/milan_datapath.sv:2214-2217`);
  - `addr_valid_o` is `state_r == ANNOUNCE_S` (`hdl/ieee1722/maap/KL_maap.sv:189`), reached only when the fourth PROBE is sent (`:487-489`);
  - a PROBE is sent only when `!tx_busy_r` (`:477`), and `tx_busy_r`, MAAP's `tvalid` (`:307`), drops only on an accepted beat (`:392-395`);
  - the hold gives MAAP `tready` 0 (`milan_datapath.sv:8818`).

  The simulation agrees: in the MAAP-on boot, `AAF no` among the offers. So a second boot leaves MAAP off. That opens the gate's `~cfg_maap_enable` term, and the AAF talker offers inside the window (`AAF yes`).
- **Why the boot words.** The arm writes `MILAN_MAAP_CTRL_BOOT`, `MILAN_AAF_CTRL_BOOT` (plus `AAF_CTRL[1]`) and `MILAN_CRF_TX_CTRL_BOOT`, the words `configure_fabric()` writes, exported by `gen_boot_fw.py` together with the firmware's own CSR offsets. The arm then differs from the firmware's boot only in the order.
- **Why "offered" is graded.** Each source's own `tvalid`, ahead of the transmit gate (`maap_txs_tvalid_w`, `aaf_txs_tvalid_w`, `crft_txs_tvalid_w`, made readable by `bootsa_probes.vlt`), must rise while the pair is unwritten. A boot where a source never tried therefore fails instead of passing vacuously, as the main boot's `pp_offered_early_` check does for the processor.
- **The octet comparison.** On `ctlg2` valid/ready, each kept octet at a frame position outside 6 to 11 is compared between `ctlg_src_tdata_w` (the IFG gasket's output, the stamp's input) and `ctlg2_tdata` (the stamp's output). The position is the harness's own count of kept octets, not the RTL's `ctl_sa_idx_r`. A beat on a reset edge is not counted.
- **MVRP.** A VLAN is joined only for a stream FSM's user (`protocol-processor/hdl/srp/KL_srp_vlan.sv:14-20`). The talker FSM joins one when the ACMP DA-gate opens (`KL_srp_talker_fsm.sv:25-27`), and that happens on a PROBE_TX with the destination allocated (`protocol-processor/hdl/acmp/KL_acmp_talker.sv:821-827`). Without a probe, MVRP has nothing to send, as the probe run showed: 5M cycles past the first ENTITY_AVAILABLE and no MVRP frame (`receipts/dev/run-mvrp-probe.log`). The leg probes once MAAP holds its claim, retrying up to five times until SUCCESS (it succeeded on the first try). The first MVRP frame leaves about 19k cycles later.

## Changes (file:line at `ba56827b`)

| Change | Where | Clause / reason |
|---|---|---|
| Two early-enable boots: reset, MAAP (first boot only), AAF (boot word with `AAF_CTRL[1]`) and CRF enabled at reset release, 400 processor ms held, then the pair; graded per source | `tb/verilator/milan_dp/sim_boot_sa.cpp:549-618` (`early_enable`), `:531-539` (`write_pair`), `:864-865` | IEEE 802.1AC-2016 11.1, IEEE 802.1Q-2022 6.8.1; acceptance 1 ("holds each transmitter") for MAAP, AAF and CRF |
| Each held source's own `tvalid` observed while the pair is unwritten | `sim_boot_sa.cpp:304-310`; `bootsa_probes.vlt:12-14` | the boots cannot pass without the source trying |
| The control lane compared octet by octet across the stamp | `sim_boot_sa.cpp:429-452` (`stamp_edge`), `:621-629` (`grade_stamp`), `:866`; `bootsa_probes.vlt:15-20` | IEEE 802.3-2022 2.3.1.2: the MAC entity inserts its own address and touches nothing else |
| CRF required in "sent and graded" where the config declares it; MVRP required | `sim_boot_sa.cpp:817-825`; `gen_boot_fw.py:154-156` | CRF: the config's own declaration, `clocking.crf_output` (`boot_policy.crf_output_declared()`); MVRP: Milan v1.2 4.3.2 |
| A listener's PROBE_TX_COMMAND once MAAP holds its claim, so the talker joins its VLAN by MVRP | `sim_boot_sa.cpp:731-757` (`probe_tx`), `:860` | Milan v1.2 4.3.3.1, 4.3.2, 5.5.2.2 (CONNECT_TX renamed PROBE_TX), Table 5.33; IEEE 1722.1-2021 8.2.1.4 (message_type 0), Table 8-4 (FAST_CONNECT bit 14 = 0x0002) |
| `boot_fw.h` exports the firmware's CSR offsets for the pair, MAAP_CTRL, AAF_CTRL, CRFT_CTRL, the three boot words, and `kCrfOutputDeclared` | `tb/verilator/milan_dp/gen_boot_fw.py:48-52`, `:107-111`, `:147-156` | the values come from the firmware and `boot_policy`, not from the harness |
| Five new controls | `tb/verilator/milan_dp/bootsa_mutants.py:69-89` (names and edits), `:116-130` | the Tests lens: each new check can fail |
| Test-evidence disposition updated to twelve controls | `scripts/measure_test_evidence_readers.py:170-176` | the ratchet's reader list |
| Docs | `tb/verilator/milan_dp/README.md:110`, `:1144-1236`; `docs/testing/TESTING.md:277`; `CHANGELOG.md:73-76` | the leg's checks stated exactly (F2), and the RTL lines for the AAF case (F1) |

## New checks, their planted controls and the failing words

Every new check line starts `[BOOTSA] `.

| Check | Control that must fail it | Failing words in that control's run |
|---|---|---|
| `early-enable, MAAP on: no MAAP frame leaves before the station MAC is written` | no hold on MAAP, AAF and CRF; no hold on MAAP alone | `got=1 exp=0` (both) |
| `early-enable, MAAP on: no CRF frame leaves before the station MAC is written` | no hold on the three; no hold on CRF alone | `got=10 exp=0` |
| `early-enable, MAAP off: no AAF frame leaves before the station MAC is written` | no hold on the three; no hold on AAF alone | `got=62 exp=0` |
| `early-enable, MAAP off: no CRF frame leaves before the station MAC is written` | no hold on CRF alone | `got=10 exp=0` |
| `every control-lane octet outside 6 to 11 leaves the stamp as it entered` | the stamp's beat position wraps past the source address instead of saturating (`ctl_sa_position`'s saturation removed) | `got=126 exp=0`, first `frame 1 octet 38 entered 0 left 2` |
| `early-enable, MAAP <on/off>: <MAAP/the AAF talker/the CRF talker> offered a frame while the station MAC was unwritten` | precondition, like `the processor offered a frame before the station MAC was written` | n/a (fails on a boot where the source never tried) |
| `early-enable, ...: <kind> frames leave once the station MAC is written`, `no CSR-addressed transmitter starts a frame ...`, `no frame carries the all-zero source address`, `every frame of the boot carries the station MAC`, `A_TXARB_DIAG ...` | the three-hold control also fails the second to fourth of these in both boots (`got=11` with MAAP on, `got=72` with MAAP off) | see `receipts/gates/mutant-runs/` |
| `MVRP frames were sent and graded`, `the talker answers PROBE_TX_COMMAND with SUCCESS`, `the probed talker joins its VLAN by MVRP` | coverage checks: they fail when MVRP or the probe's answer is missing | n/a |
| `CRF frames were sent and graded` (where the config declares CRF) | coverage check | n/a |

The failing words above are from the five controls' own runs at `ba56827b` (`receipts/gates/mutant-runs/run-07.log` to `run-11.log`, each with its planted diff `mutant-07.diff` to `mutant-11.diff`), built on a clean clone through `bootsa_mutants.py`'s own plant, build and verdict code (`receipts/gates/tools/keep_mutant_logs.py`). Their `[FAIL]` lines are identical to the same runs at `274070e8` (`receipts/diagnostic/mutant-runs-274070e8/`) and to the dev runs (`receipts/dev-mutants/`). The gate itself is `make -C tb/verilator/milan_dp bootsa-mutants`: `13 checks: 13 PASS, 0 FAIL`.

## Gates

Every gate at head `ba56827bbfe4acadb84ca220616a76ad74611e7d`, on clean clones of the committed head: the four sweep shard clones, one `clone_at.sh` clone for the lane gates, one for the control runs, and one fresh clone per `docs.yml` job. Never piped; one log and one rc each. Receipts are under `receipts/gates/`. Host path prefixes in the copied logs are redacted to `<home>`, `<lanes>`, `<scratch>` and `<data>` (`tools/collect.py`). Logs over 200 KB are listed by size and the sha256 of the original in each directory's `LARGE-LOGS.txt`, with a tail beside them.

| Gate | Command (as run) | rc | What the log shows | Receipt |
|---|---|---:|---|---|
| Full Verilator sweep, 4 native shards | `native-shards.py 839-a731b sweep4-ba56827b-spec.json <out> 4 112-115 116-119 120-123 124-127`; each shard runs `scripts/run_all_suites.sh <logs> --wait --shard k/4` with `MAKEFLAGS=-j4 --no-print-directory` | 0, 0, 0, 0 | shard 0: 15 of 15 suites, 361,188 checks; shard 1: 17 of 17, 1,525,511; shard 2: 17 of 17, 284,228 (`capture_coherence` here, on 4 CPUs); shard 3: 16 of 16, 21,575. 65 of 65 suites, 0 failed, 0 timed out, 2,192,502 checks, 0 in-suite failures. Each shard's preflight (its suite-cancellation self-test among it) passed first time, and `gptp_shadow` passed in shard 1, so no #833 re-run was needed. `milan_dp`: `== bootsa: checks: 67   failures: 0 ==`, gptp and gptp-lat `210 checks: 210 PASS, 0 FAIL` each; `milan_dp_render`: `tdm8_render: checks: 263 failures: 0` | `gates/sweep/shard-*/` (`01.log`, `complete.json`, `results.json`, suite logs, `preflight/`); the leg's own section `gates/sweep/shard-0/bootsa-section-of-milan_dp.log` |
| Firmware self-test | `tally_selftest.py`; `fw_rv32_selftest.py --require-rv32`; `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard k/4` for k = 0..3; `test_ctrl_nvm.py --require-rv32 --jobs 4` | all 0 | `tally self-test: 18 of 18 planted cases read as planted`; `RV32 build self-test: 17 checks PASS`; four shards `test_ctrl_firmware: PASS` (shard 0: `18 planted defects caught`; shard 1: `mutants: 523 of 523 caught`); `saved-state store gate (#665 F1): OK across 5 shape(s), 435 tests` | `gates/lane/fw_*` |
| Firmware coverage | `fw_coverage.py --selftest`; `fw_coverage.py --check --jobs 8` | 0, 0 | `coverage self-test: 29 of 29 planted cases read as planted`; `firmware coverage: PASS (30 files)` | `gates/lane/fw_coverage_*` |
| Builder | `python3 sw/builder/test_builder.py --require-rv32` | 0 | `ALL GATES PASS EXCEPT 2 NOT RUN`, each with the builder's reason: gate 1b's `MAKEFLAGS += -e` mutation has nothing to act on with this host's make; gate 11's calibration needs a build tree that is not on this host. Also run inside `docs.yml` (`docs-gates-1` `gate_25_0`, `docs-gates-2` `gate_25_1`) | `gates/lane/builder.*`; `gates/docsyml/` |
| behave | `cd tests && behave` | 0 | `14 features passed, 0 failed, 0 skipped`, `508 scenarios passed`, `2330 steps passed` | `gates/lane/behave.*` (log by hash, tail kept) |
| Every `run:` step of `docs.yml` | `run_docs_yml.py <head> <job> <root>` for each of its nine jobs, then `verify_docs_yml.py` (the assigned runner and verifier, their paths pointed at this lane: `diff` in `gates/tools/runner-diff.txt`) | verify 0 | `64 steps ran, 31 not run with a reason, 0 bad`; all nine jobs `failed 0`; every clone clean after its job. The 31 are hosted-only steps (records, uploads, cancels, apt and sudo installs), each with its reason in `tools/not_run.json`. The builder legs read `ALL GATES PASS EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN` | `gates/docsyml/` |
| `scripts/docs_inventory.py --check` | NOT RUN: `git ls-tree` finds it neither at the head nor at the base | n/a | `scripts/docs_inventory.py is in neither tree: NOT RUN` | `gates/lane/docs_inventory_absent.*` |
| `git diff --check` against the merge base | `git diff --check 604899c08ff1cd1830e1dd08b733109ef852400c HEAD` | 0 | no output | `gates/lane/diffcheck.*` |
| The leg's planted controls | `make -C tb/verilator/milan_dp bootsa-mutants` | 0 | `13 checks: 13 PASS, 0 FAIL`: the clean leg passes, and all twelve controls are caught by every check they name, the five new ones among them | `gates/lane/bootsa_mutants.*`; full runs of the five new ones in `gates/mutant-runs/` |

Not in the round-2 gate set (issuecomment-6655612150 lists it) and not re-run: Yosys, the RTL lint ratchet, `pp_srcs.py`, the LiteX SoC simulations and `elaborate.yml`'s elaboration legs. Their last receipts are round 1's, at `992c3d7b`. `git diff --stat 992c3d7b ba56827b` touches only `tb/verilator/milan_dp/`, `scripts/measure_test_evidence_readers.py`, `docs/testing/TESTING.md` and `CHANGELOG.md`: no file under `hdl/`, `syn/`, `sw/` or `configs/`, and no submodule pin.

Run notes:

- The first gate run, at `274070e8`, found `docs.yml` `gate_9` red on the two CHANGELOG sentences. `ba56827b` fixes them, and everything above re-ran at `ba56827b` (`receipts/diagnostic/`: `sweep-274070e8/` green 65 of 65, `docsyml-274070e8/` with the failing `gate_9`, `lane-274070e8/` stopped during the builder once `gate_9` had failed, `mutant-runs-274070e8/`).
- Round 1's scratch, its docs venv included, was removed from the host during this session (after the light `docs.yml` jobs at `ba56827b` had run on it). This lane then made its own venv with `pyyaml`, plus the pinned `wavedrom==2.0.3.post3` that `not_run.json`'s reason for the skipped `Install diagram gate dependencies` steps relies on. Two `docs.yml` runs at `ba56827b` are diagnostic only: the light jobs on the removed venv (`receipts/diagnostic/docsyml-ba56827b-oldvenv/`), and a full run on the new venv before `wavedrom` was in it, where `gate_13` failed with `the 'wavedrom' package is missing` (`receipts/diagnostic/docsyml-ba56827b-nowavedrom/`). The `docs.yml` row above is a third, full run of all nine jobs on the completed venv.

## Area

The RTL is unchanged in round 2. Round 1's out-of-context figures (base `604899c0` 45,176 LUTs, 40,222 registers; head 45,275 / 40,233, +99 / +11) were synthesised at `8d2dfb65`. Nothing synthesis reads differs between `8d2dfb65`, `992c3d7b` and `ba56827b` (`receipts/area/synthesis-inputs-unchanged.txt`), so they stand at the round-2 head. No new synthesis run.

## Findings outside scope (for new Issues; not filed)

- Round 1's two notes stand (`test_sim_pool.py`'s `LEGACY_LEGS` lacks `obj_sidmove`/`obj_sidmove8` at the base; the README's stale prose counts).
