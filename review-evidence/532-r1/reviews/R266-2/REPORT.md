[R266] NEGATIVE - exact head f5497170a2c444e01175683606310dbe7fbb2816

Round R266-2: internal, cleared-context re-review of issue #532 / PR #533, correction round 1 (three commits: `f82018a7`, `ba13a62c`, `f5497170`).

- Exact head `f5497170a2c444e01175683606310dbe7fbb2816`, tree `c340d594d9d3576f8a469ce4031c129ea8616183`.
- The PR's net change against the live dev it merged (`759da623`) is four files: `scripts/act_ci.py`, `scripts/act_slot_proof.sh`, `docs/testing/CI_WORKFLOWS.md` and `scripts/check_baremetal_only.py`.
- The correction round (`a37af3c6..f5497170`) touches only the first three.

**Verdict: NEGATIVE.**
- One new MINOR finding (F1, Tests) is open.
- Every earlier finding is resolved at this head, under its original severity and lens: R266-1 F1-F6 and R267-1 F1-F5.
- Conformance, RTL, Robustness and Docs are covered clean at this head. Tests is UNCLEAN.

## 1. How this round was run

**Reconstruction order:**
1. AGENTS.md, CONTRIBUTING.md and docs/README.md.
2. Issue #532: frozen acceptance 1-6, the assignment, the author's TAKEN and DECISION (issuecomment-5796770637), both earlier REVIEW READY comments, the correction assignment, and A213's REVIEW READY with its amendments (issuecomment-5800878550).
3. PR #533's body and the manager's comments: SOURCE VALIDATION r1 and the review-start comments.
4. `docs/testing/CI_WORKFLOWS.md`: "Act-first local replication" and "Parallel replay slots".
5. The diff `ede8d48e..f5497170`. Its net change against dev is `759da623..f5497170`, and the correction diff is `a37af3c6..f5497170` (histogram), with history.
6. The public evidence `d95083d3:review-evidence/532-r1/correction-a213`, receipts and harnesses only.

**Order relative to the earlier reviews:** my own verdict and ledger were written before I opened the R266-1 or R267-1 report. That draft already held F1 and the same lens results. Section 4 reconciles the earlier findings afterwards.

**Execution limits:**
- The candidate runner was never executed: not host-side, not its self-test, not imported.
- No Docker, act, sudo, privilege or hardware was used.
- Probes ran only on scratch copies, or in unprivileged user and network namespaces. The review clone was verified byte-exact afterwards.

## 2. Findings

### F1 - MINOR - Tests
**Where:**
- The guards: `scripts/act_slot_proof.sh:290-291` (isolation) and `:357` (the slot-0 collision reason).
- The self-test that does not control them: `:445-457` (the stand-in sudo always answers the probe name) and `:529-544` (the case table).

**Title:** The live proof's offline self-test has no negative control for three guards that keep its isolation and no-isolation-collision checks from passing vacuously.

**Authority and evidence:**
- **The rule these guards fall under.**
  - The correction assignment on #532 says: "Every protection gets a negative control that fails when it is removed".
  - AGENTS.md section 6 (Tests) says each test must be able to fail for the defect it claims to detect.
  - `docs/testing/CI_WORKFLOWS.md:1909-1916` states that the slot's refusals hold "while `--probe-name` ... resolves and answers on 443". It also says the host-side probe "must reach both, which shows the targets were live".
  - `:1920-1923` requires that the slot-0 rival be refused "on act's tool-cache or job-volume names".
- **What the mutants show.** In packet `receipts/proof-mutants-r266-2-f5497170.log`, run on scratch copies, the 14-case self-test stays green under three mutants:
  - M1: the slot-side `internet=reached` is no longer required.
  - M11: the host-side reach of the published port is no longer required.
  - M2: the slot-0 refusal reason is reduced to `.`.
