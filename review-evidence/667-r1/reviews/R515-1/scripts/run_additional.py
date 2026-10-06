#!/usr/bin/env python3
"""Usage: python3 scripts/run_additional.py CHECKOUT SIMULATOR.

Requires run_focused.py's source extraction. Two independent eight-worker
build sequences run concurrently; every child is joined in the foreground.
"""
import concurrent.futures
import os
import run_focused as f

env = os.environ.copy()
env['TMPDIR'] = str(f.SCRATCH)
suite = f.SCRATCH / 'focused-source/tb/verilator/aaf'


def multi():
    obj = f.SCRATCH / 'multi-obj'
    command = [f.SIM, '--cc', '--exe', '--build', '-j', '8', '--top-module',
               'KL_aaf_packetizer', '-GN_TALKERS_P=8', '-GWIRE_CHANS_P=8',
               '--Mdir', str(obj), '-Wno-fatal', '-CFLAGS', '-std=c++17 -O2',
               str(f.REPO / 'hdl/ieee1722/aaf/KL_aaf_packetizer.sv'),
               str(f.ROOT / 'scripts/multi_start.cpp')]
    f.run('multi-build', command, suite, env)
    f.run('multi-run', [str(obj / 'VKL_aaf_packetizer')], suite, env)


def legacy():
    for top, cpp, sources in [
        ('aaf_talker_i2s', 'sim_main.cpp',
         ['../../../hdl/ieee1722/aaf/aaf_talker_i2s.sv', '../../../hdl/common/cdc_pair_fifo.sv']),
        ('aaf_nx_wrap', 'sim_main_nx.cpp',
         ['../../../hdl/ieee1722/aaf/aaf_talker_i2s.sv',
          '../../../hdl/ieee1722/aaf/KL_aaf_capture_i2s.sv',
          '../../../hdl/ieee1722/aaf/KL_aaf_packetizer.sv',
          '../../../hdl/common/cdc_pair_fifo.sv', 'aaf_nx_wrap.sv']),
    ]:
        obj = f.SCRATCH / ('legacy-' + top)
        command = [f.SIM, '--cc', '--exe', '--build', '-j', '8', '--top-module', top,
                   '--Mdir', str(obj), '-Wno-fatal', '-CFLAGS', '-std=c++17 -O2',
                   *sources, str(suite / cpp)]
        f.run(top + '-build', command, suite, env)
        f.run(top + '-run', [str(obj / ('V' + top))], suite, env)


with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    for result in pool.map(lambda function: function(), [multi, legacy]):
        pass
