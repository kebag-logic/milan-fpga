[R311] NEGATIVE - exact head 29840136bb2d21bc0fbe92c7c533368f40837ff6

# R311-1 external independent review: processor issue #113 / PR #115

- **Repository:** Mister-M-alt/protocol-processor-control-plane-avb-milan
- **Exact head:** `29840136bb2d21bc0fbe92c7c533368f40837ff6`, tree `03bdccaf528aa94098544cf04f5598292fe855c8`, one commit on source base `a8f8ce810ddba1816cd129d0afcd71e6e02ade1b`. The diff touches 15 files, +132/-12.
- **Reviewer:** [R311], external role. I worked in a cleared context from an isolated detached clone. There were no source edits, commits, pushes or GitHub writes.
- **Scope authorities:**
  - the issue #113 body;
  - the manager decision on issue #113 (comment 5821292534): implement; F06.13 marks the latency as a Table 5.22 trigger;
  - the PR #115 body;
  - Milan v1.2 consolidated (Final, 2023-11-30) §5.4.5.2 with Table 5.22;
  - the repository's own contracts: 06 F06.13 and §7, 10 §6.4, the 02 event catalog, and 00 REQ-NOT-003.

## Verdict summary

The RTL change is correct, minimal and conforms to the clause:

- A committed change of a sink's latched accumulated latency raises exactly one unsolicited GET_STREAM_INFO for that Stream Input. It uses the existing per-descriptor pending bit.
- A refresh that leaves the latency unchanged raises none.
- No other sink is notified.
- When the same attribute write also changes registration or failure state, the change coalesces into that write's single push.
- The strobe has one consumer, the per-sink notify OR. Nothing reaches the applicant or the event router.
- The top-level port list is identical to the base.

One MINOR finding is open (F1). The committed test documentation claims that the new values "exercise the full comparison width". That is false. A comparator truncated to 8 or 16 bits, to the high half, or with bit 31 dropped still passes all 614 GI checks at this head. F1 leaves the Tests and Docs lenses unclean, so the verdict is NEGATIVE.

## Independence disclosure

- **The other reviewer's summary.** While saving the PR comment thread to a scratch file early in the review, I printed one slice too many. That showed me the first about 24 lines of the other reviewer's public report (its verdict summary, which names this comparator-width issue). I stopped reading at that point.
- **My F1 evidence is my own.** Before running anything, I derived the gap from the test's value sequence (XOR analysis below). My own probes then confirmed it. Those probes include truncations the other report does not list: [7:0] and [31:16].
- **When the verdict was fixed.** My verdict and ledger were settled, and my first probe batch, the suites and the static checks were all complete, before I read the rest of that report. The first write of that draft failed on a file-state precondition, and I read the prior report immediately afterwards. The verdict and ledger below are unchanged from that draft.
- **Material that appears after reading.** The section "Prior public review findings" was written after reading. So were two additions: the extra scope-limit wording about the manager bank, and the single-bit feasibility probe results (`t-*` receipts), which I had not yet run.

## Reconstruction

1. **Repository conventions.**
   - The tree has no AGENTS.md or CONTRIBUTING.md. I checked the repository root and every subdirectory.
   - I followed README.md and docs/README.md instead. They require single-source docs and one self-checking suite per module, and `make check` must pass before a commit.
2. **Frozen acceptance: the issue plus comment 5821292534.**
   - **Trigger:** a change of the latched `acc_latency[sink]`, not the refresh itself.
   - **Mechanism:** reuse the per-descriptor dirty and notify path, with no new rate limit.
   - **Response-level tests required:**
     - a latency-only refresh gives exactly one unsolicited response carrying the new value;
     - an unchanged refresh gives none;
     - another sink is not notified;
     - a trigger-removal mutant fails the first test.
   - **Docs:** F06.13, the §06 live-event list, and the compliance row if its status changes.
   - **Also required:** the default-shape area delta from the OOC recipe, and the parent consumer check.
