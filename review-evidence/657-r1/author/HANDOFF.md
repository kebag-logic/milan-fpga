[A574]

# Issue 657 handoff

Status: local implementation and validation complete; ready for independent review. Hosted timing and publication remain pending manager action.
Head: `62c261c2d1b899a9cf90c901b25b5a85846dfef6`.
Base: `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.
Branch: `657-render-mutants`.
Executor: [A574]. Internal reviewer: [R568]. External reviewer: [R569].

## Scope and authority

Issue #657 and assignment comment 6082915356; #643, #645, #647;
PR #672; `docs/design/MEDIA_CLOCK_FOLLOWING.md`.
IEEE 1722-2016 clauses 4.4.4.3, 10.4.3 and 10.6 provide the clock-source
and CRF context. The boot precondition and recentre timing are the repository
laws in `MEDIA_CLOCK_FOLLOWING.md` and `docs/design/TIME_SYNC.md:385`.
No normative law or tolerance changes.
Test and campaign correction only. Any required RTL change means STOP.
No push or PR operations are authorized. Hosted timing remains pending.

## Findings and correction

The complete baseline at the assigned base finished with 30 PASS / 4 FAIL,
34 checks, outer make rc 2, 5942.19 s. The four failures were the clean
epoch-only leg, both epoch arrival-skew controls, and the surviving frozen
underrun counter. The original 32 account for 28 PASS / 4 FAIL; both PR #672
additions pass. `baseline-campaign-receipt.json` records the raw log digest.

The direct epoch-only run reports 127 checks and four failures, all T30
recentre counts of zero. The issue reported 114 checks with the same four
failure types. This shortened history omits SERIAL and reaches the CRF
checks before boot pull-in has finished. Giving it the existing bounded
boot dwell used by crf-only makes all 127 checks pass. All four exact
one-action expectations remain unchanged; the later settle recentre is a
separate action under the declared law.

The baseline serial leg reports 58 passing checks but observes 839 frames
and zero repeats. Its repeat-counter assertion is vacuous, and the frozen
counter also passes. The correction adds a two-PDU-period double-rate
physical audio/serial clock burst. It observes 23 frames and 11 actual
serializer repeats. The clean control counts every repeat; the frozen
counter fails exactly the new named check with 11 uncounted repeats.
Suppressing the burst fails exactly the exercised-repeat guard.

An AAF feed pause is insufficient: it can repeat upstream samples while
committing fresh serializer frames. The consumer-clock burst reaches the
serializer underrun contract directly. It follows CRF/LAW grading and runs
while bound: after reset recovery before final bind loss in the default,
and after SERIAL in serial-only. The default and full-history pull-in gates
verify the placement before bind loss; the full campaign also runs the
serial-only placement. Diagnostic variants are separate from gate evidence.

The full campaign retains 34 arms: the original 32 plus PR #672's clean
pull-in leg and missing-settle mutation. Both additions remain required.
No arm, assertion, tolerance or normative law was weakened.

## Acceptance coverage

| Item | Evidence | Status |
|---|---|---|
| Epoch-only clean leg | Boot-dwell diagnostic 127/0; committed campaign clean epoch leg PASS | Met |
| Uncounted repeat killed by named check | Committed campaign kills the frozen-counter mutant through `T6 UNDERRUN: every forced repeat is a counted underrun` | Met |
| Complete campaign 32/32, rc 0 | Original 32/32 plus both PR #672 additions 2/2; complete 34/34, rc 0 | Met locally |
| Serial outer default, four CPUs | Cold 809.21 s, rc 0; 266/0, 71/0, 5/5 | Met locally |
| Hosted timing after push | Push not authorized | Pending manager action |
| Explicit campaign ownership row | `docs/testing/TESTING.md:273` | Met |

## Review coverage

This is an executor record, not a review verdict.

| Lens | Covering round | Head |
|---|---|---|
| Conformance | Pending independent review | Pending |
| RTL | Pending independent review | Pending |
| Robustness | Pending independent review | Pending |
| Tests | Pending independent review | Pending |
| Docs | Pending independent review | Pending |

## Gate table

| Gate | Command | Result |
|---|---|---|
| Baseline campaign | `make -C tb/verilator/milan_dp_render tdm8render-mutants` | 30/34; rc 2; 5942.19 s; exactly the four reported failures |
| Render default | `make -C tb/verilator/milan_dp_render` | rc 0; cold 809.21 s on four CPUs; shipping 266/0, multi-stream 71/0, controls 5/5 |
| Pull-in campaign | `make -C tb/verilator/milan_dp_render tdm8render-pullin PULLIN_JOBS=4` | rc 0; 19/19 legs, 838 checks, zero failures; all law windows graded; 3224.74 s |
| Final campaign | `make -C tb/verilator/milan_dp_render tdm8render-mutants` | 34/34; original 32/32 plus 2/2; rc 0; 7243.92 s |
| Builder bank | `python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration` | rc 0, 1169.34 s; historical gate 11 unrun |
| Docs gates | 41 applicable source checks and self-tests | 41/41 rc 0; five timing-document checks rc 0; added-line gate rc 0 |

## Limits and next actions

The full campaign finished with rc 0. The manager must publish the candidate,
record its hosted timing and required contexts, obtain independent reviews,
validate the merge candidate and perform post-merge containment.
This lane has no authorization to push, create a PR or merge.

## Diagnostic controls completed

| Control | Planted defect / control purpose | Observed result |
|---|---|---|
| Baseline epoch-only | Missing boot-history precondition | 127 checks, four recentre failures; rc 1 |
| Epoch-only boot dwell | Clean counterpart to missing precondition | 127 checks, zero failures; rc 0 |
| Baseline serial | Nominal feed does not force repeats | 839 graded frames, zero repeats; 58 checks pass |
| Baseline serial, frozen counter | Frozen underrun counter against the old stimulus | Survives: 58 checks, zero failures; raw rc 0 |
| New final serial burst, clean | Positive control | 23 frames, 11 repeats, zero uncounted; 66 checks pass |
| New final serial burst, frozen counter | Existing uncounted-repeat mutation | Exactly the new named counter check fails; 11 uncounted repeats; raw rc 1 |
| Burst suppressed | Missing underrun stimulus | Exactly the new exercised-repeat check fails; zero repeats; raw rc 1 |
| Reset, burst, final bind loss | Positive sequence control with the burst while bound | 89 checks, zero failures; rc 0 |

These are diagnostic controls, not independent review or final recipe evidence.

## Builder coverage limit

The required builder bank passed, including RV32 and elaboration requirements.
Its historical gate-11 placed-report calibration did not run: the reference
report is absent. This is not an elaboration/toolchain skip and supplies no
calibration evidence. Builder inputs are unchanged by the proposed correction.

## Applied changes by location

| Location | Change and purpose |
|---|---|
| `tb/verilator/milan_dp_render/sim_tdm8_render.cpp:407` | Bounded double-rate audio/serial-clock stimulus; nominal mode retains the existing ratio. |
| `tb/verilator/milan_dp_render/sim_tdm8_render.cpp:2376` | Force serializer repeats and require exercised repeats, preserved pin-frame identity and padding, counted underruns, and no skips. |
| `tb/verilator/milan_dp_render/sim_tdm8_render.cpp:4450` | Give epoch-only the existing boot dwell; preserve all four exact recentre expectations. |
| `tb/verilator/milan_dp_render/sim_tdm8_render.cpp:4459` | Run the burst after clock-law grading and reset recovery, before the final unbind; serial-only also runs it while bound. |
| `tb/verilator/milan_dp_render/sim_tdm8_render.cpp:4463` | Run the bounded burst in serial-only after SERIAL. |
| `tb/verilator/milan_dp_render/tdm8_render_mutants.py:196` | Require the frozen-counter mutation to fail the new named underrun check. |
| `tb/verilator/milan_dp_render/tdm8_render_mutants.py:503` | Explicitly suppress nested make directory banners; the required outer make invocation is documented. The baseline already built successfully with the available make release. |
| `docs/design/MEDIA_CLOCK_FOLLOWING.md:1653` | Explain the epoch-only boot-history precondition without changing the #386 or #645 laws. |
| `docs/testing/TESTING.md:273` | Assign the explicit campaign to the manager merge bank and retain authors' and reviewers' ownership. |
| `docs/testing/TESTING.md:349` | Record the 809.21 s cold default, its complete population and local margins; hosted acceptance remains pending. |
| `docs/testing/TESTING.md:614` | Record the full 34-arm inventory and the new counter stimulus and oracle. |

Tracked RTL, generated sources, module interfaces and submodule pins are unchanged.

## Complete inherited campaign coverage

Final execution: all 34 inherited arms pass at the recorded head, rc 0. The table names each planted defect and its required failure, or the clean control it protects.

| Planted defect or control | Mode | Required check / observation | Result |
|---|---|---|---|
| wrong physical base: the identity projection | ship --serial-only | T4 PROJECTION: physical keys 2..9 hold the routed sources | PASS |
| wrong slot order: the bank walk runs backwards | ship --serial-only | T6 IDENTITY: every decoded frame is a complete 24-bit match against the injection record | PASS |
| shared identity corruption: one pdu bit of EVERY channel | ship --serial-only | T6 IDENTITY: every decoded frame is a complete 24-bit match against the injection record | PASS |
| one-bit phase slip: the bit for position p, not p + 1 | ship --serial-only | T6 PADDING: the eight pad bits of every slot are zero | PASS |
| uncounted repeat: the underrun counter never increments | ship --serial-only | T6 UNDERRUN: every forced repeat is a counted underrun | PASS |
| drop NEWEST: the prefetch keeps the have-next guard | ship --serial-only | T14 SKIP LAW: the forced surplus was COUNTED as skips | PASS |
| the epoch request does not RETAIN across a reset | ship --epoch-only | T18 RESET: the reset epoch reopened EXACTLY once | PASS |
| ungated commit: a closed epoch admits frames anyway | ship --epoch-only | T26 MAP WRITE IN A CLOSED EPOCH: the re-seeded crossbar value never reaches a slot | PASS |
| the serial reset rebuilt from two reconverged levels, with arrival skew | ship --epoch-only | T18 RESET: the reset epoch reopened EXACTLY once | PASS |
| the epoch request races the acknowledgement instead of waiting | ship --epoch-only | T25 DOUBLE EVENT: two bind falls inside one round trip are TWO counted reopenings, not one | PASS |
| the epoch gate reaches the FIFO but not the adapter | ship --epoch-only | T21 COMMIT AROUND RELEASE: the adapter committed no frame between the reset release and the epoch reopening | PASS |
| the graceful flush tears the frame in flight | ship --epoch-only | T27 FLUSH BOUNDARY: ...and every routed slot of it carries ONE media event's identity | PASS |
| the preserved prefill snap keeps a different fill | ship --serial-only | T6 PREFILL: the first event the lane renders is the one the preserved prefill snap leaves at the head, plus its own counted skips | PASS |
| modelled bit-arrival skew, raw binary transport | ship --serial-only | T28 COUNTERS: no sampled frame count ran ahead of the frames the pins delivered | PASS |
| the clock-source trigger dropped from the recentre set | ship --crf-only | T30 CRF: ...as exactly one render recentre pulse | PASS |
| A2-a removed: the aligner is not engaged at INTERNAL | ship --law-only | Every one of 18 named phase checks: T30 INTERNAL LAW +0: the aligner held its settled report through the phase | PASS |
| the render setpoint one event low | ship --law-only | Every one of 36 named phase checks: T30 INTERNAL LAW +0: the fill at every PDU end is the setpoint plus that PDU, 14 events | PASS |
| the render setpoint one event high | ship --law-only | Every one of 36 named phase checks: T30 INTERNAL LAW +0: the fill at every PDU end is the setpoint plus that PDU, 14 events | PASS |
| the settle recentre never pulses | ship --pullin | T647 PULLIN +1562 after the settle: every PDU's first event is inside the law band from its PDU end | PASS |
| the bind-fall mask is not stream qualified | multi whole | M3 UNRELATED LOSS: the adapter's commit gate never closed, not for one cycle | PASS |
| the lane's stream set ignores the mapping's stream field | multi whole | M5 RENDERED LOSS: the adapter's commit gate CLOSED, which the unrelated loss never did | PASS |
| the CSR protocol-store mirror gated on the physical projection | multi whole | M6 NONPHYSICAL: ...and the SAME write is still mirrored into the AECP protocol store, read back through GET_AUDIO_MAP | PASS |
| stopped render clock | ship --defect-stopped-clock | T5 FRAMING: the window decoded whole frames | PASS |
| a single changed sample | ship --defect-one-sample | T6 IDENTITY: every decoded frame is a complete 24-bit match against the injection record | PASS |
| the clock-source selection names INTERNAL | ship --defect-internal-select | T30 CRF: the media plane's one registered resolve reads CRF | PASS |
| Clean: modelled arrival skew, one extra cycle on the acknowledgement level | ship --epoch-only | Entire clean leg must pass | PASS |
| Clean: modelled arrival skew, one extra cycle on the serial-reset level | ship --epoch-only | Entire clean leg must pass | PASS |
| Clean: modelled bit-arrival skew, gray retained | ship --serial-only | Entire clean leg must pass | PASS |
| Unmodified positive control | multi whole | Entire clean leg must pass | PASS |
| Unmodified positive control | ship --crf-only | Entire clean leg must pass | PASS |
| Unmodified positive control | ship --epoch-only | Entire clean leg must pass | PASS |
| Unmodified positive control | ship --law-only | Entire clean leg must pass | PASS |
| Unmodified positive control | ship --pullin | Entire clean leg must pass | PASS |
| Unmodified positive control | ship --serial-only | Entire clean leg must pass | PASS |

The original 32 exclude only the clean `--pullin` mode and
the missing-settle mutation introduced by PR #672. Those two additions
must pass too; they are neither removed nor credited as a substitute.

## Documentation and source gate commands

All commands below returned rc 0. The accompanying receipts record elapsed
time, output size and SHA-256. After the timing paragraph changed, the five
documentation checks in `timing-docs-receipts.json` passed again.
The added-line gate passed on the committed head, including 339 planted arms.

| Command | Result |
|---|---|
| `python3 -B scripts/docs_check.py` | rc 0 |
| `python3 -B scripts/check_doc_style.py` | rc 0 |
| `python3 -B scripts/check_doc_style.py --selftest` | rc 0 |
| `python3 -B scripts/check_gptp_docs.py --with-submodule` | rc 0 |
| `python3 -B scripts/check_gptp_docs.py --selftest` | rc 0 |
| `python3 -B scripts/check_solution_docs.py` | rc 0 |
| `python3 -B scripts/check_solution_docs.py --selftest` | rc 0 |
| `python3 -B scripts/check_feature_status.py --self-test` | rc 0 |
| `python3 -B docs/traceability/gen_module_matrix.py --check` | rc 0 |
| `python3 -B scripts/check_doc_paths.py` | rc 0 |
| `python3 -B scripts/check_archive.py` | rc 0 |
| `python3 -B scripts/check_archive.py --selftest` | rc 0 |
| `python3 -B scripts/gen_toc.py --selftest` | rc 0 |
| `python3 -B scripts/gen_toc.py --verify-anchors` | rc 0 |
| `python3 -B scripts/gen_toc.py --check` | rc 0 |
| `python3 -B scripts/check_cpp_idiom.py` | rc 0 |
| `python3 -B scripts/check_cpp_idiom.py --selftest` | rc 0 |
| `python3 -B scripts/check_py_idiom.py` | rc 0 |
| `python3 -B scripts/check_py_idiom.py --selftest` | rc 0 |
| `python3 -B scripts/check_sh_idiom.py` | rc 0 |
| `python3 -B scripts/check_sh_idiom.py --selftest` | rc 0 |
| `python3 -B scripts/check_hygiene.py --check` | rc 0 |
| `python3 -B scripts/check_hygiene.py --selftest` | rc 0 |
| `python3 -B scripts/measure_fail_fast.py --check` | rc 0 |
| `python3 -B scripts/measure_fail_fast.py --selftest` | rc 0 |
| `python3 -B scripts/measure_test_evidence.py --check` | rc 0 |
| `python3 -B scripts/measure_test_evidence.py --selftest` | rc 0 |
| `python3 -B scripts/check_todo_ownership.py` | rc 0 |
| `python3 -B scripts/check_todo_ownership.py --selftest` | rc 0 |
| `python3 -B scripts/pp_srcs.py --check` | rc 0 |
| `python3 -B scripts/pp_srcs.py --selftest` | rc 0 |
| `python3 -B scripts/check_rtl_source_lists.py` | rc 0 |
| `python3 -B scripts/check_rtl_source_lists.py --selftest` | rc 0 |
| `python3 -B scripts/check_soc_sources.py` | rc 0 |
| `python3 -B scripts/check_soc_sources.py --selftest` | rc 0 |
| `python3 -B scripts/measure_control_flow.py --selftest` | rc 0 |
| `python3 -B scripts/measure_cohesion.py --selftest` | rc 0 |
| `python3 -B scripts/ci_events.py --check` | rc 0 |
| `python3 -B scripts/ci_events.py --selftest` | rc 0 |
| `python3 -B scripts/suite_tally.py --selftest` | rc 0 |
| `python3 -B scripts/check_em_dash.py --selftest` | rc 0 |

These self-tests exercise their own embedded violating fixtures. The
behavioral planted defects for this change are the frozen underrun counter,
suppressed serial-clock burst, and the full named campaign inventory above.

## Pull-in coverage

The 18 boot phases and full-history leg all pass on the committed code.
Every law window was graded; none was excluded as ambiguous. The standing
phase at +1562 is the negative-control counterpart of the missing-settle
mutation in the full campaign. These positive legs do not claim a separate
mutant run at every phase.

| History / phase | Checks | Failures | Law windows |
|---|---:|---:|---|
| 0 | 31 | 0 | All graded |
| 130 | 31 | 0 | All graded |
| 260 | 31 | 0 | All graded |
| 391 | 31 | 0 | All graded |
| 521 | 31 | 0 | All graded |
| 651 | 31 | 0 | All graded |
| 781 | 31 | 0 | All graded |
| 911 | 31 | 0 | All graded |
| 927 | 31 | 0 | All graded |
| 1042 | 31 | 0 | All graded |
| 1156 | 31 | 0 | All graded |
| 1172 | 31 | 0 | All graded |
| 1302 | 31 | 0 | All graded |
| 1432 | 31 | 0 | All graded |
| 1562 | 31 | 0 | All graded |
| 1693 | 31 | 0 | All graded |
| 1823 | 31 | 0 | All graded |
| 1953 | 31 | 0 | All graded |
| Full history / +1562 | 280 | 0 | All graded |

## Evidence index and reproduction

All paths below are relative to this evidence bundle. Source references in
this document name repository paths at the recorded head.

- `baseline-campaign-summary.log` and `baseline-campaign-receipt.json`:
  complete unmodified-base inventory and the four reproduced failures.
- `final-campaign-summary.log` and `final-campaign-receipt.json`: all 34 passing verdicts, original/additional inventory split, timing and raw log digest.
- `candidate-inputs.json`: sizes and SHA-256 values of the shipping harness,
  campaign driver and Makefile used by the cold default and final campaign.
- `default-cold-summary.log` and `default-cold-receipt.json`:
  both cold model builds, complete default population, timing and affinity.
- `pullin-receipt.json` and `pullin/`: all 19 phase/history results, with
  phase tags checked against their requested values and no excluded window.
- `builder-summary.log` and `builder-receipt.json`: bank outcome, raw log
  digest and the one explicitly unrun historical calibration arm.
- `docs-gate-receipts.json`, `timing-docs-receipts.json` and
  `em-dash-receipt.json`: exact commands, return codes and evidence digests.
- `diagnostic-receipts.json`: the clean, frozen-counter, burst-suppressed,
  epoch and bound-sequence controls; their small logs are included.
- `standard-receipt.json`: clauses consulted and the standard file digest;
  no standard text is reproduced.
- `retired-build-receipts.json`: digests and sizes of completed diagnostic
  executables removed from scratch to conserve storage.

The environment and primary commands are in `PR-BODY.md`; all 41 source
and documentation commands are listed above. The actual separate pull-in
run used `PULLIN_OUT="$PULLIN_LOGS"` and
`TDM8R_MDIR="$PULLIN_MODEL_REL"`. Both resolve under the assigned scratch
area; the latter is relative to the suite directory because its run recipe
prefixes the executable with `./`. This keeps concurrent builds separate.
The cold default had a serial outer make, two build workers and four CPUs;
no other heavy job in this lane ran beside that timing measurement.

The cold default ran before the commit was recorded; its executable input hashes match the committed files. The final mutation and pull-in campaigns ran at the recorded head. Builder inputs were unchanged by the four-file correction. The timing paragraph was checked after it was added.

## Final repository audit

The checkout is clean. All root generated products and caches were moved to
the assigned scratch area after every long job completed. Their executable
sizes and SHA-256 values are in `final-build-receipts.json`; no binaries or tree
exports are in this bundle. `repository-audit.json` records the four-file scope,
unchanged parent and pins, one-line commit, resource measurements and cleanup.
The measured service memory peak was 6,759,710,720 bytes; final disk free space
was 92,600,016,896 bytes, above the required floor.

The four initialized submodules each passed a repository-boundary check before
their HEAD was read, and each matches its tracked pin. The separate `external`
entry is uninitialized: its boundary check resolves to the parent repository.
No subsequent command was run inside it. Its tracked gitlink matches the base;
the required gates passed in this state. This audit supplies no working-copy
HEAD claim for that entry.
