[R733] POSITIVE - exact head ac105b158bb740a65e0154305377fd4a7d0f6f87

# R733-2: internal cleared-context delta review of PR #811 (#665 S3)

Head `ac105b158bb740a65e0154305377fd4a7d0f6f87`, tree `10a286051e8aa59003bfac98cf4f7d5973d241f9`, base `dev-soft-core` `f4c9ad4f`. This round is a delta review over the round-1 head `99de3a02`: six commits (`18fa9a45`, `b8628704`, `07eba0fc`, `6987b8d8`, `7b308437`, `ac105b15`), 29 files, +361/-107. No HDL, synthesis or submodule gitlink changed (`git diff --stat 99de3a02..HEAD -- hdl syn protocol-processor gptp-processor` is empty).

**Verdict: POSITIVE.** All three round-1 findings are resolved at their cause:
- R734-1-F1 (MAJOR): the split boot driver now fails on the native model's own verdict.
- R733-1-F1 (MINOR): the console compare stops at the command's terminator, under a permanent AddressSanitizer test with a plant.
- R733-1-F2 (MINOR): the boot tests now kill both saved-state plants.

No BLOCKER, MAJOR or MINOR is open. Four RESIDUE items (wording only) and five SUGGESTIONs remain. All five lenses were applied, and every lens is CLEAN at this head.

## Reconstruction

I read the authorities in this order:
1. AGENTS.md, and CONTRIBUTING.md sections 3 and 6.
2. docs/README.md.
3. Issue #665: the body; the plan and decisions D0-D9 (issuecomment-6409738976); the S3 assignment (issuecomment-6493622258); the S3 takeover; and the S3 ruling on the round-2 STOP (issuecomment-6505997821, items 1-4).
4. The delta `git diff 99de3a02..HEAD` and its history.
5. The author's round-3 REVIEW READY (issue #665) and the published packet `review-evidence/665s3-r1/author-r3` at `06c6f5d9`.

I read the round-1 reviews only after my own pass over the delta and my own probes. Prior findings are resolved or retained below.

## Prior findings, at this head

| ID | Severity then | Status at `ac105b15` | Evidence |
|---|---|---|---|
| R734-1-F1 | MAJOR | **RESOLVED** | See (1) |
| R733-1-F1 | MINOR | **RESOLVED** | See (2) |
| R733-1-F2 | MINOR | **RESOLVED** | See (3) |
| R734-1-R1 / R733-1 R-1 | RESIDUE | Resolved for comments and docstrings. **Retained** for PR-added executable strings | R733-2-R1 |
| R733-1 R-2 | RESIDUE | Resolved. `ctrl_split_boot/README.md:101` drops "longer than any span here" | diff |
| R733-1 R-3 | RESIDUE | Resolved for the Simulation status and the CPU budget limit: PR body lines 32 and 142 state "split CPU 50 MHz, bus 100 MHz". Two new clockless figures are R733-2-R3 | PR body |
| R733-1 R-4 | RESIDUE | **Retained**. `sw/firmware/ctrl/plat/ctrl_plat.c:64-65` is unchanged | R733-2-R4 |
| R733-1 R-5 | RESIDUE | Resolved. The PR body's `c787a3ce` row names the six re-recorded files | PR body line 53 |
| R733-1 S-1, S-2, S-3 | SUGGESTION | **Retained**. Both escapes are re-confirmed at this head | R733-2-S1 to S3 |

### (1) R734-1-F1: the native model's verdict

The fix is in `tb/verilator/ctrl_split_boot/run.py`:
- `point()` deletes any stale `sim.status` before the run, then writes the model's return code (`:343-359`).
- `grade()` begins with `native()` (`:248-269`). That adds a NATIVE finding in five cases: a missing or unparseable saved status; a nonzero status; no tally, or a tally of nothing (`suite_tally.is_nocount`); an unparsed tally line; or a failure reported by `suite_tally.log_reports_failure`.
- A regrade reads the same saved status (`saved_status()`, `:335-340`).
- `sim_main.cpp:236-256` returns `check.report()`, and its exception path both prints `FAIL:` and fails a check. So the tally and the exit status are each a complete signal.

