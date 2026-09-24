[R266] NEGATIVE - exact head 604297bb41d6c8005d07539289b10bfa99273cdd

Round R266-3, internal independent review of issue #532 / PR #533, correction round 2. Exact head `604297bb41d6c8005d07539289b10bfa99273cdd`, tree `1a8cfc31dedc8eef7929a5a7529568503fa580d4`. Source base `ede8d48e`, merged dev `759da623`; live dev at review time `26d855a9`.

Three MINOR findings leave `Tests` and `Docs` unclean. All three are the same class the round was assigned to close: a protective check in `scripts/act_slot_proof.sh` that the offline self-test does not reliably fail without. Everything else in the round holds at this head:

- the memory-cap attribution text is exact;
- the `DOCKER-USER` note is correct;
- the runner changes are a pure tightening, with arms that kill their mutants;
- 45 of my 56 proof mutants are killed deterministically.

This section was written from my own pass, before any prior review was read. The disposition of prior findings is added at the end.

## Scope reconstructed

- Governance: AGENTS.md sections 3-8; CONTRIBUTING.md 2.1 and 3; docs/README.md; REQUIREMENTS.md REQ-VER-04, the zero-finding scope gate.
- Issue #532: body and acceptance 1-6. Also the A203 DECISION and its round-1 amendments, and the A10 assignment for this round (issuecomment-5803011314): "self-test cases that fail when each protective check of the live proof is removed" and "memory-cap attribution docs that state exactly what is detected".
- Interface authority: `docs/testing/CI_WORKFLOWS.md` "Act-first local replication" (bootstrap rule) and "Parallel replay slots".
- Diff: `759da623..604297bb` is four files. `f5497170..604297bb` is five commits over three files, 211+/64-. Verified with `git log`/`git diff` and the file digests in the author's receipt, which match the head:
  - `act_ci.py` `e8bf06d2...`
  - `act_slot_proof.sh` `3cffa803...`
  - `CI_WORKFLOWS.md` `44588ca3...`
  - `check_baremetal_only.py` `533c1205...`

## Findings

### F1 - MINOR - Tests, Docs - slot B's isolation control has no failing case

- **Where:**
  - `scripts/act_slot_proof.sh:284-298` (isolation) and `:310-312` (per-slot loop);
  - the stand-in `answers()` at `:467-479`;
  - cases `:596-601`;
  - `docs/testing/CI_WORKFLOWS.md:1955-1984`.
- **Authority:**
  - the round's frozen assignment (issuecomment-5803011314);
  - proof check 4, "the isolation control in each slot" (`act_slot_proof.sh:17-22`, `CI_WORKFLOWS.md:1924-1932`);
  - AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect".
- **Evidence:**
  - Every stand-in isolation fault applies to both slots alike (`slot-reaches-*`, `slot-misses-internet`, `target-dead`, `host-misses-*`). `answers(specs, inside)` never looks at which slot's namespace was entered.
  - Mutant G07 (the slot probe always enters `milan-act-slot-$slot_a`) passes all 38 cases as uid 1000 and as uid 0. So does G08 (`isolation "$slot_a"` recorded for slot B). Receipts: `receipts/proof-mutants-head-uid1000.txt` and `-uid0.txt`.
  - In both mutants the SUMMARY still holds ten PASS lines, so the backstop does not catch them either.
- **Impact:**
  - The acceptance-1/2 instrument can stop probing slot B's own namespace with no offline signal. A defect confined to slot B's firewall would then pass the live proof.
  - `CI_WORKFLOWS.md:1979` ("Two guards have no case") and the PR's DoD item "fails when any of its protective checks is removed" overstate the coverage.
- **Required outcome:** removing or redirecting the isolation probe of either slot fails the self-test, and the doc's list of cases and uncovered guards is accurate.
- **Verification:**
  - G07 and G08 are KILLED as uid 1000 and as uid 0, with the no-op control surviving.
  - Feasibility: a scratch-only copy adds one stand-in fault in which only slot 2 reaches the container. That one case kills both mutants in both modes (`receipts/feasibility-mutants-*.txt`, `scripts/feasibility_cases.py`). It shows such a case exists; it is not a proposed patch.

### F2 - MINOR - Tests, Docs - a failed network query after target removal has no case

- **Where:**
  - `scripts/act_slot_proof.sh:275-276` (`|| networks=unknown`);
  - cases `:602-604`;
  - `docs/testing/CI_WORKFLOWS.md:1968-1973`.
