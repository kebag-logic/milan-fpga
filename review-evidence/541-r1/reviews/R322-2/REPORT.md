[R322] POSITIVE - exact head fa1b5c364b39842d0f3d8e09acd7ca58a9532f0c

# R322-2: internal independent re-review of issue #541 / PR #562

- Head: `fa1b5c364b39842d0f3d8e09acd7ca58a9532f0c`, tree `f77cc840ece81a2bcda303696d96136a2b0ca415`. It is one commit on `2734b771bcf0b383ea62ef05744452827bafe9e4`, the head my round R322-1 covered. The source base is `5b73d3f47dfed519eb988c13d6beb1db664ef1e0`.
- Role: internal reviewer [R322], cleared context, executor [A306]. This is a delta review of `2734b771..fa1b5c36`. All five lenses were re-applied at this head.
- How I rebuilt the scope, in this order:
  - AGENTS.md and CONTRIBUTING.md
  - the #541 body and its frozen acceptance, plus the decision comment 5827373589 (not changed by round 2)
  - round-2 scope comment 5828726541 and the [A306] REVIEW READY comment 5829021483
  - `git diff 2734b771..fa1b5c36` and `5b73d3f4..fa1b5c36`
  - the receiver RTL and harnesses
  - the public evidence tree `3a211d8d:review-evidence/541-r1/author-r2`
- My independent pass over the diff (receipts `probe_head.txt`, `probe_mid_2734b771.txt`, `rtl_identity.txt`, `head_gate.txt`) was finished before I read the prior public findings (R322-1, comment 5827859729; R323-1, comment 5828724733).

## Verdict summary

POSITIVE. The same round-1 MINOR was raised by both reviewers (R322-1-F1 and R323-1-F1), and it is closed at this head. R323-1-F2 is also resolved.

There is no RTL change. Across `2734b771..fa1b5c36` the RTL is raw byte-identical, and against the base it is identical once comments are stripped.

The new check `rejected_stream_timeout` (`tb/verilator/crf_rx/sim_discontinuity.cpp:227-264`) works as follows:
- It locks the sink, then sends only matched wrong-type PDUs every 400 clocks (2 ms).
- It grades lock on every cycle up to 19,992 clocks (99.96 ms) and requires the unlock, with exactly one MEDIA_UNLOCKED, by 20,012 clocks (100.06 ms).
- It then requires no relock and no recount through 40,012 clocks (200.06 ms).

These mutants now fail it:
- the named campaign mutant;
- my round-1 P2 and drought probes, run unchanged;
- R323's `uf_refreshes_timeout` (the same edit as my `uf_refreshes`);
- five further reviewer variants of the refresh and relock fault.

Every refresh-class variant **survives** at `2734b771`, so the new check is what kills them. No open BLOCKER, MAJOR or MINOR remains. There are two optional SUGGESTIONs.

## Findings

### R322-2-S1: SUGGESTION: Docs, Tests: two harness-local descriptions predate the #541 checks (optional, does not affect coverage)

- **Where:**
  - `tb/verilator/crf_rx/Makefile:9` still reads "make mutants - detector/refill/servo-validity mutants with named failures".
  - `tb/verilator/crf_rx/sim_discontinuity.cpp:3` still introduces the file as "Issue #546: public-output checks of timestamp-era isolation".
- **Evidence:** both files now also carry the #541 lock-retention and timeout checks and the two `validation_error_*` mutants (`mutants.py:20-25`, `sim_discontinuity.cpp:181-264`). The authoritative index (`docs/testing/TESTING.md:463`) and the evidence disposition (`scripts/measure_test_evidence.py:597-600`) are already correct.
- **Impact:** none on correctness. A reader who starts from the harness header does not learn that lock policy is graded there.
- **Outcome (optional):** mention the validation-error lock and timeout checks in both descriptions.

### R322-1-S1 (retained, optional): SUGGESTION: Docs: `CRF_CTRL` row qualifiers

This is unchanged from round 1 (`docs/reference/REGISTER_MAP.md:837`). The row omits the "consumed while started" qualifier, and it does not say that a bind edge or reset clears lock without scoring MEDIA_UNLOCKED. It stays optional and does not affect coverage.

## Prior public findings: disposition at this head

