[R267] NEGATIVE - exact head 604297bb41d6c8005d07539289b10bfa99273cdd

Round R267-3: the external, cleared-context review of issue #532 / PR #533. Head `604297bb41d6c8005d07539289b10bfa99273cdd`, tree `1a8cfc31dedc8eef7929a5a7529568503fa580d4`. This is correction round 2: five one-line commits on the previously reviewed `f5497170`, touching `scripts/act_ci.py`, `scripts/act_slot_proof.sh` and `docs/testing/CI_WORKFLOWS.md`.

## Verdict: NEGATIVE, from three open MINOR findings

- **Tests:** unclean, from F1, F2 and F3.
- **Docs:** unclean, from F1 and F2.
- **Conformance, RTL and Robustness:** clean at this head.

**Prior public findings: all resolved.**
- R266-2 F1 is resolved. M1, M2 and M11 are KILLED, as are M3-M8 and M10, and the control survives. M9, the ten-`PASS` backstop, survives as documented.
- R267-2 F1 is resolved: P01-P13 are all KILLED and the P00 control survives.
- R267-2 F2 is resolved: the memory-cap docs now state exactly what is detected.

**What remains:** three new, narrower gaps of the same class as those findings. Each is a protective check that the offline self-tests do not reliably kill.
- In the live proof: a failed network query read as absent (F1), and the overlap check's individual conjuncts (F2).
- In the runner: the minimum case and the field identity of the OOM-at-cap refusal (F3).

**Tested against stand-ins only.** The code under test behaves correctly on every case I read or ran. The live proof has not run; it is the manager's.

## How this round was run

**Order of reading:**
1. AGENTS.md and CONTRIBUTING.md.
2. The #532 body: acceptance 1-6.
3. The DECISION and every author and manager comment on #532 and #533, including the A213 and A220 amendments.
4. The diff `ede8d48e..604297bb` and its history. The PR's own change against the merged dev `759da623` is four files: `CI_WORKFLOWS.md`, `act_ci.py`, `act_slot_proof.sh` and `check_baremetal_only.py`. No workflow file changes. `f5497170..604297bb` touches only the first three.

**Independent pass first.** My findings were written to `receipts/independent-pass-before-prior-reviews.md` before I opened any prior review report or reviewer script (`receipts/public-record-read.txt`).

**Where everything ran:**
- Every candidate execution ran only inside `bin/sandbox.sh`. That is a disposable, unprivileged, network-less namespace sandbox:
  - new user, mount, net, pid, ipc, uts and cgroup namespaces, with only `lo`;
  - `/run`, `/tmp` and `$HOME` are empty tmpfs, so there is no Docker socket and sudo is inert;
  - the tree is bound read-only.
- It ran as the namespace's uid 0 and as uid 1000 (no capabilities).
- The trees were exact `git archive` exports of `604297bb` and `f5497170`.
- There was no Docker, act, host runner, privilege, network use (beyond read-only GitHub API queries), or hardware.
- Static gates ran in a disposable clone whose pinned submodules were initialised from the review clone's own checkouts.

**Clone integrity.** The review clone was never written. Before and after, `receipts/clone-integrity-{before,after}.txt` show the same head, tree and index. Tracked bytes and modes are unchanged, and the four gitlinks are at their pins.

**Tool identity.** The scoped Verilator at the given path reports `Verilator 5.050 2026-07-01 rev v5.050`. It was not used, because the PR changes no RTL, testbench or synthesis input.

## Findings

### R267-3-F1 - MINOR - Tests, Docs - a failed isolation-network query is read as absent with no self-test case, and the doc says it is staged

**Where:**
- `scripts/act_slot_proof.sh:275-276`: `networks=$(sudo -n docker network ls ...) || networks=unknown`.
- The stand-in sudo, `:505-506`: `network ls` never fails; only `ps` fails, under `target-query-fails` at `:501-503`.
- The case table, `:604`.
- `docs/testing/CI_WORKFLOWS.md:1969-1973`: "a container or network that survives its removal or cannot be queried after it".
- `CI_WORKFLOWS.md:1979-1984`: "Two guards have no case", naming only the ten-`PASS` backstop and the non-root writability test.

