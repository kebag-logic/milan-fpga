[R501] NEGATIVE - exact head 7f8dc1b10c80c9e9631b8d6c6f5f37a039bc2e11

Round R501-2, external independent review of issue #665 / PR #669, F1.
Tree: `86236b61ec36ed252d6f91d698f2784302ef3743`.
Source base: `fa450d301805881ad713b67521477bf042ddadfd`.
Merged dev parent: `510fae60b26bef1db138de5cf2ac72b17b5011a5`.

All five lenses were applied. One MAJOR and two MINOR findings remain open. The round-1 implementation defects are addressed, but the new head is not clean. No RESIDUE is filed: the remaining documentation findings change numerical evidence or the governing selection rule, rather than wording alone.

The independent verdict and five-lens ledger were written before reading the other reviewer's report. Prior public findings were consulted only after the independent source pass. No private author material, other checkout, management directory, source fix or external write was used.

**R501-2-F1 - MAJOR - Conformance, RTL, Robustness, Tests**

Artifact: `sw/firmware/ctrl_nvm/nvm_store.c:295`, `:315`, `:421`, `:484`, `:562`; `test/nvm_checks.py:380`; `test/nvm_checks_write.py:427`. Receipts: `receipts/edge-endstation_ax7101_1x1_tdm8.log` and `receipts/edge-endstation_ax7101_8x8.log`.

Authority/evidence: the frozen F1 scope requires write-back on change, failure handling and the FASTCONNECT section 7 durability contract. A successful, verified promotion must survive a clean reboot. With an intact slot A at SEQ 5 and B blank, inject one failed boot read of A. Boot accepts neither slot and leaves the authoritative sequence at zero. An accepted changed value is then committed into B at SEQ 1. Both shapes report `ok=1 seq=1 auth=1 stale=0 dirty=0 pending=0`. On the next fault-free boot, both containers pass validation, A=5 wins over B=1, and the changed value is absent: `seq_a=5 seq_b=1 seq=5 auth=0`.

Impact: a transient read fault followed by a fully verified commit loses that committed state on the next boot. This is also the failure the executor publicly raised in issue comment 5997533145. Recording it for another Issue does not resolve the defect in this new module; AGENTS section 7 explicitly excludes that form of approval.

Required outcome: a commit after boot refusal must not claim successful authority when a surviving older container will displace it on reboot. Establish a safe generation/authority policy for this case, or explicitly refuse persistence until authority can be established. Preserve the A/B power-loss guarantees and do not derive trusted generation metadata from unvalidated bytes.

Verification: cover transient refusal followed by a real change, verified commit and clean reboot, with both slot orientations and sequence boundaries. Check restored payload as well as status. Add a control that recreates the generation restart defect. `run_edge_probes.py` currently reproduces it without modifying production source; its exit zero means the reproduction assertions held, not that persistence passed.

**R501-2-F2 - MINOR - Tests, Docs**

Artifact: `sw/firmware/ctrl_nvm/README.md:201`, `:219`, `:224`; `test/nvm_checks_write.py:391`; `plat/nvm_flash_litespi.c:66`, `:115`; PR #669, “The service bound”. Same edge receipts and `receipts/campaign-summary.log`.

Authority/evidence: round-2 assignment items 4/8 require bounded SPI service and accurately derived service claims. The individual waits are now finite. However, the CPU estimate adds one 4,096-read wait to a whole page call and compares the result with 24.5 ms. A progressing controller can delay every byte without reaching any individual timeout. On the unchanged port, `tx:261:0:4000` delays each TX wait in WREN plus the first page command by 4,000 reads. The call takes **41,969 us of model time** at both shapes, completes successfully, and reports `ls_hung=0 failed=0 ok=1`. The suite's slow-controller case delays only two waits. Under the README's assumed 0.5 us per CSR read, those 261 delays alone would cost 522 ms, before normal transfers. No such CPU duration was measured.

There is also a direct numerical overstatement in the PR's “at most 210 us measured” phrase. The unmodified suite itself reaches 849 us on four shapes and 850 us on the 4x4. The README's narrower 210-us claim for the dedicated normal bound run is consistent with that run; it should remain explicitly scoped to it.

