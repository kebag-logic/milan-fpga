import hashlib
import json
from pathlib import Path

root = Path(__file__).parent
commands = [json.loads(line) for line in (root / "commands.jsonl").read_text().splitlines()]
lines = ["# A180 commands and raw results", "",
         "All commands ran from the assigned donor lane. Raw output is retained without RTK filtering.",
         "The inner command in each entry is run by `rtk proxy python3 run.py <tag> ...`.",
         "`CONTEXT.md` describes pre-harness read-only discovery and apply_patch evidence edits.", "",
         "| Tag | UTC start | Seconds | Exit | Raw log |",
         "|---|---|---:|---:|---|"]
for record in commands:
    lines.append(f'| {record["tag"]} | {record["start"]} | {record["elapsed_seconds"]:.3f} | '
                 f'{record["exit_code"]} | [log](logs/{record["tag"]}.log) |')
for record in commands:
    lines.extend(["", "## " + record["tag"], "", "```sh", record["command"], "```"])
(root / "COMMANDS.md").write_text("\n".join(lines) + "\n")
files = []
for p in sorted(root.rglob("*")):
    if p.is_file() and p.name != "MANIFEST.sha256":
        files.append((hashlib.sha256(p.read_bytes()).hexdigest(), str(p.relative_to(root))))
(root / "MANIFEST.sha256").write_text("".join(f"{digest}  {rel}\n" for digest, rel in files))
for digest, rel in files:
    assert hashlib.sha256((root / rel).read_bytes()).hexdigest() == digest
print(f"Evidence sealed: {len(files)} files, {len(commands)} captured commands.")
print("Nonzero command exits:", [(c["tag"], c["exit_code"]) for c in commands if c["exit_code"]])
