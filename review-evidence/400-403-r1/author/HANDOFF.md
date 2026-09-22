# A177 handoff: #400 + #403 declaration bundle

**Status: blocked; NOT REVIEW READY.** Implementation is committed locally at `17e2cf6928865bbf1cabcec4800483bef685900f` (tree `2a2b1e3e1463d87d84fbc673a19cf74d3be0d1c1`), branch `400-403-declaration-truth`, based on `483a133ed08867ea0d300d2b4a027b5b48a4282f`. No push or PR was made. The one-branch/one-PR exception and roles were assigned publicly before editing. R249 internal Codex and R250 external Opus remain the independent reviewer reservations; no review or selfapproval occurred.

## Blocking decisions

1. Actual PTOF restoration cannot be preserved or measured at the authorized donor: it has no materialization path. Public conflict: https://github.com/kebag-logic/milan-fpga/issues/403#issuecomment-5781186411 . Options are recorded there. The recommended clarification is SET_STREAM_INFO/stored-value precedence in this lane, with actual persistence/restore explicitly still unmet under #500/#70. This recommendation has NOT been treated as an approved change.
2. The exact authorized donor introduces a parent warning-policy finding: `protocol-processor/tb/pp_top/Makefile` has a supplementary CFLAGS group without repeated `-Wall -Wextra`, while the parent checker requires every group. The common flags include them, but `check_cpp_idiom.py` exits1. Public conflict: https://github.com/kebag-logic/milan-fpga/issues/400#issuecomment-5781426819 . No donor source change, substituted pin or ratchet growth was made.

`REVIEW-READY.md` records this blocked status. No REVIEW READY comment was posted.

## Implementation

- Supported VID 2 is generated through the actual parent/wrapper/donor-top/SRP-child path. Every SRP leaf has a consumer, validator, or explicit scratch role. Fixed timer assertions and derived TSpec refuse unsupported shipping overrides.
- Every declared AAF/CRF output has a generated 2 ms factory row. The existing valid per-output AECP store takes precedence; runtime 1 ms affects only its addressed output in GET_STREAM_INFO and transmitted timestamps. No listener timing rejection was added.
- RX posture is named promiscuous and programmed explicitly at boot; ambiguous hardware policy refuses while hardware-presence ownership remains independent.
- AAF/MAAP reset flops and readback share neutral 0 constants; generated firmware words own active VID/control and exact output-count allocation.
- Only PP pin 8452f564294300a82d56eed464276576f65f4d58 was adopted after fetching real donor main and verifying ancestry. SUBMODULES and generated boundary diagram match. gPTP, axis and external gitlinks are unchanged. Donor source is clean. Historical donor PR13/6 continuity UNKNOWN and PR13/9 negative-merge baseline remain disclosed.

## Focused evidence

`ACCEPTANCE.md` maps every corrected criterion. Each run has a raw `.log`, `.json` with command/exit/head/tree/status/times, and captured `.diff`. Runs before the commit explicitly say **uncommitted working tree** and are not relabelled as exact-head evidence. Only the run metadata establishes a run identity; suffixes do not. The earlier `-head` batch was followed by a generated-comment freshness correction and is not final-head evidence. `-final` runs are recorded separately after that correction. The supplied Verilator 5.050 wrapper and underlying executable hashes are in `tool-identity.txt`; all compiler jobs are bounded 8. No Docker/act, shared installation or hardware was used.

- Full NxN 4x4: 1768 checks;8x8: 3448 checks, both 0 fail. They include all 5/all 9 output default/runtime GET and wire timestamp observations plus unchanged listener payload scenarios.
- Full PP-wrapper fixtures: 402 checks each,0 fail for CRF off, CRF on and test-only generatedVID 73. Post-filter reset/boot frames are compared byte-for-byte for all four destination classes; MAAP source boundaries and Domain behavior are measured.
- Full CSR shape matrix: all five YAML shapes plus reset-bit fixtures1,2,3 (default 0 covered by ordinary shapes),391 checks per run, 0 fail. Initial complete CSR bank also passed; final-head repetition is separately logged as csr-final.
- Focused builder groups 18a-18d,20a,23b/23c,35,40 pass. Ten full firmware boot transcripts,8 boot mutants,9 binding/reset mutants,3 header mutants per config,24 unsupported declarations.
- Entity shape self-test 136 checks passed; deploy shape self-test passed. RX filter 78 checks plus 5 binding and 5 elaboration controls passed. PP source-list, submodule docs, Python idiom, documentation style, port contracts, hygiene and lint-pragma checks passed. The C++ warning-policy gate remains failed solely on the donor finding above.
- Actual compiled negative controls: VID binding 3 failures; suppressed Domain adoption 1; ignored runtime offset store 17; stale AAF/MAAP reset flops 2. These raw exits are deliberately1 and are labelled mutants. No positive test was shortened or disabled.

Early fixture failures remain in the evidence: an inherited make-dry-run echo token; a boundary probe placed after the existing backend reset; the old TCTX test's deliberate uid5 interfering with the new output census; and copied-source waiver paths. They were fixture/setup defects, corrected without deleting scenarios or weakening observations. Early style/generated-diagram findings were fixed. `mutation-observations.json` lists the intended final mutant failures.

## Manager-owned work still unrun

The user expressly reserved complete banks and publication to the manager. Required donor commands are protocol-processor/scripts/run_suites.sh and make -C gptp-processor; their root integration counterparts remain specified by SUBMODULES.md. Required full parent Verilator (`scripts/run_all_suites.sh`), Yosys (`syn/yosys/run.sh`), full builder (`python3 sw/builder/test_builder.py`), donor PP/gPTP banks, full lint and Vivado front-end, remaining complete docs/quality/workflow banks, trusted live-dev act replication, protected hosted contexts, independent reviews and their exact-head lens ledger, and current-dev candidate-merge validation are UNRUN here. `CONTRIBUTING.md`, `docs/testing/CI_WORKFLOWS.md` and `docs/reference/SUBMODULES.md` remain the command authorities. Do not replace any of these with focused results.

Resolve the two public blockers before treating this as review-ready. If an authorization changes the frozen contract or exact pin, record it publicly and resume in this lane. `PR-BODY.md` is a draft artifact only and contains both closing references; publishing it before blockers are resolved would misstate readiness.

## Reproduction

Run from the candidate checkout; prefix shell commands with `rtk proxy`. The scripts in this evidence folder use the checkout's own Makefile recipes and full scenarios:

- `python3 focused_builder.py` (with this folder's script path)
- `python3 run_csr_shapes.py` (all five shapes and reset combinations)
- `python3 run_pp_fixture.py off`, `crf`, or `vid73`
- `python3 run_nxn.py obj_nxn` or `obj_nxn8`
- Mutation arguments: `run_pp_fixture.py vid73 binding`, `run_pp_fixture.py vid73 adoption`, `run_nxn.py obj_nxn offset`, `run_csr_shapes.py reset-mutant`; expect completed simulations with exit 1 and the named observations.

Use `run.py LABEL COMMAND...` to capture a fresh honest identity. Fixture headers and mutated parent source copies are preserved here for inspection. Donor source is never mutated. The scoped tool path is the one explicitly supplied by the owner; set MILAN_DECL_VERILATOR to an independently verified equivalent 5.050 installation on another host. All scenario code changes are in the committed repository tests.
