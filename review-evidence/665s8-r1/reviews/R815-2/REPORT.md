[R815] NEGATIVE - exact head e3f96a67b5dd1b9e4536ca67a6bd1595f4c19d53

# R815-2: internal independent review of PR #879 (issue #868, S8 wire timing), delta `bfb2df37..e3f96a67`

Head `e3f96a67b5dd1b9e4536ca67a6bd1595f4c19d53`, tree `5d6ae046e896cbf295bef85b96ea262283f48951`. Base `dev-soft-core`, merge base `1d6bf555`. The live `dev-soft-core` is now `764482b45f`, and the lane has not been rebased onto it.

**Verdict: NEGATIVE.** One MINOR finding (F1, Tests) is open. Every round-1 finding is resolved at this head (R815-1 F1-F4, R1, S1; R816-1 F1-F3, RES-1, SUG-1), each checked against its Required outcome and Verification line. The prior probes were rerun unchanged and every one now reports the defect it was written for. Four lenses are CLEAN and Tests is UNCLEAN. There is also one RESIDUE and two SUGGESTIONs.

## Scope as reconstructed

- **Contract.**
  - #868 acceptance 1-5 and the round 2 ruling (issuecomment-6755260058).
  - The round 3 ruling (issuecomment-6788719673), items 1-8. Items 1-6 are the fixes. Item 7 keeps the deadline-burst exclusion. Item 8 sets the gates.
- **Delta.** Six commits by the round 3 executor (`a3ec9990`, `0e38c2fd`, `267fc981`, `528554c9`, `fbe5acc9`, `e3f96a67`) across 15 files: harness, grader, self-test, CI template, generated workflow, `ci_events.py`, and docs.
  - `receipts/delta-scope.txt`: no path under `hdl/` or `rtl/`, no `.sv`, no `mailbox.yaml`, no firmware source (only `sw/firmware/ctrl/maap/README.md`), and no submodule gitlink change.
  - `tb/verilator/milan_dp/Makefile` gains only the phony `print-split-srcs` target.
  - `tb_split_top.sv` is unchanged in the delta.
- **Measurement head.** The runs and the campaign were measured at `267fc9815d`. From there to the head only the CI files and docs change, and the model, build, stimulus and grader are byte-identical (`receipts/delta-scope.txt`). The author's clean-clone gate pass at `e3f96a67` reproduced the CI step and the 8x8 runs byte-identical (`gates/wire-timing-ci-vs-head.txt`, `gates/wire-8x8-vs-head.txt`).

## What this review executed (receipts in this packet)

| Receipt | What | Result |
|---|---|---|
| `receipts/evidence-manifest-verify.txt` | the packet archive `a11b8556` `review-evidence/665s8-r1/MANIFEST.json`, every entry re-hashed | 1,545 entries, 0 mismatched (651 under author-r3). The archive commit is **unsigned**, so integrity rests on the hash manifest. |
| `receipts/selftest-head.log` | `run.py --self-test` at the head | rc 0, `49 controls, 0 failed` |
| `receipts/regrade_probes.log` (`scripts/regrade_probes.py`) | the published `ci-1x1-none` and `8x8-none` `wire.log`, regraded with the head's grader, plus a census and six mutations | see below |
| `receipts/delta_mutants.log` (`scripts/delta_mutants.py`) | 14 in-place mutants of the round's new grader and reuse-guard checks, each restored | 11 killed, 3 survived (F1) |
| `receipts/prior-probes/*` | the round-1 reviewers' probe scripts, rerun **unchanged**. Their sha256 match both review manifests and the author's `reviewer-scripts.sha256`. | every one found or refused by its own words, as listed below |
| `receipts/reuse_probe_extra.log` (`scripts/reuse_probe_extra.py`) | real edits of further source kinds, at both points' recipe variables (`split_vars`, `shape`), in a disposable clone | unchanged accepted; 8 of 8 edits refused at each point |
| `receipts/ci_events-check.log`, `receipts/ci_gate_workflows-check.log` | `ci_events.py --check` and `ci_gate_workflows.py --check` at the head | rc 0, `ci_events: OK (2440 contract item(s) …)` |
| `receipts/hosted-state.txt` | the hosted runs at the head, observed during this review | all four workflows `cancelled`. In `wire-timing`, the new pip step ran **success** and the job was cancelled in "Build Verilator from source on cache miss", so the timing step **did not run** |
| `receipts/clone-integrity.txt` | the review clone after the probes | HEAD, tree and index tree are `5d6ae046…`. 0 worktree/index differences in bytes or modes, 0 untracked, ls-files equals ls-tree, submodule gitlinks at their recorded commits |

