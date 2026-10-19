[R661] NEGATIVE - exact head 53ac2e9d75ceb381c2d2b04854e760304d9ae43f

# R661-1 independent review: FPGA-gPTP PR #86 (#84, #85)

- Repository: Mister-M-alt/FPGA-gPTP, PR #86, branch `84-85-tu-pathtrace`.
- Exact head `53ac2e9d75ceb381c2d2b04854e760304d9ae43f`, tree `69618d639b4019c0c27d6b03cfae8f9d36830d8b`.
- Base main `43acfbcc` (includes #82). Two commits: #84 `4d6288e8`, #85 `53ac2e9d`.
- Round R661-1, internal independent reviewer, cleared context, own detached clone.
- Public review start: https://github.com/Mister-M-alt/FPGA-gPTP/pull/86#issuecomment-6259586498

## Verdict

NEGATIVE. The source change is correct. #84 publishes sync-ok during mastership, so the parent's tu is 0 there, and the Annex B.1.1 holdover still runs when a peer grandmaster is replaced. #85 publishes the received pathSequence plus thisClock. Every repository gate and the 72-arm mutation arm reproduce at this head.

Two kinds of defect keep the verdict negative:

- **F1 (MAJOR).** The parent companion is incomplete. Another parent suite, milan_dp `gptp`, builds this engine with the product option on. It asserts the received-only path at eight expectations, and all eight fail at this head. The PR says the companion "rides the next gptp-processor pin adoption", but it covers only gptp_shadow.
- **F2 to F4 (MINOR).** Three documentation defects in the delta or made stale by it: a stale ROM figure, an overgeneralised holdover claim, and a stale clause note.

No prior public review FINDINGS existed on this PR at review start. The only other PR comments are the two review-start notices.

## Reconstruction (in the required order)

1. Repository rules. There is no `AGENTS.md` or `CONTRIBUTING.md` in this repository. I read `README.md`, `docs/README.md` (truth order: RTL and generated microcode, then executable tests, then guides, then history), `docs/SOURCE_EVIDENCE.md`, `docs/MANAGER.md` (ROM budget rules), and the HDL, integration and test guides.
2. Issue scope:
   - Issue #84 body: tu on every AVTPDU while grandmaster. Done when: grandmaster counts as synchronised; the 0.25 s holdover stays; a sim case plus a mutant; parent consumer gates pass.
   - Issue #85 body: GET_AS_PATH omits thisClock. Done when: the path is the received path plus thisClock; it stays consistent at every #82 transition; direct and multi-hop cases with mutants; parent gates pass.
   - Manager assignment (issue #84 comment 6257168490) and the author's STOP.
   - The newest manager ruling (6259159680): land both with `parent-adoption-gptp_shadow-85.patch`, rerun the full parent consumer list (11/11), and say in the PR that the companion rides the next pin adoption.
   - The author's REVIEW READY at the same head.
3. Requirement authorities, as quoted by the issues and ruling:
   - IEEE 1722-2016 4.4.4.7 and 10.4; Milan v1.2 4.3.5.2 and Annex B.1.1.
   - IEEE 802.1AS-2020 10.3.9.23 and 10.3.13.2.4 f) 5); IEEE 1722.1-2021 7.4.41.
   - Parent interfaces at milan-fpga dev `e9cbb676`: `KL_ptp_clock_validity.sv` (tu = ~sync_ok | hold | disc; hold armed by a GM-id change), `KL_gptp_shadow.sv` (publication latched on commit), and `milan_datapath.sv:2040` (bit 3 drives tu).
4. `git diff 43acfbcc..53ac2e9d`: 12 files, +585/-122. History: two commits, author identity only, no attribution residue.
5. Public evidence, milan-fpga `948261df` `review-evidence/gptp84-r1`. I read the receipts, the INDEX, the patch, the rc files and the logs. I did not read the author handoff narrative.

## Findings

### F1 - MAJOR - Tests, Docs - the parent companion misses eight milan_dp received-only path expectations

**Artifact.** These expectations are in milan-fpga `e9cbb676` `tb/verilator/milan_dp/sim_gptp.cpp` (blob `b9f28d9f`):

