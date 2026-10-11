#!/usr/bin/env python3
"""Verify public publication hashes, gate identity and named mutation coverage."""
import hashlib
import json
from pathlib import Path
import re
import sys


def main():
    packet = Path(sys.argv[1]).resolve()
    receipts = packet / 'receipts'
    author = receipts / 'public-author'
    publication = json.loads((receipts / 'public-evidence-MANIFEST.json').read_text())
    verified = []
    for item in publication:
        if not item['file'].startswith('author-r2/'):
            continue
        f = author / item['file'].removeprefix('author-r2/')
        if f.is_file():
            assert hashlib.sha256(f.read_bytes()).hexdigest() == item['published_sha256'], str(f)
            verified.append(item)
    inner_differences = []
    for item in json.loads((author / 'evidence/round2/MANIFEST.json').read_text()):
        f = author / 'evidence/round2' / item['path']
        if f.is_file() and hashlib.sha256(f.read_bytes()).hexdigest() != item['sha256']:
            outer = next(x for x in verified if x['file'] == 'author-r2/evidence/round2/' + item['path'])
            assert outer['path_redacted'] and outer['original_sha256'] == item['sha256']
            inner_differences.append({'path': item['path'], 'explanation': 'outer publication records path redaction',
                                      'original': outer['original_sha256'], 'published': outer['published_sha256']})
    identity = {}
    for name in ('suites', 'lint', 'matrix', 'yosys'):
        a = (author / 'evidence/round2/base' / f'{name}.log').read_bytes()
        b = (author / 'evidence/round2/head' / f'{name}.log').read_bytes()
        assert a == b
        identity[name] = hashlib.sha256(a).hexdigest()
    assert sorted((author / 'evidence/round2/base/check.log').read_text().splitlines()) == sorted(
        (author / 'evidence/round2/head/check-final.log').read_text().splitlines())
    canon = (author / 'evidence/netlists/base-canon.txt').read_bytes()
    assert canon == (author / 'evidence/netlists/head-canon.txt').read_bytes()
    names = set(re.findall(r'^inventory (\S+):', (receipts / 'guards.log').read_text(), re.M))
    assert len(names) == 31
    boundary_pairs = {}
    for filename, frontends in [
        ('probes/boundaries.log', ('verilator', 'yosys')),
        ('probes/vivado.log', ('xsim', 'synth')),
        ('head/portability-step.log', ('yosys',)),
    ]:
        log = (author / 'evidence/round2' / filename).read_text()
        assert not re.search(r'^FAIL:', log, re.M)
        for guard in names:
            for frontend in frontends:
                for side in ('GUARD', 'ELAB'):
                    assert re.search(rf'^{side}\s+{frontend}\s+{re.escape(guard)}\s', log, re.M)
        boundary_pairs[filename] = log.splitlines()[-1]
    coverage = {}
    for filename, frontends, kinds in [
        ('mutants.log', ('verilator', 'yosys'), ('error', 'warning', 'initial', 'tightened', 'loosened')),
        ('mutants013.log', ('verilator', 'yosys'), ('error', 'warning', 'initial', 'tightened', 'loosened')),
        ('vivado-mutants.log', ('xsim', 'synth'), ('tightened', 'loosened')),
    ]:
        log = (author / 'evidence/round2/head' / filename).read_text()
        sections = re.split(r'^(\S+): rc=\d+ KILLED\n', log, flags=re.M)
        arms = dict(zip(sections[1::2], sections[2::2]))
        for guard in names:
            for kind in kinds:
                arm = guard + ':' + kind
                assert arm in arms, (filename, arm)
                expected = 'ELAB' if kind == 'tightened' else 'GUARD'
                # Boundary acceptance demands the named failure in each selected front end.
                if kind in ('tightened', 'loosened'):
                    for frontend in frontends:
                        assert re.search(rf'FAIL: {expected}\s+{frontend}\s+{re.escape(guard)}\s', arms[arm]), (filename, arm, frontend)
                else:
                    assert re.search(rf'FAIL: GUARD\s+\w+\s+{re.escape(guard)}\s', arms[arm])
        coverage[filename] = {'named_arms': len(arms), 'boundary_frontends': frontends,
                              'all_31_guards_covered': True, 'tally': log.splitlines()[-1]}
    results = {'publication_commit': '14f8fe421ca8699bcba10968c8e6a8abd09b343b',
               'public_author_files_hash_verified': len(verified),
               'inner_manifest_redaction_mapping': inner_differences,
               'round2_base': 'ef86ea848dbfb0d869108a1987accb203a17474d',
               'round2_head': '02063dc1b593d422406991bf0bc60e5cc47828ff',
               'identical_gate_records_sha256': identity, 'documentation_records': 'same sorted lines',
               'retained_canonical_netlist_rom_records': len(canon.splitlines()),
               'retained_canonical_netlist_rom_sha256': hashlib.sha256(canon).hexdigest(),
               'all_31_public_boundary_pairs': boundary_pairs,
               'mutation_coverage': coverage}
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
