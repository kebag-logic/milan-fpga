[R291] POSITIVE - exact head 2e1675d2d20bbc0bb549b36b9d485b2f9b747d5f

# R291-3 independent external review: processor issue #94 / PR #110, round 2

- **Exact head:** `2e1675d2d20bbc0bb549b36b9d485b2f9b747d5f`, tree `b83ba761298a353d80c2f48bc178764615525e1d`. The PR's GitHub head matches.
- **Diff reviewed:** from source base `008edbbf486598ae237414273d75e385cf0e1a56`, with the round-2 delta taken from round-1b head `cc077a6ffe20585d20b116f008e07189ba1bb7f8`.
- **Clone:** a detached, isolated clone. It is verified at exact-head bytes at the end of the review (`receipts/clone-integrity.txt`):
  - HEAD, the HEAD tree and the index tree are all `b83ba761…`.
  - The worktree and index equal HEAD, with zero untracked or ignored entries.
  - Every tracked blob re-hashes to its index id, and every file mode matches.
  - The repository has no gitlinks and no `.gitmodules`, so there are no submodule gitlinks to verify.
- **Probes:** every probe ran in disposable clones under the packet's `scratch/`. The reviewed clone was only read.
- **Simulator:** the scoped Verilator 5.050 wrapper, identity recorded in `receipts/identity.txt`:
  - wrapper sha256 `905795b9…`
  - it reports `Verilator 5.050 2026-07-01 rev v5.050`
- **Verdict:** POSITIVE. No MINOR, MAJOR or BLOCKER finding is open, and all five lenses are clean. There are two optional SUGGESTIONs.

## 1. Reconstruction (public state only)

1. **House rules.** There is no `AGENTS.md` or `CONTRIBUTING.md` at this head. I read these conventions instead:
   - `README.md`
   - `docs/README.md`: single-source figure rules and the editing workflow (`make check` before commit)
   - `docs/diagrams/README.md`: hand-authored SVGs are the source. Every change must be rendered to PNG and looked at.
2. **Issue #94.**
   - The body holds the frozen T9 acceptance.
   - Manager scope decision (issue comment 5810666541). This PR delivers the guard and four standalone acceptance items:
     - the late-beat case, including the hold-deleted mutant and recovery
     - the stuck-memory bound
     - the store suites staying green, with a hard-reset-only guard
     - out-of-context area against T9's 5 LUT / 1 FF
   - The D3 roll-back cases are deferred. `debt_o` is documented as their interface.
3. **Port decision** (PR comment 5811722803). `debt_o` stays on the guard module only, and `protocol_processor_top`'s ports stay unchanged for the parent instantiation.
4. **Round-2 assignment [A252]** (issue comment 5812432287):
   - re-render the PNGs of figures 22 (1950 px) and 20 (2040 px) from the head SVGs, look at them, and commit them
   - optionally, R291-2 S1-S4
   - no other change
5. **The diff.** I read `git diff 008edbbf..2e1675d2` in full: 22 files, +889/−54. I also read the history `4f525eb5` → `cc077a6f` → `2e1675d2`.
6. **Public evidence.** I read the author round-2 result files under `kebag-logic/milan-fpga@c23839d5:review-evidence/pp94-r1/author-r2/`: source state, parent results and state, priority results, diagram verification, and the priority mutant diff. I did not open the `reviews/` subtree of that evidence.
7. **Prior findings.** I read the prior public findings (R290-2, R291-2) only after my own pass and my probes were complete. See §4.

## 2. Executed evidence (reviewer-owned)

The scripts are `run_probes.sh` and `probe_top_nohold.sh`. Return codes are in `receipts/rc.txt`.

