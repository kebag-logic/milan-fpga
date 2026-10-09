[R552] POSITIVE - exact head 5024dcad23140597bc1ffa58d1613990b9f73279

# R552-3: internal independent delta review of processor PR #171 (Closes #168), 66d1b501..5024dcad

- Subject: Mister-M-alt/protocol-processor-control-plane-avb-milan PR #171, branch `pp168-acmp-fields`.
- Exact head `5024dcad23140597bc1ffa58d1613990b9f73279`, tree `f407bb708ac9fa9d0b725808b99106756e2e00dc`. Its parent is `66d1b501f4879402fe76485095aef7c6e07c32af`, so the round is one commit, with no rebase or amend.
- Source base `ed340b9b85258194247334b85e62cf9c23d4d051`; live dev for the merge candidate `7c1b52bee26b497080ee22b1c1986109f80a5ee7`.
- References: review start PR #171 comment 6086783370; round assignment issue #168 comment 6086658233; author REVIEW READY 6086754012. This round answers R552-2-F1 (PR #171 comment 6086650299).
- Role: internal reviewer in a cleared context, using its own detached clone. The repository has no AGENTS.md or CONTRIBUTING.md; `docs/README.md` supplies the author conventions.

## Verdict summary

**R552-2-F1 is RESOLVED at this head.** The round's commit changes one file, `docs/architecture/06_aecp_engine.md` (+17/-6; blob `a4df5ec` → `29b9aa1`), in the single hunk `@@ -1054,12 +1054,23 @@`. No `hdl/`, `tb/`, `scripts/`, `syn/`, Makefile or workflow byte changes. The `hdl tb scripts syn` tree listing hashes identically at 66d1b501 and 5024dcad, and `git diff --name-only 96d3b783..5024dcad -- hdl tb scripts syn .github Makefile` is empty.

I checked each statement in the rewritten 06 §7 (lines 1056-1072) against the RTL, and drove four of them in simulation through the real MAC/ADP/ACMP/AECP path with disposable probes.

| 06 §7 statement | RTL | Executed evidence |
|---|---|---|
| The pbsta/acmpsta compare pushes only on a committed byte change (1056-1058). | `protocol_processor_top.sv:3488-3491`: `lstn_gsi_changed_r <= (status_r != status_w)` on each listener record write. | Probe M1, the compare forced true on every write, gives 355 failures. Existing GI checks fail as well as the probe's own. |
| A discovered retry (A12, then the A5 delay expiry) keeps the status and pushes nothing (Milan v1.2 §5.5.3.5.30 step 2, §5.5.3.5.10, Table 5.22) (1058-1060). | `KL_pp_acmp_listener.sv:1270-1273`: A12 writes pbsta ACTIVE, already ACTIVE in PRB_W_RETRY, and keeps acmpsta on `LEV_TMR_RETRY`. `:1338-1345`: A5 keeps acmpsta on `LEV_TMR_DELAY`. | **P1** passes: "discovered retry (A12, A5): no push", run twice. Under M1 both checks FAIL, so the probe is not blind. The **P2T** trace shows no compare pulse for sink 0 between the MISSING-UNBIND writes and the later re-bind, a span that covers the retry and its delay expiry. |
| A retry with the talker gone (A17) changes the status to PASSIVE/0 and pushes (§5.5.3.5.30 step 1) (1060-1062). | `:1317-1321`: A17 writes PASSIVE/0. `:598-604`: the dagger resolution sends a TMR_RETRY with no discovered talker to A17. ACTIVE/x → PASSIVE/0 is always a byte change. | Existing GI `PASSIVE` pair (`gsi_internal.hpp:167`), passing in C0. |
| A repeated double probe timeout that leaves the status unchanged pushes nothing (1062-1063). | A14 writes 7 again over a retained 7 (`:1292-1294`), so the byte is unchanged. | **P1** passes: "repeated double timeout, ACTIVE/7 unchanged: no push" and the solicited readback stays ACTIVE/7. The check FAILS under M1. |
| `act_strt_chg_o` also pushes: the §5.5.3.5.6 short-circuit, and a re-bind to another talker from a bound state (1065-1067). | `:1455-1456`: the pulse requires bound before and after, plus a real f_started change. | Existing `REBIND-SW` check and the `rebind-started-trigger-removed` control in `gsi_mutants.py`. |
| From PRB_W_RESP with no retained status the byte stays ACTIVE/0, so `act_strt_chg_o` is the only push (1067-1069). | F05.3 row `05_acmp_engine.md:267`: PWR runs A1 A11 A9 A2 A3 A4 A5 in one X_WB. A4 PASSIVE is overwritten by A5 ACTIVE, and A5 clears acmpsta on a BIND event, giving ACTIVE/0 → ACTIVE/0. | Existing `REBIND-SW` (exactly one push, ACTIVE/0, SW). |
| With a retained status, both listener terms fire on the same record write and their OR sends one frame (1069-1072). | A5 on a BIND event clears a retained acmpsta, so the compare fires. f_started flips, so `act_strt_chg_o` fires. Both are registered from the X_WB cycle (`listener:1455`, `top:3488-3491`) and OR into `ntfy_stri_in_w` (`top:3563-3568`). | **P2** passes: from PRB_W_RESP at ACTIVE/7, a re-bind to another talker with STREAMING_WAIT gives exactly one push, ACTIVE/0 with SW, and started→stopped. **P2T** shows `cmp=1 strt=1` for sink 0 in the same cycle (cyc 1379939) with one `stri_in` pulse. **P2Xs** shows the compare term alone still gives exactly one frame. |

