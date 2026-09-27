import subprocess, sys
root="/tmp/502-a345"
commands=[
("r329-unchanged", ["python3",root+"/r329_mutants.py",root+"/export",root+"/r329-unchanged"]),
("r328-unchanged", ["python3",root+"/reviewer_mutants.py",root+"/export",root+"/r328-unchanged"]),
("r329-probe-unchanged", ["python3",root+"/r329_probe.py",root+"/export",root+"/r329-probe"]),
]
for label,command in commands:
    result=subprocess.run([sys.executable,root+"/gate.py",label,*command])
    if result.returncode: sys.exit(result.returncode)
