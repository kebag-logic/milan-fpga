R400-2 independent verdict and ledger, recorded before reading any prior review findings
(R400-1 and R401-1 reports and comments) and before any other reviewer's round-2 report.
Recorded at: 2026-09-29T15:37:33Z
Exact head 053f979b9cfc84871ff2e107d43d20bf0e950db4, tree 33087148b197340778ee033f3f2210ac0f629059

Verdict (independent pass): NEGATIVE

Findings from the independent pass:
- N1 MINOR (Tests): a one-cycle Release! first seen in W_ALLOC, W_GWAIT or W_COMMIT is not graded;
  reviewer mutants tx-set-omits-alloc/-gwait/-commit survive tb/maap (191/191) and are killed by the
  reviewer probe PA (Release! absorbed: no INITIAL, the old walk or DEFEND claim continues).
- N2 MINOR (Docs): the PR body's round-1 "What remains" section still states two Release! corners as
  open and out of scope (seed not re-armed on the W_ADDR exit; a frame being drawn or built still
  leaves the wire "although footnote c says Release! sends no PDU"), contradicting the head and the
  round-2 ruling section.
- S1 SUGGESTION (Tests, Docs): "no TX slot request follows the fall" should read "no new slot request":
  at the top a request pending in the pool-access arbiter is retried (W_GWAIT -> W_ALLOC) after the fall.

Ledger (independent pass):
| lens | state |
| Conformance | CLEAN |
| RTL | CLEAN |
| Robustness | CLEAN |
| Tests | UNCLEAN (N1) |
| Docs | UNCLEAN (N2) |
