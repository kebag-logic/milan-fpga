[R685] NEGATIVE - exact head c2a080aef7cd9a4ee2cd1bb4f8214b529bfd8c83

Internal cleared-context review R685-2 of issue #775 / PR #777. This round reviews the delta since R685-1's head.
- Head and tree: `c2a080aef7cd9a4ee2cd1bb4f8214b529bfd8c83`, tree `cdba1b2c7fce0d098e8a8858275505932892b072`.
- Previously reviewed head: `c7e87c8c`.
- Source base and live dev: `a032c6d6e3775f145349d5a495c1e1ad12294936`.
- Delta: three one-line commits with no trailers (`50275e29`, `3f5cebd0`, `c2a080ae`) touching four files: `sim_main_nx.cpp`, `format_mutants.py`, `TESTING.md` and comment lines in `KL_avtp_rx_monitor_ctx.sv`.

This is a source review verdict. It is not merge authorization and not hardware acceptance.

**Why NEGATIVE.** Both round-1 findings are resolved at this head, and both of the round-1 defects (lock set, settle step) now fail their named `[SQ]` checks. But the new testing-guide sentence says the mr seed is graded. A reject that only sets or clears the seed survives every avtp_rxmon leg (new F1, MINOR, Tests and Docs). Every other claim in the new guide text was falsified by a planted mutant, and each mutant was caught.

## Reconstruction

Read in order:
1. AGENTS.md and CONTRIBUTING.md (rules for comments, commits, privacy and verification) and docs/README.md.
2. Issue #775: its frozen acceptance criteria, which this round leaves unchanged; the round-2 assignment (issuecomment-6381709748); and the author's round-2 REVIEW READY (issuecomment-6382910697).
3. My own round-1 report (issuecomment-6381703386) and R686-1 (issuecomment-6381645752).
4. `git diff c7e87c8c..c2a080ae` and the commit history.
5. The public receipt tree `15b983df…/review-evidence/775-r1`: `author-r2/receipts/round2/` and my archived round-1 scripts.

I did no new reading of the standard. The ruling recorded on #775 applies as in round 1: an off-format PDU is a received PDU, it advances the sequence state, it counts only UNSUPPORTED_FORMAT, and it presents nothing.

Coverage from round 1 at `c7e87c8c` carries over for every file this delta does not touch: `KL_crf_rx.sv`, the crf_rx and discontinuity harnesses, the lockstep reference, FR_NFR.md, the compliance matrix and `milan_dp`. Nothing in the delta changes what those files depend on.

## Prior findings, checked at this head

### R685-1-F1 (MINOR, Tests, Docs): RESOLVED

**[SQ4]** is at `tb/verilator/avtp_rxmon/sim_main_nx.cpp:1066-1085`.
- `sq_rebind()` re-binds stream 3, so lock, settle and the mr seed clear (`KL_avtp_rx_monitor_ctx.sv:685-691`).
- `[SQ4-0]` checks that the stream is unlocked.
- The off-format PDU arrives first in the era. `[SQ4c]` checks it leaves the stream unlocked, and `[SQ4d]` that it counts no MEDIA_LOCKED.
- `[SQ4f]` checks MEDIA_LOCKED +1 at the first accepted PDU, and `[SQ4g]` that this PDU locks the stream.
- This matches `monst_next_w` at :563-566, which locks on the first accepted PDU of an unlocked stream.

**[SQ5]** is at `:1092-1119`.
- The lock PDU sets settle to `SETTLE_C` = 8 (:237, :565). Seven more PDUs bring it to 1, and `[SQ5-0]` reads `0x11` (media_locked, settle 1).
- The reject comes next. A gap at the next PDU must count nothing, because `seq_mm_w` at :546 needs settle == 0 (`[SQ5c]`). The gap after that must count once (`[SQ5d]`).
- So the window is neither shortened nor restarted.

**The format_mutants.py arms** are at `tb/verilator/avtp_rxmon/format_mutants.py:93-105,130-163,200-205`.
- The `lock set` and `settle step` replacements are byte-identical to my round-1 probe's `lock_set` and `settle_dec`.
- Each arm checks that the reference still carries the same line once (`anchored`).
- The N=4 stack does not compile the reference, and the docstring says so (:22-31).

