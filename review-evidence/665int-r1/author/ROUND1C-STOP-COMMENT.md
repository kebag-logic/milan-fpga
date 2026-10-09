[A582] STOP
Head: 7c1b52bee26b497080ee22b1c1986109f80a5ee7
Branch: 665-int-split. Resumed round 1c; no repository edits or commits, worktree clean.

Ruling 6087462816 accepts packed vectors versus separate messages. That difference is now accepted and is not this STOP. Its separate requirement is the same ordered list of decoded events per transmit opportunity.

A fresh run of the prior identical-input probe reproduces:
- Fabric: `(3, 1122334455660001, New, Ready, no LeaveAll)`, then `(3, 1122334455660002, New, Ready, no LeaveAll)`.
- Split: the same two tuples in reverse order.

Both outputs are structurally valid; Ethernet headers match. The prior diagnostic sorted records and proved set equality. The new independent Clause 10.8 decoder preserves encounter order and duplicates. Ordered equality fails with rc 1. An order-preserving packing-only change passes. All seven required capture-plant categories, plus nine further controls, are detected (16 total).

This is a comparison-contract mismatch, not a claimed standards violation. The ruling also says no firmware encoding work. I have not silently sorted events or changed either implementation. Please record whether canonical ordering within each transmit opportunity is authorized while preserving multiplicity, or whether wire encounter order must be made equal in a separately authorized change.

HANDOFF.md and PR-BODY.md are updated, with fresh captures, the independent decoder, exact lists, tests/plants, file:line anchors, coverage/gate tables and size/hash receipts. This remains a prerequisite probe, not a complete two-placement datapath simulation. Largest-shape/two-interface comparison, the four-category exact ACMP integration ledger and source plants, both images, linked size against 224 KB, resource/timing evidence and the full acceptance gates remain incomplete. Implemented integration-ledger rows: 0.

No default, map, pin or generated source changed. No push, PR operation, merge, device operation or resource re-record was performed. Independent review remains pending.
