[R347] NEGATIVE - exact head b7b74b8b20c166cf69f84c2fcbb6162b420cd2d3

# R347-1 external independent review: issue #396 / PR #586

- Round: R347-1, external independent reviewer, cleared context.
- Exact head: `b7b74b8b20c166cf69f84c2fcbb6162b420cd2d3`, tree `1b8951188447bddf54204e146796b6775e4bf72a`. The head is one commit on dev `ac18b50968b12efe4d15c0a06301264b35656b31`.
- Scope reviewed: the desk lane only, acceptance items 1, 2 and 5. Bench items 3 and 4 stay open, and the PR says `Refs #396`.
- Reconstructed from: AGENTS.md and CONTRIBUTING.md; docs/README.md; the #396 issue body; the owner decision (comment 5789765788) and the manager decision and assignment (comment 5854692245); [A356] TAKEN and REVIEW READY; the PR #586 body; issue #75 (the reconnect bound) and #366 (the first-boot defect); REQUIREMENTS.md section 8; TESTING.md 6b/6d; REGISTER_MAP.md; docs/MILAN_V12_ROADMAP.md P3.1; the cited Milan v1.2, IEEE 1722-2016 and IEEE 1722.1-2021 pages (see Real limits for how the pages were extracted); `git diff ac18b509..b7b74b8b`; and the public evidence at `review-evidence/396-r1` (tree 4949b127).
- Prior public review findings on PR #586: none. The PR carries only the two review-start notices, and no PR review objects exist, so nothing needed resolving or retaining.

## Verdict summary

The diff meets the literal desk acceptance:
- REQ-VER-06 is a MUST row with 7 days, 200 cold cuts, the 160/40 split, the soak and per-cycle criteria, one DUT plus the reference peer, and the persisted items as data. The REQ-VER-05 blocker paragraph references it.
- `--plan` emits parameterized `soak` and `power` areas derived from the topology.
- The behave feature and `--self-test` reject a planted missing index, direction and CRF sink.
- CONTRIBUTING section 3 and TESTING 6d name the gate and its artifacts.
- There is no firmware, RTL or builder change, and no claim that the bench items are done.
- Every gate I ran passes.

Four MINOR findings remain open, so the verdict is NEGATIVE:
- Wrong clause citations in the release assertion contract.
- Post-cut time origins and bounds chosen without a recorded decision, which leaves the automatic restore unbounded.
- Audit negative controls that pin only one side of the audit (5 of my audit mutants survive).
- Parameter threading and release eligibility pinned only at default values (3 planner mutants survive).

## Findings

### F1 MINOR - Conformance, Docs - wrong clause citations in the release assertion contract

- **Where:** `tb/tools/torture_campaign.py:3371`, `:3374`, `:3392` and `:3397` (the clause strings of `soak.gptp-continuity`, `soak.tu-within-holdover`, `power.state-restored` and `power.adp-valid-time`).
- **Authority/evidence:** `receipts/citation-check.txt`. Assignment item (1) requires correct Milan/IEEE citations. REQ-VER-06 carries none itself and defers to the TESTING 6d plan contract, so these strings are the citations of record.
  - (a) IEEE 1722-2016 4.4.4.6 is the `sequence_num` field (PDF p37), but it is cited under `tu`. `tu` is 4.4.4.7 only. The 4.4.4.6 authority belongs with the SEQ_NUM_MISMATCH assertion.
  - (b) IEEE 1722.1-2021 6.2.6 is the Discovery State machine, the controller's entity database (p58-60). The decoded valid time is 6.2.2.5: 2-second units, 2..62 s (p49). Re-advertisement is the Advertise Entity State Machine, 6.2.4 / Figure 6-2 (p56). The same 6.2.6 attribution already exists at `:1456`, `:3096` and `:3104`, before this PR.
  - (c) `power.state-restored` cites 5.3.5.1, 5.3.7.1, 5.3.8.7, 5.3.11.1 and 5.3.13. It omits 5.3.8.2 (bound state) and 5.3.8.3 (binding parameters), p41, which are the clauses for `stream_binding`, the only item the default inventory persists. It also omits 5.3.7.6, 5.3.8.1, 5.3.9.1 and 5.3.10.1, which the repository's own inventory at `docs/MILAN_V12_ROADMAP.md:399` lists.
  - (d) "No asCapable loss" cites only the interval and timeout tolerances (4.2.6.2.2/.3). The asCapable clause itself, 4.2.6.2.4 (p24), is not cited.
  - Part of this list was copied from the issue's authority paragraph. That does not make it correct against the standards.