- **Evidence:**
  - Mutant F06 (`|| networks=`, so an unanswerable `docker network ls` reads as absent) passes all 38 cases in both modes.
  - The case "the isolation target cannot be queried after removal" fails only `docker ps`. No stand-in fault fails `docker network ls`.
  - The container-side twin, F05 (`|| containers=`), is killed.
  - The doc says the broken cases include "a container or network that survives its removal or cannot be queried after it".
- **Impact:** the guard that stops an unanswerable network query counting as proof of absence can be removed silently, and the doc claims a case that does not exist.
- **Required outcome:** a case that fails when a failed network query after removal reads as absent, and doc text that matches the cases.
- **Verification:** F06 KILLED in both modes, with the control surviving. The feasibility copy's case "the isolation network cannot be queried after removal" kills it in both modes.

### F3 - MINOR - Tests - three of the four overlap guards are killed only by a race

- **Where:**
  - `scripts/act_slot_proof.sh:307-308`: `await_holder parallel-a`, `await_holder parallel-b`, `! ended parallel-a`, `! ended parallel-b`;
  - cases `:592-594`;
  - stand-in runner `:407-432`.
- **Evidence:**
  - Only `! ended parallel-a` has a deterministic case: `refused-while-held` makes run A refuse. Mutant D07 is killed in every run.
  - `slot-unannounced` silences both slots, so dropping either `await_holder` alone still records `FAIL overlap`.
  - The other kills come only from `serialize`. Its summary depends on which stand-in run takes the queue lock first:
    - dropping `await_holder parallel-a` (D05) is caught only when run B wins;
    - dropping `await_holder parallel-b` (D06) or `! ended parallel-b` (D08) is caught only when run A wins.
  - Measured in six repeats as uid 1000: D05 killed 3/6, D06 3/6, D08 3/6. The first batch gave D05 killed in both modes, and D06 and D08 surviving as uid 1000 but killed as uid 0. The control survived 8/8. Receipts: `receipts/proof-mutants-overlap-repeats-uid1000.txt` and `proof-mutants-head-*.txt`.
- **Impact:** removing one of these guards passes the self-test about half the time. For D08, that loses the B side of check 3, "both holding their slots at one instant, before either has printed a verdict". The live code at the head is correct.
- **Required outcome:** removing any one of the four overlap conditions fails the self-test on every run.
- **Verification:**
  - D05, D06 and D08 are KILLED on repeated runs in both modes.
  - The feasibility copy has three one-sided cases: only slot A unannounced, only slot B unannounced, and run B refused before slot A is taken. They kill D05, D06 and D08 respectively, in both modes.

### S1 - SUGGESTION - Docs, Tests - the stated reason the non-root writability guard has no case is inaccurate

- **Where:** `docs/testing/CI_WORKFLOWS.md:1982-1984`, and guard `act_slot_proof.sh:128`.
- **Evidence:** consider an unprivileged user namespace that maps the invoker's own uid and keeps its capabilities as ambient ones. There, `[ "$(id -u)" -ne 0 ] && [ -w FILE ]` is true for a mode-0555 file with no write bit (`receipts/writable-no-bit-probe.txt`, `scripts/writable_no_bit_probe.sh`). So "an unprivileged scratch directory cannot produce such a file" is not the reason.
- **Optional:** where unprivileged user namespaces exist, stage it (reporting NOT RUN elsewhere), or restate the reason. Doing neither does not affect coverage.

## Proof mutation campaign (own set, 56 mutants plus a no-op control)

`scripts/proof_mutants.py` defines one exact edit per check. Every edit applies exactly once to the head file (sha256 `3cffa803...`). `scripts/run_proof_mutants.sh` runs the mutants one at a time inside `scripts/sandbox.sh`, which gives new user and network namespaces (only `lo`) as uid 1000 and as namespace uid 0.

Baseline at the head: `--selftest` PASS, 38 cases, in both modes, about 26 s each (`receipts/proof-selftest-head-*.txt`).

| Outcome | Mutants |
|---|---|
| KILLED every run, both modes (45) | A01, A04-A06, B01, B02, B04, B05, C01-C08, D01-D04, D07, E01-E03, F01-F05, F07, G01-G06, H01-H08, I01 |
| KILLED only by a race (F3) | D05, D06, D08 |
| SURVIVED, protective (F1, F2) | G07, G08, F06 |
| SURVIVED, documented as having no case | B03 (non-root writability; see S1), I02 (ten-PASS backstop) |
| SURVIVED, judged not protective | A02 and A03: no numeric check on the serial slot or slot B (A03 is below). A02 runs a non-numeric serial slot as slot 0, the default, so no false `PROVED` is possible. E04: the interrupt gate accepts any slot's teardown line. The command line fixes `--slot "$slot_a"`, so the number only restates the argument. |
| Control X00 | SURVIVED in every run (10 of 10) |