I checked it with my own probes and the round-1 probe:
- **Probe 1** (`scripts/native_probe.py`, `receipts/native_probe.log`): the head's own `native_controls()` gives 6 of 6 as required, on the run and on the regrade.
- **Probe 2**: three reviewer controls through the same stand-in and grade, each as required:
  - a model exiting 245 (as a killed process would) with no tally: NATIVE on the run and the regrade;
  - a saved status that is not a number: PASS on the run, NATIVE on the regrade;
  - an unparseable tally (`failures: x`): NATIVE on both.
- **Probe 3**: six disposable copies of `run.py`, each with one part of the NATIVE check removed. Each is killed by at least one shipped native control. With the status check removed, `native-exits-nonzero` kills it. The others:

  | Part removed | Killed by |
  |---|---|
  | the missing-status check | `native-status-not-saved` |
  | the no-tally check | `native-incomplete` |
  | the failure check | `native-tally-failed` |
  | the saved status read as 0 | two controls |
  | the status never written | two controls |

  So every part of the check is protected by its own control.
- **The round-1 probe** (`scripts/r734_1_probe_boot_exit.py`, unchanged, run at this head): the native exit 0 passes, normal and regrade (gate exit 0). The native exit 1 with a failed tally gives gate exit 1, normal and regrade. It ends `DEFECT REJECTED`, rc 0 (`receipts/r734_1_probe_boot_exit.log`).

The positive boot points and the existing boot plants rest on the author's published receipts. They are hash-verified (see Evidence) and come from a clean clone at this head (`clone-boot.txt`: 0 changed paths, the same gitlinks as mine). All figures are simulated time, with the split CPU at 50 MHz and the bus at 100 MHz:

| Run | NATIVE | Result |
|---|---|---|
| 1x1, one interface | exit status 0; tally `checks: 1   failures: 0`; `sim.status` = `0` | BOOT ready at bus cycle 8,438,300 = 4,219,150 CPU cycles = 84.383 ms, against 20,000 ms; `PASS (0 finding(s))`; the regrade equals it |
| 8x8, one interface | exit status 0; `sim.status` = `0` | `PASS (0 finding(s))`; ready at 184.647 ms = 9,232,360 CPU cycles; the regrade equals it |
| `--native-controls` | 6 of 6 as required | |
| `--self-test` | 6 of 6 native controls | `csr-write-skipped` caught as TRACE, run completed; `console-blocks` caught as UART (742.670 / 6.315 / 701.970 ms, run completed); 2 of 2 |

The cycle counts are consistent with the clocks: 4,219,150 / 50 MHz = 84.383 ms, and 8,438,300 / 100 MHz = 84.383 ms.

The NATIVE check also exposed a real defect in the old `console-blocks` plant: it spun before all three commands, about 2.1 s, so the run passed the 2 s limit and the model failed. `7b308437` corrects it. The plant now spins only inside `milan_status`'s branch (`run.py:91-94`), and `self_test()` counts a plant as caught only in a completed run (`:409-424`).

### (2) R733-1-F1: the console's compare

`sw/firmware/ctrl/plat/ctrl_plat_console.c:132-138` now loops `while (n < c->len && command[n] != '\0' && command[n] == c->line[n])`, so `command` is never read past its terminator. The return still requires `n == c->len && command[n] == '\0'`, so an exact match is unchanged and the K3 prefix and extension refusals still hold. K3 sends `milan_status\0XYZ\r` and `milan_gettime\0\r` (`test_plat.cpp:160-164`). The second also covers the old read in the return expression.