Impact: a finite per-wait limit is presented as support for a much smaller whole-call service figure. The current tests and estimate omit cumulative progress delays, so a reader cannot use them to size an event-loop service budget. This finding does not claim that the old infinite loops remain or that physical timing was measured.

Required outcome: distinguish the nominal measured scenarios from the cumulative bound for a progressing controller, and state the assumptions required for any whole-call comparison. Include a sustained-delay case, covering many waits in one call, and grade the intended bound. Correct the PR's measured maximum. A scheduling redesign is only required if the selected service contract demands a tighter bound.

Verification: rerun the ordinary bound, isolated stall, and all-byte delayed-progress cases; retain raw call durations and the assumptions behind the derived CPU figure. A changed figure/test claim is outside the owner's RESIDUE category.

**R501-2-F3 - MINOR - Conformance, RTL, Robustness, Tests, Docs**

Artifact: `docs/design/SAVED_STATE_FASTCONNECT.md:771`; `sw/firmware/ctrl_nvm/nvm_store.c:171`; `test/nvm_checks.py:222`; `test/nvm_mutants.py`, `tie_picks_b`; public issue comments 5996281116 / 5997533145 and PR body.

Authority/evidence: FASTCONNECT section 7's algorithm offers B when sequences are equal (`(int32_t)(A.seq - B.seq) > 0` is false). This store uses `>= 0`, selecting A, as the shipping implementation does. The new `tie_picks_b` control changes precisely that choice and fails `newer_wins`: “seq A 0x7 B 0x7: chose 1, want 0”. The failure is real, but the planted behavior follows the literal governing algorithm. The executor explicitly leaves this conflict for a decision. No settling decision appeared in the public issue/PR scope examined.

Impact: equal-sequence containers with different payloads restore different state depending on which authority is followed. The new test freezes one interpretation while advertising the other as a defect. This is a normative boundary-case conflict, not an optional wording change.

Required outcome: record the public tie decision and align the governing page, implementation and test oracle. This review does not prescribe A or B. AGENTS sections 2/4 prohibit privately resolving a specification conflict in favor of existing code.

Verification: equal sequences with distinct payloads at both slots must exercise the selected rule; the opposite control must fail for that publicly approved rule. Ordinary adjacent-generation wrap cases must remain green.

**Reviewer-owned coverage ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1, F3 | Issue #665 F1 scope 5993775541 and round-2 scope 5996009284; REQUIREMENTS ownership/verification; FASTCONNECT 4.2/6/7/9; MATERIALIZATION 6/8/15.1; codec and store; refusal/commit/reboot probe | R501-2 | 7f8dc1b10c80c9e9631b8d6c6f5f37a039bc2e11 |
| RTL | UNCLEAN: F1, F3 | `nvm_store.c` FSM and dirty/inflight ownership; `nvm_shape.h`; `nvm_state.h`; timer0/LiteSPI port; pinned writer `protocol-processor/hdl/aecp/KL_aecp_nvm_writer.sv` restore/retry contracts; merge artifact identity | R501-2 | 7f8dc1b10c80c9e9631b8d6c6f5f37a039bc2e11 |
| Robustness | UNCLEAN: F1, F3 | KLJ2 boundary/refusal and wrap checks; binding/D3 rollback and CLOSED; retries, console, PHC steps, counter wrap, stalls, faults and power cuts; both edge-probe logs | R501-2 | 7f8dc1b10c80c9e9631b8d6c6f5f37a039bc2e11 |
| Tests | UNCLEAN: F1, F2, F3 | `test/test_ctrl_nvm.py`, both check modules, runner, mutation seams and RV32 arm; three host models; five shape campaigns; all 69 mutant receipts; `MUTATION-AUDIT.md` | R501-2 | 7f8dc1b10c80c9e9631b8d6c6f5f37a039bc2e11 |
| Docs | UNCLEAN: F2, F3 | Module README, `nvm_flash.h`/`nvm_state.h`, docs-index row, public PR body and scope/evidence comments; saved-state authorities, published historical HANDOFF and capture receipt | R501-2 | 7f8dc1b10c80c9e9631b8d6c6f5f37a039bc2e11 |

No lens is banked clean. The implementation's positive results below do not override the open findings.

**Round-1 findings and assignment reconciliation**

