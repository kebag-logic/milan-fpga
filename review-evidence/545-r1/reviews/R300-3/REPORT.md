[R300] POSITIVE - exact head 92ad1687d84ff077f872719b4f1df601f82064d2

# R300-3: internal independent re-review of #545 / PR #563

- Head `92ad1687d84ff077f872719b4f1df601f82064d2`, tree `836c35f0b513eb9e188d63e11f5dbcda8c8555bd`. Two commits on `b94f53cc`: `b46bbcfb` and `92ad1687`. Source base is `5b73d3f47dfed519eb988c13d6beb1db664ef1e0`.
- This is a delta review of `b94f53cc..92ad1687`. My R300-2 covered `b94f53cc`. The external R301-2 review is POSITIVE at `b94f53cc`, which is an ancestor. So this verdict is the exact-head review for merge.
- Scope was reconstructed from public state only:
  - AGENTS.md and CONTRIBUTING.md.
  - The #545 body.
  - Decisions 5828714628 and 5830332403. The second is the round-3 assignment:
    - item 1: R300-2 F4;
    - item 2: R300-2 F5 and R301-2 S-B;
    - item 3: R301-2 S-C;
    - out of scope: R301-2 S-A, which goes to #495.
  - The [A308] REVIEW READY comment 5830915333.
  - The diff and its history.
  - The author packet `63063851:review-evidence/545-r1/author-r3`.
  - The exact-head hosted runs.
- I read R301-2's findings only after my own pass over the diff and my own probes.
- Verdict: **POSITIVE**.
  - R300-2 F4 and F5 are closed. R301-2 S-B and S-C are addressed.
  - Nothing changed outside the five files the round names. There is no `hdl` change, no submodule gitlink change and no dev merge.
  - Two SUGGESTIONs are recorded. Neither affects coverage.

## What changed at this head

`git diff --name-status b94f53cc 92ad1687` lists exactly five modified files, and no other paths:

- `docs/testing/CI_WORKFLOWS.md`
- `docs/testing/TESTING.md`
- `tb/verilator/mmcm_servo/Makefile`
- `tb/verilator/mmcm_servo/sim_main.cpp`
- `tb/verilator/mmcm_servo/slew_mutants.py`

`git diff --quiet b94f53cc..92ad1687 -- hdl gptp-processor protocol-processor third_party external` returns 0. Parentage is `b46bbcfb` on `b94f53cc`, then `92ad1687` on `b46bbcfb`, so there is no merge. The file count is 894 at both heads.

## Prior findings on this PR, resolved or retained at this head

