[R816] NEGATIVE - exact head bfb2df37079f0172d6e94841ea5b9bd084e3ee06

# R816-1: external review of #868 / PR #879

- Head under review: `bfb2df37079f0172d6e94841ea5b9bd084e3ee06`, tree `c39da4934203695af6af8d00b3f16dd80c8eab8c`.
- Source base: `dev-soft-core` `1d6bf5556ae28764361d85012b86394eb467d294`, seven lane commits.
- Role: external, cleared-context reviewer. The scope came from the Issue body, the round 2 ruling (issuecomment-6755260058) and the public PR and Issue text.
- Lenses applied: all five (Conformance, RTL, Robustness, Tests, Docs).
- Result: three MINOR findings and one RESIDUE. The open MINORs leave Conformance, Robustness, Tests and Docs unclean, so the verdict is NEGATIVE. RTL is clean.

The acceptance figures the PR publishes reproduce from its receipts. The two published real logs regrade at this head to byte-equal results. Every published bound holds. The findings concern:
- what the CI gate can detect (F1);
- one AEM command that the stimulus does not actually send (F2);
- the reuse guard behind the locally reused builds (F3).

## Prior public review findings

At the time of reading, PR #879 had only the two review-start notices, and Issue #868 had only executor and manager comments. No prior review finding exists to resolve or retain.

## Findings

### F1: MINOR (Tests, Robustness): a bind that causes no PROBE_TX is not a finding, and a refused bind is timed as a round trip

- **Where:** `tb/verilator/ctrl_wire_timing/wire_grade.py:399-403`, `:393-398` and `:569-574`.
- **Authority:** #868 scope, "the PROBE_TX it causes to PROBE_TX_RESPONSE". FR_NFR.md 3.4.2 H-ACMP. AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect."
- **Evidence:** `receipts/grader_probes.log`, from `scripts/grader_probes.py`, run on the author's published real log `ci-1x1-none__wire.log` (sha256 `44e571ae2161d82c…`, the log of the head's CI step):
  - **R0:** an unchanged regrade gives 0 findings, with results identical to the published `results.json`. The same holds for `8x8-none`.
  - **R1:** draw 5's PROBE_TX is never sent. Its commit, its KL_mbx egress and the talker's answer are removed too, which is the log such a firmware leaves. Result: **0 findings**, with `acmp.probe_tx` N=15 against 16 binds.
  - **R2:** only the last of 16 PROBE_TXs is sent, so 15 binds cause none. Result: **0 findings**, with `acmp.probe_tx` N=1.
  - **R3 (control):** no PROBE_TX at all gives 17 findings. The check fires only when no later PROBE_TX exists.
  - **R4:** the first BIND_RX_RESPONSE carries status 1 (LISTENER_UNKNOWN_ID). Result: **0 findings**, and the refusal is timed as `acmp.bind_rx`.
- **Why it happens:** `after = [p for p in probes if p.first > cmd.last]` (`:399`) pairs each bind with *any* later PROBE_TX, including a later draw's. So the "caused no PROBE_TX" finding (`:401`) is defeated whenever any later draw sends one. The count checks (`:569-574`) compare only the stimulus's own frames, BIND_RX and the AEM commands, which always equal `draws`. No check compares the transactions the entity performed with `draws`. No check reads a response's status (`:393`).
- **Impact:** the CI step (`run.py --ci`, required by `rtl-fast`) passes when the listener skips its PROBE_TX on 15 of 16 binds, or refuses binds. Its claim to time "the PROBE_TX it causes" then rests on one sample. `acmp.bind_to_probe_tx` would also pair a bind with another draw's PROBE_TX. The published figures are not affected: every published run has N equal to its draws on every ACMP path (16 or 342), and every published ACMP response has status 0 (`receipts/status_census.log`).
- **Required outcome:**
  - Each BIND_RX is paired only with a PROBE_TX it causes: after its own response and before the next draw's bind, or matched by stream identity. A bind without one is a finding.
  - The graded PROBE_TX transactions equal the draws.
  - A BIND_RX_RESPONSE whose status is not SUCCESS is a finding, or is excluded and reported with its reason.
  - Each of these has a self-test control.
