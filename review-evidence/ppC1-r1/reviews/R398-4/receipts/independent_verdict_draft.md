# R398-4 independent verdict draft (written before re-reading any public review finding)

Head 99bfd4bc3180bab97d47f63056513fb39eea6a37, tree d8ec1053 (unchanged since R398-3).
- R398-3 F1: RESOLVED by the PR-body amendment (edit 2026-09-29T13:52:15Z). f1_body_check.py PASS on the current body, FAIL on the round-3 revision (control).
- Body scope: one changed region, inside item 1 of the composed-head note; closing references exactly #29 #64 #65 #108.
- Source confirmation: srp_top 2200/2200, ARMDELAY 0 at 3/4/8/16; make check, gen_matrix --check, git diff --check rc 0.
- Draft verdict: POSITIVE. Lenses: Conformance, RTL, Robustness, Tests CLEAN (carried from R398-3 on identical bytes, confirmed); Docs CLEAN.
