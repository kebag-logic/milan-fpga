#!/usr/bin/env python3
"""Check the signed local-CI manifest against the candidate's workflow files.

usage: check_manifest.py <manifest.json> <clone>
Reports the subject, whether every workflow job has one coverage entry, whether every coverage
entry is ok, and whether each act-mapped entry names an act job that succeeded.
"""
import hashlib
import json
import os
import sys

import yaml


def main():
    manifest = json.load(open(sys.argv[1], encoding="utf-8"))
    clone = sys.argv[2]
    print("subject", json.dumps(manifest["subject"], sort_keys=True))
    print("result", manifest["result"], "schema", manifest["schema"])
    coverage = manifest["execution"]["coverage"]
    act_jobs = manifest["execution"]["act"]["jobs"]
    expected = set()
    for name, digest in manifest["definitions"]["candidate"].items():
        path = os.path.join(clone, ".github/workflows", name)
        with open(path, "rb") as handle:
            raw = handle.read()
        print(name, "digest_match", hashlib.sha256(raw).hexdigest() == digest,
              "head_equal", manifest["definitions"]["head"][name] == digest)
        for job in yaml.safe_load(raw)["jobs"]:
            expected.add(f"{name[:-4]}/{job}")
    print("workflow_jobs", len(expected), "coverage_entries", len(coverage))
    print("jobs_without_coverage", sorted(expected - set(coverage)))
    print("coverage_without_job", sorted(set(coverage) - expected))
    print("entries_not_ok", sorted(k for k, v in coverage.items() if v.get("ok") is not True))
    print("by_act", sum(v["by"] == "act" for v in coverage.values()),
          "by_not_run", sum(v["by"] == "not-run" for v in coverage.values()),
          "by_bank", sum(v["by"] not in ("act", "not-run") for v in coverage.values()))
    print("act_mapped_not_success",
          sorted(k for k, v in coverage.items() if v["by"] == "act" and act_jobs.get(v["act_job"]) != "success"))
    print("act_exit", manifest["execution"]["act"]["exit_code"])
    for name, bank in manifest["execution"]["banks"].items():
        print("bank", name, "exit", bank["exit_code"], "commands", len(bank["commands"]),
              "all_zero", all(c["exit_code"] == 0 for c in bank["commands"]))


if __name__ == "__main__":
    sys.exit(main())
