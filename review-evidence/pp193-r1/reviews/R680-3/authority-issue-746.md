https://github.com/kebag-logic/milan-fpga/issues/746

**Future cleanup. Not scheduled; do not start until it is picked from the backlog.**

**Rule** (owner, 2026-10-15): source comments describe what the code does and why, with the issue and requirement it serves. They never carry workflow history:
- bench lane labels ("bench lane B17", "B17's 10 binds");
- lane names ("lane F-INT");
- review rounds or reviewer IDs;
- issue-comment IDs.

That history lives in `docs/findings/`, in the design pages' evidence links and in the PRs. Issue numbers (`#645`) and requirement IDs stay, because they are the traceability.

**Known instances** at `dev` `9ef71772`, found by a scan of `hdl tb sw scripts syn configs` outside Markdown:
- `hdl/milan/milan_datapath.sv:6616-6625`, the `settle_bind_*` block: "#645, bench lane B17: …", "once in each of B17's 10 binds".
- `tb/verilator/follow_ring/`:
  - `sim_main.cpp:54`, `:148`, `:238`;
  - `Makefile:16`, `:110`;
  - `mutants.py:53`;
  - `sweep.py:21`.
  The per-cycle parameters may still name their data source (#741's measured packet), but not as a lane label.
- `sw/firmware/ctrl/test/test_acmp_mbx.cpp:670`: "(lane F-INT; #665 comment 6088423771)".
- Re-scan before starting. Identifiers such as `B10` to `B13` in the ACMP firmware tests are behaviour IDs, not bench lanes, and stay.

**Done when:**
1. Every instance is rewritten to state behaviour and reason, citing the issue or design section. There is no behaviour change and no changed check.
2. A hygiene check refuses a new workflow label in a source comment, with a planted case and its escape when the check is removed, so the rule holds by construction.
3. `docs/findings/`, the design pages' evidence sections and `docs/testing/TESTING.md` keep their records unchanged.
4. Gates:
   - `lint_rtl.py --check`, `xvlog_gate.py --check`, `syn/yosys/run.sh`;
   - `follow_ring`'s default legs, `make mutants` and `make sweep-bind`;
   - the firmware unit tests and their mutation campaigns.
   - The mutants patch source text, so a comment-only edit is re-proven, not assumed neutral.

Relates to #645.

