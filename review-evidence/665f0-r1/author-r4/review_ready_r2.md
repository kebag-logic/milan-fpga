[A542] REVIEW READY (round 2)
Commit: `a3ea8ffe16585270911705ffabd68ca5e17fc9e0` on local branch `665-f0-mailbox` (not pushed): round-1 head `0bfef498` + 9 one-line commits + a `--no-ff` merge of dev `510fae60` (dev moved during the round; processor pin `ead80360`).

**Changed**, per the round-2 assignment (5995086086), R496-1 (5995078461), R497-1 (5994956684) and the rulings 5994730420 and 5994972330:
1. **CI scope (R496-1 F1):** `docs/reference/MAILBOX_CONTRACT.md` is in `GATE_READ_DOCS` (`scripts/ci_scope.py`) with a classification case; `docs/testing/CI_WORKFLOWS.md` names its reader, `gen_mailbox.py --check --crosscheck`. `ci_scope.py --selftest`: PASS.
2. **AXI4-Lite (R497-1 F1, R496-1 F2):** `KL_mbx_axil` now registers every AXI output. AW, W and AR each go into a one-entry slot by their own handshake, READY is the slot being empty, and B and R hold until BREADY/RREADY. New `axil_checks.hpp` cover split AW/W in both orders, a read beside a write, B and R backpressure, and a reset mid-transfer (A1 to A6). A0 is a bench probe that, on every clock of the AXI run, moves each AXI input with the clock held and requires every AXI output unchanged (IHI0022H A3.1.1, A3.2.1). There are 10 adapter mutants, including two that restore a combinational READY; all are caught.
3. **TX commit order (R497-1 F5):** TX record word 1 carries SEQ[15:0], the driver's commit count over all channels, with RSVD[31:16]. `KL_mbx_tx` scans each channel's oldest SEQ and sends the earliest modulo 2^16; equal SEQs go round-robin. Check X2 runs on both adapters and the model:
   - ACMP, ACMP, AECP committed behind a stalled ACMP frame leave 1, 1, 2;
   - other arbitration origins, the 16-bit wrap and ties are also covered.

   Round-robin, unsigned-compare and fixed-tie mutants are caught, as are model and driver mutants.
4. **Pending output (R497-1 F3):** polls report owed output, and the loop sleeps only after a pass that handled nothing and owes nothing (`ctrl_loop_step`). E0 to E3 run with a HAL that really sleeps until the interrupt:
   - TX saturated, the TMR_DELAY expiry owed, nothing else pending, TICK off: no sleep;
   - the ring drains: ENTITY_AVAILABLE leaves with TMR_ADVERTISE armed 5 s after it;
   - the advertise expiry then wakes the sleeping loop.

   The mutant `poll-owes-nothing` is caught.
