[A781] REVIEW READY
Commit: 98c0b62be911f5cff7a03ebfee7f837c23847d14 (lane 894b, PR #914, round 4: four commits on round 3's 716a8ae7)

Changed:
- R844-1-F1 (MAJOR), fixed in the tree. `tb/verilator/ctrl_service_budget/egress_ledger.py` (new, with `--selftest`) holds each of `backlog-owed`'s seven held-egress rows to section 13's ledger figure at 8x8/1if (#894's held-egress ruling, item (a)). These fail the leg:
  - a measured instance of a ledger row over its figure, by as little as one bus cycle (10 ns), whatever its name;
  - a row never released or answered;
  - a ledger row with no measured instance;
  - any instance not measured;
  - any other budget miss.

  The packet's acceptance gate (`gate_r4.py`, round 3's `gate_r3.py` and its criteria) delegates both decisions to it. Section 13's table now names both service rows in full and calls its column "Ledger, ms"; the self-test holds the grader's ledger to that table.
- R844-1-R1 and R843-1-R1 (residue), fixed. 55 added lines in 25 files now cite each ruling by issue, subject and item: #894's shape ruling, held-egress ruling, retry-cost ruling and map-keying ruling. Section 13 maps the names to their links. The commit changes no code:
  - every C/H/C++ token stream is identical;
  - every Python syntax tree is identical without its docstrings, apart from five printed check descriptions that only lose their ID.
- R843-1-S1 (suggestion), taken.
  - `aecp.h` refuses, in THE SHAPES' words, a unit that charges a refused attempt (`AECP_CHARGES_ATTEMPTS`) without the shape's table in force. `aecp.c` now includes `ctrl_loop.h` first, then states it.
  - `test_aecp.cpp` asserts `MBX_N_IF == AECP_TEST_INTERFACES`. `aecp_arms.core_arm` gives a two-interface arm with no mailbox group its own interfaces' contract.
  - Two AECP campaign build rows are added.
- The fourth commit holds `egress_ledger.py`'s self-test helpers to the Python idiom gate. The full pass's first lane-gate run, at 3bb204c8, found three findings in the new file, which a working-tree run had missed while the file was untracked. That pass was stopped and ran in full again at 98c0b62b.

Validation (clean clones; receipts and their index in the round 4 packet):
- The ledger: `egress_ledger.py --selftest` PASS: 30 controls, in process and as a process, and 8 of 8 mutants caught, each by its own control. Among them is the earlier rule, a row waived by its name whatever its size.
- The acceptance gate's controls (`gate_controls.py` against `gate_r4.py`), each its own process: 20 of 20 hold.
  - The unchanged ledger exits 0, and so does section 13's measurement.
  - For each of the seven rows, one bus cycle over its figure exits 1 naming it, and so does 36.76 ms over, for example "- the ledger: backlog.owed.if0 (backlog-owed): 63.24001 ms, over its ledger figure 63.24 ms by 0.00001 ms: a larger miss".
  - R844-1's larger-egress input exits 1, and so does its unmeasured input.
  - The log-alone form passes the published figures and fails a row printed 1 us over its figure.
- The regrade of every round 3 8x8/1if leg with the fixed gate (arm A's four parts, `answering-every-port`, `aecp-largest-notice`; 112 groups): PASS.
  - Their group grades were not kept after round 3, so the gate and the tracked grader read the legs' published logs, whose `BUDGET` lines name every instance over its budget.
  - The seven rows, at most 63.0835 / 63.3055 / 63.5265 / 63.7475 / 63.9695 / 62.0255 / 61.6805 ms, are all under their ledger figures. There are 0 refusals and no other miss, and every leg ended rc 0.
- Comments: the scan of `7398ec0a..98c0b62b` prints 0 lines (issue-comment IDs, numbered rounds, phases, review labels), and R844-1's `source_comment_audit.py` prints 0 lines.
- Item 3's controls:
  - both new campaign rows are refused in the `#error`'s words: "THE SHAPES: a unit that charges a refused attempt (AECP_ATTEMPT_US) has no shape's table (ctrl_loop.h) in force";
  - a planted two-interface core arm at the tracked contract is refused in the assertion's words: "THE SHAPES: the host arm's mailbox contract (MBX_N_IF) is not at its interfaces (AECP_TEST_INTERFACES)";
  - the core arm passes 83 of 83 at one interface, and 83 of 83 at two on its own contract;
  - EIGHT_ONE passes 4 of 4, and the debug arm at two interfaces 1 of 1;
  - `counters-f5` passes at 1x1 and 8x8.
- Images: all 8 (the size fixture and the platform at 1x1/1if, 1x1/2if, 8x8/1if, 8x8/2if) are byte-identical to `716a8ae7`'s, by the sha256 of each ELF and of its loadable bytes. That holds after the rewording, after item 3, and at the head on a clean clone. The `716a8ae7` base was rebuilt this round and reproduces round 3's receipt.
  - So the sweep and the 8x8/1if measurement carry by that identity. Of the changed files, the sweep's firmware build reads only `ctrl_loop.h`, whose tokens are unchanged.
- The full pass at the head, each part on its own clean clone of 98c0b62b:
  - every `run:` step of every rtl-fast, rtl, elaborate and docs job: 139 run at rc 0, 226 not run with a reason in not_run.json, 0 bad. In the first run, `elaborate-gates-1`'s LiteX simulation `test_soc_timing_cuts` hit its 900 s wall clock under host load (exit 92, "result UNKNOWN, not a failure"); the job ran again on a fresh clone and passed.
  - the firmware jobs, every step rc 0: the campaigns caught 716, 277 (the two new rows among them) and 345 plants, 0 escaped; the boundary PASS; `aecp_wire.py --every` exit 0; the 8x8/1if mailbox arm ok;
  - the lane gates: 59, 55 at 0 and the four that exit 1 by design (`rows_tiers --terms`, the default `flip --check`, `--point 1x1/1if --design as-built`, `--point 8x8/2if`). They include the harness self-test (879 checks, 259 mutants caught, 0 failures), the ledger's self-test, both comment scans (0 lines), `docs_check`, `check_em_dash`, the Python and C++ idiom gates, and 16 `git diff --check` bases (7398ec0a and 716a8ae7 among them). The load is 0.711 of 0.75 at 8x8/1if, and 0.513 and 0.509 at 1x1/1if. Every clone was clean after its part.
- `docs_inventory --check`: not present at this head or its base (`894-tiers` 9606b3a9, `dev-soft-core` cec88385). It arrives with the sync to dev; recorded in not_run.json.

Acceptance criteria:
- Round 4's four items are met. Item 1: the gate fails any measured row over its ledger figure, with controls, and the regrade passes. Item 2: 0 lines, and images unchanged. Item 3: both checks, each with a control in its words. Item 4: the gates.
- No bound, rule or ceiling as they stand at 8a3791e4 moved. THE PACE, the 1x1/1if slice, tsn-c-stack, lwSRP and every donor are untouched.
- `rows_grade.py` changed only in its shape-keying docstring.
- No STOP condition: no regrade fails, and no image changed.

Open risks/questions:
- `894-tiers` at 9606b3a9 (#902, round 12) is not merged, by instruction. The sync after #902 merges needs a fresh byte-identity base, an 8x8/1if measurement graded with `egress_ledger.py`, and a full pass.
- The guard covers the unit that says it charges (`aecp.c`). C cannot test a name at a later use, so a future unit that uses `AECP_ATTEMPT_US` without saying so still gets the compiler's undeclared-name error.
- Unchanged from round 3, for new Issues or decisions:
  - `Mailbox.ARoundFillsWhatItsPassHasLeft` fails at 8x8/1if (since at least 7398ec0a);
  - 1x1/1if's SRP record, 26,086 cycles against 250 us;
  - the rows by every source, reported and owed to #872.
