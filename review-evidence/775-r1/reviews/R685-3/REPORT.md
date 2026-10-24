[R685] POSITIVE - exact head 220b51f2eb50c32f830e0b5a8ee1ce138b218bb6

Internal cleared-context review R685-3 of issue #775 / PR #777. This round reviews the delta since R685-2's head.

- Head and tree: `220b51f2eb50c32f830e0b5a8ee1ce138b218bb6`, tree `a4bc2ed645a1cc426a2e83d1773c3c5e2ccb5405`.
- Previously reviewed head: `c2a080aef7cd9a4ee2cd1bb4f8214b529bfd8c83`.
- Source base and live dev: `a032c6d6e3775f145349d5a495c1e1ad12294936`.
- Delta: four one-line commits with no body or trailers (`a8ddb31a`, `de094b8a`, `db5d9d27`, `220b51f2`). They touch five files:
  - `sim_main_nx.cpp`, `format_mutants.py` and `Makefile` (comment only) in the avtp_rxmon harness;
  - `TESTING.md`;
  - comment lines in `KL_avtp_rx_monitor_ctx.sv`.

  No RTL line changes.

This is a source review verdict. It is not merge authorization and not hardware acceptance.

**Why POSITIVE.** Every named prior finding is resolved at its cause:
- **Both planted copies are now built.** The two-copy arms write the planted engine and the planted reference. The N=4 stack compiles the planted engine, and both lockstep shapes compile both planted files; Verilator's dependency files show this.
- **The mr seed is now graded.** `[SQ6]` and `[SQ7]` grade it on both sides. My round-2 probe now catches 6 of 6 mutants, where it caught 4.
- **The banner change is whitespace only.** The ctx file is byte-identical after collapsing whitespace.
- **The sweep tally counts only the shipping tree.** It reads 577 checks from the avtp_rxmon log, which is the shipping tree's count.

I found no defect in the new tests or in the RTL. One RESIDUE (wording in a Makefile comment) and one optional SUGGESTION follow.

## Reconstruction

Read in order:
1. AGENTS.md and CONTRIBUTING.md, for the rules on comments, commits, privacy and verification, and docs/README.md.
2. Issue #775: its frozen acceptance criteria, unchanged since round 1, and the recorded Table 5.6 ruling. An off-format PDU is a received PDU: it advances the sequence state, counts only UNSUPPORTED_FORMAT and presents nothing.
3. The round-3 assignment (issuecomment-6383212982).
4. My own round-2 report R685-2 (issuecomment-6383207659) and R686-2 (issuecomment-6383208690).
5. `git diff c2a080ae..220b51f2` and the commit history.
6. The public evidence tree `36b5ada0…/review-evidence/775-r1` (`author-r3/receipts/round3/`) and the author's round-3 REVIEW READY (issue #775, issuecomment-6385323298).

I did no new reading of the standard.

**Carried-over coverage.** Coverage from rounds 1 and 2 carries over for every file this delta does not touch: `KL_crf_rx.sv`, the crf_rx and discontinuity harnesses, the lockstep reference, FR_NFR.md, the compliance matrix and `milan_dp`. Nothing in the delta changes what those files depend on. The ctx engine is unchanged after comment stripping, and the reference is not in the delta.

**Evidence packet.** The evidence commit is not signed. I verified its `MANIFEST.json` instead:
- 2490 entries, and every `published_sha256` matches.
- No listed file is missing, and no file is unlisted.
- The archived reviewer scripts under `reviews/R685-2/scripts/` carry the hashes the author recorded (`probe_sq_claims.py` `02ba41f2…`, `probe_lock_settle.py` `c6924f68…`, `strip_sv_comments.py` `0146ba3c…`).

Receipt: `receipts/env_and_evidence.txt`.

## Prior findings, checked at this head

### R686-2-F1 (MINOR, Conformance, Tests, Docs), with R685-2-S1 (SUGGESTION, Tests): RESOLVED

**The arm at `tb/verilator/avtp_rxmon/format_mutants.py:99-122,189-221`.** `run_pair` fills one reject write-back template (`REJECT_WB`, :101) with each copy's bundle (`cur_w` and `cur_r`).
- It requires that line exactly once in each copy (`anchored`). It then writes `KL_avtp_rx_monitor_ctx_<tag>.sv` and `KL_avtp_rx_monitor_ctx_ref_<tag>.sv`.
- It builds the N=4 stack from the planted engine; that stack compiles no reference. The arm is caught when that stack fails its named check.
- It builds the lockstep leg through `lockstep_mutants.build(engine, mdir, reference)`, which runs `make lockstep-build RXMON_SRC= REF_SRC= LS_MDIR=`. The result is printed as measured.

