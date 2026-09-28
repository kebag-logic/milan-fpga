# Findings retained in the bare-metal product tree

This directory contains current hardware findings that still inform the
shipping Milan v1.2 design. Superseded target-runtime campaigns and operational
logs are preserved in Git history, not in the checked-out product tree (#259).

## Current entries

| Document | Scope | State |
|---|---|---|
| [451_TDM8_FIRST_LIGHT.md](451_TDM8_FIRST_LIGHT.md) | TDM8 first light between the AX7101 J11 header and the SoC board of the #451 amendment, image source `9e9954e9`: slot and channel order in both directions over 70 s each, continuity and the frame-rate offset (#451) | Both directions decoded in all eight slots, in order; DIN frame coherence NOT MET, tracked by [#617](https://github.com/kebag-logic/milan-fpga/issues/617); continuity check, scope and calibrated items NOT RUN |
| [117_GPTP_SILICON_EVIDENCE.md](117_GPTP_SILICON_EVIDENCE.md) | One AX7101 against the reference peer on dev `ede8d48e`: asCapable, cadence, turnaround, GM loss and return over six switch power cycles, publication and `tu` against the wire, controller enumeration (#117) | Current; GM loss and return inside the 5 s bound (worst 1.60 s) |
| [ADP shape (historical)](../history/v1/findings/ADP_SHAPE_STATIC_0727.md) | Generated ADP/AEM shape must match the instantiated stream geometry | Fixed; guarded by `scripts/check_entity_shape.py` |
| [CBS_DATAPATH_BUG.md](CBS_DATAPATH_BUG.md) | Per-frame classifier sideband timing at the CBS boundary | Fixed; covered by the controller-rate bench |
| [Media-clock lock (historical)](../history/v1/findings/MEDIA_CLOCK_LOCK_0810.md) | Media-clock lock observations and the then-open CRF consumption boundary (closed by #74) | Current design input; physical revalidation belongs to #117 |
| [Protocol area (historical)](../history/v1/findings/PP_SHADOW_AREA_0812.md) | Protocol-processor integration area accounting | Current synthesis evidence |
| [Throughput campaign (historical)](../history/v1/findings/PERFORMANCE_GOAL.md) | Closed >500 Mbit/s campaign measured on the retired 2-hart platform | Closed 2026-07-11; archived record only — the shipping fabric datapath supersedes it |

New findings must describe the exact candidate, measurement boundary, raw
artifact identity, conclusion, and owning issue. Findings that cease to
describe the current bare-metal product leave the checkout and remain
recoverable from Git history.
