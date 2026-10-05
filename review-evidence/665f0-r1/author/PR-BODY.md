[A542]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN locally -- `665-f0-mailbox` -> `dev`. Mailbox suite 253 checks (120 through
Wishbone, 120 through AXI4-Lite, 13 co-simulation), firmware host test 618
checks over seven arms, 30 of 30 RTL and 28 of 28 firmware planted defects
caught, every touched gate rc 0 at the head (table in the review-ready
comment). The
default build is unchanged: every shipped config's gateware export compares
equal with and without this branch.

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
| Contract | `sw/mailbox/mailbox.yaml` | the only place a number is written: registers, rings, records, events, the ingress filter's channels and accept terms with their clauses, byte order stated once |
| Generator | `sw/mailbox/gen_mailbox.py` | emits the SV package, the fabric skeleton `KL_mbx.sv`, the C header and the reference page; `--check`, `--crosscheck`, `--selftest` (a positive control and 15 planted mismatches and contract defects) |
| Fabric | `hdl/milan/mailbox/` | `KL_mbx` (generated) with hand-written leaves: block-RAM rings, the ingress filter and token buckets, the TX merge, fabric timers, a coalescing event poster with the centisecond TICK for lwSRP, one interrupt; `KL_mbx_wb` and `KL_mbx_axil` bus adapters |
| SoC switch | `sw/litex/milan_soc.py` `--ctrl-mailbox` | off by default; on, the seven sources, `KL_mbx` behind `KL_mbx_wb` at `0x9010_0000`, a pinned CSR bank and one interrupt; the datapath side held idle |
| HAL and port layer | `sw/firmware/ctrl/{wire,mbx,port,plat}` | three bus functions; the driver; lwSRP's `shlan_malloc/calloc/free` on a static block pool and `shlan_printf` on a bounded debug sink; an MMIO platform for the RISC-V or a hard core |
| Event loop | `sw/firmware/ctrl/loop` | one loop, bounded passes, the TICK count fanned out to centisecond consumers such as lwSRP's `shlan_timer_tick` |
| ADP slice | `sw/firmware/ctrl/adp` | Milan v1.2 5.6.3 core with no mailbox include, its mailbox adapter with a stated latency bound per response path, fields generated from the entity model |
| Host model and tests | `sw/firmware/ctrl/{host,test}` | the fabric side modeled at transaction level; the arms below |
| Mailbox suite | `tb/verilator/mbx` | the checks through both adapters, the co-simulation, 30 planted RTL defects (four in the default `make`) |
| Docs | `docs/design/MAILBOX_SPLIT.md`, `docs/reference/MAILBOX_CONTRACT.md` | the design and the generated reference |

How the evidence is tied together:

- The mailbox suite's checks (`suite.hpp`) are written once and run on the
  RTL through each adapter AND on the host model, so the model the firmware
  tests rely on answers to the RTL's expectations.
- The co-simulation runs the firmware on the RTL (every HAL access a Wishbone
  transaction) and on the model through one 21 s scenario: the same five
  frames at the same NOW_MS.
- The processor's ADP suite is reused, not rewritten: its entity constants,
  `model_frame` builder and Table 5.51 transcription are cut from the pinned
  `protocol-processor/tb/adp_engine/sim_main.cpp` at build time (pin, checkout
  and blob proved first) and walk the firmware through the model: 36 cells,
  320 checks.
- lwSRP's own MRP core (referenced at a checkout, not vendored) runs on the
  port layer: `mvrp_app_create` on the static pool, a JoinIn through the SRP
  channel, the leavetimer expiring on fabric TICKs at 60 centiseconds.
- Each ADPDU field is compared, for every shipped config, with what the
  fabric is programmed with (`boot_policy`) and compiled with (the builder's
  ADP shape include, `pp_adp_pkg::ADP_ENTITY_CAPS_C`).

ADP service-latency bounds (mailbox accesses in the pass that takes the
input, measured equal to the derivation in `adp_mbx.h`): DISCOVER 31,
TMR_DELAY 39, TMR_ADVERTISE 11, GM_CHANGE 11, LINK 11 (down 9), SHUTDOWN 29;
the response is committed within two passes of the input.

