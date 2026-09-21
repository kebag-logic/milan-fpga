[A153] RESPONSE to R217-r2 and R218-r2 (both NEGATIVE at `40d14d92bfcf3823ed7b227537630f444b1f4f73`)

Revised heads, for re-review:
- Page (PR #503): `e67a586f92506c8623079c341e4f56a9c5ae165a` on `500-d3-materialization-adr`. The examined base is dev `07294a76e833f1831d9fcbceb8123b8380c4ae76`, an ancestor. The processor pin is `424c688fa2205b934a7689a58f2aa766420f2326`. Live dev has since moved to `2d8fd62f` (the #498 merge). This checkout was not rebased; the manager integrates base movement.
- Evidence (never merged): `fc2e3a6211bdbca3c41718eb6e1b4b4c2a128293` on `500-design-evidence`. The executed run is its ancestor `bf88b71f22d225ac3671317ab6cc720c41c76d4e`. The three commits after it change only `COMMAND_RESULTS.md`: its digest table and the commit that table names. The page cites `fc2e3a62`.

Each finding keeps the reviewer's own severity and lens labels. "Answered" means the change is made and executed evidence exists at the heads above. It does not mean the finding is cleared; each reviewer re-reviews and decides. No finding is answered by moving it to another issue. The three new interfaces are PREREQUISITES of stage 1. #501 and #502 stay open and keep gating their stages.

## The decision this revision makes

**Failure.** Every transport failure in either pass ends in the declared outcome, with no exception. A transport failure is any of:
- a device error the port reports (new cause, S1);
- a torn read;
- a record read whole in one pass and not in the other;
- a failed descriptor read that a value rule or a revert needs, including the store's own watchdog answer;
- a deadline.

The outcome depends on where the failure lands:
- In pass 0 the restore ends in DEFAULTS with nothing applied.
- In pass 1 it rolls back by owner reset, then ends in DEFAULTS once the image is proven again.
- If the image cannot be proven, at the start or after the roll-back, the restore ends CLOSED: fail, never done, and the entity is never enabled.

A per-record refusal remains in exactly two cases: a record the port reports UNFRAMED, and a framed value that fails a rule the restore actually fetched.

**Availability.** Command service and persistence-device service are separate contracts.
- *Commands.* Both walks are bounded: the binding walk by the new seam S3, the D3 walk by its own deadline. AECP is served on defaults, with restore fail set, after at most two deadlines plus the walks. W13 enables the entity at cycle 40,733.
- *Persistence device.* A read either manager abandoned stays QUARANTINED by the arbiter's drain until the device ends it. A device that never does keeps the port quarantined until reset, and every later change reads pending, never durable.

Nothing releases the port on a timer, and no reuse is claimed. No availability waiver is requested or relied on. Processor issue 15 is neither closed nor amended.

**Three new interfaces.** Each is proposed and prototyped as design evidence only. All three are prerequisites of stage 1 and of every shippable stage:
- S1, the port's terminal cause: `nvm_err_cause_o[1:0]` on `KL_pp_nvm_port`, with 1 DEVICE and 2 UNFRAMED (ticket T8).
- S2, descriptor-memory response isolation: `KL_aecp_desc_mem_guard` holds the store's next request while an accepted burst still owes its terminal beat, and gives the writer `desc_debt` (ticket T9).
- S3, a bounded binding walk: `KL_acmp_nvm_shadow`'s read phase is bounded by `RS_TMO_CYC_P`. Expiry fails the walk whole, preloads nothing and abandons its read to the arbiter's drain (T8).

How the prototypes relate to the pinned RTL:
- The amended port and binding manager are generated from the pinned files by declared amendments only, and renamed (`KL_pp_nvm_port_amd`, `KL_acmp_nvm_shadow_amd`). `run.py` refuses any other difference.
- The tracked-glue build keeps the PINNED modules.
- No product RTL or firmware is changed.

## R217 R2-F1 / R218 F1: header errors still produce a successful partial restore; equal counts do not prove pass agreement

R217 R2-F1: MAJOR; Conformance, RTL, Robustness, Tests, Docs. R218 F1: MAJOR; Conformance, RTL, Robustness, Tests, Docs.

Change (page 3 rules 7 and 11, 5.1, 5.2, 6.2, 6.3, 8.6, 8.7, 10, 13, 15 item 5; tickets T1, T4, T8):
- S1 splits the port's single zero-byte err into two causes:
  - DEVICE: a device error in any state, or a header the device ended short.
  - UNFRAMED: a header delivered whole that fails the magic or length gate.

  The writer keeps a record's default only on UNFRAMED. DEVICE aborts, with or without bytes forwarded. The binding manager consumes the same cause. That also closes processor issue 20's defect, through T8; this page does not close issue 20.
- The passes now agree RECORD BY RECORD, not by counts. The writer keeps a per-record vector: 49 bits at 1x1, 145 at 8x8. A record whole in one pass and not the other aborts at that record (cause 5). With S1 in place, this check exists to catch content that changes between the passes without any device error.
- Restore blank is defined as done AND NOT fail AND no record validated, so a failed restore is never blank. The parent's combined blank follows.
- S1 is a prerequisite of stage 1 and of every shippable stage (page section 10; T1 "Prerequisites"; T4). T1 no longer excludes port changes or treats issue 15 as optional.

Evidence at `fc2e3a62`, at 1x1 and 8x8 on V1a's committed slots unless named:

*Header faults:*
- H1 (R217 header-repeat, R218 repeat: the same header lane fails in both passes): pass 0 aborts at 0x50 with "applied 0, abort cause 2 (a device error)". Every record is at its default: "restore fail 1, D3 fail 1, blank 0".
- H2 (R217 header-balanced: 0x30 in pass 0, 0x50 in pass 1), H2b (R218 swap: 0x51, then 0x50) and H3 (pass 0 only): the same outcome.
- H4, H5, H6 (both passes, at the first record, a map record and the last name): the same, at that record.
- H7 (the last name's header in pass 1 only, after every other record applied): "9 records applied before the fault, roll-back at 6505, abort cause 2".
- H8 (a slot holding 0x50 alone, its header failing in both passes): "restore fail 1, D3 fail 1, blank 0".
- V18 (pass 1 only): "4 records applied before the fault, roll-back at 3760, abort cause 2".
- V18b (no device error; 0x50's header changed at rest after pass 0 read it whole): "roll-back at 3778, abort cause 5".
- V18c (no device error; 0x30 unframed in pass 0 only and 0x50 in pass 1 only, so the counts are equal): "roll-back at 3573, abort cause 5".

*Controls and retained faults:*
- The erased control V10 (every binding and D3 record erased): "restore fail 0 (D3 0, binding 0), causes D3 0 binding 0, done 1", blank 1.
- The separately specified per-record refusal path stays covered: V5 (crc), V3a to V3g (map framing), V2, V2b and V4 (values).
- The payload faults are kept: V11, V11b and V12 to V16, early and late in both passes, after prior applications.
- W16 (1x1): a DEVICE error on the binding record's header fails the binding walk: "binding fail 1 cause 2 (a device error on the header), preloads [], restore fail 1, blank 0".

*Mutants of the new distinction, each killed:*
- C01_device_error_reads_as_blank (round two's rule), by H8.
- C02_port_cause_collapsed (the pinned port's information), by H1: "9 records off their defaults ... D3 done 1 fail 0".
- C03_unframed_reads_as_device_error, by V10: "restore fail 1 (D3 1, binding 0)".
- X01_passes_may_disagree, by V18b.
- X02_passes_compared_by_count (round two's comparison), by V18c.
- B02_binding_device_error_reads_as_empty (issue 20's defect), by W16.
- B04_binding_unframed_reads_as_device_error, by V10.

*Your own probes.* Both reviewers' probe scripts were rerun (`reviewer-probes/`), in copies adapted only in their paths and in the one seam each that moved. Every run holds as demanded:
- R217's header-repeat, header-balanced and header-pass0 read "every row at its default True, done 1 fail 1 (D3 1, cause 2), blank 0, applied 0".
- R218's pass0, repeat, swap and pass1 read "0 records off their defaults ... restore fail 1 blank 0, cause 2".

R217's own `check_probes.py` (at `7d9da877`) now fails at its line 19, its first counterexample assertion.

*Cost.* The amended port adds 4 LUT and 2 FF. The binding manager's S1 and S3 add 107 LUT and 34 FF at 1x1 (103 and 34 at 8x8). The writer's classification and vector are included in its row.

## R217 R2-F2: descriptor-memory errors and timeouts bypass the restore transaction

MAJOR; Conformance, RTL, Robustness, Tests, Docs.

Change (page 3 rules 7 and 11, 5.1, 6.2, 6.3, 8.3, 8.6, 8.8 with the new dependency audit, 10, 15 items 8, 14 and 15; tickets T1, T2, T4, T9):
- **A refusal needs the rule.** Suppose a descriptor read that a value rule or a revert needs ends in error, either as a fetch error beat or as the store's own 4,096-cycle watchdog answering the same error. The restore aborts with cause 6. That is never counted as a refused value. A successful fetch whose value fails the rule is still a per-record refusal (V2b).
- **The image walk is part of the transaction.** If the store holds no validated image after a LOCATE of ENTITY 0, the restore ends CLOSED with cause 7, before any record is read. `desc_img_valid`, today the debug tap `dbg_img_valid_o`, becomes a product face (T1).
- **A subordinate's shorter timeout is a fault, never progress.** `RS_TMO_CYC_P` is sized above the store's whole walk, so the writer's deadline does not fire during a fetch that is still moving.
- **S2 isolates late descriptor beats.**
  - The guard holds the store's next request while an accepted burst still owes its last beat or error beat, and publishes `desc_debt`.
  - The roll-back holds the owners in reset for at least two cycles and for as long as `desc_debt` is 1, bounded by the deadline. A late beat therefore never enters the re-walk.
  - The guard takes the hard reset only.
  - The same guard closes an exposure that already exists in service (V23).
- **State-bus apply** (DERIVED from the pinned RTL). `KL_aecp_dyn_state` has no error output and takes a write in the cycle it is presented. The descriptor store's one writable region, the names, answers no error. So a write can only stall, and the deadline watches the stall (cause 3).
- **Recorded, not changed.** The pinned store does not re-arm its watchdog after a fetch's response timed out, so its next fetch errs at once (page 15 item 14, T9). That failure is honest.

Evidence at 1x1 and 8x8. V20, V21 and V22 are R217's own stimuli.

*Errors after an application:*
- V20b: one error beat on the first fetch after an application, the clock-source rule's. The case reads "the descriptor memory answered an error beat at 3389, the writer aborted at 3393" and "1 records applied before the fault, roll-back at 3394, abort cause 6". Refused 0; rolled back.
- V20c: the refused output map's revert fetch errs once: "roll-back at 3740, abort cause 6".
- V20d: the final re-judge's revert fetch errs once: "roll-back at 2659, abort cause 6".
- V20 (R217 descriptor-error): the memory fails from the first application on. Abort cause 6; the roll-back cannot prove the image, so the restore ends CLOSED.

*Delays around the store's watchdog and the deadline:*
- V21 (R217 descriptor-timeout, 5,000 cycles): "request accepted at 3386, the store's error answer aborted the restore at 7486 (4100 cycles), the late burst came at 8387, the owners left reset at 8398". Rolled back to defaults; every name is the image's.
- V21b (16,000 cycles): "the late burst came at 19387, the owners left reset at 19398".
- V21c (30,000 cycles, past the deadline): "aborted at 7486, CLOSED at 27488 (20002 cycles), the late burst came at 33387".
- V21d (4,000 cycles, inside the store's own bound): "its first beat at 7387 (4001 cycles ...)", then COMPLETE.

*Image and roll-back failures:*
- V22 (R217 descriptor-initial-error): "abort cause 7, applied 0, refused 0, image validated 0, closed 1".
- V22b: the same, on a slot of records that no rule fetch touches.
- V17: the roll-back walk fails; CLOSED.

*In service, and the refusal control:*
- V23: a locate answered by the store's watchdog, a second locate at once, and a third while the late burst is still owed. The third reads "third locate err 0 type 0x5", never the late burst's bytes. Afterwards: "a locate answered err 0, descriptor_type 0x5".
- V2b (control): a clock-source index past the count, with its rule fetched successfully: "clock source row valid 0, refused 1"; "D3 fail 0, rolled back 0, cause 0".

*What each case grades:*
- Cases that end in DEFAULTS check that every row, name and map is at its default, and check the cause. They also check entity_enabled_after_terminal and no_restore_write_after_terminal, that a controller's GET is served, and that a later SET persists.
- Cases that end CLOSED check the cause, and that the entity stays dark: `own` 1, never enabled, a GET unanswered.

*Mutants, each killed:*
- DF01_desc_error_is_a_refusal (round two's rule), by V20b.
- DF02_map_revert_read_error_ignored, by V20c: "abort cause 4 (want (6,))".
- DF03_final_revert_read_error_ignored, by V20d.
- IMG01_unproven_image_continues, by V22b.
- DG01_guard_admits_a_request_while_owed, by V23: "third locate err 0 type 0x6", another descriptor's bytes.
- DG02_rollback_ignores_mem_debt, by V21b.

*Your probes, rerun:*
- descriptor-error: "closed 1, done 0, enabled 0, cause 6".
- descriptor-timeout: "every row at its default True, done 1 fail 1, rolled back 1, cause 6, enabled 1".
- descriptor-initial-error: "closed 1, done 0, enabled 0, cause 7, image validated 0, applied 0 refused 0".

The timeout probe uses the harness knob `desc_delay_after_apply=5000` in place of your bridge seam, which this revision moved.

*Cost.* The guard is 5 LUT and 1 FF.

## R217 R2-F3: the stages still permit an unbounded binding-walk hold, and T8 promises incompatible recovery

MAJOR; Conformance, RTL, Robustness, Tests, Docs.

Change (page 3 rules 8 and 11, 5.1, 6.3, 6.4, 8.1, 8.8, 10, 13, 15 items 4 and 13; tickets T1, T4, T8):
- **S3 bounds the binding walk.** The binding manager's read phase (H_RS_REQ, H_RS_STREAM) is bounded by `RS_TMO_CYC_P` cycles without progress.
  - On expiry the walk fails whole: done, fail, cause 3, NOTHING preloaded, and every uncaptured sink at its default.
  - `nvm_abort_o` hands the issued read to the arbiter's drain.
  - The D3 walk then starts, meets the drained port, and ends at its own deadline in DEFAULTS.
  - AECP is served on defaults with restore fail set. This is how FASTCONNECT 9.3's continued AECP service when persistence wedges is met; no availability waiver is used.
- **Late binding responses are contained before commands are released.** The drain swallows them, and a failed walk preloads nothing, so no binding reaches the listener after the enable.
- **Either manager's abandoned read is drained.** The port stays QUARANTINED until its device ends that read, for ever if it never does. Nothing releases it on a timer. Page section 8.8 states command availability and persistence availability as two separate contracts.
- **T8 is rewritten** as "Prerequisites of D3 stage 1: the port's terminal cause and a bounded binding walk". It is a new processor issue that references issues 15 and 20, closes and amends neither, and claims no port reuse. The file keeps its name so earlier citations resolve.

Evidence at 1x1:
- W13, the binding walk's first read silent for ever:
  - "silence from 64, the binding walk's terminal at 20062"; "binding fail 1 cause 3, preloads []";
  - "D3 terminal at 40721", "entity enabled at 40733";
  - the GET "answered 0 valid 0", so AECP is served on defaults;
  - the later SET reads "pend 1, port busy 1": the port is quarantined, and the change stays pending, never durable.
- W13b, released when the binding deadline was 40 cycles away: "the binding deadline count reached 19960 of 20000, binding cause 0"; "preloads [(20130, 0)]"; both walks COMPLETE.
- W13c, released 5 cycles after the binding manager abandoned it: "abandoned at 20061, the response came at 20066"; "binding fail 1 cause 3"; "preloads []". The drain ends and the later SET persists.
- W15, released at 2,900,000 cycles, after the enable: "the entity enabled at 40733, the response came at 2900064"; "preloads []". The later SET persists once the drain ends.
- W16: a DEVICE error on the binding header fails the binding walk with cause 2.
- W14: an enable requested from reset: "the enable requested at 9, restore done at 7605".
- Every case that reaches done passes entity_enabled_after_terminal and no_restore_write_after_terminal.
- Mutants, each killed:
  - B01_binding_walk_no_deadline, by W13: "the binding walk's terminal at 0 (bound 20000 + 100)".
  - B03_binding_abort_not_drained, by W13c: "latest 0076adf1, newest verified slot 0016e360".
  - G05_enable_not_released_by_restore, by W14.

Note that W13, W14 and W15 are REDEFINED from revision b. There they were binding-walk silence without a deadline, and a release after, then before, the firmware's wait.

## R218 F6: the output-format oracle admits synthetic behavior without identifying that boundary

MINOR; Tests, Docs.

Change (page 8.2, 8.3, 8.4 "Which judge", 14; the labels in the results):
- The judge now has two modes:
  - SHIPPING transcribes `milan_datapath.sv`'s `sfv_supported_w`: an output admits only its declared format; an input admits the 1/2/4/6/8 family on the declared base.
  - SYNTHETIC, used everywhere else, also admits narrower output formats.
- `results.txt` labels every case whose stimulus narrows an output: "LABEL SYNTHETIC output-format judge (a narrowed output format, product-illegal)". That covers 50 cases, including every case that boots from V1a's slots. The three V1s cases sit under "LABEL SHIPPING".
- Page section 8.4 names the ordering claims that rest on the synthetic judge (V6a, V6b, V8, V9, V20c, V20d) and says they are not product-legal SET evidence. No product support is expanded.
- The page's V1a claim is corrected: V1a narrows output 0 from eight channels to four, which is not product-legal. Its input narrowing is product-legal.

Evidence at 1x1 and 8x8, under the SHIPPING judge:
- V1s_a: output 0 SET to a narrower format is refused and SET to its declared format is accepted. The declared-format and input-format records reach a slot.
- V1s_b: the declared format is restored WITH its valid flag: "GET output 0 format 0x205022002006000 valid 1". The declared value equals the generated default, so only the valid flag tells a replay from no replay.
- V1s_c: a narrower saved output is refused on replay: "output 0 format valid 0 (value 0), refused 1, D3 fail 0".
- Both format directions carry two killers:
  - RPL_fmto and RPL_fmti must fail V1s_b's check as well as V1b's.
  - TRG_fmto and TRG_fmti must fail V1s_a's check as well as V1a's.

  A mutant now counts as killed only when EVERY named check fails, and the verdict line prints each check's own state. All four are killed by both checks.
- A new process control, partial_kill_is_survival, requires the runner to report a mutant killed by only one of its two checks as SURVIVED, exit 1.

## R218 F7: permanent-silence recovery contradicts mandatory quarantine

MINOR; Docs.

Change (T8; page 6.4, 8.8, 15 item 4):
- T8 no longer claims that a permanently silent device stops holding the port. A device that never ends the abandoned read keeps the port QUARANTINED for ever.
- Reuse would need a cancellation or device-reset acknowledgement. That is processor issue 15's open recovery contract, which T8 neither supplies nor claims.
- Finite late completion and permanent silence are separate cases on both walks.

Evidence:
- Permanent silence: W1, W4 and W7 (D3) and W13 (binding). Each reaches its terminal, commands are served, and the later SET reads "pend 1, port busy 1".
- Finite late completion: W3, W6, W11 and W12 (D3) and W13c and W15 (binding). Each response is drained and the later SET persists.

## Round-one findings: what revision c keeps

The table gives each round-one finding with its original severity and lenses, the round-two disposition in summary, and what this revision keeps. Nothing here is claimed cleared.

| Finding | Severity and lenses | Round-two disposition | Revision c |
|---|---|---|---|
| R217 F1, R218 F1: two passes do not make restore all-or-nothing | MAJOR; Conformance, RTL, Robustness, Tests, Docs (both) | payload triggers corrected; OPEN under R217 R2-F1 and R2-F2 and under R218 F1 | answered above; V11b, V12 to V16, R01 to R04 and M16 kept |
| R217 F2, R218 F2: the firmware timeout enables the entity without containing the restore | MAJOR; Conformance, RTL, Robustness, Tests, Docs (both) | early enable corrected; R217: availability OPEN under R2-F2 and R2-F3 | answered above; W1 to W12, K19, W01, D01, R05 and O01 kept; G05 now killed by W14 |
| R217 F3: invalid map entries can bypass the value refusal | MAJOR; Conformance, RTL, Robustness, Tests, Docs | R217: RESOLVED for this proposal | unchanged: V3a to V3g, P01, P02 |
| R217 F4: permanent pending is still an accepted Stage 3 outcome | MAJOR; Conformance, RTL, Robustness, Docs | R217: prerequisite defect RESOLVED; #501 and #502 OPEN | unchanged: stage 3 blocked on #501, every shippable stage after #502; K16 is containment only |
| R217 F5: the evidence runner does not fail its process verdict | MINOR; Tests, Docs | R217: RESOLVED | kept; eight process controls now, exits 1, 1, 1, 1, 1, 2, 1, 2 |
| R218 F3: the runner accepts surviving mutants and failed scenarios | MAJOR; Tests, Docs | R218: corrected | kept and strengthened: a mutant needs EVERY named check to fail, each in a completed run |
| R218 F4: configuration replay can be deleted without invalidating the evidence | MAJOR; Conformance, Tests, Docs | R218: original missing checks corrected; F6 qualifies the output format | kept: RPL_cfg by its valid flag, nine TRG and nine RPL mutants, the synthetic 1x1r2 rate; the output format is now also graded by V1s |
| R218 F5: staging permits open capacity/status defects | MAJOR; Conformance, Robustness, Tests, Docs | R218: release-contract defect corrected; #501 and #502 OPEN | unchanged |

Also unchanged:
- the explicit live-write amendment request (page 15 item 1), which is not adopted until the contract acceptance records it;
- O1, limited to the one sequential control-face master, with O3 stated separately (page 4, 8.1, 13);
- the inherited snapshot obligations O1 to O4, which are not re-proved here.

## Not claimed

- No product RTL or firmware is changed. S1 to S3 are proposals with prototypes. Their tickets, T8 and T9, are drafts for the manager to file.
- Processor issue 15 is neither closed nor amended. T8 references issue 20; this page does not close it.
- Model time is not board time. The 20 ms deadline is a proposal (page 15 item 8).
- The model's omissions are listed in page section 14 and in the dependency audit at the end of page section 8.8.