- **Impact:**
  - A bench engineer, or a finding filed against a failed assertion, is sent to the wrong normative text.
  - The one persisted item the power gate checks today has no cited authority.
- **Required outcome:**
  - The new clause strings cite the clauses that define the checked behavior: 4.4.4.7 for `tu`, 6.2.2.5 with 6.2.4 for ADP, 5.3.8.2/5.3.8.3 for the binding, and 4.2.6.2.4 for asCapable.
  - The persisted-item authority covers the inventory the plan takes as data.
  - The older 6.2.6 misattributions at `:1456`, `:3096` and `:3104` go to a new Issue, not into this lane.
- **Verification:** grep the release clause strings at the new head and compare them with the cited pages.

### F2 MINOR - Conformance, Robustness, Docs - post-cut time origins and bounds are unrecorded interpretations, and automatic restore is unbounded

- **Where:**
  - `REQUIREMENTS.md:268-271`
  - `docs/testing/TESTING.md:901-908`
  - `tb/tools/torture_campaign.py:3487` (`boot_observation_s=480`, hardcoded and unsourced)
  - `:3495` (`adp_deadline="... after network readiness"`)
  - `:3497` (`rebind_start="CONNECT_RX success"`)
- **Authority/evidence:**
  - The decision (issue comment 5854692245) says every cycle "re-advertises within the ADP valid time, and rebinds within #75's bound".
  - Issue #75 defines its bound from a successful `CONNECT_RX` response to the first valid AVTP PDU, under 1 s. A cold cut has no `CONNECT_RX`.
  - The lane resolved that gap by:
    - verifying automatic restore with no deadline, inside an observation window that is only a lower bound ("Allow at least eight minutes");
    - measuring a separate controller `CONNECT_RX` against the 1 s bound;
    - measuring ADP from an undefined "network readiness" event.
  - None of the 480 s, the ADP origin or the split into automatic restore plus a controller reconnect traces to a recorded decision. TAKEN and REVIEW READY do not flag them as interpretations.
  - AGENTS.md section 2 requires such a gap to be published for a decision rather than resolved in the contract.
- **Impact:**
  - Suppose a persisted binding restores minutes after boot. #75 measured 12 to 97 s restarts in the same MRP-convergence class. That candidate passes every cold cut as long as a later manual `CONNECT_RX` is fast.
  - ADP pass or fail depends on a start event that nobody has defined.
- **Required outcome:** a recorded manager or owner decision that fixes, for each cold cut:
  - the defined start event and upper bound for automatic stream restoration;
  - what "network readiness" means for the ADP deadline;
  - whether the #75 `CONNECT_RX` measurement is additional to that bound;
  - the source of the boot window.

  REQ-VER-06, TESTING 6d and the plan args (as parameters, not literals) must then reflect that decision. If the decision is that automatic restore is intentionally unbounded, the row says so explicitly.
- **Verification:** the power step args carry a named origin and bound. The self-test pins them at a non-default value, and the decision is linked from the issue.

### F3 MINOR - Tests - the audit negative controls are one-sided, and 5 audit mutants survive

- **Where:**
  - `tb/tools/torture_campaign.py:4722` (`test_release_coverage_mutations`)
  - `tests/steps/torture_release_steps.py:72` (`step_tp_release_omission`)