Switch-on area, out of context (`xc7a100tfgg484-2`, 10 ns, `KL_mbx` behind
`KL_mbx_wb`, placed and routed): 2,756 LUT, 2,713 FF, 1 RAMB36 + 10 RAMB18, no
DSP, WNS +0.311 ns. There is no bar yet; it is above the #640 estimate, and the
design page names the two levers (the timer bank and the filter's per-term
field registers).

## Authoritative references

- #665 (scope, lanes), its lane assignment and the owner directive of 2026-10-05 12:14
- #640 owner decisions of 2026-10-05 (packet mailboxes, ingress filter, rings, doorbell and one interrupt, 32-bit accesses, no DMA, a bus adapter per host, portable C behind a small HAL, one YAML contract) and the D3 ruling (a stated, tested latency bound per response path)
- #664 (the requirement change this lane does not make)
- Milan v1.2 5.6.2, 5.6.3 (5.6.3.1 to 5.6.3.5.11, Tables 5.49 to 5.51)
- IEEE 1722.1-2021 6.2 (6.2.2.1 to 6.2.2.21; 6.2.2.15), 8.2, 9.2, Table B.1
- IEEE 1722-2016 Annex B (MAAP); IEEE 802.1Q-2018 10.8 (MRPDU), 35.2.2 (MSRP), 11.2 (MVRP)
- `docs/design/MAILBOX_SPLIT.md`, `docs/reference/MAILBOX_CONTRACT.md`
- lwSRP `src/ports/alloc.h`, `src/ports/timer.h`, `src/include/shish_lan/mrp.h`, `mrp_pdu.h`

## How to get into the same state

```sh
git fetch origin
git checkout 665-f0-mailbox
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
python3 -m pip install --quiet pyyaml
python3 scripts/ci_rv32_sdk.py --destination "$HOME/br-milan-rv32/host"
# Verilator 5.050 on PATH (the repository's pinned version)
# optional, for the lwSRP arm: a checkout of https://github.com/kebag-logic/lwSRP
```

## How to validate

```sh
python3 sw/mailbox/gen_mailbox.py --check --crosscheck
python3 sw/mailbox/gen_mailbox.py --selftest
make -C tb/verilator/mbx
make -C tb/verilator/mbx mutants
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --lwsrp <lwSRP checkout>
python3 scripts/lint_rtl.py --check --self-test
python3 scripts/xvlog_gate.py --check
bash syn/yosys/run.sh --top KL_mbx --top KL_mbx_wb --top KL_mbx_axil
python3 sw/builder/test_builder.py --require-rv32
python3 docs/traceability/gen_module_matrix.py --check
```

Expected result / pass criteria:

- the generator: `0 finding(s)` and `selftest: 0 arm(s) failed`;
- the suite: `checks: 120 failures: 0` twice, `checks: 13 failures: 0`, `mbx mutants: 4 of 4 caught`; `make mutants`: both controls `[ok]` and `30 of 30 caught`;
- the host test: every arm `[ok]`, `mutants: 28 of 28 caught`, `test_ctrl_firmware: PASS`;
- every other command exits 0.

Default build: export each shipped config with and without the branch
(`milan_soc.py <the builder's argv> --entity-gen-dir configs/generated/<cfg> --no-compile`)
and compare after removing timestamps, output paths and LiteX's comment-only
hierarchy tree: 22 of 22 files equal for each config.

## Known limitations / out of scope

- The skeleton's datapath side (ingress and egress streams, link levels, the grandmaster) is held idle under the switch; the protocol lanes connect it (F2 to F5).
- The listener's ADP discovery (Milan 5.6.4) is F3's and needs one more ADP accept term (a minor contract change).
- lwSRP has no PDU transmit hook yet; F4 adds one upstream, not in a private copy.
- Latency is stated and tested in mailbox accesses; a CPU-cycle figure on the shipping core needs the switch-on SoC in the CPU simulation.
- The two new gates are not wired into hosted CI: `scripts/ci_events.py` pins the docs job's step list and scripts, so that is a reviewed change to the CI contract. The mailbox suite runs in the Verilator sweep.
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
