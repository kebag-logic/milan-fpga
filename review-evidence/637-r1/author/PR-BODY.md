[A656]

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

GREEN at `63a187e1`: 63 of 63 suites, 2,186,578 checks, 0 failures; the dynmap leg 331/331 and 37 of 37 planted controls caught; route-1x1, ooc-1x1 and ooc-8x8 resource gates rc 0. Board cold cycle not done. `637-map-records` -> `dev`.

## Linked Issue / roles

Relates to #637 (the on-board cold power cycle runs on the next e2 image; acceptance otherwise met)
Relates to #763, #70

Executor: `[A656]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

The parent now writes and restores the channel-map records `0x60` (STREAM_PORT_INPUT) and `0x70`
(STREAM_PORT_OUTPUT). The processor ruled the channel maps the integrator's (its issue 83; D3 section 15 item 2,
amended). The shipping image restored no map after a power cycle (#763). The record format is unchanged.

| Piece | File | What |
|---|---|---|
| Device-face arbiter | `hdl/milan/KL_pp_shadow.sv` | The backend's one device face is shared between the processor's NVM port and the parent's map writer. A side keeps the face while it asks, a command stays with its side until done or err, an abandoned read is drained, and an abandoned write is never padded. |
| Pending and alarm | `hdl/milan/KL_pp_shadow.sv` | `pend_i` takes the map writer's dirty bits, and the sticky source keeps names only. The map alarm joins `nvm_alarm`. |
| Writer | `hdl/milan/milan_datapath.sv` (`amr_*`) | One dirty bit per dynamic port and direction, set by the actual phase-5 change. A 500 ms first-dirty window, a one-clock latch with no edit transaction open, then taint and clear at the untainted WRITE's done. DR2c: three attempts 500 ms apart, then the reset-sticky alarm. |
| Record | same | F07.8 framing, crc16 CCITT-FALSE, the port's mappings in GET_AUDIO_MAP order, then UNUSED entries (eight `0xFF` bytes) to the capacity of FASTCONNECT 4.2. The empty list is a framed record of UNUSED entries (D3 8.3, V3g), never an erased span. |
| Restore | same | Runs only after the D3 walk's COMPLETE terminal. An erased or unframed record, and a framed one failing its layout, id, crc16, padding or ranges, keep the reset set. A well-formed set replaces the reset set through the existing ADD/REMOVE transaction server, so the value rule is the ADD rule itself. A refused ADD puts the reset set back. |
| Roll-back | same | A device error, a short read, the 20 ms per-wait or 1,000 ms aggregate deadline, or a refused put-back rolls every map back to its reset set. `restore_rb_o` or a D3 abort leaves the reset sets in place. |
| Holds | same | Until the map restore ends, the edit face, the CSR map writer, GET_AUDIO_MAP, the format judge and the entity enable wait. |
| Gate | `scripts/check_nvm_record_space.py` check 15 | The parent's layout literal is held to the donor's `LAYOUT_VER_P`, with a negative control. |
| Evidence | `tb/verilator/milan_dp` dynmap leg, `[MAPREC]` | A planted power cycle keeps the window memory across a reset. The repository's codec frames every expected record. The section has 24 planted controls in `dynmap_mutants.py`. |
| Harness | `tb/verilator/pp_shadow` P2 | Waits, within a bound, for the map restore's blank reads after the terminal before grading the idle device face. |
| Docs | the saved-state pages, references, READMEs | The ownership is stated on every page that said the maps had no writer. |

One deliberate deviation from the processor's walk: one read pass, not two. The processor reads twice so that an
abort applies nothing its roll-back cannot reach; the parent's roll-back reaches every map, so a second pass ends in
the same states and only lengthens the faces' hold, which the processor's 4,096-clock gather watchdog bounds.

## Authoritative references

- Milan v1.2 5.3.9.1 and 5.3.10.1: each Stream Port's dynamic mapping list is saved in non-volatile memory and restored after a power cycle.
- IEEE 1722.1-2021 7.4.44 (GET_AUDIO_MAP), 7.4.45 (ADD_AUDIO_MAPPINGS), 7.4.46 (REMOVE_AUDIO_MAPPINGS).
- `docs/design/SAVED_STATE_MATERIALIZATION.md` 3, 6.1, 7.1, 8.3, 8.4, 8.6, 8.8, 15 item 2 (amended), 15.1 (DR2a to DR2c, DR3a, DR4), 18.4.
- `docs/design/SAVED_STATE_FASTCONNECT.md` 4.2 and 6.1; `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` 6.1, 7 (O3) and 11.
- The processor's `docs/architecture/07_memory_maps.md` 5.1 at pin `2cbed0a9`: the channel maps are the integrator's to save, restore and roll back. No processor file changes.

## How to get into the same state

```sh
git fetch origin
git checkout 637-map-records
git submodule update --init gptp-processor protocol-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
git rev-parse HEAD
```

The Verilator gates use Verilator 5.050, Yosys 0.66 and sv2v v0.0.12, as the hosted workflows pin them.

## How to validate

```sh
python3 scripts/lint_rtl.py --check
make -C tb/verilator/milan_dp dynmap
make -C tb/verilator/milan_dp dynmap-mutants
make -C tb/verilator/pp_shadow
python3 scripts/check_nvm_record_space.py
python3 scripts/check_nvm_record_space.py --self-test
python3 scripts/check_nvm_capture.py
suite_logs=$(mktemp -d)
scripts/run_all_suites.sh "$suite_logs"
syn/yosys/run.sh
```

Expected result / pass criteria: every command exits 0. The dynmap leg reports `checks: 331   failures: 0`, and
`dynmap-mutants` reports every planted control caught. The Python gates ran under CPython 3.12.3 with the
hash-locked pins. The suite sweep ran under CPython 3.14: its process-ownership preflight needs `os.pidfd_open`,
which the local 3.12.3 build lacks.

| Gate | Result |
|---|---|
| `scripts/run_all_suites.sh` | rc 0: 63 of 63 suites, 2,186,578 checks, 0 failures, 0 timed out (4 declared external-generator skips) |
| `syn/yosys/run.sh` | rc 0: 58 of 58 tops, tap purity PASS |
| `scripts/xvlog_gate.py --check` and `--selftest` | rc 0, 0: no finding above the ratchet |
| `scripts/lint_rtl.py --check --self-test` | rc 0: `hdl/milan` at its ratchet of 2 |
| `make -C tb/verilator/milan_dp dynmap` | 331 checks, 0 failures |
| `make -C tb/verilator/milan_dp dynmap-mutants` | 37 of 37 caught (24 new), each clean leg passing |
| `make -C tb/verilator/pp_shadow` | rc 0: 610, 610, 650 and 317 checks; the new P2 check's planted control fails it |
| `scripts/check_nvm_record_space.py`, `--self-test` | rc 0, 0: 22 controls, the new `parent_layout` among them |
| `scripts/check_nvm_capture.py` | rc 0: census, clocks, both arms and the receipt unchanged, so no re-measure is owed |
| docs gates (docs_check, paths, style, TOC, em dash, feature status, gPTP, solution, submodule docs, HDL reference) | all rc 0 |
| `syn/ooc` and `syn/yosys` self-tests, resource-gate mutants | all rc 0 |
| route-1x1 (base `e9cbb676` / head) | rc 0 / rc 0: LUT 49,613 -> 49,902 (+289), FF 52,353 -> 52,615 (+262), BRAM and DSP unchanged, WNS +0.215 -> +0.316 ns, WHS +0.036 -> +0.015 ns, route complete |
| ooc-1x1 (standalone `KL_pp_shadow`) | rc 0 / rc 0: LUT +52, FF +2 |
| ooc-8x8 | rc 0 / rc 0: LUT +71, FF 0 |

The maps-stage ceiling of DR4 (1,250 LUT / 600 FF incremental at 1x1 TDM8) is met at +289 / +262. The routed and
standalone measurements are of `90b15366`; every later commit leaves `hdl/` unchanged.

The first sweep, at `79f8aa89`, failed one suite: `pp_shadow` P2 sampled `PP_NVM_STAT[4]` (`dev_busy`) right after
the restore walk and caught the map restore's blank read of record `0x60` in flight, which the new contract makes
legitimate there. P2 now waits up to 2,000 clocks for the device face to go idle, graded as its own check with a
planted control, and then asserts the original condition unchanged.

## Known limitations / out of scope

- The cold cycle on the board (#763's "checked on the board with a cold cycle"). This change is graded on the
  desk across a planted power cycle; the window memory stands in for the slot the firmware commits and copies back,
  whose commit and copy `tb/verilator/nvm_cosim` grades.
- The faces' hold measured 553 to 635 clocks at 1x1 against a zero-latency window model. DDR latency on the board
  adds to it. A map command held past the processor's 4,096-clock gather watchdog is answered ENTITY_MISBEHAVING
  and can be retried. It is never answered with a half-restored map.
- The parent's adoption of the processor's name writer (#70 lane 3) is not done. The name half of the sticky
  pending stays.
- Multi-port shapes (8x8): restoring ports in order can refuse a saved output set that claims another port's
  stream keys. The refused set keeps the reset set, or rolls back if its put-back is refused in turn. The 8x8 is
  non-shipping (DR4): its standalone synthesis grows by 71 LUT, and its post-place obligation stays open.
- The entity enable reaches the processor only after the map restore. The side port's image-window lock follows
  that requested enable, so it engages that much later (a few hundred clocks on a healthy boot).
- The CSR map window (debug) changes no record.

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
