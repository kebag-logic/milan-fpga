[R291] NEGATIVE - exact head cc077a6ffe20585d20b116f008e07189ba1bb7f8

# R291-2 independent external review: processor issue #94 / PR #110

- Exact head `cc077a6ffe20585d20b116f008e07189ba1bb7f8`, tree `caa8229363824fcafd939fbaecdbdf62fb9160a1`.
  The diff was reviewed against source base `008edbbf486598ae237414273d75e385cf0e1a56`, commits `4f525eb5` (round 1) and `cc077a6f` (round 1b).
- The review used a detached isolated clone. At the end it was verified at exact-head bytes: HEAD, tree and index tree match, the worktree and index equal HEAD, and there are zero untracked or ignored entries. The processor repository has no gitlinks and no `.gitmodules` (`receipts/clone-integrity.txt`).
- Scoped simulator: Verilator 5.050 (`receipts/tool-identity.txt`).
- The verdict is NEGATIVE because of one open MINOR finding under the Docs lens (F1). The RTL, Conformance, Robustness and Tests lenses are clean at this head. There are four optional SUGGESTIONs.

## 1. Reconstruction (public state only)

1. **House rules.** The processor repository has no `AGENTS.md` or `CONTRIBUTING.md` at this head. I read its own conventions in `README.md`, `docs/README.md` (single-source and figure rules), `hdl/README.md` and `docs/diagrams/README.md`. I also read the parent's `AGENTS.md` §6-§7 (the lenses, severities and completion ledger) and `CONTRIBUTING.md` §5-§6 at parent dev `9d328810`. The parent's em-dash gate diffs only parent-tracked Markdown, so it does not bind this repository.
2. **Issue #94.** I read the body (frozen acceptance) and the immutable T9 ticket it cites (`c1ee27d8`).
   - The manager's scope decision (issue comment 5810666541) delivers the guard and its standalone acceptance. It defers the D3 roll-back cases.
   - The manager's port decision (PR comment 5811722803) keeps `debt_o` on the guard port and does not route it to `protocol_processor_top` until the D3 lane. The round-1b assignment covers only the parent C++ (Rule 11) and Python (Rule 12) idiom findings and the `PINMISSING` build stop.
3. **Interface authorities.** `docs/guides/integrator.md` §4.1 and `docs/architecture/07_memory_maps.md` §3.3.1. The `KL_aecp_desc_store` memory bookkeeping and watchdog (`hdl/aecp/KL_aecp_desc_store.sv:344-351,621-636`). The parent consumer's descriptor-memory path at `9d328810` (`sw/litex/milan_soc.py`, the descmem CDC lanes, with `rsp_ready` tied 1).
4. **Diff and history.** All 20 files of `008edbbf..cc077a6f` and the round-1b delta `4f525eb5..cc077a6f`. The guard RTL is byte-identical between the two rounds.
5. **Public evidence.** The `review-evidence/pp94-r1` tree at `802e90eb` (MANIFEST plus the author and round-1b receipts). Exact-head hosted runs.
   - The PR and issue carry no manager evidence comment containing parent-gate receipts at this head (see §6).
   - There were no prior public review FINDINGS on this PR. R290-1 and R291-1 were voided before a verdict, so there was nothing to resolve or retain.

## 2. Executed evidence (reviewer-owned, exact-head export, never the clone)

