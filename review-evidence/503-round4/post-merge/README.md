# PR #503 post-merge proof

Authorized candidate `2a2007cff57bd2a01254e1da7c43ec73b9d8d4b3` merged into dev as `b17580b91deb11f3441dfc5d7f9fafe539d929b8` at 2026-09-21 17:35:41 UTC. The [actual tree and parents](merged-tree-proof.json) match the validated candidate tree `1fc6e7edcfc5a3e1f055ed1f73ba70614996977e` and expected base/head. The validation checkout is clean at the merged commit.

[All three containment commands](CONTAINMENT.json) exited 0 at that merged commit: implementation branch containment; the last 20 merged PRs; review integrity over the last 20 merged PRs. Original command logs are included byte-for-byte, with SHA-256 digests in the receipt. Neither review remained in flight and the implementation branch stopped moving before merge. Evidence branches remain unmerged and preserved.

The maintainer [authorized this exact merge and gave standing automatic-merge authorization](https://github.com/kebag-logic/milan-fpga/pull/503#issuecomment-5764802190). Future eligible merges proceed after two independent positive reviews and all existing completion gates, without another per-PR permission prompt. [Authorization receipt](merge-authorization.json).

[All four hosted workflows](post-merge-hosted.json) succeeded at the actual merge commit: docs 35633016573, elaborate 35633016157, rtl-fast 35633016231 and rtl-full 35633016093. The [full RTL run](post-merge-rtl-full.json) has a successful selector, all five Verilator shards, all four Yosys shards, and both required aggregate contexts. The physical gPTP job is explicitly skipped for a push; it is reserved for nightly/manual runs. This result is not a hardware or silicon claim.

[Final completion proof](completion-proof.json) verifies the unchanged implementation branch, exact live dev merge, clean merged checkout, no running author/reviewer/validation unit, and #500 Closed/Done. The Project was moved Done only after all containment and hosted checks passed. #70, #408/#409, #501/#502 and processor #15/#20/#92/#93/#94 were verified still Open. The page stays Proposed; normative adoption/reconciliation and implementation are later work.
