#!/usr/bin/env python3
"""Plant probes in hard-linked copies of a base tree and classify the deriver's response.

Usage: probes.py <base-tree> <work-dir> <harness> [probe-name ...]
Every edit unlinks before writing so the base tree is never modified.
"""
import json, os, shutil, subprocess, sys
from pathlib import Path

BASE, WORK, HARNESS = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
ONLY = set(sys.argv[4:])
INSTALL = "subprocess.run(['sudo', 'apt-get', 'install', '-y', 'cowsay'], check=True)\n"

def write(tree, rel, text, append=False):
    p = tree / rel
    old = p.read_text() if (append and p.exists()) else ''
    if p.exists() or p.is_symlink():
        p.unlink()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(old + text)

def wf_step(tree, run, job='docs-check', env=None, extra=''):
    """Append one step to a job of docs.yml (text edit, keeps the rest byte-identical)."""
    rel = '.github/workflows/docs.yml'
    text = (tree / rel).read_text()
    marker = f'\n  {job}:\n'
    start = text.index(marker)
    nxt = text.find('\n  ', start + len(marker))
    # find the next job header (two-space indent, name, colon) after start
    import re
    m = re.search(r'\n  [A-Za-z0-9_-]+:\n', text[start + len(marker):])
    end = start + len(marker) + m.start() if m else len(text)
    body = '      - name: review probe\n'
    if env:
        body += '        env:\n' + ''.join(f'          {k}: {v}\n' for k, v in env.items())
    body += extra
    body += '        run: |\n' + ''.join('          ' + l + '\n' for l in run.splitlines())
    new = text[:end].rstrip('\n') + '\n' + body + text[end:]
    write(tree, rel, new)

PROBES = {}
def probe(name, expect):
    def deco(fn):
        PROBES[name] = (fn, expect)
        return fn
    return deco

# ---- controls: the harness detects a walked installer ----
@probe('C0-walked-script-installer', 'REFUSED')
def _(t):
    write(t, 'scripts/check_doc_paths.py', '\nimport subprocess\n' + INSTALL, append=True)

@probe('C1-workflow-literal-unknown-package', 'REFUSED')
def _(t):
    wf_step(t, 'sudo apt-get install -y --no-install-recommends cowsay')

# ---- Python: allowlisted local module reached through sys.path ----
@probe('P1-local-module-run.py-installer', 'REFUSED')
def _(t):
    write(t, 'tb/verilator/nvm_capture_cpu/run.py', '\n' + INSTALL, append=True)

@probe('P2-local-module-flash_map-installer', 'REFUSED')
def _(t):
    write(t, 'sw/litex/flash_map.py', '\nimport subprocess\n' + INSTALL, append=True)

# ---- Make: constructs accepted then resolved differently from GNU make ----
@probe('P3-make-leading-space-assignment', 'REFUSED')
def _(t):
    write(t, 'tb/verilator/zz_probe_ws/Makefile',
          'CMD = echo ok\n CMD = sudo apt-get install -y cowsay # note: leading space\n'
          '.PHONY: probe\nprobe:\n\t$(CMD)\n')

@probe('P4-make-builtin-implicit-rule', 'REFUSED')
def _(t):
    write(t, 'tb/verilator/zz_probe_builtin/Makefile',
          'CC = sudo apt-get install -y cowsay ; cc\nprobe_builtin: probe_builtin.c\n')
    write(t, 'tb/verilator/zz_probe_builtin/probe_builtin.c', 'int main(void) { return 0; }\n')

@probe('P5-make-pattern-first-prerequisite', 'REFUSED')
def _(t):
    write(t, 'tb/verilator/zz_probe_lt/Makefile',
          '.PHONY: all\nall: probe.out\nprobe.out: benign.sh\n%.out: %_evil.sh\n\tbash $<\n')
    write(t, 'tb/verilator/zz_probe_lt/benign.sh', 'echo ok\n')
    write(t, 'tb/verilator/zz_probe_lt/probe_evil.sh', 'sudo apt-get install -y cowsay\n')

@probe('P6-make-shell-assignment-with-colon', 'REFUSED')
def _(t):
    write(t, 'tb/verilator/zz_probe_bang/Makefile',
          'X != sudo apt-get install -y cowsay >&2; echo a:b\n.PHONY: all\nall:\n\techo ok\n')

