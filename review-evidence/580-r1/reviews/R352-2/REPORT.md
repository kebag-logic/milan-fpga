[R352] POSITIVE - exact head d02db63c367daf9adc7d709840bd81077e781d80

Round R352-2 is the internal independent re-review of PR #591 for issue #580.
It reviews head `d02db63c367daf9adc7d709840bd81077e781d80` (tree `b13027cbe7f6ba11196446cb4ad3cd797a94b70f`), one commit on `499b15f97eb0a469b7cd1308fbba7af3c64d1851`. The PR base is dev `682ecf0cb995473b72d5b4921088053ba753fc93`.
This is a delta review of `499b15f9..d02db63c`. I applied all five lenses at this head and all five are clean.
There are no open BLOCKER, MAJOR or MINOR findings, only two SUGGESTIONs, and my round-1 finding F1 is closed.
I reproduced the capture re-measurement at this head: the full 1x1 50 MHz traffic-ON arm and the leading rows of both 8x8 50 MHz arms. Every reproduced row equals the receipt, field for field.

## Reconstruction

I read these in order:

- AGENTS.md, CONTRIBUTING.md (including "Measure, don't assume", `:521`), docs/README.md and REQUIREMENTS.md REQ-VER-03/04.
- The issue #580 body, the [A10] scope comments 5854203161, 5854653164 and 5854987837, and the assignment 5856274975.
- The round-2 decision 5857045698 ("re-measure", which corrects assignment item 4), then the [A368] TAKEN (5857067335) and REVIEW READY (5857520828) comments.
- The PR #591 body.
- `tb/verilator/nvm_capture_cpu/README.md`, `run.py`, `soc.py`, `scripts/check_nvm_capture.py` and the receipt.
- The diffs `499b15f9..d02db63c` (5 files) and `682ecf0c..d02db63c` (13 files).
- The public evidence tree `147cb4b8:review-evidence/580-r1` (round-1 author packet; the tree has no round-2 packet).

I read prior public findings only after my own pass over the diff. My own R352-1 findings are dispositioned below. I wrote this verdict and ledger before reading the other reviewer's round-1 report; the last section records what I found there.

The delta `499b15f9..d02db63c` touches only these files:

- `CHANGELOG.md`
- `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md`
- `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md`
- `docs/reference/SUBMODULES.md`
- `tb/verilator/nvm_capture_cpu/measurements.json`

It changes no `hdl/`, `sw/`, `configs/`, harness `.py`/`.cpp` or gitlink path (`receipts/environment.txt`). The three initialised gitlinks are identical at `499b15f9` and `d02db63c`.

## Assigned verification points

