#!/usr/bin/env python3
"""Independent real-compiler exclusion, loaded-prefix and pool probes.

Usage: python3 scripts/focused_probes.py CHECKOUT PACKET
Run after run_campaigns.py has generated the coverage shape headers.
All compilation and mutation happens below PACKET/scratch.
"""
import copy
import dataclasses
import json
import os
from pathlib import Path
import subprocess
import sys

root, packet = map(lambda p: Path(p).resolve(), sys.argv[1:3])
work = packet / 'scratch' / 'independent-probes'
work.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(root / 'sw/firmware/gtest'))
import fw_coverage as cov

def command(argv, cwd):
    r = subprocess.run(list(map(str, argv)), cwd=cwd, capture_output=True, text=True, check=False)
    if r.returncode:
        raise RuntimeError(f'{Path(str(argv[0])).name} rc={r.returncode}: {r.stderr}')
    return r

def compile_program(source, main, out, includes=()):
    out.mkdir(parents=True, exist_ok=True)
    (out/'main.c').write_text(main)
    command(['gcc', '-std=c11', '-O0', '--coverage', *includes, '-c', source, '-o', out/'source.o'], out)
    command(['gcc', '-std=c11', '-O0', *includes, '-c', out/'main.c', '-o', out/'main.o'], out)
    command(['gcc', '--coverage', out/'source.o', out/'main.o', '-o', out/'probe'], out)
    r = command([out/'probe'], out)
    print(r.stdout, end='')

toy = work / 'toy'
rel = 'sw/firmware/ctrl/probe.c'
src = toy / rel
src.parent.mkdir(parents=True, exist_ok=True)
code = '''int h(int x) {
  if (x == 7)
    return 7;
  if (x == 9)
    return 9;
  return 0;
}
'''
src.write_text(code)
cov.ROOT = toy
row = cov.Exclusion(rel, 'h', 'if (x == 7)', 'arc 1 of 2; line `return 7;`', 'planted excluded case')
data = {}
for name, value in [('control',9), ('swap',7)]:
    out = work / name
    compile_program(src, f'int h(int); int main(void) {{ return h(0)+h({value})-{value}; }}\n', out)
    raw = cov.collect([out])
    data[name] = raw
    kept, findings = cov.apply_exclusions(copy.deepcopy(raw), [row], toy)
    print(f'{name}: raw={cov.tally(raw)} adjusted={cov.tally(kept)} findings={findings}')
    assert bool(findings) == (name == 'swap')
assert cov.tally(data['control']) == cov.tally(data['swap']), 'not a compensating swap'
floor = cov.tally(cov.apply_exclusions(copy.deepcopy(data['control']), [row], toy)[0])
kept, findings = cov.apply_exclusions(copy.deepcopy(data['swap']), [row], toy)
assert findings or cov.compare(cov.tally(kept), floor)
for name, changed in [
    ('renamed-statement', dataclasses.replace(row, statement='if (x == 8)')),
    ('renamed-line', dataclasses.replace(row, uncovered='arc 1 of 2; line `return 8;`')),
    ('wrong-arc-position', dataclasses.replace(row, uncovered='arc 2 of 2; line `return 7;`')),
    ('shorter-arc-vector', dataclasses.replace(row, uncovered='arc 1 of 4; line `return 7;`')),
]:
    _, found = cov.apply_exclusions(copy.deepcopy(data['control']), [changed], toy)
    assert found, name
    print(f'{name}: REFUSED {found}')
print('compensating swap and identity controls PASS')

multi = 'sw/firmware/ctrl/multiline.c'
msrc = toy/multi
msrc.write_text('int m(int a, int b) {\n  if (a > 0 &&\n      b > 0)\n    return 1;\n  return 0;\n}\n')
mrow = cov.Exclusion(multi, 'm', 'if (a > 0 &&', 'arc 4 of 4', 'second operand never false in control')
for name, calls in [('multiline-control','m(1,1)+m(0,0)-1'), ('multiline-swap','m(1,0)+m(0,0)')]:
    out = work/name
    compile_program(msrc, f'int m(int,int); int main(void) {{ return {calls}; }}\n', out)
    raw = cov.collect([out])
    data[name] = raw
    kept, findings = cov.apply_exclusions(copy.deepcopy(raw), [mrow], toy)
    print(f'{name}: raw={cov.tally(raw)} findings={findings}')
    assert bool(findings) == (name == 'multiline-swap')
