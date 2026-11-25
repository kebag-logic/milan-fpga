#!/usr/bin/env python3
"""R931-1 reviewer mutants of the store at the exact head: each applied to a disposable copy, the host suite run at one
shape. A survivor is a defect no test of that shape's suite sees. Usage: r931_mutants.py <checkout> <workdir> <config>"""
import shutil, subprocess, sys
from pathlib import Path
root, work, cfg = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
S, H = 'sw/firmware/ctrl_nvm/nvm_store.c', 'sw/firmware/ctrl_nvm/nvm_shape.h'
M = {
 # the span a save took is forgotten at a failure: the retry (whole) is right, the frame after it lacks the change
 'fail_forgets_span': (S, "\tnvm.tail[nvm.target] = 0u;\n\tnvm.dlen = 0;\n\tnvm.st.last_verdict = vd;",
                       "\tnvm.tail[nvm.target] = 0u;\n\tnvm.dlen = 0;\n\tnvm.cap_lo = nvm.cap_hi = 0u;\n\tnvm.st.last_verdict = vd;"),
 # a whole commit leaves no lag: the next frame into the other slot lacks what the whole commit saved
 'whole_commit_no_lag': (S, "\tnvm.lag_lo = nvm.cap_lo;\n\tnvm.lag_hi = nvm.cap_hi;",
                         "\tnvm.lag_lo = nvm.dlen ? nvm.cap_lo : 0u;\n\tnvm.lag_hi = nvm.dlen ? nvm.cap_hi : 0u;"),
 # a full room's reserve is one largest frame, not two
 'reserve_one_frame': (H, "\t((2u * NVM_DELTA_PAGES_MAX * NVM_FLASH_PAGE < (NVM_DELTA_END - NVM_DELTA_BASE) / 2u) ? \\\n\t 2u * NVM_DELTA_PAGES_MAX",
                       "\t((1u * NVM_DELTA_PAGES_MAX * NVM_FLASH_PAGE < (NVM_DELTA_END - NVM_DELTA_BASE) / 2u) ? \\\n\t 1u * NVM_DELTA_PAGES_MAX"),
 # a change that joined a full room's commit is never retried with a backoff (the shipped behaviour's own gap, made worse)
 'tidy_fail_drops_inflight': (S, "\tif (nvm.tidy) {\n\t\tnvm.tidy = 0;\n\t\treturn;",
                              "\tif (nvm.tidy) {\n\t\tnvm.tidy = 0;\n\t\tnvm_open_clear(&nvm.inflight);\n\t\treturn;"),
 # the frames' span of the other slot taken from its first read only is not reset between reads
 'fr_span_not_reset': (S, "\tnvm.fr_lo[slot] = 0u;\n\tnvm.fr_hi[slot] = 0u;\n\twhile", "\twhile"),
}
name = sys.argv[4] if len(sys.argv) > 4 else None
for k, (path, old, new) in M.items():
    if name and k != name: continue
    tree = work / k
    if tree.exists(): shutil.rmtree(tree)
    shutil.copytree(root, tree, symlinks=True)
    p = tree / path; s = p.read_text()
    assert s.count(old) == 1, (k, s.count(old))
    p.write_text(s.replace(old, new))
    r = subprocess.run([sys.executable, '-B', 'sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py', '--config', cfg, '--jobs', '1'],
                       cwd=tree, capture_output=True, text=True)
    out = r.stdout + r.stderr
    fails = sorted({l.split('[FAIL]')[1].strip()[:150] for l in out.splitlines() if '[FAIL]' in l})
    print(f"{k}: rc {r.returncode} {'CAUGHT' if r.returncode else 'SURVIVED'}; {len(fails)} failing line(s)", *fails[:6], sep='\n   ', flush=True)
    if r.returncode and not fails: print(out[-1500:])
    shutil.rmtree(tree)
