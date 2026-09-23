[R267] NEGATIVE - exact head f5497170a2c444e01175683606310dbe7fbb2816

Round R267-2: external independent review of issue #532 / PR #533, after correction round 1 (A213).
Exact head `f5497170a2c444e01175683606310dbe7fbb2816`, tree `c340d594d9d3576f8a469ce4031c129ea8616183`.

The lane changes four files against the merged dev parent `759da623`:

- `scripts/act_ci.py`
- `scripts/act_slot_proof.sh`
- `docs/testing/CI_WORKFLOWS.md`
- `scripts/check_baremetal_only.py`

The correction round is `f82018a7`, `ba13a62c` and `f5497170`. Each is one line with no trailer, and together they touch the first three files.

Verdict: **NEGATIVE**. Two MINOR findings are open:

- F1, under Tests;
- F2, under RTL, Robustness and Docs.

Every finding from R266-1 and R267-1 is resolved at this head, as is the manager's SOURCE VALIDATION r1 finding. Conformance is covered clean.

## How this round was run

**Reconstruction order:**

1. AGENTS.md, CONTRIBUTING.md and docs/README.md.
2. Issue #532: the body with frozen acceptance 1-6, the ASSIGNMENT, TAKEN, DECISION (issuecomment-5796770637), the three REVIEW READY posts and the A10 assignments.
3. The PR #533 body and the manager's comments.
4. `docs/testing/CI_WORKFLOWS.md`: "Act-first local replication" and "Parallel replay slots".
5. The diff `ede8d48e..f5497170`, the net diff `759da623..f5497170` (histogram), the correction diff `a37af3c6..f5497170`, and the history.
6. Public evidence: the tree `d95083d3:review-evidence/532-r1`, the exact-head hosted check runs, and the hosted `docs-check` logs at `f5497170` and `a37af3c6`.

**What was withheld:**

- No private author material, and nothing from the management tree.
- No other reviewer's report for this head. The concurrent R266-2 was not read.
- R266-1 and R267-1 were read only after this round's own pass over the diff was complete and its candidate findings were written down.

**Bootstrap rule:**

- This round never executed the candidate `act_ci.py`: not host-side, not imported, and not its `--selftest`.
- The runner self-test evidence is the exact-head hosted `docs-check` job, which executed it.
- The refusal comparison parses the runner source with `ast`, which does not run it.

**Proof script:**

- `act_slot_proof.sh --selftest` ran in a network-less user namespace (`unshare --user --map-current-user --net`). So did every mutant and control probe of it.
- The probes ran one self-test at a time, on private copies, against the script's own offline stand-in runner and `sudo`.
- The tracked file was never modified.

**Firewall rehearsal:**

- It ran in unprivileged user, net, mount and pid namespaces, with no Docker, act, sudo or host network change.
- The rule text was transcribed from the head's pinned self-test arm, and pasta was run with the runner's exact option set.
- The cgroup selector was kept. It points at a child of this session's own delegated cgroup.

**Memory probe:** three disposable transient scopes of the invoking user's own service manager, removed on exit.

**Not used:** hardware and every full bank. The diff contains no HDL, so the scoped Verilator was not used and its identity was not checked.

## Findings

### R267-2-F1 MINOR - Tests: the proof's offline self-test does not fail when several of its protective checks are removed

**Where** (all in `scripts/act_slot_proof.sh`):

- `:177-185`: `complete`, the exit-status half of the completion rule.
- `:290-291`: the isolation check requires `internet=reached` from inside the slot.
- `:357`: the slot-0 collision reason, `act-toolcache|already exist`.
- `:122-135`: `verify_runner`.
- `:266-279`: `remove_target`, network survival.
- `:113-119`: the slot arguments.
- `:237`: the interrupt gate's PASS line.
- `:529-544`: the graded cases.

**Authority:**

- The A10 correction assignment on #532: "Every protection gets a negative control that fails when it is removed".
- AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect".
- R266-1 F3 and R267-1 F2 required that "any exit-2 run fails the proof".

**Evidence, `receipts/proof_mutants.txt`** (13 single-site mutants on private copies, one at a time):

