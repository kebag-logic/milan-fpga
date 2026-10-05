# R472-4 own verdict and ledger, written before any prior review comment on PR #156 was opened

Written: 2026-10-05T08:40:38Z
Exact head: 5123548eb4de35f24d43eb088c12dab70b06d01d, tree 33b4fe59951370299cad36ec1415ead003524d5f

Verdict (independent pass): POSITIVE. No open MINOR, MAJOR or BLOCKER.

Round-3 items, as described in the manager's round-3 assignment (issue #27 comment 5988273127):
- R472-2 F3 (continued ID before optional suffix): fixed. T-ADP-/DELAY(-STRT) fails naming T-ADP-DELAY-STRT (rc 1) in markdown and in //, #, *, > and CRLF forms; the START form passes (receipts/probe_ids_forms.txt).
- R472-2 F4 = R473-2 F3 (self-test plants): fixed. Cases 7-10 plant a missing minus-one base, a line-broken optional member, the F3 composition and both breaks; each asserts rc 1 and the token. The any-minus-one mutant (case 7) and the round-2 continuation order (cases 9, 10) turn the self-test red; so does the real round-2 parser with the head's cases (receipts/mutate_ids_selftest.txt, receipts/round2_parser_with_head_cases.txt). 09 section 7 matches the cases.
- R472-2 F5 (figure clipping): fixed. Both revised SVGs fit under every measured font selection; the round-2 SVGs reproduce both clips as controls (receipts/text_fit.txt). The renderer margin is validated (receipts/probe_margin.txt). wavedrom-check is fresh at the CI-pinned renderer (receipts/make_check.log).
- R472-2 R1 (hosted-status sentence): resolved. The PR body says "not pushed at REVIEW READY" and claims no hosted result for the round.

New, reviewer-owned:
- S1 SUGGESTION (Robustness, Tests): a sibling shorthand wrapped at whitespace (TYP /<nl>-XX, TYP<nl>/ -XX, / -<nl>XX) or an optional segment after a newline before "(" is not read, so a missing member passes rc 0. No such use exists in the tree, and these are not documented forms.
- S2 SUGGESTION (Tests): no negative plant for successive continuation lines. A while->if mutant passes the self-test and fails open on T-ADP-<nl>DELAY-<nl>STRT.
- S3 SUGGESTION (Docs): F02.3 (rxwave) has 0.50-2.55 units of left margin under the measured fonts. It fits, but the same svg_margin would make it robust.

Ledger: Conformance CLEAN, RTL CLEAN, Robustness CLEAN, Tests CLEAN, Docs CLEAN (all at 5123548e, round R472-4).