3. **Clause, verified directly.**
   - **Source:** Milan v1.2 consolidated PDF. Its sha256 is `6bb902be1c1de8c44f4c4c583a645b0b37e0b2dac27870486ce229e68ce3bba8`, identical to the author's recorded provenance.
   - **§5.4.5.2** (printed p. 62): "Finally, the unsolicited notifications listed in Table 5.22 shall be sent asynchronously of any command when the state of the entity changes".
   - **Table 5.22 GET_STREAM_INFO row** (printed pp. 62-63): "Sent when one of these pieces of information changes: … • MSRP accumulated latency (Stream Input only) …".
   - **Rate limit:** only the GET_COUNTERS row carries a one-per-descriptor-per-second restriction. Adding no rate limit is therefore correct.
4. **Diff and history.** `git diff a8f8ce81..29840136` contains:
   - RTL in `KL_srp_listener_fsm.sv`, `KL_srp_top.sv` and `protocol_processor_top.sv`;
   - testbench wiring in `pp_top_wrap.sv`, `sim_main.cpp`, and the `srp_top` and `srp_stream_fsms` wrappers;
   - the GI test in `gsi_internal.hpp` and the mutant list in `gsi_mutants.py`;
   - docs in 00, 02, 06, 10, `syn/ooc/README.md` and `tb/pp_top/README.md`.

   The history is linear on top of the #114 merge.

## Lens results

### Conformance: CLEAN

- **Trigger condition.** The trigger is `lat_r[s] != evt_acc_latency_i` on a registering Talker Advertise/Failed write for an armed sink (`hdl/srp/KL_srp_listener_fsm.sv:738`). This is the Table 5.22 condition "the information changes" for a Stream Input. A same-value JoinIn refresh is silent.
- **No new rate limit**, consistent with Table 5.22.
- **Pushed value.** The GI test checks that the pushed value equals the solicited read, byte-exact, in `latency_refresh()` at `gsi_internal.hpp:271-297`. I re-ran it: 614/614.
- **Reported field.** msrp_accumulated_latency is reported from `acc_latency[sink]` plus the constant ingress delay (F06.13). The notification therefore follows exactly the changes of the reported field.
- **Validity.** MSRP_ACC_LAT_VALID is tied to "registering a matching talker attribute" (06 F06.13 flags paragraph). The pre-existing A15/A8 clear of the latch changes no valid reported value, and the ACMP status notification already reports those transitions.

### RTL: CLEAN

**Pulse generation.** In `KL_srp_listener_fsm.sv:728-744`, the comparison sits inside the same registering branch that re-latches `lat_r[s]`, so pulse and latch update share one edge.
- The pulse defaults to 0 every cycle (`:711`) and at reset (`:701`), so it is a one-cycle strobe.
- Each sink compares its own previous latch. Two sinks bound to the same stream therefore each notify only if their own latch changed, which matches 10 §6.4.
- `assign ctl_ready_o = !evt_valid_i` (`:494`) and `assign ctl_acc_w = ctl_valid_i && ctl_ready_o`. An A15/A8 control write therefore cannot coincide with a registering event, and the later clear block cannot race the pulse.

**Coalescing.** `protocol_processor_top.sv:3141-3146` ORs the pulse into `ntfy_stri_in_w[k]` with the same-index registration, unregistration and fail-change strobes. All of them are registered in the same `reg_plane` block on the same write.
- `KL_aecp_notify.sv:758` sets one pending bit per sink, and `:987` clears it at emission pick.
- The engine rebuilds each response from current state after the pick (notify header, lines 109-121).
- Result: one event per write and no stale value. My delayed-strobe probe confirms that the tests observe this (see Tests).

