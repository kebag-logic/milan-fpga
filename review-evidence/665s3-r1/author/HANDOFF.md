# [A697c] #665 S3 round 2: the platform image's ledger entry, handoff

STATUS: **REVIEW READY** at `99de3a023abfda5604a70832e23baf7ff73481a3`, posted as issuecomment-6508205340 (text in `REVIEW-READY-COMMENT.md`); the PR body for base `dev-soft-core` is `PR-BODY.md`. Every gate the ruling's exit names, and every gate the change touches, passed at that head, rc 0 (table below). No STOP condition holds: the other points plan 39.0 / 42.0 / 52.0, the ledgered one exactly 59.0.

- Lane: S3 of the Mark II split (#665). Round 2 under [A10] issuecomment-6505997821 (the S3 ruling on [A697b]'s
  STOP, issuecomment-6505966612). Earlier rounds: `../665s3-a697/` ([A697], the code) and `../665s3-a697b/`
  ([A697b], the STOP).
- Branch `665-s3-platform`. Start `5edbba1d`; this round adds two commits:
  - `2adab625` Ledger the target platform's 8x8 two-interface image at 59.0 RAMB36 by its own symbols, owed to
    S14, with its refusals, its planted ledgers and three mutants (#665)
  - `99de3a02` Record the platform's 8x8 two-interface image as ledgered at 59.0 beside the fixture's 57.5, its
    four points beside the fixture's and its added bytes by part (#665)
- Base `origin/dev-soft-core` `f4c9ad4f` (fetched today; it has not moved), an ancestor of the head. Origin verified
  `https://github.com/kebag-logic/milan-fpga.git`. No submodule pin moved and no git command was run inside a
  submodule. No RTL, `milan_soc.py`, `.github/` or firmware C changed, so the full sweep is not run.
- Nothing pushed; no PR created or edited; no issue or PR comment edited. TAKEN was already posted for the lane.

## The ruling, item by item

| Item | Ruling | Done |
|---|---|---|
| 1 | Option (a): ledger the platform's 8x8 two-interface image at 59.0, owed to S14 (D3); a second `LEDGERED` entry recognising it by its own symbols; its test (that point only; a widening plant must fail); `SPLIT_CONTROL_MEMORY.md` section 5 with this head's figures at four points, both images, and the platform's added bytes by part. STOP if any other point is over 56 or this one over 59.0. | Done. Other points 39.0 / 42.0 / 52.0, this one 59.0 exactly: no STOP condition. |
| 2 | Graders on a split image accepted as listed; their split mode owed to S12; state it in the PR body's limits and in the plan's S12 entry. | PR body limits; the plan's S12 entry (additive bullet, see "Outside the tree"); also the platform and boot READMEs. |
| 3 | SRP's live stream configuration deferred to a later S3 round after S2b's `srp_mbx.c` lands; sources declare Talker Failed until then; state it in the PR body's limits. | PR body limits; the platform README's "Not yet done". |
| 4 | `scripts/run_litex_sims.sh` accepted as a recipe under `tb/verilator/ctrl_split_boot/` until #784 step 2. | PR body limits. |
| Exit | Re-run `ctrl_plat_image.py` at all four points, the `ctrl_memory` tests, the docs gates, the builder test and the firmware self-test. | Gate table. |

## Changes (file:line, reason)

### Code (`2adab625`)

| Where | What | Why |
|---|---|---|
| `sw/litex/ctrl_memory.py:216` | `LEDGERED["platform-8x8-two-interfaces"]`: `nvm_stage` 13,264 B and `ctrl_plat` 21,240 B, 59.0 RAMB36, owed to lane S14 (D3; ruling 6505997821 amending 6425357821 for this image). | Ruling item 1. The platform's image carries no `image_allocation`, so the fixture's entry refuses it; `ctrl_plat` is the platform's one static object, absent from the fixture, and its size at that point is the platform's at 8x8 with two interfaces (18,432 / 19,928 / 19,088 at the other three points, measured). |
| `sw/litex/ctrl_memory.py:197-211` | The `LEDGERED` comment: both entries, the second symbol of each, and that a change to `struct ctrl_plat` refuses the override until its size is measured again. | The coupling is deliberate and stated: the entry names one measured image. |
| `sw/litex/ctrl_memory.py:21-24`, `:430` | The module docstring and `plan --ledgered-point`'s help: "the images", "a ledgered point's image". | Two entries now. `RULES` and the `budget` rule text are unchanged, so section 3's rule table still equals them. |
| `sw/litex/ctrl_memory_ledger.py` (new, 121 lines) | The ledger's cases for the test: `OWN` (each point's own image), `HELD` (the pinned entries), `REFUSED` (18 cases, each refused by `budget`), `refusals()` (the refusal rows), `facts()` (acceptance and the CLI's exit codes), `planted()` (six widened ledgers). | `test_ctrl_memory.py` was 985 lines and the idiom gate caps a module at 1,000 (`long module` ratchet 10, may only fall), so the ledger's cases live beside it, as its ELF writer does (`ctrl_memory_elf.py`). Not a `test_*.py`, so `run_litex_sims.sh`'s UNLISTED rule does not apply; it names no firmware path, so the boundary gate does not see it as a builder. |
| `sw/litex/test_ctrl_memory.py:191-192` | `Layout` gains `plat` (the `ctrl_plat` symbol) and `text` (.text's size; `elf()` places .rodata and .data's load after it). | A synthetic image's `rom` was fixed at 3 tiles and `sram` caps at 56, so it could not reach 59.5. |
| `sw/litex/test_ctrl_memory.py:229` `ledger_elf` | A ledger case as an ELF: one tile moved from .bss to .text (still 56.0), then a granule of .bss per half tile. | Reaches 60.0. |
| `sw/litex/test_ctrl_memory.py:311` | The ledger's refusal rows come from `ledgers.refusals()`, plus `add_ctrl_memory` on each point's own image. | Replaces the fixture-only rows (all kept as cases). |
| `sw/litex/test_ctrl_memory.py:322` `ledger_arms` | The pin (`held == ledgers.HELD`), then `ledgers.facts()`. | |
| `sw/litex/test_ctrl_memory.py:338` `ledger_plant_arms`, `:981` | Each planted ledger graded with the pin set aside: by a fact or a refusal row; only if the rules arm passed unmutated. | Ruling item 1's "a planted defect that widens it to another point or image must fail". |
| `sw/litex/test_ctrl_memory.py:768`, `:808-812` | Three `ledgered_tiles` mutants. | `ledgered_tiles` had no mutant. |
| `sw/litex/test_ctrl_memory.py:19-25` | Docstring item 2. | |
| `sw/firmware/ctrl/test/ctrl_plat_image.py:103` | `--ledgered-point` help names the platform's entry. | |
| `sw/firmware/ctrl/test/ctrl_srp_image.py:110` (shared) | Help: "a ledgered point's image" for "the one ledgered point". | One line; S2b's branch does not have this option yet, so no overlapping edit. |

### Docs (`99de3a02`)

| Where | What |
|---|---|
| `docs/design/SPLIT_CONTROL_MEMORY.md:91-109` (section 3) | The two entries as a table (name, image, symbols, tiles); how each is recognised; the `struct ctrl_plat` coupling; who names which override. |
| `docs/design/SPLIT_CONTROL_MEMORY.md:115-126` | The test's description: both points, the cross-image refusals, the six planted ledgers, the three mutants. |
| `docs/design/SPLIT_CONTROL_MEMORY.md:214-257` (section 5) | This head's figures at all four points for both images and their difference; the 59.0 ledger (ruling 6505997821, D3, amending 6425357821 for this image); every other point within 56; S13's bar; why 57.5 cannot be reached in the platform's files; the platform's added `rom`/`sram` by part at all four points; the five largest `.bss` at the shipping and the largest point. |
| `docs/design/SPLIT_CONTROL_MEMORY.md:316-326` (section 6) | The platform's command at the ledgered point. |
| `docs/design/SPLIT_CONTROL_MEMORY.md:16`, `:18` | The two Contents descriptions (human-owned; `gen_toc.py --check` passes). |
| `sw/firmware/ctrl/plat/README.md:94-96`, `:114-116` | The 59.0 point and its override; SRP's live configuration deferred (item 3); the graders (item 2); the largest point's block RAM. |
| `tb/verilator/ctrl_split_boot/README.md:79-80`, `:97` | The 59.0 point is ledgered (this simulation names no override, so builds no SoC for it); the graders ruled. |
| `tb/verilator/ctrl_service_budget/README.md:44` (shared, S2's harness) | "the size fixture's ledgered point in the planner" for "the planner's one ledgered point". One line; S2b's branch does not carry this line yet. |

### Outside the tree

- The plan's S12 entry (`665-a678/PLAN.md`, the manager's plan): one additive bullet, "The graders' split mode
  (ruling 6505997821 item 2)", with the two graders. sha256 before and after: `receipts/plan/PLAN-sha256.txt`.

### Shared files touched this round

`sw/litex/ctrl_memory.py`, `sw/litex/test_ctrl_memory.py` (S1/S2's), `ctrl_srp_image.py` (one help line),
`docs/design/SPLIT_CONTROL_MEMORY.md` (S2b edits other sections), `tb/verilator/ctrl_service_budget/README.md`
(one line). S2b's `origin/665-s2b-cycles` (`bf1773c0`) changes neither `sw/litex/ctrl_memory.py` nor
`test_ctrl_memory.py`.

## New checks, planted defects and failing words

All in `sw/litex/test_ctrl_memory.py`, at `2adab625` (log `receipts/gates-at-99de3a02/test_ctrl_memory.log`).

### Each override plans its own image (facts)

| Check | Words |
|---|---|
| the pin | `the ledger holds the ruled points, the size fixture's and the target platform's 8x8 images with two interfaces at 57.5 and 59.0` |
| fixture's acceptance | `the 8x8-two-interfaces override plans its own point's image: 57.5 RAMB36, against the 56-RAMB36 budget and its ledgered 57.5` |
| platform's acceptance | `the platform-8x8-two-interfaces override plans its own point's image: 59.0 RAMB36, against the 56-RAMB36 budget and its ledgered 59.0` |
| the CLI, fixture | `` `plan --ledgered-point 8x8-two-interfaces` accepts its point's image and refuses the 7 cases its override must (exit codes [0, 2, 2, 2, 2, 2, 2, 2]) `` |
| the CLI, platform | `` `plan --ledgered-point platform-8x8-two-interfaces` accepts its point's image and refuses the 8 cases its override must (exit codes [0, 2, 2, 2, 2, 2, 2, 2, 2]) `` |

### Refused by `budget` (`ctrl_memory_ledger.REFUSED`, plus two rows each)

Without its override and through `add_ctrl_memory`, for each point; then: the fixture's override on its image at
58.0, on the fixture's 1x1 one-, 1x1 two- and 8x8 one-interface images at 57.5, on an 8x8 image with no
`image_allocation`, on the 1x1 one-interface image within the budget, on the platform's image at 57.5; the
platform's override on its image at 59.5, on the platform's 1x1 one-, 1x1 two- and 8x8 one-interface images at
59.0, on an image with the point's `ctrl_plat` and the 1x1 stage, on an 8x8 image with no `ctrl_plat`, on its 1x1
image within the budget, on the fixture's image at 59.0; and three names the ledger does not hold.

### The six planted ledgers (`ctrl_memory_ledger.planted`), each graded with the pin set aside

| Plant | Caught by (first failure) |
|---|---|
| the platform's entry without its staging buffer | `` `plan --ledgered-point platform-8x8-two-interfaces` accepts its point's image and refuses the 8 cases its override must (exit codes [0, 2, 2, 2, 2, 0, 2, 2, 2]) `` (the image with the point's `ctrl_plat` and the 1x1 stage accepted) |
| the platform's entry without `ctrl_plat` | the same fact, exit codes `[0, 2, 2, 2, 0, 2, 0, 2, 0]` (the 8x8 one-interface platform image, the 8x8 image with no `ctrl_plat` and the fixture's image accepted) |
| the platform's entry at the 8x8 one-interface `ctrl_plat` | `the platform-8x8-two-interfaces override plans its own point's image: raised Refusal (...)` |
| the platform's entry at 59.5 RAMB36 | `the platform-8x8-two-interfaces override plans its own point's image: 59.0 RAMB36, ... ((59.0, 56, 'platform-8x8-two-interfaces', 59.5))` |
| the size fixture's entry without `image_allocation` | `` `plan --ledgered-point 8x8-two-interfaces` ... (exit codes [0, 2, 2, 2, 0, 0, 2, 0]) `` |
| the size fixture's entry at the platform's 59.0 | `the 8x8-two-interfaces override plans its own point's image: 57.5 RAMB36, ... ((57.5, 56, '8x8-two-interfaces', 59.0))` |

### The three `ledgered_tiles` mutants (`MUTANTS`, arm `checks`)

| Mutant | Edit | Caught by |
|---|---|---|
| an override on any image | `if carried != dict(point.symbols):` -> `if False:` | the fixture's CLI fact, exit codes `[0, 2, 0, 0, 0, 0, 0, 0]` |
| an override on any image carrying its symbols | -> `if None in carried.values():` | the same, `[0, 2, 0, 0, 0, 2, 0, 2]` |
| an override on any image with its staging buffer | -> `if carried[STAGE_SYMBOL] != dict(point.symbols)[STAGE_SYMBOL]:` | the same, `[0, 2, 2, 2, 0, 0, 2, 0]` |

### Measured on the real images (`receipts/gates-at-99de3a02/images/`)

The platform's override accepts its own 8x8 two-interface image at 59.0 and refuses, exit 2, the platform's
1x1 one-, 1x1 two- and 8x8 one-interface images (`this image carries {'nvm_stage': 3344, 'ctrl_plat': 18432}`,
`... 19928}`, `{'nvm_stage': 13264, 'ctrl_plat': 19088}`) and the fixture's 8x8 two-interface image
(`'ctrl_plat': None`). The platform's 8x8 two-interface image is refused without an override (`59 RAMB36 ... exceeds
the 56-RAMB36 budget`) and under the fixture's (`'image_allocation': None`).

## Gate table

Every gate at `99de3a02`, each in a fresh clone of the head (submodules at their gitlinks), each its own transient
unit (MemoryMax 10G, `systemd-run --wait`) on a CPU range of its own (two chains of serial steps, `scripts/chain_a.sh`
and `scripts/chain_b.sh`); the tree was clean after every one. Receipts: `receipts/gates-at-99de3a02/`.

| Gate | Command | Result | rc | s | Receipt |
|---|---|---|---:|---:|---|
| the memory test | `python3 sw/litex/test_ctrl_memory.py` | `RESULT: PASS`: 0 failures; 47 mutants caught (3 new on `ledgered_tiles`); 6 of 6 planted ledgers caught; the link arm ran | 0 | 84 | `test_ctrl_memory.log` |
| the memory test at `2adab625` | same | same | 0 | 92 | `at-2adab625/test_ctrl_memory.log` |
| `ctrl_plat_image.py` at four points, and the fixture's | `scripts/images.sh` | platform 39.0 / 42.0 / 52.0 / 59.0 (the last under `platform-8x8-two-interfaces`), fixture 37.0 / 40.5 / 50.5 / 57.5 (the last under `8x8-two-interfaces`); every ELF byte-identical to `2adab625`'s | 0 (8 runs) | 69 | `images/image-*.log`, `images.log` |
| the six refusals | same script | the platform's largest point without an override and with the fixture's; the platform's override at its three other points and on the fixture's largest image: each refused by `budget` | 2 (6 runs, each wanted 2) | | `images/refuse-*.log` |
| the docs, scope, idiom, harness self-test, CPU options, `git diff --check` and rtl-fast's bdd-conformance | `scripts/docs_gates.sh` (`gates_s3.py`, 97 gates, one at a time; this round adds `ci_scope.py --selftest`) | 0 of 97 nonzero; `behave` 14 features, 406 scenarios, 1977 steps passed | 0 | 1509 | `docs/summary.md`, one log per gate |
| end-station builder | `python3 sw/builder/test_builder.py --require-rv32` | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11, the calibration report of a local Arty build, as at the base and at `5edbba1d`) | 0 | 1501 | `builder_require_rv32.log` |
| TSN stack boundary, without Verilator (two builders' help text changed) | `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator` | `ctrl_boundary: PASS`, 0 findings; 112 boundary, 167 pin and 4 figure controls | 0 | 1133 | `ctrl_boundary-without-verilator.log` |
| firmware self-test, shard 0 (suites) | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4 --jobs 8` | PASS; arms `plat`, `platboot` x2, `platrv32`, `plattrace` | 0 | 384 | `selftest-shard0.log` |
| firmware self-test, shard 1 (control campaign) | `... --shard 1/4 --jobs 8` | 565 of 565 caught, the 37 platform defects among them | 0 | 1336 | `selftest-shard1.log` |
| firmware self-test, shard 2 (AECP campaign) | `... --shard 2/4 --jobs 8` | 137 caught, as at `5edbba1d` | 0 | 510 | `selftest-shard2.log` |
| firmware self-test, shard 3 (SRP campaigns, pin controls) | `... --shard 3/4 --jobs 8` | 278 caught and the 2 lwSRP pin controls, as at `5edbba1d` | 0 | 830 | `selftest-shard3.log` |

Not re-run this round, because nothing they read changed (no firmware C, header, generator, RTL or harness code):
the saved-state store and its mutants, `fw_coverage.py`, the MAAP differential, the Verilator boundary leg, the
split boot simulation and its plants, `fw_rv32_selftest.py`, `tally_selftest.py` and the CPU budget harness's two
points. [A697b]'s runs of each at `5edbba1d`, with the same firmware bytes, are in `../665s3-a697b/receipts/`. The
full sweep and Vivado: no RTL changed; no route is owed by S3.

## Measurements

### Linked images (`receipts/gates-at-99de3a02/images/`, the same at `2adab625`: `receipts/at-2adab625/images/`)

One runtime for all (the split boot simulation's archives, sha256 equal to [A697b]'s measurement:
`images/image-inputs.sha256`); the platform against the boot SoC's `csr.csv` for its shape. Every ELF, plan,
section list and `.bss` report at `99de3a02` is byte-identical to `2adab625`'s, and the figures equal [A697b]'s at
`5edbba1d` (no firmware changed this round).

| Point | Platform `rom` / `sram` need, B | Platform RAMB36 | Fixture `rom` / `sram`, B | Fixture RAMB36 | Delta, B |
|---|---|---:|---|---:|---|
| 1x1, one interface | 109,552 / 47,168 | 39.0 | 104,448 / 46,272 | 37.0 | +5,104 / +896 |
| 1x1, two interfaces | 111,192 / 58,592 | 42.0 | 106,032 / 57,648 | 40.5 | +5,160 / +944 |
| 8x8, one interface | 123,296 / 87,760 | 52.0 | 118,168 / 86,848 | 50.5 | +5,128 / +912 |
| 8x8, two interfaces | 125,040 / 113,936 | **59.0**, under `platform-8x8-two-interfaces` | 119,824 / 113,008 | 57.5, under `8x8-two-interfaces` | +5,216 / +928 |

No point but the ledgered one is over 56, and it is exactly 59.0: neither STOP condition of item 1 holds.

### The platform's added bytes by part (`receipts/gates-at-99de3a02/parts/`, the same at `receipts/at-2adab625/parts/`; `scripts/parts.py`)

From the two link maps (one section per function and object): every linked input section is attributed to one
part, platform minus fixture; alignment is the fill plus the gaps each need holds beyond its sections, so the
parts sum to the measured delta at every point. `sram` by member of `struct ctrl_plat` (its sizes from
`ctrl_plat_image.py`'s member probe) against the fixture's objects of the same types. The table is in
`SPLIT_CONTROL_MEMORY.md` section 5; at the largest point: boot +1,692 / +144, CSR policy +788 / 0, console
+1,744 / +588, strings +762 / 0, MAAP's port +916 / +32, ACMP +164, SRP +48, AECP +12, `main` +224 / +56, bus port
+16, the rest of `struct ctrl_plat` -80 / +114, the fixture's `main` removed -1,088, other objects +16, alignment
+2 / -6: total +5,216 / +928.

## Other notes

- The platform's entry is keyed on `ctrl_plat`'s exact size at that point (21,240 B), as the fixture's is keyed on
  `image_allocation`'s. A change to `struct ctrl_plat` (the later SRP round's adapter entry will add to it) makes the
  override refuse the image, naming both sizes, until the entry is measured and updated; this is stated in
  `ctrl_memory.py` and section 3.
- `MARK_II_AREA_PLAN.md`'s firmware ledger carries the mapped figures of an earlier image (54 tiles as mapped at
  8x8 with two interfaces) and was not updated at 57.5 either; the ruling does not name it, so it is unchanged.
- `ctrl_srp_image.py --ledgered-point` now also offers the platform's name; on the fixture's image it is refused
  (`receipts/gates-at-99de3a02/images/refuse-fixture-8x8-if2-platform-override.log`).
- Scratch on disk for reproduction: `$VALIDATION_STORAGE/665s3-a697c` (the clones at both heads, the images, the
  copied runtime archives and boot-SoC maps, the HDL-reference venv). Nothing of this lane's is in tmpfs `/tmp`.
- Helper scripts: `scripts/` (`chain_a.sh`, `chain_b.sh`, `unitw.sh`, `gate.sh`, `clone.sh`, `images.sh`,
  `parts.py`, `ledger_quick.py`, `docs_gates.sh`, `gates_s3.py`, `finalize_receipts.py`).
