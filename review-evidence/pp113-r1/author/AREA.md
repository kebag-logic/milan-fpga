[A280]

Default shape: 8 Stream Inputs / 8 Stream Outputs. Complete processor, all top-level ports present. Same repository recipe (`syn/ooc/protocol_processor_ooc.tcl`) for base a8f8ce810ddba1816cd129d0afcd71e6e02ade1b and candidate RTL. Reference part xc7a100tfgg484-2, clock 10 ns, synthesis release 2026.1. Both runs rc 0.

| Resource | Base | Candidate | Delta |
|---|---:|---:|---:|
| Slice LUTs | 28649 | 28643 | -6 (-0.021%) |
| Registers | 31095 | 31123 | +28 (+0.090%) |
| RAMB36 / RAMB18 / DSP | 23 / 2 / 4 | 23 / 2 / 4 | 0 |
| SRP listener LUTs | 1795 | 1868 | +73 |
| SRP listener registers | 2328 | 2336 | +8 |

The listener adds eight pulse bits and compares the existing per-sink latency latches. The complete result also contains remapping of unchanged logic; the total LUT decrease is not a logic-saving claim. OOC slack at 10 ns is negative in both builds: -10.089 ns base, -8.192 ns candidate. No routed timing or hardware qualification is claimed.

Reports: `area-base/` and `area-head/`. Command/return-code receipts: `ooc-base.json`, `ooc-head.json`; full logs alongside them. `provenance.json` records the exact HDL hashes used. Build/source directories are outside this evidence packet.
