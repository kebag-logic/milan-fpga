# [A730] FPGA-gPTP #98: Follow_Up TLV walk — HANDOFF

Status: REVIEW READY at `5b10675c3a22acc85bad7c150e1cd25984928385`. All four acceptance items are met. Every repository gate is rc 0 at base and at head, including both engine mutation arms in full (136/136 each). On the committed scratch parent the manager template's 15 commands and four extra gPTP suites are rc 0 at base and at head, milan_dp's `gptp` and `gptp-lat` legs and `gptp_shadow` included.

- Repository: Mister-M-alt/FPGA-gPTP, branch `98-followup-tlv-walk` (local, not pushed).
- Base: main `3e3a4e7695ce66eed609089f280c2fba45b24d36`. The parent pins `135afd04`. `git diff --stat 135afd04 3e3a4e7` touches Markdown, `scripts/check_docs.py` and `scripts/check_source_evidence.py` only: no `hdl/`, `tb/`, `syn/` or `bench/` file.
- Head: `5b10675c3a22acc85bad7c150e1cd25984928385`. Four commits, one-line subjects, no body, no trailers:
  - `434527a` Walk the Follow_Up TLV chain to the information TLV within messageLength and refuse a malformed chain (#98)
  - `dbe1acb` Check the Follow_Up TLV walk's acceptances and refusals, each with a planted parser mutant caught by name (#98)
  - `6f3f003` Describe the Follow_Up TLV walk in the HDL and test guides (#98)
  - `5b10675` Move the docs gate's fixture arms into their own module and annotate its public functions, so the parent's Python idiom gate passes with this gitlink (#98)
- `git diff --stat 6f3f003 5b10675 -- hdl tb syn bench` is empty. The last commit touches `scripts/` and `docs/` only.
- Issue posts: TAKEN `#98 issuecomment-6634919604`; REVIEW READY at `5b10675c` `#98 issuecomment-6640153545`.
- Scratch parent (local commits only, never pushed): milan-fpga dev `604899c0` (the trusted clone) plus one commit setting the gitlink to `5b10675c`, giving `09d163f9233dc45e2cd0982c3666baac1fc9a298`.

## Authority (clauses read for this change)

- IEEE 802.1AS-2011 11.4.1: a time-aware system that cannot parse a TLV ignores it and attempts the next TLV (IEEE 1588-2008 14.1). Cor1 PICS MDFDPP-28 repeats it.
- 802.1AS-2011 11.4.4.2.2 and 11.4.4.3 (Table 11-10), 11.4.4.3.2 to 11.4.4.3.5: the information TLV is tlvType 0x3, lengthField 28, organizationId 00-80-C2, organizationSubType 1. A sender places it first.
- 802.1AS-2011 11.4.2.2 and 10.5.2.2.4: messageLength ends with and includes the last octet of the last TLV.
- IEEE 1588-2008 5.3.8 (every TLV an even number of octets), 14.1 and 14.3.2.3 (a node that does not recognise an organizationId or subtype disregards the TLV except its lengthField).

## Changes (file:line at `5b10675`) and clause

| Where | What | Clause |
|---|---|---|
| `hdl/wire/KL_gptp_rx_parser.sv:29-31`, `:54-66` | Header: what a Follow_Up is refused for, and the chain walk | 11.4.1; 1588 14.1, 5.3.8 |
| `:183-199` | Constants: `FU_TLV_TYPE_C`, `FU_TLV_LEN_C`, `FU_TLV_ORG_C`; the two value-byte positions (organizationSubType ends at TLV octet 9, gmTimeBaseIndicator at octet 15) | 11.4.4.3, Table 11-10 |
| `:227-230` | The four fixed Follow_Up TLV offsets (frame bytes 59, 67, 71 and 73) are removed; `OFF_FU_END_C` (the 76-octet minimum) stays | Table 11-9 |
| `:241-250` | The Announce chain registers (`tlv_hdr_run_r`, `tlv_hdr_pos_r`, `tlv_left_r`) also serve the Follow_Up walk; two new flags, `fu_info_r` and `fu_found_r` | — |
| `:359-381` | Walk terms: a header byte counts only within messageLength; a value byte needs no bound; `fu_tlv_header_bad_w` (odd lengthField, or a value past messageLength, current byte included); `fu_tlv_cut_after_w` (a header messageLength cuts) | 1588 5.3.8; 11.4.2.2 |
| `:413-414`, `:464-465` | Reset and start-of-frame clear of the flags | — |
| `:559-598` | The walk: arm at octet 44; per header, skip by lengthField and name the information TLV by type and length; at value byte 5 compare organizationId and subtype; at value byte 11 write word 11; restart the header after the value | 11.4.1; 11.4.4.3 |
| `:689-708` | End of frame: a Follow_Up needs the information TLV, no current-byte header refusal, and no cut header | 11.4.2.2 |
| `docs/SOURCE_EVIDENCE.md:13`, `:33` | Two parser anchors follow the moved lines (L439, L521; 20 exact) | — |
| `tb/verilator/parser/sim_main.cpp:825-991`, `:1815-1816` | The chain builder, the accepting rows and the refusing rows | — |
| `tb/verilator/parser/mutants.py:39-47`, `:143-174`, `:293-363` | Docstring; patterns; 13 #98 mutants | — |
| `tb/verilator/parser/Makefile:22-26`, `README.md:18` | Arm description (28 defects) | — |
| `docs/HDL_DEVELOPER.md:40-44`, `docs/TEST_DEVELOPER.md:25`, `:48`, `:119-120` | Receive path and suite text | — |
| `scripts/check_docs.py`, new `scripts/check_docs_selftest.py`, `docs/INTEGRATION.md:856`, `docs/MANAGER.md:59`, `docs/README.md:48` | Fixture arms moved unchanged into their own module and split into ordered groups. `load_generator`, `constant_findings` and `copy_findings` annotated. The links follow the arms. | — |

### Why the last commit

The parent's `scripts/check_py_idiom.py` fails at any gitlink from main `3e3a4e7`. With the gitlink at plain `3e3a4e7`: rc 1, "long function 10 > ratchet 9" and "unannotated public function 3 > ratchet 0", all in `gptp-processor/scripts/check_docs.py` from #96/#97 (`receipts/docs-gate/parent-py-idiom-gitlink-3e3a4e7.log`). The #96 lane ran no parent idiom gate. A split inside one file would make it 1,059 lines, over the 1,000-line module rule, so the arms moved to a sibling module.

- `check_docs.py` and `--selftest` outputs are byte-identical before and after (`receipts/docs-gate/`). The selftest still reports 127 arms.
- Three planted gate defects fail the same arm with the same message before and after (`planted-*.out`): MAX_WORDS 11, the joined-markup search dropped, and the duplicate ROM row not reported.
- The parent's idiom scanners report zero findings on both files and on the parser `mutants.py`.

### Semantics decided

- Walk all TLVs within messageLength (not stopping at the information TLV). Acceptance 2 refuses a TLV past messageLength and a truncated header without qualification, and 11.4.2.2 ends messageLength on the last TLV's last octet. The Announce chain already follows this rule.
- Behaviour change: base accepted a Follow_Up whose trailing chain overran messageLength or ended in a cut header, because it read nothing after octet 75. Head refuses those. Every Follow_Up the base accepted with a well-formed trailing chain is still accepted.
- A TLV that differs from the information TLV in any of its four header values is not that TLV and is skipped. A second information TLV is skipped too; word 11 comes from the first. An odd lengthField refuses the frame, as the Announce chain does.

## New checks, planted mutants, failing words

Parser suite: 473 checks at head (378 at base, +95). Arm: 29/29 (control + 28 defects; 16/16 at base). Every FAIL line of every #98 mutant is in `receipts/parser/mutant-fails-98.md`.

| Row | Checks | Mutant (name in `mutants.py`) | Failing words (as printed) |
|---|---|---|---|
| `#98 plain fu` | event, ev_seq, w0..w5, w11 as built, no drop | (reference) | — |
| `#98 unknown TLV first` | event, ev_seq, w0..w5 and w11 as the plain case, no drop | a TLV ahead of the information TLV refuses the Follow_Up (#98) | `FAIL #98 unknown TLV first: event got …0 exp …2`; `… no drop got …11 exp …10` |
| same | w11 as the plain case | word 11 read at the fixed octets 68..73 (#98) | `FAIL #98 unknown TLV first: w11 as the plain case got ffffffffffffffff exp fffff00000070000` |
| `#98 three unknown TLVs first` | as above | a zero-length TLV ends the walk (#98); the information TLV is named without its organizationId and subtype (#98) | `… event got …0 exp …2`; `… w11 as the plain case got 1111111122220000 exp fffff00000070000` |
| `#98 unknown TLV first, padded` | as above | the walk reads padding past messageLength as a header (#98) | `FAIL #98 unknown TLV first, padded: event got …0 exp …2`; `… no drop got …11 exp …10` |
| `#98 second information TLV` | as above | a later information TLV is read again (#98) | `FAIL #98 second information TLV: w11 as the plain case got 00000fff00090000 exp fffff00000070000` |
| `#98 identifiers at octet 6` | as above | the information TLV is named without its lengthField (#98) | `FAIL #98 identifiers at octet 6: w11 as the plain case got 1111111122220000 exp fffff00000070000` |
| `#98 unknown TLVs after` | as above | (control) | — |
| `#98 no information TLV` | no event, one drop, no w11 write | a Follow_Up is accepted without its information TLV (#98) | `FAIL #98 no information TLV: no event got …1 exp …0`; `… one drop got …10 exp …11` |
| `#98 information TLV past messageLength` | no event, one drop, no w11 write | a TLV value past messageLength is walked (#98) | `… no event got …1 exp …0`; `… no w11 write got …1 exp …0` |
| `#98 trailing TLV past messageLength` | no event, one drop | the same | `… no event got …1 exp …0` |
| `#98 header ends messageLength, value to come` | no event, one drop | an EOF header's own overrun is not refused (#98); the value mutant | `… no event got …1 exp …0`; `… one drop got …12 exp …13` |
| `#98 header cut after 1/2/3 octet(s)[, padded]` (6 rows) | no event, one drop | a TLV header cut by messageLength is accepted (#98) | `FAIL #98 header cut after 2 octet(s), padded: no event got …1 exp …0` (all six) |
| `#98 odd lengthField` | no event, one drop, no w11 write | an odd lengthField is walked (#98) | `… no event got …1 exp …0`; `… no w11 write got …1 exp …0` |
| existing `fu tlvType 0x0008 drop` | no event, one drop, no w11 write | the information TLV is named without its tlvType (#98) | `FAIL fu tlvType 0x0008 drop: no event got …1 exp …0` |
| existing `fu orgId 00-1B-19 drop`, `fu orgSubType 2 drop` | no event | the organizationId/subtype mutant; the missing-TLV mutant | `… no event got …1 exp …0` |

Against the base RTL, the head harness fails 31 checks (`receipts/parser/head-harness-on-base-rtl.log`). The fails are the five unknown-TLV-first rows (event 0, one drop, w11 never written) and the trailing-chain refusals that base accepted.

## Timing kept: per-byte, no buffer

`receipts/probe/`: one corpus, base RTL and head RTL, every cycle that writes the bank, raises an event or moves the drop count. The corpus is Follow_Up (plain, trailing TLV, padded), Sync padded, Pdelay_Resp, Pdelay_Resp_Follow_Up, Pdelay_Req and an Announce with a two-hop path. The traces are identical for all eight (`trace.diff` shows only the two #98 frames). Word 11 lands at frame byte 73 and the event follows EOF by the same cycle. With a 12-octet TLV first, word 11 lands at byte 85 and the event keeps the same EOF distance.

## Gate table: repository

The recorded-gates runner ran one command at a time with its own log, rc and seconds, in fresh clones at base and at head. Units ran with MemoryMax 10 G, the parent CI's pinned 5.050 simulator behind a wrapper mapping "-j 0" to "-j 8", and TMPDIR in scratch.

| # | Gate | Base `3e3a4e7` | Head `5b10675` |
|---|---|---|---|
| 1 | `make contract` | rc 0 | rc 0 |
| 2 | `make -C tb/verilator/ucpu` | rc 0, 768/768 | rc 0, 768/768 |
| 3 | `make -C tb/verilator/parser` | rc 0, 378/378; arm 16/16 | rc 0, 473/473; arm 29/29 |
| 4 | `make -C tb/verilator/engine run` | rc 0, 2,048 ×3 + 60 | rc 0, 2,048 ×3 + 60 |
| 4b | `make -C tb/verilator/engine mutants` | rc 0, 136/136: 135 caught plus the control (12,024 s) | rc 0, 136/136: 135 caught plus the control (12,152 s), run at `6f3f003`; every verdict line and all 387 named FAIL lines identical to base (`repo-head-arm/verdicts-vs-base.diff`) |
| 5 | `make -C tb/verilator/gaskets` | rc 0, 81/81; arm 5/5 | rc 0, 81/81; arm 5/5 |
| 6 | `make -C tb/tsngen` | rc 0, 288/288; arm 4/4 | rc 0, 288/288; arm 4/4 |
| 7 | `make -C bench/arty test` | rc 0 | rc 0 |
| 8 | `make lint` | rc 0 | rc 0 |
| 9 | `make docs` | rc 0, 127 selftest arms, evidence 20 exact | rc 0, the same |
| 10 | `make diagrams-check` | rc 0 | rc 0 |
| 11 | `syn/ooc/check_ooc_clock.py --selftest` | rc 0 | rc 0 |
| 12 | `make ooc` | rc 0 | rc 0 |
| 13 | `git diff --exit-code --stat` after the run | rc 0 | rc 0 |

Also at `6f3f003` (the RTL and tests of `5b10675`, before the docs-gate move): all 13 rc 0 (`receipts/repo-head-6f3f003-fast/`).

- The engine arm ran at `6f3f003`. The tree ids of `hdl/` and `tb/` there equal those at `5b10675` (`receipts/repo-head-arm/input-identity-6f3f003-vs-5b10675.txt`); the arm reads nothing else, so its result is the head's.
- The suites outside the parser count the same at base and head: ucpu 768, engine 2,048 ×3 + 60, gaskets 81 + 5, tsngen 288 + 4.
- `native-shards.py` needs a spec whose suite command is the parent's `scripts/run_all_suites.sh`, and FPGA-gPTP has none. So the processor sweep ran as recorded-gates units, one clone each, on ranges booked with `cpu_ranges.py pick`, MemoryMax 10 G. MemAvailable stayed above 55 GB.

## Area and timing (the processor's own gates)

`make ooc`, out of context, 100 MHz, xc7a100t-2 (`receipts/ooc/`):

| | Engine LUTs | Engine FFs | Parser LUTs | Parser FFs | µCPU LUTs | Engine WNS | µCPU WNS |
|---|---:|---:|---:|---:|---:|---:|---:|
| Base | 4,926 | 3,459 | 927 | 302 | 1,643 | 2.249 ns | 1.941 ns |
| Head | 4,920 | 3,461 | 921 | 304 | 1,643 | 2.249 ns | 1.941 ns |

The same synthesis followed by opt and place (`receipts/area/`, script `receipts/scripts/engine_place.tcl`), same shipping image:

| | Engine LUTs | Engine FFs | Slices | Parser LUTs | Placed WNS | Worst path |
|---|---:|---:|---:|---:|---:|---|
| Base | 4,876 | 3,459 | 1,634 | 912 | 0.506 ns | inside `u_ucpu` |
| Head | 4,874 | 3,461 | 1,634 | 907 | 0.513 ns | inside `u_ucpu` |

There is no critical warning in any run. The two added FFs are `fu_info_r` and `fu_found_r`.

## Scratch-parent consumer gate table

The manager template's 15 commands (gptp68 r3's six, the five docs gates, the four milan_dp gPTP legs, as `prepare-consumer.py` lists them) ran command for command. milan_dp's `gptp` and `gptp-lat` legs and `gptp_shadow` are included. The environment adds PATH to the pinned-simulator wrapper, VERILATOR_ROOT, TMPDIR, HOME and TSN_GEN_ROOT, tsn-gen being at the parent CI pin `deca300c` and built as CI builds it. Command 14 ran in its own clone and unit. The clones hold every public submodule; the private `external` is not initialised, since no gate builds it.

- Base: dev `604899c0` unmodified (gitlink `135afd04`).
- Head: snapshot `09d163f9` (gitlink `5b10675c`).

| # | Consumer gate | Base `604899c0` (gitlink `135afd04`) | Head `09d163f9` (gitlink `5b10675c`) |
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
| 14 | `make -C tb/verilator/milan_dp_gptp` (own clone and unit) | rc 0, RESULT PASS: physical 151, setup abort 6, no-TX 20, no-Pdelay 14, recentre controls 14, 0 failures; 17.992742740 simulated s (5,349 s) | rc 0, RESULT PASS: physical 151, setup abort 6, no-TX 20, no-Pdelay 14, recentre controls 14, 0 failures; 17.992742740 simulated s (5,412 s) |
| 15 | `make -C tb/verilator/milan_dp_gm_steps` | rc 0, 6/6 (gmstep 196 checks) | rc 0, 6/6 (gmstep 196 checks) |
| x1 | `make -C tb/verilator/gptp_plane` | rc 0; phc_step campaign 8/8 | rc 0; the same |
| x2 | `make -C tb/verilator/gptp_txts` | rc 0; controls 13/13 | rc 0; controls 13/13 |
| x3 | `make -C tb/verilator/gptp_tables` | rc 0; controls 26/26 | rc 0; controls 26/26 |
| x4 | `make -C tb/verilator/tsn_fuzz ptp` (tsn-gen `deca300c`) | rc 0: 675 pass, 0 fail, 0 known gaps; freshness PASS | rc 0: the same |
| x5 | `git status --porcelain` after the run | `TEST_RESULTS.md` rewritten, timestamp only | the same (`parent-head-A/test-results-rewrite.diff`) |

- Command 14: head's 89 Pdelay-event, progress and verdict lines (11 events, 71 progress lines) are identical to base (`receipts/parent-head-B/lines-vs-base.diff`, empty).
- Run at the superseded head `6f3f003` (snapshot `8a62ef42`), the head's command 2 failed with "long function 10 > ratchet 9" and "unannotated public function 3 > ratchet 0" (`receipts/parent-superseded-8a62ef42/`). That failure came from main `3e3a4e7`, and the last commit removes it. The run was stopped, and every head row above is from `09d163f9`.
- Command 2 also fails with the gitlink at plain main `3e3a4e7` (`receipts/docs-gate/parent-py-idiom-gitlink-3e3a4e7.log`), so any adoption of main from #96/#97 on needs this commit or an equivalent.

## Not done / notes

- Nothing pushed; no PR created or edited; no hardware or bench. Posts on #98: TAKEN and REVIEW READY only. The only parent commits are local scratch-snapshot commits (`09d163f9`, the superseded `8a62ef42`, and `abd2ac3e`, the plain-main gitlink used to show the inherited Python idiom failure). None was pushed.
- No top-level port, parameter or register-map change: the parent's port-contract gate counts the same 4,080 ports, 127 of them in gptp-processor, at base and head.
- Behaviour change, deliberate (see Semantics): a Follow_Up whose trailing chain overruns messageLength or ends in a cut header was accepted at base and is refused now. No parent consumer depends on it: tsn_fuzz `ptp` 675/675 and every milan_dp leg are unchanged.
- The parent adoption still owes what any gitlink move owes: the parent pins its gPTP docs and the submodule page to the donor SHA (`check_gptp_docs.py`, `check_submodule_docs.py`, not on the template list).
- The new rows are parser-level, which acceptance 3 names. No engine-level row drives an unknown-TLV-first Follow_Up through pairing; the parser's words for it are proven identical to the plain case, and the engine reads only those words.

## Receipts

`receipts/INDEX.md` lists every file present (path, bytes, SHA-256 prefix), generated from the files. Host paths, the user, the committer and the host name are replaced by placeholders (`receipts/scripts/receipts.py`). Logs over 190 KB are kept as digests: the first and last 60 lines, every verdict line, and the full file's size and SHA-256.