| Finding | Status at `92ad1687` | Evidence |
|---|---|---|
| R300-2 F4 MINOR (Tests, Conformance): U15 could not fail for a slew discard that counts toward, or triggers, the guard streak | **Closed** | See "R300-2 F4" below the table. |
| R300-2 F5 MINOR (Docs): the 1800 s basis was stale against the hosted measurement | **Closed** | See "R300-2 F5 and R301-2 S-B" below the table. |
| R301-2 S-B SUGGESTION (Docs): the same basis | **Addressed**, as scoped by assignment item 2 | The row and the Makefile pointer are in place. S-B's wider idea, a margin trigger specific to `mmcm_servo`, was not in the assignment and was not adopted. It stays optional. |
| R301-2 S-C SUGGESTION (Docs, Tests): the shadow and processor pin were missing from the `gmstep-mutants` triggers | **Addressed** | See "R301-2 S-C" below the table. |
| R301-2 S-A SUGGESTION (Tests): the tail oracle is one-sided | **Retained** as a SUGGESTION, outside this round by decision 5830332403 (#495) | It is the conservative direction. It does not affect coverage. |

### R300-2 F4: evidence

- `sim_main.cpp:559-562`: U15 now arms one guard trip and checks `before.size() == 1`.
- After arming, the slew window and its partial tail are both discarded (`:563-571`). The four gaps after that are graded at `:576-578`.
- One trip plus two tainted windows is odd, so no fixed per-discard increment can wrap the 2-bit streak back to 0.
- My R300-2 script `reviewer_mutants_r2.py` is byte-identical to the one I published (sha256 `4bc92fb3...b524`, `receipts/tool_identity.txt`). I ran it on the exact-head extraction:

  | Case | Verdict |
  |---|---|
  | `clean_unit` | CLEAN-PASS, 100/0 |
  | `slew_discard_extends_streak` | **KILLED** at U15 |
  | `slew_discard_counts_as_guard_trip` | **KILLED** at U15 |
  | `slew_streak_reset_removed` | KILLED at U15 |
  | `step_streak_reset_removed` | KILLED at U12 |

  Receipts: `receipts/mutants_r2/`, full harness output in `receipts/runlogs/mutants_r2/`.
- `slew_mutants.py:30-45` adds the two counting variants to `STREAK_MUTANTS`, with the same anchors and replacements as my probe. Each requires `[U15] four fresh guard trips precede re-base`. `:97-103` runs all three as unit cases.
- The author's campaign, graded by its own `run_case()` (`receipts/campaign/part_[a-d].log`), passes all 10 cases, and all four parts exit 0:
  - `clean` and `clean_unit` pass;
  - `discard_removed`, `level_tied_low` and `partial_tail_trusted` are each rejected by `[S1] overlapped window is discarded`;
  - `discard_not_counted` is rejected by `[S1] discards counted`;
  - `step_dedupe_removed` is rejected by `[S5] coincident step+slew window counted once`;
  - all three streak variants are rejected by the named U15 check.
- Beyond the named variants (`receipts/mutants_r3/`):
  - A `+2` per slew discard and a decrement per slew discard are both KILLED at U15. So the odd arming covers any fixed increment, not just `+1`.
  - A slew discard handled like a #539 step, which abandons the window and restarts the streak, is KILLED at U15. It is also KILLED by the slew suite at `[S2]` and `[S4]`.
  - The one survivor is recorded as S1 below.

### R300-2 F5 and R301-2 S-B: evidence

- `CI_WORKFLOWS.md:159` now reads: `mmcm_servo` | 1800 s | hosted window 1159.1 s; 640.9 s remains (35.6% of budget). That is the `milan_dp` row's form.
- `:171-176` cites head `b94f53cc` in merge `4bb4317`, run 36113401588, job 108001867446 (passed), and the window 08:33:57.4-08:53:16.4 UTC. The pending-acceptance sentence is gone.
- I checked this against that job's log from my R300-2 receipt. The window runs from `PASS crf_tx` at 08:33:57.3805 to `PASS mmcm_servo` at 08:53:16.4428, which is 1159.06 s. 1800 - 1159.1 = 640.9, and 640.9/1800 = 35.6%. All three figures match.
- `:158` keeps "every other default suite" at the original 548 s basis. That is still true, because `mmcm_servo` now has its own row. The budget itself, `scripts/run_all_suites.sh:247`, is unchanged.
- `Makefile:19-22` keeps the round-2 local figures, labels them "Shared-host local margin", and adds "Hosted budget basis: docs/testing/CI_WORKFLOWS.md, mmcm_servo row". This is what item 2 asked for.
- The exact head has since run on the hosted runner: `rtl-full` 36124312074, Verilator shard 2/5 job 108037083220, passed.
  - `mmcm_servo` took 862.9 s (`receipts/hosted_head_verilator_shard2_job_108037083220.log:265-266`).
  - That runner was faster: `ptp_ts` took 100.5 s here against 125.5 s in the sample behind the row.
  - The documented 1159.1 s therefore stays the worst case observed, which is the correct basis.

### R301-2 S-C: evidence

- `TESTING.md:267` now names `KL_gptp_shadow.sv` (`phc_adj_o` and the slew pass-through) and the `gptp-processor` pin as triggers.
- Both identifiers exist at this head: `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:144,150,685,748-749`.
- The trigger is appropriate. The connected gmstep leg carries the level and the addend from the real plane through the shadow. Its slew controls plant at the datapath consumer of that level (`gmstep_mutants.py:125-130`), so a shadow or pin change must re-prove them.

### The default target stays no slower than round 2

- **Author's measurement:** a clean two-CPU run took 936.448 s, against 952.797 s in round 2. Both used Verilator 5.052. The log ends with the exit and wall-clock line `EXIT: 0; WALL_SECONDS: 936.448` (`author-r3/timing-round3.log:422`).
- **My stage timings** at this head, with pinned 5.050 and one CPU per simulation (`receipts/servo_default/`):

  | Stage | Checks | Time at this head | Round-2 time |
  |---|---|---|---|
  | Unit | 100/0 | 30.4 s | 29.8 s |
  | Rails | 8/0 | 20.1 s | 19.6 s |
  | Step | 113/0 | 337.9 s | 338.0 s |
  | Slew | 90/0 | 344.4 s | 338.7 s |

  The differences are within the noise of a shared host. The only stimulus change is one fewer arming window in U15.
- **Hosted, exact head:** 862.9 s, as above.
- No check was trimmed, and the deadline is unchanged.

## Findings

### S1 SUGGESTION: Tests, Robustness. U15 cannot tell a streak restart that is limited to windows whose boundary is still slewing

- **Artifact:**
  - `tb/verilator/mmcm_servo/sim_main.cpp:555-580` (U15).
  - The contract it pins: `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:88-91,715`, "Slew discards reset the guard-discard streak".
- **Evidence:** reviewer mutant `slew_reset_only_while_level_high`, which rewrites `:715` to `if (slew_hit_w && phc_slew_q_r) disc_run_r <= '0;`.
  - It **SURVIVES** the unit harness, 100/0 (`receipts/mutants_r3/slew_reset_only_while_level_high.log`).
  - It **SURVIVES** the slew suite, 90/0 (`..._suite.log`).
  - In U15, the tail is the only discard whose boundary sample is clean. The streak is already 0 when the tail arrives, so its reset is redundant there.
  - With U15's slew replaced by a 1 ms pulse inside one window (`scripts/u15_short_pulse_probe.patch`), the clean RTL passes 99/0 and this mutant is **KILLED** at U15 (`receipts/u15_short_pulse/`).
- **Impact:** only small.
  - It affects only the diagnostic re-base path: an early re-base after a slew shorter than one window. Integrator, trim, LOCKED and the tally are not affected.
  - The producer's slew typically lasts about one 512 ms window or longer, so field exposure is limited to sub-window slews.
  - The two natural "count it" alternatives that F4 named are now pinned.
- **Optional outcome:** a U15 variant, or a second arming, with a sub-window pulse. The named control would be the level-gated reset.
- **Verification:** the mutant above is KILLED, and the clean RTL passes.

### S2 SUGGESTION: Docs. The campaign disposition text lists six defect classes, but there are eight

- **Artifact:** `scripts/measure_test_evidence.py:597-600`, the disposition for `slew_mutants.py`. It reads: "...omitted tally, boundary step double counting and a retained guard streak".
- **Evidence:**
  - Round 3 added two counting variants, which extend the streak or re-base on it. `TESTING.md:268,484` now says eight defects.
  - The disposition is descriptive: it carries no count, and the ratchet passes (`receipts/measure_test_evidence_check.log`). "A retained guard streak" can be read as covering both new variants.
- **Impact:** a cosmetic inventory mismatch in a tooling disposition. `TESTING.md` is the authority for the count, and it is correct.
- **Optional outcome:** name "a counted or retained guard streak" in the disposition, the next time that file is touched.

## Lens results (all applied at `92ad1687`)

```text
[R300] PASS Conformance - issue 545 comment 5830332403 items 1-3; sim_main.cpp:555-580; slew_mutants.py:30-45,97-103; CI_WORKFLOWS.md:158-176; Makefile:19-22; TESTING.md:267-268,484; git log/parentage b94f53cc..92ad1687; receipts/hosted_exact_head_runs.txt - each item checked against the assignment text: item 1 arms U15 with one trip, adds both named counting controls, and my unchanged script reports both KILLED; item 2 uses the hosted window in the milan_dp row form with run and job, and the Makefile says its margin is local; item 3 names both triggers; out-of-scope S-A untouched; no dev merge; #545 acceptance 1-2 are unchanged from R300-1/-2
[R300] PASS RTL - hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:495-500,709-721 at 92ad1687; empty `git diff b94f53cc..92ad1687 -- hdl` and unchanged gitlinks (gptp 5dce647a, pp 09f9bf38, verilog-axis 48ff7a7e); receipts/static_gates.log (lint_rtl 90 <= 90) - the product RTL is byte-identical to the head R300-2 covered, so its RTL analysis still applies; the streak and slew-hit lines were re-read against the stated rule
[R300] PASS Robustness - sim_main.cpp:555-580 (one-trip arming, slew plus tail, fresh-trip re-base) and receipts/mutants_r3, receipts/u15_short_pulse - the clean RTL follows the stated rule under one-trip, two-trip (R300-2) and sub-window-pulse arming; reset, saturation, step-in-slew and feature-off paths unchanged since R300-2; S1 recorded as SUGGESTION
[R300] PASS Tests - sim_main.cpp:555-580; slew_mutants.py; receipts/mutants_r2 (unchanged script: 2 counting variants KILLED, clean passes), receipts/campaign (10/10, each with its named rejection), receipts/servo_default (100/8/113/90), receipts/mutants_r3 (+2, decrement, step-like variants KILLED) - U15 can now fail for the defects it and the campaign claim; S1 recorded as SUGGESTION
[R300] PASS Docs - CI_WORKFLOWS.md:158-176 against job 108001867446 timestamps (1159.06 s) and the exact-head job 108037083220; Makefile:19-22; TESTING.md:267-268,484 against the parsed slew_mutants.py (8 defects + 2 controls) and KL_gptp_shadow.sv:144,150,748; measure_test_evidence --check PASS; doc style, doc paths, docs_check, diff --check exit 0; no em dash added in the round diff; hosted docs 36124311956 success - S2 recorded as SUGGESTION
```

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #545 acceptance 1-3; decisions 5828714628 and 5830332403 items 1-3; commit parentage and the file set; hosted exact-head contexts | R300-3 | `92ad1687d84ff077f872719b4f1df601f82064d2` |
| RTL | CLEAN | servo `:88-91,495-500,709-721`; empty `hdl` and gitlink diff since `b94f53cc`; lint ratchet | R300-3 | `92ad1687d84ff077f872719b4f1df601f82064d2` |
| Robustness | CLEAN (S1 suggestion only) | U15 at one-trip arming; sub-window-pulse probe; the round-3 mutant set | R300-3 | `92ad1687d84ff077f872719b4f1df601f82064d2` |
| Tests | CLEAN (S1 suggestion only) | `sim_main.cpp`, `slew_mutants.py`, the servo Makefile; the unchanged R300-2 script; the campaign 10/10; the default servo stages; the R300-3 mutants | R300-3 | `92ad1687d84ff077f872719b4f1df601f82064d2` |
| Docs | CLEAN (S2 suggestion only) | CI_WORKFLOWS, TESTING, Makefile header, `measure_test_evidence` dispositions and `--check`, doc gates, both hosted job logs | R300-3 | `92ad1687d84ff077f872719b4f1df601f82064d2` |

Lenses outside the round-3 files still rest on earlier coverage, which remains valid because nothing in their scope changed after `b94f53cc`:

- the connected `milan_dp` leg and `gmstep_mutants.py`;
- `sim_phc_step.cpp`;
- TIME_SYNC;
- the datapath, shadow and processor pin.

My exact-head rows above cover those artifacts by their unchanged bytes. The external R301-2 POSITIVE at `b94f53cc` is its own ledger, and I have not merged it into mine.

## Real limits

- **Stage timings:** my servo timings are per-stage runs on a shared 16-CPU host with load around 11-21, one CPU per simulation. They are not a controlled benchmark.
  - The build step reported about 5 s, which is consistent with a warm compiler cache. The simulation times are the meaningful part.
  - The author's 936.448 s used Verilator 5.052, not the 5.050 pin.
- **Campaign runs:** the explicit campaign ran as four foreground invocations of the author's own `run_case()`, not as one `make slew-mutants` process. The author's single-process run passed 10/10 (`author-r3/slew-mutants.log`).
- **Not run by me this round:**
  - the full parent, protocol-processor, gPTP, Yosys and builder banks;
  - the `milan_dp` legs and the connected campaign;
  - `crf_rx` and `gptp_shadow`;
  - area;
  - the xvlog, idiom, port-contract and naming gates;
  - act or Docker.

  None of their inputs changed in this round. I rely on the manager's source banks and the author's receipts for them.
- **Em-dash gate:** it cannot judge here, because the pinned renderer is absent (exit 2). The round diff adds no em dash, and the hosted `docs` context passed at this head.
- **Hosted state:** at my query (11:00:44Z), `rtl-fast`, `docs` and `elaborate` had succeeded at this head. `rtl-full` 36124312074 was still in progress: Verilator shards 0, 2, 3 and 4 and all Yosys shards had passed, and shard 1/5 was running. So the `verilator-suites` and `yosys-portability` aggregates had not yet reported. The manager owns hosted and act acceptance.
- **Final candidate:** the hosted runs build the PR merge onto live dev. That is not the manager's final candidate from source base `5b73d3f4` onto live dev `56918419`.
- **Hardware:** physical calibration was not run. Field skips are not hardware proof, and nothing here is bench evidence.
- **Clone:** my gate runs created an ignored `scripts/__pycache__/`, which I removed. After that the clone matches the head exactly: blob bytes, modes, index and the three gitlinks (`receipts/clone_integrity.txt`).

## Pending manager duties

- Complete hosted and act acceptance at this head. The `rtl-full` aggregates, `verilator-suites` and `yosys-portability`, were still pending when I queried.
- Build and validate the final current-dev candidate at the merge turn, from `5b73d3f4` onto live dev.
- Handle the #508 text-conflict round, which is already planned. Its head will un-cover the lenses whose scope it touches and needs re-review.
- Optionally disposition S1, S2 and R301-2 S-A (#495).
- Obtain maintainer authorization for the merge.

R300-3 FINISHED