- SURVIVED:
  - P01: the inside-slot internet answer is no longer required.
  - P02: the slot-0 rival may be refused for any reason.
  - P03: a run that printed every PASS counts, whatever its exit status.
  - P04: a FAILED run counts, whatever its exit status.
  - P05, P06 and P07: the audited digest, the read-only install and the empty log directory go unchecked.
  - P11: a surviving target network goes unreported.
  - P12: slot A may equal slot B, or be 0.
  - P13: the interrupt gate's PASS line is not required.
- KILLED, as expected: P08, P09 and P10.
- The no-op P00 survives.

**Evidence, `receipts/proof_controls.txt`:**

- Four stand-in cases were added to a private copy:
  - a run that passes every workflow and is then refused;
  - a FAILED run that is then refused;
  - a slot whose uplink is dead;
  - a slot-0 rival refused for another reason.
- The head's checks already fail each case correctly (18 of 18 cases pass).
- Each new case kills exactly its mutant: P01, P02, P03 and P04.
- Under P03, the stand-in proof prints `PROVED` even though every run was refused after its workflows.

**Evidence, the author's own set:** `correction-a213/receipts/proof-mutants-final.log` in the evidence tree mutates the shared refusal grep, which the slot-1 case kills. It has no slot-0-only, exit-status or dead-uplink mutant.

**Impact:**

- The proof's logic is correct at this head, but its offline grading pins three guards nowhere:
  - the exit-status half of the completion rule, which is the central repair of R266-1 F3 and R267-1 F2;
  - the internet requirement, which separates a firewall refusal from a dead uplink;
  - the reason for the no-isolation collision.
- Any of these can be deleted with `--selftest` still green. The live proof would then:
  - accept runs refused after their workflows (slot teardown not proved, slot cap exhausted, head moved);
  - grade isolation from a slot with no connectivity;
  - credit an unrelated slot-0 failure as the collision.

**Required outcome:**

- `--selftest` has a failing case for each of those guards, so P01-P04 are killed.
- P05-P07 and P11-P13 are either killed by cases too, or the doc states which proof preconditions the offline self-test does not grade.

**Verification:** at the fixing head, `scripts/proof_mutants.py` reports P01-P07 KILLED (and P11-P13 too, unless documented), and P00 SURVIVED.

### R267-2-F2 MINOR - RTL, Robustness, Docs: the slot memory-cap attribution is documented as complete, but it sees only an OOM at the cap

**Where:**

- `docs/testing/CI_WORKFLOWS.md:1821-1828`: "A run in which the slot cap itself ran out is refused, never reported as a verdict ... so a cap-induced failure cannot pass for the candidate's `FAILED`".
- `scripts/act_ci.py:149-157`, the comment on `SLOT_MEMORY_MAX`: "a run the cap itself cut short is refused rather than reported as a verdict".
- The check itself, at `scripts/act_ci.py:4453-4482`.

**Authority:**

- The runner refuses only on a nonzero `oom` in the slice's own `memory.events.local`.
- The Linux cgroup v2 admin guide (`memory.events`) says `oom` counts the times usage reached the limit and an allocation was about to fail. It also says the event is not raised when the OOM killer is not considered an option, for example for failed high-order allocations or callers that asked not to retry.
- A limit that direct reclaim can still satisfy raises `max`, not `oom`.

