[R532] NEGATIVE - exact head b98eb2d5a21522bab3bc6bb943332cf8edf11893

Round R532-11 is the internal independent review of #665 lane F4 / PR #690. It reviews the delta `82a79638..b98eb2d5`: three commits, `14f091be`, `803e8c3c` and `b98eb2d5`, at tree `45e0efdbceac0cd7cc9b97d76d0245e33643c1ab`.

- **Inputs.** Assignment #665 comment 6049530812, with the manager's kind-change decision (a). REVIEW READY 6050418707. Author packet `review-evidence/665f4-r1/author-r11` at `2f7ab26d`.
- **Baseline.** The round-10 verdicts at `82a79638`.
- **Lenses applied.** Conformance, RTL, Robustness, Tests and Docs.

## Summary

The behavior asked for in round 11 is present and works at this head. Every named round-10 case passes at IF=1 and IF=2, through real mailbox ingress and actual GET_RX_STATE responses:

- R533-10's four cases: both kind replacements, `R533WithdrawalBeforeReregistrationStillReprobes`, and the `R533SeparatePassWithdrawalDoesReprobe` control.
- R532-10's `R10KindChangeWhileSettledReachesAcmp`, `R10FailedToAdvertiseWhileSettledReachesAcmp` and the two guard cases.

Other results at this head:

- All 19 named feedback and `r10-*` SRP plants, and the 5 named ACMP plants (including the renumbered `acmp-open-unguarded`, entry 10), are caught by name.
- Coverage is 100 % on all 22 files.
- The plain and AddressSanitizer SRP suites pass at IF=1/2.
- The four linked images reproduce the author's figures exactly.

Two MINOR findings keep the verdict NEGATIVE:

- **R532-11-F1 (MINOR; RTL, Docs).** The new observation point in the MSRP receive filter calls `mrp_attr_visit` on the same lwSRP application from inside that application's own `mrp_rx`. lwSRP's documented integration contract forbids a filter from re-entering its owning application. No round-11 artifact records this conflict.
- **R532-11-F2 (MINOR; Tests, Docs).** Three documented feedback guarantees have no discriminating test. Each planted defect passes the whole composition suite (`test_acmp_mbx.cpp`) at IF=1/2, and a reviewer probe that passes at the head catches it at IF=1/2. Two of them have real failure modes:
  - a link reset that leaves a listener SETTLED_RSV_OK with no registration;
  - an identical-identity rebind that settles RSV_OK from the retired epoch's kind.

## 1. Reconstruction (public state only)

- **Workflow.** I read `AGENTS.md` sections 3 to 8 and `CONTRIBUTING.md` (authority, review bar, merge rules), then `docs/README.md`.
- **Issue #665.** I read the body (rules while #664 is open: no RTL, default build and shipping image unchanged, per-path service-latency bound, portable C), and these comments:
  - 6030279477: the F4 lane, Parts A to C.
  - 6009661573 and 6030870481: the acceptance additions.
  - 6049530812: the round-11 assignment. Decision (a): the Talker kind is a view attribute of SETTLED_RSV_OK, updated in place through a new ACMP entry. It is not an EVT_TK_REGISTERED replay. Withdrawals are latched per sink and per interface, delivered in order outside library and port callbacks, and retired on supersession.
  - 6050418707: REVIEW READY.
