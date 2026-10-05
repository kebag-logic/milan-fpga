[R496] NEGATIVE - exact head a3ea8ffe16585270911705ffabd68ca5e17fc9e0

# R496-2: internal cleared-context review of PR #668 (issue #665, lane F0), round 2

- **Head:** `a3ea8ffe16585270911705ffabd68ca5e17fc9e0`, tree `07f62aee959ab4004ef4f2c8a3b10f0b6d52593c`. This is round-1 head `0bfef498` plus 9 one-line commits (`528b96fe1` to `9daf95ac2`) and the `--no-ff` merge of dev `510fae60b26bef1db138de5cf2ac72b17b5011a5`.
- **The merge is mechanical.** `git merge-tree --write-tree 9daf95ac2 510fae60b` gives `07f62aee...`, the head's tree. Relative to dev, the lane changes only its own files, with `sw/litex/milan_soc.py` the one shared SoC file.
- **What I reconstructed from:**
  - AGENTS.md, CONTRIBUTING.md and docs/README.md;
  - the #665 body, lane assignment 5991862788 and directive 5992455815;
  - the round-2 assignment 5995086086, rulings 5994730420 (commit order, events first) and 5994972330 (DEPARTING index), and REVIEW READY 5997778834;
  - the PR body, `git diff fa450d30..a3ea8ffe` and `0bfef498..9daf95ac2`;
  - the published evidence `review-evidence/665f0-r1` at `8df40e37` (round-1 author documents only).
- **Order of work:** I wrote my independent pass first. Only then did I read the prior findings (R496-1 5995078461, R497-1 5994956684), and I grade them below.
- **Lenses applied:** all five.
  - Clean: Conformance, RTL, Robustness.
  - Unclean: Tests (N1, N2) and Docs (N3).
  - One RESIDUE (R1) is recorded for the residue checklist.

## Findings

### N1 - MINOR - Tests - `sw/firmware/ctrl/test/test_port_loop.c:405-436` (L7), `sw/firmware/ctrl/test/test_adp.c:577,636` (F0/F4), against `sw/firmware/ctrl/loop/ctrl_loop.c:99` - lost carried centiseconds go undetected when a second TICK record arrives

- **Evidence:** round 2 added the carry: `ticks_owed`, the slice of 16 per pass, and `l->ticks_owed += ev.tick_count`. Every check that exercises it takes exactly one TICK record:
  - L7 takes 40 centiseconds in one record;
  - F0/F4 take 30 in one record.
- **The escaping defect:** I planted `l->ticks_owed = ev.tick_count` (`scripts/reviewer_fw_probes.py`, arms `p-carried-ticks-overwritten` and `-adp`). The `port` and `adp` arms both pass it at rc 0 (`receipts/reviewer_fw_probes.log`).
- **Reachability:** `scripts/tick_carry_probe.c` uses the same model and loop. It fills the event ring, coalesces 40 centiseconds, and then lets one more centisecond pass while 24 are still carried.
  - The head delivers 41 of 41.
  - The planted copy delivers 33 of 41 (`receipts/tick_carry_probe.txt`).
- **Authority:**
  - `ctrl_loop.h:49-55` says centisecond consumers "lose no tick when the core is late; a long stall is caught up a bounded slice at a time", and `MAILBOX_SPLIT.md:234` repeats it.
  - Round-2 assignment item 5 asks for tests with coalesced ticks.
  - AGENTS.md section 6, Tests lens: each new test can fail for the defect it claims to detect.
- **Impact:** a one-token regression in the new carry logic would silently drop lwSRP centiseconds whenever a TICK record arrives during catch-up, so MRP leave, LeaveAll and periodic timers would run long. Every gate would stay green.
- **Required outcome:** two things.
  - A check takes a TICK record while centiseconds are still carried and requires every centisecond delivered.
  - A planted arm (overwrite instead of accumulate) is caught by that check's name.