print('multiline controls PASS')
(packet/'receipts/exclusion-measurements.json').write_text(json.dumps(
    {name: {file: dataclasses.asdict(source) for file, source in measure.items()} for name,measure in data.items()},
    indent=2)+'\n')

cov.ROOT = root
gen = packet/'scratch/coverage/ctrl_nvm/shapes/endstation_ax7101_1x1_tdm8/suite/gen'
assert (gen/'nvm_shape_gen.h').is_file(), 'coverage shape headers not ready'
codec_main = r'''#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "nvm_klj2.h"
int main(void) {
  uint8_t whole[NVM_IMG_LEN], h40[40], h47[47], h48[48];
  nvm_klj2_blank(whole);
  assert(nvm_klj2_check(whole, sizeof whole) == NVM_VD_OK);
  memcpy(h40, whole, sizeof h40); memcpy(h47, whole, sizeof h47);
  assert(nvm_klj2_check_body(h40, sizeof whole, sizeof h40) == NVM_VD_REC);
  assert(nvm_klj2_check_body(h47, sizeof whole, sizeof h47) == NVM_VD_REC);
  printf("codec: exact 40-byte and 47-byte blank prefixes refused REC\n");
  for (struct nvm_rec r=nvm_rec_first(); r.ok; r=nvm_rec_next(r)) {
    uint8_t *rec=whole+NVM_KLJ2_HDR+r.off;
    memset(rec+NVM_REC_HDR, 0, r.plen); nvm_rec_frame(rec,r);
  }
  nvm_klj2_seal(whole);
  assert(nvm_klj2_check(whole,sizeof whole)==NVM_VD_OK);
  memcpy(h48,whole,sizeof h48);
  assert(nvm_klj2_check_body(h48,sizeof whole,sizeof h48)==NVM_VD_REC);
  printf("codec: exact 48-byte framed prefix refused REC; full framed image accepted\n");
  return 0;
}
'''
codec = root/'sw/firmware/ctrl_nvm/nvm_klj2.c'
compile_program(codec,codec_main,work/'codec',[f'-I{gen}', f'-I{codec.parent}'])
cm = cov.collect([work/'codec'])
guard = cm['sw/firmware/ctrl_nvm/nvm_klj2.c'].lines[350]
print('codec header loaded guard:',dataclasses.asdict(guard))
assert len(guard.arcs)==2 and all(guard.arcs)
print('codec loaded-prefix boundary probe PASS')

pool_main = r'''#include <assert.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include "ctrl_pool.h"
int main(void) {
  _Alignas(max_align_t) unsigned char arena[512];
  struct ctrl_pool p;
  const struct ctrl_pool_class classes[]={{32,2}};
  assert(ctrl_pool_init(&p,arena,sizeof arena,classes,1));
  void *a=ctrl_pool_alloc(&p,24), *b=ctrl_pool_alloc(&p,24);
  assert(a && b); ctrl_pool_free(&p,a); ctrl_pool_free(&p,b);
  void *end=NULL; memcpy(b,&end,sizeof end);
  assert(ctrl_pool_alloc(&p,24)==b);
  assert(ctrl_pool_alloc(&p,24)==NULL);
  assert(p.bins[0].free_count==1 && p.refused==1);
  printf("pool: free_count=1 with empty list refused and counted once\n");
  return 0;
}
'''
pool = root/'sw/firmware/ctrl/port/ctrl_pool.c'
compile_program(pool,pool_main,work/'pool',[f'-I{pool.parent}'])
pm=cov.collect([work/'pool'])
print('pool guard:', dataclasses.asdict(pm['sw/firmware/ctrl/port/ctrl_pool.c'].lines[115]))
print('pool public corruption probe PASS')
print('independent focused probes PASS')