| Finding | Severity | Disposition | Evidence |
|---|---|---|---|
| R322-1-F1: "does not refresh the timeout" ungraded; refresh mutant survives | MINOR (Tests, Robustness) | **CLOSED** | See the four points below this table. |
| R323-1-F1: the same defect (`uf_refreshes_timeout`) | MINOR (Tests, Robustness) | **CLOSED** | `probe_head.txt` `uf_refreshes` makes the identical edit (`if (w_acc_run_w \|\| w_ev_uf_w)`) and is KILLED with the same four named failures. The author's unchanged rerun (`author-r2/r323-refresh.log`) agrees. |
| R323-1-F2: TESTING.md row does not name the new mutant | SUGGESTION (Docs) | **RESOLVED** | `docs/testing/TESTING.md:463` names `validation_error_unlocks` and `validation_error_refreshes_timeout`, and states the retention and timeout property. `receipts/docs_manual.txt` shows the row, the campaign inventory and the ratchet text agree. |
| R322-1-S1: `CRF_CTRL` row qualifiers | SUGGESTION (Docs) | Open, optional | Row unchanged. |

Evidence for closing R322-1-F1:
1. The new check is at `sim_discontinuity.cpp:227-264`.
2. The named mutant `validation_error_refreshes_timeout` (`mutants.py:23-25`) fails "reject stream cannot refresh the 100 ms timeout" in the campaign (`receipts/head_gate.txt`).
3. My round-1 `P2_error_refreshes_timeout` was run unchanged. Its script sha256 is `8f2137b5…`, the same hash the author's provenance file records. P2 is now DETECTED by the discontinuity harness, with 4 named failures (`receipts/r322-1-probes-at-head.txt`).
4. My round-1 drought probe was run unchanged: the head passes 9/9 checks and P2 fails 4 (`receipts/r322-1-drought-at-head.txt`).

The round-1 required comment fix at `sim_discontinuity.cpp:182-184` is done: it now reads "does not refresh the 100 ms timeout measured from the last consumed accepted PDU".

## Lens results (reviewer-owned, all applied at `fa1b5c36`)

```text
[R322] PASS Conformance - issue 541 body + comments 5827373589, 5828726541; hdl/ieee1722/crf/KL_crf_rx.sv:34-44,354,529-564; docs/reference/REGISTER_MAP.md:837; tb/verilator/crf_rx/sim_discontinuity.cpp:181-264 - acceptance 1-3 and round-2 items 1-2 checked against the decided timeout-only unlock
[R322] PASS RTL - receipts/rtl_identity.txt; hdl/ieee1722/crf/KL_crf_rx.sv:309-386,529-609 - no RTL change in the delta (raw identical 2734b771..fa1b5c36; comment-stripped identical to base); the timeout/reject paths re-read against the new check's cycle arithmetic
[R322] PASS Robustness - tb/verilator/crf_rx/sim_discontinuity.cpp:227-264; receipts/probe_head.txt, probe_mid_2734b771.txt, r322-1-drought-at-head.txt - malformed-only traffic across the timeout, post-timeout relock and recount, and early/late timeout boundaries all graded; refresh/pause/halve/relock variants killed at head, surviving at 2734b771
[R322] PASS Tests - tb/verilator/crf_rx/sim_discontinuity.cpp:181-264; tb/verilator/crf_rx/mutants.py:19-34; receipts/head_gate.txt, unit_talker.txt, probe_head.txt, r322-1-probes-at-head.txt - 13,836 unit + 2,201 discontinuity + 69 talker-step checks green; 10/10 campaign controls; the new check fails for the defect it names
[R322] PASS Docs - docs/testing/TESTING.md:463; scripts/measure_test_evidence.py:596-600; tb/verilator/crf_rx/mutants.py:19-34; receipts/docs_checks.txt, docs_manual.txt - index and ratchet disposition match the 8-mutant inventory; ratchet PASS; doc gates OK (two renderer-dependent gates: see limits)
```

**Conformance: CLEAN.**
- The decision is unchanged: timeout-only unlock, and a validation error is counted but does not unlock. The clause reading I recorded in round 1 (Milan v1.2 5.3.8.10 / Table 5.6 leaves "unsynchronized" to the manufacturer; IEEE 1722-2016 10.6 free-wheels through packet loss) still applies. Nothing in the delta touches normative text or RTL.
- Round-2 item 1 is met. The check's validation errors are spaced every 2 ms, far inside the 20,000-clock timeout (`CLK_FREQ_HZ_P=200000`, `Makefile:39`; `TOUT_CYC_C = CLK/10`, `KL_crf_rx.sv:298`). So the timeout can expire only if the rejects fail to refresh it, and the check requires the unlock on schedule.
- The named mutant fails that check, and the reviewers' mutants were run unchanged, with verdicts recorded.
- Round-2 item 2 is met (see Docs).
- #541 acceptance 2 remains met: the header, row and RTL agree, and the check has failing arms.
- Acceptance 3 is met at source level. Hosted status is covered below.