- **Authorities.** `acmp/acmp.h:258-270,343,414-424` (view and SRP-side entries), `acmp/acmp.c:382-414` (view, `view_equal`) and `acmp.c:835-850` (GET_RX_STATE flags). Milan v1.2 Tables 5.23, 5.29 and 5.30, 5.5.3.5.42/.44/.48 as cited in-tree. The lwSRP integration contract at the pinned `9197193e`: `src/include/shish_lan/mrp.h:288-293,413-419` and `doc/integrator.md:319-324`.
- **Author's event model.** I read the round-11 "Feedback event design" section of the author HANDOFF (`HANDOFF.md:749-814`) before the code. The code matches it (section 2).
- **Diff and history.** I read `git diff d8b355fe..b98eb2d5`, focused on `82a79638..b98eb2d5`: 18 files, +446/-47, all under `sw/firmware/ctrl`, `sw/firmware/gtest/coverage.ratchet` and `docs/design/MAILBOX_SPLIT.md`.
  - The three commits are one-line with no trailers.
  - No path under `hdl`, `sw/mailbox`, `configs`, `sw/litex`, `sw/builder`, `constraints`, `syn` or `tb` changed in the delta. The gitlinks are unchanged.
  - `git diff 803e8c3c..b98eb2d5` is exactly one line in `sw/firmware/ctrl/test/acmp_review_mutants.py:256` (the oracle text "entry 9" becomes "entry 10"). This confirms that the builder receipt at `803e8c3c` differs from the head only in a mutation-oracle entry number outside builder inputs.
- **Public evidence.** I read the author packet at `2f7ab26d`: `HANDOFF.md` (round 11), `ROUND11-GATES.md`, `ROUND11-TESTS.md`, `ROUND11-COVERAGE.md`, `ROUND11-SIZE.md` and `PR-BODY.md`. The live PR body equals the packet's `PR-BODY.md` apart from one trailing blank line.
- **Order of work.** Prior public review findings were read only after my provisional verdict and ledger were written (`receipts/provisional-verdict.txt`).

## 2. Delta review against the round-11 assignment

