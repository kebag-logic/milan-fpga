[R501] NEGATIVE - exact head 9412006bd58c002835bb06d46045c53098cc59a5

Round R501-3, external independent review of issue #665 / PR #669, F1.
Tree: `ba76ab7618f8d97c681d0e33f7b2d2128c6169aa`.
Source base: `fa450d301805881ad713b67521477bf042ddadfd`.
Integrated dev: `28f9666feab2b2ba287643c63ed3a16b1e0bb863`.

All five lenses were applied. One MAJOR finding remains: matching refusal codes are mistaken for agreement between reads, allowing another generation restart and loss of saved state. No MINOR, BLOCKER or RESIDUE is added. The existing CI suggestion remains optional.

The independent source pass, verdict and ledger were written before reading prior reviewer reports (`receipts/independent-pass.md`). Reconstruction used the repository contract, documentation index, public frozen scope/decisions, linked authorities, requested diff/history, then public executable evidence. No private author material or other checkout was consulted.

Short source paths below are relative to `sw/firmware/ctrl_nvm/`; design pages are under `docs/design/`.

**R501-3-F1 - MAJOR - Conformance, RTL, Robustness, Tests, Docs**

**Artifact:** `nvm_store.c:191`, particularly `:203`; `test/nvm_checks_write.py:516`; `README.md:395`; PR #669, “Stated readings” and read-fault limitation.

**Authority/evidence:** [Decision 2](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-5997929153) requires unknown read-fault authority to prevent commits. The public [round-3 interpretation](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-5998087724) explicitly treats disagreeing reads as media faults. FASTCONNECT sections 6.2/7 require validated authority and durable promotion. The reported limitation covers corruption repeated identically on every read.

`nvm_slot_check()` retains only `prev`, an enum verdict. `vd == prev` accepts a refusal without comparing any returned bytes. Thus two different corruptions of a valid slot both returning `VD_CRC`, or both returning `VD_MAGIC`, establish a content refusal. No third read is attempted although the three-try budget has room and the transient fault has ended.

The independent probe changes only the disposable flash model's injected fault: the first relevant read XORs 8 into one byte, the second XORs 16, and subsequent reads are clean. Physical flash bytes stay intact. The compiled production store, codec and port match the head byte for byte; their hashes are recorded. Tests cover both slot orientations, SEQ 1/5/0x80000000/0xFFFFFFFF, header and body corruption, and both 1x1/8x8 shapes: **32 of 32 cases lose saved values after a successful commit and clean reboot**. Corresponding single-corruption controls all pass.

A representative case has valid slot A at SEQ 5 and blank B:

| Observation | Exact-head result |
|---|---|
| Two full-container reads, byte 256 | different returned bytes, XOR 8 then XOR 16; both fail CRC |
| Authority after those refusals | `unread=0`, `read_faults=0`; persistence allowed |
| Change one saved name; finish commit | `ok=1`, authority B, SEQ 1 |
| Clean reboot | authority A, SEQ 5; newly committed name lost |

At the other boundaries the failure varies. In 20 cases the changed record is lost because the surviving slot wins. In 12, the new SEQ-1 container wins but loses the other 53 records at 1x1 or 163 at 8x8, because it was built from defaults. Every case fails the saved-payload comparison. This is distinguishable read disagreement, beyond the documented identical-corruption limitation.

**Impact:** a transient, detectable disagreement authorizes persistence over unknown state. The store reports a verified commit but cannot preserve the saved set across a clean reboot. The current `authority_unknown` cases inject one silent corruption or signalled read failures; they do not exercise two differing bytes with the same refusal class. The README/PR overstate the protection and understate the residual fault class; this is a behavioral claim, outside RESIDUE.

**Required outcome:** two different invalid byte strings must not establish a stable content refusal solely through a shared verdict. Use agreement evidence for the relevant returned bytes, or keep authority unknown. A later validated read may establish authority; otherwise retain HELD. Do not take SEQ from unvalidated bytes. Align the tests and documented limitation with the implemented rule.

**Verification:** `scripts/probe_read_agreement.py` must cease demonstrating lost values: use the remaining clean read or report UNREAD/HELD without committing. Retain both orientations, all four sequence boundaries, header/body faults and complete payload checks. Add a planted control that reduces agreement back to verdict equality. Raw commands/stdout and expected/observed values are in `receipts/read-agreement/*.runs.jsonl` and `*.results.json`; matching controls are in `*.controls.json`. `receipts/read-agreement.rc` is **1**, a contract failure, not a build failure.

