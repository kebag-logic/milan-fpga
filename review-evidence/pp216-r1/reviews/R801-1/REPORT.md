[R801] NEGATIVE - exact head 60094a268c0df46703a3bee08c94118153634fd9

# R801-1 independent review: processor issue #216 / PR #218

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #218 (closes #216; parent issues kebag-logic/milan-fpga#860 and #857).
- Exact head `60094a268c0df46703a3bee08c94118153634fd9`, tree `4e9a67dac4d0d27d2a3022578e67d13ec1a7510f`; source base `044cb25f`. Six commits `f247533..60094a2`, 68 files, +2603 / -664.
- Reconstructed in a cleared context from: the repository README and `docs/README.md` (there is no AGENTS.md or CONTRIBUTING.md in this tree); the issue body and its two comments; the PR body; the review-start comment; IEEE 802.1Q-2018 10.7.6.2, 10.7.6.3, 10.7.7, 10.7.9, Tables 10-3/10-4/10-5 and 10.8.2.8 f), and Milan v1.2 4.2.7.1.1 Table 4.3, 4.2.7.2.1/2 (read against the RTL and against the stream FSMs' existing Table 10-3 transcription; the specification PDFs are not in the tree); the full diff and history; and the published evidence at kebag-logic/milan-fpga `8844ce1c` `review-evidence/pp216-r1`.
- No earlier public review findings exist on PR #218 (its only comment is the review start), so there is nothing to resolve or retain.
- The verdict is NEGATIVE because of one open MINOR finding (F01): a mutation count recorded in a row this PR adds is wrong. Everything else is clean. The conformance behaviour, the RTL and the acceptance arms all hold at this head, and the fix to F01 is a one-line README correction.

## Findings

### R801-1-F01 - MINOR - Docs, Tests

- **Where:** `tb/srp_encoder/README.md:255`, a row added by this delta (commit `3da1427`; the arm does not exist at `044cb25f`).
- **What it says:** `` | `vlan-rejoin-of-leaving-allocates`: a first user while the Lv is owed allocates a second entry | V10 | 7 FAIL — V10, W4, W5 (two), B1 (three) | ``
- **Evidence:** the campaign grades this arm at `failures=8`, both in my run (`receipts/camp_srp.log`) and in the author's head receipt (`head-60094a2/camp-srp/camp-srp.log`). The arm's raw log (`receipts/arm-vlan-rejoin-of-leaving-allocates.log`) has eight FAIL lines: V10 once, W4 once, W5 twice, and **B1 four times** ("B1 one Domain and one VLAN re-join bridged", "B1 VLAN frame captured", "B1-vlan: length", "B1-vlan: byte-exact"). `scripts/cmp_enc_readme.py` compares the 54 encoder README arm rows with the campaign; this is the only one that differs (`receipts/cmp_enc_readme.txt`).
- **Impact:** a published mutation record in this PR's own test documentation misstates a measured figure. That changes a figure, so it is not wording-only and is not RESIDUE.
- **Required outcome:** the row reads `8 FAIL — V10, W4, W5 (two), B1 (four)`.
- **Verification:** `python3 -I scripts/cmp_enc_readme.py <clone> receipts/camp_srp.log` reports `0 differ`.

### R801-1-F02 - RESIDUE - Docs

- **Where:** `docs/architecture/10_srp_engine.md:1116-1117` (§6.5, new text): "So the MVRP participant sends a LeaveAll every 10 to 15 s from Begin!, declaring or not (Milan v1.2 Table 4.3)."
- **Authority:** `docs/README.md` §2, single-source rules: "Timing values only in `F08.1`". A value copied outside its table is a review finding, and no gate reads values. The value itself is correct (T-MRP-LEAVEALL, `08_timing.md` F08.1 row "random 10–15 s"), so this is wording only. It changes no figure, test, code or clause claim.
- **Exact fix:** replace "every 10 to 15 s from Begin!" with "every `T-MRP-LEAVEALL` ([F08.1](08_timing.md#fig-08-constants)) from Begin!".
- This does not make the verdict negative and leaves no lens unclean. It goes to the residue checklist.

### R801-1-F03 - SUGGESTION - Conformance, RTL, Docs

- **Where:** `hdl/srp/KL_srp_vlan.sv:391` (a new entry's Registrar starts MT) and `:410` (an inactive entry in VO/AO/QO is discarded with its Registrar); `docs/architecture/10_srp_engine.md:495-496`.
- **Behaviour:** the VID Registrar exists only from the first user's join. A peer declaration of a VID received before that join is not kept.
- **Reviewer probe** (`scripts/probes/probe_tb.py`, `receipts/probe_probe216.log`): a peer JoinIn of VID 2 at about 300 ms, then DECLARE_TALKER on VID 2 at 800 ms. The participant sends `New@1001 New@1201 JoinMt@1401 JoinMt@2001 JoinMt@3001`, then after the peer's next JoinIn `JoinIn@4001 JoinIn@5001 JoinIn@6001`. A full participant holding Table 10-4 for VID 2 from the peer's JoinIn would read IN. It would go AN to QA by note 8 and answer JoinIn (10.7.6.3).
- **Why only a suggestion:**
  - The error runs in the conservative direction. JoinMt is never JoinIn without IN, and a real peer that receives the JoinMt moves its Applicant from QA to AA (Table 10-3 rJoinMt!) and declares again, which corrects it within about one T-MRP-JOIN.
  - The issue's defect (JoinIn with the Registrar MT) is gone.
  - §6.2 discloses the bound in so many words.
- **What remains is the citation.** "Table 10-3 note 11" supports discarding *Applicant* state in VO/AO/QO. It does not by itself cover dropping a Registrar that would be IN.
- **Suggested outcome:** record the bound as a tracked deviation, either in 00's gap register or in a follow-up issue, with a precise clause basis. A small "registered VIDs" set would remove it if the owner wants full Table 10-4 behaviour.
- **If the second reviewer or the manager reads 10.7.8 / note 11 as requiring that Registrar,** this becomes a MINOR conformance finding. The probe is the evidence either way.

## Focus items, against the clauses

1. **New on two tx!, then Join, for each Applicant: MET.**
   - `srp_pkg.sv:115-201` transcribes Table 10-3 row by row: New! to VN except from VN/AN; tx! VN→AN sN; AN→QA/AA by note 8 sN; AA→QA sJ; VP→AA sJ; LA→VO sL; LO→VO s; txLA! as tabled. Every row it implements is identical, cell for cell, to the stream FSMs' existing transcription (`KL_srp_talker_fsm.sv:238-359`).
   - The Domain (LINK_UP and adoption set VN, `KL_srp_domain.sv:297-315`) and each VID (`KL_srp_vlan.sv:240-282`) decide every message at a tx!.
   - Wire rows: AP1 (Domain), AP2 (VID 2) and AP4 (Talker Advertise and Listener Ready) require New, New, then JoinMt on three consecutive tx! 180-240 ms apart. `tb/pp_top` S1 checks the Domain New, New, JoinMt byte-exact.
   - My arms p1 (note 8 ignored: AN→QA always) and p3/p4 (periodic! ignored on Domain/VID) each fail AP1/AP2/AP7, AP1 and AP3 respectively.
2. **sJ follows the Registrar: MET for the Registrar the design keeps** (see F03 for values registered before allocation).
   - `srp_app_msg` gives sJ = JoinIn only with reg_in, else JoinMt; s = In/Mt.
   - The Domain Registrar follows Table 10-4 with Milan 4.2.7.2.2: register on New/JoinIn/JoinMt, Lv sets MT at once, rLA!/txLA! sets LV (encoded as MT). The adoption carries the pending value's Registrar.
   - The VID Registrar follows Table 10-4 as printed: rLv! to LV, rLA! and the own txLA! age it at the walk's start, and a received event wins its clock.
   - AP3 grades JoinMt with MT, JoinIn after the peer's JoinIn, and JoinMt after its Lv. Encoder V3 and VR1-VR11 grade it at unit level.
3. **LeaveAll with nothing declared, MVRP and MSRP: MET.**
   - An own MVRP expiry sets Active (`KL_srp_top.sv:1304-1308`, redraw at expiry). The next MVRP tx! (`:1218-1230`, every T-MRP-JOIN) is the sLA, with the txLA! walk.
   - A peer LeaveAll before or on that edge gives Passive (`:1221`, `:1320-1323`).
   - The encoder starts an MVRP drain for the LeaveAll alone (`KL_srp_encoder.sv:409-410`) and emits the existing LeaveAll-only message: NumberOfValues 0, a zero FirstValue (10.8.2.8 f).
   - AP5 (from Begin!, nothing ever declared) and AP6 (every declaration withdrawn) require the first LeaveAll within 15.5 s, then 9.5-15.5 s spacing, byte-exact LeaveAll-only MVRPDUs, and MSRP LeaveAlls in the same bounds carrying the Domain's txLA! sJ.
   - By construction the bound holds: a 10-15 s draw restarted at expiry, plus at most one T-MRP-JOIN to the tx!.
   - My arms p2 (sLA only while a VID is active) and p5 (timer not restarted after expiry) each fail AP5/AP6.
4. **MRP timers unchanged: MET.** No parameter, `_MS_P`, draw-range or F08.1 change appears in the delta (`docs/architecture/08_timing.md` is untouched). The `timers` group and the full `tb/srp_top` suite pass.
5. **Planted arms: MET.**
   - The three acceptance arms are `domain-one-new`/`vlan-one-new` (one New), `vlan-joinin-registrar-mt` (JoinIn with MT) and `mvrp-leaveall-needs-content` (LeaveAll stopped with the last declaration). Each plants a behavioural fault in the RTL, not a constant in the test. Each is killed by name at `tb/srp_top` (AP1; AP2; AP2,AP3; AP5,AP6) and at the encoder (D1; V1; V3; L7).
   - My full campaign: `350 checks: 350 PASS, 0 FAIL`, `assertion coverage: 184/184; missing=[]`, rc 0. Every arm/rc/failure-count line is identical to the author's head receipt.
   - The AP rows read the wire with timing bounds and an independent frame parser.
   - The five reviewer arms p1-p5 are all killed by the `applicant` group (`receipts/probe_p*.log`, rc 2 each).
   - The OV regrade (`push-twice-encoder-appends` replacing the two onevec gradings) is disclosed in 09 §8.14. Both encoder arms are still killed at PV1/PV2.
6. **10 §6.1 and F10.2 match the code: MET.**
   - F10.2's tx! edges, the §6.1 event table (periodic!, rLA!, rJoinMt/rMt, rJoinIn/rIn with note 5, rLv!, own sLA) and the "New, New, then JoinMt, then JoinMt at the tx! after each periodic!" ladder agree with `KL_srp_domain.sv:162-202` and the package rows.
   - §6.2/F10.3 (the LEAVING state, LA + New! = VN, LO owing s) agree with `KL_srp_vlan.sv`. §6.5 agrees with the top.
   - §5.1's area figures equal the author's area receipts: base 13,536/28,002/150/364 LUT, head 14,109/28,814/215/594.
   - Wording residue: F02.
7. **Parent consumer gates and twin: MET on the published receipts** (I did not re-run them; that is not allowed here).
   - `parent-60094a2/`: 40 `.rc` files, all 0. The pin log shows protocol-processor at `60094a268c0d…` on dev `ac0a01e3`, with the ROM digests re-recorded.
   - `twin-60094a2/twin-compare.txt`: the three owed rows `fabric-mvrp-leave-all`, `fabric-domain-one-new` and `fabric-vid2-join-in` each say "the defect has gone". The run's rc 2 comes from those three DIFF lines alone, and `entity-available-index` (#217) still holds as OWED.

**The author's two reported gaps:**

- **(a) The full sweep ran serially in one unit rather than as shards.** This is not a defect and not residue. It is an execution mode: the receipt shows rc 0 across 36 suites with `1032092 checks total, 0 failing`. I independently reproduced the four SRP-touching suites at the same counts: srp_top 8703, srp_encoder 1646, srp_stream_fsms 1512, pp_top 11066.
- **(b) Seven pre-existing `tb/srp_top/README.md` arm counts differ** (rows 287, 289, 300, 305, 397, 398, 399).
  - They are not residue, because they are figures, not wording.
  - They are not a finding on this PR: they are equal at the base (`pre-existing-counts/arm-base-stale.tsv`), the delta does not touch those rows, and the README's own prose at lines 443-447 already records the re-measured values. My campaign measures the same: 26, 8, 16, 21, 17, 7, 7.
  - They are out of scope and need a follow-up issue (a manager duty).
  - My cruder comparator (`receipts/cmp_top_readme.txt`) flags more pre-existing rows whose column meaning I did not establish. None of them was added or changed by this delta.

**Comment rule:** I scanned the added lines under `hdl/`, `tb/`, `scripts/` and `syn/`. The only ID-like tokens are figure IDs (F10.2, F10.3, F05.12) and test-row IDs (V10, D8, M11, B1). No bench lane label, lane name, review round, reviewer ID or issue-comment ID appears. No new instance.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `srp_pkg.sv:80-258` against every Table 10-3 row it implements and the talker FSM transcription; `KL_srp_domain.sv` Registrar/Applicant against Table 10-4 with Milan 4.2.7.2.2, 10.7.6.3, 4.2.7.2.1; `KL_srp_vlan.sv` Registrar against Table 10-4; `KL_srp_top.sv:1212-1323` against 10.7.9/Table 10-5; `KL_srp_encoder.sv:406-410` against 10.8.2.8 f); Milan Table 4.3 bounds; timers unchanged; F03 recorded as SUGGESTION | R801-1 | 60094a268c0df46703a3bee08c94118153634fd9 |
| RTL | CLEAN | the full HDL delta (domain, vlan, top, encoder, package): reset of every new register, same-clock event ordering, tx! owed/served/done handshakes, MVRP round coalescing, adoption vs tx! exclusion, link edges, the LA/LO entry lifetime; `scripts/lint_hdl.sh` LINT OK with Verilator 5.050; top port list unchanged; `hdl/adp`, `hdl/aecp`, `hdl/acmp` untouched | R801-1 | 60094a268c0df46703a3bee08c94118153634fd9 |
| Robustness | CLEAN | a full Domain queue (tx! owed, DT3), encoder/TX backpressure (OV10, AP7's eleven-entry search), peer LeaveAll on the sLA edge (Passive), join ticks during a running MVRP round (coalesced), LINK_DOWN/UP mid-round, Lv owed then re-join (V10), txLA! before a withdrawn VID's tx! (V11); suites srp_top 8703/8703, srp_stream_fsms 1512/1512, pp_top 11066/11066 | R801-1 | 60094a268c0df46703a3bee08c94118153634fd9 |
| Tests | UNCLEAN (F01) | AP1-AP7 source and wire oracles; encoder D/DT/DA/V/VR rows (D1 read in full); the delta's arm patches (the seven AP-graded patches read in full; every patch applied and graded by the campaign); full SRP campaign 350/350, coverage 184/184, identical to the author's receipt; five reviewer arms killed; one scenario probe; srp_encoder 1646/1646 | R801-1 | 60094a268c0df46703a3bee08c94118153634fd9 |
| Docs | UNCLEAN (F01; F02 residue) | 10 §3, §5, §5.1, §6.1/F10.2, §6.2/F10.3, §6.5; 09 §8.14, §8.15; `tb/srp_top`, `tb/srp_encoder`, `tb/pp_top` READMEs (#216 tables compared with the campaign: srp_top 12 of 12 equal, encoder 53 of 54 equal); MODULE_MATRIX; `make check` rc 0; `gen_matrix.py --check` `matrix: OK (94 rows, 0 untested)`; `git diff --check` empty; comment rule | R801-1 | 60094a268c0df46703a3bee08c94118153634fd9 |

## Gates I ran at the exact head

All gates ran in disposable clones of the head, with Verilator 5.050 verified (`verilator --version`: `Verilator 5.050 2026-07-01 rev v5.050`) and host Python 3.14 (CI uses 3.12.3). Receipts are under `receipts/`.

| Gate | rc | Result | Wall |
|---|---|---|---|
| `make check` | 0 | every docs, aecp-command, ids and figures gate OK | 226 s |
| `python3 scripts/gen_matrix.py --check` | 0 | `matrix: OK (94 rows, 0 untested)` | |
| `bash scripts/lint_hdl.sh` | 0 | every module `LINT OK` | |
| `git diff --check 044cb25f <head>` | 0 | empty | |
| `make -j4` in `tb/srp_top` | 0 | `8703 checks: 8703 PASS, 0 FAIL` (the FIFO-arm shapes first) | 1274 s |
| `make -j4` in `tb/srp_encoder` | 0 | `1646 checks: 1646 PASS, 0 FAIL` | 16 s |
| `make -j4` in `tb/srp_stream_fsms` | 0 | `1512 checks: 1512 PASS, 0 FAIL` | 78 s |
| `make -j4` in `tb/pp_top` | 0 | `11066 checks: 11066 PASS, 0 FAIL` | 3625 s |
| `python3 -B tb/srp_top/mutants.py --jobs 5` | 0 | `350 checks: 350 PASS, 0 FAIL`; `assertion coverage: 184/184; missing=[]` | 4607 s |
| reviewer arms p1-p5, `applicant` group | 2 each | each killed (AP1/AP2/AP7; AP5/AP6; AP1; AP3; AP5/AP6) | |
| reviewer scenario `probe216` | 0 | F03 behaviour, as printed above | |

The gates ran concurrently, in three sets, in separate clones.

After the probes I re-verified the reviewed clone (`receipts/clone-integrity.txt`):

- HEAD `60094a26…`, tree `4e9a67da…`
- `git status --porcelain --ignored` empty
- index entries (mode, blob, path) identical to `ls-tree -r HEAD`
- zero gitlinks: this repository has no submodules

**Hosted evidence at the exact head** (`receipts/hosted-checks-at-head.tsv`, read at 11:19Z): `docs-gates` and `portability` completed successfully on both the push and the pull_request runs, and both `suites` jobs were still in progress. This is observation only; the manager owns hosted and act acceptance.

## Real limits

- I did not run the full `scripts/run_suites.sh` sweep, `syn/yosys/run.sh`, `tb/elab_guards`, `check-req-tags.py` with executed evidence, the area flow, or the AECP campaigns. Full banks are not allowed here, and the HDL outside `hdl/srp` is untouched. For those gates I rely on the author's published receipts and the hosted jobs.
- I did not re-run the parent consumer gates or the twin (not allowed). Item 7 is judged on the published receipts only.
- I had no specification PDFs. Table 10-3/10-4/10-5 cells were checked against the clause structure, the quotations in the author's `STANDARDS.txt`, and the stream FSMs' existing transcription. I did not read the exact text of Table 10-3 note 11, which bears on F03.
- This is a source-head review. The current-dev merge candidate (base `044cb25f` against live dev `ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36`) is not covered, and no manager source bank ran at this head. Physical calibration was NOT RUN, and skipped field contexts are not hardware proof.

## Pending manager duties

- Carry F02 to the residue checklist.
- Decide F03's classification together with the second independent review.
- Open a follow-up for the pre-existing stale `tb/srp_top/README.md` counts (author's gap (b)).
- At the merge turn, build and validate the current-dev merge candidate (builder and native banks) and link its receipts.
- Own hosted and act acceptance (the `suites` jobs were in progress when read).
- On the parent side, delete the three owed twin rows when this head is adopted.

R801-1 FINISHED
