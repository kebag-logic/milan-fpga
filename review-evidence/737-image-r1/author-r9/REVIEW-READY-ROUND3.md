[A615] REVIEW READY — PR #738, round 3

Commit: e6b86814e6844ef61ba46a867a0fdbfbb925cceb

Implemented assignment 6167899804 with amendment 6167966247:
- Closed command table: classify literal commands, refuse unknown names/forms, follow scripts and Makefile targets, and record immutable container/service images. Reviewed executing/network Python scripts carry reasons and content SHA-256 pins; undeclared or changed scripts refuse. Runtime construction is listed as residue.
- Added and verified all 185 retained Ubuntu package fallbacks, including HTTP-404 and corrupt-download controls.
- Config identity now comes from the authenticated exported manifest. Both cold builds completed with buildx v0.38.0 despite its missing config-digest metadata key.
- Patch self-test passes without configured global/system identity. Documented SDK HOME link resolves GCC 14.3.0; the guide names the real compiler-override consumers.

Validation: two --no-cache builds, both rc 0; manifest/config and all 14 compressed/uncompressed layer identities match. Both exports passed full authentication/privacy scans (526 authenticated public-source allowances). Offline version and functional smoke passed, rc 0. Inventory, build/integrity/privacy/patch controls, package closure, bare-metal scope and all 738 controls, Python idiom, documentation and whitespace checks passed. Exact commands and superseded setup failures are recorded in the updated packet and image guide.

Manifest: `sha256:86d7aa16e7d2464baf8e0d246434982838c8174de8c8fa610608cce5b23b5e6c`
Config: `sha256:62b56e1ab52dce1a1914e8469429c014e69a465e74e0bdb9a7d8bf4a626b2776`
Image: 3,931,071,698 bytes. Cold Docker build times: 434,933 ms and 398,716 ms. Offline smoke: 30,028 ms.

The base and all tool layers match round two byte-for-byte; only the source-declaration layer changed. The accepted round-two grouped builder campaign remains historical evidence and was not rerun. Same-host reproduction only; runtime residue requires manual review.

HANDOFF.md and PR-BODY.md have Round 3 sections, current file/line references, inventory, layers, lock and evidence. Three local one-line commits; checkout clean. Workflow, HDL, firmware, linked-image patches and product-test assertions are unchanged. No push or PR edit. Independent re-review, publication and workflow adoption remain pending.
