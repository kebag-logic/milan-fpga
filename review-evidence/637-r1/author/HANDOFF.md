# Lane 637 (author [A656]) — HANDOFF

Status: REVIEW READY at `63a187e1579474bca562d85304b9a91466877c33` (local, not pushed). Every gate rc 0 at the head
or at a commit whose `hdl` equals it. The on-board cold cycle is not done (no bench access in this lane).

- Branch `637-map-records` from dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f` (processor pin `2cbed0a9`), not pushed.
- Commits on `e9cbb676`: `6ab04441` (RTL and the leg), `bbc6690b` (check 15, campaign arms), `bdff750c` (docs,
  READMEs, RTL comments), `5537211f` (more scenarios), `4cf7f4b9` (pending composition in the docs), `90b15366`
  (area cut and the aggregate scenario), `e3105d21` (deadline arms), `79f8aa89` (the held SET's premise), `edbd11a0`
  (README campaign table), `cf5c0c23` (pp_shadow P2), `63a187e1` (REGISTER_MAP PP_NVM_STAT[4]).
- `git diff 90b15366 HEAD -- hdl` is empty: the routed and standalone-measured commit carries the head's RTL.
- TAKEN: issue #637 comment 6257357939. REVIEW READY: issue #637 comment 6267367417 (text in `receipts/review-ready.md`).

## Step 0: dependencies (MATERIALIZATION 18.4, lane 4)

- Lane 1: done. Processor PR #132 (`d352bbaa`) is an ancestor of the pin.
- Lane 2: done. PR #623 (merge `e4b771f9`, processor `b2db3a97`) is in dev.
- Lane 3: NOT done in the parent (MATERIALIZATION.md:15-16 at base, MILAN_COMPLIANCE_MATRIX.md:182 at base). It
  does not block: the name records (`0x80..`) are disjoint, and this lane changes no name path. The name half of
  the sticky pending stays.
- DR3a: ratified (#70 comment 5873060660). DR4: ruled (#70 comment 5862405632). The maps ceiling is 1,250 LUT /
  600 FF incremental at 1x1 TDM8 (MATERIALIZATION.md:2380 at base).

## Design

- The processor never writes or reads maps (`KL_aecp_nvm_writer.sv:119-121`; processor `07_memory_maps.md:584-610`, 5.1, at
  the pin). The parent writes and restores them, with no processor change.
- The parent reaches `KL_nvm_backend` through a 2:1 device-face arbiter in `KL_pp_shadow.sv`, beside the
  processor's NVM port.
- The writer and the restore live in `milan_datapath.sv`, where the map stores and the edit server are.
- The restore applies a saved set through the existing ADD/REMOVE transaction server, so its value rule is the
  ADD rule itself (D3 15 item 7, parity by reuse).
- One deliberate deviation, published: one read pass, not two. The parent's roll-back reaches every map, so a
  second pass ends in the same states and only lengthens the faces' hold. That hold is bounded by the
  processor's 4,096-clock gather watchdog (`DESC_MEM_TMO_CYC_P`).

## Changes (file:line at the head, clause)

`hdl/milan/KL_pp_shadow.sv`
- `:402-433` the record face `mrec_*`, `amap_unflushed_i`, `amap_alarm_i` (07 5.1; D3 15 item 2, amended).
- `:1009-1020` the sticky source takes names only; `pend_i` adds `amap_unflushed_i`; the map pulse stays for the
  accepting edge (D3 5.2, 7.1; #502).
- `:1022-1099` the device-face arbiter: selection, drain, routing (D3 6.4, the drain; 15 item 4, amended).
- `:1165`, `:1180` the backend's `alarm_i` and `nvm_alarm_o` OR in the map alarm (DR2c; FASTCONNECT 9.2).
- `:1376-1391` the processor's port through the arbiter.

`hdl/milan/milan_datapath.sv`
- `:317-335` parameters `AMR_MS_CYC_P` (derived from the processor's timebase), `AMR_RS_TMO_MS_P` (20),
  `AMR_RS_AGG_MS_P` (1,000), `AMR_MEM_TMO_MS_P` (1,000) (DR2a, DR2c, DR3a; the port's T-NVM-PORT-DEADLINE).
- `:3154-3207` the edit face's processor nets renamed `ppo_*` and muxed with the restore's beats (`amr_own_r`).
- `:4166` GET_AUDIO_MAP waits while the map restore holds (07 5.1).
- `:4463` a restore beat is never a live write (D3 3.1).
- `:4641-4647` `amap_boot_busy_w` adds the map restore's hold (the edit face, the four CSR sites).
- `:4661`, `:4858` the roll-back: the stores take the clipped image and the RAMs are swept again (D3 8.6).
- `:4867-5727` the writer and the restore (`amr_*`): banner, record shape, source slot, payload generator, crc16,
  latch, set decode, the ms tick, deadlines and the FSM (Milan v1.2 5.3.9.1, 5.3.10.1; D3 3, 6.1, 7.1, 8.3, 8.4,
  8.6, 8.8; FASTCONNECT 4.2, 6.1; DR2a to DR2c, DR3a).
- `:6174` the format judge waits while the map restore runs (D3 8.4).
- `:9100-9118` the record face connected; `:9181` the entity enable waits for the map restore (07 5.1).

Comments only: `hdl/milan/KL_nvm_backend.sv:198-204`, `hdl/common/csr/milan_csr.sv:182-196`.

`scripts/check_nvm_record_space.py` check 15 and `scripts/nvm_contract.py` seam `PARENT_LAYOUT_EDIT`.

Tests: `tb/verilator/milan_dp/sim_nxn.cpp` `[MAPREC]` section and the window model's planted faults (read error,
silence, slow reads and writes, write errors); `dynmap_probes.vlt`; `Makefile` (`DYNMAP_MS_CYC`, `DYNMAP_AGG_MS`,
`SHADOW_SRC`); `dynmap_mutants.py` (24 arms, planting in `KL_pp_shadow.sv` too); `tb/verilator/pp_shadow/sim_main.cpp`
P2 (the bounded wait for the map restore's blank reads).

Docs: SAVED_STATE_MATERIALIZATION.md (status, 1, rule 9, 5.2, 8.4, 8.6, 10, 13, 15 items 2 and 3, 18.4
implementation record), SAVED_STATE_FASTCONNECT.md (1, 4.2, 12.2, 13), SAVED_STATE_SNAPSHOT_OWNERSHIP.md (status,
6.1, 11), MILAN_COMPLIANCE_MATRIX.md, REGISTER_MAP.md (CHMAP hold, PP_STAT[11]), FPGA_DESIGN.md,
BAREMETAL_FIRMWARE.md, MILAN_V12_ROADMAP.md, TESTING.md, the milan_dp and pp_shadow READMEs.

## New checks and planted mutants

`tb/verilator/milan_dp` dynmap leg, `[MAPREC]` section (`sim_nxn.cpp`, `dynmap_map_records_section`): 331 checks in
the leg, 0 failures (`receipts/gates/dynmap-run10.log`). Every planted control below was caught by its named check;
each clean leg passes (`receipts/mutants/`). Rows 12 to 35 are this lane's.

- Empty list, both directions: `empty: ...` and `empty, after the power cycle: ...` (rows 12, 13, 14, 34).
- Non-empty non-default list: `saved: ...`, `saved, after the power cycle: ...` (rows 15, 25).
- Torn-record control (a payload byte changed under its crc16, to a list the ADD rule would take): `torn input
  record: ...` (row 16).
- The parent's roll-back on a read error after the input was applied: `roll-back: ...` (rows 17, 18, 19).
- The D3 walk's roll-back (planted `rb_r`): `D3 roll-back: ...` (row 20).
- Held GET at the terminal and the entity enable: `held GET: ...` (rows 21, 23).
- Held SET_STREAM_FORMAT judged on the restored list: `held SET_STREAM_FORMAT: ...` (row 22).
- DR2b, an unchanged ADD writes nothing: `unchanged: ...` (row 24).
- Taint, a change during the slowed record write: `taint: ...` (row 26).
- DR2c, a record whose writes always fail: `failing writes: ...` (rows 27, 28, 29, 35).
- Per-wait deadline, silent memory: `silent memory: ...`, and the drain on a late answer (rows 30, 32).
- Aggregate deadline, slow memory: `slow memory: ...` (row 31; the leg compiles the aggregate to 300 ms, a test value).
- One device face, two initiators: `shared face: ...` (row 33).
- The parent layout literal: `scripts/check_nvm_record_space.py` check 15, control `--mutate=parent_layout`, caught
  ("the parent map writer frames layout_version 0x03 ... the donor's LAYOUT_VER_P is 0x02").

| # | Leg | Planted in | Mutant | Named check that fails | Failures |
|---:|---|---|---|---|---|
| 1 | dynmap | `milan_datapath.sv` | an empty reset: the power-on image holds no mapping | `[DYNMAP] power-on SPI 0: number_of_mappings` | 91 of 331 |
| 2 | dynmap | `milan_datapath.sv` | no clip after the restore: the window ignores a restored input format | `[DYNMAP] restored SPI 0: number_of_mappings` | 6 of 331 |
| 3 | dynmap | `milan_datapath.sv` | no output clip: the window ignores a STREAM_OUTPUT row | `[DYNMAP] window, output row staged at 4 ch: capture RAM keys 0..7 hold the output map` | 2 of 331 |
| 4 | dynmap | `milan_datapath.sv` | the boot writer never fills the crossbar RAMs | `[DYNMAP] power-on: render RAM keys 2..9 hold the input map` | 70 of 331 |
| 5 | dynmap | `milan_datapath.sv` | the CSR writer is not held while the boot writer is busy | `[DYNMAP] CSR hold, input: no CSR write splits the store from the RAM` | 4 of 331 |
| 6 | dynmap | `milan_datapath.sv` | the input store alone takes a CSR write while the writer is busy | `[DYNMAP] CSR hold, input: no CSR write splits the store from the RAM` | 2 of 331 |
| 7 | dynmap | `milan_datapath.sv` | the output store alone takes a CSR write while the writer is busy | `[DYNMAP] CSR hold, output: no CSR write splits the store from the RAM` | 2 of 331 |
| 8 | dynmap | `milan_datapath.sv` | the boot window ignores the CLOSED terminal | `[DYNMAP] CSR hold, input: CSR lands in both once the sweep after CLOSED has ended` | 2 of 331 |
| 9 | dynmap | `milan_datapath.sv` | no sweep after the restore's terminal | `[DYNMAP] CLOSED on the roll-back's clock: render RAM keys 2..9 hold the input map` | 6 of 331 |
| 10 | dynmap | `milan_datapath.sv` | no drain clock: busy ends while the last boot write is in flight | `[DYNMAP] CSR hold, input: no CSR write splits the store from the RAM` | 4 of 331 |
| 11 | dynmap | `milan_datapath.sv` | the edit face never waits for the boot writer | `[DYNMAP] edit meets the sweep: the ADD is answered only after the sweep ends` | 2 of 331 |
| 12 | dynmap | `milan_datapath.sv` | the map writer never marks a record dirty | `[MAPREC] empty: the window holds the codec's records and the pend has fallen` | 30 of 331 |
| 13 | dynmap | `milan_datapath.sv` | an empty saved list reads as an erased record (#763) | `[MAPREC] empty, after the power cycle: SPI 0: number_of_mappings` | 17 of 331 |
| 14 | dynmap | `milan_datapath.sv` | no first-dirty window: the change is written at the next tick | `[MAPREC] empty: the write waited out the 500 ms first-dirty window` | 2 of 331 |
| 15 | dynmap | `milan_datapath.sv` | the restore refuses every framed record | `[MAPREC] saved, after the power cycle: SPI 0: number_of_mappings` | 42 of 331 |
| 16 | dynmap | `milan_datapath.sv` | the restore ignores the record's crc16 | `[MAPREC] torn input record: SPI 0: number_of_mappings` | 3 of 331 |
| 17 | dynmap | `milan_datapath.sv` | a failed walk rolls nothing back | `[MAPREC] roll-back: SPI 0: number_of_mappings` | 11 of 331 |
| 18 | dynmap | `milan_datapath.sv` | the roll-back sweeps the RAMs and leaves the stores | `[MAPREC] roll-back: SPI 0: number_of_mappings` | 11 of 331 |
| 19 | dynmap | `milan_datapath.sv` | the roll-back puts the stores back and never sweeps the RAMs | `[MAPREC] roll-back: render RAM keys 2..9 hold the input list` | 3 of 331 |
| 20 | dynmap | `milan_datapath.sv` | the map restore runs over the D3 walk's roll-back | `[MAPREC] D3 roll-back: SPI 0: number_of_mappings` | 6 of 331 |
| 21 | dynmap | `milan_datapath.sv` | GET_AUDIO_MAP does not wait for the map restore | `[MAPREC] held GET: answered with the restored list` | 1 of 331 |
| 22 | dynmap | `milan_datapath.sv` | the format judge does not wait for the map restore | `[MAPREC] held SET_STREAM_FORMAT: SUCCESS against the restored list` | 2 of 331 |
| 23 | dynmap | `milan_datapath.sv` | the entity enable does not wait for the map restore | `[MAPREC] held GET: the entity enable waits for the map restore` | 1 of 331 |
| 24 | dynmap | `milan_datapath.sv` | every phase-5 beat marks its record, changed or not (DR2b) | `[MAPREC] unchanged: no record write follows an unchanged edit` | 3 of 331 |
| 25 | dynmap | `milan_datapath.sv` | a restore write counts as a change | `[MAPREC] saved: the restore itself writes no record` | 2 of 331 |
| 26 | dynmap | `milan_datapath.sv` | a change after the latch does not taint the write | `[MAPREC] taint: the window ends on the final list` | 5 of 331 |
| 27 | dynmap | `milan_datapath.sv` | a fourth attempt follows the third failure | `[MAPREC] failing writes: three attempts, then no more` | 1 of 331 |
| 28 | dynmap | `milan_datapath.sv` | no backoff between attempts | `[MAPREC] failing writes: the attempts are at least 500 ms apart` | 1 of 331 |
| 29 | dynmap | `milan_datapath.sv` | the last failed attempt raises no alarm | `[MAPREC] failing writes: the alarm (PP_STAT[4]) is raised` | 1 of 331 |
| 30 | dynmap | `milan_datapath.sv` | the map restore has no per-wait deadline | `[MAPREC] silent memory: the walk ends at its per-wait deadline` | 1 of 331 |
| 31 | dynmap | `milan_datapath.sv` | the map restore has no aggregate deadline | `[MAPREC] slow memory: SPI 0: number_of_mappings` | 8 of 331 |
| 32 | dynmap | `KL_pp_shadow.sv` | the arbiter does not drain a read the map writer abandoned | `[MAPREC] silent memory, late answer: a later change reaches the window` | 1 of 331 |
| 33 | dynmap | `KL_pp_shadow.sv` | the arbiter's selection moves while the backend serves a command | `[MAPREC] shared face: both writers' records are in the window` | 1 of 331 |
| 34 | dynmap | `KL_pp_shadow.sv` | the map writer's pending is not reported | `[MAPREC] empty: PP_STAT pend rises with the accepted change` | 1 of 331 |
| 35 | dynmap | `KL_pp_shadow.sv` | the map writer's alarm does not reach nvm_alarm | `[MAPREC] failing writes: the alarm (PP_STAT[4]) is raised` | 1 of 331 |
| 36 | listener | `milan_datapath.sv` | an empty reset, under the listener's end-to-end check | `T18 POWER-ON: with no map command since the reset, the lane renders injected events` | 8 of 264 |
| 37 | talker | `milan_datapath.sv` | an empty reset, under the talker's end-to-end check | `[V] every requested column was decoded` | 20 of 134 |

One arm survived the first full run: row 22, the format judge. The held SET_STREAM_FORMAT reached its judge after the
input port was already restored, so the hold made no difference. The scenario now slows the input record's lanes by
250 clocks (the whole hold stays inside the 4,096-clock gather watchdog) and adds the premise "...while the input port
still held its reset set"; the row was then caught (`receipts/mutants/mutant-22.log`) and caught again in the final
run.

## Resource / timing

Recipe unchanged (`docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, `--single-thread-synthesis`, Vivado 2026.1 under
the exclusive lock, `pp_resource_gate.py check --endpoint route-1x1`); driver `receipts/route-1x1/route.sh`, each run
on a clean clone.