**My falsifier, `scripts/probe_pair_inputs.py`.** It runs the committed `run_pair` with a kept work directory and logs each `make` it issues. Receipts: `receipts/pair_inputs/lock_set.txt` and `mr_seed_clear.txt`.
- Each planted copy differs from its source in exactly one line: engine :1020, reference :992.
- Verilator's `*__ver.d` dependency files show what each build compiled:

  | Build | Sources compiled |
  |---|---|
  | NX | `KL_avtp_rx_monitor_ctx_<tag>.sv` only |
  | Lockstep N=1 and N=8 | `KL_avtp_rx_monitor_ctx_<tag>.sv` and `KL_avtp_rx_monitor_ctx_ref_<tag>.sv` |

So both copies are really planted and built.

**The text.** The driver's messages, its docstring at :22-36, the `TESTING.md:617` sentence and the PR body's round-3 table each describe exactly this:
- the N=4 stack is built from the planted engine and must fail its named `[SQ]` check;
- the lockstep is built from both copies and its result is printed and not graded.

**Byte identity.** The lock set and settle step replacements are byte-identical, for both bundles, to the round-1/2 probe's `lock_set` and `settle_dec` (`receipts/static/mutant_bytes.txt`).

### R685-2-F1 (MINOR, Tests, Docs): RESOLVED

**The RTL.** MON_STATE bit 22 is prev_mr and bit 23 is mr_seeded (`KL_avtp_rx_monitor_ctx.sv:56-58`). `mr_toggle_w = mr_seeded && (mr != prev_mr)` (:552). An accepted PDU writes `[22] = mr` and `[23] = 1` (:559-560). So `(lctx_rd(3, 8) >> 22) & 3` reads {seed, ref}.

**[SQ6]** is at `sim_main_nx.cpp:1124-1148`.
- `sq_rebind()` re-binds the stream. `[SQ6-0]` checks that the seed and reference read 0.
- The reject carries mr = 1 (`sq_off_format`, :1215). `[SQ6c]` checks that the seed and reference still read 0.
- The era's first accepted PDU then carries mr = 1. `[SQ6e]` checks that it counts no MEDIA_RESET, and `[SQ6f]` that the field then reads 3.
- Nine more PDUs follow with mr held. `[SQ6h]`-`[SQ6k]` check UNSUPPORTED_FORMAT +1, the other counters unchanged, and FRAMES_RX 10.

**[SQ7]** is at `:1150-1181`.
- Nine PDUs with mr = 0 lock, settle and seed the stream. `[SQ7-0]` checks that the field reads 2.
- The reject carries mr = 1. `[SQ7c]` checks that the field still reads 2.
- The next accepted PDU carries mr = 1. `[SQ7d]` checks that it counts MEDIA_RESET +1.
- Three more PDUs follow with mr held. `[SQ7e]` checks that MEDIA_RESET is still +1 in all, and `[SQ7f]` that 13 PDUs are accepted.

`sq_in_order` gained `bool mr = false` (:1200-1209), so existing callers are unchanged. No check name collides.

**Byte identity.** The format_mutants arms `mr seed set` and `mr seed clear` are byte-identical to my probe's `mr_seed_set` and `mr_seed_clear`, for both bundles (`receipts/static/mutant_bytes.txt`).

**Results at this head.**
- **Re-run `probe_sq_claims.py`** (archived script, unchanged hash): 6 of 6 caught, each planted in the engine and the reference together. My `SUMMARY.txt` is byte-identical to the author's round-3 `SUMMARY.txt` (sha256 `b592b3dd…`).

  | Mutant (engine and reference) | NX failures | Lockstep N=1 / N=8 |
  |---|---|---|
  | `mr_seed_set` | `[SQ6c]` got 2, `[SQ6e]` got 1, `[SQ6i]` | PASS / PASS |
  | `mr_seed_clear` | `[SQ7c]` got 0, `[SQ7d]` got 0, `[SQ7e]` | PASS / PASS |
  | `mr_prev_from_reject` | `[SQ2d]`, `[SQ3f]`, `[SQ5i]`, `[SQ6c]`, `[SQ7c]`-`[SQ7e]` | PASS / PASS |
  | `mr_seed_and_ref_from_reject` | 8 failures, including `[SQ4j]` and `[SQ6c]` | PASS / PASS |
  | `settle_restart` | `[SQ3b]`, `[SQ5d]`, `[SQ5g]` | PASS / PASS |
  | `lock_clear` | 7 failures, including `[SQ5f]` | PASS / PASS |

  At `c2a080ae` the first two survived every leg.
