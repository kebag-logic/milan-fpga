#!/usr/bin/env python3
"""Check the F0/F1 composition's shared generators and production registration."""
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess

PACKET = Path(__file__).resolve().parent
SOURCE = "d763fce6f3e48fa9c468aaa835653befb8382d06"
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")


def git(*args):
    return subprocess.run(["git", "-c", "core.commitGraph=false", *args],
                          env=ENV, check=True, capture_output=True).stdout


def main():
    inputs = ["scripts/nvm_contract.py", "scripts/nvm_klj2.py", "scripts/nvm_shape.py",
              "scripts/check_nvm_record_space.py", "sw/litex/flash_map.py",
              "sw/builder", "configs", "tb/verilator/nvm_backend",
              "tb/verilator/nvm_capture_cpu", ".github/workflows",
              "scripts/run_all_suites.sh", "sw/firmware/milan_baremetal"]
    unchanged = {}
    for name in inputs:
        before = git("ls-tree", SOURCE, "--", name)
        after = git("ls-tree", "HEAD", "--", name)
        assert before and before == after, name
        unchanged[name] = after.decode().strip()
    soc = "sw/litex/milan_soc.py"
    sources = [git("show", ref + ":" + soc).decode() for ref in [SOURCE, "HEAD"]]
    flash_maps = []
    for text in sources:
        nodes = ast.parse(text).body
        match = [n for n in nodes if isinstance(n, ast.Assign) and
                 any(isinstance(t, ast.Name) and t.id == "FLASHBOOT_RESERVED" for t in n.targets)]
        assert len(match) == 1
        flash_maps.append(ast.dump(match[0], include_attributes=False))
    assert flash_maps[0] == flash_maps[1]
    # This suffix emits the F1-generated constants and continues to main's end.
    suffixes = [text[text.index('        soc.add_constant("MILAN_NVM_LIVE_BASE"'):] for text in sources]
    assert suffixes[0] == suffixes[1]
    search = [".github/workflows", "scripts/run_all_suites.sh", "sw/builder", "sw/litex",
              "sw/firmware/ctrl", "docs/traceability/gen_module_matrix.py", "scripts/ci_scope.py"]
    result = subprocess.run(["rg", "-n", "ctrl_nvm", *search], capture_output=True)
    assert result.returncode == 1 and not result.stdout and not result.stderr
    whitespace = git("diff", "--check", "9e05246c5455b2a1df26038345709437e13c6f18", "HEAD")
    assert not whitespace
    receipt = {
        "head": git("rev-parse", "HEAD").decode().strip(),
        "source": SOURCE, "unchanged_shared_input_entries": unchanged,
        "soc_flash_map_ast_identical": True,
        "soc_nvm_constants_to_end_of_file_identical": True,
        "soc_nvm_suffix_sha256": hashlib.sha256(suffixes[1].encode()).hexdigest(),
        "production_registration_search": {"command": ["rg", "-n", "ctrl_nvm", *search],
                                           "rc": 1, "stdout": "", "stderr": "",
                                           "meaning": "no production link, loop hook or workflow registration"},
        "git_diff_check": "PASS", "result": "PASS",
    }
    (PACKET / "dependencies.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
