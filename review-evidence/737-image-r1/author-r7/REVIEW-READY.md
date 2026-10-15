[A615] REVIEW READY
Commit: 2b2e4d2c5b7f43cfc9df5347d99f9fee2c1fb895
Branch: 737-ci-image (local; no push)
Changed: derived workflow inventory and refusal controls; checksum-locked public inputs; separate offline tool stages; build/smoke scripts and generated image lock; rebuilding and digest-consumption documentation.

Validation: all scoped commands returned 0. The image passed every tool-family smoke check without networking. The pinned CPU generator compiled offline in 72 seconds. All 13 repository gate commands passed inside the image, plus 1,501/1,501 navigation controls, 44/44 HDL-reference controls and the committed added-line prose gate (146 added lines, zero findings). Pin/hash/missing-tool/path/corrupt-cache/derived-CPU negative controls passed. The worktree is clean.

Image manifest: sha256:94128cff4711ebfe6d3c5ac10bf88cdc9bac5caff4f4b28fc873fc83897d8427
Recipe digest: aa3be31ce1924fac59d15ba2992f96561c5d8fb4c307c34b28568eae95b1a5fe
Image size: 3,989,528,152 bytes.
Build timing: 393.856 seconds for the uncached native build; 2.896 seconds for the final recipe verification rebuild, producing the same image bytes.

Acceptance evidence: workflow pins are checked against the source lock; every downloaded source has an exact version, size and SHA-256; the build runs with networking disabled; tool versions and smoke commands are recorded; the image guide documents rebuilds and digest selection. HANDOFF.md, PR-BODY.md, lock copies and evidence have been prepared in the assigned management output directory.

Open integration work: manager publication and workflow adoption, independent reviews and hosted/merge validation. Cross-host cold-build byte identity was not tested. No workflow, firmware behavior, linked image or existing test check changed. No push, PR operation, merge or hardware access occurred.
