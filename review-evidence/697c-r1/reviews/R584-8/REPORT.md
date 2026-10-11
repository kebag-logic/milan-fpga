[R584] NEGATIVE - exact head feed95bbb6429e5af0ee3f0a24c531777279e9de

Round R584-8. Internal cleared-context delta review of issue #697 / PR #705 (lane 697c), round 9. Exact published
head `feed95bbb6429e5af0ee3f0a24c531777279e9de`, tree `434e9291e6ceb5bd32bcd63fd13f257ed6d82bed`. The delta is the
three commits `2d24214d`, `107aab30` and `feed95bb` on `4cab445a`. Source base `8b61b70902f3ebf118e56967277e2686731081bd`.

The verdict, findings and ledger draft were written before any earlier review report or probe was read
(`receipts/independent_pass_ledger.txt`, 18:21Z). The section on earlier findings was added after. It changed no
verdict.

## Verdict

NEGATIVE. One MINOR finding is open.

- **Round-9 item 1 is met, except for one point.**
  - Every Git call of the pin proof at this head goes through `ctrl_build.git`. Its environment sets
    `GIT_NO_REPLACE_OBJECTS=1` and `GIT_GRAFT_FILE=/dev/null/no-grafts`.
  - Disk bytes are hashed in Python, with no Git filter.
  - The whole tree is compared: paths, types, modes and blobs.
  - All five standing disguises are refused by name before any build, and the clean clone passes.
  - Both reviewers' probes now print a refusal.
  - My own mutants show that each property is held by a control that fails without it.
  - The point that fails: the census misses a Git program written in its dashed form (F1).
- **Round-9 item 2 is met.** The README now says 96. The figure check counts the self-test's own population. Each of
  the four figure controls is refused by name, at this head and in the hosted job logs.
- **No image byte changed.**
  - The delta touches no C, header, SV or Makefile.
  - The image fixture's ELFs and images are byte-identical at this head, at `4cab445a` and at the pre-move base
    `8b61b709`.
- F1 (MINOR) is the only open finding. The census does not see a Git program named in its dashed form
  (`git-ls-files`, `/usr/lib/git-core/git-ls-tree`). Such a call starts Git outside the helper while the census and
  all 30 pin controls pass. The assignment, the README and the PR body all say the census refuses this, and the
  stated limits do not exclude it.

## Scope as reconstructed

