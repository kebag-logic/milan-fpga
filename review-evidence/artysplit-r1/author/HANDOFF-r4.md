Status: IMAGE READY. Qualified 80 MHz Arty split image and matched deployment inputs are preserved.
ETA: complete for the author image handoff. The manager's bench and independent reviews remain pending.

[A829] #878 round 4, updated 2026-11-24T19:26:44.153970+00:00.
Checkout: $LANES/arty-split; branch pf-arty-split-1 -> dev-soft-core.
Local head: 248d85c1453213b0f1642967a4046f395c82c56b; base 854bd7236792ce1adbd10c43b13a6a5002ad3bb6. Worktree clean. No push.

The entity retains one interface, one AAF talker, one AAF listener and one CRF input: FPGA shape (1,1,2). Sys/CPU is exactly 80,000,000 Hz, VCO 800 MHz, datapath 50 MHz and margin=0. MII advertises only 100BASE-TX full duplex. No Linux row was added.

All 145 fresh service cases across eight variants, thirteen final command checks and six qualification checks pass. Load 0.49667711403508774 <=0.70; txL 48.74 <=49 ms; maximum whole pass 1.6813375 <=2 ms; last notice 121.84 <=140 ms; ACMP 28.82 <=30 ms. Slice 950 us, pace 9 ms, queued bound 125 ms and ordinary transmit statement 30 ms follow the existing rules. The seven held-egress rows remain the only recorded misses, each within its own unchanged 80 MHz ledger. No owner bound failed.

Selected directive: ExtraTimingOpt. Best worst-corner WNS 0.617 ns and WHS 0.017 ns, with zero failing setup/hold endpoints in all four signoff reports. All three directives completed; REPORT.md records each result. The slot wrapper admitted at most two builds and checked at least 20 GB available memory. Slow/Fast are fixed speed models; 0/85 C are endpoint power metadata.

Selected attempt's post-placement utilization: 33411 LUTs, 40479 FFs, 78.5 BRAM tiles and 14119 occupied slices. A new Arty firmware ledger records ELF 159532 bytes; text/rodata/data/bss/stack 112748/11558/100/45072/8192 bytes; ROM live extent 124412, SRAM live extent 53392; allocation 44/56 RAMB36 equivalents.

Deployment pair inputs, preserved with their original manifest/layout bytes:

- Bitstream: $MANAGEMENT/2026-09-23/artysplit-a829/round4/image/gateware/digilent_arty.bit
  3281691 bytes; SHA256 1046292da1e73b2b595f65c66d9c429fb183a43e3466e160d95024651014735c
- Layout: $MANAGEMENT/2026-09-23/artysplit-a829/round4/image/flashboot_layout.json
  1002 bytes; SHA256 a096b7612353ce756440111ce4b89b0b241dd25ae3481e4d5ff0d16360f4b84f
- Matched manifest: $MANAGEMENT/2026-09-23/artysplit-a829/round4/image/image_manifest.json
  608 bytes; SHA256 81ade1bd936f258d58921666e4b1c5508ca29392e35ed1ea46c20b6337de47f2

The image directory also contains matched AEM files, the exact ELF, CSR maps and generated gateware. Original and copied input sets pass image identity and offline deploy input checks. No flash, JTAG, console or bench operation ran.

All four firmware shards, the complete service grader, boot/region simulations and fault controls, MII host tests and plants, affected timestamp suites, builder checks, lint/front-end checks and eleven final documentation gates pass for their executed scope. Historical area calibration is SKIP for its absent external reference. The original four scheduler blocks and old cost rows remain byte-identical. AX identity passes 42 generated/product plus thirteen controlled SoC-export comparisons, including both full ELFs; AX bitstreams were not rebuilt.

Evidence: REPORT.md, PR-BODY.md, receipts/INDEX.md and image/provenance.json in this directory. All indexed compressed receipts pass privacy.scrub_redact on their compressed and expanded bytes. The receipt index and privacy-check.json contain the complete count and hashes. Full service qualification SHA256: f6f1d2f535a8de0ec2348dbb0998a152103f3583e9bf4cc72b0115552ef1886c.

The active scratch is $VALIDATION_STORAGE/artysplit-a829/r4/build-corrected. Source and full campaign provenance are in qualified-source.json and final-census/qualification.json. The final campaign used four shared harness slots. An early exploratory fifth leg was terminated, excluded and rerun within the limit; concurrency-correction.json records the deviation. Scratch stayed below 30 GB; only closed generated precompiled headers were reclaimed with hash inventories.

The manager runs the bench after this handoff. Independent internal/external reviews, hosted checks, candidate-merge validation, merge and Issue completion remain pending. This is author evidence, not a review verdict.
Issue REPORT: https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7142099975

IMAGE READY 248d85c1453213b0f1642967a4046f395c82c56b 1046292da1e73b2b595f65c66d9c429fb183a43e3466e160d95024651014735c
