head 2128daad26b932feeed1ef2bde8f2774e8a51a31 base dev-soft-core draft false
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

Round 3 at `2128daad`, ready for delta review. `665-s7-srp-tx` -> `dev-soft-core`, on `1d6bf555`, thirteen commits.

- **Round 2** was accepted for delta review by the ruling's option (a) (issuecomment-6765717898). `SVC_MS` stays a cited literal until #810. The switch to the budget source is on the residue checklist (#495), owned by #810.
- **Round 3** answers the round 3 ruling (issuecomment-6766550989), items 1 to 4, in one commit. That covers R813-2's F-1 MINOR, R813-2's R-1 and R-2, and R814-2's R-1 to R-3.
- **Gates at the head**, on clean clones, all rc 0:
  - `make srptx` (five runs, 0 findings each), `srptx-plants` (26 of 26 refused, 4 of 4 controls clean, 2 of 2 off-grid controls holding their case) and `srptx-mutants` (12 of 12 refused);
  - R813-2's `request_probe.py` at offsets 280 and 240 (0 findings each), and R814-1's code probe (`join-10cs`, `join-15cs` refused);
  - `make twin` (the split capture byte-identical to round 1's) and `twin-plants`;
  - every `run:` step of every job a ready pull request to `dev-soft-core` triggers, in 69 job instances. 546 steps ran, all rc 0. 86 that cannot run on this host are listed with reasons: APT resolution, source builds of tools already pinned here, hosted-only API steps, and one job whose `if:` is false. That covers the firmware self-test (4 shards), `fw_coverage.py --check`, every firmware mutant campaign, `ctrl_boundary` with and without Verilator, `behave`, elaborate, the 19 Verilator shards and the Yosys shards;
  - the full sweep in 4 shards: 65 suites passed, 0 failed, 0 timed out, 2,192,910 checks;
  - `test_builder.py --require-rv32`, S2's harness at 1x1 (1 interface) and 8x8 (2 interfaces), `make split`, `split-mutants` and `split-cdc`;
  - `git diff --check` against the merge base.
- **Item 5 (#608)** still holds only under the published test fixture, as in rounds 1 and 2. So this PR does not close #867.

## Linked Issue / roles

Relates to #867
Relates to #665

Executor: `[A757]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

`make srptx` runs the split half of the two-placement simulation with `--srptx`: `tb_split_top`, with the platform firmware on the RTL mailbox. It covers lwSRP's MRPDU, the adapter's record in the SRP transmit ring, `KL_mbx_tx`, the byte crossing, `ctl_tx_mux` and the MAC. The bench sees lwSRP's own output and timers at its boundary, through the linker's `--wrap`, so the SRP adapter is not edited. `srptx_grade.py` grades three scenarios and two off-grid controls.

| Scenario | What it runs |
|---|---|
| `wire` | the twin's stimulus to 600 s, the production composition |
| `hold` | the MAC refusing every beat for 3 s under a peer's LeaveAll every 200 ms, which fills the SRP transmit ring |
| `licence` | a peer's Listener Ready for source 0, its LeaveAll, then its withdrawal in LV (the #608 case), under the fixture below |
| `licence-16280`, `licence-16240` | the licence scenario with the peer's LeaveAll at 16,280 ms and 16,240 ms, off lwSRP's 100 ms periodic grid (`--peer-leave-all-ms`) |

| #867 item | Check | Result at the head |
|---|---|---|
| 1. MRPDUs well formed | `[WIRE]`: each 10.8.1/10.8.2 field and EndMark, at most 1,500 octets, one Message per AttributeType, no value twice, a LeaveAll on every AttributeType of its application | 1,449 + 169 + 3 x 69 MRPDUs, no finding |
| 2. the port's MAC from reset | `[SA]` | the first MRPDU at 1 ms after reset; every one from the port's MAC |
| 3. JoinTime and LeaveAll spacing | `[TIME]`, each bound widened by the approved T_svc = 20 ms (#867 item 3; the owner's ruling of 2026-11-06 on #665). The checks: no four transmit opportunities in 1.5 x JoinTime less T_svc (280 ms). A Join timer's transmit opportunity within JoinTime's range (180 to 240 ms) of the one before, widened by T_svc on each side (160 to 260 ms). That opportunity is the frame lwSRP sent at its first transmit poll after the Join timer expired. A requested transmit opportunity, sent while the Join timer was stopped, within JoinTime + T_svc (220 ms) of the last poll at which lwSRP had nothing to send. The next message after a New within 220 ms. LeaveAll within 9,780 to 15,220 ms | no finding. Every Join timer interval is 198.958 to 200.024 ms, in all five runs. Every requested opportunity left at most 1.03 ms after lwSRP's last idle poll. In `wire`, the egress after a Join or periodic tick is 1.5 to 26.3 us |
| 4. a full transmit ring | `[TX]` | the ring at 507 of 512 words; the adapter kept the refused MRPDU and sent it first; all 169 MRPDUs left in order, byte for byte |
| 5. #608 | `[608]` | under the fixture: the stop at the LeaveTime deadline the peer's LeaveAll started (21,000 ms), not one the withdrawal restarted |
| 6. the licence at the policer | `[POL]` (split leg, per bit, every talker) and `[LIC]` (licence scenario) | each LICENCE bit reaches ACTIVE, admitted and the stream gate as itself, and the CRF term reads the top bit |
| 7. planted mutants | 26 capture plants, 4 controls inside their bounds, 2 off-grid controls holding their case, and 12 code mutants, plus 2 split-leg arms | each plant and mutant refused by its own words; each control graded clean |

**Round 3: a Join timer's frame is what lwSRP did, not a time window** (`2128daad`).

| Ruling item | Change |
|---|---|
| 1. attribution by what lwSRP did | lwSRP's Join timer holds every transmit after one until it expires (`join_wait`), and its expiry only releases what it held (`mrp_mad.c:854`, `:1421`, `:1539-1540`). The bench now marks each MRPDU at lwSRP's boundary, with no edit to lwSRP or the adapter (`srptx.hpp`, `poll()`). It records whether the MRPDU was sent at lwSRP's first transmit poll after its Join timer expired. With the Join timer stopped, it also records the last poll before it that sent nothing. `srptx_grade.py` grades the Join interval only for the first kind (`join_intervals`), with no time window. A LeaveAll frame the Join timer held counts too. A frame lwSRP sent after its first poll found nothing is a requested transmit opportunity. It is graded within JoinTime + T_svc of that idle poll (`FR_NFR.md` 3.4.1, Milan v1.2 4.2.7.1.1). `measure_time`'s JoinTime figures use the same attribution |
| 2. the refusals | `join-early-past-t-svc` (159 ms) and `join-interval-late` (261 ms) are still refused by their own words, and their controls at 161 and 259 ms are clean. The 10 cs and 15 cs arms are still refused by theirs (`... 98.989` and `148.989 ms after the one before, outside JoinTime's range widened by T_svc (160 to 260 ms`). R814-1's own probe, run unchanged, still refuses `join-10cs` (15 findings) and `join-15cs` (16) |
| 3. the control | `make srptx` runs R813-2's off-grid case twice: the licence scenario with the peer's LeaveAll at 16,280 ms and at 16,240 ms. Both grade clean. `make srptx-plants` requires each to hold its case: lwSRP's answer at 16,281.044 ms (281.030 ms after the frame before) and at 16,241.044 ms (241.030 ms), each after the Join expiry at 16,200.001 ms that found nothing to send. R813-2's `request_probe.py`, run unchanged, gives 0 findings at offsets 280 and 240. The grade at `2131eff4` refuses the 16,280 ms control by F-1's words |
| 4. residue | This body's status no longer reads as stopped (R813-2 R-1, R814-2 R-1). `ATTRIBUTE_MS`'s comment says what it serves now: the periodic and LeaveAll measurement only (R813-2 R-2). The grade's two garbled phrases now read "each transmit opportunity a Join timer sends ... widened by T_svc on each side (160 to 260 ms; 10.7.4.1, 10.7.11)" and "each transmit opportunity a Join timer sent, against the one before it" (R814-2 R-2). The README's rate window reads "1.5 x JoinTime less T_svc (280 ms)" (R814-2 R-3) |

The new rule has its own plant and control:
- `requested-late` puts the MSRP frame at ms 1000's last idle poll 221 ms before it. lwSRP's state allows that there: no Join timer ran and nothing was sent. The plant is refused by `a requested transmit opportunity at ms 1000, 221.000 ms after lwSRP last had nothing to send, past JoinTime + T_svc (220 ms`.
- Its control, `requested-within`, at 219 ms, grades clean.
- Without the rule, the plant escapes.

What the attribution changes in the measurement, all inside the bounds:
- A frame sent at the first poll after a Join and a periodic expiry of one tick is now the Join timer's. It waited for the Join expiry: 1 and 2 frames in `wire`, 6 and 8 in `hold`, 1 MVRP frame in `licence`.
- A LeaveAll frame the Join timer held now counts in the JoinTime interval. So `wire` measures 116 MSRP and 111 MVRP JoinTime intervals, where round 2 measured 104 and 104.
- A time window over those LeaveAll frames would refuse six of them in `wire`. Each followed a Join expiry that found nothing to send. The bench's record is what makes counting them safe.

Every other measured figure is unchanged.

| Piece | Change, over the whole PR |
|---|---|
| `tb/verilator/milan_dp/srptx.hpp` (new) | the bench: the recorder, the link-time wrappers with each MRPDU's poll record, the scenarios and the off-grid option, the fixture and the capture |
| `tb/verilator/milan_dp/twin_split.cpp` | `--srptx` with `--ms` and `--peer-leave-all-ms`; its time base, MAC hold, drain and hooks, all inactive in the twin's own run (its capture is unchanged, byte for byte) |
| `tb/verilator/milan_dp/tb_split_top.sv` | the policer's probes |
| `tb/verilator/milan_dp/srptx_grade.py`, `srptx_plants.py`, `srptx_mutants.py` (new) | the grade, the capture plants, their controls and the off-grid check, and the code mutants |
| `tb/verilator/milan_dp/sim_split.cpp`, `split_mutants.py` | `[POL]`, with two arms |
| `tb/verilator/milan_dp/Makefile`, `twin_fw.py` | the wrappers on the split half's link; `srptx` with its off-grid controls, `srptx-plants`, `srptx-mutants`; `--replace` for a planted unit |
| `sw/firmware/ctrl/test/ctrl_configs.py`, `scripts/measure_test_evidence_readers.py` | the boundary gate's classification of the two new programs, and the mutant driver's reads |
| `tb/verilator/milan_dp/README.md`, `sw/firmware/ctrl/srp/README.md`, `docs/design/MAILBOX_SPLIT.md`, `sw/firmware/ctrl/README.md` | the check, its fixture, attribution and measurements; what the adapter still owes |

There is no RTL, firmware, lwSRP, mailbox-contract or ring change. Every existing shape's generated output is unchanged.

**The licence scenario's fixture.** `srptx.hpp` wraps `srp_mbx_init` in that scenario alone, and hands the adapter source 0 allocated at MAAP's pinned simulation range, as the deferred adapter entry would. Every finding of that scenario, and of its off-grid controls, names the fixture.

## Authoritative references

- #867, acceptance 1 to 7. Item 3: T_svc 20 ms.
- #665: the plan's section S7, and the owner's ruling of 2026-11-06, item 3, which sets the SRP/MRP bound to T_svc = 20 ms ([issuecomment-6681686082](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6681686082)).
- This PR's rulings: round 2 (issuecomment-6763709522) and its follow-up (issuecomment-6765717898), and round 3 (issuecomment-6766550989), items 1 to 4.
- IEEE 802.1Q-2018:
  - 10.7.4.1, 10.7.4.3, 10.7.6.6, 10.7.9, 10.7.11;
  - Tables 10-3, 10-4, 10-5 and 10-7;
  - 10.8.1, 10.8.2, 10.8.2.6;
  - 11.2.3.1.3; 35.2.2.1/.2.
- Milan v1.2 4.2.7.1.1 and Table 4.3 (JoinTime 200 ms, 180 to 240 ms; a point-to-point requested transmit opportunity within JoinTime; `docs/reference/FR_NFR.md` 3.4.1), 4.2.7.2.2, 5.3.7.3.
- IEEE 802.1AC-2016 11.1 (#839).
- lwSRP PR #18 (one Message per AttributeType); lwSRP `mrp_mad.c` `on_join_timer` and `mrp_transmit` at the pinned gitlink.
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

- `srptx` prints `0 finding(s)` for each of the three scenarios and both off-grid controls.
- `srptx-plants` prints `srptx plants: 26 of 26 refused; 4 of 4 controls inside their bound clean; 2 of 2 off-grid controls clean with their requested transmit opportunity`.
- `srptx-mutants` prints `srptx mutants: 12 of 12 refused`.
- `split` prints `failures: 0`, and `split-mutants` catches 26 of 26.

## Known limitations / out of scope

- **`SVC_MS` is a literal at this base**, as ruled (option (a)).
  - The value is item 3's 20 ms, with its authority cited.
  - Deriving it from the CPU budget harness's `scenario.py` waits until that source carries the 2026-11-06 bound (#810). That switch is on the residue checklist (#495).
  - Until then, the plants hold item 3's figure apart from the grade's, so the grade cannot drift from it unrefused.
- **The requested rule's bound is the last poll that found nothing to send**, because the request came after it. A request lwSRP held while it answered nothing would look like no request at the boundary. So the rule holds the path from that poll to the wire: the adapter's polling, the ring, `KL_mbx_tx` and `ctl_tx_mux`. It does not hold lwSRP's own scheduling. That rule has a capture plant and a control, and no code arm.
- **Periodic and LeaveAll frames keep their time window**, which serves the measurement only. No check reads it.
- **Item 5 in the production composition.** No split source can hold a licence until the SRP adapter re-declares a source MAAP has allocated (`sw/firmware/ctrl/plat/README.md`, Not yet done). Once that entry lands, the licence scenario's fixture is to be removed, and the check must hold without it.
- **Found, not fixed here:** the split's AAF frames carry stream_id 0, because no firmware writes the publication block's `SRC_SID`. This is latent until a split talker streams.
- **The time base.** The firmware's own instructions take no simulated time. The CPU's cost is the CPU budget harness's figure.
- **One interface**, at the shipping AX7101 shape, as the two-placement simulation runs. Two-interface identity is held by the adapter's host tests.
- Ring geometry at 32x32 (#859, #865), the firmware loop structure, and bench confirmation are out of scope (#867).

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (item 5 under the fixture only)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes (at `2128daad`, the gates above)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