`scripts/regrade_probes.py` results on both published unloaded logs:

- **P0.** 0 findings. Rows and load are identical to the published `results.json`.
- **P1.** Every `aecp-get_avb_info` command is `command_type 0x0027`, descriptor_type 9, descriptor_index 0, control_data_length 16 (IEEE 1722.1-2021 7.4.40.1: two 16-bit fields after the 12-octet AEM command header). Every ACMP frame the entity sends (types 0, 7, 9) and every AEM/MVU response (types 1, 7) carries status 0.
- **P2.** Each of these mutations is found by its own words:
  - a BIND_RX_RESPONSE with status 1;
  - an AEM response with status 2;
  - an MVU response with status 1;
  - `SUMMARY rx_frames` changed, which breaks the frame equation;
  - bind 5 moved between bind 4's response and its PROBE_TX, so the pairing window catches bind 4;
  - draws + 1, which trips the PROBE_TX count.

## Findings

### F1 MINOR - Tests - the load accounting's new distinguishing counts have no control that can fail

- **Location.**
  - `tb/verilator/ctrl_wire_timing/wire_selftest.py:241-275` (`loaded()`, `LOADED`);
  - `tb/verilator/ctrl_wire_timing/wire_grade.py:659` (`partial_offers`), `:660-662` (over-delivery finding) and `:665` (`expiries_met`).
  - Related claims: `tb/verilator/ctrl_wire_timing/README.md:165-167`, `:272`, `:294-295`.
- **Authority and evidence.** Ruling item 4 (from R815-1 F2) requires the load to be reported with delivered bursts separated from armed triggers and from expiries met. R815-1 F2's evidence named the case that motivates the third count: "the cancelled probe arm's burst is delivered but meets no expiry". README:167 states that behaviour, and README:272 publishes it for the campaign: 5 MAAP bursts delivered, 4 meeting an expiry. AGENTS.md section 6, Tests: each new test can fail for the defect it claims to detect. The `LOADED` comment says the clean loaded log checks "queued, delivered and met kept apart".

  `receipts/delta_mutants.log`. Each of these mutants leaves the self-test at `49 controls, 0 failed`:
  - `expiry-met-ignores-arm`: `expiries_met += whole`, which drops the arm-expired condition, so a cancelled arm counts as met;
  - `partial-offers-never-counted`: `partial_offers += 0`;
  - `over-delivery-check-gone`: the `got > offer.frames` finding removed.

  The synthetic loaded log has no arm cancelled or superseded before its deadline, no offer delivered in part (its `untagged` variant is graded only for the frame-equation words), and no over-delivered offer. So in the fixture, met always equals delivered-whole and partial is always 0. No published run has a partial offer either.

  The code itself is correct by reading:
  - `offer.at` is the TMR arm's cycle (`wire_main.cpp:318-324`), which is the first element of `expiries()`;
  - `expiries()` drops an arm that a later write precedes;
  - the published 16-draw and campaign counts agree with the arm and cancel sequence the README describes.

  So no published figure is shown wrong.
- **Impact.** A regression that counts a cancelled or superseded arm's burst as meeting its expiry would pass every control. So would one that drops the partial count or the over-delivery finding. That is exactly the over-count R815-1 F2 was raised for, and it would inflate a published "expiries met" figure with nothing to catch it, because only the frame equation is checked on real runs.
- **Required outcome.** A self-test control, either the clean loaded log extended or a new one, has:
  - a timer-triggered offer whose arm a later write cancels or supersedes before its deadline, delivered whole and reported as not met;
  - an offer delivered in part, reported in `partial_offers`.

  `LOADED`, or the control's words, expects those counts. Optionally, add a control that is found by the over-delivery words.
