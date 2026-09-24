[A224] REVIEW READY

Correction round 1 of PR #540 (Relates to #387), under the [assignment](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5804878668). It answers the eight MINORs of [R276-1](https://github.com/kebag-logic/milan-fpga/pull/540#issuecomment-5804105668) and [R277-1](https://github.com/kebag-logic/milan-fpga/pull/540#issuecomment-5804873088).

Commit: `021b2e07b009158bcb0ce19529126eb1d330bba5`, tree `a7ffb35beea95d5bba593029f382e8c0ab0b1c27`. It is local on branch `387-gm-step-rebase` and **not pushed**; this lane may not push. It descends linearly from the reviewed head `44bf0891` through two one-line commits with no trailers: `fdd613a1` (harness and Makefile) and `021b2e07` (docs). The hot files `milan_datapath.sv`, `sim_nxn.cpp` and `CHANGELOG.md` are untouched.

Changed: `tb/verilator/milan_dp/sim_gmstep.cpp`, `tb/verilator/milan_dp/Makefile` (comments, and an optional `GMSTEP_FEED_DELAY`), `tb/verilator/milan_dp/README.md`, `docs/design/GM_LOSS_RECOVERY.md` and `docs/design/TIME_SYNC.md`. No RTL changed.

## Per-finding disposition (lenses as the reviewers assigned them)

