[A592] REVIEW READY (round 8)
Commit: d5cd863561ba1ee7bc6342fb1b00f57dd786bd97 on `671-read-fault`. There are two new commits on `9b32002c`: `f3bb2014` (merge commit of dev `fa820988`) and `d5cd8635` (capture re-measure). No push, rebase or amend.

Answers [the round-8 assignment](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6161596895).

Changed:
- **Merge (item 1).** `git fetch origin dev` gave `fa820988`, and `f3bb2014` merges it with a merge commit. Git merged it with no conflict and no hand resolution.
  - The paths that differ from dev are exactly this branch's own 15, byte-identical to `9b32002c` at the merge.
  - The merge's delta is exactly dev's 160 paths since `c6bd08c6`.
  - The only gitlink change is dev's new `third_party/tsn-c-stack` (`70936b77`). The processor pins stay at `2ad2f845` (protocol) and `7dda9c3b` (gPTP).
- **Re-measure (item 3).** Seven dev-changed RTL files are in the capture simulation's own source list: MAAP (#696), the stream frame counters (#726) and `milan_datapath.sv`. So all six capture arms were re-measured at `f3bb2014` through `tb/verilator/nvm_capture_cpu/run.py`, with round 7's unchanged driver and the receipt's simulator, Verilator 5.052.
  - The 8x8 contract maximum is 13.86328 ms against 24.5 ms: 10.63672 ms of margin and 3.5345x the 49 ms floor.
  - All 96 captures repeat round 7's cycle counts, capture for capture. Every arm's CPU netlist, firmware, BIOS, microcode and configuration hashes and its generated headers equal round 7's.
  - `d5cd8635` changes only the receipt (date, base, tree, assignment, provenance) and section 18's matching lines in `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md`, both written by their generators.
- **What holds without re-measure (item 3).** The firmware is byte-identical. Recompiled against the merged headers, its delta is again +2,050 B text and +16 B bss, so the product-header figures stand. The boot read-cost estimate holds: its CPU, BIOS, flash controller and model are unchanged, dev's SoC-generator change is an opt-in placement neither harness uses, and the cycle-exact capture repeat shows CPU and memory timing unchanged. The backend-only area rows hold, since that module is unchanged. The writer-gate time estimate holds, since that suite is unchanged.
- **Superseded attempt.** An interrupted first attempt measured with Verilator 5.050 first on `PATH`; it ran five arms and killed the sixth. The receipt and harness README record 5.052, so that attempt does not feed the receipt; it is recorded as superseded.

Validation (all rc 0; mutation controls rc 1 as required):
- At the merge `f3bb2014`, which differs from the final head only in the receipt and the design document:
  - writer gate: 5 shapes × 3,550 cases, 61 planted firmware defects and the 9 comparison-check arms;
  - all 18 #671 controls in full on three shapes: 54/54 counts equal to round 7;
  - term census, matrix and views;
  - co-simulation: 465/465 checks, 39/39 mutants;
  - service budget;
  - all 103 builder functions, with every elaboration arm. The two NOT RUN entries are unchanged and not counted;
  - the four control-firmware phases, the Mark II store (435 tests, 109 plants), coverage and the firmware boundary;
  - lint, source lists and BDD (406 scenarios);
  - the docs-check replica: 78 of 81 positions run, the other 3 covered by the builder, writer-gate and capture-gate receipts.
- At `d5cd8635`:
  - `check_nvm_capture.py` passes, and its five mutation arms reject by name;
  - C and Python idiom, hygiene and all the doc gates; `git diff --check` against the tree, `e8454e27` and `fa820988`;
  - the docs-check replica again;
  - `scripts/ci_scope.py --selftest`, `scripts/ci_events.py --check` (2,174 items) and `--firmware-census`;
  - `scripts/act_ci.py --selftest` in both layouts, inside a disposable read-only, networkless container only.

Acceptance criteria: unchanged from round 7; this round changes no firmware, test, register map, record format, A/B guarantee or processor source.

Open risks/questions:
- The verdicts R602-7 and R603-7 are at `9b32002c`; this head needs the assigned reviews.
- Exact-head hosted and act evidence comes after publication.
- Both builder NOT RUN entries are as in round 7.
- The boot read cost remains an estimate.
