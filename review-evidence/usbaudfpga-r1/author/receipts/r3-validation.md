Candidate: `75db86a926a9f4d2f7734246eac06a8f58c57bac`. Desk evidence only. Fresh physical implementation and every reported corner pass.

The exact contract comparison changes the own-clock reference watchdog to three milliseconds. The implementation also preserves the last pre-expiry feedback cycle. Reference continuity remains based on USB count/sequence, and the independent source-timestamp delivery bounds remain unchanged.

| Check | Result |
| --- | --- |
| Full-window duplex | PASS: 1,000,000 playback frames, 999,993 capture frames after startup, 37,419,648 checks, zero failures |
| Sample identity | PASS: eight channels, all 32 bits, no gaps or duplicates after comparison begins |
| Feedback | PASS: qualified 0x00060000; clock loss clears it |
| Watchdog bounds | PASS: 2.9 ms accepted, 3 ms coincident reference refused, previous cycle retained, expiry without references, full requalification |
| Protocol defects | PASS: all 24 named runtime failures |
| Transport defects | PASS: all 46 named runtime failures and five baselines |
| Default audio regression | PASS: selection, protocol, reference, media, packet, bus, source levels, both storage widths, short duplex and seven representative defects |
| Pad-grader controls | PASS: all twelve controls in the default regression |
| Source lint | PASS: 89 existing findings within the ratchet, 20 waivers, no added exception |
| Source idiom and documentation | PASS: RTL, scripting, documentation privacy and style |
| Punctuation | PASS: zero findings on nine added lines; 339 controls |
| ALINX identity | PASS: both full retained programming payloads re-read byte for byte; round-3 changes excluded from both input closures |
| Network ownership | PASS: all 22 pinned attachment files byte-identical |

Five separate watchdog defects restore the old two-ms bound, delay expiry one cycle, disable expiry, suppress feedback one cycle early, or require an arriving record to expire. Each is caught by its named runtime assertion. Replacement tests isolate the own-clock watchdog from the separate source-clock delivery guard. The no-reference test stops advancing the media timestamp and still requires own-clock expiry.

The sole reference-loss count in the long run is its intentional initial discontinuity. Startup prefill accounts for the seven-frame capture-count difference. Neither indicates a detected audio gap.

Preliminary failed attempts remain recorded and do not count as successful evidence. The corrected boundary run, successful punctuation rerun and complete campaigns are separately retained. No acceptance criterion or test expectation was weakened.

The fresh physical implementation passes Slow/Fast at both 0°C and 85°C report settings: setup +0.002 ns, hold +0.018 ns, pulse +1.389 ns, zero failing endpoints. All 55 pad endpoints, all 13 skew groups and finite flag-pair hold/setup pass. All 83,063 routable nets are routed without errors, and the reported design-rule warning table matches the baseline. The complete programming payload equals the flash output byte for byte. The routed resource increment is +2,592 LUTs, +5,861 registers, +454 slices and +8 block-RAM tiles. Setup is 0.003 ns narrower than round 2 and remains specific to this artifact. See the exact recipe, report hashes and image identity in the route receipt. External review, protected checks and merge validation are separate. No bench acceptance, host binding, interval-delivery qualification, physical bus timing or sustained hardware duplex is claimed.

Execution compliance exception: the initial documentation self-check automatically removed randomized temporary directories without advance ledger entries. Their names were not retained. The audited repeat passes; it cannot repair the original rule violation. See [the exception](r3-cleanup-exception.md).