5. **Latency bound (R497-1 F4):** `ctrl_loop.h` states the bound under four assumptions: A1 backlog (16 event records; per channel the ring's count of smallest filter-passing records, 42 for ADP), A2 callbacks, A3 transmit room, and A4 bus (the bound counts accesses; time is not measured). Events still come first, and the tick fan-out runs at most 16 per pass, carried. `adp_mbx.h` gives the figures: pass at most 407 accesses, an event's response within 1,221, an ADP record's within 8,954. "Microseconds on any bus" is gone. F0 to F7 fill both rings legally, with 30 centiseconds coalesced behind them:
   - events first in every pass, all 16 by pass 2;
   - the ENTITY_AVAILABLE in pass 2 (175 accesses);
   - the receive ring cleared by pass 14 (457);
   - worst pass 105;
   - no early sleep.

   The bound-breaking `events-halved` and `rx-before-events` mutants and two tick mutants are caught.
6. **DEPARTING index (ruling 5994972330):** Figures 6-2, 6-3 and 6.2.5.2.2 are cited in `adp.h`, `adp.c` and the design page. Wire-field checks A10 to A14 cover:
   - SHUTDOWN in WAITING and in DELAY;
   - immediate and deferred sends;
   - restart (first AVAILABLE 0);
   - wrap.

   The zero-on-DEPARTING mutant is caught.
7. **R496-1 F3 to F6:**
   - lwSRP pinned at `19f5796b63652eb1151906de73cb827d4980a53f`, with the fetch recipe in the README. The arm refuses another HEAD or an edited `src/`, and self-test arms prove both refusals on a scratch clone.
   - `KL_mbx_evt` gets the out-of-range EVT_TAIL guard; H0 to H2 test all three guards, each with a mutant.
   - An `own-discover-discarded` mutant is caught by the walk row.
   - The design page and evidence say that switch-on regenerates the CPU netlist (`f5f08b17...` becomes `9aee3fb3...`).
8. **EOF:** `gen_module_matrix` no longer writes a trailing blank line; the 14 per-leaf indexes are regenerated. `git diff --check` is rc 0.
9. **dev merged** with `--no-ff` (clean); `protocol-processor` checked out at `ead80360`. The reused walk proves the new pin and blob and passes 320 of 320.

Also: the S2 and S3 notes (WFI wake sources; device memory for a weakly ordered hard core); a `-Wall`-clean `KL_mbx_tx`.

**Validation** (all at `a3ea8ffe`, rc 0):
- `make -C tb/verilator/mbx` (Verilator 5.050): 134 Wishbone + 174 AXI4-Lite (134 + 40) + 13 co-simulation, 0 failures; quick 4 of 4. `mutants.py`: both controls ok, **44 of 44** caught.
- `test_ctrl_firmware.py --require-rv32 --self-test --lwsrp <lwSRP 19f5796b>`: 675 checks, by arm:
  - model 134, port 78, adp 84, walk 320, entity 45, rv32 1, lwsrp 13;
  - **37 of 37** firmware defects caught and both pin refusals ok;
  - RV32I text 11,412 B, bss 170 B; no heap symbol.
- `ci_scope.py --selftest`; `ci_events.py --check` and `--selftest`; `gen_mailbox.py --check --crosscheck` and `--selftest`.
- `test_builder.py --require-rv32`: ALL GATES PASS EXCEPT 1 NOT RUN (gate 11, the Arty route report is not on this host; as in round 1). The sw/litex SoC tests (`test_pp_boot_bus_freeze`, `test_pp_mem_bridge`, `test_cpu_memory_port_cdc`, `test_gptp_tx_timestamp`, `iob_pack_selftest`): PASS.
- RTL and code gates:
  - `lint_rtl.py --check --self-test`;
  - `xvlog_gate.py --check` and `--selftest` (0 hdl/ findings);
  - Yosys on the three tops, full and elaborate;
  - SoC and RTL source lists, bare-metal-only, shapes, wire accountability, `pp_srcs`;
  - idiom, hygiene, TODO, test-evidence, naming, port-contract and fail-fast gates;
  - `test_nvm_firmware.py --self-test`; `gen_module_matrix.py --check`.
- Docs gates: `docs_check`, em-dash against `origin/dev`, `gen_toc` (3 modes), doc paths, style, map, solution, submodule, PNG, feature status, archive, and `gen_hdl_reference` (self-test and build). `git diff --check origin/dev HEAD`.
- **Default build unchanged against dev `510fae60`:** gateware exports with dev's and the head's `milan_soc.py`, switch off, show 22 of 22 files equal for all five configs. AX7101 runs at the shipping arguments; the three Arty configs run at a 100 MHz proxy, because this LiteX checkout refuses 83.333 MHz identically on both sides. Switch on adds:
  - the 7 sources and the 2 instances;
  - region `0x90100000`, a CSR bank at `CSR_BASE + 0xf000`, IRQ 3;
  - the regenerated CPU netlist.
- **Switch-on area**, re-measured (Vivado 2026.1, OOC, xc7a100tfgg484-2, 10 ns, routed under the host lock): 2,641 LUT, 2,737 FF, 1 RAMB36 + 10 RAMB18, WNS +0.240 ns. Round 1 was 2,756 LUT; the scan replaced the modulo arbiter.

**Acceptance criteria:**
- Lane items 1 to 6 remain met, as in round 1, with the corrections above.
- Round-2 items 1 to 9 are each met, with the evidence above.

**Open risks/questions:**
- Not run: `act` and the hosted contexts. The head is not pushed, so no PR head exists for `act_ci.py --pr 668`; that, the hosted `changes`/`rtl-fast`/`verilator-suites`/`yosys-portability` verdicts, and the re-review of every lens fall after a push.
- SEQ orders the records of one firmware run: the transmit rings are not host-readable, so a restart cannot resume the count (stated in `mbx.c` and the design page).
- S1 (wiring the two firmware-side gates into hosted CI) is still a CI-contract change for its own issue.
- Time per mailbox access, and so a CPU-cycle figure, is not measured (assumption A4).