| Probe | Result | Receipt |
|---|---|---|
| Guard suite (`make -C tb/desc_mem_guard`) | rc 0, 77 checks: 77 PASS, 0 FAIL. Late case: third locate presented at 4185 while the old burst was owed (first late beat at 6080), served its own bytes `0005000011223344 5566778899aabbcc`, held 1895 cycles, 0 overlap accepts. Stuck case: 5 errors, max 4102 of the 4160 bound, debt held | `receipts/guard-suite.log` |
| Unguarded baseline (`make baseline`) | rc 2, 18 checks: 17 PASS, 1 FAIL. The third locate received `00060000deadbeef cafef00d01234567` (STREAM_OUTPUT), 1 overlap accept | `receipts/guard-baseline.log` |
| Shipped hold-deleted control (`mutate.py`) | rc 0 (detected): the mutant's make rc is 2, with the exact completed byte assertion and the same wrong bytes | `receipts/guard-mutate-ctl*.log` |
| Store suite (`tb/desc_store`) | rc 0, 584/584 | `receipts/desc-store-suite.log` |
| Product-top suite (`tb/pp_top`, including A12/A13) | rc 0, 1454/1454 | `receipts/pp-top-suite.log` |
| Reviewer mutants over the full guard suite: M1 valid-hold deleted, M2 ready-hold deleted, M3 clear on `last` only, M4 clear ignores `rsp_ready`, M5 clear on any beat, M6 `debt_o` tied 0, M9 debt never set | all killed (rc 2; 18/4/4/4/11/15/19 FAIL) | `receipts/mut-*.{diff,log}`, `receipts/mut-rc.txt` |
| M7: the wrapper wires the store-only reset into the guard | killed (9 FAIL, including "store-only reset cleared memory debt") | `receipts/mut-M7_*` |
| M10: product top with both holds deleted, full `pp_top` | killed: `A12: late STREAM_OUTPUT bytes reached STREAM_INPUT on the wire`, plus the A12/A13 debt checks (5 failures) | `receipts/mut-M10_*` |
| M8: terminal-beat clear given priority over acceptance | **survives** (77/77), see S2 | `receipts/mut-M8_*` |
| Focused lint, repository flags: guard, store, `protocol_processor_top`; guard alone under full `-Wall` | 0 findings each | `receipts/focused-lint.log` |
| Documentation gates: links, requirement matrix, generated module matrix, `make stale`, `git diff --check` base..head | all rc 0 | `receipts/doc-gates.log` |
| Guard-only portability (sv2v + yosys) and open-tool area cross-check (`synth_xilinx`, xc7) | elaborates; 5 LUT (2 LUT2, LUT3, LUT5, LUT6) + 1 FDRE. The published Vivado OOC report reads 4 Slice LUTs / 1 FF / 0 RAM / 0 DSP on xc7a100tfgg484-2. Both are within T9's 5 LUT / 1 FF | `receipts/guard-portability-area.log` |
| Parent Rule 11/12 scanners (parent `9d328810` copies, per-file `scan()` only) on the changed benches | head: 0 findings in `tb/desc_mem_guard/sim_main.cpp`, `tb/pp_top/sim_main.cpp` and `mutate.py`, and the Makefile warning flags are present. Positive control at `4f525eb5`: 10 c-style casts, 1 file-scope mutable, 6 multi-declarators, 1 unannotated and 1 undocumented public function, exactly the reported findings | `receipts/idiom-scan.log`, `receipts/parent-scanner-digests.txt` |
| Product-top port list, base vs head | 205 ports, identical. No `desc_mem_debt_o` port, so the parent instantiation is unaffected | §3 RTL |
| Hosted runs at exact head (push 35984790239, pull_request 35984794725) | all six jobs executed and succeeded (docs-gates, suites, portability ×2), none skipped. The suites log shows Verilator 5.050, `LINT OK KL_aecp_desc_mem_guard`, desc_mem_guard 77, desc_store 584, pp_top 1454, and 15894 checks total with 0 failing | `receipts/hosted-check-runs.txt` |
| Diagram exports | the SVGs of figures 20 and 22 changed while both PNG blobs are unchanged | `receipts/diagram-png-staleness.txt`, `receipts/diagram-png-history.txt`, `receipts/renders/` |

The scripts are in `scripts/` (00 environment, 01 suites/baseline/control, 02 mutants, 03 M8, 04 lint, 05 doc gates, 06 portability/area, 07 idiom scan, 08 scanner fetch). At most 8 parallel jobs were used, all run in the foreground.

## 3. Lens analysis