- **The new guide sentence at `TESTING.md:617`:** "a reject that sets the mr seed, clears it, or writes its own mr into the reference is graded through MEDIA_RESET". Each of the three is now caught at a MEDIA_RESET check: `[SQ6e]`, `[SQ7d]`, and `[SQ2d]`/`[SQ3f]`/`[SQ5i]`.
- **The guide's other counts are true:** "five points", "seven #775 defects", and five compare defects + seven + the control = 13.

### R685-2-R1 (RESIDUE, Docs): RESOLVED

**The rewrap.** `KL_avtp_rx_monitor_ctx.sv:17-21` now reads "100 ms silence unlock + interrupt (#762) / per-PDU format compare (a rejected PDU affects nothing else) / counter reset ONLY on that stream's …". That is the requested rewrap.

**The proof that only whitespace moved** (`receipts/static/ctx_comment_strip.txt`):

| Comparison | `c2a080ae` | `220b51f2` |
|---|---|---|
| Whole file, whitespace collapsed | `551dc9f7…` | `551dc9f7…` |
| `strip_sv_comments.py` (804 lines) | `7c744642…f046` | `7c744642…f046` |
| `verilator -E -P` | `026a45f4…` | `026a45f4…` |

The base `a032c6d6` strips to a different hash (`73072f6b…`), as expected.

### Commit 220b51f2's tally fix: VERIFIED

**The cause.** At `db5d9d27` the pair arms printed the lockstep harness's own `== avtp_rxmon lockstep N=1: checks: 116 failures: 0 ==` line. `scripts/suite_tally.py`'s `checks-colon-failures-colon` shape counts that line as a check tally.

**The fix.** `220b51f2` restates it as `N=1 116/0, N=8 119/0 (checks/failures)` (`format_mutants.py:104,214-220`). No SHAPE or `TALLY_SHAPED` pattern matches that form.

**The check** (`scripts/tally_probe.py`), feeding logs through the tree's own `suite_tally.scan` (`receipts/suite/tally.txt`):

| Log | Checks read | Unparsed |
|---|---|---|
| My suite log at this head | 577 = 97 + 218 + 116 + 119 + 14 + 13 | 0 |
| Author's superseded `db5d9d27` log | 1041 (the extra 464 = 4 × 116 are the pair lines) | 0 |

**The sweep.** The four shards report 15 + 16 + 17 + 16 = 64 suites and 54,074 + 331,530 + 262,066 + 1,541,998 = 2,189,668 checks. That is +26 over round 2, exactly NX +24 and format_mutants +2.

### R685-1-F3 (SUGGESTION, out of scope): RETAINED

The 100 ms silence watchdog across a reject is still ungraded. The guide discloses this ("`[SQ]` does not grade the 100 ms silence watchdog across a reject"). The assignment leaves it to the manager.

### Other reviews

I read the PR's submitted reviews (0), inline threads (0) and verdict lines only after my verdict and ledger were drafted. No other round-3 report existed on the PR when I checked.

## Findings

### R1 - RESIDUE - Docs - the Makefile comment's "which" reads as if the N=4 stack builds the lockstep leg

- **Where:** `tb/verilator/avtp_rxmon/Makefile:47-49`: "RXMON_SRC and NX_MDIR do the same for format_mutants.py and the N=4 stack (#765), which for #775's two-copy defects also builds this leg from a mutated engine and reference."
- **What:** the nearest antecedent of "which" is "the N=4 stack". But it is `format_mutants.py` that builds the lockstep leg, as the docstring and `run_pair` show. This is comment wording only; no recipe, measurement or claim changes.
- **Exact fix:** "RXMON_SRC and NX_MDIR do the same for format_mutants.py and the N=4 stack (#765); for #775's two-copy defects format_mutants.py also builds this leg, through RXMON_SRC, REF_SRC and LS_MDIR, from a mutated engine and reference."