**Fan-out** (`receipts/strobe-fanout.txt`).
- `evt_tk_latency_chg_o` is only declared, reset, defaulted and assigned inside the listener FSM; nothing there reads it.
- `KL_srp_top` only passes it to its port.
- The top consumes it only in the `stri_events` OR, which feeds only `KL_aecp_notify.ev_stri_in_i`.
- The two testbench wrappers leave it unconnected.

So it cannot reach the applicant, the event router or the ACMP listener.

**Ports.** The port header of `protocol_processor_top` is identical at base and head: both have sha256 `17b157e2…6bce6`, 205 declarations (`receipts/ports-top-*.txt`). The only port change is the new internal `KL_srp_top` output (`receipts/ports-srp_top-*.txt`). Every instantiation of the two changed modules is updated: the top and the two wrappers.

**Lint.** Scoped lint with the pinned 5.050 simulator uses the repository lint flags on `KL_srp_listener_fsm`, `KL_srp_top` and `protocol_processor_top`. All three return rc 0 with zero warnings (`receipts/lint-changed-modules.txt`).

**Area** (checked against the published OOC reports, `author/area-{base,head}/util*.rpt` and `timing.rpt`):

| Measure | Base | Head | Delta |
|---|---:|---:|---:|
| Slice LUTs | 28,649 | 28,643 | -6 |
| Slice Registers | 31,095 | 31,123 | +28 |
| RAMB36 / RAMB18 / DSP | 23 / 2 / 4 | 23 / 2 / 4 | 0 |
| `u_srp/u_listener` (`KL_srp_listener_fsm`) LUTs | 1,795 | 1,868 | +73 |
| `u_srp/u_listener` (`KL_srp_listener_fsm`) FFs | 2,328 | 2,336 | +8 |
| WNS | -10.089 ns | -8.192 ns | |

- Every figure in `syn/ooc/README.md`, the PR body and AREA.md matches the reports exactly.
- The reports name part `xc7a100tfgg484-2` and design `protocol_processor_top`.
- The OOC recipe is unchanged between base and head.
- All 45 HDL hashes in the author provenance equal the exact-head blobs (`receipts/provenance-vs-head.txt`).
- +8 FFs is the eight pulse bits. The README correctly declines to claim the -6 total LUTs as a saving.

### Robustness: CLEAN

- **Reset and defaults:** the strobe is a registered one-cycle pulse with a synchronous reset.
- **Adversarial input:** a peer that varies latency on every refresh produces at most one pending bit per sink. That bit coalesces until the pick, so no queue or counter grows unbounded, and each emitted response carries current state.
- **Same-cycle interplay:**
  - A registering event and an A15/A8 control write are mutually exclusive by the `ctl_ready_o` handshake.
  - An event that lands on the pick cycle re-pends and is reported by a later coherent response. This is the documented F06.13 coherence bound.
- **Unregistration:** rLv and leavetimer paths keep the latch as before. A later re-registration raises the registration strobe, so no change is lost.
- **Probe results** (`receipts/probes/`):

  | Probe | Change | Outcome |
  |---|---|---|
  | `r-delayed-strobe` | latency strobe delayed by 4,096 cycles, so it is no longer coalesced | KILLED, 22 failures. The coalescing property is really observed by the existing sequence. |
  | `r-all-sinks` | pulse broadcast to every sink | KILLED, 43 failures |
  | `r-advertise-only` | Failed sink never notifies | KILLED by `GI LATENCY-CHANGE … sink 1` |
  | `r-always-pulse` | any registering write notifies | KILLED, including `GI LATENCY-SAME` |

### Tests: UNCLEAN (F1)

**What is real and adequate.** The GI latency section (`gsi_internal.hpp:268-311`, called at `:384`):
- sends real Talker JoinIn MRPDUs through the MAC/SRP path to two settled sinks, one Advertise and one Failed;
- has the harness integrator fold the published `srp_acc_latency_o` into selector 3 with zero ingress delay (`sim_main.cpp:1537-1538`);
- grades complete 94-byte responses byte-exact, including sequence IDs;
- checks exact unsolicited counts, silence on an unchanged refresh, isolation of the other sink, solicited agreement, and an empty queue afterwards;
- uses values with bit 31 set, zero and all ones.

