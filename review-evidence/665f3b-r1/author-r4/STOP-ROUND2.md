[A612] STOP — required hosted proof is pending

Local head: `651ccb5aea1bc4d99f356503c188947d39e0c9e4` on `665-f3b-parent`.
Three new commits; clean worktree and required dependencies. No push or PR edit.

Round 2 corrections are implemented: DA_GATE uses the core's per-source predicate; scratch Git maintenance is disabled and only disappearing-file deletion errors are tolerated; dependent service bounds and adopted-pin documentation are corrected. The stack remains `70936b77`.

Local validation, all final runs rc 0:

- Unchanged R583-1 owner probe passes. Listener/probe validity controls pass at IF1 and IF2.
- 520 control, 76 AECP and 278 SRP mutations caught; zero escapes. Six harness mutations and 38 service-document controls caught.
- Coverage: adjusted 100% lines and branches across 30 files.
- Host boundary: 2854 compiled sources / 3084 invocations; 112 boundary, 126 pin and four figure controls pass. Verilator boundary: 829 sources / 926 invocations; six boundary, 126 pin and four figure controls pass.
- All 15 before/after image pairs pass linked-image audits; maximum Release growth is 1304 bytes against the unchanged 2048-byte ceiling. Default BIOS and AEM descriptor remain byte-identical.
- Documentation, source-list, evidence-reader, dispatch, generator and lint gates pass. HANDOFF.md and template-based PR-BODY.md include the Round 2 evidence and bounded reproduction commands.

The round 2 assignment requires hosted `rtl-fast`, including `firmware-boundary` and `firmware-verilator`, to pass at the new head, and prohibits pushing. PR #736 still points at `db29bdd07529fbc697b7956827092f64b1241714`; hosted success at this unpublished candidate cannot be established. That acceptance item remains open for the integration owner after publication, followed by independent re-review. No author approval is claimed.
