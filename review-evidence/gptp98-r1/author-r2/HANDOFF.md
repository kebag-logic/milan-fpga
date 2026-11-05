# [A730b] FPGA-gPTP #98 round 2: proof of the Follow_Up TLV walk — HANDOFF

Status: REVIEW READY at `762fbd6716b50337e7644a4918c216b3143aeb5b`. Every round-2 item is met. Every gate is rc 0 at this head: the repository set on a clean clone, both mutation arms in full (parser 35/35, engine 136/136), the docs gate under an isolated interpreter, `git diff --check` against `3e3a4e7`, and the scratch-parent consumer gates (milan_dp's `gptp` and `gptp-lat` legs and `gptp_shadow` included). `hdl/` is unchanged.

- Repository: Mister-M-alt/FPGA-gPTP (`git remote get-url origin` is `https://github.com/Mister-M-alt/FPGA-gPTP.git`). Branch `98-followup-tlv-walk`, PR #99. Nothing pushed.
- Base: main `3e3a4e7695ce66eed609089f280c2fba45b24d36`. The parent pins `135afd04`. `git diff --stat 135afd04 3e3a4e7` lists 14 files: Markdown (two of them the READMEs `tb/tsngen/README.md` and `tb/verilator/gaskets/README.md`), `scripts/check_docs.py` and `scripts/check_source_evidence.py`. No RTL, no test source and no build file changes.
- Round-1 head: `5b10675c3a22acc85bad7c150e1cd25984928385`.
- Round-2 head: `762fbd6716b50337e7644a4918c216b3143aeb5b`, tree `1354fd45`. Four commits on top of round 1 (no rebase, no force), one-line subjects, no body, no trailers:
  - `fc13a65` Check that a malformed TLV header ahead of the information TLV and a 30-octet one are refused, and name every Follow_Up walk row in a parser mutant (#98)
  - `a030c62` Describe the Follow_Up walk's word 11, refusals and parser defects in the guides and engine comments (#98)
  - `6e27cd6` Load the docs gate's fixture arms by their own path, so the selftest passes under an isolated interpreter (#98)
  - `762fbd6` Count the seven #87 and #88 parser mutants in the arm's docstring (#98)
- `hdl/` is unchanged in round 2: its tree is `360f2459` at `5b10675` and at `762fbd6`. No new row showed an RTL defect, so there is no STOP.
- Assignment: the [A10] round 2 comment on #98 (issuecomment-6640832434), from R771-1 (PR #99 issuecomment-6640825036) and R772-1 (PR #99 issuecomment-6640756256).
- Issue posts: TAKEN `#98 issuecomment-6640866717`. REVIEW READY at `762fbd67` `#98 issuecomment-6654446214`.
- Session note: a host reset at 22:19 on 2026-11-04 cut the previous session. The first three commits were already made and the tree was clean. That session's head-fast run at `6e27cd6` had finished rc 0 (`receipts/superseded-6e27cd6/`). Its engine-arm and parent runs were killed mid-run, and their partial results are not cited. This session added `762fbd6`, then reran every gate at that head.

## Authority (clauses read)

- IEEE 802.1AS-2011 11.4.1: the Follow_Up information TLV is the first TLV. A system that cannot parse a TLV ignores it and attempts the next one (IEEE 1588-2008 14.1).
- 802.1AS-2011 11.4.2.2: messageLength ends with and includes the last octet of the last TLV.
- 802.1AS-2011 11.4.4.3.2 to 11.4.4.3.5: tlvType 0x3, lengthField 28, organizationId 00-80-C2, organizationSubType 1.
- IEEE 1588-2008 5.3.8: the length of every TLV is an even number of octets.

## Items (assignment numbering) and where each is met

| Item | Change (file:line at `762fbd6`) | Clause |
|---|---|---|
| 1 R772-1 F1 rows | `tb/verilator/parser/sim_main.cpp:995-1003`: "#98 TLV past messageLength ahead of the information TLV" (`{0x000A, 0x0100}` with no value, then the information TLV, messageLength 80) and "#98 odd lengthField ahead of the information TLV" (`{0x000A, 0x0001}`, then the information TLV). Each expects no event, one drop and no w11 write (`expect_fu_refused(…, true)`). Comment at `:955-959`. | 11.4.2.2; 1588 5.3.8 |
| 1 latch mutant | `tb/verilator/parser/mutants.py:335-343` "a malformed TLV header does not latch the refusal (#98)" deletes `bad_r <= 1'b1;` under `if (fu_tlv_header_bad_w) begin` (`KL_gptp_rx_parser.sv:578`). It names the six checks of the two rows above. | 11.4.2.2; 5.3.8 |
| 1 split | `mutants.py:327-334` "a TLV value past messageLength is walked (#98)" now edits only the walk's header verdict (`:578` keeps only the odd term). It names the information-TLV and trailing overrun rows. The end-of-frame half is the existing "an EOF header's own overrun is not refused (#98)" (`:344-350`, the `:707` gate), named on the value-to-come row. Each fails only its own named checks (5 and 2, `receipts/parser/mutant-fails-98.md`), so each term is proven alone. The cut term is proven alone by "a TLV header cut by messageLength is accepted". | 11.4.2.2 |
| 2 R771-1 F1 | `mutants.py:176` `FU_AFTER`; `:397-402` "a complete header ending on the last declared octet is read as cut (#98)" (edits `fu_tlv_cut_after_w`, `KL_gptp_rx_parser.sv:379`); `:403-407` "a zero-length TLV after the information TLV refuses the Follow_Up (#98)". Each is caught on "#98 unknown TLVs after: event" and ": no drop", and the control passes. | 11.4.1; 11.4.2.2 |
| 3 S1 row and X3/X4 | `sim_main.cpp:1005-1011` "#98 information TLV with lengthField 30" (00-80-C2/1, Table 11-10 fields in place, two more octets, no other TLV): no event, one drop, no w11 write. `mutants.py:385-396` "the information TLV is named by any lengthField of 28 or more (#98)" names it. X3 is item 2's first mutant. X4 is `mutants.py:408-411` "the last declared octet is not walked as a header byte (#98)". | 11.4.4.3.3 |
| 3 R771-1 S2 | `mutants.py:315-320` "word 11 read two octets late (#98)" (`FU_LEFT_AT_TBI_C` 17 → 15, `KL_gptp_rx_parser.sv:199`) names "#98 plain fu: w11 as the plain case", "fu w11" and "#98 unknown TLV first: w11 as the plain case". | 11.4.4.3 Table 11-10 |
| 3 R772-1 S2 | `scripts/check_docs.py:631-655`: `selftest()` loads `check_docs_selftest` (and `check_docs` itself, when run as a script) through `_load_sibling` by its own path. `python3 -I scripts/check_docs.py --selftest` passes from the tree root and from another directory, 127 arms. | — |
| 3 not taken | R771-1 S3 (11-bit frame counter wrap over 2,047 octets): pre-existing and outside the 1,514-octet boundary, as the assignment rules. | — |
| 4 R771-1 R1 | `tb/verilator/engine/sim_main.cpp:3423-3425` "(refused at end of frame: the TLV is skipped and the chain holds no information TLV, #98)"; `:3501-3502` "the span of the former fixed Follow_Up TLV header arm (octets 44..59, before #98)". This is the review's exact text, rewrapped. | — |
| 4 R771-1 R2 = R772-1 R1 | `docs/HDL_DEVELOPER.md:44`, `:46`: "The first information TLV supplies word 11." and "A malformed chain still refuses the Follow_Up." | — |
| 5 counts | `tb/verilator/parser/Makefile:23` "Thirty-four defects"; `mutants.py:30` "Seven belong to #87 and #88" (was "Six", a wrong count since round 1; mutants 9 to 15 are seven); `mutants.py:39-52` "The last nineteen belong to #98" plus the round-2 defects; `docs/TEST_DEVELOPER.md:120-125` (three new suite lines, "Plants thirty-four parser defects, nineteen for the TLV walk."); PR body. | — |

## New checks and their planted mutants (failing words as printed)

Parser suite: 482 checks (473 at round 1, 378 at base). The three new rows add nine checks. Arm: 35/35, the unmutated control plus 34 defects (28 at round 1, 15 at base), 19 of them for #98. Every FAIL line of every #98 mutant is in `receipts/parser/mutant-fails-98.md`.

| Row / check | Mutant | Failing words |
|---|---|---|
| `#98 TLV past messageLength ahead of the information TLV`: no event, one drop, no w11 write | a malformed TLV header does not latch the refusal (#98) | `FAIL #98 TLV past messageLength ahead of the information TLV: no event got 0000000000000001 exp 0000000000000000`; `… one drop got 000000000000001b exp 000000000000001c`; `… no w11 write got 0000000000000001 exp 0000000000000000` |
| `#98 odd lengthField ahead of the information TLV`: the same three | the same mutant | `FAIL #98 odd lengthField ahead of the information TLV: no event got 0000000000000001 exp 0000000000000000` (and one drop, no w11 write) |
| `#98 information TLV with lengthField 30`: the same three | the information TLV is named by any lengthField of 28 or more (#98) | `FAIL #98 information TLV with lengthField 30: no event got 0000000000000001 exp 0000000000000000`; `… one drop got 000000000000001d exp 000000000000001e`; `… no w11 write got 0000000000000001 exp 0000000000000000` |
| `#98 unknown TLVs after`: event, no drop | a complete header ending on the last declared octet is read as cut (#98) | `FAIL #98 unknown TLVs after: event got 0000000000000000 exp 0000000000000002`; `FAIL #98 unknown TLVs after: no drop got 0000000000000011 exp 0000000000000010` |
| same | a zero-length TLV after the information TLV refuses the Follow_Up (#98) | the same two lines |
| same | the last declared octet is not walked as a header byte (#98) | the same two lines (and four "#98 header cut after 1 octet(s)" checks) |
| `#98 plain fu: w11 as the plain case`, `fu w11`, `#98 unknown TLV first: w11 as the plain case` | word 11 read two octets late (#98) | `FAIL #98 plain fu: w11 as the plain case got f000000700000000 exp fffff00000070000` (12 FAIL lines in all) |
| `#98 information TLV past messageLength` and `#98 trailing TLV past messageLength` (no event, one drop; no w11 write on the first) | a TLV value past messageLength is walked (#98), reworked | `FAIL #98 information TLV past messageLength: no event got 0000000000000001 exp 0000000000000000`; `FAIL #98 trailing TLV past messageLength: one drop got 0000000000000012 exp 0000000000000013` (exactly its 5 named checks) |
| `#98 header ends messageLength, value to come`: no event, one drop | an EOF header's own overrun is not refused (#98), unchanged | `FAIL #98 header ends messageLength, value to come: no event got 0000000000000001 exp 0000000000000000` (exactly its 2 named checks) |

The head harness against the base RTL fails 31 checks, all on #98 rows, the same 31 as round 1 (`receipts/parser/head-harness-on-base-rtl.log`). The base also refuses the three new refusal rows.

Both reviewers' own mutant scripts were rerun from copies of their packets against an export of `762fbd6` (`receipts/extra/`). R771-1's three (`eof_header_counts_as_cut`, `zero_len_after_info_refuses`, `w11_two_octets_late`) each fail the harness: 2, 2 and 12 FAIL. R772-1's X1 to X15 are each "harness: CAUGHT". The latch mutant X1 is caught on 6 checks, first "#98 TLV past messageLength ahead of the information TLV: no event".

## Gate table: repository, clean clone of `762fbd6`

Fresh clone of the committed head. The recorded-gates runner wrote one log, rc and seconds per command. The pinned 5.050 simulator ran behind a wrapper mapping "-j 0" to "-j 8", with TMPDIR in scratch. No 16-CPU range was free, so the fast set ran inside this lane's own unit in three chunks under the 10-minute foreground limit (`receipts/repo-head-fast/chunk1..3/`). The engine arm ran in its own unit (MemoryMax 10 G) on a booked range, in its own clone.

| # | Gate | Head `762fbd6` |
|---|---|---|
| 1 | `make contract` | rc 0 |
| 2 | `make -C tb/verilator/ucpu` | rc 0, 768/768 |
| 3 | `make -C tb/verilator/parser` | rc 0, 482/482; arm 35/35, every mutant caught on every check it names (227 s) |
| 4 | `make -C tb/verilator/engine run` | rc 0, 2,048 ×3 + 60 |
| 4b | `make -C tb/verilator/engine mutants` | rc 0, 136/136: 135 caught plus the control (12,348 s). Every verdict line and all 387 named FAIL lines are identical to round 1's base run (`receipts/repo-head-arm/verdicts-vs-base.diff`, `fail-lines-vs-base.diff`, both empty) |
| 5 | `make -C tb/verilator/gaskets` | rc 0, 81/81; arm 5/5 |
| 6 | `make -C tb/tsngen` | rc 0, 288/288; arm 4/4 |
| 7 | `make -C bench/arty test` | rc 0 |
| 8 | `make lint` | rc 0 |
| 9 | `make docs` | rc 0: docs check PASS, selftest 127 arms, source evidence 20 exact, 0 findings |
| 10 | `make diagrams-check` | rc 0 |
| 11 | `python3 syn/ooc/check_ooc_clock.py --selftest` | rc 0, 30 arms |
| 12 | `make ooc` | rc 0, 0 critical warnings |
| 13 | `git diff --exit-code --stat` after the run | rc 0. `git status --porcelain` is empty too. |
| e1 | `python3 -I scripts/check_docs.py` and `python3 -I scripts/check_docs.py --selftest` (tree root and another directory) | rc 0; PASS, 127 arms |
| e2 | `git diff --check 3e3a4e7 762fbd6` | rc 0 |

The OOC reports equal round 1's line for line, apart from the date and host header lines (`receipts/ooc/head/`). Engine 4,920 LUTs and 3,461 FFs, parser 921 LUTs and 304 FFs, WNS 2.249 ns, as in round 1. `hdl/` is unchanged, so round 1's base and head area and timing tables stand.

## Scratch-parent consumer gate table

Scratch parent: the round-1 `gptp98-parent` (milan-fpga dev `604899c0`, the trusted clone) and its command-14 sibling. Each took one more local commit, setting the gptp-processor gitlink to `762fbd67`, never pushed: `768b3d60970a4020a15c9718d7e4851a4ba118b8` (A) and `033ee092f2919db3f3defce1de35ad7efabffaa0` (B), with the same tree. Each ran as its own unit (MemoryMax 10 G) on a booked CPU range. The commands and environment are round 1's (`receipts/scripts/mkparentspec.py`): the manager template's 15 commands plus `gptp_plane`, `gptp_txts`, `gptp_tables` and the tsn_fuzz `ptp` campaign at tsn-gen `deca300c`. The base column is round 1's run of dev `604899c0` unmodified (gitlink `135afd04`).

| # | Consumer gate | Base `604899c0` (gitlink `135afd04`), round 1 | Head `768b3d60` / `033ee092` (gitlink `762fbd67`) |
|---|---|---|---|
| 1 | `scripts/check_cpp_idiom.py` | rc 0 (multi-declarator 0 <= 0, long function 0 <= 0) | rc 0 (the same) |
| 2 | `scripts/check_py_idiom.py` | rc 0 (long function 9 <= 9, long module 10 <= 10) | rc 0 (the same) |
| 3 | `scripts/xvlog_gate.py --check` | rc 0, PASS, 0 findings | rc 0, PASS, 0 findings |
| 4 | `scripts/check_rtl_source_lists.py` | rc 0, OK | rc 0, OK |
| 5 | `sw/builder/test_builder.py` | rc 0, all gates pass except 1 NOT RUN (gate 11, the host-dependent calibration arm) | rc 0, the same |
| 6 | `make -C tb/verilator/gptp_shadow -j8` | rc 0, 325/325; controls 9/9 | rc 0, 325/325; controls 9/9 |
| 7 | `scripts/check_port_contracts.py` | rc 0, OK | rc 0, OK (4,080 ports; gptp-processor 127) |
| 8 | `scripts/measure_naming.py --check` | rc 0 | rc 0, NAMING RATCHET PASS |
| 9 | `scripts/measure_test_evidence.py --check` | rc 0 | rc 0, TEST-EVIDENCE RATCHET PASS |
| 10 | `scripts/docs_check.py` | rc 0, 0 findings | rc 0, 0 findings |
| 11 | `scripts/lint_rtl.py --check` | rc 0 (89 <= 89) | rc 0 (89 <= 89) |
| 12 | `make -C tb/verilator/milan_dp gptp` | rc 0, 210/210 | rc 0, 210/210 |
| 13 | `make -C tb/verilator/milan_dp gptp-lat` | rc 0, 210/210 | rc 0, 210/210 |
| 14 | `make -C tb/verilator/milan_dp_gptp` (own clone and unit) | rc 0, RESULT PASS: physical 151, setup abort 6, no-TX 20, no-Pdelay 14, recentre controls 14, 0 failures; 17.992742740 simulated s | rc 0, the same counts and simulated time (5,412 s); its 89 Pdelay-event, progress and verdict lines equal base's |
| 15 | `make -C tb/verilator/milan_dp_gm_steps` | rc 0, 6/6 (gmstep 196 checks) | rc 0, 6/6 (gmstep 196 checks) |
| x1 | `make -C tb/verilator/gptp_plane` | rc 0; phc_step campaign 8/8 | rc 0; the same |
| x2 | `make -C tb/verilator/gptp_txts` | rc 0; controls 13/13 | rc 0; controls 13/13 |
| x3 | `make -C tb/verilator/gptp_tables` | rc 0; controls 26/26 | rc 0; controls 26/26 |
| x4 | `make -C tb/verilator/tsn_fuzz ptp` (tsn-gen `deca300c`) | rc 0: 675 pass, 0 fail, 0 known gaps; freshness PASS | rc 0: the same |
| x5 | `git status --porcelain` after the run | `TEST_RESULTS.md` rewritten, timestamp only | the same; restored afterwards |

- The template's commands 1 to 13 and 15 and the four extras ran in parent A, and command 14 ran alone in parent B (`receipts/parent-head-A/`, `receipts/parent-head-B/`). Both runs are rc 0 with the head unchanged throughout.
- Command 14's lines compare against round 1's base run (`receipts/parent-base-B-round1/`); `receipts/parent-head-B/lines-vs-base.diff` is empty.
- The scratch parents kept round 1's build directories. In commands 12 and 13 the simulator's own make found the model current ("Nothing to be done"); that is correct, since the gitlink's `hdl/` is round 1's tree. Both legs ran their 210 checks.
- Base column: round 1's receipts at `604899c0` (the round-1 output directory, `parent-base-A`/`parent-base-B`). This round reruns no base, since no gate input outside gptp-processor changed.

## Not done / notes

- Nothing pushed. No PR created or edited, no hardware or bench access. Posts on #98: TAKEN and REVIEW READY only. The parent commits are local scratch snapshots.
- No top-level port, parameter or register-map change. `hdl/` is byte-identical to round 1.
- Pending manager duties (from R771-1, unchanged by this round): the parent gitlink bump must update the parent's donor deep links and gPTP docs pins, then run the gm_steps mutation duty and the gptp_shadow lifecycle with the committed gitlink.
- `mutants.py:30` "Six" → "Seven" is a count fix in the docstring the assignment names (item 5). The count was wrong from round 1 (`dbe1acb`), and "The last six" was already wrong at base.

## Receipts

`receipts/INDEX.md` lists every file present (path, bytes, SHA-256 prefix) and is generated from the files. Host paths, the user, the committer and the host name are replaced by placeholders (`receipts/scripts/receipts.py`). Logs over 190 KB are kept as digests (first and last 60 lines, every verdict line, and the full file's size and SHA-256). `receipts/superseded-6e27cd6/` holds the earlier fast run at `6e27cd6` and the chunk-2 run whose console was piped, which was set aside and rerun unpiped. Neither is cited above.
