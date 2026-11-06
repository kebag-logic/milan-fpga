[R780] NEGATIVE - exact head cc92e90a95376151a9ebd484c429bc53feb8573c

# R780-1 external independent review: processor PR #215, issue #214

Head `cc92e90a95376151a9ebd484c429bc53feb8573c`, tree `4bffe18ed6a77686aad76d7fbef49316f42f7379`. Source base `a9e84b66`. `92100657` (PR #213) is merged in, so this issue's own delta is `9210065..cc92e90`, and that is the delta examined line by line.

## Verdict

**I found no RTL defect. The fix does what the issue asks. The verdict is NEGATIVE because of four MINOR test gaps.** Eight faults planted in the new encoder lines pass both repository suites. Two lose an MVRP attribute event, and one brings back the issue's own symptom, a value twice in one MRPDU. No RTL change is needed; the required outcome is new checks. F1 and F2 are from my own pass. F3 and F4 are retained from the R779 report after I reproduced them.

| Question from the brief | Answer | Evidence |
|---|---|---|
| Can a doubled Domain or VID vector occur after a LeaveAll? | No failure found | Randomized differential runs: 45 of 45 clean, 358,159 MRPDUs, 0 doubled, at table depths 2, 3, 4, 8 and 12. The same harness on the base encoder found 1,592 doubled frames in one 300,000-clock run. `tb/srp_top` OV0 to OV10 pass at head |
| Is an attribute event lost by merging? | Not in the RTL, but the benches would not notice | Those runs compared every MRPDU, value by value, with a model written from the 10 §3 table: 0 mismatches over 350,677 merges. See F1: a planted loss of an MVRP Lv passes 8683 of 8683 and 692 of 692 |
| Is the defect reproduced without the fix? | Yes, at the PR's figures | Main's encoder with the head testbench: `8683 checks: 8675 PASS, 8 FAIL` (OV0 to OV7), 69 of 17,650 frames; encoder suite `692 checks: 644 PASS, 48 FAIL` |
| Is listener and talker behaviour from PR #213 unchanged? | Yes | No file under `hdl/` other than the encoder differs from main. The only FAIL lines with main's encoder are the eight OV rows, so PS and LK rows pass either way |
| Is 802.1Q-2022 clause 10 cited correctly? | Yes | Each cited clause read in the 2022 text; see Conformance |
| Is the interpreter evidence acceptable? | Yes, with the limits below | See the interpreter section |

## Findings

### R780-1-F1: MINOR: an MVRP event lost by a merge passes every suite

- **Lenses:** Tests.
- **Location:** `hdl/srp/KL_srp_encoder.sv:465`, `:491-492` (MVRP rewrite), `:208` (MVRP identity); `tb/srp_encoder/sim_main.cpp:1585-1592` (PV9).
- **Authority:** the review focus "no attribute event is lost by merging"; 802.1Q-2022 Table 10-3 Lv! (AA and QA to LA, VN to LA) and 11.2.3.1.7 (VID range 0 to 4094); docs 10 §3 merge table.
- **Evidence:**
  - `rv-mvrp-hit-appends-addr` writes an MVRP merge to the append address, so the pending entry never changes. It reads `692 checks: 692 PASS` and `8683 checks: 8683 PASS`. The differential harness fails it at once: a VID owed Lv goes out as JoinIn (`receipts/mut/rv-mvrp-hit-appends-addr.fuzz-sample.txt`).
  - `rv-mvrp-key-low-byte` compares only the VID's low octet, so VID 2 and VID 258 merge and one VID's event disappears. It reads the same two passes. The harness with VIDs above 255 reads 0 errors at head and 360,605 under the arm (`receipts/fuzz-vid-high-byte.txt`).
- **Why the benches miss it:** PV9 pushes only New followed by re-joins and identical re-joins, so the rewrite is never observable, and every VID in both suites is below 256. No MVRP row merges an Lv or a New over another message.
- **Impact:** the head is correct, but a later edit could drop an MVRP withdrawal or merge two VIDs with the whole bank green. The case is reachable: `KL_srp_vlan` pushes Lv when the last user leaves (`hdl/srp/KL_srp_vlan.sv:268-274`), which can fall in the window of a pending New or JoinIn. I read this path; I did not drive it end to end.
- **Required outcome:** PV rows for MVRP JoinIn then Lv, New then Lv and Lv then New, and for two VIDs that differ only above bit 7, each with a planted arm in `tb/srp_top/mutants.py` that fails it by name.
- **Verification:** both arms above must fail by name. `scripts/reviewer_mutants.py` and `scripts/run_arm_encoder.sh` reproduce them.

### R780-1-F2: MINOR: four more behaviours of the new lines have no killing check

- **Lenses:** Tests.
- **Location and evidence**, each arm reading `692 of 692` and `8683 of 8683` (`receipts/reviewer-arms-encoder.txt`, `receipts/summary-tallies.txt`):

| Arm | Line | Behaviour left ungraded | Harness |
|---|---|---|---|
| `rv-value-keeps-oldest` | `KL_srp_encoder.sv:488` | the PR's stated rule that two Talker values of one StreamID merge to the newer one | 116 errors |
| `rv-fp-s-replaces-kept` | `:241` | 10 §3: a Listener entry takes the pushed declaration type when an In or Mt replaces an In or Mt | 47 errors |
| `rv-invalid-type-searches` | `:458` | the new `!valid_type_w` term: an unknown type offered while entries are pending must be dropped at once, not held until the table empties | 0 errors: my harness swaps the offer away, so this row is from reading the RTL |
| `rv-push-on-drain-start` | `:443` | a push on the clock a drain starts must wait; accepted, it is outside the snapshot and is lost. The guard predates this PR, which moved it into `base_ok_w` | 42 errors |

- **Impact:** each is a stated or load-bearing behaviour that a later edit could change unnoticed. `KL_srp_top` never offers an unknown type, so that row is a port contract rather than a wire risk.
- **Required outcome:** a named check and a planted arm for each. The fourth may instead be recorded as a pre-existing gap with a tracking reference.
- **Verification:** each arm fails by name.

### R780-1-F3: MINOR: nothing grades that one application's search leaves the other application's drain alone

- **Lenses:** Tests.
- **Origin:** R779 F-1, retained. I missed this arm in my own pass and reproduced it independently.
- **Location:** `hdl/srp/KL_srp_encoder.sv:460-463`, stated at `:425-426`.
- **Authority:** issue #214 acceptance 1; 10 §3 on the read port.
- **Evidence:** `rv-msrp-port-taken-by-any-search` removes the application term, so an MVRP search takes the MSRP read port during an MSRP drain. It reads `692 of 692` and `8683 of 8683`, while my harness finds 202 doubled frames in 400,000 clocks. The mirror arm `rv-mvrp-port-taken-by-any-search` is caught only by OV0, 1 of 8683 checks (`receipts/reviewer-arms-encoder-after-r779.txt`, `receipts/summary-tallies.txt`).
- **Impact:** the head is correct, but one edit to this term restores the issue's symptom with every gate green.
- **Required outcome:** a row that offers a value of one application, with that table non-empty, while the other application drains, in both directions, with a planted arm failing it by name.
- **Verification:** both arms must fail the new row by name.

### R780-1-F4: MINOR: the top octet of the StreamID identity has no check

- **Lenses:** Tests.
- **Origin:** R779 F-2, first half, retained and reproduced. Its second half is the first row of my F2.
- **Location:** `hdl/srp/KL_srp_encoder.sv:209`.
- **Evidence:** `rv-key-top-mac-octet-ignored` drops StreamID octet 0 from the identity and reads `692 of 692` and `8683 of 8683`. My harness also reads 0 errors, because its StreamIDs share that octet, so it gives no independent kill. Two streams differing only there would merge and one declaration would be lost.
- **Required outcome:** a row with two StreamIDs that differ only in the top octet, which must stay two values, with a planted arm.
- **Verification:** the arm fails the new row by name.

### R780-1-R1: RESIDUE: PR body overstates the header identity

- **Lenses:** none left unclean (wording in the PR body only).
- **Location:** PR body, "Its module header, parameters and ports, is byte-identical to main's."
- **Evidence:** `KL_srp_encoder.sv:101` changes the comment on `ev_ready_o`. The author's `IDENTITY.txt` says the identity holds with comments stripped, and says so correctly.
- **Exact fix:** "Its module header, parameters and ports, is identical to main's once comments are stripped; only the `ev_ready_o` comment changes."

### R780-1-R2: RESIDUE: the banner still calls the drain the only reader

- **Lenses:** none left unclean (comment wording only).
- **Origin:** R779 R-2, retained; confirmed by reading.
- **Location:** `hdl/srp/KL_srp_encoder.sv:76-77`. The next sentence adds the search as a second user of the read port.
- **Exact fix:** "(push is the only writer; the drain walk and the value search share the one read port)".

### R780-1-R3: RESIDUE: a new source comment shows a bench run label

- **Lenses:** none left unclean (comment wording only).
- **Origin:** R779 R-3, retained. My own comment-rule scan missed it because its pattern did not include run labels.
- **Location:** `tb/srp_top/sim_main.cpp:3422`, "(Run B, 10 §6.5)", added by `63ecbf5`. The file holds 2 instances at main and 3 at head, so this one is new in the delta; the older ones are tracked by #746.
- **Authority:** owner comment rule of 2026-10-15.
- **Exact fix:** "(10 §6.5)".

### R780-1-S1: SUGGESTION: record post-synthesis timing for the new ready path

- **Lenses:** RTL. This does not affect the verdict.
- `ev_ready_o` and the RAM read address now depend on a 73-bit compare fed by the intake mux. No receipt gives WNS at this head, and the acceptance asks only for area. `syn/ooc/srp_ooc.tcl` already reports it at the 100 MHz `P-CLK-HZ`. A logic-depth estimate of the encoder alone moved from 183 to 226 (`receipts/ltp-main.txt`, `receipts/ltp-head.txt`). That count is not a delay, and I draw no timing conclusion from it.

### R780-1-S2: SUGGESTION: record the area in the tree

- **Lenses:** Docs. This does not affect the verdict.
- Acceptance 3 is met by the PR table and `receipts/proc/area/`, whose figures I checked against the published stats. Issue #212 recorded its own cost in 10 §5.1; the same sentence for #214 would keep that record continuous.

### R780-1-S3: SUGGESTION: add a back-to-back search row

- **Lenses:** Tests. This does not affect the verdict.
- **Origin:** R779 S-1, retained at SUGGESTION.
- `rv-search-survives-accept` keeps the search running after an accept. It passes both suites, and my harness catches it with 363 doubled frames. It needs the same value offered on the clock straight after its accept. Reading the producers, none does this: the Domain queue's second entry is a different value and refills take a clock, and the VLAN and walk FSMs leave the push state between offers. A back-to-back row in `tb/srp_encoder` would close it.

## Lens results

### Conformance: CLEAN
Read in the 2022 text (the file's sha256 matches the author's `STANDARDS.txt`): 10.7.5.13 c), 10.7.6.1, 10.7.6.3, 10.7.6.5, 10.7.6.12, 10.7.7, Table 10-3, 10.8.2.10.1, 11.2.3.1.7, 35.2.2.7.2, 35.2.2.8, 35.2.2.8.1, 35.2.2.9.1. Every citation in the delta says what the delta claims.

