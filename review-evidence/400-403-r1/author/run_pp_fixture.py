import os
"""Complete PP-wrapper scenarios with isolated generated declaration fixtures.
No product YAML is changed. VID 73 is deliberately NOT a shipping profile.
"""
import hashlib, shlex, subprocess, sys, tempfile
from pathlib import Path
import yaml
root = Path.cwd()
sys.path.insert(0, str(root / 'sw/builder'))
import endstation_builder as eb
name = sys.argv[1]
mutation = sys.argv[2] if len(sys.argv) > 2 else ''
assert mutation in ('', 'binding', 'adoption')
assert name in ('off', 'crf', 'vid73')
work = root / 'tb/verilator/pp_shadow'
subprocess.run(['make', 'ltn_rom.hex', 'ucode.hex'], cwd=work, check=True)
sources = subprocess.check_output(['make', '-s', '-C', '../milan_dp', 'print-srcs'], cwd=work, text=True).strip()
recipe = subprocess.check_output(['make', '-n', 'run', 'DP_SRCS=' + sources, 'VERILATOR=' + os.environ.get('MILAN_DECL_VERILATOR', '$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator')], cwd=work, text=True)
commands = [shlex.split(line) for line in recipe.replace('\\\n', ' ').splitlines() if ' --cc ' in line]
assert len(commands) == 1
command = commands[0]
with tempfile.TemporaryDirectory(prefix='declaration-fixture.') as temp:
    path = Path(temp)
    raw = yaml.safe_load((root / 'configs/endstation_arty_current.yaml').read_text())
    raw.setdefault('clocking', {}).setdefault('crf_output', {})['enabled'] = name == 'crf'
    config = path / 'fixture.yaml'
    config.write_text(yaml.safe_dump(raw))
    cfg = eb.load_config(config)
    header = eb.emit_adp_shape_svh(cfg)
    if name == 'vid73':
        assert header.count("ADP_SRP_DOM_DEF_VID_C = 16'd2;") == 1
        header = header.replace("ADP_SRP_DOM_DEF_VID_C = 16'd2;", "ADP_SRP_DOM_DEF_VID_C = 16'd73;")
    (path / 'gen').mkdir()
    (path / 'gen/adp_shape_defaults.svh').write_text(header)
    output = Path(__file__).resolve().parent
    (output / ('fixture-' + name + '.svh')).write_text(header)
    print('ISOLATED TEST FIXTURE', name, 'header SHA256', hashlib.sha256(header.encode()).hexdigest(), flush=True)
    command[1] = '+incdir+' + str(path)
    command[command.index('-j') + 1] = '8'
    flags = command.index('-CFLAGS') + 1
    command[flags] += f' -DDECLARATION_VID={73 if name == "vid73" else 2} -DDECLARATION_OUTPUTS={2 if name == "crf" else 1}'
    if mutation:
        relative = 'hdl/milan/KL_pp_shadow.sv' if mutation == 'binding' else 'hdl/milan/milan_datapath.sv'
        original = (root / relative).read_text()
        old, new = (
            ('.SRP_DOM_DEF_VID_P (SRP_DOM_DEF_VID_P)',
             ".SRP_DOM_DEF_VID_P ((SRP_DOM_DEF_VID_P ^ SRP_DOM_DEF_VID_P) | 16'd2)")
            if mutation == 'binding' else
            ('assign lwsrp_op_vid      = pp_cd_srp_class_a_vid_w;',
             'assign lwsrp_op_vid = lwsrp_adopt_valid ? ADP_SRP_DOM_DEF_VID_C[11:0] : pp_cd_srp_class_a_vid_w;'))
        assert original.count(old) == 1
        copied = path / relative
        copied.parent.mkdir(parents=True, exist_ok=True)
        copied.write_text(original.replace(old, new))
        (output / ('mutant-' + mutation + '.sv')).write_text(copied.read_text())
        entry = '../../../' + relative
        assert entry in command
        command[command.index(entry)] = str(copied)
        print('TEST-ONLY PARENT MUTATION', mutation, hashlib.sha256(copied.read_bytes()).hexdigest(), flush=True)
    build_dir = 'obj_declaration_' + name + ('_' + mutation if mutation else '')
    command += ['--Mdir', build_dir]
    print(shlex.join(command), flush=True)
    subprocess.run(command, cwd=work, check=True)
    result = subprocess.run([str(work / build_dir / 'Vpp_shadow_sim')], cwd=work)
    raise SystemExit(result.returncode)