| Public finding / assignment | Disposition at this head | Exact artifacts and executed evidence |
|---|---|---|
| R501-1-F1; item 3 | RESOLVED | `nvm_store.c:125` judges the RAM container; `:179` rechecks CRC and selected SEQ. `read_flip_boot` sweeps the single-bit byte-8 fault across reads, slots and wrap orders; `read_alias_at_stage` checks mismatched generations. Corresponding controls fail. F1 above is a different post-refusal commit/reboot defect. |
| R501-1-F2 and R500-1-F2; item 2 | RESOLVED under the round-2 assignment | `:398`, `:463`, `:657`, `:675`: only changed staged bytes replenish attempts; console honors backoff/exhaustion; abandoned count/verdict survives later success. `dr2c_unchanged_set`, `dr2c_console`, recovery checks and all five bypass controls execute. FASTCONNECT 9.2 governs recoverable stale status; no producer-alarm ownership is reassigned. |
| R501-1-F3 and R500-1-F1; item 1 | RESOLVED | `plat/nvm_flash_litespi.c:202` uses accumulated timer0 ticks; production code has no PHC read. `time_base` checks +/-60-second PHC steps in debounce, backoff and hung erase/program intervals, plus the 42.9-second counter wrap. PHC-backed and nonaccumulating controls fail. Unused blocking helper removed. |
| R501-1-F4; item 4 | RESOLVED as the infinite-wait defect | `ls_ready`, `ls_open`, `ls_window`, `ls_busy` terminate stalled waits, release chip select and return failure. Delayed, permanent TX/RX and drain cases run. Both unbounded controls produce explicit `ls_hung=1`; ignored-return control reports the wrong failure stage. F2 above retains the separate cumulative timing-evidence gap. |
| R500-1-F3; item 5 | RESOLVED | `nvm_store.c:664` leaves no first-dirty window for a change consumed by the current capture. `debounce` covers a later change after that capture and a change after capture has passed. The stale-window control advances erase to 1,703 us and fails. |
| R500-1-F4; item 6 | RESOLVED | `:217`, `:244`, `:325` and `nvm_state.h` implement distinct binding and D3 walks. D3 abort leaves bindings applied; binding failure undoes bindings and permits D3; failed undo closes service. Four new controls catch ordering, isolation and rollback failures. |
| R500-1-F5; item 7 | Implemented detection; tie authority still OPEN as F3 | Verify/blank-check tails, read failures, program refusal, time and equal-sequence cases now have executed controls. All mechanically fail their named checks. `tie_picks_b` needs the public rule before it establishes a conformance defect. |
| R500-1-F6; item 8 | Original CPU-vs-model conflation RESOLVED; F2 remains | README separates counted bytes, model time and a derived CPU estimate; it names callback/record-walk/CPU costs and calls 1.2 ms a floor. The cumulative wait estimate and PR maximum still need correction. |
| Item 9 | PASS | Exact merge has ordered parents `7725bcfa0dff380966f7846ebfff10c3e21349ee` and `510fae60b26bef1db138de5cf2ac72b17b5011a5`. All 31 lane entries match the first parent; all 38 imported paths match dev, including the processor pin. |
| R500-1-S1 | Retained SUGGESTION | The lane gate is still not wired into hosted CI. Public PR body records that integration risk; it does not independently make a lens unclean. |

