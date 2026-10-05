[R496] NEGATIVE - exact head 0bfef4987eede4b022b17c7b2f56d079ff84893b

# R496-1: internal cleared-context review of PR #668 (issue #665, lane F0)

- Head: `0bfef4987eede4b022b17c7b2f56d079ff84893b`, tree `8fb1fca2c81b8fd79ba6daefe1147be4531088f4`, base `fa450d301805881ad713b67521477bf042ddadfd` (live dev at the time of review).
- Scope I reconstructed: AGENTS.md, CONTRIBUTING.md, docs/README.md, the #665 issue body, lane assignment 5991862788, owner directive 5992455815 (bare metal first, lwSRP port layer), TAKEN 5992024623, REVIEW READY 5994496304, the PR body, `git diff fa450d30..0bfef498` (71 files, 9 commits) and the published evidence tree `review-evidence/665f0-r1` at `8df40e37`.
- Prior public review findings on this PR: **none exist**. The PR has two review-start comments and no review bodies, and the issue carries no review findings. Nothing is resolved or retained from earlier rounds.
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs. **All five are UNCLEAN at this head** (ledger below).

## Findings

### F1 - BLOCKER - Tests, Conformance - `scripts/ci_scope.py:56` (`GATE_READ_DOCS`), with `sw/mailbox/gen_mailbox.py:66` - an existing CI-scope gate is red at the head, and the hosted gates are red because of it

- **Evidence:** `python3 scripts/ci_scope.py --selftest` at the exact head exits 1: `FAIL gate-read page docs/reference/MAILBOX_CONTRACT.md (named at sw/mailbox/gen_mailbox.py:66) is relevant`, then `selftest: 1 FAILURE(S)` (receipt `receipts/ci_scope_selftest_head.txt`). The PR does not touch `ci_scope.py`. Its new generator reads a `docs/` page that the classifier still treats as docs-only. The hosted run at this head fails the same way in `changes` (job 111763679877) and `elaborate` (job 111763679205). The rest cascades:
  - `rtl-fast` fails on `CHANGES_RESULT: failure`, and `verilator-lint` and `yosys-elaboration` never ran;
  - `verilator-suites` and `yosys-portability` fail with "found 0 shard directories" because every shard was skipped;
  - `full-ci-gate` fails.

  See `receipts/hosted_checks_exact_head.txt`. The gate table in the REVIEW READY comment and HANDOFF does not list `ci_scope.py`.
- **Authority:** AGENTS.md section 7 requires a successful `rtl-fast` verdict at the current head, plus exact-head `verilator-suites` and `yosys-portability` evidence. CONTRIBUTING's local bar applies. The rule this gate enforces is stated in `docs/testing/CI_WORKFLOWS.md:95`: a reader of this kind "must be added to `GATE_READ_DOCS`".
- **Impact:** the PR cannot reach a green hosted verdict. If the gate were bypassed, a docs-only change to the generated reference page would be classified docs-only and skip the tooling jobs that read it.
- **Required outcome:** `docs/reference/MAILBOX_CONTRACT.md` is classified relevant per the CI policy, and the policy page names its reader. `ci_scope.py --selftest` passes. The hosted `changes`, `rtl-fast`, `verilator-suites` and `yosys-portability` contexts execute and pass at the new head.
- **Verification:** `python3 scripts/ci_scope.py --selftest` returns rc 0; the new head shows the hosted contexts executed (not skipped) and green; the act-first replica runs at that head.

### F2 - MAJOR - Tests - `tb/verilator/mbx/bench.hpp:213-259` (AXI4-Lite master), against `hdl/milan/mailbox/KL_mbx_axil.sv:67-68,100-101` - the AXI4-Lite adapter's handshake rules are untested

