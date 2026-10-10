[A576] REVIEW READY

Commit: `e0ee38f9d94bba29289f24f8f80a8d9645643c11` (parent, branch `621-ascapable-phc-step`)
Donor: `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9` (gptp-processor, branch `621-ascapable-phc-step`; publish it before the parent)
Both are local and unpushed. No PR is open.

Changed:
- `a99dbccf`, `72848a76`: the gPTP phase-step correction (donor) and its parent tests and docs, unchanged since the earlier rounds.
- `034e2e30`: `tb/verilator/nvm_capture_cpu/run.py` applies the 24.5 ms bound only to production arms (round 1b ruling).
- `e0ee38f9`: `tb/verilator/nvm_capture_cpu/measurements.json`, recorded from this head's campaign under [ruling 6089776382](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6089776382). 56 fields change in place.

Ruling 6089776382:
1. **Lane invariant: met.** Candidate `034e2e30` + donor `7dda9c3b` against base `5603c353` + donor `5dce647a`, same recipe on Verilator 5.052.
   All nine capture logs are byte-identical: six arms plus skip-copy, no-traffic and byte-only.
   The base byte-only control exits 1 because its unfixed grader (`run.py:79` at the base) applies the production bound to it. Its log matches.
2. **Refresh: met.** `e0ee38f9` records the candidate values as measured, through the round 1e composer.
   Recorded: verdict fields, `requests`, and provenance (5.052, tree of `034e2e30`, `processor_pins`, `gptp_ucode_sha256`).
   `python3 scripts/check_nvm_capture.py` exits 0, and its four `--mutation` controls each exit 1.
3. **Bounds: met.** Every production capture is at most 13.86318 ms, within the 24.5 ms bound.
   Byte-only is 1.834x the matching maximum, against a 1.5x minimum. Every margin to the 49 ms floor is at least 3.5345.
4. **Record: met.** HANDOFF.md lists all 56 changed fields with their receipt lines.
   - The 14 verdict values and 24 `requests` values come from dev's capture-SoC RTL drift, `a2f17342` to `5603c353`.
   - The provenance fields come from this lane (`run.py` hash, gPTP ROM and pin), from dev (protocol pin; `6178aa1bd` 8x8 config hash), or from this remeasurement.
   - The old receipt was already stale at the base.
5. Neither STOP condition occurred.

Validation at `e0ee38f9` (exit status in brackets):
- `scripts/run_all_suites.sh "$RESULTS/suites"` [0]: 61 of 61 suites, 2,186,819 checks, 0 failures.
  A first attempt stopped in its preflight cancellation self-test under host load average 30, before any suite ran. The unchanged rerun passed.
- `syn/yosys/run.sh --results "$RESULTS/yosys"` [0]: 58 of 58 tops.
- Static gates [0 each]: `python3 scripts/lint_rtl.py --check` (90 of 90 in the ratchet), `docs_check.py`, `check_cpp_idiom.py`, `check_py_idiom.py`, `check_doc_style.py`, `check_gptp_docs.py --with-submodule`, `check_diagram_pngs.py`, `gen_toc.py --check`, `check_em_dash.py --base 5603c353`, `git diff --check 5603c353 HEAD`.
- Vendor stages, each Vivado run under the exclusive lock:
  - `python3 scripts/xvlog_gate.py --check` [0]: 0 findings.
  - Shipping 1x1 route with the default, AltSpreadLogic_high and ExtraTimingOpt placement directives [0 each]: fully routed with 0 routing errors.
    WNS is +0.299, +0.100 and +0.201 ns; all constraints are met.
  - 8x8 RTL elaboration, standalone 1x1 synthesis and standalone 8x8 synthesis [0 each].
  - `python3 syn/ooc/pp_resource_gate.py check` for `route-1x1`, `ooc-1x1` and `ooc-8x8` [0 each]: zero delta against the baseline.
    `check-baseline` [0].
- The sweep re-ran the lane's own tests at `e0ee38f9`. `gptp_plane` ran `phc_step`: 49 checks, 0 failures, and its campaign passed 4 of 4, with all three planted microcode defects rejected.
  `milan_dp` ran `gmstep`: 190 checks, 0 failures.
  The 20-control `gmstep-mutants` target, the 197 physical-clock checks and the 143 extended checks ran at `72848a76`; only `run.py` and `measurements.json` changed since.

Acceptance criteria: the simulation items are met (HANDOFF.md coverage table). The physical five-step repeat is the later lane and closes #621.

Open risks/questions:
- `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1619` to `:1628`, `:1641` to `:1643`, `:1660` to `:1661` and `:1808` to `:1811` still quote the old receipt (`a2f17342`, 13.86484 ms, 3.5341x).
  The ruling did not extend this lane to that page, and no gate reads it. It needs a follow-up.
- `scripts/check_nvm_capture.py` does not hash capture-SoC RTL, configuration or pins, which is how the old receipt stayed green while stale (#495 checklist).
- Operational note: service memory exceeded the 9 GB guideline once, during the 1x1 integrated synthesis.
  The cgroup peak was 10.03 GiB, under the 12 GiB cap; the remaining stages stayed at or below 7.27 GiB.

HANDOFF.md and PR-BODY.md in the lane's output directory hold the field table, the invariant table, the planted-defect checks and every gate log's size and SHA-256.
