#!/usr/bin/env python3
"""R638-3 probe: plant command forms in a fixture tree and record the deriver's outcome.

Usage: CI_IMAGE_SHFMT=<pinned shfmt> python3 probe_command_table.py <checkout> <scratch-dir>
Outcomes: REFUSED (named refusal), RESIDUE (accepted but listed as residue),
ACCEPTED-SILENT (accepted, nothing installed recorded, no residue entry).
The fixture root lives under <scratch-dir>, which must not be under /tmp.
"""
import json
import shutil
import sys
from pathlib import Path

checkout = Path(sys.argv[1]).resolve()
scratch = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(checkout / 'scripts'))
import ci_tool_inventory as inventory  # noqa: E402

PREFIX = "name: fixture\njobs:\n  gate:\n    steps:\n"

CASES = [
    # (id, workflow step text, {relative file: content})
    ('control-npx', "      - run: npx --yes fixture@1.2.3\n", {}),
    ('gh-extension-install', "      - run: gh extension install example/gh-fixture\n", {}),
    ('gh-release-download', "      - run: gh release download v1.0 -R example/tool -p 'tool*'\n", {}),
    ('git-submodule-add', "      - run: git submodule add https://example.invalid/tool.git third_party/tool\n", {}),
    ('git-config-then-submodule', "      - run: |\n          git config submodule.x.url https://example.invalid/tool.git\n          git submodule update --init x\n", {}),
    ('git-clone-scp-syntax', "      - run: git clone --no-hardlinks git@example.invalid:org/tool.git tool\n", {}),
    ('git-archive-remote', "      - run: git archive --remote=https://example.invalid/tool.git HEAD -o tool.tar\n", {}),
    ('python-heredoc-no-dash', "      - run: |\n          python3 <<'EOF'\n          import urllib.request\n          urllib.request.urlretrieve('https://example.invalid/tool', 'tool')\n          EOF\n", {}),
    ('python-heredoc-I-dash', "      - run: |\n          python3 -I - <<'EOF'\n          import urllib.request\n          urllib.request.urlretrieve('https://example.invalid/tool', 'tool')\n          EOF\n", {}),
    ('python-dash-heredoc-control', "      - run: |\n          python3 - <<'EOF'\n          import urllib.request\n          urllib.request.urlretrieve('https://example.invalid/tool', 'tool')\n          EOF\n", {}),
    ('bash-herestring', "      - run: bash <<< 'npx fixture'\n", {}),
    ('pipe-to-bash', "      - run: echo 'npx fixture' | bash\n", {}),
    ('bash-c-control', "      - run: bash -c 'npx fixture'\n", {}),
    ('py-os-popen', "      - run: python3 scripts/p.py\n", {'scripts/p.py': "import os\nos.popen('npx fixture').read()\n"}),
    ('py-os-execvp', "      - run: python3 scripts/p.py\n", {'scripts/p.py': "import os\nos.execvp('npx', ['npx', 'fixture'])\n"}),
    ('py-os-spawnlp', "      - run: python3 scripts/p.py\n", {'scripts/p.py': "import os\nos.spawnlp(os.P_WAIT, 'npx', 'npx', 'fixture')\n"}),
    ('py-asyncio-subprocess', "      - run: python3 scripts/p.py\n", {'scripts/p.py': "import asyncio\nasyncio.run(asyncio.create_subprocess_exec('npx', 'fixture'))\n"}),
    ('py-static-alias', "      - run: python3 scripts/p.py\n", {'scripts/p.py': "import subprocess\nrunner = subprocess.run\nrunner(['npx', 'fixture'])\n"}),
    ('py-pip-in-process', "      - run: python3 scripts/p.py\n", {'scripts/p.py': "from pip._internal.cli.main import main\nmain(['install', 'fixture'])\n"}),
    ('py-urllib3', "      - run: python3 scripts/p.py\n", {'scripts/p.py': "import urllib3\nopen('tool', 'wb').write(urllib3.request('GET', 'https://example.invalid/tool').data)\n"}),
    ('py-importlib-network', "      - run: python3 scripts/p.py\n", {'scripts/p.py': "import importlib\nr = importlib.import_module('urllib.request')\nr.urlretrieve('https://example.invalid/tool', 'tool')\n"}),
    ('py-ssl-socket-alt', "      - run: python3 scripts/p.py\n", {'scripts/p.py': "import ssl\nimport asyncio\nasyncio.run(asyncio.open_connection('example.invalid', 443, ssl=ssl.create_default_context()))\n"}),
    ('py-urllib-control', "      - run: python3 scripts/p.py\n", {'scripts/p.py': "import urllib.request\nurllib.request.urlretrieve('https://example.invalid/tool', 'tool')\n"}),
    ('make-pattern-rule', "      - run: make -C fx run\n", {'fx/Makefile': "run: tool.bin\n\techo ok\n%.bin:\n\tnpx fixture\n"}),
    ('make-pattern-control', "      - run: make -C fx run\n", {'fx/Makefile': "run: tool.bin\n\techo ok\ntool.bin:\n\tnpx fixture\n"}),
    ('make-directory-long-option', "      - run: make --directory=fx run\n", {'Makefile': "run:\n\techo ok\n", 'fx/Makefile': "run:\n\tnpx fixture\n"}),
    ('working-directory-make', "      - run: make\n        working-directory: fx\n", {'Makefile': "all:\n\techo ok\n", 'fx/Makefile': "all:\n\tnpx fixture\n"}),
    ('job-level-reusable-workflow', None, {}),
    # Forms listed by R638-2-F1 and R639-2-F1 (expect REFUSED, or recorded for container/services)
    ('r638-2-dpkg', "      - run: sudo dpkg -i ./fixture_1.0_amd64.deb\n", {}),
    ('r638-2-npx', "      - run: npx --yes tool@1.2.3\n", {}),
    ('r638-2-go-install', "      - run: go install example.invalid/tool@v1.0.0\n", {}),
    ('r638-2-snap', "      - run: sudo snap install tool\n", {}),
    ('r638-2-uv-tool', "      - run: uv tool install tool\n", {}),
    ('r638-2-docker-run', "      - run: docker run example/tool:tag --version\n", {}),
    ('r638-2-git-fetch-url', "      - run: git -C somewhere fetch https://example.invalid/tool.git\n", {}),
    ('r638-2-followed-urllib', "      - run: python3 scripts/fetch.py\n", {'scripts/fetch.py': "import urllib.request\nurllib.request.urlretrieve('https://example.invalid/tool', 'tool')\n"}),
    ('r639-2-keyword-args', "      - run: python3 scripts/bootstrap.py\n", {'scripts/bootstrap.py': "import subprocess\nsubprocess.run(args='python3 -m pip install fixture-package==1.0', shell=True)\n"}),
    ('r639-2-root-script', "      - run: python3 bootstrap.py\n", {'bootstrap.py': "import subprocess\nsubprocess.run(['python3', '-m', 'pip', 'install', 'fixture-package==1.0'])\n"}),
    ('r639-2-makefile-download-build', "      - run: make -C tools all\n", {'tools/Makefile': "all: install\ninstall: tool.tar.gz\n\ttar xf tool.tar.gz && $(MAKE) -C tool install\ntool.tar.gz:\n\tcurl -fsSL -o tool.tar.gz https://example.invalid/tool.tar.gz\n"}),
    ('newly-added-command', "      - run: brand_new_tool --version\n", {}),
]