**Authority:**
- The A10 assignment for this round, issuecomment-5803011314: "self-test cases that fail when each protective check of the live proof is removed".
- AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect".
- Docs: "Changed contracts are reflected in authoritative docs".

**Evidence:**
- My mutant Q53 replaces `|| networks=unknown` with `|| networks=""`, so a failed network query reads as absent.
- It SURVIVES the 38-case self-test as uid 1000 and as uid 0 (`receipts/proof-mutants-r267-3-uid{1000,0}-part3.tsv`).
- Its container twin Q52, and the author's A06, are KILLED by `target-query-fails`.
- No published mutant set (R266-2, R267-2, A213, A220) touches the network fallback.

**Impact:**
- The guard is correct at this head.
- An edit that removes it keeps `--selftest` green.
- The live proof could then print `PROVED` although the isolation network's absence was never proved: a daemon that answers `ps` but fails `network ls`.
- In practice both queries usually fail together, so this is a grading gap rather than a live hole.
- The doc tells the operator that this case is graded when it is not.

**Required outcome:** either of these:
- a stand-in fault that fails only `docker network ls`, with a case failing on `FAIL isolation target not proved absent`;
- the doc narrowed to the container query, with the network fallback added to the named guards that have no case.

**Verification:** at the fixing head, `bin/proof_mutants_r267_3.py <tree> <out> user --only Q00,Q52,Q53` reports Q52 and Q53 KILLED and Q00 SURVIVED. Alternatively, the doc sentence names exactly what is staged.

### R267-3-F2 - MINOR - Tests, Docs - the overlap check's conjuncts are killed only when the stand-in's scheduling happens to exercise them

**Where:**
- `scripts/act_slot_proof.sh:307-308`: `await_holder parallel-a && await_holder parallel-b && ! ended parallel-a && ! ended parallel-b`.
- `:222-232`: `await_holder` greps the holder marker, then tests for the status file.
- The cases, `:592-594`.
- The stand-in's `serialize` queue lock, `:412-414`, which whichever parallel run arrives first takes.
- `CI_WORKFLOWS.md:1966-1968` and `:1979`.

**Authority:** as for F1. Overlap was made a required check in round 1, from R266-1 S5.

**Evidence** (`receipts/proof-mutants-r267-3-overlap-repeats-jobs1-uid1000.txt`, the part2 TSVs and `receipts/overlap-order-probe-uid1000.txt`). Each full 38-case self-test was repeated; the tallies below include the two batch runs:

| Mutant | What it removes | KILLED |
|---|---|---|
| Q25 | `! ended parallel-a` | 5 of 6 runs |
| Q26 | `! ended parallel-b` | 3 of 8 runs |
| Q27 | `await_holder parallel-b` | 5 of 12 runs |
| Q28 | `await_holder parallel-a` | 3 of 12 runs |

- The no-op control always survived, and the head's self-test always passed.
- `bin/overlap_order_probe.sh` forces the start order in the `serialize` case:
  - with slot A first, Q26 and Q28 survive and Q27 is killed;
  - with slot B first, Q27 survives and Q26 and Q28 are killed.
- So no fixed schedule kills all three, and the head passes the case under both orders.
- Q25's one survival comes from `:226-227`. When a run prints its marker and ends between the marker grep and the status test, `await_holder` returns "never held". The case then fails on the overlap check without ever reaching the `! ended` guard. At this head that path is fail-closed.
- The published sets only ever removed both `! ended` conjuncts together, which is always killed. That is why the gap did not show before.

**Impact:**
- Each of these guards can be deleted while `--selftest` stays green about half the time or more.
- The PR's claim that the self-test "fails when any of its protective checks is removed" does not hold for them.
- Without `! ended parallel-b`, the live proof could record overlap for a slot-B run whose workflows had all finished before slot A was held. The real runner prints its verdicts before its slot teardown, so B's namespace can still answer the isolation probe.

