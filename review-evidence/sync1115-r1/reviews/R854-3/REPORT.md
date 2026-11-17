[R854] POSITIVE - exact head 9aa55d3b382750353709c3ba9ff6f6416938e83b

R854-3, external independent review of issue #665 / PR #934, round 6 only.
Tree: `fc52e64fd482c3185620b6d00048c2b2608f7d06`.
Reviewed delta: `e2be92b0e0f9a8f0529dea252f23ed44a21e050a..9aa55d3b382750353709c3ba9ff6f6416938e83b`, commits `1238a3ee` and `9aa55d3b`.

All five lenses are CLEAN for this delta. R854-2-F1 is resolved at its cause. No new BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION is reported. This is source-review acceptance, not merge authorization or completion of the composition gates.

Reconstruction followed AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue and public decisions, requirements/interfaces, the base-to-head change inventory and history, then the nine-file round-6 diff and public executable receipts. Earlier unchanged code retains its prior review coverage. The independent verdict and five-lens ledger were written before reading prior review reports; prior finding sections were then reconciled. No private author material or other checkout was read.

Public authorities: [issue #665](https://github.com/kebag-logic/milan-fpga/issues/665), [Q1's participant-opportunity decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6930885185), [freeze/composition rule](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6939574513), [round-6 REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6945152485), and [review start](https://github.com/kebag-logic/milan-fpga/pull/934#issuecomment-6945266206). Local authorities examined include REQUIREMENTS.md:60, FR_NFR.md section 3.4.1, the mailbox event/commit contract, and SPLIT_CONTROL_MEMORY.md's THE TRANSMIT contract. The participant-opportunity interpretation of IEEE 802.1Q-2018 10.7.4.1 is unchanged; the 49 ms conformance allowance remains derived from the 240 ms maximum, 190 ms armed join time and 1 ms egress allowance. The measured service rows retain 20 ms.

Prior findings and closure evidence:

| ID and original severity/lenses | Disposition at this head |
|---|---|
| R854-2-F1, MAJOR, Conformance / Robustness / Tests | CLOSED. `mrpdu_grade.py:225` passes the recorded owner through all owned outcomes. `:240` sets the missing-build horizon from that owner's opportunity. `:247` selects only commits carrying that owner's MRPDU. `:157` and `:168` start the service row from the owner. `join_grade.py:66` and `run.py:181` report the owner and original opportunity. The unchanged prior probe returns 0: four previously hidden missing builds become absent, four foreign-frame late builds become late, all naming their actual owner at 1300.001 ms. None gains a foreign service row. Four genuinely short logs remain unresolved; absence and empty-late controls pass. |
| R854-001, MAJOR, Conformance / Robustness / Tests / Docs | CLOSED, retained and checked at its dependency. Recorded ownership still drives LeaveAll matching and timing; the owned overlap fails on the skipped owner at its original opportunity, while clean and reordered output pass. The 60-control ownership probe includes the 1180 ms opportunity and 191 ms skipped-LeaveAll row. The current docs state the actual ownership proof. |
| R853-1 F1, MINOR, Conformance / Robustness / Tests / Docs | CLOSED, retained. The second expiry inside another owner's join interval cannot replace that owner. Standing overlap/record checks pass and the old output-attribution mutant is caught in the focused run. |
| R853-1 F2, MINOR, Conformance / Robustness / Tests | CLOSED, retained. `anchor()` still uses the recorded owner's posted-TICK opportunity; an unrelated join callback cannot restart an empty build's clock. The alone/callback controls retain the 59.979 ms late result, and the old callback-anchor mutant is caught. |

The original findings are [R854-2-F1](https://github.com/kebag-logic/milan-fpga/pull/934#issuecomment-6942847358), [R854-001](https://github.com/kebag-logic/milan-fpga/pull/934#issuecomment-6932841237), and [R853-1 F1/F2](https://github.com/kebag-logic/milan-fpga/pull/934#issuecomment-6938623769). Their demonstrated causes are fixed, not deferred to another issue.

[R854] PASS Conformance - `tb/verilator/ctrl_service_budget/mrpdu_grade.py:212`, `:225`, `:240`, `:247`, `:168`; `docs/reference/FR_NFR.md:388` - every owned expiry's deadline, answering frames and row start use its recorded participant. Only the owner's running join timer supplies a required wait. The old latest-participant and first-foreign-frame associations are removed without changing the bound.

[R854] PASS RTL - `delta.diff`, commit `1238a3ee` and `9aa55d3b` path inventories; `mrpdu_grade.py:252` - the delta changes grading, self-tests and two documents only. No RTL, firmware, observer, build input, configuration or gitlink changes. The extracted build-window search preserves the previous pass grouping and owed-frame retries. There is no changed clock/reset, CDC, wire layout or hardware interface to requalify in this delta.

[R854] PASS Robustness - `selftest_leaveall.py:244`, `:263`, `:302`; `selftest_polls.py:321`; `probe-missing-build.log`; `probe-ownership.log` - both applications on both interfaces exercise missing builds, foreign-only output, empty output, own output, mixed-participant commits, running owner/peer timers, short logs, unresolved ownership and overlapping LeaveAlls. Exact-bound and over-bound ownership controls pass. Legitimate empty builds and owed-frame retries remain covered. A mixed commit's row is 10.0 ms from its owner's opportunity, not 140 ms from its peer's.

[R854] PASS Tests - `selftest_mutants.py:881`; `selftest_notice.py:54`; `focused-checks.log`; `receipt-audit.log` - 882 baseline checks pass locally; all 23 transmit/LeaveAll mutants are caught by named assertions, without counting exceptions as catches. The notice fixture now carries the declared owner's MSRP EtherType, preserving its timing assertion under the owner filter. The complete 265-mutant result is published source evidence, separately audited below.

The four added mutants each fail the appropriate named control in `focused-checks.log`:

| Mutated association | Control that catches it |
|---|---|
| Latest participant's no-build horizon | “a run-out with no build after it is absent past THE TRANSMIT's bound after its owner's first transmit opportunity…” |
| First frame's participant supplies both response and opportunity | “a build that sends only another participant's MRPDU answers nothing for a run-out…” |
| Foreign frame credited while timing from the owner | The same foreign-only-output control, including empty/no-row behavior |
| Earliest opportunity among a commit's participants | “a timer's row starts at its owner's first transmit opportunity…” |

[R854] PASS Docs - `tb/verilator/ctrl_service_budget/README.md:146`, `:171`, `:233`, `:1382`; `docs/reference/FR_NFR.md:388`; PR #934's round-6 behavior table - the text matches the three owner-based outcomes and row boundaries. All four new mutant rows name the controls that actually fail. The added source comments describe behavior/reason and contain no prohibited bench-lane label, review identity, review-round label or issue-comment ID.

Public evidence audit:

The [archive at 8518f734](https://github.com/kebag-logic/milan-fpga/tree/8518f7346a60ad8ef1e6e690d58ee0d785b5c7bf/review-evidence/sync1115-r1) supplies the source-head receipts. `audit_receipts.py` verifies 472 published SHA-256 entries covering author-r6 and the relevant author-r4/r5 budget evidence.

- Every one of the 13 round-6 tables is byte-identical to round 5b's table, and every exit code is unchanged. The 1x1 valid-destinations leg is rc 0; the twelve 8x8/1if legs remain rc 1. These are not thirteen passing whole legs.
- The 26 result groups preserve every probe row, join count/extrema/violations and LeaveAll outcome. There are 1,871 owned expiries: 1,029 released and 842 empty, none late, absent, unresolved or unowned.
- All 73 published movements are enumerated in `receipt-audit.log`: 46 join and 27 periodic, exclusively released-to-empty. Each names its owner and a different participant that previously answered it; each records no owner frame in the associated builds. The movement counts agree with the old/new result totals.
- The eleven phases retain 44 sent LeaveAlls. Maxima remain leaveall 1.64360 ms, periodic 2.96879 ms and join 1.86217 ms.
- The exact-head self-test receipt reports 882 checks and 265 caught mutants, zero failures; all 265 named caught records are present. Local execution independently confirms the baseline and the 23 affected mutants.
- The exact-head docs receipts report 63 executed steps, 34 NOT RUN with reasons and zero bad, with verifier rc 0. Skips are not execution evidence.
- The seed receipt records the head's harness on the ten experiment clones; their regrade headers retain their earlier source head and experiment state. The product and valid-destinations regrades record clean `9aa55d3b`. The regrade script requests input attestation through `--reuse-build --regrade`. These are published regrades, not fresh simulations performed by this review.

Reviewer-owned completion ledger:

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | mrpdu_grade.py:157,212,225,240,247; FR_NFR.md:388; probe-attribution-audit.txt | R854-3 | 9aa55d3b382750353709c3ba9ff6f6416938e83b |
| RTL | CLEAN | delta.diff; unchanged build-window behavior at mrpdu_grade.py:252; source-integrity.log | R854-3 | 9aa55d3b382750353709c3ba9ff6f6416938e83b |
| Robustness | CLEAN | selftest_leaveall.py:244,302; selftest_polls.py:321; probe-missing-build.log; probe-ownership.log | R854-3 | 9aa55d3b382750353709c3ba9ff6f6416938e83b |
| Tests | CLEAN | selftest_mutants.py:881; focused-checks.log; receipt-audit.log | R854-3 | 9aa55d3b382750353709c3ba9ff6f6416938e83b |
| Docs | CLEAN | README.md:146,171,233,1382; FR_NFR.md:388; PR round-6 table; archive-hashes.txt | R854-3 | 9aa55d3b382750353709c3ba9ff6f6416938e83b |

Paths abbreviated in this ledger are under `tb/verilator/ctrl_service_budget/`, except FR_NFR.md under `docs/reference/` and packet receipts. This ledger renews coverage for the round-6 delta and its affected dependencies; it does not claim a fresh review of earlier untouched sync work.

Reproduction from this packet, with CHECKOUT naming the exact-head clone:

```sh
mkdir -p scratch
TMPDIR="$PWD/scratch" python3 -B focused_checks.py "$CHECKOUT"
python3 -B probe_missing_build.py "$CHECKOUT"
python3 -B probe_ownership.py "$CHECKOUT"
python3 -B audit_receipts.py "$CHECKOUT"
python3 -B verify_source.py "$CHECKOUT"
```

All five commands completed with rc 0; their raw receipts and return-code files are listed in MANIFEST.sha256. The two prior probe scripts are unchanged and match their prior published manifest hashes. The focused raw log includes deliberately exercised “CONTROL ... ESCAPED” branches from negative controls; the baseline and mutation assertions report zero failures.

Real limits and pending manager duties:

- Archive authenticity was checked against the requested Git object and published content hashes. That commit contains no cryptographic signature and no signature artifact was supplied; no signature verification is claimed. The published packet omits large raw simulation logs and retains digests/extracts. The 73 movement audit checks the published per-expiry account and result consistency, not a new replay of omitted traces.
- No manager source bank ran at this exact head, and none is inferred. Source-head execution evidence here is the author's published receipts plus the focused reviewer runs. Earlier full banks retain their recorded heads. Hosted/act acceptance remains the manager's duty; this review did not inspect or run those jobs.
- The final live-base composition, its builder/native banks, measurement acceptance, independent composition review and containment remain pending under the owner rule. Source base `659d7687` and live dev `6b66f66d89cf25d2717687bcc2c3bf617685a99a` are distinct from this reviewed head and from the eventual composed candidate.
- #898 is merged and reaches this sync at composition. The single 1x1/1if paced-record refusal is earlier evidence; #914 owns the unchanged 8x8 cost statements. These known composition obligations are not new findings in this delta.
- Physical calibration was NOT RUN. Field skips and simulation receipts supply no hardware proof. No full banks, hardware runs, source fixes, commits, pushes, GitHub writes or merges were performed.
- `source-integrity.log` verifies all 1,900 root tracked blobs and their modes/index, plus pinned bytes/modes/index for protocol-processor, gptp-processor, verilog-axis, tsn-c-stack and lwSRP. All match the exact head; the checkout is clean. The unused external submodule remains uninitialized.

R854-3 FINISHED
