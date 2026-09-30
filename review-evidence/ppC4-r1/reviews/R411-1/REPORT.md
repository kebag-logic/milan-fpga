[R411] POSITIVE - exact head a9ce0fa2e0b8b120703c6e541668d4281cec286e

# R411-1 external independent review: PR #137 (lane C4, ACMP), issues #45 / #47 / #48

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head `a9ce0fa2e0b8b120703c6e541668d4281cec286e`, tree `7d1bfe6e68b3ce9555e32eb1e9fb14220b98f43e`. Verified in the detached review clone.
- Base `b2db3a970cedbbff2f8ba813acb96122c442bc58`, which is processor `main` and includes PR #132 and PR #133. Six commits: d87b3d5, 2a3e608, af6a5f1, 20e24d4, a7ccd9e, a9ce0fa.
- Review start: PR #137 comment 5903340306. Assignment: #45 comment 5891906554.

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open at this head. Four SUGGESTIONs follow. They do not affect the verdict.

## How the review was reconstructed

1. **Governance and conventions.** The repository has no `AGENTS.md` or `CONTRIBUTING.md` at this head; both are absent from the tree. I used `README.md` and `docs/README.md` instead: the ID registries, the citation rule (§4) and the editing workflow (§6).
2. **Frozen scope.**
   - Issues #45, #47 and #48: the body and every comment. The only comments are the assignment (5891906554), TAKEN and REVIEW READY.
   - The PR #137 body. It is identical to the published `author/PR-BODY.md` apart from a trailing newline.
   - The two review-start comments on the PR.
   - **No prior review findings exist on this PR.** There are no reviews and no finding comments, so nothing needed to be resolved or retained.
3. **Authorities, taken from the architecture as it stands.**
   - `docs/architecture/05_acmp_engine.md`: §3 dispatch table, the A1 to A17 action legend, and F05.14's GET_RX_STATE forms.
   - `08_timing.md` F08.1: T-ACMP-CMD 200 ms, T-ACMP-DELAY 0 to 1 s, T-ACMP-RETRY 4 s, T-ACMP-NOTK 10 s, T-MRP-LEAVEALL 10 to 15 s.
   - `00_MILAN_COMPLIANCE_REVIEW.md`: the REQ-ACMP-001, -012 and -016 rows and F00.2.
   - The port contract of `protocol_processor_top` (`acmp_bound_*_o`, lines 610-619) and the integrator guide §8 row.
   - The specification PDFs are not distributed, so clause and table citations were checked for consistency with the tree's own citations only.
4. **Diff and history.**
   - The full `git diff b2db3a97..a9ce0fa2` was read line by line. It is 1,196 lines across 8 files, all under `tb/`.
   - `git diff b2db3a97..a9ce0fa2 -- hdl tb/common docs scripts syn .github Makefile` and the un-rerun drivers' directories is empty.
5. **Public evidence.** `kebag-logic/milan-fpga@2aa6c820:review-evidence/ppC4-r1` contains `MANIFEST.json`, `author/HANDOFF.md` (published sha256 90c6b93c…) and `author/PR-BODY.md` (4dc1993d…). The hosted CI for the exact head was also inspected (see Tests).

## Findings

There are no findings at BLOCKER, MAJOR or MINOR.

### S1 — SUGGESTION — Docs, Conformance — spec table cited for the ACMP message_type codes

- **Where:**
  - `tb/acmp_listener/README.md:69`
  - `tb/acmp_listener/sim_main.cpp:1209,1220`
  - `tb/pp_top/README.md:1141`
  - `tb/pp_top/sim_main.cpp:8974`
  - the PR body, §1 "Clause"
