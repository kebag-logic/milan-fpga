# [A308] Round 3 handoff

All assigned local gates completed with exit 0.

Head: `92ad1687d84ff077f872719b4f1df601f82064d2`
Branch: `545-crf-servo-slew`
Initial head: `b94f53cc4e5dbfd9527ba666922a55804515165c`

No RTL logic, donor file or submodule pin changed. No dev merge, push, PR edit, additional implementation checkout or hardware operation was performed.

## Public scope

- [Round 3 assignment](https://github.com/kebag-logic/milan-fpga/issues/545#issuecomment-5830332403), items 1-3.
- [Round 2 decision](https://github.com/kebag-logic/milan-fpga/issues/545#issuecomment-5828714628).
- [Reviewer R300-2](https://github.com/kebag-logic/milan-fpga/pull/563#issuecomment-5830329665): F4 and F5.
- [Reviewer R301-2](https://github.com/kebag-logic/milan-fpga/pull/563#issuecomment-5830312313): S-B and S-C. The conservative release-tail observation S-A remains out of scope under #495.

## Changes

| File:line | Change |
|---|---|
| `tb/verilator/mmcm_servo/sim_main.cpp:559` | U15 arms one guard trip. Two tainted windows cannot wrap a wrongly counted four-trip streak to zero. All six U15 checks remain. |
| `tb/verilator/mmcm_servo/slew_mutants.py:30` | Added increment and guard-like re-base variants; all three streak controls require the named U15 rejection. Eight defects plus two positive controls. |
| `tb/verilator/mmcm_servo/Makefile:19` | Labels the round-2 margin as local and points to the hosted budget basis. Default recipe and deadline unchanged. |
| `docs/testing/CI_WORKFLOWS.md:159` | Hosted 1159.1 s window, 640.9 s remaining (35.6%), exact head, run and job. Removes pending-acceptance wording. |
| `docs/testing/TESTING.md:267` | Adds shadow addend/slew pass-through and processor pin triggers; campaign table and suite index at line 484 both count eight defects. |

Commits:

- `b46bbcfbbb050bc340f1716638f40402ec87a492 Pin slew guard streak counting controls and hosted budget`
- `92ad1687d84ff077f872719b4f1df601f82064d2 Keep the servo suite index control count current`

## Wall clock

Clean build: `make -C tb/verilator/mmcm_servo clean`, then `taskset -c 8,9 make -C tb/verilator/mmcm_servo`.
**936.448 s**, exit 0; round 2 was **952.797 s**. This run is 16.349 s faster and leaves 863.552 s (48.0%) of the unchanged 1800 s budget. Both local rounds used Verilator 5.052 on the shared host; this is local evidence, separate from the hosted basis. See [timing-round3.log](timing-round3.log).
Counts remain 100 unit, 8 rails, 113 step and 90 slew checks, all passing. The later suite-index commit changes no test input; blob equality is recorded in [reviewer-script-identity.txt](reviewer-script-identity.txt).

## Servo control table

| Control | Named failure required | Result |
|---|---|---|
| `clean` | Positive control | PASS, rc 0 |
| `clean_unit` | Positive control | PASS, rc 0 |
| `discard_removed` | `[S1] overlapped window is discarded` | KILLED, rc 1 |
| `level_tied_low` | `[S1] overlapped window is discarded` | KILLED, rc 1 |
| `partial_tail_trusted` | `[S1] overlapped window is discarded` | KILLED, rc 1 |
| `discard_not_counted` | `[S1] discards counted` | KILLED, rc 1 |
| `step_dedupe_removed` | `[S5] coincident step+slew window counted once` | KILLED, rc 1 |
| `slew_streak_reset_removed` | `[U15] four fresh guard trips precede re-base` | KILLED, rc 1 |
| `slew_discard_extends_streak` | `[U15] four fresh guard trips precede re-base` | KILLED, rc 1 |
| `slew_discard_counts_as_guard_trip` | `[U15] four fresh guard trips precede re-base` | KILLED, rc 1 |

## Unchanged reviewer script

Fetched read-only from evidence revision `895db803af16caa683b40666a1b37d77b6cc76e4`, path `review-evidence/545-r1/reviews/R300-2/scripts/reviewer_mutants_r2.py`. Every case ran without modifying the script. The temporary bare fetch, reports, scripts, probes and builds were deleted. Its SHA256 and the identical tested-input blobs are in [reviewer-script-identity.txt](reviewer-script-identity.txt).

| Case | Named failure | Verdict |
|---|---|---|
| `clean_unit` | None; 100/0 | CLEAN-PASS, rc 0 |
| `slew_discard_extends_streak` | U15 four fresh guard trips precede re-base | KILLED, rc 1 |
| `slew_streak_reset_removed` | U15 four fresh guard trips precede re-base | KILLED, rc 1 |
| `slew_discard_counts_as_guard_trip` | U15 four fresh guard trips precede re-base | KILLED, rc 1 |
| `step_streak_reset_removed` | U12 first three guard gaps and fourth-trip re-base gap | KILLED, rc 1 |

All five probe invocations returned 0; the four rc 1 values above are the expected mutant harness exits. No compilation failure was counted as a kill. Individual `reviewer-*.log` files retain every verdict, and `reviewer-*.run.log` retain full harness output.

## Connected control table

| Control | Named failure | Result |
|---|---|---|
| the policy level is tied low at the servo | `slew path: the actual servo receives the level` | KILLED by named check |
| the policy level omits the applied-rate tail | `slew path: every staged sample covers the PHC tail` | KILLED by named check |
| the policy level misses an extra addend stage | `slew path: every staged sample covers the PHC tail` | KILLED by named check |
| the step does not toggle mr | `restart: the outgoing mr toggles exactly once` | KILLED by named check |
| the grandmaster identity re-bases the render stage as well as the step | `render: the GM change is one counted re-base event` | KILLED by named check |
| the step does not re-centre the render stage | `render: the GM change is one counted re-base event` | KILLED by named check |
| the render re-base is keyed to the identity, not the step | `render: every counted re-base lands at a PDU end right after the step` | KILLED by named check |
| tu reaches the talkers four cycles late | `tu: set in the first cycle the bank names GM B` | KILLED by named check |
| the plane's step does not re-arm the holdover | `tu: held at least the 0.25 s holdover after the step` | KILLED by named check |
| tu stops the talker | `licence: the talker never pauses beyond four of its intervals` | KILLED by named check |
| the grandmaster change stops the talker for good | `licence: the talker never pauses beyond four of its intervals` | KILLED by named check |
| the step's re-centre snaps one event off the setpoint | `render: every PDU push leaves the target fill across the event` | KILLED by named check |
| a software settime does not toggle mr | `CLKV: the settime toggled mr once more (#387)` | KILLED by named check |
| the step's mr toggle is gated by the CRF clock-source selection | `CLKV: its mr toggled once per PHC step issued so far (#387)` | KILLED by named check |

Both clean connected controls pass; 16/16 campaign checks, including 14 named defects.

## Gate table

Every command ran in the foreground, without piping its exit through another command. Individual logs record exact commands, exits and wall clocks. Simulation builds use only the assigned worktree or campaign-owned temporary inputs. See [GATE-TABLE.md](GATE-TABLE.md) and [gates.jsonl](gates.jsonl).

| Gate | Exit | Evidence |
|---|---:|---|
| `timing-round3` | 0 | [timing-round3.log](timing-round3.log) |
| `slew-mutants` | 0 | [slew-mutants.log](slew-mutants.log) |
| `crf-rx` | 0 | [crf-rx.log](crf-rx.log) |
| `gptp-shadow` | 0 | [gptp-shadow.log](gptp-shadow.log) |
| `gmstep-mutants` | 0 | [gmstep-mutants.log](gmstep-mutants.log) |
| `builder` | 0 | [builder.log](builder.log) |
| `docs-final` | 0 | [docs-final.log](docs-final.log) |
| `docs-no-git-final` | 0 | [docs-no-git-final.log](docs-no-git-final.log) |
| `em-dash-final` | 0 | [em-dash-final.log](em-dash-final.log) |
| `doc-style` | 0 | [doc-style.log](doc-style.log) |
| `toc-check` | 0 | [toc-check.log](toc-check.log) |
| `toc-anchors` | 0 | [toc-anchors.log](toc-anchors.log) |
| `doc-paths` | 0 | [doc-paths.log](doc-paths.log) |
| `module-matrix` | 0 | [module-matrix.log](module-matrix.log) |
| `xvlog` | 0 | [xvlog.log](xvlog.log) |
| `rtl-source-lists` | 0 | [rtl-source-lists.log](rtl-source-lists.log) |
| `sv-idiom` | 0 | [sv-idiom.log](sv-idiom.log) |
| `lint-rtl` | 0 | [lint-rtl.log](lint-rtl.log) |
| `cpp-idiom` | 0 | [cpp-idiom.log](cpp-idiom.log) |
| `py-idiom` | 0 | [py-idiom.log](py-idiom.log) |
| `port-contracts` | 0 | [port-contracts.log](port-contracts.log) |
| `naming` | 0 | [naming.log](naming.log) |
| `test-evidence` | 0 | [test-evidence.log](test-evidence.log) |
| `behave` | 0 | [behave.log](behave.log) |
| `diff-final` | 0 | [diff-final.log](diff-final.log) |
| `ooc-base` | 0 | [ooc-base.log](ooc-base.log) |
| `ooc-head` | 0 | [ooc-head.log](ooc-head.log) |
| `ooc-alignment` | 0 | [ooc-alignment.log](ooc-alignment.log) |
| Default datapath commands 1-9 | all 0 | `dp-run-01.log` through `dp-run-09.log` |
| Default datapath commands 10-20 | all 0 | `dp-run-10.log` through `dp-run-20.log` |
| Default datapath commands 21-31 | all 0 | `dp-run-21.log` through `dp-run-31.log` |
| Default datapath commands 32-33 | all 0 | `dp-run-32.log` through `dp-run-33.log` |

The 33 datapath commands are expanded from the unchanged `make -n run VERILATOR_JOBS=4` recipe; only informational echoes are omitted. [milan-dp-run-dry.txt](milan-dp-run-dry.txt) preserves the expansion. The connected gmstep leg passes 58/58, both timing legs pass 181/181, and the default controls remain in commands 32 and 33.

Gate limits:
- Builder exit 0, with one NOT RUN arm: gate 11 board-report calibration, because its required utilization report is absent. No compiler-related arm was skipped.
- Behavior suite: 14 features, 344 scenarios and 1739 steps pass.
- Live xvlog: 0 first-party findings and 4 pinned-processor findings, equal to its ratchet. RTL lint: 90 <= 90.
- Documentation ran both with Git inventory and with inaccessible Git metadata to exercise the no-Git filesystem inventory. The no-Git arm skips only inventory parity, as designed.
- Initial em-dash execution refused a missing pinned renderer (rc 2). After installing the locked dependencies in temporary storage outside the output directory, the final gate passes (339/339 controls). No dependency refusal is reported as coverage.
- No hosted/act run or hardware measurement was performed in this round. Publication and exact-head independent review remain for the next authorized turn.

## Area

| Measurement | LUT | FF | RAMB36 / RAMB18 | DSP | CARRY4 |
|---|---:|---:|---|---:|---:|
| Original base servo | 864 | 790 | 0 / 0 | 1 | 150 |
| Current servo | 871 | 792 | 0 / 0 | 1 | 150 |
| Lane delta | +7 | +2 | 0 / 0 | 0 | 0 |
| Isolated release alignment | 1 | 4 | 0 / 0 | 0 | 0 |

All three measurements use the repository OOC recipe (`synth_xilinx -family xc7 -flatten`), default leaf parameters and its normal DSP policy. The base servo comes from `5b73d3f47dfed519eb988c13d6beb1db664ef1e0`; scratch recipes only select that source or wrap the exact alignment block. [area-recipe.patch](area-recipe.patch) records those path/source changes. These are isolated parent-logic figures, not a whole-datapath measurement. Round 3 adds no area over round 2: source identity and measured counts match.

## Handoff state

`PR-BODY.md` contains the full fetched PR body with the round-3 update; it has not been applied. The branch remains unpushed. The issue handoff comment is posted only after every required local gate completes. Independent reviewer acceptance and hosted checks are not claimed by this author.

Posted [A308] REVIEW READY: [https://github.com/kebag-logic/milan-fpga/issues/545#issuecomment-5830915333](https://github.com/kebag-logic/milan-fpga/issues/545#issuecomment-5830915333).
