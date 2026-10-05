[R499] NEGATIVE - exact head bef8dd7036f711bf286929fa4cba6bf724c7118d

R499-1 external independent review of issue #653 / PR #666. All five lenses were applied. Two MINOR findings remain open; one formatting RESIDUE and one SUGGESTION are also recorded. The measured response-order result is supported; restoration evidence and public privacy prevent approval.

Reviewed tree: `20594912f6c5e614d2686232569402d6b48a2473`. Source base: `fa450d301805881ad713b67521477bf042ddadfd`. One commit adds 424 lines to `docs/findings/653_DISCONNECT_ORDER_BENCH.md`; no implementation, interface, test or submodule pin changes. Bench observations concern flashed image `bbf704ec`, not a freshly flashed reviewed head.

Scope was reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue body, and the public decisions, especially [the B12 assignment](https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5993102892). REQUIREMENTS.md, architecture and integration contracts, pinned controller sources, then the diff/history and [published evidence](https://github.com/kebag-logic/milan-fpga/tree/9649a107657bdc77d1c47d7ce735e6a282394235/review-evidence/653-b12-r1) were examined. No private author material or other review report informed this independent verdict.

**R499-1-F1 | MINOR | Docs | Public identifying fields remain in the page and encoded evidence.**

Artifact: `docs/findings/653_DISCONNECT_ORDER_BENCH.md:62`; evidence `author/identity.json:6` and `:10` at `9649a107657bdc77d1c47d7ce735e6a282394235`.

Authority/evidence: CONTRIBUTING.md section 6 and the assignment require role labels and prohibit identifying device information. The page's existing identity row contains a unit serial and device-name literals. The evidence replaces its displayed serial with a placeholder but retains the same 11-byte serial in `descriptor_payload`, beginning at decoded byte 248. The encoded name is retained too. `privacy-audit.json` locates these fields without repeating their values. The page row predates this diff; it remains present at the exact head and the requested whole-page privacy check finds it. The standard plaintext scrub passed, demonstrating its limit for encoded fields.

Impact: publishing the page and evidence republishes the identifying fields despite the apparent redaction. This touches a privacy rule and is not RESIDUE.

Required outcome: replace public device names/serials with neutral roles, including their encoded representations in the evidence. Preserve required identity verification privately and publish only a sanitized verification receipt. Regenerate affected evidence hashes and explicitly record redaction provenance.

Verification: recheck the complete page and every published evidence file, decoding embedded identity payloads. Require that only permitted anonymous fields remain. Rerun documentation checks and verify the replacement manifest.

**R499-1-F2 | MINOR | Conformance, Robustness, Tests, Docs | Restoration equality is asserted without checkable successful readbacks.**

Artifact: `docs/findings/653_DISCONNECT_ORDER_BENCH.md:776`; evidence `author/restore-comparison.json`, `author/restore_compare.py:11` and `:24`, and the six indexed `census`, `dut-descs`, `peer-descs` start/end receipts.

Authority/evidence: B12 item 5 requires both entities' bindings, formats, maps and clock sources restored with readbacks. The public packet contains eight equality summaries covering 43 observations, but none of the six underlying small readback files or their normalized values. Equal hashes are therefore operator assertions that this reviewer cannot recompute. Moreover, the comparator checks equality of status values without requiring success, and permits an empty census. In the disposable probe, 43 identically failed start/end observations return `pass_restore=true`, exit 0; two empty populations also pass. A real changed-format control fails, confirming that the comparator ran. See `offline-probes.log` and `receipt-audit.log`.

Impact: the published proof cannot distinguish restored successful state from matching failed observations. This is an evidence/validation defect; it does not establish that the physical restoration was wrong.

Required outcome: publish sanitized before/after readbacks or complete normalized records with per-command status and descriptor identity. Prove the required inventory is present, all relevant readbacks succeeded, and each effective value matches. The restoration validation must reject failed, absent, conflicting duplicate or truncated required observations before claiming equality. Preserve the stated monotonic residuals separately.

Verification: independently recompute all eight comparisons from the published values, at the stated 43-observation inventory; retain equal-success and changed-format controls and add rejected failed/empty/malformed populations. No new hardware run is required if the retained successful readbacks establish this.

**R499-1-S1 | SUGGESTION | Tests, Docs | Add the available startup timing to the peer observations.**

Artifact: `docs/findings/653_DISCONNECT_ORDER_BENCH.md:740` and `:760`; evidence `author/short-polls.csv`, `author/rule-increments.json`, `author/wire-receipts-*.json`.

Authority/evidence: B12 asks for separate first-PDU assessment and timestamped findings. The two callback times are correctly labeled as callback times, and fault ownership is explicitly unresolved. The receipts already establish more: EARLY is present at `11:19:03.730732Z`, 29.880 ms after bind submission, with 68 reported received frames; LATE is present at `11:20:09.640696Z`, 29.947 ms after submission, with 67. Both precede unbind. The application's callbacks follow those reads by 318.532 and 418.654 ms respectively. Separately, using only the tap clock, the first retained PDUs arrive 20.227033 and 20.407250 ms after the bind command. These are separate clocks; those intervals must not be subtracted from one another.

Impact: the current table adequately identifies counts and reporting listener, but leaves useful startup localization unused. A NotConnected callback does not locate the EARLY event after disconnection.

Suggested outcome: include the earliest nonzero counter read and its pre-unbind bound. State that the retained first-PDU receipts contain sequence and capture-time fields, not presentation timestamps or timestamp-validity bits. Their analysis cannot assign timestamp fault ownership; fuller headers and a justified time reference would be needed. This does not reopen the supported zero-sequence claim or require a fix to product logic in this findings-only lane.

Verification: reproduce the two counter transitions and tap-relative startup intervals with `audit_receipts.py`, retaining unresolved fault attribution. This suggestion does not affect clean coverage.

**R499-1-R1 | RESIDUE | Docs | The PR body lacks the required template structure.**

Artifact: PR #666 body at review. Authority/evidence: CONTRIBUTING.md section 2.2 names Status, Description, how-to-reproduce, how-to-validate and DoD; the body is unstructured prose. Impact: presentation only; no measurement, verdict or privacy claim changes. Exact fix: use `PR-BODY-residue.md` as the formatting-only replacement. It preserves the existing factual claims; F2 must be resolved separately before those restoration claims are accepted. Verification: compare the replacement's claims with the current body and confirm the five template fields exist. This residue does not affect the verdict or lens coverage.

The requested technical checks produced these results:

- **Response order and intervals:** all 182 selected command/response/unlock triples match controller, listener, input and sequence fields as applicable. Raw responses decode SUCCESS; all selected unlocks decode unsolicited STREAM_INPUT counters with valid ML/MU/SI/SEQ fields and values 1/1/0/0. Every response precedes its selected unlock by 114.984 to 1,098,870.791 microseconds. All 182 table intervals recompute exactly from one capture clock: tap for direction A, controller capture for B. No cross-clock subtraction was used. Earlier omitted frames and baseline selection across a complete capture remain outside the bounded receipt replay.
- **Application rule:** the pinned source's Connected-only unlock selection, five unconditional error flags, initialization and reset handling match the probe for the measured sessions. Primary source [flag selection](https://github.com/kebag-logic/Hive/blob/a13db9d97009dca49a00fb299805e379131dafb3/libs/modelsLibrary/controllerManager.cpp#L730) and cache code at lines 93-104 and 190-214 were compared. The actual probe function equals the function used in the eight controls; the inverted Connected predicate exits 1. All cycle summaries record NotConnected for the unlock update, yielding no unlock error. The complete graphical application's queue/concurrency behavior was not tested.
- **Push boundary design:** source waits for a post-bind callback, then targets an offset around the observed one-second cadence. Forty supplementary trials cover both sides for AAF/CRF in both directions. Reported command offsets are 975.355-980.562 ms after the prior push for the before group and 26.047-29.984 ms for the after group. This brackets the cadence; it is not every fixed hold crossed with both phases. The separate 140 fixed-hold matrix has five trials per requested hold, direction and stream kind. Computation uses the selected capture's clock. Prior-push and bind-response anchor records themselves are absent from the bounded packet, so those summary durations were not independently reconstructed from full captures.
- **Sequence windows and initial PDUs:** all 1,510 published reads are successful with zero SEQ/SI; 546 are scheduled early reads. Each long window has 300 scheduled hold reads and exceeds 600 seconds. Full-stream frame totals of 4,799,477 and 4,798,340, with zero gaps, are published summaries of retained captures, not complete-capture replays by this reviewer. Independently, all 2,184 retained first PDUs pass 2,002 adjacent modulo-256 checks. Yes, these first PDUs should be analyzed; their existing fields suffice to establish this bounded sequence result. Early FRX is still zero on all three reads in 86 cycles; interval-based counters can lag reception, so an early zero alone is not evidence that media was already being observed. Later readbacks and wire sequences are needed alongside it.
- **Restoration:** eight equal summary hashes, 43 claimed observations and the monotonic residuals are consistent across the page and summaries. Independent acceptance remains withheld under F2.
- **Controls:** 14 synthetic wire/status/sequence cases passed, including reversed order, foreign matches, missing push, solicited baseline, unrelated capture clocks, sequence wrap, loss and repetition. Eight extracted-rule controls passed and their predicate mutation failed. Restoration controls found F2. The seven documentation/whitespace checks passed. Their green result does not cover F1's encoded identity field.

Reviewer-owned ledger:

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2) | B12 items 1-5; REQUIREMENTS.md; findings page lines 474-514 and 776-788; decoded wire triples; pinned application rule; restore summaries | R499-1 applied; no clean coverage | bef8dd7036f711bf286929fa4cba6bf724c7118d |
| RTL | CLEAN | Exact base-to-head tree diff; architecture/integration contracts; unchanged required gitlinks; hdl/milan/milan_datapath.sv:5997 and counter wiring; counter implementations for interpreting delayed observations | R499-1 | bef8dd7036f711bf286929fa4cba6bf724c7118d |
| Robustness | UNCLEAN (F2) | wire.py and probe_phase.cpp; 40 boundary trials; first-PDU/long-window receipts; negative selector controls; failed/empty restoration probes | R499-1 applied; no clean coverage | bef8dd7036f711bf286929fa4cba6bf724c7118d |
| Tests | UNCLEAN (F2) | check_wire.py; rule_controls.cpp against both probes; reviewer offline controls; 1,510 counter reads and 182 wire receipts; restore_compare.py | R499-1 applied; no clean coverage | bef8dd7036f711bf286929fa4cba6bf724c7118d |
| Docs | UNCLEAN (F1, F2) | Complete findings page, frozen public scope, PR body, 62 manifest-verified published files, decoded identity fields, documentation receipts | R499-1 applied; no clean coverage | bef8dd7036f711bf286929fa4cba6bf724c7118d |

