[R533] NEGATIVE - exact head 42a0371affceb2a07a734449d706be01fa5abc9a

R533-2, external independent delta review of issue #665 / PR #690. One MAJOR remains in shared-binding reconciliation; one MINOR test finding remains partly unresolved. All five lenses were applied. This is not merge approval.

Tree: `ab9bd75e4d779adcc76aa958f696f6259ed72bb7`. Requested source delta: `db9aa8c9b135b34ff3d070a979dee70440b37cc6..42a0371affceb2a07a734449d706be01fa5abc9a`. The prior review head is `50d492c12789e1d80bf11f547e7fe53e02b4bdb9`; merge `8b43aed6126c39483ce20e37f0644d34f6f30696` brings in dev `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c`. The required lwSRP gitlink is `23d9a8173b07503a0ee6e8528f922fceab4e67f0`.

The independent source pass, initial verdict and reviewer-owned ledger were written before reading the prior public findings. `receipts/independent-pass.md` records that initial result. No private author material, lane scratchpad, other current-round report or management checkout was read. All probes changed disposable copies only. No source fixes, commits, pushes, GitHub writes, merge, hardware operation, shared installation or delegated review occurred.

Public scope came from the issue body and its bare-metal, testing and per-interface directives, the [F4 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6030279477), [size acceptance](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6030870481), [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6033558691) and [STOP ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6034653240). Authorities included AGENTS.md, CONTRIBUTING.md, docs/README.md, REQUIREMENTS.md section 1, FR_NFR.md NFR-SCOUT-03/H-SRP, the mailbox contract/design, the split ownership contract, Milan v1.2 and IEEE 802.1Q-2018. Standards hashes are recorded without redistributing their text. The public author evidence was read after the independent diff pass: archive `fa19435a86a1569f84db12b001a9823694d2736d`, then [author-r2 at 95f80a0a](https://github.com/kebag-logic/milan-fpga/tree/95f80a0ae28c7341dcdb43fc37c61819031fec1f/review-evidence/665f4-r1/author-r2).

**R533-2-F1 | MAJOR | Conformance, RTL, Robustness, Tests, Docs | Shared binding replacement loses the shared declaration state**

Artifact: `sw/firmware/ctrl/srp/srp_mbx.c:306`, `:313`, `:509`; `sw/firmware/ctrl/test/srp_mbx.cpp:568`; `sw/firmware/ctrl/srp/README.md:47`; PR #690's shared-declaration claim. This retains R533-1-F3 under its original five lenses.

Authority/evidence: IEEE 802.1Q-2018 35.1.2.2 and the accepted round-2 requirement require the per-interface StreamID declaration to reflect every accepted binding. The existing mixed-binding arrival orders now work, but an overlapping rebind still breaks the shared ownership:

1. Bind sinks 0 and 1 to the same StreamID and VID 2. Sink 0 expects destination ending `09`; sink 1 expects destination ending `0A`.
2. Register the Talker Advertise for destination `09`. Both per-sink declaration caches record the shared Ready declaration.
3. Successfully rebind sink 0 to destination `0A`. No binding now matches the registered Talker.
4. The rebind retains the shared Applicant because another binding exists, then clears sink 0's cache with `memset`. Reconciliation chooses sink 0 as representative, sees desired=0 and declared=0, skips the withdrawal, and copies zero into the other cache.
5. The actual Applicant still transmits Listener Ready: the independent wire capture observes event 3 / subtype 2 at 1000 ms and 2000 ms, with no Lv.

`probe_shared_rebind.cpp` reproduces this against unchanged production code at both IF=1 and IF=2. Each execution fails its two wire assertions; the ordinary 41-case suite at each interface count passes. See `receipts/probe-rebind-if1.log` and `receipts/probe-rebind-if2.log`.

Impact: an accepted rebind leaves a stale Ready reservation and can keep the upstream Talker transmitting even though no local binding is eligible. Per-sink bookkeeping falsely reports no declaration, preventing subsequent polls from repairing it. The documented support for different destinations/VIDs and the accepted rebind test requirement remain unsatisfied.

Required outcome: preserve the actual shared Applicant declaration across binding replacement and representative changes. Reconcile the resulting declaration against all accepted bindings, including the transition to no eligible user. Any unsupported replacement must refuse atomically. Keep the shared-binding contract and evidence accurate.

Verification: the supplied wire probe must pass at one and two interfaces. Exercise replacement/removal of the lowest and higher sink slots, destination and VID changes, overlapping rebinds and final-user removal. Require withdrawal when the final eligible request disappears, continued Ready when one remains, and no stale renewal. Retain the existing arrival-order and identical-binding controls.

**R533-2-F2 | MINOR | Tests | Required upstream note 4/5 regression remains unverified from public state**

Artifact: `third_party/lwSRP/src/core/mrp_mad.c:494`; pinned `third_party/lwSRP/tests/unit/integration_test.c` and `tests/check_reversals.py`; public `author-r2/HANDOFF.md`, Upstream dependency section; issue #665 comment 6034642528. This retains only the unresolved third part of R532-1-F2.

Authority/evidence: round-2 assignment 6033558691 explicitly requires discriminating upstream tests for Table 10-3 notes 4 and 5. The public handoff says those tests and three guard reversals exist on the unpushed topic `495520f5e02dd077fc9b1451942b25ec95afa1b8`, outside the reviewed pin. The pinned test files do not contain those added cases. The public repository commit query returns HTTP 422, "No commit found for SHA"; see `receipts/upstream-test-topic-query.json`. The archive supplies reported results and hashes, but not that executable test change or its raw logs. It therefore does not allow independent verification of the remaining test fix.

Impact: the previously identified regression gap cannot be cleared from the reviewable artifacts. This does not assert a new Applicant implementation defect, and it is not a finding about the authorized later move of the lwSRP pin.

Required outcome: publish the test topic and reproducible named results, establishing that both PointToPointMAC values exercise note 4's VO/VP and note 5's rIn behavior and that removing each guard fails its intended observable. The tests may be reviewed against this pin's production bytes; the separately authorized integrated-pin update remains a later delta.

Verification: inspect the published test change, verify its production-source equivalence to the dependency under review, run the positive cases and three reversals, and explicitly re-review this retained MINOR.

**Prior public finding disposition**

The [R533-1 findings](https://github.com/kebag-logic/milan-fpga/pull/690#issuecomment-6032452765) and [R532-1 findings](https://github.com/kebag-logic/milan-fpga/pull/690#issuecomment-6032564515) were read after the independent verdict and ledger. No submitted or inline reviews were present in the read-only inventory.

| Prior item | Disposition at this head | Evidence |
|---|---|---|
| R533-1-F1 / R532-1-F1, Milan immediate Leave | RESOLVED | MSRP-only opt-in in `msrp.c:400` and `mrp_mad.c:558`; immediate Listener and Talker tests pass at IF=1/2. Independent delayed-IN plant fails both. Restarted-LV plant fails the original-deadline test. D1, README and published PR body now cite Milan 4.2.7.2.2. Independent MVRP tests retain IN-to-LV and the original 5000 ms deadline. |
| R533-1-F2, short link interruption and old RX | RESOLVED | `on_event`, `reset_interface`, `receive`, `mbx_rx_mark/before`; adjacent-edge, backlog, down-link, peer-interface and owed-output cases pass at IF=1/2. The independent fence-boundary plant is caught. |
| R533-1-F3, shared declaration | RETAINED as R533-2-F1 | Arrival-order repair passes, but the independently reproduced overlapping rebind retains a stale Ready Applicant. |
| R533-1-F4, linked composition size | RESOLVED | Independently rebuilt all four head rows and eight FC/dev comparison rows; all sections, static-storage sizes and spans equal ROUND2-SIZE.json. All 57 provisioned runtime inputs match the public provenance hashes. |
| R532-1-F2, admission and ReadyFailed | RESOLVED for these two parts | Exact boundary rates discriminate tag overhead, preamble/IFG and the 75% ceiling. Strict active Ready-to-ReadyFailed mock rejects the callback glitch. All four former escapes were replanted and caught by name. |
| R532-1-F2, note 4/5 | RETAINED as R533-2-F2 | The reported upstream test-only topic is not publicly retrievable; no claim of execution of those unpublished cases is made. |
| R532-1-S1, LeaveAll scope test | ADDRESSED | Pinned `integration_test.c` contains `msrp_leaveall_changes_only_the_message_type_and_port` and its per-type/per-port assertions. Parent Run-B differential passes. |
| R532-1-S2, generic LV/rJoin indication | RETAINED SUGGESTION | The extra generic indication remains at `mrp_mad.c:341/347`. This adapter compares Domain values and recomputes retained registrations. The public handoff supplies the requested reason; manager should carry the optional bridge-use concern to dependency PR #12. It does not dirty a lens. |
| R532-1-S3, failed participant recreation | ADDRESSED | Partial allocation is destroyed, both pointers clear, failure is counted, and poll retries while advancing past the failed interface. Allocation-failure and surviving-interface tests pass at IF=1/2. |
| R532-1-R1, TICK wording | RESOLVED | SRP README now states centiseconds; NOW_MS is separately milliseconds. |
| R532-1-R2, missing size limitation in PR body | SUPERSEDED/RESOLVED | The requested linked measurement now exists and is in the published PR body. Adding the obsolete object-only limitation would be incorrect. |

No new wording-only RESIDUE is reported. The shared-binding claim affects code, wire behavior and conformance, so it cannot be classified as RESIDUE.

**Independent lens evidence and reviewer-owned ledger**

Conformance: compared the Milan IN/rLv replacement, generic MVRP Table 10-4 timing, unchanged LV deadline, Domain defaults/restart and Listener declarations against the standards. Reviewed tagged Ethernet admission arithmetic, 75% boundary, FourPacked subtype handling and D1/D2. Startup, #608, malformed input and selected processor wire cases pass. F1 prevents clean coverage.

RTL: reviewed firmware/interface architecture, the shared Applicant owner, link events, RX fencing, callback discipline, static allocation, bounded loop service and owed-frame commit ordering. F4 changes no RTL against merged dev. The source-base delta includes dev's AAF change; it is retained byte-for-byte. Software ownership remains inside this lens, so F1 prevents clean coverage.

Robustness: applied short/coalesced link, stale backlog, stable down-link, exhaustion/recreation, peer isolation, full TX ring, reentry, duplicate/invalid bind and replacement cases. Existing checks pass; the overlapping rebind fails at both interface counts. F1 remains open.

Tests: ran the exact-source adapter, selected wire differential and desk latency arms at IF=1/2; largest-shape RV32 objects; independent generic MVRP timing; eight compiled mutation controls; and all 12 linked-size fixtures. Inspected the unchanged exclusion policy and the 100% ratchet claims without rerunning the complete coverage bank. F1 exposes a missing accepted transition case; F2 retains the unreviewable upstream test fix.

Docs: compared public scope, SRP/API documentation, PR body, D1/D2, TICK units, measured-size scripts/tables and stated target-integration limits. The size, Milan and lifecycle changes now have concrete evidence. The assertion that all accepted shared bindings are reconciled is still contradicted by F1.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN, F1 | Milan 4.2.7.2.1/.2; IEEE 802.1Q-2018 10.7/35.1.2.2; `srp_mbx.c`; `mrp_mad.c`; wire and MVRP receipts | R533-2, applied | 42a0371affceb2a07a734449d706be01fa5abc9a |
| RTL | UNCLEAN, F1 | `srp_mbx.c:283/488`; `ctrl_loop.c`; `mbx.c`; mailbox contract; `receipts/merge-audit.json` and `merge-resolution.diff` | R533-2, applied | 42a0371affceb2a07a734449d706be01fa5abc9a |
| Robustness | UNCLEAN, F1 | `srp_mbx.cpp` lifecycle/exhaustion/shared cases; `probe_shared_rebind.cpp`; stale-prefix mutation receipts | R533-2, applied | 42a0371affceb2a07a734449d706be01fa5abc9a |
| Tests | UNCLEAN, F1/F2 | `srp_mbx.cpp`, `srp_walk.cpp`, `srp_latency.cpp`, `srp_mutants.py`; pinned upstream tests; native, mutation, size and topic-query receipts | R533-2, applied | 42a0371affceb2a07a734449d706be01fa5abc9a |
| Docs | UNCLEAN, F1 | `srp/README.md:47`; PR #690 body; author-r2 tables; `ctrl_image.c/.py/.ld`; `ROUND2-SIZE.json` | R533-2, applied | 42a0371affceb2a07a734449d706be01fa5abc9a |

All lenses were applied; none is banked clean while F1 remains in its scope.

**Merge preservation**

The merge has the assigned ordered parents. All 35 paths changed solely by dev are byte/mode identical to dev at the merge. The only later difference among those paths is an additive RX-fence API block in `mbx.h`; no inherited line was removed. The eight conflicted files were reviewed through the remerge diff:

| Artifact | Both sides retained |
|---|---|
| `.github/workflows/rtl-fast.yml` | SDK/header checks and fail-fast shell; required F4 dependency, SRP arms and mutations |
| `scripts/ci_events.py` | Matching workflow contract and compiler-required refusal under the merged step name |
| `ctrl/README.md` | Freestanding/assertion/reentry guidance and SRP documentation |
| `test/ctrl_build.py` | RV32I/ILP32, stack-use output, assertion runtime allowance; compiler discovery remains shared |
| `test/ctrl_mutants.py` | Both reentry arms and original controls, with reusable isolated build paths |
| `test/test_ctrl_firmware.py` | Reentry/debug coverage plus SRP arms, shapes, dependency checks and mutations; one jobs argument |
| `gtest/fw_rv32.py` | Shared freestanding checker retained; no F4-only replacement |
| `gtest/fw_rv32_selftest.py` | Hostile assert-header probe and assertion use retained, including inherited executable mode |

The mailbox generator/crosscheck passes. CI contract check passes 1741 items. These focused checks support the merge audit; they do not replace the manager's full banks.

**Executed evidence**

| Execution | Result | Receipt |
|---|---|---|
| SRP adapter, IF=1/2 | 41 + 41 tests pass | `receipts/srp-if1.log`, `srp-if2.log` |
| Selected processor wire differential, IF=1/2 | 5 + 5 tests pass | `receipts/walk-if1.log`, `walk-if2.log` |
| Desk latency, IF=1/2 | 4 + 4 tests pass; maximum normal service 1.0204 ms under the stated envelope | `receipts/latency-if1.log`, `latency-if2.log` |
| Independent generic MVRP timing | 1 + 1 tests pass | `receipts/mvrp-if1.log`, `mvrp-if2.log` |
| Largest entity RV32 objects, IF=1/2 | 12 + 12 objects pass ABI/runtime/frame checks | `receipts/rv32-largest-if1.log`, `rv32-largest-if2.log` |
| Independent shared rebind | Fails on unchanged source at IF=1/2; stale Ready visible on wire | `receipts/probe-rebind-if1.log`, `probe-rebind-if2.log` |
| Independent delayed-IN, restarted-LV, fence-boundary and shared-aggregation plants | Four compiled defects caught by named tests | `receipts/mutation-results.json`, corresponding `.log/.rc` files |
| Replayed admission/tag/preamble and ReadyFailed controls | Four former escapes caught | `receipts/boundary-controls.rc`, four named logs |
| Linked composition | All 12 rows match published sections/storage/span exactly | `receipts/sizes/results.json`, per-row size/symbol/log/rc files |
| Runtime provenance | All 57 external source/header hashes match the public records | `receipts/runtime-input-hashes.json` |
| Mailbox contract and CI contract | Both pass | `receipts/mailbox-contract.*`, `ci-contract.*` |
| Final source integrity | Parent and four required submodules match raw blobs, modes and stage-0 indexes | `receipts/final-integrity.json` |

The four independent mutation definitions and hashes are in `run_mutations.py` and its JSON receipt. The delayed-IN plant fails both Listener and Talker tests. A compiler failure is never counted as a catch. Two reviewer-harness development corrections are disclosed in `receipts/probe-development.txt`; neither changed production code or any expected behavior.

**Linked composition measurements**

All numbers are bytes. BSS includes the static arena. Data is zero. Each span includes linker alignment and the explicit 8192-byte reserved stack. This is a reachable control/ADP/SRP size fixture, not a bootable image or a routed-resource claim.

| Shape | IF | text | rodata | BSS | arena within BSS | head span | FC span | delta from FC | dev span | delta from dev |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1_tdm8 | 1 | 27376 | 2846 | 15432 | 9920 | 53856 | 18752 | 35104 | 19200 | 34656 |
| 1x1_tdm8 | 2 | 28352 | 2846 | 25708 | 19840 | 65104 | 19248 | 45856 | 19696 | 45408 |
| 8x8 | 1 | 27360 | 2846 | 30184 | 24032 | 68592 | 18752 | 49840 | 19200 | 49392 |
| 8x8 | 2 | 28308 | 2846 | 55212 | 48064 | 94576 | 19248 | 75328 | 19696 | 74880 |

The original measurement is labeled `181e3e1ac62cf768532087ee647c94c554338c8c`. The later commits change tests and an inherited script mode, not the measured production/fixture inputs. This review rebuilt from the assigned final head and reproduced every row. Link-map/symbol inspection confirms retained `ctrl_app_start`, `ctrl_loop_run`, SRP init/attach/bind, MRP receive/transmit and static storage. No undefined or heap symbols remain. Stack reservation is not a whole-call-chain bound.

**Reproduction and publication**

Run from an exact-head source clone, with this packet's scripts kept together. Set SOURCE to the clone and PACKET to this packet. Runtime input directories must match the public provenance hashes.

```sh
python3 -B "$PACKET/run_focused.py" "$SOURCE" --jobs 8
python3 -B "$PACKET/run_mutations.py" "$SOURCE" --jobs 8
python3 -B "$PACKET/run_boundary_controls.py" "$SOURCE" --jobs 4
python3 -B "$PACKET/run_mvrp.py" "$SOURCE" --jobs 8
python3 -B "$PACKET/run_sizes.py" "$SOURCE" --picolibc "$PICOLIBC" --compiler-rt "$COMPILER_RT" --litex-software "$LITEX_SOFTWARE" --jobs 4
python3 -B "$PACKET/audit_merge.py" "$SOURCE"
python3 -B "$PACKET/verify_integrity.py" "$SOURCE"
```

The focused collector intentionally retains failing review probes separately; its exit zero means its baseline arms passed, not that F1 passed. Individual `.rc` files and test assertions carry each result. The mutation collector succeeds only when every named defect is detected. Foreground orchestration used at most eight concurrent compiler workers; independent runs were concurrent inside the foreground process. No background shell jobs or heavy synthesis runs were used. All generated trees, extractions and builds remain under packet `scratch/`, excluded from publication.

Publish REPORT.md and only the files named in MANIFEST.sha256. Hashes use paths relative to this packet.

**Real limits and pending manager duties**

The assignment reports passing full source static/builder and native banks at this head. This review did not rerun the prohibited full parent, processor, gPTP, synthesis or builder banks, nor the complete coverage campaign. The fetched public author archives contain result tables and hashes; they are not substituted for raw independently executed receipts. No hosted jobs were inspected. Hosted/act acceptance remains with the manager; skipped contexts and field skips are not execution or hardware proof.

The delayed builder function is explicitly accepted by comment 6034653240 and is not a finding. The later reviewed lwSRP-main pin is also not a finding. The manager must preserve those assignments, publish/review the note-4/5 test topic, carry the optional generic-callback concern upstream, and obtain a fresh verdict on F1/F2 fixes and any later changed head.

Source validation is distinct from the final current-dev merge candidate. The manager still owns candidate construction and complete candidate gates at merge time, exact-head hosted requirements, the remaining independent review, explicit merge authorization, and post-merge containment. This negative source verdict clears none of those duties.

F3 application wiring, live MAAP/stream configuration, the actual fabric licence port, target ingress/service/egress timing and physical release validation remain as publicly scoped integration obligations. H-SRP here uses 100 ns per mailbox access, one aggregate 1 ms CPU/preemption allowance and 100 ns uncertainty; its 11 ms full-ring control rejects the original budget. These are conditional desk measurements. Physical calibration was NOT RUN; no board, wire-departure or audio-soak proof is claimed.

Final verification hashes 1169 parent blobs and all tracked blobs in the protocol processor, gPTP processor, verilog-axis and lwSRP; it checks file/symlink modes, every stage-0 index entry, hidden index flags and all required gitlinks. There are no untracked or ignored generated files in those checkouts. The optional external gitlink remains unchanged and uninitialized. No restoration edit was necessary because mutations stayed in scratch copies.

R533-2 FINISHED