**RTL: CLEAN.** `receipts/rtl_identity.txt`:
- `KL_crf_rx.sv` is raw-identical across `2734b771..fa1b5c36` and comment-stripped identical to `5b73d3f4`. No `hdl/` path changed in the delta.
- I re-read the new check's arithmetic against the RTL. After `fill()`, the last accept cleared `tout_r` (`:531-532`) and `send()` left two idle clocks. At loop index k the counter therefore reads k. The unlock fires on the edge where `tout_r == 20000` (`:533-538`), which is index 20,001. That sits inside the graded 19,992 to 20,012 window.
- A reject sets only `settle_r <= 0` and the UF flag (`:374`, `:560-564`). It never touches `tout_r` or `locked_o`, which is what the check asserts.

**Robustness: CLEAN.**
- Malformed-only input across the timeout boundary is now graded, along with post-timeout idempotence (no relock, no second MEDIA_UNLOCKED under continued rejects) and UF counting during the drought.
- Reviewer variants at the head (`receipts/probe_head.txt`) are all KILLED:
  - `uf_refreshes` and `hit_refreshes`: a reject or any matched frame refreshes the timeout;
  - `uf_halves`: a reject halves the elapsed silence;
  - `uf_pauses`: a reject stalls the counter for one clock, a 50-clock cumulative delay;
  - `uf_relocks`: a reject re-arms lock after the timeout, killed only by the new "continued reject stream" arms;
  - `tout_late20` and `tout_early20`;
  - `uf_unlocks`.
- At `2734b771` (`receipts/probe_mid_2734b771.txt`), all five refresh, pause, halve and relock variants SURVIVE. The ±20 and unlock variants were already killed.
- My round-1 probes P1, P3, P4b and P5 to P9 remain DETECTED, and P2 is now DETECTED (`receipts/r322-1-probes-at-head.txt`).

**Tests: CLEAN.**
- Head gate (`receipts/head_gate.txt`, `unit_talker.txt`): unit 13,836 checks, discontinuity 2,201, talker-step 69, all with 0 failures.
- `mutants.py` gives 10/10 controls: clean, both `validation_error_*`, tu, jump, refill, accept-edge, servo clean, and the two servo mutants.
- The +269 discontinuity checks match the new function exactly: 3 preconditions + 258 `fill()` checks + 4 in-loop + 4 final.
- The new check reads only public outputs (`locked_o`, `cnt_*_o`, `fmt_err_o`). Its expectations come from the stimulus schedule and the documented 100 ms at 200 kHz, not from DUT internals.
- The existing `locked_validation_error` retention check and the 100 ms silence unlock are unchanged apart from the comment, and still graded (`receipts/discontinuity_head.log` lines for "validation error preserves established lock" and "100 ms silence still unlocks after validation error"). `uf_unlocks`, `tout_late20` and `tout_early20` still fail them.
- The campaign enforces a unique anchor for the new mutant (`mutants.py:90`). Its named-failure string is the check's exact name.
- Pre-existing and out of this delta: my round-1 `P4_error_counts_frames_rx` still survives, exactly as it did at `2734b771`. Round 1 superseded it with P4b (DETECTED), because P4 only differs when a reject coincides with the tick cycle. That counter boundary belongs to the #529 interval counters, not to the #541 lock policy, so it is not filed against this lane.

**Docs: CLEAN.**
- `TESTING.md:463` adds the lock-retention and timeout sentence and names both `validation_error_*` mutants. The rest of the row predates the PR.
- `measure_test_evidence.py:597-600` names all eight mutation defects in the campaign (`mutants.py:19-34` plus the two servo arms).
- `measure_test_evidence.py --check`: RATCHET PASS, with no budget change. docs_check reports 0 findings; doc style, doc paths, and the C++ and Python idiom gates are OK. `git diff --check` is clean over the delta.
- No added line contains U+2014, and no heading changed (`receipts/docs_manual.txt`).
- No authoritative contract changed in the delta, so the header and `CRF_CTRL` row stay as covered in round 1.

