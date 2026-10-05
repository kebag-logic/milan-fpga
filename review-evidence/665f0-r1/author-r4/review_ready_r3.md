[A542] REVIEW READY (round 3)
Commit: `3ebd6ca30106a006c20fd2879dcad9c79bf51dca` on local branch `665-f0-mailbox` (not pushed). It is round-2 head `a3ea8ffe` plus 4 one-line commits and a `--no-ff` merge of dev `28f9666f` (one findings page from PR #666; no shared file, no submodule change).

**Changed**, per the round-3 assignment (5998250555), R497-2 (5998184135) and R496-2 (5998244827):

1. **An owed ENTITY_DEPARTING is never lost (R497-2 F1).**
   - **The change.** In `sw/firmware/ctrl/adp/adp.c` and `adp.h`, the single pending slot is replaced by two fields: `available_owed` (a flag) and `departing_owed` (a count), with `departing_index` holding the oldest owed DEPARTING's index.
   - **The rules:**
     - every SHUTDOWN's DEPARTING stays owed, with the index current at that SHUTDOWN, until the port takes it, across restart, timer expiry, link change or another SHUTDOWN;
     - owed DEPARTINGs leave oldest first;
     - a restart's ENTITY_AVAILABLE never passes an owed DEPARTING; it stays owed, with the machine in DELAY and no timer running, until the last DEPARTING has left;
     - a DEPARTING queued behind another carries 0, because its run could send no AVAILABLE;
     - an owed AVAILABLE is dropped only by a link loss or a SHUTDOWN.
   - **Unchanged.** A poll still sends at most one frame, so the per-pass bound stands (an owed DEPARTING costs 28 of the 31 accesses a poll is allowed). The API gains no precondition. The rule is stated in `adp.h` and on the design page.
   - **Standing tests in `test_adp.c`:**
     - **A15** is the review's case on the core's ports: advertise, saturate, disable, enable, then expire the new TMR_DELAY before room returns. The wire carries DEPARTING index 1, then AVAILABLE index 0. The machine is then in WAITING with TMR_ADVERTISE armed 5 s, nothing is owed, and the next AVAILABLE carries 1.
     - **E4** runs the same case through the driver, the model's timer and the loop, with a HAL that really sleeps. After the drain the wire carries DEPARTING 1, then AVAILABLE 0, and TMR_ADVERTISE is armed 5 s after the AVAILABLE left. The loop does not sleep while either frame is owed; afterwards it sleeps, and the expiry wakes it.
     - **A16:** a second SHUTDOWN while one DEPARTING is owed queues its own. The wire carries DEPARTING 1, then DEPARTING 0, and the running restart is untouched.
     - **A17:** room returns and the TMR_DELAY expires before any poll; the DEPARTING still leaves first.
   - **Defects:**
     - `available-replaces-owed-departing` (the review's defect) is caught by A15;
     - `available-passes-owed-departing` is caught by A17;
     - `second-departing-dropped` is caught by A16;
     - `departing-sends-zero` now patches the new code and is still caught by A10.
2. **Carried centiseconds (R496-2 N1).**
   - **L8** in `test_port_loop.c`: 40 centiseconds wait behind a full event ring, then one more is posted as a second TICK record while part of the 40 is still carried. All 41 are delivered and none is left owed.
   - **Defect:** `carried-ticks-overwritten` (`=` for `+=` at `ctrl_loop.c:99`) delivers 33, and L8 catches it.
3. **AXI4-Lite W/AW pairing (R496-2 N2).**
   - **A7** in `axil_checks.hpp` makes four back-to-back writes to four registers. Each channel offers its next beat the cycle after its last one was taken.
   - It runs twice: once with W beside AW, and once with W 3 clocks ahead. Each run gets exactly 4 B, and every register reads back its own write's data.
   - **Defects:** `axil-wready-while-issuing` (R496-2's probe) and its AW twin `axil-awready-while-issuing` each give 2 B for 4 writes, with the data misplaced. A7 catches both.
4. **Defect counts (R497-2 F2, R496-2 N3).** Four pages now reference `mutants.py` and `ctrl_mutants.py` instead of restating counts:
   - the design page's Verification row;
   - the suite index's `mbx` row;
   - the mbx README;
   - the firmware README.
5. **dev `28f9666f` merged** with `--no-ff`.

The RTL, the SoC, the builder, `configs`, `avdecc` and `milan_baremetal` are unchanged this round. Files changed since `a3ea8ffe`:
- `sw/firmware/ctrl/adp/{adp.c,adp.h,adp_mbx.h}`;
- `sw/firmware/ctrl/test/{test_adp.c,test_port_loop.c,ctrl_mutants.py}`;
- `sw/firmware/ctrl/README.md`;
- `tb/verilator/mbx/{axil_checks.hpp,mutants.py,README.md}`;
- `tb/verilator/README.md`;
- `docs/design/MAILBOX_SPLIT.md`;
- the merged findings page.

**Validation** (all at `3ebd6ca3`, rc 0):
- **Mailbox suite:** `make -C tb/verilator/mbx` (Verilator 5.050, from clean) gives 134 Wishbone + 179 AXI4-Lite (134 + 45) + 13 co-simulation checks, 0 failures, quick mutants 4 of 4. `mutants.py`: both controls ok, **46 of 46** caught. `suite_tally.py --verdict`: rc 0.
- **Firmware:** `test_ctrl_firmware.py --require-rv32 --self-test --lwsrp <lwSRP 19f5796b>` gives 701 checks:
  - model 134, port 81, adp 107, walk 320, entity 45, rv32 1, lwsrp 13;
  - **41 of 41** firmware defects caught, and both lwSRP pin refusals ok;
  - RV32I text 11,508 B, bss 170 B, no heap symbol.
- **Latency figures, unchanged:**
  - per path (accesses): DISCOVER 31, TMR_DELAY 39, TMR_ADVERTISE 11, GM 11, LINK 11 (down 9), SHUTDOWN 29;
  - full backlogs: the response in pass 2 (175 accesses), the receive ring by pass 14 (457), worst pass 105 against 407.
- **Builder bank:** `test_builder.py --require-rv32` gives ALL GATES PASS EXCEPT 1 NOT RUN (gate 11: the Arty route report is not on this host, as in rounds 1 and 2).
- **Scope and contract:** `ci_scope.py --selftest`; `ci_events.py --check` and `--selftest`; `gen_mailbox.py --check --crosscheck` and `--selftest`.
- **SoC and firmware tests:**
  - the sw/litex tests (`test_pp_boot_bus_freeze`, `test_pp_mem_bridge`, `test_cpu_memory_port_cdc`, `test_gptp_tx_timestamp`, `iob_pack_selftest`);
  - `test_nvm_firmware.py --self-test`.
- **RTL and code gates:**
  - `lint_rtl.py --check` and `--self-test`, and Yosys on the three mailbox tops (full and elaborate);
  - SoC and RTL source lists, bare-metal-only, sweep/deploy/entity shapes, wire accountability, `pp_srcs`;
  - the SV/C++/Python/shell idiom gates, hygiene, TODO ownership, test evidence, naming, port contracts, fail-fast;
  - `gen_module_matrix.py --check`.
- **Docs gates:**
  - `docs_check`, em-dash against `origin/dev`, `gen_toc` (3 modes);
  - doc paths, style, map, solution, submodule, PNG, feature status, archive;
  - `gen_hdl_reference` (self-test and build);
  - `git diff --check` against `origin/dev` and against `fa450d30`.
- **Default build unchanged against dev `28f9666f`.** Gateware exports with dev's and the head's `milan_soc.py`, switch off, give 22 of 22 files equal for all five configs:
  - AX7101 at the shipping arguments;
  - Arty at a 100 MHz proxy, because 83.333 MHz is refused identically on both sides.

  Switch on adds the same 8 files as in round 2.

**Acceptance criteria:**
- Round-3 items 1 to 5 are met, with the evidence above.
- Lane items and round-2 items remain met.

**Open risks/questions:**
- **Not run:** `act` and the hosted contexts (the head is not pushed, so no PR head exists for `act_ci.py --pr 668`).
- **Not run, no RTL changed:** `xvlog_gate.py` and a new switch-on OOC area; the round-2 area (2,641 LUT, WNS +0.240 ns) stands at the unchanged mailbox RTL.
- **Re-review scope:** round 3 changes ADP firmware source, so Conformance, RTL (architecture), Robustness, Tests and Docs all need re-review at this head.
- **R496-2 RESIDUE R1** (`CI_WORKFLOWS.md` wording) is left for the residue checklist; suggestions S1 to S5 are not taken this round.
- **Unchanged limits:** the SEQ count belongs to one firmware run, and time per access (A4) is not measured.
