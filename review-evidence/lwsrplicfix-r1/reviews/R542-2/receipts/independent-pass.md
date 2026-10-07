# R542-2 independent pass (written before reading any prior review report)

Exact head f800a2bb920c543934d6286a47fe20dde3efa2c5, tree f950b4f333aeb8b2cb267c7c2040645ff6f8050c.

Provisional findings from my own pass:

- N1 (MINOR; Docs, Tests): the PR body does not record every check that the contribution rule requires.
  CONTRIBUTING.md:59-60 requires the run-the-suites commands and the documentation checks, with exit codes recorded in the pull request.
  doc/tester.md:17-24 lists six commands; the body records four (it omits the direct unit runner and the scenario dry run).
  doc/tools/README.md:13-19 lists five checks; the body omits the graph renderer, and doc/tester.md:205 asks for every graph render result.
  The manager archive 844b7333 has no render log either.
  I ran all three at the head: render 27 graphs, 0 failures; direct runner 19885 passes; dry run 3 scenarios untested, rc 0.
- N2 (RESIDUE; Docs): the ctest row reads "1/1 targets"; ctest reports one test ("100% tests passed out of 1"). Fix: "1/1 tests".

Provisional ledger: Conformance CLEAN; RTL CLEAN (no HDL; C builds in both profiles); Robustness CLEAN; Tests UNCLEAN (N1); Docs UNCLEAN (N1).
Provisional verdict: NEGATIVE, pending resolution of R542-1 F1/F2 and carry of F3.