# ---- Shell: command substitution whose output is not pwd's stdout ----
@probe('P7-shell-cmdsubst-pwd-redirected', 'REFUSED')
def _(t):
    wf_step(t, 'cd "$(cd scripts && pwd > /dev/null)"\npython3 zz_probe_cwd.py')
    write(t, 'zz_probe_cwd.py', 'import subprocess\n' + INSTALL)
    write(t, 'scripts/zz_probe_cwd.py', "print('ok')\n")

# ---- closure controls: one unlisted construct per walker ----
@probe('N1-shell-test-clause', 'REFUSED')
def _(t): wf_step(t, '[[ -f README.md ]] && echo ok')
@probe('N2-shell-arith-command', 'REFUSED')
def _(t): wf_step(t, 'i=0\n((i++))\necho ok')
@probe('N3-shell-background', 'REFUSED')
def _(t): wf_step(t, 'echo ok &\nwait')
@probe('N4-shell-coproc', 'REFUSED')
def _(t): wf_step(t, 'coproc echo ok')
@probe('N5-trap-nested-test-clause', 'REFUSED')
def _(t): wf_step(t, "trap '[[ -f x ]] && echo y' EXIT\necho ok")
@probe('N6-sourced-file-uncensused-node', 'REFUSED')
def _(t):
    import re
    src = (t / 'syn/yosys/run.sh').read_text()
    m = re.search(r'^\s*(?:source|\.)\s+"?([^"\s]+)"?', src, re.M)
    rel = None
    if m:
        cand = m.group(1).replace('$(dirname "$0")', 'syn/yosys').replace('${HERE}', 'syn/yosys')
    for p in ['syn/yosys/malloc.sh']:
        if (t / p).exists(): rel = p
    write(t, rel, '\n[[ -n "${X:-}" ]] && echo y\n', append=True)
@probe('N7-workflow-env-BASH_ENV', 'REFUSED')
def _(t): wf_step(t, 'echo ok', env={'BASH_ENV': '/tmp/x'})
@probe('N8-shell-export-PYTHONPATH', 'REFUSED')
def _(t): wf_step(t, 'export PYTHONPATH=scripts\necho ok')
@probe('N9-shell-prefix-LD_LIBRARY_PATH', 'REFUSED')
def _(t): wf_step(t, 'LD_LIBRARY_PATH=/tmp python3 scripts/check_doc_paths.py')
@probe('N10-make-MAKEFILES', 'REFUSED')
def _(t): write(t, 'tb/verilator/zz_probe_mk/Makefile', 'MAKEFILES = x.mk\n.PHONY: all\nall:\n\techo ok\n')
@probe('N11-make-vpath', 'REFUSED')
def _(t): write(t, 'tb/verilator/zz_probe_vp/Makefile', 'vpath %.c src\n.PHONY: all\nall:\n\techo ok\n')
@probe('N12-make-eval', 'REFUSED')
def _(t): write(t, 'tb/verilator/zz_probe_ev/Makefile', '$(eval X = y)\n.PHONY: all\nall:\n\techo ok\n')
@probe('N13-make-ifdef', 'REFUSED')
def _(t): write(t, 'tb/verilator/zz_probe_id/Makefile', 'ifdef X\n$(error x)\nendif\n.PHONY: all\nall:\n\techo ok\n')
@probe('N14-make-ONESHELL', 'REFUSED')
def _(t): write(t, 'tb/verilator/zz_probe_os/Makefile', '.ONESHELL:\n.PHONY: all\nall:\n\techo ok\n')
@probe('N15-make-automatic-D', 'REFUSED')
def _(t): write(t, 'tb/verilator/zz_probe_ad/Makefile', '.PHONY: all\nall:\n\techo $(@D)\n')
@probe('N16-python-match-stmt', 'REFUSED')
def _(t): write(t, 'scripts/check_doc_paths.py', '\nmatch 1:\n    case 1:\n        pass\n', append=True)
@probe('N17-python-dunder-import', 'REFUSED')
def _(t): write(t, 'scripts/check_doc_paths.py', "\n__import__('os')\n", append=True)
@probe('N18-python-local-shadow-pkg', 'REFUSED')
def _(t):
    # a local package shadowing an allowlisted external import next to a walked script
    write(t, 'scripts/yaml/__init__.py', 'import subprocess\n' + INSTALL)
