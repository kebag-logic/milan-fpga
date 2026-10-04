# R459-3 scripts

Every script runs on a `git archive b59e99cb928939f5c4089964dea8f4628d06ede7` extraction of the processor repository
(`<tree>`), never in the review clone. Set `PINNED_VERILATOR` to the pinned Verilator 5.050 wrapper (`--version`
"Verilator 5.050 2026-07-01 rev v5.050"; wrapper sha256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`).
The receipts were produced with that variable's earlier hard-coded default (the same wrapper). After the runs, the
only edits were swapping the hard-coded path for the variable and resolving `lint_focus.sh`'s log path to an absolute
path. The lint was re-run after both edits: 24/24, rc 0.

| Script | What it does |
|---|---|
| `verilator-j.sh` | runs the pinned Verilator with the suites' `--build -j 0` rewritten to `-j ${VJ:-2}`, so that concurrent builds stay inside a 16-job budget. It is passed as `VERILATOR=` to each suite's `make` |
| `run_suites_focus.sh <tree> <suite> <logdir>` | runs one suite's default `make` (all arms and shapes, then the suite) with the wrapper. Used for `srp_top`, `srp_stream_fsms` and `srp_admission` |
| `lint_focus.sh <tree> <log>` | lints (the repository's lint flags, whole `hdl/` visible) the four changed SRP modules at the default shape and at N = 1, 2, 3, 5, 9 |
| `probes.py <tree> <scratch> <receipts> --jobs N` | the reviewer's 12 probes: one exact text edit each (it must match once) on a copy of the tree, then the named committed suite target. CAUGHT = non-zero exit with FAIL lines; SURVIVED = exit 0 |
| `lockstep_replay.sh <hdl/srp> <tag> <cycles> <log> "<shape>"...` | replays the published round-1 lockstep bench (`review-evidence/pp230-r1/author-r2/lockstep-r1/`, files unmodified) with reviewer-chosen shapes and seeds. It needs `VALIDATION_STORAGE` laid out as that bench's `build.sh` expects (`pp230-a523/lockstep` with `ref/` from `make_ref.py` on base `c4cb84ff`'s `hdl/srp`, and `pp230-a523/basetree/hdl`). It also needs `VALIDATION_TOOLS` with `pinned-verilator-5.050/verilator` |
| `marginal.py <vivado dir>` | re-derives the `u_srp` sub-block LUT/LUTRAM/FF and the (8x8 - 1x1) / 7 per-context costs from the published `*/ooc-*/baseline_hierarchy.rpt` (`review-evidence/pp230-r1/author-r1/vivado/`, milan-fpga `06fe795b`) |

The srp_top campaign ran as committed: `cd <tree>/tb/srp_top && TMPDIR=<scratch> VERILATOR=verilator-j.sh VJ=1 python3
mutants.py --output <scratch>/camp-out --jobs 6`.
