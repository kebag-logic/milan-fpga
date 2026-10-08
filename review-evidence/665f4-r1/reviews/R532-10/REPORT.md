[R532] NEGATIVE - exact head 82a79638405c3365e4078da471be56758f8dd679

Round R532-10, internal independent review of #665 lane F4 / PR #690. Delta `edeef61c..82a79638` (two commits: `da36eb15`, `82a79638`), tree `f09d67734ca6ccab67a2482d884331c6b4d2056c`. Assignment #665 comment 6048644347; REVIEW READY 6049231637; author packet `review-evidence/665f4-r1/author-r10` at `8ba25cb0`. Round-9 verdicts at `edeef61c` are the baseline. Lenses applied: Conformance, RTL, Robustness, Tests, Docs.

## Summary

The round closes all three round-9 findings at this head:

- **R532-9-F1:** SRP Talker registration now reaches ACMP, deferred and serialized. The round-9 `probe_tk_registered.hpp` passes at IF=1/2.
- **R532-9-F2:** permanently invalid VIDs are parked visibly and the loop sleeps. The round-9 `probe_invalid_vid.hpp` passes at IF=1/2.
- **R532-9-F3:** all eight round-9 bound plants are caught where they are not equivalent.

The 33 named binding, feedback, parking and bound-term plants are caught at both interface counts. Coverage is 100 % (`ctrl_app_srp.c` 75/75 lines, 60/60 branches). The A0 sanitizer matrix and the four linked images match the author's figures.

Three new findings stay open. All are in the new feedback path and its checks:

- **R532-10-F1 (MINOR):** a Talker that switches between Advertise and Failed while the listener is SETTLED_RSV_OK is never reported to ACMP. GET_RX_STATE_RESPONSE then carries a wrong REGISTERING_FAILED bit, in both directions, for as long as the registration lasts.
- **R532-10-F2 (MINOR):** two load-bearing statements in the new delivery poll have no discriminating check. One of those mutants makes a replacement listener settle on the old talker's registration.
- **R532-10-F3 (MINOR):** the new `CTRL_APP_SRP_FEEDBACK_MAX` term can be understated four-fold, or replaced with a constant, with every test green. Only its zero-access paths are exercised.

## 1. Reconstruction (public state only)

- **Workflow and authority.** I read `AGENTS.md` sections 3 to 8, `CONTRIBUTING.md` sections 2, 3, 5 and 6, and `docs/README.md`.
- **Frozen F4 assignment and round-10 decisions.** Assignment 6030279477 (Part B.4 declarations and port wiring; B.6 latency) and 6048644347 (decisions: R532-9-F1 option (a), wire the direction; R532-9-F2, park).
- **Issue body rules.** The service-latency bound is stated and tested per response path, and there is no RTL change.
- **Interface authorities:**
  - `acmp/acmp.h:258-270`: the sink view, where `talker_registered` and `registering_failed` mean "a matching Talker attribute ... and it is a Talker Failed".
  - `acmp/acmp.h:414-419`: the SRP-side entries.
  - `acmp/acmp.c:1116-1144`: Table 5.30 "x" outside SETTLED_NO_RSV and SETTLED_RSV_OK.
  - `acmp/acmp.c:836-850`: the GET_RX_STATE flags.
  - `srp/srp_mbx.c:475-497`: the registration snapshot, `desired` 1 = Talker Failed, 2 = Advertise.
  - `srp/srp_mbx.h:97-101`: the bind port.
  - `docs/design/MAILBOX_SPLIT.md:710-745`: the T_svc envelope.
  - `protocol-processor/docs/architecture/05_acmp_engine.md` F05.14: REGISTERING_FAILED is "1 iff registering matching Talker Failed".