def run_case(case_id, step, files):
    root = scratch / 'probe-roots' / case_id
    if root.exists():
        shutil.rmtree(root)
    (root / 'ci/image').mkdir(parents=True)
    for name in ('command-table.json', 'sources.lock.json'):
        shutil.copyfile(checkout / 'ci/image' / name, root / 'ci/image' / name)
    (root / '.github/workflows').mkdir(parents=True)
    if step is None:
        text = "name: fixture\njobs:\n  gate:\n    uses: example/tools/.github/workflows/install.yml@main\n"
    elif step.startswith('CONTAINER:'):
        text = "name: fixture\njobs:\n  gate:\n    " + step[len('CONTAINER:'):] + "    steps:\n      - run: echo ok\n"
    else:
        text = PREFIX + step
    (root / '.github/workflows/test.yml').write_text(text)
    for name, content in files.items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text(content)
    try:
        result = inventory.derive(root)
    except Exception as error:  # noqa: BLE001 - record any refusal type
        return {'case': case_id, 'outcome': 'REFUSED', 'detail': f'{type(error).__name__}: {error}'}
    outcome = 'RESIDUE' if result['residue'] else 'ACCEPTED-SILENT'
    return {'case': case_id, 'outcome': outcome, 'residue': result['residue'],
            'tools': [{k: t.get(k) for k in ('tool', 'kind', 'pin')} for t in result['tools']]}


CASES += [
    ('r638-2-container-tag', 'CONTAINER:container: example/tool:latest\n', {}),
    ('r638-2-container-digest', 'CONTAINER:container: example/tool@sha256:' + 'a' * 64 + '\n', {}),
    ('r638-2-services-tag', 'CONTAINER:services:\n      db: example/db:16\n', {}),
    ('r638-2-services-digest', 'CONTAINER:services:\n      db:\n        image: example/db@sha256:' + 'b' * 64 + '\n', {}),
]
rows = [run_case(*c) for c in CASES]
for row in rows:
    print(json.dumps(row, sort_keys=True))
