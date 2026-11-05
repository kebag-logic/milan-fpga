[A730b] Walk the Follow_Up TLV chain to the information TLV (#98)

## Why

IEEE 802.1AS-2011 11.4.1 has a receiver ignore a TLV it cannot parse and attempt the next one (IEEE 1588-2008 14.1). The parser looked for the Follow_Up information TLV (11.4.4.3) only at octet 44 and dropped the Follow_Up otherwise. A Follow_Up whose first TLV is unknown was counted as a drop and raised no event.

## What changes

`hdl/wire/KL_gptp_rx_parser.sv`, byte-serial as before, no frame buffer:

- From octet 44 the Follow_Up TLVs are walked within messageLength. Each TLV is skipped by its lengthField.
- The first TLV whose tlvType (0x3), lengthField (28), organizationId (00-80-C2) and organizationSubType (1) are those of 11.4.4.3 is the information TLV. Word 11 is read from its own octets 10..15. The Follow_Up is accepted with the same words as when that TLV is first.
- Refused and counted, one drop and no event:
  - no information TLV in the chain;
  - a TLV whose value runs past messageLength (802.1AS-2011 11.4.2.2: messageLength ends with the last octet of the last TLV), including a header that ends the message with a value still to come;
  - a TLV header that messageLength cuts after one to three octets, padded or not;
  - an odd lengthField (IEEE 1588-2008 5.3.8), as the Announce chain already refuses it.
- Physical padding past messageLength is never read as a TLV. A later information TLV is skipped like any other TLV.
- The walk reuses the Announce chain's header, position and length registers (one frame has one type). It adds two flags.

Behaviour change to note: base ignored every octet after an information TLV at octet 44. It therefore accepted a Follow_Up whose trailing chain overran messageLength or ended in a cut header. Those Follow_Ups are now refused, the same rule the Announce suffix follows. A well-formed trailing TLV is still accepted.

`scripts/check_docs.py`: the documentation gate's fixture arms move unchanged into `scripts/check_docs_selftest.py`. That module splits them into groups, and three public functions gain annotations. Main already fails the parent repository's Python idiom gate at any gitlink from 3e3a4e7: one 339-line function, three unannotated public functions, and a module that would pass 1000 lines once split in place. The change clears that failure. The arms, their order, their messages and the count (127) are unchanged. Three planted gate defects give identical failures before and after.

## Tests

Parser suite: 482 checks (378 at base). Mutation arm: 34 defects and the control (15 defects at base), 19 of the defects for #98. Every defect fails each check it names.

| Row (`tb/verilator/parser/sim_main.cpp`) | Expect | Planted parser defect that fails it |
|---|---|---|
| `#98 plain fu` | accepted; w0..w5, w11 as built | word 11 read two octets late (also the reference for the rows below) |
| `#98 unknown TLV first` | accepted, w0..w5 and w11 as the plain case | a TLV ahead of the information TLV refuses the Follow_Up; word 11 read at the fixed octets 68..73; word 11 read two octets late |
| `#98 three unknown TLVs first` (zero-length, PATH_TRACE-typed, 00-80-C2 subtype 2) | accepted, as the plain case | a zero-length TLV ends the walk; the information TLV named without its organizationId and subtype |
| `#98 unknown TLV first, padded` | accepted, as the plain case | the walk reads padding past messageLength as a header |
| `#98 second information TLV` | accepted, word 11 from the first | a later information TLV is read again |
| `#98 identifiers at octet 6` (another OUI's 30-octet TLV) | accepted, word 11 from the real TLV | the information TLV named without its lengthField |
| `#98 unknown TLVs after` (ends on a zero-length header at messageLength) | accepted | a complete header ending on the last declared octet is read as cut; a zero-length TLV after the information TLV refuses the Follow_Up; the last declared octet is not walked as a header byte |
| `#98 no information TLV` | refused, no word 11 | a Follow_Up is accepted without its information TLV |
| `#98 information TLV past messageLength` | refused, no word 11 | a TLV value past messageLength is walked |
| `#98 trailing TLV past messageLength` | refused | a TLV value past messageLength is walked |
| `#98 header ends messageLength, value to come` | refused | an EOF header's own overrun is not refused |
| `#98 header cut after 1, 2, 3 octet(s)`, each with and without padding | refused | a TLV header cut by messageLength is accepted |
| `#98 odd lengthField` | refused, no word 11 | an odd lengthField is walked |
| `#98 TLV past messageLength ahead of the information TLV` | refused, no word 11 | a malformed TLV header does not latch the refusal |
| `#98 odd lengthField ahead of the information TLV` | refused, no word 11 | a malformed TLV header does not latch the refusal |
| `#98 information TLV with lengthField 30` (00-80-C2/1, fields in place, no other TLV) | refused, no word 11 | the information TLV is named by any lengthField of 28 or more |

The existing #11 rows (`fu tlvType 0x0008 drop`, `fu orgId 00-1B-19 drop`, `fu orgSubType 2 drop`) also name the "information TLV named without its tlvType", "without its organizationId and subtype" and "accepted without its information TLV" defects. The existing `fu w11` row also names "word 11 read two octets late".

Against the base RTL, the new rows fail 31 checks: the unknown-TLV-first rows (no event, one drop) and the trailing-chain refusals that base accepted. Base refuses the three round-2 refusal rows too.

A cycle trace of base and head RTL over Follow_Up (plain, trailing TLV, padded), Sync, Pdelay_Resp, Pdelay_Resp_Follow_Up, Pdelay_Req and Announce frames is identical, line for line. Word 11 lands at frame byte 73 and every event at the same cycle after EOF. With a 12-octet TLV first, word 11 lands 12 bytes later and the event at the same cycle after EOF.

## Gates

Repository, at base `3e3a4e7` and head, all exit 0: `make contract`, the ucpu, parser, engine run, gaskets and tsngen suites, `make -C bench/arty test`, `make lint`, `make docs`, `make diagrams-check`, the OOC clock selftest, `make ooc`, and a clean tree after the runs. The engine mutation arm, `make -C tb/verilator/engine mutants`, is 136/136 at base and at head, with identical verdict and named-failure lines.

Area and timing, out of context at 100 MHz (`make ooc`):

| | Engine LUTs | Engine FFs | Parser LUTs | Parser FFs | WNS |
|---|---:|---:|---:|---:|---:|
| Base | 4,926 | 3,459 | 927 | 302 | 2.249 ns |
| Head | 4,920 | 3,461 | 921 | 304 | 2.249 ns |

The same synthesis followed by opt and place:

| | Engine LUTs | Engine FFs | Slices | Parser LUTs | Placed WNS |
|---|---:|---:|---:|---:|---:|
| Base | 4,876 | 3,459 | 1,634 | 912 | 0.506 ns |
| Head | 4,874 | 3,461 | 1,634 | 907 | 0.513 ns |

The two added flip-flops are the walk's two flags. The worst path at base and at head lies inside the µCPU, not the parser. No critical warning in any run.

Parent consumer gate. milan-fpga dev `604899c0` took this head as the gptp-processor gitlink in one local commit, never pushed. The run covers the full gPTP consumer list (the code-quality gates, the builder test, `gptp_shadow`, milan_dp's `gptp` and `gptp-lat` legs, `milan_dp_gptp`, `milan_dp_gm_steps`) plus `gptp_plane`, `gptp_txts`, `gptp_tables` and the tsn_fuzz `ptp` campaign at the parent CI's field-oracle pin. All are rc 0 with the dev pin `135afd04` and with this head:

| # | Consumer gate | Dev pin `135afd04` | Head (gitlink `762fbd6`) |
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
| 14 | `make -C tb/verilator/milan_dp_gptp` | rc 0, RESULT PASS: physical 151, setup abort 6, no-TX 20, no-Pdelay 14, recentre controls 14, 0 failures; 17.992742740 simulated s | rc 0, the same counts and simulated time (5,412 s); its 89 Pdelay-event, progress and verdict lines equal base's |
| 15 | `make -C tb/verilator/milan_dp_gm_steps` | rc 0, 6/6 (gmstep 196 checks) | rc 0, 6/6 (gmstep 196 checks) |
| x1 | `make -C tb/verilator/gptp_plane` | rc 0; phc_step campaign 8/8 | rc 0; the same |
| x2 | `make -C tb/verilator/gptp_txts` | rc 0; controls 13/13 | rc 0; controls 13/13 |
| x3 | `make -C tb/verilator/gptp_tables` | rc 0; controls 26/26 | rc 0; controls 26/26 |
| x4 | `make -C tb/verilator/tsn_fuzz ptp` (tsn-gen `deca300c`) | rc 0: 675 pass, 0 fail, 0 known gaps; freshness PASS | rc 0: the same |
| x5 | `git status --porcelain` after the run | `TEST_RESULTS.md` rewritten, timestamp only | the same; restored afterwards |

With the gitlink at plain main `3e3a4e7`, `check_py_idiom.py` fails: "long function 10 > ratchet 9", "unannotated public function 3 > ratchet 0". The docs-gate commit above removes that failure.

## Round 2

Both reviews found the RTL correct and asked for proof only. `hdl/` is unchanged in this round (its tree is the same as round 1's), and no new row showed an RTL defect. Four commits on top of round 1:

- `fc13a65` tests. Three refusal rows, each expecting no event, one drop and no word-11 write:
  - a header `{0x000A, lengthField 0x0100}` running past messageLength 80, then the information TLV;
  - a header `{0x000A, lengthField 1}`, odd, then the information TLV;
  - a 00-80-C2/1 TLV with lengthField 30, even but not 28 (802.1AS-2011 11.4.4.3.3), and no other TLV.
  
  Six new parser mutants. One mutant is reworked:
  - "a malformed TLV header does not latch the refusal" deletes the `bad_r <= 1'b1;` of the `fu_tlv_header_bad_w` branch. Only the two rows above with a malformed header ahead of the information TLV catch it. In every older row, the octets after the malformed header never form an information TLV, so the refusal still arrived through the missing TLV or the end-of-frame cut term.
  - "a TLV value past messageLength is walked" is split:
    - The walk half keeps only the odd term in the walk's header verdict and loads the value. The trailing and information-TLV overrun rows catch it.
    - The end-of-frame half is the existing "an EOF header's own overrun is not refused". The value-to-come row catches it.
    - The cut term is proven alone by "a TLV header cut by messageLength is accepted".
  - Three defects refuse the well-formed `#98 unknown TLVs after` chain, each failing its ": event" and ": no drop" checks:
    - "a complete header ending on the last declared octet is read as cut";
    - "a zero-length TLV after the information TLV refuses the Follow_Up";
    - "the last declared octet is not walked as a header byte".
  - "the information TLV is named by any lengthField of 28 or more" finds the fields from the TLV's start. The lengthField 30 row catches it.
  - "word 11 read two octets late" is caught by `#98 plain fu`, `fu w11` and `#98 unknown TLV first`.
- `a030c62` wording:
  - `docs/HDL_DEVELOPER.md` now reads "The first information TLV supplies word 11." and "A malformed chain still refuses the Follow_Up."
  - `docs/TEST_DEVELOPER.md` names the new rows and the defect count.
  - Two engine-suite comments describe the walk, not the removed fixed arm.
- `6e27cd6` `scripts/check_docs.py` loads `check_docs_selftest` (and itself, when run as a script) by its own path. `python3 -I scripts/check_docs.py --selftest` therefore passes from any directory. It reports 127 arms, with output identical to the plain invocation.
- `762fbd6` the parser arm's docstring counts the #87 and #88 mutants as seven (it said six).

Round-2 gates, on a clean clone of the head `762fbd6`:
- Parser suite: 482/482.
- Parser arm: 35/35, every #98 mutant caught on each check it names.
- Engine suite: 2,048 ×3 + 60.
- Engine mutation arm: 136/136 (135 caught plus the control), with every verdict line and all 387 named failure lines identical to base.
- The rest of the repository set: rc 0.
- `make docs`, `python3 -I scripts/check_docs.py --selftest` and `git diff --check 3e3a4e7`: rc 0.
- The OOC reports are identical to round 1's.
- Parent consumer gates, with the gitlink at `762fbd6`: the head column of the table above.

Both reviewers' own planted-mutant scripts were rerun against the head. Each of their 18 mutants is now caught by the harness, the latch mutant included.

Not taken: the 11-bit frame counter wrap on frames over 2,047 octets. It predates this change and lies outside the 1,514-octet integration boundary.

Closes #98
