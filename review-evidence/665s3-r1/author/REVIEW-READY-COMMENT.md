[A697c] REVIEW READY
Commit: `99de3a023abfda5604a70832e23baf7ff73481a3` on `665-s3-platform`, 17 commits on `dev-soft-core` `f4c9ad4f` (nothing pushed). The PR body is prepared for base `dev-soft-core`, "Relates to #665".

Changed, per the S3 ruling (issuecomment-6505997821), in two commits on `5edbba1d`:
- **Item 1, option (a).** `2adab625`: `sw/litex/ctrl_memory.py` `LEDGERED` gains `platform-8x8-two-interfaces`, which plans the platform's 8x8 two-interface image to 59.0 RAMB36, owed to S14 under D3.
  - It recognises the image by its own symbols, as the fixture's entry does by `image_allocation`: `nvm_stage` of 13,264 B (the 8x8 shape's) and `ctrl_plat` of 21,240 B. `ctrl_plat` is the platform's one static object, which the fixture lacks; it is 18,432 / 19,928 / 19,088 B at the other three points.
  - A change to `struct ctrl_plat` therefore refuses the override until its size is measured again. This is stated in the code and in section 3.
  - Its test, in `test_ctrl_memory.py`, with the cases in a new `sw/litex/ctrl_memory_ledger.py` (the test module sits at the idiom gate's 1,000-line ceiling). Each override plans its own image and is refused, by `budget`, on 18 other cases: every other point of both images, the other override's image, an 8x8 image carrying one of its two symbols alone, half a tile past its tiles, and three unknown names.
  - Six planted ledgers each widen one entry to another point or image, or past its tiles: the platform's without its staging buffer, without `ctrl_plat`, at the 8x8 one-interface `ctrl_plat`, or at 59.5; the fixture's without `image_allocation`, or at 59.0. Each is caught with the ledger's pin set aside.
  - Three new mutants of `ledgered_tiles` are caught: any image, any image carrying its symbols, any image with its staging buffer.
- **Section 5.** `99de3a02`: `docs/design/SPLIT_CONTROL_MEMORY.md` section 5 now has both images at all four points, the 59.0 ledger, and the platform's added `rom` / `sram` by part at each point. The parts come from the two link maps and sum exactly to each delta. At the largest point, +5,216 / +928 B:

  | Part | `rom` | `sram` |
  |---|---:|---:|
  | boot | +1,692 | +144 |
  | CSR policy | +788 | 0 |
  | console | +1,744 | +588 |
  | strings | +762 | 0 |
  | MAAP port | +916 | +32 |
  | ACMP / SRP / AECP ports | +164 / +48 / +12 | 0 |
  | `main` | +224 | +56 |
  | the rest of `struct ctrl_plat` | -80 | +114 |
  | the fixture's `main`, removed | -1,088 | 0 |
  | other objects and alignment | +18 | -6 |

  Sections 3 and 6 now cover the two entries, their test, and the platform's command.
- **Items 2 to 4** are stated in the PR body's limits and in the platform's and the boot simulation's READMEs. Item 2 is also added to the plan's S12 entry. One line of the CPU budget harness's README now names the fixture's entry.

Measured at the head, each run in its own clone: the platform plans 39.0 / 42.0 / 52.0 / **59.0**, the last under its override. The fixture plans 37.0 / 40.5 / 50.5 / 57.5, unchanged, and every ELF is byte-identical to `2adab625`'s. The platform's largest image is refused (exit 2) without an override and under the fixture's. The platform's override is refused at the platform's three other points and on the fixture's largest image. Neither STOP condition holds.

Validation at `99de3a02`, all rc 0, each a transient unit of its own:
- `python3 sw/litex/test_ctrl_memory.py`: RESULT: PASS (47 mutants, 6 of 6 planted ledgers caught);
- `ctrl_plat_image.py` and `ctrl_srp_image.py` at the four points (8 runs, rc 0), and the six refusals (rc 2, as wanted);
- the docs, scope and idiom gates, the CPU budget harness's self-test, the CPU options test, `ci_scope.py --selftest`, `git diff --check` and rtl-fast's bdd-conformance: 97 gates, 0 nonzero; `behave` 14 features, 406 scenarios, 1977 steps;
- `python3 sw/builder/test_builder.py --require-rv32`: all gates pass except gate 11, which is not run, as at the base (it needs a local Arty build report);
- `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator`: PASS, 0 findings;
- `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test`, four shards: the platform arms; the control campaign 565 of 565; AECP 137; SRP 278 and 2 pin controls.

No firmware C, header, generator, RTL or harness code changed this round. So [A697b]'s runs at `5edbba1d` stand, on the same firmware bytes, for: the saved-state store, coverage, the MAAP differential, the Verilator boundary leg, the split boot and its plants, and the CPU budget harness. The full sweep is not run.

Acceptance criteria: met as ruled. The graders' two differences are listed, with their split mode owed to S12. The largest point is ledgered at 59.0, owed to S14. Every other point is within 56.
Open risks/questions: SRP's live stream configuration waits for the later S3 round (item 3), and its adapter entry will change `struct ctrl_plat`, so that round re-measures this entry's `ctrl_plat` size. The area plan's firmware ledger (`MARK_II_AREA_PLAN.md`) carries mapped figures of an earlier image; the ruling does not name it, so it is unchanged.
