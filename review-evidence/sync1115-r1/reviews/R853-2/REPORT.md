[R853] POSITIVE - exact head e2be92b0e0f9a8f0529dea252f23ed44a21e050a

Internal independent review R853-2 of issue #665 / PR #934 (the dev sync), delta round. Tree `54c1e870df27971db88de7ad664a0078ca2cf9cf`.

- **Verdict: POSITIVE.** All five lenses were applied to the delta `6ceed753..e2be92b0` and are clean at this head. No BLOCKER, MAJOR or MINOR is open.
- Both prior public findings on this delta's subject are resolved at this head: R854-001 (PR #934 issuecomment-6932841237), and R853-1's F1 and F2 (issuecomment-6938623769).
- Two RESIDUE items and three SUGGESTIONs are recorded below. None of them changes a measurement, a verdict or a claim.
- **Scope note.** The brief names the round's delta as "6ceed753 to c10c549e", but the published head is `e2be92b0`. This round reviews all three commits on `6ceed753`:
  - `c10c549e`: the owner record and grading;
  - `ccc98b11`: the empty-build anchor;
  - `e2be92b0`: an unowned run-out fails.

## Scope reconstructed from public state

- **Read order.** AGENTS.md and CONTRIBUTING.md, then docs/README. Then #665's Q1 ruling (issuecomment-6930885185) and the round-5 REVIEW READY (#665 issuecomment-6942387001), which supersedes issuecomment-6940142843 and issuecomment-6936610025. Then FR_NFR.md 3.4.1 and the lwSRP / SRP-adapter sources the harness depends on. Then the delta and its history, then the public evidence archive.
- **Evidence archive.** `ea25c391` on `sync1115-review-evidence`: `author-r4` (round 4, at `c10c549e`) and `author-r5` (rounds 5 and 5b, at `e2be92b0`). It supersedes archive `c7bb132a` and holds the same `author-r4` packet.
- **Prior findings.** R854-1's and R853-1's findings were read only after this round's own pass over the diff, probes and ledger draft. No other reviewer's report for this round was read.
- **What changed.** The delta is harness, self-test and documents only. 14 paths, in `tb/verilator/ctrl_service_budget/` and `docs/reference/FR_NFR.md` (`receipts/restoration-and-delta.txt`).
  - The testbench is `sim_main.cpp`, `observers.py`, `observe.vlt` and `build.py`. Its last change is in `c10c549e`. After that, only the grader, the self-test and the docs change.
  - So the legs re-simulated at `c10c549e` and regraded at `e2be92b0` ran the head's testbench.

## Findings

No BLOCKER, MAJOR or MINOR.

### RES-1 - RESIDUE - Docs

- **Where:** `tb/verilator/ctrl_service_budget/README.md:168`, the "Each group's shortest and longest" bullet.
- **What:** it still says "or a late or absent build, prints `STATED` and fails the run". Since `e2be92b0`, an unowned run-out also fails the run (`mrpdu_grade.FAILING`; README:148 says so).
- **Why it is only wording:** no figure, check or verdict changes. The bullet does not say "only", and the rule is stated correctly two bullets earlier.
- **Exact fix:** "or a late, absent or unowned run-out, prints `STATED` and fails the run".

### RES-2 - RESIDUE - Docs

- **Where:** #665 / PR #934 public record. Also `tb/verilator/ctrl_service_budget/selftest_leaveall.py:267` ("#665's ruling on the fallback") and REVIEW READY #665 issuecomment-6942387001 ("the manager's ruling on round 5's open question").
- **What:** the decision behind `e2be92b0` is not on a public comment. That decision fails an unowned join or periodic run-out and removes the "latest participant's opportunity" fallback. It answers open question 1 of issuecomment-6940142843. The last public word on it is that question, and no ruling follows it on #665 or #934.
- **Why it is only wording:** the implemented behaviour is the stricter of the two published options and refuses rather than accepts. No measurement or verdict depends on where the ruling is recorded.
- **Exact fix:** the manager publishes the ruling on #665, and the PR body and the docstring's reference cite that comment.

### SUG-1 - SUGGESTION - Robustness, Tests

- **Where:** `tb/verilator/ctrl_service_budget/run.py:181` (`run_out_miss`) and `run.py:195` (`leave_all_miss`).
- **What:** an unowned LeaveAll run-out is named twice. The first line is "the leaveall timer's run-out ... (owner unresolved)", from `resolve`. The second is "the LeaveAll timer's run-out ... (LeaveAll owner unresolved)", from `leave_alls`. Reproduced by probe case H (`receipts/probe_owner.out`).
- **Impact:** both lines fail the run correctly. The duplicate only inflates the `STATED` list.
- **Option:** name it once, or keep both and say so in the README.

### SUG-2 - SUGGESTION - Robustness