[R499] PASS RTL - exact source diff and required gitlink/blob verification - this findings-only change introduces no RTL, CDC, reset, width, timing, parameter or interface change. This is scope-specific clean coverage, not fresh hardware or full-regression proof.

Prior public finding reconciliation: after writing the independent verdict and ledger, all public PR reviews, inline comments and conversation comments were fetched. There are zero formal reviews, zero inline comments, and only the two manager review-start notices. Thus no prior public FINDING on PR #666 exists to resolve or retain in that record. Earlier review findings mentioned in the issue concern PR #659, not this PR. `prior-findings-audit.json` records the check and the digest of the independent verdict written before it.

Limits and manager duties: no hardware access, calibration, full source banks, hosted jobs or local workflow replica were run by this reviewer. The assignment reports successful manager source validation at this head; that is distinct from final candidate validation at live dev. Physical calibration is NOT RUN; skipped field or hosted contexts supply no hardware proof. The public primary standards download was unavailable; clause claims were reviewed through frozen public requirements, interface authorities and pinned protocol/application source, not a new full standards audit. Full captures, complete callback logs and restore transactions remain indexed outside the published bounded packet and outside this review's allowed replay inputs. The two timestamp faults remain unattributed. The manager owns publication, finding resolution, both independent approvals, hosted/local acceptance, current-dev candidate validation, authorized merge and post-merge containment. This negative report does not authorize a merge.

Portable checks and raw stdout/exit receipts are in this packet. All disposable files are under scratch/ and excluded from publication. Final verification passed: all 1,802 tracked blobs across the parent and three required submodules match the reviewed objects byte for byte, with exact executable modes and index entries. All required gitlinks match; no tracked source edits or untracked files remain. `integrity-final.log` records the pins and counts. `MANIFEST.sha256` lists every publishable file; scratch/ is excluded.

Reproduction uses only public evidence and disposable local inputs:

```text
python3 audit_receipts.py <published-evidence-root> <candidate-checkout>
python3 offline_probes.py <published-evidence-root> scratch/probes
python3 verify_checkout.py <candidate-checkout>
python3 run_review_checks.py <candidate-checkout> <published-evidence-root> <pinned-markdown-interpreter>
```

The evidence root contains `MANIFEST.json` and `author/`. The combined runner waits for all work in the foreground, with at most four concurrent lightweight checks and a separate log/exit receipt for each. It does not run full source banks or hardware work.

R499-1 FINISHED