- **Verification:** `test_ctrl_firmware.py --self-test` lists the arm as caught, and `scripts/reviewer_fw_probes.py` reports `p-carried-ticks-overwritten` caught.

### N2 - MINOR - Tests - `tb/verilator/mbx/axil_checks.hpp:205-228` (A3 write stream), against `hdl/milan/mailbox/KL_mbx_axil.sv:88,118-124` - no check pairs AXI4-Lite write data with its address under back-to-back writes

- **Evidence:** I planted a registered, non-combinational defect: `assign s_wready_o = !w_full_r || go_wr_w;`. It raises WREADY on the cycle the W slot drains, but the slot loads only when empty, so that beat is lost. The suite passes it: 174 of 174 AXI4-Lite checks plus A0 (`receipts/reviewer_rtl_probes.log`, `p-axil-wready-while-issuing` ESCAPED).
- **Why it escapes:** the only back-to-back write traffic is A3's stream, which writes one register and checks only the B count.
- **A data-checked stream catches it:** in a scratch copy of `axil_checks.hpp` I added four back-to-back writes to four registers, each read back (`scripts/axil_stream_probe.patch.py`).
  - Head RTL: 179 of 179 pass.
  - The planted RTL fails 4: 3 B for 4 writes, each value landing one register early, and the last register left 0 (`receipts/axil_stream_probe.txt`).
- **Authority:**
  - `MAILBOX_SPLIT.md:176-179`: "AW, W and AR are each taken into a one-entry slot by their own handshake, in either order and in any cycle".
  - Round-2 assignment item 2.
  - AGENTS.md section 6, Tests lens (boundary behaviour covered).
- **Impact:** a lost or mispaired W beat corrupts data or hangs a hard core's streaming writes, and it would merge green. The RTL at the head is correct; the suite would not notice if it stopped being.
- **Required outcome:** two things.
  - A back-to-back write stream, or an equivalent, to distinct addresses with read-back, run by the suite's default target.
  - A planted arm for a beat accepted on the drain cycle and not stored, caught by that check's name.
- **Verification:** `make -C tb/verilator/mbx mutants` lists the arm as caught, and `scripts/reviewer_rtl_probes.py` reports `p-axil-wready-while-issuing` caught.

### N3 - MINOR - Docs - `docs/design/MAILBOX_SPLIT.md:365`, `tb/verilator/README.md:72` - the planted-defect counts are stale

- **Evidence:** the head's campaigns plant 44 RTL and 37 firmware defects, all caught (`receipts/mbx_mutants.log`, `receipts/ctrl_fw.log`).
  - The design page's Verification table still says "30 RTL arms ... and 28 firmware arms"; that row last changed at round-1 head `0bfef498`.
  - The suite index says "`make mutants` all 30".
  - `tb/verilator/mbx/README.md:14`, `sw/firmware/ctrl/README.md:72` and the PR body already say 44 and 37.
- **Authority:** AGENTS.md section 6, Docs lens: changed contracts are reflected, and a cold reviewer has enough evidence. This is a stated figure of test evidence, so under the owner rule it is not RESIDUE.
- **Impact:** the authoritative design page understates the planted-defect evidence by 14 RTL and 9 firmware arms and contradicts the suite README.
- **Required outcome:** both rows state the head's counts, or point to the README without restating a count.
- **Verification:** a grep of both files against `mutants.py` and `ctrl_mutants.py` at the new head.

## Residue (owner rule 2026-10-02; for the manager's residue checklist)

### R1 - RESIDUE - Docs - `docs/testing/CI_WORKFLOWS.md:58-59,75`

"Six pages under `docs/` are relevant because Python in a classifier-gated job names them." The sixth page's reader, `sw/mailbox/gen_mailbox.py --check --crosscheck`, runs in no hosted job. No workflow, suite Makefile or builder references it, and line 75 already says "No `docs-check` step runs it". The classification, the count (six) and the self-test are all correct. Only the reason given is wrong for this page.

**Exact fix:**

