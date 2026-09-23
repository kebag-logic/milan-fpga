# HANDOFF: [A197], #74 item 2 (junction-counter raced-lock chatter)

## State

- **Lane:** `$LANES/74-junction-chatter`, branch `74-junction-chatter`.
- **Base:** live `dev` `ede8d48ecd7c7f589a14b957951f040d92c99c70`.
- **Head:** `6d1572d6caeb94cd3dd871b9df90e4c5298998b6`. One commit with a one-line subject, no trailers; the worktree is clean.
- **Not pushed. No PR opened.** Pushing and PR edits were out of bounds for this lane. `PR-BODY.md` is ready to paste.
- **Public comments on #74:**
  - TAKEN: https://github.com/kebag-logic/milan-fpga/issues/74#issuecomment-5794228544
  - DECISION: https://github.com/kebag-logic/milan-fpga/issues/74#issuecomment-5794560116
  - REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/74#issuecomment-5795282366
- **Toolchain:** Verilator `5.050 2026-07-01 rev v5.050`, the pinned wrapper `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` (sha256 `905795b9...e92f`). The system `verilator` is 5.052 and was not used for evidence. Parallelism was at most 8.

## What changed (10 files, +357/-44)

1. `hdl/ieee1722/crf/KL_media_grid_align.sv` gets the lock-phase keep-off. At engagement, `ref_r` becomes the capture clamped into `[LOCK_KEEPOFF_CYC_P, DIV_C - LOCK_KEEPOFF_CYC_P]`. The new parameter defaults to `DIV_C/128` (16 cycles at 100 MHz), and an elaboration guard is added. A non-raced engagement is bit-identical to base.
2. `hdl/ieee1722/aaf/KL_chan_map_capture.sv` changes the `tdm_slip_count` `2'b11` branch: `tdm_frame_pend_r <= tdm_frame_pend_r` (it was `<= 1'b0`). The KNOWN CAVEAT banner is replaced by a COINCIDENCE paragraph.
3. `tb/verilator/media_grid_align` changes:
   - The wrap instantiates the real `KL_chan_map_capture`.
   - Arms G7, G8 and G9 are added.
   - The `MGA_MUT_NO_KEEPOFF` mutant is a define in the wrap that sets `LOCK_KEEPOFF_CYC_P = 0`.
   - The `MGA_MUT_COIN` mutant is a sed-built copy of the capture file, and the recipe refuses the copy if nothing changed.
   - The README is updated, and `gen_toc` switched the page's Contents separator to `--`.
4. `tb/verilator/chmap_capture/sim_main.cpp` adds three directed coincidence checks to [T0].
5. Docs: the `REGISTER_MAP.md` `SLIP_TDM` paragraph, one row in the `TIME_SYNC.md` Media boundary table, and the `TESTING.md` suite row.

No change to `milan_datapath.sv`, `milan_csr.sv`, pins, shape, CSR words, counters, `mr` triggers or the settle criterion. No blocker was needed.

## Decision in one paragraph

The mechanism is a lock-phase keep-off target. Detector hysteresis was rejected because it makes the marker-to-tick association ambiguous inside its band, so a step slip there goes uncounted. The one-line coincidence correction ships with it because the base counter's coincidence branch also miscounts free-running slips: about a dozen dups per slip, and skip-direction slips read as dups with no skip. Neither half suffices alone; the measurements are in the DECISION comment and `PR-BODY.md`. The ledger item offered "a lock-phase target or detector hysteresis". This lane ships the target, plus the counter-law repair that the [R1] finding itself named ("the 2'b11 coincidence branch silently eats the balancing skip"). A reviewer who reads the repair as scope growth should say so on #74.

## Evidence (`receipts/`, see `receipts/README.md`)

- **At head:**
  - `media_grid_align`: 45/45. The three mutants fail on G2, G7 and G9 respectively.
  - `chmap_capture`: 204/204, plus netlist 20/20.
  - `milan_dp aclk`: 139/139, with output byte-identical to a base build of the same leg.
  - lint 90<=90, `sv_idiom`, naming, port contracts, `cpp_idiom`, test evidence, hygiene, fail-fast, TODO, RTL source lists, feature status, doc paths, gPTP docs, solution docs, `gen_toc`, `docs_check`, doc style, em-dash (0/35 lines), `git diff --check`: all pass.
  - xvlog passes with 0 findings in `hdl/`. It used the home-directory Vivado install, not a container.
- **At base (the branch harnesses against base RTL, extracted by `git show` into `base_rtl/`):**
  - `media_grid_align`: 13/45 failures, all in G7-G9.
  - `chmap_capture`: 3/204 failures, exactly the new checks.
- **Unchanged arms:** G0-G6 output is identical across base with the old harness, base with the new harness, and head.

## Open items for the next owner

1. **Review.** Needs internal cleared-context review and external review, covering all five lenses.
2. **Push and PR.** Push the branch, open a draft PR against `dev` using `PR-BODY.md`, then run the act-first local replica and let hosted CI run. None of this was done in this lane.
3. **VERSION and CHANGELOG.** The `SLIP_TDM` counting semantics changed: a free-running slip is now counted once in its direction. The next VERSION bump (in `milan_csr.sv`) should carry a release note.
4. **Top-level jitter model.** The unit loop models the root's marker pop jitter as 0 or 1 edge. Silicon width is unmeasured, and ledger items 1 and 4 (bench) would confirm it.
5. **Pre-existing ratchet slack.** Test evidence could be lowered to 74 and fail-fast to 82, 4 and 0. It predates this lane and was left alone as out of scope.

## Output directory contents

- `taken.md`, `decision.md`: the posted comment bodies.
- `PR-BODY.md`, `HANDOFF.md`.
- `receipts/`: logs, diffs and `run_base_receipts.sh`.
- `base_rtl/`: base copies of the five RTL files the receipts build.
- `scratch/`: the exploration benches: prototype RTL, the 12 s free-run timestamp runs `scratch/explore/free12-*.log`, and the jitter A/B runs `scratch/mga/j-*-run.log`.
- `obj_*` directories are regenerable build output.
