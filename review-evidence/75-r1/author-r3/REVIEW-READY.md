[A391] REVIEW READY
Commit: `9c18068512dec844d24fdff7fe0a3eb0d63c14f5`

Changed: round-3 page and packet corrections for all four assigned items.
- R370-2 F1: declaration-only replay derives 99/100 declared holds. Cycle 1 withdraws, carries only Mt through the hold, then restarts in 0.117736084 s. The page qualifies the DUT-state inference and points #606 to this counterexample.
- R371-2 F5 / R370-2 S1: all three non-stop cycles' Listener events and small records are prepared. Withdrawals arrive +0.009770679, +0.010356881 and +0.025307595 s after disconnect success. No Listener re-declaration follows until after reconnect success. Continuous CRF supports DUT-side attribution at the tapped boundary; #608 owns the internal cause. Stop checks, acceptance and the findings index link #608.
- R371-2 S5 / R370-2 S2: explicit replay classification and consistency checks; optimized execution refused; printed outcomes derived from computed rows. Focused controls pass.

Validation, all rc 0 at this committed head: `docs_check.py` with submodules, without submodules, and without Git metadata; `check_doc_style.py`; `gen_toc.py --check`; `check_em_dash.py --base 8bc97021`; `check_doc_paths.py`; `ci_scope.py --selftest`; `check_baremetal_only.py --check`; `check_feature_status.py --self-test`; `git diff --check`, including the full committed delta. Every table renders with all cells preserved.

Offline replay: all 200 stop results and distributions remain unchanged (100 listener, 97 talker demonstrated restarts). Raw MSRP replay matches all 100 talker TSVs and setup. The round-3 addendum contains HANDOFF.md, updated PR-BODY.md, scripts, results, cycle records and hashes; original packets remain unchanged.

Acceptance: assignment items 1-4 addressed. Refs #75; three demonstrated talker restarts remain missing, AAF remains unmeasured, #606 and #608 remain open. Independent re-review is required. Internal receipt of the withdrawal and its mechanism remain unproved. No hardware action, push or PR edit performed; publication remains pending.