- **Verification.** Rerun `scripts/delta_mutants.py` on the fixed head: `expiry-met-ignores-arm` and `partial-offers-never-counted` are KILLED (and `over-delivery-check-gone` too, if that option is taken), and the other 11 mutants stay KILLED.

### R1 RESIDUE - PR #879 body, line 79 (the "Results at the head" bullets) - a figure attributed to the head that was measured at `267fc9815d`

- **Text.** "The CI step at the head on four CPUs of a shared host: `PASS`, 693 s (build 85 s, then both runs at once, 608 s each)."
- **Why it is residue.** The 693 s run is `head/ci-head.console`, at `267fc9815d`, whose model, build, stimulus and grader the head keeps byte-identical. The CI step at the head itself is the gate pass's 2,505 s run, which the same PR body cites in its gate table. No figure, measurement or verdict changes; only the commit the sentence names is wrong.
- **Exact fix.** "The CI step at `267fc9815d` (the head keeps its harness, build and stimulus) on four CPUs of a shared host: `PASS`, 693 s (build 85 s, then both runs at once, 608 s each)."

### S1 SUGGESTION - Docs - `docs/testing/CI_WORKFLOWS.md:465-481` - give the cold figure beside the cached one

- The page quotes the cached-netlist replica: 693 s, build 85 s.
- The closest local analogue of a first hosted run is the fresh-runner replica at `fbe5acc983`: 1,299 s for the step, its build 323 s with the CPU netlist generated cold (`replica/replica.log`).
- The hosted job at the head was cancelled while building Verilator in-job on a cache miss (`receipts/hosted-state.txt`). The Verilator cache key includes `hashFiles('.github/workflows/*.yml')`, so every workflow-changing head starts with that build inside the 30-minute budget.
- Stating the cold figure and that cache behaviour, and the first hosted wall time once one exists (R816-1 SUG-2, still open because no hosted run has executed the step), would let a reader judge item 5 from the page.

### S2 SUGGESTION - RTL/Robustness hygiene - `tb/verilator/ctrl_wire_timing/wire_grade.py:488` - a local shadows the `window` parameter

- In `acmp()`, `window = [at for at in slot_arms …]` rebinds the `window: Window` parameter.
- This predates the delta (it was `:413` at `bfb2df37`) and is harmless today, because the `Window` is used only above it.
- The round added a second `window.unanswered` call (the missing-PROBE_TX case). Any later use below the probe loop would silently get a list. Renaming the local (for example `in_window`) removes the trap.

## Prior public review findings at this head

Each was read only after the independent pass over the diff. It is resolved here against its own Required outcome and Verification line.

