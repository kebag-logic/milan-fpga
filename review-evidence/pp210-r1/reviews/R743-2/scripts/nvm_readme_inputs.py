"""Print every README-derived input of tb/nvm_port/measure_figures.py for one
extracted tree, without building or running the suite.
usage: python3 -I nvm_readme_inputs.py <extracted tb/nvm_port dir>"""
import importlib.util, json, re, sys
from pathlib import Path
d = Path(sys.argv[1]).resolve(); sys.path.insert(0, str(d))
spec = importlib.util.spec_from_file_location("mf", d / "measure_figures.py")
mf = importlib.util.module_from_spec(spec); spec.loader.exec_module(mf)
flat = mf.flat_readme()
out = {
  "claim_matches": {n: [len(re.findall(c, flat)) for c in cs] for n, cs, _ in mf._all_claims()},
  "claim_spans_text": {n: [[flat[m.start():m.end()] for m in re.finditer(c, flat)] for c in cs] for n, cs, _ in mf._all_claims()},
  "figures": [flat[m.start():m.end()] for m in mf.FIGURE_RE.finditer(flat)],
  "arm_rows": mf.readme_arm_rows(),
  "readme_matrix": mf.readme_matrix(),
  "size_claims_vs_393": mf.readme_figures(393, flat),
  "claim_coverage_problems": mf.claim_coverage(flat),
}
print(json.dumps(out, indent=1, sort_keys=True, default=str))