- **Evidence:** the bench's AXI4-Lite master is always polite:
  - AW and W are offered in the same cycle;
  - BREADY and RREADY are held high;
  - no read is ever offered beside a write.

  I planted four single-line adapter defects into copies (`scripts/adapter_mutants.sh`, `receipts/adapter_mutants.txt`):
  - B dropped when BREADY is low;
  - R dropped when RREADY is low;
  - a read accepted in the same cycle as a write;
  - a write accepted on AW without W.

  **All four pass the suite's AXI4-Lite build at `checks: 120 failures: 0`.** My stress bench (`scripts/axil_stress/`) covers AW before W, W before AW, BREADY and RREADY held low, AR beside AW+W, and back-to-back reads. It catches every one of the four (1 to 3 failures each), and it passes 14 of 14 on the head's RTL, plus 3 of 3 on Wishbone back-to-back cycles (`receipts/adapter_stress_head.txt`). The adapter RTL is correct today. Its tests would not notice if it stopped being correct.
- **Authority:**
  - AGENTS.md section 6, Tests lens: each new test can fail for the defect it claims to detect, and negative and boundary behavior is covered.
  - Lane item 3: the API "must also fit a hard core".
  - The design page section "Bus adapters and the hard core": `KL_mbx_axil` is the hard-core path.
  - The suite's README claims "the same checks through both adapters".
- **Impact:** the only shipped evidence for the hard-core bus path is a happy-path master. A regression that hangs or drops a response under a real interconnect's backpressure would merge green.
- **Required outcome:** the mailbox suite, or a suite run by its default target, drives the AXI4-Lite adapter with AW/W skew in both orders, BREADY and RREADY low with BVALID/RVALID and payload stability, and a read offered beside a write. Each of these behaviours has a planted defect in `mutants.py` that the suite catches.
- **Verification:** `make -C tb/verilator/mbx mutants` catches the four defects above (or equivalents) by named checks, and the positive controls stay green.

### F3 - MINOR - Tests, Docs - `sw/firmware/ctrl/test/ctrl_arms.py:177-201` (`arm_lwsrp`), `sw/firmware/ctrl/README.md:82,86`, `docs/design/MAILBOX_SPLIT.md:274` - lwSRP is "referenced" with no recorded revision, and "unmodified" is not checked

- **Evidence:** 19f5796b appears nowhere in the tree. Only the REVIEW READY comment and HANDOFF name it. The arm compiles whatever checkout `--lwsrp` names. It prints that checkout's HEAD but checks neither HEAD nor worktree state. For a copy of lwSRP at 19f5796b with one local edit to `src/core/mrp_mad.c`, the arm reports `lwSRP at 19f5796b...` and passes 13 of 13 (`scripts/lwsrp_pin_probe.sh`, `receipts/lwsrp_arm_dirty_checkout.log`). I confirmed that it is not vendored: the diff adds only `shlan_port.h`/`.c` (prototypes restated, and identical to lwSRP's `src/ports/alloc.h` at 19f5796b) and the test driver. lwSRP's upstream HEAD at review time is also 19f5796b.
- **Authority:**
  - Owner directive 5992455815, item 2: fixes go upstream, "not as a private copy".
  - AGENTS.md section 2: a cold reviewer must reconstruct from the repository.
  - The lane's own claim "lwSRP 19f5796b, not vendored, ... unmodified".
- **Impact:** the lwsrp arm's evidence cannot be reproduced against a known revision. A local or upstream change to lwSRP, such as the F4 transmit-hook PR or a changed `alloc.h`, would change what the arm proves without the gate noticing.
- **Required outcome:** the tree records the lwSRP revision the port layer is written against. The arm refuses or fails, by name, on a checkout whose HEAD differs from it or whose sources and headers it compiles are modified. Alternatively, a recorded decision states that the reference floats, and the docs say so.
- **Verification:** re-run `scripts/lwsrp_pin_probe.sh`. The dirty checkout is refused, and the clean pin passes.

### F4 - MINOR - Tests, Robustness, RTL - `hdl/milan/mailbox/KL_mbx_rx.sv:141`, `KL_mbx_tx.sv:100`, `KL_mbx_evt.sv:132,136` - host-counter guards: two are untested, and the event ring has none

