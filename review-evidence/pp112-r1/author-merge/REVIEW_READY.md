[A273] REVIEW READY

PR #114 / issue #112 merge round: new head `f222f6b96328c8eb0f4d2c5c3470ebd365e51fdc` on `112-stale-grant`. One merge commit, parents `ae7f531bc97a7277116e0df78e70c84396c499d0` and `7a47f5788ff504f099a47ad4407c340771bb6bdb`; one-line subject with no body or trailers.

Resolved `syn/ooc/README.md` keeping both the SRP admission area/pending-round notes and the #43/#49 GSI area rows. Resolved `tb/srp_top/README.md` to the measured merged total of 1,531 checks, preserving both sets of notes.

Reviewed all six clean overlaps against both sides: `hdl/srp/KL_srp_top.sv`, `hdl/top/protocol_processor_top.sv`, `tb/srp_top/sim_main.cpp`, `tb/srp_top/srp_top_wrap.sv`, `docs/architecture/10_srp_engine.md`, and `docs/guides/integrator.md`. The source admission hold remains separate from GSI's sink registrar/listener readers and failure-change notification; no interaction defect found.

Validation at this head (all enclosing gates rc 0):

| Gate | Result |
|---|---|
| Every processor CI gate, plus diagram lint | PASS, including link/matrix/waveform/staleness checks, HDL lint, generated module matrix, 46-build historical figure gate, and portability/memory mapping |
| Full suite bank | 33 suites, 1,008,919 canonical checks, zero failing suites; both PRs' suites included |
| `gsi_mutants.py` | All 13 mutants detected by named checks; golden and restored controls pass 488 checks each |
| SRP admission mutant runner | 12/12 verdicts: three controls and all three mutants across both unit shapes and the SRP integration suite |
| Parent C++/Python idiom and RTL source lists | PASS with the new processor head staged |
| Parent `make -C tb/verilator/pp_shadow -j8` | 371 checks, zero failures; parent index reset afterward |

`HANDOFF.md` and raw gate logs are in the assigned output directory, with conflict file:line references, the complete overlap review, and gate tables. Processor tree clean; parent HEAD unchanged and no staged changes. No push, PR edit, parent commit, main-branch merge, or hardware action. Ready for independent review.
