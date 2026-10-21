#!/usr/bin/env python3
"""Reproduce focused controls and the full-width CRF offset probe.

Usage: python3 run_focused.py REPOSITORY [COMPILER]
All disposable source/build trees stay under this packet's scratch directory.
"""
import concurrent.futures
import io
from pathlib import Path
import subprocess
import sys
import tarfile
import time

PACKET = Path(__file__).resolve().parent
REPO = Path(sys.argv[1]).resolve()
COMPILER = sys.argv[2] if len(sys.argv) > 2 else '$VALIDATION_TOOLS/pinned-verilator-5.050/verilator'
HEAD = '2ff30f0dc5e89be46f8103272883885e8553f4b8'
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip() == HEAD
receipts = PACKET / 'receipts'
receipts.mkdir(exist_ok=True)
work = PACKET / 'scratch' / 'focused'
work.mkdir(parents=True, exist_ok=True)
blob = subprocess.check_output(['git', 'archive', HEAD, 'hdl', 'tb/common', 'tb/verilator/media_phase', 'tb/verilator/mmcm_servo'], cwd=REPO)
with tarfile.open(fileobj=io.BytesIO(blob)) as archive:
    archive.extractall(work, filter='data')
bench = work / 'tb/verilator/media_phase'
source = (bench / 'sim_ofs.cpp').read_text()
anchor = '        // the phase: each AAF output against the CRF timing points, mod Ps\n'
assert source.count(anchor) == 1
addition = '''        // Independent oracle: CRF carries all 64 timestamp bits. The
        // offset is the full Equation (14) result, not the readback's low word.
        int exact_bad = 0;
        double physical_worst = 0;
        for (const auto& c : crf_) {
            if (c.at < from) continue;
            const uint64_t expected_offset = rounded(rows_[kN]);
            if (!frames_.count(c.ts - expected_offset)) exact_bad++;
            const double phase = std::fabs(fold(static_cast<double>(c.ts) - static_cast<double>(*frames_.begin())));
            physical_worst = std::fmax(physical_worst, phase);
        }
        std::printf("  probe: [%s] full offset %llu ns, applied low %u ns, wrong full stamps %d, grid phase %.3f ns\\n",
                    tag, static_cast<unsigned long long>(rounded(rows_[kN])), d_->applied_ns_o[kN], exact_bad, physical_worst);
        std::snprintf(what, sizeof what, "[probe %s] full 64-bit CRF timestamp equals a frame instant plus full Equation (14) offset", tag);
        c_.that(what, exact_bad == 0 && ncrf >= 2);
        std::snprintf(what, sizeof what, "[probe %s] CRF timestamp stays within +/-5 %% of its physical frame grid", tag);
        c_.that(what, physical_worst < kBandNs && ncrf >= 2);
'''
(bench / 'sim_ofs_probe.cpp').write_text(source.replace(anchor, addition + anchor))
makefile = (bench / 'Makefile').read_text()
(bench / 'Probe.mk').write_text(makefile.replace('sim_ofs.cpp -o Vofs_wrap', 'sim_ofs_probe.cpp -o Vofs_wrap'))
# Positive control for the oracle: use the transmitter's existing full-width
# converter on its raw row. No reviewed RTL source is changed.
wrapper = (bench / 'ofs_wrap.sv').read_text()
assert wrapper.count("KL_crf_tx #(.ROUND_MTT_P (1'b0))") == 1
assert wrapper.count('.transit_ns_i (applied_ns_o[N_AAF_P*32 +: 32])') == 1
(bench / 'ofs_control.sv').write_text(wrapper.replace("KL_crf_tx #(.ROUND_MTT_P (1'b0))", "KL_crf_tx #(.ROUND_MTT_P (1'b1))")
    .replace('.transit_ns_i (applied_ns_o[N_AAF_P*32 +: 32])', '.transit_ns_i (raw_ns_i[N_AAF_P*32 +: 32])'))

def run(name, args, expected):
    started = time.monotonic()
    with (receipts / (name + '.log')).open('w') as log:
        log.write('Command: ' + ' '.join(args) + '\n')
        log.flush()
        result = subprocess.run(args, cwd=bench, stdout=log, stderr=subprocess.STDOUT, timeout=580)
    (receipts / (name + '.rc')).write_text(str(result.returncode) + '\n')
    return {'name': name, 'rc': result.returncode, 'expected': expected, 'seconds': round(time.monotonic() - started, 3)}

common = ['make', '-j16', '--no-print-directory', 'VERILATOR=' + COMPILER, 'VERILATOR_JOBS=4']
jobs = [('control-det', common + ['det'], 0),
        ('control-blend', common + ['blend'], 0),
        ('control-ofs', common + ['ofs'], 0),
        ('probe-ofs', common + ['-f', 'Probe.mk', 'OFS_MDIR=obj_probe', 'ofs'], 2),
        ('control-full-width', common + ['-f', 'Probe.mk', 'OFS_WRAP=ofs_control.sv', 'OFS_MDIR=obj_full', 'ofs'], 0)]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(lambda item: run(*item), jobs))
import json
(receipts / 'focused-summary.json').write_text(json.dumps(results, indent=2) + '\n')
for item in results:
    print(item, flush=True)
sys.exit(any(item['rc'] != item['expected'] for item in results))
