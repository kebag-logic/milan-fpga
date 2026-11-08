[R800] POSITIVE - exact head e69d243a61a8ec1c1ad8c473f809e1351dab1b61

# R800-1: external review of PR #861 (#665 S6b, the two-placement `milan_dp` twin)

- **Head under review:** `e69d243a61a8ec1c1ad8c473f809e1351dab1b61`, tree `037c224506ac65797390f90449df3cc743a553db`.
- **Delta reviewed:** the commits after S6a's `e6d27f3a`, that is `git diff e6d27f3a..e69d243a`: 32 files. No file under `hdl/` and no submodule gitlink changes in it.
- **Base and target:** source base `6584b7bf`. The PR is stacked on S6a (#853) and targets `dev-soft-core` once S6a merges.
- **Authority:** the [A10] rulings on #665: issuecomment-6724570965 (round 5); 6722002738, 6717765106 and 6716584453 where round 5 does not change them; 6715535566 for S6b's scope.
- **Out of scope, as directed:** the REBOOT carrier, the AECP-owned items (S11) and `aecp/README.md:24-29`.

**Verdict: POSITIVE.** There is no open BLOCKER, MAJOR or MINOR finding. Two RESIDUE items (wording only) and one SUGGESTION are recorded below. Every lens is covered clean at this head.

## What was executed at this head

All runs used clean clones of the committed head, built with the submodules at their gitlinks (`scripts/clean_tree.sh`). Verilator is the pinned 5.050; its identity was checked by `--version` through the pinned wrapper. The census used the pinned sv2v v0.0.12 and Yosys 0.66.

| Run | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/milan_dp twin` | rc 0. `twin: 0 finding(s)`. The only notes are 1 `[TAIL]` (ADP), 6 `[LEDGER]` and 6 `[OWED]`, among them `fabric-domain-one-new` and `fabric-vid2-join-in`, owed to #860. Same per-protocol counts as the author's. | `receipts/make-twin.txt` |
| the captures `fabric.json`, `split.json` and `report.json` | sha256 byte-identical to the author's published receipts (`fa6a5a12…`, `ee143865…`, `04014a9c…`). The run is deterministic. | `receipts/twin/` |
| `make -C tb/verilator/milan_dp twin-plants` | rc 0: 38 lines `REFUSED`, 0 `ESCAPED` (19 plants × 2 controls) | `receipts/make-twin-plants.txt` |
| `python3 -I tb/verilator/milan_dp/split_parallel.py --selftest` (from the review clone; the gate clones HEAD itself) | rc 0. The planted old rule gives `make -j8 split` rc 2 with `Vmilan_dp_split: No such file or directory`. The clean tree gives rc 0 with `checks: 71   failures: 0`. Ends `split_parallel: PASS`. | `receipts/split-parallel.txt` |
| `make split-mutants` | rc 0: `split mutants: 24 of 24 caught by the check each names` | `receipts/make-split-mutants.txt` |
| `make split-cdc` | rc 0: `checks: 13   failures: 0` | `receipts/make-split-cdc.txt` |
| `publication_census.py --check --jobs 4` (both populations) | rc 0: 6 shapes, `checks: 246   failures: 0`, `RESULT: PASS`. Every shape shows `split ctl ports: 80: C 12, F 16, R 34, E 6, M 12` with 4 ports read in neither placement. 229 s, peak RSS 1.64 GB. | `receipts/census-check.txt` |
| the same with sv2v v0.0.13 first on PATH | rc 2, refused before elaborating: "the census elaborates with the pinned sv2v v0.0.12 and Yosys v0.66 … not `sv2v v0.0.13`" (a correct refusal, kept as robustness evidence) | `receipts/census-check-refused-sv2v013.txt` |
| probe: Table 10-3/10-4 encoding and synthetic traces (`scripts/probe_mrp_table.py`) | 46 of 46 ok, PASS | `receipts/probe_mrp_table.txt` |
| probe: the comparison on the unplanted captures, with in-memory mutants (`scripts/probe_twin_compare.py`) | PASS (details under Conformance and Tests) | `receipts/probe_twin_compare.txt` |
| probe: the two new `available_index` mutants through `aecp_mutants.py`'s own campaign, plus an unplanted control (`scripts/probe_available_index.py`) | Both mutants are caught by `App.EntityReadSeesTheLastAdvertisedIndex` with their words. The unplanted control passes the test. PASS | `receipts/probe_available_index.txt`, `receipts/avidx/` |
| probe: boundary-gate classification (`scripts/probe_boundary_classes.py`) | No program naming the firmware's tree is unclassified. Removing any one of the three new entries leaves its file unclassified. PASS | `receipts/probe_boundary_classes.txt` |
| hosted check runs at this head (read-only snapshot, 2026-11-08 23:00 CET) | 22 success, 1 skipped by its `if:` (`Physical gPTP`), 25 in progress or queued, none failed. Succeeded: `split-cdc`, `firmware-unit`, `firmware-aecp-mutants`, `firmware-srp-mutants`, `firmware-control-mutants`, `firmware-boundary`, `firmware-verilator`, `verilator-lint`, `yosys-elaboration`, `bdd-conformance`, `wire-accountability`, `docs-check-no-git`, the docs and elaborate gates, and 2 of 19 Verilator shards. Still running: `publication-census` and 17 shards. | `receipts/hosted-checks-e69d243a.tsv` |

The probes edit no tracked file. Their mutants live in memory or in the mutant campaign's own copy. After the probes, the review clone was checked (`receipts/clone-integrity.txt`):

- `git status --porcelain --ignored` is empty (the probes' two bytecode caches were removed);
- HEAD and tree are as above;
- index modes and blobs equal HEAD's tree;
- the six gitlinks are unchanged.

## Findings

### RES-1 RESIDUE: the comment rule (issue-comment IDs, ruling IDs and lane labels in new source comments)

- **Lenses:** Docs.
- **Where:** 38 new comment or docstring lines in the reviewed delta, each listed with its `path:line` in `receipts/comment-rule-instances.txt` (`scripts/comment_rule_scan.sh`). That file has 42 lines. Four of them are runtime strings printed in the `[OWED]` notes, not comments, and are not part of this item: `twin_compare.py:460`, `:490`, `:530` and `:553`. Examples:
  - `sw/firmware/ctrl/app/ctrl_app_aecp.c:108` and `sw/firmware/ctrl/test/test_aecp.cpp:439` (`#665 issuecomment-6717765106, item 1`);
  - `tb/verilator/milan_dp/Makefile:868`, `:883` and `:884`;
  - `tb/verilator/milan_dp/tb_split_top.sv:61` (`#665 S6b`);
  - `scripts/ci_events.py:1344` and `:2494` (`#665 S6b`), and `:1345` (`ruling 6715535566 item 6`);
  - `.github/ci-templates/rtl-fast.yml:318`;
  - `sw/mailbox/census_split.py:11`, `:67` and `:70` (`ruling 6715535566`, `S11's`);
  - `sw/mailbox/census_plants.py:537` and `sw/mailbox/publication_census.py:117`;
  - the docstrings and comments of `twin_compare.py`, `twin_grades.py`, `twin_mrp.py`, `twin_plants.py`, `twin_decode.py`, `twin_fw.py`, `twin.hpp` and `split_parallel.py`.
- **Authority:** the owner's comment rule of 2026-10-15. Source comments state behaviour and reason with issue and requirement IDs. They never show lane names, review rounds, reviewer IDs or issue-comment IDs. A new instance in the reviewed delta is RESIDUE.
- **Impact:** wording only. No measurement, verdict, test, code or generated artifact changes.
- **Exact fix:** in each listed comment or docstring:
  - keep `#665` (and `#857`, `#858` or `#860` where they apply) and the requirement clause;
  - delete the `issuecomment-NNNN, item N` and `ruling NNNN item N` references;
  - replace a lane label (`S6b`, `S11`, `S2b`) with the issue or the behaviour it stands for. For example, `(#665 S6b)` becomes `(#665)`, and "is S11's" becomes "waits for REBOOT's carrier (#665, #787)".
- **Verification:** `scripts/comment_rule_scan.sh <repo> e6d27f3a <new head>` prints only the four runtime strings, or nothing.

### RES-2 RESIDUE: "Table 7.1" left in two new comments, and the PR body names only one of them

- **Lenses:** Docs.
- **Where:**
  - `sw/firmware/ctrl/test/test_aecp.cpp:437`: "IEEE 1722.1-2021 Table 7.1: the ENTITY descriptor's available_index is …";
  - `sw/firmware/ctrl/test/aecp_mutants.py:408`: "(IEEE 1722.1-2021 Table 7.1), not ADP's next one";
  - the PR body's *Known limitations*, which says only `aecp_mutants.py:408` "cites 'Table 7.1' too".
- **Authority:** issuecomment-6724570965 item 4 corrects the citation to IEEE 1722.1-2021 Table 7-2 (the ENTITY descriptor), as `ctrl_app_aecp.c:106`, the twin and the docs now cite it. The ruling names only the C line, so the two comments are a wording residue, not a defect of the ruled change. The PR body's list of what was left is incomplete.
- **Impact:** wording only. The test, its assertions and the mutants are unchanged by the fix.
- **Exact fix:**
  - in both comments, change "Table 7.1" to "Table 7-2";
  - in the PR body, either list `test_aecp.cpp:437` beside `aecp_mutants.py:408`, or drop the item once both are fixed.
- **Verification:** `git grep -n 'Table 7\.1' -- sw/firmware/ctrl tb/verilator/milan_dp` prints nothing.

### SUG-1 SUGGESTION: the Applicant grade does not read a frame that omits an attribute as that attribute's tx!

- **Lenses:** Tests, Conformance.
- **Where:** `tb/verilator/milan_dp/twin_mrp.py:269-289` (`observations`), as its docstring at `:16-20` states. A non-LeaveAll frame is a tx! only for the attributes it carries.
- **Evidence:** in Table 10-3, tx! goes to every Applicant of the participant. An MRPDU that leaves out an attribute in VN, AN, AA, VP, LA, LO or AP is therefore not an Applicant's (note 7, a full MRPDU, aside). The grade cannot refuse such an omission. LeaveAll frames do get the strict reading: my probe confirms that a LeaveAll frame omitting a declared attribute is refused.
- **Why only a SUGGESTION:**
  - The rulings let the Applicant group attributes into MRPDUs (issuecomment-6717765106 item 4; IEEE 802.1Q-2018 10.8). A frame is therefore not provably one transmit opportunity.
  - The rate and periodic grades (`twin_grades.py:156-185`) bound the gap.
  - Neither half shows such an omission at this head.
- **Possible outcome:** group a half's frames of one application by transmit opportunity (same millisecond), and read each group as one tx! for every attribute.

**Earlier findings.** None is open on PR #861. I read the PR's public thread only after my own pass; my draft verdict from before that read is kept as `receipts/draft-verdict-before-prior-findings.txt`. The thread held only the two review-start notices, so there were no findings to resolve or keep. The issue holds the [A10] rulings and the [A746e] REVIEW READY, whose claims I checked against my receipts above.

## Lenses

### Conformance: CLEAN

- **(1) `make twin`**
  - rc 0 with only `[TAIL]`, `[LEDGER]` and `[OWED]` notes (`receipts/make-twin.txt`).
  - **Every ledger row is a real difference at this pin.** `probe_twin_compare.py` evaluated each `LEDGER` row (`twin_compare.py:372-413`). Each holds. Each half's selection fails the other half's predicate. The two selections differ.
  - **The AECP owner's rows 5 and 6 agree, so they have no row.** The STREAM_INPUT 0 GET_STREAM_INFO notices (10 per half) and the LOCK_ENTITY notices (5 per half) are equal without `sequence_id`. A fabric release notice carries flags bit 0 (UNLOCK).
  - **Each owed row names its owner and asserts the fabric's exact behaviour.** The `OWED_GRADES` rows are at `twin_compare.py:547-564`: `fabric-mvrp-leave-all` (#857), `fabric-domain-one-new` (#860) and `fabric-vid2-join-in` (#860). `OWED`'s `entity-available-index` (`:483-490`) is owed to #858. `stream-output-0-notices` and `split-talker-failed` are owed to the SRP adapter round, as issuecomment-6717765106 item 3 rules.
  - **A row whose defect has gone is reported.** `apply_grade_rows` (`:567-583`) and `apply_rows` (`:586-610`) do so, and the four `vanished-*` fabric plants are refused by "the defect has gone" or "the difference has gone".
  - **The #860 rows are load-bearing.** Removing either #860 row brings back exactly the fabric findings it covered: 1 for the Domain, 2 for VID 2. Changing either asserted trace by one character gives "does not hold".
- **(2) The Table 10-3 grade**
  - `TRANSITIONS`, `TX` and `TXLA` (`twin_mrp.py:58-77`) match a second transcription, `third_party/lwSRP/src/core/mrp_mad.c:149-238`, row by row. The only differences are cells where the twin brackets an action (optional) that lwSRP omits.
  - `rLA!` equals `rLv!`.
  - The tx! and txLA! actions match: VN and AN send New.
  - Note 8 is implemented at `:159-160`, and matches the processor's own encoding (`KL_srp_talker_fsm.sv:307`). Notes 4 and 5 are at `:147`.
  - 10.7.6.3 (`sJ` is JoinIn only with the Registrar IN) is implemented at `:134-141`.
  - The Registrars are at `:79-91`: MSRP's with Milan v1.2 4.2.7.2.2's IN/rLv! to MT, MVRP's Table 10-4 as printed.
  - `OPER_P2P` (`:101`) is each half's configured value. The fabric half has `hdl/milan/KL_pp_shadow.sv:1289` `.p2p_i (1'b1)`. The split half has `sw/firmware/ctrl/srp/srp_mbx.c:252-253`, both participants `true`.
  - Synthetic traces behave as the table requires (`receipts/probe_mrp_table.txt`):
    - New, New, JoinMt is legal;
    - one New then JoinMt is illegal;
    - MVRP JoinIn with the Registrar MT is illegal;
    - after a received JoinIn the next JoinMt is illegal;
    - MSRP's rLv! goes to MT and MVRP's to LV;
    - Lv before any declaration is illegal;
    - a LeaveAll frame omitting a declared attribute is illegal.
  - The split's MSRP and MVRP pass at this head.
  - Across halves, MSRP is compared only by the declaration state at each LeaveAll boundary (`compare_declarations`, `twin_compare.py:249-259`). `msrp_attributes` is read only by the owed rows. The only other MSRP cross-half check is that the frames carry the same Ethernet header (`:653-654`).
- **(3) `sequence_id` of entity-sent commands**
  - The command byte compare uses `without_seq` (`twin_compare.py:191`), per destination controller (`:213-218`).
  - `grade_commands` (`twin_grades.py:125-145`) requires a strict modular rise, allows gaps, and matches each response to its command.
  - At this head the fabric sends `{first: [0], second: [0, 1]}` and the split `{first: [1], second: [0, 2]}`. Refusing the gap, or byte-comparing `sequence_id`, each makes the comparison find a difference (probe). Both rules are load-bearing, per IEEE 1722.1-2021 9.2.2.9 and issuecomment-6722002738 item 2.
- **(6) The boundary gate and the citation**
  - `sw/firmware/ctrl/test/ctrl_configs.py:231-234` and `:259-261` hold the three entries. Each is load-bearing (probe).
  - The README's 181 pin controls (`sw/firmware/ctrl/README.md:255`) match the author's `ctrl_boundary` receipt ("117 boundary, 181 pin and 4 figure controls"). The hosted `firmware-boundary` job succeeded at this head.
  - `ctrl_app_aecp.c:106` cites IEEE 1722.1-2021 Table 7-2. The value (`:113-118`) follows issuecomment-6717765106 item 1.

### RTL: CLEAN

- **No product RTL changes.** The delta touches no file under `hdl/` and no gitlink.
- **The CSR window.** `tb/verilator/milan_dp/tb_split_top.sv:56-78` and `:328-333` bring the datapath's CSR window out as ports. `sim_split.cpp:94-104` drives the same idle values the old ties did (valids 0, `bready` and `rready` 1, address and data 0). The split leg still passes (71/0) and so do its 24 mutants.
- **The twin's AXI master.** The split half (`twin_split.cpp:246-278`) drives the window on `dp_clk` cycles, with a guard that throws on a missing response.
- **The image default is unchanged.** `ctrl_plat.c:193-219` defaults `CTRL_PLAT_MAAP_PREFERRED` to 0, which `ctrl_app.c:19` and `:78` read as "draw at random". `git grep` shows only `twin_fw.py:91` defines it.
- **The split rule.** `Makefile:870-871` (`split: build-split` then `$(MAKE) exec-split`) removes the race. The selftest proves the old rule fails under `-j8`.
- **The split CDC check** passes: 13/0.
- **The census** shows every split ctl port classed and consumed, or read in neither placement, in all six shapes.

### Robustness: CLEAN

- **Malformed and truncated MRPDUs** raise by name (`twin_decode.py:287-315`, `srp_wire_compare.require`). A frame of no compared protocol stops the load (`:93`).
- **The halves exit non-zero** on host or AXI timeouts (`twin_split.cpp:262`, `:277`, `:451`; `twin_fabric.cpp:261`, `:276`).
- **`split_parallel.py`** refuses rather than passes:
  - when it cannot make a clean tree (exit 2);
  - when the Makefile does not hold the rule exactly once;
  - unless there are a verdict line and rc 0.
- **The census refuses a non-pinned sv2v** (observed, rc 2).
- **Owed rows fail closed** both when their defect goes and when their trace moves (plants and probe).
- **The `available_index` boundaries** are each asserted (`test_aecp.cpp:443-482`):
  - 0 before the first ENTITY_AVAILABLE;
  - N-1 after N;
  - kept across a link-down;
  - 0 after DEPARTING.
- **Repeat runs** reproduce the author's capture bytes exactly.

### Tests: CLEAN

- **All 19 plants are refused in both controls** (38/38). Each plant was read against its words and tests what it names:
  - `command-sequence` is caught by `grade_commands` and not by the byte compare;
  - `mvrp-join-in` and `mvrp-received-join` reach 10.7.6.3 and the Registrar;
  - `vanished-domain-new` and `vanished-vid2-join-in` plant the legal fixed trace (New ×2, then JoinMt);
  - `domain-trace-moved` and `vid2-registrar-in` keep the defect but change the asserted trace.
- **`split_parallel.py --selftest`** plants the old rule under the real simulator and requires the missing-binary failure.
- **The two new firmware mutants** (`aecp_mutants.py:407-418`) are caught by `App.EntityReadSeesTheLastAdvertisedIndex` with their words. The unplanted arm passes, so the test fails only for the defect (`receipts/avidx/`).
- **My in-memory mutants** of the comparison were each detected:
  - `sequence_id` byte-compared;
  - gaps refused;
  - each `OWED_GRADES` row removed;
  - each #860 trace changed.
- **SUG-1** is the only weakness found, and it is optional.

### Docs: CLEAN

- **`tb/verilator/milan_dp/README.md`** (the two-placement section) matches the code and my run: rows, plants and words, the counts (JoinMt x79, JoinIn x15), the per-controller ids, and the 19 plants in 38 controls.
- **Also consistent with the code and the receipts:**
  - `docs/design/MAILBOX_SPLIT.md` (the twin, the split census, the split rule and its gate, the open items);
  - `docs/testing/CI_WORKFLOWS.md` (`split-cdc`);
  - `tb/verilator/mbx/README.md`;
  - `sw/firmware/ctrl/plat/README.md:77`;
  - `sw/firmware/ctrl/README.md:255`.
- **The PR body** says it touches S6a's file (`tb/verilator/milan_dp/Makefile`) and S2b's tree, as the rulings direct.
- **RES-1 and RES-2** are wording only.

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `twin_mrp.py:58-163`, `twin_compare.py:191-259`, `:372-610`, `twin_grades.py:125-145`, `ctrl_app_aecp.c:102-118`, `ctrl_configs.py:231-261`, `KL_pp_shadow.sv:1289`, `srp_mbx.c:252-253`, lwSRP `mrp_mad.c:149-238`; the rulings; `receipts/make-twin.txt`, `probe_mrp_table.txt`, `probe_twin_compare.txt` | R800-1 | `e69d243a61a8ec1c1ad8c473f809e1351dab1b61` |
| RTL | CLEAN | `tb_split_top.sv:56-78`, `:328-333`; `sim_split.cpp:94-104`; `twin_split.cpp:225-278`; `Makefile:866-980`; `ctrl_plat.c:190-219`; no `hdl/` or gitlink change; `make-split-mutants.txt`, `make-split-cdc.txt`, `split-parallel.txt`, `census-check.txt` | R800-1 | `e69d243a61a8ec1c1ad8c473f809e1351dab1b61` |
| Robustness | CLEAN | `twin_decode.py:85-97`, `:287-315`; `twin_split.cpp:225-278`, `:404-451`; `split_parallel.py:52-127`; `test_aecp.cpp:437-482`; `census-check-refused-sv2v013.txt`; the owed rows' fail-closed paths | R800-1 | `e69d243a61a8ec1c1ad8c473f809e1351dab1b61` |
| Tests | CLEAN | `twin_plants.py`; `twin_compare.py:68-120`, `:670-680`; `make-twin-plants.txt` (38/38); `split_parallel.py:103-112`; `aecp_mutants.py:407-418` and `receipts/avidx/`; `probe_twin_compare.txt`; `probe_boundary_classes.txt` | R800-1 | `e69d243a61a8ec1c1ad8c473f809e1351dab1b61` |
| Docs | CLEAN (RES-1 and RES-2 recorded as RESIDUE) | `tb/verilator/milan_dp/README.md` (two-placement section), `docs/design/MAILBOX_SPLIT.md`, `docs/testing/CI_WORKFLOWS.md`, `tb/verilator/mbx/README.md`, `sw/firmware/ctrl/plat/README.md:77`, `sw/firmware/ctrl/README.md:255`, the PR body, `receipts/comment-rule-instances.txt` | R800-1 | `e69d243a61a8ec1c1ad8c473f809e1351dab1b61` |

## Real limits

- **Not run by me** (author receipts and hosted jobs only):
  - the firmware boundary gate (`ctrl_boundary.py --require-rv32 --selftest`) as a whole. I ran its classification step as a probe, and the hosted `firmware-boundary` job succeeded at this head;
  - the full Verilator sweep, `test_builder.py`, `test_ctrl_firmware.py --self-test`, the identity compare against `a9d69c77` and `publication_census.py --selftest`. The last is the hosted `publication-census` job, still running when snapshotted;
  - the native replay of every workflow `run:` step. The author's `ci-replay-table.md` and `not_run.json` show 546 ran with rc 0 and 86 could not run, each with its reason. I read those receipts and did not reproduce them.
- **The standard's printed tables are not in the repository.** Table 10-3 and 10-4 were checked against a second in-tree transcription (lwSRP, which cites IEEE 802.1Q-2018 10.7.7) and the processor's note-8 encoding, not against the standard's text.
- **Untested in this stimulus:** the MVRP checks of Milan v1.2 4.3.2 and 4.4.1 hold vacuously (no stream frame, no settled sink), as the PR states.
- **Untested anywhere:** no plant distinguishes Milan's MSRP Registrar cell. It changes no message an Applicant may send, as `twin_mrp.py:31-34` states.
- **Hosted checks:** they were in progress when snapshotted. I distinguished the executed jobs from the skipped context (`Physical gPTP`, by its `if:`) and claim no hosted verdict.
- **No manager source bank** runs at this head, and none is claimed. No act run (split PR). Physical calibration NOT RUN. No hardware.

## Pending manager duties

- The exact-head hosted contexts to completion, including `publication-census` and the 17 Verilator shards still running.
- S6a (#853) merges first. Then retarget this PR to `dev-soft-core` and validate the merge candidate against live `dev-soft-core` (builder and native banks), linking its receipts on the PR.
- Carry RES-1 and RES-2 to the residue checklist.
- The author's open question: whether a hosted job should run `split_parallel.py`.
- The #857, #858 and #860 lanes each delete their owed row when they land.

R800-1 FINISHED
