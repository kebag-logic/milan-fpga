#!/usr/bin/env python3
"""Check published round-2 case outcomes and source identities without rerunning banks."""
import json, pathlib, subprocess
OUT = pathlib.Path(__file__).resolve().parent
P = OUT / "public-evidence/author-r2/evidence/round2"
HEAD = "2e83841675e4e1439c413c9ca11b4a123898a60e"
TREE = "4b1bed5825eae73757cb5368c71468c7d1d67d72"
def read(path):
    return json.loads(path.read_text())
rows = []
for name, passed in (("head-relative",True),("head-absolute",True),("missing-dep",False),
                     ("missing-dep-unpatched",False),("unpatched",False),("shared-4",False),
                     ("dev-race-3",False)):
    r = read(P / "fixtures" / (name + ".json"))
    rc = int((P / "fixtures" / (name + ".rc")).read_text())
    assert r["isolated"] is passed and rc == (0 if passed else 1)
    if name in ("head-relative", "head-absolute", "shared-4"):
        assert r["rev"] == HEAD
    if "missing-dep" in name or name == "unpatched":
        assert (P / "fixtures" / (name + "-mutation.base")).read_text().strip() == HEAD
    if "missing-dep" in name:
        assert all(v.startswith("NOT RUN:") for leg in r["patch_checks"].values() for v in leg.values())
    if name == "unpatched":
        assert all(v == "no receipt" for leg in r["patch_checks"].values() for v in leg.values())
    if passed:
        assert all(v == "ran and passed" for leg in r["patch_checks"].values() for v in leg.values())
        assert r["changed_paths"] == 0
    if name in ("shared-4", "dev-race-3"):
        assert r["changed_paths"] > 0
        assert any("Place the VexiiRiscv" in step["step"] and step["rc"] != 0 for leg in r["legs"].values() for step in leg)
    rows.append({"case": name, "rev": r["rev"], "rc": rc, "isolated": r["isolated"], "changed_paths": r["changed_paths"]})
gates = read(P / "gate-legs/gate-legs.json")
assert gates["rev"] == HEAD and gates["gate_legs"] and gates["isolated"]
assert gates["changed_paths"] == 0 and gates["planted_manifest_sha256"] == gates["final_manifest_sha256"]
assert all(step["rc"] == 0 for leg in gates["legs"].values() for step in leg)
for i in (0,1):
    leg = read(P / f"gate-legs/builder-leg-{i}.json")
    assert leg["head"] == HEAD and leg["tree"] == TREE and leg["leg"] == i
    patch = read(P / f"gate-legs/gate-23h-leg-{i}.json")
    assert len(patch["gates"]) == 2
    assert all(row["verdict"] == "pass" and not row["not_run"] for row in patch["gates"])
docs = read(P / "docs-gates-2e838416.json")
assert len(docs) == 46 and all(r["rc"] == 0 for r in docs)
result = {"fixtures": rows, "gate_legs_exact_head_and_tree": True,
          "cache_paths": gates["planted_paths"], "cache_manifest_sha256": gates["final_manifest_sha256"],
          "gate_leg_seconds": gates["gate_leg_seconds"], "docs_rows_rc_zero": len(docs),
          "basis": "Published author execution receipts; no manager source execution inferred"}
(OUT / "evidence-audit.json").write_text(json.dumps(result, indent=2) + "\n")
print("PASS: seven fixture outcomes, exact-head leg receipts, both patch checks, equal post-leg cache manifests, 46 documentation gate rows")