**Results at this head:**

- **My round-1 `probe_lock_settle.py`** (sha256 `c6924f68…`, the hash the author recorded) was re-run on an extracted copy of the head (`receipts/probe_lock_settle/SUMMARY.txt`).

  | Mutant | NX | Lockstep N=1 / N=8 |
  |---|---|---|
  | `lock_set`, engine and reference | 194 checks, 2 failures: `[SQ4c]` got 1, `[SQ4f]` got 0 | 116/0 and 119/0 (as designed, cannot see it) |
  | `settle_dec`, engine and reference | 3 failures: `[SQ5c]` got 1, `[SQ5d]` got 2, `[SQ5g]` got 2 | 116/0 and 119/0 |
  | either, engine only | as above | fails `[LS]`/`[GC]` |

  This is byte-for-byte the result in the author's `round2/probe_lock_settle/SUMMARY.txt`.
- **Suite run, `make -C tb/verilator/avtp_rxmon`:** `format_mutants.py` 11/11, with `lock set` breaking `[SQ4f]` and `settle step` breaking `[SQ5c]` (`receipts/suite/avtp_rxmon.log`).
- **Restart falsifier (my own probe):** `settle_restart` (the reject writes settle = 8), planted in both copies, fails `[SQ5d]`, `[SQ3b]` and `[SQ5g]`. So the "not restarted" claim is graded too.
- **`lock_clear`**, planted in both copies, fails `[SQ5f]`, `[SQ3b]`, `[SQ5d]` and four existing lock checks (`receipts/probe_sq_claims/SUMMARY.txt`).
- **The guide line `docs/testing/TESTING.md:617`:**
  - It now states the three points of a stream, the counters held at each and the format_mutants arms.
  - It explicitly says "`[SQ]` does not grade the 100 ms silence watchdog across a reject".
  - The round-1 phrase "writes only prev_seq" is gone.
  - Every claim except the mr-seed sentence was checked against a planted mutant; that sentence is new F1 below.

### R685-1-F2 (RESIDUE, Docs): RESOLVED

- `KL_avtp_rx_monitor_ctx.sv:97-99` carries the exact fix text: "it does not compare the channel count with the current format (#765), and its format reject does not advance prev_seq (#775)".
- `:15-23` now places #775 outside the flat contract: "Here, unlike there, a rejected PDU advances the sequence state and affects nothing else (#775)."
- That matches the flat reject path at `KL_avtp_rx_monitor.sv:265-268`, which does not touch prev_seq.
- **No RTL line changed:**
  - My comment-stripping script (`scripts/strip_sv_comments.py`) gives the same hash at `c7e87c8c` and `c2a080ae`: `7c744642…f046`. The base `a032c6d6` differs, as expected (`receipts/static/ctx_comment_strip.txt`).
  - The author's `verilator -E -P` comparison agrees: `026a45f4…`, 804 lines.
  - The reference is not in the delta.

### R685-1-F3 (SUGGESTION, out of scope): RETAINED

The silence watchdog across a reject is still ungraded. The assignment leaves it to the manager, and the guide now discloses it.

### Other reviews

R686-1 raised no finding.

I read the PR's comment list, its submitted reviews (0) and its inline threads (0) only after my verdict and ledger draft were written. No other review exists on this head.

## Findings

### F1 - MINOR - Tests, Docs - the guide says a reject that moves the mr seed is graded; a seed-only move survives every leg

- **Where:**
  - `docs/testing/TESTING.md:617`: "The mr reference and its seed are graded through MEDIA_RESET: a reject that moved either would count a toggle at the next accepted PDU."
  - The same claim in the PR #777 body's round-2 table (the `3f5cebd0` row) and in the REVIEW READY.
  - The stimulus: `tb/verilator/avtp_rxmon/sim_main_nx.cpp:1138-1146` (`sq_in_order`, where every accepted PDU carries the default mr = false, :70) and :1124 (`sq_rebind`).
