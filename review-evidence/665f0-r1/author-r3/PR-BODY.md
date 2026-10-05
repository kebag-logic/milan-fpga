[A542]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why, including what rounds 2 and 3 changed for each review finding.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN locally, round 3 -- `665-f0-mailbox` -> `dev`. Mailbox suite 326 checks
(134 through Wishbone, 134 + 45 AXI4-Lite handshake checks through
AXI4-Lite, 13 co-simulation), firmware host test 701 checks over seven arms,
46 of 46 RTL and 41 of 41 firmware planted defects caught plus the two lwSRP
pin refusals, the full builder bank, `scripts/ci_scope.py --selftest` and
every touched gate rc 0 at the head, which merges dev `28f9666f` (table in
the review-ready comment). The default build is unchanged: every shipped
config's gateware export compares equal with and without this branch,
against that dev.

## Linked Issue / roles

Relates to #665

Executor: `[A542]`
Internal cleared-context reviewer: `[R496]`
External reviewer: `[R497]`

## Description

Lane F0 of #665: the packet-mailbox contract between the fabric and the
bare-metal control-plane firmware (the owner decisions of 2026-10-05 on
#640), its harness, and ADP as the first slice through it, written to the
owner directive of 2026-10-05 12:14 (#665): bare metal first, lwSRP's port
layer carried by the HAL, every protocol a portable ports-and-adapters module.
Everything sits behind a default-off build switch; the shipping image is
unchanged.

| Piece | Where | What |
|---|---|---|
| Contract | `sw/mailbox/mailbox.yaml` | the only place a number is written: registers, rings, records (the TX record's SEQ for commit order), events, the ingress filter's channels and accept terms with their clauses, the host-counter range rule, byte order stated once |
| Generator | `sw/mailbox/gen_mailbox.py` | emits the SV package, the fabric skeleton `KL_mbx.sv`, the C header and the reference page; `--check`, `--crosscheck`, `--selftest`; the reference page is gate-read in `scripts/ci_scope.py` |
| Fabric | `hdl/milan/mailbox/` | `KL_mbx` (generated) with hand-written leaves: block-RAM rings, the ingress filter and token buckets, the TX merge in commit order, fabric timers, a coalescing event poster with the centisecond TICK, one interrupt; `KL_mbx_wb` and a registered-output `KL_mbx_axil` |
| SoC switch | `sw/litex/milan_soc.py` `--ctrl-mailbox` | off by default; on, the seven sources, `KL_mbx` behind `KL_mbx_wb` at `0x9010_0000`, a pinned CSR bank, one interrupt, and (through the region list) a regenerated CPU netlist; the datapath side held idle |
| HAL and port layer | `sw/firmware/ctrl/{wire,mbx,port,plat}` | three bus functions; the driver (stamps SEQ); lwSRP's `shlan_malloc/calloc/free` on a static block pool and `shlan_printf` on a bounded debug sink, at lwSRP's pinned revision; an MMIO platform for the RISC-V or a hard core |
| Event loop | `sw/firmware/ctrl/loop` | events first, bounded passes, the TICK fan-out in slices, sleep only when nothing is owed, the latency bound and its assumptions |
| ADP slice | `sw/firmware/ctrl/adp` | Milan v1.2 5.6.3 core with no mailbox include, its mailbox adapter with stated per-path and backlog bounds, fields generated from the entity model |
| Host model and tests | `sw/firmware/ctrl/{host,test}` | the fabric side modeled at transaction level; seven arms and the planted defects of `ctrl_mutants.py` |
| Mailbox suite | `tb/verilator/mbx` | the checks through both adapters, the AXI4-Lite handshake checks with a per-clock input-to-output probe, the co-simulation, the planted RTL defects of `mutants.py` |
| Docs | `docs/design/MAILBOX_SPLIT.md`, `docs/reference/MAILBOX_CONTRACT.md`, `docs/testing/CI_WORKFLOWS.md` | the design, the generated reference, the gate-read page's reader |

### Round 3: what changed per finding

| Finding | Change | Evidence |
|---|---|---|
| R497-2 F1 (MAJOR): a restart could erase an owed ENTITY_DEPARTING | the ADP core keeps owed frames apart (a flag for the owed ENTITY_AVAILABLE, a count of owed DEPARTINGs with the oldest one's index): every SHUTDOWN's DEPARTING stays owed with its SHUTDOWN index until the port takes it, oldest first, across restart, timer expiry, link change or another SHUTDOWN; a restart's ENTITY_AVAILABLE never passes an owed DEPARTING (owed, the machine in DELAY with no timer running, until the last DEPARTING has left); a poll sends one frame at most, so the per-pass bound is unchanged; the API gains no precondition | A15 (the review's case on the core's ports): advertise, saturate, disable, enable, expire the new TMR_DELAY before room returns: DEPARTING index 1, then AVAILABLE index 0, then WAITING with TMR_ADVERTISE armed 5 s, nothing owed. E4: the same case through the driver, the model's timer and the loop with a HAL that sleeps. A16: a second SHUTDOWN queues its own DEPARTING (1, then 0). A17: room back and the expiry before any poll, DEPARTING still first. Defects `available-replaces-owed-departing` (the review's defect), `available-passes-owed-departing` and `second-departing-dropped` caught by A15, A17 and A16 |
| R496-2 N1: carried centiseconds lost on a second TICK record | no source change (the carry was correct) | L8: 40 centiseconds behind a full ring, then one more posted as a second record while part of the 40 is carried: all 41 delivered. Defect `carried-ticks-overwritten` delivers 33 and is caught by L8 |
| R496-2 N2: AXI4-Lite W and AW pairing under back-to-back writes | no RTL change (the adapter was correct) | A7: four back-to-back writes to four registers, each channel offering its next beat the cycle after the last was taken, with W beside AW and W 3 clocks ahead: four B each, every register reads back its own data. Defects `axil-wready-while-issuing` and `axil-awready-while-issuing` (a beat taken on the drain cycle and lost) are caught by A7 |
| R497-2 F2 = R496-2 N3: stale defect counts | the design page and the suite index now reference `mutants.py` and `ctrl_mutants.py` instead of restating counts; the suite and firmware READMEs too | no count of either defect campaign remains on the four pages (the generator self-test's 8 and 7 arms, still exact, are its own) |
| merge dev | dev `28f9666f` merged with `--no-ff` (one findings page, no shared file) | every gate re-run at the merge head |

### Round 2: what changed per finding

| Finding | Change | Evidence |
|---|---|---|
| R496-1 F1 (BLOCKER): the CI-scope self-test red | the contract page is in `GATE_READ_DOCS` with a classification case; the CI policy page names its reader | `ci_scope.py --selftest` PASS |
| R497-1 F1, R496-1 F2: AXI4-Lite input-to-output paths; untested handshakes | every AXI output a register or a function of registers; AW, W, AR each into a one-entry slot by its own handshake; B and R held | A1 to A6 (split AW/W both orders, a read beside a write, B and R backpressure, reset mid-transfer) and A0, a per-clock probe that moves every AXI input with the clock held; 10 adapter defects, two restoring a combinational READY, all caught |
| R497-1 F5, ruling 5994730420: TX order across channels | SEQ in TX record word 1, stamped by the driver; the merge sends the earliest SEQ modulo 2^16 | ACMP, ACMP, AECP behind a stalled frame leave 1, 1, 2 on both adapters and the model; a round-robin defect fails it |
| R497-1 F3: an owed frame could sleep | polls report owed output; the loop sleeps only when nothing is handled or owed | a HAL that sleeps until the interrupt: TX saturated then drained, nothing else pending; the frame leaves and TMR_ADVERTISE is armed |
| R497-1 F4: the two-pass bound | the bound restated with assumptions (backlog, callbacks, transmit room, bus); events first; tick fan-out in slices of 16 | full event and receive rings with 30 coalesced centiseconds: events by pass 2, the response in pass 2, the receive ring by pass 14, worst pass 105 of 407 accesses; a halved event budget fails it |
| ruling 5994972330: the DEPARTING index | Figures 6-2, 6-3 and 6.2.5.2.2 cited | wire-field checks for SHUTDOWN in WAITING and DELAY, immediate and deferred, restart and wrap; the zero-on-DEPARTING reading fails them |
| R496-1 F3 to F6 | lwSRP pinned and refused otherwise; the event ring guarded and all three guards tested; an own-entity DISCOVER defect; the CPU netlist documented | pin refusals on a scratch clone; H0 to H2 and three guard defects; the walk row catches the DISCOVER defect |
| builder gate 44 | no blank line at EOF in the generated per-leaf indexes | `git diff --check` rc 0 |

ADP service latency: per path, in the pass that takes the input with
nothing else pending (measured equal to the derivation in `adp_mbx.h`):
DISCOVER 31, TMR_DELAY 39, TMR_ADVERTISE 11, GM_CHANGE 11, LINK 11 (down 9),
SHUTDOWN 29 mailbox accesses. With full legal backlogs: an event is taken by
pass 2 and an ADP record by pass 21, a pass costs at most 407 accesses, and
the response is committed within 1,221 (event) or 8,954 (ADP record)
accesses. Time is the platform's cost per access, which is not measured here.

Owed frames: a frame the transmit ring has no room for is owed, and nothing
that follows drops an owed ENTITY_DEPARTING: each keeps its SHUTDOWN's index
and leaves, oldest first, before any later ENTITY_AVAILABLE. An owed
ENTITY_AVAILABLE is dropped only by a link loss or a SHUTDOWN, which end the
run it would have announced.

Switch-on area, out of context (`xc7a100tfgg484-2`, 10 ns, `KL_mbx` behind
`KL_mbx_wb`, placed and routed, at the round-2 RTL): 2,641 LUT, 2,737 FF, 1
RAMB36 + 10 RAMB18, no DSP, WNS +0.240 ns. There is no bar yet; it is above
the #640 estimate, and the design page names the two levers (the timer bank
and the filter's per-term field registers).

## Authoritative references

- #665 (scope, lanes), its lane assignment, the owner directive of 2026-10-05 12:14 and the round-2 and round-3 assignments
- #640 owner decisions of 2026-10-05 (packet mailboxes, ingress filter, rings, doorbell and one interrupt, 32-bit accesses, no DMA, a bus adapter per host, portable C behind a small HAL, one YAML contract) and the D3 ruling (a stated, tested latency bound per response path)
- PR #668 rulings 5994730420 (TX commit order, events first) and 5994972330 (the DEPARTING index)
- #664 (the requirement change this lane does not make)
- Milan v1.2 5.6.2, 5.6.3 (5.6.3.1 to 5.6.3.5.11, Tables 5.49 to 5.51)
- IEEE 1722.1-2021 6.2 (6.2.2.1 to 6.2.2.21; 6.2.2.15 with Figures 6-2 and 6-3 and 6.2.5.2.2), 8.2, 9.2, Table B.1
- IEEE 1722-2016 Annex B (MAAP); IEEE 802.1Q-2018 10.8 (MRPDU), 35.2.2 (MSRP), 11.2 (MVRP)
- AMBA AXI protocol specification (IHI0022H) A3.1.1, A3.1.2, A3.2.1
- `docs/design/MAILBOX_SPLIT.md`, `docs/reference/MAILBOX_CONTRACT.md`, `docs/testing/CI_WORKFLOWS.md`
- lwSRP `19f5796b63652eb1151906de73cb827d4980a53f`: `src/ports/alloc.h`, `src/ports/timer.h`, `src/include/shish_lan/mrp.h`, `mrp_pdu.h`

## How to get into the same state

```sh
git fetch origin
git checkout 665-f0-mailbox
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
python3 -m pip install --quiet pyyaml
python3 scripts/ci_rv32_sdk.py --destination "$HOME/br-milan-rv32/host"
# Verilator 5.050 on PATH (the repository's pinned version)
# for the lwSRP arm, lwSRP at its pinned revision:
git clone https://github.com/kebag-logic/lwSRP lwSRP
git -C lwSRP checkout 19f5796b63652eb1151906de73cb827d4980a53f
```

## How to validate

```sh
python3 scripts/ci_scope.py --selftest
python3 sw/mailbox/gen_mailbox.py --check --crosscheck
python3 sw/mailbox/gen_mailbox.py --selftest
make -C tb/verilator/mbx
make -C tb/verilator/mbx mutants
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --lwsrp lwSRP
python3 scripts/lint_rtl.py --check --self-test
python3 scripts/xvlog_gate.py --check
bash syn/yosys/run.sh --top KL_mbx --top KL_mbx_wb --top KL_mbx_axil
python3 sw/builder/test_builder.py --require-rv32
python3 docs/traceability/gen_module_matrix.py --check
git diff --check origin/dev HEAD
```

Expected result / pass criteria:

- the CI-scope self-test: `selftest: PASS`;
- the generator: `0 finding(s)` and `selftest: 0 arm(s) failed`;
- the suite: `checks: 134 failures: 0` (Wishbone), `checks: 179 failures: 0` (AXI4-Lite), `checks: 13 failures: 0` (co-simulation), `mbx mutants: 4 of 4 caught`; `make mutants`: both controls `[ok]` and `46 of 46 caught`;
- the host test: every arm `[ok]`, `mutants: 41 of 41 caught`, both `lwSRP pin` lines `[ok]`, `test_ctrl_firmware: PASS`;
- every other command exits 0.

Default build: export each shipped config with and without the branch
(`milan_soc.py <the builder's argv> --entity-gen-dir configs/generated/<cfg> --no-compile`)
and compare after removing timestamps, output paths and LiteX's comment-only
hierarchy tree: every generated file equal for each config.

## Known limitations / out of scope

- The skeleton's datapath side (ingress and egress streams, link levels, the grandmaster) is held idle under the switch; the protocol lanes connect it (F2 to F5).
- The listener's ADP discovery (Milan 5.6.4) is F3's and needs one more ADP accept term (a minor contract change).
- lwSRP has no PDU transmit hook yet; F4 adds one upstream, not in a private copy.
- Latency is stated and tested in mailbox accesses; a time figure needs the platform's cost per access, and a CPU-cycle figure on the shipping core needs the switch-on SoC in the CPU simulation.
- SEQ orders the records of one run of the firmware; the transmit rings are not host-readable, so a restart cannot resume the count.
- The two firmware-side gates are not wired into hosted CI: `scripts/ci_events.py` pins the docs job's step list and scripts, so that is a reviewed change to the CI contract. The mailbox suite runs in the Verilator sweep.
- Out of scope: F1 to F5, any shipping-image change, #664's requirement edits.

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
