[A863] REVIEW READY
Commit: 47f2a3d7ffdf7ef701c69267a91ac92892a1c99e
Branch: `arty-4x4-1127`, PR #1026, base `dev-soft-core`, stacked on #1004 (carries #1004 round 11 `c0b625d1792e61b8e99944daea65b842e6b9dcde`; merges after it). Closes #1027.
Previous reviewed head: `12ab4b189f54439cd126f677b906a19835d7f32a` (R967-1 NEGATIVE, R968-1 NEGATIVE).

Changed since `12ab4b189` (7 commits, no firmware, HDL, LiteX, mailbox or existing-configuration file):
- `f7c1b674e` #1027 named as this point's task contract:
  - the config header, `run.py`, `arty_grade.py`, `poll_grade.py`, `shape_costs.py`, the builder suite comment and the builder and build pages;
  - section 15, renamed "Arty split points" with its links, gains the 4x4's decisions, its stated costs, the two qualifying rows and the tie-break.
- `988b13a8d` `egress_mii.py`:
  - per-point stream-load controls at `arty-1x1` and `arty-4x4`, and four CRF plants;
  - `--packet`/`--structural --point`, and a log of another point's queue refused;
  - FR_NFR 3.4.1's structural and queued figures stated per point (4x4: 431.12 us, 2.42 ms, 2.71 ms, 35 records).
- `8c5047efa` `record_classes.py`: Arty checks at both points (the 4x4 at 100 MHz, an 80 MHz leg refused, its configuration named to its point, its own ACMP record cost read at (1,5,5)); `selftest_share.py` pins each Arty clock to `arty_grade.CLOCKS`.
- `8bca16462` `egress_ledger.py`: the planted cycle held to each point's configured `sys_clk_hz`, two mutants; the comment-ID residue removed.
- `5ed652182`, `47f2a3d7f` `egress_fixed.py`: runs under `-I`, refuses a malformed `SYS_HZ` with its usage (exit 2), and gains `--selftest` (stub simulator, 3 mutants).
- `8018399b2` harness README: the controls, the CRF frame in the queue bullet, the ledger and fixed-path bullets.

Findings, each with its required outcome:

