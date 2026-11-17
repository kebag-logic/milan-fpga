[A781] REVIEW READY
Commit: 8883d499 (lane 894b, PR #914; round 12, one commit on round 11's 05a7ea82, by [the ruling on round 11's STOP](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6938589932))

Changed:
- **The two escaped SRP plants (8883d499).** `asking-is-ready` and `readyfailed-ignored` still mutated the registrar walk's expression (`srp_mbx.c:861`), which no longer decides readiness on these records. Each now plants in the Listener's indication (`srp_mbx.c:185`), where #930 copies the declaration:
  - `asking-is-ready` counts Asking Failed as ready;
  - `readyfailed-ignored` drops Ready Failed.

  Each keeps its named test and its words. `sw/firmware/ctrl/test/srp_mutants.py` is the only file changed; no test, ledger or bound is weakened.
- **The twin and twin-plants failures** are the base's stale `split-talker-failed` row, recorded as owed to PR #935 by the ruling.

Validation (each on a fresh clone of 8883d499):
- **The retargeted plants:** both caught by name at one and two interfaces, and the clone is unchanged after.
- **The SRP campaign** (`rtl-fast.yml` `firmware-srp-mutants`): every step rc 0, 436 caught and 0 escaped. That includes the five Listener copy defects at 8x8/1if, the `four-way-f3b-*` plants and the lwSRP pin controls.
- **Verilator shards** 1, 3, 4, 6, 10 and 17 of 19, from clones whose tsn-c-stack origin is the one `.gitmodules` declares, with the pinned tools: 37 suites and 966,909 checks, 0 failed.
  - Shard 1's `tsn_fuzz` rewrites only the date line of two generated result pages in its clone, with the counts unchanged.
- **Quick checks:** 23 of 23 rc 0. They cover:
  - the shape table, the flip check (612 controls) and both points;
  - rows_tiers (1,033), the load gate (28 and `--check`), the record classes (14), the mixed-point probe;
  - the ledger's 15 mutants, docs_check and the idiom gates;
  - the comment scans over the PR's and each round's delta, and R844-1's audit (0 lines);
  - the diff checks.
- **Images:** all eight are byte-identical to the measured 46cf2a7d's, by ELF and loadable sha256; the 8x8/1if platform is 56.0 RAMB36.
- **Carried from round 11 at 05a7ea82** (round 12 changes only a defect table that the SRP campaign alone reads):
  - the firmware suites and `fw_coverage --check` (39 files; `srp_mbx.c` 746 of 746 lines);
  - the control and AECP campaigns, the boundary and simulation jobs and the docs jobs;
  - the lane gates but the twin's.

Acceptance criteria:
- **#930: met, as the ruling on round 10's STOP confirms.**
  - At 1x1/1if SRP's record is 250 us by the rule (stated 280, at most 280), and the last queued notice by every source is 136.65 ms (140).
  - At 8x8/1if the load at the pin is 0.735 (0.75).
  - Every row is within its bound at both points, `srp-talker-held` included. `service.aecp.last` is 62.04905 ms against its ruled 62.16.
- **The PR body closes #930.**

Open risks/questions:
- **`twin` and `twin-plants`** fail on the base's `split-talker-failed` row until PR #935 lands.
- **R4 by every source at 8x8/1if**, 21.39 ms against 20, stays owed to #872.
- **The timing floor** is #818's: +0.030 ns setup and 0 ns hold, on the best of the three directives. No route ran.
- **Reviews:** R843-3 (NEGATIVE) and R844-3 (POSITIVE) were at af2c4d7a, so a re-review of this head is owed.
