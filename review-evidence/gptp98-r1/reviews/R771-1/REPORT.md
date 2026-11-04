[R771] NEGATIVE - exact head 5b10675c3a22acc85bad7c150e1cd25984928385

# R771-1 independent review: FPGA-gPTP PR #99 / issue #98

- Reviewed head: `5b10675c3a22acc85bad7c150e1cd25984928385`, tree `405ab40b58cc53d6b57d819d83616c8c1b4d3fc7` (verified in the isolated clone).
- Base: `3e3a4e7695ce66eed609089f280c2fba45b24d36` (main), four commits `434527a`, `dbe1acb`, `6f3f003`, `5b10675`.
- Parent context: milan-fpga dev `604899c08ff1cd1830e1dd08b733109ef852400c`, pinning gptp-processor at `135afd04`.
- Role: internal independent reviewer, cleared context. I read no private author material and no other reviewer's report. Before this pass, PR #99 had no public review findings. Its only comments were the two review-start notices.

## Verdict summary

The RTL change is correct against the clauses. I found no conformance, RTL or robustness defect. On their own reruns at this head, the parser suite, the arm, the repo gates and the focused parent gates are all green.

The verdict is NEGATIVE because of one open MINOR in the Tests lens. One of the new harness rows, "#98 unknown TLVs after", is the only check that guards the PR's stated "a well-formed trailing TLV is still accepted" behaviour. It is also the only check for a walk that ends on a complete zero-length header at exactly messageLength. No mutant in the arm names that row. Two single-edit parser defects I planted are caught by that row alone. Two RESIDUE wording items and three SUGGESTIONs are also recorded.

## Reconstruction (order followed)

1. The repository has no AGENTS.md or CONTRIBUTING.md. I read `README.md`, `docs/README.md` (truth order: RTL, then executable tests, then guides) and `docs/MANAGER.md`.
2. Issue #98: the body holds the frozen acceptance items 1 to 4. The comments hold only the take and review-ready notices, with no added scope decisions. The PR #99 body and its two review-start comments.
3. Authorities applied:
   - IEEE 802.1AS-2011 11.4.1 (ignore a TLV the receiver cannot parse and attempt the next).
   - 11.4.4.3 and Table 11-10 (information TLV: tlvType 0x0003, lengthField 28, organizationId 00-80-C2, organizationSubType 1, field offsets).
   - 10.5.2.2.4 and 11.4.2.2 (messageLength counts every octet through the last octet of the last TLV).
   - Table 11-9 (76-octet Follow_Up minimum).
   - IEEE 1588-2008 14.1 (TLV skip by lengthField) and 5.3.8 / 14.1 (TLVs are an even number of octets).
4. `git diff 3e3a4e7..5b10675` and the history, file by file.
5. Public evidence at milan-fpga `b5042b8e` `review-evidence/gptp98-r1` (receipts, parent runs, area and timing reports, cycle trace). There are no manager evidence comments on the issue or PR yet.

## Clause and RTL analysis (`hdl/wire/KL_gptp_rx_parser.sv`)

- **Start of the walk.** At frame byte 57 (`OFF_TS_NS_END_C`, last preciseOriginTimestamp octet) the walk arms `tlv_hdr_run_r` (:566-569). PTP octet 44 is therefore frame byte 58.
- **Header bytes** count only while `cnt_r <= msg_end_r` (:365-366). Physical padding is never read as a header.
- **At each header end** (:573-584):
  - `fu_tlv_header_bad_w` (:374-376) refuses an odd lengthField, or a value whose last octet `cnt_r + len` lies past `msg_end_r`. The widths are 17-bit, so there is no overflow at lengthField 0xFFFE.
  - A zero-length TLV re-arms the next header.
  - Any other TLV loads `tlv_left_r` and is skipped by its lengthField. This meets acceptance item 1 and 1588 14.1.
