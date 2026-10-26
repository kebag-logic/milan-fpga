[R703] NEGATIVE - exact head f887663852d118e810ef690c3dd5cf9fe2292588

# [R703] R703-3: internal cleared-context review of PR #792 (issue #665, CPU budget), round 3 delta

Head `f887663852d118e810ef690c3dd5cf9fe2292588`, tree `cf2618f79f020ff486b2165ffd81f12e1146298d`, base `dev-soft-core` `e76a755a`.
The delta under review is `cd3525c3..f8876638`, one commit by the S2 executor. It changes only `tb/verilator/ctrl_service_budget/` (README, grade, oracle, run, scenario, selftest, selftest_mutants).
It answers R703-2 and R704-2, per the round-3 assignment.
The expected T_svc miss is the result, not a finding.

## Verdict

**NEGATIVE.** Round 3 fixes every round-2 finding at its cause, and my measurements reproduce the published figures exactly:

- SRP is now graded as a measured service row, and its starvation is reported by duration.
- Fan-out runs at the registration capacity.
- The owed row carries its 12 ACMP commands, with causal order proven.
- The self-test checks every composed window against a load restated from the contract.
- N6, N8 and N10 are caught.
- SHUTDOWN counts as one path.

Four findings remain open:

- **R703-3-F1 (MAJOR).** The PR fails the repository's bare-metal scope gate at this head, both locally and hosted. The hosted fail-fast then cancels the exact-head long gates.
- **R703-3-F2 (MINOR).** In the formal arm, the "composed maximum" headline is a figure that excludes the windows the firmware never finished. It is half the measured lower bound.
- **R703-3-F3 (MINOR).** The README's and PR's fan-out cost and time ranges are lower than the README's own table.
- **R703-3-F4 (MINOR).** Two rules behind newly published figures (the per-recipient cost and the service rows' records ahead) have no check that can fail. Plausible defects in either change published values while the self-test passes.

## Round-2 probes, rerun unmodified at this head

| Probe | Result | Receipt |
|---|---|---|
| (1) SRP service under the composed load | **Met.** SRP's first and last record of every window are graded rows from commit to the end of the releasing pass. In arm A's `backlog-adp` and `backlog-adp-refill`, all 32 SRP records are never released (at least 567.95-628.32 ms at 1x1, 583.52-658.79 ms at 8x8), and the window reports `serviced` false with `unreleased {'srp': 32}`. My raw-log recomputation (`scripts/service_check.py`, which uses neither `grade.py` nor `scenario.py`) agrees with every service row and every committed population in all 14 windows, arms A and B, both points. Round 2's `srp_service.py` reproduces the round-2 figures (no release in the bound-talker windows; 76.88 ms to the first release in `backlog`). | `service_check_*.txt`, `srp_service_a1x1.txt` |
| (2) Fan-out at registration capacity | **Met.** My round-2 `fanout_full.py` group reproduces 11.33241 ms (1x1) and 20.68273 ms (8x8), identical to round 2. The harness's `aecp-fanout` group registers 16 controllers per interface. It gives SET_NAME 11.33 ms at 1x1 and 20.68 / 22.98 ms at 8x8, every recipient count 16 or 32, and every README fan-out cell matches in both arms. | `fanout_full_*.txt`, `fanout_group_A.txt`, `fanout_group_B.txt` |
| (3) Owed row population and coverage | **Met.** At both points and in both arms the owed window commits ADP 8, ACMP 12, AECP 16, MAAP 7, SRP 32 and GM 15. That equals my own contract derivation: min(burst, ring room at the clause frame size), 16 event records less the row's own, and the ring's room for the refill ADP. From raw wire frames, the probe's response 0x7387 follows the 12 pre-filled responses and then exactly 0x7380-0x7386 in order. 0x7390-0x7393 are never answered at 1x1, and 0x7391 and 0x7393 at 8x8, as published. My eight source plants each fail a named check: SRP, MAAP or ACMP omitted from the scenario source in every row, at one point only, in the bound-talker rows only, half the AECP burst, and 14 GM changes. | `owed_check_A.txt`, `armB_summary.txt`, `review_mutants3.log` S1-S8 |
| (4) A composition defect halving the composed maximum | **Met** for the defect named in round 2. N6 (the window's first pass) is caught by "the composed maximum is the window's longest pass, wherever it falls". So are N8, N10, H1 (the last pass) and H2 (the median pass). A value-dependent filter (H3) still escapes; see S1. | `review_mutants2.log`, `review_mutants3.log` |
| (5) SHUTDOWN counting | **Met.** `control.shutdown.if0` has path `adp.shutdown`. S1 reports 1 path and 2 instances, S8 2 paths and 3 instances (published `runs/S1`, `runs/S8`). A check on the real groups and a mutant exist (`selftest.py:469-491`). | published `runs/S1/results.json`, `runs/S8/results.json`; `selftest.log` |

## What reproduces

- **Self-test.** `run.py --self-test` gives 81 checks and 52 of 52 mutants caught, rc 0 (`selftest.log`).
- **Arm A, full runs at the head on fresh builds.**
  - 1x1: `18 groups graded, 0 refusals, 58 T_svc misses (58 of 141 probe instances, 22 of 81 paths)`.
  - 8x8: `17 groups, 102 of 182, 60 of 129`, rc 0 each.
  - Every published probe row is identical to mine, as are the worst pass and the composed window: 141 of 141 and 182 of 182 (`compare_published_A.txt`).
- **Arm B.** I ran `backlog`, `backlog-adp`, `backlog-owed` and `aecp-fanout`, and 52 of 52 and 60 of 60 rows are identical (`compare_published_B.txt`).
- **Fixture.** Regenerating it through its generator from my 1x1 fixture run gives `fixture.log` and `oracle.json` byte-identical to the committed files (`fixture_regen.txt`).
- **Release accounting.** All 1,297 RX_TAIL writes in my logs land on a record boundary of header words plus ceil(bytes / 4), mod 2^16. That is the accounting `grade.releases()` assumes (`tail_boundaries.txt`).
- **Idle range.** Excluding the last idle run does not change the reported idle maximum at either point (`idle_runs_A.txt`).
- **Gates.** All docs.yml check-mode gates I ran pass except `check_baremetal_only.py --check` (F1): docs, doc paths, doc style, em dash (0 of 607 added lines), TOC and anchors, py/cpp/sh/sv idiom, hygiene, TODO ownership, naming, fail-fast, test evidence, archive, SoC sources, RTL source lists, port contracts, wire accountability, solution docs, gate workflows and `git diff --check` (`gates/summary.txt`).

## Findings

### R703-3-F1 MAJOR: Tests, Docs. The PR fails the repository's bare-metal scope gate at this head

- **Where.** `tb/verilator/ctrl_service_budget/scenario.py:805`, the comment "the egress held and the TX ring filled".
  - The line arrived in `d58c8e22`.
  - This delta rewrote the comment block it opens (`:805-808`) and left the line unchanged.
- **Authority and evidence.**
  - `.github/workflows/docs.yml:306` runs `python3 scripts/check_baremetal_only.py --check` (#259; `docs/testing/CI_WORKFLOWS.md:2402`).
  - Locally at the head it exits 1: `scenario.py:805: [H] retired target host-plane surface 'TX ring' ... baremetal-only: FAIL (1 finding(s) across 1431 scanned file(s))` (`gates/check_baremetal_only.log`).
  - Hosted `docs-gates-0` fails on the same line (job 121723005938, step "Bare-metal scope gate"). `docs-check` then fails, and "Fail fast across this head" cancels the Verilator shards, the firmware jobs and the Yosys workers. So `verilator-suites` and `yosys-portability` fail on unvalidated shards (`hosted_checks_excerpt.txt`).
  - `cd3525c3` failed the same way. The REVIEW READY gate list does not include this gate.
  - AGENTS.md, Tests lens: "Existing regressions remain green". Section 7: the required gates pass.
- **Impact.**
  - A required gate is red at the PR head.
  - The hosted exhaustive Verilator and Yosys evidence cannot complete at any head that keeps the line.
- **Required outcome.**
  - The comment names the mailbox ring without the refused term, for example "the ACMP transmit ring filled", as `mailbox.yaml` names it. The gate's term table is not changed.
  - The author's validation lists the bare-metal gate.
- **Verification.**
  - `python3 scripts/check_baremetal_only.py --check` exits 0 at the new head.
  - Hosted `docs-gates-0` succeeds, and the long gates are not cancelled by fail-fast.

### R703-3-F2 MINOR: Conformance, Docs. The formal arm's "composed maximum" headline excludes the windows the firmware never finished, and so halves the measured figure

- **Where.**
  - README: `README.md:193` (the Passes table's "Composed maximum" column), `:200`, `:205` ("The composed maximum at both points is the `backlog` group's") and `:427` ("The composed maximum is 14.81 ms at 1x1 and 27.84 ms at 8x8, in both arms").
  - PR body: the row "Composed maximum (load released), A and B | 14.81 ms | 27.84 ms".
  - REVIEW READY: "S2b should re-base ... because round 2's composed maximum ... [is] superseded".
- **Authority and evidence.**
  - The S2 assignment asks for "the worst pass at the composed maximum", meaning the worst pass under the defined composed load.
  - In arm A, the formal measurement, `backlog-adp` and `backlog-adp-refill` commit exactly the defined load (my contract derivation agrees, `service_check_a*.txt`). Inside those windows the CPU runs passes of 1,565,803 cycles (31.32 ms) at 1x1 and 2,209,308 cycles (44.19 ms) at 8x8.
  - The worst pass under the composed load in arm A is therefore at least 31.32 ms and 44.19 ms: a lower bound, because SRP's work never ran.
  - Round 3 now defines the composed maximum as "the longest pass of a window that released its whole load" (`README.md:200`). That definition drops those windows, and the arm A headline falls from 31.32 ms to 14.81 ms and from 44.19 ms to 27.84 ms.
  - The lower bounds are in the table's last column and in the same sentence, so nothing is hidden. But the figure labelled "composed maximum" for arm A is not the worst pass under the defined load.
  - R703-2-F1's required outcome was that a starved load "cannot stand as a measured composed maximum". It did not ask for the formal figure to be replaced by a smaller one from other windows.
- **Impact.**
  - Firmware that fails to finish its load lowers the headline figure.
  - S2c's acceptance compares "composed maximum" against S2's no-cache tables. If a cache shortens the passes enough for SRP to be served in `backlog-adp`, that window starts to count. The before-and-after then compares different window sets, and the no-cache baseline is understated by half in the formal arm.
- **Required outcome.**
  - Arm A's composed maximum is stated as the maximum over every window committing the defined load: at least 31.32 ms at 1x1 and at least 44.19 ms at 8x8, labelled a lower bound because SRP's load is never released.
  - The figure restricted to windows that released their load may stay beside it, labelled as such.
  - `README.md:193`, `:200`, `:205`, `:427`, the PR body and the hand-off agree. The S2b and S2c re-base note says which figure is the baseline.
- **Verification.** Read the README and PR text. A regrade of the same logs (no new measurement is needed) gives the same cycles.

### R703-3-F3 MINOR: Conformance, Docs. The stated fan-out cost and time ranges are lower than the README's own table

- **Where.** `README.md:303` ("the others cost 11,800 to 13,400"), `README.md:440` ("costs a recipient 11,800 to 20,400 CPU cycles, so 16 registrations take 7.8 to 11.3 ms at 1x1 and 32 take 12.4 to 23.0 ms at 8x8"), `README.md:446` (D4 (a): "11,800 to 20,400 cycles each"), and the PR body's "A notification costs 11,800 to 20,400 CPU cycles a recipient".
- **Evidence.** The README's own fan-out table (`README.md:284-298`), reproduced by my arm B runs (`fanout_group_B.txt`), shows:
  - SET_STREAM_INFO at 21,875 / 22,030 cycles a recipient, which is above 20,400, and BIND_RX's GET_STREAM_INFO notice at 18,358 / 18,359, which is outside "the others ... 11,800 to 13,400".
  - At 1x1, SET_STREAM_INFO 11.68 ms and the BIND_RX notice 14.80 ms. Both are above "7.8 to 11.3 ms".
  - At 8x8, SET_STREAM_INFO if1 32.78 ms, above "12.4 to 23.0 ms".
  - The ranges hold for arm A only, and none of the sentences says so.
- **Impact.** The D4 (a) consumer list and the Findings understate the measured per-recipient cost and fan-out time. These are figure claims, so this is not wording residue.
- **Required outcome.** Either:
  - the ranges cover every measured fan-out (11,800 to 22,030 cycles; 7.8 to 14.8 ms at 1x1; 12.4 to 32.8 ms at 8x8), with the arm named where it matters; or
  - each sentence is scoped to arm A explicitly, and arm B's maxima are stated next to it.
- **Verification.** Every range in `README.md:303`, `:440`, `:446` and the PR body contains every cell of the fan-out table it summarizes.

### R703-3-F4 MINOR: Tests. Two rules behind newly published figures have no check that can fail

- **Where.**
  - `grade.py:516-518`: `per_recipient_cpu_cycles` is (last - first) // (recipients - 1).
  - `grade.py:718`: a service row's `ahead` counts the earlier records not yet released at its commit.
  - Both figures are new in this delta and published: the README fan-out table's "CPU cycles a recipient" column and the D4 (a) consumer, and the brackets "[N ahead]" of "The load's service" table.
- **Authority and evidence.**
  - The `selftest.py` docstring says "each rule is mutated in turn, and a named check must fail". AGENTS.md, Tests lens: each test can fail for the defect it claims to detect.
  - My plant G6 divides by the recipients rather than the gaps. G9 counts only the records never released as ahead.
  - Both pass the self-test, rc 0 (`review_mutants3.log`). Regrading my head logs under them changes published values (`mutant_regrade_escapes_*.txt`):
    - G6: SET_NAME 20,358 to 19,085 cycles a recipient at 1x1 (9 rows), and 20,486 to 19,846 at 8x8 (13 rows).
    - G9: every service row's last-record bracket goes to 0, for example `backlog.service.srp.last` 31 to 0 and `acmp.last` 11 to 0 (18 rows per point).
  - The fixture's service rows have one record per channel, so their pinned `ahead` is 0 and cannot detect G9. No check computes a per-recipient cost.
- **Impact.** A refactor that miscounts either figure would change the published decision inputs silently.
- **Required outcome.**
  - A named check fails under G6: for example, a synthetic fan-out of three recipients at known commits with its per-recipient cost asserted.
  - A named check fails under G9: for example, a synthetic window with two records on one channel, the second committed before the first is released, so its `ahead` must be 1.
- **Verification.** `scripts/review_mutants3.py` reports G6 and G9 caught.

## RESIDUE (purely wording; exact fix given; carried to the manager's checklist)

- **R703-3-R1: SET_STREAM_FORMAT's notice is not run, and nothing says so.**
  - `sw/firmware/ctrl/aecp/aecp_commands.c:264-275` notifies a changed stream format (`AECP_CHANGE_FORMAT`).
  - Both arms' format port answers unsupported (`sw/firmware/ctrl/test/ctrl_aecp_image.c:73`, `a_format`; arm B's edits in `build.py:67-77` leave it), so the image never completes it.
  - The coverage claim "each state-changing command the image notifies" is therefore literally true, and no figure changes.
  - Fix: add to the README's Limits, after the START_STREAMING line: "SET_STREAM_FORMAT is refused in both arms, whose format port answers unsupported (`ctrl_aecp_image.c`, `a_format`), so its fan-out is not run."
- **R703-1 R-4 / R704-2-R1 (retained).** `docs/testing/TESTING.md:518` still names one Makefile exception. It sits outside this lane's file map, as disclosed.

## SUGGESTION

- **S1: a value-dependent composition filter escapes.**
  - H3 drops passes over 1 M cycles from the window. It passes the self-test and lowers the 8x8 composed maximum from 1,392,016 to 881,915 cycles (`mutant_regrade_escapes_a8x8.txt`).
  - The synthetic window's passes are 100 to 900 cycles and the fixture's are all under 1 M, so no check sees a long pass.
  - The threshold is contrived, so this is optional. A synthetic window whose longest pass is several million cycles would close it.
- **S2: idle range.**
  - `grade.py:794-796` drops the whole last idle run, from both the minimum and the maximum.
  - Only the minimum is distorted by the cut pass. A cut pass can only be shorter than its whole, so the run's maximum is still a real idle pass's lower bound.
  - It changes no figure at this head (`idle_runs_A.txt`). Excluding the run only from the minimum would keep a longer final idle pass from being lost.
- **S3: R703-2 S1-S3 (carried, optional).** Refill-phase sweep, `-B` for the build's child Python, and a note that cross-build identity is the ELF and the logs.
  - My fresh builds again have different executable digests from the author's, while every compared probe row is identical.

## Prior public findings at this head

| Finding | Status at `f8876638` | Evidence |
|---|---|---|
| R703-2-F1 (SRP service) | **Resolved as required**: service rows with verdicts, starvation reported by duration, the starved window flagged with its unreleased records, the mechanism in Findings. The headline's new exclusion rule is F2, a new finding. | probe 1 |
| R703-2-F2 (fan-out capacity) | **Resolved**: every fan-out the image completes, at 16 per interface, reported with a per-recipient cost. The range wording is F3, and the cost rule's protection is F4. | probe 2 |
| R703-2-F3 (composition protection) | **Resolved**: N6, N8 and N10 are caught. | `review_mutants2.log` |
| R703-2-R1 to R5 | **Resolved** (`README.md:166-167`, `:321-322`, `:356`; the comment-rule instances are gone from the harness). | grep at the head |
| R704-2-F1 (owed population, independent coverage) | **Resolved**: 12 ACMP commands, 7 owed proven in order, the defined load derived from the contract in `grade.defined_load` and restated in `selftest.DEFINED`, and SRP, MAAP and ACMP omissions caught (the author's mutants and my S1-S8). | probe 3 |
| R704-2-F2 (SHUTDOWN counting) | **Resolved**: one path, 2 / 3 instances, with a real-group check. | probe 5 |
| R703-1 R-4 / R704-2-R1 | **Retained** as residue. | |

## Comment rule (delta)

- No new source comment in the delta carries a bench lane label, lane name, review round, reviewer ID or issue-comment ID.
- "A3" (`scenario.py:797`) is `MAILBOX_SPLIT.md`'s assumption A3 (`:460`), and "H-AECP" and "H-NOTIFY" are `FR_NFR.md` hazard IDs.
- "(earlier rule)" replaced the head-hash suffixes, and the README's round-2 clause is removed.

## Lens ledger (reviewer-owned)

| Lens | Result | Examined artifacts (at the head) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | **UNCLEAN** (F2, F3) | Round-3 items 1-5 against `grade.py:621-641` (`defined_load`), `:695-734` (`service`) and `:742-765` (`composed`); `scenario.py:529-608` (`aecp_fanout_groups`) and `:801-839` (`owed_group`); `aecp.c:401-419` (recipients exclude the requester); `README.md:193-205`, `:278-303`, `:427-446`; PR body; my contract derivation (`service_check.py`) and wire-order check (`owed_check.py`) | R703-3 | `f887663852d118e810ef690c3dd5cf9fe2292588` |
| RTL | **CLEAN** | `[R703] PASS RTL — sw/mailbox/mailbox.yaml:419-433 (RX_HEAD/RX_TAIL mod 2^16) and grade.py:655-673 (releases) — all 1,297 RX_TAIL writes in my logs fall on header + ceil(bytes/4) record boundaries; srp_mbx.c:441-451 (rx_order_ready, the starvation cause) and tsn-c-stack ACMP_OWED_MAX (the drop) are cited correctly; no RTL, SoC, firmware or CI file is in the delta (git diff --stat cd3525c3..f8876638)` | R703-3 | `f887663852d118e810ef690c3dd5cf9fe2292588` |
| Robustness | **CLEAN** | `[R703] PASS Robustness — grade.py:438-446 (never_answered), :500 (may_drop), :695-734 (never released) and run.py:44-56 (verdict_word, severity) — a dropped command and a never-released record are reported unbounded and outrank any time (selftest window_checks; my G8 plant caught); overpopulation, an omitted channel and a short declaration are refused (N8, S1-S8 caught); misordered or missing owed responses are refused (G7 caught); the backpressure rows (the owed egress held, the ACMP drop at 8 owed) were reproduced from wire frames at both points and in both arms` | R703-3 | `f887663852d118e810ef690c3dd5cf9fe2292588` |
| Tests | **UNCLEAN** (F1, F4) | `selftest.py:147-546`; `selftest_mutants.py:26-100`, `:249-331`; `oracle.json`; `review_mutants2.log` (23 of 25 caught, N11 and N12 changing 0 values), `review_mutants3.log` (16 of 21 caught; G2 and G3 change 0 values, G6 and G9 change published values, H3 is contrived); the fixture regenerated byte-identical; `gates/check_baremetal_only.log` | R703-3 | `f887663852d118e810ef690c3dd5cf9fe2292588` |
| Docs | **UNCLEAN** (F1, F2, F3) | `README.md` (the whole delta, by section), the PR body and REVIEW READY; `scenario.py:805` against #259's gate; the docs gates (`gates/summary.txt`) | R703-3 | `f887663852d118e810ef690c3dd5cf9fe2292588` |

My round-2 ledger stands for code this delta does not touch: `sim_main.cpp`, `build.py`, `split_soc.py`, `frames.py`, `runtime_ssp.py`, `fixture_variant.py` and `observe.vlt` are unchanged.

## Real limits of this review

- **No manager source bank** runs at this exact head, and I claim none. Source-head execution evidence is the author's published receipts plus my own runs listed here.
- **Hosted evidence.** At this head, `docs-gates-0` fails on F1's line. `docs-check`, the `Union *` contexts, `elaborate`, `verilator-suites` and `yosys-portability` fail or are cancelled behind the fail-fast. No exact-head hosted Verilator or Yosys result exists. Hosted and act acceptance belong to the manager.
- **Arm B coverage.** I re-ran four of arm B's eight groups (`backlog`, `backlog-adp`, `backlog-owed`, `aecp-fanout`). The other four (`acmp-*`) are unchanged scripts, accepted from the published receipts.
- **Shutdown arm and controls.** I did not re-run the shutdown-entry arm or the three controls; I accepted the published `runs/S1`, `runs/S8` and `drivers/regrade-C-*` receipts. The delta does not change their scripts, only the SHUTDOWN control's path key, which I checked in the published `results.json`.
- **Physical calibration NOT RUN.** Every figure is a simulated cycle count on the test SoC. Flash erase and program waits are zero, and no hardware was used.
- I did not check the Milan v1.2 Table 5.26 citation for the ACMP controller timeout against the standard's text.

## Pending manager duties

- Validate the current-dev merge candidate (source base `e76a755a`, live dev `76de691e5625cc4ea2f9a19def9e07c1183a14ee`) with the builder and native banks, and own hosted and act acceptance once F1 is fixed.
- Carry R703-3-R1 and R-4 to the residue checklist.
- Decide the author's open question: whether the SRP starvation (`srp_mbx.c:441-451` with passes longer than the TICK), the ACMP owed-capacity drop (ring room 12 against `ACMP_OWED_MAX` 8) and the per-recipient fan-out cost become Issues or S2b scope.
- Tell S2b and S2c which composed-maximum figure is the no-cache baseline (F2).

## Receipts

All receipts are under `receipts/`, and scripts under `scripts/`; `MANIFEST.sha256` lists them.

- **Runs.** `runs/{a1x1,a8x8,b1x1,b8x8}/` (results.json, table.md, the printed summary with rc, and the build identity).
- **Raw logs.** `logs/*.log.gz` for `backlog-adp`, `backlog-owed` and `aecp-fanout` at both points, arm A.
- **Delta.** `delta_cd3525c3_f8876638.diff`.
- **Gates and environment.** `gates/` (each gate's log and `summary.txt`), `hosted_checks_excerpt.txt`, `environment.txt`.
- **Clone restore.** `clone_identity_final.txt`: the clone restored to exact head bytes, modes, index and gitlinks, with 0 rehash mismatches.

R703-3 FINISHED