**Conformance.** Each acceptance line from the issue body and the manager's scope decision is met by executed evidence:
- **Late-beat case.** The locate is answered with its own bytes, never another burst's. The unguarded baseline and the hold-deleted mutant fail the completed byte assertion. Service recovers after the drain (guard suite, and `pp_top` A12 on the wire).
- **Stuck memory.** Requests stay held and every locate gets a bounded error, `NO_SUCH_DESCRIPTOR` on the wire (A13).
- **Existing suites.** The store suite is green, and the store RTL change is comments only (`KL_aecp_desc_store.sv:27-30`).
- **Reset.** The guard's reset is the hard reset alone (`protocol_processor_top.sv` guard instance `.rst_n(rst_n)`). M7 proves the bench detects a store-reset connection.
- **Area.** Area is measured against T9.
- **`debt_o`.** It stays on the guard port as the documented D3 interface, per the port decision. The D3 roll-back cases are deferred by scope decision 5810666541 and are not claimed.

The T9 seam semantics are realised exactly: set on accepted request, cleared on consumed `last` or `err`, requests held on both arms, responses passed through.

**RTL** (`hdl/aecp/KL_aecp_desc_mem_guard.sv:56-80`):
- One flop with a synchronous active-low reset, matching the store's reset style. The request holds are purely combinational, and the guard never withdraws a presented request: `m_req_valid_o` falls only when `owed_r` rises, which requires a handshake.
- No combinational loop is added. `s_req_ready_o` already followed `m_req_ready_i` combinationally before the guard.
- Widths pass through unchanged (32-bit address, 9-bit beats, 64-bit data).
- Acceptance has priority over the terminal clear, which is the conservative choice for an unowed terminal beat.
- The store ties `mem_rsp_ready_o` to 1 and discards beats while `!mem_busy_r` (`KL_aecp_desc_store.sv:344,351`), so a late burst always drains.
- The documented assumptions pre-date this PR or are satisfied by the parent path. The first response comes after acceptance, which the store already required (`mem_busy_r` is registered). The error beat is terminal, which T9 records for the bridge.
- The top-level port list is unchanged; `debt_o` lands on `desc_mem_debt_nc_w`.
- No open finding. S1 is cosmetic.

**Robustness:**
- Watchdog paths: an abandoned fetch, a request held past the watchdog, and a never-ending burst.
- Reset during activity: store-only reset with debt, hard reset with debt and a flushed queue.
- Terminal error without `last`.
- Backpressured terminal beats; valid-less `last`/`err`; the next request held through the terminal cycle.
- Stray beats with no debt.
- Recovery after every one of these.

All are exercised, and M3-M7 and M9 show the checks bite. The unowed-terminal-coincident-with-acceptance ordering is outside the documented contract and unpinned (S2). The parent's hard-reset flush obligation is a pending manager/D3 duty (§6), not a defect of this head.

**Tests:**
- Every new test demonstrably fails for the defect it names: the baseline, the shipped control, M1-M7, M9 and M10.
- The fixture is independent of the implementation (image bytes and FIFO transaction counts).
- Real integration wiring is tested at the product top through wire-level READ_DESCRIPTOR (A12/A13), observing debt hierarchically without a new port.
- Existing regressions are green locally and in hosted runs.
- The `pp_top` memory model changed from ready-only-when-idle to an always-ready in-order FIFO. With the guard in place the store sees the same request/response sequence as before, and the standalone suite keeps a ready-low case (`sim_main.cpp:269-272`), so no coverage is lost.
- The round-1b bench refactor keeps the 77-check population, and the parent idiom counts are zero at file level.
- No open finding. S2 is a pinning suggestion.

**Docs:**
- The contract is stated in 07 §3.3.1 and integrator §4.1 with reciprocal anchors: debt semantics, hard-reset-only, the D3 interface, the flush and terminal-error obligations, and the unchanged watchdog quirk. `debt_o` was correctly withdrawn from F02.10 once it stopped being a top port.
- The module matrix is regenerated (46 modules, 0 untested).
- Coverage is documented in `tb/desc_mem_guard/README.md` and `tb/pp_top/README.md` A12/A13; the OOC flow and figure are in `syn/ooc/README.md`; `syn/yosys/run.sh` has the new top.
- The links, matrix and staleness gates pass.
- **Open: F1.** The committed PNG exports of the two edited figures were not re-rendered.