@probe('N19-workflow-step-shell', 'REFUSED')
def _(t): wf_step(t, 'echo ok', extra='        shell: sh\n')
@probe('N20-job-uses', 'REFUSED')
def _(t):
    rel = '.github/workflows/docs.yml'
    write(t, rel, (t / rel).read_text().rstrip('\n') + '\n  zz-probe:\n    uses: ./.github/workflows/x.yml\n')
@probe('N21-container-moving-tag', 'REFUSED')
def _(t):
    rel = '.github/workflows/docs.yml'
    write(t, rel, (t / rel).read_text().rstrip('\n') + '\n  zz-probe:\n    runs-on: ubuntu-latest\n    container: ubuntu:24.04\n    steps:\n      - run: echo ok\n')
@probe('N22-new-command-name', 'REFUSED')
def _(t): wf_step(t, 'cowsay hello')

@probe('P3b-make-leading-space-assignment', 'REFUSED')
def _(t):
    write(t, 'tb/verilator/zz_probe_ws2/Makefile',
          'CMD = echo ok\n CMD = sudo apt-get install -y cowsay # note:\n'
          '.PHONY: probe\nprobe:\n\t$(CMD)\n')

@probe('P6b-make-shell-assignment-with-colon', 'REFUSED')
def _(t):
    write(t, 'tb/verilator/zz_probe_bang2/Makefile',
          'X != sudo apt-get install -y cowsay >&2; echo a:\n.PHONY: all\nall:\n\techo ok\n')

@probe('N16b-python-match-stmt-undeclared', 'REFUSED')
def _(t): write(t, 'scripts/check_doc_style.py', '\nmatch 1:\n    case 1:\n        pass\n', append=True)
@probe('N17b-python-dunder-import-undeclared', 'REFUSED')
def _(t): write(t, 'scripts/check_doc_style.py', "\n__import__('os')\n", append=True)
@probe('N18b-python-local-shadow-pkg-builder', 'REFUSED')
def _(t): write(t, 'sw/builder/yaml/__init__.py', 'import subprocess\n')
@probe('N23-python-walrus-undeclared', 'REFUSED')
def _(t): write(t, 'scripts/check_doc_style.py', "\nif (zz := 1):\n    pass\n", append=True)

# ---- re-run of every form listed by R638-4 and R639-4 (payload: unclassified brand_new_command) ----
HID = 'brand_new_command\n'
def hidden(t, rel='hidden.sh'): write(t, rel, HID); os.chmod(t / rel, 0o755)
@probe('R4-W1-step-shell-hidden', 'REFUSED')
def _(t): hidden(t); wf_step(t, 'echo okay', extra='        shell: bash hidden.sh {0}\n')
@probe('R4-W2-defaults-run-shell', 'REFUSED')
def _(t):
    hidden(t); rel = '.github/workflows/docs.yml'
    write(t, rel, (t / rel).read_text().rstrip('\n') + '\ndefaults:\n  run:\n    shell: bash hidden.sh {0}\n')
@probe('R4-W3-env-BASH_ENV-hidden', 'REFUSED')
def _(t): hidden(t); wf_step(t, 'echo okay', env={'BASH_ENV': 'hidden.sh'})
@probe('R4-W4-GITHUB_PATH-write', 'REFUSED')
def _(t):
    write(t, 'tools/git', HID); wf_step(t, 'echo "$PWD/tools" >> "$GITHUB_PATH"\ngit rev-parse HEAD')
@probe('R4-W5-export-PATH', 'REFUSED')
def _(t): write(t, 'tools/git', HID); wf_step(t, 'export PATH="tools:$PATH"\ngit rev-parse HEAD')
@probe('R4-S7-prefix-PATH-lookup', 'REFUSED')
def _(t):
    write(t, 'zzs7/bootstrap.sh', 'echo okay\n'); write(t, 'zzs7/sub/bootstrap.sh', HID)
    wf_step(t, 'cd zzs7\nPATH="sub:$PATH" bootstrap.sh')
