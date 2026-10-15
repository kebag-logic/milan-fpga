[A614] REVIEW READY

Commit: `84ee9ea119b548b4982d2c0988d8753a2ce4d0cf`
Branch: `737-ci-30min`, from round-two head `2658a64c`. Clean worktree. No push or PR write occurred; origin still holds `2658a64c`.

Changed under ruling 6176299708:

1. R637-2-F2 (`cb25fc6b2`, `3083347d6`): every inventory reader gets pinned dependency preparation, including `ci-manifest` and the docs scheduling controls. The generator refuses an unprepared reader. Removing the preparation from each of the thirteen readers fails. A fresh checkout with no submodules prepares and collects all six suite unions (19/31/31/66/3/4 legs).
2. R637-2-F1 (`8a8833e4e`, `e4e6e20e3`): raw skipped-matrix names, derived from the committed definitions, flow through the graph, collector and watcher. The retained hosted job shape yields skipped legs and an incomplete manifest, with no success recorded and no cancellation. Unknown names, invalid raw states and raw/expanded overlap are refused in both orders, before failure selection.
3. R637-2-F3 with R636-2-S5(b) (`4c6f5b7cd`): an observer-only failure (403, 429, 5xx, timeout or retry exhaustion) in the watcher or the collector ends that job without a failed conclusion and with an explicit `observer_only_error` output. It marks the manifest incomplete and grants no cancellation. Genuine collection, tail and upload failures still cancel. The collector's 15-minute limit exceeds its 600-second read budget. Failures are injected through the production entry point and the generated graph, including 360/480-second waits beyond the old allowance. `docs/testing/CI_WORKFLOWS.md` describes the behaviour.
4. R636-2-F1 (`225135e22`, `2ac674b47`, `84ee9ea11`): both contract self-tests run on source-derived worker `docs-gates-2`. Each generated arm regenerates only its mutated workflow; no arm is removed and no timeout raised. Yosys compilation moves to prerequisite `yosys-tool`. Projected worker times: `docs-gates-0/1/2` 922/1506/553 s and elaboration 1561/713 s, each at most 1620. `yosys-tool` cold is 720 s and Yosys shard 0 is 554 s, against 1044. The docs workflow projects at 1776 s (29.6 min). Every worker's margin is in `CI_WORKFLOWS.md`.
5. R636-2-F2 (`c93c303f3`, `bbb19cec8`): `CI_TOOL_BUILD_JOBS=min(available CPUs, 8)`. At 16/12 CPUs, Verilator peaks at 4811259904/4793225216 bytes and Yosys at 5264482304/5117616128 bytes, with all memory events zero and at least 38.713% reserve. Unrestricted builds are recorded as rejected counterexamples. The largest class is still capture at 6047100928 bytes, leaving 29.60% of the cap. Caps and admission are unchanged.
6. R636-2-S1, S2, S4 (`c8896fab2`): removing each guard makes its self-test fail.
7. R636-2-S3, S5(a): no change; recorded for the #495 checklist.

Found during committed-head validation and fixed in `0fd126de4`: the bare-metal scope gate failed on three host-OS words that this lane had added (`ci/constraints-ci.txt:1`, `docs/testing/CI_WORKFLOWS.md:2787`, `scripts/build_ci_act.py:55`). The two prose lines are reworded. The Go archive's OS segment now comes from `sys.platform`, and the digest pin is unchanged. The gate is unchanged. The rebuilt dispatcher has the same binary SHA-256 as in round two.

Validation at `84ee9ea1`: exact source step bodies in the shipping job image, one 8 GiB container per bank, no network.

- docs `docs-check`: 40/40 steps rc 0; contract self-test 5,209 arms; bare-metal gate 0 findings.
- rtl-fast, all twelve jobs: 20/20 steps rc 0, scope `rtl=true`.
- docs `docs-check-no-git`: rc 0.
- Runner contract gate, both invocations, in an isolated read-only container without a Docker socket: rc 0.
- Python idiom, hygiene, docs, style, cited-path, TOC, em-dash, generator and CI-event contract checks: rc 0.

Setup steps are provided by the image; the source Yosys build is sized separately under item 5. No test assertion, case, arm, timeout, firmware behaviour or linked image was changed to obtain a pass.

Acceptance criteria: items 1-6 are met with the evidence above; item 7 is recorded.

Open risks/questions:

- These are projections, not hosted times. In the committed-head banks the builder step took 1411-1416 s, running one simulation child and sharing CPUs with the rtl-fast bank. With that figure, `docs-gates-1` would be 1531-1536 s (within 1620), and the docs workflow 1802-1806 s, up to 6 s over thirty minutes. The projection keeps the 1386 s shipping-width measurement, and hosted readback decides.
- `scripts/build_ci_act.py` now derives the Go archive name from the build host instead of spelling it out. The alternative is a file-pinned allowance in the bare-metal gate, but that changes what the gate checks.
- Runner SHA-256 for repinning: `f968f67655ac386ea703248b724c3781b95ec379d3a5287b378e470df81f895c`.
- Coordinating publication, repinning, complete replay, hosted timings and independent re-review remain. Both round-two reviews are NEGATIVE; this handoff is not a review verdict. No owner-level decision is requested.

`HANDOFF.md` and `PR-BODY.md` carry the Round 3 section with file:line references, receipts and bank attempts.