- **Evidence:**
  - The new text cites "IEEE 1722.1-2021 Table 8-2" as the source of the message_type codes.
  - The tree already cites "IEEE 1722.1 Table 8.1 message types" and "Table 8.2" for the ACMP **flags** (`tb/acmp_nvm/sim_main.cpp:176,184`). It cites "IEEE 1722.1-2021 Table 8-3" for status codes (`hdl/acmp/pp_acmp_pkg.sv:119`).
  - The existing `acmp_nvm` citation carries no edition and uses 2013-style numbering. The 2021 edition may therefore have renumbered the tables, which is consistent with the PR's "§8.2.1.6 sets control_data_length".
  - Without the standard, which of the two is right cannot be settled here. The codes themselves are correct: they match 05 §3's list 0/1 … 12/13, with 14 and 15 left over.
- **Impact:** a compliance reader cross-checking REQ-ACMP-012 finds two table numbers for one code list.
- **Suggested outcome:** name the edition next to both citations, or align them. This can be done at any later documentation touch.

### S2 — SUGGESTION — Docs — F00.2 "Open residue" of GAP-15 still links #45

- **Where:** `docs/00_MILAN_COMPLIANCE_REVIEW.md:509`, with the column rule at `:513`.
- **Evidence:**
  - The PR closes #45. The GAP-15 row keeps #45 as its open residue.
  - The column is explicitly "the audit of 2026-09-18 at main `6a878f6`", a dated snapshot, so it is not wrong after the merge.
  - The PR body's wording "per that table's own rule it reads none found" overstates what the rule says. The PR discloses the point under "What remains".
- **Suggested outcome:** a manager decision on whether the snapshot column is refreshed when a residue issue closes.

### S3 — SUGGESTION — Conformance, Robustness (pre-existing RTL, not attributable to this diff) — the bound stream identity survives an A8 teardown

- **Where:**
  - `hdl/top/protocol_processor_top.sv:1659-1663` (latch at A15) and `:1664-1674` (clear only on disarm)
  - the port comment at `:612-616`, "held while acmp_bound_o"
- **Evidence:**
  - After T-ACMP-NOTK in SETTLED_NO_RSV, or EVT_TK_UNREGISTERED in SETTLED_RSV_OK, A8 clears the listener's settled {stream_id, DA, VLAN}.
  - GET_RX_STATE then reports zeros, while `acmp_bound_sid/dmac/vlan_o` keep the last stream.
  - The behaviour matches the documented port contract. The PR records it as noted, not graded and not changed, which respects the lane's STOP rule on port-visible change.
- **Suggested outcome:** track it as its own issue, since any change is a class-D, parent-visible decision.

### S4 — SUGGESTION — Robustness, Tests — no per-run timeout in the mutation driver

- **Where:** `tb/pp_top/acmp_mutants.py:188`, the same pattern as `d3_mutants.py:486`.
- **Evidence:** `subprocess.run` is called without a timeout. A planted defect that hangs a simulation would stall the campaign instead of failing it.
- **Impact:** this cannot produce a false KILLED. A hang yields no tally, so it never counts as a kill. Its only cost is wall time.
- **Suggested outcome:** add a generous timeout that records such a run as SURVIVED/TIMEOUT.

## Lens results

### Conformance — CLEAN

**#47, REQ-ACMP-012 (Milan §5.5.3.1):**
- B13 (`tb/acmp_listener/sim_main.cpp:1218`) drives 3, 5, 7, 9, 11, 13, 14 and 15. Each arrives with the own listener EID and a valid listener unique_id, in both PRB_W_RESP (SUCCESS) and PRB_W_RESP2 (NO_BANDWIDTH), and is shaped as the perfect probe answer.
- It is graded inert on every face, using the model cell plus explicit checks: no frame, no write, no timer op, no notify, no strobe, the record unchanged, and exactly one RX free of the slot it arrived in.
- This matches 05 §3 "anything else → ignore". The issue asked for 3, 5, 7, 9, 11, 13 and 14 in one probing state; the lane covers a superset.

**B14 (`:1260`):**
- Grades the controller EID, talker EID and talker unique_id terms of the §5.5.3.5.18 / .25 step-1 guard in both probing states.
- The unaltered answer then settles, which is the positive control.
- The fourth term, sequence_id, is pre-existing B8. My probe `r411_guard_seq_dropped` confirms B8 kills it.

