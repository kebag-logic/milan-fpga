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

GREEN at `8000520c`: the full Verilator sweep 63 of 63 suites, 2,187,192 checks, 0 failures; the dynmap leg 589/0, `maprec8` 219/0, `maprec4` 137/0; 60 of 60 planted controls caught with every clean leg passing; both reviews' probes rerun, every R669 probe and both R670 controls caught; every docs and rtl-fast step runnable here rc 0 (the two firmware-boundary steps under a different interpreter, below); route-1x1, ooc-1x1, ooc-8x8 and the full Yosys run rc 0. Board cold cycle not done. `637-map-records` -> `dev`.

## Linked Issue / roles

Relates to #637 (the on-board cold power cycle is not run in this lane; every other acceptance item is met)
Relates to #763, #70

Executor: `[A656]`
Internal cleared-context reviewer: `[R669]` (round 1, NEGATIVE at `63a187e1`); round 2 to be assigned
External reviewer: `[R670]` (round 1, NEGATIVE at `63a187e1`); round 2 to be assigned

## Description

The parent writes and restores the channel-map records `0x60` (STREAM_PORT_INPUT) and `0x70`
(STREAM_PORT_OUTPUT). The processor ruled the channel maps the integrator's (its issue 83; D3 section 15 item 2,
amended). The shipping image restored no map after a power cycle (#763). The record format is unchanged.

| Piece | File | What |
|---|---|---|
| Device-face arbiter | `hdl/milan/KL_pp_shadow.sv` | The backend's one device face is shared between the processor's NVM port and the parent's map writer. A side keeps the face while it asks, a command stays with its side until done or err, an abandoned read is drained, and an abandoned write is never padded. |
| Pending and alarm | `hdl/milan/KL_pp_shadow.sv` | `pend_i` takes the map writer's dirty bits, and the sticky source keeps names only. The map alarm joins `nvm_alarm` (PP_STAT `[4]`). |
| Writer | `hdl/milan/milan_datapath.sv` (`amr_*`) | One dirty bit per dynamic port and direction, set by the actual phase-5 change. A 500 ms first-dirty window, a one-clock latch with no edit transaction open, then taint and clear at the untainted WRITE's done. DR2c: three attempts 500 ms apart, then the reset-sticky alarm. |
| Record | same | F07.8 framing, crc16 CCITT-FALSE, the port's mappings in GET_AUDIO_MAP order, then UNUSED entries (eight `0xFF` bytes) to the capacity of FASTCONNECT 4.2. The empty list is a framed record of UNUSED entries (D3 8.3, V3g), never an erased span. |
| Restore | same | Runs only after the D3 walk's COMPLETE terminal, as one transaction over the map records in one read pass, in three stages through the existing ADD/REMOVE transaction server. Stage 0 REMOVEs every dynamic port's reset set. Stage 1 reads each record once and ADDs a well-formed set, judged by the ADD rule. An erased or unframed record, a framed one failing its layout, id, crc16, padding or ranges, and a refused set mark the port. Stage 2 ADDs every marked port's reset set back. So a channel moved between ports comes back whatever the port order. |
| Roll-back | same | A device error, a short read, the 20 ms per-wait or 1,000 ms aggregate deadline, or a refused take-down or put-back rolls every map back to its reset set. `restore_rb_o` or a D3 abort leaves the reset sets in place. |
| Holds | same | Until the map restore ends, the edit face, the CSR map writer, GET_AUDIO_MAP, the format judge and the entity enable wait. |
| Status | same, `pp_stat_*_w` | PP_STAT's busy, done, fail and blank are composed with the map restore's: busy covers it, done waits for its end, fail adds its roll-back, and blank needs it to have read no framed, crc-clean record and failed nowhere. The processor's interface is unchanged. |
| Gate | `scripts/check_nvm_record_space.py` check 15 | The parent's layout literal is held to the donor's `LAYOUT_VER_P`, with a negative control. |
| Evidence | `tb/verilator/milan_dp`: the dynmap leg's `[MAPREC]` section, and the `maprec8` and `maprec4` legs | A planted power cycle keeps the window memory across a reset, and the repository's codec frames every expected record. The multi-port legs move channels between the 8x8's output ports and save and restore the 4x4's input ports. `dynmap_mutants.py` holds the planted controls. |
| Harness | `tb/verilator/pp_shadow` P2; `sim_nxn.cpp` boot walk | P2 waits, within a bound, for the map restore's blank reads before grading the idle device face. The boot walk's poll holds the TX trunk, so an AECP answer the release sends while PP_STAT done still waits for the map restore is kept whole. |
| Docs | the saved-state pages, REGISTER_MAP, TESTING, READMEs | The ownership, the amended one-pass transaction (D3 3 rule 7, 18.4), PP_STAT's composed bits and the new legs. |

### Round 2 (answers R669-1 and R670-1)

Both reviews were NEGATIVE at `63a187e1`. The round-2 assignment (PR #768 comment 6269988820) ruled two design
questions: the one-pass restore is accepted for the map records, and cross-port ownership must be fixed, not
documented. Dev `e26f1816` is merged in (merge commit `8a7e6beb`; #763's change is `sw/firmware/ctrl` only).

| Finding | Answer | Where |
|---|---|---|
| R670-F1, R669-F1 (MAJOR), R669-S2: PP_STAT ignored the map restore | PP_STAT `[1]`, `[2]`, `[3]`, `[7]` are composed with it: busy covers it, done waits for its end, fail adds its roll-back, blank needs it to have read no framed, crc-clean record. Graded by public-register assertions after a blank boot, saved and empty lists, both device-error cases, both deadlines and a refused put-back, and inside a running map restore, each with a planted control (campaign rows 38 to 44 and 56) | `milan_datapath.sv` `pp_stat_*_w`; `[MAPREC]` |
| R670-F2 (MAJOR), R669-F5: another port's reset set refused a legal saved output map | The restore takes every reset set down first (stage 0), applies the saved sets (stage 1), and puts back the refused or absent ports' reset sets last (stage 2). The new `maprec8` leg moves channels between the 8x8's output ports in both port orders and around a cycle, saved by the writer and restored, graded on GET_AUDIO_MAP, every key's owner and cluster, and the capture RAM. The round-1 ordering planted back is caught (row 54) | `amr_fsm` AS_RNEXT, AS_RJDG, AS_EEND |
| R670-F3 (MAJOR), R669-F2: six restore arms had no killing control | Committed checks on the real restore path for the put-back, holes, layout, id, ranges and conflicting keys (each in both directions where the direction has the field), a D3 pass-0 abort, the legal maximum, conflicting keys across ports, and the first and last ports (`maprec4`: the 4x4's input ports). Each arm's planted control is caught (rows 45 to 53, 57 to 60) | `[MAPREC]` value arms, `maprec8`, `maprec4` |
| R670-F4, R669-F3/F4 (MAJOR): three required docs gates failed | `mrec_offset_i`'s literal now carries its rationale on the line: every command is a whole-record READ or WRITE from byte 0. The `[MAPREC]` code is split into functions under 100 lines with single declarators, and the alarm check no longer spells `alarm (`. No ratchet moved. Every docs-workflow step was run at the head (table below) | `milan_datapath.sv` port binding; `sim_nxn.cpp` |
| R670-F5, R669-F6 (MINOR): PP_STAT `[4]` omitted the map writer | The row names the parent map writer of records `0x60`/`0x70` (#637), three attempts 500 ms apart, reset-sticky | `REGISTER_MAP.md` |
| R670-F6 (MINOR): one-pass deviation unruled | Ruled accepted. D3 section 3 rule 7 carries the amendment, and 18.4 states the transaction, its map-only boundary and its validation obligation for one pass and its deadlines | `SAVED_STATE_MATERIALIZATION.md` |
| R669-R1 to R3 (= R670-R1 to R3) | "check 15"; lane labels removed from both source comments | `milan_datapath.sv`, `KL_pp_shadow.sv`, `sim_nxn.cpp` |
| R669-S1 | One sentence in 18.4: an ungranted request counts as a failed attempt; against the 50 ms capture hold this changes no outcome | 18.4 |

Round 1's account was wrong on one point: it listed "the docs gates ... all rc 0", but three required
docs-workflow steps (port contracts, C/C++ idiom, test-evidence) were never run, and all three failed. Round 2
runs every step of the docs and rtl-fast workflows it can run locally, and lists what it could not run.

The boot-walk helper in `sim_nxn.cpp` now holds the TX trunk (`tready` low) while it polls PP_STAT. Since done
waits for the map restore, the AECP answer the release sends arrived during the poll and was clocked off half-read
at 8x8 (`nxn8`'s held READ_DESCRIPTOR check); held, it reaches the caller's await whole. The check is unchanged.

**The reviews' own probes, rerun at the head.** Both reviews' probe scripts were rerun from clean clones at
`af5eefc6` (whose `hdl/` and `tb/` equal the head's). A probe whose round-1 anchor line no longer exists was
re-pointed to the head's line doing the same job, with the diff kept beside it. R670's status probe: 131 checks, 0
failures (3 at round 1). R670's two controls (hole rule off, put-back off): each fails exactly its three targeted
value and RAM checks. R669's six restore-arm probes, all of which survived at round 1: all six caught (3 to 12
failures of 589), the clean leg passing. R669's PP_STAT readout: fail is set with the map roll-back in every
roll-back, deadline and first-record-error case, and blank is 0 wherever a record validated.

**One more gate this lane broke, found and fixed in round 2.** The firmware boundary gate
(`ctrl_boundary.py --only verilator`, rtl-fast `firmware-verilator`) counts a pin control for every Makefile target
that builds against the stack. The two new legs add four (`build-`/`exec-maprec8`, `build-`/`exec-maprec4`), so the
count is 165 and `sw/firmware/ctrl/README.md` said 161. `8000520c` states 165, and the gate passes there.


## Authoritative references

- Milan v1.2 5.3.9.1 and 5.3.10.1: each Stream Port's dynamic mapping list is saved in non-volatile memory and restored after a power cycle.
- IEEE 1722.1-2021 7.4.44 (GET_AUDIO_MAP), 7.4.45 (ADD_AUDIO_MAPPINGS), 7.4.46 (REMOVE_AUDIO_MAPPINGS).
- `docs/design/SAVED_STATE_MATERIALIZATION.md` 3 (rule 7, amended), 5.2, 6.1, 7.1, 8.3, 8.4, 8.6, 8.7, 8.8, 15 item 2 (amended), 15.1 (DR2a to DR2c, DR3a, DR4), 18.4.
- `docs/design/SAVED_STATE_FASTCONNECT.md` 4.2 and 6.1; `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` 6.1, 7 (O3) and 11.
- `docs/reference/REGISTER_MAP.md` PP_STAT (`0x924`).
- The processor's `docs/architecture/07_memory_maps.md` 5.1 at pin `2cbed0a9`: the channel maps are the integrator's to save, restore and roll back. No processor file changes.
- The round-2 rulings: PR #768 comment 6269988820.

## How to get into the same state

```sh
git fetch origin
git checkout 637-map-records
git submodule update --init gptp-processor protocol-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
git rev-parse HEAD
```

The Verilator gates use Verilator 5.050, Yosys 0.66 and sv2v v0.0.12, as the hosted workflows pin them. The
Python gates use CPython 3.12.3, as the hosted runner does.

## How to validate

```sh
make -C tb/verilator/milan_dp dynmap
make -C tb/verilator/milan_dp maprec8
make -C tb/verilator/milan_dp maprec4
make -C tb/verilator/milan_dp_render tdm8render-build
make -C tb/verilator/milan_dp dynmap-mutants DYNMAP_MUTANT_JOBS=4
python3 scripts/check_port_contracts.py
python3 scripts/check_cpp_idiom.py
python3 scripts/measure_test_evidence.py --check
python3 scripts/lint_rtl.py --check --self-test
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator
suite_logs=$(mktemp -d)
scripts/run_all_suites.sh "$suite_logs"
```

Expected result / pass criteria: every command exits 0, and `dynmap-mutants` reports 65 checks, 65 PASS: five
clean legs and 60 planted controls caught. The `milan_dp_render` build comes first because the campaign's listener
leg reads that suite's generated inputs from its clean build; dev's campaign has the same precondition (below).

**Validation account (round 2).** Each command ran from a clean clone, unpiped, with one log and one rc.

| Executed | Head | Result |
|---|---|---|
| docs.yml: docs-gates-0 steps 4, 12 to 21, 23, 24, 27, 29 to 52 and 54; docs-check-no-git; wire-accountability; docs-gates-2 steps 16 and 17 (95 commands) | `8000520c` | all rc 0 |
| docs.yml: both builder legs (docs-gates-1 and -2 step 15) | `8000520c` | rc 0, rc 0 |
| rtl-fast: firmware-boundary and firmware-verilator (`ctrl_boundary.py`, both legs) | `8000520c` | rc 0, rc 0; 165 pin controls, 0 findings |
| rtl-fast: verilator-lint, bdd-conformance, yosys-elaboration, publication-census, firmware-unit and the three firmware mutation campaigns, and the `changes` job's self-test (28 commands) | `af5eefc6` | all rc 0 |
| the full Yosys run; the `dynmap-mutants` campaign and its five clean legs | `af5eefc6` | rc 0; 60 of 60 caught |
| `xvlog_gate.py --check` and `--selftest`; route-1x1, ooc-1x1, ooc-8x8 | `887b6bf2` | all rc 0 |
| the full Verilator sweep, as the runner's four shards | `8000520c` | rc 0 each; 63 of 63 suites, 2,187,192 checks, 0 failures (round 1: 2,186,578; the +614 are the dynmap leg's +258 and the two new legs' 219 and 137); the four declared `tsn_fuzz` skips |

`af5eefc6` differs from the head by one line of `sw/firmware/ctrl/README.md`, which only `ctrl_boundary.py` reads,
and both of its legs reran at the head. `887b6bf2` differs from the head in no file under `hdl`, `syn` or
`constraints`.

Skipped: the workflows' provisioning steps (installs, downloads, fetches, tool builds; the same pinned tools were
used here), the steps that read hosted job results (outcome records, the every-gate-once check, the manifest,
fail-fast and cancel-tail jobs, the changed-file classification and the `rtl-fast` aggregate), builder gate 11
(the builder declares it NOT RUN: it needs a local LiteX build tree), the act-first replica (this lane does not
push, so there is no remote head to record), the hosted exhaustive gates (they start when the PR is marked ready),
the sweep's four declared `tsn_fuzz` skips, and the on-board cold cycle.

Cancelled or superseded, none cited as a result: at `af5eefc6` both builder legs refused to start (a receipt file
from an earlier run was in their path), and both boundary legs failed, one because `migen` was absent from the
3.12.3 interpreter and one on the README's pin-control count. `8000520c` fixes the count, and all four reran and
passed at the head. Three host resets cut runs (ooc-8x8, the boundary leg without Verilator, three sweeps, the
last of them in `milan_dp`); each was rerun from the start. One sweep start aborted in the sweep's own cancellation
preflight because its launcher ignored SIGHUP. After the third reset the sweep ran as the runner's four shards
(`scripts/run_all_suites.sh "$suite_logs" --shard <i>/4`, i = 0 to 3), one after another, each a complete run with
its own log and rc, so a reset could cost only the shard it cut. Those four runs are the sweep in the table.

## Known limitations / out of scope

- The cold cycle on the board (#763's "checked on the board with a cold cycle") is not run in this lane. This change
  is graded on the desk across a planted power cycle; the window memory stands in for the slot the firmware
  commits and copies back, whose commit and copy `tb/verilator/nvm_cosim` grades.
- The faces' hold measured 598 to 672 clocks at 1x1 against a zero-latency window model. DDR latency on the board
  adds to it, against the processor's 4,096-clock gather watchdog.
- At 8x8 (non-shipping, DR4) the three stages hold the faces about 13,700 clocks, past that watchdog: a command held
  there meanwhile is answered by the watchdog and can be retried, never with a half-restored map. It stays open
  with the other 8x8 obligations of D3 18.4.
- Records that disagree with each other (two records claiming one key, or a saved set claiming the key of a port
  whose record is erased) arise only when a record write was lost. The first claimant in walk order keeps the key
  and the other port gets its reset set back, or, when that reset set cannot come back, every map rolls back
  with PP_STAT fail.
- The parent's adoption of the processor's name writer (#70 lane 3) is not done; the name half of the sticky
  pending stays.
- The entity enable reaches the processor only after the map restore, so the side port's image-window lock, which
  follows the requested enable, engages that much later (a few hundred clocks on a healthy 1x1 boot).
- The two new `milan_dp` legs add hosted time to CI pieces `milan_dp__2` and `milan_dp__3` (round-robin); the
  recorded piece durations in `scripts/suite_shards.py` are hosted measurements and are not re-measured here.
- `ci/image/tool-inventory.json` records `dynmap_mutants.py`'s hash at dev's version; no workflow gate reads it and
  round 1's change already left it behind, so it is not regenerated here.
- The CSR map window (debug) changes no record.
- The `dynmap-mutants` campaign's listener leg reads `tb/verilator/milan_dp_render`'s generated inputs from that
  suite's clean build, and the campaign target does not build it, so from a fresh clone the leg's clean run fails
  until that suite is built (the step in How to validate). Dev's campaign has the same entry and the same target
  prerequisites; this lane leaves the arrangement as it found it.
- The firmware boundary gate imports `migen` through `sw/litex/test_ctrl_memory.py`. The hosted job installs the
  LiteX pins into its interpreter; here both boundary steps ran under the LiteX environment's CPython 3.14.8, the
  other Python gates under 3.12.3, and the suite sweep under 3.14.8 (it needs `os.pidfd_open`).

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