`plat_arms.py:39-50` builds the CSR window, the console and `test_plat` with AddressSanitizer and `abort_on_error=1`, graded by the same `fw_gtest.run_binary`/`grade()` that `execute()` uses. The MMIO platform stays unsanitised, for the reason stated in the docstring. Coverage moves to 119/119 lines and 68/68 branches. The two new branches are the NUL case, which the K3 lines exercise.

Probe results (`scripts/plat_probe.py`, `receipts/plat_probe*.log`; round-1 C probe, `receipts/r733_1_console_*`):

| Probe | Result |
|---|---|
| The head's arms | `plat` PASS (2 tests); `platboot1` and `platboot2` PASS (10 tests each) |
| Shipped `plat-command-read-past-its-end` | caught by `Plat.K3LinesEndOnceAndOthersAreRefused`: `crashed on signal 6` |
| Reviewer `probe-compare-one-past` (a different over-read) | caught by K3, `crashed on signal 6` |
| Both, with the sanitizer withheld | both ESCAPE, rc 0 (`receipts/plat_probe_noasan.log`): the sanitizer is what catches them, as the plant's comment claims |
| Round-1 `r733_console_nul.c`, at the head | 0 sanitizer reports; the line refused (`commands 0 refused 1`) |
| The same, with the fix reverted | `global-buffer-overflow ... console_revert.c:135 in is` |
| Widest `milan_status` response at this head | 309 B, against `CTRL_PLAT_RESPONSE_MAX` 320 |

### (3) R733-1-F2: the saved state's place and its write-back

`test_plat_boot.cpp` wraps F1's flash model in a port that stamps every read, program and erase with the mailbox's access count (`:80-97`, bound at `:155-157`). There are two new checks:
- **B1** (`:208-214`) requires a flash access, and requires that every flash access precede the mailbox's first access. It also requires a BLANK terminal.
- **B10** (`:378-402`) binds sink 0 with `BIND_RX_COMMAND` through the mailbox model after READY. It then steps the loop at 10 ms of both clocks per pass, and requires exactly one more commit and more flash programs.

Probe results (`receipts/plat_probe.log`):

| Probe | Result |
|---|---|
| Shipped `plat-saved-state-after-mailbox-open` | caught by B1 on its own words |
| Shipped `plat-store-service-unbound` | caught by B10 on its own words (2 checks) |
| Reviewer `probe-saved-state-never-read` | caught by B1 (the boot no longer reaches READY; 6 checks) |
| Round-1 campaign, `scripts/r733_plat_campaign_at40.py` | 15 of 17 compiling probes caught; both former F-2 escapes now `[ok]` (`receipts/r733_1_probes_member*.log`) |
| Round-1 campaign, the 2 remaining escapes | `r733-tod-no-snapshot-wait` and `r733-response-max-too-small`, the round-1 suggestions S-1/S-2, carried as R733-2-S1/S2 |
| Round-1 campaign, `r733-window-read-any-interface` | does not compile (`-Werror=unused-parameter`), as at round 1, and is discarded |

The campaign script is the round-1 script with one change: its assertion of 37 shipped defects is raised to this head's 40 (`plat_mutants.py`: 40, three of them new).

`B10` cites Milan v1.2 5.5.2.4, which `REQUIREMENTS.md:430` names as the Controller Bind authority. That is consistent with the tree's other uses.

## Findings of this round

None is a BLOCKER, MAJOR or MINOR.

### R733-2-R1: RESIDUE, Docs. Lane labels and ruling IDs in PR-added executable strings (carries R733-1 R-1's string part)

- **Where:**
  - `sw/litex/ctrl_memory.py:218-220`: the `platform-8x8-two-interfaces` `Ledgered` reason `"lane S14, the hybrid XIP (#665 decision D3: ... ruling 6505997821, amending 6425357821 for this image)"`, added by `2adab625`.
  - `sw/firmware/ctrl/test/ctrl_configs.py:167, 169, 171, 234`: `"(#665 S3)"` in four reason strings, added by `f4a839eb`. The fixture's entry at `ctrl_memory.py:214-215` predates the base and is #746's.
