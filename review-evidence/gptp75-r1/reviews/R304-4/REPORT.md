[R304] POSITIVE - exact head 6fd2ceb025e2a1bc7eaa6ccb09558584f0d499bf

# R304-4 independent delta review: FPGA-gPTP issue #75 / PR #76

- Exact head: `6fd2ceb025e2a1bc7eaa6ccb09558584f0d499bf`, tree `9669a0460e926a3d0c2911918cba793288f69216`. The PR head reported by the host matches it.
- Delta reviewed: `3face0914efd9d5e71f36da7e30108cfe09c837d..6fd2ceb0`, one commit. It touches `scripts/check_source_evidence.py` (+5 −3) and `tb/verilator/engine/sim_main.cpp` (+27 −0).
- Source base: `e5dcea6e351abff18a27a00f8e345f3251bdbd8f`. Parent consumer: kebag-logic/milan-fpga dev `573f0052a0e4412e81f0845438fcec2086ce5d55`.
- My R304-3 ledger at the ancestor `3face091` stands for everything this commit does not touch.
- Scope authority: the issue #75 body, and the round-4 assignment (issue #75 comment 5821534416). That assignment scopes three things:
  - split the 159-line slew contract into named phases under 100 lines, with check names, count, order and mutant kills unchanged;
  - annotate `check`, `selftest` and `main`, and document `main`, with no change in behaviour;
  - make the parent's C++ and Python idiom gates pass.

## 1. Verdict

**POSITIVE.** No MINOR, MAJOR or BLOCKER finding is open, and all five lenses are clean at this head. Three carried SUGGESTIONs remain (§2); they do not affect the verdict.

The round-4 scope is met, and every point is verified by execution:

| Scope item | Result | Evidence |
|---|---|---|
| Split into named phases, each under 100 lines | Met | `sim_main.cpp:4731` dispatches eight phases in textual order. Phases start at `:4742`, `:4756`, `:4781`, `:4810`, `:4829`, `:4860`, `:4883` and `:4899`. They are 13, 24, 28, 18, 30, 22, 15 and 17 lines; the dispatcher is 10. The ancestor function was 159 lines. |
| Check names, count and order unchanged | Met, byte-identical | Both commits were built with the same disposable instrumentation, which logs every `expect()` as ordinal, name, got and exp. All three shipping passes (plain, request-seeded, Sync-seeded) ran at each commit. The result is 4,839 check records per commit, 355 of them `slew:` per pass. The two logs are byte-identical, observed values included (sha256 `c3602e3b…62f2` for both). Each pass reports `1613 checks: 1613 PASS, 0 FAIL`. |
| No statement moved or changed | Met | The raw diff for `sim_main.cpp` has 27 insertions and 0 deletions, so the ancestor file is an ordered subsequence of the head file. All 27 inserted lines are phase calls, phase headers, closing braces, blank lines and one comment (`:4730`, which records that each phase continues from its predecessor's state). With that scaffolding removed, both files are 4,725 identical lines. Every local (`idle_edges`, `idle_cap_*`, `held_edges`, `lapse_*`, `master_*`, `lost_*`) is declared and used inside a single phase, so nothing is shadowed or rebound by a member. |
| Every mutant still killed, by the same check | Met, byte-identical | The tree's own `mutants.py` ran unmodified at both commits. A wrapper recorded every harness FAIL line for each of the 33 mutants and for the clean control. Arm result at both commits: `34 checks: 34 PASS, 0 FAIL`, exit 0. Per-mutant FAIL sets and arm stdout are byte-identical between the commits. The six `slew:` controls are each caught at their named check, for example `slew level tied low` at `slew: policy decision starts at +101 ns` and `slew idle asCapable loss arms qualification` at `slew: in-band pair after asCapable recovery stays inactive`. |
| Annotate `check`/`selftest`/`main`; docstring on `main`; same results | Met | `check_source_evidence.py:47-48`, `:83`, `:100-101`. Only the three signatures and one docstring changed. At both commits the ledger check prints the same 20 EXACT lines and `0 findings` (rc 0), and the self-test prints `PASS (7 arms)` (rc 0); outputs are byte-identical. Both also pass on Python 3.11, 3.12 and 3.14. The PEP 604 `str \| None` form needs Python ≥ 3.10, which the shipping generator already requires (`gen_gptp_ucode.py:610`). The annotated return type matches the returned `(findings, exact)` lists. |
| Parent `check_cpp_idiom` and `check_py_idiom` pass | Met | I made a fresh parent clone at dev `573f0052` with `protocol-processor` at its pin. `gptp-processor` was committed locally only and never pushed. Results by gitlink: <br>• `e5dcea6`: both pass. <br>• `3face091`: both fail, which reproduces the manager's round-4 report exactly: `long function 1 > ratchet 0`, `unannotated public function 3 > ratchet 0` and `undocumented public function 1 > ratchet 0`. <br>• `6fd2ceb0`: both pass, rc 0, with `long function: 0 <= 0`, `unannotated public function: 0 <= 0` and `undocumented public function: 0 <= 0` (149 translation units, 233 modules). |

## 2. Findings

No open MINOR, MAJOR or BLOCKER findings. This delta introduces no new finding.

Carried SUGGESTIONs (they do not affect the verdict, and this commit does not touch the files they name):

- **S1 (Docs), carried from R304-3 S1.** `docs/MANAGER.md` gives the area baseline without naming its commit.
  - Suggestion: name `e5dcea6` the next time that snapshot is edited.
- **S2 (Docs, Tests), carried from R304-3 S2.** The engine bullets in `docs/TEST_DEVELOPER.md:105-107` do not list the inactive asCapable loss/recovery check or its control.
  - Suggestion: add them with the next test-guide change.
- **S3 (Robustness), carried from R304-3 S3.** Field behaviour of the level is characterised only in simulation.
  - Parent #545 may want to count assertions and time spent high.

## 3. Resolution of prior public review findings at this head

I read these only after my own pass over the delta and my probe results were complete.

| Prior item | Status at 6fd2ceb0 | Evidence |
|---|---|---|
| R304-1 F1 / R305-1 F1 (MINOR; Tests, Conformance): inactive idle-timeout, GM-change and return-from-GM directions | **Still resolved** | The same checks run in the same order with the same values. The controls `slew idle lapse arms qualification` and `slew mastership keeps qualification` are caught at `slew: in-band pair after idle timeout stays inactive` and `slew: in-band return from GM stays inactive`. |
| R304-1 F2 / R305-1 F2 (MINOR; Docs): ledger anchors and slew row | **Still resolved** | 20 exact, 0 findings; self-test 7 arms; `docs/` and `hdl/` are unchanged in this delta. |
| R304-2 F3 / R305-2 F1 (MINOR; Tests, Conformance): inactive asCapable loss/recovery | **Still resolved** | The phase `keep_slew_inactive_across_capability_loss` (`sim_main.cpp:4781`) holds the ancestor block verbatim. Its control is caught at `slew: in-band pair after asCapable recovery stays inactive`. |
| R305-3 S1 (SUGGESTION; Docs): test-guide bullets | Open SUGGESTION | Same as S2 above. |
| R305-3 S2 / R304-3 S3 (SUGGESTION; Robustness): field characterisation | Carried | S3 above. |
| R304-3 S1, S2 (SUGGESTION) | Carried | S1 and S2 above. |
| Earlier SUGGESTIONs (R304-1 S1/S2, R305-1 S1/S2, R304-2 S1, R305-2 S1) | Remain taken | The files they name are unchanged in this delta. |
| Manager round-4 consumer-gate failure (issue comment 5821534416) | **Resolved** | Reproduced at `3face091`; both gates pass at `6fd2ceb0` (§1). |

## 4. Lens results (artifact-specific evidence)

### Conformance: CLEAN
- The issue #75 requirements (port, timing contract, tests, integration documentation) are unchanged from `3face091`. This delta changes no RTL, microcode, image, documentation or mutation arm.
  - `git diff --stat 3face091..6fd2ceb0 -- hdl bench syn docs Makefile tb/verilator/engine/gptp_ucode.hex tb/verilator/engine/mutants.py` is empty.
- The committed engine image matches regeneration at both commits.
- All three round-4 scope items are met (§1). The parent-consumer requirement (issue item 5) now passes the two idiom gates that previously blocked the parent pin.

### RTL: CLEAN
- There is no HDL, microcode generator or ROM image change in the delta.
- The engine was rebuilt at head under the pinned simulator with 0 warnings (`-Wall -Wextra`). Its behaviour is byte-identical to the ancestor across 4,839 observed check values.

### Robustness: CLEAN (S3 SUGGESTION carried)
- The phases keep strict sequential state coupling. That is documented at `sim_main.cpp:4730`, and every phase is called exactly once, in source order.
- No phase reads a local declared in another phase, so the split cannot change stimulus.
- The annotated checker behaves the same on Python 3.11, 3.12 and 3.14.

### Tests: CLEAN
- Check sequence, names, count and values are identical in all three passes.
- The mutation arm passes 34/34 at both commits, with byte-identical per-mutant FAIL sets. All six `slew:` controls are caught at their named checks.
- The evidence-checker self-test is unchanged (7 arms, PASS).

### Docs: CLEAN (S1, S2 SUGGESTIONs carried)
- The new `main` docstring (`check_source_evidence.py:101`) is accurate: it returns 0 for the self-test and `int(bool(findings))` for the ledger check.
- The phase names describe their content.
- No guide references the split function or `sim_main.cpp` line numbers, so nothing went stale.
- The ledger is still 20/20 exact.

## 5. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #75 body; assignment 5821534416; delta diff; untouched-path diff; parent idiom gates at `e5dcea6`, `3face091` and `6fd2ceb0` | R304-4 (delta); R304-3 for the rest | 6fd2ceb025e2a1bc7eaa6ccb09558584f0d499bf |
| RTL | CLEAN | Empty HDL/ucode/image diff; engine rebuild at head, 0 warnings; image regeneration match | R304-4 (delta); R304-3 for the rest | 6fd2ceb025e2a1bc7eaa6ccb09558584f0d499bf |
| Robustness | CLEAN (S3) | Phase locals and state coupling (`sim_main.cpp:4730-4915`); checker on 3 Python versions | R304-4 (delta); R304-3 for the rest | 6fd2ceb025e2a1bc7eaa6ccb09558584f0d499bf |
| Tests | CLEAN | Instrumented check logs at both commits (3 passes each); body-identity proof; unmodified mutation arm at both commits, with per-mutant FAIL capture | R304-4 | 6fd2ceb025e2a1bc7eaa6ccb09558584f0d499bf |
| Docs | CLEAN (S1, S2) | `check_source_evidence.py` docstrings/annotations; ledger check and self-test at both commits; guide references to changed code | R304-4 (delta); R304-3 for the rest | 6fd2ceb025e2a1bc7eaa6ccb09558584f0d499bf |

## 6. Real limits

- **Consumer gates.** I ran only two of the six: `check_cpp_idiom` and `check_py_idiom`. `xvlog_gate.py --check`, `check_rtl_source_lists.py`, `sw/builder/test_builder.py` and the `gptp_shadow` build were outside my scope. For those I rely on public author evidence at this head (`author-r4/gate-results.tsv`, all rc 0), which I did not re-execute.
- **Not run by me:** the full donor bank (`make -j8`), the parent, PP, gPTP, Yosys and builder banks, and Docker/act.
  - The manager reports that its full source static/builder and native banks passed at this head.
  - I ran the engine suite (3 passes) and the engine mutation arm at both commits.
- **Hosted checks:** the host reports 0 check runs and 0 statuses at this head, so there is no hosted executed or skipped job to distinguish.
- **Hardware:** physical calibration was NOT RUN, and field skips are not hardware proof. The level's field behaviour is simulation-only (S3).
- **My consumer clone:** dev `573f0052` directly plus a local gitlink commit. The author's consumer commit sat on a different local parent (`584a8c17`), and I did not use it.
- **Clone state:** the review clone was restored and verified at exact head. HEAD, tree and index tree are `9669a046…`. All 104 index entries match the HEAD tree by mode and blob, worktree bytes rehash to their blobs with 0 mismatches, exec bits match, and there are no untracked or ignored files. The repository has no gitlinks. The disposable consumer clone was reset to `573f0052` with gitlink `e5dcea6`.

## 7. Pending manager duties

- Build and validate the final current-dev candidate at the merge turn: source base `e5dcea6e`, live dev `573f0052`, including all six parent consumer gates on the real pin.
- Own hosted/act acceptance.
- Obtain the second independent review. R305-3 stays POSITIVE at the ancestor `3face091`, under the round-4 assignment.
- Publish this packet (REPORT.md plus the files listed in MANIFEST.sha256).

## 8. Packet contents

- `scripts/`: the four probes.
  - `probe_checklist.sh`: instrumented check-list diff.
  - `probe_mutants.py`: per-mutant FAIL capture around the unmodified arm.
  - `probe_body_identity.py`: scaffold-stripped body identity.
  - `probe_consumer_gates.sh`: parent idiom gates per gitlink.
- `receipts/`: raw outputs (check logs, mutation logs, checker outputs, gate outputs, delta diff, hosted status, environment, clone verification).

R304-4 FINISHED
