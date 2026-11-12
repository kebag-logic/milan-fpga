# HANDOFF — lane 897 (A776): the split's GET_AS_PATH from the datapath's path sequence

Status: **STOP** on one question (section 6), posted on #897 with the head: issuecomment-6828566150 (`STOP-COMMENT.md`). Everything else is done and gated. `PR-BODY.md` is ready for the manager.
**Head: `5e6fef3ee74dcf6766ac3923349ae83524bc0e7b`** (clean; nothing pushed).
Worktree: `$LANES/897-aspath`, branch `897-split-as-path`.
Base: `7f50ee6a90` (#810 round 29 tip). TAKEN: #897 issuecomment-6825437904 (`TAKEN-COMMENT.md`).

| Commit | Subject |
|---|---|
| `36ebd45f` | the face's `path()` through GSI kind 2, the platform stub removed, tests and plants, docs |
| `6de1475f` | the CPU budget harness's answering arms keep answering GET_AS_PATH through the face's port |
| `d7b977f0` | the coverage ratchet through `fw_coverage.py --write` (`aecp_face.c` 179/179, 160/160; `ctrl_plat.c` 129/129) |
| `5e6fef3e` | `SPLIT_CONTROL_MEMORY.md` section 5: the images' sizes with the change |

## 1. Reading (what the change rests on)

- IEEE 1722.1-2021 7.4.41 (read): command `descriptor_index` + reserved; response `descriptor_index`, `count` (number of ClockIdentities in `path_sequence`), `path_sequence` = pathSequence of the latest Announce PathTrace TLV; restriction 7.4.41.3 names NOT_AUTHENTICATED only. **No status is named for an entity that cannot read its path.** Table 7-141 (read): ENTITY_MISBEHAVING (10) "internal error while trying to process the command"; NO_RESOURCES (8); IN_PROGRESS (9) with 9.3.2.6's 120 ms cadence.
- Milan v1.2 5.4.2.24 (read): "shall implement GET_AS_PATH as specified in [ATDECC, Clause 7.4.41]". 5.4.5.2 Table 5.22 (read): GET_AS_PATH "Sent when the gPTP path sequence changes". 5.4.1: GET_AS_PATH may exceed cdl 524.
- Contract: `mbx_contract.h:704` GSI_SEL KIND 2 = GET_AS_PATH, SEL the word, ORD an array ordinal (8 bits); `:1062` AS_PATH_CHANGED (7).
- The processor's word table (protocol-processor `docs/architecture/06_aecp_engine.md` 6.10): kind 2 selector 0 `{48'0, count}` at @26, selector 8 `path_sequence[gsi_ord]` at @28 + 8k. Its gather watchdog voids a wedged face to ENTITY_MISBEHAVING (`KL_aecp_engine.sv` `gather_watchdog`, `gsi_hold_w`; doc 6.x "a wedged face voids to ENTITY_MISBEHAVING").
- **The split datapath serves kind 2** (no STOP): `hdl/milan/milan_datapath.sv` `g_sp_ctrl` routes `i_ctl_gsi_*` to the GSI answer block (`:10062-10070`), whose kind 2 answers selector 0 `{60'd0, asp_served_count_w}` and selector 8 `asp_served_entry_w` (`:6666-6670`), from a snapshot taken at the count's request edge (`asp_resp_capture_w`, `:6296-6298`, `:6336-6340`); `o_ctl_asp_chg_p = gsi_asp_chg_w` (`:10079`). At most 8 entries (`ASP_SLOTS_C` 7 + the head).
- AS_PATH_CHANGED already leads to the GET_AS_PATH notice: `ctrl_app_aecp.c:176-177` `ctrl_app_aecp_changed(c, 9u, e->interface, 4u)` (Table 5.22 bit 2; `aecp.c` scan builds command 40 through the path port). Item 2 needed no code, only tests on the face's real read.

## 2. Changes (file:line, reason)

| Commit | File:line | Change | Reason |
|---|---|---|---|
| `36ebd45f` | `sw/firmware/ctrl/aecp/aecp_face.c:248-269` | `path()`: GSI kind 2 selector 0 the count; a count past `capacity` fails the port; each entry at selector 8, ordinal k; any unanswered word fails the port; `_Static_assert(AECP_PATH_ITEMS <= 1 << MBX_GSI_SEL_ORD_WIDTH)` | item 1 (7.4.41.2; the processor's table) |
| `36ebd45f` | `sw/firmware/ctrl/aecp/aecp_face.h:29-35`, `:47`, `:59` | the `path` port documented; the platform supplies `random` only | item 1 |
| `36ebd45f` | `sw/firmware/ctrl/plat/ctrl_plat.c:117-124`, `:216` | the stub `path()` removed; `aecp_platform = {.random}` | item 1 (#897's cause) |
| `36ebd45f` | `sw/firmware/ctrl/test/ctrl_aecp_image.c:59-63` | the size fixture's `a_path` stub removed | the fixture links the face's read too |
| `36ebd45f` | `sw/firmware/ctrl/plat/README.md:81-84`, `:126`, `:120`, "Not yet done" | the AECP port item states the behaviour; "GET_AS_PATH answers unavailable" removed; 42 plants (was stated 40, 41 at the base) | item 3 |
| `36ebd45f` | `docs/design/MAILBOX_SPLIT.md:1373`, `:1400-1409`, `:1640` | `path` is the face's; GET_AS_PATH's reads; the host tests' row | docs |
| `36ebd45f` | `sw/firmware/ctrl/aecp/README.md:335` | the fixture's GET_AS_PATH through the GSI window | docs |
| `36ebd45f` | `sw/firmware/ctrl/test/test_aecp.cpp` | `Far` serves kind 2 and records each request; four tests (section 3) | item 4 |
| `36ebd45f` | `sw/firmware/ctrl/test/test_plat_boot.cpp` | B8's stub check removed; `Far` answers kind 2; `Boot.B11GetAsPathAnswersTheDatapathsSequence` | item 4 |
| `36ebd45f` | `sw/firmware/ctrl/test/aecp_mutants.py`, `plat_mutants.py` | nine AECP plants, one platform plant | item 4 |
| `d7b977f0` | `sw/firmware/gtest/coverage.ratchet:10`, `:26` | the measurement, through `fw_coverage.py --write` on a clean clone | the ratchet records the file's totals |
| `5e6fef3e` | `docs/design/SPLIT_CONTROL_MEMORY.md:282`, `:293` | the four points' sizes with the change, the notice arm's image | section 4 below |
| `6de1475f` | `tb/verilator/ctrl_service_budget/build.py:118-262`, `run.py:409-410`, `README.md:208-210` | `answering-ports` replaces the face's `path` with an empty sequence (`b_path`); `answering-every-port` defines `a_path` itself and puts it in the face's `path` port | the arms anchored on the removed stub; each keeps its behaviour |

## 3. New checks, planted mutants and failing words

| Test | Plant (campaign) | Planted defect | Failing words |
|---|---|---|---|
| `Face.AsPathIsTheDatapathsSequenceThroughItsOwnWindow` | `face-as-path-count-read-as-avb-info` (AECP) | count read at kind 1 | "the count, then each entry once" |
| same | `face-as-path-entries-at-one-ordinal` (AECP) | every entry at ordinal 0 | "at selector 8, by its ordinal" |
| same | `face-as-path-through-the-first-interface` (AECP, 2 interfaces) | the count read through interface 0 | "read through its own interface's window" |
| `Face.AsPathCarriesItsWholeBoundAndFailsACountPastIt` | `face-as-path-truncated-at-its-bound` (AECP) | a count past the bound clamped and carried | "a count past the bound fails the port" |
| same | `face-as-path-bound-off-by-one` (AECP) | `n >= capacity` | "AECP_PATH_ITEMS entries are carried" |
| `Face.AnUnansweredAsPathWordFailsItsPortThere` | `face-as-path-count-unanswered-ignored` (AECP) | the count's failure ignored | "the count unanswered fails the port" |
| same | `face-as-path-entry-unanswered-ignored` (AECP) | an entry's failure ignored | "an entry unanswered fails the port" |
| `AppFace.AnAsPathChangeNotifiesTheDatapathsSequence` | `face-as-path-change-notifies-avb-info` (AECP) | AS_PATH_CHANGED marks bit 1 | "an AS_PATH change notifies GET_AS_PATH" |
| same | `face-as-path-change-on-the-first-interface` (AECP, 2 interfaces) | the notice for AVB_INTERFACE 0 | "an AS_PATH change notifies GET_AS_PATH" |
| `Boot.B11GetAsPathAnswersTheDatapathsSequence` | `plat-as-path-unavailable` (control, platboot1 and platboot2) | the old stub's answer: the face's path fails | "B11 GET_AS_PATH answers SUCCESS" |

Iteration receipts (working tree): every new test PASS at 1 and 2 interfaces; 9 of 9 AECP plants caught, 1 of 1 platform plant caught; `aecp_mutants.controls()` and `ctrl_mutants.unnamed_tests()` clean. Final evidence comes from the clean-clone pass (section 5).

## 4. ROM ledger and the CPU budget harness

**ROM** (`receipts/rom/`): `ctrl_srp_image.py --with-aecp` and `ctrl_plat_image.py` at the four points, base `7f50ee6a` and head `6de1475f` (the final head's image: later commits change the ratchet and docs only), each on a clean clone, on #810 round 29's runtime archives and split SoC exports. Caps: the #895 ruling (issuecomment-6824623445) and the #665 owner decision (issuecomment-6824896581).

| Image, point | Base rom B | Head rom B | Delta | sram | RAMB36 | Cap | Verdict |
|---|---:|---:|---:|---|---:|---:|---|
| fixture 1x1/1if | 107,896 | 108,224 | +328 | unchanged | 38.0 | 56 | holds |
| fixture 1x1/2if | 109,600 | 109,928 | +328 | unchanged | 41.0 | 56 | holds |
| fixture 8x8/1if | 121,440 | 121,768 | +328 | unchanged | 51.5 | 56 | holds |
| fixture 8x8/2if | 123,112 | 123,440 | +328 | unchanged | 58.0 | 58.5 | holds (1,488 B before 124,928) |
| platform 1x1/1if | 112,968 | 113,280 | +312 | unchanged | 39.5 | 56 | holds |
| platform 1x1/2if | 114,696 | 115,008 | +312 | unchanged | 43.0 | 56 | holds |
| platform 8x8/1if | 126,560 | 126,872 | +312 | unchanged | 52.5 | 56 | holds |
| platform 8x8/2if | 128,264 | 128,576 | +312 | unchanged | 59.5 | 60.5 | holds the cap; the tree's own 59.0 entry refuses it at the base as at the head (pre-existing, #810's F-PLAT; the #895 ruling's 60.0 entry is #895's) |

The harness's `answering-every-port` 8x8/2if image: 123,420 B (round 29) to 123,756 B, 58.0 tiles, 1,172 B under 124,928.

**The CPU budget harness** (`receipts/harness/`). The load gate (`load_grade.py --check`, tables unchanged): 1x1/1if 0.486 at the pin and 0.483 with tsn-c-stack#32, ceiling 0.70: HELD, RESULT PASS. `run.py --self-test` at `6de1475f`: 0 failures (the variants' new anchors apply). A fresh build of each point and arm at `6de1475f`, sampled groups, compared with round 29's legs by the round's own cost tools (`tools-r26`: parts, eventcost, costs24):

| Build | Groups | Graded | Costs against the stated tables |
|---|---|---|---|
| A1 (1x1, arm A) | aecp, aecp-fanout, acmp-cmd | 3, 0 refusals, 0 budget misses, 0 share misses | every cost within its stated cost; record.aecp 17,129 cycles (205 us stated), event.AECP 3,141 (60 us), base 14,951 (155 us) |
| A8 (8x8, arm A) | the same | 3, 0, 0, 0 | within; record.aecp 22,973 (265 us) |
| B1, B8 (arm B, `answering-ports`) | aecp | 1, 0, 0, 0 each | within |
| N1 (1x1, `answering-every-port`) | notice-burst-0 | 1, 0, 0, 0; every notice committed within its 22 ms bound | within; item.aecp 18,824 (210 us), event.AECP 5,186 (60 us) |
| N8 (8x8, `answering-every-port`) | notice-burst-0 | 1, 0, 0, 0; every notice committed within its 62 ms bound | within; record.aecp 23,175 (265 us), event.AECP 8,455 (100 us), centisecond 33,967 (510 us) |

Differences against the recorded legs are layout effects of a few percent either way (the face's read runs only on GET_AS_PATH, which no arm A group stages, and both answering arms replace the port). **The full legs (every group at both points) were not run again**: no stated cost is exceeded by the samples, and the 1x1/1if load has 0.21 of headroom, so no table is restated and no STOP condition is near.

## 5. Gate table (the clean-clone pass, once, on the final head `5e6fef3e`)

Each workflow job a pull request to `dev-soft-core` triggers, run step by step on its own fresh clean clone by `run_wf.py` (#810 round 29's runner, its paths set to this lane; the steps from the workflows at the head, a step left out only with its reason in `not_run.json`), and the lane gates (`lane_gates.sh`, three parts, each on its own clean clone), dispatched one unit each on booked ranges or the session pool (`receipts/gates/dispatch.txt`). The full Verilator sweep is left out: no RTL change. Every clone's tree was clean after its gates.

| Gate | Command | Result | Receipt |
|---|---|---|---|
| every workflow step | `verify_wf.py <head> ... rtl-fast.yml docs.yml elaborate.yml rtl.yml` | **139 steps ran, 226 not run with a reason, 2 bad**: the same two, and the same counts, as #810's own pass at the base `7f50ee6a` | `receipts/gates/verify-table.md` |
| firmware self-test | `test_ctrl_firmware.py --require-rv32 --self-test` in four shards (firmware-unit 0/4, control 1/4, aecp 2/4, srp 3/4) | PASS in each | `gates/wf/rtl-fast__firmware-*__ci_step_9.log`, `__firmware-unit__ci_step_10.log` |
| AECP campaign | shard 2/4 | 236 of 236 caught, the nine new among them | `gates/wf/rtl-fast__firmware-aecp-mutants__ci_step_9.log` |
| control campaign (the platform's plants) | shard 1/4 | 697 of 697 caught, `plat-as-path-unavailable` among them | `gates/wf/rtl-fast__firmware-control-mutants__ci_step_9.log` |
| SRP campaign | shard 3/4 | 340 ok, 0 escaped | `gates/wf/rtl-fast__firmware-srp-mutants__ci_step_9.log` |
| coverage | `fw_coverage.py --check` (firmware-unit step 12, and lane part a) | PASS, 39 files; `aecp_face.c` 179/179 lines, 160/160 branches | `gates/lane/fw_coverage_check.log` |
| builder | `test_builder.py --require-rv32` (lane part b; and docs-gates-1/2's builder legs) | PASS | `gates/lane/test_builder.log` |
| docs | docs.yml's docs-gates-0/1/2, docs-check, docs-check-no-git, wire-accountability; `docs_check.py` | PASS but gate_38 (below) | `gates/wf/docs__*` |
| bdd-conformance | rtl-fast.yml `bdd-conformance`; lane `cd tests && behave` | PASS; 508 scenarios, 2,330 steps, 0 failed | `gates/lane/behave.log.excerpt.txt` |
| split boot simulation | `ctrl_split_boot/run.py` at 1x1, 8x8, native controls, `--self-test` | PASS each (0 findings) | `gates/lane/boot_*.log` |
| two-placement twin | `make -C tb/verilator/milan_dp twin` | 0 findings | `gates/lane/twin.log.excerpt.txt` |
| harness | `run.py --self-test`, `load_grade.py --selftest`/`--check`, `flip_grade.py --selftest` | PASS; load 1x1/1if 0.486 against 0.70 | `gates/lane/` |
| flip check | `flip_grade.py --check` (all, 1x1/1if, 8x8/2if) | exits 1, as at the base (no merge gate; #810's rows, red with #894) | `gates/lane/flip_check_*.log` |
| the rest of lane part a | py idiom, baremetal, ctrl_hot self-test and check, hooks and target self-tests, gen_mailbox check and self-test, lint_rtl, soc_options, ctrl_memory, nvm self-test, diff --check against the base | PASS but the two below | `gates/lane-summary.txt` |
| harness at the final head | `hsf.sh`: a fresh build of each point's arm A on its own clean clone at `5e6fef3e`, `acmp-cmd` run, compared with the `6de1475f` build | images byte-identical (objcopy and ELF), the sample's log identical, at both points | `harness/final-head-build-A1.log`, `-A8.log` |

**Red at the head, all four pre-existing at the base and fixed by #810's later round 29 commit `b2d39235` (not on this branch):**
- `check_cpp_idiom.py` (lane, and docs-gates-0 gate_38): `test_aecp.cpp:1428` `bool held=false, refuse_end=false;`, a multi-declarator line from #810 (`receipts/gates/base-7f50ee6a-cpp_idiom.log` reproduces it at the base).
- `ctrl_service_hooks/run.py --self-test`: 27 of 28, "the plants apply: an anchor occurs 0 times in acmp/acmp_mbx.c" (#810's H-ACMP plant anchor).
- firmware-boundary step 9: "`flip_grade.py` names the firmware's tree and is a program, and is neither a known builder...".
- (the flip checks' exit 1 is expected, above.)

**A runner fault, fixed and re-run:** docs-gates-1's builder leg (gate_25_0) first failed "--require-rv32: the provisioned absolute SDK selector must be adopted": my runner's `$HOME` lacked the SDK link the round's runner home has (`br-milan-rv32`). With the link added, the job ran again on a fresh clone and passed (`dispatch.txt`, `W-docs-gates-1b`); gate_25_1 (docs-gates-2) passed.

## 6. Open question (STOP)

IEEE 1722.1-2021 7.4.41 names no status for a GET_AS_PATH whose datapath window does not answer (a datapath in reset, or wedged), and #897's acceptance 3 forbids ENTITY_MISBEHAVING "for a read of a valid AVB_INTERFACE". The core answers such a port failure ENTITY_MISBEHAVING (`aecp_commands.c:476-477`, pinned by `Core.ObservationRefusals`), as it does GET_AVB_INFO's, GET_STREAM_INFO's and GET_COUNTERS'; the all-fabric processor's gather watchdog does the same for a wedged GSI face. The same decision covers `aecp_commands.c:467-468` (an AVB_INTERFACE descriptor past the build's interfaces), which no shipped image reaches. With an answering datapath every valid AVB_INTERFACE answers SUCCESS (the tests above). This lane changes no status.

Options stated on #897: (a) keep ENTITY_MISBEHAVING for an unanswering datapath and read acceptance 3 as "with an answering datapath" (recommended: Table 7-141's meaning, the all-fabric image's behaviour); (b) IN_PROGRESS with a retried read, which still needs (a) or (c) at the end; (c) another status, which no clause supports.

**After the ruling.** (a): no code change; the gate pass at `5e6fef3e` stands; post REVIEW READY. Otherwise: change the core's status for the path port's failure (`aecp_commands.c:476-477`), `Core.ObservationRefusals`' expected status, a plant naming it in `aecp_mutants.py`, the plat README's sentence "the core answers as for GET_AVB_INFO's" and `MAILBOX_SPLIT.md:1395-1396`; then the AECP campaign, `fw_coverage.py --check`, the harness self-test and the clean-clone pass again.

## 7. Notes for the next session

- Scratch (`/data-2/milan/tmp/897-a776`, 7.5 GB): `cl-head`, `cl-base` (clean clones), `hb/` (the harness builds A1, A8, N1, N8, B1, B8 at `6de1475f` and A1-final, A8-final at `5e6fef3e`), `gates-out/` (the pass's logs), `gates-wt/` (the pass's lane and boot clones), `gates/` (the runner, its venv and home). `scripts/`: `unit.sh`, `clone.sh`, `images.sh`, `hs.sh`, `hsf.sh`, `sample_costs.sh`, `compare_groups.py`, `gate_queue.sh`, `dispatch.py`, `lane_gates.sh`, `receipts.py`. No unit of this lane is left running.
- The runner's `$HOME` needs the `br-milan-rv32` link for the builder legs (section 5).
- Live `dev-soft-core` was not merged; the candidate merge is the manager's.
- Nothing pushed, no PR opened, no board touched.
