[R296] NEGATIVE - exact head f219a5edaa191b33acc8b77abd22469f8f0db1f9

# R296-2 internal independent review: issue #551 / PR #553

- **Reviewed head:** `f219a5edaa191b33acc8b77abd22469f8f0db1f9`, tree `aca067d42122d785d8319d4d0926484dd9351568`.
- **History reviewed:** merge `8dc98a429bd9918ad643fdb0051c2c9660395722` (parents `babb8925`, dev `864b36f5`), then the content commit `f219a5ed`.
- **Source base and live dev:** `864b36f5e9450ef64f75ca3f0d68c44330e447d7`.
- **Gitlinks at head, equal to dev:**
  - `protocol-processor` `990f96526bb89356c963a260ebbdcf2a77e6623a`, which contains `a8f8ce81` (processor PR #114 / issue #112);
  - `gptp-processor` `e5dcea6e`;
  - `third_party/verilog-axis` `48ff7a7e`;
  - `external` `efeb541a`, not initialised and not needed.

**Scope was reconstructed from:**
- AGENTS.md, CONTRIBUTING.md and docs/README.md;
- the #551 issue body (acceptance items 1-3);
- the manager decisions and assignments on the issue:
  - 5813147847: the licence becomes ACTIVE AND the real grant;
  - 5814963437: the acceptance for that change;
  - 5816014072: the R296-1 F1 fix goes in the processor;
  - 5831903033: round 3 (merge dev, flip the unwarmed arm, remove the residual-window text);
  - 5832468673: the history split;
- FR-SRP-03 (`docs/reference/FR_NFR.md:211`) and the processor interface the gate consumes (`protocol_processor_top.sv:518-527`, `KL_srp_top.sv`, `KL_srp_admission.sv`, `KL_srp_talker_fsm.sv:800-803`);
- the full diff `864b36f5..f219a5ed` and `git show --remerge-diff 8dc98a42`;
- the hosted check runs at the exact head.

I read the prior public review findings (R296-1, R297-1) only after completing my own pass.

**Verdict.** Every assigned behaviour holds, and I reproduced each one independently:
- the two-term gate;
- the mandatory unwarmed arm, which passes only because of the #112 fix;
- all the mutants;
- the clean merge.

One open MINOR (N1) keeps the verdict NEGATIVE. The spec-facing licence scenario still carries the pre-#112 "Residual ... pending fix" text, which round 3 was assigned to remove and which is now false.

## Findings

### N1 - MINOR - Conformance, Tests, Docs - `tests/features/milan_streaming_licence.feature:92-94` - the spec-facing licence scenario still describes the pre-#112 residual window as open

- **Authority/evidence:**
  - Round-3 assignment 5831903033, step 3: "the 'cannot open' claims are now true. Remove the residual-window text that described the pre-#112 round."
  - The comment in the `@clause:5.3.7.3` scenario at line 87 still reads: "Residual: a refused re-declaration with a different previous TSpec can still see about one round of licence: the first-round grant uses the previous slope. Processor issue #112 owns that pending fix."
  - It was added in `babb8925` and was not touched by `8dc98a42` or `f219a5ed` (`git log -- tests/features/milan_streaming_licence.feature`).
  - At this head the statement is false. The unwarmed arm `[I]` passes with 0 failures in all four source/phase cases (`receipts/crflic_head.log`). The same fixture fails 28 `[I]` assertions only when #112 is removed (`receipts/crflic_ctl_pin_7a47f57.log`, `receipts/crflic_ctl_rev_112.log`).
  - It also contradicts the other docs, which now say refused re-declarations cannot open a licence: FR_NFR:220, ieee8021q:57, CHANGELOG:101, REGISTER_MAP:1116, EGRESS_QUEUE_MAP:87.
  - It is the only such remnant: a search of the whole tree for residual, pending-fix or previous-slope wording found no other.
- **Impact:** a cold reader of the specification-facing contract, the artefact that pins #551's gate, is told two false things: that FR-SRP-03's "on failure the stream MUST NOT transmit" is still violated for changed TSpecs, and that a processor fix is pending. The executable evidence shows the opposite, so the assigned documentation acceptance is not met. Hosted `bdd-conformance` cannot catch this, because the text is a comment.
- **Required outcome:** the scenario's comment no longer describes a residual window or a pending #112 fix. It may say that the grant waits for the current TSpec (processor #112, adopted through #508). The step text and assertion stay unchanged.
- **Verification:**
  - A search of `tests/` at the fix head for `Residual|pending fix|previous slope` returns nothing.
  - `behave --no-capture -f plain` still passes all 344 scenarios.
  - `scripts/bdd_mutants.py` still reports all four mutants caught: ACTIVE-only, raw-grant-only, OR and extra-term.

### Suggestions (optional; they do not affect coverage)

**S1 - Tests - `tb/verilator/milan_dp/sim_crf_licence.cpp` `[INV]`: the closing edge where the grant falls while ACTIVE is high is not exercised.**
- A reviewer mutant with licence = ACTIVE AND (grant OR the grant delayed one cycle) survives, 415/0 (`receipts/reviewer_mutants.log`).
- ACTIVE is combinational over `opt_r | grant` (`KL_srp_talker_fsm.sv:800-803`). The grant can therefore fall under a high ACTIVE only inside the optimistic window, so the mutant is near-equivalent and has no practical impact.
- A future case that revokes a grant inside the window would make the documented "either term falling closes the gate" executable.

**S2 - Docs - `tb/verilator/milan_dp/README.md:468`: the pre-#112 control row gives only the 28 `[I]` failures.**
- The same run also fails 6 `[J]` admitted-case timing checks, 34 in total. I reproduced this, and the executor's issue comment also states it.
- Stating the total would let a re-runner match the receipt exactly.

## Assigned verification items

1. **Merge `8dc98a42`.** `receipts/merge_remerge_diff.txt` shows conflict resolutions in exactly three files and nothing outside them: `REGISTER_MAP.md`, `milan_datapath.sv` and the milan_dp README.
   - In `milan_datapath.sv`, the resolved gate is `assign lwsrp_stream_gate = pp_cd_srp_active_w[...] & pp_cd_srp_sr_admitted_w[...]`. Dev's #530 ACTIVE term and this PR's real-grant term both survive.
   - Dev's #508 content survives: the published-round and pending-declaration text and the `[GSI]` README row.
   - `receipts/merge_structure.txt` records that the merge's gitlinks equal dev's.
   - The merge alone builds and passes the leg: default 253/0 (`receipts/crflic_merge_8dc98a42.log`), and the then-opt-in unwarmed arm 339/0 (`receipts/crflic_merge_8dc98a42_unwarmed.log`).
   - The merge's README row already says the unwarmed arm keeps both licences closed, while its default leg still skipped that arm. That was true only transiently and `f219a5ed` fixes it, so it is not a finding.
2. **The unwarmed fixture.**
   - `[I]` preloads an admissible 224-byte TSpec, withdraws, then re-declares 20,000 bytes. A real MAC Listener Ready is decoded one cycle after the declaration (`sim_crf_licence.cpp:1078-1163`).
   - The fixture asserts that ACTIVE really rose once, optimistically (`:1125-1128`). A licence that read ACTIVE alone would therefore open.
   - At head the leg passes 415/0 (`receipts/crflic_head.log`).
   - My control repinning the processor to `7a47f578` gives 415 checks and 34 failures (`receipts/crflic_ctl_pin_7a47f57.log`):
     - 28 are `[I]`, in all four source/phase cases: a grant rise, a licence rise, STREAM_START/STOP each +1, and the 17/29/43 counter seeds reset to 0;
     - the other 6 are `[J]` timing checks.
   - A tighter control keeps `990f9652` and reverts only #112's admission RTL (`scripts/prefix_revert.sh`, `receipts/ctl_rev.patch`). It gives the identical 34 failures (`receipts/crflic_ctl_rev_112.log`). The pass is caused by the #112 fix, not by other processor changes.
3. **Mutants.**
   - The shipped campaign is 7/7 (`receipts/crflic_mutants_head.log`):
     - the clean control passes;
     - the three raw-grant-only mutants are caught on their pre-Listener checks;
     - the three drop-real-grant mutants (ACTIVE-only: whole gate, CRF alone, AAF 0 alone) are caught on "refused ... never opened".
   - The reviewer's OR mutant is caught with 79 failures (`receipts/reviewer_mutants.log`).
   - BDD: the ACTIVE-only, raw-grant-only, OR and extra-term variants all fail the scenario. The clean control passes before and after (`receipts/bdd_mutants.log`).
4. **Docs.**
   - The residual-window text is removed from FR_NFR, REGISTER_MAP, EGRESS_QUEUE_MAP, ieee8021q, CHANGELOG, the milan_dp README and the RTL comments. The feature file is the exception (N1).
   - The "cannot open" claims hold under the SRP-policing configuration they describe. The pre-existing escapes are unchanged and documented: the `AAF_CTRL[1]` bypass (audit B9), and lwSRP or talker policing turned off.
5. **Clauses.**
   - The FR-SRP-03 quote matches `FR_NFR.md:211` verbatim.
   - The Milan v1.2 5.3.7.3 licence matches `MILAN_COMPLIANCE_MATRIX.md:179`.
   - The 5.3.7.7 Table 5.4 counters match `REGISTER_MAP.md:941` and the leg README's FRAMES_TX section.
   - 802.1Q 34.3/34.4 map to `KL_pp_shadow` in `MODULE_MATRIX.md:160`.
   - `docs/spec-refs.md` does not exist in this tree or in history (see limits).

## Round-1 findings: resolution at this head

| finding | state | evidence |
|---|---|---|
| R296-1 F1 (MAJOR, stale first-round grant) | CLOSED | Processor `990f9652` invalidates a declaring source at every pipeline stage (`KL_srp_admission.sv:118,142-149`), retires its grant on the declaration edge, and does not publish a round that met a pending source (`:192,220-238`). `[I]` and `[J]` are mandatory and pass. The pre-fix pin and revert controls fail 28 `[I]` assertions. Latency is re-measured for both histories: AAF 5/5, CRF 3/5, matching README:442-449 and CHANGELOG. The reset-state variant is closed by RTL reading: `slope_valid_r` resets to 0 and `invalid_w = invalidate_i \| ~req_i`. The remaining text remnant is N1. |
| R296-1 F2 (BLOCKER, BDD red) | CLOSED | The scenario pins the exact AND (`milan_streaming_licence_steps.py:174-185`). The full suite passes 344/0 (`receipts/behave_full_head.log`), and the four BDD mutants fail. `MILAN_COMPLIANCE_MATRIX.md:179` and README:27 are updated. Hosted `bdd-conformance` is success. |
| R296-1 F3 (MAJOR, generator stale) | CLOSED | `gen_module_matrix.py --check` returns rc 0 (`receipts/gate_docs_traceability_gen_module_matrix.py.log`). |
| R296-1 F4 (MINOR, Q-9/Q-10) | CLOSED | `ieee8021q.md:96-97` restores the mapping (`KL_srp_admission` behind `KL_pp_shadow`), the PROCESSOR status, the deleted-suite caveat, "It does not test the 75 % boundary" and the 34.3/34.4 rationale. Line 35 names both terms. `milan_datapath.sv:6572-6575` now says the licences read the grant per source. |
| R297-1 F1 (MAJOR, cold pipeline) | CLOSED | As R296-1 F1. Withdraw-then-redeclare within one round is covered too: every accepted declare or withdraw strobes `invalidate_i` (`KL_srp_top.sv:759-764`). |
| R297-1 F2 (MAJOR, BDD) | CLOSED | As R296-1 F2. |
| R297-1 F3 (MINOR, matrix and citation) | CLOSED | As R296-1 F3 and F4. The `KL_pp_shadow` row lists 34.3 and 34.4. |
| R297-1 F4 (MINOR, ACTIVE-only descriptions) | CLOSED | Corrected at `milan_datapath.sv:1642-1645,1910-1913,5293-5295,5334`, `ieee8021q.md:35`, README:27 and MILAN_COMPLIANCE_MATRIX:179. `KL_pp_shadow.sv:635-642` records the #551 deviation. The processor's own port comment (`protocol_processor_top.sv:518-519`) now recommends the same AND. |

## Clean lenses (evidence)

```text
[R296] PASS RTL - hdl/milan/milan_datapath.sv:6623-6624,1885-1887,1914-1917,2023-2028,2506,3056-3060,5296-5297,5321-5335; hdl/milan/KL_pp_shadow.sv:632-642; protocol-processor@990f9652 hdl/srp/KL_srp_admission.sv:109-263, KL_srp_top.sv:448-451,739-893, KL_srp_talker_fsm.sv:795-803 - checked: both vectors are [SRP_TALKERS_C-1:0] slices of ACMP_SRC_C-wide processor outputs on axis_clk (pp_shadow clk_i at :7690), so there is no new CDC; every lwsrp_stream_gate reader inherits the AND (lobs above index 0, AAF 0, AAF above 0, LWSRP_STATUS[8], and the CRF licence into crft_emit_en_w, tkd_streaming_w and CRFT_CTRL[6]/[7]); LWSRP_STATUS[6] stays |ACTIVE (:6640); lint_rtl, the sv/cpp/py idiom gates, the source-list gate and the xvlog ratchet all return rc 0 (receipts/rtl_gates_summary*.txt); the remerge-diff is clean.
[R296] PASS Robustness - sim_crf_licence.cpp:1078-1190 with receipts/crflic_head.log, crflic_ctl_pin_7a47f57.log, crflic_ctl_rev_112.log - checked: both sources at both round phases; same and changed TSpec histories in both directions; withdrawal clears the grant and ACTIVE; nonzero counter seeds expose resets; refusal under a live early Listener Ready; the first declaration after reset, by RTL reading (slope_valid_r resets to 0; invalid_w = invalidate_i | ~req_i); repeated identical re-declarations invalidate (KL_srp_top.sv:759-764); the configuration escapes (bypass, lwSRP off, talker policing off) are unchanged; pending rounds hold the other grants, which fails closed.
```

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (N1) | #551 acceptance, decisions and round-3 assignment; FR_NFR:211-231; MILAN_COMPLIANCE_MATRIX:179; the processor interface `protocol_processor_top.sv:518-527`; `receipts/crflic_head.log`, the control logs, `bdd_mutants.log` | R296-2 | f219a5edaa191b33acc8b77abd22469f8f0db1f9 |
| RTL | CLEAN | see the PASS RTL line; `receipts/merge_remerge_diff.txt`, `rtl_gates_summary2.txt`, `reviewer_mutants.log` | R296-2 | f219a5edaa191b33acc8b77abd22469f8f0db1f9 |
| Robustness | CLEAN | see the PASS Robustness line | R296-2 | f219a5edaa191b33acc8b77abd22469f8f0db1f9 |
| Tests | UNCLEAN (N1) | `sim_crf_licence.cpp` [G]-[J] and [INV]; `crflic_probes.vlt`; `crflic_mutants.py`; the Makefile crflic targets; the feature and steps; `receipts/crflic_head.log`, `crflic_head_flag.log`, `crflic_mutants_head.log`, `reviewer_mutants.log`, `bdd_mutants.log`, `behave_full_head.log`, both controls | R296-2 | f219a5edaa191b33acc8b77abd22469f8f0db1f9 |
| Docs | UNCLEAN (N1) | CHANGELOG:46-112; FR_NFR:211-231; REGISTER_MAP:936,1105-1147,1176-1177; EGRESS_QUEUE_MAP:74-106; ieee8021q:35,50-67,96-97,122; MILAN_COMPLIANCE_MATRIX:179; milan_dp README:27,357-475; the RTL comments; the generated matrices; `receipts/doc_gates_summary.txt`: docs_check, doc_style, doc_paths, gen_module_matrix, em_dash (base 864b36f5) and gen_toc all rc 0 | R296-2 | f219a5edaa191b33acc8b77abd22469f8f0db1f9 |

## Real limits

- **Clause text.** `docs/spec-refs.md`, the authority the brief names, does not exist in this tree or in its history. No Milan or 802.1Q standard text is available on this host. I checked clause citations against the in-repo authorities (FR_NFR, MILAN_COMPLIANCE_MATRIX, REGISTER_MAP, MODULE_MATRIX), not against the standards.
- **Geometry.** Everything I executed ran on the AX 1x1 TDM8 two-source shape, with the leg's compressed millisecond grid. The latency figures and the three-round bound hold for two sources only, as the docs state.
- **First declaration after reset.** This case is RTL reading only, and the README discloses that the arm does not cover it.
- **Fixture method.**
  - The fixture stages the processor's S_GATE service tuple instead of driving a DECLARE from a controller (disclosed). Its effect is equivalent to a real request after S_IDLE acceptance (`KL_srp_top.sv:801-893`).
  - Refusal is staged with an oversized 20,000-byte TSpec, not at the 75 % boundary (disclosed in Q-9).
- **PDU check sensitivity.** Neither pre-fix control produced a refused-case PDU, so in this schedule the "emits no PDU" check has no failing arm. The licence-never-opened check is strictly stronger, and the OR mutant's `[A]` failures show the PDU counters are sensitive.
- **Banks not run.** I did not run the default `milan_dp` sweep, the full parent, PP or gPTP banks, Yosys, the builder, act or Docker. I did not re-execute the manager's banks at this head.
- **Environment workarounds.**
  - The first idiom and xvlog attempts refused to run because the scratch clone's submodules were not registered. They passed once the submodules were registered (`rtl_gates_summary.txt`, then `rtl_gates_summary2.txt`).
  - The em-dash and TOC gates ran in an existing pinned Markdown environment, used read-only. The first attempt without it reported the renderer missing.
- **Hosted evidence.** Read at observation time (`receipts/hosted_checks_f219a5ed.tsv`): every context succeeded at the exact head, and Physical gPTP was skipped. The manager owns hosted and act acceptance.
- **Hardware.** Physical calibration was NOT RUN. Field skips and simulation are not hardware proof.

## Pending manager duties

- Route N1 to the executor.
  - A comment-only edit to the feature file changes an artefact in the Tests, Docs and Conformance scopes, so those three lenses must be covered again at the fix head.
  - RTL and Robustness stay banked at `f219a5ed` if nothing in their scope changes.
- The PR body's "Status" section and its leading `[A312]` line predate publication; refresh them at the next edit.
- Own hosted and act acceptance at the final head, and obtain a second independent positive review.
- Build and validate the current-dev candidate at the merge turn.
- No merge happens without explicit maintainer authorization.

## Restoration

- Every build, control and mutant ran in disposable clones under `scratch/`, which is not published.
- The review clone was never edited. `receipts/restore_verification.txt` checks it against the exact head:
  - HEAD is `f219a5ed`, and `write-tree` equals `aca067d4`;
  - `status --porcelain --ignored` is empty;
  - the index and HEAD agree on mode, blob and path, every tracked blob re-hashes equal, and no mode changed;
  - the gitlinks are `990f9652`, `e5dcea6e`, `48ff7a7e` and `efeb541a` (uninitialised, as at start), and the submodule checkouts are clean.
- `scripts/redact.py` replaced the host paths in the receipts with placeholders.

R296-2 FINISHED
