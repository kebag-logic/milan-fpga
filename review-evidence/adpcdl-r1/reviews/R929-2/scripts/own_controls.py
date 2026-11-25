"""Usage: own_controls.py TREE WORK. Reviewer-owned defects in adp_rx, run plain and under address sanitizer."""
import subprocess, sys, pathlib, os, concurrent.futures as cf
tree, work = map(lambda p: pathlib.Path(p).resolve(), sys.argv[1:3])
work.mkdir(parents=True, exist_ok=True)
src = (tree / 'src/adp.c').read_text()
CMP = "(wire_be16(frame + ADP_HEADER_BYTES + 2u) & 0x07FFu) < ADP_CONTROL_DATA_LENGTH ||"
CDL = "(wire_be16(frame + ADP_HEADER_BYTES + 2u) & 0x07FFu)"
TGT = "\tuint64_t target = wire_be64(frame + ADP_HEADER_BYTES + 4u);\n"
FGN = "if (target != 0u && target != a->entity->entity_id) {"
VER = "(frame[ADP_HEADER_BYTES + 1u] & 0x70u) != 0u ||"
MSG = "(frame[ADP_HEADER_BYTES + 1u] & 0x0Fu) != ADP_MSG_ENTITY_DISCOVER) {"
HEAD = "\t// Milan v1.2 5.6.3.1\n\t// IEEE 1722.1-2021 Figure 6-1\n\t// IEEE 1722.1-2021 6.2.2.3 and 6.2.2.6\n\t// IEEE 1722.1-2021 6.2.7.1.3\n"
def rd(cond, idx): return f"\tif ({cond}) {{ volatile uint8_t s = frame[{idx}]; (void)s; }}\n"
M = {
 'control': (CMP, CMP),
 # reads past the frame
 'read-82-any-length': (TGT, rd('1', '82') + TGT),
 'read-82-long': (TGT, rd(CDL + ' > 56u', '82') + TGT),
 'read-82-only-57': (TGT, rd(CDL + ' == 57u', '82') + TGT),
 'read-82-only-2047': (TGT, rd(CDL + ' == 2047u', '82') + TGT),
 'read-last-surplus-octet': (TGT, rd(CDL + ' > 56u', '25u + ' + CDL) + TGT),
 'read-2072-only-2047': (TGT, rd(CDL + ' == 2047u', '2072') + TGT),
 'read-82-short-length': (HEAD, rd('len >= 82u && ' + CDL + ' < 56u', '82') + HEAD),
 'read-82-only-waiting': (TGT, rd(CDL + ' > 56u && a->state == ADP_STATE_WAITING', '82') + TGT),
 'read-82-only-foreign': (FGN, 'if (target != 0u && target != a->entity->entity_id) { volatile uint8_t s = frame[82]; (void)s; }\n\t' + FGN),
 'read-82-only-valid-time-31': (TGT, rd('(frame[16] >> 3) == 31u', '82') + TGT),
 # narrowed reads, caps, gaps
 'mask-0x03FF': (CMP, CMP.replace('0x07FF', '0x03FF')),
 'mask-0x01FF': (CMP, CMP.replace('0x07FF', '0x01FF')),
 'mask-0x00FF': (CMP, CMP.replace('0x07FF', '0x00FF')),
 'mask-0x007F': (CMP, CMP.replace('0x07FF', '0x007F')),
 'mask-0x003F': (CMP, CMP.replace('0x07FF', '0x003F')),
 'mask-0x05FF': (CMP, CMP.replace('0x07FF', '0x05FF')),
 'mask-0x0FFF': (CMP, CMP.replace('0x07FF', '0x0FFF')),
 'refuse-1000': (CMP, CMP + ' ' + CDL + ' == 1000u ||'),
 'refuse-57': (CMP, CMP + ' ' + CDL + ' == 57u ||'),
 'refuse-2047': (CMP, CMP + ' ' + CDL + ' == 2047u ||'),
 'cap-1500': (CMP, CMP + ' ' + CDL + ' > 1500u ||'),
 'bound-55': (CMP, CMP.replace('< ADP', '< 55u + 0u * ADP')),
 'bound-57': (CMP, CMP.replace('< ADP', '< 57u + 0u * ADP')),
 'surplus-refused-in-long-buffer': (CMP, CMP + ' (len > 82u && ' + CDL + ' > 56u) ||'),
 'target-from-after-surplus': (TGT, TGT.replace('+ 4u)', '+ 4u + (' + CDL + ' > 56u ? 8u : 0u))')),
 # a long length that skips another check
 'long-skips-foreign-target-check': (FGN, 'if (' + CDL + ' == 56u && target != 0u && target != a->entity->entity_id) {'),
 'long-skips-version-check': (VER, '(' + CDL + ' == 56u && ' + VER.replace(' ||', ') ||')),
 'long-skips-message-type-check': (MSG, '(' + CDL + ' == 56u && ' + MSG.replace(') {', ')) {')),
}
pkg = lambda a: subprocess.check_output(['pkg-config', a, 'gmock', 'gtest'], text=True).split()
cxxf, ld = pkg('--cflags'), pkg('--libs')
def sh(c): 
    r = subprocess.run(c, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if r.returncode: raise SystemExit('build failed: ' + ' '.join(map(str, c)) + r.stdout)
kinds = {'plain': [], 'asan': ['-fsanitize=address,undefined', '-fno-sanitize-recover=undefined']}
for k, s in kinds.items():
    for f in ('test_adp', 'main'):
        sh(['g++', '-std=c++20', '-O0', '-g', *s, *cxxf, '-I', tree/'include', '-I', tree/'tests', '-I', tree/'examples', '-c', tree/f'tests/{f}.cpp', '-o', work/f'{f}.{k}.o'])
def one(a):
    n, (old, new), k = a
    assert src.count(old) == 1, (n, src.count(old))
    c = work/f'{n}.c'; c.write_text(src.replace(old, new))
    b = work/f'{n}.{k}'
    sh(['gcc', '-std=c11', '-O0', '-g', '-DNDEBUG', '-DCTRL_REENTRY_ASSERT', *kinds[k], '-I', tree/'include', '-c', c, '-o', f'{b}.o'])
    sh(['g++', *kinds[k], f'{b}.o', work/f'test_adp.{k}.o', work/f'main.{k}.o', *ld, '-o', b])
    r = subprocess.run([b], text=True, errors='replace', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env={**os.environ, 'ASAN_OPTIONS': 'detect_leaks=1:halt_on_error=1'})
    fails = sorted({l.split('] ')[1].split(',')[0].split(' (')[0].split('/')[1 if l.count('/') > 1 else 0] for l in r.stdout.splitlines() if l.startswith('[  FAILED  ] ') and 'test' not in l})
    san = 'asan-report' if 'ERROR: AddressSanitizer' in r.stdout else ''
    return f"{k:5s} {'PASS  ' if r.returncode == 0 else 'CAUGHT'} rc={r.returncode} {n}: {' '.join(fails)} {san}"
jobs = [(n, v, k) for k in kinds for n, v in M.items()]
with cf.ThreadPoolExecutor(8) as p:
    for line in p.map(one, jobs): print(line, flush=True)
