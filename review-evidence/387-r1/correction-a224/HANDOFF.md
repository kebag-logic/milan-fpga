# [A224] HANDOFF: kebag-logic/milan-fpga #387, PR #540 correction round 1

Author lane A224. Assignment: https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5804878668
REVIEW READY posted: https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5805175917 (text in `REVIEW-READY.md`)

Findings answered: R276-1 F1 to F5 (https://github.com/kebag-logic/milan-fpga/pull/540#issuecomment-5804105668) and R277-1 findings 1 to 3 (https://github.com/kebag-logic/milan-fpga/pull/540#issuecomment-5804873088), all MINOR, plus the four suggestions.

| Item | Value |
|---|---|
| Branch | `387-gm-step-rebase` (worktree `$LANES/387-gm-step-rebase`), **not pushed** |
| Base of the round | PR head `44bf089108fec666d50873445720b51090ceede0` |
| New head | `021b2e07b009158bcb0ce19529126eb1d330bba5`, tree `a7ffb35beea95d5bba593029f382e8c0ab0b1c27` |
| Commits | `fdd613a1` harness and Makefile; `021b2e07` docs. One-line subjects, no trailers |
| Hot files | `hdl/milan/milan_datapath.sv`, `tb/verilator/milan_dp/sim_nxn.cpp` and `CHANGELOG.md` are untouched (`git diff --stat 759da623 HEAD`) |
| Working tree | clean (build outputs are ignored `obj_*` directories only) |
| Tool | Verilator 5.050 through the pinned wrapper, sha256 `905795b9...e92f`, at most 8 jobs |

The campaigns below ran at `fdd613a1`. From `fdd613a1` to `021b2e07`, the only change under `tb/` is `README.md`, so the harness and the Makefile are byte-identical at the new head. `make gmstep` was also re-run at `021b2e07` (`logs/gmstep-head-final.log`).

## Per-finding disposition

The reviewers set the lens labels. They are not re-labelled here.

| Finding | Lens | What changed | Evidence at the new head |
|---|---|---|---|
| R276-1 F1 = R277-1 finding 1: the grid-aligner row's Decided column states an owner decision the owner did not make | Conformance, Docs | `docs/design/GM_LOSS_RECOVERY.md:119`. The Decided column quotes part (b) verbatim: "the render elastic stage (#386) and the media grid aligner's phase reference re-centre in one bounded, counted event". The This-tree column states the observation: `KL_media_grid_align.sv` has no PHC or step input, and under CRF selection a step reaches it only through the CRF-steered grid (#539). It also says the question is with the owner on #387. The packet NCO moved to its own row (`:120`), "Not named by the decision". The render row's Decided column (`:118`) now also cites part (b) instead of paraphrasing the implementation | The row is traceable to 5606198212 part (b). This page no longer settles the aligner question; it is raised in the REVIEW READY comment. `docs_check`, `check_doc_style` and `check_em_dash` pass |
| R276-1 F2: the section omits ruling 5802264260 item 2 | Conformance, Docs | New row at `GM_LOSS_RECOVERY.md:124`. Decided: the step "merges with it: exactly one restart, never a cancellation, and the step's MEDIA_RESET is still counted". This tree: "Not yet: `KL_media_clock_restart` flips its target once per request, so a second request before the first reaches the wire cancels it" (`KL_media_clock_restart.sv:167`) | A reader of the section alone can state the rule. The gates are green |
| R276-1 F3 = R277-1 finding 2: "The `milan_dp` gmstep leg measures all of this" overclaims | Docs (R277-1: Docs, Tests) | That sentence is gone. `GM_LOSS_RECOVERY.md:135-151` lists what the leg grades, each item a named check. It lists what the leg does not grade and where each one is covered or left open: the aligner (TDM clocks held), the CRF servo (DRP answers zero; #539), the lwSRP licence (escape bit), the pending-restart merge (arm with the edit) and the physical re-base (#117). The verification row (`:179`) is narrowed. The leg's banner (`sim_gmstep.cpp:4-19`) and README carry the same "does not grade" list | Each graded item maps to checks in `sim_gmstep.cpp`: tu `:886-911`, streams `:916-960`, render `:963-990`, `mr` and MEDIA_RESET `:996-1024` |
| R276-1 F4: the counted-event checks do not tie the event to the step | Tests | Three new checks and one guard. (a) `:977` "render: every counted re-base lands at a PDU end right after the step": each move of `rsp_recentres_w` lands within 500 cycles (two AAF periods) after the plane's step pulse. (b) `:1013` "restart: every mr toggle is first sent right after the step": the first PDU with the new level leaves within two talker intervals. (c) `:1020` "restart: MEDIA_RESET does not move between the commit and the step", from a GET_COUNTERS read taken after the commit. (d) `:872` checks that this read lands between the commit and the step. The identity change precedes the step by about 160000 cycles | R276-1's own probe `edit-identity-keyed-rebase` now fails (a), (b) and (c): `logs/r276-probes-at-head.txt`. R277-1's E8 fails the same three (`logs/r277-probes-at-head.jsonl`). Control 8 fails them at delays 0 and 12 (`logs/gmstep-controls-edit.txt`). On the edited copy, the event lands at +132 and +116 cycles |
| R276-1 F5: the licence checks cannot see a talker that stops for good | Tests, Robustness | The graded window ends when the licence is graded. `longest` starts from the silence after the last PDU (`:925`), and the rate span runs to the window end (`:931`). `grade_uncertainty` now requires more than 100 talker PDUs both inside the hold and after `tu` clears (`:908-909`) | R276-1's own probe `edit-talker-silent-after-event` now fails "licence: the talker never pauses beyond four of its intervals" (longest pause 440726 cycles), "licence: the talker keeps its baseline rate within 1%" and "tu: talker PDUs graded after tu clears". R277-1's E9 and control 4 (at delays 0 and 12) fail the same three |
| R277-1 finding 3: the render-law arms depend on the leg's start phase | Tests, Robustness, Docs | The law is graded at the stage's own reference point. `KL_render_setpoint` judges its bands on the fill right after each PDU's push, TARGET_C = setpoint 8 + one PDU = 14. The leg reads that fill as the peak of the registered `rsp_fill_w` between two accepts (`:437-447`). Pops only lower it after the push, and the next PDU pushes only after its own accept, because the depacketizer commits at tlast, after the monitor's accept at byte 48. The checks are `:809` (baseline) and `:989` (across the event). The fill at accept is printed, not graded. An optional second argument (`GMSTEP_FEED_DELAY`) idles before the feed starts, at the same point the reviewer's probe did (`:769`). The banner and README now describe the reference point, and the "9 events, the band's upper edge" statement is gone | Sweep over delays 0 to 41 with the edit: **42/42 pass**, fill after every push 14 at every delay, fill at accept 9 or 10 (`logs/gmstep-sweep-edit.txt`). This includes delays 6 to 12, which R277-1 showed failing. The stage mutant (snap one event off) is caught at delays 0 and 12 by "render: every PDU push leaves the target fill across the event" and by nothing else. R277-1's E6 is caught the same way |

### Suggestions (optional, taken)

| Suggestion | What changed | Evidence |
|---|---|---|
| R276-1 S1 = R277-1 S1: the Makefile names a runner that is not in the tree | `Makefile:99-101` and `:277-284` describe the override and say the runner joins with the datapath edit. They name no file | No comment names an untracked file |
| R276-1 S2 = R277-1 S2: Stream Input answers are never checked for validity | `:953` checks that both Stream Input answers carry the MEDIA_UNLOCKED and FRAMES_RX bits. `:956` checks that FRAMES_RX moves by the accepts the harness saw between the two reads. Stream Output validity is now checked on all three reads (`:1014-1019`). A missing answer now reads `counters_valid` = 0 (`:705-708`). Before, the `0xDEADBEEF` marker happened to satisfy the new mask | R277-1's H9 now fails both new checks. Control 5 does too, at delays 0 and 12 |
| R276-1 S3: cite #539 on the CRF-servo row | `GM_LOSS_RECOVERY.md:121` | |
| R277-1 S3: `TIME_SYNC.md:95` said `KL_gptp_txret` enforces the bound | `TIME_SYNC.md:95-97`: the plane's microcode clamps the trim, `KL_gptp_txret` computes the same bound as `PHC_ADJ_MAX_C` and refuses egress timestamps while the trim exceeds it (`KL_gptp_txret.sv:303-305,434-436`; donor `gen_gptp_ucode.py:428`) | |

## Gates

| Gate | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/milan_dp gmstep` at `021b2e07` (tree datapath) | 48 checks, 4 failures, exactly the pending decided behaviour: render counts 2, one of them outside the step window, no `mr` toggle, no MEDIA_RESET. Make exit 2 | `logs/gmstep-head-final.log`, and `logs/gmstep-tree.log` at `fdd613a1` |
| Start-phase sweep, clean leg on the edited datapath copy, delays 0 to 41 | 42/42 PASS, 48/48 each | `logs/gmstep-sweep-edit.txt`, `logs/sweep-edit/` |
| Failing-arm runner (`work/gmstep_mutants.py --controls 0,12`) | 10 controls x 2 delays, 0 escapes. Each run failed with every named check among its failures, and the failure sets are identical at both delays | `logs/gmstep-controls-edit.txt`, `logs/controls-edit/` |
| R276-1's `gmstep_probes.py`, unmodified, from `origin/387-review-evidence` at `dbfab84f` | edit-clean 48/0; edit-identity-keyed-rebase 3 failures; edit-talker-silent-after-event 3 failures; edit-step-recentre-removed 1 failure | `logs/r276-probes-at-head.txt`, `logs/r276-probes/` |
| R277-1's `gmstep_probes.py`, unmodified | E0 48/0; E8 3; E9 3; H9 6; E6 1; H3 3 failures (H3 now fails the window check as well as the count) | `logs/r277-probes-at-head.jsonl`, `logs/r277-probes/` |
| `docs_check`, `check_doc_style`, `check_em_dash --base 759da623`, `check_gptp_docs` (with and without the submodule), `check_cpp_idiom`, `check_py_idiom`, `gen_toc --check`, `measure_test_evidence --check`, `check_feature_status`, `check_submodule_docs`, `git diff --check 759da623 HEAD` | all exit 0 | `logs/static-gates.log` |
| Makefile `print-srcs`, `print-pp-srcs`, `print-dp-vflags` | byte-identical to `44bf0891` (sha256 in the receipt) | `logs/static-gates.log` |

R277-1's `phase_probe.sh` was not re-run, because its anchors patch the old harness text. The leg's own feed delay replaces it at the same insertion point, and the sweep above is its equivalent.

**Not run, and why:**

- `gptp_shadow`, `clkvalid` and `media_grid_align`: this round touches none of their sources or any RTL. The changed files are `sim_gmstep.cpp`, the `milan_dp` Makefile (comments, plus the `gmstep` run line and one variable), the `milan_dp` README, `GM_LOSS_RECOVERY.md` and `TIME_SYNC.md`.
- The `milan_dp` `gptp` and `gptp-lat` legs and the full `run` recipe: their source lists and flags are byte-identical to the reviewed head.
- Yosys and the builder: no RTL or configuration changed.
- Hosted CI, act, Docker and hardware: not allowed in this lane. Acceptance 4 (#117) was not attempted.

## Open points for the manager and the owner

1. **The grid aligner's re-centre (owner ruling needed).** Decision part (b) names "the media grid aligner's phase reference" as re-centring in the counted event. `KL_media_grid_align.sv` has no PHC or step input. Its reference is captured at engagement against the physical frame marker. Under CRF selection, a step reaches it only through the CRF-steered grid, via the CRF servo whose step guard has the #539 gap. The page now quotes the decision and records the gap. It does not settle the question. The gmstep leg cannot grade it, because the TDM clocks are held.
2. **The pending-restart merge (ruling 5802264260 item 2)** is recorded as "Not yet". Its failing arm belongs to the datapath edit.
3. **Observation, not a finding:** across the event, the listener's EARLY_TIMESTAMP moves by 2 at every phase. The peer's media timestamps step with its first GM B Sync, a moment before the DUT steps on consuming it. The leg prints this and does not grade it.

## Packet

| File | sha256 | What |
|---|---|---|
| `PR-BODY.md` | see `MANIFEST.sha256` | Proposed PR #540 body; starts with [A224] and contains "Relates to #387" |
| `work/milan_datapath.sv` | `45ac96c0367103e37a23632dc85fdf764f3d67486046a89768c1d2b00a4f5930` | The tree datapath (`34e3000b...`) with A214's `proposed-milan_datapath.patch` applied, byte-identical to A214's published `work/milan_datapath.sv` |
| `work/gmstep_mutants.py` | `8ddf009bf1fa53edf8ef10810d85b298a0849d16190749ff752436e34fbd3161` | The failing-arm runner: `--sweep A-B` and `--controls D,..` with 10 controls. It was A214's 7 controls; this round adds the identity-keyed re-base, the talker that stops for good and the dead Stream Input counters, and updates the render control's check name |
| `logs/` | see `MANIFEST.sha256` | Every receipt named above. Planted RTL copies were removed; the scripts regenerate them |

Reproduce the campaigns from `tb/verilator/milan_dp` at the head:

```sh
export VERILATOR=$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator VERILATOR_JOBS=8
python3 -I <packet>/work/gmstep_mutants.py --datapath <packet>/work/milan_datapath.sv --sweep 0-41 --jobs 8 --logs <dir>
python3 -I <packet>/work/gmstep_mutants.py --datapath <packet>/work/milan_datapath.sv --controls 0,12 --jobs 8 --logs <dir>
```

The sweep takes about 2.5 minutes and the controls about 3.5 minutes on 8 jobs.
