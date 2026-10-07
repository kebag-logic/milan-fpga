[R533] NEGATIVE - exact head a6e6916826448f81de2b779ca61a87a9f8c47278

Round R533-8 finds one MAJOR acceptance and integration defect: ACMP's binding requests do not reach the attached SRP adapter. The merge preserves both protocol implementations and satisfies the specified IRQ, wake, timer and access-bound checks, but the original conditional wiring requirement became applicable when F3 entered the base. The author's deferral to target integration is not a public scope decision. One wording-only RESIDUE also remains.

Reviewed tree: `819d9290c443690487fbc8123765a14a5ba4535e`. First parent: `f74b9403b330ce316eeec6f724846f16def98443`; second parent and assigned source base: `d8b355fe0f41d49dca6cae1cd8b3826e2edde364`. This is one merge commit with both parents intact. Review scope is the round-8 delta, with round-7 positive reviews as the baseline for unchanged F4 code.

I reconstructed the task from AGENTS.md, CONTRIBUTING.md, docs/README.md, issue scope, requirements and interfaces, then both parent diffs/history, before reading prior review findings. Authorities included `REQUIREMENTS.md:51`, `docs/reference/FR_NFR.md` sections 3.4.1/3.4.2 (NFR-SCOUT-03 and H-SRP), `docs/reference/MAILBOX_CONTRACT.md`, and the ACMP/SRP port headers. `INDEPENDENT-VERDICT.md` records my own negative verdict and five-lens ledger before that reconciliation. No other current-round review report was used. Short source paths below are relative to `sw/firmware/ctrl/` unless another repository path is given.

**R533-8-F1 | MAJOR | Conformance, RTL, Robustness, Tests, Docs | ACMP-to-SRP binding delivery is absent after F3 enters the base**

Artifacts: `app/ctrl_app.c:47`, `app/ctrl_app_srp.c:7`, `acmp/acmp.c:158`, `acmp/acmp.h:320`, `test/ctrl_image.c:19`, `srp/README.md:62`, `srp/README.md:257`; independent `binding_probe.py` and `receipts/binding-delivery.log`.

Authority: [frozen F4 assignment, Part B.4](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6030279477) requires: “Wire it in `ctrl_app` if F3 is in your base by the end; otherwise state the wiring as owed.” The [round-8 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6045716528) brings F3 into this base and directs composition of all four modules. It does not waive Part B.4. The original assignment also requires serialized ports under #678. `srp_mbx.h:97` documents refusal and retry after owed transmission and retained reception.

Evidence: `ctrl_app_compose` passes the caller's ACMP environment unchanged; ACMP sends its SRP request to `env->srp`. `ctrl_app_attach_srp` registers the SRP loop handlers and opens reception/ticks, but installs no binding delivery or pending-request owner. The image fixture uses a no-op ACMP stream callback and a separate direct binder. The README explicitly says the integrator still owns delivery and retries. This is an omitted acceptance item, not an inference that every application environment must be interchangeable.

The probe compiles unchanged production sources with a copy of the existing mailbox fixture. It starts all four modules, accepts BIND_RX followed by a valid PROBE_TX_RESPONSE, and observes ACMP requesting the expected stream. After another 320 ms of loop service, the attached SRP sink remains unbound. Direct delivery to `srp_mbx_bind` succeeds immediately. This reproduces at IF=1 and on both interfaces at IF=2. The required-behavior assertion fails once per tested interface; the direct-delivery controls pass. The wrapper's zero exit means reproduction succeeded, not that application delivery passed.

Impact: a successful ACMP exchange in the explicit composition does not produce the required SRP listener binding. There is also no composition-owned pending request to retry or cancel when the adapter refuses, or to deliver later unbind/replacement work. The adapter's recovery tests cannot establish this missing handoff. The size fixture and U6/F6 tests exercise module coexistence while leaving the port disconnected. The README's integration deferral conflicts with the frozen conditional requirement.

Required outcome: satisfy the assigned ACMP-to-SRP delivery in the explicit composition, preserving interface/sink identity, serialized service, refusal/retry and unbind/replacement behavior. Do not introduce synchronous callback reentry. Add integration checks that observe the attached SRP adapter after real ACMP input, with discriminating plants at one and two interfaces, and align documentation and measured fixtures. Alternatively, a maintainer must explicitly change the public acceptance contract; the reviewer cannot infer that decision from the author's handoff. Re-review the corrected head and its changed bounds/images.

