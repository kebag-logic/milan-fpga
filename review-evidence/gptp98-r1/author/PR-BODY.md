[A730] Walk the Follow_Up TLV chain to the information TLV (#98)

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

Parser suite: 473 checks (378 at base). Mutation arm: 28 defects and the control (15 defects at base). Every defect fails each check it names.

| Row (`tb/verilator/parser/sim_main.cpp`) | Expect | Planted parser defect that fails it |
|---|---|---|
| `#98 plain fu` | accepted; w0..w5, w11 as built | (the reference for the rows below) |
| `#98 unknown TLV first` | accepted, w0..w5 and w11 as the plain case | a TLV ahead of the information TLV refuses the Follow_Up; word 11 read at the fixed octets 68..73 |
| `#98 three unknown TLVs first` (zero-length, PATH_TRACE-typed, 00-80-C2 subtype 2) | accepted, as the plain case | a zero-length TLV ends the walk; the information TLV named without its organizationId and subtype |
| `#98 unknown TLV first, padded` | accepted, as the plain case | the walk reads padding past messageLength as a header |
| `#98 second information TLV` | accepted, word 11 from the first | a later information TLV is read again |
| `#98 identifiers at octet 6` (another OUI's 30-octet TLV) | accepted, word 11 from the real TLV | the information TLV named without its lengthField |
| `#98 unknown TLVs after` | accepted | (control) |
| `#98 no information TLV` | refused, no word 11 | a Follow_Up is accepted without its information TLV |
| `#98 information TLV past messageLength` | refused, no word 11 | a TLV value past messageLength is walked |
| `#98 trailing TLV past messageLength` | refused | a TLV value past messageLength is walked |
| `#98 header ends messageLength, value to come` | refused | an EOF header's own overrun is not refused; a TLV value past messageLength is walked |
| `#98 header cut after 1, 2, 3 octet(s)`, each with and without padding | refused | a TLV header cut by messageLength is accepted |
| `#98 odd lengthField` | refused, no word 11 | an odd lengthField is walked |

The existing #11 rows (`fu tlvType 0x0008 drop`, `fu orgId 00-1B-19 drop`, `fu orgSubType 2 drop`) also name the "information TLV named without its tlvType", "without its organizationId and subtype" and "accepted without its information TLV" defects.

Against the base RTL, the new rows fail 31 checks: the unknown-TLV-first rows (no event, one drop) and the trailing-chain refusals that base accepted.

A cycle trace of base and head RTL over Follow_Up (plain, trailing TLV, padded), Sync, Pdelay_Resp, Pdelay_Resp_Follow_Up, Pdelay_Req and Announce frames is identical, line for line. Word 11 lands at frame byte 73 and every event at the same cycle after EOF. With a 12-octet TLV first, word 11 lands 12 bytes later and the event at the same cycle after EOF.

## Gates

Repository, at base `3e3a4e7` and head, all exit 0: `make contract`, the ucpu, parser, engine run, gaskets and tsngen suites, `make -C bench/arty test`, `make lint`, `make docs`, `make diagrams-check`, the OOC clock selftest, `make ooc`, and a clean tree after the runs. The engine mutation arm, `make -C tb/verilator/engine mutants`, is 136/136 at base and at head, with identical verdict and named-failure lines. It ran on the commit before the docs-gate move, whose `hdl/` and `tb/` trees are identical to the head's.

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

| Gate | Dev pin | This head |
|---|---|---|
| `check_cpp_idiom.py`, `check_py_idiom.py`, `xvlog_gate.py --check`, `check_rtl_source_lists.py` | rc 0 | rc 0 |
| `sw/builder/test_builder.py` | rc 0 (one host-dependent arm not run) | rc 0, the same |
| `make -C tb/verilator/gptp_shadow` | 325/325; controls 9/9 | 325/325; controls 9/9 |
| `check_port_contracts.py`, `measure_naming.py --check`, `measure_test_evidence.py --check`, `docs_check.py`, `lint_rtl.py --check` | rc 0 | rc 0 |
| `make -C tb/verilator/milan_dp gptp`, `gptp-lat` | 210/210, 210/210 | 210/210, 210/210 |
| `make -C tb/verilator/milan_dp_gptp` | RESULT PASS (151 + 6 + 20 + 14 + 14) | RESULT PASS; its 89 event, progress and verdict lines identical |
| `make -C tb/verilator/milan_dp_gm_steps` | 6/6 | 6/6 |
| `gptp_plane`, `gptp_txts`, `gptp_tables` | rc 0 | rc 0 |
| `make -C tb/verilator/tsn_fuzz ptp` | 675 pass, 0 fail | 675 pass, 0 fail |

With the gitlink at plain main `3e3a4e7`, `check_py_idiom.py` fails: "long function 10 > ratchet 9", "unannotated public function 3 > ratchet 0". The docs-gate commit above removes that failure.

Closes #98