**Required outcome:** either of these:
- deterministic cases that separately take away each run's hold and each run's liveness (for example, a fault in which only slot B, or only slot A, ends or never announces while the other holds), so Q25-Q28 are killed on every run;
- the doc names these conjuncts among the guards the self-test does not reliably grade.

**Verification:** at the fixing head:
- `bin/overlap_order_probe.sh` (inside `bin/sandbox.sh`) reports every mutant KILLED under both orders;
- five repeats of `bin/proof_mutants_r267_3.py <tree> <out> user --jobs 1 --only Q00,Q25,Q26,Q27,Q28` report Q25-Q28 KILLED every time, and Q00 SURVIVED.

### R267-3-F3 - MINOR - Tests - the OOM-at-cap refusal is pinned only by a two-OOM fixture with equal `oom` and `oom_kill`

**Where:**
- `scripts/act_ci.py:12204`, the only OOM fixture: `"low 0\nmax 9\noom 2\noom_kill 2\n"`.
- The guard itself, `:4474` (`exhausted = int(events["oom"])`) and `:4480` (`if exhausted:`).

**Authority:**
- AGENTS.md section 6, Tests: "Positive, negative, and boundary behavior is covered", and "Tests do not merely reproduce implementation assumptions".
- Linux cgroup v2 records `oom` on the cgroup whose limit was exceeded (the slice), but `oom_kill` on the killed task's own cgroup.
- The slice holds no tasks itself: its jobs and daemons live in child cgroups. So in the slice's `memory.events.local`, a real OOM at the cap reads `oom N`, `oom_kill 0`.

**Evidence** (`receipts/slot-mutants-r267-3-uid{1000,0}.tsv`; same result as uid 1000 and uid 0):
- S07 SURVIVES. It is `if exhausted > 1:`: a single OOM at the cap, the most likely case, is reported as the candidate's verdict.
- S04 SURVIVES. It reads the OOM count from `oom_kill`, which is always 0 in that file, so every OOM at the cap goes unrefused.
- The new code of this round is fully controlled: S01, S02, S03, S05, S06, S08 and S09 are KILLED. The failing arms always include the one meant for the mutant; S03, S05 and S08 also fail wider lifecycle arms.
- S10 (a fallback on a key absent from the fixtures) is contrived and not counted, but has the same cause: the fixtures do not model the real local file.

**Impact:**
- The refusal is correct at this head.
- Two one-token edits would silently disable it for the real case, with the runner self-test green.
- The live proof cannot catch that either, since it grades a refusal only as not completing.

**Required outcome:** an arm with a realistic fixture of exactly one OOM and no local kill (`oom 1`, `oom_kill 0`), refused naming the cap. S04 and S07 are then KILLED.

**Verification:** `bin/slot_mutants_r267_3.py <tree> <out> user` (and `root`) at the fixing head reports S04 and S07 KILLED and S00 SURVIVED. The self-test passes as uid 1000 and 0.

### Suggestions (optional; they do not affect coverage)

- **SG1 (Tests).**
  - Q61 (slot B's parallel verdict exempt from comparison) and Q62 (slot B's isolation view exempt) survive. `parallel-break` breaks only slot 1, and the isolation faults are graded only at `isolation slot 1`.
  - These are per-call-site bypasses of shared guards whose removal is killed (Q20, Q21, Q42), so I do not count them.
  - A slot-B variant of each fault would pin both slots.
- **SG2 (Docs).** `CI_WORKFLOWS.md:1835` is a single 140-character line inside prose wrapped near 76 columns. It is cosmetic, and the style gates pass.
- **SG3 (Docs).**
  - Ordinary page-cache reclaim at the cap also raises `max`, so on a long slot run a nonzero count is routine. R267-2's published probe had already recorded `max` 172 in its capped scope when its measured passes began, with `oom` 0.
  - One sentence saying so would stop an operator reading the count as evidence of cause.
  - The prescribed slot-0 replay is already the right response.

## Prior public findings at this head