- **What is controlled.** The slot-A analogue of M2 (M10) is killed by the existing `rival-other-refusal` case. The case `target-dead` kills both host-side targets together, but never the published port alone.
- **Why this matters with pasta.** The author's public pasta rehearsal (`correction-a213/receipts/pasta-reach-rehearsal-final.log`) shows that blocked targets time out rather than refuse. So from inside a slot, a firewall refusal, a dead target and a dead uplink all read as `refused`. These three guards are the only thing that tells them apart.

**Impact:**
- At this head the three checks are present and correct (read against the code, and the honest self-test case passes).
- Nothing pins them, so an edit can remove any of them with the self-test still green.
- The acceptance-1 instrument could then print `PROVED` in two vacuous ways:
  - an isolation "refusal" from a slot whose uplink or published target is dead;
  - a "collision without isolation" whose rival was refused for an unrelated reason. The pattern `act-toolcache|already exist` is loose enough that this case deserves its own control.

**Required outcome:** self-test cases that fail on the matching `FAIL` line when:
- (a) the slot cannot reach the probe name;
- (b) the host cannot reach the published port while the container answers;
- (c) the slot-0 rival is refused for a reason other than the tool cache or a job volume.

**Verification:** re-run packet `scripts/proof_mutants_r266_2.py` on the fixing head. M1, M2 and M11 must be KILLED, the control must SURVIVE, and `act_slot_proof.sh --selftest` must pass.

The other survivors in that log need no change, because each is backed by another check:
- M3 and M4 (digest and write bits): the runner's own `validate_installed_runner_file`, `scripts/act_ci.py:1245-1271`, repeats both checks on every PR run.
- M5 (non-empty log directory): stale SUMMARY lines cannot produce `PROVED`, because every check records exactly one PASS or FAIL.
- M6 (`ended` ignoring a refusal) and M7 (rival exit status): `complete` and the refusal-text match already imply them.
- M8 (holder marker): replacing it with the workflow-start line is semantically no weaker.
- M9 (the PASS-count guard): every skip path already records a FAIL.

### Suggestions (optional; they do not affect coverage)
- **S1 - Docs, Robustness - `docs/testing/CI_WORKFLOWS.md:1747-1768`, `scripts/act_ci.py:4113-4140`.** Slot traffic leaves as host-originated output through the uplink, so any operator egress policy placed in Docker's `DOCKER-USER` forward chain applies to slot 0's jobs but not to an isolated slot.
  - The author's public pre-change ruleset receipt shows that chain empty on the replay host, so nothing differs there today.
  - One sentence saying that operator egress restrictions must be expressed on the slot's output path too would keep the "stricter than slot 0" reading true on other hosts.

## 3. What was examined and held at this head

**Firewall (R266-1 F1 = R267-1 F1):**
- `slot_uplink_interfaces` (`scripts/act_ci.py:4076-4110`) runs after the residue check and before any creation (`:4253`).
- `slot_firewall_rules` (`:4113-4140`) keeps the host-local reject and adds `oifname != { <uplinks> } counter reject`, both behind the slice's `socket cgroupv2 level 1` selector.
- My unprivileged namespace probe (packet `receipts/firewall-semantics-probe-f5497170.log`, `scripts/firewall_semantics_probe.sh`) loaded the exact rule text the runner's self-test pins, read statically with `ast`. Only the cgroup path and the uplink name were retargeted, and the probing socket stood in the level-1 cgroup it names.

  | Case | Uplink target | Routed container | DNAT-published gateway port | Loopback | Bridge gateway |
  |---|---|---|---|---|---|
  | Head rules | reached | refused | refused | refused | refused |
  | Previous head's single rule | reached | **reached** | **reached** | refused | refused |
  | Selector naming another level-1 cgroup | reached | reached | reached | reached | reached |

  The last row shows that the selector gates both rules.
- The author's public pasta rehearsal covers pasta itself with the selector removed. Together the two receipts cover both halves of the rule.
- My redacted read of this host's `ip -json` default routes (packet `receipts/route-json-shape.txt`) confirms the parser's assumptions: a unicast route omits `type`, and an empty `-6` answer parses as no route.

