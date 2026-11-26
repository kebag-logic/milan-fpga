# Review ready: #1008 round 4, lane `1008-ci-30min` at `5b5b076514` (not pushed)

Base: dev-soft-core `c34e7d8b06`. The PR body is `PR-BODY.md` ("Relates to #1008"). Receipts are under
`receipts/` (see `receipts/INDEX.md`).

## What to review

1. **`sw/firmware/ctrl/test/test_ctrl_firmware.py` and `test_ctrl_firmware_shards.py`.**
   - `--campaign-shard` for phases 1-3.
   - The SRP slicing of its three tables.
   - `campaign_cases`: the real-driver proof each leg runs, with its planted dropped and duplicated legs and its
     six refusals.
2. **`sw/mailbox/census_legs.py`, and `census_selftest.jobs_for`.**
   - `jobs_for` is factored out of `selftest()` with the same order.
   - The receipt schema and the judge's refusals.
3. **`scripts/ci_fast_legs.py`, and in `scripts/ci_gate_workflows.py`:**
   - `FAST_TOOL_SHARED`, so the census legs restore `yosys-tool`'s tree and a recipe that differs is refused;
   - `DOCS_WORKERS`.
4. **`scripts/ci_events.py`:** `check_fast_legs`, run on the generated `rtl-fast.yml`, and `_fast_leg_arms`, run by
   `_selftest_fast_legs` against that generated graph.
5. **`scripts/ci_fast_tool_selftest.py` and `ci_gate_workflows_selftest.py`.**
   - The shared restore is held as exactly as `yosys-elaboration`'s.
   - The census budget owner is now the legs job.
6. **`scripts/suite_shards.py`:** `gptp_shadow` set to 517.
7. **`docs/testing/CI_WORKFLOWS.md`:** the #1008 paragraph, the census paragraph, and the projection tables.

## Evidence

- **Gates:** `receipts/gates/summary`, every gate in a clean clone at the head.
- **Verdict identity** against serial hosted run 45657606423, whose inputs equal the base's:
  - `identity/control.txt`: 844/844;
  - `identity/aecp.txt`: 398/398;
  - `identity/srp.txt`: 662/662, with the pin controls in each leg;
  - `identity/census.txt`: 22 check lines and 222 self-test lines.
- **Planted failures:**
  - `identity/census-plants.txt`: 7 of 7 refused on the real receipts;
  - the required-context shell, in `ci_fast_legs_selftest` (gates log);
  - 22 contract arms, in `ci_events_selftest` (gates log).
- **Projection:** `identity/projection.txt`. Every divided job's slowest leg is at most 1027 s hosted.
- **Profiles:** `profile4/`.
- **Runner-minutes:** `tools/minutes.py`. rtl-fast goes from 263.9 to about 269.2, docs from 91.2 to about 94.5.

## Known gaps

- **Not shown here:**
  - any hosted run of the head (not pushed);
  - an act replay;
  - local runs of `firmware-unit`'s legs.
- **Still over the budget:** the Verilator and Yosys cache-miss jobs, the elaborate builder's single gate, and
  rtl-full's Yosys shard 0. See `HANDOFF.md`, "Open".