| Line | Check name | Expected | At this head |
|---|---|---:|---:|
| `:984` | fabric live AS_PATH count is four | 4 | 5 |
| `:1044` | GET_AS_PATH full-tail wire length | 74 | 82 |
| `:1046` | GET_AS_PATH cdl | 48 | 56 |
| `:1048` | GET_AS_PATH count four | 4 | 5 |
| `:1403` | explicit one-entry fabric PathTrace serves count one | 1 | 2 |
| `:1414` | explicit one-entry GET_AS_PATH cdl | 24 | 32 |
| `:1416` | explicit one-entry GET_AS_PATH count | 1 | 2 |
| `:1450` | in-flight response remains wholly old count one | 1 | 2 |

The same `sim_gptp.cpp` is also built by the `gptp-lat` leg (`tb/verilator/milan_dp/Makefile:426-429`). Both legs are `PREFIX_CASES` of that suite's default `run` (`Makefile:557, 579-581`), and both elaborate this engine with `GPTP_PLANE_EN_P` at its product default.

The PR text that is affected:
- Status: "The companion rides the next gptp-processor pin adoption in milan-fpga".
- "Parent companion" section.
- Definition of done: "Full parent consumer list passes 11/11 ... with the parent companion (rides the next pin adoption)".

**Evidence.** Reviewer runs of the milan_dp `gptp` leg on committed-file snapshots of milan-fpga dev `e9cbb676`, with the pinned 5.050 simulator. Receipts are `receipts/parent_milan_dp_gptp_{devpin,base,head}.log/.rc`.

| gptp-processor tree | Result |
|---|---|
| `e4869fd0` (the parent's own pin) | 182/182, rc 0 |
| `43acfbcc` (this PR's base, adds #82) | 179/182, rc 2 |
| `53ac2e9d` (this head) | 171/182, rc 2 |

- The three base failures are `:825`, `:826` and `:835`. They come from #82's reset publication: the GM is thisClock from reset and arms the hold. They are present at base and are not this PR's (see manager duties).
- The eight additional failures at head are exactly the rows above. Each asserts the received-only path that #85 corrects. These are the same defect class as the four gptp_shadow rows the companion updates.
- The 11-gate list the author ran (receipts `parent-*/rc.txt`) does not include milan_dp. The builder's 103 gates do not run it either (`parent-adoption/builder/inventory.json`).

**Impact.** Adopting this head with only the published companion leaves the parent's milan_dp `gptp` and `gptp-lat` legs red on eight expectations each. So the PR's "rides the next pin adoption" claim is not sufficient as written. Issue #85's "the parent's consumer gates pass" holds only for the manager's 11-gate list, not for every parent suite that builds this engine.

**Required outcome.** Either of:
- Extend the parent companion, or add a second companion, with one row per expectation above. Each row should cite IEEE 802.1AS-2020 10.3.9.23 / 10.3.13.2.4 f) 5): count + 1, wire length and cdl + 8 bytes per added entry. Add a check that the served last entry is thisClock. Run milan_dp `gptp` and `gptp-lat` with it at this head, and update the PR body.
- Or record a manager ruling on the PR that milan_dp belongs to a separate adoption item, and narrow the PR's companion claim to gptp_shadow.

**Verification.** At this head plus the companions, milan_dp `gptp` and `gptp-lat` show none of the eight rows failing. The only remaining failures should be the three #82-attributed rows, unless their own companion is applied too. A planted "thisClock not appended" control should fail the new rows.

### F2 - MINOR - Docs - the ROM budget in the manager guide is stale

**Artifact.** `docs/MANAGER.md:103` ("Shipping usage: 1,013 of 1,024 words (98.9%).") and `docs/MANAGER.md:107` ("Only eleven words remain free").

**Evidence.** The generator's default image at this head reports "1024 words, 1015 real (99.1%)". At base it reports 1013 (98.9%). Receipt: `receipts/rom_usage.txt`. The #84 receipt-timeout leg grows from three words to five (`hdl/ucode/gen_gptp_ucode.py:2000-2006`), and SRTO moves from @187 to @249. The same guide says the packer needs a gap per leg, and calls this "Current ROM budget".

**Impact.** A current figure the manager guide relies on for ROM planning is wrong by two words. Nine words remain free, not eleven.