## Completion ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|------|---------------|--------------------|----------------|------------|
| Conformance | CLEAN | #541 body; comments 5827373589, 5828726541, 5829021483; `KL_crf_rx.sv:34-44,298,354,529-564`; `REGISTER_MAP.md:837`; `sim_discontinuity.cpp:181-264`; `Makefile:39` | R322-2 | `fa1b5c364b39842d0f3d8e09acd7ca58a9532f0c` |
| RTL | CLEAN | `receipts/rtl_identity.txt`; `KL_crf_rx.sv:309-386,529-609` | R322-2 | `fa1b5c364b39842d0f3d8e09acd7ca58a9532f0c` |
| Robustness | CLEAN | `sim_discontinuity.cpp:227-264`; `receipts/probe_head.txt`; `receipts/probe_mid_2734b771.txt`; `receipts/r322-1-probes-at-head.txt`; `receipts/r322-1-drought-at-head.txt` | R322-2 | `fa1b5c364b39842d0f3d8e09acd7ca58a9532f0c` |
| Tests | CLEAN | `sim_discontinuity.cpp:14-31,181-264`; `mutants.py:19-34,90`; `receipts/head_gate.txt`; `receipts/unit_talker.txt`; probe receipts above | R322-2 | `fa1b5c364b39842d0f3d8e09acd7ca58a9532f0c` |
| Docs | CLEAN | `TESTING.md:463`; `measure_test_evidence.py:596-600`; `REGISTER_MAP.md:837`; `receipts/docs_checks.txt`; `receipts/docs_manual.txt`; `author-r2/em-dash.log`, `toc-check.log`, `toc-anchors.log` | R322-2 | `fa1b5c364b39842d0f3d8e09acd7ca58a9532f0c` |

Every lens was applied and is clean at the merge-candidate head. Only the two optional SUGGESTIONs are open.

## Commands (portable; all run in the foreground)

- RTL identity: `python3 scripts/rtl_identity.py <clone> 5b73d3f4… 2734b771… fa1b5c36…`
- Head gate: `sh scripts/run_head_gate.sh <clone> fa1b5c36… scratch/head <pinned-verilator>`. This runs discontinuity and `mutants.py` on a `git archive` copy. Then `make VERILATOR=<pinned> unit talker_step` runs in `scratch/head/tb/verilator/crf_rx`.
- Reviewer probes (8 parallel builds at most): `python3 scripts/probe_mutants.py scratch/head <pinned> scratch/probe_head`, then the same against a `2734b771` archive.
- Round-1 probes, unchanged (sha256 checked against the round-1 packet in `receipts/r322-1-scripts-origin.sha256`): `python3 scripts/r322-1-unchanged/probe_mutants.py scratch/head scratch/r1probes <pinned> 8` and `sh scripts/r322-1-unchanged/run_drought.sh scratch/head scratch/drought <pinned>`.
- Doc and evidence gates: run from the clone, each command listed in `receipts/docs_checks.txt`.
- Tool: Verilator 5.050 rev v5.050, via the scoped wrapper (wrapper sha256 `905795b9…`).
- Clone integrity after review (`receipts/clone_integrity.txt`):
  - HEAD, index write-tree and HEAD tree all equal `f77cc840`.
  - All 889 regular entries match in raw bytes and modes, and the worktree and index are clean.
  - Gitlinks are unchanged: `external efeb541a`, `gptp-processor e5dcea6e`, `protocol-processor 09f9bf38`, `third_party/verilog-axis 48ff7a7e`.
  - Running the repo scripts created an ignored `scripts/__pycache__/` (timestamped inside this session). I removed it, and the clone now has zero untracked or ignored entries.
  - All builds and mutants ran on archive copies under `scratch/`.

## Real limits

- `gen_toc.py --check`, `gen_toc.py --verify-anchors` and `check_em_dash.py` could not run here: the pinned Markdown renderer is not installed, both gates exit 2, and installing it is out of my authority. The substitutes:
  - I checked by hand that no added line contains U+2014 and no heading changed.
  - The author's exact-head logs (`author-r2/em-dash.log`: 0 findings; `toc-check.log` and `toc-anchors.log`: OK) and the manager's source banks cover these gates. I did not re-execute them.
- I had no primary copy of Milan v1.2 or IEEE 1722-2016. The conformance reading rests on the round-1 basis (in-repo quotations and the published clause evidence), and the delta does not change it.
- I did not run the servo suite, parent, PP, gPTP, Yosys or builder banks, or `act`. None of their inputs changed in the delta. The manager's banks passed at this head.
- Hosted snapshot at 08:19Z (`receipts/hosted-checks-snapshot.tsv`):
  - completed with success: `rtl-fast`, `full-ci-gate`, `elaborate`, `verilator-lint`, `yosys-elaboration`, Yosys shards 0-3, Verilator shards 0, 2 and 3;
  - still in progress: Verilator shards 1 and 4, and `docs-check`;
  - skipped: `Physical gPTP (nightly and manual)`. It did not run, and it is not hardware proof.
- Physical calibration was NOT RUN. No hardware evidence exists or is claimed.

## Pending manager duties

- Accept the hosted and `act` evidence at the exact head, including the in-progress Verilator shards 1 and 4 and `docs-check`.
- Build and validate the final current-dev candidate at the merge turn: source base `5b73d3f4`, live dev `a3d795ae`.
- Obtain the external round-2 verdict (R323-2).
- Obtain maintainer merge authorization, then run post-merge containment and close #541.

R322-2 FINISHED
