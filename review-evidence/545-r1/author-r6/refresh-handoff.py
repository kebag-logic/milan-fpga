from pathlib import Path
import json
import shlex
p=Path(__file__).resolve().parent
rows=[json.loads(s) for s in (p/"gates.jsonl").read_text().splitlines()]
s=(p/"report-prefix.md").read_text()
s+="| Gate | Exact command | Exit | Seconds | Evidence |\n| --- | --- | ---: | ---: | --- |\n"
for r in rows:
    if r["name"].startswith("dp-"):
        continue
    command=shlex.join(r["command"]).replace("|", "\\|")
    s+=f"| {r['name']} | `{command}` | {r['rc']} | {r['seconds']:.3f} | `{r['name']}.log` |\n"
s+="\n### Datapath command exits\n\nExact commands appear by position in `dp-commands.json`.\n\n| Command | Exit | Seconds | Evidence |\n| --- | ---: | ---: | --- |\n"
for r in rows:
    if r["name"].startswith("dp-"):
        s+=f"| {r['name']} | {r['rc']} | {r['seconds']:.3f} | `{r['name']}.log` |\n"
s+="\n## Delivery\n\nPR-BODY.md retains the complete fetched public body, changes its first line to [A320], and adds the current merge-dev record. Final issue comment pending validation completion.\n"
(p/"HANDOFF.md").write_text(s)
