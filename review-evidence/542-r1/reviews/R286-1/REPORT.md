[R286] POSITIVE - exact head 68117c0bec0b767d38d9bb1150542e2346b615b7

# R286-1: internal independent review of PR #550 (issue #542)

- Head: `68117c0bec0b767d38d9bb1150542e2346b615b7`, tree `a66d547d152511b69f68f32dc6418212b52d30c8`.
- Source base: `615b5a5d7de01b23f15502e3732c6f2cb81ce74b`.
- Diff: `git diff 615b5a5d7..68117c0be` touches one file, `tb/verilator/milan_dp/sim_nxn.cpp` (+76 -24), in three commits:
  - `766b6a1`: the lever;
  - `6c5fa55`: the fix;
  - `68117c0`: the lever's liveness count.
- Commit messages: each is one line with no trailers, as CONTRIBUTING.md section 2 requires.
- Role: cleared-context internal reviewer.
- Reconstructed, in this order, from:
  1. AGENTS.md and CONTRIBUTING.md (sections 2 and 3);
  2. docs/README.md, and docs/development/CODE_QUALITY.md Rules 7 and 8;
  3. issue #542: the body with its frozen AC1-AC3, the `[A10] ASSIGNMENT` comment and the `[A233] REVIEW READY` comment;
  4. the PR description;
  5. the diff and history;
  6. the published evidence tree `review-evidence/542-r1` at `3b2ef4f`;
  7. this round's own executed probes.
- Every probe was built and run in a disposable clone under `scratch/`. The review clone was only read. See `receipts/restore_verify.txt`.

## Verdict basis

The frozen acceptance of #542 is met at this head. Executed evidence shows it:

- **AC1 (keep a copy or index, not a pointer).**
  - `notify_last()` returns a value copy, or an empty frame when nothing matches (`sim_nxn.cpp:1165-1177`).
  - The two holds the issue names are now values: `nB2` at `:1232`, taken at `:1331`, and `n1` at `:1374`. `nB1` at `:1289` is a value too.
  - `notify_seq` (`:1128-1130`) and `notify_same_from` (`:1192-1196`) take `const&` to a copy.
  - No function in the file returns a pointer, reference or iterator into `uns_log`.
- **AC2 (a forced-reallocation run shows no stale access).**
  - The lever (`:823-855`) frees the log's outer buffer at entry to `await_aecp` (`:860`) and `drain_tx` (`:891`).
  - Fixed code, lever on: every leg that runs the notify section passes, with only the lever's two lines added (`receipts/identity_summary.txt`):

    | Leg | Result |
    |---|---|
    | notify | 147/0 |
    | nxn | 1709/0 |
    | nxn8 | 3137/0 |
    | nxn4c | 1709/0 |
    | nxndv | 1711/0 |

  - Fixed code, lever plus AddressSanitizer:
    - notify: 147/0, 0 sanitizer lines (`run_notify_asan.log`);
    - nxn: 1709/0, 0 heap-use-after-free (`run_nxn_leverasan.log.gz`).
  - Old checks under the same final lever (`variant_oldchk.diff`):
    - notify 147/2 and nxn 1709/1. The failures are exactly the N5 `GET_NAME right after is byte-identical` bar and the `[NOTIFY-CRF] ...byte-identical ... to the solicited answer` bar (`run_notify_oldlever.log`, `run_nxn_oldlever.log`).
    - With AddressSanitizer: 4 heap-use-after-free, 8-byte reads in `notify_same_from`. Two are under `notify_section`, the N5 bar, and two under `prove_the_crf_input_counters_push_under_the_one_second_limit`. Each buffer was freed in `force_uns_log_realloc` under `await_aecp` and `aecp_xact_from` (`run_notify_oldasan.log`).
    - The same old checks without the lever give 146/0 (`run_notify_oldplain.log`).
    - The base under AddressSanitizer without the lever gives 146/0 and 0 sanitizer lines (`run_notify_baseasan.log`). The defect is latent, which is why the proof needs the lever.
- **AC3 (the milan_dp legs pass).** Plain runs at the head:

  | Leg | Result |
  |---|---|
  | main (`sim`) | 230/0 |
  | notify | 146/0 |
  | nxn | 1708/0 |
  | nxn8 | 3136/0 |
  | nxn4c | 1708/0 |
  | nxndv | 1710/0 |

  - Each of the five `sim_nxn.cpp` legs is **byte-identical** to the base source built the same way (`identity_summary.txt`).
  - The published author logs agree. `run-gate-*` and `run-dev-*` differ only by a shell `time` footer, and each published sha256 matches its manifest entry.