I checked each merge rule against Table 10-3. Join!, periodic! and rLA! leave VN in VN, so New stays. LA with Join! is AA, so a join replaces Lv. New! and Lv! replace what was owed. An s replaces only an s. Identity by StreamID follows 35.2.2.8, which allows no FirstValue change for an existing StreamID, and AttributeType is part of the identity. One Applicant per Talker source and the issue #202 park mean a walk carries one message per value, so I found no route to an Lv and New of one StreamID with different FirstValues merging in normal operation.

### RTL: CLEAN
I reviewed the search for read-port ownership, restart on a changed offer, the first-clock stale read, hit and last against the count, the write mux, and the `E_COLLECT`, prepare and cross-application paths, at depths including powers of two. `lint_hdl.sh` passes on Verilator 5.050 (`LINT OK protocol_processor_top`). `ev_ready_o` now depends on `ev_valid_i`, but every producer's valid is registered, so there is no combinational loop. The doc's five-clock figure is measured: 5 clocks from tx! to the drain tick at 2x2 and 11 at 8x8 (`receipts/txgap-histogram.txt`).

### Robustness: CLEAN
The differential harness ran 45 of 45 clean with random transmitter backpressure, own and received LeaveAll, prepared rounds, unknown types and intake re-arbitration at 0, 5 and 30 percent. It accepted 1,513,847 events. The `onevec` group also passes at 2x2, 12 of 12, on a scratch build. The timer FIFO shapes 1x1, 2x2, 3x5 and 9x9 each read 15 of 15. A table full of pending values holds a push until it drains, as before and as documented.

