[R532] NEGATIVE - exact head cce554f64f6bdab1f6d26e5c4d7b46d54d228c52

# R532-6: internal cleared-context review of PR #690 (issue #665, lane F4), round 6

- Role: internal independent reviewer `[R532]`, cleared context. Assignment: issue #665 comment 6038730087 (round 6), review start PR #690 comment 6039684799.
- Exact head `cce554f64f6bdab1f6d26e5c4d7b46d54d228c52`, tree `c27f9958d4f5a2f86e9cfcb34316d00213e6d28d` (verified, `receipts/integrity.txt`).
- Delta reviewed: Round 5 head `500b8f64` to this head. That is the `--no-ff` merge `06987495` of dev `e21c1ca0` (F2), the lwSRP re-pin to public main `9197193e`, and commits `45e5803a`, `fcc1e8d9` and `cce554f6`. Lane base: `db9aa8c9` (FC r2 head).
- Verdict: **NEGATIVE**. There is one MAJOR (F1) and one MINOR (F2), plus one RESIDUE (R1).
- The round-6 assignment items themselves are met: the retained-record retry, the unchanged R533-5 probe at IF=1/2, the F2 merge, the composition and 100 % coverage with no new exclusion. F1 is a new robustness defect that the retry design introduces. A single wire-valid MSRP PDU can make the retained record unrecoverable, and then every later SRP record and every binding change waits forever.

## Findings

### F1 - MAJOR - Conformance, RTL, Robustness, Tests, Docs - a retained receive record that can never fit blocks all SRP reception and binding indefinitely

- **Where:**
  - `sw/firmware/ctrl/srp/srp_mbx.c:401` retains the refused record.
  - `:352` gates all later SRP reception on it, for every interface.
  - `:291` refuses every `srp_mbx_bind` while it is held.
  - `:649` retries it once per poll with no bound and no exit except success, destroy or a reset of its own interface's link.
  - `:122`: the receive-interest filter admits every Class A Domain value (any priority, any VID), and each distinct value is a separate attribute instance.
  - `sw/firmware/ctrl/srp/README.md:84-90` documents waiting and "Storage recovery completes the payload on the next eligible poll". `:35` says the filters "retain only the Class A Domain".