| Finding | Required outcome / Verification | At `e3f96a67` | Status |
|---|---|---|---|
| R815-1 F1 (MAAP echo) | the echo finds interface 0's last ANNOUNCE whenever one has been sent; units 2 and 3 re-measured; a control shows the echo found after unrelated traffic fills the history | `wire_main.cpp:488-494`: each echo keeps its own newest match, and the 64-frame whole-traffic history is gone. `define_load` refuses a load defined after the first frame, so no match is missed. The grader finds any echo skipped after its interface's first ANNOUNCE (`wire_grade.py:666-669`; the `TXW`/`TXB` order matches the model's `history()` call order, `wire_main.cpp:424-431`, `:463-465`). Units 2 and 3 were re-measured at `267fc9815d`: in each, the 231 skipped were all queued before the first ANNOUNCE (`campaign/unit2/3-results.json`: 112 + 105 + 14), and 4,641 were found after it beside 1,650 DEFENDs on the MAAP channel (`campaign/echoes.txt`). Controls `clean-loaded` (70 unrelated frames after the ANNOUNCE) and `echo-skipped-after-the-announce`; mutant `skip-after-announce-gone` is KILLED. The control is at grader level; the model's behaviour is shown on the real campaign logs. | Resolved |
| R815-1 F2 (delivered load) | delivered apart from armed and met; delivered + 4/draw = `rx_frames` + `bench_rx` on every loaded run | Three counts, per offer tag `load-<name>-<n>` (`wire_grade.py:642-675`). The equation is checked on every run, and holds on all 8 published results: 1,887 + 64 = 1,951 (1x1 composed: 1,951 + 0; 8x8 composed: 1,104 + 847); 42,122 + 1,368 = 43,490 per loaded campaign unit; 64 and 1,368 unloaded. Mutating `rx_frames` is found (P2). | Resolved; the new counts' controls are F1 |
| R815-1 F3 (PROBE_TX, advertise) | both of R815's probes found by their own words | `probe_missing_probe_tx.py` 1x1 k0, 1x1 k3, 8x8 k3: each `caught`, with "caused no PROBE_TX after its response and before the next bind" and "15 PROBE_TX transactions graded". The mutant no longer pairs with the next draw (`bind_to_probe_tx` max 1.16 / 1.93 ms). `probe_no_advertise.py`: "no sample in a run to its second ANNOUNCE" plus "stopped advertising"; its control stays at 0 findings. | Resolved |
| R815-1 F4 (reuse guard) | the probe's five changes refused | `probe_reuse_stale.py`: 6 of 6 refused. `milan_dp/Makefile` is refused only because the probe's `// probe` line breaks make (the source list cannot be read). A valid `# probe` comment is refused by the Makefile's own digest (`reuse_probe_extra.log`, both points; and the author's `makefile-comment-probe.log`). | Resolved |
| R815-1 R1 (residue) | `wire_scenario.py:18` | `THE LOAD (#868):` | Resolved |
| R815-1 S1 | refusal exit 2 on every path | `run.py:175-198` `refusing()` wraps the run, campaign and regrade paths | Taken |
| R816-1 F1 | R1, R2, R4 found; R0 passes; self-test controls | `grader_probes.py`: R0 0 findings and identical results (1x1 and 8x8); R1 2 findings; R2 16; R3 18; R4 "carries status 1, not SUCCESS"; R5 found. Controls `bind-without-its-probe-tx`, `probe-tx-transactions-not-the-draws`, `bind-refused`; their mutants are KILLED. | Resolved |
| R816-1 F2 (GET_AVB_INFO) | 0x0027 on AVB_INTERFACE 0 with its 7.4.40 length; non-SUCCESS a finding; rows re-measured and text corrected | `wire_scenario.py:111`; the census P1 and R816's `status_census` semantics (all status 0). `aecp()` refuses a command with no stated status and finds any other status. Controls `aem-refused`, `mvu-refused`; their mutant is KILLED. Rows re-measured: slowest AEM 24.504 ms, the 8x8 composed GET_AVB_INFO (`head/8x8-composed__results.json`); campaign 7.251 ms. README:103-104, :182, :208 and PR line 76 are corrected. The issue body carries no AEM figure. The CPU budget harness's row is out of lane (ruling item 2). | Resolved (out-of-lane Issue pending, below) |
| R816-1 F3 (reuse guard) | `reuse_probe.py` reports every edit refused | unchanged accepted; `wire_main.cpp`, `tb_split_top.sv`, `KL_mbx.sv`, `milan_datapath.sv` refused by name; `tsn-c-stack/src/maap.c` and `maap_mbx.c` refused by `tree:firmware` | Resolved |
| R816-1 RES-1 | `(#868)` | as above | Resolved |
| R816-1 SUG-1 | margin to the strict 9 s beside 9,400 ms; widened bound in the clause | `Path_.strict_ms`. Clause text "graded inside 4998 to 9400 ms". README:144, :269: 612.6 ms to 9,000 ms and 1,012.6 ms to 9,400 ms, matching `campaign/summary.txt` (`strict margin 612.6435`). | Taken |
| R816-1 SUG-2 | hosted wall time in `CI_WORKFLOWS.md` | no hosted run has executed the step (`receipts/hosted-state.txt`) | Open as S1 (optional) |

