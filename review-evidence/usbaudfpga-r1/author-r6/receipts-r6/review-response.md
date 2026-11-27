Candidate: `00979246dc22698c0f3a1e4a9796c1a2bcdd03c7`. Executor response for [PR #1024](https://github.com/kebag-logic/milan-fpga/pull/1024), addressing [the internal re-review](https://github.com/kebag-logic/milan-fpga/pull/1024#issuecomment-7219613979). Independent re-review remains required.

| Finding | Correction and evidence |
|---|---|
| N1, MINOR, Docs | Updated the register prose source, then regenerated the reference through the repository generator. Both writable words describe the option, applied low 16 bits, configured resets and Arty split reset values. The read-only publication describes the applied pair. The generator reports fresh: 203 registers, 34 modules, 240 files. See [register reference receipt](register-reference.json). |
| N2, MINOR, Tests | Added a queued next-epoch frame through seven deferred transition offsets. Assertions prohibit consumption or acknowledgement during deferral, require prefill, and score the eventual frame exactly once with no gap. Added an old status record stalled after its third word across capture-state application; capture stays closed until the matching new status completes. Both baselines pass; each of the three requested edits fails its own named runtime assertion. See [ordering controls](ordering-controls.json). |
| R1, packet residue | Prepared corrected historical handoff and readiness copies, using verified public receipt and manifest links. The local historical handoff is corrected too. The [publication patch](public-link-correction.patch) applies only to the evidence packet. Remote publication remains the manager's action. |

| Reviewer probe | Shipped defect | Named assertion | Result |
|---|---|---|---|
| p7 | `bridge_snapshot_epoch` | `BRIDGE_SNAPSHOT_ACK_BEFORE_CAPTURE` | CAUGHT |
| p8 | `media_deferred_frame` | `MEDIA_DEFERRED_FRAME_RETAINED` | CAUGHT |
| p9 | `media_deferred_ack` | `MEDIA_DEFERRED_ACK_AFTER_APPLY` | CAUGHT |

No production defect was found in these windows. The guards were already correct; the missing stimulus is now shipped, and all three controls run in the default regression and full transport campaign. No gate, acceptance criterion or defect oracle was weakened.

All protected network content and modes remain identical to the approved head; both deletions agree. [Network identity](network-identity.json).

Only documentation and simulation entries changed. [Complete tree comparison](source-identity.json) binds the prior physical and million-frame evidence. Both retained complete programming-payload pairs were compared again, and all physical report hashes match. [Retained evidence check](retained-physical-evidence.json). No new route is claimed.

All 44 workflow steps pass, and the builder union covers all 115 checks exactly once. All 80 protocol and transport defects are caught, including the three new ordering controls. The default regression passes. See [workflow results](repository-gates.json), [builder union](builder-union.json), [complete controls](defect-controls.json) and [checkout integrity](checkout-integrity.json). Relates to #1021 until bench acceptance.