- **Verification:** `scripts/grader_probes.py` R1, R2 and R4 each yield a finding at the fixed head, R0 still passes, and `run.py --self-test` carries the new controls.

### F2: MINOR (Conformance, Tests, Docs): the stimulus's "GET_AVB_INFO" is GET_AS_PATH on AVB_INTERFACE 9, which the entity refuses, and the published slowest AEM response is that refusal

- **Where:** `tb/verilator/ctrl_wire_timing/wire_scenario.py:104` sends `('get_avb_info', 0x0028, f.be(9, 2) + f.be(0, 2) + bytes(16))`. Related: `tb/verilator/ctrl_wire_timing/README.md:100` and `:178`, the `aecp.response.get_avb_info` result rows, `wire_grade.py:436-446` (any status accepted as final), and the PR body's AECP sentences.
- **Authority:** AEM command codes, IEEE 1722.1-2021 7.4.40 and 7.4.41 (Milan v1.2 5.4.2.23 and 5.4.2.24): `0x0027` is GET_AVB_INFO and `0x0028` is GET_AS_PATH. The repository agrees in three places:
  - its table at `docs/MILAN_V12_ROADMAP.md:126-127`;
  - the processor's AECP ucode, `protocol-processor/hdl/aecp/ucode/gen_ucode.py:196-197`;
  - the firmware, `sw/firmware/ctrl/aecp/aecp_commands.c:642` (`case 39: case 40: return avb(a, cmd == 40u, ...)`, where 40 is the AS_PATH form).

  GET_AS_PATH reads its descriptor_index from the payload's first word (`aecp_commands.c:427`), which is 9 here, and no AVB_INTERFACE 9 exists (`:428-429`).
- **Evidence:** `receipts/aecp_status_1x1.log` and `receipts/status_census.log`, read from the published real logs. Every response to command `0x0028` carries status 2 (NO_SUCH_DESCRIPTOR), 3 of 3 in each run. Every other AEM command, the MVU command and every ACMP response is status 0.
- **Effect on the published figures:**
  - In the author's `gates/extra/logs/wire-8x8-composed.log` (head `bfb2df3707`), the run's `aecp.response` maximum, 20567.440 us, is the `aecp.response.get_avb_info` maximum.
  - So "The slowest AEM response is the loaded 8x8's at 20.6 ms" (README:178, PR body, REVIEW READY item 3) is a GET_AS_PATH refusal.
  - README:100 says each draw's AEM command is, in turn, "READ_DESCRIPTOR (ENTITY), GET_CONFIGURATION, GET_COUNTERS, GET_AVB_INFO, GET_NAME and the MVU GET_MILAN_INFO".
  - `aecp()` accepts a response of any status, so the grader cannot notice.
- **Impact:** one sixth of the AECP draws never exercise the stated command or its GSI-window path (kind 1). A headline figure and the per-command rows are labelled with a command that was not sent. The 240 ms bound itself still holds for every response measured.
- **Required outcome:**
  - The stimulus sends what it states: GET_AVB_INFO `0x0027` on AVB_INTERFACE 0 with its 7.4.40 command length. Alternatively, it names the row GET_AS_PATH with a valid index.
  - The affected figures are re-measured, or relabelled, in README, PR and Issue text.
  - The grader treats a non-SUCCESS AEM or MVU final response as a finding unless that status is stated as expected.
  - The same row in the read-only CPU budget harness (`tb/verilator/ctrl_service_budget/scenario.py:464`) is outside this lane and needs its own Issue.
- **Verification:** at the fixed head, `scripts/status_census.py` and `scripts/aecp_status.py` on a fresh run's `wire.log` show status 0 for every AEM response, or only the stated expected statuses. The renamed or re-measured rows appear in `results.json`, and a self-test control with a refused AEM response is caught.

### F3: MINOR (Robustness, Docs): `--reuse-build` accepts a build after its split-top RTL or firmware sources change, although the build docstring says every input is recorded