- **Authority/evidence:**
  - Every planted omission targets the same corner: the first repeat group of an area, a DUT `stream_input`, and the return direction.
  - `receipts/mutants.log` shows these audit mutants passing both `--self-test` and the plan feature:
    - A1: the audit checks only the first repeat group.
    - A2: DUT targets only.
    - A3: return direction only.
    - A5: no outbound CRF-binding check.
    - A6: listener targets only.
  - `receipts/audit-probe.log` shows that the reviewed audit correctly rejects six further plan defects, D1 to D6 (a `power.journal_commit` group missing a DUT or peer index or a DUT talker index, a lost outbound direction, a lost outbound or return CRF pair). Each surviving mutant accepts some of them. A1 alone accepts D1, D2, D3 and D6.
  - So half of the audit's behavior is correct today, but no test pins it.
  - AGENTS.md Tests lens: "Each new test can fail for the defect it claims to detect". The claim here is that "each area rejects missing index, direction and CRF".
- **Impact:** a refactor that drops the per-repeat, peer-side, outbound or talker-side checks stays green. A release plan whose journal-commit group skips an index or a direction would then pass its own audit.
- **Required outcome:** the controls plant omissions in every repeat group, on both devices, in both directions and on both the talker and listener sides, including CRF in both directions. Each of mutants A1, A2, A3, A5 and A6 is killed.
- **Verification:** rerun `scripts/mutants.py` against the new head: no audit mutant survives.

### F4 MINOR - Tests - parameter threading and release eligibility are pinned only at default values

- **Where:**
  - `tb/tools/torture_campaign.py:4785` (reduced settings `ReleaseSettings(125, 60, 3, 2, 1, ...)`)
  - `:4807` (CLI test `--soak-interval-s 60`)
  - `:3489-3491` (power `release_eligible`)
- **Authority/evidence:**
  - Assignment item (2) requires interval, duration, count and phase mix as parameters, never hardcoded.
  - `receipts/mutants.log` shows three planner mutants passing every shipped test:
    - P1 hardcodes `interval_s=60`. Every non-default profile still uses 60.
    - P2 hardcodes `total_cycles=200`. No non-default test reads it.
    - P3 reduces power eligibility to `power_cycles >= 200` alone. The reduced profile 3/2/1 is below all three minimums, so dropping two of them changes nothing.
  - The reviewed code is correct today. `receipts/audit-probe.log` shows a non-default interval of 300 and a total of 10 threading through, and a 200-cut 199/1 split correctly reported `release_eligible: false`. Nothing pins any of that.
- **Impact:** a regression that hardcodes the interval or the cycle total, or that marks a 199 idle / 1 commit profile release-eligible, passes both gates.
- **Required outcome:** the self-test and the CLI test use a non-default interval and a non-default total and assert both. The eligibility test includes cases that fail exactly one minimum each (for example 200 split 199/1).
- **Verification:** mutants P1, P2 and P3 are killed.

### S1 SUGGESTION - Robustness - soak eligibility ignores the sampling interval

`tb/tools/torture_campaign.py:3461`. A 604800 s soak with a 604800 s interval, sampled only at baseline and endpoint, reports `release_eligible: true` (`receipts/audit-probe.log`). The decision fixes no interval, so bounding it needs a decision. Cumulative counters and the continuous-evidence list keep the zero-growth criteria measurable in the meantime.

### S2 SUGGESTION - Robustness - an AAF index set that includes the CRF index produces a CRF-into-AAF bind that passes the audit

With `--dut talker_index_set=0|1|4,crf_out=4`, `_release_pairs` binds DUT stream output 4 (CRF) into the peer's AAF sink 4, and `--coverage-by-area` still exits 0 (`receipts/cli-probes.log`). The cause is the older `Device.talker_indices(include_crf=False)` semantics. TESTING 6d tells users to give separate CRF indices, and the bench format policy would refuse the bind, but a refusal at plan time would be cheaper.

### S3 SUGGESTION - Docs/Tests - the #366 negative control named in 6d has no assertion that can fail on it

