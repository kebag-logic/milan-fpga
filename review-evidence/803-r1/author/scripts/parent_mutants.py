"""parent_mutants.py <clone> <out-dir> <mutant|C0:suite> [...] | --list   (SUITES_ONLY=a,b restricts the suites)

#803: the parent checks the two companions add or re-grade, each made to fail by a planted defect. One defect at a
time, in a clean clone at the head: plant it, build the named suites from scratch, run them, restore the file and
require that every check the mutant names prints FAIL. A clean pass (no mutant) is run first in the same clone and
must print no FAIL at all, so every named check is reached clean and graded red only by its defect.

Parent defects are the companion RTL reverted one property at a time. Engine defects are the donor's own planted
texts, taken by name from gptp-processor/tb/verilator/engine/mutants.py (its MUTATIONS, RECEIPT_MUTATIONS and the
parser arm's PARSER_EDITS), so the parent and the donor arm plant the same defect.
"""
import importlib.util
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

CLONE = Path(sys.argv[1]) if len(sys.argv) > 2 else None

SHADOW = 'hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv'
DP = 'hdl/milan/milan_datapath.sv'
ENGINE = 'gptp-processor/hdl/top/KL_gptp_engine.sv'

# suite -> (directory, the commands of one fresh build and run, relative to the clone)
SUITES = {
    'gptp_shadow': ['make -C tb/verilator/gptp_shadow clean', 'make -C tb/verilator/gptp_shadow run'],
    'milan_dp_gptp_leg': ['rm -rf tb/verilator/milan_dp/obj_gptp tb/verilator/milan_dp/gptp_ucode.hex',
                          'make -C tb/verilator/milan_dp gptp'],
    'tsn_fuzz_ptp': ['make -C tb/verilator/tsn_fuzz clean', 'make -C tb/verilator/tsn_fuzz ptp'],
    'phc_step': ['make -C tb/verilator/gptp_plane clean', 'cd tb/verilator/gptp_plane && python3 phc_step.py'],
    'physical': ['rm -rf tb/verilator/milan_dp/obj_ax1x1gptp tb/verilator/milan_dp/gptp_ax1x1_ucode.hex',
                 'make -C tb/verilator/milan_dp ax1x1gptp'],
}


