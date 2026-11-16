# HANDOFF — [A789] lane 923 (#923 + #924), round 1

Status: **STOPPED** at `def26a61` (local, not pushed), posted once on #923 as issuecomment-6906644789 (STOP-COMMENT.md): the
target platform's 8x8/1if image plans 56.5 RAMB36 (rom 130,184 -> 132,352 B, 888 B spare at the base), past the 56 the
product build holds every image to and no ledger entry lets a product image exceed (the owner's flip criterion of
2026-11-12). The change's code cannot be compacted back inside #923's scope. Recommendation (A) in the STOP: ledger it at 56.5 as
S14 debt, the product build planning an image at its own ledgered point. Nothing more is owed on #923 this round.
Started 2026-11-16 02:32, stopped 05:1x.

- Worktree: /data-2/milan/lanes/923-aecp-maps, branch `923-aecp-maps`, base `16ba667d` (#901's review head).
- Scratch: /data-2/milan/tmp/923-a789
- Posted: TAKEN on #923, issuecomment-6904937191 (TAKEN-COMMENT.md); STOP issuecomment-6906644789 (STOP-COMMENT.md).

## 1. Step-1 report (before any change, at `16ba667d`)

**The EDIT window protocol** (contract 2.3, `docs/reference/MAILBOX_CONTRACT.md` "Face windows"; `mbx_contract.h:606-693`;
`KL_mbx_cdc_window.sv`; the datapath's transaction server `milan_datapath.sv:4549-4845` validate, `:5083-5245` commit).
- Registers per interface block: EDIT_REQ (type, index), EDIT_BEAT (PHASE[2:0], REMOVE[4], REC[15:8], COUNT[31:16]),
  EDIT_RECORD_HI:LO (the record's two wire quadlets: {stream_index, stream_channel}:{cluster_offset, cluster_channel}),
  EDIT_VALUE (unread by the datapath for an edit), GO = EDIT_CMD, STATUS {BUSY, DONE, TIMEOUT, TAG}, DATA_HI:LO
  (bit 0 the verdict). Answered or timed out within 64 `clk_i` cycles (MBX_WIN_EDIT_WAIT_CYCLES). The firmware's
  generic access is `mbx_win_read` (`mbx.c:392`): busy check, every request word, GO, STATUS polled up to
  wait_cycles + 1 times, then DATA_HI and DATA_LO.
- The crossing: KL_mbx opens the request under a new tag; `KL_mbx_cdc_window` carries it in by `cdc_handshake`, waits
  while the datapath's `wait` is high (PRE_S), raises `req` for the beat (REQ_S), takes the answer in the first cycle
  wait is low, carries it back with its tag (a late answer's old tag is discarded; a newer request wins).
- The phases, the release processor's walk (`gen_ucode.py` E_AMADD, `KL_aecp_engine.sv:2317-2344`): 0 begin
  validation (bit 0: the port is dynamic; else NOT_SUPPORTED), 4 validate record REC (bit 0 accepted: it claims the
  record's key; else BAD_ARGUMENTS), 1 begin commit (bit 0: the recheck passed and the commit is reserved, the point of
  no return; else BAD_ARGUMENTS), 5 commit record REC (writes the claimed word into `amap_in_store_r` / the output
  owner registers and the crossbar RAM), 2 finish (bit 0 a mapping changed), 3 abort. Every refusal aborts. A
  duplicate record is idempotent (a key's claim is taken once). The datapath's `wait` is `amap_boot_busy_w`: high only
  from reset until the restore's terminal reaches it (F_RESTORE.DONE or CLOSED, `:5037`) and the one boot sweep after
  it (`AMAP_BOOT_KEYS_C` + 1 datapath cycles), so after boot no beat waits. During the boot window the store is held at
  the reset image clipped to the published formats (`:5238-5243`). The split builds no map restore of its own
  (`g_af_amr`, `:5640-5646`: "the firmware's AECP owner holds the maps ... and applies them through the EDIT window").
- No firmware writes the window today: `MBX_WIN_EDIT` appears only in `mbx.c:381` (the table) and `mbx.h:74`.

**Cost per edit, in CPU cycles** (to be measured; the derivation): a beat is the request words it writes, GO, STATUS
reads until answered, and DATA_HI and DATA_LO; a mailbox access costs 9 CPU cycles in the budget harness's test SoC
(README "Per access", 9 / 9 read / write; a register read one or two mailbox clocks more since #870). At the contract's
slowest datapath, answered at wait_cycles - 1 = 63 cycles, a record beat (BEAT, RECORD_LO, RECORD_HI, GO, ~4-7 STATUS
reads, two DATA reads) is about 160-180 CPU cycles before the firmware's own instructions; on the shipping datapath the
crossing answers in about 12-14 mailbox cycles, about 100. An edit of k mappings that change the store is 3 + 2k
beats (begin, k validations, commit-begin, k commits, finish): one mapping about 0.8-0.9 k cycles at the slowest
(8-9 us at 100 MHz). The release processor's walk was in hardware.

**Callers that must commit** (every writer of `aecp_map.rows`/`count`):
- ADD_AUDIO_MAPPINGS / REMOVE_AUDIO_MAPPINGS: `aecp_map_command` (`aecp_maps.c:354`), from `aecp_command` case 44/45
  (`aecp_commands.c:693`). Not reachable through GET_DYNAMIC_INFO (`dynamic_member` lists GETs only).
- The boot restore: `aecp_nvm.c` `apply` -> `aecp_map_restore` (`aecp_maps.c:506`), `settle` ->
  `aecp_restore_settle` (`:528`, the #658 clip), `rollback` -> `aecp_restore_defaults` (`aecp_state.c:68`). These run
  in the saved-state walk, before AECP opens, while the datapath's edit face still waits for the restore's terminal,
  so the commit belongs after `aecp_face_open`'s acknowledged commit (which carries F_RESTORE.DONE and the formats) and
  before `aecp_mbx_open`, in `ctrl_app_open_aecp` (`ctrl_app_aecp.c:246`).
- `aecp_init` (`aecp.c:252-261`) loads the defaults, which is the datapath's reset image: no commit.
- SET_CONFIGURATION: reloads no map. Maps are per configuration (`aecp_map.configuration`) and every shipped model has
  one configuration (`aecp.h:75`), so an accepted SET_CONFIGURATION never moves the index. Not a committer.
- SET_STREAM_FORMAT never clips a map at run time: it is refused while a mapping would not survive
  (`aecp_maps_allow_format`, and the datapath's verdict through the GSI window).

**#924:** `aecp_commands.c:192-193` answers BAD_ARGUMENTS for an index at or past configurations_count; the processor
answers NO_SUCH_DESCRIPTOR with the current index (`gen_ucode.py` E_SCFGNSD, processor issue #179), its checks in the
same order (running, lock, range). `aecp_commands.c:361-364` refuses a SET body under 84 bytes; processor PR #183
accepts exactly 48 (cdl 60) and 84 (cdl 96), answers both in the 84-byte 2021 form, and refuses every other length.
The SET reads only `flags` (@4) and `msrp_accumulated_latency` (@24), inside the 48 bytes.

## 2. Changes (file:line, reason)

Commits on `16ba667d`: `10264ac2` (firmware, unit tests, plants, harness SoC answer), `def26a61` (co-simulation
check, docs).

| Where | What, and why |
|---|---|
| `sw/firmware/ctrl/aecp/aecp.h:203-210` | new optional port `edit` (the integrator's map store), NULL where none: #923's commit path, so every fixture without a store keeps its behaviour |
| `sw/firmware/ctrl/aecp/aecp.h:397-404` | `aecp_restore_commit` declared and specified |
| `sw/firmware/ctrl/aecp/aecp_maps.c:490-517` | after every check passes: the changing mappings (an ADD's additions, a REMOVE's distinct mappings), compacted into `e.rep`; the store's edit before the map moves; its refusal is the answer and changes nothing (all or none, Milan v1.2 5.4.2.27/.28); the ADD loop adds from the same list |
| `sw/firmware/ctrl/aecp/aecp_maps.c:585-660` | `kept`, `unmoved`, `reset`, `commit`, `aecp_restore_commit`: the boot commit (reset set removed for every moved port, then the restored sets added; refusal fallbacks keep what the store holds) |
| `sw/firmware/ctrl/aecp/aecp_face.c:248-325` | the face's `edit`: the release processor's walk on interface 0's EDIT window (begin, validate each, commit-begin, commit each, finish; abort on refusal or no answer before the reservation), begin asked once more for the boot sweep |
| `sw/firmware/ctrl/aecp/aecp_face.h` | the port documented |
| `sw/firmware/ctrl/aecp/aecp_mbx.c:130-148`, `sw/firmware/ctrl/app/ctrl_app_aecp.c:126-131,235` | the port forwarded through both composition layers, NULL where the environment has none |
| `sw/firmware/ctrl/app/ctrl_app_aecp.c:261-262` | `aecp_restore_commit` after the acknowledged open, before AECP opens |
| `sw/firmware/ctrl/mbx/mbx.c:392-405`, `mbx.h:161-166` | `mbx_win_ask`: a window request writing only some request words (EDIT_REQ once a transaction); `mbx_win_read` is it over every word |
| `sw/firmware/ctrl/aecp/aecp_commands.c:192-194` | #924: an index past configurations_count answers NO_SUCH_DESCRIPTOR (IEEE 1722.1-2021 7.4.7.1) |
| `sw/firmware/ctrl/aecp/aecp_commands.c:363-366` | #924: SET_STREAM_INFO takes the 48-octet 2013 body, answered in the 84-octet form; 49..83 still refused, past 84 unchanged |
| `tb/verilator/ctrl_service_budget/split_soc.py` | the harness SoC answers EDIT at the contract's bound with verdict 1 (`slowest_edit`), so the edit path is measured at its longest wait |
| `tb/verilator/milan_dp/twin_split.cpp`, `twin_probes.vlt`, `Makefile` | the co-simulation check `twin-maps` and its plant `twin-maps-plants` |
| docs | `sw/firmware/ctrl/aecp/README.md`, `docs/design/MAILBOX_SPLIT.md` (the open item closed), the harness README, the milan_dp README |

## 3. New checks, planted mutants, failing words

Unit tests (`test_aecp.cpp`), each owned by a plant (aecp campaign table: `aecp_map_mutants.py`, `aecp_mutants.py`,
`aecp_configuration_mutants.py`); 29 new plants, every one caught on its words (receipts `plants/`):

| Test | Plants (failing words) |
|---|---|
| Core.AnAcceptedEditReachesTheStoreBeforeTheMap | edit-store-skipped ("one store edit for the command"), edit-every-record, edit-held-mappings-added ("an ADD's additions alone, each once, in command order"), edit-repeats-sent ("a REMOVE's every distinct mapping, each once, in command order") |
| Core.AStoreRefusalIsTheAnswerAndChangesNothing | edit-refusal-ignored ("the store's refusal is the command's status") |
| Core.ARefusedEditNeverReachesTheStore | edit-before-the-checks ("a command the core refuses never reaches the store") |
| Core.RestoredMapsReachTheStoreRemovalsFirst | restore-adds-beside-its-removal ("two removals and two additions"), restore-removes-what-it-adds ("the input port's reset set removed") |
| Core.TheStoresResetSetIsTheClippedOne | restore-reset-set-unclipped ("a map that is the clipped reset set has not moved") |
| Core.ARefusedRestoreKeepsWhatTheStoreHolds | restore-removal-refusal-ignored ("a refused removal keeps the reset set the store holds"), restore-not-put-back, restore-put-back-trusted ("a refused put-back leaves the store's empty port empty") |
| Core.TheRestoreCommitsOnlyAClosedCoresMapsInForce | restore-commits-an-open-core ("an open core commits no restored map"), restore-past-a-page ("a port past a page reaches no store"), restore-every-configuration ("a map of another configuration is not committed") |
| AppStore.TheRestoredMapsReachTheStoreBeforeAecpOpens | restore-not-committed-at-open ("AECP's open commits the restored maps") |
| Face.AnEditIsTheReleasesTransactionOnTheEditWindow | window-record-halves-swapped ("the record as its two wire quadlets"), window-port-every-beat, window-request-words-from-the-first ("EDIT_REQ written once a transaction"), edit-store-skipped |
| Face.ARefusedBeatAbortsAndNothingMoves | window-never-aborts, window-validation-trusted ("a refused record aborts"), window-commit-begin-trusted ("a refused commit-begin aborts"), window-begin-trusted ("a refused begin aborts"), edit-refusal-ignored ("the map keeps its mappings") |
| Face.AnUnansweredEditFailsUntilItsCommitIsReserved | window-begin-asked-once ("a begin the boot sweep holds is asked once more"), window-reserved-commit-refuses ("after the reserved commit, the edit stands"), window-silence-uncounted ("each unanswered beat is counted") |
| Face.RestoredMapsReachTheStoreThroughTheEditWindow | restore-removes-what-it-adds ("the reset set removed first") |
| Core.SetConfigurationOutOfRangeIsNoSuchDescriptor | configuration-past-the-count-bad-arguments ("an index past configurations_count names no CONFIGURATION descriptor") |
| Core.SetStreamInfoTakesTheEarlierBodyOf48Octets | stream-info-earlier-body-refused ("the 48-octet body is taken"), stream-info-short-bodies-taken ("a body between 48 and 84 octets, or short of 48, is refused") |

Co-simulation (`make -C tb/verilator/milan_dp twin-maps`, the platform firmware on `tb_split_top`): 21 checks PASS
(boot map, BAD_ARGUMENTS with the mappings, the removal on the render store, 1/2/4/6 channels SUCCESS, 7 refused,
an edited map on the store, the saved map restored at the next boot on the store; GET_AUDIO_MAP agreeing after
each). `twin-maps-plants`: `--plant no-edit` (the core's edit port cut, #923's defect) fails MAPS-STORE, MAPS-FORMAT
(4 channels) and MAPS-EDIT on their words.

## 4. Gate table (round 1, at `def26a61`; partial: the STOP came first)

| Gate | Result | Receipt |
|---|---|---|
| AECP arms, app at 1 and 2 interfaces (`aecp_arms.py --app`) | 161 tests PASS each | scratch `arms/` |
| AECP core arm 1if | 95 tests PASS | scratch `arms/core1` |
| The 29 new plants (and 4 re-run restore plants), subset campaign over `aecp_mutants.DEFECTS` with the whole table's controls | 33 of 33 caught | `receipts/plants/new-plants.json` |
| every plant table's sites on the changed files (aecp 328, ctrl 384, acmp review 42, mbx dma 15, ctrl plants 47) | one site each | (this handoff) |
| `twin-maps` / `twin-maps-plants` | 21 PASS / the no-edit plant caught on its three words | `receipts/twin/` |
| harness self-test (`run.py --self-test`) at `10264ac2`'s SoC change | rc 0, `self-test: 0 failures` | scratch `units/selftest1.log` |
| harness, arm A, edit groups: 1x1 (aecp-fanout, aecp-largest-notice, aecp), 8x8-1if (aecp-fanout, aecp) | 0 refusals, 0 budget misses, 0 passes over the share | `receipts/budget/` |
| record classes on those groups | 1x1/1if long 92,489 cycles (975 us, stated 975); paced one-row edit 26,177 (275 us, under the class's 300); other 19,437 (205, stated 235); 8x8/1if other 19,946 (210) | `receipts/budget/record-classes-*.txt` |
| release image, base and head, both configs | `bios.bin` byte-identical; `bios.elf` identical with debug stripped | `receipts/release/` |
| ROM, every image at every point, base and head | see section 5 | `receipts/rom/` |
| idioms (`check_py_idiom.py`, `check_cpp_idiom.py`), `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, `ctrl_hot.py --check`, `check_baremetal_only.py --check`, `load_grade.py --check`, `flip_grade.py --check --point 1x1/1if` | rc 0 each | (foreground) |

Not run this round: the clean-clone workflow pass, the 4-shard sweep, the 8x8/1if image (refused by its plan).

## 5. Costs, rows, ROM, area, release hash

- Costs: the edit's transaction at the contract's slowest datapath adds about 864 CPU cycles a 5-beat transaction
  (the largest legal command 91,625 -> 92,489). No stated cost the tier model reads moves: `LONG_RECORD_US` 975 and
  `EDIT_RECORD_US` 300 hold. `edit_rows.PACED['1x1/1if']['a one-row edit']` 260 should become 275 by the rule,
  pending the full runs. The tier model at the head is unchanged: txL 48.58 of 49, R4L 203.57 of 238 at 1x1/1if.
- ROM (`receipts/rom/`): platform 1x1/1if 43.0 -> 43.5, 1x1/2if 44.0 -> 44.5, **8x8/1if 56.0 -> 56.5 (refused)**,
  8x8/2if 60.5 -> 61.0 (its entry 60.5; `ctrl_plat` 20,352 -> 20,416 B); fixture 1x1/1if 41.0 -> 41.5, 1x1/2if 42.5 -> 43.0,
  8x8/1if 55.0 -> 55.5, 8x8/2if 59.0 -> 59.5 (its entry 59.0). Sram unchanged at every point but the platform 8x8/2if
  (+64 B). The text growth by object: `aecp_maps.c` +1,720, `aecp_face.c` +1,012, `aecp_mbx.c` +60,
  `ctrl_app_aecp.c` +68, `mbx.c` +44, `aecp_commands.c` +12 (`receipts/rom/objects-*.txt`; rv32im -Os at the 8x8
  header). A one-loop face walk measured 216 B smaller (not kept).
- Area: not measured (no route yet).
- Release: byte-identical (`receipts/release/VERDICT.txt`).

## 6. Run history

- 02:32 assignment read; #923, #924, #665 report and ruling, replica handoff 10.4 and the f14 probes read.
- 02:5x TAKEN posted.
- 03:00-03:40 firmware, unit tests, 29 plants (all caught), harness SoC EDIT answer, harness self-test rc 0, `10264ac2`.
- 03:40-03:50 twin-maps co-simulation (21 PASS) and its plant (caught), docs, `def26a61`.
- 03:44-: every CPU range booked (128 busy); the firmware unit suite needs more than 10 min, so it waits for a range.
- 04:16-04:35 the harness edit groups at both points (session pool; no range in 0-95 was free all night); the
  release image hash at base and head.
- 04:31 the full arm A at both points started in three parts each, and the answering-ports arm's edit groups.
- 04:40 the ROM ledger: the 8x8/1if platform image over the 56 budget; compaction measured; STOP posted 05:1x.
- 05:0x the 1x1/1if split image queued behind a Vivado slot (`img1x1`).

## 7. Units still running at the STOP (each its own systemd user unit; output under the scratch `units/` and `build/`)

| Unit | What | Output |
|---|---|---|
| `milan-923-a789-fw0`, `-fw2` | rtl-fast's firmware-unit (shard 0, with the store suites and `fw_coverage.py --check`) and the AECP campaign (shard 2), clean clones `c-fw0`, `c-fw2` at `def26a61` | `units/fw0.log`, `units/fw2.log`, `.rc` |
| `milan-923-a789-a1x1p0..2`, `-a8x8p0..2` | arm A, every remaining group, 1x1 and 8x8-1if, on the edit groups' builds (`build/b1x1`, `build/b8x8`), clone `c-head` | `build/b*/parts/p*/` |
| `milan-923-a789-B1x1`, `-B8x8` | the answering-ports arm's aecp, aecp-fanout, aecp-largest-notice | `build/B1x1`, `build/B8x8` |
| `milan-923-a789-img1x1` | the 1x1/1if split image, S9's recipe, directive ExtraPostPlacementOpt, behind `vivado-slot.sh` | `units/img1x1.log`, `image/endstation_ax7101_1x1_tdm8/` |

## 8. For round 2 (after the ruling)

- Apply the ruling on the 8x8/1if image (recommendation A: a `ctrl_memory.LEDGERED` product entry at 56.5 with its
  symbols, `add_ctrl_memory` planning it, `ctrl_memory_ledger.py`/`test_ctrl_memory.py`, `plat_ledger.py`, the fit
  page), and raise the two 8x8/2if entries to 59.5 and 61.0 (`ctrl_plat` 20,416, `PLAT_8X8_2`).
- `edit_rows.PACED['1x1/1if']['a one-row edit']` to the full runs' figure (275 us from the edit groups), and
  `rows_tiers.LONG_RECORD_US`'s comment to 92,489 cycles; re-run `flip_grade.py`/`load_grade.py` checks.
- The 8x8/1if image, the other two directives for both images, the area delta, the clean-clone workflow pass and
  the sweep; then REVIEW READY and PR-BODY.md (a draft is in this directory).
- SET_STREAM_INFO bodies past 84 octets are still taken (the processor refuses them): recorded in PR-BODY's
  limitations, not changed.