| Probe | Result | Receipt |
|---|---|---|
| Round-2 scope `cc077a6f..2e1675d2` | Exactly 8 files: two PNGs, two SVGs, `integrator.md`, the top (−1 blank line), the guard bench README (+1) and `sim_main.cpp` (+8). Nothing else changed. | `round2-scope.txt` |
| `git diff --check 008edbbf 2e1675d2` | rc 0 | `diff-check.log` |
| Re-render every hand-authored SVG at its committed PNG width | 20 at 2040, 21 at 2010, 22 at 1950, 23 at 2040, 24 at 2040: all **byte-identical** to the committed PNGs. The old PNG blob of figure 20 (the same at base and at `cc077a6f`) differs from the new one. | `png-render.txt` |
| Guard suite (`make -C tb/desc_mem_guard`) | 78 checks: 78 PASS, 0 FAIL. The late case's third locate gets its own bytes `0005000011223344 5566778899aabbcc`, with overlap-accepts=0. In the stuck case, 5 locates answer errors, max 4,102 cycles against a bound of 4,160, with debt=1. | `guard-suite.log` |
| Unguarded reproduction (`make … baseline`) | 18 checks, 17 PASS, 1 FAIL. `third locate late_beats_never_served` gets `00060000deadbeef cafef00d01234567`. make rc 2. | `guard-baseline.log` |
| Hold-deleted mutation control (`mutate.py`) | Controller rc 0, "detected=True". The mutant fails the same completed byte assertion with the same wrong bytes. | `guard-hold-mutant*.log` |
| **Inverted-priority mutant** (the terminal-beat clear moved above acceptance; reviewer-authored, `prio-mutant.diff`) on the head bench | 78 checks, **77 PASS, 1 FAIL**: exactly `request acceptance must win over a coincident stray terminal beat`. The late and stuck scenarios completed. make rc 2. | `prio-mutant-head.log` |
| The same mutant on the round-1b bench (`cc077a6f`) | 77 checks, 77 PASS, rc 0. The new assertion is the only thing that detects it. | `prio-mutant-prior-bench.log` |
| Descriptor-store suite | 584 PASS, 0 FAIL | `desc-store-suite.log` |
| Product-top suite | 1,454 PASS, 0 FAIL. This includes A12 (wire-level late burst) and A13 (unterminated burst). | `pp-top-suite.log` |
| Product-top bench with both guard holds deleted (disposable tree, restored afterwards) | 1,434 checks, 5 failures. The scenarios completed. One failure is `A12: late STREAM_OUTPUT bytes reached STREAM_INPUT on the wire`, and A13 detects the forgotten debt. make rc 2. The tree was restored: 0 modified tracked files. | `top-nohold*.txt/log` |
| Lint (repository rule set: `-Wall`, whole tree visible) of `KL_aecp_desc_mem_guard` and `protocol_processor_top` | rc 0 for both, no warnings | `lint-*.log` |
| `make check` (lint, WaveDrom, links, requirement matrix, module matrix, stale) and `gen_matrix.py --check` | rc 0 | `make-check.log`, `gen-matrix.log` |
| `protocol_processor_top` port block (`module` … `);`) compared with base | Byte-identical, empty diff. The top is changed only at hunks @3206 and @3275. | `top-port-block.*` |
| Hosted check runs at the exact head (read only) | Two workflow runs. The first has docs-gates, portability and suites **success**. In the second, docs-gates and portability are success and suites was **in progress** when observed; the combined status was `pending`. | `hosted-check-runs.txt` |

## 3. Lens analysis

