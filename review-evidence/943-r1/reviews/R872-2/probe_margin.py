import pathlib,sys
from unittest.mock import patch
root=pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0,str(root/"tb/verilator/ctrl_service_budget"))
import edit_rows,rows_tiers,record_classes
for cost in (310,320,325,340):
 with patch.dict(edit_rows.EDIT_RECORD_US,{"1x1/1if":cost}):
  rows=rows_tiers.rows(root,"1x1/1if",rows_tiers.BUILT)
  findings=rows_tiers.findings(root,rows_tiers.BUILT,("1x1/1if",))
  print("paced statement",cost,"us; last queued notice",rows["last"][0],"ms; bound 140 ms")
  print("\n".join(findings) or "all held rows within bounds")
assert record_classes.rule(23330,100_000_000)==245
assert record_classes.rule(23333,100_000_000)==245
assert record_classes.rule(23334,100_000_000)==250
print("Held SET_STREAM_INFO: 23330 cycles => 245 us; 23333 => 245; 23334 => 250. Three cycles of headroom.")
print("All changes were in-memory table substitutions; no tracked source changed.")