**My reruns** (pinned 5.050 simulator, exact-head `git archive`, at most 8 parallel jobs):

| Suite | Result |
|---|---|
| GI focused | 614 checks, 0 failures |
| `tb/pp_top` full | 2,074/2,074 (matches the PR) |
| `tb/srp_top` | 1,531/1,531 |
| `tb/srp_stream_fsms` | 1,087/1,087 |

**Retained mutant.** I reproduced the author's retained mutant independently as `r-trigger-removed`. It is KILLED by the named check `GI LATENCY-CHANGE: exactly one unsolicited response` ("got 0" for sinks 0, 1, 0 and 1), with 594 checks and 8 failures. That is identical to the author's published `latency-trigger-removed-run.log`.

**Comparator-width probes survive: F1.**

| Probe | Comparator used | GI result |
|---|---|---|
| `r-cmp-low8` | bits [7:0] | 614 checks, 0 failures |
| `r-cmp-low16` | bits [15:0] | 614 checks, 0 failures |
| `r-cmp-high16` | bits [31:16] | 614 checks, 0 failures |
| `r-cmp-no-bit31` | bits [30:0] | 614 checks, 0 failures |

**Wiring probes survive: suggestion SA.** Two probes route the latency strobe to places the design forbids:
- `r-strobe-to-applicant` feeds it into the registrar indication, so it re-declares a Listener;
- `r-strobe-to-acmp` feeds it into `evt_tk_registered_o`.

Both pass the head's suite unchanged. The design keeps these paths closed, as confirmed by the fan-out above, but the latency section has no wire-level guard. The FailureInformation section does have one (`GI FAILED-REFRESH wire …` plus the retained mutant `failure-change-redeclares`).

### Docs: UNCLEAN (F1)

**Accurate and complete for the required scope:**
- **F06.13** msrp_accumulated_latency row (`docs/architecture/06_aecp_engine.md:303`), naming the committed latch change, the silent unchanged refresh and the clause.
- **§7 live-event list** (`06_aecp_engine.md:735-748`), with the coalescing statement and no GET_COUNTERS-style limit.
- **10 §6.4 latch contract** (`docs/architecture/10_srp_engine.md:391-398`) plus two stateDiagram self-edges (`:379-380`) and the corrected FailureInformation sentence (`:414-415`).
- **02 event catalog** row `TK_LATENCY_CHANGE{sink}` (`docs/architecture/02_interfaces.md:400`), marked as not routed.
- **REQ-NOT-003** evidence text (`docs/00_MILAN_COMPLIANCE_REVIEW.md:377`). The status stays P, which is correct because the row still covers other partial triggers.
- **`syn/ooc/README.md` area section**, which matches the reports.
- **`tb/pp_top/README.md` mutation-table row** for the latency trigger, which matches the retained mutant.

The concept document's historical marker is unchanged, as stated.

**Local doc gates at the exact head** (`receipts/doc-gates.txt`), all rc 0:
- links: 856 checked;
- matrix: 115 REQ rows, 17 GAP;
- modmatrix: 92 rows, 0 untested;
- diagram lint: 41 mermaid and 18 wavedrom blocks;
- wavedrom render check: 18 blocks.

The drawio staleness check is not applicable: no drawio source changed.

The false coverage sentence at `tb/pp_top/README.md:65-66` is F1.

## Findings

### R311-1-F1: MINOR (Tests, Docs). The latency comparator's width is not exercised, and the committed test documentation says it is

- **Where:**
  - the value sequence `latency_changes()` at `tb/pp_top/gsi_internal.hpp:299-311`;
  - the claim at `tb/pp_top/README.md:65-66`: "Distinct values, bit 31, zero and all ones exercise the full comparison width and sink selection."
