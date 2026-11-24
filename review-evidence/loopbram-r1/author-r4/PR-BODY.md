[A826] Status: REVIEW READY
Target: pf-loopbram-1 into dev-soft-core. Closes #979.
Validated head: dc78aedae34c25a97125ecd6816a1f645db5575f.

Adds optional input-mapped loopback from received audio to transmitted audio.
The 8x8 shape has 63 independent mono destinations plus an independent physical
destination in 64 keys. Port 0 has physical plus eight loopback destinations;
port 7 has seven. The 1x1 shape has eight physical plus eight loopback destinations.
The option defaults off.

Received samples are copied into synchronous block memory with one media frame
of added latency. Eight sample pages retain the claimed frame through its capture
walk. Missing or invalidated data produces silence. Unsupported leads refuse
elaboration; timestamp matching has a derived bound.

Disabled builds retain their original ports, widths, instance names and mapping
writer. Optional fields extend existing buses only when enabled; optional state
exists only in enabled branches. Both complete disabled release-top netlists have
identical canonical hashes against the base.

| Shape | LUT base / head | FF base / head | BRAM tiles base / head | DSP base / head | F7 / F8 delta |
|---|---:|---:|---:|---:|---:|
| 1x1/1if | 33792 / 33792 | 42649 / 42649 | 80 / 80 | 11 / 11 | 0 / 0 |
| 8x8/1if | 45199 / 45199 | 53086 / 53086 | 99 / 99 | 11 / 11 | 0 / 0 |

The parent integration checks production command handling and the real map store
at both sizes, including ADD, REMOVE, replacement, GET pages, clipping and changes
during copying. All 63 mapped destinations and eight output streams run together.
Four runtime connection and retention defects fail sample assertions. Both wire
sizes and all seven leaf plants pass. Processor instructions and mailbox transport
are outside this harness.

All requested regression and portability gates pass. The 114-entry builder union retains one documented calibration-report row marked NOT RUN.
Five defensive guards remain explicitly untested in isolation: bind-only flush,
one-shot claim, expiry, backlog and age.

Fresh enabled 1x1 route: minimum setup +0.124 ns and hold +0.036 ns across four corners, zero failing endpoints and routing errors. LUT 32792, FF 42637, BRAM tiles 83.
The enabled 8x8 route was not repeated in this round.

Disabled builder artifacts, descriptors, firmware ROM and initialization bytes
remain identical. Enabled control-memory allocation remains 47.0 tiles at 1x1 and
70.5 at 8x8. The latter remains S14 debt and the ordinary allocator refuses it.
Split builds use layout 3's NAME capacity instead of the absent all-fabric
backend's 128-record bound. Owner memory ledgers and service limits remain unchanged.