A03 in detail: a non-numeric slot B runs without `--slot`, and its isolation probe cannot enter `milan-act-slot-<word>`, so the proof fails.

The round's named targets are killed by this head's cases:

- a slot that cannot reach the probe name (G03);
- a host that cannot reach the container (G05) or the published port (G06);
- a slot-0 rival refused for another reason (H07);
- runs refused after passing or failing (C02, C03);
- digest, write bit and log directory (B01, B02, B04);
- slot pairs (A04-A06);
- the interrupt gate without its PASS line (E02).

## Memory-cap attribution and the DOCKER-USER note

- **Runner.** `act_ci.py:4455-4495` refuses only a nonzero `oom` in the slice's own `memory.events.local`. Events missing `oom` or `max` are also refused, as are unreadable or malformed events. It prints `memory peak X of its 24G cap; the cap was hit N time(s), with no OOM at it`.
  - The check runs only after a body that returns. A raising body keeps its error (`:4498-4537`).
  - The comment (`:149-160`) and docstrings claim nothing beyond the peak and the count.
  - `max` is present in every cgroup-v2 `memory.events.local`, so the new missing-count refusal is a tightening and cannot fire on a well-formed kernel file.
  - No consumer parses the old "which never ran out" line (`git grep`).
  - The proof's verdict extraction (`act_slot_proof.sh:171`, `:218`) cannot match `act-ci: slot N: ...`.
- **Doc** (`CI_WORKFLOWS.md:1826-1841`). It says the OOM at the cap is all that is detected. Reclaim at the cap and an allocation that fails without trying the OOM killer keep their verdict. The peak and `max` count are "the only sign" and not proof of cause, and it says to replay a slot `FAILED` with a nonzero count in slot 0. This matches the cgroup-v2 definitions of `max` (usage about to exceed the limit, before reclaim) and `oom` (not raised when the OOM killer is not an option).
- **Arms** (`act_ci.py:12188-12257`):
  - the honest line with its count;
  - events without `max` refused and torn down;
  - a `FAILED` run at the cap with no OOM keeps `FAILED`.
- **Evidence this round could use.** Executing `act_ci.py` was out of this round's bounds. What I used:
  - the hosted `docs-check` job on this head: 424 `ok`, `selftest: PASS`, the three new arms present (`receipts/hosted-docs-check-act-ci-selftest-excerpt.txt`). Its merge build leaves all four touched files at the head's blobs.
  - the author's published receipts: 56/56 slot mutants KILLED as uid 1000 and uid 0, control surviving;
  - my static check that all 57 published slot-mutant edits apply exactly once to the head file (`receipts/slot-mutant-applicability-604297bb.txt`).
  - By construction each of the three new mutants is killed by the arm aimed at it, and "a slice at its cap refused" only by the new `FAILED` arm.
- **DOCKER-USER** (`CI_WORKFLOWS.md:1769-1773`): correct. Slot traffic leaves as host output from the uplink's sockets, so a forward-path `DOCKER-USER` policy never sees it. The note's "For the same reason" follows three DNS sentences, which blurs its antecedent; this is wording only.

## Gates and hosted evidence at the head

- **Focused gates**, all rc 0, in a network-less sandbox (`receipts/focused-gates-summary.txt`, logs in `receipts/gates/`):
  - `check_baremetal_only.py --check` (0 findings, 847 files) and `--selftest` (441 arms);
  - `docs_check.py` (0 findings);
  - `check_em_dash.py --base 759da623` (0 over 338 added lines) and `--base ede8d48e` (0 over 635);
  - `check_py_idiom.py`, `check_sh_idiom.py`;
  - `gen_toc.py --check` and `--verify-anchors`;
  - `check_doc_paths.py`, `check_doc_style.py`, `ci_events.py --check`, `check_feature_status.py`;
  - `git diff --check` from `759da623` and `f5497170`;
  - `bash -n` on the proof script.