| Route-1x1 | LUT | FF | SLICE | RAMB36 | RAMB18 | DSP | WNS ns | WHS ns | gate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| base `e9cbb676` | 49,613 | 52,353 | 15,725 | 74 | 25 | 14 | +0.215 | +0.036 | rc 0 (equals the accepted record) |
| first head `6ab04441` | 50,203 (+590) | 52,699 (+346) | 15,720 | 74 | 25 | 14 | +0.479 | +0.036 | rc 1: LUT grew by more than 500 |
| head `90b15366` (logic of the final head) | 49,902 (+289) | 52,615 (+262) | 15,801 (+76) | 74 | 25 | 14 | +0.316 | +0.015 | rc 0 |

- The first head's +590 LUT was +525 in `milan_datapath`'s own logic. `90b15366` cut it: the deadlines count
  milliseconds (11-bit counters), one crc16 step is shared, the byte counter is 11 bits, the header is judged as it
  streams, the owner compares use the bits an owner can differ in, and REMOVE reads the clip instead of the live
  store (equal at restore time, by the holds). Post-synthesis: +619 to +445.
- `u_nvm` grows by +153 to +164 in every head, from the arbiter's muxes on the backend's request inputs. The rest of
  the movement is the optimizer's in unrelated blocks (gPTP shadow about -285, CSR +100).