**Reviewer-owned coverage ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN, F1 | #665 scope 5993775541 and decisions 5997929153; FASTCONNECT 4.2/6.2/7/9; MATERIALIZATION 8/15.1; `nvm_store.c:191`, `:363`, `:488`; codec and authority probe | R501-3 | 9412006bd58c002835bb06d46045c53098cc59a5 |
| RTL | UNCLEAN, F1 | `nvm_store.c:135`, `:277`, `:393`, `:692`; `nvm_shape.h`; `nvm_state.h`; `plat/nvm_flash_litespi.c:78`; pinned `protocol-processor/hdl/aecp/KL_aecp_nvm_writer.sv:35`; merge/input identity receipt | R501-3 | 9412006bd58c002835bb06d46045c53098cc59a5 |
| Robustness | UNCLEAN, F1 | `test/nvm_checks.py:313`, `:436`, `:532`; `test/nvm_checks_write.py:243`, `:433`, `:516`, `:579`; read-agreement and permanent-failure receipts | R501-3 | 9412006bd58c002835bb06d46045c53098cc59a5 |
| Tests | UNCLEAN, F1 | All `test/` check/driver/control sources and three `host/` implementations; recorded 1x1/8x8 vectors; `receipts/campaign/`, 80 controls; independent differing-read probe | R501-3 | 9412006bd58c002835bb06d46045c53098cc59a5 |
| Docs | UNCLEAN, F1 | `README.md:122`, `:239`, `:395`; `nvm_flash.h`, `nvm_state.h`; FASTCONNECT section 7 tie edit; docs-index row; PR body and public evidence comments | R501-3 | 9412006bd58c002835bb06d46045c53098cc59a5 |

No lens is banked clean while F1 remains open. Positive results below establish the specified paths only.

**HELD, permanent read failure and reset**

`nvm_store_boot()` releases AECP at `nvm_store.c:412` before selecting HELD at `:416`. Each HELD service call samples time, publishes status and returns through the switch default; it performs no capture or media access. `nvm_store_changed()` still marks dirty; `nvm_store_commit_now()` refuses any phase other than IDLE.

At both shapes, a flash model returning failure for every read reaches HELD after six failed reads, three per slot. The receipt records `unread=3`, `read_faults=6`, `releases=1`, `dirty=1`, zero erase/program operations and 100,000 completed service calls over 10 seconds. Two console requests are refused. Clearing the injected fault halfway through leaves HELD intact, so there is no implicit runtime recovery or repeated read storm.

Reset followed by a new boot is the only supported exit; the public contract assumes coupled cold initialization. That is acceptable under decision 2 and the round-3 assignment: persistence is held, ordinary service is released. An unproven entity model independently remains CLOSED under D3 8.1/8.8. These are bounded-return HAL results, not proof that an unresponsive physical memory-mapped bus transaction returns. Hardware and real owner integration remain untested here. Reporting is through `nvm_store_status()`; an actual console/status consumer belongs to integration.

**Prior public findings, resolved or retained at this head**

