[R400] POSITIVE - exact head 47afa74d5cb7cf67ec1f606a0b8ea05fda3e3346

DRAFT (independent pass complete; prior public findings not yet read). Verdict and ledger below were fixed before reading any prior review.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | merge composition vs issue #66 assignment 5910732518; hdl diff both sides; no hdl/maap or tb/maap change | R400-4 | 47afa74d5cb7cf67ec1f606a0b8ea05fda3e3346 |
| RTL | CLEAN | protocol_processor_top.sv:1721-1753, 2175-2240, 3690, 3871-3878; KL_aecp_engine.sv:654,1784-1814 | R400-4 | 47afa74d5cb7cf67ec1f606a0b8ea05fda3e3346 |
| Robustness | CLEAN | merge-tree replay; per-path classification; gate-enable-dropped full-run probe | R400-4 | 47afa74d5cb7cf67ec1f606a0b8ea05fda3e3346 |
| Tests | CLEAN | run_suites; both campaigns full; D3/GSI/name-write drivers; focused modes; ledgers | R400-4 | 47afa74d5cb7cf67ec1f606a0b8ea05fda3e3346 |
| Docs | CLEAN | PR body Round 4; tb/pp_top README MP+AD; ledgers; .gitattributes; hdl.yml | R400-4 | 47afa74d5cb7cf67ec1f606a0b8ea05fda3e3346 |

Candidate SUGGESTION S1 (Docs): tb/adp_engine/README.md:184 dated count 7,924; at the merged head the same 4 failures are of 7,929 default-build checks.
