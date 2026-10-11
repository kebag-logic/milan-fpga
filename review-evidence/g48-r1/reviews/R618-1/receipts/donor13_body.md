closed closed=2026-08-22T18:13:34Z
The parent integration has moved beyond the status described by this repository's README.

## Problem

The pinned commit is integrated by `milan-fpga` through `KL_gptp_shadow`, and parent PR #135 makes that plane the default owner. The current README still says the engine only intends to take over the softcore duties, calls parent-side integration the next step, and describes the software daemon as the current publication owner.

That makes the donor repository's front page contradict its implemented parent contract and the exact submodule revision consumers inspect.

## Scope

- State that the implemented state machines are consumed by the parent wrapper.
- Describe the default fabric ownership and the explicit option-off comparison path without claiming #117's still-open two-board acceptance.
- Update the integration-contract wording from future tense to the implemented RX, TX, PHC, and atomic-publication seams.
- Keep the remaining protocol and physical-acceptance gaps explicit.

## Acceptance

- README statements match the current engine RTL and the `milan-fpga` parent integration.
- Parent integration is not described as future work.
- Software mirroring is labeled option-off compatibility, not the product default.
- No claim implies that the open two-board/rootfs acceptance has completed.

Authoritative parent references: kebag-logic/milan-fpga#116, kebag-logic/milan-fpga#117, kebag-logic/milan-fpga#135.

Priority: Urgent
Size: S

