import os
"""Run the complete CSR main scenario against all five generated shapes."""
from pathlib import Path
import shlex, subprocess, tempfile, sys
import yaml
root = Path.cwd()
sys.path.insert(0, str(root / 'sw/builder'))
import endstation_builder as eb
work = root / 'tb/verilator/csr'
recipe = subprocess.check_output(['make', '-B', '-n', 'obj_dir/Vcsr_sim', 'VERILATOR=' + os.environ.get('MILAN_DECL_VERILATOR', '$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator')], cwd=work, text=True)
commands = [shlex.split(line) for line in recipe.replace('\\\n', ' ').splitlines() if ' --cc ' in line]
assert len(commands) == 1
mutation = len(sys.argv) > 1 and sys.argv[1] == 'reset-mutant'
cases = [(p, 0) for p in sorted((root / 'configs').glob('endstation_*.yaml'))]
cases += [(root / 'configs/endstation_arty_current.yaml', bits) for bits in (1, 2, 3)]
if mutation:
    cases = cases[:1]
for config, bits in cases:
    raw = yaml.safe_load(config.read_text())
    clock = raw.get('clocking', {})
    co = clock.get('crf_output', {}).get('enabled', False)
    ci = clock.get('crf_sink', True)
    sources = len(raw['streams']['talkers']) + int(co)
    sinks = len(raw['streams']['listeners']) + int(ci)
    talk = ((0x4001 | (0x800 if co else 0)) << 16) | sources
    listen = ((0x4001 | (0x800 if ci else 0)) << 16) | sinks
    command = list(commands[0])
    command[1] = '+incdir+' + str(root / 'configs/generated' / config.stem)
    command[command.index('-j') + 1] = '8'
    command[command.index('-CFLAGS') + 1] += f' -DCSR_DECL_TALK=0x{talk:08x}u -DCSR_DECL_LIST=0x{listen:08x}u'
    command[command.index('-CFLAGS') + 1] += f' -DCSR_SRP_RESET_BITS={bits}u'
    name = 'obj_decl_' + config.stem + (f'_bits{bits}' if bits else '') + ('_reset_mutant' if mutation else '')
    command += ['--Mdir', name]
    print('DECLARATION', config.name, f'ADP {talk:08x}/{listen:08x}', flush=True)
    print(shlex.join(command), flush=True)
    with tempfile.TemporaryDirectory(prefix='csr-declaration.') as temp:
        if bits or mutation:
            fixture = Path(temp)
            raw['srp'].update(enable_at_reset=bool(bits & 1), talker_declare_at_reset=bool(bits & 2), rtl_table=False)
            config_path = fixture / 'case.yaml'
            config_path.write_text(yaml.safe_dump(raw))
            cfg = eb.load_config(config_path)
            csr = fixture / 'milan_csr.sv'
            source = (root / 'hdl/common/csr/milan_csr.sv').read_text()
            if mutation:
                for old, new in (("aaf_ctrl <= AAF_CTRL_RST_C;", "aaf_ctrl <= 32'h0002_0000;"),
                                 ("maap_ctrl  <= MAAP_CTRL_RST_C;", "maap_ctrl  <= 32'h0000_0800;")):
                    assert source.count(old) == 1
                    source = source.replace(old, new)
                (Path(__file__).resolve().parent / 'mutant-reset.sv').write_text(source)
            csr.write_text(source)
            (fixture / 'gen').mkdir()
            header = eb.emit_csr_defaults_svh(cfg)
            (fixture / 'gen/lwsrp_csr_defaults.svh').write_text(header)
            (fixture / 'gen/adp_shape_defaults.svh').write_text(eb.emit_adp_shape_svh(cfg))
            (Path(__file__).resolve().parent / f'csr-reset-bits{bits}.svh').write_text(header)
            command[command.index('../../../hdl/common/csr/milan_csr.sv')] = str(csr)
            command.insert(1, '+incdir+' + str(fixture))
        print('RESET BITS', bits, shlex.join(command), flush=True)
        subprocess.run(command, cwd=work, check=True)
        subprocess.run([str(work / name / 'Vcsr_sim')], cwd=work, check=True)