| Item (6049530812) | Result | Evidence at this head |
|---|---|---|
| Decision (a): kind change in SETTLED_RSV_OK updates `tk_failed` in place through a new entry, not EVT_TK_REGISTERED; recorded in `acmp.h` and the README | **Met** | `acmp.c:1132-1143`: `acmp_tk_kind_changed` refuses any state but SETTLED_RSV_OK (`impossible++`), sets only `tk_failed`, keeps the reentry guard, and lets `finish()` publish the changed view. `view_equal` includes `registering_failed`, so one CHANGED notification is sent. `acmp.h:420-424` and `ctrl/README.md:134-144` record the interpretation. |
| 1. Kind delivered through the serialized composition, per sink and per interface; unchanged repeats idempotent; named cases at IF=1/2; each direction with a standing case and a discriminating plant | **Met** | `ctrl_app_srp.c:84-94` calls the entry only when `tk_failed` differs. The R533 and R532 named cases pass at IF=1/2: flags 0x42 after Failed and 0x02 after Advertise, at port 1 for sink 1 at IF=2 (`receipts/named-probes-if{1,2}.log`). Reviewer case `R11Feedback.UnchangedRepeatsAreIdempotent` (20 refreshes, no CHANGED, `impossible` 0) passes. The plants `feedback-kind-failed-lost`, `feedback-kind-advertise-lost`, `acmp-kind-lost` and `acmp-kind-any-state` are caught by name. |
| 2. Withdrawal latched per sink and per interface, in order, outside callbacks, even with same-pass re-registration; expiry then fresh receive; supersession retires feedback; plants for dropping the retained transition, isolation and supersession | **Met in behavior; tests incomplete (F2); one observation point re-enters lwSRP (F1)** | `srp_mbx.c:515-536` (`capture`/`snapshot`), `:51` (tick), `:133` (filter), `:389` (receive end), `:648` (reset), `:714` (poll). `ctrl_app_srp.c:75-99`. `R533WithdrawalBeforeReregistrationStillReprobes` passes at IF=1/2 (PRB_W_AVAIL, SRP unbound, two records received). The separate-pass control passes. The author's seven temporal cases pass and their plants are caught by name. The reviewer probes for reset, identical-identity reseed and post-withdrawal kind pass at the head. The plants for those three guarantees escape the author's suite (F2). |
| 3. R532-10-F2: `r10-feedback-ignores-pending` and `r10-transient-refusal-forgotten` killed by name at IF=1/2; a standing transient-refusal case | **Met** | `SrpFeedback.ReplacementAwaitingDeliveryGetsNoOldRegistration` and `SrpFeedback.EarlierSinkTransientRefusalKeepsDeliveryAwake` catch both by name at IF=1/2 (`receipts/author-plants-if{1,2}.log`). The original reviewer cases also pass. |
| 4. R532-10-F3: allowance measured on the funded path at IF=1/2; both allowance plants caught | **Met** | `SrpFeedback.DiscoveredWithdrawalMeasuresTheFundedPath` measures 5 and 5 accesses at IF=1 and 7 and 11 at IF=2 (settled; first registration then withdrawal), for two sinks against 12. Both plants are caught by the measured assertion at IF=1/2. My reviewer case `R10DiscoveredWithdrawalFeedbackCostFitsAllowance` reproduces 5 (IF=1) and 7 (IF=2). The compiled `CTRL_APP_PASS_MAX` prints 3224 and 4073 (`test_acmp_mbx.cpp:1036` F6 line), equal to `MAILBOX_SPLIT.md:715-716` and `ctrl/README.md:159`. Every four-module row is ×3, ×11, ×22 and ×9 of those bounds, with floor-rounded access times. |
| Every round-10 gate, ASan, bounds and images | **Met locally** (this reviewer's subset, section 5) | No hosted check run exists at this head (section 7). |

## 3. Findings

### R532-11-F1 | MINOR | RTL, Docs | `sw/firmware/ctrl/srp/srp_mbx.c:126-133` (`interested_msrp` calls `snapshot(i)`), `srp_mbx.c:525-536` (`snapshot` calls `mrp_attr_visit(i->msrp,...)`), `srp_mbx.c:181`; `sw/firmware/ctrl/srp/README.md:70-75` | The MSRP receive filter re-enters its owning lwSRP application

- **Authority.** Three lwSRP documents at the pinned `9197193e`, which `third_party/lwSRP` records:
  - `doc/integrator.md:321-323`: "Transport callbacks, indications, observers, and filters must never synchronously reenter the owning application. Queue future work instead. The firmware adapter owns debug and release enforcement of this contract."
  - `src/include/shish_lan/mrp.h:288-290` (the filter contract): "It must not re-enter MRP."
  - `mrp.h:314-318`: the library marks one query, `mrp_attr_registered_ports`, as intended for use inside callbacks. `mrp_attr_visit` (`mrp.h:413-419`) carries no such allowance.

  AGENTS section 6 RTL lens: "Existing module/interface contracts remain valid". Section 8: "Never hide a material assumption or specification conflict in code". F4 assignment 6030279477: lwSRP changes go to lwSRP PRs.
- **Evidence.**
  - `srp_mbx.c:181` registers `interested_msrp` as the MSRP rx filter. lwSRP calls the filter from `rx_on_attr` (`src/core/mrp_mad.c:998`) inside `mrp_rx(i->msrp, ...)`.
  - Round 11 adds `snapshot(i)` at `srp_mbx.c:133`. `snapshot` calls `mrp_attr_visit(i->msrp, ...)` (`:533`), which iterates that same application's attribute list while its `mrp_rx` is on the stack.
  - At `82a79638` the visitor was called only from `poll`, outside every library callback. This is the first round-11 call into an lwSRP application from inside one of its own callbacks.
  - The design depends on this call. Removing it (`feedback-intrapdu-lost`) fails `SrpFeedback.SinglePduWithdrawalThenRegistrationRetainsTheFirstEvent`.
  - The in-code comment (`srp_mbx.c:130-132`) and `srp/README.md:72-73` describe the call as "read-only ... with no protocol mutation". Neither cites nor resolves the library's prohibition, and neither the handoff nor the PR body records the conflict.
  - By reading the pinned source, the call is functionally safe today. The filter runs before any change for the current event (`mrp_mad.c:993-1000`), and `mrp_attr_visit` is a `const` list walk (`mrp_mad.c:1170-1196`). The suites, including AddressSanitizer at IF=1/2, pass.
- **Impact.** Correct behavior now rests on an implementation detail that the dependency's integrator contract reserves the right to break. The contract says filters may not re-enter, and it gives the adapter the job of enforcing that. A future lwSRP pin that calls the filter while an attribute list is being changed, or that adds a reentrancy guard, would break or trap withdrawal observation, and no review artifact would point to the cause.
- **Required outcome.** One of the following:
  - (a) Observe the preceding wire event without calling into the owning lwSRP application from its filter. For example, use data handed to the callback, then visit only outside callbacks.
  - (b) Amend the lwSRP contract through an lwSRP PR so that the read-only visitor is explicitly permitted inside the rx filter, pin that commit, and cite it.
  - (c) Record a public maintainer or manager decision accepting this deviation, and state it in `srp/README.md` next to the observation-boundary text.

  In every case, the intra-PDU Lv-then-New ordering must still be preserved.
- **Verification.**
  - By code reading: no lwSRP application entry occurs inside the MSRP filter, or the cited contract or decision permits the one that remains.
  - `feedback-intrapdu-lost`, or its replacement, is still caught at IF=1/2.
  - `SinglePduWithdrawalThenRegistrationRetainsTheFirstEvent` and `R533WithdrawalBeforeReregistrationStillReprobes` pass at IF=1/2.

### R532-11-F2 | MINOR | Tests, Docs | `sw/firmware/ctrl/app/ctrl_app_srp.c:78`; `sw/firmware/ctrl/srp/srp_mbx.c:648`; `srp_mbx.c:520`; `sw/firmware/ctrl/test/srp_feedback.hpp`; `sw/firmware/ctrl/srp/README.md:66,77,82,257-259`; `ctrl/README.md:146`; PR body "Round 11" ("Standing tests cover ... supersession") | Three documented feedback guarantees have no discriminating check

- **Authority.** AGENTS section 6 Tests lens: "Each new test can fail for the defect it claims to detect"; positive, negative and boundary behavior is covered. The assignment's item 2 requires plants for dropping the retained transition, plus isolation and supersession checks. The docs claim each of these guarantees:
  - `srp/README.md:82` "Accepted intent retires feedback, even for identical stream identities", and `ctrl/README.md:146`.
  - `srp/README.md:77` "Expiry before receive remains visible, as does interface reset".
  - `srp/README.md:66` "Later registration cannot erase it or replace its preceding kind".
  - `srp/README.md:259` "Named plants ... remove each delivery guarantee".
- **Evidence.** The reviewer plants (`scripts/r532_11_plants.py`) are single-site and compile. Each was run through the whole `test_acmp_mbx.cpp` composition suite, with `SrpBinding.*` and `SrpFeedback.*` included, at IF=1 and IF=2 (`receipts/reviewer-plants-suite-if{1,2}.log`). The table lists the three that the reviewer probes catch.

| Plant | Site | Author suite | Reviewer probe (`scripts/r532_11_probe.hpp`) | Failure mode the probe shows |
|---|---|---|---|---|
| `p11-supersession-kind-stale` | `ctrl_app_srp.c:78`, reseed removed | **escapes** IF=1/2 | `IdenticalRebindAfterUndeliveredWithdrawalSettlesNoRsv` passes at the head and **fails** at IF=1/2 | Lv, then BIND_RX to another talker with the identical StreamID, destination and VID before delivery. The new epoch settles SETTLED_RSV_OK from the retired kind while no Talker is registered (`desired` 0). |
| `p11-reset-withdrawal-lost` | `srp_mbx.c:648`, reset no longer latches | **escapes** IF=1/2 | `LinkResetWithdrawsTheSettledRegistration` passes at the head and **fails** at IF=1/2 | A link down, or a down/up with the Talker re-registering before delivery, leaves the listener SETTLED_RSV_OK. The withdrawal is never delivered, and RSV_OK has no timer to recover. |
| `p11-postwithdrawal-kind-overwrite` | `srp_mbx.c:520`, `!s->withdrawn &&` removed | **escapes** IF=1/2 | `LaterKindAfterWithdrawalIsNotReported` passes at the head and **fails** at IF=1/2 | Lv then Failed New before delivery. A spurious REGISTERING_FAILED view change and CHANGED notification are sent before the reprobe. |

  - The other four reviewer plants are equivalent at this head, because another observation point already covers the change. They escape both the author's suite and the probes (`receipts/reviewer-plants-probe-if{1,2}.log`):
    - `p11-tick-snapshot-lost`: the filter and poll snapshots observe expiry.
    - `p11-receive-snapshot-lost`: the next filter or poll snapshot observes it.
    - `p11-kind-change-uncompared`: ACMP's `view_equal` suppresses an unchanged kind.
    - `p11-withdrawn-not-cleared`: delivery requests an SRP stop and unbind zeroes the sink.

    They are not findings.
  - Coverage is 100 % (`srp_mbx.c` 489/489 lines and 454/454 branches; `ctrl_app_srp.c` 82/82 lines and 62/62 branches). The reset `capture` and the reseed lines are executed but asserted by nothing.
- **Impact.** The first two guarantees are what stop a listener from claiming a reservation that does not exist. Either can be removed with every gate green, and the docs and PR body state that they are covered.
- **Required outcome.**
  - Standing integration cases, through real mailbox input and the composition poll at IF=1/2, for identical-identity supersession after an undelivered withdrawal, interface reset of a settled registration, and kind retention across a withdrawal.
  - A named plant for each, caught by its named observable at IF=1/2.
  - Alternatively, narrow the README and PR-body claims for any guarantee that is deliberately left untested, and record that decision publicly.
- **Verification.** The three plants above, or the author's equivalents, are caught by name at IF=1/2. The reviewer probes pass. The coverage ratchet stays at 100 %.

### Suggestion (non-blocking)

- **R532-11-S1 | SUGGESTION | Docs | `srp_mbx.c:126-133`, `docs/design/MAILBOX_SPLIT.md:735-737`.** The filter-time snapshot walks every registrar attribute and every sink once per received AttributeEvent. A full MSRP PDU therefore costs events × attributes × sinks CPU work. The handoff mentions this; the docs carry it only as general "CPU work". Name the term in the CPU-cycle open item so that target calibration measures it. (If F1 is answered by option (a), this term may disappear.)

## 4. Prior public findings at this head

The rows below were read after the provisional verdict and ledger (`receipts/provisional-verdict.txt`, file time in `receipts/provisional-verdict.mtime.txt`).

| Finding | Status at `b98eb2d5` |
|---|---|
| R533-10-F1 (MAJOR): stale REGISTERING_FAILED after a kind change | **Resolved.** Both directions produce the correct `tk_failed` and GET_RX_STATE flags at IF=1/2, through the authorized SETTLED_RSV_OK view entry, with no EVT_TK_REGISTERED replay, no reprobe and `impossible` 0. `R533FailedReplacementUpdatesReportedRegistration` and `R533AdvertiseReplacementClearsReportedFailure` pass at IF=1/2. The probe source sha256 `3c46dfd2...` is fetched from `c27b5ecf` (`receipts/r533-10-probe-source.sha256`). Standing cases and plants exist for each direction. |
| R533-10-F2 (MAJOR): withdrawal erased by same-pass re-registration | **Resolved in behavior.** `R533WithdrawalBeforeReregistrationStillReprobes` passes at IF=1/2, and `R533SeparatePassWithdrawalDoesReprobe` stays green. Expiry followed by a fresh receive is covered (`ExpiryThenRegistrationRetainsTheFirstEvent`, plant caught). The adjacent test gaps for supersession and reset are the new R532-11-F2, and the observation mechanism carries R532-11-F1. Neither is a retention of R533-10-F2. |
| R532-10-F1 (MINOR): kind change while settled never reaches ACMP | **Resolved.** `R10KindChangeWhileSettledReachesAcmp` and `R10FailedToAdvertiseWhileSettledReachesAcmp` pass at IF=1/2 (flags 0x0042 and 0x0002, `impossible` 0). |
| R532-10-F2 (MINOR): two delivery-poll statements without a check | **Resolved.** Both plants are caught by name at IF=1/2, and a standing transient-refusal case exists. |
| R532-10-F3 (MINOR): feedback allowance not falsifiable on the funded path | **Resolved.** The funded path is measured at IF=1/2 and both allowance plants are caught by the measured assertion. My diagnostic `R10WithdrawalFeedbackCostFitsAllowance` (the undiscovered path) still measures 0 accesses and fails its `> 0` check by design. It is not an acceptance case (`receipts/probe-suite-if{1,2}.log`). |
| R532-10-S1: 113-column attach comment | **Taken** (`ctrl_app.h:143-144` wrapped). |
| R532-8-F1 (A0, hosted half), carried | **Hosted half still open.** There is no check run or workflow run at this head (section 7). The local half was confirmed in round 10 and is untouched by this delta. |

## 5. Executable evidence (this reviewer)

All runs used the pinned lwSRP `9197193e` from a separate scratch clone, GCC 16.2.1 for host builds, and at most 16 concurrent compile jobs.

| Work | Result | Receipt |
|---|---|---|
| SRP suites (adapter 53, debug 3, receive recovery 17, `srp_app`, composition 44, latency, walk 5) | PASS at IF=1 and IF=2 | `positive-if{1,2}.log` |
| The same under AddressSanitizer | PASS at IF=1/2 | `asan-positive-if{1,2}.log` |
| The author's 19 named `feedback-*` and `r10-*` SRP plants | 19/19 caught by name at each count | `author-plants-if{1,2}.log` |
| ACMP plants `acmp-kind-lost`, `acmp-kind-any-state`, `acmp-open-unguarded` (entry 10), `acmp-unregistered-anywhere`, `acmp-unregistered-keeps-srp`, plus reviewer `p11-acmp-kind-unguarded` (reentry guard of the new entry, A23 entry 4) | 6/6 caught | `acmp-plants.log` |
| Named round-10 cases (R533 ×4, R532 ×5), the author's SrpFeedback ×11 and the reviewer's R11Feedback ×4 | 24/24 pass at IF=1 and IF=2 | `named-probes-if{1,2}.log` |
| Reviewer plants through the whole composition suite | 7/7 escape at IF=1/2 (3 real gaps: F2; 4 equivalent) | `reviewer-plants-suite-if{1,2}.log` |
| Reviewer plants through the reviewer probes | 3/7 caught at IF=1/2; 4 equivalent | `reviewer-plants-probe-if{1,2}.log` |
| Coverage checker (`fw_coverage.py --check --jobs 4`) | PASS, 22 files at 100 % after unchanged exclusions | `coverage-check.log` |
| Linked images, CI-pinned SDK installed offline after digest check, runtime from the provisioned sources | RAM span 79,904 / 92,576 (1x1, IF=1/2) and 94,736 / 122,240 (8x8), equal to the author's figures. F3 `ctrl_image`, `ctrl_image_selftest` and `fw_rv32_selftest` rc 0. | `images.log`, `images/*.size.json`, `sdk-install.log` |
| Docs and idiom gates: `docs_check`, `check_doc_style`, `check_doc_paths`, `check_em_dash --base d8b355fe`, `gen_toc --check`, `check_cpp_idiom`, `check_py_idiom`, `gen_mailbox --check`, `check_hygiene --check`, `check_baremetal_only --check`, `git diff --check` | All rc 0. The em-dash and TOC checks ran with the pinned Markdown renderer installed in a scratch environment. | `docs-checks.log` |
| Clone integrity after all work | Index tree equals HEAD tree, 0 worktree diffs, 0 untracked or ignored entries, gitlinks unchanged, checked-out submodules clean | `clone-integrity.txt` |

Two runs were repeated and superseded:

- The first probe-copy attempt failed before compiling, because the disposable copy was not a git checkout.
- The first image attempt was refused, because the disposable copy lacked its own lwSRP checkout.

Both were rerun in proper disposable clones, and only the reruns are cited. The probe-copy suite runs return rc 1 only because of the by-design undiscovered-path diagnostic named in section 4.

## 6. Reviewer ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `acmp.c:1132-1143` (Table 5.30 entry contract), `acmp.c:382-414,847-848` (Table 5.23 view and GET_RX_STATE flag), `ctrl_app_srp.c:84-99` (5.5.3.5.42/.48 delivery order), `MAILBOX_SPLIT.md:715-743` (bound figures equal the compiled 3224/4073), `receipts/named-probes-if{1,2}.log` (wire flags and reprobe state) | R532-11 | `b98eb2d5a21522bab3bc6bb943332cf8edf11893` |
| RTL | UNCLEAN (F1) | `srp_mbx.c:44-54,126-133,381-399,512-536,624-652,700-716`, `ctrl_app_srp.c:50-104`, `acmp.c:357-378,1115-1158`, `ctrl_app.h:67-75`, lwSRP `mrp_mad.c:990-1060,1170-1196`, `mrp.h:288-293,413-419`, `doc/integrator.md:319-324` | R532-11 | `b98eb2d5a21522bab3bc6bb943332cf8edf11893` |
| Robustness | CLEAN | Reset, supersession, refusal, idempotence and ordering paths at `srp_mbx.c:515-536,640-652`, `ctrl_app_srp.c:62-101`; `receipts/named-probes-if{1,2}.log` (all reviewer reset, reseed, retention and idempotence probes pass at the head); `asan-positive-if{1,2}.log` | R532-11 | `b98eb2d5a21522bab3bc6bb943332cf8edf11893` |
| Tests | UNCLEAN (F2) | `srp_feedback.hpp:1-194`, `srp_binding.hpp:270-283`, `test_acmp.cpp:751-777,1286-1300`, `srp_mutants.py:707-830`, `acmp_mutants.py:347-365`, `acmp_review_mutants.py:252-256`, `test_ctrl_firmware.py:199-203`; `receipts/author-plants-*`, `acmp-plants.log`, `reviewer-plants-*` | R532-11 | `b98eb2d5a21522bab3bc6bb943332cf8edf11893` |
| Docs | UNCLEAN (F1, F2) | `srp/README.md:53-90,253-262`, `ctrl/README.md:131-163`, `acmp.h:417-424`, `MAILBOX_SPLIT.md:712-745`, `ctrl_app.h:67-75,140-150`; live PR body (= packet `PR-BODY.md`); `docs-checks.log` | R532-11 | `b98eb2d5a21522bab3bc6bb943332cf8edf11893` |

## 7. Limits and pending manager duties

- **Hosted evidence.** At the query time in `receipts/gh-query-time.txt` the PR head is `b98eb2d5`, the PR is open and not a draft, and the base is `dev`. The commit has 0 check runs, 0 workflow runs and 0 statuses (`gh-*.tsv`, `gh-pr-state.txt`). No hosted job was executed at this head, so there is nothing hosted to cite. Hosted and act acceptance, and the hosted half of R532-8-F1, remain with the manager.
- **Gates not re-run.** I did not run the full builder, parent, PP, gPTP or Yosys banks, the complete control campaign, the saved-state campaign, the compiler audits, the mailbox Verilator suite or the MAAP differential. I rely on the manager's published source and builder evidence for those. The round-11 delta touches no `tb`, `sw/mailbox` or builder input.
- **Calibration.** Physical calibration was NOT RUN, and field skips are not hardware proof. The timing tables remain uncalibrated host envelopes (mailbox accesses only). The 8,192-byte stack is a reservation.
- **Allowance.** The feedback allowance is measured on a two-sink fixture. The 16-sink worst case is analytic, from the per-entry timer and clock reads.
- **lwSRP.** lwSRP objects are built with ordinary flags under AddressSanitizer, as in the harness. I make no instrumentation claim for the library.
- **Merge candidate.** Source validation here is distinct from the final current-dev candidate (source base `d8b355fe`, live dev `291710b1`), which the manager builds at the merge turn. Post-merge containment and the merge authorization also remain with the manager.

R532-11 FINISHED