- **Authority and evidence:**
  - The four changed-latency transitions the head tests have these XORs:

    | Transition | XOR |
    |---|---|
    | 0x00012345→0x81234567 | 0x81226622 |
    | 0x00012345→0xABCDEF01 | 0xABCCCC44 |
    | 0x81234567→0x00000000 | 0x81234567 |
    | 0xABCDEF01→0xFFFFFFFF | 0x543210FE |

  - Every transition differs in the low byte and in the high half at once, and three of them also flip bit 31. So no single bit is ever the only difference, and bit 31 is never isolated.
  - The comparator at `hdl/srp/KL_srp_listener_fsm.sv:738` is the new logic under test. Probes `r-cmp-low8`, `r-cmp-low16`, `r-cmp-high16` and `r-cmp-no-bit31` narrow it, and each still passes all 614 GI checks (`receipts/probes/results-mutants.json`).
  - Table 5.22 requires a notification for any change of the reported latency.
- **Impact:**
  - The acceptance test does not protect the property its documentation claims.
  - A regression that narrows the comparison would miss, for example, every latency step that is a multiple of 65,536 ns. That would ship silently, and a registered controller would keep the old latency. This is the exact symptom issue #113 fixes.
  - The committed README overstates the suite's coverage to future maintainers.
- **Required outcome:** do one of the following.
  - **(a)** Add latency-only refreshes whose old and new values differ in a single high bit (bit 31) and in a single low bit (bit 0). Each must require exactly one unsolicited response. Preferably also retain a comparator-narrowing mutant in `gsi_mutants.py` with a named failing check.
  - **(b)** Reword `tb/pp_top/README.md:65-66`, and the PR text if it repeats the claim, so it claims only what is exercised.

  (a) is preferred because it closes the gap rather than documenting it.
- **Verification.** Feasibility is already shown by the `t-*` probes (`receipts/probes/results-test-feasibility.json`). They append two refreshes to the head's own sequence, 0xFFFFFFFF→0x7FFFFFFF (bit 31 only) and 0x7FFFFFFF→0x7FFFFFFE (bit 0 only), with these results:
  - **Unmodified RTL** (`t-golden`): 656 checks, 0 failures.
  - **Narrowed comparators** (`t-cmp-low8`, `t-cmp-low16`, `t-cmp-high16`, `t-cmp-no-bit31`): all four KILLED by `GI LATENCY-CHANGE: exactly one unsolicited response for sink 1, got 0`.

  The next round should show a named-check kill for at least the [15:0] and [30:0] narrowings, or show the reworded text.

### R311-1-SA: SUGGESTION (Tests). Wire-level guard for the latency strobe

This follows the FailureInformation precedent (`GI FAILED-REFRESH wire …` plus the retained mutant `failure-change-redeclares`). Add a `listener_news()` == 0 check around one latency-only refresh, and retain a mutant that feeds the latency difference into `ind_reg_w`. The `r-strobe-to-applicant` probe currently survives, which shows the head suite does not guard the "never re-declares" contract of 10 §6.4 for this strobe. The RTL is correct today; this suggestion does not affect the verdict.

## Prior public review findings: resolved or retained at this head

These were read after my own pass; see the Independence disclosure. The only prior public review on PR #115 is R310-1 (NEGATIVE, comment 5822538155).

| Prior item | Disposition at 29840136 | Basis |
|---|---|---|
| R310 F1 MINOR (Tests, Docs): comparator width not covered; the README claims full width | **RETAINED** as R311-1-F1 | Independently reproduced: [15:0] and [30:0] survive in my probes too, and so do [7:0] and [31:16]. The single-bit additions kill them. The head is unchanged, so the finding stays open. |
| R310 S1 SUGGESTION (Docs): integrator note on the live selector-3 derivation | RETAINED as suggestion, non-blocking | F06.13 already says the integrator answers its words live ("the same way"), so the contract holds. An explicit tie to the new trigger would help integrators. |
| R310 S2 SUGGESTION (Docs): say that the A15/A8 latch clear raises no latency strobe | RETAINED as suggestion, non-blocking | Consistent with my RTL reading: `ctl_acc_w` clears `lat_r` with no strobe, and MSRP_ACC_LAT_VALID is 0 there. |
| R310 S3 SUGGESTION (RTL/area): optional shared comparator | RETAINED as optional, non-blocking | The current per-sink comparator is correct and small (+73 LUTs). Sharing is an area option, not a defect. |