**No check was weakened.** Every check name, expected value and verdict is unchanged: the plain output is byte-identical to the base on five legs. Every rewritten predicate is equivalent on every reachable input:

- A match always passes `aecp_is_unsolicited` (`:817-819`, size > 37). So "empty copy" is exactly the old null pointer.
- `notify_seq` of an empty copy still gives -1.
- `notify_same_from` with an empty copy is still false.
- `ctr_word` and `memcmp` stay guarded.

## Findings against this head

No BLOCKER, MAJOR or MINOR finding is open.

**R286-S1 - SUGGESTION - Tests, Docs - `tb/verilator/milan_dp/sim_nxn.cpp:836-840` and `tb/verilator/milan_dp/Makefile` (no recipe sets `NOTIFY_REALLOC_TB`) - nothing runs the lever by default, so #542's regression guard is manual**

- Authority/evidence:
  - CODE_QUALITY.md Rule 8 says an arm counts only when an executed recipe runs it: "a driver named in a comment, in `echo`, or on a target nothing runs is not an arm".
  - The lever is set by no Makefile leg, CI job or README row. The PR body asks this question itself.
  - The defect is latent without the lever. At the base, AddressSanitizer alone is clean (146/0). So if a future change held a pointer, reference or iterator into `uns_log` across `await_aecp` or `drain_tx`, every gate would stay green.
- Why a SUGGESTION and not MINOR:
  - #542 AC2 asks for "a sanitizer or forced-reallocation run", which is a demonstration, and executed runs give it.
  - The assignment kept the lane to test-bench C++.
  - The fix removes the hazard structurally: nothing hands out a pointer to hold.
  - The lever is an ordinary `if (!kForceRealloc) return;` that every leg compiles, so it cannot rot syntactically.
  - It is not Rule 7 dead code: it serves the named requirement, and one flag reaches it.
  - AGENTS.md section 4 routes new work to a new Issue, not to scope growth.
- Impact: #542 stays fixed only as long as reviewers keep reading for pointer holds.
- Suggested outcome: the manager opens a follow-up Issue for one of two options, plus a README row.
  - Add a lever build to `make run`, for example a notify variant built with `-CFLAGS -DNOTIFY_REALLOC_TB=1`.
  - Or turn the lever on in an existing leg. It is harmless there: this round shows no verdict moves on notify, nxn, nxn8, nxn4c or nxndv, only the lever's own check is added, and no DUT cycle changes.
- Verification: `make run` prints `[ok] [NOTIFY] (#542 lever) the waits moved logs holding real frames`. A disposable mutant that restores a pointer hold then fails the suite.
- **The answer to the manager's question:** leaving the lever off the default targets is acceptable for merging #542. A follow-up Issue is recommended.

## Independent audit of every hold into `uns_log` (head)

The only writers of `uns_log` are:

- `push_back` at `:871` (`await_aecp`) and `:902` (`drain_tx`);
- the lever's `swap` at `:853`;
- `clear()` in `notify_clear` at `:1205`.

Every path that can push goes through those two waits: `aecp_xact`, `aecp_xact_from`, `notify_set_name`, `grade_read_desc`, and the section bodies that call them. Found by `grep -n uns_log`, plus a file-wide scan for pointer, `auto&`, `.back()`/`.front()` and iterator holds:

| Site | What is held | Held across a push or clear? |
|---|---|---|
| `:846-851` lever | its own iteration and move | no (it is the mover) |
| `:1149-1157` `notify_count` | loop-local `f` | no: the body calls only pure predicates |
| `:1167-1176` `notify_last` | loop-local `f`; returns a copy | no |
| `:1181-1187` `notify_when` | loop-local `f`; stamp read by value | no |
| `:1344-1352` `notify_ctr_when` | loop-local `f`; stamp read by value | no |
| `:1566-1572` N9 lambda | `uns_log[i]` within one expression | no. `p0 >= 0` short-circuits, so the lever's -1 stamps can never match |
| `nB1` `:1289`, `nB2` `:1331`->`:1232`, `n1` `:1374` | value copies | safe by construction |
| temporaries `:1325`, `:1386`, `:1612` | copies passed to pure readers | safe (full-expression lifetime) |

- **Outside the log.** `desc_of()` (`:548-552`) returns pointers into the `std::map` `desc_want`. The map is modified only by `clear()` at image build (`:374`), insertion at `:467`, and in-place `operator[]` writes at `:2062-2066`, none of which moves a node. It is not a hazard and is unchanged.
- The author's audit agrees with this table, and this round found no hold it missed.
- **The lever reaches both waits.**
  - Mutant `variant_mut_drainhold.diff` holds a reference into `uns_log` across `drain_tx(1)` at N2. Under the lever it fails 4 checks, and AddressSanitizer reports 8 heap-use-after-free.
  - Without the lever it gives 146/0 (`run_notify_drainhold*.log`, `run_notify_drainasan.log`).