- **Authority:** the owner's comment rule of 2026-10-15. The author deliberately left executable strings unchanged, and R734-1-R1 excluded them, so I record them as wording rather than as an unresolved finding. They change no verdict, measurement or figure.
- **Exact fix:**
  - At `ctrl_memory.py:218-220`, change the reason to `"the hybrid XIP (#665 decision D3: the boot and the CSR policy are cold code; #665's documented memory exception for this image)"`.
  - At `ctrl_configs.py:167, 169, 171, 234`, replace `(#665 S3` with `(#665`.
  - Re-run `test_ctrl_memory.py` and the boundary gate, since the strings are compared or printed there.

### R733-2-R2: RESIDUE, Docs. The run docstring says a missing status is refused

- **Where:** `tb/verilator/ctrl_split_boot/run.py:17-18`, "a regrade reads the same saved status, and refuses a run that saved none".
- **Evidence:** the code makes it a NATIVE finding, exit 1 (`native()`, `:254-255`; my probe 2's garbage status and the shipped `native-status-not-saved` control). "Refused" is exit 2 in the same docstring. The README (`:63`) correctly says "is a finding".
- **Exact fix:** "a regrade reads the same saved status, and a run that saved none is a NATIVE finding".

### R733-2-R3: RESIDUE, Docs. Timing figures that state no CPU clock

- **Where:**
  - `tb/verilator/ctrl_split_boot/README.md:68`: "spins 700,000 turns, about 0.7 s".
  - `run.py:86-89`: "about 0.7 s, each turn ... about 1 us".
  - PR body line 21: "about 2.1 s".
  - PR body line 50: "spins about 0.7 s".
- **Evidence:** the product split runs the CPU at 50 MHz and the bus at 100 MHz. The spin's duration depends on the CPU clock. The measured span is 742.670 ms at the 50 MHz CPU (self-test receipt).
- **Exact fix:** append "at the 50 MHz CPU" to each figure. For example: "about 0.7 s at the 50 MHz CPU (742.670 ms measured), each turn about 1 us". The 2 s simulated-time limit needs no clock.

### R733-2-R4: RESIDUE, Docs. R733-1 R-4, retained

- **Where:** `sw/firmware/ctrl/plat/ctrl_plat.c:64-65`, "so no source reports an address the window does not hold".
- **Evidence:** at two interfaces, interface 1's sources report a range with no window (B8 asserts it, `test_plat_boot.cpp:350-354`).
- **Exact fix:** "so no interface-0 source reports an address the window does not hold; interface 1 has no window (ctrl_plat.h)".

### R733-2-S1: SUGGESTION, Tests. R733-1 S-1, retained

No test bounds the widest `milan_status` by `CTRL_PLAT_RESPONSE_MAX`. `r733-response-max-too-small` (320 to 200) still escapes at this head with rc 0. The constant itself is correct: the widest response is 309 B. Add a test that formats the all-ones status and asserts it fits.

### R733-2-S2: SUGGESTION, Tests and Robustness. R733-1 S-2, retained

`CTRL_PLAT_SNAPSHOT_SPIN` cannot be observed on the host. `r733-tod-no-snapshot-wait` still escapes. The bench lane should confirm the wait on hardware.

### R733-2-S3: SUGGESTION, Conformance. R733-1 S-3, retained

The policy write mirroring `configure_fabric()` sets `MAAP_CTRL[0]` briefly, until MAAP's one-owner report clears it. Record this in `plat/README.md` step 3, and take it to S6/S12 for a ruling.

### R733-2-S4: SUGGESTION, Tests

`native()` reads the tally and `[FAIL]` markers. A bare `FAIL:` line under a passing tally and exit 0 would pass. `sim_main.cpp` cannot produce that, since its catch block prints `FAIL:` and fails a check, so this is not a defect. Counting `FAIL:` lines as a NATIVE finding would also make the check independent of that coupling.

### R733-2-S5: SUGGESTION, Tests

B1 proves the saved state's place only against a blank flash (terminal BLANK). A restored binding visible before the mailbox opens is S4's valid-slot case. When S4 lands, a B1 variant with a valid slot would make the order check observable as well as positional.

## Lens coverage at this head

| Lens | Result | Artifact | What was checked, against what |
|---|---|---|---|
| Conformance | PASS | `run.py:248-359`, `sim_main.cpp:236-256`; `test_plat_boot.cpp:208-214, 378-402`; `ctrl_plat.c` step order; `docs/design/SPLIT_CONTROL_MEMORY.md` section 5 table | S3 acceptance (a boot to ready, graded UART, the CSR trace) now requires the native model's own pass; Milan v1.2 5.6.1 steps 6-7 before the open, and 5.5.2.4 write-back, against `ARCHITECTURE_HW_SW_SPLIT.md` section 2; the S3 ruling item 1 (59.0 at one point, the others within 56: 39.0 / 42.0 / 52.0 / 59.0, the tiles unchanged); the by-part table re-summed to the stated totals at all four points (+5,112/+896, +5,168/+944, +5,136/+912, +5,224/+928) |
| RTL | PASS | `ctrl_plat_console.c:132-138` (indexing); `plat_arms.py:39-50`; empty `git diff --stat 99de3a02..HEAD -- hdl syn` and the submodules | Bounds of `is()`, both loop and return, against C11 6.5.6 and the portable-C rule; no HDL, CDC, clock or gitlink change; firmware ROM +8 B, tiles unchanged |
| Robustness | PASS | K3 NUL lines; ASan arm; NATIVE paths for killed, nonzero, no-tally, unparseable, missing and garbage status; probes 2-3 | Malformed UART input, and failure or incomplete paths of the native run, normal and regrade |
| Tests | PASS | 40 shipped platform defects (3 new, each caught on its own words in my probe and in the author's shards); 6 native controls; 6 control-removal mutants killed; round-1 campaign 15 of 17 compiling probes; `fw_coverage` receipt (35 files, console 119/119 and 68/68) | AGENTS section 6, Tests: each new test fails for the defect it claims; the sanitizer is shown necessary |
| Docs | PASS (residue R1-R4 only) | `plat/README.md:72, 103-109`; `ctrl_split_boot/README.md:12, 25-35, 63-79, 101`; `SPLIT_CONTROL_MEMORY.md:215-251`; PR body | Behaviour, counts (40 defects, B10) and figures against the code and the receipts; the clocks stated on the boot figures; the author's 97 docs gates (receipts); wording items recorded as RESIDUE |

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `run.py` NATIVE and plant changes, `sim_main.cpp` exit path, B1/B10 against 5.6.1 and 5.5.2.4, memory section 5 against the S3 ruling | R733-2 | `ac105b158bb740a65e0154305377fd4a7d0f6f87` |
| RTL | CLEAN | `ctrl_plat_console.c` `is()` indexing, `plat_arms.py` sanitizer build, no HDL/gitlink change | R733-2 | `ac105b158bb740a65e0154305377fd4a7d0f6f87` |
| Robustness | CLEAN | NUL input under ASan, native failure and regrade paths (my probes 1-3, R734-1 probe) | R733-2 | `ac105b158bb740a65e0154305377fd4a7d0f6f87` |
| Tests | CLEAN | 3 new plants, 2 reviewer plants and the sanitizer-withheld pair; 6 native controls and 6 cuts; round-1 18-probe campaign; head arms; author shards and coverage receipts | R733-2 | `ac105b158bb740a65e0154305377fd4a7d0f6f87` |
| Docs | CLEAN (RESIDUE R733-2-R1 to R4) | plat README, split boot README, `SPLIT_CONTROL_MEMORY.md` section 5, PR body, new comments in the delta | R733-2 | `ac105b158bb740a65e0154305377fd4a7d0f6f87` |

The code the delta does not touch keeps its round-1 lens results. Those were Conformance clean and RTL clean apart from F-1, which is now resolved. The delta changes nothing those results depend on: the firmware outside `ctrl_plat_console.c` is byte-identical since `b8628704` apart from the README, and the author's ELF digests are identical to `6987b8d8`'s.

## Evidence

- **Author packet:** `review-evidence/665s3-r1/author-r3` at `06c6f5d97328e8c4c684314df156d02637224341`. I fetched 27 receipts:
  - boot, regrades, `sim.status`, native controls, self-test;
  - the four self-test shards;
  - coverage, builder, memory and docs summary;
  - the round-1 probe re-runs and the residue scan.

  Each matches its `published_sha256` in `MANIFEST.json` (27 ok, 0 bad, 0 missing; `receipts/evidence_manifest_check.txt`). The publish commit is not GPG-signed (GitHub `verified: false`, `unsigned`), so integrity rests on the manifest hashes and the commit id.
- **Author source-head gates** (receipts, not re-run): firmware self-test, four shards, each `HEAD ac105b15`, rc 0. The control campaign catches 568 of 568, the 40 platform defects among them; the shards log `[ok]` for the three new defects. `fw_coverage` PASS. The split boot at 1x1 and 8x8, regrades, `--native-controls` and `--self-test`, all rc 0.
- **My runs** (host only; no LiteX or RV32 build):
  - `native_probe.py`: PASS.
  - `plat_probe.py`: 6 of 6 as required.
  - `plat_probe.py --no-asan`: 2 of 2 as required.
  - Round-1 campaign, three members: 15 caught of 17 compiling, the 2 known escapes.
  - R734-1 probe: `DEFECT REJECTED`.
  - Round-1 console C probes: clean at the head; overflow on the revert.
- **Checkout integrity after the probes** (`receipts/checkout_integrity.txt`):
  - HEAD and tree as above; `git status --porcelain --ignored` empty.
  - Every one of 1,490 tracked files hashes to its index blob, and index mode/blob/path equals the HEAD tree.
  - Gitlinks: gptp-processor `55680bff`, protocol-processor `ed211803`, lwSRP `08ee86e8`, tsn-c-stack `70936b77`, verilog-axis `48ff7a7e`, each at its pin and clean. `external` (`efeb541a`) is uninitialised, as in the author's clone record.
- **Hosted contexts at this head** (snapshot 2026-10-30T00:11Z, `receipts/hosted_snapshot.txt`): 2 success, 1 skipped, 5 in progress, 25 queued. Nothing is concluded from them.

## Real limits

- I did not run the split boot simulation, the CPU budget harness, `test_builder`, `ctrl_boundary`, the full firmware self-test, the AECP/SRP campaigns, the docs gates or `behave`. Those results rest on the author's hash-verified receipts at this head.
- My boot, console and native evidence is host-side: GoogleTest arms through the campaign's own code, the native grader through its stand-in, and C probes under the sanitizer.
- The simulation has no datapath, and its flash is blank. The UART has no baud rate.
- Physical calibration was NOT RUN, and field skips are not hardware proof.
- No manager source bank exists at this head, and none is claimed or inferred.
- Source validation here is distinct from the current-dev merge candidate (source base `f4c9ad4f`, live dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`).

## Pending manager duties

- Hosted and act acceptance at the exact head. Most hosted contexts were still queued at the snapshot.
- The current-dev merge candidate, with its builder and native banks, at the merge turn, and its receipts on the PR.
- Carrying R733-2-R1 to R4 to the residue checklist.
- Routing the suggestions: S2 and S3 to S12/S6, and S5 to S4.
- The ruled limits, which stay as stated in the PR body: the graders' split mode owed to S12; SRP live configuration deferred; the split boot a recipe until #784 step 2; the 8x8 two-interface image ledgered at 59.0, owed to D3's hybrid XIP.

R733-2 FINISHED