**Evidence, `receipts/memcap_probe.txt`** (MemoryMax=128M and MemorySwapMax=0, the slot's shape at small scale):

- The positive control is recorded as the runner expects: `oom 1`, `oom_kill 1`.
- A workload held 100 MiB of anonymous memory and re-read 192 MiB of its own files. It ran about 7.5 times slower than the same workload uncapped: 0.45 s against 0.06 s.
- Under the cap:
  - `max` rose from 172 to 5361;
  - `memory.peak` equalled the cap;
  - memory pressure `full` rose by 87 ms;
  - `oom` stayed 0.
- The runner's check would accept that run and print "which never ran out".

**Relation to R267-1 F4:** that finding is satisfied as written, since an OOM kill inside the slice is now exit 2. This is the residual it leaves, raised here because the head's text now claims more than the check does.

**Not attributed to Conformance:** no acceptance criterion and no DECISION clause requires detecting cap effects other than OOM, and the doc states that the cap is unmeasured.

**Impact:**

- A slot run held at its 24G no-swap cap can be slowed by reclaim into a workflow timeout, or can see an allocation fail without the OOM path.
- The run is then reported as the candidate's `FAILED` (exit 1), while the authoritative doc tells the operator that cannot happen.
- Only failures are affected. The cap cannot turn a failure into a pass.
- The slot's peak line is the only signal.

**Required outcome.** Either:

- the doc and the constant's comment state exactly what is refused (an OOM at the slot's own cap) and what is not (reclaim throttling at the cap, or an allocation failed without the OOM killer); or
- the runner also flags or refuses a run whose slice reached its cap. It could use `memory.peak` at `MemoryMax`, `max` events or memory pressure beside the peak. A behaviour change needs an offline arm.

**Verification:**

- Re-read the doc and the comment against `require_slot_memory_cap_unexhausted`.
- For a behaviour change: an arm with a FAILED body and a slice at its cap without `oom`.

### Suggestions (optional; they do not affect coverage)

- **S1 (Tests).** No workflow or suite runs `scripts/act_slot_proof.sh --selftest`: nothing under `.github/`, `scripts/*.sh`, `scripts/*.py`, `docs/testing/TESTING.md` or `docs/testing/RUNNING_TESTS.md` references it. Running it beside `act_ci.py --selftest` in the docs workflow would stop it rotting between live proofs.
- **S2 (Tests).** The runner prints the verdict line `act-ci: <workflow>: PASS` without a flush (`scripts/act_ci.py:5230`). The line reaches the log only at the next flushed line or at exit. So with one selected workflow, the overlap check (`act_slot_proof.sh:305-306`) can read a run as un-ended after its only workflow has finished. Flushing that line, or requiring both runs' `act-ci: running` lines before either verdict, would prove that the workflows themselves overlapped.
- **S3 (Robustness).** The residue check (`scripts/act_ci.py:4180-4196`) does not look at the slice's runtime drop-in, although teardown proves it absent (`:4372-4376`). Suppose a dead invocation leaves a cap drop-in and someone removes its namespace by hand. The next run silently re-applies that drop-in and then reverts it, rather than refusing it as residue.

## Prior public findings at this head