- **Where:** `tb/verilator/ctrl_wire_timing/wire_build.py:22-23` (claim), `:169-179` (`inputs()`), `:206-215` (`reused()`), and `README.md:44`.
- **Authority:** the module's own claim: "Every input the model is built from, or reads when it runs, is recorded in build.json with its digest, so a reused build is refused when any changed."
- **Evidence:** `receipts/reuse_probe.log`, from `scripts/reuse_probe.py`. The probe builds a synthetic build directory recorded by `wire_build.inputs` itself, with the CPU half's tracked mailbox Verilog as `spec['sources']`, as the published CI step's verilate command lists them. It then appends one comment line to each source in turn and restores its exact bytes:
  - **Refused:** edits to `wire_main.cpp` and `hdl/milan/mailbox/KL_mbx.sv`.
  - **ACCEPTED:** edits to `tb/verilator/milan_dp/tb_split_top.sv`, `hdl/milan/milan_datapath.sv`, `third_party/tsn-c-stack/src/maap.c` and `sw/firmware/ctrl/maap/maap_mbx.c`.
  - The guard records built outputs (the ELF, the split archive), not the sources they are built from, and not the recipe (`milan_dp/Makefile`).
- **Impact:** campaign units and `--reuse-build` runs are the local evidence for B.3.4.1 and Table 5.50. They can run on a model built from older RTL or firmware while being reported at a later head. CI is not affected, because it always builds fresh. The published campaign is not shown wrong: it ran on one build at its stated head `107f3f95de`, and the head changes only documentation and one docstring after it (verified with `git diff 107f3f95de bfb2df3707`).
- **Required outcome:** either the reuse guard records the split recipe's and the image's source inputs (the tb_split_top and datapath source list, the firmware sources, the Makefile) and refuses a reuse when any of them changes, or the docstring and README narrow the claim to what is recorded and state that a reused build must be rebuilt after any source change.
- **Verification:** with the guard fixed, `scripts/reuse_probe.py` (extended with the real build's source list) reports "refused" for every edited source. With the claim narrowed, the docstring and `README.md:44` name exactly the recorded set.

### RES-1: RESIDUE (Docs; wording only): a review round named in a source comment

- **Where:** `tb/verilator/ctrl_wire_timing/wire_scenario.py:18`: `THE LOAD (#868, the round 2 ruling): the CPU budget harness's composed load`
- **Rule:** source comments state behaviour and reason with issue and requirement IDs, and never name review rounds (owner, 2026-10-15). This is a new instance in the reviewed delta. Nothing else in the added source lines matched (`receipts/comment_rule_scan.log`).
- **Exact fix:** replace `(#868, the round 2 ruling)` with `(#868)`.

### Suggestions (optional)

- **SUG-1 (Conformance, Docs):** `adp.advertise_period` is graded against 9,400 ms (Table 5.50's 9 s plus FR_NFR.md 3.4.1's 400 ms ceiling), while its clause string says "inside 5 to 9 s" (`wire_grade.py:507-508`, `:529`). Publish the margin to the strict 9 s as well, or put the widened bound in the clause text. The measured maximum, 8,387.6 ms, is inside 9 s either way, and CI measures no period.
- **SUG-2 (Docs):** `docs/testing/CI_WORKFLOWS.md:452-478` quotes only the 578 s local replica. Once the first hosted `wire-timing` run exists, record its wall time there, since it settles item 5.
- **Reviewer position on the PR's open question (ruling item 3), no finding:**
  - The CPU budget harness's composed load never loads a measured path's own channel. Here the draws' ACMP and AECP records are measured paths, so leaving them out of a MAAP or ADP deadline's burst is the faithful translation.
  - The whole-burst variant was also measured (the first campaign, `79997664d5`), with the timers inside their clauses.
  - No change is needed for acceptance. The decision remains the manager's.

## What was checked, by lens

- **Conformance:**
  - Acceptance 1 to 5 against the README and PR tables and the receipts. Campaign `head-107f3f95de/unit{0..3}-results.json`, `-run.json` (seeds 1 to 4, loads none, none, composed, composed, 342 draws, to ANNOUNCE 2, rc 0) and `summary.md`.
  - Each derived sentence recomputed from the receipts: 2.46 ms over 36 frames, 1.7 ms, 1.4 ms, 2.3 ms, 2.1 ms and 2.2 ms, 41.8 ms below the ceiling, 5,363.0 to 8,387.6 ms, 31,956.5 to 31,958.2 ms, 17.7 ms and 182.3 ms, 6.7 ms and 5.4 ms.
  - Bounds at `wire_grade.py:93-112`: 200 ms (Table 5.26), 240 ms (FR_NFR.md 3.4.1, stricter than the 250 ms transaction timeout), strict 500/600 ms and 30/32 s (B.3.4.2 and B.3.4.1), 511 to 589 ms and 30,011 to 31,989 ms (`maap/README.md:43-44`), 0 to 4 s and 0 to 2 s, and 400 and 200 ms.
  - The probe/announce sequencing against `third_party/tsn-c-stack/src/maap.c:69-141`: the last PROBE and the first ANNOUNCE share one expiry, so three probe intervals is the complete set.
  - `maap/README.md:47` is closed by the delta.
  - Finding: F2.
- **RTL:**
  - `tb/verilator/milan_dp/tb_split_top.sv` (head diff): the receive arbiter holds the interface for a whole frame, and resets clear its state. Transmit routes by `tx_if_o`. The interface-1 commit acknowledgement equals `split_soc.py:213-225` `slowest_ack`, and against `KL_mbx.sv:497-508` it is a one-cycle pulse. The `N == 1` path reproduces the old composition.
  - `Makefile:842-881`: the default recipe is unchanged.
  - Built with pinned Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`, `receipts/rtl/build-head-*.log`):
    - default 1x1: rc 0;
    - 8x8 / 2 interfaces with the generated variant: rc 0;
    - no warning on `tb_split_top` or the variant (the remaining warnings are pre-existing ones in `milan_datapath.sv`);
    - the head and base 1x1 split legs give byte-identical output (`exec-{base,head}-1x1.log`, sha256 `14b57a6d8c041bfc…`, `checks: 71 failures: 0`);
    - the recipe's Verilator command lines are byte-identical (`cmd-{base,head}-1x1.txt`).
  - Interface 1 works at 8x8: 13 frames sent unloaded and 847 received under load (published `results.json`).
  - No finding.
- **Robustness:** the grader's refusals (clock, commit pairing, lost frames, censoring with `TAIL_MS` 250 ms covering both bounds); `wire_main.cpp:762-816` (failure on the time limit and on an unsettled boundary); the reuse guard; mutation probes R1 to R5. Findings: F1 and F3.
- **Tests:**
  - `run.py --self-test` at head: `33 controls, 0 failed` (`receipts/selftest.log`).
  - Every control read against its mutation, and the plants on every run read against `wire_selftest.plants`.
  - Grader probes on two real logs (above).
  - `ci_gate_workflows.py --check`: rc 0. `ci_events.py --check`: OK, 2432 items.
  - The author's CI-step receipt at head (`gates/rtl-fast/logs/rtl-fast__wire-timing__ci_step_20.log`, `PASS`) and its byte-equality table (`gates/wire-timing-ci-vs-head.txt`).
  - Findings: F1 and F2.
- **Docs:**
  - The harness README, `milan_dp/README.md:1188-1204`, `CI_WORKFLOWS.md:55-56, 147, 177, 452-478`, `maap/README.md:47-50`, the PR body and the REVIEW READY text, against code and receipts.
  - The README Contents block matches its eight headings.
  - `docs_check.py`: 0 findings.
  - No U+2014 on any added line (`receipts/em_dash_grep.txt`).
  - `git diff --check` against the base: clean.
  - Findings: F2, F3 and RES-1.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2) | #868 acceptance 1-5 and round 2 ruling; `wire_grade.py:93-112, 374-536`; `wire_scenario.py:100-107`; `maap.c:69-141`; `aecp_commands.c:417-430, 642`; FR_NFR.md 3.4.1; campaign and head receipts | R816-1 | `bfb2df37079f0172d6e94841ea5b9bd084e3ee06` |
| RTL | CLEAN | `tb_split_top.sv` diff; `milan_dp/Makefile:842-881`; `KL_mbx.sv:497-508`; `split_soc.py:213-225`; `receipts/rtl/*` (pinned 5.050 builds at 1x1 and 8x8/2if, split leg base = head byte for byte, recipe command line byte-identical) | R816-1 | `bfb2df37079f0172d6e94841ea5b9bd084e3ee06` |
| Robustness | UNCLEAN (F1, F3) | `wire_grade.py` refusals and censoring; `wire_main.cpp:762-816`; `wire_build.py:169-215`; `receipts/grader_probes.log`; `receipts/reuse_probe.log` | R816-1 | `bfb2df37079f0172d6e94841ea5b9bd084e3ee06` |
| Tests | UNCLEAN (F1, F2) | `wire_selftest.py` (33 controls, plants); `receipts/selftest.log`; `receipts/grader_probes.log`; `receipts/status_census.log`; `ci_gate_workflows`/`ci_events` checks; author CI-step receipt | R816-1 | `bfb2df37079f0172d6e94841ea5b9bd084e3ee06` |
| Docs | UNCLEAN (F2, F3; RES-1 is residue) | `ctrl_wire_timing/README.md`; `milan_dp/README.md:1188-1204`; `docs/testing/CI_WORKFLOWS.md:55-56, 452-478`; `maap/README.md:47-50`; PR #879 body; `receipts/docs_check.log`; `receipts/comment_rule_scan.log` | R816-1 | `bfb2df37079f0172d6e94841ea5b9bd084e3ee06` |

## Real limits

- **The wire-timing native model was not built or run here.** No private LiteX tree and CPU generator was available outside the shared product install, and this review does not use shared installs. The exact-head figures rest on:
  - the author's published gate receipts;
  - the regrade of the two published real logs (`ci-1x1-none`, `8x8-none`), which reproduces their `results.json` exactly.
- The composed-load and campaign `wire.log` files are not published (only their hashes). Those figures were checked against their `results.json`, tables and summaries, not regraded.
- The twin leg was not run. Its build differs from the split leg only by `tb_split_top.sv`, whose one-interface output was shown byte-identical on the split leg.
- `check_em_dash.py` and `gen_toc.py` could not run because the pinned Markdown renderer is not installed. A direct scan of the added lines replaced the em-dash check. The Contents block was compared with the headings by hand.
- **Hosted runs were incomplete.** At inspection, the hosted exact-head `rtl-fast` run had its `changes` job queued and `wire-timing` not started. No hosted wire-timing evidence exists yet. Item 5's 30-minute budget is evidenced only locally: 578 s on four CPUs, and 2,317 s in the contended gate pass, which is over the job's 30-minute timeout.
- No physical calibration, bench or hardware result is claimed, and field skips are not hardware proof. No source bank was run here.

## Pending manager duties

- Hosted exact-head `wire-timing` verdict and wall time against item 5's 30-minute budget. The cold-cache CPU generation is part of that job.
- Plus the remaining hosted `rtl-fast`, `rtl`, `docs` and `elaborate` contexts.
- The current-dev merge candidate (live dev `45c0b56c1f4a8a52878815fdcb1359d18e2c5b1c`), with its builder and native banks.
- The decision on the PR's open load question (reviewer position above).
- An Issue for the same `0x0028`-labelled-GET_AVB_INFO row in `tb/verilator/ctrl_service_budget/scenario.py:464` (outside this lane).
- RES-1 onto the residue checklist.
- Re-review of F1 to F3 at the corrected head.

## Clone state after probes

`receipts/restore_verification.txt`:
- HEAD and index tree are `c39da4934203695af6af8d00b3f16dd80c8eab8c`.
- Index modes and blobs equal the HEAD tree, and the worktree and index match HEAD.
- The gitlinks are unchanged: gptp-processor `135afd04`, protocol-processor `a9e84b66`, lwSRP `08ee86e8`, tsn-c-stack `70936b77`, verilog-axis `48ff7a7e`.
- No untracked or ignored files remain.

R816-1 FINISHED
