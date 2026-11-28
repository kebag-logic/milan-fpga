[R928] NEGATIVE - exact head c0b625d1792e61b8e99944daea65b842e6b9dcde

External independent re-review R928-5 of [PR #1004](https://github.com/kebag-logic/milan-fpga/pull/1004), relating to [#878](https://github.com/kebag-logic/milan-fpga/issues/878). Head tree `1f528462806ea0a8262320787e7c3cbb2431b0f7`. Delta since my last reviewed head: `011aaa6f..c0b625d1`, the merge `aa53840d9` of dev-soft-core `0b594023` plus 18 lane commits (25 files, +1268/-66 after the merge).

**The measured results of rounds 10 and 11 reproduce. The verdict is NEGATIVE because a required repository gate fails at this exact head, the merged image has no public routed evidence, and six MINOR findings are open.**

- The hosted `firmware-boundary` job fails at this head on a file this delta adds, and I reproduce the refusal locally (F1, BLOCKER).
- The round-10 census extract regrades identically at the head: 159 of 159 cases and the cross-case step PASS, byte-identical to the author's round-10 and round-11 logs. A copy without `none/srp-bound` is refused by name.
- The 100 Mb/s egress row is 505.738 us of 1000 us from the published observations, byte-identical to the author's grade. The fixed path measures 312.5 ns, stated 320 ns.
- The three shipping ELFs cannot differ from `640699e6`'s: the only compiled input changed since is a two-line comment in `ctrl_loop.h`.
- Both round-3 extractor findings and the empty builder receipt are closed at their cause.

## Scope and authority

Read in order: AGENTS.md and CONTRIBUTING.md (unchanged by the delta), docs/README.md, #878's frozen acceptance and its public rulings, then the diff, then the public evidence at commit `3e8f3014f28d13bd008b06ec43f919d282d681ee` (`author-r10`, `author-r11`). The rulings governing this delta are retained verbatim in `receipts/public-scope.json`:

| Authority | What it requires here |
|---|---|
| [Egress ruling on #1020](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7216971645), carried as a [merge gate on #1004](https://github.com/kebag-logic/milan-fpga/pull/1004#issuecomment-7216972073) | At 100 Mb/s `T_egress` is a held row. (a) Every commit's free-space test keeps its census outcome, else the census is re-run drained at link rate (item 3). (b) Largest commit-to-last-octet wait plus 5 % plus the fixed path is at most 1000 us. Grader with planted defects; FR_NFR 3.4.1 states the row and 254 records. |
| [Bind-bound ruling](https://github.com/kebag-logic/milan-fpga/pull/1004#issuecomment-7221391389) | The Arty in-flight bound is the rest of a save plus one save from the census model's save time; burst count by the same rule; the bench figure stated beside it. |
| [Held-egress ledger ruling on #1020](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7234489667) | The 62.14 ms point is the USB-network Arty's and belongs to #1020. The 1x1 Arty's figures are unchanged, which holds: `egress_ledger.ARTY` changes only in a comment. |
| [#878 acceptance ruling](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7153532537) | PR #1004 relates to #878 and may merge on its own gates; #878 stays open for the offset line. |

## What I verified

| Check | Result | Receipt |
|---|---|---|
| Published packets | `author-r10` 976 files and `author-r11` 342 files equal their outer manifest; the 834 extract files are original = published = actual, none redacted; 832 inventory entries, 159 case manifests and both inner manifests verify | `receipts/audit.log` |
| Census regrade at the head | Exit 0: `RESULT: PASS cases=159 worst_pass_cycles=143181` and the cross-case PASS. Byte-identical to the author's `extract-regrade.log`, `regrade-full.log` and round-11 `consistency/extract-regrade.log` | `receipts/regrade.log` |
| Missing-bound control | Exit 1 after 158 grades: `srp-kept and srp-bound are graded together on one image, this run graded srp-kept alone` | `receipts/missing-bound.log`, `control-preparation.log` |
| 100 Mb/s row | 159 cases, 27,924 records, 0 refused, 0 disagreeing, 44 held in two cases, at most 19 queued. `426.470 us + 54.88 us, x 1.05, + 0.32 us = 505.738 us`. Byte-identical to both author logs | `receipts/egress-packet.log` |
| Fixed path | 312.5 ns at most over 7 lengths and 64 phases, pinned Verilator 5.050 | `receipts/egress-fixed.log` |
| Self-tests | `egress_mii` 17/17, `census_extract` 6/6, and `rows_tiers`, `load_grade`, `egress_ledger`, `record_classes`, `arty_grade`, `kept_grade`, `arty_grade.py`, `--structural` (391.51, 2177.82, 2646.82 us) all exit 0 | `receipts/selftests.rc`, `selftest-*.log` |
| Documentation gates | 14 of 14 exit 0: docs check, style, paths, gPTP docs, inventory, Python and C++ idiom, em dash, contents, anchors, bare-metal and its self-test, test-evidence, register reference (fresh; the page differs from `640699e6` by the three parameter rows only) | `receipts/gates/` |
| ELF identity to `640699e6` | 11 files differ; the only compiled input is `ctrl_loop.h`, a 2-line comment, 667 lines at both heads, comment-stripped SHA256 `26be07bc…` at both. No gitlink moved. The author's receipt gives `f17d1a9d…`, `0f1450ac…`, `6e0a5412…` at both heads | `receipts/elf-source-identity.log` |
| Merge resolution | Three files differ from both parents: `CDL_BOUND` joins `ctrl_mutant_fixtures.py`, its import is added, and `run.py`'s docstring is rewrapped. No lane label returned | diff of `aa53840d9` against both parents |
| Rulings in code | 254 = 21+42+85+21+85; 21,336 wire bytes. Bind: 188.8 ms twice is 377.6, stated 400; burst floor(530/188.8)+2 = 4; measured 369.2 ms and 4 saves. Queue constants match `milan_soc.py:1483-1499`, `milan_datapath.sv:9227` and `mbx_contract.h:1406` | code read; `receipts/regrade.log` |
| Console coverage exclusion | The arc is infeasible: `lat` returns unless `c->len == 15`, and the walk compares `at` of at most 3 with it (`ctrl_plat_console.c:178-185`) | code read |
| Clone integrity | 2008 tracked blobs, modes, index and the five initialized gitlinks equal the head; no untracked or ignored file left | `receipts/source-integrity.log` |

## Findings

### R928-5-F1 - BLOCKER - Tests, Docs - the `firmware-boundary` gate fails at this head on `egress_mii.py`

- **Artifact:** `sw/firmware/ctrl/test/ctrl_configs.py:161` (`OUTSIDE`) and `:473-479`; `tb/verilator/ctrl_service_budget/egress_mii.py:49`; `.github/workflows/rtl-fast.yml:1351,1436`; the PR body's round-11 section and Definition of done.
- **Evidence:**
  - Hosted [job 140976578401](https://github.com/kebag-logic/milan-fpga/actions/runs/46139268494/job/140976578401), step 13, exits 2: `REFUSED: tb/verilator/ctrl_service_budget/egress_mii.py names the firmware's tree and is a program, and is neither a known builder … nor listed …` (`receipts/hosted-firmware-boundary-refusal.txt`). The run tested merge `1529cf41` of this head into `0b594023`, whose tree is this head's.
  - Reproduced at the exact head without a capture: of 94 files that name the firmware tree, one program is listed nowhere, `egress_mii.py` (`receipts/probe-boundary-listing.log`, exit 1). The file is new in this delta.
  - The author's local CI ran the two capture legs but not this job. `author-r11/receipts/ci-final/results.json` has 67 jobs and no `rtl-fast/firmware-boundary`; the index classes it with "jobs that only read other jobs' artifacts". It is a gate of its own.
  - Fail-fast then cancelled the rest. Hosted `rtl-fast` and `rtl-full` concluded cancelled: 26 contexts cancelled, among them 8 of 27 Verilator shards and all 4 Yosys shards (`receipts/hosted-checks.tsv`, `hosted-runs.txt`).
- **Impact:** the head has no successful `rtl-fast` verdict and no exact-head `verilator-suites` or `yosys-portability` evidence, which AGENTS.md section 7 requires. The PR's "every pull-request CI job passes at the head" is not true.
- **Required outcome:** `egress_mii.py` is listed in the table that fits it with its reason, and the whole `firmware-boundary` job passes. The PR text names which jobs a local replica ran and which it did not.
- **Verification:** `scripts/probe_boundary_listing.py` exits 0 at the new head, and the hosted `firmware-boundary`, `rtl-fast`, `verilator-suites` and `yosys-portability` contexts succeed there.

### R928-5-F2 - MAJOR - Conformance, RTL, Tests, Docs - the merged image has no public routed, utilization or identity receipt

- **Artifact:** PR body "Source and image" and Definition of done; evidence tree at `3e8f3014`; #878 acceptance item 1.
- **Evidence:** the merge changes a gateware input (the gPTP processor pin, so `gptp_ucode.hex`) and the firmware, so the image at the head is not round 7's. The PR states bitstream `82a226e3…`, checkpoint `6aec5a4a…`, WNS/WHS at twelve reports, 33077 LUTs and passing identity and flash-pair checks. The evidence tree holds no round-9 packet and no timing report, utilization report, checkpoint or bitstream hash, image manifest, native boot or region log for this image. `author-r10/receipts/INDEX.md` says round 9's gates "stand" and links nothing. Round 7's equivalents are published (`author-r7/image/`, `timing-r7/`, `author-r8/receipts/route-utilization/`), which closed R928-2-F2.
- **Impact:** acceptance item 1 for the image this head carries rests on PR prose. The stated Fast WHS of +0.017 ns is under the recorded +0.030 ns floor and cannot be inspected. The +62-LUT line the PR leaves "to review" cannot be judged from public bytes. The published bench result is the round-7 image's.
- **Required outcome:** publish, bound by hash to the checkpoint, the bitstream and ELF `f17d1a9d…`, the post-route timing at every corner, the post-route utilization, the image manifest with its identity and flash-pair logs, and the native boot, controls and region logs. Attribute the +62 LUTs, for example by a hierarchical utilization comparison with round 7.
- **Verification:** a cold reader regrades timing and reproduces the LUT comparison from an evidence commit, and the figures equal the PR's.
- **Lens note:** the internal reviewer filed this cause as MINOR under RTL and Docs. I keep MAJOR: R928-2-F2 was MINOR when only the utilization comparison was missing, and here every routed receipt is. Both lens sets are recorded.

### R928-5-F3 - MINOR - Docs - the harness README names the superseded qualification as the installed row's

- **Artifact:** `tb/verilator/ctrl_service_budget/README.md:229-231`.
- **Evidence:** the README cites the round-7 file, SHA256 `076e7cc7…`, "PASS over 147 measured cases", and says "its `model` is `arty_grade.py`'s at this point". At the head `arty_grade.inspect()` equals the 159-case link-rate qualification `3075a3eb…` and differs from the cited one in 16 model fields, among them load, ACMP, txL and last notice (`receipts/qualification-pointer.log`). `563ee9105` raised the statements and left these lines.
- **Impact:** the pointer, hash, case count and model claim are wrong at the head. This is the cause both reviewers closed at `011aaa6f` (R927-2-F2), reopened by the delta.
- **Required outcome:** cite the 159-case qualification by an evidence-pinned link, its SHA256 and its count; keep `076e7cc7…` as history only.
- **Verification:** `scripts/qualification_pointer.py` prints `True` for the file the README names.

### R928-5-F4 - MINOR - Docs - section 15 states the non-carrying census's observed figures

- **Artifact:** `docs/design/SPLIT_CONTROL_MEMORY.md:3581-3582` and `:3594`; the PR body's owner-bound table.
- **Evidence:** section 15 gives an observed maximum whole pass of 143165 cycles (1.7895625 ms) and held-egress rows of 61.80119 to 63.30645 ms. The link-rate census, which carries under the ruling's item 3 and which the regrader reproduces at the head, observes 143181 cycles (1.7897625 ms) and 61.80119 to 63.31139 ms (`receipts/regrade.log:178,183`). Neither 143165 nor 63.30645 is in any round-10 or round-11 receipt.
- **Impact:** the design record states a superseded campaign's maxima, each smaller than the carrying census's. Both stay inside their bounds (2 ms; ledger 63.51 ms), so no verdict moves.
- **Required outcome:** state the link-rate census's figures, or both campaigns' with each attributed to a published receipt.
- **Verification:** the figures equal `census/qualification.json` and the regrade log.

### R928-5-F5 - MINOR - Tests, Docs - the egress agreement check does not compare the beat-in it says it does

- **Artifact:** `tb/verilator/ctrl_service_budget/egress_mii.py:439`; `README.md:263` ("reproduce every departure the testbench printed exactly, the beat in and the last octet").
- **Evidence:** `agree` compares the anchored last-byte edge and the last octet only. A synthetic log with one `EGRESS` beat-in moved one datapath cycle grades `agree_ps=0` and PASS; the same shift on the last octet fails (`receipts/probe-egress-beat-in.log`). On the published extract the beat-in does agree in all 27,924 records, so the measured result stands.
- **Impact:** a queue divergence that moves when a frame enters the FIFO, but not its last octet on a busy wire, passes. The FIFO's occupancy decides `tx_ready`, the quantity item 2(a) is about.
- **Required outcome:** compare the beat-in too, with a plant its control catches; or state only what is compared.
- **Verification:** the probe reports a failing verdict for the beat-in shift, and `--selftest` shows the new plant caught.

### R928-5-F6 - MINOR - Tests - the extractor self-test does not bind the limit its readers pass

- **Artifact:** `tb/verilator/ctrl_service_budget/census_extract.py:46,132,139-181`; `receipt_regrade.py:192`; `egress_mii.py:640`.
- **Evidence:** with `READ_LIMIT` set back to `PART_LIMIT`, the round-3 defect itself, `--selftest` still passes 6 of 6 (`receipts/probe-extract-limit.log`). Its controls pass their own `limit + 1` to `read_parts` and never reach `case()`. The three readers each compute `+ 1` on their own. The published extract's largest part is 13,999,999 bytes, one short of the limit, so no real packet exercises the boundary either.
- **Impact:** the control added for R928-3-F2 cannot fail for R928-3-F2. That finding's stated verification asked for exact-limit controls that reproduce their grades.
- **Required outcome:** a control that drives the production read limit (through `case()` or the constant its readers share) on an exact-limit part and fails when the limit is exclusive.
- **Verification:** the probe's mutant is reported killed.

### Retained from the internal review at this head

I read the internal reviewer's round-5 report only after my own findings were fixed. Its F2, F3 and F5 are the causes of my F4, F3 and F2. Its other two I checked myself and retain:

- **R927-5-F1 - MINOR - Tests - an over-exclusion defect passes the egress gate.** `egress_mii.py:412-422,544-610`. Confirmed: with `mark_held` leaving every record to the ledger, every control still holds, and two unheld 550-byte frames grade `wait_ps=0`, PASS, against 112,567,500 ps shipped (`receipts/probe-egress-all-held.log`). The shipped plants test only the opposite direction. Required outcome and verification as the internal report states: a control that holds an unheld record to its hand-computed wait, with the all-held plant caught.
- **R927-5-F4 - MINOR - Conformance, Docs - FR_NFR 3.4.1 calls a figure the structural maximum that the same paragraph exceeds.** `docs/reference/FR_NFR.md:511`. Confirmed by reading: "each waits at most 391.5 us" is under the census's 426.47 us two lines above and under the 2.65 ms rings-at-capacity figure one line below. Required outcome: say what the AECP figure bounds, and that the row is census-held under the ruling with the 2.65 ms envelope outside it and its disposition named.

## Prior findings at this head

| Finding | Disposition | Cause-level evidence |
|---|---|---|
| R928-3-F2 MINOR, inclusive part-size boundary | **CLOSED at its cause**; its control gap is F6 | `READ_LIMIT = PART_LIMIT + 1` at `census_extract.py:46,132`; the CLI and the egress reader add one. At the shipped 14,000,000 bytes, a single part and a first part before another are written and read back, and refused under the old exclusive limit (`receipts/probe-extract-limit.log`). README:238-241 states the contract. |
| R928-3-F3 MINOR, overlong line never advances | **CLOSED** | `census_extract.py:73-77` refuses when no newline ends inside a part. At the shipped limit an overlong line is refused first and after a completed part, leaving at most one file; three self-test controls cover it. |
| R927-3-F2 MINOR, empty builder receipt | **CLOSED** | `author-r10/receipts/builder/builder-split.log` and `.json`: the command, four heads, every output's SHA256 and exit 0. `4adfa9dc` to `011aaa6f` is identical in both placements; the merge changes `gptp_ucode.hex` only. The later head compared is `fb4b456a4`; nothing the builder reads changed after it. |
| R928-3-F1 / R927-3-F1, published extract bytes | Remains **CLOSED**, now for the round-10 extract | 834 files original = published = actual; unmodified regrade and control above. |
| R927-2-F2 / R927-1-F6, qualification pointer | **REGRESSED**: reopened as F3 | Above. |
| R928-2-F2, routed comparison | Closed for round 7's image; the merged image's equivalent is **F2** | Above. |
| R928-2-RS1, lane labels in the fixture file | Remains closed | `ctrl_mutant_fixtures.py:5-7,27-28` carry issue and requirement IDs; the base's labelled block did not return through the merge. |
| R927-2-F1, R928-1-F2, R928-1-F3 / R927-1-F1, R927-1-F2 to F5 | Closed, carried | Section 15 still routes the owed cost to #1022; inventory and idiom gates pass at the head; no firmware source changed in the lane's delta but one comment. |
| R927-3-RS-1, inventory wording | **CLOSED** | `census_extract.py:11-15`, README:238-240; the copied qualification is now checked against the inventory (`:199-204`). |

## Wording residue

Each is wording only; none changes a figure, a test or a verdict.

- **R928-5-RS1 - source-comment rule.** `egress_mii.py:5-6` shows issue-comment IDs in a docstring. Replace "ruling (comment 7216971645) makes" with "ruling makes", and "as a merge gate (comment 7216972073):" with "as a merge gate:". It is the only new instance in the delta (`receipts/comment-rule-sweep.txt`). Same as the internal RS-4.
- **R928-5-RS2.** `egress_fixed.py:11` gives `python3 -I egress_fixed.py BUILD_DIR`, which fails with `ModuleNotFoundError: egress_mii` (`receipts/egress-fixed-isolated.log`); without `-I` it passes. Fix: "usage: python3 egress_fixed.py BUILD_DIR". My own pass drafted this as MINOR; on reconciliation I accept the internal RS-5 class, since the usage line alone resolves it. The code alternative is S2.
- **R928-5-RS3.** `README.md:266`, FR_NFR:509 and the PR body say both hold cases leave their records "to the ledger". `egress_ledger.py` has no `aecp-outputs` row; that case's 18 records are held by its own rows' budgets (`aecp_outputs.held_set_stream_info`, `held_get_stream_info`, 9.10 and 4.05 ms in its published grade). Fix for the README: "`backlog-owed` leaves 26 held records to the ledger and `aecp-outputs` 18 to its own held rows (`declaring_outputs.py`)".
- **R928-5-RS4.** PR body and `author-r11/receipts/INDEX.md`: "Removing the redundant bound would have changed every image." Only `endstation_arty_split.yaml` sets `latency_writable`, so only that image compiles `lat`. Fix: "would have changed the Arty split image".
- **R928-5-RS5.** PR body, round 10: "See the open questions." The body has no such section. Fix: list the two questions, or link `author-r10/REVIEW-READY.md` at the evidence commit.
- **R928-5-RS6.** `scripts/measure_test_evidence_readers.py:296-301`: the waits are the testbench queue model's printed departures, and the Python queue is a port of that model. Replace "the census's own measured departures, held to that testbench's C++ queue as an independent second implementation" with "the departures the census testbench's C++ queue printed, which this module's Python port of that queue must reproduce exactly".
- **R928-5-RS7.** `author-r10/receipts/recipes/gates10.sh:2` and `author-r11/receipts/gates/gates11.sh:2` are headed "Round 8 gates at the head". Fix: the round each ran in.
- **Retained, widened (internal RS-2).** `author-r8`, `author-r10` and `author-r11` `receipts/INDEX.md:5`, both REVIEW-READY files and both HANDOFF files say nothing has been posted or pushed. All are published. Delete the sentence or prefix it "When written:".
- **Retained (internal RS-3).** The PR body's "Reproduce and inspect" pins no evidence commit. Link `author-r10/receipts/census-extract/` at `3e8f3014`.
- **Retained (R928-3-RS1).** `author-r7/receipts/INDEX.md:128-130` is unchanged: "ELF and stimulus are identical; these non-XIP variants produce no separate flash image".

## Suggestions

- **S1, model fidelity.** The grade checks two ports of one queue model against each other and the fixed path on an idle chain. Run a census burst through the converted MII chain and hold the model's departures to it. The internal SG-8 notes one structural difference: `milan_datapath.sv:1684-1686` describes two round-robin merges where the model has one alternation; the whole-gPTP-burst term covers it for (b).
- **S2.** Insert the script directory into `sys.path` in `egress_fixed.py`, and put it and the `egress_mii` and `census_extract` self-tests in a standing gate. A local CI replica should run every job that executes a gate, artifact-consuming ones included.
- **S3.** `egress_mii.py --packet` passes whatever population `census.json` lists; hold the case count to the published qualification's.
- **S4.** The rings-at-capacity envelope (2.65 ms) needs a recorded disposition; it goes with R927-5-F4.
- **Carried optional items** are unchanged: versioned derivation and qualification recipes (now also `qualify-final-census.py`, the only place `egress-100` is defined), the remaining extractor plants, and the earlier items outside this delta.

## Lens results

```text
[R928] MAJOR Conformance — PR "Source and image" against the evidence tree at 3e8f3014; docs/reference/FR_NFR.md:511 — F2, R927-5-F4. Otherwise applied clean: item 3 census at link rate (sim_main.cpp:150,170,258-259), row 505.738 us (receipts/egress-packet.log), 254 records (FR_NFR.md:502), bind 400 ms and 4 saves (bind_save.py:50-60)
[R928] MAJOR RTL — bitstream 82a226e3 and checkpoint 6aec5a4a against the evidence tree — F2. Otherwise applied clean: no HDL, SoC, configuration or constraint file in aa53840d9..c0b625d1; the merge's gateware delta is the gptp-processor gitlink and syn/yosys/rom_digests.tsv
[R928] PASS Robustness — census_extract.py:65-83,132,199-204 with receipts/probe-extract-limit.log; egress_mii.py:316-340,429-434,645-646; sim_main.cpp:170 and egress_queue.hpp:47-48 (a gigabit point states no queue)
[R928] BLOCKER Tests — hosted job 140976578401 and receipts/probe-boundary-listing.log — F1; also F2, F5, F6, R927-5-F1
[R928] BLOCKER Docs — PR round-11 section and Definition of done — F1; also F2, F3, F4, F5, R927-5-F4
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F2, R927-5-F4 | Rulings 7216971645, 7216972073, 7221391389, 7234489667; #878 acceptance; FR_NFR 3.4.1 at `:499-513`; section 15; `egress_mii.py`, `egress_queue.hpp`, `sim_main.cpp`, `bind_save.py`; regrade, egress grade and control | R928-5 applied; no clean covering round | `c0b625d1792e61b8e99944daea65b842e6b9dcde` |
| RTL | UNCLEAN: F2 | Merge gateware delta; lane delta (no RTL file); queue constants against `milan_soc.py`, `milan_datapath.sv:9227`, `mbx_contract.h`; fixed-path run on `mac_tx_chain_mii.v`; image claims against the evidence tree | R928-5 applied; no clean covering round | `c0b625d1792e61b8e99944daea65b842e6b9dcde` |
| Robustness | CLEAN | Extractor refusals and limits at the shipped value; egress parse, refusal and hash paths; the testbench's gigabit path; merge resolution; the `lat` length guard | R928-5 | `c0b625d1792e61b8e99944daea65b842e6b9dcde` |
| Tests | UNCLEAN: F1, F2, F5, F6, R927-5-F1 | Hosted check runs and the boundary probe; egress and extractor self-tests with three mutation probes; regrade and control; fixed path; bind targets (`selftest_bind.py:290-293`); coverage exclusion and its logs; author's `ci-final` | R928-5 applied; no clean covering round | `c0b625d1792e61b8e99944daea65b842e6b9dcde` |
| Docs | UNCLEAN: F1, F2, F3, F4, F5, R927-5-F4 | FR_NFR 3.4.1; section 15; harness README:141-145,228-268; gtest README and ratchet; register reference; `ctrl_loop.h:354-355`; the live PR body; r10 and r11 INDEX, REVIEW-READY, HANDOFF; 14 gates | R928-5 applied; no clean covering round | `c0b625d1792e61b8e99944daea65b842e6b9dcde` |

All five lenses were applied to the delta. RTL has no lane source change to examine; its open finding is the merged image's missing evidence.

## Reproduction

From the exact-head checkout, with `PACKET` this directory and `X=$PACKET/scratch/evidence/author-r10/receipts/census-extract`. All disposable material stays under `scratch/`.

```sh
git fetch --no-tags --filter=blob:none origin 3e8f3014f28d13bd008b06ec43f919d282d681ee
python3 -I "$PACKET/scripts/fetch_evidence.py" . "$PACKET/scratch/evidence"
python3 -I "$PACKET/scripts/audit_evidence.py" "$PACKET/scratch/evidence"
python3 -B tb/verilator/ctrl_service_budget/receipt_regrade.py "$X"
python3 -I -B tb/verilator/ctrl_service_budget/egress_mii.py --packet "$X"
python3 -I "$PACKET/scripts/prepare_control.py" "$X" "$PACKET/scratch/control" none/srp-bound
python3 -B tb/verilator/ctrl_service_budget/receipt_regrade.py "$PACKET/scratch/control"
PATH="$PINNED_VERILATOR:$PATH" python3 -B tb/verilator/ctrl_service_budget/egress_fixed.py "$PACKET/scratch/egress-fixed"
python3 -B "$PACKET/scripts/probe_boundary_listing.py" .
python3 -B "$PACKET/scripts/probe_extract_limit.py" . "$PACKET/scratch/probe-tmp"
python3 -B "$PACKET/scripts/probe_egress_beat_in.py" . "$X"
python3 -B "$PACKET/scripts/probe_egress_all_held.py" .
python3 -I "$PACKET/scripts/qualification_pointer.py" . R7_QUALIFICATION "$X/published-qualification.json"
python3 -I -B "$PACKET/scripts/check_source.py" .
```

`R7_QUALIFICATION` is `review-evidence/artysplit-r1/author-r7/receipts/published-qualification.json` at the evidence commit. The register-reference gate needs the pinned documentation environment (`wavedrom` 2.0.3.post3). The regrade, the egress grade, the control and the self-tests ran concurrently, each with its own log and status file.

## Real limits

- **Order of reading.** My findings F1 to F6 and the lens verdicts were fixed before I read any other reviewer's findings at this head. The file recording them, `receipts/own-pass-draft.md`, was saved just after the first section of the internal report was displayed, because the first write failed. Listing the PR's comments early had also shown the first line of that report, so its verdict word was visible before my pass; nothing else was. `receipts/own-pass-draft.md` lists a seventh MINOR that reconciliation reclassified as RS2.
- **No ELF rebuilt.** Identity rests on the compiled-input proof and the author's receipt.
- **No image built, routed or timed**, no Vivado run and no hardware. F2 is about publication; I neither confirm nor dispute the timing figures.
- **The queue model is checked against its sources' constants and the idle fixed path**, not cycle for cycle against the RTL under load.
- **Coverage figures** (154/154 lines, 97/97 branches) rest on the author's logs under two compilers; I checked the arc's infeasibility by reading.
- **The author's 212 local steps were not rerun.** I reran 14 gates, 8 self-tests, the regrade, the egress grade, the control and the fixed path.
- **Hosted evidence at this head, read after 12:44Z:** `docs` and `elaborate` succeeded. `rtl-fast` and `rtl-full` concluded cancelled after `firmware-boundary` failed. 61 contexts succeeded, among them 19 of 27 Verilator shards, the three unit legs and the lint; 26 were cancelled; 10 aggregate contexts failed because their legs were cancelled; `Physical gPTP` was skipped. A cancelled or skipped context is not a pass. The manager owns hosted and replica acceptance.
- **No manager source bank** ran at this head and none is inferred. Source execution evidence is the author's receipts, with census executables at `7bc47c0ee`; no testbench, firmware or RTL file changed after it.
- **Physical calibration NOT RUN.** Field skips are not hardware proof. The public bench result is the round-7 image's (bitstream `24a782c5…`, ELF `b6cfb9a4…`), not this head's.
- **Receipts are raw** except that the checkout's path is written `$SOURCE` in `egress-fixed.log`, `egress-fixed-isolated.log` and `missing-bound.log`.
- **The evidence commit is unsigned** and no detached signature was supplied. Hashes and Git objects verify; signer authentication is not established. Hashes of original logs cannot authenticate bytes an extract omits.

## Pending manager duties

- A follow-up round must fix F1 to F6 and the two retained internal findings, and re-cover Conformance, RTL, Tests and Docs at its head. Any new commit also un-covers Robustness where it touches that lens's artifacts.
- Carry the residue list to the residue checklist.
- The PR is `CONFLICTING` with its base: `dev-soft-core` is now at `c1c42843`, and the PR names one more integration after #977. That integration changes the candidate.
- Build and validate the current-dev merge candidate (builder and native banks; source base `854bd7236792ce1adbd10c43b13a6a5002ad3bb6`, live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`) and link its receipts. This report validates neither merge.
- Decide the disposition of the 2.65 ms rings-at-capacity envelope, and whether the merged image needs a bench run before it is called the published image.
- Hosted and local-replica acceptance at the final head, two independent positive reviews, maintainer authorization and post-merge containment remain required. #878 stays open for the offset line and #1022 for the owed registration cost.
- No source fix, commit, push, GitHub write, author contact, full bank, hardware operation or edit to another checkout was made. Only this report and the files in `MANIFEST.sha256` are publishable.

R928-5 FINISHED