**Memory cap (R267-1 F4):**
- `require_slot_memory_cap_unexhausted` (`:4453-4482`) reads the slice's own `memory.events.local`. In cgroup v2 that file's `oom` counts only OOMs the slice's own limit caused, never those of a container's 16 GB limit below it.
- It runs after the Docker boundary's teardown and before the slot teardown, including when the body returns `RC_FAILED` (`run_validation`, `:5268-5295`).
- A missing, malformed or unreadable file refuses with exit 2.

**Slot root (R266-1 F6 = R267-1 F5):** `validate_slot_root` (`:3815-3850`) `lstat`s every component from `/` down, and requires a real directory owned by uid 0 and not writable by group or other.

**Lock timing and memory prose (R266-1 F4):**
- `docs/testing/CI_WORKFLOWS.md:1733-1738` matches `run_validation` (`:5248-5268`) and `acquire_replay_slot` (`:4243-4244`).
- `:1812-1830` now says each job container is unchanged, while the slot as a whole is not hosted-shaped.
- The old sentences ("whole invocation", "only its CPUs differ" about the slot) are gone.

**Live proof (R266-1 F3 = R267-1 F2):**
- `complete`, `await_holder`/`ended`, the overlap check, both collisions, the interrupt slot line and the ten-PASS gate (`scripts/act_slot_proof.sh:177-230`, `:232-243`, `:298-362`) all hold.
- The self-test passes 14/14 here (packet `receipts/proof-selftest-f5497170.log`).
- Both earlier rounds' refusing stand-ins, replayed offline against the head script with its own stand-in sudo first on PATH, now end with exit 1 and no `PROVED`: 1 PASS and 9 FAIL each (packet `receipts/prior-standins-vs-head-f5497170.log`).
- Why the overlap check is sound: every completing isolated run flushes its buffered PASS lines through the `memory peak` print, which runs before the slot teardown (`:4516-4519`). So "held, and no verdict yet" is a real common instant.

**Runner self-test (422 arms):**
- The published sandbox logs (uid 1000 and uid 0) and the hosted `docs-check` job `107331098784`, both at this head, each show 422 ok and 0 FAIL, with equal label sets (packet `receipts/selftest-label-recount.txt`, `receipts/hosted-docs-check-excerpt-f5497170.txt`).
- Against `a37af3c6` (363): 4 labels are reworded and each is strictly stronger; 59 are net added; none is lost.

**Mutation sets:**
- All 54 published slot mutants (53 plus the control) and all 15 published proof mutants (14 plus the control) apply exactly once to the head bytes (packet `receipts/slot-mutant-applicability-f5497170.txt`, `receipts/proof-mutant-applicability-f5497170.txt`).
- The published kill logs record 53/53 and 14/14 KILLED, each with its control surviving.

**Amendments to the DECISION:** all five are implemented as recorded, and each is a tightening or a wording fix, never a weakened refusal:
- the second firewall rule and the read-only route query;
- lock timing wording;
- ancestor checks;
- cap exhaustion as exit 2;
- the proof always running the slot-0 collision, plus the isolation control and `sudo -n`.

The slot-0 path returns before any new code (`:4498-4500`), and no workflow file is in the PR diff (acceptance 4 and 6).

**Gates** (packet `receipts/focused-gates-f5497170.log`, all rc 0):
- `check_em_dash.py --base 759da623`: 0 findings over 299 lines.
- `docs_check.py`: 0 findings.
- `gen_toc.py --check`.
- `check_baremetal_only.py --check`: 0 findings over 847 files. `--selftest`: 441 arms.
- `check_py_idiom.py`, `check_sh_idiom.py`, `ci_events.py --check`, `check_doc_paths.py` and `check_doc_style.py`.
- `git diff --check 759da623 f5497170`.
- `bash -n scripts/act_slot_proof.sh`.
- The three correction commits are one line each, with no trailers.

## 4. Earlier public findings on this PR, reconciled at `f5497170`

