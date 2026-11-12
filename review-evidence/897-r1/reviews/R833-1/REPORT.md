[R833] POSITIVE - exact head 5e6fef3ee74dcf6766ac3923349ae83524bc0e7b

# R833-1: internal cleared-context review of PR #898 for issue #897

- Head `5e6fef3ee74dcf6766ac3923349ae83524bc0e7b`, tree `3f0b90490650e0bc4b51f2f55ecb10c20dab5a06`. The delta is `7f50ee6a..5e6fef3e`: four commits, 16 files, +346/-54. No file is added, deleted or renamed, and no mode changes.
- Base `7f50ee6a` is #810's round 29 tip. The PR is stacked on `665-s2b-cycles`.
- Role: internal reviewer, independent of the executor. I made no source edits, commits, pushes or GitHub writes.
- Scope I reconstructed from public sources:
  - AGENTS.md and CONTRIBUTING.md.
  - The #897 body, with acceptance 1-4 as amended (acceptance 3 now reads "with an answering datapath").
  - The ruling issuecomment-6828659285, option (a): a datapath window that does not answer keeps ENTITY_MISBEHAVING. Acceptance 5 is a bench item and out of scope.
  - The STOP issuecomment-6828566150 and the PR body.
  - IEEE 1722.1-2021 7.4.41 and Table 7-141; Milan v1.2 5.4.2.24 and Table 5.22.
  - The all-fabric processor's GET_AS_PATH gather as the reference.
- The verdict and ledger were drafted before I read any other review on this PR.
- There were no prior review findings to resolve: the PR thread holds only the two review-start notices.

## Verdict basis

I found no BLOCKER, MAJOR or MINOR finding at this head. All five lenses are covered clean. There is one SUGGESTION, and I recorded one observation about base text outside the delta.

## Checks against code and receipts

### 1. The face's `path()` reads GSI kind 2 as the datapath serves it

**The face read** (`sw/firmware/ctrl/aecp/aecp_face.c:248-268`):
- The count is read at kind 2, selector 0, ordinal 0.
- Each entry is then read at kind 2, selector 8, ordinal `k` for `k < n`, through the caller's `interface` window, with type AVB_INTERFACE and the command's index.
- `n > capacity` fails the port before any entry is read.
- A window with no answer (`mbx_win_read` != OK) fails the port at that word and counts it unanswered.
- `*count` is written only on success.
- `_Static_assert(AECP_PATH_ITEMS <= 1u << MBX_GSI_SEL_ORD_WIDTH)` at line 253 holds: 64 <= 256 (`mbx_contract.h:705-717`, ORD is 8 bits at LSB 8).

**What the datapath serves** (`hdl/milan/milan_datapath.sv`, unchanged by the delta):
- The split wiring is `pp_gsi_req_w = i_ctl_gsi_req` (g_sp_ctrl, line 10062).
- The snapshot is taken at the rising edge of a kind-2, selector-0 request (`asp_resp_capture_w`, 6297-6299; capture at 6339-6343).
- Entry `ord` comes from that snapshot: the head at 0, the tail slots at 1-7, and 0 past the count (6570-6581).
- The kind-2 answer is `{60'd0, count}` at selector 0 and the entry at selector 8 (6666-6670).

**Each count read gets a new snapshot.** The CDC requester drops `d_req_o` through `PRE_S` before every request (`hdl/milan/mailbox/KL_mbx_cdc_window.sv:84, 98-101`), so every count read raises a fresh edge. A GET_AS_PATH response therefore carries one consistent sequence, and the next command takes a new snapshot.

**Byte order and layout.** The core writes the count big-endian at payload +2 and each entry with `aecp_put64` at +4+8k (`aecp_commands.c:470-483`). That matches the processor's word table: count @26 and entries @28+8k of the AVTPDU (`protocol-processor/docs/architecture/06_aecp_engine.md:1006-1007`). `KL_aecp_engine.sv:3502-3507` handles GET_AS_PATH the same way.

**Executed checks:**
- `Face.AsPathIsTheDatapathsSequenceThroughItsOwnWindow` (`test_aecp.cpp:3088`) asserts the exact GSI_REQ and GSI_SEL words, the ordinals and the interface.
- My own plants were all caught: entry selector 9, count selector 1, entries written to slot 0, ordinal k+1, last entry skipped, count descriptor type 5, entry index 0, and `*count` not reported. The receipts are `receipts/probe_results.json` and `receipts/probe_logs/r-*.log`.