### Tests: UNCLEAN (F1, F2, F3, F4)
Passing at head, run by me: `tb/srp_encoder` 692 of 692, `tb/srp_top` 8683 of 8683. The eight issue #214 arms are killed by name with their controls passing, 13 of 13, and `second-queueing` fails `OV1:` and `PV1 two re-joins of one Domain value` as acceptance 2 requires. Of 28 reviewer arms from my own pass, 22 are killed by a suite: 21 by the encoder suite or a hang there, and `rv-search-steals-drain-port` by OV rows at top only. The other six are F1 and F2. Of four more arms written after reading R779, one is caught by OV0 only and three survive (F3, F4, S3). The idiom gate's own scan of both suite sources reads 0 for every rule.

### Docs: CLEAN
The new 10 §3 text, the §5.1 row, the §6 notes and 09 §8.14 match the RTL and the measurements. `make check` passes on a clean clone, `gen_matrix.py --check` reads `94 rows, 0 untested`, and the README counts 8683 and 692 match my runs. My scan of the 1,259 added lines found no lane label, review round, reviewer ID or comment ID, but it missed one run label, recorded as R3. `git diff --check` is clean. R1, R2 and R3 are carried as RESIDUE. The 09 §8.14 row "the merge rule by rule ... MVRP" should be re-read once F1 lands.

