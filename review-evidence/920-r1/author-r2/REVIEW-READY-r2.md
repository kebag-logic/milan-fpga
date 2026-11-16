[A786] REVIEW READY
Commit: `bd252db1` (branch `920-save-burst`): round 1's `54280c94`, one `--no-ff` merge of `dev-soft-core` `70f4056f` (`d66b4045`, both sides kept), and one docs commit restating the figures as measured on that merge.

**Changed**
- **The cause, proved at the base before any fix.** The AECP owner's pending marks covered 256 ids. Layout 3 puts the names at id 222 and up, so every name from ordinal 34 on never reached the store: at 1x1/1if, the five names the rehearsal lost.
- **`945a1217`:** the pending bits cover layout 3's id space, with a count of the bits set and a static assert.
- **`c1a24c18`:** the ruling's three mechanisms, and nothing else.
  - A change marked during a running capture joins it.
  - The next save starts at the first idle step after the save in flight.
  - A step a pass in passes that took no input, with the step's time left.
- **Tests:**
  - `Nvm.EveryAcknowledgedNameSurvivesTheRealStorePowerCycle`, with AECP mutants;
  - the store's `capture_joins` and `busy_steps` cases, with their mutants;
  - the budget harness's `save-burst` and `save-flight` groups, their grader self-test, and three planted save controls, each caught by name.
- **The merge:** `aecp_nvm.h` keeps this branch's pending-bit words with #901's name runs. The ledger keeps #895's 60.5 for the platform's 8x8/2if image, with #920's 296 B within it. `ctrl_plat` is measured on the merge.

**Validation**
- **CPU budget harness, every group, re-measured on the merge.** The two save groups run first, then the rest in parts, with one `--regrade` a point.
  - 1x1/1if (98 groups): exit 0, 0 refusals, 0 of 132,926 passes over the share, no stated-cost line.
  - 8x8/1if (97 groups): 0 refusals, 0 of 231,039 passes over the share. It exits 1 on stated-cost lines alone, #914's per-shape statements as ruled: the polls base, the most 25,015 cycles against 22,500; an ACMP item, 7,277 against 5,500; a declined offer, 2,338 against 2,000.
  - At both points every row the CPU decides is within its bound. The only misses are the seven held-egress rows behind the 60 ms egress hold, as at the base.
- **The target, at both shapes under the held load:**

  | | 1x1/1if | 8x8/1if |
  |---|---|---|
  | `save-burst`, the latest name durable after its response | 1,107.8 ms | 1,370.3 ms |
  | `save-burst`, saves and the cut | 1 save, every name at the cut | 6 saves, every name at the cut |
  | `save-flight`, durable after its response | 165.0 ms | 663.1 ms |
  | `save-flight`, steps to the next save's erase | 19 (want 19) | 59 (want 59) |
  | `save-starved` and `save-second` against their worst cases | 4,049.1 of 4,070; 6,030.3 of 6,070 ms | 12,448.1 of 12,470; 22,829.6 of 22,870 ms |

- **Self-tests:** the harness's has 0 failures, all 251 mutants caught. The store suite passes 546 tests at 5 shapes and catches all 152 planted defects.
- **rtl-fast firmware jobs** (`d66b4045`): 0 failed steps in each; `verify_wf` reports 0 bad. They cover firmware-unit (with `fw_coverage --check`), the AECP, control and SRP mutant campaigns, verilator and boundary.
- **elaborate** (`d66b4045`) and **docs** (`bd252db1`): 0 failed steps.
- **Load gate:** 1x1/1if at 0.517 of 0.70. The memory ledger, the Python idiom gate and the docs checks pass.
- **ROM:** every image is #901's plus 296 to 304 B, within every entry.
- **Suite sweep at `bd252db1`, four shards:** 65 of 65 suites passed, 0 failed, 0 timed out; 2,713,040 checks, 0 in-suite failures.
- **Round 1's sweep at `54280c94`:** the four suites it could not judge pass alone (`gptp_shadow`, `media_phase`, `milan_dp` and `reboot_ctrl`, rc 0 each).

**Acceptance criteria:** met. Every acknowledged change is durable within 5 s of its response at 1x1/1if and 8x8/1if, under the held load, a burst of every name and a change marked during a save in flight included. Only the ruling's mechanisms are used, with the cause proved first.

**Open risks/questions**
- **The 8x8/1if routes miss at the base, owed to #927.** Per the ruling no route was re-run, and the merge has no gateware change. The figures:
  - the recipe's directive: WNS +0.011, WHS +0.034;
  - ExtraTimingOpt: WNS +0.171, WHS +0.014;
  - AltSpreadLogic_high: WNS +0.215, WHS +0.014.
- **8x8/1if's stated costs** are #914's per-shape statements.
- **The sync onto #919** waits for #919's REVIEW READY.
