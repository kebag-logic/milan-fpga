Candidate: `ba2a66f72db495bd7c48700d46688de08a6c2c61`. Desk evidence only. Arty physical implementation passes all four requested corner reports and independent internal review. Both ALINX image-identity comparisons pass and are independently accepted.

| Check | Result |
|---|---|
| Default audio suite | PASS: selection, record/status/reference, media, packetization, bus, both storage widths, short duplex and seven representative defects |
| Packing grader controls | PASS: 55 endpoints and twelve named absent/misplaced/unregistered endpoint controls; all 55 endpoints also pass on the selected final route |
| Long duplex, K=13 | PASS on current source: 1000000 playback frames and 999993 capture frames checked; 37419648 checks and zero failures; eight channels, all 32 bits, no gap or duplicate after startup |
| Feedback | PASS: 0x00060000 after qualification; extra-event and clock-loss cases covered separately |
| Protocol records | PASS: 120000 records, all payload bits; reset at each record-word boundary |
| Status | PASS: fixed 20-byte format, 65539 records across sequence wrap |
| Capture mapper and AAF serialization | PASS: 6000 frames per width, 24 and 32 bits |
| Existing default-width input loopback | PASS: 79587 checks at eight streams and 76017 at one stream |
| Existing split datapath integration | PASS: 148 checks, no failures |
| Language and documentation gates | PASS: Python, C++, RTL, shell, documentation style/privacy and punctuation |
| Existing render queue suite | PASS: 39 checks at each width |
| Protocol defect controls | PASS: 24/24 named failures; relevant RTL unchanged since the recorded campaign |
| Transport defect controls | PASS: 42/42 named failures, including all three source-launch hazard bypasses; five baselines pass |
| Audio/network selection | PASS: both options selectable separately; combined selection refused; audio refused on ALINX |

The long run uses independently advancing bus, media-processing and media-oscillator clocks. Channel-distinct data exercises every subslot bit. Startup prefill accounts for the difference between directions' checked frame counts. Once comparison starts, every frame must be the exact next expected frame.

Capture tests include every position of an epoch change within a render frame, acknowledgement backpressure, trailing old-frame beats, partial-frame rejection and restart at channel zero. Bus tests include a blocked status socket while audio continues, read turnaround, final-word commit and asynchronous reset during an active write. Reference tests include count and sequence wrap, discontinuity, duplicates, malformed fields, watchdog, delivery timing, timestamp units and independent physical qualification.

Run the repository audio suite's default make target with an external build directory, two jobs and the cleanup ledger. Its named `duplex` target uses K=13 and defaults to 100000 frames; the extended run passed 1000000 as its frame-count argument. Run each defect driver with all plants selected, two jobs and completed-build disposal only after ledger recording. Detailed plant names and required assertions are in [r2-planted-defects.json](r2-planted-defects.json).

No physical interval-latency qualification, hardware stream operation, host binding, electrical compliance or sustained hardware duplex is claimed. No external review has been obtained.

The corrected default suite passes at the stated candidate. Its first formatting attempt failed compilation and remains failed evidence; it was repaired and independently reviewed. The final committed harness also passed the full-window million-frame run: 1000000 playback and 999993 capture frames, qualified feedback 0x00060000, zero gaps or duplicates after startup, and feedback cleared on clock loss.

The final run counts one reference discontinuity: the driver deliberately marks its initial reference as discontinuous before qualification. This is distinct from audio gaps; the audio gap/drop checks remain zero.

The shared model owner and counted assertion reporter are exercised on this head. A zero-frame workload exits with one counted CAPTURE_LONG_RUN_COUNT failure; this is a reporter control, separate from the 66 planted implementation defects.

The actual first placement accepted 48 data endpoints and rejected an address register in fabric. The source fix gives the scheduler separate preserved socket state; the selected final placement and route pass. The initial revised address plant failed an ownership assertion before its declared address assertion, so it was not counted. The final plant corrupts capture writes only, passes its baseline and reaches the declared address assertion without changing runtime checks.

At the current head, all three source-launch hazard bypasses are caught. Each baseline tests 50 transient hazards across receiving edges, stable transitions and reset on the actual bridge crossing. The prior route audit exposed suppressed flag-pair hold analysis and combinational source launches; their corrections pass source review and the actual selected route reports.

The full-window million-frame repeat passes at the current head: 37419648 checks, zero failures; the intentional initial reference discontinuity is the sole reference-loss count.

Final physical evidence: minimum setup +0.005 ns, hold +0.040 ns and pulse-width slack +1.389 ns, zero failing endpoints at every reported corner. All 13 skew bounds pass; timestamp skew is 1.196 ns against 20 ns. Flag-pair hold/setup are +0.122/+1.215 ns. Every routable net is routed, with zero routing errors. The design-rule warning table matches the baseline. See the route and cost receipts for exact artifact hashes and complete counts.

Current punctuation gate: zero findings across 148 added lines in two changed documentation pages; all 339 controls pass. Current source-analysis gate: zero findings in its declared scope. These scoped checks are not a claim that protected or full merge gates have run.
