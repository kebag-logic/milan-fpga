[R295] POSITIVE - exact head a024ab51b926690be5ade8ec35ec1fa7dd23981b

# R295-3 independent external review: PR #111 (issues #43, #49), round 2b delta

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head: `a024ab51b926690be5ade8ec35ec1fa7dd23981b`, tree `631666c74bc87ee6f422650ce91ed729fc44c285` (PR #111 `headRefOid` matches)
- Delta under review: `a14ef8b4787b5309dd9ab472e82ae2b4a3fdbb72..a024ab51` (one commit, [A262] "Split SRP failure-change test scenarios"). R294-2 and R295-2 are POSITIVE at `a14ef8b4`.
- Source base: `939c143333d11e2378a514f1c7b6abd4c3259bfd`
- Review start: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/111#issuecomment-5817025952

## Verdict

**POSITIVE.** No MINOR, MAJOR or BLOCKER finding is open at this head. The delta is a behaviour-preserving split of one test function. The claims checked:

- **No behaviour change.** The SRP stream suite gives the same 1087 checks at both commits. The output is byte-identical: plain, and with a per-check trace that prints the sequence number, the result, the message and the observed values.
- **Every assertion of the original function still executes.** All 19 section-L checks (15 in the first scenario, 2 in each split-off scenario) run in the same order at the same positions (seq 1069-1087), with the same observed values.
- **The parent long-function rule holds.** Rule 11 (F.3, 100 lines, ratchet 0) was 1 at `a14ef8b4` and is 0 at `a024ab51`. The three scenarios are 79, 20 and 24 lines, and the file maximum is 90.
- **Nothing else changed.** One blob changed (+8/−0) in `tb/srp_stream_fsms/sim_main.cpp`, with the same mode. Every other tree entry is identical.

I wrote my own verdict and ledger (`receipts/verdict-before-prior-findings.txt`, 2026-09-24T15:29:12Z) before reading any prior review's findings. Section 4 resolves or retains those findings.

## 1. Reconstruction (in the prescribed order)

1. **Contributor rules.** The processor repository has no AGENTS.md or CONTRIBUTING.md. The review contract is the parent's, read at live dev `57456af9`:
   - AGENTS.md §6: the lenses, the finding format, and one clean-lens line with an artifact.
   - The parent's `scripts/check_cpp_idiom.py` (Rule 11) and `scripts/cpp_idiom.budget` (`long function = 0`), with git blob ids in `receipts/tool_identity.txt`.
2. **Docs.** I read `README.md` (repository map, build and check commands) and `tb/srp_stream_fsms/README.md` (the suite contract: 1087 checks, section L, the mutation table).
3. **Frozen scope.** I read the issue #43 and #49 bodies and acceptance sections, and the manager's decisions:
   - A253: the internal seam, with response-level acceptance.
   - A255: round 2 required items.
   - A262: round 2b. It must be test code only and split the function that A255 lengthened, because the parent's `check_cpp_idiom` failed at `a14ef8b4` ("long function 1 > ratchet 0"). The suite must run the same checks, with the same count and the same results.
4. **Diff and history.**
   - The range `939c1433..a024ab51` has six commits.
   - `a024ab51` has the single parent `a14ef8b4`.
   - Its diff adds two member declarations (`sim_main.cpp:426-427`) and two `}` + new-signature pairs at the existing `h.reset()` boundaries (`:1002-1004`, `:1023-1025`). It adds two calls in `run()`, directly after the original call (`:1064-1065`).
   - It removes no line (`receipts/delta_scope.txt`).
5. **Public evidence.**
   - `kebag-logic/milan-fpga@87b38a25/review-evidence/pp43-r1`. Its MANIFEST covers `author/` and `author-r2/`, both at `a14ef8b4` or earlier, and it has no receipt at `a024ab51`.
   - The manager's comment on the PR at `a024ab51`: donor 9/9, parent consumer 7/7 including `check_cpp_idiom`, on parent dev `57456af9`.
   - Hosted runs at the exact head (Section 3.5).

## 2. Lens results at the exact head

| Lens | Result | Artifact | What was checked and against what |
|---|---|---|---|
| Conformance | PASS | `receipts/delta_scope.txt`; `tb/srp_stream_fsms/sim_main.cpp:918-1047`; `receipts/{anc,head}-trace.out` | No byte under `hdl/`, `docs/`, `syn/` or `scripts/` changed, so the issue #43/#49 acceptance and the A253/A255 decisions are satisfied exactly as at `a14ef8b4`. The section-L checks that carry the conformance claims run identically, with identical observed values. They cover a FailureInformation change notifying without MRP New or TK_REGISTERED (L1-L7), the per-sink latch comparison (L8) and a shared stream (L9). A262's own acceptance is met: the same checks, the same count, the same results. |
| RTL | PASS | tree diff (`receipts/delta_scope.txt`); mutants at `hdl/srp/KL_srp_listener_fsm.sv:474-475` and `:735` (`receipts/{anc,head}-mut-*.out`) | Every `hdl/` blob at the head is identical to `a14ef8b4`. No module, port, parameter or synthesis input changed, so there is no area or timing delta. Two RTL mutants give byte-identical failure sets at both commits. The first, the comparator reading sink 0's latch, fails 2 of 1087 (L8, L9). The second, the change strobe never raised, fails 6 of 1087 (L2, L3 ×2, L6, L8, L9). |
| Robustness | PASS | `sim_main.cpp:1009`, `:1029` (`h.reset()` opening L8 and L9); `:325-327` (file-scope `SID0`/`DA0`/`VID0`); `receipts/head-fault-dropcall.*`; build logs (0 warnings) | The two cuts fall at existing `h.reset()` boundaries, so neither new scenario depends on DUT state left by the one before it. Their order in `run()` is preserved anyway. No split-off body uses a local of the original function: `no_new` is used only in L6, and `SIDB`/`DAB` are local to L8. No file-scope name is shadowed, so no identifier silently re-binds. `h`, `checks` and `fails` are class members, so the tally accumulates as before. Under `-Wall -Wextra` there are 0 warnings at both commits. The fault probe drops the L9 call: the suite loses exactly 2 checks (1085), and the compiler flags `-Wunused-function`. The split does not hide a dropped scenario. |
| Tests | PASS | `receipts/{anc,head}-trace.out` (md5 `5f1d3abb…` both); `receipts/runs.txt`; `receipts/idiom_scan.txt` | The traced runs match line for line, all 1088 lines. Each check's sequence number, result, message and printed values are identical. So every assertion of the original 121-line function still executes (19 checks, seq 1069-1087), in the same order and against the same DUT state. The plain runs are identical (`1087 checks: 1087 PASS, 0 FAIL`, rc 0). Both mutant sets are identical, so the scenarios keep their detection power after the split. Rule 11 was measured with the parent's own checker over all 34 C/C++ files under `tb/`. At `a14ef8b4` it finds `long function` = 1 (`sim_main.cpp:922`, 121 lines). At `a024ab51` it finds 0: the scenarios are at `:924` (79), `:1004` (20) and `:1025` (24), and the file maximum is `:647` (90, pre-existing). Every other Rule 11 key is 0 at both commits. |
| Docs | PASS | `tb/srp_stream_fsms/README.md:8`, `:58-70`, `:130-138`; PR body; issue #43 A262 comments; PR manager comment at `a024ab51` | README `:8` ("1087 checks") still holds. Section L (`:58-70`) still describes the three scenarios: the single stream, two sinks on different streams, and three sinks on one stream. The mutation rows `:136` and `:137` reproduce exactly at the head (6 and 2 of 1087, the same named checks). No contract changed, so no authoritative doc needed a change. The round-2b rationale and evidence are public on issue #43 (A262 assignment and REVIEW READY) and on the PR (manager validation). The PR body does not mention round 2b, but nothing in it becomes false (S1). |

## 3. Executed evidence

All commands ran in the foreground. Trees were extracted with `git archive` into a disposable scratch area, so the clone was never modified. Builds used the Makefile's own recipe, except `-j 0` → `-j 8` for the job cap.

### 3.1 Tool identity (`receipts/tool_identity.txt`)
The scoped simulator reports `Verilator 5.050 2026-07-01 rev v5.050`. The wrapper sha256 is `905795b9…e92f`, and the wrapped binary sha256 is `44898b22…bfdd`.

### 3.2 Behaviour identity (`scripts/run_delta_probe.sh` → `receipts/runs.txt`)

| Run | `a14ef8b4` | `a024ab51` | Compare |
|---|---|---|---|
| plain | rc 0, 1087/0 | rc 0, 1087/0 | IDENTICAL |
| trace (per-check sequence, result, message, values) | rc 0, 1087/0 | rc 0, 1087/0 | IDENTICAL (1088 lines) |
| mutant: comparator reads sink 0's latch | rc 2, 2 FAIL (L8, L9) | rc 2, 2 FAIL (L8, L9) | IDENTICAL |
| mutant: change strobe never raised | rc 2, 6 FAIL (L2, L3 ×2, L6, L8, L9) | rc 2, 6 FAIL | IDENTICAL |
| fault: head without the L9 call | n/a | rc 0, 1085 checks, 1 `-Wunused-function` warning | count-sensitive |

### 3.3 Rule 11 (`scripts/idiom_scan.py` → `receipts/idiom_scan.txt`)

The measurement uses the parent's checker, unchanged, with a stub for its tree-scope import. `939c1433` measures 0, `a14ef8b4` measures 1 (the 121-line function), and `a024ab51` measures 0. The Makefile-level key `build without warnings` is only counted in the parent's full audit. The delta changes no Makefile, and `tb/srp_stream_fsms/Makefile` passes `-Wall -Wextra`.

### 3.4 Scope and clone integrity (`receipts/delta_scope.txt`, `receipts/clone_integrity.txt`)

- `git diff --raw` lists one entry: `100644 → 100644 ce51222 → 39e1b2e tb/srp_stream_fsms/sim_main.cpp`. There are 8 insertions and 0 deletions, and `git diff --check` returns rc 0.
- A full `ls-tree -r` comparison differs only on that line.
- After the probes, the clone is at HEAD `a024ab51`, tree `631666c7`. `status --porcelain --ignored` is empty, the index matches HEAD and the worktree matches the index. `ls-files -s` equals `ls-tree -r HEAD` for every mode, blob and path.
- The processor tree has no gitlinks (0 entries of mode 160000 at the head and in the index) and no `.gitmodules`, so no submodule gitlink needed restoring.

### 3.5 Hosted evidence at the exact head (inspected; hosted acceptance is the manager's)

`receipts/hosted_checks.txt` and `receipts/hosted_suites_log_excerpt.txt` cover two workflow runs, both on `head_sha a024ab51`. All six jobs completed with success, and none was skipped.

- **Push run 36017365806:** suites, portability and docs-gates. It reports `PASS srp_stream_fsms (1087 checks: 1087 PASS, 0 FAIL)` and `16416 checks total, 0 failing`.
- **pull_request run 36017369774:** the merge ref `ca59bf8`, a merge of `a024ab51` into `939c1433`, with the same three jobs. It reports the same SRP and bank totals.

## 4. Prior public review findings on this PR (read after Section 2 and the pre-read ledger)

Every file named below is byte-identical between `a14ef8b4` and `a024ab51`, except `tb/srp_stream_fsms/sim_main.cpp`, whose behaviour is proven identical above.

| Finding | At `a14ef8b4` | At this head | Basis |
|---|---|---|---|
| R295-1 F1 MAJOR (a re-bind from ACTIVE/0 did not notify) | RESOLVED (R294-2, R295-2) | **RESOLVED, retained** | The ACMP listener, the top and GI are unchanged, and hosted GI is green at the head |
| R295-1 F2 MINOR = R294-1-F1 MAJOR (a changed FailureInformation re-declared with New) | RESOLVED | **RESOLVED, retained** | The RTL is unchanged. The module-level evidence (section L, L2 "no Listener New") runs identically, and the no-strobe mutant is still killed by L2/L3/L6/L8/L9 |
| R295-1 F3 MINOR = R294-1-S1 (untested sample-and-hold) | RESOLVED (removed) | **RESOLVED, retained** | The top is unchanged |
| R295-1 S1 = R294-1-S2 (index-guard test) | RESOLVED | **RESOLVED, retained** | `tb/pp_top` is unchanged |
| R295-1 S2 (gate once, compare on the hit sink) | RESOLVED | **RESOLVED, retained** | The RTL is unchanged. The hit-sink comparator is still killed by L8/L9 at the head |
| R295-1 S3 (portable affinity), S4 (`dbg_recwr` documented) | RESOLVED | **RESOLVED, retained** | The files are unchanged |
| R294-1-S3 (area at 1x1; decoder copy) | TAKEN IN PART | **Retained as SUGGESTION** | The decoder copy is unchanged and outside this diff |
| R295-2 S1 (`bnd_was_r` guard unpinned) | SUGGESTION | **Retained as SUGGESTION** | `hdl/acmp`, `tb/acmp_listener` unchanged |
| R295-2 S2 (hit-sink comparator proven at module level only) | SUGGESTION | **Retained as SUGGESTION** | The module-level proof survives the split: the sink-0-latch mutant is still killed by L8 and L9 at the head. There is still no GI step |
| R294-2-S1 (internal-selector wait mask untested), S2 (index = N boundary), S3 (`bnd_was_r`), S4 (coherence bound wording) | SUGGESTION | **Retained as SUGGESTION** | The files are unchanged |

No prior finding is reopened, and none of the retained items is above SUGGESTION.

## 5. Findings at this head

No BLOCKER, MAJOR or MINOR.

### S1: SUGGESTION. The PR body does not record round 2b
- **Lenses:** Docs.
- **Artifact:** PR #111 body. Its "Round 2" and "Validation" sections describe commits up to `a14ef8b4`. `a024ab51` is listed among the PR's commits but not described.
- **Authority/evidence:** Parent AGENTS.md §6 (Docs): the PR and issue must carry enough evidence for a cold reviewer. The round-2b rationale is public on issue #43 (A262 assignment and REVIEW READY) and in the PR's manager validation comment. The PR body itself is silent, and the A262 handoff it cites is not published. The evidence MANIFEST at `87b38a25` stops at `a14ef8b4`.
- **Impact:** None on correctness, and no statement in the body is false at the head. A reader of the body alone does not learn why the head moved.
- **Suggested outcome:** Add one line to the body naming `a024ab51` as a test-only split for parent Rule 11, with the identical 1087/0 output, or publish the round-2b receipts next to `author-r2`.
- **Verification:** The PR body or the evidence manifest names `a024ab51`.

## 6. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `receipts/delta_scope.txt` (no `hdl/`/`docs/`/`syn/` byte changed); section-L trace `receipts/head-trace.out` seq 1069-1087; issue #43/#49 acceptance with A253/A255/A262 | R295-3 | a024ab51b926690be5ade8ec35ec1fa7dd23981b |
| RTL | CLEAN | tree diff; `hdl/srp/KL_srp_listener_fsm.sv:474-475,:735` mutants identical at both commits (`receipts/*-mut-*.out`) | R295-3 | a024ab51b926690be5ade8ec35ec1fa7dd23981b |
| Robustness | CLEAN | `tb/srp_stream_fsms/sim_main.cpp:924,1004,1009,1025,1029,1063-1065,325-327`; `receipts/head-fault-dropcall.*`; 0 compiler warnings (`receipts/*.warnings`) | R295-3 | a024ab51b926690be5ade8ec35ec1fa7dd23981b |
| Tests | CLEAN | `receipts/{anc,head}-{plain,trace}.out` identical; `receipts/runs.txt`; `receipts/idiom_scan.txt` (Rule 11: 1 → 0) | R295-3 | a024ab51b926690be5ade8ec35ec1fa7dd23981b |
| Docs | CLEAN (S1 is a SUGGESTION only) | `tb/srp_stream_fsms/README.md:8,58-70,130-138`; PR body; issue #43 A262 comments; PR manager comment at `a024ab51` | R295-3 | a024ab51b926690be5ade8ec35ec1fa7dd23981b |

This round is a delta review. The full-scope lens coverage of the rest of PR #111 (RTL, docs and tests unchanged since `a14ef8b4`) is carried by R295-2 and R294-2 at `a14ef8b4`. This round establishes that nothing outside the one test file changed, and that the test file's behaviour is identical.

## 7. Real limits

- **Scope of reproduction.** I did not run the parent consumer gates (including `check_cpp_idiom` in its native tree-wide form), the donor bank, the full processor bank, lint or the builder banks. Rule 11 was reproduced with the parent's own checker over the processor's `tb/` C/C++ only, and the Makefile-level key only by inspection. The processor-wide 16,416-check bank at the head is taken from the hosted runs, not rerun here.
- **Suites run.** I ran only `tb/srp_stream_fsms`, at both commits. I did not rerun the other SRP suites, because their inputs are byte-identical.
- **Trace variant.** The trace build evaluates each check's printf arguments on every check, not only on failure. It was applied identically at both commits. The plain runs, which are the authoritative behaviour comparison, are also identical.
- **Build flag.** Builds used `-j 8` instead of the Makefile's `-j 0`, to respect the job cap. This does not affect simulation semantics.
- **Hardware.** Physical calibration was NOT RUN. Field and hardware skips are not hardware proof, and nothing here is.

## 8. Pending manager duties

- Hosted/act acceptance at the exact head. I inspected the hosted runs: six jobs succeeded and none was skipped.
- The final current-dev candidate at the merge turn: source base `939c1433`, live dev `57456af96b3127b9d309a995bbbd35a6113ce52d`, with the processor gitlink at `a024ab51`. This includes the parent consumer gates, `check_cpp_idiom` tree-wide, and the donor bank on that candidate.
- Publishing this packet (REPORT.md plus the files in MANIFEST.sha256). Optionally, publish the round-2b receipts next to `author-r2` (S1).
- Merge still requires two independent positive reviews at this head and the full completion bar.

## 9. Receipts and reproduction

The files are listed in `MANIFEST.sha256`, with paths relative to the packet root.

- `scripts/run_delta_probe.sh CLONE OUT_DIR VERILATOR [SCRATCH]`: the plain, trace, mutant and fault runs at both commits. It writes `receipts/*.out`, `*.warnings` and `runs.txt`.
- `scripts/idiom_scan.py CLONE CHECKER_PY COMMIT...`: Rule 11 with the parent's checker (fetch URL in `receipts/tool_identity.txt`). It writes `receipts/idiom_scan.txt`.
- `receipts/delta_scope.txt`, `receipts/clone_integrity.txt`, `receipts/hosted_checks.txt`, `receipts/hosted_suites_log_excerpt.txt`, `receipts/tool_identity.txt`, `receipts/verdict-before-prior-findings.txt`.

R295-3 FINISHED