Verification: the supplied required-behavior probe must pass without its direct-delivery workaround; verify refusal followed by recovery, cancellation/unbind and interface isolation through the same composed path, then rerun affected coverage, mutations and image measurements. The final attribution includes Robustness because continued service cannot progress an unowned request and no retry owner exists. The independent checkpoint initially assigned the other four lenses; no finding was removed to bank clean coverage.

**R533-8-R1 | RESIDUE | Docs | Checkout introduction still describes publication as future work**

Artifact: current PR body, `receipts/pr-body.md:156`. It says “After the manager publishes the new head, use this checkout recipe.” The exact head is already published, confirmed by the PR source identity and public review start. This retains R533-7-R1 and the remaining part of earlier publication-wording residues. Exact fix: replace that sentence with “Use this checkout recipe.” Leave the following “Set the” and recipe unchanged. This changes only tense, not a command, measurement, figure, verdict or technical claim. Verification is a reread of the published body. It does not make a lens unclean; F1 does.

**Applied lenses and evidence**

Conformance: compared the original Part B port/declaration/latency requirements and round-8 assignment against `app/ctrl_app_srp.c:7`, `app/ctrl_app.h:69`, `srp/srp_bounds.h:1`, `test/test_acmp_mbx.cpp:966` and `:1106`, and `docs/design/MAILBOX_SPLIT.md:715`. Receive channels are exactly ADP, ACMP, MAAP and SRP, with the event interrupt and no AECP bit. U6 sleeps before a valid SRP-only record, checks IRQ before allowing service to resume, and checks consumption. The binding handoff violates Part B.4 (F1).

RTL and architecture: compared both parent trees and resolved source/test artifacts in `receipts/merge-retention.log`. Every file under `hdl/` and `sw/mailbox/`, the mailbox contract, register map, and processor gitlinks match dev. The SRP adapter and loop match the round-7 F4 baseline; F3's ACMP implementation and `ctrl_app.c` match dev. ADP, ACMP and MAAP retain disjoint `MBX_N_IF` timer runs. SRP owns the shared centisecond consumer and no one-shot slot. Mailbox bus and firmware co-simulation checks pass. F1 is an architecture/port integration defect; no new HDL defect is alleged.

Robustness: examined `srp/srp_mbx.c`, `test/srp_rx_retry.cpp`, `test/srp_mbx.cpp`, `test/srp_app.cpp` and U6/F6. The unchanged adapter retains link-level reconciliation, malformed-PDU handling, bounded retained reception, original-arrival expiry, wrap handling, shared declarations, event/TX ordering, attach refusal and reentry protection. Existing executed regressions remain green. Exact-mask and SRP-only wake checks address idle progress; mixed-backlog tests retain bounded pass work. F1 leaves the new application's binding delivery/retry ownership absent, so this lens is unclean despite the adapter regressions passing.

Tests: checked conflict resolution in `test/ctrl_arms.py`, `test/test_ctrl_firmware.py`, `test/srp_arms.py`, `test/srp_mutants.py`, `test/acmp_review_mutants.py`, `test/test_acmp_mbx.cpp` and `sw/firmware/gtest/coverage.ratchet`. All 205 F4-parent and 219 F3-parent named TEST/TEST_F/TEST_P entries found by the inventory remain in the same files. This is a source-retention check, not the runtime test count. Both inherited image auditors remain available. U6's sleeping HAL prevents polling from concealing the IRQ defect; F6 ties the runtime pass measurement to the module formula. F1 demonstrates the cross-module behavior these checks do not cover.

Docs: checked `srp/README.md:38`, `:64`, `:255`, `sw/firmware/ctrl/README.md:127`, `docs/design/MAILBOX_SPLIT.md:715`, dependency inventory and exact public source/evidence records. R532-7-R1 now reads exactly “Retry after owed transmission commits and retained reception completes or expires.” The optional clarification says `refused` counts attempts, including retries. The bound table and conditional timing paragraph recompute. The integration deferral conflicts with acceptance (F1); checkout tense is R1. Documentation and generated-contract checks pass, which does not resolve that conflict.

The independent compiled-macro check obtains:

| Interfaces | ACMP, including ADP | MAAP | SRP | Shared event reads subtracted | Composed maximum |
|---|---:|---:|---:|---:|---:|
| 1 | 1,012 | 616 | 1,596 | 2 × 48 | 3,128 |
| 2 | 1,043 | 664 | 2,366 | 2 × 48 | 3,977 |

