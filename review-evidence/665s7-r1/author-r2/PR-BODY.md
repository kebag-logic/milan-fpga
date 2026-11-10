[A757]

## Contents

- **[Status](#status)** — The gate tally, the open items, and the branch.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

STOPPED at the round 2 head, on one line in item 1 of the round 2 ruling. `665-s7-srp-tx` -> `dev-soft-core`, on `1d6bf555`, twelve commits.

- **Round 2** answers R814-1's two MINOR findings in two commits: F-1, the 20 ms allowance, and F-2, Join spacing graded on both sides.
- **The open line.** The ruling asks for `SVC_MS` to be derived from the one source the firmware budget uses, not written as a literal. At this base that source cannot give 20 ms:
  - `tb/verilator/ctrl_service_budget/scenario.py` holds `T_SVC_MS = 10.0`, the proposed figure, and an SRP ceiling of 18.0;
  - the hooks harness grades SRP at min(20, 18) = 18 ms;
  - the 2026-11-06 bounds reach that source only with #810.

  So `srptx_grade.py:64` holds `SVC_MS = 20`, citing #867 item 3 and the 2026-11-06 ruling. Every bound and every plant is derived from that constant or from item 3's own figure. This needs a decision (below).
- **Gates run at the head** on clean clones, all rc 0:
  - `make srptx`: three scenarios, no finding;
  - `srptx-plants`: 25 of 25 refused, and 3 of 3 controls clean;
  - `srptx-mutants`: 12 of 12 refused;
  - every `run:` step of the nine docs-workflow jobs, plus rtl-fast's `changes`, `firmware-boundary` and `firmware-verilator`. Across those twelve jobs, 120 steps ran, all rc 0, and 11 that cannot run on this host (APT resolution, hosted-only API steps, a source build of a tool already pinned) are listed with reasons. Both boundary jobs report `ctrl_boundary: PASS`;
  - `git diff --check` against the merge base.
- **Not run at this head:** the full sweep, the firmware self-test and the other firmware jobs, S2's harness, `test_builder.py`, `behave`, and the rtl and elaborate workflows. They wait for the final head, so that pass runs once. The round 2 commits change only the SRP transmit check's three scripts and two READMEs, and nothing those gates read.
- **Item 5 (#608)** still holds only under the published test fixture, as in round 1. So this PR does not close #867.

## Linked Issue / roles

Relates to #867
Relates to #665

Executor: `[A757]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

`make srptx` runs the split half of the two-placement simulation with `--srptx`: `tb_split_top`, with the platform firmware on the RTL mailbox. It covers lwSRP's MRPDU, the adapter's record in the SRP transmit ring, `KL_mbx_tx`, the byte crossing, `ctl_tx_mux` and the MAC. The bench sees lwSRP's own output and timers at its boundary, through the linker's `--wrap`, so the SRP adapter is not edited. `srptx_grade.py` grades three scenarios.

| Scenario | What it runs |
|---|---|
| `wire` | the twin's stimulus to 600 s, the production composition |
| `hold` | the MAC refusing every beat for 3 s under a peer's LeaveAll every 200 ms, which fills the SRP transmit ring |
| `licence` | a peer's Listener Ready for source 0, its LeaveAll, then its withdrawal in LV (the #608 case), under the fixture below |

| #867 item | Check | Result at the head |
|---|---|---|
| 1. MRPDUs well formed | `[WIRE]`: each 10.8.1/10.8.2 field and EndMark, at most 1,500 octets, one Message per AttributeType, no value twice, a LeaveAll on every AttributeType of its application | 1,449 + 169 + 69 MRPDUs, no finding |
| 2. the port's MAC from reset | `[SA]` | the first MRPDU at 1 ms after reset; every one from the port's MAC |
| 3. JoinTime and LeaveAll spacing | `[TIME]`, each bound widened by the approved T_svc = 20 ms (#867 item 3; the owner's ruling of 2026-11-06 on #665). A Join timer's transmit opportunity is held on both sides, within JoinTime's range (180 to 240 ms) of the one before, widened by T_svc (160 to 260 ms). The next message after a New is held within 220 ms, and LeaveAll within 9,780 to 15,220 ms | no finding. Every Join timer interval is 198.989 to 200.015 ms, in all three scenarios. The egress after a Join or periodic tick is 1.5 to 26.3 us |
| 4. a full transmit ring | `[TX]` | the ring at 507 of 512 words; the adapter kept the refused MRPDU and sent it first; all 169 MRPDUs left in order, byte for byte |
| 5. #608 | `[608]` | under the fixture: the stop at the LeaveTime deadline the peer's LeaveAll started (21,000 ms), not one the withdrawal restarted |
| 6. the licence at the policer | `[POL]` (split leg, per bit, every talker) and `[LIC]` (licence scenario) | each LICENCE bit reaches ACTIVE, admitted and the stream gate as itself, and the CRF term reads the top bit |
| 7. planted mutants | 25 capture plants, 3 controls inside their bounds, and 12 code mutants, plus 2 split-leg arms | each plant and mutant refused by its own words; each control graded clean |

**Round 2.**

| Finding | Change |
|---|---|
| F-1, the egress allowance (`0d8e89bc`) | `SVC_MS` = 20 ms, the approved T_svc, replaces min(T_svc, the MRP ceiling) = 18 ms in every `[TIME]` bound and the `[608]` window. The plant `join-late-in-t-svc` becomes `join-late-past-t-svc`: the second MSRP frame and the adapter's record of it 221 ms after the first. Its control, `join-late-within-t-svc`, sits at 219 ms and must grade clean. The plants hold item 3's 20 ms as their own figure, so a grade bound off item 3's fails one or the other. The 23-centisecond and LeaveAll mutants take their words from the grade |
| F-2, Join spacing on both sides (`2131eff4`) | `grade_time` grades the interval `measure_time` already measured, through the shared `causes` and `join_intervals`. The bound is JoinTime's range in Milan v1.2 Table 4.3, widened by T_svc on each side, as LeaveAll's is. New plants: a short Join timer (159 ms) and a long one after a LeaveAll (261 ms), each with a control 1 ms inside. New code mutants: lwSRP Join timers of 10 and 15 centiseconds. Each is refused by the new words alone and grades with no finding without the new check |

The bound is JoinTime's range, not the configured 200 ms, widened on each side. A frame delayed within T_svc shortens the interval after it: a frame 219 ms after the one before leaves the next 179.99 ms later. A bound of 180 ms, 200 ms less T_svc, would refuse that frame, which item 3 allows.

R814-1's third arm, a 17-centisecond timer, leaves at 170 ms intervals. That is inside 160 to 260 ms, so it is not refused, and the probe that ran it says so.

**Measurements.** The egress interval error per MRP timer is in the `milan_dp` README, with min, mean and max in us over 104 Join, about 520 periodic and about 40 LeaveAll intervals per participant. They are unchanged by round 2: each scenario's measured block is identical to round 1's. Frames per transmit opportunity: 1 (727 MSRP and 722 MVRP opportunities).

| Piece | Change |
|---|---|
| `tb/verilator/milan_dp/srptx.hpp` (new) | the bench: the recorder, the link-time wrappers, the three scenarios, the fixture and the capture |
| `tb/verilator/milan_dp/twin_split.cpp` | `--srptx`; its time base, MAC hold, drain and hooks, all inactive in the twin's own run (its capture is unchanged, byte for byte) |
| `tb/verilator/milan_dp/tb_split_top.sv` | the policer's probes |
| `tb/verilator/milan_dp/srptx_grade.py`, `srptx_plants.py`, `srptx_mutants.py` (new) | the grade, the capture plants and their controls, and the code mutants |
| `tb/verilator/milan_dp/sim_split.cpp`, `split_mutants.py` | `[POL]`, with two arms |
| `tb/verilator/milan_dp/Makefile`, `twin_fw.py` | the wrappers on the split half's link; `srptx`, `srptx-plants`, `srptx-mutants`; `--replace` for a planted unit |
| `sw/firmware/ctrl/test/ctrl_configs.py`, `scripts/measure_test_evidence_readers.py` | the boundary gate's classification of the two new programs, and the mutant driver's reads |
| `tb/verilator/milan_dp/README.md`, `sw/firmware/ctrl/srp/README.md`, `docs/design/MAILBOX_SPLIT.md`, `sw/firmware/ctrl/README.md` | the check, its fixture and measurements; what the adapter still owes |

There is no RTL, firmware, lwSRP, mailbox-contract or ring change. Every existing shape's generated output is unchanged.

**The licence scenario's fixture.** `srptx.hpp` wraps `srp_mbx_init` in that scenario alone, and hands the adapter source 0 allocated at MAAP's pinned simulation range, as the deferred adapter entry would. Every finding of that scenario names the fixture.

## Authoritative references

- #867, acceptance 1 to 7. Item 3: T_svc 20 ms.
- #665: the plan's section S7, and the owner's ruling of 2026-11-06, item 3, which sets the SRP/MRP bound to T_svc = 20 ms ([issuecomment-6681686082](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6681686082)).
- The round 2 ruling on this PR, items 1 and 2.
- IEEE 802.1Q-2018:
  - 10.7.4.1, 10.7.4.3, 10.7.6.6, 10.7.9, 10.7.11;
  - Tables 10-3, 10-4, 10-5 and 10-7;
  - 10.8.1, 10.8.2, 10.8.2.6;
  - 11.2.3.1.3; 35.2.2.1/.2.
- Milan v1.2 Table 4.3 (JoinTime 200 ms, 180 to 240 ms; `docs/reference/FR_NFR.md` 3.4.1), 4.2.7.2.2, 5.3.7.3.
- IEEE 802.1AC-2016 11.1 (#839).
- lwSRP PR #18 (one Message per AttributeType).
- `tb/verilator/milan_dp/README.md`, "The split build's SRP transmit path".

## How to get into the same state

```sh
git fetch origin 665-s7-srp-tx
git checkout --detach FETCH_HEAD
git submodule update --init --recursive
```

## How to validate

```sh
make -C tb/verilator/milan_dp srptx
make -C tb/verilator/milan_dp srptx-plants
make -C tb/verilator/milan_dp srptx-mutants
make -C tb/verilator/milan_dp split
make -C tb/verilator/milan_dp split-mutants
make -C tb/verilator/milan_dp twin
make -C tb/verilator/milan_dp twin-plants
```

Expected result / pass criteria: each command exits 0.

- `srptx` prints `0 finding(s)` for each of the three scenarios.
- `srptx-plants` prints `srptx plants: 25 of 25 refused; 3 of 3 controls inside their bound clean`.
- `srptx-mutants` prints `srptx mutants: 12 of 12 refused`.
- `split` prints `failures: 0`, and `split-mutants` catches 26 of 26.

## Known limitations / out of scope

- **`SVC_MS` is a literal at this base.**
  - The value is item 3's 20 ms, with its authority cited.
  - Deriving it from the CPU budget harness's `scenario.py` waits until that source carries the 2026-11-06 bound (#810).
  - Until then, the plants hold item 3's figure apart from the grade's, so the grade cannot drift from it unrefused.
- **Item 5 in the production composition.** No split source can hold a licence until the SRP adapter re-declares a source MAAP has allocated (`sw/firmware/ctrl/plat/README.md`, Not yet done). Once that entry lands, the licence scenario's fixture is to be removed, and the check must hold without it.
- **Found, not fixed here:** the split's AAF frames carry stream_id 0, because no firmware writes the publication block's `SRC_SID`. This is latent until a split talker streams.
- **The time base.** The firmware's own instructions take no simulated time. The CPU's cost is the CPU budget harness's figure.
- **One interface**, at the shipping AX7101 shape, as the two-placement simulation runs. Two-interface identity is held by the adapter's host tests.
- Ring geometry at 32x32 (#859, #865), the firmware loop structure, and bench confirmation are out of scope (#867).

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (item 5 under the fixture only)
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes (the full pass waits for the final head)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
