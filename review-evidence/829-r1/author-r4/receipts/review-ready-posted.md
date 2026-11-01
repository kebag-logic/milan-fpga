[A725e] REVIEW READY
Commit: b9628c8963d436af0dccebb205a5241ece5d9e93 (local, on `cfb79922`; this lane pushes nothing, so PR #831 still reads `cfb79922` until the manager pushes it)
Changed: `sw/builder/test_builder.py` only, no RTL. Gate 1h now gives `sv2v --pass-through` the whole ordered source list, defines and include directories that `syn/yosys/run.sh --emit milan_datapath` states, with the text under test in the datapath's place, and reads the one `milan_datapath` module from that output. R762-3's plant is a committed control. The gate's comment states its purpose and limit: it catches accidental cuts of the two bindings and their defaults, read as the build reads them; it parses and does not elaborate, so a `defparam` or a generate arm that never elaborates stays outside it.
Validation:
- `docs.yml`, every `run:` step on clean clones of this head, then the verifier: rc 0; 64 steps rc 0, 31 hosted-only or package-install steps not run, each with its reason.
- `python3 scripts/ci_builder_legs.py run <leg> ... -- python3 sw/builder/test_builder.py --require-rv32`, as `docs.yml` runs it: leg 0 rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN`; leg 1 rc 0, `ALL GATES PASS EXCEPT 16 NOT RUN`, gate 1h printing `43/43 cuts rejected, 9/9 equal spellings accepted`.
- `git diff --check 1f29f189 HEAD`, the merge base and live `dev`: rc 0.
- Gate 1h's run time, by name on clean clones, `sv2v v0.0.12`, host load 79 to 189: `cfb79922` 41.0 s and 38.9 s; this head 178.5 s and 144.0 s. One read is 2.66 s and at most 883 MB.
- R762-3's `plant_gate1h_r3.py`, unmodified, 4 jobs: rc 0, `not as wanted: 0`, 66 of 66 refused including the finding's four rows, 15 of 15 accepted. At its stated 16 jobs one read passed the gate's 300 s limit, rc 1 with no verdict; that log is kept and the cause is not established.
- Five mutants of the gate's reader: 5 of 5 red, each by name. No `sv2v`: rc 1 by name. Empty environment with `LC_ALL=C`, `POSIX` and unset: rc 0 each.
Acceptance criteria: R762-3-F1 met by its option 1, with the evidence above. No #829 criterion moved: no RTL changed. `gptp_txts` is `cfb79922`'s and the full sweep is `2d534bec`'s, not repeated, as assigned.
Open risks/questions:
- Both reviews are owed at this head: it changes what `Tests` and `Docs` cover. Hosted runs and the local replica need the pushed head, so the longer gate's hosted cost is unmeasured.
- A second plane in a module other than the datapath is now accepted, since the gate reads only the datapath's module. It is a committed control.
- Not taken, as assigned: R762-3-R1, R761-3 RES1 and RES2 stay open as wording residue; R762-3-S1, S2 and R761-3 S1, S2 and the rest of S3 stay suggestions.
- Reviewers: R761 internal, R762 external.
https://github.com/kebag-logic/milan-fpga/issues/829#issuecomment-6564902769