- **Where:** `tb/verilator/ctrl_service_budget/mrpdu_grade.py:208` (`built`), the absent-vs-unresolved horizon. This is the author's open risk 2 in issuecomment-6942387001.
- **What:** a run-out with no build after it is `absent` only past the bound after the latest of every participant's opportunity, not its recorded owner's.
- **Impact:** only a log that ends within about one JoinTime of such a run-out can call it `unresolved`, which does not fail, where the owner's horizon would call it `absent`. The README states the rule exactly as coded (README:146).
- **Option:** now that every run-out has an owner, use the owner's opportunity for the horizon.

### SUG-3 - SUGGESTION - Tests

- **Where:** `tb/verilator/ctrl_service_budget/sim_main.cpp:422` (`note_owner`) and `sim_main.cpp:444` (`owner_of`).
- **What:** the register-file binding has no self-test arm or planted harness-side defect. The self-test exercises the grader on synthetic `ENTRY ... <owner>` lines only. The binding itself is evidenced by the real traces, which do discriminate:
  - the 26 re-run traces' 1,871 MRP run-outs all carry a resolved owner;
  - in every leg, the MSRP and MVRP LeaveAll expiries are 0.4 s or more apart (owner extracts, e.g. s10092 at 10.092 / 10.492 s);
  - seed s15032 has MVRP's expiry first, at 14.632 / 15.032 s;
  - probe case A-swapped shows that a swapped or positional binding fails both expiries (late and absent), so the 44 owned `sent` results could not have come from a wrong binding.
- **Not exercised by any real trace:** interface index > 0. The source supports it: `sw/firmware/ctrl/srp/srp_mbx.c:476` sets `i->index = n`, the mailbox interface that both the TX path (`tx_due` bit) and `mbx_pub_domain` use.
- **Option:** a later round could add a 2if trace with a LeaveAll, or one seed run with the application tag planted swapped, to show the testbench side fails by name.

### Comment rule

No new instance in the delta. All added source lines of `git diff 6ceed753..e2be92b0 -- '*.py' '*.cpp' '*.vlt'` were checked for lane labels, lane names, review rounds, reviewer IDs and issue-comment IDs. New comments cite "#665" and "PR #934", both issue/PR IDs. The overlap case is called "PR #934's overlap", with no reviewer or round named.

## Prior public review findings, resolved at this head

| Finding | Required outcome | Status at `e2be92b0` | Evidence |
|---|---|---|---|
| R854-001 (MAJOR; Conformance, Robustness, Tests, Docs): LeaveAll expiries bound to whichever participant's LeaveAll comes first | Bind each expiry to its interface and application by evidence independent of later output. Use it for the opportunity, missing/late output and first-MRPDU checks. Refuse or report unresolvable ownership. Add overlap, reordered and skipped/late/absent controls for both applications and interfaces. Regrade the eleven phases and the valid-destinations leg. Keep 49 ms. | **Resolved** | See the six points below the table. |
| R853-1 F1 (MINOR; Conformance, Robustness, Tests, Docs): a skipped LeaveAll escapes when another participant's expiry falls inside its join interval | Match each run-out to its own participant. Case B fails naming MSRP. An arm and a mutant hold it. | **Resolved** | The self-test's "inside another participant's join interval" arm is case B: MSRP named `skipped` at its 1,180 ms opportunity, MVRP `sent`. The earlier-rule owner mutant is caught by it (`receipts/probe_mutants.summary.txt`). |
| R853-1 F2 (MINOR; Conformance, Robustness, Tests): an empty build's lateness restarts at any participant's join callback | Anchor on the participant's opportunity from posted TICKs, not on any join callback. Case C is late. | **Resolved** | `mrpdu_grade.anchor` (`mrpdu_grade.py:252`) uses the recorded owner's `opportunity`, and an unknown owner is now `unowned`, which fails. That is stricter than the "latest participant" fallback F2 allowed (RES-2). The self-test arm holds C0 and C late at 59.979 ms and "own running" held. The earlier-rule mutant and the fallback-restored mutant are both caught. Probe cases E and F agree. |

R854-001 resolution evidence:
- **Binding at expiry:** `sim_main.cpp:338-347` prints the owner at the callback's own entry, from `a0`. `note_owner` binds each `timer_arg` at `shlan_timer_init(..., on_la_timer, arg)` inside `msrp_app_create` / `mvrp_app_create`, then at `mbx_pub_domain(index, false, ...)`. That matches `third_party/lwSRP/src/core/mrp_mad.c:903-912` and `srp_mbx.c:419-440`.
- **Grading:** `leave_alls` (`mrpdu_grade.py:273`) uses `log.owners` only.
- **Refusal:** an unowned or unresolved run-out fails (`LEAVE_ALL_FAILING`, `FAILING`).
- **Controls:** the self-test's overlap arm holds the reviewer's `participant_swap` case: MSRP named `skipped` at 1,180 ms, 191 ms late. Its clean and reordered arms pass. Its both-applications / both-interfaces arm names MVRP skipped on interface 1, MSRP late on interface 1 and MVRP absent on interface 0.
- **Regrade:** `author-r5/receipts/budget/regrade-at-e2be92b0.md`. The 22 eleven-phase groups: 44 LeaveAlls `sent`, none skipped, late, absent, unresolved or unowned. v1 (1x1/1if valid-destinations) rc 0.
- **Bound:** 49 ms unchanged. `LATE_MS` is still derived from `ctrl_loop.h`, which the delta does not touch.