| Finding | Severity and lenses as filed | Status | Evidence at this head |
|---|---|---|---|
| Manager SOURCE VALIDATION r1 (`fcce541b`), 29 scope-gate findings | gate failure | RESOLVED | `check_baremetal_only.py --check`: 0 findings; `--selftest`: 441 arms (local, and hosted `docs-check`) |
| R266-1 F1: a slot reaches the default daemon's containers and published ports | MAJOR; Conformance, RTL, Robustness, Tests, Docs | RESOLVED | Two-rule table `:4113-4140`, discovered uplinks `:4076-4110`. My namespace probe shows both reached under the previous rule and refused under the head's. Rule text, loaded firewall and route refusals are pinned, and 8 A213 F1 mutants apply and are recorded KILLED. Docs `:1747-1768`, `:1886-1890`. The live control is in the proof (isolation). The live run is the manager's. |
| R266-1 F2: absence proofs and query failures uncontrolled | MAJOR; Tests, Docs | RESOLVED | There are survivor arms for all nine proofs, and residue- and teardown-time query-failure arms. R266's six mutants apply and are recorded KILLED. The doc list `:1978-1982` matches the arms. |
| R266-1 F3: the proof can print `PROVED` with no run, and the no-isolation collision is optional | MAJOR; Tests, Conformance | RESOLVED | `complete` `:177-185`, the unconditional `collide 0` `:357`, the interrupt slot line `:238`. The R266-1 refusing stand-in now ends with exit 1 and no `PROVED` (packet receipt). The remaining guard-control gap is the new F1, not a retention. |
| R266-1 F4: slot resource and lock prose inaccurate | MINOR; Docs | RESOLVED | `CI_WORKFLOWS.md:1733-1738`, `:1812-1830` |
| R266-1 F5: six slot behaviours uncontrolled | MINOR; Tests | RESOLVED | The six mutants apply and are recorded KILLED. There are arms for root validation on acquisition, the CPU boundary at 11/12 CPUs, signal-blocked teardown, non-active slice states, dangling symlinks, and the interrupt gate entering its slot. |
| R266-1 F6: slot-root check narrower than the DECISION | MINOR; Conformance, Robustness | RESOLVED | `validate_slot_root` `:3815-3850`, with arms for a symlinked, user-owned, group-writable, sticky 1777, non-directory or missing ancestor |
| R267-1 F1 (= R266-1 F1) | MAJOR; Conformance, RTL, Robustness, Tests, Docs | RESOLVED | As R266-1 F1. The proof's probe leaves the slot namespace through the same pasta path a job container uses, toward a listener on a default-daemon bridge, so it tests the requested control's rule path. |
| R267-1 F2: vacuous `PROVED`; interrupt gate ungraded for its slot | MAJOR; Tests, Conformance, Docs | RESOLVED | As R266-1 F3. The R267-1 stand-in now ends with exit 1 and no `PROVED`. R01 and R02 are recorded KILLED. The docs describe the ten checks at `:1900-1937`. |
| R267-1 F3: R03-R05, R07-R12, R15 survive | MINOR; Tests, Docs | RESOLVED | Each applies once and is recorded KILLED as uid 1000 and uid 0; the doc lists what is pinned |
| R267-1 F4: slot memory cap unattributed and unmeasured | MINOR; Conformance, RTL, Robustness, Docs | RESOLVED (attribution option) | `oom` in the slice's local events means exit 2 naming the cap, with the peak printed. Arms plus 4 mutants cover it. The doc sentence is corrected and the measurement is left to the live `rtl-full` pair. |
| R267-1 F5 (= R266-1 F6) | MINOR; Conformance, Robustness | RESOLVED | As R266-1 F6 |

The earlier suggestions are optional:
- R266-1 S4 (literal `show` pins) and S5 (overlap) were taken.
- R266-1 S1-S3 and R267-1 S1-S5 were not taken. They do not affect coverage.
- On R267-1 S1 (keeping the table while the uplink survives): I found the risk remote. The uplink unit's default stop timeout ends pasta before the independent table deletion can run after the slice stop.