## 4. Findings

### F1: MINOR, Docs: committed PNG exports of figures 20 and 22 are stale against their edited SVGs

- **Where:**
  - `docs/diagrams/22-aecp-descriptor-fetch.png` (blob `abe76f52`, unchanged) versus `docs/diagrams/22-aecp-descriptor-fetch.svg:27,65-76,135-136,149-150` (changed).
  - `docs/diagrams/20-rtl-dataflow.png` (blob `cd2525f5`, unchanged) versus `docs/diagrams/20-rtl-dataflow.svg:128` (changed).
- **Authority and evidence:**
  - The repository commits a PNG render beside each hand-authored SVG "so a wiki can show them without a renderer" (commit `2ca216e`). It refreshes that render when the SVG changes: on this very base line, `f8d30ec` ("Render the dataflow diagram's PNG again now that it shows...", #92/#93) followed the SVG edits `3bde3c3`/`daab6a5` before merge (`receipts/diagram-png-history.txt`).
  - `docs/README.md` §3 requires one source per figure. The diagrams README calls these figures "drawn against the landed RTL".
  - At this head the PNG of figure 22 still shows the pre-guard contract: "one outstanding request ... rsp_last on the last beat", "req_ready tied 0 is LEGAL wiring", and module and suite lists without `KL_aecp_desc_mem_guard` or `tb/desc_mem_guard`. It has no guard box. The PNG of figure 20 lacks the guard label.
  - Compare `receipts/renders/*.head.png` (head SVGs rendered) with the committed PNGs (`receipts/diagram-png-staleness.txt`).
- **Impact:** a reader of the committed image, such as a renderer-less wiki, gets a descriptor-memory path with no isolation guard, contradicting the landed RTL and the SVG of the same figure. No gate catches it: `make stale` checks only `.drawio` against `.svg`.
- **Required outcome:** the committed PNGs of figures 20 and 22 match their head SVGs, re-rendered and visually checked as the diagrams README requires. Alternatively, the repository explicitly retires or declares the PNG copies so no stale export of the figure is published.
- **Verification:** both PNG blob ids change, and a render of each head SVG matches the committed PNG content (guard box and text present in 22, guard label in 20). The documentation gates stay green.

### S1: SUGGESTION, RTL, Docs: stray blank line left in the top's port block

- **Where:** `hdl/top/protocol_processor_top.sv:246-247`.
- **Evidence:** round 1b removed the `desc_mem_debt_o` port line but left an extra empty line, a pure whitespace delta versus base.
- **Suggested outcome:** drop it, so the port block is byte-identical to base apart from intended changes.

### S2: SUGGESTION, Tests, Robustness, RTL: acceptance-over-clear priority is unpinned

- **Where:** `hdl/aecp/KL_aecp_desc_mem_guard.sv:72-77`; `tb/desc_mem_guard/sim_main.cpp:255-326`.
- **Evidence:** M8 swaps the priority so a terminal beat clears debt in the same cycle a request is accepted, and passes all 77 checks. The difference appears only for an unowed terminal beat coincident with acceptance. That is outside the documented contract, but it is exactly what an unflushed memory path after hard reset would present. The shipped priority, where acceptance wins, is the safe one.
- **Suggested outcome:** a unit check in `handshake_case` that presents a stray terminal beat in the acceptance cycle and requires debt to be set afterwards.

### S3: SUGGESTION, Docs: figure placement of the guard

- **Where:** `docs/diagrams/20-rtl-dataflow.svg:128` and `:17`; `docs/diagrams/22-aecp-descriptor-fetch.svg:73-76`.
- **Evidence:** figure 20 says every solid box is a module under `hdl/`, yet the new top-level module appears only as text inside the external "integrator main memory" box. Figure 22 draws the guard below the memory box on a dashed stub, not between step 4 and the memory.
- **Suggested outcome:** draw the guard on the processor side of the memory arrow when F1 is re-rendered.

### S4: SUGGESTION, Docs: reset instruction addressed to a wire the integrator cannot reach

- **Where:** `docs/guides/integrator.md:136-137`.
- **Evidence:** "Connect the guard's synchronous active-low reset to the hard reset only" is written to an integrator, but the guard is inside `protocol_processor_top` and already receives the top's `rst_n`.
- **Suggested outcome:** state it as the integrator's obligation on the top: drive `rst_n` only from a hard reset that also flushes the descriptor-memory path, never from an entity disable or a store/roll-back reset. Keep the guard-internal rule in the RTL banner.

## 5. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #94 body and T9; scope decision 5810666541; port decision 5811722803; guard, top and store RTL; late, stuck, reset, terminal-error, area and `debt_o` evidence (§2) | R291-2 | cc077a6ffe20585d20b116f008e07189ba1bb7f8 |
| RTL | CLEAN (S1, S2 optional) | `KL_aecp_desc_mem_guard.sv`, `protocol_processor_top.sv` guard insertion and port list, store handshake/watchdog, focused lint, portability, both area reports | R291-2 | cc077a6ffe20585d20b116f008e07189ba1bb7f8 |
| Robustness | CLEAN (S2 optional) | watchdog, stuck, store-only/hard reset, err-terminal, backpressure and stray-beat paths; mutants M3-M9; parent memory path shape | R291-2 | cc077a6ffe20585d20b116f008e07189ba1bb7f8 |
| Tests | CLEAN (S2 optional) | `tb/desc_mem_guard/*`, `tb/pp_top` A12/A13 and model change, `tb/desc_store`; baseline, shipped control, M1-M10; parent Rule 11/12 file-level scan with control; hosted suites | R291-2 | cc077a6ffe20585d20b116f008e07189ba1bb7f8 |
| Docs | **UNCLEAN** (F1 open; S1, S3, S4 optional) | 07 §3.3.1, integrator §4.1, 02 F02.10 withdrawal, `MODULE_MATRIX.md`, suite READMEs, `syn/ooc/README.md`, figures 20/22 (SVG and PNG), documentation gates | R291-2 | cc077a6ffe20585d20b116f008e07189ba1bb7f8 |

## 6. Real limits and pending manager duties

- **Parent consumer gates at this head.** The parent Rule 11/12 C++/Python idiom gates, `xvlog_gate.py --check`, the `pp_shadow` build and the source-list gates with `cc077a6f` as the processor gitlink at parent dev `9d328810` are manager receipts. They are not present in the public evidence tree I read: the round-1b author receipts there show the idiom and xvlog gates REFUSED (rc 2) on the index pin, and `pp_shadow`/source lists rc 0. I verified the Rule 11/12 counts per file only, with a positive control. The full parent gates remain the manager's.
- **Not run here, by instruction.** Full processor, parent, gPTP, Yosys and builder banks, the nvm_port figure gate, the Vivado OOC re-run, Docker/act and hardware. The hosted exact-head runs executed the suites, lint, portability and docs gates successfully, and the manager owns hosted/act acceptance.
- **Merge-turn candidate.** Source validation here is distinct from the final current-dev candidate (source base `008edbbf`, live dev `9d328810`), which the manager builds at the merge turn.
- **Parent hard-reset flush.** The integrator obligation this PR documents (hard reset flushes the descriptor-memory CDC queues and bridge) was not verified in the parent. It belongs to the parent/D3 lane.
- **Deferred D3 scope.** The D3 roll-back cases (owners held while `debt_o` is set, deadline to CLOSED, the 5,000/16,000-cycle and slot-shape cases, the owner-release mutant) and the routing of `debt_o` to the top and parent are deferred by the scope and port decisions. Nothing here claims them.
- **Physical calibration.** NOT RUN. Field skips and post-synthesis area are not hardware proof.
- **Clone hygiene.** One empty untracked `abc.history`, written into the clone by my open-tool area probe, was removed. That probe now runs in scratch, and the clone was re-verified clean at exact head (`receipts/clone-integrity.txt`).

R291-2 FINISHED
