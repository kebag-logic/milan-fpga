#!/usr/bin/env python3
"""Bind published execution receipts to local source and prior image hashes."""
import argparse
import ast
import base64
import hashlib
import json
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    root, packet = args.root.resolve(), args.packet.resolve()
    evidence = packet / "public-source"
    read = lambda name: json.loads((evidence / name).read_text())
    endpoint = "repos/kebag-logic/milan-fpga/contents/review-evidence/734-r1/MANIFEST.json?ref=ff22678d017ecc58e271c917a76cb3423f4a0498"
    envelope = json.loads(subprocess.check_output(["gh", "api", endpoint]))
    publication = json.loads(base64.b64decode(envelope["content"]))
    selected = []
    for record in json.loads((packet / "public-source-provenance.json").read_text()):
        name = Path(record["file"]).name
        row = next(row for row in publication if row["file"] == f"author-r5/{name}")
        assert hashlib.sha256((evidence / name).read_bytes()).hexdigest() == row["published_sha256"], name
        selected.append(row)
    (packet / "publication-manifest-selected.json").write_text(json.dumps({"revision": "ff22678d017ecc58e271c917a76cb3423f4a0498", "manifest_git_blob": envelope["sha"], "entries": selected}, indent=2) + "\n")
    source = read("r5-head.json")
    verified = []
    for path, row in source["changes_relative_to_dev"].items():
        data = (root / path).read_bytes()
        assert len(data) == row["bytes"] and hashlib.sha256(data).hexdigest() == row["sha256"], path
        verified.append(path)
    assert source["head"] == "7c862ad980dfe829ef4d85ff8f4fb4fab451984f"
    assert source["tested_tree"] == "622e79ae2a21917a49426c675d417307104112a1"
    execution = read("r5-workflow.json")
    log = (evidence / "r5-workflow.log").read_bytes()
    assert execution["rc"] == 0 and execution["head"] == source["head"] and execution["validated_tree"] == source["tested_tree"]
    assert len(log) == execution["bytes"] and hashlib.sha256(log).hexdigest() == execution["sha256"]
    parts = log.decode().split("selftest: PASS")
    assert len(parts) == 3
    counts = [sum(line.startswith("  ok   ") for line in part.splitlines()) for part in parts[:2]]
    assert counts == [570, 568], counts
    for part in parts[:2]:
        for token in ["exactly the six approved entries", "all five public pins", "drops tsn-c-stack is refused", "redirects tsn-c-stack is refused", "drops tsn-c-stack gitlink is refused", "adds tsn-c-stack gitlink is refused"]:
            assert token in part, token
    assert "flat isolated full selftest uses the explicit shipping worktree" in parts[0]
    scope_rows = read("r5-scope-classifications.json")
    assert scope_rows["before_head"] == source["starting_head"] and scope_rows["after_head"] == source["head"]
    assert len(scope_rows["rows"]) == 30
    for row in scope_rows["rows"]:
        assert row["before_hosted"] == row["after_hosted"] == row["before_replay"] == row["after_replay"], row
    prior = {row["shape"]: row for row in read("r4-image-hashes.json")}
    images = read("r5-image-hashes.json")
    assert len(images) == len(prior) == 5
    for row in images:
        old = prior[row["shape"]]
        assert row["identical"] and row["before_bytes"] == row["after_bytes"] == old["bytes_after"]
        assert row["before_sha256"] == row["after_sha256"] == old["sha256_after"]
    old_source = subprocess.check_output(["git", "-C", str(root), "show", "59354ffe:scripts/act_ci.py"], text=True)
    functions = lambda text: {n.name: ast.dump(n) for n in ast.parse(text).body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
    old_functions, current_functions = functions(old_source), functions((root / "scripts/act_ci.py").read_text())
    changed = sorted(name for name in old_functions if old_functions[name] != current_functions.get(name))
    added = sorted(set(current_functions) - set(old_functions))
    assert changed == ["selftest_lwsrp_manifest", "selftest_submodule_manifest"], changed
    assert added == ["selftest_stack_manifest"], added
    result = {"head": source["head"], "tree": source["tested_tree"], "publication_manifest_matches": len(selected), "published_source_hashes_match": verified, "published_scope_rows_unchanged": 30, "runner_log_hash_verified": True, "published_runner_assertion_counts": counts, "both_runner_forms_pass_stack_controls": True, "image_evidence": "Author-published execution and linked-image hash receipts; no reviewer rebuild", "five_prior_and_current_image_hashes_equal": True, "images": images, "runner_functions_changed_from_previous": changed, "runner_functions_added_from_previous": added, "all_other_runner_functions_and_classes_unchanged": True}
    (packet / "receipt-audit.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
