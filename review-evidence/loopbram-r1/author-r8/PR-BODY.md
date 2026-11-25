[A826] Status: REVIEW READY
Target: pf-loopbram-1 into dev-soft-core. Closes #979.
Validated head: 09201d35d7ea720b3ba205da185ba35c159ec24a, which contains dev-soft-core 5de21ff3.

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
identical canonical hashes against the base. No shipped RTL from this change has changed since that proof.
The figures are from that proof's base, before dev's merged changes.

| Shape | LUT base / head | FF base / head | BRAM tiles base / head | DSP base / head | F7 / F8 delta |
|---|---:|---:|---:|---:|---:|
| 1x1/1if | 33792 / 33792 | 42649 / 42649 | 80 / 80 | 11 / 11 | 0 / 0 |
| 8x8/1if | 45199 / 45199 | 53086 / 53086 | 99 / 99 | 11 / 11 | 0 / 0 |

The parent integration test checks production command handling and the real map store
at both sizes, including ADD, REMOVE, replacement, GET pages, clipping and changes
during copying. All 63 mapped destinations and eight output streams run together.
Each output stream's delivery is graded separately in both traffic phases. Each stream
must send its own packets, and its undelivered words are bounded by one packet.
The parent campaign has two controls and fifteen plants. Holding any one output off,
at each 8x8 talker and the 1x1 talker, fails that stream's named delivery and completeness checks.
Broken connections and reduced retention fail the sample checks, the connection plants
at both sizes. Processor instructions and mailbox transport are outside this harness.

The leaf harness drives the depacketizer with the queued and completed verdicts that
#948 introduced, and their accepting mask. Each flat monitor's accept is its PDU's one verdict, as dev's
own flat-monitor harnesses use it. Its results are unchanged: the same checks and packets per shape.

The parent harness compiles the firmware's AECP sources into the library its model links.
So the firmware boundary gate now lists it as a known builder that needs the RTL simulator, with its
build-only commands at both shapes. The boundary job for simulator builders judges its compiles; the
other boundary jobs leave it out and name it. That gate passes over the four simulator
builders' capture with its self-test. Removing the entry brings back, word for word, the
refusal the first hosted run reported. The leaf suite's files name no firmware path and
compile no firmware source, so it needs no entry.

Both new suites are registered with the shard planner as provisional, at the 300-second
timeout the sweep driver gives each, as for `reboot_ctrl`. At dev's twenty-six workers,
those figures leave four regular workers over the 1276-second budget, so the sweep now
deals twenty-seven workers. That is the step the new-suite decision provides when the
planner's self-test requires it. The largest regular worker stays at 1275 seconds, and
workers 14 and 15 own the new suites. Cold runs took 20.3 and 43.5 seconds under heavy
host load. Their hosted windows replace both figures after the first hosted run that
completes them; none has yet.

Disabled builder artifacts, descriptors and firmware images remain identical to dev's.
That covers both shipped configurations and all twelve composition images of the boundary gate.
Against the previously reviewed head, the only differences are dev's own: the FPGA-gPTP
microcode and the images that compile lwSRP. Enabled control-memory allocation remains 47.0 tiles at 1x1 and
70.5 at 8x8. The latter remains S14 debt (+11.0 over dev's 59.5-tile entry) and the ordinary allocator refuses it.
Split builds use layout 3's NAME capacity instead of the absent all-fabric
backend's 128-record bound. Owner memory ledgers and service limits remain unchanged.
The CPU budget harness builds an identical image and SoC to dev's at 8x8/1if.

## Enabled routes at the reviewed head 09201d35

Both enabled shapes are routed from 09201d35d7ea720b3ba205da185ba35c159ec24a (hdl tree 244c59e030d9078054fc88744f22e4e3e7d59246),
which contains dev-soft-core 5de21ff3. These are the reviewed head's routes. If dev-soft-core moves before
this PR merges, the merge candidate re-routes both shapes. The recipe is unchanged:
all three prescribed placement directives run from one post-optimization checkpoint per shape, and
the best worst-corner setup slack is selected. Setup must be at least +0.030 ns and hold at least 0 at every corner.

| Shape | Setup / hold, four corners | Failing endpoints / routing errors | LUT | FF | BRAM tiles | Slices | DSP |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1x1/1if, best of three | +0.147 / +0.036 ns | 0 / 0 | 32669 | 42821 | 82.5 | 14225 | 13 |
| 8x8/1if, best of three | +0.309 / +0.036 ns | 0 / 0 | 48485 | 54965 | 110.5 | 15792 | 13 |

The other two directives reach +0.125 and +0.020 ns at 1x1, and +0.117 and +0.049 ns at 8x8 (hold
+0.015 ns or more), so the margin is placement-sensitive. One 1x1 directive misses the floor.
Every route is fully routed. No worst path of the six is in the loopback logic. Earlier routes, at 9acb9b82
(8x8: +0.223/+0.036 ns, LUT 48901, FF 54672, 111 tiles) and at dc78aeda (1x1: +0.124/+0.036 ns,
LUT 32792, FF 42637, 83 tiles), remain valid for those sources only. The ordinary allocator
still refuses the enabled 8x8 image.

Review coverage before this head, corrected: R909-5 POSITIVE at 1516b2ffe321337858389ec8e42897f8a80644bb;
R910-3 POSITIVE at 9acb9b828b29aba71bd51303a4836f86c2278267.

## Validation at 09201d35, the merge's tree

| Gate | Result |
|---|---|
| `input_loopback` and `input_loopback_dp`, cold, as the sweep runs each suite | PASS in 20.3 s and 43.5 s; the tally reads both |
| `render_queue` and `chmap_capture` | PASS |
| Leaf campaign and bounds; parent campaign | PASS: control and 7 plants, 8 bounds; 2 controls and 15 plants |
| Firmware boundary gate, simulator builders, with its self-test | PASS, 202 controls |
| Boundary text cross-check with the new entry removed | Refuses on the parent harness, as hosted did |
| Docs workflow replay, 43 of 46 gate steps | PASS, 0 failures; tree clean after every step |
| Suite ownership for 27 shards, and physical selection | PASS |
| Planner self-test; workflow generator checks; test-evidence check | PASS |
| Builder driver, `test_input_loopback_contract` | PASS |
| Egress ledger self-test | PASS, 18 mutants |
| Image identity against dev: builder artifacts, descriptors, twelve firmware images, CPU budget harness build | IDENTICAL |

Not run at this head: the boundary gate's two capture legs and their joint judgement, the egress
ledger at 8x8/1if (it reads a harness run of hours), the docs builder legs, the compiler-absent
firmware command, the elaboration gates, the rtl-fast jobs, the twenty-seven suite shards and their
aggregate, and portability. Each exceeds this session's ten-minute command limit, and the local
replica needs the pushed head. Hosted acceptance at this head is required.
