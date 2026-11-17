[R853] NEGATIVE - exact head 9aa55d3b382750353709c3ba9ff6f6416938e83b

R853-3, internal independent narrow-delta review of issue #665 / PR #934 (dev sync), round 6: `e2be92b0..9aa55d3b`
(commits `1238a3ee`, `9aa55d3b`). Tree `fc52e64fd482c3185620b6d00048c2b2608f7d06`. All five lenses applied.

One MAJOR remains. R854-2-F1's demonstrated branches are fixed: the missing-build deadline, the frame that answers a
run-out, and the start of the service row now come from the recorded owner. R854-2's probe now exits 0. But the branch
for "no frame from the owner" still judges the run-out on whichever participant built first. So a timely build by
another participant that sends its own MRPDU still hides the owner's late MRPDU. At `e2be92b0` this case graded
`released` (on the other participant's frame); at this head it grades `empty`. In both, nothing fails. This is a
grader soundness defect, not evidence of a product transmission defect.

## Finding

### R853-3-F1 - MAJOR - Conformance, Robustness, Tests, Docs

- **Title:** when another participant builds first, its timely frame-bearing build still stands in for an owned
  run-out's missing owner build, so the owner's late MRPDU passes.
- **Where:**
  - `tb/verilator/ctrl_service_budget/mrpdu_grade.py:228-234` (`built`): `first` is the first `build_mrpdu` of any
    participant (`window`, :253-283), and `:234` returns `empty` when `first` is within 49 ms of the owner's
    opportunity.
  - `selftest_leaveall.py:302-343` (`foreign_checks`): the `within` case at :319 asserts `empty` for a timely foreign
    build. It has no later owner frame, so the control encodes the rule but cannot see the escape.
  - Claims: `README.md:146` ("judged on its owner alone"), `README.md:150`, `README.md:171`, the `mrpdu_grade.py`
    docstring at :15-25, and `docs/reference/FR_NFR.md:388`.
- **Authority:**
  - [#665 Q1](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6930885185): lateness counts from the
    participant's own transmit opportunity (IEEE 802.1Q-2018 10.7.4.1, bound 49 ms).
  - R854-2-F1's required outcome
    ([PR #934](https://github.com/kebag-logic/milan-fpga/pull/934#issuecomment-6942847358)): "Another participant's
    callback, running join timer or emitted frame must not defer that expiry's deadline or satisfy its service row",
    and "use each recorded owner's transmit opportunity consistently to judge missing and late service".
  - Firmware structure: `build_mrpdu` builds exactly one participant's MRPDU (`sw/firmware/ctrl/srp/srp_mbx.c:1091-1099`,
    `participant(i,slot)`). `transmit()` builds the slots of an interface in order, MSRP and then MVRP, one per slice
    at both points (`srp_mbx.c:1224-1262`). It serves the first interface that owes a build first. So a build that
    commits only another participant's MRPDU is positively known not to be the owner's build.
- **Evidence:** `probe_owner_build.py <checkout>`, receipt `receipts/probe_owner_build.log` (rc 0, a report-only
  probe). Every case uses an owned periodic run-out at 1,300.001 ms whose owner's opportunity is the run-out itself.
  Every case was run for all four owners (MSRP and MVRP on interfaces 0 and 1).

  | Case | Log after the run-out | Expected (owner-bound) | Observed at `9aa55d3b` | At `e2be92b0` |
  |---|---|---|---|---|
  | O (control) | owner's own MRPDU at 1,431 ms | late, 131 ms | late, named with owner and 1,300.001 ms opportunity | (not run) |
  | **F** | other application on the other interface builds and commits its MRPDU at 1,311 ms; the owner's MRPDU at 1,431 ms, in a later build run | late, 131 ms | **`empty`, no finding, no row** | `released`, no finding, row on the *other* interface 11.0 ms |
  | FE | a build that sends nothing at 1,311 ms; the owner's MRPDU at 1,431 ms | late if the 1,311 ms build is not the owner's | `empty`, no finding | `empty` |
  | J (control) | owner's own join timer runs to the 1,430 ms TICK; owner's MRPDU at 1,431 ms | released, ~1 ms from the owner's own opportunity | released, row 1.0 ms | (not run) |
  | JF | J plus another participant's MRPDU at 1,311 ms | released, owner's row | `empty`, no row | (not run) |

  - Case F is R854-2's frame-bearing escape with the other participant's build moved inside 49 ms. Only the outcome
    label changed (`released` to `empty`); the owner's 131 ms delay still escapes
    (`receipts/probe_owner_build_at_e2be92b0.log`).
  - Case JF shows the same branch: a build made before the owner's own opportunity is accepted as the owner's empty
    build, and the owner's timely MRPDU gets no row.
  - Case FE is the same branch with a build that sends nothing. The trace names no participant for a `build_mrpdu`
    entry, so the grader cannot tell whose empty build it was.
- **Impact:**
  - For an MVRP-owned run-out, the MSRP build of the same interface always comes first. So does every interface-0 build
    when interface 0 also owes one and the owner is on interface 1.
  - If the owner's own build is delayed past 49 ms, which is the CPU service failure this gate exists to catch, more
    than one pass falls between the two builds. `window` then splits them into separate runs, and the run-out grades
    `empty`.
  - The escape is reachable by construction. It was not shown to occur in the published traces, but those traces cannot
    rule it out:
    - 50 of the 73 moved run-outs are if0 MVRP run-outs answered only by if0 MSRP's frame.
    - `r6_compare.py:69` computes `owner_frame_after_opportunity_ms` only inside the same window, so it is `null` for
      every `empty` by construction. It does not show where, or whether, the owner built.
- **Why the claims are not just wording:** README:146 says "judged on its owner alone". README:150 and the docstring
  say another participant's frame never "answers" the run-out. FR_NFR:388 states what is proven per expiry. FR_NFR's
  per-build sentence ("the first runs within 49 ms") is literally accurate. But the claims together state an owner-bound
  conformance property that this branch does not establish.
- **Required outcome:**
  - An owned run-out's empty or late judgement must rest on a build that can be the owner's.
  - A build whose frames are all another participant's must never settle the owner's deadline. Neither must any build
    before the owner's own opportunity.
  - Where the trace cannot tell whose a build was that sent nothing, the grader must either resolve it or classify it
    conservatively. It must not pass it as the owner's empty build. Alternatively, the README and FR_NFR 3.4.1 must
    state the remaining limit, with a public ruling that accepts it.
  - Unchanged: legitimate empty builds, owed-frame retries, short logs, the owner's own running join timer, and the
    49 ms bound.
  - How to get there is the author's choice. Examples: record the build's participant the way the timer callbacks'
    argument is recorded, or skip builds known to be another participant's.
- **Verification:**
  - `probe_owner_build.py` case F reports `late` for each of the four owners, named by the owner at its 1,300.001 ms
    opportunity.
  - Cases O and J keep their results.
  - A standing control and a mutant restore the "first build of any participant" association.
  - R854-2's `probe_missing_build.py`, the self-test and the affected regrades are re-run. The regrade lists, for each
    move to `empty`, where the owner's own build or frame came.

No other BLOCKER, MAJOR or MINOR.

### R853-3-RES-1 - RESIDUE - Docs (carried, R853-2 RES-1)

- `tb/verilator/ctrl_service_budget/README.md:172` still reads "or a late or absent build, prints `STATED` and fails the
  run". An unowned run-out also fails the run (README:151).
- **Exact fix:** "or a late, absent or unowned run-out, prints `STATED` and fails the run".

### R853-3-SUG-1 - SUGGESTION - Tests

- `README.md` mutant table: two existing mutants' catching checks changed in `9aa55d3b`. They now name the overlap and
  join-interval checks, which catch them first at this head. That is correct, as my self-test confirms.
- Optional: the "build that sends nothing late only past the last join callback" mutant is now first caught by a
  LeaveAll overlap check, not by the anchor check written for it. A one-line note would keep a reader from thinking the
  anchor check lost its discrimination.

## Prior public findings: disposition at this head

My independent pass over the delta, the probe and the draft verdict were done before I read the R853-1, R853-2 and
R854-1 reports. I read R854-2-F1 first because it defines this round's focus; this report says so for transparency.

| Prior finding | Disposition at `9aa55d3b` |
|---|---|
| R854-2-F1, MAJOR | **Demonstrated branches resolved.** `probe_missing_build.py` rc 0: 8 absent and 8 late cases, each named by the actual owner at 1,300.001 ms. The four short-log controls stay unresolved. `horizon`, `served` and `start_of` are owner-bound, and the row on the other interface is gone. **The required outcome's general clause is still unmet** in the no-owner-frame branch: retained at its cause as R853-3-F1. |
| R854-001 (R854-1), MAJOR | LeaveAll binding unchanged by this delta. R854-2's `probe_ownership.py` gives 60 controls, 0 failures, and `check_focused_mutants.py` catches 15 of 15 at this head. Its periodic and missing-build remainder is R854-2-F1 above. |
| R853-1 F1, MINOR | Resolved (unchanged code). Its self-test check passes at this head. |
| R853-1 F2, MINOR | Resolved for its callback cause: `anchor` is owner-bound and its check passes. The empty-build branch's *build* identity is R853-3-F1's FE and JF cases, which is a different cause. |
| R853-2 RES-1 | Still present: R853-3-RES-1. |
| R853-2 RES-2 | Manager's: the unowned-fallback ruling is to be published. |
| R853-2 SUG-2 | Implemented (`horizon` is the owner's opportunity). SUG-1 and SUG-3 are unchanged and optional. |

## Per-lens results

- **Conformance:** UNCLEAN, R853-3-F1.
  - Artifacts: `mrpdu_grade.py:212-299`, against #665 Q1 and 802.1Q 10.7.4.1.
  - The 49 ms bound and `LATE_MS` are unchanged.
  - Owner binding holds for the horizon, the frames and the row start, in both applications on both interfaces
    (my cases O and J, R854-2's probe, the author's `foreign_checks`).
- **RTL:** PASS. The delta touches only nine files, all of them `tb/verilator/ctrl_service_budget/*.py`,
  `README.md` and `FR_NFR.md` (`git diff --stat e2be92b0..9aa55d3b`).
  - There is no product RTL, firmware, `sim_main.cpp`, observer, build input, configuration, gitlink or bound change.
    The prior RTL verdict stands.
  - The firmware read in `srp_mbx.c:1091-1262` is used only as authority for F1.
- **Robustness:** UNCLEAN, R853-3-F1 (cases F, FE, JF).
  - Checked clean: short logs stay unresolved; the owner's own running join timer, and another participant's running
    join timer, do not defer the horizon; the unowned path (`resolve:217-219`) is unchanged and fails the run.
- **Tests:** UNCLEAN, R853-3-F1.
  - `foreign_checks` and the four new mutants discriminate their own associations. Each is caught by name
    (`receipts/selftest-extract.txt`).
  - No control holds a timely foreign build ahead of a late owner build.
  - The `selftest_notice.py:53` frame change (from an all-zero frame to an MSRP MRPDU) is required by the owner-frames
    rule. It does not weaken the test: the 19 and 21 ms limits and the "no frame, no row" check are unchanged.
  - The `selftest_polls.py:333` change is message text only.
- **Docs:** UNCLEAN, R853-3-F1 (owner-alone claims, listed above), plus RES-1.
  - The new delta's source comments cite only `PR #934` and requirement clauses. They have no lane labels, review
    rounds, reviewer IDs or issue-comment IDs. `git diff --check` rc 0.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R853-3-F1) | mrpdu_grade.py:141-299; #665 Q1; 802.1Q 10.7.4.1; srp_mbx.c:1091-1262; probe_owner_build.log; R854-2 probe | R853-3 | 9aa55d3b382750353709c3ba9ff6f6416938e83b |
| RTL | CLEAN | delta file list (9 harness and doc files); no RTL, firmware or testbench-C++ path in `git diff --stat e2be92b0..9aa55d3b` | R853-3 | 9aa55d3b382750353709c3ba9ff6f6416938e83b |
| Robustness | UNCLEAN (R853-3-F1) | built/horizon/served/window/anchor; probe cases F, FE, J, JF; short-log and unowned controls | R853-3 | 9aa55d3b382750353709c3ba9ff6f6416938e83b |
| Tests | UNCLEAN (R853-3-F1) | selftest_leaveall.py:302-343; selftest_mutants.py:881-892; selftest_notice.py:53; selftest_polls.py:333; full self-test rc 0, 882 PASS, 265 caught | R853-3 | 9aa55d3b382750353709c3ba9ff6f6416938e83b |
| Docs | UNCLEAN (R853-3-F1; RES-1 non-blocking) | README.md:146-172, 234, 1382-1400; FR_NFR.md:388; mrpdu_grade.py docstring :1-25; run.py:181-196; join_grade.py:66-90 | R853-3 | 9aa55d3b382750353709c3ba9ff6f6416938e83b |

## Executed by this round (commands from this packet; `<checkout>` is a git-archive extraction of the exact head with submodules at their gitlinks)

| Command | Result |
|---|---|
| `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` | rc 0; 882 PASS, 0 FAIL, 265 `MUTANT caught`, "self-test: 0 failures" (the count matches the author's 882 and 265). Full log sha256 `ef10b292...` (865,092 bytes, the author's size; the digest differs from the author's `5a432a41...`, and I did not investigate why) |
| `python3 -B probe_missing_build_r854_2.py <checkout>` (R854-2's script, unchanged) | rc 0; 0 hidden missing builds, 0 hidden late builds |
| `python3 -B probe_ownership_r854_2.py <checkout>` | rc 0; 60 controls, 0 failures |
| `python3 -B check_focused_mutants_r854_2.py <checkout>` | rc 0; 15 of 15 caught |
| `python3 -B probe_owner_build.py <checkout>` | the R853-3-F1 table above |
| `python3 -B probe_owner_build.py <e2be92b0 extraction>` | case F `released`, with a row on the other interface |
| `python3 -I audit_r6_packet.py <archive>/review-evidence/sync1115-r1 <archive MANIFEST.json>` | rc 0. All 217 author-r6 files match the archive manifest's published sha256. 216 match INDEX.md, plus the two docs-gate logs the manifest marks path-redacted; INDEX.md carries their pre-redaction digests, which is not a defect. All 13 legs' `table.md` are byte-identical to round 5b's (`author-r5/.../legs-at-e2be92b0`) with rc unchanged (v1 0, others 1). 73 of 1,871 run-outs moved, all released to empty (46 join, 27 periodic): 50 owned by if0 MVRP and answered before by if0 MSRP, 23 the reverse. None moved to late, absent or unowned |
| Source integrity (`receipts/source-state.log`) | HEAD `9aa55d3b`; index clean; no untracked or ignored files; five required gitlinks equal their checkouts. Nothing in the clone was modified, so no restoration was needed |

Public evidence: archive commit `8518f734` on `sync1115-review-evidence`. Git reports it **unsigned** (`%G?` = N), so no
signature verification is claimed. The docs-batch receipt shows six docs.yml jobs, each rc 0. I did not re-execute
the docs jobs or the leg simulations.

## Real limits

- R853-3-F1 is shown on synthetic logs built with the self-test's own helpers. Whether it occurred in any published
  trace is not known, because the raw traces are not published and the moves listing cannot show it.
- The regrade evidence is a receipt audit. I did not reconstruct the simulations or rebuild the images.
- Hosted CI was not inspected. No manager source bank was run at this head, and none is claimed.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- Known and not findings: #898 reaches the sync at composition. `record_classes.py`'s refusal of the 1x1/1if paced
  record is round 3's. The 8x8 legs' `STATED` cost lines (rc 1) are #914's.

## Pending manager duties

- Carry R853-3-F1 to the author. RES-1 goes to the residue checklist.
- Publish R853-2 RES-2's ruling.
- At the merge turn, validate the current-dev merge candidate (source base `659d7687`, live dev `6b66f66d`), including
  #898's composition, with builder and native banks. Own hosted and act acceptance.

R853-3 FINISHED