The table is `(taken-by pass + 1) × composed maximum`: event 9,384/11,931; full ACMP ring 34,408/43,747; full ADP ring 68,816/87,494; owed response 28,152/35,793 accesses. Rounded-down 10 ms access budgets are 1.06/0.83, 0.29/0.22, 0.14/0.11 and 0.35/0.27 microseconds. At one microsecond/access only the one-interface event envelope fits 10 ms; both event envelopes fit the 20 ms ACMP ceiling. These are conditional mailbox-access envelopes. CPU work, external callbacks and unavailable TX capacity remain outside this arithmetic; inherited ACMP pass counts are not SRP delivery bounds.

**Reviewer execution receipts**

All commands ran under foreground supervision; independent campaigns, coverage and image builds overlapped. Disposable builds and probes stayed under `scratch/`. The SDK archive checksum is `d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`; its verified compiler is version 14.3.0 targeting `riscv32-buildroot-linux-gnu`. The scoped simulator identity was verified as 5.050 before use. Commands, durations, return codes and original/normalized log digests are in receipt JSON files.

| Execution | Result and receipt |
|---|---|
| Full control suite/campaign, required RV32, `--jobs 4` | PASS, IF=1/2, five shapes and processor-wire arms; 469/469 control plants, 108/108 SRP plants, six additional IF=1 plants and two pin controls; `receipts/ctrl-campaign.log` (rc 0, 1,409.168 s) |
| Existing 100% coverage ratchet, `--check --jobs 4` | PASS, 22 files; SRP 469/469 lines and 438/438 branches; application SRP 12/12 and 8/8; `receipts/coverage.log` |
| Mailbox from an exact-head archive, `make -j16 VBUILD_JOBS=2` | PASS: WB 382, AXI 427, co-simulation 32; IF=2 WB 384, AXI 429, model 369; five quick plants caught; `receipts/mailbox.log` |
| MAAP wire differential and self-test | PASS: 12 positive tests and 16/16 planted defects; `receipts/maap-differential.log` |
| Both inherited linked-image auditors | PASS: two F3 and four SRP-composed images; all six ELF hashes match exact-head public measurements; `receipts/f3-images.log`, `receipts/srp-images.log`, `receipts/image-comparison.log` |
| Inherited image controls | PASS, 33/33; `receipts/image-controls.log` |
| Bound arithmetic, parent retention, generated contract | PASS; `receipts/bound-table.log`, `receipts/merge-retention.log`, `receipts/generated-contract.log` |
| Documentation and CI contract | PASS; `receipts/docs.log`, `receipts/ci-contract.log` |
| Independent ACMP-to-SRP delivery probe | Required behavior FAILS at IF=1 and both interfaces at IF=2; direct-port controls PASS; `receipts/binding-delivery.log` |

Each of the six round-8 plants was caught by its assigned observable at **both IF=1 and IF=2**. `receipts/four-way-plants.log` records the failed assertions and hashes; the twelve individual logs are under `receipts/four-way-if1/` and `receipts/four-way-if2/`.

| Plant | Named failed observable at each interface count |
|---|---|
| `four-way-srp-irq-missing` | U6 exact four-channel receive and event interrupt mask |
| `four-way-srp-wake-missing` | U6 idle loop wakes for SRP alone |
| `four-way-acmp-enable-lost` | U6 four receive channels and no others |
| `four-way-unbound-irq-enabled` | U6 exact four-channel receive and event interrupt mask |
| `four-way-bound-drops-srp` | F6 four modules count each shared event record once |
| `four-way-bound-duplicates-events` | F6 four modules count each shared event record once |

The first two intentionally use the same missing-IRQ mutation to discriminate two separate assertions. They are six named controls, not six distinct source changes.

The linked SRP fixture measurements are:

| Shape | IF | text | rodata | data | bss | reserved stack | RAM span |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1×1 | 1 | 43,400 | 2,878 | 0 | 22,888 | 8,192 | 77,376 |
| 1×1 | 2 | 44,724 | 2,878 | 0 | 34,248 | 8,192 | 90,064 |
| 8×8 | 1 | 43,352 | 2,878 | 0 | 37,640 | 8,192 | 92,080 |
| 8×8 | 2 | 44,704 | 2,878 | 0 | 63,752 | 8,192 | 119,536 |

