"""Bounded documentation/idiom/hygiene/source gates; no native/act orchestrator."""
import concurrent.futures
import json
from pathlib import Path
from run import OUT, run


def main():
    commands = [
        ('toc-selftest', ['scripts/gen_toc.py', '--selftest']),
        ('toc-check', ['scripts/gen_toc.py', '--check']),
        ('toc-anchors', ['scripts/gen_toc.py', '--verify-anchors']),
        ('emdash-selftest', ['scripts/check_em_dash.py', '--selftest']),
        ('docs', ['scripts/docs_check.py']),
        ('py-idiom', ['scripts/check_py_idiom.py']),
        ('py-idiom-selftest', ['scripts/check_py_idiom.py', '--selftest']),
        ('hygiene', ['scripts/check_hygiene.py', '--check']),
        ('hygiene-selftest', ['scripts/check_hygiene.py', '--selftest']),
        ('doc-paths', ['scripts/check_doc_paths.py']),
        ('doc-style', ['scripts/check_doc_style.py']),
        ('doc-style-selftest', ['scripts/check_doc_style.py', '--selftest']),
        ('archive', ['scripts/check_archive.py']),
        ('archive-selftest', ['scripts/check_archive.py', '--selftest']),
        ('feature-status', ['scripts/check_feature_status.py', '--self-test']),
        ('traceability', ['docs/traceability/gen_module_matrix.py', '--check']),
        ('rtl-source-lists', ['scripts/check_rtl_source_lists.py']),
        ('rtl-source-lists-selftest', ['scripts/check_rtl_source_lists.py', '--selftest']),
        ('pp-sources', ['scripts/pp_srcs.py', '--check']),
        ('pp-sources-selftest', ['scripts/pp_srcs.py', '--selftest']),
        ('baremetal', ['scripts/check_baremetal_only.py', '--check']),
        ('baremetal-selftest', ['scripts/check_baremetal_only.py', '--selftest']),
        ('gptp-docs', ['scripts/check_gptp_docs.py']),
        ('solution-docs', ['scripts/check_solution_docs.py']),
        ('submodule-docs', ['scripts/check_submodule_docs.py']),
    ]
    def one(row):
        name, args = row
        return {'name': name, 'exit': run(name, ['python3', '-B', *args])}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(one, commands))
    (OUT / 'gates.json').write_text(json.dumps(results, indent=2) + '\n')
    return int(any(row['exit'] for row in results))


if __name__ == '__main__':
    raise SystemExit(main())
