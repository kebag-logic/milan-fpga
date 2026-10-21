[A659]

## Contents

- **[Status](#status)** — Ready for review; branch `632-sinfo-notify-stored` -> `main`, three commits on `08023123`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, consumer, executor and reviewers.
- **[Description](#description)** — The SET_STREAM_INFO change gate, the ruled form, and what each commit changes.
- **[New checks](#new-checks)** — Section NS of `tb/pp_top` and its two planted defects.
- **[Authoritative references](#authoritative-references)** — Requirements and specification clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout commands.
- **[How to validate](#how-to-validate)** — Exact commands and the results measured.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — The factory-row residue and the follow-up.
- **[Definition of Done](#definition-of-done)** — The merge bar.

## Status

Ready for review. `632-sinfo-notify-stored` -> `main`, three commits on processor main `08023123`:

| Commit | Subject |
|---|---|
| `175a5a15` | Compare SET_STREAM_INFO's offset with the stored row once a controller set it and with the integrator's factory word before, so the push follows the offset as set (milan-fpga #632) |
| `0b097464` | Re-record tb/aecp_cmds' decode sweep against the ROM with SET_STREAM_INFO's stored-row compare |
| `51f88c7e` | Measure D3S5's SET_STREAM_INFO latency on a row already set, the arm its timed SET takes, since E_SINFO's two arms reach the store a cycle apart |

The form is option (b) of the ruling on milan-fpga PR #770 (issuecomment-6312625146). Every gate this change
touches passes at `51f88c7e` (below).

## Linked Issue / roles

Relates to kebag-logic/milan-fpga#632

Consumed by milan-fpga's fourth processor pin adoption: milan-fpga's `milan_dp` `[NOTIFY]` SET_STREAM_INFO case
(the timed leg) passes only with this gate, so milan-fpga PR #770 merges after a pin that carries it.

Executor: `[A659]`
Reviewers: assigned by the manager.

## Description

SET_STREAM_INFO (E_SINFO) decides whether to notify the other registered controllers by comparing the commanded
presentation time offset with the offset in force. On `main` that value is GATHER_EXT GSI(3), the integrator's
GET_STREAM_INFO word. Since milan-fpga #632 the integrator answers that word with the offset as applied, rounded up
to whole media clock periods (IEEE 1722-2016 10.7 Equation (14)), as Milan v1.2 5.4.2.10.2 asks ("the presentation
time offset currently used by the talker"). The command sets the offset as set (5.4.2.9), and 5.4.5.2 notifies only
for a command that "modifies the state". So on `main`:

- a repeated identical SET of an offset that is not whole periods notifies (2,010,000 ns against 2,020,834);
- a SET that writes back the applied value changes the stored offset and notifies nobody.

**The change (`175a5a15`, `hdl/aecp/ucode/gen_ucode.py:2434-2466`).** E_SINFO compares with the stored SEL_PTOFF row
once a controller or a restore has set it (`READ_ST RGN_DYNV + SEL_PTOFF`, COMPARE, BR_STATUS), and with the
integrator's GSI(3) word while the row is still unset. This is the store's own idiom, as E_SCFG uses for #178. The
store reads a row nothing has written as 0 with its valid bit clear, while the offset in force is the integrator's
factory value. So reading the stored row on every row (option (a), one word) pushes for a SET of the factory value
and misses a SET of 0, which moves the offset in force from 2 ms to 0 (5.4.5.2; IEEE 1722.1-2021 7.5.2). The program
grows by five words (1856..1873 of its 32-word slot); the ROM differs from `main`'s at words 1859..1873 alone. Three
asserts pin the two branch targets and the END. The word `READ_ST rd=6, RGN_DYN + SEL_PTOFF  # the offset stored` is
the anchor of milan-fpga's own planted control (`tb/verilator/milan_dp/gsi_mutants.py` mutant 9).

**The face model (`tb/pp_top/sim_main.cpp:1286-1299`, `:2018-2021`).** Every existing section's face serves a set
row's GSI(3) as set (the settings fold), so the applied and the set value never differ there and the defect cannot
be seen. `gsi_ptoff_applied`, on in section NS alone, answers as milan-fpga's integrator does: the row rounded up to
whole 48 kHz periods once set, the factory 2,000,000 ns (whole periods) before.

**Docs.** `docs/architecture/06_aecp_engine.md:522` (the chain names the compare and its residue),
`docs/architecture/09_verification.md:184` (NS on both arms of the presentation offset's A/B row) and `:318` (the
evidence table), `tb/pp_top/README.md:2484` (the `--notify-only` run list), `:2661-2698` (section NS) and the
mutation record (`:2997-3003`, `:3029-3036`).

**`0b097464`.** `tb/aecp_cmds/decode.json` records the ROM digest its sweep ran on; `make -C tb/aecp_cmds record`
re-recorded it. The sweep's decode is unchanged; the digest line alone moves (`a7b1af66...` -> `1f78804e...`).

**`51f88c7e` (`tb/pp_top/d3_phases.hpp:640-682`, `tb/pp_top/README.md:69-73`).** D3S5 places an NVM WRITE's done on
the store's accepting cycle of a SET_STREAM_INFO, using the latency of an earlier SET to the same row. That earlier
SET ran on a row never set (the GSI(3) arm), the timed one on a set row (the stored arm), which reaches the store a
cycle later, so the premise failed by one cycle ("the change accepted at 315227, the WRITE's done at 315228"). The row
is now set first and the latency measured on the arm the timed SET takes; the premise is graded as before. The D3
control it grades (`clear_wins_same_edge`) and the other eleven D3 controls graded by section S fail exactly their
recorded checks.

## New checks

Section NS (`tb/pp_top/notify_phases.hpp:1131-1201`), under `--notify-only`, on its own model, the requester A and
a second controller B registered; every SET from A answers SUCCESS byte-exact:

| Step | SET_STREAM_INFO from A | Expected |
|---|---|---|
| NS0b | (premise) | no row set; GET reads 2,000,000 ns on both outputs |
| NS1 | output 1, 2,000,000 ns, the factory value, row never set | nothing to B or A |
| NS2 | output 0, 0 ns, row never set | one push to B, byte-exact, carrying 0; none to A |
| NS3 | output 0, 2,010,000 ns, a change | one push; NS3b: GET reads 2,020,834 ns, not the value set (premise) |
| NS4 | output 0, 2,010,000 ns again | nothing to B or A |
| NS5 | output 0, 2,020,834 ns, the value GET read | one push |

Planted defects (`tb/pp_top/notify_mutants.py:228-243`), each required to fail its named checks:

| Mutant | Planted | Failing words |
|---|---|---|
| `stream_info_compare_applied` | the set arm's stored read back to `GATHER_EXT GSI(3)`, the compare on `main` | "NS4 SET_STREAM_INFO(output 0, 2,010,000 ns) again: an unchanged offset pushes nothing (Milan 5.4.5.2), got 1 at the other controller"; "NS5 SET_STREAM_INFO(output 0, 2,020,834 ns), the value GET read, a change: exactly one unsolicited response of this command at the other registered controller, got 0" |
| `stream_info_unset_arm_dropped` | the never-set arm's branch a NOP, so every row reads the store (option (a)) | "NS1 SET_STREAM_INFO(output 1, 2,000,000 ns), the factory offset, on a row never set: an unchanged offset pushes nothing (Milan 5.4.5.2), got 1 at the other controller"; "NS2 SET_STREAM_INFO(output 0, 0 ns) on a row never set: exactly one unsolicited response of this command at the other registered controller, got 0" |

NS's pushes also move four existing records, each re-measured: `enq_dropped_stream_info` and `stream_info_get_body`
now fail NS2, NS3 and NS5 beside NP3, `requester_not_excluded` 15 checks (was 12), `entry_seq_not_advanced` 15
(was 13). The campaign holds 137 controls.

## Authoritative references

- Milan v1.2 5.4.2.9 (SET_STREAM_INFO sets the offset; the response echoes the commanded value), 5.4.2.10.2
  (GET_STREAM_INFO reads the offset in use), 5.4.5.1 and 5.4.5.2 (a notification follows a command that modifies
  the state, and carries the response's content).
- IEEE 1722.1-2021 7.4.15, 7.5.2; IEEE 1722-2016 10.7 Equation (14) (the integrator's rounding).
- milan-fpga #632; milan-fpga PR #770: R677-2-F1 and the round 3 ruling (issuecomment-6312625146).

## How to get into the same state

From a checkout of this repository:

```sh
git fetch origin 632-sinfo-notify-stored
git switch 632-sinfo-notify-stored
```

Verilator 5.050, as the workflow pins.

## How to validate

```sh
make check
./scripts/lint_hdl.sh
REQ_TAG_LOG=req-tags.txt ./scripts/run_suites.sh > suites.txt
python3 scripts/check-req-tags.py --suites suites.txt --evidence req-tags.txt
python3 tb/pp_top/d3_mutants.py --output d3-mutants --jobs 1 --only latch_ignores_program taint_ignored clear_wins_same_edge clear_by_group clear_by_index identify_is_a_change unchanged_compare_ignores_validity no_backoff_d3 fourth_attempt alarm_forgiven_by_success backoff_derivation backoff_holds_dispatch
python3 -B tb/aecp_cmds/mutants.py --output aecp-cmds-mutants --jobs 1
(cd tb/pp_top && python3 aecp_dispatch_mutants.py --output ../../aecp-dispatch-mutants --jobs 1)
(cd tb/pp_top && python3 aecp_mutants.py --output ../../aecp-mutants --jobs 1)
python3 tb/pp_top/notify_mutants.py --output notify-mutants --jobs 1 --only enq_dropped_configuration enq_dropped_stream_info class_4_mapped_to_rate class_9_mapped_to_control requester_not_excluded entry_seq_not_advanced stream_info_get_body stream_info_compare_applied stream_info_unset_arm_dropped configuration_compare_whole_lane configuration_unchanged_notifies configuration_running_route_dropped configuration_success_reserved_dirty configuration_refusal_notifies counter_limit_500ms fan_out_skips_row_0 refresh_resets_seq foreign_unlock_allowed lock_taker_notified deregister_keeps_row registry_holds_15 set_control_ignores_lock
```

Measured at `51f88c7e`, Verilator 5.050, each in a clean clone at the commit, at most two builds at once:

| Gate | Result |
|---|---|
| `make check` | rc 0; the AECP command gate's selftest 231 of 231, 31 commands; 231 requirement tags |
| `./scripts/lint_hdl.sh` | rc 0 |
| `./scripts/run_suites.sh` | rc 0: every suite passes, 1,030,329 checks, 0 failing; `pp_top` 10,741 over its seven builds (NS 20, NP 53 in `--notify-only`), `ucpu` 447, `aecp_cmds` 176 |
| `check-req-tags.py --suites --evidence` | rc 0: 231 evidence lines, 14 suites |
| `notify_mutants.py`, the 22 `--notify-only` controls | goldens PASS, 22 of 22 KILLED by their named checks |
| `d3_mutants.py`, the 12 controls graded by section S | goldens PASS, 12 of 12 KILLED, each failing exactly its recorded count |
| `tb/aecp_cmds/mutants.py` | 17 of 17 detected by their named failures; golden and restored PASS |
| `aecp_dispatch_mutants.py` | four controls PASS, 69 of 69 KILLED |
| `aecp_mutants.py` | six controls PASS, 61 of 61 KILLED |

The consumer, measured in milan-fpga at PR #770's head with this head's E_SINFO block applied uncommitted to its
processor submodule (pin `2cbed0a9`; the ROM is byte-identical to the one measured for option (b) in round 3): the
timed notify leg 441 checks, 0 failures, pushes 0, 1, 0, 1 over the four steps; its planted control (`gsi_mutants.py
9`) caught at step 3; a SET of 0 on the CRF output's never-set row pushes once.

## Known limitations / out of scope

- **The factory-row residue.** Before a row's first SET, the compare reads the integrator's GSI(3) word, which is the
  offset as applied. A factory row that is not a whole number of media clock periods therefore compares with its
  applied value, so a SET of exactly that factory value would push although the offset as set did not change. No
  configuration milan-fpga ships has such a row: every factory row is 2 ms, whole periods. Recorded by the ruling;
  not a finding.
- **An applied offset that changes without a SET** (a media clock rate change under the same row) changes what
  GET_STREAM_INFO reads with no SET behind it: IEEE 1722.1-2021 7.5.2's normal-operation case. Recorded as a
  follow-up on milan-fpga #632, not implemented here.
- Pushing the branch, the pin adoption in milan-fpga, and the candidate merge are the merge turn's.

## Definition of Done

- [x] The form is ruled (option (b), issuecomment-6312625146)
- [x] E_SINFO change, processor-level test (section NS), planted defects (`stream_info_compare_applied`, `stream_info_unset_arm_dropped`)
- [x] The repository's ucode generator and the gates the change touches pass
- [ ] Reviews positive
- [ ] Merged to `main`, then adopted by milan-fpga's pin

