# A177 acceptance ledger for the #400 + #403 bundle

Status: implementation prepared; NOT REVIEW READY. This is executor evidence, not a review verdict or a lens-coverage ledger. The public corrected decisions govern the original examples.

| Criterion | Implementation and focused evidence | Status |
| --- | --- | --- |
| #400 AC1, every SRP leaf | ENDSTATION_BUILDER section 3 rows 35-44 distinguish validators, live consumers and explicit scratch; README-parameters and REGISTER_MAP agree. Gate 40 refuses unsupported VID/timers/TSpec/budget values. | Implemented |
| #400 AC2, fixed timer profile | No timer routing. Gate 40 reads donor JOIN=200, PERIODIC=1000, LEAVE=5000 and PRNG base10000/limit5000; unsupported declarations refuse. Original changed-Leave-time scenario is inapplicable under the public decision. | Implemented |
| #400 AC3, one supported generated startup/default | ADP_SRP_DOM_DEF_VID_C -> milan_datapath -> KL_pp_shadow -> protocol_processor_top -> KL_srp_top. Normal and isolated VID 73 fixtures pass; hard-coded parent binding mutant fails 3 startup/link observations. All three binding hops have source mutation controls. | Implemented |
| #400 reset admission vs firmware policy | Four generated reset combinations; complete CSR main scenario checks real enable/arm outputs and readback; gate 35 compiles real configure_fabric for each and requires OR3. Dropped enable/arm boot mutants fail. | Implemented |
| #400 diagnostic overrides and adoption | PP-wrapper runtime writes VID 19 and AAF VID 23, adopts network VID 5, observes independent diagnostic readbacks, then link-cycles to generated default. Adoption mutant fails the network observation. | Implemented |
| #400 AC4, existing gates and donor adoption | Gates 18a-18d/20a retained and pass. Exact authorized donor8452f564 is clean and reachable from fetched real main; pin table and generated boundary diagram updated. Parent pp_srcs and submodule-doc checks pass. | Focused pass; full banks manager-owned |
| #403 AC1, factory declaration | Omitted/explicit 2000000 agree, other values refuse with Milan5.3.7.6. Every AAF and declared CRF output gets an indexed generated row. Header shape/value/VID mutants fail gate 40. | Implemented |
| #403 runtime/default precedence and indexing | Complete4x4 and8x8 NxN scenarios check GET for every output, runtime 1 ms for one addressed row at a time, and actual AAF/CRF transmitted timestamps. Ignoring runtime store mutant fails 17 checks in the full 1768-check scenario. | Implemented for SET_STREAM_INFO |
| #403 actual restored PTOF | Authorized donor has no PTOF restore/materialization path. No hierarchical injection is labelled restore evidence. Public conflict5781186411 awaits a public decision. | NOT MET / BLOCKED |
| #403 AC2, truthful RX posture | Omitted default is promiscuous; hardware refuses with migration message. Hardware ownership stays board.features.rx_mac_filter. Firmware generated MAC mask8 and TCAM1. Full PP integration measures exact bytes once for station/foreign unicast, broadcast, unregistered multicast at reset and boot on post-filter stream. AVTP pre-filter tap unchanged; fullNxN listener scenarios pass. | Implemented |
| #403 AC3, neutral reset and firmware ownership | AAF_CTRL_RST_C=0 and MAAP_CTRL_RST_C=0 shared by real flops/readback. FullCSR main runs all five shapes; outputs and readback agree. Host-compiled firmware transcripts cover all five shapes, CRF-off variant and all four reset-bit cases. Static4 reset/readback mutants plus compiled old-reset mutant provide controls. | Implemented |
| #403 exact MAAP count | Generated count is len(stream_outputs), AAF plusCRF only if declared. CRF-off/on difference 256 in control word (= one address). FullPP fixtures measure highest-valid granted DA=base+index and first-invalid UNKNOWN_ID with no allocation request. Unconditional+1 boot mutant fails. | Implemented |
| #403 AC4, shape and complete validation | Allconfig entityshape/self-test 136 checks pass; deploy-shape/self-test passes. Focused CSR/PP/NxN controls recorded. Complete parent/PP/gPTP/Yosys/builder/act/hosted/current-dev candidate remain assigned to manager. | Required manager work unrun |
| Parent warning-policy gate | check_cpp_idiom reports donor tb/pp_top/Makefile supplementary CFLAGS group lacks repeated Wall/Wextra; common VFLAGS includes them but current checker requires every group. No donor edit, pin substitution or ratchet growth. Public conflict5781426819. | FAIL / BLOCKED |
| Reviews/merge/completion | R249 and R250 are reserved, neither invoked here. No selfapproval, push, PR, act, hosted polling or merge. Historical donor PR13/6 continuity UNKNOWN and PR13/9 negative-merge remain disclosed. | Not completed |

Public conflicts:
- https://github.com/kebag-logic/milan-fpga/issues/403#issuecomment-5781186411
- https://github.com/kebag-logic/milan-fpga/issues/400#issuecomment-5781426819

No acceptance criterion was silently removed. Until a public disposition resolves the PTOF contradiction and the required donor policy check, no REVIEW READY comment is authorized by the readiness condition.