- **Matching the information TLV.**
  - `fu_info_r` is set only when tlvType is 3, lengthField is 28 and no TLV matched before.
  - `fu_found_r` needs the TLV's own octets 4..9 to equal 00-80-C2 / 00-00-01. That compare runs at `tlv_left_r == 23` (TLV octet 9).
  - Word 11 is written at `tlv_left_r == 17` (TLV octet 15), from octets 10..15 as `{csro, tbi, 16'd0}`. This is the Table 11-10 layout and the w11 map at :101.
  - I checked the countdown by hand: octet k arrives with left = 32 - k.
- **End of frame** (:706-708): the Follow_Up needs `fu_found_r`, no header overrun on the EOF byte itself, and no cut header.
  - `fu_tlv_cut_after_w` (:379-381) covers a header cut after one to three octets, padded or not. With padding, `tlv_hdr_pos_r` stays non-zero.
  - It also covers a chain ending on a complete header or a complete value at exactly messageLength.
  - A value cannot be in flight at EOF on an accepted frame, because `cnt_r >= msg_end_r` is already required.
- **Registers.** The walk shares `tlv_hdr_run_r`, `tlv_hdr_pos_r` and `tlv_left_r` with the Announce chain. Every Announce term is gated on `MT_ANN_C` and every Follow_Up term on `MT_FU_C`. `mtype_r` is fixed from byte 14, and SOF clears all walk state (:460-465).
- **Datapath.** There is no frame buffer; two flip-flops are added (`fu_info_r`, `fu_found_r`). The bank lane has no conflict: the earliest walk write is frame byte 73, after the fixed writes at bytes ≤ 57.
- **Conformance of the refusals.** Every refusal is of input that 802.1AS-2011 / 1588-2008 do not let a conformant sender emit:
  - no information TLV;
  - a TLV or header past messageLength (11.4.2.2);
  - an odd TLV length (1588-2008: TLVs are an even number of octets);
  - a 00-80-C2/1 TLV whose lengthField is not 28 (11.4.4.3.3).
  
  So nothing 802.1AS-2011 requires to be accepted is refused. The behaviour change (base accepted a Follow_Up whose trailing chain was malformed) is disclosed in the PR body. It matches the existing Announce rule.
- **Comment rule.** I scanned every added line for bench lane labels, lane names, review rounds, reviewer IDs and issue-comment IDs. There are none. The new comments cite behaviour with #98 / #11 and clause IDs.

## Executed evidence (this review, pinned simulator 5.050, identity verified by `--version`)

| Run | Result | Receipt |
|---|---|---|
| Parser suite, head | 473 checks: 473 PASS, 0 FAIL | `receipts/parser-head-run.log` |
| Parser suite, base | 378 checks: 378 PASS, 0 FAIL | `receipts/parser-base-run.log` |
| Parser mutation arm, head | 29/29 PASS: the unmutated control plus 28 mutants, each failing all named checks; all 13 #98 mutants caught | `receipts/parser-head-mutants.log` |
| Head harness + reviewer probe rows, head RTL | 536 checks: 536 PASS (473 + 63 probe checks) | `receipts/probes-head-rtl.log` |
| Same harness and probes, base RTL | 536 checks: 478 PASS, 58 FAIL; 31 failures are the PR's #98 rows (matches the PR's "31"), 27 are my probes | `receipts/probes-base-rtl.log` |
| Reviewer-planted mutants against the unmodified head harness | see finding F1 | `receipts/reviewer-mutants/` |
| Repo gates at head: `make contract`, `docs` (127 arms), `diagrams-check`, `lint`; engine run; ucpu; gaskets; `bench/arty test`; tsngen | all rc 0. Tallies: engine 2048 + 60, ucpu 768, gaskets 81 + 5, tsngen 288 + 4 (executed, not skipped) | `receipts/repo-head/` |
| Scratch parent `604899c0` with the gptp-processor gitlink **staged** at `5b10675c` (no commit): `check_py_idiom.py` | rc 0 (long function 9 <= 9, unannotated public 0 <= 0) | `receipts/parent-head/py_idiom.*` |
| same: `make -C tb/verilator/milan_dp gptp` and `gptp-lat` | 210/210 and 210/210, rc 0 | `receipts/parent-head/milan_dp_gptp*.log` |
| same: `make -C tb/verilator/gptp_shadow` | suite 325/325 PASS. Its mutation lifecycle then refused: "required dependency gitlinks differ from HEAD". It needs a committed gitlink and I make no commits. The author's receipt shows controls 9/9 with a committed local parent `09d163f9` | `receipts/parent-head/gptp_shadow.log` |
| Control: gitlink at plain main `3e3a4e7` | `check_py_idiom.py` rc 1: "long function 10 > ratchet 9", "unannotated public function 3 > ratchet 0", exactly as the PR states | `receipts/parent-controls/py_idiom_main3e3a4e7.*` |
| Parent imported gPTP documentation gate (`check_gptp_docs.py --with-submodule`, CI-bound in `scripts/ci_events.py:820`) at head gitlink | rc 1. All 35 findings are parent donor deep links still pinned to `135afd04`. `--selftest` also rc 1 ("production donor links failed"). Both are rc 0 at the dev pin, so the failure is pin drift that comes with any gitlink move. `make -C gptp-processor docs` rc 0 | `receipts/parent-head/check_gptp_docs_*`, `receipts/parent-controls/*devpin*` |

