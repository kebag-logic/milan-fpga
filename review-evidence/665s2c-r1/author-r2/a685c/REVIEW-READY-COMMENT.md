[A685c] REVIEW READY
Commit: `de91db59d10d4e9e3de607f068ace7680f293fd7` on branch `665-s2c-icache`, not pushed. It adds six commits to the round-1 head `a611785f` (PR #796), on S2's final `f58d049b` (PR #792). Base: `dev-soft-core` `e76a755a`. S2's branch has not moved, so there is no re-base.

Changed: the answers to R713-1 and R714-1. There is no new measurement, and no measured cycle count changed.
- **R713-1-F1.** The six rows of the two "Paths that still miss T_svc" tables whose worst instance was never answered or never released now read "at least X, **never answered**" or "at least X, **never released**" in both ms columns. Their cycles cells are marked the same way, and a note above the tables says these are lower bounds that do not measure what the cache saves.
- **R713-1-F2 / R714-1-F2.** "in Vivado, one tile for each 4 KiB of data and half a tile of tags for each way" (README `:769`).
- **R713-1-F3.** Every S2 reproduction command on the page selects `--fetch-l1 none`: the controls, the fixture regeneration (which now gives the run that records the fixture) and a new Results block at both points. The page states that the default commands give the split cache's arms, and the cache section's controls name their command, with `--fetch-l1 64x1`.
- **R713-1-F4.** Two self-test checks drive `run.main()` on temporary files, with the build's toolchain steps replaced. They replace the check that compared `built_as()` with `selected()` only.
  - `the run builds and records the fetch L1 and the arm it selected` builds a `64x1` XIP build and a cacheless build, and reads what `build.json` records for `fetch_l1` and `xip`.
  - `the run refuses a reused build of another fetch L1 or arm and reuses the selected one; a build with no fetch L1 is cacheless` runs eight `--reuse-build` cases. Each must reach group setup or exit 2 with the refusal. One case is a build whose `build.json` records neither key.
  - Three new mutants: `reuse: a reused build is not compared with the selection`, `build: an XIP build records the block-RAM arm` and `build: the CPU is built with the split's cache whatever the selection`.
- **R714-1-F1.** `test_soc_options.py` restates `--fetch-l1 --fetch-l1-sets=64 --fetch-l1-ways=1` and requires it exactly. Both the constructor's options and `ctrl_cpu_args(CTRL_FETCH_L1)` must equal `--xlen=32` plus that string. Three new killed controls: 128 sets, two ways, 32 sets.
- **Residue.**
  - RES1/RS1: `build.py:149` and `:151`, "(#665, decision D3)" and "the saved-state flash driver (nvm_flash_litespi.c)". The check and mutant names say "the flash driver".
  - RES2: README `:746` and the PR body's XIP bullet, worded to what was measured.
  - RS2: `MARK_II_AREA_PLAN.md:897-898`.
  - RS3 and RS4: the PR body's Status, and "a CPU of 13 tiles" in README `:741`, `:745` and the PR body.
  - **The two exact texts for `build.py:149` differ.** RES1's is applied, keeping the D3 citation on `:153`. RS1's "(#665, the hybrid-XIP decision)" is not, so please re-file it if you prefer it.

Validation: at the head, rc 0 each, unpiped, with the tree clean after each.
- `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test`: 93 `PASS`, 70 `MUTANT caught`, `self-test: 0 failures`. The README's mutant table matches all 70 rows.
- `python3 sw/builder/test_soc_options.py`: `Split placement CPU: the 4 KiB direct-mapped instruction cache on the split CPU only, 6 killed controls`, then `RESULT: PASS`.
- `python3 scripts/check_baremetal_only.py --check`: `baremetal-only: OK`.
- The docs workflow's check-mode gates (87 commands, the pinned renderer and HDL parser), `git diff --check e76a755a HEAD`, the idiom, hygiene and TOC gates: rc 0 each. In all, 0 of 97 gates were nonzero or left the tree dirty. A first full run at `619e84e6` failed `py_idiom` on an undocumented nested function in the new check. `de91db59` documents it, and the whole set ran again from the start.
- `cd tests && behave`: 14 features, 406 scenarios, 1977 steps passed.
- `python3 sw/builder/test_builder.py --require-rv32`: `ALL GATES PASS EXCEPT 1 NOT RUN`. Gate 11 needs a local Arty build report, as in round 1.

Verification of the findings:
- F1: all 47 rows of the two miss tables, against the archived regrades of the 1x1 and 8x8 arms with and without the cache: 0 mismatches. The six unbounded rows carry their labels.
- F2: all 8 rows of the README's Vivado table satisfy 4.5 + size / 4 KiB + 0.5 per way.
- F3: the documented `--point 1x1 --fetch-l1 none --mutation slow-adp-rx`, rerun with this round's harness, measures `BUDGET control.discover.if0: 24.614 ms over T_svc 10 ms` and prints `CONTROL slow-adp-rx caught`, rc 0, the figure beside it. The documented fixture run (`--fetch-l1 none --groups fixture`), followed by `selftest.py --write-fixture`, reproduces the committed `fixture.log` and `oracle.json` byte for byte (`git status` empty).
- F4: R713-1's source mutants, replayed on a copy of the head, are killed. They are `run.py:317`'s condition set to `False` and `build.py:520`'s `spec['xip'] = False`, plus `run.py:321` building `split` whatever `--fetch-l1` says. The other five of R713-1's probes survive, as at round 1. They are outside this round's items.
- R714-1-F1: `probe_soc_geometry.sh`, run unchanged on a full copy of `619e84e6` (only `selftest.py` has changed since), gives `control rc=0`, `sets128 rc=1`, `ways2 rc=1` and `sets32 rc=1`.
- Comment rule: no lane or review label on any source line added since `f58d049b`. The same scan finds round 1's four lines at `a611785f`.

Acceptance criteria: issuecomment-6433542516 items 1 to 6 are met, and so are its gates. The PR stays "Relates to #665": T_svc is not closed, and NFR-SCOUT-01 awaits the owner.

Open risks/questions:
- The `build.py:149` wording choice above.
- The new build check stands a recorder in for the SoC export, which needs LiteX. `split_soc.build`'s own record of its selection is attested by each run's `build.json`, not by the portable self-test (README Limits).
- The optional suggestions were not taken: R713-1-S2 to S4, and R714-1-S1 and S2. R713-1-S1 is answered by R714-1-F1's fix.
