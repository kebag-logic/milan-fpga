"""parent_mutants.py <clone> <out-dir> <C0|tag> [...] | --list

#806 (the #803 lane's runner, its rows replaced): every #94 check of the milan_dp gptp leg, each made to fail by a
planted defect. One defect at a time, in a clean clone at the head: plant it, build the leg from scratch, run it,
restore the file and require that every check the defect names prints FAIL. `C0` is the clean pass in the same
clone: the same fresh build with no defect, which must print no FAIL at all, so every named check is reached clean
and graded red only by its defect.

Parent defects (P) break the wiring this adoption adds, one property at a time. Engine defects (D) are the donor's
own planted texts, taken by name from gptp-processor/tb/verilator/engine/port_mutants.py (PORT_MUTATIONS), so the
parent leg and the donor arm plant the same defect.
"""
import importlib.util
import json
import re
import subprocess
import sys
import time
from pathlib import Path

CLONE = Path(sys.argv[1]) if len(sys.argv) > 2 else None

SHADOW = 'hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv'
DP = 'hdl/milan/milan_datapath.sv'
LEG = ['rm -rf tb/verilator/milan_dp/obj_gptp tb/verilator/milan_dp/gptp_ucode.hex',
       'make -C tb/verilator/milan_dp gptp VERILATOR_JOBS=4']

LOSS = '#94 asCapable falls at link loss'
CTRL = '#94 asCapable falls when LINK_CTRL[0] withdraws the link'
GUARD = '#94 asCapable falls when the guard loses the receive clock'
CEASE = '#94 a link loss inside the cease ends it: a Pdelay_Req within one interval of the return'
COUNT = '#94 the cease countdown exit is unchanged: 5 s from the last request'
PRE = ['#94 asCapable is TRUE before the link loss',
       '#94 asCapable is TRUE before LINK_CTRL[0] withdraws the link',
       '#94 asCapable is TRUE before the guard loses the receive clock']

SHADOW_PORT = '      .port_enabled_i     (port_enabled_i),\n'
DP_PORT = '        .port_enabled_i  (eff_link_w),\n'

# (tag, name, file, [(pattern, replacement)], [checks that must print FAIL])
PARENT = [
    ('P1', 'KL_gptp_shadow ties the engine portEnabled high', SHADOW,
     [(SHADOW_PORT, '      .port_enabled_i     (1\'b1),\n')], [LOSS, CTRL, CEASE, GUARD]),
    ('P2', 'KL_gptp_shadow ties the engine portEnabled low', SHADOW,
     [(SHADOW_PORT, '      .port_enabled_i     (1\'b0),\n')], PRE),
    ('P3', 'the datapath drives portEnabled from the PHY link alone', DP,
     [(DP_PORT, '        .port_enabled_i  (i_link_up),\n')], [CTRL, GUARD]),
    ('P4', 'the datapath portEnabled ignores LINK_CTRL[0]', DP,
     [(DP_PORT, '        .port_enabled_i  (i_link_up & (cfg_linkg_dis | linkg_est_w)),\n')], [CTRL]),
    ('P5', 'the datapath portEnabled ignores the link guard estimate', DP,
     [(DP_PORT, '        .port_enabled_i  (i_link_up & cfg_sw_link),\n')], [GUARD]),
]
# (tag, the donor control's name in PORT_MUTATIONS, [checks that must print FAIL])
DONOR = [
    ('D1', 'a portEnabled edge keeps the cease', [CEASE]),
    ('D2', 'the falling edge raises no event', [LOSS, CTRL, GUARD]),
    ('D3', 'slot 6 runs no NOT_ENABLED leg', [LOSS, CTRL, CEASE, GUARD]),
    ('D4', 'the countdown loads one beat less', [COUNT]),
    ('D5', 'the cease entry ends the cease at once', [COUNT]),
]


