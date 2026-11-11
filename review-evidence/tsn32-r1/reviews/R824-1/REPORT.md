[R824] NEGATIVE - exact head 9043b926532dc4ffb57218ee0eebca7564262289

# R824-1: external independent review of kebag-logic/tsn-c-stack PR #34 (issue #32)

- Exact head `9043b926532dc4ffb57218ee0eebca7564262289`, tree `a77b293b7dd3c1d67ec853a12c672d3dd1d8733e` (verified in the reviewer's detached clone; `receipts/clone-integrity.txt`).
- Source base `main` `9deb0ddb` (#33, the #31 owed-release mask). The branch holds `fa31d4c8` (the walk), the merge commit `dd8b026f` and `9043b926`.
- Scope: the changed-sink walk of issue #32, its merge of #33, and acceptance items 1 to 4, checked against IEEE 1722.1-2021 8.2, Milan v1.2 5.5 and the code.
- Verdict: **NEGATIVE.** One MINOR finding is open (F-1, the parent consumer bar). The stack change itself is clean under every lens: behaviour equivalence, the merge, the plants, CI and coverage. The only other items are three RESIDUE wording fixes and three SUGGESTIONs.

## Reconstruction order and sources

1. `CONTRIBUTING.md` (the repository has no `AGENTS.md`), `README.md`, `docs/` (REQUIREMENTS, PORTING, VERIFICATION, TESTS, TRACEABILITY).
2. Issue #32 body. It has no comments, so the four acceptance items in the body are the frozen scope. There are no maintainer or manager scope comments on the issue.
3. Requirement ACMP-13 (new), ACMP-09, ACMP-10 and ACMP-12, and the port contract sections "ACMP changed-sink walk" and "ACMP machine storage".
4. The diff `9deb0ddb..9043b926`, and the history `ea4af6f..fa31d4c8`, `dd8b026f` and `9043b926`.
5. Public evidence:
   - milan-fpga archive `f5200b66`, `review-evidence/tsn32-r1`. All 79 manifest entries match their published SHA-256.
   - The hosted runs at the exact head.
   - The parent's public rulings and STOP reports on milan-fpga #665 and its PR #810.
6. Prior public review findings on PR #34: **none exist.** The PR has two comments, both review-start notices (R823-1 and R824-1). It has no review bodies and no inline comments. So nothing needs resolving or retaining at this head. My verdict and ledger were formed without reading any other reviewer's report.

## What I executed

All runs were on disposable clones under the packet's scratch area. Every script is in `scripts/` and every receipt in `receipts/`.

| Probe | Result | Receipt |
|---|---|---|
| Clean-clone CI: the `quality.yml` `run:` steps `validate.py --jobs 16 --graphs` and `baremetal.py --jobs 16` | 27 of 28 gates rc 0. The 28th, `clang-sanitizers-build`, rc 2: the pinned Clang 18.1.3 cannot compile against this host's libstdc++ 16 headers. That is a host limit, not a PR defect; see the next row and the hosted run. Mutation `{"CAUGHT": 470, "ESCAPED": 0, "ERROR": 0}`. `src/acmp.c` 847/847 lines and 436/436 branches. GCC CTest 10/10, `acmp_walk` passed. RV32 Debug and Release rc 0, with imports equal to `main`'s | `receipts/ci-head/` |
| Sanitizer gate (`-DTSN_SANITIZERS=ON`, `detect_leaks=1`, `halt_on_error=1`) with the host Clang 23.1.4 | configure, build and test rc 0; 10/10, `acmp_walk` passed | `receipts/sanitizer-host/` |
| Hosted runs at the exact head, inspected only (the manager owns hosted acceptance) | push run 42972778067 and pull_request run 42972806247: `quality` and `bare-metal` both completed success, every `run:` step executed. The push-run artifacts show 28/28 gates rc 0 under GCC 13.3.0 and Clang 18.1.3, mutation 470/0/0, `acmp.c` 847/847 and 436/436, and RV32 Debug and Release rc 0 | `receipts/hosted/` |
| **Independent differential against `main`'s real core.** `scripts/dwalk.cpp` links the head's `src/acmp.c` and `9deb0ddb`'s `src/acmp.c` (renamed `old_acmp_*`, built with its own header) side by side under ASan, UBSan and shift sanitizers. After every entry it requires identical port and environment traces (every frame byte by byte), identical return values, and an identical public view, binding latch, change-pending flag and `rx_ready` for every sink | **560 of 560 runs pass** (`matrix.rc` 0), about 9.4 M entries in total. Mask widths `ACMP_MAX_SINKS` 16, 32, 33, 64 and 255; sink counts 1, 8, 16, 32, 33, 63, 64 and 255; 8 seeds each. Modes: the author's test mix; LIFT (BIND/UNBIND reach sinks 32 and up, and transmit room is withdrawn at 33 sinks and more); REENTER (port callbacks, including the walk's own publish, admit, persist, changed and timer calls, try to re-enter with UNBIND_RX, `acmp_poll`, `acmp_set_started` or `acmp_restore_rollback`); NOOPEN (restore not followed by open, so marks persist across other entries) | `receipts/differential/matrix.txt` |
| Probe controls (planted copies of the head) | `c1` (`acmp_set_started` unmarked) is caught at step 15. `c2` and `c3` (the merged release loop marks the wrong word, or skips the mark for sinks 32 and up) pass the author-style 33-sink mix and fail under LIFT. The head's own `AcmpWide` tests catch both (`OwedResponsesHoldOnlyTheirOwnSinksChanges`, `SinksThirtyOneAndThirtyTwoWaitOnlyForTheirOwnResponses`). `c4` (probe-left marks word 0) is not observable here, because sinks k and k mod 32 share an interface in this map | `receipts/probe-controls-*.txt`, `receipts/differential/plant-*.diff` |
| Plant-table merge audit (`ea4af6f`, `fa31d4c8`, `9deb0ddb`, head) | 470 = 462 ∪ 452 by name, none dropped, none invented. 466 are equal to an unconflicted parent version. Only 4 differ: the two hand merges, each the walk's `mark(a, k)` with #31's word read or `k + 1u` release argument and the parents' kills, and #31's two release-loop plants re-anchored on the merged `if`, with #31's kills. Both parents' orders are kept, the 18 `walk-` plants are contiguous after `acmp-wide-release-clears-one-word`, and the last three are the entity plants | `receipts/plant-merge-audit.txt` |
| Kill words in my campaign | All 18 `walk-` plants are CAUGHT by "the changed-sink walk makes the full walk's calls". `acmp-unbind-srp-after-response` is CAUGHT by "A3 a settled sink stops SRP before the response"; `acmp-first-owed-releases-every-change` by "A19 the bind's response left but the unbind's is still owed". The re-anchored `acmp-wide-release-loop-word-ignored` and `-word-off-by-one` are CAUGHT by their #31 `AcmpWide` words. `acmp-timer-port-called-every-time` and `acmp-publish-stream-cache-stale` are CAUGHT by the new A17 and A31 assertions | `receipts/new-and-merged-plants.txt` |
| Merge survival (changed lines only) | `include/acmp.h`, `tests/test_acmp.cpp`, `test_acmp_walk.cpp` and `test_acmp_wide.cpp` are identical on both sides. `src/acmp.c` differs only at the one conflict line, the release loop, which carries both changes. `CMakeLists.txt` and `scripts/mutation.py` fold `tsn_walk`/`WALK` into `tsn_wide`/`WIDE`, with an identical definition, sanitizers and arm flags | `receipts/merge-survival.txt` |
| Host benchmark, the author's `bench_finish.c` rebuilt at `main` and the head (`ACMP_MAX_SINKS=32u`, one pinned CPU) | -O2: 558→124 at 8 sinks and 2,325→279 at 32 sinks. -Os: 961→217 and 3,844→434. This matches the PR's 558→124, 2,294→279, 961→217 and 3,844→465 within noise | `receipts/bench-reproduction.txt` |
| RV32 cost of the change (`acmp.c` object, `riscv64-elf-size`) | Debug text 21,429→22,189 B (+760), Release 20,365→21,077 B (+712). `struct acmp` grows by 8 B at 32 sinks or fewer | `receipts/rv32-acmp-size.txt` |

## Lens notes

- **Conformance.** The walk changes no observable behaviour. Under IEEE 1722.1-2021 8.2 and Milan v1.2 5.5.3 and 5.6.4 (frames, probe timers, SRP calls, persistence, Table 5.22 notices and admission), every call is the same in the same global order, so also in the same order per controller. This holds against `main`'s real core, not only against the head with every sink marked, and includes:
  - re-entry from inside the walk,
  - marks left pending across non-completing entries,
  - an entry changing a sink twice, such as a re-BIND of a settled sink or several timer kinds in one expiry,
  - UNBIND while frames are owed.

  Code reading confirms the invariant. Every writer of a field that `publish`, `rearm`, `admit`, `record_of`, `view_of` or `change_owed` reads runs under a mark before the next walk:
  - `bind`, `unbind`, `probe_response` and `acmp_adp_rx` (`src/acmp.c:888`, `:924`, `:1004`, `:1194`),
  - expiry (`:1223`, `:1230`, `:1235`),
  - the four entries (`:1252`, `:1268`, `:1282`, `:1296`),
  - the release and probe-left (`:1312`, `:794`),
  - restore and rollback (`:1367`, `:1392`).

  Init needs no mark, because `acmp_init` settles each sink's caches.
- **RTL.** No HDL is in this repository. For the hardware-facing build:
  - The freestanding RV32 build and the QEMU smoke test pass in my run and in the hosted run, and the core imports are unchanged.
  - Every new shift is bounded: `k % 32u`, `interface < n_interfaces ≤ ACMP_MAX_INTERFACES = 4`.
  - The code grows by about 0.7 kB, and that growth reaches the parent's soft-core image (F-1).
- **Robustness.**
  - Mask storage is sized from `ACMP_MAX_SINKS` on every new path: `ACMP_DIRTY_WORDS`, and the merged release loop's `o->release[k / 32u] >> (k % 32u)`.
  - It holds at 33, 64 and 255 sinks under shift, UBSan and ASan (the matrix).
  - Early-return paths set no mark, or set a superset that the next completion consumes.
- **Tests.**
  - Acceptance 1: four differential tests at 1, 8, 32 and 33 sinks.
  - Acceptance 2: each of the 15 mark sites, plus the interface bit and the two word reads, has a plant killed by the trace assertion.
  - Acceptance 3: coverage stays 100 % after exclusions, and Linux and bare-metal CI are rc 0.
  - Acceptance 4: the benchmark is stated and reproduced.
  - The 33-sink differential still runs with no owed frame at all (S-1). The merged release line at sink 32 is protected by #31's `AcmpWide` tests (probe controls `c2` and `c3`).
- **Docs.**
  - ACMP-13 is in the requirement record, `requirements.json`, origins, traceability and the port contract; the gates check that these agree.
  - The CHANGELOG keeps both entries.
  - The comment-rule scan of every added line in `src`, `include`, `tests/*.cpp`, `scripts`, `CMakeLists.txt` and the edited prose finds no lane label, review round, reviewer ID or issue-comment ID.
  - No public text in the delta or the PR body names a private host, tool or model. The PR body names a lane, which the owner rule allows.

## Findings

### F-1 (MINOR): the parent consumer bar is not met at this donor head

- **Lenses:** Tests, Robustness, RTL.
- **Where:**
  - milan-fpga `dev-soft-core` `1d6bf555` and live dev `46c971fa` both pin `third_party/tsn-c-stack` at `70936b77`, which is before #28 and #33.
  - The parent adapter calls `acmp_rx(&m->acmp, …)` and ignores its result (`sw/firmware/ctrl/acmp/acmp_mbx.c:111` at `1d6bf555`). #28 makes that result one ports must act on.
  - The S2b lane's public receipts: #665 issuecomment-6751120577 (round 25 STOP), issuecomment-6788757307 (round 26 STOP), and the PR #810 body.
- **Evidence:**
  - No published receipt runs the parent's firmware gates with the stack at `9043b926`, or with its port. The missing gates are `firmware-unit` (which carries the parent's own ACMP lock-step walk `sw/firmware/ctrl/test/acmp_walk.cpp` and `test_acmp_mbx.cpp`), `firmware-control-mutants`, `firmware-boundary`, `firmware-verilator`, the twin, and the image ledger.
  - The S2b lane measured only the load, with #32 ported to the old pin in a scratch build, and that port takes #31's word read back to one word, so it is not this head's code.
  - Round 26's final-head gate sweep at `0b37f3d2` was cut by host resets and is not re-run, and it ran at the unchanged pin.
  - The lane's own round 25 report and the PR #810 body record a consumer gate the donor change breaks: with tsn-c-stack#32 at the pin, the 8x8/2if `answering-every-port` image is 123,012 B, **132 B over its 122,880 B granule** ("the pin move owes it 132 bytes").
  - My RV32 measurement of the head confirms the growth: +712 B Release text in `acmp.c`.
  - The donor PR body does not state this consumer cost.
- **Impact:** the donor bar for this review includes the parent consumer gates. They are unproven at this head, and one known consumer gate (the image's rom fit) fails with the change applied. Merging does not move the pin, so nothing breaks today, but the regression is carried silently to the pin move.
- **Required outcome:** one of the following.
  - **(a)** Publish parent consumer gate receipts with the donor change applied at a scratch pin: the `firmware-unit`, `firmware-control-mutants`, `firmware-boundary` and `firmware-verilator` jobs and the image rom ledger. Use either this head with the adapter changes #28 requires, or the merged head's port. State each result, including the 132 B overflow or its resolution.
  - **(b)** A recorded maintainer or manager decision that this PR's donor bar defers the parent consumer gates to the pin move that carries #28, #31 and #32. In both cases the PR body must state the change's code-size cost and the known +132 B over-granule consumer effect.
- **Verification:** the receipts or the decision link are on the PR, and the PR body names the consumer cost.

### RES-1 (RESIDUE): REQUIREMENTS.md describes the mark order wrongly for restore

- **Lens:** Docs.
- **Where:** `docs/REQUIREMENTS.md:41`.
- **Defect:** the text says "Each entry marks a sink before it changes the sink's binding, state, timers or owed changes". But `acmp_restore_binding` (`src/acmp.c:1366-1367`) and `acmp_restore_rollback` (`:1390-1392`) reset the sink and then mark it. Behaviour is unaffected, because no walk runs in between.
- **Exact fix:** "Each entry marks a sink before the next walk reads it: before it changes the sink's binding, state, timers or owed changes, and, for `acmp_restore_binding` and `acmp_restore_rollback`, right after the reset."

### RES-2 (RESIDUE): VERIFICATION.md says every walk plant drops one mark

- **Lens:** Docs.
- **Where:** `docs/VERIFICATION.md:24`.
- **Defect:** "The 18 changed-sink walk plants each drop one mark". In fact 15 drop one mark site, one (`walk-mark-interface-dropped`) drops the interface bit, and two (`walk-mark-word-zero`, `walk-marked-word-zero`) use word 0 for every sink.
- **Exact fix:** "Fifteen of the 18 changed-sink walk plants each drop one mark, one drops `mark()`'s interface bit, and two write or read word 0 for every sink (caught at 33 sinks), each built at 33 sinks …"

### RES-3 (RESIDUE): the PR body does not say which compilers built the CTest gates

- **Lens:** Docs (PR text).
- **Where:** PR #34 body, "Validation", the sentence after the table.
- **Defect:** the sentence lists only Clang 18.1.3 among the compilers. The author receipts (`gates/gcc-configure.log`, `gates/clang-sanitizers-configure.log`) show that the CTest gates were built with the host's GCC 16.2.1 and Clang 23.1.4; Clang 18.1.3 served only the gates that require it. The figures are unaffected: the hosted run at the exact head used GCC 13.3.0 and Clang 18.1.3 and passed 28/28.
- **Exact fix:** add "The GCC and Clang-sanitizer CTest gates ran with the host's GCC 16.2.1 and Clang 23.1.4 (the pinned Clang 18 cannot build against the host's C++ library); the hosted run at the head used the CI image's GCC 13.3.0 and Clang 18.1.3."

### S-1 (SUGGESTION): lift the 33-sink restriction in the differential test

- **Lens:** Tests.
- **Where:** `tests/test_acmp_walk.cpp:187`, `:254` and `:304`.
- **What:** after the merge, #31's word-sized release mask is in the branch, so the reason the PR body gives ("`1u << 32` would have been undefined") no longer holds. At 33 sinks the test still never owes a frame: 0 owed steps in my probe. My LIFT mode passes against `main`'s real core and kills the release-loop plants `c2` and `c3` directly. Dropping `wide ||` at `:304` and the `k - 32u` remap at `:187` would let the differential test cover the merged release line at sink 32 itself. A sink-to-interface map in which k and k mod 32 sit on different interfaces would also make `c4` observable.

### S-2 (SUGGESTION): state the parent's target figures

- **Lens:** Docs.
- **What:** acceptance 4 says "Target figures come from the parent's measurement". The PR's "Cycles" section could quote the parent's figures beside the host benchmark. Those figures are 18,782 of 22,170 cycles per ADP record at 8 sinks on 2 interfaces, and #665's per-record costs with tsn-c-stack#32.

### S-3 (SUGGESTION): assert the interface mask's width

- **Lens:** Robustness.
- **Where:** `src/acmp.c:213` and `:1223`.
- **What:** `dirty_if` is a `uint32_t` indexed by interface. `ACMP_MAX_INTERFACES` is fixed at 4 today, so this is safe. A `_Static_assert(ACMP_MAX_INTERFACES <= 32u, …)` beside #31's storage refusals would keep it safe if that bound is ever made configurable.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `src/acmp.c` delta and every mark site against IEEE 1722.1-2021 8.2 and Milan v1.2 5.5.3 and 5.6.4; differential against `main`'s real core (560 runs); author and hosted differential tests | R824-1 | 9043b926532dc4ffb57218ee0eebca7564262289 |
| RTL | UNCLEAN (F-1) | RV32 freestanding build and QEMU smoke (mine and hosted); core imports; `acmp.c` RV32 text delta; parent image rom fit with #32 (the lane's receipts) | R824-1 | 9043b926532dc4ffb57218ee0eebca7564262289 |
| Robustness | UNCLEAN (F-1) | Mask sizing on every new path at mask widths 16, 32, 33, 64 and 255 under ASan, UBSan and shift; re-entry; early returns; persisting marks; parent consumer integration (pin, adapter, receipts) | R824-1 | 9043b926532dc4ffb57218ee0eebca7564262289 |
| Tests | UNCLEAN (F-1) | `test_acmp_walk.cpp`; A17 and A31 additions; 470-plant campaign with kill words; plant-merge audit; probe controls; CI rc (mine, author's and hosted); coverage; parent consumer gate receipts (absent) | R824-1 | 9043b926532dc4ffb57218ee0eebca7564262289 |
| Docs | CLEAN (RES-1, RES-2 and RES-3 carried) | REQUIREMENTS ACMP-13, `requirements.json`, origins, PORTING walk and storage, VERIFICATION, CHANGELOG, TESTS and TRACEABILITY (generator gates), PR body, comment-rule and privacy scans | R824-1 | 9043b926532dc4ffb57218ee0eebca7564262289 |

## Real limits

- The pinned Clang 18.1.3 cannot build the C++ tests against this host's libstdc++. My sanitizer gate therefore used Clang 23.1.4. The CI image's GCC 13.3.0 and Clang 18.1.3 results come from the hosted run at the exact head, which I inspected; I did not execute it.
- My GCC CTest, coverage and mutation runs used GCC 16.2.1.
- No parent firmware gate was run by me. That is outside the allowed scope (no parent banks); see F-1.
- No manager source bank runs at this head, and none is claimed or inferred. Source-head execution evidence is the author's published receipts, my own runs and the inspected hosted runs.
- Physical calibration: NOT RUN. Nothing here is hardware proof.
- For portability, the packet's scripts read the toolchain root from `TOOLS`. A local grep pass-through used during the runs was replaced by plain `grep` in the published copies; the output is unchanged.

## Pending manager duties

- Rule on F-1: consumer receipts or a recorded deferral to the pin move carrying #28, #31 and #32, and the PR body's statement of the consumer cost (+132 B over the 8x8/2if `answering-every-port` granule).
- Carry RES-1, RES-2 and RES-3 to the residue checklist.
- Hosted and act acceptance; the current-dev merge candidate (builder and native banks, source base `9deb0ddb`, live dev `46c971fa`) at the merge turn, with its receipts linked on the PR.
- The second independent review (R823) remains its own.

R824-1 FINISHED