**Edge cases:**
- A count past the bound fails the port (`Face.AsPathCarriesItsWholeBoundAndFailsACountPastIt`, 3118). That test tries AECP_PATH_ITEMS+1 and 2^32. Masking the count to 16 bits is caught (`r-count-low-16-bits`).
- A word with no answer is covered at the count and at every entry (`Face.AnUnansweredAsPathWordFailsItsPortThere`, 3153).

### 2. The response payload and the unsolicited response

- The payload has descriptor_index, count and path_sequence in 7.4.41.2's order, with control_data_length 16 + 8 per entry. This is asserted at 0, 1, 3 and 8 entries on both interfaces, with SUCCESS checked by the fixture's `receive()` (`test_aecp.cpp:2898-2905`).
- AS_PATH_CHANGED marks event bit 2 for the changed interface (`ctrl_app_aecp.c:176-177`).
- `AppFace.AnAsPathChangeNotifiesTheDatapathsSequence` (`test_aecp.cpp:3665`) checks that the notice to the registered controller is a SUCCESS AEM_RESPONSE. It carries the datapath's count and entries, read through the changed interface's window, at 2, 3 and 0 entries on each interface.
- At the composed platform level, `Boot.B11GetAsPathAnswersTheDatapathsSequence` (`test_plat_boot.cpp:415`) passes at one and two interfaces.

### 3. No ENTITY_MISBEHAVING for a valid AVB_INTERFACE with an answering datapath

In `aecp_commands.c:453-483`, a valid AVB_INTERFACE (one `aecp_find` returns, with index < cfg.interfaces) answers ENTITY_MISBEHAVING only when the path port fails. With an answering window the port fails only when `n > capacity`. The RTL count is 4 bits (at most 15, and at most 8 slots in practice) against a capacity of 64, so that branch cannot occur.

The remaining ENTITY_MISBEHAVING paths are the two the ruling covers:
- an unanswered window;
- index >= cfg.interfaces, which no shipped image reaches.

A busy window at entry (`mbx.c:386-388`) belongs to the non-answering case.

### 4. Each new test fails for its planted defect, and `aecp_face.c` coverage

- All nine author AECP plants were caught by name under the repository's own `aecp_mutants.caught` rule, in the app arm at two interfaces.
- `plat-as-path-unavailable` was caught by name in both `platboot1` and `platboot2` (`ctrl_mutants.caught`).
- The clean arms pass: app at if1 and if2, platboot at 1 and 2 (`receipts/probe_as_path.log`).
- The table sizes match the stated campaign totals: AECP 227 to 236 (+9), control 696 to 697 (+1), platform table 41 to 42. The plat README's "42 defects" is now true; the base's "40" was stale.
- `fw_coverage.py --check` passes (rc 0). `aecp_face.c` is at 179/179 lines and 160/160 branches. `ctrl_plat.c` is at 129 lines and 42 branches, the ratchet's values (`receipts/fw_coverage_check.log`).

### 5. ROM and load claims

I checked the author's size receipts (`review-evidence/897-r1/author/receipts/rom`, archive `299a7500`; `head-HEAD.txt` reads 6de1475f, dirty 0):
- Every fixture point grows by +328 B of rom and every platform point by +312 B.
- sram is unchanged at every point, and so are the tiles: fixture 38.0/41.0/51.5/58.0, platform 39.5/43.0/52.5/59.5.
- The platform's 8x8/2if image needs 128,576 B in 129,024, so it plans 59.5 tiles. That is under the 60.5 cap and refused by the 59.0 entry, exactly as at the base (128,264 B).
- The `ctrl_plat` members are unchanged; only `.text` grows by 312 B.
- Every other point is at most 52.5 tiles, within 56.
- The commits after 6de1475f touch only `coverage.ratchet` and one doc, so the firmware bytes are the same. The final-head harness builds report the ELF objcopy identical to the sampled build.
- The figures in `SPLIT_CONTROL_MEMORY.md:282,293` match these receipts: margin 1,488 B, 1,600 B past 126,976, and the arm at 123,756 B, 1,172 B under 124,928.
- `load_grade.py --check` at the head passes: 1x1/1if holds 0.486 against 0.70 (`receipts/load_grade_check_head.log`). That figure comes from the stated tables, which the delta does not change.

### 6. The three red gates are the base's

