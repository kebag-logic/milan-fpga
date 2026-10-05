[R496] NEGATIVE - exact head 3ebd6ca30106a006c20fd2879dcad9c79bf51dca

Round R496-3, internal independent review of #665 lane F0 / PR #668. Tree `58f02a8d2be6f1d5605db8df5aeab173a9ea76f1`. Round-3 delta: `592f09cb`, `7c2df592`, `f67f055e`, `5f4fe8b3` on `a3ea8ffe`, then a `--no-ff` merge of dev `28f9666f`.

## Summary

- **The round-3 assignment (5998250555) is met in substance.** R497-2 F1, R497-2 F2 = R496-2 N3, R496-2 N1 and R496-2 N2 are each resolved at this head, with reproduced evidence and reviewer probes (table below).
- **Two new MINOR findings are open, both from the owed-frame change of this round:**
  - **F1:** the stated latency bound no longer holds for an ENTITY_AVAILABLE queued behind owed ENTITY_DEPARTINGs. It is committed k+1 passes after room returns, not in the first. At k = 64 it took 1,959 accesses, against the stated 1,221.
  - **F2:** three legs of the new rule "an owed frame is never dropped by what follows" have no check. A planted copy that loses an owed DEPARTING on a link change during the restart passes the whole firmware gate.
- **Ledger:** F1 is attributable to all five lenses, so no lens is covered clean at this head. The verdict is NEGATIVE.
- **What I reproduced at the head (all rc 0):**
  - the mailbox suite: Wishbone 134, AXI4-Lite 179, co-simulation 13, quick 4 of 4;
  - `mutants.py`: both controls, 46 of 46;
  - the firmware gate with `--require-rv32 --self-test` and lwSRP at `19f5796b`: model 134, port 81, adp 107, walk 320, entity 45, rv32 1 (text 11,508 B, bss 170 B), lwsrp 13; 41 of 41 defects caught, both pin refusals;
  - the docs, contract, idiom and lint gates listed under "Executed".
- **The merge** is a clean automatic merge: `git merge-tree` of the two parents gives the head tree. It adds one findings page (`docs/findings/653_DISCONNECT_ORDER_BENCH.md`) and changes no gitlink.

The independent pass, findings F1 and F2, and the probes were completed before I read R497-2 (5998184135) or R496-2 (5998244827). Those two were read only to grade them, below.

## Findings

### F1 - MINOR - Conformance, RTL (architecture), Robustness, Tests, Docs - an ENTITY_AVAILABLE queued behind owed ENTITY_DEPARTINGs is committed k+1 passes after room returns, and the stated bound says the first pass

**Artifacts:**
- the claims: `sw/firmware/ctrl/loop/ctrl_loop.h:28-31,42-44`, `docs/design/MAILBOX_SPLIT.md:335-347`, `sw/firmware/ctrl/adp/adp_mbx.h:26,62-66`, and the PR body's latency paragraph;
- the mechanism: `sw/firmware/ctrl/adp/adp.c:121-131` and `:265-279` (one frame per poll, DEPARTINGs first);
- the evidence: `probes/probe_owed_bound.c`, `receipts/probe_owed_bound.log`.

**Authority:**
- The D3 ruling on #640 asks for a deterministic bound per response path, stated and tested, as cited at `MAILBOX_SPLIT.md:324-326`.
- `ctrl_loop.h` A3 states: when a response finds no room, "it is committed in the first pass after the merge frees the room".
- `ctrl_loop.h` and the design page also state: "the module's response is committed in the pass that takes it", and an event's response comes within 3 x 407 = 1,221 accesses.

**Evidence.** Round 3 lets one interface owe k DEPARTINGs plus the restart's AVAILABLE. A poll sends one frame, oldest DEPARTING first. That keeps the per-pass bound, but the AVAILABLE then leaves in pass k+1 after room returns. The same happens when the TMR_DELAY expiry is taken in a pass that already has room (A17's case through the loop). I measured this through the driver, the model and the loop at the head:

