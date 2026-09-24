[A255]

Closes #43
Closes #49

GET_STREAM_INFO now reads input failure information from the SRP registrar and probing/ACMP status from committed listener records. Input selectors 5 and 7 are handled inside the processor, and selector 4's failure-code byte comes from SRP. These owners are read live at each gather beat. The processor's top-level interface and the parent instantiation are unchanged.

Solicited and unsolicited responses use the same gather. Every committed change of an input field the processor observes notifies registered controllers once: probing/ACMP status, started/stopped (including a re-bind that flips STREAMING_WAIT), Talker registration and a changed Talker Failed FailureInformation. A changed FailureInformation only notifies. It does not re-declare the Listener attribute on the wire. A missing descriptor returns the full zero body.

Response tests drive real binding, discovery, probe timeout, settle, failure registration, withdrawal, re-bind and unbind transitions across two sinks, plus reset, a missing descriptor and an out-of-shape index. MSRP frames on the wire are checked around a changed FailureInformation. Thirteen retained mutations fail named checks; golden and restored controls pass 488 checks each.

A new binding first becomes ACTIVE, then reaches PASSIVE after unanswered probes and backoff, following Milan 5.5.3.5.3 and 5.5.3.5.29. Both states are checked.

## Round 2

Round 1 (`57715787`) had two NEGATIVE reviews, R294-1 and R295-1. The manager's decision is on issue #43. Each required item is below.

**1. Re-bind notification (R295-1 F1).**
- **Cause.** Round 1 replaced the bind, settle and teardown notification terms with the committed pbsta/acmpsta compare. A re-bind to another talker from PRB_W_RESP keeps ACTIVE/0, so that compare stays silent. The listener's started/stopped pulse still excluded walks that bind, so a STREAMING_WAIT flip on that path pushed nothing.
- **Fix.** The exclusion is removed from `KL_pp_acmp_listener`. The started/stopped pulse and the pbsta compare are both registered off the same record write. A walk that moves both therefore raises one event and one frame.
- **Tests.**
  - GI REBIND-SW: a re-bind from PRB_W_RESP with STREAMING_WAIT gives exactly one unsolicited response. That response carries STREAMING_WAIT and ACTIVE/0, and the solicited body matches it.
  - Unit test RV8: the pulse fires once, one cycle after its record write. A re-bind that keeps STREAMING_WAIT raises no pulse.
- **Retained mutant.** `rebind-started-trigger-removed` restores the exclusion. It fails `GI REBIND-SW: exactly one unsolicited response`.
- **Documentation.** The listener and top comments are corrected. The input trigger set is now stated once, in 06 §7, and §6.2 points to it.

**2. FailureInformation change without re-declaration (R294-1 F1, R295-1 F2).**
- **Fix.** `KL_srp_listener_fsm` raises a separate `evt_tk_fail_chg_o`. It feeds only the GET_STREAM_INFO notify OR in the top. It never drives the applicant with New, never raises EVT_TK_REGISTERED, and never reaches the event router or the ACMP listener. The registration indication is back to fresh registration or type swap only.
- **Tests.**
  - Processor top: a fresh Talker Failed registration still declares Listener New. This is the detector control.
  - Processor top: after the changed refresh, no Listener New appears on the wire. The processor's MSRP frames are parsed value by value to check this.
  - Processor top: FAILED-REFRESH still notifies, and an unchanged refresh stays quiet.
  - Module tests in `srp_stream_fsms` (section L) and `srp_top` (section D) cover strobes and wire silence, the LeaveAll-aged state, swaps, and single and shared streams.
- **Retained mutants.** `failure-change-strobe-removed` and `failure-change-redeclares` fail the named FAILED-REFRESH checks.
- **Documentation.** The behaviour is documented in 10 §6.4 (with an F10.5 self-transition), F06.13, 06 §7 and the F02.10 event catalog.

**3. Selector-0 sample-and-hold removed (R295-1 F3, R294-1 S1).**
- **Change.** The top reads the SRP and listener owners live at each beat.
- **Bound (06 F06.13).** One gather spans a few cycles, longer only while the integrator holds a beat, bounded by the gather watchdog. An owner change inside a gather can mix beats in that one response. That change is itself a trigger, and its pending bit is set after the change. Its own notification therefore follows with coherent values.
- **Registers saved.** Measured on the top's own registers: 81 at 8x8 and 78 at 1x1. The reviewers' `sample-transparent` mutant is moot.

**4. Area (R295-1 S2, R294-1 S3).**
- **Bridge gating.** The SRP bridge output is now the raw latch. The top gates it once, after its index mux, on the addressed sink's registered FAILED.
- **Comparator.** FailureInformation is compared once, on the hit sink. Every candidate sink is registered Failed on the same stream and holds the same latch.
- **Measurement.** Both shapes use the repository's recipe, which now accepts an optional stream shape. Synthesis estimates only:

| Shape | Resource | Base `939c1433` | Round 1 | Round 2 | Round 2 − base |
|---|---|---:|---:|---:|---:|
| 8x8 | LUTs | 28,092 | 28,732 | 28,326 | +234 (+0.83%) |
| 8x8 | Registers | 30,354 | 31,138 | 31,064 | +710 (+2.34%) |
| 1x1 (shipping) | LUTs | 20,978 | 21,163 | 21,245 | +267 (+1.27%) |
| 1x1 (shipping) | Registers | 23,446 | 23,745 | 23,674 | +228 (+0.97%) |

Block RAM is unchanged. Changes by instance, round 2 against round 1:

| Shape | Instance | LUTs | Registers | What changed |
|---|---|---:|---:|---|
| 8x8 | SRP listener | −353 | +8 | Bridge gated once in the top; one hit-sink comparator; +8 is the strobe |
| 8x8 | Top's own logic | +41 | −81 | Live index mux and one bridge gate; the sample-and-hold is gone |
| 1x1 | SRP listener | −47 | +1 | Same changes at one sink |
| 1x1 | Top's own logic | +32 | −78 | Same changes at one sink |

- **Remaining cost.** Against base, the remaining registers are owned state that the new readers keep alive:
  - the per-sink 64-bit bridge latch
  - the decoder's FailureInformation capture (+128 at both shapes)
  - the eight-bit committed status view per sink
- **LUT noise.** LUT moves of a few tens in modules this PR does not touch are synthesis variance. The 1x1 LUT total is dominated by them.
- **Timing.** The new paths meet the 10 ns clock:
  - into the gather-answer register: +4.83 ns
  - from the bridge latch: +5.97 ns

  The worst post-synthesis path is the same pre-existing notification-to-router path in every build.

**5. Also taken.**
- **Index-guard test (R295-1 S1, R294-1 S2).** After the second reset, the GI image carries STREAM_INPUT 0..9. Index 9 would alias sink 1 through the three-bit sink index. GI INDEX-GUARD requires zero internal fields for index 9, with the aliased sink shown non-zero as a control. The check is solicited only, because notifications are raised per hardware sink, so no unsolicited response can name an out-of-shape index. The retained `index-guard-removed` mutant fails it.
- **Portable affinity (R295-1 S3).** The mutant runner pins eight CPUs only where the platform provides affinity calls.
- **`dbg_recwr_*` (R295-1 S4).** These ports are documented in the listener as the functional record write bus: the NVM shadow capture and the GET_STREAM_INFO status view both read it. They are not observability only.

**Not taken.** R294-1 S3's other saving is outside this change: the decoder's registered FailureInformation copy.

**Reviewer probes and mutants, re-run unchanged on an extract of the final head.**

| Reviewer item | Round 1 | Round 2 |
|---|---|---|
| R294 P1 (module) | Changed refresh strobes registration; New on next tick | `reg_strobes=0`, `changed-failure next tick pushes=0`; suite 1087/0 |
| R294 P2 (top, GI) | Two Listener New in the changed window | 0 Listener declarations in the changed window; GI 488/0 |
| R295 R1 | 0 notifications on the re-bind | 1 notification; started 1→0 |
| R295 R2 | 2 Listener New after changed FailureInformation | 0 |
| R295 R3 | No leak | No leak (8 checks, 0 failures) |
| R294 `notify-every-write`, R295 `status-compare-removed`, `desc-type-ignored` | Killed | Killed (unchanged edits) |
| R295 `sink-index-guard-removed` | Survived | Killed (unchanged edit) |
| R294 `index-guard-removed` | Survived | Edit site moved; same edit on the new site killed |
| R294 `sel4-integrator-byte`, `srp-failure-strobe-removed`; R295 `srp-failure-change-strobe-removed` | Killed | Edit site moved; same edit on the new site killed |
| R294 `live-unsampled-fields`, R295 `sample-transparent` | Survived | Moot: sample removed |

## Validation

| Gate | Result |
|---|---|
| Lint (zero tolerance) and every suite | rc 0; 16,416 checks, 0 failures |
| Suite breakdown | processor top 1,948 (GI 488), `srp_stream_fsms` 1,087, `srp_top` 259, `acmp_listener` 2,544 |
| Traceability matrix | 92 rows, 0 untested |
| NVM figure gate | rc 0 |
| Docs gates and `make check` | Links, matrix, waveforms, staleness and diagram lint: rc 0 |
| Off-vendor portability elaboration | rc 0; 36 tops |
| Retained mutant runner | 13 of 13 killed by named checks; golden and restored clean |
| Parent consumer (processor checkout only moved; parent index untouched) | Source lists OK; consumer simulation 371 checks, 0 failures |

The additional scoped lint of the top at 1x1 and 8x8, and of the SRP listener, SRP top and ACMP listener at one sink, reports zero findings. The parent's gitlink-dependent gates, hosted runs and the merge-turn candidate remain the manager's.