## Reviewer ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Milan v1.2 §5.4.5.2 and Table 5.22 (printed pp. 62-63, PDF hash verified); issue #113 plus decision 5821292534; F06.13 and §7; value path via gather selector 3; the GI solicited-vs-unsolicited agreement | R311-1 | 29840136bb2d21bc0fbe92c7c533368f40837ff6 |
| RTL | CLEAN | `KL_srp_listener_fsm.sv` (hit map, indications, `reg_plane`, ctl handshake); `KL_srp_top.sv`; `protocol_processor_top.sv` (`stri_events`, gsi owner read, port header); `KL_aecp_notify.sv` (intake, pick clear); fan-out receipt; scoped lint; OOC util, util_hier and timing reports plus provenance | R311-1 | 29840136bb2d21bc0fbe92c7c533368f40837ff6 |
| Robustness | CLEAN | Reset and pulse defaults; ctl/event exclusivity; pick-cycle re-pend; unregistration latch retention; adversarial refresh coalescing; probes `r-delayed-strobe`, `r-all-sinks`, `r-advertise-only`, `r-always-pulse` | R311-1 | 29840136bb2d21bc0fbe92c7c533368f40837ff6 |
| Tests | UNCLEAN (F1) | `gsi_internal.hpp`, `sim_main.cpp` fold, `pp_top_wrap.sv`, `gsi_mutants.py`, author mutant logs; reruns: GI 614, pp_top 2,074, srp_top 1,531, srp_stream_fsms 1,087; 11 reviewer mutation probes plus 5 test-feasibility probes | R311-1 | 29840136bb2d21bc0fbe92c7c533368f40837ff6 |
| Docs | UNCLEAN (F1) | 00 REQ-NOT-003; 02 catalog; 06 F06.13 and §7; 10 §6.4 and diagram; `syn/ooc/README.md`; `tb/pp_top/README.md`; integrator guide GSI paragraphs; local doc gates; PR body claims | R311-1 | 29840136bb2d21bc0fbe92c7c533368f40837ff6 |

## Public evidence consulted

**Author packet.** `kebag-logic/milan-fpga@b0a26b65daa9c781ddf8777259f27b242f02b4a8/review-evidence/pp113-r1/`, fetched at that exact commit.
- All 104 files match the published sha256 in `MANIFEST.json`. 54 are path-redacted, which explains why the author's own `MANIFEST.sha256` lists pre-redaction hashes. No file is unlisted.
- The tree contains only the author subtree. I found no separate manager-bank receipts there, and no manager evidence comment on the issue or the PR other than the decision and the review-start notices. The manager bank result at this head is therefore taken from the review brief. I did not verify it.

**Parent consumer** (author receipts): 7/7 commands return rc 0 at both pins, on parent dev `573f0052`.
- **Control:** processor `a8f8ce81`, parent `9947af73`.
- **Candidate:** processor `29840136`, parent `dd8b228b`.

The commands were C++ idiom, Python idiom, front-end ratchet, RTL source lists, processor source check with self-test, builder, and consumer simulation.
- The consumer passes 371 checks with 0 failures at both pins, and the same four front-end findings appear at both.
- Both builder logs say `1 GATE ARM(S) DID NOT RUN` (gate 11, resource calibration; its placement report is absent) and `ALL GATES PASS EXCEPT 1 NOT RUN`.