### Reviewer probe rows (all pass at head; `scripts/r771_probes.cpp`)

- A 00-80-C2/1 TLV with lengthField 30, and one with lengthField 26, each alone: refused, one drop. Lengthfield 30 followed by a real information TLV: accepted, word 11 from the real one.
- Two information TLVs, the first in front: word 11 comes from the first.
- Zero-length TLVs in first position, and between the information TLV and a zero-length TLV that ends at exactly messageLength followed by padding: accepted.
- Unknown TLV with lengthField 0xFFFE: refused.
- An information TLV only in padding past messageLength: refused.
- messageLength 1500 with a 1420-octet unknown TLV first or last: accepted, words intact.
- Frame cut 6 octets short of messageLength: refused. An odd trailing TLV after the information TLV: refused. rx_err on the gmTimeBaseIndicator byte behind an unknown TLV: refused once.
- Back-to-back frames with no idle cycle (refused cut chain then unknown-first, unknown-first then Announce, Announce then unknown-first): events, words and drops are exact.
- **Timing.** The event lands 1 cycle after the EOF edge for the plain case, unknown-first, padded, and with an idle cycle between every byte. The per-byte timing is kept, which agrees with the author's cycle-trace receipt (`probe/trace.diff` differs only on the unknown-first frame).

## Evidence cross-check (published receipts)

- **Area and timing.** The PR tables match the receipts exactly:
  - Out of context: engine 4,926/3,459 → 4,920/3,461; parser 927/302 → 921/304; WNS 2.249 ns at both.
  - Placed: 4,876/3,459/1,634 slices/912 → 4,874/3,461/1,634/907; WNS 0.506 → 0.513 ns.
  - The worst path starts and ends in `u_ucpu` at both heads, and both area logs hold 0 critical warnings.
- **Parent receipts.** Each `parent-head-A` command is rc 0, and the xvlog log states "gptp-processor@5b10675c". The commands cover cpp/py idiom, xvlog, RTL source lists, builder test, gptp_shadow 325/325 with controls 9/9, port contracts, naming, test evidence, docs_check, lint, milan_dp `gptp` 210/210, `gptp-lat` 210/210, gm_steps 6/6, gptp_plane, gptp_txts, gptp_tables, and tsn_fuzz `ptp` 675/0. `parent-head-B` `milan_dp_gptp` reports RESULT PASS, with an empty lines-vs-base diff.
- **Engine arm.** The engine mutation arm receipt (136/136) is from `6f3f003`. I verified that `hdl`, `tb`, `syn` and `bench` tree IDs are identical at `6f3f003` and `5b10675` (`360f2459…`, `3a468eca…`, `388abf2d…`, `d176bcf0…`).
- **Fourth commit** (`5b10675`). Outside `selftest`, `check_docs.py` changes only three return/parameter annotations (`load_generator`, `constant_findings`, `copy_findings`). The 42 failure messages are identical and in the same order, the arm count is 41 increments either way, and the selftest gives "PASS (127 arms)" at both. The four doc edits repoint the `selftest()` link to the new module and add its Test-developer row. That is what the parent idiom gate needs and nothing more.
- **Hosted checks.** None are reported for this head (the hosted check list is empty; the combined status is pending with no contexts).

