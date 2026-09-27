import subprocess, sys
root="/tmp/502-a345"
commands=[
("r329-reanchored", ["python3",root+"/adapt-reviewers.py",root+"/r329_mutants.py",root+"/export",root+"/r329-reanchored", "M1_drop_map", "M2_drop_name", "M4_wrong_phase_2", "M5_early_phase_4", "M6_add_only", "M8_input_ports_only", "M9_any_phase", "M10_late_mark"]),
("r328-reanchored", ["python3",root+"/adapt-reviewers.py",root+"/reviewer_mutants.py",root+"/export",root+"/r328-reanchored", "drop_name", "drop_map", "phase4_validate", "phase1_begin_commit", "phase0_begin", "phase2_finish", "map_any_phase"]),
("r328-oracle-driver", ["python3",root+"/run-r328-oracle.py"]),
]
for label,command in commands:
    result=subprocess.run([sys.executable,root+"/gate.py",label,*command])
    if result.returncode: sys.exit(result.returncode)