The re-bind sentence is now qualified as R552-2-F1 required. The clause citations match the LD2 corrections and the 05 legend (A5 `05:290`, A12 `05:297`, A17 `05:302`, the dagger note `05:305-309`). Repository-wide searches find no other prose that keeps the old premise; `tb/pp_top/README.md:2839-2842` (RETRY-RETAIN) agrees with the new text. The two in-code comments that keep the old premise were left unchanged by assignment and are recorded below as carried RESIDUE.

At the exact head, `make -j16 check` and `python3 scripts/gen_matrix.py --check` both return 0. All earlier findings stay resolved. No BLOCKER, MAJOR or MINOR is open. All five lenses are CLEAN.

## Findings

### BLOCKER / MAJOR / MINOR

None.

### RESIDUE (carried, unchanged at this head by assignment 6086658233; manager residue checklist)

**R552-3-RES1 - RESIDUE - RTL, Docs - top-level trigger comment still lists "retry" as a status-compare push**
- **Where:** `hdl/top/protocol_processor_top.sv:3551-3553`, which reads "the pbsta/acmpsta compare (bind, unbind, settle, teardown, double timeout, retry)".
- **Authority/evidence:** Milan v1.2 §5.5.3.5.30 step 2, §5.5.3.5.10 and Table 5.22. Probe P1 and the P2T trace show that a discovered retry raises no compare pulse. Only A17 (talker gone) does.
- **Impact:** comment text only. It changes no logic, test, figure or claim in an architecture document, and the authoritative 06 §7 is now correct.
- **Required outcome (exact fix):** replace "(bind, unbind, settle, teardown, double timeout, retry)" with "(a committed byte change only: bind, unbind, settle, teardown, a first double timeout, a retry with the talker gone; a discovered retry keeps the status and pushes nothing)".
- **Verification:** in the next change that touches the file, `git diff` shows a comment-only hunk, and `make check` returns 0.

**R552-3-RES2 - RESIDUE - RTL, Docs - listener comment calls `act_strt_chg_o` the ONLY notification of a re-bind from PRB_W_RESP**
- **Where:** `hdl/acmp/KL_pp_acmp_listener.sv:336-337`, which reads "from PRB_W_RESP the re-bind leaves pbsta/acmpsta at ACTIVE/0, so this pulse is the ONLY notification of that started/stopped change".
- **Authority/evidence:** same as RES1. Probe P2 and the P2T trace show that with a retained status both terms fire in one cycle. The listener's own comment at `:1449-1454` already states the both-terms case correctly.
- **Impact:** comment text only. The hardware sends one frame in both cases.
- **Required outcome (exact fix):** replace that sentence with "from PRB_W_RESP with no retained status the re-bind leaves pbsta/acmpsta at ACTIVE/0, so this pulse is then the ONLY notification of that started/stopped change; with a retained status A5 clears it, the pbsta compare fires on the same write, and the OR sends one frame".
- **Verification:** as for RES1.

### SUGGESTION (does not affect the verdict)