| Finding | Original severity; lenses | Status at f5497170 | Evidence |
|---|---|---|---|
| R266-1 F1 = R267-1 F1 | MAJOR; Conformance, RTL, Robustness, Tests, Docs | RESOLVED | Second rule `oifname != { <uplinks> }` at `scripts/act_ci.py:4113-4140`. Uplinks come from unicast default routes (`:4064-4110`), read after the residue check and before creation (`:4253`). The rule text and the loaded firewall are pinned (`selftest_slot_commands` `:11452-11464`, `selftest_slot_uplinks` `:11468`, `selftest_slot_loaded_firewall` `:11662`); hosted-executed, see `receipts/labels_new.txt`. `receipts/firewall_rehearsal/rehearsal.txt`: under the parent head's single rule the slot reached the bridged container, the DNAT-published port and a routed VM network. Under the head's two rules all three and the host-local listener are refused, the uplink LAN and internet stand-ins still answer, and the host reaches everything. The counters put the published port on the second rule. Doc at `CI_WORKFLOWS.md:1747-1768`. The live isolation control is in the proof (`act_slot_proof.sh:245-296`); its live run is the manager's. |
| R266-1 F2 | MAJOR; Tests, Docs | RESOLVED | A survivor arm for each of the nine absence proofs (`SLOT_SURVIVORS` `scripts/act_ci.py:11828`, `selftest_slot_teardown_failures` `:11841`). Unanswerable-query arms at residue (`:11811-11823`) and at teardown (`selftest_slot_teardown_queries` `:11894`); hosted-executed. The doc lists exactly what is pinned (`CI_WORKFLOWS.md:1961-1993`). |
| R266-1 F3 = R267-1 F2 | MAJOR; Tests, Conformance (R267-1 also Docs) | RESOLVED | Completion rule `act_slot_proof.sh:177-185`; `PROVED` only on ten PASS records (`:358`); the slot-0 collision always runs (`:357`); the interrupt arm requires the runner's own slot line (`:237-238`, printed at `scripts/act_ci.py:13410`). R267-1's R01 is pinned by `selftest_live_gate_slot` (`:12220`). The "every run refuses after taking its slot" case (R266-1's and R267-1's scenario) FAILs as required: `receipts/proof_selftest_head.txt`. The remaining missing controls are this round's F1 (Tests), not a retention. |
| R266-1 F4 | MINOR; Docs | RESOLVED | Lock timing (`CI_WORKFLOWS.md:1733-1738`) matches `run_validation` (`scripts/act_ci.py:5248-5268`), `acquire_replay_slot` and `release_replay_slot`. The cap's effect on multi-leg jobs is stated at `:1815-1820`. |
| R266-1 F5 | MINOR; Tests | RESOLVED | Arms cover six properties: root validation on acquisition and the CPU boundary (`selftest_slot_guards` `:12276`), signal-blocked teardown (`:11917`), residue in any non-absent unit state (`:11794-11810`), the dangling-symlink probe (`:12301-12310`), and the live gate entering its slot (`:12220`). |
| R266-1 F6 = R267-1 F5 | MINOR; Conformance, Robustness | RESOLVED | `validate_slot_root` walks every component from `/` with `lstat` (`scripts/act_ci.py:3815-3850`). Ancestor arms at `:11982`; doc at `CI_WORKFLOWS.md:1832-1839`. Recorded as a DECISION amendment in A213's REVIEW READY. |
| R267-1 F3 | MINOR; Tests, Docs | RESOLVED | Arms for each probe: R03, R04, R05 and R07 (survivors); R08 (nft query at residue and teardown); R09 (`:12276`); R10 (literal owner `0` checked through the AST, `selftest_slot_wiring` `:12082`); R11 (exact `sudo -n --` argv); R12 (`:11917`); R15 (`:11794`). The doc claim is narrowed to what is pinned. |
| R267-1 F4 | MINOR; Conformance, RTL, Robustness, Docs | RESOLVED as specified | An OOM inside the slice is exit 2 naming the cap (`scripts/act_ci.py:4453-4482`), with arms at `selftest_slot_memory_cap` `:12165`. The "only its CPUs differ" sentence is corrected (`CI_WORKFLOWS.md:1812-1820`). The residual is this round's F2. |
| Manager SOURCE VALIDATION r1 (29 scope findings) | gate failure | still RESOLVED | `receipts/gate_baremetal_check.txt`: 0 findings over 847 files. `receipts/gate_baremetal_selftest.txt`: 441 arms. The masks are unchanged this round. |

Prior suggestions:

- Taken:
  - R266-1 S4: the `show` queries are pinned as literal argv (`scripts/act_ci.py:11586-11599`).
  - R266-1 S5: overlap is required (`act_slot_proof.sh:299-313`).
- Not taken, and optional: the other suggestions from R266-1 and R267-1.

## Checked and found clean (evidence)

**DECISION amendments.** A213 recorded five amendments, and each matches the code and the doc:

- two rules plus a read-only default-route query before creation (`:4253`, `:4113-4140`);
- the lock held from acquisition to the end of teardown (`:4244`, `:4438-4443`);
- the ancestor rule (`:3831-3850`);
- a slot-cap exhaustion is exit 2 (`:4471-4477`);
- the proof always runs the slot-0 collision and the isolation control, and calls `sudo -n` itself.

The remaining DECISION items (names, argv, teardown order, CPU sets, the inherited-endpoint refusal) are unchanged this round.

**No refusal weakened** (AST comparison of `raise Refusal(...)` expressions between `a37af3c6` and `f5497170`, source only):

- Distinct expressions go from 302 to 311.
- The only three parent texts missing are the old single-component slot-root refusals, which are now stricter per-component refusals.
- No expression is raised fewer times.

