[A826] Status: REVIEW READY
Target: pf-loopbram-1 into dev-soft-core. Closes #979.
Validated head: 9acb9b828b29aba71bd51303a4836f86c2278267.

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
identical canonical hashes against the base. No RTL changed after that proof.

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

Both new suites are registered with the shard planner from measured cold runs, scaled
by the documented hosted factor; their hosted windows are owed by the first hosted run.
The planner self-test and all nineteen shard listings pass. Every worker is predicted
within its bound, the largest at 1615 of 1620 seconds. The two shards that own the new
suites pass through the sweep driver. The complete serial sweep was not run.
The docs workflow's gates pass when replayed locally, including the idiom, test-evidence,
contents, inventory and traceability gates, and the sweep's tally now reads the leaf suite.
All of these failed earlier on this PR's own files.

The leaf, queue, capture, datapath, render, coherence, portability, builder union and
plant campaigns pass at this head; the builder union keeps one documented calibration
row marked NOT RUN. Five defensive guards remain explicitly untested in isolation:
bind-only flush, one-shot claim, expiry, backlog and age.

Enabled 8x8, routed at this head's source: minimum setup +0.223 ns and hold +0.036 ns across
four corners, zero failing endpoints and routing errors. LUT 48901, FF 54672, BRAM tiles 111, DSP 11.
That is the best of the three prescribed placement recipes. The other two reached +0.008 and
+0.003 ns, below the floor, so the margin is placement-sensitive. Every recipe's worst path is
in the mailbox, not in the loopback logic. Enabled 1x1 RTL is unchanged since its route at
minimum setup +0.124 ns and hold +0.036 ns, with zero failing endpoints and routing errors.

Disabled builder artifacts, descriptors, firmware ROM and initialization bytes
remain identical. Enabled control-memory allocation remains 47.0 tiles at 1x1 and
70.5 at 8x8. The latter remains S14 debt and the ordinary allocator refuses it.
Split builds use layout 3's NAME capacity instead of the absent all-fabric
backend's 128-record bound. Owner memory ledgers and service limits remain unchanged.
