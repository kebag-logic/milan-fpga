[A581] STOP
Head: bc89f84e6757f8fcddf21958e99f40f17bc0ee1e

The step-1 route prerequisite is absent at the assigned base. `sw/litex/milan_soc.py:2505` and `:2549` leave the mailbox datapath idle; `hdl/milan/milan_datapath.sv:8003` still instantiates the fabric wrapper unconditionally. Parent integration must connect ingress/egress/events, select F0-F4 firmware ownership, and remove ADP/ACMP/MAAP/SRP while retaining fabric AECP. No selected route or new resource figure is claimed.

Step 2 is complete locally: explicit all-fabric, F0-F4 and full-split measurement selections; named population checks; wrapper-free whole-image measurement; unchanged acceptance schema, policy, thresholds and baseline; updated recipe and intermediate ledgers. Commit: Support selected placement resource measurements for M0s.

Validation: 28 final commands, all rc 0. Both positive controls pass; 41 recipe and 180 resource enforcement-removal mutations are detected. The OOC suite passes 58 arms; the resource suite retains 260 arms and 500 seeded cases. Documentation, source, quality and lint checks pass; the committed-head added-line gate passes 339 controls with zero findings. Worktree and pinned dependencies are clean.

HANDOFF.md, PR-BODY.md and log digest/size receipts are prepared. Independent reviews by [R580] and [R581] remain pending. No push, PR operation, RTL change or resource re-record was performed.