**R552-3-S1 - SUGGESTION - Docs - the ACTIVE/0 re-bind property is not unique to PRB_W_RESP.**
- **Where:** `docs/architecture/06_aecp_engine.md:1067-1069`.
- **Evidence:** the same F05.3 cell (`05:267`) applies from PRB_W_DELAY and PRB_W_RESP2, which also hold pbsta ACTIVE. With no retained status, those re-binds also leave the byte at ACTIVE/0. The sentence is accurate for the state it names, and the general rule at 1056-1058 covers the others, so this is not a defect.
- **Optional outcome:** write "from a probing-ACTIVE state (PRB_W_DELAY, PRB_W_RESP, PRB_W_RESP2)".

**R552-3-S2 - SUGGESTION - Tests - two new 06 §7 statements are graded only by this review's disposable probes.**
- **Where:** `tb/pp_top/gsi_internal.hpp:425-429`.
- **Evidence:** the suite does not separately check "a repeated double timeout with unchanged status pushes nothing" or "a retained-status re-bind sends exactly one frame". The general change-only premise is enforced: M1 fails 355 checks in the existing suite.
- **Optional outcome:** the P1 and P2 edits in `scripts/probe_gsi.py` are ready-made checks, at +18 checks and one extra retry period of simulated time. Add them, with the M1 control.

**Retained earlier suggestions.** Tests are unchanged, so these were not re-probed:
- R552-2-S1 (R552-1 S3): DISCONNECT_TX to an in-range but disabled source is ungraded.
- R552-2-S2 (R552-1 S2): the SRP VID slice is graded only below 0x100.
- R552-1 S4: the OOC timing observation is a limit, not a finding.

## Prior public review findings at this head

I read these only after my own pass, verdict draft and ledger draft were complete.

| Prior item | Status at 5024dcad | Evidence |
|---|---|---|
| R552-2-F1 (MINOR, Docs): 06 §7 still assumed the removed A5/A12 clear | **RESOLVED** | Each required outcome is present at 06:1056-1072 and verified in the table above. Both sub-cases R552-2 left un-simulated are now executed (P1, P2, P2T). The two in-code comments are carried as RES1 and RES2 under the assignment. |
| R552-1 F1 to F4, R553-1 F1 and F2 (all MINOR, resolved at 66d1b501 by R552-2 and R553-2) | **Still RESOLVED** | The only hunk is 06:1054-1076. The resolution sites (05 scope, F05.3 legend and F05.11; 01 Δ4; 00 GAP-02 and REQ-ACMP-007; operator.md; figure 24; F07.6 and 07 overlay; 06:335, :421-433; 02 §4.4; integrator.md) are byte-identical to 66d1b501. |
| R552-1 S1 | Resolved as documented (unchanged) | 05:305-309 |
| R552-2-S1, R552-2-S2, R552-1 S4 | Retained, as above | No test or source change |
| RESIDUE in any earlier round | None existed | — |

## Executed evidence (this review, exact head)

| Run | rc | Result | Receipt |
|---|---|---|---|
| `make -j16 check` | 0 | lint (41 mermaid + 18 WaveDrom), wavedrom-check (18), links (1186), matrix (115 REQ, 17 GAP), modmatrix (94 rows, 0 untested), params (29), ids and its selftest (30 cases), figures and its selftest (17 cases), stale | `receipts/make_check.{log,rc}` |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested | `receipts/gen_matrix_check.{log,rc}` |
| C0: unmodified head, pp_top `--gsi-internal-only` | 0 | 6183 checks, 0 failures | `receipts/probes/C0.*` |
| P1: test-only retry and repeated-timeout probe | 0 | 6201 checks, 0 failures (+18) | `receipts/probes/P1.*` |
| P1M1: P1 plus M1 (compare fires on every write) | 1 | 355 failures, including all three probe "no push" checks | `receipts/probes/P1M1.*` |
| P2: retained-status re-bind from PRB_W_RESP | 0 | 193 checks, 0 failures (the phase stops after the probe) | `receipts/probes/P2.*` |
| P2Xs: P2 with the started/stopped term removed | 0 | The compare alone still gives exactly one frame | `receipts/probes/P2Xs.*` |
| P2Xc and P2Xcs: P2 with the compare term removed, alone or with the strt term | 1 / 1 | **Not isolating.** Both fail at the earlier `BIND-ACTIVE` step, because the compare is the only trigger the phase waits on there. They are kept only as disclosure. | `receipts/probes/P2Xc*.*` |
| P2T: P2 plus non-functional `$display` instrumentation | 0 | 193/0. Both listener terms fire for sink 0 in the same cycle with one `stri_in` pulse, and no compare pulse appears across the discovered retry. | `receipts/probes/P2T.*` |
| Clone integrity after all probes | 0 | Head and tree exact, worktree clean, index equals HEAD (write-tree `f407bb70`). All 582 tracked files match by bytes and mode, with 0 mismatches. 0 gitlinks exist in this tree, so none are required. | `receipts/integrity-after-probes.log` |