- Line 58-59 becomes: "Six pages under `docs/` are relevant because Python that the classifier's self-test scans names them; five of those readers run in a classifier-gated job."
- Line 75 becomes: "(#665). No hosted job runs it yet; the page is relevant because its reader is Python under `sw/`."

## Suggestions (non-blocking; they do not affect coverage)

- **S1 (retained from R496-1 S1):** wire `gen_mailbox.py --check --crosscheck --selftest` and `test_ctrl_firmware.py --require-rv32 --self-test` into hosted CI. This is a reviewed CI-contract change for its own issue (the author's open risk S1).
- **S2:** add a dedicated A2 arm, such as a write issued on its W alone. My `p-axil-write-without-aw` is caught by A2, with 3 A2 checks failing (`receipts/reviewer_rtl_probes_a2.log`). So the check works; only the table lacks it.
- **S3:** state the commit-order scan's timing premise in the contract. A record committed on a channel the in-flight scan has already passed is seen by the next scan. Order holds because two TX_HEAD doorbells are at least one record (7 or more accesses, 14 or more clocks) apart, while the scan spans at most 5 clocks between channels. A future batched-commit driver or DMA producer would need that premise restated.
- **S4:** the ADP filter's smallest record is 26 bytes (9 words, 28 records), while A1 counts 15-byte records (42). So the 21-pass ADP figure is a conservative upper bound, not the reachable worst case. Saying so beside A1 would help a later lane that tightens it.
- **S5 (retained from R496-1 S4):** no check wraps the 16-bit ring counters past 65535. The 16-bit SEQ wrap is now checked (X2).

## Prior public findings at this head

| Finding | Status at `a3ea8ffe` | Evidence |
|---|---|---|
| R496-1 F1 (ci_scope gate-read) | RESOLVED | `MAILBOX_CONTRACT.md` is in `GATE_READ_DOCS` with a case at `scripts/ci_scope.py:60,276-277`; `ci_scope.py --selftest` rc 0 (`receipts/gate_ci_scope_selftest.log`); the policy page names its reader. Hosted `changes` and `rtl-fast` succeeded at the head; other contexts were still running at my snapshot (manager-owned). Wording residue R1. |
| R496-1 F2 (AXI4-Lite handshakes untested) | RESOLVED | A1 to A6 and the per-clock probe A0. My four round-1 defects now map to caught arms: `axil-b-dropped-without-bready`, `axil-r-dropped-without-rready`, `axil-read-before-write` and `axil-write-without-w` (`receipts/mbx_mutants.log`). A new, narrower gap is N2. |
| R496-1 F3 (lwSRP pin) | RESOLVED | `ctrl_arms.py:184-205` holds `LWSRP_REV` and refuses another HEAD or a dirty `src/`. Both refusal arms are `[ok]` in my run, and the clean pin passes 13 of 13 (`receipts/ctrl_fw.log`). The README carries the fetch recipe. |
| R496-1 F4 (host-counter guards) | RESOLVED | The `KL_mbx_evt.sv` guard is added; H0 to H2 are present, with `rx-tail-unguarded`, `tx-head-unguarded` and `evt-tail-unguarded` caught. My own `p-evt-guard-ahead-only` is caught by H2. |
| R496-1 F5 (own-entity DISCOVER arm) | RESOLVED | `own-discover-discarded` is caught by the walk row (`receipts/ctrl_fw.log`). |
| R496-1 F6 (CPU netlist on switch-on) | RESOLVED | `MAILBOX_SPLIT.md` "Default build" states the regeneration and why. My switch-on export shows `f5f08b17...` becoming `9aee3fb3...` (`receipts/switch_on_additions.txt`). |
| R496-1 S2, S3, S5 | adopted | `mbx_plat_mmio.c:12-25` (wake source, device memory); `ctrl_loop.h:28-47` (composition bound). S1 and S4 are retained above as S1 and S5. |
| R497-1 F1 (combinational READY) | RESOLVED | Every AXI output at `KL_mbx_axil.sv:87-94` is a register or a constant. A0 catches both lane mutants and my three further combinational paths (BREADY to AWREADY, RREADY to ARREADY, WVALID to RDATA; `receipts/reviewer_rtl_probes.log`). |
| R497-1 F2 (DEPARTING index) | no defect by ruling 5994972330; the ruling's outcome is present | The citation of Figure 6-2, Figure 6-3 and 6.2.5.2.2 is in `adp.h:24-31`, `adp.c:148-149` and `MAILBOX_SPLIT.md:274-285`. A10 to A14 read the wire field for WAITING, DELAY, deferred sends, restart and wrap. `departing-sends-zero` is caught; my `p-departing-index-plus-one` is caught. |
| R497-1 F3 (owed output and sleep) | RESOLVED | `ctrl_loop.c:138-155`; E0 to E3 run with a HAL that really sleeps. `poll-owes-nothing` is caught, and so are my `p-step-sleeps-when-only-owed` and `p-poll-owes-departing-only`. |
| R497-1 F4 (latency bound) | RESOLVED | A1 to A4 are stated (`ctrl_loop.h:28-47`); I re-derived 407, 1,221 and 8,954 (`adp_mbx.h:86-103`). F0 to F7 reproduce: events by pass 2, the response in pass 2 at 175 accesses, the receive ring by pass 14 at 457, worst pass 105. "Microseconds on any bus" is gone. N1 is a narrower test gap in the tick carry this fix introduced. |
| R497-1 F5 (TX commit order) | RESOLVED | SEQ is in word 1 (`mailbox.yaml`, `KL_mbx_tx.sv:83-101,194-211`, `mbx.c:160-170`, model). X2 runs on both adapters and the model, and D3 on the driver; `tx-round-robin`, `tx-seq-wrap-unsigned`, `tx-ties-fixed-priority`, `model-round-robin` and `seq-not-stamped` are caught. My five further merge defects are caught. |

Round-2 assignment items 8 and 9:

- **Item 8:** `git diff --check` is rc 0 against both base and dev. No tracked `README-tests.md` ends in a blank line.
- **Item 9:** the dev merge is clean and mechanical; the processor gitlink is `ead80360`, and the walk proves pin and blob (320 of 320).

## Lens results (artifact-specific)

```text
[R496] PASS Conformance - hdl/milan/mailbox/KL_mbx_axil.sv:82-157, sw/mailbox/mailbox.yaml (TX record word 1), hdl/milan/mailbox/KL_mbx_tx.sv:83-255, sw/firmware/ctrl/mbx/mbx.c:160-170, sw/firmware/ctrl/adp/adp.c:140-153, sw/firmware/ctrl/loop/ctrl_loop.h:13-55, sw/firmware/ctrl/adp/adp_mbx.h:23-103, sw/litex/milan_soc.py (lane hunks vs dev 510fae60), scripts/ci_scope.py:52-64,273-277 - checked against IHI0022H A3.1.1/A3.2.1 as cited by the assignment (no input-to-output path: every output a register or constant, A0 plus 5 combinational defects caught), ruling 5994730420 (commit order across channels incl. wrap and ties, events first in each pass, per-channel RX budgets kept), ruling 5994972330 (DEPARTING carries the current index, first AVAILABLE after restart 0; Figures 6-2/6-3 and 6.2.5.2.2 cited), the latency-bound arithmetic (407 / 1,221 / 8,954) and the measured backlog figures, lane items 1-6, and the default build: 22 of 22 export files equal dev vs head for all five shipped configs under the repository's PYTHONHASHSEED=0 launch rule (dev-vs-dev control equal; Arty at the 100 MHz proxy, 83.333 MHz refused identically on both sides), switch-on adding exactly 7 sources, KL_mbx + KL_mbx_wb, region 0x90100000, CSR bank 0xf000f000, IRQ 3 and netlist f5f08b17 -> 9aee3fb3 (receipts/default_build_*.txt, receipts/switch_on_additions.txt).
[R496] PASS RTL - hdl/milan/mailbox/KL_mbx_axil.sv, KL_mbx_tx.sv, KL_mbx_evt.sv:101-138, KL_mbx_pkg.sv (TXREC W1 SEQ/RSVD), KL_mbx.sv:38,405-427 (one-cycle registered ack that the adapter's pulse-then-busy protocol relies on) - checked: slot/busy/B/R FSM complete, write-first arbitration with a read guaranteed the cycle after a write's B, synchronous reset clears all slots and responses; scan step width KW_C = 3 covers N_CH+1 = 6, modular SEQ compare by sign bit, PICK rechecks pending, ERR/DONE update last_ch_r; event guard covers tail ahead and more than a ring behind; Verilator 5.050 -Wall build of both adapters with no warnings (receipts/mbx_make.log), lint_rtl --check PASS 90 <= ratchet 90 with no mailbox entry (receipts/gate_lint_rtl_check.log), Yosys full and elaborate on KL_mbx, KL_mbx_wb, KL_mbx_axil PASS (receipts/yosys_focused.txt); single clock, no CDC. Switch-on area 2,641 LUT is internally consistent (rows sum 2,621; deltas 132 and 115) but not re-measured.
[R496] PASS Robustness - KL_mbx_tx.sv refusal/flush and out-of-range TX_HEAD (H1), KL_mbx_evt.sv out-of-range EVT_TAIL (H2), RX_TAIL (H0), KL_mbx_axil.sv reset mid-transfer (A6) and B/R backpressure (A4/A5), ctrl_loop.c:92-155 owed output / sleep and tick carry, adp.c:248-260 adp_poll - checked on the head: all H, A, E0-E3 and F0-F7 checks pass; my tick-carry scenario delivers 41 of 41 (receipts/tick_carry_probe.txt) and my back-to-back data-checked AXI stream passes 179 of 179 (receipts/axil_stream_probe.txt); malformed SEQ word on a malformed record only affects which channel is refused first (the flush still applies).
[R496] UNCLEAN Tests - N1 (tick carry across a second TICK record undetected), N2 (AXI write data/address pairing under back-to-back writes undetected). Reproduced at the head: make -C tb/verilator/mbx 134 / 174 / 13 checks, quick 4 of 4; mutants.py both controls ok, 44 of 44; test_ctrl_firmware.py --require-rv32 --self-test --lwsrp <19f5796b>: model 134, port 78, adp 84, walk 320, entity 45, rv32 1 (text 11,412 B, bss 170 B), lwsrp 13, 37 of 37, both pin refusals ok; gen_mailbox --check --crosscheck and --selftest, ci_scope --selftest, ci_events --check/--selftest, gen_module_matrix --check all rc 0; reviewer probes 13 of 14 RTL and 6 of 9 firmware caught (the firmware escapes: N1, plus one equivalent BAD-record break/continue).
[R496] UNCLEAN Docs - N3 (stale planted-defect counts). Examined: docs/design/MAILBOX_SPLIT.md (commit order, adapters, firmware, ADP slice incl. DEPARTING citation, service latency, verification, default build incl. CPU netlist, area), docs/reference/MAILBOX_CONTRACT.md (generated, --check clean), docs/testing/CI_WORKFLOWS.md (residue R1), sw/firmware/ctrl/README.md, tb/verilator/mbx/README.md, tb/verilator/README.md, hdl/milan/mailbox/README-tests.md, ctrl_loop.h / adp_mbx.h / adp.h / mbx_plat_mmio.c comments, the PR body (no host paths or account names) and REVIEW READY 5997778834.
```

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_mbx_axil.sv`, `KL_mbx_tx.sv`, `mailbox.yaml`, `mbx.c`, `adp.c`/`adp.h`, `ctrl_loop.h`, `adp_mbx.h`, `milan_soc.py`, `ci_scope.py`; default-build and switch-on exports vs dev `510fae60` | R496-2 | a3ea8ffe16585270911705ffabd68ca5e17fc9e0 |
| RTL | CLEAN | `hdl/milan/mailbox/*.sv` (8), `tb_mbx_top.sv`; Verilator -Wall build, lint_rtl, Yosys full and elaborate on 3 tops | R496-2 | a3ea8ffe16585270911705ffabd68ca5e17fc9e0 |
| Robustness | CLEAN | H0-H2, A4-A6, E0-E3, F0-F7 paths in RTL and firmware; tick-carry and AXI-stream behaviour probed on the head | R496-2 | a3ea8ffe16585270911705ffabd68ca5e17fc9e0 |
| Tests | UNCLEAN (N1, N2) | `suite.hpp`, `axil_checks.hpp`, `bench.hpp`, `mutants.py`, `test_adp.c`, `test_port_loop.c`, `ctrl_mutants.py`, `ctrl_arms.py`; full suite, 44 RTL and 37 firmware campaigns; 23 reviewer probes | R496-2 | a3ea8ffe16585270911705ffabd68ca5e17fc9e0 |
| Docs | UNCLEAN (N3; RESIDUE R1 does not affect coverage) | `MAILBOX_SPLIT.md`, `MAILBOX_CONTRACT.md`, `CI_WORKFLOWS.md`, the four READMEs, header comments, PR body | R496-2 | a3ea8ffe16585270911705ffabd68ca5e17fc9e0 |

Coverage is banked against this commit. Fixes for N1 and N2 change test files, which are within the Tests scope. The fix for N3 changes docs, which are within the Docs scope. If a fix stays inside those files, Conformance, RTL and Robustness stay covered at `a3ea8ffe` as an ancestor. Any RTL, firmware, contract or SoC change un-covers the lenses whose scope it touches.

## What I ran (all at the exact head in disposable copies under `scratch/`; rc 0 unless noted)

| Command or probe | Result |
|---|---|
| Verilator identity | `verilator --version` gives `Verilator 5.050 2026-07-01 rev v5.050` |
| `make -C tb/verilator/mbx` | Wishbone 134/0, AXI4-Lite 174/0, co-simulation 13/0, quick mutants 4 of 4 (`receipts/mbx_make.log`) |
| `tb/verilator/mbx/mutants.py --jobs 3` | both controls ok; 44 of 44 caught (`receipts/mbx_mutants.log`) |
| `test_ctrl_firmware.py --require-rv32 --self-test --lwsrp <lwSRP 19f5796b>` | all 7 arms ok, 37 of 37 caught, both pin refusals ok, PASS (`receipts/ctrl_fw.log`; a first attempt refused because my scratch tree lacked `gptp-processor`, then I initialised it) |
| `ci_scope.py --selftest`; `ci_events.py --check` and `--selftest`; `gen_mailbox.py --check --crosscheck` and `--selftest`; `gen_module_matrix.py --check`; `git diff --check` vs base and vs dev | all rc 0 (`receipts/gates_rc.txt`) |
| `lint_rtl.py --check` | rc 2 on the first attempt, a refusal because my scratch tree lacked `third_party/verilog-axis`; rc 0 after initialising it, PASS 90 <= 90. `--self-test` rc 0 |
| `syn/yosys/run.sh --mode full` and `elaborate` on `KL_mbx`, `KL_mbx_wb`, `KL_mbx_axil` | 6 of 6 PASS (`receipts/yosys_focused.txt`) |
| `default_build_probe.py` + `normalise_compare.py`, five configs, dev vs head and dev vs dev, `PYTHONHASHSEED=0` | 22 of 22 equal for every config, control equal (`receipts/default_build_compare.txt`). Unseeded runs vary the ISA spelling and CPU netlist name run to run on dev alone (`receipts/unseeded_export_nondeterminism.txt`), which is why the repository pins the seed (`docs/integration/BUILDING.md:329`) |
| switch-on export (AX7101 1x1) | the stated additions exactly (`receipts/switch_on_additions.txt`) |
| `reviewer_rtl_probes.py` (12) and `reviewer_rtl_probes_a2.py` (2) | 13 of 14 caught; `p-axil-wready-while-issuing` escapes (N2) |
| `axil_stream_probe.patch.py` | head 179/0; drain-cycle WREADY defect 179/4 (N2) |
| `reviewer_fw_probes.py` (9) | 6 caught. Escapes: `p-carried-ticks-overwritten` in port and adp (N1), and `p-bad-record-ends-rx-stage` (equivalent: after a BAD record the driver resyncs to RX_HEAD, so `break` and `continue` differ only for a frame arriving inside the pass) |
| `tick_carry_probe.c` | head 41 of 41; planted copy 33 of 41 (N1) |
| hosted check runs (read-only API) | `receipts/hosted_checks_snapshot.txt` |
| review-clone integrity | `receipts/clone_integrity.txt` |

## Real limits

- **Hardware:** physical calibration was NOT RUN, and no hardware was used. Field skips are not hardware proof.
- **Source validation only:** this is not the final current-dev candidate, which the manager builds at the merge turn.
- **Hosted state:** I read it read-only at one moment.
  - Succeeded: `changes`, `rtl-fast`, `verilator-lint`, `yosys-elaboration`, the four Yosys shards, Verilator shard 3/5, `docs-check-no-git`, `bdd-conformance`, `wire-accountability` and `full-ci-gate`.
  - Still running: Verilator shards 0, 1, 2 and 4, `elaborate` and `docs-check`.
  - Skipped (not executed): `Physical gPTP`.
  - Hosted and act acceptance belong to the manager.
- **Not reproduced:** the switch-on routed area (2,641 LUT, 2,737 FF, WNS +0.240 ns). No Vivado was run. I checked the figures' internal arithmetic only. I did not run `xvlog_gate.py`.
- **Arty identity:** default-build identity for the three Arty configs is shown at the 100 MHz proxy only, because this LiteX checkout refuses 83.333 MHz on both sides.
- **Latency units:** the bounds are counted in mailbox accesses. No CPU-cycle figure exists (assumption A4, an open item).
- **Standards texts:** the IEEE 1722.1-2021, Milan v1.2 and AMBA texts were not available locally. I graded DEPARTING and the AXI path rule against the public rulings and the clauses they cite.
- **Round-2 evidence:** the published evidence tree I was given holds round-1 author documents only. I graded round 2 from the PR body, the REVIEW READY comment and my own runs.
- **Not run, by instruction:** the full parent, processor, gPTP, Yosys and builder banks; act or the host act runner; hosted re-runs.
- **The review clone was never edited.**
  - All 1,077 tracked files hash to their index blobs, the index matches HEAD's tree (blobs and modes), and nothing is untracked.
  - The `gptp-processor`, `protocol-processor` and `third_party/verilog-axis` gitlinks match HEAD and their checkouts.
  - `external` was uninitialised as received and remains so (`receipts/clone_integrity.txt`).
- **Redaction:** receipts have host paths replaced by `<packet>`, `<clone>`, `<pinned-verilator-5.050>`, `<verilator-image>` and `~`. The raw originals stay under the unpublished `scratch/`.

## Pending manager duties

- Publish this packet. Carry RESIDUE R1 to the residue checklist.
- After the N1 to N3 fixes:
  - obtain a new exact head;
  - run the act-first replica;
  - get exact-head hosted `changes`, `rtl-fast`, `verilator-suites` and `yosys-portability` executed and green;
  - re-review Tests and Docs, plus any lens whose scope the fix touches.
- Before merge: two independent positive reviews, the final current-dev candidate validation, explicit maintainer authorization to merge, and post-merge containment.
- Track S1 (CI wiring) as its own issue if accepted.

R496-2 FINISHED