- **C/C++ idiom gate:** at base and head, the same single finding, "multi-declarator declaration 1 > ratchet 0" in `test_aecp.cpp`. The `--list` outputs are identical (`receipts/cpp_idiom_list_base_vs_head.diff` is empty).
- **Hooks self-test:** at base and head, the same "27 of 28 checks pass; 96 of 96 mutants caught". The failing check is an anchor in `acmp/acmp_mbx.c`, and the logs are identical (`receipts/hooks_selftest_base_vs_head.diff` is empty).
- **Firmware boundary:** the author's log refuses `tb/verilator/ctrl_service_budget/flip_grade.py` as unclassified. Neither that file nor the classification tables (`ctrl_configs.py`, `ctrl_boundary.py`) are in the delta, and the delta adds no file. I did not rerun this gate (its builders take about 15 minutes).
- **Informational check:** the head merges cleanly onto the base branch's live tip `b2d39235`, of which `7f50ee6a` is an ancestor. On that composed tree (58f06f5c) the idiom gate and the hooks self-test are green: 0 findings, and 28/28 checks. This is not a manager bank and not merge-candidate validation.

## Findings

**S1 - SUGGESTION - Tests, Robustness - `tb/verilator/ctrl_service_budget/build.py:142,193`**
- Evidence: the answering arms' GET_AS_PATH stand-ins (`b_path`, `a_path`) answer an empty sequence and read no window, as the base's stand-ins did. So no harness group times a GET_AS_PATH response or notice that carries entries and costs 1+n window reads. The PR's "Known limitations" says so.
- Impact: negligible by inspection. Each entry adds one bounded GSI read (64 polls, `mbx_contract.h:833`) and 8 frame bytes, at most 8 entries from the datapath. A refused attempt fails at the first word, inside the round's 34 µs charge (`aecp.h:60`). `AECP_ROUND_PORTS` already counts the path port as a window read (`aecp.h:61-64`).
- Optional outcome: a sampled notice or aecp group with an n=8 stand-in, if the margin is ever tight.

**O1 - observation, outside the delta, no lens effect - `sw/firmware/ctrl/plat/README.md:139`**
- "Not yet done" still says the 8x8/2if image "plans 58.5 RAMB36, within the 59.0 ledgered". The base's own receipts and `SPLIT_CONTROL_MEMORY.md:281` say it plans 59.5 and is refused.
- The text is unchanged since the base, so it is not a finding against this delta. The manager may route it to the #665 or #746 residue.

**Comment rule.** I scanned the added lines of the source comments and strings. They cite only issue IDs and IEEE/Milan clauses. "B11" (`test_plat_boot.cpp:35-37,415`) continues that file's own boot-rule list B1-B10 (header, lines 13-34); it is not a bench lane label. Nothing else needs flagging.

## Per-lens results