- **Diff and history.** I read `git diff d8b355fe..82a79638` focused on `edeef61c..82a79638`: 13 files, +462/-60. Both commits are one-line with no trailers. `git diff edeef61c..HEAD -- hdl sw/mailbox configs sw/litex sw/builder constraints syn .gitmodules` and the dependency gitlinks are empty: no RTL, contract, register-map or pin change.
- **Public executable evidence.** I read the author packet at `8ba25cb0` (`ROUND10-TESTS.md`, `ROUND10-REVIEW-PROBES.json`, `ROUND10-COVERAGE.md`, `ROUND10-SIZES.json`, `PR-BODY.md`) and the live PR body. The live body matches the packet's `PR-BODY.md` apart from one trailing blank line.

## 2. Delta review against the round-10 assignment

| Assignment item | Result | Evidence |
|---|---|---|
| 1. Advertise -> `acmp_tk_registered(sink,false)`, Failed -> `(sink,true)`, withdrawal -> `acmp_tk_unregistered`, deferred and serialized, no reentry, per interface | **Met for the three named transitions** | `app/ctrl_app_srp.c:78-88`. Feedback runs in the fifth poll after SRP's poll, from SRP's own snapshot. `acmp_tk_*` is entered only from `deliver()`, never inside a port. The case hooks assert `in_port` and `!srp_adapter.busy` (`test/srp_binding.hpp:245-270`). `reentries` is 0 in every case. A **kind change while settled** is not delivered: new finding F1. |
| Healthy talker keeps a composed listener SETTLED_RSV_OK past TMR_NO_TK (Milan v1.2 5.5.3.5.36, 5.5.3.5.42) | **Met** | `SrpBinding.AdvertiseFeedbackIsDeferredAndSurvivesNoTalkerDeadline` refreshes for 12 s. The round-9 probe `probe_tk_registered.hpp` passes at IF=1 and IF=2, with sink state 7 (RSV_OK), SRP bound and `desired` 2 after 12 s (`receipts/r532-9-probes-if{1,2}.log`). |
| Registered, Failed, unregistered and isolation cases, each with a discriminating plant at both counts | **Met** | The six `feedback-*` plants are caught at IF=1 and IF=2 by named observable (`receipts/author-plants-if{1,2}.log`). |
| SRP README owed list and `ctrl/README.md` updated | **Met** (accurate for the delivered transitions) | `srp/README.md:53-62,294-299`; `ctrl/README.md:129-151`. |
| 2. Invalid VID parked visibly, including retiring an older accepted binding; the loop sleeps; a plant restoring the perpetual retry; transient refusals retry | **Met** | `ctrl_app_srp.c:45,61-68`; `ctrl_app.h:84` (`parked`). The round-9 `probe_invalid_vid.hpp` passes at IF=1/2: first idle pass at 1 ms, and the 1,205 non-idle passes in 12 s are the centisecond ticks. `binding-invalid-retries`, `binding-park-keeps-old`, `binding-invalid-upper-bound` and `binding-park-never-clears` are caught at IF=1/2. Three reviewer plants are also caught at IF=1/2: VID 0 dropped, parking ignoring unbind, and the parked-retire refusal sleeping (`receipts/reviewer-plants-if{1,2}.log`). |
| 3. Each `srp_bounds.h` term checked through a path that reaches it; named plants at IF=1/2; the eight round-9 plants caught | **Met** | `test/srp_app.cpp:148-235`, and the `srp-term-*`, `srp-poll-extra-read` and `srp-send-extra-read` plants caught at IF=1/2. All eight round-9 plants (six `rv-*` from its `bound_probes.tsv`, two `code-*`) are caught by `srp_app.cpp` at IF=2. At IF=1, 7 of 8 are caught; `rv-poll-per-if` (`MBX_N_IF` -> `1u`) is textually equivalent at IF=1 (`receipts/r532-9-plants-if{1,2}.log`). |
| 4. S1 (indentation/comment) recommended; S2 optional | **Taken** | `ctrl_app.h` is tab-indented throughout; `without_delivery()` names the intent (`srp_binding.hpp:43-48`). One reflowed comment line is 113 columns (S1 below). |
| Run every round-9 gate including AddressSanitizer; re-measure bounds/images | **Met locally** (this reviewer's subset, section 5) | No hosted check run exists at this head at query time (section 8). |

## 3. Findings

### R532-10-F1 | MINOR | Conformance, RTL, Robustness, Tests, Docs | `sw/firmware/ctrl/app/ctrl_app_srp.c:80-87`; `acmp/acmp.c:1116-1130,847-848`; `acmp/acmp.h:269-270`; `ctrl/README.md:135-137`; `srp/README.md:54-56,297-299` | A Talker Advertise <-> Talker Failed change while the listener is SETTLED_RSV_OK never reaches ACMP, so REGISTERING_FAILED on the wire is wrong in both directions

- **Authority:**
  - The round-10 assignment, item 1: "The composition delivers SRP's per-sink Talker **registration changes** to ACMP".
  - The ACMP view contract: `acmp.h:269-270` defines `registering_failed` as "a matching Talker attribute (SETTLED_RSV_OK) ... and it is a Talker Failed". `acmp.c:847-848` puts it on the wire as GET_RX_STATE_RESPONSE REGISTERING_FAILED (Milan v1.2 Table 5.23, as `acmp.h:191-195` cites).
  - The processor reference F05.14 gives the same live semantics.
- **Evidence:**
  - Feedback calls `acmp_tk_registered` only when the sink is `ACMP_SETTLED_NO_RSV` (`ctrl_app_srp.c:83`). `acmp_tk_registered` itself refuses any other state (`acmp.c:1121`), so `tk_failed` is latched at first registration.
  - **Probe** `scripts/r532_10_probe_kind.hpp`, cases `R10KindChangeWhileSettledReachesAcmp` and `R10FailedToAdvertiseWhileSettledReachesAcmp`, at IF=1 and IF=2 (`receipts/probe-kind-if{1,2}.log`):
    - Advertise -> Failed (Failed New, Advertise rapid Leave, then Failed refreshed for 2 s): SRP's snapshot is `desired` 1 (Failed), but ACMP stays RSV_OK with `tk_failed` 0. A real GET_RX_STATE_COMMAND is answered with flags `0x0002`, without REGISTERING_FAILED.
    - Failed -> Advertise: SRP's snapshot is `desired` 2, but GET_RX_STATE_RESPONSE keeps flags `0x0042`, so REGISTERING_FAILED stays set.
    - Both directions show `impossible` 0. The state persists until the registration is withdrawn or the sink is rebound.
    - SRP's own Listener declaration follows its snapshot (`srp_mbx.c:553-576`, by code reading), so only ACMP's view is stale.
  - No case or plant covers a kind change. `ctrl/README.md:137` ("Repeated registration is not a new event under Milan Table 5.30") and the PR body ("Repeated unchanged registration is not delivered again") describe the unchanged case only, and `srp/README.md:297-299` presents the feedback as complete.
- **Impact:** a controller is told a working reservation has failed, or a failed one is healthy, for the life of the registration. A talker's reservation can flip in operation, for example on a path bandwidth change.
- **Required outcome:** one of the following, with the choice published.
  - (a) A kind change while SETTLED_RSV_OK updates ACMP's `tk_failed`, through an ACMP entry whose Table 5.30 interpretation is recorded. Today `acmp_tk_registered` refuses that state as "x", so this touches the F3 interface and needs a public decision.
  - (b) A public decision that REGISTERING_FAILED latches at first registration, with that limitation stated in `srp/README.md`, `ctrl/README.md` and the PR body.
  - Either way, add integration cases for both directions at IF=1/2, each with a discriminating plant.
- **Verification:** under (a), both probe cases pass at IF=1/2 and the new cases' plants are caught. Under (b), the decision and the wording are published and the new cases assert the latched behavior.

### R532-10-F2 | MINOR | Tests | `sw/firmware/ctrl/app/ctrl_app_srp.c:80` and `:89`; `test/srp_mutants.py` (round 9 `binding-first-refusal-forgotten`, at `edeef61c` line 675, removed at `82a79638`) | Two load-bearing statements of the delivery poll can be removed with every test green

- **Authority:**
  - `AGENTS.md` section 6, Tests: each test "can fail for the defect it claims to detect"; positive, negative and boundary behavior is covered.
  - The code states both invariants:
    - `ctrl_app_srp.c:78-79`: "Never feed an old binding's registration to a replacement awaiting delivery". `srp/README.md:57` says the same ("only the accepted binding").
    - `ctrl/README.md:129`: "Transient refusal keeps the request pending and the loop awake".
- **Evidence** (`scripts/r532_10_escape.py`, run through the whole `test_acmp_mbx.cpp` suite; `receipts/reviewer-plants-if{1,2}.log`):
  - `r10-feedback-ignores-pending` (`if (!r->pending && r->bound)` -> `if (r->bound)`) **escapes** at IF=1 and IF=2.
    - The reviewer probe `R10ReplacementAwaitingDeliveryGetsNoOldRegistration` (`scripts/r532_10_probe_guard.hpp`) passes at the head and **fails** under this plant at IF=1/2: a rebind to another talker whose SRP delivery is transiently refused is settled RSV_OK from the old talker's registration.
  - `r10-transient-refusal-forgotten` (`pending = r->pending || pending;` -> `pending = r->pending;`) **escapes** at IF=1/2.
    - Its round-9 plant and test (`OneRefusedSinkDoesNotBlockAnotherOrLetTheLoopSleep`) were removed when the invalid-VID case was rewritten for parking, and nothing replaced them.
    - The probe `R10EarlierSinkTransientRefusalKeepsDeliveryAwake` passes at the head and **fails** under the plant at IF=1/2.
    - Probe and plant results: `receipts/probe-guard-if{1,2}.log` and `receipts/reviewer-probe-plants-if{1,2}.log`.
- **Impact:** the first guard is all that stops a listener settling on a talker it is not bound to. A later edit can drop it, or the refusal accumulation, with every gate green.
- **Required outcome:** integration cases that pass at the head and fail when either statement is removed, with named plants at IF=1/2.
- **Verification:** both plants above are caught by name at IF=1/2.

### R532-10-F3 | MINOR | Tests, Conformance, Docs | `sw/firmware/ctrl/app/ctrl_app.h:69-72`; `test/srp_binding.hpp:256-258`; `test/test_acmp_mbx.cpp:1041-1043`; `test/srp_binding.hpp:272-289`; author `ROUND10-TESTS.md` "Measured bound terms" row "Application feedback allowance" | The new feedback allowance in `CTRL_APP_PASS_MAX` is not falsifiable on the path it funds

- **Authority:**
  - The issue body: each protocol "states its firmware service-latency bound per response path and tests it" (NFR-SCOUT-03).
  - The round-10 assignment: "Re-measure the bounds ... if they change".
  - The same standard R532-9-F3 applied to `srp_bounds.h`.
- **Evidence:**
  - The allowance is derived for withdrawal reprobing through TMR_DELAY: clock, first-draw seed, two-word timer arm (`ctrl_app.h:69-72`, `MAILBOX_SPLIT.md:719-721`).
  - The only measurement (`srp_binding.hpp:256-258`) is the registration path against the whole 64. `test_acmp_mbx.cpp:1041-1043` restates the macro. `FailedRegistrationReachesAcmpAndWithdrawalReprobes` withdraws undiscovered sinks, which go passive with **0** accesses (the probe `R10WithdrawalFeedbackCostFitsAllowance` measures 0).
  - Both reviewer plants **escape** at IF=1 and IF=2 (`receipts/reviewer-plants-if{1,2}.log`):
    - `r10-feedback-allowance-quarter` (`ACMP_MAX_SINKS * 4u` -> `* 1u`);
    - `r10-feedback-allowance-eight` (-> `8u`).
  - The reviewer probe `R10DiscoveredWithdrawalFeedbackCostFitsAllowance` reaches the funded path: ENTITY_AVAILABLE first, then withdrawal. It measures 5 accesses for two sinks at IF=1 and 7 at IF=2, within four per sink (`receipts/probe-kind-if{1,2}.log`).
  - The figure is therefore correct by my trace and measurement. It is a falsifiability gap, not a wrong bound. The author's table nevertheless files the row under "Measured bound terms".
- **Impact:** a later change to the reprobe path (an extra clock read, a second timer write) can raise the real feedback cost above the published 3,192 / 4,041 envelope with every gate green.
- **Required outcome:**
  - A check that reaches discovered-talker withdrawal for several sinks and fails when the per-sink term is understated, with named plants at IF=1/2.
  - Or narrow the claim to analytic and record that decision publicly.
- **Verification:** the two plants above are caught at IF=1/2, or the published evidence and docs call the term analytic.

### Suggestions (non-blocking)

- **R532-10-S1** | Docs | `sw/firmware/ctrl/app/ctrl_app.h:143`. The reflowed attach comment leaves one 113-column line ("each SRP interface, as MAAP/ADP do. A refusal leaves the ADP/ACMP/MAAP composition running and SRP unattached."). Wrap it like the neighboring comment lines. The C/C++ idiom gate passes (`receipts/idiom-gates.log`).

## 4. Prior public findings at this head

The two rows below cover the R533-9 review, which was read only after the verdict and ledger above were written.

| Finding | Status at `82a79638` |
|---|---|
| R532-9-F1 (MAJOR, no SRP-to-ACMP registration) | **Resolved per its required outcome.** The three named transitions are delivered, deferred and serialized, per interface. The round-9 probe passes at IF=1/2. The six `feedback-*` plants are caught at IF=1/2. The kind-change gap is a new finding, R532-10-F1, not a retention. |
| R532-9-F2 (MINOR, invalid VID busy loop) | **Resolved.** The round-9 idle assertion passes at IF=1/2; parking is visible and retires an older accepted binding. The perpetual-retry plant is caught, transient refusals retry, and three extra reviewer plants are caught. |
| R532-9-F3 (MINOR, `srp_bounds.h` terms) | **Resolved.** All eight round-9 plants are caught at IF=2, and 7 of 8 at IF=1 with the eighth textually equivalent there. The author's eleven `srp-term-*`/extra-read plants are caught at IF=1/2. The same falsifiability standard applied to the new term is R532-10-F3. |
| R532-9-S1 / S2 | **Taken** (one long line remains: S1 above). |
| R532-8-F1 (A0, hosted half) | **Local half re-confirmed.** The clean build passes 62/62 under gcc, clang, gcc+ASan and clang+ASan (`__asan_report` symbols 12/48). The planted tree fails exactly A0 by name in all four, with no sanitizer report (`receipts/a0/`). **Hosted half still open:** there is no check run at this head (section 8). |
| R533-9 (POSITIVE at `edeef61c`) | **No open finding to carry.** Its reconciled rounds stay resolved at this head. R533-8-F1 (delivery): the R533-8 binding probe, without direct delivery, passes at IF=1 and on both interfaces at IF=2 (`receipts/binding-probe-nodirect.log`), and the 14 older `binding-*` plants are caught at IF=1/2. R532-8-F1: see the row above. R532-8-F2 to F4, the R1/R2 residues and R533-8-R1 are untouched by this delta. |

## 5. Executable evidence (this reviewer, at `82a79638`)

| Run | Result |
|---|---|
| Positive SRP arms, IF=1 and IF=2 (`srp_mbx` 53, `srp_debug` 3, `srp_rx_retry` 17, `srp_app` 5, `test_acmp_mbx` 33, `srp_latency` 5, `srp_walk` 5) | All rc 0 (`receipts/positive-if{1,2}.log`). The SRP poll envelope is 770/770 and 1,540/1,540. The pass envelope is 1,596/1,596 and 2,366/2,366. |
| The same arms with AddressSanitizer | All rc 0 at IF=1/2. Instrumentation confirmed (`receipts/asan-positive-if{1,2}.log`). |
| Author plants: `binding-*`, `feedback-*`, `srp-term-*`, `srp-poll-extra-read`, `srp-send-extra-read` | 33/33 caught at IF=1 and 33/33 at IF=2, by named observable (`receipts/author-plants-if{1,2}.log`). |
| R533-8 binding probe without direct delivery (`scripts/binding_probe_nodirect.py`, reused from round 9) | PASS at IF=1 and on both interfaces at IF=2 (`receipts/binding-probe-nodirect.log`). |
| Round-9 reviewer probes (`probe_tk_registered.hpp`, `probe_invalid_vid.hpp`) | Pass at IF=1/2 (`receipts/r532-9-probes-if{1,2}.log`). |
| Round-9 eight escaping plants | Caught (section 4) (`receipts/r532-9-plants-if{1,2}.log`). |
| Reviewer plants (`scripts/r532_10_escape.py`, eight plants) | Caught at both counts: the parked-retire refusal, VID 0 dropped and parking ignoring unbind. Interface-zero is caught at IF=2 and is equivalent at IF=1. Escaped at both counts: the ignored-pending guard, the forgotten transient refusal and both allowance plants (F2, F3). |
| Reviewer probes (`scripts/r532_10_probe_kind.hpp`, `scripts/r532_10_probe_guard.hpp`) | Kind change wrong on the wire (F1). Discovered withdrawal 5/7 accesses (F3). The guard probes pass at the head and catch both F2 plants (`receipts/probe-*`, `receipts/reviewer-probe-plants-*`). |
| `fw_coverage.py --check --lwsrp` | PASS, 22 files at 100 %. `ctrl_app_srp.c` 75/75 lines and 60/60 branches (`receipts/coverage-check.log`). |
| A0 matrix | Section 4 (`receipts/a0/`). |
| Linked images (`scripts/images.sh`, CI-pinned SDK installed offline from the digest-checked archive) | RAM span 79,536 / 92,240 (1x1, IF=1/2) and 94,224 / 121,712 (8x8). These equal the author's figures and are +752 / +752 / +736 / +752 over round 9's verified 78,784 / 91,488 / 93,488 / 120,960. F3 `ctrl_image`, `ctrl_image_selftest` and `fw_rv32_selftest` rc 0 (`receipts/images.log`). |
| `scripts/docs_check.py` (pinned docs environment), C/C++ and Python idiom gates | rc 0 (`receipts/docs_check.log`, `receipts/idiom-gates.log`). |

## 6. Lens results

- **Conformance - UNCLEAN** (F1, F3):
  - Examined: round-10 items 1-3 against `ctrl_app_srp.c:37-121`, `acmp.c:1116-1144,836-850,880-910`, `acmp.h:258-270,414-419` and `srp_mbx.c:475-497`.
  - Also examined: TMR_NO_TK behavior (5.5.3.5.36/.42) via the round-9 probe, and the NFR-SCOUT-03 bound rule against `ctrl_app.h:66-77`.
  - The three named transitions, parking and per-term SRP bounds conform.
- **RTL (architecture) - UNCLEAN** (F1):
  - Examined: poll order and serialization (`ctrl_app_srp.c:94-121`, the loop's poll table), and reentry flags (`acmp.c:89-97`; `srp_mbx` `enter`).
  - Also examined: the request-slot lifecycle including tk_unregistered -> `request(NULL)` within `deliver()` (`ctrl_app_srp.c:37-48,80-89`), and the composition-to-ACMP SRP-side contract.
  - The RTL/contract/pin diff is empty.
- **Robustness - UNCLEAN** (F1):
  - Examined: invalid VID 0/4095/65535, an invalid replacement over an accepted binding, transient refusal (retained receive) with delivery and retirement, replacement overtaking unbind, and kind change while settled.
  - Also examined: discovered and undiscovered withdrawal (probes and `srp_binding.hpp:193-310`).
- **Tests - UNCLEAN** (F1, F2, F3):
  - Examined: `srp_binding.hpp:40-330`, `srp_app.cpp:146-235`, `srp_cost_probe.hpp`, `srp_mutants.py:648-786`, `srp_arms.py:62-78`, `test_ctrl_firmware.py:198-207`, `test_acmp_mbx.cpp:1036-1046` and the coverage ratchet.
  - Also examined: the author, round-9 and reviewer plant campaigns at IF=1/2, and the A0 matrix.
- **Docs - UNCLEAN** (F1, F3):
  - Examined: `srp/README.md:50-80,228-245,290-305`, `ctrl/README.md:124-160`, `MAILBOX_SPLIT.md:710-745` and `ctrl_app.h:58-150`.
  - Also examined: the live PR body Round 10 and the author `ROUND10-TESTS.md`. The docs gate is rc 0 and has no em-dash in the delta.

## 7. Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F3) | `ctrl_app_srp.c`, `acmp.c/.h` SRP entries and GET_RX_STATE, `srp_mbx.c:475-497`, round-9 probes, kind-change probe, `ctrl_app.h` bounds | none clean at this head (R532-10 applied it) | `82a79638405c3365e4078da471be56758f8dd679` |
| RTL | UNCLEAN (F1) | delivery poll order/serialization, request-slot lifecycle, ACMP SRP-side contract, empty RTL/contract/pin diff | none clean at this head (R532-10 applied it) | `82a79638405c3365e4078da471be56758f8dd679` |
| Robustness | UNCLEAN (F1) | invalid VIDs, invalid replacement, transient refusal, overtaken unbind, kind change, withdrawal paths | none clean at this head (R532-10 applied it) | `82a79638405c3365e4078da471be56758f8dd679` |
| Tests | UNCLEAN (F1, F2, F3) | `srp_binding.hpp`, `srp_app.cpp`, `srp_cost_probe.hpp`, `srp_mutants.py`, campaigns (33+33 author, 16+16 round-9, 8+8 and 2+2 reviewer), coverage 22/22, A0 matrix | none clean at this head (R532-10 applied it) | `82a79638405c3365e4078da471be56758f8dd679` |
| Docs | UNCLEAN (F1, F3) | SRP and ctrl READMEs, `MAILBOX_SPLIT.md`, `ctrl_app.h` comments, live PR body, author `ROUND10-TESTS.md`; docs and idiom gates rc 0 | none clean at this head (R532-10 applied it) | `82a79638405c3365e4078da471be56758f8dd679` |

## 8. Real limits

- Host model only. Physical calibration is NOT RUN, and no field skip is hardware proof.
- I did not consult the Milan v1.2 text directly for REGISTERING_FAILED. F1 relies on the in-repo restatements (`acmp.h:191-195,269-270`; processor F05.14) and on the observed wire response.
- F1 and F3 use synthetic MSRP Talker frames built by the suite's own helper (`srp_binding.hpp:49-63`). I did not establish what a bench talker sends during a kind change.
- My runs are the SRP-related subset:
  - Not re-run: the full control campaign (469 plants), the saved-state campaign, the mailbox Verilator suite (no RTL or contract change), the builder bank and the MAAP differential. These are unchanged by the delta, or the manager's per the assignment. The pinned Verilator was not used.
  - The plant campaigns were run with my own driver (`scripts/srp_driver.py`), which reuses the head's `srp_mutants.campaign` and `arm_srp` unchanged.
- At query time (`receipts/gh-query-time.txt`) the GitHub API listed **no check runs and no workflow runs** for this exact head, and `gh pr checks 690` reported none (`receipts/gh-*.tsv`, `receipts/gh-pr-checks.txt`). I make no hosted claim.

## 9. Pending manager duties

- Hosted acceptance at this head: `firmware-unit`/`rtl-fast`, which also closes R532-8-F1's hosted half, and the ready-state gates. Also trusted local replication.
- A public decision on R532-10-F1: option (a) touches the F3 ACMP SRP-side interface.
- Candidate merge validation against live `dev` `291710b180ca9196780a6d17f2517957c9bcb89c` (source base `d8b355fe`), merge authorization and containment.
- Publication of this report and receipts.

R532-10 FINISHED
