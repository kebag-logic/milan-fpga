# [A681c] #665 lane S2, round 3: the CPU cycle and latency budget (HANDOFF)

Status: **REVIEW READY**, 2026-10-26. Every R703-2 and R704-2 finding is fixed at its cause, with a check that fails on `cd3525c3`; both points, both arms, the SHUTDOWN arm and three controls are re-measured; both reviewers' probes were rerun unmodified. The measured rows still miss T_svc = 10 ms (owner decision D4: S2b follows).

- Head: `f887663852d118e810ef690c3dd5cf9fe2292588`, one commit on round 2's `cd3525c3ddcbdb5d78bf8fccdab354c468926997`. Subject `Grade the composed load's service, fan out at registration capacity and answer for the owed row's whole population (#665)`, no body, no trailers.
- Branch `665-s2-cpu-budget`, base `origin/dev-soft-core` `e76a755afc0536453161e3cd33f6f4d2dcd7641f` (verified with `git merge-base`; `dev-soft-core` has since moved to `9220f9b3`, and the lane is not rebased, as the brief forbids). The PR targets `dev-soft-core`.
- Remote `https://github.com/kebag-logic/milan-fpga.git` (verified). The only git command run inside a submodule was the prescribed `rev-parse --show-toplevel` check in `third_party/tsn-c-stack`, which was then read only (`acmp.h`, `acmp.c`).
- Assignment: issue #665 issuecomment-6420330377. Findings: R703-2 (PR #792 issuecomment-6420323457), R704-2 (issuecomment-6419144949). TAKEN: issuecomment-6420686784. REVIEW READY: issuecomment-6422362395 (its body is `REVIEW-READY-COMMENT.md`).
- Every change is under `tb/verilator/ctrl_service_budget/` (no new file). No shipping RTL, SoC, firmware, CI, workflow or doc file outside it changed; `sim_main.cpp`, `observe.vlt` and `build.py` are unchanged, so round 2's nine attested builds stay valid. Nothing pushed; no PR, issue or comment edited; no Vivado, bench or hardware.
- The commit was amended once before any push: a mutant that restores `cd3525c3`'s composed rule gained its `(earlier rule)` suffix. Every gate, the self-test and the head regrade below ran at the amended head.


## Contents