## Interpreter evidence

I accept it. The published records are consistent with `INTERPRETER.txt`:

- 43 gates. The first 27 ran 11:06:35Z to 12:25:48Z, and the first bytecode time, 12:06:35 CET, is the start of `check_cpp_idiom`. The first 3.14 bytecode, 14:18:13 CET, falls 52 minutes after the last of those gates ended.
- All 14 gates that started later were discarded, 12 of them despite rc 0, and kept apart. Nothing that ran after `fw_shard3_srp` is cited from the first attempt.
- 16 gates, those 14 plus `milan_dp_mclk` and `milan_dp_render`, carry a `.python` record reading the pinned venv and 3.12.3 both before and after. `parent-rerun.sh` turns a mismatch into rc 97.
- A later manager comment on this PR gives the cause of the removal.

Limits of that evidence:

- The 27 earlier gates rest on an inference from bytecode times that I cannot re-measure, because the tree was cleaned. A script importing no parent module would leave no trace. `check_cpp_idiom` is dated by the matching start time and `fw_shard3_srp` by a 3.12 bytecode written during its run.
- "Rebuilt from the same pins" has no published package list.
- `milan_dp.log`, `pp_shadow.log` and `behave.log` are published by hash and tally line only.
- The scratch parent's two local commits are not public, so I could not re-run the consumer gates.

## Prior public findings

The only prior review on this PR is R779-1, posted while this review ran. Each item is decided at this head:

| R779 item | Decision | Here |
|---|---|---|
| F-1 MINOR, search against the other application's drain | Retained, reproduced | F3 |
| F-2 MINOR, identity width | Retained, reproduced | F4 |
| F-2 MINOR, newer FirstValue rule | Retained, found independently | F2 row 1 |
| R-1 RESIDUE, PR body byte identity | Retained, found independently | R1 |
| R-2 RESIDUE, banner "only reader" | Retained, confirmed | R2 |
| R-3 RESIDUE, "Run B" label | Retained, confirmed | R3 |
| S-1 SUGGESTION, restart after accept | Retained | S3 |
| S-2 SUGGESTION, area in the tree | Retained, found independently | S2 |