| # | Point | Result | Receipt |
|---|---|---|---|
| 1 | Receipt `base` gitlink equals `processor_pins.protocol-processor` (16be6768) | **PASS.** `git rev-parse 499b15f9:protocol-processor` = `16be6768f710e79450aace277abacd6c2c3336e5` = `measurements.json:306`. `git rev-parse 499b15f9^{tree}` = `83b988d3…` = the receipt `tree` (`:310`). The `gptp-processor` and `verilog-axis` pins also equal the tree's gitlinks. The measured source (`499b15f9`) differs from this head only in the five non-product files above. So the measured product equals the head's product. | environment.txt |
| 2 | The measurement is real: reproduce at least one 8x8 arm at the head and compare | **PASS.** The builds and runs used the head clone, with processor checked out at `16be6768`, Verilator 5.052 (the receipt's simulator), the SDK compiler 14.3.0 and the receipt's SoC component revisions. The network was disabled with `unshare -Urn`, and the flags were exactly those of the receipt. Results: **8x8/50/ON** rows 0-2 are 3/3 identical in all 11 fields. **8x8/50/OFF** rows 0-1 are 2/2 identical, including row 1 = 2,426,154 ticks, the OFF arm's maximum. **1x1/50/ON** has all 16/16 rows identical. For that arm, `run.py`'s own grader passed, `CAPTURE_DONE` was present with native rc 0, and every field of the regenerated `measurement.json` summary equals the receipt arm. The CPU netlist, instrumented firmware, BIOS, gPTP microcode, config and product firmware hashes all equal the receipt rows for each arm. The measured SoC's source list takes 45 sources from this clone's `protocol-processor` at `16be6768`. | repro-*.txt, repro-1x1-50-on.measurement.json |
| 3 | `check_nvm_capture.py` passes | **PASS**, rc 0 at the head. The four named mutations (`bytes`, `records`, `clock`, `ignore-off-timing`) each give rc 1. | check_nvm_capture.log, check_nvm_capture-mutation-*.log |
| 4 | Receipt rows, maxima and section 18 are consistent | **PASS.** I recomputed every arm's min/max ticks, ms and 49 ms margin from the receipt rows. Each of the six strings appears verbatim in the section 18 table (`SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1625-1630`). The maxima (`measurements.json:284`) are 1x1 6.60642, 8x8 24.30246 and 8x8@100 19.79024, and the gate recomputes them. The 8x8 contract maximum is 24.30246 ms, 0.19754 ms below 24.5 ms, so the STOP was correctly not triggered. | check_nvm_capture.log |
| 5 | CHANGELOG and section 18 state the re-measurement | **PASS.** `CHANGELOG.md:46-49` says the capture was re-measured at the adopted pin, the receipt names the measured parent tree and pins, there are 16 captures per arm, and the 8x8 maximum is below 24.5 ms. The round-1 overclaim "Measured inputs remain unchanged" is removed. `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1591-1598` gives the date, the pin-adoption assignment, the measured parent `499b15f9`, tree `83b988d3` and pin `16be6768`. | diff |
| 6 | Doc suggestions applied | **PASS.** R352-1 S1 is applied at `PP_DESCRIPTOR_OWNERSHIP.md:5` ("The audit's processor pin was"). R352-1 S2 is applied at `SUBMODULES.md:66-67`, which links processor PRs 124/126 to the processor repository. The cluster-minimum wording from the round-2 decision is at `SUBMODULES.md:68-70`, `CHANGELOG.md:41-43` and `PP_DESCRIPTOR_OWNERSHIP.md:58,134-139,245`, with link definitions `:301-302`. I checked each linked artifact read-only. Processor #122 comment 5853884588 retains F07.2 `1..*` under Milan §5.3.3.8 and says dynamic mapping's zero maps waive nothing. Parent #584 is open and titled for the 8x8 zero-cluster violation. Processor PRs 124/126 are merged at `493e5e4b`/`16be6768`. | diff; read-only queries |
| 7 | No RTL or firmware change | **PASS.** The delta has no product path. `sw/firmware`, `configs` and the harness `.py`/`.cpp` are unchanged against the base. The product firmware hash equals `0bf43cd4…`. | environment.txt, repro-*.txt |

## Round-1 finding disposition (own)

- **R352-1 F1 (MINOR; Tests, Docs): closed at this head.** The maintainer chose the re-measure option (decision 5857045698). F1's verification condition now holds: the receipt base's gitlink equals `processor_pins.protocol-processor` (point 1). A new measurement exists at the adopted pin, and I reproduced it at this head (point 2). The receipt no longer contradicts itself (`base` `:3`, `processor_pins` `:305-306`, `tree` `:310` and `provenance` `:320` agree). The CHANGELOG wording matches the chosen option (point 5).
  - Note on the rows: the new rows are identical to the pre-bump rows. Deterministic simulation with unchanged firmware, CPU netlist and memory-path timing makes that plausible. The rows now carry true provenance because they were re-run at the adopted tree, not relabelled, and three arms reproduce here.
- **R352-1 S1 and S2 (SUGGESTION; Docs): applied** (point 6).

## Findings at this head

### S1 - SUGGESTION - Tests, Docs - `scripts/check_nvm_capture.py:58-94`, `tb/verilator/nvm_capture_cpu/README.md:154-156` - hosted capture gate cannot detect receipt provenance drift

- **Authority/evidence.**
  - The capture measures processor and parent RTL (the SoC source list includes 45 processor sources).
  - `check_receipt` never reads `base`, `tree` or `processor_pins`.
  - Probe: I set `processor_pins.protocol-processor=0922e434`, `base=831f94f4` and `tree=ae513021` (the pre-bump values) in the receipt. The gate still printed PASS, rc 0 (`receipts/probe-stale-provenance.log`). The receipt was then restored byte-exact.
  - README:156 says harness hashes prevent carrying evidence "across measurement-path changes". The hashes cover only the harness `.py`/`.cpp` files, not the RTL on that path.
- **Impact.** A future pin or RTL bump can again carry timing across a changed measured product without any gate objecting. That is how R352-1 F1 arose. It does not affect this head, whose receipt is correct and reproduced.
- **Required outcome (optional, separate Issue).** Either:
  - bind the receipt provenance to the tree in the gate (compare `processor_pins` with the gitlinks, or hash the measured RTL source list); or
  - narrow the README sentence to what is enforced.
  - This is outside #580's frozen scope ("newly discovered work becomes another public Issue").
- **Verification.** The stale-provenance probe above fails the gate, or the README states the limit.

### S2 - SUGGESTION - Docs - `tb/verilator/milan_dp/README.md:570` - "The adopted pin `0922e434`" reads as current

- This predates this PR (the pin was already `870ff88a` at the base) and is not in the diff.
- After this PR the adopted pin is `16be6768`. The sentence dates when processor PR 115 arrived. Past-tense wording, as for R352-1 S1, would avoid the ambiguity.
- Optional; a later doc change.

## Lens ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round-2 decision 5857045698 items 1-2 against: `measurements.json:2-3,284,305-310,320` (date, base, maxima, pins, tree, provenance); six-arm key set and 16 captures per arm enforced by `check_nvm_capture.py:68-79` (rc 0); 8x8 max 24.30246 < 24.5 ms; `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1591-1630`; `CHANGELOG.md:36-49`; `SUBMODULES.md:64-70`; `PP_DESCRIPTOR_OWNERSHIP.md:5,58,134-139,245,301-302`; Milan §5.3.3.8 wording against processor #122 comment 5853884588. Round-1 acceptance (pin, ledger, disposition, F7 `:247`, five-configuration equality) was covered clean at ancestor `499b15f9`, and the delta touches none of those artifacts. | R352-2 | d02db63c367daf9adc7d709840bd81077e781d80 |
| RTL | CLEAN | The delta diff has no `hdl/`, `sw/`, `configs/`, `syn/` or gitlink path (environment.txt). The gitlinks at the head equal the measured tree's. The reproduced SoC source list compiles 118 sources, 45 of them from `protocol-processor@16be6768`, with Verilator 5.052 rc 0 for three arm builds (repro-*.txt). Round-1 RTL coverage (processor `870ff88a..16be6768` changes only the Python packer; ROM digests; suites) at ancestor `499b15f9` is untouched by the delta. | R352-2 | d02db63c367daf9adc7d709840bd81077e781d80 |
| Robustness | CLEAN | Gate mutations bytes/records/clock/ignore-off-timing each rc 1 (check_nvm_capture-mutation-*.log). OFF arm rows reproduce zero traffic counters and ON rows positive counters (repro-8x8-50-off.txt, repro-1x1-50-on.txt). The 8x8 margin to the 24.5 ms stop is 0.19754 ms. The stale-provenance probe passes the gate; that is recorded as S1, a suggestion outside frozen scope, and the head receipt itself is correct. | R352-2 | d02db63c367daf9adc7d709840bd81077e781d80 |
| Tests | CLEAN | Independent re-execution of the capture harness at the head: 1x1/50/ON 16/16 rows equal plus `run.py` grader pass; 8x8/50/ON 3/3 and 8x8/50/OFF 2/2 rows equal, including the OFF-arm maximum row; all six build-input hashes equal (repro-*.txt, compare_rows.py). `check_nvm_capture.py` rc 0 plus 4 controls. `measure_test_evidence.py --check` rc 0; `check_port_contracts.py` rc 0 (gates.tsv). F1 is closed. | R352-2 | d02db63c367daf9adc7d709840bd81077e781d80 |
| Docs | CLEAN | `CHANGELOG.md:36-49`, `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1591-1630,1772-1780`, `PP_DESCRIPTOR_OWNERSHIP.md:1-5,55-58,132-139,242-247,296-302`, `SUBMODULES.md:55-73` and `nvm_capture_cpu/README.md:136-137` (Verilator 5.052 still true). Section 18 table recomputed from receipt rows (6/6 verbatim). External links verified read-only. At the head, these docs gates return rc 0: docs_check, check_doc_style, check_submodule_docs, check_doc_paths, check_archive, check_diagram_pngs, submodule_boundaries `--check`, gen_toc `--check`/`--verify-anchors`, check_em_dash `--base 682ecf0c` and `--base 499b15f9`, and `git diff --check` against both bases (gates.tsv). A stale-sentence search for `831f94f4`/`0922e434`/`2026-09-26` finds only historical entries plus S2. F1 and both round-1 suggestions are closed. | R352-2 | d02db63c367daf9adc7d709840bd81077e781d80 |

All five lenses are covered clean by R352-2 at the exact head `d02db63c367daf9adc7d709840bd81077e781d80`. S1 and S2 are SUGGESTIONs and do not affect coverage.

## Real limits

- **8x8 arms not fully reproduced.** The reproduction was bounded by the foreground rule, at about 10 minutes per step. A full 8x8 arm needs about 50 minutes of simulation, so I reproduced only its leading rows. The 8x8 contract maximum row (ON index 13, 2,430,246 ticks) and the two 100 MHz arms were not re-simulated here. Their equality rests on the author's run plus the determinism shown by 21/21 reproduced rows and identical build inputs.
- **Timeouts.** The two 8x8 native runs ended at the timeout (rc 124) after the rows listed. The 1x1 run needed a second native invocation of the same build (the first timed out at 14 rows), and the second completed with rc 0.
- **Simulator path.** The assigned 5.050 launcher path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist. I used no suite simulator. The capture used the host Verilator 5.052 build, which is the version the receipt and README record. I did not rerun pp_shadow, milan_dp, the builder banks, the OOC/Yosys ROM check or any full bank. The delta touches none of their inputs, and they were covered at ancestor `499b15f9` in R352-1 and by the manager's source banks.
- **Markdown gates.** Four gates need the pinned Markdown renderer. I ran them with an existing pinned environment, without installing anything (`$MD_PYTHON` in gates.tsv).
- **Tracked-file rewrite.** The capture build rewrote two tracked generated headers (`configs/generated/*/gen/adp_shape_defaults.svh`) with identical bytes. I removed the ignored outputs afterwards.
- **Shared installs.** A marker-file check found no writes by these runs to the shared SDK or LiteX trees. The only newer files there belong to an unrelated concurrent board build.
- **Hosted CI.** At snapshot time (`receipts/hosted-snapshot.tsv`), no check runs or statuses were registered for the exact head. I observed no hosted evidence.
- **Physical calibration.** Physical calibration was NOT RUN, field skips are not hardware proof, and no hardware was used. The capture numbers are CPU simulation evidence only.
- **Out of scope.** The 8x8 zero-cluster non-conformance with Milan §5.3.3.8 is pre-existing product behaviour, owned by open parent #584 under the recorded decision. This PR changes only its wording. It is neither introduced nor resolved here.

## Clone restoration

After all probes (`receipts/restoration.txt`):

- HEAD is `d02db63c`, and the HEAD tree and index tree are both `b13027cb`.
- `git diff HEAD` is clean after a full refresh. Status, including ignored files, lists 0 entries.
- All 926 tracked blobs re-hash to their index ids. There are no exec-bit mismatches and no assume-unchanged or skip-worktree flags.
- Gitlinks: `protocol-processor` `16be6768`, `gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e`, all checked out clean. `external` is uninitialised, as at start.

## Pending manager duties

- Exact-head hosted contexts and the act replica. None were registered at snapshot.
- Candidate merge validation against live dev `9e9954e9` (source base `682ecf0c`) at the merge turn.
- Deciding whether S1 becomes a separate Issue.
- The completion ledger's other bullets, and maintainer merge authorization.
- #584 acceptance item 2 ("D8 and `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` are updated, with the processor #122 disposition linked") is now partly satisfied on the ownership page by this PR, under decision 5857045698. When the #584 lane corrects D8, it must also retire the present-tense "violate" statements (`PP_DESCRIPTOR_OWNERSHIP.md:58,137-139,245`, `SUBMODULES.md:69`, `CHANGELOG.md:42`). This is not a defect here; it is a lane-coordination note.

## Other prior public findings on this PR (read after the verdict above)

I read the external round-1 report (R353-1, POSITIVE at `499b15f9`) after this verdict and ledger were written. It has two SUGGESTIONs, and neither changes the verdict.

- **R353-1 S1 (SUGGESTION; Docs, Tests): resolved.** This is the same subject as R352-1 F1: `processor_pins` described a different tree from `base`. At this head `base`, `tree` and `processor_pins` describe one measured tree (point 1). The receipt defines the fields' meaning at `measurements.json:320` ("base, tree and processor_pins identify the source measured by all six runs"). I reproduced the measurement at that tree (point 2).
- **R353-1 S2 (SUGGESTION; Docs): resolved.**
  - A #584 pointer now stands beside each cluster-minimum sentence: `SUBMODULES.md:68-70`, `CHANGELOG.md:41-43` and `PP_DESCRIPTOR_OWNERSHIP.md:58,245`.
  - The stale "must disposition it under PP60" sentence and the processor-owned F5 row were replaced (`PP_DESCRIPTOR_OWNERSHIP.md:134-139,245`).
  - The wording matches processor #122 comment 5853884588.

R352-2 FINISHED
