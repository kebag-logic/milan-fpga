[A255] REVIEW READY

Head: `a14ef8b4787b5309dd9ab472e82ae2b4a3fdbb72`
Branch: `43-49-gsi-internal` (local; not pushed). Three commits on top of round 1 (`57715787`):
- `f28e90b2`: RTL, tests and docs
- `68ad9356`: the area recipe now takes a stream shape, plus the area record
- `a14ef8b4`: test only

Round 2 against the [decision](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/43#issuecomment-5814505442):

1. **R295-1 F1: re-bind notification.**
   - The listener's exclusion of re-binding walks is removed.
   - The started/stopped pulse and the pbsta/acmpsta compare register off the same record write, so one event gives one frame.
   - New test GI REBIND-SW: a re-bind from PRB_W_RESP with STREAMING_WAIT gives exactly one unsolicited response, and that response carries STREAMING_WAIT.
   - The retained mutant `rebind-started-trigger-removed` is killed.
   - The listener comment, the top comment and 06 §7 are corrected.
2. **R294-1 F1 = R295-1 F2: FailureInformation change.**
   - A separate `evt_tk_fail_chg_o` feeds only the notification OR. It causes no MRP New and no TK_REGISTERED, and it is not routed.
   - Wire-level GI check: no Listener New after a changed FailureInformation. A fresh Failed registration still declares New, as the control.
   - FAILED-REFRESH still notifies.
   - Module checks are added in `srp_stream_fsms` and `srp_top`.
3. **Sample-and-hold removed.**
   - Owners are read live, and F06.13 now states the bound.
   - Registers saved (the top's own): 81 at 8x8, 78 at 1x1.
4. **Area.** The bridge is gated once, after the index mux, and the change is compared on the hit sink only. Same recipe against base `939c1433`:

   | Shape | Round 1 | Round 2 |
   |---|---|---|
   | 8x8 | +640 LUT / +784 FF | **+234 LUT / +710 FF** |
   | 1x1 | +185 LUT / +299 FF | **+267 LUT / +228 FF** |

   Block RAM is unchanged. The 1x1 LUT figure is dominated by variance in untouched modules. The SRP listener is −47 LUT against round 1.
5. **Also taken:** an index-guard test (its mutant is killed), portable CPU affinity in the mutant runner, and `dbg_recwr_*` documented as a functional bus.

Evidence at the exact head. The pinned simulator was used; every command ran in the foreground and its rc was read directly.
- **CI gates, all rc 0:**
  - lint
  - every suite: 16,416 checks, 0 failing (processor top 1,948, of which GI 488)
  - traceability matrix
  - NVM figures
  - links, matrix, waveforms and staleness
  - `make check`
  - off-vendor elaboration of 36 tops
  - `git diff --check`
- **Retained mutants:** 13 of 13 killed by named checks; golden and restored runs clean.
- **Reviewer probes, run unchanged:**
  - R294 P1 prints `changed-failure next tick pushes=0`.
  - R294 P2 shows 0 Listener declarations in the changed window.
  - R295 R1 gives 1 notification (started 1→0).
  - R295 R2 gives 0 New.
  - R295 R3 shows no leak.
- **Reviewer mutants:**
  - Every mutant whose site is unchanged is killed. This includes `sink-index-guard-removed`, which survived in round 1.
  - Sites removed by design were re-expressed on the new code, and those mutants are killed.
  - `sample-transparent` and `live-unsampled-fields` are moot.
- **Parent consumer** (`pp94-parent-consumer`; only the processor checkout moved, parent index untouched): `check_rtl_source_lists.py` rc 0; `pp_shadow` 371 checks, 0 failures.

`HANDOFF.md` and `PR-BODY.md` are complete in the assigned output directory.

Pending with the manager:
- push and the PR body update
- hosted and act acceptance
- the parent's gitlink-dependent gates
- the merge-turn candidate
- re-review