- **Evidence:** `scripts/ring_boundary_mutants.py` (`receipts/ring_boundary_mutants.txt`) planted seven ring and doorbell boundary defects. Five are caught. Removing the RX guard (`used_w > ring_words_w ? 0 : ...`) **survives**, and so does removing the TX guard (`occ_w <= ring_words_w`): 0 of 120 checks fail for each. The event poster has no equivalent guard. `free_w = 64 - (head_r - evt_tail)` in 16-bit arithmetic: for an EVT_TAIL ahead of EVT_HEAD it wraps to 68 or more, and `start_w` posts, overwriting records. This is despite the module's own statement that "the ring can never overflow". The RX and TX paths both guard the same class of bad host counter.
- **Authority:** AGENTS.md section 6, Robustness lens (invalid ordering and state; reset during activity, for example a fabric reset under a running core) and Tests lens (boundary and negative behaviour covered). `KL_mbx_evt.sv:21-32` and the contract's EVT_TAIL row.
- **Impact:** the guards that exist are not pinned by any test. The event ring behaves differently from the frame rings when the host's counter is wrong, which a later lane could hit after a partial reset.
- **Required outcome:** tests that fail when the RX and TX guards are removed. For EVT_TAIL, either the same guard plus a test, or the contract (the `EVT_TAIL` row in `mailbox.yaml`) stating that a tail outside [EVT_HEAD - 64, EVT_HEAD] is undefined.
- **Verification:** re-run `ring_boundary_mutants.py`. The guard mutants are caught, and an EVT_TAIL arm is caught or the contract states the precondition.

### F5 - MINOR - Tests, Docs - `sw/firmware/ctrl/test/ctrl_mutants.py:35-63`, `sw/firmware/ctrl/README.md:72` - no planted defect exists for the walked row RCV_ADP_DISCOVER(own eid), although the docs say there is one per walked row

- **Evidence:** the ten walk arms target these rows: DISC0, LINK_DOWN (two arms), GM, SHUTDOWN, TMR_ADVERTISE, TMR_DELAY and LINK_UP, plus one available_index arm and P11. None plants a defect in the `R_DISCOWN` row. The README says "ADP clause defects caught by the walk (one per walked row)", and the REVIEW READY comment says "one per walked Table 5.51 row", excepting only the foreign DISCOVER. Planting the defect myself (`scripts/own_discover_probe.sh`, `receipts/fw_probe_own_discover_mutant.log`) shows the existing checks catch it: `adp` A4, and the walk row `RCV_ADP_DISCOVER(own eid) x WAITING`. So this is a gap in the table and a false coverage claim, not a missing check.
- **Authority:** the lane assignment, item 5: "Each new check needs a planted mutant that fails it". AGENTS.md section 6, Tests lens.
- **Impact:** the self-test does not show that the own-entity DISCOVER path's checks can fail, and the coverage statement overstates what the campaign proves.
- **Required outcome:** an arm in `ctrl_mutants.py` for the own-entity DISCOVER row (for example, my substitution), or a corrected claim.
- **Verification:** `test_ctrl_firmware.py --self-test` lists the new arm as caught by the named check.

### F6 - MINOR - Docs - `docs/design/MAILBOX_SPLIT.md:280-285`; REVIEW READY 5994496304 and HANDOFF section 6 - the switch-on composition omits the regenerated CPU netlist

- **Evidence:** with `--ctrl-mailbox`, every shipped config's export also swaps the CPU netlist:
  - AX7101: `VexiiRiscvLitex_f5f08b17...` becomes `VexiiRiscvLitex_9aee3fb3...`;
  - Arty: `7c73187a...` becomes `da596635...`.

  The CPU wrapper hashes the SoC memory-region list (`vexiiriscv/core.py`, the `memory_regions` term of the netlist hash), and the new uncached `ctrl_mbx` region changes that list. Nine export files differ, `litex.log` included (`receipts/switch_on_additions.txt`). The REVIEW READY comment says switch-on "adds exactly the 7 sources, 2 instances, one region ..., one pinned CSR bank ... and one interrupt". HANDOFF says "8 files differ, exactly". The design page's "On, it adds ..." list does not mention the CPU change. No existing CSR bank or region moves; that claim is correct.