- DR4's maps-stage ceiling is 1,250 LUT / 600 FF incremental; the head uses +289 / +262.
- Route complete at every head, no unrouted net. WHS stays positive (+0.015 ns).
- `git diff 90b15366 HEAD -- hdl` is empty (only tests and docs after it).

Standalone `KL_pp_shadow` (the recipe's standalone measurements, `--integrated-clock`; the 8x8 parameter block from
the recipe's RTL-only elaboration of the 8x8 export), `pp_resource_gate.py check`:

| Endpoint | base LUT / FF | head LUT / FF | delta | gate (base, head) |
|---|---|---|---|---|
| ooc-1x1 | 23,314 / 19,821 | 23,366 / 19,823 | +52 / +2 | rc 0, rc 0 |
| ooc-8x8 | 30,211 / 27,451 | 30,282 / 27,451 | +71 / 0 | rc 0, rc 0 |

Both bases equal the accepted records. RAMB36, RAMB18 and DSP are unchanged at every endpoint. The head of these
runs is the routed head `90b15366`.

## Gates

All commands unpiped, one log and rc each; logs in `receipts/gates/` and `receipts/final/`. Python gates ran under
CPython 3.12.3 (the hosted runner's) with the hash-locked Markdown, HDL-reference and PyYAML pins, except the suite
sweep: its process-ownership preflight needs `os.pidfd_open`, which that 3.12.3 build lacks, so the sweep ran under
the host's CPython 3.14.8 (PyYAML 6.0.3). Verilator 5.050 (pinned), Yosys 0.66 (the workflow's sha), sv2v v0.0.12.

| Gate | Head | rc |
|---|---|---|
| `scripts/lint_rtl.py --check --self-test` | `79f8aa89` (hdl = final) | 0 (`hdl/milan` 2 of ratchet 2) |
| `scripts/pp_srcs.py --check --selftest` | `79f8aa89` | 0 |
| `scripts/xvlog_gate.py --check`, `--selftest` (under the Vivado lock) | `79f8aa89` (hdl = final) | 0, 0 (0 findings) |
| `syn/yosys/run.sh` | `e3105d21` (hdl = final) | 0 (58 of 58 tops; tap purity PASS) |
| `syn/ooc` and `syn/yosys` self-tests (12, as `rtl-fast` runs them) and `pp_resource_gate_mutants.py` | `79f8aa89` | all 0 |
| `scripts/check_nvm_record_space.py`, `--self-test` | `79f8aa89` | 0, 0 (22 controls, `parent_layout` among them) |
| `scripts/check_nvm_capture.py` (its controls included) | `79f8aa89` | 0: census, clocks, both timing arms and receipt agree, so no re-measure is owed |
| docs: `docs_check`, `check_doc_paths`, `check_doc_style` (+selftest), `gen_toc --check`, `check_em_dash --base e9cbb676` (+selftest), `check_feature_status`, `check_gptp_docs` (+selftest), `check_solution_docs` (+selftest), `check_submodule_docs` (+selftest), `check_wire_accountability --self-test`, `ci_scope --selftest`, `check_baremetal_only --check`, `gen_hdl_reference --selftest` and build | final | all 0 |
| `make -C tb/verilator/milan_dp dynmap` | `79f8aa89` (leg unchanged since) | 0, 331 checks, 0 failures |
| `make -C tb/verilator/milan_dp dynmap-mutants` | `79f8aa89` | 0, 37 of 37 caught |
| `make -C tb/verilator/pp_shadow` | `cf5c0c23` | 0 (610, 610, 650, 317 checks) |
| `scripts/run_all_suites.sh`, first run | `79f8aa89` | 1: 62 of 63 suites; `pp_shadow` P2 failed (see below) |
| `scripts/run_all_suites.sh`, final | `63a187e1` | 0: 63 of 63 suites, 2,186,578 checks, 0 failures, 0 timed out (4 declared `tsn_fuzz` skips: the external generator is absent) |
| docs, lint, `pp_srcs`, record-space, capture, HDL reference at the head | `63a187e1` | all 0 (`receipts/final/`) |
| route-1x1, ooc-1x1, ooc-8x8 | see Resource / timing | 0 |

**The first sweep's one failure, and its fix.** `pp_shadow` P2 read `PP_NVM_STAT[4]` (`dev_busy`) right after the
restore walk and found an operation in flight. It was the map restore's blank read of record `0x60`: a probe showed
the bit clear 20 idle clocks later. Since #637 that read follows the D3 terminal by design. The check now waits up to
2,000 clocks for the device face to go idle, graded as its own check, and then asserts the original condition
unchanged (`cf5c0c23`).

**Its planted control** (`receipts/ppshadow-control/`). A map restore that never takes its read bytes and has no
per-wait deadline (`hold-control.diff`) fails the new check, "PP_NVM_STAT[4]: the map restore's blank reads end
within 2,000 clocks", and the original one: 610 checks, 2 failures. Never taking the bytes alone is healed by
design: the 20 ms per-wait deadline fires and the arbiter's drain completes the read, so the face still goes idle in
bound (`rready-only-healed.log`). Reproduce from `tb/verilator/pp_shadow`, with the two edits applied to a copy at
`<dir>/hdl/milan/milan_datapath.sv` (the suite's waivers match that path):

```sh
SRCS=$(MAKEFLAGS= make -s --no-print-directory -C ../milan_dp print-srcs | tr ' ' '\n' | sed "s|.*/hdl/milan/milan_datapath.sv$|$DIR/hdl/milan/milan_datapath.sv|" | tr '\n' ' ')
make run-base BUILD_DIR="$DIR/obj" "DP_SRCS=$SRCS"
```

## Acceptance (issue #637 and the #763 additions)

| Item | Met | Evidence |
|---|---|---|
| 1. Restore at boot under the D3 rules (well-formed only; torn or corrupt keeps the default) and reset on a roll-back | yes, with one stated deviation (one read pass) | `[MAPREC]` saved, torn, roll-back, D3 roll-back, silent and slow memory; rows 15 to 20, 30, 31 |
| 2. The contract and design pages state the ownership; the processor's amended D3 contract matches | yes | D3 page status, 1, 5.2, 8.4, 15 item 2, 18.4; FASTCONNECT 1, 4.2, 12.2, 13; snapshot page 6.1, 11; processor `07_memory_maps.md` 5.1 and `KL_aecp_nvm_writer.sv:93-97,119-121` and `07_memory_maps.md:584-610` at the pin |
| 3. A parent check plants a power cycle after a map change and the maps return; a torn-record control keeps the default | yes | `[MAPREC]` empty, saved, torn |
| 4. Capture timing and census unchanged, or re-measured | unchanged | `scripts/check_nvm_capture.py` rc 0 at the head (census, clocks, both arms and the receipt agree) |
| #763: an EMPTY list in both directions and a non-empty non-default list survive a planted power cycle | yes | `[MAPREC]` empty and saved, GET_AUDIO_MAP and both crossbar RAMs |
| #763: the record format is kept (FASTCONNECT 6.1, D3 8.3 V3g) | yes | the window equals the repository codec's framing byte for byte; the empty list is a framed record of UNUSED entries |
| #763: checked on the board with a cold cycle | NOT done | no bench access in this lane |

## Open risks and questions

- The deviation: one read pass instead of the processor's two (D3 18.4, implementation record). A reviewer may want it ruled.
- The faces' hold (553 to 635 clocks here) is measured against a zero-latency window model; DDR latency adds to it, against the 4,096-clock gather watchdog.
- The entity enable now reaches the processor after the map restore, so the side port's image-window lock, which follows the requested enable, engages that much later.
- The sweep ran under CPython 3.14.8, because the CI-matching 3.12.3 build lacks `os.pidfd_open`; the other Python gates ran under 3.12.3.
- Multi-port ordering at 8x8, and the name stage (lane 3), as in the PR body's limitations.