def donor_table(clone):
    """{name: (file, [(pattern, replacement)])} from the donor's PORT_MUTATIONS, as its arm plants them."""
    here = clone / 'gptp-processor/tb/verilator/engine'
    sys.path.insert(0, str(here))
    spec = importlib.util.spec_from_file_location('donor_port_mutants', here / 'port_mutants.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    table = {}
    for name, rel, pattern, replacement, _checks in mod.PORT_MUTATIONS:
        edits = list(pattern) if replacement is None else [(pattern, replacement)]
        table[name] = ('gptp-processor/hdl/' + rel, edits)
    return table


def sh(cmd, log):
    start = time.time()
    with open(log, 'a') as handle:
        handle.write(f'$ {cmd}\n')
        handle.flush()
        rc = subprocess.run(['bash', '-c', cmd], cwd=CLONE, stdout=handle, stderr=subprocess.STDOUT).returncode
        handle.write(f'[rc={rc} {time.time() - start:.0f}s]\n')
    return rc


def restore(rel):
    if rel.startswith('gptp-processor/'):
        subprocess.run(['git', '-C', str(CLONE / 'gptp-processor'), 'checkout', '--', rel[len('gptp-processor/'):]],
                       check=True)
    else:
        subprocess.run(['git', '-C', str(CLONE), 'checkout', '--', rel], check=True)
    dirty = subprocess.run(['git', '-C', str(CLONE), 'status', '--porcelain', '--untracked-files=no',
                            '--ignore-submodules=none'], capture_output=True, text=True).stdout
    assert dirty == '', dirty


def fails_of(text):
    """Every check name the leg printed as failing: `FAIL <name> got ...`."""
    out = []
    for line in text.splitlines():
        m = re.match(r'\s*FAIL\s+(.*?)\s+got\s', line) or re.match(r'\s*FAIL\s+(.*)$', line)
        if m:
            out.append(m.group(1).strip())
    return out


def run_leg(log):
    log.write_text('')
    rc = 0
    for cmd in LEG:
        rc = sh(cmd, log)
        if rc:
            break
    return rc


def main():
    if sys.argv[1] == '--list':
        for row in PARENT:
            print(row[0], row[1])
        for row in DONOR:
            print(row[0], row[1])
        return 0
    out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    wanted = sys.argv[3:]
    donor = donor_table(CLONE)
    rows = [(tag, name, rel, edits, checks) for tag, name, rel, edits, checks in PARENT]
    rows += [(tag, name) + donor[name] + (checks,) for tag, name, checks in DONOR]
    results = []
    if 'C0' in wanted:
        log = out / 'C0.log'
        rc = run_leg(log)
        failed = fails_of(log.read_text())
        results.append(dict(mutant='C0 clean milan_dp gptp leg', rc=rc, all_failed=failed,
                            verdict='CLEAN' if rc == 0 and not failed else 'NOT CLEAN'))
        print(f"{results[-1]['verdict']:8} C0", flush=True)
        (out / 'results.json').write_text(json.dumps(results, indent=1) + '\n')
    for tag, name, rel, edits, checks in rows:
        if tag not in wanted:
            continue
        log = out / f'{tag}.log'
        path = CLONE / rel
        text = path.read_text()
        counts = [text.count(p) for p, _ in edits]
        row = dict(tag=tag, mutant=name, file=rel, pattern_counts=counts, named=checks)
        if not all(c == 1 for c in counts):
            row['verdict'] = 'NOT PLANTED'
            results.append(row)
            print(f"{row['verdict']:8} {tag} {name}", flush=True)
            continue
        for pattern, replacement in edits:
            text = text.replace(pattern, replacement)
        path.write_text(text)
        try:
            row['rc'] = run_leg(log)
        finally:
            restore(rel)
        failed = fails_of(log.read_text())
        row['all_failed'] = failed
        row['not_failed'] = [c for c in checks if c not in failed]
        row['verdict'] = 'KILLED' if not row['not_failed'] else 'ESCAPED'
        results.append(row)
        print(f"{row['verdict']:8} {tag} {name}", flush=True)
        (out / 'results.json').write_text(json.dumps(results, indent=1) + '\n')
    (out / 'results.json').write_text(json.dumps(results, indent=1) + '\n')
    return 0 if all(r['verdict'] in ('KILLED', 'CLEAN') for r in results) else 1


if __name__ == '__main__':
    sys.exit(main())