`docs/testing/TESTING.md:933` proposes "the first-boot defect or disabled persistence" as the item-4 control. No `POWER_ASSERTS` entry observes the boot count or an unexpected restart. A #366 image restarts once during memtest and then boots and restores normally, so it would produce no failed assertion. Before bench item 4, either add such an assertion or name only the disabled-persistence control.

## Clean-lens evidence

[R347] PASS RTL - `git diff --stat ac18b509..b7b74b8b` (7 files: CONTRIBUTING.md, REQUIREMENTS.md, docs/testing/TESTING.md, tb/tools/torture_campaign.py, the plan feature and two step files; nothing under `hdl/`, firmware, `sw/builder`, `tb/verilator` or submodule gitlinks) and `docs/reference/REGISTER_MAP.md:1251` - The diff changes no RTL, firmware or builder file. I checked the one interface contract it references, `AVTPRX_TSD` at `0x6EC` (signed ns, last accepted STREAM_INPUT[0] PDU), and the plan's `timestamp_margin` and the 6d wording agree with it and do not attribute it to other streams. The four submodule gitlinks are unchanged (`receipts/clone-integrity.txt`). The hosted `verilator-lint`, the four Yosys shards and `bdd-conformance` report success at the exact head (`receipts/hosted-check-runs.tsv`).

Conformance, Robustness, Tests and Docs are UNCLEAN (F1 to F4). What I checked clean inside those lenses:
- REQ-VER-06 states 7 continuous days, bidirectional binding with the reference peer, CRF with AAF, periodic counter observation of every declared index, zero SEQ_NUM_MISMATCH and STREAM_INTERRUPTED growth, no unexplained MEDIA_UNLOCKED, no asCapable loss, `tu` bounded by holdover, 200 cold cuts split 160 idle / 40 commit, warm resets excluded, the persisted inventory as data (today `stream_binding`), ADP valid time, #75's `<1 s`, and one DUT plus the reference peer (`REQUIREMENTS.md:250-275`).
- The REQ-VER-05 blocker paragraph references REQ-VER-06 (`:280`).
- `--plan --areas soak,power` emits one soak repeat and two power repeats built from `Device` topology and `ReleaseSettings` (`receipts/plan-json.log`). The emitted content covers:
  - counter targets for every DUT and peer talker and listener index, CRF included;
  - Table 5.4/5.6 counter walks, gPTP publication fields, `AVTPRX_TSD` and uptime;
  - the persisted items as `--persisted-items` data;
  - invalid profiles refused with rc 2 (`receipts/cli-probes.log`);
  - a distinct DUT and peer required.
- Planner mutants P4 to P9 and T1 to T5 (bad eligibility, hardcoded duration or items, missing sum check, inclusive bound, missing endpoint sample, dropped CRF pair or sink, dropped return AAF, AAF bound into a CRF sink, dropped talker targets) are all killed.
- CONTRIBUTING.md section 3 (`:418-428`) and TESTING.md 6d (`:841-935`) name the gate, the parameters and the retained artifacts, and keep bench items 3 and 4 explicitly open. REQUIREMENTS.md, CONTRIBUTING.md, TESTING.md and the PR body claim no hardware result.

## Commands and results (this reviewer, exact head, foreground)

Receipts are in `receipts/`, and `receipts/gate-summary.txt` lists the exact commands.