| k owed DEPARTINGs | AVAILABLE committed in pass (after room) | accesses from room to AVAILABLE |
|---:|---:|---:|
| 0 | 1 | 39 |
| 1 | 2 | 69 |
| 3 | 4 | 129 |
| 16 | 17 | 519 |
| 64 | 65 | **1,959 (> ADP_MBX_EVT_ACCESSES 1,221)** |

The k = 1 row is the assignment's own standing case, and E4 also shows the AVAILABLE in the second step. k is bounded only by `UINT32_MAX` (`adp.h:43`): each SHUTDOWN while the ring is stalled adds one.

**Impact.** The service-latency statement that D3 makes authoritative is false for a path this round created. A later lane that composes figures from A3 and `ADP_MBX_EVT_ACCESSES` would inherit a bound that the TMR_DELAY response path does not meet under backpressure plus repeated SHUTDOWN.

The ordering itself is correct. This is not a wire defect.

**Required outcome:**
- State the owed-frame latency as it is, in `ctrl_loop.h` A3, `adp_mbx.h` and the design page. For example: an owed AVAILABLE behind k owed DEPARTINGs is committed in pass k+1 after the room returns.
- Give k a stated bound, or change the queueing so a stated figure holds.
- Add a check that grades a k ≥ 1 case against the stated figure, with a planted defect that breaks it.

**Verification:**
- `probes/probe_owed_bound.c` against the corrected head agrees with the restated figure.
- The new check fails on its planted defect in `--self-test`.

### F2 - MINOR - Tests - three legs of the new owed-frame rule are unguarded; a copy that loses an owed DEPARTING on a link change passes every gate

**Artifacts:**
- the rule: `sw/firmware/ctrl/adp/adp.h:33-43`, repeated at `docs/design/MAILBOX_SPLIT.md:289-299` and in the PR body. It reads: "Every SHUTDOWN's ENTITY_DEPARTING stays owed ... across any restart, timer expiry, link change or later SHUTDOWN", and "An owed AVAILABLE is dropped only by a link loss or a SHUTDOWN".
- the code: `sw/firmware/ctrl/adp/adp.c:211-215` and `:218-224`;
- the checks: `sw/firmware/ctrl/test/test_adp.c:223` (A7) and `:235` (A8);
- the evidence: `probes/adp_reviewer_mutants.py`, `probes/probe_owed_rules.c`, `receipts/adp_reviewer_mutants.log`, `receipts/fullgate_*.log`, `receipts/probe_owed_rules.log`.

**Authority:**
- AGENTS.md section 6, Tests lens: each test can fail for the defect it claims to detect.
- The round-3 assignment item 1: an owed ENTITY_DEPARTING must never be lost.
- The lane rule: each new check needs a planted defect.

**Evidence.** The head behaves correctly on all three legs (`probe_owed_rules.log`, "head"). Each of these planted copies passes the whole firmware gate (model, port, adp, walk, entity, rv32, lwsrp; `receipts/fullgate_*.rc` = 0), and each produces a wire-visible defect:

| Planted copy | Effect on the wire (probe) | Why no check sees it |
|---|---|---|
| `link-loss-drops-owed-departing` (`departing_owed = 0` in the link-loss branch) | L1: advertise, saturate, disable, enable, link down, then link up and room. The wire carries `AVAILABLE(0) AVAILABLE(0)`; **DEPARTING(1) is lost**. | A8 exercises a link loss only in DOWN, where that branch is never reached. No check combines an owed DEPARTING, a running restart and a link loss. |
| `gm-change-drops-owed-available` | L2: a GM change while the AVAILABLE is owed. The machine **wedges in DELAY with no timer and nothing owed**. | No check sends a GM change, a DISCOVER or a stray expiry while an AVAILABLE is owed. |
| `link-loss-keeps-owed-available` | L3: the link bounces before a poll. **The AVAILABLE goes out without its new TMR_DELAY** (5.6.3.5.3). | A7 says "a link loss drops an owed ENTITY_AVAILABLE", but it polls before checking. The poll's own defensive drop then hides the defect. |

