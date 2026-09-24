[A10] Manager note on head `0bf22c935`: generator output only.

At `4eca4540` the builder bank failed one gate, 08: `docs/traceability/gen_module_matrix.py --check` reported `MODULE_MATRIX.md` and `hdl/milan/README-tests.md` stale. I ran the generator unchanged and committed its output as `0bf22c93`, two generated lines. The subject says "for the refused re-declaration leg"; more precisely, the regeneration follows this PR's `docs/traceability/ieee8021q.md` rewrite.

The effect deserves review: `KL_pp_shadow`'s clause column changes from "34.3, 34.4" to "--". `KL_pp_shadow.sv` is unchanged, so the rewritten `ieee8021q.md` no longer names `KL_pp_shadow` against 802.1Q 34.3/34.4. Reviewers: please judge whether that citation was correctly retired or lost.

R296-1 and R297-1 review `4eca4540`. A delta review covers `0bf22c93` afterwards.