- **Authority:** AGENTS.md section 6, Docs lens: changed contracts reflected, and enough evidence for a cold reviewer.
- **Impact:** an F-lane that measures or budgets the switch-on SoC would not know that the CPU variant changes with the switch. The published "exactly" list is wrong about a generated artifact.
- **Required outcome:** the design page and the evidence state that switch-on also regenerates the CPU netlist, and why (the region list).
- **Verification:** a docs read against `receipts/switch_on_additions.txt`.

## Suggestions (non-blocking; they do not affect coverage)

- **S1:** wire `gen_mailbox.py --check --crosscheck --selftest` and `test_ctrl_firmware.py --require-rv32 --self-test` into hosted CI through a reviewed CI-contract change. The author disclosed this gap, and it deserves its own issue.
- **S2:** `plat/mbx_plat_mmio.c`: a platform that defines `CTRL_MBX_WFI` must also enable the LiteX `ctrl_mbx` EventManager source and the CPU interrupt mask. Say so beside the macro.
- **S3:** for a weakly ordered hard core, state that the window must be mapped as device or strongly ordered memory, or give the HAL a barrier before the doorbell writes (TX_HEAD, RX_TAIL, EVT_TAIL).
- **S4:** no check exercises the 16-bit ring counters wrapping past 65535. The modular arithmetic is correct by reading; a long-run arm would pin it.
- **S5:** the "within two passes" latency statement depends on at most `CTRL_LOOP_EVENTS_PER_PASS` events and `CTRL_LOOP_RX_PER_PASS` records being ahead of the input. That holds for F0's composition (at most three event sources, TICK off), but later lanes should restate the bound for their composition.

## Residue

None recorded.

## Lens results (artifact-specific)

What I examined under each lens, including the parts I found clean, so a re-review can target the open findings:

```text
[R496] UNCLEAN Conformance - F1 open. Examined and found sound: sw/mailbox/mailbox.yaml (one byte-order statement, lines 21-26; frame offsets vs IEEE 1722.1-2021 Fig. 6-1/8-x/9-x: ADP entity_id @18, ACMP talker @34/listener @42, AECP target @18, MAAP requested_start @26; EtherTypes 0x22F0/0x22EA/0x88F5; subtypes FA/FB/FC/FE; ADP msg types 0/1/2); sw/firmware/ctrl/adp/adp.c:61-92 (ADPDU 68 bytes, control_data_length 56, valid_time 10, available_index incremented after send and reset by DEPARTING per 6.2.2.15) and the state machine vs the processor's own Table 5.51 transcription (walk 320/320, cut from pinned protocol-processor 631eeb34, blob proved); latency bounds ADP_MBX_LAT_* re-derived (DISCOVER 1+25+1+3+1=31 etc.) and measured C0-C6; default build unchanged, proved by diff (receipts/default_build_identity.txt: 22/22 files equal for all five configs; receipts/builder_fragment_identity.txt: 50/50 builder outputs equal, git status clean); no heap (receipts/rv32_link_probe.txt).
[R496] UNCLEAN RTL - F4 open. Examined and found sound: KL_mbx.sv (one-cycle host answer, partial-strobe refusal, GM snapshot, ERR set-wins, IRQ OR of enabled levels), KL_mbx_rx.sv (classification at byte 14, speculative writes only into released space, header-then-head commit, token bucket), KL_mbx_tx.sv (record checks before a byte leaves, flush on refusal, tail after last byte, round-robin), KL_mbx_evt.sv (wrap-safe deadline compare, command beats scan, coalescing, 4-free-word posting), KL_mbx_ring.sv, KL_mbx_wb.sv, KL_mbx_axil.sv (VALID never depends on READY; payload held; write priority) - confirmed by receipts/adapter_stress_head.txt; Verilator -Wall lint clean apart from unused package parameters (receipts/verilator_wall_lint.txt); lint_rtl, xvlog gate (81 hdl/ files, 0 findings) and Yosys on the three tops pass (receipts/rtl_gates.txt); single clock, no CDC in F0.
[R496] UNCLEAN Robustness - F4 open. Examined and found sound: truncated/short/tagged/foreign frames (C4, F2), oversize and full-ring drops never touching an unread record (D0/D1, rx-free-space-off-by-one caught), malformed TX records (X1), stale timer tags (B1, walk S cells), driver resync on a bad RX record, pool double/interior/foreign free and calloc overflow, debug-sink truncation, loop per-pass bounds.
[R496] UNCLEAN Tests - F1, F2, F3, F4, F5 open. Examined and reproduced at the head: make -C tb/verilator/mbx (120+120+13, quick mutants 4/4; receipts/mbx_suite_make.log), mutants.py 30/30 after both controls (receipts/mbx_mutants_30.log), test_ctrl_firmware.py --require-rv32 --self-test --lwsrp (7 arms, 618 checks, 28/28; receipts/ctrl_firmware_selftest_lwsrp.log), gen_mailbox.py --check --crosscheck and --selftest (16 ok) plus five reviewer-planted mismatches outside the self-test fixtures all caught (receipts/gen_mismatch_probe.log).
[R496] UNCLEAN Docs - F3, F5, F6 open. Examined: docs/design/MAILBOX_SPLIT.md, docs/reference/MAILBOX_CONTRACT.md (generated, --check clean), sw/firmware/ctrl/README.md, tb/verilator/mbx/README.md, hdl/milan/mailbox/README-tests.md, docs/README.md, MODULE_MATRIX.md; docs_check, check_em_dash --base fa450d30, gen_toc --check/--verify-anchors, check_doc_paths, gen_module_matrix --check all rc 0 (receipts/fast_gates.log).
```

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | mailbox.yaml, adp/adp.c, adp/adp_mbx.h, ctrl_reuse.py + adp_walk.cpp, milan_soc.py switch, the export and builder identity receipts | R496-1 | 0bfef4987eede4b022b17c7b2f56d079ff84893b |
| RTL | UNCLEAN (F4) | hdl/milan/mailbox/*.sv (8 files), tb_mbx_top.sv, lint, xvlog, Yosys, adapter stress | R496-1 | 0bfef4987eede4b022b17c7b2f56d079ff84893b |
| Robustness | UNCLEAN (F4) | KL_mbx_rx/tx/evt guards, mbx.c resync, ctrl_pool.c, ctrl_debug.c, ctrl_loop.c, ring boundary mutants | R496-1 | 0bfef4987eede4b022b17c7b2f56d079ff84893b |
| Tests | UNCLEAN (F1, F2, F3, F4, F5) | suite.hpp, bench.hpp, mutants.py, ctrl_arms.py, ctrl_mutants.py, test_adp.c, test_port_loop.c, lwsrp_port.c, gen_mailbox.py self-test, ci_scope self-test, hosted check runs | R496-1 | 0bfef4987eede4b022b17c7b2f56d079ff84893b |
| Docs | UNCLEAN (F3, F5, F6) | MAILBOX_SPLIT.md, MAILBOX_CONTRACT.md, READMEs, PR body, REVIEW READY, HANDOFF | R496-1 | 0bfef4987eede4b022b17c7b2f56d079ff84893b |

No lens is banked clean at this head. A fix commit changes artifacts within every lens's scope, so all five need coverage again at the corrected head.

## What I ran (all at the exact head, in disposable copies; rc 0 unless noted)

| Command or probe | Result |
|---|---|
| `make -C tb/verilator/mbx` (pinned Verilator 5.050, identity checked) | 120 / 120 / 13 checks, 0 failures; quick mutants 4 of 4 |
| `tb/verilator/mbx/mutants.py --jobs 6` | both controls ok; 30 of 30 caught |
| `test_ctrl_firmware.py --require-rv32 --self-test --lwsrp <lwSRP 19f5796b>` | model 120, port 72, adp 47, walk 320, entity 45, rv32 1, lwsrp 13; 28 of 28 caught |
| `gen_mailbox.py --check --crosscheck`; `--selftest` | 0 findings; 16 ok |
| `scripts/gen_mismatch_probe.sh` | 5 of 5 out-of-fixture mismatches caught; gates clean after restore |
| `scripts/ci_scope.py --selftest` | **rc 1** (F1) |
| `scripts/default_build_identity.sh` + `normcmp.py` | base vs head: 22/22 files equal, AX7101 at shipping argv and all five configs at the Arty 100 MHz proxy; Arty at 83.333 MHz refused identically at base, head and switch-on |
| `scripts/builder_fragment_identity.sh` | 50 of 50 builder outputs equal; tracked tree clean |
| switch-on vs off (`receipts/switch_on_additions.txt`) | adds the region at 0x90100000, CSR bank 0xf000f000 (loc 30), IRQ 3 and 7 sources; no bank moves; CPU netlist changes (F6) |
| `scripts/rv32_link_probe.sh` | full -nostdlib RV32I image links with only memcpy/memset/vsnprintf supplied: 0 undefined, 0 heap/OS symbols; firmware text 11,080 B, bss 163 B |
| `lint_rtl.py --check`; Verilator `-Wall --lint-only` per mailbox module; `xvlog_gate.py --check` (alone); `syn/yosys/run.sh` on the three tops | PASS; clean except UNUSEDPARAM; PASS (0 hdl/ findings); 3 PASS |
| `scripts/axil_stress/run.sh` | AXI4-Lite 14/14, Wishbone 3/3 on the head |
| `scripts/adapter_mutants.sh` | 4 of 4 AXI4-Lite defects survive the suite; all caught by the stress probe (F2) |
| `scripts/ring_boundary_mutants.py` | 5 caught, 2 survive (F4) |
| `scripts/lwsrp_pin_probe.sh`; `scripts/own_discover_probe.sh` | dirty lwSRP accepted (F3); own-DISCOVER defect caught by existing checks, with no planted arm (F5) |
| docs, source-list, hygiene and idiom gates (`receipts/fast_gates.log`) | all rc 0 (the two Markdown gates run with the pinned renderer venv) |

## Real limits

- Physical calibration was NOT RUN, and no hardware was used; field skips are not hardware proof.
- I did not reproduce the switch-on OOC area (2,756 LUT, 2,713 FF, 1 RAMB36 + 10 RAMB18, WNS +0.311 ns). The figure rests on the author's evidence.
- This host's LiteX checkout refuses the three Arty configs at 83.333 MHz, at base and head alike. Their default-build identity is proven at a 100 MHz proxy only.
- Latency bounds are in mailbox accesses. No CPU-cycle figure exists; the author lists this as an open item.
- The IEEE 1722.1-2021 and Milan v1.2 texts were not available locally. I judged ADP conformance against the clause structure the PR cites, the processor's reviewed Table 5.51 transcription and frame builder, and the processor's compliance notes.
- Not run, by instruction: the full parent, protocol-processor, gPTP, Yosys and builder banks; act or the host act runner; hosted re-runs. I read the hosted state only through the read-only API.
- The review clone was never edited. Five `__pycache__` directories that my `--help` and import runs created were removed. Tracked blobs, modes, the index and the submodule gitlinks match the head (`receipts/clone_restore_verification.txt`).

## Pending manager duties

- After the fixes: a new exact head, the act-first replica, and hosted `changes`, `rtl-fast`, `verilator-suites` and `yosys-portability` executed and green at that head (F1).
- Re-review of every lens at the corrected head; coverage cannot carry over (section 7).
- The final current-dev candidate merge validation and post-merge containment.
- Carry S1 (CI wiring) to its own issue if accepted.

R496-1 FINISHED
