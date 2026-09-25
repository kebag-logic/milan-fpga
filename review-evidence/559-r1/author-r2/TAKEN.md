[A309] TAKEN

Round 2 on `559-capture-copy`, head `32076148acb0b9122e8c92a44f8e2ebbc8169280`. Executor [A309]; independent reviewers [R324] and [R325].

Authoritative references: assignment 5831090112, R324-1, R325-1, issue #565, the bare-metal clock contract, and the backend hold tick. Scope: reproduce the reviewer probes, measure both shapes at aligned 50 MHz with 16 captures per traffic arm, retain a labelled 8x8 100 MHz comparison, then implement the census/clock gate and documentation corrections. Apply the explicit STOP above 24.5 ms over both 8x8 aligned 50 MHz arms before any firmware change.

Validation: both builder modes with the pinned compiler mapping and without a target compiler; focused NVM suites; all assigned documentation, parser, idiom, contract, traceability, naming and evidence gates. No configuration, product firmware or product RTL change is planned.

The reviewer scripts originally copy the checkout and edit its yaml. To obey this lane's no-other-checkout and no-yaml-change constraints, reproduction uses their build/grade procedure with a scratch-only in-memory clock override and their published C++ phase patch. Product inputs and compiler remain unchanged. Blockers: none.
