[A768] STOP
Head: `f58347dfd90d8ef41161f64f4c2dd329a7afd670` (branch `883-adopt-processor-801ef228`, from dev `46c971fa`; nothing pushed)

**Why STOP: FPGA-gPTP `a64be73d` fails a gate every PR to dev runs, so acceptance items 1 and 5 cannot both hold.**
- Gate: docs.yml `docs-gates-0` `gate_39`, `python3 scripts/check_py_idiom.py`. At dev `46c971fa` (gPTP `1616fc8f`) it exits 0; at this head it exits 1: `long module 11 > ratchet 10`, `unannotated public function 4 > ratchet 0`, `undocumented public function 4 > ratchet 0`.
- Every finding is FPGA-gPTP PR #103's test code: `tb/verilator/engine/mutants.py` grew from 999 to 1080 lines; `named_verdict` (line 890), `run_mutant` (926), `in_list_order` (986) and `planted` (1044) are unannotated; `control` (1041), `planted` and `task` (1045) are undocumented; `tb/mutation_jobs_test.py` `main` (66) is undocumented.
- The gate scans both project submodules by design (`scripts/code_quality_scope.py` `PROJECT_SUBMODULES`), and its budget may only go down. Raising the ratchet or narrowing the scope would weaken the gate, so I did neither.

**Decision needed, with my recommendation first:**
- (b, recommended) Keep `gptp-processor` at `1616fc8f` in this adoption and carry FPGA-gPTP #103 with a follow-up into the next one. #103 changes no `hdl/`, `syn/` or ROM byte, so the release image, the route and every test below are identical at either gPTP pin; the processor fixes for #857, #858 and #860 ship now.
- (a) A small FPGA-gPTP follow-up under #102 (annotate the four functions, document the four, bring `mutants.py` to 1000 lines or fewer), then this lane moves the gitlink to that `main` and re-runs only the docs gates.
- (c) A ruling to raise the parent ratchet. Not recommended.

**Everything else is done and measured, at this head unless named:**
- Item 1: both gitlinks move, each a fast-forward of the old pin on its donor's `main`.
- Item 2: the #495 rows: the parent C++ idiom gate's brace-initialiser miscount fixed with three selftest arms, its planted old pattern failing the new arm by name; the milan_dp Makefile line of row 6731336971; processor-side rows 6758048783 and the FPGA-gPTP row 6777009988 are donor files, dispositioned to the donors. One more parent change the pin needs: since processor #216 the #851 `[ONEVEC]` control ("the encoder never merges") survived; it now removes both layers, as the processor's own arm does, and is caught.
- Item 3, AX7101 1x1: crflic `[MRPAPP]` (802.1Q-2018 Table 10-3, 10.7.6.3; #860) and `[MVRPLA]` (10.7.9, Table 10-5, Milan v1.2 Table 4.3; #857) pass 458 / 458 and fail 7 at the old pins; notify `[AIDX]` (1722.1-2021 Table 7-2, 6.2.2.15; #858) passes 535 / 535 and fails 4 at the old pins. `crflic-mutants` 16 / 16, `gsi-mutants` 19 / 19, `unb-mutants` 6 / 6.
- Item 4: the AX7101 1x1 route at `a89802c8` (synthesis inputs equal this head's), the three #818 directives from one synthesis checkpoint, every directive over the +0.030 ns floor at every corner. Best, ExtraPostPlacementOpt: +0.334 / +0.017 ns, 53,461 LUT, 54,971 FF, 15,849 slices (1 free); against `46c971fa` at the same directive -73 LUT, +121 FF, +29 slices, RAM and DSP unchanged. The resource gate passes all three endpoints against the sixteenth record; re-recorded as the seventeenth (NFR-RES-01's shipping-image accounting). One slice of margin is left.
- Item 5: the full sweep as 4 native-shards units, 65 / 65 suites, 2,192,633 checks, 0 failures (at `6c6706e5`; this head adds only the baseline JSON and four doc pages, which no suite reads), the consumer legs among them (milan_dp's 19 legs with gptp and gptp-lat); every `run:` step of rtl-fast, rtl, docs and elaborate on fresh clones of this head, 164 rc 0 and 507 not run with a reason, **one failing: `gate_39`, the finding above**; `test_builder.py --require-rv32` rc 0; `git diff --check` against the merge base rc 0.

**Pre-existing, for a new issue:** `make dynmap-mutants` on a fresh clone runs its listener leg without `tb/verilator/milan_dp_render`'s ROM images (built with `-o` on them), so that clean control fails; standalone the leg passes 263 / 263 and, with the suite's inputs built, its arm is caught (2 / 2). The other 65 arms, the processor-copy ones among them, are caught.

Live `dev` moved to `fa6c094b` (PR #875, #873: `scripts/act_ci.py` and `docs/testing/CI_WORKFLOWS.md` only) after these gates; no file is in common with this branch. The candidate merge and its validation are the manager's.

The PR body, HANDOFF and receipts are with the manager.
