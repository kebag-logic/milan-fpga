import fcntl,json,subprocess,sys,os
from pathlib import Path
r=Path(__file__).resolve().parent
lock=(r/"compiler-gates.lock").open("w")
fcntl.flock(lock,fcntl.LOCK_EX)
for label,args in (("compiler-pinned",["--sdk-destination",os.environ["SDK"],"--audit",str(r/"rv32-pinned.jsonl")]),
                   ("compiler-absent",["--absent","--audit",str(r/"rv32-absent.jsonl")]),
                   ("compiler-controls",["--selftest"])):
 receipt=r/(label+".json")
 if receipt.exists() and json.loads(receipt.read_text())["rc"]==0:
  print(label,"already verified",flush=True)
  continue
 subprocess.run([sys.executable,str(r/"run.py"),label,"python3","sw/builder/test_firmware_compiler.py",*args],check=True)
