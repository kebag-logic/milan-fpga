# How the reviewer receipts were produced (portable)

All runs use the pinned Verilator 5.050 first on PATH and a TMPDIR inside the packet's
scratch. `<clone>` is a detached clone of the processor at a2fce4326ebdaf398a1920d79a664d44e6f1e5dd.

1. SRP campaign, every arm whose named check is a PS or LK row (46 labels, 48 entries):
   `python3 -I tb/srp_top/mutants.py --output <scratch>/campaign212 --only <46 labels> --jobs 8`
   run from `<clone>` (the driver copies the tree per unit). Log: `receipts/srp-campaign-issue212-arms.log`.
   Comparison: `python3 -I probes/compare_campaign.py receipts/srp-campaign-issue212-arms.log <author camp-srp.log>`.
2. Reviewer probes: `probes/make_probe_tree.sh <clone> <scratch>/probe`, then
   `make -C <scratch>/probe/tb/srp_stream_fsms RUN_ARGS=suite`. Inserted block:
   `probes/r769_2_probe_block.cpp`; resulting diff: `receipts/probe-srp_stream_fsms.diff`.
3. Round-1 re-bind probe: copy `hdl/`, `tb/common`, `tb/srp_stream_fsms` of `<clone>`,
   `python3 -I probes/r769_1_probe_rebind_same_full_table.py <copy>`, then the suite as in 2.
4. Area at 2x2: `bash probes/area_some.sh <copy of hdl> receipts/area-head-a2fce43 srp_top_2x2`
   (sv2v, yosys 0.66 `synth_xilinx -family xc7 -flatten`; the author's published script).
5. Lint: `bash scripts/lint_hdl.sh` in a copy of `hdl/` and `scripts/`.
6. Evidence integrity: `python3 -I probes/verify_evidence_manifest.py <pp212-r1> author-r2/ reviews/R769-1/`.