- A real mid-wait reallocation moves elements (the `vector` move constructor is noexcept) exactly as the lever does, so the lever's model matches the real hazard.

## Lens coverage (evidence per lens)

```text
[R286] PASS Conformance - issue #542 AC1-AC3 vs sim_nxn.cpp:1165-1177,1232-1237,1289-1298,1331-1336,1374-1386 at 68117c0; receipts run_notify_{plain,lever,asan,oldlever,oldasan}.log, run_nxn_{plain,lever,oldlever}.log, identity_summary.txt - AC1 copies; AC2 lever/ASan clean at head and 2 FAIL + 4 heap-use-after-free on the old checks; AC3 six legs pass, five byte-identical to base; the Milan 5.4.5 content-bar semantics (frame named BEFORE the exchange vs the solicited answer) are kept because the copy is taken where the pointer was
[R286] PASS RTL - git diff --stat 615b5a5d7..68117c0 (one C++ file), gitlinks in restore_verify.txt, sim_nxn.cpp:856-911 - no hdl/, submodule or build-input change; the lever touches no DUT port and no cycle count (uns_log_cycle, lo/hi untouched) and plain vs lever outputs differ only by the lever lines on five legs
[R286] PASS Robustness - sim_nxn.cpp:1128-1130,1192-1196,1293-1296,1376-1379,1566-1572; receipts run_notify_absentasan.log, run_*_lever.log - absent frame (mutant M3) fails closed on all 12 notify_last consumers with 0 sanitizer lines; bounds guarded by size tests; lever -1 stamps unreachable by readers; lever inert (kForceRealloc=false) in every Makefile leg and harmless when on in all five sim_nxn legs
[R286] PASS Tests - receipts run_notify_{oldlever,oldasan,nolever,drainhold,drainasan,absentasan}.log, run_nxn_oldlever.log, run_nxn_leverasan.log.gz, run_notify_baseasan.log, cpp_idiom.log - the lever detects the defect on old code and is clean on new; its liveness check fails when the lever is dead (M1: 0 moves, 1 FAIL); it reaches drain_tx holds (M2); no check weakened (byte identity); check_cpp_idiom exit 0, selftest 75/75; S1 is optional
[R286] PASS Docs - sim_nxn.cpp:823-855,1160-1164,1190-1191,1313-1314,1373 comments; tb/verilator/milan_dp/README.md:26; docs_check.log (0 findings); PR #550 body - comments match executed behaviour (the "only two pushers" claim holds by grep); no authoritative document names the changed helpers; the PR body's commands reproduce the stated results; a lever README row is S1's optional scope
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #542 AC1-AC3; `sim_nxn.cpp` bars `:1232-1237`, `:1289-1298`, `:1331-1336`, `:1374-1386`; plain, lever and ASan runs of notify and nxn; byte identity on 5 legs | R286-1 | `68117c0bec0b767d38d9bb1150542e2346b615b7` |
| RTL | CLEAN | diff stat (C++ only); gitlinks; `await_aecp`/`drain_tx` DUT drive `:856-911`; lever-vs-plain identity | R286-1 | `68117c0bec0b767d38d9bb1150542e2346b615b7` |
| Robustness | CLEAN | helper bounds `:1121-1196`; N9 lambda `:1566-1572`; M3 absent-frame + ASan; lever on in 5 legs | R286-1 | `68117c0bec0b767d38d9bb1150542e2346b615b7` |
| Tests | CLEAN (R286-S1 and the retained R287-S2 are SUGGESTIONs) | old/new lever and ASan runs; mutants M1 (dead lever), M2 (drain_tx hold), M3 (absent); base ASan; nxn lever+ASan; `check_cpp_idiom` 0 and 75/75 | R286-1 | `68117c0bec0b767d38d9bb1150542e2346b615b7` |
| Docs | CLEAN | code comments `:823-855`, `:1160-1196`, `:1313-1314`, `:1373`; suite README; `docs_check` 0 findings; `git diff --check` clean; PR body | R286-1 | `68117c0bec0b767d38d9bb1150542e2346b615b7` |

## Prior public findings (resolved or retained at this head)

- **Process disclosure.** The PR's public comments contained the parallel R287-1 report. This round read it after:
  - its own diff pass and hold audit;
  - every notify, nxn and legs probe;
  - mutants M1, M2 and M3;
  - its lever decision (S1).

  That read came before this verdict and ledger were written, which departs from the instructed order. Receipt timestamps show every probe above finished by 08:41:59 CEST (`run_notify_absentasan.log`), and the comments were read at about 08:42.

  The only probe run after the read was `run_nxn_leverasan.log.gz`, to verify R287's OBS-1 independently. No verdict or finding here depends on R287. The issue's own comments are the assignment and REVIEW READY, and neither carries a finding.
- **R287-S1 (SUGGESTION, Tests/Docs: nothing runs the lever by default).** Retained. It is the same conclusion as R286-S1, reached independently.
- **R287-S2 (SUGGESTION, Tests: the liveness check is section-wide, not per hold).** Retained as a SUGGESTION. This round corroborates the premise without re-running R287's `oldna` probe:
  - In the untimed legs the lever moves a log holding a real frame exactly once per notify section. That move is the N5 exchange, and it is the one that fails the old N5 check.
  - The timed notify leg makes 258 such moves.
  - So the check proves that the lever fired, not that it fired inside each hold's window. The old-check runs prove the latter at this head. It matters only if the lever becomes a gate (S1).
- **R287 OBS-1 (out of scope, pre-existing: global-buffer-overflow at `sim_nxn.cpp:5741`).** Retained as a required new Issue. It is not a finding against this head.
  - Verified independently: the nxn leg under lever plus AddressSanitizer at this head reports 2169 global-buffer-overflow reads. Every one is `inject` (`:750`) called from `prove_the_rx_to_talker_loopback_lane` `:5741`, and there are 0 heap-use-after-free (`run_nxn_leverasan.log.gz`).
  - `git blame` puts the line in `b943c4a` (2026-09-04). The #542 diff does not touch it.

## Real limits

- **Executed:**
  - plain and lever runs of the notify, nxn, nxn8, nxn4c and nxndv legs, plus plain main (`sim`);
  - AddressSanitizer on the notify leg (head, old checks, base, M2, M3) and on the nxn leg (head, with the lever).
- **Not run here:**
  - AddressSanitizer on nxn8, nxn4c and nxndv;
  - the full parent, processor, gPTP, Yosys and builder banks;
  - act; hardware.
- **Toolchain.** Verilator 5.050 through the scoped wrapper (`receipts/tool_identity.txt`) with the host GCC 16.2.1. AddressSanitizer used `detect_leaks=0` (the author used 1). Leaks are not the question here.
- **Lever scope.** The lever makes a reallocation certain at the entry of each wait. A pointer taken inside a wait is not modelled, and none exists.
- **Physical calibration NOT RUN.** The hosted `Physical gPTP (nightly and manual)` context is SKIPPED, which is not hardware proof. The other 21 hosted contexts at the exact head completed with success (`receipts/hosted_check_runs.tsv`). That was observed only: the manager owns hosted and act acceptance.
- **Job-limit breach.** One background probe batch hit the command time limit and kept running while this round started its foreground re-runs. For about 4 minutes, two 8-job builds overlapped, up to 16 compile jobs, which exceeds the 8-job cap. The affected logs (`notify` baseasan and drainasan, and all four notify ASan runs) were then re-run on their own, with nothing else running. `status.txt` keeps the duplicate lines (`rerun ...`).
- **Redaction.** The published receipts replace the local home prefix with `$HOME`, and the 6 MB nxn ASan log is gzip-compressed. Nothing else was edited.

## Reproduction

Set `REPO` (a clone at the exact head with the three gitlinked submodules initialised), `PKT` (this packet) and `V` (Verilator 5.050), then:

```sh
scripts/run_matrix.sh prep
scripts/run_matrix.sh notify
scripts/run_matrix.sh nxn
scripts/run_matrix.sh legs
scripts/run_matrix.sh asan
scripts/run_matrix.sh nxnasan
```

- `scripts/probe_lib.sh` rebuilds each leg with its own `make -n run` recipe and records every command in `receipts/build_<leg>_<tag>.cmd`.
- `scripts/make_mutants.py` writes mutants M1-M3. Each one's pattern must match exactly once.

## Pending manager duties

- Build and validate the final current-`dev` candidate at the merge turn. The source base is `615b5a5d7`; live `dev` is `f86c34fe2ddbc6cfb7c8c70ddbe0d9726f4d3c2f`.
- Own hosted and act acceptance.
- Open a follow-up Issue for R286-S1 / R287-S1 (a lever target plus a README row); S2 folds into it.
- Open a new Issue for R287 OBS-1 (the `sim_nxn.cpp:5741` `len` of 2000 against a 120-byte frame).
- Get the second positive review. R287-1 is positive at this head.
- Obtain maintainer merge authorization, then check post-merge containment.

R286-1 FINISHED
