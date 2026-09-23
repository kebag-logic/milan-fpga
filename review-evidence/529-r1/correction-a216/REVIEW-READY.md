[A216] REVIEW READY
Commit: `535701a06128d54c7f0f161e1c061fa02d4d1342` (tree `8c62c1a118b6bdacc0cf9b39d2cbdc633717630f`)

This is correction round 1 of PR #534, for R268-1 and R269-1. Two one-line commits sit on
the reviewed head `f8155775`: `a51d5164` (harness) and `535701a0` (docs). Nothing is pushed
from this lane.

**No RTL change.** `git diff f8155775 HEAD -- hdl` is empty. So there is no VERSION,
descriptor or synthesis consequence, and CHANGELOG.md is unchanged.

| Finding | Severity, lens (as filed) | Fix | Failing arm shown |
|---|---|---|---|
| R269 F1 = R268 F1: a permuted `KL_crf_rx` port binding is invisible; 7 of the 10 bindings are not discriminated | MAJOR (per the assignment; R268 filed MINOR). Conformance, Tests, Docs | New last arm of `[CTRS-CRF]` (`sim_nxn.cpp:3578`). No tally is seeded. In a fresh era, real PDUs at the root move each of the ten through its own engine event, as do the engine's 100 ms silence timeout for the unlock (see the note below). The ten end at pairwise-distinct counts (2, 1, 3, 4, 5, 6, 7, 8, 9, 21), each checked exactly. The Table 5.6 lock pair is also graded after the first lock (1/0) and after the unlock (1/1). | All **45 pairwise exchanges** of the ten bindings at the instance are red on nxn and on nxn8. Every one reddens both of its own quadlets. R269 mx1-mx4 (byte-identical to their receipt 15) and R268 p1-p5 (hunk-identical to their `mutant.diff`) are red on nxn, nxn8, nxndv and nxn4c. With the f8155775 harness, 22 of the 45 were green on nxn. |
| R268 F2: `[NOTIFY-CRF]` cannot fail for a row that keeps pushing | MINOR. Tests, Docs | After the release, the next two seconds without a change must bring no further push, to B nor to A (`sim_nxn.cpp:1346-1353`). | R268's `r3_crf_pend_stuck` is red on obj_notify: 4 pushes against 2, to B and to A. The marked control passes, 145/0. |
| R268 F3: the REGISTER_MAP opening status lists the CRF bank as a gap | MINOR. Docs | `REGISTER_MAP.md:31-35` now says served and pushed since #529. | Docs gates |
| R269 docs overclaim: REGISTER_MAP 846-877, `sim_nxn.cpp` 3409-3411, README 507-521 | Part of F1. Docs | The signature arm is described as grading the gather mux only. The binding claim rests on the event arm. The mutation claims read "turns at least one check red". The frozen criteria are quoted beside their evidence (this takes up R269 S4). The compliance matrix 5.4.2.25 names the event arm. | Docs gates |

**How the unlock's silence is spent.** A real 100 ms is 10M fabric cycles. That measured
6.2 s -> 37.6 s on nxn, on a suite with a 2700 s hosted deadline. So the harness advances
`KL_crf_rx`'s own timeout counter, through the engine's hierarchy, to 1 ms short of its
limit, and that last millisecond runs for real. No tally is written, and a port-map
exchange cannot relabel that counter. All 9 exchanges involving MEDIA_UNLOCKED are red on
each shape.

**Validation**, on the pinned simulator 5.050 with 8 jobs. Every leg ran with its `run`
recipe line, at harness sha256 `fe0e4c37…` (= HEAD):

| Leg | Result | Before this round |
|---|---|---|
| nxn | 1705/0 | 1687 |
| nxndv | 1707/0 | 1689 |
| nxn4c | 1705/0 | 1687 |
| nxn8 | 3133/0 | 3115 |
| notify | 145/0 | 143 |
| main | 230/0, with 1 section guarded as at base | 230 |

`[CTRS-CRF]` now has 72 checks per broad leg, up from 54. `[NOTIFY-CRF]` has 10, up from 8.

Gates at `535701a0`:

- `xvlog_gate --check` passes, with `hdl/` at 0 findings.
- These exit 0:
  - `check_rtl_source_lists`, `check_cpp_idiom` (every ratchet 0 <= 0), `check_py_idiom`
    and `check_baremetal_only --check`;
  - `docs_check`, `lint_rtl --check`, `check_sv_idiom` and `check_port_contracts`;
  - `gen_module_matrix --check` and 13 further docs-workflow gates.
- `test_builder.py` passes, except gate 11, which was not run: it needs the mf48 build
  report, which is not on this host.
- `git diff --check` is clean.
- `check_em_dash --base ede8d48e` (the merge base) finds 0 over 153 added lines.
- `--base 759da623` reports 1 finding, at `CONTRIBUTING.md:342`. This lane never touches
  that file. 759da623 is not an ancestor, and the candidate merge with it adds 0 em dashes.
- A merge-tree against the live dev tip `26d855a9` is clean. It was not built.

**Mutation evidence.** 197 receipts. Each names the datapath and harness sha256, the exit
codes, the `[FAIL]` lines and the tally.

- R269 ma1-ma7 are all red on nxn.
- R268 a1-a8 are all red on nxn, with `ctl_marked` green at 1705/0.
- R268 r2, r4, r5 and r7 are red.
- r1, r3 and r6 stay green on nxn, as in R268's own receipts:
  - r1 is equivalent at the wire;
  - r3 is red on notify (F2);
  - r6 is R268 S1 and not taken up.
- Neither notify nor main carries `[CTRS-CRF]`, so mx1-mx3 were not rerun there.

The packet for the coordinator to archive:

- `HANDOFF.md` and `PR-BODY.md`;
- `MUTATION-RESULTS.md` and the receipts;
- the generator and runner scripts, plus both reviewers' generators, verbatim;
- `MANIFEST.sha256`.

**Acceptance criteria.** REGISTER_MAP closure criteria 1-4 are met, with the evidence above.
Criterion 4's "controller decoding" now covers all ten bindings. The silicon Milan-compatible
verdict follows the merge (#117).

**Open risks and questions:**

- **Found, out of scope, for a new Issue.** The `KL_crf_rx` banner (`:32-34`) and the
  REGISTER_MAP `CRF_CTRL` row say a validation error unlocks the sink, and the banner adds a
  jitter window to lock. The engine does neither: it unlocks only on the 100 ms silence
  (`:484-488`). This predates the lane. The event arm keeps its rejected PDUs before the
  first lock, so it encodes neither reading.
- **Not taken up** (all suggestions): R269 S1/S2/S3, R268 S1, and `Closes #529` with the
  silicon item (R269 S5 / R268 S3, a manager duty).
- **Not run this round**, because their inputs are unchanged: the milan_dp legs that do not
  compile `sim_nxn.cpp`, pp_shadow, milan_dp_render, crf_rx, behave, Yosys, act and hardware.
