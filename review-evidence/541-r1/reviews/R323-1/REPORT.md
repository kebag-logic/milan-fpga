[R323] NEGATIVE - exact head 2734b771bcf0b383ea62ef05744452827bafe9e4

# R323-1: external independent review of PR #562 (issue #541)

- Round: R323-1, external independent reviewer, cleared context.
- Exact head: `2734b771bcf0b383ea62ef05744452827bafe9e4`, tree
  `34cb4d208c6681af5405dd4da79fe7c5fe6fbc5e`, one commit on source base
  `5b73d3f47dfed519eb988c13d6beb1db664ef1e0` (live `dev` at review time).
- Diff reviewed: `git diff 5b73d3f4..2734b771`: `hdl/ieee1722/crf/KL_crf_rx.sv`
  (+9/-4, header comment only), `docs/reference/REGISTER_MAP.md` (+1/-1, the
  `CRF_CTRL` row), `tb/verilator/crf_rx/sim_discontinuity.cpp` (+46),
  `tb/verilator/crf_rx/mutants.py` (+3).
- Reconstructed from: AGENTS.md, CONTRIBUTING.md sections 3, 5 and 6,
  docs/README.md (authority order), the issue #541 body and its frozen
  acceptance, decision comment 5827373589, takeover and clause comment
  5827406716, REVIEW READY comment 5827529280, the PR #562 body, and the
  published evidence tree `review-evidence/541-r1` at `a7f7e57a`.

## Verdict

NEGATIVE. There is one open MINOR, filed under the Tests and Robustness
lenses (F1). The RTL is
functionally unchanged: its comment-stripped form is byte-identical to the
base. The corrected header comment and the `CRF_CTRL` row describe the
engine accurately, and the requested lock-retention check and its named
mutant work as claimed. But the PR adds a new documented property: a
validation error "does not refresh the timeout". The decision's safety
argument depends on that property, and nothing in the receiver gate can
fail if it breaks. I built a mutant in which a validation error refreshes
the lock timeout. It survives all three receiver harnesses. A short check
kills it (receipt 06). Conformance, RTL and Docs are CLEAN. Docs
carries one optional SUGGESTION (F2).

## Findings

### F1: MINOR, Tests and Robustness: the new "does not refresh the timeout" claim has no failing arm

