import subprocess,sys
from pathlib import Path
r=Path(__file__).resolve().parent
commands=[
("coverage-selftest",["python3","sw/firmware/gtest/fw_coverage.py","--selftest"]),
("rv32-selftest",["python3","sw/firmware/gtest/fw_rv32_selftest.py","--require-rv32"]),
("tally-mutants",["python3","sw/firmware/gtest/tally_selftest.py","--mutants"]),
("mailbox-contract",["python3","sw/mailbox/gen_mailbox.py","--check"]),
("docs-selftest",["python3","scripts/docs_check.py","--selftest"])]
for label,command in commands:
 result=subprocess.run([sys.executable,str(r/"run.py"),label,*command],timeout=550)
 if result.returncode: raise SystemExit(result.returncode)