| Finding | Severity; lenses as filed | Status at 604297bb | Evidence |
|---|---|---|---|
| R266-2 F1 | MINOR; Tests | RESOLVED | R266-2's published script, replayed verbatim in my sandbox. As uid 1000 and 0, M1, M2 and M11 are KILLED, each by its own new case: `a slot cannot reach the probe name`, `the slot-0 rival is refused for neither the tool cache nor a job volume`, and `the host cannot reach the published port while the container answers`. M3-M8 and M10 are KILLED. M9 (ten-`PASS` backstop) SURVIVES, as R266-2 ruled and the doc records (`CI_WORKFLOWS.md:1979-1981`). The control SURVIVES. Receipts: `receipts/published-proof-mutants-r266-2-604297bb-uid{1000,0}.tsv`. |
| R267-2 F1 | MINOR; Tests | RESOLVED as specified | R267-2's published script: P01-P13 are all KILLED as uid 1000 and 0, and P00 SURVIVES (`receipts/published-proof-mutants-r267-2-604297bb-uid{1000,0}.tsv`). Every case named in its required outcome now exists (`act_slot_proof.sh:575-612`). The remaining gaps of the same class are new, narrower mutants (F1, F2), not a retention. |
| R267-2 F2 | MINOR; RTL, Robustness, Docs | RESOLVED | The same statement appears in three places: the doc (`CI_WORKFLOWS.md:1822-1841`), the constant's comment (`act_ci.py:149-160`) and the docstrings (`:4455-4468`, `:4505-4510`). Each says that only a nonzero slice-local `oom` (an OOM at the slot's own cap) is refused. Neither reclaim at the cap nor an allocation that fails without the OOM killer is detected, and either keeps its verdict. The peak and the `max` count are printed as the only signs, with a slot-0 replay advised. This matches the code (`:4470-4494`) and the kernel semantics. The runner line claims no more: `...; the cap was hit N time(s), with no OOM at it`. The new tightening (events without `max` are refused) has an arm, and the FAILED-at-cap arm pins that such a run keeps its FAILED. |
| R266-2 S1 | suggestion; Docs, Robustness | taken, accurate | `CI_WORKFLOWS.md:1769-1773`. Slot traffic leaves as host output from the uplink (pasta) in the slot slice, so the host's FORWARD-path `DOCKER-USER` chain never sees it. It does apply to slot 0's bridged jobs. The advice to restrict the slice's host output matches the runner's own cgroup-matched output rules (`act_ci.py:4115-4142`). |
| R267-2 S1-S3 | suggestions | not taken | Optional. S1 would need a workflow edit, which acceptance 6 constrains. |
| R266-1 F1-F6, R267-1 F1-F5, manager SOURCE VALIDATION r1 | MAJOR/MINOR as filed | still RESOLVED | Outside the memory-cap hunks, `act_ci.py` is byte-identical to `f5497170`, where R266-2 and R267-2 recorded these resolved. At this head the 53 published A213 slot mutants that pin them, plus A220's 3, are all KILLED as uid 1000 and 0, and the control survives (`receipts/published-slot-mutants-604297bb-uid{1000,0}.tsv`). A213's 14 and A220's 10 proof mutants are all KILLED. The scope gate `check_baremetal_only.py --check` reports 0 findings over 847 files, and `--selftest` reports 441 arms. |

## The requested focus checks

- **Each protective check of the proof has a case that fails when it is removed:** NOT fully met.
  - 63 independent mutants of my own (Q00-Q62), each graded by exactly the case meant for it. Uid 1000: 50 KILLED, 13 SURVIVED. Uid 0: 51 KILLED, 12 SURVIVED.
  - The race-dependent overlap mutants explain the difference between the two uids (F2).
  - **Survivors that are real gaps:** Q53 (F1), and Q25-Q28, race-dependent (F2).
  - **Documented as having no case:** Q08, the non-root writability test that an unprivileged scratch directory cannot stage; Q56, the ten-`PASS` backstop, which is R266-2's M9.
  - **Masked or not protective:**
    - Q05, the required-argument usage check. Every empty value is refused later by the digest check, argument parsing or the runner's worktree validation.
    - Q24, the early exit on an ended run, which only affects liveness.
    - Q49, the empty-address check, backed by the host-reach requirement.
    - Q59, the per-run digest pin. The stand-in does not model it; without it a live run fails closed in `validate_trusted_runner` (`act_ci.py:1222-1245`).
  - **Suggestion only:** Q61 and Q62 (SG1).