Read [R501-1](https://github.com/kebag-logic/milan-fpga/pull/669#issuecomment-5995888263), [R500-1](https://github.com/kebag-logic/milan-fpga/pull/669#issuecomment-5996001016), [R501-2](https://github.com/kebag-logic/milan-fpga/pull/669#issuecomment-5997910948) and [R500-2](https://github.com/kebag-logic/milan-fpga/pull/669#issuecomment-5997904664) after recording the independent verdict. The retrieved PR has zero submitted reviews and zero inline comments; `receipts/public-state.json` records the public artifacts.

| Finding | Disposition | Exact-head evidence |
|---|---|---|
| R501-2-F1 | **RETAINED through F1 above.** Original signalled-fault case is fixed; the authority/durability outcome remains violated for differing corrupt reads. | `nvm_slot_check`, `nvm_stage_slot`, HELD; `authority_unknown` passes both slots at four boundaries and checks reboot payload; `unread_not_held` is caught. Independent differing-read probe still loses state. |
| R501-2-F2; R500-2-F2 | RESOLVED | `ls_call_begin`/`ls_late` add a whole-call deadline; `port_deadline` grades ten/twelve/all slowed waits. README and PR separate nominal 250-us checks from the 2,213-us cumulative model bound. Actual maximum is correctly stated as 2,190 us at 4x4, 2,189 elsewhere; CPU estimate is a floor without a 24.5-ms comparison. |
| R501-2-F3 | RESOLVED by decision 1 | FASTCONNECT section 7 now uses `>= 0 ? A : B` and cites the ruling. `newer_wins` checks distinct payloads tied at 7 and 0xFFFFFFFF; `tie_picks_b` fails. |
| R500-2-F1 | RESOLVED | `nvm_restore:363` chooses/stages, restores bindings, then proves the model before D3. `model_unproven_closes` checks retained bindings, COMPLETE binding terminal, CLOSED D3 and no release; both controls fail. |
| R500-2-F3 | RESOLVED | `fallback_restage` corrupts all three re-stages of both picks; `fallback_restage_unchecked` fails. `debounce` changes the next cursor record; `taken_off_by_one` fails. |
| R500-2-F4 | RESOLVED | `nvm_heal:482` runs after DR2b suppression and verified promotion. `recovers_after_failure` ends with `stale=0`, no dirty/pending work; `dr2b_keeps_stale` fails. |
| R500-2-S1 | RESOLVED | Both failed re-stages publish VD_LEN and their UNREAD bits through `nvm_choose:337`; `fallback_restage` grades both. |
| R501-1-F1 | RESOLVED as unvalidated-SEQUENCE selection | `nvm_slot_read:153` takes SEQ only from a validated RAM image; `nvm_restage_once:230` checks CRC and chosen SEQ. Single-bit, alias and fallback checks pass; their controls fail. |
| R501-1-F2; R500-1-F2 | RESOLVED | Only changed staged bytes reset the budget; console honors backoff/exhaustion; `abandoned` survives later success. `dr2c_unchanged_set`, `dr2c_console` and recovery checks pass, including all bypass controls. |
| R501-1-F3; R500-1-F1 | RESOLVED | The port uses accumulated timer0 time. `time_base` applies +/-60-second PHC steps in windows, backoff and media waits, and crosses the timer wrap. PHC and nonaccumulation controls fail. |
| R501-1-F4 | RESOLVED | TX, RX and drain waits return failure and release chip select; permanent/delayed stall checks pass. Both unbounded-wait controls and ignored-return control fail. The additional cumulative deadline is independently graded. |
| R500-1-F3 | RESOLVED | Current-capture changes leave no stale first-dirty window; after-capture changes get a new window. Both original and exact-cursor boundary controls fail. |
| R500-1-F4 | RESOLVED | Binding and D3 walks have separate rollback scopes; apply/settle faults retain bindings, binding failure permits D3, failed undo closes. Isolation/order controls fail. |
| R500-1-F5 | Original missing controls RESOLVED | Tail verify/blank-check, tie, time, program refusal and read-failure checks now kill their controls. F1 above is a separate missing disagreement case. |
| R500-1-F6 | RESOLVED | README service section distinguishes counted bytes, model time and unmeasured CPU work, including callback/record-walk exclusions. |
| R500-1-S1 | Retained SUGGESTION, Tests | No hosted workflow references `test_ctrl_nvm.py`; the PR records this integration risk. Optional outcome: wire it into the CI contract or track a follow-up; verification is an executed lane job and selector test. |

For retained R500-1-S1, the examined artifacts are `.github/workflows/docs.yml`, `scripts/ci_events.py` and `test/test_ctrl_nvm.py`. The Tests lens requires regression evidence: changes to its shared codecs/build inputs can escape this suite when hosted CI omits it. Adding an executed lane job under the selector contract, or tracking that risk publicly, remains an optional improvement and leaves no additional lens unclean.

**Executed evidence and other examined paths**

- `scripts/run_campaign.py --repo <checkout> --jobs 16` ran independent campaigns and controls concurrently, with a foreground coordinator joining all workers. All **85 tasks returned 0**: five shapes, all 40 named checks per shape, and all 80 controls. The source campaigns made 1,578 runner invocations. Each task has raw output, runner commands/stdout and an rc file in `receipts/campaign/`; `receipts/campaign-summary.json` gives the totals. No build error or process timeout was counted as a control kill.
- The **3,126 power-cut cases passed**: three starting media states, both ports, four fractions inside every erase/page effect, and a representative cut on entering read-back. Each recovery commits another change and reboots. This is finite simulated coverage, not every physical cut position.
- Nominal maximum: **210 us** across each shape's suite. Slowed maximum: **2,190 us** at 4x4 and **2,189 us** elsewhere. At 1x1/8x8, ten slowed waits take 1,859 us, twelve take 2,189 us, and all slowed waits cause bounded program failures at 2,009 us, followed by recovery for a changed set. `call_deadline_ignored` and `deadline_per_wait` are caught.
- The RV32I freestanding builds executed for all five shapes. At 1x1/8x8, bss is **4,048/14,408 bytes**, text **11,773/11,777 bytes**, stage **3,344/13,264**, payload **136/576**, chunk **256**, store state **288**, clock/deadline **20**. Production storage is static; no heap/OS dependency was found. These are compilation/size results, not CPU execution measurements.
- Codec inspection covered mixed byte order, CRC-32/CRC16, identity, lengths, inventory, ascending IDs, erased spans and refusal ordering. The supplied suite compares byte-exact containers and the recorded 1x1/8x8 vector lengths, CRC and record offsets. The write path preserves the authoritative slot, programs ascending pages and promotes only after full byte-equal read-back. Dirty/inflight ownership, DR2a/b/c, page/journal guards, rollback and CLOSED paths were inspected and exercised.
- The requested source-base diff contains imported dev work. The final lane delta against integrated dev is **32 paths**, limited to `ctrl_nvm`, the docs-index row and FASTCONNECT's tie edit. All 39 imported changed paths match dev exactly except FASTCONNECT, whose additional delta is the reviewed tie amendment. The round-3 history has five commits on `7f8dc1b1`; merge `e2000ef9` has ordered parents `716d3213` and `28f9666f`. The shipping writer and recorded capture inputs are unchanged by this lane. No image/build input links the new module. The default-off switch and actual owner adapters remain integration work.
- The pinned processor writer's framing, independent binding/D3 ownership, rollback and retry contracts were compared with `nvm_state.h` and the firmware state machine. No lane HDL/CDC change exists. The abstract `settle()` hook cites #658's clip-before-release ruling; the synthetic owner does not prove real clipping, descriptor-memory debt containment or actual SET judges.
- Public historical executable receipts were read at [38e93660, review-evidence/665f1-r1](https://github.com/kebag-logic/milan-fpga/tree/38e93660c8e2d4c190a00e8538611de01fece598/review-evidence/665f1-r1), and their hashes match that directory's manifest. They identify `gates-215c3c0b`, not this head. Its builder result has physical calibration gate 11 **NOT RUN**. Current source results are publicly reported in [5999002886](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-5999002886); the assignment also reports the manager's full source static/builder/native banks passed at this head. Historical results are not relabelled as current-head evidence.

**Real limits, integrity and manager duties**

Physical calibration **NOT RUN**. No hardware or field campaign was performed; field skips are not hardware proof. The CPU time of this module, actual generated-header integration, the real flash's behavior, and the eventual event-loop/owner wiring remain unmeasured. The unchanged 24.5-ms capture gate concerns the shipping writer and supplies no CPU upper bound for this module. The timer requires exclusive ownership and sampling within one 32-bit wrap, as documented. Identical, unreported repeated corruption remains a stated limit distinct from F1's differing reads.

No full parent, processor, gPTP, synthesis or builder bank was rerun. No hosted result or skipped context is counted as an execution here; hosted/local-replica acceptance remains manager-owned. No prohibited CI runner, container, privileged action, shared install, source fix, commit, push, GitHub write or merge was used. All disposable trees are under `scratch/`, excluded from publication. Every foreground campaign/probe completed; no job remains running.

`receipts/integrity.log` and `.rc` prove the complete index and **1,041 superproject blobs/modes**, plus all required submodule bytes/modes/indexes:

| Submodule | Pin | Checked blobs |
|---|---|---:|
| protocol-processor | `ead8036035affd53ef4b29979190f2f4f67084c0` | 558 |
| gptp-processor | `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` | 104 |
| third_party/verilog-axis | `48ff7a7e2ef782cf778d47910cf85835c64b1bce` | 214 |

The optional `external` checkout was unused and uninitialized; its gitlink/index entry matches the head. Review-created bytecode caches were removed. Production bytes required no restoration, and the checkout has no tracked, untracked or ignored residue.

Portable reproduction from the packet directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_campaign.py --repo <exact-checkout> --jobs 16
PYTHONDONTWRITEBYTECODE=1 python3 scripts/probe_read_agreement.py --repo <exact-checkout> --jobs 2
python3 -B scripts/verify_integrity.py <exact-checkout>
sha256sum -c MANIFEST.sha256
```

The campaign and integrity commands return 0; the fault probe returns 1 on this head for the reproduced defect. Existing prerequisites are required; the scripts install nothing. `MANIFEST.sha256` is the publication allowlist, with relative paths; only listed files and REPORT.md are intended for publication.

The manager must publish the packet, keep R501-2-F1 open through R501-3-F1, obtain the correction and re-review the changed head, and reconcile both independent reviews. Source validation is separate from the final candidate against then-current dev; the manager owns that candidate build, source/hosted/local-replica acceptance, explicit merge authorization and post-merge containment. Issue #665 remains open for its other lanes. The shipping writer's separate generation issue #671 and codec-parity follow-up remain separate duties.

R501-3 FINISHED
