[R287] POSITIVE - exact head 68117c0bec0b767d38d9bb1150542e2346b615b7

# R287-1: external independent review of PR #550 (issue #542)

- Head: `68117c0bec0b767d38d9bb1150542e2346b615b7`, tree `a66d547d152511b69f68f32dc6418212b52d30c8`.
- Source base and live `dev`: `615b5a5d7de01b23f15502e3732c6f2cb81ce74b`.
- Diff under review: `git diff 615b5a5d7..68117c0be`, which touches one file, `tb/verilator/milan_dp/sim_nxn.cpp` (+76 -24), in three commits: `766b6a1` (the lever), `6c5fa55` (the fix) and `68117c0` (the lever's liveness count). Each commit message is one line with no trailers.
- Role: cleared-context external reviewer. Reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, issue #542 (body, assignment comment and REVIEW READY comment), the PR description, the diff and history, and executed probes.
- Prior public review findings were read only after this verdict and ledger were written. See "Prior public findings" at the end.

## Verdict basis

The frozen acceptance of #542 is met at this head, and executed evidence shows it:

1. **Copies, not pointers (AC1).** `notify_last()` now returns a value copy (`sim_nxn.cpp:1165-1177`). The two holds the issue names are values: `nB2` at `:1232` (from `:1331`/`:1336`) and `n1` at `:1374`. `nB1` at `:1289` is also a value. No helper in the file returns a pointer, reference or iterator into `uns_log` any more.
2. **No stale access under forced reallocation (AC2).**
   - At the head with the lever: notify 147/0 and nxn 1709/0. Each differs from its plain run only by the lever's two lines.
   - At the head with the lever and AddressSanitizer: notify has 0 sanitizer lines, and nxn has 0 heap-use-after-free (nxn does carry a pre-existing, unrelated report; see OBS-1).
   - The same lever against the old checks (`766b6a1`): notify 147/2 and nxn 1709/1. The failures are exactly the N5 and `[NOTIFY-CRF]` byte-identical bars. With AddressSanitizer there are 4 heap-use-after-free reads in `notify_same_from`, two from `notify_section` (N5) and two from `prove_the_crf_input_counters_push_under_the_one_second_limit`.
3. **The milan_dp legs pass (AC3).**
   - notify 146/0 and nxn 1708/0, byte-identical to the base.
   - The manager's full source banks and the hosted exhaustive gates are green at this head (receipt `hosted_check_runs.tsv`). The manager owns that acceptance.

No check was weakened. Every changed predicate is equivalent on every reachable input, because a match is always longer than 37 bytes (`aecp_is_unsolicited`, `:817-819`), and the plain legs' output is byte-identical to the base. A mutation making `notify_last()` always answer "absent" fails 12 checks: every consumer fails closed.

## Findings against this head

No BLOCKER, MAJOR or MINOR finding is open. Two SUGGESTIONs (optional, not coverage-affecting):

**R287-S1 - SUGGESTION - Tests, Docs - `tb/verilator/milan_dp/sim_nxn.cpp:836-840` and `tb/verilator/milan_dp/Makefile` (no target) - the lever is not run by any default target**
- Authority/evidence: `NOTIFY_REALLOC_TB` is the only preprocessor switch in `sim_nxn.cpp` that no Makefile leg sets. Every other switch is set by a leg: `AX8X8_TB`, `DIVERGENT_TB`, `LB_SEQ_FIXED`, `LOOPBACK_TB`, `MS_CYC_TB`, `NOTIFY_TIMED_TB` and `NSTREAMS_TB`. No CI job and no README row names the lever.
- Why this is not MINOR:
  - AC2 of #542 asks for a demonstration run, and executed runs at this head give it.
  - The fix removes the hazard structurally: `notify_last()` is by value, so nothing hands out a pointer to hold.
  - The lever's body is an ordinary `if (!kForceRealloc) return;` rather than an `#ifdef` region, so every leg still compiles it and it cannot rot syntactically.
- Impact: a future change that reintroduces a pointer, reference or iterator into `uns_log` held across `await_aecp`/`drain_tx` would pass every gate, because the defect is latent without the lever. The plain AddressSanitizer run at the base is clean (`notify_base_asan.log`: 146/0, 0 sanitizer lines).
- Suggested outcome: open a follow-up Issue that either adds a lever target (a notify variant built with `-DNOTIFY_REALLOC_TB=1`, which costs about 15 s to build and 13 s to run here) with a README row, or turns the lever on in the existing `obj_notify` leg. It only adds empty entries that no reader matches, and this review shows the leg's verdicts do not move.
- Verification: the new target runs in `make run`/CI and prints `[ok] [NOTIFY] (#542 lever) ...`.

**R287-S2 - SUGGESTION - Tests - `tb/verilator/milan_dp/sim_nxn.cpp:1242-1248` - the lever's liveness check is section-wide, not per-hold**
- Evidence: probe `oldna` takes the old pointer checks with the lever and deletes only the lever call in `await_aecp` (`receipts/oldna.diff`). The notify leg then gives 147/0: both old pointer bars PASS and the liveness check still passes, with 315 moves, all from `drain_tx`.
- Scope: the check's printed claim ("the waits moved logs holding real frames") is accurate as stated. It does not claim to prove that the exchange each hold crosses was moved, and the nxn leg's count is exactly 1, which is the N5 exchange.
- Impact: in a lever build, losing the `await_aecp` call silently removes the proof for exactly the two holds of #542.
- Suggested outcome, if the lever is kept as a gate (see S1): count moves inside `aecp_xact_from`/`await_aecp` separately and require at least one in each of the N5 and `[NOTIFY-CRF]` bar windows.
- Verification: the `oldna` probe fails the lever check.

## Out-of-scope discovery (new Issue required; NOT a finding against this head)

**OBS-1 - pre-existing global-buffer-overflow in the nxn leg, `tb/verilator/milan_dp/sim_nxn.cpp:5741`**
- The defect: `inject(mkaaf(sidB, static_cast<uint8_t>(120 + s), 2, LB_PAY0), 2000);` passes `2000` as `len`, the second parameter of `inject` (`:744`). `mkaaf` returns a 120-byte static buffer (`:1059`). Every other `inject(mkaaf(...), ...)` call passes 120. So `inject` reads 1880 bytes past the buffer, and the loopback-lane listener is fed 2000-byte frames with trailing garbage.
- Sanitizer evidence: AddressSanitizer reports 2169 global-buffer-overflow reads, all from `prove_the_rx_to_talker_loopback_lane`. The count is identical at the base (`nxn_base_asan.log.gz`, line `:5689` there) and at the head (`nxn_head_lasan.log.gz`), and both runs pass their checks (1708/0 and 1709/0).
- Why it is out of scope: the line was last changed in `b943c4a` (2026-09-04), and it is outside `uns_log` and outside #542's scope. This PR neither introduced nor touched it. The PR's AddressSanitizer claim covers only the notify leg, and that claim is accurate.
- Per AGENTS.md section 4, newly discovered work becomes another public Issue. The manager should open one: the call site should pass the frame length (120) and, if it meant it, a drain of 2000. The nxn leg under AddressSanitizer should then be clean.

## Independent audit of every hold into `uns_log` (at the head)

The only writes to `uns_log`:

- `push_back` at `:871` (`await_aecp`) and `:902` (`drain_tx`);
- the lever's swap at `:853`;
- `clear()` at `:1205` (`notify_clear`).

Every call that can push goes through `await_aecp`/`drain_tx`, directly or via `aecp_xact`, `aecp_xact_from`, `notify_set_name` and `grade_read_desc`. Every access (`grep uns_log`) is one of these:

| Site | Hold | Crosses a push or clear? |
|---|---|---|
| `:846-851` lever | the lever's own iteration and move | no (it is the mover) |
| `:1149-1157` `notify_count` | loop-local `f` | no: the body calls only `aecp_is_unsolicited`, `notify_cmd`, `notify_to` |
| `:1167-1176` `notify_last` | loop-local `f`; returns a copy | no |
| `:1181-1187` `notify_when` | loop-local `f`; `uns_log_when[i]` by value | no |
| `:1344-1352` `notify_ctr_when` | loop-local `f`; stamp by value | no |
| `:1566-1572` N9 lambda | `uns_log[i]` indexed within one expression | no; `p0 >= 0` short-circuits, so the lever's `-1` stamps never match |
| `nB1` `:1289`, `nB2` `:1331`/`:1232`, `n1` `:1374` | value copies | safe by construction |
| temporaries `:1325`, `:1386`, `:1612` | `notify_last()` copies passed to a pure reader | safe; lifetime ends at the full-expression |

No alias of `uns_log` exists: no reference or pointer variable binds the container. `desc_of()` (`:548-552`) returns pointers into the `std::map` `desc_want`. Map insertion (including `operator[]` at `:2062-2063`) does not move nodes, and `clear()` runs only at image build (`:374`). This is outside `uns_log` and unchanged. The author's published audit agrees with this table, and I found no hold it missed.

## Lens coverage (evidence per lens)

```text
[R287] PASS Conformance - issue #542 AC1-AC3 vs sim_nxn.cpp:1165-1177,1232-1237,1289-1298,1331-1336,1374-1386 at 68117c0 and receipts notify_*/nxn_* - AC1 copies; AC2 lever+ASan clean at head, 2 FAIL + 4 heap-use-after-free on old checks; AC3 notify 146/0, nxn 1708/0 byte-identical to base; the Milan 5.4.5 content-bar semantics (the frame named BEFORE the exchange vs the solicited answer) are preserved: copy taken at the old pointer's point
[R287] PASS RTL - git diff --stat 615b5a5d7..68117c0 (one C++ file) and git submodule status (pins unchanged) - no hdl/, submodule or build-input change; DUT drive in await_aecp/drain_tx unchanged (lever touches no port and no cycle count: uns_log_cycle identical, outputs byte-identical)
[R287] PASS Robustness - sim_nxn.cpp:1128-1130,1192-1196,1293-1296,1376-1379,1566-1572 and receipts notify_mutempty.log, notify_head_lever.log - absent frame (empty copy) fails closed on all 12 consumers; bounds guarded by size tests (notify_seq no longer relies on at()); lever's -1 stamps unreachable by the N9 lambda; lever inert (kForceRealloc=false) in every Makefile leg
[R287] PASS Tests - receipts notify_old_lever/nxn_old_lever/notify_old_lasan (fail on old), notify_head_lever/nxn_head_lever/notify_head_lasan/nxn_head_lasan (clean on new), notify_base_asan (latent without lever), notify_oldna_lever, notify_mutempty - the lever demonstrably detects the defect it claims; no check weakened; S1/S2 are optional
[R287] PASS Docs - sim_nxn.cpp:823-855,1160-1164,1190-1191,1313-1314,1373 comments; tb/verilator/milan_dp/README.md:26 (obj_notify row) and docs_check.py 0 findings - comments match executed behavior (the "only two pushers" claim verified by grep); no authoritative doc names the changed helpers; PR body carries reproducible commands; lever README row is S1's optional scope
```

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #542 AC1-3; `sim_nxn.cpp` bars `:1232-1237`, `:1289-1298`, `:1374-1386`; notify/nxn plain, lever and ASan runs | R287-1 | `68117c0bec0b767d38d9bb1150542e2346b615b7` |
| RTL | CLEAN | Diff stat (C++ only); submodule gitlinks; `await_aecp`/`drain_tx` DUT drive `:856-911` | R287-1 | `68117c0bec0b767d38d9bb1150542e2346b615b7` |
| Robustness | CLEAN | Helper bounds `:1121-1196`; N9 lambda `:1566-1572`; `mutempty` probe; lever-off path | R287-1 | `68117c0bec0b767d38d9bb1150542e2346b615b7` |
| Tests | CLEAN (S1 and S2 are SUGGESTIONs) | old-vs-new lever and ASan runs; `oldna` and `mutempty` mutations; base-vs-head byte identity; `check_cpp_idiom` 0 and selftest 75/75 | R287-1 | `68117c0bec0b767d38d9bb1150542e2346b615b7` |
| Docs | CLEAN | Code comments `:823-855`, `:1160-1196`, `:1313-1314`, `:1373`; suite README; `docs_check` 0 findings; `git diff --check` clean | R287-1 | `68117c0bec0b767d38d9bb1150542e2346b615b7` |

## Real limits

- Only the two legs that carry the holds were built and run here (notify and nxn, the plain, lever and ASan variants). nxn8, nxndv, nxn4c and the main leg were not run by this review. They are the manager's banks. The diff's effect on them is limited to the same byte-identical helper semantics.
- Verilator 5.050 through the scoped wrapper (`--version` prints `Verilator 5.050 2026-07-01 rev v5.050`), with the host C++ toolchain. AddressSanitizer detects only accesses that execute. The lever makes the reallocation certain, but only at call entry. A realistic mid-wait reallocation is covered by equivalence, since any hold across the call is invalidated either way.
- Physical calibration was NOT RUN. The hosted `Physical gPTP (nightly and manual)` context is SKIPPED, which is not hardware proof. Every other hosted context at this head completed success (`hosted_check_runs.tsv`). This review did not run act, the full banks, Yosys or the builder.
- The published receipts replace the local home prefix with `$HOME`, and the two 6 MB nxn ASan logs are gzip-compressed. Nothing else was edited.

## Reproduction

`probe.sh` (listed in `MANIFEST.sha256`) reproduces every run from a clone at the exact head:

```sh
export REPO=<clone at 68117c0> V=<verilator 5.050> PKT=<this packet>
./probe.sh prep
./probe.sh build notify head_lever && ./probe.sh run notify head_lever
```

- Tags: `base`, `head`, `old` (`766b6a1`), `oldna` and `mutempty`, each optionally suffixed `_lever`, `_lasan` or `_asan`.
- `probe.sh clean` removes every untracked artifact, and `receipts/restore_verify.txt` records the restored clone.
- `receipts/builds.txt` and `receipts/runs.txt` record every build and run with its exit status. The per-run logs are `receipts/<leg>_<tag>.log`, and the exact build lines are `receipts/build_<leg>_<tag>.cmd`.

## Pending manager duties

- Build and validate the final current-`dev` candidate at the merge turn (source base `615b5a5d7`), and own hosted/act acceptance.
- Open a new public Issue for OBS-1 (the `sim_nxn.cpp:5741` length/drain mix-up and its 2169 AddressSanitizer reads).
- Decide on S1/S2: a follow-up Issue for a lever target is recommended but not required for merge.
- Maintainer merge authorization; post-merge containment.

## Prior public findings

Read after the verdict and ledger above were written. The PR has 2 conversation comments and no review or inline comment; the issue's public comments were read at the start of the round.

- The PR's only comments are two coordinator notices, `[A10] INDEPENDENT REVIEW STARTED: R287-1` and `R286-1`. Neither carries a finding.
- The issue's comments are the assignment (`[A10] ASSIGNMENT`) and the executor's `[A233] REVIEW READY`, and neither carries a review finding.

There are no prior public review findings on this PR to resolve or retain at this head. R286-1 runs in parallel and independently; this report did not read it.

R287-1 FINISHED