The F3 profile totals are 46,664/57,020 bytes for 1×1/8×8, excluding stack. These auditors measure distinct fixtures, not the shipping image or routed resources. Runtime input source digests match the public packet; local archive container hashes differ, while all six linked ELF hashes and measured sections match. No byte-identical archive-container or link-map claim is made.

**Prior public findings reconciled at this head**

The [round-7 external verdict](https://github.com/kebag-logic/milan-fpga/pull/690#issuecomment-6041323333) and [round-7 internal verdict](https://github.com/kebag-logic/milan-fpga/pull/690#issuecomment-6041452190) supply the unchanged-F4 baseline. Earlier finding bodies were read only after the independent pass and checkpoint. “Resolved, retained” means the reviewed fix and relevant source/tests survive the merge, with current executions where stated; it does not claim an unchanged dependency's entire upstream suite was rerun.

| Prior IDs | Disposition and exact-head evidence |
|---|---|
| R533-1-F1; R532-1-F1 | Resolved, retained. Milan immediate IN withdrawal and LV original deadline: unchanged adapter/pin, `test/srp_mbx.cpp`, `test/srp_walk.cpp`, SRP campaign. |
| R533-1-F2; R532-2-F1 | Resolved, retained. Attach/poll read current link level and clear stale lifecycle state; unchanged adapter, lifecycle regressions/plants. |
| R533-1-F3; R533-2-F1 | Resolved, retained. Shared StreamID reconciliation and binding-replacement inheritance in `srp_mbx.c` and `test/srp_mbx.cpp`. |
| R533-1-F4 | Resolved, retained. Image auditors and public historical comparisons survive; current six ELF/section measurements reproduced. These measurements do not resolve new F1. |
| R532-1-F2, parts 1–2 | Resolved, retained. 75% boundary and strict Ready-to-ReadyFailed output tests/plants in `test/srp_mbx.cpp` and `test/srp_mutants.py`. |
| R532-1-F2, part 3; R533-2-F2 | Resolved, retained. Required upstream note 4/5 tests are public at the unchanged lwSRP pin: `third_party/lwSRP/tests/integration_test.c:327` and `:352`, reversals in `tests/check_reversals.py:74` and `:185`. No fresh full upstream suite claimed. |
| R532-2-F2 | Resolved, retained. Public exact submodule pin initialized successfully; `docs/reference/SUBMODULES.md`, `THIRD_PARTY.md`, and docs checks agree. Hosted acceptance remains separate. |
| R532-2-F3; R532-2-F4 | Resolved, retained. Final never-eligible VID release and lifecycle/shared-VLAN controls; `reset-keeps-owed-domain`, `reset-keeps-sink-vlan`, `shared-ready-uses-first-vlan` remain in the campaign. |
| R532-3-F1; R532-3-F2 | Resolved, retained. Shared-Applicant inheritance and final Domain-VID guard exercised by retained tests/plants and stated in `srp/README.md`. |
| R533-5-F1; R532-5-F1 | Resolved, retained. Recoverable reception preserves/retries the accepted record; `test/srp_rx_retry.cpp` retains all 17 cases and corresponding plants. |
| R532-6-F1 | Resolved, retained. Original-arrival 1,000 ms expiry, distinct discard accounting, later-input progress, wrap/recreation/flood tests and plants are unchanged from round 7 and execute in this campaign. |
| R532-6-F2 | Resolved, retained. Public base/round-5 size attribution remains; round-8 deltas over round 7 are +14,688/+14,800/+14,704/+14,816 bytes in table order. Current images reproduced; historical images not relinked again. |
| R533-6-F1 | Resolved, retained. Mailbox archive recipe now names existing paths and includes the NVM header dependency; fresh exact-head archive suite passes. |
| R532-1-S1; R532-1-S2; R532-1-S3; R532-2-S1 | Addressed/retained at the pinned dependency and adapter: LeaveAll scope, generic LV/rJoin indication, participant recreation guard, and Milan-only MSRP behavior retain their tests/plants. |
| R532-5-S1; R532-5-S2; R532-6-S1; R532-7-S1 | Addressed/retained: timer-cancellation wording, future-version/whole-PDU atomicity tests, pending-event wording, and unsuccessful-attempt counter clarification. |
| R532-1-R1; R532-1-R2; R532-2-R1; R532-3-R1; R532-5-R2 | Resolved, retained: tick units, object-only size description, public dependency fetch instructions, obsolete STOP/compiler text, and notes-merge publication wording. |
| R532-2-R2; R532-5-R1; R532-6-R1; R533-6-R1; R533-7-R1 | Main publication-status text resolved; remaining checkout-introduction tense retained explicitly as R533-8-R1. |
| R532-7-R1 | Resolved exactly at `srp/README.md:64`: “completes or expires.” Verified by `check_bounds.py`. |

The reviewer-owned completion ledger is:

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN — F1 | #665 Part B.4 and round-8 assignment; `app/ctrl_app.c:47`; `app/ctrl_app_srp.c:7`; binding probe; bound-table receipt | R533-8, applied; no clean covering round for this merge | a6e6916826448f81de2b779ca61a87a9f8c47278 |
| RTL | UNCLEAN — F1 | `acmp/acmp.c:158`; `app/ctrl_app_srp.c:7`; both parent trees; merge-retention and mailbox receipts | R533-8, applied; no clean covering round for this merge | a6e6916826448f81de2b779ca61a87a9f8c47278 |
| Robustness | UNCLEAN — F1 | `srp/srp_mbx.h:97`; `test/srp_rx_retry.cpp`; U6/F6; binding-delivery receipt | R533-8, applied; no clean covering round for this merge | a6e6916826448f81de2b779ca61a87a9f8c47278 |
| Tests | UNCLEAN — F1 | `test/test_acmp_mbx.cpp:966`; `test/srp_mutants.py:611`; campaign, coverage and binding-delivery receipts | R533-8, applied; no clean covering round for this merge | a6e6916826448f81de2b779ca61a87a9f8c47278 |
| Docs | UNCLEAN — F1 | `srp/README.md:62` and `:257`; `docs/design/MAILBOX_SPLIT.md:715`; exact issue acceptance and published body | R533-8, applied; no clean covering round for this merge | a6e6916826448f81de2b779ca61a87a9f8c47278 |

**Evidence limits and remaining duties**

The [public source packet](https://github.com/kebag-logic/milan-fpga/tree/60ce747fdc9f10e928c87525f3dbc5c5bdaa9780/review-evidence/665f4-r1/author-r8), [review-ready record](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6046592070), and manager evidence comments were examined. `audit_public.py` independently hashes all 100 retained logs underlying 102 zero-exit records. Author campaign and MAAP differential raw logs were not retained there; both were executed independently for this review. The reported complete source static/builder/native banks belong to manager/author evidence, not my local execution. Physical calibration was NOT RUN; field skips are not hardware proof.

The one exact-head hosted snapshot records 11 successful contexts, eight still running and one skipped physical context. Successful shards are executed evidence; the skipped physical job is not. `changes` and `full-ci-gate` success alone do not establish unfinished suites passed. This is not final hosted acceptance. The manager owns hosted/local replication acceptance and the final candidate built against current dev; assigned source base and stated live dev were both `d8b355fe0f41d49dca6cae1cd8b3826e2edde364`. No candidate-merge or post-merge containment claim follows from these source checks.

All review campaigns finished. `receipts/integrity-final.log` verifies the exact head/tree, all 1,208 root tracked blobs, executable/symlink modes, exact index entries and absence of hidden index flags. Required submodules are at their committed gitlinks, with all 936 tracked blobs and their indices/modes also checked: protocol processor `ead8036035affd53ef4b29979190f2f4f67084c0`, timing processor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, lwSRP `9197193e47a6bb1c45a56d90a18c1784123aba44`, and stream library `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. Working-tree status is clean, including untracked files. `git diff --check` passes. No restoration of production bytes was necessary because probes mutated only disposable copies. Recorded unit memory peak was 6,127,013,888 bytes, below its 12 GiB cap.

`REPRODUCE.md` and the packet scripts reproduce the focused checks and defect probe. The first `binding-probe` receipt preserves a superseded wrapper counting error; the final `binding-delivery` receipt fixes that assertion and is the evidence used here. Logs retain original and normalized hashes; path substitutions are documented. `MANIFEST.sha256` selects the public files and receipts. Disposable trees and unselected input snapshots are excluded.

The manager must resolve F1 publicly, obtain corrected-head independent review, carry R1 to the residue checklist, and complete required hosted acceptance, final current-dev candidate validation, authorized merge and post-merge containment. The PR remains partial to #665. No source fix, commit, push, GitHub write, merge, author contact, external review delegation or hardware operation was performed.

R533-8 FINISHED