### S1 - SUGGESTION - Tests - the pair's lockstep result could act as a symmetry anchor

- **Where:** `format_mutants.py:211-221`.
- **What:** the arm prints the lockstep result on the pair and does not grade it, as the assignment asks. Symmetry is already guaranteed by construction: one template and one anchor per copy. So this is optional.
- **Suggestion:** if a later edit ever plants the copies differently, a non-zero lockstep rc on the pair is the signal. A one-word marker on that line, such as "asymmetric?" when rc != 0, would make it visible. It has no effect on the verdict.

## Lens results

[R685] PASS Conformance - `KL_avtp_rx_monitor_ctx.sv:552,559-560,1020` (unchanged after comment stripping, `receipts/static/ctx_comment_strip.txt`); `sim_main_nx.cpp:1124-1181`; the issue #775 ruling and Table 5.6 - the new arms' expectations were checked against the recorded rule.
- The era's first accepted PDU only seeds the mr reference and counts no MEDIA_RESET (`[SQ6e]`).
- A toggle against a seeded reference counts once (`[SQ7d]`), and a held mr counts nothing (`[SQ7e]`).
- The reject counts UNSUPPORTED_FORMAT +1 and presents nothing (`[SQ6a]`, `[SQ6b]`, `[SQ6h]`, `[SQ7a]`, `[SQ7b]`, `[SQ7h]`).
- The shipping RTL passes them all (NX 218/0).
- The round-2 task contract (R686-2-F1) is now met by the committed driver.

[R685] PASS RTL - `KL_avtp_rx_monitor_ctx.sv` (diff `c2a080ae..220b51f2` is :17-21, comment whitespace only); `tb/verilator/avtp_rxmon/reference/` (not in the delta); `receipts/gates/lint_rtl.log` - no clock, reset, width, FSM, port or contract change.
- Whitespace-collapsed, comment-stripped and preprocessed hashes are all equal across `c2a080ae` and `220b51f2`.
- `lint_rtl.py --check` rc 0 (89 <= 89).
- The round-1 RTL verdict stands, re-banked at this head.

[R685] PASS Robustness - `sim_main_nx.cpp:1124-1181`; `receipts/probe_sq_claims/SUMMARY.txt` - both sides of the mr seed boundary are covered.
- Covered: unseeded first in a fresh era, and seeded with reference 0.
- Each re-bind re-asserts its precondition (`[SQ6-0]`, `[SQ7-0]`).
- Seed set, seed clear, reference-from-reject, settle restart and lock clear are each caught at a named check.
- Remaining limit: this is targeted coverage, not proof of every coincidence of events. The silence watchdog across a reject is still ungraded (R685-1-F3, retained and disclosed).

[R685] PASS Tests - `format_mutants.py:99-122,169-221`; `sim_main_nx.cpp:1124-1209`; `receipts/suite/avtp_rxmon.log`; `receipts/pair_inputs/`; `receipts/probe_sq_claims/`; `receipts/gates/behave.log` - every new arm was checked against a planted defect.
- **Each new arm fails for the defect it names:** mr seed set fails `[SQ6e]`, and mr seed clear fails `[SQ7d]`.
- **The two-copy arms build what they claim** (dependency files).
- **`make -C tb/verilator/avtp_rxmon`:** rc 0 with flat 97/0, NX 218/0, lockstep 116/0 and 119/0, `lockstep_mutants.py` 14/14 and `format_mutants.py` 13/13 (wall 5:46, max RSS 0.36 GB).
- **`behave`:** 14 features, 406 scenarios, 1977 steps, 0 failed.
- **The sweep tally** now counts only the shipping tree's checks.
- **Existing regressions:** `[SQ0]`-`[SQ5]` stay green, and the `sq_in_order` default keeps their stimulus unchanged.

[R685] PASS Docs - `docs/testing/TESTING.md:617`; `format_mutants.py:5-36`; the PR #777 body (round-3 section and validation); `KL_avtp_rx_monitor_ctx.sv:17-21`; `receipts/gates/rc.txt` - the text describes what is graded and built, and each claim was checked against a probe or receipt.
- `docs_check.py`, `check_doc_style.py` and `check_doc_paths.py`: rc 0.
- The delta's source comments state behaviour with issue IDs. They carry no bench lane label, review round, reviewer ID or comment ID.
- Commits are one line with no trailers.
- R1 above is RESIDUE and leaves the lens clean.

## Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ctx.sv :552,:559-560,:1020 (stripped identical); `[SQ6]`/`[SQ7]` expectations; #775 ruling; round-2 assignment item 1 met | R685-3 | 220b51f2eb50c32f830e0b5a8ee1ce138b218bb6 |
| RTL | CLEAN | ctx.sv whitespace-only diff and three hashes; reference unchanged; lint_rtl rc 0 | R685-3 | 220b51f2eb50c32f830e0b5a8ee1ce138b218bb6 |
| Robustness | CLEAN | `[SQ6]`/`[SQ7]` boundary arms; six-mutant probe | R685-3 | 220b51f2eb50c32f830e0b5a8ee1ce138b218bb6 |
| Tests | CLEAN | sim_main_nx.cpp `[SQ]`; format_mutants.py run_pair; pair-input falsifier; suite run; probe; behave; tally probe | R685-3 | 220b51f2eb50c32f830e0b5a8ee1ce138b218bb6 |
| Docs | CLEAN (RESIDUE R1 carried) | TESTING.md:617; driver docstring and messages; Makefile:47-49; PR body; ctx.sv banner; docs gates | R685-3 | 220b51f2eb50c32f830e0b5a8ee1ce138b218bb6 |

Files the delta does not touch keep their R685-1 verdicts at `c7e87c8c`: `KL_crf_rx.sv`, the crf_rx and discontinuity harnesses, the reference, FR_NFR.md and the compliance matrix. Nothing in this delta touches their scope.

## Executions (this round)

All ran with pinned Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`, identity checked; `receipts/env_and_evidence.txt`).
- Builds ran on extracted copies of the head tree plus the `third_party/verilog-axis` gitlink `48ff7a7e`, under unpublished `scratch/`.
- The gates ran read-only in the clone.

| Run | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/avtp_rxmon` | rc 0; 97/0, 218/0, 116/0, 119/0, 14/14, 13/13 | receipts/suite/ |
| `probe_sq_claims.py` (archived, hash `02ba41f2…`) | 6 of 6 caught; byte-identical to the author's SUMMARY | receipts/probe_sq_claims/ |
| `probe_pair_inputs.py` (lock set, mr seed clear) | both copies planted; NX compiles the planted engine; lockstep compiles both | receipts/pair_inputs/ |
| `tally_probe.py` | 577 at head; 1041 at superseded `db5d9d27` | receipts/suite/tally.txt |
| comment strip / preprocess / whitespace hash | equal across `c2a080ae` and `220b51f2` | receipts/static/ctx_comment_strip.txt |
| `compare_mutants.py` | four two-copy replacements byte-identical to the reviewer probes | receipts/static/mutant_bytes.txt |
| behave; lint; docs and idiom checks | rc 0 | receipts/gates/ |
| clone integrity | HEAD and tree exact; index, worktree bytes and modes clean; six gitlinks as recorded | receipts/static/clone_integrity.txt |

## Real limits

- **No sweep of my own.** I ran no full sweep, Yosys or route bank; none is required with no RTL line changed. The 64/64 sweep and the static and docs-workflow gates are the author's published receipts, which I verified by manifest hash and by summing the shards.
- **The em-dash gate was not judged here.** `check_em_dash.py --base a032c6d6` could not run on this host because the pinned Markdown renderer is not installed. The author's receipt reports 0 findings.
- **Two docs-workflow steps were not run by the author:** gate_42 and the no-git step, as in rounds 1 and 2.
- **`probe_lock_settle.py` was not re-run by me.** Its lock and settle defects are covered by the committed arms in my suite run, and its pair builds by my pair-input falsifier.
- **Hosted contexts were still running.** At this head they were in flight when I looked: 8 success, 1 skipped, 33 queued or in progress (`receipts/hosted_checks.txt`). That is not evidence either way.
- **No manager source bank** runs at this head, and I claim none.
- **No hardware proof.** Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Ignored caches in the clone.** My gate runs left `__pycache__` directories, which are ignored and untracked. Tracked bytes are unchanged.

## Pending manager duties

- Hosted and act acceptance at the exact head.
- The current-dev merge candidate: builder and native banks at the merge turn.
- Carry R1 to the residue checklist.
- Decide on R685-1-F3: the watchdog across a reject is still ungraded.
- The second independent positive review, and maintainer merge authorization.

R685-3 FINISHED
