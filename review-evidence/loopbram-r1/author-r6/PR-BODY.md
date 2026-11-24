[A826] Status: REVIEW READY
Target: pf-loopbram-1 into dev-soft-core. Closes #979.
Validated head: c413d33abe016f5c1e44bdaa1e0354cfe4ab6d99.

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

Both new suites are registered with the shard planner as provisional, at the 300-second
timeout the sweep driver now gives each, as for `reboot_ctrl`. The driver's 1800-second default
cannot be a provisional figure: no regular worker holds it within its 1620-second bound. Cold
runs took 34.2 and 98.0 seconds under heavy host load. Their hosted windows replace both figures
after the first hosted run. The planner self-test and all nineteen shard listings pass, with no
added worker; the largest worker stays at 1615 of 1620 seconds. Shards 12 and 13 now own the new
suites. The complete serial sweep was not run.
The docs workflow's gates pass when replayed locally, including the idiom, test-evidence,
contents, inventory and traceability gates, and the sweep's tally now reads the leaf suite.
All of these failed earlier on this PR's own files.

The leaf, queue, capture, datapath, render, coherence, portability, builder union and
plant campaigns pass at 9acb9b82, the previous head; the builder union keeps one documented calibration
row marked NOT RUN. Five defensive guards remain explicitly untested in isolation:
bind-only flush, one-shot claim, expiry, backlog and age.

Enabled 8x8, routed at 9acb9b82's source (no RTL has changed since): minimum setup +0.223 ns and hold +0.036 ns across
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

The first hosted run, at 9acb9b82, failed in the docs and elaboration gate aggregates. Those two
jobs check out without submodules and read the builder's gate list. The builder driver imported
the new loopback test before answering `--list`, and that test imported a descriptor generator
which exits 2 without the protocol-processor submodule. The generator imports now sit inside
the test functions, as other builder tests already do. Against that run's own receipts, both
aggregates fail exactly as hosted without the submodule and pass with it. At this head the gate
list is produced without the submodule and is byte-identical. The suite-shard failure in that run
was fail-fast cancellation.

## Validation at c413d33a, merged into dev-soft-core 2509db68

| Gate | Result |
|---|---|
| Docs workflow replay, 43 of 46 gate steps at the merge | PASS, 0 failures; tree clean after every step |
| Gate aggregates' builder inventory without submodules | PASS: 114 gates, byte-identical to the hosted inventory |
| First hosted run's receipts, both aggregates, submodule present | PASS: 45 and 5 source gates exactly once |
| Suite ownership step for 19 shards, and physical selection | PASS |
| Planner self-test; 19 shard listings | PASS; 19 of 19 exit 0 |
| `input_loopback` and `input_loopback_dp` cold, within their 300 s timeouts | PASS in 34.2 s and 98.0 s |
| Builder driver, `test_input_loopback_contract` | PASS |
| Test-evidence check and self-test | PASS, 105 of 105 |

Not run at this head: the docs builder legs, the compiler-absent firmware command, the
elaboration gates, the six rtl-fast jobs cancelled in the first hosted run, the nineteen suite
shards and their aggregate, and portability. Each exceeds this session's ten-minute command
limit, and the local act runner needs the pushed head. Hosted acceptance at this head is required.