### Conformance: CLEAN
- **Round-2 assignment.** The F1 re-render is done at the mandated widths: 22 at 1950×1440 and 20 at 2040×1380, both byte-identical to a fresh render of the head SVG. S1-S4 are all taken. No other file changed (`round2-scope.txt`).
- **Scope decision (#94 comment 5810666541).** Every item is met at this head:
  - **Late-beat case:** the guarded run gets its own bytes and recovers. Deleting the hold fails the completed byte assertion, standalone and at the product top.
  - **Stuck memory:** errors arrive within the bound while debt holds requests.
  - **Store suites:** green (584/584).
  - **Hard reset only:** the guard's `rst_n` is the top's `rst_n` (`protocol_processor_top.sv:3219-3220`), and the bench proves that debt survives a store-only reset.
  - **Area:** the committed OOC measurement (4 LUT, 1 FF, `syn/ooc/README.md`) is prior post-synthesis evidence for the unchanged guard RTL. I did not re-run it (see §7).
- **D3 deferral.** It matches the decision. `debt_o` is documented as the D3 interface in 07 §3.3.1 and integrator §4.1. The top's port list is byte-identical to base, so the parent instantiation is unaffected (port decision 5811722803).

### RTL: CLEAN
- **Guard** (`hdl/aecp/KL_aecp_desc_mem_guard.sv:56-80`):
  - `owed_r` is set on `m_req_valid_o && m_req_ready_i` and cleared on a consumed `last|err`. Acceptance has priority.
  - Both request arms are gated by `!owed_r`, and there is no combinational loop: `m_req_valid_o` does not depend on ready.
  - The response path is pure pass-through.
  - The store's `mem_rsp_ready_o` is tied 1 (`KL_aecp_desc_store.sv:351`), so abandoned beats always drain.
- **Round-2 RTL delta.** The only RTL change is the removed blank line at `protocol_processor_top.sv:246` (S1). The port block is now byte-identical to base.
- **Guard logic** is unchanged since `4f525eb5`.

### Robustness: CLEAN
- **Coincident stray terminal beat.** A stray terminal beat in the acceptance cycle keeps the new debt. That is the safe outcome for an unflushed path after hard reset, and it is now pinned: the inverted mutant fails exactly one new assertion.
- **Never-ending burst.** Locates stay bounded (4,102 ≤ 4,160 cycles standalone; A13 at the top).
- **Integrator obligations** are documented: a hard reset must flush the descriptor-memory path, and no beats may follow `err`.
- **Remaining D3 exposures** (owner hold, deadline to CLOSED) are the deferred lane's, per the decision.

### Tests: CLEAN
- **New assertion** (`tb/desc_mem_guard/sim_main.cpp:327-333`):
  - The preconditions are established by the preceding checks: no debt, response valid and ready, `mem_req_ready_i` still 1.
  - The new assertion detects the inverted-priority mutant on the head bench and is absent from the round-1b bench, which the mutant passes (77/77).
  - Detection is a completed assertion, not a crash.
- **Existing controls re-executed:** baseline, hold mutant, store suite, product top, and a top-level hold-deleted probe that completes its scenarios and fails A12/A13.

### Docs: CLEAN
- **Figure 20** (viewed at its committed size):
  - The guard is a solid processor-module box with the text "at processor top · hard reset only". The engine's descriptor master arrow enters it, and a `desc_mem_*` arrow goes on to "integrator main memory".
  - The response-buffer master bypasses it to memory.
  - The subtitle now distinguishes processor boxes from external main memory.
  - I saw no clipped text or labels escaping their boxes.
- **Figure 22:**
  - The guard box sits between step 4 and the descriptor image, in the memory-face column, with the arrow to the image header. The descriptor-image box is reflowed to fit.
  - The module list includes `KL_aecp_desc_mem_guard.sv` and the suite list includes `tb/desc_mem_guard`.
  - I saw no overlap.
- **Integrator reset text** (`docs/guides/integrator.md:136-139`, S4). It now addresses `protocol_processor_top.rst_n`, a real top port (`protocol_processor_top.sv:109`). It is consistent with integrator §1 ("exactly one clock and one reset") and with the RTL banner's guard-internal rule.
- **Bench README** (`tb/desc_mem_guard/README.md:25`) records the new property.
- **Doc gates** pass.

## 4. Prior public findings on this PR, resolved at this head

I read these only after completing my own pass and probes.

| Prior finding | State at `2e1675d2` | Reviewer evidence |
|---|---|---|
| R290-2 F1 = R291-2 F1 (MINOR, Docs): PNGs of figures 20 and 22 were stale against their SVGs | **Resolved** | The PNG blobs changed (20: `cd2525f5` → `f030f10b`; 22: `abe76f52` → `57849c9c`). A fresh render at 2040 / 1950 px is byte-identical to each committed PNG (`png-render.txt`). Visual check: the guard box and the module and suite lists are present in 22, and the guard box is present in 20. `make check` rc 0. |
| R291-2 S1 (blank line in the top port block) | **Resolved** | The port block is byte-identical to base (`top-port-block.diff` is empty). |
| R291-2 S2 (acceptance-over-clear priority unpinned) | **Resolved** | `sim_main.cpp:327-333`. The inverted mutant gives 77/1 on the head bench at exactly the new assertion, and 77/77 on the round-1b bench. |
| R291-2 S3 (guard placement in the figures) | **Resolved** | In both figures the guard is drawn as a processor module on the path to memory. The response-buffer master bypasses it in 20. |
| R291-2 S4 (reset instruction addressed to an unreachable wire) | **Resolved** | `integrator.md:136-139` now instructs on `protocol_processor_top.rst_n`. |
| Round-1 parent-gate failures (C++ and Python idiom, `PINMISSING`; manager comment 5811722803) | **Remain resolved** | The top port block is unchanged from base. At this head the round-2 changes to C++/Python are 8 lines of plain assignments and `CHECK` calls. The parent idiom gates at this head are the manager's receipts. |

## 5. Findings

No MINOR, MAJOR or BLOCKER finding.

### SG1: SUGGESTION, Tests: the priority mutant has no in-repo controller
- **Where:** `tb/desc_mem_guard/mutate.py` (hold mutant only) and the README mutation table at `tb/desc_mem_guard/README.md:48-52`.
- **Evidence:** the inverted-priority control exists only in the author's evidence packet (`check-priority-mutant.py`, `KL_aecp_desc_mem_guard.clear_priority.sv`). I reproduced it independently (`receipts/prio-mutant.diff`, `prio-mutant-head.log`).
- **Impact:** a future edit to the priority is caught by the new assertion, but the repository alone cannot re-demonstrate that the assertion discriminates.
- **Suggested outcome:** add an optional `--priority` mode to `mutate.py` and a row to the README table.
- **Verification:** the new controller returns 0 only on the single expected FAIL.

### SG2: SUGGESTION, Docs: figure 20 has a tight parallel run beside the SRP line
- **Where:** `docs/diagrams/20-rtl-dataflow.svg:133` (new response-buffer path, vertical at x=976) and `:153` (existing SRP path, vertical at x=964).
- **Evidence:**
  - Between y=452 and y=492 the two verticals run 12 px apart.
  - The response-buffer horizontal at y=452 crosses the SRP vertical.
  - The committed render is legible because the colours differ (purple and teal).
  - The diagrams README's routing guidance asks for parallel runs spaced at least 20 px.
- **Suggested outcome:** at the next edit of figure 20, move the response-buffer vertical to x≥984, or the SRP vertical left.
- **Verification:** re-render and look.

## 6. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #94 body and decisions 5810666541 and 5812432287; port decision 5811722803; round-2 scope diff; top port block compared with base; `syn/ooc/README.md` | R291-3 | `2e1675d2d20bbc0bb549b36b9d485b2f9b747d5f` |
| RTL | CLEAN | `hdl/aecp/KL_aecp_desc_mem_guard.sv`; `hdl/top/protocol_processor_top.sv` (port block, guard instance, engine rewiring); `KL_aecp_desc_store.sv` (banner, rsp_ready); lint of the guard and the top | R291-3 | `2e1675d2d20bbc0bb549b36b9d485b2f9b747d5f` |
| Robustness | CLEAN | Priority semantics; stray-terminal, stuck and late cases; hard and store-only reset; the top-level no-hold probe | R291-3 | `2e1675d2d20bbc0bb549b36b9d485b2f9b747d5f` |
| Tests | CLEAN | `tb/desc_mem_guard/{sim_main.cpp,wrap.sv,Makefile,mutate.py}`; `tb/pp_top` A12/A13; executed guard (78/78), baseline, hold mutant, inverted-priority mutant on the head and round-1b benches, desc_store 584/584, pp_top 1,454/1,454 | R291-3 | `2e1675d2d20bbc0bb549b36b9d485b2f9b747d5f` |
| Docs | CLEAN | Figures 20 and 22 (SVG and PNG, viewed); re-render of all five hand-authored figures; `docs/guides/integrator.md` §4.1; `07_memory_maps.md` §3.3.1; guard and top bench READMEs; `MODULE_MATRIX.md`; `make check` | R291-3 | `2e1675d2d20bbc0bb549b36b9d485b2f9b747d5f` |

## 7. Real limits and pending manager duties

**Not run by this reviewer:**
- the full parent, processor, gPTP, Yosys or builder banks
- the full `run_suites.sh` bank (I ran only the guard, desc_store and pp_top suites)
- the NVM figure gate
- the portability gate
- out-of-context synthesis. The 4 LUT / 1 FF figure is the author's prior post-synthesis evidence on unchanged guard RTL.
- Docker/act and hosted acceptance

**Manager duties, still pending:**
- **Donor and parent consumer banks at this head.** These are the manager's receipts: idiom gates, `xvlog_gate`, `check_rtl_source_lists`, `pp_shadow`, and the gitlink-dependent `pp_srcs` / `test_builder`. The author's round-2 parent results show rc 0 for five parent gates, but that is author evidence, not a manager receipt.
- **The final current-dev candidate at the merge turn** (source base `008edbbf`, live dev `eaf0e6c4`). Source validation at this head is separate from that candidate.
- **Hosted acceptance.** One hosted `suites` job was still in progress when observed.
- **Publication** of this packet.

**Hardware:** physical calibration was NOT RUN, and field skips are not hardware proof. No hardware, timing-closure or silicon claim is made.

**D3 deferral:** the D3 roll-back cases (owners held while debt is set, deadline to CLOSED, the 5,000/16,000-cycle cases, the owner-release mutant) remain deferred to the D3 lane by manager decision, and are not covered by this review.

**Receipts:** they are in `receipts/`, and the scripts are `run_probes.sh` and `probe_top_nohold.sh`, all listed in `MANIFEST.sha256`. Home-directory prefixes in logs are shown as `~`.

R291-3 FINISHED
