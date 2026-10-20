"""Rerun chosen dynmap_mutants.py rows and reviewer probes against a clone.
Usage: python3 -I probe_mutants.py <clone> <jobs> <row>...   (row: 1-based MUTATIONS index, or L)
L = reviewer probe: the record's length bytes are never compared (both AS_RRD length arms),
so a framed record with a wrong length field is taken as framed; expected to SURVIVE when no
committed check plants a wrong-length record."""
import importlib.util, sys
from pathlib import Path
clone = Path(sys.argv[1]).resolve()
suite = clone / "tb/verilator/milan_dp"
sys.path.insert(0, str(suite))
spec = importlib.util.spec_from_file_location("dynmap_mutants", suite / "dynmap_mutants.py")
dm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dm)
L4 = "              11'd4: amr_hframe_r <= amr_hframe_r && (mrec_rdata_w == amr_plen_w[15:8]);\n"
L5 = "              11'd5: amr_hframe_r <= amr_hframe_r && (mrec_rdata_w == amr_plen_w[7:0]);\n"
PROBE_L = ("dynmap", "reviewer probe: the record's length field is never compared",
           [(L4, "              11'd4: amr_hframe_r <= amr_hframe_r;\n"),
            (L5, "              11'd5: amr_hframe_r <= amr_hframe_r;\n")], None)
picks = []
for a in sys.argv[3:]:
    picks.append(PROBE_L if a == "L" else dm.MUTATIONS[int(a) - 1])
dm.MUTATIONS[:] = picks
sys.argv = ["dynmap_mutants.py", "--jobs", sys.argv[2]]
sys.exit(dm.main())
