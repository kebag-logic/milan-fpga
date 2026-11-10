#!/usr/bin/env python3
"""Scratch: plant each changed-sink-walk defect in a copy of src/acmp.c, build the walk test against it at 33 sinks
with the arm's flags, and report which tests fail. usage: walk_plants.py STACK OUT"""
import subprocess, sys, json
from pathlib import Path
root, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
PLANTS = {
 'walk-bind-unmarked': ("\tstruct acmp_sink *s = &a->sinks[k];\n\tmark(a, k);\n\tbool sw", "\tstruct acmp_sink *s = &a->sinks[k];\n\tbool sw"),
 'walk-unbind-unmarked': ("\tstruct acmp_sink *s = &a->sinks[k];\n\tmark(a, k);\n\tif (s->state", "\tstruct acmp_sink *s = &a->sinks[k];\n\tif (s->state"),
 'walk-probe-response-unmarked': ("\tmark(a, k);\n\tsm_stop(s);\n\tif (rsp->status", "\tsm_stop(s);\n\tif (rsp->status"),
 'walk-adp-unmarked': ("\t\ttaken++;\n\t\tmark(a, k);\n", "\t\ttaken++;\n"),
 'walk-expired-interface-unmarked': ("\ta->dirty_if |= 1u << interface;\n", ""),
 'walk-aging-unmarked': ("\t\t\tmark(a, k);\n\t\t\ts->adp_armed = false;\n", "\t\t\ts->adp_armed = false;\n"),
 'walk-expiry-unmarked': ("\t\t\tmark(a, k);\n\t\t\tsm_expired(a, k);", "\t\t\tsm_expired(a, k);"),
 'walk-registered-unmarked': ("\tmark(a, sink);\n\tsm_stop(s);\n", "\tsm_stop(s);\n"),
 'walk-kind-unmarked': ("\tmark(a, sink);\n\ta->sinks[sink].tk_failed = failed;", "\ta->sinks[sink].tk_failed = failed;"),
 'walk-unregistered-unmarked': ("\tmark(a, sink);\n\tsrp_stop(a, sink);", "\tsrp_stop(a, sink);"),
 'walk-started-unmarked': ("\tmark(a, sink);\n\ta->sinks[sink].started = started;", "\ta->sinks[sink].started = started;"),
 'walk-release-unmarked': ("\t\t\t\t\tmark(a, k);\n\t\t\t\t\ta->sinks[k].change_owed--;", "\t\t\t\t\ta->sinks[k].change_owed--;"),
 'walk-probe-left-unmarked': ("\t\tmark(a, o->probe_of - 1u);\n", ""),
 'walk-restore-unmarked': ("\tsink_reset(a, sink);\n\tmark(a, sink);\n", "\tsink_reset(a, sink);\n"),
 'walk-rollback-unmarked': ("\t\tsink_settle(&a->sinks[k]);\n\t\tmark(a, k);\n", "\t\tsink_settle(&a->sinks[k]);\n"),
 'walk-mark-interface-dropped': ("\ta->dirty_if |= 1u << a->sinks[k].interface;\n", ""),
 'walk-mark-word-zero': ("\ta->dirty[k / 32u] |= 1u << (k % 32u);", "\ta->dirty[0] |= 1u << (k % 32u);"),
 'walk-marked-word-zero': ("return ((a->dirty[k / 32u] >> (k % 32u)) & 1u) != 0u;", "return ((a->dirty[0] >> (k % 32u)) & 1u) != 0u;"),
}
flags = ['-O0', '-g', '-Wall', '-Wextra', '-Werror', '-DACMP_MAX_SINKS=33u', '-fsanitize=shift,undefined',
         '-fno-sanitize-recover=shift,undefined']
gt = '<tools>/gtest-1.14.0'
src = (root / 'src/acmp.c').read_text()
out.mkdir(parents=True, exist_ok=True)
test_o = out / 'test.o'
subprocess.run(['g++', '-std=c++20', *flags, f'-I{root}/include', f'-I{root}/tests', f'-I{gt}/include', '-c',
                str(root / 'tests/test_acmp_walk.cpp'), '-o', str(test_o)], check=True)
main_o = out / 'main.o'
subprocess.run(['g++', '-std=c++20', *flags, f'-I{gt}/include', '-c', str(root / 'tests/main.cpp'), '-o', str(main_o)], check=True)
result = {}
for name, (old, new) in PLANTS.items():
    if src.count(old) != 1:
        result[name] = f'{src.count(old)} sites'
        continue
    c = out / f'{name}.c'
    c.write_text(src.replace(old, new))
    o = out / f'{name}.o'
    subprocess.run(['gcc', '-std=c11', *flags, '-DNDEBUG', '-DCTRL_REENTRY_ASSERT', f'-I{root}/include', '-c', str(c), '-o', str(o)], check=True)
    exe = out / name
    subprocess.run(['g++', *flags, str(o), str(test_o), str(main_o), f'-L{gt}/lib', '-lgmock', '-lgtest', '-pthread', '-o', str(exe)], check=True)
    run = subprocess.run([str(exe)], capture_output=True, text=True, env={'LD_LIBRARY_PATH': f'{gt}/lib'})
    failed = sorted({l.split()[3] for l in run.stdout.splitlines() if l.startswith('[  FAILED  ] AcmpWalk.') and '(' in l})
    walkmsg = 'the changed-sink walk makes' in run.stdout
    result[name] = {'rc': run.returncode, 'failed': failed, 'trace_assertion': walkmsg}
    print(name, result[name], flush=True)
(out / 'result.json').write_text(json.dumps(result, indent=1))