The first row is the defect class R497-2 F1 named: a lost DEPARTING. It is reached through the "link change" leg of the rule that round 3 wrote.

**Impact.** A regression in any of these legs would merge green. Two of them lose or wedge required ADP output.

**Required outcome:**
- Checks for an owed DEPARTING across a restart interrupted by a link loss and recovery.
- Checks that the inputs which may not drop an owed AVAILABLE (GM change, DISCOVER, a stray expiry) leave it owed.
- A check that a link loss itself, with no poll in between, drops the owed AVAILABLE.
- A named planted defect for each, caught by that check's name.

**Verification:**
- `--self-test` lists the new arms as caught.
- `probes/adp_reviewer_mutants.py` reports the three copies caught.

## Prior findings, graded against the round-3 assignment (5998250555) after the independent pass

| Prior item | Disposition at 3ebd6ca3 | Evidence |
|---|---|---|
| R497-2 F1 (MAJOR): a restart erases an owed DEPARTING | **RESOLVED** | See "R497-2 F1 in detail" below. Every item the assignment asked for is present, on both paths, with the named defects caught. F1 and F2 above are new findings about this fix, not a reopening of it. |
| R497-2 F2 = R496-2 N3: stale defect counts | **RESOLVED** | `MAILBOX_SPLIT.md:385`, `tb/verilator/README.md:72`, `tb/verilator/mbx/README.md:14,25` and `sw/firmware/ctrl/README.md:70-77` reference `mutants.py` and `ctrl_mutants.py` rather than restating counts. A grep finds no campaign count left on these pages. The PR body's 46 and 41 equal my campaigns. |
| R496-2 N1: lost carried centiseconds undetected | **RESOLVED** | L8 (`test_port_loop.c:438-457`) takes a second TICK record while centiseconds are carried and requires all 41 delivered and none owed. `carried-ticks-overwritten` (`ctrl_loop.c:99`, `=` for `+=`) fails only L8 (`got=0x21 exp=0x29`; `receipts/named_mutant_e4.log`). The design page states the accumulation (`MAILBOX_SPLIT.md:235-236`). |
| R496-2 N2: AXI4-Lite W/AW pairing under back-to-back writes | **RESOLVED** | A7 (`axil_checks.hpp:386-401`) runs in the default `run-axil`: four back-to-back writes to four registers, W beside AW and W 3 clocks ahead, 4 B each, read back. `axil-wready-while-issuing` and `axil-awready-while-issuing` are caught by A7 (`receipts/mbx_mutants.log`). My two crossing copies keep the B count and lose no beat (`wdata-overwritten-while-held`, `awaddr-overwritten-while-held`). They fail only A7's read-back checks, 2 of 179 (`receipts/axil_pairing_mutants.log`), so A7 grades the pairing itself. |
| R496-2 R1 (RESIDUE): `CI_WORKFLOWS.md:58-59,75` wording | **RETAINED as RESIDUE** | The text is unchanged at this head. The exact fix from R496-2 stands and goes to the manager's residue checklist. |
| R496-2 S1 to S5 | retained as suggestions | Not taken this round, as the executor states. They do not affect coverage. |

### R497-2 F1 in detail