**Runner self-test.** The hosted exact-head `docs-check` job executed `act_ci.py --selftest`: 422 `ok`, 0 `FAIL`, `selftest: PASS` (`receipts/hosted_act_ci_selftest.log`). Against the hosted run at `a37af3c6` (363 `ok`):

- 4 labels were reworded, each into a stricter form;
- 59 were added;
- none was lost.

See `receipts/labels_lost.txt` and `receipts/labels_new.txt`.

**Proof self-test.** 14 of 14 cases pass at this head (`receipts/proof_selftest_head.txt`), and the file digest matches the author's receipts: `84d1777f...`.

**Focused gates at this head** (network-less, read-only; `receipts/gate_*.txt`), all rc 0:

- `check_baremetal_only.py --check` (0 findings) and `--selftest` (441);
- `docs_check.py` (0 findings);
- `check_em_dash.py --base 759da623` (0 findings over 299 added lines);
- `check_sh_idiom.py`, `check_py_idiom.py` and `gen_toc.py --check`;
- `git diff --check 759da623..f5497170`.

**Scope of the correction round:**

- Its hunks touch only slot-specific code, self-test arms and help text. They touch no slot-0 path and no workflow file (acceptances 4 and 6).
- All three commits are one line with no trailer.

**Hosted state at the exact head** (`receipts/hosted_checkruns_f5497170.txt`):

- 22 check runs: 21 completed with success, including `rtl-fast`, `docs-check`, `elaborate`, `wire-accountability`, `docs-check-no-git`, `verilator-suites` and `yosys-portability`.
- `Physical gPTP (nightly and manual)` is a skipped context and is not evidence.
- Hosted and act acceptance remain the manager's.

**Clone integrity after every probe** (`receipts/clone_integrity_f5497170.txt`):

- HEAD and tree are exact, with 0 index differences, 0 hidden-index flags and 0 status entries.
- All 873 regular files match their blob bytes and modes.
- The gitlinks `third_party/verilog-axis` `48ff7a7e`, `protocol-processor` `424c688f` and `gptp-processor` `c1b61743` are checked out at their pins.
- `external` is uninitialised, as intended.

## Clean-lens line

[R267] PASS Conformance - issue #532 acceptance 1-6 and DECISION issuecomment-5796770637 with A213's five recorded amendments, against `scripts/act_ci.py:3815-4523` and `:14174-14263` and `scripts/act_slot_proof.sh:122-362`, at f5497170 - the slot selection, per-slot resources, bounds, teardown, slot-0 invariance (the correction hunks leave slot-0 paths untouched), no workflow change and no weakened refusal (`receipts/labels_*.txt`, the AST refusal comparison in this report); the live half of acceptance 1 is pending the manager's audited proof, not claimed

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #532 acceptance 1-6, the DECISION and A213's amendments; `scripts/act_ci.py:3815-4523`, `:5236-5295`, `:14174-14263`; `scripts/act_slot_proof.sh`; the AST refusal comparison; `receipts/labels_*.txt` | R267-2 | f5497170a2c444e01175683606310dbe7fbb2816 |
| RTL | UNCLEAN (F2) | the runner's slot architecture: firewall and uplink (`scripts/act_ci.py:4064-4140`), lifecycle order and rollback (`:4232-4450`), memory cap and resource bounds (`:149-158`, `:4453-4550`); `receipts/firewall_rehearsal/`; `receipts/memcap_probe.txt`; no HDL, tb, syn or constraints file in the diff | R267-2 | f5497170a2c444e01175683606310dbe7fbb2816 |
| Robustness | UNCLEAN (F2) | uplink discovery refusals; residue, teardown and query-failure paths; slot-root ancestors; lock; cap exhaustion (`scripts/act_ci.py:3815-4523`); the proof's timing checks (`act_slot_proof.sh:212-341`); `receipts/memcap_probe.txt` | R267-2 | f5497170a2c444e01175683606310dbe7fbb2816 |
| Tests | UNCLEAN (F1) | the 59 new runner arms (hosted-executed, 422 ok); `selftest_slot_*` at `scripts/act_ci.py:11402-12391`; `receipts/proof_selftest_head.txt`; `receipts/proof_mutants.txt`; `receipts/proof_controls.txt`; the author's proof and slot mutant receipts | R267-2 | f5497170a2c444e01175683606310dbe7fbb2816 |
| Docs | UNCLEAN (F2) | `docs/testing/CI_WORKFLOWS.md:1709-1993`; the runner constant comments and help (`scripts/act_ci.py:138-181`, `:14100-14171`); the proof header (`act_slot_proof.sh:1-42`); the PR body; `receipts/gate_docs_check.txt`, `gate_em_dash.txt`, `gate_gen_toc.txt` | R267-2 | f5497170a2c444e01175683606310dbe7fbb2816 |