- **Authority / evidence:**
  - The round-6 assignment (issue #665 comment 6038730087) requires the retry "on the next poll, or on storage recovery, within the bounded service", without losing later attributes.
  - The pinned lwSRP receive contract (`third_party/lwSRP/src/include/shish_lan/mrp.h:270-283`, `:356-360`) says a refused receive "stops later attributes", leaves "earlier events ... applied", and must be replayed "after recovery".
  - The replay re-applies the earlier events. Their JoinIn keeps refreshing the attributes the same PDU created, so those attributes never age out, and the storage that blocks the retry is held by the retry itself.
  - Reviewer probe `scripts/r532_hol_probe.cpp` (runner `scripts/r532_probe.py`) uses the tree's own fixture and the generated entity-sized pool, with no artificial exhaustion. It offers one valid MSRP PDU of N Class A Domain vectors on interface 0, then an ordinary Listener withdrawal on the last interface:

| Head | IF | N (PDU bytes) | Result after 30 simulated s |
|---|---|---|---|
| this head | 1 | 2, 12, 20 | applied; withdrawal received (control) |
| this head | 1 | **30 (233 B)**, 150 (1073 B) | record still retained; `received` frozen at 1; `refused` above 3,000,000; pool still full (33 blocks); withdrawal **never** received |
| this head | 2 | 2, 12, 20, 30 | applied |
| this head | 2 | **150 (1073 B)** | retained forever; the withdrawal on **interface 1** is never received |
| Round 5 `500b8f64` | 1 and 2 | 30, 150 | record dropped (counted malformed, the round-5 defect); withdrawal received by t+5 s; pool recovers by t+20 s |

  - Receipts: `receipts/probes/hol-if{1,2}.log`, `receipts/probes/hol-r5-if{1,2}.log`, built from `scripts/r532_hol_probe.cpp` and `scripts/r532_hol_probe_r5.cpp`. The Round 5 tree is an export of `500b8f64` with lwSRP `a4cbe41d`.
  - At this head the Talker licence stays active for about 15 to 20 s after the peer's withdrawal. It ends only when the local LeaveAll cycle expires the registration, not when the Leave arrives.
  - **Ordinary-size PDUs reach it too.** Probe `scripts/r532_flood_probe.cpp` sends 60 separate frames carrying one Class A Domain value each, which is the R532-5 wire-only flood, then a Listener Lv (`receipts/probes/flood-*.log`).
    - At this head a Domain record is retained (`pending=30` bytes), and the Lv is applied and the licence revoked only after **18.2 s** at both IF=1 and IF=2.
    - At IF=1 a record is still retained after that, with the pool still full.
    - The Round 5 control revokes in the same pass (0 ms), because it drops the overflowing Domain frames as malformed.
  - My R532-5 probe, re-run unchanged at this head (`receipts/probes/r532-5-exhaustion-if{1,2}.log`), reproduces the same 60-frame case as `ProbeDomainFloodThenRapidListenerLeave`: still active 3 s after the Lv.
- **Impact:**
  - One peer PDU carrying more retained attributes than the free pool can hold causes a permanent SRP outage on every interface. At IF=1 that threshold falls between 20 and 30 Class A Domain values, a 233-byte frame.
  - No later Listener or Talker registration, withdrawal or Domain change is processed.
  - The ACMP-facing `srp_mbx_bind` returns false forever.
  - Withdrawals are delayed from LeaveTime to the LeaveAll cycle: 18.2 s after a 60-frame Domain churn, and indefinitely after one oversize PDU.
  - The loop never sleeps: the waiting record keeps the RX level set and the refused Domain change reports owed work. Every pass re-parses the retained PDU.
  - Only a link reset of the originating interface clears it, and normal operation does not produce one.
  - Round 5's behaviour (drop and count) lost the partial PDU but healed itself. This head trades that for an outage with no end.
- **Required outcome:**
  - A refused record whose completion cannot be guaranteed must not block later SRP input on any interface, or the binding port, without bound.
  - For example, bound retention by the original arrival's service or protocol deadline, or detect a refusal that persists although the record's own replay holds the storage. Then discard it once, count it in a distinct counter (neither `received` nor `malformed`), and let MRP's own refresh recover.
  - Keep the R533-5 recoverable cases passing.
  - State the bound in `srp/README.md`, and correct "retain only the Class A Domain" to say that every Class A Domain value is retained.
  - Add an IF=1/IF=2 regression with a wire-valid PDU that exceeds capacity, followed by later input on another interface, and a plant that removes the bound and must fail it.
- **Verification:** at IF=1/2, re-run:
  - `scripts/r532_hol_probe.cpp`: N=30 and N=150 must complete or be discarded, and the later withdrawal must be received within its LeaveTime budget;
  - `scripts/r532_flood_probe.cpp`: revocation within the rapid-leave budget;
  - `scripts/r533_5_independent.cpp`;
  - the lane's `srp_rx_retry.cpp`;
  - the SRP campaign.

### F2 - MINOR - Conformance, Docs - linked-size report omits the delta from base although the image grew 7968 to 9312 bytes

- **Where:**
  - PR #690 body, "Known limitations", size bullet.
  - Issue #665 comment 6039666970 ("Four exact-head ... links").
  - Author packet `review-evidence/665f4-r1/author-r6/HANDOFF.md`, "Linked size and timing".
- **Authority:** the F-lane acceptance addition (issue #665 comment 6030870481) requires the linked image "for the shipping shape and the largest supported shape, with the delta from its base". Round 5 published a prior/new/increase table; round 6 publishes only absolute spans and says "Pools are unchanged".
- **Evidence:** I reproduced both heads with the CI-pinned RV32 SDK (installed into scratch by `scripts/ci_rv32_sdk.py`, archive sha256 `d42680e9...`) and identical runtime inputs (`receipts/size-*.log`, `receipts/size-r5-*.log`).

| Shape / IF | Round 5 `500b8f64` | This head | Delta |
|---|---:|---:|---:|
| 1x1 / 1 | 54592 | 62560 | +7968 |
| 1x1 / 2 | 65840 | 75152 | +9312 |
| 8x8 / 1 | 69280 | 77264 | +7984 |
| 8x8 / 2 | 95296 | 104608 | +9312 |

  - The head spans equal the author's published figures exactly.
  - Symbol attribution at 1x1/IF=2 (`receipts/size-symbol-delta.txt`): `image_app` +2172 B (the F2 MAAP state), `image_srp` +1528 B (the retained `struct mbx_frame`), and about 5 KB of MAAP and composition text.
- **Impact:** the largest shape is now at 80 % of the about 128 KB block-RAM budget the acceptance addition tracks. A 15 % one-round growth and its causes are absent from the public record.
- **Required outcome:** publish the delta from the lane's base (or from Round 5) for both shapes and both interface counts, with the attribution: MAAP composition, and the retained-record buffer per adapter.
- **Verification:** the published table matches `receipts/size-*.log` and `receipts/size-r5-*.log`.

### R1 - RESIDUE - PR #690 body - stale publication wording

- **Where:** PR #690 body, "Status", second and third sentences of the first paragraph and the first sentence of the second.
- **Problem:** "The candidate is unpushed." and "PR #690 already contains Round 5 `500b8f64443777685e6a54049d933476710d26f0`." are false now that `cce554f6` is the published PR head.
- **Exact fix:** replace them with "PR #690 head is Round 6 `cce554f64f6bdab1f6d26e5c4d7b46d54d228c52`."
- Wording only. It changes no figure, test, code or claim.

### S1 - SUGGESTION (non-blocking) - `sw/firmware/ctrl/srp/README.md:88`

"Each poll retries after earlier events, ticks and owed output": the gate (`rx_order_ready`) waits for all owed ticks and pending events, including those posted after the record's arrival. Consider "after pending events, ticks and owed output".

## What was checked, by lens (independent pass, completed before reading any prior review)

### Conformance
- **Assignment items (6038730087).**
  - Retain and retry, with record, interface, order and arrival kept: `srp_mbx.c:349-401`, `:577-579`, `:647-653`.
  - Later attributes and records are kept, and lifecycle and link-reset fences hold. Reviewer probes `R532.RetainedLeaveThenQueuedReadyApplyInArrivalOrder`, `R532.RetainedFirstInterfacePrecedesLaterInterface` (IF=2), `R532.LinkResetDuringExhaustionCancelsAndRecreatesCleanly` and `R532.RepeatedRefusalAcrossTicksAppliesOnceAfterRecovery` all pass at IF=1/2 (`receipts/probes/head-r532-if*.log`).
  - Only malformed input counts as malformed: `R532.OnlyMalformedInputCountsMalformed`.
  - The unchanged R533-5 `independent.cpp` (sha256 `72318b58...`, equal to the R533-5 published manifest) passes 4/4 at IF=1 and IF=2 with no peer retransmission: `withdraw/recovery: active=0 received=2 malformed=0 stops=1` (`receipts/probes/head-r533-if*.log`).
- **lwSRP pin.** `9197193e` is the current public `main` (checked against the remote) and includes merged PR #15.
- **Composition.** `ctrl_app_start_maap` plus `ctrl_app_attach_srp` (`app/ctrl_app.c:36-60`, `app/ctrl_app_srp.c:7-19`): the receive mask is ADP|MAAP|SRP plus EVT, the centisecond tick is enabled, the filter is opened, and an attach refusal leaves ADP/MAAP intact. The ADP and MAAP timer slots are distinct, per `srp_app.cpp:59`.
- **Unclean only by F1** (the bounded-service clause) **and F2** (the size acceptance addition).

### RTL (firmware architecture, loop and port contracts; no HDL source change in the delta)
- `git diff 500b8f64..HEAD -- hdl` is empty.
- Loop contract `loop/ctrl_loop.h:13-26`: RX and EVT are level causes (`docs/reference/MAILBOX_CONTRACT.md:29`). In a target-like servicing model, a sleeping loop retries on the next centisecond tick and completes 10 ms after recovery (`R532.SleepingLoopRetriesOnTickWithoutPeerInput`).
- A successful retry returns `owed=false` with a later record still queued. That is correct only because RX is a level cause; noted, not a finding.
- The retained `struct mbx_frame` copy is self-contained (`mbx/mbx.h:45-51`). The lane test overwrites the loop's shared frame before recovery.
- The bind-port contract change is documented at `srp_mbx.h:96-97`.
- **Unclean by F1:** stall, backpressure and liveness. The loop never sleeps and the binding port is refused without bound.
- The `tb/verilator/mbx/Makefile` change is imported from F2. The mailbox suite at this head (tracked export, pinned Verilator 5.050, wrapper sha256 `905795b9...`) passed: Wishbone 316, AXI4-Lite 361, cosimulation 13, two-interface 316/361/316 checks, and 5 of 5 mutants (`receipts/runs/mbx.log`).

### Robustness
- **Covered and passing at IF=1/2:** mixed and partial payloads, repeated refusal across 60 ms of ticks, retained MVRP, a failed participant recreate, link reset during exhaustion, another interface's reset, and destroy. Lane tests plus my probes.
- **Seven reviewer plants** in disposable full-tree exports (`scripts/r532_plants.sh`, `scripts/r532_matrix.sh`, `receipts/plants/`). The unplanted head-export control passes all three suites at IF=1 and IF=2.

| Plant | Caught at IF=1 and IF=2 by |
|---|---|
| `retry-removed` | R533-5 probe, my probes and lane `srp_rx_retry.cpp` |
| `retain-dropped` | R533-5 probe, my probes and lane `srp_rx_retry.cpp` |
| `refusal-malformed` | R533-5 probe, my probes and lane `srp_rx_retry.cpp` |
| `overtake` | my probes and lane |
| `reset-keeps` | my probes and lane |
| `retry-ignores-order` | lane `RetainedReceiveWaitsForOwedTransmit` |
| `reset-any-interface` | lane `OtherInterfaceResetPreservesRetainedPayload` at IF=2; an equivalent mutant at IF=1 |

- **Unclean by F1:** a maximum-size or adversarial but wire-valid input.

### Tests
- **Firmware gate**, both shards: `test_ctrl_firmware.py --require-rv32 --self-test --mutation-shard {0,1} 2 --jobs 4` exits 0 (565 s and 555 s).
  - 98 + 98 = 196 control/MAAP plants and 90 of 90 SRP plants caught in each shard; both pin controls refuse.
  - All arms pass: model, port, adp, unit, walk, entity, rv32, maap, maap_debug, maap_if2, reentry, lwsrp, and SRP at IF=1/2 (mailbox 53, debug 3, recovery 11, composition 2, latency 5, processor wire 5) for all five entity shapes on host and RV32 (`receipts/runs/fw-shard{0,1}.log`).
  - The 20 SRP plants added this round (`srp_mutants.py:512-574`) appear in the log, each with its named test and observable.
- **Coverage:** `fw_coverage.py --check --jobs 4` exits 0; 19 files at 100 % lines and branches after exclusions (`receipts/runs/coverage.log`).
  - The exclusion table (`sw/firmware/gtest/README.md`, "Coverage exclusions") is byte-identical at `500b8f64`, `e21c1ca0` and this head, with 14 rows. No new exclusion.
- **Unclean by F1:** no case covers a refusal that cannot recover (the boundary of "repeated refusal").

### Docs
- **F2 merge re-derived.** `git merge-tree 500b8f64 e21c1ca0` conflicts only in `sw/firmware/ctrl/README.md`, `test/test_ctrl_firmware.py` and `gtest/coverage.ratchet`. The recorded merge differs from the automatic result only in those three files (`receipts/merge-tree.txt`).
  - Both sides are kept in each. The F2 `--jobs` default (CPU count) yields to the lane's 1-4 clamp, and CI passes `--jobs 4` (`.github/workflows/rtl-fast.yml:281`). The ratchet takes the merged-source totals, and `--check` passes.
  - The clean auto-merges (`ctrl_arms.py`, `ctrl_mutants.py`, `gtest/README.md`) keep both sides.
- **Docs gates at this head** (`scripts/docs_gates.sh`, `receipts/docs/summary.txt`): 27 commands, all exit 0. They include `check_em_dash.py --base e21c1ca0`, `docs_check.py`, the submodule-diagram generator check, `check_submodule_docs.py`, `check_diagram_pngs.py`, `gen_toc.py --check`, the idiom checks, `ci_events.py --check`, `gen_mailbox.py --check` and the wire-accountability check.
- **Corrected claims verified.**
  - The timer-removal claim (`gtest/README.md:418`) matches `mrp_app_destroy` (lwSRP `src/core/mrp_mad.c:919-939`).
  - The Round 5 no-adaptation correction is at `srp/README.md:243-245`.
  - The pin text matches the gitlink: `SUBMODULES.md:26,199-200` and `ctrl/README.md:139-141`.
- **Unclean by F1** (the README recovery and filter text) **and F2.**

## Reviewer-owned lens ledger (this round)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | assignment 6038730087 and acceptance addition 6030870481; `srp_mbx.c:349-401,577-579,647-653`; `app/ctrl_app.c:36-60`, `app/ctrl_app_srp.c`; lwSRP `mrp.h:270-283,356-360`; R533-5 probe at IF=1/2 | R532-6 | cce554f64f6bdab1f6d26e5c4d7b46d54d228c52 |
| RTL | UNCLEAN (F1) | `ctrl_loop.h:13-26`, `ctrl_loop.c:119-176`; `srp_mbx.c:291,349-353,647-653`; `srp_mbx.h:96-97`; `MAILBOX_CONTRACT.md:29`; mailbox Verilator suite log | R532-6 | cce554f64f6bdab1f6d26e5c4d7b46d54d228c52 |
| Robustness | UNCLEAN (F1) | probes `r532_retry_probes.cpp`, `r532_hol_probe.cpp`; 7-plant matrix at IF=1/2; Round 5 control export | R532-6 | cce554f64f6bdab1f6d26e5c4d7b46d54d228c52 |
| Tests | UNCLEAN (F1) | `srp_rx_retry.cpp`, `srp_app.cpp`, `srp_latency.cpp:142-168`, `srp_mutants.py:512-574`; both shard logs; coverage log; exclusion-table comparison | R532-6 | cce554f64f6bdab1f6d26e5c4d7b46d54d228c52 |
| Docs | UNCLEAN (F1, F2) | `srp/README.md:35,84-90,120-124,243-245`; `ctrl/README.md`; `gtest/README.md:346-350,413-420`; `SUBMODULES.md:26,199-200`; PR #690 body; merge re-derivation; 27 docs gates | R532-6 | cce554f64f6bdab1f6d26e5c4d7b46d54d228c52 |

## Prior public findings at this head (read after the verdict and ledger above were written)

- **Sources:** my own R532-5 report and the R533-5 report (`review-evidence/665f4-r1/reviews/R533-5/REPORT.md` on the public evidence branch). Their disposition tables carry rounds 1 to 4 forward.
- **Rounds 1 to 4:** I re-checked each against this head through the named plants, all caught in both shards of my gate run (`receipts/runs/fw-shard{0,1}.log`). The checked plants are `delayed-in-listener`, `delayed-in-talker`, `short-leave`, `milan-rapid-leave-leaks-to-mvrp`, `cancelled-link-never-recovers`, `attach-ignores-current-link`, `short-link-interruption-ignored`, `rebind-loses-shared-applicant`, `consecutive-rebind-loses-applicant`, `unbind-shared-listener`, `last-ineligible-vid-leaks`, `reset-keeps-owed-domain`, `reset-keeps-sink-vlan`, `shared-ready-uses-first-vlan`, `joining-binding-loses-applicant`, `applicant-inherited-across-streams`, `final-unbind-withdraws-domain-vid`, `admission-ceiling-ignored`, `ninety-percent-ceiling`, `readyfailed-ignored`, `failed-init-leaks`, `malformed-uncounted` and `walk-leave-shortened`.

| Finding | Disposition at `cce554f6` |
|---|---|
| **R532-5-F1 / R533-5-F1** (MAJOR, refused receive dropped as malformed) | **RESOLVED for the recoverable case, as assigned.** See the bullets below this table. The unrecoverable case it now creates is **new finding R532-6-F1**. |
| R532-5-R1 / R532-2-R2 (PR body publication tense) | The text it cited is gone. The new body carries new stale wording, **retained as R532-6-R1** (RESIDUE). |
| R532-5-R2 (`srp/README.md` called the notes merge local) | **RESOLVED.** `srp/README.md:193-196` cites PR #15 merged at `9197193e`. |
| R532-5-S1 (stale timer-removal claim) | **ADDRESSED.** `gtest/README.md:415-420` now matches `mrp_app_destroy` (`mrp_mad.c:919-939`). |
| R532-5-S2 (no adapter wire case for the dependency's higher-version and whole-PDU rules) | **ADDRESSED.** See the bullets below this table. |
| R533-1-F1 / R532-1-F1 (Milan immediate leave) | RESOLVED, retained. The rapid-leave and #608 plants are caught. |
| R533-1-F2 / R532-2-F1 (link lifecycle) | RESOLVED, retained. The lifecycle plants are caught, and retained receive is cancelled by a reset of its own interface only. |
| R533-1-F3 / R533-2-F1 (shared declarations) | RESOLVED, retained. The shared-binding plants are caught. |
| R533-1-F4 (linked size) | RESOLVED, retained. The four head spans reproduce exactly. The missing round delta is the new **R532-6-F2**. |
| R532-1-F2 / R533-2-F2 (admission, ReadyFailed, notes 4/5) | RESOLVED, retained. The notes 4/5 tests are merged upstream as lwSRP PR #15, inside the pin; their upstream suite was not re-run here. |
| R532-2-F2 (submodule docs) | RESOLVED, retained. `check_submodule_docs.py`, the diagram check and `docs_check.py` exit 0. |
| R532-2-F3, R532-2-F4, R532-3-F1, R532-3-F2 | RESOLVED, retained. Their plants are caught. |
| R532-1-S1, R532-1-S2, R532-1-S3, R532-2-S1 | ADDRESSED or RESOLVED, retained. |
| R532-1-R1, R532-1-R2, R532-2-R1, R532-3-R1 | RESOLVED, retained. |

- **R532-5-F1 / R533-5-F1 evidence:**
  - The unchanged R533-5 probe passes 4/4 at IF=1/2.
  - My unchanged R532-5 probe (`receipts/probes/r532-5-exhaustion-if*.log`) now revokes 100 ms after storage release for the rapid leave, against 19.7 s at round 5, and within 200 ms after release for the LeaveTime case, with `malformed+0`.
  - Its in-exhaustion expectations encode the fail-closed alternative, which round 6 did not choose. Deferral until recovery is the assigned design and is stated at `srp/README.md:120-124`.
  - The retry-removal, record-loss and refusal-as-malformed plants are caught by the lane, by R533-5 and by me.
- **R532-5-S2 evidence:**
  - `srp_rx_retry.cpp:240` (`WholeInvalidPduIsMalformedAndFutureUnknownMessageIsSkipped`) fails, at IF=1 and IF=2, under each of three dependency plants committed in disposable clones: L5 (higher-version skip removed), L6 (per-value skip instead of whole-PDU rejection) and L7 (the validation pre-pass removed).
  - The unplanted control passes (`receipts/lw-plants.txt`, `receipts/probes/lw-*.log`).

## Real limits

- Host model only. No target timing, no booted image, no hardware, and no physical calibration (NOT RUN). Field skips are not hardware proof.
- I did not run lwSRP's own unit and behaviour suites at the pin, because their unit-test framework is not installed on this host. The pin is public `main` with merged PR #15.
- I did not run the builder bank, the compiler-absent check, `test_ctrl_nvm.py`, the MAAP differential, or the full 75-command docs bank. My docs subset is listed in `receipts/docs/summary.txt`.
- The size fixtures were linked, not booted. The runtime inputs (LiteX `a1e1c365`, picolibc and compiler-rt data packages) are recorded in `receipts/runs/fetch-runtime.log`.
- The public author packet `author-r6/` holds only `HANDOFF.md` and `PR-BODY.md`. The `ROUND6-*` receipts it cites are not published. Every figure I rely on above was re-executed independently.
- The F1 threshold depends on the generated pool shape. I measured it only for `endstation_ax7101_1x1_tdm8` at IF=1 (between 20 and 30 values) and confirmed it at 150 values for IF=2.
- Hosted checks at this head were still running when read (`receipts/hosted-check-runs.tsv`): 16 success, 4 in progress (Verilator shards 1, 2 and 4, and docs-check), and 1 skipped (the physical gPTP context, nightly/manual only). They are not counted here.

## Pending manager duties

- Carry R1 to the residue checklist.
- Route F1 and F2 to the executor.
- Hosted and local-replica acceptance at the final head.
- The builder bank and the compiler-absent check.
- Candidate merge validation against live dev `e21c1ca0`, and post-merge containment.
- Publication of this packet.

## Receipts

Every publishable file is listed in `MANIFEST.sha256`, with paths relative to the packet root. Scratch (exports, builds, SDK, runtime sources) is not published.

- `scripts/`:
  - the probe sources: `r532_retry_probes.cpp`, `r532_hol_probe.cpp`, `r532_hol_probe_r5.cpp`, `r532_flood_probe.cpp` and `r532_flood_probe_r5.cpp`;
  - the unchanged `r533_5_independent.cpp` (sha256 `72318b58...`) and `r532_5_exhaustion_probe.cpp` (sha256 `24e5ed79...`, as published in R532-5);
  - the runner `r532_probe.py`, the plant and matrix drivers, `lw_plants.sh`, `docs_gates.sh`, `integrity.sh`, `fetch_runtime.sh`, `size_probe.py` and `bg.sh`.
- `receipts/runs/`: firmware shards, coverage, mailbox suite, docs bank and runtime fetch, with `.rc` files in the form `<rc> <seconds>s`.
- `receipts/probes/`: head probes, the head-of-line and flood probes, their Round 5 controls, and the dependency plants.
- `receipts/plants/`: the 7-plant matrix.
- `receipts/docs/`: the 27 docs gates.
- `receipts/size-*.log`, `receipts/size-r5-*.log` and `receipts/size-symbol-delta.txt`: linked sizes.
- `receipts/merge-tree.txt`, `receipts/hosted-check-runs.tsv`, `receipts/integrity.txt`, `receipts/sdk-install.log` and `receipts/lw-plants.txt`.
- Local absolute roots in receipts and scripts are normalized to `$PACKET`, `$REPO`, `$PRIOR_PACKET`, `$PINNED_VERILATOR`, `$DOCS_ENV`, `$SDK_ARCHIVE_DIR`, `$VERILATOR_IMAGE`, `$HOME` and `$DATA`.
- How the runs were executed:
  - Probes and plants ran in the foreground with at most 6 parallel builds.
  - The firmware shards, coverage, mailbox and docs runs were started as detached processes and waited on in foreground commands.
  - Planted copies were disposable exports under scratch.
  - The review clone was never edited. After all probes it is byte-identical to the head, with clean submodules at their gitlinks (`receipts/integrity.txt`, rc 0).

R532-6 FINISHED
