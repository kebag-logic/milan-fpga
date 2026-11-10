[A757]

## Contents

- **[Status](#status)** — The gate tally, the open item, and the branch.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN at the head, with one acceptance item open. `665-s7-srp-tx` -> `dev-soft-core`, on `1d6bf555`, ten commits.

- Every `run:` step of the four workflows a pull request to `dev-soft-core` triggers passes natively on clean clones of the head: 546 ran, all rc 0, and 86 cannot run on this host (APT resolution, source builds of tools already pinned here, GitHub API steps), each with its reason. The firmware boundary gate is included, with the LiteX tree's venv.
- The full sweep passes as four shards: 65 suites, 2,192,910 checks, 0 failures.
- `make srptx` grades three scenarios with no finding. `srptx-plants` refuses 23 of 23, and `srptx-mutants` 10 of 10.
- `make split` passes, and `split-mutants` catches 26 of 26. `make twin` and `twin-plants` pass, and the twin's split capture is byte-identical to the base's.

Item 5 (#608) holds only under a published test fixture, so this PR does not close #867. In the production composition no split talker can hold a licence until the SRP adapter takes MAAP's allocation. #665 defers that until the adapter's transmit rework lands.

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
| 3. JoinTime and LeaveAll spacing | `[TIME]`, each bound widened by min(T_svc, the MRP ceiling) = 18 ms, the owner's per-family rule | no finding; the egress after a Join or periodic tick is 1.5 to 26.3 us |
| 4. a full transmit ring | `[TX]` | the ring at 507 of 512 words; the adapter kept the refused MRPDU and sent it first; all 169 MRPDUs left in order, byte for byte |
| 5. #608 | `[608]` | under the fixture: the stop at the LeaveTime deadline the peer's LeaveAll started (21,000 ms), not one the withdrawal restarted |
| 6. the licence at the policer | `[POL]` (split leg, per bit, every talker) and `[LIC]` (licence scenario) | each LICENCE bit reaches ACTIVE, admitted and the stream gate as itself, and the CRF term reads the top bit |
| 7. planted mutants | 23 capture plants and 10 code mutants, plus 2 split-leg arms | each refused by its own words |

**Measurements.** The egress interval error per MRP timer is in the `milan_dp` README, with min, mean and max in us over 104 Join, about 520 periodic and about 40 LeaveAll intervals per participant. Frames per transmit opportunity: 1 (727 MSRP and 722 MVRP opportunities).

| Piece | Change |
|---|---|
| `tb/verilator/milan_dp/srptx.hpp` (new) | the bench: the recorder, the link-time wrappers, the three scenarios, the fixture and the capture |
| `tb/verilator/milan_dp/twin_split.cpp` | `--srptx`; its time base, MAC hold, drain and hooks, all inactive in the twin's own run (its capture is unchanged, byte for byte) |
| `tb/verilator/milan_dp/tb_split_top.sv` | the policer's probes |
| `tb/verilator/milan_dp/srptx_grade.py`, `srptx_plants.py`, `srptx_mutants.py` (new) | the grade, the capture plants and the code mutants |
| `tb/verilator/milan_dp/sim_split.cpp`, `split_mutants.py` | `[POL]`, with two arms |
| `tb/verilator/milan_dp/Makefile`, `twin_fw.py` | the wrappers on the split half's link; `srptx`, `srptx-plants`, `srptx-mutants`; `--replace` for a planted unit |
| `sw/firmware/ctrl/test/ctrl_configs.py` | the boundary gate's classification of the two new programs |
| `tb/verilator/milan_dp/README.md`, `sw/firmware/ctrl/srp/README.md`, `docs/design/MAILBOX_SPLIT.md` | the check, its fixture and measurements; what the adapter still owes |

There is no RTL, firmware, lwSRP, mailbox-contract or ring change. Every existing shape's generated output is unchanged.

**The licence scenario's fixture.** `srptx.hpp` wraps `srp_mbx_init` in that scenario alone, and hands the adapter source 0 allocated at MAAP's pinned simulation range, as the deferred adapter entry would. Every finding of that scenario names the fixture.

## Authoritative references

- #867, acceptance 1 to 7; #665, the plan's section S7, and the owner's approval of T_svc = 20 ms graded per family (2026-10-29)
- IEEE 802.1Q-2018 10.7.4.1, 10.7.4.3, 10.7.6.6, 10.7.9, 10.7.11, Tables 10-3, 10-4, 10-5 and 10-7; 10.8.1, 10.8.2, 10.8.2.6; 11.2.3.1.3; 35.2.2.1/.2
- Milan v1.2 Table 4.3, 4.2.7.2.2, 5.3.7.3
- IEEE 802.1AC-2016 11.1 (#839)
- lwSRP PR #18 (one Message per AttributeType)
- `tb/verilator/milan_dp/README.md`, "The split build's SRP transmit path"

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

Expected result / pass criteria: each exits 0. `srptx` prints `0 finding(s)` for each of the three scenarios. `srptx-plants` prints `srptx plants: 23 of 23 refused`. `srptx-mutants` prints `srptx mutants: 10 of 10 refused`. `split` prints `failures: 0`, and `split-mutants` catches 26 of 26.

## Known limitations / out of scope

- **Item 5 in the production composition.** No split source can hold a licence until the SRP adapter re-declares a source MAAP has allocated (`sw/firmware/ctrl/plat/README.md`, Not yet done). Once that entry lands, the licence scenario's fixture is to be removed, and the check must hold without it.
- **Found, not fixed here:** the split's AAF frames carry stream_id 0, because no firmware writes the publication block's `SRC_SID`. This is latent until a split talker streams.
- **The time base.** The firmware's own instructions take no simulated time. The CPU's cost is the CPU budget harness's figure.
- **One interface**, at the shipping AX7101 shape, as the two-placement simulation runs. Two-interface identity is held by the adapter's host tests.
- Ring geometry at 32x32 (#859, #865), the firmware loop structure, and bench confirmation are out of scope (#867).

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (item 5 under the fixture only)
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