- **The change.** `adp.c:107-131,154-173,265-279` replaces the single pending slot with `available_owed` plus a `departing_owed` count and the oldest DEPARTING's index.
- **A15 (the core's ports)** is the review's case: DEPARTING(1), then AVAILABLE(0), then WAITING with TMR_ADVERTISE at 5 s, nothing stranded, and the next AVAILABLE carries 1.
- **E4 (the driver, the model timer and the loop)** runs the same case with a HAL that sleeps.
- **The named defect** `available-replaces-owed-departing` fails 15 checks across A15, A16, A17 and E4, so it is caught on both paths. `available-passes-owed-departing` is caught by A17 and `second-departing-dropped` by A16.
- **My five further copies** were all caught: `queued-departing-keeps-first-index` (A16), `second-shutdown-overwrites-index` (A16), `poll-forgets-owed-available` (A15 and E1/E3/E4), `blocked-available-not-owed` (A15) and `poll-sends-two-frames` (A15 and E4).
- **The API** gains no precondition: `adp_set_enable` is unchanged.

### The round-3 focus points

- **Owed DEPARTING queue.** DEPARTINGs are never lost to a restart, a timer expiry or another SHUTDOWN. They leave oldest first, and a restart's AVAILABLE never passes one: `advertise()` refuses while `departing_owed != 0` (`adp.c:124`). An owed AVAILABLE is dropped only at `adp.c:164` (SHUTDOWN) and `:213` (link loss), plus the defensive drop in `adp_poll` at `:275`, which is reached only after those two. The link-change leg of "never lost" and the "only" leg are untested (F2).
- **The reading "a DEPARTING queued behind another carries 0" is sound under ruling 5994972330.** A DEPARTING carries the index current at its SHUTDOWN (Figure 6-3, 6.2.5.2.2). Each SHUTDOWN zeroes `available_index` (`adp.c:163`), and 6.2.2.15 increments it only after an AVAILABLE is transmitted. While any DEPARTING is owed, `advertise()` transmits nothing, so a run that starts behind an owed DEPARTING ends with index 0. The code relies on that invariant instead of storing a per-entry index (`depart()` sets `departing_index = 0`). Copies that break it are caught by A16.
- **Per-pass bound.** It holds. The probe's per-pass costs after room returns are 30 accesses (an owed-DEPARTING poll of 28 = TX record 25 + gPTP 3, plus the 2-access tail), and 33 for the final AVAILABLE pass. Both are within `ADP_MBX_POLL_MAX` 31 per poll and 407 per pass. The per-path statement is F1.
- **Lost-centisecond check.** See N1 above.
- **AXI data and address pairing.** See N2 above. `KL_mbx_axil.sv` is unchanged since `a3ea8ffe`.
- **The corrected counts.** See N3 above.

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | the round-3 assignment items 1-5 against `adp.c`, `adp.h` (the owed-frame rule, Milan v1.2 5.6.3.5.x, IEEE 1722.1-2021 6.2.2.15, Figure 6-3, 6.2.5.2.2 per ruling 5994972330), `ctrl_loop.h` A1-A4, `adp_mbx.h` bounds; A15/E4 wire order; the merge identity | R496-3 | 3ebd6ca30106a006c20fd2879dcad9c79bf51dca |
| RTL | UNCLEAN (F1, architecture: firmware latency under TX backpressure) | `hdl/milan/mailbox/*` unchanged since `a3ea8ffe` (empty diff, also `sw/mailbox`, `sw/litex`, `syn`, gitlinks); Verilator -Wall builds of both adapters with no warnings; `lint_rtl.py --check` PASS 90 ≤ 90; `KL_mbx_axil.sv` slot/handshake logic re-read for A7; the ADP owed-output state in `adp.c` | R496-3 | 3ebd6ca30106a006c20fd2879dcad9c79bf51dca |
| Robustness | UNCLEAN (F1) | owed frames under a stalled ring with restart, a second SHUTDOWN, link loss and recovery, GM change, and timer expiry (probe L1-L3: the head is correct on each); k up to 64 owed DEPARTINGs; tick carry across a second TICK record (L8) | R496-3 | 3ebd6ca30106a006c20fd2879dcad9c79bf51dca |
| Tests | UNCLEAN (F1, F2) | `test_adp.c` A6-A8, A10-A17, E0-E4, C0-C6, F0-F7; `test_port_loop.c` L7-L8; `axil_checks.hpp` A0-A7; `ctrl_mutants.py` (41 caught), `mutants.py` (46 caught); 8 reviewer firmware copies (5 caught, 3 escape) and 2 reviewer RTL copies (both caught by A7) | R496-3 | 3ebd6ca30106a006c20fd2879dcad9c79bf51dca |
| Docs | UNCLEAN (F1) | `MAILBOX_SPLIT.md` (owed frames, tick carry, A7, service latency, verification row), `tb/verilator/README.md`, `tb/verilator/mbx/README.md`, `sw/firmware/ctrl/README.md`, `adp.h`, `ctrl_loop.h`, `adp_mbx.h` comments, the PR body (counts match); `docs_check`, `check_em_dash --base fa450d30` (0 findings over 2,268 added lines), `gen_toc --check` and `--verify-anchors`, doc style, doc paths, `ci_events --check`, `ci_scope --selftest`, `gen_mailbox --check --crosscheck`, `git diff --check fa450d30 HEAD` all rc 0; R1 residue retained | R496-3 | 3ebd6ca30106a006c20fd2879dcad9c79bf51dca |

## Executed (receipts under `receipts/`)

- **Mailbox suite:** `make -j16` of `tb/verilator/mbx` (Verilator 5.050, identity checked), from a clean export of the head: `mbx_make.log`, rc 0.
- **RTL campaign:** `mutants.py --jobs 8`: `mbx_mutants.log`, rc 0, 46 of 46 caught.
- **Firmware gate:** `test_ctrl_firmware.py --require-rv32 --self-test --lwsrp <lwSRP 19f5796b>`: `fw_selftest.log`, rc 0.
- **Focused gates:** `gate_*.log` and `.rc`, all rc 0. `check_em_dash` and `gen_toc` ran with the pinned renderer from `tools/markdown/requirements.txt`, installed in a disposable environment.
- **Probes** (portable sources under `probes/`; `run_probes.sh` re-ran them with identical results, `run_probes_rerun.log`):
  - `probe_owed_bound.log`;
  - `probe_owed_rules.log`;
  - `adp_reviewer_mutants.log`;
  - `fullgate_*.log` and `.rc`;
  - `named_mutant_e4.log`;
  - `axil_pairing_mutants.log` and `probe_axil_*`.
- **Restore:** the clone was never edited, and probes ran on exported copies. A cache directory the firmware driver created was removed. Afterwards HEAD, tree, index, worktree blobs and modes, and every gitlink equal the head, with nothing untracked or ignored (`restore_check.txt`). Host paths in three build logs are normalized to placeholders.

## Real limits

- **Not run by me:** the full builder bank, the parent, PP, gPTP and Yosys banks, `xvlog_gate`, the default-build export comparison, and a switch-on OOC area.
  - Since `a3ea8ffe`, nothing they read changed: no HDL, SoC, `syn`, config or gitlink.
  - The dev side `510fae60..28f9666f` adds one Markdown page.
  - So R496-2's default-build and RTL evidence carries forward by file identity. It was not re-executed here.
- **Not executed here:** the co-simulation (13 checks) runs only the fixed round-1 scenario. The two crossing RTL copies were run through `run-axil` only.
- **Time:** time per mailbox access (A4) is not measured. F1's figures are access and pass counts on the host model.
- **Hardware:** physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Publish this packet.
- Obtain fixes for F1 and F2, then a re-review that covers every lens at the corrected head.
- Carry R1 to the residue checklist.
- Hosted acceptance at the exact head: at my snapshot 11 contexts passed, 7 were pending (Verilator shards 0, 1, 2 and 4, `yosys-elaboration`, `docs-check`, `elaborate`) and 1 was skipping ("Physical gPTP"). All four runs are `pull_request` runs on `3ebd6ca3`. The `act` replica is also the manager's.
- Build the final current-dev candidate (source base `fa450d30`, live dev `28f9666f`).
- The second independent positive review and a reviewer-accepted clean ledger.
- Merge authorization and post-merge containment.

R496-3 FINISHED
