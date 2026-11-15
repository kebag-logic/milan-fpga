[A761c] REVIEW READY
Commit: `d3566d44` (branch `665-s11-aecp-reboot`; 16 commits on round 4's accepted `049f0e4d`, the first the merge of #902's review head `41ca9f87`; not pushed, the manager pushes)

Round 5 is the maintainer's ruling #665 issuecomment-6894152131, item 1: #881 joins the flip train (#902, #901, #898, #881, #914). No STOP condition holds.

Changed:
- **The merge (`6cfdf650`)** keeps both sides:
  - #902's owed-notice queue, pace stamp, record classes and tiers;
  - the REBOOT's answer, gate and reset port.
- **Semantic conflicts fixed:**
  - The REBOOT port's CSR bank moved to `n_locs - 4`, below #902's record mover's. The split SoC's `csr.csv` against `41ca9f87`'s adds only `ctrl_reboot`.
  - THE RETRY's round, which came in from `dev-soft-core`, now starts nothing after a REBOOT's SUCCESS (`b4b0c3eb`; core check, defect `reboot-retries-after-its-success`).
  - B15, B17, B18 and B23 are adapted to THE STEP and to the driver's cached ring tail (`7072343a`, `88b0fcd1`).
  - The REBOOT simulation's flash journal is now the map's KLJ3 span (`a3e45e68`). Its early-reset plant fires before AECP's handler, since a plain response is now committed in the record's own turn (`20e08ceb`, `cb0fc679`).
  - #902's `owed-round-beside-the-queue` anchor now carries the REBOOT's `round_waits` term (`d3566d44`).
- **REBOOT's record (`b01968a4`)** is measured in the answering-ports arm's `aecp-reboot` group; that arm's patch list gives the fixture a reset port. `record_classes.py` holds every REBOOT record as ordinary, and refuses a pass without an accepted and a refused one (14 of 14 controls).
  - At 1x1/1if: SUCCESS 125 us, the refusals 100 to 115, of the ordinary 240.
  - At 8x8/2if, reported: 95 to 115 of 265.
- **The survey** of every stated table over every 1x1/1if leg (arm A whole, the answering-every-port arm, the answering-ports arm) found four costs over by the rule. All are restated (`7653571f`):
  - `record.srp` 285, with `CTRL_LOOP_SRP_UNIT_US`, which `load_grade.py --check` holds to it. This is this lane's one `ctrl/loop/` change, by #894's derivation ruling.
  - `record.aecp` 240.
  - `events_none` 40.
  - the paced class 305.
  - The cause is the hot-code move: `aecp_retry_aged` -28 B, fourth in the hot order.
- **The bound rule** then gives `AECP_QUEUED_MS` 135 ms, its row 134.74. The notice windows run to it (`935dacf2`).
- **Every one-interface leg ran again** on the rebuilt image. Only #894's class lines are over, and `record_classes.py` gives RESULT PASS over every leg.
- **The rows at 1x1/1if** all hold, flip check PASS. Tightest: txL 48.75 of 49, the last queued notice 134.74 of 135, ACMP 29.22 of 30.
  - The load is 0.520.
  - The slice rule still chooses the built 950 us; the pace rule 8 ms.
- **ROM, reported:** the platform's 8x8/2if image plans 60.5 RAMB36, past its 60.0 entry. The entry is raised as S14 debt (`24e63089`, owner 2026-11-15). Every other image is within its entry.
- **Documents (`7b452a5f`, `41dcdd8f`, `57daf4ff`):** REBOOT_RESET section 8, SPLIT_CONTROL_MEMORY sections 3, 5 and 13, FR_NFR 3.4.1, the AECP, harness and REBOOT simulation READMEs.

Validation, each on its own clean clone, at the head named:
- **The sweep:** four shards on picked ranges at `57daf4ff`. 65 of 65 suites, 2,713,040 checks, 0 in-suite failures, 0 timed out. The cancellation preflight passes on each shard.
- **Every `run:` step of rtl-fast, rtl and elaborate:** 88 ran rc 0, 167 not run with a reason, 0 bad. The builder-running jobs ran at `20e08ceb`, and the AECP campaign at `d3566d44`.
- **The campaigns:**
  - control 738 of 738;
  - SRP PASS;
  - AECP 314 of 314 at `d3566d44`. At `57daf4ff` it refused the moved anchor, now fixed, and all 314 anchors have one site.
  - firmware-unit: suites PASS, `fw_coverage.py --check` PASS.
- **`docs.yml`** at `cb0fc679`: 64 steps rc 0, 31 not run with a reason, 0 bad.
- **The model and statement gates** at `cb0fc679`: rc 0, but for the four that exit 1 by design, as at #902.
  - `rows_tiers` 1,033 of 1,033; flip 585 of 585; load 26 of 26.
  - `plat_ledger` PASS; `test_ctrl_memory` PASS; `ctrl_hot` in order.
- **Whitespace** against three bases, the idiom gates and `docs_check` at `d3566d44`: rc 0.
- **Self-tests at `57daf4ff`:** the harness 246 of 246 mutants; the hooks 28 of 28 and 96 of 96; behave 511 scenarios; the split boot simulations PASS.
- **At `20e08ceb`:** the REBOOT simulation PASS, 12 of 12 plants and controls on their own words; the builder all pass but its two usual arms not run (gate 1b passes alone under make 4.4.1); the saved-state campaign 144 of 144.
- **Carries:** after `57daf4ff` only the REBOOT simulation's plant and README, their comments and one AECP mutant row changed, and each gate that runs one of those ran again after it. Arm A's 96 group scripts are byte-identical at `d3566d44`.

Acceptance criteria: items 2 to 5 met. Item 1 is met for six of the eight items and the binding, as before, so the PR still says Relates to #871.

Open risks/questions:
- The 1x1/1if margins are small (0.25, 0.26, 0.78 ms). The #898 sync moves the hot code again, so the survey reruns there.
- The packet is `665s11-a761c/round5/` (PR body, HANDOFF-r5, receipts, scripts, INDEX).