None is resolved at this head, because the head has not changed.

## Disclosure: exposure to the R779 report

The brief required my verdict and ledger to be written before I read any other reviewer's report. I did not fully keep to that. At 2026-11-06T21:07:27Z a listing command I ran to fetch prior PR comments printed the first 1,500 characters of the R779 report. That text gave its NEGATIVE verdict, its summary of two MINOR test gaps from planted encoder faults, and part of its answer table. It named no finding, arm or line.

I stopped there, and read the rest only after my verdict and ledger were on disk at 21:17:55Z. My F1 and F2 arms and results predate the exposure: the encoder-suite survivors are dated 20:32:34Z and the group runs 20:55:02Z (`receipts/independence-timeline.txt`). The full-run confirmation of three of those arms ended at 21:04:41Z, and the other three ran after the exposure. So the NEGATIVE direction was already supported by my own results, but I cannot claim I reached the verdict wording unexposed. Treat F1 and F2 as independent and F3, F4, R2, R3 and S3 as derived from R779. Two lines of my first draft were also corrected after the read: the Docs comment-rule statement, and the verdict count.

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | merge rules, identity, citations against 802.1Q-2022 clause 10, 11.2.3.1.7, 35.2.2 | R780-1 | cc92e90a95376151a9ebd484c429bc53feb8573c |
| RTL | CLEAN | `hdl/srp/KL_srp_encoder.sv` delta, its producers and intake, lint, tx-to-drain measurement | R780-1 | cc92e90a95376151a9ebd484c429bc53feb8573c |
| Robustness | CLEAN | differential harness, 45 runs at five depths, 2x2 `onevec`, storage shapes | R780-1 | cc92e90a95376151a9ebd484c429bc53feb8573c |
| Tests | UNCLEAN (F1, F2, F3, F4) | both suites, base reproduction, 8 author arms, 32 reviewer arms, OV and PV rows | R780-1 | cc92e90a95376151a9ebd484c429bc53feb8573c |
| Docs | CLEAN | 09 §8.14, 10 §3, §5.1, §6, suite READMEs, `make check`, comment rule | R780-1 | cc92e90a95376151a9ebd484c429bc53feb8573c |

## Real limits

- No hardware, and physical calibration NOT RUN. Field skips are not hardware proof.
- No Vivado on this host, so there is no timing or routed result.
- I ran no full sweep, no campaign beyond the eight issue #214 arms, and no parent gate. Those results are the author's receipts.
- The 28 per-arm README differences are taken as stated: identical at base. I confirmed only that the rows of the new arms match my run.
- The differential model is written from the 10 §3 table, so it shows the RTL matches the documented table. Table 10-3 agreement is a separate reading.
- My harness drives the encoder alone, and its StreamIDs share their top octet.
- Exposure: see the disclosure section.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `a9e84b66`, live dev `87e9d03aa2a4797957ac0124d0c7851a2eec234c`) and link the receipts. No manager source bank exists at this head and none is claimed here.
- Own hosted and act acceptance. At my last reading, `docs-gates` and `portability` had completed successfully twice each, and `suites` was still in progress twice (`receipts/hosted-check-runs.txt`).
- Carry R1, R2 and R3 to the residue checklist.
- Perform the real parent bump. The consumer gates ran on a scratch parent over `604899c0`.

## Receipts

`receipts/` and `scripts/` hold the results and the portable probes listed in `MANIFEST.sha256`. Raw logs that are large or carry host paths are not published; `receipts/RAW-RECORDS.txt` gives their size and sha256, and `receipts/summary-tallies.txt` gives their tally and FAIL lines. All probes ran in disposable copies under the packet's scratch directory.

The clone was not modified: HEAD `cc92e90a95376151a9ebd484c429bc53feb8573c`, tree `4bffe18ed6a77686aad76d7fbef49316f42f7379`, working tree and index clean, nothing untracked (`receipts/clone-final-state.txt`). The repository has no submodule gitlinks to verify.

R780-1 FINISHED
