"""Run an unchanged complete NxN scenario using its repository build recipe."""
import os, shlex, subprocess, sys, tempfile
from pathlib import Path
root = Path.cwd()
work = root / "tb/verilator/milan_dp"
name = sys.argv[1] if len(sys.argv) > 1 else "obj_nxn"
subprocess.run(["make", "ltn_rom.hex", "ucode.hex"], cwd=work, check=True)
recipe = subprocess.check_output(["make", "-n", "run", "VERILATOR_JOBS=8", "VERILATOR=" + os.environ.get("MILAN_DECL_VERILATOR", "$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator")], cwd=work, text=True)
commands = [shlex.split(line) for line in recipe.replace("\\\n", " ").splitlines() if " --Mdir " + name + " " in line and " --cc " in line]
assert len(commands) == 1, (name, len(commands))
command = commands[0]
mutation = len(sys.argv) > 2 and sys.argv[2] == 'offset'
with tempfile.TemporaryDirectory(prefix='offset-mutant.') as temp:
    if mutation:
        relative = 'hdl/milan/milan_datapath.sv'
        source = (root / relative).read_text()
        old = '? pp_aecp_pt_offset_w[32*k +: 32]'
        new = '? ADP_STROUT_PRES_NS_C[k]'
        assert source.count(old) == 1
        copied = Path(temp) / relative
        copied.parent.mkdir(parents=True)
        copied.write_text(source.replace(old, new))
        (Path(__file__).resolve().parent / 'mutant-offset.sv').write_text(copied.read_text())
        command[command.index('../../../' + relative)] = str(copied)
        name += '_offset_mutant'
        command[command.index('--Mdir') + 1] = name
    print(shlex.join(command), flush=True)
    subprocess.run(command, cwd=work, check=True)
    binary = command[command.index('-o') + 1]
    raise SystemExit(subprocess.run([str(work / name / binary)], cwd=work).returncode)