1. [Result](#1-result)
2. [Findings and their fixes](#2-findings-and-their-fixes)
3. [Changes, file:line and reason](#3-changes-fileline-and-reason)
4. [New checks, planted mutants and failing words](#4-new-checks-planted-mutants-and-failing-words)
5. [Gate table](#5-gate-table)
6. [Run history and reproducibility](#6-run-history-and-reproducibility)
7. [The reviewers' probes, rerun unmodified](#7-the-reviewers-probes-rerun-unmodified)
8. [Acceptance](#8-acceptance)
9. [Open items, risks and questions](#9-open-items-risks-and-questions)

## 1. Result

Every figure is a measured clock count on the shipping cacheless VexiiRiscv, CPU 50 MHz, bus 100 MHz. The tables are in the README (Results) and `receipts/report.md`; every probe is in `receipts/runs/<arm>/table.md` and the per-group JSON.

| Arm | Groups | Paths missing T_svc | Probe instances missing T_svc | Refusals |
|---|---:|---:|---:|---:|
| A 1x1 | 18 | 22 of 81 | 58 of 141 | 0 |
| A 8x8 | 17 | 60 of 129 | 102 of 182 | 0 |
| B 1x1 | 8 | 18 of 44 | 41 of 68 | 0 |
| B 8x8 | 8 | 36 of 68 | 60 of 92 | 0 |
| SHUTDOWN arm 1x1 / 8x8 | 2 / 2 | 0 of 1 / 0 of 2 | 0 of 2 / 0 of 3 | 0 |

| Figure | 1x1 | 8x8 |
|---|---|---|
| Composed maximum (a window that released its whole load), A and B | 740,260 cycles (14.81 ms), backlog | 1,392,016 (27.84 ms), backlog |
| Longest pass of a window that never released its load (A; a lower bound) | 1,565,803 (31.32 ms), backlog-adp | 2,209,308 (44.19 ms), backlog-adp-refill |
| Worst pass, A | 1,565,803 (31.32 ms), backlog-adp | 2,989,496 (59.79 ms), acmp-notk |
| Idle pass, A | 65,703 to 72,632 (1.31 to 1.45 ms) | 157,133 to 185,315 (3.14 to 3.71 ms) |
| SRP under the composed load, A (backlog-adp, backlog-adp-refill) | 0 of 32 records ever released, at least 567.95 to 628.32 ms | 0 of 32, at least 583.52 to 658.79 ms |
| SRP under the composed load where served (first / last record, worst) | 84.11 / 186.48 ms | 143.91 / 340.85 ms |
| SET_NAME fan-out at capacity (16 / 32 recipients) | 11.33 ms, 20,358 cycles a recipient | 20.68 / 22.98 ms, 20,486 |
| Other fan-outs at capacity (arm A) | 7.77 to 8.58 ms | 12.39 to 16.39 ms |
| BIND_RX -> GET_STREAM_INFO notice (arm B) | 14.80 ms | 25.79 / 28.92 ms, over the 24 ms ceiling |
| A response with 7 frames owed ahead (12 ACMP commands), A | 126.29 ms (bound 130.31), 7 owed responses 0x7380-0x7386 in order | 161.10 ms (170.62) |
| The four commands behind it | none answered (at least 363.98 ms) | 0x7390, 0x7392 at 176.52, 188.27 ms; 0x7391, 0x7393 never (at least 860.00 ms) |
| SHUTDOWN -> ENTITY_DEPARTING | 0.58 ms; 1 path, 2 instances | 0.58 / 1.17 ms; 2 paths, 3 instances |

Round 2 published the composed maximum at 31.32 / 44.19 ms: those passes ran in windows whose SRP load was never served, so they are now reported as lower bounds, and the worst pass column keeps them. The 8x8 idle range was 2.04 ms (A) and 0.14 ms (B) at the low end in round 2: both were the pass the script's end cuts short, now excluded, so idle passes are longer than published.

## 2. Findings and their fixes

| Finding | Fix (file:line at the head) | Check that fails on `cd3525c3` |
|---|---|---|
| R703-2 F1 (MAJOR): SRP's load never serviced in the headline groups, unreported | `grade.py:655` `releases` (each record's release by RX_TAIL), `:676` `unreleased`, `:686` `served`, `:695` `service`: every loaded channel's first and last record of the window, commit to the end of the releasing pass; a record never released is a measured row flagged `starved`, its time a lower bound, fitting neither T_svc nor the ceiling. `:742` `composed` returns `serviced` and `unreleased`; `run.py:60` `windows` and `table` list each window, and the README's composed maximum is taken only over windows that released their load. README Findings state `srp_mbx.c:441-451` and the TICK mechanism with its measured extent. | `a starved channel is reported by name, and its window is no composed maximum` (fixture with SRP's release deleted); mutants `service: a record never released is omitted`, `service: a window that left its load unreleased is the composed maximum (earlier rule)`, `service: a record's service ends at its release, not at its pass's end`, `tables: a starved instance is not its path's worst` |
| R703-2 F2 (MAJOR): fan-out with one registered controller | `scenario.py:483` `registrations` reads `AECP_REGISTRATIONS` from `aecp.h`; `:529` `aecp_fanout_groups` registers 16 controllers on every interface and sends, from an unregistered controller, every state-changing command the image notifies (SET_NAME, SET_CLOCK_SOURCE, SET_CONTROL identify on/off, REMOVE/ADD_AUDIO_MAPPINGS, SET_SAMPLING_RATE, LOCK_ENTITY acquire/release; with the answering arm SET_CONFIGURATION, SET_STREAM_INFO, output map edits and BIND_RX's GET_STREAM_INFO notice), each ending at the last of 16 / 32 recipients; `:490` `descriptor_value`, `:509` `map_edit` read the values from the image. `grade.py` `grade_probe` reports `fanout` (recipients, per-recipient cycles). The `aecp` group's SET_NAME is now its solicited response (`scenario.py:437`, script unchanged); the fixture's one-recipient fan-out has its own path (`:969`). | `the fan-out group registers the firmware's capacity, every registration a recipient` (capacity read from `aecp.h` by the self-test itself); mutant `notify: the fan-out registers one controller an interface (earlier rule)` |
| R704-2 F1 (MAJOR): owed row ACMP 8 of 12; coverage against the stimulus's declaration | `scenario.py:798` `OWED_AHEAD`, `:801` `owed_group`: seven owed, the probe, then the rest of the ACMP burst (four) behind it, each a tagged probe; `Probe.owed` (`:122`) and `grade.py:449` `owed_ahead` require exactly the seven owed responses, in order, ahead of the probe's. `grade.py:45` `LOAD_FRAME_BYTES`, `:615` `room`, `:621` `defined_load` derive every row's population from the contract alone; `:644` `check_load` compares the window with it, never with `Group.load`. `selftest.py:58` restates the defined loads; `:420` `stimulus` counts the real scenario's composed windows by decoding their frames. | `every composed window's stimulus is its defined load`, `every composed window declares its defined load`, `the defined loads, restated`, `a window short of its defined load is refused although it declares it`, `the owed row has seven responses owed ahead of its own`, `the responses owed ahead are checked` (four cases); mutants `composition: the backlog stimulus omits SRP`, `... omits MAAP`, `composition: the owed row omits the ACMP commands behind its input (earlier rule)`, `composition: the load is the stimulus's own declaration (earlier rule)`, `owed: the responses ahead are not checked`. R704-2's own plant (`probe_scenario_control.py`) now fails two named checks (it failed none at `cd3525c3`). |
| R703-2 F3 (MINOR): N6, N8, N10 escape | `selftest.py:369` `window_checks`: a synthetic window whose longest pass is neither first nor last, and a run whose worst pass is its last; `:189` a window against a defined load one record smaller | `the composed maximum is the window's longest pass, wherever it falls`, `the worst pass includes the run's last pass`, `a composed window that committed more than its load is refused`; R703-2's `review_mutants2.py`, unmodified: N6, N8, N10 CAUGHT (escaped at `cd3525c3`) |
| R704-2 F2 (MINOR): SHUTDOWN control a distinct path | `scenario.py:923` `path='adp.shutdown'` for both shutdown groups' probes | `a control instance is its functional path` (the real control, ADP and shutdown groups at one and two interfaces), `repeated instances of one path: one path, its worst instance, every miss`; mutant `tables: a control instance is its own path (earlier rule)`. S1 reports 1 path / 2 instances, S8 2 paths / 3 instances. |
| Found while re-measuring: ACMP drops the commands it cannot owe | `scenario.py:125` `Probe.may_drop`; `grade.py:438` `never_answered`: a command behind the owed input whose response never comes is a measured finding, `unanswered`, unbounded; `run.py:44` `verdict_word` NEVER ANSWERED. README Findings: `ACMP_OWED_MAX` = 8 (tsn-c-stack `acmp.h:164`, `acmp.c` `room()` busy drop) against the ring's 12. | `a command never answered is reported, unbounded, where it may be dropped`, `every command behind the owed input is a path that reports a drop`; mutant `owed: a command never answered fits` |
| Found while re-measuring: the idle minimum was the pass the script's end cuts | `grade.py:102` `Log.cut_idle`, `:171`, `:176`, `:794`: the run of idle passes flushed at the end is excluded | `the pass the script's end cuts is no idle pass`; mutant `passes: the pass the script's end cuts counts as idle (earlier rule)` |
| R703-2 RESIDUE R1-R5 | README: R1 the backlog paragraph states each row's own channel's records (ACMP 12, ADP 8 or 11); R2 the round-2 clause removed from the header and every `(d58c8e22)` suffix renamed `(earlier rule)`, with the docstring wording given; R3 the arm labels defined before the counts; R4 "at 8x8 each interface's instance is its own path"; R5 the full event ring at 8x8 explained | wording |
| R703-1 R-4 / R704-2 R1 | **Not applied**: `docs/testing/TESTING.md` is in the release lanes' file map; left for the residue checklist, as in round 2 | - |
| R703-2 S1-S3 | Not applied (optional): the refill leg's phase, `-B` for the build's child Python steps (`build.py`, which would invalidate every attested build), the cross-build identity note | - |

## 3. Changes, file:line and reason

| File:line | What | Reason |
|---|---|---|
| `grade.py:1-27` | docstring: the composition against `defined_load`, the service, the owed frames | each rule in one place, mutable by the self-test |
| `grade.py:39-48` | `CONTRACT`, `LOAD_FRAME_BYTES` (each load record's size from its clause), `COMPOSED_ROWS` | the defined load is derived from the contract, never from the stimulus (R704-2 F1) |
| `grade.py:100-102`, `:171`, `:176`, `:792-796` | `Log.cut_idle`; the run of idle passes the script's end flushes is no idle pass | the 8x8 idle minimum was that cut pass (found while re-measuring) |
| `grade.py:438` | `never_answered` | a command the core takes and drops is a measured, unbounded finding (found while re-measuring) |
| `grade.py:449` | `owed_ahead` | causal evidence for the seven responses ahead (R704-2 F1) |
| `grade.py:486-541` | `grade_probe`: `may_drop`; `fanout` (recipients, per-recipient cycles, robust to a missing commit); `owed_ahead` and its mismatch | R703-2 F2, R704-2 F1 |
| `grade.py:615-652` | `room`, `defined_load`, `check_load` against the defined load | R704-2 F1, R703-2 F3 (N8) |
| `grade.py:655-734` | `releases`, `unreleased`, `served`, `SERVICE_FAMILY`, `service` | R703-2 F1 |
| `grade.py:742-765` | `composed`: `serviced`, `unreleased`, `window_ms`; refuses a composed row with no window | R703-2 F1 |
| `grade.py:768-` | `grade`: the service rows join the probes | R703-2 F1 |
| `scenario.py:37-44` | docstring: the declaration is never trusted | R704-2 F1 |
| `scenario.py:119-125` | `Probe.owed`, `Probe.may_drop` | R704-2 F1; the dropped commands |
| `scenario.py:426-480` | `aecp_groups`: rows end at the solicited response; SET_NAME's wait keeps its notices (script byte-identical) | the fan-out moved to its capacity group (R703-2 F2) |
| `scenario.py:483-608` | `registrations`, `descriptor_value`, `map_edit`, `FANOUT_CONTROLLER`, `aecp_fanout_groups` | R703-2 F2 and the manager's "every other fan-out path" |
| `scenario.py:798-840` | `OWED_AHEAD`, `owed_group`: 12 ACMP, the four behind as tagged probes that may be dropped | R704-2 F1 |
| `scenario.py:904-926` | `shutdown_groups`: both groups' probes on path `adp.shutdown` | R704-2 F2 |
| `scenario.py:966-969` | the fixture's SET_NAME on its own path, one recipient | no sub-capacity instance on the capacity path (R703-2 F2) |
| `scenario.py:994-` | `all_groups` adds `aecp_fanout_groups` (the anchors R703-2's `fanout_full.py` edits are kept) | R703-2 F2 |
| `run.py:44-65` | `verdict_word` (STARVED, NEVER ANSWERED), `severity`, `windows` | R703-2 F1 |
| `run.py:67-85` | `paths`: a starved or unanswered instance is its path's worst | R703-2 F1 |
| `run.py:94-131` | `table`: lower-bound cells and the composed windows | R703-2 F1 |
| `run.py:196-217`, `:277-281` | `graded`: misses name a never released or never answered record; `results.json` gains `windows` | R703-2 F1 |
| `selftest.py:1-26` | docstring | the new families |
| `selftest.py:52-61` | `AT_ONCE`, `DEFINED` (restated), `FIRMWARE_AECP_H` | independent of the grader and the scenario (R704-2 F1, R703-2 F2) |
| `selftest.py:77-86` | `headline` pins `serviced` and `unreleased` | R703-2 F1 |
| `selftest.py:147-213` | fixture checks: a window short of its defined load though it declares it, one record too many, SRP starved; `refusal` | R704-2 F1, R703-2 F3 (N8), R703-2 F1 |
| `selftest.py:335-366` | a starved instance is its path's worst | R703-2 F1 |
| `selftest.py:369-407` | `window_checks`: longest pass wherever it falls, the run's last pass, the cut idle pass, the owed responses, the dropped command | R703-2 F3 (N6, N10), R704-2 F1 |
| `selftest.py:410-466` | `channel_of`, `stimulus`, `points`, `load_checks` | R704-2 F1 |
| `selftest.py:469-490` | `path_checks` | R704-2 F2 |
| `selftest.py:493-546` | `image_header` (a minimal generated AEM header), `fanout_checks` | R703-2 F2, portable |
| `selftest.py:635-638` | `checks` adds the four families | - |
| `selftest_mutants.py:1-100` | docstring "(earlier rule)" (R703-2-R2's wording); `_first_pass_only`, `_last_pass_dropped`, `_cut_pass_idle`, `_load_at_least`, `_load_declared`, `_starved_omitted`, `_offer_without`, `_control_own_path` | the new mutants |
| `selftest_mutants.py:249-332` | `MUTANTS`: six suffixes renamed `(earlier rule)`; sixteen new | R703-2-R2; section 4 |
| `oracle.json` | regenerated by `selftest.py --write-fixture` from round 2's raw `fixture` log: ten service rows added, `serviced` and `unreleased` pinned; `fixture.log` regenerated byte-identical (sha256 `8137bb36...`) | the fixture's window now pins its service |
| `README.md` | run (arm B's groups), markers (fan-out capacity, owed, may-drop, cut pass), defined load and service, every result table, the fan-out and service tables, Findings (SRP starvation, the ACMP drop, fan-out cost), self-test and mutant tables, Limits; RESIDUE R1-R5 | the corrected harness and figures |

## 4. New checks, planted mutants and failing words

`python3 -B tb/verilator/ctrl_service_budget/run.py --self-test`: 81 `PASS` lines (51 in round 2), 52 `MUTANT caught` (36), `self-test: 0 failures`, rc 0 (`receipts/gates/selftest.log`). A failing check prints `FAIL: <check>: <differing fields>`; an uncaught mutant prints `MUTANT ESCAPED: <mutant>` and fails the run.

| Planted mutant (new this round) | Failing check and words, as printed |
|---|---|
| composition: the composed maximum is the window's first pass | `fixture passes: worst pass and composed maximum (composed_passes 1 (pinned 3))`; R703-2's own N6 text plant fails `the composed maximum is the window's longest pass, wherever it falls: (100, 3, 5000)` |
| worst pass: the run's last pass is dropped | `the pass bound runs from the running pass at the bus ratio`; R703-2's N10 fails `the worst pass includes the run's last pass: (900, 3, 900)` |
| passes: the pass the script's end cuts counts as idle (earlier rule) | `the pass the script's end cuts is no idle pass ((50, 3000))` |
| composition: a window that committed more than its load is accepted | `a composed window that committed more than its load is refused (accepted)` |
| composition: the load is the stimulus's own declaration (earlier rule) | `a window short of its defined load is refused although it declares it` |
| composition: the backlog stimulus omits SRP | `every composed window's stimulus is its defined load (backlog@1 {'GM': 15, 'LINK': 1, 'adp': 8, 'aecp': 16, 'maap': 7, 'acmp': 12} (defined {... 'srp': 32 ...}))` |
| composition: the backlog stimulus omits MAAP | `every composed window's stimulus is its defined load (backlog@1 {... 'srp': 32, 'acmp': 12} (defined {... 'maap': 7 ...}))` |
| composition: the owed row omits the ACMP commands behind its input (earlier rule) | `every composed window's stimulus is its defined load (backlog-owed@1 {... 'acmp': 8} (defined {... 'acmp': 12 ...}))` |
| service: a record never released is omitted | `a starved channel is reported by name, and its window is no composed maximum (([], {'srp': 1}))` |
| service: a window that left its load unreleased is the composed maximum (earlier rule) | `a starved channel is reported by name, and its window is no composed maximum` |
| service: a record's service ends at its release, not at its pass's end | `fixture row fixture.service.adp.first.if0 (end_sys 33843440 (pinned 34638820), ...)` |
| owed: the responses ahead are not checked | `the responses owed ahead are checked: ['31'] ({'status': 'measured', ..., 'owed_ahead': ['31', '32']})` |
| owed: a command never answered fits | `a command never answered is reported, unbounded, where it may be dropped ([('measured', None, True, True), ...])` |
| notify: the fan-out registers one controller an interface (earlier rule) | `the fan-out group registers the firmware's capacity, every registration a recipient (1 interfaces, none: [1] registered, 9 fan-outs; ...)` |
| tables: a control instance is its own path (earlier rule) | `a control instance is its functional path (['control.discover.if0', 'control.shutdown.if0', ...])` |
| tables: a starved instance is not its path's worst | `a starved instance is its path's worst ({'probe': 'd.x.if0', ...})` |

The 36 round-2 mutants are all still caught (six renamed `(earlier rule)`); `notify: a missing recipient is not refused` is caught by its named check again, not by an exception (the per-recipient figure skips a missing commit). The full list, with the check that catches each, is the README's mutant table.

Full-harness controls, regraded at the head (`receipts/drivers/regrade-C-*.log`):

| Control | Plant | Failing words | Verdict |
|---|---|---|---|
| `--mutation slow-adp-rx` | 16,000-iteration spin before `adp_rx` | `BUDGET control.discover.if0: 24.614 ms over T_svc 10 ms` | `CONTROL slow-adp-rx caught`, rc 0 |
| `--variant shutdown-entry --mutation slow-adp-shutdown` | spin before disabling ADP | `BUDGET control.shutdown.if0: 24.903 ms over T_svc 10 ms` | `CONTROL slow-adp-shutdown caught`, rc 0 |
| `--cpu-regions as-built` | the generator gets the 224 KiB regions | `REFUSED boot-fault: ... TRAP ... 0 1 00006880` | `CONTROL as-built caught: an instruction access fault (cause 1)`, rc 0 |

## 5. Gate table

Every gate ran at the head `f887663852d118e810ef690c3dd5cf9fe2292588`, foreground and unpiped; logs in `receipts/gates/` with the rc on the last line (`HEAD.txt` names the head). The two Markdown gates ran with the pinned renderer environment (`tools/markdown/requirements.txt`).

| Gate | Command | rc |
|---|---|---:|
| Harness self-test | `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` (81 checks, 52 mutants caught) | 0 |
| BDD conformance (rtl-fast) | `cd tests && behave`: 14 features, 406 scenarios, 1,977 steps (full log kept out of the packet, sha256 in `behave.log`) | 0 |
| Docs wording and links | `python3 scripts/docs_check.py` | 0 |
| Doc cited paths | `python3 scripts/check_doc_paths.py` | 0 |
| Doc style, its self-test | `python3 scripts/check_doc_style.py`, `--selftest` | 0, 0 |
| Archive, its self-test | `python3 scripts/check_archive.py`, `--selftest` | 0, 0 |
| Em dash, its self-test | `python3 scripts/check_em_dash.py --base e76a755afc0536453161e3cd33f6f4d2dcd7641f` (607 added lines, 0 findings), `--selftest` | 0, 0 |
| Per-page contents | `python3 scripts/gen_toc.py --selftest`, `--verify-anchors`, `--check` | 0, 0, 0 |
| Python idiom, its self-test | `python3 scripts/check_py_idiom.py` (every ratchet held, 0 over-long lines, 0 eval/exec), `--selftest` | 0, 0 |
| C++ idiom, its self-test | `python3 scripts/check_cpp_idiom.py`, `--selftest` | 0, 0 |
| Hygiene | `python3 scripts/check_hygiene.py --check` | 0 |
| TODO ownership | `python3 scripts/check_todo_ownership.py` | 0 |
| SoC sources | `python3 scripts/check_soc_sources.py` | 0 |
| RTL source lists | `python3 scripts/check_rtl_source_lists.py` | 0 |
| Whitespace | `git diff --check e76a755a HEAD` | 0 |
| Regrade at the head, six arms and three controls | `scripts/regrade_r3.sh` on copies of every log: `results.json` and `table.md` byte-identical to the measuring regrade (`receipts/head-regrade/summary.txt`) | 0 each, 0 refusals |

The full serial sweep was not run: the lane changes only files under `tb/verilator/ctrl_service_budget/`, and no shared file, as the brief allows.

## 6. Run history and reproducibility

- **Builds.** Round 2's nine builds (A1, A8, B1, B8, S1, S8, C-slow, C-shutdown, C-asbuilt) still attest at the head (`build.reused` accepts each): this round changed no build input (`sim_main.cpp`, `observe.vlt`, `flash.hpp`, the firmware trees and the configs are unchanged). Their `build.json` are in `receipts/builds/`. Two fresh builds at the head (R704-2's build step, the pinned 5.050 simulator) reproduce the 1x1 and 8x8 ELFs (`d4c28047...`, `c89a1871...`) and ROM banks byte for byte.
- **What was simulated.** Of the 52 group scripts round 2 recorded, 50 are byte-identical at the head (`receipts/script-identity.txt`); their logs were regraded. `backlog-owed` changed (12 ACMP, the four behind tagged) and ran again at A1, A8, B1 and B8; `aecp-fanout` is new and ran at A1, A8, B1 and B8. The owed group ran twice: the first run (before the four behind became probes) showed only 8 (1x1) or 10 (8x8) of the 12 commands answered, which is how the ACMP drop was found; the second run, with the same frames and only tags and marks added, measured the main row to the cycle again (126.29163 / 161.10225 ms) and is the one used.
- **Fresh-build reproduction.** R704-2's campaign (`run_delta.py`) on the fresh builds ran `backlog`, `backlog-adp`, `backlog-adp-refill`, `backlog-owed` and `aecp` at both points: all ten logs and graded JSONs are byte-identical to this round's (`receipts/review-probes/R704-2-fresh-build-vs-measured.txt`), and its audit finds 5 of 5 exact matches per point.
- **Regrades.** Every arm and control was regraded at the head (`scripts/regrade_r3.sh`), then again from copies at the amended head: byte-identical.
- **Fixture.** `oracle.json` was regenerated through `selftest.py --write-fixture` from round 2's raw `fixture` log on the A1 build; `fixture.log` came back byte-identical, and regenerating again at the head changes nothing.
- **Disclosed corrections during the round.** A first launch lost a shell variable, so R704-2's native probe did not start; it was relaunched and ran to completion. The Python idiom gate refuses `exec` outside its inventory in `scripts/`, so the source-edit mutants were written as patches instead; R703-2's own text plants still run through its script.

## 7. The reviewers' probes, rerun unmodified

Every script is byte-identical to its published copy (`665s2-review-evidence` `03ee8f89`). Where a probe reads a fixed packet layout, this round's evidence was placed where it reads; nothing in a probe was edited. Outputs are in `receipts/review-probes/`.

| Probe | What it showed at the head |
|---|---|
| R703-2 `review_mutants2.py` (25 source mutants) | N6, N8 and N10 CAUGHT (escaped at `cd3525c3`); R1-R12, N1-N5, N7, N9, N13 caught; N11 and N12 escape as in round 2 |
| R703-2 `mutant_regrade2.py` on N11, N12, every group at both points | 0 published values change under either (N12 is equivalent: `fan_out` refuses first) |
| R703-2 `fanout_full.py` + `fanout_run.py` (16 controllers on every interface, a 17th sends SET_NAME) | 11.33241 ms at 1x1, 20.68273 ms at 8x8, `status measured`: the harness's own `aecp_fanout.set_name` rows, to the cycle |
| R703-2 `srp_service.py` on every backlog log | A1/A8 `backlog-adp`, `backlog-adp-refill`: no SRP release (the grader's never-released rows); elsewhere the first release after 59.68 to 127.91 ms and the last by 158.93 to 340.87 ms, matching the service rows |
| R703-2 `recompute.py` (independent of the grader) | every group's worst pass and composed maximum equal the grader's at both points (0 mismatches); clock pairs all 2:1, NOW_MS every 100,000 bus cycles; the owed row's wire bound 126.293 / 161.103 ms |
| R703-2 `population_fanout.py`, `drain.py` | the owed window commits ACMP 12, the four behind with 8 to 11 records ahead; per-pass releases per channel |
| R703-2 `stale_probe2.py` on copies of a fresh build | 15 cases, 0 wrong; `run.py --reuse-build` on the ROM plant rc 1 |
| R704-2 `get_public_receipts.py` | 444 published entries, 0 mismatches |
| R704-2 `prior-probes/run_review.py build` | fresh A1 and A8 builds, rc 0 |
| R704-2 `run_delta.py` | both campaigns rc 0, 0 refusals |
| R704-2 `probe_native_delta.py` | its twelve-command owed variant: 126.29163 / 161.10225 ms, the figures R704-2 published for it and the head's owed row; its four extra frames fill the ring, so the filter refuses the scenario's four tagged commands (`no start`) and the window still commits ACMP 12. The prior fan-out stimulus: 7.70397 ms. |
| R704-2 `probe_delta.py` | PASS; "Admission shortfalls: {}" (the owed row was ACMP 8 of 12 at `cd3525c3`) |
| R704-2 `probe_scenario_control.py` | omitting SRP from the backlog stimulus and its declaration now fails `every composed window's stimulus is its defined load` and `every composed window declares its defined load` (none at `cd3525c3`) |
| R704-2 `audit_receipts.py` (this round's receipts in its public slot) | 56 traces regraded identically; fresh matches 5/5 at each point; SHUTDOWN counts reported equal deduplicated: S1 1 path / 2 instances, S8 2 / 3 |
| R704-2 self-test under its wrapper | `self-test: 0 failures` |
| R704-2 `verify_identity.py` | not run: it verifies the reviewer's own checkout at `cd3525c3` (and walks the submodules with git), so it does not apply at this head |

## 8. Acceptance

| Item (round 3) | Status | Evidence |
|---|---|---|
| 1. SRP serviced and reported | met: SRP's receive latency under the load is a measured row in every composed window; where SRP is never released (arm A's bound-talker windows) the row reports it never released with its duration, and those windows do not set the composed maximum, which comes from windows that released their load | README "The load's service" and Passes; `a starved channel is reported by name...` |
| 2. Fan-out at registration capacity, SET_NAME and every other fan-out path, both points | met for every command-driven fan-out the image completes; the lock expiry (60 s) and counter pushes are not run (Limits) | README "Notification fan-out"; R703-2's probe reproduces SET_NAME |
| 3. The owed row's full population; independent coverage; omission fails a named check | met | README Backlog rows; `load_checks`; R704-2's plant fails two named checks |
| 4. Self-protection | met | N6, N8, N10 caught |
| 5. Path counting | met | S1 1/2, S8 2/3 |
| Re-measure at both points, replace the tables | met | section 1; README |
| Rerun both reviewers' probes unmodified | met, but `verify_identity.py` (not applicable) | section 7 |
| Rows within T_svc | **not met**: owner decision D4, S2b follows | section 1 |

So the PR body says "Relates to #665".

## 9. Open items, risks and questions

- **For the manager (new findings, measured and reported, not fixed here):** the ACMP core's owed capacity (`ACMP_OWED_MAX` = 8, tsn-c-stack) is below the ACMP ring's admitted burst (12), so commands are dropped under held egress; SRP starves while passes exceed the 10 ms TICK (`srp_mbx.c:441-451`); a notification costs 11,800 to 20,400 CPU cycles a recipient. Whether these become Issues or S2b scope is the manager's decision.
- **R-4 not applied** (`docs/testing/TESTING.md:518`, a release-lane file), as in round 2.
- **R703-2 S1-S3 not applied** (optional). S2 (`-B` for the build's child steps) would change `build.py`, an attested input of every build, and invalidate them.
- **N11 and N12 still escape** the self-test; 0 published values change under either at both points.
- **A composed window closes at its settle**; a record still unreleased is reported with a lower bound, not followed to its release (R703-2 saw none released 2.07 s after the load in arm A).
- **The fan-out group's first SET of a value** is the only notifying one for the sampling rate (one rate in the image) and the configuration, so those are measured on interface 0 only.
- **Round 2's composed maximum and 8x8 idle floor are superseded** (section 1): S2b's before-and-after figures should be taken from this head.
- Large logs (58 files over 200 KB) are listed in `receipts/MANIFEST.json` by sha256 and size; every group's graded JSON and `table.md` is kept. Host paths in receipts are replaced by role placeholders (`<checkout>`, `<scratch>`, `<litex>`, ...), with both digests recorded.
- The self-test is portable, but no CI job runs it (registering it is a CI change outside this lane). START_STREAMING remains unrun. Physical calibration NOT RUN; nothing here is hardware evidence.
