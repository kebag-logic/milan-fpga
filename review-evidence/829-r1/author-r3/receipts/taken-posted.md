[A725d] TAKEN
Branch: 829-mii-gptp (local, continues 2d534bec; PR #831 round 3)
Authoritative references: R761-2 F1 and R762-F9 at 2d534bec, with their plants and residue; AGENTS section 6, Tests; hdl/milan/milan_datapath.sv; sw/builder/test_builder.py gate 1h
Interpreted scope: make gate 1h read the code rather than the text, so a binding or default that is commented out, inside a block comment or inside a dead preprocessor arm is refused. Every plant in both reports becomes a control that must fail, and the shipped wiring passes. Apply the two reports' residue exactly. No RTL.
Validation plan: every run step of docs.yml as its jobs run it on a clean clone of the head, through the round 2 runner and verifier; sw/builder/test_builder.py as the docs workflow runs it; make -C tb/verilator/gptp_txts; git diff --check against the merge base. No full sweep: only a builder test and comments change.
Blockers: none