- **Hosted, exact head** (`receipts/hosted-check-runs-604297bb.tsv`):
  - All seven required contexts completed success: `rtl-fast`, `docs-check`, `wire-accountability`, `docs-check-no-git`, `elaborate`, `verilator-suites`, `yosys-portability`.
  - The shards behind them executed, with nonzero durations: Verilator 0-4/5 and Yosys 0-3/4.
  - The only skipped context is "Physical gPTP (nightly and manual)", which is not hardware evidence.
  - The manager owns hosted and act acceptance.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #532 acceptance 1-6 against the head. `759da623..604297bb` changes no workflow file (acceptance 6). The one new refusal (missing `max`) is a tightening. The live logic of `act_slot_proof.sh:139-364` against checks 1-6 in `CI_WORKFLOWS.md:1905-1950` and the DECISION as amended. Acceptance 1 remains NOT MET pending the live proof; that is a pending duty, not a finding. | R266-3 | 604297bb41d6c8005d07539289b10bfa99273cdd |
| RTL | CLEAN | `act_ci.py:149-160` and `:4234-4537`: acquisition order, cap set before any unit starts, the memory read before teardown, teardown under blocked signals, error paths. Call sites `:5260-5305` and `:13380-13455`. The runner-to-proof output contract: runner lines at `:4523`, `:5205`, `:5241-5243`, `:13441-13452`, `:14234`; proof parsing at `act_slot_proof.sh:171`, `:218`, `:224`, `:239-240`. | R266-3 | 604297bb41d6c8005d07539289b10bfa99273cdd |
| Robustness | CLEAN | Malformed, missing and unreadable memory events and peak, and a raising body (`act_ci.py:4455-4537`, arms `:12188-12257`). The proof's live failure paths: `start_target` `:250-265`, `remove_target` `:268-281` (unanswerable queries read as `unknown`), `isolation` `:284-298`, `ended`/`await_holder` `:217-232`, `collide` `:322-343`. Cap semantics against the doc at `CI_WORKFLOWS.md:1826-1841`. | R266-3 | 604297bb41d6c8005d07539289b10bfa99273cdd |
| Tests | UNCLEAN (F1, F2, F3) | Proof self-test `act_slot_proof.sh:366-624` under 56 mutants plus a control in both uid modes, with repeats and a feasibility probe. Runner arms `act_ci.py:12188-12257`, with hosted exact-head results and author receipts. | R266-3 | 604297bb41d6c8005d07539289b10bfa99273cdd |
| Docs | UNCLEAN (F1, F2) | `CI_WORKFLOWS.md:1709-2033` (slot section, memory bullets, `DOCKER-USER` note, the proof's case list and uncovered guards, runner pins). `act_ci.py` comments and docstrings `:149-160`, `:4455-4512`. PR body DoD and validation lines. | R266-3 | 604297bb41d6c8005d07539289b10bfa99273cdd |

Lens lines, in findings format:

```text
[R266] PASS Conformance - issue #532 acceptance 1-6 and the DECISION as amended vs scripts/act_ci.py:4234-4537 and scripts/act_slot_proof.sh:139-364 at 604297bb; receipts/diff-scope-604297bb.txt (no workflow file) - acceptance 2-6 hold, the one new refusal is a tightening; acceptance 1 is pending the manager's live proof and is not banked
[R266] PASS RTL - scripts/act_ci.py:149-160, :4234-4537, :5260-5305, :13380-13455 and the runner/proof line contract (act_slot_proof.sh:171, :218, :224, :239-240) - lifecycle order, error paths, cap placement and interfaces hold
[R266] PASS Robustness - scripts/act_ci.py:4455-4537 with arms :12188-12257; scripts/act_slot_proof.sh:217-343 - malformed, missing and unreadable inputs fail closed; unanswerable proof queries read as unknown
[R266] MINOR Tests - scripts/act_slot_proof.sh:275-276, :284-312, :307-308, :366-624 - F1, F2, F3
[R266] MINOR Docs - docs/testing/CI_WORKFLOWS.md:1955-1984 - F1, F2 (the case list and "Two guards have no case" overstate coverage)
```

## Prior public findings, resolved or retained at this head

Read only after the verdict, findings and ledger above were written.

- Round-2 findings: each one's own published script was rerun unmodified against a byte-identical scratch copy of the head proof, as uid 1000 and uid 0.
- Round-1 findings: rechecked through the round-2 diff scope, the prior stand-ins and the mutant sets.

| Finding | Severity; lenses as filed | Status at 604297bb | Evidence |
|---|---|---|---|
| Manager SOURCE VALIDATION r1 (29 scope-gate findings at `fcce541b`) | gate failure | RESOLVED | `check_baremetal_only.py --check` 0 findings; `--selftest` 441 arms (`receipts/gates/`). Masks unchanged this round. |
| R266-1 F1 = R267-1 F1: a slot reaches host-routed container networks and published ports | MAJOR; Conformance, RTL, Robustness, Tests, Docs | RESOLVED | Firewall and uplink code (`act_ci.py:4066-4142`) is untouched by round 2 (`receipts/diff-scope-604297bb.txt`). Its published mutants apply once at the head (`receipts/slot-mutant-applicability-604297bb.txt`) and are recorded KILLED in the author's exact-head receipts. The hosted exact-head self-test passes. The live control is the proof's isolation check, which the manager runs live. |
| R266-1 F2: absence proofs and query failures uncontrolled | MAJOR; Tests, Docs | RESOLVED | Teardown code and its arms are untouched: the head's label set against `f5497170` has one reworded memory label and two added, none lost. Mutants apply once and are recorded KILLED. |
| R266-1 F3 = R267-1 F2: `PROVED` with no run; the slot-0 collision optional | MAJOR; Tests, Conformance (R267-1 also Docs) | RESOLVED | The proof's live logic is unchanged apart from one FAIL message. Both published round-1 refusing stand-ins end with exit 1 and no `PROVED` at the head (`receipts/prior-standins-vs-head-604297bb.txt`). My C01, C05, C06 and H04 are KILLED. |
| R266-1 F4: slot resource and lock prose | MINOR; Docs | RESOLVED | Lock timing `CI_WORKFLOWS.md:1733-1738` is unchanged. The memory prose at `:1819-1841` is exact (above). |
| R266-1 F5: six slot behaviours uncontrolled | MINOR; Tests | RESOLVED | The six mutants apply once and are recorded KILLED at the head; their arms are untouched. |
| R266-1 F6 = R267-1 F5: slot-root check narrower than the DECISION | MINOR; Conformance, Robustness | RESOLVED | `validate_slot_root` `act_ci.py:3817-3852` is untouched. |
| R267-1 F3: R03-R05, R07-R12 and R15 survive | MINOR; Tests, Docs | RESOLVED | They apply once and are recorded KILLED at the head. |
| R267-1 F4: slot cap unattributed | MINOR; Conformance, RTL, Robustness, Docs | RESOLVED | The OOM refusal is kept and tightened (`act_ci.py:4470-4486`). |
| R266-2 F1: no negative control for three isolation and collision guards | MINOR; Tests | RESOLVED | R266-2's script: M1, M2 and M11 KILLED in both uid modes, by exactly the cases for (a), (b) and (c). M3-M8 and M10 are also KILLED. M9 SURVIVES, which R266-2 ruled needs no case and the doc now states. The control SURVIVES. The reviewed copy is byte-exact after the run (`receipts/r266-2-proof-mutants-604297bb-*.txt`). |
| R267-2 F1: proof self-test does not fail when guards are removed | MINOR; Tests | RESOLVED | R267-2's script: P01-P13 all KILLED in both uid modes, and P00 SURVIVES (`receipts/r267-2-proof-mutants-604297bb-*.txt`). |
| R267-2 F2: memory-cap attribution documented as complete | MINOR; RTL, Robustness, Docs | RESOLVED | Doc, comment and docstrings now state exactly what is refused and what is not. The count is printed. The requested arm (a `FAILED` body at the cap with no `oom`) exists and is hosted-executed. Its mutant is recorded KILLED only by that arm. |

Nothing earlier is retained.

F1-F3 are new. They are in the same class as R266-2 F1 and R267-2 F1, but concern guards neither published set mutated:

- slot B's own isolation probe;
- a failed `docker network ls` after removal (R267-2's P11 is network survival, which is killed);
- the B side and the waits of the overlap check (R267-2's P09 removes both `ended` tests together, which is killed).

**Suggestions.** R266-2 S1 was taken, and the note is correct. R267-2 S1-S3 were not taken, which is allowed; they are optional and do not affect coverage.

- **R267-2 S1:** no workflow runs `act_slot_proof.sh --selftest`. That is still true at the head.
- **R267-2 S2:** the overlap check reads unflushed verdict lines. This is distinct from F3. F3 is about the self-test's grading, not the live read.

## Real limits

**Runner not executed.** This round did not run `scripts/act_ci.py`: not host-side, not imported, and not its self-test.

- Its 424-check result rests on two sources: the hosted `docs-check` job, which executed it on this head's bytes, and the author's sandbox receipts.
- The 56/56 slot-mutant kills, for uid 1000 and uid 0, rest on the author's receipts. This round confirmed statically that each edit applies exactly once. It did not re-execute them.

**Nothing live.**

- No Docker, act, sudo, host privilege, slot, cgroup or hardware was used.
- The memory-cap semantics were checked against the cgroup-v2 counter definitions by reading. R267-2's small-scale probe is the published measurement; this round did not repeat it.
- Acceptance 1 is NOT MET until the manager's audited live proof.
- Physical calibration was NOT RUN. The skipped hosted context is not hardware proof.

**Probe method.**

- Proof self-tests and mutants ran on scratch copies, in new unprivileged user and network namespaces.
- Two self-tests ran at a time (one per uid mode), each with its own 38 internal parallel cases. The race-dependent kill rates in F3 were measured under that load.
- The feasibility copy is evidence that deterministic cases exist. It is not a proposed patch.

**Not run, not claimed.**

- No full parent, PP, gPTP, Yosys or builder bank was run; only focused gates.
- The scoped Verilator was not used, because no HDL is in the diff, so its identity was not checked.
- The manager's source static/builder and native banks for this head are still running.
- The final current-dev candidate was not built. Its source base is `ede8d48e`; live dev is `26d855a9`.

**Clone state** (`receipts/clone-integrity-604297bb.txt`):

- After all probes: HEAD and tree are exact, the index matches HEAD, there are no hidden index flags, and there are 0 untracked or ignored entries.
- All 873 tracked files match their blob ids and modes, hashed from disk.
- `third_party/verilog-axis` `48ff7a7e`, `protocol-processor` `424c688f` and `gptp-processor` `c1b61743` are at their pins and clean. `external` (`efeb541a`) is uninitialised, as intended.
- The focused gates had left five ignored bytecode files. They were created by this round and removed before the final check.
- The clone's remote-tracking refs were refreshed to read live dev and the public evidence commit `ead93cd7`. No tracked content or index changed.

## Pending manager duties

1. **Fixing head.** Assign F1-F3. Re-review the fixing head, re-covering Tests and Docs, plus any lens whose scope that commit touches. `act_slot_proof.sh` is the acceptance-1 instrument, so Conformance is re-covered if its live logic moves.
2. **Live proof.** Run it with an audited, installed copy of the reviewed runner: `act_slot_proof.sh --selftest` first, then the ten checks, including an `rtl-full` pair whose logs record each slot's peak and cap-hit count. This covers acceptance 1 and the live halves of 2 and 3.
3. **Banks and acceptance.** Publish the source static/builder and native banks for this head, and own hosted and act acceptance.
4. **Merge turn.** Build and gate the current-dev candidate. After merge, run containment, then close the issue and move the card. The merge bar requires two independent positive reviews and the full completion bar.

## Packet (every file below is listed in MANIFEST.sha256)

**Scripts:**

- `scripts/sandbox.sh`
- `scripts/proof_mutants.py`
- `scripts/run_proof_mutants.sh`
- `scripts/feasibility_cases.py`
- `scripts/focused_gates.sh`
- `scripts/slot_mutant_applicability.py`
- `scripts/writable_no_bit_probe.sh`
- `scripts/clone_integrity.sh`

**Receipts:**

- `receipts/proof-selftest-head-uid1000.txt` and `-uid0.txt`
- `receipts/proof-mutants-head-uid1000.txt` and `-uid0.txt`
- `receipts/proof-mutants-overlap-repeats-uid1000.txt`
- `receipts/feasibility-selftest-uid1000.txt`
- `receipts/feasibility-mutants-uid1000.txt` and `-uid0.txt`
- `receipts/r266-2-proof-mutants-604297bb-uid1000.txt` and `-uid0.txt`
- `receipts/r267-2-proof-mutants-604297bb-uid1000.txt` and `-uid0.txt`
- `receipts/prior-standins-vs-head-604297bb.txt`
- `receipts/slot-mutant-applicability-604297bb.txt`
- `receipts/writable-no-bit-probe.txt`
- `receipts/focused-gates-summary.txt` and `receipts/gates/*.log`
- `receipts/hosted-check-runs-604297bb.tsv`
- `receipts/hosted-docs-check-act-ci-selftest-excerpt.txt`
- `receipts/diff-scope-604297bb.txt`
- `receipts/clone-integrity-604297bb.txt`

R266-3 FINISHED