@probe('R4-M1-make-SHELL', 'REFUSED')
def _(t):
    write(t, 'tb/verilator/zz_m1/Makefile', 'SHELL := ./hidden.sh\n.PHONY: all\nall:\n\techo okay\n'); hidden(t, 'tb/verilator/zz_m1/hidden.sh')
@probe('R4-M1b-make-SHELL-override', 'REFUSED')
def _(t):
    write(t, 'zzm1b/Makefile', '.PHONY: all\nall:\n\techo okay\n'); hidden(t, 'zzm1b/runner.sh')
    wf_step(t, 'make -C zzm1b SHELL=./runner.sh')
@probe('R4-X1-xargs-pip', 'REFUSED')
def _(t): wf_step(t, 'echo evilpkg | xargs python3 -m pip install')
@probe('R4-X2-sudo-xargs-apt', 'REFUSED')
def _(t): wf_step(t, 'echo evilpkg | sudo xargs apt-get install -y')
@probe('R4-X3-xargs-bash', 'REFUSED')
def _(t): wf_step(t, 'echo hidden.sh | xargs bash')
@probe('R4-S2-printf-v', 'REFUSED')
def _(t):
    write(t, 'zzs/bootstrap.sh', 'echo okay\n'); hidden(t, 'zzs/hidden.sh')
    wf_step(t, "cd zzs\nname=bootstrap.sh\nprintf -v name '%s' hidden.sh\nbash \"$name\"")
@probe('R4-S3-read-herestring', 'REFUSED')
def _(t):
    write(t, 'zzs/bootstrap.sh', 'echo okay\n'); hidden(t, 'zzs/hidden.sh')
    wf_step(t, 'cd zzs\nf=bootstrap.sh\nread -r f <<< hidden.sh\nbash "$f"')
@probe('R4-S4-source-variable', 'REFUSED')
def _(t):
    write(t, 'zzs/bootstrap.sh', 'echo okay\n'); hidden(t, 'zzs/hidden.sh'); write(t, 'zzs/fragment.sh', 'name=hidden.sh\n')
    wf_step(t, 'cd zzs\nname=bootstrap.sh\nsource fragment.sh\nbash "$name"')
@probe('R4-S5-source-directory', 'REFUSED')
def _(t):
    write(t, 'zzs/bootstrap.sh', 'echo okay\n'); hidden(t, 'zzs/sub/bootstrap.sh'); write(t, 'zzs/fragment.sh', 'cd sub\n')
    wf_step(t, 'cd zzs\nsource fragment.sh\nbash bootstrap.sh')
@probe('R4-M2-make-default-from-step-env', 'REFUSED')
def _(t):
    write(t, 'zzm2/Makefile', 'TOOL ?= echo\n.PHONY: all\nall:\n\t$(TOOL) okay\n')
    wf_step(t, 'make -C zzm2', env={'TOOL': 'brand_new_command'})
@probe('R4-M2b-make-default-from-export', 'REFUSED')
def _(t):
    write(t, 'zzm2/Makefile', 'TOOL ?= echo\n.PHONY: all\nall:\n\t$(TOOL) okay\n')
    wf_step(t, 'export TOOL=brand_new_command\nmake -C zzm2')
@probe('R4-M3-make-at-D', 'REFUSED')
def _(t):
    write(t, 'zzm3/Makefile', '.PHONY: sub/x\nsub/x:\n\tbash ./$(@D)/bootstrap.sh\n')
    write(t, 'zzm3/bootstrap.sh', 'echo okay\n'); hidden(t, 'zzm3/sub/bootstrap.sh')
    wf_step(t, 'make -C zzm3 sub/x')
@probe('R4-M4-recursive-override', 'REFUSED')
def _(t):
    write(t, 'zzm4/Makefile', '.PHONY: all\nall:\n\t$(MAKE) -C sub\n')
    write(t, 'zzm4/sub/Makefile', 'TOOL = echo\n.PHONY: all\nall:\n\t$(TOOL) okay\n')
    wf_step(t, 'make -C zzm4 TOOL=brand_new_command')