- **The reviewers' surviving mutants, including M1, M2 and M11:** KILLED, and the controls survive (table above).
- **The 56 slot mutants:** 56/56 KILLED as uid 1000 and as uid 0, and the control survives. The head's `act_ci.py` sha256 `e8bf06d2...` was byte-exact before and after.
- **The memory-cap attribution docs:** exact, as recorded for R267-2 F2 above. The one test gap in that area is F3.
- **The DOCKER-USER egress note:** accurate, as recorded for R266-2 S1 above.

## Lens results (every lens, with its artifacts)

[R267] PASS Conformance - issue #532 acceptance 1-6, DECISION issuecomment-5796770637 with the A213 and A220 amendments (issuecomment-5800878550, -5804781514) vs `git diff --stat 759da623..604297bb` (4 files, no `.github/` path), `act_ci.py:4455-4536` and `:5281-5308`, `act_slot_proof.sh:345-364`, `CI_WORKFLOWS.md:1709-2032` - acceptance 2-6 hold offline. Slot 0 is untouched this round. The one new refusal (events without `max`) tightens and weakens nothing. Acceptance 1's live half is the manager's and is not banked here.

[R267] PASS RTL - no `hdl/`, `tb/`, `syn/`, constraint or processor path in `759da623..604297bb`. The runner lifecycle at this head:
- the memory report runs only after a body that returns, before teardown, while the slice exists (`act_ci.py:4498-4536`);
- a `return` from inside the slot at `:5308` reaches it;
- a raising body skips it, and teardown stays signal-blocked;
- the slice-local `oom`/`max` fields are read against cgroup v2 recording on `mem_over_limit`.

The rest of the acquisition, firewall and teardown code (`:3976-4450`) is byte-identical to `f5497170`, and its 56 pinning mutants are killed.

[R267] PASS Robustness - checked inputs:
- `act_ci.py:4470-4479`: missing, unreadable or malformed events, or a missing `oom` or `max`, give a Refusal after full teardown (arms `:12202-12226`);
- `:4486-4490`: an unreadable peak is reported, not refused;
- `act_slot_proof.sh:115-137`: non-numeric, equal or zero slots, a digest mismatch, write bits and a non-empty log directory give exit 2 before any record (7 cases);
- `:268-281`: a failed query reads as `unknown` and FAILs;
- `:222-232`: the marker-then-status race fails closed.

Everything examined fails closed.

[R267] MINOR Tests - `act_slot_proof.sh:275-276`, `:307-308`, `:592-594`, `:604`; `act_ci.py:12204` - F1, F2 and F3.
- The runner self-test gives 424 ok and 0 FAIL at the head, as uid 0 and uid 1000 (422 at `f5497170`: 1 label reworded, 2 added, none lost). The hosted docs-check job gives the same 424 labels.
- The proof self-test passes 38 of 38 as uid 0 and uid 1000.
- All published mutant sets apply at this head.