**Required outcome.** State 1,015 of 1,024 words (99.1%) and nine free words.

**Verification.** `python3 hdl/ucode/gen_gptp_ucode.py -o x.hex` prints 1015 real, matching the guide.

### F3 - MINOR - Docs - the holdover is claimed for every mastership commit, but it arms only when a peer grandmaster is replaced

**Artifact.** The claim appears in three places:
- `hdl/ucode/gen_gptp_ucode.py:1734-1737`: "the parent's tu falls once the holdover that this commit's grandmaster change arms has run (Milan v1.2 Annex B.1.1)".
- `tb/verilator/engine/sim_main.cpp:172-173`: phase 37 header, "the parent's tu is 0 there once its Milan v1.2 Annex B.1.1 holdover has run".
- PR body, #84 section: "The becoming-grandmaster commit still changes the published grandmaster identity, which arms the parent's 0.25 s holdover".

**Evidence.**
- Reset already publishes thisClock as grandmaster (`hdl/top/KL_gptp_engine.sv:831`). SELF rewrites the same value (S_CID is asserted equal to the ROM thisClock at `:872-873`).
- So the first mastership after reset, and mastership after a self publication (the asCapable drop of #82), commit no grandmaster change. The parent arms its hold only on a GM-id change, a discontinuity pulse or a PHC step (`KL_ptp_clock_validity.sv:188-201` at `e9cbb676`).
- A reviewer probe measured this. It instrumented a copy of the parent gptp_shadow harness at head plus companion (`scripts/tu_probe.py`, `receipts/tu_probe_padopt.log`). There were 4 mastership entries. Entry 2 (GM `00aaccfffe010204` -> thisClock) held tu = 1 for 120 cycles, which is the B.1.1 hold. Entries 1, 3 and 4 (GM already thisClock) had tu = 0 from the first master cycle.
- The behaviour itself is conformant: no grandmaster change and no time discontinuity. The B.1.1 hold on a real change is kept. `docs/INTEGRATION.md:552-554` already states it correctly ("Taking mastership from a peer ...").

**Impact.** Source and test comments, and the PR, make a clause claim (Annex B.1.1 holdover at every mastership) that is false on two of the four reachable BECOME paths. A maintainer could rely on a hold that does not exist.

**Required outcome.** Reword all three places to match `docs/INTEGRATION.md:552-554`. The holdover arms when mastership replaces a peer grandmaster. When the publication already names thisClock, there is no grandmaster change and tu falls at the mastership commit.

**Verification.** Reread the three places. No code or test change is needed.

### F4 - MINOR - Docs - a module note still calls the SlavePort pathTrace copy moot

**Artifact.** `hdl/ucode/gen_gptp_ucode.py:72-74`: "(d)'s pathTrace copy for a SlavePort is moot on a single-port end station: a slave port transmits no Announce ..., so the global array has no reader here."

**Evidence.** #85 now implements exactly that copy plus the thisClock append in the published path (`hdl/top/KL_gptp_engine.sv:722-730, 977-993`). GET_AS_PATH reads it (IEEE 1722.1-2021 7.4.41, parent `milan_datapath.sv:2143-2157`).

**Impact.** An unchanged clause note now contradicts the delta's behaviour and its clause claim.

**Required outcome.** Rewrite the note: the SlavePort pathTrace copy with thisClock appended is the published path (#85), read by GET_AS_PATH. Only the Announce transmit side has no reader on a single-port end station.

**Verification.** Reread the note.

### R1 - RESIDUE - Docs - phase order in the engine suite header

**Artifact.** `tb/verilator/engine/sim_main.cpp:168-174`.

**Defect.** The header lists phase 38 before phase 37. The suite calls 37 (`keep_sync_ok_in_every_master_cycle`) before 38.

**Exact fix.** Move the five-line `// 37      #84: ...` entry (lines 170-174) above the two-line `// 38      #85: ...` entry (lines 168-169).

This is wording only; no check changes.

### S1 - SUGGESTION - Tests - an out-of-threshold Pdelay verdict during mastership is not exercised

**Evidence.** Reviewer probe A (`scripts/probes.py`, `receipts/probes/probe_A-*.log`) clears sync-ok on the bad-delay asCapable fall (`hdl/ucode/gen_gptp_ucode.py:1970-1971`). The full engine suite passes with it (rc 0), so that probe survived.

The same defect on the two other asCapable-fall paths is caught by "#84 every master cycle publishes sync-ok":
- probe A2, lost responses (`:1540`);
- probe A3, the multiple-response cease (`:1491`);
- probe A4, an RTL mask on any asCapable-clear master.

The line is unchanged by this PR, and the published behaviour is right.

**Suggestion.** Add a master-side out-of-threshold Pdelay case so all three fall paths are graded.

## Lens ledger (reviewer-owned)

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | See below | R661-1 | 53ac2e9d75ceb381c2d2b04854e760304d9ae43f |
| RTL | CLEAN | See below | R661-1 | 53ac2e9d75ceb381c2d2b04854e760304d9ae43f |
| Robustness | CLEAN | See below | R661-1 | 53ac2e9d75ceb381c2d2b04854e760304d9ae43f |
| Tests | UNCLEAN (F1) | See below | R661-1 | 53ac2e9d75ceb381c2d2b04854e760304d9ae43f |
| Docs | UNCLEAN (F1, F2, F3, F4; R1 residue) | See below | R661-1 | 53ac2e9d75ceb381c2d2b04854e760304d9ae43f |

**Conformance.**
- #84: `prog_become` sets flags bits 1 and 3 together. The receipt-timeout mask keeps bit 3 exactly where bit 1 is set. Every handover to a peer clears both, in the GM-change commit. Parent tu = ~sync_ok | hold | disc.
- Measured tu during mastership: base had tu = 1 on all 11,465,716 master cycles; head plus companion had tu = 1 on 121. The B.1.1 hold is kept on the peer-to-thisClock change (120 cycles).
- #85: the received path of 1..7 entries is published plus thisClock (count + 1). 8 or more entries keep their first eight; an absent TLV keeps count 0. This agrees with the repository's own 802.1AS-2011 10.3.10.2.1 d) note.
- Clause citations checked against the issue and ruling quotations.

**RTL.**
- `KL_gptp_engine.sv:719-730` and `:977-993`: slot index pk = c-1 for count c; inactive slots are zeroed.
- `gen_gptp_ucode.py:2000-2006`: the SRTO mask is correct over all 32 flag bits, because only bits 0..3 are ever written (every `e_flags` and `WRST RG_PUB|2` was audited).
- No `input`, `output`, `parameter` or `module` line changed. Lint is clean for the engine and the bench top.
- All four tracked images regenerate byte-identical.

**Robustness.**
- An SRTO expiry queued behind BECOME is handled, graded, and its planted mutant is caught.
- The parent latches publication on commit (`KL_gptp_shadow.sv:735-750`), so the raw write order inside BECOME is not observable.
- The pre-commit discontinuity edge at handover is seen as a single tu = 1 cycle (probe).
- The path-stage guard is intact. Reset and warm reset are covered by #82 checks.
- Reviewer probes B to H are all caught (`receipts/probes/probes_summary.txt`).

**Tests.**
- Engine suite at head: 1703/1703 on each of three passes and 53/53 on the priority1 255 pass. Base: 1642 and 46.
- Mutation arm: 72/72 caught through each arm's named checks, with 8/8 slice controls (`scripts/mutslices.py` over the suite's own `mutants.py`).
- New cases 8n, 19, 37 and 38 were read.
- Reviewer probes: 10 of 11 caught; S1 records the survivor.
- Parent gptp_shadow at base, head and head + companion: 309/309, 305/309 (exactly the four named rows), 310/310.
- Parent milan_dp `gptp` leg: F1.

**Docs.**
- The diff to `HDL_DEVELOPER.md`, `INTEGRATION.md`, `SOURCE_EVIDENCE.md` (anchors: 20 exact, 0 findings) and `TEST_DEVELOPER.md`.
- `MANAGER.md`, all source comments in the delta, the module notes, the PR body and the parent companion header.
- Comment rule: no bench lane labels, lane names, round or reviewer IDs, or comment IDs in any added line or commit message.

## Executed evidence (this round, exact head unless stated)

| Run | Result | Receipt |
|---|---|---|
| `make contract`, `make lint` (engine + bench top), `make docs` | PASS; docs: 11 current / 17 historical pages; diagrams: 9 pinned assets; source evidence: 20 exact | `receipts/head_light.log`, rc 0 |
| ucpu / parser (+9 mutants) / gaskets / tsngen (+4 mutants) / bench arty | 768/768; 337/337 + 9/9; 81/81 (+5/5); 288/288 + 4/4; PASS | `receipts/head_light.log` |
| Engine `make run`, head | 1703 ×3, 53 (p1 255) | `receipts/head_engine_run.log`, rc 0 |
| Engine `make run`, base 43acfbcc | 1642 ×3, 46 | `receipts/base_engine_run.log`, rc 0 |
| Engine mutation arm, head | 72 arms, 72 caught, controls 8/8 | `receipts/head_engine_mutslices/` |
| Reviewer fault probes (engine suite) | A survived; A2, A3, A4, B, C, D, E, F, G, H caught | `receipts/probes/`, `receipts/probes2/` |
| Image regeneration and ROM usage | 4/4 byte-identical; 1015 real at head vs 1013 at base | `receipts/rom_usage.txt` |
| Author receipts INDEX vs files | 194 rows = 194 files, 0 mismatches | `receipts/evidence_index_check.txt` |
| Parent gptp_shadow `make run` | base 309/309; head 305/309; head + companion 310/310 | `receipts/parent_shadow_*.log` |
| Parent tu probe (gptp_shadow copy) | base: tu = 1 on every master cycle; head + companion: tu = 1 on 121 master cycles (120 = B.1.1 hold on the one GM change, 1 = handover edge) | `receipts/tu_probe_*.log` |
| Parent milan_dp `make gptp` | devpin 182/182; base 179/182; head 171/182 | `receipts/parent_milan_dp_gptp_*.log` |
| Clone integrity after all work | HEAD, tree, index and all 107 tracked blobs and modes match; no gitlinks in this repository | `receipts/clone_integrity.txt` |

All probes ran on disposable copies under the packet's scratch area. The clone was never written.

## Reconciled author claims

- The engine figures (1703/53; base 1642/46), 72/72, the 11-gate rc files, gptp_shadow 305/309 to 310/310, the builder verdict digest (`8800c441...` at base, head and adoption), and "no port or parameter change": all confirmed.
- "Seven planted defects" for #84 counts six new arms plus one existing arm that now also names "#84 the run hands mastership to a peer". The mutation arm grew from 58 to 72: one obsolete arm removed, fifteen added.

## Real limits

- I had no copies of the standards. Clause wording was checked against the issue and ruling quotations and the repository's own clause notes.
- There are no hosted check runs or statuses at this head (zero contexts); none were inspected as executed.
- The full 11-gate parent consumer list was not rerun: it is not permitted here. It is accepted on the author's receipts, whose index I verified. I reran only the gptp_shadow `run` target (not its lifecycle or mutation targets) and the milan_dp `gptp` leg.
- `gptp-lat` was not run. It compiles the same `sim_gptp.cpp`, so the same rows are expected to fail.
- tsn_fuzz, gptp_plane, gptp_tables and gptp_txts were only read, not run.
- Parent snapshots were built with the pinned 5.050 simulator, not the parent's CI image.
- No synthesis or out-of-context resource measurement of the RTL delta was made (not required by the acceptance). The `MANAGER.md` resource tables are dated measurements.
- Physical calibration NOT RUN. No hardware was used. Simulation is not hardware proof.

## Pending manager duties

- Rule on F1: extend the companion for milan_dp `sim_gptp.cpp` (both legs), or record that it is out of scope and narrow the PR claim.
- Track that the milan_dp `gptp` leg already fails 3 checks at base `43acfbcc` (`sim_gptp.cpp:825, 826, 835`), against 182/182 at the parent's pin `e4869fd0`. This comes from #82's reset publication and is outside this PR, but it will meet the same pin adoption.
- Current-dev merge-candidate validation (builder and native banks) at the merge turn, on live dev `e9cbb676`. No manager source bank is claimed or inferred here.
- Hosted and act acceptance. Carry R1 to the residue checklist.

R661-1 FINISHED