- **#697 acceptance 1 to 5:**
  - the owner decisions 6074086970 (MIT), 6074093506 (option (b)) and 6074191062 (`third_party/tsn-c-stack`);
  - the lane assignment 6091228902;
  - the pin ruling 6092176555 (`1a9f651c`: token-identical cores and byte-identical images);
  - the budget ruling 6107349992 (`firmware-unit` headroom is #716's).
- **The round-9 assignment 6107732413** (the pin class is ruled by construction):
  - one Git helper, with replacement objects and grafts disabled;
  - disk bytes hashed with no filter;
  - a whole-tree comparison;
  - a census with a planted mutant;
  - five standing disguise controls, plus the clean control;
  - both reviewers' probes must refuse;
  - the README figure checked against the self-test's population, with a planted mutant;
  - a STOP on any image byte change.
- **Authorities:**
  - CONTRIBUTING.md:474-494 (#236: a pin proved byte by byte, with `GIT_NO_REPLACE_OBJECTS=1` on every Git call that
    contributes to the decision);
  - AGENTS.md sections 6 and 7;
  - `sw/firmware/ctrl/README.md` (the stack section);
  - `docs/testing/CI_WORKFLOWS.md` (the firmware jobs).
- **Author REVIEW READY:** 6108314179. Its private evidence packet was not read.

## Findings

### F1 - MINOR - Conformance, Robustness, Tests, Docs - the census does not see a dashed Git program, so a Git call outside the helper passes every check

- **Where:**
  - `sw/firmware/ctrl/test/ctrl_pin.py:72`: `GIT_WORD = re.compile(rf"(?<![\w.-]){HELPER}(?![\w-])")`. The negative
    lookahead on `-` rejects `git-ls-files`, `git-ls-tree` and `/usr/lib/git-core/git-rev-parse`.
  - The census loop is at `ctrl_pin.py:125-131`.
- **Claims it falsifies:**
  - `sw/firmware/ctrl/README.md:169`: "every Git command it runs goes through one helper".
  - `README.md:173-174`: "A string of either module ... that names the Git program is refused ... A program name
    assembled at run time is not seen."
  - The docstring at `ctrl_pin.py:12-18`.
  - The PR body Status: "a census refuses any Git command the proof's modules start outside the helper".
  - The round-9 assignment 6107732413: "A census check fails if any module of the pin proof starts a Git process
    other than through the helper."
  - The stated limits (README, PR body Known limitations, REVIEW READY) name only a run-time-assembled name and
    another module's call.
- **Evidence** (`scripts/proof_mutants.py`, `receipts/mutants/`):
  - **M11.** `stack_gitlink`'s `git(root, "ls-files", ...)` becomes `run(["/usr/lib/git-core/git-ls-files", ...],
    cwd=root)`. This is a literal string, not assembled at run time.
    - Result: `rc=0`. The census reports `[]`, all 30 pin controls `[ok]` and all 4 figure controls `[ok]`.
    - So a Git process started outside the helper passes every check the round added.
  - **M8.** The same dashed form for `ls-tree` in `stack_pin`.
    - The census is again silent.
    - The replacement-tree and replacement-commit controls ESCAPE. The standing controls still catch that one,
      because it reads the pinned tree.
  - **M9.** The dashed `rev-parse HEAD`: the census is silent.
  - **M10.** The plain form `run(["git", ...])` is named by the census (`ctrl_build.py:249`), as designed.
  - `receipts/probes/dashed_git_programs.txt`:
    - `/usr/lib/git-core/git-ls-files`, `git-ls-tree` and `git-rev-parse` are symbolic links to `/usr/bin/git`
      (the same sha256).
    - So the string names the Git program itself, not another program.
  - No literal in either module at this head contains `git-` or `-git`, so dropping `-` from the lookahead would
    raise no false finding today.
- **Impact:**
  - A future Git call in the pin proof, written in the dashed form, bypasses the helper's environment with no
    census finding.
  - If it reads a tree or commit, the replacement controls still fail (M8).
  - If it reads anything else (the gitlink, `HEAD`, the object format), nothing fails (M11, M9).
  - The census is the mechanism the round uses to hold the class "by construction", and its published guarantee
    does not hold for one literal spelling.
  - No such call exists at this head, and the pin check itself is not weakened today. That is why this is MINOR and
    not MAJOR.
- **Required outcome:**
  - The census names any literal string, outside the helper and docstrings, that names the Git program in its
    dashed form (`git-<command>`, bare or with a path), as it names the plain form.
  - A standing census control plants such a call and must be refused by name.
  - Alternatively, if the manager rules the dashed form out of scope, that limit is stated in the README, the
    docstring and the PR body beside the run-time-assembly limit. The Status sentence "refuses any Git command"
    is then narrowed to match.
- **Verification:**
  - Rerun `scripts/proof_mutants.py <checkout> <scratch> <out> M11-dashed-ls-files-outside-helper
    M8-dashed-ls-tree-outside-helper`. The census line must name the planted line in `ctrl_build.py`.
  - `ctrl_boundary.py --selftest` lists the new census control `[ok]`.

### S1 - SUGGESTION - Robustness - a corrupted object store can stand in for the pinned tree

- `sw/firmware/ctrl/test/ctrl_build.py:235-260` trusts that the stack's object store holds, under each id, the
  object of that id.
- `receipts/probes/forged_object_probe.log` (`scripts/forged_object_probe.sh`):
  - In a disposable clone with loose objects, the pinned `src/` tree's object file is overwritten with a tree that
    holds an edited `adp.c`, and the edit is made on disk.
  - `git fsck` reports `hash-path mismatch`, but `ctrl_build.py --stack-pin` accepts the clone (`rc=0`).
- This is outside the class the round ruled (replacement objects, grafts, filters, modes). It needs a damaged
  repository rather than a Git feature, and CONTRIBUTING #236 asks no more than the helper does. So it is optional.
- Option: verify the pinned commit's bytes hash to the pin, and recompute the tree ids from the disk entries in
  Python, comparing the root with the commit's `tree`. Git's object store would then not be trusted at all.
- Option: soften README:170 "so Git reads the real objects only" to name the trust in the store.

### S2 - SUGGESTION - Robustness - the same replacement class outside the pin proof

- `sw/firmware/ctrl/test/ctrl_image.py:410-435`:
  - `extract` and `base_tree` are lane code.
  - `ctrl_image.py --base <rev>` reads the base firmware and the base's stack by `git archive`, with replacement
    objects honoured.
  - The base side of an image delta can therefore be read from a replaced tree.
- `sw/firmware/ctrl/test/aecp_wire.py:154-159` (#700's code) reads the processor reference trees the same way.
- Neither is part of the pin proof, and the round-9 STOP clause confines the helper to the proof's modules and
  callers. Applying `GIT_NO_REPLACE_OBJECTS=1` there, as `ctrl_reuse.py:55` does, would close the class in this
  directory.

### S3 - SUGGESTION - Tests - the Verilator figure counts every Verilator plant as a defect

- `sw/firmware/ctrl/test/ctrl_boundary.py:409-414` counts `plant.needs == "verilator"` with or without a `needle`.
- The README sentence it checks (README:158, "it plants 5 more", after "96 defects") reads as defects.
- All five are defects today (`receipts/baseline/pin_suite.log`, population line), so the check is right at this
  head. Counting `bool(plant.needle)` there would keep it right if a passing Verilator control is ever added.

### RES-1 - RESIDUE - Docs - the stack's suite instructions do not say the build directory must be outside the submodule

- `sw/firmware/ctrl/README.md:196-203` gives
  `cmake -S third_party/tsn-c-stack -B <build directory>` with no constraint.
- The stack's own README builds into `build/` inside its checkout.
- At this head the whole-tree pin check refuses any path the pinned tree does not hold, ignored files included.
  `receipts/probes/ignored_build_dir.log`: `build/...` is refused while `git status` is empty, and an empty
  directory is refused too. So following either README inside the submodule refuses every gate until the directory
  is removed.
- The PR body states this limit. The README does not.
- **Exact fix:** in `README.md:198`, replace "runs it, with GoogleTest and GoogleMock 1.14.0:" with "runs it, with
  GoogleTest and GoogleMock 1.14.0, from a build directory outside the submodule (the pin check refuses any file its
  pinned tree does not hold, a build directory inside it included):".
- This is pure wording. It changes no figure, test, code or verdict.

## Independent evidence

The clone is `$CLONE`, at the exact head. Host: Git 2.56.0, CPython 3.14, GCC 16. The RV32 compiler is the Bootlin
riscv32 SDK, GCC 14.3.0 (`$RV32_SDK`). This is not the CI container, and these are source-head runs.

| What | Result | Receipt (under `receipts/`) |
|---|---|---|
| Delta scope | 4 files: README, `ctrl_boundary.py`, `ctrl_build.py`, `ctrl_pin.py`. 0 paths under `hdl/ syn/ tb/` processors `third_party/ .github/`; 0 C/H/SV/Makefile | `delta_scope.txt` |
| Pin check, CLI, real submodule | `tsn-c-stack at 1a9f651c...`, rc 0 | `baseline/cli_pin.log` |
| Standing pin controls (`ctrl_pin.pin_controls`), census, figure check and figure controls, at head | 30 pin controls, 0 misbehaved: clean passes; replaced tree, replaced commit, graft, clean filter (checked to turn the edit into the pinned blob), mode, symbolic link, `LICENSE`, added header and the 3 census controls each refused by name. Census `[]`. Population 96/8/5/30 equals the README. 4 figure controls refused by name | `baseline/pin_suite.log` |
| Mutants of the proof, each restored | M1 (no `GIT_NO_REPLACE_OBJECTS`): both replacement controls escape and the census names it. M2 (no `GIT_GRAFT_FILE`): only the census names it, as stated. M3 (disk hashed through Git filters): the filter control escapes. M4 (modes ignored): the mode control. M5b (links followed): the link control. M6 (round 8's partial scope): the `LICENSE` control. M7 (extra paths ignored): the added-header control. M10 (plain `git` outside the helper): the census names it. M8/M9/M11 (dashed form): census silent (F1). M5 (link target hashed as bytes only) is still caught, by type. M9's rc 1 is the census control's anchor moving, not a census finding | `mutants/SUMMARY.txt`, `mutants/*.log` |
| Entry points on the real submodule, five disguises (`include/adp.h` to `ADP_ADVERTISE_MS 9000u` under a replaced tree, a replaced commit, a graft and a clean filter that leaves `git status` empty; a script made executable) | 45 of 45 refused, exit 2, naming the changed path, before any build: `ctrl_build.py --stack-pin`, `make stack-pin`, `make obj_fw/libctrlfw.a`, `test_ctrl_firmware.py --build-only`, `fw_coverage.py --build-only`, `maap_differential.py`, `aecp_arms.py --app`, `ctrl_image.py`, `ctrl_boundary.py`. Each disguise was undone and the clean pin re-accepted | `probes/entry_points_probe.log` |
| R584-7's `pin_replace_probe.sh` and R585-7's `pin_probe.py`, public bytes (sha256 equals their manifests), unchanged | R584-7 step 3 (`refs/replace/<pin>` to `ae982af`): `REFUSED`. R585-7: `replacement control: REFUSED ... include/adp.h`, compiler reads `9000u`, restored clone accepted | `probes/r584-7_pin_replace_probe_at_feed95bb.log`, `probes/r585-7_pin_probe_at_feed95bb.log`, `probes/public_probes_sha256.txt` |
| Config cannot re-enable replacement | `GIT_NO_REPLACE_OBJECTS=1` with `-c core.useReplaceRefs=true` still reads the real tree. Git has no `--replace-objects` option | Measured in scratch; recorded in this table |
| Images | `ctrl_image.py --base 4cab445a` and `--base 8b61b709`: both default shapes, `ctrl_app.elf` and `.img.bin` byte-identical, head against base (4 of 4 each); `+0` in every section | `image/elf_sha256.txt`, `image/elf_sha256_vs_8b61b709.txt`, `image/ctrl_image_base_*.log` |
| Docs gates at head | `docs_check.py` 0 findings (202 md); `ci_scope.py --selftest` PASS (the `feed95bb` fix); `check_py_idiom.py` every ratchet held; `check_em_dash.py --base 4cab445a` (pinned renderer) 0 findings | `docs_gates_head.txt` |
| Hosted, exact head (read-only) | 24 contexts success, 1 skipped (Physical gPTP, nightly/manual). `firmware-boundary` (job 114457347829, 12 min 06 s of 30): `0 finding(s), 105 boundary, 30 pin and 4 figure controls, 0 misbehaved`. `firmware-verilator` (job 114457347794, 11 min 35 s of 40): `6 boundary, 30 pin and 4 figure controls, 0 misbehaved`. Both checked out the merge `94ffdd8` (`feed95bb` into dev `6bfeeb13`). `firmware-unit` success in 39 min 01 s of 45 | `hosted_check_runs_feed95bb.tsv`, `hosted_boundary_extract.txt` |
| Clone restored | HEAD and tree exact; index writes the head tree; 0 flagged or unmerged entries; 1266 tracked files hashed from disk, 0 byte or mode differences; no replace refs or graft file; initialised submodules at their gitlinks, clean, no replace refs, grafts, attributes or filters; 0 untracked or ignored entries | `clone_restore_check.txt` |

### README claims at head, checked against the code

All claims are at `sw/firmware/ctrl/README.md`.

- **:151 and :158 (96 defects, 8 passing, 5 more):** equal to `PLANTS` (109 = 96 + 8 + 5).
- **:162-163 (figure check, figure controls):** confirmed.
- **:167-168 (whole tree, own bytes, no filter):** M3, M4, M5b and M6 above.
- **:170 (helper environment):** `ctrl_build.py:183-193`.
- **:179 (30 pin controls):** confirmed.
- **:180-185 (the standing controls):** confirmed.
- **:184 (a graft changes only parents):** confirmed. M2 escapes no proof control.
- **:169, :173-174 (the census):** see F1.

## Earlier public findings on this PR, at this head

These were read after the verdict above: R584-7 6107725598 and R585-7 6107554012, with their dispositions of rounds 1
to 6.

| Finding | State at `feed95bb` | Evidence |
|---|---|---|
| R584-7-F1, R585-7-F1 (the pin check follows replacement objects) | **Resolved.** One environment for every Git call; both public probes refuse; standing replacement-tree and replacement-commit controls; M1 shows they fail without the setting. One residual census gap is new as **F1** above | `probes/*`, `baseline/pin_suite.log`, `mutants/M1-*.log` |
| R584-7-F2, R585-7-F2 (README 95, gate 96) | **Resolved.** README:151 says 96, checked by `ctrl_boundary.figures` against `PLANTS`, with 4 figure controls; hosted logs show them `[ok]` | `baseline/pin_suite.log`, `hosted_boundary_extract.txt` |
| R584-7-RES1, R585-7-RS1 (stale "not pushed" lines in the PR body) | **Applied** in the body at this head: Status reads GREEN at `feed95bb`; the round-8 bullet links the manager's ruling; no "not pushed" remains. The residue checklist entry (#495) stays the manager's | PR body read 18:10Z |
| R584-7-S1 (cite exact-head hosted figures on the CI page) | **Retained SUGGESTION.** `CI_WORKFLOWS.md:96` still cites a replica at `0a9c5fa8`, which is accurate for that head. This head's hosted `firmware-boundary` took 12 min 06 s | `hosted_check_runs_feed95bb.tsv` |
| R584-6-S2 (executable mode not checked) | **Resolved** by the whole-tree mode comparison and its control (M4) | `mutants/M4-*.log` |
| R585-2-S2 (an explicit `--stack` still builds the submodule's tests in `aecp_arms.py`) | **Retained SUGGESTION.** Unchanged by the delta; stated in the PR body | PR body, Known limitations |
| R584-3-S1 remainder, R585-5-S1/R584-5-S3 (shell or compiled-helper absolute compiler paths) | **Retained** as documented limits. Unchanged by the delta | README:138 |
| R584-4-S2, R585-4-S1 (`firmware-unit` headroom) | **Retained**, #716's by the manager's ruling. Observation: hosted at this head took 39 min 01 s of 45 (87 %), above the 26 to 37 min dev range the ruling cites. The delta adds no work to that job | `hosted_check_runs_feed95bb.tsv` |
| All other round 1 to 6 findings (as tabulated in R584-7 and R585-7) | **Unchanged and still resolved.** The delta touches only the pin proof, the figure check and the README | `delta_scope.txt` |

## Lens ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #697 acceptance 1-5 and rulings 6091228902, 6092176555, 6107349992. Round-9 assignment 6107732413, item by item. CONTRIBUTING.md:474-494 (#236). `image/*` (4 of 4 identical vs `4cab445a` and `8b61b709`); `delta_scope.txt`; `probes/*`; `baseline/pin_suite.log`; `mutants/*` | R584-8 (applied; not clean) | `feed95bbb6429e5af0ee3f0a24c531777279e9de` |
| RTL | CLEAN | `delta_scope.txt` (no HDL, SV, contract, Makefile or processor gitlink in the delta); `image/*`; hosted `firmware-verilator` executing the bench, the MAAP differential and the AECP wire comparison (`hosted_boundary_extract.txt`); `tb/verilator/mbx/Makefile:79-115` (order-only `stack-pin`) refusing in `probes/entry_points_probe.log` | R584-8 | `feed95bbb6429e5af0ee3f0a24c531777279e9de` |
| Robustness | UNCLEAN (F1) | `ctrl_build.py:174-260` (helper, `on_disk`, `stack_pin`); `ctrl_pin.py:108-145` (census); `mutants/*`; `probes/entry_points_probe.log`; `probes/forged_object_probe.log` (S1); `probes/ignored_build_dir.log` (RES-1); Git config override probe | R584-8 (applied; not clean) | `feed95bbb6429e5af0ee3f0a24c531777279e9de` |
| Tests | UNCLEAN (F1) | `ctrl_pin.py:313-524` (`Clone`, 30 controls); `ctrl_boundary.py:152-161, 406-440` (figures, 4 controls); `mutants/*` (every new control fails for its defect, except the dashed census case); `baseline/pin_suite.log`; hosted control lines | R584-8 (applied; not clean) | `feed95bbb6429e5af0ee3f0a24c531777279e9de` |
| Docs | UNCLEAN (F1) | `sw/firmware/ctrl/README.md:145-203`; docstrings of `ctrl_pin.py:1-48`, `ctrl_boundary.py:77-98`, `ctrl_build.py:181-193, 235-240`; `docs/testing/CI_WORKFLOWS.md:57-112`; PR body (Status, Round 9, Known limitations); `docs_gates_head.txt` | R584-8 (applied; not clean) | `feed95bbb6429e5af0ee3f0a24c531777279e9de` |

[R584] PASS RTL - `receipts/delta_scope.txt`, `receipts/image/elf_sha256.txt`, `receipts/hosted_boundary_extract.txt` - checked against the round-9 STOP rule and acceptance 3:
- the delta changes no HDL, SV, Makefile, contract or processor gitlink;
- both image-fixture shapes are byte-identical against `4cab445a` and `8b61b709`;
- hosted `firmware-verilator` ran its Verilator builders at the head's merge and passed.

Only F1 is open, and it is filed under Conformance, Robustness, Tests and Docs. S1 to S3 are optional, and RES-1 goes
to the residue checklist. Neither changes this ledger.

## Real limits

- **Toolchain:**
  - Host Git 2.56.0, CPython 3.14 and GCC 16, not the CI container's CPython 3.12.3 and GCC 13.3.
  - `ctrl_pin.census` uses `Path.exists(follow_symlinks=...)`, which needs Python 3.12 or later. CI has 3.12.3, and
    the repository states no lower floor.
  - The RV32 compiler is a Bootlin riscv32 SDK (GCC 14.3.0), not verified here as the CI SDK archive. The image
    claim is head against base under one compiler, at the image fixture's two default shapes only. The 35-ELF
    manifest over every shape and composition was not rebuilt.
- **Not run:**
  - the full `ctrl_boundary.py --selftest` (its boundary controls are unchanged by the delta; its pin and figure
    parts were run directly and seen in the hosted logs);
  - the firmware, store and coverage suites and campaigns;
  - the full parent, PP, gPTP and Yosys banks;
  - act, the host `act_ci` and its self-test;
  - any hardware.
  - Physical calibration was NOT RUN. Field skips are not hardware proof.
- **Hosted** was inspected read-only. It ran on the PR merge ref `94ffdd8`, not the bare head.
- **No manager source bank ran at this exact head, and none is claimed.** Source-head execution evidence is the
  author's published receipts and the focused runs above.

## Pending manager duties

- Obtain a fix for F1 (or a public ruling that scopes the dashed form out, with the limit stated), and a re-review
  at the fixed head. A change to `ctrl_pin.py`, the README or the PR body un-covers the lenses it touches.
- Carry RES-1 (this round) and the R584-7 RES1 / R585-7 RS1 entry to the residue checklist (#495).
- Optional: rule on S1 to S3.
- Note the `firmware-unit` duration at this head (39 min 01 s of 45) against #716.
- At the merge turn, validate the current-dev candidate:
  - source base `8b61b70902f3ebf118e56967277e2686731081bd`;
  - live dev `6bfeeb132fa0b1ad8a5b957446c66a498e633af7`, or its successor;
  - with the builder and native banks, and link the receipts on the PR.
- Also outstanding: hosted and act acceptance, the external review, no round in flight, explicit maintainer merge
  authorization, post-merge containment and issue closure.

Only REPORT.md and the files listed in MANIFEST.sha256 are publishable. `scratch/` is excluded. Host paths in the
receipts are written `$PACKET`, `$CLONE`, `$RV32_SDK` and `$PINNED_VERILATOR`.

R584-8 FINISHED
