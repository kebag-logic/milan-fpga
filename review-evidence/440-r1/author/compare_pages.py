"""Assert engine stability on both populations and enumerate document edits."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
data = {name: json.loads((root / (name+".json")).read_text()) for name in (
    "pages-base-base", "pages-head-base", "pages-base-head", "pages-head-head")}
assert data["pages-base-base"] == data["pages-head-base"]
assert data["pages-base-head"] == data["pages-head-head"]
old, new = data["pages-base-base"], data["pages-head-head"]
changed = [path for path in old if old[path]["content_sha256"] != new[path]["content_sha256"]]
assert changed == ["docs/DOC_GENERATION.md"], changed
for path in old:
    for field in ("headings", "generated", "owns", "refusals"):
        assert old[path][field] == new[path][field], (path, field)
report = dict(pages=len(old), provenance=sum(x["generated"] is not None for x in old.values()),
              base_population_engine_differences=[], head_population_engine_differences=[],
              changed_document_contents=changed, changed_headings=[], changed_generated_contents=[],
              directly_affected_parser_corrections=[],
              hashes={name: hashlib.sha256((root/(name+".json")).read_bytes()).hexdigest() for name in data})
(root / "perpage-summary.json").write_text(json.dumps(report, indent=2)+"\n")
print(json.dumps(report, indent=2))
