#!/usr/bin/env python3
"""Prove only the authorized masks and selftest additions changed executable policy."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path('$CANDIDATE')
OUT = Path(__file__).resolve().parents[1]
BASE = '7ab1c8d0ad073fbc1977c455dea89b7b318d4e52'
PATH = 'scripts/check_baremetal_only.py'
ADDED_KEYS = {
    'TERM_MASKS': {'tb/verilator/milan_dp/sim_pool.py', 'tb/verilator/milan_dp/test_sim_pool.py',
                   'tb/verilator/milan_dp/README.md'},
    'HOST_RUNTIME_MASKS': {'tb/verilator/milan_dp/sim_pool.py', 'tb/verilator/milan_dp/test_sim_pool.py'},
}


def main():
    original = subprocess.check_output(['rtk', 'proxy', 'git', 'show', BASE + ':' + PATH], cwd=ROOT)
    candidate = (ROOT / PATH).read_bytes()
    tree = ast.parse(candidate)
    added_functions = {'_sim_pool_host_fixtures', '_arms_sim_pool_host_masks'}
    assert {node.name for node in tree.body if isinstance(node, ast.FunctionDef)
            and node.name in added_functions} == added_functions
    tree.body = [node for node in tree.body if not (isinstance(node, ast.FunctionDef)
                 and node.name in added_functions)]
    seen = set()
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in ADDED_KEYS:
                assert isinstance(node.value, ast.Dict)
                pairs = list(zip(node.value.keys, node.value.values))
                removed = {key.value for key, value in pairs if key.value in ADDED_KEYS[name]}
                assert removed == ADDED_KEYS[name]
                node.value.keys = [key for key, value in pairs if key.value not in removed]
                node.value.values = [value for key, value in pairs if key.value not in removed]
                seen.add(name)
        if isinstance(node, ast.FunctionDef) and node.name == 'selftest':
            group_loop = next(child for child in node.body if isinstance(child, ast.For))
            assert isinstance(group_loop.iter, ast.Tuple)
            old_count = len(group_loop.iter.elts)
            group_loop.iter.elts = [item for item in group_loop.iter.elts
                                   if item.id != '_arms_sim_pool_host_masks']
            assert len(group_loop.iter.elts) == old_count - 1
    assert seen == set(ADDED_KEYS)
    assert ast.dump(tree) == ast.dump(ast.parse(original)), 'Unexpected policy/control edit'
    local_failure = (OUT / 'raw/baseline-check.log').read_bytes()
    public_failure = (OUT / 'public/original-failure-29.log').read_bytes()
    assert local_failure == public_failure
    result = dict(base=BASE, current_checker_sha256=hashlib.sha256(candidate).hexdigest(),
                  additions_only=['five file-pinned mask entries', 'two private fixture/control helpers',
                                  'one selftest registration'],
                  preexisting_policy_and_controls_ast_identical=True,
                  original_failure_byte_identical=True,
                  failure_sha256=hashlib.sha256(public_failure).hexdigest())
    (OUT / 'policy-scope-proof.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