- Lenses: Tests and Robustness. My independent pass first filed this under
  Tests only. After my verdict was written I read the prior public round,
  which files the same defect under Tests and Robustness (see "Prior public
  review findings" below). The ungraded case is exactly malformed input on
  a timeout path, both of which the Robustness lens names. AGENTS.md
  section 6 says a finding attributable to more than one lens is recorded
  under each, so this round records it under both. The verdict is
  NEGATIVE either way.
- Location: `tb/verilator/crf_rx/sim_discontinuity.cpp:180-224`
  (`locked_validation_error`) and `tb/verilator/crf_rx/mutants.py:19-31`,
  measured against the claim added at `hdl/ieee1722/crf/KL_crf_rx.sv:38-39`
  and `docs/reference/REGISTER_MAP.md:837` ("It does not refresh the
  timeout"). The claim is implemented at `KL_crf_rx.sv:531-533`, where the
  timeout reset is gated by `w_acc_run_w` only.
- Authority and evidence:
  - AGENTS.md section 6, Tests lens: each test must be able to fail for
    the defect it claims to detect, and positive, negative and boundary
    behaviour must be covered. Section 5 requires tests for changed
    behaviour.
  - The #541 decision (comment 5827373589) sets the contract: "a CRF sink
    unlocks only after 100 ms without valid PDUs". It justifies keeping
    lock with "the timeout already bounds how long invalid data can be
    followed". That bound holds only if rejects do not refresh the
    timeout.
  - In the new check, the silence phase is measured from a valid resume
    PDU (`sim_discontinuity.cpp:209-221`). No shipped case follows a
    locked sink's last accepted PDU with validation-error PDUs alone.
  - I ran the mutant `uf_refreshes_timeout`, which changes
    `if (w_acc_run_w) begin` to `if (w_acc_run_w || w_ev_uf_w) begin` at
    `KL_crf_rx.sv:531`. It builds and passes unit (13,836 checks),
    discontinuity (1,932 checks) and talker_step (69 checks), all rc=0
    (receipt 03). It is not one of the campaign's mutants.
  - Its contrast control, the clean build, passes the same three harnesses
    (receipts 03 and 04).
- Impact: a regression in which malformed PDUs keep a locked CRF sink
  locked indefinitely would pass the whole receiver gate, including the
  new check. Under that regression the sink reports lock with no valid
  timing arriving, and MEDIA_UNLOCKED never counts. That defeats the
  decided contract and the bound the decision relies on, while the header
  and register map keep saying the opposite.
- Required outcome: a `tb/verilator/crf_rx` check in which a LOCKED sink,
  after its last accepted PDU, receives only validation-error PDUs. It must
  grade lock retained before 100 ms, lock cleared at 100 ms, and exactly
  one MEDIA_UNLOCKED event. The campaign must also carry a mutant in which
  a validation error refreshes the timeout, and that mutant must fail the
  named check. The RTL needs no change.
- Verification: receipt 06 shows the check is feasible without touching
  the RTL. I appended a 25-line reviewer probe to a scratch copy of the
  discontinuity harness. At head it passes: 2,194 checks, 0 failures,
  including "probe: reject-only stream still unlocks at 100 ms". Under
  `uf_refreshes_timeout` it fails exactly "probe: reject-only stream still
  unlocks at 100 ms" and "probe: that unlock is one MEDIA_UNLOCKED event".
  A re-review runs the author's new check and mutant the same way.

### F2: SUGGESTION, Docs: the testing index does not name the new mutant

- Lenses: Docs.
- Location: `docs/testing/TESTING.md:463`.
- Evidence: the `crf_rx` row lists the default-gate mutants as "tu, jump,
  refill, sample-edge and servo-validity". Since this head the gate also
  carries `validation_error_unlocks` and the locked-sink validation-error
  check (receipt 01: nine controls).
- Impact: none on correctness. A reader of the index does not learn that
  lock retention is gated.
- Outcome (optional): name the validation-error lock mutant in that row.
  Not required for coverage.

## Per-lens results (clean lenses carry artifact evidence)

- [R323] PASS Conformance - issue #541 acceptance 1-3; Milan v1.2 5.3.8.10 /
  Table 5.6; IEEE 1722-2016 10.6 and 10.7; `KL_crf_rx.sv:531-565`;
  receipts 01 and 10.
  - AC1: the clause is recorded publicly (5827406716 and the published
    `CLAUSE-EVIDENCE.md`). My reading agrees. Table 5.6 leaves
    "synchronized" and "unsynchronized" to the manufacturer, and constrains
    only the MEDIA_LOCKED / MEDIA_UNLOCKED pair relation. UNSUPPORTED_FORMAT
    is an interval counter and does not touch lock state. Clause 10.6 lets
    the media clock free-wheel through missing CRF timestamps. Nothing
    requires unlock on a validation error, so the stop condition is not met
    and the 100 ms timeout stands as implementation policy.
  - AC2: the RTL, header and row agree. The locked-sink check fails under
    the named mutant: `validation_error_unlocks` rc=1, "[FAIL] validation
    error preserves established lock" (receipt 01).
  - AC3: exact-head hosted contexts executed green: `rtl-fast`,
    `verilator-suites`, `yosys-portability`, 5/5 Verilator shards and 4/4
    Yosys shards. Physical gPTP was skipped, which proves nothing
    (receipt 10).
  - The pair invariant is preserved: a reject scores neither a lock nor an
    unlock event.
- [R323] PASS RTL - `hdl/ieee1722/crf/KL_crf_rx.sv` at base and head, and
  `hdl/milan/milan_datapath.sv:2574-2575,3556,5506` with
  `hdl/common/csr/milan_csr.sv:2355-2358`; receipts 02 and 12.
  - The comment-stripped RTL is IDENTICAL: sha256 `f0081e18...` at both
    commits, 278 code lines, scanner aware of string literals. The only
    hunk is header lines 34-42.
  - I checked the new header text against the implementation:
    - Lock needs `settle_r` to reach 7 plus one more consumed accept, which
      is 8 PDUs (`:575-581`).
    - Timeout reset happens on `w_acc_run_w` only (`:531-533`).
    - A reject clears only `settle_r` (`:560-565`).
    - The count folds into the interval (`:374,480-481,503`).
    - `fmt_err_o[7:0]` reaches CRF_STATUS[15:8], and the full 32 bits reach
      GET_COUNTERS offset 32.
  - No width, reset, FSM or CDC change.
- [R323] MINOR Robustness - `KL_crf_rx.sv:374,480-481,503,531-565`;
  receipts 03, 05 and 06. UNCLEAN under F1.
  - Malformed input on a locked sink, at head: lock is held on the reject
    edge and through the interval commit. A reject-only stream still
    unlocks at 100 ms with exactly one unlock event (probe 06, head leg).
    There is no phantom FRAMES_RX, lock or unlock event.
  - Repeated rejects in one interval count once (existing unit case "5
    malformed: ONE interval tick"). Resumption needs no new lock event.
  - Reviewer mutants that violate these behaviours are all killed:
    - `uf_unlock_at_commit`, `uf_unlock_counted`,
      `uf_uncounted_when_locked` and `uf_scores_lock_event` die in unit and
      discontinuity.
    - `uf_flags_frames_rx` dies in unit and discontinuity (receipt 05).
    - `uf_keeps_settle` dies in unit.
  - The shipped RTL behaviour is correct. The malformed-only timeout path
    has no graded regression (F1), so this lens is not covered clean at
    this head.
- [R323] MINOR Tests - `tb/verilator/crf_rx/sim_discontinuity.cpp:180-224`,
  `tb/verilator/crf_rx/mutants.py:19-31`; receipts 01 and 03-06.
  - What works:
    - The new check starts LOCKED (precondition asserted, one lock event).
    - It grades lock at the rejection edge and through the commit, the
      single UNSUPPORTED_FORMAT count, no FRAMES_RX, no lock or unlock
      event, no recount, resumption, and silence at 19,992 cycles (held)
      and 20,012 cycles (cleared, one unlock). The engine unlocks at the
      20,001st idle edge, so the bracket is honest.
    - The named mutant fails that check. The campaign passes 9/9.
    - The existing #546 legs stay green: unit 13,836/0, discontinuity
      1,932/0, talker_step 69/0, and servo 85/8/113 with 0 failures
      (receipts 01 and 09).
  - Open: F1.
- [R323] PASS Docs - `hdl/ieee1722/crf/KL_crf_rx.sv:34-42`,
  `docs/reference/REGISTER_MAP.md:837`; receipts 07, 08 and 12.
  - Both texts now state the timeout-based unlock and exactly what a
    validation error does: it breaks settling, retains lock, does not
    refresh the timeout, and counts once per interval through `fmt_err_o`,
    with the GET_COUNTERS (32-bit) and CRF_STATUS[15:8] views. Each clause
    is checked against the RTL lines listed under RTL.
  - The unsupported "delta jitter within window" lock condition was
    correctly removed. No current (non-history) page repeats the old
    claim; the only survivor is the obsolete `docs/history/v1` page.
  - The docs, em-dash, doc style, TOC, anchor, doc-path, C++ and Python
    idiom gates all pass, and `git diff --check` is clean. The added lines
    contain no U+2014 and no non-ASCII bytes.
  - F2 is a SUGGESTION only.

## Completion ledger (reviewer-owned)

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #541 AC1-3 and decision 5827373589; clause record 5827406716 / `CLAUSE-EVIDENCE.md`; Milan v1.2 5.3.8.10 Table 5.6, 7.3.2-7.3.4; IEEE 1722-2016 10.6/10.7; `KL_crf_rx.sv:531-581`; hosted contexts (receipt 10) | R323-1 | `2734b771bcf0b383ea62ef05744452827bafe9e4` |
| RTL | CLEAN | `KL_crf_rx.sv` comment-stripped base vs head (receipt 02); `KL_crf_rx.sv:309-316,374,477-509,529-609`; `milan_datapath.sv:2574-2575,3556,5506`; `milan_csr.sv:2355-2358` | R323-1 | `2734b771bcf0b383ea62ef05744452827bafe9e4` |
| Robustness | UNCLEAN (F1 open) | `KL_crf_rx.sv:374,480-481,503,531-565`; reviewer mutants and probe (receipts 03-06) | R323-1 | `2734b771bcf0b383ea62ef05744452827bafe9e4` |
| Tests | UNCLEAN (F1 open) | `sim_discontinuity.cpp:1-224`; `mutants.py:1-123`; `sim_main.cpp:186-191,440-470,600-652`; `Makefile`; receipts 01, 03-06, 09 | R323-1 | `2734b771bcf0b383ea62ef05744452827bafe9e4` |
| Docs | CLEAN (F2 SUGGESTION only) | `KL_crf_rx.sv:34-44`; `REGISTER_MAP.md:822-845`; `docs/testing/TESTING.md:463`; repository sweep (receipt 12); doc gates (receipts 07, 08) | R323-1 | `2734b771bcf0b383ea62ef05744452827bafe9e4` |

## Real limits

- Primary standards text: no copy of Milan v1.2 or IEEE 1722-2016 was
  available in a location this round may read. My clause reading is my
  own reading of those clauses, cross-checked against two things: the
  executor's published excerpts, and the independent, pre-existing in-tree
  quotation of the analogous Milan "left open to each manufacturer" wording
  (`hdl/milan/milan_datapath.sv:3430`, cited there as 5.3.11.2). I did not
  re-compare the quoted bytes against the printed pages.
- Simulation used the pinned Verilator 5.050 wrapper, with builds capped
  at 8 jobs by a reviewer wrapper (receipt 00). Harness builds ran from
  `git archive` extractions of the exact head under the scratch directory.
  The clone was used only for the static documentation gates.
- Receipt 04 was stopped by the 590 s cap after `uf_unlock_counted`'s
  discontinuity leg. Its talker_step leg did not run, which does not matter
  because unit and discontinuity already killed it. `uf_flags_frames_rx`
  was rerun alone to completion (receipt 05). Receipt 03's
  `uf_unlock_counted` unit leg failed to link on a transient full disk and
  is superseded by receipt 04. Receipt 03's `uf_counts_frames_rx` touched
  only the tick-cycle term and is a near-equivalent mutant. I discarded it
  as a reviewer design error, and it is not evidence for F1.
- Three Markdown gates need the pinned renderer, so they ran under the
  prepared `md-venv` interpreter (receipt 08).
- Not run, by assignment: the full parent, PP, gPTP, Yosys and builder
  banks, `milan_dp`, Docker/act, and hardware. Physical calibration was NOT
  RUN. The hosted "Physical gPTP" context is skipped, and skipped field
  contexts are not hardware proof.
- The `external` submodule is uninitialised in this clone. I did not touch
  it. The required processor gitlinks match their checkouts (receipt 11).

## Clone integrity after probes

Receipt 11, taken after I removed the Python bytecode caches that my own
gate runs had created:

- HEAD is `2734b771...` and the tree is `34cb4d20...`.
- The index holds 893 stage-0 records, equal to the HEAD tree.
- All 889 tracked regular files re-hash to their blobs, and the modes
  match.
- No untracked or ignored residue remains.
- The gitlinks are `gptp-processor e5dcea6e`, `protocol-processor 09f9bf38`,
  `third_party/verilog-axis 48ff7a7e` and `external efeb541a`
  (uninitialised).

## Pending manager duties

- The candidate merge build on current `dev` at the merge turn. The source
  base and live `dev` were both `5b73d3f4` during this round.
- Hosted and act acceptance. The combined commit status reads `pending`
  with zero legacy statuses; the check runs themselves concluded.
- Route F1 (the same defect as R322-1-F1) to the executor, and re-review
  at the fix head. That re-review must re-cover Tests and Robustness.
- A fix that touches only `tb/verilator/crf_rx/` leaves Conformance, RTL
  and Docs banked at this head. A change to `KL_crf_rx.sv` or
  `REGISTER_MAP.md` un-covers the lenses whose scope it touches.
- The physical calibration and field evidence owed by #117. That is not
  part of this lane.

## Prior public review findings on this PR

I read these only after my verdict and ledger above were written.

- The only prior round is R322-1: PR comment 5827859729, NEGATIVE at this
  same head. It has no PR reviews and no inline comments. It reports no
  earlier findings.
- R322-1-F1 (MINOR, Tests and Robustness): the timeout-refresh-on-reject
  gap is ungraded. RETAINED at this head.
  - It is the same defect as this round's F1, reached independently. R322's
    mutant P2 widens `w_acc_run_w` to `w_hit`. Mine widens the timeout
    reset to `w_acc_run_w || w_ev_uf_w`. Both survive, and both probes pass
    at head.
  - I adopt R322's lens pair, as explained under F1.
  - R322 also asks for a correction to the new check's comment at
    `sim_discontinuity.cpp:182` ("only silence expires lock"). I concur and
    fold it into F1's outcome. The accurate rule is: lock expires after
    100 ms without a consumed accepted PDU, and rejects do not count.
- R322-1-S1 (SUGGESTION, Docs): the `CRF_CTRL` row omits "consumed while
  started" on the lock rule. It also omits that a bind edge or a reset
  clears lock without scoring MEDIA_UNLOCKED. RETAINED as an optional
  SUGGESTION. I confirmed the omissions against `KL_crf_rx.sv:571-581` and
  `:619-670`. The header is complete and the row is not wrong, so this has
  no effect on coverage.
- R322 did not see the `verilator-suites` or `yosys-portability`
  aggregates in its snapshot. This round observed both concluded `success`
  on the exact head, with Verilator shards 0-4 all `success` (receipt 10).
  This is evidence only; acceptance stays with the manager.

R323-1 FINISHED