| Finding | Outcome | Evidence |
|---|---|---|
| R967 F1 / R968 F4: no public task contract or decision record | #1027 carries scope, acceptance and decisions 1 to 5. The tree and PR body cite it (`Closes #1027`), and #878 stays the 1x1's. | `SPLIT_CONTROL_MEMORY.md` section 15 "Arty split 4x4/1if"; PR-BODY.md "Decisions it rests on" |
| R967 F2 / R968 F1: the CRF frame in the stream load has no control | `[arty-4x4] arty-4x4: the stream load is its talkers' frames and its CRF output's, (90, 90, 90, 90, 46)` and `... every frame of the stream load is on the wire in its interval` fail under `return aaf`, `CRF_AVTPDU = 0` and `crf = ()`, each planted in the tree. | `receipts/gates5/mutants/mutants.json`, `egress-mii-selftest.log` (35 of 35) |
| R967 F2: `--packet`/`--structural` grade at the 1x1 | Both take `--point`, arty-1x1 unless given. A log of the other point's queue is refused, named by the control `a log of arty-1x1's queue is refused`. | `egress-mii-structural-4x4.log`; the census-4 extract regrade |
| R968 F2: the record-class gate's arty-4x4 branches have no control | M8 is caught by `endstation_arty_split_4x4 is named to arty-4x4`. M9 is caught by `endstation_arty_split_4x4: its shape (1, 5, 5) reads arty-4x4's ACMP record cost, 210 us`. M10 is caught by `arty-4x4 record classes accept their complete 100 MHz fixture`. | `mutants.json`; `record-classes-selftest.log` (26 Arty checks) |
| R968 F3: the `egress_fixed.py` usage line does not run; SYS_HZ untested | `python3 -I tb/verilator/ctrl_service_budget/egress_fixed.py DIR 100000000` exits 0 reporting 300.0 ns. Without SYS_HZ it gives PASS, 312.5 ns against the stated 320. `--selftest` holds the arguments, the period passed to the build and the report's verdict. | `egress-fixed-100.log`, `egress-fixed-80.log`, `egress-fixed-selftest.log` |
| R967 F3 / R968 F5: compressed receipts unpublished | All 123 compressed receipts of rounds 1, 3 and 4, and the one tar archive's members, are shipped as extracted text under `receipts/earlier/`. INDEX.md maps each to its `.gz` sha256. The census-4 extract regrades 446.76 / 527.04 us, all 159 per-case grades identical to the full logs', and the ledger's 1655 instances. | `receipts/INDEX.md`, `receipts/census4-extract/`, `checks/g-full.txt` = `checks/g-ext.txt` |
| R967 R1 / R968 R1: comment ID | Removed. | `egress_ledger.py:102-103` |
| R967 R2 / R968 R2: one-clock comments and the check label | Reworded as required. | `shape_costs.py:57-58`, `record_classes.py:100`, `selftest_share.py:170`, `test_builder.py:23900` |
| R967 R3: unqualified Arty clock statements | Qualified to the 1x1. | `ENDSTATION_BUILDER.md:25,28`, `BUILDING.md:361` |
| R967 R4 / R968 R3: 300 ns versus 320 ns in the egress sentence | "the stated 320 ns fixed path (300.0 ns measured at 100 MHz)". | PR-BODY.md |
| R968 R4: the README queue bullet | The CRF output's 46-byte frame is added. | harness README |
| R967 S1, S2, S4 / R968 S1, S2 | Done: the clock mutants are caught, SYS_HZ is validated, the clocks are pinned to `arty_grade`, and section 15 is renamed. | as above |
| R967 S3 | Done: the stated-cost table, the two qualifying rows and the tie-break. | section 15 |
| R967 S5 (#1022's body), R968 S3 (README link to a published qualification) | Not done; both need a public record this lane does not post. | none |

Validation at `47f2a3d7` (`receipts/gates5/`):
- `egress_mii.py --selftest` 35 of 35, and `--structural` at both points;
- `egress_fixed.py --selftest` 3 mutants, plus its usage line run at 100 MHz (300.0 ns) and at the default (312.5 ns, PASS);
- `record_classes.py --selftest` 26 of 26 planted controls and 26 Arty checks;
- `egress_ledger.py --selftest` 26 mutants;
- `arty_grade.py` at both points and `--selftest`;
- `rows_tiers`, `load_grade`, `shape_costs` and `kept_grade` self-tests;
- the census-4 extract regrades (egress row, ledger);
- 8 of 8 named mutants, and the restored tree clean;
- the service self-test, 323 of 323 mutants caught;
- the docs workflow's 96 runner-free commands. 92 pass on system Python. The four needing the pinned Markdown renderer (`gen_toc` x3, `check_em_dash --base aa30d77f`) pass in its venv: 0 em-dash findings over 2821 added lines. `git diff --check` is clean;
- the builder suite, ALL GATES PASS EXCEPT 1 NOT RUN (gate 11);
- the 4x4 split boot, 0 findings, and native controls 6 of 6. Identity at this head: the 66 builder outputs and the three existing product ELFs are byte-identical to `aa53840d9`, and the 4x4 ELF is the routed `1b8066e4cd65f446366f6f2574a8e6b099310f7d34f6d8923d861f20a887b09c`. The firmware shards, the 1x1 boot, the region self-test, `test_ctrl_memory`, the host arms and the coverage ratchet last ran at `12ab4b189`. Since then no file any of them reads has changed, except the 4x4 configuration's header comment, and the images and the generated include are byte-identical through it.

Acceptance (#1027):
- Route at the floor, every corner, best of three directives: met (ExtraPostPlacementOpt +0.049 / +0.012 ns).
- Rule's row from the link-rate census within every owner bound: met (load 0.4689, ACMP 28.52, txL 48.72, last 117.68 ms, SHARE 1.733 ms).
- 100 Mb/s egress within 1000 us with the CRF output in the load: met, 527.04 us, load (90, 90, 90, 90, 46).
- Every gate passes, or states why NOT RUN: met; gate 11 NOT RUN (its v1-era oracle report is not on disk and not reproducible from the tree).
- 1x1 and AX7101 images byte-identical: met.
- FR_NFR and SPLIT_CONTROL_MEMORY state the point: met.
- Every change has a self-checking control with a planted defect: met (`mutants.json`, 8 of 8 named mutants caught; the self-tests' own plants).
- Bench session with 4+4 streams and CRF, and the latency pair at 100 MHz: NOT MET, owed to the bench (no bench this round).

Open risks/questions:
- Thin margins, as measured: txL 0.28 ms, THE SHARE 0.267 ms, setup 0.019 ns over the floor on the one closing directive, hold +0.012 ns.
- The published receipts are the extracted contents of the `.gz` files, not their bytes; INDEX.md records the `.gz` sha256 beside each content's.
- The census traces themselves (0.4 to 0.5 GB per census) stay local. The census-4 extract carries every line the egress and ledger grades read.
