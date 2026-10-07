[R533] POSITIVE - exact head edeef61c5a0cc6c18caa61db4019a8e378baf366

Round R533-9 finds no open source BLOCKER, MAJOR or MINOR. All five review lenses are CLEAN at this head. The round-8 binding, fixture, measurement and documentation defects are resolved in source and executable tests. Hosted success is still pending and is not implied by this verdict. This is a source review, not merge authorization or completion of issue #665.

Reviewed tree: `164108f28665ce5ad1a24f350bf28b056100cb56`. The two-commit delta is `a6e6916826448f81de2b779ca61a87a9f8c47278..edeef61c5a0cc6c18caa61db4019a8e378baf366`: `877c0b9d04078867e2bef481903745198527844c` adds delivery/tests/docs; the final commit changes only the coverage ratchet. Source base and observed live dev both equal `d8b355fe0f41d49dca6cae1cd8b3826e2edde364`.

I reconstructed AGENTS.md, CONTRIBUTING.md, docs/README, the issue's frozen acceptance and public decisions, requirements/interfaces, then the full source diff and round-9 delta/history, then public executable evidence. My independent verdict and five-lens ledger were written before opening prior review findings. Round 8 supplies the baseline for unchanged artifacts; no other round-9 review was read. Short paths below are relative to `sw/firmware/ctrl/` unless stated otherwise.