@probe('R4-S6-literal-marker-inline', 'REFUSED')
def _(t): wf_step(t, "bash -c 'brand_new_command <dynamic>'")
@probe('R4-S8-literal-dollar-make-dir', 'REFUSED')
def _(t):
    write(t, 'zzs8/sub$x/Makefile', '.PHONY: all\nall:\n\tbrand_new_command\n')
    wf_step(t, "make -C 'zzs8/sub$x'")
@probe('R4-Y1-ctypes-system', 'REFUSED')
def _(t):
    write(t, 'zzy1.py', 'import ctypes\nctypes.CDLL(None).system(b"brand_new_command")\n'); wf_step(t, 'python3 zzy1.py')
@probe('R4-Y3-from-local-pkg-import-module', 'REFUSED')
def _(t):
    write(t, 'zzy3/run_me.py', 'from firmware import hidden\n')
    write(t, 'zzy3/firmware/__init__.py', '')
    write(t, 'zzy3/firmware/hidden.py', 'import subprocess\nsubprocess.run(["brand_new_command"])\n')
    wf_step(t, 'python3 zzy3/run_me.py')
@probe('R4b-F1d-conditional-functions', 'REFUSED')
def _(t): wf_step(t, 'if true; then f() { brand_new_command; }; else f() { echo okay; }; fi\nf')
@probe('R4b-F1c-background-cd', 'REFUSED')
def _(t):
    write(t, 'zzs/bootstrap.sh', HID); write(t, 'zzs/sub/bootstrap.sh', 'echo okay\n')
    wf_step(t, 'cd zzs\ncd sub & bash bootstrap.sh')
@probe('R4b-F3-literal-marker-echo', 'REFUSED')
def _(t): wf_step(t, "bash -c 'echo \"<dynamic>\"; brand_new_command'")
@probe('R4b-F4a-local-json-shadow', 'REFUSED')
def _(t):
    write(t, 'zzf4/bootstrap.py', 'import json\n')
    write(t, 'zzf4/json/__init__.py', 'import subprocess\nsubprocess.run(["brand_new_command"])\n')
    wf_step(t, 'python3 zzf4/bootstrap.py')
@probe('R4b-F4b-local-pkg-init', 'REFUSED')
def _(t):
    write(t, 'zzf4b/bootstrap.py', 'import localpkg\n')
    write(t, 'zzf4b/localpkg/__init__.py', 'import subprocess\nsubprocess.run(["brand_new_command"])\n')
    wf_step(t, 'python3 zzf4b/bootstrap.py')
@probe('N16c-python-global-undeclared', 'REFUSED')
def _(t): write(t, 'scripts/check_doc_style.py', "\ndef zz():\n    global ZZ\n", append=True)
@probe('N23b-python-async-undeclared', 'REFUSED')
def _(t): write(t, 'scripts/check_doc_style.py', "\nasync def zz():\n    pass\n", append=True)

results = {}
for name, (fn, expect) in PROBES.items():
    if ONLY and name not in ONLY:
        continue
    tree = WORK / name
    if tree.exists():
        shutil.rmtree(tree)
    subprocess.run(['cp', '-al', str(BASE), str(tree)], check=True)
    fn(tree)
    watch = ['tb/verilator/nvm_capture_cpu/run.py', 'sw/litex/flash_map.py', 'zz_probe_cwd.py', 'scripts/zz_probe_cwd.py']
    r = subprocess.run([sys.executable, '-B', HARNESS, str(tree), str(BASE / 'ci/image/tool-inventory.json'), *watch],
                       capture_output=True, text=True)
    out = json.loads(r.stdout) if r.stdout.strip() else {'status': 'HARNESS-ERROR', 'stderr': r.stderr[-500:]}
    out['expected'] = expect
    out['ok'] = out['status'] == expect
    results[name] = out
    print(f"{name:42s} {out['status']:14s} expect={expect:8s} {'OK' if out['ok'] else 'UNEXPECTED'}  {out.get('message', '')[:150]}", flush=True)
json.dump(results, open(WORK / ('probe-results-' + ('-'.join(sorted(ONLY)) if ONLY else 'all') + '.json')[:200], 'w'), indent=1)