How the probes were run:
- Every probe ran in a separate `git archive` extraction under the never-published scratch directory. The clone was only read.
- Builds used the pinned simulator 5.050, the same version as the CI pin (`receipts/toolchain-identity.txt`). Build parallelism was 3 to 8 per build, with at most four builds at once.
- Host home-directory prefixes in published logs are replaced by `<PINNED_ROOT>`. The wrapper sha256 in the toolchain receipt was taken over the unredacted file.

## Lens evidence

- **Conformance - CLEAN.**
  - The rewritten triggers match Milan v1.2 Table 5.22: GET_STREAM_INFO is notified on a change of a visible field only.
  - The retention clauses are cited as the LD2 correction and the 05 legend cite them: §5.5.3.5.30 step 2 and §5.5.3.5.10 for retention, step 1 for A17.
  - No conformance or compliance-matrix claim changed.
- **RTL - CLEAN.**
  - No `hdl/` byte changed.
  - Every RTL fact the new text asserts was re-traced: the compare at top:3488-3491; A12, A14, A17 and A5 at listener:1270-1345; the dagger at :598-604; the X_WB `act_strt_chg_o` at :1455; the OR at top:3563-3568.
  - The two old-premise comments are carried as RES1 and RES2.
- **Robustness - CLEAN.**
  - Change-only notification holds across the retry loop, including a repeated double timeout (P1).
  - The dual-trigger re-bind coalesces into one frame rather than a duplicate (P2, P2T, P2Xs).
  - The final GI "no duplicate notifications" check passes in C0 and P1.
- **Tests - CLEAN.**
  - No test changed. The unmodified GI phase passes at head.
  - The change-only premise is enforced by existing checks (M1 gives 355 failures).
  - The new statements' sub-cases are executed by non-blind probes. Adding them to the suite is optional (S2).
- **Docs - CLEAN.**
  - R552-2-F1 is resolved. The new text agrees with 05 F05.3, the legend, F05.4's note and `tb/pp_top/README.md` RETRY-RETAIN.
  - `docs/README.md` rules hold: no timing or parameter value is copied, and citations are plain text.
  - Gates pass. The remaining items are wording residue (RES1, RES2) and a suggestion (S1).

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #168 frozen table and rulings (6050554601, 6086658233); Milan v1.2 §5.5.3.5.30 steps 1-2, §5.5.3.5.10, Table 5.22 as cited; 06 §7:1056-1072; 05 F05.3:267, legend :290/:297/:302, note :305-309 | R552-3 | 5024dcad23140597bc1ffa58d1613990b9f73279 |
| RTL | CLEAN | Empty `hdl/` diff for 66d1b501..5024dcad and 96d3b783..5024dcad; `protocol_processor_top.sv:3470-3569` (status compare, GSI answer, `stri_events`); `KL_pp_acmp_listener.sv` classify :540-578, dagger :598-604, A12/A14/A17/A5 :1270-1345, X_WB :1432-1462, comments :215-227 and :323-342 | R552-3 | 5024dcad23140597bc1ffa58d1613990b9f73279 |
| Robustness | CLEAN | Retry loop with repeated double timeout (P1); dual-term re-bind coalescing (P2, P2T, P2Xs); duplicate-notification guard (C0, P1) | R552-3 | 5024dcad23140597bc1ffa58d1613990b9f73279 |
| Tests | CLEAN | `tb/pp_top/gsi_internal.hpp` (whole phase); `gsi_mutants.py` and `acmp_mutants.py` LD2 controls; C0, P1, P1M1, P2, P2Xs, P2Xc, P2Xcs, P2T; `make -j16 check`; `gen_matrix.py --check` | R552-3 | 5024dcad23140597bc1ffa58d1613990b9f73279 |
| Docs | CLEAN (RES1, RES2 carried as RESIDUE; S1 suggestion) | `git diff 66d1b501..5024dcad` (one hunk); 06 §7 in context :1040-1085; 05 F05.3, legend, F05.4 note; `tb/pp_top/README.md:2839-2842`; repository-wide searches for the old premise; `docs/README.md` rules; PR body Round 4 section | R552-3 | 5024dcad23140597bc1ffa58d1613990b9f73279 |