Prior findings: [R501-1](https://github.com/kebag-logic/milan-fpga/pull/669#issuecomment-5995888263), [R500-1](https://github.com/kebag-logic/milan-fpga/pull/669#issuecomment-5996001016). The PR had zero submitted reviews and zero inline comments when checked. The other reviewer's findings were read after this review's independent verdict and ledger were recorded; no round-2 peer report was used.

**Executed evidence and limits**

- `python3 run_campaign.py --repo <exact-checkout> --jobs 8` ran five independent shape campaigns and all 69 mutations under a foreground coordinator, each with its own log and return code. All 74 tasks returned zero. The source campaigns ran all 37 named checks with the suite's port matrix and required RV32I compilation. Full parent/processor/gPTP/synthesis/builder banks were not run.
- The source campaigns total 1,018 runner invocations. The 3,126 power-cut cases cover three initial media states, both ports, four fractions within every erase/page program, and a representative cut at entry to read-back. No mixed old/new restore was accepted. This is finite model coverage, not every physical cut position.
- RV32I bss/text sizes reproduce the page: 4,032/10,997 bytes at 1x1 and 14,392/11,001 at 8x8. Stage sizes are 3,344/13,264; payload 136/576; chunk 256; store state 280; timer state 12. Production storage is static. RV32 was compiled, not executed.
- The codec is consistent with the reference encoder on the suite's refusal cases and recorded 1x1/8x8 vectors. Frame ordering, mixed endianness, CRCs, erased spans, identity/shape and sequence-wrap checks were inspected. No shipping writer, recorded vector or capture input was changed by the lane.
- All 24 newly added mutations were inspected and their actual failure messages checked. One old control was removed, giving 69 rather than 70. `MUTATION-AUDIT.md` maps every added control to its failure. No compile error or generic process timeout was counted as a kill. The tie control's authority exception is F3.
- `python3 run_edge_probes.py --repo <exact-checkout> --jobs 2` reproduced F1 and the delayed-progress timing case at both 1x1 and 8x8. All build/probe trees are confined to `scratch/`, excluded from publication. The raw logs contain full runner summaries and commands.
- The lane adds portable store/port contracts and a host state adapter. No image links it yet. F0's switch/event-loop integration and F3/F5's real state owners remain separate work. `settle()` documents #658's clip-to-restored-format seam; the synthetic state model does not prove that clipping or actual descriptor-memory rollback/debt containment.
- The timer requires exclusive ownership and sampling more often than one 32-bit wrap. The README records this condition. Model PHC-step and wrap tests do not measure clock behavior on silicon.
- Public historical evidence was read from commit `38e93660c8e2d4c190a00e8538611de01fece598`, `review-evidence/665f1-r1`, and checked against its published hashes. That immutable directory contains `gates-215c3c0b`, not round-2 raw gate receipts. Its builder result is rc 0 with physical calibration gate 11 NOT RUN. The round-2 exact-head source results are reported publicly in [5997533145](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-5997533145); the assignment additionally reports the manager's full source static/builder/native banks passed. This review independently reran the focused lane bank described above. It does not relabel historical evidence as exact-head evidence.
- No hosted-job result or skipped context is counted as an execution in this packet. Hosted/replica acceptance belongs to the manager. Physical calibration NOT RUN; no hardware or field campaign was performed. Field skips are not hardware proof. The unchanged shipping capture receipt is conditional evidence for that writer, not a CPU bound for this module.

**Integrity, publication and remaining duties**

`receipts/integrity.log` and `.rc` verify the complete superproject index and 1,041 tracked blob bytes/modes against the exact head/tree. Required submodules are initialized at their gitlinks and independently byte/mode/index checked:

| Submodule | Exact pin | Checked blobs |
|---|---|---:|
| protocol-processor | `ead8036035affd53ef4b29979190f2f4f67084c0` | 558 |
| gptp-processor | `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` | 104 |
| third_party/verilog-axis | `48ff7a7e2ef782cf778d47910cf85835c64b1bce` | 214 |

The optional external gitlink/index entry is unchanged and unused. Review-created bytecode caches were removed. The checkout has no tracked, untracked or ignored residue. No production source edit required restoration, and no job remains running.

Portable reproduction scripts are `run_campaign.py`, `run_edge_probes.py` and `verify_integrity.py`. Use an exact detached checkout and the existing build prerequisites; the packet installs nothing. Each invocation remains foreground, and campaign concurrency is capped at 16. `verify_integrity.py <exact-checkout>` verifies the entire tracked state; `sha256sum -c MANIFEST.sha256` verifies the publication allowlist. Only REPORT.md and manifest-listed files are intended for publication; `scratch/` and downloaded source material outside the allowlist are excluded.

The manager must publish this packet, resolve F1-F3 (including the public tie decision), and obtain re-review at the corrected exact head. The manager owns the remaining source/hosted/replica evidence and the final merge candidate built against then-current dev. This source review is not that candidate's validation. Merge still needs the complete review bar, no review in flight, explicit maintainer authorization and post-merge containment. Issue #665 remains open for its other lanes. The unchanged shipping-writer parity discrepancy remains a separate follow-up.

R501-2 FINISHED
