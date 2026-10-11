"""Move only the lane's known ignored test artifacts into disk scratch."""
import shutil
import subprocess
import sys
from pathlib import Path

repo, scratch = (Path(value).resolve() for value in sys.argv[1:])
paths = [
    "avdecc/__pycache__", "configs/generated/ltn_rom.hex", "configs/generated/ucode.hex",
    "scripts/__pycache__", "sw/builder/__pycache__", "sw/builder/out",
    "sw/firmware/ctrl/test/__pycache__", "sw/firmware/ctrl_nvm/test/__pycache__",
    "sw/firmware/gtest/__pycache__", "sw/firmware/nvm_hosttest/__pycache__",
    "sw/litex/__pycache__", "sw/litex/platforms/__pycache__", "sw/mailbox/__pycache__",
    "tb/tools/__pycache__", "tb/verilator/nvm_capture_cpu/__pycache__",
    "tb/verilator/nvm_cosim/build", "tb/verilator/nvm_cosim/runs", "tests/steps/__pycache__",
]
tracked = subprocess.run(["git", "ls-files", "--", *paths], cwd=repo, check=True,
                         capture_output=True, text=True).stdout
assert not tracked, tracked
for relative in paths:
    source = repo / relative
    if not source.exists() and not source.is_symlink():
        continue
    assert source.resolve().is_relative_to(repo), relative
    assert subprocess.run(["git", "check-ignore", "-q", "--", relative], cwd=repo).returncode == 0, relative
    target = scratch / relative
    assert not target.exists(), target
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(target))
    print(relative)
print("Known generated test artifacts moved out of the worktree.")
