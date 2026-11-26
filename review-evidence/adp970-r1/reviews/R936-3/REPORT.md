[R936] POSITIVE - exact head 701a980b32bf31636811ef831739c9bfd3d6f978

R936-3, external independent review of issue #970 / PR #1015.
Tree: `03e2a77c669704aa8b42207ff0e99163d925e304`.
Source base: `4df125b8c11f0e1706b3c1e489f3e66a5d856b18`.
Narrow delta: `f4833e16a07d07494277aba8dc7a5de19320c20b..701a980b32bf31636811ef831739c9bfd3d6f978`, one commit, six files.

R936-2-F1 is resolved at its cause. No new BLOCKER, MAJOR or MINOR was found. All five lenses are CLEAN for this delta and its dependencies. Previously reported wording residues and optional suggestions are explicitly retained below. This verdict neither authorizes merge nor closes #970.

**Scope and independence.** Reconstructed the repository contract and documentation map, the issue's acceptance and public rulings, requirements and interface authorities, the source-base diff and history, then the public executable evidence. The independent source verdict and five-lens ledger were recorded before reading prior public findings. No current-round peer report, private author material or management checkout was read. Untouched code retains its preceding review disposition; it was not subjected to another broad bank.

The controlling [scope ruling](https://github.com/kebag-logic/milan-fpga/issues/970#issuecomment-7174054394) preserves immediate LINK_UP delivery, the full Milan delay ranges and the declared 6.0 s. The [earlier correction](https://github.com/kebag-logic/milan-fpga/issues/970#issuecomment-7080789556) rejects narrowing the range. The [later attribution](https://github.com/kebag-logic/milan-fpga/issues/970#issuecomment-7184965594) does not expand this count-only review into hardware qualification.

**R936-2-F1: resolved, formerly MINOR, RTL / Tests / Docs.**

Artifacts: `tb/verilator/ctrl_service_budget/scenario.py:266` and `:944`; `model_counts.py:33`, `:47`, `:71`; `run.py:897`; `sw/firmware/ctrl/adp/adp_mbx.h:123`; `adp_mbx.c:60`; `grade.py:638`.

Both constructors now publish 12. The size-fixture composition calls no `adp_mbx_set_clock`; the core's qualified rise calls `leave_down`, and the adapter's fallback adds one NOW_MS read. The preceding public gate receipt measures `C0 LINK_UP -> TMR_DELAY armed 12 accesses (bound 12)`. Those runtime and test sources, the stack pin and the image composition are byte-identical between the preceding and current heads. The platform's separately wired clock still gives the 11-access path; README line 1326 and the live PR Description distinguish it correctly.

Independent `delta_probe.py` checks the actual constructors at 1x1/1if, 8x8/1if and 8x8/2if. They contain 6, 6 and 11 corrected LINK_UP instances respectively. Every generated stimulus byte, wait, budget, simulation duration and other probe field is identical to the preceding head. Planting 11 independently at either construction site is detected. Mutating each of the five mapped ADP paths also produces its expected finding. Both explicit `probe.path` and interface-suffixed names are exercised.

The committed trace was regraded with both scenario versions. Its complete result is identical after normalizing the single `model_accesses` value from 11 to 12: timings, measured accesses, deadline verdicts, pass bounds and composed results do not change. `fixture-regraded.json` and `fixture-table.md` record the corrected output. The LINK_UP row prints `88 (12)`; 88 is that recorded CPU pass's measured accesses, and 12 is the separate host-model comparison. These are not interchangeable measurements.

The actual `run.py --self-test` dispatch was also exercised: stale metadata returns failure before the fixture campaign; correct metadata reaches that campaign and preserves its failure status. The repository's planted stale count is found six times at one interface and eleven at two interfaces. The checker covers its five explicit `ADP_MBX_LAT_*` mappings; it is not an independent runtime counter or an exhaustive checker of arbitrary future probes.

**Executed and carried evidence.**

| Check | Result and receipt |
|---|---|
| Independent constructor, stale-value, dispatch and real-trace checks | PASS, `delta-probe.log`, `delta-probe.json`, exit 0 |
| New count check plus existing budget baseline and all 295 existing mutations | PASS, 296/296 completed, zero failures; `budget-campaign.log`, `.json`, exit 0 |
| Python idiom gate | PASS, `python-idiom.log`, exit 0; long modules 10/10, overlong lines 0/0 |
| Public author receipt digests | PASS, all 42 files, `evidence-integrity.json` and `.log`, exit 0 |
| Source dependency and public receipt spot-check | PASS, `receipt-audit.log`, exit 0 |
| Exact tracked bytes, modes, indexes and required gitlinks | PASS, 3,361 entries, `checkout-integrity.json`, exit 0 |

The ordinary serial budget self-test was interrupted for scheduling, exit 130. Its partial output is retained as `budget-selftest.log`; it is not a successful gate. `budget_campaign.py --jobs 16` runs the same baseline `selftest.checks()` and each existing mutation under the repository's own mutation context and exception rules, with at most sixteen workers. No assertion, mutation or exception rule was weakened. The real dispatcher was checked separately above. Complete worker output is in `budget-worker-logs.tar.gz`; the portable driver and result JSON are included.

The author packets are immutable public artifacts at [40ce56ee, first packet](https://github.com/kebag-logic/milan-fpga/tree/40ce56ee579d00874e4c9db98893f0742498aee3/review-evidence/adp970-r1) and [af092a85, preceding-head packet](https://github.com/kebag-logic/milan-fpga/tree/af092a85bcda1d60fab649ca42e2b013996ee21e/review-evidence/adp970-r2). Every author file matches its published digest. Neither evidence commit contains an embedded signature; no detached signature was supplied or found in the inspected evidence tree. This proves digest integrity, not independent signature authentication. The evidence branch snapshot `4f3f1974e4745ad5d7942f8ee226be55f471d086` exposes these two packets and no round-6 author packet (`evidence-snapshot.json`). Historical ready statements are not treated as current-head claims.

The preceding-head `arms.log` records adp, portable, unit, walk, platboot1 and platboot2 all exiting 0. `gate.log` records 84 ADP checks, zero failures and the 12-access C0 measurement. `bselftest.log` records zero failures. These unchanged runtime arms were spot-checked and carried, not rerun or relabeled as fresh execution at 701a980b.

The published CPU receipts pair 75 probes at 1x1/1if with zero misses on either side, and 90 at 8x8/1if with the same seven known misses on both sides. Their execution summaries record zero refusals and zero passes above the 2 ms share. The comparison is against `5de21ff3`; the three-byte base-image distinction is retained below. Current runtime/image inputs and grading are unchanged; constructor comparison proves the corrected metadata does not alter the stimuli or budgets. No new CPU simulation, complete two-point CPU report regeneration, or four-point image build is claimed. The new generated receipt here is the real recorded fixture plus the three-point constructor comparison. Earlier generated evidence remains evidence of its named head.

**Reviewer-owned lens ledger.** Each row applies the lens to this delta and checks its dependencies against the preceding head; it does not claim a fresh broad regression bank.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #970 rulings; `docs/reference/FR_NFR.md:199` discovery derivation; `docs/design/MAILBOX_SPLIT.md:528`; `scenario.py:266,944`; unchanged pinned `src/adp.c:98,263`. Count metadata adds no link hold, range change, GM behavior change or clause change. | R936-3 | 701a980b32bf31636811ef831739c9bfd3d6f978 |
| RTL | CLEAN | Six-file delta; `adp_mbx.c:60`, `adp_mbx.h:123`, `ctrl_plat.c:401`, size-fixture composition, `grade.py:638`; `receipt-audit.log`. No HDL, clock/reset/CDC, firmware runtime, image input or gitlink change; fallback accounting agrees with its boundary. | R936-3 | 701a980b32bf31636811ef831739c9bfd3d6f978 |
| Robustness | CLEAN | `model_counts.py:42,47,64,71`, `run.py:897`; `delta-probe.log`. One/two interfaces, both path forms, each stale construction site, every mapped path and failure propagation checked. Existing reset, duplicate/disabled rise, timer and backpressure behavior is untouched. | R936-3 | 701a980b32bf31636811ef831739c9bfd3d6f978 |
| Tests | CLEAN | `model_counts.py`, `scenario.py`, `run.py`; existing `selftest.py`/fixture/oracle; `delta-probe.log`, `budget-campaign.json`, public ADP arm receipts. New check detects the original defect and the dispatcher invokes it; timings and verdicts remain independently unchanged. | R936-3 | 701a980b32bf31636811ef831739c9bfd3d6f978 |
| Docs | CLEAN | Budget `README.md:1326`; `SUBMODULES.md:1199`; `adp_first_mutants.py:121`; live PR Description; generated fixture table. Correct 12/11 composition distinction, paragraph repair and behavior-based source comment; retained wording residues below do not affect clean coverage. | R936-3 | 701a980b32bf31636811ef831739c9bfd3d6f978 |

**Prior findings reconciled.** Sources: [R936-1](https://github.com/kebag-logic/milan-fpga/pull/1015#issuecomment-7178340125), [R935-1](https://github.com/kebag-logic/milan-fpga/pull/1015#issuecomment-7179085015), [R936-2](https://github.com/kebag-logic/milan-fpga/pull/1015#issuecomment-7187819678), [R935-2](https://github.com/kebag-logic/milan-fpga/pull/1015#issuecomment-7188837546). No current-round peer report was consulted.

| Prior ID | Disposition at this head and cause evidence |
|---|---|
| R936-2-F1, MINOR, RTL/Tests/Docs | RESOLVED by both 12 literals, the consistency check and independent generated-output comparison detailed above. |
| R936-2-R1 and R935-2-RES3, RESIDUE, Docs | RESOLVED. `adp_first_mutants.py:121` now states behavior with #970 and IEEE 6.2.4.2.2, without review narration. Test-case IDs elsewhere are executable case identifiers, not bench labels. |
| R936-2-R2 and R935-2-RES1, RESIDUE, Docs | RESOLVED. `SUBMODULES.md:1199` is followed directly by its refusal statement at 1201; all numbers are preserved. |
| R936-1-F1, MAJOR, all five lenses | Remains RESOLVED. Unchanged stack pin calls `leave_down` on startup and qualified LINK_UP, behind duplicate/disabled guards; unchanged H9/H10 and B27 cover sample count and link-time dependence. No new dependency invalidates that resolution. |
| R935-1-F1, MAJOR, Tests/Docs | Source causes remain RESOLVED. Current Python gate passes; the existing CHANGELOG contents repair is untouched. Hosted acceptance remains a manager duty. |
| R935-1-F2, MINOR, Docs/RTL | Measurement cause remains RESOLVED. Unchanged `SPLIT_CONTROL_MEMORY.md:755` gives the explicit measured baseline and +264/+272/+264/+256 B deltas. Its remaining base-label residue is retained separately. |
| R935-1-F3, MINOR, Tests | Remains RESOLVED. Unchanged B25 uses three origins one microsecond apart and reset clears the binding. Its previously verified coarse-clock/late-wiring controls retain their disposition. |
| R935-1-F4, MINOR, Docs/Conformance | Remains RESOLVED by the implemented fresh sample; unchanged current description agrees with the pin. Historical ready text is not used to assert old code had new behavior. |
| R935-1-R1, RESIDUE, Docs | Remains RESOLVED: FR_NFR attributes uniformity to H4-H6 and seed terms to H7. |
| R935-1-S1/S2/S3, SUGGESTION | Remain addressed: mixed NOW_MS fallback documentation, clock-origin/reset cleanup, and PR explanation of fixed-duration idle polling are unchanged. |
| R935-1-S4, SUGGESTION, Tests | RETAINED outside this delta: generator-order reproducibility remains disclosed in PR Known limitations; the prior boot receipts use `PYTHONHASHSEED=0`. Optional outcome: separately remove ordering dependence and verify repeated generation. |

**Retained wording residues and suggestions.** These are existing public items, not newly discovered blockers. Their original IDs are preserved.

- **R935-2-RES2, RESIDUE, Docs.** Artifact: `docs/design/SPLIT_CONTROL_MEMORY.md:755`. Authority/evidence: preceding public baseline ledgers and unchanged text; the numbers agree at both baselines, while “this change's own base c34e7d8b” is stale after the merge. Impact: reference wording only. Exact outcome: replace that phrase with “against `c34e7d8b` and this change's base `4df125b8`, which take the same figures”. Verification: paragraph diff; retain all figures verbatim. Manager carries it to the residue checklist.
- **R935-2-RES4, RESIDUE, Docs.** Artifacts: public `adp970-r2/author/REVIEW-READY.md` section 2 and live PR CPU comparison rows. Authority/evidence: preceding review's image comparison and the manifest-verified packet; CPU base is `5de21ff3`, with the previously recorded three-byte `adp_rx` distinction, not full image identity. Impact: base/path wording; no measured figure or verdict changes. Exact outcome: label both PR rows “CPU budget legs against `5de21ff3`”; qualify the handoff's image-equality sentence with “but for #38's one comparison in `adp_rx` (3 bytes, the same instruction count, a path no leg's probe takes differently)”; correct `receipts/r5/milan/` and `receipts/r5/attribution/` to `receipts/milan/` and `receipts/attribution/`. Verification: compare text with published paths and preserve receipt bytes/history. Manager carries it to the residue checklist.
- **R936-2-S1, SUGGESTION, Docs.** Artifact: live PR opening and Linked Issue / roles. Evidence: duplicated role prefix and three “to be assigned” placeholders remain, despite public role records. Impact: presentation only. Optional outcome: keep one prefix and populate the recorded roles. Verification: compare with the review-start notices.
- **R935-2-S1, SUGGESTION, Tests.** Artifact: `test_adp.cpp:1052`, H10. Evidence: the unchanged distinct-delay floor is 600 for 1,024 draws, with 915 observed in preceding execution. Impact: optional sensitivity beyond the constant-sample defect and existing distribution/resolution checks. Optional outcome: consider a justified stronger floor, such as the previously suggested 850. Verification: intended partial-entropy controls and unchanged positive ensemble.
- **R935-2-S2, SUGGESTION, Docs.** Artifact: `adp_mbx.h:23`. Evidence: unchanged comment wraps after “and seeds its”. Impact: readability only. Optional outcome: reflow the paragraph without changing its meaning. Verification: comment-only diff.
- **R935-2-S3, SUGGESTION, Conformance.** Artifact: pinned `src/adp.c:53`, unchanged draw mapping. Evidence: preceding finding notes 16-bit multiply-shift quantization. Impact: optional separate investigation of pre-existing distribution resolution; no new defect is attributed to this count delta. Optional outcome: resolve the desired precision separately before changing arithmetic. Verification: exhaustive mapping analysis and existing range/seed tests for any future change.

**Limits and pending manager duties.**

No manager source bank ran at this head, and none is inferred. Source receipts and this review's focused checks are distinct from the final current-dev candidate. The manager owns the candidate formed from source base `4df125b8c11f0e1706b3c1e489f3e66a5d856b18` and live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`, its builder/native banks, linked receipts, hosted/local-replica acceptance and any required refreshed full CPU reports. No hosted snapshot or aggregate completion is asserted by this round. Skipped contexts are not executed evidence. Independent approvals, explicit merge authorization and post-merge containment remain required.

Physical calibration: NOT RUN. Field skips are not hardware proof. No physical boot-entropy measurement or new proof of advertisement delivery within 6.0 s is supplied. The issue's remaining bench acceptance and wider release obligations remain separate.

No source fix, commit, push, GitHub write, full parent/processor/build bank, local workflow replica, hardware access or other-checkout edit was performed. Probes changed in-memory objects only. Final integrity verification covers the parent and all five required initialized submodules, including raw blobs/modes and stage-0 indexes; the optional `external` gitlink remains uninitialized. Disposable trees stay under `scratch/` and are excluded from publication.

Reproduction from this packet, with an exact checkout and the two public evidence commits available:

```sh
python3 -B verify_evidence.py CHECKOUT PACKET
python3 -B audit_receipts.py CHECKOUT PACKET
python3 -B delta_probe.py CHECKOUT PACKET
python3 -B budget_campaign.py CHECKOUT PACKET --jobs 16
python3 -B verify_checkout.py CHECKOUT PACKET
```

All five commands should exit 0. `MANIFEST.sha256` lists every publishable receipt and portable script. `REPORT.md` is published alongside them; `scratch/` is never published.

R936-3 FINISHED
