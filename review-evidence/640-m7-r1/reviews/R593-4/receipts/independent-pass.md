[R593] NEGATIVE - exact head 412e3f6c8c402bce63e94c291d2782b5579aaa1d

Round R593-4, independent external delta review of issue #640 / parent PR #713 and donor PR #78. Tree: `3a0b668761728b2e9fcc328f71f67f885ef3d11e`. Donor: `e4869fd0c42889b2ac806587cc5c78afb1c33461`.

All five lenses have been applied independently. This initial verdict and ledger were written before reading prior public review findings or another reviewer's report. Prior-finding reconciliation and final packet checks follow separately.

R593-4-F1 | MAJOR | Conformance, Tests | `scripts/suite_shards.py:160`, `scripts/suite_shards.py:239`, `.github/workflows/rtl.yml:219` | Merged inventory omits the M7 suite's duration.

Authority/evidence: the round-four assignment requires integration with dev `fa820988`. The imported scheduler requires every default suite in `SUITE_SECONDS`; its new-suite procedure is at `scripts/suite_shards.py:54`. `tb/verilator/gptp_tables/Makefile` makes M7 a discovered default suite, but the duration table has no `gptp_tables` row. Exact-head `python3 scripts/suite_shards.py --selftest` exits 1, naming that missing row. Disposable copies of both parent revisions' scheduler inputs pass. All five hosted workers in run `38524965102` fail the same prerequisite.

Impact: every hosted simulation shard stops before its suites. The serial full sweep also aborts at `scripts/run_all_suites.sh:291`. Passing the focused M7 campaign and CI scope/event checks cannot supply the missing full-suite evidence.

Required outcome: integrate M7 with the scheduler's duration/provisional inventory and capacity contract, preserving complete/disjoint suite ownership and the existing timeout/headroom rules. Follow the documented new-suite procedure; do not remove M7, skip the prerequisite, or raise a budget to hide the failure.

Verification: the focused scheduler selftest must pass on the corrected head, alongside scope/event checks and complete suite selection. The manager must obtain the required successful hosted contexts and current-dev candidate evidence. `receipts/inventory-probe.log`, `receipts/inventory-head.log` and `receipts/hosted-failure-context.log` reproduce the defect.

R593-4-D1 | RESIDUE | Docs | PR #713 body, Status / How to get into the same state / Known limitations | Publication wording still describes local-only heads.

Authority/evidence: the read-only PR response names published head `412e3f6c8c402bce63e94c291d2782b5579aaa1d`, while the body says both heads remain local and the latest commits are not remotely available.

Impact: stale publication wording only; no measurement, test, figure, verdict or protocol claim changes.

Exact fix: replace the Status local-only sentences with “REVIEW READY at the published parent and donor revisions listed above.” Replace the reproduction introduction with “Check out the published parent revision and initialize its pinned submodules.” Qualify the no-push/no-PR-edit statement as the executor's implementation-stage history. The manager carries this wording change on the residue checklist.

Verification: read the corrected body against the published parent/donor heads. This residue leaves Docs clean under the owner's rule.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | Issue #640 frozen M7 scope and round-four rulings; parent/donor merge identities; `scripts/suite_shards.py:54,160,239`; `receipts/inventory-probe.log` | R593-4; F1 open | `412e3f6c8c402bce63e94c291d2782b5579aaa1d` |
| RTL | CLEAN | Parent M7 RTL blobs and automatic merge comparison; donor timer, parser and generator provenance; `receipts/merge-style-audit.log`; fresh M7 lockstep | R593-4 delta; unchanged M7 artifacts retain R593-3 coverage | `412e3f6c8c402bce63e94c291d2782b5579aaa1d` |
| Robustness | CLEAN | `tb/verilator/gptp_tables` consumer checks, census, declared limits and 26 controls; donor parser before/after runtime output; clock defect fixtures | R593-4 delta | `412e3f6c8c402bce63e94c291d2782b5579aaa1d` |
| Tests | UNCLEAN | Focused checks pass; scheduler inventory and all five hosted shard prerequisite failures establish F1 | R593-4; F1 open | `412e3f6c8c402bce63e94c291d2782b5579aaa1d` |
| Docs | CLEAN | Donor `docs/MANAGER.md:34,72,103,113`; parent measurement histories, eight donor-link pages, generated diagrams and ROM ledger; PR revision-qualified figures | R593-4 delta; D1 wording residue | `412e3f6c8c402bce63e94c291d2782b5579aaa1d` |

The donor reviewed by every row is `e4869fd0c42889b2ac806587cc5c78afb1c33461`.

The donor merge has ordered parents `18dd997b` and `61d486e9`; only `docs/MANAGER.md` differs from the automatic merge. Both measurement histories survive. The following style commit changes only that guide, the clock checker's fixture organization/docstring, and four parser declarations. Production clock-check functions and CLI remain identical. The fixture list, required findings and runner compare structurally equal. The functions span 95, 30 and eight lines. Both clock selftests pass 30 arms. Both parser simulations pass 337 checks, with identical 2,049-byte runtime output (SHA-256 `f521be7f25439184b14991a9667aabeb05d84a3b98f27df2b6dbe2ea2e8e556c`).

The parent has ordered parents `354f7818` and `fa820988`. No code differs from the automatic merge; manual results are documentation, generated artifacts, the donor gitlink and ROM records. Its M7 RTL, complete table-test subtree and README generator are byte-identical to round 3. Both idiom gates pass; their budgets are unchanged from both parents, and gate code equals incoming dev. There is no M7-specific exception. Fresh generated ROM bytes match `a435fba6167238268fa9074dd4645dd03380e56ff1eeea273fd3fc2fcecab9fd`; usage is 1,016 words and `FUTO@249`.

Fresh local checks pass: M7 baseline 36/36, all 26 original mutations caught by their named checks, one-valued table generation, Python/C++ idiom gates, `ci_scope.py --selftest`, `ci_events.py --check` (2,174 items), six exact submodule pins, eight donor-link pages and both generated diagrams. The diagrams were also visually inspected. Builds and mutation copies reside only in packet `scratch/`; all processes were awaited. No source edit was needed or made.

The source validation is distinct from the final current-dev candidate. No manager source bank at this head is claimed. Public author evidence reports the isolated offline workflow selftest passing; this reviewer did not run that host-side script or a container. Physical calibration was NOT RUN. Skipped physical contexts and field skips provide no hardware proof. Full parent/donor/processor/synthesis/builder banks were not run by this reviewer.

Hosted snapshot: Yosys completed successfully; all five simulation shards and their aggregate failed. Physical gPTP was skipped. Other contexts were still running when inspected. Hosted and local workflow acceptance remain manager duties. The final current-dev merge candidate, builder/native banks, required contexts, two independent reviews, post-merge containment and the following day's area measurement remain pending. The issue's overall resource closure is not claimed by this intermediate M7 review.