| Command | Result |
|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | rc 0, 41 tests OK |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | rc 0: 36 scenarios and 172 steps passed, none skipped |
| `python3 -B -m behave tests/features --tags=@torture -f progress` | rc 0: 181 scenarios passed, 172 skipped by tag |
| `python3 -B scripts/check_feature_status.py --self-test` / without it | rc 0, 46/46, 0 findings / rc 0, 0 findings |
| `python3 -B scripts/docs_check.py` | rc 0, 0 findings |
| `python3 -B scripts/check_doc_paths.py` | rc 0, 850 paths |
| `python3 -B scripts/check_doc_style.py` | rc 0 |
| `python3 -B scripts/check_py_idiom.py` | rc 0 |
| `check_em_dash.py --base ac18b509` and `gen_toc.py --check` with the pinned Markdown venv (requirements hash 40cdefe08ebd) | rc 0 and rc 0 (the system interpreter lacks the renderer and gives rc 2, recorded) |
| `git diff ac18b509 HEAD --check` | rc 0 |
| `torture_campaign.py --coverage-by-area --areas soak,power` | rc 0, both areas complete |
| `scripts/mutants.py` (21 mutants, disposable extracted tree) | 13 killed, 8 survived (A1, A2, A3, A5, A6, P1, P2, P3) |
| `scripts/audit_probe.py` | the reviewed audit rejects D1 to D6; the surviving mutants accept them |

After the probes, the clone is byte-identical to the head:
- porcelain empty;
- index listing sha256 `712a69fa...` unchanged;
- `torture_campaign.py` blob `93197119` with sha256 `187db19a...`;
- the four gitlinks unchanged.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | REQUIREMENTS.md:250-281; decisions 5789765788 and 5854692245; issue #75; plan clause strings :3349-3408; Milan v1.2 p23-24, 36-46, 72, 76, 141; IEEE 1722-2016 p37; IEEE 1722.1-2021 p47-49, 56, 58-60 | R347-1 | b7b74b8b20c166cf69f84c2fcbb6162b420cd2d3 |
| RTL | CLEAN | diff stat (no hdl/firmware/builder/gitlink change); REGISTER_MAP.md:1251 against plan timestamp_margin; hosted lint/Yosys at exact head | R347-1 | b7b74b8b20c166cf69f84c2fcbb6162b420cd2d3 |
| Robustness | UNCLEAN (F2) | ReleaseSettings validation and CLI refusal probes; topology probes; post-cut timing contract :3478-3512 and TESTING.md:895-912 | R347-1 | b7b74b8b20c166cf69f84c2fcbb6162b420cd2d3 |
| Tests | UNCLEAN (F3, F4) | _ReleasePlanChecks :4683-4823; torture_release_steps.py; feature :304-339; 21 mutants; audit probe D1-D6 | R347-1 | b7b74b8b20c166cf69f84c2fcbb6162b420cd2d3 |
| Docs | UNCLEAN (F1, F2) | CONTRIBUTING.md:418-428; TESTING.md:841-935; REQUIREMENTS.md section 8; PR body; REVIEW READY; docs gates | R347-1 | b7b74b8b20c166cf69f84c2fcbb6162b420cd2d3 |

## Real limits

- Desk review only. Physical calibration was NOT RUN, and nothing here is hardware proof. The hosted `Physical gPTP` context is skipped, which is not evidence.
- At capture time, the hosted Verilator shards, `elaborate`, `yosys-elaboration` and `docs-check` were still in progress at the exact head (`receipts/hosted-check-runs.tsv`). I record them and do not rely on them.
- I did not run the full parent/PP/gPTP/Yosys/builder banks, Docker/act, or any hardware step, as assigned. The source banks and the manager's static/builder/native evidence are the manager's.
- Standards handling deviated from the assignment. To find page numbers, I first converted the three standards to transient text in the unpublished scratch area. I deleted those conversions immediately. I then extracted and read only the cited pages, plus the pages needed to identify the correct clauses (Milan p38-41, IEEE 1722.1-2021 p49 and p56). No standards text is published.
- The mutants are textual and target only the new release code. Survival shows a gap in the tests, not a defect in the reviewed code, which is correct on every probe.

## Pending manager duties

- Hosted and act acceptance at the exact head, and the final current-dev candidate at the merge turn (source base and live dev both `ac18b509` at review time).
- Recording the decision F2 requires. Filing a new Issue for the older 1722.1-2021 6.2.6 misattributions (F1 part b).
- Re-review of the corrected head by both reviewers. Bench items 3 and 4 stay open under #396.

R347-1 FINISHED