## 5. Lens results (evidence for every lens, clean or not)

```text
[R266] PASS Conformance - issue #532 acceptance 1-6, DECISION issuecomment-5796770637 and A213 amendments vs scripts/act_ci.py:4064-4140, :4232-4312, :4453-4523, :3815-3850 and scripts/act_slot_proof.sh:343-362; packet receipts/firewall-semantics-probe-f5497170.log; git diff --stat 759da623..f5497170 (4 files, no workflow) - design, amendments and acceptance 2-6 hold; acceptance 1's live half is the manager's and is not banked here
[R266] PASS RTL - no hdl/, tb/, syn/, constraints/ or processor path in 759da623..f5497170; scripts/act_ci.py:4232-4450 (acquire order, lease-before-create, independent teardown), :4531-4550 (cpuset 4N..4N+3 < host CPUs), :4453-4482 (slice-local oom semantics), :176 (15-character interface names) - lifecycle state, error paths and resource bounds checked against cgroup v2 and nft semantics
[R266] PASS Robustness - scripts/act_ci.py:4076-4110 plus packet receipts/route-json-shape.txt (malformed, failed, unreachable, multipath and no-route inputs), :4156-4196 and :4315-4332 (unanswerable queries fail closed; any unit state but absent is residue), :4461-4470 (unreadable or malformed events), :4520-4523 (teardown with signals blocked), :3815-3850 (ancestors) - fail-closed on every input examined
[R266] MINOR Tests - scripts/act_slot_proof.sh:290-291, :357, :445-457, :529-544 - F1 (three guards without a negative control); runner self-test 422/0 at head, published mutant sets apply at head, proof self-test 14/14 and the earlier stand-ins refused
[R266] PASS Docs - docs/testing/CI_WORKFLOWS.md:1709-1993 against the code lines above and the 422 self-test labels; scripts/act_ci.py:25-31 docstring; packet receipts/focused-gates-f5497170.log - every changed contract is stated accurately, and the corrected lock and memory prose matches the code
```

## 6. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #532 acceptance 1-6, DECISION and A213 amendments; `scripts/act_ci.py:3815-3850`, `:4064-4140`, `:4232-4312`, `:4453-4523`, `:5236-5295`; `scripts/act_slot_proof.sh:343-362`; packet `receipts/firewall-semantics-probe-f5497170.log`; PR diff file list | R266-2 | f5497170a2c444e01175683606310dbe7fbb2816 |
| RTL | CLEAN | PR diff (no HDL, testbench, synthesis or processor path); `scripts/act_ci.py:176`, `:4232-4450`, `:4453-4482`, `:4531-4550` | R266-2 | f5497170a2c444e01175683606310dbe7fbb2816 |
| Robustness | CLEAN | `scripts/act_ci.py:3815-3850`, `:4064-4110`, `:4156-4196`, `:4315-4450`, `:4461-4470`, `:4486-4523`; packet `receipts/route-json-shape.txt`, `receipts/firewall-semantics-probe-f5497170.log` | R266-2 | f5497170a2c444e01175683606310dbe7fbb2816 |
| Tests | UNCLEAN (F1) | `scripts/act_slot_proof.sh` self-test and checks; published 422-arm logs and hosted `docs-check` job `107331098784`; published slot and proof mutant sets (applicability and kill logs); packet `receipts/proof-mutants-r266-2-f5497170.log`, `receipts/proof-selftest-f5497170.log`, `receipts/prior-standins-vs-head-f5497170.log`, `receipts/selftest-label-recount.txt` | R266-2 | f5497170a2c444e01175683606310dbe7fbb2816 |
| Docs | CLEAN | `docs/testing/CI_WORKFLOWS.md:1232-1323`, `:1709-1993`; `scripts/act_ci.py:1-36` docstring; packet `receipts/focused-gates-f5497170.log` | R266-2 | f5497170a2c444e01175683606310dbe7fbb2816 |

## 7. Real limits

