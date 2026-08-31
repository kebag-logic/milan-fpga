# Findings retained in the bare-metal product tree

This directory contains current hardware findings that still inform the
shipping Milan v1.2 design. Superseded target-runtime campaigns and operational
logs are preserved in Git history, not in the checked-out product tree (#259).

## Current entries

| Document | Scope | State |
|---|---|---|
| [ADP_SHAPE_STATIC_0727.md (historical)](ADP_SHAPE_STATIC_0727.md) | Generated ADP/AEM shape must match the instantiated stream geometry | Fixed; guarded by `scripts/check_entity_shape.py` |
| [CBS_DATAPATH_BUG.md](CBS_DATAPATH_BUG.md) | Per-frame classifier sideband timing at the CBS boundary | Fixed; covered by the controller-rate bench |
| [MEDIA_CLOCK_LOCK_0810.md (historical)](MEDIA_CLOCK_LOCK_0810.md) | Media-clock lock observations and remaining CRF consumption boundary | Current design input; physical revalidation belongs to #117 |
| [PP_SHADOW_AREA_0812.md (historical)](PP_SHADOW_AREA_0812.md) | Protocol-processor integration area accounting | Current synthesis evidence |

New findings must describe the exact candidate, measurement boundary, raw
artifact identity, conclusion, and owning issue. Findings that cease to
describe the current bare-metal product leave the checkout and remain
recoverable from Git history.
