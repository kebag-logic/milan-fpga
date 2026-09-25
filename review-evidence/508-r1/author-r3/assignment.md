[A10] Round 3 assignment for PR #560, covering R306-1 and R307-1. Acceptance 2 (R306-1 F4 = R307-1 F2) is decided in 5825732419; no source change. Executor [A297].

1. **CHANGELOG (R306-1 F1 = R307-1 F1):** remove the four processor #116/#113 lines from the historical #530 / `09f9bf38` section (about `CHANGELOG.md:113-116`). That section must be byte-identical to dev `c266432d`'s. The lines stay only in the 990f9652 section.
2. **Line citations (R306-1 F2):** every processor line citation this PR touched must resolve at `990f9652` to the construct it names: `milan_datapath.sv` about :6603-6604 and :6683-6684, and `tb/verilator/pp_shadow/sim_main.cpp:2849`. Use the reviewer's `cite_drift.py`, or equivalent, to prove every one resolves. Prefer citing by construct name next to the line where that reads well.
3. **G8 withdrawal (R306-1 F3):**
   - G8 grades the exact push count to each registered controller.
   - Each push is tied to a named change, with its content graded against the state it announces. The measured count is two: the registrar withdrawal, then the settlement teardown to PASSIVE. Show which is which.
   - The README (:477, :481) and the banner (`sim_nxn.cpp:1667`) state the withdrawal's count.
   - Add a mutant with a duplicated withdrawal push, on a processor copy as the round-1 mutants do. A named G8 check must fail it.
4. Gates as in round 2, including `make -C tb/verilator/milan_dp notify gsi-mutants`, `pp_shadow`, the docs set, and the three docs-check gates.

Review: delta reviews by [R306] and [R307].
