# [A154] PR #503 revision d: response to the round-three reviews

Heads for re-review:

- Page: `2a2007cff57bd2a01254e1da7c43ec73b9d8d4b3`, branch
  `500-d3-materialization-adr`, base dev
  `2d8fd62fd986ea2d6a87d284e144f023034c0944` (an ancestor).
- Evidence: `c1ee27d81c4a1e98f9584e979b73a88acfe238b3`, branch
  `500-design-evidence` (never merged; its tree stays on dev `07294a76`).
  The executed-run sources are `a78c79afebab98d53b94c034c92f7191989e8806`;
  the four commits after it change records, results and documentation only.
- Reviewed heads: page `ab0fb23f`, evidence `fc2e3a62`.

Answering a finding does not clear it. Each reviewer re-reviews these heads
and publishes its own verdict and ledger; no lens is claimed covered here.
Every finding keeps the reviewer's severity and every lens label. No product
RTL or firmware changed. No processor issue was filed: T8 and T9 stay
drafts, and processor issues 15 and 20 stay open.

## Round-three findings

| Finding | Severity and lenses | Answer (page sections) | Evidence at `c1ee27d8` |
|---|---|---|---|
| R217 R3-F1: unbounded listener preload still defeats the promised command-recovery bound | MAJOR; Conformance, RTL, Robustness, Tests, Docs | seam S4, the listener's boot-owned admission, a prerequisite of stage 1 and of every shippable stage (T8) (2, 3 rules 7, 8 and 11, 4, 5.1, 5.3, 6.2, 6.3, 8.1, 8.6, 8.8, 8.9, 10 to 16) | L00 to L13, L03b, L06b, L08a/b, L10 m1/0/p1 at 1x1 and 8x8; LG01 to LG05; tracked L01, L05; R217's round-three probe, adapted (20 runs) |
| R218 R3-F1: stage 1 defers descriptor recovery needed for its finite-timeout acceptance | MAJOR; Conformance, RTL, Robustness, Tests, Docs | the descriptor store's roll-back reset belongs to stage 1 with the dynamic-state store's (T1); the guard's debt survives it (T9); stage 2 adds no owner (T2) (3 rule 11, 5.1, 8.6, 8.8, 10, 11, 13, 14, 15 item 14) | S1a to S1h on the stage-1 build and both full builds; ST1; R218's reproduction, adapted (12 runs); DG01, DG02 |

### R217 R3-F1 (MAJOR; Conformance, RTL, Robustness, Tests, Docs)

The selected mechanism is an enforced admission gate,
`KL_pp_acmp_lsn_admit`, in front of the UNCHANGED pinned
`KL_pp_acmp_listener`'s four work faces. It is not a timeout, and nothing is
released on time.

- **Ownership and reset.** It owns the faces from the hard reset, which the
  gate and the listener share; neither takes the D3 roll-back. It releases
  them once: when the binding walk is at its terminal (done or failed), no
  preload is presented, the listener is idle and its last A4 discovery
  strobe has left. The binding manager never walks again before a reset, so
  the gate never owns the faces again before one.
- **The faces while owned.** A transaction and a talker event are held at
  their producers, valid AND ready masked. On those faces ready is an
  acceptance, so nothing is consumed unseen and nothing is popped unserved.
  START/STOP: the request's valid is masked and the listener's completion
  passes (next section). Timer expiries are not admitted, and each
  listener-owner expiry is counted. None can be legitimate, because the
  listener arms its timers only in walks the gate holds off, and the timer
  service's armed bits reset to 0.
- **The bound comes from construction, not fairness.** With nothing else
  admitted, the listener can only be in X_INIT, X_IDLE or X_PRELOAD, so a
  preload is taken in the cycle it is presented. The preload phase ends
  within four cycles a sink plus four. The release follows the walk's
  terminal within four cycles (two after a preload and one without, in the
  evidence). The phase has no failure exit, and no partial binding image
  can be left.
- **Order.** The release starts the listener's live ACMP work and the D3
  walk. `restore_done_o` is the release AND the D3 walk's done, and it gates
  the entity enable, so neither the D3 walk nor the enable precedes the last
  preload's record write and discovery arm. A D3 roll-back leaves the
  completed binding restore in place (L13).