[R267] MINOR Docs - `CI_WORKFLOWS.md:1966-1973` and `:1979-1984` - F1 and F2. Everything else was re-read against the code and the self-test labels and is accurate:
- `:1766-1773` (DOCKER-USER), `:1818-1841` (memory cap), `:1951-1985` (proof self-test groups) and `:2022-2026` (runner pins);
- the proof header, `act_slot_proof.sh:39-44`;
- `act_ci.py:149-160` and `:4455-4468`.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #532 acceptance 1-6, DECISION and amendments; diff `759da623..604297bb` (4 files, no workflow); `act_ci.py:4455-4536`, `:5281-5308`; `act_slot_proof.sh:345-364` | R267-3 | 604297bb41d6c8005d07539289b10bfa99273cdd |
| RTL | CLEAN | no RTL/TB/syn path in the diff; `act_ci.py:4498-4536` lifecycle, `:4455-4494` cgroup semantics, `:3976-4450` byte-identical to `f5497170` with 56/56 pinning mutants killed | R267-3 | 604297bb41d6c8005d07539289b10bfa99273cdd |
| Robustness | CLEAN | `act_ci.py:4470-4494` with arms `:12202-12248`; `act_slot_proof.sh:115-137`, `:222-232`, `:268-281`; 7 bad-start cases | R267-3 | 604297bb41d6c8005d07539289b10bfa99273cdd |
| Tests | UNCLEAN (F1, F2, F3) | runner self-test 424/0 (sandbox uid 0 and 1000, hosted); proof self-test 38/38 (uid 0 and 1000); 63 own proof mutants, 11 own slot mutants, 56 published slot mutants, 52 published proof mutants | R267-3 | 604297bb41d6c8005d07539289b10bfa99273cdd |
| Docs | UNCLEAN (F1, F2) | `CI_WORKFLOWS.md:1709-2032`; `act_slot_proof.sh:1-44`; `act_ci.py:149-160`, `:4455-4509`; focused doc gates green | R267-3 | 604297bb41d6c8005d07539289b10bfa99273cdd |

## Real limits

- **No live run.** Nothing live was run: no Docker, act, privilege, network (beyond read-only API queries) or hardware. Every runtime claim about the slot runner and the proof rests on the repository's stand-ins and fakes, read against the code.
  - The live proof (acceptance 1), with its `rtl-full` pair, is not run.
  - Nor are the uplink discovery, the firewall, the memory events and the teardown on a real host.
- **Sandbox.** My sandbox differs from the author's bubblewrap sandbox. Both give only `lo`, no Docker socket and a read-only tree.
- **Kernel semantics from reading only.** The cgroup v2 statements (where `oom`, `oom_kill` and `max` are recorded) come from the kernel's admin guide and memcontrol source. I did not re-run a live cgroup probe this round.
- **Timing-dependent results.** The race-dependent kill rates in F2 depend on load. I ran one or two self-tests at a time (each forks its 38 cases), on a 16-CPU host.
- **Hosted evidence.** 22 check runs at the exact head: 21 executed and succeeded, including the seven required contexts (`verilator-suites` and `yosys-portability` ran as aggregates). One was skipped: the nightly physical gPTP job, which is not hardware proof. Hosted and act acceptance are the manager's.
- **Not run or claimed:**
  - the manager's full source static, builder and native banks for this head;
  - the parent, PP, gPTP, Yosys or builder banks;
  - the final current-dev candidate (source base `ede8d48e`, live dev `26d855a9`, merge base `759da623`).
- Physical calibration was NOT RUN.

## Pending manager duties

- Publish this packet (REPORT.md and the MANIFEST-listed files).
- After the findings are answered and re-reviewed, run the privileged live proof with an audited install:
  - `act_slot_proof.sh --selftest` first, then the ten checks with an `rtl-full` pair;
  - record each slot's peak and cap-hit count.
- Own the hosted, act and source-validation acceptance for this head, and build and validate the current-dev candidate at the merge turn.

## Packet contents (MANIFEST.sha256)

**`bin/`:**
- `sandbox.sh`
- `clone_integrity.sh`
- `proof_mutants_r267_3.py`
- `proof_one_case.py`
- `overlap_order_probe.sh`
- `slot_mutants_r267_3.py`
- `replay_published_slot_mutants.py`
- `replay_published_proof_mutants.py`

**`evidence-copies/`:** unmodified copies of the published author and reviewer mutant scripts that the replay drivers read.

**`receipts/`:**
- clone integrity, before and after;
- runner self-test logs at both heads, with the label diff;
- proof self-test logs;
- own and published mutant TSVs;
- the overlap repeat and order probes;
- the focused gates;
- the hosted check runs and the hosted runner self-test comparison;
- the independent-pass record and the public-record index.

R267-3 FINISHED