## Hosted CI at the exact head (observed, not accepted; the manager owns hosted acceptance)

Observed 2026-10-09T18:30:04Z (`receipts/hosted-ci-final.txt`, `receipts/hosted-ci-steps.txt`). Both runs report head_sha 5024dcad.

| Run | docs-gates | portability | suites |
|---|---|---|---|
| pull_request 37972718231 | success; the `make check` step executed | success; "Elaborate every top off-vendor" executed | **in progress**: lint and suites running; the five campaigns, matrix and nvm_port steps pending |
| push 37972712542 | success; `make check` executed | success; elaborate executed | **in progress**, same state |

Neither suites job is counted as passed. "Build Verilator v5.050" is skipped in both because the cache hit; that is not a skipped check.

## Real limits

- **Standards texts.** The Milan v1.2 and IEEE 1722.1-2021 texts were not available. Clause judgements rest on:
  - the issue's frozen table and the manager's rulings;
  - the clause citations accepted in earlier rounds;
  - the RTL and its clause tests.
- **Re-runs.** I re-ran no full suite bank, campaign, lint, off-vendor flow or OOC area. Sources are byte-identical to 96d3b783, whose execution is in the public evidence tree `kebag-logic/milan-fpga@1570e003` (`review-evidence/pp168-r1`, the round-2 packet: 33 suites, 51 ACMP controls, +29 LUT / +14 FF). That tree holds no round-3 or round-4 receipts. The author's round-4 gate results are stated in REVIEW READY 6086754012, and my own exact-head runs cover the same two commands.
- **Probe coverage.** The probes cover the default build only. They are disposable and were not added to the suite. P2Xc and P2Xcs could not isolate the compare term, as disclosed above.
- **Manager source bank.** None ran at this exact head, and none is claimed or inferred.
- **Hardware.** Physical calibration is NOT RUN. Field skips, simulation and documentation gates are not hardware proof.
- **Memory.** Memory was not metered per unit. The builds were capped at four concurrent, 3 to 8 jobs each. No heavy synthesis run was started.

## Pending manager duties

- Re-run the donor bank (9) and the parent consumer bank (17) at this head.
- Build the current-dev merge candidate (builder and native banks; source base ed340b9b, live dev 7c1b52be) at the merge turn and link its receipts on the PR.
- Hosted acceptance: both suites jobs were still in progress at observation.
- Residue checklist: R552-3-RES1 and R552-3-RES2, with the exact fixes above, for the next change that touches those files.
- Carry the optional suggestions S1 and S2 and the retained R552-2-S1, R552-2-S2 and R552-1 S4.
- Carry the parent-side handling of a stream_vlan_id that is not a valid VID (out of scope by ruling 6050554601).

## Receipts

Paths are relative to this packet; every published file is listed in `MANIFEST.sha256`.

- `scripts/probe_gsi.py`: archive extraction, variant edits, build and run. Usage is in its docstring.
- `scripts/integrity.sh`: clone byte, mode, index and gitlink check.
- `receipts/delta_66d1b501_5024dcad.diff`, `receipts/line-anchors.txt`.
- `receipts/make_check.*`, `receipts/gen_matrix_check.*`.
- `receipts/probes/*.log`, `receipts/probes/*.rc`, `receipts/probes/summary.tsv`.
- `receipts/integrity-after-probes.log`, `receipts/toolchain-identity.txt`.
- `receipts/gh_pr_checks.txt`, `receipts/gh_check_runs_5024dcad.tsv` (first observation), `receipts/hosted-ci-final.txt`, `receipts/hosted-ci-steps.txt`.

R552-3 FINISHED