Authorities: [frozen F4 assignment, Part B.4](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6030279477), [round-9 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6047209532), [serialized-port ruling #678](https://github.com/kebag-logic/milan-fpga/issues/678), `REQUIREMENTS.md:23-56`, `docs/reference/FR_NFR.md:330-413`, `docs/design/MAILBOX_SPLIT.md`, `acmp/acmp.h` and `srp/srp_mbx.h:97-101`. The review start is [public](https://github.com/kebag-logic/milan-fpga/pull/690#issuecomment-6048276399).

**Round-8 findings reconciled at this head**

| Finding and original lenses | Disposition and current evidence |
| --- | --- |
| R533-8-F1, MAJOR; Conformance, RTL, Robustness, Tests, Docs | RESOLVED. `app/ctrl_app_srp.c:36-96` installs composition-owned intent storage and a delivery poll after the adapter's poll. `test/srp_binding.hpp:59-202` supplies real ACMP/mailbox cases. `binding_required.log` passes at IF=1 and both interfaces at IF=2 with the old direct-delivery block removed. Both `plants-if*.log` and individual receipts demonstrate the required discriminating failures. Updated binding contracts, zero-access check and independently reproduced images agree. |
| R532-8-F1, MAJOR; Tests | SOURCE/TEST DEFECT RESOLVED. `test/test_acmp.cpp:208-221` owns and zeroes the byte a relaxed source-count guard inspects. `a0-gcc.log`, `a0-clang.log`, `a0-asan.log` each show a pristine A0 pass and the plant failing exactly the named sources assertion, without a memory diagnostic. Hosted `firmware-unit` and aggregate `rtl-fast` success remain unverified in the captured snapshot; that remaining acceptance duty belongs to the manager. No current-head hosted failure was observed. |
| R532-8-F2, MINOR; Tests | RESOLVED. `test/srp_app.cpp:94-143` counts actual callback/driver accesses, including refused reception and a poll that demonstrably transmits. Seven standing bound plants are caught at both interface counts. The unmodified prior four `srp-*` probes are all caught at IF=1/2; their unplanted control passes. `run_prior_probes.py` rejects build refusals and requires the named suite to fail at each count. |
| R532-8-F3, MINOR; Docs | RESOLVED. `maap/README.md:134`, `test/test_acmp_mbx.cpp:20` and `test/acmp_review_mutants.py:398` now name `CTRL_APP_THREE_PASS_MAX`. The 1,580/1,659 figures retain their three-module meaning; four-module references carry 3,128/3,977. `check_bounds.log` independently compiles the macros and recomputes the table. |
| R532-8-F4, MINOR; Tests, Docs | RESOLVED. `README.md:143` narrows the mutation claim to exact-mask, SRP-only wake and algebraic-bound checks. All six related standing plants are caught at IF=1/2. It no longer claims named plants for every listed assertion. |
| R532-8-R1 and R2, RESIDUE; Docs | RESOLVED with the requested text at `README.md:44` and `:344`: the composition includes SRP attachment, and the 256-byte pool belongs to the separate historical fixture. |
| R533-8-R1, RESIDUE; Docs | RESOLVED. The current PR body says “Use this checkout recipe.” This also resolves the retained R533-7-R1 and earlier publication-tense residue. |
| R532-8-S2, SUGGESTION; Docs, Robustness | ADDRESSED. `app/ctrl_app.h:137` explicitly requires MAAP composition and documents storage lifetime, observer restrictions and recomposition before replacement. |
| R532-8-S1 and S3, SUGGESTION | Optional, unchanged. The F6 historical test name remains; the earlier F3 size table stays explicitly historical. Neither is claimed as fresh four-module measurement. No lens is left unclean by these optional items. |

**Applied lenses**

[R533] PASS Conformance - `app/ctrl_app_srp.c:36-96`, `test/srp_binding.hpp:59-202`, frozen Part B.4 and #678 - The callback copies stream identity, destination and VID into static storage; delivery uses the sink's configured interface and the original sink index. Refusal leaves intent pending. Unbind and replacement supersede it. Delivery occurs after SRP service returns, outside ACMP's guarded callback. The old probe now observes the attached adapter bound without calling its public binder directly. The unchanged MSRP/MVRP declarations, Milan immediate withdrawal, original LV deadline and selected processor-wire comparisons pass at both interface counts.

[R533] PASS RTL - `app/ctrl_app_srp.c:46-101`, `app/ctrl_app.h:72-146`, `loop/ctrl_loop.c:161-184`, `srp/srp_bounds.h:8-17`, `integrity.json`, `mailbox.log` - Checked serialized ownership, static sizing, attachment capacity, return-value handling, byte order and poll ordering. ACMP environment forwarding preserves the original callback context. Attachment reserves room for both polls before mutation; repeated wiring is refused. No HDL, mailbox YAML/generated contract or register-contract bytes differ from the source base. Disjoint one-shot timer runs and the shared centisecond consumer remain intact. The actual delivery poll adds zero mailbox accesses; combined maxima remain 3,128/3,977. CPU work and external callback costs remain outside those counts.

[R533] PASS Robustness - `test/srp_binding.hpp:94-202`, `srp/srp_mbx.c:288-345,395-403,638-716`, `test/srp_rx_retry.cpp`, `native-if1.log`, `native-if2.log` - Verified real allocation refusal followed by recovery or original-arrival expiry, owed transmission followed by commit, cancellation of pending/accepted bindings, replacement identity, independent sink/interface state, and an earlier refusal not being erased by a later success. Pending work keeps service awake. Duplicate attachment, missing poll room, oversized sink shape and detached-adapter service are checked. Existing malformed-input, reset/link fencing, retained-payload, clock-wrap and shared-declaration cases remain green. The lifetime contract requires service to stop before storage is released; runtime detach/reuse beyond that contract is not claimed.

[R533] PASS Tests - `test/test_acmp.cpp:208-221`, `test/srp_binding.hpp`, `test/srp_app.cpp:94-143`, `test/srp_mutants.py:644-710`, `.github/workflows/rtl-fast.yml:277`, the receipts below - Each required new integration behavior kills its assigned source plant at IF=1/2. The source-count control fails through its intended assertion under both compilers and AddressSanitizer. Bound tests observe actual accesses and transmit progress. Native controls, old external probes, the coverage checker and mailbox gate all pass their expected grading. Intentional mutation failures are retained separately from pristine-suite passes. Hosted execution is recorded separately and remains pending.

[R533] PASS Docs - `README.md:123-146,341-344`, `srp/README.md:62-91,215-224,273-286`, `maap/README.md:134-135`, `docs/design/MAILBOX_SPLIT.md:715-747`, current PR body and public round-9 packet - Contracts now assign delivery/retry/cancellation to the composition, retain the no-reentry rule, and distinguish observer callbacks from delivery. The table still bounds mailbox accesses, not target time. Size fixtures, stack assumption, physical limits and manager duties are stated. Seven targeted documentation/contract checks pass; all 16 changed-source hashes agree with the public evidence record.

**Independent execution**

| Execution | Result and receipt |
| --- | --- |
| Six focused native suites at each interface count | 112 tests at IF=1 and 112 at IF=2, all pass: adapter 53, receive recovery 17, SRP composition 3, four-module composition 29, latency 5, wire differential 5. `native-if1.log`, `native-if2.log`. |
| Standing delta and four-way plants | 28/28 caught at each count: 14 new binding controls, seven bounds, six four-way controls and the inherited binding debug guard. `plants-if1.log`, `plants-if2.log`, `receipts/plants-if*/`. |
| Original external probes | Four understatements caught at both counts; control passes. `srp-*.log`, `control-none.log`, full logs under `receipts/external-*/`. Old binding probe passes without direct delivery: `binding_required.log`. |
| A0 compiler/sanitizer controls | Pristine pass plus named planted failure under gcc, clang and AddressSanitizer; no overflow diagnostic. `a0-*.log`. |
| Coverage `--check --jobs 4` | 22 files at 100% lines/branches after unchanged exclusions. Delivery: 63/63 lines, 32/32 branches; adapter: 469/469, 438/438. `coverage.log`. |
| Mailbox gate, tracked scratch export | PASS: WB 382, AXI 427, co-simulation 32; IF=2 WB 384, AXI 429, model 369; five quick plants caught. `mailbox.log`; scoped release identity checked before use. |
| Four RV32 linked fixtures | Every ELF SHA256, section count and static-storage measurement matches public ROUND9-SIZES. `image-comparison.json`, `image-*.log`; verified SDK and rebuilt runtime, 57 provisioned source inputs hash-matched. |
| Bounds and targeted documentation/contract checks | PASS. `check_bounds.log`, `docs-checks.log`. |
| Public evidence integrity | 107 recorded zero-exit source invocations; all 105 retained log byte counts/hashes match. Full control campaign and MAAP differential are hash-only there; this audit is not their independent rerun. `public-audit.json`. |

Measured SRP accesses at IF=1/2: event 1/1 (bound 1); refused reception 2/2 (bound 2); retained-receive poll 3/4; transmitting poll 48/91 (poll bounds 770/1,540); maximum TX and RX records 383 each; measured complete pass 388/389 (bounds 1,596/2,366). These measurements discriminate the planted omissions; they do not claim simultaneous saturation of every conservative term.

| Shape | IF | text | rodata | data | bss | reserved stack | RAM span |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1x1 | 1 | 44,264 | 2,878 | 0 | 23,432 | 8,192 | 78,784 |
| 1x1 | 2 | 45,604 | 2,878 | 0 | 34,792 | 8,192 | 91,488 |
| 8x8 | 1 | 44,216 | 2,878 | 0 | 38,184 | 8,192 | 93,488 |
| 8x8 | 2 | 45,584 | 2,878 | 0 | 64,296 | 8,192 | 120,960 |

Growth over round 8 is 1,408/1,424 bytes at IF=1/2: 544 BSS plus 864/880 text bytes. The binder is now reachable through ACMP; the artificial forced entry is removed. These are size fixtures with a reserved stack, not booted images or a whole-call-chain proof.

**Earlier findings retained as resolved**

The following retain round 8's reconciled status. I compared their artifacts against the delta and ran the current native cases. No fresh execution of every historical plant or unchanged upstream suite is claimed.

| Prior IDs | Current disposition and artifacts |
| --- | --- |
| R533-1-F1; R532-1-F1 | RESOLVED, retained: immediate MSRP leave and original #608 LV deadline; unchanged adapter/dependency, `srp_mbx.cpp`, `srp_walk.cpp`. |
| R533-1-F2; R532-2-F1 | RESOLVED, retained: attach/poll link-level recovery, lifecycle fences and recreation; `srp_mbx.c`, current lifecycle cases. |
| R533-1-F3; R533-2-F1; R532-2-F3; R532-2-F4; R532-3-F1; R532-3-F2 | RESOLVED, retained: shared StreamID reconciliation, replacement inheritance, final-user VID and Domain ownership; unchanged implementation/tests and current native execution. |
| R532-1-F2 parts 1/2 | RESOLVED, retained: admission ceiling and strict ReadyFailed callback cases; `srp_mbx.cpp`, `srp_mutants.py`. |
| R532-1-F2 part 3; R533-2-F2 | RESOLVED, retained: public pinned note-4/5 tests and reversals, `third_party/lwSRP/tests/unit/integration_test.c`, `tests/check_reversals.py`. Upstream suite not rerun. |
| R532-2-F2 | RESOLVED, retained: public exact gitlink, dependency ownership/licensing inventory and generated diagram inputs unchanged; submodule/docs checks pass. |
| R533-5-F1; R532-5-F1; R532-6-F1 | RESOLVED, retained: complete retained input, recoverable retry and original-arrival 1000 ms expiration; all 17 recovery cases run at IF=1/2. |
| R533-1-F4; R532-6-F2 | RESOLVED, retained: historical base comparisons remain public; current linked images and round-8 deltas reproduced. |
| R533-6-F1 | RESOLVED, retained: mailbox export uses existing paths and includes the NVM headers; fresh export passes. |
| R532-1-S1/S2/S3; R532-2-S1; R532-5-S1/S2; R532-6-S1; R532-7-S1 | ADDRESSED/RESOLVED, retained: LeaveAll scope, generic LV indication, recreation, Milan-only behavior, timer wording, atomic/future-version cases, pending-event wording and refusal-attempt semantics. Relevant source/tests remain unchanged. |
| R532-1-R1/R2; R532-2-R1; R532-3-R1; R532-5-R2; R532-7-R1 | RESOLVED, retained: tick units, linked-size scope, public fetch/status, merged-note wording and “completes or expires.” |
| R532-2-R2; R532-5-R1; R532-6-R1; R533-6-R1; R533-7-R1 | RESOLVED, including the final checkout-introduction tense, as R533-8-R1 above. |

**Reviewer-owned completion ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | Frozen B.4/#678; `app/ctrl_app_srp.c:36-96`; `test/srp_binding.hpp`; binding and native receipts | R533-9 | edeef61c5a0cc6c18caa61db4019a8e378baf366 |
| RTL | CLEAN | `app/ctrl_app.h:72-146`; `loop/ctrl_loop.c:161-184`; `srp_bounds.h`; integrity, bounds, mailbox receipts | R533-9 | edeef61c5a0cc6c18caa61db4019a8e378baf366 |
| Robustness | CLEAN | `srp_binding.hpp:94-202`; `srp_mbx.c:288-345,395-403,638-716`; receive-retry and binding receipts | R533-9 | edeef61c5a0cc6c18caa61db4019a8e378baf366 |
| Tests | CLEAN | `test_acmp.cpp:208-221`; `srp_app.cpp:94-143`; `srp_mutants.py`; A0, plants, external probes, coverage | R533-9 | edeef61c5a0cc6c18caa61db4019a8e378baf366 |
| Docs | CLEAN | ctrl/SRP/MAAP READMEs; `MAILBOX_SPLIT.md:715-747`; current PR body; public audit and size receipts | R533-9 | edeef61c5a0cc6c18caa61db4019a8e378baf366 |

**Real limits and pending manager duties**

`hosted-checks-final.json` is a read-only exact-head snapshot. At 2026-10-07 22:45:33 UTC, firmware-unit, yosys-elaboration, elaborate, docs-check and all five long simulation shards were IN_PROGRESS. The aggregate rtl-fast success was not yet available. Four Yosys shards, lint, BDD, wire-accountability, docs-check-no-git and selectors reported SUCCESS. Physical gPTP was SKIPPED. Executed and skipped contexts are not interchangeable evidence. The manager must obtain successful exact-head firmware-unit/rtl-fast and all required hosted contexts, and complete trusted local replication. This review does not clear that pending acceptance.

Physical calibration is NOT RUN. Field skips are not hardware proof. Mailbox-access counts and the conditional H-SRP host envelope do not establish target CPU, wire or physical timing. Live stream/MAAP configuration, fabric licence output and eventual shipping integration remain the documented target duties.

I did not run full parent, processor, gPTP, Yosys or builder banks, the full historical mutation campaign, hardware, or deployment. The public source evidence and manager's reported banks remain distinct from a final current-dev candidate. The manager must form and validate that candidate at the merge turn, finish both independent reviews with no round in flight, reconcile hosted acceptance, obtain maintainer merge authorization, and perform containment and public workflow updates afterward.

All review commands had foreground supervision and bounded concurrent children. No source fixes, commits, pushes or GitHub writes were made. Every disposable product is under packet `scratch/`. Final integrity checks prove all 1,209 parent blobs and all required initialized submodule blobs, modes and indexes match their recorded heads: processor `ead80360`, gPTP `5dce647a`, axis `48ff7a7e`, lwSRP `9197193e`. The unused external gitlink remains `efeb541a`, uninitialized. The checkout is clean; no probe restoration was needed because plants used disposable copies. No review command remains running.

`REPRODUCE.md` and the scripts make the focused checks repeatable. Receipt paths are normalized to public role aliases; original/published hashes are recorded separately. Publish only REPORT.md and files listed in MANIFEST.sha256. The manager owns publication; this review made no public write.

R533-9 FINISHED