## Findings

### R771-1-F1: MINOR (Tests)

- **Where:** `tb/verilator/parser/mutants.py:293-358` (the #98 block of `MUTATIONS`; `FU_FIRST` at :164 omits the row) and `tb/verilator/parser/sim_main.cpp:914` (row "#98 unknown TLVs after").
- **Authority:**
  - The review focus (3): each new harness row has a parser mutant caught by name.
  - `tb/verilator/parser/Makefile:22-26`, Rule 8: prove the #98 Follow_Up TLV walk checks are load-bearing.
  - `docs/TEST_DEVELOPER.md:121`: "Proves each acceptance through a planted defect."
  - The PR body's behaviour-change note: "A well-formed trailing TLV is still accepted."
- **Evidence:** No mutant in the arm names "#98 unknown TLVs after" (the PR body calls it the control). I planted two defects and built each against the unmodified head harness (`scripts/reviewer_mutants.py`, `receipts/reviewer-mutants/`). Each fails exactly 2 of 473 checks, both "#98 unknown TLVs after: event" and ": no drop":
  1. A complete TLV header that ends on the last declared octet is read as a cut. This edits `fu_tlv_cut_after_w`, `KL_gptp_rx_parser.sv:379-381`.
  2. A zero-length TLV after the information TLV refuses the Follow_Up (`:580`).
- **Impact:** The boundary "walk ends exactly at messageLength on a complete header" and the trailing-chain acceptance are checked, but the arm does not prove them. This is the class of check Rule 8 exists to prove.
- **Required outcome:**
  - Add a named mutant to `MUTATIONS`, for example defect 1, whose checks are "#98 unknown TLVs after: event" and "#98 unknown TLVs after: no drop".
  - Update the defect counts in the Makefile comment, the `mutants.py` docstring and the PR body.
- **Verification:** `make -C tb/verilator/parser mutants` reports the new mutant caught on both named checks with the control passing, and `make -C tb/verilator/parser run` still reports 473/473.

### R771-1-R1: RESIDUE (Docs)

- **Where:** `tb/verilator/engine/sim_main.cpp:3423-3424` and `:3500`.
- **Evidence:**
  - "a 76-octet frame whose TLV type is 0x0008 (refused at the TLV header)": after #98 that TLV is skipped by its lengthField, and the frame is refused at the end-of-frame gate for lack of an information TLV.
  - ":3500 'the span of the whole Follow_Up TLV header arm'" names the fixed octet-44 arm that this PR removed.
- **Exact fix:**
  - Replace "(refused at the TLV header)" with "(refused at end of frame: the TLV is skipped and the chain holds no information TLV, #98)".
  - Replace "the span of the whole Follow_Up TLV header arm" with "the span of the former fixed Follow_Up TLV header arm (octets 44..59, before #98)".

### R771-1-R2: RESIDUE (Docs)

- **Where:** `docs/HDL_DEVELOPER.md:44`, "The first information TLV accepts the Follow_Up."
- **Evidence:** The Follow_Up is accepted only if the rest of the chain is also well formed (`KL_gptp_rx_parser.sv:706-708`). `docs/TEST_DEVELOPER.md:120` and the RTL header state the refusals correctly.
- **Exact fix:** "The first information TLV supplies word 11; a malformed chain is still refused."

### R771-1-S1: SUGGESTION (Tests)

The arm has no refusal row for a 00-80-C2/1 TLV whose lengthField is not 28 when no proper information TLV follows. My probes show the RTL refuses it correctly. The lengthField term is already proven by the "#98 identifiers at octet 6" row. A dedicated refusal row would pin the 11.4.4.3.3 rule directly.

### R771-1-S2: SUGGESTION (Tests)

No mutant names "#98 plain fu" (the reference row). A word-11 offset defect (`FU_LEFT_AT_TBI_C` 17 → 15) is caught by it and by the existing "fu w11" check (`receipts/reviewer-mutants/w11_two_octets_late.log`). Naming it in such a mutant would prove the reference too.

### R771-1-S3: SUGGESTION (Robustness, pre-existing)

The 11-bit `cnt_r` wraps on a physical frame over 2047 octets. Head and base both refuse my 2100-octet-padding probe. This is outside the untagged 1514-octet integration boundary and not introduced here, so it is recorded for awareness only.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | RTL walk vs 802.1AS-2011 11.4.1, 11.4.4.3 / Table 11-10, 10.5.2.2.4, 11.4.2.2, Table 11-9; 1588-2008 14.1, 5.3.8; 63 probe checks on head and base RTL | R771-1 | 5b10675c3a22acc85bad7c150e1cd25984928385 |
| RTL | CLEAN | `hdl/wire/KL_gptp_rx_parser.sv` full read; register sharing, widths, bank-lane timing, EOF gate; OOC/placed reports; event-latency probe; comment-rule scan of the delta | R771-1 | 5b10675c3a22acc85bad7c150e1cd25984928385 |
| Robustness | CLEAN | Boundary probes (0xFFFE length, padding-only TLV, 1500 messageLength, truncation, rx_err in walk, back-to-back with no idle cycle, idle-cycle gaps); parent milan_dp gptp/gptp-lat and gptp_shadow reruns | R771-1 | 5b10675c3a22acc85bad7c150e1cd25984928385 |
| Tests | UNCLEAN (F1) | `sim_main.cpp` #98 rows, `mutants.py` arm (29/29 rerun), base 378 / head 473 reruns, base-RTL 31-failure reproduction, 3 reviewer-planted mutants | R771-1 | 5b10675c3a22acc85bad7c150e1cd25984928385 |
| Docs | CLEAN (RESIDUE R1, R2 carried) | `docs/*.md` delta, `SOURCE_EVIDENCE.md` anchors L439/L521 (both land on the cited lines), parser README / Makefile counts, fourth commit's `check_docs.py` / `check_docs_selftest.py` split, PR body tables vs receipts | R771-1 | 5b10675c3a22acc85bad7c150e1cd25984928385 |

## Real limits

- I did not rerun the engine mutation arm (12,152 s in the author's receipt). I relied on its `6f3f003` receipt and on the verified identical `hdl`/`tb` trees.
- I did not rerun `make ooc` or place-and-route; the area figures are checked against the published reports only.
- I did not rerun these parent gates: builder test, gm_steps, gptp_plane / txts / tables, tsn_fuzz, `milan_dp_gptp`, port contracts, naming, test evidence, lint, cpp idiom, xvlog. For them I relied on the author's `parent-head-A/B` receipts.
- gptp_shadow's mutation lifecycle did not run here: it requires a committed gitlink and I made no commit.
- No manager source bank exists at this exact head, and none is claimed. No hosted check ran at this head.
- Physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `3e3a4e7`, live dev `604899c0`), builder and native banks, and link the receipts on the PR.
- The parent gitlink bump must update the 35 parent donor deep links from `135afd04` to the new pin. The imported gPTP documentation gate (`check_gptp_docs.py --with-submodule` and `--selftest`) fails until it does.
- Run the parent duties for a `gptp-processor` pin change listed in the parent `docs/testing/TESTING.md:278` (`make -C tb/verilator/milan_dp_gm_steps gmstep-mutants`), and the gptp_shadow lifecycle with the committed gitlink.
- Carry R771-1-R1 and R771-1-R2 to the residue checklist.
- Hosted/act acceptance.

## Restoration

- I made no edits in the review clone; all builds ran on `git archive` exports under the packet's scratch directory.
- After the probes, HEAD is `5b10675c…` with tree `405ab40b…`, and the worktree and index equal HEAD. All 114 tracked blob hashes match the index (110 at mode 100644, 4 at mode 100755), and nothing is untracked or ignored (`receipts/clone-index-after.txt`). The repository has no `.gitmodules` and no gitlinks.
- The scratch parent is disposable and was left at its dev pin with the index reset.

R771-1 FINISHED