**Nothing live was exercised:**
- No slot was run live: no service-manager units, pasta on the host, slot dockerd, real `memory.events.local`, teardown absence, interrupt gate or `act_slot_proof.sh` live run.
- The firewall behaviour is shown in an unprivileged namespace model. It uses the exact rule text and a real cgroup selector, but not pasta. The author's public rehearsal covers pasta, but without the selector.

**The runner was not executed:**
- Under the bootstrap rule and this round's limits, `scripts/act_ci.py` was never run.
- The 422-arm result and the 53/53 slot-mutant kills therefore rest on the published sandbox receipts and on the hosted `docs-check` job at this head.
- This round checked statically that every published mutant applies exactly once to the head bytes, and recounted the labels.

**My own probes were bounded:**
- My proof mutants are a focused set of 11 plus a control, not an exhaustive one.
- No Verilator, Yosys, builder or parent/PP/gPTP bank was run, because no RTL is in scope. The scoped Verilator was not used, so its identity was not checked.

**Hosted state at observation** (packet `receipts/hosted-check-runs-f5497170.tsv`): 22 check runs.
- 21 executed and succeeded, including `docs-check`, `elaborate`, `rtl-fast`, `wire-accountability`, `docs-check-no-git`, `full-ci-gate`, `verilator-suites` and `yosys-portability`, with all Verilator and Yosys shards.
- `Physical gPTP (nightly and manual)` was skipped. That is not hardware proof, and physical calibration was NOT RUN.
- Hosted and act acceptance belong to the manager.

**Not claimed:**
- The manager's source static/builder and native banks for this head, which are still running.
- The final current-dev candidate (source base `ede8d48e`, live dev `26d855a9`), which this clone does not contain.

**Clone after probes** (packet `receipts/clone-integrity-f5497170.txt`):
- HEAD, tree and index are exact.
- 873 tracked entries match their blobs and modes, with no hidden index flags and no untracked or ignored paths.
- `third_party/verilog-axis` 48ff7a7e, `protocol-processor` 424c688f and `gptp-processor` c1b61743 are checked out at their gitlinks. `external` (efeb541a) is uninitialised, as intended.

## 8. Pending manager duties

- **F1:** have it fixed. Then re-review the fixing head, re-covering Tests and every other lens whose scope that commit touches (`scripts/act_slot_proof.sh` is also the acceptance-1 instrument).
- **Live proof:** run the privileged live proof with an audited install of the reviewed runner: `act_slot_proof.sh --selftest`, then the ten-check proof including an `rtl-full` pair so each slot prints its memory peak. This is acceptance 1, and the live halves of acceptance 2 and 3.
- **Banks:** publish the source static/builder and native banks for this head.
- **Merge turn:** build and gate the current-dev candidate merge. After merge, run containment.
- **Merge bar:** two independent positive reviews and the full completion bar.

## 9. Packet contents (listed in MANIFEST.sha256)

**Scripts:**
- `scripts/proof_mutants_r266_2.py`
- `scripts/mutant_applicability.py`
- `scripts/pinned_firewall_text.py`
- `scripts/firewall_semantics_probe.sh`
- `scripts/route_json_shape.py`
- `scripts/prior_standins_vs_head.sh`
- `scripts/clone_integrity.sh`

**Receipts:**
- `receipts/proof-mutants-r266-2-f5497170.log`
- `receipts/proof-selftest-f5497170.log`
- `receipts/prior-standins-vs-head-f5497170.log`
- `receipts/slot-mutant-applicability-f5497170.txt`
- `receipts/proof-mutant-applicability-f5497170.txt`
- `receipts/selftest-label-recount.txt`
- `receipts/firewall-semantics-probe-f5497170.log`
- `receipts/route-json-shape.txt`
- `receipts/focused-gates-f5497170.log`
- `receipts/hosted-check-runs-f5497170.tsv`
- `receipts/hosted-docs-check-excerpt-f5497170.txt`
- `receipts/clone-integrity-f5497170.txt`

R266-2 FINISHED