I did not rerun the parent check, as the rules require.

**Hosted checks at the exact head** (`receipts/hosted-check-runs.txt`). There are two `hdl` workflow runs, push 36055947134 and pull_request 36055952583. Each executed docs-gates, suites and portability, and all 6 of 6 jobs completed with success. None was skipped. The legacy commit-status API shows `pending` with 0 statuses, meaning no status contexts are posted. The manager owns hosted/act acceptance.

## Real limits

- I ran focused suites, scoped lint, doc gates and disposable probes only. I did not run the full processor, parent, gPTP, Yosys or builder banks. I also did not run OOC synthesis, Docker/act, host act_ci or hardware.
- The area figures are the author's published reports, cross-checked to the head blobs through provenance. I did not resynthesize.
- Physical calibration was NOT RUN. Field skips are not hardware proof. There is no routed-timing claim, and both OOC builds have negative slack.
- My probes ran in `git archive` exports of the exact head. The only build-flag change was the compile parallelism (`-j 0` → `-j 4` or `-j 8`), made to respect the 8-job budget. The reviewer test additions are probes only, not proposed patches.
- The GI image carries two Stream Input descriptors. Isolation is checked directly between sinks 0 and 1, and for all other descriptors through the empty-queue check and the `r-all-sinks` kill.
- See the Independence disclosure above.

## Pending manager duties

- Disposition of R311-1-F1 (and R310 F1) in a new round.
- The final current-dev candidate build and banks at the merge turn: source base `a8f8ce810ddba1816cd129d0afcd71e6e02ade1b`, live dev `ffcbd33de70278ae34b533dcbadde0b36c8cba13`. The author's parent comparison used dev `573f0052`, not live dev.
- The manager-bank parent consumer 7/7 with the `a8f8ce81` control.
- Hosted/act acceptance.
- The parent re-pin as a separate lane after merge.

## Reproduction and receipts

- `probe_mutants.py --repo <clone> --rev 29840136bb2d21bc0fbe92c7c533368f40837ff6 --verilator <pinned 5.050> --scratch <dir> --out <dir> --workers 2 --jobs 4 [--only names]`
  - It exports `hdl`, `tb/common` and `tb/pp_top` with `git archive`, then applies each exact-count edit.
  - It builds with `make gsi-build` and runs `--gsi-internal-only`.
  - Variants: `golden`, eleven `r-*` mutants and five `t-*` feasibility variants.
  - Results: `receipts/probes/results-mutants.json` and `results-test-feasibility.json`, plus per-variant build and run logs. The golden result is in `golden-run.log`.
- `port_list.py`: `git show <rev>:hdl/top/protocol_processor_top.sv | port_list.py protocol_processor_top` gives the normalised port declarations (`receipts/ports-*.txt`).
- **Suites:** `receipts/suites/{pp_top,srp_top,srp_stream_fsms}.log` (the default `make` target in each bench, from an exact-head export).
- **Other receipts:**
  - `receipts/lint-changed-modules.txt`
  - `receipts/doc-gates.txt`
  - `receipts/strobe-fanout.txt`
  - `receipts/provenance-vs-head.txt`
  - `receipts/hosted-check-runs.txt`
- **Tool identity** (`receipts/tool-identity.txt`): the simulator reports 5.050 rev v5.050. The wrapper sha256 is `905795b9…e92f`, and the wrapped binary sha256 is `44898b22…bfdd`.
- **Clone integrity after all probes** (`receipts/clone-restore-check.txt`):
  - HEAD `29840136…` and tree `03bdccaf…` are exact.
  - `git status --porcelain --ignored` is empty.
  - There is no index-vs-HEAD or worktree-vs-index difference, and a freshly read HEAD index also shows no worktree difference.
  - Modes: 236 × 100644 and 10 × 100755.
  - The repository has no submodule gitlinks, so none are required.

R311-1 FINISHED