## Real limits of this round

**The candidate runner was not executed here.**

- Its 422-check self-test is evidenced by the executed hosted exact-head `docs-check` job and by the label diff.
- The author's 53 slot mutants were not re-run here, because the host-side self-test is excluded for this round.
- Each prior mutant was checked against the arm expected to kill it by reading the arm.

**The firewall rehearsal is a model.**

- It ran on this review host's kernel (7.2.6) and pasta (2026_07_28), not on the build host.
- The selector was adapted to a delegated session cgroup (`level 6`) instead of a top-level slice at `level 1`.
- Docker's published-port DNAT was modelled with an nft nat rule.
- There was no real dockerd, no service-manager unit and no IPv6.

**The memory probe is small.** It ran at 128 MiB. It shows the counter semantics, not the 24G slot on `rtl-full`.

**The proof script was graded only against stand-ins.** Its self-test runs its 14 (here, 18) cases in parallel by its own design, and this round ran one self-test at a time.

**Nothing was run live:**

- no slot daemon, uplink unit, slice, nft table on the build host, interrupt gate or concurrent replay;
- acceptance 1 is not met until the manager's live proof;
- no full parent, PP, gPTP, Yosys or builder bank was run;
- physical calibration was NOT RUN, and skipped hosted contexts are not hardware proof;
- the manager's source static/builder and native banks for this head are not claimed or inferred.

## Pending manager duties

- Publish the source static/builder and native bank results for this head.
- After F1 and F2 are answered and re-reviewed, run the audited-install live proof:
  - `act_slot_proof.sh --selftest` first;
  - then the live proof with the interrupt gate in a slot, completed serial references, overlapping slots, the isolation control and both collision controls;
  - include an `rtl-full` pair, so each slot's peak against the 24G cap is recorded (acceptance 1).
- Hold hosted and act acceptance for the final head.
- At the merge turn, build and gate the current-dev candidate merge. The source base is `ede8d48e`; live dev is `26d855a9` or later.
- Run post-merge containment, then close the issue and move the card.
- Re-cover the lenses at the fixing head:
  - RTL, Robustness, Tests and Docs are unclean here;
  - Conformance must be covered again if the fix changes anything within its scope.

## Receipts (listed in MANIFEST.sha256)

**Scripts:**

- `scripts/proof_mutants.py`: the 13 proof mutants plus a no-op control.
- `scripts/proof_controls.py`: the four candidate negative controls, run against the head's checks and against P01-P04.
- `scripts/firewall_rehearsal.sh`: the unprivileged firewall rehearsal.
- `scripts/memcap_probe.py`: the memory-cap attribution probe.
- `scripts/clone_integrity.py`: the clone-integrity check.

**Receipts:**

- `receipts/proof_selftest_head.txt`
- `receipts/proof_mutants.txt`
- `receipts/proof_controls.txt`
- `receipts/firewall_rehearsal/rehearsal.txt`
- `receipts/firewall_rehearsal/pasta.log` (host nameserver redacted)
- `receipts/memcap_probe.txt`
- `receipts/gate_*.txt`
- `receipts/hosted_checkruns_f5497170.txt`
- `receipts/hosted_act_ci_selftest.log` and `receipts/hosted_act_ci_selftest_a37.log` (public hosted job logs, runner self-test section only)
- `receipts/labels_lost.txt` and `receipts/labels_new.txt`
- `receipts/clone_integrity_f5497170.txt`

R267-2 FINISHED