## Per-lens results (each applied to the delta at `e3f96a67`)

```text
[R815] PASS Conformance — wire_scenario.py:98-119, wire_grade.py:459-478,525-531,614-628, receipts/regrade_probes.log P1, campaign/summary.txt, head/*__results.json — GET_AVB_INFO is 0x0027 with descriptor_type 9 / index 0 and control_data_length 16 per IEEE 1722.1-2021 7.4.40.1; the status field is byte 16 bits 7:3 for ACMP and AECP, SUCCESS 0 (Tables 8-3, 7-170); a bind's PROBE_TX is taken only after its own BIND_RX_RESPONSE and before the next bind (Milan v1.2 5.5.2.3 flow); the advertise period is graded 4,998-9,400 ms with the strict 9 s margin published (Table 5.50); acceptance 1-4 figures re-checked against the published results: ACMP max 18.277 ms (181.7 ms margin), AECP max 24.504 ms, probe 513.1-583.7 ms, announce 31,956.5-31,958.4 ms, MAAP egress 0.30-2.47 ms, interval error ≤1.819 ms, advertise 5,362.6-8,387.4 ms; item 5's hosted wall time is pending (manager)
[R815] PASS RTL — receipts/delta-scope.txt, tb/verilator/milan_dp/Makefile:1085-1097, wire_main.cpp:128-140,318-324,488-528 — no RTL, .sv, mailbox.yaml, firmware source or gitlink in the delta; tb_split_top.sv untouched; the Makefile adds only a phony print target that echoes the existing SRCS/SPLIT_SRCS; the testbench's new echo/offer code was read for indexing and widths (skipped_on is std::array<unsigned,n_if> indexed with .at(); offer tags numbered per load in queue order, which the grader's numbering in log order matches; the LOAD line carries sys_ as the queue cycle, equal to the TMR arm's cycle)
[R815] PASS Robustness — wire_build.py:131-162,224-240,266-275, run.py:175-198, wire_grade.py:268-275,285-291, receipts/prior-probes/r815-reuse-stale.log, r816-reuse-probe.log, receipts/reuse_probe_extra.log — the reuse guard refuses an edit of every source kind both rulings name, plus KL_mbx_cdc, verilog-axis' FIFO, lwSRP, mailbox.yaml, the shape's config and the build tools, at both points' variables; an unreadable source list, a build.json with no inputs and a listed file gone are each refused; a LOAD line without its new fields and a SUMMARY without its counts are refused; defload after the first frame and a load defined twice are refused; refusal exits 2 on the run, campaign and regrade paths
[R815] FINDING Tests — wire_selftest.py:241-275, receipts/delta_mutants.log — F1 (MINOR): 11 of 14 delta mutants killed, including every check the rulings named (pairing, PROBE_TX count, bind and AEM/MVU status, no-period, stopped, skip-after-ANNOUNCE, frame equation, split sources, Makefile, firmware tree); expiries-met, partial and over-delivery mutants survive
[R815] PASS Docs — tb/verilator/ctrl_wire_timing/README.md:1-350, sw/firmware/ctrl/maap/README.md:46-49, docs/testing/CI_WORKFLOWS.md:465-485, tb/verilator/milan_dp/README.md:1201-1208, PR #879 body, receipts head/ and campaign/ — every figure in the Results and campaign tables and bullets matches the published results.json and summary.txt to the stated rounding (spot-checked: 18.3/181.7, 24.5/215.5, 1,887+64=1,951, 1,104+847, 42,122+1,368=43,490, 664/663/4,641/231, 5 and 11 delivered, 4 and 11 met, 41.6 ms, 1.82 ms, 2.46 ms on 20 frames, 612.6/1,012.6 ms); the control tables list all 49 controls with their words as the self-test prints them; the reuse record's text matches inputs(); the CI page's three packages and their reason match the template, workflow and ci_events entry (ci_events --check rc 0); the round-1 GET_AS_PATH figure is corrected in README and PR, and the issue body quotes no figure; the source comments in the delta carry no lane label, round, reviewer ID or comment ID (scan of added .py/.cpp/.yml/Makefile lines); R1 is wording only
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `wire_scenario.py` AECP_COMMANDS; `wire_grade.py` acmp/aecp/adp; the published logs' census; results and campaign summary against #868 1-4 and the clauses | R815-2 | `e3f96a67b5dd1b9e4536ca67a6bd1595f4c19d53` |
| RTL | CLEAN | `receipts/delta-scope.txt` (no RTL/firmware/mailbox/gitlink); `milan_dp/Makefile` print target; `wire_main.cpp` echo/offer/LOAD | R815-2 | `e3f96a67b5dd1b9e4536ca67a6bd1595f4c19d53` |
| Robustness | CLEAN | `wire_build.py` reuse guard (three probe sets, both points); `run.py` refusal paths; grader refusals; defload guards | R815-2 | `e3f96a67b5dd1b9e4536ca67a6bd1595f4c19d53` |
| Tests | UNCLEAN (F1) | `wire_selftest.py` (49 controls, run), 14 delta mutants, round-1 probes rerun | R815-2 | `e3f96a67b5dd1b9e4536ca67a6bd1595f4c19d53` |
| Docs | CLEAN (R1 residue carried) | harness README, MAAP README, CI_WORKFLOWS.md, milan_dp README, PR body | R815-2 | `e3f96a67b5dd1b9e4536ca67a6bd1595f4c19d53` |

## Real limits

- **Hosted evidence.** No hosted run has executed the wire-timing step at this head. All four workflows at `e3f96a67` were `cancelled`. The `wire-timing` job ran its new pip install step successfully, then was cancelled while building Verilator on a cache miss. So acceptance 5's hosted wall time inside the 30-minute budget is unproven. Locally:
  - the fresh-runner replica took 1,299 s for the step at `fbe5acc983`;
  - the gate pass on four contended CPUs took 2,505 s, which is over 30 minutes.
- **No build or simulation run by this reviewer.** Source-head execution evidence is the author's published, hash-manifested receipts, spot-checked as above. No manager source bank runs at this head, and none is claimed.
- **Unloaded logs only.** The composed and campaign `wire.log` files (over 200 KB) are not in the packet; only their sha256 are. So the regrade and mutation probes ran on the two unloaded logs. Loaded figures, the echo census and the frame equation are checked from the published `results.json`, `echoes.txt` and `summary.txt`.
- **`read_by_tools()` and `generator_modules` not exercised.** These parts of the reuse record need a real build's dependency files. The probes used stand-in build directories recorded by `inputs()` itself. The required kinds are covered independently by `split_sources()` and `tree:firmware`. The author's same-head `--reuse-build` 8x8 run (accepted, byte-identical) shows the real record does not over-refuse.
- **Unsigned packet.** The evidence archive commit is unsigned; integrity rests on the hash manifest, verified 1,545 of 1,545.
- **No hardware proof.** Physical calibration was NOT RUN; simulation figures are not hardware proof.

## Pending manager duties

- The hosted `rtl-fast` (with `wire-timing`), `rtl-full`, `docs` and `elaborate` contexts at the exact head, and the first hosted `wire-timing` wall time against acceptance 5's 30-minute budget.
- The current-dev candidate merge (live `dev` `fa6c094b`, base `dev-soft-core` now `764482b45f`, lane merge base `1d6bf555`), with its builder and native banks.
- Open the separate Issue for the CPU budget harness's GET_AVB_INFO row (`tb/verilator/ctrl_service_budget/scenario.py:464`, still 0x0028), per ruling item 2.
- Carry R1 to the residue checklist.
- After F1 is fixed, re-cover Tests at the new head. Any commit that touches the grader, harness or docs also un-covers the lenses whose scope it touches.

R815-2 FINISHED