- [R833] PASS Conformance — `aecp_face.c:248-268`; `aecp_commands.c:453-483`; `ctrl_app_aecp.c:176-177`; test_aecp.cpp:3088/3118/3153/3665; test_plat_boot.cpp:415. Checked against 7.4.41.1-2 (layout, cdl 16+8n), Table 7-141 under the ruling, Milan 5.4.2.24 and Table 5.22, and the processor's 06_aecp_engine.md:1006-1007 word table. Acceptance 1-4 are met, with acceptance 3 as amended. Acceptance 5 is out of scope.
- [R833] PASS RTL — `milan_datapath.sv:6286-6343, 6570-6581, 6666-6670, 10062`; `KL_mbx_cdc_window.sv:84-110`; `KL_mbx.sv:636-653, 714`; `mbx.c:380-405`. There is no RTL change in the delta. I checked that the firmware's read sequence matches the served snapshot: count-edge capture through PRE_S, ordinal decode, `{60'd0,count}`, the 4-bit count against the 64-entry capacity, and the 64-cycle window bound. The `_Static_assert` covers the ordinal width.
- [R833] PASS Robustness — `aecp_face.c:256-267`. Covered: a count past the bound and past the caller's capacity; high count bits (2^32); no answer at the count and at each entry; no count reported on failure; a busy window; the own interface at two interfaces; re-snapshot on each command. A datapath that does not answer keeps ENTITY_MISBEHAVING under the ruling, and its notice is retried through the existing round.
- [R833] PASS Tests — `receipts/probe_results.json`. Ten of ten author plants were caught by name; nine of nine reviewer plants were caught; the clean arms pass at if1 and if2 and at platboot 1 and 2. `fw_coverage.py --check` passes with `aecp_face.c` at 179/179 and 160/160. The three base reds match at base and head.
- [R833] PASS Docs — `MAILBOX_SPLIT.md:1304,1400-1406,1640`; `SPLIT_CONTROL_MEMORY.md:282,293`; `plat/README.md:81-84,122,126`; `aecp/README.md:335`; `aecp_face.h:26-35`; `ctrl_service_budget/README.md:210`; the PR body. Checked against the code, the size receipts and the plant tables: the ROM numbers, the plant counts and the port ownership agree. `docs_check.py` reports 0 findings at the head.

## Ledger (reviewer-owned)

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | aecp_face.c path(); aecp_commands.c avb(path); ctrl_app_aecp.c AS_PATH_CHANGED; the 5 new tests; 7.4.41, Table 7-141 (ruling), Milan 5.4.2.24 and Table 5.22; processor 6.10 word table and KL_aecp_engine GASP | R833-1 | 5e6fef3ee74dcf6766ac3923349ae83524bc0e7b |
| RTL | CLEAN | milan_datapath.sv GSI kind 2 snapshot, answer and g_sp_ctrl wiring; KL_mbx_cdc_window.sv requester; KL_mbx.sv GSI busy/timeout; mbx.c mbx_win_read (no RTL in delta) | R833-1 | 5e6fef3ee74dcf6766ac3923349ae83524bc0e7b |
| Robustness | CLEAN | aecp_face.c bound, unanswered and partial-failure paths; two-interface window; notice retry and round model (aecp.h AECP_ROUND_PORTS, AECP_ATTEMPT_US); the 9 reviewer plants | R833-1 | 5e6fef3ee74dcf6766ac3923349ae83524bc0e7b |
| Tests | CLEAN | test_aecp.cpp Face/AppFace tests; test_plat_boot.cpp B11; aecp_mutants.py:661-695; plat_mutants.py:194-197; coverage.ratchet; probe receipts; fw_coverage --check | R833-1 | 5e6fef3ee74dcf6766ac3923349ae83524bc0e7b |
| Docs | CLEAN | MAILBOX_SPLIT.md; SPLIT_CONTROL_MEMORY.md section 5; plat and aecp READMEs; aecp_face.h; harness README, build.py and run.py text; PR body; docs_check | R833-1 | 5e6fef3ee74dcf6766ac3923349ae83524bc0e7b |

## Evidence I executed (receipts in this packet)

- `scripts/probe_as_path.py` produced `receipts/probe_as_path.log`, `receipts/probe_results.json` and `receipts/probe_logs/`. All planted copies lived in disposable scratch; the checkout was never written.
- `fw_coverage.py --check --jobs 8` produced `receipts/fw_coverage_check.log` (rc 0).
- At base and head: the C/C++ idiom gate (`receipts/idiom_base_vs_head.log`, `cpp_idiom_list_base_vs_head.diff`) and the hooks self-test (`hooks_selftest_{base,headcopy}.log`, `.rc`, `hooks_selftest_base_vs_head.diff`).
- At head: `load_grade.py --check` (`load_grade_check_head.log`, rc 0) and `docs_check.py` (`docs_check_head.log`, 0 findings).
- Composition (informational): `composition.txt`, `composed_cpp_idiom.log` (rc 0) and `composed_hooks_selftest.log` (rc 0).
- Hosted checks at the exact head: `hosted_checks_snapshot.txt`, a point-in-time read. Many jobs were queued or in progress. Physical gPTP was skipped, not executed. Hosted pull_request jobs build the merge with the live base `b2d39235`, so a hosted green docs-gates-0 is not exact-head evidence for the idiom gate.
- Clone integrity after the probes: `clone_integrity.txt`. HEAD, the index tree and the worktree equal `3f0b9049`, there are 0 status lines, the six gitlinks are at their pins, and every submodule worktree is clean.

## Real limits

- I did not run an RTL simulation. The datapath's kind-2 serving is checked statically, and the RTL is unchanged by the delta.
- Acceptance 1's "same sequence as the all-fabric image" rests on both images reading the same datapath answer block. I did not execute a differential run.
- Acceptance 5 (bench) is not run. Physical calibration was NOT RUN. Field skips are not hardware proof.
- I did not rerun the firmware boundary gate, the full firmware self-test shards, the CPU-budget harness legs or the ROM links. For those I rely on the author's receipts (`299a7500`), which I checked arithmetically and for consistency.
- At the boot level, B11's two-interface arm queries only AVB_INTERFACE 0, because the shipping model holds one. Interface 1's own window is covered at unit level (Face and AppFace, rekeyed).
- No manager source bank exists at this head, and I claim or infer none.

## Pending manager duties

- Validate the current-dev merge candidate at the merge turn (live dev `fa6c094b8e196666a8a8865788d5e83b5bbaea09`, after #810). The three base reds (idiom ratchet, hooks self-test, firmware boundary) must be green at the composed head. The boundary gate was not checked on any composed tree here.
- Own hosted and act acceptance on the exact head and the candidate.
- The external review (R834) and the second positive review.
- Optionally route O1 to the residue tracking.

R833-1 FINISHED