- **Cost** (out of context; estimates, not bounds). The gate alone is 13 LUT
  and 17 FF at 1x1 and 14 and 17 at 8x8; 16 of those flops are its
  diagnostic expiry count. In place it adds +13/+17 (1x1) and +8/+17 (8x8)
  to the pinned listener's 2,174/1,530 and 2,268/1,557. Candidate (b) with
  S1 to S4 is 2,506 LUT and 942 FF at 1x1 and 3,242 and 1,163 at 8x8, about
  3.95 and 5.11 percent of the XC7A100T's LUT.

Evidence. The harness uses the real pinned listener (its ROM comes from the
pinned generator) and the real timer service. Every producer holds a
presented request until its handshake. Each case is graded on the listener's
own valid AND ready, its record writes, its A4 arms, its PDUs and its
GET_RX_STATE answers, on the slot, and on a controller's AECP GET and SET
after recovery. At 1x1, L00 reads "preload offers from 235: the longest
untaken 0 cycles, 0 withdrawn, 0 left open; the walk's terminal at 241 (6
cycles after the first offer, bound 12), the listener released at 243".

| R217's required test | Where |
|---|---|
| persistent and finite backpressure (R217's lever) | L01, L02; R217's probe, adapted only in its lever: with the gate, the held and the finite level end where the ready control does ("binding walk ends at 178 (control 178), D3 terminal 7606 (control 7606), enable 7613, GET (1500000, 1)") |
| first and later sinks | L03, L05, L08a; both sinks in every case |
| START/STOP, transaction, timer and talker-event interference | L06, L06b; L04, L05, L09, L10; L07; L01 to L03b |
| near the admission, deadline and release boundaries | L10 m1, 0 and p1 (the last owned, first released and next cycle); L11 (the binding read 40 cycles short of its deadline), L12 (past it) |
| reset during the preload phase | L08a (power cut as the last sink's preload is taken), L08b (the next boot) |
| last sink's commit and discovery against the release | `release_after_the_final_preload_action` in every L case |
| no delayed preload, discovery or live-state overwrite | the same check; L03b; L09 |
| usable GET and SET after recovery | every case |
| a named deletion mutant restoring starvation, killed by a completed bounded scenario | LG01 (the gate deleted: the pinned wiring), killed by L01 ("the longest untaken 3229969 cycles, 2 withdrawn") and by L05 |
| the real valid AND ready and the listener's committed state | every case (`held_requests_taken_once_after_release`, record writes, the slot) |
| live-touch suppression and queued events | L05 (a read-only GET_RX_STATE between a sink's store and its preload); L03b |
| a failure after an earlier sink was preloaded | once nothing else is admitted, the preload phase has no failure exit. The failures that remain reachable there are a power cut (L08a, L08b) and a D3 failure after both preloads (L13) |
| port silence, quarantine and drain | W13, W13b, W13c, W15, W16, L12, retained |

LG02 (valid admitted, ready masked), LG03 (valid masked, ready passed), LG04
(expiries admitted) and LG05 (START/STOP admitted) are each killed by every
check named for them, in completed runs. The tracked glue, which is the
pinned wiring, fails L01 and L05 as the runner requires. R217's own
round-three checker exits 1 on the gate's results, with both counterexample
assertions false. On LG01's results its held assertion holds again.

### START/STOP completion (A10's final-doc item)

The gate masks the START/STOP request's VALID and passes the listener's
completion (`strm_set_ready_o`, `strm_set_error_o`) unmasked. That face is
not an acceptance handshake. The engine holds its request until the
completion, which the listener raises once the record commit or the no-op
check is done (error when its bounded wait expires). The listener captures
a presented request into its holder in any state.

The reset-owned invariant makes this safe. The holder and its done and fail
flags reset to 0 and fill only from a presented request. The gate owns the
faces from the same hard reset, and neither module takes the roll-back.
From reset to the release the holder therefore stays empty and no
completion can fire, so a passed completion never answers a request the
listener did not capture. Masking the completion as well would change
nothing while the gate owns the faces. Every L case grades that no
START/STOP request is captured while the gate owns the faces and that
captures and completions agree in number (L06 and L06b hold a request from
reset).

Paired valid-and-ready masking stays explicit for the transaction and
talker-event faces.

**Superseded wording.** The initial decision recorded paired masks on all
three faces. The prototype as built and run (`a78c79af`) always used the
face-specific rule above, and its header says why. The page (rules 8 and
11, sections 5.1, 6.3, 8.9 and 16), T8 and the evidence README now state it
exactly.

### R218 R3-F1 (MAJOR; Conformance, RTL, Robustness, Tests, Docs)

- **Stage 1 owns both stores' roll-back resets:** the dynamic-state store's
  and the descriptor store's. For the descriptor store, its reset or a
  re-walk request that also returns its fetch watchdog count to zero.
- **Why stage 1 needs it.** The pinned store's response-timeout branch
  (`KL_aecp_desc_store.sv` line 980) leaves the count at its limit, so the
  next fetch errs in its first cycle (line 938). That error clears the
  count, and in ordinary service the fetch after it succeeds (V23). The
  roll-back, however, proves the image by one LOCATE, and that LOCATE is
  the next fetch.
- **The guard and stage 2.** The guard's response debt (S2) survives the
  roll-back reset, because it takes the hard reset only (T9). Stage 2 adds
  no owner: its names come back on stage 1's reset (T2).
- **Evidence.** A stage-1 build (`D3_STAGE1`: both stores roll back, the
  map plane does not) runs R218's selector-only slot. The same cases also
  run on both full builds.

| Case | Stimulus | Result |
|---|---|---|
| S1a | no fault | COMPLETE |
| S1b | 4,000 cycles late, below the store's watchdog | COMPLETE |
| S1c | 5,000 cycles late | DEFAULTS, commands served; "the owners left reset at 7455" |
| S1d | 16,000 cycles late | DEFAULTS, commands served; "18455" |
| S1e | 30,000 cycles late, beyond the D3 deadline | CLOSED |
| S1f | one error beat | DEFAULTS |
| S1g | the memory fails from before boot | CLOSED, cause 7 |
| S1h | a payload read error | DEFAULTS |

- **Mutants and the reviewer's reproduction.**
  ST1_stage1_rollback_skips_desc_store (revision c's stage-1 scope) is
  killed by S1c and S1d: "D3 done 0 fail 1 rolled back 0 (want 1) closed 1
  own 1 cause 6". R218's reproduction, adapted, gives 12 runs as demanded.
  With the store's reset, V21 and V21b end in DEFAULTS ("terminal 8110,
  enable 8123"; "terminal 19110, enable 19118"). Without it (R03, ST1)
  they end CLOSED. The one-error control V20b recovers either way. DG01
  and DG02 are retained and killed.

## Integration clarification (A10, PR #503 comment 5762146376; not a finding)

The page's section 8.1 now states three separate release points, and T1, T4
and T8 state the same:

| Release point | What runs from it |
|---|---|
| S4's release, the binding walk's drained terminal | the listener's live ACMP work: held and later commands, talker events, START/STOP once AECP runs, and the expiries of its own live walks |
| the D3 terminal, COMPLETE or DEFAULTS | the state bus, and with it AECP dispatch |
| the combined enable, `(PP_CTRL[0] OR ADP_CTRL[0]) AND restore_done` | ADP advertising (F07.9, "ADP may start") |

Live ACMP work after S4 is not a late restore action. No preload is
presented after the release, and every preload's record write and discovery
arm precede it. A live change after the release follows the restored image
and persists as a live change.

The enable freezes no traffic. In the pinned top it reaches only the ADP
engine, which holds its advertise state machines in DOWN, and the side
port's image-window lock. The talker-discovery state machines are a separate
path. A CLOSED terminal holds AECP and the enable, and does not take the
listener back.

L04 at 1x1 shows the three points separately. The listener first takes a
polled GET_RX_STATE at 243, the D3 terminal is at 3879, and the entity is
enabled at 3893.

## Prior findings: original severities and lenses, controls retained

| Prior finding | Severity and lenses | Round-three dispositions (R217 / R218) | Revision d |
|---|---|---|---|
| R217 R2-F1 / R218 F1: header failures | MAJOR; Conformance, RTL, Robustness, Tests, Docs, for each | resolved for the proposal / corrected in the proposal and model | retained: H1 to H8, V18, V18b, V18c, W16; C01 to C03, B02, B04 |
| R217 R2-F2: descriptor errors, watchdog, initial image | MAJOR; Conformance, RTL, Robustness, Tests, Docs | resolved for the proposal / partially corrected, open through R218 R3-F1 | its stage-1 remainder is answered as R218 R3-F1; V20 to V23, V17, V2b; DF01 to DF03, IMG01, DG01, DG02 retained |
| R217 R2-F3: unbounded binding walk, incompatible recovery promise | MAJOR; Conformance, RTL, Robustness, Tests, Docs | partly corrected, open as R3-F1 / read-silence defect corrected | its preload-phase remainder is answered as R217 R3-F1; W13, W13b, W13c, W15, W16, W14; B01, B03, G05 retained |
| R218 F6: synthetic output judge | MINOR; Tests, Docs | corrected / corrected | retained: V1s_a, V1s_b, V1s_c, the synthetic labels |
| R218 F7: T8 promised reuse after permanent silence | MINOR; Docs | corrected / corrected | retained: T8 keeps quarantine for ever, claims no reuse, and S4 releases no port |
| R217 F1 / R218 F1, round one: partial restore | MAJOR; Conformance, RTL, Robustness, Tests, Docs, for each | corrected, retained | retained: pass-0 validation, per-record agreement, whole-D3 roll-back; V11b to V18, M13 |
| R217 F2 / R218 F2, round one: early enable | MAJOR; Conformance, RTL, Robustness, Tests, Docs, for each | corrected, retained | retained, and the enable now also waits for S4's release: G02, G05, W14, V1b |
| R217 F3: padding aliases | MAJOR; Conformance, RTL, Robustness, Tests, Docs | resolved, retained | retained: V3a to V3g |
| R217 F4: capacity and status staging | MAJOR; Conformance, RTL, Robustness, Docs | resolved, retained | retained: stage 3 blocked on #501, every shippable stage on #502 (both open) |
| R217 F5: process success as verdict | MINOR; Tests, Docs | resolved, retained | retained: the 8 CLI controls |
| R218 F3: runner accepts survivors and crashes | MAJOR; Tests, Docs | corroborated / corrected and retained | retained: FULL and FOCUSED runs, INCOMPLETE, named killers in completed runs, 8 controls |
| R218 F4: configuration replay deletion survives | MAJOR; Conformance, Tests, Docs | retained / corrected and retained | retained: 9 trigger and 9 replay deletions, the configuration valid flag, the synthetic-rate label |
| R218 F5: stages permit capacity and status defects | MAJOR; Conformance, Robustness, Tests, Docs | verified / corrected, product issues open | retained: #501 and #502 gates |

Also retained without change: the header classification, the port's cause
(S1), the per-record agreement, the padding rule, the shipping format judge,
the configuration valid flag, the CLI exit statuses and controls, O1 and O3,
the snapshot obligations, and the live-write amendment request (UNRESOLVED
1). The FULL run from empty trees grades all of them: 76 builds, 386 runs,
4,560 checks, 0 verdict failures, and 71 of 71 mutants killed.

## A separate defect in the pinned wiring, for the manager

Tracked control L05 shows a defect of today's shipping wiring, independent
of D3. A read-only GET_RX_STATE served during the binding walk, between a
sink's stored record and its preload, runs the listener's record
write-back. The binding manager captures that write-back as a live change,
marks the sink touched, withdraws its preload and flushes the unbound
record over the saved binding. At the pinned wiring, L05 reads "answered
[(0, '0000000000000000')]; sink 0 in the newest verified slot
000000000000000000000000".

The window is the boot binding walk. ACMP dispatch is not gated by the
entity enable, so a controller that already knows the entity can hit it.
S4 closes it for this design, and T8's acceptance names it. It has no
processor issue of its own, and filing one is the manager's decision.

## Remaining decisions (none blocks re-review)

1. The live-write trigger amendment (page UNRESOLVED 1), for the accepted
   requirements.
2. Filing T8 (S1, S3, S4) and T9 (S2) in the processor repository, and
   whether the L05 hazard above gets its own issue.
3. #501 (stage 3) and #502 (every shippable stage) remain open.
4. Whether a product narrows the gate's 16-bit diagnostic expiry count to a
   sticky bit (section 12).
5. Board time, integrated area and timing (UNRESOLVED 8 and 9).
6. The producers' own queue policy behind a held head during the binding
   walk (UNRESOLVED 16), which stays the processor's.