**#45, REQ-ACMP-001 (Milan §5.5.2.2, 03 V3, F09.4 96-B row):**
- F29 (`tb/rx_validator/sim_main.cpp:766`) sends the cdl-84 form with a patterned 40-byte tail. It is committed whole (96 bytes) with no counter moving, and `run_case` checks every counter against the offset model. The header beat is field-exact and equal to the 56-B form's apart from cdl.
- AL1 to AL4 (`tb/pp_top/sim_main.cpp:9021`) show long UNBIND_RX, BIND_RX and PROBE_TX each answered by the byte-identical 56-B cdl-44 response.
- AL2's regenerated PROBE_TX #2 proves that the long command's fields reached the record, because AL1 had unbound the sink.

**#48, REQ-ACMP-016 (Milan §5.5.3.5.18/.36/.42/.45, §5.3.8.5/.9):**
- AS1 to AS6 (`:9079`–`:9221`) follow F05.2/F05.4 and the A5/A12/A13/A15/A8/A9/A10 actions.
- The GET_RX_STATE expectations match F05.14 row by row:
  - probing: cc 1, FAST_CONNECT, stream fields 0
  - settled: the response's {sid, DA, VLAN}
  - unbound: all zero except the echoes
- The Listener declaration is attribute type 3, FirstValue = StreamID, with FourPackedType Ready (2) on both New and Lv.
- AS5 grades the SETTLED_RSV_OK state itself, not only its Table 5.39 bytes (which equal Table 5.38's): the sink outlives T-ACMP-NOTK plus the maximum T-ACMP-DELAY, with the talker still discovered (ADP valid_time 10, which is 20 s).
- The tests' timing windows are consistent with F08.1:
  - AI3: 195 to 260 ms around the 200 ms T-ACMP-CMD
  - AS1: 4600 ms, which is at least the 200 ms duplicate plus 200 ms plus the 4 s retry
  - AS5: 11.5 s, which is at least 10 s plus up to 1 s delay

**No RTL, port, parameter or architecture change.** Every expectation is graded against the unchanged `hdl/`.

### RTL — CLEAN

- The diff contains no RTL. `git diff b2db3a97..a9ce0fa2 -- hdl` is empty.
- `tb/pp_top/pp_top_wrap.sv` only connects four existing top outputs (`acmp_bound_eid/sid/dmac/vlan_o`), with widths 8×64, 8×64, 8×48 and 8×12, which match the top's `N_STREAM_IN_P*` declarations at `:611-619`.
- I read the planted-edit targets and the graded RTL behaviour at head:
  - the listener pre-decode `txn_msg_ok_w` (`KL_pp_acmp_listener.sv:450-453`) and `probe_match_w`
  - the validator V1 limit
  - the `st_ls_r` service stage
  - the `binding_view` latch (`protocol_processor_top.sv:1644-1677`)
  - the SRP listener matcher (`KL_srp_listener_fsm.sv:408-413`)
  - the trace record layout (`:3045-3047`; ring lane 1 = bits [95:64] = {src, lost, payload}; `KL_pp_trace_ring.sv:62,106`) and `pp_evr_map.tk_reg = 0` (`pp_pkg.sv:298`)
- The bench's decode helpers (`lane()`, `registered_traced`, snapshot words 12, 14, 15 and 25) agree with them.
- `./scripts/lint_hdl.sh` passes with the scoped 5.050 simulator: rc 0, 41 LINT OK.

### Robustness — CLEAN (S3 and S4 are suggestions)

- Section AC runs on a fresh model (`AcmpPathPhase`, `model2`/`h2`), so the main DUT's timeline is untouched.
- The `main()` dispatch (`sim_main.cpp:10459-10471`) keeps `--gsi-internal-only`, `--name-writes-only`, `--d3-only` and `--dr3a` free of AC. All four pp_top-building entry points pass at head.
- Byte-exact MRPDU checks are aligned with `sync_join` inside a LeaveAll-free window (`la_window`).
- I instrumented `registered_traced` in a scratch copy. The trace span in the AS3 and AS4 windows is 0 and 1 records of the 256-record ring, and the count never wraps, so the "no TK_ATTR_REGISTERED{1}" and "exactly one" checks are not vacuous. This is `public/probe_trace_span.txt`, and the author's own fix of an earlier source-2 keying confirms it was a real risk.
- The suites give the same tallies under two simulator builds: 5.050 scoped and 5.052 system.
- The mutation driver:
  - plants each defect in a private temporary copy of `hdl/`, `tb/common/` and the grading suite, never in the tree
  - refuses an edit whose text does not occur exactly once
  - counts KILLED only with build 0, a completed tally, a non-zero exit and every named check failing
  - runs goldens first and gives a mutant with the same name graded by two suites two distinct labels and logs

### Tests — CLEAN

**Suites at the exact head, in exports of the head tree:**

| Suite | Scoped 5.050 | System 5.052 |
|---|---|---|
| `tb/acmp_listener` | 2988/2988 PASS, rc 0 | same |
| `tb/rx_validator` | 495/495 PASS, rc 0 | same |
| `tb/pp_top` | 7930/7930 PASS, rc 0 (AC 42/42, 18,924 ms simulated) | same |

These are the PR's figures. `check_upc_map` PASS.

**`tb/pp_top/acmp_mutants.py` at 8 jobs:**
- 19 of 19 KILLED by their named checks, and the three goldens PASS (rc 0).
- Every failing count equals the README tables and the PR body exactly:

| Mutant | Failing checks |
|---|---|
| `msg_ok_forced` | 93/2988 listener and 1/42 AC |
| `guard_ctlr_dropped` | 50/2984 |
| `guard_talker_eid_dropped` | 40/2984 |
| `guard_talker_uid_dropped` | 30/2984 |
| `cdl_not_44_rejected` | 27/495 and 19/42 |
| `st_ls_settle_as_withdraw` | 7 |
| `st_ls_teardown_as_declare` | 1 |
| `st_ls_sid_da_swapped` | 7 |
| `st_ls_state_none` | 7 |
| `st_ls_vid_dropped` | 7 |
| `st_ls_index_zero` | 6 |
| `st_ls_teardown_lost` | 2 |
| `bound_view_not_latched` | 2 |
| `bound_dmac_from_sid` | 2 |
| `bound_view_not_cleared` | 1 |
| `matcher_da_ignored` | 5 |
| `matcher_vid_ignored` | 5 |

**Discrimination beyond the author's table.** My `scripts/r411_probes.py` reuses the driver's own grading rule. 11 of 11 extra defects are KILLED on named checks:
- the listener admitting only type 13, 9 or 5: B13 fails for that exact type in both states, so the census is per type and not only aggregate
- admitting only 7, or only 14, at the top: AI3 fails, which also proves both frames reach the listener through the real steer
- the sequence_id guard term dropped: B8
- a validator rejecting only cdl > 44, with the short form intact: F29 in both forms, and AL1 to AL3
- the SRP matcher ignoring stream_id: all three AS3 checks, so the third near miss discriminates too
- the bound VLAN not latched: AS2 and AS5
- the bound talker EID not latched: AS2

I found no defect within the acceptance lists that the tests miss.

**Other entry points that build the changed `tb/pp_top`, all at head:**
- `gsi_mutants.py`: 20 detected, golden and restored PASS, rc 0
- `name_wr_mutant.py`: decode killed, golden and restored PASS, rc 0
- `d3_mutants.py` in six `--only` chunks at 8 jobs: 83 of 83 KILLED, 11 golden runs PASS, rc 0 each

**Hosted evidence at the exact head:**
- Push run 36663365099: `docs-gates`, `portability` and `suites` executed with success.
- PR run 36663373922: the same three jobs executed with success. It checked out merge `baa3f76` of a9ce0fa2 into b2db3a97; `main` is still b2db3a97, so that tree equals the head tree.
- The only skipped step in either run is "Build Verilator v5.050", a cache hit.
- The hosted `suites` log shows the three changed suites at 2988, 7930 and 495, and "suites: 1016816 checks total, 0 failing". The same job also executed the SRP LeaveAll mutation campaign and the `nvm_port` figures check, green. The manager owns hosted and act acceptance.

**The author's un-rerun drivers are untouched by this diff:**

| Driver | What it reads | Changed by this diff |
|---|---|---|
| `make -C tb/srp_top mutants` | `hdl`, `tb/{common,srp_top,srp_stream_fsms,srp_encoder}` | no |
| `make -C tb/nvm_port figures` | `tb/nvm_port`, `hdl/packet_engine`, `tb/common` | no |
| `syn/yosys/run.sh` | `hdl` | no |
| `tb/srp_admission/mutants.py` | `tb/{common,srp_admission,srp_top}` | no |
| `tb/acmp_talker/retry_mutants.py` | `hdl`, `tb/{acmp_talker,common}` | no |

No other suite's Makefile, C++ or Python reads the three changed `tb/` directories. `tb/acmp_nvm` references only `hdl/acmp/KL_pp_acmp_listener.sv`, which is unchanged. Every suite other than the three changed ones therefore sees byte-identical inputs to the base.

### Docs — CLEAN (S1 and S2 are suggestions)

- The suite READMEs match what I measured:
  - `tb/acmp_listener/README.md`: 2988 checks and the mutation table
  - `tb/rx_validator/README.md`: the 495 tally, the F29 text and the M5 row
  - `tb/pp_top/README.md`: the section AC narrative, the `--acmp-only` usage, the about-19 s cost and the 14-row mutation table
- Driver usage in the README matches the driver's argument parser.
- No stale count remains. The "2 of 2544" at `tb/acmp_listener/README.md:101` is a dated historical record.
- The PR body's parent-visible list and "What remains" are accurate and disclose the open parent items.
- Doc gates in an export of the head:
  - `make links`: 976 OK
  - `make matrix`: 115 REQ / 17 GAP OK
  - `make modmatrix`: 94 rows, 0 untested
  - `make params`: 26 OK
  - `make lint`: 41 mermaid + 18 wavedrom blocks OK
  - `make stale`: rc 0, run in the clone and read-only
  - `git diff --check b2db3a97..a9ce0fa2`: rc 0
- `wavedrom-check` was not run locally, because it would bootstrap a virtual environment. `docs/` is unchanged, and the hosted `docs-gates` job executed with success.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | B13/B14, F29, AC AI/AL/AS against 05 §3, A-legend, F05.14, F08.1, 00 REQ-ACMP-001/012/016 rows, port contract `:610-619` | R411-1 | a9ce0fa2e0b8b120703c6e541668d4281cec286e |
| RTL | CLEAN | `hdl/` diff empty; `pp_top_wrap.sv` port hookup; planted-edit targets in listener, validator, `st_ls_r`, `binding_view`, SRP matcher, trace record; `lint_hdl.sh` rc 0 | R411-1 | a9ce0fa2e0b8b120703c6e541668d4281cec286e |
| Robustness | CLEAN | fresh-model isolation, `main()` flag dispatch, LeaveAll/join alignment, trace-ring span probe, two simulator builds, driver grading rule (S3, S4 suggestions) | R411-1 | a9ce0fa2e0b8b120703c6e541668d4281cec286e |
| Tests | CLEAN | 3 changed suites ×2 tools; `acmp_mutants.py` 19/19; 11/11 reviewer probes; `gsi_mutants`, `name_wr_mutant`, `d3_mutants` 83/83; hosted executed jobs; un-rerun driver input analysis | R411-1 | a9ce0fa2e0b8b120703c6e541668d4281cec286e |
| Docs | CLEAN | three suite READMEs, PR body, `acmp_mutants.py` docstring, 00 F00.2, doc gates (S1, S2 suggestions) | R411-1 | a9ce0fa2e0b8b120703c6e541668d4281cec286e |

## Real limits

- **Simulator substitution.** The simulator path named in the assignment does not exist on this host. I used the scoped Verilator 5.050 wrapper from a sibling manager run directory instead. Its identity: "Verilator 5.050 2026-07-01 rev v5.050", wrapper sha256 905795b9…, recorded in `public/tool_identity.txt`. I cross-ran the changed suites with the system 5.052 build, which is the author's version.
- **Full bank not run locally.** The full processor sweep (`./scripts/run_suites.sh`) is a full bank and outside my allowance. Its evidence here is the hosted executed `suites` job at the head (1,016,816 checks, 0 failing), plus the byte-identity argument for every unchanged suite.
- **No manager bank receipts to inspect.** The public evidence directory `review-evidence/ppC4-r1` contains only the author's handoff and PR body. No manager receipts for the source static/builder and native banks were posted there or on the issue or PR, so I could not inspect them. The assignment states they passed.
- **Parent side not run.** The parent consumer bank, the parent C++ and Python idiom gates on the new files, and `measure_test_evidence --check` are parent-side and were not run by this reviewer.
- **Citations unverified against the standard.** The specification PDFs are not available here. Citations were checked against the tree's own documents only, which is the reason S1 is a suggestion.
- **Raw logs not published.** The per-mutant raw build logs and the unredacted suite logs are retained locally and are not published, because they carry host paths. The redacted suite logs and every `results.json` are published.
- **No hardware.** Physical calibration was NOT RUN and no hardware was used. Field skips are not hardware proof.
- **Clone integrity after all probes.** HEAD and tree are exact. Status is clean, including ignored files. The index equals HEAD and the worktree equals the index. All tracked blobs re-hash equal to the index (0 mismatches), and modes are verified via index = HEAD. The repository has no gitlinks and no `.gitmodules`, so there were no submodule pins to check. Every build and probe ran in exports or temporary copies outside the clone.

## Pending manager duties

1. Run the donor full bank and the parent consumer bank at milan-fpga dev `ec0cc0c1df7d7ab3e25d973958f53f0074393d2c`, with the combined #132 + C1 parent adaptation applied, and post both.
   - Confirm the PR body's attribution: the five parent failures come from #132/#133 at a gitlink-only parent.
   - Confirm that the head adds only the `acmp_mutants.py` reader to `measure_test_evidence`.
2. At pin adoption, add the `DUT_READER_DISPOSITIONS` entries for `protocol-processor/tb/pp_top/acmp_mutants.py` and `…/d3_mutants.py`.
3. Build the final current-dev candidate at the merge turn from source base b2db3a97 against live dev ec0cc0c1.
4. Own hosted and act acceptance.
5. Decide whether to track S2 (F00.2 snapshot refresh) and S3 (bound-view hold across A8).

## Receipts (published set: see MANIFEST.sha256)

- `public/suite_*_v5050.log`, `public/suite_*_v5052.log`: the three changed suites under both tools.
- `public/acmp_mutants_v5050.stdout` and `public/acmp_mutants_v5050.results.json`: the author driver, 19/19.
- `public/r411_probes.stdout` and `public/r411_probes.results.json`, driven by `scripts/r411_probes.py`: reviewer probes, 11/11. Portable; run with `python3 scripts/r411_probes.py --root <export of the head> --output DIR --verilator <5.050> --jobs 8`.
- `public/gsi_mutants_v5050.stdout`, `public/name_wr_v5050.stdout`, and `public/d3_mutants_v5050_c0{0..5}.stdout` with their `.results.json`.
- `public/static_gates.log`, `public/check_upc_map.log`, `public/probe_trace_span.txt`, `public/tool_identity.txt`, `public/clone_integrity.txt`, `public/hosted_checks.txt`, `public/hosted_suites_pr_tallies.txt`.
- Paths in the published receipts are redacted to `$HOME`, `$PACKET`, `$PINNED_TOOL_BIN`, `$PINNED_ROOT` and `$CLONE`.

R411-1 FINISHED
