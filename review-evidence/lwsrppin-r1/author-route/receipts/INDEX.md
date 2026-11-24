# Receipts: 8x8/1if split route, head dbba60e6 vs base aa30d77f (first directive, ExtraPostPlacementOpt)

Scratch (full reports, checkpoints): `/data-2/milan/tmp/lwsrppin-a834/route/{head,base}/route8/split/gateware/`.
Every file here is under 200 KB. The signoff timing reports are 1.27-1.30 MB each, so they are kept as stubs: the
size and sha256 of the full report, then its head through the Design Timing Summary and the clock summary.

| File | What it is |
|---|---|
| `head/summary.txt`, `base/summary.txt` | `tools/summ.py`: LUT/FF/BRAM tile/RAMB36/RAMB18/DSP from the placed and post-route utilization reports; WNS/TNS/WHS/THS for each signoff corner; checkpoint sha256s |
| `<side>/alinx_ax7101_utilization_place.rpt`, `<side>/baseline_utilization.rpt` | the placed (Physopt postPlace) and post-route (Physopt postRoute) utilization reports, as written |
| `<side>/alinx_ax7101_signoff_<corner>_timing.rpt.stub.txt` | the four signoff corners (Slow/Fast at 0 and 85 C), stubbed as above |
| `<side>/alinx_ax7101_signoff_check_timing.rpt`, `<side>/alinx_ax7101_route_status.rpt` | check_timing; route status (0 nets with routing errors at both sides) |
| `<side>/alinx_ax7101_iob_pack.rpt`, `<side>/critical-warnings.txt` | the #475 IOB pack check (every port PASS but the two documented INERT ones, `eth0_rx_er` with no net and 8x8's parked `tdm_dout`); the run's CRITICAL WARNING census: one `Place 30-722`, which is that `tdm_dout`. No ERROR line at either side |
| `<side>/fw-identity.txt` | `tools/fw_ident.py`: the manifest's ctrl_firmware record, the sha256 of the linked ELF and of the copy the recipe's `--ctrl-firmware` names, the ROM bank inits, the export Verilog, the repo and lwSRP HEADs, and the `mrp_mad.o` `.text` bytes in the link map |
| `<side>/driver.log`, `<side>/image.log`, `<side>/boot.tail.txt` | `tools/side.sh`'s log (signoff included); `route_image8.sh`'s log (builder, image link, export, identity gate, `pp_baseline.py`); the split boot's last 40 lines (`ctrl_split_boot: PASS`) |
| `hier-delta.txt` | the post-route hierarchy (`baseline_hierarchy.rpt`), base to head: the top, plus every instance at depth 3 or less that moves by 10 or more LUTs or FFs |
| `tools/` | the scripts as run. `route_image8.sh` is the composed train's (`train1117-a794/round5/receipts/fit/tools/route_image8.sh`), changed only to take W and B as arguments and with the redacted paths filled in. `signoff.py` is the train's, unchanged. `side.sh` is the train's `fitpoint.sh` 8x8 arm, cut to its first directive, with the train's `boot8.sh` and `route_one8.sh` inlined. `paths3.py` and `prep_directives3.py` are the train's, copied for a best-of-3 run and not used |