| Finding | Lens | Change | Evidence |
|---|---|---|---|
| R276-1 F1 = R277-1 finding 1: the aligner row's Decided column | Conformance, Docs | `GM_LOSS_RECOVERY.md:119`. The Decided column quotes part (b) verbatim: "the render elastic stage (#386) and the media grid aligner's phase reference re-centre in one bounded, counted event". This tree: `KL_media_grid_align.sv` has no PHC or step input; under CRF selection a step reaches it only through the CRF-steered grid (#539); the question is with the owner. The packet NCO has its own row, "Not named by the decision" | The row is traceable to 5606198212(b). The question is below |
| R276-1 F2: ruling 5802264260 item 2 missing | Conformance, Docs | New row `GM_LOSS_RECOVERY.md:124`. Decided: the step merges with a pending restart, giving exactly one restart, never a cancellation, and the step's MEDIA_RESET still counted. This tree: "Not yet", because `KL_media_clock_restart.sv:167` flips once per request | Docs gates green |
| R276-1 F3 = R277-1 finding 2: "measures all of this" | Docs (R277-1: Docs, Tests) | `GM_LOSS_RECOVERY.md:135-151` lists the graded rows (tu, render re-base, render law, `mr` and MEDIA_RESET, streams) and the ungraded ones with where each is covered or left open: the aligner (TDM clocks held), the CRF servo (#539), the lwSRP licence (escape bit), the pending-restart merge (arm with the datapath edit) and the physical re-base (#117). The verification row (`:179`), the leg's banner and the README say the same | Each graded row maps to named checks in `sim_gmstep.cpp:886-1024` |
| R276-1 F4: the counted event is not tied to the step | Tests | New checks: "render: every counted re-base lands at a PDU end right after the step" (within 500 cycles of the plane's step pulse); "restart: every mr toggle is first sent right after the step" (within two talker intervals); "restart: MEDIA_RESET does not move between the commit and the step" (a GET_COUNTERS read after the commit, with a check that it lands before the step) | R276-1's own `edit-identity-keyed-rebase` and R277-1's E8 now fail all three new checks |
| R276-1 F5: the licence checks cannot see a talker that stops for good | Tests, Robustness | The pause and rate measures run to the end of the graded window. The tu grading requires more than 100 talker PDUs after `tu` clears | R276-1's `edit-talker-silent-after-event` and R277-1's E9 now fail "licence: the talker never pauses beyond four of its intervals" (440726 cycles), the 1% rate check and "tu: talker PDUs graded after tu clears" |
| R277-1 finding 3: the render arms depend on the start phase | Tests, Robustness, Docs | The law is graded where `KL_render_setpoint` judges its bands: the fill right after every PDU push is TARGET_C = 14. The leg reads it as the peak of `rsp_fill_w` between two accepts. The fill at accept is printed, not graded. The leg takes an optional feed delay, inserted where the reviewer's probe inserted it | With the edited datapath copy, the clean leg passes **42/42 feed delays (0 to 41)**, fill after push 14 at every delay, fill at accept 9 or 10. The stage mutant (snap one off) is caught at delays 0 and 12 by "render: every PDU push leaves the target fill across the event" alone |

The suggestions are also taken:

- The Makefile no longer names an untracked runner.
- The Stream Input answers must carry the MEDIA_UNLOCKED and FRAMES_RX valid bits, and FRAMES_RX must move by the accepts seen. R277-1's H9 now fails.
- Stream Output validity is checked on all three reads.
- The CRF-servo row cites #539.
- `TIME_SYNC.md:95-97` says the microcode clamps the trim and `KL_gptp_txret` refuses egress timestamps outside the bound.

## Validation (Verilator 5.050 through the pinned wrapper, at most 8 jobs)

| Gate | Result |
|---|---|
| `make -C tb/verilator/milan_dp gmstep` at `021b2e07` | 48 checks, **4 failures**, all decided behaviour pending the datapath edit. The render stage counts 2 re-bases, the identity-keyed one outside the step window. There is no `mr` toggle and no MEDIA_RESET |
| Clean leg on the edited copy (tree datapath plus A214's published patch, byte-identical to A214's published copy), feed delays 0 to 41 | 42/42 PASS, 48/48 each |
| Failing-arm runner, 10 controls at feed delays 0 and 12 | 20/20 caught by their named checks, with identical failure sets at both delays. The controls: tu late; holdover not re-armed; tu stops the talker; talker stops for good; Stream Input counters dead; no step re-centre; identity re-centres too; re-base keyed to the identity; snap one off; no restart |
| Both reviewers' probe scripts, unmodified, from `387-review-evidence` at `dbfab84f` | as in the table above. R277-1's H3 (at head) now also fails the window check. `phase_probe.sh` was superseded by the leg's own feed delay, because its anchors patch the old harness text |
| `docs_check`, `check_doc_style`, `check_em_dash --base 759da623`, `check_gptp_docs` (with and without the submodule), `check_cpp_idiom`, `check_py_idiom`, `gen_toc --check`, `measure_test_evidence --check`, `check_feature_status`, `check_submodule_docs`, `git diff --check 759da623 HEAD` | all exit 0 |
| Makefile `print-srcs`, `print-pp-srcs`, `print-dp-vflags` | byte-identical to `44bf0891` |

The `gptp_shadow`, `clkvalid` and `media_grid_align` suites were not run, because no RTL or suite source changed. The same holds for `milan_dp gptp` and the full `run` recipe: their source lists and flags are unchanged. Hosted CI, act and hardware are outside this lane. The runner, the edited copy, every log, the HANDOFF and the proposed PR body (starting "[A224]", with "Relates to #387") are in the A224 author packet, `$HOME/milan-fpga-management/2026-09-23/387-a224/` (`MANIFEST.sha256`).

Acceptance criteria:

- Acceptance 1 and 5: unchanged from A214 and met.
- Acceptance 2: met, with the aligner question open as stated in the page.
- Acceptance 3: **not met**. It waits for the datapath edit after #529, and the leg's 4 failures are that edit.
- Acceptance 4: the #117 bench.

Open risks/questions:

1. **For the owner: does the media grid aligner's phase reference need its own re-centre on a step?** Decision part (b) names it. The tree gives it no PHC or step input, and its reference is captured against the physical frame marker. Under CRF selection, a step reaches it only through the CRF-steered grid, whose servo guard has the #539 gap. The page quotes the decision and records the gap; it does not settle the question. The gmstep leg holds the TDM clocks and cannot grade it.
2. The pending-restart merge (ruling item 2) is recorded as "Not yet". Its failing arm belongs to the datapath edit.
3. Observation: across the event, the listener's EARLY_TIMESTAMP moves by 2 at every phase. The peer's media timestamps step with its first GM B Sync, just before the DUT steps. The leg prints this and does not grade it.
