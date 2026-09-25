import json, subprocess, hashlib
from pathlib import Path
out = Path(__file__).resolve().parent
probe = out / "probes"
head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
sha = hashlib.sha256(Path("sw/builder/test_builder.py").read_bytes()).hexdigest()

def read(tag):
    data = json.loads((probe / (tag + ".json")).read_text())
    if tag.startswith("r316"):
        run = json.loads((probe / (tag + "-run.json")).read_text())
        assert run["head"] == head and run["builder_sha256"] == sha
        rows = data["results"]
    else:
        assert data["summary"]["head"] == head, tag
        rows = data["rows"]
    assert (probe / (tag + ".rc")).read_text().strip() == "0"
    return rows

def cell(row):
    if row["verdict"] == "ACCEPTED":
        return "ACCEPTED"
    reason = row.get("reason", "")
    for token, label in (("boot-unit asm allowlist rule", "ASM"),
                         ("identity-sample absence rule", "SAMPLE"),
                         ("identity-sample macro replacement rule", "MACRO")):
        if token in reason:
            return "REFUSED:" + label
    return "REFUSED:OTHER"

def table(name, tags):
    sets = [read(tag) for tag in tags]
    assert all([r.get("id", r["label"]) for r in rows] ==
               [r.get("id", r["label"]) for r in sets[0]] for rows in sets)
    lines = ["# " + name, "", "Head: `" + head + "`.", "",
             "ASM: unit allowlist; SAMPLE: prior absence rule; MACRO: replacement rule.",
             "OTHER: full refusal retained in the corresponding JSON receipt.", "",
             "| Case | " + " | ".join(tags) + " |",
             "|---|" + "---|" * len(tags)]
    for index, row in enumerate(sets[0]):
        label = (row.get("id", "") + " " + row["label"]).strip().replace("|", "\\|")
        lines.append("| " + label + " | " + " | ".join(cell(rows[index]) for rows in sets) + " |")
    (out / (name + ".md")).write_text("\n".join(lines) + "\n")
    return sum(map(len, sets))

r316 = ["r316-sdk", "r316-sdk-assert_preprocessed_identity_sample",
        "r316-sdk-assert_preprocessed_asm_allowlist", "r316-absent",
        "r316-absent-assert_identity_macro_free"]
count = table("R316-ROUND3-MATRIX", r316)
for part in ("r2", "r2b", "r2c", "r2d", "r2e"):
    tags = ["r317-cases_544_" + part + "-" + mode for mode in
            ("sdk", "sdk-disconnected", "absent", "absent-disconnected")]
    count += table("R317-" + part.upper() + "-ROUND3-MATRIX", tags)
normal = {r["id"]: r for r in read(r316[0])}
without = {r["id"]: r for r in read(r316[2])}
absent = {r["id"]: r for r in read(r316[3])}
for name in ("W01", "W02", "W03"):
    assert cell(normal[name]) == "REFUSED:ASM"
    assert without[name]["verdict"] == absent[name]["verdict"] == "ACCEPTED"
for index in range(1, 11):
    name = "A%02d" % index
    assert cell(normal[name]) == "REFUSED:SAMPLE"
    assert absent[name]["verdict"] == "ACCEPTED"
assert count == 483, count
(out / "probe-summary.json").write_text(json.dumps({"head": head, "builder_sha256": sha,
    "configurations": 25, "verdicts": count, "W01_W03_named_refusal_and_control": True,
    "A01_A10_compiler_free_bound": True}, indent=2) + "\n")
print(count, "verdicts at", head)