def donor_tables(clone):
    here = clone / 'gptp-processor/tb/verilator/engine'
    sys.path.insert(0, str(here))
    spec = importlib.util.spec_from_file_location('donor_engine_mutants', here / 'mutants.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    table = {}
    for name, rel, pattern, replacement, _checks in mod.MUTATIONS + mod.RECEIPT_MUTATIONS:
        table[name] = ('gptp-processor/hdl/' + rel, mod.edits_of(pattern, replacement))
    for name, edits in mod.PARSER_EDITS.items():
        table.setdefault(name, ('gptp-processor/hdl/wire/KL_gptp_rx_parser.sv', list(edits)))
    return table


# (name, file, edits or donor name, suites, {suite: [checks that must print FAIL]})
PARENT = [
    ('P1 the shadow path generation ignores entry 0', SHADOW,
     [("  wire pub_path_changed_w = (pub_path_count_next_w != pub_path_count_o)\n"
       "      || (pub_path_next_w != pub_path_o);\n",
       "  wire pub_path_changed_w = (pub_path_count_next_w != pub_path_count_o)\n"
       "      || (pub_path_next_w[8*64-1:64] != pub_path_o[8*64-1:64]);\n")],
     {'gptp_shadow': ['entry-0-only change spends one path generation'],
      'milan_dp_gptp_leg': ['entry-0-only change advances generation once']}),
    ('P2 the shadow publishes no entry 0', SHADOW,
     [("        if (4'(pk + 1) <= pub_path_count_next_w)\n",
       "        if (pk != 0 && 4'(pk + 1) <= pub_path_count_next_w)\n")],
     {'gptp_shadow': ['published path head is the received head',
                      'explicit one-entry PathTrace head is the GM',
                      'empty PathTrace publishes thisClock at entry 0',
                      'path headed elsewhere publishes the received head',
                      'entry-0-only change publishes the new head'],
      'milan_dp_gptp_leg': ['#88 post-cut response is {thisClock}',
                            '#88 GET_AS_PATH entry 0 is the received head',
                            'entry-0-only change: GET_AS_PATH serves the new entry 0']}),
    ('P3 GET_AS_PATH entry 0 is the grandmaster again', DP,
     [("  wire [63:0] asp_owner_head_w = GPTP_PLANE_EN_P ? gptp_pub_path_head_w\n",
       "  wire [63:0] asp_owner_head_w = GPTP_PLANE_EN_P ? cfg_adp_gptp_gm\n")],
     {'milan_dp_gptp_leg': ['#87 TLV-less GM switch: GET_AS_PATH entry 0 is still GMID',
                            '#88 post-cut response is {thisClock}',
                            '#88 GET_AS_PATH entry 0 is the received head',
                            'entry-0-only change: GET_AS_PATH serves the new entry 0']}),
    ('P4 the AS_PATH notification ignores entry 0', DP,
     [("                    && ((asp_live_head_w != gsi_asp_head_q_r)\n",
       "                    && ((1'b0)\n")],
     {'milan_dp_gptp_leg': ['entry-0-only change emits one GET_AS_PATH push']}),
    ('P5 the CSR face takes entries 0..6 as its tail', DP,
     [("  wire [7*64-1:0] gptp_pub_path_tail_w = gptp_pub_path_w[8*64-1:64];\n",
       "  wire [7*64-1:0] gptp_pub_path_tail_w = gptp_pub_path_w[7*64-1:0];\n")],
     {'milan_dp_gptp_leg': ['#87 TLV-less GM switch: GET_AS_PATH still ends with thisClock',
                            '#88 GET_AS_PATH entry 1 is the parent',
                            '#88 GET_AS_PATH ends with thisClock']}),
    # the #207 full-queue arm, rewritten by the PR #92 companion: an engine that stops counting the refused event
    ('P6 a full event queue refuses without counting', ENGINE,
     [("      if (pev_valid_w && (evq_full_w || ann_reject_w))\n",
       "      if (pev_valid_w && ann_reject_w)\n")],
     {'milan_dp_gptp_leg': ['a full queue moves only the event count']}),
]
DONOR = [
    ('D1 a TLV-less Announce publishes {thisClock} (#87)', 'a TLV-less Announce publishes {thisClock}',
     {'gptp_shadow': ['TLV-less selected PathTrace keeps its count', 'TLV-less selected path keeps its head',
                      'better TLV-less Announce keeps the previous count', 'TLV-less refresh keeps the explicit path'],
      'milan_dp_gptp_leg': ['TLV-less fabric publication keeps the path count',
                            'TLV-less GM switch keeps the path count',
                            '#87 TLV-less GM switch: GET_AS_PATH keeps count five']}),
    ('D2 the empty sequence published without a TLV (#87, the 2020 rule)', 'the empty sequence published without a TLV',
     {'gptp_shadow': ['TLV-less selected PathTrace keeps its count', 'TLV-less selected path keeps its head'],
      'milan_dp_gptp_leg': ['TLV-less fabric publication keeps the path count',
                            '#87 TLV-less GM switch: GET_AS_PATH keeps count five']}),
    ('D3 the received head replaced by the grandmaster (#88)', 'the received head replaced by the grandmaster',
     {'gptp_shadow': ['path headed elsewhere publishes the received head',
                      'entry-0-only change publishes the new head'],
      'milan_dp_gptp_leg': ['#88 GET_AS_PATH entry 0 is the received head',
                            'entry-0-only change: GET_AS_PATH serves the new entry 0']}),
    ('D4 the path-head refusal restored (#88)', 'the path-head refusal restored',
     {'gptp_shadow': ['path headed elsewhere publishes count three'],
      'milan_dp_gptp_leg': ['#88 path headed elsewhere serves count three'],
      'tsn_fuzz_ptp': ['better vector, path-trace head is not the announced grandmaster (10.3.10.2.1): adopted',
                       'better vector, path-trace head is not the announced grandmaster (10.3.10.2.1): '
                       'parser drop counter unmoved']}),
    ('D5 the path-count refusal restored (#88)', 'the path-count refusal restored',
     {'tsn_fuzz_ptp': ['better vector, one path-trace hop against stepsRemoved 1 (10.3.10.2.1): adopted',
                       'better vector, one path-trace hop against stepsRemoved 1 (10.3.10.2.1): '
                       'parser drop counter unmoved',
                       'better vector, stepsRemoved 255 on a one-hop path trace (10.3.10.2.1b): '
                       'parser drop counter unmoved']}),
    ('D6 the empty-path refusal restored (#88)', 'the empty-path refusal restored',
     {'gptp_shadow': ['empty PathTrace publishes count one'],
      'milan_dp_gptp_leg': ['empty PathTrace serves count one', '#88 post-cut response is {thisClock}']}),
    ('D7 lost responses clear asCapable at the fourth (#90)', 'lost responses clear asCapable at the fourth',
     {'phc_step': ['asCapable falls at the fifth unanswered request after a crossing exchange',
                   'asCapable falls at the fourth unanswered request after an unanswered crossing request']}),
]
PHYSICAL = [
    ('X7 lost responses clear asCapable at the fourth (#90), physical leg', 'lost responses clear asCapable at the fourth',
     {'physical': ['five unanswered Pdelay intervals elapsed']}),
    ('X8 a sync receipt timeout only clears sync-ok (#89), physical leg', 'a sync receipt timeout only clears sync-ok',
     {'physical': ['the 375 ms Sync timeout makes this station grandmaster']}),
]


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
    # the field campaigns rewrite their artifacts' date stamps on every run (the sweep restores them the same way)
    subprocess.run(['git', '-C', str(CLONE), 'checkout', '--', 'hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md',
                    'hdl/ieee1722/avtp/doc/TEST_RESULTS.md'], check=True)
    dirty = subprocess.run(['git', '-C', str(CLONE), 'status', '--porcelain', '--untracked-files=no',
                            '--ignore-submodules=none'], capture_output=True, text=True).stdout
    assert dirty == '', dirty


def fails_of(text):
    """Every check name a harness printed as failing: `FAIL <name> got ...` (C++), `[FAIL] <name>` (Python)."""
    out = []
    for line in text.splitlines():
        m = re.match(r'\s*\[FAIL\]\s+(.*?)\s{2,}', line + '  ') or re.match(r'\s*FAIL\s+(.*?)\s+got\s', line) \
            or re.match(r'\s*\[FAIL\]\s+(.*)$', line) or re.match(r'\s*FAIL\s+(.*)$', line)
        if m:
            out.append(m.group(1).strip())
    return out


def main():
    if sys.argv[1] == '--list':
        for row in PARENT + DONOR + PHYSICAL:
            print(row[0])
        return 0
    out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    wanted = sys.argv[3:]
    donor = donor_tables(CLONE)
    rows = []
    for name, rel, edits, expect in PARENT:
        rows.append((name, rel, edits, expect))
    for name, dname, expect in DONOR + PHYSICAL:
        rel, edits = donor[dname]
        rows.append((name, rel, edits, expect))
    results = []
    for suite in [w.split(':', 1)[1] for w in wanted if w.startswith('C0:')]:
        # the clean pass: no mutant, the same fresh build, no FAIL at all
        slog = out / f'C0-{suite}.log'
        slog.write_text('')
        rc = 0
        for cmd in SUITES[suite]:
            rc = sh(cmd, slog)
            if rc:
                break
        failed = fails_of(slog.read_text())
        row = dict(mutant=f'C0 clean {suite}', rc=rc, all_failed=failed,
                   verdict='CLEAN' if rc == 0 and not failed else 'NOT CLEAN')
        results.append(row)
        print(f"{row['verdict']:8} C0 clean {suite}", flush=True)
        (out / 'results.json').write_text(json.dumps(results, indent=1) + '\n')
    for name, rel, edits, expect in rows:
        if not any(name.startswith(w + ' ') or name == w for w in wanted):
            continue
        only = [s for s in os.environ.get('SUITES_ONLY', '').split(',') if s]
        if only:
            expect = {s: c for s, c in expect.items() if s in only}
            if not expect:
                continue
        tag = name.split()[0]
        log = out / f'{tag}.log'
        log.write_text(f'# {name}\n# file {rel}\n')
        path = CLONE / rel
        text = path.read_text()
        counts = []
        for pattern, replacement in edits:
            counts.append(text.count(pattern))
            text = text.replace(pattern, replacement)
        row = dict(mutant=name, file=rel, pattern_counts=counts, suites={})
        if not all(c >= 1 for c in counts):
            row['verdict'] = 'NOT PLANTED'
            results.append(row)
            continue
        path.write_text(text)
        try:
            for suite, checks in expect.items():
                slog = out / f'{tag}-{suite}.log'
                slog.write_text('')
                rc = 0
                for cmd in SUITES[suite]:
                    rc = sh(cmd, slog)
                    if rc:
                        break
                failed = fails_of(slog.read_text())
                missing = [c for c in checks if not any(f == c or f.startswith(c) for f in failed)]
                row['suites'][suite] = dict(rc=rc, named=checks, failed_named=[c for c in checks if c not in missing],
                                            not_failed=missing, all_failed=failed)
        finally:
            restore(rel)
        row['verdict'] = 'KILLED' if expect and all(not s['not_failed'] for s in row['suites'].values()) else \
            ('NO CHECK NAMED' if not expect else 'ESCAPED')
        results.append(row)
        print(f"{row['verdict']:8} {name}", flush=True)
        (out / 'results.json').write_text(json.dumps(results, indent=1) + '\n')
    (out / 'results.json').write_text(json.dumps(results, indent=1) + '\n')
    return 0 if all(r['verdict'] in ('KILLED', 'CLEAN') for r in results) else 1


if __name__ == '__main__':
    sys.exit(main())
