"""Plant the two rounding probes of this review in a disposable copy of the
tree: probe A rounds the AAF lead down (166,666 ns), probe C rounds the CRF TC
down (41,666 ns). Then build and run capture_coherence's dp leg with --quick
in each copy (make dp-build; ./obj_dp/Vcoherence_dp --quick); each must fail
[GRID] alone.
usage: python3 rounding_probes.py <tree-copy-A> <tree-copy-C>"""
import pathlib, sys
def mut(p, a, b):
    s = pathlib.Path(p).read_text()
    assert s.count(a) == 1, (p, a)
    pathlib.Path(p).write_text(s.replace(a, b))
mut(sys.argv[1] + "/hdl/ieee1722/aaf/KL_aaf_packetizer.sv",
    "+ 64'(FS_HZ_P) - 64'd1) / 64'(FS_HZ_P);", ") / 64'(FS_HZ_P);")
mut(sys.argv[2] + "/hdl/ieee1722/crf/KL_crf_tx.sv",
    "localparam longint unsigned TC_NS_C  = (TC_PER_C * 64'(MCLK_NUM_C) + 64'(MCLK_DEN_C) - 64'd1)",
    "localparam longint unsigned TC_NS_C  = (TC_PER_C * 64'(MCLK_NUM_C))")