- **Authority and evidence:**
  - AGENTS.md section 6, Tests lens: a test must be able to fail for the defect it claims to detect. That is the R685-1-F1 requirement: what the guide says `[SQ]` proves must match what it grades.
  - In the RTL, `mr_toggle_w = mr_seeded && (mr != prev_mr)` (:553). A bind clears both prev_mr and mr_seeded (:690-691). Every accepted `[SQ]` PDU carries mr = 0.
  - So a reject that changes only `mr_seeded` never changes a toggle verdict here.
  - Probe `scripts/probe_sq_claims.py`, with each mutant planted in the engine and the reference together (`receipts/probe_sq_claims/SUMMARY.txt`):

    | Mutant (reject write-back) | NX | Lockstep N=1 / N=8 | Verdict |
    |---|---|---|---|
    | `mr_seed_clear`: `{ram_q_r[31:24], 1'b0, ram_q_r[22:8], seq}` | 194/0 | PASS / PASS | survives every leg |
    | `mr_seed_set`: `{ram_q_r[31:24], 1'b1, ram_q_r[22:8], seq}` | 194/0 | PASS / PASS | survives every leg |
    | `mr_prev_from_reject`: prev_mr takes the reject's mr | fails `[SQ2d]`, `[SQ3f]`, `[SQ5i]` | PASS / PASS | caught |
    | `mr_seed_and_ref_from_reject` (round 1's `aaf_mr_seed`) | also fails `[SQ4j]` | PASS / PASS | caught |

- **Impact:** if a later edit to the reject write-back cleared the seed, the next real mr toggle after a reject would reseed silently. MEDIA_RESET would then under-count for that interval (Table 5.6).
  - If an edit instead set the seed on an unseeded stream, a phantom toggle would count when the era's first accepted PDU carries mr = 1.
  - Either way, every check stays green while the guide says the case is graded.
  - The shipping RTL is correct: `{ram_q_r[31:8], seq}` keeps bits 22-23.
- **Required outcome:** the guide and the PR text claim only what `[SQ]` grades. Either of these meets it:
  - **(a) Restrict the sentence.** For example: "A reject that wrote its own mr into the reference would count a toggle at the next accepted PDU (graded through MEDIA_RESET); a reject that only sets or clears the mr seed is not graded."
  - **(b) Grade the seed.** For example:
    - after a reject on a freshly bound stream, the era's first accepted PDU carries mr = 1 and counts no MEDIA_RESET;
    - after a reject on a seeded stream, an accepted PDU with a toggled mr counts MEDIA_RESET once;
    - plus format_mutants arms for the two seed-only defects.

  Either outcome is fine. Because the claim is about what a test grades, this is MINOR and not RESIDUE.
- **Verification:**
  - For (a): read TESTING.md:617 and the PR body against `receipts/probe_sq_claims/SUMMARY.txt`.
  - For (b): re-run `python3 -I scripts/probe_sq_claims.py <tree> <out>`. `mr_seed_clear` and `mr_seed_set` must each fail a named `[SQ]` check, and `make -C tb/verilator/avtp_rxmon` must stay green.

### R1 - RESIDUE - Docs - an odd line wrap in the ctx banner contract

- **Where:** `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:18-19`.
- **What:** "/ per-PDU format\n compare (a rejected\n PDU affects nothing else) /" breaks the parenthetical early. The line is comment only, and the text is correct.
- **Exact fix:** rewrap lines 17-19 as "100 ms silence unlock + interrupt (#762) / per-PDU format compare (a rejected PDU affects nothing else) / counter reset ONLY on that", wrapped at the banner's usual width.

### S1 - SUGGESTION - Tests - format_mutants' two-copy arms check the reference line but do not build it

- **Where:** `tb/verilator/avtp_rxmon/format_mutants.py:93-105,141-149`.
- **What:** the arm verifies that the reference carries the same anchor and grades only the engine copy in the N=4 stack. The claim that the lockstep compare "cannot see" a two-copy defect is argued in the docstring, but no gate runs it.
- **Evidence:** both my probe and the author's run show the lockstep passing 116/0 and 119/0 with both copies planted.
- **Suggestion:** optionally run the lockstep leg on the two planted copies in that arm, so the claim is executable evidence. This has no effect on the verdict.

## Lens results

[R685] PASS Conformance - `KL_avtp_rx_monitor_ctx.sv:546,553,563-568,1009-1021` (unchanged after comment stripping, `receipts/static/ctx_comment_strip.txt`); `sim_main_nx.cpp:1066-1119`; issue #775's frozen criteria - checked against the recorded Table 5.6 ruling.
- The delta changes no RTL line, so every round-1 conformance result at `c7e87c8c` holds for the shipped logic.
- The new arms' expectations follow the ruling and Table 5.6:
  - MEDIA_LOCKED counts at the first accepted PDU, never at a reject (`[SQ4d]`, `[SQ4f]`).
  - The reject counts UNSUPPORTED_FORMAT +1 and presents nothing (`[SQ4a]`, `[SQ4b]`, `[SQ5a]`, `[SQ5b]`, `sq_untouched`).
  - The settle window is the 8-PDU rule (`SETTLE_C`, :237).
- The head passes all of them (NX 194/0).

[R685] PASS RTL - `KL_avtp_rx_monitor_ctx.sv` (diff `c7e87c8c..c2a080ae` is :15-23 and :94-100, comment lines only); `tb/verilator/avtp_rxmon/reference/` (not in the delta); `receipts/gates/lint_rtl.log` (rc 0) - no clock, reset, width, FSM, port or contract change.
- The stripped source of c7e87c8c and c2a080ae is identical (`7c744642…`), and so is the author's preprocessed output (`026a45f4…`).
- The round-1 RTL verdict at `c7e87c8c` stands, re-banked at this head.

[R685] PASS Robustness - `sim_main_nx.cpp:1066-1119,1124-1171`; `receipts/probe_sq_claims/SUMMARY.txt`; `receipts/probe_lock_settle/SUMMARY.txt` - the new boundary points were checked against planted lock and settle defects.
- First in a fresh era (unlocked, unseeded) and the last PDU of the settle window are now covered.
- Shortening (settle_dec), restarting (settle_restart), lock set and lock clear are each caught at a named check.
- The sequence cursor is `uint8_t` with an explicit cast at `[SQ1c]`, so wrap stays exact.
- Each re-bind re-asserts its precondition (`[SQ0]`, `[SQ4-0]`, `[SQ5-0]`).
- Remaining limit: this is targeted coverage, not proof of every coincidence of events. The silence watchdog across a reject is still ungraded (R685-1-F3, retained and disclosed).

[R685] UNCLEAN Tests - `docs/testing/TESTING.md:617`; `sim_main_nx.cpp:1138-1146`; `receipts/probe_sq_claims/SUMMARY.txt` - F1 is open.
- The R685-1-F1 arms are real and fail for the defects they name: `[SQ4f]` for lock set and `[SQ5c]` for settle step, in both copies.
- Clean results: `make -C tb/verilator/avtp_rxmon` rc 0, with flat 97/0, NX 194/0, lockstep 116/0 and 119/0, `lockstep_mutants.py` 14/14 and `format_mutants.py` 11/11 (`receipts/suite/avtp_rxmon.log`); `behave` 14 features, 406 scenarios, 0 failed (`receipts/gates/behave.log`).
- Open: the mr-seed claim is not graded.

[R685] UNCLEAN Docs - `docs/testing/TESTING.md:617`; the PR #777 body's round-2 table; `KL_avtp_rx_monitor_ctx.sv:15-23,94-100` - F1 is open.
- R685-1-F2 is resolved.
- Docs gates I ran: `docs_check.py`, `check_doc_style.py` and `check_doc_paths.py`, all rc 0.
- The delta's source comments state behaviour with issue IDs. They carry no bench lane label, review round, reviewer ID or comment ID.
- Commits are one line with no trailers.

## Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ctx.sv :546,:553,:563-568,:1009-1021 (stripped identical); `[SQ4]`/`[SQ5]` expectations; issue #775 criteria and ruling | R685-2 | c2a080aef7cd9a4ee2cd1bb4f8214b529bfd8c83 |
| RTL | CLEAN | ctx.sv comment-only diff and stripped hash; reference unchanged; lint_rtl rc 0 | R685-2 | c2a080aef7cd9a4ee2cd1bb4f8214b529bfd8c83 |
| Robustness | CLEAN | `[SQ4]`/`[SQ5]` arms; settle_dec/settle_restart/lock_set/lock_clear probes | R685-2 | c2a080aef7cd9a4ee2cd1bb4f8214b529bfd8c83 |
| Tests | UNCLEAN (F1) | sim_main_nx.cpp `[SQ]`; format_mutants.py; suite run; both probe scripts; behave | R685-2 | c2a080aef7cd9a4ee2cd1bb4f8214b529bfd8c83 |
| Docs | UNCLEAN (F1) | TESTING.md:617; PR body; ctx.sv banner; docs gates | R685-2 | c2a080aef7cd9a4ee2cd1bb4f8214b529bfd8c83 |

Files the delta does not touch keep their R685-1 verdicts at `c7e87c8c`: `KL_crf_rx.sv`, the crf_rx and discontinuity harnesses, the reference, FR_NFR.md and the compliance matrix.

## Executions (this round)

All ran with pinned Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`, identity checked; `receipts/env.txt`).
- Builds ran on an extracted copy of the head tree plus the `third_party/verilog-axis` gitlink `48ff7a7e`, under unpublished `scratch/`.
- The clone was never edited.

| Run | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/avtp_rxmon` | rc 0; 97/0, 194/0, 116/0, 119/0, 14/14, 11/11; wall 4:34, max RSS 0.36 GB | receipts/suite/ |
| `probe_lock_settle.py` (round-1 script, unchanged hash) | lock_set, settle_dec caught by NX in both arms | receipts/probe_lock_settle/ |
| `probe_sq_claims.py` (this round) | 4 of 6 caught; mr_seed_clear and mr_seed_set survive | receipts/probe_sq_claims/ |
| Static gates (lint_rtl, cpp/py/sv idiom, hygiene, doc style and paths, docs_check, measure_test_evidence, `git diff --check`) | rc 0 | receipts/gates/rc.tsv |
| check_em_dash | rc 2: cannot judge, the pinned Markdown renderer is absent here; no em dash in any added line | receipts/gates/check_em_dash.log |
| `cd tests && behave --no-capture -f plain` | rc 0; 14 features, 406 scenarios, 1977 steps | receipts/gates/behave.log |
| Evidence audit of 131 downloaded receipts against the public MANIFEST.json | 131 match, 0 mismatch | receipts/evidence_audit.txt |

The one INDEX.md difference, `round2/scripts/route_vivado.sh`, is a path redaction recorded in MANIFEST.json (`path_redacted`). Its published hash matches.

The author's published source-head evidence was verified by hash. These are author executions, not a manager source bank:
- full sweep as four shards: 15+16+17+16 = 64/64 suites, 0 failures, each `complete.json` exit 0 at c2a080ae;
- 30 static gates, rc 0;
- the docs workflow's gates under GNU Make 4.3: 44 steps, 0 failed, with gate_42 and the no-git step skipped;
- the avtp_rxmon suite, rc 0.

Shard 0 lists SKIPPED tsn_fuzz field campaigns, because the tool is absent. Those skips are not proof.

After the probes, the tracked state matches the exact head: `git status --porcelain` is empty, `git diff --quiet HEAD` passes, and the `git ls-files -s` hash and `git submodule status` are identical before and after (`receipts/index.*.sha256`, `receipts/gitlinks.*.txt`). Running the gates left ignored `__pycache__/` directories.

## Real limits

- I did not run the docs workflow's gates under GNU Make 4.3, the full sweep, Yosys, route-1x1, hosted runs or the act replica. The rules forbid them here, or they need the CI container. They are covered by the author's published receipts, checked by hash.
- check_em_dash could not render locally. My own scan found no em dash in any added line.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- The mutation probes are targeted, not exhaustive.

## Pending manager duties

- Validate the current-dev merge candidate (builder and native banks), and run the hosted and act acceptance at the exact head.
- Carry R1 to the residue checklist.
- File R685-1-F3 (the silence watchdog across a reject) as a new issue if it agrees.
- Publish this packet.
- Re-review is needed after F1 is answered.

R685-2 FINISHED
