[R816] POSITIVE - exact head e3f96a67b5dd1b9e4536ca67a6bd1595f4c19d53

# R816-2: external review of #868 / PR #879 (round 3 delta)

- **Head:** `e3f96a67b5dd1b9e4536ca67a6bd1595f4c19d53`, tree `5d6ae046e896cbf295bef85b96ea262283f48951`.
- **Delta:** `bfb2df3707..e3f96a67b5`, six commits (`a3ec9990`, `0e38c2fd`, `267fc981`, `528554c9`, `fbe5acc9`, `e3f96a67`). They answer the round 3 ruling (#868 issuecomment-6788719673, items 1 to 8).
- **Source base:** dev-soft-core `1d6bf555`.
- **Verdict:** POSITIVE.
  - Every round 1 finding is resolved at its cause: R815-1 F1 to F4, R1 and S1; R816-1 F1 to F3, RES-1 and SUG-1.
  - No BLOCKER, MAJOR or MINOR is open.
  - One RESIDUE (wording only) and four SUGGESTIONs are below.

## Scope reconstructed

- **Authority:** AGENTS.md sections 6 and 7, and the issue body.
  - The issue body has five acceptance items: ACMP under Table 5.26; MAAP B.3.4.x and the closed `maap/README.md:47` note; ADP Table 5.50 and AECP 9.2.1; the planted controls; CI inside the 30-minute budget.
  - Out of scope: 32x32 (#859), S2b and S12.
- **The round 3 ruling:**
  - All fixes are harness, grader and docs only.
  - Item 7 (deadline bursts keep the ACMP and AECP records out) is kept as built.
- **Delta scope** (`receipts/delta-scope.log`):
  - Changed: 15 files, all under `.github/`, `docs/testing/`, `scripts/ci_events.py`, `tb/verilator/ctrl_wire_timing/`, `tb/verilator/milan_dp/{Makefile,README.md}`, and `sw/firmware/ctrl/maap/README.md`. The last one is documentation only.
  - Unchanged: no `hdl/`, `sw/mailbox/` (so `mailbox.yaml` too), protocol-processor, gptp-processor or third_party path; no `.sv`, `.c` or `.h` file; no gitlink.
  - The Makefile change is one added `print-split-srcs` target (`tb/verilator/milan_dp/Makefile:1096`). `build-split` is untouched.
  - No harness code, Makefile or source changed between the measurement head `267fc9815d` and this head. Later commits touch CI, docs and READMEs only.

## Evidence used

- **The author's round 3 packet:** `review-evidence/665s8-r1/author-r3`, archive `a11b85564b`.
  - Verified: all 1,545 `MANIFEST.json` entries match their `published_sha256`, with no unlisted file. That includes all 651 `author-r3` entries (`receipts/evidence-manifest-verify.log`).
  - Spot-checked:
    - `head/ci-head.console`: the CI step's result is `PASS`, 49 controls, 0 failed, both runs 0 findings, both plants caught, wall 693 s, rc 0.
    - `stimulus-at-head.txt`: the gate pass's eight logs are sha-identical to the measurement.
    - `diff-since-measurement.txt`, which I confirmed independently.
- **Probes I ran myself, at the head:** all in `receipts/`, with the scripts in `scripts/`. The two round 1 reviewers' scripts were copied unchanged and match their published manifests by sha256.
- **Hosted runs:** inspected read-only, for context only. They are not source evidence, and I make no claim about a manager source bank.

## Prior findings, resolved or retained at this head

| Prior finding | Required outcome / verification | At `e3f96a67` | Evidence |
|---|---|---|---|
| R816-1 F1 / R815-1 F3: PROBE_TX pairing | Each bind pairs with its own PROBE_TX (after its response, before the next bind); the PROBE_TX count equals the draws; a non-SUCCESS BIND_RX_RESPONSE is a finding; self-test controls; R1, R2 and R4 found; R0 passes | **Resolved** | `wire_grade.py:472` (own window), `:474`, `:501` (count), `:467` (status). `receipts/r816-1-grader-probes.log`: R0 is 0 findings and identical to the published results for ci-1x1-none and 8x8-none; R1 gives 2 findings by their own words; R2 gives 16; R3 gives 18; R4 gives 1 (`status 1, not SUCCESS`); R5 gives 1. `receipts/r815-1-missing-probe-tx-*.log`: all three mutants `caught`. Controls `bind-without-its-probe-tx`, `probe-tx-transactions-not-the-draws` and `bind-refused` pass. |
| R815-1 F3: no advertise period at `announces > 1` | Finding plus control; the no-advertise probe found | **Resolved** | `wire_grade.py:623`, plus the stopped-advertising check `:625-626`. `receipts/r815-1-no-advertise.log`: the control gives 0 findings; the mutant gives 2 (`no sample in a run to its second ANNOUNCE`, `stopped advertising`). |
| R816-1 F2: GET_AVB_INFO was GET_AS_PATH on AVB_INTERFACE 9 | 0x0027 on AVB_INTERFACE 0 at 7.4.40 length; a non-SUCCESS AEM/MVU status is a finding; rows re-measured; slowest AEM restated | **Resolved** | `wire_scenario.py:111` sends `0x0027`, `be(9,2)+be(0,2)`; `wire_grade.py:528` checks status. `receipts/r816-1-aecp-status-1x1.log`: `('0x0027', (9, 0), 0) 3`. `receipts/r816-1-status-census.log`: every ACMP and AECP status is 0 in both unloaded head logs, and the campaign's census is all 0 too. 8x8-composed `aecp.response` max is 24.5044 ms = `aecp.response.get_avb_info` max, margin 215.4956; this matches README, PR body and REVIEW READY. Campaign GET_AVB_INFO is 1.3527 to 6.6371 ms, matching the PR's "1.35 to 6.64". Controls `aem-refused` and `mvu-refused` pass. |
| R815-1 F1: MAAP echo lost after the first ANNOUNCE | Echo found whenever an ANNOUNCE has been sent; units 2 and 3 re-measured; after-unrelated-traffic control | **Resolved** | `wire_main.cpp:489-492`: each echo keeps its newest match. `wire_main.cpp:531`: loads must be defined before the first frame. `wire_grade.py:667`: a skip after the ANNOUNCE is a finding on every run. Campaign `echoes.txt` (units at `267fc9815d`, code-identical to the head): 4,641 echoes found after the ANNOUNCE, 0 skipped, 1,650 DEFENDs sent. The 231 skipped (112+14+105, matching each loaded unit's `skipped`) were all queued before it. Controls `clean-loaded` (70 unrelated frames, then the echo found) and `echo-skipped-after-the-announce` pass. See SUG-A. |
| R815-1 F2: armed vs delivered load | Queued / delivered / expiries met reported apart; delivered + 4 a draw = `rx_frames` + `bench_rx` on every loaded run | **Resolved** | `wire_grade.py:642-675`. `receipts/frame-equation.log`, recomputed by my script from every published `results.json`: 8 of 8 runs hold (1,887 + 64 = 1,951 for both loaded 16-draw runs; 42,122 + 1,368 = 43,490 for units 2 and 3; 64 and 1,368 unloaded). README and PR tables label the three counts. Control `received-frame-unaccounted` passes. |
| R816-1 F3 / R815-1 F4: reuse guard | Record the split recipe, datapath / KL_mbx / split-top sources, Makefile, firmware and tsn-c-stack; both probes report every edit refused | **Resolved** | `wire_build.py:131` (`print-split-srcs` list), `:153` (dependency files), `:86` (TOOLS, Makefile), `:83` (FIRMWARE_TREES), `:267`. In a disposable head clone, `receipts/r816-1-reuse-probe.log` refuses all 6 edits (unchanged: accepted), and `receipts/r815-1-reuse-stale.log` refuses all 6 edits; the tree is restored. |
| R816-1 RES-1 / R815-1 R1 | `wire_scenario.py:18` becomes `THE LOAD (#868):` | **Resolved** | `wire_scenario.py:18`. |
| R816-1 SUG-1 (taken by the ruling) | Strict 9 s margin beside the 9,400 ms bound; widened bound in the clause text | **Resolved** | `wire_grade.py:133`, the `strict_ms` row, and the clause text "graded inside 4998 to 9400 ms". Campaign: 612.6435 ms to the strict 9,000 ms, 1,012.6435 ms to 9,400 ms. |
| R815-1 S1: exit 2 on refused paths | Optional | **Taken** | `run.py:191` `refusing()` wraps the `--point`, `--campaign` and `--regrade` paths. |
| R816-1 SUG-2: hosted wall time in `CI_WORKFLOWS.md` | Optional | **Still open** (carried as SUG-C) | The hosted `wire-timing` job at this head was cancelled before its step (see the limits). |

## Independent checks beyond the prior probes

- **The reuse guard on a real build** (`receipts/real-dep-probe.log`, `scripts/real_dep_probe.py`):
  - **Setup:** I built the split top with milan_dp's own `build-split` (pinned Verilator 5.050, identity checked; 33 s) in the disposable clone.
  - **The `.d` path:** `read_by_tools()` reads 155 files from the real dependency files. These include two `include`d headers that `print-split-srcs` does not list: `hdl/common/eth_event_counter/ethernet_events.svh` and `configs/generated/<shape>/gen/adp_shape_defaults.svh`. Editing either one is refused, and restoring it is accepted again. So the dependency-file path, which no self-test exercises, works on Verilator's real `__ver.d` format.
- **A suspected hole that did not hold:**
  - The split top's PP and gPTP modules `$readmemh` `ltn_rom.hex`, `ucode.hex` and `gptp_ucode.hex` by relative name. The guard does not record these files.
  - But the generated split model contains no `$readmem` call, so it reads none of them when it runs. The CPU half's `.init` files are recorded through `soc/gateware/*.init`.
  - The published logs carry no `$readmem file not found` warning. So "every input the model ... reads when it runs" holds for the ROM images.
- **Grader mutants** (`receipts/grader-mutants.log`, `scripts/grader_mutants.py`, run in the disposable clone):
  - Nine one-line mutants of the new checks, all killed by the self-test: the pairing reverted, the count dropped, the BIND status ignored, the AEM status ignored, the missing period accepted, the stopped-advertising check dropped, the frame equation dropped, the skip-after-ANNOUNCE check dropped, and delivered counted as queued.
  - The source was restored byte-exact after the run.
- **Self-test at head** (`receipts/selftest-head.log`): 49 controls, 0 failed. At `bfb2df37` there were 33, so 16 are new: 9 grader controls, 6 reuse controls and 1 clean log.
- **CI contract** (`receipts/ci-events-check.log`, `receipts/ci-gate-workflows-check.log`):
  - `scripts/ci_events.py --check` passes (2,440 contract items).
  - `scripts/ci_gate_workflows.py --check` gives rc 0, so the generated `rtl-fast.yml` matches its template.
  - The new install step pins three `pythondata` packages by commit and is mirrored in `ci_events.py:2658`.
- **Comment rule over the added source lines** (`receipts/comment-rule-scan.log`): no lane label, round, reviewer ID or comment ID. The five pattern hits are hex constants and `round()`.
- **Figures restated in the README, the MAAP note and the PR body**, recomputed from the published `results.json`:
  - ACMP: the worst is 18.2768 ms (`acmp.bind_rx`, 8x8 loaded), margin 181.7232.
  - MAAP: egress 0.302 to 2.4722 ms over 16 + 20 = 36 timer-driven frames; interval error at most 1.819 ms; probe intervals 513.086 to 583.689 ms; announce intervals 31,956.50 to 31,958.38 ms.
  - ADP: egress at most 2.637 ms.
  - The live PR body is byte-identical to the packet's `PR-BODY.md`, apart from a trailing newline.

## Findings

### RES-1: RESIDUE (Docs; wording only): the reuse paragraph says a build is reused "only at the tree it was built from"

- **Where:** `tb/verilator/ctrl_wire_timing/README.md:46`
- **Evidence:** `wire_build.reused()` (`wire_build.py:267-278`) refuses a reuse when a *recorded* input changes. A change elsewhere in the tree leaves the build reusable, and correctly so. Examples: the grader, the stimulus generator `wire_scenario.py`, or documentation outside the firmware trees. The sentence states more than the guard does. No measurement, figure, test or code depends on it.
- **Exact fix:** replace `So a build is reused only at the tree it was built from.` with `So a build is reused only while every recorded input is unchanged; a change outside the record (the grader, the stimulus, documentation outside the firmware trees) leaves it reusable.`

### SUG-A: SUGGESTION (Tests): the model's echo fix is guarded only in campaign units

- **Where:** `tb/verilator/ctrl_wire_timing/wire_main.cpp:489-492` and `wire_grade.py:667`.
- **What:** the self-test's `clean-loaded` and `echo-skipped-after-the-announce` controls are grader controls on synthetic logs. The CI step's 16-draw runs end before the first ANNOUNCE. So a regression of `wire_main.cpp`'s echo store would be found only by a campaign unit's skip-after-ANNOUNCE check, not in CI.
- **Why this is not a finding:** the campaign is the measurement of record, and it shows the property on the real model (4,641 found, 1,650 DEFENDs).
- **Optional:** a short model-level check would catch such a regression in CI. For example, a scripted ANNOUNCE-matching frame, then more than 64 unrelated frames, then one echo offer.

### SUG-B: SUGGESTION (Robustness): a censored final bind still trips the PROBE_TX count

- **Where:** `wire_grade.py:464`, `:474` and `:501`.
- **What:** a last bind that the log ends within 200 ms of is censored, but `len(probe.cycles) != draws` still reports it as a finding. That contradicts the docstring's censoring rule.
- **Why this is not a finding:** it cannot occur in the harness's runs, because `TAIL_MS` waits out every bound. It also errs toward a finding, not toward a pass.
- **Optional:** exclude censored binds from the expected count.

### SUG-C: SUGGESTION (Docs; carried from R816-1 SUG-2): record the hosted wall time

- **Where:** `docs/testing/CI_WORKFLOWS.md:477`.
- **What:** the page quotes the local 693 s replica. Once a hosted `wire-timing` run executes its step, record that run's wall time beside it.

### SUG-D: SUGGESTION (Tests): the reuse self-test controls never touch a file

- **Where:** `wire_selftest.py` `REUSE_CONTROLS`.
- **What:** these controls alter a recorded digest rather than edit a file, and run with no dependency files. So `read_by_tools()` and `split_sources()` are exercised only by reviewer probes.
- **Optional:** a control that edits a temporary copy of a listed file, or reads a small synthetic `__ver.d`, would keep that path under test.

## What was checked, by lens

| Lens | Result | Artifact (at `e3f96a67`) | What was checked, against what |
|---|---|---|---|
| Conformance | PASS | `wire_scenario.py:107-114`, `wire_grade.py:442-505, 507-535, 583-628`; `author-r3/receipts/head/*__results.json`, `campaign/unit*-results.json`, `campaign/status-census.log` | Every acceptance item against the clauses at the restated figures, as recomputed above. GET_AVB_INFO 0x0027 against IEEE 1722.1-2021 7.4.40.1 (descriptor_type and descriptor_index, 4 bytes) and against 0x0028 GET_AS_PATH. SUCCESS = 0 against Table 7-170 and Table 8-3. MAAP ANNOUNCE detection `data[12:15]==22f0fe`, message_type 3, against IEEE 1722-2016 Table B.4. Table 5.50's strict 9 s margin is published beside the widened bound. Ruling items 1 to 6 and 8 are met; item 7 is unchanged, as ruled. |
| RTL | PASS | `receipts/delta-scope.log`; `tb/verilator/milan_dp/Makefile:1084-1098`; `wire_main.cpp:415-470` (TX/RX boundary taps); `receipts/real-dep-probe.log` (real split build) | No RTL, mailbox contract or gitlink changed. The only recipe change is a print target, and `build-split` is byte-unchanged. The model's boundary sampling is unchanged; only the echo store and the LOAD print changed. The split build at the head elaborates at Verilator 5.050 and contains no runtime `$readmem`. The prior RTL lens verdict carries for code the delta does not touch. |
| Robustness | PASS | `wire_grade.py:268-275` (LOAD refusal), `:285-291` (SUMMARY refusal), `:623-628`, `:642-675`; `wire_main.cpp:529-532`; `run.py:191-198`; `wire_build.py:131-164, 267-278`; `receipts/r815-1-reuse-stale.log`, `receipts/r816-1-reuse-probe.log`, `receipts/real-dep-probe.log` | Malformed LOAD or SUMMARY lines are refused, with exit 2 on every path. A defload after the first frame, or defined twice, throws. Partial and over-delivered offers are counted or found. A cancelled arm is delivered but meets no expiry. An unreadable recipe list is refused, and a missing file is recorded as `missing`. Every reuse edit is refused, including `include`d headers on a real build. SUG-B is optional. |
| Tests | PASS | `wire_selftest.py` (49 controls); `receipts/selftest-head.log`, `receipts/grader-mutants.log`, `receipts/r816-1-grader-probes.log`, `receipts/r815-1-*.log`, `receipts/frame-equation.log` | Each new check has a control that fails when it is removed: 9 of 9 mutants killed. Round 1 probes R0 to R5 and both R815 probes are found by their own words on real head logs. R0 regrades are identical to the published results. SUG-A and SUG-D are optional. |
| Docs | PASS (RES-1 recorded) | `tb/verilator/ctrl_wire_timing/README.md` (delta), `sw/firmware/ctrl/maap/README.md:48-50`, `tb/verilator/milan_dp/README.md`, `docs/testing/CI_WORKFLOWS.md:465-485`, `wire_grade.py` docstring, live PR body; `receipts/comment-rule-scan.log` | Every restated figure recomputes from the published results. The tables state queued, delivered and met. GET_AVB_INFO is relabelled and re-measured. No residue under the comment rule in the added source lines. The issue body quotes no GET_AVB_INFO figure. RES-1 is wording only. |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | scenario AECP rows, grader ACMP / AECP / ADP / MAAP checks, head and campaign `results.json`, status censuses | R816-2 | `e3f96a67b5dd1b9e4536ca67a6bd1595f4c19d53` |
| RTL | CLEAN | delta scope (no RTL, mailbox contract or gitlink), `milan_dp/Makefile` print target, model boundary taps, real split build at head | R816-2 | `e3f96a67b5dd1b9e4536ca67a6bd1595f4c19d53` |
| Robustness | CLEAN | grader refusals and load accounting, model defload guards, `run.py` refusal path, reuse guard on synthetic and real builds | R816-2 | `e3f96a67b5dd1b9e4536ca67a6bd1595f4c19d53` |
| Tests | CLEAN | 49-control self-test, 9 grader mutants, round 1 probes rerun unchanged, frame equation on 8 published runs | R816-2 | `e3f96a67b5dd1b9e4536ca67a6bd1595f4c19d53` |
| Docs | CLEAN (RES-1 to the residue checklist) | harness README, MAAP note, milan_dp README, CI_WORKFLOWS, grader docstring, PR body, comment-rule scan | R816-2 | `e3f96a67b5dd1b9e4536ca67a6bd1595f4c19d53` |

## Real limits

- **No gate bank of my own.** I ran no full parent, PP, gPTP, Yosys or builder bank, no wire-timing run and no campaign unit.
  - The source-head execution evidence is the author's published clean-clone gate pass and campaign, which I verified by hash and spot-checked.
  - The campaign ran at `267fc9815d`. That commit is code-identical to the head for the harness, model, recipe and sources.
  - The head's runs are sha-identical to it, by the author's `stimulus-at-head.txt`.
- **Large logs were not checked.** The loaded runs' and campaign units' `wire.log` files (over 200 KB) are not published, only their sha256. My frame-equation and echo checks read the published `results.json` and `echoes.txt`, not those logs.
- **Hosted runs at this head** (`receipts/hosted-checks-at-head.log`) do not carry the CI step:
  - `docs-gates-0` and `docs-gates-1` failed at "Install diagram gate dependencies" (exit 100). The delta does not touch that step.
  - Fail-fast then cancelled the rest. The `wire-timing` job's new install step (15) succeeded on the hosted runner, and the job was cancelled at "Build Verilator from source on cache miss".
  - So no hosted wire-timing wall time exists at this head (acceptance item 5's hosted figure). Hosted and act acceptance are the manager's.
- **No hardware proof.** Physical calibration was not run, and field skips are not hardware proof.
- **Probe setup.** The reuse probes and mutants ran in a disposable clone of the head. The real-dependency probe used one split build at 1x1/1if. The 2-interface variant's generated `KL_mbx` package is covered by `print-split-srcs` (the `build:` key) and by `sw/mailbox` in the firmware trees.

## Pending manager duties

- Carry RES-1 to the residue checklist.
- Hosted acceptance at the exact head: a hosted `wire-timing` run that executes its step, its wall time against the 30-minute budget, and a rerun of the runner-side `docs-gates` dependency failure.
- Build and validate the current-dev merge candidate (source base dev-soft-core `1d6bf555`; live dev `fa6c094b8e196666a8a8865788d5e83b5bbaea09`; dev-soft-core has moved to `764482b45f`, as the author notes). Then post-merge containment.
- The CPU budget harness's GET_AVB_INFO row (`tb/verilator/ctrl_service_budget/scenario.py:464`, still 0x0028) needs its own Issue, per ruling item 2.
- Any manager or issue comment that quotes round 2's 20.6 ms "GET_AVB_INFO" figure is the manager's to correct.

## Clone state after probes

- The review clone is at `e3f96a67b5dd1b9e4536ca67a6bd1595f4c19d53`, tree `5d6ae046e8`.
- `git status --porcelain --untracked-files=all` is empty, and the worktree and index match HEAD.
- Index modes, blobs and paths are identical to the HEAD tree.
- The gitlinks are unchanged: `gptp-processor 135afd04`, `protocol-processor a9e84b66`, `third_party/lwSRP 08ee86e8`, `third_party/tsn-c-stack 70936b77`, `third_party/verilog-axis 48ff7a7e`, and `external efeb541a`, which is not initialised (`receipts/clone-state.log`).
- The only clone-side effect was one object fetch of the public evidence commit, into FETCH_HEAD; no ref was changed.
- Every probe edit ran in the disposable clone under `scratch/` and was restored.

R816-2 FINISHED