## Per-lens results, with evidence

| Lens | Result | Artifact | What was checked, and against what |
|---|---|---|---|
| Conformance | PASS | `mrpdu_grade.py:200-296`; `docs/reference/FR_NFR.md:388`; `third_party/lwSRP/src/core/mrp_mad.c:851-870,903-912`; `sw/firmware/ctrl/srp/srp_mbx.c:419-440,476` | Q1 (IEEE 802.1Q-2018 10.7.4.1: the LeaveAll at the owner's next transmit opportunity) against `leave_alls`. The owner is its own participant (`timer_arg` per application and port). Its first MRPDU after the expiry must carry the LeaveAll, within 49 ms of its opportunity. The empty-build anchor is the owner's opportunity. The bound is unchanged. Probe A/A-swapped/B/C confirm each binding direction. |
| RTL | PASS | `git diff --name-only 6ceed753..e2be92b0` (no `hdl/`, `rtl/` or product path); `observe.vlt:43`; `observers.py:20,35` | The delta changes no product RTL, CDC, configuration or pin. The testbench only makes VexiiRiscv's `RegFileMem.asMem_ram` readable (`public_flat_rd`) and reads it at commit. The author's receipt shows the 26 re-run traces equal their earlier executions once the owner lines are removed, and the 13 firmware ELFs are byte-identical (issuecomment-6936610025). So the added observer changes no simulated behaviour. |
| Robustness | PASS | `sim_main.cpp:422-452`; `grade.py:166-175`; `mrpdu_grade.py:246-296`; `receipts/probe_owner.out` | Each failure path checked: an unbound or failed creation (not exactly one MSRP and one MVRP before the Domain) binds nothing, so it is unowned and fails; a missing record or an `unresolved` record is unowned and named; an owner silent after its expiry is absent; another interface's or application's LeaveAll answers nothing; a double expiry before one opportunity is answered by the one LeaveAll (case D, protocol-consistent); and logs with a mix of owned and unowned run-outs are graded per run-out (case H). The absent/unresolved horizon remains lenient at a log's end (SUG-2). The double naming is SUG-1. |
| Tests | PASS | `receipts/selftest-at-e2be92b0.txt`; `receipts/probe_mutants.summary.txt`; `receipts/readme-mutant-table-vs-selftest.txt`; `selftest_leaveall.py:104-298`; `selftest_mutants.py:868-902` | The self-test was run at this head on a clean clone: rc 0, 879 checks pass, 0 fail, 261/261 mutants caught. All 19 transmit and LeaveAll mutants were re-run alone, and each is caught by its named arm; the eight earlier ones are still effective. Each new arm can fail for its defect: the earlier-rule owner, fallback, interface-collapse and unowned-not-failing mutants are each caught. The README table's 19 rows match the self-test's first catching check. The binding's own test gap is SUG-3. |
| Docs | PASS | `tb/verilator/ctrl_service_budget/README.md:146-166,1379-1397`; `docs/reference/FR_NFR.md:388`; `receipts/docs-gates-spotcheck.txt`; `author-r5/receipts/workflows/verify-docs-at-e2be92b0.md` | README "What this proves" and FR_NFR 3.4.1 were compared with the code line by line. They state exactly what the grader proves: the owner recorded at expiry, the owner's next MRPDU carries the LeaveAll, within 49 ms of the owner's opportunity, "unresolved proves nothing", and an unowned run-out fails. They claim nothing for the wire (`T_egress`) or for unbound participants. Spot checks at this head: `docs_check.py` 0 findings (rc 0) and `check_doc_style.py` OK (rc 0). Added em-dashes: 0. The author's full docs jobs show 63 steps rc 0 and 34 NOT RUN, each with a reason. Wording residue: RES-1, RES-2. |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `mrpdu_grade.py` leave_alls/resolve/anchor; FR_NFR 3.4.1; lwSRP `mrp_mad.c` timers; `srp_mbx.c` create_participants; #665 Q1 ruling; probe_owner A to H | R853-2 | e2be92b0e0f9a8f0529dea252f23ed44a21e050a |
| RTL | CLEAN | delta path list (harness and docs only); `observe.vlt:43`; `observers.py`; author's trace-equality and ELF-identity receipts | R853-2 | e2be92b0e0f9a8f0529dea252f23ed44a21e050a |
| Robustness | CLEAN (SUG-1, SUG-2 optional) | `sim_main.cpp` note_owner/owner_of; `grade.py` entry; unowned/absent/unresolved paths; probe_owner B, C, D, G, H | R853-2 | e2be92b0e0f9a8f0529dea252f23ed44a21e050a |
| Tests | CLEAN (SUG-3 optional) | self-test rc 0, 879/0, 261/261; 19 transmit/LeaveAll mutants and their catching arms; README mutant table, 19/19 | R853-2 | e2be92b0e0f9a8f0529dea252f23ed44a21e050a |
| Docs | CLEAN (RES-1, RES-2 residue) | README:146-166 and the mutant table; FR_NFR:388; docs_check and doc_style at head; author's docs-job receipts | R853-2 | e2be92b0e0f9a8f0529dea252f23ed44a21e050a |

Code outside the delta keeps its earlier lens verdicts from this PR's prior rounds. The delta changes nothing that code depends on, apart from the grader's own ownership inputs, which this round covered.

## Executed by this round

All runs were in disposable copies under `scratch/`. The review clone was only read.

- **Harness self-test** on a clean clone of `e2be92b0`, with lwSRP and tsn-c-stack at their gitlinks: `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` gave rc 0, 879 PASS, 0 FAIL, 261 caught, 0 escaped, and porcelain 0. Receipt: `receipts/selftest-at-e2be92b0.txt`. The full log (850,874 B, sha256 `303dbfc2...`) stays in scratch.
- **`probe_owner.py`:** eight grader cases built with the self-test's own log builder, 0 unexpected (`receipts/probe_owner.out`).
- **`probe_mutants.py`:** all 879 checks pass unmutated, and each of the 19 transmit/LeaveAll mutants is caught, with every check it fails listed (`receipts/probe_mutants.summary.txt`).
- **README mutant table** against the self-test's first catching check: 19/19 match (`receipts/readme-mutant-table-vs-selftest.txt`).
- **Docs gates:** `docs_check.py` and `check_doc_style.py` pass at head. `check_em_dash.py` was NOT RUN because the pinned renderer is absent and no shared install was made. A substitute grep of the delta's added lines found 0 em-dashes (`receipts/docs-gates-spotcheck.txt`).
- **Evidence archive `ea25c391`:** every one of the 1,219 `author-r4`/`author-r5` files matches its `published_sha256` in MANIFEST.json (`receipts/evidence-manifest-verify.txt`).
- **Hosted checks at the head:** a read-only snapshot (`receipts/hosted-checks-snapshot.txt`) shows 16 completed successful, 1 skipped (physical gPTP), and 33 still queued or in progress. No hosted verdict is claimed here.

## Real limits

- **No simulation was run by this round.** The 26 re-run traces, the eleven 8x8/1if phases and the 1x1/1if valid-destinations leg are the author's published receipts. This round checked their hashes and the extracts and tables; their raw logs (over 200 KB each) are not published.
- **Only 1if is covered by real traces.** The owner binding at interface index > 0 rests on source reasoning and synthetic arms (SUG-3).
- **Known, not findings:**
  - every 8x8 leg exits 1 on #914's per-shape `STATED` polls-base costs;
  - #898's paced SET_CONFIGURATION record (305 against 300 at 1x1/1if) is refused by `record_classes.py` until the sync composes on #898's merge `cb96336d`;
  - #929, #916 and #919 remain as recorded.
- Physical calibration was NOT RUN, and field skips are not hardware proof.
- This round ran in the separate internal session the owner's 2026-09-23 decision provides for. No manager source bank ran at this head, and none is claimed.

## Pending manager duties

- Publish the ruling behind `e2be92b0` (unowned run-outs fail, no fallback) on #665, and link it from the PR body (RES-2). Carry RES-1 to the residue checklist.
- Build and validate the current-dev merge candidate at the merge turn: source base `659d7687`, live dev `6b66f66d89cf25d2717687bcc2c3bf617685a99a`, composed on #898's `cb96336d`. Run the builder and native banks, and regrade `record_classes.py` there.
- Own the hosted and act acceptance of the exact-head contexts still running (snapshot above).
- Obtain the second independent review. Merge needs two positive reviews and the full completion bar.

## Restoration

The review clone is at `e2be92b0e0f9a8f0529dea252f23ed44a21e050a`, tree `54c1e870` (write-tree equal), with porcelain 0 lines including submodules. The index (mode, blob, stage, path) hashes identically to the HEAD tree, `af809b92...`. All six gitlinks equal their checked-out submodule commits (`receipts/restoration-and-delta.txt`). No commit, push or GitHub write was made.

R853-2 FINISHED
