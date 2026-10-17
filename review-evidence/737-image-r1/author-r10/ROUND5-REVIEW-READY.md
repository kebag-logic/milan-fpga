[A615] REVIEW READY

PR: #738. Relates to #737.
Local commit (not pushed): `4391f353690972f4844cb641b1e77fa94f38cdf4` on `737-ci-image`.

Changed: fixed the Entity shape and derived protocol-processor source-list regressions first. Added a structural syntax census, exact sensitive shell uses, source-state and function-alternative handling, Make environment/override handling, local Python import traversal and capability checks, literal-provenance controls, and component-aware path normalization. Uncensused startup-variable forms refuse; the existing allocator uses retain explicit runtime loader residue. The 45 tool/pin/workflow-provenance records match `e6b86814`.

Validation:
- Final-head Entity shape: 228 checks, zero failures. Protocol-processor source-list check/self-test: rc 0.
- Full docs-check: 79 commands, all rc 0. Full rtl-fast: 36 commands, all rc 0; the unchanged aggregate also returns zero from the recorded local results. Receipts name the exact tested ancestors. Product gate inputs, workflows and submodule pins are unchanged; affected checks were rerun after the validator and lock updates.
- Final inventory controls, 13 source/documentation checks, seven ratchet/Markdown checks, and inventory checks mounted at both `/src` and `/include`: all rc 0.
- Two sequential cold builds: 442460 ms and 452858 ms. Both exports authenticate against the generated lock and match byte-for-byte. Manifest: `sha256:86d7aa16e7d2464baf8e0d246434982838c8174de8c8fa610608cce5b23b5e6c`; size 3931071698 bytes. All 131 image version/smoke records pass.

Limitations: the unchanged full builder command returns zero but reports two NOT RUN arms: the inert `MAKEFLAGS += -e` mutation on this Make version and calibration against the unavailable `mf48` report. Neither is claimed as covered. Runtime-assembled behavior remains located residue. This is local evidence, not hosted CI or a review verdict.

HANDOFF.md and PR-BODY.md have updated Round 5 sections with commands, file:line changes, tool inventory, layers, lock identities, receipts and limitations. The worktree is clean; all eight round-five commits remain local. No push, PR modification, publication, merge, product behavior change or product-test assertion change occurred. Independent re-review is required.
