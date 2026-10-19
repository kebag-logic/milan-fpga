[R670] NEGATIVE - exact head 63a187e1579474bca562d85304b9a91466877c33

# R670-1: external independent review of #637 / PR #768

Four MAJOR and two MINOR findings remain open. All five lenses were applied;
none is clean. Three wording residues are non-blocking. This is a source
review, not permission to merge or hardware qualification.

Head: `63a187e1579474bca562d85304b9a91466877c33`.
Tree: `45c859e17681896f2fa3db26c04de75ef9f125d4`.
Base: `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`.
The delta has 11 commits and 22 changed files.

## Scope and independence

Reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README.md, the
[issue and public decisions](https://github.com/kebag-logic/milan-fpga/issues/637),
linked requirements and interfaces, the complete diff/history, then
[published executable receipts](https://github.com/kebag-logic/milan-fpga/tree/270c5c99c74e88be21806ec5319556981b0f188b/review-evidence/637-r1/author/receipts).
No private author material or other checkout was examined or edited.
`receipts/independent-initial.md` records my own verdict and five-lens ledger
before opening the prior public review. Its findings were then reconciled
below. No GitHub writes were made.

The acceptance covers parent writes and restore of `0x60 + input port` and
`0x70 + output port`, successful ADD/REMOVE changes, empty sets, well-formed
restore, defaults for torn/corrupt records, rollback, ownership documentation,
unchanged framing, and capture timing/census evidence. The assignment requires
planted controls and stops on processor register-map/top-level-port/parameter
changes. No such processor change occurs in this delta.

| Acceptance / decision | Result |
|---|---|
| Parent restores maps under D3 and resets them on rollback | Implemented and exercised at 1x1, but F1/F2/F3 prevent full acceptance. |
| Ownership stated and aligned with the processor | Parent ownership matches pinned `07_memory_maps.md` 5.1. F6 leaves the pass-count contract unresolved. |
| Planted cycle, empty and non-default lists, torn-record default | Reproduced: committed dynmap leg 331 checks, zero failures. |
| Existing record format retained | Codec byte comparisons pass at 1x1; record-space/self-test passes, including parent-layout control. |
| Capture timing/census unchanged or remeasured | Census, clocks, both timing arms and existing receipt check pass. Capture implementation/census are unchanged. |
| Physical cold cycle from release scheduling | NOT RUN. The subsequent assignment explicitly calls for a planted cycle; physical qualification remains owed on #637. PR uses “Relates to”, not an issue-closing claim. |
| Every touched gate passes | Not met: three required gates fail locally; hosted docs-check fails. |

The public dependency account identifies merged scalar prerequisites and
ratified DR3a/DR4 decisions. Name adoption remains outstanding and its sticky
pending source is retained. DR4 limits shipping placement acceptance to 1x1;
it does not silently waive multi-port functional persistence.

## Findings

### R670-F1 - MAJOR - Conformance, RTL, Robustness, Tests, Docs

**Artifact:** `hdl/milan/milan_datapath.sv:5228`, `:5583`, `:2834`;
`hdl/milan/KL_pp_shadow.sv:1630`, `:1641`;
`docs/reference/REGISTER_MAP.md:2391`.

**Title:** Public restore status excludes the map restore.

**Authority/evidence:** MATERIALIZATION 5.2/8.7 forbid reporting a failed
restore as a clean blank boot; acceptance 1 adopts the D3 rules.
`amr_rs_fail_r` is set on map rollback but has no public status consumer.
Fail/blank still come solely from the processor walks. Committed tests grade
an internal map flag rather than the public result.

My independent probe, with unchanged production RTL, reads:

| Case | PP_STAT | Public done/fail/blank | Local map failure |
|---|---|---|---|
| Saved maps restored, confirmed by GET and both RAMs | `0x5b000484` | `1 / 0 / 1` | `0` |
| Error restricted to output-map payload lanes; all maps rolled back | `0x5b000484` | `1 / 0 / 1` | `1` |

`receipts/probe-maps-run.txt` has 131 checks and exactly three failures:
blank after successful restore, fail after map-only error, and blank after
that error. The fault premise explicitly requires local map failure, so a
processor-walk failure cannot substitute for this case.

**Impact:** Software cannot distinguish successful map recovery from saved
maps lost to a transport failure. Firmware boot diagnostics report a clean
blank result for both. Public done also precedes the map outcome.

**Required outcome:** Compose truthful parent restore outcomes, including
map-only success/failure, and document observable timing and bit semantics.
Preserve the assignment's processor-interface boundary. An alternative
status contract requires an explicit public decision.

**Verification:** Public-register assertions for blank boot, saved maps,
device error, both deadline paths and refused put-back, with controls that
disconnect the outcomes. Keep the map value/RAM assertions.

### R670-F2 - MAJOR - Conformance, RTL, Robustness, Tests, Docs

**Artifact:** `hdl/milan/milan_datapath.sv:4396`, `:4548`, `:4582`, `:5346`,
`:5562`; generated 8x8 geometry; PR #768 multi-port limitation.

**Title:** Another port's reset ownership can reject a legal saved output map.

**Authority/evidence:** Acceptance 1 covers the map records. MATERIALIZATION
18.4 requires independent persistence, first/last ports and real ownership
and routing checks. The restore removes and adds each port before advancing;
other ports still own their reset keys. ADD refuses a differently owned key.

Concrete counterexample: remove stream 1/channel 0 from output port 1,
add it to output port 0, and save both records. These command-time changes
are legal. After reset, port 1 owns that key again. Restoring port 0 first
removes only port 0's identity, then refuses the saved claim. Port 0 gets
its reset set instead; later restoring port 1 never revisits port 0.

This is source-derived, not a claimed 8x8 execution. The PR acknowledges
the failure mode. The new runtime leg has only one port per direction;
codec/model record-space tests do not execute this ownership ordering.

**Impact:** Successful map changes can lose their saved routing after a
cycle. Non-shipping placement status is not a functional waiver. Moving the
limitation to another issue does not resolve the defect.

**Required outcome:** Restore valid cross-port ownership transfers without
transient reset-owner conflicts, or obtain an explicit scope amendment for
excluded shapes and reconcile the authoritative contract. Documentation alone
does not satisfy the current acceptance.

**Verification:** Real multi-port save/reset/restore for transfers in both
port orders and a cyclic swap; grade GET, ownership and routing, with a
control restoring the current ordering.

### R670-F3 - MAJOR - Conformance, Robustness, Tests

**Artifact:** `tb/verilator/milan_dp/sim_nxn.cpp:4864`;
`tb/verilator/milan_dp/dynmap_mutants.py:163`;
`hdl/milan/milan_datapath.sv:5333`, `:5409`, `:5415`, `:5422`, `:5456`, `:5567`.

**Title:** Important refusal and recovery arms lack committed defect-detecting tests.

**Authority/evidence:** MATERIALIZATION 18.4 requires malformed records,
UNUSED/hole rules, conflicting keys and recovery controls. The assignment
requires a planted mutant for each new check. The committed section tests
payload corruption under an old CRC, but supplies no CRC-valid hole/range/
conflict cases or ADD refusal requiring the clipped reset set to be re-added.

My disposable tests supply a hole, invalid channel, conflicting input-cluster
mappings, and a saved channel-6 mapping against a restored four-channel input
format. All four correctly default the input while restoring the output at
this head. The refused ADD puts back the four-channel clipped identity.

Two independent controls prove the additional oracles detect their faults:

| Control | Additional failures beyond the three F1 failures |
|---|---|
| Disable hole-malformed flag | Input count, exact list and render RAM: one entry wrongly applied instead of eight defaults. |
| Omit reset-map re-add after refused ADD | Input count, exact list and render RAM: zero entries instead of four defaults. |

Both builds succeed; each executable runs 131 checks with six failures.
See `receipts/hole-control-run.log` and `receipts/putback-control-run.log`.
These are value/routing mismatches, not timeout or compilation failures.

The prior public review also reports surviving controls for wrong layout/id,
range dropping, duplicate-cluster acceptance and restore after pass-0 DEFAULTS.
I retained these after checking the source guards and absence of their stimuli
in the committed test. I did not rerun that six-control campaign; its executions
remain attributed to the prior public review.

**Impact:** These regressions can ship while the committed leg stays green,
including a port left empty after a refused saved set.

**Required outcome:** Commit checks and killing controls for all six retained
arms: put-back, holes, layout/id, ranges, conflicting keys and pass-0 DEFAULTS.
Include directional and port-boundary coverage required by 18.4. Codec-only
tests do not replace the actual restore path.

**Verification:** Clean source passes the new value/RAM assertions; every
planted guard/recovery defect fails its named oracle. This packet supplies
review evidence, not a production fix.

### R670-F4 - MAJOR - RTL, Tests, Docs

**Artifact:** `hdl/milan/milan_datapath.sv:9106`;
`tb/verilator/milan_dp/sim_nxn.cpp:4814`, `:4815`, `:4864`, `:5240`;
`.github/workflows/docs.yml:361`, `:374`, `:389`.

**Title:** Three mandatory gates fail; the public all-green account is incomplete.

**Authority/evidence:** CONTRIBUTING requires successful local gates and
protected contexts. Independently reproduced on the unchanged source copy:

| Command | RC | Finding |
|---|---|---|
| `python3 scripts/check_port_contracts.py` | 1 | Literal `pp_shadow.mrec_offset_i` lacks its required binding rationale. |
| `python3 scripts/check_cpp_idiom.py` | 1 | Two multi-declarator detections and one long-function detection exceed zero ratchets. |
| `python3 scripts/measure_test_evidence.py --check` | 1 | Four detected wall-clock-dependent suite files exceed ratchet three. |

The last detector matches `alarm (` in a new assertion label. That is a
false positive on prose, not evidence of actual host-clock use. The required
gate nevertheless remains red; increasing its ratchet would hide the problem.

The exact-head [hosted docs job](https://github.com/kebag-logic/milan-fpga/actions/runs/39253615324/job/118063268343)
failed at step 38, Port contract gate. Steps 41/44 are skipped, not passed.
Included API receipts distinguish executed steps and cancelled checks. The
full-ci selector succeeded; the long aggregates failed and their execution
shards were cancelled. They provide no successful exact-head long-gate result.

**Impact:** This head cannot meet the merge bar. Fixing only the first hosted
failure leaves two independently reproduced failures.

**Required outcome:** All three checks and required self-tests pass without
loosening ratchets. Justify the port binding; make focused code/detector
corrections as appropriate. Correct the validation account to distinguish
executed, skipped and cancelled work.

**Verification:** Exact-head local receipts and successful hosted docs job,
then the manager's remaining required contexts.

### R670-F5 - MINOR - Docs

**Artifact:** `docs/reference/REGISTER_MAP.md:2391`;
`hdl/milan/KL_pp_shadow.sv:1180`.

**Title:** PP_STAT[4] documentation omits the parent map writer.

**Authority/evidence:** New logic ORs `amap_alarm_i` into public alarm and
backend backing revocation. MAPREC grades it. The register row still names
only the binding manager and D3 writer.

**Impact:** The observable register contract gives an incomplete alarm source.
This changes a contract claim, so it is MINOR rather than wording residue.

**Required outcome:** Include the parent map writer with the same three-attempt,
reset-sticky semantics.

**Verification:** Revised row matches wiring and failing-write test; doc gates pass.

### R670-F6 - MINOR - Conformance, Docs

**Artifact:** `docs/design/SAVED_STATE_MATERIALIZATION.md:375`, `:2811`, `:2844`;
`hdl/milan/milan_datapath.sv:4913`; issue REVIEW READY comment 6267367417.

**Title:** The one-pass deviation remains unreconciled with the accepted contract.

**Authority/evidence:** The accepted D3 decision specifies two reads per record;
18.4 still requires remeasurement of both passes and rollback. The added
implementation subsection specifies one pass. The author flags the deviation
and asks whether it needs a ruling. No such manager decision appears in the
issue comments or PR review-start notices inspected. AGENTS 2/4 require public
resolution of normative conflicts, rather than implementation text deciding them.

**Impact:** A cold reviewer cannot determine which restore transaction is
accepted. This is not a claim that one pass inherently loses data: the examined
1x1 rollback cases work. It is an unresolved contract/acceptance choice.

**Required outcome:** Obtain a public disposition and reconcile the normative
text, validation obligation and implementation description, or satisfy the
existing two-pass requirement. State the map-only transaction boundary explicitly.

**Verification:** Linked decision, consistent authorities and tests for the
selected transaction's faults and deadlines at the corrected head.

## Residues

These are **RESIDUE**, lens **Docs**, under the owner's wording/comment rule.
They change no measurement, figure, verdict, test, code behavior, generated
artifact, conformance claim or privacy rule and leave no additional lens unclean.

| ID | Artifact | Evidence / impact | Exact fix and verification |
|---|---|---|---|
| R670-R1 | `hdl/milan/milan_datapath.sv:4931` | Navigation comment points to check 13; layout check is 15. | Replace `check 13` with `check 15`; compare with gate docstring. |
| R670-R2 | `hdl/milan/KL_pp_shadow.sv:966` | New source comment carries a lane label. | Replace `(D3 18.3, lane 3)` with `(D3 18.3)`; inspect added-line diff. |
| R670-R3 | `tb/verilator/milan_dp/sim_nxn.cpp:5183` | New source comment carries a lane label. | Delete ` (lane 3)`; inspect added-line diff. |

## Prior public findings: explicit disposition

Source: [prior public review](https://github.com/kebag-logic/milan-fpga/pull/768#issuecomment-6268811441),
read only after my independent verdict/ledger was written. No intervening source
commit exists. No finding is cleared by moving it to a follow-up issue.

| Prior item | Disposition at this head |
|---|---|
| F1: invisible map verdict | RETAINED as F1, independently reproduced; Robustness also applies. |
| F2: six uncovered restore arms | RETAINED as F3. Four additional clean cases and two killing controls executed here; other survivor executions remain attributed to the prior public review. |
| F3: port contract gate | RETAINED in F4; independently reproduced. |
| F4: two later gates | RETAINED in F4; independently reproduced. |
| F5: multi-port ordering | RETAINED as F2, elevated from MINOR to MAJOR: loss of accepted saved routing is a functional defect, not just missing prose. All five attributable lenses apply; no functional waiver was found. |
| F6: alarm contract | RETAINED as F5. |
| R1/R2/R3 | RETAINED as R670-R1/R2/R3. |
| S1: ungranted waits count as attempts | Retained as optional clarification of attempt terminology; no additional finding asserted here. |
| S2: busy/done excludes map interval | Retained with F1's required timing reconciliation. |
| S3: payload formula consistency beyond 1x1 | Retained as optional gate improvement; F2/F3 still require behavioral coverage. |

## Evidence and passing sub-results

Before execution, the pinned simulator was verified as version 5.050,
SHA-256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`.
No shared installs, hardware, full banks or hosting orchestration ran.
All disposable copies/builds are under `scratch/`. Independent commands ran
concurrently; compilation stayed at twelve jobs total, with `make -j16`.
Every foreground process was awaited.

| Receipt / command | Result |
|---|---|
| `run_focused.py`, committed dynmap leg | RC 0; 331 checks, zero failures. |
| Record-space self-test and census | RC 0; 22 controls detected, including parent-layout; five configurations. |
| Capture check | RC 0; census, clocks, both timing arms and receipt agree. |
| `probe_maps.py` | Make RC 2 from assertion failures; 131 checks, exactly three F1 failures. Added malformed-value/put-back checks pass. |
| `probe_controls.py` | Both builds RC 0; each run RC 1, 131 checks, six failures: three F1 failures plus three targeted value/RAM failures. |
| `check_local_gates.py` | All three target checks RC 1, as F4 details. |
| `verify_checkout.py` | Exact tracked bytes, file kinds/modes, index and five required submodule checkouts/gitlinks pass. |

Architecture review covered common clock/reset wiring, stable requests,
registered grants, side selection while busy, read drainage, abandoned-write
containment, record/cursor widths, dirty/taint priorities, accepting-edge
pending, retries/alarms and format/edit/CSR holds. No new CDC is introduced.
Framing matches FASTCONNECT 4.2/6.1; empty remains a framed UNUSED payload.

The passing committed leg exercises actual ADD/REMOVE/GET paths and both map
RAMs, debounce, unchanged-write suppression, taint, contention, retry exhaustion,
both restore deadlines and late-read drainage. Passing sub-results do not
clear a lens with an open finding.

I hash-verified 86 selected published author receipts against the public
manifest. The exact-head sweep reports 63/63 suites and 2,186,578 checks;
four explicit field/freshness skips contribute zero checks. The published
campaign reports 37 controls caught. These are author executions, not this
reviewer's reruns or a manager source bank.

Matched route evidence reports LUT +289, FF +262, unchanged BRAM/DSP,
WNS +0.215 to +0.316 ns and complete routing, within DR4's 1x1 ceiling.
Its measured commit is `90b15366`; the `hdl/` diff from there to head is empty.
The 8x8 receipt is standalone shadow synthesis, not execution of the multi-port
map restore or full 8x8 placement qualification.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1/F2/F3/F6 | Issue acceptance; REQUIREMENTS persistence inventory; FASTCONNECT 4.2/6.1; MATERIALIZATION 3/8/18.4; processor 07_memory_maps 5.1; codec/status probes | R670-1 | 63a187e1579474bca562d85304b9a91466877c33 |
| RTL | UNCLEAN: F1/F2/F4 | milan_datapath FSM/ownership/holds/CSR wiring; KL_pp_shadow arbiter/pending/alarm; backend and pinned NVM-port grant/drain contracts; port gate | R670-1 | 63a187e1579474bca562d85304b9a91466877c33 |
| Robustness | UNCLEAN: F1/F2/F3 | Frame/UNUSED/range guards; error/deadline rollback; refused-ADD recovery; contention/late read; multi-port ownership; probe/control receipts | R670-1 | 63a187e1579474bca562d85304b9a91466877c33 |
| Tests | UNCLEAN: F1/F2/F3/F4 | sim_nxn MAPREC; dynmap_mutants; pp_shadow P2 delta; record-space control; nvm_cosim scope; baseline/additional oracles/controls; failed required gates | R670-1 | 63a187e1579474bca562d85304b9a91466877c33 |
| Docs | UNCLEAN: F1/F2/F4/F5/F6 | Saved-state design/ownership pages; REGISTER_MAP; compliance matrix; firmware/design/roadmap pages; TESTING and changed READMEs; PR/evidence claims | R670-1 | 63a187e1579474bca562d85304b9a91466877c33 |

No clean covering round is banked here. Fixes require re-review of changed
artifacts and explicit closure of the retained findings.

## Reproduction and integrity

Copy the exact-head initialized clone to `scratch/source`, then run:

```sh
python3 run_focused.py
python3 check_local_gates.py
python3 probe_maps.py
python3 probe_controls.py
python3 verify_checkout.py /absolute/path/to/exact-head-review-clone
```

`REVIEW_VERILATOR` can select the same verified installation on another host.
Probes edit only disposable copies. `receipts/probe-harness.diff` records the
additional harness instrumentation. Expected failure counts above separate
the production status defect from the controls.

The original clone retains the exact head/tree. Required pins are:

- processor: `2cbed0a987c1e68402658d69459ab7e5aa571adc`;
- time processor: `e4869fd0c42889b2ac806587cc5c78afb1c33461`;
- lwSRP: `08ee86e812a0eb5e1dc6cd61b494d8baf3491348`;
- tsn-c-stack: `70936b77dc41981e192438388cd0aced69954f18`;
- verilog-axis: `48ff7a7e2ef782cf778d47910cf85835c64b1bce`.

The optional `external` gitlink remains recorded and uninitialized. Integrity
verification compares raw blobs and modes, not merely status/index cleanliness.

Raw logs remain under `scratch/raw-receipts/`, excluded from publication.
Published build logs redact installation paths; `receipt-provenance.json`
records original and published hashes. Extracted simulation run receipts
preserve raw output. `MANIFEST.sha256` enumerates publishable files; disposable
trees and downloaded caches are excluded.

## Real limits and pending manager duties

- Physical calibration and board cold cycles: **NOT RUN**. Field skips and
  retained-window resets are not hardware proof. Actual DDR hold latency and
  full saved-set qualification remain open. The zero-latency hold measurement
  is not a board guarantee against the 4,096-clock command watchdog.
- Not rerun: full 37-control author campaign, full suite/synthesis/route banks,
  or the prior six-control campaign. Full 8x8 map behavior was not executed.
  Only enumerated executions are claimed.
- No manager source bank ran at this head; none is inferred. Source evidence
  is the author's public receipts plus this focused review.
- Resolve findings and scope/contract decisions, obtain independent re-reviews,
  and carry R1-R3 to the residue checklist. A follow-up issue does not clear an
  extant defect. Physical qualification remains owed on #637.
- The manager owns hosted/local-replica acceptance. Failed/cancelled contexts
  do not discharge it.
- At merge time the manager constructs the current-dev candidate, runs the
  builder/native banks and links receipts. Stated live dev equals this source
  base, but no candidate validation or merge is claimed. Explicit maintainer
  merge authorization, post-merge containment and issue/board completion remain
  separate duties.

R670-1 FINISHED
