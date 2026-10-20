"""Count published campaign outcomes independently of the PR's prose."""
import json
import re
from pathlib import Path

PACKET = Path(__file__).resolve().parents[1]
ROOT = PACKET / "receipts/public/author-r2/receipts/round2"
result = {}
for side in ("base", "head"):
    lines = (ROOT / f"campaigns/{side}/srp_top.log").read_text().splitlines()
    result[side] = {
        "golden_passes": sum(line.startswith("control ") and line.endswith(" PASS")
                             for line in lines),
        "killed_mutation_entries": sum(" KILLED tags=" in line for line in lines),
        "coverage": [line for line in lines if line.startswith("assertion coverage:")],
        "campaign_tally": [line for line in lines if re.match(r"^\d+ checks:", line)],
    }
assert result["base"]["golden_passes"] == result["head"]["golden_passes"] == 17
assert result["base"]["killed_mutation_entries"] == 150
assert result["head"]["killed_mutation_entries"] == 161
text = json.dumps(result, indent=2) + "\n"
(PACKET / "receipts/campaign-accounting.json").write_text(text)
print(text, end="")
