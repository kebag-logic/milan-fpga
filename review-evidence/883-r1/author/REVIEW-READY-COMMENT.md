[A768] REVIEW READY
Commit: `e18c822536ebeaf1cb0f42abea74513501aa26c7` (branch `883-adopt-processor-801ef228`, from dev `46c971fa`; live dev `fa6c094b` merges cleanly, no file in common; nothing pushed)

Changed, after the ruling (issuecomment-6805166676, option (b)), three new commits and no rewrite:
- `8edfae99`: `gptp-processor` back to `1616fc8f`, dev's pin. FPGA-gPTP PR #103 rides with the next adoption; the parent ratchet is not raised.
- `f746d659`: the gPTP pin-derived records at `1616fc8f`, through their generators. Every gPTP-only page and the time-sync diagram are byte-identical to dev's. `ooc.sh --record-rom-digests` leaves the ledger unchanged; it keeps the `a64be73d` gptp row, equal to `1616fc8f`'s, since the generator keeps other pins' rows by design.
- `e18c8225`: the changelog, pin page, area budget, finding 234 and the three records' notes state the adoption as the processor's alone.
- Earlier commits unchanged: the processor gitlink `044cb25f` -> `801ef228` (PRs #218, #219), crflic `[MRPAPP]` and `[MVRPLA]`, notify `[AIDX]`, their campaign arms, the #851 control fix, #495 row 6758088112, and the seventeenth resource record.

Validation at this head, on clean clones; workflow jobs on the pull_request merge commit `9a803dbe` (live dev and this head):
- docs.yml, all five jobs: 64 steps rc 0, 33 not run with a reason, 0 failing. `python3 scripts/check_py_idiom.py` rc 0: `long module: 10 <= 10`, `unannotated public function: 0 <= 0`, `undocumented public function: 0 <= 0`.
- rtl-fast `yosys-elaboration`, the one job outside docs.yml that reads a file changed after `f58347df` (the baseline JSON): 7 rc 0, 3 not run with a reason, `baseline PASS: 3 endpoints`.
- The gPTP consumer suites, each its own `make -C tb/verilator/<suite>`: capture_coherence, gptp_plane, gptp_shadow, gptp_tables, gptp_txts, milan_dp, milan_dp_gm_steps, milan_dp_mclk, milan_dp_render, pp_shadow, tsn_fuzz. 11 / 11 pass, 40,591 checks, 0 failures (`suite_tally.py`). milan_dp's 19 legs all pass: gptp and gptp-lat 212 / 212 each, crflic 458 / 458, notify 535 / 535. Every suite's count equals the `6c6706e5` sweep's.
- The pin and doc gates (`check_submodule_docs.py`, `check_gptp_docs.py --with-submodule`, `check_diagram_pngs.py`, `docs_inventory.py --check`, `pp_resource_gate.py check-baseline` and five more): 10 / 10 rc 0. `git diff --check 46c971fa HEAD` rc 0.
- Standing from the earlier pass, whose inputs the later commits leave unchanged:
  - the full sweep, 65 / 65 suites, 2,192,633 checks, 0 failures (`6c6706e5`);
  - every `run:` step of rtl-fast, rtl and elaborate rc 0 (`f58347df`);
  - `test_builder.py --require-rv32` rc 0;
  - the campaigns: crflic 16 / 16, gsi 19 / 19, unb 6 / 6.

  The two gPTP pins differ only in four `docs/` and `tb/` files. Every parent gate that reads those is a docs.yml step, and the suites that read the gPTP tree are the 11 above (from their builds' dependency files and logs).

Acceptance criteria:
1. The processor gitlink moves to `801ef228`, a fast-forward on the donor's `main`: met.
2. Parent changes, #495 rows and planted mutants: met.
3. #857, #858, #860 each graded at the AX7101 1x1 shape, failing at the old pins (7 and 4 failures): met.
4. Route: met. All three #818 directives pass the +0.030 ns floor at every corner. Best is ExtraPostPlacementOpt at +0.334 / +0.017 ns; against `46c971fa`, -73 LUT, +121 FF, +29 slices (1 free). The record, measured at `a89802c8` (gPTP `a64be73d`), holds at `1616fc8f`: an export there reads the same files and ROM images, and differs only inside the exporter's hierarchy comment.
5. The gates: met, re-run as the ruling scoped.

Open risks/questions:
- Two pre-existing faults need their own issues; the texts are in the handoff:
  - `dynmap-mutants`: on a fresh clone the listener leg's clean control runs without `milan_dp_render`'s generated inputs.
  - The resource gate's `inputs_sha256`: it hashes the exporter's `/* */` hierarchy comment, whose black-box order is not reproducible across runs.
- One slice of margin is left on the selected route.
